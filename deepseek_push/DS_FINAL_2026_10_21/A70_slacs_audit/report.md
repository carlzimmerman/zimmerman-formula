# A70 — IS THE 4.9σ SLACS LENSING FAILURE REAL?

**Lane:** A70_slacs_audit · **Date:** 2026-10-22 · **Base:** `deepseek_push/DS_FINAL_2026_10_21`
**Script:** `a70_checks.py` (25/25 PASS, exit 0, 7 s) · **Output:** `a70.out` · **Data:** `a70_results.json`
**Mutations:** `MUTATE.md`, 12 runs, each exit 1, every check killed by ≥1 mutation.

**Read:** `A55_lensing_prediction/report.md` (the 4.9σ failure), `A51_kappa_measured/report.md`
(κ = 0.371 ± 0.119), `A65_stiffness_origin/report.md` (L\* = 24 pc fitted).
**Data audited (sha256, all read-only):**

| file | content | sha256 (16) |
|---|---|---|
| `real_research/data/slacs_auger2009_lenses.tsv` | Auger+2009 SLACS IX, 85 rows / 70 usable | `d78d7627d6bbcc07` |
| `…/XR33_data_treu2010_table1.tsv` | Treu+2010, 56 SLACS lenses, per-lens IMF mismatch | `87f0751be13d4843` |
| `…/XR33_data_cvd12b_table2.tsv` | Conroy & van Dokkum 2012b, 35 ETGs, spectroscopic M/L | `d52e0f499141e812` |
| `…/XR33_data_slacsX_auger2010_table1.tsv` | Auger+2010, 59 lenses, M_e2 and f_DM | `ba31a31145ae99fc` |
| `_external_data/etherington2022/src/6_Results.tex` | Etherington+2022, 43 SLACS lenses, γ and γ_ext | `50ac40eb18dea535` |

---

## 0. Bottom line

1. **A55's number is wrong.** The M/L that zeroes the SLACS residual is **1.174 × Salpeter**,
   not 1.283. A55 computed `1/median²`, which assumes M₂D ∝ R²; the model's actual response is
   `dlnR/dlnB = 0.7775`, and the response route reproduces the root-found boost to 10⁻⁴.
2. **With the right number, the IMF escape is allowed at 95% CL — by 0.25%.** The direct SLACS
   dynamical calibration (Treu+2010, the same lenses) gives `α_Salp = 1.00 ± 0.036` (stat ⊕ sys),
   i.e. 95% **[0.850, 1.177]**. 1.174 sits at the 95% boundary, 1.80σ from the mean. With A55's
   own 1.283 it would have been **outside at 3.0σ**. Their arithmetic error is the difference
   between "allowed" and "excluded".
3. **It is not a κ tension.** With Salpeter fixed, lensing prefers κ\* = 1.028 (6.2σ from A51's
   0.371) — but `dlnR/dlnκ = 0.1205`, and with the IMF free the profile likelihood is
   **Δχ² = 0.26 over κ ∈ [0.20, 0.80]**. Lensing measures the mass normalisation, not a₀.
4. **It is mostly an amplitude.** At fixed amplitude the model's total-density slope matches the
   imaging-only measurement: `γ_pred − γ_obs = +0.012 ± 0.039` on 43 lenses. One residual shape
   term survives: `R_E/R_e` at +0.172 ± 0.060 (2.9σ), i.e. lenses with R_E < 0.4 R_e are 0.216 dex
   low. That is degenerate with the assumed Sérsic n = 4, which is not in the catalogue.
5. **Verdict:** the 4.9σ is real as *"Salpeter + a₀ = 1.132×10⁻¹⁰ is 11.5% short"*, but it is a
   measurement of the IMF normalisation. Replacing the Salpeter prior with the measured SLACS
   calibration leaves **1.8σ**, not 4.9σ. The theory is not falsified; it is at the 95% edge of
   the same survey's dynamical IMF calibration.

---

## 1. Same data, same model — verified before anything is concluded

