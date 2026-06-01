"""
Muon g-2 Anomaly Analysis in the Z² Framework
=============================================

Target: Δa_μ = (251 ± 59) × 10⁻¹¹ = 2.51 × 10⁻⁹
This is the experimental - SM theory discrepancy

Goal: Find if Z² framework provides a principled derivation
"""

import numpy as np
from typing import Tuple, List

# =============================================================================
# CONSTANTS
# =============================================================================

# Z² Framework
Z_squared = 32 * np.pi / 3
Z = np.sqrt(Z_squared)
alpha = 1 / 137.036  # Fine structure constant
alpha_inv = 137.036

print("=" * 70)
print("Z² FRAMEWORK CONSTANTS")
print("=" * 70)
print(f"Z² = 32π/3 = {Z_squared:.6f}")
print(f"Z = √(32π/3) = {Z:.6f}")
print(f"α = 1/137.036 = {alpha:.6e}")
print(f"α⁻¹ = 4Z² + 3 = 4×{Z_squared:.4f} + 3 = {4*Z_squared + 3:.4f}")
print()

# Physical Constants (in MeV)
m_mu = 105.6583755  # Muon mass
m_e = 0.51099895    # Electron mass
m_tau = 1776.86     # Tau mass
m_W = 80379         # W boson mass
m_Z = 91187.6       # Z boson mass
m_H = 125100        # Higgs mass

print("PARTICLE MASSES (MeV)")
print("-" * 40)
print(f"m_e = {m_e:.6f} MeV")
print(f"m_μ = {m_mu:.4f} MeV")
print(f"m_τ = {m_tau:.2f} MeV")
print(f"m_W = {m_W} MeV")
print(f"m_Z = {m_Z:.1f} MeV")
print()

# Target anomaly
delta_a_mu_exp = 2.51e-9
delta_a_mu_err = 0.59e-9

print("TARGET: MUON g-2 ANOMALY")
print("-" * 40)
print(f"Δa_μ = ({delta_a_mu_exp*1e11:.0f} ± {delta_a_mu_err*1e11:.0f}) × 10⁻¹¹")
print(f"     = {delta_a_mu_exp:.2e}")
print()

# =============================================================================
# YOUR PROPOSED FORMULA
# =============================================================================

print("=" * 70)
print("YOUR PROPOSED FORMULA: α × (m_μ/m_W)² / Z")
print("=" * 70)

mass_ratio_W = m_mu / m_W
mass_ratio_W_sq = mass_ratio_W**2

formula_1 = alpha * mass_ratio_W_sq / Z

print(f"\nStep-by-step calculation:")
print(f"  1. α = 1/137.036 = {alpha:.6e}")
print(f"  2. m_μ/m_W = {m_mu}/{m_W} = {mass_ratio_W:.6e}")
print(f"  3. (m_μ/m_W)² = {mass_ratio_W_sq:.6e}")
print(f"  4. Z = {Z:.6f}")
print(f"\n  Result: α × (m_μ/m_W)² / Z = {formula_1:.4e}")
print(f"\n  Target: Δa_μ = {delta_a_mu_exp:.4e}")
print(f"  Ratio (predicted/observed) = {formula_1/delta_a_mu_exp:.4f}")
print(f"  Discrepancy: {abs(formula_1 - delta_a_mu_exp)/delta_a_mu_exp * 100:.1f}%")

# =============================================================================
# SYSTEMATIC EXPLORATION OF FORMULAS
# =============================================================================

print("\n" + "=" * 70)
print("SYSTEMATIC FORMULA EXPLORATION")
print("=" * 70)

results = []

def evaluate_formula(name: str, value: float, description: str = ""):
    """Evaluate a formula against the target anomaly."""
    ratio = value / delta_a_mu_exp
    sigma_off = abs(value - delta_a_mu_exp) / delta_a_mu_err
    results.append((name, value, ratio, sigma_off, description))
    return value

# Category 1: Your original and variants
print("\n--- Category 1: Electroweak Loop Structure ---")

