# UA1 frozen criteria: the two fragile rows of SE2 (groups, Coma UDGs)

Frozen before any UA1 script or UA1 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle.
No LCDM input. Both footings, graded separately, never pooled:
- canonical: a0 = 9.3603e-11 m/s^2, Lstar = 21.7 pc;
- alt: a0 = 1.1312e-10 m/s^2, Lstar = 22.9 pc.

Spec: closure_2026_11_07/WINNER_SEARCH_BRIEF_2026_11_07.md, "UA1: the two fragile rows". Parent lane: SE2
(criteria f49a99a04c; closure_2026_11_06/SE2_step_as_systematics). No new data, no downloads; every input is on disk
and named below. One thread, peak RSS under 1 GB, minutes.

**Not blind.** SE2's numbers (including its pericentre reading 1/9 and its widths x2 intervals), ST1, GB1, S1, QX30's
assumption ledger, the Lovisari+2015 table and the Eckmiller+2011 transcription (deepseek_push/G125) were read before
this freeze. What is new here is the groups budget, the pericentre cut and the width rule, all fixed now.

## 0. Machinery and statistics (unchanged from SE2)

se2.py is exec'd read-only (writes redirected to a temp directory outside the repo, its exit caught); every SE2 function,
loader, seed, statistic, prior and label rule is reused as is, except where a section below adds a knob or a cut.
- Posterior: flat prior on the step s; N = 20,000 Monte Carlo draws per class and footing; each draw takes every nuisance
  from its prior and one statistical draw (bootstrap over systems / Gaussian se, as SE2). SE2's statistical and nuisance
  random streams are kept exactly; every NEW knob draws from its own stream (seed 9100 + class offset, + 1 for alt), so
  zeroing the new knobs reproduces SE2 bit for bit.
- Labels per class and footing, from the posterior 95 % central interval of s (SE2 section 3):
  - **NOT A TEST** if (a) fewer than 5 admissible systems (UDG and dSph classes), or (b) no power: the raw stat-only
    95 % interval (GB1 L0 data side of the admissible set, no nuisance) contains 0 (groups: at both f* = 0 and f* = 1);
  - **EXPLAINED** if the posterior 95 % interval contains 0;
  - **NOT EXPLAINED** otherwise.
  Class label: the common label if both footings agree, else SPLIT (canonical / alt).

## 1. Groups (Lovisari+2015, 20 groups x 2 radii; GB1 G3 data; statistic = median residual over the 40 points,
bootstrap over the 20 groups)

### 1.1 Width rule: SINGLE widths (frozen)
Every stated range is read as +-1 sigma (Gaussian) or a uniform bracket, exactly SE2's prior rule. Doubled widths are
reported only and decide nothing. Reason: SE2's +-1 sigma reading is already the generous reading of a stated range
(the conventional reading is 2 sigma); doubling it again is a sensitivity, not a budget; and choosing the doubled rule
after SE2 showed that doubled widths contain 0 would be choosing the rule by its answer.

### 1.2 Full budget (every knob drawn jointly; source for each)
Kept from SE2:
- **stellar share** f* ~ U[0, 1] (GB1 f* 0 / 1 bracket; QX30 ledger G5).
- **IMF** on the stellar share: lambda ~ N(1, 1) truncated >= 0, sigma_star ~ U[200, 300] km/s (QX26; SE2).
New in UA1 (SE2 set the hydrostatic term to 0 and had no distance, clumping or dataset term):
- **non-thermal pressure / hydrostatic bias, NGC 5044-class.** M_true = M_HSE / (1 - b_nt) at both radii, one b_nt per
  draw common to all 20 groups (a systematic of the method), **b_nt ~ U[0, 0.20]**. Upper edge: Lovisari+2015 Sect. 6.2
  cites up to 20 % for disturbed / merging systems (QX30 ledger G4); CFG34 carried 20 % for groups. The AGN-disturbed,
  multiphase atmospheres of the NGC 5044 class are read at the top of the measured range (XRISM few % in cores; Eckert+19
  about 6 % at R500, 10 % at R200: record FAILURES_LITERATURE_REVIEW / QX30 X5), so the bracket runs from 0 to 20 %.
  Sign: physical non-thermal support makes the thermal (HSE) mass LOW, so this knob can only RAISE the step. No source on
  disk gives b_nt < 0 for groups. Reported only (not graded): the symmetric reading b_nt ~ U[-0.20, +0.20] (CFG34 carried
  its allowance symmetrically).