The 85-row VizieR table yields **70 usable lenses** (finite z_l, z_s, R_E, M_E, f\*_Salp, f\*_Chab,
R_E > 0), exactly A55's N. Re-running A55's model on the same file reproduces **all 70 per-lens
ratios to 2.2×10⁻¹⁶** and the headline to the last digit:

| quantity | this audit | A55 |
|---|---|---|
| median R_E,pred/R_E,obs | 0.8852 | 0.8852 |
| ⟨ln⟩ ± sem | −0.1245 ± 0.0255 | −0.1245 ± 0.0255 |
| significance | 4.88σ | 4.9σ |
| scatter | 0.0927 dex | 0.093 dex |
| Newton / Chabrier / canonical | 0.7536 / 0.5533 / 0.8664 | same |

So this is not a rival re-implementation. Every disagreement below is a disagreement with A55's
**inference**, not with its arithmetic — except the one arithmetic error in §3.1.

---

## 2. Task 1 — the data

### 2.1 The Einstein radii are model-derived, not measured

SLACS IX fits a **singular isothermal ellipsoid** to the lens-subtracted arcs:
*"the mass of the lensing galaxy for each system is modeled as an SIE profile … the source is
lensed by ray-tracing through the SIE mass model"*, and the paper itself warns *"these are not
perfect lens models (not all of the lens are isothermal, nor are the sources always ideally
described by Sersic profiles)"*. Only part of the grade-A sample was modelled in Paper IX; the rest
is inherited from Paper V. **R_E is therefore a parameter of an isothermal model, not a measured ring
radius.** That matters because the theory's own total-density slope at R_E is γ = 2.103 (K25),
i.e. also isothermal: the SIE assumption and the model's shape coincide at the radius the test uses,
so the amplitude test is not biased by the SIE choice — but it cannot be used to test isothermality.

### 2.2 The "~2%" R_E error is an assumption, not data

- The catalogue has **zero columns** carrying an uncertainty on R_E or M_E (K6). A55's
  `s_th = 0.02` is hard-coded.
- The independent check available on disk is Etherington+2022's power-law/PyAutoLens fit to the
  same 43 lenses. Its **formal** θ_E error is 0.75% (max 10%), but the **difference between the two
  pipelines** is median 1.2% with a **6.9% scatter** (|1−ratio| median 2.1%).
- So 2% is a fair single-pipeline statistical error and **3.5× smaller than the real
  inter-pipeline scatter**. A55's total per-lens budget (2% θ_E ⊕ propagated M\* ⊕ 5% shape) is
  0.0446 dex, which is larger than the 6.9% scatter, so the error model is conservative overall —
  but not for the reason stated.
- Control (K23): replacing 2% by the measured 6.9% lowers χ²/dof from **6.21 to 4.20**. The excess
  scatter survives; it is not an error-model artefact.

### 2.3 Redshifts and geometry

| quantity | median | 16–84 | min / max |
|---|---|---|---|
| z_lens | 0.1925 | 0.125–0.285 | 0.063–0.513 |
| z_source | 0.6055 | 0.470–0.807 | 0.197–1.300 |
| D_ls/D_s | 0.634 | 0.478–0.750 | 0.233–0.867 |
| Σ_cr | 8.79 kg m⁻² | 7.00–10.8 | — |

Every source is behind its lens; the minimum D_ls/D_s is 0.233, so no lens sits in a pathological
geometry. The tabulated M_E is reproduced from θ_E, z_l, z_s to **+0.0003 ± 0.0032 dex** (K3), so
the cosmology is not a source of error.

### 2.4 Selection

- **No σ cut.** σ spans 164–404 km/s, median 241; 43% above 250, 11% above 300, 3% above 350.
- The parent is the SDSS LRG spectroscopic sample with a background emission line. Auger+2009's
  own claim is that SLACS is *"representative of the overall population of massive early-type
  galaxies with M\* ≳ 10¹¹ M⊙"*.
- So the sample is biased **to massive ETGs relative to all galaxies**, but not to the most massive
  within that class. That is the population where the heavy-IMF claims are strongest (MASSIVE,
  σ > 250), which means the selection bias works **in favour of** the theory's IMF escape, not
  against it.

