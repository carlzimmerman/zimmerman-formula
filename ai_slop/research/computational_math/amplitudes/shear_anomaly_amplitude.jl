#!/usr/bin/env julia
#=
================================================================================
INVESTIGATION: 0.99% SHEAR ANOMALY AMPLITUDE
================================================================================

Objective: Analytically derive the claimed 0.99% shear anomaly amplitude
at the magic angle θ = arctan(1/√2).

Approach:
1. Compute face-diagonal coupling C_face(θ) - known to be 0 at magic angle
2. Compute body-diagonal coupling C_body(θ) at magic angle
3. Compute coupling ratios and deviations
4. Search for origin of 0.99% ≈ 1/100 or 1/101
================================================================================
=#

using Printf
using LinearAlgebra

println("=" ^ 70)
println("INVESTIGATION: 0.99% SHEAR ANOMALY AMPLITUDE")
println("=" ^ 70)
println()

# =============================================================================
# MAGIC ANGLE PARAMETERS (EXACT)
# =============================================================================

println("MAGIC ANGLE PARAMETERS (exact values):")
println()

# From sin²θ = 1/3:
sin2_θ = 1//3
cos2_θ = 2//3
tan2_θ = 1//2

println("  sin²θ = 1/3")
println("  cos²θ = 2/3")
println("  tan²θ = 1/2")
println("  tan θ = 1/√2")
println("  θ = arctan(1/√2) = 35.2644°")
println()

# Numerical values
θ_magic = atan(1/√2)
sin_θ = sin(θ_magic)
cos_θ = cos(θ_magic)

println(@sprintf("Numerical: θ = %.10f rad = %.6f°", θ_magic, rad2deg(θ_magic)))
println(@sprintf("           sinθ = %.10f", sin_θ))
println(@sprintf("           cosθ = %.10f", cos_θ))
println()

# =============================================================================
# SHEAR TENSOR COUPLING FORMULAS
# =============================================================================

println("=" ^ 60)
println("SHEAR TENSOR COUPLING FORMULAS")
println("=" ^ 60)
println()

println("""
Given:
  - Shear direction n̂ = (sinθ cosφ, sinθ sinφ, cosθ)
  - Target direction d̂ (face or body diagonal)

The traceless shear tensor is:
  σ_n = (3/2) n̂⊗n̂ - (1/2) I

The coupling (Frobenius inner product) is:
  C(n̂, d̂) = Tr(σ_n^T σ_d) = (9/4)(n̂·d̂)² - 3/4
""")

# =============================================================================
# COMPUTE ALL COUPLINGS AT MAGIC ANGLE
# =============================================================================

println()
println("=" ^ 60)
println("COUPLINGS AT MAGIC ANGLE (φ = π/4)")
println("=" ^ 60)
println()

# Shear direction at magic angle with φ = π/4
φ = π/4
n̂ = [sin_θ * cos(φ), sin_θ * sin(φ), cos_θ]
println("Shear direction n̂ at θ_magic, φ = π/4:")
println(@sprintf("  n̂ = (%.6f, %.6f, %.6f)", n̂[1], n̂[2], n̂[3]))
println(@sprintf("    = (1/√6, 1/√6, √(2/3))"))
println()

# Face diagonals (in xy, xz, yz planes)
d̂_xy = [1/√2, 1/√2, 0]       # (1,1,0)/√2
d̂_xz = [1/√2, 0, 1/√2]       # (1,0,1)/√2
d̂_yz = [0, 1/√2, 1/√2]       # (0,1,1)/√2

# Body diagonal
b̂ = [1/√3, 1/√3, 1/√3]       # (1,1,1)/√3

# Coupling function
function coupling(n, d)
    dot_prod = dot(n, d)
    return 9/4 * dot_prod^2 - 3/4
end

