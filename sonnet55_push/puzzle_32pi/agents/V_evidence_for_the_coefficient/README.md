# Lane V -- what the data actually establish about the coefficient Z in a0 = c H / Z  (evidence lane, not a derivation)

## Bottom line
1. **The data support "a0 = cH0 / (6.0 +0.8/-0.7)" (68%, rho_total footing, H0 = 67.4), not "a0 = cH/5.789".** On the rho_Lambda footing the same data give a0 = cH_Lambda / (4.9 +/- 0.6).
   Basis: a0 = 1.10e-10 +/- 12% (the scatter of nine full-sample analyses that differ in interpolating function, mass-to-light treatment and method; statistical errors are 1-8%).
   Z = 5.789, 6 and 2 pi are all inside the 68% interval on the rho_total footing; F (5.789) is 0.25 sigma below the data, V (6) 0.05 above, M (2 pi) 0.42 above.
2. **The declared candidates are not separated.** Bayes factors F:V = 0.97 and F:M = 1.06 (rho_total, Planck H0); pairwise separations F-V 0.29 sigma, F-M 0.67 sigma, V-M 0.38 sigma. Only the "forced kernel" Z = sqrt(8 pi/3) = 2.894 (kappa = 1) is excluded (5.7 sigma) and the 2 pi-in-kappa reading Z = 18.2 (9 sigma).
   To separate 5.789 from 6 at 2 sigma needs a total error of 1.8% (1.6% on a0 with Planck H0), and from 2 pi 4.1% (4.0% on a0). The best published total error is 8.3%, the honest analysis-choice scatter 12%, and the H0 tension alone (4% half-difference) already exceeds the 5.789-vs-6 gap.
3. **Omega_Lambda = 32 pi a0^2/(3 H0^2 c^2):** the audit's 0.906 reproduces (a0 = 1.0766e-10, H0 = 67.4). The "2.4 sigma" is 1.7-2.6 sigma depending on parametrisation/estimator; removing it needs a0 to fall by 13.0% (7.6% for 1 sigma), which is inside the measured systematic budget (rescaling all SPARC distances by 73/67.4 alone gives -13.8%), and the sign of the tension flips with the interpolating function (RAR kernel: Omega_pred = 0.595). Nothing was adjusted.
4. **Finding relevant to the record (not to the derivation):** the record's SPARC profile-likelihood a0 = 1.0766e-10 is conditional on its alpha = 1 kernel. Same data, Upsilon free per galaxy: alpha1 1.083, RAR 0.873, simple 0.881, standard 1.117 (e-10). The data prefer RAR-like shapes over the record's kernel (d chi2 = 168 on independent points, about 9 after the crude clustering deflation), and under RAR the ordering of Z_F versus Milgrom's 2 pi on the rho_Lambda footing flips.
5. **Verdict: NOTHING NEW on the derivation.** kappa = 1/2 stays FITTED. Deliverable = the quantified evidence table below.

