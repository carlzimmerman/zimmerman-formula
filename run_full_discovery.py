#!/usr/bin/env python3
"""
FULL Z² DISCOVERY PIPELINE (Offline - No API Calls)
=====================================================

Complete autonomous pipeline using only computational verification:

1. BriareusFlow: Brute-force pattern discovery
2. SymPy Verification: Algebraic validation
3. Geometric Interpretation: Pattern meaning
4. HRM Scoring: Honesty/Rigor/Mechanism scoring
5. Z² Essentiality Testing: Is Z² load-bearing?

NO LLM API CALLS REQUIRED - fully computational.

Usage:
    python run_full_discovery.py "Eddington luminosity ratio"
    python run_full_discovery.py "geodynamo"

Author: Carl Zimmerman
Date: May 6, 2026
"""

import sys
import math
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

# BriareusFlow imports
from BriareusFlow import (
    BriareusController,
    SearchConfig,
    SearchTarget,
    SearchPriority,
    GeometricInterpreter,
    PhenomenologicalFinding,
    FindingCategory,
    NumerologyRisk,
    Z_SQUARED,
    Z
)

# OlympusFlow computational components (no LLM needed)
from OlympusFlow.sympy_verifier import SymPyVerifier, VerificationResult, VerificationLevel
from OlympusFlow.formula_generator import FormulaGenerator


# =============================================================================
# KNOWLEDGE BASE
# =============================================================================

