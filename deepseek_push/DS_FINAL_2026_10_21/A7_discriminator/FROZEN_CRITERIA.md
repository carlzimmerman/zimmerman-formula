# A7 FROZEN CRITERIA — pre-registered n=1 vs n=2 discriminator on SPARC

**FROZEN at 2026-10-21T21:28:48Z (2026-10-21 17:28:48 EDT), before any χ², Δχ², best-fit Υ
or residual number in this lane was computed.** Nothing below was chosen after seeing a
Δχ². The only data-facing operation performed before this file was written was reading
the rotmod headers (to name the columns) and counting files/rows/galaxies with < 5 rows.

Amendments, if any, are appended at the bottom in a section `## AMENDMENTS` with the reason
and the time; the body above an amendment is never edited.

---

## 1. Question and the two models

Does SPARC, as it stands, separate the two surviving galactic laws at fixed a₀ and the same
baryonic source?

- **n = 1 (canonical, frozen S2 rest state; BRIEF §1).**
  `g_N = g² / (g + a₀)`, inverted for prediction:
  `g₁(g_N) = (g_N/2) · (1 + √(1 + 4 a₀/g_N))`.
- **n = 2 (a₀-line, half capacity; BRIEF §1).**
  `g² − g_N² = a₀ g_N`, inverted:
  `g₂(g_N) = √(g_N² + a₀ g_N)`.

Both have the same leading deep limit `g → √(a₀ g_N)`; they differ in the next order and,
crucially, at high acceleration: `g − g_N → a₀` (n=1) versus `a₀/2` (n=2). They are
therefore *different effective theories*, not relabellings, and the difference is largest in
the transition region `g_N/a₀ ~ 0.1–3`, not in the deep limit.

`g` is the total (observed) acceleration, `g_N` the baryonic one, both in m s⁻².

## 2. a₀ footings (never pooled, reported separately, no combined number)

- canonical: `a0_can = 9.36e-11 m s⁻²`
- alt: `a0_alt = 1.13e-10 m s⁻²`

These are the two values mandated by BRIEF §4 and are used **exactly** as given; no fitted
a₀ enters anywhere. A fit of a₀ is *not* performed (it would confound the law comparison).

## 3. Data and columns used

`real_research/data/sparc_data/*_rotmod.dat`, 175 files. Header of every file is

```
# Distance = <D> Mpc
# Rad  Vobs  errV  Vgas  Vdisk  Vbul  SBdisk  SBbul
# kpc  km/s  km/s  km/s   km/s   km/s   L/pc^2  L/pc^2
```

Columns used, and their meaning as used here:

| col | use |
|---|---|
| 1 `Rad` [kpc] | radius; `r_m = Rad · 3.0856775814913673e19 m` |
| 2 `Vobs` [km/s] | observed rotation velocity = data |
| 3 `errV` [km/s] | statistical error on `Vobs` |
| 4 `Vgas` [km/s] | gas contribution **including the 1.33 helium correction** (SPARC/Lelli+2016 convention: the column is the full gas term, HI+He), held **fixed** |
| 5 `Vdisk` [km/s] | stellar disk contribution at Υ_disk = 1 M☉/L☉,3.6μm |
| 6 `Vbul` [km/s] | stellar bulge contribution at Υ_bul = 1 M☉/L☉,3.6μm |

`SBdisk`, `SBbul` (cols 7–8) are **not used** (they are not needed for the fit; they would
only matter for a profile-shape systematic, which is out of scope here and declared in §9).

Baryonic source, identical for both laws and both footings:

```
V_bar²(Υ) = Vgas² + Υ · (Vdisk² + Vbul²)          [km²/s²]
g_N       = V_bar² · 1e6 / r_m                     [m/s²]
```

(The `1e6` converts km²/s² → m²/s².) `Vgas²` is used squared, so a negative `Vgas` entry
(which occurs in SPARC where the gas term is a small deficit) still contributes its mass
term with the correct sign; this is the standard SPARC handling.

**Point selection (identical for both laws, both footings, all Υ):** a row enters the fit iff
`Vobs > 0`, `errV > 0`, and `Vgas² + Υ_min·(Vdisk² + Vbul²) > 0` with `Υ_min = 0.05`. The set
does not depend on the law, on a₀, or on the fitted Υ — so every Δχ² below is a paired
comparison on identical points. Galaxies with **fewer than 5** selected points are dropped
(count reported). No quality flag, inclination or distance cut in the primary (declared
variants in §8).

## 4. Free parameters — exactly one per galaxy, identical freedom for both laws

- **Primary: a single stellar mass-to-light ratio per galaxy**, `Υ ≡ Υ_disk = Υ_bul`
  (one number at 3.6 μm, in solar units), applied to both stellar components:
  `Υ ∈ [0.05, 2.50]`.