## What I did (all scripts committed here, all exit 0; run order v00, v02, v01, v03, v04, v05; `v_common.py` is shared)
| script | content | checks |
|---|---|---|
| `v00_declared_hypotheses.py` | candidate Z list **declared before any data or likelihood** (sha256 6ea13c2f...; later scripts print it) | -- |
| `v01_determinations_table.py` | the a0 determinations I could open (arXiv IDs), unit/error recomputation, Z on both footings, the pre-declared ensemble E | 10/10 |
| `v02_sparc_refit_systematics.py` | the record's profile likelihood re-implemented and reproduced; bootstrap; IF x Upsilon matrix; validation against papers; perturbations (distance, gas, inclination, H0-coupling); the record's headline comparison under other IFs; mocks | 31/31 |
| `v03_posterior_Z.py` | posterior of Z, both footings, three H0 treatments; Bayes factors; sigma matrix; injection-recovery | 15/15 |
| `v04_omega_lambda_prediction.py` | Omega_Lambda prediction per determination and H0; tension; required shift vs budget | 12/12 |
| `v05_required_precision.py` | required precision, H floor, present budget, wide-binary sensitivity, a0(z) context, figure | 7/7 |
Outputs: `*.out` beside each script, `v0*_results.json`, `v_Z_posteriors.png`. Total 75 checks, 0 failures. Runtime about 2 minutes (v02 dominates).
Declared candidates (v00): F sqrt(32 pi/3) = 5.7888 (kappa 1/2), V 6 (Verlinde), M 2 pi (Milgrom), K1 sqrt(8 pi/3) = 2.894 (kappa = 1), N 3 sqrt 3 = 5.196 (Nariai shell), P 1/2 + pi sqrt 2 = 4.943 (van Putten), Q 18.19 (kappa = 1/2 pi in the framework's convention); controls Z = 0.5 (a0 = 2cH family), Z = 12.

## 1. The determinations (numbers read from the papers' text; a0 in 1e-10 m/s^2; Z_tot = cH0/a0, Z_Lam = cH0 sqrt(0.685)/a0 at H0 = 67.4)
Opened in full (PDF converted locally): 1609.05917, 1610.08981, 1803.00022, 2009.11525, 2106.11677, 1806.06803, 1812.05002, 2301.04368, 2303.11314, 1107.2934, astro-ph/0204521, 1112.3960 (a0 statements only), 2406.09685 and 1901.05966 (no a0 quoted). Abstract page or HTML summary only: 2001.08340, 2604.22613. Not opened: Milgrom 2001.09729 (another lane read it), the original Begeman et al. 1991, the 2025 paper behind a z = 0.05 row of the record's `a0_of_z.csv`.
| source (arXiv) | data / interpolating function (IF) / M/L treatment | a0 | stat | sys | Z_tot | Z_Lam |
|---|---|---|---|---|---|---|
| Begeman-Broeils-Sanders 1991 via Sanders & McGaugh 2002 (astro-ph/0204521) | 9 spirals, HI curves, H0 = 75 distances, standard IF, M/L free | 1.2 | 0.27 (scatter of 9) | distance scale | 5.46 | 4.52 |
| McGaugh 2012 (1107.2934) | BTFR of gas-rich galaxies; a0 = chi/(G A), A = 47 +/- 6, chi = 0.80 | 1.3 | 0.3 (incl. 20% on chi) | chi = 1 would give 1.60 (recomputed) | 5.04 | 4.17 |
| McGaugh-Lelli-Schombert 2016 (1609.05917) | SPARC RAR, 153 galaxies, RAR IF, Upsilon fixed 0.5/0.7, ODR | 1.20 | 0.02 | 0.24 (20% on Upsilon) | 5.46 | 4.52 |
| Lelli et al. 2017 (1610.08981) | same fit; variant with an acceleration floor, dSphs included | 1.20; 1.1 +/- 0.1 | 0.02 | 0.24 | 5.46 | 4.52 |
| Li et al. 2018 (1803.00022) | **not a determination**: fixes 1.20 +/- 0.02; with a flat prior per galaxy g_dagger is broad with no chi2 gain (M/L degeneracy) | -- | | | | |
| Rodrigues et al. 2018 (1806.06803, Table 1) | 100 SPARC galaxies, per-galaxy Bayesian, Upsilon within x2, D +/- 20%; standard / simple / RAR | 1.253 / 1.208 / 1.099 | none printed | | 5.23 / 5.42 / 5.96 | 4.33 / 4.49 / 4.93 |
| Chang & Zhou 2019 (1812.05002, Table 1) | same sample, Gaussian priors; standard / simple / RAR | 1.189 / 1.146 / 1.099 | none printed | | 5.51 / 5.72 / 5.96 | 4.56 / 4.73 / 4.93 |
| Desmond-Bartlett-Ferreira 2023 (2301.04368, Table 1) | SPARC, prior-max galaxy parameters; simple / RAR / standard / simple+EFE | 1.11 / 1.13 / 1.54 / 1.16 | none printed | standard is a far worse fit | 5.90 / 5.80 / 4.25 / 5.65 | 4.88 / 4.80 / 3.52 / 4.67 |
| Desmond 2023 (2303.11314) | SPARC, HMC, all galaxy parameters free (priors), RAR; models span 1.07-1.31 | 1.19 | 0.04 | 0.09 | 5.50 | 4.55 |
| Chae et al. 2020 (2009.11525) | **not a determination**: fixes 1.2 throughout | -- | | | | |
| Brouwer et al. 2021 (2106.11677) | KiDS weak-lensing RAR, isolated galaxies: low-acceleration tail has a similar constant, ~1.2 | ~1.2 (no fit, no error) | | | | |
| Tian et al. 2020 (2001.08340, abstract) | 20 CLASH clusters: g_ddagger = 2.02 +/- 0.11 e-9 (**16.8x** the galaxy value) | 20.2 | 1.1 | | 0.32 | 0.27 |
| Mistele et al. 2024 (2406.09685); Lelli et al. 2019 (1901.05966) | lensing BTFR / BTFR velocity definitions: no a0 quoted | -- | | | | |
| record (`mi_a0_profile_likelihood_milgrom_footing_2026.py`) | SPARC 175, alpha1 kernel, Upsilon free per galaxy | 1.0766 | 0.059 (5.44% clustered-crude; 1.24% independent) | | 6.08 | 5.03 |
| this work (`v02`), Upsilon free, all 175 | alpha1 / RAR / simple / standard | 1.083 / 0.873 / 0.881 / 1.117 | 8.2% (galaxy bootstrap) | | 6.05 / 7.51 / 7.43 / 5.86 | 5.00 / 6.21 / 6.15 / 4.85 |
Reading: every galaxy-scale z ~ 0 determination gives Z_tot = 5.0-7.5 (median 5.9); **the cluster value is a different scale (17x)**, so a universal a0 is a galaxy-scale statement. Wide binaries are not an a0 determination and are not in the table.
Systematics stated in the papers: Upsilon (20%, MLS16), model choices (7.6%, Desmond 2023), chi geometry (25% swing, McGaugh 2012), distance scale (Sanders & McGaugh: a0 tracks the assumed distance scale), IF (below).
**Ensemble E** (declared in `v01` before its statistics were computed): MLS16 1.20, Desmond 1.19, Rodrigues-RAR 1.099, Chang-Zhou-RAR 1.099, DBF23-RAR 1.13, McGaugh12 1.3, this work RAR Upsilon-free 0.873, RAR Upsilon in [0.25,1] 0.944, RAR fixed 0.5 1.106. Log-mean 1.097, sd 12.2% (median 1.106, range 0.873-1.300; dropping any member moves the centre by < 5.1%). These are analysis choices, not independent measurements: the sd is the analysis-choice systematic.

## 2. What moves a0 (measured with the record's own profile-likelihood machinery, `v02`)
Reproduction first: sigma_int = 0.0808 dex, chi2 = 3204.0, 3380 points at the canonical a0; the record's grid gives a0 = 1.0766e-10, 1.24%, 5.44% (all reproduced). **Own finding:** on a fine local grid the points-independent sigma is 1.59% (the record's 1.24% is a coarse-grid interpolation underestimate) and a0_hat = 1.0806e-10; a galaxy bootstrap gives 8.2% (jackknife 8.4%) against the crude 4.39x rule's 7.0%.
Validation against papers (fixed Upsilon 0.5/0.7, the 153 galaxies of MLS16): RAR 1.113, simple 1.086, standard 1.557 versus the published 1.20 (ODR), and 1.13 / 1.11 / 1.54 in 2301.04368.