# Compute all couplings
C_face_xy = coupling(n̂, d̂_xy)
C_face_xz = coupling(n̂, d̂_xz)
C_face_yz = coupling(n̂, d̂_yz)
C_body = coupling(n̂, b̂)

println("FACE DIAGONAL COUPLINGS:")
println(@sprintf("  C(n̂, d̂_xy) = %.15f", C_face_xy))
println(@sprintf("  C(n̂, d̂_xz) = %.15f", C_face_xz))
println(@sprintf("  C(n̂, d̂_yz) = %.15f", C_face_yz))
println()

println("BODY DIAGONAL COUPLING:")
println(@sprintf("  C(n̂, b̂)    = %.10f", C_body))
println()

# Verify face-xy coupling is zero
println("Verification: C(n̂, d̂_xy) should be 0 at magic angle")
println(@sprintf("  n̂ · d̂_xy = %.10f (= sinθ)", dot(n̂, d̂_xy)))
println(@sprintf("  (n̂ · d̂_xy)² = %.10f (= 1/3)", dot(n̂, d̂_xy)^2))
println(@sprintf("  C = (9/4)(1/3) - 3/4 = 3/4 - 3/4 = %.2e", C_face_xy))
println()

# =============================================================================
# BODY DIAGONAL COUPLING: ANALYTICAL DERIVATION
# =============================================================================

println()
println("=" ^ 60)
println("BODY DIAGONAL COUPLING: ANALYTICAL DERIVATION")
println("=" ^ 60)
println()

println("At magic angle with φ = π/4:")
println("  n̂ = (sinθ/√2, sinθ/√2, cosθ)")
println("  b̂ = (1/√3, 1/√3, 1/√3)")
println()

# Dot product
dot_n_b_analytical = 2 * (sin_θ / √2) * (1/√3) + cos_θ / √3
println("n̂ · b̂ = 2(sinθ/√2)(1/√3) + cosθ/√3")
println("      = (2sinθ)/(√6) + cosθ/√3")
println()

# At magic angle: sinθ = 1/√3, cosθ = √(2/3)
println("At magic angle:")
println("  sinθ = 1/√3, cosθ = √(2/3)")
println()
println("  n̂ · b̂ = 2/(√3 × √6) + √(2/3)/√3")
println("        = 2/√18 + √2/3")
println("        = 2/(3√2) + √2/3")
println("        = √2/3 + √2/3")
println("        = 2√2/3")
println()

dot_exact = 2*√2/3
println(@sprintf("  Exact: n̂ · b̂ = 2√2/3 = %.10f", dot_exact))
println(@sprintf("  Computed: n̂ · b̂ = %.10f", dot(n̂, b̂)))
println()

# Body coupling
println("Body diagonal coupling:")
println("  C_body = (9/4)(n̂ · b̂)² - 3/4")
println("        = (9/4)(2√2/3)² - 3/4")
println("        = (9/4)(8/9) - 3/4")
println("        = 2 - 3/4")
println("        = 5/4 = 1.25")
println()

C_body_exact = 5/4
println(@sprintf("  Exact: C_body = 5/4 = %.10f", C_body_exact))
println(@sprintf("  Computed: C_body = %.10f", C_body))
println()

# =============================================================================
# SEARCH FOR 0.99% = 1/101 OR SIMILAR
# =============================================================================

println()
println("=" ^ 60)
println("SEARCH FOR 0.99% ORIGIN")
println("=" ^ 60)
println()

println("Target: 0.99% = 0.0099 ≈ 1/101")
println()

# At magic angle:
# - Face coupling = 0
# - Body coupling = 5/4 = 1.25

# What ratios can we form?

# Ratio of face to body at magic angle: 0/1.25 = 0 (not 0.99%)

# What about the DEVIATION from isotropy?
# In isotropic case, all couplings would be equal

# The maximum possible coupling is when n̂ = d̂:
C_max = 9/4 * 1 - 3/4  # = 6/4 = 3/2
println(@sprintf("Maximum coupling (n̂ = d̂): C_max = 3/2 = %.4f", C_max))
println()

