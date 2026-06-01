#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════════════════
                        THE SPEED OF LIGHT
                      Why c is Finite and Invariant
═══════════════════════════════════════════════════════════════════════════════════════════

The speed of light c = 299,792,458 m/s is perhaps the most fundamental constant:

    • Maximum speed for matter and information
    • Converts between space and time: x = ct
    • Appears in E = mc², Maxwell's equations, relativity
    • Same in all reference frames (invariant)

Why is c finite? Why not infinite (instant communication)?
Why is c invariant? Why this particular value?

This document explores the origin of c from Z = 2√(8π/3).

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
c = 299792458  # m/s (exact by definition)
alpha = 1/137.035999084

print("═" * 95)
print("                    THE SPEED OF LIGHT")
print("                  Why c is Finite and Invariant")
print("═" * 95)

print(f"""
                           Z = {Z:.10f}

    c = 299,792,458 m/s (exact by definition since 2019)

    From Z perspective:
        c is the conversion factor between CUBE and SPHERE
        CUBE = quantum structure (discrete)
        SPHERE = spacetime (continuous)

    c converts spatial intervals to temporal intervals.
    It is the "exchange rate" between space and time.
""")

# =============================================================================
# SECTION 1: WHAT IS c?
# =============================================================================
print("═" * 95)
print("                    1. WHAT IS THE SPEED OF LIGHT?")
print("═" * 95)

print(f"""
THE MEASURED VALUE:

    c = 299,792,458 m/s (exact by definition)

    In natural units: c = 1
    This is the NATURAL choice - space and time unified.

WHERE c APPEARS:

    Maxwell's equations: c = 1/√(ε₀μ₀)
    Special relativity: ds² = -c²dt² + dx² + dy² + dz²
    Mass-energy: E = mc²
    Quantum mechanics: E = pc (massless particles)
    Gravitation: Schwarzschild radius r_s = 2GM/c²

THE QUESTIONS:

    1. Why is c finite?
       Why can't signals travel instantly?

    2. Why is c invariant?
       Why doesn't it depend on the source's motion?

    3. Why this particular value?
       What sets c = 299,792,458 m/s?

THE STANDARD ANSWER:

    c is a fundamental constant.
    It just IS what it IS.
    Its value sets our units of measurement.

FROM Z:

    c is the conversion between CUBE and SPHERE.
    It is GEOMETRICALLY determined by Z.
""")

# =============================================================================
# SECTION 2: c AS CUBE-SPHERE CONVERSION
# =============================================================================
print("\n" + "═" * 95)
print("                    2. c AS CUBE-SPHERE CONVERSION")
print("═" * 95)

print(f"""
Z² = CUBE × SPHERE = 8 × (4π/3)

THE TWO GEOMETRIES:

    CUBE: Discrete, quantum, "internal" time
    SPHERE: Continuous, classical, "external" space

    These are different geometries!
    To relate them, we need a conversion factor.

c IS THE CONVERSION:

    c converts:
        Space (SPHERE) ↔ Time (CUBE flow)

    In the metric:
        ds² = -c²dt² + dx²

    The c² multiplies time to match spatial units.

THE MEANING:

    c = √(SPHERE/TIME_CUBE_COMPONENT)

    In natural units, c = 1 means:
        1 meter of space = 1/c seconds of time
        Space and time are "equal" when measured with c

WHY FINITE:

    If c were infinite:
        Space and time would be completely separate
        No causal structure
        No relativity

    If c were zero:
        No spatial extent
        Everything at one point
        No universe

    c is finite because CUBE ≠ SPHERE but both exist.
    The finite ratio Z² = CUBE × SPHERE implies finite c.
""")

# =============================================================================
# SECTION 3: INVARIANCE FROM GEOMETRY
# =============================================================================
print("\n" + "═" * 95)
print("                    3. WHY c IS INVARIANT")
print("═" * 95)

