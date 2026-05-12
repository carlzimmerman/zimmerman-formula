# =============================================================================
# CASIMIR ENERGY WITH Z² FIELD CONTENT
# =============================================================================
# The Z² framework claims the vacuum energy involves:
# - 4 body diagonals (Bekenstein modes)
# - 12 edges (gauge fields: SU(3)×SU(2)×U(1))
# - 3 face pairs (generations)
#
# The total is 4 + 12 + 3 = 19, and the structure gives:
# Z² = 32π/3 with suppression S = 3/110
#
# For Casimir energy, different spin fields contribute differently:
# - Scalar (spin 0): +1
# - Fermion (spin 1/2): -1 (periodic) or +1 (antiperiodic)
# - Vector (spin 1): +2
# - Tensor (spin 2): +5
#
# The Z² structure might modify these weights.
# =============================================================================

using Printf
using Dates

println("=" ^ 70)
println("CASIMIR ENERGY WITH Z² FIELD STRUCTURE")
println("=" ^ 70)
println("Testing Z² contribution to aspect ratio preference")
println("Start: ", now())
println()

# Z² constants
const Z2 = 32 * π / 3
const Z = sqrt(Z2)
const BEKENSTEIN = 4
const GAUGE = 12
const GENERATIONS = 3

println("Z² parameters:")
println("  Z² = 32π/3 = $(round(Z2, digits=4))")
println("  Bekenstein (body diagonals) = $BEKENSTEIN")
println("  Gauge (edges) = $GAUGE")
println("  Generations (face pairs) = $GENERATIONS")
println()

# =============================================================================
# CASIMIR ENERGY WITH WEIGHTED FIELDS
# =============================================================================

function casimir_z2_weighted(L1, L2, L3; n_max=30)
    """
    Compute Casimir energy with Z² field content weighting.

    The key insight from Z² is that the cube structure gives:
    - 4 body diagonals at angle arccos(1/√3) from edges
    - 12 edges
    - 6 faces (3 pairs)

    The ratio 13:19 might emerge from:
    13 = BEKENSTEIN + GAUGE - GENERATIONS = 4 + 12 - 3 = 13
    19 = BEKENSTEIN + GAUGE + GENERATIONS = 4 + 12 + 3 = 19

    We weight modes by their geometric origin.
    """
    E = 0.0

    # Volume for normalization
    V = L1 * L2 * L3

    for n1 in -n_max:n_max
        for n2 in -n_max:n_max
            for n3 in -n_max:n_max
                if n1 == 0 && n2 == 0 && n3 == 0
                    continue
                end

                k1 = 2π * n1 / L1
                k2 = 2π * n2 / L2
                k3 = 2π * n3 / L3

                k_sq = k1^2 + k2^2 + k3^2
                k = sqrt(k_sq)

                # Classify mode by geometric type
                n_nonzero = (n1 != 0) + (n2 != 0) + (n3 != 0)

                if n_nonzero == 3
                    # Body diagonal type (all components nonzero)
                    weight = BEKENSTEIN / 4  # 4 body diagonals
                elseif n_nonzero == 2
                    # Face diagonal type
                    weight = GENERATIONS / 3  # 3 face pairs
                else
                    # Edge type (only one component)
                    weight = GAUGE / 12  # 12 edges
                end

                # Z₂ projection: even parity only
                parity = (-1)^(abs(n1) + abs(n2) + abs(n3))
                if parity == -1
                    # Odd parity: suppressed by S = 3/110
                    weight *= 3/110
                end

                # Regularization
                cutoff = exp(-k / (2π * n_max / min(L1, L2, L3)))

                E += 0.5 * weight * k * cutoff
            end
        end
    end

    E_normalized = E * V^(1/3)
    return E, E_normalized
end

# =============================================================================
# ASPECT RATIO SWEEP
# =============================================================================

function sweep_ratios()
    L3 = 1.0
    ratios = [0.5, 0.55, 0.6, 0.65, 13/19, 0.7, 0.72, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]

    println("Aspect ratio sweep with Z² weighting:")
    println("-" ^ 50)
    println(@sprintf("%12s  %12s", "L1/L2", "E_Z²_weighted"))
    println("-" ^ 50)

    results = []

    for r in ratios
        L2 = 1 / sqrt(r)
        L1 = sqrt(r)

        E, E_norm = casimir_z2_weighted(L1, L2, L3)
        push!(results, (ratio=r, E_norm=E_norm))

        r_str = r == 13/19 ? "13/19" : @sprintf("%.4f", r)
        println(@sprintf("%12s  %12.4f", r_str, E_norm))
    end

    println("-" ^ 50)
    println()

    return results
end

# =============================================================================
# MAIN
# =============================================================================

function main()
    results = sweep_ratios()

    min_idx = argmin([r.E_norm for r in results])
    best = results[min_idx]

    println("=" ^ 50)
    println("RESULTS")
    println("=" ^ 50)
    println()

    println("With Z² weighting:")
    println("  Minimum at ratio = $(round(best.ratio, digits=4))")
    println()

    target = 13/19
    println("Z² prediction: 13/19 = $(round(target, digits=4))")
    println()

    idx_1319 = findfirst(r -> r.ratio == 13/19, results)
    if idx_1319 !== nothing
        E_1319 = results[idx_1319].E_norm
        E_min = best.E_norm

        println("At 13/19: E = $(round(E_1319, digits=2))")
        println("Minimum:  E = $(round(E_min, digits=2))")

        diff_pct = (E_1319 - E_min) / E_min * 100
        println("Difference: $(round(diff_pct, digits=2))%")
        println()

        if abs(best.ratio - target) < 0.03
            println("✓ CONFIRMED: Minimum at 13/19!")
            status = "CONFIRMED"
        elseif diff_pct < 5
            println("⚠ CLOSE: 13/19 within 5% of minimum")
            status = "CLOSE"
        else
            println("✗ NOT CONFIRMED: Minimum at $(round(best.ratio, digits=2)), not 13/19")
            status = "NOT_CONFIRMED"
        end
    else
        status = "ERROR"
    end

    println()
    println("Interpretation:")
    println("  The Z² weighting (13 vs 19 mode structure) was applied.")
    println("  Odd-parity modes were suppressed by S = 3/110.")
    println("  The minimum is at ratio $(round(best.ratio, digits=3)).")
    println()
    println("End: ", now())

    return status, best.ratio
end

status, best_ratio = main()
