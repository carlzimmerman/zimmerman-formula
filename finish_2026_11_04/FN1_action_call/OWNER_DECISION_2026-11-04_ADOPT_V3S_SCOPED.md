# Owner decision, 2026-11-04 (later): v3s is adopted as the action for the galaxy law, scoped; this supersedes the same day's "no action"

Recorded at the owner's instruction. Asked in chat whether to adopt v3s as the galaxy law's action with clusters and the CMB stated as open, the owner answered **"Adopt v3s, scoped"**. This supersedes `OWNER_DECISION_2026-11-04_NO_ACTION.md` (option c) on requirement 12. That file is kept unedited as the record of the earlier call. kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.

## What is decided
- **v3s is the action for the a0 law, in this scope:** isolated galaxies, the Solar System, galaxy lensing and gravitational waves. Requirement 12 is met for that scope only.
- **Not in scope, still open:** clusters, linear growth and the CMB, the radiation era, hosted dwarfs and the Milky Way joint fit. The 10-24 verdict's failures there stand unchanged (`covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md`), and v3s supplies no cluster or CMB mass.
- **a0 is put in by hand.** a0 = kappa c sqrt(G rho_DE) is not derived from the action, and kappa = 1/2 is fitted.
- Route E's cold sector stays retired. Nothing here reinstates it.

## What the scope rests on (each lane's README is the record)
| Gate | Result | Lane, commit |
|---|---|---|
| Every action class graded | only v3s's screening length L* passes G1-G4 on both footings; unscreened classes fail Cassini Q2 by 1.69-5.18x | AX1, 9c11102bf3 |
| Solar System | clean PASS; Q2 margin to Hees >= 4.9e7 (canonical), 5.7e7 (alt); planets <= 0.17 of bound | C6P, 8c5703da06 |
| PPN gamma, beta | derived from the action: gamma = beta = 1, remainders <= 1e-12 | V3W W1, 17d7b7ecdc |
| Galaxy lensing = dynamics | KiDS isolated A 1.13 +- 0.21 / 1.04 +- 0.19; weak power | V3W W3, 17d7b7ecdc |
| GW speed, galaxy health | c_T = c (<= 6e-32); no ghost or gradient instability | V3W W4a/b, 17d7b7ecdc |
| Solar-System health, 3D hyperbolicity | (a) and (c) PASS; (b) no instability, two precision lines missed | V3X, ee4210e959 |

## Carried weak spots, stated with the adoption
- **V3X W2 UNDECIDED:** the in-window ladder reads Richardson -0.7 % against the 2 % line, but check K1 was frozen too tight at an ungraded radius.
- **V3X W4c(b) UNDECIDED:** the l = 1-4 spectral ladder misses at 14.6 % against 5 %, and the tensor roots sit 1.1e-10 below c against a 1e-10 line.
- **Constraints act instantaneously** (C5's cone-causality criterion fails; carried, not graded).
- **Still asserted, not shown:** post-Newtonian corrections don't flip signs, the Sun is at rest in the khronon frame, a uniform-density solar interior, and nonlinear well-posedness.
- **Weak lensing power:** on KiDS alone the MUTATE twin is caught at only 1.9 sigma; GH1 is what catches it.

## What follows
- STANDING.md gets one dated addendum.
- The status board should show v3s as the scoped action. The board belongs to its own session; this file is the source for it.
- A PAPER67 v1.2 would be needed to state this, since v1.1 (DOI 10.5281/zenodo.23966443) says no action is selected. It needs the owner's go and is not drafted here.
