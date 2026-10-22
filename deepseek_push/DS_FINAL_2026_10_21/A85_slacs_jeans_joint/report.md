# A85 — JOINT SLACS JEANS + LENSING SOLVER

**Lane:** A85_slacs_jeans_joint · **Date:** 2026-10-22 · **Base:** `deepseek_push/DS_FINAL_2026_10_21`
**Script:** `a85_checks.py` — **32/32 PASS, exit 0** · **Output:** `a85.out` · **Data:** `a85_results.json`
**Mutations:** 8 (`newton_jeans`, `wrong_aperture_radius`, `corrupt_virial`, `shift_anisotropy`,
`invert_b_lens`, `tophat_psf`, `deproj_bad`, `beta_sign`), each **exit 1**, killing between 1 and 7
named checks (`MUTATE.md`).

**Read:** `A70_slacs_audit/report.md` + `a70_checks.py` (loader at the `recno` header, `M2D_from_g`,
the single shared `boost`, `dlnR_E/dlnB = 0.7775`, `dlnR_E/dlnκ = 0.1205`, `B = 1.1738` at
a₀ = 1.132×10⁻¹⁰, the +0.172 ± 0.060 shape residual); `A71_global_fit/report.md` (shared B,
per-galaxy Υ only in SPARC, B = 1.1916 ± 0.0364, T = 5.69).
**`A80_slacs_sersic` did not exist when this lane started** (checked at t = 0): n = 4 is the
baseline and the n-sensitivity curve is generated here.

---

## 0. Bottom line

1. **Route 1 works — and that is the lane's real result.** With each lens's boost `B_i` fixed by
   `R_E` alone and **no free normalisation anywhere**, the model's aperture dispersions come out
   **−2.33 per cent** low in the mean (`-0.0103` dex, `1.58` sigma on the SEM) with **13.29 per cent**
   per-lens scatter (`0.0542` dex). The lensing mass — stars plus the polarisation stress, no dark
   particle — reproduces the *dynamical* mass at the few-per-cent level. That is the sharpest test
   the "same g drives lensing and dynamics" claim has passed so far, and it passes it with zero
   fitted parameters.
2. **But the offset is degenerate with two unmeasured shape parameters.** The mean offset is zeroed
   by `n_0 = 4.74` (Sérsic index) or by `beta_0 = +0.223` (constant anisotropy). Both are inside
   their plausible ranges, neither is measured per lens, and they move the answer by ±4 per cent
   each. **Route 1 therefore cannot distinguish "n = 4 and the theory is 2.3 per cent low" from
   "n = 4.74 and the theory is exact".** The 13.29 per cent *scatter* is 2.12× the median e_sigma:
   that part is real astrophysical scatter, not a normalisation.
3. **Route 2 (shared B) gives B = 1.2269 ± 0.0043 (formal) ± 0.0106 (scaled by √(χ²/dof)).** That is
   **2.27 sigma** above the Treu+2010 SLACS dynamical calibration of 1.000 ± 0.0361 dex. Profiling
   beta to the edge of the prior (`beta = +0.250`) lowers it to B = 1.1852 → **1.89 sigma**. So the
   thermal a₀ is *not* excluded, but it sits between 1.9 and 2.3 sigma — worse than A70's 1.80 sigma,
   because **the thermal a₀ (8.6257e-11) is 0.7620 of A70's footing** and a lower a₀ demands more
   stellar mass: `B_i` rises from 1.1754 to 1.2209 (+3.87 per cent).
4. **The σ channel does NOT break the B–κ degeneracy in any useful way.** `dlnσ_ap/dlnκ = 0.0345`
   against `dlnσ_ap/dlnB = 0.4706`, a ratio of **0.0732** — *smaller* than the lensing ratio
   **0.1550**. The aperture dispersion is **more** B-dominated than lensing, not less: the two
   constraint directions lie **3.079 deg** apart in the (ln B, ln κ) plane. The 2×2 Fisher is
   non-singular (det = 1.4278e+05) but has condition number **746.4**, and σ(κ) only improves from
   **0.6292 to 0.2677** (factor **2.35**). A κ measured to ±0.27 does not compete with A71's
   0.0258 statistical error and does not confirm, kill or strengthen A71's Δχ² = 6.35.
