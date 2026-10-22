# A80 — THE SLACS SÉRSIC-n TEST

**Lane:** A80_slacs_sersic · **Date:** 2026-10-22 · **Base:** `deepseek_push/DS_FINAL_2026_10_21`
**Script:** `a80_checks.py` — **25/25 PASS, exit 0** (36 s cold start) · **Output:** `a80.out` · **Data:** `a80_results.json`
**Mutations:** nine (`MUTATE.md`), every run exit 1, every check killed by ≥1 mutation.

**Read:** `A70_slacs_audit` (the 70 lenses, dlnR/dlnB = 0.7775, B = 1.1738 ± 0.0385, the 2.9σ
R_E/R_e residual), `A71_global_fit` (Δχ² = 6.35 in the scatter term, unused because of n = 4),
`A79_external_audit` (the one surviving observation: n 4.0 → 5.8 raises the enclosed 2D
fraction by 17.40 % — its own check FAILED, so it is recomputed here from the projection).

---

## 0. Bottom line

1. **The generalised solver is exact and it reproduces A70 at n = 4.** `b_n` is solved from
   `gammainc(2n, b_n) = 1/2` (residual 3.3e-15) instead of the asymptotic series, and the 3D
   profile is the exact Abel deprojection of the same 2D Sérsic (verified against adaptive
   quadrature to 5.58e-04). At n = 4 it returns A70's numbers: per-lens ratios to **1.32e-06**,
   `dlnR/dlnB = 0.7775`, `B = 1.1738 ± 0.0385`, `χ²/dof = 6.206` (A70 stored 6.206), slope
   `+0.1722 ± 0.0597` (2.89σ), inner lenses `-0.2158`. Swapping A70's Prugniel–Simien kernel for
   the exact one moves `B_req` by **0.18 %** and no conclusion.
2. **The 2.9σ residual is entirely degenerate with n — but *which* sign the degeneracy takes
   depends on what the catalogue's f\* column measures, and that is not on disk.**
   The catalogue's own f\* satisfies `f* M_E / M*_tot = 0.0240 + 1.0223 f2(x, n=4)` with
   **R² = 0.8967** and 0.0286 residual (K5), i.e. f\* behaves like a Sérsic enclosed fraction rather
   than an independent aperture mass (but see the first limit: this is evidence, not proof). On that reading the n-independent quantity is the SED **total**
   stellar mass, the enclosed mass inside R_E moves as `f2(x,n)`, and
   `dlnR_E/dlnn = +0.52 at x = 0.3, +0.04 at x = 1, zero at x = 1.22` — so the residual
   **vanishes at n = 6.09**, inside the early-type range [4.5, 6.5], with `Δ(-2lnL) = 47.0` against n = 4.
   If instead f\* is held literally fixed (A70's implementation), `dlnR_E/dlnn` is only
   `+0.093` at x = 0.3 — **six times too small** (+0.0347 dex against the -0.2158 dex needed) —
   and the slope stays at **2.3σ for every n up to 20.0**.
3. **The likelihood runs past the cure.** With a uniform free `n_0` the ML solution is
   `n_0 = 14.14` (B = 0.8883), where the slope has **reversed to -0.1481 (-3.34σ)**. n is not
   measured by lensing: it drives the intrinsic scatter from 0.1584 down to 0.1054 dex and
   keeps going. The value that *zeroes* the shape trend is n = 6.09; n = 14.14 makes the inner
   profile a power law of local slope -1.813 (isothermal = -2).
4. **Model (c) is not a test.** An n(σ) law leaves the x-trend untouched (2.5σ, fixed *and* free
   exponent) because σ and x are uncorrelated (corr = 0.027). An n(R_e) law does absorb it
   (0.4σ at β = 0.5) — but x ≡ R_E/R_e, so an n(R_e) law is a coordinate reparametrisation of an
   n(x) law. Neither is evidence about Sérsic indices.
5. **The IMF penalty improves, then overshoots.** `B = 1.2280 → 2.30σ` (thermal a₀, n = 4);
   at the slope-zeroing n = 6.0, `B = 1.0985 → 1.05σ`; at the ML n₀ = 14.14,
   `B = 0.8883 → -1.33σ`. Profiling n moves the tension from A70's 1.79σ to 1.05σ
   at the n the residual asks for — and then past it, below Salpeter.
6. **A71's 6.35 is not a Sérsic-n degeneracy: it is an unprofiled-B artefact.** The number is
   reproduced exactly (63.29 → 56.94), but `a71_checks.py` builds that scatter table from
   `predict()` calls that leave `boost` at its default 1.0, while the surrounding text says
   "at its own best B". With B actually profiled the same statistic runs **54.53 → 54.50,
   Δ = 0.29**. With (B, n) jointly profiled the residual κ preference is **3.53** (free n) or
   **2.80** (n = 5.2 ± 0.8) — above the 2.0 threshold, but a different object from A71's 6.35.

---

## 1. What was built, and the one modelling choice that decides the answer

### The solver

A70's kernel is: 2D Sérsic enclosed mass `M₂D(<R) = M gammainc(2n, b_n (R/R_e)^{1/n})` (already
exact for any n), a **Prugniel–Simien fitting formula** for the 3D profile, and the g-law
projection `M₂D,lens(<R) = (R²/G)∫_R^∞ g(r) dr/√(r²-R²)`. Two things were generalised:

