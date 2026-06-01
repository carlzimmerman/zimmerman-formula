# =============================================================================
# SIMULATION 4: Vacuum Partition Resonance
# =============================================================================
#
# ⚠️  DEPRECATED: This prediction has been FALSIFIED (May 12, 2026).
#
# The amplitude audit proved that:
# - Casimir energy E(α) has minimum at α = 1 (square), NOT at 13/19
# - There is NO physical mechanism connecting cosmological Ω_Λ to cavity geometry
# - Scale mismatch: cosmological (10²⁶ m) vs lab-scale
#
# This simulation is retained for historical record only.
# See: research/theoretical/AMPLITUDE_AUDIT_RESULTS.md
#
# Original (incorrect) claim: Aspect ratio 13:19 — Energy minimum
#
# xdiag Credit: Alexander Wietek (Apache 2.0)
# =============================================================================

using XDiag
using LinearAlgebra
using Printf
using Dates

include("z2_constants.jl")
using .Z2Constants

println("=" ^ 70)
println("SIMULATION 4: VACUUM PARTITION RESONANCE")
println("=" ^ 70)
println("Z² Prediction: Energy minimum at ratio 13/19 = $(round(13/19, digits=4))")
println("Start: ", now())
println()

const J = 1.0

# Aspect ratios to test (keeping total sites manageable)
# Target: ratio close to 13/19 ≈ 0.684
const CONFIGS = [
    (3, 4),   # 0.75, N=12
    (3, 5),   # 0.60, N=15 (odd, skip)
    (4, 4),   # 1.00, N=16
    (4, 5),   # 0.80, N=20
    (4, 6),   # 0.67, N=24  ← close to 13/19
    (3, 6),   # 0.50, N=18
    (4, 7),   # 0.57, N=28
    (5, 6),   # 0.83, N=30
    (5, 7),   # 0.71, N=35 (odd, skip)
]

# Filter to even N only (for Sz=0)
VALID_CONFIGS = filter(c -> (c[1]*c[2]) % 2 == 0, CONFIGS)

println("Testing $(length(VALID_CONFIGS)) lattice configurations")
println()

# =============================================================================
# BUILD HAMILTONIAN FOR GIVEN LATTICE
# =============================================================================

function build_heisenberg(Nx, Ny)
    N = Nx * Ny
    site(x, y) = (mod1(y, Ny) - 1) * Nx + mod1(x, Nx)

    ops = OpSum()

    # Horizontal bonds
    for y in 1:Ny, x in 1:Nx
        i = site(x, y)
        j = site(x+1, y)
        ops += J * Op("SdotS", [i, j])
    end

    # Vertical bonds
    for y in 1:Ny, x in 1:Nx
        i = site(x, y)
        j = site(x, y+1)
        ops += J * Op("SdotS", [i, j])
    end

    return ops, N
end

# =============================================================================
# COMPUTE GROUND STATE ENERGY FOR EACH CONFIGURATION
# =============================================================================

function sweep_aspect_ratios()
    println("Aspect ratio sweep:")
    println("-" ^ 60)
    println(@sprintf("%8s  %6s  %8s  %12s  %12s", "Nx×Ny", "N", "Aspect", "E_0", "E/N"))
    println("-" ^ 60)

    results = []

    for (Nx, Ny) in VALID_CONFIGS
        N = Nx * Ny
        nup = N ÷ 2
        aspect = Nx / Ny

        ops, _ = build_heisenberg(Nx, Ny)
        block = Spinhalf(N, nup)

        E0, psi0 = eig0(ops, block)
        E_per_site = E0 / N

        push!(results, (Nx=Nx, Ny=Ny, N=N, aspect=aspect, E=E0, E_N=E_per_site))
        println(@sprintf("%4d×%-3d  %6d  %8.4f  %12.6f  %12.6f", Nx, Ny, N, aspect, E0, E_per_site))
    end

    println("-" ^ 60)
    println()

    return results
end

# =============================================================================
# MAIN
# =============================================================================

function main()
    results = sweep_aspect_ratios()

    # Find minimum E/N
    min_idx = argmin([r.E_N for r in results])
    best = results[min_idx]

    println("=" ^ 50)
    println("Z² PREDICTION VERIFICATION")
    println("=" ^ 50)
    println()

    println("Results:")
    println("  Minimum E/N at $(best.Nx)×$(best.Ny)")
    println("  Aspect ratio = $(round(best.aspect, digits=4))")
    println("  E/N = $(round(best.E_N, digits=6))")
    println()

    target_ratio = Z2Constants.VACUUM_RATIO  # 13/19
    println("Z² prediction:")
    println("  Aspect ratio = 13/19 = $(round(target_ratio, digits=4))")
    println()

    # Find lattice closest to 13/19
    closest_idx = argmin([abs(r.aspect - target_ratio) for r in results])
    closest = results[closest_idx]

    println("Lattice closest to predicted ratio:")
    println("  $(closest.Nx)×$(closest.Ny), ratio = $(round(closest.aspect, digits=4))")
    println("  E/N = $(round(closest.E_N, digits=6))")
    println()

    # Compare
    if closest.E_N <= minimum([r.E_N for r in results]) + 0.01
        println("✓ CONFIRMED: Lattice near 13:19 has lowest/near-lowest energy")
        status = "CONFIRMED"
    else
        # Check if it's at least in the lower half
        sorted = sort(results, by=r->r.E_N)
        rank = findfirst(r -> r.Nx == closest.Nx && r.Ny == closest.Ny, sorted)
        if rank <= length(results) ÷ 2
            println("✓ PARTIAL: Lattice near 13:19 is in lower half of energies")
            status = "PARTIAL"
        else
            println("⚠ NOT CONFIRMED: No special behavior at 13:19 ratio")
            status = "NOT_CONFIRMED"
        end
    end

    println()
    println("Note: Finite-size effects are significant for small lattices.")
    println("      Thermodynamic limit needed for rigorous test.")
    println()
    println("End: ", now())
    println("Status: ", status)

    # Save results
    results_file = joinpath(@__DIR__, "..", "results", "sim4_results.txt")
    mkpath(dirname(results_file))
    open(results_file, "w") do f
        println(f, "# Simulation 4: Vacuum Resonance")
        println(f, "# Date: ", now())
        for r in results
            println(f, "Nx=$(r.Nx) Ny=$(r.Ny) aspect=$(r.aspect) E=$(r.E) E_N=$(r.E_N)")
        end
        println(f, "best = $(best.Nx)x$(best.Ny)")
        println(f, "status = ", status)
    end

    return status
end

status = main()
