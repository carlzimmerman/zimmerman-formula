# A7 — pre-registered n=1 vs n=2 discriminator on SPARC

Lane: `deepseek_push/DS_FINAL_2026_10_21/A7_discriminator/`. Criteria frozen at
2026-10-21T21:28:48Z in `FROZEN_CRITERIA.md` before any χ² in this lane was computed
(one amendment appended afterwards, for the forecast only; see that file, `AMENDMENTS`).

## Claim

On all 171 SPARC galaxies with ≥ 5 usable points (3375 points), with **one free stellar
Υ per galaxy** (disk = bulge, at 3.6 μm) and a 5 % error floor, the two laws are **not
separated at 3σ**: the pre-registered rule fires on each footing, but in *opposite
directions*, so no kill can be claimed. Δχ² ≡ χ²(n=2) − χ²(n=1) = **+219.45** on the
canonical footing (n=1 favoured) and **−344.66** on the alt footing (n=2 favoured). The galaxy-to-galaxy scatter of Δχ²_g is 22.7,
so the bootstrap significance of either total is **z = +0.75** and **z = −1.21**: both totals
are consistent with zero. Per-galaxy wins are 84/87 and 73/98 — a coin toss
(sign-test p = 0.879 and 0.066). **SPARC as it stands cannot decide n.** The flip is a
footing-dependent balance between two footing-stable regime effects: 76 galaxies with median
y < 0.1 prefer n=2 (mean Δχ²_g = −6.29 / −9.33) and 20 with median y > 1 prefer n=1
(+17.16 / +10.22), with Spearman ρ = +0.32 (p ≈ 2e−5) on both footings. The forecast
(measured-scatter calibrated) is **N ≈ 1330–1980 SPARC-quality galaxies**, or effective
errors smaller by a factor ≈ 3 at N = 171; the ideal-error-model forecast (5–6 galaxies) is
invalid here because χ²/dof = 2.27.

## Derivation

1. Laws. `g` is the total (observed) acceleration and `g_N` the baryonic one, m s⁻²;
   `a₀` is fixed per footing and never fitted. Inverting the two frozen laws:

   - n = 1 (canonical, `g_N = g²/(g+a₀)`):
     `g₁(g_N) = (g_N/2)·(1 + √(1 + 4a₀/g_N))`
   - n = 2 (a₀-line, `g² − g_N² = a₀ g_N`):
     `g₂(g_N) = √(g_N² + a₀ g_N)`

   Equivalently ν₁(y) = (1+√(1+4/y))/2, ν₂(y) = √(1+1/y), y = g_N/a₀. Both have the same
   leading deep limit `√(a₀ g_N)`; they differ at next order and, at high acceleration, by a
   factor 2 in the anomaly: `g − g_N → a₀` (n=1) vs `a₀/2` (n=2). Check K2 measures
   the ratio 1.99985 at y = 10⁴.

2. Baryonic source, identical for both laws and both footings. From the rotmod columns
   `Rad` [kpc], `Vobs` [km/s], `errV` [km/s], `Vgas` [km/s] (HI+He, held fixed),
   `Vdisk`, `Vbul` [km/s] (at Υ = 1 M☉/L☉,3.6μm):

   `V_bar²(Υ) = Vgas² + Υ·(Vdisk² + Vbul²)`,  `g_N = V_bar²·10⁶ / r_m`,  `r_m = Rad·3.0856775814913673e19 m`.

   `SBdisk`, `SBbul` (cols 7–8) are not used.

3. Likelihood. `σ_i² = errV_i² + (0.05·Vobs_i)²`; `χ²_g(Υ) = Σ_i [(Vobs_i − V_pred,i)/σ_i]²`
   with `V_pred = √(g_law(g_N)·r_m)/10³` km/s. One parameter per galaxy, Υ ∈ [0.05, 2.50],
   fitted by a 400-point log grid + bounded Brent; identical freedom for both laws.

4. Statistic. `Δχ²_g = χ²_g(n=2) − χ²_g(n=1)` at each galaxy's own best-fit Υ;
   `Δχ²_tot = Σ_g Δχ²_g`, computed **separately per footing, never pooled**.

5. Decision rule (frozen): `Δχ²_tot ≥ +9` kills n=2 at 3σ, `≤ −9` kills n=1, and the kill is
   claimed only if **both footings agree in sign**. Otherwise: not decided.

## Result — primary (both footings, reported separately)

