"""Evaluate gas classification on later acquisition batches."""
import re
import numpy as np
import pandas as pd
from sklearn.datasets import load_svmlight_file
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from common import options, plt, save_plot


def demo():
    rng = np.random.default_rng(42)
    centers = rng.normal(0, 0.75, (6, 16))
    drift = rng.normal(0, 0.22, 16)
    batches = np.repeat(np.arange(1, 11), 120)
    labels = np.tile(np.repeat(np.arange(1, 7), 20), 10)
    features = centers[labels - 1] + batches[:, None] * drift + rng.normal(size=(len(labels), 16))
    return features, labels, batches


def load_uci(directory):
    records = []
    for path in sorted(directory.rglob("batch*.dat")):
        match = re.fullmatch(r"batch(\d+)\.dat", path.name)
        if match:
            batch = int(match.group(1))
            features, labels = load_svmlight_file(str(path), n_features=128, zero_based=False)
            records.append((features.toarray(), labels.astype(int), np.full(len(labels), batch)))
    if sorted(int(b[0]) for _, _, b in records) != list(range(1, 11)):
        raise ValueError("Supply exactly one original UCI 224 batch1.dat through batch10.dat.")
    return tuple(np.concatenate(items) for items in zip(*records))


def main():
    args = options("gas", "Extracted UCI 224 dataset directory (optional)")
    x, y, batch = load_uci(args.data) if args.data else demo()
    source = "UCI 224" if args.data else "Seeded synthetic sensor signals"
    train = batch <= 7
    model = make_pipeline(StandardScaler(), PCA(n_components=0.95, svd_solver="full"),
                          RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=1))
    model.fit(x[train], y[train])
    pred = model.predict(x[~train])
    classes = model.classes_
    probabilities = model.predict_proba(x[~train])
    auc = roc_auc_score(y[~train], probabilities, multi_class="ovr", average="macro", labels=classes)
    metrics = dict(source=source, train_rows=int(train.sum()), test_rows=int((~train).sum()),
                   accuracy=accuracy_score(y[~train], pred), macro_f1=f1_score(y[~train], pred, average="macro"),
                   macro_ovr_auc=auc, retained_components=model.named_steps["pca"].n_components_)
    pd.DataFrame([metrics]).to_csv(args.out / "metrics.csv", index=False)
    pd.DataFrame(dict(batch=batch[~train], actual=y[~train], predicted=pred)).to_csv(args.out / "predictions.csv", index=False)
    matrix = confusion_matrix(y[~train], pred, labels=classes)
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.imshow(matrix, cmap="Blues")
    for (i, j), count in np.ndenumerate(matrix):
        ax.text(j, i, str(count), ha="center", va="center", color="white" if count > matrix.max()/2 else "black")
    ax.set(xticks=range(len(classes)), xticklabels=classes, yticks=range(len(classes)), yticklabels=classes,
           xlabel="Predicted class", ylabel="Observed class", title=f"{source} | held-out batches 8–10")
    save_plot(fig, args.out)
    print(metrics)


if __name__ == "__main__":
    main()
