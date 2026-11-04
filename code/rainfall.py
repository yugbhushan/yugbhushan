"""Forecast next-day rainfall from daily weather with chronological evaluation."""
import numpy as np
import pandas as pd
from common import options, plt, save_plot

FEATURES = ["temp_c", "humidity_pct", "wind_ms", "pressure_hpa", "rain_mm"]
CITIES = ["Delhi", "Chennai", "Agra"]


def demo():
    rng = np.random.default_rng(73)
    frames = []
    for i, city in enumerate(CITIES):
        dates = pd.date_range("2020-01-01", periods=730)
        season = np.sin(2*np.pi*(np.arange(len(dates))/365.25 - 0.22*i))
        temp = 26 + 5*season + rng.normal(0, 2, len(dates))
        humidity = np.clip(62 + 18*season + rng.normal(0, 7, len(dates)), 15, 100)
        wind = rng.uniform(0.5, 6, len(dates))
        pressure = 1008 - 4*season + rng.normal(0, 2, len(dates))
        rain = np.zeros(len(dates))
        for day in range(1, len(dates)):
            rain[day] = max(0, 0.28*(humidity[day-1]-64) + 0.24*rain[day-1] + rng.normal(0, 3))
        frames.append(pd.DataFrame(dict(city=city, date=dates, temp_c=temp, humidity_pct=humidity,
                                        wind_ms=wind, pressure_hpa=pressure, rain_mm=rain)))
    return pd.concat(frames, ignore_index=True)


def main():
    args = options("rainfall", "Daily weather CSV, schema in the project guide")
    data = pd.read_csv(args.data) if args.data else demo()
    data["date"] = pd.to_datetime(data["date"], errors="raise")
    if data.duplicated(["city", "date"]).any() or data[["date", "city"]].isna().any().any():
        raise ValueError("Provide one dated observation per city per day.")
    if set(data.city) != set(CITIES) or not np.isfinite(data[FEATURES]).all().all() or (data.rain_mm < 0).any():
        raise ValueError("Supply finite weather measurements for all three cities and nonnegative rainfall.")
    records, forecasts, coefficients = [], [], []
    fig, axes = plt.subplots(3, 1, figsize=(8, 6))
    for ax, city in zip(axes, CITIES):
        frame = data[data.city == city].sort_values("date").copy()
        frame["target_date"] = frame.date.shift(-1)
        frame["target"] = frame.rain_mm.shift(-1)
        frame = frame[(frame.target_date-frame.date) == pd.Timedelta(days=1)]
        if len(frame) < 40:
            raise ValueError(f"{city} needs at least 40 consecutive-day pairs.")
        split = int(0.8*len(frame))
        x = np.column_stack([np.ones(len(frame)), frame[FEATURES]])
        y = frame.target.to_numpy()
        beta = np.linalg.lstsq(x[:split], y[:split], rcond=None)[0]
        coefficients.append(dict(city=city, **dict(zip(["intercept", *FEATURES], beta))))
        prediction = np.maximum(0, x[split:] @ beta)
        actual = y[split:]
        persistence = x[split:, -1]
        mse = np.mean((actual-prediction)**2)
        r = np.corrcoef(actual, prediction)[0, 1] if min(actual.std(), prediction.std()) > 0 else np.nan
        records.append(dict(city=city, train_pairs=split, test_pairs=len(actual), r=r, rmse_mm=np.sqrt(mse),
                            nmse=mse/actual.var() if actual.var() > 0 else np.nan,
                            persistence_rmse_mm=np.sqrt(np.mean((actual-persistence)**2))))
        dates = frame.target_date.iloc[split:]
        forecasts.append(pd.DataFrame(dict(city=city, target_date=dates, actual_mm=actual, prediction_mm=prediction)))
        ax.plot(dates, actual, lw=1, label="Observed"); ax.plot(dates, prediction, lw=1, label="Forecast")
        ax.set(ylabel=f"{city}\nmm/day")
    axes[0].set_title("Next-day rainfall | " + ("supplied observations" if args.data else "synthetic demonstration"))
    axes[0].legend(ncol=2)
    save_plot(fig, args.out)
    pd.concat(forecasts).to_csv(args.out/"predictions.csv", index=False)
    pd.DataFrame(coefficients).to_csv(args.out/"coefficients.csv", index=False)
    summary = pd.DataFrame(records)
    summary.to_csv(args.out/"metrics.csv", index=False)
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
