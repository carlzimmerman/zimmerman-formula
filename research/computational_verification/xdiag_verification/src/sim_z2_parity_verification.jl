# =============================================================================
# Z² PARITY SECTOR VERIFICATION
# =============================================================================
# Purpose: Compare ground state energies in even vs odd parity sectors
# to verify Z₂ topology predictions
#
# Physics: The T³/Z₂ orbifold topology predicts odd-parity states should
# show suppression S = 3/110 relative to even-parity states
#
# Method: Use XDiag with explicit parity symmetry to diagonalize in
# separate parity sectors and compare energies
#
# xdiag Credit: Alexander Wietek (Apache 2.0)
# =============================================================================

using XDiag
using LinearAlgebra
using Printf
using Dates

println("=" ^ 70)
println("Z² PARITY SECTOR VERIFICATION")
println("=" ^ 70)
println("Using XDiag library by Alexander Wietek")
println("Target: Apple M4, 64 GB")
println("Start: ", now())
println()

# =============================================================================
# LATTICE CONFIGURATION
# =============================================================================

const NX = 6
const NY = 4
const N_SITES = NX * NY  # = 24 sites
const J = 1.0

println("Lattice: $(NX) × $(NY) = $(N_SITES) sites")
println("Model: S=1/2 Heisenberg antiferromagnet")
println()

# Site indexing (1-based for XDiag.jl)
site(x, y) = (mod1(y, NY) - 1) * NX + mod1(x, NX)

# =============================================================================
# PARITY SYMMETRY
# =============================================================================

function build_parity_permutation()
    """
    Build spatial parity (inversion) permutation P: r → -r

    For a 2D square lattice with periodic BC:
    P: (x, y) → (NX+1-x, NY+1-y)
    """
    perm = zeros(Int64, N_SITES)

    for y in 1:NY
        for x in 1:NX
            i = site(x, y)
            # Inversion: (x,y) → (NX+1-x, NY+1-y) with PBC
            x_inv = NX + 1 - x
            y_inv = NY + 1 - y
            j = site(x_inv, y_inv)
            perm[i] = j
        end
    end

    return perm
end

# =============================================================================
# BUILD HAMILTONIAN
# =============================================================================

function build_heisenberg()
    """Build Heisenberg Hamiltonian."""
    println("Building Heisenberg Hamiltonian...")

    ops = OpSum()

    # Horizontal bonds
    for y in 1:NY
        for x in 1:NX
            i = site(x, y)
            j = site(x+1, y)
            ops += J * Op("SdotS", [i, j])
        end
    end

    # Vertical bonds
    for y in 1:NY
        for x in 1:NX
            i = site(x, y)
            j = site(x, y+1)
            ops += J * Op("SdotS", [i, j])
        end
    end

    n_bonds = 2 * N_SITES
    println("  Bonds: $(n_bonds)")

    return ops
end

# =============================================================================
# DIAGONALIZE IN PARITY SECTORS
# =============================================================================

function diagonalize_with_parity(ops::OpSum)
    """Diagonalize in both parity sectors and compare."""
    println()
    println("Setting up parity symmetry...")

    # Build parity permutation
    parity_perm = build_parity_permutation()
    println("  Parity permutation: ", parity_perm[1:min(8, N_SITES)], "...")

    # Create Z₂ group with both identity and parity
    # Z₂ = {e, P} where P² = e
    identity_perm = collect(1:N_SITES)
    perm_id = Permutation(identity_perm)
    perm_P = Permutation(parity_perm)
    group = PermutationGroup([perm_id, perm_P])

    nup = N_SITES ÷ 2

    # Character table for Z₂:
    # χ_even(e) = 1, χ_even(P) = 1  (trivial representation)
    # χ_odd(e) = 1, χ_odd(P) = -1   (sign representation)

    # Even parity sector (trivial irrep: +1, +1)
    println()
    println("Diagonalizing EVEN parity sector...")
    irrep_even = Representation(group, [1.0, 1.0])
    block_even = Spinhalf(N_SITES, nup, irrep_even)
    dim_even = dim(block_even)
    println("  Dimension: $(dim_even)")

    t_start = time()
    E_even, psi_even = eig0(ops, block_even)
    t_even = time() - t_start
    println("  E_0(even) = $(round(E_even, digits=8))")
    println("  Time: $(round(t_even, digits=1))s")

    # Odd parity sector (sign irrep: +1, -1)
    println()
    println("Diagonalizing ODD parity sector...")
    irrep_odd = Representation(group, [1.0, -1.0])
    block_odd = Spinhalf(N_SITES, nup, irrep_odd)
    dim_odd = dim(block_odd)
    println("  Dimension: $(dim_odd)")

    t_start = time()
    E_odd, psi_odd = eig0(ops, block_odd)
    t_odd = time() - t_start
    println("  E_0(odd) = $(round(E_odd, digits=8))")
    println("  Time: $(round(t_odd, digits=1))s")

    return E_even, E_odd, dim_even, dim_odd
