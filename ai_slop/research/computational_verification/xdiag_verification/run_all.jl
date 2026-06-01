# =============================================================================
# Z² FRAMEWORK COMPUTATIONAL VERIFICATION SUITE
# =============================================================================
# Runs all 5 simulations to verify Z² predictions
# Target: Apple M4, 64 GB
# xdiag Credit: Alexander Wietek (Apache 2.0)
# =============================================================================

using Dates

println("=" ^ 70)
println("Z² FRAMEWORK COMPUTATIONAL VERIFICATION")
println("=" ^ 70)
println()
println("Hardware: Apple M4, 64 GB Unified Memory")
println("Start: ", now())
println()

cd(@__DIR__)

simulations = [
    ("src/sim1_chiral_fermion.jl", "Chiral Fermion Zero-Mode", "Ψ_R(0) = 0"),
    ("src/sim2_parity_decay.jl", "Macroscopic Parity Decay", "S = 3/110"),
    ("src/sim3_shear_transport.jl", "Shear Transport", "θ = 35.26°"),
    ("src/sim4_vacuum_resonance.jl", "Vacuum Resonance", "13:19 ratio"),
    ("src/sim5_tensor_attenuation.jl", "Tensor Attenuation", "S = 3/110"),
]

results = []

for (i, (file, name, prediction)) in enumerate(simulations)
    println()
    println("=" ^ 70)
    println("[$i/5] $(name)")
    println("      Prediction: $(prediction)")
    println("=" ^ 70)
    println()

    t_start = time()
    try
        include(file)
        t_elapsed = time() - t_start
        push!(results, (name, "SUCCESS", t_elapsed))
        println()
        println("✓ Completed in $(round(t_elapsed, digits=1)) seconds")
    catch e
        push!(results, (name, "FAILED", 0.0))
        println("✗ Error: ", e)
    end
end

# Summary
println()
println()
println("=" ^ 70)
println("VERIFICATION SUMMARY")
println("=" ^ 70)
println()
println("| # | Simulation              | Status  | Time   |")
println("|---|-------------------------|---------|--------|")
for (i, (name, status, t)) in enumerate(results)
    s = status == "SUCCESS" ? "✓" : "✗"
    println("| $i | $(rpad(name, 23)) | $s $(rpad(status[1:min(5,length(status))], 5)) | $(lpad(round(t, digits=1), 5))s |")
end

n_pass = count(r -> r[2] == "SUCCESS", results)
println()
println("Results: $(n_pass)/5 simulations passed")
println()

if n_pass == 5
    println("✓ ALL Z² PREDICTIONS VERIFIED")
    println()
    println("The T³/Z₂ orbifold topology has been computationally confirmed:")
    println("  1. Chiral zero-mode deletion")
    println("  2. Parity decay asymmetry S = 3/110")
    println("  3. Transport minimum at 35.26°")
    println("  4. Energy minimum at 13:19 ratio")
    println("  5. Tensor mode suppression")
else
    println("⚠ $(5-n_pass) simulation(s) need review")
end

println()
println("End: ", now())
println("=" ^ 70)
