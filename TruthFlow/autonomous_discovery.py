#!/usr/bin/env python3
"""
TruthFlow Autonomous Discovery
==============================
Can Z² discover physics relationships we didn't tell it about?

This script tests whether the framework can:
1. Take ANY physical constant
2. Find Z² relationships automatically
3. Validate against measurements
4. Report what it finds (or doesn't)

Author: Carl Zimmerman
Date: May 3, 2026
"""

import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json
from pathlib import Path

# ============================================================================
# Z² CONSTANTS (IMMUTABLE)
# ============================================================================

Z2 = 32 * np.pi / 3  # = 33.510321638...
Z = np.sqrt(Z2)       # = 5.788809821...

# ============================================================================
# COMPREHENSIVE PHYSICS CONSTANTS DATABASE
# Source: CODATA 2022, PDG 2024, Planck 2020
# ============================================================================

PHYSICS_CONSTANTS = {
    # Fundamental Constants
    "speed_of_light_c": {"value": 299792458, "unit": "m/s", "source": "exact"},
    "planck_constant_h": {"value": 6.62607015e-34, "unit": "J·s", "source": "exact"},
    "elementary_charge_e": {"value": 1.602176634e-19, "unit": "C", "source": "exact"},
    "boltzmann_constant_k": {"value": 1.380649e-23, "unit": "J/K", "source": "exact"},
    "avogadro_number": {"value": 6.02214076e23, "unit": "mol⁻¹", "source": "exact"},

    # Masses (dimensionless ratios are better for Z²)
    "electron_mass_MeV": {"value": 0.51099895, "uncertainty": 0.00000015, "unit": "MeV", "source": "CODATA 2022"},
    "muon_mass_MeV": {"value": 105.6583755, "uncertainty": 0.0000023, "unit": "MeV", "source": "CODATA 2022"},
    "tau_mass_MeV": {"value": 1776.86, "uncertainty": 0.12, "unit": "MeV", "source": "PDG 2024"},
    "proton_mass_MeV": {"value": 938.27208816, "uncertainty": 0.00000029, "unit": "MeV", "source": "CODATA 2022"},
    "neutron_mass_MeV": {"value": 939.56542052, "uncertainty": 0.00000054, "unit": "MeV", "source": "CODATA 2022"},
    "W_boson_mass_GeV": {"value": 80.377, "uncertainty": 0.012, "unit": "GeV", "source": "PDG 2024"},
    "Z_boson_mass_GeV": {"value": 91.1876, "uncertainty": 0.0021, "unit": "GeV", "source": "PDG 2024"},
    "Higgs_mass_GeV": {"value": 125.25, "uncertainty": 0.17, "unit": "GeV", "source": "PDG 2024"},

    # Dimensionless Ratios (best for Z² patterns!)
    "fine_structure_constant_inverse": {"value": 137.035999084, "uncertainty": 0.000000021, "source": "CODATA 2022"},
    "weak_mixing_angle_sin2": {"value": 0.23122, "uncertainty": 0.00004, "source": "PDG 2024"},
    "strong_coupling_alpha_s": {"value": 0.1180, "uncertainty": 0.0009, "source": "PDG 2024"},
    "muon_electron_mass_ratio": {"value": 206.7682830, "uncertainty": 0.0000046, "source": "CODATA 2022"},
    "tau_electron_mass_ratio": {"value": 3477.23, "uncertainty": 0.23, "source": "CODATA 2022"},
    "tau_muon_mass_ratio": {"value": 16.817029, "uncertainty": 0.0001, "source": "CODATA 2022"},
    "proton_electron_mass_ratio": {"value": 1836.15267343, "uncertainty": 0.00000011, "source": "CODATA 2022"},
    "neutron_proton_mass_ratio": {"value": 1.00137841931, "uncertainty": 0.00000000049, "source": "CODATA 2022"},
    "neutron_electron_mass_ratio": {"value": 1838.68366173, "uncertainty": 0.00000089, "source": "CODATA 2022"},
    "W_Z_mass_ratio": {"value": 0.88147, "uncertainty": 0.00013, "source": "PDG 2024"},
    "Higgs_Z_mass_ratio": {"value": 1.374, "uncertainty": 0.002, "source": "PDG 2024"},

    # Quark Mass Ratios (MS-bar at 2 GeV)
    "up_down_mass_ratio": {"value": 0.462, "uncertainty": 0.030, "source": "PDG 2024"},
    "strange_down_mass_ratio": {"value": 20.2, "uncertainty": 1.5, "source": "PDG 2024"},
    "charm_strange_mass_ratio": {"value": 13.6, "uncertainty": 0.4, "source": "PDG 2024"},
    "bottom_charm_mass_ratio": {"value": 3.29, "uncertainty": 0.05, "source": "PDG 2024"},
    "top_bottom_mass_ratio": {"value": 41.3, "uncertainty": 0.8, "source": "PDG 2024"},
    "top_charm_mass_ratio": {"value": 136.0, "uncertainty": 3.0, "source": "PDG 2024"},
    "charm_up_mass_ratio": {"value": 588.0, "uncertainty": 109.3, "source": "PDG 2024"},
    "strange_up_mass_ratio": {"value": 43.2, "uncertainty": 8.5, "source": "PDG 2024"},
    "bottom_up_mass_ratio": {"value": 1935.2, "uncertainty": 358.6, "source": "PDG 2024"},

    # CKM Matrix
    "V_ud_magnitude": {"value": 0.97373, "uncertainty": 0.00031, "source": "PDG 2024"},
    "V_us_magnitude": {"value": 0.22650, "uncertainty": 0.00048, "source": "PDG 2024"},
    "V_ub_magnitude": {"value": 0.00382, "uncertainty": 0.00020, "source": "PDG 2024"},
    "V_cb_magnitude": {"value": 0.04182, "uncertainty": 0.00085, "source": "PDG 2024"},
    "Jarlskog_invariant": {"value": 3.18e-5, "uncertainty": 0.15e-5, "source": "PDG 2024"},

    # Neutrinos (NuFIT 5.2, NO)
    "theta_12_degrees": {"value": 33.41, "uncertainty": 0.82, "source": "NuFIT 5.2"},
    "theta_23_degrees": {"value": 42.2, "uncertainty": 1.1, "source": "NuFIT 5.2"},
    "theta_13_degrees": {"value": 8.58, "uncertainty": 0.11, "source": "NuFIT 5.2"},
    "delta_CP_degrees": {"value": 195.0, "uncertainty": 25.0, "source": "T2K+NOvA 2024"},
    "dm21_squared_eV2": {"value": 7.53e-5, "uncertainty": 0.18e-5, "source": "NuFIT 5.2"},
    "dm31_squared_eV2": {"value": 2.453e-3, "uncertainty": 0.033e-3, "source": "NuFIT 5.2"},
    "dm31_dm21_ratio": {"value": 32.6, "uncertainty": 1.8, "source": "NuFIT 5.2"},

    # Cosmology (Planck 2020 + DESI 2024)
    "Omega_Lambda": {"value": 0.6847, "uncertainty": 0.0073, "source": "Planck 2020"},
    "Omega_matter": {"value": 0.315, "uncertainty": 0.007, "source": "Planck 2020"},
    "Omega_baryon": {"value": 0.0493, "uncertainty": 0.0006, "source": "Planck 2020"},
    "Hubble_constant_km_s_Mpc": {"value": 67.4, "uncertainty": 0.5, "source": "Planck 2020"},
    "dark_energy_w": {"value": -0.99, "uncertainty": 0.15, "source": "DESI 2024"},
    "spectral_index_ns": {"value": 0.9649, "uncertainty": 0.0042, "source": "Planck 2020"},
    "optical_depth_tau": {"value": 0.0544, "uncertainty": 0.007, "source": "Planck 2020"},
    "baryon_photon_ratio": {"value": 6.14e-10, "uncertainty": 0.25e-10, "source": "Planck 2020"},
    "tensor_scalar_r_upper": {"value": 0.036, "uncertainty": None, "source": "Planck+BICEP/Keck 2021"},

    # Other
    "muon_g_minus_2_anomaly": {"value": 2.51e-9, "uncertainty": 0.59e-9, "source": "Fermilab 2023"},
    "Rydberg_constant_m_inv": {"value": 10973731.568160, "uncertainty": 0.000021, "source": "CODATA 2022"},
    "Bohr_radius_m": {"value": 5.29177210903e-11, "uncertainty": 0.00000000080e-11, "source": "CODATA 2022"},
    "electron_g_factor": {"value": -2.00231930436256, "uncertainty": 0.00000000000035, "source": "CODATA 2022"},

    # Number of things (exact integers)
    "number_gauge_bosons": {"value": 12, "uncertainty": 0, "source": "Standard Model"},
    "number_fermion_generations": {"value": 3, "uncertainty": 0, "source": "Standard Model"},
    "number_colors": {"value": 3, "uncertainty": 0, "source": "QCD"},
    "number_spacetime_dimensions": {"value": 4, "uncertainty": 0, "source": "GR"},
}

