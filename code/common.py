"""Output conventions shared by the four portfolio examples."""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def options(project, data_help=None):
    parser = argparse.ArgumentParser(description=project)
    parser.add_argument("--out", type=Path, default=Path("results") / project)
    if data_help:
        parser.add_argument("--data", type=Path, help=data_help)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    return args


def save_plot(fig, directory):
    plt.rcParams["svg.hashsalt"] = "yug-portfolio"
    fig.tight_layout()
    fig.savefig(directory / "figure.svg", metadata={"Date": None})
    plt.close(fig)