### 2.5 Environment: unmeasured convergence, measured shear

- The catalogue's companion flag (`f_MType`, "c") is **empty in every row** — the environment
  cannot be read from the file A55 used.
- Etherington+2022 supplies an external shear: median **γ_ext = 0.062**, 16–84 = 0.023–0.154,
  max 0.35; **33% above 0.1 and 7% above 0.2**. The sample is not "isolated".
- The leading O(γ_ext²) effect on θ_E is 0.19% (median), 2.0% at γ = 0.2, 6.2% for the single
  most-sheared lens. It cannot produce an 11.5% deficit, and it averages out.
- **External convergence is not measured anywhere on disk.** Its sign is unambiguous: an
  unsubtracted κ_ext makes the observed θ_E larger while the SED stellar mass is unchanged, so the
  deficit **deepens**. κ_ext = 0.02/0.05/0.10 would raise the required normalisation to
  1.186/1.204/1.237. This is the one environmental systematic that could move the answer, and it
  moves it against the theory.

### 2.6 LOS and projection: no double counting

- The 3D law identity `r²g/G = M_b(1+F)` holds at R_E to 4.4×10⁻¹⁶.
- A55's `g`-integral projection agrees with the analytic projected stellar mass to **0.2%**,
  so the projection is not double-counting the light.
