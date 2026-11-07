# SE2 frozen criteria: the hot/cold step as systematics, graded as one joint budget per class

Frozen before any SE2 script or SE2 number exists. Kappa = 1/2 FITTED; not theory closed. Adopts nothing. No particle.
Both footings, graded separately, never pooled:
- canonical: a0 = 9.3603e-11 m/s^2, Lstar = 21.7 pc;
- alt: a0 = 1.1312e-10 m/s^2, Lstar = 22.9 pc.

Lane spec: HANDOFF_FIELD_EQUATIONS_CHAT_2026_11_06.md, "Lane SE2". No new data, no downloads. Every input is on disk
and named below. Compute: one thread, under 1 GB, minutes.

**Not blind.** ST1 (criteria 3622fad837, result 82703215e0), GB1, S1, CFG948, QX18, QX20-QX26 numbers were read
before this freeze. What is new here is the joint grading rule, the admissibility rule and the priors, all fixed now.

## 0. Frame

ST1 set each systematic at its favourable edge, one at a time. SE2 replaces that with a joint posterior per class:
every knob is a nuisance parameter with a prior frozen below, all knobs are drawn together, and the class's step is
the GB1 class statistic on the corrected data side. The prediction is the plain law throughout (GB1's L0: b = 1,
F = 1, T = 0). Data sides, statistics and anchors are GB1's (gb1.py exec'd read-only up to its "# --- main" block),
except where a knob changes the data side as stated.