| quantity | canonical a₀ = 9.36e-11 | alt a₀ = 1.13e-10 |
|---|---|---|
| χ²(n=1), 171 galaxies, 3375 pts | 7259.38 | 7908.09 |
| χ²(n=2) | 7478.83 | 7563.43 |
| **Δχ²_tot = χ²(n2) − χ²(n1)** | **+219.45** | **−344.66** |
| galaxies won by n=1 / n=2 | 84 / 87 | 73 / 98 |
| sign-test p (two-sided) | 0.879 | 0.066 |
| bootstrap sd of Δχ²_tot (10⁴ resamples) | 294.44 | 284.98 |
| z = Δχ²_tot / sd | +0.75 | −1.21 |
| χ²/dof (n=1 / n=2), dof = 3204 | 2.266 / 2.334 | 2.468 / 2.361 |

**Per-galaxy Δχ²_g distribution** (n=2 minus n=1):

| | p5 | p16 | median | p84 | p95 | min | max | mean | sd |
|---|---|---|---|---|---|---|---|---|---|
| canonical | −16.96 | −6.67 | −0.015 | +9.12 | +27.31 | −122.24 | +143.13 | +1.28 | 22.72 |
| alt | −24.64 | −9.72 | −0.745 | +5.14 | +18.50 | −152.83 | +120.67 | −2.02 | 22.01 |

The distribution is centred on zero (median −0.015 / −0.745) with p16–p84 of −6.67…+9.12 /
−9.72…+5.14: 47/171 (canonical)
and 44/171 (alt) galaxies individually give |Δχ²_g| < 1; 87/171 and 85/171 give < 3. Half the
sample does not individually prefer either law at Δχ² = 3.

**Concentration / robustness (reported, not decisive).** The five largest |Δχ²_g| carry 29.7 %
(canonical) and 29.2 % (alt) of Σ|Δχ²_g|: UGC06787 +143.1 / DDO161 −122.2 / UGC02953 +99.2 /
UGC04305 −90.5 / NGC2903 +71.9 (canonical). Removing them: +117.9 / −211.8 (sign preserved).
31 and 33 galaxies have a best-fit Υ pinned on a bound (12.9 % / 11.7 % at the lower bound on
the canonical footing); those galaxies carry 28.7 % / 39.5 % of Σ|Δχ²_g|, and **removing them
gives Δχ²_tot = +673.74 (canonical) and +305.61 (alt)** — both footings then prefer n=1. This
is an unregistered cut and is not used for the verdict; it identifies where the alt-footing
sign flip comes from (see Mechanism).

**Fit quality and the nuisance parameter.** χ²/dof ≈ 2.3 means the 5 % floor understates the
real per-point scatter (distance, inclination, profile shape). Υ(n=2)/Υ(n=1) = 1.236 (median):
n=2 buys back part of its weaker boost with ~24 % more stellar mass, and |Υ₂/Υ₁ − 1| > 20 % in
61–62 % of galaxies — the quantitative statement of the degeneracy.

## Where the two laws differ — stacked curve in g_N/a₀

At **fixed baryonic source** (same Υ, same a₀) the fractional circular-speed difference is

  `(V₂ − V₁)/V₁ = √(ν₂/ν₁) − 1`,

which is independent of radius. Its maximum is **6.9395 % at g_N/a₀ = 0.500** (check K8).
Normalised by V₂ the same point is 7.4570 % — this is exactly the prior lane's "7.46 %":
**one number, two denominators.** It is not a discrepancy; the prior claim is reproduced, and
the peak sits in the transition region, as it must, because the deep limit is shared.

Stacked residuals at each law's own best-fit Υ (median fractional residual
(Vobs−Vmodel)/Vobs, canonical footing; n = points):

| bin g_N/a₀ | n | med δ(n=1) | med δ(n=2) | theory (V₂−V₁)/V₁ |
|---|---|---|---|---|
| 0.010–0.032 | 250 | −0.0226 | −0.0042 | −0.0301 |
| 0.032–0.100 | 823 | −0.0120 | +0.0021 | −0.0444 |
| 0.100–0.316 | 766 | +0.0153 | +0.0251 | −0.0608 |
| 0.316–1.000 | 618 | +0.0161 | +0.0250 | −0.0684 |
| 1.000–3.160 | 476 | +0.0027 | +0.0040 | −0.0593 |
| 3.160–10.000 | 279 | −0.0221 | −0.0267 | −0.0332 |
| 10.000–31.600 | 103 | −0.0052 | −0.0277 | −0.0141 |
| 31.600–100.000 | 24 | −0.0543 | −0.1078 | −0.0058 |

