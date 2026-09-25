# S01 — THE RUNNING-a0 SYNTHESIS

**Phi(x) = (g_obs² − g_bar²)/(a0 g_bar)** at **x = g_bar/a0**, a0 = 9.3619e-11 m/s²
(the committed framework footing). On the pointwise RAR identity
g_obs² = g_bar² + a0_eff g_bar, Phi = a0_eff/a0: **Phi(x) IS the running-a0
function**, and the deep-regime a0_eff/a0 measurements of O01/O03/N05 are band
means of Phi at the band's median x. This lane computes Phi per ring on SPARC,
per dwarf (O01), per MIGHTEE ring, and per MW annulus (O03), and tests
UNIVERSALITY at fixed x.

Real data only, in-repo. Script `S01_running_a0.py` → `S01_running_a0.out`,
`S01_results.json`. No git commit. SEs everywhere.

---

## 0. Pre-registered verdict rule (stated BEFORE any Phi statistics)

**COLLAPSE** of a universal running-a0 law Phi(x) is declared iff **both**:

- **C1**: in ≥ 2/3 of the overlapping bin–survey comparisons,
  |Phi_survey − Phi_SPARC_bin| < 3 × combined SE,
  combined SE = sqrt(SE_survey² + SE_SPARC_bin²), SE_SPARC_bin from the
  galaxy-clustered bootstrap; **and**
- **C2**: the shared power-law exponent p of fit (a) on SPARC+dwarfs has
  |p|/SE_p > 5 (Phi genuinely RUNS with x; a flat Phi cannot be a
  "running-a0 law" at all).

Comparison inventory (fixed by geometry, not by the numbers): every in-window
survey point (log10 x ∈ [−1.5, +0.3]) whose x lies inside a SPARC bin holding
≥ 5 rings from ≥ 2 galaxies. Inventory: O01 primary (x = 0.109), O01 deep tail
(x = 0.074), MIGHTEE deep (x = 0.034), MW annuli 6 of 7 (the 5–8 kpc annulus at
log10 x = +0.324 lies OUT of the window by design and is reported separately).
If C1 and C2 hold → *The Running-a0 Law IS the new synthesis* (MIGHTEE
sign-mirror and G208 staircase are x-sampling). If C1 fails (offsets > 3 SE in
the majority of comparisons) → *the sign-mirror is a GENUINE SYSTEMATICS
DIVIDE*, registered — the same conclusion N05's arbitration program would
reach, now data-side.

---

## 1. Per-survey conversions (named explicitly)

