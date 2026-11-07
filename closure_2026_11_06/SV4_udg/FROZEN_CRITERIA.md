# SV4: do the AGC 114905 / Malin 1 failures survive the systematics the record has not graded? (FROZEN CRITERIA, shared)

Committed alone, with iter_1/ to iter_4/FROZEN_CRITERIA.md, before any script or graded number of this lane exists.
kappa = 1/2 FITTED; not theory closed. Adopts nothing. One galaxy excludes nothing. Footings never pooled. Not blind:
the record's misses (UD1 chi2 844/996, UD2 69/132, QX4 exact field 700/830 and A1 54.7/42.9, A2 56.7/91.3) are known.
Rules: closure_2026_11_06/SWARM_BRIEF.md. No downloads: a dataset that is not on disk gives NOT EVALUABLE and a line
in NEEDS_OWNER.md.

## 1. What is graded

Data, errors and baryons are the record's: UD1 (AGC 114905, Mancera Pina+2024 vector figures, 5 rings) and UD2
(Malin 1, Lelli+2010 Table 3 and vector components, 4 rings). Their committed code and QX4's solver
(closure_2026_11_06/QX4_udg/aqual.py, and QX4's density builders in iter1_exact_aqual.py) are executed read-only.
QX8 graded SPARC with this same solver read-only, so "QX8's solver" = QX4/aqual.py.

The model is always the action's exact static field: the axisymmetric AQUAL solve, mu(x) = x/(1+x), of the
baryon density, midplane V_c(R) = sqrt(R dPhi/dR). Grid 480 x 144 in (ln r, theta), p = 3, as QX4's top rung; the
240 x 72 rung is run beside it and must agree to 1 % in V (ladder line, QX4's). Both footings:
canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2.

## 2. Statistic and labels (per galaxy, per systematic, per footing)

- chi2 = sum((V_data - V_model)/E)^2 over all rings, p = chi2.sf(chi2, N), N = 5 (AGC) or 4 (Malin).
- A correction is applied with its form and error budget frozen in its iter file. Its envelope is a short list of
  declared corners; the grade is taken at each corner, never at a value chosen to pass.
- **RESCUED (systematic, corner)**: p >= 0.05 at a corner that lies inside the published errors (each input within
  its published 2 sigma, or inside a published range). A pass only at a corner the iter file marks GENEROUS
  (outside the published errors) is reported as "rescued only outside published errors" and labelled NOT RESCUED.
- **NOT RESCUED**: no in-errors corner reaches p >= 0.05.
- **NOT EVALUABLE**: the published input the correction needs is not on disk.
- The galaxy's lane label is RESCUED only if some single systematic, or the declared all-at-once row of iter_2,
  is RESCUED inside its published errors on BOTH footings. A rescue on one footing only is reported as such.

## 3. Known answers (all iterations)

- KA0: with no correction, my exact-field V reproduces QX4 iter1.json V_exact (AGC; Malin 1 A2 run) to 1e-3
  relative at every ring, and chi2 to 1 %. If KA0 fails, no label is formed.
- Ladder line 1 % (above). A ladder miss tags the row NO VERDICT (convergence).

## 4. MUTATE (every iteration)

Each iteration names a MUTATE in its file: the same correction with the wrong sign (or a planted input for iter_3).
It must bite: the wrong-sign chi2 must exceed the uncorrected exact-field chi2 on both footings (iter_1, 2, 4), and the
planted host must flip iter_3's label. A MUTATE that does not bite means no clean label. Outputs go to *_MUTATE.*.

## 5. Not in scope

No change of the law, a0, mu or action. No new inclination escape (UD1/UD3 graded it). No Lean file in this lane
(stated, not done). Nothing here is a verdict on a theory.
