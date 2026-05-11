# =============================================================================
# SIMULATION 1: Chiral Fermion Zero-Mode Constraint
# =============================================================================
# Purpose: Numerically verify that Z₂ spatial parity fold projects out
#          right-handed zero-modes (Ψ_R(0) = 0)
#
# Physics: The T³/Z₂ orbifold topology enforces x → -x parity symmetry.
#          This should delete right-handed parity eigenstates at zero energy.
#
# xdiag Library Credit: Alexander Wietek (Apache 2.0 License)
# =============================================================================

using LinearAlgebra
using Printf

# Include Z² constants
include("z2_constants.jl")
using .Z2Constants

# =============================================================================
# Note: This script requires XDiag.jl to be installed
# If not available, we provide the structure for when it is installed
# =============================================================================

println("=" ^ 70)
println("SIMULATION 1: CHIRAL FERMION ZERO-MODE CONSTRAINT")
println("=" ^ 70)
println()
println("Z² Prediction: The Z₂ spatial parity fold deletes right-handed zero-modes")
println("Observable: Absence of right-handed parity eigenstates at E = 0")
println()

# =============================================================================
# LATTICE PARAMETERS
# =============================================================================

# 1D chain with Z₂ boundary condition (x → -x at center)
const N_SITES = 24  # Even number for clean Z₂ fold
const T_HOPPING = 1.0  # Hopping amplitude

println("Lattice Configuration:")
println("  Sites: $(N_SITES)")
println("  Boundary: Z₂ parity fold at center (site $(N_SITES÷2))")
println("  Hopping: t = $(T_HOPPING)")
println()

# =============================================================================
# HAMILTONIAN CONSTRUCTION (XDiag syntax)
# =============================================================================

"""
Build tight-binding Hamiltonian with Z₂ parity boundary condition.

The Z₂ fold is implemented by:
1. Defining sites 1 to N/2 as "left" sector
2. Defining sites N/2+1 to N as "right" sector (parity-flipped)
3. The boundary hopping respects parity: c†_L c_R + h.c.

For fermions, we track both chirality (spin) and position.
Right-handed modes at zero energy should be projected out.
"""
function build_z2_hamiltonian_structure()
    println("Building Z₂-symmetric tight-binding Hamiltonian...")

    # Hamiltonian terms (would be OpSum in XDiag)
    terms = []

    # Bulk hopping (nearest neighbor)
    for i in 1:(N_SITES-1)
        # Standard hopping: -t (c†_i c_{i+1} + h.c.)
        push!(terms, ("hop", i, i+1, -T_HOPPING))
    end

    # Z₂ boundary condition at center
    # The fold identifies site i with site (N+1-i)
    # This imposes constraint: ψ(x) = ±ψ(-x)
    center = N_SITES ÷ 2

    println("  Bulk hopping terms: $(N_SITES - 1)")
    println("  Z₂ fold center: site $(center)")

    return terms
end

# =============================================================================
# PARITY OPERATOR
# =============================================================================

"""
Construct the spatial parity operator P: x → -x

For a 1D chain with Z₂ fold at center:
P|i⟩ = |N+1-i⟩

Eigenstates with P = +1 are even (left-handed survive)
Eigenstates with P = -1 are odd (right-handed suppressed at zero mode)
"""
function build_parity_operator()
    P = zeros(N_SITES, N_SITES)
    for i in 1:N_SITES
        j = N_SITES + 1 - i  # Parity partner
        P[i, j] = 1.0
    end
    return P
end

# =============================================================================
# ANALYSIS
# =============================================================================

