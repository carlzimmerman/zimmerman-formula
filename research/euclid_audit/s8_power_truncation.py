#!/usr/bin/env python3
"""
WORK-ORDER I: S₈ POWER SPECTRUM TRUNCATION
==========================================

Target: Explain the S₈ tension (Planck 0.811 vs local 0.76)

Physics: In finite T³/Z₂ topology, P(k) = 0 for k < k_min = 2π/L_c.
Missing large-scale power reduces σ₈.

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
from scipy.special import spherical_jn
import json
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# LOCKED PARAMETERS - DO NOT MODIFY
# ═══════════════════════════════════════════════════════════════════════════════

# Topology
L_C_GPC = 20.6          # Gpc - LOCKED (symmetric cube)
L_C_MPC = 20600.0       # Mpc - LOCKED
K_MIN = 2 * np.pi / L_C_MPC  # = 3.05e-4 Mpc^-1 - LOCKED (fundamental mode)

# Planck 2018 Cosmology - LOCKED
H0 = 67.4               # km/s/Mpc
h = H0 / 100            # = 0.674
OMEGA_M = 0.315
OMEGA_B = 0.0493
OMEGA_CDM = OMEGA_M - OMEGA_B
OMEGA_LAMBDA = 1 - OMEGA_M
N_S = 0.9649            # Spectral index
SIGMA_8_PLANCK = 0.811  # Planck ΛCDM value
A_S = 2.1e-9            # Scalar amplitude

# Integration parameters
R_8 = 8.0 / h           # 8 Mpc/h in Mpc = 11.87 Mpc
K_MAX = 10.0            # Mpc^-1 (sufficient for σ₈ convergence)

# ═══════════════════════════════════════════════════════════════════════════════
# MATTER POWER SPECTRUM (Eisenstein & Hu 1998 Transfer Function)
# ═══════════════════════════════════════════════════════════════════════════════

class MatterPowerSpectrum:
    """
    Matter power spectrum using Eisenstein & Hu (1998) transfer function.

    This is the standard ΛCDM P(k) without any modifications.
    """

    def __init__(self):
        # Derived parameters
        self.omega_m = OMEGA_M * h**2
        self.omega_b = OMEGA_B * h**2
        self.omega_cdm = OMEGA_CDM * h**2

        # Sound horizon fitting (Eisenstein & Hu)
        self.theta_cmb = 2.7255 / 2.7  # CMB temperature ratio
        self.z_eq = 2.5e4 * self.omega_m * self.theta_cmb**(-4)
        self.k_eq = 0.0746 * self.omega_m * self.theta_cmb**(-2)  # Mpc^-1

        # Baryon fraction
        self.f_b = OMEGA_B / OMEGA_M
        self.f_c = OMEGA_CDM / OMEGA_M

        # Sound horizon
        self.z_drag = self._z_drag()
        self.r_s = self._sound_horizon()

        # Normalize to Planck σ₈
        self.A_norm = self._normalize_amplitude()

    def _z_drag(self):
        """Redshift at baryon drag epoch"""
        b1 = 0.313 * self.omega_m**(-0.419) * (1 + 0.607 * self.omega_m**0.674)
        b2 = 0.238 * self.omega_m**0.223
        return 1291 * self.omega_m**0.251 / (1 + 0.659 * self.omega_m**0.828) * \
               (1 + b1 * self.omega_b**b2)

    def _sound_horizon(self):
        """Sound horizon at drag epoch in Mpc"""
        return 44.5 * np.log(9.83 / self.omega_m) / \
               np.sqrt(1 + 10 * self.omega_b**0.75)

    def transfer_function(self, k):
        """
        Eisenstein & Hu (1998) transfer function T(k).

        This gives the shape of P(k). The full power spectrum is:
        P(k) = A * k^n_s * T(k)^2
        """
        # Convert to h/Mpc for EH98 formula
        q = k / (self.omega_m * h)  # Scaled wavenumber

        # Fitting parameters
        alpha_c = self._alpha_c()
        beta_c = self._beta_c()

        # CDM transfer function (no wiggles approximation)
        f = 1 / (1 + (k * self.r_s / 5.4)**4)

        L = np.log(np.e + 1.8 * beta_c * q)
        C = 14.2 / alpha_c + 386 / (1 + 69.9 * q**1.08)
        T_c = L / (L + C * q**2)

        # Baryon transfer function (simplified)
        T_b = T_c  # Using CDM approximation for simplicity

        # Total transfer function
        T_k = self.f_c * T_c + self.f_b * T_b

        return T_k

    def _alpha_c(self):
        """CDM shape parameter"""
        a1 = (46.9 * self.omega_m)**0.670 * (1 + (32.1 * self.omega_m)**(-0.532))
        a2 = (12.0 * self.omega_m)**0.424 * (1 + (45.0 * self.omega_m)**(-0.582))
        return a1**(-self.f_b) * a2**(-self.f_b**3)

    def _beta_c(self):
        """CDM logarithmic slope"""
        b1 = 0.944 / (1 + (458 * self.omega_m)**(-0.708))
        b2 = (0.395 * self.omega_m)**(-0.0266)
        return 1 / (1 + b1 * ((self.f_c)**b2 - 1))

    def _normalize_amplitude(self):
        """
        Normalize power spectrum amplitude to match Planck σ₈ = 0.811.

        This ensures our ΛCDM baseline is correct before truncation.
        """
        # Compute σ₈ with unit amplitude using unnormalized P(k)
        sigma8_unit = self._compute_sigma8_unnormalized()

        # Scale to match Planck
        return (SIGMA_8_PLANCK / sigma8_unit)**2

    def _compute_sigma8_unnormalized(self):
        """Compute σ₈ with A_norm = 1 for normalization purposes."""

        def integrand(k):
            if k < 1e-6:
                return 0.0

            x = k * R_8
            if x < 0.01:
                W = 1 - x**2 / 10
            else:
                W = 3 * (np.sin(x) - x * np.cos(x)) / x**3

            P = self.P_k_unnormalized(np.array([k]))[0]
            return k**2 * P * W**2

        result, _ = integrate.quad(integrand, 1e-5, K_MAX, limit=200, epsrel=1e-6)
        sigma_sq = result / (2 * np.pi**2)
        return np.sqrt(sigma_sq)

    def P_k_unnormalized(self, k):
        """
        Unnormalized matter power spectrum (for computing normalization).
        """
        k = np.atleast_1d(k)
        k_pivot = 0.05  # Mpc^-1

        # Shape only (A_norm = 1)
        P_prim = (k / k_pivot)**(N_S - 1)
        T_k = self.transfer_function(k)
        P = P_prim * k**N_S * T_k**2

        return P

    def P_k(self, k, k_min=0.0):
        """
        Matter power spectrum P(k) in (Mpc)³.

        Parameters:
        -----------
        k : float or array
            Wavenumber in Mpc^-1
        k_min : float
            Minimum wavenumber cutoff (0 for ΛCDM, 2π/L_c for Z²)

        Returns:
        --------
        P(k) : float or array
            Power spectrum in Mpc³
        """
        k = np.atleast_1d(k)

        # Normalized power spectrum
        P = self.A_norm * self.P_k_unnormalized(k)

        # STRICT CUTOFF (Heaviside step function)
        # DO NOT SMOOTH THIS - it is a hard topological boundary
        P = np.where(k >= k_min, P, 0.0)

        return P

    def _compute_sigma8(self, k_min=0.0):
        """
        Compute σ₈ = σ(R=8 Mpc/h).

        σ²(R) = (1/2π²) ∫ k² P(k) W²(kR) dk

        where W(x) = 3(sin(x) - x cos(x))/x³ is the top-hat window.
        """

        def integrand(k):
            if k < 1e-6:
                return 0.0

            # Top-hat window function
            x = k * R_8
            if x < 0.01:
                W = 1 - x**2 / 10  # Taylor expansion for small x
            else:
                W = 3 * (np.sin(x) - x * np.cos(x)) / x**3

            # Normalized P(k) with cutoff
            P = self.P_k(np.array([k]), k_min=k_min)[0]

            return k**2 * P * W**2

        # Integration from k_min to k_max
        k_low = max(k_min, 1e-5)  # Avoid numerical issues at k=0

        # Use adaptive quadrature
        result, error = integrate.quad(integrand, k_low, K_MAX,
                                       limit=200, epsrel=1e-6)

        sigma_sq = result / (2 * np.pi**2)
        return np.sqrt(sigma_sq)

# ═══════════════════════════════════════════════════════════════════════════════
# S₈ TRUNCATION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

class S8TruncationAnalysis:
    """
    Compute S₈ with and without topological IR cutoff.

    STRICT BOUNDARY: k_min = 2π/L_c = 2π/(20.6 Gpc) = 3.05e-4 Mpc^-1

    NO SMOOTHING, NO TUNING.
    """

    def __init__(self):
        self.pspec = MatterPowerSpectrum()

        # Comparison values (LOCKED)
        self.S8_planck = 0.811
        self.S8_des_y3 = 0.776
        self.S8_kids_1000 = 0.759
        self.S8_local_mean = (self.S8_des_y3 + self.S8_kids_1000) / 2  # = 0.768

        # Errors
        self.S8_planck_err = 0.006
        self.S8_local_err = 0.020  # Combined

    def compute_sigma8_lcdm(self):
        """σ₈ in standard ΛCDM (no cutoff)"""
        return self.pspec._compute_sigma8(k_min=0.0)

    def compute_sigma8_z2(self):
        """σ₈ in Z² framework with strict IR cutoff"""
        return self.pspec._compute_sigma8(k_min=K_MIN)

    def compute_S8(self, sigma8):
        """S₈ = σ₈ × √(Ω_m/0.3)"""
        return sigma8 * np.sqrt(OMEGA_M / 0.3)

    def compute_power_removed(self):
        """
        Fraction of σ₈² removed by the IR cutoff.

        This shows how much large-scale power is missing in finite topology.
        """
        sigma8_lcdm = self.compute_sigma8_lcdm()
        sigma8_z2 = self.compute_sigma8_z2()

        # Fractional variance removed
        var_removed = 1 - (sigma8_z2 / sigma8_lcdm)**2
        return var_removed

    def run_analysis(self):
        """
        Execute the full S₈ truncation analysis.

        STRICT PROTOCOL:
        - Use k_min = 2π/L_c exactly
        - No smoothing of cutoff
        - Report failure if tension not resolved
        """
        print("=" * 80)
        print("WORK-ORDER I: S₈ POWER SPECTRUM TRUNCATION")
        print("=" * 80)
        print()

        # Display locked parameters
        print("╔" + "═" * 78 + "╗")
        print("║  LOCKED PARAMETERS (DO NOT MODIFY):" + " " * 40 + "║")
        print("╠" + "═" * 78 + "╣")
        print(f"║  L_c = {L_C_GPC} Gpc (symmetric cube)" + " " * 39 + "║")
        print(f"║  k_min = 2π/L_c = {K_MIN:.6e} Mpc⁻¹" + " " * 30 + "║")
        print(f"║  Cutoff type: STRICT HEAVISIDE (no smoothing)" + " " * 30 + "║")
        print("╚" + "═" * 78 + "╝")
        print()

        # Compute σ₈ values
        print("Computing σ₈...")
        sigma8_lcdm = self.compute_sigma8_lcdm()
        sigma8_z2 = self.compute_sigma8_z2()

        print(f"  σ₈ (ΛCDM, no cutoff):    {sigma8_lcdm:.6f}")
        print(f"  σ₈ (Z², k_min cutoff):   {sigma8_z2:.6f}")
        print()

        # Compute S₈ values
        S8_lcdm = self.compute_S8(sigma8_lcdm)
        S8_z2 = self.compute_S8(sigma8_z2)

        print(f"Computing S₈ = σ₈ × √(Ω_m/0.3)...")
        print(f"  S₈ (ΛCDM):    {S8_lcdm:.4f}")
        print(f"  S₈ (Z²):      {S8_z2:.4f}")
        print()

        # Power removed
        power_removed = self.compute_power_removed()
        print(f"Power removed by IR cutoff: {power_removed*100:.2f}%")
        print()

        # Comparison
        print("╔" + "═" * 78 + "╗")
        print("║  COMPARISON:" + " " * 65 + "║")
        print("╠" + "═" * 78 + "╣")
        print(f"║  S₈ (Planck CMB):        {self.S8_planck:.3f} ± {self.S8_planck_err:.3f}" + " " * 40 + "║")
        print(f"║  S₈ (DES Y3):            {self.S8_des_y3:.3f} ± 0.017" + " " * 40 + "║")
        print(f"║  S₈ (KiDS-1000):         {self.S8_kids_1000:.3f} ± 0.024" + " " * 40 + "║")
        print(f"║  S₈ (Local mean):        {self.S8_local_mean:.3f}" + " " * 47 + "║")
        print("║" + " " * 78 + "║")
        print(f"║  S₈ (Z² truncated):      {S8_z2:.4f}" + " " * 46 + "║")
        print("╚" + "═" * 78 + "╝")
        print()

        # Tension analysis
        tension_before = (self.S8_planck - self.S8_local_mean) / self.S8_local_err
        tension_after = (S8_z2 - self.S8_local_mean) / self.S8_local_err

        S8_shift = self.S8_planck - S8_z2
        tension_explained = S8_shift / (self.S8_planck - self.S8_local_mean)

        print("╔" + "═" * 78 + "╗")
        print("║  TENSION ANALYSIS:" + " " * 59 + "║")
        print("╠" + "═" * 78 + "╣")
        print(f"║  Original tension (Planck vs local):  {tension_before:.2f}σ" + " " * 37 + "║")
        print(f"║  S₈ shift from truncation:            {S8_shift:.4f}" + " " * 37 + "║")
        print(f"║  Tension explained:                   {tension_explained*100:.1f}%" + " " * 38 + "║")
        print(f"║  Remaining tension (Z² vs local):     {tension_after:.2f}σ" + " " * 37 + "║")
        print("╚" + "═" * 78 + "╝")
        print()

        # VERDICT
        success = bool(abs(S8_z2 - self.S8_local_mean) < 2 * self.S8_local_err)

        print("╔" + "═" * 78 + "╗")
        if success:
            print("║  VERDICT: ✓ TENSION RESOLVED" + " " * 48 + "║")
            print("║" + " " * 78 + "║")
            print("║  The IR cutoff at k_min = 2π/L_c naturally reduces S₈ to match" + " " * 14 + "║")
            print("║  local weak lensing observations. The S₈ tension is explained" + " " * 15 + "║")
            print("║  by the finite topology of the universe." + " " * 36 + "║")
            status = "RESOLVED"
        else:
            print("║  VERDICT: ✗ TENSION NOT FULLY RESOLVED" + " " * 38 + "║")
            print("║" + " " * 78 + "║")
            print(f"║  The IR cutoff reduces S₈ by {S8_shift:.4f}, but {tension_after:.1f}σ tension remains." + " " * 21 + "║")
            print("║  Additional physics may be required." + " " * 40 + "║")
            print("║" + " " * 78 + "║")
            print("║  REPORTING FAILURE AS REQUIRED BY WORK-ORDER PROTOCOL." + " " * 22 + "║")
            status = "FAILED"
        print("╚" + "═" * 78 + "╝")
        print()

        # Build results dictionary
        results = {
            "work_order": "I",
            "target": "S8_tension",
            "date": datetime.now().strftime("%B %d, %Y"),
            "framework": "Z² Unified Action v11.1.0",
            "parameters_locked": {
                "L_c_Gpc": L_C_GPC,
                "L_c_Mpc": L_C_MPC,
                "k_min_Mpc_inv": float(K_MIN),
                "cutoff_type": "Heaviside_strict_NO_SMOOTHING",
                "Omega_m": OMEGA_M,
                "h": h,
                "n_s": N_S
            },
            "computation": {
                "sigma8_LCDM": float(sigma8_lcdm),
                "sigma8_Z2_truncated": float(sigma8_z2),
                "sigma8_reduction_pct": float((1 - sigma8_z2/sigma8_lcdm) * 100),
                "power_removed_pct": float(power_removed * 100),
                "S8_LCDM": float(S8_lcdm),
                "S8_Z2_truncated": float(S8_z2)
            },
            "comparison": {
                "S8_Planck": self.S8_planck,
                "S8_DES_Y3": self.S8_des_y3,
                "S8_KiDS_1000": self.S8_kids_1000,
                "S8_local_mean": float(self.S8_local_mean),
                "S8_local_err": self.S8_local_err
            },
            "result": {
                "S8_shift": float(S8_shift),
                "tension_before_sigma": float(tension_before),
                "tension_after_sigma": float(tension_after),
                "tension_explained_pct": float(tension_explained * 100),
                "status": status
            },
            "verdict": {
                "success": success,
                "interpretation": "IR cutoff from finite topology reduces large-scale power" if success
                                  else "IR cutoff insufficient to fully resolve tension"
            }
        }

        # Save results
        output_file = "research/euclid_audit/s8_power_truncation_results.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"Results saved to: {output_file}")
        print("=" * 80)

        return results

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    analysis = S8TruncationAnalysis()
    results = analysis.run_analysis()
