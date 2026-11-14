# RB2R LEAD CHECK (2026-11-14): commit ids, the lead's re-run, the blindness check, and the comparison with RB2

Written by the lead session after the blind result was committed. TEST lane; adopts nothing, relabels nothing.
The blind agent's files in this folder are not edited.

## Commit ids

| what | local | origin |
|---|---|---|
| WHAT_I_SAW_AT_START.md + frozen criteria (alone) | d8951c0b42 | 77a8502c1c |
| AMENDMENT_A1.md (alone, one added twin pair) | 17bde9c946 | 3d88e69730 |
| script and run outputs | f76f9e672c | ef352048a5 |
| RESULT_BLIND.md | 5ff25fccd5 | 655d96fc81 |

## The lead's re-run

`rb2r.py` copied alone into a new folder at the same depth (not committed, removed afterwards) and run from scratch:
`rb2r.out`, `rb2r.json`, `rb2r_MUTATE.out` and `rb2r_MUTATE.json` are byte-identical to the committed files.

## Blindness

- The agent's tool calls were listed by script (32 calls). It read two files with the read tool: the house rules and its
  specification. Its shell commands touched the three catalogue files and their provenance note, its own folder, and
  git commands on its own folder (`git add`, `git commit`, `git log -1 -- <its folder>`, one `git show --stat` of its
  own commit). It opened nothing in RB2's or NH2's folders, no scorecard, no papers folder and no memory folder, and
  did not use the web.
- **One hint came from the lead's own specification.** Its list of forbidden search terms named "NGC 147", "IC 1613"
  and "Crater". That tells a reader these systems matter in the earlier lane. The agent disclosed it. The LOW rule is
  arithmetic on catalogue rows that the agent graded for all 51 systems alike, so the hint could not move a number,
  but the lane is not blind to which rows to expect. A forbidden list should name folders and file names, not objects.
- The specification handed over was RB2's frozen text for this part (form B, the Jacobi radius and its three edges, the
  estimator, the LOW rule and the two words), without RB2's seen numbers or hand estimates. The lead narrowed the
  sample to M_V <= -7.7 (51 rows graded, 49 left out) so the lane would not depend on the binary-correction table.

## Comparison with RB2 (made after the blind result was committed)

| quantity | RB2 | RB2R (blind) |
|---|---|---|
| LOW rows, canonical | Crater II, NGC 147, IC 1613, DF2, DF4 | the same five |
| LOW rows, alt | the same five and Cassiopeia III | the same six |
| TIDES CANNOT REACH on both footings | NGC 147, IC 1613, DF2, DF4 | NGC 147, IC 1613, DF2, DF4 |
| Crater II | TIDES CAN REACH, needs r_J inside r_1/2 | TIDES CAN REACH, needs r_J inside r_1/2 |
| DF2 below B's isolated law, canonical / alt | 0.743 / 0.781 dex | 1.710 / 1.798 in ln, that is 0.743 / 0.781 dex |
| DF4 below B's isolated law | 0.943 / 0.981 dex | 2.171 / 2.259 in ln, that is 0.943 / 0.981 dex |
| DF2, DF4: r_J / r_1/2 at the projected distance | 3.48 / 8.67 (alt 3.49 / 8.68) | 3.48 / 8.67 |
| DF2: host mass inside 79.3 kpc that B would need | 1.163e13 / 1.347e13 Msun, 16.6 / 17.6 times the law's | 1.16e13 / 1.35e13 Msun, about 17 times |
| DF4: host mass inside 165.3 kpc that B would need | 1.396e14 / 1.618e14 Msun, 99 / 105 times | 1.40e14 / 1.62e14 Msun, about 100 times |
| NGC 147 below B | 0.56 / 0.59 dex; r_J about 5 r_1/2 at the strong edge | 0.554 / 0.585 dex; 5.07 / 5.30 |
| IC 1613 below B (no host) | 0.54 / 0.58 dex | 0.537 / 0.574 dex |
| Cassiopeia III, alt only | -0.230 against s 0.100 | -0.221 against s 0.100 |
| Crater II today | 0.44 dex below B at 115 kpc, r_J = 1.78 r_1/2 | 0.435 / 0.475 dex, r_J = 1.77 / 1.86 r_1/2 |
| Crater II at the strong edge | pericentre 32 kpc, r_J = 0.17 r_1/2, B's residual +1.03 | pericentre 31.7 kpc, r_J = 0.158 / 0.186 r_1/2, residual + 2 s = +1.88 / +1.77 |

Reading:

- **The blind build confirms the part of RB2 that scorecard row 36 rests on: DF2, DF4, NGC 147 and IC 1613 sit below
  form B's isolated law by more than twice their uncertainty on both footings, and tides cannot reach any of them.**
  The same rows are LOW and carry the same words in both builds. DF2's and DF4's numbers agree to three figures.
- The one number that differs is Crater II's residual at the strong edge (RB2 +1.03; RB2R about +1.58 before the
  2 s is added). The cause was not traced. The word is the same, and Crater II does not count against B in either
  build.
- The mass-to-light ratios quoted beside the rows are not the same quantity in the two builds (RB2: the ratio that
  brings NGC 147 onto B; RB2R: the ratio at which a row stops being LOW), so they are not compared.
- The frozen twin T3 did not bite, as the agent reports first; its amendment A1 adds a twin pair that does. What T3
  showed is a property of B, not a fault of the pipeline: a dwarf deep in the law's regime comes back to Newton only
  when its tidal radius is a small fraction of its half-mass radius. The four rows that count against B have tidal
  radii 3 to 10 times their half-mass radii, far from that.
- What this confirmation covers: the arithmetic of the frozen part, done twice with separate code, including a separate
  orbit integrator. What it does not cover: the assumptions both builds share (spherical, isotropic, equilibrium; the
  Wolf estimator; a mass-to-light ratio of 2 with a 0.15 dex prior; no gas term; an instantaneous tidal cut; host
  masses by convention; NGC 1052's mass taken as the law's on 1e11 Msun of baryons; D = 20 Mpc for DF2 and DF4).
  IC 1613 is gas-rich and rotating, so a dispersion-only estimate is not its full mass budget; adding gas moves it
  further below B.

Scorecard row 36 keeps its word, FAILS. Its blind column changes from "no" to "yes (RB2R, same rows and words)".

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
