#!/usr/bin/env python3
"""
LAGRANGIAN TEMPLATES
====================

Standard physics Lagrangians and action principles that serve as
templates for deriving Z² relationships.

Author: Carl Zimmerman
Date: May 6, 2026
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


class PhysicsFramework(Enum):
    """Physics frameworks/theories."""
    QED = "quantum_electrodynamics"
    QCD = "quantum_chromodynamics"
    ELECTROWEAK = "electroweak"
    STANDARD_MODEL = "standard_model"
    GENERAL_RELATIVITY = "general_relativity"
    QUANTUM_MECHANICS = "quantum_mechanics"
    STATISTICAL_MECHANICS = "statistical_mechanics"
    FLUID_DYNAMICS = "fluid_dynamics"
    THERMODYNAMICS = "thermodynamics"
    OPTICS = "optics"
    NUCLEAR = "nuclear_physics"


@dataclass
class LagrangianTemplate:
    """A template for a physical Lagrangian."""
    name: str
    framework: PhysicsFramework
    lagrangian: str              # Mathematical expression
    latex: str                   # LaTeX rendering
    fields: List[str]            # Field content
    symmetry: str                # Gauge/symmetry group
    parameters: Dict[str, str]   # Physical parameters
    z2_potential: str = ""       # How Z² might enter
    notes: str = ""


# =============================================================================
# GAUGE THEORY LAGRANGIANS
# =============================================================================

GAUGE_THEORY_TEMPLATES = {
    "qed": LagrangianTemplate(
        name="Quantum Electrodynamics",
        framework=PhysicsFramework.QED,
        lagrangian="L = ψ̄(iγ^μD_μ - m)ψ - 1/4 F_μν F^μν",
        latex=r"\mathcal{L} = \bar{\psi}(i\gamma^\mu D_\mu - m)\psi - \frac{1}{4}F_{\mu\nu}F^{\mu\nu}",
        fields=["electron ψ", "photon A_μ"],
        symmetry="U(1)",
        parameters={
            "e": "electric charge (coupling)",
            "m": "electron mass",
            "α": "fine structure constant = e²/4πℏc"
        },
        z2_potential="α⁻¹ = 4Z² + 3 through dimensional compactification",
        notes="QED describes electromagnetic interactions of electrons"
    ),

    "qcd": LagrangianTemplate(
        name="Quantum Chromodynamics",
        framework=PhysicsFramework.QCD,
        lagrangian="L = -1/4 G^a_μν G^aμν + Σq̄(iγ^μD_μ - m_q)q",
        latex=r"\mathcal{L} = -\frac{1}{4}G^a_{\mu\nu}G^{a\mu\nu} + \sum_q\bar{q}(i\gamma^\mu D_\mu - m_q)q",
        fields=["quarks q", "8 gluons G^a_μ"],
        symmetry="SU(3)_color",
        parameters={
            "g_s": "strong coupling",
            "α_s": "strong coupling constant = g_s²/4π"
        },
        z2_potential="8 gluons connect to Z² = 8 × (4π/3)",
        notes="8 gluons from SU(3) adjoint representation"
    ),

    "electroweak": LagrangianTemplate(
        name="Electroweak Theory",
        framework=PhysicsFramework.ELECTROWEAK,
        lagrangian="L = -1/4 W^a_μν W^aμν - 1/4 B_μν B^μν + |D_μH|² - V(H)",
        latex=r"\mathcal{L} = -\frac{1}{4}W^a_{\mu\nu}W^{a\mu\nu} - \frac{1}{4}B_{\mu\nu}B^{\mu\nu} + |D_\mu H|^2 - V(H)",
        fields=["W^a (3)", "B", "Higgs H", "fermions"],
        symmetry="SU(2)_L × U(1)_Y → U(1)_EM",
        parameters={
            "g": "SU(2) coupling",
            "g'": "U(1) coupling",
            "θ_W": "weak mixing angle",
            "v": "Higgs VEV"
        },
        z2_potential="sin²θ_W = 3/13 from gauge coupling ratio",
        notes="Unified electromagnetic and weak interactions"
    ),
}


# =============================================================================
# GRAVITATIONAL LAGRANGIANS
# =============================================================================

GRAVITY_TEMPLATES = {
    "einstein_hilbert": LagrangianTemplate(
        name="Einstein-Hilbert Action",
        framework=PhysicsFramework.GENERAL_RELATIVITY,
        lagrangian="S = (1/16πG) ∫ √(-g)(R - 2Λ) d⁴x",
        latex=r"S = \frac{1}{16\pi G}\int\sqrt{-g}(R - 2\Lambda)d^4x",
        fields=["metric g_μν"],
        symmetry="Diffeomorphism invariance",
        parameters={
            "G": "Newton's constant",
            "Λ": "cosmological constant",
            "R": "Ricci scalar curvature"
        },
        z2_potential="Λ/ρ_crit = Ω_Λ = 13/19 from holographic bound",
        notes="Governs spacetime geometry"
    ),

    "friedmann": LagrangianTemplate(
        name="Friedmann Cosmology",
        framework=PhysicsFramework.GENERAL_RELATIVITY,
        lagrangian="H² = (8πG/3)ρ - k/a² + Λ/3",
        latex=r"H^2 = \frac{8\pi G}{3}\rho - \frac{k}{a^2} + \frac{\Lambda}{3}",
        fields=["scale factor a(t)", "matter density ρ"],
        symmetry="FLRW (homogeneous, isotropic)",
        parameters={
            "H": "Hubble parameter",
            "Ω_m": "matter fraction",
            "Ω_Λ": "dark energy fraction"
        },
        z2_potential="H₀ = 2Z² + 6 km/s/Mpc",
        notes="Expanding universe dynamics"
    ),
}


# =============================================================================
# NUCLEAR PHYSICS
# =============================================================================

NUCLEAR_TEMPLATES = {
    "shell_model": LagrangianTemplate(
        name="Nuclear Shell Model",
        framework=PhysicsFramework.NUCLEAR,
        lagrangian="H = Σᵢ(p²ᵢ/2m + V(rᵢ)) + Σᵢⱼ V_spin-orbit",
        latex=r"H = \sum_i\left(\frac{p_i^2}{2m} + V(r_i)\right) + \sum_{ij}V_{SO}",
        fields=["nucleons (protons, neutrons)"],
        symmetry="Rotational symmetry + spin-orbit coupling",
        parameters={
            "magic_numbers": "[2, 8, 20, 28, 50, 82, 126]",
            "spin_orbit": "ℓ·s coupling strength"
        },
        z2_potential="Magic 82 = 2Z² + 15 from shell closure geometry",
        notes="Explains nuclear magic numbers and stability"
    ),

    "beta_decay": LagrangianTemplate(
        name="Weak Beta Decay",
        framework=PhysicsFramework.ELECTROWEAK,
        lagrangian="L_W = (G_F/√2) [ū γ^μ(1-γ₅)d][ē γ_μ(1-γ₅)ν_e]",
        latex=r"\mathcal{L}_W = \frac{G_F}{\sqrt{2}}[\bar{u}\gamma^\mu(1-\gamma_5)d][\bar{e}\gamma_\mu(1-\gamma_5)\nu_e]",
        fields=["quarks", "electron", "neutrino"],
        symmetry="V-A (parity violation)",
        parameters={
            "G_F": "Fermi constant",
            "τ_n": "neutron lifetime"
        },
        z2_potential="τ_n = 26Z² + 8 seconds from weak coupling",
        notes="n → p + e⁻ + ν̄_e process"
    ),
}


# =============================================================================
# FLUID DYNAMICS
# =============================================================================

FLUID_TEMPLATES = {
    "navier_stokes": LagrangianTemplate(
        name="Navier-Stokes Equations",
        framework=PhysicsFramework.FLUID_DYNAMICS,
        lagrangian="ρ(∂v/∂t + v·∇v) = -∇p + μ∇²v + f",
        latex=r"\rho\left(\frac{\partial\mathbf{v}}{\partial t} + \mathbf{v}\cdot\nabla\mathbf{v}\right) = -\nabla p + \mu\nabla^2\mathbf{v} + \mathbf{f}",
        fields=["velocity v", "pressure p", "density ρ"],
        symmetry="Galilean invariance",
        parameters={
            "Re": "Reynolds number = ρvL/μ",
            "Ra": "Rayleigh number (buoyancy)",
            "Pr": "Prandtl number"
        },
        z2_potential="Ra_crit = 50Z² + 32 ≈ 1708 for convection onset",
        notes="Governs fluid motion, convection"
    ),

    "rayleigh_benard": LagrangianTemplate(
        name="Rayleigh-Bénard Convection",
        framework=PhysicsFramework.FLUID_DYNAMICS,
        lagrangian="Ra = gαΔT L³/(νκ) > Ra_crit",
        latex=r"Ra = \frac{g\alpha\Delta T L^3}{\nu\kappa} > Ra_{crit}",
        fields=["temperature T", "velocity v"],
        symmetry="Horizontal translation + vertical reflection",
        parameters={
            "Ra_crit": "critical Rayleigh number ≈ 1708",
            "α": "thermal expansion",
            "ν": "kinematic viscosity",
            "κ": "thermal diffusivity"
        },
        z2_potential="Ra_crit = 50Z² + 32 from marginal stability",
        notes="Critical value for convection cells"
    ),
}


# =============================================================================
# CHEMISTRY/MOLECULAR
# =============================================================================

CHEMISTRY_TEMPLATES = {
    "hybridization": LagrangianTemplate(
        name="Molecular Orbital Hybridization",
        framework=PhysicsFramework.QUANTUM_MECHANICS,
        lagrangian="ψ_sp³ = (s + px + py + pz)/2",
        latex=r"\psi_{sp^3} = \frac{1}{2}(s + p_x + p_y + p_z)",
        fields=["atomic orbitals s, p"],
        symmetry="Tetrahedral (T_d)",
        parameters={
            "θ_tet": "tetrahedral angle = arccos(-1/3) ≈ 109.47°"
        },
        z2_potential="θ_tet ≈ 3Z² + 9 from 3D geometry",
        notes="sp³ hybridization geometry"
    ),

    "water_molecule": LagrangianTemplate(
        name="Water Molecular Geometry",
        framework=PhysicsFramework.QUANTUM_MECHANICS,
        lagrangian="V = k(θ - θ₀)²/2 + electrostatic + hydrogen bonding",
        latex=r"V = \frac{k}{2}(\theta - \theta_0)^2 + V_{elec} + V_{HB}",
        fields=["H-O-H angle", "O-H bond"],
        symmetry="C_2v point group",
        parameters={
            "θ_HOH": "H-O-H bond angle ≈ 104.5°",
            "r_OH": "O-H bond length"
        },
        z2_potential="θ_HOH ≈ 3Z² + 4 from orbital geometry",
        notes="Most important molecule in chemistry"
    ),
}


# =============================================================================
# COMBINED TEMPLATE DICTIONARY
# =============================================================================

LAGRANGIAN_TEMPLATES: Dict[str, LagrangianTemplate] = {
    **GAUGE_THEORY_TEMPLATES,
    **GRAVITY_TEMPLATES,
    **NUCLEAR_TEMPLATES,
    **FLUID_TEMPLATES,
    **CHEMISTRY_TEMPLATES,
}


# Domain to framework mapping
DOMAIN_FRAMEWORKS: Dict[str, List[PhysicsFramework]] = {
    "particle_physics": [PhysicsFramework.QED, PhysicsFramework.ELECTROWEAK,
                          PhysicsFramework.STANDARD_MODEL],
    "cosmology": [PhysicsFramework.GENERAL_RELATIVITY],
    "nuclear_physics": [PhysicsFramework.NUCLEAR, PhysicsFramework.QCD],
    "chemistry": [PhysicsFramework.QUANTUM_MECHANICS],
    "fluid_dynamics": [PhysicsFramework.FLUID_DYNAMICS],
    "thermodynamics": [PhysicsFramework.STATISTICAL_MECHANICS,
                       PhysicsFramework.THERMODYNAMICS],
    "optics": [PhysicsFramework.QED, PhysicsFramework.OPTICS],
    "atmospheric": [PhysicsFramework.THERMODYNAMICS, PhysicsFramework.FLUID_DYNAMICS],
}


def get_templates_for_domain(domain: str) -> List[LagrangianTemplate]:
    """Get relevant Lagrangian templates for a domain."""
    frameworks = DOMAIN_FRAMEWORKS.get(domain, [])
    return [t for t in LAGRANGIAN_TEMPLATES.values()
            if t.framework in frameworks]


def get_template_with_z2_potential(domain: str) -> List[LagrangianTemplate]:
    """Get templates that have Z² potential connections."""
    templates = get_templates_for_domain(domain)
    return [t for t in templates if t.z2_potential]
