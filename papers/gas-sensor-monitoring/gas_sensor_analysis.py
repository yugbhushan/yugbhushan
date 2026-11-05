"""Proposed PCA-RF protocol; original project data/results are not bundled."""
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, balanced_accuracy_score,
    f1_score, roc_auc_score, confusion_matrix, classification_report)

CLASSES = np.arange(1, 7)
FEATURES = [f"x{i}" for i in range(1, 129)]

def evaluate(y, pred, proba):
    aucs = []
    for j, label in enumerate(CLASSES):
        binary = (y == label).astype(int)
        aucs.append(roc_auc_score(binary, proba[:, j])
                    if np.unique(binary).size == 2 else np.nan)
    # Six-class AUC is undefined if any one-vs-rest task lacks positives.
    macro_auc = float(np.mean(aucs)) if np.isfinite(aucs).all() else np.nan
    return dict(n=len(y), accuracy=accuracy_score(y, pred),
        balanced_accuracy=balanced_accuracy_score(y, pred),
        f1_macro6=f1_score(y, pred, labels=CLASSES,
                          average="macro", zero_division=0),
        f1_weighted=f1_score(y, pred, labels=CLASSES,
                            average="weighted", zero_division=0),
        auc_macro_ovr6=macro_auc)

def forest(trees):
    return RandomForestClassifier(n_estimators=trees,
        min_samples_leaf=2, max_features="sqrt",
        class_weight="balanced", random_state=42, n_jobs=-1)

def group_importance(model, X, y, repeats=3):
    rng = np.random.default_rng(42)
    base = balanced_accuracy_score(y, model.predict(X))
    rows = []
    for sensor in range(16):
        cols = slice(8*sensor, 8*(sensor+1))
        drops = []
        for _ in range(repeats):
            shuffled = X.copy()
            order = rng.permutation(len(X))
            shuffled[:, cols] = X[order, cols]
            drops.append(base-balanced_accuracy_score(
                y, model.predict(shuffled)))
        rows.append(dict(sensor=sensor+1,
                         mean_drop=np.mean(drops),
                         std_drop=np.std(drops)))
    return pd.DataFrame(rows)

def load_csv(path):
    data = pd.read_csv(path)
    required = {"batch", "class", *FEATURES}
    if not required.issubset(data.columns):
        raise ValueError("Missing columns: " + str(required-set(data.columns)))
    X = data[FEATURES].apply(pd.to_numeric, errors="raise").to_numpy(float)
    labels = pd.to_numeric(data["class"], errors="raise").to_numpy(float)
    batches = pd.to_numeric(data["batch"], errors="raise").to_numpy(float)
    if not (np.isfinite(X).all() and np.isfinite(labels).all()
            and np.isfinite(batches).all()):
        raise ValueError("Missing or nonfinite data require source-level review")
    if not np.isin(labels, CLASSES).all():
        raise ValueError("Classes must be integers 1 through 6")
    if not np.isin(batches, np.arange(1, 11)).all():
        raise ValueError("Batches must be integers 1 through 10")
    if np.unique(X, axis=0).shape[0] != len(X):
        raise ValueError("Duplicate feature rows: investigate before splitting")
    return X, labels.astype(int), batches.astype(int)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv")
    parser.add_argument("--protocol", choices=["temporal", "random"],
                        default="temporal")
    parser.add_argument("--out", default="gas_sensor_outputs")
    parser.add_argument("--trees", type=int, default=300)
    parser.add_argument("--importance", action="store_true")
    args = parser.parse_args()
    if args.trees < 1:
        raise ValueError("Tree count must be positive")
    X, y, batches = load_csv(args.csv)
    ids = np.arange(len(y))
    if args.protocol == "temporal":
        train, test = ids[batches <= 6], ids[batches >= 7]
    else:
        train, test = train_test_split(ids, test_size=0.20,
                                      stratify=y, random_state=42)
    if len(train) < 6 or len(test) < 6:
        raise ValueError("Insufficient training/test observations")
    if not np.array_equal(np.unique(y[train]), CLASSES):
        raise ValueError("All six classes must occur in training")
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    models = {
      "PCA_RF": Pipeline([("scale", StandardScaler()),
          ("pca", PCA(n_components=0.95, svd_solver="full")),
          ("rf", forest(args.trees))]),
      "RF_no_PCA": Pipeline([("scale", StandardScaler()),
                             ("rf", forest(args.trees))]),
      "Majority": DummyClassifier(strategy="most_frequent")}
    rows = []
    for name, model in models.items():
        model.fit(X[train], y[train])
        pred, prob = model.predict(X[test]), model.predict_proba(X[test])
        if not np.array_equal(model.classes_, CLASSES):
            raise ValueError("Unexpected probability-column class order")
        rows.append(dict(protocol=args.protocol, model=name, batch="all",
                         **evaluate(y[test], pred, prob)))
        for batch in np.unique(batches[test]):
            mask = batches[test] == batch
            rows.append(dict(protocol=args.protocol, model=name,
                batch=int(batch), **evaluate(y[test][mask], pred[mask], prob[mask])))
        if name != "PCA_RF":
            continue
        pca = model.named_steps["pca"]
        pd.DataFrame({"component": np.arange(1, pca.n_components_+1),
          "variance_ratio": pca.explained_variance_ratio_,
          "cumulative": pca.explained_variance_ratio_.cumsum()}).to_csv(
              out / "pca_variance.csv", index=False)
        pd.DataFrame(pca.components_, columns=FEATURES).to_csv(
              out / "pca_loadings.csv", index_label="component_zero_based")
        prediction = pd.DataFrame({"source_row": test,
           "batch": batches[test], "actual": y[test], "predicted": pred})
        for j, label in enumerate(CLASSES):
            prediction[f"p_{label}"] = prob[:, j]
        prediction.to_csv(out / "predictions.csv", index=False)
        report = classification_report(y[test], pred, labels=CLASSES,
                    zero_division=0, output_dict=True)
        pd.DataFrame(report).T.to_csv(out / "classification_report.csv")
        cm = confusion_matrix(y[test], pred, labels=CLASSES)
        pd.DataFrame(cm, index=CLASSES, columns=CLASSES).to_csv(
                    out / "confusion_matrix.csv", index_label="actual")
        fig, ax = plt.subplots(figsize=(5, 4))
        image = ax.imshow(cm, cmap="Blues")
        ax.set(xlabel="Predicted class", ylabel="Actual class",
               xticks=range(6), yticks=range(6),
               xticklabels=CLASSES, yticklabels=CLASSES)
        fig.colorbar(image, ax=ax); fig.tight_layout()
        fig.savefig(out / "confusion_matrix.png", dpi=180); plt.close(fig)
        if args.importance:
            group_importance(model, X[test], y[test]).to_csv(
                      out / "sensor_group_importance.csv", index=False)
        print("Retained PCs:", pca.n_components_)
    pd.DataFrame(rows).to_csv(out / "metrics.csv", index=False)
    pd.DataFrame({"source_row": np.r_[train, test],
       "partition": ["train"]*len(train)+["test"]*len(test)}).to_csv(
                     out / "split_indices.csv", index=False)
    print(pd.DataFrame(rows).to_string(index=False))

if __name__ == "__main__":
    main()
