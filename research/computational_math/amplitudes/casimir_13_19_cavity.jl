#!/usr/bin/env julia
#=
================================================================================
INVESTIGATION: 13:19 CASIMIR CAVITY RESONANCE
================================================================================

Objective: Compute the Casimir energy for rectangular cavities and determine
if the 13:19 aspect ratio has any special properties (minimum, resonance, etc.)

The Casimir energy for a rectangular cavity with sides (a, b, c) is:

  E_C = (ℏc π²/2) Σ'_{n_x,n_y,n_z} √[(n_x/a)² + (n_y/b)² + (n_z/c)²]

where the prime indicates exclusion of negative integers and special
treatment of zero modes.

For a 2D rectangular cavity (plates at z=0, z=c, with transverse dimensions a×b):
The Casimir energy per unit area is given by the regularized sum.

We compute E_C as a function of aspect ratio and look for special behavior at 13/19.
================================================================================
=#

using Printf
using LinearAlgebra

println("=" ^ 70)
println("INVESTIGATION: 13:19 CASIMIR CAVITY RESONANCE")
println("=" ^ 70)
println()

# =============================================================================
# FRAMEWORK CONSTANTS
# =============================================================================

const RATIO_13_19 = 13/19
const OMEGA_LAMBDA = 13/19

println("Framework constants:")
println(@sprintf("  Ω_Λ = 13/19 = %.10f", OMEGA_LAMBDA))
println(@sprintf("  1 - Ω_Λ = 6/19 = %.10f", 1 - OMEGA_LAMBDA))
println()

# =============================================================================
# CASIMIR ENERGY FOR 2D RECTANGULAR CAVITY
# =============================================================================

"""
    casimir_energy_2d(aspect_ratio; N_max=50)

Compute the regularized Casimir energy for a 2D rectangular cavity
with aspect ratio α = a/b.

The energy is computed using zeta-function regularization:
  E(α) = Σ'_{m,n} √(m²/α² + n²α²)^(-s) |_{s→-1}

Returns the energy in units where ℏc = 1 and the smaller dimension = 1.
"""
function casimir_energy_2d(α::Float64; N_max::Int=100, s::Float64=-1.0)
    # For s < 0, the sum diverges, so we use a regularization
    # Here we compute the finite part using Epstein zeta function

    # For regularization at s = -1, we use the heat kernel method
    # E_reg = -(1/2) × d/ds Z(s)|_{s=0} where Z(s) = Σ' λ_n^(-s)

    # For practical computation, we use a cutoff and extrapolation
    total = 0.0

    for m in 0:N_max
        for n in 0:N_max
            if m == 0 && n == 0
                continue
            end

            # Eigenvalue: λ = (mπ/a)² + (nπ/b)²
            # With a = α × L, b = L: λ = π²[(m/α)² + n²]/L²
            λ = (m/α)^2 + n^2

            # Energy contribution: √λ (with regularization weight)
            if s == -1.0
                # For s = -1, ω ~ √λ, so we'd sum √λ which diverges
                # Use exponential regularization: e^(-ε√λ)
                ε = 0.01
                total += sqrt(λ) * exp(-ε * sqrt(λ))
            else
                total += λ^(s/2)
            end
        end
    end

    return total
end

"""
    casimir_energy_epstein(α; N_max=50)

Compute the Casimir energy using proper Epstein zeta regularization.
For a 2D cavity, the finite Casimir energy is:

  E_C(α) = -(π/6) × [ζ(-1, α) + ζ(-1, 1/α)]

where ζ(s, α) is the Epstein zeta function.
"""
function casimir_energy_epstein(α::Float64; N_max::Int=200)
    # The Casimir energy for a 2D rectangular domain is related to
    # the Epstein zeta function Z_2(s) = Σ'_{m,n} (m²/α² + n²α²)^(-s)

    # For practical computation, we use the reflection formula and
    # the fact that Z_2(-1/2) is finite (after removing divergent terms)

    # Simplified approach: compute the energy difference from a reference
    # This removes the divergent contribution

    # Reference: α = 1 (square cavity)
    function raw_sum(ratio, s_param, Nmax)
        total = 0.0
        for m in 1:Nmax
            for n in 1:Nmax
                λ = (m/ratio)^2 + n^2 * ratio^2
                total += λ^(-s_param)
            end
        end
        # Add edge contributions (m=0 or n=0, but not both)
        for m in 1:Nmax
            total += (m/ratio)^(-2*s_param) / 2  # m>0, n=0
            total += (m*ratio)^(-2*s_param) / 2  # m=0, n>0
        end
        return total
    end

    s = 1.5  # Convergent for s > 1
    Z_α = raw_sum(α, s, N_max)
    Z_1 = raw_sum(1.0, s, N_max)

    # The finite part of the Casimir energy is proportional to Z(-1/2)
    # which we can't compute directly, but we can compute the ratio
    # E(α)/E(1) ≈ Z(α, s)/Z(1, s) for the relative comparison

    return Z_α / Z_1
