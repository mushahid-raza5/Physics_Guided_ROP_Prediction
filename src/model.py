"""
model.py — Physics-Guided ROP Prediction Models

This module implements two approaches to predicting Rate of Penetration (ROP)
during drilling operations:

1. **Log-MLR (Baseline):** A log-transformed multiple linear regression model
   that predicts log(ROP) from Weight on Bit (WOB) and rotary speed (RPM).

2. **Bingham (Physics-Guided):** A nonlinear, physics-based model derived from
   the classical Bingham ROP equation, fitted via Maximum Likelihood Estimation
   (MLE) using scipy's curve_fit.

Dataset: ~53,000 real-time observations from the USROP_A 3 N-SH-F-15d well.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from scipy.optimize import curve_fit


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
BIT_DIAMETER_MM = 444.5  # Bit diameter in mm (constant for this well)


# ---------------------------------------------------------------------------
# Data Loading & Cleaning
# ---------------------------------------------------------------------------
def load_and_clean_data(filepath: str) -> pd.DataFrame:
    """
    Load the drilling dataset and filter out non-physical rows.

    Parameters
    ----------
    filepath : str
        Path to the CSV file. The file is expected to have two header rows
        (row 1 = column names, row 2 = units); the units row is skipped.

    Returns
    -------
    pd.DataFrame
        Cleaned dataframe with rows where ROP > 0, WOB > 0, and RPM > 0.
    """
    df = pd.read_csv(filepath, skiprows=[1])
    df_clean = df[(df["ROP"] > 0) & (df["WOB"] > 0) & (df["RPM"] > 0)].copy()
    return df_clean


# ---------------------------------------------------------------------------
# VIF Analysis
# ---------------------------------------------------------------------------
def compute_vif(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Compute the Variance Inflation Factor (VIF) for each feature.

    VIF quantifies multicollinearity. A VIF > 5–10 indicates that a variable
    is highly correlated with others and should be considered for removal.

    Parameters
    ----------
    df : pd.DataFrame
        The dataframe containing the feature columns.
    columns : list of str
        Column names to include in the VIF calculation.

    Returns
    -------
    pd.DataFrame
        A dataframe with columns 'Variable' and 'VIF'.
    """
    X = df[columns].values
    vif_data = pd.DataFrame()
    vif_data["Variable"] = columns
    vif_data["VIF"] = [variance_inflation_factor(X, i) for i in range(len(columns))]
    return vif_data


# ---------------------------------------------------------------------------
# Log-MLR Model (Baseline)
# ---------------------------------------------------------------------------
def fit_log_mlr(df: pd.DataFrame):
    """
    Fit a log-transformed multiple linear regression model.

    Model: log(ROP) = β₀ + β₁·WOB + β₂·RPM + ε

    This serves as the **baseline** statistical model.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe with columns 'ROP', 'WOB', and 'RPM'.

    Returns
    -------
    statsmodels.regression.linear_model.RegressionResultsWrapper
        The fitted OLS model object.
    """
    y = np.log(df["ROP"])
    X = sm.add_constant(df[["WOB", "RPM"]])
    model = sm.OLS(y, X).fit()
    return model


# ---------------------------------------------------------------------------
# Bingham Model (Physics-Guided)
# ---------------------------------------------------------------------------
def bingham_model(X, K: float, a: float) -> np.ndarray:
    """
    Bingham ROP equation — a physics-based drilling model.

    ROP = K · (WOB / Db)^a · RPM

    where:
        - K  : formation drillability constant (fitted)
        - a  : WOB exponent (fitted)
        - Db : bit diameter in mm (= 444.5, constant for this well)

    Parameters
    ----------
    X : array-like, shape (2, n)
        Stacked array where X[0] = WOB (kkgf) and X[1] = RPM (rpm).
    K : float
        Drillability constant.
    a : float
        Weight-on-bit exponent.

    Returns
    -------
    np.ndarray
        Predicted ROP values in m/h.
    """
    wob, rpm = X
    return K * (wob / BIT_DIAMETER_MM) ** a * rpm


