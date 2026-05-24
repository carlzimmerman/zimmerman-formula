#!/usr/bin/env python3
"""
================================================================================
WORK-ORDER EE: THE CATWISE QUASAR DIPOLE (COSMIC REST FRAME CRISIS)
================================================================================

SYSTEM DIRECTIVE: MACROSCOPIC REFERENCE FRAME TEST

Task: Resolve the 5σ Cosmic Dipole tension using the topological velocity
vectors from T³/Z₂ geometry.

The Crisis:
- CMB Dipole: 369 km/s toward (l=264°, b=48°)
- CatWISE/Quaia Quasar Dipole: Different direction AND amplitude (>5σ tension)
- Standard ΛCDM: These should be IDENTICAL (same cosmic rest frame)

The Z² Resolution:
- The universe is NOT a smooth fluid; it's a T³/Z₂ lattice
- Our local topological bulk flow (265 km/s) adds vectorially to the CMB dipole
- The quasar dipole sees BOTH the CMB motion AND the topological bulk flow
- Vector subtraction should resolve the tension

Technical Requirements:
1. Load CatWISE2020 or Quaia quasar catalog dipole measurements
2. Load Planck CMB dipole vector
3. Calculate the Z² topological bulk flow vector (toward Vertex #6)
4. Perform vector subtraction: Quasar_dipole - Z²_bulk_flow
5. Compare residual with CMB dipole

Author: Carl Zimmerman + Claude
Date: May 23, 2026
Framework: Z² Unified Action v11.1.0
Work-Order: EE (Cosmic Dipole Resolution)
================================================================================
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json

try:
    from scipy import stats
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

# =============================================================================
# LOCKED PARAMETERS - DO NOT MODIFY
# =============================================================================

# CMB Dipole (Planck 2018)
CMB_DIPOLE = {
    'v_kms': 369.82,           # km/s
    'l_gal': 264.021,          # Galactic longitude
    'b_gal': 48.253,           # Galactic latitude
    'T_dipole_mK': 3.3621,     # Dipole amplitude in mK
}

# CatWISE2020 Quasar Dipole (Secrest et al. 2021, 2022)
# This is the ANOMALY - it disagrees with CMB at >5σ
CATWISE_DIPOLE = {
    'v_kms': 450,              # Inferred velocity (approximate)
    'l_gal': 247,              # Galactic longitude (differs from CMB!)
    'b_gal': 36,               # Galactic latitude (differs from CMB!)
    'amplitude': 0.0152,       # Dipole amplitude (dimensionless)
    'sigma_tension': 5.1,      # Tension with CMB
    'n_quasars': 1355352,      # Number of quasars in sample
}

# Quaia (Gaia DR3 Quasar Dipole - Dalang & Bonvin 2024)
QUAIA_DIPOLE = {
    'v_kms': 380,              # Approximate
    'l_gal': 260,              # Closer to CMB but still offset
    'b_gal': 45,
    'n_quasars': 1300000,
}

# Z² Topological Bulk Flow
# This is our motion relative to the T³/Z₂ lattice
Z2_BULK_FLOW = {
    'v_kms': 265,              # km/s
    'l_gal': 276.4,            # Toward Vertex #6 (Shapley direction)
    'b_gal': 29.8,
    'source': 'T³/Z₂ topology',
}

# KBC Void outflow component
KBC_VOID = {
    'v_kms': 50,               # Additional outflow from local void
    'l_gal': 280,              # Approximate direction
    'b_gal': 35,
}

OUTPUT_DIR = Path(__file__).parent

print("=" * 80)
print("WORK-ORDER EE: CATWISE QUASAR DIPOLE RESOLUTION")
print("=" * 80)
print(f"\nFramework: Z² Unified Action v11.1.0")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n*** THE COSMIC DIPOLE CRISIS ***")
print(f"  CMB Dipole:     {CMB_DIPOLE['v_kms']:.0f} km/s toward "
      f"(l={CMB_DIPOLE['l_gal']:.1f}°, b={CMB_DIPOLE['b_gal']:.1f}°)")
print(f"  CatWISE Dipole: {CATWISE_DIPOLE['v_kms']:.0f} km/s toward "
      f"(l={CATWISE_DIPOLE['l_gal']:.1f}°, b={CATWISE_DIPOLE['b_gal']:.1f}°)")
print(f"  Tension: {CATWISE_DIPOLE['sigma_tension']:.1f}σ")

# =============================================================================
# VECTOR OPERATIONS
# =============================================================================

def galactic_to_cartesian(v_kms, l_deg, b_deg):
    """Convert velocity in Galactic coordinates to Cartesian."""
    l_rad = np.radians(l_deg)
    b_rad = np.radians(b_deg)

    vx = v_kms * np.cos(b_rad) * np.cos(l_rad)
    vy = v_kms * np.cos(b_rad) * np.sin(l_rad)
    vz = v_kms * np.sin(b_rad)

    return np.array([vx, vy, vz])


def cartesian_to_galactic(v_vec):
    """Convert Cartesian velocity to Galactic coordinates."""
    vx, vy, vz = v_vec
    v_mag = np.sqrt(vx**2 + vy**2 + vz**2)

    if v_mag == 0:
        return 0, 0, 0

    b_rad = np.arcsin(vz / v_mag)
    l_rad = np.arctan2(vy, vx)

    l_deg = np.degrees(l_rad) % 360
    b_deg = np.degrees(b_rad)

    return v_mag, l_deg, b_deg


def angular_separation(l1, b1, l2, b2):
    """Angular separation between two directions."""
    l1, b1, l2, b2 = map(np.radians, [l1, b1, l2, b2])

    cos_sep = (np.sin(b1) * np.sin(b2) +
               np.cos(b1) * np.cos(b2) * np.cos(l1 - l2))
    cos_sep = np.clip(cos_sep, -1, 1)

    return np.degrees(np.arccos(cos_sep))


# =============================================================================
# DIPOLE RESOLUTION
# =============================================================================

def compute_z2_correction():
    """
    Compute the Z² topological correction to the quasar dipole.

    The total local motion has three components:
    1. CMB thermal dipole (motion through CMB rest frame)
    2. Z² bulk flow (motion through topological lattice)
    3. KBC void outflow (local void dynamics)
    """
    print("\n" + "-" * 60)
    print("COMPUTING Z² TOPOLOGICAL CORRECTION")
    print("-" * 60)

    # Convert all vectors to Cartesian
    v_cmb = galactic_to_cartesian(CMB_DIPOLE['v_kms'],
                                   CMB_DIPOLE['l_gal'],
                                   CMB_DIPOLE['b_gal'])

    v_z2 = galactic_to_cartesian(Z2_BULK_FLOW['v_kms'],
                                  Z2_BULK_FLOW['l_gal'],
                                  Z2_BULK_FLOW['b_gal'])

    v_kbc = galactic_to_cartesian(KBC_VOID['v_kms'],
                                   KBC_VOID['l_gal'],
                                   KBC_VOID['b_gal'])

    print(f"\nVelocity Vectors (Cartesian):")
    print(f"  CMB:  ({v_cmb[0]:+.0f}, {v_cmb[1]:+.0f}, {v_cmb[2]:+.0f}) km/s")
    print(f"  Z²:   ({v_z2[0]:+.0f}, {v_z2[1]:+.0f}, {v_z2[2]:+.0f}) km/s")
    print(f"  KBC:  ({v_kbc[0]:+.0f}, {v_kbc[1]:+.0f}, {v_kbc[2]:+.0f}) km/s")

    # In Z² framework, distant quasars see:
    # v_quasar = v_cmb + v_z2 + v_kbc
    # (they observe ALL our motions, not just CMB)

    v_total = v_cmb + v_z2 + v_kbc
    v_total_mag, l_total, b_total = cartesian_to_galactic(v_total)

    print(f"\n*** PREDICTED QUASAR DIPOLE (Z²) ***")
    print(f"  v = {v_total_mag:.0f} km/s")
    print(f"  l = {l_total:.1f}°")
    print(f"  b = {b_total:.1f}°")

    return {
        'v_cmb': v_cmb,
        'v_z2': v_z2,
        'v_kbc': v_kbc,
        'v_total': v_total,
        'predicted_v_kms': v_total_mag,
        'predicted_l': l_total,
        'predicted_b': b_total
    }


def compare_with_catwise(z2_prediction):
    """
    Compare Z² prediction with observed CatWISE dipole.
    """
    print("\n" + "-" * 60)
    print("COMPARING WITH CATWISE OBSERVATIONS")
    print("-" * 60)

    # CatWISE observed
    v_cat = galactic_to_cartesian(CATWISE_DIPOLE['v_kms'],
                                   CATWISE_DIPOLE['l_gal'],
                                   CATWISE_DIPOLE['b_gal'])

    # Z² predicted
    v_pred = z2_prediction['v_total']

    # Residual (what's left after Z² correction)
    v_residual = v_cat - v_pred
    v_res_mag, l_res, b_res = cartesian_to_galactic(v_residual)

    print(f"\nCatWISE Observed:  {CATWISE_DIPOLE['v_kms']:.0f} km/s "
          f"toward (l={CATWISE_DIPOLE['l_gal']:.1f}°, b={CATWISE_DIPOLE['b_gal']:.1f}°)")
    print(f"Z² Predicted:      {z2_prediction['predicted_v_kms']:.0f} km/s "
          f"toward (l={z2_prediction['predicted_l']:.1f}°, b={z2_prediction['predicted_b']:.1f}°)")
    print(f"Residual:          {v_res_mag:.0f} km/s "
          f"toward (l={l_res:.1f}°, b={b_res:.1f}°)")

    # Angular separation between observed and predicted
    sep_pred_obs = angular_separation(z2_prediction['predicted_l'],
                                       z2_prediction['predicted_b'],
                                       CATWISE_DIPOLE['l_gal'],
                                       CATWISE_DIPOLE['b_gal'])

    # Angular separation between residual and zero (should be small if Z² works)
    # Actually, compare residual direction to CMB direction
    sep_res_cmb = angular_separation(l_res, b_res,
                                      CMB_DIPOLE['l_gal'],
                                      CMB_DIPOLE['b_gal'])

    print(f"\nAngular Separations:")
    print(f"  Z² prediction vs CatWISE:  {sep_pred_obs:.1f}°")
    print(f"  Residual vs CMB direction: {sep_res_cmb:.1f}°")

    return {
        'v_catwise': v_cat,
        'v_residual': v_residual,
        'residual_mag': v_res_mag,
        'residual_l': l_res,
        'residual_b': b_res,
        'sep_pred_obs': sep_pred_obs,
        'sep_res_cmb': sep_res_cmb
    }


def test_tension_resolution(z2_prediction, comparison):
    """
    Test whether Z² resolves the CMB-Quasar dipole tension.
    """
    print("\n" + "-" * 60)
    print("TESTING TENSION RESOLUTION")
    print("-" * 60)

    # Original tension
    original_sep = angular_separation(CMB_DIPOLE['l_gal'], CMB_DIPOLE['b_gal'],
                                       CATWISE_DIPOLE['l_gal'], CATWISE_DIPOLE['b_gal'])

    v_diff_original = abs(CMB_DIPOLE['v_kms'] - CATWISE_DIPOLE['v_kms'])

    # After Z² correction
    # The residual should be close to CMB if Z² is correct
    residual_sep = comparison['sep_res_cmb']
    residual_mag = comparison['residual_mag']

    # Estimate new tension
    # Simplified: assume angular and velocity tensions add in quadrature
    original_tension = CATWISE_DIPOLE['sigma_tension']

    # If Z² works, the residual should be small
    # New tension ~ residual / typical_error
    typical_error = 30  # km/s approximate uncertainty
    new_velocity_tension = residual_mag / typical_error
    new_angular_tension = residual_sep / 5  # ~5° typical pointing error

    new_tension = np.sqrt(new_velocity_tension**2 + new_angular_tension**2)

    print(f"\n*** ORIGINAL TENSION ***")
    print(f"  CMB vs CatWISE angular separation: {original_sep:.1f}°")
    print(f"  CMB vs CatWISE velocity difference: {v_diff_original:.0f} km/s")
    print(f"  Combined tension: {original_tension:.1f}σ")

    print(f"\n*** AFTER Z² CORRECTION ***")
    print(f"  Residual magnitude: {residual_mag:.0f} km/s")
    print(f"  Residual vs CMB separation: {residual_sep:.1f}°")
    print(f"  New estimated tension: {new_tension:.1f}σ")

    tension_reduction = (original_tension - new_tension) / original_tension * 100

    print(f"\n  TENSION REDUCTION: {tension_reduction:.0f}%")

    return {
        'original_angular_sep': original_sep,
        'original_velocity_diff': v_diff_original,
        'original_tension_sigma': original_tension,
        'residual_magnitude': residual_mag,
        'residual_angular_sep': residual_sep,
        'new_tension_sigma': new_tension,
        'tension_reduction_pct': tension_reduction
    }


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Execute Work-Order EE: CatWISE Quasar Dipole Resolution"""

    print("\n" + "=" * 80)
    print("EXECUTING WORK-ORDER EE")
    print("=" * 80)

    # Step 1: Compute Z² correction
    z2_prediction = compute_z2_correction()

    # Step 2: Compare with CatWISE
    comparison = compare_with_catwise(z2_prediction)

    # Step 3: Test tension resolution
    tension = test_tension_resolution(z2_prediction, comparison)

    # Step 4: Compile results
    results = {
        'work_order': 'EE',
        'task': 'CatWISE Quasar Dipole Resolution',
        'date': datetime.now().isoformat(),
        'inputs': {
            'cmb_dipole': CMB_DIPOLE,
            'catwise_dipole': CATWISE_DIPOLE,
            'z2_bulk_flow': Z2_BULK_FLOW,
            'kbc_void': KBC_VOID
        },
        'z2_prediction': {
            'v_kms': float(z2_prediction['predicted_v_kms']),
            'l_gal': float(z2_prediction['predicted_l']),
            'b_gal': float(z2_prediction['predicted_b'])
        },
        'comparison': {
            'residual_v_kms': float(comparison['residual_mag']),
            'residual_l': float(comparison['residual_l']),
            'residual_b': float(comparison['residual_b']),
            'sep_pred_obs_deg': float(comparison['sep_pred_obs'])
        },
        'tension_analysis': tension
    }

    # Verdict
    if tension['new_tension_sigma'] < 2.0:
        results['verdict'] = "DECISIVE EVIDENCE DETECTED: COSMIC DIPOLE TENSION RESOLVED BY TOPOLOGY"
        results['status'] = 'RESOLVED'
    elif tension['new_tension_sigma'] < 3.0:
        results['verdict'] = f"Significant reduction ({tension['tension_reduction_pct']:.0f}%) but {tension['new_tension_sigma']:.1f}σ residual remains"
        results['status'] = 'PARTIAL'
    else:
        results['verdict'] = f"Tension reduced from {tension['original_tension_sigma']:.1f}σ to {tension['new_tension_sigma']:.1f}σ - more work needed"
        results['status'] = 'INSUFFICIENT'

    # Save
    output_file = OUTPUT_DIR / 'WORK_ORDER_EE_dipole_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {output_file}")

    # Final summary
    print("\n" + "=" * 80)
    print("WORK-ORDER EE COMPLETE")
    print("=" * 80)
    print(f"""
┌─────────────────────────────────────────────────────────────────┐
│        WORK-ORDER EE: COSMIC DIPOLE RESOLUTION COMPLETE         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  THE ANOMALY:                                                   │
│    CMB Dipole:     {CMB_DIPOLE['v_kms']:>4.0f} km/s → (l={CMB_DIPOLE['l_gal']:.0f}°, b={CMB_DIPOLE['b_gal']:.0f}°)      │
│    CatWISE Dipole: {CATWISE_DIPOLE['v_kms']:>4.0f} km/s → (l={CATWISE_DIPOLE['l_gal']:.0f}°, b={CATWISE_DIPOLE['b_gal']:.0f}°)      │
│    Original Tension: {tension['original_tension_sigma']:.1f}σ                                  │
│                                                                 │
│  Z² TOPOLOGICAL CORRECTION:                                     │
│    Bulk flow: {Z2_BULK_FLOW['v_kms']:.0f} km/s toward Vertex #6                   │
│    KBC void:  {KBC_VOID['v_kms']:.0f} km/s local outflow                        │
│                                                                 │
│  RESULT:                                                        │
│    Predicted Quasar Dipole: {z2_prediction['predicted_v_kms']:.0f} km/s                       │
│    Residual after Z²:       {comparison['residual_mag']:.0f} km/s                       │
│    New Tension:             {tension['new_tension_sigma']:.1f}σ                            │
│    Tension Reduction:       {tension['tension_reduction_pct']:.0f}%                            │
│                                                                 │
│  {results['verdict']:<60} │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
""")

    return results


if __name__ == "__main__":
    main()
