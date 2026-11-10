# DG1 frozen criteria: the dwarfs' data side and their gas history under form B (RB2's high rows)

Frozen before any DG1 script exists and before any DG1 number is computed. TEST lane: it relabels nothing, adopts nothing,
is not registered, and changes no label of RB2, RB1, P1, G2, SE2, CFG655, CFG441 or DF1. kappa = 1/2 FITTED; not theory
closed. Cold dark energy is a gravitating field component, never a particle. Both footings graded separately, never pooled:
canonical a0 = 9.3603e-11 m/s^2, alt a0 = 1.1312e-10 m/s^2. Lane id DG1 checked free (`ls`, `git log --all --grep=DG1`,
grep of the 11-09 / 11-10 closure folders): no collision. Folder `closure_2026_11_10/` created by this lane.

**Post hoc to RB2, and partly not blind.** RB2's class numbers were known when this lane was designed (MW ultra-faint
+0.634 / +0.592, bright M31 +0.273 / +0.231, MW classical +0.281 / +0.241, LG field +0.054 / +0.017, Coma +0.326) and the
brief quoted five classical rows (Draco +0.63, Ursa Minor +0.57, Sextans +0.50, Fornax -0.10, Leo I -0.03). The class
gate G1 is therefore weak evidence; the per-system gates G2 and G3 carry the weight. Not opened before this freeze: any
per-system number in `rb2.json`, any per-system L in P1's `p1_per_system.csv` (only its column names and which systems
have a finite value were read), any value in the Weisz 2014 tables (only galaxy names and column names), and the results
of CFG824, CFG827 and CFG923, which used the Weisz 2014 tables (only their folder names were seen).

## 0. The question and the hypothesis under test

RB2 graded form B on the hosted dwarfs as the isolated law on TODAY'S STARS (Upsilon_V = 2, no gas term, Wolf estimator,
spherical isotropic equilibrium Plummer), cut only by an instantaneous tide. MW ultra-faints and bright M31 dwarfs read
B FAILS HIGH on both footings. Two readings could put them there:

- **Data side (Part A):** what the people who measured the dispersions assumed (censoring at the instrument floor, binaries,
  velocity-error floors) and RB2's statistic (measurement scatter only; no Upsilon, anisotropy, membership or distance
  budget; SE2's joint budget not applied).
- **History (Part B):** under form B the cold share is one conserved charge (FB1 note, section 1.2). If a dwarf's halo
  settled around its baryons while it still held its gas, and the gas then left, the halo's charge stays. RB1 already graded
  the hot systems with the share tied to the baryons that FELL IN; RB2 did not do this for dwarfs.

The hypothesis to try to kill: the high rows are the halo of gas the dwarfs lost after it settled.

## 1. Inputs (copied code paths, nothing imported from another lane's folder)

- **RB2's dSph pipeline, copied verbatim:** X1's LVD loader, build (seed 20261031, same call order), the Arroyo binary
  factor for M_V > -7.7, classes, B's law gl(), gNp(), rJ_iso(), gB(), dsph_reading(), XF1's boot_median (4,000
  resamples, seed 11). RB2's "prim" reading is the observed residual Delta_B,i (median over the 2,000 MC draws) with sd_i.
