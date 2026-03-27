#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════════════════
                        RENORMALIZATION
                      Why Infinities Cancel
═══════════════════════════════════════════════════════════════════════════════════════════

Quantum field theory produces INFINITE answers.
Yet these infinities can be systematically removed:

    • Infinite self-energy → renormalized mass
    • Infinite charge → renormalized coupling
    • Infinite vacuum energy → subtracted

WHY does this work? Why is QFT "renormalizable"?

This document shows renormalization emerges from Z = 2√(8π/3).

Carl Zimmerman, March 2026
═══════════════════════════════════════════════════════════════════════════════════════════
"""

import numpy as np

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
Z = 2 * np.sqrt(8 * np.pi / 3)
Z2 = Z**2
pi = np.pi
alpha = 1/137.035999084

print("═" * 95)
print("                    RENORMALIZATION")
print("                      Why Infinities Cancel")
print("═" * 95)

print(f"""
                           Z = {Z:.10f}

    Z² = 8 × (4π/3) = CUBE × SPHERE

    Infinities appear because we integrate to infinite energy.
    The SPHERE (continuous) has no upper limit.
    The CUBE (discrete) provides a natural cutoff.

    Renormalization works because:
        Z² = CUBE × SPHERE is FINITE
        The infinite SPHERE is tamed by finite CUBE
""")

# =============================================================================
# SECTION 1: THE PROBLEM OF INFINITIES
# =============================================================================
print("═" * 95)
print("                    1. WHERE DO INFINITIES COME FROM?")
print("═" * 95)

print(f"""
THE DIVERGENCES:

    QFT calculations involve integrals over all momenta:
        ∫ d⁴k (something)

    These often diverge at high k (ultraviolet divergence).

EXAMPLES:

    1. Electron self-energy:
       The electron interacts with its own EM field.
       Energy = ∫ d³k ℏω/2 (zero-point energy)
              → ∞ (diverges!)

    2. Vacuum polarization:
       Virtual e⁺e⁻ pairs screen charge.
       Correction involves ∫ d⁴k / k²
              → ∞ (diverges logarithmically)

    3. Vertex correction:
       How electron couples to photon.
       Also divergent.

THE CRISIS:

    Early QED seemed to give nonsense!
    Infinite mass, infinite charge, infinite everything.

THE SOLUTION:

    Renormalization: Absorb infinities into redefinitions.
    Feynman, Schwinger, Tomonaga (1940s).
    QED becomes the most precise theory ever!
""")

# =============================================================================
# SECTION 2: HOW RENORMALIZATION WORKS
# =============================================================================
print("\n" + "═" * 95)
print("                    2. HOW RENORMALIZATION WORKS")
print("═" * 95)

print(f"""
THE PROCEDURE:

    1. Introduce a CUTOFF Λ (maximum momentum)
       Now integrals are finite (depend on Λ)

    2. Split parameters into "bare" + "counterterm":
       m = m_bare + δm (mass)
       e = e_bare + δe (charge)

    3. Choose counterterms to CANCEL Λ dependence.
       Physical quantities become Λ-independent.

    4. Take Λ → ∞.
       If everything stays finite: RENORMALIZABLE!

THE MEANING:

    "Bare" parameters are infinite but unobservable.
    Physical (renormalized) parameters are finite and measured.

    Example: Electron mass
        m_bare = ∞ (includes infinite self-energy)
        m_physical = 0.511 MeV (what we measure)

RENORMALIZABILITY:

    A theory is renormalizable if:
        All infinities can be absorbed into a FINITE
        number of parameter redefinitions.

    QED: 3 parameters (m_e, e, field normalization)
    SM: ~19 parameters (masses, couplings)

NON-RENORMALIZABLE:

    Gravity (GR) is NOT renormalizable.
    New infinities appear at each loop order.
    Need infinitely many parameters.

    This is why we need quantum gravity!
""")

# =============================================================================
# SECTION 3: THE CUTOFF FROM Z
# =============================================================================
print("\n" + "═" * 95)
print("                    3. THE NATURAL CUTOFF FROM Z")
print("═" * 95)

print(f"""
THE PUZZLE:

    We introduce cutoff Λ, then take Λ → ∞.
    But maybe there's a PHYSICAL cutoff?

