#!/usr/bin/env python3
"""
Z² DISCOVERY ENGINE - Simple Entry Point
==========================================

Ask a simple question, get full autonomous research.

Usage:
    python run_discovery.py "Eddington luminosity ratio"
    python run_discovery.py "Roche limit coefficient"
    python run_discovery.py "Titius-Bode law"
    python run_discovery.py "monarch butterfly navigation" --research  # Web research

The engine handles everything:
1. Research the topic → extract constants (via HermesFlow if --research)
2. BriareusFlow → brute-force pattern search
3. OlympusFlow → rigorous validation
4. Report findings

Author: Carl Zimmerman
Date: May 6, 2026
Updated: May 6, 2026 - Added HermesFlow integration via ResearchBridge
"""

import sys
import math
import asyncio
import argparse
from typing import List, Dict, Any
from dataclasses import dataclass

from BriareusFlow import (
    BriareusController,
    SearchConfig,
    SearchTarget,
    SearchPriority,
    OlympusBridge,
    integrate_with_olympusflow,
    Z_SQUARED,
    Z
)

# Try to import HermesFlow ResearchBridge for web research
try:
    from HermesFlow.research_bridge import (
        ResearchBridge,
        DomainRegistry,
        run_automated_discovery,
        HERMES_AVAILABLE
    )
    RESEARCH_BRIDGE_AVAILABLE = True
except ImportError:
    RESEARCH_BRIDGE_AVAILABLE = False
    HERMES_AVAILABLE = False


# =============================================================================
# KNOWLEDGE BASE - Known constants by topic
# =============================================================================