- **distance scale** (QX30 G1, ADM, graded there): all lengths x d_f, M_HSE x d_f, M_gas x d_f^2.5 (stars follow M_gas
  through f*), d_f ~ U[1, 0.70 / 0.674] (published h 0.70 to QX30's native h 0.674; bracket, uniform).
- **gas clumping** (QX30 G7 / X7, BOUND): M_gas x c_g, c_g ~ U[1, 1.1] (sqrt(C) 1.1 upper end, PROVISIONAL in QX30).
- **dataset / analysis term (cross-catalogue).** One common shift of log10 M_obs per draw, ~ N(0, m_G),
  m_G = sqrt(mu^2 + (rms / sqrt N)^2) of log10(M500_Lovisari / M500_Eckmiller+2011) over groups matched by name
  (upper case, spaces / dashes / dots removed). Source: the Eckmiller+2011 Table 15 transcription in
  deepseek_push/G125_group_equipartition.py (E11 list; marked UNVERIFIED-in-repo there, so PROVISIONAL here). This is
  SE2's dSph "membership / dataset" rule applied to groups. If fewer than 3 groups match, the term is 0, NOT IN BUDGET.
- **membership / interloper rule of the source catalogue.** Lovisari+2015 masses are X-ray hydrostatic masses
  (double-beta n_e, parametric T); the catalogue has no member-galaxy velocity step, so there is no interloper rule to
  vary on the mass side: **NOT APPLICABLE, contributes 0, disclosed.** Member galaxies enter only through the stellar
  share f*, which is already the widest knob; the cross-catalogue term above is the dataset analogue.
- Not in budget, disclosed: T-profile extrapolation to R500 (QX30 G3, either sign, not computable on disk); per-point
  measurement errors eM (bootstrap over groups carries the scatter; adding eM would double count); XMM vs Chandra T
  calibration (QX30 X12, wrong sign, no ground truth).

### 1.3 Groups known answer and MUTATE
- **KA-G (must hold, to 0):** with every NEW knob pinned (b_nt = 0, d_f = 1, c_g = 1, shift 0) the UA1 groups posterior
  equals SE2's groups posterior draw for draw (array_equal), and its summary equals se2.json's groups cell exactly, both
  footings. This is the "budget zeroed reproduces SE2's single-width verdict" check.
- **MG (must bite):** sign-inverted non-thermal term, b_nt ~ U[-0.20, 0] (HSE masses read as too HIGH). Bites iff on both
  footings the posterior median falls by at least 0.03 dex against UA1 main.

## 2. Coma UDGs and the symmetric pericentre cut

### 2.1 Admissibility (applied to every hosted pressure-supported class SE2 carries: Coma UDGs, bright M31, MW classical,
MW ultra-faint, M31 others; LG field has no host term and passes by definition, as SE2)
A system is ADMISSIBLE iff all three hold:
- **A1 tidal at the present distance** (SE2 A1, unchanged): tau = R_e / r_J(d) < 0.375.
- **A2 dynamical time** (SE2 A2, unchanged): t_cross = r_1/2 / sigma <= 0.1 t_orb.
- **A3 tidal at pericentre (NEW, named now):** tau_p = R_e / r_J(r_p) < 0.375, with the same estimator
  r_J(r) = r (M_W / (3 M_host(<r)))^(1/3), M_W = 4 sigma^2 R_e / G (QX24 / ST1 / SE2), and r_p from the on-disk orbits:
  - MW and M31 satellites: r_p = Z2's PM-based pericentre (rebuild_2026_10_22/Z2_satellite_systematics/z2_per_system.csv,
    r_peri_kpc, same footing, rows with pm = True) where it exists; otherwise r_p = d_host / 3 (the record's no-PM central
    convention: X20 A3 qualifier, UX4 T3, ST1 / SE2 pericentre reading). r_p is capped at d_host.
    M_host(<r_p) = V_c^2 r_p / G with SE2's V_c (200 MW / 230 M31 km/s).
  - Coma UDGs: no orbit or proper motion exists on disk for any of the 9, so r_p = d_mean / 3 (same convention), and
    M_host(<r_p) = g_host(r_p) r_p^2 / G with g_host from S1's Coma beta model (kT 8.6 keV, r_c 276 kpc, beta 0.71,
    mu 0.6; s1_v3_hosted_small.py g_beta), the same field SE2 used at d_mean. KA: g_beta(d_mean) / a0 reproduces S1's
    x_e_dmean to 1e-12.
  - Reported only: the ceiling r_p = d / 5 (UX4 T3) for no-PM systems.
