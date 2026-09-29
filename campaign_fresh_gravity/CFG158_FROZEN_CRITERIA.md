# CFG158 — Referee of CFG118 (Door 6): does secondary infall put too much cold mass inside r_M and too little outside? FROZEN CRITERIA

Written 2026-09-29, before any script or number of this lane. It re-derives ONE headline of CFG118 with its own code, from CFG118's frozen criteria and README only (the CFG84–86 / CFG155 way), and says where independence stops. The menu of ten doors (closure_map/TEN_DOORS_GATES_2026-09-29.md) was written knowing the target. The referee is NOT blind: CFG118's README states its numbers. Those numbers are TARGETS I read, not blind predictions. Where a hand estimate below matches a README number, the estimate was made after reading it; the probabilities are my honest belief that my own independent code lands on the number, not evidence that I derived it first. In phase 1 no CFG118 script, .c, .out or .json file was opened; nothing here is committed by the writing agent.

## The headline under test (pinned from the CFG118 README)

For a static baryon core in a Planck18 background, cold shells that start on the Hubble flow at z = 100 and fall in with shell crossing give, on the canonical footing (a₀ = 9.3603e-11 m/s²):
- **H-A (cumulative mass, x ≈ 1).** M_c(<r)/M_c,target(<r) = 1.0–4.2 at x = r/r_M ≈ 1 (README bin x ≈ 1.12).
- **H-B (cumulative mass, x ≈ 28).** The same ratio is 0.28–0.66 at x ≈ 28 (README bin x ≈ 28.2).
- **H-C (falls with radius).** So C_infall/C_target falls with radius, where C(r) = ρ_c r³ g_tot and the target is C = (a₀/4π) M_b(<r). This is stable to resolution (README: median 2% between 5,000 and 20,000 shells at x ≈ 28).
- **H-D (radial scale, R2).** The radius where M_c(<r) = M_b scales as M_b^0.32–0.35 for point cores (x from 1.5–1.9 at 1e9 to 0.54–0.57 at 1e12; exponential spheres 0.22–0.24), following the turnaround radius (M^0.333), not r_M ∝ M^(1/2).
- **Set-up numbers (README).** z = 0 turnaround mass 23.6 M_b for point cores (19.7–23.6 for the exponential spheres); r_ta(z = 0) = 236, 508, 1095, 2358 kpc for M_b = 1e9, 1e10, 1e11, 1e12 M☉, i.e. x_ta = 193, 132, 90, 61.
- **Controls to re-derive (README).** EdS control: least-squares log-slope −2.238 against −9/4 over r/r_ta in [0.03, 0.15]. Hubble-flow check: with no core every shell stays on the Planck18 Hubble flow to ~1e-6 (README 4.3e-7 in position).

Not re-derived: the local binned C ratios at x ≲ 1 (README calls them noisy), the exact ±10% G1 verdict, the alt-footing tables, the bootstrap errors. Local-ratio curves are computed and REPORTED only.

## What is shared and what is independent

- **Shared inputs (read from the frozen file/README, not re-derived):**
  - Planck18 flat H₀ = 67.4, Ω_m = 0.315, Ω_Λ = 0.685, Ω_c = 0.2655 (Ω_b/Ω_m = 0.157), matter + Λ only (no radiation), z_i = 100.
  - Target definition (CFG44): point mass ρ_c = a₀/(4πG r√(1+x²)), M_c = M_b(√(1+x²) − 1), g_tot = √(g_N² + a₀g_N); exponential sphere ρ_b = M/(8πh³) e^(−r/h), M_b(<r) = M[1 − (1+s+s²/2)e^(−s)] (Bcommon docstring), with the target from ρ_c = a₀ M_b(<r)/(4π r³ g_tot), w′ = a₀ r u_N/u, u = u_N + w (CFG44/CFG155 statement).
  - r_M = √(GM_b/a₀); G = 4.30091727e-6 kpc (km/s)²/M☉; canonical a₀ = 2888.3 (km/s)²/kpc.
  - The README's disclosed readings: static core from z_i; smooth uniform baryon background (Ω_b outside the core) on the Hubble flow; point-mass softening 1e-3 r_M (Plummer, my choice of form); j set at first turnaround by the energy/pericentre relation in the enclosed-mass potential (j² = 2[Φ(r_ta) − Φ(q r_ta)]/((q r_ta)⁻² − r_ta⁻²)); brackets q = 0.05, 0.1, 0.2; time-averaging over one local dynamical time (Binney & Tremaine t_dyn = √(3π/(16 G ρ̄)), capped 0.9 of the run).
  - **Assumption of mine:** exponential h = 2, 3, 4, 5 kpc pair with M_b = 1e9, 1e10, 1e11, 1e12 in ascending order (the frozen text lists four h and four masses without saying).
