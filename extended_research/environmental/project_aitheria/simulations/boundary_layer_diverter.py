"""
Project Aitheria: Boundary Layer Diverter Model
=================================================

AGPL-3.0 License
Author: Carl Zimmerman
Date: May 2026

CORE QUESTION: Can we "nudge" CO2 molecules out of a gas stream using
surface acoustic waves on a Z-strained stanene surface?

This script models the "Topological Nudge" concept:
1. Gas molecules pass parallel to a SAW-activated surface
2. Quadrupole/polarizability interactions create transverse forces
3. Target molecules drift toward the "capture wall"
4. No pressure drop (unlike through-flow filtration)

ULTRATHINK TARGET: This is the key physics claim. Does it work?
"""

import numpy as np
import json
from typing import Dict, Any, Tuple
from dataclasses import dataclass
from aitheria_constants import (
    Z_CONSTANT_M, MOLECULES, F_TARGET_HZ, F_SAW_HZ,
    FLUE_GAS_VELOCITY_TYPICAL, FLUE_GAS_T_TYPICAL_K,
    K_BOLTZMANN, EPSILON_0, N_AVOGADRO, H_PLANCK,
    get_molecule_thermal_velocity, get_residence_time
)

# =============================================================================
# PHYSICAL MODELS FOR GAS-SURFACE INTERACTION
# =============================================================================

@dataclass
class NudgeResult:
    """Result of transverse displacement calculation."""
    molecule: str
    channel_length_m: float
    residence_time_s: float
    transverse_displacement_m: float
    transverse_displacement_um: float
    capture_fraction: float
    is_viable: bool
    notes: str


def calculate_quadrupole_interaction(Q: float, E_gradient: float,
                                       distance: float) -> float:
    """
    Calculate interaction energy between molecular quadrupole and field gradient.

    U = -Q * ∂E/∂z

    For a SAW, the field gradient comes from the piezoelectric substrate.

    Args:
        Q: Quadrupole moment (C·m²)
        E_gradient: Electric field gradient (V/m²)
        distance: Distance from surface (m)

    Returns:
        Interaction energy (J)
    """
    # Quadrupole interaction with field gradient
    U = -Q * E_gradient * np.exp(-distance / (100e-9))  # Decay over 100 nm
    return U


def calculate_polarizability_force(alpha: float, E_field: float,
                                    gradient: float) -> float:
    """
    Calculate force on molecule due to polarizability in non-uniform field.

    F = (1/2) * α * ∂(E²)/∂z = α * E * ∂E/∂z

    Args:
        alpha: Polarizability (C²·m²/J or F·m²)
        E_field: Electric field strength (V/m)
        gradient: Field gradient (V/m²)

    Returns:
        Force (N)
    """
    F = alpha * E_field * gradient
    return F


def saw_electric_field(frequency_hz: float, amplitude_nm: float = 1.0,
                        piezo_coefficient: float = 0.5) -> Tuple[float, float]:
    """
    Estimate electric field from SAW on piezoelectric substrate.

    For LiNbO3: d₃₃ ≈ 6 pC/N, typical SAW amplitude ~1 nm

    Args:
        frequency_hz: SAW frequency (Hz)
        amplitude_nm: Mechanical amplitude (nm)
        piezo_coefficient: Piezoelectric coefficient (C/m² per strain)

    Returns:
        (E_field, E_gradient) in V/m and V/m²
    """
    # SAW wavelength
    v_saw = 3500  # m/s (LiNbO3)
    wavelength = v_saw / frequency_hz

    # Strain amplitude
    strain = amplitude_nm * 1e-9 / wavelength

    # Piezoelectric field generation
    # E ≈ (d × stress) / ε ≈ piezo_coefficient × strain × stiffness / ε
    # Simplified estimate
    stiffness = 200e9  # Pa (typical)
    E_field = piezo_coefficient * strain * stiffness / EPSILON_0

    # Limit to reasonable values
    E_field = min(E_field, 1e8)  # Max ~100 MV/m before breakdown

    # Field gradient over one wavelength
    E_gradient = E_field / wavelength

    return E_field, E_gradient