5. **The exact likelihood prefers high κ, and that preference is not credible.** Profiling the shared
   B over κ ∈ [0.20, 1.10], χ² falls monotonically to the scan edge (best κ = 1.1000,
   a₀ = 2.059772e-10), improving by **−28.4** in Δχ² from the thermal point. But the σ channel has
   **χ²/dof = 8.13** and **17.8 per cent** RMS residuals against 0.0628 median fractional errors:
   the fit is buying its Δχ² by shaving the scatter of an already-bad fit. With both channels'
   errors scaled to χ²/dof = 1 the same move gives **Δχ² = 2.96**, i.e. below 3 sigma. **The
   (R_E + σ_ap) pair does not constrain κ.** The high-κ branch is nevertheless interesting: at
   κ = 1.1000 the shared B falls to 1.0920, which would *remove* the IMF tension — but it is a
   1.7 sigma preference built on an 8-dof-8 fit, not a measurement.

---

## 1. What was built, and the two routes kept separate

### 1.1 The solver (`a85_checks.py`, Tasks 1a–1c)

* **Stellar profile.** Sérsic V-band light, **deprojected numerically** by Abel inversion
  `rho(x) = (1/pi) ∫_x^∞ (−dΣ/dy) dy / sqrt(y²−x²)` on a 1600-point log grid with the
  `y = x cosh u` substitution (300-node Gauss–Legendre), `x = R/R_e`.
  Checked three ways: (i) total 3D mass = 2D mass to `6.28e-08`; (ii) the round trip
  `2∫rho r dr/sqrt(r²−R²) = Σ(R)` at six radii to `5.14e-10`; (iii) against A70's
  Prugniel–Simien `nu = n(3−p)` form: `0.054%` at R = R_e, `5.424%` at 0.02 R_e, and the
  resulting `B_i` (1.2983 vs 1.2961) and σ_ap (240.21 vs 240.86 km/s) differ by `0.27%` at most.
* **Lensing.** `M_2D(<R) = (R²/G)∫_0^acosh(rmax/R) g(R cosh u) du` with the **same** Langmuir law
  `g = (g_N + sqrt(g_N² + 4 a₀ g_N))/2`, `g_N = G M_*(<r)/r²`, `rmax = 10⁶ kpc`. The stellar
  normalisation is `M_*(<R_E) = B f_* M_E` (the catalogue's `Fs` column is the Salpeter mass
  fraction *inside* R_E, which is why the total mass carries a `1/frac2D(R_E/R_e)`).
  Verified: Newtonian limit = the analytic projected mass to `5.91e-06`; rmax convergence
  `-2.38e-06`; every solved `B_i` satisfies the lens equation to `2.06e-08`.
* **Jeans.** `d(νσ_r²)/dr + (2β/r)νσ_r² = −ν g(r; B_i, κ)` solved by the standard integral
  `νσ_r² = r^{−2β}∫_r^∞ r'^{2β}ν g dr'` on 1100 log-spaced radii out to 45 R_e, then projected
  `σ_los²(R) = (2R/Σ)∫_0^acosh(rout/R) νσ_r² (1−β/cosh²u) cosh u du` and integrated over the fibre.
* **Aperture convention (stated once).** **R_ap = 1.5 arcsec** (radius of the 3.0 arcsec SDSS
  fibre) and a Gaussian PSF with **FWHM 1.4 arcsec** (σ = 0.5946 arcsec). σ_ap is the
  luminosity-weighted second moment of the LOS velocity distribution inside that fibre after
  convolution with that PSF — the quantity the SDSS pipeline's Gaussian fit returns. **No aperture
  correction is applied**, because the catalogue's `sigma` column *is* the fibre measurement and
  any correction to R_e/8 or R_e needs the very mass profile under test. The convolution is done
  exactly with the Marcum-Q form `W(R) = ncx2.cdf((R_ap/σ_psf)², 2, (R/σ_psf)²)`, verified against
  a direct 2D quadrature to `1.62e-14`, and the solver's own kernel matches the declared one to
  `0.00e+00`.