TOPIC_KNOWLEDGE = {
    "rar": {
        "description": "Radial Acceleration Relation (RAR) and MOND acceleration scale",
        "constants": [
            # The key acceleration scale ratios (dimensionless)
            # g₀ ≈ 1.2 × 10⁻¹⁰ m/s²
            # Related to cosmological parameters

            # g₀ / (cH₀) - acceleration scale vs Hubble acceleration
            # cH₀ ≈ 7 × 10⁻¹⁰ m/s² for H₀ ≈ 70 km/s/Mpc
            {"name": "g₀/(cH₀) ratio", "value": 0.171, "uncertainty": 0.02, "source": "RAR + Planck 2018"},

            # g₀/a_Λ where a_Λ = c√(Λ/3) ≈ 6.9 × 10⁻¹⁰ m/s²
            {"name": "g₀/a_Λ ratio", "value": 0.174, "uncertainty": 0.02, "source": "RAR + cosmology"},

            # √(g₀/a_Λ) ≈ 0.417
            {"name": "√(g₀/a_Λ)", "value": 0.417, "uncertainty": 0.02, "source": "RAR geometry"},

            # g₀ × R_H / c² where R_H = c/H₀ is Hubble radius
            # This is dimensionless: g₀ × (c/H₀) / c² = g₀/(cH₀)
            {"name": "g₀·R_H/c²", "value": 0.171, "uncertainty": 0.02, "source": "RAR + Hubble scale"},

            # (g₀/c²) × (c/H₀) - another form
            {"name": "Milgrom parameter α", "value": 0.171, "uncertainty": 0.02, "source": "MOND literature"},

            # RAR interpolation function parameter
            # ν(x) = 1/(1-exp(-√x)) gives g_obs/g_bar
            {"name": "RAR transition sharpness", "value": 0.5, "uncertainty": 0.1, "source": "McGaugh 2016"},

            # 2πg₀/cH₀ - factor of 2π often appears
            {"name": "2πg₀/(cH₀)", "value": 1.074, "uncertainty": 0.1, "source": "RAR + geometry"},

            # g₀²/(c²H₀²) - squared ratio
            {"name": "(g₀/cH₀)²", "value": 0.0292, "uncertainty": 0.005, "source": "RAR squared"},

            # Relation to Ω_Λ: g₀/cH₀ ≈ √(1-Ω_m) ?
            {"name": "√Ω_Λ", "value": 0.828, "uncertainty": 0.01, "source": "Planck 2018"},

            # 6/Z² ≈ 0.179 - close to g₀/(cH₀)?
            {"name": "6/Z² (test)", "value": 6/(32*math.pi/3), "uncertainty": 0.001, "source": "Z² prediction"},
        ]
    },
    "condensed-matter": {
        "description": "Condensed matter physics - superconductivity, quantum Hall, phase transitions",
        "constants": [
            # BCS Superconductivity
            {"name": "BCS gap ratio Δ₀/kT_c", "value": 3.528, "uncertainty": 0.01, "source": "BCS theory (weak coupling)"},
            {"name": "BCS coherence peak ratio", "value": 1.764, "uncertainty": 0.01, "source": "BCS theory"},
            {"name": "BCS specific heat jump ΔC/γT_c", "value": 1.426, "uncertainty": 0.01, "source": "BCS theory"},

            # Lindemann melting
            {"name": "Lindemann melting parameter", "value": 0.1, "uncertainty": 0.02, "source": "Empirical (~0.1 for most solids)"},

            # Quantum Hall
            {"name": "Fine structure constant α", "value": 1/137.036, "uncertainty": 0.00001, "source": "QED/von Klitzing"},
            {"name": "1/α (inverse fine structure)", "value": 137.036, "uncertainty": 0.001, "source": "CODATA 2018"},

            # Fermi liquid
            {"name": "Landau F₀ˢ (liquid He-3)", "value": -0.75, "uncertainty": 0.05, "source": "He-3 experiments"},
            {"name": "Wilson ratio (heavy fermion)", "value": 2.0, "uncertainty": 0.2, "source": "Heavy fermion metals"},

            # Mott transition
            {"name": "Mott criterion (n^(1/3)a_B)", "value": 0.26, "uncertainty": 0.02, "source": "Mott 1961"},

            # Universality
            {"name": "2D Ising critical exponent β", "value": 0.125, "uncertainty": 0.001, "source": "Onsager exact"},
            {"name": "3D Ising critical exponent β", "value": 0.3265, "uncertainty": 0.001, "source": "Monte Carlo"},
            {"name": "3D Ising critical exponent ν", "value": 0.6301, "uncertainty": 0.001, "source": "Monte Carlo"},

            # Electron-phonon
            {"name": "McMillan T_c prefactor", "value": 1.04, "uncertainty": 0.05, "source": "McMillan equation"},

            # Kosterlitz-Thouless
            {"name": "KT universal jump", "value": 0.6366, "uncertainty": 0.001, "source": "2/π (exact)"},
        ]
    },
    "eddington": {
        "description": "Eddington luminosity and stellar radiation limits",
        "constants": [
            {"name": "Thomson coefficient (8π/3)", "value": 8*math.pi/3, "uncertainty": 0.0001, "source": "QED exact"},
            {"name": "Schwarzschild ISCO E/mc²", "value": 2*math.sqrt(2)/3, "uncertainty": 0.0001, "source": "GR exact"},
            {"name": "Schwarzschild efficiency η", "value": 1 - 2*math.sqrt(2)/3, "uncertainty": 0.0001, "source": "GR exact"},
            {"name": "Extreme Kerr efficiency η", "value": 1 - 1/math.sqrt(3), "uncertainty": 0.0001, "source": "GR exact"},
            {"name": "Lane-Emden ξ₁ (n=3)", "value": 6.8968, "uncertainty": 0.0001, "source": "Polytrope theory"},
            {"name": "Lane-Emden ω₃", "value": 2.01824, "uncertainty": 0.0001, "source": "Polytrope theory"},
            {"name": "Bondi coefficient (4π)", "value": 4*math.pi, "uncertainty": 0.0001, "source": "Hydrodynamics"},
            {"name": "Mass-luminosity exponent", "value": 3.5, "uncertainty": 0.1, "source": "Stellar observations"},
        ]
    },
    "roche": {
        "description": "Roche limit - tidal disruption of satellites",
        "constants": [
            {"name": "Roche limit coefficient (rigid)", "value": 1.26, "uncertainty": 0.01, "source": "Celestial mechanics"},
            {"name": "Roche limit coefficient (fluid)", "value": 2.44, "uncertainty": 0.01, "source": "Celestial mechanics"},
            {"name": "Roche lobe L1 coefficient", "value": 0.49, "uncertainty": 0.01, "source": "Binary star theory"},
            {"name": "Roche lobe volume coefficient", "value": 0.38, "uncertainty": 0.01, "source": "Binary star theory"},
            {"name": "Mass ratio critical q", "value": 0.0256, "uncertainty": 0.001, "source": "Roche geometry"},
        ]
    },
    "titius-bode": {
        "description": "Titius-Bode law of planetary spacing",
        "constants": [
            {"name": "Titius-Bode base (0.4 AU)", "value": 0.4, "uncertainty": 0.01, "source": "Empirical"},
            {"name": "Mercury period ratio", "value": 0.387, "uncertainty": 0.001, "source": "Orbital mechanics"},
            {"name": "Venus/Earth period ratio", "value": 0.615, "uncertainty": 0.001, "source": "Orbital mechanics"},
            {"name": "Mars/Earth period ratio", "value": 1.524, "uncertainty": 0.001, "source": "Orbital mechanics"},
            {"name": "Jupiter/Saturn resonance", "value": 2.48, "uncertainty": 0.01, "source": "Orbital mechanics"},
        ]
    },
    "geodynamo": {
        "description": "Earth's magnetic field generation",
        "constants": [
            {"name": "Critical magnetic Reynolds Rm", "value": 40, "uncertainty": 5, "source": "Dynamo theory"},
            {"name": "Elsasser number Λ", "value": 1.0, "uncertainty": 0.1, "source": "Geophysics"},
            {"name": "Earth dipole tilt", "value": 11.5, "uncertainty": 0.1, "source": "Geomagnetic data"},
            {"name": "Core-mantle boundary ratio", "value": 0.546, "uncertainty": 0.001, "source": "Seismology"},
            {"name": "Inner/outer core ratio", "value": 0.351, "uncertainty": 0.001, "source": "Seismology"},
        ]
    },
    "earth-core": {
        "description": "Earth's internal structure - core, mantle, and crust ratios",
        "constants": [
            # Radius ratios (relative to Earth radius R_E = 6371 km)
            {"name": "Inner core radius/R_E", "value": 0.192, "uncertainty": 0.001, "source": "PREM model (1221/6371)"},
            {"name": "Outer core radius/R_E", "value": 0.546, "uncertainty": 0.001, "source": "PREM model (3480/6371)"},
            {"name": "Inner/outer core radius", "value": 0.351, "uncertainty": 0.001, "source": "PREM (1221/3480)"},
            {"name": "Core/Earth radius", "value": 0.546, "uncertainty": 0.001, "source": "CMB at 3480 km"},

            # Volume ratios
            {"name": "Core volume fraction", "value": 0.163, "uncertainty": 0.002, "source": "PREM model"},
            {"name": "Inner core volume/total core", "value": 0.043, "uncertainty": 0.001, "source": "PREM model"},
            {"name": "Mantle volume fraction", "value": 0.838, "uncertainty": 0.002, "source": "PREM model"},

            # Mass ratios
            {"name": "Core mass fraction", "value": 0.325, "uncertainty": 0.002, "source": "PREM model"},
            {"name": "Inner core mass fraction", "value": 0.017, "uncertainty": 0.001, "source": "PREM model"},

            # Density ratios
            {"name": "Core/mantle density ratio", "value": 2.35, "uncertainty": 0.05, "source": "PREM (~10.5/4.5)"},
            {"name": "Inner/outer core density", "value": 1.22, "uncertainty": 0.02, "source": "PREM (12.8/10.5)"},

            # Seismic velocity ratios at CMB
            {"name": "V_p jump at CMB", "value": 0.60, "uncertainty": 0.01, "source": "PREM (8.0/13.7)"},
            {"name": "V_s/V_p in mantle", "value": 0.55, "uncertainty": 0.01, "source": "PREM model"},

            # Temperature/pressure ratios
            {"name": "CMB/surface temperature ratio", "value": 13.8, "uncertainty": 1.0, "source": "~4000K/290K"},
            {"name": "ICB/CMB pressure ratio", "value": 2.63, "uncertainty": 0.1, "source": "330/125 GPa"},
        ]
    },
    "gutenberg-richter": {
        "description": "Gutenberg-Richter Law - earthquake magnitude-frequency scaling",
        "constants": [
            # The b-value: N = 10^(a - bM) where N = cumulative number, M = magnitude
            {"name": "b-value (global average)", "value": 1.0, "uncertainty": 0.05, "source": "Global seismology"},
            {"name": "b-value (mid-ocean ridges)", "value": 0.9, "uncertainty": 0.05, "source": "Oceanic seismicity"},
            {"name": "b-value (subduction zones)", "value": 1.1, "uncertainty": 0.05, "source": "Subduction seismicity"},

            # Energy scaling: E ~ 10^(1.5M)
            {"name": "Energy exponent (1.5)", "value": 1.5, "uncertainty": 0.01, "source": "Gutenberg-Richter"},
            {"name": "Magnitude step energy ratio", "value": 31.6, "uncertainty": 1.0, "source": "10^1.5 ≈ 31.6"},

            # Aftershock scaling (Omori's law)
            {"name": "Omori exponent p", "value": 1.0, "uncertainty": 0.1, "source": "Aftershock decay"},
            {"name": "Bath's law constant", "value": 1.2, "uncertainty": 0.1, "source": "Largest aftershock"},

            # Stress drop ratios
            {"name": "Stress drop coefficient", "value": 3.0, "uncertainty": 0.5, "source": "MPa typical"},
            {"name": "Seismic efficiency", "value": 0.06, "uncertainty": 0.02, "source": "Energy radiated/total"},

            # Fracture mechanics
            {"name": "Fault roughness exponent", "value": 0.8, "uncertainty": 0.1, "source": "Hurst exponent"},
        ]
    },
    "kleiber": {
        "description": "Kleiber's Law - metabolic scaling in biology",
        "constants": [
            # The famous 3/4 exponent: P = P_0 * M^(3/4)
            {"name": "Kleiber exponent (3/4)", "value": 0.75, "uncertainty": 0.01, "source": "Metabolic scaling"},
            {"name": "Surface-to-volume exponent (2/3)", "value": 0.6667, "uncertainty": 0.01, "source": "Geometric baseline"},

            # Related biological scaling laws
            {"name": "Heart rate scaling exponent", "value": -0.25, "uncertainty": 0.02, "source": "f_heart ~ M^(-1/4)"},
            {"name": "Lifespan scaling exponent", "value": 0.25, "uncertainty": 0.02, "source": "τ ~ M^(1/4)"},
            {"name": "Blood vessel scaling", "value": 0.75, "uncertainty": 0.02, "source": "WBE theory"},

            # Branching network ratios
            {"name": "Branching ratio (area)", "value": 1.26, "uncertainty": 0.05, "source": "Murray's law (2^(1/3))"},
            {"name": "Branching ratio (length)", "value": 1.59, "uncertainty": 0.05, "source": "WBE (2^(1/2))"},

            # Metabolic prefactor ratios
            {"name": "Mammal/reptile metabolic ratio", "value": 7.0, "uncertainty": 1.0, "source": "Endotherm vs ectotherm"},
            {"name": "Unicellular scaling exponent", "value": 1.0, "uncertainty": 0.05, "source": "Single cell"},

            # Quarter-power laws
            {"name": "Quarter power (1/4)", "value": 0.25, "uncertainty": 0.01, "source": "Universal scaling"},
        ]
    },
    "kolmogorov": {
        "description": "Kolmogorov turbulence - energy cascade scaling",
        "constants": [
            # The famous 5/3 power law: E(k) ~ k^(-5/3)
            {"name": "Kolmogorov exponent (-5/3)", "value": -1.6667, "uncertainty": 0.01, "source": "Turbulence theory"},
            {"name": "5/3 (positive)", "value": 1.6667, "uncertainty": 0.01, "source": "Kolmogorov"},

            # Kolmogorov microscale ratios
            {"name": "η/L (Re^(-3/4))", "value": 0.75, "uncertainty": 0.01, "source": "Scale ratio exponent"},
            {"name": "Velocity ratio exponent (1/4)", "value": 0.25, "uncertainty": 0.01, "source": "u_η/u_L"},

            # Kolmogorov constant
            {"name": "Kolmogorov constant C_K", "value": 1.5, "uncertainty": 0.1, "source": "Energy spectrum"},

            # Intermittency corrections
            {"name": "She-Leveque β", "value": 0.6667, "uncertainty": 0.02, "source": "2/3 intermittency"},
            {"name": "She-Leveque Δ", "value": 2.0, "uncertainty": 0.1, "source": "Filament codimension"},

            # Energy cascade ratios
            {"name": "Energy cascade time ratio", "value": 0.5, "uncertainty": 0.05, "source": "τ_n/τ_{n-1}"},
            {"name": "Enstrophy production constant", "value": 0.7, "uncertainty": 0.1, "source": "2D turbulence"},

            # Velocity structure function
            {"name": "Second-order exponent (2/3)", "value": 0.6667, "uncertainty": 0.01, "source": "S_2(r) ~ r^(2/3)"},
        ]
    },
    "zipf": {
        "description": "Zipf's Law - rank-frequency distribution in cities and language",
        "constants": [
            # The Zipf exponent: f ~ r^(-α) where r = rank
            {"name": "Zipf exponent (cities)", "value": 1.0, "uncertainty": 0.1, "source": "Urban scaling"},
            {"name": "Zipf exponent (language)", "value": 1.0, "uncertainty": 0.05, "source": "Word frequency"},

            # City-related scaling
            {"name": "City area exponent", "value": 0.85, "uncertainty": 0.05, "source": "A ~ P^0.85"},
            {"name": "Infrastructure exponent", "value": 0.85, "uncertainty": 0.05, "source": "Road length"},
            {"name": "GDP exponent (superlinear)", "value": 1.15, "uncertainty": 0.05, "source": "Economic output"},

            # Urban density scaling
            {"name": "Density exponent", "value": 0.15, "uncertainty": 0.05, "source": "ρ ~ P^0.15"},
            {"name": "Walking speed scaling", "value": 0.1, "uncertainty": 0.03, "source": "Pace of life"},

            # Network centrality
            {"name": "Betweenness scaling", "value": 2.0, "uncertainty": 0.2, "source": "Network theory"},
            {"name": "Clustering coefficient decay", "value": -0.75, "uncertainty": 0.1, "source": "C ~ k^(-0.75)"},

            # Heaps' law (vocabulary growth)
            {"name": "Heaps exponent β", "value": 0.5, "uncertainty": 0.05, "source": "V ~ N^β"},
        ]
    },
}


