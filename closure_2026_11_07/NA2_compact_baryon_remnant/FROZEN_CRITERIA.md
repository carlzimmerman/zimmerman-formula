# NA2 frozen criteria: the hot-system half as a SEPARATE cause, a late-formed compact baryonic remnant population (1e2-1e7 Msun) under the a0 law

Frozen and committed alone, before any NA2 script or NA2 number exists. Adopts nothing. Kappa = 1/2 FITTED; not theory
closed. TEST lane: no particle, no LCDM input, no downloads; both footings (canonical a0 9.3603e-11 m/s^2, Lstar 21.7 pc;
alt a0 1.1312e-10 m/s^2, Lstar 22.9 pc), never pooled; a pass needs both. One thread, under 1 GB RSS, SIGTERM writes a
partial JSON and exits; peak RSS reported. Every input below is already on disk and is used read-only.

**This door does not touch the CMB wall.** It grades only the hot-system half of the seed (closure_2026_11_06/SEED_2026_11_06.md,
"show the two failures need separate causes"). The CMB-lensing half (cold extra gravity at z 3400) stays a separate wall:
late-formed compact baryons do not exist at z 3400 and are baryons already counted in the BBN budget, so they add nothing
there by construction. Nothing in this lane can pass or fail the CMB.

## 0. Why this door, and what the record already says

- **The clue (DOORS lane, 3f31773c79, QX7 iter_7):** every profile tried for the hot systems' missing mass misses the same way,
  too little in the centre and too much outside; a remnant tracing the hot gas fails the group shape; only profiles tracing all
  baryons including the stars fit X-COP (QX29 B1, -0.003/0.082 and -0.027/0.087). The missing mass is MORE CONCENTRATED than the
  hot gas.
- **DB1 (40e2665f48):** every CBDM reading fails; of the physical classes only 1e2-1e7 Msun black holes pass DB1's five gates,
  with no known formation channel; millilensing and dynamics at the high end not computed.
- **PB1-PB4 (PB2 f3af8b7cea, PB3 1e6606a77c, PB4 4dca9d97f8):** primordial BHs need f_b >= 0.2 and every decade 1e0-1e9 is CLOSED.
  The rows that close it, and whether each applies to a NON-primordial population formed late from baryons:

  | PB2 row | what dominates | applies to late-formed compact baryons? |
  |---|---|---|
  | A1, A2, A3 CMB accretion (z 300-1000) | 1e3-1e9 ROBUST envelope | **No**: the objects do not exist before they form |
  | P1 Ly-alpha / P2 Poisson isocurvature | 1e8-1e9 without A1 | **No**: no primordial Poisson noise; they inherit the adiabatic baryon field |
  | G1 LVK primordial binaries, G2 PTA, S1 mu distortion | 1e0-1e2 | **No**: primordial binary channel / Gaussian primordial peaks |
  | D1 wide binaries, D2 Eri II, D3 disc heating, D4 dynamical friction (MW) | 1e4-1e7 without A1 | **Yes, if** the population sits in the MW / UFDs at that density; it scales with the local amount the formation rule puts there |
  | L1 LMC, L2 quasar microlensing | <= ~1e1 | Yes in principle, but below this window (not binding at 1e2-1e7) |
  | L3 cosmological millilensing | 1e5-1e8 (f_b <= 0.32) | **Yes, CONDITIONAL** on formation before the lensed sources (z_f >= 2) |
  | X1 Galactic X-ray / radio accretion | 1e2 | Yes, scaled by the local amount |

  So the walls that shut PBHs at 1e3-1e9 (CMB accretion, Poisson) do not apply. What does apply is the dynamics of the systems
  that must carry the objects, accretion X-rays where gas is dense, millilensing, and the baryon budget (late-formed objects are
  inside Omega_b; PBHs were extra).

## 1. The model graded

A population of compact baryonic objects (CBOs: black holes or other dark remnants formed from baryons after BBN; no new
particle), all with one mass M_c in [1e2, 1e7] Msun (one mass function: a delta, scanned on a 0.25 dex grid; a log-flat
1e2-1e7 bracket is reported only), added to the baryons and acted on by the plain a0 law per footing (GB1 / QX7 interface:
g = g_law(G (M_b + M_cbo)/r^2)). One formation rule sets the CBO amount per system at formation, M_cbo = F M_b (per baryon)
or = eta M_* (per star); F or eta may depend on ONE formation-native key q (section 4). The objects are collisionless and,
as the clue requires, placed more concentrated than the hot gas: primary shape = the system's stars (X-COP: the BCG +
galaxies stellar profile `*_mstar.fits`; groups: all inside R2500, the most concentrated limit; dwarfs/UDGs: the stars'
Plummer profile). Brackets reported: X-COP CBOs tracing the HSE mass profile (`*_hydro_mass.fits`, M_FORW) and tracing the gas.

