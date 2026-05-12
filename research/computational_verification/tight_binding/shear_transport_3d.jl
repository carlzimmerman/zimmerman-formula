#!/usr/bin/env julia
#=
================================================================================
3D TIGHT-BINDING MODEL WITH SHEAR - MAGIC ANGLE 35.26°
================================================================================

Objective: Test whether the body diagonal angle θ = arctan(1/√2) ≈ 35.26°
shows a transport anomaly in a 3D tight-binding model with spatial shear.

The key difference from Heisenberg spin models:
- Here we have SPATIAL COORDINATES (x, y, z)
- The hopping matrix t_ij depends on geometry
- We can apply a shear tensor σ_ij along specific directions
- We measure conductivity σ(θ) as a function of measurement angle

Physics:
- 3D tight-binding Hamiltonian: H = -Σ_{<i,j>} t_ij (c†_i c_j + h.c.)
- Apply shear along body diagonal (1,1,1) direction
- Measure Drude weight / DC conductivity
- Look for anomaly at θ = arctan(1/√2) ≈ 35.26°

References:
- Kubo formula for conductivity
- Drude weight from current-current correlator
================================================================================
=#

using LinearAlgebra
using SparseArrays
using Printf
using Statistics

println("=" ^ 70)
println("3D TIGHT-BINDING SHEAR TRANSPORT")
println("Testing Magic Angle θ = arctan(1/√2) ≈ 35.26°")
println("=" ^ 70)
println()

# =============================================================================
# LATTICE SETUP
# =============================================================================

"""
    site_index(x, y, z, L)

Convert 3D coordinates (1-based) to linear site index.
"""
function site_index(x::Int, y::Int, z::Int, L::Int)
    return x + (y - 1) * L + (z - 1) * L^2
end

"""
    index_to_site(idx, L)

Convert linear index to 3D coordinates.
"""
function index_to_site(idx::Int, L::Int)
    z = div(idx - 1, L^2) + 1
    rem_z = mod(idx - 1, L^2)
    y = div(rem_z, L) + 1
    x = mod(rem_z, L) + 1
    return (x, y, z)
end

"""
    site_position(x, y, z, a=1.0)

Return the real-space position of a site.
"""
function site_position(x::Int, y::Int, z::Int; a::Float64=1.0)
    return a .* Float64.([x, y, z])
end

# =============================================================================
# TIGHT-BINDING HAMILTONIAN WITH SHEAR
# =============================================================================

"""
    build_hopping_matrix(L, t0; shear_tensor=zeros(3,3))

Build the tight-binding hopping matrix for a 3D cubic lattice.

H = -Σ_{<i,j>} t_ij (c†_i c_j + h.c.)

where t_ij = t0 × (1 + r̂_ij · σ · r̂_ij) for shear tensor σ.
The shear modifies hopping along different directions.
"""
function build_hopping_matrix(L::Int, t0::Float64; shear_tensor::Matrix{Float64}=zeros(3,3))
    N = L^3

    I_idx = Int[]
    J_idx = Int[]
    V = Float64[]

    # Nearest-neighbor hopping vectors
    neighbors = [
        (1, 0, 0),   # +x
        (-1, 0, 0),  # -x
        (0, 1, 0),   # +y
        (0, -1, 0),  # -y
        (0, 0, 1),   # +z
        (0, 0, -1)   # -z
    ]

    for z in 1:L, y in 1:L, x in 1:L
        site_i = site_index(x, y, z, L)

        for (dx, dy, dz) in neighbors
            # Neighbor with periodic BC
            xn = mod1(x + dx, L)
            yn = mod1(y + dy, L)
            zn = mod1(z + dz, L)
            site_j = site_index(xn, yn, zn, L)

            # Direction unit vector
            r_hat = Float64.([dx, dy, dz])
            r_hat ./= norm(r_hat)

            # Shear modification: t = t0 × (1 + r̂ · σ · r̂)
            shear_factor = 1.0 + dot(r_hat, shear_tensor * r_hat)
            t_ij = -t0 * shear_factor

            push!(I_idx, site_i)
            push!(J_idx, site_j)
            push!(V, t_ij)
        end
    end

    H = sparse(I_idx, J_idx, V, N, N)
    return Hermitian(Matrix(H))  # Make Hermitian for eigensolve
end

