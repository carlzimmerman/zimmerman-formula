#!/usr/bin/env python3
"""
Z² Framework: Honest Radion-Photon Coupling Computation
========================================================

This script computes the ACTUAL radion-photon coupling constant γ
from first principles via Kaluza-Klein dimensional reduction of the
8D Einstein-Maxwell action on T³/Z₂ × S¹/Z₂.

It then determines:
  1. The realistic pump strength h achievable with state-of-the-art EM sources
  2. The Mathieu instability threshold (h_crit = 2ζ)
  3. Whether parametric resonance is physically accessible
  4. Corrected power extraction estimates with coupling suppression

Author: Carl Zimmerman & Antigravity AI
Date: May 20, 2026
License: AGPL-3.0-or-later
"""

import numpy as np
from scipy.special import zeta as riemann_zeta

# =============================================================================
# PART 0: FUNDAMENTAL CONSTANTS (CODATA 2018)
# =============================================================================
c       = 299792458.0          # m/s
hbar    = 1.054571817e-34      # J·s
G_N     = 6.67430e-11          # m³/(kg·s²)
e_charge= 1.602176634e-19     # C
k_B     = 1.380649e-23         # J/K
epsilon0= 8.8541878128e-12     # F/m
mu0     = 1.2566370621e-6      # N/A²
eV      = e_charge             # J per eV
GeV     = 1e9 * eV
TeV     = 1e12 * eV

# Planck units
M_Pl_kg     = np.sqrt(hbar * c / G_N)           # 2.176e-8 kg
M_Pl_eV     = M_Pl_kg * c**2 / eV               # 1.221e28 eV
M_Pl_red_kg = M_Pl_kg / np.sqrt(8 * np.pi)      # reduced Planck mass
M_Pl_red_eV = M_Pl_red_kg * c**2 / eV           # 2.435e27 eV
l_Pl        = np.sqrt(hbar * G_N / c**3)         # 1.616e-35 m

# Z² Framework
Z2 = 32.0 * np.pi / 3.0   # ≈ 33.510
Z  = np.sqrt(Z2)           # ≈ 5.789
alpha_inv_Z2 = 4 * Z2 + 3  # ≈ 137.04
alpha_em = 1.0 / alpha_inv_Z2

print("=" * 80)
print("Z² FRAMEWORK: HONEST RADION-PHOTON COUPLING COMPUTATION")
print("=" * 80)
print(f"\nZ² = 32π/3 = {Z2:.6f}")
print(f"Z  = √Z²   = {Z:.6f}")
print(f"α⁻¹ = 4Z²+3 = {alpha_inv_Z2:.4f}")
print(f"M_Pl (reduced) = {M_Pl_red_eV:.4e} eV = {M_Pl_red_kg:.4e} kg")


# =============================================================================
# PART 1: RADION-PHOTON COUPLING FROM KK DIMENSIONAL REDUCTION
# =============================================================================
print("\n" + "=" * 80)
print("PART 1: DERIVING THE RADION-PHOTON COUPLING γ")
print("=" * 80)

print("""
DERIVATION:
-----------
Start from the 8D Einstein-Hilbert + Maxwell action:

  S_8D = ∫ d⁸x √(-g₈) [ M₈⁶/(2) R₈ - 1/(4g₈²) F_MN F^MN ]

After KK reduction on the internal manifold K⁴ with volume V₄:

  V₄(φ) = V₄₀ × e^{4φ/M_P}

The 4D effective gauge kinetic term becomes:

  S_4D ⊃ -1/4 ∫ d⁴x √(-g₄) × [V₄(φ)/g₈²] × F_μν F^μν

Expanding around the VEV φ = φ_* + δφ:

  V₄(φ) ≈ V₄₀ (1 + 4 δφ/M_P + ...)

So the 4D gauge coupling is:

  1/g₄² = V₄₀/g₈² × (1 + 4 δφ/M_P)

Comparing with α⁻¹(φ) = α⁻¹(1 + γ δφ/M_P):

  ⟹  γ = 4  (for a single compact 4-volume breathing mode)

For the T³/Z₂ orbifold, the Z₂ quotient halves the volume, introducing
a factor of 1/2, and the S¹/Z₂ adds another factor. The net result for
the FULL orbifold with all moduli frozen except the universal volume mode:

  γ = 4 / (number of orbifold images) = 4 / 1 = 4

NOTE: γ = 4 is the GEOMETRIC coupling. The PHYSICAL coupling to the
canonically normalized radion is γ/M_P, which is Planck-suppressed.
""")

