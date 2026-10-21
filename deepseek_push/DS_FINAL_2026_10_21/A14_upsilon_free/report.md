# A14 — κ from data with no stellar mass-to-light prior

## Claim

The Upsilon-free channel exists, works, and is not good enough. Concretely:

1. **The sample is 12 galaxies.** Of 175 SPARC curves, **12** (73 points) have gas
   dominating the baryonic budget at *every* fitted radius outside 2 disk scale
   lengths (`f_gas > 0.80`), reach `g_bar < a0`, and pass `Q <= 2`. The median
   depth reached is **g_bar/a0 = 0.0235** (deepest point 0.0092, shallowest galaxy
   0.0702), so the deep law is genuinely probed. At a Salpeter M/L only 4 survive.
2. **The channel does what it was built to do, and only that.** The stellar-M/L
   lever falls from `dln a0/dln Upsilon = -1.082` on the full sample to **-0.167**
   on the free sample: the Chabrier→Salpeter bracket (+0.24 dex) moves a0 by
   **×1.097** here versus **×1.819** there. A 6.5× reduction in the log, but not
   zero — and the residual is exactly the `(1 - f_gas)` predicted in D1.
3. **One parameter, both laws, both footings:** `a0 = 6.62e-11` (canonical n = 1)
   and `7.94e-11` (quadratic n = 2), χ²r = 4.12 and 3.94 with the 5% floor. The
   two laws differ by **20%**, so the interpolation choice alone is a ±10%
   systematic — twice the 5% target.
4. **κ = 0.354 ± 0.106** (CMB-normalised ρ_DE) or **0.326** (local-H0 ρ_DE). The
   record's `0.465 ± 0.076` sits 1.0σ away and κ = 1/2 sits 1.4σ away. Nothing is
   confirmed and nothing is excluded — that is the measurement.
5. **The conventions are not internally consistent at 5%, before any data are
   touched.** The 2×2 grid {canonical, alt} × {CMB, local} spans
   **0.4615 → 0.6046, a factor 1.31**. Adding the data widens the full range to
   **0.326 → 0.605, a factor 1.85**.
6. **The decisive adversarial number: the answer is set by the distance prior, the
   one prior the channel was meant to escape.** The 4 galaxies with 2–5% distances
   give `a0 = 1.132e-10`; the 8 with 25–30% Hubble-flow distances give
   `5.138e-11`. Factor **2.20** — κ from 0.275 to 0.605 — and the footing preference
   (canonical over alt by Δχ² = 201 pooled) **reverses** on the clean-distance half.
7. **5% κ needs ~195 galaxies and simultaneously a ≤2.5% coherent distance scale.**
   SPARC supplies 4 galaxies that satisfy both the gas and the distance condition.
   The coherent floors — distance zero point 16.1%, residual M/L 9.7%, law choice
   10.0% — do not shrink with N.

## Derivation

**D1 (the residual M/L lever is exactly 1 − f_gas).** In the deep limit
`a0 = g_obs²/g_bar`. With `g_bar = g_gas + Υ g_*` and `f_gas = g_gas/g_bar`,

```
dln a0 = -dln g_bar = -(Υ g_*/g_bar) dlnΥ = -(1 - f_gas) dlnΥ .
```

At the frozen threshold this predicts `|slope| <= 0.20`; with the sample's mean
`f_gas = 0.874` it predicts **-0.126**. Measured: **-0.167**. The measured
full-sample slope is **-1.082**, six times larger, because there the disc and bulge
enter as a mass model rather than through a `1 - f_gas` weight. The point stands
either way: **"Upsilon-free" means `(1 - f_gas)`-free, i.e. 13% free at this
threshold, not free.**

**D2 (distance scaling: a0 → a0/f², not a0/f).** At fixed angular position, `D → fD`
sends `r → fr`, `V_obs → V_obs` (Doppler), and — because surface brightness is
distance-free while `L ∝ D²` and `M_gas ∝ D²` from the fluxes — `V_bar → f^(1/2) V_bar`.
Hence

```
g_bar = V_bar²/r → invariant ,      g_obs = V_obs²/r → g_obs/f .
```

A distance error is therefore a **pure vertical shift** of the RAR. In the deep
limit `g_obs = sqrt(a0 g_bar)`:

```
a0 → a0 / f²        (exact in the deep limit; residual O(sqrt(g_bar/a0)))
```