**a0_hat (1e-10) by IF and Upsilon treatment (all 175 galaxies, sig_int fixed 0.0808 dex):**
| Upsilon treatment | alpha1 (record) | RAR | simple | standard |
|---|---|---|---|---|
| free, 0.05-3 (record) | 1.083 (chi2 3140) | 0.873 (2972) | 0.881 (3015) | 1.117 (3244) |
| in [0.25, 1.0] | 1.179 | 0.944 | 0.941 | 1.246 |
| in [0.3, 0.8] | 1.252 | 1.002 | 0.997 | 1.330 |
| fixed 0.5 (bulge 0.7) | 1.411 | 1.106 | 1.079 | 1.548 |
- The IF is a 20-30% systematic **within a single dataset**; the two shapes the data prefer (RAR, simple) agree with each other to 1.0% (Upsilon free) to 2.5% (fixed).
- The record's own likelihood prefers RAR to its alpha1 kernel by d chi2 = 168 (independent points; about 9, roughly 3 sigma, after the crude clustering deflation). Mocks (16 per truth): a wrong kernel biases a0 by +20% (alpha1 fitted to RAR truth) or -23% (RAR fitted to alpha1 truth); the estimator is unbiased with the right kernel (+0.04% +/- 0.5%); the real alpha1/RAR ratio (1.24) is what RAR-truth mocks predict (1.22).
- **Class heterogeneity:** with Upsilon free, gas-dominated (T >= 8, n = 81) and star-dominated (T <= 5, n = 62) galaxies want a0 = 0.57-0.74 versus 1.32-1.66 (ratio 2.25-2.41 for **every** IF, so it is not a kernel artefact). In the cleanest published-style fit (RAR, fixed Upsilon, MLS16 cuts, 0.11 dex) 0.856 versus 1.248 (ratio 1.46, half-range 19%). No statistical error covers this; I did not investigate its cause.
- **Perturbations (record kernel, d ln a0):** all distances x1.05: -8.4% (x0.95: +8.8%); Hubble-flow (f_D = 1, 97 of 175 galaxies, adopted at H0 = 73) distances x73/67.4: -7.2%; all distances x73/67.4: -13.8% (-13.3 to -14.6% for the four IFs); gas mass x1.10: -6.3% (x0.90: +6.6%, x1.20: -12.2%); coherent inclination shift +1 / -1 per-galaxy sigma_i: -3.4% / +13.9%. The transform is unit-tested (g_bar invariant, g_obs scales as 1/s, deviation 6e-16, and a mutated transform fails the test).
- a0 depends on the distance scale, so **a0_obs and H0 are coupled**: a smaller H0 lengthens the Hubble-flow distances and lowers the measured a0 while lowering the prediction cH/Z.
- Quadrature budget: distance +/-5% (8.6%), gas +/-10% (6.5%), inclination (8.7%) = 13.8%; adding IF (12.4%), Upsilon treatment (11.9%), class heterogeneity (18.8%) = 29%. For comparison MLS16 quote 20% total and Desmond 2023 9% (stat + sys).

