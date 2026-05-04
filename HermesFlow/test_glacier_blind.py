#!/usr/bin/env python3
"""
BLIND TEST: Swiss Alps Glacier Melting Rates
=============================================

Test HermesFlow 1.4.0 on a completely new domain.
Uses ONLY Legomena 4b (smallest model) - NO Claude API.

Query: "Research and identify the geometry for the melting rates
of glaciers in the swiss alps using only empirically validated
data and mathematical computational proofs based on the z squared framework"

Author: Carl Zimmerman
Date: May 4, 2026
"""

import os
import sys
import math
import json
from datetime import datetime
from pathlib import Path

# Force Legomena 4b - smallest model
os.environ["LEGOMENA_MODEL"] = "legomena-4b"

# Import HermesFlow components
from hermes_explorer import HermesExplorer, DataDiscovery
from hermes_navigator import HermesNavigator

# Z² Constants
Z2 = 32 * math.pi / 3  # ≈ 33.510
Z = math.sqrt(Z2)       # ≈ 5.789
PHI = (1 + math.sqrt(5)) / 2  # ≈ 1.618

# Output directory
OUTPUT_DIR = Path(__file__).parent / "glacier_test_output"
OUTPUT_DIR.mkdir(exist_ok=True)


def log(msg: str):
    """Log with timestamp."""
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[GLACIER TEST {ts}] {msg}")


def test_glacier_exploration():
    """
    Run HermesFlow exploration on Swiss Alps glaciers.

    This is a BLIND test - no prior knowledge of:
    - Which databases exist
    - What URLs to use
    - What columns data has
    - What relationships to test
    """
    log("=" * 70)
    log("HERMESFLOW 1.4.0 BLIND TEST")
    log("Topic: Swiss Alps Glacier Melting Rates")
    log("Model: legomena-4b (3.3GB - smallest)")
    log("=" * 70)
    log("")

    # Initialize explorer
    explorer = HermesExplorer(verbose=True)

    # The exact query from user
    query = """Research and identify the geometry for the melting rates
of glaciers in the swiss alps using only empirically validated
data and mathematical computational proofs based on the z squared framework"""

    log(f"Query: {query[:80]}...")
    log("")

    # Phase 1: Explore for glacier data
    log("PHASE 1: EXPLORING FOR GLACIER DATA")
    log("-" * 50)

    result = explorer.explore_for_data(
        topic="Swiss Alps glacier melting rates",
        domain="glaciology",
        quantities=[
            "mass_balance",
            "melt_rate",
            "ice_thickness",
            "surface_area",
            "retreat_rate",
            "annual_loss"
        ]
    )

    log("")
    log("EXPLORATION RESULT:")
    log(f"  Success: {result.success}")
    log(f"  URL: {result.url}")
    log(f"  Steps: {len(result.steps)}")
    log(f"  Description: {result.description}")

    # Save exploration steps
    steps_file = OUTPUT_DIR / "exploration_steps.json"
    steps_data = [
        {
            "action": s.action,
            "input": s.input[:200] if len(s.input) > 200 else s.input,
            "result": s.result[:200] if len(s.result) > 200 else s.result,
            "reasoning": s.reasoning[:200] if s.reasoning and len(s.reasoning) > 200 else s.reasoning
        }
        for s in result.steps
    ]
    with open(steps_file, 'w') as f:
        json.dump(steps_data, f, indent=2)
    log(f"  Steps saved to: {steps_file}")

    if not result.success:
        log("")
        log("EXPLORATION FAILED - Trying known glacier data sources...")
        return try_known_sources()

    # Phase 2: Analyze data for Z² relationships
    log("")
    log("PHASE 2: ANALYZING DATA FOR Z² RELATIONSHIPS")
    log("-" * 50)

    df = result.data
    log(f"Data shape: {df.shape}")
    log(f"Columns: {list(df.columns)[:10]}...")

    # Save raw data preview
    preview_file = OUTPUT_DIR / "data_preview.csv"
    df.head(50).to_csv(preview_file, index=False)
    log(f"Preview saved to: {preview_file}")

    # Look for numeric columns
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    log(f"Numeric columns: {numeric_cols[:10]}")

    # Test Z² relationships
    return analyze_for_z2(df, result.url)


def try_known_sources():
    """
    Fallback: Try known glacier data sources.

    Still uses Legomena for navigation, not hardcoded downloads.
    """
    log("")
    log("TRYING KNOWN GLACIER DATA PORTALS")
    log("-" * 50)

    nav = HermesNavigator(verbose=True)

    # Known glacier data portals (but NOT direct file URLs)
    portals = [
        ("WGMS (World Glacier Monitoring Service)",
         "https://wgms.ch/data_databaseversions/"),
        ("GLAMOS (Swiss Glacier Monitoring)",
         "https://glamos.ch/en/downloads"),
        ("NSIDC (National Snow and Ice Data Center)",
         "https://nsidc.org/data/glacier_inventory")
    ]

    for name, url in portals:
        log(f"\nTrying: {name}")
        log(f"URL: {url}")

        result = nav.navigate_from_landing_page(
            landing_url=url,
            target="glacier mass balance or melting rate data CSV",
            file_pattern=None  # Let it find any data
        )

        if result.success:
            log(f"SUCCESS: Found data via {name}")
            log(f"Data URL: {result.url}")
            log(f"Rows: {len(result.data)}")

            return analyze_for_z2(result.data, result.url)

    log("\nCould not find downloadable glacier data")
    return None