**Posterior.** Flat prior on the step s. For each class and footing, N = 20,000 Monte Carlo draws; each draw takes
one draw of every nuisance from its prior and one statistical draw (a bootstrap resample of the class's systems, or
a Gaussian with the record's statistical error where the record carries only that), and records the class statistic.
The draws are the posterior of s. Seeds fixed in the script.

**Prior rule (one rule for every knob).**
- A stated +- range (a factor, a dex, a per cent) is +-1 sigma of a Gaussian, in log where the source states a
  factor or dex. This is more generous than reading the range as 2 sigma.
- A stated bracket [lo, hi] with no preferred value is uniform on it.
- A one-sided sign with no stated amplitude contributes 0 and is disclosed with its sign.
- A knob with no source on disk contributes 0 and is disclosed as NOT IN BUDGET.

## 1. Admissibility (equilibrium), pressure-supported dwarfs and Coma UDGs

Applied to every dSph class GB1 carries (bright M31, MW classical, LG field, MW ultra-faint, M31 others) and to the
9 admitted Coma UDGs. It uses the observed dynamical mass, never the law, so it removes systems that pass the law and
systems that fail it alike. A system is ADMISSIBLE iff both hold:

- **A1 tidal:** tau = R_e / r_J < 0.375 (r_1/2 / r_J < 0.5, r_1/2 = (4/3) R_e), r_J = d (M_W / (3 M_host(<d)))^(1/3),
  M_W = 4 sigma^2 R_e / G. Source: QX24 iter_1 estimator, ST1 S-D line (Z2 C1).
  - dSphs: d = X1 d_host_kpc, M_host = V_c^2 d / G with V_c 200 (MW) / 230 (M31) km/s, as ST1.
  - Coma UDGs: d = S1 d_mean_kpc, M_host(<d) = g_host d^2 / G with g_host = x_e_dmean a0 (S1's Coma beta-model
    field at dmean, s1_coma_per_galaxy.csv).
- **A2 dynamical time:** t_cross = r_1/2 / sigma <= 0.1 t_orb, t_orb = 2 pi d / V_c(d) (V_c(d) = sqrt(g_host d) for
  Coma).
- A system whose host is not MW, M31 or Coma (the LG field dwarfs) has no host term: A1 and A2 hold by definition.
- Reported, not graded: A1 at pericentre (tau x 3^(2/3), ST1's reading).

A removed system is NOT A TEST. It is never counted as a pass.

## 2. Classes, statistics and priors (source for each)

### 2.1 X-ray ellipticals (GB1 G4 data, 7 galaxies x 3 radii)
Statistic: mean residual over the 21 points; statistical draw = bootstrap over the 7 galaxies (each with its three
points).
- **IMF:** b = 1 + share (max(alpha(s sigma_e) R_SK, 1)^lambda - 1), the Posacki+2015 relation of QX26 / GB1 b_imf
  scaled by an exponent. lambda ~ N(1, 1) truncated at lambda >= 0: centred on the measured relation, Kroupa
  (lambda = 0) at -1 sigma, nothing lighter than Kroupa (GB1's floor). Source: QX26 (44b5658218).
- **sigma_0 scale** s ~ N(1, 0.1): QX26's x0.9 / x1.1 bracket read as +-1 sigma.
- distance: NOT IN BUDGET (no stated per-galaxy distance error on disk).
- anisotropy: 0 (hydrostatic X-ray masses).
- gas: 0, sign disclosed: QX18 neglected gas, so the baseline is an upper bound on the step; gas would lower it.
- membership, tides: not applicable.

### 2.2 KiDS early/late split (GB1 G7)
Statistic: R = DX - D_cand; statistical draw ~ N(0, STOT) (GB1's s_tot, which carries its 0.05 floor).
- **IMF:** lambda as 2.1 on the early colour; early sigma_e ~ U[130, 210] km/s (QX26 bracket, no per-lens sigma);
  late at 60 km/s (Kroupa floor). Source: QX26.
- distance (photo-z), membership (colour contamination): NOT IN BUDGET (nothing on disk). Anisotropy, gas, tides: not
  applicable.

### 2.3 X-COP (GB1 G2 data, 7 clusters x 5 radii)
Statistic: mean residual; statistical draw = bootstrap over the 7 clusters.
- **IMF:** lambda as 2.1, sigma_star ~ U[250, 350] km/s (GB1's G2 fill bracket).
- hydrostatic bias: 0, sign disclosed (QX21 T3: lensing masses >= hydrostatic, so a bias raises the step).
- gas: measured (in the data). Distance, anisotropy, membership, tides: 0 (not applicable or not on disk).

### 2.4 Groups (GB1 G3 data, 20 groups x 2 radii)
Statistic: median residual over all 40 points; statistical draw = bootstrap over the 20 groups.
- **stellar share** f* ~ U[0, 1] (GB1's f* 0 / 1 bracket).
- **IMF:** lambda as 2.1 on the stellar share, sigma_star ~ U[200, 300] km/s (GB1's G3 fill bracket).
- hydrostatic bias: as X-COP. Others 0.

### 2.5 dSph classes (GB1 G6 data; graded: bright M31, MW classical; LG field is the control; MW ultra-faint and
M31 others reported only, as GB1)
Statistic: median over the ADMISSIBLE systems of the class minus GB1's SPARC anchor (L0 Z, fixed); statistical draw
= bootstrap over the admissible systems. Per system D' = D + 2 dsig_c + da_c - dd_i - [log10 g_law(B_i g_N,i) -
log10 g_law(g_N,i)], g_N,i = x_i a0 from GB1's features.
- **IMF / Upsilon_V:** log10 Upsilon_V ~ N(log10 2, 0.30), common to every dSph: the record's declared prior
  Upsilon_V = 2, bracket 1-4 (E3 ledger, X1 criteria), read as +-1 sigma.
- **gas:** B_i = Upsilon_V/2 + 2 q_i (1.33 M_HI,i) / M*_i, M_HI from LVD mass_HI (QX23's convention, 1.33 for
  helium); upper limits drawn U[0, UL]; q_i ~ U[0, 0.5] is the share of the gas inside r_1/2 (0: all outside;
  0.5: gas follows the stars). The q bracket is a frozen assumption (no profile on disk), disclosed.
- **distance:** per system, dd_i ~ N(0, (DM_em + DM_ep)/2 / 5) from LVD distance_modulus errors; D shifts by -dd_i
  (M* and r_1/2^2 scale alike, so g_N is unchanged).
- **anisotropy / estimator:** common per class, da_c ~ N(0, a_c), a_c = median over the class of
  |Delta[v3 L*floor E-V] - Delta[v3 L*floor]| (X1 x1_per_system.csv; S1's E-V vs E-W estimator).
- **membership / dataset:** common per class, dsig_c ~ N(0, m_c) in log10 sigma. m_c = sqrt(mu^2 + (rms / sqrt N)^2)
  from log10(sigma_LVD / sigma_alt) over the class's systems found in the alternative catalogue (Collins+2013 for
  bright M31; McConnachie 2012 for MW classical and LG field; zero sigma entries skipped). Names matched after
  lower-casing and removing spaces, parentheses and dashes, with "andromeda" -> "and". If fewer than 3 match, the pooled
  value over the three graded/control classes is used.
- binaries: no separate term (LW1 applies Arroyo factors to ultra-faints only; for the bright classes it is folded
  into membership / dataset). Disclosed.
- tides: the admissibility cut (section 1); no residual tidal term.

### 2.6 Coma UDGs (GB1 G5; S1 row "<foot>|S4 v3 dmean L*floor E-W")
Statistic: mean E over the ADMISSIBLE galaxies, in dex. Statistical draw ~ N(0, se), se by CFG933's convention
(max of scatter / sqrt n and measurement) from s1_coma_per_galaxy.csv (E_v3_dmean, sE). Knobs enter linearly in ln E,
theta_k ~ N(0, 1), shift theta_k s_k:
- **M* (IMF + SPS)** +-0.2 dex: s_M (S1 / CFG948). The IMF is inside this term; not counted twice.
- **sigma** +-15 % (aperture, tracer membership): s_A (S1 / CFG948).
- **distance** +-5 %: s_D (S1 / CFG948).
- **anisotropy / estimator:** s_aniso = |meanE(E-V) - meanE(E-W)| at dmean (S1 rows).
- **sample membership:** s_mem = |meanE(all 11) - meanE(9)| at dmean (S1 rows).
- **3-D position:** s_pos = |meanE(dproj) - meanE(dmean)| (S1 rows).
- gas: 0, NOT IN BUDGET (no HI for Coma UDGs on disk; gas would lower the step). Tides: admissibility.
- If admissibility removes galaxies, the full-sample s_k are kept (disclosed approximation).
- Reported only, not graded (model choices, as ST1): S1's field / 2 and isolated rows.

## 3. Labels

Per class and footing, from the posterior 95 % central interval of s:
- **EXPLAINED:** the interval contains 0.
- **NOT EXPLAINED:** the interval excludes 0.
- **NOT A TEST:** (a) fewer than 5 admissible systems (dSph and UDG classes), or (b) no power: on the GB1 L0 data
  side of the admissible set, with no nuisance, the statistical 95 % interval already contains 0 (the class never
  established a step, so systematics cannot be said to explain it).
Class label: the common label if both footings agree, else SPLIT (canonical / alt).
Reported per cell: posterior median, 68 % and 95 % intervals, sd, z = median / sd, P(s <= 0); the GB1-line reading
P(|s| <= line) (reported only); and a widths x2 sensitivity (reported only).

**Lane label.**
- **STEP = SYSTEMATICS EXCEPT CLUSTERS AND GROUPS** if X-COP and groups are NOT EXPLAINED and every other hot class
  (ellipticals, KiDS, bright M31, MW classical, Coma UDGs) is EXPLAINED or NOT A TEST, on both footings;
- **STEP = SYSTEMATICS IN PART (remaining set)** if at least one hot class is EXPLAINED and at least one non-cluster
  hot class is NOT EXPLAINED;
- **STEP STANDS** if no hot class is EXPLAINED.
The handoff expects Coma UDGs to stay NOT EXPLAINED; RESULT says it plainly either way.

## 4. CMB row

Is the CMB wall a separate cause from the hot-system step? Read from the record (no re-solve), per key: G9 (CMB-lensing
shape / cold at z 3400) and the hot classes (at least G2 X-COP and G3 groups):
KD1 (kd1.json table), HC1 (hc1.json, hc1_g9.json), LD1 (ld1.json), EN1 (en1.json), QX12 iter_2 / iter_3 (README,
qx12_i3.json), QX3 iter1-iter3 (README), QX15 (README / qx15.json). SE1 is included if a committed SE1 result exists
when the script runs; otherwise that is stated.
- **SEPARATE** if no single key in the record passes both G9 and the hot classes.
- **COMMON** otherwise.
Disclosed with the label: if no key passes the hot classes at all, SEPARATE is the frozen rule's reading, not a
proof that two causes exist.

## 5. Known answers (a KA failure stops grading)

- **KA1 (ST1 to 0):** st1.py exec'd read-only (its writes redirected to a scratch path, its exit caught); every
  numeric leaf of its result equals the committed st1.json exactly (difference 0), every string equal.
- **KA2 (SE2 machinery at ST1's settings, to 1e-12):** lambda = 1, s = 1 -> ST1's G4 corrected mean; lambda = 1 at
  sigma_e 130 / 170 / 210 -> ST1's G7 bracket R (exact law); A1 alone at ST1's line with no knob, through GB1's
  g_dsph -> ST1's G6 cut medians and CIs; S1 row -> ST1's G5 Q z and L residual; SE2's vectorised X-COP and groups
  residuals at lambda = 0, f* 0 / 1 -> GB1 L0 G2 mean and G3 medians.
- **KA3:** the 9-UDG mean and se rebuilt from the CSV equal S1's JSON row to 1e-12.

## 6. MUTATE (separate outputs se2_MUTATE.*)

- **M1 (frozen, must bite): inverted IMF bracket.** lambda ~ N(-1, 1) truncated at lambda <= 0 (the mirror: lighter
  than Kroupa, b = f^lambda <= 1) on ellipticals, KiDS, X-COP and groups. Bites iff, on both footings, (i) the MUTATE
  posterior median exceeds the main one for each of the four classes, and (ii) KiDS reads NOT EXPLAINED (if main KiDS is
  already NOT EXPLAINED, (i) alone decides).
- **M2 (frozen, must hold): zero-width priors** reproduce, for every class, the no-nuisance statistical posterior
  used by the power rule (same seeds) exactly.

Any change after this freeze is disclosed in RESULT.md as post-freeze.

Kappa = 1/2 FITTED; not theory closed.
