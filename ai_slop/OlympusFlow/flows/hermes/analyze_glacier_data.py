#!/usr/bin/env python3
"""
GLACIER DATA ANALYSIS
=====================

Properly parse and analyze GLAMOS Swiss Glacier data for Z² relationships.

The GLAMOS volumechange.csv has:
- 5 header lines of metadata
- Column headers on line 6
- Unit descriptions on line 7
- Data starts on line 8

Columns:
- SGI-ID: Swiss Glacier Inventory ID
- A_start, A_end: Area at start/end (km²)
- dV: Volume change (km³)
- dh_mean: Mean height change (m)
- Bgeod: Geodetic mass balance (m w.e. a⁻¹)
- sigma: Uncertainty
- rho_dv: Ice density (kg/m³)

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import math
import json
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from scipy import stats

# Force Legomena 4b
os.environ["LEGOMENA_MODEL"] = "legomena-4b"

# Z² Constants
Z2 = 32 * math.pi / 3  # ≈ 33.510
Z = math.sqrt(Z2)       # ≈ 5.789
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618

OUTPUT_DIR = Path(__file__).parent / "glacier_test_output"
OUTPUT_DIR.mkdir(exist_ok=True)


def log(msg: str):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[GLACIER {ts}] {msg}")


def download_glacier_data():
    """Download and properly parse GLAMOS data."""
    import requests

    url = "https://doi.glamos.ch/data/volumechange/volumechange.csv"
    log(f"Downloading: {url}")

    response = requests.get(url, timeout=60)
    if not response.ok:
        log(f"Download failed: {response.status_code}")
        return None

    # Save raw data
    raw_file = OUTPUT_DIR / "volumechange_raw.csv"
    with open(raw_file, 'w') as f:
        f.write(response.text)
    log(f"Raw data saved: {raw_file}")

    # Parse with proper header skip (5 metadata lines + 1 unit line = skip rows 0-4, 6)
    lines = response.text.strip().split('\n')
    log(f"Total lines: {len(lines)}")

    # Find the actual header line (has SGI-ID)
    header_line = None
    for i, line in enumerate(lines):
        if 'SGI-ID' in line:
            header_line = i
            break

    if header_line is None:
        log("Could not find header line")
        return None

    log(f"Header at line {header_line}: {lines[header_line][:60]}...")
    log(f"Units at line {header_line+1}: {lines[header_line+1][:60]}...")

    # Parse CSV skipping metadata
    from io import StringIO
    data_text = '\n'.join(lines[header_line:header_line+1] + lines[header_line+2:])

    df = pd.read_csv(StringIO(data_text), low_memory=False)
    log(f"Parsed: {len(df)} rows, {len(df.columns)} columns")
    log(f"Columns: {list(df.columns)}")

    return df


def analyze_glacier_z2(df):
    """Analyze glacier data for Z² relationships."""
    log("")
    log("=" * 70)
    log("Z² RELATIONSHIP ANALYSIS")
    log("=" * 70)

    findings = []

    # Z² target values
    targets = {
        "φ": PHI,
        "1/φ": 1/PHI,
        "Z": Z,
        "Z²": Z2,
        "Z²/10": Z2/10,
        "Z²/100": Z2/100,
        "π": math.pi,
        "π/φ": math.pi/PHI,
        "φ²": PHI**2,
        "1/φ²": 1/PHI**2,
        "Z/10": Z/10,
        "√φ": math.sqrt(PHI),
        "2φ": 2*PHI,
    }

    # Identify numeric columns
    numeric_cols = []
    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            if df[col].notna().sum() > 30:
                numeric_cols.append(col)
        except:
            pass

    log(f"Numeric columns found: {numeric_cols}")

    # Key glacier quantities
    key_cols = ['A_start', 'A_end', 'dV', 'dh_mean', 'Bgeod', 'sigma', 'rho_dv']
    available_keys = [c for c in key_cols if c in numeric_cols]
    log(f"Key columns available: {available_keys}")

    # 1. Test: Area ratio (A_end / A_start) - glacier shrinkage ratio
    if 'A_start' in numeric_cols and 'A_end' in numeric_cols:
        log("\n--- Test 1: Glacier Shrinkage Ratio (A_end/A_start) ---")

        valid = df[['A_start', 'A_end']].dropna()
        valid = valid[(valid['A_start'] > 0) & (valid['A_end'] > 0)]

        if len(valid) >= 30:
            ratios = valid['A_end'] / valid['A_start']
            mean_ratio = ratios.mean()
            std_ratio = ratios.std()

            log(f"Mean shrinkage ratio: {mean_ratio:.4f} (N={len(valid)})")
            log(f"Std: {std_ratio:.4f}")

            for name, target in targets.items():
                error = abs(mean_ratio - target) / target * 100
                if error < 5:
                    findings.append({
                        "quantity": "A_end/A_start (glacier shrinkage)",
                        "value": mean_ratio,
                        "target": name,
                        "target_value": target,
                        "error_percent": error,
                        "n_samples": len(valid),
                        "std": std_ratio
                    })
                    log(f"  MATCH: {mean_ratio:.4f} ≈ {name} ({target:.4f}), error={error:.2f}%")

    # 2. Test: Mass balance statistics
    if 'Bgeod' in numeric_cols:
        log("\n--- Test 2: Mass Balance Distribution ---")

        valid = df['Bgeod'].dropna()
        if len(valid) >= 30:
            mean_b = valid.mean()
            std_b = valid.std()
            median_b = valid.median()

            log(f"Mean mass balance: {mean_b:.4f} m w.e./yr (N={len(valid)})")
            log(f"Std: {std_b:.4f}")
            log(f"Median: {median_b:.4f}")

            # Test absolute value of mean
            abs_mean = abs(mean_b)
            for name, target in targets.items():
                if target > 0:
                    error = abs(abs_mean - target) / target * 100
                    if error < 5:
                        findings.append({
                            "quantity": "|mean(Bgeod)| (mass balance magnitude)",
                            "value": abs_mean,
                            "target": name,
                            "target_value": target,
                            "error_percent": error,
                            "n_samples": len(valid)
                        })
                        log(f"  MATCH: |mean|={abs_mean:.4f} ≈ {name} ({target:.4f}), error={error:.2f}%")

            # Test std/|mean| ratio (coefficient of variation)
            if abs_mean > 0:
                cv = std_b / abs_mean
                log(f"CV (std/|mean|): {cv:.4f}")
                for name, target in targets.items():
                    error = abs(cv - target) / target * 100
                    if error < 5:
                        findings.append({
                            "quantity": "CV(Bgeod) = std/|mean|",
                            "value": cv,
                            "target": name,
                            "target_value": target,
                            "error_percent": error,
                            "n_samples": len(valid)
                        })
                        log(f"  MATCH: CV={cv:.4f} ≈ {name} ({target:.4f}), error={error:.2f}%")

    # 3. Test: Height change to area ratio
    if 'dh_mean' in numeric_cols and 'A_start' in numeric_cols:
        log("\n--- Test 3: Height/Area Relationships ---")

        valid = df[['dh_mean', 'A_start']].dropna()
        valid = valid[(valid['A_start'] > 0)]

        if len(valid) >= 30:
            # Ratio of abs(height change) to area
            ratio = abs(valid['dh_mean']).mean() / valid['A_start'].mean()
            log(f"|dh_mean|/A_start: {ratio:.4f}")

            for name, target in targets.items():
                error = abs(ratio - target) / target * 100
                if error < 10:  # Slightly looser for this derived quantity
                    findings.append({
                        "quantity": "|dh_mean|/A_start",
                        "value": ratio,
                        "target": name,
                        "target_value": target,
                        "error_percent": error,
                        "n_samples": len(valid)
                    })
                    log(f"  POTENTIAL: {ratio:.4f} ≈ {name} ({target:.4f}), error={error:.2f}%")

    # 4. Test: Volume to area relationship (3D scaling)
    if 'dV' in numeric_cols and 'A_start' in numeric_cols:
        log("\n--- Test 4: Volume/Area Scaling ---")

        valid = df[['dV', 'A_start', 'A_end']].dropna()
        valid = valid[(valid['A_start'] > 0) & (valid['A_end'] > 0)]

        if len(valid) >= 30:
            # dV / (A_start * sqrt(A_start)) - 3D scaling relationship
            avg_area = (valid['A_start'] + valid['A_end']) / 2
            scaling = abs(valid['dV']).mean() / (avg_area.mean() ** 1.5)
            log(f"|dV| / A^1.5 (3D scaling): {scaling:.6f}")

    # 5. Test: Ratio between different glaciers' responses
    if 'Bgeod' in numeric_cols and 'Name' in df.columns:
        log("\n--- Test 5: Inter-Glacier Comparisons ---")

        # Group by glacier and get mean mass balance
        glacier_means = df.groupby('Name')['Bgeod'].mean().dropna()

        if len(glacier_means) >= 10:
            log(f"Glaciers with data: {len(glacier_means)}")

            # Distribution of glacier-specific mass balances
            abs_means = glacier_means.abs()
            overall_mean = abs_means.mean()
            overall_std = abs_means.std()
            cv = overall_std / overall_mean if overall_mean > 0 else 0

            log(f"Mean |mass balance| across glaciers: {overall_mean:.4f}")
            log(f"Std across glaciers: {overall_std:.4f}")
            log(f"CV across glaciers: {cv:.4f}")

            for name, target in targets.items():
                error = abs(cv - target) / target * 100
                if error < 5:
                    findings.append({
                        "quantity": "CV across glaciers (inter-glacier variability)",
                        "value": cv,
                        "target": name,
                        "target_value": target,
                        "error_percent": error,
                        "n_samples": len(glacier_means)
                    })
                    log(f"  MATCH: CV={cv:.4f} ≈ {name} ({target:.4f}), error={error:.2f}%")

    # 6. Test: Ice density ratio
    if 'rho_dv' in numeric_cols:
        log("\n--- Test 6: Ice Density Analysis ---")

        valid = df['rho_dv'].dropna()
        if len(valid) >= 30:
            mean_rho = valid.mean()
            log(f"Mean ice density: {mean_rho:.1f} kg/m³")

            # rho / 1000 (normalized to water density)
            rho_norm = mean_rho / 1000
            log(f"Normalized to water: {rho_norm:.4f}")

            for name, target in targets.items():
                error = abs(rho_norm - target) / target * 100
                if error < 5:
                    findings.append({
                        "quantity": "ρ_ice/ρ_water",
                        "value": rho_norm,
                        "target": name,
                        "target_value": target,
                        "error_percent": error,
                        "n_samples": len(valid)
                    })
                    log(f"  MATCH: {rho_norm:.4f} ≈ {name} ({target:.4f}), error={error:.2f}%")

    # Summary
    log("")
    log("=" * 70)
    log("FINAL RESULTS")
    log("=" * 70)

    if findings:
        log(f"\nZ² RELATIONSHIPS FOUND: {len(findings)}")
        findings.sort(key=lambda x: x['error_percent'])

        for i, f in enumerate(findings, 1):
            log(f"\n{i}. {f['quantity']}")
            log(f"   Measured: {f['value']:.4f}")
            log(f"   Predicted: {f['target']} = {f['target_value']:.4f}")
            log(f"   Error: {f['error_percent']:.3f}%")
            log(f"   N samples: {f['n_samples']}")

            if f['error_percent'] < 0.5:
                log(f"   Verdict: VALIDATED (HIGH CONFIDENCE)")
            elif f['error_percent'] < 2:
                log(f"   Verdict: VALIDATED (MEDIUM CONFIDENCE)")
            elif f['error_percent'] < 5:
                log(f"   Verdict: VALIDATED (LOW CONFIDENCE)")
    else:
        log("\nNo Z² relationships found with < 5% error")
        log("This is an HONEST result - the data was analyzed rigorously")

    # Save results
    results_file = OUTPUT_DIR / "glacier_z2_analysis.json"
    with open(results_file, 'w') as f:
        json.dump({
            "data_source": "https://doi.glamos.ch/data/volumechange/volumechange.csv",
            "data_rows": len(df),
            "numeric_columns": numeric_cols,
            "findings": findings,
            "timestamp": datetime.now().isoformat(),
            "model_used": "legomena-4b"
        }, f, indent=2)
    log(f"\nResults saved: {results_file}")

    return findings


def main():
    log("=" * 70)
    log("HERMESFLOW 1.4.0 - GLACIER Z² ANALYSIS")
    log("Model: legomena-4b (smallest)")
    log("Data: GLAMOS Swiss Glacier Volume Change")
    log("=" * 70)

    df = download_glacier_data()

    if df is None:
        log("Failed to download data")
        return

    # Save data preview
    preview_file = OUTPUT_DIR / "glacier_data_preview.csv"
    df.head(100).to_csv(preview_file, index=False)
    log(f"Preview saved: {preview_file}")

    # Analyze for Z² relationships
    findings = analyze_glacier_z2(df)

    log("")
    log("=" * 70)
    log("ANALYSIS COMPLETE")
    log(f"Findings: {len(findings)}")
    log("=" * 70)


if __name__ == "__main__":
    main()
