"""Checks for the supplied paper implementations; fixtures are synthetic."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def module(slug, filename):
    path = ROOT / "papers" / slug / filename
    spec = importlib.util.spec_from_file_location(path.stem, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


rain = module("rainfall-prediction", "rainfall_analysis.py")
gas = module("gas-sensor-monitoring", "gas_sensor_analysis.py")
thermal = module("brake-thermal-analysis", "thermal_verification.py")


class PaperChecks(unittest.TestCase):
    def weather(self):
        rng = np.random.default_rng(2026)
        rows = []
        for city in rain.CITIES:
            n = 100
            rows.append(pd.DataFrame({
                "date": pd.date_range("2020-01-01", periods=n), "city": city,
                "temperature": rng.normal(28, 3, n),
                "humidity": rng.uniform(30, 95, n),
                "wind_speed": rng.uniform(0.2, 8, n),
                "pressure": rng.normal(1000, 5, n),
                "rainfall": rng.gamma(2, 3, n)}))
        return pd.concat(rows, ignore_index=True)

    def test_calendar_gaps_do_not_become_next_day_labels(self):
        frame = self.weather().query("city == 'Delhi'")
        missing = pd.Timestamp("2020-03-21")
        frame = frame.loc[frame.date != missing]
        prepared = rain.prepare(frame)
        self.assertNotIn(missing, prepared.index)
        self.assertNotIn(missing - pd.Timedelta(days=1), prepared.index)
        observed = frame.set_index("date").rainfall
        np.testing.assert_allclose(prepared.target, observed.loc[prepared.target_date])
        with self.assertRaises(ValueError):
            rain.prepare(pd.concat([frame, frame.iloc[:1]]))

    def test_rainfall_cli_writes_actual_metrics_and_dates(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            frame = self.weather()
            frame.to_csv(path / "weather.csv", index=False)
            subprocess.run([sys.executable, rain.__file__, str(path / "weather.csv"),
                            "--out", str(path / "out")], check=True, capture_output=True)
            metrics = pd.read_csv(path / "out/metrics.csv")
            self.assertEqual(len(metrics), 9)
            for city in rain.CITIES:
                pred = pd.read_csv(path / f"out/{city}_predictions.csv")
                delta = pd.to_datetime(pred.target_date) - pd.to_datetime(pred.origin_date)
                self.assertTrue((delta == pd.Timedelta(days=1)).all())
                actual_mse = np.mean((pred.observed_mm - pred.predicted_mm_raw)**2)
                reported = metrics.query("city == @city and model == 'OLS_raw'").MSE.iloc[0]
                self.assertAlmostEqual(actual_mse, reported)

    def sensor_frame(self):
        rng = np.random.default_rng(42)
        y = np.tile(np.repeat(np.arange(1, 7), 4), 10)
        x = rng.normal(size=(len(y), 128)) + y[:, None] * 0.2
        frame = pd.DataFrame(x, columns=gas.FEATURES)
        frame["batch"] = np.repeat(np.arange(1, 11), 24)
        frame["class"] = y
        return frame

    def test_sensor_cli_preserves_temporal_partition(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            frame = self.sensor_frame()
            frame.to_csv(path / "sensor.csv", index=False)
            subprocess.run([sys.executable, gas.__file__, str(path / "sensor.csv"),
                            "--out", str(path / "out"), "--trees", "5"],
                           check=True, capture_output=True)
            pred = pd.read_csv(path / "out/predictions.csv")
            self.assertTrue((pred.batch >= 7).all())
            np.testing.assert_array_equal(pred.actual, frame.loc[pred.source_row, "class"])
            np.testing.assert_allclose(pred[[f"p_{i}" for i in range(1, 7)]].sum(axis=1), 1)
            split = pd.read_csv(path / "out/split_indices.csv")
            train = split.loc[split.partition == "train", "source_row"]
            self.assertTrue((frame.loc[train, "batch"] <= 6).all())
            self.assertEqual(set(train) & set(pred.source_row), set())

    def test_sensor_rejects_duplicate_and_nonfinite_features(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            frame = self.sensor_frame()
            pd.concat([frame, frame.iloc[:1]]).to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                gas.load_csv(path)
            frame.loc[0, "x1"] = np.inf
            frame.to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, "nonfinite"):
                gas.load_csv(path)

    def test_missing_class_auc_is_undefined(self):
        labels = np.array([1, 2, 3, 4, 5])
        probabilities = np.eye(6)[labels - 1]
        result = gas.evaluate(labels, labels, probabilities)
        self.assertTrue(np.isnan(result["auc_macro_ovr6"]))
        self.assertEqual(result["accuracy"], 1)

    def test_thermal_equilibrium_energy_and_braking_load(self):
        p = dict(thermal.PARAMS)
        cold = dict(p, heat_fraction=0)
        equilibrium = thermal.solve(cold, elements=8, dt=0.1, end=1)
        np.testing.assert_allclose(equilibrium.surface_K, p["ambient"], atol=1e-8)
        heated = thermal.solve(p, elements=10, dt=0.05, end=4)
        expected = (p["heat_fraction"] * p["front_fraction"] / p["rotors"]
                    * 0.5 * p["m_vehicle"] * p["v0"]**2
                    / (2 * np.pi * (p["ro"]**2 - p["ri"]**2)))
        self.assertAlmostEqual(heated.input_J_m2.iloc[-1], expected, places=6)
        np.testing.assert_allclose(heated.input_J_m2 - heated.loss_J_m2,
                                   heated.stored_J_m2, atol=1e-4)


if __name__ == "__main__":
    unittest.main()