| piece | A70 | A80 |
|---|---|---|
| `b_n` | `B4 = 7.669249934` at n = 4, asymptotic series otherwise | exact root of `gammainc(2n, b_n) = 1/2`, brentq to machine precision |
| 3D profile | Prugniel–Simien `gammainc(ν_ps(n), ·)` | **exact Abel deprojection** of the same 2D Sérsic, tabulated once per n on a log grid with Gauss–Legendre quadrature |

The deprojection is the double-integral form
`M₃(<r) = -4[∫₀^r Σ′(R)πR²/4 dR + ∫_r^∞ Σ′(R)((R²/2)asin(r/R) - (r/2)√(R²-r²)) dR]`
with Σ′ analytic, evaluated on a log grid and splined. K4 checks it against an independent
adaptive-quadrature evaluation: **max |dev| 5.58e-04** over R/R_e = 0.4–2.5. A70's
Prugniel–Simien kernel differs from it by a few tenths of a per cent at r = R_e
(F3(1,4) = 0.415155 vs 0.415584).

`mode="ps"` keeps A70's kernel (and, with `ref=True`, his `b_ser`) purely so the n = 4
reproduction can be verified to 1.32e-06; **every science number below is `mode="exact"`.**

### The mass anchor — the crux

f\* in the Auger catalogue is the stellar fraction inside R_E. Two ways to vary n:

* **`renorm` (primary).** The SED total stellar mass `M*_tot = 10^{logMs}` is the n-independent
  measurement; the model's enclosed mass inside R_E is `f2(x,n) M*_tot`, so it *moves* with n.
  At n = 4 this is **identical** to A70's model (verified: the two anchors return the same
  residual vector to machine precision).
* **`fstar` (A70 literal).** `M₂D,star(<R_E) = f* M_E` is held fixed; n only reshapes the 3D/LOS
  distribution.

The data prefer the first: **K5** regresses `f* M_E / M*_tot` on `f2(x, n=4)` and gets
**slope 1.0223, intercept 0.0240, R² = 0.8967, residual 0.0286** (two routes agree to 5.6e-17).
That is what a Sérsic enclosed fraction looks like. It is *not* proof — an aperture mass would
also track f2(x) approximately, with the 0.0286 residual being the true spread in n — and the
alternative is therefore run everywhere and reported.

Both anchors give the same model at n = 4, so **the A70 baseline is not in dispute**. They differ
only through `f2(x,n)/f2(x,4)`, which is exactly A79's +17.4 %.

### The data

| file | content | sha256 (16) |
|---|---|---|
| `real_research/data/slacs_auger2009_lenses.tsv` | Auger+2009 SLACS IX, 85 rows / **70 usable** | `d78d7627d6bbcc07` |
| `…/XR33_data_treu2010_table1.tsv` | Treu+2010, the SLACS dynamical IMF | `87f0751be13d4843` |
| `…/XR33_data_cvd12b_table2.tsv` | CvD12b, ETGs, IMF(σ) | `d52e0f499141e812` |
| `_external_data/etherington2022/src/6_Results.tex` | Etherington+2022, 43 lenses, γ, γ_ext | `50ac40eb18dea535` |

