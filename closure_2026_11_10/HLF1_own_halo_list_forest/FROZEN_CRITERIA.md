# HLF1 FROZEN CRITERIA: CO1's redistribution rows with the record's own halo list, and the forest row computed for form B

Committed alone, before any HLF1 script exists and before any HLF1 number is computed. TEST lane, quarantined. Relabels
nothing, registers nothing. Footings canonical (a0 9.3603e-11) and alt (1.1312e-10 m/s^2), graded separately, never pooled.
Cold dark energy is a gravitating field component; no particle is added anywhere. Nothing here can turn form B into a pass,
and no outcome is read as the data favouring the framework.

## 0. What is graded, and what was seen before this freeze

CO1 (`closure_2026_11_09/CO1_form_b_cosmology_computed/`, criteria 020522140a, A1 5e1496298d) labels form B's cosmology rows
ROWS HOLD / ROWS HOLD "with an inherited halo list" (NO VERDICT / NO VERDICT with M4 as frozen) and states two limits:
the halo list (Tinker 2008 mass function, Tinker 2010 bias, CFG556's c(M) = 10.14 (M / 2e12)^-0.081, CFG556's declared
baryon shapes) is not framework-native, and the Lyman-alpha forest row is not recomputed ("stays carried"). The paper's
gate table carries the forest as "carried from the cold reference" (PD1 P4: "forest Delta chi^2 0"; PD1 cites the WM1 lines).

Seen before this freeze: CO1's FROZEN_CRITERIA, AMENDMENT_A1, RESULT (all its numbers), `co1_hm.py`; CFG556's library head;
CFG596's engine and the listing of its S0 run directory; the S0 z = 0 block-mean file's shape and extremes (256^3, delta from
-1 to 7623, 7161 cells with 1 + delta >= 200); WM1's criteria line 8 and its stored MN-W forest Delta chi^2 (167379.35 /
167378.92); SS1's `forest_eval` source; QX15's stored main theta; the forest lanes' README headers (P1D1, P1D2, P1D4 all NOT
DIAGNOSTIC: the record's absolute forest models do not fit the data). No mass function, bias, ratio or forest number of this
lane exists.

## 1. What is on disk (checked before planning)

