# GRW2 FROZEN CRITERIA: the growth history the four gates REQUIRE, graded against the independent rows

Committed alone, before any GRW2 script exists and before any GRW2 number is computed. TEST lane, quarantined. Relabels
nothing, adopts nothing, registers nothing. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), graded
separately, never pooled. Cold dark energy is a gravitating field component; no particle is added anywhere.
kappa = 1/2 FITTED; not theory closed.

**Lane id.** The brief names this lane GRW2. No earlier lane carries it (`GRW1_late_growth_baryons_and_law` is the only
GRW*). So this lane is **GRW2**.

## 0. The question, and what was seen before this freeze

**The inverse question.** SRH1 asked whether one history R_set(z, M_b) = f x R_fold(z, M_b) with a single constant f
passes the forest (G1), high-z rotation curves (G2), present-day rotation curves (G3) and galaxy lensing (G4) together,
and answered WINDOW EMPTY / WINDOW EMPTY (the gap is 1.39 / 1.45). This lane does not propose a mechanism. It takes the
law's halo as given at each epoch, frees the share, and asks:

1. **What history is REQUIRED?** At each frozen redshift node, the interval of f(z) (equivalently of R_set and of the
   settled share X_s) that the four gates jointly allow.
2. **Does any required history survive the four independent rows** — CMB lensing amplitude, DESI DR1 f sigma8, PR4
   lensing r_eff, and raw KiDS d_cold — which no gate in G1 to G4 used?
3. **Is SRH1's post hoc tilt excluded, or merely post hoc?** If merely post hoc, freeze the pre-registered test that
   would decide it, and say what data would run it.