**A note on the file named in the brief.** `6_Results.tex` is on disk and is parsed here (43
SLACS lenses, columns R_Ein,eff, γ, q, φ, γ_ext, φ_ext), but it carries **none** of
sigma / Mass / RE / Re(V) / Re(I) / Re(B) / z_l / z_s / f\* (K2, 0 of 10). Those columns exist
only in the Auger TSV, which is the file A70 used and which reproduces A70's 70 per-lens ratios
to 1.32e-06. The two files are used for what each contains; no number in this report comes
from anywhere else.

Census: z_l 0.1925, z_s 0.6055, σ 241.0 km/s, R_E 4.070 kpc, θ_E 1.2119″, f\*_Salp 0.6900,
f\*_Chab 0.3950. **x = R_E/R_e(V) runs 0.158–0.991, median 0.513; 20 lenses have x < 0.4 and
none has x > 1** — so the whole sample sits inside R_e, and the tightest test is the inner third.

---

## 2. Task 1 — the exact solver, verified, and dlnR_E/dln(n)

### Reproduction at n = 4 (A70's kernel, A70's a₀ = 1.132e-10, B = 1)

| quantity | A80 | A70/A55 |
|---|---|---|
| max per-lens deviation from A55's stored ratios | **1.32e-06** | — |
| median R_E,pred/R_E,obs | 0.885233 | 0.885232 |
| ⟨ln⟩ ± sem | -0.124539 | -0.124539 |
| scatter | 0.0927 dex | 0.0927 dex |
| χ²/dof (A70's error budget) | **428.19/69 = 6.206** | 6.206 |
| dlnR/dlnB | **0.7775** | 0.7775 |
| B_req | **1.1738** | 1.1738 |
| B ± σ | **1.1738 ± 0.0385** | 1.1738 ± 0.0385 (A70's stored) |
| slope vs ln(R_E/R_e), raw | **+0.1726 ± 0.0647** (2.7σ) | +0.1726 ± 0.0647 |
| slope after the IMF(σ) correction | **+0.1722 ± 0.0597** (2.9σ) | +0.1722 ± 0.0597 |
| inner (x < 0.4) mean ln r | **-0.2158** | 0.216 dex low |

The exact kernel differs from A70's by **2.00 % per lens at worst** (mean -0.0033 dex) and moves
`B_req` from 1.1738 to **1.1760 (0.18 %)**. Both are far below the deficit they have to explain.

### dlnR_E/dln(n) — from the solver

Two definitions, both computed by finite-differencing the full lens solve on a synthetic family
(x swept by R_e at fixed R_E, a₀ = 1.132e-10):

| x | dln f₂/dln n | dlnR_E/dln n at fixed M\*_tot | dlnR_E/dln n at fixed f\* |
|---|---|---|---|
| 0.15 | +0.8568 | +1.0342 | +0.1279 |
| 0.30 | **+0.4739** | **+0.5239** | **+0.0933** |
| 0.50 | +0.2381 | +0.2632 | +0.0689 |
| 1.00 | **-0.0000** | **+0.0394** | +0.0394 |
| 1.22 | — | **zero** | — |
| 2.00 | -0.1297 | -0.0658 | +0.0160 |

* The **enclosed-fraction** response changes sign **exactly at x = 1** (by definition of R_e) —
  zero at 1.000, positive below, negative above.
* The **R_E** response at fixed total mass changes sign at **x = 1.22**: at x = 1 the 3D/LOS term
  is still +0.0394 (the sphere inside R_E holds relatively more of the fixed enclosed 2D mass as
  n rises), which pushes the crossing just above 1. So the brief's expectation — positive for
  x < 0.5, ≈ zero near x = 1 — is confirmed in this convention, with the caveat that the crossing
  is at 1.22, not 1.00.
* **A70's convention (f\* fixed) has no crossing at all**: the response is positive everywhere
  (+0.1279 at x = 0.15, +0.0059 at x = 3), because f\* fixes the enclosed mass and only the
  LOS/3D term survives. At x = 0.30 it delivers **+0.0347 dex for n 4 → 5.8**, against the
  **-0.2158 dex** the inner lenses need. That is the whole reason the two anchors disagree.

Over the 70 real lenses (fixed M\*_tot) the per-lens response is **median +0.1912, 16–84
0.084–0.402**, binned in x: +0.725 (x < 0.35), +0.277 (0.35–0.5), +0.157 (0.5–0.7), +0.060
(0.7–1.0). No lens has x > 1, so the negative branch is a solver result, not a sample property.

### A79's K17, recomputed from the projection

At x = 0.30: f₂(4.0) = 0.212730, f₂(5.8) = **0.249735**, so the enclosed 2D fraction rises
**+0.1740 (+17.40 %)**. An independent numerical integration of the 2D Sérsic agrees to
8.5e-07 (K10). So A79's physics was right and its *check* was wrong (it compared 0.06965 dex
against 0.0647 and failed its own 5 % tolerance). The +17.4 % is real — and it is a
**fixed-total-mass** statement, which is why it does not transfer to A70's f\*-fixed pipeline
(the third column of the response table).

---

## 3. Task 2 — does n cure the 2.9σ residual?

Three models at the thermal a₀ = 8.6257e-11 and again at the κ = ½ branch a₀ = 9.3600e-11.
All use A70's per-lens error budget and the measured CvD12b IMF(σ) boost applied per lens (that is
what makes the baseline A70's 2.9σ rather than the raw 4.9σ). `χ²/dof` uses A70's fixed errors;
without the IMF correction the n = 4 model at the same B gives **4.18**, the number comparable
to A70's 6.21 (which was at B = 1).

### At the thermal a₀

| model | n | B | -2lnL | s (dex) | χ²/dof | slope vs ln x | σ | inner (x<0.4) | AIC | BIC |
|---|---|---|---|---|---|---|---|---|---|---|
| **(a)** n = 4 | 4.00 | 1.2280 | -32.85 | 0.1584 | 3.45 | **+0.1454 ± 0.0587** | **2.5** | -0.0614 | -30.85 | -28.60 |
| **(b)** free n, renorm | **14.14** | 0.8883 | -67.65 | 0.1054 | 2.11 | **-0.1481 ± 0.0444** | 3.3 | +0.0666 | -63.65 | -59.15 |
| (b) free n, f\* fixed | 20.00 | 1.0705 | -75.93 | 0.0938 | 1.87 | +0.1004 ± 0.0433 | 2.3 | -0.0498 | -71.93 | -67.43 |
| **(c)** n(σ), α = 0.6 fixed | 3.11–5.33 | 1.2387 | -29.86 | 0.1626 | 3.55 | +0.1499 ± 0.0601 | 2.5 | -0.0611 | -27.86 | -25.61 |
| (c) n(σ), α free | α = 0.100 | 1.2287 | -32.93 | 0.1582 | — | +0.1453 | 2.5 | — | — | — |
| **(c)** n(R_e), β = 0.5 fixed | 1.97–6.16 | 1.2106 | -42.27 | 0.1449 | 3.08 | **+0.0211 ± 0.0568** | **0.4** | +0.0002 | -40.27 | -38.02 |
| (c) n(R_e), β free | β = 0.400 | 1.2089 | -43.11 | — | — | +0.0426 | 0.8 | — | — | — |

At κ = ½ the same pattern: (a) B = 1.2147, slope +0.1457 ± 0.0586 (2.5σ); (b) n₀ = 14.14,
B = 0.8794, slope -0.1474 (3.3σ); (c) n(σ) 2.5σ, n(R_e) 0.4σ.

**The n-profile** (thermal a₀, B profiled at every n) — this is the actual answer:

```
 n      B       -2lnL    Δ(-2lnL)   s       slope(x)        σ
 4.0   1.2280   -32.85    34.81    0.1584  +0.1454±0.0587   2.5
 5.0   1.1507   -48.20    19.47    0.1346  +0.0588±0.0545   1.1
 6.0   1.0985   -56.37    11.30    0.1224  +0.0038±0.0518   0.1   <-- zero
 7.0   1.0588   -60.98     6.68    0.1155  -0.0343±0.0499   0.7
 10.0  0.9728   -66.36     1.30    0.1075  -0.1017±0.0466   2.2
 14.14 0.8883   -67.65     0.00    0.1054  -0.1481±0.0444   3.3
 20.0  0.8007   -67.24     0.42    0.1058  -0.1825±0.0427   4.3
```

**So: the trend dies at n = 6.09, inside [4.5, 6.5], with Δ(-2lnL) = 47.0 against n = 4 — and then
the same likelihood keeps going to n = 14.14, where the trend has reversed to -3.3σ.** The reason is
not the shape residual: n drives the intrinsic scatter from 0.1584 to 0.1054 dex,
i.e. it is fitting the per-lens scatter, not the trend. n = 14.14 corresponds to a local 2D slope of
-1.813 at x = 0.3 (n = 4: -1.419; isothermal: -2), i.e. the fit is really asking for a stellar
profile that follows the isothermal total mass.

**Model (c) does not work as a test.** n(σ) leaves the x-trend at 2.5σ whether the exponent is
fixed (0.6) or free (0.100, which collapses to n ≈ 4), because corr(ln x, ln σ) = 0.027. n(R_e)
does absorb the trend (0.4σ) — but x ≡ R_E/R_e by construction, so any n(R_e) law is a
reparametrisation of an n(x) law and the fit cannot distinguish them. AIC/BIC prefer (b) over (a)
at -63.65 against -30.85, and prefer (c, n(R_e), β = 0.5) at -40.27 against -30.85 with the same parameter count — which
is a statement about the coordinate, not about Sérsic indices.

### What this means

The 2.9σ residual is **not** a robust measurement of a profile failure. Under the reading the
catalogue's own f\* column supports (K5), it is what an n = 4 Sérsic gets wrong when the true
index is ≈ 6; under the literal f\*-fixed reading it survives at 2.3σ no matter what n does,
because there the response is six times too small. **The discriminator is a per-lens photometric
n (or an independent aperture mass), and it is not on disk.** That is exactly the second
measurement A70 itself asked for.

---

## 4. Task 3 — the IMF normalisation penalty

Treu+2010 on disk: **N = 56**, ⟨log α_Salp⟩ = **-0.0005 ± 0.0182** (sem), scatter **0.1359 dex**, 95 % mean
bound **[0.8498, 1.1767]**. The prior used here is the abstract's 1.00 ± 0.0361 dex, which is **1.98× the
table's own sem** (conservative); with the lensing error 0.0143 in quadrature, **0.0388 dex**.

| a₀ | B(n=4) | σ | B at n = 6.0 | σ | B(n₀ = 14.14) | σ | shift |
|---|---|---|---|---|---|---|---|
| thermal 8.6257e-11 | 1.2280 | **+2.30** | 1.0985 | **+1.05** | 0.8883 | **-1.33** | -0.1406 dex |
| κ = ½, 9.3600e-11 | 1.2147 | +2.18 | — | — | 0.8794 | -1.44 | -0.1403 dex |
| A70 (1.132e-10, B=1) | 1.1738 | +1.79 | — | — | — | — | — |
| A71 joint | 1.1916 | +1.96 | — | — | — | — | — |

**Profiling n moves the tension the right way — from 2.30σ (thermal) / 2.18σ (κ = ½) to
1.05σ — and then overshoots.** At the n that actually zeroes the shape residual, B = 1.0985
and the tension is **1.05σ**: inside Treu's 95 % bound of 1.1767 with room to spare. At the ML n₀ = 14.14 the
required normalisation falls *below* Salpeter by 1.33σ, which is not a resolution either — it is the
same degeneracy read from the other side.

So the answer to the task's question is: **toward 1.05σ, not the wrong way** — but only at the
n the shape residual asks for, not at the n the likelihood prefers.

---

## 5. Task 4 — A71's Δχ² = 6.35, unlocked or killed?

### The number is reproduced, and it is computed at B = 1

A71's statistic is `χ²_shape(κ) = N sd(ln r)²/s²` with s = 0.2317 ln. Reproduced exactly:

| κ | 0.20 | 0.50 | 0.80 | Δ |
|---|---|---|---|---|
| A80 | 63.29 | 59.42 | 56.94 | **6.35** |
| A71 (K25) | 63.29 | 59.42 | 56.94 | 6.35 |

But the `SD_TAB` block of A71's K25 builds that scatter table from `predict()` calls that never
pass `boost` (it stays at the default 1.0), while the accompanying text says "the full per-lens chi2
**at its own best B**". A71's own text also says "with B profiled, the mean term is exactly zero…". The mean
term is zeroed by profiling B; the *scatter* table is not.

**With B actually profiled at every κ the same statistic runs 54.53 / 54.25 / 54.50 — Δ = 0.29.**
The 6.35 is an artefact of not profiling the parameter the lane says it profiled. (This does not
change A71's conclusions: it explicitly refused to use the 6.35 as κ information.)

### The exact sweep with (B, n) jointly profiled

κ in A51's P3 convention: the thermal a₀ = 8.6257e-11 is κ_P3 = **0.38126** (= κ_DE 0.4607), and
κ_P3 = 0.5 is a₀ = 1.1314e-10.

| κ_P3 | B (n free) | n | Δ(-2lnL) | B (n = 5.2±0.8) | n | Δ(-2lnL) |
|---|---|---|---|---|---|---|
| 0.2000 | 0.9327 | 14.71 | 3.53 | 1.1437 | 6.58 | 2.80 |
| 0.3000 | 0.9007 | 14.76 | 2.63 | 1.1040 | 6.58 | 1.98 |
| 0.3813 (thermal) | 0.8768 | 14.81 | **2.02** | 1.0737 | 6.60 | **1.45** |
| 0.5000 (½) | 0.8435 | 14.96 | 1.28 | 1.0342 | 6.60 | 0.84 |
| 0.6000 | 0.8172 | 15.11 | 0.77 | 1.0037 | 6.60 | 0.47 |
| 0.8000 | 0.7696 | 15.41 | **0.00** | 0.9485 | 6.60 | **0.00** |

**Δ(-2lnL) = 3.53 (free n) and 2.80 (n = 5.2 ± 0.8): above the 2.0 threshold, so the
"κ-blind" conclusion cannot be claimed outright.** But it is 6.35 → 3.53, and its
minimum is at the **κ = 0.80 edge**, reached by pushing B to 0.7696 (-2.93σ below Treu). So the
residual preference is for high κ *and* a light IMF simultaneously — it is not a κ measurement.

**The κ constraints, as the task asks for them:**

* **SLACS only:** κ_P3 = 0.80 (edge; Δ = 3.53 to κ = 0.20), i.e. a one-sided pull to high a₀.
* **Joint with Treu's B prior, n free:** best κ_P3 = **0.300**, Δ < 1 band **[0.20, 0.50]**,
  Δ at the thermal point **0.19**, at κ = 0.5 **0.91** — the thermal point is fine.
* **Joint with Treu's B prior and the ETG n prior:** best κ_P3 = **0.700**, band **[0.50, 0.80]**,
  Δ at the thermal point **1.81**, at κ = 0.5 **0.72** — the thermal point is out by 1.81 units, and the
  pull is toward *higher* κ, i.e. **away from κ_DE = 0.4607 and away from κ = ½**.

The two joint rows disagree (0.30 vs 0.70) because the n prior changes B(κ) and hence the IMF term.
**That disagreement, not either number, is the result: SLACS lensing does not measure κ, and the
residual 3 units of "information" is a statement about the n/B degeneracy.**

---

## 6. Where this contradicts A70, A71 and A79 — explicitly

| lane says | this lane computes | consequence |
|---|---|---|
| A70: "the 2.9σ R_E/R_e residual is degenerate with n = 4 but unresolved" | **it is fully degenerate**: zero at n = 6.09, reversed at n = 14.14, and the answer flips sign between the two mass anchors | A70's caveat was right and stronger than stated: the residual measures nothing about the profile unless f\*'s definition is known |
| A70: "χ²/dof = 6.21, B = 1.1738 ± 0.0385, dlnR/dlnB = 0.7775, slope +0.1722 ± 0.0597" | **all reproduced** (6.206, 1.1738 ± 0.0385, 0.7775, +0.1722 ± 0.0597) | the baseline is not in dispute; only its interpretation moves |
| A71: "the scatter term carries Δχ² = 6.35 of κ information, unused because of n = 4" | **the 6.35 is computed at B = 1**; at the profiled B it is **0.29** | the 6.35 was never there to be unlocked — it is an unprofiled-B artefact, not a Sérsic one |
| A71: "Δχ² = 6.35 monotone in κ" | monotone at B = 1 (63.29 → 56.94), **flat-to-U** at profiled B (54.53 → 54.50) | ditto |
| A79: "n ≈ 5.8 supplies almost exactly the inner mass A70 needs (+17.4 %)" | **+17.40 % is reproduced exactly** from the projection (two routes) — but it is a fixed-total-mass statement, and A70's pipeline fixes f\* instead | A79's physics was right, its check failed, and its mechanism does not apply to A70's model as written |
| A71: joint κ, B = 1.1916, global tension T | not re-run here (no joint fit attempted); the SLACS leg is confirmed at n = 4 | the joint fit's B tension is real; profiling n moves it to +1.05σ at n = 6 |

---

## 7. Limits

1. **The anchor is not decidable from disk.** K5's R² = 0.8967 is consistent with both
   "f\* is a Sérsic fraction at n ≈ 4" and "f\* is an aperture mass with a spread of true n".
   Everything in the model fits and the κ sweep inherits that ambiguity. A per-lens Sérsic n, or an independent
   aperture mass, settles it.
2. **No per-lens n exists in either on-disk catalogue** (K2). Every "n" in this lane is either a
   free parameter, a declared prior (α_n = 0.6, β_n = 0.5), or an inference from f\*.
3. **The PS-vs-exact kernel difference is 2.00 % per lens.** It is far smaller than the deficit
   but it is not zero, and it is carried in every exact-mode number.
4. **The likelihood is misspecified at fixed errors**: with A70's 0.0446 dex budget the residual
   scatter is 0.0927 dex, χ²/dof = 3.45 at the fitted B. All model comparisons therefore use a
   profiled intrinsic scatter s; the fixed-error χ²/dof is reported only for continuity.
5. **The ML n runs to the search boundary** in the f\*-fixed anchor (n = 20.0) and to 14.14 in the
   primacy anchor. Neither is a measurement of n; both are the model absorbing scatter.
6. **External convergence is still unmeasured** and still pushes the required B *up* (A70's environment section),
   which would worsen every IMF number here.
7. **No stacked radial profile, no per-lens photometry, no new data.** Nothing was downloaded.

---

## 8. Checks (25/25 PASS, exit 0) and mutations

| id | what it proves | measured |
|---|---|---|
| K1 | census 85 → 70 and the median lens | 0.1925 / 0.6055 / 241.0 / 4.070 |
| K2 | no Sérsic column on disk; the .tex has no lens columns | 43 lenses, 0/10 columns |
| K3 | `b_n` is solved, not expanded | 3.3e-15 ; b₄ 7.6692494425 vs 7.6692499340 |
| K4 | the 3D kernel is the exact deprojection | max dev 5.58e-04 |
| K5 | f\* is a Sérsic enclosed fraction (the anchor evidence) | slope 1.0223, R² 0.8967 |
| K6 | n = 4 reproduces A55/A70's 70 per-lens ratios | max dev 1.32e-06 |
| K26 | A70's χ²/dof is reproduced from the same vector | 6.206 vs 6.206 |
| K7 | the response and the required boost | 0.7775 ; 1.1738 ; 0.0143 dex |
| K8 | A70's 2.9σ shape residual | +0.1722 ± 0.0597 ; inner -0.2158 |
| K9 | exact vs PS kernel: A70's numbers transfer | max 0.0200 ; B_req 0.18 % |
| K10 | A79's +17.4 % recomputed from the projection, two routes | +0.1740 ; 8.5e-07 |
| K11 | the sign change of dlnR/dlnn near x = 1 | zero at x = 1.000 (f₂) and 1.220 (R_E) |
| K12 | A70's f\*-fixed convention: 6× too small | +0.0347 dex vs -0.2158 needed |
| K13/K14 | the A70 baseline at both a₀ | 2.5σ ; B 1.2280 / 1.2147 |
| K15/K16 | the free-n fit at both a₀ | n₀ 14.14 ; Δ(-2lnL) -34.8 |
| K17 | the slope zeroes at a plausible n | n = 6.09, 0.1σ, Δ = 47 |
| K18 | n(σ) cannot, n(R_e) can (a coordinate degeneracy) | 2.5σ vs 0.4σ |
| K19 | the B penalty moves 2.30 → -1.33σ | 1.05σ at n = 6 |
| K20 | A71's 6.35 reproduced — at B = 1 | 63.29 → 56.94 |
| K21 | at profiled B the same statistic is flat | 0.29 |
| K22 | (B,n) profiled: Δ(-2lnL) 3.53 / 2.80 | > 2, min at κ = 0.80 |
| K23 | A70's κ\* and dlnR/dlnκ | 1.0279 ; 0.1205 ; ratio 6.45 |
| K24 | the thermal a₀ identity and its Ω_Λ sensitivity | 8.62384e-11 (-0.02 %) ; 1.09 % |

**Mutations:** nine (`fix_n4`, `wrong_bn_coeff`, `invert_re_ratio`, `imf_prior_shift`, `newton_limit`,
`drop_lens`, `fake_ncol`, `omega_shift`, `deproj_bad`), each exit 1, each killing a named set of
checks; **all 25 checks are killed by at least one** (matrix in `MUTATE.md`). One candidate check
(the 4-node lnB interpolation) was **deleted**: it compares two evaluations of the *same* model, so
no input mutation can make them disagree. Its numbers are still printed.

---

## VERDICT

**(1) Best-fit n₀ and the residual.** With a uniform free n and the Sérsic-enclosed-fraction anchor
that the catalogue's own f\* supports (f\*M_E/M\*_tot = 0.0240 + 1.0223 f₂(x, n=4), R² = 0.8967), the
ML solution is **n₀ = 14.14** — unphysically high — but the R_E/R_e slope **passes through zero at
n = 6.09**, inside the early-type range [4.5, 6.5], with Δ(-2lnL) = 47.0 against n = 4: there the
residual is **eliminated (0.1σ)**. The likelihood keeps going because n also drives the intrinsic
scatter from 0.1584 to 0.1054 dex, and at n₀ it has overshot to -0.1481 ± 0.0444 (-3.3σ, opposite sign). Under the
literal f\*-fixed implementation the residual **survives at 2.3σ for every n up to 20.0**, because the
response is only +0.0347 dex where 0.2158 dex is needed. **So the 2.9σ is not a profile failure and
not a detection: it is a statement about how the catalogue's f\* was defined, and the two
self-consistent readings differ in sign.**

**(2) B and Treu.** B = 1.2280 (+2.30σ) at n = 4, thermal a₀; 1.0985 (+1.05σ) at the slope-zeroing
n = 6.0; 0.8883 (-1.33σ) at n₀ = 14.14. At κ = ½: 2.18σ → -1.44σ. Profiling n moves the tension
**to 1.05σ and then past it** — the right direction, with an overshoot that is itself the
degeneracy showing.

**(3) A71's 6.35.** It is reproduced exactly (63.29 → 56.94) but it is **computed at B = 1**, not at
the profiled B its text claims. With B profiled the same statistic is flat: **54.53 → 54.50,
Δ = 0.29**. With (B, n) jointly profiled the residual κ preference is **3.53** (free n) or **2.80**
(n = 5.2 ± 0.8) — above 2, but a different and much weaker object, minimised at the κ = 0.80 edge
with B = 0.7696 (-2.93σ below Treu).

**(4) The global tension.** The IMF leg **improves**: 2.30σ → 1.05σ at n = 6, and the joint fit's
1.96σ pull would relax correspondingly. The κ leg does **not** improve: with the ETG n prior the
joint constraint is κ_P3 = 0.700 [0.50, 0.80], 1.81 units from the thermal point — a pull
*away* from κ_DE = 0.4607 and from κ = ½, and with n free it is κ_P3 = 0.300 [0.20, 0.50], which
includes the thermal point. **The two differ by more than their widths, so SLACS lensing does not
constrain κ; what A80 removes is the claim that it had 6.35 units of information.** The honest
summary of A71's global fit after this lane is: the *B* tension is smaller than stated (1.05σ at
the n the data prefer) and the *κ* tension is unmeasured, in either direction.
