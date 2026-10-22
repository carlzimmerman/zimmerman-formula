# A41 — the full cluster profile shape: eight bins, one parameter, and a kink only a step reproduces

## Claim

**1. The eight-bin profile is measured, and one number fits it.** Stacking CFG687's 318 eRASS1 ×
KiDS clusters bin by bin (30-patch jackknife) gives the amplitude in law units
`A = D/P_law = 2.802, 2.270, 2.532, 2.095, 2.147, 1.727, 0.931, 1.056` at
`R = 0.181 … 2.488 Mpc`, i.e. the sourcing fraction

    u(R) = 0.294, 0.373, 0.333, 0.417, 0.412, 0.532, 1.089, 0.939
           ±0.125 ±0.107 ±0.050 ±0.065 ±0.044 ±0.055 ±0.209 ±0.106

(A29 reproduced to 4e-5). The theory's full-profile prediction — the law's phantom with
`u = u_in` for `r < r_sp` and `u = 1` outside, `r_sp = 0.83 r200m = 1.3674 r200c = 1.4138 Mpc`,
**one** free parameter — fits all eight bins at **χ²/dof = 9.96/7 = 1.42** with
**u_in = 0.4371 ± 0.0288**. Replacing the single `r_sp` by each cluster's own `r_sp ∝ M^(1/3)`
(zero new parameters) gives u_in = 0.4057 ± 0.0279 at χ²/dof = 1.19; the two agree at 0.8σ.
Nothing else is adjusted: the phantom's shape is CFG687's own, the baryon profile is its own.

**2. Both rivals fail, and the full profile is harder on them than the band ratio was.**

