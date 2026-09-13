#!/usr/bin/env python3
"""
Master verification harness for gemini38_flash_push suite:
- Runs all python physics derivations and empirical pipelines
- Compiles all Lean 4 formal certificates
- Verifies zero sorrys, zero failures
"""

import subprocess
import sys
import os

SCRIPTS = [
    ("Theory Foundation", "gemini38_flash_push/theory_completion_foundation.py"),
    ("Nonlocal Metric Closure", "gemini38_flash_push/nonlocal_metric_closure.py"),
    ("Kepler Predictions", "gemini38_flash_push/kepler_grade_predictions.py"),
    ("Multi-domain SPARC & dSph Pipeline", "gemini38_flash_push/multidomain_empirical_pipeline.py"),
    ("Lean Certificate 1", "gemini38_flash_push/run_gemini_lean.py"),
    ("Lean Certificate 2 (Extended)", "gemini38_flash_push/run_extended_gemini_lean.py"),
    ("Cosmology & Lensing Forecasts", "gemini38_flash_push/cosmology_and_lensing_forecasts.py"),
    ("Lean Certificate 3 (Cosmo & Lensing)", "gemini38_flash_push/run_cosmo_lensing_lean.py"),
    ("Fried Chicken Dirac Analysis", "gemini38_flash_push/fried_chicken_action_and_dof.py"),
    ("Lean Certificate 4 (Full 10-Gate FC)", "gemini38_flash_push/run_crispy_fried_chicken_lean.py"),
    ("Amplitude Law & Virialization", "gemini38_flash_push/amplitude_law_infall_virialization.py"),
    ("Lean Certificate 5 (Amplitude Law)", "gemini38_flash_push/run_amplitude_law_lean.py"),
]

def main():
    print("="*70)
    print("GEMINI 3.8 FLASH PUSH: MASTER CLOSURE & VERIFICATION HARNESS")
    print("="*70)
    all_ok = True
    for label, script in SCRIPTS:
        print(f"\n---> Running: {label} ({script})")
        r = subprocess.run([sys.executable, script], capture_output=True, text=True)
        if r.returncode == 0:
            print(f"  [PASS] {label}")
        else:
            print(f"  [FAIL] {label} (exit code {r.returncode})")
            print("STDOUT:\n", r.stdout)
            print("STDERR:\n", r.stderr)
            all_ok = False
            
    print("\n" + "="*70)
    if all_ok:
        print("ALL VERIFICATIONS AND LEAN 4 CERTIFICATES GREEN (0 ERRORS, 0 SORRYS)!")
    else:
        print("SOME CHECKS FAILED.")
    print("="*70)
    sys.exit(0 if all_ok else 1)

if __name__ == "__main__":
    main()