- Both laws get the **same** one-parameter freedom. No other parameter is fitted: no a₀, no
  distance, no inclination, no gas scaling, no intrinsic-scatter parameter.
- Fitting method: deterministic 1-D global scan in `log10 Υ` (400 points) followed by bounded
  Brent refinement in the bracket of the best grid point (`scipy.optimize.minimize_scalar`,
  `method="bounded"`, `xatol=1e-10`), on `log10 Υ`. Convergence is checked by re-running the
  whole fit with 800 grid points (check K6) and by the local-optimality check (K3).
- Boundary solutions are **not** clipped or penalised; the fraction of galaxies at either
  boundary is reported.

## 5. Error model

```
σ_i² = errV_i² + (0.05 · Vobs_i)²
χ²_g(Υ) = Σ_i [ (Vobs_i − V_pred,i(Υ)) / σ_i ]²
```

The 5 % floor on `Vobs` is **included** (declared here, as required): SPARC's quoted errors
are formal and do not include distance, inclination or profile systematics, and without a
floor high-S/N points dominate the fit. A no-floor variant is reported in §8 but is not the
primary.

`V_pred` is computed in velocity space (not log space), because the floor is defined on
`Vobs` and the two laws differ by a velocity-space amount that is roughly constant per
galaxy; χ² in velocity space is the standard SPARC likelihood.

Units: `V_pred = √(g_pred · r_m) / 1000` [km/s], with `g_pred` from §1.

## 6. Primary statistic and decision rule (fixed now)

For each galaxy `g`, each law `L`, each footing:

`χ²_{g,L} = min_Υ χ²_g(Υ; L)`,  `Δχ²_g = χ²_{g,n2} − χ²_{g,n1}`,  `Δχ²_tot = Σ_g Δχ²_g`.

- **Decision (per footing):**
  - `Δχ²_tot ≥ +9.0` → **n = 2 KILLED at 3σ** (canonical preferred), on that footing.
  - `Δχ²_tot ≤ −9.0` → **n = 1 KILLED at 3σ** (n = 2 preferred), on that footing.
  - `|Δχ²_tot| < 9.0` → **NOT DECIDED**: the laws are degenerate at SPARC precision and the
    forecast (§7) is the deliverable.
- **Footing consistency:** the headline verdict "SPARC decides n" requires the *same*
  category and sign on **both** footings. If the two footings disagree in sign, the result is
  reported as **footing-dependent** and no kill is claimed on either.
- **Secondary (reported, not decisive):** number of galaxies won by each law
  (`Δχ²_g < 0` → n=2 wins), two-sided binomial sign test, and a bootstrap (10 000 resamples
  over galaxies, seed 20261021) standard error on `Δχ²_tot` giving `z = Δχ²_tot/σ_boot`.
  The bootstrap is secondary because per-galaxy `Δχ²_g` are correlated with galaxy mass and
  the sum is dominated by the best-measured systems.

A kill is a kill only if `|Δχ²_tot| ≥ 9`; a "preference" below that is reported as such and
**must not** be written up as evidence.

## 7. Forecast (declared before the data are read)

Two independent forecasts, both from the measured per-point scatter and the fitted models:

1. **Non-centrality forecast (primary).** For each galaxy take the *truth* to be one law at
   its own best-fit Υ, form the noiseless curve `V_true` on that galaxy's radii, refit the
   *other* law (and refit Υ) to `V_true` with the same σ_i, and record
   `λ_g = Σ_i [(V_true,i − V_other,bf,i)/σ_i]²`. Then `λ_tot = Σ_g λ_g` is the expected Δχ²
   for a 3σ separation. `N_3σ = 9 / (λ_tot/N_gal)`. Compute this for both truth hypotheses
   and both footings.
2. **Error-reduction forecast.** Δχ² scales as `1/σ²`; the factor by which all error bars
   must shrink to reach `λ_tot = 9` is `√(λ_tot/9)` (reported as "errors × f", f < 1 means
   shrink).

Also report the single-galaxy maximum of `|V₂ − V₁|/V₁` at fixed `g_N` and fixed Υ (a pure
theory number, independent of the fit), its location in `g_N/a₀`, and the binned curve — this
is the independent check of the prior lane's "7.46 %" claim, which is **not** trusted.

**Verdict wording fixed now:** "SPARC can decide n at 3σ" iff `λ_tot ≥ 9` on both footings;
otherwise SPARC **cannot** decide n and the required `N_3σ` (or error factor) is the result.

## 8. Reported variants (declared now; the primary stands whatever they show)

- V1: `Υ_bul = 1.4 · Υ_disk` (two-parameter stellar model, common SPARC/CFG4 convention).
- V2: no 5 % floor (`σ_i = errV_i`).
- V3: quality cut `Q ≤ 2` (requires the Lelli+2016 master table; if unreadable, reported as
  unavailable).