evaluate_formula(
    "α(m_μ/m_W)²/Z",
    alpha * (m_mu/m_W)**2 / Z,
    "Your original proposal"
)

evaluate_formula(
    "α(m_μ/m_W)²/Z²",
    alpha * (m_mu/m_W)**2 / Z_squared,
    "Divided by Z² instead of Z"
)

evaluate_formula(
    "α(m_μ/m_W)²×Z",
    alpha * (m_mu/m_W)**2 * Z,
    "Multiplied by Z"
)

evaluate_formula(
    "α²(m_μ/m_W)²/Z",
    alpha**2 * (m_mu/m_W)**2 / Z,
    "Alpha squared"
)

# Category 2: Using Z boson mass instead
print("\n--- Category 2: Using Z Boson Mass ---")

evaluate_formula(
    "α(m_μ/m_Z)²/Z",
    alpha * (m_mu/m_Z)**2 / Z,
    "Z boson mass"
)

evaluate_formula(
    "α(m_μ/m_Z)²×Z²",
    alpha * (m_mu/m_Z)**2 * Z_squared,
    "Z boson with Z² multiplier"
)

# Category 3: Higher order alpha terms
print("\n--- Category 3: Higher Order α Terms ---")

evaluate_formula(
    "α³/(2πZ²)",
    alpha**3 / (2 * np.pi * Z_squared),
    "Your suggested alternative"
)

evaluate_formula(
    "α³/(πZ)",
    alpha**3 / (np.pi * Z),
    "Alpha cubed variant"
)

evaluate_formula(
    "α⁴×Z²",
    alpha**4 * Z_squared,
    "Fourth order with Z²"
)

evaluate_formula(
    "α³/Z",
    alpha**3 / Z,
    "Simple alpha cubed over Z"
)

evaluate_formula(
    "α²/(2πZ)",
    alpha**2 / (2 * np.pi * Z),
    "Alpha squared over 2πZ"
)

# Category 4: Mass ratio combinations
print("\n--- Category 4: Mass Ratio Combinations ---")

evaluate_formula(
    "α(m_μ/m_τ)²/Z",
    alpha * (m_mu/m_tau)**2 / Z,
    "Tau mass ratio"
)

evaluate_formula(
    "α(m_e/m_μ)²×Z",
    alpha * (m_e/m_mu)**2 * Z,
    "Electron-muon ratio"
)

evaluate_formula(
    "α(m_μ²/(m_W×m_Z))/Z",
    alpha * m_mu**2 / (m_W * m_Z) / Z,
    "W-Z geometric mean"
)

# Category 5: Pure Z² geometric structures
print("\n--- Category 5: Pure Z² Geometric Structures ---")

evaluate_formula(
    "α²/Z³",
    alpha**2 / Z**3,
    "Alpha squared over Z cubed"
)

evaluate_formula(
    "α²/(Z²√Z)",
    alpha**2 / (Z_squared * np.sqrt(Z)),
    "Fractional Z power"
)

evaluate_formula(
    "1/(α×Z⁵)",
    1 / (alpha * Z**5),
    "Inverse structure"
)

# Category 6: Mixed structures with π factors
print("\n--- Category 6: Including π Factors ---")

evaluate_formula(
    "α(m_μ/m_W)²/(2π)",
    alpha * (m_mu/m_W)**2 / (2 * np.pi),
    "Loop factor 1/2π"
)

evaluate_formula(
    "α(m_μ/m_W)²×(Z/π)",
    alpha * (m_mu/m_W)**2 * Z / np.pi,
    "Z/π structure"
)

evaluate_formula(
    "α²(m_μ/m_W)×Z²/(4π)",
    alpha**2 * (m_mu/m_W) * Z_squared / (4 * np.pi),
    "Linear mass ratio"
)

# Category 7: Trying to match exactly
print("\n--- Category 7: Engineering Matches ---")

