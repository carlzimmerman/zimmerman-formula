"""
Project Aitheria: SAW Power Audit
==================================

AGPL-3.0 License
Author: Carl Zimmerman
Date: May 2026

QUESTION: What's the energy cost of driving SAW transducers?
Does it make economic sense vs carbon credit value?

NOTE: Given the boundary layer analysis shows the nudge mechanism
      is NOT viable, this audit is somewhat academic. However,
      we complete it for thoroughness and to understand the
      energy scale if the mechanism DID work.
"""

import numpy as np
import json
from typing import Dict, Any
from aitheria_constants import (
    F_TARGET_HZ, F_SAW_HZ, MOLECULES, FLUE_GAS_COMPOSITION,
    FLUE_GAS_VELOCITY_TYPICAL, CURRENT_TECH
)

# =============================================================================
# SAW TRANSDUCER POWER MODELS
# =============================================================================

def saw_transducer_power(frequency_hz: float,
                          amplitude_nm: float = 1.0,
                          aperture_m: float = 0.01,
                          length_m: float = 1.0,
                          efficiency: float = 0.5) -> Dict[str, float]:
    """
    Estimate electrical power required for SAW transducer.

    P = (1/2) * ρ * v³ * A * (amplitude / wavelength)²

    where:
    - ρ: substrate density (LiNbO3 ≈ 4640 kg/m³)
    - v: SAW velocity (~3500 m/s)
    - A: acoustic aperture × length
    - amplitude/wavelength: strain amplitude

    Args:
        frequency_hz: SAW frequency
        amplitude_nm: Mechanical amplitude target (nm)
        aperture_m: Transducer aperture width (m)
        length_m: Transducer length along flow (m)
        efficiency: Electrical to acoustic conversion efficiency

    Returns:
        Power estimates in various units
    """
    # Substrate properties (LiNbO3)
    rho = 4640  # kg/m³
    v_saw = 3500  # m/s
    wavelength = v_saw / frequency_hz

    # Strain amplitude
    strain = amplitude_nm * 1e-9 / wavelength

    # Area of SAW propagation
    area = aperture_m * length_m

    # Acoustic power (simplified model)
    # P_acoustic ≈ (1/2) * ρ * v³ * k² * amplitude²
    # where k = 2π/λ is wavenumber
    k = 2 * np.pi / wavelength
    P_acoustic = 0.5 * rho * v_saw**3 * k**2 * (amplitude_nm * 1e-9)**2 * area

    # Electrical power (accounting for efficiency)
    P_electrical = P_acoustic / efficiency

    # Per unit area
    P_per_m2 = P_electrical / area

    return {
        'P_acoustic_W': P_acoustic,
        'P_electrical_W': P_electrical,
        'P_per_m2_W': P_per_m2,
        'wavelength_um': wavelength * 1e6,
        'strain_amplitude': strain,
        'efficiency': efficiency,
    }


def industrial_scale_power(channel_length_m: float = 10.0,
                            channel_width_m: float = 2.0,
                            channel_height_m: float = 2.0,
                            frequency_hz: float = F_TARGET_HZ) -> Dict[str, float]:
    """
    Estimate power for industrial-scale Aitheria channel.

    Assumes SAW transducers line all four walls of a rectangular duct.

    Args:
        channel_length_m: Length of Z-lined channel
        channel_width_m: Width of channel
        channel_height_m: Height of channel
        frequency_hz: SAW frequency

    Returns:
        Industrial power requirements
    """
    # Total SAW surface area (4 walls)
    wall_area = 2 * (channel_width_m + channel_height_m) * channel_length_m

    # Power per unit area (from single transducer model)
    single = saw_transducer_power(frequency_hz, amplitude_nm=1.0)
    P_per_m2 = single['P_per_m2_W']

    # Total power
    P_total_W = P_per_m2 * wall_area
    P_total_kW = P_total_W / 1000
    P_total_MW = P_total_W / 1e6

    # Gas flow rate
    cross_section = channel_width_m * channel_height_m
    velocity = FLUE_GAS_VELOCITY_TYPICAL
    flow_rate_m3_s = cross_section * velocity

    # CO2 mass flow (13% of flue gas, density ~1.8 kg/m³ at 200°C)
    co2_fraction = FLUE_GAS_COMPOSITION['CO2']
    gas_density = 0.9  # kg/m³ at 200°C
    co2_mass_flow_kg_s = flow_rate_m3_s * gas_density * co2_fraction

    # Energy per kg CO2 "processed" (not captured - mechanism doesn't work!)
    if co2_mass_flow_kg_s > 0:
        energy_per_kg_co2 = P_total_W / co2_mass_flow_kg_s  # J/kg
        energy_per_ton_co2 = energy_per_kg_co2 / 1000  # MJ/ton
        energy_kWh_per_ton = energy_per_ton_co2 / 3.6  # kWh/ton
    else:
        energy_per_kg_co2 = 0
        energy_per_ton_co2 = 0
        energy_kWh_per_ton = 0

    return {
        'wall_area_m2': wall_area,
        'P_total_W': P_total_W,
        'P_total_kW': P_total_kW,
        'P_total_MW': P_total_MW,
        'flow_rate_m3_s': flow_rate_m3_s,
        'co2_mass_flow_kg_s': co2_mass_flow_kg_s,
        'co2_mass_flow_ton_hr': co2_mass_flow_kg_s * 3.6,
        'energy_kWh_per_ton_co2': energy_kWh_per_ton,
    }


