# W4-06: is there a 4 in weak lensing? CONSISTENT, NOT DECISIVE

**Bottom line.** Weak lensing of isolated late-type galaxies gives **κ_Λ = 0.52 ± 0.09 (stat) ± 0.24 (stellar mass)**.
- It agrees with the rotation-curve value (CFG493: 0.417 ± 0.095; z = +0.78 statistical, +0.38 with the mass systematic).
- It agrees with ½.
- It cannot tell ½ from 0.461: Δχ² = 0.4.

This is the first κ in the record from a route that shares none of the rotation-curve systematics: no HI-flux tie, no
inclinations, no rotation-curve reduction. Its own limit is the lens stellar masses. A ±0.2 dex shift moves κ from 0.41 to
0.88. So lensing confirms that κ is of order ½ by an independent method, but it does not pin the 4. Pinning it needs about
3% on κ; this route is at 48%.

This is an **observational lane (`obs`)**, not a derivation. **κ = ½ is FITTED.** Not theory closed.

## Method

- **Data.** B21's public KiDS-1000 RAR files for isolated blue lenses (u−r < 2.5): 15 points, g_bar 1.4×10⁻¹⁵ to
  3.9×10⁻¹² m/s². The full B21 covariance is used. CFG829's loader is copied unchanged.
- **Fit.** κ is fitted directly by χ² on a fine log grid, with g_obs = g_bar ν(g_bar/(κ s)) and s = c√(Gρ).
- **Footings,** never pooled: ρ_DE = Ω_Λ ρ_crit, and ρ_crit.
- **Windows:** CFG829's frozen windows only.
- **Check.** K1 reproduces CFG829's amplitude to 4 decimals: A = 1.0164 ± 0.0858.

## Results (`w4_06.out`)

| fit | κ (ρ_DE) | κ (ρ_crit) | points |
|---|---|---|---|
| **PRIMARY**: ν_simple, window 10^−13.3–10^−11.9 | **0.520 [0.433, 0.614]** | **0.430 [0.358, 0.509]** | 6 |
| ν_e, same window | 0.520 | 0.430 | 6 |
| window extended to 10^−10.9 | 0.455 [0.385, 0.531] | 0.377 [0.318, 0.440] | 8 |
| all 15 blue points (report; the lowest-g_bar points may carry two-halo contamination) | 0.481 [0.425, 0.540] | 0.398 [0.352, 0.447] | 15 |
| calibration window alone | not diagnostic (2 points) | — | 2 |

**Systematics on the PRIMARY** (each a separate refit; ρ_DE):

| variant | κ |
|---|---|
| lens M★ −0.2 dex | 0.877 |
| lens M★ +0.2 dex | 0.406 |
| native distances, T 0.968 (CFG885) | 0.486 |
| native distances, T 1.062 (CFG885) | 0.589 |
| window −0.3 dex | 0.761 |
| window +0.3 dex | 0.526 |

The envelope is 0.41–0.88. Stellar mass dominates: in the deep regime κ ∝ g_obs²/g_bar, so a 0.2 dex mass shift is a factor
of 1.58 in κ.

**Grading (frozen)**

| footing | κ_lens | vs CFG493 | ½ vs 0.461 | verdict |
|---|---|---|---|---|
| ρ_DE | 0.520 ± 0.091 ± 0.235 | z = +0.78 statistical, +0.38 total | Δχ² +0.40, not separated | CONSISTENT, NOT DECISIVE |
| ρ_crit | 0.430 ± 0.075 ± 0.195 | z = +0.78 statistical, +0.38 total | Δχ² −0.65, not separated | CONSISTENT, NOT DECISIVE |

## What it adds to "why 4"

- **The 4 is not a rotation-curve artefact.** An independent lensing route lands at the same κ ~ ½, within its errors.
- **Lensing cannot be the route to the decisive 3%.** Its error is set by stellar masses: κ ∝ g_obs²/g_bar in the deep
  regime, so σ(κ)/κ ≈ ln 10 × σ(log M★) ≈ 0.46 for 0.2 dex. Reaching 3% would need lens masses to about 0.013 dex. The "4 versus 2π" question stays a rotation-curve
  and distance problem: M/L zero point, gas scale, ladder.

## Checks and controls

- **I1:** no footing a₀ value and no measured κ upstream of the fit.
- **K1:** reproduces CFG829.
- **K2:** mock recovery with κ_true = 0.30 and 0.50 (50 mocks each, seed 101) gives medians 0.288 and 0.499, each inside the
  mocks' own 1σ.
- **K3:** the minimum is interior and bracketed.
- **K4 (report):** ½A² = 0.517 against a fitted 0.520.
- **MUTATE** (g_obs × 1.21): κ rises by 1.481, against about 1.46 expected in the deep regime. Exit 1 by design. In MUTATE
  mode K1 is not graded, because A scales by 1.21 as intended.

## Run note

The orchestrator restarted NC2x (1024³, chain7b) while this lane ran. Both runs were single-core, 46 MB and about 4 s, under
the CFG894 §11 light-script rule. NC2x's swap was flat (5.46 GB, below its 5.79 GB start) before and after.

## Files and how to run

| file | what |
|---|---|
| `FROZEN_CRITERIA.md` | committed alone first (6f967094d) |
| `w4_06.py` | numpy, one process, 3.7 s, 46 MB peak; reads B21 files and CFG885's committed JSON |
| `w4_06.out`, `w4_06_results.json` | normal run, 5/5 PASS, exit 0 |
| `w4_06_MUTATE.out`, `w4_06_results_MUTATE.json` | `W4_06_MUTATE=1`, κ × 1.481, exit 1 by design |

    OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_06_lensing_kappa/w4_06.py > why_4_puzzle/W4_06_lensing_kappa/w4_06.out
    W4_06_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 why_4_puzzle/W4_06_lensing_kappa/w4_06.py > why_4_puzzle/W4_06_lensing_kappa/w4_06_MUTATE.out

The B21 files are read only and nothing was downloaded. B21's ESDs use flat ΛCDM distances. CFG885's native-background
bracket (S2) covers that, and it is a small effect next to M★.

## Register

Row **K636** in `campaign_fresh_gravity/CFG894_kappa_campaign_ledger/kappa_attempts_register.csv` (obs class). The register commit
b1fd309ec says "K631" in its message: a parallel session had appended K631–K635 a moment earlier. The CSV row itself is K636.
