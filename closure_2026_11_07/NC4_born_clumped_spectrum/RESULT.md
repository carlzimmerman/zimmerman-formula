# NC4 RESULT: the born-clumped clump spectrum. FAILS (rows) on both footings; binding K3 (cosmic share), K5 also fails

**NC4 = Framework Candidate 2's NC1.** Criteria `FROZEN_CRITERIA.md`, 54784e16e5 on origin, committed alone before any
script or number (NC3's core rule folded in before freeze). Scripts `nc4.py` (main) and `nc4_r7.py` (R7 child, separate
process). Outputs `nc4.json` / `nc4.out` / `run_main.txt` and `nc4_MUTATE.json` / `nc4_MUTATE.out` / `run_mutate.txt`.
Every number below is read from those files. TEST lane. Adopts nothing. Kappa = 1/2 FITTED; not theory closed.

**Label line:** canonical: FAILS (K3, K5) | alt: FAILS (K3, K5) | overall: **FAILS (rows): K3, K5; binding K3** (the
observed hosts can hold 0.8-2.5 % of the cosmic cold dark energy, so the clump abundance would have to be 40-128 times
the observed host abundance). R7 PASSES on both footings for a fitted slope (s_f 0.8-2.2 per dex common to both).

**Status: a record row, not a gate.** NC2 (origin 47c50d2827) closed Framework Candidate 2 on both footings while this
lane was running: the primary CMB tolerates a large-scale bias of only 0.9967-1.0014 against 45-1866 for peaks-born
clumps; the DESI P1D forest tolerates 0.13-0.28 % of the component in clumps; clump Poisson power fails CMB lensing at
>= 1e14. NC4's label is therefore recorded as a row (abundance vs the cosmic share; cored clump vs NA2's band), and it
no longer gates the candidate.

## Known answers and MUTATE (all PASS / bite / hold)

| Check | canonical | alt |
|---|---|---|
| KA1 KD1 f-table | X-COP 4.1786, SPARC cap 0.3257, groups 1.2320-3.4640, capture 4.1110 | 3.7833, 0.1937, 0.9323-2.8646, 4.1121 |
| KA2 NA2 band (per cluster, 7 X-COP) | gas 0.159-0.238, HSE 0.211-0.303, stars 0.319-0.507 | same |
| KA2 NA2 shapes | stars F 1.7232, rms 0.1208; baryon-traced at need mean 0.000, rms 0.0818 | 1.5595, 0.1138; 0.000, 0.0835 |
| KA3 NA2 eRASS1 census | 467 clusters, 590 groups, V 1.632e8 Mpc^3, host baryons 0.01085 of rho_b | |
| KA4 UA1 / CK3 | step +0.259 (array_equal), data slope +0.21 [+0.04, +0.49] | +0.221, +0.20 [+0.05, +0.45] |
| M1 flat spectrum (per-bin abundance) | implied / observed 51-1390 in all 8 bins: BITES | 58-1620: BITES |
| M2 uniform component | f = 4.1110 (KD1 4.1110, d 0), above the SPARC cap: HOLDS / BITES | 4.1121 (d 0): HOLDS / BITES |
| M3 planted | abundance x 1/C reads A 1.000, K3 PASS; r_f 0.4 R500 gives c 0.244, in band 7/7: HOLDS | same |

## R3 / K3: abundance and cosmic share (binding)

Statistic: eRASS1 1/Vmax host baryon mass function, M_b = M_gas500 (1 + s) inside R500, hosts M500 >= 1e13 Msun,
0.02 <= z <= 0.10, PCONT <= 0.5, F500 >= F_lim, Euclidean D = cz/H0 (h 0.70), Omega 20,626 deg^2 (brackets 13,116 deg^2,
h 0.674 / 0.74, F_lim neighbours, X_HSE, power-law extension below 1e13). F_lim = 5e-13 erg/cm^2/s (N 660; see
disclosure 1). Cosmic share rho_d = 5.562 rho_b.

