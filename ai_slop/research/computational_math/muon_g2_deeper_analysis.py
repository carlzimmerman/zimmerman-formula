"""
Deeper Analysis: Can we derive the muon g-2 anomaly from Z² principles?
======================================================================

Key finding from initial analysis:
- α × (m_μ/m_W)² / Z gives 2.18 × 10⁻⁹ vs observed 2.51 × 10⁻⁹
- Within 1σ of experimental error (0.56σ deviation)
- But the factor 1/Z needs theoretical justification

This analysis explores:
1. What correction factor would give exact match?
2. Can this factor be expressed in Z² terms?
3. What does SM electroweak physics predict?
"""

import numpy as np

print("=" * 70)
print("DEEPER ANALYSIS: MUON g-2 IN Z² FRAMEWORK")
print("=" * 70)

# Constants
Z_squared = 32 * np.pi / 3
Z = np.sqrt(Z_squared)
alpha = 1 / 137.036

m_mu = 105.6583755  # MeV
m_W = 80379         # MeV
m_Z_boson = 91187.6 # MeV

delta_a_mu_exp = 2.51e-9
delta_a_mu_err = 0.59e-9

# =============================================================================
# PART 1: EXACT FACTOR ANALYSIS
# =============================================================================

print("\n" + "=" * 70)
print("PART 1: WHAT FACTOR DO WE NEED?")
print("=" * 70)

base_term = alpha * (m_mu/m_W)**2
print(f"\nBase electroweak term: α(m_μ/m_W)² = {base_term:.6e}")

factor_needed = delta_a_mu_exp / base_term
print(f"Factor needed to match experiment: {factor_needed:.6f}")

print(f"\nCompare to various expressions involving Z:")
print(f"  1/Z = {1/Z:.6f} (ratio: {factor_needed/(1/Z):.4f})")
print(f"  1/(2π) = {1/(2*np.pi):.6f} (ratio: {factor_needed/(1/(2*np.pi)):.4f})")
print(f"  3/(4π) = {3/(4*np.pi):.6f} (ratio: {factor_needed/(3/(4*np.pi)):.4f})")
print(f"  1/Z × (Z²/32) = {Z/32:.6f}")
print(f"  3/(2πZ) = {3/(2*np.pi*Z):.6f}")

# The factor we need is ~0.199
# 1/Z = 0.173
# The ratio is ~1.15

print(f"\nThe correction factor {factor_needed/(1/Z):.4f} beyond 1/Z")
print(f"Could this be a loop correction?")

# In QED, loop corrections often have factors like:
# 1 + α/π, 1 + 3α/(4π), etc.
alpha_over_pi = alpha / np.pi
print(f"\nα/π = {alpha_over_pi:.6f}")
print(f"1 + α/π = {1 + alpha_over_pi:.6f}")
print(f"1 + 3α/(4π) = {1 + 3*alpha/(4*np.pi):.6f}")

# =============================================================================
# PART 2: STANDARD MODEL EXPECTATION
# =============================================================================

print("\n" + "=" * 70)
print("PART 2: WHAT DOES THE STANDARD MODEL PREDICT?")
print("=" * 70)

print("""
The SM electroweak contribution to muon g-2 has the form:

a_μ^EW ≈ (5/3) × (G_F m_μ²)/(8π²√2) × [1 + (1-4sin²θ_W)² + ...]

Or equivalently using α and m_W:

a_μ^W ≈ (10/3) × (α/4π) × (m_μ/m_W)² × [1 + corrections]

The full SM prediction for the total EW contribution is:
a_μ^EW ≈ 153.6 × 10⁻¹¹ = 1.536 × 10⁻⁹

But the ANOMALY (experiment - SM) ≈ 251 × 10⁻¹¹ = 2.51 × 10⁻⁹
represents NEW PHYSICS beyond SM.
""")

# Let's see if Z² framework gives the NEW PHYSICS part
print("Checking if Z² gives the BSM contribution:")

