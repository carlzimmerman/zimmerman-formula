#!/usr/bin/env python3
"""
ZIMMERMAN FORMULA CALCULATOR
============================

Practical tool for making predictions using the Zimmerman formula:
    a₀ = c√(Gρc)/2 = cH₀/5.79

Usage:
    python zimmerman_calculator.py

Or import as module:
    from zimmerman_calculator import ZimmermanCalculator
    calc = ZimmermanCalculator()
    calc.galaxy_rotation(M_bar=1e11)
"""

import numpy as np
import argparse

class ZimmermanCalculator:
    """Calculator for Zimmerman formula predictions."""

    # Fundamental constants
    c = 299792458           # m/s
    G = 6.67430e-11         # m³/kg/s²
    M_sun = 1.989e30        # kg
    kpc_to_m = 3.08567758e19
    Mpc_to_m = 3.08567758e22

    # Cosmological parameters (Planck 2020)
    Omega_m = 0.315
    Omega_Lambda = 0.685

    # Zimmerman constant
    ZIMMERMAN_CONSTANT = 5.7888  # = 2√(8π/3)

    def __init__(self, H0=67.4):
        """
        Initialize calculator with Hubble constant.

        Parameters:
        -----------
        H0 : float
            Hubble constant in km/s/Mpc (default: 67.4 Planck value)
        """
        self.H0 = H0
        self.H0_SI = H0 * 1000 / self.Mpc_to_m  # Convert to s⁻¹
        self.a0 = self.c * self.H0_SI / self.ZIMMERMAN_CONSTANT

    def print_basics(self):
        """Print basic derived quantities."""
        print("=" * 60)
        print("ZIMMERMAN FORMULA BASICS")
        print("=" * 60)
        print(f"Input H₀:           {self.H0} km/s/Mpc")
        print(f"Zimmerman constant: {self.ZIMMERMAN_CONSTANT:.4f} = 2√(8π/3)")
        print()
        print(f"MOND acceleration:  a₀ = cH₀/5.79 = {self.a0:.3e} m/s²")
        print(f"Observed a₀:        1.2×10⁻¹⁰ m/s²")
        print(f"Agreement:          {abs(self.a0 - 1.2e-10)/1.2e-10 * 100:.1f}%")
        print()

    def a0_at_redshift(self, z):
        """
        Calculate a₀ at redshift z.

        Parameters:
        -----------
        z : float or array
            Redshift

        Returns:
        --------
        a0_z : float or array
            MOND acceleration at redshift z
        """
        E_z = np.sqrt(self.Omega_m * (1 + z)**3 + self.Omega_Lambda)
        return self.a0 * E_z

    def galaxy_rotation(self, M_bar, z=0, verbose=True):
        """
        Predict rotation curve for a galaxy.

        Parameters:
        -----------
        M_bar : float
            Baryonic mass in solar masses
        z : float
            Redshift (default: 0)
        verbose : bool
            Print results

        Returns:
        --------
        dict with v_flat, r_transition, mass_discrepancy
        """
        M = M_bar * self.M_sun
        a0_z = self.a0_at_redshift(z)

        # Deep MOND prediction: v⁴ = G × M × a₀
        v_flat = (self.G * M * a0_z)**0.25 / 1000  # km/s

        # Transition radius: where g_Newton = a₀
        r_trans = np.sqrt(self.G * M / a0_z) / self.kpc_to_m  # kpc

        # Newtonian prediction at large r (for comparison)
        # At r >> r_trans, v_Newton would fall as 1/√r
        # Mass discrepancy = (v_MOND/v_Newton)² at large r
        # In deep MOND: v_MOND/v_Newton ~ √(r/r_trans)

        if verbose:
            print("=" * 60)
            print(f"GALAXY ROTATION PREDICTION (z = {z})")
            print("=" * 60)
            print(f"Baryonic mass:      M_bar = {M_bar:.2e} M☉")
            print(f"Redshift:           z = {z}")
            print(f"a₀(z):              {a0_z:.3e} m/s²")
            print()
            print("MOND PREDICTIONS (no free parameters):")
            print(f"  Flat velocity:    v_flat = {v_flat:.1f} km/s")
            print(f"  Transition radius: r_trans = {r_trans:.1f} kpc")
            print()

        return {
            'v_flat': v_flat,
            'r_transition': r_trans,
            'a0_z': a0_z,
            'M_bar': M_bar
        }

    def hubble_from_a0(self, a0_measured):
        """
        Derive H₀ from measured a₀.

        Parameters:
        -----------
        a0_measured : float
            Measured MOND acceleration in m/s²

        Returns:
        --------
        H0 : float
            Hubble constant in km/s/Mpc
        """
        H0_SI = self.ZIMMERMAN_CONSTANT * a0_measured / self.c
        H0 = H0_SI * self.Mpc_to_m / 1000

        print("=" * 60)
        print("H₀ FROM MOND MEASUREMENT")
        print("=" * 60)
        print(f"Measured a₀:  {a0_measured:.2e} m/s²")
        print(f"Derived H₀:   {H0:.1f} km/s/Mpc")
        print()
        print("Comparison:")
        print(f"  Planck (CMB):     67.4 km/s/Mpc")
        print(f"  Zimmerman:        {H0:.1f} km/s/Mpc  ← YOUR VALUE")
        print(f"  SH0ES (Cepheids): 73.0 km/s/Mpc")
        print()

        return H0

    def cosmological_constant(self, verbose=True):
        """
        Derive cosmological constant from a₀.

        Returns:
        --------
        dict with Lambda, rho_Lambda
        """
        # Asymptotic a₀ (de Sitter limit)
        a0_inf = self.a0 * np.sqrt(self.Omega_Lambda)

        # Dark energy density from a₀
        rho_Lambda = 4 * a0_inf**2 / (self.G * self.c**2)

        # Cosmological constant
        Lambda = 32 * np.pi * a0_inf**2 / self.c**4

        # Observed value for comparison
        rho_c = 3 * self.H0_SI**2 / (8 * np.pi * self.G)
        rho_Lambda_obs = self.Omega_Lambda * rho_c
        Lambda_obs = 8 * np.pi * self.G * rho_Lambda_obs / self.c**2

        if verbose:
            print("=" * 60)
            print("COSMOLOGICAL CONSTANT FROM a₀")
            print("=" * 60)
            print(f"a₀(today):    {self.a0:.3e} m/s²")
            print(f"a₀,∞:         {a0_inf:.3e} m/s² (de Sitter limit)")
            print()
            print("DERIVED VALUES:")
            print(f"  ρ_Λ(derived):  {rho_Lambda:.3e} kg/m³")
            print(f"  ρ_Λ(observed): {rho_Lambda_obs:.3e} kg/m³")
            print(f"  Agreement:     {rho_Lambda/rho_Lambda_obs * 100:.1f}%")
            print()
            print(f"  Λ(derived):    {Lambda:.3e} m⁻²")
            print(f"  Λ(observed):   {Lambda_obs:.3e} m⁻²")
            print(f"  Agreement:     {Lambda/Lambda_obs * 100:.1f}%")
            print()

        return {
            'Lambda': Lambda,
            'Lambda_observed': Lambda_obs,
            'rho_Lambda': rho_Lambda,
            'rho_Lambda_observed': rho_Lambda_obs,
            'agreement': Lambda/Lambda_obs
        }

    def mass_discrepancy_at_z(self, z_values=None, verbose=True):
        """
        Calculate expected mass discrepancy (DM signal) vs redshift.

        Parameters:
        -----------
        z_values : array-like
            Redshifts to calculate (default: 0, 0.5, 1, 2, 3, 5, 10)
        """
        if z_values is None:
            z_values = [0, 0.5, 1, 2, 3, 5, 10]

        if verbose:
            print("=" * 60)
            print("MASS DISCREPANCY VS REDSHIFT")
            print("=" * 60)
            print("(Higher a₀ → stronger MOND → larger 'dark matter' signal)")
            print()
            print(f"{'z':<8} {'a₀(z)/a₀(0)':<15} {'Expected M_dyn/M_bar':<20}")
            print("-" * 43)

            for z in z_values:
                ratio = self.a0_at_redshift(z) / self.a0
                # In deep MOND, mass discrepancy scales as √(a₀)
                # Actually more complex, but rough estimate
                discrepancy = ratio**0.5  # Approximate scaling
                print(f"{z:<8} {ratio:<15.2f} ~{discrepancy:.1f}× (approximate)")
            print()

    def tully_fisher_evolution(self, M_bar=1e10, z_values=None, verbose=True):
        """
        Predict Baryonic Tully-Fisher evolution with redshift.

        Parameters:
        -----------
        M_bar : float
            Reference baryonic mass in M☉
        z_values : array-like
            Redshifts to calculate
        """
        if z_values is None:
            z_values = [0, 0.5, 1, 2, 3]

        if verbose:
            print("=" * 60)
            print("TULLY-FISHER EVOLUTION")
            print("=" * 60)
            print(f"Reference mass: M_bar = {M_bar:.1e} M☉")
            print()
            print(f"{'z':<8} {'a₀(z)/a₀(0)':<15} {'v_flat (km/s)':<15} {'Δlog(M) dex':<15}")
            print("-" * 53)

            v_z0 = self.galaxy_rotation(M_bar, z=0, verbose=False)['v_flat']

            for z in z_values:
                result = self.galaxy_rotation(M_bar, z=z, verbose=False)
                ratio = self.a0_at_redshift(z) / self.a0
                # BTF: M ∝ v⁴/a₀, so at fixed v, inferred M changes
                delta_log_M = -0.25 * np.log10(ratio) * 4  # = -log10(ratio)
                print(f"{z:<8} {ratio:<15.2f} {result['v_flat']:<15.1f} {delta_log_M:<+15.2f}")
            print()
            print("Interpretation: At fixed v_obs, inferred baryonic mass is LOWER at high-z")
            print("because a₀ was higher → more MOND boost per unit mass")
            print()


