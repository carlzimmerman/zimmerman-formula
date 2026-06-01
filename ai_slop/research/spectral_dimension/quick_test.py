#!/usr/bin/env python3
"""
Quick test of spectral dimension calculation.
Runs on small lattice (L=8) for fast verification.
"""

import numpy as np
import sys

# Add parent directory to path
sys.path.insert(0, '.')

from heat_kernel_calculation import (
    run_spectral_dimension_analysis,
    Z_SQUARED, Z, ALPHA_Z2
)

def main():
    print("="*60)
    print("QUICK TEST: Spectral Dimension on Z² Lattice")
    print("="*60)
    print(f"Z² = {Z_SQUARED:.4f}")
    print(f"α = 1/Z² = {ALPHA_Z2:.6f}")
    print("="*60)

    # Test 1: Standard lattice (should give d_s ≈ 3 everywhere)
    print("\n[Test 1] Standard Laplacian (no Harper)")
    result_std = run_spectral_dimension_analysis(
        L=8,
        alpha=0,
        use_harper=False,
        verbose=True
    )

    # Test 2: Harper-modified with Z² coupling
    print("\n[Test 2] Harper Laplacian (α = 1/Z²)")
    result_harper = run_spectral_dimension_analysis(
        L=8,
        alpha=ALPHA_Z2,
        use_harper=True,
        verbose=True
    )

    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"{'Lattice Type':<20} {'d_s(UV)':<12} {'d_s(IR)':<12}")
    print("-"*60)
    print(f"{'Standard':<20} {result_std.d_s_UV:<12.3f} {result_std.d_s_IR:<12.3f}")
    print(f"{'Harper (Z²)':<20} {result_harper.d_s_UV:<12.3f} {result_harper.d_s_IR:<12.3f}")
    print("-"*60)
    print(f"{'Theory':<20} {'2.0':<12} {'3.0':<12}")
    print("="*60)

    # Assessment
    print("\nASSESSMENT:")
    uv_error_std = abs(result_std.d_s_UV - 2.0)
    uv_error_harper = abs(result_harper.d_s_UV - 2.0)

    if uv_error_harper < uv_error_std:
        print(f"  Harper modification IMPROVES UV limit")
        print(f"  Standard UV error:  {uv_error_std:.3f}")
        print(f"  Harper UV error:    {uv_error_harper:.3f}")
    else:
        print(f"  Harper modification does NOT improve UV limit")

    ir_error_std = abs(result_std.d_s_IR - 3.0)
    ir_error_harper = abs(result_harper.d_s_IR - 3.0)
    print(f"\n  IR errors: Standard={ir_error_std:.3f}, Harper={ir_error_harper:.3f}")

    # Check if we achieve d_s → 2 in UV
    if result_harper.d_s_UV < 2.5:
        print(f"\n  UV dimension ({result_harper.d_s_UV:.2f}) shows reduction toward 2")
    else:
        print(f"\n  WARNING: UV dimension ({result_harper.d_s_UV:.2f}) does not show expected reduction")

    return result_std, result_harper


if __name__ == "__main__":
    result_std, result_harper = main()
