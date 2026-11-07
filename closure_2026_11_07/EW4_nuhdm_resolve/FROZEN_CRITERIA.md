# EW4 frozen criteria: nuHDM (the a0 law + one ~11 eV thermal fermion), HC1 vs Angus resolved, graded on its own terms

TEST lane. Adopts nothing. **The no-dark-matter-particle rule is relaxed for this lane only, as it was for HF1 and
HC1** (owner 11-07: "we need to get all actions that work everywhere"). Otherwise closure_2026_11_06/SWARM_BRIEF.md
binds. Kappa = 1/2 FITTED; never 'theory closed'. Both footings (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2),
never pooled. No LCDM inputs (LCDM appears only as COMPARISON-ONLY notes). No downloads. Frozen and committed alone,
before any EW4 script or EW4 number exists. Compute: nice -n 15, <= 2 threads, small outputs.

## 1. Why HC1 (FAIL) and Angus (cluster fits) disagree: the differences, stated before grading

Literature items are from memory, no download: **[lit, PROVISIONAL]**. Record items cite their commit.

| Item | Angus 2009; Angus, Famaey & Diaferio 2010 [lit, PROVISIONAL] | HC1 (c207d70254 / 27edbba890) | Same? |
|---|---|---|---|
| Fermion mass | 11 eV sterile, thermal at T_nu, g = 2, Omega_s h^2 ~ 0.117 | 11.1377 eV = 93.14 eV x omega_d 0.11958 (QX3 iter2 worst corner), T_nu, g 2 | Same to 1.3 %. Not the cause |
| How m was fixed | CMB acoustic peaks with a Lambda-like background (CAMB) | the record's own CMB-lensing cold share (QX3 iter2), not floated | Different route, same m |
| Phase-space bound | Tremaine-Gunn, rho_max = m^4 (g/2h^3)(2 pi sigma^2)^(3/2) at the neutrino's local dispersion | same closed form (hf1_fermion.rho_cap, f_max = g/2h^3) | Same form. Not the cause |
| sigma in the bound | from the Jeans equation of the inferred neutrino profile in the observed potential | V_max/sqrt 2 of the self-consistent law+fermion MODEL | Different |
| **The test itself** | **consistency**: infer the fermion density each cluster needs (hydrostatic mass minus MOND-on-baryons), ask whether phase space allows it. Amount and profile are free per cluster | **prediction**: amount fixed by cosmic fair share R = 5.562 inside turnaround r_ta (several Mpc), profile isothermal in the model potential, capped; then graded against data | **Different: the main cause** |
| Cluster sample | ~30 Chandra groups and clusters (Vikhlinin+2006, Gastaldello+2007) | X-COP 12 clusters (GB1, 0.1-0.7 R500) + Lovisari 2015 20 groups | Different |
| Radii | outside the cores; reported failure in cluster centres (r <~ 100-150 kpc) and in groups with T <~ 2 keV | 0.1, 0.2, 0.3, 0.5, 0.7 R500; groups at R2500, R500 | Different |
| Hydrostatic masses | Chandra X-ray only | X-COP forward HSE (X-ray + SZ pressure), Lovisari XMM | Different |
| Interpolation | simple mu, a0 ~ 1.0-1.2e-10 | simple nu (GB1 glaw), a0 0.936 / 1.131e-10 | Same family; lower a0 here (more missing mass) |
| Background | Lambda + 11 eV sterile, H0 ~ 70-72 (LCDM-like expansion: COMPARISON-ONLY) | framework footing background (QX10 rule) | Different; enters only through m and r_ta |
| Literature's own verdict | consistent in T > 2 keV clusters outside cores; FAILS in groups T < 2 keV and in the centres | FAIL: supply-limited (M_f/M_b 0.31 at X-COP's radii), wrong shape (HF1 pipeline +0.42 at 0.1 R500, -0.09 at 0.7 R500) | Partly the SAME conclusion |

Hypothesis stated in advance (graded below, not assumed): the two are not in direct contradiction. Angus's fits are a
consistency reading with a free per-cluster profile; HC1 is a prediction with a fixed amount and profile. EW4 runs the
consistency reading (C) on the record's own clusters and groups, so both readings exist on the same data.

## 2. The candidate, fixed once

- Fermion: thermal relic, g_f = 2, T_f = T_nu (CLASS T_ncdm 0.71611, deg 1), **m = 11.1377 eV** (HC1's value; the record's
  own route: omega_f = omega_d of QX3 iter2's worst corner = 0.11958; Angus's 11 eV is the literature cross-check). R =
  omega_f / omega_b = 5.5619. No m grid. No constant tuned to any gate.
- Phase-space bound (published form, Tremaine & Gunn 1979): rho_TG(sigma) = m^4 (g_f / 2h^3)(2 pi sigma^2)^(3/2), via
  hf1_fermion.rho_cap read-only.