# What coefficient would we need?
coeff_needed = delta_a_mu_exp / (alpha * (m_mu/m_W)**2)
print(f"\nTo match with α(m_μ/m_W)² × C, we need C = {coeff_needed:.4f}")
print(f"Compare: 1/Z = {1/Z:.4f}, 1/Z² = {1/Z_squared:.6f}, Z = {Z:.4f}")
print(f"         π = {np.pi:.4f}, 2π = {2*np.pi:.4f}")

# What if coefficient is 1/2 or 1/4?
evaluate_formula(
    "α(m_μ/m_W)²/2",
    alpha * (m_mu/m_W)**2 / 2,
    "Simple 1/2 factor"
)

evaluate_formula(
    "α(m_μ/m_W)²/(2Z)",
    alpha * (m_mu/m_W)**2 / (2*Z),
    "Factor of 1/(2Z)"
)

# Category 8: Schwinger-like with Z² modification
print("\n--- Category 8: Schwinger Structure Modified ---")

a_mu_schwinger = alpha / (2 * np.pi)  # Leading QED term

evaluate_formula(
    "(α/2π)(m_μ/m_W)²",
    a_mu_schwinger * (m_mu/m_W)**2,
    "Schwinger × mass ratio squared"
)

evaluate_formula(
    "(α/2π)(m_μ/m_W)²×Z",
    a_mu_schwinger * (m_mu/m_W)**2 * Z,
    "With Z enhancement"
)

evaluate_formula(
    "(α/2π)²×(m_μ/m_e)×/Z²",
    (alpha/(2*np.pi))**2 * (m_mu/m_e) / Z_squared,
    "Higher order with electron ratio"
)

# =============================================================================
# RESULTS SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("RESULTS RANKED BY AGREEMENT WITH EXPERIMENT")
print("=" * 70)

# Sort by how close to 1.0 the ratio is
results.sort(key=lambda x: abs(x[2] - 1.0))

print(f"\n{'Formula':<30} {'Value':>12} {'Ratio':>8} {'σ off':>8} Description")
print("-" * 90)

for name, value, ratio, sigma, desc in results[:20]:
    match_quality = "***" if 0.8 < ratio < 1.2 else "**" if 0.5 < ratio < 2.0 else "*" if 0.1 < ratio < 10 else ""
    print(f"{name:<30} {value:>12.3e} {ratio:>8.3f} {sigma:>8.2f} {desc} {match_quality}")

print("\n" + "=" * 70)
print("DETAILED ANALYSIS OF BEST CANDIDATES")
print("=" * 70)

# Get top 5 candidates
top_candidates = results[:5]

for i, (name, value, ratio, sigma, desc) in enumerate(top_candidates, 1):
    print(f"\n#{i}: {name}")
    print(f"    Description: {desc}")
    print(f"    Predicted: {value:.4e}")
    print(f"    Observed:  {delta_a_mu_exp:.4e} ± {delta_a_mu_err:.4e}")
    print(f"    Ratio (pred/obs): {ratio:.4f}")
    print(f"    Within {sigma:.2f}σ of experimental value")

    # Check if within experimental error
    if abs(value - delta_a_mu_exp) < delta_a_mu_err:
        print(f"    ✓ WITHIN 1σ EXPERIMENTAL ERROR")
    elif abs(value - delta_a_mu_exp) < 2 * delta_a_mu_err:
        print(f"    ✓ Within 2σ experimental error")

# =============================================================================
# THEORETICAL INTERPRETATION
# =============================================================================

print("\n" + "=" * 70)
print("THEORETICAL INTERPRETATION")
print("=" * 70)

print("""
PHYSICAL MEANING OF FORMULA COMPONENTS:

1. α (fine structure constant):
   - Measures electromagnetic coupling strength
   - Each factor of α corresponds to a loop in Feynman diagrams
   - α/2π is the Schwinger term (leading QED correction)

2. (m_μ/m_W)² ≈ 1.73 × 10⁻⁶:
   - Electroweak loop suppression factor
   - Appears in W-loop contributions to (g-2)
   - Reflects that muon is much lighter than weak scale

3. Z = √(32π/3) ≈ 5.79:
   - Z² framework geometric factor
   - If appearing, suggests new geometric structure
   - The key question: does Z appear naturally or ad hoc?
""")