TOPIC_KNOWLEDGE = {
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
            {"name": "Darwin instability ratio", "value": 3.0, "uncertainty": 0.1, "source": "Tidal theory"},
        ]
    },
    "titius-bode": {
        "description": "Titius-Bode law of planetary spacing",
        "constants": [
            {"name": "Titius-Bode base (0.4 AU)", "value": 0.4, "uncertainty": 0.01, "source": "Empirical"},
            {"name": "Titius-Bode ratio", "value": 2.0, "uncertainty": 0.1, "source": "Empirical"},
            {"name": "Titius-Bode offset (0.3)", "value": 0.3, "uncertainty": 0.01, "source": "Empirical"},
            {"name": "Mercury period ratio", "value": 0.387, "uncertainty": 0.001, "source": "Orbital mechanics"},
            {"name": "Venus/Earth period ratio", "value": 0.615, "uncertainty": 0.001, "source": "Orbital mechanics"},
            {"name": "Mars/Earth period ratio", "value": 1.524, "uncertainty": 0.001, "source": "Orbital mechanics"},
            {"name": "Jupiter/Saturn resonance", "value": 2.48, "uncertainty": 0.01, "source": "Orbital mechanics"},
            {"name": "Kirkwood gap 3:1", "value": 2.5, "uncertainty": 0.01, "source": "Asteroid belt"},
        ]
    },
    "geodynamo": {
        "description": "Earth's magnetic field generation",
        "constants": [
            {"name": "Critical magnetic Reynolds Rm", "value": 40, "uncertainty": 10, "source": "Dynamo theory"},
            {"name": "Elsasser number Λ", "value": 1.0, "uncertainty": 0.1, "source": "Geophysics"},
            {"name": "Earth dipole tilt", "value": 11.5, "uncertainty": 0.1, "source": "Geomagnetic data"},
            {"name": "Secular variation rate", "value": 0.05, "uncertainty": 0.01, "source": "Geomagnetic data"},
            {"name": "Core-mantle boundary ratio", "value": 0.546, "uncertainty": 0.001, "source": "Seismology"},
            {"name": "Inner/outer core ratio", "value": 0.351, "uncertainty": 0.001, "source": "Seismology"},
        ]
    },
    "golden": {
        "description": "Golden ratio and related constants",
        "constants": [
            {"name": "Golden ratio φ", "value": (1+math.sqrt(5))/2, "uncertainty": 0.0001, "source": "Mathematics"},
            {"name": "1/φ", "value": 2/(1+math.sqrt(5)), "uncertainty": 0.0001, "source": "Mathematics"},
            {"name": "φ²", "value": ((1+math.sqrt(5))/2)**2, "uncertainty": 0.0001, "source": "Mathematics"},
            {"name": "ln(φ)", "value": math.log((1+math.sqrt(5))/2), "uncertainty": 0.0001, "source": "Mathematics"},
        ]
    },
    "river-network": {
        "description": "River network scaling laws - Hack's law, Horton's laws, fractal geometry",
        "constants": [
            # Hack's Law: L = C * A^h
            {"name": "Hack exponent h (original)", "value": 0.6, "uncertainty": 0.02, "source": "Hack 1957"},
            {"name": "Hack exponent h (mean)", "value": 0.57, "uncertainty": 0.02, "source": "Global average"},
            {"name": "Hack exponent h (Mueller)", "value": 0.55, "uncertainty": 0.02, "source": "Mueller large basins"},
            {"name": "Hack exponent h (theoretical)", "value": 0.568, "uncertainty": 0.01, "source": "Percolation theory"},
            # Horton's Bifurcation Ratio R_B
            {"name": "Bifurcation ratio R_B (mean)", "value": 4.0, "uncertainty": 0.5, "source": "Horton's law"},
            {"name": "Bifurcation ratio R_B (min)", "value": 3.0, "uncertainty": 0.2, "source": "Horton's law"},
            {"name": "Bifurcation ratio R_B (max)", "value": 5.0, "uncertainty": 0.2, "source": "Horton's law"},
            {"name": "Bifurcation ratio R_B (random)", "value": 3.618, "uncertainty": 0.1, "source": "Random network theory"},
            # Horton's Length Ratio R_L
            {"name": "Length ratio R_L", "value": 2.0, "uncertainty": 0.3, "source": "Horton's law"},
            {"name": "Length ratio R_L (typical)", "value": 2.3, "uncertainty": 0.3, "source": "Empirical"},
            # Horton's Area Ratio R_A
            {"name": "Area ratio R_A", "value": 4.5, "uncertainty": 0.5, "source": "Horton's law"},
            # Fractal Dimensions
            {"name": "Fractal dimension D_T (min)", "value": 1.7, "uncertainty": 0.05, "source": "Tokunaga networks"},
            {"name": "Fractal dimension D_T (max)", "value": 1.8, "uncertainty": 0.05, "source": "Tokunaga networks"},
            {"name": "Fractal dimension D_T (mean)", "value": 1.75, "uncertainty": 0.05, "source": "River networks"},
            {"name": "Stream branch fractal", "value": 1.84, "uncertainty": 0.05, "source": "Measured"},
            # Drainage density exponents
            {"name": "Drainage density fractal", "value": 0.71, "uncertainty": 0.05, "source": "Measured"},
            # Dimensionless ratios
            {"name": "h × 2 (Hack doubled)", "value": 1.14, "uncertainty": 0.04, "source": "Computed"},
            {"name": "R_B / R_L (ratio of ratios)", "value": 4.0/2.0, "uncertainty": 0.2, "source": "Computed"},
            {"name": "ln(R_B)/ln(R_L) (fractal)", "value": math.log(4)/math.log(2), "uncertainty": 0.1, "source": "Fractal dimension"},
        ]
    },
    "turbulence": {
        "description": "Turbulence constants - empirically observed, no first-principles derivation",
        "constants": [
            # von Kármán constant
            {"name": "von Kármán κ", "value": 0.41, "uncertainty": 0.01, "source": "Turbulent boundary layers"},
            {"name": "von Kármán κ (Bailey 2014)", "value": 0.40, "uncertainty": 0.02, "source": "Bailey et al 2014"},
            {"name": "von Kármán κ (Nagib)", "value": 0.384, "uncertainty": 0.01, "source": "Nagib & Chauhan 2008"},
            # Strouhal number
            {"name": "Strouhal St (cylinder)", "value": 0.21, "uncertainty": 0.01, "source": "Vortex shedding"},
            {"name": "Strouhal St (universal)", "value": 0.20, "uncertainty": 0.01, "source": "Bluff bodies"},
            {"name": "Strouhal St* (wake)", "value": 0.178, "uncertainty": 0.01, "source": "Roshko 1954"},
            # Critical Reynolds numbers
            {"name": "Re_crit (pipe)", "value": 2300, "uncertainty": 100, "source": "Pipe flow transition"},
            {"name": "Re_crit (Schiller)", "value": 2320, "uncertainty": 50, "source": "Schiller lower critical"},
            {"name": "Re_crit (theoretical)", "value": 1840, "uncertainty": 50, "source": "Axisymmetric stability"},
            {"name": "Re_crit (flat plate)", "value": 500000, "uncertainty": 50000, "source": "Boundary layer transition"},
            # Kolmogorov constants
            {"name": "Kolmogorov C_K", "value": 1.5, "uncertainty": 0.1, "source": "Energy spectrum"},
            {"name": "Kolmogorov C_2", "value": 2.0, "uncertainty": 0.1, "source": "Structure function"},
            # Turbulence exponents
            {"name": "Kolmogorov -5/3 exponent", "value": -5/3, "uncertainty": 0.01, "source": "Inertial range"},
            {"name": "Richardson 4/3 exponent", "value": 4/3, "uncertainty": 0.01, "source": "Eddy diffusion"},
            # Other empirical constants
            {"name": "Sphere drag C_d", "value": 0.47, "uncertainty": 0.02, "source": "Sphere at Re>1000"},
            {"name": "Critical Weber We_crit", "value": 12, "uncertainty": 1, "source": "Droplet breakup"},
            {"name": "Smagorinsky C_s", "value": 0.17, "uncertainty": 0.02, "source": "LES modeling"},
            # Dimensionless ratios
            {"name": "1/κ (log law slope)", "value": 1/0.41, "uncertainty": 0.05, "source": "Wall law"},
            {"name": "κ²", "value": 0.41**2, "uncertainty": 0.01, "source": "Squared von Kármán"},
        ]
    },
    "snowflake": {
        "description": "Snowflake and ice crystal structure (Ice Ih)",
        "constants": [
            # Exact geometric values
            {"name": "Hexagonal arm angle", "value": 60.0, "uncertainty": 0.0001, "source": "Hexagonal symmetry"},
            {"name": "Internal hexagon angle", "value": 120.0, "uncertainty": 0.0001, "source": "Hexagonal symmetry"},
            {"name": "Tetrahedral angle arccos(-1/3)", "value": math.degrees(math.acos(-1/3)), "uncertainty": 0.0001, "source": "Exact geometry"},
            {"name": "-cos(tetrahedral) = 1/3", "value": 1/3, "uncertainty": 0.0001, "source": "Exact"},
            {"name": "Number of arms", "value": 6, "uncertainty": 0.0001, "source": "Hexagonal symmetry"},
            # Bond angles
            {"name": "H-O-H angle in ice", "value": 109.47, "uncertainty": 0.01, "source": "Ice Ih structure"},
            {"name": "H-O-H angle in water", "value": 104.5, "uncertainty": 0.1, "source": "Liquid water"},
            {"name": "Water/ice angle ratio", "value": 104.5/109.47, "uncertainty": 0.001, "source": "Computed"},
            # Bond lengths (Angstroms)
            {"name": "O-O hydrogen bond", "value": 2.76, "uncertainty": 0.01, "source": "Ice Ih neutron diffraction"},
            {"name": "O-H covalent bond", "value": 1.01, "uncertainty": 0.01, "source": "Ice Ih structure"},
            {"name": "O-H/O-O bond ratio", "value": 1.01/2.76, "uncertainty": 0.005, "source": "Computed"},
            # Density
            {"name": "Ice Ih density", "value": 0.917, "uncertainty": 0.001, "source": "Ice physics"},
            {"name": "Ice/water density ratio", "value": 0.917, "uncertainty": 0.001, "source": "Ice physics"},
            # Lattice spacings
            {"name": "Interlayer spacing (nm)", "value": 0.276, "uncertainty": 0.001, "source": "Ice Ih crystallography"},
            {"name": "Inter-plane spacing (nm)", "value": 0.0923, "uncertainty": 0.001, "source": "Ice Ih crystallography"},
            {"name": "Plane/layer spacing ratio", "value": 0.0923/0.276, "uncertainty": 0.005, "source": "Computed"},
            # Dimensionless angles as fractions of circle
            {"name": "60°/360° = 1/6", "value": 1/6, "uncertainty": 0.0001, "source": "Hexagonal fraction"},
            {"name": "120°/360° = 1/3", "value": 1/3, "uncertainty": 0.0001, "source": "Hexagonal fraction"},
            {"name": "Tetrahedral/360°", "value": math.degrees(math.acos(-1/3))/360, "uncertainty": 0.0001, "source": "Computed"},
        ]
    },
    "earthquake-aftershock": {
        "description": "Earthquake aftershock decay - Omori's law, Båth's law, Gutenberg-Richter",
        "constants": [
            # Omori's Law: n(t) = K / (c + t)^p
            {"name": "Omori p-value (universal)", "value": 1.0, "uncertainty": 0.1, "source": "Omori 1894"},
            {"name": "Omori p-value (California)", "value": 1.22, "uncertainty": 0.03, "source": "California sequences"},
            {"name": "Omori p-value (Morocco 2023)", "value": 1.56, "uncertainty": 0.02, "source": "Morocco earthquake study"},
            {"name": "Omori p-value (global mean)", "value": 1.1, "uncertainty": 0.1, "source": "Global average"},
            {"name": "Omori c (time delay)", "value": 0.02, "uncertainty": 0.01, "source": "Days, typical"},
            # Båth's Law: ΔM = M_mainshock - M_largest_aftershock
            {"name": "Båth law ΔM", "value": 1.2, "uncertainty": 0.1, "source": "Båth 1965"},
            {"name": "Båth law (precise)", "value": 1.18, "uncertainty": 0.05, "source": "Global catalog"},
            # Gutenberg-Richter Law: log₁₀(N) = a - b*M
            {"name": "Gutenberg-Richter b-value", "value": 1.0, "uncertainty": 0.05, "source": "Gutenberg-Richter"},
            {"name": "G-R b-value (global)", "value": 0.95, "uncertainty": 0.05, "source": "Global seismicity"},
            {"name": "G-R b-value (subduction)", "value": 0.85, "uncertainty": 0.1, "source": "Subduction zones"},
            {"name": "G-R b-value (volcanic)", "value": 1.3, "uncertainty": 0.1, "source": "Volcanic regions"},
            # Energy-magnitude relationship: log₁₀(E) = 1.5*M + 4.8
            {"name": "Energy-magnitude factor", "value": 1.5, "uncertainty": 0.01, "source": "Kanamori 1977"},
            {"name": "Energy constant 4.8", "value": 4.8, "uncertainty": 0.1, "source": "Joules convention"},
            # Aftershock productivity: log₁₀(N) = α*M + β
            {"name": "Aftershock productivity α", "value": 1.0, "uncertainty": 0.1, "source": "Felzer et al"},
            {"name": "Aftershock zone L/rupture", "value": 1.5, "uncertainty": 0.2, "source": "Rupture scaling"},
            # Dimensionless ratios
            {"name": "10^(ΔM) energy ratio", "value": 10**1.2, "uncertainty": 1, "source": "Computed from Båth"},
            {"name": "Energy ratio 10^(1.5)", "value": 10**1.5, "uncertainty": 0.5, "source": "Per magnitude step"},
            {"name": "Omori p - 1 (departure)", "value": 0.1, "uncertainty": 0.1, "source": "Deviation from unity"},
            {"name": "b/p ratio", "value": 1.0/1.1, "uncertainty": 0.05, "source": "Scaling connection"},
        ]
    },
    "kleiber": {
        "description": "Kleiber's law metabolic scaling - quarter-power biology",
        "constants": [
            # Kleiber's Law: B ∝ M^α where α ≈ 3/4
            {"name": "Kleiber exponent (observed)", "value": 0.75, "uncertainty": 0.01, "source": "Kleiber 1932"},
            {"name": "Kleiber exponent (mammals)", "value": 0.74, "uncertainty": 0.02, "source": "Mammalian data"},
            {"name": "Kleiber exponent (birds)", "value": 0.72, "uncertainty": 0.02, "source": "Avian data"},
            {"name": "Kleiber exponent (fish)", "value": 0.79, "uncertainty": 0.03, "source": "Fish metabolic data"},
            {"name": "Kleiber exponent (plants)", "value": 0.75, "uncertainty": 0.02, "source": "Plant growth"},
            # West-Brown-Enquist theoretical derivation
            {"name": "WBE theoretical 3/4", "value": 3/4, "uncertainty": 0.001, "source": "West-Brown-Enquist 1997"},
            # Related quarter-power scaling laws
            {"name": "Heart rate exponent", "value": -0.25, "uncertainty": 0.01, "source": "Heart rate ~ M^-1/4"},
            {"name": "Lifespan exponent", "value": 0.25, "uncertainty": 0.02, "source": "Lifespan ~ M^1/4"},
            {"name": "Circulation time exp", "value": 0.25, "uncertainty": 0.01, "source": "Blood circuit time"},
            {"name": "Aorta radius exponent", "value": 0.375, "uncertainty": 0.01, "source": "Aorta ~ M^3/8"},
            # Surface area scaling (alternative theory)
            {"name": "Surface area exponent", "value": 2/3, "uncertainty": 0.01, "source": "Rubner isometry"},
            {"name": "Rubner 2/3 law", "value": 0.667, "uncertainty": 0.01, "source": "Rubner 1883"},
            # Dimensionless ratios
            {"name": "3/4 exact", "value": 0.75, "uncertainty": 0.0001, "source": "Quarter-power exact"},
            {"name": "1/4 exact", "value": 0.25, "uncertainty": 0.0001, "source": "Quarter-power exact"},
            {"name": "3/8 exact", "value": 0.375, "uncertainty": 0.0001, "source": "Eighth-power exact"},
            {"name": "Kleiber/Rubner ratio", "value": 0.75/0.667, "uncertainty": 0.01, "source": "Computed"},
            {"name": "4 × Kleiber exp", "value": 3.0, "uncertainty": 0.01, "source": "Dimensionality"},
            {"name": "1 - Kleiber exp", "value": 0.25, "uncertainty": 0.01, "source": "Complementary"},
            {"name": "Kleiber exp squared", "value": 0.5625, "uncertainty": 0.01, "source": "Computed"},
        ]
    },
    "zipf": {
        "description": "Zipf's law and power-law distributions - word frequencies, city sizes, wealth",
        "constants": [
            # Zipf's Law: f(r) ∝ 1/r^α
            {"name": "Zipf exponent (ideal)", "value": 1.0, "uncertainty": 0.01, "source": "Zipf 1935"},
            {"name": "Zipf exponent (English)", "value": 1.07, "uncertainty": 0.02, "source": "English word frequency"},
            {"name": "Zipf exponent (cities)", "value": 1.05, "uncertainty": 0.05, "source": "City size distribution"},
            {"name": "Zipf exponent (web)", "value": 0.95, "uncertainty": 0.05, "source": "Web page popularity"},
            # Zipf-Mandelbrot: f(r) ∝ 1/(r+q)^α
            {"name": "Mandelbrot q parameter", "value": 2.7, "uncertainty": 0.3, "source": "Mandelbrot modification"},
            # Heaps' Law: V(n) ∝ n^β (vocabulary growth)
            {"name": "Heaps exponent β (low)", "value": 0.4, "uncertainty": 0.05, "source": "Heaps law lower"},
            {"name": "Heaps exponent β (high)", "value": 0.6, "uncertainty": 0.05, "source": "Heaps law upper"},
            {"name": "Heaps exponent β (typical)", "value": 0.5, "uncertainty": 0.05, "source": "Heaps law mean"},
            # Pareto Distribution (wealth, 80/20 rule)
            {"name": "Pareto exponent α", "value": 1.16, "uncertainty": 0.1, "source": "Pareto income"},
            {"name": "Pareto 80/20 exponent", "value": math.log(5)/math.log(4), "uncertainty": 0.01, "source": "80/20 rule exact"},
            # Benford's Law: P(d) = log10(1 + 1/d)
            {"name": "Benford P(1) = log10(2)", "value": math.log10(2), "uncertainty": 0.0001, "source": "Benford exact"},
            {"name": "Benford P(2)", "value": math.log10(3/2), "uncertainty": 0.0001, "source": "Benford exact"},
            {"name": "Benford P(9)", "value": math.log10(10/9), "uncertainty": 0.0001, "source": "Benford exact"},
            # Power law exponents in nature
            {"name": "Earthquake freq exp", "value": 1.0, "uncertainty": 0.05, "source": "Gutenberg-Richter b"},
            {"name": "Solar flare exp", "value": 1.8, "uncertainty": 0.1, "source": "Solar flare frequency"},
            {"name": "Forest fire exp", "value": 1.3, "uncertainty": 0.1, "source": "Forest fire size"},
            # Dimensionless ratios
            {"name": "1/Zipf = 1", "value": 1.0, "uncertainty": 0.01, "source": "Inverse Zipf"},
            {"name": "Zipf - Heaps", "value": 0.5, "uncertainty": 0.05, "source": "Exponent difference"},
            {"name": "ln(2)", "value": math.log(2), "uncertainty": 0.0001, "source": "Natural log 2"},
        ]
    },
    "fluid-advanced": {
        "description": "Advanced fluid dynamics constants - drag, instabilities, mixing",
        "constants": [
            # Drag coefficients
            {"name": "Cylinder drag C_d", "value": 1.2, "uncertainty": 0.1, "source": "Bluff body"},
            {"name": "Flat plate friction (laminar)", "value": 1.328, "uncertainty": 0.01, "source": "Blasius"},
            {"name": "Flat plate friction (turbulent)", "value": 0.074, "uncertainty": 0.005, "source": "Re^-0.2 scaling"},
            # Critical numbers for instabilities
            {"name": "Critical Rayleigh (convection)", "value": 1708, "uncertainty": 10, "source": "Benard cells"},
            {"name": "Critical Taylor number", "value": 1708, "uncertainty": 10, "source": "Couette instability"},
            {"name": "Critical Dean number", "value": 36, "uncertainty": 2, "source": "Curved pipe"},
            {"name": "Critical Grashof", "value": 1e9, "uncertainty": 1e8, "source": "Natural convection"},
            # Turbulence structure
            {"name": "Turbulent Prandtl Pr_t", "value": 0.85, "uncertainty": 0.05, "source": "Heat/momentum"},
            {"name": "Log-law intercept B", "value": 5.2, "uncertainty": 0.3, "source": "Wall turbulence"},
            {"name": "Boundary layer shape H", "value": 2.59, "uncertainty": 0.05, "source": "Blasius profile"},
            {"name": "Entrainment coefficient", "value": 0.08, "uncertainty": 0.01, "source": "Jet spreading"},
            # Higher-order statistics
            {"name": "Skewness factor S", "value": -0.4, "uncertainty": 0.05, "source": "Velocity derivative"},
            {"name": "Flatness factor F", "value": 7.5, "uncertainty": 0.5, "source": "Intermittency"},
            {"name": "Kolmogorov C_2", "value": 2.0, "uncertainty": 0.1, "source": "Structure function"},
            # Wake geometry
            {"name": "Kelvin wake angle", "value": 19.47, "uncertainty": 0.01, "source": "Ship wake degrees"},
            {"name": "Wake angle arcsin(1/3)", "value": math.degrees(math.asin(1/3)), "uncertainty": 0.01, "source": "Exact geometry"},
            # Force coefficients
            {"name": "Added mass (sphere)", "value": 0.5, "uncertainty": 0.01, "source": "Potential flow"},
            {"name": "Lift slope 2π", "value": 2*math.pi, "uncertainty": 0.01, "source": "Thin airfoil"},
            {"name": "Oseen correction 3/8", "value": 3/8, "uncertainty": 0.01, "source": "Low Re drag"},
        ]
    },
    "geophysics-planetary": {
        "description": "Geophysics and planetary science constants",
        "constants": [
            # Earth shape and rotation
            {"name": "Earth oblateness 1/f", "value": 298.257, "uncertainty": 0.001, "source": "WGS84"},
            {"name": "Chandler wobble (days)", "value": 433, "uncertainty": 1, "source": "Free nutation"},
            {"name": "LOD change (ms/century)", "value": 2.3, "uncertainty": 0.1, "source": "Tidal braking"},
            # Internal structure ratios
            {"name": "Core/Earth radius", "value": 0.546, "uncertainty": 0.001, "source": "Seismology"},
            {"name": "Inner/outer core", "value": 0.351, "uncertainty": 0.001, "source": "Seismology"},
            {"name": "Moho depth (km)", "value": 35, "uncertainty": 5, "source": "Continental"},
            {"name": "Lithosphere (km)", "value": 100, "uncertainty": 20, "source": "Thermal"},
            # Seismic properties
            {"name": "P/S velocity ratio", "value": 1.732, "uncertainty": 0.01, "source": "sqrt(3)"},
            {"name": "Mantle Q factor", "value": 300, "uncertainty": 100, "source": "Attenuation"},
            {"name": "Adiabatic gradient K/km", "value": 0.5, "uncertainty": 0.1, "source": "Mantle"},
            # Plate tectonics
            {"name": "Plate velocity cm/yr", "value": 5, "uncertainty": 2, "source": "Mean rate"},
            {"name": "Subduction angle deg", "value": 45, "uncertainty": 10, "source": "Mean dip"},
            {"name": "Ridge push 10^12 N/m", "value": 2.5, "uncertainty": 0.5, "source": "Driving force"},
            # Magnetic field
            {"name": "Reversal rate /Myr", "value": 4.5, "uncertainty": 1, "source": "Polarity"},
            {"name": "Dipole decay kyr", "value": 20, "uncertainty": 5, "source": "Diffusion time"},
            {"name": "Dipole tilt degrees", "value": 11.5, "uncertainty": 0.5, "source": "Current"},
            # Heat flow
            {"name": "Heat flow mW/m2", "value": 87, "uncertainty": 5, "source": "Global mean"},
            {"name": "Radiogenic fraction", "value": 0.7, "uncertainty": 0.1, "source": "Heat source"},
            {"name": "Mantle viscosity ratio", "value": 100, "uncertainty": 50, "source": "Upper/lower"},
        ]
    },
    "atmospheric": {
        "description": "Atmospheric and climate science constants",
        "constants": [
            # Vertical structure
            {"name": "Lapse rate K/km", "value": 6.5, "uncertainty": 0.5, "source": "Troposphere"},
            {"name": "Tropopause height km", "value": 11, "uncertainty": 2, "source": "Mid-latitude"},
            {"name": "Scale height km", "value": 8.5, "uncertainty": 0.5, "source": "Pressure e-fold"},
            # Stability
            {"name": "Critical Richardson", "value": 0.25, "uncertainty": 0.02, "source": "Turbulence onset"},
            {"name": "Bulk aerodynamic C_D", "value": 0.0015, "uncertainty": 0.0003, "source": "Ocean surface"},
            {"name": "Charnock constant", "value": 0.015, "uncertainty": 0.005, "source": "Wave roughness"},
            # Energy balance
            {"name": "Earth albedo", "value": 0.30, "uncertainty": 0.02, "source": "Reflectivity"},
            {"name": "Effective emissivity", "value": 0.612, "uncertainty": 0.02, "source": "Greenhouse"},
            {"name": "Solar constant W/m2", "value": 1361, "uncertainty": 1, "source": "TSI"},
            # Climate sensitivity
            {"name": "ECS degrees C", "value": 3.0, "uncertainty": 1.5, "source": "Per CO2 doubling"},
            {"name": "TCR degrees C", "value": 1.8, "uncertainty": 0.6, "source": "Transient"},
            {"name": "TCR/ECS ratio", "value": 0.6, "uncertainty": 0.1, "source": "Response ratio"},
            # Carbon cycle
            {"name": "Airborne fraction", "value": 0.45, "uncertainty": 0.05, "source": "CO2 remaining"},
            {"name": "Ocean uptake fraction", "value": 0.25, "uncertainty": 0.05, "source": "Absorbed"},
            {"name": "Revelle factor", "value": 10, "uncertainty": 1, "source": "Buffer capacity"},
            # Feedbacks W/m2/K
            {"name": "Water vapor feedback", "value": 1.8, "uncertainty": 0.3, "source": "Dominant"},
            {"name": "Ice-albedo feedback", "value": 0.3, "uncertainty": 0.1, "source": "Polar"},
            {"name": "Cloud feedback", "value": 0.5, "uncertainty": 0.5, "source": "Uncertain"},
            {"name": "Planck feedback", "value": -3.2, "uncertainty": 0.1, "source": "Stabilizing"},
        ]
    },
    "oceanography": {
        "description": "Oceanography and marine physics constants",
        "constants": [
            # Circulation scales
            {"name": "Ekman depth m", "value": 100, "uncertainty": 30, "source": "Wind-driven"},
            {"name": "Ekman angle degrees", "value": 45, "uncertainty": 5, "source": "Surface deflection"},
            {"name": "Thermocline depth m", "value": 500, "uncertainty": 200, "source": "Stratification"},
            {"name": "Mixed layer m", "value": 100, "uncertainty": 50, "source": "Seasonal mean"},
            # Transport
            {"name": "Thermohaline Sv", "value": 20, "uncertainty": 5, "source": "Overturning"},
            {"name": "Gulf Stream Sv", "value": 30, "uncertainty": 5, "source": "Western boundary"},
            {"name": "ACC transport Sv", "value": 140, "uncertainty": 10, "source": "Antarctic"},
            # Energy
            {"name": "Tidal dissipation TW", "value": 3.7, "uncertainty": 0.2, "source": "Global"},
            {"name": "Wind power input TW", "value": 1.0, "uncertainty": 0.2, "source": "Surface"},
            {"name": "Eddy/mean KE ratio", "value": 100, "uncertainty": 50, "source": "Mesoscale"},
            # Waves
            {"name": "Wave breaking H/L", "value": 1/7, "uncertainty": 0.01, "source": "Steepness limit"},
            {"name": "Stokes drift ratio", "value": 0.01, "uncertainty": 0.005, "source": "Drift/phase"},
            {"name": "Significant wave factor", "value": 4, "uncertainty": 0.1, "source": "Hs = 4σ"},
            # Mixing
            {"name": "Diapycnal diffusivity", "value": 1e-5, "uncertainty": 5e-6, "source": "m2/s background"},
            {"name": "Isopycnal diffusivity", "value": 1000, "uncertainty": 500, "source": "m2/s"},
            {"name": "Mixing efficiency", "value": 0.2, "uncertainty": 0.05, "source": "Osborn"},
            # Density
            {"name": "Thermal expansion", "value": 2e-4, "uncertainty": 5e-5, "source": "/K at 20C"},
            {"name": "Haline contraction", "value": 7.5e-4, "uncertainty": 1e-4, "source": "/PSU"},
            {"name": "Density ratio R_rho", "value": 2, "uncertainty": 0.5, "source": "Double diffusion"},
        ]
    },
    "physiology": {
        "description": "Biological physiology and scaling constants",
        "constants": [
            # Respiration
            {"name": "Respiratory quotient", "value": 0.82, "uncertainty": 0.05, "source": "CO2/O2"},
            {"name": "Oxygen extraction", "value": 0.25, "uncertainty": 0.05, "source": "Tissue uptake"},
            {"name": "VO2max scaling exp", "value": 0.75, "uncertainty": 0.05, "source": "Aerobic capacity"},
            # Cardiovascular
            {"name": "Blood pressure mmHg", "value": 100, "uncertainty": 10, "source": "Mammal constant"},
            {"name": "Hematocrit optimal", "value": 0.45, "uncertainty": 0.05, "source": "Viscosity tradeoff"},
            {"name": "Cardiac output exp", "value": 0.75, "uncertainty": 0.05, "source": "Blood flow"},
            {"name": "Stroke volume exp", "value": 1.0, "uncertainty": 0.05, "source": "Per beat"},
            # Cellular
            {"name": "Capillary spacing um", "value": 40, "uncertainty": 10, "source": "O2 diffusion"},
            {"name": "Mitochondria density exp", "value": -0.25, "uncertainty": 0.05, "source": "Per cell"},
            {"name": "Cell turnover exp", "value": -0.25, "uncertainty": 0.05, "source": "Replacement"},
            # Neural
            {"name": "Synapse density /mm3", "value": 1e8, "uncertainty": 5e7, "source": "Cortex"},
            {"name": "Conduction velocity m/s", "value": 100, "uncertainty": 20, "source": "Myelinated"},
            {"name": "Reaction time exp", "value": 0.25, "uncertainty": 0.05, "source": "Body size"},
            # Life history
            {"name": "Gestation exp", "value": 0.25, "uncertainty": 0.03, "source": "Duration"},
            {"name": "Maturity age exp", "value": 0.25, "uncertainty": 0.03, "source": "Development"},
            {"name": "Max lifespan exp", "value": 0.25, "uncertainty": 0.03, "source": "Senescence"},
            # Locomotion
            {"name": "Max run speed exp", "value": 0.17, "uncertainty": 0.03, "source": "Sprint"},
            {"name": "Cost of transport exp", "value": -0.25, "uncertainty": 0.03, "source": "J/kg/m"},
            {"name": "Froude optimal", "value": 0.25, "uncertainty": 0.05, "source": "Walk-run"},
        ]
    },
    "ecology": {
        "description": "Ecology and population dynamics constants",
        "constants": [
            # Biodiversity
            {"name": "Species-area z", "value": 0.25, "uncertainty": 0.05, "source": "Island biogeography"},
            {"name": "Fisher alpha", "value": 10, "uncertainty": 5, "source": "Log-series"},
            {"name": "Preston lambda", "value": 1.0, "uncertainty": 0.2, "source": "Lognormal"},
            # Trophic
            {"name": "Predator/prey mass", "value": 100, "uncertainty": 50, "source": "Ratio"},
            {"name": "Trophic efficiency", "value": 0.10, "uncertainty": 0.03, "source": "10% rule"},
            {"name": "Assimilation efficiency", "value": 0.70, "uncertainty": 0.1, "source": "Ingestion"},
            {"name": "Production efficiency", "value": 0.30, "uncertainty": 0.1, "source": "Net growth"},
            # Population
            {"name": "Intrinsic rate r_max", "value": 0.5, "uncertainty": 0.2, "source": "Per year typical"},
            {"name": "Carrying capacity exp", "value": -0.75, "uncertainty": 0.1, "source": "Density"},
            {"name": "Generation time exp", "value": 0.25, "uncertainty": 0.05, "source": "Life history"},
            # Extinction
            {"name": "Background extinction", "value": 0.1, "uncertainty": 0.05, "source": "Per Myr"},
            {"name": "Speciation rate", "value": 0.3, "uncertainty": 0.1, "source": "Per Myr"},
            {"name": "Turnover rate", "value": 0.2, "uncertainty": 0.1, "source": "Species/Myr"},
            # Food webs
            {"name": "Connectance", "value": 0.10, "uncertainty": 0.03, "source": "Links/possible"},
            {"name": "Food chain length", "value": 4, "uncertainty": 1, "source": "Trophic levels"},
            {"name": "Omnivory index", "value": 0.3, "uncertainty": 0.1, "source": "Diet breadth"},
            # Succession
            {"name": "Succession half-life yr", "value": 50, "uncertainty": 20, "source": "Recovery"},
            {"name": "Fire return interval", "value": 30, "uncertainty": 20, "source": "Years"},
            {"name": "Decomposition rate /yr", "value": 0.5, "uncertainty": 0.3, "source": "Litter k"},
        ]
    },
    "cosmology": {
        "description": "Astrophysics and cosmology fundamental constants",
        "constants": [
            # Fundamental couplings
            {"name": "Fine structure 1/alpha", "value": 137.036, "uncertainty": 0.001, "source": "QED"},
            {"name": "Weak mixing sin2_theta", "value": 0.2312, "uncertainty": 0.0002, "source": "Electroweak"},
            {"name": "Strong coupling alpha_s", "value": 0.118, "uncertainty": 0.001, "source": "QCD at M_Z"},
            # Cosmological parameters
            {"name": "Dark energy Omega_Lambda", "value": 0.685, "uncertainty": 0.01, "source": "Planck"},
            {"name": "Dark matter Omega_DM", "value": 0.265, "uncertainty": 0.01, "source": "Planck"},
            {"name": "Baryon Omega_b", "value": 0.050, "uncertainty": 0.001, "source": "Planck"},
            {"name": "Hubble h", "value": 0.674, "uncertainty": 0.005, "source": "Planck"},
            {"name": "CMB temperature K", "value": 2.7255, "uncertainty": 0.0001, "source": "COBE"},
            # Primordial
            {"name": "Helium Y_p", "value": 0.247, "uncertainty": 0.002, "source": "BBN"},
            {"name": "Spectral index n_s", "value": 0.965, "uncertainty": 0.004, "source": "Inflation"},
            {"name": "Sigma_8", "value": 0.811, "uncertainty": 0.01, "source": "Clustering"},
            {"name": "Optical depth tau", "value": 0.054, "uncertainty": 0.007, "source": "Reionization"},
            # Stellar/galactic
            {"name": "Salpeter IMF slope", "value": 2.35, "uncertainty": 0.1, "source": "Mass function"},
            {"name": "IMF turnover M_sun", "value": 0.5, "uncertainty": 0.2, "source": "Characteristic"},
            {"name": "Star formation eff", "value": 0.02, "uncertainty": 0.01, "source": "Per free-fall"},
            {"name": "Tully-Fisher slope", "value": 4.0, "uncertainty": 0.3, "source": "L vs v"},
            {"name": "M-sigma slope", "value": 4.5, "uncertainty": 0.5, "source": "BH mass"},
            {"name": "Eddington ratio", "value": 0.05, "uncertainty": 0.03, "source": "AGN typical"},
            {"name": "NS max mass M_sun", "value": 2.2, "uncertainty": 0.1, "source": "TOV limit"},
        ]
    },
    "condensed-matter": {
        "description": "Condensed matter and materials physics constants",
        "constants": [
            # Melting/stability
            {"name": "Lindemann criterion", "value": 0.15, "uncertainty": 0.05, "source": "Melting"},
            {"name": "Born stability", "value": 0.15, "uncertainty": 0.03, "source": "Elastic"},
            {"name": "Glass T_g/T_m ratio", "value": 0.6, "uncertainty": 0.1, "source": "Amorphous"},
            {"name": "Kauzmann T_K/T_m", "value": 0.75, "uncertainty": 0.1, "source": "Entropy crisis"},
            # Elastic
            {"name": "Poisson ratio typical", "value": 0.30, "uncertainty": 0.05, "source": "Metals"},
            {"name": "Gruneisen parameter", "value": 2.0, "uncertainty": 0.5, "source": "Thermal"},
            # Plasticity
            {"name": "Hall-Petch exponent", "value": 0.5, "uncertainty": 0.1, "source": "Grain size"},
            {"name": "Creep exponent n", "value": 4.0, "uncertainty": 1.0, "source": "Power law"},
            {"name": "Fatigue exponent b", "value": 0.1, "uncertainty": 0.05, "source": "S-N curve"},
            # Percolation (2D square lattice)
            {"name": "Percolation p_c (2D sq)", "value": 0.5928, "uncertainty": 0.0001, "source": "Site"},
            {"name": "Percolation p_c (3D sc)", "value": 0.3116, "uncertainty": 0.0001, "source": "Site"},
            {"name": "Percolation nu (2D)", "value": 4/3, "uncertainty": 0.01, "source": "Correlation"},
            {"name": "Percolation beta (2D)", "value": 5/36, "uncertainty": 0.01, "source": "Order param"},
            # Ising critical exponents (2D)
            {"name": "Ising beta (2D)", "value": 1/8, "uncertainty": 0.001, "source": "Exact"},
            {"name": "Ising gamma (2D)", "value": 7/4, "uncertainty": 0.001, "source": "Exact"},
            {"name": "Ising nu (2D)", "value": 1.0, "uncertainty": 0.001, "source": "Exact"},
            # Superconductivity
            {"name": "BCS gap ratio", "value": 3.5, "uncertainty": 0.1, "source": "2Delta/kT_c"},
            {"name": "London penetration nm", "value": 100, "uncertainty": 50, "source": "Typical"},
            {"name": "Coherence length nm", "value": 50, "uncertainty": 30, "source": "Pair size"},
        ]
    },
    "networks": {
        "description": "Network science and complexity constants",
        "constants": [
            # Degree distributions
            {"name": "Scale-free exponent", "value": 2.5, "uncertainty": 0.5, "source": "Power law"},
            {"name": "Small-world clustering", "value": 0.6, "uncertainty": 0.1, "source": "Local"},
            {"name": "Small-world path", "value": 6, "uncertainty": 1, "source": "Degrees of sep"},
            {"name": "Dunbar number", "value": 150, "uncertainty": 50, "source": "Social group"},
            # Structure
            {"name": "Modularity Q optimal", "value": 0.5, "uncertainty": 0.2, "source": "Community"},
            {"name": "Assortative r", "value": 0.1, "uncertainty": 0.2, "source": "Social positive"},
            {"name": "Rich club coefficient", "value": 1.5, "uncertainty": 0.5, "source": "Hub connect"},
            # Dynamics
            {"name": "Cascade threshold", "value": 0.18, "uncertainty": 0.05, "source": "Failure p_c"},
            {"name": "Epidemic R0 threshold", "value": 1.0, "uncertainty": 0.01, "source": "Spreading"},
            {"name": "Voter consensus exp", "value": 1.0, "uncertainty": 0.1, "source": "Time ~ N"},
            # Game theory
            {"name": "Cooperation threshold", "value": 0.5, "uncertainty": 0.1, "source": "Equilibrium"},
            {"name": "Schelling threshold", "value": 0.35, "uncertainty": 0.1, "source": "Segregation"},
            {"name": "El Farol attendance", "value": 0.6, "uncertainty": 0.05, "source": "Bar problem"},
            # Traffic
            {"name": "Traffic phase rho_c", "value": 0.2, "uncertainty": 0.05, "source": "Congestion"},
            {"name": "Braess factor", "value": 2.0, "uncertainty": 0.5, "source": "Paradox"},
            {"name": "Metcalfe exponent", "value": 2.0, "uncertainty": 0.2, "source": "Network value"},
            # Information
            {"name": "Compression ratio", "value": 0.3, "uncertainty": 0.1, "source": "Text typical"},
            {"name": "Channel capacity", "value": 0.5, "uncertainty": 0.1, "source": "Noisy bit"},
            {"name": "Error threshold", "value": 0.11, "uncertainty": 0.02, "source": "Fault tolerant"},
        ]
    },
    "urban": {
        "description": "Urban scaling and human systems constants",
        "constants": [
            # Urban scaling
            {"name": "Urban pop exponent", "value": 1.15, "uncertainty": 0.05, "source": "Superlinear"},
            {"name": "Infrastructure exponent", "value": 0.85, "uncertainty": 0.05, "source": "Sublinear"},
            {"name": "Crime scaling", "value": 1.16, "uncertainty": 0.05, "source": "Per capita"},
            {"name": "Patent scaling", "value": 1.27, "uncertainty": 0.1, "source": "Innovation"},
            {"name": "GDP scaling", "value": 1.13, "uncertainty": 0.05, "source": "Productivity"},
            # Transport
            {"name": "Walking pace m/s", "value": 1.4, "uncertainty": 0.1, "source": "Urban"},
            {"name": "Marchetti constant min", "value": 30, "uncertainty": 5, "source": "Commute"},
            {"name": "Travel time hr/day", "value": 1.1, "uncertainty": 0.2, "source": "Budget"},
            {"name": "Trip rate /day", "value": 3.5, "uncertainty": 0.5, "source": "Movements"},
            # Economics
            {"name": "Gini coefficient", "value": 0.40, "uncertainty": 0.1, "source": "Inequality"},
            {"name": "Phillips slope", "value": -0.5, "uncertainty": 0.2, "source": "Unemp-inflation"},
            {"name": "Okun coefficient", "value": 2.0, "uncertainty": 0.5, "source": "GDP-unemp"},
            {"name": "Verdoorn coefficient", "value": 0.5, "uncertainty": 0.1, "source": "Productivity"},
            # Adoption
            {"name": "Learning curve exp", "value": 0.25, "uncertainty": 0.05, "source": "Cost reduction"},
            {"name": "S-curve inflection", "value": 0.5, "uncertainty": 0.1, "source": "Technology"},
            {"name": "Bass p (innovation)", "value": 0.03, "uncertainty": 0.01, "source": "Diffusion"},
            {"name": "Bass q (imitation)", "value": 0.38, "uncertainty": 0.05, "source": "Diffusion"},
            {"name": "Engel coefficient", "value": 0.30, "uncertainty": 0.1, "source": "Food spend"},
            {"name": "Price elasticity food", "value": -0.5, "uncertainty": 0.2, "source": "Demand"},
        ]
    },
    "psychology": {
        "description": "Psychology and cognitive science constants",
        "constants": [
            # Memory
            {"name": "Miller number", "value": 7, "uncertainty": 2, "source": "Working memory"},
            {"name": "Ebbinghaus b", "value": 0.5, "uncertainty": 0.1, "source": "Forgetting"},
            {"name": "Learning power exp", "value": 0.4, "uncertainty": 0.1, "source": "Skill"},
            {"name": "Spacing effect ratio", "value": 2.0, "uncertainty": 0.5, "source": "Optimal gap"},
            # Perception
            {"name": "Weber fraction vision", "value": 0.02, "uncertainty": 0.01, "source": "JND"},
            {"name": "Weber fraction weight", "value": 0.05, "uncertainty": 0.02, "source": "JND"},
            {"name": "Stevens brightness", "value": 0.33, "uncertainty": 0.05, "source": "Power law"},
            {"name": "Stevens loudness", "value": 0.67, "uncertainty": 0.05, "source": "Power law"},
            {"name": "Stevens pain", "value": 2.0, "uncertainty": 0.3, "source": "Power law"},
            # Motor
            {"name": "Fitts law a (ms)", "value": 50, "uncertainty": 20, "source": "Intercept"},
            {"name": "Fitts law b (ms/bit)", "value": 150, "uncertainty": 50, "source": "Slope"},
            {"name": "Hick law slope (ms/bit)", "value": 150, "uncertainty": 30, "source": "Choice RT"},
            # Attention
            {"name": "Stroop interference ms", "value": 100, "uncertainty": 30, "source": "Conflict"},
            {"name": "Attentional blink ms", "value": 500, "uncertainty": 100, "source": "Recovery"},
            {"name": "Change blindness rate", "value": 0.5, "uncertainty": 0.1, "source": "Miss prob"},
            # Bias
            {"name": "Overconfidence bias", "value": 0.2, "uncertainty": 0.1, "source": "Calibration"},
            {"name": "Anchoring effect", "value": 0.5, "uncertainty": 0.1, "source": "Adjustment"},
            {"name": "Confirmation bias", "value": 0.7, "uncertainty": 0.1, "source": "Selection"},
            {"name": "Loss aversion ratio", "value": 2.0, "uncertainty": 0.5, "source": "Kahneman"},
        ]
    },
    "chaos-fractals": {
        "description": "Chaos theory and fractal geometry constants",
        "constants": [
            # Feigenbaum constants
            {"name": "Feigenbaum delta", "value": 4.669201, "uncertainty": 0.000001, "source": "Period doubling"},
            {"name": "Feigenbaum alpha", "value": 2.502907, "uncertainty": 0.000001, "source": "Scaling"},
            # Fractal dimensions
            {"name": "Coastline Britain", "value": 1.25, "uncertainty": 0.05, "source": "Richardson"},
            {"name": "Mandelbrot boundary", "value": 2.0, "uncertainty": 0.01, "source": "Area-filling"},
            {"name": "Cantor set dim", "value": math.log(2)/math.log(3), "uncertainty": 0.001, "source": "Exact"},
            {"name": "Sierpinski triangle", "value": math.log(3)/math.log(2), "uncertainty": 0.001, "source": "Exact"},
            {"name": "Koch snowflake", "value": math.log(4)/math.log(3), "uncertainty": 0.001, "source": "Exact"},
            {"name": "Menger sponge", "value": math.log(20)/math.log(3), "uncertainty": 0.001, "source": "Exact"},
            # Time series
            {"name": "Hurst exponent typical", "value": 0.7, "uncertainty": 0.1, "source": "Long memory"},
            {"name": "DFA exponent healthy", "value": 1.0, "uncertainty": 0.1, "source": "Heart rate"},
            {"name": "Lyapunov positive", "value": 0.1, "uncertainty": 0.05, "source": "Chaos typical"},
            # Attractors
            {"name": "Lorenz dim", "value": 2.06, "uncertainty": 0.02, "source": "Strange attractor"},
            {"name": "Henon dim", "value": 1.26, "uncertainty": 0.01, "source": "Map attractor"},
            {"name": "Rossler dim", "value": 2.01, "uncertainty": 0.02, "source": "Attractor"},
            # Universality
            {"name": "Logistic r_chaos", "value": 3.5699, "uncertainty": 0.0001, "source": "Onset"},
            {"name": "Period-3 window", "value": 3.8284, "uncertainty": 0.0001, "source": "Logistic map"},
            {"name": "Intermittency exponent", "value": 0.5, "uncertainty": 0.1, "source": "Type I"},
            {"name": "Crisis exponent", "value": 0.5, "uncertainty": 0.1, "source": "Boundary"},
            {"name": "Escape rate", "value": 0.3, "uncertainty": 0.1, "source": "Transient chaos"},
        ]
    },
    "particle-physics": {
        "description": "Particle physics mass ratios and coupling constants",
        "constants": [
            # Mass ratios
            {"name": "Proton/electron mass", "value": 1836.15, "uncertainty": 0.01, "source": "CODATA"},
            {"name": "Neutron/proton mass", "value": 1.00138, "uncertainty": 0.00001, "source": "CODATA"},
            {"name": "Muon/electron mass", "value": 206.77, "uncertainty": 0.01, "source": "CODATA"},
            {"name": "Tau/electron mass", "value": 3477, "uncertainty": 1, "source": "CODATA"},
            {"name": "W/Z mass ratio", "value": 0.8815, "uncertainty": 0.001, "source": "PDG"},
            {"name": "Higgs/W mass ratio", "value": 1.56, "uncertainty": 0.01, "source": "PDG"},
            {"name": "Top/bottom mass ratio", "value": 41, "uncertainty": 2, "source": "PDG"},
            {"name": "Charm/strange mass ratio", "value": 11.7, "uncertainty": 0.5, "source": "PDG"},
            # Binding energies
            {"name": "Deuteron binding MeV", "value": 2.224, "uncertainty": 0.001, "source": "Nuclear"},
            {"name": "Alpha binding MeV/nucleon", "value": 7.07, "uncertainty": 0.01, "source": "Nuclear"},
            {"name": "Fe-56 binding MeV/nucleon", "value": 8.79, "uncertainty": 0.01, "source": "Most bound"},
            # Decay constants
            {"name": "Neutron lifetime min", "value": 14.7, "uncertainty": 0.1, "source": "Free neutron"},
            {"name": "Muon lifetime us", "value": 2.2, "uncertainty": 0.01, "source": "Decay"},
            {"name": "Pion lifetime ns", "value": 26, "uncertainty": 1, "source": "Charged pion"},
            # Cabibbo angle
            {"name": "sin(Cabibbo)", "value": 0.225, "uncertainty": 0.002, "source": "CKM matrix"},
            {"name": "Cabibbo angle deg", "value": 13.0, "uncertainty": 0.1, "source": "CKM"},
            # CP violation
            {"name": "epsilon_K", "value": 2.228e-3, "uncertainty": 0.01e-3, "source": "Kaon CP"},
            {"name": "sin(2beta)", "value": 0.699, "uncertainty": 0.017, "source": "B meson CP"},
            {"name": "CKM Jarlskog", "value": 3.08e-5, "uncertainty": 0.15e-5, "source": "CP invariant"},
        ]
    },
    "nuclear-magic": {
        "description": "Nuclear magic numbers and shell structure",
        "constants": [
            # Magic numbers (dimensionless)
            {"name": "Magic number 2", "value": 2, "uncertainty": 0.0001, "source": "Helium-4"},
            {"name": "Magic number 8", "value": 8, "uncertainty": 0.0001, "source": "Oxygen-16"},
            {"name": "Magic number 20", "value": 20, "uncertainty": 0.0001, "source": "Calcium-40"},
            {"name": "Magic number 28", "value": 28, "uncertainty": 0.0001, "source": "Nickel-56"},
            {"name": "Magic number 50", "value": 50, "uncertainty": 0.0001, "source": "Tin isotopes"},
            {"name": "Magic number 82", "value": 82, "uncertainty": 0.0001, "source": "Lead-208"},
            {"name": "Magic number 126", "value": 126, "uncertainty": 0.0001, "source": "Lead-208 n"},
            # Magic number ratios
            {"name": "8/2 ratio", "value": 4, "uncertainty": 0.0001, "source": "Shell ratio"},
            {"name": "20/8 ratio", "value": 2.5, "uncertainty": 0.0001, "source": "Shell ratio"},
            {"name": "28/20 ratio", "value": 1.4, "uncertainty": 0.0001, "source": "Shell ratio"},
            {"name": "50/28 ratio", "value": 1.786, "uncertainty": 0.001, "source": "Shell ratio"},
            {"name": "82/50 ratio", "value": 1.64, "uncertainty": 0.001, "source": "Shell ratio"},
            {"name": "126/82 ratio", "value": 1.537, "uncertainty": 0.001, "source": "Shell ratio"},
            # Semi-empirical mass formula
            {"name": "Volume term a_V MeV", "value": 15.8, "uncertainty": 0.3, "source": "SEMF"},
            {"name": "Surface term a_S MeV", "value": 18.3, "uncertainty": 0.3, "source": "SEMF"},
            {"name": "Coulomb term a_C MeV", "value": 0.714, "uncertainty": 0.02, "source": "SEMF"},
            {"name": "Asymmetry term a_A MeV", "value": 23.2, "uncertainty": 0.5, "source": "SEMF"},
            {"name": "Pairing term a_P MeV", "value": 12.0, "uncertainty": 1, "source": "SEMF"},
            {"name": "a_S/a_V ratio", "value": 1.158, "uncertainty": 0.03, "source": "SEMF ratio"},
        ]
    },
    "molecular-geometry": {
        "description": "Molecular bond angles and geometry constants",
        "constants": [
            # Common bond angles
            {"name": "H2O angle deg", "value": 104.5, "uncertainty": 0.1, "source": "Water"},
            {"name": "NH3 angle deg", "value": 107.8, "uncertainty": 0.1, "source": "Ammonia"},
            {"name": "CH4 angle deg", "value": 109.47, "uncertainty": 0.01, "source": "Methane tetrahedral"},
            {"name": "CO2 angle deg", "value": 180.0, "uncertainty": 0.01, "source": "Linear"},
            {"name": "H2S angle deg", "value": 92.1, "uncertainty": 0.1, "source": "Hydrogen sulfide"},
            {"name": "PH3 angle deg", "value": 93.5, "uncertainty": 0.1, "source": "Phosphine"},
            {"name": "SO2 angle deg", "value": 119.0, "uncertainty": 0.5, "source": "Sulfur dioxide"},
            {"name": "NO2 angle deg", "value": 134.3, "uncertainty": 0.5, "source": "Nitrogen dioxide"},
            # Bond angle deviations from ideal
            {"name": "H2O deviation from tet", "value": 109.47 - 104.5, "uncertainty": 0.1, "source": "Computed"},
            {"name": "NH3 deviation from tet", "value": 109.47 - 107.8, "uncertainty": 0.1, "source": "Computed"},
            # Hybridization angles
            {"name": "sp3 angle", "value": 109.47, "uncertainty": 0.01, "source": "Tetrahedral"},
            {"name": "sp2 angle", "value": 120.0, "uncertainty": 0.01, "source": "Trigonal planar"},
            {"name": "sp angle", "value": 180.0, "uncertainty": 0.01, "source": "Linear"},
            # Dihedral angles
            {"name": "Gauche dihedral", "value": 60, "uncertainty": 5, "source": "Alkane conformation"},
            {"name": "Anti dihedral", "value": 180, "uncertainty": 1, "source": "Alkane conformation"},
            {"name": "Eclipsed barrier kcal", "value": 3.0, "uncertainty": 0.3, "source": "Ethane"},
            {"name": "Peptide omega angle", "value": 180, "uncertainty": 5, "source": "Trans peptide"},
            {"name": "Protein phi typical", "value": -60, "uncertainty": 20, "source": "Alpha helix"},
            {"name": "Protein psi typical", "value": -45, "uncertainty": 20, "source": "Alpha helix"},
        ]
    },
    "critical-phenomena": {
        "description": "Critical exponents and phase transition universality",
        "constants": [
            # Mean field exponents
            {"name": "MF alpha", "value": 0, "uncertainty": 0.001, "source": "Heat capacity"},
            {"name": "MF beta", "value": 0.5, "uncertainty": 0.001, "source": "Order parameter"},
            {"name": "MF gamma", "value": 1.0, "uncertainty": 0.001, "source": "Susceptibility"},
            {"name": "MF delta", "value": 3.0, "uncertainty": 0.001, "source": "Critical isotherm"},
            {"name": "MF nu", "value": 0.5, "uncertainty": 0.001, "source": "Correlation length"},
            {"name": "MF eta", "value": 0, "uncertainty": 0.001, "source": "Anomalous dimension"},
            # 3D Ising exponents
            {"name": "3D Ising alpha", "value": 0.110, "uncertainty": 0.003, "source": "Heat capacity"},
            {"name": "3D Ising beta", "value": 0.326, "uncertainty": 0.002, "source": "Magnetization"},
            {"name": "3D Ising gamma", "value": 1.237, "uncertainty": 0.003, "source": "Susceptibility"},
            {"name": "3D Ising delta", "value": 4.79, "uncertainty": 0.02, "source": "Critical isotherm"},
            {"name": "3D Ising nu", "value": 0.630, "uncertainty": 0.002, "source": "Correlation"},
            {"name": "3D Ising eta", "value": 0.036, "uncertainty": 0.002, "source": "Anomalous"},
            # 3D XY (superfluid) exponents
            {"name": "3D XY alpha", "value": -0.015, "uncertainty": 0.005, "source": "He-4 lambda"},
            {"name": "3D XY beta", "value": 0.348, "uncertainty": 0.002, "source": "Superfluid"},
            {"name": "3D XY nu", "value": 0.671, "uncertainty": 0.002, "source": "Correlation"},
            # 3D Heisenberg exponents
            {"name": "3D Heisenberg beta", "value": 0.365, "uncertainty": 0.003, "source": "Ferromagnet"},
            {"name": "3D Heisenberg gamma", "value": 1.386, "uncertainty": 0.004, "source": "Susceptibility"},
            {"name": "3D Heisenberg nu", "value": 0.707, "uncertainty": 0.003, "source": "Correlation"},
            # Scaling relations (exact)
            {"name": "alpha + 2*beta + gamma", "value": 2.0, "uncertainty": 0.001, "source": "Rushbrooke"},
        ]
    },
    "quantum-hall": {
        "description": "Quantum Hall effect filling fractions",
        "constants": [
            # Integer QHE
            {"name": "IQHE nu=1", "value": 1, "uncertainty": 0.0001, "source": "Integer"},
            {"name": "IQHE nu=2", "value": 2, "uncertainty": 0.0001, "source": "Integer"},
            {"name": "IQHE nu=3", "value": 3, "uncertainty": 0.0001, "source": "Integer"},
            # Principal Laughlin fractions
            {"name": "Laughlin 1/3", "value": 1/3, "uncertainty": 0.0001, "source": "FQHE"},
            {"name": "Laughlin 1/5", "value": 1/5, "uncertainty": 0.0001, "source": "FQHE"},
            {"name": "Laughlin 1/7", "value": 1/7, "uncertainty": 0.0001, "source": "FQHE"},
            # Jain sequence (p/(2p+1))
            {"name": "Jain 2/5", "value": 2/5, "uncertainty": 0.0001, "source": "Composite fermion"},
            {"name": "Jain 3/7", "value": 3/7, "uncertainty": 0.0001, "source": "Composite fermion"},
            {"name": "Jain 4/9", "value": 4/9, "uncertainty": 0.0001, "source": "Composite fermion"},
            # Jain sequence (p/(2p-1))
            {"name": "Jain 2/3", "value": 2/3, "uncertainty": 0.0001, "source": "Composite fermion"},
            {"name": "Jain 3/5", "value": 3/5, "uncertainty": 0.0001, "source": "Composite fermion"},
            {"name": "Jain 4/7", "value": 4/7, "uncertainty": 0.0001, "source": "Composite fermion"},
            # Even-denominator (non-Abelian)
            {"name": "Moore-Read 5/2", "value": 5/2, "uncertainty": 0.0001, "source": "Non-Abelian"},
            {"name": "Read-Rezayi 12/5", "value": 12/5, "uncertainty": 0.0001, "source": "Parafermion"},
            # Hall resistance quantum
            {"name": "R_K (h/e^2) kOhm", "value": 25.813, "uncertainty": 0.001, "source": "von Klitzing"},
            {"name": "R_K / R_0 ratio", "value": 25.813/25, "uncertainty": 0.001, "source": "Near integer"},
            {"name": "Flux quantum (h/e)", "value": 4.136e-15, "uncertainty": 1e-18, "source": "Weber"},
            {"name": "Flux quantum (h/2e)", "value": 2.068e-15, "uncertainty": 1e-18, "source": "SC flux"},
            {"name": "e^2/h conductance", "value": 3.874e-5, "uncertainty": 1e-8, "source": "Siemens"},
        ]
    },
    "biological-ratios": {
        "description": "Biological and biochemical ratios",
        "constants": [
            # DNA/RNA
            {"name": "DNA base pair rise nm", "value": 0.34, "uncertainty": 0.01, "source": "B-DNA"},
            {"name": "DNA helix pitch nm", "value": 3.4, "uncertainty": 0.1, "source": "B-DNA"},
            {"name": "DNA bp per turn", "value": 10.5, "uncertainty": 0.5, "source": "B-DNA"},
            {"name": "DNA major groove nm", "value": 2.2, "uncertainty": 0.1, "source": "B-DNA"},
            {"name": "DNA minor groove nm", "value": 1.2, "uncertainty": 0.1, "source": "B-DNA"},
            {"name": "Major/minor groove", "value": 2.2/1.2, "uncertainty": 0.1, "source": "Ratio"},
            # Protein structure
            {"name": "Alpha helix rise nm", "value": 0.15, "uncertainty": 0.01, "source": "Per residue"},
            {"name": "Alpha helix pitch nm", "value": 0.54, "uncertainty": 0.02, "source": "Per turn"},
            {"name": "Alpha helix residues/turn", "value": 3.6, "uncertainty": 0.1, "source": "Structure"},
            {"name": "Beta sheet rise nm", "value": 0.35, "uncertainty": 0.02, "source": "Per residue"},
            {"name": "Ramachandran allowed %", "value": 0.25, "uncertainty": 0.05, "source": "Phi-psi space"},
            # Cell biology
            {"name": "Membrane thickness nm", "value": 7.5, "uncertainty": 0.5, "source": "Lipid bilayer"},
            {"name": "ATP molecules per glucose", "value": 36, "uncertainty": 2, "source": "Oxidative"},
            {"name": "Krebs cycle ATP", "value": 2, "uncertainty": 0.1, "source": "Per cycle"},
            {"name": "ETC ATP per NADH", "value": 2.5, "uncertainty": 0.2, "source": "Electron transport"},
            {"name": "ETC ATP per FADH2", "value": 1.5, "uncertainty": 0.2, "source": "Electron transport"},
            # Enzyme kinetics
            {"name": "Typical k_cat /s", "value": 1000, "uncertainty": 500, "source": "Turnover"},
            {"name": "Typical K_M mM", "value": 0.1, "uncertainty": 0.05, "source": "Michaelis"},
            {"name": "Catalytic perfection", "value": 1e8, "uncertainty": 5e7, "source": "k_cat/K_M limit"},
        ]
    },
    "geomorphology": {
        "description": "Geomorphology and landform scaling",
        "constants": [
            # Erosion
            {"name": "Denudation rate mm/kyr", "value": 50, "uncertainty": 30, "source": "Global mean"},
            {"name": "Soil production mm/kyr", "value": 30, "uncertainty": 20, "source": "Equilibrium"},
            {"name": "Weathering exp", "value": 0.4, "uncertainty": 0.1, "source": "Temp dependence"},
            # Rivers
            {"name": "Manning n typical", "value": 0.035, "uncertainty": 0.01, "source": "Natural channel"},
            {"name": "Width/depth ratio", "value": 10, "uncertainty": 5, "source": "Alluvial"},
            {"name": "Sinuosity typical", "value": 1.5, "uncertainty": 0.3, "source": "Meandering"},
            {"name": "Meander wavelength/width", "value": 10, "uncertainty": 2, "source": "Scaling"},
            {"name": "Pool spacing/width", "value": 6, "uncertainty": 2, "source": "Riffle-pool"},
            # Slopes
            {"name": "Threshold hillslope deg", "value": 35, "uncertainty": 5, "source": "Angle of repose"},
            {"name": "Relief ratio", "value": 0.1, "uncertainty": 0.05, "source": "Typical basin"},
            {"name": "Hypsometric integral", "value": 0.5, "uncertainty": 0.1, "source": "Mature landscape"},
            # Glacial
            {"name": "Cirque aspect ratio", "value": 3, "uncertainty": 1, "source": "Width/height"},
            {"name": "Glacier AAR", "value": 0.65, "uncertainty": 0.1, "source": "Equilibrium"},
            {"name": "Debris cover fraction", "value": 0.3, "uncertainty": 0.1, "source": "Himalayan"},
            # Coastal
            {"name": "Beach slope deg", "value": 5, "uncertainty": 2, "source": "Sandy"},
            {"name": "Bruun rule factor", "value": 100, "uncertainty": 50, "source": "SLR response"},
            {"name": "Cliff retreat m/yr", "value": 0.1, "uncertainty": 0.05, "source": "Typical"},
            {"name": "Barrier migration rate", "value": 1, "uncertainty": 0.5, "source": "m/yr"},
            {"name": "Delta progradation km/kyr", "value": 0.5, "uncertainty": 0.3, "source": "Large rivers"},
        ]
    },
    "acoustics-music": {
        "description": "Acoustics and musical interval ratios",
        "constants": [
            # Just intonation intervals
            {"name": "Octave ratio", "value": 2, "uncertainty": 0.0001, "source": "Harmonic"},
            {"name": "Perfect fifth 3/2", "value": 3/2, "uncertainty": 0.0001, "source": "Harmonic"},
            {"name": "Perfect fourth 4/3", "value": 4/3, "uncertainty": 0.0001, "source": "Harmonic"},
            {"name": "Major third 5/4", "value": 5/4, "uncertainty": 0.0001, "source": "Harmonic"},
            {"name": "Minor third 6/5", "value": 6/5, "uncertainty": 0.0001, "source": "Harmonic"},
            {"name": "Major sixth 5/3", "value": 5/3, "uncertainty": 0.0001, "source": "Harmonic"},
            {"name": "Minor sixth 8/5", "value": 8/5, "uncertainty": 0.0001, "source": "Harmonic"},
            {"name": "Major second 9/8", "value": 9/8, "uncertainty": 0.0001, "source": "Harmonic"},
            {"name": "Minor second 16/15", "value": 16/15, "uncertainty": 0.0001, "source": "Harmonic"},
            # Equal temperament
            {"name": "ET semitone", "value": 2**(1/12), "uncertainty": 0.0001, "source": "12-TET"},
            {"name": "ET fifth", "value": 2**(7/12), "uncertainty": 0.0001, "source": "12-TET"},
            {"name": "ET major third", "value": 2**(4/12), "uncertainty": 0.0001, "source": "12-TET"},
            {"name": "Pythagorean comma", "value": (3/2)**12 / 2**7, "uncertainty": 0.0001, "source": "Spiral of fifths"},
            {"name": "Syntonic comma", "value": 81/80, "uncertainty": 0.0001, "source": "5-limit"},
            # Room acoustics
            {"name": "RT60 typical s", "value": 0.5, "uncertainty": 0.2, "source": "Living room"},
            {"name": "Concert hall RT60", "value": 2.0, "uncertainty": 0.3, "source": "Symphony"},
            {"name": "Speech clarity C50 dB", "value": 2, "uncertainty": 1, "source": "Good speech"},
            {"name": "Critical distance ratio", "value": 0.3, "uncertainty": 0.1, "source": "Room acoustics"},
            {"name": "A-weighting 1kHz factor", "value": 1.0, "uncertainty": 0.01, "source": "Reference"},
        ]
    },
    "optics-vision": {
        "description": "Optics and human vision constants",
        "constants": [
            # Human eye
            {"name": "Eye focal length mm", "value": 17, "uncertainty": 1, "source": "Relaxed"},
            {"name": "Pupil min diameter mm", "value": 2, "uncertainty": 0.5, "source": "Bright light"},
            {"name": "Pupil max diameter mm", "value": 8, "uncertainty": 1, "source": "Dark adapted"},
            {"name": "Pupil range ratio", "value": 4, "uncertainty": 0.5, "source": "Max/min"},
            {"name": "Accommodation range D", "value": 10, "uncertainty": 2, "source": "Young adult"},
            {"name": "Rod/cone ratio", "value": 20, "uncertainty": 5, "source": "120M/6M"},
            {"name": "Foveal cone spacing um", "value": 2.5, "uncertainty": 0.5, "source": "Center"},
            {"name": "Visual angle resolution min", "value": 1, "uncertainty": 0.2, "source": "Arc minute"},
            # Color vision
            {"name": "L cone peak nm", "value": 564, "uncertainty": 5, "source": "Red"},
            {"name": "M cone peak nm", "value": 534, "uncertainty": 5, "source": "Green"},
            {"name": "S cone peak nm", "value": 420, "uncertainty": 5, "source": "Blue"},
            {"name": "Rod peak nm", "value": 498, "uncertainty": 5, "source": "Scotopic"},
            {"name": "Luminous efficacy max lm/W", "value": 683, "uncertainty": 1, "source": "555nm"},
            # Refractive indices
            {"name": "Water n", "value": 1.333, "uncertainty": 0.001, "source": "Visible"},
            {"name": "Glass crown n", "value": 1.52, "uncertainty": 0.01, "source": "Typical"},
            {"name": "Diamond n", "value": 2.42, "uncertainty": 0.01, "source": "Visible"},
            {"name": "Eye cornea n", "value": 1.376, "uncertainty": 0.005, "source": "Physiological"},
            {"name": "Eye lens n", "value": 1.406, "uncertainty": 0.005, "source": "Physiological"},
            {"name": "Critical angle diamond deg", "value": 24.4, "uncertainty": 0.1, "source": "TIR"},
        ]
    },
    "information-entropy": {
        "description": "Information theory and entropy constants",
        "constants": [
            # Entropy bounds
            {"name": "Binary entropy H(0.5)", "value": 1.0, "uncertainty": 0.0001, "source": "Max bits"},
            {"name": "Nat/bit conversion", "value": math.log(2), "uncertainty": 0.0001, "source": "ln(2)"},
            {"name": "English entropy bit/char", "value": 1.3, "uncertainty": 0.2, "source": "Shannon"},
            {"name": "English redundancy", "value": 0.75, "uncertainty": 0.05, "source": "Shannon"},
            # Channel capacity
            {"name": "Shannon limit dB", "value": -1.6, "uncertainty": 0.1, "source": "Eb/N0"},
            {"name": "Capacity approach factor", "value": 0.9, "uncertainty": 0.05, "source": "Modern codes"},
            # Compression
            {"name": "Huffman efficiency", "value": 0.95, "uncertainty": 0.03, "source": "Typical"},
            {"name": "LZ77 compression ratio", "value": 0.4, "uncertainty": 0.1, "source": "Text"},
            {"name": "JPEG quality factor", "value": 0.1, "uncertainty": 0.05, "source": "10:1 photo"},
            {"name": "Video compression ratio", "value": 0.01, "uncertainty": 0.005, "source": "H.264"},
            # Kolmogorov complexity
            {"name": "Random incompressible", "value": 1.0, "uncertainty": 0.001, "source": "AIT"},
            {"name": "Computable fraction", "value": 0, "uncertainty": 0.001, "source": "Measure 0"},
            # Error correction
            {"name": "Hamming (7,4) rate", "value": 4/7, "uncertainty": 0.001, "source": "Code rate"},
            {"name": "Reed-Solomon typical rate", "value": 0.8, "uncertainty": 0.05, "source": "CD/DVD"},
            {"name": "Turbo code rate", "value": 0.5, "uncertainty": 0.1, "source": "Near capacity"},
            {"name": "LDPC typical rate", "value": 0.9, "uncertainty": 0.05, "source": "5G"},
            # Mutual information
            {"name": "Correlation coefficient r", "value": 0.5, "uncertainty": 0.2, "source": "Typical"},
            {"name": "MI for Gaussian", "value": 0.5, "uncertainty": 0.1, "source": "-0.5*log(1-r^2)"},
            {"name": "Transfer entropy typical", "value": 0.1, "uncertainty": 0.05, "source": "Causal"},
        ]
    }
}