- V4: fixed `Υ = 0.5` for all galaxies (no fit), to show how much of any difference the
  nuisance parameter absorbs.
- V5: restrict to the transition region `0.1 ≤ g_N/a₀ ≤ 3` and recompute `Δχ²_tot`.

None of these may replace the primary; any change of sign in a variant is disclosed.

## 9. What is deliberately not modelled

Distance and inclination errors (coherent per galaxy, would add a correlated error and can
mimic a law change), non-circular motions, warps, the 3.6 μm profile shape, the bulge/disk
decomposition, and any a₀ evolution. These are the standard weaknesses of a SPARC
law-comparison and are stated in the report as the scope of the claim.

## 10. Checks that must pass (implementation, not physics outcomes)

- **K1** data integrity: 175 files parsed, 3391 data rows, columns match the header, the
  number of galaxies with ≥ 5 selected points is reported.
- **K2** law algebra: round-trip inversion of both laws to 1e-12 relative; both laws share the
  leading deep limit (ratio → 1 as `y → 0`, checked at `y = 1e-8`); the high-acceleration
  anomaly ratio `(g−g_N)|₁ / (g−g_N)|₂ → 2` as `y → ∞` (checked at `y = 1e4`).
- **K3** optimiser local optimality: for every interior best fit, `χ²(Υ_bf) ≤ χ²(1.02 Υ_bf)`
  and `χ²(Υ_bf) ≤ χ²(0.98 Υ_bf)`.
- **K4** arithmetic: `Σ_g Δχ²_g = Δχ²_tot` to 1e-8; wins sum to the galaxy count.
- **K5** mutation `--mutate` (laws swapped) flips the sign of `Δχ²_tot` exactly
  (`|Δχ²_mut + Δχ²| ≤ 1e-9`), on both footings.
- **K6** grid convergence: `Δχ²_tot` from the 400-point scan and from an 800-point scan agree
  within 0.5.
- **K7** finiteness: every χ² is finite and ≥ 0; every galaxy is fitted under both laws on
  both footings.
- **K8** theory-level difference: the dense scan of `max |V₂−V₁|/V₁` at fixed `g_N`, fixed Υ
  is attained in `0.1 ≤ g_N/a₀ ≤ 3` and lies in `[0.03, 0.15]` (a sanity band for the
  independent 7.46 % claim; a value outside it would mean the two laws are being implemented
  wrongly or the claim is wrong — either way it must be surfaced, not hidden).

Status of the lane is `NUMERICAL` (BRIEF §5), with the verdict taken from §6 and the forecast
from §7.

---

## AMENDMENTS

### Amendment 1 — 2026-10-21T21:35:24Z — forecast F2 added, after unblinding

**Status: appended after the primary numbers were computed. Nothing above this line was
edited; no model, point selection, Upsilon range, error model, statistic or decision rule was
changed.**

Reason. The pre-registered forecast (section 7, item 1, "F1") assumes the declared error model
is exact: it computes the expected non-centrality `λ_tot` using `σ_i = √(errV² + (0.05 Vobs)²)`
as if the fits were perfect. The data reject that assumption: the best fits have
`χ²/dof = 2.27` (n=1) and `2.33` (n=2) on the canonical footing, and the measured per-galaxy
Δχ² scatter is `sd = 22.7`, versus `√(2·2λ̄) ≈ 3.8` expected from the same λ̄ ≈ 1.8. F1
therefore predicts N(3σ) = 5–6 galaxies, while the 171 galaxies on disk give `z = 0.75`
(0.75σ). The two cannot both be right, and the discrepancy is itself a result about the data
quality, not about the laws.

Added, as a **reported** forecast (F2), not as a replacement:

- `N(3σ) = (3 · sd(Δχ²_g) / λ̄)²`, where `λ̄` is F1's model-predicted mean Δχ² per galaxy (the
  signal) and `sd(Δχ²_g)` is the measured galaxy-to-galaxy scatter of Δχ²_g on SPARC (the
  noise, which includes distance/inclination systematics and profile mismatch). This is the
  number of *SPARC-quality* galaxies needed for a 3σ total, and it is the forecast the task
  asks for ("given the measured per-point scatter").
- The equivalent error-reduction factor at fixed N = 171 follows from `SNR ∝ 1/σ_eff²`:
  errors must shrink by `√(N_needed/171)`.

Also added, as reported robustness diagnostics only (section 6's decision rule is untouched):

- D1: Δχ²_tot recomputed excluding galaxies whose best-fit Upsilon sits on a bound. Their
  Upsilon is not measured by the data (mostly gas-rich dwarfs where the stellar term is
  subdominant), so their per-galaxy Δχ² is bound-driven, not law-driven.
- D2: the per-galaxy Δχ² histogram, the five largest contributors and the total without them.

Both are labelled "reported, not decisive" wherever they appear. The verdict remains that of
section 6, evaluated on the primary statistic.
