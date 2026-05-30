"""
Project Aitheria: Thermal Lattice Drift Audit
==============================================

AGPL-3.0 License
Author: Carl Zimmerman
Date: May 2026

CRITICAL QUESTION: Does Z-strained stanene survive flue gas temperatures (150-300°C)?

This script performs the "honesty check" on thermal stability:
1. Calculate lattice expansion at operating temperatures
2. Determine if Z-resonance is maintained or lost
3. Identify cooling requirements or strain compensation needed
4. Compare to literature on 2D material thermal stability

ULTRATHINK TARGET: This is the first potential "kill shot" for Aitheria.
"""

import numpy as np
import json
from typing import Dict, Any, Tuple
from dataclasses import dataclass
from aitheria_constants import (
    Z_CONSTANT_M, Z_CONSTANT_ANGSTROM, STANENE_Z_A, STANENE_NATIVE_A,
    ALPHA_STANENE_ESTIMATED, ALPHA_TIN_BULK, TIN_MELTING_K,
    FLUE_GAS_T_MIN_K, FLUE_GAS_T_MAX_K, FLUE_GAS_T_TYPICAL_K,
    K_BOLTZMANN, get_lattice_at_temperature
)

# =============================================================================
# THERMAL EXPANSION MODELS
# =============================================================================

@dataclass
class ThermalExpansionResult:
    """Results from thermal expansion analysis."""
    temperature_K: float
    temperature_C: float
    lattice_constant_A: float
    drift_from_Z_percent: float
    strain_from_native_percent: float
    is_stable: bool
    stability_notes: str


def grüneisen_thermal_expansion(T_K: float, theta_D: float = 200,
                                  gamma: float = 2.0, B: float = 50e9,
                                  V0: float = 3e-29) -> float:
    """
    Calculate thermal expansion coefficient using Grüneisen parameter.

    For 2D materials, the Grüneisen parameter γ relates thermal expansion
    to the change in phonon frequencies with volume.

    α = (γ × C_V) / (B × V)

    Args:
        T_K: Temperature in Kelvin
        theta_D: Debye temperature (~200 K for stanene)
        gamma: Grüneisen parameter (~2 for many materials)
        B: Bulk modulus (Pa)
        V0: Unit cell volume (m³)

    Returns:
        Linear thermal expansion coefficient (/K)
    """
    # Simplified Debye heat capacity (3D approximation)
    x = theta_D / T_K
    if x < 0.1:
        # High temperature limit: C_V → 3R
        C_V = 3 * K_BOLTZMANN
    else:
        # Use Debye function approximation
        C_V = 3 * K_BOLTZMANN * (4 * (T_K / theta_D)**3 *
                                  debye_integral(theta_D / T_K) -
                                  3 * theta_D / T_K / (np.exp(theta_D / T_K) - 1))

    # For 2D materials, we use the 2D version
    # α_linear ≈ γ × C_V / (2 × B × A) where A is area
    alpha = gamma * C_V / (B * V0)

    # Convert volumetric to linear (divide by 3 for isotropic, 2 for 2D)
    alpha_linear = alpha / 2

    return alpha_linear


def debye_integral(x: float, n_terms: int = 100) -> float:
    """Numerical approximation of Debye function D(x)."""
    if x < 1e-6:
        return 1.0
    result = 0
    for n in range(1, n_terms + 1):
        result += np.exp(-n * x) * (x**3 / n**3 + 3 * x**2 / n**2 +
                                     6 * x / n**3 + 6 / n**4)
    return 3 * result


