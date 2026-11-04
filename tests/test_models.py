"""Independent physical checks and end-to-end data-interface checks."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.datasets import dump_svmlight_file

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
from brake import MATERIALS, simulate
from gas import load_uci
from packed_bed import coefficients
from rainfall import demo


class ModelChecks(unittest.TestCase):
    def test_shape_limits_and_balance(self):
        a, b = coefficients(.4, 1., .003, 1.8e-5, 1.2)
        a2, b2 = coefficients(.4, .65, .003, 1.8e-5, 1.2)
        self.assertAlmostEqual(a2/a, .65**-2)
        self.assertAlmostEqual(b2/b, .65**-1)
        with tempfile.TemporaryDirectory() as directory:
            subprocess.run([sys.executable, str(ROOT/"code/packed_bed.py"), "--out", directory], check=True)
            wall = pd.read_csv(Path(directory)/"wall.csv")
            self.assertAlmostEqual(wall.velocity_ms @ wall.area_fraction, 0.2, places=10)
            self.assertGreater(wall.velocity_ms.iloc[-1], wall.velocity_ms.iloc[0])

    def test_brake_equilibrium_and_energy(self):
        for props in MATERIALS.values():
            equilibrium = simulate(props, duration=1, peak_flux=0)
            np.testing.assert_allclose(equilibrium.surface_C, 20, atol=1e-8)
            hot = simulate(props, duration=8)
            self.assertAlmostEqual(hot.input_J_m2.iloc[-1], 1.2e6, places=5)
            np.testing.assert_allclose(hot.stored_J_m2, hot.input_J_m2-hot.loss_J_m2, atol=1e-4)

    def test_uci_format_preserves_batch_identity(self):
        with tempfile.TemporaryDirectory() as d:
            for batch in range(1, 11):
                samples = np.zeros((6, 128))
                samples[:, 0] = batch
                samples[:, -1] = np.arange(6)
                dump_svmlight_file(samples, np.arange(1, 7), str(Path(d)/f"batch{batch}.dat"), zero_based=False)
            x, y, batch = load_uci(Path(d))
            self.assertEqual(x.shape, (60, 128))
            np.testing.assert_array_equal(x[:, 0], batch)
            np.testing.assert_array_equal(x[:, -1], y-1)

    def test_rainfall_uses_next_calendar_day(self):
        with tempfile.TemporaryDirectory() as d:
            frame = demo().groupby("city").head(90)
            frame = frame[frame.date != pd.Timestamp("2020-03-20")]
            csv = Path(d)/"input.csv"
            frame.to_csv(csv, index=False)
            subprocess.run([sys.executable, str(ROOT/"code/rainfall.py"), "--data", str(csv),
                            "--out", d], check=True, capture_output=True)
            forecasts = pd.read_csv(Path(d)/"predictions.csv", parse_dates=["target_date"])
            merged = forecasts.merge(frame, left_on=["city","target_date"], right_on=["city","date"])
            self.assertEqual(len(merged), len(forecasts))
            np.testing.assert_allclose(merged.actual_mm, merged.rain_mm)
            self.assertNotIn(pd.Timestamp("2020-03-21"), forecasts.target_date.tolist())