- The `c_n = B(2n+1)/B(n+1)` slip correction is reproduced exactly
  (0.8346 / 0.7854 / 0.7628 / 0.7500 for n = 0.5/1/1.5/2), and its size is
  **δα/α = 1.8×10⁻⁶**, i.e. **1.6×10⁻⁵ of the 11.5% deficit**. It is not applied in A55's R_E
  pipeline at all (only quoted in A55's K19), which changes nothing.
- The one number the 3D language hides: the phantom's **projected** mass inside R_E is 24.3% of
  the stellar projected mass, **2.34× its 3D F(y) = 10.4%**, because ρ_ph ∝ r⁻² extends along the
  line of sight. So "the phantom is 10% of the mass" understates its lensing weight by a factor 2.3.

### 2.7 Numbers I could not verify (flagged, not used)

Per-lens σ(θ_E); external convergence κ_ext; per-lens Sérsic index (no column); source morphology /
ring completeness per lens; the parent SDSS σ distribution; the SIE fit quality per lens; the
intrinsic M\*/L scatter. None of these is on disk. Everything else quoted above is computed in
`a70.out`.

---

## 3. Task 2 — the IMF question (the load-bearing one)

### 3.1 A55's 1.28 is arithmetically wrong: the answer is 1.174

A55 takes the mass deficit as `2 ×` the log-radius deficit (`0.108 dex`) and converts it to
`M/L = 1.283`. That assumes M₂D ∝ R². The model does not: at fixed observed R_E the **measured**
mass deficit is **0.0598 dex (1.148)** and the radius deficit is 0.0529 dex (1.130) — a ratio of
1.13, not 2. Solving the actual lens equation for a single multiplicative boost gives

**B = 1.1738**, with `1/median = 1.1296` and `1/median² = 1.2761`.

Two independent routes agree: the response of R_E to a boost is `dlnR/dlnB = 0.7775`, and
`exp(0.1245/0.7775) = 1.1737`. The boost exceeds the fixed-R mass deficit because raising the
stellar mass lowers y = g_N/a₀, which lowers the phantom's share — the total mass rises
sub-linearly.

The data measure this boost to **σ(log B) = 0.0143 dex**, i.e. **B = 1.174 ± 0.039 (3.3%)**.
That is the sharpest statement in the lane: *70 SLACS lenses measure the IMF normalisation to 3%.*

**Consequence for A55's claim.** With 1.283 the required normalisation is 3.0σ above the SLACS
dynamical mean and **outside** its 95% interval. With the correct 1.174 it is 1.8σ above and
inside by 0.25%. A55's conclusion ("inside the observed IMF band") is right only after their own
number is corrected.

### 3.2 The independent measurements

| probe | sample | α_Salp | notes |
|---|---|---|---|
| **SLACS dynamical M/L** (Treu+2010, lensing+Jeans+NFW) | 56 SLACS lenses | **1.000 ± 0.036**, per-lens scatter **0.136 dex** | abstract: `⟨log α⟩ = 0.00 ± 0.03 ± 0.02`; the same lenses |
| **Spectroscopic IMF(σ)** (CvD12b, full spectral fitting) | 35 ETGs, σ = 96–385 | **0.939** at σ = 241; relation `log α_MW = 0.113 + 0.617 log(σ/200)`, rms **0.122 dex** | Salpeter = 1.55 in these units; 86th percentile of the sample |
| **MASSIVE XVI** (Re/8, σ > 250) | 41 ETGs | **1.187** (α_Kroupa 1.84, range 1.12–3.05) | most massive ETGs; central aperture |
| **MASSIVE XXI** (Re/4–Re/2) | 37 ETGs | **1.123** (α_Kroupa 1.74); Re/8: 1.394 | the aperture closest to SLACS R_E ≈ 0.51 R_e |
| **Leier+2016** (SLACS, non-parametric lens masses) | 18 lenses | ~1.0 | very bottom-heavy excluded; Salpeter needs ≳25% DM inside R_e |
| **Smith, Lucey & Collier 2018** (upper-limit lensing) | 1 lens at σ = 314 (+2 limits) | < 1 (one system) | counter-claim: a massive ETG with a light IMF |

### 3.3 The 95% CL range, and where 1.174 sits

Two defensible constructions, both computed:

- **Direct SLACS calibration** (Treu+2010, the same 56 lenses): `1.00 ± 0.036` →
  **95% [0.850, 1.177]** on the mean; the per-galaxy 95% range is **[0.45, 1.57]**.
  1.174 sits at the **67.9th percentile** of the per-galaxy distribution and **1.80σ** from the
  mean (1.93σ ignoring the lensing error).
- **Cross-method random effects** (DerSimonian–Laird over Treu, CvD12b, MASSIVE XVI, MASSIVE XXI;
  τ = 0.103 dex, Q = 23.9/3): mean **1.057 ± 0.055**, **95% [0.949, 1.166]**.
  1.174 is 2.0σ outside (1.70σ including the lensing error).

The two intervals disagree because the methods disagree: the dynamical calibration says 1.00, the
spectroscopic relation at σ = 241 says 0.94, the MASSIVE aperture-matched points say 1.12–1.19.
That method spread (τ = 0.103 dex) is the real uncertainty, and it is far larger than the 0.25%
margin by which 1.174 clears the direct 95% bound.

### 3.4 (a) allowed, (b) required, or (c) excluded?

- **(a) Allowed — at the 95% boundary.** Inside the direct SLACS 95% interval by 0.25%; inside the
  per-galaxy 95% range comfortably (68th percentile); at the mean of the MASSIVE aperture-matched
  measurement (1.123). Not comfortably allowed: the cross-method combination puts it 2σ outside,
  and any unsubtracted κ_ext pushes it further out.
- **(b) Not required.** The independent central values are 0.94–1.19, with the SLACS-specific
  dynamical value at **1.00**. Nothing in the data asks for 1.17; it is the value the *theory*
  needs, and it is 1.8σ above what the same lenses' dynamics give.
- **(c) Not excluded.** 2σ is not exclusion, and the two IMF methods disagree by more than the
  tension. The heavy-IMF literature (CvD12b's 86th percentile, MASSIVE's mean) contains 1.17
  without strain.

### 3.5 Does 1.174 overshoot the dynamical mass?

Auger+2010's `f_DM(<R_e/2)` with Salpeter masses has median **0.230** (mean 0.209; 8 of 59 lenses
negative). The theory with Salpeter stars + phantom gives **M_th/M_dyn = 0.817 → f_DM = 0.183**,
consistent with the measured 0.230 to 0.047. With the required 1.174× Salpeter it gives
**M_th/M_dyn = 0.948 → f_DM = 0.052** — still non-negative. So independent dynamics at R_e/2 does
not exclude the heavier normalisation; it leaves ~5% dark mass, which is allowed.