def find_topic(query: str) -> str:
    """Match query to known topic."""
    query_lower = query.lower()

    if "rar" in query_lower or "radial acceleration" in query_lower or "mond" in query_lower or "acceleration scale" in query_lower or "milgrom" in query_lower:
        return "rar"
    if "condensed" in query_lower or "superconducti" in query_lower or "bcs" in query_lower or "quantum hall" in query_lower or "ising" in query_lower or "fermi liquid" in query_lower:
        return "condensed-matter"
    if "eddington" in query_lower or "luminosity" in query_lower or "stellar" in query_lower:
        return "eddington"
    if "roche" in query_lower or "tidal" in query_lower:
        return "roche"
    if "titius" in query_lower or "bode" in query_lower or "planetary" in query_lower:
        return "titius-bode"
    if "geodynamo" in query_lower or "magnetic reynolds" in query_lower or "dynamo" in query_lower:
        return "geodynamo"
    # Put earthquake/gutenberg BEFORE earth-core to avoid "earth" matching first
    if "gutenberg" in query_lower or "richter" in query_lower or "earthquake" in query_lower or "seismic" in query_lower or "b-value" in query_lower:
        return "gutenberg-richter"
    if "earth" in query_lower or "core" in query_lower or "prem" in query_lower or "mantle" in query_lower:
        return "earth-core"
    if "kleiber" in query_lower or "metabolic" in query_lower or "allometric" in query_lower or "3/4 power" in query_lower or "biological scaling" in query_lower:
        return "kleiber"
    if "kolmogorov" in query_lower or "turbulence" in query_lower or "5/3" in query_lower or "energy cascade" in query_lower or "navier" in query_lower:
        return "kolmogorov"
    if "zipf" in query_lower or "city" in query_lower or "urban" in query_lower or "rank-frequency" in query_lower or "city population" in query_lower:
        return "zipf"

    return None