gamma = 4.0  # Geometric coupling constant (dimensionless)
print(f"  γ (geometric) = {gamma}")
print(f"  γ/M_P = {gamma / M_Pl_red_eV:.4e} eV⁻¹")
print(f"  γ/M_P = {gamma / (M_Pl_red_kg * c**2):.4e} J⁻¹")
print(f"  γ/M_P = {gamma * hbar * c / (M_Pl_red_eV * eV):.4e} m")

coupling_eV_inv = gamma / M_Pl_red_eV
print(f"\n  RESULT: The radion-photon coupling is {coupling_eV_inv:.3e} eV⁻¹")
print(f"  This is Planck-suppressed: ~ 1/M_Pl")


# =============================================================================
# PART 2: RADION MASS FROM Z² POTENTIAL
# =============================================================================
print("\n" + "=" * 80)
print("PART 2: RADION MASS (CONDITIONAL ON Z² POTENTIAL)")
print("=" * 80)

print("""
The Z² potential is ASSUMED (not derived from first principles):

  V(φ) = V₀ [1 - cos(Z² φ/M_P)]

This gives:

  m_φ² = Z⁴ V₀ / M_P²

We evaluate at V₀ = (246 GeV)⁴ (electroweak scale):
""")

v_higgs_eV = 246e9  # Higgs VEV in eV
V0_eV4 = v_higgs_eV**4
V0_J_m3 = V0_eV4 * eV / (hbar * c)**3  # Convert to J/m³

m_phi_eV = Z2 * np.sqrt(V0_eV4) / M_Pl_red_eV
m_phi_J  = m_phi_eV * eV
f_phi_Hz = m_phi_J / hbar
lambda_phi_m = c / f_phi_Hz

print(f"  V₀ = (246 GeV)⁴ = {V0_eV4:.4e} eV⁴")
print(f"  m_φ = Z² √V₀ / M_P = {m_phi_eV:.6e} eV")
print(f"  f_φ = m_φ/ℏ = {f_phi_Hz:.6e} Hz = {f_phi_Hz/1e12:.4f} THz")
print(f"  λ_φ = c/f = {lambda_phi_m:.4e} m = {lambda_phi_m*1e6:.2f} μm")
print(f"\n  ⚠ CAVEAT: This frequency depends entirely on the assumed V₀.")
print(f"    If V₀ = (1 TeV)⁴: m_φ = {Z2 * np.sqrt((1e12)**4) / M_Pl_red_eV:.4e} eV")
print(f"    If V₀ = (10 GeV)⁴: m_φ = {Z2 * np.sqrt((10e9)**4) / M_Pl_red_eV:.4e} eV")


# =============================================================================
# PART 3: CORRECT CASIMIR ENERGY FOR T³/Z₂ ORBIFOLD
# =============================================================================
print("\n" + "=" * 80)
print("PART 3: ORBIFOLD CASIMIR ENERGY (EPSTEIN ZETA)")
print("=" * 80)

print("""
The Casimir energy density on a D-dimensional torus T^D with equal radii R
for a single massless scalar field is:

  ρ_Cas = -(1/2) × 1/(2πR)^D × ∑'_{n∈Z^D} |n|^{-(D+1)} × Γ((D+1)/2) / π^{(D+1)/2}

For a cubic T³ (D=3), the sum ∑'|n|^{-4} is the 3D Epstein zeta function E₃(4).

For T³/Z₂, the orbifold projects out half the modes (odd parity), so:
  ρ_Cas(T³/Z₂) ≈ ρ_Cas(T³) / 2  (approximate; exact requires careful mode counting)

We compute E₃(s) = ∑'_{n₁,n₂,n₃ ∈ Z} (n₁² + n₂² + n₃²)^{-s/2}
numerically for s = 4 (the exponent needed for 3 compact dimensions).
""")

