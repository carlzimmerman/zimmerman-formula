# AGB4R — blind re-grade of AGB4 (published host ages, SDSS-II hosts, Pantheon+ magnitudes): result

2026-11-14. Independent second implementation, written from AGB4's `FROZEN_CRITERIA.md` alone (plus AGB2
amendment 1 for the weights and AGB1's frozen W1 thresholds). My reading of the rules, with every ambiguity
resolved, is `READING.md`, committed alone (73f6016fa4) before any fit. The loaders and run script were
committed (20049979ab) before any real-data fit. No AGB4 file other than its frozen criteria was opened, and no
README, script, output or result of any other AGB folder.

## Words

| | word |
|---|---|
| **M0** (no mass step) | **SLOPE OVERPREDICTS THE HOSTS AT 3 SIGMA, FRAGILE (sample `big`)** |
| **M1** (mass step free) | **AGE BIAS EXCLUDED AT 3 SIGMA, ROBUST** |
| Rose rows | **NOT EVALUABLE** (KR failed) |

Primary: `pp`, reading R, FSPS ages, 8 bins, 286 supernovae.
- M0: Â = +0.299 ± 0.194; Δχ²(A=0) = 2.37; Δχ²(A=1) = 13.03. Â < 1 and Δχ²(A=1) ≥ 9.
- M1: Â = +0.195 ± 0.210; g = +0.028 ± 0.021 mag; Δχ²(A=0) = 0.86; Δχ²(A=1) = 14.75. Δχ²(A=1) ≥ 9, Δχ²(A=0) < 4.

## Known-answer checks (judged before the words were read)

| check | value | rule | result |
|---|---|---|---|
| K1 match | 321 of 321 found; max \|zHD − z_CMB(table)\| = 0.0205 on `pp` (0 rows > 0.03); r(mass P+, FSPS) = 0.849 | all found, ≤ 0.03, ≥ 0.80 | **PASS** |
| K2 ages sort progenitors | low-stretch share 0.372 (age ≥ 6, n 86) − 0.045 (n 200) = **0.327** | ≥ 0.15 | **PASS** |
| K3 mutation twins | 8 of 8: worst \|Â − A_true\| 3e-12, worst χ²_min 1.6e-22; script exit 3 | ≤ 1e-6, ≤ 1e-8 | **PASS** |
| K4 M0 | σ_A 0.1942; shuffle mean −0.074 σ_A; scatter 0.867 σ_A; sandwich (HC0) 1.095 σ_A (HC1 1.117) | ≤ 0.2; [0.8, 1.25]; [0.8, 1.25] | **PASS** |
| K4 M1 | σ_A 0.2096; shuffle mean −0.090 σ_A; scatter 0.929 σ_A; sandwich (HC0) 1.034 σ_A (HC1 1.057) | same | **PASS** |
| KR Rose et al. | step (younger − older, local age split at 8 Gyr, weighted) **0.207 ± 0.021** mag (86 younger, 17 older); unweighted 0.202 ± 0.037 | within 0.04 of 0.114 | **FAIL** → Rose rows NOT EVALUABLE |

M0 and M1 are evaluable (K1, K2, K3 pass) and each keeps its word (K4 passes for both).

Implementation sanity (`agb4r_sanity.out`, not frozen checks): μ_fid matches the Einstein–de Sitter closed form
to 1e-14 and a fine trapezoid to 4e-14 mag; a second solver (QR / lstsq) gives the same Â and σ_A to 1e-6;
Δχ² from refitting with A fixed equals ((Â − k)/σ_A)² to 6e-11 in every fit; bins are equal-count (35/36 per bin).
Design-only σ_A reproduce the frozen forecasts: 0.194 / 0.210 [0.19 / 0.21], Rose global 0.243, local 0.252
[0.24, 0.25].

## Every amplitude (weighted least squares, diagonal weights, formula error)

**Primary and the four forks of the second word** (one change at a time):