| Survey | Phi conversion | x conversion | SE |
|---|---|---|---|
| **SPARC** (3389 rings / 175 galaxies, corpus v7) | per-ring Phi = (g_obs² − g_bar²)/(a0 g_bar) with the L06/G071 conventions exactly: v_b² = sign(Vgas)Vgas² + m2l(Vdisk²+Vbul²), m2l = m2l_disk (fallback 0.5), g_bar = v_b²·1e6/R, g_obs = (Vobs·1e3)²/R, R = Rad·KPC | x = g_bar/a0 per ring | galaxy-clustered bootstrap, B = 2000, seed 20260923+31 |
| **O01 dwarfs** (G114 LT dwarfs) | Phi = a0_eff/a0 = (V_obs/v_pred)⁴, the deep-limit estimator (V_obs⁴ = G M_b a0_eff), 4·mean(log10 V_obs/v_pred), cluster bootstrap over galaxies, B = 10000 (O01_results.json, registered) | x = band **median gN/a0** from G114_combined_sample.csv: primary (gN<0.2, N=16) → x = 0.109; deep tail (gN<0.1, N=7) → x = 0.074 | registered 0.1625 / 0.1186 |
| **MW** (Eilers+2019 RC; O03 primary baryons) | Phi = a0_eff/a0 = geomean((g_obs² − g_bar²)/g_bar)/a0, the O03 **full-line** estimator, per annulus (O03_results.json r_dependence.annuli_primary) | x = gbar_over_a0 per annulus (annulus median g_bar/a0) | O03 bootstrap SE (B = 10000, V_obs perturbed by the table's asymmetric errors) |
| **MIGHTEE** (80 rings, digitized CSV, G099-validated 0.036 dex) | deep point Phi = a0_eff/a0 = 1 + Delta/(a0 E[g_bar]) on the deep cut g_bar < 0.2 a0, N = 72 (N05_results.json, registered 2.164) — an x-weighted band mean of ring Phi; per-ring Phi also computed here for all 80 rings | x = median g_bar/a0 of the 72 deep rings = **0.0343** (from the CSV) | colour-group-clustered SE converted to a0eff/a0 units: 0.160 (ring-level 0.177) |

CSV deep band-mean cross-check: mean of the per-ring Phi on the N = 72 deep
rings = 2.39 ± 0.17 (ring-level) — consistent with N05's registered 2.164
(difference = estimator weighting, as stated).

---

## 2. SPARC Phi(x) per bin (log10 x ∈ [−1.5, +0.3], 0.15-dex bins)

2711 of 3389 SPARC rings lie in the window. Per-bin **mean** of ring Phi (SE:
galaxy-clustered bootstrap, B = 2000), median given as skewness diagnostic.

| bin | log10 x range | x (med) | N | Ngal | Phi mean | SE | Phi median | SE(med) |
|---|---|---|---|---|---|---|---|---|
| 0 | −1.50..−1.35 | 0.039 | 54 | 27 | 0.93 | 0.26 | 0.45 | 0.13 |
| 1 | −1.35..−1.20 | 0.054 | 107 | 39 | 0.83 | 0.17 | 0.51 | 0.10 |
| 2 | −1.20..−1.05 | 0.075 | 164 | 60 | 0.84 | 0.12 | 0.67 | 0.10 |
| 3 | −1.05..−0.90 | 0.109 | 301 | 97 | 0.76 | 0.07 | 0.53 | 0.05 |
| 4 | −0.90..−0.75 | 0.152 | 343 | 113 | 0.67 | 0.07 | 0.44 | 0.05 |
| 5 | −0.75..−0.60 | 0.210 | 318 | 132 | 0.72 | 0.06 | 0.50 | 0.04 |
| 6 | −0.60..−0.45 | 0.296 | 284 | 124 | 0.77 | 0.06 | 0.57 | 0.05 |
| 7 | −0.45..−0.30 | 0.413 | 258 | 113 | 0.83 | 0.07 | 0.62 | 0.05 |
| 8 | −0.30..−0.15 | 0.594 | 251 | 101 | 0.88 | 0.09 | 0.62 | 0.06 |
| 9 | −0.15..−0.00 | 0.836 | 251 | 90 | 1.14 | 0.15 | 0.71 | 0.07 |
| 10 | −0.00..+0.15 | 1.179 | 195 | 73 | 1.07 | 0.15 | 0.70 | 0.09 |
| 11 | +0.15..+0.30 | 1.670 | 185 | 54 | 0.96 | 0.17 | 0.59 | 0.09 |

Deep SPARC bins are **right-skewed** (mean ≈ 1.5–2× median): a minority of
rings with g_obs well above the baryonic prediction carries the mean. The
median battery ([r2] below) checks the verdict against this.

### Overlay survey points (inline with the SPARC table)

| survey | label | x | log10 x | Phi | SE |
|---|---|---|---|---|---|
| O01 | primary LT gN<0.2 (N=16) | 0.109 | −0.96 | 0.638 | 0.163 |
| O01 | deep tail gN<0.1 (N=7) | 0.074 | −1.13 | 0.310 | 0.119 |
| MW | 22.5–25.5 kpc (N=3) | 0.263 | −0.58 | 0.797 | 0.240 |
| MW | 20.0–22.5 kpc (N=5) | 0.322 | −0.49 | 0.942 | 0.175 |
| MW | 17.0–20.0 kpc (N=6) | 0.414 | −0.38 | 1.218 | 0.061 |
| MW | 14.0–17.0 kpc (N=6) | 0.566 | −0.25 | 1.372 | 0.024 |
| MW | 11.0–14.0 kpc (N=6) | 0.811 | −0.09 | 1.473 | 0.026 |
| MW | 8.0–11.0 kpc (N=6) | 1.243 | +0.09 | 1.557 | 0.019 |
| MW | 5.0–8.0 kpc (N=6) | 2.110 | +0.32 | 1.691 | 0.050 | *(OUT of window; excluded from the test)* |
| MIGHTEE | deep g_bar<0.2a0 (N=72) | 0.034 | −1.46 | 2.164 | 0.160 |

The brief's headline probe (MW a0_eff/a0 = 0.80 at x ≈ 0.27) is the 22.5–25.5
kpc annulus (0.797 ± 0.240 at x = 0.263). MIGHTEE 2.16 sits at x = 0.034.

---

## 3. Universality test: survey-mean Phi per overlapping bin

| bin | x range | surveys (Phi ± SE) | chi2 (ndof=1) | SPARC-vs-other offset | z (combined SE) |
|---|---|---|---|---|---|
| 0 | −1.50..−1.35 | SPARC 0.93±0.26, **MIGHTEE 2.164±0.160** | 16.6 | +1.24 ± 0.30 | **+4.08** |
| 2 | −1.20..−1.05 | SPARC 0.84±0.12, **O01 dt 0.310±0.119** | 10.4 | −0.53 ± 0.17 | **−3.22** |
| 3 | −1.05..−0.90 | SPARC 0.76±0.07, O01 pr 0.638±0.163 | 0.5 | −0.12 ± 0.18 | −0.68 |
| 6 | −0.60..−0.45 | SPARC 0.77±0.06, MW 0.942±0.175, MW 0.797±0.240 | 0.9 (ndof=2) | +0.18 / +0.03 | +0.95 / +0.13 |
| 7 | −0.45..−0.30 | SPARC 0.83±0.07, MW 1.218±0.061 | 16.6 | +0.39 ± 0.10 | **+4.08** |
| 8 | −0.30..−0.15 | SPARC 0.88±0.09, MW 1.372±0.024 | 30.1 | +0.49 ± 0.09 | **+5.48** |
| 9 | −0.15..−0.00 | SPARC 1.14±0.15, MW 1.473±0.026 | 4.7 | +0.33 ± 0.15 | +2.16 |
| 10 | −0.00..+0.15 | SPARC 1.07±0.15, MW 1.557±0.019 | 10.3 | +0.49 ± 0.15 | **+3.21** |

**9 comparisons, 4 within 3 combined SE (44.4%).** Total chi2 = 90.1 on 9 dof.
Offsets > 3 SE in 5 of 9 comparisons (the majority).

Robustness legs:
- **[r1]** MW annulus SEs inflated by a +15% baryonic-model systematic in
  quadrature (O03's registered deep drop-points span 0.80/1.00/1.29 across the
  three modelings): MW comparisons within 3 SE go 3/6 — bins 8 (z = 5.4) and
  10 (z = 3.2) survive the inflation; the divide at the MW inner annuli is not
  a 15%-level model effect.
- **[r2]** SPARC bin **medians** + median-bootstrap SEs (deep bins are
  right-skewed): 4/9 within 3 SE; MIGHTEE-vs-SPARC deep goes to **z = +8.4**
  (median Phi 0.45 vs 2.16); MW inner bin offsets grow to +4.3…+7.1. The
  divide is robust to the mean/median choice.

**The fixed-x deep window (the decisive table):** at x ≈ 0.03–0.11 the three
surveys give **Phi = 0.31 (O01 deep tail), ~0.8–0.9 (SPARC bins 0–2), and 2.16
(MIGHTEE)** — a 7× spread at fixed x, spanning both signs around the canonical
line Phi = 1. No x-coordinate inside the data reconciles them; the SPARC+dwarf
curve would predict Phi(0.034) ≈ 0.6–0.9 against MIGHTEE's 2.16 at 4.1 SE
(8.4 SE median-battery).

---

## 4. Candidate laws (inverse-variance weighted LS in linear Phi; SPARC bins
+ the two O01 band points, N = 14)

