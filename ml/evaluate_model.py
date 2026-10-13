"""
ReviewGuard AI - Model Evaluation & Visualization
Computes rigorous classification metrics (Accuracy, Precision, Recall, F1, ROC-AUC)
and generates publication-quality evaluation figures using Matplotlib.
"""

import os
from typing import Dict, Any, Optional
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for headless / server execution
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve,
    classification_report
)

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")

def calculate_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_scores: Optional[np.ndarray] = None
) -> Dict[str, Any]:
    """Calculate standard binary classification metrics for fake review detection."""
    acc = float(accuracy_score(y_true, y_pred))
    prec = float(precision_score(y_true, y_pred, zero_division=0))
    rec = float(recall_score(y_true, y_pred, zero_division=0))
    f1 = float(f1_score(y_true, y_pred, zero_division=0))

    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()

    metrics = {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": {
            "true_negative": int(tn),
            "false_positive": int(fp),
            "false_negative": int(fn),
            "true_positive": int(tp),
            "raw_matrix": cm.tolist()
        },
        "support": {
            "total_samples": int(len(y_true)),
            "genuine_count": int(np.sum(y_true == 0)),
            "fake_count": int(np.sum(y_true == 1))
        }
    }

    if y_scores is not None:
        try:
            auc = float(roc_auc_score(y_true, y_scores))
            metrics["roc_auc"] = round(auc, 4)
        except Exception:
            metrics["roc_auc"] = None
    else:
        metrics["roc_auc"] = None

    return metrics

def plot_confusion_matrix(
    cm: np.ndarray,
    output_path: Optional[str] = None,
    model_name: str = "ReviewGuard Classifier"
) -> str:
    """Plot and save a clean, aesthetic confusion matrix heatmap."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    save_path = output_path or os.path.join(MODELS_DIR, "confusion_matrix.png")

    fig, ax = plt.subplots(figsize=(6, 5), dpi=150)
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#1E293B")

    # Draw matrix cells
    cax = ax.matshow(cm, cmap="Blues", alpha=0.85)
    fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)

    # Label values
    for (i, j), z in np.ndenumerate(cm):
        ax.text(
            j, i, f"{z}",
            ha="center", va="center",
            color="white" if z > cm.max() / 2 else "#94A3B8",
            fontsize=13, fontweight="bold"
        )

    classes = ["Genuine (0)", "Fake (1)"]
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(classes, color="#F8FAFC", fontsize=10)
    ax.set_yticklabels(classes, color="#F8FAFC", fontsize=10)

    ax.tick_params(colors="#94A3B8", bottom=False, top=True, left=True, right=False)
    ax.set_xlabel("Predicted Label", color="#F8FAFC", fontsize=11, labelpad=10)
    ax.set_ylabel("True Label", color="#F8FAFC", fontsize=11, labelpad=10)
    ax.set_title(f"Confusion Matrix — {model_name}", color="#F8FAFC", fontsize=12, pad=15, fontweight="bold")

    plt.tight_layout()
    plt.savefig(save_path, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    return save_path

def plot_roc_curve(
    y_true: np.ndarray,
    y_scores: np.ndarray,
    output_path: Optional[str] = None,
    model_name: str = "ReviewGuard Classifier"
) -> str:
    """Plot and save a sleek ROC Curve."""
    os.makedirs(MODELS_DIR, exist_ok=True)
    save_path = output_path or os.path.join(MODELS_DIR, "roc_curve.png")

    fpr, tpr, _ = roc_curve(y_true, y_scores)
    auc_val = roc_auc_score(y_true, y_scores)

    fig, ax = plt.subplots(figsize=(6, 5), dpi=150)
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#1E293B")

    # Grid
    ax.grid(True, linestyle="--", alpha=0.15, color="#94A3B8")

    # Curve
    ax.plot(fpr, tpr, color="#8B5CF6", lw=2.5, label=f"{model_name} (AUC = {auc_val:.3f})")
    ax.plot([0, 1], [0, 1], color="#64748B", lw=1.5, linestyle="--", label="Random Chance (0.500)")

    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel("False Positive Rate", color="#F8FAFC", fontsize=11)
    ax.set_ylabel("True Positive Rate (Recall)", color="#F8FAFC", fontsize=11)
    ax.set_title(f"ROC Curve — {model_name}", color="#F8FAFC", fontsize=12, pad=15, fontweight="bold")
    ax.tick_params(colors="#94A3B8")

    legend = ax.legend(loc="lower right", facecolor="#0F172A", edgecolor="#334155")
    for text in legend.get_texts():
        text.set_color("#F8FAFC")

    for spine in ax.spines.values():
        spine.set_color("#334155")

    plt.tight_layout()
    plt.savefig(save_path, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    return save_path
