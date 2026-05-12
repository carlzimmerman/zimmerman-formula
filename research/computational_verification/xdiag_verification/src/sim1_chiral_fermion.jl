# =============================================================================
# SIMULATION 1: Chiral Fermion Zero-Mode Constraint
# =============================================================================
# Target: Apple M4, 64 GB
# Purpose: Verify Z₂ spatial parity fold projects out right-handed zero-modes
# Prediction: Ψ_R(0) = 0
# xdiag Credit: Alexander Wietek (Apache 2.0)
# =============================================================================

using LinearAlgebra
using Printf
using Dates

include("z2_constants.jl")
using .Z2Constants

println("=" ^ 70)
println("SIMULATION 1: CHIRAL FERMION ZERO-MODE CONSTRAINT")
println("=" ^ 70)
println("Start: ", now())
println()

# Lattice: 1D chain with Z₂ parity boundary
const N = 24  # Sites (even for clean Z₂ fold)
const t = 1.0  # Hopping

println("Lattice: $(N)-site 1D chain with Z₂ boundary")
println()

# Build tight-binding Hamiltonian
function build_hamiltonian()
    H = zeros(N, N)
    for i in 1:(N-1)
        H[i, i+1] = -t
        H[i+1, i] = -t
    end
    # Periodic boundary
    H[1, N] = -t
    H[N, 1] = -t
    return H
end

# Parity operator P: site i → site (N+1-i)
function build_parity()
    P = zeros(N, N)
    for i in 1:N
        P[i, N+1-i] = 1.0
    end
    return P
end

# Main computation
function main()
    println("Building Hamiltonian...")
    H = build_hamiltonian()
    P = build_parity()

    println("Diagonalizing...")
    t_start = time()
    E, V = eigen(H)
    t_elapsed = time() - t_start
    println("  Completed in $(round(t_elapsed, digits=2)) sec")
    println()

    # Analyze parity of each eigenstate
    println("Eigenvalue Analysis (near E = 0):")
    println("-" ^ 50)

    threshold = 0.1
    n_even = 0
    n_odd = 0

    for (idx, e) in enumerate(E)
        if abs(e) < threshold
            ψ = V[:, idx]
            P_expect = real(ψ' * P * ψ)
            chirality = P_expect > 0 ? "LEFT (even)" : "RIGHT (odd)"

            if P_expect > 0.5
                n_even += 1
            elseif P_expect < -0.5
                n_odd += 1
            end

            println(@sprintf("E = %8.4f  ⟨P⟩ = %6.3f  %s", e, P_expect, chirality))
        end
    end

    println("-" ^ 50)
    println()

    # Z² Verification
    println("=" ^ 50)
    println("Z² PREDICTION VERIFICATION")
    println("=" ^ 50)
    println()
    println("Zero-modes (|E| < $(threshold)):")
    println("  Even parity (left-handed):  $(n_even)")
    println("  Odd parity (right-handed):  $(n_odd)")
    println()

    if n_odd == 0 && n_even > 0
        println("✓ CONFIRMED: Right-handed zero-modes ABSENT")
        println("  The Z₂ fold successfully projects out Ψ_R(0)")
        status = "CONFIRMED"
    elseif n_odd < n_even
        println("⚠ PARTIAL: Right-handed suppressed")
        status = "PARTIAL"
    else
        println("✗ NOT CONFIRMED")
        status = "FAILED"
    end

    println()
    println("End: ", now())
    println("Status: ", status)

    return status
end

status = main()