def find_topic(query: str) -> str:
    """Match query to known topic."""
    query_lower = query.lower()

    # Direct matches
    if "eddington" in query_lower or "luminosity" in query_lower or "stellar" in query_lower:
        return "eddington"
    if "roche" in query_lower or "tidal" in query_lower:
        return "roche"
    if "titius" in query_lower or "bode" in query_lower or "planetary" in query_lower:
        return "titius-bode"
    if "geodynamo" in query_lower or "magnetic reynolds" in query_lower or "dynamo" in query_lower:
        return "geodynamo"
    if "golden" in query_lower or "fibonacci" in query_lower:
        return "golden"
    if "snowflake" in query_lower or "ice crystal" in query_lower or "ice ih" in query_lower:
        return "snowflake"
    if "turbulence" in query_lower or "karman" in query_lower or "kármán" in query_lower or "strouhal" in query_lower or "reynolds" in query_lower:
        return "turbulence"
    if "river" in query_lower or "hack" in query_lower or "horton" in query_lower or "drainage" in query_lower or "stream" in query_lower or "bifurcation" in query_lower:
        return "river-network"
    if "earthquake" in query_lower or "aftershock" in query_lower or "omori" in query_lower or "seism" in query_lower or "gutenberg" in query_lower or "richter" in query_lower or "båth" in query_lower or "bath" in query_lower:
        return "earthquake-aftershock"
    if "kleiber" in query_lower or "metabolic" in query_lower or "allometric" in query_lower or "quarter-power" in query_lower or "3/4 law" in query_lower:
        return "kleiber"
    if "zipf" in query_lower or "pareto" in query_lower or "benford" in query_lower or "heaps" in query_lower or "power law" in query_lower or "word frequency" in query_lower:
        return "zipf"
    if "fluid-advanced" in query_lower or "drag coefficient" in query_lower or "rayleigh number" in query_lower or "taylor number" in query_lower or "blasius" in query_lower:
        return "fluid-advanced"
    if "geophysics" in query_lower or "planetary" in query_lower or "oblateness" in query_lower or "chandler" in query_lower or "plate tectonics" in query_lower or "mantle" in query_lower:
        return "geophysics-planetary"
    if "atmospheric" in query_lower or "climate" in query_lower or "lapse rate" in query_lower or "tropopause" in query_lower or "albedo" in query_lower or "sensitivity" in query_lower:
        return "atmospheric"
    if "ocean" in query_lower or "ekman" in query_lower or "thermocline" in query_lower or "thermohaline" in query_lower or "tidal" in query_lower or "wave" in query_lower:
        return "oceanography"
    if "physiology" in query_lower or "cardiac" in query_lower or "respir" in query_lower or "blood" in query_lower or "neural" in query_lower or "lifespan" in query_lower:
        return "physiology"
    if "ecology" in query_lower or "species-area" in query_lower or "trophic" in query_lower or "food web" in query_lower or "extinction" in query_lower or "biodiversity" in query_lower:
        return "ecology"
    if "cosmolog" in query_lower or "fine structure" in query_lower or "dark energy" in query_lower or "dark matter" in query_lower or "hubble" in query_lower or "cmb" in query_lower or "primordial" in query_lower:
        return "cosmology"
    if "condensed" in query_lower or "lindemann" in query_lower or "percolation" in query_lower or "ising" in query_lower or "superconducti" in query_lower or "bcs" in query_lower or "glass transition" in query_lower:
        return "condensed-matter"
    if "network" in query_lower or "scale-free" in query_lower or "small-world" in query_lower or "dunbar" in query_lower or "cascade" in query_lower or "epidemic" in query_lower:
        return "networks"
    if "urban" in query_lower or "city" in query_lower or "commute" in query_lower or "gini" in query_lower or "infrastructure" in query_lower or "innovation" in query_lower:
        return "urban"
    if "psychology" in query_lower or "cogniti" in query_lower or "memory" in query_lower or "perception" in query_lower or "weber" in query_lower or "stevens" in query_lower or "fitts" in query_lower:
        return "psychology"
    if "chaos" in query_lower or "fractal" in query_lower or "feigenbaum" in query_lower or "lorenz" in query_lower or "mandelbrot" in query_lower or "hurst" in query_lower or "lyapunov" in query_lower:
        return "chaos-fractals"
    if "particle" in query_lower or "proton" in query_lower or "neutron" in query_lower or "muon" in query_lower or "cabibbo" in query_lower or "ckm" in query_lower:
        return "particle-physics"
    if "nuclear" in query_lower or "magic number" in query_lower or "shell" in query_lower or "binding energy" in query_lower or "semf" in query_lower:
        return "nuclear-magic"
    if "molecular" in query_lower or "bond angle" in query_lower or "hybridization" in query_lower or "dihedral" in query_lower or "peptide" in query_lower:
        return "molecular-geometry"
    if "critical exponent" in query_lower or "phase transition" in query_lower or "universality" in query_lower or "mean field" in query_lower or "heisenberg" in query_lower:
        return "critical-phenomena"
    if "quantum hall" in query_lower or "laughlin" in query_lower or "fqhe" in query_lower or "filling fraction" in query_lower or "von klitzing" in query_lower:
        return "quantum-hall"
    if "biological ratio" in query_lower or "dna" in query_lower or "protein structure" in query_lower or "enzyme" in query_lower or "atp" in query_lower:
        return "biological-ratios"
    if "geomorphology" in query_lower or "erosion" in query_lower or "landform" in query_lower or "hillslope" in query_lower or "meander" in query_lower or "glacier" in query_lower:
        return "geomorphology"
    if "acoustic" in query_lower or "music" in query_lower or "interval" in query_lower or "temperament" in query_lower or "harmonic" in query_lower:
        return "acoustics-music"
    if "optic" in query_lower or "vision" in query_lower or "eye" in query_lower or "refractive" in query_lower or "cone" in query_lower or "rod" in query_lower:
        return "optics-vision"
    if "information" in query_lower or "entropy" in query_lower or "shannon" in query_lower or "compression" in query_lower or "error correct" in query_lower:
        return "information-entropy"

    # Default to eddington for astrophysics queries
    if any(w in query_lower for w in ["black hole", "accretion", "thomson", "kerr"]):
        return "eddington"

    return None