Verified by refitting rescaled data: `a0 f²/a0 = 0.9795` (canonical) and `0.9932`
(quadratic) at `f = 1.10` (K4). The residual 2% is the interpolation correction,
not a failure of the scaling. **This is not the `a0 ∝ 1/f` of "freeze V_bar and
move only r"** — that bookkeeping rescales the baryonic mass as `M ∝ D` instead of
`D²`, and it is what A9 K2's exact-degeneracy claim rests on. K5 tests the exponent
against the data with no rescaling at all: the per-galaxy a0 scatter is **0.207 dex**
and the published `e_D/D` (rms 0.242) predicts **0.210 dex** for p = 2 versus
**0.105 dex** for p = 1. p = 1 would require 0.178 dex of intrinsic a0 scatter on
top; p = 2 requires none. **The data pick the squared scaling.**

**D3 (kappa on two densities).** `kappa = a0/(c sqrt(G rho_DE))`. The CMB measures
`Omega_L h² = 0.3107`, so

```
rho_DE(CMB)   = 3 (Omega_L h²) H100²/(8 pi G) = 5.8355e-27 kg/m³   (no local H0 in it)
rho_DE(local) = 3 Omega_L H0²/(8 pi G) = 6.8566e-27 kg/m³          (H0 = 73, Omega_L = 0.685)
kappa_local / kappa_CMB = sqrt(rho_loc/rho_CMB) = (73/67.36) sqrt(0.685/0.6847) = 1.0840 .
```

An 8.4% convention on κ, exact, with no data involved.

**D4 (the alt footing is the same κ on a different density).** `a0_alt = 1.1312e-10`
is `0.5 c sqrt(G rho_crit)` (it reproduces κ = 1/2 when divided by `rho_crit`), so

```
kappa_DE(a0_alt) = 0.5 / sqrt(Omega_L) = 0.5/0.8278 = 0.6046 .
```

"Two footings" and "two densities" are therefore **one choice**, made twice:
0.5003 → 0.6046 is a 20.9% span with no measurement in it.

**D5 (error budget and the N scaling).** With one parameter and a fixed 5% floor,
`sigma_a0` from `Δχ² = 1` is 3.00%, but the per-point errors are not the truth
(χ²r = 4.12), so the honest statistical error is the **block bootstrap over
galaxies**: 21.2%. Coherent systematics add as
`sigma² = sigma_stat² + sigma_scatter² + (2 ln f_H0)² + (|dln a0/dlnΥ| × 0.24 ln10)²
+ (Δlaw/2)² + sigma_He²`, giving **30.0%** in quadrature and 64.2% if every term is
treated as fully coherent. Because the leading term is galaxy-level scatter,
`sigma(N) = 0.201 sqrt(12/N)`, so 5% needs `N = 195`.

## Status

**NUMERICAL.** Thirteen checks pass on data on disk, and the result is a *measured
no-go for 5% κ from this channel*: the ceiling is set by convention (×1.31), by
distance quality (×2.20 across the sample split) and by the law (×1.20), none of
which the data can resolve. The negative result is the deliverable: the Upsilon-free
channel is **prior-free but not precision-clean**, and the record's
"κ measured = 0.465 ± 0.076" cannot be replaced by a better measurement from SPARC —
only by a differently *sourced* one.

## Checks (what `a14_checks.py` proves)