* **Validation anchors (all computed, all in `a85.out`):**
  * Jeans ODE residual `4.96e-04` (β = 0) / `5.12e-04` (β = 0.25).
  * **Virial identity** `σ_ap(R_ap→∞)² = (1/3)∫rho_* r g d³r / M_*` to `5.11e-04` at β = 0, +0.25
    and −0.15 (the β terms cancel exactly, so this tests the anisotropy implementation too).
  * **Independent brute-force reimplementation** (different deprojection grid, `l = sqrt(r²−R²)`
    quadrature, direct 2D Gaussian convolution, no Marcum-Q, no interpolation of σ_r²):
    `243.80` vs `244.23 km/s`, `-1.78e-03`.
  * Grid convergence `3.43e-05` / `2.65e-05`; β-monotonicity `237.26 → 246.42 km/s`.
  * **Reproduces A70**: `B_req = 1.1754` vs `1.1738` (0.13%), `dlnR/dlnB = 0.7847` vs `0.7775`,
    `dlnR/dlnκ = 0.1239` vs `0.1205`.

### 1.2 Route 1 vs Route 2 — the distinction the lane is built on

A70's model has **one** IMF boost per lens in the likelihood. Two different objects hide behind
the letter B and they must not be conflated:

| | definition | status | used for |
|---|---|---|---|
| **B_i(R_E, κ)** | the boost that makes lens i's lens equation reproduce `R_E,i` | **diagnostic**, absorbs per-galaxy photometric error (its 16–84 spread is a factor 1.56) | **Route 1** |
| **B** | the single shared IMF normalisation in the likelihood (A70's `boost`, A71's 1.1916) | **physical parameter** | **Route 2** |

**Route 1** fixes `B_i` from `R_E` alone and then *predicts* σ_ap with no free normalisation. It
tests whether the theory's own lensing mass reproduces the dynamics.
**Route 2** fits the shared B to (R_E, σ_ap) simultaneously. A per-lens free `B_i` in Route 2 would
make the κ sweep vacuous by construction (χ² ≡ 0 for every κ), so it is not done.

---

## 2. Task 2 — Fisher matrix and the degeneracy

At the sample median (median-parameter lens, `B_i = 1.2983`, β = 0, thermal a₀):

| derivative | value |
|---|---|
| `dln sigma_ap/dlnB` | **0.4706** |
| `dln sigma_ap/dlnkappa` | **0.0345** |
| ratio (σ channel) | **0.0732** |
| lensing ratio `0.1205/0.7775` | **0.1550** |

Per-lens medians over the 70 lenses agree: `dln sigma/dlnB = 0.4720` (16–84 `0.461`–`0.477`),
`dln sigma/dlnkappa = 0.0330` (16–84 `0.028`–`0.044`), ratio `0.0699` (16–84 `0.058`–`0.095`).

**The σ constraint direction is not the lensing one — but it is closer to the B axis, not further
from it.** In the (ln B, ln κ) plane the lensing direction `(0.7865, 0.1003)` sits `7.27 deg` from
the ln B axis and the σ direction `(0.4706, 0.0345)` sits `4.19 deg` from it. The **angle between
the two constraints is 3.079 deg** (`sin = 0.0537`).