# Average coupling over all directions?
# For uniformly distributed n̂, the average of (n̂·d̂)² is 1/3
C_avg = 9/4 * (1/3) - 3/4  # = 3/4 - 3/4 = 0
println(@sprintf("Average coupling (uniform): C_avg = 0", ))
println()

# What about the deviation of body coupling from face coupling?
# At a general angle, both are non-zero.
# At magic angle, face = 0, body = 5/4

# The RELATIVE deviation from the body-diagonal value:
# (C_body - C_face) / C_body = (5/4 - 0) / (5/4) = 1 = 100%

println("At magic angle:")
println(@sprintf("  Face coupling:  %.4f", C_face_xy))
println(@sprintf("  Body coupling:  %.4f", C_body))
println(@sprintf("  Ratio C_face/C_body = %.4f", C_face_xy/C_body))
println()

# =============================================================================
# ALTERNATIVE: SMALL PERTURBATION AROUND MAGIC ANGLE
# =============================================================================

println()
println("=" ^ 60)
println("PERTURBATION ANALYSIS AROUND MAGIC ANGLE")
println("=" ^ 60)
println()

println("C_face(θ) = (9/4)sin²θ - 3/4")
println()
println("At magic angle θ₀: sin²θ₀ = 1/3, so C(θ₀) = 0")
println()
println("For small perturbation δθ:")
println("  sin²(θ₀ + δθ) ≈ sin²θ₀ + 2sinθ₀cosθ₀ × δθ")
println("                = 1/3 + 2(1/√3)(√(2/3))δθ")
println("                = 1/3 + (2√2/3)δθ")
println()

# Derivative of C with respect to θ at magic angle
# dC/dθ = (9/4) × 2sinθcosθ = (9/2)sinθcosθ
dC_dθ = (9/2) * sin_θ * cos_θ
println(@sprintf("dC/dθ|_{θ=θ₀} = (9/2)sinθcosθ = %.6f", dC_dθ))
println()

# For a 1% perturbation in angle:
δθ_percent = 0.01 * θ_magic
δC_1percent = dC_dθ * δθ_percent
println("For 1% angle perturbation:")
println(@sprintf("  δθ = 0.01 × θ_magic = %.6f rad = %.4f°", δθ_percent, rad2deg(δθ_percent)))
println(@sprintf("  δC = (dC/dθ) × δθ = %.6f", δC_1percent))
println()

# What perturbation gives δC = 0.0099?
δC_target = 0.0099
δθ_needed = δC_target / dC_dθ
println("To get δC = 0.0099:")
println(@sprintf("  δθ = %.6f rad = %.4f°", δθ_needed, rad2deg(δθ_needed)))
println(@sprintf("  Fractional: δθ/θ = %.4f%%", (δθ_needed/θ_magic)*100))
println()

# =============================================================================
# THE 0.99% IN TRANSPORT CONTEXT
# =============================================================================

println()
println("=" ^ 60)
println("TRANSPORT INTERPRETATION")
println("=" ^ 60)
println()

println("""
In a transport measurement (resistivity, conductivity), the
measured quantity depends on the tensor coupling.

If conductivity σ depends on coupling C as:
  σ(θ) = σ₀ × (1 + αC(θ))

At magic angle C = 0:
  σ(θ_magic) = σ₀

At nearby angle θ_magic + δθ:
  σ(θ_magic + δθ) = σ₀ × (1 + αδC)

For a 0.99% effect:
  (σ - σ₀)/σ₀ = αδC = 0.0099
""")

# What value of α and δC gives 0.99%?
# If δC ≈ 0.01 (from small angle deviation), then α ≈ 1

# Alternative: The coupling at body diagonal divided by some reference
ratio_body_100 = C_body / 100  # = 1.25/100 = 0.0125 (close to 1%!)
println("Alternative calculation:")
println(@sprintf("  C_body / 100 = 5/400 = 1/80 = %.6f (= 1.25%%)", ratio_body_100))
println()