(alt footing, same shape: theory −0.0298 / −0.0432 / −0.0608 / −0.0681 / −0.0575 / −0.0331 /
−0.0138 / −0.0062.) Two things are visible. (i) The laws differ by ≤ 7 % in V, with the
difference confined to 0.01 ≲ y ≲ 30 and peaking at y = 0.5; in the deep limit proper they
approach each other. (ii) At y > 3 the n=2
residuals are systematically more negative than the n=1 residuals — the half-anomaly shows up
as a deficit, as it should. At y < 0.1 the data sit slightly **below** both laws.

## Mechanism: why the footing flips the sign

The sample splits by regime, and the split is the *same* on both footings — it is the
weighting that changes. With each galaxy's median g_N/a₀ (canonical):

- **76 galaxies with median y < 0.1** (gas-rich dwarfs, sitting slightly below the shared deep
  limit): mean Δχ²_g = **−6.29** (canonical) and **−9.33** (alt) — n=2, the *weaker* law,
  wins. Examples: DDO161, UGC04305, UGC07125, CamB, all with Υ pinned at 0.05.
- **20 galaxies with median y > 1** (massive spirals, high-acceleration inner points): mean
  Δχ²_g = **+17.16** and **+10.22** — n=1, the *larger* anomaly, wins. Examples: UGC06787,
  UGC02953, NGC2903, NGC2841.

Spearman correlation of Δχ²_g with median y: **ρ = +0.321 (p = 1.8e−5)** canonical and
**+0.323 (p = 1.6e−5)** alt — the same coherent trend on both footings. The total is a
near-cancellation between these two groups (76 dwarfs × −6.3 against 20 spirals × +17), and
a₀ sets how many galaxies fall in each and how strongly each prefers. That is why the *total*
flips sign while the *per-galaxy* physics does not: a genuine law preference at the total
level must have the same sign on both footings, because a₀ only shifts y.

Consistently, the pre-registered variant restricted to the transition region
(0.1 ≤ y ≤ 3, refit) gives **Δχ²_tot = +195.06 (canonical) and +124.24 (alt)** — same sign on
both footings, n=1 preferred, ~1σ. And the footing itself is constrained: χ²(alt) − χ²(can) =
**+648.71** under n=1 but only **+84.60** under n=2, i.e. n=2 is far less sensitive to a₀.

## Forecast

**F1 (pre-registered, assumes the error model is exact).** Non-centrality from the fitted
models: λ_tot = 301.43 (truth n=1, canonical), 254.05 (n=1, alt), 319.97 (n=2, canonical),
290.68 (n=2, alt) → N(3σ) = 5–6 galaxies, or errors × 5.3–6.0 **larger** than needed. F1 says
five galaxies would do. The 171 on disk give z = 0.75, so F1's assumption is what fails:
the fits are systematics-dominated (χ²/dof = 2.27) and the per-galaxy Δχ² scatter (22.7) is
≈ 5× the 2√(1+2λ̄) ≈ 4.3 that two one-parameter fits at the same λ̄ would produce.

**F2 (scatter-calibrated; Amendment 1).** With the model signal λ̄ per galaxy and the measured
per-galaxy scatter sd(Δχ²_g):

  `N(3σ) = (3·sd/λ̄)²` → **1495** (truth n=1, canonical), **1976** (n=1, alt), **1327**
  (n=2, canonical), **1509** (n=2, alt).

Per-galaxy signal-to-noise is 0.068–0.082. Equivalently, at N = 171 the effective per-galaxy
errors must shrink by a factor **2.8–3.4** — shrinking all errors 3× would drive χ²/dof from
2.3 to ~20, so this requires sub-percent *coherent* systematics (distances, inclinations),
not a reanalysis. **SPARC cannot decide n; a ~10× larger SPARC-quality sample, or a
transition-region sample with controlled distances/inclinations, can.**

## Best-fit Υ and physical sanity

Medians (p16–p84), in M☉/L☉ at 3.6 μm, one value per galaxy applied to disk and bulge:

| footing | Υ(n=1) | Υ(n=2) | in [0.1,1] (n1/n2) |
|---|---|---|---|
| canonical | 0.497 (0.107–0.927) | 0.633 (0.155–1.178) | 69 % / 65 % |
| alt | 0.416 (0.069–0.833) | 0.540 (0.102–1.036) | 68 % / 68 % |

Sane: medians 0.42–0.63, the canonical n=1 value 0.497 sitting on the stellar-population
value 0.5. The tails are the known SPARC behaviour: 12–16 % of galaxies (gas-rich dwarfs)
drive Υ to the 0.05 bound and 1–5 % to the 2.50 bound. Those are not
measurements of Υ — the stellar term is subdominant there — and they are the galaxies that
carry the alt-footing sign flip.