# =============================================================================
# THE KEY TEST: IS IT PRINCIPLED OR NUMEROLOGY?
# =============================================================================

print("\n" + "=" * 70)
print("NUMEROLOGY VS FIRST PRINCIPLES TEST")
print("=" * 70)

print("""
CRITERIA FOR FIRST-PRINCIPLES DERIVATION:

1. UNIQUENESS: Does the formula have a single natural form?
   - If many similar formulas work equally well, likely numerology
   - If one specific combination stands out, potentially meaningful

2. DERIVABILITY: Can we derive it from Lagrangian/action principles?
   - Would need to show Z² emerges from symmetry considerations
   - Must explain WHY Z appears with specific power

3. PREDICTIVITY: Does it predict other quantities correctly?
   - Same framework should give electron (g-2), tau (g-2)
   - Should relate to other anomalies consistently

4. THEORETICAL MOTIVATION:
   - What physical process introduces the Z factor?
   - Is Z² a loop correction factor? A phase space factor?
""")

# Test: Does the same formula work for electron g-2?
print("\n--- Cross-Check: Electron g-2 ---")
delta_a_e_exp = 4.8e-13  # Approximate electron g-2 anomaly (much smaller, controversial)

for name, value, ratio, sigma, desc in top_candidates[:3]:
    if "m_μ" in name or "μ" in name:
        # Replace muon mass with electron mass
        name_e = name.replace("m_μ", "m_e").replace("μ", "e")
        # Crude scaling
        if "(m_μ/m_W)²" in name or "(m_e/m_W)²" in name:
            value_e = value * (m_e/m_mu)**2
            print(f"\n{name} scaled to electron:")
            print(f"  Predicted: {value_e:.3e}")
            print(f"  Observed Δa_e ≈ {delta_a_e_exp:.3e}")
            print(f"  Ratio: {value_e/delta_a_e_exp:.2f}")

# =============================================================================
# SEARCHING FOR THE "GOLDEN" FORMULA
# =============================================================================

print("\n" + "=" * 70)
print("SEARCHING FOR ELEGANT Z² FORMULA")
print("=" * 70)

# What would make a formula elegant?
# 1. Uses only Z, π, α, and mass ratios
# 2. Simple integer or half-integer powers
# 3. Natural interpretation in terms of loops/geometry

# Try systematic combinations
print("\nSystematic search: α^a × (m_μ/m_W)^b × Z^c × π^d")
print("-" * 60)

best_match = None
best_ratio_diff = float('inf')

for a in [1, 2, 3]:
    for b in [1, 2]:
        for c in [-3, -2, -1, 0, 1, 2, 3]:
            for d in [-2, -1, 0, 1, 2]:
                val = (alpha**a) * ((m_mu/m_W)**b) * (Z**c) * (np.pi**d)
                if val > 0:
                    ratio_diff = abs(val/delta_a_mu_exp - 1)
                    if ratio_diff < 0.3:  # Within 30%
                        if ratio_diff < best_ratio_diff:
                            best_ratio_diff = ratio_diff
                            best_match = (a, b, c, d, val)
                        print(f"α^{a} × (m_μ/m_W)^{b} × Z^{c} × π^{d} = {val:.3e} (ratio: {val/delta_a_mu_exp:.3f})")

if best_match:
    a, b, c, d, val = best_match
    print(f"\nBest match: α^{a} × (m_μ/m_W)^{b} × Z^{c} × π^{d}")
    print(f"Value: {val:.4e}")
    print(f"Ratio to observed: {val/delta_a_mu_exp:.4f}")

# =============================================================================
# FINAL ASSESSMENT
# =============================================================================

print("\n" + "=" * 70)
print("FINAL ASSESSMENT")
print("=" * 70)

