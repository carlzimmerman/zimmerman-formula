# CQ6_past_first_caustic: NOT EVALUABLE

**The regulated dust does not fold at the caustic time, but no run gets through the first bounce with energy held. So
"settles" cannot be graded.**

κ = ½ FITTED; not theory closed. Criteria `FROZEN_CRITERIA.md` (8131404df6, committed alone first). Scripts 63eb2356dc.
- Not blind. No amendments; the frozen label stands.
- a0 does not enter, so both footings give the same numbers and nothing is pooled.
- No particle. The cold sector stays retired and nothing here revives it.
- No data are used. Nothing here says the data favour the framework.
- Adopts nothing.

## Plain statement

**The setup.** This is v3s's P(X) dust limit with AZ14's quartic regulator, F = λ∫|ρ'|⁴/ρ³ with λ = 1e-8 FITTED. The
collapse is planar 1D, starting from a sinusoid whose unregulated Zel'dovich caustic falls at t_c = 3 τ.

**What passes.** On every grid the regulated run passes t_c without a crossing.
- The central density is held at 5.56 / 5.60 / 5.60 ρ̄ (N 256 / 512 / 1024), converged to 0.7 %.
- The unregulated twin reaches 4.0e4 / 1.7e5 / 7.6e5 at its crossing.

**What fails.** Every regulated run then hits the frozen BLOW-UP. Newton fails at 64 substeps during the first bounce,
at t = 3.216 / 3.195 / 3.095. Before that, the energy error passes the 1e-3 K_max line (t ≈ 3.0–3.1).

**Why the label is NOT EVALUABLE.** K-dt fails: dt 5e-4 also blows up, at 3.1825 with energy error 4.8e-2. Section 6
puts a failed control first, so the label is NOT EVALUABLE. Had the controls passed, the blow-up on all grids would have
read ILL-POSED.

**What it means for row 12.** Row 12 ("past the first caustic no") is unchanged. It is not closed in either direction.

## Controls

| Check | Result | Line | Pass? |
|---|---|---|---|
| K-ZEL (λ = 0) | first crossing at t = 3.000025 / 3.0000061 / 3.0000013 (rel. 8.3e-6 / 2.0e-6 / 4.4e-7) | 1 % of t_c = 3 | pass |
| MUTATE (λ = 0) | crosses on all three grids, so it does not pass the caustic | must not pass | pass |
| K-FD | 2.8e-16 | 1e-8 | pass |
| K-hom | scaling 0; virial identity 5.1e-15 | 1e-12 / 1e-10 | pass |
| **K-dt** (N 512, dt 5e-4) | BLOW-UP at t = 3.1825, energy error 4.8e-2 K_max, no W5 quantities | same (a), (b) passes, (e) within 5 % | **FAIL** |

## Caustic passage, conservation and profile, per grid (`cq6_results.json`)

| Run | t_c passed without crossing? | Ends | Energy max\|ΔE\|/K_max (first > 1e-3 at) | Momentum | ρ_c at t_c | ρ_c peak (t) |
|---|---|---|---|---|---|---|
| N 256 | yes | BLOW-UP t = 3.216 | 2.4e-1 (t 3.10) | < 1e-10 | 5.561 | 6.43 (3.10) |
| N 512 | yes | BLOW-UP t = 3.195 | 1.25e-2 (t 3.10) | < 1e-10 | 5.596 | 6.54 (3.15) |
| N 1024 | yes | BLOW-UP t = 3.095 | 2.6e-2 (t 3.00) | < 1e-10 | 5.600 | 5.95 (3.05) |
| K-dt 512 | yes | BLOW-UP t = 3.1825 | 4.8e-2 (t 3.10) | < 1e-10 | 5.620 | 6.62 (3.15) |
| S1 λ 1e-9, N 512 | yes | BLOW-UP t = 3.110 | 5.9e-2 (t 3.05) | < 1e-10 | 7.809 | 8.91 (3.10) |
| S1 λ 1e-9, N 1024 | yes | BLOW-UP t = 3.029 | 8.0e-2 (t 3.00) | < 1e-10 | 7.794 | 7.79 (3.00) |

Line (a), the caustic passed through t_end = 65.83, fails on every grid. Line (b) fails on every grid. Lines (c), (d) and
(e) cannot be computed, because no run reaches the settling window (t ≥ 34.4).

- **Oscillates and settles, or runs away?** Neither is shown. No run gets more than about 0.2 τ past t_c. The failure
  comes earlier as N grows (3.216 → 3.195 → 3.095) and as λ falls (S1).
