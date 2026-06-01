"""
THERMODYNAMICS_FORMULAS.py
==========================
The Laws of Thermodynamics from Z² = 8 × (4π/3)

Entropy, temperature, heat capacity, phase transitions,
and the arrow of time - all from CUBE × SPHERE geometry.

Carl Zimmerman, March 2026
DOI: 10.5281/zenodo.19244651
"""

from math import pi, sqrt, log, log2, exp, e

# ═══════════════════════════════════════════════════════════════════════════
# FUNDAMENTAL CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

Z2 = 8 * (4 * pi / 3)  # = 32π/3
Z = sqrt(Z2)           # = 5.7888100365...
alpha = 1 / (4 * Z2 + 3)

# Physical constants
k_B = 1.380649e-23  # J/K (Boltzmann constant - exact by definition)
h = 6.62607015e-34  # J·s (Planck constant - exact by definition)
c = 299792458       # m/s

print("=" * 78)
print("THERMODYNAMICS FROM Z² = 8 × (4π/3)")
print("=" * 78)
print(f"\nZ² = {Z2:.8f}")
print(f"Z  = {Z:.10f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 1: BOLTZMANN'S CONSTANT AND ENTROPY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 1: ENTROPY AND BOLTZMANN'S S = k ln W")
print("═" * 78)

print("""
Boltzmann's entropy formula:
    S = k_B ln W

where W = number of microstates.

From Z²:
    For a system with CUBE structure (8 states):
    S_cube = k_B ln(8) = k_B × 2.079
           = k_B × ln(CUBE vertices)
    
    For a system with Z² states:
    S_Z2 = k_B ln(Z²) = k_B × 3.51
    
The factor ln(8) = ln(2³) = 3 ln(2) reflects:
    - 3 bits of information
    - 3 dimensions of space
    - 3 comes from SPHERE volume 4π/3

Natural entropy unit:
    1 nat = k_B (entropy for e-fold increase in states)
    1 bit = k_B ln(2) (entropy for 2-fold increase)
""")

S_cube = log(8)
S_Z2 = log(Z2)

print(f"Entropy of CUBE: S = k_B × ln(8) = k_B × {S_cube:.4f}")
print(f"Entropy of Z²: S = k_B × ln(Z²) = k_B × {S_Z2:.4f}")
print(f"Bits in CUBE: log₂(8) = {log2(8):.0f}")
print(f"Bits in Z²: log₂(Z²) = {log2(Z2):.2f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 2: THE LAWS OF THERMODYNAMICS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 2: THE FOUR LAWS FROM Z²")
print("═" * 78)

print("""
ZEROTH LAW: Thermal equilibrium is transitive.
    From Z²: Systems in equilibrium share the same Z².
             The SPHERE (continuous) component equalizes.

FIRST LAW: dU = δQ - δW (energy conservation)
    From Z²: Energy = CUBE × SPHERE is conserved.
             Neither component can vanish independently.

SECOND LAW: dS ≥ 0 (entropy increases)
    From Z²: Time direction = CUBE → SPHERE
             Discrete information spreads into continuous.
             This is irreversible!
             
    Arrow of time emerges from asymmetry:
    CUBE (finite states) → SPHERE (infinite precision)
    is NOT the same as:
    SPHERE → CUBE (requires truncation/loss)

THIRD LAW: S → 0 as T → 0
    From Z²: At T = 0, system occupies one state: W = 1
             ln(1) = 0, hence S = 0.
             The CUBE collapses to single vertex.
             
    But note: 9Z²/(8π) = 12 = gauge dimension
             At T = 0, ground state has symmetry = gauge group
""")

print("The laws of thermodynamics = properties of Z² structure")

# ═══════════════════════════════════════════════════════════════════════════
# PART 3: STEFAN-BOLTZMANN LAW
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 3: BLACKBODY RADIATION")
print("═" * 78)