### 3.6 The answer in one sentence

**1.17× Salpeter is allowed at 95% CL, not required, and not excluded — but only just, and the
"just" is A55's arithmetic error: at their quoted 1.28 the answer would be "excluded at 95%"**.

---

## 4. Task 3 — the κ / a₀ tension

### 4.1 The scan

`R_E,pred/R_E,obs` (median over 70 lenses) as a function of κ, with a₀ = κ × 2.2627×10⁻¹⁰:

| κ | 0.252 | 0.3415 | 0.371 | 0.490 | 0.5265 | 0.60 | 0.80 | 1.00 | 1.20 |
|---|---|---|---|---|---|---|---|---|---|
| median ratio | 0.8276 | 0.8494 | 0.8564 | **0.8830** | **0.8908** | 0.9062 | 0.9469 | 0.9941 | 1.0306 |

Across A51's measured band [0.252, 0.490] the prediction runs **0.828 → 0.883**: the whole band is
short, by 11.7% at its top. Across the falsifier band [0.3415, 0.5265] it runs 0.849 → 0.891.

### 4.2 The κ that gives zero residual — with Salpeter fixed

**κ\* = 1.0279**, i.e. 110% above the top of A51's measured band. The fixed-Salpeter error from the full per-lens likelihood is **0.130**; from the
mean/SEM route, **0.106**. That puts κ\* **6.2σ** from A51's 0.371.

Taken alone, that looks like a decisive cross-channel tension. It is not, for one reason:

### 4.3 The theory is nearly blind to a₀

**dlnR_E/dlnκ = 0.1205.** A 10% change in κ moves R_E by 1.2%. The 11.5% radius deficit would need
a 110% change in κ — which is exactly what κ\* = 1.03 is. The data are not measuring a₀; they are
measuring the mass normalisation, and κ is a very inefficient way to supply mass.

With the IMF normalisation free, the profile likelihood over κ (B marginalised, flat prior) is:

```
κ      0.20  0.30  0.40  0.50  0.60  0.70  0.80
Δχ²    0.25  0.09  0.01  0.00  0.05  0.14  0.26
best B 1.310 1.270 1.228 1.189 1.152 1.118 1.087
```

**Δχ² = 0.26 over a factor 4 in κ.** κ is unconstrained; the best-fit B slides from 1.31 to 1.09
along the degeneracy. A51's whole band is inside the allowed region.

### 4.4 The answer

**There is no κ tension.** Lensing alone, with the IMF free, cannot distinguish κ = 0.2 from 0.8.
The κ\* = 1.03 result is the Salpeter prior reappearing in κ units. Any statement of the form
"lensing prefers a higher a₀" is mis-specified: the required change is in M\*/L, and
`dlnR/dlnκ` is 6.5× smaller than `dlnR/dlnB`.

---

## 5. Task 4 — amplitude or shape?

### 5.1 The amplitude is one number

A single multiplicative M/L zeroes the mean residual (B = 1.174) and leaves the per-lens scatter
unchanged. χ²/dof with A55's per-lens errors is **6.21**; the propagated error is 0.0446 dex against
an observed scatter of **0.0927 dex** (2.1×), so there is real per-lens astrophysical scatter that
no single normalisation can remove.

### 5.2 The shape at fixed amplitude is right

No stacked SLACS reduced-shear profile is on disk (A55 did not use one either). The shape test that
*is* available is Etherington+2022's imaging-only power-law slope γ at θ_E for 43 of the 70 lenses.
Normalising the A55 model to each lens's observed θ_E (amplitude removed by construction), the
model's local slope is

**γ_pred = 2.103 vs γ_obs = 2.080, Δ = +0.012 ± 0.039** (median +0.049, scatter 0.254, N = 43).

So at R_E the total-density shape is reproduced. This verifies A55's "amplitude, not shape" for
this observable — and it contradicts the positive slope offset reported by `CFG712`, which used a
different model normalisation; the discrepancy between those two lanes is itself unresolved and is
flagged here, not adjudicated.

### 5.3 But the residuals are not structureless