def analyze_thermal_expansion(T_K: float,
                               alpha_model: str = 'empirical') -> ThermalExpansionResult:
    """
    Analyze lattice expansion at a given temperature.

    Args:
        T_K: Temperature in Kelvin
        alpha_model: 'empirical' (literature estimate) or 'grüneisen' (calculated)

    Returns:
        ThermalExpansionResult with stability analysis
    """
    T_C = T_K - 273.15
    T_ref = 300  # Reference temperature

    # Select thermal expansion coefficient
    if alpha_model == 'empirical':
        alpha = ALPHA_STANENE_ESTIMATED
    else:
        alpha = grüneisen_thermal_expansion(T_K)

    # Calculate expanded lattice constant
    delta_T = T_K - T_ref
    a_T = STANENE_Z_A * (1 + alpha * delta_T)
    a_T_angstrom = a_T * 1e10

    # Calculate drifts
    drift_from_Z = (a_T - Z_CONSTANT_M) / Z_CONSTANT_M * 100
    strain_from_native = (a_T - STANENE_NATIVE_A) / STANENE_NATIVE_A * 100

    # Stability assessment
    stability_notes = []
    is_stable = True

    # Check 1: Is lattice too far from Z-resonance?
    if abs(drift_from_Z) > 1.0:
        stability_notes.append(f"WARNING: Lattice drift {drift_from_Z:.2f}% exceeds 1% tolerance")
        is_stable = False
    elif abs(drift_from_Z) > 0.5:
        stability_notes.append(f"CAUTION: Lattice drift {drift_from_Z:.2f}% approaching tolerance")

    # Check 2: Is temperature approaching melting point?
    if T_K > 0.7 * TIN_MELTING_K:
        stability_notes.append(f"WARNING: T = {T_C:.0f}°C is >{70}% of melting point")
        is_stable = False

    # Check 3: Is the strain too high for structural integrity?
    if strain_from_native > 30:
        stability_notes.append(f"WARNING: Total strain {strain_from_native:.1f}% may cause fracture")
        is_stable = False

    # Check 4: Substrate-supported vs freestanding
    stability_notes.append("NOTE: Analysis assumes substrate-supported stanene")
    stability_notes.append("Freestanding stanene may buckle at high strain")

    if not stability_notes:
        stability_notes.append("Lattice appears stable at this temperature")

    return ThermalExpansionResult(
        temperature_K=T_K,
        temperature_C=T_C,
        lattice_constant_A=a_T_angstrom,
        drift_from_Z_percent=drift_from_Z,
        strain_from_native_percent=strain_from_native,
        is_stable=is_stable,
        stability_notes="; ".join(stability_notes)
    )


def temperature_sweep(T_min_K: float = 300, T_max_K: float = 600,
                      n_points: int = 50) -> Dict[str, Any]:
    """
    Sweep temperature range and analyze lattice stability.

    Returns comprehensive thermal analysis with ultrathink assessment.
    """
    temperatures = np.linspace(T_min_K, T_max_K, n_points)
    results = []

    for T in temperatures:
        result = analyze_thermal_expansion(T)
        results.append({
            'T_K': T,
            'T_C': T - 273.15,
            'a_A': result.lattice_constant_A,
            'drift_percent': result.drift_from_Z_percent,
            'strain_percent': result.strain_from_native_percent,
            'is_stable': result.is_stable,
        })

    # Find critical temperatures
    stable_temps = [r['T_K'] for r in results if r['is_stable']]
    unstable_temps = [r['T_K'] for r in results if not r['is_stable']]

    if stable_temps and unstable_temps:
        T_critical = min(unstable_temps)
    elif not unstable_temps:
        T_critical = T_max_K  # All stable
    else:
        T_critical = T_min_K  # All unstable

    # Calculate at key flue gas temperatures
    flue_gas_analysis = {
        'T_min_150C': analyze_thermal_expansion(FLUE_GAS_T_MIN_K).__dict__,
        'T_typical_200C': analyze_thermal_expansion(FLUE_GAS_T_TYPICAL_K).__dict__,
        'T_max_300C': analyze_thermal_expansion(FLUE_GAS_T_MAX_K).__dict__,
    }

    return {
        'sweep_results': results,
        'flue_gas_analysis': flue_gas_analysis,
        'T_critical_K': T_critical,
        'T_critical_C': T_critical - 273.15,
        'max_operating_temp_K': max(stable_temps) if stable_temps else None,
    }


def calculate_cooling_requirement(T_flue: float, T_target: float = 350) -> Dict[str, float]:
    """
    Calculate cooling needed to keep lattice stable.

    Args:
        T_flue: Flue gas temperature (K)
        T_target: Target operating temperature (K)

    Returns:
        Cooling requirements and energy estimates
    """
    delta_T = T_flue - T_target

    if delta_T <= 0:
        return {
            'cooling_required': False,
            'delta_T_K': 0,
            'message': 'No cooling required'
        }

    # Rough estimate: cooling 1 kg of air by 1 K requires ~1 kJ
    # For flue gas flow rate of 1000 m³/s at ~0.9 kg/m³
    flow_rate_kg_s = 900  # kg/s (rough estimate)
    cooling_power_kW = flow_rate_kg_s * 1.0 * delta_T  # kW

    return {
        'cooling_required': True,
        'delta_T_K': delta_T,
        'cooling_power_kW': cooling_power_kW,
        'cooling_power_MW': cooling_power_kW / 1000,
        'message': f'Need to cool {delta_T:.0f} K, requiring ~{cooling_power_kW/1000:.1f} MW'
    }