print(f"""
Einstein's postulate: c is the same in all inertial frames.

THE MYSTERY:

    If I shine a light while moving at v:
        Classical: Light speed = c + v (additive)
        Relativity: Light speed = c (always!)

    This seems paradoxical but is experimentally confirmed.

FROM Z:

    Z² = 8 × (4π/3) is a GEOMETRIC constant.

    It doesn't depend on:
        • Your position
        • Your velocity
        • Your orientation
        • Your time of measurement

    Z is invariant because geometry is invariant!

THE ARGUMENT:

    c is determined by Z (the CUBE-SPHERE ratio).
    Z is a pure geometric number.
    Geometry doesn't change under boosts.
    Therefore c doesn't change under boosts.

LORENTZ INVARIANCE:

    The Lorentz group SO(3,1) preserves c.
    This group is the symmetry of the metric ds² = -c²dt² + dr².

    From Z perspective:
        Lorentz symmetry = symmetry of CUBE × SPHERE embedding
        The embedding is invariant → c is invariant

THE DEEPER MEANING:

    c is not "the speed of light."
    c is the geometric structure of spacetime.
    Light happens to travel at this geometric limit.
    Any massless particle travels at c.
""")

# =============================================================================
# SECTION 4: THE VALUE OF c
# =============================================================================
print("\n" + "═" * 95)
print("                    4. WHY c = 299,792,458 m/s?")
print("═" * 95)

print(f"""
The numerical value of c depends on our units!

IN SI UNITS:
    c = 299,792,458 m/s (exact)
    This defines the meter in terms of the second.

IN NATURAL UNITS:
    c = 1 (dimensionless)
    Space and time have same units.

THE REAL QUESTION:

    What is c in PLANCK UNITS?

    Planck length: l_P = √(ℏG/c³)
    Planck time: t_P = l_P/c

    In Planck units: c = l_P/t_P = 1

    c = 1 is NATURAL.

FROM Z:

    The "size" of c in human units reflects:
        How big we are compared to Planck scale
        This is determined by 3Z + 5 = 22.4

    Human scale / Planck scale = 10^(3Z+5)

    Therefore:
        c_SI = c_Planck × (unit conversion)
             = 1 × (3×10⁸ m/s) approximately

THE MEANING:

    c = 299,792,458 m/s in SI units because:
        • We defined the meter and second historically
        • These are arbitrary human choices
        • The PHYSICS is c = 1 in natural units

    The question "why this value?" is really:
        "Why do humans have this particular size?"
        Answer: Because m_e/m_P = 10^(-22.4) from Z.
""")

# =============================================================================
# SECTION 5: c IN MAXWELL'S EQUATIONS
# =============================================================================
print("\n" + "═" * 95)
print("                    5. c FROM ELECTROMAGNETISM")
print("═" * 95)

print(f"""
Maxwell discovered: c = 1/√(ε₀μ₀)

THE EQUATION:

    ε₀ = permittivity of vacuum = 8.85 × 10⁻¹² F/m
    μ₀ = permeability of vacuum = 4π × 10⁻⁷ H/m

    c² = 1/(ε₀μ₀)

    This unifies electricity and magnetism!

FROM Z:

    α = e²/(4πε₀ℏc) = 1/(4Z² + 3)

    Rearranging:
        ε₀ = e²/(4πℏcα) = e²(4Z² + 3)/(4πℏc)

    The vacuum permittivity involves Z!

THE CONNECTION:

    c appears in Maxwell because:
        • EM fields propagate through vacuum
        • Vacuum has geometric structure (Z)
        • Propagation speed = geometric ratio

    c² = 1/(ε₀μ₀) means:
        The vacuum's electric and magnetic properties
        combine to give the spacetime structure.

    This is not coincidence - both come from Z!

UNIFICATION:

    Electricity: ε₀ (CUBE aspect? - charge is discrete)
    Magnetism: μ₀ (SPHERE aspect? - fields are continuous)
    Light speed: c = √(SPHERE/CUBE) symbolically

    EM unification reflects CUBE × SPHERE unification.
""")