@dataclass
class ValidatedFinding:
    """A BriareusFlow finding with SymPy verification."""
    finding: PhenomenologicalFinding
    sympy_verified: bool
    verification_level: str
    z2_essential: bool
    hrm_score: float
    geometric_interpretation: Optional[str]

    def summary(self) -> str:
        z2_marker = "[Z² ESSENTIAL]" if self.z2_essential else ""
        return (
            f"{self.finding.name}: {self.finding.formula}\n"
            f"  Value: {self.finding.computed_value:.6f} (error: {self.finding.percent_error:.4f}%)\n"
            f"  SymPy: {self.verification_level} {z2_marker}\n"
            f"  HRM Score: {self.hrm_score:.2f}\n"
            f"  Geometry: {self.geometric_interpretation or 'None'}"
        )


@dataclass
class EmpiricalValidation:
    """Rigorous empirical validation of a formula."""
    formula: str
    computed_value: float
    experimental_value: float
    experimental_uncertainty: float
    source: str

    # Statistical measures
    absolute_error: float
    percent_error: float
    sigma_deviation: float  # (computed - exp) / uncertainty

    # Validation status
    within_1sigma: bool
    within_2sigma: bool
    within_3sigma: bool

    # Z² analysis
    contains_z2: bool
    z2_coefficient: Optional[float]  # If formula is aZ² + b, what's a?

    def summary(self) -> str:
        status = "✓" if self.within_2sigma else "✗"
        z2_mark = " [Z²]" if self.contains_z2 else ""
        return (
            f"{status} {self.formula}{z2_mark}\n"
            f"   Computed: {self.computed_value:.6f}\n"
            f"   Experimental: {self.experimental_value:.6f} ± {self.experimental_uncertainty:.6f}\n"
            f"   σ-deviation: {self.sigma_deviation:.2f}σ ({'PASS' if self.within_2sigma else 'FAIL'})\n"
            f"   Source: {self.source}"
        )