def run_discovery(query: str, verbose: bool = True, timeout: float = 60) -> Dict[str, Any]:
    """
    Run full discovery pipeline on a simple query.

    Args:
        query: Natural language question (e.g., "Eddington luminosity ratio")
        verbose: Print progress
        timeout: Search timeout in seconds

    Returns:
        Full results dict
    """
    print("=" * 70)
    print("Z² DISCOVERY ENGINE")
    print("=" * 70)
    print(f"\nQuery: {query}")
    print()

    # 1. Find relevant topic
    topic = find_topic(query)
    if not topic:
        print(f"Unknown topic. Available: {list(TOPIC_KNOWLEDGE.keys())}")
        return {"error": "Unknown topic"}

    topic_data = TOPIC_KNOWLEDGE[topic]
    print(f"Topic: {topic}")
    print(f"Description: {topic_data['description']}")
    print(f"Constants to search: {len(topic_data['constants'])}")
    print()

    # 2. Build search targets
    targets = []
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
        targets.append(target)
        if verbose:
            print(f"  {const['name']:40} = {const['value']:.6f}")

    print()

    # 3. Run BriareusFlow
    print("-" * 70)
    print("PHASE 1: BriareusFlow Brute-Force Search")
    print("-" * 70)

    config = SearchConfig(
        max_error_percent=1.0,
        max_integer=50,
        max_denominator=50,
        num_threads=8,
        verbose=verbose,
        log_every_n=2
    )

    controller = BriareusController(config)
    controller.add_targets(targets)

    briareus_result = controller.run(timeout=timeout)

    print(f"\nBriareusFlow complete:")
    print(f"  Targets processed: {briareus_result.targets_processed}")
    print(f"  Total findings: {briareus_result.findings_total}")
    print(f"  Z² patterns: {briareus_result.z2_patterns_found}")
    print(f"  Runtime: {briareus_result.runtime_seconds:.1f}s")

    # 4. Get Z² findings
    z2_findings = controller.get_z2_findings()
    promising = controller.get_promising_findings()

    # 5. Integrate with OlympusFlow
    print()
    print("-" * 70)
    print("PHASE 2: OlympusFlow Integration")
    print("-" * 70)

    integration = integrate_with_olympusflow(briareus_result)
    print(f"  Promoted to OlympusFlow: {integration['summary']['promoted']}")
    print(f"  Z² candidates: {integration['summary']['z2_candidates']}")

    # 6. Report results
    print()
    print("=" * 70)
    print("DISCOVERY RESULTS")
    print("=" * 70)

    # Group findings by target
    by_target = {}
    for f in controller.all_findings:
        if f.name not in by_target:
            by_target[f.name] = []
        by_target[f.name].append(f)

    print("\nBEST MATCHES PER CONSTANT:")
    print("-" * 70)

    for target_name, findings in sorted(by_target.items()):
        best = min(findings, key=lambda x: x.percent_error)
        z2_marker = " [Z²]" if "Z²" in best.formula or "Z^2" in best.formula else ""
        pi_marker = " [π]" if "π" in best.formula else ""

        print(f"\n{target_name}")
        print(f"  Experimental: {best.experimental_value:.6f}")
        print(f"  Best match:   {best.formula} = {best.computed_value:.6f}{z2_marker}{pi_marker}")
        print(f"  Error:        {best.percent_error:.4f}%")

        # Show alternatives
        alts = sorted(findings, key=lambda x: x.percent_error)[1:4]
        if alts:
            print(f"  Alternatives: ", end="")
            print(", ".join(f"{a.formula}" for a in alts))

    # Z² specific findings
    if z2_findings:
        print()
        print("-" * 70)
        print("Z² PATTERN DISCOVERIES")
        print("-" * 70)
        for f in z2_findings[:10]:
            print(f"  {f.name}: {f.formula} = {f.computed_value:.6f} ({f.percent_error:.4f}%)")

    # Check for Z² connections
    print()
    print("-" * 70)
    print("Z² CONNECTION ANALYSIS")
    print("-" * 70)
    print(f"Z² = 32π/3 ≈ {Z_SQUARED:.6f}")
    print(f"Z = √(32π/3) ≈ {Z:.6f}")

    # Look for interesting ratios with Z²
    for target_name, findings in by_target.items():
        best = min(findings, key=lambda x: x.percent_error)
        value = best.experimental_value

        # Check ratio with Z²
        ratio = value / Z_SQUARED if value > 1 else Z_SQUARED / value
        inv_ratio = Z_SQUARED / value if value > 1 else value / Z_SQUARED

        # Check if ratio is close to a simple fraction
        for a in range(1, 20):
            for b in range(1, 20):
                if abs(ratio - a/b) / ratio < 0.01:
                    print(f"  {target_name}: value × {b}/{a} ≈ Z²")
                if abs(inv_ratio - a/b) / inv_ratio < 0.01:
                    print(f"  {target_name}: Z² × {b}/{a} ≈ value")

    print()
    print("=" * 70)
    print("DISCOVERY COMPLETE")
    print("=" * 70)

    return {
        "query": query,
        "topic": topic,
        "briareus_result": briareus_result,
        "z2_findings": z2_findings,
        "promising_findings": promising,
        "olympus_integration": integration,
        "by_target": by_target
    }


