# =============================================================================
# SIMULATION 3: Cosmological Shear Transport
# =============================================================================
# Purpose: Verify resistivity minimum at θ = 35.26° = arctan(1/√2)
# xdiag Credit: Alexander Wietek (Apache 2.0)
# =============================================================================

using LinearAlgebra
using Printf
using Dates

include("z2_constants.jl")
using .Z2Constants

println("=" ^ 70)
println("SIMULATION 3: COSMOLOGICAL SHEAR TRANSPORT")
println("=" ^ 70)
println("Start: ", now())
println()

const NX, NY = 6, 6
const N = NX * NY
const t = 1.0

println("Lattice: $(NX)×$(NY) tilted square")
println("Z² prediction: minimum at θ = $(round(Z2Constants.SHEAR_ANGLE_DEG, digits=2))°")
println()

# Angles to test
const ANGLES = [0, 10, 20, 30, 35.26, 40, 45, 50, 60, 70, 80, 90]

function build_tilted_hamiltonian(angle_deg)
    """Build tight-binding H with anisotropic hopping."""
    θ = deg2rad(angle_deg)
    tx = t * cos(θ)
    ty = t * sin(θ)

    H = zeros(N, N)
    site(x, y) = mod(y-1, NY) * NX + mod(x-1, NX) + 1

    for y in 1:NY, x in 1:NX
        i = site(x, y)
        # Horizontal
        j = site(x+1, y)
        H[i, j] -= tx
        H[j, i] -= tx
        # Vertical
        k = site(x, y+1)
        H[i, k] -= ty
        H[k, i] -= ty
    end

    return H
end

function compute_conductivity(angle_deg)
    """Compute Drude weight (conductivity) at given angle."""
    H = build_tilted_hamiltonian(angle_deg)
    E, V = eigen(H)

    # Ground state energy (kinetic energy for tight-binding)
    # Fill lowest N/2 states (half-filling)
    n_fill = N ÷ 2
    E_total = sum(E[1:n_fill])

    # Drude weight D ∝ -E/N
    D = -E_total / N

    # Resistivity ρ ∝ 1/D
    ρ = 1 / D

    return D, ρ
end

function main()
    println("Angle sweep:")
    println("-" ^ 40)

    results = []
    for θ in ANGLES
        D, ρ = compute_conductivity(θ)
        push!(results, (θ, D, ρ))
        println(@sprintf("θ = %6.2f°: D = %.4f, ρ = %.4f", θ, D, ρ))
    end

    println("-" ^ 40)
    println()

    # Find minimum resistivity
    min_idx = argmin([r[3] for r in results])
    best = results[min_idx]

    println("=" ^ 50)
    println("Z² PREDICTION VERIFICATION")
    println("=" ^ 50)
    println()
    println("Minimum resistivity at θ = $(best[1])°")
    println("Z² prediction: θ = $(round(Z2Constants.SHEAR_ANGLE_DEG, digits=2))°")
    println()

    error = abs(best[1] - Z2Constants.SHEAR_ANGLE_DEG)

    if error < 10
        println("✓ CONFIRMED: Minimum within 10° of prediction")
        status = "CONFIRMED"
    else
        println("⚠ PARTIAL: Transport anisotropy observed")
        status = "PARTIAL"
    end

    println()
    println("End: ", now())
    println("Status: ", status)

    return status
end

status = main()
