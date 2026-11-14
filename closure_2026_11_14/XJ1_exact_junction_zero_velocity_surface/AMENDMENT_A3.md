# XJ1 AMENDMENT A3 (2026-11-14, written 11:06 EST by the clock): two more settled radii for the exact junction, below the fold

Post hoc: written after the reported chains were read (matter level, lensing G4 with the s table, and A2's rotation
curves) and before any flux-level number of this lane has been read (build B's primary stage is still running; no part
has been opened except the first, for the identity of its R and J5 fields). It adds two cases. It changes nothing of
the frozen cases E1, E2, E3, Ezv, their known answers, twins, brackets or label rules.

**What was seen.**
- Matter level, record convention (`xj1_matter_*.out`), gate 4: the exact junction reads 32.2 / 78.7 at R_fold, 134.8 /
  326.9 at 2 R_fold, 212.2 / 494.5 at 3 R_fold and 176.0 / 423.3 at R_zv (canonical / alt), where FZS1's junction reads
  0.049 / 0.146 at 2 R_fold and 1.99 / 6.43 at 3 R_fold. So at matter level the exact junction is over the gate at
  every frozen radius, the fold itself included.
- Lensing G4 with the exact junction (`xj1_lens.out`): PASS at R_fold, 2 and 3 R_fold and R_zv on both footings (early
  types -0.06 / -0.19 / -0.27 / -0.19 canonical, +0.65 / +0.57 / +0.44 / +0.57 alt), where FZS1's junction fails at
  R_fold (+2.003 / +2.037).
- A2 (`xj1_sparc.out`): under FZS1's junction at z = 0 the median galaxy keeps 0.59 to 0.75 of the law's halo and
  PD1's rotation-curve gate reads PASS / PASS at f = 1.25, FAIL / PASS at f = 2, FAIL / FAIL at f = 3 and FAIL / PASS at
  R_zv (canonical / alt), with the fitted median mass-to-light ratio rising from 0.58 / 0.52 to 0.75 to 0.87.
- FLD1: every SPARC galaxy's last measured radius lies inside 0.47 R_fold(z = 0).

**Why two more cases.** With the law exact inside, rotation curves need R_set >= 0.47 R_fold today, and the matter-level
forest number says the upper edge lies below R_fold. Whether any settled radius is left between the two is the
question the frozen grid cannot answer. This re-opens f as a number read from data for the exact junction; the two
radii with no free constant (R_fold, R_zv) stay as frozen.

**Added cases (exact junction, section 1's definition unchanged):** **E0.5** (R_set = 0.5 R_fold) and **E0.75**
(R_set = 0.75 R_fold).

- Flux level, build B, a second pass with its own parts (`parts_b2/`): fields R, E0.5, E0.75 and, at the anchors, TWB2 =
  R + 2 (E0.75 - R); same boxes, seeds (0 to 3 in all 12 bins), gas, estimator, D, SE, gate and guards as the first
  pass; brackets (anchors, seeds 0 and 1) for R, E0.5, E0.75. It starts only when no more than two other heavy
  processes are alive.
- Known answers: the first pass's list, with KA-5 replaced by **KA-R2**: the R field of every second-pass part equals
  the first pass's R (same z, seed, footing) with |ratio - 1| <= 1e-6 at every mode k_v > 0; KA-E extended to the two
  new radii on the tables (same items, A1's tolerance); the control J5 and KA-C / KA-INF / TW-A are the first pass's.
  Twin TW-B2: anchors of TWB2 against E0.75's, bites if the factor is >= 2.5; it gates E0.5 and E0.75. If E0.75's anchor
  statistic is below 0.05 (too small for a ratio to mean anything) the twin is replaced by the first pass's TW-B at E3,
  and that is stated.
- Labels per case and footing: section 6's (HOLDS / FAILS / NO VERDICT, FRAGILE).
- Lane word added, per footing: **Q3, the window under the exact junction:** "A WINDOW IS LEFT: f in [0.5, <largest f
  of 0.5, 0.75, 1 that reads HOLDS>]" if E0.5 reads HOLDS; "NO WINDOW LEFT ABOVE THE ROTATION CURVES' REACH" if E0.5
  reads FAILS; otherwise "NOT RESOLVED". A window is a hit awaiting a blind re-grade, and its lower edge 0.5 is a grid
  point, not a measurement (rotation curves need 0.47 today; the forest's redshifts are 2.2 to 4.4, where no rotation
  curve of this record tests R_set).
- Reported: the matter-level number and the lensing gate G4 for E0.5 and E0.75 through the same two scripts (case list
  extended; the frozen cases' outputs are not overwritten: new files `xj1_matter2_*`, `xj1_lens2.*`).
- Hand estimate (before any number of the two cases): matter level 3 to 15 at 0.5 R_fold and 10 to 40 at 0.75 R_fold
  (canonical; alt about twice); flux level E0.5 HOLDS 60 %, E0.75 HOLDS 40 %; lensing G4 passes at 0.75 (65 %) and is
  uncertain at 0.5.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