## 2. Inputs (all on disk, read-only)

- Class amounts (canonical / alt), uniform per-baryon F in GB1's L0 convention (b = 1 + F): X-COP 4.1786 / 3.7833 and SPARC
  cap 0.3257 / 0.1937 (KD1 `kd1.json` uniform_f_diag); groups 1.23-3.46 / 0.93-2.86 (KD1 f* 1 / f* 0); bright M31 dSphs
  1.64 / 1.50 and Coma UDGs >= 23.6 / 20.2 (ST1 RESULT.md, favourable-edge; raw 86.4 / 77.7); LG field dwarfs 0.
- Class allowed F intervals for section 4 (SE2 95 % posterior, model U, PB3 `pb3.json` footings.*.U.intervals): SPARC, X-COP,
  groups f* 0 / 1, ellipticals, KiDS, bright M31, Coma UDGs. LG field dwarfs (not in PB3): [0, F_hi] with F_hi from SE2's LG
  field ci95 upper edge through the deep-MOND map Delta = 0.5 log10(1 + F) (frozen approximation, disclosed).
- Per-point keys from GB1's battery (`gb1.py`, loaded read-only as PB3 does): Mb, r, v, sigma, fgas.
- X-COP: `real_research/data/xcop/*/` (_fgas_profile, _mstar, _hydro_mass) through QX7 iter_5/iter_7's loaders (exec'd from
  source, unchanged); groups: QX7's GR table.
- Baryon budget: eRASS1 primary catalogue on disk (`real_research/data/erass1cl_primary_v3.2.fits`; MGAS500 measured from the
  X-ray surface brightness; the catalogue's own distance convention h = 0.70). BBN: Omega_b h^2 = 0.02166 from primordial D/H
  (Cooke+2018), a measurement of D/H plus nuclear rates, not an LCDM fit, PROVISIONAL and from memory exactly as DB1 and PB3 used
  it (no Planck number). rho_b = Omega_b h^2 x 2.775e11 Msun/Mpc^3 needs no h; the catalogue gas density scales as h^(1/2),
  bracketed h 0.67-0.74.
- PB2 `pb2_fmax_results.json` FW ceilings (rows D1, D3, D4, L3, X1) as frozen there; DB1 `db1_phys.json`; PB3 `pb3.json`,
  `pb3_bullet.json`; DB1's Bullet machinery (`db1_fast.py`, exec'd read-only exactly as PB3 does).
- t_H = 13.8 Gyr (as PB3; PROVISIONAL convention).

## 3. (a) Amount and budget

- Per class: needed CBO mass = F x M_b (table of section 2), and the progenitor baryons needed if the CBOs formed in place
  (1 + F) M_b. Reported per class and footing.