**Seen before this freeze** (every number below is another lane's, and this lane has computed none of its own):
- SRH1's `FROZEN_CRITERIA.md` (5ed8a37ec6), `AMENDMENT_A1.md` (68969e177e), `RESULT.md`, `srh1_grade.out`,
  `srh1_tilt.out`, `srh1_lens.out`, `srh1_rc.out`, `srh1_forest_canonical.out`, `srh1_hm.py`, `srh1_lens.py`,
  `srh1_tilt.py`: G1 upper edge 0.722 / 0.725; G4 lower edge 1.004 / 1.050; gap 1.39 / 1.45; G2 lower 0.391 / 0.391;
  G3(a) coverage 0.467 / 0.467; G3 itself holds at every grid f; the three A1 tilt cases (beta -1 f0 1.5 and 2.0,
  beta -0.5 f0 1.25) pass all four on both footings; the frozen tilt grid opens no window; the KiDS lens redshifts
  (median 0.31, 5-95 % 0.16 to 0.43).
- CO1's `RESULT.md`, `co1.out`, `co1_linear.out`, `co1_shear.out`, `co1_hm.py`, `co1_linear.py`, `co1_shear.py`: the four
  independent rows as form B holds them (C2 PR4 lensing amplitude A = 0.9617 +- 0.0231 canonical / 0.9564 +- 0.0230 alt,
  shape chi^2 8.56 against a line 18.48, 9 bandpowers; C3 DESI DR1 f sigma8 chi^2 2.23 / 2.20 canonical and 2.29 / 2.23
  alt over 4 bins, line every |pull| <= 2; C4 PR4 lensing with the redistribution, r_eff - 1 = +0.00003 / +0.00005
  against a line 0.0481; C5 raw KiDS d_cold +1.15 / +2.21 against a line < 9), and R_cold(k) at z 0 (k 1 / 3 / 5:
  1.006 / 1.051 / 1.090 canonical, 1.010 / 1.088 / 1.159 alt).
- GRW1's `RESULT.md`, `grw1_lib.py`, `grw1_obs.py`: T-A FALLS SHORT / FALLS SHORT, T-S FALLS SHORT AND OVERSHOOTS;
  the z-dependent Limber machinery (`S_of_z`, `ratio_interp`, `S_of_kz`, `lensing`) and GAL1's PR4 amplitude rule.
- FRZ1, FZS1, FLD1, ONE1, PD1, HLF1 as SRH1 named them, and their stored outputs.
- **No GRW2 number of any kind has been computed.** In particular no required-history interval, no per-bin forest
  upper limit, and no value of C2 to C5 under any history.

## 1. The family (SRH1's, unchanged, with f freed from a constant to a function of z)

1. **R_set(z, M_b) = f(z) x R_fold(z, M_b)**, f one function of redshift only; the mass dependence is R_fold's, as SRH1
   froze it (FLD1's `rfold_kpc`: FLD1's primary run files, linear in z on each stored series, log R linear in log M_b
   between table masses, M_b^(1/3) outside 6.5 to 12; capped at the halo's r_ta). A mass dependence of f itself is
   reported at log M_b = 9.4, 10.7, 11.5 and 12 and is **not** graded (SRH1 froze f mass-independent).
2. **The layout is FZS1's rule, unchanged** (SRH1 section 1 item 2): M_S(r) = Bar(r) + s C_B(r) for r <= R_set and
   Bar(r) + C_R(r) for r > R_set, s = C_R(R_set) / C_B(R_set). C_B is the law's (form-B) cold layout, C_R the cold
   reference's. R_set = 0 gives the reference; R_set = r_ta gives FRZ1's form-B layout.
3. **f(z) is represented on a frozen node grid** (section 2) and is log-linear in log(1 + z) between nodes everywhere
   this lane needs it at a z between nodes (the halo model, the Limber integrals, the KiDS row).
4. **The share footing.** Beside f, every required-history number is reported on the second footing of the brief:
   **X_s(z, M_b) = C_R(R_set) / C_R(r_ta)** at the same z and M_b — the fraction of the halo's cold mass that has
   settled into the law's layout, the reference's own cumulative cold mass at R_set over its value at r_ta. X_s = 0 at
   R_set = 0 and 1 at R_set = r_ta. Computed from FRZ1's `halo_basics_z` (Duffy c(M, z), Delta_ta(z)) at that z.

## 2. The frozen node grid, and the required interval at each node

**Nodes (frozen).** z = 0; 0.16; 0.31; 0.43; 0.295; 0.510; 0.706; 0.919; 0.6; 1.0; 1.5; 2.0; 2.5; and the twelve DESI
P1D bins 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4.

**Required interval I(z_n) = [L(z_n), U(z_n)]** (this is the deliverable of part 1):

- **U(z_n) at the twelve forest nodes (G1, upper).** The largest f such that the history with f(z_n) = f and f = 0 at
  every other node gives G1 Delta chi^2 <= 4. (f = 0 means R_set = 0, the cold reference: R_cold = 1 identically,
  SRH1's KA-0.) Found by bisection, then verified by one direct recomputation of `ratios_S` at the crossing. Because
  Delta chi^2 is a quadratic form in the per-bin residual vectors with a positive-definite covariance, and the residual
  at each bin is monotone in that bin's f, U(z_n) is a **necessary** upper limit on f(z_n) in any passing history. The
  monotonicity of Delta chi^2 in each single-bin f is **checked, not assumed** (section 5, KA-3); if it fails at any
  node, U(z_n) is reported as "not a bound" and that node drops out of the envelope.
  - The twelve U(z_n) are each a *single-bin* bound. The **joint** forest bound is reported beside them: the largest
    constant f over all twelve bins with Delta chi^2 <= 4 (SRH1's 0.722 / 0.725, re-verified here).
- **L(z_n) at the lens nodes 0.16, 0.31, 0.43 (G4, lower).** ONE1's KiDS host-free row, exactly as SRH1 graded it
  (G-K1 |R_s,data - R_s,model| <= 2 sigma for all / late / early at the 1.6 R_h veto, KO1 tie rule, k fitted on the
  inner window; G-K2 profile chi^2 <= 9.49; G-K3 type difference <= 2 sigma), run with f(z) = f constant over the lens
  window (ONE1's table spans z 0 to 0.85, and the lens sample is z 0.16 to 0.43). L(z_n) is the smallest such f that
  passes. Because the stack cannot resolve f below the innermost KiDS radii, L is reported as the same number at all
  three nodes, and the reading is **a bound on f over the whole window z <= 0.85**, not on f at 0.31 alone. Disclosed.
- **L(z_n) at the RC100 nodes 0.6, 1.0, 1.5, 2.0, 2.5 (G2, lower).** FLD1's line: 2.2 R_e,i <= f(z_i) R_fold(z_i, M_i)
  for every RC100 galaxy in that node's z bin. Reported at each node; the 4 R_e line is reported, not graded.
- **L(0) (G3).** SPARC coverage 2.2 R_last <= f(0) R_fold(0, M_b) for all 175 galaxies; and PD1's truncated-curve line
  (rms <= 0.0660, |mean| <= 0.05, and the same for Vflat >= 250 km/s) evaluated at f(0). G3 passes iff coverage holds or
  PD1's line holds; SRH1 found G3 holds at every grid f, so L(0) is reported and is not expected to bind.
- **The DESI f sigma8 nodes 0.295, 0.510, 0.706, 0.919 carry no gate.** They are where the independent row C3 reads the
  history, and the envelope there is the interpolation of the nodes on either side.

**The envelope is empty at a node iff L(z_n) > U(z_n) there.** The envelope is reported in full as a table, on both
footings, on all three footings of the history (f, R_set in kpc at log M_b = 10.7, and X_s at log M_b = 10.7).

**The crux number (frozen).** G_req = L(0.31) / U(2.2), the factor by which R_set / R_fold must grow between the first
forest bin and the lens epoch. Reported with its two ingredients.

## 3. The graded histories

Each is graded on G1, G2, G3, G4 and on the four independent rows C2 to C5. f(z) is log-linear in log(1 + z) between
the defining points.

| id | f(z) | what it is |
|---|---|---|
| H0 | 0 at every z | the cold reference everywhere; the lower comparator |
| H1 | R_set = r_ta at every z (f = inf) | form B's layout, **CO1's baseline**; the upper comparator |
| H2 | f_F at every z, f_F = the joint G1 edge (SRH1 0.722 / 0.725, re-verified) | the most settling the forest allows, held at all z |
| H3 | f_L at every z, f_L = the G4 edge (SRH1 1.004 / 1.050, re-verified) | the least settling lensing allows, held at all z |
| **H4** | **f_L for z <= 0.85; a power law in (1 + z) from f_L at z = 0.85 to f_F at z = 2.2; f_F for z >= 2.2** | **the required history (primary).** It takes the maximum settling the forest allows at every z >= 2.2 and the minimum lensing allows at every z <= 0.85, and joins them by the steepest single power law through that pair. |
| H5 | 1.5 (1 + z)^-1 (both footings), and 1.25 (1 + z)^-0.5 | SRH1's A1 cases: the post hoc tilt being checked |
| H6 | 1.0 (1 + z)^-1 | SRH1's frozen tilt case that fails; the control for "post hoc" |

H4, H5 and H6 are the histories that carry the verdict. H0 to H3 are comparators and brackets; they are reported and
never in the window.

## 4. The independent rows (the survival test), and what counts as surviving

CO1's four rows, recomputed with the history's own R_cold(k, z) in place of CO1's z = 0 R_cold applied at all z.
Reuse: CO1's `co1_linear.py` and `co1_shear.py` machinery, GAL1's PR4 amplitude rule through QX3 iter2's `iter2`,
CE2's DESI transcription, PD1's KiDS loader, all read-only and executed from their own paths.

- **C2 PR4 lensing amplitude and shape.** A = data / prediction with GAL1's best-amplitude rule; shape chi^2 over the 9
  bandpowers. **Passes iff |A - 1| <= 2 sigma_A and chi^2_shape <= 18.48.** CO1's own values are 0.9617 +- 0.0231 /
  0.9564 +- 0.0230 and 8.56 / 8.56.
- **C3 DESI DR1 f sigma8, 4 bins (z 0.295, 0.510, 0.706, 0.919).** Form B's f sigma8 against the published ratios, with
  the history's R_cold(k, z) inside sigma8(z) and therefore inside its z-derivative. **Passes iff every |pull| <= 2**
  (SF and SF+BAO); chi^2 over 4 bins reported. CO1's own: 2.23 / 2.20 canonical, 2.29 / 2.23 alt, largest pull 1.22 /
  1.23.
- **C4 PR4 lensing with the redistribution, r_eff - 1.** The history's R_cold on the Limber kernel. **Passes iff
  |r_eff - 1| <= 0.0481.** CO1's own: +0.00003 / +0.00005.
- **C5 raw KiDS-1000, d_cold (104 points).** **Passes iff d_cold < 9** (CO1's `klass` line). CO1's own: +1.15 / +2.21.
- **A history survives iff all four pass on that footing.**

**What the four rows are sensitive to, stated now.** C2 and C4 integrate R_cold over a kernel that peaks at z ~ 1 to 3;
C3 reads sigma8 and its growth at z 0.3 to 0.9; C5 reads z 0.1 to 1.2. A required history suppresses R_cold below 1 at
z 2.2 to 4.4 (SRH1's z = 0 table reads 0.992 at k 1 in the forest's range) and raises it to the law's level at z < 1.
So the expected direction is: **C2's A rises toward 1 (form B currently predicts 3.8 % too much lensing, -1.66 sigma),
and C3's f sigma8 rises** (form B is already +1.22 sigma high on BGS). The survival test is whether those moves stay
inside the lines. Which way each row moves is **computed, not assumed**; if a row moves the other way the lane says so.

## 5. Labels, known answers, MUTATE

**Labels (per footing).**

- **REQUIRED HISTORY SURVIVES** iff the envelope is non-empty at every node where a gate binds, **and** H4 passes
  G1 to G4, **and** H4 passes C2, C3, C4 and C5.
- **REQUIRED HISTORY EXCLUDED** iff the envelope is empty at some node where two gates bind, or H4 fails G1 to G4, or
  H4 fails any of C2 to C5. The RESULT names the row that fails and the size of the miss.
- **NO VERDICT** iff a known answer fails, a MUTATE arm does not bite, or a row cannot be evaluated.
- **The tilt verdict (separate, printed beside the label).**
  - **TILT EXCLUDED** iff H5 and H6 both fail at least one of C2 to C5 on both footings, or iff H5 fails G1 to G4 here
    (a re-grade of SRH1's A1 cases on this lane's own path).
  - **TILT POST HOC, NOT EXCLUDED** iff H5 passes G1 to G4 here and passes C2 to C5.
  - **NO VERDICT on the tilt** iff H5 cannot be evaluated or a known answer fails.
  - A third line is printed either way: **the pre-registered test** (section 6) that would decide it, frozen here.

**Known answers.**

- **KA-1 (the anchor).** H1 (f = inf) through this lane's path reproduces CO1's four rows to CO1's own tolerance:
  C2 A 0.9617 +- 0.0231 / 0.9564 +- 0.0230, shape chi^2 8.56 / 8.56; C3 chi^2 2.23 / 2.20 canonical and 2.29 / 2.23
  alt, largest pull 1.22 / 1.23; C4 r_eff - 1 +0.00003 / +0.00005; C5 d_cold +1.15 / +2.21. Line: 1e-3 relative on A,
  chi^2, r_eff - 1 and 0.05 absolute on d_cold.
- **KA-2 (the forest gate).** This lane's path reproduces SRH1's G1 at f = 1 (38.741 / 36.658), at f = 0.5
  (0.189 / 0.185) and at R_set = r_ta (9916.246 / 9008.690); and R_set = 0 gives 0.
- **KA-3 (monotonicity, the assumption behind U(z_n)).** At three nodes (2.2, 3.0, 4.4) and five f (0.4, 0.7, 1.0, 1.5,
  2.0), Delta chi^2 of the single-bin history is non-decreasing in f. If it is not, U is reported as not a bound there.
- **KA-4 (R_fold).** FLD1's R_fold at z 0 / 2 / 4 for log M_b 9.4, 10.45, 10.7, 10.9 reproduces FZS1's KA-F.
- **KA-5 (the lensing row).** H1 through this lane's KiDS path reproduces ONE1's stored primary (model R_s 1.003 /
  0.847, z -1.14 / -0.23 at 1.6 R_h, gate PASS / PASS) within SRH1's KA-G4c tolerance (0.13 / 0.07 of it).

**MUTATE (each must bite on both footings).**

- **MU1, the required history reversed in z:** f_F for z <= 0.85 and f_L for z >= 2.2 (the same pair, the opposite
  order). G1 must fail **and** G4 must fail. This is the arm that says the gates really do order the epochs.
- **MU2, the amplitude row must respond:** H1 against H0 (the reference). C2's A must move by more than 0.01.
- **MU3, the shape of the transition must be visible:** H4 against the same pair of endpoints joined by a step at
  z = 1.5 instead of a power law. C3's chi^2 over 4 bins must change by more than 0.1.
- **MU4, the history must be visible to lensing:** H4 against H2 (f_F held at every z). C4's r_eff must differ by more
  than 1e-4.

## 6. The pre-registered test for the tilt (frozen here, whatever the label comes out)

The tilt is a two-parameter family f = f0 (1 + z)^beta fitted to four gates after they were seen. This lane will report
whether it is excluded by the independent rows. Whatever that says, the following test is frozen now, in the form it
would be run, so that running it is not a choice.

- **Grid (frozen now):** f0 in {0.75, 1.0, 1.25, 1.5, 2.0, 2.5}, beta in {-1.5, -1.25, -1.0, -0.75, -0.5, -0.25, 0.0},
  42 cases, both footings, each graded on G1 to G4 and on C2 to C5 by this lane's own code. No case is dropped, none is
  added after the run, and no sub-grid is selected after the fact. A window that exists only for cases added after a
  number was seen is reported as post hoc and does not count.
- **Statistic (frozen):** ONE1's model R_s at 1.6 R_h, for all / late / early, with its own k fit, veto and tie rule,
  evaluated on **a lens sample split at z_l = 0.5** (two stacks, ONE1's estimator on each, its own jackknife errors).
  The discriminating quantity is Delta R_s = R_s(z_l > 0.5) - R_s(z_l < 0.5).
- **Decision rule (frozen):** the tilt is confirmed only if, for at least one grid case that also passes C2 to C5,
  |Delta R_s| exceeds 2 sigma of the split statistic **and** carries the sign the case predicts; it is excluded if every
  grid case that passes C2 to C5 predicts |Delta R_s| below 1 sigma. Anything between is NO VERDICT, and the run says
  which.
- **The data that would run it, and why it is not run here:** ONE1's KiDS lens sample is z 0.16 to 0.43 (median 0.31),
  so it contains no lens above z_l = 0.5. Running the test needs a KiDS-like galaxy-galaxy lensing stack with lenses at
  z 0.5 to 0.9 (KiDS-1000's own deeper lens bins, HSC-Y1 / HSC-Y3, DES Y3's redMaGiC high-z bin, or BOSS / eBOSS lenses
  with an overlapping source catalogue), together with ONE1's host-free veto applied at that redshift. **None of those
  catalogues is in this repository**, so the test is frozen and not run. Second best, already in the repository: the
  CMB-lensing and DESI f sigma8 rows (C2, C3), which read the same history integrated over z; this lane computes their
  response and reports the predicted separation between the tilt and a constant f, so that the same decision rule can be
  applied to them when the split lensing stack exists.
- **What the tilt would have to explain, stated now:** a settled radius that grows by a factor of at least G_req more
  than FLD1's R_fold between z 2.2 and z 0.3. FLD1's spherical fold gives no such extra growth, and nothing in the
  record derives it. GRW1 found that baryons plus the law do not build late structure with a warm cold component.

## 7. Reported, not graded

- The envelope at every node, on all three footings of the history (f, R_set in kpc, X_s), at log M_b = 9.4, 10.7,
  11.5, 12.
- R_fold(z, M_b) itself, so the reader can rescale.
- The joint forest bound beside the twelve single-bin bounds; the per-bin Delta chi^2 of every graded history.
- The z = 0 redistribution R_tot at k 1 / 3 / 5 for every graded history, beside CO1's 1.006 / 1.051 / 1.090.
- The mass dependence of the envelope (f free to depend on M_b): the ratio of the required U at log M_b 9.4 to that at
  12, reported at z 2.2 and 0.31.
- The 4 R_e line of G2, and PD1's truncated-curve line, at every graded history.
- What a uniformly rescaled R_fold does to the envelope (SRH1's disclosure: a uniform rescale cancels in the gap; only a
  change in the redshift dependence moves it).

## 8. What counts against (stated now)

- An envelope that is empty at any node where two gates bind.
- A required history that moves C2 or C3 outside its line.
- A required history that survives only because the rows are too wide to see it: the RESULT states the size of the move
  against the line for each row, so a reader can judge this.
- The required history is a *required* history, not a derived one. Nothing in this lane produces it; the joint (the
  equation that takes the cold component from falling dust to the settled halo) stays missing, as in SRH1.
- The tilt's three passing cases are SRH1's A1, chosen after the gates were seen.
- Inherited from the reused lanes: G1's halo model (Tinker 2008 z-scaling and Duffy c(M, z) from memory, PROVISIONAL;
  present-day baryon shapes; a linear 1D projection). G4's neighbours keep ONE1's counted-once halos and are not
  re-laid out; G4 keeps ONE1's central-point baryons. G2's 2.2 R_e is RC100's sample mean extent. C3's f sigma8 is a
  linear-theory quantity and the halo model's R_cold is a halo-model quantity; the product is a hybrid, as in CO1.
- R_cold(k, z) is computed at the node grid and interpolated in log(1 + z); below KK[0] it is clamped to 1 (the 2-halo
  term is 1.000000 there, CO1's KA).

## 9. Hand estimates (before any number)

- **The envelope.** U(2.2) near 0.9 to 1.1 and rising with z (the forest's bins carry different weight: the low-z bins
  have more power, so I expect the tightest U at 2.2 to 2.6, loosening toward 4.4). U(3.0) and U(4.4) well above 1.
  L(0.31) = 1.004 / 1.050 as SRH1 interpolated. L(0.6 to 2.5) from RC100, near 0.4 to 0.7, nowhere binding against L(0.31).
  So G_req near 1.1 to 1.4, close to SRH1's 1.39 / 1.45 but computed per bin.
- **The independent rows.** C2: A rises by 0.2 to 1.5 % (the suppression is at k 0.1 to 1 and z 2 to 4, inside a kernel
  that peaks near z 2), so A moves 0.963 to 0.977 — **still inside the line and closer to 1**. C3: f sigma8 rises by
  under 1 % at z 0.3 to 0.9 (R_cold is within 1 % of the law's at k < 0.3), so the largest pull goes from +1.22 to about
  +1.3 — **still inside 2**. C4: |r_eff - 1| stays under 1e-3, against 0.0481. C5: d_cold stays near +1.15 / +2.21.
  So my expectation is **REQUIRED HISTORY SURVIVES / SURVIVES, with TILT POST HOC, NOT EXCLUDED**.
- **Where I could be wrong.** If R_cold at f < 1 is *below* 1 at k 0.1 to 0.5 (SRH1's z = 0 table reads 0.992 at k 1 in
  the forest's range), the suppression at z 2 to 4 is bigger than I think, and C2's A could move by several per cent
  and go over 1.0462 (the upper edge of the line) — then the required history is excluded by the row it helped. That is
  the failure mode I would watch for, and it is the one the lane is built to see.

## 10. Files (planned)

- `grw2.py` -> `grw2.json` / `grw2.out` (everything: the envelope, the graded histories, G1 to G4, C2 to C5, the known
  answers, MUTATE, the label). One thread.
- `RESULT.md`, and the label on both footings.
- Amendments, if any, as `AMENDMENT_An.md`, each committed alone, marked post hoc if any number was seen.
- Nothing is written outside this folder. The reused lanes' folders stay read-only.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