"""
    build_current_operator(L, direction; a=1.0)

Build the current operator in a given direction.

J_α = (ie/ℏ) Σ_{<i,j>} (r_j - r_i)_α t_ij (c†_i c_j - c†_j c_i)

For the Drude weight, we need:
    D_α = -(1/N) <ψ₀| ∂²H/∂k_α² |ψ₀> + (2/N) Σ_{n≠0} |<ψ_n|J_α|ψ₀>|² / (E_n - E₀)

Simplified: We compute <J_α²> to get the Drude weight.
"""
function build_current_operator(L::Int, direction::Vector{Float64}; t0::Float64=1.0)
    N = L^3

    I_idx = Int[]
    J_idx = Int[]
    V = Complex{Float64}[]

    # Normalize direction
    d_hat = direction / norm(direction)

    neighbors = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1)
    ]

    for z in 1:L, y in 1:L, x in 1:L
        site_i = site_index(x, y, z, L)

        for (dx, dy, dz) in neighbors
            xn = mod1(x + dx, L)
            yn = mod1(y + dy, L)
            zn = mod1(z + dz, L)
            site_j = site_index(xn, yn, zn, L)

            # Displacement vector
            r_ij = Float64.([dx, dy, dz])

            # Current contribution: i × r_ij · d_hat × t_ij
            J_contrib = im * dot(r_ij, d_hat) * t0

            push!(I_idx, site_i)
            push!(J_idx, site_j)
            push!(V, J_contrib)
        end
    end

    J = sparse(I_idx, J_idx, V, N, N)
    return J
end

# =============================================================================
# DRUDE WEIGHT CALCULATION
# =============================================================================

"""
    compute_drude_weight(H, J)

Compute the Drude weight from the Kubo formula.

For a gapped/metallic system at T=0, the Drude weight is:
    D = (π/N) Σ_n f_n <n|(-∂²H/∂k²)|n>

For a half-filled band, we sum over occupied states.
We approximate using the current-current correlator.
"""
function compute_drude_weight(H::Hermitian{Float64, Matrix{Float64}},
                              J::SparseMatrixCSC{Complex{Float64}, Int64};
                              filling::Float64=0.5)
    N = size(H, 1)
    n_occupied = round(Int, filling * N)

    # Diagonalize
    E, V = eigen(H)

    # Compute <J²> for occupied states
    J_dense = Matrix(J)
    J_sq_trace = 0.0

    for n in 1:n_occupied
        psi_n = V[:, n]
        J_psi = J_dense * psi_n
        J_sq_trace += real(dot(psi_n, J_dense * J_psi))
    end

    # Drude weight (simplified formula)
    D = -J_sq_trace / N

    return D, E
end

# =============================================================================
# ANGLE SWEEP
# =============================================================================

