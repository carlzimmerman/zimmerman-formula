# OQ2 frozen criteria: the OQ1 one-scalar door with a powered bin rule

Frozen before any OQ2 script or OQ2 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. TEST lane: no
particle; no LCDM input; both footings (canonical a0 9.3603e-11, Lstar 21.7 pc; alt a0 1.1312e-10, Lstar 22.9 pc), never
pooled; "passes" needs both. No downloads. One thread, under 1 GB RSS, `nice`, preemptible (checkpoint on SIGTERM).

Successor of OQ1 (criteria 3d8e38ffb2, result 048386c5fb). Everything in OQ1's FROZEN_CRITERIA.md is unchanged:
q = Sigma / rho_DE with Sigma = F rho_ph + 2X, the self-consistent iteration (starts F0 in {0, 1, 10}, cap 200), the classes
and their allowed-F intervals, groups f* = 0 and 1, the web arm, KA1-KA4, S2, S3, the labels and the twins M1 / M2 / M3.
`oq2.py` imports `oq1.py` read-only and reuses its functions; no OQ1 function is edited.

## 0. Why OQ2, and the one change

OQ1 reads NO VERDICT because M1 (planted true law F_true = 1 + 3 (q/q_med)^0.5, noise at each point's measured error, seed 21)
found false conflicts. Every M1 false conflict sits in a bin where at least one voting class has 1 to 4 points (LG field 1,
bright M31 1, groups 1 or 4, X-COP 1, Coma UDGs 2). One noisy point gives a narrow band that the noise can push off the law.
So a class with too few points in a bin should not vote in that bin.

**The one change: occupancy minimum.** In S1 (and in S3, which reads the same bins), a class votes in a bin only if it has at
least N_min points there. The web votes in a bin if it has at least N_min cells there. Bin width (0.2 dex), anchoring, the
iteration and the projection of each point onto its own class band are unchanged. So N_min changes which bins are tested,
not the fixed points. A bin with fewer than two voting classes is not tested. "Conflict" is unchanged: an empty intersection
of the voting classes' allowed-F intervals, any gap (0 dex included).

Why this rule, not the other two options:
- Adaptive equal-count bins would mix 0.2-dex resolution across classes and change what "fixed q" means.
- A bootstrap overlap test on q ranges would replace the F-interval test itself.
- The occupancy minimum changes one thing only, and it targets exactly the failure M1 showed.

Disclosed: this session ran OQ1 and has seen OQ1's main-data bins (SPARC vs X-COP, X-COP 1-7 points per bin). N_min is not
chosen by hand. It comes from the M1 null alone, by the rule in section 1, before any OQ2 main-data run.

Expected outcome, stated in advance: probably DEAD, from SPARC vs X-COP at log q 2.8-4.4, if N_min stays at or below the
X-COP occupancy there. If calibration pushes N_min above what X-COP reaches, M2 will not bite and the run says NO VERDICT.

## 1. Stage 0: calibrate N_min from the M1 null (no main data touched)

- **Twin.** OQ1's `plant` with the noise seed as the only argument. q_med is OQ1's committed value per footing
  (oq1_MUTATE_M1.json: 53345.4 canonical, 40698.9 alt). Web excluded from the twins, as OQ1 did (disclosed there).
- **Ensemble.** Noise seeds 1001-1020 (20 seeds) at start F0 = 1, groups f* = 0 and 1: 40 runs per footing. Plus OQ1's own
  M1 (seed 21) at all three starts and both f*: 6 runs per footing.
- **Grid.** N_min in {1, 2, 3, 4, 5, 6, 7, 8}.
- **Rule.** N_min* = the smallest N in the grid such that, on both footings:
  - (a) the false-conflict rate over the 40 ensemble runs is <= 5 % (at most 2 of 40 runs have any conflict); and
  - (b) seed 21 reads no conflict in all 6 runs and S3 holds in all 6 runs (OQ1 section 6 M1 condition, under N_min).
- **No N passes.** Then the method has no power to find a true law. Label: NO VERDICT. Main data is still run and reported
  at N_min = 8, without a label.
- **Commit first.** Stage 0 writes oq2_stage0.json / oq2_stage0.out. These are committed before the main-data run.

## 2. Power checks at N_min* (both footings; all must hold, else NO VERDICT)

- M1 (seed 21): reads no conflict and S3 holds, every start and every f*. This is rule (b) above.
- M2 (seed 21, planted +0.3 dex on X-COP, groups and ellipticals): S1 must read DEAD. That means, for every footing and f*,
  at least one start has a conflict (OQ1 rule).
- M3 (Newton, F = 0): SPARC G1 |Z| > 0.057 (G1 fails), as OQ1.

## 3. Main data at N_min*

OQ1's S1 runs, unchanged, with the occupancy rule applied. The labels are OQ1's:
- **DEAD**: a conflict in any run on either footing. Report the bin, the classes with n and the gap in dex.
- **S1 holds**: S2 and S3 as OQ1 section 4. If S2 is not built in this lane, the label is "S1 HOLDS, S2 OWED", not a pass.

Every label also prints the number of points per class that never vote (in bins below N_min), so the reader sees what the
rule dropped.

## 4. Web row (its own labelled row, both footings)

Question: does the CMB wall need the law's phantom off on the web? F_web,max is the largest uniform F with lensing amplitude
r <= 1 + 3 sigma_A on SV5 iter_1's statistic (OQ1's `web_pass`, recomputed; KA3 must match SV5 to 1e-3).
- **YES**: F_web,max < 1 on both footings. The full law phantom is excluded on the web.
- **NO**: F_web,max >= 1 on either footing.

A second row, SEPARATED (yes / no), is also reported. YES if the largest web q at F_web,max is below the lowest host q
(non-SS classes, F0 = 1 run, both f*) on both footings. That is, the one scalar can tell the web from every host.

Neither row adopts anything. A YES says what the web needs. It does not say an action supplies it.

## 5. Outputs

`oq2.py` writes:
- oq2_stage0.json / .out (committed first);
- oq2.json / oq2.out;
- oq2_MUTATE_M1.json, oq2_MUTATE_M2.json, oq2_MUTATE_M3.json (separate outputs).

RESULT.md gives, per footing:
- N_min* and the calibration table (false rate per N);
- the bin table of the conflicts;
- the label, the web rows and the margins, all read from the JSON.

Any change after this freeze is disclosed in RESULT.md as post-freeze.

Kappa = 1/2 FITTED; not theory closed.