- Field rule (HC1 rule TOT): g = g_law(g_N,b + g_N,f), g_law(x) = x/2 + sqrt(x^2/4 + a0 x) (GB1 glaw, simple nu).
  Inverse: g_N,tot = g_obs^2 / (g_obs + a0).
- MOND part for Cassini / c_T (stated per cell): the record's v3s / AC2q action (static = law) and, for the literature
  version, Angus's QUMOND.

## 3. Two readings per static cell and the cell label rule

- **C (consistency, Angus's test, on the record's data).** Required fermion mass M_req(<r) = r^2 g_N,tot(g_obs) / G -
  M_b(<r). Necessary conditions for SOME fermion profile to exist:
  - (C-a) no negative fermion: on each shell, Delta M_req + 2 err >= 0 (otherwise the law over-predicts there and adding
    a fermion cannot help);
  - (C-b) phase space: the shell (or central sphere) mean required density, at its 2-sigma LOWER edge, must not exceed
    rho_TG(sigma), because any local density is <= rho_TG and the mean of a region cannot exceed the region's maximum.
    sigma = V_c,max,obs / sqrt 2 (isothermal dispersion at the largest observed circular speed in the system's measured
    range), graded. Generous reading sigma = V_c,max,obs reported only.
  - err on a shell = quadrature of the endpoint hydrostatic mass errors (generous for correlated errors).
  - Supply (reported only): M_req at the largest graded radius / (R M_b there).