def fit_bingham(df: pd.DataFrame) -> tuple:
    """
    Fit the Bingham ROP model via nonlinear least-squares (MLE).

    Uses scipy.optimize.curve_fit with initial guesses K=1, a=1.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe with columns 'WOB', 'RPM', and 'ROP'.

    Returns
    -------
    tuple of (float, float)
        (K_hat, a_hat) — the estimated parameters.
    """
    wob = df["WOB"].values
    rpm = df["RPM"].values
    rop_obs = df["ROP"].values
    X_data = np.vstack((wob, rpm))

    params_opt, _ = curve_fit(
        bingham_model,
        X_data,
        rop_obs,
        p0=(1.0, 1.0),
        maxfev=20000,
    )
    K_hat, a_hat = params_opt
    return K_hat, a_hat


# ---------------------------------------------------------------------------
# Evaluation
# ---------------------------------------------------------------------------
def evaluate_models(
    df: pd.DataFrame, log_model, K_hat: float, a_hat: float
) -> dict:
    """
    Compute RMSE for both the Log-MLR and Bingham models.

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe.
    log_model : statsmodels OLS result
        Fitted Log-MLR model.
    K_hat, a_hat : float
        Bingham model parameters.

    Returns
    -------
    dict
        {'Log-MLR RMSE': float, 'Bingham RMSE': float}
    """
    rop_obs = df["ROP"].values
    wob = df["WOB"].values
    rpm = df["RPM"].values

    # Bingham predictions
    rop_bingham = bingham_model(np.vstack((wob, rpm)), K_hat, a_hat)
    rmse_bingham = np.sqrt(np.mean((rop_obs - rop_bingham) ** 2))

    # Log-MLR predictions (back-transform from log space)
    X_comp = sm.add_constant(df[["WOB", "RPM"]])
    rop_logmlr = np.exp(log_model.predict(X_comp))
    rmse_logmlr = np.sqrt(np.mean((rop_obs - rop_logmlr) ** 2))

    return {"Log-MLR RMSE": round(rmse_logmlr, 4), "Bingham RMSE": round(rmse_bingham, 4)}


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------
def plot_correlation_matrix(df: pd.DataFrame, save_path: str = None):
    """
    Plot a correlation heatmap for key drilling parameters.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe with drilling columns.
    save_path : str, optional
        If provided, the figure is saved to this path.
    """
    corr_vars = ["ROP", "WOB", "RPM", "Torque", "TFLO", "HKLD", "SPPA", "MD"]
    corr_matrix = df[corr_vars].corr()

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    ax.set_title("Correlation Matrix of Drilling Parameters")
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {save_path}")
    else:
        plt.show()
    plt.close(fig)


def plot_model_comparison(
    df: pd.DataFrame, log_model, K_hat: float, a_hat: float, save_path: str = None
):
    """
    Plot ROP vs RPM with both model curves overlaid (WOB fixed at median).

    Parameters
    ----------
    df : pd.DataFrame
        Cleaned dataframe.
    log_model : statsmodels OLS result
        Fitted Log-MLR model.
    K_hat, a_hat : float
        Bingham model parameters.
    save_path : str, optional
        If provided, the figure is saved to this path.
    """
    median_wob = df["WOB"].median()
    rpm_grid = np.linspace(df["RPM"].min(), df["RPM"].max(), 200)

    # Log-MLR curve
    X_grid_log = pd.DataFrame({"const": 1.0, "WOB": median_wob, "RPM": rpm_grid})
    rop_logmlr = np.exp(log_model.predict(X_grid_log))

    # Bingham curve
    X_grid_bing = np.vstack((np.full_like(rpm_grid, median_wob), rpm_grid))
    rop_bingham = bingham_model(X_grid_bing, K_hat, a_hat)

    # Subsample for scatter readability
    df_sample = df.sample(n=min(3000, len(df)), random_state=42)

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(df_sample["RPM"], df_sample["ROP"], alpha=0.15, s=8, label="Observed", color="#888888")
    ax.plot(rpm_grid, rop_logmlr, linewidth=2.5, label="Log-MLR (Baseline)", color="#2196F3")
    ax.plot(rpm_grid, rop_bingham, linewidth=2.5, linestyle="--", label="Bingham (Physics-Guided)", color="#FF5722")

    ax.set_xlabel("RPM", fontsize=12)
    ax.set_ylabel("ROP (m/h)", fontsize=12)
    ax.set_title(f"ROP vs RPM — Model Comparison (WOB fixed at {median_wob:.1f} kkgf)", fontsize=13)
    ax.legend(fontsize=11)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        print(f"Saved: {save_path}")
    else:
        plt.show()
    plt.close(fig)