- **P1's lost-gas code path, copied verbatim:** moments(), the (k, u) grid, e6_equiv(), u0_solve(), g0_exact(), lmdf(),
  lvd_sigma(), intervals(), mass_g() (gas = 1.33 M_HI). L = the minimum over P1's zeta >= 1 one-zone family of
  (baryons that took part) / (baryons today), at the LVD mean [Fe/H] (`metallicity`) and the LVD MDF width.
  - **Central L:** P1's graded corner, `L_MDF_I0_m05` (central width, log y_Fe = -0.5). This is P1's lowest-L reading
    (minimised over the outflow family; pre-enrichment and pristine inflow only raise L).
  - **Lower edge:** `L_MDF_I2_m05` (2-sigma-low width, log y -0.5). **Upper edge:** `L_MDF_hi_p01` (2-sigma-high width,
    log y +0.1). Reported per system and used by G5.
  - Coverage: P1 holds L for 26 of RB2's 31 MW ultra-faints, 3 of 25 bright M31, 0 of 8 MW classical, Leo T of the LG field
    and Crater II. This lane runs P1's copied lmdf() on every RB2 row with an LVD mean [Fe/H] and an LVD width
    (spectroscopic, else photometric, P1's order). Ms = 10^LVD mass_stellar (M_V rule of X1 where missing); for P1's own
    systems Ms = E6's logMstar, as P1. Expected coverage: ultra-faints 26, bright M31 10, MW classical 8, LG field 12.
  - Systems with an LVD mean [Fe/H] but no width (bright M31: 9 more) get a reported-only arm with the class's median LVD
    width imputed (P1's interval rule, no error bars). Never graded.
- **SE2's dSph budget, copied verbatim:** dsph_admiss() (A1 tidal tau < 0.375, A2 crossing time <= 0.1 orbit), the per
  class anisotropy width a_c and membership width m_c (dsph_inputs: McConnachie 2012 for MW classes and LG field,
  Collins+2013 for M31), SPEC main priors (log10 Upsilon_V ~ N(0, 0.30) common; gas share q ~ U[0, 0.5]; HI upper limits
  U[0, UL]; per-system distance from LVD distance-modulus errors), post_dsph's seeds (rngs(cls, f)) and NDRAW 20,000.
- **LVD upper limits:** `vlos_sigma_ul` in `real_research/data/dsph/lvd_dwarf_*.csv`. Counted before this freeze: MW 45
  measured, 9 upper-limit-only (Aquarius III 3.5, Draco II 2.6, Grus II 2.0, Hydra II 4.11, Phoenix II 21.2, Reticulum III
  8.3, Segue 2 2.06, Triangulum II 3.5, Tucana III 1.5 km/s; all M_V > -7.7, so all MW ultra-faint by X1's rule); M31 34
  measured, 2 upper-limit-only (Andromeda XII 4.0, Andromeda XXIV 7.3); LG field 13 measured, 0. No row carries both. RB2's
  31 ultra-faints are therefore only the systems with a measured dispersion.
- **Weisz et al. 2014 (ApJ 789, 147), on disk** (`real_research/data/dsph/weisz2014_dl/`, tables 5 and 6, VizieR
  J/ApJ/789/147): cumulative best-fit SFHs. Used only in Part D (reported, not in the label).

## 2. Part A, the data side (graded per class, per footing; RB2's labels are not changed)

Classes: MW ultra-faint and bright M31 (the two FAILS HIGH); MW classical reported.

- **A1 censoring.** Each upper-limit system is built by the copied pipeline with sigma = its UL (and its own Arroyo factor
  or the median one, as RB2), giving a bound Delta_UL,i (median over its MC draws; the true residual is at or below it).
  Class statistic: the Kaplan-Meier median of the left-censored set (flip x -> -x, right-censored KM, median = first
  event time with S <= 0.5; if S never reaches 0.5, the lowest bound is used and flagged), inside XF1's bootstrap (4,000
  resamples of systems, seed 11, measured values drawn as Delta_i + N(0, sd_i), bounds kept fixed). 95 % interval from
  the 2.5 / 97.5 percentiles. Reported beside it: a censored-normal maximum likelihood (mu, tau with each sd_i) with a
  profile-likelihood 95 % interval on mu.
  - The upper-limit systems of the class are included whatever their size or nature (same loader rule as RB2).
- **A2 binaries and velocity-error floors (frozen bracket).** Arms, each run through the censored A1 statistic:
  - a0: RB2's choice (Arroyo free-f factor for M_V > -7.7);
  - a+: no binary factor (b = 1) (upper edge);
  - af07: Arroyo f = 0.7 factor (X1's other column);
  - alow: sigma = the lower of LVD and Geha 2026 where Geha resolves it (X1's "lower" source);
  - afl: velocity-error floor: for every system with sigma < 4 km/s, sigma -> sqrt(sigma^2 - delta^2), delta = 1.0 km/s;
    a measured sigma <= sqrt(2) delta becomes an upper limit at its measured value;
  - adown: af07 + alow + afl together (the most generous data side to B).
- **A3 SE2's joint budget re-derived for B.** Per draw: D'_i = Delta_B,i + N(0, sd_i) + 2 dsig_c + da_c - dd_i -
  [log10 gl(B_i g_N,i) - log10 gl(g_N,i)], B_i = Upsilon_V / 2 + 2 q (1.33 M_HI,i) / M*_i, g_N,i = B's Newtonian field at
  r_1/2 from the central y (gNp(4/3, y0)), anchor 0 (B is graded against 0, not against SPARC). Admissible systems only
  (SE2's A1 and A2; for an upper-limit system A1 / A2 use its UL). Bootstrap over systems, median. The SE2-verbatim form
  (no N(0, sd_i)) is reported beside it.
- **A-full:** A1 + A3 together (censored KM median inside the joint-budget draws; bounds shifted by the same common knobs),
  with RB2's binary choice (a0). The adown arm of A-full is reported.

**Part A outcome per class and footing (frozen):** "FAILS HIGH SURVIVES THE DATA-SIDE REGRADE" iff the A-full 95 % interval
lies above 0; otherwise "DOES NOT SURVIVE". Printed beside: A1 alone, A3 alone, every A2 arm.

## 3. Part B, the history gate (blind to the per-system residuals until the run)

**Formula (frozen).** Per system, on RB2's MC draws (y_d = the draw's G M*/(a^2 a0), a = R_h, r_1/2 = (4/3) a, Plummer):
- today's baryons: g_N,today = (1 + 2 q_c (1.33 M_HI) / M*) g_N*(r_1/2), q_c = 0.25 (the midpoint of SE2's q prior) for
  systems with a measured LVD mass_HI; 0 for upper limits (gas-free dSphs); lost gas follows the stars;
- baryons when the halo settled: g_N,0 = g_N,today + eta g_N*(r_1/2), eta = (L - 1)(M* + M_g) / M* (gas-free: eta = L - 1,
  so g_N,0 = L g_N*); M_g = 1.33 M_HI;
- **edge NR, no response:** the cold mass is the law's phantom of the settled baryons and does not move when the gas leaves:
  g_hist = g_N,today + [gl(g_N,0) - g_N,0];
- **edge AD, adiabatic expansion (slow loss):** every cold shell keeps r M_tot(<r) when the gas leaves (circular-orbit
  invariant); initial M_tot = settled baryons + phantom; final M_tot = today's baryons + the shell's cold mass; the cold mass
  inside r_1/2 is read off the expanded shells (gas and stars as Plummer with scale a, today's stars unchanged);
- prediction P_i = log10[g_hist / gl(g_N*)] (RB2's B on today's stars is gl(g_N*)); after-history residual per draw
  R_H = RB2's prim residual - P; per system the median and sd over draws.
- Reported arm, not graded: lost gas spread as a Plummer of scale 2a (more extended than the stars).
- In the deep limit with gas-free baryons, P -> (1/2) log10 L: the ultra-faints' +0.63 needs L about 18.

**Gates (per footing, per edge; central L).** Graded classes: MW ultra-faint (26 with L), bright M31 (10 with L),
MW classical (8). Coma UDGs: no chemistry on disk, not graded here.
- **G1 class residual after history, two-sided.** XF1's C2 (boot_median, 4,000, seed 11) of R_H over each graded class.
  PASS iff the 95 % interval contains 0 for all three; FAIL HIGH (history not enough) or FAIL LOW (overshoot) otherwise.
  RB2's C2 on the same subset (before history) printed beside it.
- **G2 per system, within class.** S = sum_c n_c rho_c / sum_c n_c, rho_c = Spearman of Delta_B,i on P_i in class c.
  Null: 10,000 permutations of P within each class (seed 20261110). Slope: OLS of Delta_B on P after subtracting each
  class's means, 95 % interval from 4,000 bootstraps of systems within class (seed 20261111).
  PASS iff S > 0 with one-sided p <= 0.05 AND the slope interval contains 1.
- **G3 at fixed stellar mass and at fixed size.** As G2's S and permutation test, after regressing both Delta_B and P
  linearly on log10 M* (G3m) and separately on log10 r_1/2 (G3r) within each class. PASS iff both S > 0 with p <= 0.05.
- **Power (plant, frozen):** 500 synthetic sets Delta_syn,i = P_i + N(0, sd_i^2 + tau^2), tau^2 = max(0.05^2, rms^2 -
  median(sd_i^2) - mean within-class var(P)), rms = RB2's stored M2 unscrambled pooled rms (0.371 canonical, 0.370 alt);
  1,000 permutations each (seed 20261112). A gate whose plant pass rate is < 0.5 reads NO POWER on that footing and edge
  (its observed outcome is printed, but it cannot close and does not count as a fail).
- **G4 controls.**
  - G4a LG field (12 with L, gas-bearing; present HI counted with q_c): C2 interval of R_H contains 0 -> PASS; else FAIL
    (LOW = overshoot, HIGH). Fewer than 5 with L -> NOT EVALUABLE. HI share q = 0 and 0.5 reported.
  - G4b least gas lost: the lowest third by P of the pooled graded rows; FAIL iff the C2 interval of R_H lies above 0
    (the high residual persists where history predicts little).
- **G5 supply.** L_need,i solves P(L) = Delta_B,i on the edge (L_need = 1 if Delta_B,i <= 0). PASS iff, in each graded
  class, the median L_need <= the median of P1's upper edge `L_MDF_hi_p01` (copied code). Per-system excess counted.

**Lane label per footing (frozen):**
- **HISTORY CLOSES THE HIGH ROWS** iff on at least one edge (NR or AD) G1, G2, G3m, G3r, G4a, G4b and G5 all PASS, with G2,
  G3m and G3r each having power. The label names the edge(s).
- **HISTORY DOES NOT CLOSE THEM** iff on both edges at least one gate FAILS (a G2 / G3 fail counts only where that gate
  has power; NOT EVALUABLE never counts as a fail).
- **NO VERDICT** otherwise.
- Printed beside it, per footing: Part A's outcome for MW ultra-faint and bright M31 (SURVIVES / DOES NOT SURVIVE).
- L-sensitivity: G1 and G5 are rerun at the lower and upper L edges and reported; a label that changes there carries
  "(L-sensitive)".

**What counts AGAINST form B (stated now):** a G1 overshoot (FAIL LOW): B with its own history would put the dwarfs below
their data; a G4a overshoot: the gas-rich field dwarfs, which B's law fits on stars alone, would be pushed low by their own
history; G5 FAIL: the history B needs is more gas than the chemistry allows. A G2 / G3 fail with power says the high rows
are not B's history, which leaves them as B's open item. None of these changes RB2's labels.

## 4. MUTATE twins (separate outputs dg1_MUTATE.out / dg1_MUTATE.json)

- **M1 lost gas scrambled within class:** 20 fixed permutations of L within each class (seed 4242), everything else
  unchanged. Bites iff the G2 pass rate over the 20 is <= 2/20 and the median S drops below the unscrambled S. If the
  unscrambled S is not above the scrambled median, RESULT says so (no history ordering to destroy).
- **M2 stellar-mass power law in place of history:** P_pl,i = a + b (log10 M* - 6), (a, b) by OLS of Delta_B on log10 M*
  over the pooled graded rows with L (2 fitted numbers; history has 0). Reported: G1, G2, G4 under P_pl; rms of Delta_B - P
  for both; BIC (n ln(RSS/n) + k ln n) for both; Spearman of P_hist with log10 M* within class. Reading (frozen):
  "HISTORY BEATS THE POWER LAW" iff BIC_hist < BIC_pl - 2; "SAME TREND RENAMED" iff the within-class |rho(P_hist, log M*)|
  >= 0.7 and G3 does not PASS; otherwise "NOT SEPARATED". Bites iff P_pl changes G1's class medians by > 0.01 dex.

## 5. Known answers (a failure stops grading; numbers in dg1.out)

- **KA1** RB2 reproduced: every per-system Delta[prim] and sd[prim] equals rb2.json to 1e-9, both footings; the C2 class
  medians of MW ultra-faint, bright M31, MW classical equal rb2.json to 1e-9.
- **KA2** P1 reproduced: the copied lmdf() gives P1's stored L_MDF_I0_m05, L_MDF_I2_m05 and L_MDF_hi_p01 for P1's tested
  systems to 1e-6 relative.
- **KA3** SE2's stored dsph_widths (a_c, m_c per class) reproduced by the copied dsph_inputs() to 1e-9.
- **KA4** history formula: L = 1 gives P = 0 exactly on both edges; deep gas-free limit (y 1e-8) gives P = (1/2) log10 L to
  1e-3 (NR); the AD edge keeps r M(<r) on every shell to 1e-9 and equals NR when L = 1; P rises with L.
- **KA5** statistics: KM median with no censoring equals the plain median; KM with all bounds above every measured value
  equals the plain median of the measured values; censored ML with no censoring equals the weighted-mean solution to 1e-6.
- **KA6** Part A arm a0 with no censored systems reproduces RB2's C2 class medians (= KA1's numbers).

## 6. Part C (cited, no new computation, no new label)

DF2, DF4, DF9 and LEDA 4014647 as CFG655 stands: PASS conditional on the formation-channel label from outside the
framework (1 of 16 assignments passes). NGC 147, IC 1613, Cassiopeia III and Crater II: the on-disk evidence is listed
(`_external_data/ic1613_muse2024`, `_external_data/little_things_oh2015`, LVD, RB2's orbit edge). History only ADDS cold mass
(P >= 0), so it cannot lift a LOW row; that is stated with the numbers. No new label for a low row.

## 7. Part D (reported; not in the label)

- **Held-out prediction (frozen now):** tau90 = the lookback time at which 90 % of the stars had formed.
  - D1 (sign): within each class, Delta_B rises with tau90 (earlier quenching, higher residual), because early quenchers
    are the metal-poor, high-L systems. Expected size: the within-class spread of P between the earliest and latest
    third, 0.2 to 0.5 dex. Statistic: G2's S with tau90 in place of P, within-class permutation null.
  - D2 (premise): the after-history residual R_H has no trend with tau90 (two-sided p > 0.05) if every halo settled before
    its gas left. A negative trend (early quenchers over-predicted) would say the halo had not settled before early losses;
    a positive trend would say history is missing something keyed to time, not chemistry.
  - Falsified as the cause of the high rows if D1 reads S <= 0 in a class with >= 8 systems and the class offset remains.
- **On disk (Weisz 2014):** tau90 per galaxy from the best-fit cumulative SFH (table 6 for multi-field galaxies, else the
  first table 5 field), linear interpolation in log t between the f(log t) grid points; overlap with RB2's rows reported
  with D1 and D2. MW classical residuals were partly seen (section header).
- **Not on disk (to be fetched only with the owner's go):** the M31 satellites' HST lifetime SFHs (Savino et al. 2025,
  the per-galaxy tau50 / tau90 table), the HST ultra-faint SFHs (Brown et al. 2014, per-galaxy quenching ages; Sacchi et al.
  2021), and per-star [Fe/H] for the bright M31 dwarfs without an LVD width (Kirby et al. 2020; Wojno et al. 2020).

## 8. Hand estimate (frozen, to be marked HIT / MISS)

- A1: the 9 upper limits (1.5 to 4 km/s, with B predicting 1 to 2 km/s) sit below the class median, so the KM median drops
  0.15 to 0.25 dex to about +0.40 to +0.48; still above 0 on the censored C2 statistic.
- A2: af07 lowers the ultra-faints by 0.05 to 0.1 dex; afl by about 0.05 to 0.1; adown about +0.3.
- A3: the common knobs (2 m_c 0.24 dex, a_c 0.09, Upsilon about 0.15 dex in g) widen the ultra-faint interval to about
  +-0.6; it contains 0. Bright M31 contains 0. Part A: both FAILS HIGH DO NOT SURVIVE (ultra-faints 70 %, bright M31 85 %).
- Part B: ultra-faint P about +0.6 to +0.9 (L 20 to 60), so G1 near 0 or a mild overshoot; classical P about 0.15 (Fornax)
  to 0.65 (Draco, Ursa Minor), G1 near 0; bright M31 P about 0.3 to 0.6 against +0.27, a possible overshoot. G2 within
  class: weak (S about +0.15, p about 0.15): FAIL 60 %. G3: L is close to a function of M* through the mass-metallicity
  relation and DF1 found no mass key at fixed size: FAIL or NO POWER 70 %. G4a: with the HI counted the field sits about
  -0.15, with history about -0.35: FAIL LOW 55 %. AD lowers P by 0 to 0.2 dex.
- Label: HISTORY DOES NOT CLOSE THEM 65 %, NO VERDICT 25 %, CLOSES 10 %.

## 9. Limits stated now

- The form-B premise that the halo settled before the gas left is not derived: COL1 finds the collapse does not reach the
  static state, and FB1 (section 2.2) lists the collapse as unsolved. FLD1's fold reach is context only.
- P1's L is a model quantity (one-zone family, minimised, Fe yield bracket, homogeneous mixing). It is the record's only
  native history number. Unmixed-ejecta escape (P1's A4) would lower it and is untestable on disk.
- The response of the cold charge to gas loss is not solved in the action; NR and AD are frozen edges, not derivations.
- Spherical, isotropic, equilibrium Plummer; the Wolf estimator; RB2's tidal cut carried unchanged (history makes dwarfs
  denser, so r_J only grows).
- No LCDM-calibrated quantity enters any graded row. 5.364 does not enter (L comes from chemistry alone).

Compute: one thread, nice 10, under 2 GB, minutes. Outputs: dg1.py, dg1.out, dg1.json, dg1_MUTATE.out, dg1_MUTATE.json,
RESULT.md. Any change after this freeze goes in AMENDMENT_A#.md, committed alone and marked post hoc if a number was seen.

kappa = 1/2 FITTED; not theory closed. Relabels nothing.
