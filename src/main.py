"""
main.py — Run the full ROP modeling pipeline.

Usage:
    python src/main.py

This script:
  1. Loads and cleans the USROP_A 3 N-SH-F-15d drilling dataset.
  2. Fits a Log-MLR (baseline) model and a Bingham (physics-guided) model.
  3. Prints RMSE comparison.
  4. Saves key visualizations to the assets/ folder.
"""

import os
import sys

# Ensure the project root is on the path so `src.model` can be imported
# when running as `python src/main.py` from the project root.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from src.model import (
    load_and_clean_data,
    compute_vif,
    fit_log_mlr,
    fit_bingham,
    evaluate_models,
    plot_correlation_matrix,
    plot_model_comparison,
)


def main():
    # --- Paths ---
    data_path = os.path.join(PROJECT_ROOT, "data", "USROP_A 3 N-SH-F-15d - Final.csv")
    assets_dir = os.path.join(PROJECT_ROOT, "assets")
    os.makedirs(assets_dir, exist_ok=True)

    # --- 1. Load & Clean ---
    print("Loading data...")
    df = load_and_clean_data(data_path)
    print(f"  Rows after cleaning: {len(df):,}")

    # --- 2. VIF Analysis ---
    print("\nVIF — All candidate features:")
    vif_all = compute_vif(df, ["WOB", "RPM", "Torque", "TFLO", "HKLD", "SPPA", "MD"])
    print(vif_all.to_string(index=False))

    print("\nVIF — Final features (WOB, RPM):")
    vif_final = compute_vif(df, ["WOB", "RPM"])
    print(vif_final.to_string(index=False))

    # --- 3. Fit Models ---
    print("\nFitting Log-MLR model...")
    log_model = fit_log_mlr(df)
    print(log_model.summary())

    print("\nFitting Bingham model...")
    K_hat, a_hat = fit_bingham(df)
    print(f"  Estimated K = {K_hat:.6f}")
    print(f"  Estimated a = {a_hat:.6f}")

    # --- 4. Evaluate ---
    results = evaluate_models(df, log_model, K_hat, a_hat)
    print("\n" + "=" * 50)
    print("MODEL COMPARISON")
    print("=" * 50)
    print(f"  Log-MLR (Baseline)       RMSE = {results['Log-MLR RMSE']}")
    print(f"  Bingham (Physics-Guided) RMSE = {results['Bingham RMSE']}")
    print("=" * 50)

    # --- 5. Generate Plots ---
    print("\nGenerating plots...")
    plot_correlation_matrix(df, save_path=os.path.join(assets_dir, "correlation_matrix.png"))
    plot_model_comparison(df, log_model, K_hat, a_hat, save_path=os.path.join(assets_dir, "model_comparison.png"))

    print("\nDone! Check the assets/ folder for output plots.")


if __name__ == "__main__":
    main()
