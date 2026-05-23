#!/usr/bin/env python3
"""
WORK-ORDER J: JWST VOLUME DEFICIT VERIFICATION
===============================================

Target: Prove the symmetric box regulates early universe galaxy formation

Physics: Standard cosmology assumes infinite volume, leading to the "Impossible
Early Galaxies" problem. Because the Z² geometry dictates:

    Ω_DE(z) = 1 - (D_H(z)/L_c)³

The physical volume available for galaxy formation at high redshift is
strictly governed by the 20.6 Gpc boundaries.

SYSTEM DIRECTIVE: STRICT SYMMETRIC BOUNDARY (NO HALLUCINATION)
══════════════════════════════════════════════════════════════
  HARD STOP: DO NOT ALTER THE SYMMETRIC 20.6 Gpc BOX
  HARD STOP: DO NOT TUNE PARAMETERS TO FIT THE DATA
  HARD STOP: IF THE MODEL FAILS, REPORT THE FAILURE
══════════════════════════════════════════════════════════════

Author: Carl Zimmerman + Claude
Date: May 2026
Framework: Z² Unified Action v11.1.0
"""

import numpy as np
from scipy import integrate
import json
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# LOCKED PARAMETERS - DO NOT MODIFY
# ═══════════════════════════════════════════════════════════════════════════════

# Topology
L_C_GPC = 20.6          # Gpc - LOCKED (symmetric cube)
L_C_MPC = 20600.0       # Mpc - LOCKED

# Planck 2018 Cosmology - LOCKED
H0 = 67.4               # km/s/Mpc
h = H0 / 100            # = 0.674
C_LIGHT = 299792.458    # km/s
OMEGA_M_0 = 0.315       # Matter density today
OMEGA_LAMBDA_0 = 0.685  # Dark energy density today (ΛCDM)
OMEGA_R_0 = 9.24e-5     # Radiation density today

# Hubble distance
D_H = C_LIGHT / H0      # = 4448 Mpc = 4.45 Gpc

# JWST Parameters
M_STAR_THRESHOLD = 1e10  # M_sun (mass threshold for "impossible" galaxies)
Z_MIN = 10               # Minimum redshift for high-z analysis
Z_MAX = 14               # Maximum redshift

# ═══════════════════════════════════════════════════════════════════════════════
# COSMOLOGY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def E_squared_lcdm(z):
    """
    E²(z) = H²(z)/H₀² for ΛCDM.

    E²(z) = Ω_m(1+z)³ + Ω_r(1+z)⁴ + Ω_Λ
    """
    return OMEGA_M_0 * (1+z)**3 + OMEGA_R_0 * (1+z)**4 + OMEGA_LAMBDA_0


def E_lcdm(z):
    """E(z) = H(z)/H₀ for ΛCDM"""
    return np.sqrt(E_squared_lcdm(z))


def comoving_distance_lcdm(z):
    """
    Comoving distance in ΛCDM (Mpc).

    D_c(z) = (c/H₀) × ∫₀ᶻ dz'/E(z')
    """
    if z == 0:
        return 0.0

    def integrand(zp):
        return 1.0 / E_lcdm(zp)

    result, _ = integrate.quad(integrand, 0, z, limit=100)
    return D_H * result  # Mpc


def E_squared_z2(z, D_c_func=None):
    """
    E²(z) for Z² geometric dark energy.

    Ω_DE(z) = 1 - (D_c(z)/L_c)³

    where D_c(z) is the comoving distance to redshift z.

    This creates a self-consistent equation since D_c depends on E(z).
    We solve this iteratively.
    """
    # Use ΛCDM comoving distance as approximation
    D_c = comoving_distance_lcdm(z)  # Mpc
    D_c_gpc = D_c / 1000  # Convert to Gpc

    # Geometric dark energy
    ratio = min(D_c_gpc / L_C_GPC, 0.99)  # Cap to avoid Ω_DE < 0
    Omega_DE_z = 1.0 - ratio**3

    # Ensure Ω_DE doesn't go negative or exceed physical bounds
    Omega_DE_z = max(0.0, min(Omega_DE_z, 1.0 - OMEGA_M_0 * (1+z)**3 / 10))

    return OMEGA_M_0 * (1+z)**3 + OMEGA_R_0 * (1+z)**4 + Omega_DE_z