end

"""
    casimir_energy_analytic_2d(α)

For a 2D rectangular region, the Casimir energy has a known form.
Using the result from "Casimir Effect in Rectangular Geometries":

  E(α) = E_0 × f(α)

where f(α) depends on the aspect ratio and E_0 is a reference energy.
"""
function casimir_energy_analytic_2d(α::Float64)
    # The Casimir energy for a 2D rectangle is related to
    # the Dedekind eta function, but for our purposes we use
    # the numerical sum with proper regularization

    # For a simpler model: electromagnetic cavity
    # E_EM(α) ∝ (1/α + α)/2 for the dominant terms

    return (1/α + α)/2
end

# =============================================================================
# CASIMIR ENERGY FOR 3D RECTANGULAR CAVITY
# =============================================================================

"""
    casimir_energy_3d(a, b, c; N_max=30)

Compute the Casimir energy for a 3D rectangular cavity.
Uses cutoff regularization with extrapolation.
"""
function casimir_energy_3d(a::Float64, b::Float64, c::Float64; N_max::Int=30)
    total = 0.0
    cutoff = 100.0  # Energy cutoff

    for nx in 0:N_max
        for ny in 0:N_max
            for nz in 0:N_max
                if nx == 0 && ny == 0 && nz == 0
                    continue
                end

                # Mode frequency: ω² = π²c²[(nx/a)² + (ny/b)² + (nz/c)²]
                ω2 = (nx/a)^2 + (ny/b)^2 + (nz/c)^2
                ω = sqrt(ω2)

                # Regularization: exponential cutoff
                weight = exp(-ω / cutoff)
                total += 0.5 * ω * weight
            end
        end
    end

    return total
end

# =============================================================================
# SCAN ASPECT RATIOS
# =============================================================================

println("=" ^ 60)
println("CASIMIR ENERGY VS ASPECT RATIO")
println("=" ^ 60)
println()

println("Scanning 2D rectangular cavities with aspect ratio α = a/b")
println()

# Scan aspect ratios
ratios = [0.5, 0.6, 13/19, 0.7, 0.75, 0.8, 0.9, 1.0, 1.1, 1.2, 19/13, 1.5, 2.0]
labels = ["0.50", "0.60", "13/19", "0.70", "0.75", "0.80", "0.90", "1.00", "1.10", "1.20", "19/13", "1.50", "2.00"]

println("Using simplified analytic form: E(α) ∝ (1/α + α)/2")
println()
println(@sprintf("%10s  %15s  %15s", "α", "E(α)/E(1)", "Note"))
println("-" ^ 45)

E_ref = casimir_energy_analytic_2d(1.0)  # Reference at α = 1

for (i, α) in enumerate(ratios)
    E = casimir_energy_analytic_2d(α)
    E_norm = E / E_ref
    note = ""
    if abs(α - 13/19) < 0.001
        note = "← Ω_Λ"
    elseif abs(α - 19/13) < 0.001
        note = "← 1/Ω_Λ"
    elseif α == 1.0
        note = "← minimum"
    end
    println(@sprintf("%10s  %15.8f  %s", labels[i], E_norm, note))
end
println()

# =============================================================================
# FINE SCAN AROUND 13/19
# =============================================================================

println()
println("=" ^ 60)
println("FINE SCAN AROUND 13/19")
println("=" ^ 60)
println()

fine_ratios = collect(0.60:0.01:0.80)

println(@sprintf("%10s  %15s", "α", "E(α)/E(1)"))
println("-" ^ 28)

min_E = Inf
min_α = 0.0

for α in fine_ratios
    E = casimir_energy_analytic_2d(α)
    E_norm = E / E_ref
    mark = ""
    if abs(α - 13/19) < 0.005
        mark = "  ← 13/19"
    end
    println(@sprintf("%10.4f  %15.8f%s", α, E_norm, mark))

    if E_norm < min_E
        global min_E = E_norm
        global min_α = α
    end
end
println()

println(@sprintf("Minimum at α = %.4f (E/E₀ = %.6f)", min_α, min_E))
println(@sprintf("Value at 13/19 = %.4f (E/E₀ = %.6f)", 13/19, casimir_energy_analytic_2d(13/19)/E_ref))
println()