- **Budget gate B1 (can kill: DEAD).** Lower-bound census: eRASS1 clusters with 0.02 <= z <= 0.10 and PCONT <= 0.5,
  Euclidean volume D = cz/H0 at h 0.70 over 20,626 deg^2 (the whole German half sky, which can only understate the density).
  Hosts with M500 >= 1e14 Msun carry the X-COP F; 1e13 <= M500 < 1e14 carry the groups F (upper end of each footing's range).
  Host baryons M_b = M_gas (1 + s), s = X-COP's mean M_*/M_gas at R500 for clusters, s in {0, 1} for groups (worse taken).
  B1 = (1 + F) Sigma M_b / (rho_b V). **B1 > 1 on either footing: DEAD.** B1 <= 1 reads "not excluded by the census" only
  (a lower bound cannot pass a budget). Brackets reported: area 13,116 deg^2, PCONT <= 0.2, h 0.67 / 0.74, z <= 0.05.
- Reported, PROVISIONAL, no label: DB1's census reading (hot cluster gas 4-10 % of cosmic baryons) times (1 + F), and the cosmic
  CBO share f_b,cbo used by the L3 row.

## 4. (b) One formation rule without a class label

Keys (formation-native, per point from the battery): q1 = f_* = 1 - fgas (gas-free dSph/UDG/ellipticals: 1); q2 = M_b at the
point; q3 = Sigma_b = M_b / (pi r^2) (dSph/UDG: M_b / (2 pi r_h^2)); q4 = v (the battery's characteristic velocity). Two
conventions: per baryon (the class F interval) and per star (eta interval = F interval / f_*, per point). Dead keys of the record
(depth / g_N, temperature, environment, enclosed density) are not re-proposed; q3 is close to depth and is graded anyway.

- **S1 existence (OQ1 S1):** bin log10 q at 0.2 dex; in every bin with points from two or more classes, intersect their
  allowed intervals; any empty intersection = key DEAD on that footing (bin, classes, gap in dex reported).
- **S3 prediction (OQ1 S3, frozen text):** only if S1 holds: leave-one-class-out, rebuild F(q) (piecewise-linear in log q
  through bin midpoints) without class k and predict k (interpolation or extrapolation <= 0.5 dex in log q; beyond that k is
  UNCONSTRAINED BY OTHERS). A hot class whose q range touches no other class's range makes the rule a class label.
- **Spread** reported: max / min class median F (SPARC at its cap), per footing.
- (b) reads ONE RULE EXISTS only if some key in some convention passes S1 and S3 on both footings; otherwise NO ONE RULE.

## 5. (c) Dynamics of 1e2-1e7 Msun objects in each class (grid 10^2 ... 10^7 at 0.25 dex)

Each class carries its section-2 amount (needs-based, independent of the rule); per point, rho_cbo = F M_b / 2 / (4/3 pi r^3)
(half the mass inside the point radius r; r_h for dwarfs and UDGs), sigma from the battery (v / sqrt(2) where sigma is absent),
lnLambda = ln(r sigma^2 / (G M_c)) floored at 1. Newtonian two-body physics with the measured sigma (which already carries the
law's field); the law bracket (times 1/nu at the point) is reported.

- **C1 heating of the stars by the CBOs** (dSphs, UDGs, LG field at the SPARC cap as a reported row): t_heat = sigma^3 /
  (8 pi G^2 M_c rho_cbo lnLambda) >= t_H, class median over points.
- **C2 dynamical friction sinking** (all needing classes): t_DF = 1.17 r^2 (sqrt 2 sigma) / (G M_c lnLambda) >= t_H, class
  median; the law bracket t_DF / nu is reported and the graded value is the shorter.
- **C3 Bondi-Hoyle X-rays in X-COP:** CBOs on the fitted stellar shape (section 6); gas density from d MGAS/dr; kT from HSE,
  kT = mu m_p G M_FORW / (r s), s = -dln rho_gas/dln r, mu 0.6; Mdot = 4 pi lambda G^2 M_c^2 rho / (c_s^2 + v^2)^{3/2}, lambda 0.25,
  c_s^2 = (5/3) kT/(mu m_p), v^2 = 3 kT/(mu m_p); L = eps Mdot c^2 with eps = 0.1 min(1, mdot/0.01) (mdot in Eddington units).
  Gate: L_acc(<R500) <= 0.1 L_brems(<R500) (L_brems from the same rho, T: 1.4e-27 T^1/2 n_e n_i g_B, g_B 1.2), cluster median.
  eps = 0.1 everywhere is reported as the upper bracket.
- **Window:** the set of M_c passing C1-C3 in every needing class (X-COP, groups, bright M31, Coma UDGs). **Empty on either
  footing: DEAD.** A class with no allowed M_c is a failed row.
- Reported rows (not window gates; they constrain how much the rule may put in MW-like discs and when it forms):
  PB2 FW D1, D3, D4, X1 read at f_b = the SPARC cap (largest M_c allowed if discs carry the cap); L3 at the cosmic share
  f_b,cbo from section 3, CONDITIONAL on z_f >= 2 (NOT EVALUABLE for later formation). Cluster millilensing (kappa_cbo,
  granularity of lensed sources) and caustic-transient stars: **NOT EVALUABLE** (no lensed-source data on disk); the order of
  magnitude is PB3's and is restated, not graded.

## 6. (d) Radial SHAPE in X-COP and groups (DOORS construction, per bin, not one amplitude)

QX7 iter_5/iter_7's X-COP and group machinery, read-only, with switch retention off (everyone keeps). Per footing, one amplitude
per shape fitted on X-COP alone (F_X = M_cbo / Mb_last minimising X-COP rms, golden search on [0, 30]); groups get their own
amplitude per f* (minimising the sum of squared Delta over the 40 points).
- **X-COP shape gate:** |mean| <= 0.05 AND rms <= 0.10 (HO1 lines) AND every r/R500 bin (edges 0, 0.25, 0.5, 0.75, 1.0, 2.0;
  bins with >= 3 points) has |bin mean| <= 0.10.
- **Groups shape gate:** >= 16 of 20 within 2 sigma at f* 0 AND f* 1 (iter_7's strict rule).
- Primary shape = stars (section 1). Graded rows: X-COP stars, groups all-inside-R2500. Brackets reported with their own fitted
  amplitude: HSE-traced, gas-traced, baryon-traced.
- **Bullet row:** DB1's Bullet machinery with the CBOs on the galaxies, R_j = M_cbo / M_* = eta_X (the per-star amount X-COP's
  fitted stellar-shape F implies, F_X Mb_last / M_*,last, cluster median); label as bullet_row returns it.

## 7. Labels (per footing; the overall takes the worse; precedence top to bottom)

- **NO VERDICT:** any known answer fails or any MUTATE that must bite does not (numbers read reported).
- **DEAD:** B1 > 1, or the section-5 window is empty.
- **FAILS (rows):** neither, but a graded row fails (X-COP shape, groups shape, Bullet, a needing class with no allowed M_c).
- **CONSISTENT, NOT PREDICTIVE:** every row passes but (b) reads NO ONE RULE: the amounts would be a class label.
- **SURVIVES (scoped):** every row passes and ONE RULE EXISTS. Even then: not adopted, not closure; it owes a formation channel
  (DB1: none known that turns ~4x the hot gas into dark objects without stars or metals), cluster millilensing, the L3 epoch,
  and the CMB half stays open.

## 8. Known answers (fail = stop and fix; nothing is graded until they pass)

- KA1 (DOORS shape result): gas-traced CBOs at F = f_cap R (iter_7's 0.76 x 5.562) reproduce iter_7's X-COP +0.0189/0.1003
  and -0.0055/0.0996 to 1e-3, and baryon-traced reproduce K2 -0.0029/0.082 and -0.0269/0.087 to 1e-3 (qx7_iter7.json).
- KA2: F = 0 gives X-COP +0.4675 / +0.4345 (QX2, iter_7 MUTATE A) to 1e-3.
- KA3 (DB1): db1_phys.json has exactly one surviving class, the 1e2-1e7 Msun black holes, and M_cb/M_gas at 300 kpc for P1G/P3
  spans 4.4-5.4 (PB3 KA1).
- KA4: class amounts read from kd1.json equal section 2 to 1e-4; pb3.json U intervals load for every class listed.
- KA5: Bullet at R = 0 gives M300 1.112e14 / 7.337e13 and dkappa -0.068 / -0.111 (DB1 K1, PB3 KA4).

## 9. MUTATE (must bite; separate outputs na2_MUTATE_*.json / .out)

- M1 (shape power to pass): replace X-COP M_obs by the law with star-traced CBOs at F = 3; the fit must recover F within 2 %
  and the X-COP shape gate must PASS on both footings.
- M2 (shape power to kill): replace X-COP M_obs by the law with gas-traced CBOs at F = f_cap R; the star-traced fit must FAIL
  the X-COP shape gate on both footings.
- M3 (rule power to pass): replace every class interval by the image of a planted F_true(q) = 10^(0.3 log10 q - c) over that
  class's own q range (x/÷ 1.2); S1 must find no empty bin for that key.
- M4 (rule power to kill): M3 plus x10 on the hot classes (X-COP, groups, Coma UDGs); S1 must read DEAD.
- M5 (dynamics bites): M_c = 1e9 Msun must fail C1 or C2 in the Coma UDGs and the bright M31 dSphs.
Any of M1-M5 failing as required: the label is NO VERDICT.

## 10. Outputs

`na2.py` writes `na2.json` / `na2.out`; `na2.py --mutate` writes `na2_MUTATE.json` / `na2_MUTATE.out`. RESULT.md gives the label
line, the per-class / per-footing table with margins read from the JSON, MUTATE status, peak RSS, and any post-freeze change as
a disclosure.

Kappa = 1/2 FITTED; not theory closed.
