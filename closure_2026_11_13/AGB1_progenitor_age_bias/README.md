# AGB1 — the supernova progenitor-age bias on DESI DR2 BAO and the DES-SN5YR Dovekie supernovae

Commit ids, local / origin: criteria 27faac7b3e / 31e18a2caa (alone, before any script); scripts bb0a1c246b /
347646898b (before any real-data number); result 45d6341180 / d223c720b9.
Labels: `agb1_collect.out`, `agb1_results.json`. Per-run files: `agb1_<MODE>.{json,out}`, `agb1_cfg68x_*`.
A test of a published claim on public data. It adopts nothing and edits no ledger.

## Verdict
Son et al. (arXiv:2510.13121) say a progenitor-age correction to supernova magnitudes turns the supernova + BAO + CMB
fit into a universe that is not accelerating today. Three questions were frozen. Every known-answer check passes.

1. **Amplitude (W1): UNDECIDED / ROBUST.** With A = 0 the published moduli and A = 1 the correction at its published
   size, the BAO + supernova fit gives A = 0.62 (68 % 0.19 to 1.05). Neither end is excluded: Δχ² 2.10 at A = 0 and 0.79
   at A = 1. Dropping the legacy low-redshift supernovae gives A = 0.35 (−0.12 to 0.81), still UNDECIDED; so does
   keeping only the BAO bins inside the supernova range.
2. **Today (W2).** Published moduli: **ACCELERATING TODAY** (q0 −0.37, Δχ² 18.6 against q0 = 0). Correction at full
   size: **SIGN NOT SETTLED** (q0 +0.14, Δχ² 3.4, under the frozen line of 4). Amplitude free: **SIGN NOT SETTLED**
   (q0 −0.05, Δχ² 0.05).
3. **Ever (W3): NEVER-ACCELERATED EXCLUDED AT 3 SIGMA in every fork.** Δχ² 168 with the published moduli, 37.5 with
   the correction at full size, 28.7 with the amplitude free. With the correction on, the best fit still has q < 0
   around z 0.3 to 0.5 (q −0.15 at z 0.40).

