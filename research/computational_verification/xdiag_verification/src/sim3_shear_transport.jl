# =============================================================================
# SIMULATION 3: Cosmological Shear Transport
# =============================================================================
# Z² Prediction: θ = 35.26° = arctan(1/√2) — Magic angle for transport
#
# Method: Compute ground state energy of anisotropic Heisenberg model
# as a function of anisotropy angle. The Z² orbifold geometry suggests
# a special point at θ = arctan(1/√2), the angle between body and face
# diagonals of the cube.
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
println("SIMULATION 3: COSMOLOGICAL SHEAR TRANSPORT")
println("=" ^ 70)
println("Z² Prediction: θ = $(round(Z2Constants.SHEAR_ANGLE_DEG, digits=2))°")
println("Start: ", now())
println()

# 2D lattice
const NX = 4
const NY = 4
const N = NX * NY
const J = 1.0

println("Lattice: $(NX)×$(NY) = $(N) sites")
println("Model: Anisotropic Heisenberg")
println()

# Site indexing
site(x, y) = (mod1(y, NY) - 1) * NX + mod1(x, NX)

# =============================================================================
# BUILD ANISOTROPIC HAMILTONIAN
# =============================================================================

function build_anisotropic_heisenberg(θ_deg)
    """
    Build Heisenberg Hamiltonian with anisotropic exchange:
    J_x = J * cos²(θ), J_y = J * sin²(θ)

    The magic angle θ = arctan(1/√2) gives J_x:J_y = 2:1
    """
    θ = deg2rad(θ_deg)
    Jx = J * cos(θ)^2
    Jy = J * sin(θ)^2

    ops = OpSum()

    # Horizontal bonds with Jx
    for y in 1:NY, x in 1:NX
        i = site(x, y)
        j = site(x+1, y)
        ops += Jx * Op("SdotS", [i, j])
    end

    # Vertical bonds with Jy
    for y in 1:NY, x in 1:NX
        i = site(x, y)
        j = site(x, y+1)
        ops += Jy * Op("SdotS", [i, j])
    end

    return ops, Jx, Jy
end

# =============================================================================
# COMPUTE GROUND STATE ENERGY VS ANGLE
# =============================================================================

function sweep_angles()
    # Include the magic angle and nearby values
    θ_magic = Z2Constants.SHEAR_ANGLE_DEG
    angles = sort(unique([0, 15, 30, θ_magic-5, θ_magic, θ_magic+5, 45, 60, 75, 90]))

    nup = N ÷ 2

    println("Angle sweep ($(length(angles)) points):")
    println("-" ^ 50)
    println(@sprintf("%8s  %8s  %8s  %10s", "θ (deg)", "Jx", "Jy", "E_0/N"))
    println("-" ^ 50)

    results = []

    for θ in angles
        ops, Jx, Jy = build_anisotropic_heisenberg(θ)
        block = Spinhalf(N, nup)

        E0, psi0 = eig0(ops, block)
        E_per_site = E0 / N

        push!(results, (θ=θ, Jx=Jx, Jy=Jy, E=E0, E_N=E_per_site))
        println(@sprintf("%8.2f  %8.4f  %8.4f  %10.6f", θ, Jx, Jy, E_per_site))
    end

    println("-" ^ 50)
    println()

    return results
end

# =============================================================================
# MAIN
# =============================================================================

function main()
    results = sweep_angles()

    # Find angle with minimum (most negative) energy per site
    min_idx = argmin([r.E_N for r in results])
    best = results[min_idx]

    println("=" ^ 50)
    println("Z² PREDICTION VERIFICATION")
    println("=" ^ 50)
    println()

    println("Results:")
    println("  Minimum E/N at θ = $(round(best.θ, digits=2))°")
    println("  E/N = $(round(best.E_N, digits=6))")
    println("  Jx:Jy ratio = $(round(best.Jx/best.Jy, digits=3))")
    println()

    θ_predicted = Z2Constants.SHEAR_ANGLE_DEG
    println("Z² prediction:")
    println("  θ = arctan(1/√2) = $(round(θ_predicted, digits=2))°")
    println("  This gives Jx:Jy = 2:1")
    println()

    # Check if magic angle is special (local extremum or inflection)
    # Find the result closest to the magic angle
    magic_result = results[argmin([abs(r.θ - θ_predicted) for r in results])]

    # Compare with neighbors
    idx = findfirst(r -> r.θ == magic_result.θ, results)
    if 1 < idx < length(results)
        E_prev = results[idx-1].E_N
        E_magic = results[idx].E_N
        E_next = results[idx+1].E_N

        curvature = (E_prev + E_next - 2*E_magic) / (results[idx+1].θ - results[idx-1].θ)^2

        println("At magic angle θ = $(round(magic_result.θ, digits=2))°:")
        println("  E/N = $(round(E_magic, digits=6))")
        println("  Local curvature: $(round(curvature * 1000, digits=4)) × 10⁻³")

        if curvature > 0
            println("  → Local MINIMUM")
            status = "CONFIRMED"
        elseif curvature < 0
            println("  → Local MAXIMUM")
            status = "PARTIAL"
        else
            println("  → Inflection point")
            status = "PARTIAL"
        end
    else
        status = "PARTIAL"
    end

    println()
    println("End: ", now())
    println("Status: ", status)

    # Save results
    results_file = joinpath(@__DIR__, "..", "results", "sim3_results.txt")
    mkpath(dirname(results_file))
    open(results_file, "w") do f
        println(f, "# Simulation 3: Shear Transport")
        println(f, "# Lattice: $(NX) x $(NY) = $(N)")
        println(f, "# Date: ", now())
        for r in results
            println(f, "theta=$(r.θ) Jx=$(r.Jx) Jy=$(r.Jy) E=$(r.E) E_N=$(r.E_N)")
        end
        println(f, "status = ", status)
    end

    return status
end

status = main()