# Find best formula from all results
best = results[0]
print(f"\nBest formula found: {best[0]}")
print(f"Predicted: {best[1]:.4e}")
print(f"Observed:  {delta_a_mu_exp:.4e}")
print(f"Agreement: {best[2]*100:.1f}% (ratio = {best[2]:.4f})")

assessment = """
VERDICT:
========

Your original formula: α × (m_μ/m_W)² / Z

Result: {:.3e} vs observed {:.3e}
Ratio: {:.3f} (off by {:.1f}%)

This is in the RIGHT ORDER OF MAGNITUDE, which is non-trivial because:
- The anomaly is ~10⁻⁹
- Random combinations often give wrong orders of magnitude
- The electroweak structure (m_μ/m_W)² is physically motivated

PHYSICAL INTERPRETATION:
The formula suggests the anomaly arises from:
1. An electromagnetic vertex (factor of α)
2. Electroweak loop suppression (m_μ/m_W)²
3. A geometric factor from Z² structure (1/Z)

CONCERNS:
1. The factor of 1/Z seems arbitrary - why not 1/Z², or Z, or 1/2π?
2. We haven't derived this from a Lagrangian
3. Multiple similar formulas work approximately as well

POSSIBLE PATH FORWARD:
- If Z² represents a geometric modification to loop integrals,
  this could emerge from the regularization/renormalization scheme
- The factor of ~5-6 could be related to number of degrees of freedom
  or internal symmetry dimensions

STATUS: Suggestive but not yet a derivation. The order of magnitude
match with physical motivation (electroweak loops) makes this worth
pursuing, but the specific Z factor needs theoretical justification.
""".format(results[0][1] if "α(m_μ/m_W)²/Z" in results[0][0] else formula_1,
           delta_a_mu_exp,
           formula_1/delta_a_mu_exp,
           abs(formula_1/delta_a_mu_exp - 1)*100)

print(assessment)

# =============================================================================
# BONUS: What would derive Z naturally?
# =============================================================================

print("\n" + "=" * 70)
print("BONUS: DERIVING Z FROM LOOP STRUCTURE")
print("=" * 70)

print("""
If Z = √(32π/3) appears in g-2, possible origins:

1. MODIFIED PROPAGATOR:
   If the photon propagator is modified by Z² geometry:
   D(q²) → D(q²) × f(Z²/q²)
   This would introduce Z into loop integrals

2. VERTEX CORRECTION:
   If the γμμ vertex includes Z² phase space:
   Γ → Γ × (Z²)^n for some power n

3. LOOP MEASURE MODIFICATION:
   ∫d⁴k → ∫d⁴k × g(Z)
   where g(Z) is a geometric factor

4. NUMBER OF INTERNAL STATES:
   Z² ≈ 33.5 is close to number of SM fermions (45) or
   gauge degrees of freedom (12 for SU(3)×SU(2)×U(1))

The cleanest derivation would show Z emerging from
integration over some internal manifold with Z² volume.
""")

# Calculate what loop factor would give exact match
exact_factor = delta_a_mu_exp / (alpha * (m_mu/m_W)**2)
print(f"\nTo match exactly, need: α(m_μ/m_W)² × {exact_factor:.4f}")
print(f"Compare to: 1/Z = {1/Z:.4f}")
print(f"           1/(2π) = {1/(2*np.pi):.4f}")
print(f"           Z/Z² = 1/Z = {1/Z:.4f}")
print(f"           √(3/32) = {np.sqrt(3/32):.4f}")

# What is the exact factor in terms of Z?
print(f"\nExact factor ÷ (1/Z) = {exact_factor * Z:.4f}")
print(f"This means: Δa_μ ≈ α(m_μ/m_W)² × {exact_factor:.4f}")
print(f"          ≈ α(m_μ/m_W)² / {1/exact_factor:.4f}")
print(f"If 1/Z works perfectly, factor would be {1/Z:.4f}")
print(f"Actual factor needed: {exact_factor:.4f}")
print(f"Discrepancy: {exact_factor/(1/Z):.4f} = factor of ~{exact_factor*Z:.2f}")