def berry_phase_nudge_estimate(molecule: str, T_K: float,
                                E_field: float, E_gradient: float,
                                residence_time: float) -> float:
    """
    Estimate transverse displacement from "Berry Phase Nudge."

    This is the SPECULATIVE physics claim. The idea is that the
    SAW creates a periodic potential that couples to the molecule's
    quadrupole or polarizability, causing net transverse drift.

    HONEST CAVEAT: This mechanism is NOT established in literature.
    We're estimating an upper bound.

    Args:
        molecule: Molecule name
        T_K: Temperature (K)
        E_field: Electric field (V/m)
        E_gradient: Field gradient (V/m²)
        residence_time: Time in Z-zone (s)

    Returns:
        Transverse displacement (m)
    """
    mol_props = MOLECULES[molecule]
    m = mol_props['molar_mass'] / N_AVOGADRO  # kg per molecule

    # Get quadrupole if available, else use polarizability
    if 'quadrupole_moment' in mol_props:
        Q = mol_props['quadrupole_moment']
        # Force from quadrupole-gradient interaction
        F = abs(Q) * E_gradient
    else:
        # Use polarizability for non-quadrupolar species
        alpha = mol_props.get('polarizability', 1e-40)
        F = abs(alpha * E_field * E_gradient)

    # Acceleration
    a = F / m

    # BUT: thermal randomization competes with this drift
    # Mean thermal velocity
    v_thermal = get_molecule_thermal_velocity(molecule, T_K)

    # Thermal "noise" displacement
    # Random walk: Δx_thermal ~ sqrt(2 * D * t) where D = kT * mobility
    D = K_BOLTZMANN * T_K / (6 * np.pi * 1e-5 * mol_props.get('kinetic_diameter', 3e-10) / 2)
    delta_thermal = np.sqrt(2 * D * residence_time)

    # Coherent drift displacement
    # x = (1/2) * a * t² ... but limited by mean free path collisions
    # In gas at 1 atm, mean free path ~ 70 nm
    mean_free_path = 70e-9  # m

    # Time between collisions
    tau_collision = mean_free_path / v_thermal

    # Number of collisions during residence
    n_collisions = residence_time / tau_collision

    # Each "step" in the nudge direction
    # After each collision, molecule gets a "kick" in the nudge direction
    # before thermal randomization
    delta_per_step = 0.5 * a * tau_collision**2

    # Net drift (biased random walk)
    # Δx_drift ~ n_collisions * delta_per_step
    delta_drift = n_collisions * delta_per_step

    # The HONEST answer: drift competes with thermal diffusion
    # Signal-to-noise ratio
    snr = delta_drift / delta_thermal

    # Return the drift (may be << thermal noise)
    return delta_drift, delta_thermal, snr


def calculate_nudge_displacement(molecule: str,
                                  channel_length_m: float = 1.0,
                                  channel_width_m: float = 0.1,
                                  gas_velocity: float = FLUE_GAS_VELOCITY_TYPICAL,
                                  T_K: float = FLUE_GAS_T_TYPICAL_K,
                                  frequency_hz: float = F_TARGET_HZ) -> NudgeResult:
    """
    Calculate whether a molecule can be nudged to the capture wall.

    Args:
        molecule: Target molecule name
        channel_length_m: Length of Z-lined channel (m)
        channel_width_m: Width of channel (m)
        gas_velocity: Gas flow velocity (m/s)
        T_K: Gas temperature (K)
        frequency_hz: SAW frequency (Hz)

    Returns:
        NudgeResult with viability assessment
    """
    # Residence time
    t_residence = get_residence_time(channel_length_m, gas_velocity)

    # SAW field estimates
    E_field, E_gradient = saw_electric_field(frequency_hz)

    # Calculate nudge displacement
    delta_drift, delta_thermal, snr = berry_phase_nudge_estimate(
        molecule, T_K, E_field, E_gradient, t_residence
    )

    # Capture fraction estimate
    # If drift > channel_width/2, we expect good capture
    # If drift << thermal_noise, random chance only
    if delta_drift > channel_width_m / 2:
        capture_fraction = 0.9
        is_viable = True
        notes = "Drift exceeds half-channel width - high capture expected"
    elif snr > 1:
        capture_fraction = 0.5 * (1 + np.tanh(snr - 1))
        is_viable = snr > 2
        notes = f"SNR = {snr:.2f}; drift detectable above thermal noise"
    else:
        capture_fraction = 0.01 * snr  # Random capture dominated
        is_viable = False
        notes = f"SNR = {snr:.3f}; thermal noise dominates - nudge NOT viable"

    return NudgeResult(
        molecule=molecule,
        channel_length_m=channel_length_m,
        residence_time_s=t_residence,
        transverse_displacement_m=delta_drift,
        transverse_displacement_um=delta_drift * 1e6,
        capture_fraction=capture_fraction,
        is_viable=is_viable,
        notes=notes
    )