## 3. Posterior on Z (flat prior in ln Z; log-normal a0 likelihood; H0 and Omega_Lambda independent as briefed; 68% / 95% intervals; kappa = sqrt(8 pi/3)/Z)
| a0 scenario (1e-10, error) | footing / H0 | Z median | 68% | 95% | kappa 68% |
|---|---|---|---|---|---|
| **Ensemble E** (1.097, 12.2%) | tot / Planck 67.4 | 5.97 | 5.28-6.74 | 4.70-7.59 | 0.430-0.548 |
| | tot / SH0ES 73.0 | 6.46 | 5.72-7.30 | 5.08-8.23 | 0.396-0.506 |
| | tot / average 70.2 +/- 2.8 | 6.21 | 5.46-7.05 | 4.83-7.98 | 0.410-0.530 |
| | Lam / Planck | 4.94 | 4.37-5.58 | 3.88-6.28 | 0.519-0.662 |
| | Lam / SH0ES | 5.35 | 4.73-6.04 | 4.20-6.81 | 0.479-0.612 |
| | Lam / average | 5.14 | 4.52-5.84 | 3.99-6.61 | 0.496-0.640 |
| record as quoted (1.0766, 5.44%) | tot / Planck | 6.08 | 5.76-6.42 | 5.46-6.77 | 0.451-0.502 |
| | Lam / Planck | 5.03 | 4.76-5.32 | 4.52-5.61 | 0.544-0.607 |
| record + measured systematics (1.081, 16.1%) | tot / Planck | 6.06 | 5.16-7.11 | 4.42-8.30 | 0.407-0.561 |
| | Lam / Planck | 5.01 | 4.27-5.89 | 3.66-6.88 | 0.492-0.677 |
| MLS16 (1.20, 20.1%) | tot / Planck | 5.46 | 4.47-6.66 | 3.68-8.09 | 0.434-0.648 |
| | Lam / Planck | 4.52 | 3.70-5.52 | 3.05-6.69 | 0.525-0.782 |
| Desmond 2023 (1.19, 8.3%) | tot / Planck | 5.50 | 5.07-5.98 | 4.67-6.47 | 0.484-0.571 |
| | Lam / Planck | 4.55 | 4.19-4.95 | 3.87-5.36 | 0.585-0.690 |
The 'physical Lambda' footing variant (rho_Lambda held at its Planck value whatever H0 is) equals the Lam/Planck rows. Prior and likelihood-shape choices move the median by 1.6% (flat in ln Z vs in Z; log-normal vs Gaussian in a0). The H0 tension is an 8% shift in Z (73/67.4).
**Two footings differ by sqrt(Omega_Lambda) = 0.828 (17% in Z), more than every coefficient gap among F, V, M; which footing is right is not something these data can say.**
Sigma offsets of the candidates from the data, (ln Z_i - ln Z_hat)/s_tot (+ = candidate above the data), ensemble E: tot/Planck F -0.25, V +0.05, M +0.42, N -1.13, P -1.54, K1 -5.9; Lam/Planck F +1.30, V +1.59, M +1.97, N +0.42, P +0.01, K1 -4.4; Lam/SH0ES F +0.64, V +0.93, M +1.31.

