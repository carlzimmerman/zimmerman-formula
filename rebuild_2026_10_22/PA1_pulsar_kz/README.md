# PA1_pulsar_kz: CANNOT DECIDE. No published potential-free K_z(R0, 1.1 kpc) exists that I could find, and no pulsar row separates AQUAL/QUMOND from the round rule on both footings

## A1 forward model (AMENDMENT_A1.md, fc6e39493e): still CANNOT DECIDE, both footings
Stated before any catalogue number; post-PA1, with the forecast on record. Three files fetched, approval relayed by the coordinator, sizes matched, hashes in `FETCH_LOG.md`. Untrusted, parsed only, python -I from outside `data/`. These catalogue values are data as published by its authors, not re-derived, beyond the check below. a_los at each pulsar's own position, forms A, Q, R, all in-prior cells with v_c in line for both A and R (435 canonical, 686 alt).

| binary-only, n 23 | canonical | alt |
|---|---|---|
| **N1 (primary): 2 dlnL A-R, median [range]** | -0.98 [-1.64, -0.49] | -1.24 [-2.08, -0.54] |
| Label | **NOT SEPARATED** | **NOT SEPARATED** |
| Lorentzian, median cell | +0.16 | +0.07 |
| Mock power for 9, if A or if R true | 0.000, 0.000 | 0.000, 0.000 |
| K_est A, R, N1 | 43.3 +- 35.0, 45.7 +- 36.4 | 41.8 +- 35.0, 44.6 +- 36.7 |
| N0, 2 dlnL, label | -4.12 [-4.76, -2.35], LEAN | -4.80 [-5.39, -2.60], LEAN |
| K_est A, R, N0 | 26.2 +- 25.6, 49.3 +- 17.1 | 20.6 +- 28.4, 49.1 +- 17.1 |

Secondary, all 47 with spin: NOT SEPARATED on N1 and N0, -1.42, -2.04 canonical, -1.69, -2.41 alt. K_est is negative there, A -16 +- 50 on N1, -49 +- 50 on N0: no usable vertical signal. Q tracks A within 0.05 in dL (form Q median -0.98, -1.25 on N1).

K_est vs the line: NO TENSION on every row of every form; that is lack of power, not agreement. **N0's lean toward R has mock power 0, its Lorentzian is -1.60, -1.89, and N1 removes most of it (the Solar offset and |z| term): no claim.** On N1, K_est is only 1.2 sigma from zero, with s fitted to 0, so the catalogue's own errors already cover the scatter here; the error is about 2 mm/s/yr per pulsar, not PA1's xi. K_est's error is far larger than D24's slope error because N1 frees four terms and the scale, against one alpha; different questions.

**Scaled forecast from real error (1/sqrt N, same errors, no floor):** A vs R, 1200 canonical, 940 alt binary pulsars. A floor vs line top, 9700, 8600. That fits PA1's forecast at its high end. Currently 23.

**Post-result, no label** (`fm_post.out`, one middle cell): distance +-DIST_ERR moves dL at most 0.19; Sun z 20 pc, 0.09; round rule with r, 0.01. Removing J0125-2327, J1400-1431 changes nothing: they aren't in this cut.

**A1 checks:** geometry vs textbook formula 3.6e-15 PASS. ALOS_PB recomputed, 26 rows, worst 0.058 error PASS. Sign, corr +0.25, PASS, weak. UX5 K(1.1) A 0.0000, R 0.0004 PASS. Shuffled data K_est -55 +- 59, -57 +- 60 PASS; planted A, err/20, SEPARATED on both PASS (dL +41, +45). Rerun byte-identical for `fm_read` and `fm_post`. **PA1's unmet form A MUTATE is now fixed:** AQUAL at density x 1e8, potential / 1e8, reaches Newton to 7e-9, 9e-9 (56.273, 52.698; form A 82.35, 82.03). Those solves stopped at the 80 iteration cap, residual 1e-6. Form A is now on every eligible cell, so the 28-cell limit is lifted for A1. A bug in `label` for a passing row was fixed before output; real rows never reached it, and plant runs needed it.