| form | parameters (SE) | chi2 / dof |
|---|---|---|
| (a) Phi = c x^p | c = 0.957 ± 0.057, **p = +0.154 ± 0.039** (z_p = +3.92) | 18.9 / 12 = 1.58 |
| (b) Phi = 1 + α ln x | α = **+0.115 ± 0.031** (z_α = +3.64) | 19.7 / 12 = 1.64 |
| (c) Phi = (1+x)/(1+x/b) | b = 0.492 ± 0.043 (family implies Phi(1) = 0.66; imposing Phi(1)=1 forces b=1 → the constant Phi ≡ 1, degenerate) | 76.6 / 13 = 5.89 |
| (c2) Phi = c_b(1+x)/(1+x/b), Phi(1)=1 enforced | b = 3.39 ± 0.71 (deep Phi(0) = 0.65, large-x Phi → 2.20, unphysical outside the window) | 18.1 / 13 = 1.39 |

SPARC+dwarfs alone show a **mild positive running** (p = +0.154 ± 0.039,
α = +0.115 ± 0.031; deep Phi ≈ 0.6–0.9 rising toward Phi ≈ 1.1–1.5 at
x ≈ 1) — but the exponent is at **3.9 SE from zero, NOT > 5 SE**.

---

## 5. Verdict (pre-registered rule)