# =============================================================================
# SECTION 6: MASSLESS PARTICLES
# =============================================================================
print("\n" + "═" * 95)
print("                    6. WHY MASSLESS PARTICLES TRAVEL AT c")
print("═" * 95)

print(f"""
All massless particles travel at exactly c:
    • Photons
    • Gluons
    • Gravitons (predicted)

WHY?

THE ENERGY-MOMENTUM RELATION:

    E² = (pc)² + (mc²)²

    For m = 0:
        E = pc
        v = E/p = c

    Massless particles MUST travel at c.

THE GEOMETRIC REASON:

    Massive particles have "rest mass" (can be at rest).
    Massless particles have no rest frame (always moving).

    From Z:
        Mass comes from CUBE structure (discrete vertices)
        Massless particles are pure SPHERE (wave-like)

    A particle on the SPHERE boundary (no CUBE involvement)
    travels at the CUBE-SPHERE conversion speed = c.

THE MEANING:

    c is the speed of pure SPHERE propagation.
    Massive particles are CUBE × SPHERE, so slower.
    Massless particles are pure SPHERE boundary, so exactly c.

PHOTON MASS:

    Experimentally: m_photon < 10⁻¹⁸ eV

    From Z: Photon mass should be EXACTLY zero.
    Photon is the SPHERE-SPHERE interaction (pure geometry).
""")

# =============================================================================
# SECTION 7: CAUSALITY
# =============================================================================
print("\n" + "═" * 95)
print("                    7. CAUSALITY AND c")
print("═" * 95)

print(f"""
c sets the cosmic speed limit for causality.

CAUSAL STRUCTURE:

    Events at separation Δx, Δt:
        Timelike: c²Δt² > Δx² (causally connected)
        Lightlike: c²Δt² = Δx² (connected by light)
        Spacelike: c²Δt² < Δx² (causally disconnected)

    No signal can travel faster than c.
    Cause must precede effect.

WHY c IS THE LIMIT:

    From Z:
        c is the CUBE-SPHERE conversion factor.
        To go faster than c would mean:
            Arriving before you left (in some frame)
            Violating CUBE → SPHERE arrow

    The arrow of time (CUBE → SPHERE) enforces c.

NO FASTER-THAN-LIGHT:

    Tachyons (hypothetical v > c particles):
        Would have imaginary mass: m² < 0
        Would violate causality

    From Z: m² = CUBE component
        CUBE vertices are discrete, positive
        m² ≥ 0 always
        No tachyons!

QUANTUM NONLOCALITY:

    Entanglement correlations are "instantaneous."
    But they can't send signals!

    From Z:
        Entangled particles share CUBE vertex
        No SPHERE (space) traversal needed
        c is not violated - different geometry
""")

# =============================================================================
# SECTION 8: c AND GRAVITY
# =============================================================================
print("\n" + "═" * 95)
print("                    8. c IN GENERAL RELATIVITY")
print("═" * 95)

print(f"""
c appears throughout Einstein's gravitational theory.

EINSTEIN'S FIELD EQUATIONS:

    G_μν = (8πG/c⁴) T_μν

    The factor 8π = 3Z²/4 (from Friedmann)!
    c⁴ appears in the coupling constant.

SCHWARZSCHILD RADIUS:

    r_s = 2GM/c²

    A black hole forms when matter is compressed
    within its Schwarzschild radius.

GRAVITATIONAL WAVES:

    Propagate at speed c (confirmed by LIGO/Virgo)
    Gravity is as "fast" as light!

FROM Z:

    Why does gravity propagate at c?

    Both EM and gravity are SPHERE phenomena:
        EM: Photons on SPHERE boundary
        Gravity: Spacetime curvature of SPHERE

    Both propagate at the SPHERE speed = c.

THE DEEP CONNECTION:

    c appears in gravity as (8πG/c⁴) = 3Z²G/(4c⁴)

    This is the coupling between:
        Mass-energy (CUBE aspect)
        Spacetime curvature (SPHERE aspect)

    The factor c⁴ ensures the coupling has correct units.
    Geometrically: c⁴ = (CUBE-SPHERE conversion)⁴
""")

