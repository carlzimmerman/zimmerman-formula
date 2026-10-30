# SH1_softened_halo_grade: softening at galaxy mass alone FAILS; it passes only if clusters soften too (untested), and MW and lensing still fail

Criteria: `FROZEN_CRITERIA.md` (335e212551), committed before any script or number. Script `sh1_grade.py`. Results:
`sh1.out`, `sh1_results.json`, `sh1_mutate.out`, `x79_*/`. Cluster masses are ng 48 until A4.

## Route E grader (X74 unchanged), canonical. Same labels at f★ 0.034 and 0.0615
| scenario | R | η at 10¹² / 10¹³ / 10¹⁴ | SPARC Υ | label | failing |
|---|---|---|---|---|---|
| A supernovae only | 0.573 | 14.86 / 17.67 / 16.91 | 0.55 | **SOFTENED FAIL** | G-MID-T3, G-IN-Mall (OVER) |
| A | 0.685 | 17.77 / 17.67 / 16.91 | 0.53 | **SOFTENED FAIL** | same |
| A | 0.817 | 21.19 / 17.67 / 16.91 | 0.52 | **SOFTENED FAIL** | same |
| B cluster softening granted | 0.573 | 14.86 / 10.12 / 9.69 | 0.56 | KNIFE EDGE | at η p16: groups above law, Z +2.01 |
| B | 0.685 | 17.77 / 12.10 / 11.59 | 0.54 | **SOFTENED PASS** | none at median, p16, p84 |
| B | 0.817 | 21.19 / 14.43 / 13.82 | 0.52 | KNIFE EDGE | at η p84: G-IN-Mall (OVER) |

Alt fails the SPARC line in all six (Υ 0.44–0.47), and A also fails the same two cluster lines. X78 traced the alt SPARC
failure to the a0 law, not to route E.

## Milky Way and KiDS (X79's text, only η changed; canonical)
| scenario | MW class | in-prior v_c (R_d 2.60; Eilers 229.1 ± 4.6) | KiDS Δχ² all radii | X53 rule |
|---|---|---|---|---|
| A / B R 0.573 | V+K ONLY | 202.5 | +423.7 / +423.7 | LAW |
| A / B R 0.685 | V+K ONLY | 204.9 | +426.4 / +426.1 | LAW |
| A / B R 0.817 | FEASIBLE (WIDE PRIORS ONLY) | 209.6 | +433.3 / +433.0 | LAW |

**ALL LINES: none.** No scenario reaches the MW within published priors, and every scenario stays LAW on KiDS.

## Reading
- **Supernovae alone do not rescue route E.** Softening at 10¹² fixes SPARC, which the grader confirms, but the cluster
  lines fail OVER at every R, because CL4 excludes supernova energy at those masses.
- **The one pass is conditional.** B R 0.685 needs about the same softening at 10¹³ and 10¹⁴, which only black hole coupling
  could pay for. That coupling is untested and R there is assumed. It also needs coupling ~1 at 10¹² (CM3).
- **Softening pulls against the MW.** Softer halos lower v_c: the pass at R 0.685 sits at 204.9, against 209.1 for X77's η.
- **Lensing is unaffected.** It is a halo-mass deficit (X79), and softening does not change M200.
- **Not graded:** LS1's L★ analogs. LS1 found c_f 4 under-massed there and converged η mostly fixes it; softened η lies
  between, so part of that deficit may return.

## Checks
- **K1 PASS:** R = 1 reproduces CE1 (max |d| 0).
- **K2 PASS:** grader η(10¹²) at R 0.817 is 21.191.
- **K3 PASS:** X79's table reproduces v_c 209.1 and Δχ² +432.2.
- **MUTATE FAIL as frozen:** R 0.3 gives Υ 0.560, the same as B R 0.573 (0.560), and the criterion required a rise. Not amended.
  Reported after the result: the a0 floor already binds at R 0.573 for most of SPARC (the MW's Σ/Σ_a0 is 1.000 there), so Υ has
  saturated and the criterion was badly chosen. The grader does respond at R 0.3: rms 0.07134 vs 0.07137, and groups
  Z +2.09 and G-MID-T3 (UNDER) newly fail. Υ also rises with softening from R 1 to 0.573 (0.48 to 0.56).

## Run notes
- The first `--x79` start raced the script's creation and did nothing.
- The first version of `x79_run` wrote into a subfolder, which would have broken REB; fixed before any X79 run.
- The X79 runner's file sweep caught grader outputs running at the same time. They were moved back unchanged, and copies of
  `sh1.out` and `sh1_results.json` were removed.
- Home paths were stripped from outputs.

R is one 6×10¹¹ galaxy applied at all masses at or below 10¹². Coupling, cadence and moved mass are inputs.

κ = ½ FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework. Cold dark energy
is a gravitating field component, never a particle.