- **Final density profile.** There is none, because no run reaches W5. Below is the last profile that is converged across
  the ladder, at t = 3.0. It is given as enclosed-mass widths w_f (the full width holding mass fraction f; box L = 1).
  - **Regulated, t = 3.0.** ρ_c 5.56–5.60. w_0.25 0.0520, w_0.5 0.1679, w_0.75 0.5248, w_0.9 0.8016, identical on all
    grids to 1e-4. R_v ≈ 1.085 and F/K ≈ 0.19.
  - **Regulated, t = 3.1** (N 256 / 512). ρ_c 6.43 / 6.31, w_0.25 0.0458, w_0.5 0.1353. R_v ≈ 1.35, still rising, so the
    core is not in equilibrium.
  - **Unregulated at its crossing.** w_0.25 is 0.0249. The regulator holds the inner quarter of the mass about 2 times
    wider at t_c.

## Post-result diagnostic, no label weight (`cq6_explicit_diag.py`, `cq6_explicit_diag.out`)

This is an adaptive explicit velocity Verlet on the same discrete Lagrangian, with dt = 0.5/ω_max from the regulator's
dispersion. It was run to t = 3.5 at N 128 / 256 / 512.

**It gets through the bounce without a crossing**, so the frozen failure is at least partly the implicit integrator's.

**But it shows the solution losing convergence at the grid scale right after the bounce:**
- Energy error passes 1e-3 K_max by t ≈ 3.4–3.5 on every N: 1.9e-3 / 3.8e-3 / 3.3e-3 at t 3.5.
- The largest sheet acceleration grows with N:

  | t | N 128 | N 256 | N 512 |
  |---|---|---|---|
  | 3.3 | 1.2e3 | 2.8e3 | 5.9e3 |
  | 3.5 | 1.3e3 | 7.1e3 | 3.7e4 |

- The stable step collapses: at t 3.5 it is 6.3e-6, 2.7e-7 and 4.2e-8 τ.
- Core numbers agree across N to about 8 % up to t ≈ 3.2. They then separate: R_v at t 3.4 is 1.93 / 2.04 / 2.78.

**Reading, not a label.** The regulator stops the fold. It does not stop the infall from steepening into structure at
the grid scale during the bounce. That leans toward ILL-POSED (a gradient catastrophe the quartic term does not resolve,
since it vanishes where ρ' = 0). The frozen machinery cannot certify it.

## What would decide it

An energy-conserving integrator that resolves the regulator's k² dispersion, run past t ≈ 3.5 at N ≥ 512. Its test is
whether max|a| converges with N.
- At the explicit diagnostic's collapsing step (≈ 1e-6 to 4e-8 τ), reaching t_end = 65.8 is not feasible on the current
  queue.
- AZ16's nondegenerate add-on q0² |∇ρ|²/ρ would give the regulator a dispersion that does not vanish where ρ' = 0. AZ16
  notes it breaks AZ14's zero-linear-pressure gate. It is a pointer only, not adopted or run here.

## Caveats

- One λ (FITTED, set for resolvability, tied to no galaxy) and one amplitude. Planar 1D, static background with the
  background subtracted, so no expansion.
- The regulator is a nonrelativistic functional with no covariant realization. Even a pass would not complete v3s's
  action.
- **Bug fixed before the frozen runs.** The first smoke test (scratch output, not committed) had a wrong midpoint
  velocity update. The fixed script is the committed one. The smoke tests after the fix (N 256, dt 1e-3 / 2e-4 / 5e-5)
  already showed the failure at t ≈ 3.18–3.27. The frozen criteria were not changed.

## Files

| File | Contents |
|---|---|
| `FROZEN_CRITERIA.md` | the frozen criteria |
| `cq6.py` | the frozen script; run with `nice -n 10 python3 cq6.py all` |
| `cq6.out` | the run log |
| `cq6_results.json` | checks, analysis and label, the λ = 1e-8 runs, K-dt and S1 |
| `cq6_results_MUTATE.json` | the λ = 0 twin and K-ZEL |
| `runs/*.json`, `runs/*_series.npz` | per-run summaries and time series sampled every 0.05 τ |
| `cq6_explicit_diag.py`, `cq6_explicit_diag.out` | the post-result diagnostic |

Every run used one thread, `nice -n 10` and under 1 GB. The frozen ladder took about 2 minutes and the diagnostic about
3.5 minutes.

κ = ½ FITTED; not theory closed.
