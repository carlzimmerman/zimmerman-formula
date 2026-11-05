# CQ7_lstar_dwarf_window: WINDOW OPEN [21.68, 27.00] pc canonical and [22.85, 24.60] pc alt. With v3s's own static solves, no dwarf closes CQ1's window. The first dwarf to bind, beyond it, is LITTLE THINGS DDO 210 (median line): at 60 pc canonical and 40 pc alt

κ = ½ FITTED; not theory closed. Footings are never pooled. No particle, no cold sector, no ΛCDM input. Nothing here says the data favour the framework.

Criteria are in `FROZEN_CRITERIA.md` (a199cb1eb0), committed alone before the script. Amendment A1 (`AMENDMENTS.md`) swaps the rotation-curve solver from `solve_bvp` (it hit its node limit) to a finite-difference Newton solve. The ODE and the grading lines are unchanged, and the swap came before any graded label. Run with `OMP_NUM_THREADS=1 nice -n 10 python3 -B cq7.py`: 171 s, one thread, peak RSS 0.42 GB. It writes `cq7.out` / `cq7.json` / `cq7.time`. The MUTATE twin wrote `cq7_MUTATE.*`. No download. No file outside this folder is edited. D10's `d10_solver.py` is imported read-only.

## What changed from CQ1
CQ1's top edge was a reading: UGC 4483's screening radius must be ≤ 0.1 r_M, so L★ ≤ 27.0 / 24.6 pc. CQ7 instead solves v3s's statics, the C4-literal grad-div form that is unchanged under the switch (X3), and grades the predictions against data:
- **24 dSphs:** D10's 2D solver in the Newtonian host field, inverted through the law. The CZ5 line: a dwarf passes if some Υ in [1, 3] gives |σ − σ_obs| ≤ 2e, and the gate needs ≥ 15/24 to pass.
- **Isolated rotation curves:** UGC 4483 plus every SPARC or LITTLE THINGS galaxy with r_M (or 1.68 R_d) < 10 L★. Each is solved with the radial ODE on its own V_bar profile. KT19's lines are applied per galaxy against the same galaxy at L★ = 0.

## Labels
| footing | L★ graded (pc) | dSphs pass | RC gate galaxies | label |
|---|---|---|---|---|
| canonical | 21.68 / 24.34 / 27.00 | 17 / 17 / 17 (L★ = 0: 17) | 4 / 4 / 5, all SURVIVE | **WINDOW OPEN [21.68, 27.00] pc** |
| alt | 22.85 / 23.73 / 24.60 | 17 / 17 / 17 (L★ = 0: 17) | 4 / 5 / 5, all SURVIVE | **WINDOW OPEN [22.85, 24.60] pc** |

- **UGC 4483 at the top edge moves by almost nothing.** The rms shift is −0.0017 dex, the median shift +0.0005 dex and the largest pointwise shift 0.0058 dex. Under the actual solve, the "≪ r_M" reading was far too strict.
- **The largest graded shifts are in LITTLE THINGS:**
  - DDO 210: median +0.030 dex canonical, +0.029 alt (line 0.05);
  - UGC 8508: max pointwise shift 0.116 dex at its innermost point, with median +0.002.
- **Beside points (information only, no label):**
  - At 40 pc, canonical still passes everything.
  - At 60 pc, canonical first fails: DDO 210's median shift is +0.089 dex. Leo T also drops, taking the dSphs to 16/24, which is still above the line.
  - Alt first fails at 40 pc on DDO 210 (median +0.054).
  - **Binding dwarf beyond the window: LITTLE THINGS DDO 210** on both footings.
  - So the dwarf-set upper edge lies between 40 and 60 pc (canonical) and between 24.6 and 40 pc (alt). It was not bisected, since the frozen bisection applies only to graded failures. CQ1's other upper bounds still apply: MW H2 layer 90 pc, Leo T a_min 120 pc.
- **The window is still CQ1's [lo, hi] as labelled.** The top edge is the frozen grid's top, not a new bound. The lower edge, D10's globular floor (21.68 / 22.85 pc), is carried as is, along with its sensitivities: binary fraction 0.5 or the E-W estimator gives 25.9–27.0 pc, which would close alt's window as graded here, though not its extension beyond.

## Reading
- **Why the dSphs barely move.** At these L★ the screening acts only inside a few × L★. The dSph σ is set at r_h ≈ 120–700 pc, so all 24 pass or fail on exactly the same set as at L★ = 0, out to 40 pc. The 7 that fail do so unscreened: Draco, Ursa Minor, Sextans, Carina, CVn I, Cetus, Tucana. That is a law result, not a screening one.
- **Why isolated rotation curves barely move.** The isolated grad-div term shifts p by ≈ (L★/r)²-scale amounts. CQ1 noted this: l_γ = L★²/2r_M is about 1 pc for UGC 4483.
- **Screening raises the prediction's deficit (positive median shift = less boost) but often lowers the rms.** DDO 210's rms falls by 0.02–0.08 dex while its median crosses 0.05. Its fail is the frozen median line, not a worse fit. This is stated as is, not reweighed.
- **Switch state (reading only, not graded).** In every dSph solve, about 92–95 cells within 10 a have ∇·p < 0 in the solver's sign convention. CQ7 did not re-solve the switch there. X3/H5 resolved the globular and satellite lobes as benign. Whether these cells are the same external-field lobes was not checked here.

## As hard as a fail
- **Checks: 5/5 PASS.**
  - K1 reproduces CQ1's UGC 4483 numbers exactly: M_b 4.906e7, r_M 270.32 / 245.90 pc, 0.1 r_M 27.03 / 24.59 pc.
  - K2 reproduces C6's 24 recorded Sun wide-binary γ − 1 values, rel 0.
  - K3 matches the isolated 2D L★ = 0 σ to the law, 1.3e-4.
  - K4 matches the 1D solve at L★ = 0.3 pc to the law, 1.2e-4.
  - K5 is peak RSS, 0.42 GB.
- **MUTATE (L★ ≡ 0 everywhere) behaves as required.** Every RC shift is 0, the dSph count is 17 at every L★, there is no binding dwarf, and it exits 1 by design. So every shift above comes from the screening term.
- **A1 is disclosed.** The first, stopped run used `solve_bvp`, which failed to converge, so every gate galaxy was marked FAILS on solver status alone. Its unconverged shifts were within 1e-3 dex of the graded ones.
- **Approximations.**
  - The RC solves are spherical monopoles on V_bar²/r, as in KT19, not disc solves.
  - The dSphs are Plummer spheres in a uniform host field; the host is a 7e10 M☉ point mass for MW satellites, and M31 satellites are treated as isolated.
  - σ is the global virial σ (D10's E-V), not an aperture σ.
  - SPARC Υ is fixed at 0.5 / 0.7.
  - LITTLE THINGS uses V_bar² = V_tot² − V_DM² from Oh+2015's own decomposition (p47's loader). That decomposition is an input, not a framework quantity.

## Commits
- Criteria: a199cb1eb0.
- Script, outputs, amendment, README: this commit.