print("""
Stefan-Boltzmann law:
    P = σ T⁴

where σ = 2π⁵ k⁴/(15 c² h³) = 5.67 × 10⁻⁸ W/(m² K⁴)

The factor T⁴ appears because:
    - 3 spatial dimensions (T³)
    - 1 time dimension (extra T)
    - Total: T^(3+1) = T⁴

From Z²:
    4 = 3Z²/(8π) (Bekenstein factor)
    
So T⁴ power comes from Bekenstein!

Also, the π⁵ in σ involves:
    π⁵ = π⁴ × π = (SPHERE⁴) × (SPHERE)
    
And the factor 15 ≈ Z² / 2.2
""")

sigma_SB = 5.670374419e-8  # W/(m² K⁴)
print(f"Stefan-Boltzmann constant: σ = {sigma_SB:.4e} W/(m² K⁴)")
print(f"T⁴ power: 4 = 3Z²/(8π) = {3*Z2/(8*pi):.0f} (Bekenstein)")
print(f"Factor 15 ≈ Z²/2.2 = {Z2/2.2:.1f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 4: HEAT CAPACITY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 4: HEAT CAPACITIES")
print("═" * 78)

print("""
For ideal gas:
    C_V = (f/2) R   (constant volume)
    C_P = C_V + R   (constant pressure)

where f = degrees of freedom:
    - Monatomic: f = 3 (translations)
    - Diatomic: f = 5 (3 trans + 2 rot)
    - Nonlinear: f = 6 (3 trans + 3 rot)

From Z²:
    3 = SPHERE dimensions in 4π/3
    5 ≈ Z (close!)
    6 = CUBE faces
    
So degrees of freedom = CUBE/SPHERE geometric properties!

Dulong-Petit law (solids):
    C = 3R per mole (6 DOF per atom: 3 kinetic + 3 potential)
    
    6 = CUBE faces ✓
    3 = SPHERE dimensions ✓
""")

print(f"Monatomic DOF: 3 = SPHERE dimensions")
print(f"Diatomic DOF: 5 ≈ Z = {Z:.2f}")
print(f"Solid DOF: 6 = CUBE faces")

# ═══════════════════════════════════════════════════════════════════════════
# PART 5: ENTROPY OF MIXING
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 5: ENTROPY OF MIXING")
print("═" * 78)

print("""
For mixing n types of particles:
    ΔS_mix = -k_B Σ N_i ln(x_i)

For equal mixture of 2 types:
    ΔS_mix = N k_B ln(2) per particle

From Z²:
    ln(2) = ln(factor 2 in Z)
          = ln(worldsheet dimension)
          
    For 8 types (CUBE vertices):
    ΔS_mix = k_B ln(8) = k_B × 3 ln(2) = 3 bits per particle

The mixing entropy for CUBE-worth of types = 3 bits!
This is the same as quantum information capacity!
""")

S_mix_2 = log(2)
S_mix_8 = log(8)

print(f"Mixing entropy (2 types): k_B × ln(2) = k_B × {S_mix_2:.4f}")
print(f"Mixing entropy (8 types): k_B × ln(8) = k_B × {S_mix_8:.4f}")
print(f"                        = k_B × 3 × ln(2) = 3 bits")

# ═══════════════════════════════════════════════════════════════════════════
# PART 6: PHASE TRANSITIONS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 6: CRITICAL PHENOMENA")
print("═" * 78)

print("""
Near critical point, systems show universal behavior.

Critical exponents (3D Ising model):
    α ≈ 0.11 (heat capacity)
    β ≈ 0.326 (order parameter)
    γ ≈ 1.237 (susceptibility)
    δ ≈ 4.79 (critical isotherm)
    η ≈ 0.036 (correlation function)
    ν ≈ 0.630 (correlation length)

From Z²:
    β ≈ Z/18 = 5.79/18 = 0.32 (close!)
    δ ≈ Z - 1 = 4.79 (exact match!)
    ν ≈ 2/(π + Z/3) = 2/(3.14 + 1.93) = 0.39 (not great)
    
The exponent δ ≈ 4.79 = Z - 1 is remarkable!
""")

