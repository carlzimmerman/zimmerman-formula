#!/usr/bin/env python3
"""
analysis_mitochondrial_stark.py - Stark Effect on Z² Constant in Mitochondria

Calculates the electric field perturbation of the Z² biological constant
within the inner mitochondrial membrane environment.

Physics Background:
- Peter Mitchell (1961): Chemiosmotic theory, ~150 mV proton motive force
- Inner mitochondrial membrane: ~5-7 nm thick
- Electric field: ~150 mV / 5 nm = 30 MV/m (one of strongest in biology)

The Stark Effect describes how electric fields perturb:
1. Electronic energy levels (spectral shifts)
2. Molecular polarizability (electron cloud distortion)
3. Optimal interaction distances (geometry shifts)

Question: Does the Z² constant need adjustment from 6.015 Å to ~5.98 Å
to compensate for the mitochondrial electric field?

Author: Carl Zimmerman
License: AGPL-3.0-or-later
"""

import math
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import Dict, Tuple


# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

# Fundamental constants (SI units)
ELECTRON_CHARGE = 1.602176634e-19  # C (coulombs)
VACUUM_PERMITTIVITY = 8.8541878128e-12  # F/m (farads per meter)
BOLTZMANN = 1.380649e-23  # J/K
PLANCK = 6.62607015e-34  # J·s
BOHR_RADIUS = 5.29177210903e-11  # m (0.529 Å)
ANGSTROM = 1e-10  # m

# Z² Constants
Z2_VACUUM = 5.788810036466141  # Å
Z2_BIOLOGICAL = 6.015152508891966  # Å
Z2_SCALING_FACTOR = 1.0391  # Biological/Vacuum ratio

# Temperature
PHYSIOLOGICAL_TEMP = 310.15  # K (37°C)
MITOCHONDRIAL_TEMP = 323.15  # K (~50°C, mitochondria run hot)


# =============================================================================
# MITOCHONDRIAL MEMBRANE PARAMETERS
# =============================================================================

@dataclass
class MitochondrialMembrane:
    """Inner mitochondrial membrane properties."""

    # Membrane potential (Peter Mitchell, 1961)
    potential_mV: float = 150.0  # mV (typical range: 140-180 mV)

    # Membrane thickness
    thickness_nm: float = 5.0  # nm (phospholipid bilayer)

    # Dielectric properties
    membrane_dielectric: float = 2.0  # Low dielectric in lipid core
    interface_dielectric: float = 20.0  # Higher at water interface
    water_dielectric: float = 80.0  # Bulk water

    # pH gradient (ΔpH)
    delta_pH: float = 0.5  # Matrix more alkaline

    def electric_field(self) -> float:
        """Calculate electric field in V/m."""
        voltage = self.potential_mV * 1e-3  # Convert to V
        thickness = self.thickness_nm * 1e-9  # Convert to m
        return voltage / thickness

    def electric_field_MV_per_m(self) -> float:
        """Electric field in MV/m (more intuitive units)."""
        return self.electric_field() / 1e6

    def proton_motive_force(self) -> float:
        """
        Total proton motive force (Δp) in mV.
        Δp = Δψ + (2.303 RT/F) × ΔpH
        """
        RT_over_F = (8.314 * PHYSIOLOGICAL_TEMP) / 96485  # ~0.0267 V at 37°C
        pH_contribution = 2.303 * RT_over_F * 1000 * self.delta_pH  # mV
        return self.potential_mV + pH_contribution


# =============================================================================
# TRYPTOPHAN POLARIZABILITY
# =============================================================================