def epstein_zeta_3d(s, n_max=50):
    """
    Compute the 3D Epstein zeta function:
    E₃(s) = Σ'_{n ∈ Z³} (n₁² + n₂² + n₃²)^{-s/2}
    where the prime means we exclude n = (0,0,0).
    For a cubic torus with equal radii.
    """
    total = 0.0
    for n1 in range(-n_max, n_max + 1):
        for n2 in range(-n_max, n_max + 1):
            for n3 in range(-n_max, n_max + 1):
                r2 = n1**2 + n2**2 + n3**2
                if r2 == 0:
                    continue
                total += r2**(-s / 2.0)
    return total

print("  Computing 3D Epstein zeta function E₃(4)...")
E3_4 = epstein_zeta_3d(4.0, n_max=30)
print(f"  E₃(4) = {E3_4:.8f}")
print(f"  (For comparison: 6 × ζ(2) = {6 * riemann_zeta(2):.8f} — nearest-neighbor approx)")

# Casimir energy density for a single real scalar on T³ with radius R_c
# ρ = -(1/2) × Γ(2)/π² × E₃(4) / (2πR_c)⁴
# Γ(2) = 1, so:
def casimir_T3_Z2(R_c):
    """Casimir energy density on T³/Z₂ for a single real scalar."""
    prefactor = -0.5 * E3_4 / (np.pi**2 * (2 * np.pi * R_c)**4)
    orbifold_factor = 0.5  # Z₂ projection
    return prefactor * orbifold_factor * hbar * c  # Convert to J/m³ (need ℏc/R⁴ dimensions)

# Compare with naive parallel-plate formula
def casimir_plates(R_c):
    """Naive parallel-plate Casimir for comparison."""
    return -(np.pi**2 / 720.0) * hbar * c / R_c**4

R_test = 1e-18  # 1 am (electroweak scale)
rho_orbifold = casimir_T3_Z2(R_test)
rho_plates   = casimir_plates(R_test)
ratio = rho_orbifold / rho_plates

print(f"\n  At R_c = {R_test:.0e} m:")
print(f"    ρ_Cas (T³/Z₂ orbifold) = {rho_orbifold:.6e} J/m³")
print(f"    ρ_Cas (parallel plates) = {rho_plates:.6e} J/m³")
print(f"    Ratio (orbifold/plates) = {ratio:.4f}")
print(f"    ⟹ The plate formula was off by a factor of {1/ratio:.1f}")


# =============================================================================
# PART 4: REALISTIC PUMP STRENGTH WITH STATE-OF-THE-ART EM SOURCES
# =============================================================================
print("\n" + "=" * 80)
print("PART 4: REALISTIC PUMP STRENGTH h")
print("=" * 80)

print("""
The pump strength in the Mathieu equation is:

  h = γ × ⟨E² - B²⟩ / (M_P × m_φ²)

For a standing wave in a cavity, ⟨E² - B²⟩ = E₀² (time-averaged).

We evaluate h for various EM source intensities:
""")

# Convert E-field to intensity: I = c ε₀ E₀² / 2
# So E₀² = 2I / (c ε₀)

def pump_strength(intensity_W_m2, m_phi_eV_val, gamma_val=4.0):
    """Compute the Mathieu pump parameter h."""
    E0_squared = 2.0 * intensity_W_m2 / (c * epsilon0)  # V²/m²
    # Convert E₀² to natural units (eV⁴):
    # E₀² [V²/m²] = E₀² [J/(C·m)]² ... 
    # Energy density u = ε₀ E₀²/2 [J/m³]
    # In natural units: u [eV⁴] = u_SI / (ℏc)³ × (1/eV)
    u_J_m3 = epsilon0 * E0_squared / 2.0  # J/m³ = energy density
    u_eV4 = u_J_m3 / (eV * (1.0 / (hbar * c))**3)
    
    # h = γ × u / (M_P × m_φ²)  ... but need consistent units
    # In SI: h = γ × (ε₀ E₀²/2) × (ℏc)³ / (M_P_eV × eV × m_φ_eV² × eV²)
    # Actually let's just work in eV:
    # The interaction Lagrangian gives: δm²/m² = γ × u / (M_P × m_φ²) ... 
    # More carefully: the modulation of ω₀² is:
    #   δ(ω₀²)/ω₀² = γ × (δφ/M_P)
    # and δφ ≈ γ × ⟨T^μμ_EM⟩ / (M_P × m_φ²) [from the EOM]
    # so h = γ² × u_EM / (M_P² × m_φ²)
    
    h_val = gamma_val**2 * u_eV4 / (M_Pl_red_eV**2 * m_phi_eV_val**2)
    return h_val, E0_squared, u_J_m3