**Bayes factors and posterior probabilities over the declared candidates (equal prior weights; a0 likelihood marginalised over H0 and Omega_Lambda):**
| scenario | footing / H0 | P(F) | P(V) | P(M) | P(N) | P(P) | BF F:V | BF F:M | best |
|---|---|---|---|---|---|---|---|---|---|
| E | tot / Planck | 0.26 | 0.27 | 0.25 | 0.14 | 0.08 | 0.97 | 1.06 | V |
| E | Lam / Planck | 0.16 | 0.10 | 0.05 | 0.33 | 0.36 | 1.5 | 3.0 | P |
| record as quoted | tot / Planck | 0.27 | 0.39 | 0.34 | 0.01 | 0.00 | 0.69 | 0.79 | V |
| record as quoted | tot / average H0 | 0.19 | 0.34 | 0.46 | 0.01 | 0.00 | 0.57 | 0.42 | M |
| record as quoted | Lam / Planck | 0.02 | 0.00 | 0.00 | 0.46 | 0.51 | 6.4 | 131 | P |
| record + systematics | tot / Planck | 0.24 | 0.25 | 0.24 | 0.16 | 0.11 | 0.96 | 0.99 | V |
| MLS16 | tot / Planck | 0.21 | 0.20 | 0.17 | 0.22 | 0.20 | 1.07 | 1.23 | N |
Reading: on the rho_total footing nothing is separated. On the rho_Lambda footing at the record's own 5.44%, F beats V and M (BF 6 and 131) but the Nariai-shell 3 sqrt 3 and van Putten's 4.94 beat F by a factor ~20; with the honest error the three are indistinguishable. Neither result favours F specifically. Controls Z = 0.5 and Z = 12 are rejected everywhere (largest likelihood ratio to the best candidate 1.3e-3, reached at a 20% a0 error).
Pairwise separations, ensemble E (s_tot = 12.2%): F-V 0.29, F-M 0.67, F-N 0.88, F-P 1.29, V-M 0.38, V-N 1.18, M-N 1.55, N-P 0.41, K1 from any of them 4.4-6.3 sigma, Q from any of them 8.7-10.6 sigma. At the record's own 5.5%: F-V 0.65, F-M 1.49, F-N 1.97, F-P 2.88, V-M 0.84, K1 9.8-14 sigma. Full matrix in `v03_posterior_Z.out`.
Injection-recovery (truth F, 20000 datasets per row; intervals cover 68.3% / 95% as they should): the fraction of datasets with BF > 3 for the true F over V / over M is 0% / 10% at a 12% a0 error, 9% / 51% at 5.4%, 57% / 95% at 2%, 85% / 99.9% at 1% (H floor 0.74%); the median ln BF equals the analytic Delta^2/(2 s^2).