- The record's own run is CFG596's S0 run (`_external_data/cfg596_work/P0/`, L = 100 Mpc/h, 1024^3 particles, PM mesh 1024,
  seed 359, h 0.6736, omega_b 0.02237, omega_c 0.1200, n_s 0.965, sigma8 0.811: the same cosmology as CFG556's halo model).
  The engine saves z = 0 particle positions only when N <= 512, so **this run left no positions**. It left 256^3 block means
  of the particle density contrast (`dpart`) at z_i, 1, 0.7548, 0.5, 0.2562 and 0 (cell 0.390625 Mpc/h; cell mass
  5.19e9 Msun/h; particle mass 8.1e7 Msun/h).
- Other S0 runs with positions exist (N256 and N128, different seeds and resolution: cfg654 VNs / VNcs, cfg960 VS0). They
  are not the run CO1's base spectrum comes from and are not used for the graded list.
- No new simulation is run by this lane. A 1024^3 rerun with positions saved would cost about 9.3 h of wall time at 14
  threads and 42 GB resident (CFG596's own log), far over this lane's limits: it is a plan to report, not to start.

## 2. Part A: the halo list

### A.1 What "own halo list" means here

- **Finder (frozen):** spherical overdensity on the 256^3 z = 0 `dpart` grid of the S0 run. Candidates are cells that are
  the maximum of their periodic 3^3 neighbourhood with 1 + delta >= 200. In descending order of peak 1 + delta, each
  candidate's centre is the mass-weighted centroid of its 3^3 cube (periodic). Enclosed mass M(<r) is the sum of
  (1 + delta) m_cell over cells whose centres lie within r of the centre; the mean enclosed density is evaluated on r from
  0.25 to 12 cells in steps of 0.05 cells; r200m is the first r >= 0.75 cells at which it falls below 200 rho_m (linear
  interpolation between the two steps); M200m = 200 rho_m (4 pi / 3) r200m^3. A candidate whose centre lies inside r200m of
  an already accepted halo is discarded. No unbinding, no sub-cell refinement beyond the centroid.
- **Resolved range, lower end (fixed by a known answer, KA-A1, before the run is measured):** planted NFW halos with
  CFG556's c(M), M200m in {1e13, 2e13, 3e13, 5e13, 1e14, 3e14, 1e15} Msun/h, each at 8 random sub-cell centres on a uniform
  background (delta = 0), the profile continued to 2 r200m, sampled on a grid 4 times finer than 256^3 with r clipped at a
  quarter of a fine cell and the profile mass renormalised on the fine grid, then block-averaged by 4^3 (as the engine's
  block mean does). The true M200m is solved on the analytic profile plus background. **M_lo** = the smallest tested mass
  at and above which, at every tested mass, the median |M_found / M_true - 1| <= 0.15 and the largest <= 0.30. If no tested
  mass qualifies, Part A is NOT RESOLVED.
- From the mesh and cell alone (hand estimate, before any number): r200m = 2 cells at M200m about 3.5e13 Msun/h; M_lo is
  expected near 2e13 to 5e13.
- **Mass bins:** 0.25 dex wide, starting at M_lo. **M_hi** = the upper edge of the last bin, contiguous from M_lo, holding
  at least 5 found halos. The resolved range is [M_lo, M_hi]. Masses below M_lo and above M_hi keep the inherited list.
- **Own mass function:** in bin j, r_j = N_own,j / N_T,j with N_T,j = V sum over CFG556's mass grid points in the bin of
  W_M (Tinker 2008 per grid point, V = 1e6 (Mpc/h)^3). The own list is W_M x r_j inside bin j (the inherited shape inside
  the bin, the run's count for the bin).
- **Own bias:** halos of each 0.5 dex bin from M_lo (the last bin ending at M_hi) assigned to the 256^3 grid by NGP;
  b = sum Re(delta_h delta_m*) / sum |delta_m|^2 over the half-space modes with k_f <= k <= 0.2 h/Mpc (the cross ratio
  cancels the run's large-scale draw to first order); its error by a bootstrap over those modes (500 resamples, seed 1).
  The bin's measured b replaces Tinker 2010 by the ratio b / b_T (b_T the count-weighted Tinker bias in the bin) only if
  the bootstrap error is <= 20 % of b; otherwise the inherited bias stays in that bin, and that is reported as "bias not
  resolved in this bin". A_MISS and NORM_TA are recomputed from the own W_M and BIAS exactly as CO1's `set_population` does.
- **Never resolved by this run (stated, not graded):** c(M) at every mass (the scale radius of a 1e14 halo is about 0.2
  Mpc/h, half a cell; the 256^3 grid cannot see it), the baryon shapes (S0 is gravity-only), and every mass below M_lo. These
  stay inherited, and every Part A label carries the words "c(M) and masses below M_lo inherited". CO1's c(M) x 0.7 / x 1.3
  brackets remain the record's measure of that part.
- **Realisation noise (disclosed before any number):** the S0 run's large-scale power is a high draw (CO2: its starting
  spectrum is 1.48 times linear in its third bin). Halo counts in a single 100 Mpc/h box carry that draw and Poisson noise;
  the own counts are the run's counts as measured, not corrected.

### A.2 Resolved share of the rows (decides NOT RESOLVED, computed with the inherited list before the own list enters)

For each footing, CO1's primary layout with the inherited list: per mass grid point i, the contribution d_i to
R_tot - R_bar at k = 1 h/Mpc (1-halo plus 2-halo, CO1's `drivers` formula evaluated per grid point instead of per decade).
f_res = sum over i with M200m in [M_lo, M_hi] of |d_i| / sum over all i of |d_i|. Also reported at k = 3.

### A.3 The test

CO1's pipeline (copies of `co1_hm.py`, `co1_linear.py`, `co1_shear.py`, `co1_grade.py` in this folder; source named in each
header; only the population switch, file names and the PD1 path are changed) is run twice: with the inherited list
("inherited") and with the own list in [M_lo, M_hi] ("own"). Rows compared: R_cold at k 1 / 3 / 5, C4 (r_eff - 1 and the
shape chi^2 on PR4 lensing), C5 (raw KiDS-1000 d_cold, the four robust variants, the tooth), and CO1's lane label.

**Part A labels (per footing, fixed now):**
- **NOT RESOLVED:** f_res < 0.5 at k = 1, or no tested mass qualifies as M_lo, or fewer than 2 bins in [M_lo, M_hi].
- **ROWS MOVE (row, size):** otherwise, if the own list changes the C4 status or the C5 klass label or the CO1 lane label
  against the inherited run; the row and both numbers are named.
- **ROWS HOLD WITH THE OWN LIST:** otherwise. Reported beside it, never graded: the shift in d_cold and in R_cold(k = 1).
- **NO VERDICT:** any Part A known answer fails or any Part A mutation does not bite (it overrides the three above).

## 3. Part B: the forest row

### B.1 The row as the record states it

PD1 P4 (`closure_2026_11_09/PD1_phantom_is_dust/FROZEN_CRITERIA.md` line 44, RESULT.md line 113) carries "forest Delta chi^2 0"
from WM1 gate 8 (`closure_2026_11_09/WM1_warm_component_law_baryons/FROZEN_CRITERIA.md` line 76): `ss1_cosmo.forest_eval`
(`closure_2026_11_09/SS1_self_shielded_conversion/ss1_cosmo.py` lines 211-238) on DESI DR1 P1D (QMLE, blinded, md5
33d7fc21bfd3d745ed71a0bbe80ca433), with the gate **Delta chi^2 <= 4**. The statistic is a modification gate: the ratio r of
the model's linear 1D power (P_lin x R^2 projected, each model's own H(z) for the k conversion) to the reference's at the
data points, d = (r - 1) P_data, Delta chi^2 = d C^-1 d with the published covariance. It does not fit the data (the record's
absolute forest models are NOT DIAGNOSTIC: P1D1, P1D2, P1D4). The carried 0 is the cold limit: no modification.

### B.2 Which of form B's rules change the forest relative to the cold reference (written before any number)

- Rule 3: where the clock falls with the expansion the charge is pressureless dust. The IGM that makes the forest at z 2 to
  4.6 (overdensities about 0.1 to 10, outside collapsed galaxies) is in that regime, so form B's linear content there is the
  cold reference at form B's own parameters (F1A's B2 cold fit per footing).
- Rule 4 does not act on the gas as a force: under B the law is the layout of a standing clock's charge around condensed
  baryons, not a modified force (CO1 section 2). So the forest gas feels Newtonian gravity of the total mass, and nothing
  modifies its linear growth.
- Rule 5 (counted once) re-lays the cold component inside each halo's turnaround sphere. That is the only form-B-specific
  change to the matter that the forest could see. CO1 computed it at z = 0 only (R_cold(k)) and holds it in z.
- So form B's forest row is: form B's own linear spectrum, with and without the redistribution R_cold.

### B.3 The computation (per footing)

The record's pipeline is executed read-only: `ss1_cosmo.py`'s prefix up to its "run" marker in its own namespace (as WM1
does), giving `forest_setup`, `forest_eval`, `KG` (1/Mpc), `ZG`. The pipeline's reference model `M` and background `REFBG` are
replaced by form B's own: CLASS at F1A's stored B2 cold best fit (`closure_2026_11_07/F1A_primary_cmb_audit/parts/
fit_B2_<footing>_cold.json`, CO1's `class_B` settings with P_k_max raised to 210 /Mpc and z_max_pk 20, as the pipeline needs),
and its CLASS background (H in km/s/Mpc, as WM1's `class_bg`). The model is the same spectrum times Rkz^2 with
Rkz(k, z) = sqrt(R_cold(k / h_B)) (R_cold is a power ratio; the pipeline squares an amplitude ratio), R_cold from CO1's stored
`co1_hm.json` primary per footing, interpolated in ln k on CO1's grid (1e-3 to 10 h/Mpc), held flat at its end values
outside it.

- **Reading H (held, CO1's frozen convention):** Rkz independent of z.
- **Reading F (the record's fade, CFG592 `Pmat(boost="fade")`):** R - 1 scaled by (1 - z) for z <= 1 and zero above; at the
  forest's redshifts this is R = 1 exactly.
- **Reported only:** reading H with R = 1 above 10 h/Mpc instead of flat; reading H with the own-list R_cold of Part A;
  form B's own spectrum against the pipeline's original reference (QX15 main theta with A_s fixed at 2.0e-9; that A_s is a
  placeholder of the modification gate, so a comparison of absolute parameter sets through it is not a gate).

**Part B labels (per footing, fixed now):**
- **FOREST ROW HOLDS:** Delta chi^2 <= 4 in reading H and in reading F.
- **FOREST ROW FAILS:** Delta chi^2 > 4 in both readings.
- **NO VERDICT:** the two readings disagree (the row then turns on how the redistribution evolves from z 0 to z 3, which the
  record does not compute: stated as not computed, with the cost of computing it), or a Part B known answer fails, or a
  Part B mutation does not bite. The number and the gate are printed with every label.

## 4. Known answers

- **KA-A1** (planted halos): as A.1; it also must recover every planted 3e14 and 1e15 halo within 0.15.
- **KA-A2** (published mass function, reported with a tolerance, gates nothing beyond NO VERDICT): in the resolved bins the
  own counts against Tinker 2008 at the run's cosmology, chi^2 with Poisson errors and the ratio per bin. Reported only;
  a ratio outside [0.5, 2] in any resolved bin is flagged and discussed, not graded (the run's draw is known to be high).
- **KA-A3** (inherited list put back): my copied pipeline with the inherited list reproduces CO1's stored numbers: every
  array of `co1_hm.json` primary and brackets to 1e-10 relative, C4 r_eff to 1e-6, C5 d_cold and every robust variant to
  0.005, KiDS chi^2 S0 / S0 x R_bar / S0 x R_tot to 0.005, the tooth to 0.005, and CO1's labels.
- **KA-A4** (bias code): a Poisson-sampled halo field drawn from (1 + b0 delta_m) of the run's own field with b0 = 2 and the
  same number density as the 1e13.5 to 1e14 bin returns b within its bootstrap error band (2 sigma).
- **KA-B1** (the carried row): form B's own spectrum fed as both reference and model with R = 1 gives Delta chi^2 = 0 to 1e-9;
  and the DESI file's md5 matches.
- **KA-B2** (the executed pipeline is the record's): WM1's MN-W row replayed (the 188.69 / 188.68 eV relic at WM1's stored
  m_eV and T_ncdm against the pipeline's own reference) gives WM1's stored 167379.35 / 167378.92 to 1e-4 relative.

## 5. MUTATE (separate `_MUTATE` outputs; each must bite)

- **MA1 (the finder sees structure):** the z = 0 grid with its cells randomly permuted (seed 1) gives at most 10 % of the
  own count above M_lo.
- **MA2 (the finder sees growth):** the z = 1 grid (same comoving threshold) gives at most 80 % of the z = 0 count above M_lo.
- **MA3 (the list reaches the rows):** the own list with every r_j doubled changes the halo-model total spectrum P_std at
  k = 1 h/Mpc by at least 10 % (canonical).
- **MB1 (warm cutoff caught):** form B's own spectrum times a 3 keV thermal-relic transfer (Viel et al. 2005 form as WM1's
  `viel`: alpha = 0.049 m_keV^-1.11 (Omega_c / 0.25)^0.11 (h / 0.7)^1.22 / h Mpc, nu 1.12, T = [1 + (alpha k)^(2 nu)]^(-5 / nu))
  gives Delta chi^2 > 4.
- **MB2 (a large redistribution caught):** CFG556's candidate-B primary R(k) (CO1's M1 array) in reading H gives Delta chi^2 > 4.

## 6. Hand estimates (unverified, before any code)

- Part A: M_lo about 3e13 Msun/h; about 100 to 200 halos above it; M_hi about 2e14 to 5e14 (no 1e15 halo in a 100 Mpc/h
  box is likely). The power at k = 1 comes mostly from 1e13.5 to 1e15, so f_res is near 0.4 to 0.7: NOT RESOLVED is a real
  possibility. If resolved, the own counts sit above Tinker by 0 to 40 % (the high draw) and the rows hold: CO1's
  Press-Schechter bracket moved d_cold by 0.3, so ROWS HOLD WITH THE OWN LIST with |shift in d_cold| below 1.
- Part B: reading F gives 0 by construction. In reading H, R_cold at 1 to 5 h/Mpc is 1.006 to 1.09 (canonical) and 1.01 to
  1.16 (alt); the forest's projected power at k_par 0.3 to 2.4 /Mpc integrates P above k_par, so r - 1 of 1 to 5 % against
  DESI's percent-level errors on several hundred points gives Delta chi^2 of order 10^2 to 10^3: reading H fails, and the
  expected Part B label is NO VERDICT (the readings disagree). MB1: Delta chi^2 of order 10^2 or more. MB2: of order 10^4.

## 7. Lane label (per footing)

Pair of part labels "A / B". In one word: **HOLDS** if A is ROWS HOLD WITH THE OWN LIST and B is FOREST ROW HOLDS;
**FAILS** if A is ROWS MOVE to a worse CO1 label or B is FOREST ROW FAILS; **NO VERDICT** otherwise (NOT RESOLVED included).
A HOLDS outcome is reported as needing an independent re-grade, not as a pass.

## 8. Compute

At most 4 threads, nice 19, one heavy job at a time, resident memory under 6 GB, 5 GB disk left free, no file above 1 GB;
nothing heavy while lane BX1's queue runs. Every job is minutes long; the shear step (CO1: 272 s) is the longest.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
