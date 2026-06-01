# =============================================================================
# CASIMIR ENERGY ON T³/Z₂ ORBIFOLD
# =============================================================================
# Goal: Test whether aspect ratio 13:19 minimizes vacuum energy
#
# Physics: On the orbifold T³/Z₂, the Z₂ action is x → -x
# This projects out odd-parity modes, leaving only even modes.
# The Casimir energy is the sum of zero-point energies of allowed modes.
#
# For a massless scalar field:
#   E_Casimir = (1/2) Σ_k |k|  (with regularization)
#
# On T³ with sides L₁, L₂, L₃:
#   k = 2π(n₁/L₁, n₂/L₂, n₃/L₃)  for n_i ∈ ℤ
#
# On T³/Z₂, only even modes survive:
#   Either all n_i even, or specific combinations
#
# Z² Prediction: Minimum at L₁:L₂ = 13:19
# =============================================================================

using Printf
using Dates

println("=" ^ 70)
println("CASIMIR ENERGY ON T³/Z₂ ORBIFOLD")
println("=" ^ 70)
println("Z² Prediction: Energy minimum at aspect ratio 13:19 = 0.6842")
println("Start: ", now())
println()

# =============================================================================
# CASIMIR ENERGY CALCULATION
# =============================================================================

function casimir_energy_t3(L1, L2, L3; n_max=50, regularize=true)
    """
    Compute regularized Casimir energy for scalar field on T³.
    Uses zeta function regularization (effectively).

    E = (1/2) Σ_{n≠0} |k_n| with cutoff

    For proper comparison, we compute E * (L1*L2*L3)^(1/3) to get
    dimensionless energy density.
    """
    E = 0.0

    for n1 in -n_max:n_max
        for n2 in -n_max:n_max
            for n3 in -n_max:n_max
                if n1 == 0 && n2 == 0 && n3 == 0
                    continue  # Skip zero mode
                end

                # Momentum magnitude
                k_sq = (2π * n1 / L1)^2 + (2π * n2 / L2)^2 + (2π * n3 / L3)^2
                k = sqrt(k_sq)

                # Regularization: exponential cutoff
                if regularize
                    cutoff = exp(-k / (2π * n_max / min(L1, L2, L3)))
                else
                    cutoff = 1.0
                end

                E += 0.5 * k * cutoff
            end
        end
    end

    # Normalize by volume^(1/3) for dimensionless comparison
    V = L1 * L2 * L3
    E_normalized = E * V^(1/3)

    return E, E_normalized
end

function casimir_energy_t3z2(L1, L2, L3; n_max=50, regularize=true)
    """
    Compute Casimir energy on T³/Z₂ orbifold.

    The Z₂ action x → -x projects to even modes.
    For scalar field: only modes with even parity under k → -k survive.
    This means we sum over |n_i| only (avoiding double counting).

    Actually, for Z₂ orbifold, the mode counting is:
    - Bulk modes: sum over n_i ≥ 0 with factor 1/2 for boundary
    - Fixed points contribute additional terms

    Simplified: sum over n_i ≥ 0 (half the modes of T³)
    """
    E = 0.0

    for n1 in 0:n_max
        for n2 in 0:n_max
            for n3 in 0:n_max
                if n1 == 0 && n2 == 0 && n3 == 0
                    continue
                end

                # Multiplicity factor for orbifold
                mult = 1.0
                if n1 > 0
                    mult *= 2
                end
                if n2 > 0
                    mult *= 2
                end
                if n3 > 0
                    mult *= 2
                end
                mult /= 2  # Z₂ projection

                k_sq = (2π * n1 / L1)^2 + (2π * n2 / L2)^2 + (2π * n3 / L3)^2
                k = sqrt(k_sq)

                if regularize
                    cutoff = exp(-k / (2π * n_max / min(L1, L2, L3)))
                else
                    cutoff = 1.0
                end

                E += 0.5 * mult * k * cutoff
            end
        end
    end

    V = L1 * L2 * L3
    E_normalized = E * V^(1/3)

    return E, E_normalized
end

# =============================================================================
# ASPECT RATIO SWEEP
# =============================================================================