| fit | M0: Â ± σ | Δχ²(0) | Δχ²(1) | M0 word | M1: Â ± σ | Δχ²(0) | Δχ²(1) | M1 word |
|---|---|---|---|---|---|---|---|---|
| primary (`pp`, R, 8 bins, N 286) | +0.299 ± 0.194 | 2.37 | 13.03 | OVERPREDICTS AT 3σ | +0.195 ± 0.210 | 0.86 | 14.75 | EXCLUDED AT 3σ |
| reading P | +0.038 ± 0.168 | 0.05 | 32.81 | OVERPREDICTS AT 3σ | +0.100 ± 0.189 | 0.28 | 22.78 | EXCLUDED AT 3σ |
| 12 bins | +0.298 ± 0.195 | 2.34 | 12.95 | OVERPREDICTS AT 3σ | +0.174 ± 0.211 | 0.68 | 15.29 | EXCLUDED AT 3σ |
| sample `big` (N 1,092, 16 bins) | +0.707 ± 0.174 | 16.41 | 2.83 | **HOSTS AS LARGE AS THE SLOPE NEEDS** | +0.271 ± 0.199 | 1.84 | 13.39 | EXCLUDED AT 3σ |
| `pp` without wide intervals (N 278) | +0.348 ± 0.200 | 3.05 | 10.68 | OVERPREDICTS AT 3σ | +0.230 ± 0.214 | 1.16 | 12.92 | EXCLUDED AT 3σ |
| *reading only:* without wide intervals, either-side reading (N 248) | +0.495 ± 0.225 | 4.82 | 5.03 | *OVERPREDICTS (2σ)* | +0.407 ± 0.243 | 2.79 | 5.95 | *DISFAVOURED* |

Mass steps in M1: `pp` R +0.028 ± 0.021, P −0.015 ± 0.021, 12 bins +0.032 ± 0.021, `big` **+0.099 ± 0.022**,
no-wide +0.032 ± 0.021. Stretch and colour (R): a ≈ −0.14, b ≈ 2.57 (`pp`); a ≈ −0.125, b ≈ 2.49 (`big`).
χ²/dof: `pp` R 298.3/275 (M0), 296.5/274 (M1); `big` 1376.2/1073, 1355.8/1072.

**Reported rows (no word)**, `pp` reading R, 8 bins unless stated:

| row | M0: Â ± σ (Δχ²(0), Δχ²(1)) | M1: Â ± σ (Δχ²(0), Δχ²(1)) |
|---|---|---|
| Rose global age, `rose` N 66, 4 bins, R — NOT EVALUABLE (KR) | +0.349 ± 0.243 (2.07, 7.16) | +0.206 ± 0.268 (0.59, 8.76) |
| Rose global age, P — NOT EVALUABLE (KR) | +0.192 ± 0.218 (0.78, 13.76) | +0.253 ± 0.254 (0.99, 8.67) |
| Rose local age, R — NOT EVALUABLE (KR) | +0.569 ± 0.252 (5.08, 2.92) | +0.464 ± 0.282 (2.71, 3.62) |
| Rose local age, P — NOT EVALUABLE (KR) | +0.429 ± 0.239 (3.22, 5.70) | +0.562 ± 0.276 (4.15, 2.53) |
| FSPS age on the same 66, R (for comparison) | +0.408 ± 0.391 (1.09, 2.29) | +0.130 ± 0.436 (0.09, 3.98) |
| PEGASE age | +0.111 ± 0.098 (1.30, 82.8) | +0.089 ± 0.099 (0.82, 85.4) |
| `big`, 387 spectroscopic, 16 bins | +0.622 ± 0.264 (5.56, 2.06) | +0.239 ± 0.294 (0.66, 6.72); g +0.090 ± 0.030 |
| split at 6 Gyr, continuous hinge (my primary reading): below / above | +0.554 ± 0.309 / −0.164 ± 0.478 (corr −0.46) | +0.411 ± 0.333 / −0.163 ± 0.478 (corr −0.42) |
| split at 6 Gyr, two pieces D[age<6], D[age≥6]: below / above | +0.313 ± 0.350 / +0.305 ± 0.231 (corr +0.92) | +0.158 ± 0.369 / +0.178 ± 0.250 (corr +0.93) |

**Low-stretch share (Pantheon+ x1 < −1) against FSPS age**, `pp`: < 2 Gyr 0.00 (n 3); 2–4 0.026 (77); 4–6 0.058
(120); 6–8 0.347 (72); 8–14 0.500 (14). r(age, x1) = −0.470; r(PEGASE age, x1) = −0.107.

**Reliability of the FSPS age, stretch and host mass as witnesses** (inside the 8 bins, fit weights):
var(W) = 2.569 Gyr² (within-bin spread 1.60 Gyr); shared = 1.992 → reliability **0.775**, noise 0.577 Gyr².

| | var of W left in fit | reliability in fit | Â / reliability | Δχ²(0), Δχ²(1) of the corrected value |
|---|---|---|---|---|
| M0, Z2 = Pantheon+ mass | 1.921 | 0.699 | **+0.428 ± 0.278** | 2.37, 4.24 |
| M1, Z2 = Pantheon+ mass | 1.648 | 0.649 | **+0.300 ± 0.323** | 0.86, 4.70 |
| M0, Z2 = FSPS mass (variant) | 1.921 | 0.761 | +0.393 ± 0.255 | 2.37, 5.67 |
| M1, Z2 = FSPS mass (variant) | 1.648 | 0.722 | +0.270 ± 0.290 | 0.86, 6.32 |