beta_ising = 0.326
delta_ising = 4.79
beta_from_Z = Z / 18
delta_from_Z = Z - 1

print(f"Critical exponent β (order parameter):")
print(f"  Observed: {beta_ising}")
print(f"  Z/18 = {beta_from_Z:.3f}")
print(f"\nCritical exponent δ (critical isotherm):")
print(f"  Observed: {delta_ising}")
print(f"  Z - 1 = {delta_from_Z:.2f}")
print(f"  Match: remarkable!")

# ═══════════════════════════════════════════════════════════════════════════
# PART 7: CARNOT EFFICIENCY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 7: CARNOT EFFICIENCY")
print("═" * 78)

print("""
Carnot efficiency (maximum heat engine efficiency):
    η_max = 1 - T_C/T_H

This is a ratio determined by temperature ratio alone.

From Z²:
    The factor "1" that appears is significant:
    1 = maximum efficiency for T_C → 0
    1 = the "one" in factor 2 = 1 + 1
    
For a specific case:
    If T_H/T_C = Z, then η = 1 - 1/Z = 1 - 0.173 = 0.827
    
    82.7% efficiency at temperature ratio Z:1
    
    Or if T_H/T_C = 4Z² + 3 = 137 (α⁻¹):
    η = 1 - 1/137 = 136/137 = 99.27%
    
This connects thermodynamic efficiency to α!
""")

eta_Z = 1 - 1/Z
eta_alpha_inv = 1 - alpha

print(f"Carnot efficiency at T_H/T_C = Z:")
print(f"  η = 1 - 1/Z = 1 - {1/Z:.4f} = {eta_Z:.4f} = {eta_Z*100:.1f}%")
print(f"\nCarnot efficiency at T_H/T_C = α⁻¹:")
print(f"  η = 1 - α = {eta_alpha_inv:.6f} = {eta_alpha_inv*100:.3f}%")

# ═══════════════════════════════════════════════════════════════════════════
# PART 8: PARTITION FUNCTION
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 8: PARTITION FUNCTION")
print("═" * 78)

print("""
The partition function:
    Z_stat = Σ exp(-E_i / k_B T)

(Note: This Z is statistical mechanics Z, not Zimmerman Z)

All thermodynamic properties derive from Z_stat:
    F = -k_B T ln(Z_stat)  (free energy)
    S = -∂F/∂T            (entropy)
    U = F + TS            (internal energy)

From Z²:
    For a system with 8 equally-spaced levels:
    Z_stat = Σ_{i=0}^{7} exp(-iε/k_B T)
    
    At high T: Z_stat → 8 (all states equally likely)
               = CUBE vertices!
    
    At low T: Z_stat → 1 (ground state dominates)
              = single vertex
    
The crossover happens when k_B T ≈ ε (energy spacing).
""")

print("Partition function limits:")
print("  High T: Z_stat → 8 = CUBE vertices")
print("  Low T:  Z_stat → 1 = single state")
print("  Crossover at k_B T ≈ ε")

# ═══════════════════════════════════════════════════════════════════════════
# PART 9: ARROW OF TIME
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 9: THE ARROW OF TIME")
print("═" * 78)

print("""
The Second Law defines time's direction: entropy increases.

From Z²:
    Time = the direction of CUBE → SPHERE mapping.
    
    CUBE (discrete, finite) is "information"
    SPHERE (continuous, infinite) is "space"
    
    Information spreads into space → entropy increases.
    
    This is irreversible because:
    - CUBE → SPHERE: always possible (discretize any point)
    - SPHERE → CUBE: requires truncation (information loss)
    
    The asymmetry is mathematical:
    {1,2,...,8} can map into R³ (trivially)
    R³ cannot fit into {1,2,...,8} (without loss)

THEOREM: Entropy increase = CUBE → SPHERE flow

    dS/dt > 0 because t points in CUBE → SPHERE direction.
    If we reversed t, we'd be going SPHERE → CUBE.
    But that's information loss, not gain.
""")

