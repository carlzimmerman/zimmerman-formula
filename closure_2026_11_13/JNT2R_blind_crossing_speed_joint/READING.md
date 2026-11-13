# JNT2R READING (frozen): the crossing-speed joint, blind build

Committed alone, before any JNT2R script exists and before any number of this joint has been computed in this lane.
TEST lane. Adopts nothing, relabels nothing, registers nothing. Two footings, canonical (a0 9.3603e-11) and alt
(1.1312e-10 m/s^2), graded separately and never pooled. Cold dark energy is a gravitating field component; no particle is
added. kappa = 1/2 and the share X = 5.41 are FITTED. The family (law inside f x R_fold, reference outside) is post hoc to
FRZ1's forest fail; nothing here can be a pass of the theory, and a hit is a hit on a post hoc family.

## 0. What was read before this freeze, and blindness

- The lemma `fable52_push/SHAPE_search/route_D_dark_energy_column.md` (section 3.3, the C5 block of its check script and
  its printed output). FLD1's folder listing and its runs directory as loaded by FZS1 / SRJ1.
- SRJ2: FROZEN_CRITERIA, RESULT, RERUN_AND_IDS, all six scripts. SRJ1: RESULT (head), `srj1.py` lines 1 to 270.
  JNT1: RESULT. SRH1: RESULT (head), the FGRID line of `srh1_lens.py`. SRJ3: RESULT (head). SRF1 RESULT (head), SRF1R
  RESULT_BLIND (head). FZS1 `fzs1_hm.py` lines 30 to 70. FRZ1 `frz1_hm.py` (grep of constants). The FLD1 loaders
  `rc100()` and `sparc()` and the header line of the RC100 table (two data rows).
- The memory files named in the brief, and the auto-loaded memory index (MEMORY.md) that the session shows at start. That
  index has no JNT2 entry.
- **JNT2 seen by accident:** only the folder name `closure_2026_11_13/JNT2_crossing_speed_joint` in a plain `ls` of
  `closure_2026_11_13/` (also `JNT1R_blind_massive_spiral_regrade`). No file in it was listed or opened. One `git log`
  call that would have touched `closure_2026_11_13/` was refused by the harness before it ran; nothing was printed.
- No number of this joint was computed. The hand numbers in section 9 are from the lemma's constants and the data's
  ranges only.

## 1. v* and its scaling (how the lemma is read)

- The lemma's clustering relation `v^3 = 10 G M H` is the 200 rho_crit virial convention: M200 = v200^3 / (10 G H).
  With M = (1 + X) M_b it meets the law's `v^4 = G M_b a0` at `v* = a0 / (10 (1 + X) H)`. Today, with the lemma's H0 =
  67.4 km/s/Mpc: 669 / 808 km/s (KA1 recomputes this in SI).