**Limits of A1:** no disequilibrium beyond N1; axisymmetric; distance held at DIST except the sensitivity; catalogue trusted beyond the recompute. Only binary-only is primary, by the amendment. `cache/` isn't committed, 12 MB, rebuilt by `fm_field.py` in minutes.


Criteria: `FROZEN_CRITERIA.md` (3eb905dc96), committed alone first. **Not blind.** All literature values are **PROVISIONAL**: read from web pages through a summariser, no file downloaded, no table checked by me. kappa = 1/2 FITTED. Footings never pooled. The cold sector stays retired; this reinstates nothing. Nothing here says the data favour the framework. Not theory closed. No line moved.

**Answer.** Current values can't decide. The binary pulsar rows give slopes, not K at 1.1 kpc. On the frozen label, 5 of 7 rows have NO POWER on alt and all 7 on canonical. The 2 alt SEPARATES fire only at the lowest allowed height, and the form-choice spread (0.36 dex) is over twice the form gap (0.09-0.17 dex). A real reanalysis at the pulsars' actual positions is possible and small; files are at the end, awaiting approval.

## 1. What the forms predict
UX5's solver at R0, every in-prior cell (1375, Q and R) with form A on 28 cells; Q/A differs at most 0.41 %. Conversion: K of 1 Msun/pc^2 = 0.02764 mm/s/yr.

| | canonical | alt |
|---|---|---|
| Form A, least K(1.1), v_c in line | 75.9 = 2.10 mm/s/yr | 76.2 = 2.11 |
| A - R, same baryons, v_c in line, min / BV2 median | 14.6 / 16.4 = 0.40 / 0.45 mm/s/yr | 16.4 / 18.9 = 0.45 / 0.52 |
| A - R, all in-prior, min | 13.9 | 16.0 |
| Kinematic line 66.4 +- 2.2, top 70.8 | 1.84, 1.96 | same |
| Median log alpha gap (chord a_z/z), z 0.1 / 0.3 / 1.1 kpc | 0.151 / 0.140 / 0.103 dex | 0.169 / 0.156 / 0.114 |

Chord log alpha falls fast with height: form A median 3.85 at 0.1 kpc, 3.34 at 1.1 (canonical). Tables: `pa1_read.out`.

## 2. Rows and labels
alpha in Gyr^-2, a_z = -alpha z. Errors are as published, no added systematic. Per-pulsar heights weren't readable from pages, so each row is tested over a height range, not at its own heights (below).

| Row | log alpha | Best min gap / sigma, canonical | alt | Label canonical / alt |
|---|---|---|---|---|
| C21 alpha1, 14 PSR | 3.61 +0.13 -0.10 | 1.17 | 1.36 | NO POWER / NO POWER |
| C21 alpha1, beta (their preferred) | 3.69 +0.19 -0.12 | 0.62 | 0.72 | NO POWER / NO POWER |
| D24 alpha, 24 PSR | 3.60 +- 0.06 | 2.83 | 3.27 | NO POWER / **SEPARATES** |
| D24 alpha-beta | 3.51 +- 0.13 | 1.48 | 1.71 | NO POWER / NO POWER |
| D24 anharmonic alpha1 | 3.51 +- 0.08 | 2.82 | 3.26 | NO POWER / **SEPARATES** |
| D24 2alpha-beta alpha1 | 3.56 +- 0.11 | 1.76 | 2.04 | NO POWER / NO POWER |
| D24 local expansion da_z/dz | 3.73 +- 0.08 | 1.70 | 1.96 | NO POWER / NO POWER |

**Overall: CANNOT DECIDE** (C3 needs both footings). No row EXCLUDES a form; closest is form A against D24 anharmonic, 2.24 and 2.60 sigma, and D24's local expansion row points the other way.

**The alt SEPARATES is weak, and I don't read it as a separation.** It means "error small enough", not "one form preferred".
- It fires only at the lowest height: D24 alpha at 0.10 kpc (3.27), falling to 2.58 at 0.2, 2.06 at 0.3, 1.43 at 0.5. Anharmonic at 0.05 (3.25), then 2.94 at 0.1.
- **Height range was not in the freeze.** I chose chord 0.1-1.1 kpc and midplane 0.05-0.2 after the freeze, taking the best height, which is generous to SEPARATES. C2 asked for each row's own heights; this is the closest available, so strictly those rows are NOT COMPARABLE until the reanalysis.
- Height and form are degenerate: log alpha 3.60 is matched by median form Q at 0.41 kpc and form R at 0.21 (alt 0.45, 0.21). So without the actual heights either form fits every chord row.
- Errors are statistical within one fit form. D24's forms alone run 3.37 to 3.73.