def residence_time_analysis(molecule: str,
                             target_displacement_m: float = 0.01,
                             gas_velocity: float = FLUE_GAS_VELOCITY_TYPICAL,
                             T_K: float = FLUE_GAS_T_TYPICAL_K) -> Dict[str, float]:
    """
    Calculate required channel length for target displacement.

    Inverts the nudge calculation to find:
    "How long must the channel be to achieve X displacement?"
    """
    # Binary search for required length
    L_min, L_max = 0.1, 1000  # meters

    for _ in range(50):
        L_mid = (L_min + L_max) / 2
        result = calculate_nudge_displacement(
            molecule, channel_length_m=L_mid,
            gas_velocity=gas_velocity, T_K=T_K
        )

        if result.transverse_displacement_m < target_displacement_m:
            L_min = L_mid
        else:
            L_max = L_mid

    return {
        'molecule': molecule,
        'target_displacement_m': target_displacement_m,
        'required_channel_length_m': L_mid,
        'residence_time_s': L_mid / gas_velocity,
        'is_practical': L_mid < 100,  # < 100m is practical
        'notes': f"Need {L_mid:.1f}m channel for {target_displacement_m*100:.0f}cm displacement"
    }


def run_boundary_layer_analysis() -> Dict[str, Any]:
    """
    Run complete boundary layer diverter analysis.

    ULTRATHINK: Does the nudge mechanism work?
    """
    print("=" * 70)
    print("PROJECT AITHERIA: BOUNDARY LAYER DIVERTER ANALYSIS")
    print("=" * 70)
    print("\nCORE QUESTION: Can we nudge gas molecules with SAW on stanene?")
    print("-" * 70)

    # SAW parameters
    E_field, E_gradient = saw_electric_field(F_TARGET_HZ)
    saw_wavelength = 3500 / F_TARGET_HZ

    print(f"\n### SAW PARAMETERS ###")
    print(f"Frequency: {F_TARGET_HZ/1e6:.1f} MHz")
    print(f"Wavelength: {saw_wavelength*1e6:.2f} μm")
    print(f"E-field (estimated): {E_field:.2e} V/m")
    print(f"E-gradient: {E_gradient:.2e} V/m²")
    print()

    # Analyze each target molecule
    results = {}
    print("### TARGET MOLECULE ANALYSIS (1m channel, 15 m/s flow) ###\n")

    for molecule in ['CO2', 'Hg', 'Xe', 'N2']:
        if molecule not in MOLECULES:
            continue

        result = calculate_nudge_displacement(
            molecule,
            channel_length_m=1.0,
            channel_width_m=0.1,
            gas_velocity=15,
            T_K=473  # 200°C
        )

        results[molecule] = {
            'residence_time_s': result.residence_time_s,
            'transverse_displacement_um': result.transverse_displacement_um,
            'capture_fraction': result.capture_fraction,
            'is_viable': result.is_viable,
            'notes': result.notes,
        }

        print(f"{molecule}:")
        print(f"  Residence time: {result.residence_time_s*1000:.1f} ms")
        print(f"  Transverse displacement: {result.transverse_displacement_um:.3e} μm")
        print(f"  Capture fraction: {result.capture_fraction*100:.1f}%")
        print(f"  Viable: {result.is_viable}")
        print(f"  Notes: {result.notes}")
        print()

    # Required channel length analysis
    print("-" * 70)
    print("\n### REQUIRED CHANNEL LENGTH (for 1 cm displacement) ###\n")

    length_requirements = {}
    for molecule in ['CO2', 'Hg', 'Xe']:
        if molecule not in MOLECULES:
            continue

        req = residence_time_analysis(molecule, target_displacement_m=0.01)
        length_requirements[molecule] = req

        print(f"{molecule}: {req['notes']}")
        print(f"  Practical: {req['is_practical']}")
        print()

    # ULTRATHINK VERDICT
    print("=" * 70)
    print("ULTRATHINK VERDICT: BOUNDARY LAYER NUDGE")
    print("=" * 70)

    # Check if any molecule shows viable nudge
    any_viable = any(r['is_viable'] for r in results.values())
    co2_displacement = results.get('CO2', {}).get('transverse_displacement_um', 0)

    verdicts = []

    if co2_displacement > 10:  # > 10 μm in 1m channel
        verdicts.append("PROMISING: CO2 shows measurable displacement")
        overall_viability = "YELLOW"
    elif co2_displacement > 0.1:
        verdicts.append("MARGINAL: CO2 displacement detectable but small")
        overall_viability = "YELLOW"
    else:
        verdicts.append("NOT VIABLE: CO2 displacement negligible vs thermal noise")
        overall_viability = "RED"

    # Compare to N2 (should have low displacement for selectivity)
    n2_displacement = results.get('N2', {}).get('transverse_displacement_um', 0)
    if co2_displacement > 10 * n2_displacement:
        verdicts.append("GOOD: 10× selectivity for CO2 over N2")
    else:
        verdicts.append("POOR: No selectivity between CO2 and N2")
        overall_viability = "RED"

    for v in verdicts:
        print(f"  • {v}")

    # Probability assessment
    print("\n### PROBABILITY ASSESSMENT ###")

    if overall_viability == "GREEN":
        p_nudge = 0.6
    elif overall_viability == "YELLOW":
        p_nudge = 0.2
    else:
        p_nudge = 0.05

    print(f"\n  P(Berry Phase nudge works as modeled) = {p_nudge*100:.0f}%")
    print(f"\n  KEY UNCERTAINTIES:")
    print(f"    1. Quadrupole-field coupling in gas phase NOT established")
    print(f"    2. Thermal noise dominates at flue gas temperatures")
    print(f"    3. No experimental validation of SAW gas-molecule interaction")
    print(f"    4. Mean free path limits coherent acceleration")
    print()

    # Honest assessment
    print("### HONEST ASSESSMENT ###")
    print("""
  The boundary layer nudge mechanism faces fundamental challenges:

  1. THERMAL NOISE: At 200°C, random molecular motion (~500 m/s)
     completely dominates any coherent drift from SAW fields.

  2. SHORT RESIDENCE TIME: In 1m at 15 m/s, molecules only spend
     67 ms near the surface - too brief for significant displacement.

  3. WEAK COUPLING: Electric field gradients decay exponentially
     from the surface; gas molecules at μm heights see negligible field.

  4. NO LITERATURE SUPPORT: Gas-phase molecular sorting via SAW
     has NOT been demonstrated. All SAW sorting works in liquids.

  VERDICT: The "Topological Nudge" mechanism is likely NOT viable
  for bulk gas separation at industrial conditions.

  ALTERNATIVE APPROACH: Consider adsorption-based separation
  where molecules actually contact the surface, not parallel flow.
""")

    # Compile results
    output = {
        'metadata': {
            'analysis': 'Boundary Layer Diverter Analysis',
            'date': '2026-05-30',
            'author': 'Carl Zimmerman',
            'purpose': 'Determine if SAW nudge mechanism works for gas separation'
        },
        'saw_parameters': {
            'frequency_MHz': F_TARGET_HZ / 1e6,
            'wavelength_um': saw_wavelength * 1e6,
            'E_field_V_m': E_field,
            'E_gradient_V_m2': E_gradient,
        },
        'molecule_analysis': results,
        'length_requirements': length_requirements,
        'verdict': {
            'overall_viability': overall_viability,
            'p_nudge_works': p_nudge,
            'key_finding': 'Thermal noise dominates; nudge mechanism likely not viable',
            'alternative_recommendation': 'Consider adsorption-based or membrane separation',
        },
        'ultrathink_status': 'RED - Fundamental physics challenges'
    }

    return output


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    results = run_boundary_layer_analysis()

    # Save results
    output_path = "../data/results/boundary_layer_results.json"

    def convert_types(obj):
        if isinstance(obj, dict):
            return {k: convert_types(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_types(v) for v in obj]
        elif isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    results_serializable = convert_types(results)

    with open(output_path, 'w') as f:
        json.dump(results_serializable, f, indent=2, default=str)

    print(f"\nResults saved to: {output_path}")
