# X35_a0_tracks_ede — AMENDMENT A1 (POST-FIRST-RUN, before any finding is graded)

The first run of `x35_ede_tracking.py` fired the Step 0 stop rule (S0-1, S0-4) and failed K1 and K6. Each failure was traced
to a mechanism in this lane's own code before any change; none is a threshold, a literature value or an analysis line.
The first-run output is not kept as a result (it was produced by the bug in A1.1, which made every Ψ, hence every x,
wrong by up to ~10⁴).

**A1.1 Potential evolution (K6, S0-1).** The script evolved φ with the 0i Einstein equation,
φ′ = −ℋφ + 4πGa²Σ(ρ+P)θ/k². Super-horizon this is a near-exact cancellation between −ℋφ and the velocity term, and the
numerical error grows: K6 (Ψ at k = 0.001 Mpc⁻¹ divided by its initial value, frozen window [0.80, 1.0]) returned 7463.
Replaced by the 00 equation, φ′ = −ℋφ − [k²φ + (3/2)ℋ²Σ Ω_i δ_i]/(3ℋ) (Ma & Bertschinger 1995 Eq. 23a), the standard stable
choice. Equations, ICs and the estimator are otherwise unchanged.

**A1.2 Drag redshift (S0-4).** The Eisenstein–Hu 1998 z_d fitting formula (ASSUMPTION A11) gives 1020.7 for the ruler
cosmology. That formula's z_d is known to sit ~40 below the drag epoch defined by optical depth unity (≈ 1060); EH98
calibrate their own r_s formula with it. Used inside a direct sound-horizon integral it overestimates r_d (150.7 Mpc).
Now z_d = z_d,EH98(ω_b, ω_m) × 1059.94 / z_d,EH98(0.02236, 0.1426), anchoring the scale to the Planck 2018 drag redshift
1059.94 (LITERATURE, PROVISIONAL) and keeping EH98's dependence on ω_b and ω_m. This is not fitted to r_d; S0-4's 1 % line
against CFG689's 147.07 Mpc is unchanged. EDE is taken not to move z_d (APPROXIMATION, stated in the README).

**A1.3 K1 sign in code (K1).** FROZEN_CRITERIA §2 D1 states the identity with a plus sign,
∫Ξ·[∇·(J_Y∇Ξ) + μ_K²Ξ] = +∫[|∇Ξ|²/(1+x) + μ_K²Ξ²]; the code tested the opposite sign (lhs + rhs). The code now tests the
frozen identity (|lhs − rhs|/rhs < 1e-8).

Nothing else changes: literature points, models, k ranges, thresholds, verdict rules and MUTATE checks are as frozen.