**Listed, can't decide:**

| Value | Why it can't decide |
|---|---|
| D25, 53 PSR, rho_0 0.108 +- 0.008 stat +- 0.011 sys; alpha-model mean 0.038 +- 0.013 | Poisson and disc + NFW families: NOT POTENTIAL-FREE. In AQUAL the Poisson density isn't baryons |
| D24 rho_0 0.062 +- 0.017; C21 0.08 +0.05 -0.02; Moran+ disc 0.040 +- 0.020 | Poisson: NOT POTENTIAL-FREE |
| Donlon, Widrow, Chakrabarti (2511.15865) mean density | Gauss's law, Newtonian. No K_z values given |
| D25 a_los,z(1.5 kpc) -1.5 mm/s/yr | A normalisation for a disc-wave term, a line-of-sight quantity: NOT COMPARABLE |
| Phillips+ 1.7 +- 0.5 e-10 m/s^2; Bovy v_c 244 +- 8 | In-plane, not K_z: NOT COMPARABLE |
| Yasin and Desmond (2605.06659), vector RAR, 26 binaries | Reduced chi^2 3.58 vs Newton's 10.86, but a constant Solar acceleration gives 3.75: their own reading is that the Sun dominates. Not a vertical test, and not this lane's form |
| Eclipse timing (Chakrabarti+ 2022) | Method demonstration only; I found no measurement |
| Spectroscopic drift | I found no published vertical result; one search only |

**Reconstruction, NOT POTENTIAL-FREE, no label.** K(R0, 1.1) from D25's fit parameters, independent errors, no covariance available, so these errors are rough: exponential 64.1 +- 6.3, isothermal 63.3 +- 9.1, Miyamoto-Nagai 79.9 +- 66 (the error is dominated by uncorrelated M and a, so it means little). Those families span the kinematic line and form A's floor. Against the line: NO TENSION, for what a family-dependent number is worth. Chord rows can't be set against the line, which sits at 1.1 kpc alone.

## 3. Systematics
- **Shklovskii and distance:** P_b mu^2 d / c. Parallax and Pbdot dominate a_los errors (D24). Distance enters both position and Shklovskii, a correlation D24 says standard propagation misses. One parallax was corrected from 1.9 to 0.26 mas between papers.
- **Spin-based accelerations:** need an empirical magnetic-braking model, so not fully direct. Use binary-only as the primary sample.
- **Scatter:** D25 fits an extra Lorentzian noise xi about 1.6 mm/s/yr per pulsar. That's 4 times the A - R gap.
- **Disequilibrium, the likely floor:** observed north-south difference about 0.4-0.5 mm/s/yr at 1 kpc, the same size as the gap; about 30 % of the force in the expanded sample. Averaging both sides removes only the odd part. Mock work (2606.31042) has direct-acceleration K_z with 18 % median bias and 19 % scatter in underdense regions of an interacting simulation, against a form difference of about 20 %. Different context, but a warning.
- **Solar term:** all values are relative to the Sun; D24 finds a residual removed by a 1.1 mm/s/yr Solar acceleration. Any forward model has to carry the law's own in-plane field.

## 4. Forecast (judgment on N)
3 sigma on K(R0, 1.1), no systematic floor. N from xi with mean projection 0.5, my assumption, as Gaussian and Lorentzian; current N is 26 binary, about 50 total.

| Target | canonical: sigma K, mm/s/yr, N | alt |
|---|---|---|
| A vs R, minimum gap | 4.85, 0.134, 570-1140 | 5.46, 0.151, 450-900 |
| A vs R, median gap | 5.46, 0.151, 450-900 | 6.29, 0.174, 340-680 |
| A floor vs line top 70.8 | 1.71, 0.047, 4600-9200 | 1.81, 0.050, 4100-8200 |