@dataclass
class TryptophanElectronics:
    """Electronic properties of tryptophan indole ring."""

    # Polarizability tensor (approximate, from literature)
    # Units: Å³ (volume polarizability)
    alpha_parallel: float = 25.0  # Along indole plane
    alpha_perpendicular: float = 12.0  # Perpendicular to plane

    # Dipole moment
    permanent_dipole_D: float = 2.1  # Debye

    # Ionization potential
    ionization_eV: float = 7.9  # eV

    # π-electron delocalization length
    pi_length_A: float = 5.5  # Å (indole conjugation extent)

    def mean_polarizability(self) -> float:
        """Isotropic polarizability in Å³."""
        return (2 * self.alpha_parallel + self.alpha_perpendicular) / 3

    def polarizability_SI(self) -> float:
        """Convert to SI units (C²·m²/J)."""
        # α(SI) = 4πε₀ × α(Å³) × 10⁻³⁰
        return 4 * math.pi * VACUUM_PERMITTIVITY * self.mean_polarizability() * 1e-30

    def dipole_SI(self) -> float:
        """Dipole moment in C·m."""
        # 1 Debye = 3.336e-30 C·m
        return self.permanent_dipole_D * 3.336e-30


# =============================================================================
# STARK EFFECT CALCULATIONS
# =============================================================================

def calculate_stark_shift(
    electric_field: float,  # V/m
    polarizability: float,  # C²·m²/J
    dipole: float,  # C·m
    alignment_cos: float = 0.5  # Average orientation
) -> Dict[str, float]:
    """
    Calculate Stark effect energy and geometry shifts.

    The Stark effect has two contributions:
    1. Linear Stark: ΔE = -μ·E·cos(θ) (permanent dipole)
    2. Quadratic Stark: ΔE = -½α·E² (induced dipole)

    For aromatic stacking, the quadratic term dominates geometry shifts.
    """

    # Linear Stark effect (dipole alignment)
    linear_stark_J = -dipole * electric_field * alignment_cos
    linear_stark_meV = linear_stark_J / ELECTRON_CHARGE * 1000

    # Quadratic Stark effect (polarization)
    quadratic_stark_J = -0.5 * polarizability * electric_field**2
    quadratic_stark_meV = quadratic_stark_J / ELECTRON_CHARGE * 1000

    # Total energy shift
    total_stark_J = linear_stark_J + quadratic_stark_J
    total_stark_meV = total_stark_J / ELECTRON_CHARGE * 1000

    # Compare to thermal energy
    thermal_energy_J = BOLTZMANN * PHYSIOLOGICAL_TEMP
    thermal_energy_meV = thermal_energy_J / ELECTRON_CHARGE * 1000

    stark_to_thermal_ratio = abs(total_stark_J) / thermal_energy_J

    return {
        'linear_stark_meV': linear_stark_meV,
        'quadratic_stark_meV': quadratic_stark_meV,
        'total_stark_meV': total_stark_meV,
        'thermal_energy_meV': thermal_energy_meV,
        'stark_to_thermal_ratio': stark_to_thermal_ratio,
    }


def calculate_geometry_shift(
    electric_field: float,  # V/m
    polarizability: float,  # C²·m²/J
    base_distance: float,  # Å
) -> Dict[str, float]:
    """
    Calculate how the optimal aromatic stacking distance shifts under E-field.

    The polarization energy creates an effective force:
    F = -dU/dr = α·E²·(1/r)

    This compresses or expands the optimal distance depending on field orientation.

    For parallel field (along stacking axis): compression
    For perpendicular field: expansion
    """

    # Polarization energy at base distance
    U_base = -0.5 * polarizability * electric_field**2

    # Force constant for aromatic stacking (approximate)
    # From π-π interaction potential: k ≈ 0.1 N/m typical
    k_stacking = 0.1  # N/m

    # Field-induced displacement
    # F = α·E² / r ≈ displacement × k
    # δr = α·E² / (r × k)

    r_m = base_distance * ANGSTROM  # Convert to meters
    force_polarization = polarizability * electric_field**2 / r_m

    displacement_m = force_polarization / k_stacking
    displacement_A = displacement_m / ANGSTROM

    # Sign convention: negative = compression, positive = expansion
    # For parallel E-field, electron clouds compress toward field source

    # New optimal distance
    new_distance = base_distance - displacement_A  # Compression case

    # Percentage shift
    percent_shift = (new_distance - base_distance) / base_distance * 100

    return {
        'base_distance_A': base_distance,
        'displacement_A': displacement_A,
        'new_distance_A': new_distance,
        'percent_shift': percent_shift,
        'force_pN': force_polarization * 1e12,  # picoNewtons
    }