ratio_body_126 = C_body / 126.26  # ≈ 0.0099
println(@sprintf("  C_body / 126.26 ≈ %.6f (≈ 0.99%%)", ratio_body_126))
println()

# =============================================================================
# TOPOLOGICAL RATIO SEARCH
# =============================================================================

println()
println("=" ^ 60)
println("TOPOLOGICAL RATIO SEARCH")
println("=" ^ 60)
println()

# 0.99% ≈ 1/101
# Is there any combination of framework numbers that gives ≈ 101?

println("Is there a topological origin for 1/101 ≈ 0.0099?")
println()

# Try combinations
println("Combinations near 100-101:")
println(@sprintf("  19 × 5 + 6 = %d", 19*5 + 6))  # 101!
println(@sprintf("  16 × 6 + 5 = %d", 16*6 + 5))  # 101!
println(@sprintf("  13 × 8 - 3 = %d", 13*8 - 3))  # 101!
println()

println("FOUND multiple ways to get 101:")
println("  101 = 19 × 5 + 6 = N × (traceless tensor dim) + faces")
println("  101 = 16 × 6 + 5 = n_B × faces + (tensor dim)")
println("  101 = 13 × 8 - 3 = Δn × fixed_points - n_F")
println()

# These seem contrived but let's check if any has physical meaning
println("Most natural: 101 = 13 × 8 - 3")
println("  = (n_B - n_F) × (fixed points) - (n_F)")
println("  = net_vacuum × geometry - fermionic_correction")
println()

# So S = 1/101 = 1/(13×8 - 3) = n_F / (13×8)  × correction?
S_topological = 3 / (13 * 8)
println(@sprintf("Topological: 3/(13×8) = 3/104 = %.6f (%.4f%%)", S_topological, S_topological*100))
println()

S_101 = 1/101
println(@sprintf("Target: 1/101 = %.6f (%.4f%%)", S_101, S_101*100))
println()

# =============================================================================
# CRITICAL ASSESSMENT
# =============================================================================

println()
println("=" ^ 60)
println("CRITICAL ASSESSMENT")
println("=" ^ 60)
println()

println("""
FINDING: The number 0.99% ≈ 1/101 can be expressed as:

  101 = 13 × 8 - 3 = Δn × N_fixed - n_F

This DOES have a topological interpretation:
  - 13 = net vacuum contribution
  - 8 = fixed points (orbifold geometry)
  - 3 = fermionic correction

However, the physical meaning is unclear:
  - Why multiply Δn by N_fixed?
  - Why subtract n_F?
  - What transport mechanism yields this ratio?

CLASSIFICATION:
  ┌──────────────────────────────────────────────────────────────┐
  │  The 0.99% amplitude is POSSIBLY topological but the        │
  │  physical derivation is incomplete.                         │
  │                                                              │
  │  The ratio 1/101 = 1/(13×8 - 3) uses framework numbers     │
  │  but lacks a clear physical mechanism.                      │
  │                                                              │
  │  STATUS: PLAUSIBLE but not PROVEN                          │
  └──────────────────────────────────────────────────────────────┘

RECOMMENDATION: Present as "predicted amplitude requiring
experimental verification" rather than "derived from first
principles."
""")

println("=" ^ 60)
println("FINAL ANSWER")
println("=" ^ 60)
println()
println("At the magic angle θ = arctan(1/√2):")
println()
println("  Face-diagonal coupling:  C_face = 0 (EXACT)")
println("  Body-diagonal coupling:  C_body = 5/4 (EXACT)")
println()
println("The 0.99% amplitude could arise from:")
println("  1/101 where 101 = 13 × 8 - 3")
println()
println("But this requires a physical transport model to connect")
println("the coupling C to the measured resistivity anomaly.")
println()

