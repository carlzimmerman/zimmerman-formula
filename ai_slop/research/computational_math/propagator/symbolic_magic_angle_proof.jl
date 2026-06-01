#!/usr/bin/env julia
#=
================================================================================
SYMBOLIC PROOF: MAGIC ANGLE FACE-DIAGONAL DECOUPLING
================================================================================

This script provides a PURELY ALGEBRAIC proof that the face-diagonal coupling
vanishes exactly at θ = arctan(1/√2), using no floating-point arithmetic.

The proof:
1. Compute the coupling C(θ) = (9/4)sin²θ - 3/4 algebraically
2. Set C(θ) = 0 and solve for θ
3. Show θ = arctan(1/√2) exactly

This is NOT a numerical verification - it is a symbolic derivation.
================================================================================
=#

using Printf

println("=" ^ 70)
println("SYMBOLIC PROOF: MAGIC ANGLE FACE-DIAGONAL DECOUPLING")
println("=" ^ 70)
println()

println("""
THEOREM: The face-diagonal tensor coupling vanishes exactly at
         θ = arctan(1/√2) ≈ 35.2644°

PROOF (purely algebraic, no floating-point):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 1: Define the shear direction and face diagonal

  The shear direction at polar angle θ (with φ = π/4):
    n̂ = (sin(θ)/√2, sin(θ)/√2, cos(θ))

  The face diagonal (xy-plane):
    d̂ = (1/√2, 1/√2, 0)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 2: Compute the dot product n̂ · d̂

  n̂ · d̂ = (sin(θ)/√2)(1/√2) + (sin(θ)/√2)(1/√2) + (cos(θ))(0)
        = sin(θ)/2 + sin(θ)/2
        = sin(θ)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 3: Compute the coupling C(θ)

  The traceless shear tensors are:
    σ_n = (3/2) n̂⊗n̂ - (1/2) I
    σ_d = (3/2) d̂⊗d̂ - (1/2) I

  The Frobenius coupling is:
    C(θ) = Tr(σ_n^T σ_d)
         = Tr[(3/2 n̂⊗n̂ - 1/2 I)(3/2 d̂⊗d̂ - 1/2 I)]

  Expanding:
    C(θ) = (9/4) Tr(n̂⊗n̂ · d̂⊗d̂) - (3/4) Tr(n̂⊗n̂) - (3/4) Tr(d̂⊗d̂) + (1/4) Tr(I)

  Using Tr(â⊗â · b̂⊗b̂) = (â·b̂)² and Tr(û⊗û) = |û|² = 1:
    C(θ) = (9/4)(n̂·d̂)² - 3/4 - 3/4 + 3/4
         = (9/4)(n̂·d̂)² - 3/4

  Substituting n̂·d̂ = sin(θ):

    ┌─────────────────────────────────────┐
    │  C(θ) = (9/4) sin²(θ) - 3/4        │
    └─────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 4: Solve C(θ) = 0

  Setting C(θ) = 0:
    (9/4) sin²(θ) - 3/4 = 0
    (9/4) sin²(θ) = 3/4
    sin²(θ) = (3/4) × (4/9) = 1/3

  Therefore:
    sin(θ) = 1/√3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STEP 5: Compute tan(θ)

  From sin²(θ) = 1/3:
    cos²(θ) = 1 - 1/3 = 2/3
    cos(θ) = √(2/3)

  Therefore:
    tan(θ) = sin(θ)/cos(θ)
           = (1/√3) / (√(2/3))
           = (1/√3) × √(3/2)
           = √(1/2)
           = 1/√2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CONCLUSION:

  The face-diagonal coupling C(θ) vanishes exactly when:

    ┌─────────────────────────────────────┐
    │  θ = arctan(1/√2)                   │
    └─────────────────────────────────────┘

  This is the MAGIC ANGLE ≈ 35.2644°.

  The proof is PURELY ALGEBRAIC. No floating-point arithmetic was used.
  The result is EXACT, not an approximation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QED ∎

""")

# =============================================================================
# NUMERICAL VERIFICATION (for completeness)
# =============================================================================

println("=" ^ 70)
println("NUMERICAL VERIFICATION")
println("=" ^ 70)
println()

# Using exact rational arithmetic where possible
sin2_θ_exact = 1//3
cos2_θ_exact = 2//3

println("Exact values (rational arithmetic):")
println("  sin²(θ) = 1/3")
println("  cos²(θ) = 2/3")
println("  tan²(θ) = sin²(θ)/cos²(θ) = (1/3)/(2/3) = 1/2")
println("  tan(θ) = 1/√2")
println()

# Compute the angle
θ_magic = atan(1/√2)
θ_magic_deg = rad2deg(θ_magic)

println("Numerical evaluation:")
println(@sprintf("  θ = arctan(1/√2) = %.15f rad", θ_magic))
println(@sprintf("                   = %.10f°", θ_magic_deg))
println()

# Verify C(θ) = 0
sin2_θ = sin(θ_magic)^2
C_θ = 9/4 * sin2_θ - 3/4

println("Verification of C(θ) = 0:")
println(@sprintf("  sin²(θ) = %.15f", sin2_θ))
println(@sprintf("  Expected: 1/3 = %.15f", 1/3))
println(@sprintf("  C(θ) = (9/4)sin²θ - 3/4 = %.2e", C_θ))
println()

if abs(C_θ) < 1e-14
    println("✓ VERIFIED: C(θ) = 0 to machine precision")
else
    println("✗ ERROR: C(θ) ≠ 0")
end
println()

println("=" ^ 70)
println("SUMMARY")
println("=" ^ 70)
println()
println("The face-diagonal coupling is:")
println()
println("    C(θ) = (9/4) sin²(θ) - 3/4")
println()
println("This vanishes when sin²(θ) = 1/3, giving:")
println()
println("    θ = arctan(1/√2) = 35.2644°")
println()
println("This is an ANALYTICAL IDENTITY, not a numerical result.")
println("The magic angle is EXACTLY arctan(1/√2), proven algebraically.")
println()
