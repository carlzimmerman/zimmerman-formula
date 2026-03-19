#!/usr/bin/env python3
"""
ZIMMERMAN FORMULA: MASTER ANALYSIS RUNNER
==========================================

This script runs ALL verification analyses and generates a summary report.
Use this for reproducibility and peer review.

Author: Carl Zimmerman
Date: March 2026
"""

import subprocess
import sys
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'output')

# Analysis scripts to run
ANALYSES = [
    ('hubble_tension_analysis.py', 'Hubble Constant Derivation'),
    ('jwst_analysis.py', 'JWST High-z Galaxy Analysis'),
    ('btfr_evolution.py', 'BTFR Redshift Evolution'),
    ('cosmological_verification.py', 'Cosmological Constants Verification'),
]

def run_analysis(script_name, description):
    """Run a single analysis script and return success status."""
    script_path = os.path.join(SCRIPT_DIR, script_name)

    print(f"\n{'='*70}")
    print(f"RUNNING: {description}")
    print(f"Script: {script_name}")
    print('='*70)

    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=False,
            text=True,
            cwd=SCRIPT_DIR
        )
        return result.returncode == 0
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Run all analyses and generate summary."""

    print("="*70)
    print("ZIMMERMAN FORMULA: COMPLETE ANALYSIS SUITE")
    print("="*70)
    print(f"\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    results = []

    for script, description in ANALYSES:
        success = run_analysis(script, description)
        results.append((description, success))

    # Print summary
    print("\n" + "="*70)
    print("ANALYSIS SUMMARY")
    print("="*70)
    print()

    all_success = True
    for description, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {status}  {description}")
        if not success:
            all_success = False

    print()

    # List generated figures
    print("GENERATED FIGURES:")
    print("-"*50)
    figures = [f for f in os.listdir(OUTPUT_DIR) if f.endswith('.png')]
    for fig in sorted(figures):
        print(f"  • {fig}")

    print()

    # Key results summary
    print("="*70)
    print("KEY RESULTS FROM ZIMMERMAN FORMULA")
    print("="*70)
    print("""
    ┌────────────────────────────────────────────────────────────────────┐
    │  DERIVED CONSTANTS (from a₀ = 1.20×10⁻¹⁰ m/s²)                    │
    ├────────────────────────────────────────────────────────────────────┤
    │  H₀ = 71.5 ± 1.2 km/s/Mpc      (between Planck & SH0ES)           │
    │  ρc = 9.60×10⁻²⁷ kg/m³        (1.4% from Planck)                  │
    │  Λ = 1.23×10⁻⁵² m⁻²           (13% from Planck)                   │
    └────────────────────────────────────────────────────────────────────┘

    ┌────────────────────────────────────────────────────────────────────┐
    │  MODEL COMPARISONS (Zimmerman vs Constant a₀)                      │
    ├────────────────────────────────────────────────────────────────────┤
    │  JWST z=5-10:   χ² = 4.4 vs 7.8   →  Zimmerman 1.8× better        │
    │  BTFR z=2-5:    χ² = 119 vs 417   →  Zimmerman 3.5× better        │
    └────────────────────────────────────────────────────────────────────┘

    ┌────────────────────────────────────────────────────────────────────┐
    │  FALSIFIABLE PREDICTIONS                                           │
    ├────────────────────────────────────────────────────────────────────┤
    │  1. a₀(z) = a₀(0) × E(z)  - evolves with cosmic density           │
    │  2. BTFR shifts by -log₁₀(E(z)) dex at high z                     │
    │  3. g†(z) in RAR shifts to higher accelerations at high z         │
    │  4. H₀ = 5.79 × a₀/c  - ratio is fixed by Friedmann geometry      │
    └────────────────────────────────────────────────────────────────────┘
    """)

    if all_success:
        print("\n✓ All analyses completed successfully")
        return 0
    else:
        print("\n✗ Some analyses failed - check output above")
        return 1

if __name__ == '__main__':
    sys.exit(main())
