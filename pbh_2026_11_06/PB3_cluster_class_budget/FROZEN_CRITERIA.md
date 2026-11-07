# PB3 FROZEN CRITERIA: a uniform-born primordial black hole (PBH) population as the cluster / class extra mass

Written and committed alone, before any PB3 script or PB3 number. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
No particle: PBHs are compact objects born before BBN, but **their mass is a component that must be paid for**. A
population that is F times the baryons everywhere is, in the bookkeeping, a cold collisionless mass component; if F
comes out near 4 it is Omega_PBH ~ 4 Omega_b, i.e. a cold sector by another name (the cold sector stays RETIRED,
11-01; nothing here reinstates it). Footings canonical / alt graded separately, never pooled.

## Question
Can PBHs born as a fixed ratio F = M_PBH / M_baryon everywhere supply (i) DB1's cluster deficit and (ii) SE2's class
pattern (X-COP, groups, Coma UDGs NOT EXPLAINED; ellipticals, KiDS, bright M31 EXPLAINED), while (iii) staying out of
SPARC discs, with only physical segregation (no class tags)?

## Inputs (read-only; never edited)
- GB1 battery `closure_2026_11_06/GB1_all_gates_battery/gb1.py` (loaders, features, delta, gates; 7ca0d54d47), exec'd
  read-only exactly as DX1 does (`load_prefix` up to "# ---- main" plus the `short` block).
- KD1 `kd1.json` uniform_f_diag (c4008a456c): SPARC_f_max 0.326 / 0.194, needs X-COP 4.18 / 3.78, groups f*0 3.46 /
  2.86, f*1 1.23 / 0.93, E 0.86 / 0.77, bright M31 1.68 / 1.27, MW classical 1.82 / 1.41, UDG 86.4 / 77.7.