## 4. Omega_Lambda = 32 pi a0^2/(3 H0^2 c^2) from each a0 (0.685 +/- 0.007 measured)
- Algebra (checked): Omega_pred = Z_F^2 (a0/cH0)^2; a0 = cH0 sqrt(0.685)/Z_F = 9.362e-11 returns exactly 0.685; Omega ~ a0^2 H0^-2.
- **Record a0 = 1.0766e-10, H0 = 67.4: Omega_pred = 0.9058 (audit 0.906).** The same offset expressed four ways: 2.40 sigma (a0 linear, sigma = 5.44% of the fit, the record's number), 2.23 (Omega linear, sigma = 2 x 5.44%), 2.57 (ln a0), 1.82 (profile d chi2 = 63.9 deflated by 19.3, the record's P3 number), and 1.75 with my bootstrap sigma (8.2%). **Why they differ:** Omega ~ a0^2 doubles the fractional error and makes the map non-linear; the record divides by 5.44% of the fitted value rather than of the prediction; the profile is asymmetric. Honest range 1.7-2.6 sigma, none using a systematic budget.
| a0 (1e-10, error) | Omega_pred, H0 = 67.4 | H0 = 70.2 | H0 = 73.0 |
|---|---|---|---|
| record 1.0766 (5.4%) | 0.906 +/- 0.099 (+2.2 s) | 0.835 (+1.3 s) | 0.772 (+1.0 s) |
| record kernel, bootstrap 1.083 (8.2%) | 0.917 +/- 0.151 (+1.5 s) | 0.845 | 0.782 (+0.7 s) |
| MLS16 1.20 (20%) | 1.125 +/- 0.452 (+1.0 s) | 1.037 | 0.959 |
| Desmond 2023 1.19 (8.3%) | 1.107 +/- 0.184 (+2.3 s) | 1.020 (+1.8 s) | 0.943 (+1.6 s) |
| McGaugh 2012 1.3 (23%) | 1.321 +/- 0.610 (+1.0 s) | 1.217 | 1.126 |
| ensemble E 1.097 (12.2%) | 0.941 +/- 0.230 (+1.1 s) | 0.868 | 0.802 (+0.6 s) |
| this work RAR / simple, Upsilon free | 0.595 / 0.607 | 0.548 / 0.560 | 0.507 / 0.517 |
| this work RAR, Upsilon in [0.25,1] / fixed 0.5 | 0.696 / 0.957 | | |
| Rodrigues / Chang-Zhou RAR (1.099) | 0.944 | 0.870 | 0.805 |
The published 1.19 +/- 0.098 also sits above the canonical 9.36e-11 (+2.6 sigma in a0), so the offset is not peculiar to the record's kernel; but the prediction spans 0.60-1.32 across the RAR-family analyses (standard IF at fixed Upsilon: 1.85), and the measured 0.685 lies inside that range. The 'prediction' carries twice the fractional error of a0 (about +/-0.23 for the ensemble).
- **Shift needed:** a0_obs must fall 13.0% (a0 = 0.9362e-10) to hit 0.685, 7.6% to be within 1 sigma, 2.2% within 2 sigma. Measured items (v02): Hubble-flow distances at H0 = 67.4: -7.2% (52% of what is needed); all distances rescaled by 73/67.4: -13.8% (99%); distances x1.05: -8.4% (60%); gas +10%: -6.3% (45%), +20%: -12.2% (87%); inclination +1 sigma: -3.4% (25%); alpha1 -> RAR IF: -21.6% (155%, overshoots to Omega_pred = 0.595). The needed 13.0% is 1.0x the distance + gas + inclination budget (13.8%), 0.48x the full measured budget (29%), 0.65x MLS16's 20%. **It is inside the systematic budget.**
- H0-coupled worlds (record kernel, Upsilon free; sensitivity statements, not corrections): Planck H0 with Hubble-flow distances rescaled 0.793, with all distances rescaled 0.696, SH0ES H0 with SPARC as published 0.782 (RAR kernel: 0.509 / 0.445 / 0.507).

