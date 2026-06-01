# =============================================================================
# RIGOROUS FINITE-SIZE SCALING: Parity Suppression Factor
# =============================================================================
# Goal: Extract S = lim_{N→∞} (E_odd - E_even)/|E_even|
# Method: Compute for multiple lattice sizes, fit to S(N) = S_∞ + a/N + b/N²
#
# Z² Prediction: S_∞ = 3/110 = 0.02727...
#
# This is the PROPER way to test the Z² prediction.
# xdiag Credit: Alexander Wietek (Apache 2.0)
# =============================================================================

using XDiag
using LinearAlgebra
using Printf
using Dates
using Statistics

println("=" ^ 70)
println("RIGOROUS FINITE-SIZE SCALING ANALYSIS")
println("=" ^ 70)
println("Goal: Extract thermodynamic limit of parity suppression S")
println("Z² Prediction: S = 3/110 = 0.027273")
println("Start: ", now())
println()

const J = 1.0
const S_PREDICTED = 3/110

# Lattice sizes to test (all even for Sz=0 sector)
# Use square-ish lattices to minimize shape effects
const LATTICES = [
    (4, 4),   # N = 16
    (4, 5),   # N = 20
    (4, 6),   # N = 24
    (5, 5),   # N = 25 - skip, odd
    (4, 7),   # N = 28
    (5, 6),   # N = 30
    (6, 6),   # N = 36
]

# Filter to even N
VALID_LATTICES = filter(c -> (c[1]*c[2]) % 2 == 0, LATTICES)

println("Lattices: ", VALID_LATTICES)
println()

# =============================================================================
# COMPUTE PARITY GAP FOR SINGLE LATTICE
# =============================================================================

function compute_parity_gap(Nx, Ny)
    N = Nx * Ny
    site(x, y) = (mod1(y, Ny) - 1) * Nx + mod1(x, Nx)

    # Build Hamiltonian
    ops = OpSum()
    for y in 1:Ny, x in 1:Nx
        i = site(x, y)
        ops += J * Op("SdotS", [i, site(x+1, y)])
        ops += J * Op("SdotS", [i, site(x, y+1)])
    end

    # Build parity symmetry
    parity_perm = zeros(Int, N)
    for y in 1:Ny, x in 1:Nx
        i = site(x, y)
        j = site(Nx + 1 - x, Ny + 1 - y)
        parity_perm[i] = j
    end

    identity_perm = collect(1:N)
    group = PermutationGroup([Permutation(identity_perm), Permutation(parity_perm)])

    nup = N ÷ 2

    # Even sector
    irrep_even = Representation(group, [1.0, 1.0])
    block_even = Spinhalf(N, nup, irrep_even)
    E_even, _ = eig0(ops, block_even)

    # Odd sector
    irrep_odd = Representation(group, [1.0, -1.0])
    block_odd = Spinhalf(N, nup, irrep_odd)
    E_odd, _ = eig0(ops, block_odd)

    ΔE = E_odd - E_even
    S = ΔE / abs(E_even)

    return N, E_even, E_odd, ΔE, S
end

# =============================================================================
# FINITE-SIZE SCALING FIT
# =============================================================================

function fit_finite_size(Ns, Ss)
    """
    Fit S(N) = S_∞ + a/N + b/N²
    Using least squares.
    """
    n = length(Ns)

    # Design matrix: [1, 1/N, 1/N²]
    X = zeros(n, 3)
    for i in 1:n
        X[i, 1] = 1.0
        X[i, 2] = 1.0 / Ns[i]
        X[i, 3] = 1.0 / Ns[i]^2
    end

    # Least squares: β = (X'X)^{-1} X' y
    β = (X' * X) \ (X' * Ss)

    S_inf = β[1]
    a = β[2]
    b = β[3]

    # Compute residuals
    S_fit = X * β
    residuals = Ss - S_fit
    rmse = sqrt(mean(residuals.^2))

    return S_inf, a, b, rmse
end

# =============================================================================
# MAIN
# =============================================================================