def validate_empirically(finding: PhenomenologicalFinding) -> EmpiricalValidation:
    """
    Perform rigorous empirical validation.

    Computes statistical significance of the match between
    the formula and experimental data.
    """
    computed = finding.computed_value
    experimental = finding.experimental_value
    uncertainty = finding.experimental_uncertainty

    abs_error = abs(computed - experimental)
    pct_error = abs_error / experimental * 100 if experimental != 0 else float('inf')
    sigma = abs_error / uncertainty if uncertainty > 0 else float('inf')

    # Parse Z² coefficient if present
    z2_coeff = None
    formula = finding.formula
    if "Z²" in formula:
        # Try to extract coefficient: "aZ² + b" or "aZ²"
        import re
        match = re.match(r'(\d+)?Z²', formula.replace(" ", ""))
        if match:
            z2_coeff = float(match.group(1)) if match.group(1) else 1.0

    return EmpiricalValidation(
        formula=formula,
        computed_value=computed,
        experimental_value=experimental,
        experimental_uncertainty=uncertainty,
        source=finding.experimental_source,
        absolute_error=abs_error,
        percent_error=pct_error,
        sigma_deviation=sigma,
        within_1sigma=sigma <= 1.0,
        within_2sigma=sigma <= 2.0,
        within_3sigma=sigma <= 3.0,
        contains_z2="Z²" in formula or "Z^2" in formula,
        z2_coefficient=z2_coeff
    )