## 5. What would discriminate (requirements only; I make no forecast for Gaia DR4, JWST or any future survey)
| pair | gap in Z | total error for 2 sigma | 3 sigma | expected BF = 3 | expected BF = 10 |
|---|---|---|---|---|---|
| F-V (5.789 vs 6) | 3.6% | 1.8% | 1.2% | 2.4% | 1.7% |
| F-M (5.789 vs 2 pi) | 8.5% | 4.1% | 2.7% | 5.5% | 3.8% |
| V-M | 4.7% | 2.3% | 1.5% | 3.1% | 2.2% |
| F-N (Nariai shell) | 11.4% | 5.4% | 3.6% | 7.3% | 5.0% |
| F-P (van Putten) | 17.1% | 7.9% | 5.3% | 10.7% | 7.4% |
- **H floor:** required precision on a0 alone for F-V at 2 sigma: 1.63% (Planck H0), 1.15% (SH0ES), 1.55% (Planck + Omega_Lambda footing), **impossible** with the H0 tension unresolved (floor 4.0%). F-M: 4.0% / 3.9% / 4.0% / 0.94%.
- **Present vs required:** best published total 8.3% (x5 improvement needed for F-V, x2 for F-M), ensemble scatter 12% (x7, x3); every systematic component in section 2 except the data-preferred-IF pair (1.0% full spread) exceeds the 1.8% needed for F-V. Improved H0 (below 1%) is necessary, not sufficient.
- **Interpolating function:** the data already choose RAR-like over the record's kernel (section 2); within the RAR/simple class the residual IF spread is 1-2.5%, so IF choice within that class is not the limit, while the alpha1-versus-RAR shape question is (20%).
- **Wide binaries:** not an a0 measurement; they probe the boost nu(y), y = g_N/a0, in the Galaxy's external field. Sensitivity d ln nu/d ln a0 is 0.39 (y = 0.3) and 0.14 (y = 3) averaged over the four IFs (0.385 / 0.125 for the record kernel, analytic 1/(2(1+y))). To fix a0 to 1.8% the boost must be known to 0.7% (y ~ 0.3) or 0.3% (y ~ 3), to 4.1% (F vs 2 pi) 1.6%, and the external-field model, IF and contamination must be controlled at the same level.
- **a0 at z ~ 2.5:** the flat and cH(z) laws differ by 0.576 dex there (E = 3.767), so such a point separates the two **footings**, not Z = 5.79 from 6 (that needs 1.8%; single-object precision in the record is 0.13 dex = 35%). A published claim (2604.22613, abstract/HTML summary only) of a0(z ~ 0.9) = 2.38 +/- 0.11 against a local 1.0-1.2 would strain both z-laws (flat by ~2x, cH(z) by ~1.3x, measurement error only; their stated systematics include gas mass ~0.2 dex and the disc-halo decomposition). I do not evaluate it; the record's own audit calls MUSE non-diagnostic.

## 6. Is the supported statement 'a0 = cH/(6 +/- 0.5)-ish' rather than 'a0 = cH/5.789'?
Yes, with two qualifications. (i) The width: on the rho_total footing at H0 = 67.4 the 68% half-widths are +/-0.33 (record as quoted), +/-0.46 (Desmond 2023), +/-0.73 (ensemble), +/-1.1 (MLS16), so '6 +/- 0.5' is the lower end of the honest range; the central value is 5.5-6.1. (ii) The footing: on the rho_Lambda footing the same statement is cH_Lambda/(4.9 +/- 0.6) and 5.789 sits 1.3 sigma above the ensemble (2.5 sigma above the record as quoted, but inside the systematic budget, section 4). 'a0 = cH/5.789' is one point inside the allowed interval; it is not selected by the data over 6 or 2 pi at any footing, H0 or error treatment tested, and it is not excluded either. The forced kernel (kappa = 1) is excluded; kappa = 0.43-0.55 (rho_total) or 0.52-0.66 (rho_Lambda) at 68%.