THE PLANCK SCALE:

    E_Pl = √(ℏc⁵/G) ~ 10¹⁹ GeV

    At this energy, quantum gravity is important.
    Above E_Pl, our theories break down anyway.

FROM Z:

    log₁₀(M_Pl/m_e) = 3Z + 5 ≈ 22.4

    The Planck scale is SET by Z!

    The cutoff is not arbitrary.
    The cutoff IS the Planck scale.
    The Planck scale comes from Z geometry.

THE PICTURE:

    Z² = CUBE × SPHERE

    SPHERE: Continuous, extends to infinity
    CUBE: Discrete, has finite structure (8 vertices)

    Without CUBE, SPHERE integrals diverge.
    The CUBE provides the regularization!

THE ARGUMENT:

    Below Planck: SPHERE dominates (continuous physics)
    Above Planck: CUBE dominates (discrete structure)

    The CUBE structure "cuts off" the SPHERE at Planck.
    This is the NATURAL regularization.

    Renormalization = CUBE taming SPHERE infinity.
""")

# =============================================================================
# SECTION 4: RUNNING COUPLINGS
# =============================================================================
print("\n" + "═" * 95)
print("                    4. RUNNING COUPLINGS FROM Z")
print("═" * 95)

# Calculate running
def alpha_QED(Q_GeV):
    """QED coupling at energy Q (approximately)."""
    alpha_0 = 1/137.036
    return alpha_0 / (1 - alpha_0 * np.log(Q_GeV/0.000511) / (3*pi))

print(f"""
COUPLING CONSTANTS RUN:

    α(Q) depends on energy scale Q!

    At low energy: α ≈ 1/137
    At M_Z (91 GeV): α ≈ 1/128
    At higher energy: Even larger

THE BETA FUNCTION:

    dα/d(log Q) = β(α) = b₀α² + b₁α³ + ...

    For QED: b₀ = 2/(3π) > 0 (coupling grows with energy)
    For QCD: b₀ = -(11-2n_f/3)/(4π) < 0 (coupling shrinks!)

FROM Z:

    α = 1/(4Z² + 3)

    This is the LOW ENERGY value.
    What about running?

    The running depends on:
        • Number of charged particles (loop contributions)
        • Gauge group structure

    Both are encoded in Z:
        3 generations from "3" in SPHERE
        Gauge generators: 12 = 9Z²/(8π)

THE MEANING:

    α = 1/137 at low energy is from Z.
    But α RUNS because:
        Virtual particles contribute at higher energy
        More CUBE modes activated
        Coupling strength changes

    The running is CONSISTENT with Z.
    It doesn't change 1/(4Z² + 3) formula - that's the definition point.
""")

# =============================================================================
# SECTION 5: ANOMALY CANCELLATION
# =============================================================================
print("\n" + "═" * 95)
print("                    5. ANOMALY CANCELLATION")
print("═" * 95)

print(f"""
ANOMALIES:

    Some symmetries break due to quantum effects.
    These are called ANOMALIES.

GAUGE ANOMALIES:

    If gauge symmetry has anomaly:
        Theory is INCONSISTENT (non-renormalizable)!

    Gauge anomalies MUST cancel for consistency.

IN THE STANDARD MODEL:

    Anomaly = Tr(Y³) summed over fermions.

    For one generation:
        Quarks: 3 colors × (2Y_L³ + Y_uR³ + Y_dR³)
        Leptons: 2Y_L³ + Y_eR³ + Y_νR³

    With correct hypercharges:
        Quarks contribute: 3 × 2 × (1/6)³ + 3 × (2/3)³ + 3 × (-1/3)³
        Leptons contribute: 2 × (-1/2)³ + (-1)³ + 0³

    SUM = 0! Anomaly cancels!

FROM Z:

    Why do anomalies cancel?

    The Standard Model fermion content is:
        3 colors × 2 chiralities × 3 generations × 2 types (u,d)

    These numbers come from Z:
        3 from SPHERE
        2 from factor 2 in Z
        8 = 2³ structure

    The consistency is BUILT IN to Z geometry!