| model | u | χ² | dof | χ²/dof | Δχ² vs step | σ |
|---|---|---|---|---|---|---|
| **step, u_in free, u=1 outside** | 0.437 ± 0.029 | 9.96 | 7 | **1.42** | — | — |
| u = 1 everywhere (cold = the law's phantom) | 1.000 | 82.9 | 8 | 10.4 | **73.0** | **8.5** |
| u = 0.4716 everywhere (A21's MID value) | 0.472 | 49.0 | 8 | 6.13 | **39.1** | **6.3** |
| u = 0.488 everywhere (the cosmic-share normalisation) | 0.488 | 45.7 | 8 | 5.71 | 35.7 | 6.0 |
| best constant u (fitted) | 0.566 | 39.9 | 7 | 5.70 | 29.9 | 5.5 |

`u = 1` is excluded at 8.5σ — the same verdict as A18's 7.7σ band test, slightly stronger because
all eight bins are used. The constant-u readings are excluded for a reason the band ratio could not
see: they fit the inner six bins and **over-predict the two outer ones by 6.9σ and 8.7σ**. Even the
best single constant (u = 0.566, not 0.472) is rejected at 5.5σ with the *same number of
parameters* as the step. **u is not a number; it is a function with a feature.**

**3. The feature is a kink, and it is amplitude-free.** The log-slope of the amplitude
`dlnA/dlnR` between 1.18 and 1.71 Mpc is **−1.650 ± 0.445**, i.e. **3.7σ from zero**; the step model
predicts −1.935 (0.6σ away), while `u = 1` and `u = 0.472` predict **0.000** and **+0.033** and
miss by 3.7σ and 3.8σ. On the seven slopes alone, with no amplitude information at all,
χ²/dof = **0.79** (step) against **2.62** (u=1) and **2.75** (u=0.472) — Δχ² = 12.8 and 13.8, i.e.
3.6σ/3.7σ from shape alone. The curvature statistic
`C = lnA(1.71) − 2lnA(1.18) + lnA(0.81) = −0.400 ± 0.244` is non-zero at 1.6σ; the step predicts
−0.739 (1.4σ), both smooth readings predict 0.000 exactly. **A rescaling cannot buy this: a
constant multiplier cancels identically in `dlnA/dlnR` (K6).**

**4. But the step is not a spherical mass step, and that is the lane's real result.** Realising the
step in 3D as `ρ_cold = ρ_ph/u` inside `r_sp` (the shape-preserving reading of A18's λ_req) forces
**≈1.3e14 M_☉ of extra enclosed cold mass inside r_sp — 0.8-1.0 M200c —** and `ΔΣ = Σ̄(<R) − Σ(R)` then
gives `A = 1.60-1.74` from 0.18 to 1.71 Mpc and 1.47 at 2.49 Mpc, where the data give 0.93-1.06.
That model is rejected at **Δχ² = 27.1, i.e. 5.2σ**, against the projected step. So `u(R)` is a statement about the **radial
shape of the cold sector**, not about a mass shell at the splashback radius. The data have a
caustic (dlnΔΣ/dlnR = −2.04 between 1.18 and 1.71 Mpc) and the law's phantom does not
(−0.39 in the same interval, −0.1 to −0.4 everywhere).

**5. And the profile alone does not single out the law.** A smooth NFW cold sector fits the same
eight bins at χ²/dof = **0.85** (c = 2.5, M = 1.37e14 M_☉) — 2.00 at c = 4.5. What the eight bins
*establish* is that **the law's own phantom shape is wrong** (u = 1 out at 8.5σ) and that **the
correction is not a constant in radius** (out at 5.5σ); they do not establish that the correction
has a step rather than a different smooth shape. The step is the minimal modification, not the
unique one.

## Derivation

Units `c = 1`, `G = 6.674e-11`, `a0 = 9.360324825e-11 m/s²` (canonical footing, never pooled),
`H0 = 67.4 km/s/Mpc`, `Ω_m = 0.315`, `Ω_Λ = 0.685`, `Δ = 200`, `c_NFW = 4.5`,
`r_sp = 0.83 (±0.06) r200m`, `M_☉ = 1.989e30`, `Mpc = 3.0857e22 m`,
`f_gas,500 = M_gas,500/M500 = 0.11`, `R_cosmic = (1−f_b)/f_b = 5.364327`.

**1. The three conventions, stated once.** Write `P_N` for the baryons-only ΔΣ (`a0 = 0`), `P_l` for
the full law (`a0` on, phantom included) and `D` for the measurement. Then

    u ≡ (P_l − P_N)/(D − P_N) = 1/λ,     D = P_N + (P_l − P_N)/u,     A ≡ D/P_l.        (1)

`u` is the fraction of the *required* cold excess that the law's phantom supplies; `λ = 1/u` is the
factor by which the phantom must be amplified. Exact in sympy (K6). Three normalisations hide in
this one symbol and must not be mixed:

- `u = 1` ⇔ cold = exactly the law's phantom at its own amplitude ⇔ `A_MID = 1.000` (A18's
  "cold = the law's phantom", excluded).
- `u = 0.488` ⇔ cold = `M_c = 5.3643 M_b` with the phantom's shape, i.e. `λ_cosmic = 2.049`
  (A18 §8). Note `0.488 = R_tot/R_cosmic = 2.6179/5.3643` is exactly A21's ceiling `f_ret ≤ 1`.
- A21's `u_MID = 0.4716 ± 0.0362` is `1/λ_req = 1/2.1207`, i.e. the *measured* amplification; it is
  3% below `λ_cosmic` because `R_req = 5.552` is 3% above 5.364.
  Recomputing the cosmic share for *this* stack (M200c = 1.490e14, c = 4.5, `M_b(<r_v) = 2.56e13`)
  gives `R_tot = 2.894` and `u_CS = 0.540`, 10% above A18's anchor; CFG687's own baryon budget
  (`M_ph(<r_sp)/M_b(3 Mpc) = 2.765`) gives 0.515. The three routes span **0.488 / 0.515 / 0.540**,
  i.e. `u_CS = 0.514 ± 0.05`, and that spread is the normalisation's own systematic.

**2. The data.** CFG687's `cfg687_percluster.npz`: `D`, `E`, `P_L`, `P_N`, `mg`, `z`, `ra`, `R500`
for 318 clusters (median z = 0.2337, median M_gas,500 = 1.1608e13, median R500 = 0.7845 Mpc →
M500 = 1.055e14 → M200c = 1.490e14 → r200c = 1.0340 Mpc, r_sp = 1.4138 Mpc). The model is CFG687's
own `law()`: cored power-law baryons (`β = 2/3`, `r_c = 0.15 R500`, +20% non-gas, truncated at
3 Mpc), `g = g_N ν_mono(g_N/a0)`, exact spherical ΔΣ projection. K7 reproduces the stored `P_L` and
`P_N` to 2e-15. Grid `logspace(0.15, 3.0, 9)`, weights `1/E²`, 30 RA-ordered patches.

| j | R_in | R_out | R_c | R_c/r200c | ΔΣ | σ | P_law | P_N | A | σ_A | u | σ_u |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0.1500 | 0.2181 | 0.1809 | 0.175 | 92.05 | 37.18 | 32.85 | 8.25 | 2.802 | 1.192 | 0.294 | 0.125 |
| 1 | 0.2181 | 0.3172 | 0.2630 | 0.254 | 71.52 | 18.35 | 31.51 | 7.70 | 2.270 | 0.607 | 0.373 | 0.107 |
| 2 | 0.3172 | 0.4613 | 0.3825 | 0.370 | 77.03 | 10.41 | 30.43 | 7.15 | 2.532 | 0.357 | 0.333 | 0.050 |
| 3 | 0.4613 | 0.6708 | 0.5563 | 0.538 | 56.81 | 8.22 | 27.12 | 5.89 | 2.095 | 0.288 | 0.417 | 0.065 |
| 4 | 0.6708 | 0.9755 | 0.8089 | 0.782 | 51.56 | 5.08 | 24.01 | 4.74 | 2.147 | 0.207 | 0.412 | 0.044 |
| 5 | 0.9755 | 1.4186 | 1.1764 | 1.138 | 35.83 | 3.25 | 20.75 | 3.61 | 1.727 | 0.158 | 0.532 | 0.055 |
| 6 | 1.4186 | 2.0630 | 1.7107 | 1.655 | 16.66 | 2.63 | 17.90 | 2.73 | 0.931 | 0.146 | 1.089 | 0.209 |
| 7 | 2.0630 | 3.0000 | 2.4878 | 2.406 | 16.55 | 1.65 | 15.67 | 2.07 | 1.056 | 0.105 | 0.939 | 0.106 |

Edges in r200c: **0.145, 0.211, 0.307, 0.446, 0.649, 0.943, 1.372, 1.995, 2.901** (K4). The sixth
edge, 1.4186 Mpc, lands at 1.372 r200c — **0.4% above r_sp/r200c = 1.3674**. That is a coincidence
of CFG687's 8-bin grid, and a useful one: the predicted discontinuity falls inside the
MID/OUTER boundary bin, so the step is resolved by exactly one bin pair. The bands reproduce the
published `A_law = 2.5091 / 1.9102 / 1.0118`, `A_newton = 10.4352 / 10.1737 / 7.2620`,
`u = 0.3348 / 0.4716 / 0.9865` (K1, K3).

The covariance is close to diagonal: `max|ρ_ij| = 0.36`, condition number 622 (K5). All fits use the
full 8×8 jackknife covariance with eigenvalues clipped at 1e-2 of the largest; the diagonal is
quoted as a cross-check and agrees.

**3. The model and the one-parameter fit.** The model is linear in `v ≡ 1/u_in`:

    m_j(v) = P_N,j + v·Φ_j + Ψ_j ,   Φ_j = fraction of bin j's phantom *inside* r_sp,
                                     Ψ_j = the rest,     u = 1 for R > r_sp.                (2)

`v` is fitted by weighted least squares (no grid, no degeneracy), `u_in = 1/v`,
`σ_u = σ_v/v²`. Fixed `r_sp = 1.4138 Mpc`: **v = 2.2880 ± 0.1508, u_in = 0.4371 ± 0.0288,
χ² = 9.96 for 7 dof**. Residuals `(D−m)/σ`: `+0.74 +0.51 +1.60 +0.29 +0.54 −2.15 −0.47 +0.53`
(max 2.15σ in the 0.98-1.42 Mpc bin, where the model over-predicts because the step is at the bin's
upper edge). The model's own band amplitudes are `INNER 1.978 (record 2.509), MID 2.046 (1.910),
OUTER 1.000 (1.012)`: the one-parameter fit lands on MID to 7% and OUTER to 1.2%, and sits 1.7σ
*below* INNER — the same inner-gradient residual that shows up in the slope table of §5. The fit is
in A18/A21's normalisation (K1/K3), and it is the inner bins, not the outer ones, that it cannot
fully reach.

With each cluster's own `r_sp,i = 1.3674 r200c(M200,i)` (spread 16-84% = 0.94-1.90 Mpc):
**u_in = 0.4057 ± 0.0279, χ² = 8.32/7 = 1.19**, residuals
`+0.62 +0.28 +1.22 −0.12 +0.24 −1.20 −2.84 +0.36` (max 2.84σ at 1.71 Mpc, where the low-mass
clusters are still "inside"). The two variants bracket the data and agree at 0.8σ (K9). **The
single-`r_sp` fit is the task's model; the per-cluster one is the theory's actual prediction, and
it is not worse.**

**4. The rivals (Task 3).** Table in §Claim 2. Per-bin residuals make the failure mode explicit:

- `u = 1` everywhere: `+1.59 +2.18 +4.48 +3.61 +5.42 +4.64 −0.47 +0.53`. It is wrong *inside*;
  the two outer bins are, of course, perfect, because there the model *is* u=1.
- `u = 0.4716` everywhere: `+0.85 +0.73 +1.97 +0.72 +1.17 −1.27 −6.93 −8.68`. It fits the inner
  six bins and **over-predicts the outer two by 18.2 and 14.3 M_☉/pc²**, i.e. 6.9σ and 8.7σ. This
  is the new information in the full profile: the constant-u reading is destroyed not by the core
  but by the outskirts.
- `u = 0.488` (cosmic share, zero parameters): same failure, −6.5σ / −8.1σ.
- best constant (`u = 0.566`): −4.9σ / −5.8σ, Δχ² = 29.9 → 5.5σ.

The fitted `u_in = 0.4371 ± 0.0288` sits **0.75σ from A21's MID value 0.4716 ± 0.0362**: the full
profile does not move the inner amplitude, it fixes the outer one. Against the cosmic-share
prediction `u_CS = 0.514 ± 0.05` (three baryon-budget routes), the fit is **−1.3σ**: consistent,
and not a zero-parameter confirmation.

**5. The shape diagnostic (Task 4).** `dlnA/dlnR` per interval, measured and predicted:

| interval (Mpc) | measured | ±  | step (fixed r_sp) | step (per-cluster) | u=1 | u=0.472 |
|---|---|---|---|---|---|---|
| 0.18-0.26 | −0.562 | 1.267 | +0.011 | +0.012 | 0.000 | +0.011 |
| 0.26-0.38 | +0.291 | 0.751 | +0.016 | +0.010 | 0.000 | +0.015 |
| 0.38-0.56 | −0.506 | 0.548 | +0.031 | +0.020 | 0.000 | +0.029 |
| 0.56-0.81 | +0.066 | 0.449 | +0.034 | −0.042 | 0.000 | +0.032 |
| 0.81-1.18 | −0.582 | 0.341 | +0.039 | −0.242 | 0.000 | +0.036 |
| **1.18-1.71** | **−1.650** | **0.445** | **−1.935** | **−0.937** | 0.000 | +0.033 |
| 1.71-2.49 | +0.337 | 0.491 | −0.000 | −0.751 | 0.000 | +0.031 |

χ² over the seven slopes (diagonal): **5.50 (step), 9.77 (per-cluster), 18.34 (u=1), 19.27
(u=0.472)**; with the full slope covariance 14.98 vs 56.09. The kink is the whole story: 3.7σ from
zero, and only the step predicts it. The observed inner slopes average **−0.321 ± 0.228** (five
intervals, inverse-variance) against a predicted **+0.033** — a 1.4σ hint of an extra inward rise
that the flat-A prediction does not have (the same inner rise A29 flagged at 2.7σ, here 1.4σ as an
amplitude-free inverse-variance average). Curvature: `C = −0.400 ± 0.244` measured, step −0.739, both smooth readings
exactly 0.000; `Δs = s(1.18-1.71) − s(1.71-2.49) = −1.986 ± 0.872` measured, step −1.935.

The physical content of the table is the slope of the *data* against the slope of the *model*:

    dlnD/dlnR    = −0.67 +0.20 −0.81 −0.26 −0.97 −2.04 −0.02
    dlnP_l/dlnR  = −0.11 −0.09 −0.31 −0.32 −0.39 −0.39 −0.36

The law's phantom is a smooth power law with no feature anywhere; the data have a caustic at
1.2-1.7 Mpc (slope −2.04) and a flat 2-halo-like tail outside (−0.02). That is why `u(R)` steps.

**6. The step is not a spherical mass step (K19).** `ρ_cold = ρ_ph/u` with a 3D step at `r_sp`
(enclosed-mass-continuous, density-jumping) raises `M(<R)` inside `r_sp` and therefore
`Σ̄(<R)` at *all* radii: `ΔΣ = Σ̄ − Σ` cannot fall as fast as the data. Best 3D fit: `u_in = 0.557`,
χ² = 37.1/7 = 5.3, residuals `+1.1 +1.1 +2.7 +1.5 +2.3 −0.1 −5.3 −3.9`, `A(R) = 1.60 1.60 1.62
1.64 1.67 1.74 1.71 1.47` against a measured `2.80 2.27 2.53 2.09 2.15 1.73 0.93 1.06`. The extra
enclosed mass required is **1.22e14 M_☉ (0.82 M200c) for cluster 0 and 1.43e14 (0.96 M200c) for a
median-mass cluster**, and the model is rejected at
**Δχ² = 27.1 (5.2σ)** against the projected step. This is the quantitative death of A18's
shape-preserving `λ_req`, and it resolves an internal tension in A18: its P-A18 prose says the
unsourced share "falls natively and is more concentrated", but its §9 `λ_req` implements a
shape-preserving rescaling. The data take the prose, not the formula.

**7. The NFW rival, and what is actually established (K20).** Baryons + an NFW cold sector, c = 4.5,
one parameter: χ² = 14.0/7 = 2.00. With c free (two parameters): **χ² = 5.09/6 = 0.85** at
`M = 1.37e14 M_☉`, `c = 2.5`, residuals `−0.4 −1.2 −0.2 −0.7 +0.9 +0.7 −2.3 +1.1`. So a smooth
NFW fits the eight bins as well as the stepped law. The profile therefore does **not** prove a
step; it proves that (i) the law's phantom is excluded as the cold sector (`u = 1`, 8.5σ), (ii) the
required correction is not a constant in radius (5.5σ), (iii) the correction is confined to
`R < r_sp` at the resolution of the grid, and (iv) the correction cannot be a spherical
amplification of the phantom (5.2σ). Whether the cold sector is "phantom + concentrated extra" or
"NFW" is not decided by these eight numbers.

**8. The transition width is not measured (K21).** Smoothing the projected step over
`w = 0 … 0.22 dex` (0 … 0.72 Mpc) changes χ² by less than 1.4 (8.28 → 9.62) and u_in by less than
0.011. The eight bins localise the transition to **1.2-1.7 Mpc**; they do not measure its
sharpness. "Step" here means "a feature narrower than one CFG687 bin", not "a discontinuity".

## Status

- **Task 1 — NUMERICAL.** The stacked ΔΣ, `A(R) = D/P_law` and `u(R)` in all eight bins, with
  jackknife errors, are in the table of §2 (edges in Mpc and in r200c, K4). `u` reproduces A29 to
  4e-5 (K3); the six band amplitudes reproduce CFG687 to 3.5e-8 (K1); the model reproduces the
  stored arrays to 2e-15 (K7).
- **Task 2 — NUMERICAL / one parameter.** `u_in = 0.4371 ± 0.0288` at χ²/dof = 1.42 (fixed r_sp) or
  `0.4057 ± 0.0279` at 1.19 (per-cluster r_sp), with per-bin residuals. The cosmic-share
  normalisation (`M_c = 5.3643 M_b`, recomputed for this stack three ways) predicts
  `u_CS = 0.514 ± 0.05`: **−1.3σ**, consistent but not a confirmation.
- **Task 3 — DECIDED.** `u = 1` excluded at Δχ² = 73 (8.5σ); `u = 0.4716` at 39 (6.3σ);
  `u = 0.488` at 36 (6.0σ); the best constant (`u = 0.566`) at 30 (5.5σ). The full profile agrees
  with the band ratio on `u = 1` and is much stronger on "u is constant".
- **Task 4 — DECIDED (shape).** The kink `s(1.18-1.71) = −1.650 ± 0.445` is 3.7σ, reproduced by the
  step at 0.6σ and missed by both smooth readings at 3.7-3.8σ; amplitude-free shape
  χ²/dof = 0.79 (step) vs 2.62 / 2.75. Curvature `C = −0.400 ± 0.244` vs −0.739 (step) and 0.000
  (both smooth).
- **Two negative results that bound the claim — DECIDED.** The 3D realisation of the step is
  rejected at 5.2σ (it needs 0.8-1.0 M200c of extra enclosed mass and over-predicts 1.7-2.5 Mpc), and
  a smooth NFW cold sector fits the same bins at 0.85/dof.

## Checks

`a41_checks.py` — 22 checks, deterministic, stdlib + numpy/scipy/sympy, ~3 s, no network, reads
the CFG687 per-cluster npz, exit 0 iff all pass. `a41.out` is the captured stdout; four mutations
each break a check group and exit 1 (`MUTATE.md`).

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | the npz IS CFG687 (six band amplitudes) | 3.5e-8 rel | <1e-4 |
| K2 | the 8-bin ΔΣ with jackknife errors | max σ/D = 0.40; A(1.71)=0.931, A(2.49)=1.056 | σ/D<0.45, \|A−1\|<0.2 outside |
| K3 | u(R) reproduces A29's eight values | max Δu = 4.4e-5 | <2e-3 |
| K4 | bin edges in Mpc and r200c; r_sp in the 6th edge | edge 6 = 1.372 r200c vs r_sp 1.3674 | <1% |
| K5 | the jackknife covariance is near-diagonal | max\|ρ\|=0.36, cond 622 | <0.5, <1e4 |
| K6 | the algebra (1) and dln(kA)/dlnR = dlnA/dlnR | 0 (sympy) | <1e-25 |
| K7 | the model reimplementation is CFG687's `law()` | 2.2e-15 | <1e-10 |
| K8 | the one-parameter step fit | u_in = 0.4371±0.0288, χ²/dof = 1.42, max resid 2.15σ | χ²/dof<2, u_in∈(0.3,0.6) |
| K9 | per-cluster r_sp variant; the two agree | 0.4057±0.0279, 1.19/dof, 0.78σ apart | χ²/dof<2, <1.5σ |
| K10 | the cosmic-share normalisation | u_CS = 0.514 (routes 0.488/0.515/0.540); Z = −1.3 | \|Z\|<3 |
| K11 | rival (a) u = 1 everywhere | χ² = 82.9/8; Δχ² = 73 (8.5σ) | Δχ²>49 |
| K12 | rival (b) u = 0.4716 everywhere | χ² = 49.0/8; Δχ² = 39 (6.3σ) | Δχ²>16 |
| K13 | rival (c) u = 0.488 everywhere | χ² = 45.7/8; Δχ² = 36 (6.0σ) | Δχ²>16 |
| K14 | even the best constant u is rejected | u = 0.566; Δχ² = 30 (5.5σ) | Δχ²>20 |
| K15 | the ordering, and u_in vs A21's MID | 1.42 / 4.99 / 10.4 per dof; 0.75σ | ordered, <3σ |
| K16 | amplitude-free shape χ² | step 0.79 vs u=1 2.62 vs u=.472 2.75 | step<1.5, rivals>2 |
| K17 | THE KINK: s(1.18-1.71) | −1.650±0.445 (3.7σ); step −1.935 (0.6σ) | >2.5σ, step<2σ, rivals>2.5σ |
| K18 | the curvature at r_sp | C = −0.400±0.244; step −0.739; smooth 0.000 | >1.2σ, step<2.5σ |
| K19 | the 3D realisation is rejected | χ²/dof = 5.30; Δχ² = 27.1 (5.2σ); 0.82 M200c | Δχ²>15 |
| K20 | a smooth NFW also fits | 0.85/dof (c free), 2.00 (c=4.5) | <1.5 (reported) |
| K21 | the transition width is unconstrained | χ² range 8.28-9.62 over w = 0-0.22 dex | range<2 |
| K22 | the u-space estimator reproduces A29 | χ²(const) = 41.4 (A29: 41.5); u_in = 0.4116 | ±2, u_in∈(0.35,0.48) |

## What this does not do

1. **`u(R)` is projected, not deprojected.** The step is a feature of `u_proj(R)`; the 3D `u(r)` is
   bounded, not measured. K19 shows that the naive deprojection (a spherical density step) is
   excluded, which sharpens rather than settles A29's caveat 1.
2. **The step is not shown to be a step.** The width is unconstrained (K21) and a smooth NFW fits
   the same eight bins (K20). What is excluded is the law's phantom shape and any constant `u`.
3. **The significance is record-internal.** A 30-patch jackknife on 318 clusters of one survey and
   one shear catalogue; miscentring, photo-z systematics and the `M_gas → M500` conversion
   (`f_gas = 0.11`, whose catalogue-`R500` counterpart is 54% higher) are not in the error budget.
   An 8.5σ is not a survey-independent 8.5σ.
4. **`r_sp` carries inherited coefficients.** 0.83 ± 0.06 r200m (More+2015) × 1.6474 (NFW at
   c = 4.5), neither from the theory; with the three mass routes the prediction spans
   1.21-1.75 Mpc. The data localise the transition to 1.2-1.7 Mpc, so the *coincidence* is at the
   ~10% level, not the 0.4% level of the bin edge.
5. **The per-cluster `r_sp` spread over-predicts bin 6 by 2.8σ.** Either the mass dependence is
   weaker than `M^(1/3)` at fixed metric radius, or the catalogue's extreme mass tail
   (`r_sp` 0.22-3.32 Mpc, i.e. M200 from 6e11 to 2e15) is partly spurious. Not resolved here.
6. **The inner profile has a 1.4σ unexplained slope.** `A(R)` is predicted flat inside `r_sp`
   (+0.03); the data give −0.32 ± 0.23. A one-parameter step cannot describe a residual gradient.
7. **The cosmic-share comparison is normalisation-limited.** `u_CS` spans 0.488-0.540 across three
   baryon-budget routes, a ±5% systematic comparable to the fit's ±0.029; the R500-based M500 route
   (54% higher than M_gas/0.11) would shift it further. The amplitude-level A18 statement
   (`R_req = 5.55 ± 0.43` vs 5.364) is the more robust version.
8. **Spherical symmetry, one median mass for the stack, no 2-halo separation.** The outer excess is
   flat in ΔΣ (16.66 → 16.55 between 1.71 and 2.49 Mpc), which is also the signature of correlated
   large-scale structure; "u = 1 outside" and "unbound 2-halo material" both produce it.

## Next

1. **Deproject `u_proj(R) → u_3D(r)`** with a two-parameter model (amplitude + a scale radius for
   the concentrated component), which is the only way to turn "the extra cold mass is more
   concentrated than the phantom" into a number.
2. **A finer radial grid across 1.0-2.0 Mpc** (the CFG687 bins are 0.44 Mpc wide there). This is
   the measurement that would (a) measure the transition width, (b) separate `r_sp ∝ M^(1/3)` from
   a fixed radius, and (c) test whether the kink is at 1.367 r200c or at 1.42 Mpc (the data-driven
   caustic) — the two differ by 0.3%, far below the present resolution.
3. **The 8-bin profile in three mass terciles.** The self-similarity test `u = U(r/r_sp)` uses data
   already on disk, and A29's tercile ordering (u_OUTER = 1.90 / 1.04 / 0.68) is the sharpest
   existing hint.
4. **3-6 Mpc.** `u = 1` outside `r_sp` is currently tested only to 2.9 Mpc, where the 2-halo term
   dominates. A measured `A > 1` at 3-6 Mpc would say the law under-predicts there too, i.e. that
   `u = 1` is not the asymptotic value.

## Falsifier

The lane's claim is "the cold sector's projected profile has a feature at `r_sp`, and outside it the
law's phantom needs no rescaling". Three measurements kill it:

- **`A(R) = 1` inside.** `u = 1` in 0.15-0.5 r200c (0.16-0.52 Mpc, `σ_u ≤ 0.10`) would remove the
  step entirely; the present INNER band gives 0.335 ± 0.056, excluding it at 11.8σ.
- **`A(R) > 1` outside.** `u < 1` at 3-6 Mpc at >3σ, i.e. `A(4 Mpc) > 1.15`, would say the phantom
  is under-sourced everywhere and the step is an artefact of the 1.5-2.5 Mpc window.
- **No kink at `r_sp` in a finer grid.** If `dlnA/dlnR` between 1.0 and 2.0 Mpc is smooth at
  `σ ≤ 0.2`, the 3.7σ feature in this lane is a binning artefact and the profile is "law + a
  smooth concentrated component" with no boundary.

The decisive positive test is a **mass-binned** version: `r_sp ∝ M^(1/3)` moves the kink from 1.10
to 1.99 Mpc between 5e13 and 3e14 M_☉, so the same fixed annulus must show `u` falling with mass.
That is a zero-parameter prediction, and eRASS1's full sky (~12 000 clusters) crossed with LSST Y1
or DES Y6 supplies it at the required `σ_u ≈ 0.03`.
