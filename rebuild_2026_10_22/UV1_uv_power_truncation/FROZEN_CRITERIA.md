# UV1_uv_power_truncation: FROZEN CRITERIA (committed alone, before any zoom or number from this test)

**Question.** Argon's claim, relayed 10-31. X48's grid is scaled to the halo, so its initial conditions stop at k_Nyq(M) = π ng/(4 q_M), which falls as M^(−1/3). So each mass runs a different truncated P(k). It says this makes a fake cold radial spike at 10¹⁴ (r₋₂ c_f 10.07), and that adding the velocity dispersion of the missing native modes brings c_f(10¹⁴) down to 4.5–5.5 and leaves 10¹² near 7.5. The truncation is real, and it's worth a direct test, since ZN1's result rests on these zooms.

**Disclosed, computed before this lane (`../ARGON_REPLY_2026-10-31/argon_check2.out`).**
- k_Nyq at ng 64 is 161.6, 34.8, 16.2, 7.50 per Mpc at 10¹⁰, 10¹², 10¹³, 10¹⁴, about 3.7 × Argon's h/Mpc values.
- The missing band's linear velocity rms, up to k_Nyq(10¹⁰), is 2.7 km/s at z_i and 12.3 km/s at z_f for 10¹⁴, where V_vir is 531: **ratio 0.023, at every mass.** Argon's text says 0.11 to 0.24. On its own formula that gives (0.023)² of r_f, far below r₀. So I expect the kick to do nothing.
- Like for like, concentration falls with mass at ng 64: NFW fit 7.75, 7.15, 6.80; η_conv 25.94, 23.54, 22.10; ZN1's c₂₀₀ at z = 0 7.68, 6.47, 5.94. Only r₋₂ rises (7.74, 8.67, 10.07), with 68 % ranges above 25 %, and X77 already flagged it as an estimator artefact. So I don't expect a spike to remove.
- A velocity kick isn't the same as the missing modes. Those modes would collapse into bound clumps, and their internal motions don't act as a pressure on the cluster's orbits. So a second test measures what power on these scales does: cut it, same phases, and see how much the shape moves.

**Standing.** κ = ½ FITTED. Cold dark energy, never a particle. No ΛCDM input. Not "theory closed". Nothing here says the data favour the framework. No downloads.

## Runs (10¹⁴, ng 64, seeds 1–9, same seeds as X48's A4 and ZN1, to z_f and on to z = 0)
- **Kick (Argon's test):** at z_i, each particle gets an isotropic Gaussian velocity, per axis σ_v/√3, where σ_v is the band's rms at z_i from native P(k): a_i H_i f_i D_i √(∫ dk P/(2π²)), band k_Nyq(10¹⁴) to k_Nyq(10¹⁰). Nothing else changes.
- **Cut:** P(k) = 0 above k_Nyq(10¹⁴)/2, same random numbers, so identical phases below the cut.
- X48's zoom and ZN1's continuation with ZK1's kernel, unchanged. Single thread, nice 15, preemptible. Fewer than 6 finished pairs: UNDECIDED.

## Read-outs, same-seed pairs against X48's and ZN1's runs, median over seeds
At z_f: r₋₂ c_f (X48's), NFW-fit c, η_S (X77). At z = 0: c₂₀₀, M₂₀₀, and m(x) at x = 0.05, 0.1, 0.2, 0.5, 1, 1.5, 2.

## Verdict
**Kick, against Argon's line:**
- **ARGON'S SPIKE CONFIRMED:** median r₋₂ c_f at z_f lands in 4.5–5.5.
- **NO EFFECT:** median paired |Δ ln| at or below 0.05 on both NFW-fit c and η_S.
- **PARTIAL:** otherwise, with sign and size.

**Cut, on the zooms' UV dependence:**
- **UV-SENSITIVE:** median paired |Δ ln m(x)| above 0.10 at x = 0.1 or 0.2 at z = 0, the radii where X-COP misses. Sign stated.
- **UV-INSENSITIVE:** otherwise.

If UV-SENSITIVE, ZN1's shape isn't converged in power, and its classes get that caveat.

## Reported, not graded
1. The same read-outs at z = 0.25.
2. ZN1's grade with the 10¹⁴ tag replaced by each variant's stack, X-COP and keys.

## Checks
- **K1:** with neither change, the wrapper's ICs equal X48's for a seed: |d| 0.
- **K2:** the cut's modes below k_cut equal the full run's to 1e-12 after the constraint; the constraint values match to 1e-9.
- **K3:** the kick's sample σ per axis within 1 % of σ_v/√3.
- ZK1's K3 stands for the kernel.
- Any K failure: no verdict, exit 1.