async def run_web_research(query: str, verbose: bool = True, timeout: float = 60) -> Dict[str, Any]:
    """
    Run discovery with web research via HermesFlow ResearchBridge.

    This is used for topics not in the hardcoded TOPIC_KNOWLEDGE.
    It uses HermesFlow web tools to search for scientific data.

    Args:
        query: Topic to research
        verbose: Print progress
        timeout: Search timeout

    Returns:
        Full results dict
    """
    if not RESEARCH_BRIDGE_AVAILABLE:
        print("Error: HermesFlow ResearchBridge not available")
        print("Install HermesFlow or use a known topic from TOPIC_KNOWLEDGE")
        return {"error": "ResearchBridge not available"}

    # Use the automated discovery pipeline
    return await run_automated_discovery(query, timeout=timeout, verbose=verbose)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Z² Discovery Engine")
    parser.add_argument("query", nargs="?", default="Eddington luminosity ratio",
                        help="Topic to research (e.g., 'Eddington luminosity ratio')")
    parser.add_argument("--timeout", type=float, default=60, help="Search timeout")
    parser.add_argument("--quiet", action="store_true", help="Less output")
    parser.add_argument("--research", action="store_true",
                        help="Use HermesFlow web research for unknown topics")

    args = parser.parse_args()

    # Check if topic is in knowledge base
    topic = find_topic(args.query)

    if topic:
        # Use hardcoded knowledge base
        run_discovery(args.query, verbose=not args.quiet, timeout=args.timeout)
    elif args.research and RESEARCH_BRIDGE_AVAILABLE:
        # Use web research
        print(f"Topic not in knowledge base, using HermesFlow web research...")
        asyncio.run(run_web_research(args.query, verbose=not args.quiet, timeout=args.timeout))
    else:
        print(f"Unknown topic: {args.query}")
        print(f"Available topics: {list(TOPIC_KNOWLEDGE.keys())}")
        if RESEARCH_BRIDGE_AVAILABLE:
            print(f"\nTip: Use --research to search the web for unknown topics")
        else:
            print(f"\nNote: Install HermesFlow to enable web research for unknown topics")
