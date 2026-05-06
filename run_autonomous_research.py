#!/usr/bin/env python3
"""
Z² AUTONOMOUS RESEARCH RUNNER
==============================

Processes 500+ research topics automatically using embedded knowledge:
1. Look up known constants for each topic
2. BriareusFlow → brute-force pattern matching
3. Save all findings

This version uses embedded knowledge for speed (no LLM queries per topic).

Usage:
    python run_autonomous_research.py                    # Run all topics
    python run_autonomous_research.py --domain cosmology # Run specific domain
    python run_autonomous_research.py --priority 1       # Run priority 1 only
    python run_autonomous_research.py --limit 50         # Run first 50 topics

Author: Carl Zimmerman
Date: May 6, 2026
"""

import os
import sys
import json
import time
import math
import re
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict, field

# Import research topics
from research_topics import (
    RESEARCH_TOPICS,
    ResearchTopic,
    get_topics_by_domain,
    get_topics_by_priority,
    get_all_domains
)

# Import BriareusFlow pattern search
from BriareusFlow import (
    PatternSearchEngine,
    SearchResult,
    PatternMatch,
    Z_SQUARED,
    Z
)

# Constants
OUTPUT_DIR = Path("OlympusFlow/discoveries/autonomous_research")
SUMMARY_FILE = OUTPUT_DIR / "research_summary.json"

# Z² constants
Z2 = 32 * math.pi / 3  # ≈ 33.51


# =============================================================================
# EMBEDDED KNOWLEDGE BASE
# =============================================================================

# This maps topic keywords to known numerical constants
# Format: { "keyword": [{"name": ..., "value": ..., "uncertainty": ..., "source": ...}] }