def main():
    """Interactive calculator."""
    print()
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║         ZIMMERMAN FORMULA CALCULATOR                        ║")
    print("║         a₀ = cH₀/5.79 = c√(Gρc)/2                           ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print()

    # Initialize with standard cosmology
    calc = ZimmermanCalculator(H0=67.4)

    # Print basics
    calc.print_basics()

    # Example calculations
    print("\n" + "=" * 60)
    print("EXAMPLE CALCULATIONS")
    print("=" * 60 + "\n")

    # 1. Milky Way
    print("1. MILKY WAY (M_bar = 6×10¹⁰ M☉)")
    calc.galaxy_rotation(M_bar=6e10, z=0)

    # 2. Dwarf galaxy
    print("2. DWARF GALAXY (M_bar = 10⁸ M☉)")
    calc.galaxy_rotation(M_bar=1e8, z=0)

    # 3. High-z galaxy
    print("3. HIGH-Z GALAXY (M_bar = 10¹⁰ M☉ at z=2)")
    calc.galaxy_rotation(M_bar=1e10, z=2)

    # 4. Derive H₀ from a₀
    print("4. H₀ FROM MOND MEASUREMENT")
    calc.hubble_from_a0(a0_measured=1.2e-10)

    # 5. Cosmological constant
    print("5. COSMOLOGICAL CONSTANT")
    calc.cosmological_constant()

    # 6. Mass discrepancy evolution
    print("6. MASS DISCREPANCY VS REDSHIFT")
    calc.mass_discrepancy_at_z()

    # 7. Tully-Fisher evolution
    print("7. TULLY-FISHER EVOLUTION")
    calc.tully_fisher_evolution()

    print("=" * 60)
    print("END OF DEMONSTRATION")
    print("=" * 60)
    print()
    print("For custom calculations, import this module:")
    print("  from zimmerman_calculator import ZimmermanCalculator")
    print("  calc = ZimmermanCalculator(H0=71.5)")
    print("  calc.galaxy_rotation(M_bar=1e11, z=0.5)")
    print()


if __name__ == "__main__":
    main()