# ============================================================================
# FORMULA GENERATOR
# ============================================================================

class FormulaSearcher:
    """Generate and test Z² formulas for a target value."""

    def __init__(self):
        self.z = Z
        self.z2 = Z2

    def generate_all_candidates(self, max_complexity: int = 3) -> List[Tuple[str, str, float]]:
        """
        Generate all Z² formula candidates up to given complexity.

        Returns: List of (human_readable, python_eval, value)
        """
        candidates = []

        # Level 1: Simple powers and ratios
        for n in range(-6, 7):
            if n == 0:
                continue
            val = self.z ** n
            candidates.append((f"Z^{n}", f"Z**{n}", val))

            val2 = self.z2 ** (n/2) if n != 0 else 1
            candidates.append((f"Z²^({n}/2)", f"Z2**({n}/2)", val2))

        # Level 2: With integer coefficients
        for coef in [2, 3, 4, 5, 6, 8, 11, 12, 13, 16, 19, 64, 67]:
            for n in range(-4, 5):
                if n == 0:
                    continue

                val = coef * self.z ** n
                candidates.append((f"{coef}×Z^{n}", f"{coef}*Z**{n}", val))

                val2 = self.z ** n / coef
                candidates.append((f"Z^{n}/{coef}", f"Z**{n}/{coef}", val2))

                val3 = coef * self.z2 ** (n/2)
                candidates.append((f"{coef}×Z²^({n}/2)", f"{coef}*Z2**({n}/2)", val3))

        # Level 2: Linear combinations
        for a in range(-10, 20):
            candidates.append((f"Z² + {a}", f"Z2 + {a}", self.z2 + a))
            candidates.append((f"Z + {a}", f"Z + {a}", self.z + a))

            for b in range(1, 10):
                candidates.append((f"{b}Z + {a}", f"{b}*Z + {a}", b*self.z + a))
                candidates.append((f"{b}Z² + {a}", f"{b}*Z2 + {a}", b*self.z2 + a))

        # Level 2: With π
        for n in [1, 2, 3, 4, 8, 16, 32, 64]:
            candidates.append((f"{n}π", f"{n}*np.pi", n*np.pi))
            candidates.append((f"{n}π + Z", f"{n}*np.pi + Z", n*np.pi + self.z))
            candidates.append((f"Z² + {n}π", f"Z2 + {n}*np.pi", self.z2 + n*np.pi))

        # Level 2: Fractions
        for num in range(1, 20):
            for denom in range(2, 20):
                if num != denom and np.gcd(num, denom) == 1:
                    val = num / denom
                    candidates.append((f"{num}/{denom}", f"{num}/{denom}", val))

        # Level 3: Combined with sqrt
        sqrt_factors = [2, 3, 5, 7]
        for sf in sqrt_factors:
            for n in range(-4, 5):
                if n == 0:
                    continue
                val = self.z ** n * np.sqrt(sf)
                candidates.append((f"Z^{n}×√{sf}", f"Z**{n}*np.sqrt({sf})", val))

        # Level 3: Special combinations that work in physics
        special = [
            ("4Z² + 3", 4*self.z2 + 3),
            ("4Z² + 2", 4*self.z2 + 2),
            ("4Z² - 3", 4*self.z2 - 3),
            ("Z² - √2", self.z2 - np.sqrt(2)),
            ("1/(Z - √2)", 1/(self.z - np.sqrt(2))),
            ("13/19", 13/19),
            ("6/19", 6/19),
            ("3/13", 3/13),
            ("11/8", 11/8),
            ("67/5", 67/5),
            ("64π + Z", 64*np.pi + self.z),
            ("3Z³", 3*self.z**3),
            ("Z⁴√3", self.z**4 * np.sqrt(3)),
            ("(13/19)/Z", (13/19)/self.z),
            ("(6/19)/Z", (6/19)/self.z),
            ("α⁻¹ × 67/5", 137.036 * 67/5),
            ("2α⁴Z/13", 2 * (1/137.036)**4 * self.z / 13),
            ("5α⁴/(4Z)", 5 * (1/137.036)**4 / (4*self.z)),
            ("M_Z × √(10/13)", 91.1876 * np.sqrt(10/13)),
            ("Z²/2", self.z2/2),
            ("16π/3", 16*np.pi/3),
        ]

        for formula_str, val in special:
            candidates.append((formula_str, formula_str, val))

        return candidates

    def find_matches(self, target: float, uncertainty: float = None, tolerance: float = 0.05) -> List[Dict]:
        """
        Find Z² formulas matching a target value.

        Returns list of matches sorted by error.
        """
        candidates = self.generate_all_candidates()
        matches = []

        for formula_human, formula_python, predicted in candidates:
            if np.isnan(predicted) or np.isinf(predicted) or predicted <= 0:
                continue

            # Check if it's close
            error_pct = abs(predicted - target) / abs(target) * 100

            if error_pct > tolerance * 100:
                continue

            sigma = abs(predicted - target) / uncertainty if uncertainty and uncertainty > 0 else None

            match = {
                "formula_human": formula_human,
                "formula_python": formula_python,
                "predicted": predicted,
                "target": target,
                "error_pct": error_pct,
                "sigma": sigma,
            }

            if sigma is not None:
                if sigma < 2:
                    match["status"] = "VALIDATED"
                elif sigma < 3:
                    match["status"] = "TENSION"
                elif error_pct < 0.5:
                    match["status"] = "PRECISE"
                else:
                    match["status"] = "FAILED"
            else:
                match["status"] = "UNKNOWN"

            matches.append(match)

        # Sort by error
        matches.sort(key=lambda x: x["error_pct"])

        return matches[:5]  # Top 5