| regressor | slope of ln(R_pred/R_obs) | significance |
|---|---|---|
| ln σ | −0.392 ± 0.132 | 3.0σ |
| ln(R_E/R_e) | +0.173 ± 0.065 | 2.7σ |
| ln θ_E | −0.289 ± 0.120 | 2.4σ |
| log M_E | −0.325 ± 0.083 | 3.9σ |

Binned in σ: 0.919 (< 220), 0.928 (220–260), 0.882 (260–300), **0.779 (> 300)**. The theory fails
worst in the most massive lenses.

Two different explanations, and the data separate them:

- **The σ trend is the IMF.** Multiplying each lens by the independently measured CvD12b
  `α(σ)` relation (normalised at σ = 241) flattens the slope from **−0.392 ± 0.132** to
  **+0.116 ± 0.129** (0.9σ), while the mean offset barely moves (−0.1245 → −0.1160). So the
  mass dependence is exactly the IMF-σ trend, not a profile-shape error.
- **The R_E/R_e trend is not the IMF.** After the same correction it survives at
  **+0.172 ± 0.060 (2.9σ)**: lenses with R_E < 0.4 R_e are 0.216 dex low, those with
  R_E/R_e = 0.4–0.8 are 0.08–0.09 dex low. That is a genuine shape residual in the inner light
  profile, and it is degenerate with the assumed Sérsic n = 4 (the catalogue has no n). It is the
  one place where "amplitude, not shape" is not the whole story.

### 5.4 The answer

The failure is **an amplitude at R_E, absorbed by one number (the IMF normalisation), plus a 2.9σ
inner-profile shape residual at R_E < 0.4 R_e that a heavier IMF cannot fix** (it makes the profile
steeper, not shallower). The single physical quantity that absorbs the amplitude is M\*/L; it is
independently measured (Treu, CvD12b, MASSIVE) and its required value is 1.174 ± 0.039.

---

## 6. Where this verdict differs from A55 — explicitly

| A55 says | this audit computes | consequence |
|---|---|---|
| "M\*/L = 1.28 × Salpeter" | **1.174** (root-found; response route 1.1737) | 8% lower; moves the value from outside Treu's 95% CL to inside it by 0.25% |
| "the failure is 0.108 dex in mass" | **0.0598 dex at fixed R_E**; 0.0696 dex is the M/L that zeroes the fit | A55's 0.108 = 2× the radius deficit, an M ∝ R² assumption the model does not satisfy (`dlnR/dlnB = 0.78`) |
| "inside the observed IMF band for massive ellipticals" | allowed at the **95% boundary**, 1.80σ above the SLACS dynamical mean; 2σ outside the cross-method interval | true only in the per-galaxy sense; not true for the population mean at 95% in the cross-method combination |
| "the failure is in the amplitude, not the shape" | amplitude yes; shape at R_E yes (`Δγ = +0.012 ± 0.039`); **a 2.9σ R_E/R_e shape residual survives** | A55's statement holds at R_E but not at small R_E/R_e; the inner-profile residual is real and unmodelled |
| (no κ statement) | κ\* = 1.028 with Salpeter fixed, but **Δχ² = 0.26 with a free IMF** | the 4.9σ is not a footing statement; it cannot be read as "the theory wants a larger a₀" |
| "the theory passes lensing only with a fitted M/L — the same status as ΛCDM's NFW fit" | **still true** | this is the part of A55 that survives intact: the zero-parameter gate fails, and the fitted number is 1.17×Salpeter, at the edge of what the same survey's dynamics allow |

---

## 7. What single measurement would settle it

**A homogeneous, gravity-sensitive spectroscopic IMF determination for the 70 SLACS lenses
themselves** — Na I λ8190, Ca II λ8498/8542/8662, FeH Wing-Ford, full spectral fitting at
R_E/2–R_E — calibrated to **≤ 0.03 dex**. At that precision the 1.00-vs-1.17 gap (0.070 dex) is
a 2.3σ measurement; 3σ needs **0.023 dex**. (The current method spread is 0.06–0.10 dex, so this is
a calibration campaign, not a reanalysis.)