| id | what it proves | measured |
|---|---|---|
| K0 | data on disk and the V_disk convention | 175 curves, 0 Table-1 mismatches, `M(V_disk)/L36 = 1.094` (p16–84 0.94–1.25) → the column is the **M/L = 1** template |
| K1 | the sample exists and is big enough to fit | N_gal = **12**/175, N_points = **73** |
| K2 | every curve reaches the deep branch | median per-galaxy min `g_bar/a0` = **0.0235**, worst 0.0702; median over points 0.0345 |
| K3 | what the channel buys | `dln a0/dlnΥ` = **-0.167** (free) vs **-1.082** (full); IMF move **×1.10** vs **×1.82**; gas-only a0 = 7.845e-11 (×1.19); Υ_eff = **0.708** |
| K4 | the distance exponent, by experiment | `a0 f²/a0 = 0.9795` at f = 1.10 |
| K5 | the distance exponent, from the scatter | **0.207** dex measured vs **0.210** (p=2) and **0.105** (p=1) |
| K6 | a0 on both laws | **6.6198e-11** (χ²r 4.12) and **7.9397e-11** (χ²r 3.94); ratio **1.1994** |
| K7 | both footings, and whether the verdict holds | χ²(can) − χ²(alt) = **-201** pooled, but **+13** on the 4 clean-distance galaxies |
| K8 | κ on the 2×2 grid | 0.4615–0.6046 (**×1.31**) conventions only; 0.326–0.605 (**×1.85**) with the fits |
| K9 | the error budget | **30.0%** quadrature, 64.2% linear; κ = **0.3538 ± 0.1060** |
| K10 | the forecast for 5% | **N = 195**; coherent distance floor **16.1%** |
| K11 | the pipeline is the same one that gives the record's a0 | full-sample `a0 = 9.6433e-11` vs A9's 1.1033e-10 (**0.874**) |
| K12 | the answer is not an artefact of the cuts | outer/inner = **0.970**; floor scan 6.448–7.010e-11 (×1.09); threshold scan N = 24/19/12/7/3 |

The mutation (`--mutate`) adopts A9's `a0 ∝ 1/f` bookkeeping consistently — freezing
`V_bar` under the rescaling and predicting the p = 1 scatter. It breaks **K4**
(0.1018 vs threshold 0.05) and **K5**, exits 1, and is recorded in `MUTATE.md`.

## What this does not do

- **It does not measure κ to 5%, and it does not claim a value.** The fitted
  0.354 ± 0.106 is one number from one cut; the threshold scan (N = 24 at 0.70,
  3 at 0.90) moves it. `f_gas > 0.90` (3 galaxies) gives a0 = 9.685e-11 → κ = 0.518,
  i.e. the answer is cut-sensitive at the 46% level between 0.354 and 0.518, which
  is the point.
- **It does not resolve Chabrier from Salpeter.** The channel's Υ_eff = 0.708;
  with the 30% error that is 1.0σ from Chabrier (0.50) and 0.8σ from Salpeter (0.87).
  This reads the free channel as an M/L *for the full sample*, so it assumes the two
  samples measure the same a0 — which point 6 of the Claim disputes.
- **It does not correct for pressure support / asymmetric drift**, which for these
  V_flat ≈ 50–70 km/s dwarfs is a ~2–3% correction to V_obs and therefore of order
  +10% in a0 (`a0 ∝ V_obs⁴`), always in the direction that would raise a0 toward
  the footings. Adding it would move κ up,
  not down; it is not in the budget because it needs data not on disk.
- **It does not correct for beam smearing**, which grows with distance and is
  therefore degenerate with the f_D = 1 / f_D = 2 split — the largest term found.
  Separating them needs angular resolution, not more galaxies.
- **It does not distinguish n = 1 from n = 2.** Pooled Δχ² = 12.9 favours the
  quadratic law, but it is +3.1 on the clean-distance half and −2.7 on the other,
  so the preference is not robust; what is robust is that the two laws give a0
  20% apart.
- **K11's 12.6% offset from A9's 1.1033e-10** is estimator difference (A9 minimises
  a log-space mean square with no error floor over 175 galaxies; this fits χ² in V
  with a 5% floor over 154 that satisfy `R > 2 R_d`). It is a validation, not an
  independent confirmation of the record's number.

## Next

1. **Stop quoting a single κ.** Quote the 2×2 grid and the data bracket:
   `kappa_DE = 0.354 [0.275, 0.605]` (method bracket), `kappa_crit = 0.326`.
2. **The binding requirement is distances, not galaxies.** A 5% κ needs
   `sigma_D/D <= 2.5%` coherent. That is a survey specification (TRGB or better on
   ~200 gas-dominated dwarfs), not an analysis improvement.
3. **Get the last 13% of the stellar mass out.** `f_gas > 0.93` at every fitted
   radius is what makes the residual M/L term fall below 5%. SPARC has **zero**
   galaxies that satisfy both `f_gas > 0.93` and a 2–5% distance; this cannot be
   fixed from the existing catalogue.
- **Settle n = 1 vs n = 2 on a sample where the two laws differ by more than the
   errors** — i.e. at `g_bar/a0 ~ 1`, not at 0.02, where their predictions differ by
   less than the data's own scatter.
   The Upsilon-free deep sample is the *worst* place to discriminate them.
