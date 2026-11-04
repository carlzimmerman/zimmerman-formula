# WG3_bound_only_web_rule: the record's bound-only switch FAILS LOW. From a baryons-only start it never turns on, and no rule tried lands CMB lensing

**Commits.**
- Criteria: bb3410083d, committed alone before any script or number.
- Amendment A1 and engine: ba8477ae8e, before any production run.
- Grader: ec50c264d8, before any run finished.
- Result: this commit.

**Origin.** Owner 2026-11-04: "lets go!", after WG2.

**Standing.** κ = ½ FITTED. The cold sector stays retired; T1 is borrowed from it as a test and adopts nothing. Not theory closed. Nothing here says the data favour the framework.

## Question
WG2 (6856666719, under its post-result A2) showed the law alone misses CMB lensing on both sides:
- off on the web: r ≤ 0.31;
- QUMOND on the web: r 11-6,900.

WG2's README and the PAPER67 v1.1 draft then said "no rule on record lands there", but only off and on had been tried. This lane runs the record's one web rule on WG2's engine and data: CFG354's T1 bound-only switch, as CFG359 ran it.

**The rule.** QUMOND's phantom × f, with f = clip(½ + (λ₂ − τ)/2ε, 0, 1), ε 0.077, τ from the EdS turnaround Δ_ta = 9π²/16. That Δ_ta is the record's lower bound, the setting that switches the law on most.

## Result
r is the model's lensing amplitude over the measured one (Planck PR4, PACKAGE rule; PLAIN agrees within 3 %). f is the switch's ON fraction, by volume / by mass.

| rule | B2 (A_s 1e-9 / 4e-9) | B1 (A_s 1e-9 / 4e-9) | f at z 0 | label |
|---|---|---|---|---|
| **T1 (record rule, graded)** | 0.00022 / 0.00089 | 0.077 / 0.31 | 0 / 0 everywhere | **FAILS LOW** |
| T1V (filament veto, reported) | 0.00047 (A_s 2.1e-9) | not run | 0 / 0 | FAILS LOW |
| T1τ0, τ = 0 (reported) | 1.34 / 1.85 | 124 / 162 | B2 0.50 / 0.50; B1 0.37 / 0.59-0.64 | STRADDLES |
| WG2 R0, law off (context) | 0.00022 / 0.00089 | 0.077 / 0.31 | n/a | FAILS LOW |
| WG2 R1, QUMOND on (context) | 11.4 / 14.1 | 560 / 657 | n/a | FAILS HIGH |

**Record line: no rule tried lands there.** That covers law off, QUMOND on, and the record's bound-only switch (T1).
- **Why T1 fails.** From a Silk-damped baryons-only start, nothing reaches turnaround without the law, so the switch never turns on. T1 reproduces law-off to four digits (δ_rms at z 0 0.04887 against 0.0489; 0.002008 against 0.00201). This matches the expectation written in the criteria before any run.
- **Resolution.** K5 (192³) gives the same label, r 0.00077.

**T1τ0 is not a rule, and its within-×2 in B2 is not a hit.** It was reported only, as a bracket member. With the measured-style expansion (B2) the field stays linear (|λ₂| ≪ ε), so the ramp sits at its midpoint: f = 0.50 by volume and by mass at every redshift. T1τ0 there is QUMOND with its phantom halved uniformly, and the ½ comes from the ramp's midpoint, not from physics.
- **What it shows (a post-hoc reading):** in B2, halving the phantom source drops the lensing from about 12× to 1.3-1.9×. The law-on overshoot sits within roughly a factor 2 in phantom strength.
- **A route to test, not a result:** a rule derived from the action that halved the web phantom would land within ×2 there. It would still need its own frozen criteria and all gates. With baryons alone in the expansion (B1), T1τ0 fails high.

## Checks
- **K1** (WG2 engine, 128³): 0.985, PASS.
- **K2** (QUMOND plane wave): 2.5e-7, PASS.
- **K3** (Limber): 7.9e-7, PASS.
- **K4b** (ICs, ratio of summed power): 0.970, PASS.
- **K8** (switch):
  - fully on vs R1, off the Nyquist planes (A1): 1.7e-7;
  - all modes, as frozen: 2.8e-3; the difference sits entirely on the Nyquist planes;
  - fully off vs R0: 0;
  - eig3 vs numpy: 1.2e-15;
  - PASS under A1.
- **K5** (192³): same label, PASS.
- **MUTATE** (WG2's Poisson-halved K1): K1 0.149 FAIL, and the record line reads NOT EVALUABLE. The check bites.

## What this means for the record
- **WG2 and PAPER67.** "No rule on record lands there" becomes "no rule tried lands there: off, QUMOND on, or the record's bound-only switch (T1, WG3)".
- **D9 for the law alone.** It stays FAILS. The record's web rule adds a third failing reading, on the low side.
- **A requirement for any future action.** On the linear web, from a baryons-only start, the law's source must come out at about half of unscreened QUMOND's (B2), and that factor has to be derived, not set.

## What this lane can't say
- It shares WG2's limits: 12.5 h⁻¹ Mpc mesh, no primary-CMB test, A_s bracketed, lensing assumed to see the dynamical potential.
- T1 is a sub-cell criterion. Collapse below 8.3 h⁻¹ Mpc is invisible to it. With Silk-damped baryons-only initial conditions there is little such power without the law.
- T1τ0's numbers are a post-hoc reading of a reported variant.
- Nothing here reinstates the cold sector.

## Files
- `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`
- Scripts: `wg3_pm.py` (wraps WG2's engine, read only), `wg3_run_all.py`, `wg3_grade.py`.
- Run outputs: `runs/*.json`.
- Graded results: `wg3.out` and `wg3_results.json`, and the `_MUTATE` versions.

**Run.**
- `python3 wg3_pm.py checks`, then `python3 wg3_run_all.py` (about 35 min).
- `python3 wg3_grade.py`, then `python3 wg3_grade.py --mutate`.