**2×2 Fisher** (70 lenses, A70's per-lens R_E budget 0.0446 dex + the actual e_sigma):

```
F = [[10235.6, 949.3], [949.3, 102.0]]      det = 1.4278e+05
eigenvalues 10323.7 / 13.8306               condition number 746.4
B-kappa correlation coefficient 0.9291
```

| | σ(κ) |
|---|---|
| R_E alone (B marginalised) | **0.6292** |
| σ_ap alone | **0.7318** |
| R_E + σ_ap | **0.2677** (improvement factor **2.35**) |

With the observed R_E scatter `0.0927` dex instead of the formal budget the numbers get worse, not
better: det = `3.9722e+04`, condition number `1235.6`, σ(κ) `1.3077 → 0.4188` (factor `3.123`).

**Verdict on the degeneracy: formally broken, practically not.** The determinant is non-zero and
σ(κ) improves by 2.35×, but the improvement starts from “unconstrained” (0.6292, i.e. wider than the
whole prior range) and lands at 0.2677 — still 10× A71's statistical error and 2× its systematic
one. The condition number 746.4 says the second eigen-direction carries 0.13 per cent of the
information of the first: the two “independent” constraints are 3.079 deg apart, so the κ direction
is measured by the *residual* of two nearly parallel lines.

---

## 3. Task 3a — Route 1 and Route 2 at the two κ anchors

κ convention: **a₀ = κ × 1.87252e-10 m s⁻²**, so κ_DE = 0.460659 ↔ a₀ = 8.625932e-11 and
κ = 1/2 ↔ a₀ = 9.362600e-11. (The task quotes 8.6257e-11 and 9.355e-11; the 0.08 per cent
difference between the two anchors' rounding is far below every quoted precision, and I anchor on
the theory value a₀(κ_DE) = 8.6257e-11.)

### Route 1 — no free normalisation

| a₀ | β | mean log₁₀(σ_pred/σ_obs) | scatter | χ²/N | median ratio |
|---|---|---|---|---|---|
| 8.625700e-11 | 0 | **−0.0103 ± 0.0065** dex | 0.0542 dex | 3.89 | 0.9733 |
| 8.625700e-11 | profiled (+0.2096) | −0.0007 dex | 0.0545 dex | 3.65 | — |
| 9.362600e-11 | 0 | −0.0112 ± 0.0065 dex | 0.0540 dex | 3.93 | 0.9708 |
| 9.362600e-11 | profiled (+0.2202) | −0.0010 dex | 0.0544 dex | 3.65 | — |

The model is **2.33 per cent low**, not 15 per cent: the lensing deficit at B = 1 is −14.76 per cent
in R_E, but the *dynamical* prediction at the same `B_i` is only 2.33 per cent low — **the lensing
mass does reproduce the dynamics**. What it does not do is reproduce them *per galaxy*: 13.29 per cent scatter against a
0.0628 median fractional error (2.12×), i.e. χ²/N = 3.89 with no free parameter. Changing κ from
0.460659 to 1/2 moves the mean by −0.0009 dex — the σ channel is nearly κ-blind.

### Route 2 — shared B

| a₀ | β | B | χ² (R_E + σ) | χ²/dof | log₁₀ B | Treu tension |
|---|---|---|---|---|---|---|
| 8.625700e-11 | 0 | **1.2269 (+0.0043/−0.0043 dex)** | 838.3 (277.2 + 561.1) | 6.03 | +0.0888 ± 0.0043 | **2.27 sigma** |
| 8.625700e-11 | profiled (+0.250) | 1.1852 | 821.3 (285.3 + 536.0) | 5.95 | +0.0738 | **1.89 sigma** |
| 9.362600e-11 | 0 | 1.2174 | 834.8 (276.9 + 557.9) | 6.01 | +0.0854 | 2.19 sigma |
| 9.362600e-11 | profiled (+0.250) | 1.1758 | 816.4 (284.1 + 532.3) | 5.92 | +0.0703 | 1.80 sigma |

Tension denominator `0.0391` dex = √(0.0043² + 0.0361² + 0.0143²) (fit ⊕ Treu ⊕ lensing), as
specified. The formal error is optimistic because both channels over-fit (χ²/dof = 6.03); scaling
by √(χ²/dof) gives **±0.0106** dex, which changes the tension to 2.2 sigma — the tension is
dominated by Treu's own 0.0361 dex, so it is robust to the fit's error model.

**Reading.** At the thermal a₀ the SLACS lensing + aperture data require **1.2269 × Salpeter**,
2.27 sigma above the same survey's dynamical calibration. A70's 1.80 sigma was at a₀ = 1.132e-10;
the thermal point is lower (0.7620 of it) and therefore needs more stellar mass
(`B_i` 1.1754 → 1.2209, +3.87 per cent). Allowing beta to float to the prior edge recovers most of
A70's number (1.89 sigma). **The thermal point is allowed at ~2 sigma, not comfortably.**

---

## 4. Task 3b — does Route 1 reproduce the dispersions? What absorbs the offset, n or β?

Sérsic sweep at the thermal a₀, β = 0 (A80 absent, so this curve is generated here):

| n | median B_i(R_E) | mean log₁₀(σ_pred/σ_obs) | scatter | χ²/N | σ_ap (median lens) |
|---|---|---|---|---|---|
| 2.5 | 1.2168 | −0.0176 | 0.0539 | 4.69 | 233.55 km/s |
| 3.0 | 1.2184 | −0.0180 | 0.0535 | 4.52 | 234.42 km/s |
| **4.0** | **1.2209** | **−0.0103** | **0.0542** | **3.89** | **240.21 km/s** |
| 5.0 | 1.2227 | +0.0035 | 0.0555 | 3.50 | 249.10 km/s |
| 6.0 | 1.2242 | +0.0205 | 0.0568 | 4.09 | 259.90 km/s |

`dln sigma_ap / dln n = 0.1301` (at n = 4, with B_i held at its own R_E solution).
**`n_0 = 4.74` zeroes the mean offset.**

Anisotropy sweep at n = 4:

| β | mean offset | scatter | χ²/N |
|---|---|---|---|
| −0.15 | −0.0159 | 0.0541 | 4.26 |
| −0.10 | −0.0141 | 0.0541 | 4.13 |
| 0.00 | −0.0103 | 0.0542 | 3.89 |
| +0.10 | −0.0060 | 0.0543 | 3.72 |
| +0.20 | −0.0012 | 0.0545 | 3.65 |
| +0.25 | +0.0014 | 0.0546 | 3.66 |

**`beta_0 = +0.223` zeroes the mean offset** — inside the declared prior [−0.15, +0.25].

**How much does each absorb?** Both fully absorb the 2.33 per cent. The n range 2.5–6 spans
−0.0176 to +0.0205 dex and the β range spans −0.0159 to +0.0014 dex — each about as wide as the
offset itself, which is why neither can be called *the* explanation. Neither is measured for these
lenses (the catalogue has no n and no anisotropy), so **the 2.3 per cent offset is not evidence for
or against the theory** — it is a measurement of an `n`/β degeneracy at the same 2–4 per cent
level. What *is* measured is the 13.29 per cent scatter, which
neither n nor β removes (it is flat across both sweeps: 0.0535–0.0568 dex), and that scatter is
the real per-galaxy failure of the "lensing mass = dynamical mass" identity.

---

## 5. Task 3c — the κ sweep, with the shared B profiled

β = 0, n = 4, no Treu prior. 12 κ values from 0.20 to 1.10 (0.20–0.80 is the task's range; 0.95 and
1.10 are added to locate the turnover).

| κ | a₀ [m s⁻²] | κ_P3 | B_RE | B_sigma | B_joint | χ²_min | Δχ² | Δχ²(scaled) |
|---|---|---|---|---|---|---|---|---|
| 0.2000 | 3.745040e-11 | 0.1655 | 1.3414 | 1.2653 | 1.2955 | 871.02 | 61.13 | 7.54 |
| 0.2800 | 5.243056e-11 | 0.2317 | 1.3077 | 1.2498 | 1.2732 | 858.85 | 48.96 | 5.79 |
| 0.3600 | 6.741072e-11 | 0.2979 | 1.2765 | 1.2351 | 1.2520 | 848.72 | 38.82 | 4.37 |
| 0.4400 | 8.239088e-11 | 0.3641 | 1.2473 | 1.2210 | 1.2319 | 840.23 | 30.33 | 3.22 |
| **0.4607** | **8.625932e-11** | **0.3812** | **1.2401** | **1.2175** | **1.2269** | **838.28** | **28.38** | **2.96** |
| 0.5000 | 9.362600e-11 | 0.4138 | 1.2266 | 1.2108 | 1.2174 | 834.80 | 24.90 | 2.50 |
| 0.5800 | 1.086062e-10 | 0.4800 | 1.2002 | 1.1976 | 1.1987 | 828.63 | 18.73 | 1.72 |
| 0.6600 | 1.235863e-10 | 0.5462 | 1.1752 | 1.1849 | 1.1808 | 823.54 | 13.64 | 1.11 |
| 0.7400 | 1.385665e-10 | 0.6124 | 1.1514 | 1.1726 | 1.1634 | 819.40 | 9.50 | 0.65 |
| 0.8000 | 1.498016e-10 | 0.6620 | 1.1343 | 1.1636 | 1.1508 | 816.85 | 6.95 | 0.39 |
| 0.9500 | 1.778894e-10 | 0.7862 | 1.0939 | 1.1420 | 1.1206 | 812.28 | 2.38 | 0.02 |
| 1.1000 | 2.059772e-10 | 0.9103 | 1.0566 | 1.1215 | 1.0920 | 809.90 | 0.00 | 0.00 |

* **Best-fit κ = 1.1000** (a₀ = `2.059772e-10`, κ_P3 = 0.9103), at the scan edge; the Δχ² = 1
  crossing on the low side is at `1.037`, i.e. only a one-sided bound follows from this scan.
* **Δχ² over the whole scan = 61.13.** Compare A70's 0.26 (lensing only, B free) and A71's 6.35
  (per-lens scatter/shape, joint). The σ channel is *not* κ-blind — but see below.
* **Moving κ 0.4607 → 0.80**: the linearised Fisher predicts Δχ² = 1.6, the exact profile gives
  **−21.4**; **0.4607 → 1.10** gives **−28.4**. The linearisation is off by an order of magnitude because the
  model is a poor fit (see next point) and the profile is dominated by the scatter term, not by the
  mean.
* **The σ channel is in a bad-fit regime:** χ²/dof = `8.13` and RMS residuals `17.8 per cent` per
  lens against 0.0628 median fractional errors (`2.83`× e_sigma). The inflation needed to reach
  χ²/dof = 1 is `2.852`. With that inflation (and R_E at its observed 0.0927 dex) the same sweep
  gives **Δχ²(max) = 7.54** and **Δχ²(thermal → best) = 2.96** — under 3 sigma. The κ preference is
  therefore *not* a measurement: it is a small improvement in the RMS of a fit whose RMS is already
  3× the errors.
* **Does (R_E + σ_ap) constrain κ on its own? No.** The honest summary is the linearised one
  (σ(κ) = 0.2677, factor 2.35 over R_E alone) and it is already too weak; the exact profile's
  apparent 61.13 collapses to 7.54 once the errors are made honest.
* **What the high-κ branch would mean if it were real:** at κ = 1.1000 the shared B is 1.0920, i.e.
  essentially the Treu value. So the *only* way the σ channel relieves the IMF tension is by
  raising a₀ by a factor `2.3879` (`2.059772e-10 / 8.625700e-11`) — and it pays for it with a Δχ² that
  does not survive an honest error model. **Do not claim it.**

---

## 6. Checks and mutations

32 checks, all evaluating computed quantities (`a85.out`). The load-bearing ones:

| id | what it proves | measured |
|---|---|---|
| K1 | 3D mass integral = 2D mass | 0.99999992 vs 0.99999998 |
| K2 | Abel round trip | 5.14e-10 |
| K3 | exact vs P&S at R = R_e | 0.054% |
| K5 | reproduces A70's B_req | 1.1754 vs 1.1738 |
| K6 | reproduces A70's response exponents | 0.7847 / 0.1239 vs 0.7775 / 0.1205 |
| K7 | lens-equation residual at every B_i | 2.06e-08 |
| K8 | Newtonian limit of M2D_from_g | 5.91e-06 |
| K11 | Jeans ODE residual | 4.96e-04 |
| K12 | **virial identity**, β = 0, ± | 5.11e-04 |
| K12b | exact vs P&S deprojection → σ_ap | 0.27% |
| K13 | PSF kernel vs direct 2D quadrature | 1.62e-14; solver kernel 0.00e+00 |
| K14 | aperture is 1.5 arcsec, fibre flux = analytic | 0.3819 vs 0.3819 |
| K15 | **independent brute-force reimplementation** | 243.80 vs 244.23 km/s |
| K16 | grid convergence | 3.43e-05 |
| K18/K19 | Fisher non-singular; σ(κ) improves | det 1.4278e+05, 0.6292 → 0.2677 |
| K20/K21 | Route 1 statistics; β profiling | −0.0103 dex; β̂ +0.2096 |
| K22/K23/K24 | Route 2 minimum, interpolation, curvature | B = 1.2269, 7.93e-06, Δχ² > 20 |
| K25/K26 | n-monotonicity; β_0 inside the prior | 233.55→259.90 km/s; +0.223 |
| K27–K31 | κ profile, B ordering, scaled-Δχ² honesty | 61.13 → 7.54; 2.96 |

**Eight mutations, all exit 1:**

| mutation | what it changes | checks killed |
|---|---|---|
| `newton_jeans` | a₀ → 0 in the Jeans g only | K12, K15, K26 |
| `wrong_aperture_radius` | R_ap = 3.0 arcsec | K13, K15, K25, K26 |
| `corrupt_virial` | drops a cosh factor in the LOS integral | K12, K15, K26 |
| `shift_anisotropy` | β + 0.1 in the projection only | K12, K15, K26 |
| `invert_b_lens` | M_* uses 1/B | K5, K6, K28 |
| `tophat_psf` | no seeing convolution | K13, K16 |
| `deproj_bad` | 5 per cent density normalisation error | K1, K2, K3, K4, K5, K8, K12b |
| `beta_sign` | flips the sign of the β projection term | K12 |

Fifteen of the 32 checks are killed by at least one mutation. The other 17 are measurements of the
data rather than tests of the solver (Route-1 means, Route-2 fits, the Fisher determinant, the κ
profile); a mutation moves their values but not across a pass threshold, because those thresholds
are physics statements. `MUTATE.md` says so explicitly rather than claiming coverage it does not
have. No check was deleted for being unfalsifiable; the one candidate that *was* removed (a
“point-aperture limit” test) is documented in `MUTATE.md` — the Sérsic n = 4 profile drops by
`exp(−b (R/R_e)^{1/4})` so fast that the R → 0 limit probes R < 10⁻⁴ R_e, where no fixed grid
resolves the cusp. It was deleted rather than fudged.

---

## 7. Limits

1. **A80 was absent.** The n = 4 baseline and the n-curve (2.5–6) are this lane's own. A
   per-lens n from A80 would replace the ±2 per cent n-degeneracy with a measurement.
2. **The catalogue `sigma` is the SDSS fibre dispersion, not an aperture-corrected one.** That is
   deliberate (§1.1) but it means the comparison is to a 1.5 arcsec fibre, not to R_e/8 or R_e.
   An aperture-corrected σ would need the same mass model to correct with, so it would not be an
   independent test.
3. **β is one constant for the whole sample.** Real ETGs have radially varying β; the virial
   identity shows the constant-β implementation is self-consistent, not that β is constant.
4. **The 13.29 per cent σ scatter is not modelled.** It is the dominant χ² term and the reason the
   κ profile is untrustworthy. It is plausibly the per-galaxy IMF/`f_*` variation that `B_i`
   absorbs in Route 1 and a shared B cannot absorb in Route 2.
5. **R_E has no error column.** The Fisher uses A70's 0.0446 dex budget as fiducial and 0.0927 dex
   (the observed scatter) as the robustness variant; the conclusions do not change sign between
   them, only the strength.
6. **The 2.3 per cent Route-1 offset is at the level of the model systematics** (n, β, the fibre
   convention, the P&S-vs-exact deprojection at 0.27 per cent). It should not be read as a
   detection of anything.

---

## VERDICT

**The σ channel does not break the B–κ degeneracy, and the lane's value is elsewhere.**

Route 1 — `B_i` fixed by `R_E`, **no free normalisation** — predicts the SDSS aperture dispersions
**2.33 per cent low** in the mean (−0.0103 dex, 1.58 sigma) with **13.29 per cent** per-lens scatter.
The lensing mass of the polarisation-stress theory therefore *is* the dynamical mass at the few-per-cent
level, which is the sharpest zero-parameter confirmation the "no dark particle" claim has had. But the
offset is fully absorbed by `n_0 = 4.74` or by `beta_0 = +0.223`, neither of which is measured, so it
is not evidence either way.

Route 2 gives **B = 1.2269 ± 0.0043 (formal) ± 0.0106 (scaled)**, i.e. **2.27 sigma** above
Treu+2010's 1.000 ± 0.0361 dex; profiling β to the prior edge gives 1.1852 and **1.89 sigma**. The
thermal a₀ is allowed at ~2 sigma, less comfortably than A70's 1.80 sigma, because it is 0.7620 of
A70's footing and needs `B_i` = 1.2209 instead of 1.1754 (+3.87 per cent).

The degeneracy survives: `dlnσ_ap/dlnκ = 0.0345` vs `dlnσ_ap/dlnB = 0.4706`, ratio **0.0732**,
*smaller* than the lensing **0.1550**. The constraints are **3.079 deg** apart, the 2×2 Fisher has
condition number **746.4**, and σ(κ) improves only **0.6292 → 0.2677** (factor **2.35**) — from
“unconstrained” to “±0.27”, which is 10× A71's statistical error. The exact likelihood prefers
κ = 1.1000 with Δχ² = **−28.4** from the thermal point, but the σ channel has χ²/dof = **8.13** and
**17.8 per cent** RMS residuals, and with honest errors the same preference is **Δχ² = 2.96** —
below 3 sigma. **The (R_E + σ_ap) pair confirms nothing, kills nothing, and does not strengthen
A71's Δχ² = 6.35.** The one thing it does say, robustly, is that the *mean* dynamical mass agrees
with the lensing mass to 2.3 per cent — which is a consistency statement about the theory, not a
measurement of a₀.