# The leading W-loop contribution
a_W_approx = (10/3) * (alpha/(4*np.pi)) * (m_mu/m_W)**2
print(f"\nSM W-loop estimate: (10/3)(α/4π)(m_μ/m_W)² = {a_W_approx:.4e}")

# What if Z² gives an ADDITIONAL contribution?
z2_contribution = alpha * (m_mu/m_W)**2 / Z
print(f"Z² contribution: α(m_μ/m_W)²/Z = {z2_contribution:.4e}")
print(f"This is {z2_contribution/a_W_approx:.2f}× the SM W-loop term")

# =============================================================================
# PART 3: REFINING THE Z² FORMULA
# =============================================================================

print("\n" + "=" * 70)
print("PART 3: REFINING THE Z² FORMULA")
print("=" * 70)

# The discrepancy between 1/Z and the needed factor is ~15%
# Can we express this more precisely in Z² terms?

# Try: 1/Z × (1 + something small)
ratio_to_Z = factor_needed * Z
print(f"\nRatio: (factor needed) × Z = {ratio_to_Z:.6f}")
print(f"This is the correction beyond 1/Z")

# Interesting: 1.152 ≈ 1 + 3/(2Z) ?
correction_guess1 = 1 + 3/(2*Z)
print(f"\n1 + 3/(2Z) = {correction_guess1:.4f}")
print(f"1 + 1/Z = {1 + 1/Z:.4f}")
print(f"1 + π/Z² = {1 + np.pi/Z_squared:.4f}")

# What if the correct factor is (1+ε)/Z where ε is a Z-dependent correction?
# We need factor = 0.199
# If factor = (1 + ε)/Z = (1 + ε)/5.789
# Then 1 + ε = 0.199 × 5.789 = 1.152
# So ε = 0.152

epsilon = factor_needed * Z - 1
print(f"\nIf factor = (1+ε)/Z, then ε = {epsilon:.4f}")

# Can we express ε in Z² terms?
print(f"\nTrying to express ε = {epsilon:.4f} in Z² terms:")
print(f"  1/Z = {1/Z:.4f}")
print(f"  1/Z² = {1/Z_squared:.6f}")
print(f"  Z/Z² = 1/Z = {1/Z:.4f}")
print(f"  π/Z² = {np.pi/Z_squared:.4f}")
print(f"  3/Z² = {3/Z_squared:.4f}")
print(f"  (Z-5)/Z = {(Z-5)/Z:.4f}")

# The value 0.152 is close to 1/Z (0.173) but not exact
# Also close to (Z-5.5)/Z ≈ 0.05

# =============================================================================
# PART 4: ALTERNATIVE INTERPRETATION
# =============================================================================

print("\n" + "=" * 70)
print("PART 4: COULD Z APPEAR DIFFERENTLY?")
print("=" * 70)

# What if Z appears in the numerator instead?
# Or what if Z² appears as a coefficient?

# Try: coefficient × α × (m_μ/m_W)²
# where coefficient involves Z² more naturally

# If BSM physics adds a sector with Z² degrees of freedom:
# contribution = (g²/16π²) × (m_μ/M_BSM)² × N_states
# where N_states could be related to Z²

# If N_states = 1/Z² ≈ 0.03, this is too small
# If N_states = 1/Z ≈ 0.17, this is close to 0.199

print("If new physics has Z² structure in loop integrals:")
print(f"  1/Z factor suggests ~{1/Z:.2f} effective coupling modifier")
print(f"  Could arise from averaging over Z² internal states")
print()

# Alternatively, what if Z modifies the mass scale?
# a_BSM = α × (m_μ / (m_W × Z^n))²
print("If Z modifies the effective mass scale:")
for n in [0.1, 0.2, 0.25, 0.3, 0.5]:
    m_eff = m_W * Z**n
    a_test = alpha * (m_mu/m_eff)**2
    print(f"  n = {n:.2f}: m_eff = {m_eff:.0f} MeV, a = {a_test:.3e}, ratio = {a_test/delta_a_mu_exp:.3f}")