## Checks (`a7_checks.py`, 8/8 PASS, exit 0, ≈1.3 s, no network)

- **K1** 175 files, 3391 rows parsed, 171 galaxies with ≥ 5 points (3375 points used;
  dropped D512-2, NGC6789, UGC00634, UGC07232).
- **K2** exact inversion round-trips (0 and 0); shared deep limit |g₁/g₂−1| = 5.0e−5 at
  y = 1e−8; high-acceleration anomaly ratio 1.99985 at y = 10⁴.
- **K3** every interior best fit is locally minimal (0 violations under ±2 % Υ).
- **K4** Σ_g Δχ²_g = Δχ²_tot (1e−8) and wins sum to 171.
- **K5** the `--mutate` run swaps the laws and flips Δχ²_tot exactly:
  +219.453 → −219.453 and −344.663 → +344.663, |mutated + baseline| = 0.00e+00.
- **K6** 400-point and 800-point Υ grids give identical Δχ² (max diff 0.0000).
- **K7** all χ² finite, ≥ 0, one fit per galaxy per law per footing.
- **K8** max |V₂−V₁|/V₁ = 6.9395 % at y = 0.500, inside the pre-registered band.

## Variants (reported, not decisive)

| variant | Δχ² canonical | Δχ² alt |
|---|---|---|
| V1 Υ_bul = 1.4 Υ_disk | +529.37 | −51.94 |
| V2 no 5 % floor | +10535.03 | +3946.47 |
| V4 fixed Υ = 0.5 (no fit) | +3064.32 | +681.47 |
| V5 transition region 0.1 ≤ y ≤ 3, refit | +195.06 | +124.24 |

V4 is the key degeneracy number: at a common Υ = 0.5 the canonical law is preferred by 3064 on
the canonical footing, and letting each law fit its own Υ removes 92.8 % of that. V2 shows what happens without the
floor: the comparison becomes a contest between the worst-fit points (Δχ² ~ 10⁴) and is
meaningless. V1 (two-parameter stellar model) makes the alt footing flip further.

## Status

**NUMERICAL — no decision.** The pre-registered rule fires per footing but in opposite
directions, so no kill is claimed; the bootstrap says both totals are < 1.3σ. The two laws are
degenerate at SPARC's precision once each galaxy's Υ is free. The forecast is the deliverable:
**N ≈ 1330–1980 galaxies of SPARC quality (or ~3× smaller effective errors) for a 3σ
separation**, and the discriminating data are the transition region 0.1 ≲ g_N/a₀ ≲ 3 of
*well-measured* (distance-controlled) galaxies.

## What this does not do

- No distance, inclination, or profile-shape error is propagated. Those are coherent per
  galaxy and are the dominant cause of the 22.7 scatter in Δχ²_g; propagating them adds a
  common-mode error and reduces the significance — it cannot be relied on to strengthen it.
- One Υ for disk and bulge; no separate bulge prior (V1 explores the 1.4× alternative).
- No intrinsic-scatter parameter is fitted; the 5 % floor stands in for it.
- No a₀ fit. Fitting a₀ per law would confound "law" with "footing" — the footing flip above
  shows exactly why.
- No quality cut in the primary (V3/Q ≤ 2 not run: it needs the master table and would be one
  more unregistered handle). No use of `SBdisk`/`SBbul`, no 3.6 μm profile decomposition.
- The forecast treats galaxies as independent draws of the measured Δχ² distribution; it does
  not model how a future sample's systematics would differ.

## Next

1. The decisive measurement is not more points on the same galaxies — it is **more galaxies
   with controlled distances/inclinations** in 0.1 ≲ y ≲ 3 (the 6.9 % band), where the two
   regimes of the Mechanism overlap and the laws differ most: at the ~1500-galaxy level, or a
   ~3× reduction in coherent per-galaxy systematics.
2. A cheap intermediate: repeat this exact pipeline on a distance-refit sample (e.g. TRGB/
   Cepheid distances) to see whether the Δχ²_g scatter drops; if it does not, the scatter is
   intrinsic and even 1500 galaxies will not decide it.
3. The a₀ sensitivity asymmetry (Δχ² 648.7 vs 84.6 between footings) is itself a handle: if an
   independent a₀ measurement pins the footing to ≪ 20 %, n=2's insensitivity becomes a
   prediction, not a nuisance.