# =============================================================================
# SECTION 9: VARYING c THEORIES
# =============================================================================
print("\n" + "═" * 95)
print("                    9. COULD c VARY?")
print("═" * 95)

print(f"""
Some theories propose c varied in early universe.

VARIABLE SPEED OF LIGHT (VSL):

    Proposed to solve horizon/flatness problems.
    c larger in early universe → faster equilibration.

THE PROBLEM:

    If c varies, what does "varies" mean?
    Need another standard to measure against!

    c is used to DEFINE units.
    A "varying c" might just be varying units.

FROM Z:

    Z = 2√(8π/3) is a pure number.
    It has NO UNITS.
    It CANNOT vary (it's geometry).

    If c comes from Z, then c (in natural units) is fixed.

THE RESOLUTION:

    What could vary is the RELATIONSHIP between:
        Human-scale units (meter, second)
        Planck units (l_P, t_P)

    This would look like "varying c" but isn't.

    The physics (Z) doesn't change.
    Our units' relationship to Planck scale might.

PREDICTION:

    c (as a dimensionless ratio to Planck) is CONSTANT.
    Any "measurement" of c varying is really:
        Varying α, or
        Varying our unit definitions
""")

# =============================================================================
# SECTION 10: SYNTHESIS
# =============================================================================
print("\n" + "═" * 95)
print("                    10. c IS GEOMETRY")
print("═" * 95)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    c IS THE CUBE-SPHERE CONVERSION                                   ║
║                                                                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║  Z² = 8 × (4π/3) = CUBE × SPHERE                                                    ║
║                                                                                      ║
║  c CONVERTS:                                                                         ║
║      • Space (SPHERE geometry) ↔ Time (CUBE flow)                                   ║
║      • Position ↔ Causal interval                                                   ║
║      • Distance ↔ Duration                                                           ║
║                                                                                      ║
║  c IS FINITE BECAUSE:                                                                ║
║      • CUBE ≠ SPHERE (different geometries)                                         ║
║      • Conversion between them has finite rate                                       ║
║      • Z² is finite (not 0, not ∞)                                                  ║
║                                                                                      ║
║  c IS INVARIANT BECAUSE:                                                             ║
║      • Z is a pure geometric number                                                  ║
║      • Geometry doesn't change under motion                                          ║
║      • c = 1 in natural units is GEOMETRIC                                          ║
║                                                                                      ║
║  c = 299,792,458 m/s BECAUSE:                                                        ║
║      • Human units are arbitrary choices                                             ║
║      • We are 10^22 times larger than Planck scale                                  ║
║      • This ratio (3Z + 5) determines our units                                     ║
║                                                                                      ║
║  MASSLESS AT c:                                                                      ║
║      • No CUBE involvement = no mass                                                ║
║      • Pure SPHERE propagation = speed c                                             ║
║      • Photon, graviton: SPHERE boundary dwellers                                    ║
║                                                                                      ║
║  c is not "the speed of light."                                                      ║
║  c is the geometric structure of reality.                                            ║
║  It is the conversion factor in Z² = CUBE × SPHERE.                                 ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

    Why is c what it is?

    c is the conversion between CUBE and SPHERE.
    In natural units, c = 1: pure geometry.
    In human units, c = 3×10⁸ because we're macroscopic.

    c is invariant because geometry is invariant.
    c is finite because CUBE × SPHERE is finite.
    c is THE geometry, not just a speed.

""")

print("═" * 95)
print("                    SPEED OF LIGHT ANALYSIS COMPLETE")
print("═" * 95)