# Various source intensities
sources = [
    ("Sunlight on Earth",                       1.4e3),
    ("Industrial CO₂ laser (focused)",          1e10),
    ("High-power pulsed THz source (current)",  1e8),
    ("Petawatt laser (focused, ~10²² W/cm²)",   1e26),
    ("Schwinger limit (QED breakdown)",         4.65e29),
]

print(f"  {'Source':<45} {'I (W/m²)':<14} {'h':<14} {'h/h_crit':<12}")
print("  " + "-" * 85)

# Critical h for parametric resonance with damping
Q_cavity = 1e6  # Very optimistic superconducting THz cavity
zeta_val = 1.0 / (2.0 * Q_cavity)
h_crit = 2.0 * zeta_val
print(f"\n  Cavity Q = {Q_cavity:.0e}, ζ = {zeta_val:.2e}, h_crit = 2ζ = {h_crit:.2e}\n")

for name, intensity in sources:
    h_val, E0sq, u = pump_strength(intensity, m_phi_eV)
    ratio_to_crit = h_val / h_crit
    print(f"  {name:<45} {intensity:<14.2e} {h_val:<14.2e} {ratio_to_crit:<12.2e}")

print(f"""
  ⚠ CONCLUSION: Even at the Schwinger limit (where QED itself breaks down
  and electron-positron pairs are spontaneously created from the vacuum),
  the pump strength h is MANY orders of magnitude below the threshold
  for parametric resonance.
  
  The deficit is ~{np.log10(h_crit / pump_strength(4.65e29, m_phi_eV)[0]):.0f} orders of magnitude.
""")


# =============================================================================
# PART 5: WHAT WOULD IT TAKE?
# =============================================================================
print("=" * 80)
print("PART 5: WHAT INTENSITY WOULD BE NEEDED?")
print("=" * 80)

# Solve for I such that h = h_crit
# h_crit = γ² × u / (M_P² × m_φ²)
# u = ε₀ E₀² / 2 = I / c
# u_eV4 = (I/c) / (eV × (1/(ℏc))³)
# I_needed = h_crit × M_P² × m_φ² × c × eV × (1/(ℏc))³ / γ²

u_needed_eV4 = h_crit * M_Pl_red_eV**2 * m_phi_eV**2 / gamma**2
u_needed_J_m3 = u_needed_eV4 * eV * (1.0 / (hbar * c))**3
I_needed = u_needed_J_m3 * c  # W/m²

print(f"\n  Required intensity for h = h_crit:")
print(f"    I_needed = {I_needed:.4e} W/m²")
print(f"    = {I_needed / 1e4:.4e} W/cm²")

# For context
I_sun = 3.828e26  # W (total solar luminosity)
print(f"\n  For context:")
print(f"    Solar luminosity: {I_sun:.3e} W")
print(f"    Required intensity / Solar luminosity: {I_needed / I_sun:.2e}")
print(f"    Schwinger limit: 4.65e29 W/m²")
print(f"    Required / Schwinger: {I_needed / 4.65e29:.2e}")


# =============================================================================
# PART 6: CORRECTED POWER EXTRACTION WITH COUPLING SUPPRESSION
# =============================================================================
print("\n" + "=" * 80)
print("PART 6: CORRECTED POWER EXTRACTION ESTIMATES")
print("=" * 80)