- **Redshift scaling (the brief's):** v*(z) = v*(0) H0 / H(z), a0 held constant, H(z) = H0 sqrt(Om (1 + z)^3 + OL) with
  the lemma's OL = 0.6847, Om = 1 - OL (flat; radiation neglected). The same H(z) is used on both footings.
- **The boundary in baryon mass.** Both relations rise with M_b, so a system's lemma speed is above v*(z) exactly when
  M_b > M_b*(z) = v*(z)^4 / (G a0), which scales as (H0 / H)^4. KA4 checks that the two forms give the same boundary.

## 2. Which speed of each system is compared with v*(z)

- **Primary: the lemma's model virial speed** `v_cl = (10 G H(z) (1 + X) M_b)^(1/3)`: the virial speed of the system's
  cosmic-share halo. It is equivalent to the law's flat speed (G M_b a0)^(1/4) at the boundary. **M_b is the baryon mass
  the record already uses to set that system's fold radius**, so R_set and the membership see one mass:
  - SPARC: FLD1's M_b (0.5 L36 + 1.33 M_HI) for line (a); PD1's M_b (`Mbs` from the baryon curve) for line (b);
  - RC100: the table's log M_bar at the disc's z;
  - KiDS: M_b = k M_gal at the fitted k, at z_lens; the lens table switches at nodes (log M_b, z) with log M_b > log
    M_b*(z) (SRJ2's node scheme, my boundary);
  - forest: FZS1's `Mb_fold(hb)` at the bin's z (galaxy-regime haloes (1 - FB) M_ta / X; others FB M200c), in Msun;
  - X-COP and groups: SRJ1's fold mass M200 / (1 + X) from RB1's anchored M200, at the system's z.
- **Bracket B-meas (measured speed), reported:** SPARC Vflat (rows with Vflat = 0 use the largest observed V); RC100
  Vc(R_e); X-COP and groups v500 = sqrt(G M500 / R500) (groups: Lovisari M500, R500; X-COP: M500 = 500 rho_crit(z) 4 pi
  R500^3 / 3 with SRJ1's rho_crit). KiDS and the forest have no measured speed: primary only.
- **Bracket B-halo (the record's halo virial speed), reported:** SRJ2's v_vir of FRZ1's halo (galaxies: M_ta = X M_b h /
  (1 - FB); forest: v_vir(hb); clusters and groups: v200 of RB1's M200), compared with v*(z) instead of v_stiff.
- A bracket that changes any row's mark at any grid f puts **FRAGILE** beside the word and names the crossing. The word
  stays the primary's.

## 3. The joint as computed

Inside R_set = f x R_fold (FLD1, FZS1's `rset_com` / SRH1's / SRJ1's R_set, capped at r_ta) of a system with v_cl <=
v*(z): the record's law layout (FRZ1 mode "B", unchanged, including its own internal fc and W), with FZS1's junction s at
R_set. Outside R_set, and at every radius of a system with v_cl > v*(z): the reference layout (FRZ1 mode "Rb"; RB1's
ZN4 reference for clusters; SRH1's f = 0 profile for lenses). Membership, boundary and assembly are this lane's code; the
row machinery is copied from SRH1, SRJ1 and SRJ2 (executed read-only from their own paths where they do so).

**f grid: 0.75, 1.00, 1.25, 1.5, 2, 3.** f = 0 is run as the reference check.

## 4. Rows and lines (unchanged from the lanes that own them)

- **Membership table** (reported, every f): count on each side of v*(z) for SPARC (both M_b), RC100, KiDS lens classes
  (late / early, at each config's fitted k, host-free 1.0 R_h set), X-COP, groups, and the forest's haloes per DESI z bin
  with the boundary mass; under the primary and both brackets.
- **G1 forest, matter level** (FZS1 / SRJ2 machinery, DESI DR1 P1D 755 points, full covariance): holds iff Delta chi^2
  <= 4, the split applied per halo at each bin's z. Flux-level readings of SRF1 / SRF1R are carried beside it, ungraded.
- **G2 RC100** (SRH1's line): holds iff 2.2 R_e <= R_set for all 100; a disc above v*(z) has R_set = 0 and is not
  covered. Graded as a coverage line. Carried, not recomputed: SRJ3 / SRJ4 found that RC100's single R_e point has no
  power to test the reference layout on such discs.
- **G3 SPARC** (SRH1's line): (a) every R_last <= R_set(0, M_b); if (a) fails, (b) PD1's P2-SPARC line with R_trunc = R_set
  (rms <= 0.0660 and |mean| <= 0.05, all and massive tail), galaxies above v* at g = g_N (SRJ2's graded form).
  Data test for SPARC galaxies above v* (JNT1's row S lines) applies only if any galaxy is above; n < 5 is NO POWER.
- **G4 KiDS lensing by type** (ONE1's gate as SRH1 / SRJ2 ran it, 1.6 R_h veto, KO1 ties, k fitted): |z| <= 2 for all,
  late, early; chi^2 <= 9.49; type difference |z| <= 2.
- **Clusters (X-COP) and groups (Lovisari)** (RB1's gates as SRJ1 ran them): (a) q at r_last CONSISTENT; (b) shape bins
  |D| <= 0.10 dex; (c) groups q at R500 CONSISTENT. A system below v*(z) gets SRJ1's `make_system` at f; above, f = 0.
  The inherited R500 aperture bracket is reported and sets FRAGILE as in SRJ1 / SRJ2.

## 5. Marks per row and f

- **TRIVIAL:** every system graded on the row is above v*(z) (joint = reference by construction), or the joint is within
  SRJ2's tolerances of the reference (G1 Delta chi^2 < 1; G4 every z within 0.10 and chi^2 within 0.10 of f = 0).
- **EQUAL TO THE LAW:** no system on the row is above v*(z) (no lens-table node above, for G4), so the joint equals the
  no-split settled family (SRH1 / SRJ1) at that f. Checked numerically at f = 1 against TW-N.
- **NO POWER:** the row cannot weigh the joint: (i) the deciding set has fewer than 5 systems; or (ii) the owning lane
  recorded the statistic as NO POWER (carried); or (iii) the row's mark is the same for the reference (f = 0), for the
  law everywhere (TW-N at f = 1) and for the joint at every grid f. A NO POWER row is reported and does not enter the
  window. TRIVIAL and EQUAL TO THE LAW rows with power do enter it.

## 6. Labels per footing

- **NO VERDICT:** a known answer or check fails, a required twin does not bite, a row cannot be evaluated, or the
  window is non-empty but every powered row in it passes only TRIVIALLY.
- **JOINT COMPLETE ON POWERED ROWS [f window]:** the grid f values at which every powered row passes, provided at least
  one powered row there passes non-trivially. A HIT, not a pass; post hoc family; kappa and X fitted.
- **JOINT FAILS ON <rows> (on data / on coverage):** the window is empty. Named: the rows that fail at every grid f, and
  for each f the failing rows. A coverage fail (G2, G3a) counts as a fail.
- Reported beside, not graded: the same window with coverage-only lines (G2, G3a without (b)) set aside.

## 7. Twins (each must bite; each writes `*_MUTATE*` outputs and exits 1) and known answers

- **TW-V, SRJ2's boundary** (v_vir of FRZ1's halo > 265.8 / 288.1 km/s, constant in z), f = 1: must reproduce SRJ2's
  stored values: G1 0.048 / 0.081 (+- 0.01), G2 covered 69 / 78, G3(a) 172 / 175, G4 early z +2.012 / +2.037 (+- 0.005),
  clusters and groups equal to the reference; i.e. SRJ2's words at f 1 (FAILS ON G2, G3, G4 / G2, G4). Bites iff it
  reproduces them and its membership differs from the primary's on at least one row.
- **TW-N, no boundary**, f = 1: must reproduce FZS1 / SRH1 G1 38.741 / 36.658 (+- 0.01), SRH1's G2 f_min 0.391237 /
  0.391383, SRH1's stored G4 f1 row (+- 0.005 z, +- 0.01 chi^2) and SRJ1's X-COP shape bins at f 1 (+0.153 / +0.144 first
  bin, +- 0.002), FAILS. Bites iff it reproduces them and a row's mark differs from the primary's at f = 1.
- **TW-H, boundary halved** (v*/2) and **TW-D, boundary doubled** (2 v*), f = 1: each bites iff a row's mark at f = 1
  differs from the primary's, or a graded statistic moves by more than its TRIVIAL tolerance (G1 1; G4 z 0.10; X-COP bin
  0.05 dex; q median 0.05), against the primary at f = 1.
- **KA1:** v*(0) = 669 / 808 km/s recomputed in SI from a0, X and H0 (to +- 1 km/s).
- **KA2:** one SRH1 number with its boundary (none): G1 38.741 / 36.658 via TW-N. **KA3:** one SRJ2 number with its
  boundary: G1 0.048 / 0.081 and G4 early +2.012 / +2.037 via TW-V.
- **KA4:** M_b*(z) from v_cl and from v_f agree to 1e-10; f = 0 gives G1 0 (1e-10) and G4 = SRH1's f0 row; M_ta
  conserved and M_S non-decreasing under the joint at z 3 (FZS1's KA-M), 1e-9; SRJ1's K1 (f = 0 against `rb1.json`) 1e-6.

## 8. What is left out

The weak-lensing amplitude, hosted dwarfs, the Milky Way rows, the flux-level forest (carried only), a data fit of RC100
discs above v* (carried NO POWER), any bracket on X (56 to 59) in FRZ1's halo, any bracket on H(z) beyond the lemma's.

## 9. Expectation and hand estimate (may be wrong)

- KA1 by hand: H0 = 2.1843e-18 /s; 10 x 6.41 x H0 = 1.4001e-16 /s; v* = 9.3603e-11 / 1.4001e-16 = 6.69e5 m/s and
  1.1312e-10 / 1.4001e-16 = 8.08e5 m/s. M_b*(0) = v*^4 / (G a0) = 1.6e13 / 2.8e13 Msun (log 13.21 / 13.45). Then
  log M_b* is about 12.2 at z 1, 11.3 at z 2, 10.9 at z 2.5, 11.1 at z 2.2, 10.6 at z 3 (canonical; alt +0.24 dex).
- SPARC: no galaxy above (largest M_b near 3e11). G3 EQUAL TO THE LAW, holds at every grid f (SRH1's f_min 0.467).
- RC100: some massive discs at z > 2 lie above on canonical (my guess 3 to 15), fewer on alt (0 to 5). Any one makes G2
  fail on coverage at every f. Under B-meas (Vc 250 to 350 km/s against v* about 220 km/s at z 2) many more lie above.
- KiDS: no lens and no table node above (boundary near log M_b 12.7 at z 0.5). G4 equals SRH1's no-split rows: FAILS at
  0.75 and 1.00 (early +2.14, +2.00), PASSES from 1.25 up. EQUAL TO THE LAW. SRH1R found this gate cannot see f.
- X-COP: all above (fold M_b near 1e14). TRIVIAL hold, FRAGILE by the R500 bracket.
- Groups: below on alt; on canonical v200 up to 666 km/s against v*(z) near 660 to 669, so 0 to 2 above. They get SRJ1's
  law layout: q near 0.62 to 0.65, CONSISTENT at every f, as is the reference: NO POWER by rule (iii).
- Forest: with FZS1's Mb_fold the primary split at z 2.2 to 4.4 falls close to SRJ2's VST split, so G1 is near SRJ2's
  (0.05 / 0.08 at f 1, 0.4 / 0.6 at f 2); f 3 likely still under 4. TRIVIAL or near it at every f.
- **Likeliest labels:** canonical JOINT FAILS ON G2 (coverage), every f (70 %). Alt: FAILS ON G2 if any disc is above
  (50 %), else JOINT COMPLETE ON POWERED ROWS [1.25, 3] resting on G4 alone (law-equal) with TRIVIAL forest and clusters.
  Coverage-free reading: [1.25, 3] on both footings. TW-D bites through X-COP (fold M_b near the doubled boundary,
  log 14.4) and the forest; TW-H bites through RC100 and KiDS.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