def calculate_electron_cloud_stability(
    electric_field: float,  # V/m
    ionization_eV: float,
    pi_length: float,  # Å
) -> Dict[str, float]:
    """
    Assess whether the Trp electron cloud remains stable in the E-field.

    Stability criterion:
    - If field energy << ionization energy: stable
    - If field energy approaches ionization: electron tunneling possible

    Field ionization threshold: E_crit = I² / (4·e³) for hydrogen-like
    For conjugated systems, threshold is lower due to delocalization.
    """

    # Energy gained by electron traversing π-system
    # ΔE = e × E × L_π
    pi_length_m = pi_length * ANGSTROM
    field_energy_J = ELECTRON_CHARGE * electric_field * pi_length_m
    field_energy_eV = field_energy_J / ELECTRON_CHARGE

    # Compare to ionization potential
    ionization_J = ionization_eV * ELECTRON_CHARGE
    stability_ratio = field_energy_eV / ionization_eV

    # Critical field for ionization (simplified)
    # For aromatic systems, ~10 V/nm causes significant perturbation
    critical_field = ionization_J / (ELECTRON_CHARGE * pi_length_m)
    critical_field_MV_m = critical_field / 1e6

    # Stability assessment
    if stability_ratio < 0.01:
        stability = "HIGHLY STABLE"
        recommendation = "No Z² adjustment needed"
    elif stability_ratio < 0.05:
        stability = "STABLE"
        recommendation = "Minor Z² adjustment may improve precision"
    elif stability_ratio < 0.1:
        stability = "MODERATELY STABLE"
        recommendation = "Consider Z² adjustment of 0.02-0.05 Å"
    else:
        stability = "PERTURBED"
        recommendation = "Z² adjustment required for mitochondrial targets"

    return {
        'field_energy_eV': field_energy_eV,
        'ionization_eV': ionization_eV,
        'stability_ratio': stability_ratio,
        'critical_field_MV_m': critical_field_MV_m,
        'stability': stability,
        'recommendation': recommendation,
    }


# =============================================================================
# Z² MITOCHONDRIAL CORRECTION
# =============================================================================