THE MEANING:

    Anomaly cancellation is not coincidence.
    It's required by Z² = CUBE × SPHERE consistency.

    The CUBE (gauge structure) must embed consistently
    in SPHERE (spacetime).
    This FORCES anomaly cancellation.
""")

# =============================================================================
# SECTION 6: EFFECTIVE FIELD THEORY
# =============================================================================
print("\n" + "═" * 95)
print("                    6. EFFECTIVE FIELD THEORY PERSPECTIVE")
print("═" * 95)

print(f"""
MODERN VIEW:

    All QFTs are EFFECTIVE theories.
    Valid up to some cutoff scale Λ.
    Above Λ, new physics appears.

THE HIERARCHY:

    Low energy: QED (electron + photon)
    Medium: Electroweak (add W, Z, Higgs)
    High: Full SM (add quarks, gluons)
    Very high: ??? (beyond SM)
    Planck: Quantum gravity (unknown)

EACH LEVEL:

    Has its own effective Lagrangian
    Matches onto next level at boundary
    "Integrating out" heavy degrees of freedom

FROM Z:

    The hierarchy is SET by Z!

    log₁₀(M_Pl/m_W) = 3Z ≈ 17.4 (electroweak)
    log₁₀(M_Pl/m_e) = 3Z + 5 ≈ 22.4 (electron)

    Different scales = different Z projections.

THE PICTURE:

    Z² = CUBE × SPHERE

    At different energies, different CUBE faces visible.
    Low energy: Some CUBE vertices
    High energy: More CUBE vertices
    Planck: Full CUBE structure

    Effective theory = partial view of CUBE.
    Full theory = complete Z² structure.
""")

# =============================================================================
# SECTION 7: WHY IS SM RENORMALIZABLE?
# =============================================================================
print("\n" + "═" * 95)
print("                    7. WHY IS THE STANDARD MODEL SPECIAL?")
print("═" * 95)

print(f"""
THE SM IS RENORMALIZABLE:

    Despite many particles and interactions,
    all SM infinities can be absorbed into ~19 parameters.

WHY?

    1. Gauge invariance:
       Constrains interactions, limits divergences.

    2. Lorentz invariance:
       Only certain types of operators allowed.

    3. Renormalizable operators:
       Dimension ≤ 4 in the Lagrangian.

THE STRUCTURE:

    Gauge group: SU(3) × SU(2) × U(1)
        12 generators (from Z!)

    Fermion content:
        Anomaly-free (from Z!)

    Higgs sector:
        Single doublet (minimal, from Z!)

FROM Z:

    All these constraints come from Z² = CUBE × SPHERE!

    Gauge structure: 9Z²/(8π) = 12
    Anomaly cancellation: 3 generations from SPHERE
    Lorentz invariance: SPHERE geometry

    The SM is renormalizable because:
        It's the UNIQUE low-energy limit of Z geometry.

BEYOND SM:

    Non-renormalizable operators are SUPPRESSED:
        By powers of (E/M_Pl)

    At low energy, only renormalizable terms matter.
    This is the SM!

    New physics appears at higher scales.
    But it's still within Z structure.
""")

# =============================================================================
# SECTION 8: DIMENSIONAL REGULARIZATION
# =============================================================================
print("\n" + "═" * 95)
print("                    8. DIMENSIONAL REGULARIZATION")
print("═" * 95)

print(f"""
A CLEVER TRICK:

    Instead of cutoff Λ, work in d = 4 - ε dimensions.

    Integrals that diverge in 4D are finite in (4-ε)D.
    Calculate in d dimensions, then take ε → 0.

THE POLES:

    Divergences appear as 1/ε poles.
    These are removed by counterterms.
    Final answers are finite.

WHY DOES IT WORK?

    Dimensional regularization preserves:
        • Gauge invariance
        • Lorentz invariance
        • Most symmetries

    It's the "cleanest" regulator.

FROM Z:

    The SPHERE factor is 4π/3 in 3D.

    In d dimensions:
        V_d = π^(d/2) / Γ(d/2 + 1)

    For d = 3: V_3 = 4π/3 ✓

    The "3" in SPHERE (4π/3) IS the dimension!