Why nothing else works:

- **Lensing cannot**: with the IMF free, Δχ²(κ) = 0.26 and the M/L–κ degeneracy is 6.5:1 (§4.3).
- **Dynamics alone cannot**: a Jeans M/L is degenerate with the dark component under test. Treu's
  1.00 is obtained *with* an NFW halo; replacing it with the weaker phantom is exactly what raises
  the requirement to 1.17.
- **More lenses cannot**: the error on B is already 3.3%; the limit is the method spread
  (τ = 0.103 dex), not N.
- **A better R_E error model cannot**: the excess scatter is astrophysical (0.093 dex against
  0.045 propagated), and the 6.9% inter-pipeline scatter is already in the budget.

The second measurement, if the first is unavailable: a homogeneous re-fit of all 70 lenses with
free Sérsic n and a common power-law slope (Etherington-style), which would test whether the 2.9σ
R_E/R_e residual is a real profile failure or the n = 4 assumption.

---

## 8. Checks (25/25 PASS, exit 0, 7 s) and mutations

| id | what it proves | measured |
|---|---|---|
| K1 | 85 rows → 70 usable; medians vs A55's stored values | 0.1925 / 0.6055 / 241 / 4.07 |
| K2 | θ_E from R_E and D_A(z_l) vs A55 | 1.2119″ vs 1.2119″ |
| K3 | M_E from geometry vs tabulated Mass | +0.0003 ± 0.0032 dex |
| K4 | arcsec→kpc conversion vs D_A·arcsec; R_E/R_e | 3.2018 vs 3.2019; 0.513 |
| K5 | Fs/Fc vs the SPS Salpeter/Chabrier mass ratio | 1.766 vs 1.778; f\*_Chab 0.395 |
| K6 | no R_E error column; inter-pipeline scatter > 2× the assumed 2% | 0 columns; 6.9% = 3.5× |
| K7 | all z_s > z_l; D_ls/D_s in range | min 0.233, median 0.634 |
| K8 | no Sérsic column; n=3/6 bracket vs A55 | 0.8768 / 0.8933 |
| K9 | external shear is non-zero but its median θ_E effect ≪ 11.5% | 0.062; 0.19% median |
| K10 | my 70 per-lens ratios vs A55's stored ones | 2.2×10⁻¹⁶ |
| K11 | headline median / ⟨ln⟩ / σ vs A55 | 0.8852 / −0.1245 / 4.88 |
| K12 | Newton / Chabrier / canonical vs A55 | 0.7536 / 0.5533 / 0.8664 |
| K13 | A55's 1.28 is not the required M/L | 1.1738 vs 1.2761 |
| K14 | response route vs root-found boost | 1.1737 vs 1.1738 |
| K15 | the prediction is 95% a restatement of f\* | R² = 0.9522 |
| K16 | fixed-Salpeter κ error, two routes | 0.130 / 0.106; 6.2σ |
| K17 | κ unconstrained with a free IMF | Δχ² = 0.26 over 0.2–0.8 |
| K18 | Treu+2010 reproduces its abstract; 95% mean range | 1.000 ± 0.036; [0.850, 1.177] |
| K19 | 1.17× vs the SLACS dynamical calibration | 1.80σ; inside 95% by 0.25% |
| K20 | CvD12b relation slope/rms and the required value | 0.617 / 0.122; 0.80σ; 86th pct |
| K21 | the two 95% intervals disagree about 1.17 | RE [0.949, 1.166]; SLACS [0.850, 1.177] |
| K22 | Auger+2010 f_DM at R_e/2 vs theory+Salpeter | 0.183 vs 0.230 |
| K23 | χ²/dof 6.21; propagated 0.045 vs observed 0.093 dex | 2.1× excess |
| K24 | the σ residual is the IMF-σ trend | −0.392 → +0.116 |
| K25 | shape at fixed amplitude | Δγ = +0.012 ± 0.039 |