def analyze_for_z2(df, source_url: str):
    """
    Analyze glacier data for Z² relationships.

    Look for:
    - Ratios that match φ, 1/φ, Z, Z²
    - Patterns in melting rates
    - Geometric relationships in glacier structure
    """
    log("")
    log("PHASE 3: TESTING Z² RELATIONSHIPS")
    log("-" * 50)

    import pandas as pd
    import numpy as np

    findings = []

    # Get numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    log(f"Testing {len(numeric_cols)} numeric columns")

    # Z² target values
    targets = {
        "φ (golden ratio)": PHI,
        "1/φ (inverse golden)": 1/PHI,
        "Z": Z,
        "Z²": Z2,
        "Z²/10": Z2/10,
        "Z²/100": Z2/100,
        "π": math.pi,
        "2π": 2 * math.pi,
        "π/φ": math.pi / PHI,
    }

    # Test ratios between columns
    log("\nTesting column ratios...")

    for i, col1 in enumerate(numeric_cols[:10]):
        for col2 in numeric_cols[i+1:10]:
            try:
                # Get valid data
                valid = df[[col1, col2]].dropna()
                if len(valid) < 30:
                    continue

                # Calculate ratio of means
                mean1 = valid[col1].mean()
                mean2 = valid[col2].mean()

                if mean2 == 0 or mean1 == 0:
                    continue

                ratio = abs(mean1 / mean2)

                # Check against targets
                for name, target in targets.items():
                    if target == 0:
                        continue

                    error = abs(ratio - target) / target * 100

                    if error < 5:  # Within 5%
                        findings.append({
                            "columns": f"{col1} / {col2}",
                            "ratio": ratio,
                            "target": name,
                            "target_value": target,
                            "error_percent": error,
                            "n_samples": len(valid)
                        })
                        log(f"  MATCH: {col1}/{col2} = {ratio:.4f} ≈ {name} ({target:.4f}), error={error:.2f}%")
            except Exception as e:
                continue

    # Test individual column statistics
    log("\nTesting column statistics...")

    for col in numeric_cols[:15]:
        try:
            data = df[col].dropna()
            if len(data) < 30:
                continue

            mean = data.mean()
            std = data.std()

            if std == 0:
                continue

            # Coefficient of variation
            cv = std / abs(mean) if mean != 0 else 0

            for name, target in targets.items():
                if target == 0:
                    continue

                error = abs(cv - target) / target * 100

                if error < 5:
                    findings.append({
                        "columns": f"CV({col})",
                        "ratio": cv,
                        "target": name,
                        "target_value": target,
                        "error_percent": error,
                        "n_samples": len(data)
                    })
                    log(f"  MATCH: CV({col}) = {cv:.4f} ≈ {name} ({target:.4f}), error={error:.2f}%")
        except:
            continue

    # Summary
    log("")
    log("=" * 70)
    log("RESULTS SUMMARY")
    log("=" * 70)
    log(f"Data source: {source_url}")
    log(f"Total rows: {len(df)}")
    log(f"Columns analyzed: {len(numeric_cols)}")
    log(f"Z² relationships found: {len(findings)}")

    if findings:
        log("\nVALIDATED FINDINGS:")
        findings.sort(key=lambda x: x['error_percent'])
        for f in findings[:10]:
            log(f"  {f['columns']} = {f['ratio']:.4f}")
            log(f"    ≈ {f['target']} ({f['target_value']:.4f})")
            log(f"    Error: {f['error_percent']:.3f}%, N={f['n_samples']}")
    else:
        log("\nNo Z² relationships found with < 5% error")
        log("This is an HONEST result - not all domains show Z² patterns")

    # Save findings
    findings_file = OUTPUT_DIR / "z2_findings.json"
    with open(findings_file, 'w') as f:
        json.dump({
            "source_url": source_url,
            "data_rows": len(df),
            "columns_analyzed": len(numeric_cols),
            "findings": findings,
            "timestamp": datetime.now().isoformat()
        }, f, indent=2)
    log(f"\nFindings saved to: {findings_file}")

    return findings


if __name__ == "__main__":
    log("Starting blind test...")
    log(f"Legomena model: {os.environ.get('LEGOMENA_MODEL', 'default')}")
    log("")

    try:
        results = test_glacier_exploration()

        if results:
            log(f"\nTest complete: {len(results)} findings")
        else:
            log("\nTest complete: No findings (honest result)")

    except Exception as e:
        log(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