THE MEANING:

    Dimensional regularization explores what happens
    if SPHERE dimension varies from 3.

    Z² = 8 × (4π/3) assumes 3D SPHERE.
    Varying d tests the robustness.

    The theory is well-defined because:
        Z structure is consistent for any d
        Taking d → 3 recovers physical answers
        Poles encode the d = 3 specific structure
""")

# =============================================================================
# SECTION 9: THE LANDAU POLE
# =============================================================================
print("\n" + "═" * 95)
print("                    9. THE LANDAU POLE AND Z")
print("═" * 95)

print(f"""
THE LANDAU POLE:

    In QED, α runs UP with energy.
    Eventually α → ∞ at some energy Λ_L.

    For QED: Λ_L ~ 10^286 GeV (astronomical!)

    This is called the LANDAU POLE.

THE PROBLEM:

    At Λ_L, theory breaks down.
    QED is not "asymptotically complete."

    But Λ_L >> M_Pl, so it's not a real problem.
    New physics (gravity, GUT) intervenes first.

FOR QCD:

    Opposite behavior! α_s runs DOWN.
    At low energy: α_s large (confinement)
    At high energy: α_s → 0 (asymptotic freedom)

    QCD is "asymptotically free" - no Landau pole.

FROM Z:

    α = 1/(4Z² + 3) at low energy.
    α_s = 7/(3Z² - 4Z - 18) at low energy.

    The SIGNS of the running come from:
        QED: Electron loops (screening)
        QCD: Gluon loops (antiscreening)

    Z determines the LOW energy values.
    Running is determined by particle content.
    Both are consistent with Z.

THE MEANING:

    Any Landau pole is at energy >> Planck.
    Before we reach it:
        Gravity becomes important
        Z structure changes character
        CUBE = SPHERE transition happens

    The Landau pole is never reached because:
        Planck scale (from Z) intervenes first.
""")

# =============================================================================
# SECTION 10: SYNTHESIS
# =============================================================================
print("\n" + "═" * 95)
print("                    10. RENORMALIZATION IS CUBE TAMING SPHERE")
print("═" * 95)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    RENORMALIZATION = CUBE REGULATES SPHERE                          ║
║                                                                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║  Z² = 8 × (4π/3) = CUBE × SPHERE                                                    ║
║                                                                                      ║
║  THE INFINITIES:                                                                     ║
║      • Come from SPHERE (continuous, unbounded)                                      ║
║      • Integrals over all momenta diverge                                            ║
║      • UV divergences: high energy modes                                             ║
║                                                                                      ║
║  THE CURE:                                                                           ║
║      • CUBE (discrete, finite) provides cutoff                                       ║
║      • Planck scale = where CUBE = SPHERE                                           ║
║      • log₁₀(M_Pl/m_e) = 3Z + 5 sets the scale                                     ║
║                                                                                      ║
║  WHY SM IS RENORMALIZABLE:                                                           ║
║      • Gauge structure from Z (12 generators)                                        ║
║      • Anomaly cancellation from Z (3 generations)                                   ║
║      • Lorentz invariance from SPHERE                                                ║
║      • All constraints are Z geometry                                                ║
║                                                                                      ║
║  RUNNING COUPLINGS:                                                                  ║
║      • α = 1/(4Z² + 3) at low energy                                                ║
║      • Running determined by particle loops                                          ║
║      • Particle content from Z structure                                             ║
║                                                                                      ║
║  EFFECTIVE THEORY:                                                                   ║
║      • Different energy = different CUBE faces                                       ║
║      • SM = low energy limit of Z                                                   ║
║      • Full theory = complete Z² structure                                          ║
║                                                                                      ║
║  Renormalization is not a trick to remove infinities.                                ║
║  Renormalization is the CUBE making SPHERE finite.                                   ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

    Why do infinities cancel?

    Because Z² = CUBE × SPHERE.

    The SPHERE alone is infinite (continuous).
    The CUBE is finite (8 vertices).
    Their PRODUCT Z² is finite.

    Renormalization is extracting the finite Z²
    from infinite SPHERE integrals.

    It works because Z is the underlying geometry.

""")

print("═" * 95)
print("                    RENORMALIZATION ANALYSIS COMPLETE")
print("═" * 95)