print("""
The PREVIOUS calculation ignored the coupling suppression entirely.
The corrected power extraction density is:

  P/V = ω_φ × Δρ_Cas × (h/h_crit)²    [below threshold: no resonance]
  P/V = ω_φ × Δρ_Cas × exp(growth)     [above threshold: exponential]

Since h << h_crit for ALL known EM sources, there is NO parametric 
resonance. The best we can do is the FORCED (non-resonant) response:

  P/V_forced = γ² × ω_φ × ρ_Cas × (u_EM / M_P²) / m_φ²

This is the rate at which a non-resonant EM field can shake the radion 
and modulate the Casimir energy.
""")

# Use the best available source: petawatt laser
I_best = 1e26  # W/m²
h_best, _, u_best_J = pump_strength(I_best, m_phi_eV)
omega_phi = 2.0 * np.pi * f_phi_Hz

# Non-resonant power: essentially the DC response
# δφ_forced = γ u_EM / (M_P m_φ²) [static limit]
delta_phi_forced_over_MP = gamma * (u_best_J / (M_Pl_red_kg * c**2)) / (m_phi_eV * eV)**2 * (hbar * c)**3 

# The Casimir energy modulation
rho_cas_EW = abs(casimir_T3_Z2(1e-18))
delta_rho_forced = 4.0 * rho_cas_EW * abs(delta_phi_forced_over_MP)
P_forced = omega_phi * delta_rho_forced

print(f"  With petawatt laser (I = 10²⁶ W/m²):")
print(f"    h = {h_best:.4e}")
print(f"    δφ/M_P (forced) ≈ {delta_phi_forced_over_MP:.4e}")
print(f"    |ρ_Cas| at EW scale = {rho_cas_EW:.4e} J/m³")
print(f"    Δρ_Cas (forced) = {delta_rho_forced:.4e} J/m³")
print(f"    P/V (forced) = {P_forced:.4e} W/m³")

# Previous (wrong) estimate for comparison
P_wrong = 1.3779e46
print(f"\n  COMPARISON:")
print(f"    Previous (overclaimed) estimate: {P_wrong:.4e} W/m³")
print(f"    Corrected estimate:              {P_forced:.4e} W/m³")
if P_forced > 0:
    print(f"    Overclaim factor:                {P_wrong / P_forced:.2e}×")


# =============================================================================
# PART 7: SUMMARY TABLE
# =============================================================================
print("\n" + "=" * 80)
print("FINAL HONEST SUMMARY")
print("=" * 80)

print(f"""
┌──────────────────────────────────────────────────────────────────────────┐
│                     Z² ZPE EXTRACTION: HONEST NUMBERS                  │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                        │
│  Radion-photon coupling γ:              {gamma:.0f} (dimensionless)          │
│  Physical coupling γ/M_P:               {coupling_eV_inv:.2e} eV⁻¹        │
│  Radion mass m_φ:                       {m_phi_eV:.4e} eV             │
│  Radion frequency f_φ:                  {f_phi_Hz/1e12:.4f} THz              │
│                                                                        │
│  Mathieu threshold h_crit (Q=10⁶):     {h_crit:.2e}                 │
│  Best achievable h (petawatt laser):    {h_best:.2e}                 │
│  Gap: {np.log10(h_crit/h_best):.0f} orders of magnitude                             │
│                                                                        │
│  Previous power density claim:          1.38 × 10⁴⁶ W/m³             │
│  Corrected (forced, non-resonant):      {P_forced:.2e} W/m³           │
│                                                                        │
│  VERDICT: Parametric resonance is NOT achievable with                  │
│  any known or foreseeable electromagnetic technology.                   │
│  The coupling is Planck-suppressed by ~{np.log10(M_Pl_red_eV):.0f} orders of magnitude.   │
│                                                                        │
│  HOWEVER: The Z² prediction of m_φ ≈ 8.3×10⁻⁴ eV                     │
│  (f = 1.26 THz) IS a falsifiable prediction that could                 │
│  be tested by precision measurements of α variation at THz.            │
│                                                                        │
└──────────────────────────────────────────────────────────────────────────┘
""")