- DX1 `dx1.json` (515dad3b5d): oracle O1 rows (f = 0 in disc set, KD1 capture 4.111 / 4.112 elsewhere).
- SE2 `se2.json` (59b101bbd7): per class x footing posterior step (median, ci95).
- DB1 `db1_phys.json` amounts_300kpc (40e2665f48): M_cb/M_gas at 300 kpc, X-COP median; Bullet machinery in
  `db1_fast.py` (UX6 model through RQ3's bullet_ns), exec'd read-only from its source with its output file handle
  replaced in memory by a StringIO (no file in DB1's dir is written).

## Models (the extra mass is ordinary mass the law acts on: g = law(g_b + g_PBH), i.e. GB1 candidate b = 1 + g_PBH/g_b, F = 1, T = 0)
- **U (no segregation):** b = 1 + F at every point (KD1's uniform convention). Baseline.
- **I (collisionless vs dissipative infall; primary):** gas cools and settles to where the baryons are observed; PBHs
  do not dissipate and stay in a spheroid set by the infall: total M_PBH = F M_b,tot, singular isothermal
  M_PBH(<r) = F M_b,tot min(r / r_vir, 1), r_vir = [3 (1+F) M_b,tot / (4 pi 200 rho_c0)]^(1/3), rho_c0 at h = 0.70
  (PROVISIONAL convention, not a framework number). Then b = 1 + M_PBH(<r) / M_b(<r).
  - Brackets (reported, labels from I primary only): r_vir x s with s in {0.5 (z_f ~ 1), 2 (more extended)}; and a
    Hernquist profile (a = r_vir / 10, normalised to F M_b,tot at r_vir, constant beyond).
- Per class: M_b(<r) and M_b,tot from GB1 features. SPARC, X-COP, groups, ellipticals: M_b(<r) = feat Mb, M_b,tot from
  feat rrM (M_b,tot = a0 (r / rrM)^2 / G). Coma UDGs: M_b(<r_h) = Ms/2, M_b,tot = Ms. dSphs: M_b(<r_h) = Ms/2,
  M_b,tot = Ms (points without Ms keep b = 1, counted and disclosed). KiDS lenses: M_b(<r) = M_b,tot = x a0 r^2 / G.
  Solar System: b = 1 (a uniform PBH background adds no field at AU scales to this order; disclosed).
- Not modelled (disclosed): adiabatic contraction (pulls PBHs in: wrong sign for discs); feedback expulsion of
  baryons (raises F locally; reported as the epsilon each class would need, no label).

## Targets and per-class shift
- Class PBH shift Delta (dex) = mean over the class of GB1 delta (X-COP, groups, ellipticals, UDGs); KiDS = GB1
  D_cand (early minus late); dSph classes = median delta minus SPARC mean delta (SE2's anchor convention).
- **T_SE2 (graded):** the class is reproduced if Delta lies inside SE2's 95 % posterior interval for that class and
  footing (the remaining step after systematics must be absorbed; EXPLAINED classes must not be over-filled beyond
  their interval). Groups graded at f* 0 and f* 1 separately: REPRODUCED only if both inside, FAILS if both outside,
  else BRACKETED. MW classical, LG field, M31 others: NOT A TEST (reported).
- **SPARC (graded):** GB1 G1 pass (|Z| <= 0.057, rms <= L0 + 0.010).
- T_raw (reported): GB1 gates G1-G8 as-is under each model at F*.

## Numbers computed
1. **Mass budget.** Per model, class, footing: F needed to bring the raw class residual to 0 (KD1-style brentq on
   log F in [-4, 4]) and F needed under T_SE2 (Delta = SE2 posterior median); SPARC F_max by bisection on G1 (as
   KD1). Needed segregation factor per class = F_need(class) / F_need(X-COP), and the spread = max / min over graded
   classes, with SPARC entering as an upper bound. X-COP F converted to M_PBH / M_gas at 300 kpc for comparison with
   DB1 (not a KA). Omega_PBH = F Omega_b with Omega_b h^2 = 0.02166 (BBN D/H, PROVISIONAL, as DB1), h = 0.70.
2. **Segregation processes** (order of magnitude, representative systems: SPARC disc r 10 kpc v 150 km/s; dSph
   0.3 kpc, 10 km/s; Coma UDG 3 kpc, 25 km/s; elliptical 10 kpc, 250 km/s; group 100 kpc, 400 km/s; cluster 300 kpc,
   1000 km/s; host baryon masses stated in the script; M_PBH grid 1e2-1e7 Msun):
   - S1 dynamical friction: t_df = 1.17 r^2 v / (G M lnL), lnL = max(ln(r v^2 / (G M)), 1); r_sink where t_df =
     t_H = 13.8 Gyr; sunk fraction of an isothermal spheroid = r_sink / r_vir. Newtonian (the law's phantom
     background only strengthens it; sign unchanged).
   - S2 two-body relaxation: N = M_PBH(<r) / M; t_rel = 0.1 N / ln N x r / v; evaporated fraction 1 - exp(-0.045
     t_H / t_rel) (tidal rate, generous); stellar heating time by the PBH sea t_heat = v^3 / (G^2 rho_PBH M lnL)
     reported.
   - S3 disc vs spheroid: model I itself (the SPARC F_max under I).
   - S4 infall factor: per class median of [M_PBH(<r) / M_b(<r)] / F under I (the segregation the infall model
     delivers), vs the needed factor from 1. Baryon expulsion epsilon needed per class: F_local = F / (1 - eps).
3. **Bullet.** DB1's own bullet_row with PBHs placed on the galaxies (collisionless, DB1 arm P1 placement): per
   subcluster R_j = F* (M_gas,j + M_st,j) / M_st,j, F* = X-COP T_SE2 need under U (cluster interior ~ uniform).
   DB1's pass rule (classification not FAIL and |Z_M300| <= ZL). If one run exceeds 15 min it is stopped and the
   Bullet row is read qualitatively from DB1's P1G / P3 rows (disclosed).
4. **Millilensing / granularity.** Per X-COP cluster N_PBH(<300 kpc) = M_PBH / M; PBH convergence share at a cluster
   Einstein radius kappa_PBH = Sigma_PBH / Sigma_eff with Sigma_eff from the law (X-COP points nearest 150 and 300 kpc),
   Sigma_cr at D_eff 1 Gpc (DB1); theta_E(M) = sqrt(4 G M / (c^2 D_eff)); astrometric jitter ~ theta_E sqrt(kappa_PBH),
   flux-ratio perturbation order unity for sources smaller than theta_E in the source plane. Order of magnitude, a
   prediction, not graded; outside bounds are PB2's job.

## Labels
- Per class x footing (model I primary, at F* = the F that puts X-COP's Delta on SE2's X-COP median): REPRODUCED /
  FAILS (groups may be BRACKETED). Footings that disagree: SPLIT.
- **Overall:**
  - **PATTERN REPRODUCED:** under I primary, on both footings, the F intervals of all graded classes (SPARC G1;
    T_SE2 for ellipticals, KiDS, X-COP, groups f*0 and f*1, bright M31, Coma UDGs) have a non-empty intersection.
  - **PARTIAL:** not that, but SPARC G1 and X-COP T_SE2 intersect under I primary on both footings.
  - **FAILS:** SPARC and X-COP do not intersect under I primary (either footing failing = FAILS on that footing;
    both = FAILS).
  - Brackets (s = 0.5, 2, Hernquist) and U reported; if a bracket flips the overall label it is stated, label stays.

## Known answers (all must pass before any label)
- KA1: DB1 M_cb/M_gas at 300 kpc read from db1_phys.json: P1G 4.82 / 4.36, P3 5.44 / 4.82 (the record's "4.4-5.4"),
  printed exactly; and GB1 L0 class means vs KA20 to <= 1e-6 (DX1's KA1).
- KA2: under U, every KD1 need and SPARC_f_max re-derived to <= 1e-6 relative.
- KA3: SE2 posterior medians / ci95 read from se2.json match SE2 RESULT.md's table to its printed rounding.
- KA4: DB1 Bullet machinery at R = 0 reproduces DB1's K1 (M300 1.112e14, 7.34e13; dkappa -0.068, -0.111) to 1 %.
  (Skipped with disclosure only if the Bullet run is stopped for time.)

## MUTATE (must hold / must bite)
- M1: planted perfect segregation (b = 1 + 4.111 / 4.112 on DX1's hot set, b = 1 on DX1's disc set, same tags)
  through PB3's grading path reproduces DX1 O1's graded numbers to <= 1e-12 and its labels exactly.
- M2: F = 0 in every model returns GB1 L0 (dx1 KA2 style compare, <= 1e-12, statuses equal).
- M3 (bite): model U at F* must FAIL SPARC G1 on both footings.

## Seen before freezing (disclosed)
KD1 needs and capture 4.11; DX1 O1 table and its ~100x spread statement; SE2 table; DB1 README tables (amounts, Bullet
rows P1 / P1G / P3, gates, 1e2-1e7 Msun window). Hand estimates made before freezing with model I: SPARC F_eff ~ 0.25 F
at the last radius (against an allowed ~0.3 with F ~ 4 needed), Coma UDG ~ 0.4 F (needed ~ 80), dSph ~ 0.08 F,
ellipticals ~ 0.1 F; Bullet expected between DB1's P1G and P3 rows. Expectation: FAILS on SPARC vs X-COP and on UDGs.
Machine load ~38: one thread, small compute only, no downloads.

kappa = 1/2 FITTED; not theory closed.