**Mutations:** 12 (`imf`, `newton`, `arcsec`, `a0shift`, `treu`, `dropmassive`, `shuffle_re`,
`cosmo`, `zsrc`, `fsx`, `ethcopy`, `gextq`), each exit **1**, each breaking a named set of checks.
Every one of the 25 checks is killed by at least one mutation (matrix in `MUTATE.md`). Five candidate
checks were **deleted** because no input mutation can break them (algebraic identity, analytic
constant, physical band, two derived positions); their numbers are still printed. `MUTATE.md` says
which and why.

---

## 9. Limits

1. **No stacked SLACS reduced-shear profile is on disk.** The shape test at fixed amplitude uses
   Etherington+2022's global power-law γ, not a radial shear profile. A radial stacked profile
   (Gavazzi+2007-style) would test 1–10 R_E, which is where A55 itself says the phantom and NFW
   diverge; that test is not done here.
2. **External convergence is not measured.** Only shear is. κ_ext ≳ 0.02 would raise the required
   normalisation to ≥ 1.186, i.e. outside the direct 95% bound. That is the largest unquantified
   systematic in the lane, and it goes against the theory.
3. **The IMF conversion uses Salpeter = 1.55 Kroupa.** CvD's text says ≈ 1.6, MASSIVE says 1.55,
   SNELLS says 1.55. The 0.014 dex ambiguity is below every conclusion.
4. **Treu's α assumes an NFW halo.** That is why the theory's requirement is higher than his
   central value; the residual difference is the halo-model difference, not an IMF measurement.
5. **The Sérsic index is assumed.** n = 4 for every lens; the n = 3/6 bracket moves the median by
   0.017, but the R_E/R_e residual may be an n effect and cannot be resolved without per-lens n.
6. **The 70-lens sample is the massive-ETG population**, not all ETGs. The IMF range quoted is for
   that population.

---

## VERDICT

**The 4.9σ is real arithmetic on a real offset, but it is not a falsification of the theory — it is
an IMF-prior statement, and the sharpest number in the lane is that 70 SLACS lenses measure the IMF
normalisation to 3.3%.** A55's escape number is wrong: solving the actual lens equation gives
**M\*/L = 1.174 ± 0.039 × Salpeter**, not 1.283, because the model's response is
`dlnR/dlnB = 0.7775`, not the `M ∝ R²` assumed in `1/median²`; the mass deficit at fixed R_E is
0.0598 dex, not 0.108. The empirically allowed 95% CL range for the SLACS lens population is
**[0.850, 1.177] × Salpeter** from the direct dynamical calibration of the same 56 lenses
(1.00 ± 0.036, per-galaxy scatter 0.136 dex, per-galaxy 95% [0.45, 1.57]); a cross-method
random-effects combination with the CvD12b spectroscopic σ-relation and the MASSIVE
aperture-matched points gives [0.949, 1.166]. **1.17 is therefore (a) allowed at the 95% boundary —
by 0.25%, inside the direct interval and 2σ outside the cross-method one — (b) not required by
independent dynamics, whose SLACS central value is 1.00, and (c) not excluded (1.8–2.0σ).** The
lensing-only best-fit κ with Salpeter *fixed* is **κ\* = 1.028 (σ_κ = 0.106–0.130)**, outside A51's
[0.252, 0.490] at 6.2σ — but that number is the M/L deficit relabelled: `dlnR/dlnκ = 0.1205`, and
with the IMF free the profile likelihood is **Δχ² = 0.26 over κ ∈ [0.20, 0.80]**, so κ is not
measured and there is no physical κ tension. The failure is an amplitude at R_E (one number absorbs
it) plus a 2.9σ inner-profile shape residual at R_E < 0.4 R_e that a heavier IMF makes worse, and
the profile shape at R_E itself matches the imaging-only measurement (Δγ = +0.012 ± 0.039). **One
measurement settles it: a homogeneous gravity-sensitive spectroscopic IMF determination (Na I
8190 / Ca II triplet / FeH) for the 70 SLACS lenses at R_E/2–R_E, calibrated to ≤ 0.03 dex** —
lensing cannot do it (Δχ² = 0.26), and dynamics alone cannot, because it is degenerate with the
dark component under test.