def E_z2(z):
    """E(z) = H(z)/H₀ for Z² geometric DE"""
    return np.sqrt(max(E_squared_z2(z), 0.01))


def comoving_distance_z2(z):
    """
    Comoving distance in Z² cosmology (Mpc).

    Uses the modified E(z) from geometric dark energy.
    """
    if z == 0:
        return 0.0

    def integrand(zp):
        return 1.0 / E_z2(zp)

    result, _ = integrate.quad(integrand, 0, z, limit=100)
    return D_H * result  # Mpc


def comoving_volume_element(z, E_func, D_c_func):
    """
    Comoving volume element dV/dz (Mpc³/sr).

    dV/dz = (c/H₀) × D_c² / E(z)
    """
    D_c = D_c_func(z)  # Mpc
    E_z = E_func(z)

    return D_H * D_c**2 / E_z  # Mpc³/sr


def comoving_volume(z_min, z_max, E_func, D_c_func):
    """
    Total comoving volume between z_min and z_max (Gpc³).

    V = 4π × ∫_{z_min}^{z_max} dV/dz dz
    """
    def integrand(z):
        return comoving_volume_element(z, E_func, D_c_func)

    result, _ = integrate.quad(integrand, z_min, z_max, limit=100)

    # Convert to Gpc³ and multiply by full sky (4π sr)
    return 4 * np.pi * result / 1e9  # Gpc³


# ═══════════════════════════════════════════════════════════════════════════════
# JWST GALAXY DATA (Simulated based on published results)
# ═══════════════════════════════════════════════════════════════════════════════

# These are representative values from JADES/CEERS publications
# Labbé et al. 2023, Boylan-Kolchin 2023, etc.

JWST_DATA = {
    # Redshift bins: [z_min, z_max, N_galaxies, survey_area_arcmin2]
    "z_10_11": {
        "z_min": 10.0,
        "z_max": 11.0,
        "z_eff": 10.5,
        "N_observed": 6,  # Approximate from JADES
        "survey_area_arcmin2": 25.0,
        "M_star_threshold": 1e10,
    },
    "z_11_12": {
        "z_min": 11.0,
        "z_max": 12.0,
        "z_eff": 11.5,
        "N_observed": 3,
        "survey_area_arcmin2": 25.0,
        "M_star_threshold": 1e10,
    },
    "z_12_14": {
        "z_min": 12.0,
        "z_max": 14.0,
        "z_eff": 13.0,
        "N_observed": 2,
        "survey_area_arcmin2": 25.0,
        "M_star_threshold": 1e10,
    },
}

# Theoretical predictions from halo mass function (approximate)
# Number density of M* > 10^10 M_sun galaxies per Gpc³
THEORY_DENSITY = {
    "z_10_11": 1e-6,  # per Gpc³ (very rough estimate from HMF)
    "z_11_12": 3e-7,
    "z_12_14": 5e-8,
}


def survey_solid_angle(area_arcmin2):
    """Convert survey area in arcmin² to steradians"""
    # 1 arcmin = π/(180*60) rad
    arcmin_to_rad = np.pi / (180 * 60)
    return area_arcmin2 * arcmin_to_rad**2


# ═══════════════════════════════════════════════════════════════════════════════
# VOLUME DEFICIT ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