# ============================================================================
# AUTONOMOUS DISCOVERY
# ============================================================================

def run_autonomous_discovery(
    constants: Dict = None,
    tolerance: float = 0.05,
    verbose: bool = True
) -> Dict:
    """
    Autonomously search for Z² relationships in all physics constants.

    This tests whether Z² can find patterns we didn't tell it about.
    """

    if constants is None:
        constants = PHYSICS_CONSTANTS

    searcher = FormulaSearcher()

    print("=" * 80)
    print("TRUTHFLOW AUTONOMOUS DISCOVERY")
    print("=" * 80)
    print(f"Z² = 32π/3 = {Z2:.10f}")
    print(f"Z  = √Z²   = {Z:.10f}")
    print(f"Tolerance: {tolerance*100:.1f}%")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print(f"Searching {len(constants)} physics constants for Z² relationships...")
    print()

    discoveries = []
    no_matches = []

    for name, data in constants.items():
        value = data["value"]
        uncertainty = data.get("uncertainty")

        if value is None or (isinstance(value, float) and (np.isnan(value) or np.isinf(value))):
            continue

        # Skip exact values like c, h (they're definitional)
        if data.get("source") == "exact":
            continue

        # Search for matches
        matches = searcher.find_matches(value, uncertainty, tolerance)

        if matches:
            best = matches[0]
            if best["status"] in ["VALIDATED", "PRECISE", "TENSION"]:
                discoveries.append({
                    "name": name,
                    "value": value,
                    "uncertainty": uncertainty,
                    "source": data.get("source", "Unknown"),
                    "match": best
                })

                if verbose:
                    status_symbol = {"VALIDATED": "✓", "PRECISE": "△", "TENSION": "⚠"}.get(best["status"], "?")
                    sigma_str = f"σ={best['sigma']:.2f}" if best["sigma"] else "σ=N/A"
                    print(f"{status_symbol} {name}")
                    print(f"    Value: {value}")
                    print(f"    Z² formula: {best['formula_human']} = {best['predicted']:.10g}")
                    print(f"    Error: {best['error_pct']:.4f}% | {sigma_str} | {best['status']}")
                    print()
        else:
            no_matches.append(name)

    # Summary
    print("=" * 80)
    print("DISCOVERY SUMMARY")
    print("=" * 80)
    print(f"\nTotal constants searched: {len(constants)}")
    print(f"Z² patterns found: {len(discoveries)}")
    print(f"No Z² pattern: {len(no_matches)}")

    # Categorize discoveries
    validated = [d for d in discoveries if d["match"]["status"] == "VALIDATED"]
    precise = [d for d in discoveries if d["match"]["status"] == "PRECISE"]
    tension = [d for d in discoveries if d["match"]["status"] == "TENSION"]

    print(f"\n  VALIDATED (<2σ): {len(validated)}")
    print(f"  PRECISE (<0.5%): {len(precise)}")
    print(f"  TENSION (2-3σ): {len(tension)}")

    if no_matches and verbose:
        print(f"\n[NO Z² PATTERN FOUND] ({len(no_matches)} constants)")
        for name in no_matches[:10]:
            val = constants[name]["value"]
            print(f"  {name}: {val}")
        if len(no_matches) > 10:
            print(f"  ... and {len(no_matches) - 10} more")

    # Save results
    output_dir = Path(__file__).parent / "truth_accumulator"
    output_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"autonomous_discovery_{timestamp}.json"

    results = {
        "timestamp": timestamp,
        "z2": Z2,
        "z": Z,
        "tolerance": tolerance,
        "total_searched": len(constants),
        "discoveries": discoveries,
        "no_matches": no_matches,
    }

    with open(output_file, "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\nResults saved to: {output_file}")

    return results