def economic_analysis(energy_kWh_per_ton: float,
                       electricity_cost_per_kWh: float = 0.10,
                       carbon_credit_per_ton: float = 100) -> Dict[str, Any]:
    """
    Compare energy cost to carbon credit value.

    Args:
        energy_kWh_per_ton: Energy consumption (kWh/ton CO2)
        electricity_cost_per_kWh: Electricity price ($/kWh)
        carbon_credit_per_ton: Carbon credit value ($/ton CO2)

    Returns:
        Economic viability analysis
    """
    # Energy cost per ton CO2
    energy_cost = energy_kWh_per_ton * electricity_cost_per_kWh

    # Net value
    net_value = carbon_credit_per_ton - energy_cost

    # Breakeven electricity price
    if energy_kWh_per_ton > 0:
        breakeven_price = carbon_credit_per_ton / energy_kWh_per_ton
    else:
        breakeven_price = float('inf')

    # Compare to amine scrubbing
    amine_energy = CURRENT_TECH['amine_scrubbing']['energy_GJ_per_ton_CO2'] * 1000 / 3.6  # kWh/ton
    amine_cost = amine_energy * electricity_cost_per_kWh

    return {
        'energy_kWh_per_ton': energy_kWh_per_ton,
        'electricity_cost_per_kWh': electricity_cost_per_kWh,
        'carbon_credit_per_ton': carbon_credit_per_ton,
        'energy_cost_per_ton': energy_cost,
        'net_value_per_ton': net_value,
        'is_profitable': net_value > 0,
        'breakeven_electricity_price': breakeven_price,
        'comparison': {
            'amine_energy_kWh_per_ton': amine_energy,
            'amine_cost_per_ton': amine_cost,
            'aitheria_vs_amine': 'better' if energy_cost < amine_cost else 'worse',
        }
    }