# =============================================================================
# PART 5: THE MOST NATURAL FORMULA
# =============================================================================

print("\n" + "=" * 70)
print("PART 5: SEARCHING FOR THE MOST NATURAL FORMULA")
print("=" * 70)

# The formula α(m_μ/m_W)²/Z works to 13%
# Can we find a more natural form?

# Try formulas with manifest Z² structure
candidates = [
    ("α(m_μ/m_W)²/Z", alpha * (m_mu/m_W)**2 / Z),
    ("α(m_μ/m_W)²/(2π)", alpha * (m_mu/m_W)**2 / (2*np.pi)),
    ("(α/2π)(m_μ/m_W)²", (alpha/(2*np.pi)) * (m_mu/m_W)**2),
    ("α(m_μ/m_W)²×√(3/Z²)", alpha * (m_mu/m_W)**2 * np.sqrt(3/Z_squared)),
    ("α(m_μ/m_W)²×(3/Z²)^(1/4)", alpha * (m_mu/m_W)**2 * (3/Z_squared)**0.25),
    ("(α/Z)(m_μ/m_W)²×(1+1/Z)", (alpha/Z) * (m_mu/m_W)**2 * (1 + 1/Z)),
    ("α(m_μ/m_W)²/(Z-0.8)", alpha * (m_mu/m_W)**2 / (Z - 0.8)),
    ("α(m_μ/m_W)²×(Z/Z²)×1.15", alpha * (m_mu/m_W)**2 * (Z/Z_squared) * 1.15),
    ("α(m_μ/m_W)²/(√(2π×Z))", alpha * (m_mu/m_W)**2 / np.sqrt(2*np.pi*Z)),
]

print(f"{'Formula':<40} {'Value':>12} {'Ratio':>8}")
print("-" * 65)

for name, val in sorted(candidates, key=lambda x: abs(x[1]/delta_a_mu_exp - 1)):
    print(f"{name:<40} {val:>12.4e} {val/delta_a_mu_exp:>8.4f}")

# =============================================================================
# PART 6: DIMENSIONAL ANALYSIS
# =============================================================================

print("\n" + "=" * 70)
print("PART 6: DIMENSIONAL ANALYSIS")
print("=" * 70)

print("""
For a_μ (dimensionless anomalous magnetic moment):

Any formula must combine:
- α (dimensionless)
- Mass ratios (dimensionless)
- Pure numbers like Z, π (dimensionless)

The simplest electroweak structure is:
  a ~ α × (m_μ/M_heavy)²

where M_heavy could be:
  - m_W ≈ 80 GeV (W boson)
  - m_Z ≈ 91 GeV (Z boson)
  - Some effective scale involving Z² structure

The factor 1/Z ~ 0.17 could represent:
  - Loop suppression factor (like 1/4π ≈ 0.08 or 1/2π ≈ 0.16)
  - Coupling constant in new sector
  - Statistical factor from internal states
""")

# Compare 1/Z to typical loop factors
print("Comparison of Z to loop factors:")
print(f"  Z = {Z:.4f}")
print(f"  2π = {2*np.pi:.4f} (ratio Z/(2π) = {Z/(2*np.pi):.4f})")
print(f"  4π = {4*np.pi:.4f}")
print(f"  √(8π) = {np.sqrt(8*np.pi):.4f}")
print(f"  √(32π/3) = Z = {Z:.4f}")

# Note: Z ≈ 0.92 × 2π
print(f"\nZ/2π = {Z/(2*np.pi):.4f} ≈ 0.92")
print(f"So Z ≈ 2π × 0.92 = 2π × √(8/9) where √(8/9) = {np.sqrt(8/9):.4f}")