**Part C (the same with DESI's compressed CMB prior; inherited early-universe physics): the same words.**
W1c UNDECIDED / ROBUST (A = 0.62, 0.23 to 1.02); W2c ACCELERATING TODAY / SIGN NOT SETTLED / SIGN NOT SETTLED;
W3c NEVER-ACCELERATED EXCLUDED AT 3 SIGMA in every fork (Δχ² 199, 57.0, 39.3).

**Part B (this repository's Dovekie lanes re-read with the correction at A = 1): they lean on the age question.**
CFG684's flat-a0 Ω_m is AGE-DEPENDENT (0.307 → 0.350). CFG689's tracking band is SHIFTED at z* 1.0 and 1.2 and STABLE
at 1.5 and 2.33, CLASS UNCHANGED, in both modes and both samples.

In one sentence: the distances on disk neither confirm nor exclude the published correction, and granting it in full
leaves the sign of the acceleration today open but does not undo the acceleration itself.

## Checks (all judged before the words were read)
| check | result | target |
|---|---|---|
| KT template | Δage_S(1.0) 5.44 Gyr, T_S(1.0) 0.163 mag, Δage_W(1.2) 1.99 Gyr: PASS | 5.0–5.6, 0.15–0.17, 1.7–2.1 |
| K1 BAO only, flat ΛCDM | Ω_m 0.2973, h r_d 101.55 Mpc: PASS | 0.2975 ± 0.003, 101.54 ± 0.3 |
| K2 supernovae only, flat ΛCDM | Ω_m 0.3303: PASS | 0.330 ± 0.0075 |
| K4 integrator against CAMB | largest relative difference 4.5 × 10⁻⁴: PASS | ≤ 10⁻³ |
| K3a / K3b mutation twins | A recovered as 1.00000 / 0.00000, (w0, wa) to 10⁻⁵: PASS / PASS | see criteria |
| KA profile against analytic fit | spline 0.6181 against 0.6182: PASS | within 0.03 |
| K5 (Part C) BAO + prior | Δχ²(w0–wa − ΛCDM) −8.24: PASS | −8.0 ± 1.0 |
| K6 (Part C) + supernovae, A = 0 | w0 −0.820, wa −0.643: PASS | −0.803 ± 0.040, −0.72 ± 0.16 |

The noise-free twins put Δχ² 5.4 to 5.6 between A = 0 and A = 1, so these data could at best have reached the 2σ words.

## Part A — BAO + supernovae, no CMB
Amplitude (template T_S):

| sample | n | best A | 68 % | 95 % | Δχ²(A=0) | Δχ²(A=1) | W1 |
|---|---|---|---|---|---|---|---|
| full | 1,820 | +0.618 | 0.191 to 1.049 | −0.233 to 1.484 | 2.10 | 0.79 | UNDECIDED |
| des_only (legacy dropped) | 1,623 | +0.346 | −0.123 to 0.813 | −0.569 to 1.281 | 0.54 | 1.96 | UNDECIDED |
| rand197 (size control) | 1,623 | +0.725 | 0.283 to 1.170 | −0.155 to 1.620 | 2.71 | 0.38 | UNDECIDED |
| bao_overlap (BAO z < 1.2 only) | 1,820 | +0.681 | 0.238 to 1.122 | −0.209 to 1.563 | 2.35 | 0.52 | UNDECIDED |

The lean towards a drift (A = 0 sits 1.4σ from the best fit on `full`) halves when the legacy set is dropped and does
not when 197 DES supernovae are dropped at random. So part of it rests on the legacy set.

The three forks:

| sample | fork | Ω_m | w0 | wa | q0 | smallest q (z) | Δχ²(q0=0) | W2 | Δχ²(never) | W3 |
|---|---|---|---|---|---|---|---|---|---|---|
| full | A = 0 | 0.314 | −0.843 | −0.538 | −0.367 | −0.367 (0) | 18.64 | ACCELERATING TODAY | 168.1 | EXCLUDED AT 3 SIGMA |
| full | A = 1 | 0.368 | −0.377 | −1.935 | +0.142 | −0.151 (0.40) | 3.41 | SIGN NOT SETTLED | 37.5 | EXCLUDED AT 3 SIGMA |
| full | A free (0.62) | 0.347 | −0.561 | −1.391 | −0.049 | −0.181 (0.29) | 0.05 | SIGN NOT SETTLED | 28.7 | EXCLUDED AT 3 SIGMA |
| des_only | A = 0 | 0.288 | −1.002 | +0.247 | −0.570 | −0.570 (0) | 11.56 | ACCELERATING TODAY | 98.8 | EXCLUDED AT 3 SIGMA |
| des_only | A = 1 | 0.359 | −0.453 | −1.613 | +0.064 | −0.145 (0.36) | 0.18 | SIGN NOT SETTLED | 34.2 | EXCLUDED AT 3 SIGMA |
| des_only | A free (0.35) | 0.315 | −0.819 | −0.419 | −0.342 | −0.342 (0) | 1.06 | SIGN NOT SETTLED | 27.5 | EXCLUDED AT 3 SIGMA |
| bao_overlap | A = 0 | 0.300 | −0.851 | −0.285 | −0.394 | −0.394 (0) | 9.47 | ACCELERATING TODAY | 144.2 * | EXCLUDED AT 3 SIGMA |
| bao_overlap | A = 1 | 0.256 | −0.407 | −0.854 | +0.046 | −0.117 (0.49) | 0.12 | SIGN NOT SETTLED | 20.9 * | EXCLUDED AT 3 SIGMA |
| bao_overlap | A free (0.68) | 0.264 | −0.542 | −0.579 | −0.099 | −0.143 (0.26) | 0.17 | SIGN NOT SETTLED | 16.8 * | EXCLUDED AT 3 SIGMA |

"EXCLUDED AT 3 SIGMA" is short for NEVER-ACCELERATED EXCLUDED AT 3 SIGMA.
\* AT PRIOR EDGE: the never-accelerated fit of `bao_overlap` sits on Ω_m = 0.05 (a nearly empty, coasting universe), so
a wider Ω_m range could lower these three numbers. `bao_overlap` is a control and carries no W3 word of its own.
On the amplitude grid every point from A = 1.8 upward sits on wa = −3; the 95 % upper limit (1.48) is below that.
The BAO scale moves with the amplitude: h r_d 99.4 Mpc at A = 0, 92.9 at A = 1, 95.4 at the best A (`full`).

## Part C — with DESI's compressed CMB prior
| sample | best A | 68 % | 95 % | Δχ²(A=0) | Δχ²(A=1) | W1c |
|---|---|---|---|---|---|---|
| full | +0.624 | 0.231 to 1.021 | −0.158 to 1.424 | 2.54 | 0.90 | UNDECIDED |
| des_only | +0.533 | 0.141 to 0.929 | −0.248 to 1.331 | 1.85 | 1.38 | UNDECIDED |

| sample | fork | Ω_m | w0 | wa | q0 | smallest q (z) | Δχ²(q0=0) | W2c | Δχ²(never) | W3c |
|---|---|---|---|---|---|---|---|---|---|---|
| full | A = 0 | 0.313 | −0.820 | −0.643 | −0.345 | −0.345 (0) | 27.37 | ACCELERATING TODAY | 199.3 | EXCLUDED AT 3 SIGMA |
| full | A = 1 | 0.358 | −0.396 | −1.732 | +0.118 | −0.142 (0.40) | 3.57 | SIGN NOT SETTLED | 57.0 | EXCLUDED AT 3 SIGMA |
| full | A free (0.62) | 0.340 | −0.561 | −1.299 | −0.055 | −0.177 (0.28) | 0.08 | SIGN NOT SETTLED | 39.3 | EXCLUDED AT 3 SIGMA |
| des_only | A = 0 | 0.308 | −0.878 | −0.460 | −0.412 | −0.412 (0) | 13.28 | ACCELERATING TODAY | 118.2 | EXCLUDED AT 3 SIGMA |
| des_only | A = 1 | 0.353 | −0.458 | −1.529 | +0.056 | −0.143 (0.36) | 0.25 | SIGN NOT SETTLED | 50.4 | EXCLUDED AT 3 SIGMA |
| des_only | A free (0.53) | 0.331 | −0.661 | −1.002 | −0.163 | −0.212 (0.19) | 0.57 | SIGN NOT SETTLED | 38.5 | EXCLUDED AT 3 SIGMA |

The fitted h falls from 0.673 (A = 0) to 0.631 (A = 1) on `full`.

## Part B — CFG684 and CFG689 with the correction at A = 1
Harness checks: `cfg684 full A=0` equals the committed `cfg684_results.json` (max |diff| 0); `cfg689 TD5F des_only A=0`
equals LGS1's committed file (max |diff| 0). The committed lane files are untouched.

CFG684 (each row against A = 0 of the same sample, from LGS1's committed outputs):

| sample | combination | flat-a0 Ω_m, A = 0 | A = 1 | shift (combined sd) | A2 | Δχ²_max | A1 | √X(2.33) band | A3 |
|---|---|---|---|---|---|---|---|---|---|
| full | BAO+DES5 | 0.3067 ± 0.0074 | 0.3503 ± 0.0066 | +0.0436 (0.0099) | AGE-DEPENDENT | 1.67 → 1.36 | NOT BROKEN | 0.690–2.168 → 1.320–2.631 | FLOOR HOLDS |
| full | BAO+DES5+CC | 0.3070 ± 0.0073 | 0.3505 ± 0.0062 | +0.0436 (0.0096) | AGE-DEPENDENT | 1.72 → 1.46 | NOT BROKEN | 0.687–2.166 → 1.419–2.627 | FLOOR HOLDS |
| des_only | BAO+DES5 | 0.2917 ± 0.0085 | 0.3330 ± 0.0092 | +0.0413 (0.0125) | AGE-DEPENDENT | 0.11 → 0.19 | NOT BROKEN | 0–2.019 → 0–2.513 | FLOOR LOST |
| des_only | BAO+DES5+CC | 0.2920 ± 0.0080 | 0.3331 ± 0.0088 | +0.0411 (0.0119) | AGE-DEPENDENT | 0.16 → 0.17 | NOT BROKEN | 0–2.026 → 0–2.508 | FLOOR LOST |

CFG689 (60,000 steps, same seeds, chain check ok in all four runs). Tracking √X, 68 % band (median), A = 0 → A = 1:

| mode | sample | z* 1.0 | z* 1.2 | z* 1.5 | z* 2.33 |
|---|---|---|---|---|---|
| D5 | full | 0.811–1.057 (0.950) → 0.973–1.197 (1.098) SHIFTED | 0.780–1.059 (0.941) → 0.954–1.204 (1.096) SHIFTED | 0.677–1.099 (0.927) → 0.870–1.258 (1.094) STABLE | 0.338–1.207 (0.908) → 0.737–1.423 (1.152) STABLE |
| D5 | des_only | 0.805–1.036 (0.934) → 0.948–1.167 (1.069) SHIFTED | 0.789–1.048 (0.936) → 0.943–1.182 (1.077) SHIFTED | 0.716–1.099 (0.937) → 0.884–1.242 (1.088) STABLE | 0.506–1.222 (0.953) → 0.812–1.418 (1.173) STABLE |
| TD5F | full | 0.912–1.031 (0.973) → 1.003–1.135 (1.070) SHIFTED | 0.895–1.003 (0.949) → 0.983–1.103 (1.044) SHIFTED | 0.781–1.032 (0.912) → 0.857–1.133 (1.001) STABLE | 0.678–1.045 (0.879) → 0.747–1.149 (0.970) STABLE |
| TD5F | des_only | 0.870–0.991 (0.932) → 0.953–1.087 (1.021) SHIFTED | 0.860–0.969 (0.916) → 0.943–1.064 (1.003) SHIFTED | 0.762–1.004 (0.889) → 0.835–1.103 (0.975) STABLE | 0.654–1.009 (0.848) → 0.715–1.105 (0.927) STABLE |

B2: CLASS UNCHANGED in all four runs (P1 DEGENERACY BROKEN; D5 P0 FLAT CONSISTENT).

Reported, no frozen label:
- **CFG689's own class for constant dark energy (P2) changes in every run.** D5 full 7.78 (1.38σ, CONSISTENT WITH
  CONSTANT) → 85.89 (8.39σ, EVOLVING DE REQUIRED); D5 des_only 6.96 (1.22σ) → 29.84 (4.32σ, EVOLVING DE REQUIRED);
  TD5F full 11.32 (2.00σ, HINT) → 131.52 (10.69σ, EVOLVING DE REQUIRED); TD5F des_only 9.02 (1.61σ, CONSISTENT WITH
  CONSTANT) → 37.01 (4.99σ, EVOLVING DE REQUIRED).
- **Native H0** falls by about 4.2 km/s/Mpc: D5 67.85 → 63.65 (full), 69.40 → 65.23 (des_only); TD5F 67.73 → 63.53,
  69.27 → 65.05.
- e_3σ changes by at most 0.014.

Reading: if the correction is right at full size, the tracking curve at z about 1 sits 2 to 10 % above today's value
in place of 3 to 7 % below it, and the framework's own-ruler lane would call evolving dark energy required. If the
correction is absent the committed numbers stand. W1 does not say which.

## Reported only (no frozen word)
- **Template T_W (short-delay age history, same slope).** `full`: best A_W 2.28, 68 % lower limit 0.60, upper limits
  beyond the grid; Δχ² 1.84 at A_W = 0, 1.49 at 0.23 (Wiseman et al.'s own slope), 0.58 at 1. `des_only`: 1.94, lower
  limit 0.18; Δχ² 1.21, 0.94, 0.28. In magnitudes by z = 1 the two templates ask for the same drift (0.62 × 0.163 = 0.10
  mag; 2.28 × 0.058 = 0.13 mag): the distances constrain the size of a drift by z about 1, not the age history behind it.
- **Legacy offset.** A constant step between the 197 legacy supernovae and the DES ones, alone: δ = +0.034 mag (legacy
  fainter than the DES-anchored model), Δχ² 1.69 against δ = 0, and the fit returns to w0 −0.988, wa +0.121.
  With δ and A both free: A = 0.50 (0.05 to 0.95), Δχ² 1.21 at A = 0 and 1.23 at A = 1, δ = +0.024 mag.
  A step between surveys and a smooth drift share the lean; neither is required.
- **Son et al.'s printed fits beside ours** (PROVISIONAL web reading; they used the older DES-SN5YR calibration and
  the full CMB likelihoods; ours are best fits on Dovekie):

  | combination | Son et al. (Ω_m, w0, wa, q0) | AGB1 |
  |---|---|---|
  | BAO + supernovae, corrected, no CMB | 0.374 ± 0.011, −0.320 ± 0.072, −2.136 ± 0.386, +0.199 ± 0.070 | 0.368, −0.377, −1.935, +0.142 |
  | BAO + CMB + supernovae, corrected | 0.363 ± 0.006, −0.337 ± 0.062, −1.902 ± 0.246, +0.178 ± 0.061 | 0.358, −0.396, −1.732, +0.118 |
  | BAO + CMB + supernovae, uncorrected | 0.319 ± 0.006, −0.754 ± 0.056, −0.848 ± 0.217, −0.271 ± 0.061 | 0.313, −0.820, −0.643, −0.345 |
  | BAO + CMB, no supernovae | w0 −0.430 ± 0.207, wa −1.704 ± 0.580, q0 +0.075 ± 0.215 | 0.351, −0.448, −1.638, +0.063 |

  The rebuilt template reproduces their direction and size. Their q0 > 0 at about 2.9σ becomes Δχ² 3.4 to 3.6 here.

## Post hoc (written after the Part A numbers were seen; `agb1_posthoc_nosn.py`; no frozen word)
The today and ever questions with **no supernova in the fit**, so nothing depends on the age dispute:

| data | Ω_m | w0 | wa | q0 | smallest q (z) | Δχ²(q0=0) | Δχ²(never) |
|---|---|---|---|---|---|---|---|
| DESI DR2 BAO alone | 0.386 | −0.183 | −2.706 | +0.331 | −0.177 (0.46) | 0.65 | 29.5 |
| BAO + compressed CMB prior | 0.351 | −0.448 | −1.638 | +0.063 | −0.159 (0.37) | 0.07 | 39.8 |

BAO alone cannot say whether the expansion is speeding up today, and BAO alone excludes a flat w0–wa universe that
never accelerated.

## Independent spot checks (scratch script, not part of the frozen files)
- χ² at the A free, A = 0 and A = 1 best fits of `full` and `des_only`, recomputed with adaptive quadrature per redshift
  and explicit least squares for the offset, the amplitude and the BAO scale: supernova χ² agrees to 1.1 × 10⁻⁴, BAO χ²
  to 4 × 10⁻⁶, A and h r_d to every printed digit.
- A global optimiser (differential evolution) finds the same unconstrained and q0 = 0 minima to 10⁻⁴ in all six forks.
  Its never-accelerated minima are 0.06 to 0.74 lower than the lane's because its single penalty lets q dip to
  −0.0002 to −0.0006; no word moves (smallest Δχ²_never 27.4).

## What this says and does not say
- It does not say the age bias is real or absent. A is the size of a redshift drift with the Son et al. shape; a
  calibration step between surveys, selection, dust, or an expansion history outside the flat w0–wa family would fit
  the same way. Whether progenitor age causes any of it is a host-galaxy question this lane does not read.
- A = 1 is the published size applied on top of the DES team's own host-mass step. If that step already removes part
  of an age effect (Wiseman et al.'s argument), A = 1 double counts and is the upper end.
- The template is a rebuild of a plotted curve from the paper's stated recipe. It matches the two numbers the paper
  prints (5.3 Gyr, about 0.16 mag) and reproduces its fits; its shape below z 0.3 is not checked against the figure.
- All words live inside the flat w0–wa family, with DESI's bounds on w0 and wa. "Never accelerated" means no member of
  the family with q ≥ 0 over 0 ≤ z ≤ 2.33 fits. Δχ² is read as one degree of freedom.
- W2 at A = 1 sits close to its line (3.41 and 3.57 against 4).
- Parts A and C use no a0 and do not grade the framework. Part B says only that CFG684 and CFG689 carry a dependence on
  the age question; it does not say which amplitude is right.
- The web readings of the four papers are PROVISIONAL (summariser). No blind re-grade has been run.

## Note added 2026-11-14: the blind re-grade and the host-galaxy follow-up
- **AGB1R** (`closure_2026_11_13/AGB1R_blind_progenitor_age_bias/`), a second build written from `FROZEN_CRITERIA.md`
  alone, reaches the same frozen word in every case of Parts A and C, and every check passes there too. Part B was not
  re-graded. The sentence above, "No blind re-grade has been run", is superseded by this note.
- It found two small defects in this build; neither moves a word. (1) Part C takes supernova distances by linear
  interpolation on a 601-point CAMB grid, which shifts χ² by up to 0.005 (Δχ²_today at A = 0 on `full` is 27.38, not
  27.37). (2) The short-delay template T_W, reported only, is 3 to 7 × 10⁻⁵ mag high: on `full` the best A_W is 2.29 and
  Δχ² is 1.86 at A_W = 0, 1.50 at 0.23 and 0.59 at 1, where this file prints 2.28 and 1.84 / 1.49 / 0.58.
  The numbers above are left as first written.
- **AGB2** (`closure_2026_11_14/AGB2_host_mass_step_redshift/`) tests the same slope on Pantheon+ host galaxies and
  combines it with this lane's Part A profile. Its words are in its own README.

kappa = 1/2 FITTED; not theory closed.