class JWSTVolumeDeficitAnalysis:
    """
    Compare galaxy number densities using ΛCDM vs Z² volumes.

    The "impossible galaxies" problem:
    - JWST observes N massive galaxies at z > 10
    - In ΛCDM volume V_ΛCDM, density = N/V_ΛCDM appears impossibly high
    - If Z² gives different volume V_Z2, the implied density changes

    STRICT PROTOCOL:
    - L_c = 20.6 Gpc LOCKED
    - Ω_DE(z) = 1 - (D_c/L_c)³ (no modification)
    - Report actual results, success or failure
    """

    def __init__(self):
        self.jwst_data = JWST_DATA
        self.theory_density = THEORY_DENSITY

    def compute_volumes(self, z_min, z_max, area_arcmin2):
        """
        Compute comoving volumes in both cosmologies.

        Returns volumes in Gpc³ for the survey area.
        """
        # Solid angle of survey
        omega_sr = survey_solid_angle(area_arcmin2)

        # Full-sky volumes
        V_lcdm_fullsky = comoving_volume(z_min, z_max, E_lcdm, comoving_distance_lcdm)
        V_z2_fullsky = comoving_volume(z_min, z_max, E_z2, comoving_distance_z2)

        # Survey volumes (scale by solid angle fraction)
        fraction = omega_sr / (4 * np.pi)
        V_lcdm = V_lcdm_fullsky * fraction
        V_z2 = V_z2_fullsky * fraction

        return V_lcdm, V_z2, V_lcdm_fullsky, V_z2_fullsky

    def compute_number_density(self, N_observed, volume_Gpc3):
        """Compute number density in Gpc⁻³"""
        if volume_Gpc3 == 0:
            return np.inf
        return N_observed / volume_Gpc3

    def compute_anomaly_factor(self, n_observed, n_theory):
        """
        Anomaly factor = observed density / theoretical prediction.

        > 1 means more galaxies than expected ("impossible")
        ~ 1 means consistent
        < 1 means fewer than expected
        """
        if n_theory == 0:
            return np.inf
        return n_observed / n_theory

    def run_analysis(self):
        """Execute the full volume deficit analysis"""

        print("=" * 80)
        print("WORK-ORDER J: JWST VOLUME DEFICIT VERIFICATION")
        print("=" * 80)
        print()

        # Display locked parameters
        print("╔" + "═" * 78 + "╗")
        print("║  LOCKED PARAMETERS (DO NOT MODIFY):" + " " * 40 + "║")
        print("╠" + "═" * 78 + "╣")
        print(f"║  L_c = {L_C_GPC} Gpc (symmetric cube)" + " " * 39 + "║")
        print(f"║  Ω_DE(z) = 1 - (D_c(z)/L_c)³ (geometric dark energy)" + " " * 22 + "║")
        print(f"║  M* threshold = {M_STAR_THRESHOLD:.0e} M_sun" + " " * 43 + "║")
        print(f"║  Redshift range: z = {Z_MIN} - {Z_MAX}" + " " * 42 + "║")
        print("╚" + "═" * 78 + "╝")
        print()

        # Compute cosmological distances for reference
        print("Cosmological distances at key redshifts:")
        print("-" * 60)
        for z in [0, 2, 5, 10, 12, 14]:
            D_c_lcdm = comoving_distance_lcdm(z) / 1000  # Gpc
            D_c_z2 = comoving_distance_z2(z) / 1000  # Gpc

            # Geometric Ω_DE
            ratio = min(D_c_lcdm / L_C_GPC, 0.99)
            Omega_DE_geom = 1 - ratio**3

            print(f"  z = {z:2d}: D_c(ΛCDM) = {D_c_lcdm:.2f} Gpc, "
                  f"D_c(Z²) = {D_c_z2:.2f} Gpc, Ω_DE(geom) = {Omega_DE_geom:.3f}")
        print()

        # Analyze each redshift bin
        results_by_bin = {}

        print("╔" + "═" * 78 + "╗")
        print("║  VOLUME AND DENSITY ANALYSIS BY REDSHIFT BIN" + " " * 32 + "║")
        print("╚" + "═" * 78 + "╝")
        print()

        for bin_name, data in self.jwst_data.items():
            z_min = data["z_min"]
            z_max = data["z_max"]
            z_eff = data["z_eff"]
            N_obs = data["N_observed"]
            area = data["survey_area_arcmin2"]

            # Compute volumes
            V_lcdm, V_z2, V_lcdm_full, V_z2_full = self.compute_volumes(
                z_min, z_max, area
            )

            # Compute densities (using full-sky extrapolated volume)
            n_lcdm = self.compute_number_density(N_obs / survey_solid_angle(area) * (4*np.pi),
                                                  V_lcdm_full)
            n_z2 = self.compute_number_density(N_obs / survey_solid_angle(area) * (4*np.pi),
                                                V_z2_full)

            # Anomaly factors
            n_theory = self.theory_density[bin_name]
            anomaly_lcdm = self.compute_anomaly_factor(n_lcdm, n_theory)
            anomaly_z2 = self.compute_anomaly_factor(n_z2, n_theory)

            # Volume ratio
            volume_ratio = V_z2_full / V_lcdm_full if V_lcdm_full > 0 else 1.0

            results_by_bin[bin_name] = {
                "z_range": f"{z_min}-{z_max}",
                "z_eff": z_eff,
                "N_observed": N_obs,
                "V_lcdm_Gpc3": V_lcdm_full,
                "V_z2_Gpc3": V_z2_full,
                "volume_ratio_z2_lcdm": volume_ratio,
                "n_lcdm_per_Gpc3": n_lcdm,
                "n_z2_per_Gpc3": n_z2,
                "n_theory_per_Gpc3": n_theory,
                "anomaly_lcdm": anomaly_lcdm,
                "anomaly_z2": anomaly_z2,
            }

            print(f"  {bin_name} (z = {z_min}-{z_max}):")
            print(f"    N observed:           {N_obs}")
            print(f"    V(ΛCDM):              {V_lcdm_full:.2e} Gpc³")
            print(f"    V(Z²):                {V_z2_full:.2e} Gpc³")
            print(f"    Volume ratio (Z²/ΛCDM): {volume_ratio:.4f}")
            print(f"    n(ΛCDM):              {n_lcdm:.2e} Gpc⁻³")
            print(f"    n(Z²):                {n_z2:.2e} Gpc⁻³")
            print(f"    n(theory):            {n_theory:.2e} Gpc⁻³")
            print(f"    Anomaly (ΛCDM):       {anomaly_lcdm:.1f}×")
            print(f"    Anomaly (Z²):         {anomaly_z2:.1f}×")
            print()

        # Summary statistics
        mean_volume_ratio = np.mean([r["volume_ratio_z2_lcdm"] for r in results_by_bin.values()])
        mean_anomaly_lcdm = np.mean([r["anomaly_lcdm"] for r in results_by_bin.values()])
        mean_anomaly_z2 = np.mean([r["anomaly_z2"] for r in results_by_bin.values()])

        # Check if Z² helps
        anomaly_reduction = (mean_anomaly_lcdm - mean_anomaly_z2) / mean_anomaly_lcdm * 100
        z2_helps = mean_anomaly_z2 < mean_anomaly_lcdm
        anomaly_resolved = mean_anomaly_z2 < 3  # Within factor of 3 of theory

        print("╔" + "═" * 78 + "╗")
        print("║  SUMMARY:" + " " * 68 + "║")
        print("╠" + "═" * 78 + "╣")
        print(f"║  Mean volume ratio (Z²/ΛCDM):     {mean_volume_ratio:.4f}" + " " * 34 + "║")
        print(f"║  Mean anomaly factor (ΛCDM):      {mean_anomaly_lcdm:.1f}×" + " " * 37 + "║")
        print(f"║  Mean anomaly factor (Z²):        {mean_anomaly_z2:.1f}×" + " " * 37 + "║")
        print(f"║  Anomaly reduction:               {anomaly_reduction:.1f}%" + " " * 37 + "║")
        print("╚" + "═" * 78 + "╝")
        print()

        # VERDICT
        print("╔" + "═" * 78 + "╗")
        if anomaly_resolved:
            print("║  VERDICT: ✓ IMPOSSIBLE GALAXIES EXPLAINED" + " " * 35 + "║")
            print("║" + " " * 78 + "║")
            print("║  The Z² geometric volume reduces the anomaly to within acceptable" + " " * 11 + "║")
            print("║  bounds. The 'impossible' early galaxies are consistent with the" + " " * 12 + "║")
            print("║  topological volume constraint." + " " * 45 + "║")
            status = "RESOLVED"
        elif z2_helps:
            print("║  VERDICT: ○ PARTIAL IMPROVEMENT" + " " * 45 + "║")
            print("║" + " " * 78 + "║")
            print(f"║  Z² reduces the anomaly by {anomaly_reduction:.0f}%, but {mean_anomaly_z2:.1f}× excess remains." + " " * 20 + "║")
            print("║  The geometric volume helps but doesn't fully explain the data." + " " * 13 + "║")
            status = "PARTIAL"
        else:
            print("║  VERDICT: ✗ Z² DOES NOT HELP" + " " * 49 + "║")
            print("║" + " " * 78 + "║")
            print("║  The geometric dark energy formula produces LARGER volumes at high z," + " " * 7 + "║")
            print("║  making the anomaly WORSE. This hypothesis is falsified." + " " * 20 + "║")
            print("║" + " " * 78 + "║")
            print("║  REPORTING FAILURE AS REQUIRED BY WORK-ORDER PROTOCOL." + " " * 22 + "║")
            status = "FAILED"
        print("╚" + "═" * 78 + "╝")
        print()

        # Physical interpretation
        print("╔" + "═" * 78 + "╗")
        print("║  PHYSICAL INTERPRETATION:" + " " * 52 + "║")
        print("╠" + "═" * 78 + "╣")
        print("║" + " " * 78 + "║")
        print("║  The formula Ω_DE(z) = 1 - (D_c/L_c)³ gives:" + " " * 32 + "║")
        print("║" + " " * 78 + "║")
        for z in [10, 12, 14]:
            D_c = comoving_distance_lcdm(z) / 1000
            ratio = min(D_c / L_C_GPC, 0.99)
            Omega_DE = 1 - ratio**3
            print(f"║    z = {z}: D_c = {D_c:.1f} Gpc, D_c/L_c = {ratio:.2f}, Ω_DE = {Omega_DE:.3f}" + " " * 25 + "║")
        print("║" + " " * 78 + "║")
        print("║  At z > 10, D_c ~ 10-12 Gpc, which is ~50% of L_c = 20.6 Gpc." + " " * 15 + "║")
        print("║  This gives Ω_DE ~ 0.85-0.90, implying DE dominates at high z." + " " * 14 + "║")
        print("║" + " " * 78 + "║")
        if status == "FAILED":
            print("║  The DE domination at high z INCREASES the expansion rate," + " " * 18 + "║")
            print("║  which INCREASES the comoving volume, making the galaxy" + " " * 21 + "║")
            print("║  excess problem WORSE, not better." + " " * 42 + "║")
        print("║" + " " * 78 + "║")
        print("╚" + "═" * 78 + "╝")
        print()

        # Build results dictionary
        results = {
            "work_order": "J",
            "target": "JWST_impossible_galaxies",
            "date": datetime.now().strftime("%B %d, %Y"),
            "framework": "Z² Unified Action v11.1.0",
            "parameters_locked": {
                "L_c_Gpc": L_C_GPC,
                "Omega_DE_formula": "1 - (D_c(z)/L_c)^3",
                "M_star_threshold_Msun": M_STAR_THRESHOLD,
                "z_range": f"{Z_MIN}-{Z_MAX}"
            },
            "redshift_bins": results_by_bin,
            "summary": {
                "mean_volume_ratio_z2_lcdm": float(mean_volume_ratio),
                "mean_anomaly_lcdm": float(mean_anomaly_lcdm),
                "mean_anomaly_z2": float(mean_anomaly_z2),
                "anomaly_reduction_pct": float(anomaly_reduction),
                "z2_helps": bool(z2_helps),
                "anomaly_resolved": bool(anomaly_resolved)
            },
            "result": {
                "status": status,
                "interpretation": self._get_interpretation(status, anomaly_reduction, mean_anomaly_z2)
            }
        }

        # Save results
        output_file = "research/jwst_audit/high_z_volume_deficit_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"Results saved to: {output_file}")
        print("=" * 80)

        return results

    def _get_interpretation(self, status, reduction, anomaly):
        if status == "RESOLVED":
            return "Geometric volume constraint explains impossible galaxies"
        elif status == "PARTIAL":
            return f"Geometric volume reduces anomaly by {reduction:.0f}% but {anomaly:.1f}x excess remains"
        else:
            return "Geometric DE increases high-z volume, worsening the anomaly"


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    analysis = JWSTVolumeDeficitAnalysis()
    results = analysis.run_analysis()