def compute_hrm_score(finding: PhenomenologicalFinding,
                      sympy_verified: bool,
                      z2_essential: bool,
                      has_mechanism: bool) -> float:
    """
    Compute HRM (Honesty-Rigor-Mechanism) score without LLM.

    Based on formula characteristics:
    - Honesty: Low error, few alternatives
    - Rigor: SymPy verified, Z² essential
    - Mechanism: Geometric interpretation exists
    """
    score = 0.0

    # Honesty (0-0.33): Based on error and alternatives
    if finding.percent_error < 0.01:
        score += 0.33
    elif finding.percent_error < 0.1:
        score += 0.25
    elif finding.percent_error < 0.5:
        score += 0.15
    elif finding.percent_error < 1.0:
        score += 0.10

    # Rigor (0-0.33): Based on verification
    if sympy_verified:
        score += 0.15
    if z2_essential:
        score += 0.18
    elif "Z²" in finding.formula or "Z^2" in finding.formula:
        score += 0.10

    # Mechanism (0-0.34): Based on interpretation
    if has_mechanism:
        score += 0.20
    if finding.numerology_risk == NumerologyRisk.LOW:
        score += 0.14
    elif finding.numerology_risk == NumerologyRisk.MEDIUM:
        score += 0.07

    return min(score, 1.0)