- **C1: 44.4% of overlapping comparisons within 3 combined SE — FAIL** (need ≥ 2/3).
- **C2: p/SE_p = +3.92 — FAIL** (need > 5).

**VERDICT: Phi(x) does NOT collapse across surveys at fixed x. The sign-mirror
is a GENUINE SYSTEMATICS DIVIDE (registered finding)** — the conclusion N05's
arbitration program would reach, now data-side. Registered content:

1. **The MIGHTEE sign-mirror is a fixed-x divide, not x-sampling**: at x ≈
   0.034 MIGHTEE gives Phi = 2.164 ± 0.160 while at the *same x* SPARC rings
   give 0.93 ± 0.26 (median 0.45) — z = +4.1 (+8.4 in the median battery) —
   and O01 dwarfs at x ≈ 0.07–0.11 give 0.31–0.64. Three surveys, three
   mutually inconsistent values, 7× spread, at x's that overlap within one
   bin width.
2. **The G208 staircase is not x-sampling either**: SPARC-deep (x ~ 0.11),
   O01 (x ~ 0.07–0.11) and MIGHTEE (x ~ 0.034) fail to align on any single
   Phi(x); the "staircase" (SPARC 0.69 < HI 1.08 < MIGHTEE 1.87 ×1e-10)
   reappears as the survey-level a0_eff axis *at overlapping x*, i.e. as
   systematic offsets between survey systematics, not as a smooth track of x.
3. **Where the divide closes**: the MW's two outermost annuli (x = 0.26–0.32,
   Phi = 0.80/0.94) agree with SPARC at the same x (+0.1…+0.9 SE) and with
   the SPARC-deep/O01 primary tension family; the MW divide appears only
   inward of ~17 kpc (Phi → 1.2–1.6 at x ≈ 0.4–1.2, z = +4…+5.5), i.e., in
   the region where the O03 baryonic model is least secured (bar/inner disc;
   still > 3 SE after a +15% model systematic). And O01's deep tail (Phi =
   0.31 ± 0.12) sits 3.2 SE *below* SPARC at the same x — the deep window is
   simultaneously over-Newtonian (MIGHTEE) and under-Newtonian (O01 tail)
   relative to SPARC.
4. Honest limits: the SPARC deep bins are right-skewed with large clustered
   SEs; survey estimators differ (unweighted ring mean vs x-weighted band
   mean vs geomean); the MW model systematics dominate the inner-annulus
   values. None of these caveats moves the registered conclusion: 5/9
   comparisons are > 3 SE at fixed x, and the > 5-SE-running condition (C2)
   also fails.

## 6. The fitted law (descriptive; NOT established as universal)

Phi(x) = **0.96 x^(+0.154 ± 0.039)** — the best of the three forms on
SPARC+dwarfs (chi2/dof = 1.58; log form 1.64; interpolant form 5.89; the
Phi(1)=1-renormalized interpolant fits 1.39 but is unphysical beyond the
window). Its **falsifier**: any survey with ≥ 3 rings in a single x-bin whose
mean Phi departs > 3 combined SE from 0.96 x^0.154 — **already fired by
MIGHTEE at x ≈ 0.034 (z = +4.1)** — or a flat fit with |p|/SE_p < 5 on the
pooled SPARC+dwarf sample (current z_p = 3.9). The law is registered as the
best internal description of the SPARC+dwarf ensemble; the cross-survey
reality is the systematics divide above.