As the criteria say, the like-for-like comparison with the published slope is the uncorrected one (the slope was
measured on ages of this kind, noise included). The corrected value sits about 2σ below A = 1, not 3σ.

## Post hoc (written after the words were read; changes no word) — `agb4r_posthoc.out`
- **KR.** The frozen reading uses the `mu` column of `campbell_local.tsv` minus a flat Ω_m = 0.3 line: 0.207. The
  file's own `hr` column gives 0.152 (weighted) and 0.139 (unweighted), which would be within 0.04 of 0.114. The
  `hr` column is not `mu` minus any smooth Hubble line: the two differ object by object with a scatter of 0.061 mag
  for every Ω_m tried. So Rose et al.'s residuals come from a standardisation the `mu` column does not carry. Under
  the frozen rule KR fails and the Rose rows stay NOT EVALUABLE.
- **Rescaling the formula error by χ²/dof** (1.04–1.12 for `pp`, 1.27–1.28 for `big`) changes no first word in any
  fork. The closest is `pp` without wide intervals, M0: Δχ²(A=1) 10.68 → 9.59, still ≥ 9.
- The 8–14 Gyr low-stretch share is 0.500 (7 of 14) with either stretch column. The criteria quote 0.47.

## What I think is under-specified or wrong in the criteria
1. **"Hosts whose stated age interval is wider than ± 2.5 Gyr" moves a second word.** I read it as half-width
   (age_hi − age_lo)/2 > 2.5 Gyr (8 hosts removed). Read as "either side longer than 2.5 Gyr" (38 removed), the fork
   gives AGE BIAS DISFAVOURED for M1 and SLOPE OVERPREDICTS THE HOSTS (2 SIGMA) for M0. Under that reading M1 would
   be **FRAGILE (`pp` without wide intervals)** and M0 FRAGILE (`big`, `pp` without wide intervals). So M1's ROBUST
   depends on that one reading. The first words do not change.
2. **KR is ill-posed against the files fetched.** The step depends on whether one uses `mu` or the file's own `hr`
   (0.207 against 0.139–0.152). The criteria say "their distance moduli". Neither comes closer to the published
   0.114 than 0.025. The check may also have needed Rose et al.'s own probabilistic split, not a hard cut at
   8 Gyr (17 hosts are older; one sits at exactly 8.0, counted as older).
3. **`big` needs the positive lower age bound too.** The criteria state it only for `pp`, but the frozen count
   1,092 (387) is reached only with it (1,095 / 389 without).
4. **Reading P is not a fit with no mass step.** Pantheon+'s m_b_corr already carries its own host-mass correction.
   So "M0 in reading P" is not the no-step fit that the M0 rationale describes.
5. **The `big` fork tests a different thing under M0.** In `big` the mass step is large (+0.099 ± 0.022 in M1).
   Without it (M0), the age template absorbs it (Â 0.71). With it, Â falls to 0.27, matching `pp`. The M0
   FRAGILE comes from this mass–age degeneracy, not from the ages of `pp`.
6. **K4 audits only the primary configuration.** `big`'s weights (muerr² + 0.1²) give χ²/dof 1.28, and its error
   is not audited by any shuffle or sandwich.
7. **"Split of the template at 6 Gyr" admits two readings, and they disagree.** A continuous hinge gives slopes
   below and above. Two pieces through age 0 give amplitudes that are 92 % correlated and mostly measure the level
   of the old group. Both are reported.
8. **The reliability method reads high against the criteria's own error budget.** The criteria give errors of
   about ± 1.7 Gyr against a within-bin spread of 1.6 Gyr; taken literally, that budget leaves no room for any
   signal (1.7² > 1.6²).
   The witness method gives 0.78 (0.82 with the FSPS mass, which shares its photometric fit with the age). That
   suggests some fitting noise is shared between the age and the witnesses. The corrected amplitude should
   therefore be read as an upper bound on the correction, not its size. This row carries no word.
9. Implementation-dependent details that will not match the lane bit for bit: the mapping of seed 20261117 to
   permutations, tie-breaking of the equal-count bins, and HC0 versus HC1 for the sandwich (both printed, both pass).

## Files
`READING.md`, `agb4r_data.py`, `agb4r_run.py` (modes k1 k2 k3 kr k4 fits rows words; one `.json` and one `.out`
each), `agb4r_sanity.py` / `.out`, `agb4r_posthoc.py` / `.out` (post hoc, labelled), this file.
Run: `python3 -I agb4r_run.py MODE > agb4r_MODE.out` from this folder; `k3` exits 3 on pass.

kappa = 1/2 FITTED; not theory closed.