def calculate_z2_mitochondrial_correction(
    membrane: MitochondrialMembrane,
    trp: TryptophanElectronics,
) -> Dict[str, any]:
    """
    Calculate the corrected Z² constant for mitochondrial membrane environment.

    This integrates:
    1. Stark effect geometry shift
    2. Dielectric environment change
    3. Temperature correction (mitochondria are ~50°C)
    4. Electron cloud stability assessment
    """

    results = {}

    # Basic membrane properties
    E_field = membrane.electric_field()
    E_field_MV = membrane.electric_field_MV_per_m()
    pmf = membrane.proton_motive_force()

    results['membrane'] = {
        'potential_mV': membrane.potential_mV,
        'thickness_nm': membrane.thickness_nm,
        'electric_field_MV_m': E_field_MV,
        'proton_motive_force_mV': pmf,
    }

    # Tryptophan properties
    alpha_SI = trp.polarizability_SI()
    dipole_SI = trp.dipole_SI()

    results['tryptophan'] = {
        'polarizability_A3': trp.mean_polarizability(),
        'dipole_Debye': trp.permanent_dipole_D,
        'ionization_eV': trp.ionization_eV,
        'pi_length_A': trp.pi_length_A,
    }

    # Stark effect
    stark = calculate_stark_shift(E_field, alpha_SI, dipole_SI)
    results['stark_effect'] = stark

    # Geometry shift
    geometry = calculate_geometry_shift(E_field, alpha_SI, Z2_BIOLOGICAL)
    results['geometry_shift'] = geometry

    # Electron cloud stability
    stability = calculate_electron_cloud_stability(
        E_field, trp.ionization_eV, trp.pi_length_A
    )
    results['stability'] = stability

    # Dielectric correction
    # In lower dielectric, electrostatic interactions are stronger
    # Distance scales as ε^(-1/3) for charge-charge, ε^(-1/6) for dispersion
    dielectric_ratio = membrane.interface_dielectric / membrane.water_dielectric
    dielectric_correction_A = Z2_BIOLOGICAL * (dielectric_ratio**(1/6) - 1)

    results['dielectric_correction'] = {
        'membrane_dielectric': membrane.interface_dielectric,
        'water_dielectric': membrane.water_dielectric,
        'dielectric_ratio': dielectric_ratio,
        'correction_A': dielectric_correction_A,
    }

    # Temperature correction
    # Higher T increases entropic breathing
    temp_ratio = MITOCHONDRIAL_TEMP / PHYSIOLOGICAL_TEMP
    thermal_expansion_A = 0.08 * (temp_ratio - 1)  # ~0.08 Å per 37°C

    results['temperature_correction'] = {
        'physiological_K': PHYSIOLOGICAL_TEMP,
        'mitochondrial_K': MITOCHONDRIAL_TEMP,
        'temp_ratio': temp_ratio,
        'thermal_expansion_A': thermal_expansion_A,
    }

    # Total Z² correction
    stark_correction = geometry['displacement_A']
    total_correction = stark_correction + dielectric_correction_A + thermal_expansion_A

    z2_mitochondrial = Z2_BIOLOGICAL + total_correction

    results['z2_correction'] = {
        'z2_vacuum': Z2_VACUUM,
        'z2_biological': Z2_BIOLOGICAL,
        'stark_correction_A': stark_correction,
        'dielectric_correction_A': dielectric_correction_A,
        'thermal_correction_A': thermal_expansion_A,
        'total_correction_A': total_correction,
        'z2_mitochondrial': z2_mitochondrial,
    }

    # Final recommendation
    if abs(total_correction) < 0.02:
        recommendation = f"Z² = {Z2_BIOLOGICAL:.3f} Å remains valid for mitochondrial targets"
    elif total_correction < 0:
        recommendation = f"Shorten Z² to {z2_mitochondrial:.3f} Å for mitochondrial targets"
    else:
        recommendation = f"Extend Z² to {z2_mitochondrial:.3f} Å for mitochondrial targets"

    results['recommendation'] = recommendation

    return results


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_mitochondrial_stark_analysis():
    """Run complete Stark effect analysis for mitochondrial Z² correction."""

    print("=" * 80)
    print("MITOCHONDRIAL STARK EFFECT ANALYSIS")
    print("Z² Constant Correction for Proton Motive Force Environment")
    print("=" * 80)
    print()
    print("Reference: Peter Mitchell (1961) - Chemiosmotic Theory")
    print(f"Z² Biological Constant: {Z2_BIOLOGICAL:.6f} Å")
    print()

    # Initialize components
    membrane = MitochondrialMembrane()
    trp = TryptophanElectronics()

    # Run analysis
    results = calculate_z2_mitochondrial_correction(membrane, trp)

    # Print results
    print("-" * 80)
    print("INNER MITOCHONDRIAL MEMBRANE PROPERTIES")
    print("-" * 80)
    m = results['membrane']
    print(f"    Membrane potential (Δψ): {m['potential_mV']:.1f} mV")
    print(f"    Membrane thickness: {m['thickness_nm']:.1f} nm")
    print(f"    Electric field: {m['electric_field_MV_m']:.1f} MV/m")
    print(f"    Proton motive force (Δp): {m['proton_motive_force_mV']:.1f} mV")
    print()

    print("-" * 80)
    print("TRYPTOPHAN ELECTRONIC PROPERTIES")
    print("-" * 80)
    t = results['tryptophan']
    print(f"    Mean polarizability: {t['polarizability_A3']:.1f} Å³")
    print(f"    Permanent dipole: {t['dipole_Debye']:.1f} Debye")
    print(f"    Ionization potential: {t['ionization_eV']:.1f} eV")
    print(f"    π-electron length: {t['pi_length_A']:.1f} Å")
    print()

    print("-" * 80)
    print("STARK EFFECT ANALYSIS")
    print("-" * 80)
    s = results['stark_effect']
    print(f"    Linear Stark shift: {s['linear_stark_meV']:.4f} meV")
    print(f"    Quadratic Stark shift: {s['quadratic_stark_meV']:.4f} meV")
    print(f"    Total Stark shift: {s['total_stark_meV']:.4f} meV")
    print(f"    Thermal energy (kT): {s['thermal_energy_meV']:.2f} meV")
    print(f"    Stark/Thermal ratio: {s['stark_to_thermal_ratio']:.4f}")
    print()

    print("-" * 80)
    print("GEOMETRY SHIFT UNDER ELECTRIC FIELD")
    print("-" * 80)
    g = results['geometry_shift']
    print(f"    Base Z² distance: {g['base_distance_A']:.6f} Å")
    print(f"    Field-induced displacement: {g['displacement_A']:.6f} Å")
    print(f"    New optimal distance: {g['new_distance_A']:.6f} Å")
    print(f"    Percentage shift: {g['percent_shift']:.4f}%")
    print(f"    Polarization force: {g['force_pN']:.2f} pN")
    print()

    print("-" * 80)
    print("ELECTRON CLOUD STABILITY")
    print("-" * 80)
    st = results['stability']
    print(f"    Field energy across π-system: {st['field_energy_eV']:.4f} eV")
    print(f"    Ionization potential: {st['ionization_eV']:.1f} eV")
    print(f"    Stability ratio: {st['stability_ratio']:.4f}")
    print(f"    Critical field for ionization: {st['critical_field_MV_m']:.1f} MV/m")
    print(f"    Assessment: {st['stability']}")
    print(f"    → {st['recommendation']}")
    print()

    print("-" * 80)
    print("DIELECTRIC ENVIRONMENT CORRECTION")
    print("-" * 80)
    d = results['dielectric_correction']
    print(f"    Membrane interface ε: {d['membrane_dielectric']:.1f}")
    print(f"    Bulk water ε: {d['water_dielectric']:.1f}")
    print(f"    Dielectric ratio: {d['dielectric_ratio']:.3f}")
    print(f"    Distance correction: {d['correction_A']:.6f} Å")
    print()

    print("-" * 80)
    print("TEMPERATURE CORRECTION (Mitochondria run hot)")
    print("-" * 80)
    tc = results['temperature_correction']
    print(f"    Physiological: {tc['physiological_K']:.1f} K ({tc['physiological_K']-273.15:.1f}°C)")
    print(f"    Mitochondrial: {tc['mitochondrial_K']:.1f} K ({tc['mitochondrial_K']-273.15:.1f}°C)")
    print(f"    Thermal expansion: {tc['thermal_expansion_A']:.6f} Å")
    print()

    print("=" * 80)
    print("Z² MITOCHONDRIAL CORRECTION SUMMARY")
    print("=" * 80)
    z = results['z2_correction']
    print(f"""
    Z² Vacuum:              {z['z2_vacuum']:.6f} Å
    Z² Biological (37°C):   {z['z2_biological']:.6f} Å

    Corrections:
      Stark effect:         {z['stark_correction_A']:+.6f} Å
      Dielectric:           {z['dielectric_correction_A']:+.6f} Å
      Temperature:          {z['thermal_correction_A']:+.6f} Å
      ─────────────────────────────────
      TOTAL:                {z['total_correction_A']:+.6f} Å

    Z² MITOCHONDRIAL:       {z['z2_mitochondrial']:.6f} Å
    """)

    print("=" * 80)
    print("RECOMMENDATION")
    print("=" * 80)
    print(f"    {results['recommendation']}")
    print()

    # Stability verdict
    if results['stability']['stability_ratio'] < 0.05:
        print("    ✓ Tryptophan electron cloud REMAINS STABLE in mitochondrial E-field")
        print("    ✓ Z² aromatic anchors will function correctly")
        print(f"    ✓ Design distance adjustment: {z['total_correction_A']*1000:.1f} milliAngstroms")
    else:
        print("    ⚠ Significant electron cloud perturbation detected")
        print("    ⚠ Consider alternative anchor residues for mitochondrial targets")

    print("=" * 80)

    # Save results
    output_dir = Path("../mitochondrial_analysis")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "stark_effect_analysis.json"

    # Convert to JSON-serializable format
    json_results = {
        'timestamp': datetime.now().isoformat(),
        'reference': 'Peter Mitchell (1961) - Chemiosmotic Theory',
        'membrane': results['membrane'],
        'tryptophan': results['tryptophan'],
        'stark_effect': results['stark_effect'],
        'geometry_shift': results['geometry_shift'],
        'stability': results['stability'],
        'dielectric_correction': results['dielectric_correction'],
        'temperature_correction': results['temperature_correction'],
        'z2_correction': results['z2_correction'],
        'recommendation': results['recommendation'],
    }

    with open(output_file, 'w') as f:
        json.dump(json_results, f, indent=2)

    print(f"\n    Saved: {output_file}")

    return results