function main()
    println("Computing parity gaps for each lattice size...")
    println("-" ^ 70)
    println(@sprintf("%6s  %10s  %10s  %10s  %12s", "N", "E_even", "E_odd", "ΔE", "S = ΔE/|E|"))
    println("-" ^ 70)

    results = []

    for (Nx, Ny) in VALID_LATTICES
        N = Nx * Ny
        print("  $(Nx)×$(Ny) (N=$(N))... ")

        t_start = time()
        N, E_even, E_odd, ΔE, S = compute_parity_gap(Nx, Ny)
        t_elapsed = time() - t_start

        push!(results, (N=N, E_even=E_even, E_odd=E_odd, ΔE=ΔE, S=S))
        println(@sprintf("done in %.1fs", t_elapsed))
        println(@sprintf("%6d  %10.4f  %10.4f  %10.4f  %12.6f", N, E_even, E_odd, ΔE, S))
    end

    println("-" ^ 70)
    println()

    # Extract arrays for fitting
    Ns = [r.N for r in results]
    Ss = [r.S for r in results]

    # Finite-size scaling fit
    println("=" ^ 50)
    println("FINITE-SIZE SCALING FIT")
    println("=" ^ 50)
    println()
    println("Model: S(N) = S_∞ + a/N + b/N²")
    println()

    S_inf, a, b, rmse = fit_finite_size(Ns, Ss)

    println("Fit results:")
    println(@sprintf("  S_∞ = %.6f", S_inf))
    println(@sprintf("  a   = %.4f", a))
    println(@sprintf("  b   = %.4f", b))
    println(@sprintf("  RMSE = %.6f", rmse))
    println()

    println("=" ^ 50)
    println("Z² PREDICTION COMPARISON")
    println("=" ^ 50)
    println()
    println(@sprintf("Extrapolated: S_∞ = %.6f", S_inf))
    println(@sprintf("Z² predicts:  S   = %.6f (3/110)", S_PREDICTED))
    println()

    error_pct = abs(S_inf - S_PREDICTED) / S_PREDICTED * 100
    println(@sprintf("Discrepancy: %.2f%%", error_pct))
    println()

    if error_pct < 20
        println("✓ CONSISTENT: Extrapolated value within 20% of Z² prediction")
        status = "CONSISTENT"
    elseif error_pct < 50
        println("⚠ PARTIAL: Same order of magnitude as Z² prediction")
        status = "PARTIAL"
    elseif S_inf > 0
        println("⚠ QUALITATIVE: Parity suppression observed but magnitude differs")
        status = "QUALITATIVE"
    else
        println("✗ INCONSISTENT: Sign or magnitude wrong")
        status = "INCONSISTENT"
    end

    # Show scaling behavior
    println()
    println("Scaling behavior:")
    for r in results
        S_fit = S_inf + a/r.N + b/r.N^2
        println(@sprintf("  N=%2d: S=%.4f, fit=%.4f, diff=%.4f", r.N, r.S, S_fit, r.S - S_fit))
    end

    println()
    println("End: ", now())
    println("Status: ", status)

    # Save results
    results_file = joinpath(@__DIR__, "..", "results", "finite_size_scaling.txt")
    mkpath(dirname(results_file))
    open(results_file, "w") do f
        println(f, "# Finite-Size Scaling Analysis")
        println(f, "# Date: ", now())
        println(f, "# Model: S(N) = S_inf + a/N + b/N^2")
        println(f, "")
        println(f, "S_inf = ", S_inf)
        println(f, "a = ", a)
        println(f, "b = ", b)
        println(f, "rmse = ", rmse)
        println(f, "S_predicted = ", S_PREDICTED)
        println(f, "error_pct = ", error_pct)
        println(f, "status = ", status)
        println(f, "")
        for r in results
            println(f, "N=$(r.N) E_even=$(r.E_even) E_odd=$(r.E_odd) S=$(r.S)")
        end
    end

    return status, S_inf
end

status, S_inf = main()