| | canonical | alt |
|---|---|---|
| s_f passing R7 and the groups f-table | 0.6-2.3 per dex | 0.8-2.2 per dex |
| best spectrum (largest capacity among those) | s_f 0.6: f(median group) 3.42 | s_f 0.8: f(median group) 2.77 |
| host baryons inside R500 / rho_b | 0.0133 | 0.0133 |
| capacity C (fraction of rho_d the hosts hold) | 0.0091 | 0.0078 |
| needed abundance A = 1/C (times observed) | **110** | **128** |
| most generous bracket (area 13,116, h 0.74, X_HSE, extension) | C 0.0248, **A 40.3** | C 0.0222, **A 45.0** |
| X_HSE (room between R500 and R200 from X-COP HSE masses) | 1.69 | 1.76 |
| theorem bound (every baryon in a host at f_X) | C <= f_X / R = 0.751 | 0.680 |
| gate A <= 2 | **FAIL** | **FAIL** |

- **Why it cannot pass for any spectrum.** Every host class has f <= 4.18 / 3.78 < R = 5.562. So even if every baryon in the
  universe sat inside a host, the hosts would hold at most 75 % / 68 % of the cosmic cold dark energy. With field galaxies
  empty of it and no baryon-free clumps (R3), the rest has nowhere to be.
- The observed hosts put 1.3 % of the cosmic baryons inside R500. The only ways out are dark lenses (forbidden by R3),
  cold dark energy far outside R500 (the X-COP HSE masses allow X <= 1.7-1.8 out to R200, not 40-128), or a host class
  with f > R that is not on the record.
- X-COP's whole-sky lower bound, n(>= 3.5e14) >= 3.9e-8 Mpc^-3, is consistent with eRASS1's 1/Vmax 3.9e-7.
  Lovisari's abundance is NOT EVALUABLE (no selection volume on disk); its masses enter R7 only.

## R7: the f-mass trend (PASS, fitted)

CK3's tests on UA1's joint posterior, with the spectrum's f at each Lovisari group (eps = f / 5.4).
- Canonical, s_f 0.6: predicted eps slope +0.111. A: data minus prediction 95 % [-0.069, +0.378], PASS. B: class step
  -0.068 [-0.242, +0.115], PASS.
- Alt, s_f 0.8: predicted eps slope +0.148. A: [-0.099, +0.303], PASS. B: -0.064 [-0.242, +0.115], PASS.
- s_f = 0 (flat) fails A on both footings, as in CK3.

A line through X-COP's need with 0.8-2.2 per dex satisfies UA1. That slope is fitted to the data, not predicted by the
collapse model.

## K5: the early-collapsed clump's profile (FAIL), with NC3's core rule

The collapse model is a Lagrangian top-hat at born overdensity Delta_b = (R/phi + 1)/(R + 1) - 1, integrated from z_b in
the law's field on KD1's QX15 footing background, then virialised at r_f = r_ta / 2 as a uniform sphere.

| phi (field volume 1 - phi) | Delta_b | z_ta (z_b = z_eq 3428) | r_f (kpc) | concentration (band per cluster: gas 0.16-0.24 to stars 0.32-0.51) | NA2 per-bin gate, fitted F (canonical) |
|---|---|---|---|---|---|
| 0.01-0.5 | 84-0.85 | 3275-769 | 0.4-5.6 | 1.000, in band 0/7 | rms 0.226, bins -0.12 / +0.19 / +0.23 FAIL |
| 0.9 | 0.094 | 114 | 31-40 | 1.000, 0/7 | FAIL (core rule fails too: r_f < 100 kpc) |
| 0.99 | 0.0086 | 15-16 | 221-306 | 1.000, 0/7 | rms 0.122 FAIL |
| 0.999 | 8.5e-4 | 8.6-9.9 | 377-556 | 0.23-0.53, 5/7 | rms 0.156, bins +0.16 / -0.10 / -0.07 FAIL |
| 0.9999 | 8.5e-5 | 8.1-9.3 | 401-596 | 0.19-0.44, 5/7 | rms 0.166 FAIL |

- **No phi passes on either footing, at z_b = z_eq or at the z_b 1100 bracket.** Alt reads the same (phi 0.9999: c
  0.29-0.67, 2/7 in band, rms 0.143).
- If the field holds more than about 1 % of the volume, the clump collapses at z >= 15 into r_f <= 0.3 Mpc. Its
  concentration is then 1: everything is inside 0.25 R500, against a need of 0.21-0.30. Below phi 0.95 it also fails
  NC3's core rule (r_f < 100 kpc).