## Controls (each would fail if the claim were wrong)
Mutations behave as expected: wrong-sign footing (H0/sqrt(Omega_L)) moves Z_hat by exactly 1/Omega_L = 1.4599 (found 1.4598); wrong H0 (73 for 67.4) by 73/67.4 (found 1.0831); halving a0 doubles Z; data placed exactly at F, V or M make that hypothesis the maximum-likelihood one; halving the error doubles every sigma separation; Omega_Lambda scales as a0^2 and H0^-2 and 2 pi in place of Z_F changes it by 3 pi/8 = 1.178; a km-to-m slip in the log-table conversion would give 12.5 not 1.25; a wrongly implemented distance transform fails the g_bar-invariance test; mocks recover an injected a0 unbiasedly with the right kernel and are biased +20% / -23% with the wrong one; injected Z intervals cover 68.3% / 95%; the a0 profile reproduces the record's chi2, sigma_int, n_pts, a0 and both sigmas on its own grid; the fixed-Upsilon fits reproduce the ESR-paper values (1.11 / 1.13 / 1.54) within 6%.

## Own errors fixed openly
(1) My first inclination transform clipped cos(90 deg) and boosted V_bar 4x for edge-on discs, so both signs of the shift lowered a0; the 'opposite signs' sanity check caught it (fixed by capping at 85 deg). (2) My first distance-transform 'mutation' sat on the bracket boundary and could not fail; replaced by a g_bar-invariance unit test with a mutation that does fail. (3) I mis-remembered three Rodrigues/Chang-Zhou conversions (1.2505 vs 1.2531, 1.0965 vs 1.0990) in the first check; the computed values were right, the expectation was wrong. (4) Monte-Carlo marginal likelihoods were 27% off in the far tails; replaced by Gauss-Hermite quadrature (0.03% agreement near the peak). (5) My first power-check expectation at 1% error was wrong (F over V reaches BF > 3 in 85%, not < 60%); replaced by the analytic expectation. (6) The record's 1.24% and 5.44% are reproduced but are coarse-grid values (1.59% and 7.0% on a fine grid).

## What is NOT established
- The ensemble E is not a sample of independent measurements; its sd (12%) is a scale for analysis-choice systematics. Other constructions give 8% (Desmond 2023) to 20% (MLS16); the conclusion (no discrimination) holds for all of them (section 3 table).
- The perturbation budget uses coherent shifts (global distance scale +/-5%, gas +/-10%, inclination +/-1 sigma_i), which overstate what independent per-galaxy errors do; it is not a full marginalisation. The -13.8% 'all distances x73/67.4' item assumes the whole distance ladder scales with H0.
- H0 and Omega_Lambda are treated as independent (as briefed); their Planck correlation is not modelled. The physical-Lambda variant is reported but the H0-tension worlds are sensitivity statements.
- Upsilon and IF results use the record's profile likelihood (fixed sig_int = 0.0808, calibrated for alpha1; recalibrating per IF changes a0_hat by < 1% (check I3)). The alpha1-versus-RAR preference is d chi2 = 168 on independent points but only about 3 sigma after the crude clustering deflation; 16 mocks per truth are few.
- The gas-/star-dominated a0 split (2.3x Upsilon-free, 1.46x cleanest) is descriptive; its cause (Upsilon freedom, gas calibration, dwarf distances, non-circular motions) was not investigated.
- Not opened: Milgrom 2001.09729, the original Begeman et al. 1991 paper, the 2025 z = 0.05 paper; 2001.08340 and 2604.22613 only at abstract / summary level; the KiDS lensing paper gives no formal a0. I made no Gaia DR4, JWST or ALMA forecast.
- Nothing here bears on why 32 pi: kappa = 1/2 stays FITTED and I derive nothing.

## Verdict
**NOTHING NEW on the derivation.** The evidence lane result is quantitative and negative for discrimination: the data allow Z = 5.79, 6 and 2 pi equally (BF 0.9-1.1, 0.3-0.7 sigma apart on the rho_total footing), the a0 systematics (IF 12%, Upsilon treatment 12%, galaxy class 19%, distance scale 9%) and the H0 tension (8%) each exceed the 1.8% needed to separate 5.789 from 6, and the Omega_Lambda offset is inside that budget. Side finding for the record: its SPARC a0 and its kappa = 1/2-versus-2 pi preference are conditional on the alpha = 1 kernel, which the same data disfavour against RAR-like shapes.