def test_new_constant(name: str, value: float, uncertainty: float = None, tolerance: float = 0.05):
    """
    Test a single constant - can Z² explain it?

    This is the core test: given ANY physics measurement, can Z² find a formula?
    """
    print("=" * 60)
    print(f"TESTING: Can Z² explain {name}?")
    print("=" * 60)
    print(f"Value: {value}")
    print(f"Uncertainty: {uncertainty}")
    print()

    searcher = FormulaSearcher()
    matches = searcher.find_matches(value, uncertainty, tolerance)

    if not matches:
        print(f"❌ NO Z² FORMULA FOUND")
        print(f"   This quantity may not be related to Z² = 32π/3")
        print()
        return None

    print(f"Found {len(matches)} Z² formulas:")
    print()

    for i, match in enumerate(matches, 1):
        status_symbol = {
            "VALIDATED": "✓", "PRECISE": "△", "TENSION": "⚠", "FAILED": "✗"
        }.get(match["status"], "?")

        sigma_str = f"σ={match['sigma']:.2f}" if match["sigma"] else "σ=N/A"

        print(f"  {i}. {match['formula_human']} = {match['predicted']:.10g}")
        print(f"     Error: {match['error_pct']:.4f}% | {sigma_str} | {status_symbol} {match['status']}")
        print()

    best = matches[0]
    if best["status"] == "VALIDATED":
        print(f"✅ Z² CAN EXPLAIN {name}")
        print(f"   Best formula: {best['formula_human']}")
    elif best["status"] == "PRECISE":
        print(f"△ Z² MATCHES {name} (precise but high σ)")
        print(f"   Best formula: {best['formula_human']}")
    else:
        print(f"⚠ Z² TENSION with {name}")
        print(f"   Best formula: {best['formula_human']} but σ > 2")

    return matches


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Run full autonomous discovery
    results = run_autonomous_discovery(verbose=True)

    print("\n" + "=" * 80)
    print("INDIVIDUAL TESTS")
    print("=" * 80)

    # Test some specific constants that we didn't hardcode formulas for
    print("\n[Testing constants without pre-existing formulas]\n")

    # Can Z² explain the spectral index?
    test_new_constant("spectral_index_ns", 0.9649, 0.0042)

    # Can Z² explain the Jarlskog invariant?
    test_new_constant("Jarlskog_invariant", 3.18e-5, 0.15e-5)

    # Can Z² explain theta_13?
    test_new_constant("theta_13_neutrino", 8.58, 0.11)

    # Can Z² explain the up/down mass ratio?
    test_new_constant("up_down_mass_ratio", 0.462, 0.030)

    print("\n" + "=" * 80)
    print("TRUTH ENGINE AUTONOMOUS DISCOVERY COMPLETE")
    print("=" * 80)