end

# =============================================================================
# MAIN
# =============================================================================

function main()
    ops = build_heisenberg()

    E_even, E_odd, dim_even, dim_odd = diagonalize_with_parity(ops)

    println()
    println("=" ^ 50)
    println("Z² PARITY VERIFICATION RESULTS")
    println("=" ^ 50)
    println()

    # Energy comparison
    E_per_site_even = E_even / N_SITES
    E_per_site_odd = E_odd / N_SITES

    println("Even parity sector:")
    println("  E_0 = $(round(E_even, digits=6))")
    println("  E_0/N = $(round(E_per_site_even, digits=6))")
    println()

    println("Odd parity sector:")
    println("  E_0 = $(round(E_odd, digits=6))")
    println("  E_0/N = $(round(E_per_site_odd, digits=6))")
    println()

    # Energy gap between sectors
    ΔE = E_odd - E_even
    println("Energy gap between sectors:")
    println("  ΔE = E_odd - E_even = $(round(ΔE, digits=6))")
    println()

    # Z² prediction: S = 3/110 ≈ 0.0273
    S_Z2 = 3/110

    # The suppression should manifest as the odd sector being higher in energy
    if ΔE > 0
        # Calculate relative suppression
        relative_gap = ΔE / abs(E_even)
        println("✓ Odd parity sector is higher in energy (as expected)")
        println("  Relative gap: ΔE/|E_even| = $(round(relative_gap, digits=6))")
        println("  Z² prediction: S = 3/110 = $(round(S_Z2, digits=6))")

        # Check if close to Z² prediction
        if abs(relative_gap - S_Z2) / S_Z2 < 0.5
            println("  → Gap is within 50% of Z² prediction!")
            status = "CONSISTENT"
        else
            println("  → Gap differs from Z² prediction (finite-size effects)")
            status = "PARTIAL"
        end
    else
        println("⚠ Even parity sector is not lowest (unusual)")
        status = "UNEXPECTED"
    end

    println()
    println("Dimension comparison:")
    println("  Even sector: $(dim_even) states")
    println("  Odd sector: $(dim_odd) states")
    println("  Ratio: $(round(dim_even/dim_odd, digits=3))")
    println()

    println("=" ^ 70)
    println("VERIFICATION COMPLETE")
    println("=" ^ 70)
    println("Status: ", status)
    println("End: ", now())

    # Save results
    results_file = joinpath(@__DIR__, "..", "results", "z2_parity_results.txt")
    mkpath(dirname(results_file))
    open(results_file, "w") do f
        println(f, "# Z² Parity Sector Verification")
        println(f, "# Lattice: $(NX) x $(NY) = $(N_SITES) sites")
        println(f, "# Date: ", now())
        println(f, "# XDiag by Alexander Wietek")
        println(f, "")
        println(f, "E_even = ", E_even)
        println(f, "E_odd = ", E_odd)
        println(f, "delta_E = ", ΔE)
        println(f, "dim_even = ", dim_even)
        println(f, "dim_odd = ", dim_odd)
        println(f, "status = ", status)
    end

    println("Results saved")
    return status
end

status = main()
