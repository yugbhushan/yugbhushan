"""Daily one-day-ahead OLS. Input units are documented in the paper."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

FEATURES = ["temperature", "humidity", "wind_speed", "pressure", "rainfall"]
CITIES = ["Delhi", "Chennai", "Agra"]

def scores(y, pred):
    e = y - pred
    sst = np.sum((y - y.mean()) ** 2)
    r = np.nan
    if np.ptp(y) > 0 and np.ptp(pred) > 0:
        r = np.corrcoef(y, pred)[0, 1]
    return dict(n=len(y), R=r,
                R2=1-np.sum(e**2)/sst if sst > 0 else np.nan,
                MSE=np.mean(e**2), RMSE=np.sqrt(np.mean(e**2)),
                MAE=np.mean(np.abs(e)), bias=np.mean(pred-y))

def prepare(frame):
    frame = frame.copy()
    frame["date"] = pd.to_datetime(frame["date"], errors="raise")
    if not frame["date"].eq(frame["date"].dt.normalize()).all():
        raise ValueError("Expected daily dates without time components")
    if frame["date"].duplicated().any():
        raise ValueError("Duplicate dates within city")
    frame = frame.set_index("date").sort_index()
    frame = frame.reindex(pd.date_range(frame.index.min(),
                                        frame.index.max(), freq="D"))
    frame.index.name = "date"
    for col in FEATURES:
        frame[col] = pd.to_numeric(frame[col], errors="coerce")
    frame[FEATURES] = frame[FEATURES].replace([np.inf, -np.inf], np.nan)
    bad = ((frame.humidity < 0) | (frame.humidity > 100) |
           (frame.wind_speed < 0) | (frame.pressure <= 0) |
           (frame.rainfall < 0))
    frame.loc[bad, FEATURES] = np.nan
    # Shift on the complete calendar, before missing-row removal.
    frame["target"] = frame.rainfall.shift(-1)
    frame["target_date"] = frame.index + pd.Timedelta(days=1)
    return frame.dropna(subset=FEATURES + ["target"])

def analyse(city, source, out):
    data = prepare(source)
    if len(data) < 40:
        raise ValueError(f"{city}: fewer than 40 complete daily pairs")
    split = int(0.70 * len(data))
    test = data.iloc[split:]
    # Conservative purge: no training label reaches test origin.
    train = data.iloc[:split]
    train = train[train.target_date < test.index.min()]
    if len(train) < 24 or len(test) < 6:
        raise ValueError(f"{city}: insufficient train/test rows")
    x = train[FEATURES].to_numpy(float)
    xt = test[FEATURES].to_numpy(float)
    y = train.target.to_numpy(float)
    yt = test.target.to_numpy(float)
    mu, sd = x.mean(axis=0), x.std(axis=0)
    if np.any(sd == 0):
        raise ValueError(f"{city}: constant training predictor")
    X = np.column_stack([np.ones(len(x)), (x-mu)/sd])
    Xt = np.column_stack([np.ones(len(xt)), (xt-mu)/sd])
    beta, _, rank, singular = np.linalg.lstsq(X, y, rcond=None)
    if rank < X.shape[1]:
        raise ValueError(f"{city}: rank-deficient design matrix")
    pred = Xt @ beta
    baselines = {"OLS_raw": pred,
                 "Persistence": test.rainfall.to_numpy(float),
                 "Train_mean": np.full(len(test), y.mean())}
    rows = []
    for name, estimate in baselines.items():
        rows.append(dict(city=city, model=name, **scores(yt, estimate)))
    raw_slopes = beta[1:] / sd
    raw_intercept = beta[0] - np.dot(raw_slopes, mu)
    pd.DataFrame({"term": ["intercept"] + FEATURES,
                  "coefficient": np.r_[raw_intercept, raw_slopes]}).to_csv(
        out / f"{city}_coefficients.csv", index=False)
    pd.DataFrame({"origin_date": test.index,
                  "target_date": test.target_date.to_numpy(),
                  "observed_mm": yt, "predicted_mm_raw": pred,
                  "residual_mm": yt-pred}).to_csv(
        out / f"{city}_predictions.csv", index=False)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
    axes[0].scatter(yt, pred, s=10)
    lo, hi = min(yt.min(), pred.min()), max(yt.max(), pred.max())
    axes[0].plot([lo, hi], [lo, hi], "k--", linewidth=1)
    axes[0].set(xlabel="Observed (mm)", ylabel="Predicted (mm)")
    axes[1].plot(test.target_date, yt-pred, linewidth=0.8)
    axes[1].axhline(0, color="black", linewidth=0.6)
    axes[1].set(xlabel="Target date", ylabel="Residual (mm)")
    fig.suptitle(city + ": chronological holdout")
    fig.autofmt_xdate(); fig.tight_layout()
    fig.savefig(out / f"{city}_diagnostics.png", dpi=180)
    plt.close(fig)
    print(city, "train", len(train), "test", len(test),
          "condition", singular[0]/singular[-1])
    return rows

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="Daily city meteorology CSV")
    parser.add_argument("--out", default="rainfall_outputs")
    args = parser.parse_args()
    frame = pd.read_csv(args.csv)
    required = {"date", "city", *FEATURES}
    if not required.issubset(frame.columns):
        raise ValueError("Missing columns: " + str(required-set(frame.columns)))
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    rows = []
    for city in CITIES:
        group = frame.loc[frame.city.eq(city)]
        if group.empty:
            raise ValueError("Missing city: " + city)
        rows.extend(analyse(city, group, out))
    metrics = pd.DataFrame(rows)
    metrics.to_csv(out / "metrics.csv", index=False)
    print(metrics.to_string(index=False))

if __name__ == "__main__":
    main()