- **My own reading of the ambiguous extent rule:** the outermost shell is the one whose single-shell z = 0 physical radius equals 3 r_ta (r_ta = the z = 0 zero-velocity radius). The README's "77.8 M_b" agrees with a rough hand check; a sensitivity run with the extent doubled is a reported row.
- **Independent (mine):**
  - Code and language: Julia kernel, Python driver (CFG118 is C + Python).
  - Integrator: not a block-step KDK leapfrog with per-kick sorting. Each shell is a test body integrated by an adaptive embedded Runge–Kutta (Dormand–Prince 5(4), rtol ~1e-10) in a potential whose enclosed cold mass M_c(<r, t) is rebuilt from the sorted shell positions every Δt_s = 1 Myr and interpolated linearly in time inside the interval by a predictor–corrector (predict with the profile frozen at t_n, correct with the linear interpolation between t_n and the predicted t_{n+1}).
  - A shell's own mass counts half (the profile node sits at (k − ½)m).
  - Shell placement: mass midpoints M_i = (i − ½) m at the cosmic cold density; the z = 0 turnaround mass and r_ta by root-finding on a single-shell ODE (scipy) separate from the kernel.
  - Cumulative-mass extraction, binning and averaging code; the EdS control set-up; the analytic Friedmann a(t) by quadrature.
- **Independence stops at:** the frozen cosmology and set-up, the target definition, the README's readings above, the j formula, and Newtonian gravity. The referee is not blind. Where CFG118's C code and mine share a wrong reading (for example the smooth-baryon background or the j formula), the referee cannot see it; the reading sensitivity rows (M3 below, the extent doubling, a point-mass-form j row) are the only probes.

## My own hand ESTIMATES (labelled estimates, made after reading the README)

