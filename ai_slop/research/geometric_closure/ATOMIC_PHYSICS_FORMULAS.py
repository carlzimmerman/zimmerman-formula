"""
ATOMIC_PHYSICS_FORMULAS.py
==========================
Deriving Atomic and Molecular Physics from Z² = 8 × (4π/3)

Bohr radius, Rydberg constant, ionization energies, fine structure,
and atomic transitions - all connected to Z² geometry.

Carl Zimmerman, March 2026
DOI: 10.5281/zenodo.19244651
"""

from math import pi, sqrt, log10

# ═══════════════════════════════════════════════════════════════════════════
# FUNDAMENTAL CONSTANTS
# ═══════════════════════════════════════════════════════════════════════════

Z2 = 8 * (4 * pi / 3)  # = 32π/3
Z = sqrt(Z2)           # = 5.7888100365...

# Fine structure constant from Z²
alpha = 1 / (4 * Z2 + 3)  # = 1/137.04

# Physical constants
c = 299792458           # m/s
hbar = 1.054571817e-34  # J·s
e = 1.602176634e-19     # C
m_e = 9.1093837015e-31  # kg
epsilon_0 = 8.8541878128e-12  # F/m

print("=" * 78)
print("ATOMIC PHYSICS FROM Z² = 8 × (4π/3)")
print("=" * 78)
print(f"\nZ² = {Z2:.8f}")
print(f"Z  = {Z:.10f}")
print(f"α  = 1/(4Z² + 3) = {alpha:.10f} = 1/{1/alpha:.2f}")

# ═══════════════════════════════════════════════════════════════════════════
# PART 1: BOHR RADIUS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 1: BOHR RADIUS")
print("═" * 78)

print("""
The Bohr radius is the characteristic size of atoms:

    a₀ = ℏ/(m_e c α) = 4πε₀ℏ²/(m_e e²)

This can be written as:
    a₀ = ℏ/(m_e c) × (4Z² + 3)

Since α = 1/(4Z² + 3), the Bohr radius is:
    a₀ = (Compton wavelength) × (4Z² + 3)

The factor (4Z² + 3) = 137.04 sets the atomic scale!
""")

# Compton wavelength
lambda_C = hbar / (m_e * c)
# Bohr radius
a_0_calc = lambda_C / alpha
a_0_obs = 5.29177210903e-11  # m

print(f"Compton wavelength: λ_C = ℏ/(m_e c) = {lambda_C:.4e} m")
print(f"Bohr radius: a₀ = λ_C/α = λ_C × (4Z² + 3)")
print(f"           = {lambda_C:.4e} × {1/alpha:.2f}")
print(f"           = {a_0_calc:.4e} m")
print(f"Observed:    {a_0_obs:.4e} m")
print(f"Error: {abs(a_0_calc - a_0_obs)/a_0_obs * 100:.3f}%")

# ═══════════════════════════════════════════════════════════════════════════
# PART 2: RYDBERG CONSTANT
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 2: RYDBERG CONSTANT")
print("═" * 78)

print("""
The Rydberg constant determines atomic energy levels:

    R_∞ = m_e c α² / (2h) = m_e e⁴ / (8ε₀²h³c)

From Z²:
    R_∞ = m_e c / (2h × (4Z² + 3)²)

The Rydberg energy:
    E_R = hc R_∞ = m_e c² α² / 2 = 13.6 eV

In terms of Z²:
    E_R = m_e c² / (2 × (4Z² + 3)²)
        = 0.511 MeV / (2 × 137²)
        = 0.511e6 / 37538 eV
        = 13.6 eV ✓
""")

# Rydberg constant
R_inf_calc = m_e * c * alpha**2 / (2 * 2 * pi * hbar)
R_inf_obs = 1.0973731568160e7  # m⁻¹

# Rydberg energy in eV
E_R_calc = m_e * c**2 * alpha**2 / 2 / e  # in eV
E_R_obs = 13.605693122994  # eV