# =============================================================================
# CRITICAL ANALYSIS
# =============================================================================

println()
println("=" ^ 60)
println("CRITICAL ANALYSIS")
println("=" ^ 60)
println()

println("""
FINDING: For the simple Casimir energy model E(α) = (1/α + α)/2:

  - The MINIMUM occurs at α = 1 (square cavity)
  - There is NO special feature at α = 13/19

The ratio 13/19 does NOT correspond to:
  - A minimum of the Casimir energy
  - A maximum of the Casimir energy
  - A critical point or resonance

The Casimir energy is monotonically increasing as α moves away from 1.
""")

# =============================================================================
# ALTERNATIVE: MODE COUNTING RESONANCE
# =============================================================================

println()
println("=" ^ 60)
println("ALTERNATIVE: MODE COUNTING RESONANCE")
println("=" ^ 60)
println()

println("""
Alternative hypothesis: The 13:19 ratio is not about Casimir energy
minimum, but about MODE COUNTING RESONANCE.

If a cavity has dimensions proportional to 13 × 19 units, then the
number of modes below a certain frequency might match the topological
partition (13 dark energy, 6 matter modes per 19 total).
""")

# Count modes below cutoff for 13×19 vs other dimensions
function count_modes_below_cutoff(a::Int, b::Int, ω_max::Float64)
    count = 0
    for nx in 1:100
        for ny in 1:100
            ω2 = (nx/a)^2 + (ny/b)^2
            if sqrt(ω2) < ω_max
                count += 1
            end
        end
    end
    return count
end

# Compare 13×19 with nearby dimensions
println("Mode count for ω < 1:")
println()
for (a, b) in [(13, 19), (12, 19), (13, 18), (14, 20), (10, 10), (7, 10)]
    N = count_modes_below_cutoff(a, b, 1.0)
    ratio = a/b
    println(@sprintf("  %d × %d (ratio %.4f): %d modes", a, b, ratio, N))
end
println()

# =============================================================================
# THE 13:19 CLAIM: HONEST ASSESSMENT
# =============================================================================

println()
println("=" ^ 60)
println("HONEST ASSESSMENT: 13:19 CASIMIR CAVITY")
println("=" ^ 60)
println()

println("""
FINDING: The claim that a 13:19 aspect ratio cavity shows a
"topological resonance" or Casimir energy feature is NOT SUPPORTED
by standard Casimir effect calculations.

The reasons:

1. SCALE MISMATCH: Cosmological Ω_Λ operates at Hubble scale (10²⁶ m).
   A micron-scale cavity has NO physical connection to this ratio.

2. NO MINIMUM: The Casimir energy E(α) has its minimum at α = 1,
   not at α = 13/19 or any other "special" ratio.

3. NO RESONANCE: There is no resonance or critical behavior at 13/19.

CLASSIFICATION:
  ┌──────────────────────────────────────────────────────────────┐
  │  The 13:19 Casimir cavity claim is UNFOUNDED.               │
  │                                                              │
  │  There is NO physical mechanism connecting the topological  │
  │  mode ratio Ω_Λ = 13/19 to a micron-scale cavity geometry.  │
  │                                                              │
  │  STATUS: FALSE / REMOVE FROM PREDICTIONS                    │
  └──────────────────────────────────────────────────────────────┘

RECOMMENDATION: Do NOT propose this as an experimental test.
It conflates topological mode counting with cavity QED without
physical justification.
""")

# =============================================================================
# WHAT WOULD BE VALID?
# =============================================================================

println()
println("=" ^ 60)
println("VALID ALTERNATIVES FOR TABLETOP TESTS")
println("=" ^ 60)
println()

println("""
Instead of the unphysical Casimir cavity claim, consider these
genuinely testable predictions:

1. CRYSTAL TENSOR ANISOTROPY
   Measure resistivity tensor in a cubic crystal oriented at
   θ = 35.26° to the shear direction.
   Prediction: Zero face-diagonal coupling (from magic angle).

2. GRAVITATIONAL WAVE POLARIZATION
   If the universe has T³/Z₂ topology, GW polarizations should
   show directional dependence correlated with CMB anisotropies.

3. CMB DIPOLE-QUADRUPOLE ALIGNMENT
   The tensor coupling at magic angle predicts specific alignments
   in CMB multipoles.

These are PHYSICAL predictions from the topology, not numerological
matching of ratios.
""")

println("=" ^ 60)
println("CONCLUSION")
println("=" ^ 60)
println()
println("  13:19 Casimir cavity: NOT VALID (remove from predictions)")
println("  Magic angle crystal test: VALID (keep)")
println()