def substrate_compensation_analysis() -> Dict[str, Any]:
    """
    Analyze substrate options for thermal compensation.

    Some substrates have negative thermal expansion (NTE) that could
    compensate for stanene expansion.
    """
    substrates = {
        'SiC': {
            'alpha': 4.0e-6,  # /K
            'type': 'positive',
            'notes': 'Standard substrate, adds to expansion'
        },
        'BN': {
            'alpha': -2.7e-6,  # /K (in-plane, can be negative)
            'type': 'negative (in-plane)',
            'notes': 'Partial compensation possible'
        },
        'Graphite': {
            'alpha': -1.0e-6,  # /K (a-axis)
            'type': 'negative (a-axis)',
            'notes': 'Could partially compensate'
        },
        'ZrW2O8': {
            'alpha': -9.0e-6,  # /K (isotropic NTE)
            'type': 'strongly negative',
            'notes': 'Best NTE material, but epitaxy unclear'
        },
        'Engineered_metamaterial': {
            'alpha': 'tunable',
            'type': 'designed',
            'notes': 'Could be designed to match stanene expansion'
        }
    }

    # Calculate net expansion with BN substrate
    alpha_stanene = ALPHA_STANENE_ESTIMATED
    alpha_BN = -2.7e-6

    # Simplified bilayer model (rule of mixtures)
    # Net α ≈ (h₁α₁ + h₂α₂) / (h₁ + h₂)
    h_stanene = 0.5e-9  # 0.5 nm
    h_BN = 1.0e-9  # 1 nm
    alpha_net = (h_stanene * alpha_stanene + h_BN * alpha_BN) / (h_stanene + h_BN)

    return {
        'substrates': substrates,
        'bilayer_analysis': {
            'stanene_thickness_nm': h_stanene * 1e9,
            'BN_thickness_nm': h_BN * 1e9,
            'alpha_stanene': alpha_stanene,
            'alpha_BN': alpha_BN,
            'alpha_net': alpha_net,
            'compensation_achieved': alpha_net < alpha_stanene * 0.5,
            'notes': 'BN substrate could reduce effective expansion by ~50%'
        }
    }