"""
    sweep_measurement_angle(L, t0, shear_magnitude; n_angles=37)

Sweep the measurement direction from 0° to 90° relative to x-axis
in the xz-plane, and measure the Drude weight.

Look for anomaly at θ = arctan(1/√2) ≈ 35.26° (body diagonal projection).
"""
function sweep_measurement_angle(L::Int, t0::Float64, shear_magnitude::Float64;
                                  n_angles::Int=37)
    println("Lattice size: L = $L (N = $(L^3) sites)")
    println("Hopping: t₀ = $t0")
    println("Shear magnitude: σ = $shear_magnitude")
    println()

    # Magic angle
    θ_magic = atan(1/√2)
    θ_magic_deg = rad2deg(θ_magic)
    println("Magic angle: θ = arctan(1/√2) = $(round(θ_magic_deg, digits=2))°")
    println()

    # Shear tensor along body diagonal (1,1,1)
    # Traceless shear: σ_ij = σ × (3 d_i d_j - δ_ij) where d = (1,1,1)/√3
    d = [1.0, 1.0, 1.0] / √3
    shear_tensor = shear_magnitude * (3 * d * d' - I(3))

    println("Building Hamiltonian with shear tensor...")
    H = build_hopping_matrix(L, t0; shear_tensor=shear_tensor)
    println("  Done.")
    println()

    # Angle sweep in xz-plane
    angles_deg = range(0, 90, length=n_angles)
    drude_weights = Float64[]

    println("Sweeping measurement angle from 0° to 90°...")
    println("-" ^ 50)
    println(@sprintf("%10s  %15s", "θ (deg)", "Drude Weight"))
    println("-" ^ 50)

    for θ_deg in angles_deg
        θ = deg2rad(θ_deg)

        # Measurement direction in xz-plane
        direction = [cos(θ), 0.0, sin(θ)]

        # Current operator
        J = build_current_operator(L, direction; t0=t0)

        # Drude weight
        D, _ = compute_drude_weight(H, J)
        push!(drude_weights, abs(D))

        # Mark magic angle
        marker = abs(θ_deg - θ_magic_deg) < 2.0 ? " ← MAGIC" : ""
        println(@sprintf("%10.2f  %15.6f%s", θ_deg, abs(D), marker))
    end

    println("-" ^ 50)
    println()

    return collect(angles_deg), drude_weights, θ_magic_deg
end

# =============================================================================
# ANALYSIS
# =============================================================================

"""
    analyze_anomaly(angles, drude_weights, θ_magic)

Analyze whether there's an anomaly at the magic angle.
"""
function analyze_anomaly(angles::Vector{Float64}, drude_weights::Vector{Float64},
                         θ_magic::Float64)
    println("ANOMALY ANALYSIS")
    println("=" ^ 60)
    println()

    # Find the value at the magic angle
    idx_magic = argmin(abs.(angles .- θ_magic))
    D_magic = drude_weights[idx_magic]
    θ_at_magic = angles[idx_magic]

    # Find min and max
    D_min, idx_min = findmin(drude_weights)
    D_max, idx_max = findmax(drude_weights)

    println("Results:")
    println(@sprintf("  Drude weight at θ = %.2f° (magic): D = %.6f", θ_at_magic, D_magic))
    println(@sprintf("  Minimum: D = %.6f at θ = %.2f°", D_min, angles[idx_min]))
    println(@sprintf("  Maximum: D = %.6f at θ = %.2f°", D_max, angles[idx_max]))
    println()

    # Check if magic angle is special
    D_mean = mean(drude_weights)
    D_std = std(drude_weights)

    deviation = (D_magic - D_mean) / D_std

    println("Statistical analysis:")
    println(@sprintf("  Mean Drude weight: %.6f", D_mean))
    println(@sprintf("  Std deviation: %.6f", D_std))
    println(@sprintf("  Magic angle deviation: %.2f σ from mean", deviation))
    println()

    # Check for local extremum near magic angle
    is_local_min = false
    is_local_max = false

    if idx_magic > 1 && idx_magic < length(drude_weights)
        if D_magic < drude_weights[idx_magic-1] && D_magic < drude_weights[idx_magic+1]
            is_local_min = true
        elseif D_magic > drude_weights[idx_magic-1] && D_magic > drude_weights[idx_magic+1]
            is_local_max = true
        end
    end

    println("Local structure at magic angle:")
    if is_local_min
        println("  ✓ LOCAL MINIMUM detected at magic angle!")
    elseif is_local_max
        println("  ✓ LOCAL MAXIMUM detected at magic angle!")
    else
        println("  No local extremum at magic angle")
    end
    println()

    # Relative anomaly
    if D_mean > 0
        relative_anomaly = (D_magic - D_mean) / D_mean * 100
        println(@sprintf("Relative anomaly: %.2f%% from mean", relative_anomaly))
    end

    return deviation, is_local_min || is_local_max
end

# =============================================================================
# MAIN
# =============================================================================

function main()
    println("=" ^ 70)
    println("3D TIGHT-BINDING SHEAR TRANSPORT SIMULATION")
    println("Testing Z² Magic Angle θ = arctan(1/√2) ≈ 35.26°")
    println("=" ^ 70)
    println()

    # Parameters
    L = 8          # Lattice size (8³ = 512 sites)
    t0 = 1.0       # Hopping amplitude
    σ = 0.1        # Shear magnitude

    # Sweep angles
    angles, drude_weights, θ_magic = sweep_measurement_angle(L, t0, σ; n_angles=37)

    # Analyze
    deviation, is_extremum = analyze_anomaly(angles, drude_weights, θ_magic)

    # Summary
    println()
    println("=" ^ 70)
    println("SUMMARY")
    println("=" ^ 70)
    println()

    if is_extremum
        println("✓ ANOMALY DETECTED at magic angle θ = 35.26°")
        println("  The body diagonal direction shows special transport properties.")
    else
        if abs(deviation) > 1.5
            println("⚠ PARTIAL SIGNAL: Magic angle shows $(round(deviation, digits=2))σ deviation")
            println("  May indicate underlying structure, but not a clear extremum.")
        else
            println("✗ No clear anomaly at magic angle in this parameter regime.")
            println("  This may require:")
            println("    - Larger system size")
            println("    - Different shear magnitude")
            println("    - Different observable (e.g., Hall conductivity)")
        end
    end

    println()
    println("Physical interpretation:")
    println("  The angle θ = arctan(1/√2) ≈ 35.26° is the angle between")
    println("  a cube face normal and the body diagonal (1,1,1).")
    println()
    println("  In the Z² framework, this angle appears in:")
    println("  - Gravitational wave polarization")
    println("  - Shear viscosity tensor")
    println("  - Transport along preferred directions in extra dimensions")
    println()

    return angles, drude_weights, deviation
end

# Run
angles, drude_weights, deviation = main()
