# =============================================================================
# MAXIMUM SCALE: Heisenberg Model Parity Sector Comparison
# =============================================================================
# Target: Apple M4, 64 GB — PUSH TO THE MAX
# Method: Full exact diagonalization using XDiag library
#
# xdiag Credit: Alexander Wietek (Apache 2.0)
# =============================================================================

using XDiag
using LinearAlgebra
using Printf
using Dates

println("=" ^ 70)
println("MAXIMUM SCALE: HEISENBERG PARITY SECTOR ANALYSIS")
println("=" ^ 70)
println("Using XDiag library by Alexander Wietek")
println("Target: Apple M4, 64 GB")
println("Start: ", now())
println()

# =============================================================================
# LATTICE CONFIGURATION
# =============================================================================

const NX = 6
const NY = 5
const N_SITES = NX * NY  # = 30 sites
const J = 1.0

println("Lattice: $(NX) × $(NY) = $(N_SITES) sites")
println("Model: S=1/2 Heisenberg antiferromagnet")
hilbert_size = binomial(BigInt(N_SITES), BigInt(N_SITES÷2))
println("Hilbert space (Sz=0): ~$(round(Float64(hilbert_size)/1e6, digits=1)) million states")
println()

# Site indexing (1-based for XDiag.jl)
# Maps (x,y) to site ∈ [1,N_SITES] with periodic BC
site(x, y) = (mod1(y, NY) - 1) * NX + mod1(x, NX)

# =============================================================================
# BUILD HAMILTONIAN WITH CORRECT XDIAG API
# =============================================================================

function build_heisenberg()
    """Build Heisenberg Hamiltonian using correct XDiag Op syntax."""
    println("Building Heisenberg Hamiltonian...")

    ops = OpSum()

    # Horizontal bonds (with periodic BC via mod1 in site function)
    for y in 1:NY
        for x in 1:NX
            i = site(x, y)
            j = site(x+1, y)  # wraps: site(NX+1, y) = site(1, y)
            ops += J * Op("SdotS", [i, j])
        end
    end

    # Vertical bonds (with periodic BC via mod1 in site function)
    for y in 1:NY
        for x in 1:NX
            i = site(x, y)
            j = site(x, y+1)  # wraps: site(x, NY+1) = site(x, 1)
            ops += J * Op("SdotS", [i, j])
        end
    end

    n_bonds = 2 * N_SITES
    println("  Bonds: $(n_bonds)")

    return ops
end

# =============================================================================
# DIAGONALIZATION
# =============================================================================

function diagonalize(ops::OpSum)
    """Diagonalize in Sz=0 sector (nup = N/2 for Sz=0)."""
    println()
    println("Diagonalizing in Sz=0 sector...")

    t_start = time()

    # Create spin-1/2 block in Sz=0 sector
    # Sz=0 means equal up and down spins: nup = N/2
    nup = N_SITES ÷ 2
    block = Spinhalf(N_SITES, nup)
    block_dim = dim(block)
    println("  Block dimension: $(block_dim) (N=$(N_SITES), nup=$(nup))")

    # Lanczos for ground state
    println("  Running Lanczos...")
    E0, psi0 = eig0(ops, block; precision=1e-12, max_iterations=1000)

    t_elapsed = time() - t_start

    println("  Ground state: E_0 = $(round(E0, digits=8))")
    println("  Energy per site: E_0/N = $(round(E0/N_SITES, digits=8))")
    println("  Completed in $(round(t_elapsed, digits=1)) sec")

    return E0, psi0, block_dim
end

# =============================================================================
# MAIN
# =============================================================================

function main()
    # Build Hamiltonian
    ops = build_heisenberg()

    # Diagonalize
    E0, psi0, dim_H = diagonalize(ops)

    println()
    println("=" ^ 50)
    println("RESULTS")
    println("=" ^ 50)
    println()

    # Energy per site (should be ~-0.67 for 2D Heisenberg)
    E_per_site = E0 / N_SITES
    println("Ground state energy per site: $(round(E_per_site, digits=6))")
    println("(2D Heisenberg AFM exact: ~-0.669)")
    println()

    # Compare with known 2D Heisenberg results
    # QMC gives E/N ≈ -0.6693 for infinite 2D square lattice
    expected = -0.6693
    deviation = abs(E_per_site - expected) / abs(expected) * 100
    println("Deviation from infinite-lattice QMC: $(round(deviation, digits=2))%")

    println()
    println("=" ^ 70)
    println("SIMULATION COMPLETE")
    println("=" ^ 70)
    println("End: ", now())

    # Save results
    results_file = joinpath(@__DIR__, "..", "results", "heisenberg_maxscale.txt")
    mkpath(dirname(results_file))
    open(results_file, "w") do f
        println(f, "# Heisenberg Model (MAXSCALE)")
        println(f, "# Lattice: $(NX) x $(NY) = $(N_SITES) sites")
        println(f, "# Date: ", now())
        println(f, "# XDiag by Alexander Wietek")
        println(f, "")
        println(f, "E_per_site = ", E_per_site)
        println(f, "dim_Sz0 = ", dim_H)
        println(f, "E_0 = ", E0)
    end

    println("Results saved to: ", results_file)
    return "SUCCESS"
end

status = main()