Derivation of each is short; none is a prediction I would defend blind.
- **E1. M_ta.** The cold shell equation with a static core, δ_c″ + 2Hδ_c′ = 4πGρ_c(δ_c + M_b/M_c), growth exponent p = (−1 + √(1 + 24 Ω_c/Ω_m))/4 = 0.902, initial δ_c = δ_c′ = 0 gives a growing share −q/(p − q) = 0.609 with q = −1.40. At a = 1 (matter-era form ×~0.8 for Λ): δ_lin ≈ 30 M_b/M_c. Turnaround at δ_lin ≈ 1.06 gives M_ta ≈ 28 M_b (plausible range 20–35). **P(code within 15% of 23.6) = 55%.**
- **E2. r_ta.** The README's 236 kpc for 23.6e9 M☉ means ρ_ta/ρ̄_c ≈ 12.8, the usual ΛCDM z = 0 turnaround contrast (~12–13). **P(each r_ta within 5% of the README) = 70%.** M_ta/M_b independent of M_b: r_ta ∝ M_b^0.333. **P(exponent within ±0.01) = 97%.**
- **E3. r_M and x_ta.** r_M = 1.22, 3.86, 12.2, 38.6 kpc (hand-computed) → x_ta = 193, 132, 90, 61 if r_ta reproduces. **P(all four within 6%) = 65%.**
- **E4. x ≈ 28 cumulative ratio.** With ρ ∝ r^(−9/4) (M ∝ r^0.75) and the first apocentre at ~0.35 r_ta, M_c(<r) is 0.3–0.8 M_ta at x = 28 (r/r_ta from 0.14 at 1e9 to 0.46 at 1e12), i.e. 7–19 M_b against the target 27 M_b. Estimated ratio 0.25–0.75. **P(both README ends 0.28 and 0.66 within 15% for the point-core envelope) = 40%; P(each end within a factor 1.3) = 70%.**
- **E5. x ≈ 1 cumulative ratio.** The same M ∝ r^0.75 gives ≈1.1 at 1e9 rising to ≈2.7 at 1e12 (∝ M^0.125). The README's 4.2 is above that, so either the profile normalisation or the exponential spheres set the top. **P(both ends within 15% of 1.0 and 4.2 over the point+exponential envelope) = 30%; P(qualitative: every ratio > 1 and larger at higher mass) = 80%.**
- **E6. Falls with radius (H-C).** **P = 97%** (needs only that the two ratios straddle 1).
- **E7. R2 radial scale.** With x₁ ∝ M^(−1/6) (self-similar), the M_c = M_b radius scales as M^(1/3). **P(each q gives an exponent within 0.03 of the README's 0.32–0.35, i.e. in [0.29, 0.38]) = 70%.** Exponential spheres (0.22–0.24): no estimate; **P = 35%.**
- **E8. EdS slope.** Theory −2.25 (Bertschinger). **P(within 0.05 of README −2.238 with my estimator) = 50%; P(within 0.15 of −9/4) = 80%.** The README's local slopes (−2.10 to −2.96) show the estimator matters.
- **E9. Hubble flow.** **P(≤ 1e-6 relative) = 90%.**
- **E10. Verdict.** If E4 and E5 hold the target's flat ratio 1 is excluded at every mass. **P(my code reproduces the sign of the deviation: too much inside, too little outside) = 92%.**

## Checks and exact pass lines

Measurement definitions (all frozen here):
- R(x) = M_c,sim(<r)/M_c,target(<r) at r = x r_M, x = 1.12 and 28.2 (the README's bin centres, 10^0.05 and 10^1.45). M_c,sim is the cold mass inside r at z = 0, averaged over the local dynamical-time window (README convention, sampled every 10 Myr from stored profiles). The snapshot value at z = 0 is reported too. Canonical footing is the pass footing; alt footing is reported.
- The envelope over a set of runs is [min R, max R]. "Within 15%" of a README number N means [0.85 N, 1.15 N].
- Point-mass and exponential runs each: 4 masses × 3 brackets q = 0.05, 0.1, 0.2 (24 runs), N_s = 20,000 shells and again at N_s = 5,000 (48 sims).

**Headline lines (all must pass for the main run to exit 0):**
- **H-A** the envelope of R(1.12) over all 24 runs has min in [0.85, 1.15] and max in [3.57, 4.83]. The point-mass-only envelope is reported beside it.
- **H-B** the envelope of R(28.2) over all 24 runs has min in [0.238, 0.322] and max in [0.561, 0.759].
- **H-C** R(28.2) < R(1.12) in every one of the 24 runs, and the ratio R at x = 0.3, 1.12, 3, 10, 28.2 (all reported) is non-increasing beyond x = 1.12 for the median run.
- **H-D** point-mass runs: exponent n of r₁ (radius where M_c = M_b, log-log fit over the 4 masses) is in [0.29, 0.38] for each q, all n < 0.45, and the z = 0 turnaround exponent is in [0.323, 0.343]. Exponential runs: n reported against 0.22–0.24 (line ±0.05: [0.17, 0.29]).
- **H-E** M_ta/M_b within 15% of 23.6 for point cores (≥ 20.1 and ≤ 27.1, all 4 masses) and within 15% of the README's 19.7–23.6 range for the exponential spheres (min ≥ 16.7, max ≤ 27.1); r_ta(z = 0) within 5% of 236, 508, 1095, 2358 kpc for the point cores; x_ta within 6% of 193, 132, 90, 61.
- **H-F** (G1 verdict) for every run, |C_infall/C_target − 1| exceeds 0.10 somewhere in x ∈ [0.1, 30] (G1 fails); reported per mass and geometry, with the largest deviation and the x range inside ±10%.

**Controls (each must pass):**
- **C1 Hubble flow.** No core: every shell's position and velocity at z = 0 agree with the analytic Planck18 Hubble flow (a(t) by quadrature) to 1e-6 relative.
- **C2 EdS.** Einstein–de Sitter background, Λ = 0, no smooth-baryon background (all shells at Ω_m = 1, a single collisionless species), point seed, q = 0.05, z_i = 100, 20,000 shells, snapshot at a = 1, 0.1-dex log bins, least-squares log-slope of ρ over r/r_ta ∈ [0.03, 0.15]. Pass: |slope + 2.25| ≤ 0.15 (frozen CFG118 line) AND, as the agreement line with the README, |slope + 2.238| ≤ 0.05. Also reported: M_ta/M_seed at a = 1 against my hand value 57 (linear (3/5)(a/a_i)/1.062, P(within 5%) = 80%).
- **C3 Resolution (two shell counts).** Between N_s = 5,000 and 20,000: cumulative R(28.2) agrees to ≤ 10% in every run, and R(1.12) to ≤ 25% in every run (README: 2% median at x ≈ 28 and 12% median, 25% largest, over x in [1, 30]). And H-A/H-B/H-C evaluated on the 5,000-shell runs must give the same verdicts (reported). **P(pass both lines) = 65%.**
- **C4 Time-step convergence.** (1e10, point core, q = 0.1, N_s = 5,000): Δt_s = 0.5 Myr and rtol 1e-11 changes R(1.12) and R(28.2) by ≤ 3%.
- **C5 Single-shell tie.** In the main run the z = 0 zero-velocity radius of the shells not yet crossed matches the single-shell (scipy) r_ta to 1%.
- **C6 Static orbit.** A test body in the static softened 1e10 point core with turnaround at 0.7 kpc: realised pericentre/r_ta = q to 2% (q = 0.05, 0.1, 0.2) and energy drift ≤ 1e-3 over ~2,000 orbits (README's own drift: 0.06–0.43%; not a pass line for them).
- **C7 Target identities.** Point-mass M_c,target = M_b(√(1+x²) − 1) and C = (a₀/4π)M_b to 1e-10; the exponential-sphere target (ODE) satisfies Poisson ((1/r²)d(r²g_tot)/dr = 4πGρ_c) to 1e-6 and C = (a₀/4π) M_b(<r) to 1e-8.
- **C8 Evaluator control.** The evaluator applied to the target's own M_c gives R = 1 at both radii, and it FAILS H-A (min/max not in the README's ranges) and H-C (the ratio does not fall). This shows the pass lines are not satisfied by the target.

**Reported rows (no pass line):**
- R1 local C_infall/C_target on 0.1-dex bins x = 0.1–31.6, both footings, with the largest deviation and the ±10% range per curve.
- R2 the snapshot R values; the ratio at x = 0.3, 3, 10; the alt-footing analogues.
- R3 extent sensitivity (outer shell at 6 r_ta instead of 3), and a point-mass-form j row (j² = 2GM(<r_ta) r_ta q/(1+q)) on the 1e10 point core.
- R4 the fraction of runs where the realised first pericentre is < 0.9 of the bracket.

## MUTATE controls (each flips a load-bearing cell)

MUTATE=1 re-runs the cells below with the same code and criteria, scoped to (1e10 M☉, point core, q = 0.1, N_s = 5,000) unless stated. Bite = the mutated run fails the named line.
- **M1 drop the baryon core.** No perturbation, so the shells stay on the Hubble flow. R(1.12) ≈ (4π/3)ρ̄_c r³/(0.414 M_b) ≈ 1e-6. **Must bite:** H-A fails (R(1.12) < 0.85) and H-E fails (no finite M_ta). P(bite) = 99%.
- **M2 near-radial infall, q = 0.002 (j → 0).** Exactly j = 0 needs ~1e7 crossings per shell of the softened core and is infeasible; q = 0.002 puts the first pericentre at 0.12–0.39 r_M (x_p = 0.002 x_ta). Expected to raise the inner mass because shells spend time at small radius. Declared line: R_mut(1.12) ≥ 1.3 × R(1.12) of the same-mass q = 0.05 run. **Informative, not required to bite** (P(bite) = 60%); reported either way.
- **M3 no smooth baryon background (shells carry all of Ω_m = 0.315, i.e. clustering baryons).** The growth exponent becomes 1 and M_ta rises (my estimate 40–55 M_b). **Must bite:** M_ta/M_b > 27.1 (H-E fails). P(bite) = 85%.
- **M4 replace the Hubble-flow initial condition by v_i = 0.9 H_i r (sub-Hubble).** No-core C1 fails at > 1e-2, and with a core every shell turns around and collapses (no finite M_ta). **Must bite:** C1 fails at > 1e-2. P(bite) = 99%.
- **M5 evaluator on the target's own M_c** (this is C8 restated as a control on the evaluator).

MUTATE exits 1 iff M1, M3 and M4 each bite (M2 is a declared, informative row). If M2 or M3 fails to bite it is kept and disclosed, not repaired.

## Resolution and convergence

- Two shell counts: N_s = 5,000 and 20,000 for all 24 (mass, geometry, q) cases (C3).
- One integrator/time-step doubling (C4), plus the extent doubling (R3).
- No cap on the local-averaging window other than the README's 0.9 of the run.

## What counts as disagreement (a valid, kept result)

- **Numerical disagreement:** any of H-A, H-B, H-D, H-E outside its line while the qualitative direction holds (E10). That would be reported as "qualitatively reproduced, numbers off by X"; the CFG118 README would need its ranges corrected.
- **Qualitative disagreement:** R(1.12) < 1 at some mass, or R(28.2) ≥ 1, or the ratio does not fall with radius, or the radial scale follows M^(1/2) (n > 0.45). That contradicts CFG118's bottom line and would be its own finding.
- **Control disagreement:** C1 above 1e-6, C2 slope off, C3 fails at both shell counts, or C6 fails, means my own integrator is at fault and the run cannot be read for a verdict; that is reported as such.
- Either way CFG118's G1 no-go concerns only its declared set-up (spherical, static core from z = 100, smooth baryon background, three q brackets). Non-spherical collapse, mergers, a growing core, feedback, and warm or self-interacting dark matter are untested. A reproduced FAIL is a scoped no-go, not a statement about the theory. κ = ½ and Ω_c h² stay fitted; nothing here says the data favour either model or that the theory is closed.

## Script plan

Directory (phase 2, by the orchestrator's commit): campaign_fresh_gravity/CFG158_door6_infall_referee/.
- `cfg158_shells.jl`: the Julia kernel. Reads a spec (JSON: mass, geometry, q, N_s, Δt_s, mutate flags), writes cumulative mass histories at probe radii and the binned profiles (binary/JSON). No physics constants beyond the frozen ones.
- `cfg158_referee.py`: the driver. Builds the cosmology and single-shell root-finding (scipy), the targets (C7), launches the Julia runs in parallel (`CFG158_NPROC`, default 8), caches products in `cfg158_sims.json` keyed by a spec hash, evaluates H-A to H-F, C1–C8, R1–R4. Prints only relative or bare file names, never an absolute home path.
- Outputs: `cfg158_referee.out`, `cfg158_referee_results.json`; with MUTATE=1 the driver reuses the cached main products where a cell is unchanged and runs only the M1–M4 sims: `cfg158_referee_MUTATE.out`, `cfg158_referee_MUTATE_results.json`.
- Exit convention: main exits 0 only if every headline line and every control passes; any failure is kept and exits 1. MUTATE exits 1 when M1, M3 and M4 each bite (the controls bite).
- After my own main and MUTATE runs are saved and only then: `cfg158_posthoc_compare.py` opens CFG118's outputs and tabulates each README number I re-derived against mine (R5), tolerance 5% on M_c ratios where conventions align.
- Runtime target: about 20 min wall per run on 8 processes (the machine is shared and loaded; the budget is a target, not a criterion). The frozen scope is not reduced after a result is seen.
- Files failing to compile or run are reported; a first run that fails a control is kept as `_firstrun` beside the rerun.