function sweep_aspect_ratios()
    """
    For fixed volume, sweep aspect ratios and find energy minimum.
    Fix L3 = 1, vary L1/L2 ratio, adjust L2 to keep volume constant.
    """
    V_target = 1.0  # Fixed volume
    L3 = 1.0

    # Aspect ratios to test
    ratios = [0.3, 0.4, 0.5, 0.55, 0.6, 0.65, 13/19, 0.7, 0.75, 0.8, 0.9, 1.0]

    println("Aspect ratio sweep (fixed volume = $(V_target)):")
    println("-" ^ 60)
    println(@sprintf("%10s  %10s  %10s  %12s  %12s", "L1/L2", "L1", "L2", "E_T³", "E_T³/Z₂"))
    println("-" ^ 60)

    results_t3 = []
    results_z2 = []

    for r in ratios
        # For ratio L1/L2 = r, with L3 = 1 and V = L1*L2*L3 = 1:
        # L1 = r*L2, so r*L2^2 = 1, L2 = 1/sqrt(r), L1 = sqrt(r)
        L2 = 1 / sqrt(r)
        L1 = sqrt(r)

        E_t3, E_t3_norm = casimir_energy_t3(L1, L2, L3; n_max=30)
        E_z2, E_z2_norm = casimir_energy_t3z2(L1, L2, L3; n_max=30)

        push!(results_t3, (ratio=r, L1=L1, L2=L2, E=E_t3, E_norm=E_t3_norm))
        push!(results_z2, (ratio=r, L1=L1, L2=L2, E=E_z2, E_norm=E_z2_norm))

        r_str = r == 13/19 ? "13/19" : @sprintf("%.4f", r)
        println(@sprintf("%10s  %10.4f  %10.4f  %12.4f  %12.4f", r_str, L1, L2, E_t3_norm, E_z2_norm))
    end

    println("-" ^ 60)
    println()

    return results_t3, results_z2
end

# =============================================================================
# MAIN
# =============================================================================

function main()
    results_t3, results_z2 = sweep_aspect_ratios()

    # Find minima
    min_t3 = argmin([r.E_norm for r in results_t3])
    min_z2 = argmin([r.E_norm for r in results_z2])

    best_t3 = results_t3[min_t3]
    best_z2 = results_z2[min_z2]

    println("=" ^ 50)
    println("RESULTS")
    println("=" ^ 50)
    println()

    println("T³ (no orbifold):")
    println("  Minimum at ratio = $(round(best_t3.ratio, digits=4))")
    println("  E_normalized = $(round(best_t3.E_norm, digits=4))")
    println()

    println("T³/Z₂ (orbifold):")
    println("  Minimum at ratio = $(round(best_z2.ratio, digits=4))")
    println("  E_normalized = $(round(best_z2.E_norm, digits=4))")
    println()

    # Compare with 13/19
    target_ratio = 13/19
    println("Z² prediction: 13/19 = $(round(target_ratio, digits=4))")
    println()

    # Find energy at 13/19
    idx_1319 = findfirst(r -> r.ratio == 13/19, results_z2)
    if idx_1319 !== nothing
        E_1319 = results_z2[idx_1319].E_norm
        E_min = best_z2.E_norm

        println("At 13/19:")
        println("  E_normalized = $(round(E_1319, digits=4))")
        println("  vs minimum = $(round(E_min, digits=4))")
        println("  Difference = $(round((E_1319 - E_min)/E_min * 100, digits=2))%")
        println()

        if abs(best_z2.ratio - target_ratio) < 0.05
            println("✓ CONFIRMED: Minimum near 13/19!")
            status = "CONFIRMED"
        elseif (E_1319 - E_min) / E_min < 0.05
            println("⚠ CLOSE: 13/19 within 5% of minimum")
            status = "CLOSE"
        else
            println("✗ NOT CONFIRMED: Minimum not at 13/19")
            status = "NOT_CONFIRMED"
        end
    else
        status = "ERROR"
    end

    println()
    println("Note: This is a simplified calculation. Full treatment requires:")
    println("  - Proper zeta function regularization")
    println("  - Fixed point contributions")
    println("  - Massive modes if applicable")
    println()
    println("End: ", now())
    println("Status: ", status)

    # Save results
    results_file = joinpath(@__DIR__, "..", "results", "casimir_t3z2.txt")
    mkpath(dirname(results_file))
    open(results_file, "w") do f
        println(f, "# Casimir Energy on T³/Z₂")
        println(f, "# Date: ", now())
        println(f, "")
        println(f, "best_ratio_t3 = ", best_t3.ratio)
        println(f, "best_ratio_z2 = ", best_z2.ratio)
        println(f, "target_ratio = ", target_ratio)
        println(f, "status = ", status)
        println(f, "")
        println(f, "# T³/Z₂ results:")
        for r in results_z2
            println(f, "ratio=$(r.ratio) E_norm=$(r.E_norm)")
        end
    end

    return status
end

status = main()