# Actually compute Z/2π precisely
ratio_z_2pi = Z / (2*np.pi)
print(f"\nMore precisely: Z/2π = √(32π/3)/(2π) = √(8/(3π)) = {np.sqrt(8/(3*np.pi)):.6f}")
print(f"Check: {ratio_z_2pi:.6f}")

# =============================================================================
# PART 7: THE VERDICT
# =============================================================================

print("\n" + "=" * 70)
print("PART 7: FINAL VERDICT")
print("=" * 70)

# Calculate the prediction with your formula
pred = alpha * (m_mu/m_W)**2 / Z

print(f"""
YOUR FORMULA: Δa_μ = α × (m_μ/m_W)² / Z

RESULT:
  Predicted: {pred:.4e}
  Observed:  {delta_a_mu_exp:.4e} ± {delta_a_mu_err:.4e}

  Ratio: {pred/delta_a_mu_exp:.4f} ({(pred/delta_a_mu_exp-1)*100:.1f}% off)
  Sigma deviation: {abs(pred-delta_a_mu_exp)/delta_a_mu_err:.2f}σ

ASSESSMENT:

✓ CORRECT ORDER OF MAGNITUDE (10⁻⁹)
✓ WITHIN 1σ EXPERIMENTAL ERROR
✓ PHYSICALLY MOTIVATED STRUCTURE (electroweak loop × geometric factor)
✓ USES ESTABLISHED Z² FRAMEWORK

⚠ CONCERNS:
- Why 1/Z and not 1/Z² or 1/2π?
- 1/2π gives nearly identical result, so not uniquely Z²
- The 1/Z factor needs derivation from first principles

NUMEROLOGY SCORE: 6/10
- Better than random coincidence
- But shares success with 1/2π (which has standard interpretation)
- Would need Lagrangian derivation to be convincing

PHYSICAL PICTURE (if true):
The muon g-2 anomaly arises from BSM physics where:
1. The electromagnetic coupling α enters at the vertex
2. The electroweak scale suppression (m_μ/m_W)² comes from W-like loops
3. The Z² geometric structure contributes a 1/Z phase space factor

The key prediction: If this is correct, similar structures should appear
in other precision observables (electron g-2, W mass, etc.)
""")

# =============================================================================
# PART 8: COMPARISON WITH 2π
# =============================================================================

print("\n" + "=" * 70)
print("PART 8: IS Z DISTINGUISHABLE FROM 2π?")
print("=" * 70)

pred_Z = alpha * (m_mu/m_W)**2 / Z
pred_2pi = alpha * (m_mu/m_W)**2 / (2*np.pi)

print(f"\nFormula with 1/Z: {pred_Z:.6e}")
print(f"Formula with 1/2π: {pred_2pi:.6e}")
print(f"Difference: {abs(pred_Z - pred_2pi):.4e}")
print(f"Relative difference: {abs(pred_Z - pred_2pi)/delta_a_mu_exp * 100:.2f}%")

print(f"\nBoth are within 1σ of experiment!")
print(f"Experimental precision needed to distinguish: {abs(pred_Z - pred_2pi)/delta_a_mu_exp * 100:.1f}%")
print(f"Current precision: {delta_a_mu_err/delta_a_mu_exp * 100:.1f}%")

if abs(pred_Z - pred_2pi) < delta_a_mu_err:
    print("\n⚠ IMPORTANT: Current experimental precision cannot distinguish 1/Z from 1/2π!")
    print("   Both are equally valid explanations statistically.")
else:
    print("\n✓ Experiment can potentially distinguish between Z and 2π factors.")

# What precision would be needed?
precision_needed = abs(pred_Z - pred_2pi) / delta_a_mu_exp
print(f"\nTo distinguish Z from 2π at 3σ, need precision: {precision_needed/3 * 100:.2f}%")
print(f"This requires error: ±{delta_a_mu_exp * precision_needed/3 * 1e11:.0f} × 10⁻¹¹")