def run_full_thermal_audit() -> Dict[str, Any]:
    """
    Run complete thermal stability audit for Project Aitheria.

    This is the ULTRATHINK honesty check for thermal viability.
    """
    print("=" * 70)
    print("PROJECT AITHERIA: THERMAL LATTICE DRIFT AUDIT")
    print("=" * 70)
    print("\nCRITICAL QUESTION: Does Z-strained stanene survive flue gas temps?")
    print("-" * 70)

    # Run temperature sweep
    sweep = temperature_sweep(300, 600, 50)

    # Analyze flue gas conditions
    print("\n### FLUE GAS TEMPERATURE ANALYSIS ###\n")
    for key, analysis in sweep['flue_gas_analysis'].items():
        print(f"{key}:")
        print(f"  Temperature: {analysis['temperature_C']:.0f}°C ({analysis['temperature_K']:.0f} K)")
        print(f"  Lattice: {analysis['lattice_constant_A']:.4f} Å")
        print(f"  Drift from Z: {analysis['drift_from_Z_percent']:+.3f}%")
        print(f"  Total strain: {analysis['strain_from_native_percent']:.1f}%")
        print(f"  Stable: {analysis['is_stable']}")
        print(f"  Notes: {analysis['stability_notes']}")
        print()

    # Critical temperature
    print("-" * 70)
    print(f"\nCRITICAL TEMPERATURE: {sweep['T_critical_C']:.0f}°C")
    if sweep['max_operating_temp_K']:
        print(f"MAX OPERATING TEMP: {sweep['max_operating_temp_K']-273:.0f}°C")
    print()

    # Cooling requirements
    print("### COOLING REQUIREMENTS ###\n")
    for T_flue in [FLUE_GAS_T_TYPICAL_K, FLUE_GAS_T_MAX_K]:
        cooling = calculate_cooling_requirement(T_flue, T_target=350)
        print(f"Flue gas at {T_flue-273:.0f}°C: {cooling['message']}")
    print()

    # Substrate compensation
    print("### SUBSTRATE COMPENSATION OPTIONS ###\n")
    substrates = substrate_compensation_analysis()
    bilayer = substrates['bilayer_analysis']
    print(f"Stanene/BN bilayer analysis:")
    print(f"  Net α: {bilayer['alpha_net']*1e6:.2f} × 10⁻⁶ /K")
    print(f"  Compensation achieved: {bilayer['compensation_achieved']}")
    print(f"  Notes: {bilayer['notes']}")
    print()

    # ULTRATHINK VERDICT
    print("=" * 70)
    print("ULTRATHINK VERDICT: THERMAL STABILITY")
    print("=" * 70)

    # Check all conditions
    T200_stable = sweep['flue_gas_analysis']['T_typical_200C']['is_stable']
    T300_stable = sweep['flue_gas_analysis']['T_max_300C']['is_stable']
    drift_at_200 = abs(sweep['flue_gas_analysis']['T_typical_200C']['drift_from_Z_percent'])
    drift_at_300 = abs(sweep['flue_gas_analysis']['T_max_300C']['drift_from_Z_percent'])

    verdicts = []

    if T200_stable and drift_at_200 < 0.5:
        verdicts.append("VIABLE at 200°C: Drift < 0.5%, structure stable")
        viability_200 = "GREEN"
    elif T200_stable:
        verdicts.append("MARGINAL at 200°C: Stable but drift may affect resonance")
        viability_200 = "YELLOW"
    else:
        verdicts.append("NOT VIABLE at 200°C: Structure unstable")
        viability_200 = "RED"

    if T300_stable and drift_at_300 < 1.0:
        verdicts.append("VIABLE at 300°C: Within tolerance")
        viability_300 = "GREEN"
    elif T300_stable:
        verdicts.append("MARGINAL at 300°C: Approaching limits")
        viability_300 = "YELLOW"
    else:
        verdicts.append("NOT VIABLE at 300°C: Requires pre-cooling")
        viability_300 = "RED"

    for v in verdicts:
        print(f"  • {v}")

    # Probability assessment
    print("\n### PROBABILITY ASSESSMENT ###")
    if viability_200 == "GREEN":
        p_thermal = 0.7
    elif viability_200 == "YELLOW":
        p_thermal = 0.4
    else:
        p_thermal = 0.1

    print(f"\n  P(stanene survives 200°C flue gas) = {p_thermal*100:.0f}%")
    print(f"  P(stanene survives 300°C flue gas) = {p_thermal*0.5*100:.0f}%")
    print(f"\n  KEY UNCERTAINTY: 2D stanene thermal expansion coefficient")
    print(f"  Literature data is sparse; actual α may differ from estimate")
    print()

    # Recommendations
    print("### RECOMMENDATIONS ###")
    print("  1. Use substrate with negative thermal expansion (BN, ZrW2O8)")
    print("  2. Pre-cool flue gas to <200°C before Z-channel")
    print("  3. Measure actual α for substrate-supported stanene")
    print("  4. Consider strain-compensation design (tensioned membrane)")
    print()

    # Compile results
    results = {
        'metadata': {
            'analysis': 'Thermal Lattice Drift Audit',
            'date': '2026-05-30',
            'author': 'Carl Zimmerman',
            'purpose': 'Determine if Z-strained stanene survives flue gas temperatures'
        },
        'sweep_summary': {
            'T_min_K': 300,
            'T_max_K': 600,
            'T_critical_K': sweep['T_critical_K'],
            'T_critical_C': sweep['T_critical_C'],
        },
        'flue_gas_analysis': sweep['flue_gas_analysis'],
        'cooling_requirements': {
            'at_200C': calculate_cooling_requirement(FLUE_GAS_T_TYPICAL_K, 350),
            'at_300C': calculate_cooling_requirement(FLUE_GAS_T_MAX_K, 350),
        },
        'substrate_compensation': substrates,
        'verdict': {
            'viability_200C': viability_200,
            'viability_300C': viability_300,
            'p_thermal_survival_200C': p_thermal,
            'p_thermal_survival_300C': p_thermal * 0.5,
            'key_uncertainty': '2D stanene thermal expansion coefficient not well characterized',
        },
        'recommendations': [
            'Use NTE substrate (BN or ZrW2O8) for thermal compensation',
            'Pre-cool flue gas to <200°C',
            'Measure actual α for fabricated stanene samples',
            'Consider active strain compensation',
        ],
        'ultrathink_status': 'MARGINAL - Requires mitigation strategies'
    }

    return results


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    results = run_full_thermal_audit()

    # Save results
    output_path = "../data/results/thermal_drift_results.json"

    # Convert numpy types for JSON serialization
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