print(f"Rydberg constant:")
print(f"  R_∞ = m_e c α²/(4πℏ) = {R_inf_calc:.6e} m⁻¹")
print(f"  Observed: {R_inf_obs:.6e} m⁻¹")
print(f"  Error: {abs(R_inf_calc - R_inf_obs)/R_inf_obs * 100:.4f}%")
print(f"\nRydberg energy:")
print(f"  E_R = m_e c² α²/2 = m_e c²/(2×(4Z²+3)²)")
print(f"      = {m_e * c**2 / e / 1e6:.4f} MeV / (2 × {(4*Z2+3)**2:.0f})")
print(f"      = {E_R_calc:.4f} eV")
print(f"  Observed: {E_R_obs:.4f} eV")
print(f"  Error: {abs(E_R_calc - E_R_obs)/E_R_obs * 100:.3f}%")

# ═══════════════════════════════════════════════════════════════════════════
# PART 3: HYDROGEN ENERGY LEVELS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 3: HYDROGEN ENERGY LEVELS")
print("═" * 78)

print("""
Hydrogen energy levels:
    E_n = -E_R / n² = -13.6 eV / n²

The principal quantum number n = 1, 2, 3, ...

Balmer series (visible): transitions to n=2
    - H-α: 3→2 (656 nm, red)
    - H-β: 4→2 (486 nm, cyan)
    - H-γ: 5→2 (434 nm, violet)

Wavelengths:
    λ = hc / ΔE = hc / (E_R × (1/n₁² - 1/n₂²))
""")

def hydrogen_energy(n):
    return -E_R_calc / n**2

def transition_wavelength(n1, n2):
    dE = abs(hydrogen_energy(n1) - hydrogen_energy(n2))  # eV
    wavelength = 1240 / dE  # nm (using hc ≈ 1240 eV·nm)
    return wavelength

print("Hydrogen energy levels:")
for n in range(1, 6):
    print(f"  n={n}: E = {hydrogen_energy(n):.4f} eV")

print("\nBalmer series (visible transitions to n=2):")
balmer = [(3, "H-α", 656.3), (4, "H-β", 486.1), (5, "H-γ", 434.0)]
for n, name, obs_nm in balmer:
    calc_nm = transition_wavelength(2, n)
    print(f"  {name} ({n}→2): λ = {calc_nm:.1f} nm (obs: {obs_nm} nm)")

# ═══════════════════════════════════════════════════════════════════════════
# PART 4: FINE STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 4: FINE STRUCTURE SPLITTING")
print("═" * 78)

print("""
Fine structure comes from relativistic and spin-orbit effects:

    ΔE_fs / E_n ~ α² / n

The splitting is proportional to α² = 1/(4Z² + 3)²

For hydrogen ground state:
    ΔE_fs ~ E_R × α² ~ 13.6 eV × (1/137)² ~ 0.7 meV

This is the "fine" in fine structure constant!
The factor (4Z² + 3)² = 137² determines how small the splitting is.
""")

# Fine structure splitting estimate
dE_fs = E_R_calc * alpha**2  # eV
print(f"Fine structure scale:")
print(f"  ΔE_fs ~ E_R × α² = {E_R_calc:.2f} × ({alpha:.6f})²")
print(f"        = {dE_fs * 1000:.4f} meV")
print(f"        = {dE_fs * 1e6:.2f} µeV")

# 21 cm line (hyperfine)
E_21cm = 5.9e-6  # eV
lambda_21cm = 1240e-9 / E_21cm  # nm -> m
print(f"\n21 cm line (hyperfine splitting):")
print(f"  E = {E_21cm*1e6:.2f} µeV")
print(f"  λ = {lambda_21cm*100:.1f} cm")
print(f"  This is α times smaller than fine structure!")

# ═══════════════════════════════════════════════════════════════════════════
# PART 5: ATOMIC SIZE SCALING
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 5: ATOMIC SIZE SCALING")
print("═" * 78)

print("""
Atoms scale with atomic number Z_atom:

    Radius: r ~ a₀ × n² / Z_atom
    Energy: E ~ E_R × Z_atom² / n²

The Bohr radius a₀ = 0.529 Å sets the fundamental scale.

From Z²:
    a₀ = (ℏ/m_e c) × (4Z² + 3)
       = 3.86e-13 m × 137.04
       = 5.29e-11 m ✓

All atomic sizes derive from (4Z² + 3) = α⁻¹!
""")

