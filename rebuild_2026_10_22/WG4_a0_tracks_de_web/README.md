# WG4_a0_tracks_de_web: a0 tracking evolving dark energy cuts the overshoot from 11-14× to 6.7-8.5× but FAILS HIGH. The missing factor can't come from a0's evolution

**Commits.**
- Criteria: 6f8cd8bbd1, committed alone before any script or number.
- Engine and driver: 55c08a479b.
- Grader: b896f00c58, before any run finished.
- Result: this commit.

**Origin.** Owner 2026-11-04, on WG3's open lead, a factor of about ½ in the web phantom that "has to come from the theory": "okay work on this then".

**Standing.** κ = ½ FITTED. The cold sector stays retired. No particle and no cold component is added. Not theory closed. Nothing here says the data favour the framework.

## Question
The framework's law is a0(z) = κ c √(G ρ_DE(z)), and the owner's standing rule is that a0 tracks evolving dark energy. WG2 ran only flat a0, the w = −1 case. With DESI DR2's evolving dark energy (CPL −0.838, −0.62, the record's values, via a0kit), a0 is lower in the past: 0.87 at z 2, 0.45 at z 10, 0.17 at z 50. That weakens the deep-regime boost exactly when WG2's growth runs away. Does it supply the missing factor?

## Result
Setup: WG2's engine (baryons-only CLASS start, QUMOND on the web, 1600 h⁻¹ Mpc, 128³), graded on Planck PR4 8-400. r is the model's lensing amplitude over the measured one.

| a0 history | expansion | r (A_s 1e-9 / 4e-9) | label |
|---|---|---|---|
| flat (WG2, context) | B2 | 11.4 / 14.1 | FAILS HIGH |
| **tracks ρ_DE, DESI CPL (primary)** | **B2D** | **6.7 / 8.5** | **FAILS HIGH** |
| tracks ρ_DE, CPL (a0 only) | B2 (Λ) | 6.7 / 8.5 | FAILS HIGH (reported) |
| native band, 68 % lower edge, held at 0.33 beyond z 2.33 | B2 | 3.7 / 4.7 | FAILS HIGH (reported) |
| tracks ρ_DE, CPL | B1D (baryons-only expansion) | 321 / 388 | FAILS HIGH |

Checks on the primary:
- K5 (192³): 7.51 against 7.60 at 128³, same label.
- The alt footing gives 10.5.
- Every K check passes: K1 0.985, K2 2.5e-7, K3 7.9e-7, K4b 0.970, K9 exact.
- MUTATE bites: K1 0.149 FAIL, and the record line reads NOT EVALUABLE.

**Record line: a0 tracking DESI's evolving dark energy does not close the gap.** It fails high. The CPL comes from a CDM-family fit and is extrapolated beyond z 2.33.

## What this settles
- **How far the evolving-dark-energy a0 gets.** It closes about 40 % of the gap in log: from 12.7 to 7.6 (A_s 2.1e-9). Landing needs r ≤ 2.
- **Even the most extreme history the native data allow isn't enough.** That history sits at the CFG689 band's 68 % lower edge, with a0 down to 0.33 of today's from z 2.33 on, and it leaves 3.7-4.7×.
- **So the remaining factor lives at z ≲ 2.**
  - WG3's T1τ0 shows that halving the phantom at every redshift lands, at 1.3-1.9.
  - At fixed source, halving the deep-regime phantom means a0 at a quarter of its value.
  - At z ≲ 1, a0 is pinned by galaxies (SPARC) and by the band's 0.91 [0.76, 1.03] at z 1.
- **Consequence:** the missing factor can't come from a0's time evolution without contradicting the galaxies the law was built on.
- **Where the factor must come from instead:** a difference between the linear web and bound galaxies at the same epoch and the same a0. That is a rule that weakens the law on the web but not in galaxies. It must be derived, not set.
  - The record's one such rule (T1, the turnaround switch) never turns on (WG3).
  - No other rule on record does this.

## What this lane can't say
- It shares WG2's limits: 12.5 h⁻¹ Mpc mesh, no primary-CMB test, A_s bracketed, lensing assumed to see the dynamical potential.
- The CPL form beyond z 2.33 is an extrapolation. The native band ends at z 2.33.
- "No other rule on record" is a reading of the record, not a theorem. A modified-inertia reading of the law, in which the law depends on the whole trajectory rather than only the local field, could differ for the web's infall motion. No such computation exists on record.
- Nothing here reinstates the cold sector.

## Files
- `FROZEN_CRITERIA.md`
- Scripts: `wg4_pm.py` (wraps WG2's engine, read only), `wg4_run_all.py`, `wg4_grade.py`.
- Run outputs: `runs/*.json`.
- Graded results: `wg4.out` and `wg4_results.json`, and the `_MUTATE` versions.

**Run.**
- `python3 wg4_pm.py checks`, then `python3 wg4_run_all.py` (about 25 min).
- `python3 wg4_grade.py`, then `python3 wg4_grade.py --mutate`.

## Correction 2026-11-04 (WG5)
The line on a modified-inertia reading of the law ("could differ for the web's infall motion. No such computation exists on record") missed the record. Pure modified inertia, the framework's original arm, was closed on 2026-08-08: galaxy lensing excludes it at 21σ, and all three rescues are closed (`RETRACTIONS.md`, `STANDING.md` line 284). In it, light sees no phantom, so it can't be the rule that weakens the law on the web but not in galaxies. WG5's diagnostic adds that it also misses CMB lensing, low with the measured-style expansion (r 0.013-0.051). No number here changes.

