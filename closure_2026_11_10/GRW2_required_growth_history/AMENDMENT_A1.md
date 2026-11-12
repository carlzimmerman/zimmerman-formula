# GRW2 AMENDMENT A1: three MUTATE arms restated, and one node added

**POST HOC in the sense that the criteria (1863e717a8) was written first, but no GRW2 number has been computed.** What has
been computed so far is only the replay of other lanes' numbers through this lane's intended paths (SRH1's G1 at f = 1 and
0.5, SRH1's G4 at f = 1.00 and 1.25, FLD1's R_fold), which are the known answers of section 5, not graded rows. No
required-history interval, no per-bin forest limit, and no value of C2 to C5 under any history exists yet.

Committed alone, before the graded run.

## Why

Three of the four MUTATE arms of section 5, as first written, point at quantities the criteria's own text already shows
cannot move:

- **MU2 as written: "H1 against H0 on C2's A; A must move by more than 0.01."** But C2 is the PR4 lensing amplitude of
  form B's **linear** content (CO1's `amp_fit` on `I2.X_of(M)` from CLASS). The 1-halo redistribution — the only thing
  that distinguishes H0 from H1 — does not enter C2 at all; it enters C4. CO1's own C2 is 0.9617 for the reference and
  0.9617 for form B. So the arm as written compares two identical numbers and cannot bite by construction, not because
  the pipeline is inert. This is a defect in my criteria, of the same kind GRW1's A1 fixed.
- **MU3 as written: "H4 against a step at z = 1.5; C3's chi^2 must change by more than 0.1."** C3 is a sum of four pulls
  at z 0.295 to 0.919. A change in the history's shape at z = 1.5 is *above* every one of those bins, so the arm tests
  the growth rate where the growth rate is not read. It is aimed at the wrong row.
- **MU4 as written: "H4 against H2 on C4's r_eff; more than 1e-4."** CO1's own r_eff - 1 for the full law layout is
  3e-5. A 1e-4 threshold is above the entire effect this row carries, so the arm asks C4 to move by three times its own
  scale.

Each of these is a threshold or a row that the criteria's own quoted numbers contradict. Restating them is not a change of
the test's target — the target in every case is still "the rows must respond to the history" — only of the row and the
threshold used to see it.

## The restatement (this is what the run grades)

- **MU2 (restated): the amplitude row must respond to the history's shape.** H4 against H2 on **C2's A**. H2 holds the
  forest's value f_F at every z, so it suppresses R_cold at z 0 to 2 as well; H4 suppresses it only at z >= 2.2. The
  CMB-lensing kernel peaks at z ~ 1 to 3, so the two differ. **Bites iff |A(H4) - A(H2)| > 1e-4.**
- **MU3 (restated): the lensing row must respond to the history at all.** H4 against H1 (form B's layout at every z) on
  **C4's r_eff**. H1 is CO1's own baseline (+0.00003 / +0.00005). **Bites iff |r_eff(H4) - r_eff(H1)| > 1e-5.**
- **MU4 (restated): the growth row must respond to the history's shape.** H4 against H2 on **C3's largest |pull|** over
  the four DESI bins. **Bites iff the largest pull differs by more than 0.01.**

**MU1 is unchanged** (the required history reversed in z must fail G1 and G4 both).

## One node added to the grid

Section 2's node list has 0.6 and 1.0 and 1.5 but no node at the G4 window's upper edge in physical units, and no node
between 1.5 and 2.0 where the required history's power-law segment does most of its turning. **Add z = 1.75.** This is a
reporting node only; it carries no gate of its own.

## What is unchanged

The family, the layout, the definition of U and L, the graded histories H0 to H6, the four independent rows and their
lines, the labels, the known answers, MU1, and the whole of section 6 (the pre-registered test). Nothing in this
amendment touches a graded number, because no graded number exists.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