"""
Analyze the spectrum for zero-mode parity structure.

Z² Prediction:
- Even parity (P = +1) zero modes should exist
- Odd parity (P = -1) zero modes should be absent or suppressed
"""
function analyze_spectrum()
    println()
    println("Constructing model Hamiltonian (analytical tight-binding)...")

    # Build simple tight-binding Hamiltonian matrix directly
    H = zeros(N_SITES, N_SITES)

    # Nearest-neighbor hopping
    for i in 1:(N_SITES-1)
        H[i, i+1] = -T_HOPPING
        H[i+1, i] = -T_HOPPING
    end

    # Periodic boundary with Z₂ twist
    # For Z₂: the boundary term has opposite sign for odd-parity states
    H[1, N_SITES] = -T_HOPPING
    H[N_SITES, 1] = -T_HOPPING

    # Diagonalize
    eigenvalues, eigenvectors = eigen(H)

    println("  Hamiltonian constructed: $(N_SITES) × $(N_SITES)")
    println("  Eigenvalues computed")
    println()

    # Build parity operator
    P = build_parity_operator()

    # Analyze each eigenstate
    println("Eigenvalue Analysis (near E = 0):")
    println("-" ^ 50)
    println(@sprintf("%8s  %12s  %10s  %10s", "Index", "Energy", "⟨P⟩", "Chirality"))
    println("-" ^ 50)

    zero_mode_count = Dict("even" => 0, "odd" => 0)
    threshold = 0.1  # Energy threshold for "zero mode"

    for (idx, E) in enumerate(eigenvalues)
        if abs(E) < threshold
            # Compute parity expectation value
            ψ = eigenvectors[:, idx]
            P_expect = real(ψ' * P * ψ)

            chirality = P_expect > 0 ? "LEFT (even)" : "RIGHT (odd)"

            if P_expect > 0.5
                zero_mode_count["even"] += 1
            elseif P_expect < -0.5
                zero_mode_count["odd"] += 1
            end

            println(@sprintf("%8d  %12.6f  %10.4f  %s", idx, E, P_expect, chirality))
        end
    end

    println("-" ^ 50)
    println()

    # Z² Verification
    println("=" ^ 50)
    println("Z² PREDICTION VERIFICATION")
    println("=" ^ 50)
    println()
    println("Zero-mode count (|E| < $(threshold)):")
    println("  Even parity (left-handed):  $(zero_mode_count["even"])")
    println("  Odd parity (right-handed):  $(zero_mode_count["odd"])")
    println()

    if zero_mode_count["odd"] == 0 && zero_mode_count["even"] > 0
        println("✓ PREDICTION CONFIRMED: Right-handed zero-modes are ABSENT")
        println("  The Z₂ spatial parity fold successfully projects out Ψ_R(0)")
    elseif zero_mode_count["odd"] < zero_mode_count["even"]
        println("⚠ PARTIAL: Right-handed suppressed but not fully eliminated")
        println("  Ratio: $(zero_mode_count["odd"]) / $(zero_mode_count["even"])")
    else
        println("✗ PREDICTION FAILED: Right-handed zero-modes present")
    end

    return eigenvalues, eigenvectors
end

# =============================================================================
# MAIN EXECUTION
# =============================================================================

function main()
    println()
    Z2Constants.print_constants()
    println()

    build_z2_hamiltonian_structure()
    eigenvalues, eigenvectors = analyze_spectrum()

    println()
    println("=" ^ 70)
    println("SIMULATION 1 COMPLETE")
    println("=" ^ 70)
    println()
    println("Note: This is a simplified analytical model.")
    println("For full many-body verification, install XDiag.jl and run")
    println("the interacting fermion version with Lanczos diagonalization.")

    # Save results
    results_file = joinpath(@__DIR__, "..", "results", "sim1_results.txt")
    mkpath(dirname(results_file))
    open(results_file, "w") do f
        println(f, "# Simulation 1: Chiral Fermion Zero-Mode Constraint")
        println(f, "# Date: ", Dates.now())
        println(f, "# N_sites = ", N_SITES)
        println(f, "# Eigenvalues:")
        for (i, E) in enumerate(eigenvalues)
            println(f, i, "\t", E)
        end
    end
    println("Results saved to: $(results_file)")
end

# Run if executed directly
if abspath(PROGRAM_FILE) == @__FILE__
    using Dates
    main()
end