print(f"Atomic scales from Z²:")
print(f"  Compton wavelength: λ_C = {lambda_C:.4e} m")
print(f"  Factor: 4Z² + 3 = {4*Z2 + 3:.2f}")
print(f"  Bohr radius: a₀ = λ_C × (4Z²+3) = {lambda_C * (4*Z2+3):.4e} m")
print(f"  Observed: {a_0_obs:.4e} m")

# Ratio check
print(f"\nScale hierarchy:")
print(f"  a₀ / λ_C = {a_0_obs/lambda_C:.2f} = α⁻¹ ✓")

# ═══════════════════════════════════════════════════════════════════════════
# PART 6: IONIZATION ENERGIES
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 6: IONIZATION ENERGIES")
print("═" * 78)

print("""
First ionization energy scales with Z_atom²:

    IE = E_R × Z_eff² ≈ 13.6 eV × Z_eff²

For hydrogen-like ions:
    H:  13.6 eV (Z=1)
    He⁺: 54.4 eV (Z=2)
    Li²⁺: 122.4 eV (Z=3)

All set by E_R = m_e c² / (2 × (4Z²+3)²)
""")

print("Ionization energies (hydrogen-like):")
for Z_atom in range(1, 6):
    IE = E_R_calc * Z_atom**2
    print(f"  Z={Z_atom}: IE = {IE:.2f} eV")

# ═══════════════════════════════════════════════════════════════════════════
# PART 7: MAGNETIC MOMENTS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("PART 7: ELECTRON MAGNETIC MOMENT")
print("═" * 78)

print("""
The electron magnetic moment (g-factor):

    g_e = 2 × (1 + a_e)

where a_e is the anomalous magnetic moment.

Leading QED correction:
    a_e ≈ α/(2π) = 1/(2π × (4Z² + 3))

From Z²:
    a_e ≈ 1/(2π × 137.04) = 0.00116

Observed: a_e = 0.00115965...

The anomaly comes directly from α = 1/(4Z² + 3)!
""")

a_e_pred = alpha / (2 * pi)
a_e_obs = 0.00115965218128

print(f"Electron anomalous magnetic moment:")
print(f"  a_e (leading order) = α/(2π)")
print(f"                      = 1/(2π × (4Z² + 3))")
print(f"                      = 1/(2π × {4*Z2+3:.2f})")
print(f"                      = {a_e_pred:.8f}")
print(f"  Observed: {a_e_obs:.11f}")
print(f"  Error: {abs(a_e_pred - a_e_obs)/a_e_obs * 100:.3f}%")
print(f"  (Higher order QED corrections needed for full precision)")

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 78)
print("SUMMARY: ATOMIC PHYSICS FROM Z²")
print("=" * 78)

print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│  ATOMIC PHYSICS FROM Z² = 8 × (4π/3)                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FINE STRUCTURE CONSTANT:                                                   │
│  ────────────────────────                                                   │
│  α = 1/(4Z² + 3) = 1/137.04                              ← 0.004% error    │
│                                                                             │
│  BOHR RADIUS:                                                               │
│  ────────────                                                               │
│  a₀ = (ℏ/m_e c) × (4Z² + 3) = 5.29 × 10⁻¹¹ m           ← from Z²         │
│                                                                             │
│  RYDBERG ENERGY:                                                            │
│  ───────────────                                                            │
│  E_R = m_e c² / (2 × (4Z²+3)²) = 13.6 eV                ← from Z²         │
│                                                                             │
│  HYDROGEN SPECTRUM:                                                         │
│  ──────────────────                                                         │
│  E_n = -13.6 eV / n²                                                       │
│  H-α: 656 nm, H-β: 486 nm, H-γ: 434 nm                  ← all from Z²     │
│                                                                             │
│  FINE STRUCTURE:                                                            │
│  ───────────────                                                            │
│  ΔE_fs ~ E_R × α² ~ 0.7 meV                             ← α from Z²       │
│                                                                             │
│  MAGNETIC MOMENT:                                                           │
│  ────────────────                                                           │
│  a_e ≈ α/(2π) = 0.00116                                 ← α from Z²       │
│                                                                             │
│  KEY INSIGHT:                                                               │
│  ────────────                                                               │
│  ALL atomic physics depends on α = 1/(4Z² + 3)                             │
│  The factor (4Z² + 3) = 137 sets the scale of atoms!                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
""")

print("=" * 78)
print("ATOMS ARE Z² GEOMETRY")
print("=" * 78)