EMBEDDED_CONSTANTS = {
    # PARTICLE PHYSICS
    "fine structure": [
        {"name": "Fine structure constant inverse 1/α", "value": 137.035999, "uncertainty": 0.000001, "source": "CODATA 2018"},
        {"name": "Fine structure constant α", "value": 0.0072973525693, "uncertainty": 0.0000000011, "source": "CODATA 2018"},
    ],
    "weak mixing angle": [
        {"name": "sin²θ_W (on-shell)", "value": 0.22290, "uncertainty": 0.00030, "source": "PDG 2024"},
        {"name": "sin²θ_W (MS-bar)", "value": 0.23122, "uncertainty": 0.00004, "source": "PDG 2024"},
    ],
    "proton electron mass": [
        {"name": "Proton/electron mass ratio", "value": 1836.15267343, "uncertainty": 0.00000011, "source": "CODATA 2018"},
    ],
    "neutron proton mass": [
        {"name": "Neutron/proton mass ratio", "value": 1.00137842, "uncertainty": 0.00000001, "source": "CODATA"},
    ],
    "muon electron mass": [
        {"name": "Muon/electron mass ratio", "value": 206.7682830, "uncertainty": 0.0000046, "source": "CODATA"},
    ],
    "w boson z boson": [
        {"name": "W/Z mass ratio", "value": 0.88145, "uncertainty": 0.00013, "source": "PDG"},
        {"name": "cos θ_W", "value": 0.88145, "uncertainty": 0.0002, "source": "PDG"},
    ],
    "higgs boson": [
        {"name": "Higgs mass (GeV)", "value": 125.25, "uncertainty": 0.17, "source": "ATLAS+CMS"},
        {"name": "Higgs/W mass ratio", "value": 125.25/80.379, "uncertainty": 0.01, "source": "PDG"},
    ],
    "cabibbo angle": [
        {"name": "sin θ_c (Cabibbo)", "value": 0.22452, "uncertainty": 0.00044, "source": "PDG"},
        {"name": "cos θ_c (Cabibbo)", "value": 0.97434, "uncertainty": 0.00011, "source": "PDG"},
    ],
    "neutron lifetime": [
        {"name": "Neutron lifetime (seconds)", "value": 879.4, "uncertainty": 0.6, "source": "PDG 2024"},
    ],
    "muon lifetime": [
        {"name": "Muon lifetime (μs)", "value": 2.1969811, "uncertainty": 0.0000022, "source": "PDG"},
    ],
    "deuteron binding": [
        {"name": "Deuteron binding energy (MeV)", "value": 2.224566, "uncertainty": 0.000001, "source": "CODATA"},
    ],

    # NUCLEAR PHYSICS
    "nuclear magic": [
        {"name": "Magic number 2", "value": 2, "uncertainty": 0, "source": "Nuclear shell model"},
        {"name": "Magic number 8", "value": 8, "uncertainty": 0, "source": "Nuclear shell model"},
        {"name": "Magic number 20", "value": 20, "uncertainty": 0, "source": "Nuclear shell model"},
        {"name": "Magic number 28", "value": 28, "uncertainty": 0, "source": "Nuclear shell model"},
        {"name": "Magic number 50", "value": 50, "uncertainty": 0, "source": "Nuclear shell model"},
        {"name": "Magic number 82", "value": 82, "uncertainty": 0, "source": "Nuclear shell model"},
        {"name": "Magic number 126", "value": 126, "uncertainty": 0, "source": "Nuclear shell model"},
        {"name": "126/82 ratio", "value": 126/82, "uncertainty": 0.001, "source": "Computed"},
    ],
    "nuclear binding": [
        {"name": "Fe-56 binding energy per nucleon (MeV)", "value": 8.79, "uncertainty": 0.01, "source": "Nuclear data"},
        {"name": "Maximum binding per nucleon (MeV)", "value": 8.79, "uncertainty": 0.01, "source": "Nuclear data"},
    ],
    "nuclear radius": [
        {"name": "Nuclear radius constant r0 (fm)", "value": 1.25, "uncertainty": 0.02, "source": "Nuclear physics"},
    ],

    # COSMOLOGY
    "dark energy omega lambda": [
        {"name": "Ω_Λ (dark energy density)", "value": 0.685, "uncertainty": 0.007, "source": "Planck 2018"},
        {"name": "Ω_Λ (Planck 2020)", "value": 0.6889, "uncertainty": 0.0056, "source": "Planck 2020"},
    ],
    "dark matter omega": [
        {"name": "Ω_DM (dark matter)", "value": 0.265, "uncertainty": 0.007, "source": "Planck 2018"},
    ],
    "baryon density omega": [
        {"name": "Ω_b (baryon density)", "value": 0.0493, "uncertainty": 0.0006, "source": "Planck 2018"},
    ],
    "hubble constant": [
        {"name": "H0 (km/s/Mpc)", "value": 67.4, "uncertainty": 0.5, "source": "Planck 2018"},
        {"name": "H0 SH0ES (km/s/Mpc)", "value": 73.0, "uncertainty": 1.0, "source": "SH0ES 2022"},
    ],
    "cmb temperature": [
        {"name": "CMB temperature (K)", "value": 2.7255, "uncertainty": 0.0006, "source": "COBE/WMAP"},
    ],
    "primordial helium": [
        {"name": "Primordial helium Y_p", "value": 0.245, "uncertainty": 0.003, "source": "BBN"},
    ],
    "spectral index": [
        {"name": "Spectral index n_s", "value": 0.9649, "uncertainty": 0.0042, "source": "Planck 2018"},
    ],
    "sigma 8": [
        {"name": "σ_8 (matter fluctuation)", "value": 0.811, "uncertainty": 0.006, "source": "Planck 2018"},
    ],
    "age of universe": [
        {"name": "Age of universe (Gyr)", "value": 13.787, "uncertainty": 0.020, "source": "Planck 2018"},
    ],

    # QUANTUM MECHANICS
    "bohr radius": [
        {"name": "Bohr radius (Å)", "value": 0.529177, "uncertainty": 0.000001, "source": "CODATA"},
    ],
    "rydberg constant": [
        {"name": "Rydberg energy (eV)", "value": 13.605693, "uncertainty": 0.000001, "source": "CODATA"},
    ],
    "quantum conductance": [
        {"name": "Quantum of conductance e²/h (S)", "value": 7.7480917e-5, "uncertainty": 1e-12, "source": "CODATA"},
        {"name": "von Klitzing constant h/e² (Ω)", "value": 25812.807, "uncertainty": 0.001, "source": "CODATA"},
    ],

    # ASTROPHYSICS
    "chandrasekhar mass": [
        {"name": "Chandrasekhar limit (M☉)", "value": 1.44, "uncertainty": 0.02, "source": "White dwarf theory"},
    ],
    "salpeter imf": [
        {"name": "Salpeter IMF slope", "value": 2.35, "uncertainty": 0.05, "source": "Stellar IMF"},
    ],
    "star formation efficiency": [
        {"name": "Star formation efficiency ε", "value": 0.02, "uncertainty": 0.01, "source": "Observations"},
    ],
    "tully-fisher": [
        {"name": "Tully-Fisher slope", "value": 4.0, "uncertainty": 0.2, "source": "Galaxy observations"},
    ],
    "faber-jackson": [
        {"name": "Faber-Jackson slope", "value": 4.0, "uncertainty": 0.3, "source": "Elliptical galaxies"},
    ],
    "m-sigma": [
        {"name": "M-σ relation slope", "value": 4.38, "uncertainty": 0.29, "source": "Black hole masses"},
    ],
    "kerr efficiency": [
        {"name": "Maximum Kerr efficiency η", "value": 0.423, "uncertainty": 0.001, "source": "GR exact"},
    ],
    "roche limit": [
        {"name": "Roche limit coefficient (fluid)", "value": 2.44, "uncertainty": 0.01, "source": "Celestial mechanics"},
        {"name": "Roche limit coefficient (rigid)", "value": 1.26, "uncertainty": 0.01, "source": "Celestial mechanics"},
    ],

    # FLUID DYNAMICS
    "von karman": [
        {"name": "von Kármán constant κ", "value": 0.41, "uncertainty": 0.01, "source": "Turbulence"},
    ],
    "strouhal": [
        {"name": "Strouhal number (cylinder)", "value": 0.21, "uncertainty": 0.01, "source": "Vortex shedding"},
    ],
    "reynolds": [
        {"name": "Critical Re (pipe)", "value": 2300, "uncertainty": 100, "source": "Pipe flow"},
        {"name": "Critical Re (flat plate)", "value": 500000, "uncertainty": 50000, "source": "Boundary layer"},
    ],
    "kolmogorov": [
        {"name": "Kolmogorov constant C_K", "value": 1.5, "uncertainty": 0.1, "source": "Turbulence"},
        {"name": "Kolmogorov -5/3 exponent", "value": -5/3, "uncertainty": 0.01, "source": "Turbulence theory"},
    ],
    "rayleigh": [
        {"name": "Critical Rayleigh number Ra_c", "value": 1708, "uncertainty": 5, "source": "Convection"},
    ],
    "taylor number": [
        {"name": "Critical Taylor number Ta_c", "value": 1708, "uncertainty": 10, "source": "Couette flow"},
    ],
    "weber": [
        {"name": "Critical Weber number", "value": 12, "uncertainty": 1, "source": "Droplet breakup"},
    ],
    "sphere drag": [
        {"name": "Sphere drag coefficient C_d", "value": 0.47, "uncertainty": 0.02, "source": "Re > 1000"},
    ],
    "blasius": [
        {"name": "Blasius friction coefficient", "value": 1.328, "uncertainty": 0.001, "source": "Laminar flow"},
    ],
    "kelvin wake": [
        {"name": "Kelvin wake angle (degrees)", "value": 19.47, "uncertainty": 0.01, "source": "Ship wakes"},
    ],

    # GEOPHYSICS
    "chandler wobble": [
        {"name": "Chandler wobble period (days)", "value": 433, "uncertainty": 2, "source": "Geophysics"},
    ],
    "core mantle": [
        {"name": "Core-mantle boundary radius ratio", "value": 0.546, "uncertainty": 0.001, "source": "Seismology"},
    ],
    "inner outer core": [
        {"name": "Inner/outer core ratio", "value": 0.351, "uncertainty": 0.001, "source": "Seismology"},
    ],
    "moho depth": [
        {"name": "Moho depth continental (km)", "value": 35, "uncertainty": 5, "source": "Seismology"},
    ],
    "lithosphere": [
        {"name": "Lithosphere thickness (km)", "value": 100, "uncertainty": 20, "source": "Geophysics"},
    ],
    "plate velocity": [
        {"name": "Mean plate velocity (cm/yr)", "value": 5, "uncertainty": 2, "source": "Plate tectonics"},
    ],
    "gutenberg richter": [
        {"name": "Gutenberg-Richter b-value", "value": 1.0, "uncertainty": 0.1, "source": "Seismology"},
    ],
    "omori": [
        {"name": "Omori p-value (aftershocks)", "value": 1.0, "uncertainty": 0.1, "source": "Seismology"},
    ],
    "bath law": [
        {"name": "Båth's law magnitude difference", "value": 1.2, "uncertainty": 0.1, "source": "Seismology"},
    ],
    "byerlee": [
        {"name": "Byerlee friction coefficient", "value": 0.85, "uncertainty": 0.05, "source": "Rock mechanics"},
    ],

    # ATMOSPHERIC
    "lapse rate": [
        {"name": "Atmospheric lapse rate (K/km)", "value": 6.5, "uncertainty": 0.5, "source": "Standard atmosphere"},
    ],
    "tropopause": [
        {"name": "Tropopause height mid-lat (km)", "value": 11, "uncertainty": 1, "source": "Standard atmosphere"},
        {"name": "Tropopause temperature (K)", "value": 217, "uncertainty": 2, "source": "Standard atmosphere"},
    ],
    "scale height": [
        {"name": "Atmospheric scale height (km)", "value": 8.5, "uncertainty": 0.3, "source": "Atmospheric physics"},
    ],
    "richardson": [
        {"name": "Critical Richardson number", "value": 0.25, "uncertainty": 0.02, "source": "Turbulence"},
    ],
    "earth albedo": [
        {"name": "Planetary albedo", "value": 0.30, "uncertainty": 0.01, "source": "Earth observations"},
    ],
    "emissivity": [
        {"name": "Effective emissivity (greenhouse)", "value": 0.612, "uncertainty": 0.01, "source": "Climate science"},
    ],
    "solar constant": [
        {"name": "Solar constant (W/m²)", "value": 1361, "uncertainty": 1, "source": "Solar observations"},
    ],
    "climate sensitivity": [
        {"name": "Equilibrium climate sensitivity (°C)", "value": 3.0, "uncertainty": 0.5, "source": "IPCC"},
    ],
    "co2 airborne": [
        {"name": "CO2 airborne fraction", "value": 0.45, "uncertainty": 0.05, "source": "Carbon cycle"},
    ],
    "planck feedback": [
        {"name": "Planck feedback (W/m²/K)", "value": -3.2, "uncertainty": 0.1, "source": "Climate physics"},
    ],
    "clausius clapeyron": [
        {"name": "C-C scaling (%/K)", "value": 7, "uncertainty": 0.5, "source": "Thermodynamics"},
    ],
    "karman line": [
        {"name": "Kármán line altitude (km)", "value": 100, "uncertainty": 0, "source": "Definition"},
    ],

    # OCEANOGRAPHY
    "ekman": [
        {"name": "Ekman depth typical (m)", "value": 100, "uncertainty": 20, "source": "Oceanography"},
        {"name": "Ekman transport angle (degrees)", "value": 45, "uncertainty": 1, "source": "Theory"},
    ],
    "thermocline": [
        {"name": "Thermocline depth typical (m)", "value": 500, "uncertainty": 100, "source": "Oceanography"},
    ],
    "thermohaline": [
        {"name": "Thermohaline circulation (Sv)", "value": 20, "uncertainty": 5, "source": "Oceanography"},
    ],
    "gulf stream": [
        {"name": "Gulf Stream transport (Sv)", "value": 30, "uncertainty": 5, "source": "Oceanography"},
    ],
    "wave breaking": [
        {"name": "Wave breaking steepness H/L", "value": 1/7, "uncertainty": 0.01, "source": "Wave physics"},
    ],
    "mixing efficiency": [
        {"name": "Osborn mixing efficiency", "value": 0.2, "uncertainty": 0.05, "source": "Oceanography"},
    ],
    "isopycnal diffusivity": [
        {"name": "Isopycnal diffusivity (m²/s)", "value": 1000, "uncertainty": 200, "source": "Oceanography"},
    ],
    "redfield": [
        {"name": "Redfield C:N ratio", "value": 106/16, "uncertainty": 0.5, "source": "Biogeochemistry"},
        {"name": "Redfield N:P ratio", "value": 16/1, "uncertainty": 0.5, "source": "Biogeochemistry"},
    ],
    "sea level rise": [
        {"name": "Sea level rise rate (mm/yr)", "value": 3.4, "uncertainty": 0.3, "source": "Altimetry"},
    ],
    "ocean ph": [
        {"name": "Ocean pH current", "value": 8.1, "uncertainty": 0.05, "source": "Oceanography"},
    ],

    # BIOLOGY SCALING
    "kleiber": [
        {"name": "Kleiber metabolic exponent", "value": 0.75, "uncertainty": 0.02, "source": "Kleiber's law"},
        {"name": "Kleiber 3/4 exact", "value": 3/4, "uncertainty": 0, "source": "Theory"},
    ],
    "heart rate": [
        {"name": "Heart rate scaling exponent", "value": -0.25, "uncertainty": 0.02, "source": "Allometry"},
    ],
    "lifespan": [
        {"name": "Lifespan scaling exponent", "value": 0.25, "uncertainty": 0.02, "source": "Allometry"},
    ],
    "brain size": [
        {"name": "Brain-body scaling exponent", "value": 0.75, "uncertainty": 0.03, "source": "Allometry"},
    ],
    "respiratory quotient": [
        {"name": "Respiratory quotient RQ", "value": 0.82, "uncertainty": 0.02, "source": "Physiology"},
    ],
    "blood pressure": [
        {"name": "Blood pressure constant (mmHg)", "value": 100, "uncertainty": 10, "source": "Physiology"},
    ],
    "hematocrit": [
        {"name": "Optimal hematocrit", "value": 0.45, "uncertainty": 0.02, "source": "Physiology"},
    ],
    "nerve conduction": [
        {"name": "Nerve conduction velocity (m/s)", "value": 100, "uncertainty": 20, "source": "Neurophysiology"},
    ],
    "froude walk": [
        {"name": "Froude number walk-run transition", "value": 0.25, "uncertainty": 0.02, "source": "Biomechanics"},
    ],
    "respiration q10": [
        {"name": "Respiration Q10", "value": 2.0, "uncertainty": 0.3, "source": "Biology"},
    ],
    "circadian": [
        {"name": "Circadian period (hours)", "value": 24.2, "uncertainty": 0.3, "source": "Chronobiology"},
    ],

    # ECOLOGY
    "species area": [
        {"name": "Species-area exponent z", "value": 0.25, "uncertainty": 0.05, "source": "Island biogeography"},
    ],
    "predator prey": [
        {"name": "Predator/prey mass ratio", "value": 100, "uncertainty": 50, "source": "Ecology"},
    ],
    "trophic efficiency": [
        {"name": "Trophic transfer efficiency", "value": 0.1, "uncertainty": 0.02, "source": "Ecology"},
    ],
    "food web connectance": [
        {"name": "Food web connectance", "value": 0.1, "uncertainty": 0.02, "source": "Ecology"},
    ],
    "food chain": [
        {"name": "Food chain length typical", "value": 4, "uncertainty": 0.5, "source": "Ecology"},
    ],
    "background extinction": [
        {"name": "Background extinction rate (per Myr)", "value": 0.1, "uncertainty": 0.05, "source": "Paleontology"},
    ],

    # CONDENSED MATTER
    "lindemann": [
        {"name": "Lindemann melting parameter", "value": 0.1, "uncertainty": 0.02, "source": "Melting theory"},
    ],
    "glass transition": [
        {"name": "Glass Tg/Tm ratio", "value": 0.67, "uncertainty": 0.05, "source": "Glass physics"},
    ],
    "poisson ratio": [
        {"name": "Poisson ratio typical metals", "value": 0.3, "uncertainty": 0.05, "source": "Materials"},
    ],
    "gruneisen": [
        {"name": "Grüneisen parameter typical", "value": 2.0, "uncertainty": 0.5, "source": "Solid state"},
    ],
    "hall petch": [
        {"name": "Hall-Petch exponent", "value": 0.5, "uncertainty": 0.05, "source": "Metallurgy"},
    ],
    "percolation threshold": [
        {"name": "2D square lattice percolation", "value": 0.5928, "uncertainty": 0.0001, "source": "Percolation theory"},
        {"name": "3D simple cubic percolation", "value": 0.3116, "uncertainty": 0.0001, "source": "Percolation theory"},
    ],
    "ising": [
        {"name": "2D Ising β exponent", "value": 1/8, "uncertainty": 0, "source": "Exact"},
        {"name": "2D Ising γ exponent", "value": 7/4, "uncertainty": 0, "source": "Exact"},
        {"name": "2D Ising ν exponent", "value": 1, "uncertainty": 0, "source": "Exact"},
        {"name": "3D Ising β exponent", "value": 0.326, "uncertainty": 0.001, "source": "Numerical"},
        {"name": "3D Ising γ exponent", "value": 1.237, "uncertainty": 0.002, "source": "Numerical"},
        {"name": "3D Ising ν exponent", "value": 0.630, "uncertainty": 0.001, "source": "Numerical"},
    ],
    "bcs gap": [
        {"name": "BCS gap ratio 2Δ/kTc", "value": 3.528, "uncertainty": 0.01, "source": "BCS theory"},
    ],
    "quantum hall": [
        {"name": "Laughlin 1/3 filling", "value": 1/3, "uncertainty": 0, "source": "FQHE"},
        {"name": "Laughlin 1/5 filling", "value": 1/5, "uncertainty": 0, "source": "FQHE"},
        {"name": "Laughlin 2/5 filling", "value": 2/5, "uncertainty": 0, "source": "FQHE"},
    ],

    # CHEMISTRY
    "water bond angle": [
        {"name": "H-O-H bond angle (degrees)", "value": 104.5, "uncertainty": 0.1, "source": "Spectroscopy"},
    ],
    "ammonia bond angle": [
        {"name": "H-N-H bond angle (degrees)", "value": 107.0, "uncertainty": 0.2, "source": "Spectroscopy"},
    ],
    "methane tetrahedral": [
        {"name": "Tetrahedral angle (degrees)", "value": 109.47, "uncertainty": 0.01, "source": "Geometry"},
    ],
    "sp3 hybridization": [
        {"name": "sp³ tetrahedral angle", "value": 109.47, "uncertainty": 0.01, "source": "Exact"},
    ],
    "sp2 hybridization": [
        {"name": "sp² trigonal angle", "value": 120.0, "uncertainty": 0.01, "source": "Exact"},
    ],
    "dna base pair": [
        {"name": "DNA base pair rise (nm)", "value": 0.34, "uncertainty": 0.01, "source": "X-ray"},
        {"name": "DNA helix pitch (nm)", "value": 3.4, "uncertainty": 0.1, "source": "X-ray"},
        {"name": "DNA base pairs per turn", "value": 10.5, "uncertainty": 0.3, "source": "B-DNA"},
    ],
    "alpha helix": [
        {"name": "Alpha helix residues per turn", "value": 3.6, "uncertainty": 0.1, "source": "Protein structure"},
    ],
    "hydrogen bond": [
        {"name": "H-bond energy (kJ/mol)", "value": 20, "uncertainty": 5, "source": "Thermochemistry"},
    ],
    "electronegativity": [
        {"name": "Oxygen electronegativity (Pauling)", "value": 3.44, "uncertainty": 0.05, "source": "Pauling scale"},
        {"name": "Carbon electronegativity (Pauling)", "value": 2.55, "uncertainty": 0.05, "source": "Pauling scale"},
    ],
    "dielectric water": [
        {"name": "Dielectric constant of water", "value": 80.1, "uncertainty": 0.5, "source": "25°C"},
    ],
    "surface tension water": [
        {"name": "Water surface tension (mN/m)", "value": 72.8, "uncertainty": 0.2, "source": "25°C"},
    ],
    "ice water density": [
        {"name": "Ice/water density ratio", "value": 0.917, "uncertainty": 0.001, "source": "Ice physics"},
    ],

    # NETWORKS
    "scale free": [
        {"name": "Scale-free network exponent", "value": 2.5, "uncertainty": 0.3, "source": "Network theory"},
    ],
    "small world": [
        {"name": "Small world clustering", "value": 0.6, "uncertainty": 0.1, "source": "Network theory"},
    ],
    "six degrees": [
        {"name": "Six degrees of separation", "value": 6, "uncertainty": 1, "source": "Social networks"},
    ],
    "dunbar number": [
        {"name": "Dunbar number", "value": 150, "uncertainty": 20, "source": "Anthropology"},
    ],
    "metcalfe": [
        {"name": "Metcalfe network exponent", "value": 2.0, "uncertainty": 0.1, "source": "Network economics"},
    ],

    # URBAN
    "urban population": [
        {"name": "Urban scaling exponent", "value": 1.15, "uncertainty": 0.05, "source": "Urban scaling"},
    ],
    "urban infrastructure": [
        {"name": "Infrastructure scaling exponent", "value": 0.85, "uncertainty": 0.05, "source": "Urban scaling"},
    ],
    "marchetti": [
        {"name": "Marchetti constant (min)", "value": 30, "uncertainty": 5, "source": "Urban planning"},
    ],
    "travel time budget": [
        {"name": "Travel time budget (hours/day)", "value": 1.1, "uncertainty": 0.1, "source": "Transport"},
    ],
    "gini": [
        {"name": "Typical Gini coefficient", "value": 0.4, "uncertainty": 0.1, "source": "Economics"},
    ],
    "zipf city": [
        {"name": "Zipf city size exponent", "value": 1.0, "uncertainty": 0.1, "source": "Urban geography"},
    ],
    "okun": [
        {"name": "Okun's law coefficient", "value": 2, "uncertainty": 0.5, "source": "Macroeconomics"},
    ],
    "learning curve": [
        {"name": "Learning curve exponent", "value": 0.2, "uncertainty": 0.05, "source": "Industrial learning"},
    ],

    # PSYCHOLOGY
    "miller number": [
        {"name": "Miller's number (7±2)", "value": 7, "uncertainty": 2, "source": "Cognitive psychology"},
    ],
    "ebbinghaus": [
        {"name": "Forgetting curve exponent", "value": 0.5, "uncertainty": 0.1, "source": "Memory research"},
    ],
    "power law learning": [
        {"name": "Power law of learning exponent", "value": 0.4, "uncertainty": 0.1, "source": "Learning"},
    ],
    "weber": [
        {"name": "Weber fraction typical", "value": 0.1, "uncertainty": 0.05, "source": "Psychophysics"},
    ],
    "stevens brightness": [
        {"name": "Stevens brightness exponent", "value": 0.33, "uncertainty": 0.05, "source": "Psychophysics"},
    ],
    "stevens loudness": [
        {"name": "Stevens loudness exponent", "value": 0.67, "uncertainty": 0.05, "source": "Psychophysics"},
    ],
    "loss aversion": [
        {"name": "Loss aversion ratio", "value": 2.0, "uncertainty": 0.3, "source": "Behavioral economics"},
    ],
    "subitizing": [
        {"name": "Subitizing limit", "value": 4, "uncertainty": 1, "source": "Cognitive psychology"},
    ],

    # CHAOS & FRACTALS
    "feigenbaum delta": [
        {"name": "Feigenbaum δ constant", "value": 4.669201609, "uncertainty": 0.000000001, "source": "Universal"},
    ],
    "feigenbaum alpha": [
        {"name": "Feigenbaum α constant", "value": 2.502907875, "uncertainty": 0.000000001, "source": "Universal"},
    ],
    "logistic map": [
        {"name": "Logistic map chaos onset r", "value": 3.56995, "uncertainty": 0.00001, "source": "Chaos theory"},
    ],
    "lorenz attractor": [
        {"name": "Lorenz attractor dimension", "value": 2.06, "uncertainty": 0.02, "source": "Numerical"},
    ],
    "coastline britain": [
        {"name": "Britain coastline dimension", "value": 1.25, "uncertainty": 0.02, "source": "Richardson"},
    ],
    "mandelbrot": [
        {"name": "Mandelbrot boundary dimension", "value": 2.0, "uncertainty": 0.01, "source": "Fractal geometry"},
    ],
    "cantor set": [
        {"name": "Cantor set dimension", "value": math.log(2)/math.log(3), "uncertainty": 0.0001, "source": "Exact"},
    ],
    "sierpinski": [
        {"name": "Sierpiński triangle dimension", "value": math.log(3)/math.log(2), "uncertainty": 0.0001, "source": "Exact"},
    ],
    "koch snowflake": [
        {"name": "Koch snowflake dimension", "value": math.log(4)/math.log(3), "uncertainty": 0.0001, "source": "Exact"},
    ],
    "hurst": [
        {"name": "Hurst exponent (persistence)", "value": 0.7, "uncertainty": 0.1, "source": "Time series"},
    ],

    # INFORMATION
    "shannon entropy": [
        {"name": "Maximum binary entropy (bits)", "value": 1.0, "uncertainty": 0, "source": "Shannon theory"},
    ],
    "english entropy": [
        {"name": "English entropy (bits/char)", "value": 1.3, "uncertainty": 0.2, "source": "Shannon"},
    ],
    "english redundancy": [
        {"name": "English redundancy", "value": 0.75, "uncertainty": 0.05, "source": "Information theory"},
    ],
    "huffman": [
        {"name": "Huffman coding efficiency", "value": 0.95, "uncertainty": 0.03, "source": "Compression"},
    ],
    "hamming": [
        {"name": "Hamming (7,4) code rate", "value": 4/7, "uncertainty": 0, "source": "Exact"},
    ],

    # ACOUSTICS
    "perfect fifth": [
        {"name": "Perfect fifth ratio", "value": 3/2, "uncertainty": 0, "source": "Music theory"},
    ],
    "perfect fourth": [
        {"name": "Perfect fourth ratio", "value": 4/3, "uncertainty": 0, "source": "Music theory"},
    ],
    "major third": [
        {"name": "Major third (just)", "value": 5/4, "uncertainty": 0, "source": "Music theory"},
    ],
    "equal temperament semitone": [
        {"name": "ET semitone ratio", "value": 2**(1/12), "uncertainty": 0.0001, "source": "Music theory"},
    ],
    "pythagorean comma": [
        {"name": "Pythagorean comma", "value": (3**12)/(2**19), "uncertainty": 0.0001, "source": "Music theory"},
    ],
    "concert hall": [
        {"name": "Concert hall RT60 (s)", "value": 2.0, "uncertainty": 0.3, "source": "Acoustics"},
    ],
    "hearing threshold": [
        {"name": "Hearing threshold (dB SPL)", "value": 0, "uncertainty": 0, "source": "Audiology"},
    ],
    "pain threshold": [
        {"name": "Pain threshold (dB SPL)", "value": 120, "uncertainty": 5, "source": "Audiology"},
    ],

    # OPTICS
    "human eye focal": [
        {"name": "Eye focal length (mm)", "value": 17, "uncertainty": 1, "source": "Ophthalmology"},
    ],
    "pupil diameter": [
        {"name": "Pupil diameter range (mm)", "value": 5, "uncertainty": 2, "source": "Physiology"},
    ],
    "rod cone ratio": [
        {"name": "Rod/cone ratio in retina", "value": 20, "uncertainty": 2, "source": "Anatomy"},
    ],
    "visual angle": [
        {"name": "Visual acuity (arc min)", "value": 1, "uncertainty": 0.2, "source": "Vision science"},
    ],
    "l cone": [
        {"name": "L cone peak wavelength (nm)", "value": 564, "uncertainty": 5, "source": "Color vision"},
    ],
    "luminous efficacy": [
        {"name": "Maximum luminous efficacy (lm/W)", "value": 683, "uncertainty": 1, "source": "Definition"},
    ],
    "water refractive": [
        {"name": "Water refractive index", "value": 1.333, "uncertainty": 0.001, "source": "Optics"},
    ],
    "diamond refractive": [
        {"name": "Diamond refractive index", "value": 2.42, "uncertainty": 0.01, "source": "Optics"},
    ],
    "rainbow angle": [
        {"name": "Rainbow angle (degrees)", "value": 42, "uncertainty": 1, "source": "Optics"},
    ],

    # GEOMORPHOLOGY
    "hack law": [
        {"name": "Hack's law exponent", "value": 0.57, "uncertainty": 0.03, "source": "River networks"},
    ],
    "horton bifurcation": [
        {"name": "Horton bifurcation ratio", "value": 4, "uncertainty": 1, "source": "River networks"},
    ],
    "horton length": [
        {"name": "Horton length ratio", "value": 2.3, "uncertainty": 0.3, "source": "River networks"},
    ],
    "manning roughness": [
        {"name": "Manning n (natural channel)", "value": 0.035, "uncertainty": 0.005, "source": "Hydraulics"},
    ],
    "sinuosity": [
        {"name": "Sinuosity typical", "value": 1.5, "uncertainty": 0.2, "source": "Geomorphology"},
    ],
    "meander wavelength": [
        {"name": "Meander wavelength/width ratio", "value": 10, "uncertainty": 2, "source": "Geomorphology"},
    ],
    "hillslope angle": [
        {"name": "Threshold hillslope angle (deg)", "value": 35, "uncertainty": 3, "source": "Geomorphology"},
    ],
    "hypsometric": [
        {"name": "Hypsometric integral (mature)", "value": 0.5, "uncertainty": 0.1, "source": "Geomorphology"},
    ],
    "denudation": [
        {"name": "Denudation rate (mm/kyr)", "value": 50, "uncertainty": 20, "source": "Geomorphology"},
    ],
    "glacier aar": [
        {"name": "Glacier accumulation area ratio", "value": 0.65, "uncertainty": 0.05, "source": "Glaciology"},
    ],
    "bruun rule": [
        {"name": "Bruun rule factor", "value": 100, "uncertainty": 20, "source": "Coastal geology"},
    ],
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def find_constants_for_topic(topic: ResearchTopic) -> List[Dict]:
    """
    Find relevant constants for a topic from embedded knowledge.
    """
    constants = []
    query_lower = topic.query.lower()

    # Check all keywords
    for keyword, const_list in EMBEDDED_CONSTANTS.items():
        if keyword in query_lower:
            for c in const_list:
                if c not in constants:
                    constants.append(c)

    return constants


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class TopicResult:
    """Result from processing a single topic."""
    topic_query: str
    domain: str
    timestamp: str
    constants_found: int
    z2_patterns_found: int
    best_z2_match: Optional[Dict] = None
    all_z2_matches: List[Dict] = field(default_factory=list)
    all_matches: List[Dict] = field(default_factory=list)
    constants: List[Dict] = field(default_factory=list)


# =============================================================================
# Z² PATTERN ANALYSIS
# =============================================================================

class Z2Analyzer:
    """
    Analyzes constants for Z² patterns using BriareusFlow.
    """

    def __init__(self, max_error: float = 2.0, verbose: bool = False):
        self.engine = PatternSearchEngine(
            config={"max_error_percent": max_error},
            verbose=False
        )
        self.verbose = verbose
        self.max_error = max_error

    def analyze_constant(self, value: float, name: str, domain: str) -> Tuple[List[Dict], Optional[Dict]]:
        """
        Analyze a constant for patterns.
        Returns: (all_z2_matches, best_z2_match)
        """
        result = self.engine.search(value, domain=domain)

        z2_matches = []
        best_z2 = None
        best_error = 100.0

        for match in result.matches:
            match_dict = {
                "constant_name": name,
                "constant_value": value,
                "formula": match.formula,
                "computed_value": match.computed_value,
                "percent_error": match.percent_error,
                "has_z2": "Z²" in match.formula
            }

            if "Z²" in match.formula:
                z2_matches.append(match_dict)
                if abs(match.percent_error) < best_error:
                    best_error = abs(match.percent_error)
                    best_z2 = match_dict

        return z2_matches, best_z2

    def get_all_matches(self, value: float, name: str, domain: str) -> List[Dict]:
        """Get all matches (not just Z²) for a constant."""
        result = self.engine.search(value, domain=domain)

        matches = []
        for match in result.matches[:10]:  # Top 10
            matches.append({
                "constant_name": name,
                "constant_value": value,
                "formula": match.formula,
                "computed_value": match.computed_value,
                "percent_error": match.percent_error,
                "has_z2": "Z²" in match.formula
            })

        return matches


# =============================================================================
# AUTONOMOUS RESEARCH RUNNER
# =============================================================================

class AutonomousResearchRunner:
    """
    Main orchestrator for autonomous Z² research.
    """

    def __init__(self, verbose: bool = True, max_error: float = 2.0):
        self.verbose = verbose
        self.analyzer = Z2Analyzer(max_error=max_error, verbose=verbose)
        self.results: List[TopicResult] = []

        # Create output directory
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def _log(self, msg: str):
        if self.verbose:
            print(msg)

    def process_topic(self, topic: ResearchTopic, index: int, total: int) -> TopicResult:
        """Process a single research topic."""
        print(f"[{index}/{total}] {topic.query[:60]}...", end=" ")

        result = TopicResult(
            topic_query=topic.query,
            domain=topic.domain,
            timestamp=datetime.now().isoformat(),
            constants_found=0,
            z2_patterns_found=0
        )

        # Step 1: Find constants
        constants = find_constants_for_topic(topic)
        result.constants_found = len(constants)
        result.constants = constants

        if not constants:
            print("No constants found")
            return result

        # Step 2: Analyze each constant
        all_z2_matches = []
        all_matches = []

        for const in constants:
            value = const.get("value", 0)
            name = const.get("name", "Unknown")

            if value == 0:
                continue

            # Get Z² matches
            z2_matches, best_z2 = self.analyzer.analyze_constant(value, name, topic.domain)
            all_z2_matches.extend(z2_matches)

            # Get all matches
            matches = self.analyzer.get_all_matches(value, name, topic.domain)
            all_matches.extend(matches)

        # Store results
        result.all_z2_matches = all_z2_matches
        result.z2_patterns_found = len(all_z2_matches)
        result.all_matches = all_matches

        # Find best Z² match overall
        if all_z2_matches:
            best = min(all_z2_matches, key=lambda x: abs(x.get("percent_error", 100)))
            result.best_z2_match = best
            print(f"{len(constants)} consts, {len(all_z2_matches)} Z² matches - Best: {best['formula']} ({best['percent_error']:.4f}%)")
        else:
            print(f"{len(constants)} constants, no Z² matches")

        return result

    def save_result(self, result: TopicResult):
        """Save individual result to file."""
        safe_name = re.sub(r'[^\w\s-]', '', result.topic_query)[:40]
        safe_name = re.sub(r'[\s]+', '_', safe_name).lower()

        filename = OUTPUT_DIR / f"{result.domain}_{safe_name}.json"

        with open(filename, 'w') as f:
            json.dump(asdict(result), f, indent=2, default=str)

    def save_summary(self):
        """Save overall summary."""
        total_constants = sum(r.constants_found for r in self.results)
        total_z2_patterns = sum(r.z2_patterns_found for r in self.results)
        successful = sum(1 for r in self.results if r.constants_found > 0)

        # Find top discoveries
        all_z2_matches = []
        for r in self.results:
            if r.best_z2_match:
                all_z2_matches.append({
                    "topic": r.topic_query,
                    "domain": r.domain,
                    **r.best_z2_match
                })

        all_z2_matches.sort(key=lambda x: abs(x.get("percent_error", 100)))

        summary = {
            "timestamp": datetime.now().isoformat(),
            "topics_processed": len(self.results),
            "topics_with_constants": successful,
            "total_constants_found": total_constants,
            "total_z2_patterns_found": total_z2_patterns,
            "domains_covered": list(set(r.domain for r in self.results)),
            "top_50_z2_discoveries": all_z2_matches[:50],
            "by_domain": {}
        }

        for r in self.results:
            if r.domain not in summary["by_domain"]:
                summary["by_domain"][r.domain] = {
                    "topics": 0,
                    "constants": 0,
                    "z2_patterns": 0
                }
            summary["by_domain"][r.domain]["topics"] += 1
            summary["by_domain"][r.domain]["constants"] += r.constants_found
            summary["by_domain"][r.domain]["z2_patterns"] += r.z2_patterns_found

        with open(SUMMARY_FILE, 'w') as f:
            json.dump(summary, f, indent=2, default=str)

        self._create_markdown_report(summary, all_z2_matches)

        return summary

    def _create_markdown_report(self, summary: Dict, all_matches: List[Dict]):
        """Create human-readable markdown report."""
        report_file = OUTPUT_DIR / "AUTONOMOUS_RESEARCH_REPORT.md"

        with open(report_file, 'w') as f:
            f.write("# Z² Autonomous Research Report\n\n")
            f.write(f"**Generated:** {summary['timestamp']}\n\n")
            f.write("---\n\n")

            f.write("## Summary Statistics\n\n")
            f.write(f"| Metric | Value |\n")
            f.write(f"|--------|-------|\n")
            f.write(f"| Topics Processed | {summary['topics_processed']} |\n")
            f.write(f"| Topics with Constants | {summary['topics_with_constants']} |\n")
            f.write(f"| Total Constants | {summary['total_constants_found']} |\n")
            f.write(f"| Z² Patterns Found | {summary['total_z2_patterns_found']} |\n")
            f.write(f"| Domains Covered | {len(summary['domains_covered'])} |\n")
            f.write("\n---\n\n")

            f.write("## Top 50 Z² Discoveries\n\n")
            f.write("| Rank | Domain | Constant | Z² Formula | Computed | Actual | Error |\n")
            f.write("|------|--------|----------|------------|----------|--------|-------|\n")

            for i, match in enumerate(all_matches[:50], 1):
                f.write(f"| {i} | {match.get('domain', '')} | ")
                f.write(f"{match.get('constant_name', '')[:25]} | ")
                f.write(f"**{match.get('formula', '')}** | ")
                f.write(f"{match.get('computed_value', 0):.6g} | ")
                f.write(f"{match.get('constant_value', 0):.6g} | ")
                f.write(f"{match.get('percent_error', 0):.4f}% |\n")

            f.write("\n---\n\n")

            f.write("## Results by Domain\n\n")
            for domain, stats in sorted(summary.get("by_domain", {}).items()):
                f.write(f"### {domain}\n")
                f.write(f"- Topics: {stats['topics']}\n")
                f.write(f"- Constants: {stats['constants']}\n")
                f.write(f"- Z² Patterns: {stats['z2_patterns']}\n\n")

            f.write("---\n\n")
            f.write("*Generated by Z² Autonomous Research Engine*\n")

    def run(self, topics: List[ResearchTopic]) -> Dict:
        """Run autonomous research on all topics."""
        print("\n" + "=" * 70)
        print(f"Z² AUTONOMOUS RESEARCH - Processing {len(topics)} topics")
        print("=" * 70 + "\n")

        start_time = time.time()

        for i, topic in enumerate(topics, 1):
            result = self.process_topic(topic, i, len(topics))
            self.results.append(result)
            self.save_result(result)

        elapsed = time.time() - start_time
        summary = self.save_summary()

        print("\n" + "=" * 70)
        print("RESEARCH COMPLETE")
        print("=" * 70)
        print(f"Time: {elapsed:.1f} seconds ({elapsed/60:.1f} minutes)")
        print(f"Topics: {len(self.results)}")
        print(f"Constants: {summary['total_constants_found']}")
        print(f"Z² Patterns: {summary['total_z2_patterns_found']}")
        print(f"\nResults: {OUTPUT_DIR}")

        return summary


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Run autonomous Z² research on 500+ topics"
    )
    parser.add_argument("--domain", type=str, help="Only process topics from this domain")
    parser.add_argument("--priority", type=int, choices=[1, 2, 3], help="Only priority N topics")
    parser.add_argument("--limit", type=int, help="Limit to first N topics")
    parser.add_argument("--max-error", type=float, default=2.0, help="Max percent error (default: 2.0)")
    parser.add_argument("--quiet", action="store_true", help="Reduce output")
    parser.add_argument("--list-domains", action="store_true", help="List available domains")

    args = parser.parse_args()

    if args.list_domains:
        print("Available domains:")
        for domain in get_all_domains():
            count = len(get_topics_by_domain(domain))
            print(f"  {domain}: {count} topics")
        return

    topics = RESEARCH_TOPICS

    if args.domain:
        topics = get_topics_by_domain(args.domain)
        print(f"Filtered to {len(topics)} topics in domain '{args.domain}'")

    if args.priority:
        topics = [t for t in topics if t.priority == args.priority]
        print(f"Filtered to {len(topics)} priority {args.priority} topics")

    if args.limit:
        topics = topics[:args.limit]
        print(f"Limited to {len(topics)} topics")

    if not topics:
        print("No topics to process!")
        return

    runner = AutonomousResearchRunner(
        verbose=not args.quiet,
        max_error=args.max_error
    )

    runner.run(topics)


if __name__ == "__main__":
    main()
