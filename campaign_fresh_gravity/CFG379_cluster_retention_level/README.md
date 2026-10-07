# CFG379: does the working model's supply limit set the cluster retention level? FAILS

Criteria: `FROZEN_CRITERIA.md`, committed alone first in 2858fb9a3. Script: `cfg379_retention.py` (output `cfg379.out`, `cfg379_results.json`). MUTATE: `CFG379_MUTATE=1` (outputs `*_MUTATE`). POST-FREEZE: `cfg379_postfreeze.py` (labelled).

**The question.** The working model's rule is r = min(M_ph(<R_ap), S_catch) / (5.364 M_b): a host settles cold fluid only up to its phantom target, and only as much as its catchment supplies. Does this rule give the measured levels (X-COP 0.576, groups 0.60, Milky Way-like 0.14) with no new constant?

**Frozen verdict: FAILS.** Neither catchment reaches 2 of 3 classes on either footing.

## What came out

| catchment | footing | clusters (target 0.576) | groups (0.60) | MW-like (0.14) | passes |
|---|---|---|---|---|---|
| TA (turnaround, Delta_ta = 11.76) | canonical | 0.556 PASS | 1.133 fail | 0.480 fail | 1/3 |
| TA | alt | 0.619 PASS | 1.254 fail | 0.536 fail | 1/3 |
| RC (Gaussian, 3 Mpc/h) | canonical | 0.101 fail | 1.128 fail | 0.480 fail | 0/3 |
| RC | alt | 0.101 fail | 1.249 fail | 0.536 fail | 0/3 |

**Which constraint binds:**
- **TA:** the supply never binds. S/(5.364 M_b) is 4.3–5.7 for clusters, 7.8–12.3 for groups and 29 for the Milky Way. The phantom target sets r everywhere.
- **RC:** the supply binds in all 12 clusters (S/(5.364 M_b) = 0.06–0.18), in 4 of 20 groups (canonical) or 6 of 20 (alt), and not in the Milky Way.

**Reading.**
- Under the turnaround catchment, the supply limit does nothing: the catchment holds 4–29 times the host's cosmic share.
- Under the 3 Mpc/h catchment, the limit starves clusters to 0.10 instead of 0.58.
- So no catchment from the record produces the cluster level through the supply limit.
- The phantom target alone overshoots the group level by about 2x, and the Milky Way level by 3.4–3.8x.

**The one cluster "pass" is not a prediction.** The TA cluster numbers match 0.576 because, at R500 in clusters, M_ph happens to be about equal to the mass beyond the law. That is MOND's classic factor of about 2 in clusters. It does not come from retention physics.

## Bookkeeping check B (reported; it changes how the question should be posed)

The measured levels use definition A (cm02/cm08): the mass beyond the law, (M_tot − M_b − M_ph)/(5.364 M_b). The literal rule compares M_ph with that excess, so it compares two different quantities.

In the working model's own accounting, all gravitating mass beyond the baryons is cold fluid, and the cap says M_tot − M_b ≤ min(M_ph, S). Against the data:
- **The cap is violated in 12/12 clusters and 20/20 groups, on both footings.** Every host has f_A > 0.
- **Measured total cold content, r_tot = (M_tot − M_b)/(5.364 M_b):**
  - clusters: 0.96 at R500 and 1.04 at 1 Mpc. Clusters hold about their full cosmic cold share; roughly half of it sits beyond the phantom target.
  - groups: 1.69, inflated by baryon depletion (CFG371).
- The Milky Way has M_ph/(5.364 M_b) = 0.48. Adding the ledger's 0.14 gives a total of about 0.62, which also exceeds the cap.

So, read in its own bookkeeping, the rule "settles only up to the phantom target" is contradicted by the hydrostatic masses in every group and cluster.
- A working version needs either cold fluid that sits inside R500 without settling (uncapped), or a cap other than M_ph.
- Making the phantom act as extra gravity is the additive reading, which over-builds growth (CFG359/361).
- In clusters the open question is why the target is only about half of what is there. It is not why the retention is 0.6.

## Controls
- **C1 FAILS, and the failure is kept.** At R500 the X-COP median f_A is 0.430, not the ledger's 0.576. The ledger value is CFG4's, taken at r = 1 Mpc (0.70–0.95 R500).
- **C2 passes:** Lovisari median f_A = 0.549, reproducing cm02 exactly.
- **C3 passes:** the turnaround identity holds to 4e-15.
- **C4 passes:** the min rule gives the right limits.
- Main run rc 1, because C1 failed.

**POST-FREEZE (labelled; `cfg379_postfreeze.out`): clusters at r = 1 Mpc, the ledger's aperture.**
- Measured f_A is 0.560 (canonical) and 0.497 (alt), close to the ledger.
- TA predictions are 0.508 / 0.567 (PASS; target binds in all 12). RC predictions are 0.132 / 0.132 (fail; supply binds in all 12).
- At R500 itself, the TA cluster prediction 0.556 would fail against the R500-consistent measured 0.430: it misses by 0.126 and lies outside 16–84% = 0.37–0.49.
- Groups and the Milky Way fail on both catchments, so **the verdict stays FAILS at either cluster aperture.**

## MUTATE (supply x10)
- The declared flip is **MET**. Under RC the clusters stop binding (12/12 → 0/12) and pass, at 0.556 / 0.619. RC moves from 0/3 to 1/3.
- **The headline is unchanged (FAILS).** That is disclosed, as CFG370 did: groups and the Milky Way fail on the target alone, whatever the supply.
- MUTATE rc 1.

## Sensitivities (reported)
- MW-like r_ph at M_b = 5e10 / 8e10 is 0.56 / 0.43 (canonical). It fails either way.
- Top-hat RC catchment (3.8x smaller supply): clusters drop to r = 0.027.
- A mass sweep at the MOND radius gives r_ph = 0.108 at every mass there (y = 1). TA never binds from 1e10 to 1e15. RC binds above about 8e13 (10^13.9).

## Caveats
- Hydrostatic masses with no bias. A lensing bias would raise f_A and r_tot further.
- Monopole phantom. MW baryons treated as a point mass inside 30 kpc.
- Delta_ta comes from the LCDM-background solver in CFG100 (11.76 here, against the 11.806 quoted in the brief).
- Supply is taken at the cosmic mean cold density, with no prior clustering of the cold fluid.
- The aperture baryon mass is used as the host baryon mass in r_ta.
- M_star for X-COP clusters without an M_star profile is set to 0.10 M_gas, as in CFG371.
- κ = ½ is fitted. No dark-matter particle is added, but the cold fluid's mass (Ω_c/Ω_b = 5.364) is still required and is not derived. This is not "theory closed".