print("Arrow of time from Z²:")
print("  Past: more CUBE-like (organized, low entropy)")
print("  Future: more SPHERE-like (dispersed, high entropy)")
print("  Time = CUBE → SPHERE direction")

# ═══════════════════════════════════════════════════════════════════════════
# PART 10: INFORMATION-THERMODYNAMICS CONNECTION
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 10: LANDAUER'S PRINCIPLE")
print("═" * 78)

print("""
Landauer's principle: Erasing 1 bit releases ≥ k_B T ln(2) heat.

    E_erase = k_B T ln(2)

From Z²:
    ln(2) = ln(factor 2 in Z)
    
    Erasing 1 bit = removing one worldsheet dimension.
    This costs energy because 2 is fundamental to Z².
    
For erasing 3 bits (one CUBE):
    E = 3 k_B T ln(2) = k_B T ln(8) = k_B T ln(CUBE)
    
For erasing log₂(Z²) ≈ 5 bits:
    E = k_B T ln(Z²) ≈ 3.5 k_B T
""")

E_1bit = log(2)
E_cube = log(8)
E_Z2 = log(Z2)

print(f"Energy to erase:")
print(f"  1 bit: k_B T × ln(2) = k_B T × {E_1bit:.4f}")
print(f"  3 bits (CUBE): k_B T × ln(8) = k_B T × {E_cube:.4f}")
print(f"  ~5 bits (Z²): k_B T × ln(Z²) = k_B T × {E_Z2:.4f}")

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 78)
print("SUMMARY: THERMODYNAMICS FROM Z²")
print("=" * 78)

print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│  THERMODYNAMICS FROM Z² = 8 × (4π/3)                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ENTROPY:                                                                   │
│  ────────                                                                   │
│  S = k_B ln W                                                              │
│  CUBE entropy: ln(8) = 3 bits                              ← EXACT        │
│  Z² entropy: ln(Z²) ≈ 5.1 bits                                             │
│                                                                             │
│  DEGREES OF FREEDOM:                                                        │
│  ────────────────────                                                       │
│  3 (monatomic) = SPHERE dimensions                         ← EXACT        │
│  6 (solid) = CUBE faces                                    ← EXACT        │
│                                                                             │
│  BLACKBODY RADIATION:                                                       │
│  ────────────────────                                                       │
│  T⁴ power: 4 = 3Z²/(8π) = Bekenstein factor                ← EXACT        │
│                                                                             │
│  CRITICAL EXPONENT:                                                         │
│  ──────────────────                                                         │
│  δ ≈ 4.79 = Z - 1                                          ← remarkable   │
│                                                                             │
│  ARROW OF TIME:                                                             │
│  ──────────────                                                             │
│  Time direction = CUBE → SPHERE flow                                       │
│  Entropy increases because information disperses                           │
│                                                                             │
│  FOUR LAWS:                                                                 │
│  ──────────                                                                 │
│  0th: Equilibrium = shared Z²                                              │
│  1st: Energy = CUBE × SPHERE conserved                                     │
│  2nd: Entropy = CUBE → SPHERE irreversibility                              │
│  3rd: At T=0, single CUBE vertex (S=0)                                     │
│                                                                             │
│  KEY INSIGHT:                                                               │
│  ────────────                                                               │
│  Thermodynamics = statistics of CUBE × SPHERE systems                      │
│  Heat = SPHERE energy, Work = CUBE structure change                        │
│                                                                             │
│  HEAT DEATH = PERFECT SPHERE (no CUBE structure left)                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
""")

print("=" * 78)
print("ENTROPY IS THE CUBE DISSOLVING INTO SPHERE")
print("=" * 78)