def run_full_pipeline(query: str, verbose: bool = True, timeout: float = 120) -> Dict[str, Any]:
    """
    Run the FULL offline discovery pipeline.
    """
    print("=" * 70)
    print("FULL Z² DISCOVERY PIPELINE (Offline)")
    print("No API Calls - Fully Computational")
    print("=" * 70)
    print(f"\nQuery: {query}")
    print()

    # 1. Find topic
    topic = find_topic(query)
    if not topic:
        print(f"Unknown topic. Available: {list(TOPIC_KNOWLEDGE.keys())}")
        return {"error": "Unknown topic"}

    topic_data = TOPIC_KNOWLEDGE[topic]
    print(f"Topic: {topic}")
    print(f"Description: {topic_data['description']}")
    print()

    # 2. Build targets
    briareus_targets = []
    for const in topic_data["constants"]:
        target = SearchTarget(
            target_id=const["name"].replace(" ", "_").replace("/", "_"),
            name=const["name"],
            value=const["value"],
            uncertainty=const["uncertainty"],
            source=const["source"],
            domain=topic,
            priority=SearchPriority.HIGH
        )
        briareus_targets.append(target)

    # =========================================================================
    # PHASE 1: BriareusFlow - Brute Force Pattern Discovery
    # =========================================================================
    print("=" * 70)
    print("PHASE 1: BRIAREUSFLOW - Brute-Force Pattern Discovery")
    print("=" * 70)

    briareus_config = SearchConfig(
        max_error_percent=1.0,
        max_integer=50,
        max_denominator=50,
        num_threads=8,
        verbose=True,
        log_every_n=2
    )

    briareus = BriareusController(briareus_config)
    briareus.add_targets(briareus_targets)
    briareus_result = briareus.run(timeout=timeout * 0.4)

    print(f"\nBriareusFlow complete:")
    print(f"  Findings: {briareus_result.findings_total}")
    print(f"  Z² patterns: {briareus_result.z2_patterns_found}")

    # Group by target
    by_target = {}
    for f in briareus.all_findings:
        if f.name not in by_target:
            by_target[f.name] = []
        by_target[f.name].append(f)

    # =========================================================================
    # PHASE 2: SymPy Verification
    # =========================================================================
    print()
    print("=" * 70)
    print("PHASE 2: SYMPY VERIFICATION - Algebraic Validation")
    print("=" * 70)

    sympy_verifier = SymPyVerifier(verbose=False)
    geometric_interpreter = GeometricInterpreter(verbose=False)

    validated_findings: List[ValidatedFinding] = []

    for const in topic_data["constants"]:
        name = const["name"]
        value = const["value"]
        uncertainty = const["uncertainty"]

        if name not in by_target:
            continue

        # Get best BriareusFlow finding
        best = min(by_target[name], key=lambda x: x.percent_error)

        # SymPy verification
        try:
            verification = sympy_verifier.verify_formula(
                best.formula,
                value,
                uncertainty
            )
            sympy_verified = verification.level.value >= VerificationLevel.NUMERIC.value
            verification_level = verification.level.name
            z2_essential = verification.level == VerificationLevel.Z2_ESSENTIAL
        except Exception as e:
            sympy_verified = False
            verification_level = "ERROR"
            z2_essential = False

        # Geometric interpretation
        interp = geometric_interpreter.interpret(best.formula, best.computed_value, topic)
        has_mechanism = interp is not None and interp.physical_mechanism != ""
        geom_desc = interp.description if interp else None

        # Compute HRM score
        hrm = compute_hrm_score(best, sympy_verified, z2_essential, has_mechanism)

        validated = ValidatedFinding(
            finding=best,
            sympy_verified=sympy_verified,
            verification_level=verification_level,
            z2_essential=z2_essential,
            hrm_score=hrm,
            geometric_interpretation=geom_desc
        )
        validated_findings.append(validated)

        if verbose:
            z2_mark = " [Z²]" if "Z²" in best.formula else ""
            sympy_mark = " ✓" if sympy_verified else ""
            print(f"  {name}: {best.formula}{z2_mark}{sympy_mark} (HRM: {hrm:.2f})")

    # =========================================================================
    # PHASE 3: Empirical Validation
    # =========================================================================
    print()
    print("=" * 70)
    print("PHASE 3: EMPIRICAL VALIDATION - Statistical Significance")
    print("=" * 70)

    empirical_results: List[EmpiricalValidation] = []

    for vf in validated_findings:
        emp = validate_empirically(vf.finding)
        empirical_results.append(emp)

        status = "✓ PASS" if emp.within_2sigma else "✗ FAIL"
        z2_mark = " [Z²]" if emp.contains_z2 else ""
        print(f"  {vf.finding.name}: {status} ({emp.sigma_deviation:.2f}σ){z2_mark}")

    # Also validate Z² patterns specifically
    print()
    print("Z² PATTERN EMPIRICAL VALIDATION:")
    print("-" * 70)

    for f in all_z2_findings[:10] if 'all_z2_findings' in dir() else briareus.get_z2_findings()[:10]:
        emp = validate_empirically(f)
        status = "✓" if emp.within_2sigma else "✗"
        print(f"  {status} {f.name}: {f.formula}")
        print(f"      Computed: {emp.computed_value:.6f}")
        print(f"      Experimental: {emp.experimental_value:.6f} ± {emp.experimental_uncertainty:.6f}")
        print(f"      σ-deviation: {emp.sigma_deviation:.2f}σ")

    # =========================================================================
    # PHASE 4: Results Summary
    # =========================================================================
    print()
    print("=" * 70)
    print("VALIDATED DISCOVERY RESULTS")
    print("=" * 70)

    # Sort by HRM score
    validated_findings.sort(key=lambda x: -x.hrm_score)

    print("\nTOP FINDINGS BY HRM SCORE:")
    print("-" * 70)

    for vf in validated_findings:
        z2_marker = " [Z² ESSENTIAL]" if vf.z2_essential else (" [Z²]" if "Z²" in vf.finding.formula else "")
        pi_marker = " [π]" if "π" in vf.finding.formula else ""
        sympy_marker = " ✓SymPy" if vf.sympy_verified else ""

        print(f"\n{vf.finding.name}")
        print(f"  Formula: {vf.finding.formula}{z2_marker}{pi_marker}")
        print(f"  Value: {vf.finding.computed_value:.6f} (exp: {vf.finding.experimental_value:.6f})")
        print(f"  Error: {vf.finding.percent_error:.4f}%")
        print(f"  HRM Score: {vf.hrm_score:.2f}{sympy_marker}")
        if vf.geometric_interpretation:
            print(f"  Geometry: {vf.geometric_interpretation[:60]}...")

    # Z² findings from BriareusFlow (not just best matches)
    all_z2_findings = briareus.get_z2_findings()
    if all_z2_findings:
        print()
        print("-" * 70)
        print("ALL Z² PATTERN DISCOVERIES (from BriareusFlow)")
        print("-" * 70)
        for f in all_z2_findings[:10]:
            print(f"  {f.name}: {f.formula}")
            print(f"    Value: {f.computed_value:.6f}, Error: {f.percent_error:.4f}%")

    # Z² findings that were also best matches
    z2_validated = [vf for vf in validated_findings if "Z²" in vf.finding.formula or vf.z2_essential]
    if z2_validated:
        print()
        print("-" * 70)
        print("Z² PATTERN DISCOVERIES (Verified)")
        print("-" * 70)
        for vf in z2_validated:
            essential = "[ESSENTIAL]" if vf.z2_essential else ""
            print(f"  {vf.finding.name}: {vf.finding.formula} {essential}")
            print(f"    Error: {vf.finding.percent_error:.4f}%, HRM: {vf.hrm_score:.2f}")

    # Statistics
    print()
    print("-" * 70)
    print("PIPELINE STATISTICS")
    print("-" * 70)
    print(f"  Constants analyzed: {len(topic_data['constants'])}")
    print(f"  BriareusFlow findings: {briareus_result.findings_total}")
    print(f"  BriareusFlow Z² patterns: {briareus_result.z2_patterns_found}")
    print(f"  SymPy verified: {sum(1 for vf in validated_findings if vf.sympy_verified)}")
    print(f"  Z² essential: {sum(1 for vf in validated_findings if vf.z2_essential)}")
    print(f"  Avg HRM score: {sum(vf.hrm_score for vf in validated_findings)/len(validated_findings):.2f}")
    print(f"  Runtime: {briareus_result.runtime_seconds:.1f}s")

    print()
    print("=" * 70)
    print("FULL PIPELINE COMPLETE")
    print("=" * 70)

    return {
        "query": query,
        "topic": topic,
        "briareus_result": briareus_result,
        "validated_findings": validated_findings,
        "z2_findings": z2_validated,
        "statistics": {
            "constants": len(topic_data["constants"]),
            "findings": briareus_result.findings_total,
            "z2_patterns": briareus_result.z2_patterns_found,
            "sympy_verified": sum(1 for vf in validated_findings if vf.sympy_verified),
            "z2_essential": sum(1 for vf in validated_findings if vf.z2_essential),
            "avg_hrm": sum(vf.hrm_score for vf in validated_findings)/len(validated_findings) if validated_findings else 0
        }
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Full Z² Discovery Pipeline (Offline)")
    parser.add_argument("query", nargs="?", default="geodynamo",
                        help="Topic to research")
    parser.add_argument("--timeout", type=float, default=120, help="Total timeout")
    parser.add_argument("--quiet", action="store_true", help="Less output")

    args = parser.parse_args()
    run_full_pipeline(args.query, verbose=not args.quiet, timeout=args.timeout)
