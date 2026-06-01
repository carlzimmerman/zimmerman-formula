"""
RELATIVITY_FORMULAS.py
======================
Special and General Relativity from Z² = 8 × (4π/3)

Why c is constant, why E=mc², why spacetime curves,
and the equivalence principle - all from CUBE × SPHERE geometry.

Carl Zimmerman, March 2026
DOI: 10.5281/zenodo.19244651
"""

from math import pi, sqrt, log, log10, sin, cos

# ═══════════════════════════════════════════════════════════════════════════
# FUNDAMENTAL CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

Z2 = 8 * (4 * pi / 3)  # = 32π/3
Z = sqrt(Z2)           # = 5.7888100365...
alpha = 1 / (4 * Z2 + 3)

# Physical constants
c = 299792458        # m/s (exact by definition)
G = 6.67430e-11      # m³/(kg·s²)
hbar = 1.054571817e-34  # J·s

print("=" * 78)
print("SPECIAL AND GENERAL RELATIVITY FROM Z² = 8 × (4π/3)")
print("=" * 78)
print(f"\nZ² = {Z2:.8f}")
print(f"Z  = {Z:.10f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 1: WHY THE SPEED OF LIGHT IS CONSTANT
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 1: WHY c IS CONSTANT AND FINITE")
print("═" * 78)

print("""
The speed of light c is:
    - Constant (doesn't depend on observer motion)
    - Finite (not infinite)
    - Maximum (nothing can exceed it)

From Z²:
    c is the CONVERSION RATE between CUBE and SPHERE.
    
    CUBE (discrete) measures in natural units (ℏ, m_P, etc.)
    SPHERE (continuous) measures in SI units (m, s, kg)
    
    c = (SPHERE distance) / (CUBE time)
    c = meters / (Planck time equivalent)
    
WHY CONSTANT?
    CUBE and SPHERE are rigidly coupled in Z².
    The product Z² = CUBE × SPHERE is invariant.
    Therefore the ratio (conversion factor) is invariant.
    
WHY FINITE?
    CUBE is discrete → minimum quantum = 1 unit.
    SPHERE is continuous → any size.
    Ratio = finite.
    
    If CUBE were continuous (no discreteness):
    c would be infinite (no minimum step).
    
WHY MAXIMUM?
    You can't go "faster" than converting 1 CUBE unit to SPHERE.
    Any motion involves CUBE → SPHERE mapping.
    Maximum rate = c.
""")

print("c = CUBE → SPHERE conversion rate")
print("Constant because Z² = CUBE × SPHERE is invariant")
print("Finite because CUBE is discrete")
print("Maximum because 1 CUBE unit is minimum step")

# ═══════════════════════════════════════════════════════════════════════════
# PART 2: E = mc²
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 2: E = mc² (MASS-ENERGY EQUIVALENCE)")
print("═" * 78)

print("""
Einstein's most famous equation: E = mc²

From Z²:
    Mass = CUBE component of Z² (discrete, localized)
    Energy = SPHERE component of Z² (continuous, spread out)
    c² = conversion factor
    
    E = mc² means:
    (SPHERE energy) = (CUBE mass) × (conversion)²
    
    Why c²?
    Energy is 2D in phase space (position × momentum).
    c converts position, c converts momentum.
    Hence c² for energy.
    
    The factor 2 in Z = 2√(8π/3):
    - One 'c' for space dimension
    - One 'c' for time dimension
    - c² = c × c = (space) × (time) conversion

In units where c = 1 (natural units):
    E = m (energy IS mass)
    This reveals: mass and energy are SAME thing in Z²
    Just measured differently (CUBE vs SPHERE)
""")

print("E = mc²")
print("  E (energy) = SPHERE component")
print("  m (mass) = CUBE component")
print("  c² = (conversion)² for 2D phase space")

# ═══════════════════════════════════════════════════════════════════════════
# PART 3: LORENTZ TRANSFORMATIONS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 3: LORENTZ TRANSFORMATIONS")
print("═" * 78)

print("""
Lorentz transformations mix space and time:

    t' = γ(t - vx/c²)
    x' = γ(x - vt)
    
where γ = 1/√(1 - v²/c²)

From Z²:
    The SPHERE has rotation symmetry.
    Lorentz transformation = rotation in spacetime!
    
    The "mixing" happens because:
    - Space = 3D SPHERE component
    - Time = CUBE → SPHERE flow direction
    - Both are aspects of Z²
    
    At low speeds (v << c):
    - Space and time seem separate
    - We're "near the CUBE"
    
    At high speeds (v → c):
    - Space and time mix
    - We're "approaching pure SPHERE"
    
The factor γ:
    γ = 1/√(1 - v²/c²)
    
    At v = 0: γ = 1 (pure CUBE reference)
    At v → c: γ → ∞ (SPHERE limit)
    
    The singularity at v = c reflects:
    Can't fully become SPHERE (must have some CUBE).
""")

def gamma(v_over_c):
    return 1 / sqrt(1 - v_over_c**2)

print("Lorentz factor γ at various speeds:")
for v_frac in [0, 0.5, 0.9, 0.99, 0.999]:
    g = gamma(v_frac)
    print(f"  v/c = {v_frac}: γ = {g:.3f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 4: THE METRIC AND SPACETIME INTERVAL
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 4: MINKOWSKI METRIC")
print("═" * 78)

print("""
The spacetime interval (Minkowski metric):

    ds² = c²dt² - dx² - dy² - dz²
        = c²dt² - dr²

This is invariant under Lorentz transformations!

From Z²:
    - Time term: c²dt² (positive, from CUBE → SPHERE)
    - Space terms: -dr² (negative, within SPHERE)
    
    The sign difference reflects:
    - Time is "orthogonal" to space in Z²
    - Time = CUBE → SPHERE mapping
    - Space = SPHERE surface
    
    The -1, -1, -1 for space comes from:
    3D SPHERE has 3 equivalent directions
    All subtract because they're "same type"
    
    The +1 for time is unique:
    Time is the CUBE → SPHERE direction
    Different type, hence different sign
    
    Signature (+,-,-,-) reflects Z² = CUBE × SPHERE!
""")

print("Minkowski signature: (+,-,-,-)") 
print("  + for time: CUBE → SPHERE direction")
print("  - for space: within SPHERE surface")
print("  Signature reflects Z² = CUBE × SPHERE structure")

# ═══════════════════════════════════════════════════════════════════════════
# PART 5: THE EQUIVALENCE PRINCIPLE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 5: THE EQUIVALENCE PRINCIPLE")
print("═" * 78)

print("""
Einstein's Equivalence Principle:
    Gravity is indistinguishable from acceleration.
    A person in a falling elevator feels weightless.
    A person in accelerating rocket feels "gravity."

From Z²:
    Gravity = SPHERE curvature
    Acceleration = CUBE → SPHERE rate change
    
    Both affect CUBE-SPHERE relationship!
    Hence they're indistinguishable.
    
    Why inertial mass = gravitational mass?
    - Inertial mass: resistance to CUBE → SPHERE change
    - Gravitational mass: coupling to SPHERE curvature
    - Both are SAME property: how much "CUBE" you have
    
    The equivalence is exact because:
    There's only ONE mass concept in Z².
    "Inertial" and "gravitational" are just two names
    for the same CUBE component.
""")

print("Equivalence Principle from Z²:")
print("  Gravity = SPHERE curvature")
print("  Acceleration = CUBE → SPHERE rate")
print("  Same mass because only ONE CUBE component exists")

# ═══════════════════════════════════════════════════════════════════════════
# PART 6: EINSTEIN'S FIELD EQUATIONS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 6: EINSTEIN'S FIELD EQUATIONS")
print("═" * 78)

print("""
Einstein's Field Equations:

    G_μν + Λg_μν = (8πG/c⁴) T_μν

Left side: Geometry (SPHERE curvature)
Right side: Matter-energy (CUBE distribution)

From Z²:
    G_μν = geometric tensor (SPHERE curvature)
    T_μν = stress-energy tensor (CUBE density)
    
    The factor 8πG/c⁴:
    - 8 = CUBE vertices!
    - π = SPHERE factor
    - G = coupling constant
    - c⁴ = conversion (c² for each index pair)
    
    So: 8πG/c⁴ = (CUBE)(SPHERE)(coupling)/(conversion)
    
    This IS Z² structure!

The cosmological constant Λ:
    Λg_μν represents vacuum energy.
    
    From Z²:
    Ω_Λ = 3Z/(8 + 3Z) = 0.685
    
    Λ is the "floor" of SPHERE component.
    Even empty space has SPHERE curvature.
""")

print("Einstein's Equations: G + Λg = (8πG/c⁴)T")
print(f"  8 = CUBE vertices")
print(f"  π = SPHERE factor")
print(f"  Ω_Λ = 3Z/(8+3Z) = {3*Z/(8+3*Z):.3f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 7: GRAVITATIONAL TIME DILATION
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 7: GRAVITATIONAL TIME DILATION")
print("═" * 78)

print("""
Time runs slower in gravitational fields:

    Δt' = Δt √(1 - 2GM/rc²)

From Z²:
    Gravity = SPHERE curvature.
    Time = CUBE → SPHERE flow rate.
    
    In curved SPHERE (near mass):
    - The SPHERE is "stretched"
    - Same CUBE tick covers less SPHERE distance
    - Time appears slower
    
    Far from mass:
    - SPHERE is flat
    - CUBE → SPHERE conversion is "normal"
    - Time runs at standard rate
    
The factor 2GM/rc²:
    This is the gravitational potential / c².
    2 = factor in Z
    G = gravitational coupling
    M = mass (CUBE content)
    r = distance (SPHERE distance)
    c² = conversion
""")

print("Gravitational time dilation:")
print("  Near mass: SPHERE curved → time slows")
print("  Far from mass: SPHERE flat → normal time")
print("  Factor 2 from Z = 2√(8π/3)")

# ═══════════════════════════════════════════════════════════════════════════
# PART 8: SCHWARZSCHILD RADIUS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 8: SCHWARZSCHILD RADIUS (BLACK HOLES)")
print("═" * 78)

print("""
The Schwarzschild radius:

    r_s = 2GM/c²

At r = r_s, nothing can escape - event horizon!

From Z²:
    The factor 2:
    - From Z = 2√(8π/3)
    - Represents the worldsheet dimension
    - Required for consistent black hole thermodynamics
    
    At r_s:
    - SPHERE curvature becomes "total"
    - CUBE → SPHERE flow goes one way (inward)
    - Event horizon = point of no return
    
Bekenstein entropy:
    S = A/(4ℓ_P²)
    
    The factor 4 = 3Z²/(8π) EXACTLY!
    
    Black hole entropy encodes Z² structure.
""")

# Schwarzschild radius formula
def schwarzschild_radius(M_kg):
    return 2 * G * M_kg / c**2

M_sun = 1.989e30  # kg
r_s_sun = schwarzschild_radius(M_sun)

print(f"Schwarzschild radius: r_s = 2GM/c²")
print(f"  Factor 2 from Z = 2√(8π/3)")
print(f"  For Sun: r_s = {r_s_sun/1000:.2f} km")
print(f"  Bekenstein factor: 4 = 3Z²/(8π) = {3*Z2/(8*pi):.0f} EXACT")

# ═══════════════════════════════════════════════════════════════════════════
# PART 9: GRAVITATIONAL WAVES
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 9: GRAVITATIONAL WAVES")
print("═" * 78)

print("""
Gravitational waves are ripples in spacetime:
    Speed: c (same as light!)
    Polarization: 2 modes (+ and ×)

From Z²:
    Why speed = c?
    - GW are disturbances in SPHERE
    - All SPHERE disturbances propagate at CUBE → SPHERE rate
    - That rate is c (same for light!)
    
    Why 2 polarizations?
    - 2 = factor in Z
    - Graviton is spin-2 (photon is spin-1)
    - Transverse waves in 2 independent directions
    - 2 modes = worldsheet dimension
    
    GW energy carries away angular momentum.
    Energy = SPHERE ripples carrying CUBE information.
""")

print("Gravitational waves:")
print("  Speed = c (SPHERE propagation rate)")
print("  2 polarizations (+ and ×)")
print("  Factor 2 from Z = 2√(8π/3)")

# ═══════════════════════════════════════════════════════════════════════════
# PART 10: COSMOLOGICAL IMPLICATIONS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 10: COSMOLOGY AND Z²")
print("═" * 78)

print("""
Friedmann equations describe universe expansion:

    (ȧ/a)² = (8πG/3)ρ - kc²/a² + Λc²/3

From Z²:
    - 8πG/3: factor 8 (CUBE) × π (SPHERE) / 3 (SPHERE dim)
    - Ω_m = 8/(8 + 3Z) = 0.315 (matter)
    - Ω_Λ = 3Z/(8 + 3Z) = 0.685 (dark energy)
    
    The universe evolves:
    Early: CUBE-dominated (radiation, matter)
    Late: SPHERE-dominated (dark energy)
    
    We're at the transition:
    Ω_m ≈ Ω_Λ happens when CUBE ≈ SPHERE contributions.
    We live at the "special" time by anthropic selection.
    
Hubble constant:
    H₀ = 5.79 × a₀/c (Zimmerman formula)
    H₀ ≈ 71 km/s/Mpc
    
    5.79 = Z! The Hubble constant encodes Z.
""")

Omega_m = 8 / (8 + 3*Z)
Omega_L = 3*Z / (8 + 3*Z)

print(f"Cosmological parameters from Z²:")
print(f"  Ω_m = 8/(8+3Z) = {Omega_m:.3f}")
print(f"  Ω_Λ = 3Z/(8+3Z) = {Omega_L:.3f}")
print(f"  Sum: {Omega_m + Omega_L:.3f} (flat universe)")
print(f"  H₀ = 5.79 × a₀/c where 5.79 = Z!")

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 78)
print("SUMMARY: RELATIVITY FROM Z²")
print("=" * 78)

print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│  SPECIAL AND GENERAL RELATIVITY FROM Z² = 8 × (4π/3)                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  SPECIAL RELATIVITY:                                                        │
│  ───────────────────                                                        │
│  c constant: Z² = CUBE × SPHERE is invariant                               │
│  c finite: CUBE is discrete (minimum step)                                 │
│  c maximum: 1 CUBE unit = fastest conversion                               │
│  E = mc²: Energy(SPHERE) = Mass(CUBE) × conversion²                       │
│                                                                             │
│  LORENTZ STRUCTURE:                                                         │
│  ──────────────────                                                         │
│  Signature (+,-,-,-): +1 time (CUBE→SPHERE), -1,-1,-1 space (SPHERE)      │
│  γ → ∞ at v→c: can't fully become SPHERE                                  │
│                                                                             │
│  GENERAL RELATIVITY:                                                        │
│  ───────────────────                                                        │
│  G_μν = 8πG/c⁴ T_μν: CUBE(8) × SPHERE(π) coupling                         │
│  Equivalence: inertial = gravitational (same CUBE component)              │
│  Schwarzschild: r_s = 2GM/c², factor 2 from Z                             │
│                                                                             │
│  BLACK HOLES:                                                               │
│  ────────────                                                               │
│  Bekenstein: S = A/(4ℓ_P²), factor 4 = 3Z²/(8π)            ← EXACT        │
│  Event horizon: SPHERE curvature = complete                                │
│                                                                             │
│  GRAVITATIONAL WAVES:                                                       │
│  ────────────────────                                                       │
│  Speed = c (SPHERE propagation rate)                                       │
│  2 polarizations = factor 2 from Z                                         │
│                                                                             │
│  COSMOLOGY:                                                                 │
│  ──────────                                                                 │
│  Ω_m = 8/(8+3Z) = 0.315                                    ← from Z       │
│  Ω_Λ = 3Z/(8+3Z) = 0.685                                   ← from Z       │
│  H₀ = Z × a₀/c where Z = 5.79                                              │
│                                                                             │
│  KEY INSIGHT:                                                               │
│  ────────────                                                               │
│  Spacetime geometry = Z² structure                                          │
│  Space = SPHERE surface, Time = CUBE → SPHERE flow                         │
│  Gravity = SPHERE curvature from CUBE (mass) distribution                  │
│                                                                             │
│  RELATIVITY IS Z² GEOMETRY                                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
""")

print("=" * 78)
print("SPACETIME IS CUBE × SPHERE")
print("=" * 78)