def run_power_audit() -> Dict[str, Any]:
    """
    Run complete SAW power audit.

    NOTE: This is somewhat academic given the nudge mechanism doesn't work,
    but we complete it for thoroughness.
    """
    print("=" * 70)
    print("PROJECT AITHERIA: SAW POWER AUDIT")
    print("=" * 70)
    print("\nQUESTION: What's the energy cost of driving SAW transducers?")
    print("NOTE: Boundary layer analysis shows nudge mechanism NOT viable.")
    print("      This audit is for completeness only.")
    print("-" * 70)

    # Single transducer analysis
    print("\n### SINGLE TRANSDUCER (10cm × 1m) ###\n")
    single = saw_transducer_power(F_TARGET_HZ, amplitude_nm=1.0)
    print(f"Frequency: {F_TARGET_HZ/1e6:.1f} MHz")
    print(f"Wavelength: {single['wavelength_um']:.2f} μm")
    print(f"Acoustic power: {single['P_acoustic_W']:.3f} W")
    print(f"Electrical power: {single['P_electrical_W']:.3f} W")
    print(f"Power density: {single['P_per_m2_W']:.1f} W/m²")
    print()

    # Industrial scale
    print("### INDUSTRIAL SCALE (10m × 2m × 2m channel) ###\n")
    industrial = industrial_scale_power(
        channel_length_m=10,
        channel_width_m=2,
        channel_height_m=2
    )
    print(f"Wall area: {industrial['wall_area_m2']:.0f} m²")
    print(f"Total power: {industrial['P_total_kW']:.1f} kW ({industrial['P_total_MW']:.3f} MW)")
    print(f"Gas flow: {industrial['flow_rate_m3_s']:.0f} m³/s")
    print(f"CO2 flow: {industrial['co2_mass_flow_ton_hr']:.1f} ton/hr")
    print(f"Energy per ton CO2: {industrial['energy_kWh_per_ton_co2']:.1f} kWh/ton")
    print()

    # Economic analysis
    print("### ECONOMIC ANALYSIS ###\n")
    econ = economic_analysis(industrial['energy_kWh_per_ton_co2'])
    print(f"Energy cost: ${econ['energy_cost_per_ton']:.2f}/ton CO2")
    print(f"Carbon credit: ${econ['carbon_credit_per_ton']:.0f}/ton CO2")
    print(f"Net value: ${econ['net_value_per_ton']:.2f}/ton CO2")
    print(f"Profitable: {econ['is_profitable']}")
    print(f"\nComparison to amine scrubbing:")
    print(f"  Amine energy: {econ['comparison']['amine_energy_kWh_per_ton']:.0f} kWh/ton")
    print(f"  Amine cost: ${econ['comparison']['amine_cost_per_ton']:.2f}/ton")
    print(f"  Aitheria vs amine: {econ['comparison']['aitheria_vs_amine']}")
    print()

    # ULTRATHINK VERDICT
    print("=" * 70)
    print("ULTRATHINK VERDICT: ENERGY ECONOMICS")
    print("=" * 70)

    verdicts = []

    # The energy cost is actually quite low!
    if econ['energy_cost_per_ton'] < 10:
        verdicts.append("GOOD: Energy cost << carbon credit value")
        energy_viability = "GREEN"
    elif econ['energy_cost_per_ton'] < 50:
        verdicts.append("MARGINAL: Energy cost significant but profitable")
        energy_viability = "YELLOW"
    else:
        verdicts.append("POOR: Energy cost too high for profitability")
        energy_viability = "RED"

    # Compare to amine
    if econ['comparison']['aitheria_vs_amine'] == 'better':
        verdicts.append("GOOD: Lower energy than amine scrubbing")
    else:
        verdicts.append("POOR: Higher energy than amine scrubbing")

    # BUT - the mechanism doesn't work!
    verdicts.append("**IRRELEVANT**: Nudge mechanism doesn't work!")
    verdicts.append("Energy efficiency is moot if capture efficiency is 0%")

    for v in verdicts:
        print(f"  • {v}")

    print("\n### HONEST ASSESSMENT ###")
    print("""
  The SAW transducer energy requirement is surprisingly low:
  ~{:.1f} kWh/ton CO2 vs ~1100 kWh/ton for amine scrubbing.

  IF the nudge mechanism worked, this would be excellent.

  BUT the boundary layer analysis shows:
  - Capture efficiency: ~0%
  - Required channel length: ~1000m
  - Thermal noise dominates completely

  CONCLUSION: Energy economics are irrelevant because
  the fundamental physics doesn't support the mechanism.

  The SAW power is low because we're only trying to "nudge"
  molecules, not separate them through a membrane. But even
  this gentle nudge is overwhelmed by thermal motion.
""".format(econ['energy_cost_per_ton']))

    # Compile results
    results = {
        'metadata': {
            'analysis': 'SAW Power Audit',
            'date': '2026-05-30',
            'author': 'Carl Zimmerman',
            'purpose': 'Evaluate energy economics of SAW-based gas separation',
            'note': 'Academic exercise - nudge mechanism NOT viable'
        },
        'single_transducer': single,
        'industrial_scale': industrial,
        'economic_analysis': econ,
        'verdict': {
            'energy_viability': energy_viability,
            'is_economic': econ['is_profitable'],
            'irrelevant_because': 'Nudge mechanism capture efficiency ~0%',
        },
        'ultrathink_status': 'N/A - Mechanism fails before energy question matters'
    }

    return results


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    results = run_power_audit()

    # Save results
    output_path = "../data/results/saw_power_results.json"

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