On slopes: sigma(log alpha) 0.03-0.05 dex at known heights, near D24's best 0.06 but only within one fit form. Separating the forms from each other is much easier than settling form A against the kinematic line. UX5's "about +-3" corresponds to a smaller separation than 3 sigma here. Longer baselines help (error improves with time), xi may be mostly model error, so these N could be pessimistic; the disequilibrium floor could make them optimistic.

## 5. Files for a real reanalysis: for owner approval, none downloaded
| File | Source URL | Bytes | Use |
|---|---|---|---|
| v3/binary_only.csv | https://raw.githubusercontent.com/thomasdonlon/Empirical_Model_MSP_Spindown_Accels/main/v3/binary_only.csv | 4482 | primary: ALOS_PB, positions, DIST, PBDOT terms |
| v3/data.csv | https://raw.githubusercontent.com/thomasdonlon/Empirical_Model_MSP_Spindown_Accels/main/v3/data.csv | 14347 | secondary: spin-based, 53 PSR |
| README.md (same repo) | https://raw.githubusercontent.com/thomasdonlon/Empirical_Model_MSP_Spindown_Accels/main/README.md | 3828 | columns |
| 2401.15808 source, gzip | https://arxiv.org/e-print/2401.15808 | 836655 | D24 Table 1 |
| 2501.03409 source, gzip | https://arxiv.org/e-print/2501.03409 | 303154 | D25 likelihood, xi |
| 2306.13137 source, gzip | https://arxiv.org/e-print/2306.13137 | 1448999 | independent 29-PSR table |
| psrcat_pkg.tar.gz | https://www.atnf.csiro.au/research/pulsar/psrcat/downloads/psrcat_pkg.tar.gz | 1249005 | optional: updated parallax |

Repo commit to pin: 6cb4e31f6b2e732f5973b024634507c2e4f59988. Sizes are from the GitHub tree or HEAD requests; I checked content-length, not contents.

**The reanalysis:** forward-model a_los at each pulsar's position from forms A, Q, R, with the law's in-plane field and Sun included, and compare with no Newtonian family, both footings, binary-only first. It needs only the first three files, 22657 bytes. I expect it to narrow the height problem but not to decide, given xi.

## Checks
- Recovering UX5's K(1.1) from the solver: |d| 0.000 for A, Q, R on the sampled cells, 0.0 on all 1375. PASS.
- Byte-identical rerun of every JSON and read output: PASS, compared by cmp.
- Injected row, error / 20: all rows SEPARATES, overall flips. PASS.
- **MUTATE as frozen: NOT MET for form A in PA1; fixed in A1, above.** The freeze said nu = 1 must change form A - form R. I could only set nu = 1 in form Q, since AQUAL's nu lives in P4's solver and I don't edit other lanes. Q falls to Newton (83.62 to 56.71, Newton 56.71). Form A wasn't mutated.
- **Form A on 28 cells only, Q stands in on the rest for labels.** Q/A at most 0.41 %.
- **Slip, fixed:** `ux5_core` exports its own HERE, so my first profile run wrote 3 JSONs into UX5's directory. I moved them here before anything was committed and fixed the script; UX5's tracked files are unchanged.
- **WebFetch saved 4 PDFs automatically** (2401.15808, 2511.15865, 2008.13052, 2606.31042) to the session's tool-results folder, outside the repo, when I tried PDF URLs. Not intended under the no-download rule. I didn't read them and used arXiv HTML instead.

## Limits
Summariser reads of long pages, parts unread (2401.15808 beyond 100000 characters, others' tails). No number here was checked against a PDF table. Search was not exhaustive; a K_z value in a paper I didn't reach is possible. Moran+'s page gave only the abstract. Isolated solves, no external field or disequilibrium. Only two field equations and a rule with no field equation are tested. C21 = Chakrabarti+ 2021, arXiv:2010.04018. D24 = Donlon+ 2024, arXiv:2401.15808. D25 = Donlon+ 2025, arXiv:2501.03409. Moran+ = arXiv:2306.13137. Phillips+ = arXiv:2008.13052. Bovy = arXiv:2012.02169.

## Expectation against result
Cannot decide, 80 %: held. Wrong: slope errors are closer to useful than UX5's "about 5 times" suggested. What blocks it is height, fit form and disequilibrium more than the statistical error.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