# =============================================================================
# ADDITIONAL ANALYSIS: Electron Transport Chain Proximity
# =============================================================================

def analyze_etc_proximity():
    """
    Analyze Z² stability near Electron Transport Chain complexes.

    The ETC generates local electric fields much stronger than the
    bulk membrane potential due to electron tunneling events.
    """

    print("\n" + "=" * 80)
    print("ELECTRON TRANSPORT CHAIN PROXIMITY ANALYSIS")
    print("=" * 80)

    # ETC complex local fields (approximate)
    etc_complexes = {
        'Complex I (NADH-CoQ)': {'field_MV_m': 50, 'distance_nm': 2},
        'Complex III (CoQ-Cyt c)': {'field_MV_m': 40, 'distance_nm': 3},
        'Complex IV (Cyt c oxidase)': {'field_MV_m': 60, 'distance_nm': 1.5},
        'ATP Synthase (F₀F₁)': {'field_MV_m': 35, 'distance_nm': 4},
    }

    trp = TryptophanElectronics()
    alpha_SI = trp.polarizability_SI()

    print("\n    Complex-specific Z² corrections:\n")

    for complex_name, props in etc_complexes.items():
        E_field = props['field_MV_m'] * 1e6  # Convert to V/m

        geometry = calculate_geometry_shift(E_field, alpha_SI, Z2_BIOLOGICAL)

        z2_local = Z2_BIOLOGICAL + geometry['displacement_A']

        print(f"    {complex_name}:")
        print(f"      Local field: {props['field_MV_m']} MV/m at {props['distance_nm']} nm")
        print(f"      Z² shift: {geometry['displacement_A']*1000:+.2f} mÅ")
        print(f"      Z² local: {z2_local:.4f} Å")
        print()

    print("    Note: These are proximity effects. At >5 nm from ETC complexes,")
    print("    the bulk membrane correction applies.")


# =============================================================================
# CLI
# =============================================================================

if __name__ == '__main__':
    results = run_mitochondrial_stark_analysis()
    analyze_etc_proximity()
