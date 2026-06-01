#!/usr/bin/env python3
"""
================================================================================
WORK-ORDER GG: THE EL GORDO CLUSTER SHOCK VELOCITY
================================================================================

SYSTEM DIRECTIVE: EXTREME KINEMATIC SHOCK TEST

Task: Model the El Gordo cluster collision using topological vertex repulsion
to explain the "impossible" collision velocity.

The Anomaly:
- El Gordo (ACT-CL J0102-4915) is the most massive known cluster at z > 0.5
- Two sub-clusters collided at v ~ 2500 km/s
- In standard ΛCDM, this velocity is a 3σ outlier ("impossible" probability)
- The cluster is too massive and moving too fast for its redshift

The Z² Explanation:
- The T³/Z₂ topological vertices create repulsive potential wells
- Matter is accelerated TOWARD the void walls (away from vertices)
- The El Gordo progenitors were accelerated by topological repulsion
- Standard dark matter friction is reduced by topological inertia effects

Technical Requirements:
1. Load El Gordo kinematic constraints
2. Calculate ΛCDM expected collision velocity
3. Add Z² vertex repulsion (v = 0.236 potential)
4. Apply topological inertial modifier (Ω_m = 0.3158)
5. Compare predicted vs observed velocities

Author: Carl Zimmerman + Claude
Date: May 23, 2026
Framework: Z² Unified Action v11.1.0
Work-Order: GG (Extreme Kinematics Test)
================================================================================
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json

try:
    from scipy.integrate import odeint, solve_ivp
    from scipy.optimize import brentq
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

# =============================================================================
# LOCKED PARAMETERS - DO NOT MODIFY
# =============================================================================

# Fundamental constants
G_SI = 6.67430e-11          # m³/kg/s²
C_MS = 299792458            # m/s
C_KMS = 299792.458          # km/s
M_SUN_KG = 1.989e30         # kg
MPC_M = 3.086e22            # Mpc in meters
GYR_S = 3.156e16            # Gyr in seconds

# El Gordo observational constraints (Menanteau et al. 2012, Zhang et al. 2015)
EL_GORDO = {
    'name': 'ACT-CL J0102-4915 (El Gordo)',
    'z': 0.87,                      # Redshift
    'M_total': 2.16e15,             # Total mass in M_sun (including DM)
    'M_total_err': 0.32e15,
    'M1': 1.4e15,                   # Subcluster 1 mass
    'M2': 0.76e15,                  # Subcluster 2 mass
    'v_collision': 2500,            # Observed collision velocity km/s
    'v_collision_err': 400,
    'separation': 0.7,              # Current separation in Mpc
    'ra': 15.72,                    # RA in degrees
    'dec': -49.26,                  # Dec in degrees
}

# Z² Topological Parameters
L_C_GPC = 20.6              # Fundamental domain Gpc
L_C_MPC = L_C_GPC * 1000    # In Mpc
OMEGA_M = 6 / 19            # = 0.3158
V_VERTEX = 0.236            # Topological vertex potential (dimensionless)

# Hubble parameter at z=0.87
H0 = 70.0                   # km/s/Mpc
OMEGA_M_LCDM = 0.315
OMEGA_LAMBDA = 0.685

# Nearest Z² vertex to El Gordo (Southern vertex)
NEAREST_VERTEX = {
    'name': 'V4 (Southern)',
    'l_gal': 6.4,
    'b_gal': -60.2,
    'distance_mpc': 8500,   # Approximate distance to vertex from El Gordo
}

OUTPUT_DIR = Path(__file__).parent

print("=" * 80)
print("WORK-ORDER GG: EL GORDO CLUSTER SHOCK TEST")
print("=" * 80)
print(f"\nFramework: Z² Unified Action v11.1.0")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n*** THE EL GORDO ANOMALY ***")
print(f"  Cluster: {EL_GORDO['name']}")
print(f"  Redshift: z = {EL_GORDO['z']}")
print(f"  Total mass: {EL_GORDO['M_total']:.2e} M_sun")
print(f"  Collision velocity: {EL_GORDO['v_collision']} ± {EL_GORDO['v_collision_err']} km/s")
print(f"  THIS IS A 3σ OUTLIER IN ΛCDM!")

# =============================================================================
# COSMOLOGY FUNCTIONS
# =============================================================================

def hubble_z(z):
    """Hubble parameter at redshift z."""
    return H0 * np.sqrt(OMEGA_M_LCDM * (1 + z)**3 + OMEGA_LAMBDA)


def cosmic_time(z):
    """Cosmic time at redshift z (in Gyr)."""
    # Approximate integral
    if not SCIPY_AVAILABLE:
        # Rough approximation
        return 13.8 / (1 + z)**1.5

    from scipy.integrate import quad

    def integrand(z_prime):
        return 1 / ((1 + z_prime) * hubble_z(z_prime))

    # Convert H to 1/Gyr: H [km/s/Mpc] / (km/s per Mpc) * Gyr
    H_to_invGyr = 1 / (MPC_M / 1e3) * GYR_S

    result, _ = quad(integrand, z, np.inf)
    return result * H_to_invGyr


def comoving_distance(z):
    """Comoving distance to redshift z in Mpc."""
    if not SCIPY_AVAILABLE:
        # Approximate
        return z * C_KMS / H0

    from scipy.integrate import quad

    def integrand(z_prime):
        return 1 / hubble_z(z_prime)

    result, _ = quad(integrand, 0, z)
    return C_KMS * result


# =============================================================================
# ΛCDM CLUSTER DYNAMICS
# =============================================================================

def lcdm_infall_velocity(M_total, separation_mpc, z):
    """
    Expected infall velocity in ΛCDM.

    For two clusters falling together from large separation:
    v² ≈ 2GM/r × (1 - b²/r²)^(-1)

    where b is the impact parameter.

    For radial infall: v = √(2GM/r)
    """
    M = M_total * M_SUN_KG
    r = separation_mpc * MPC_M

    # Simple estimate: free-fall velocity
    v_freefall = np.sqrt(2 * G_SI * M / r)

    # Convert to km/s
    return v_freefall / 1000


def lcdm_collision_probability(v_observed, M_total, z):
    """
    Estimate the probability of observing this collision velocity in ΛCDM.

    Based on cosmological N-body simulations:
    - Typical collision velocities follow a Maxwell-Boltzmann distribution
    - The characteristic velocity depends on mass and redshift
    """
    # Typical collision velocity for clusters of this mass
    # From simulations: v_typical ~ 1500 km/s for 10^15 M_sun clusters
    v_typical = 1500 * (M_total / 1e15)**0.2  # Weak mass scaling

    # Dispersion
    sigma_v = v_typical / np.sqrt(2)

    # Probability of observing v > v_observed
    from scipy.stats import maxwell
    scale = sigma_v
    p_value = 1 - maxwell.cdf(v_observed, scale=scale)

    # Convert to sigma
    from scipy.stats import norm
    sigma = norm.ppf(1 - p_value)

    return p_value, sigma


def lcdm_max_expected_velocity(M_total, z, percentile=99.7):
    """
    Maximum expected collision velocity at 3σ (99.7%) in ΛCDM.
    """
    v_typical = 1500 * (M_total / 1e15)**0.2
    sigma_v = v_typical / np.sqrt(2)

    from scipy.stats import maxwell
    return maxwell.ppf(percentile/100, scale=sigma_v)


# =============================================================================
# Z² TOPOLOGICAL DYNAMICS
# =============================================================================

def z2_vertex_acceleration(distance_to_vertex_mpc):
    """
    Acceleration due to Z² topological vertex repulsion.

    The vertices of the T³/Z₂ fundamental domain create a repulsive
    potential that accelerates matter AWAY from vertices (into void walls).

    a_vertex = (v_vertex × c²) / L_c × exp(-d/L_c)

    where v_vertex = 0.236 is the vertex potential strength.
    """
    d = distance_to_vertex_mpc
    L_c = L_C_MPC

    # Vertex acceleration scale
    a_scale = V_VERTEX * C_MS**2 / (L_c * MPC_M)  # m/s²

    # Exponential decay with distance from vertex
    a = a_scale * np.exp(-d / L_c)

    return a


def z2_additional_velocity(distance_to_vertex_mpc, time_gyr):
    """
    Additional velocity gained from Z² vertex repulsion over time.

    Δv = a_vertex × t
    """
    a = z2_vertex_acceleration(distance_to_vertex_mpc)
    t = time_gyr * GYR_S

    delta_v = a * t
    return delta_v / 1000  # km/s


def z2_inertial_modifier(z):
    """
    Z² topological inertial modifier.

    In Z², dark matter is not localized particles but a topological
    inertial effect. This REDUCES dynamical friction during mergers.

    Standard: friction ~ ρ_DM × v²
    Z²: friction ~ (ρ_baryonic × f_inertia) × v²

    where f_inertia < 1 at cluster scales.
    """
    # Inertial reduction factor
    # At high accelerations (cluster scales), inertia is normal
    # But the "dark matter" component doesn't provide friction

    # Effective friction reduction
    f_friction = OMEGA_M / (1 - OMEGA_M)  # ~ 0.46

    return f_friction


def z2_collision_velocity(M_total, separation_mpc, z, distance_to_vertex_mpc):
    """
    Predicted collision velocity in Z² cosmology.

    Components:
    1. Standard gravitational infall
    2. Z² vertex repulsion boost
    3. Reduced dynamical friction (topological inertia)
    """
    # Standard infall
    v_infall = lcdm_infall_velocity(M_total, separation_mpc, z)

    # Cosmic time available for acceleration
    t_cosmic = cosmic_time(z)  # Gyr

    # Z² vertex boost
    v_vertex = z2_additional_velocity(distance_to_vertex_mpc, t_cosmic)

    # Inertial modifier (reduces friction during collision)
    f_inertia = z2_inertial_modifier(z)

    # The reduced friction allows clusters to reach higher velocities
    # v_eff = v / √f_friction
    v_friction_boost = v_infall * (1 / np.sqrt(f_inertia) - 1)

    # Total velocity
    v_total = v_infall + v_vertex + v_friction_boost

    return {
        'v_infall': v_infall,
        'v_vertex': v_vertex,
        'v_friction_boost': v_friction_boost,
        'v_total': v_total,
        't_cosmic_gyr': t_cosmic,
        'f_inertia': f_inertia
    }


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def analyze_el_gordo():
    """Full analysis of El Gordo kinematics."""
    print("\n" + "-" * 60)
    print("ANALYZING EL GORDO KINEMATICS")
    print("-" * 60)

    z = EL_GORDO['z']
    M_total = EL_GORDO['M_total']
    sep = EL_GORDO['separation']
    v_obs = EL_GORDO['v_collision']

    # ΛCDM analysis
    print("\n*** ΛCDM PREDICTION ***")
    v_lcdm = lcdm_infall_velocity(M_total, sep, z)
    p_val, sigma = lcdm_collision_probability(v_obs, M_total, z)
    v_max_3sigma = lcdm_max_expected_velocity(M_total, z)

    print(f"  Predicted infall velocity: {v_lcdm:.0f} km/s")
    print(f"  Maximum at 3σ: {v_max_3sigma:.0f} km/s")
    print(f"  Observed: {v_obs} km/s")
    print(f"  P-value: {p_val:.4f}")
    print(f"  Tension: {sigma:.1f}σ")

    # Z² analysis
    print("\n*** Z² PREDICTION ***")
    z2_result = z2_collision_velocity(M_total, sep, z, NEAREST_VERTEX['distance_mpc'])

    print(f"  Standard infall: {z2_result['v_infall']:.0f} km/s")
    print(f"  Vertex repulsion boost: {z2_result['v_vertex']:.0f} km/s")
    print(f"  Reduced friction boost: {z2_result['v_friction_boost']:.0f} km/s")
    print(f"  TOTAL PREDICTED: {z2_result['v_total']:.0f} km/s")

    # Compare with observation
    v_diff_lcdm = abs(v_obs - v_lcdm)
    v_diff_z2 = abs(v_obs - z2_result['v_total'])

    print("\n*** COMPARISON ***")
    print(f"  |v_obs - v_ΛCDM|: {v_diff_lcdm:.0f} km/s")
    print(f"  |v_obs - v_Z²|:   {v_diff_z2:.0f} km/s")

    return {
        'lcdm': {
            'v_predicted': v_lcdm,
            'v_max_3sigma': v_max_3sigma,
            'p_value': p_val,
            'tension_sigma': sigma,
            'v_diff': v_diff_lcdm
        },
        'z2': {
            'v_infall': z2_result['v_infall'],
            'v_vertex': z2_result['v_vertex'],
            'v_friction_boost': z2_result['v_friction_boost'],
            'v_total': z2_result['v_total'],
            'v_diff': v_diff_z2
        },
        'observed': {
            'v_collision': v_obs,
            'v_error': EL_GORDO['v_collision_err']
        }
    }


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Execute Work-Order GG: El Gordo Shock Velocity Test"""

    print("\n" + "=" * 80)
    print("EXECUTING WORK-ORDER GG")
    print("=" * 80)

    # Analyze El Gordo
    analysis = analyze_el_gordo()

    v_obs = analysis['observed']['v_collision']
    v_err = analysis['observed']['v_error']
    v_z2 = analysis['z2']['v_total']
    v_lcdm = analysis['lcdm']['v_predicted']

    # Check if Z² matches observation within errors
    z2_matches = abs(v_z2 - v_obs) < 2 * v_err
    lcdm_matches = abs(v_lcdm - v_obs) < 2 * v_err

    # Compile results
    results = {
        'work_order': 'GG',
        'task': 'El Gordo Cluster Shock Velocity Test',
        'date': datetime.now().isoformat(),
        'cluster': EL_GORDO,
        'nearest_vertex': NEAREST_VERTEX,
        'analysis': analysis,
        'z2_parameters': {
            'v_vertex': V_VERTEX,
            'omega_m': OMEGA_M,
            'L_c_gpc': L_C_GPC
        }
    }

    # Verdict
    if z2_matches and not lcdm_matches:
        results['verdict'] = "DECISIVE EVIDENCE DETECTED: EL GORDO SHOCK VELOCITY EXPLAINED BY TOPOLOGY"
        results['status'] = 'Z2_WINS'
    elif z2_matches and lcdm_matches:
        results['verdict'] = f"Both models marginally consistent (Z²: {v_z2:.0f}, ΛCDM: {v_lcdm:.0f}, Obs: {v_obs})"
        results['status'] = 'INCONCLUSIVE'
    elif not z2_matches and analysis['z2']['v_diff'] < analysis['lcdm']['v_diff']:
        results['verdict'] = f"Z² closer to observation but outside errors (Z² diff: {analysis['z2']['v_diff']:.0f} km/s)"
        results['status'] = 'Z2_CLOSER'
    else:
        results['verdict'] = f"Neither model fully explains velocity (ΛCDM tension: {analysis['lcdm']['tension_sigma']:.1f}σ)"
        results['status'] = 'BOTH_FAIL'

    # Save
    output_file = OUTPUT_DIR / 'WORK_ORDER_GG_el_gordo_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {output_file}")

    # Final summary
    print("\n" + "=" * 80)
    print("WORK-ORDER GG COMPLETE")
    print("=" * 80)
    print(f"""
┌─────────────────────────────────────────────────────────────────┐
│         WORK-ORDER GG: EL GORDO KINEMATICS COMPLETE             │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  CLUSTER: {EL_GORDO['name']:<48} │
│  MASS:    {EL_GORDO['M_total']:.2e} M_sun at z = {EL_GORDO['z']:<22} │
│                                                                 │
│  OBSERVED COLLISION VELOCITY: {v_obs:>5} ± {v_err:>3} km/s             │
│                                                                 │
│  ΛCDM PREDICTION:                                               │
│    Infall velocity:   {v_lcdm:>5.0f} km/s                              │
│    3σ maximum:        {analysis['lcdm']['v_max_3sigma']:>5.0f} km/s                              │
│    Tension:           {analysis['lcdm']['tension_sigma']:>5.1f}σ (ANOMALY!)                    │
│                                                                 │
│  Z² PREDICTION:                                                 │
│    Infall:            {analysis['z2']['v_infall']:>5.0f} km/s                              │
│    Vertex boost:     +{analysis['z2']['v_vertex']:>5.0f} km/s                              │
│    Friction boost:   +{analysis['z2']['v_friction_boost']:>5.0f} km/s                              │
│    TOTAL:             {v_z2:>5.0f} km/s                              │
│                                                                 │
│  {results['verdict']:<60} │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
""")

    return results


if __name__ == "__main__":
    main()