- Only phi >= 0.999 lands partly in the band. There the turnaround is driven by the law's boost on the whole enclosed
  matter (nu_ta 1.7), not by the overdensity. The field is then <= 0.1 % of space, and the uniform sphere's M ~ r^3
  overfills the 0.25-0.5 R500 bins while starving the core (inner bin +0.16 to +0.18).
- At the f-table amount every collapse cell fails harder (rms 0.30-0.81).

**Cored-profile question (reported; NC3 addition).** rho proportional to (1 + (r/r_c)^2)^-1 with r_c **50, 75, 100 kpc**
meets the core rule, sits in the gas-to-stars band for 7/7 clusters, and passes NA2's per-bin rule at the fitted amount
on both footings.
- r_c 100 kpc: c 0.248-0.266 (HSE offset -0.004); canonical F 3.73, rms 0.086, bins +0.04 / +0.02 / -0.05; alt F 3.37,
  rms 0.086. It also passes at the f-table amount (rms 0.091 / 0.091).
- r_c 50 and 75 kpc pass only at the fitted F (2.9-3.3 canonical), below the f-table.
- The gamma 3 family has no r_c that passes 7/7.
- **So one profile can meet both the core requirement and the band, on both footings: a cored isothermal with r_c ~ 100
  kpc.** The collapse model does not produce it. A cold top-hat born at these overdensities gives a uniform sphere
  that is either far too compact (phi < 0.99) or the wrong shape (phi -> 1).

**CLASH (soft, no label).** The CLASH-type slope s = d log(M_cde / M_b) / d log r past 100 kpc (X-COP points, cluster
median), against CLASH's -0.08 to -0.13:
- cored r_c 100 kpc: -0.102 (canonical and alt);
- r_c 75: -0.23; r_c 50: -0.37;
- collapse cells: -1.6 (phi 0.95), -0.6 / -0.8 (phi 0.99), +0.15 to +0.52 (phi >= 0.999).

## The best spectrum and its miss

- **Spectrum:** f(M500) = f_X + s_f log10(M500 / 10^14.81), with s_f 0.6 canonical / 0.8 alt. s_f 0.8 is common to both
  footings and passes R7 on both. Clump abundance = the observed eRASS1 hosts, phi free.
- **Miss on K3:** the hosts hold C = 0.0091 / 0.0078 of the cosmic cold dark energy (A 110 / 128). In the most generous
  bracket C = 0.025 / 0.022 (A 40 / 45). Even the theorem ceiling is C <= 0.75 / 0.68.
- **Miss on K5:** the collapse model's best cell (phi 0.9999) fits X-COP at rms 0.166 / 0.143 (line 0.10), with the inner
  bin off by +0.18 / +0.14 (line 0.10). It also leaves no field.

## Compute

- Main peak RSS 233 MB (MUTATE 241 MB); R7 child 0.73 GB. Under 1 GB per process.
- One thread, nice 15, about 9 s per run.

## Disclosures

1. **The Schmidt test never passed.** <V/Vmax> was 0.403-0.465 (+- 0.009-0.011) on the whole F_lim grid, so the frozen rule
   took the largest grid value (5e-13). <V/Vmax> < 0.5 means V_max is overestimated, so the densities are likely low. NA2's
   no-Vmax census gives 0.0108 of rho_b against 0.0133 here. A factor of 2-3 would still leave A >= 13, and the theorem
   bound does not depend on the census.
2. **eRASS1 M500 is the catalogue's lensing-calibrated scaling-relation mass** (a survey-calibrated aperture). It is used
   only for the 1e13 / 1e14 cuts and for the f(M500) mapping; M_gas500 is measured inside that R500. The same convention
   as NA2.
3. **The shell model applies the law to all enclosed matter** (as frozen). At phi >= 0.99 the turnaround at z 8-16 is
   law-driven (nu_ta 1.3-1.7), not overdensity-driven. That is the only regime with c near the band. Growth before z_b is
   ignored, which is generous.
4. **M1 bites mostly through normalisation.** The flat spectrum carries the full rho_d, so every bin is high by 50-1600.
5. **Working tree behind origin.** UA1's files were read from an extraction of origin/main in a scratch folder (env
   `NC4_UA1_DIR`). The scripts default to the repo path. Nothing in UA1, NA2, KD1 or CK3 was edited.
6. **Power-law extension below 1e13 M500.** It uses the two lowest populated bins (n >= 3). It is part of the generous
   bracket only.

Adopts nothing. Kappa = 1/2 FITTED; not theory closed.