- **P (prediction, HC1's frozen R4 rule):** the record's HC1 numbers, carried by commit (same m, same bound). Rerun
  only for KiDS G6 (section 4.6), which HC1 did not run.
- **Cell label:** C FAIL -> **FAIL** (robust: no phase-space-allowed profile works). C PASS and P FAIL -> **FAIL**
  [prediction], written "FAIL (P); C consistent". Both PASS -> **PASS**. Missing data -> **NOT EVALUABLE** (NEEDS_OWNER.md).

## 4. Cells (both footings, never pooled)

### 4.1 X-COP clusters (GB1's QX5 loader, read-only; 12 clusters, X-COP M_FORW / EM_FORW, gas + stars)
- Regions per cluster: central sphere 0 -> 0.1 R500, shells 0.1-0.2, 0.2-0.3, 0.3-0.5, 0.5-0.7 R500, using only radii
  where QX5 returns finite hydrostatic, gas and stellar masses. Masses at a radius from QX5's li() interpolation.
- Cluster consistent iff every region passes C-a and C-b. **C PASS iff >= 10 of 12 clusters consistent** (the GB1
  groups' 80 % count line, 16/20, applied to 12).
- P: HC1 G2 FAIL (+0.392 / +0.360; HF1 pipeline +0.178 / +0.147).
- Reported: per-cluster failing regions, the inner radius in kpc below which C-b fails (Angus's "core" statement), supply.

### 4.2 Groups (QX20 / GB1 loader, Lovisari 2015, 20 groups, f* = 0 and 1)
- Regions: sphere 0 -> R2500, shell R2500 -> R500; baryons M_gas (1 + f*); err from eM2500, eM500.
- **C PASS iff >= 16 of 20 consistent for f* = 0 AND f* = 1.** P: HC1 G3 FAIL (0 and 3 of 20).
- Reported: kT split at 2 keV (the literature's line), counts above and below.

### 4.3 Ellipticals (QX5 loader, GB1's 2, 4, 8 Re): C on sphere 0 -> 2 Re and shells 2-4, 4-8 Re with M_obs from
QX5's Mtot(r); no per-point mass error in the loader, so err = 0 (stated). C PASS iff >= 80 % of galaxies consistent.
P: HC1 G4 FAIL.

### 4.4 SPARC: the fermion must not collect in discs
- Phase-space ceiling for ANY profile: M_f(<r) <= (4 pi/3) r^3 rho_TG(V_max,obs / sqrt 2). Put the ceiling in at
  every point and grade GB1's G1 line (|Z| <= 0.057 AND rms <= rms(L0) + 0.010). PASS at the ceiling = robust PASS.
  If the ceiling fails G1, the cell takes HC1's P reading (G1 PASS) and is marked "not robust".
- Reported: rho_TG per galaxy (Msun/pc^3), median and max M_f,max / M_b at R_last.

### 4.5 UDGs: AGC 114905 (UD1, 167a274304) and Malin 1 (UD2, 46d8dcd8c5), primary inputs of those lanes read-only
- A fermion can only ADD Newtonian field, and g_law is increasing, so V_nuHDM >= V_law at every ring. Lower bound on
  any fermion profile: chi2_min >= sum over rings with V_law > V_obs of ((V_law - V_obs)/E)^2.
- **FAIL iff p(chi2_min, N rings) < 0.01** (UD1/UD2's FAIL line), per footing. Otherwise C PASS and the cell needs P:
  P = the HC1 cap at sigma = V_max,obs/sqrt 2 (UDG phase-space ceiling as 4.4) graded on the same chi2 line.
- Coma UDGs: HC1 G5, FAIL at the maximum bound (+1.000 / +0.953 dex, 3.8 / 3.6 sigma_U) = C FAIL, carried.

### 4.6 dSphs and KiDS
- dSphs: HC1 G6 carried (P FAIL, bright M31 CI misses 0 by +0.094 / +0.086). C reading = HC1's maximum bound (Delta_max
  1.75 / 1.74 for bright M31: room exists). Label by section 3; the host-sea dependence (hc1_report) is restated.
- KiDS colour split: HC1 G7 carried (FAIL, R 2.42 sigma, no split).
- **KiDS G6 (QX10 / EW2 line, computed here):** QX5's LE list (Brouwer+21 isolated, 4 mass bins), Hernquist baryons
  a_h = 3 kpc, each LE point at r = sqrt(G Mb / gbar); the fermion by HC1's R4 rule (hf1_fermion.solve, fair share in
  r_ta, isothermal, TG cap; HC1's grid and r_ta form); shift_i = log10(g_law(g_N,b) / g_law(g_N,b + g_N,f));
  G6 = mean. **PASS iff |G6| <= 0.05 dex.** C for KiDS is trivially consistent (the law fits; M_f = 0 allowed).

### 4.7 Cassini / PPN and c_T
- With the record's v3s / AC2q as the MOND part: Cassini and c_T inherit R10/R11 (C6P 8c5703da06; V3W; AC9) plus the
  fermion's local field at the Milky Way cap (HC1 G8: 1.3e-20 m/s^2 at Saturn). PASS iff the fermion field is < 1e-3
  of the Cassini-derived bound used by GB1 G8 (use <= 1 there).
- With Angus's QUMOND (the literature nuHDM): Cassini FAIL (AX1 Q2 1.70-3.70x / 1.91-4.03x Hees); c_T N/A
  (non-relativistic). Both written; the cell label names the action.

### 4.8 CMB
- **Primary CMB:** QX15's grader (qx15_like.grade_spectra, PR4 CamSpec cut + ACT DR6, data on disk) with CLASS: omega_cdm
  = 0, one ncdm species m 11.1377 eV, T_ncdm 0.71611, deg 1, N_ur 3.046 (the relic's own Delta N_eff ~ 1 comes from the
  ncdm), footing background by QX15's background() with od = omega_f fixed. Fit (omega_b, ln A_s, n_s, tau) by
  Nelder-Mead from QX15's main best fit, maxfev 120, QX15's brackets. **PASS iff Delta = chi2_PA - 3805.80 <= 9**
  (QX15's L1 line), FAIL if > 25, TENSION between. Run only if one CLASS evaluation takes <= 60 s at 1 thread; else NOT
  EVALUABLE and the literature (Angus 2009 PASS with a Lambda background [lit, PROVISIONAL]) is cited.
  - KA-CMB: CLASS with omega_cdm = omega_d (cold) at QX15's canonical main theta reproduces chi2_PA 3741.08 within 5;
    if not, the cell is NOT EVALUABLE.
- **CMB lensing:** HC1 G9 carried, FAIL (chi2 166-194 vs 18.48, footing-free; linear, no a0 term).

## 5. Known answers (any KA FAIL: stop, nothing graded)
- KA1: with M_f = 0 the harness reproduces GB1's L0 X-COP mean and rms and groups counts (gb1.json) to 1e-6, both footings.
- KA2: rho_TG via hf1_fermion.rho_cap equals the closed form above to 1e-12.
- KA3: SPARC G1 with M_f = 0 reproduces GB1 L0 Z and rms to 1e-9.
- KA4: UD1/UD2 law chi2 recomputed from their json (V, E, Vlaw) equals their reported chi2 to 1e-3 relative.
- KA5: KiDS G6 with M_f = 0 gives 0 to 1e-12.

## 6. MUTATE (separate outputs, *_MUTATE.*)
- M1 fermion mass x 0.5 (5.5689 eV; rho_TG / 16), everything else fixed: **must FAIL clusters** (C on X-COP) on both
  footings: the phase-space bound must bite. If C already fails at m, bite = strictly more failing clusters at m/2.
- M2 no fermion: C with M_f = 0 must FAIL X-COP (law-only miss), and the harness must give GB1 L0's X-COP mean
  (+0.468 / +0.435). If either does not bite, the run says NO POWER.

## 7. Overall line
"Does nuHDM pass every column EW1 has?": YES only if every EW1 column for R22 is PASS. EW1 columns not graded here
(wide binaries OPEN, galaxy lensing, Bullet [lit], growth, BBN, causality, a0 tie) keep EW1's cells, quoted.

Any change after this freeze is disclosed in README.md as post-freeze. Kappa = 1/2 FITTED; not theory closed.