A removed system is NOT A TEST, never a pass. The cut uses the observed dynamical mass and the host field, never the law,
so it removes systems that pass the law and systems that fail it alike.

### 2.2 Grading the survivors (as frozen in SE2)
- Coma UDGs: SE2 2.6 unchanged (mean E over the admissible galaxies, CFG933 se; six knobs s_M, s_A, s_D, s_aniso, s_mem,
  s_pos at single widths; the full-sample s_k are kept if galaxies are removed, SE2's disclosed approximation).
- dSph classes: SE2 2.5 unchanged on the admissible set (bright M31 and MW classical graded; LG field control; MW
  ultra-faint and M31 others reported only).

### 2.3 Admissibility MUTATE (must bite)
- **MA:** inverted admissibility: grade the COMPLEMENT (systems failing A1, A2 or A3) of each hosted class with the same
  machinery. Bites iff on both footings the Coma UDG complement is non-empty and its label differs from the main Coma
  label. If the main cut removes no Coma UDG, MA cannot bite and the pericentre cut is disclosed as having NO POWER on
  Coma (the Coma label is then SE2's).

## 3. Known answers (a KA failure stops grading)
- **KA0 (SE2 to 0):** se2.py exec'd read-only with writes redirected; every numeric leaf of its se2.json equals the
  committed se2.json exactly (difference 0) and every string is equal. (SE2's own KA1, the ST1 replay, runs inside it.)
- **KA-G** as 1.3.
- **KA-U:** with A3 switched off, UA1's admissible sets and the Coma / dSph posteriors equal SE2's cells exactly.
- **KA-beta:** g_beta(d_mean) / a0 = x_e_dmean to 1e-12 for all 9 UDGs, both footings.

## 4. Expected labels (stated before any number)
- **Groups: NOT EXPLAINED on both footings.** The new knob with the largest amplitude (non-thermal pressure) has the
  wrong sign; distance and clumping move the step by about -0.02 to -0.04 dex; the dataset term only widens.
- **Coma UDGs: NOT A TEST (admissible N < 5) on both footings is the expected reading**, but this is not sure: the beta
  model's core makes M_host(<d/3) smaller than SE2's isothermal x 2.08 reading assumed, so more than 1 of 9 may survive.
  If 5 or more survive, the expectation is NOT EXPLAINED.
- Bright M31 stays EXPLAINED; MW classical stays NOT A TEST.
- If both rows drop (groups EXPLAINED or NOT A TEST, Coma NOT A TEST or EXPLAINED), the residue reads X-COP + CMB lensing.
  RESULT says plainly which happened.

## 5. Outputs
ua1.py -> ua1.json / ua1.out (main, KA0, KA-G, KA-U, KA-beta) and ua1_MUTATE.out / ua1_MUTATE.json (MG, MA). Small files;
no arrays stored; no home paths. Any change after this freeze is a numbered, dated amendment disclosed in RESULT.md.

Kappa = 1/2 FITTED; not theory closed.
