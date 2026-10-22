# A46 — is the minimal-vacuum cosmology falsified? A full background fit

**Lane:** A46_cosmology_fit · **Date:** 2026-10-21 · **Base:** A42 `report.md`,
A33 `MASTER_ACTION.md` §3.5 (F1/F2), CFG960 `FROZEN_CRITERIA.md` (footings never pooled).
**Script:** `a46_checks.py` (17/17 PASS, exit 0, ≈15 s) · **Output:** `a46.out` · **Data:** `a46_results.json`.
Two mutations, each exit 1: `MUTATE.md`, `a46_MUTATE_*.out`.

## Claim

**A42's 10.3σ exclusion is an artefact, and the honest fit reverses it — but the theory still fails, one
step later and for a different reason.**

1. A42 compared `Ω_m,eff h² = 0.1092` with Planck's `Ω_m h² = 0.1431`. Those are not the same quantity:
   `Ω_m,eff` is the coefficient of `(1+z)³` in `H²`, not a density. The model's **physical** matter density
   is `Ω_m h² = 0.1437`, identical to Planck's (K13). The 10.3σ is a category error.
2. Done properly, the model's background is an **exact reparametrisation of flat ΛCDM**:
   `E²_model(z; Ω_m,h) = E²_ΛCDM(z; Ω_eff,h_L)` with `Ω_eff = Ω_m/(1+Ω_m)` and `h = h_L√(1−Ω_m,L)`.
   Every distance **ratio** (`D_M/r_d`, `D_H/r_d`, `R`, `l_A`) and the whole SNe Hubble diagram are
   invariant; at the mapped point they agree to 0.33% and `Δχ²_SN = 0.005` (K5, K17).
   Fitting BAO + SNe + CMB gives **Δχ² = −0.58 for the same 3 parameters** — not 10σ. **The background
   data do not exclude it.**
3. The reparametrisation is not free: it forces `H0 = H0,ΛCDM√(1−Ω_m,LCDM) = 68.42 × 0.8355 = 57.2 km/s/Mpc`,
   hence `a0 = cH0/Z = 9.5–9.6×10⁻¹¹ m/s²` (9.59 from the exact map, 9.53 from the fit). That is the **canonical**
   footing (+2.4% / +1.8% from `9.3603e-11`), **not** `1.1312e-10` (−15.2% / −15.8%).
4. Fixing `H0 = 67.40` (the value `a0 = 1.1312e-10` demands) gives **Δχ² = +58.8 (7.7σ) without the baryon
   prior and +749.3 (27.4σ) with it**, ΔAIC = +56.8 / +747.3. The failure is in the **distance normalisation**
   — `r_d = 169.8 Mpc` against the 147.09 the BAO needs (+15.5%) — **not in the shape of H(z)**: the SNe
   χ² moves by +43 out of 1389 for 1580 points (K11).

**Status:** `DERIVED(the degeneracy, exact at the distance-ratio level)` + `NUMERICAL(the fits)` +
`NO-GO(a0 = 1.1312e-10 branch, Δχ² ≥ 58.8)` + `CONDITIONAL(background only — no Boltzmann, no BBN)`.

---

## 1. The model's own background, exactly

(F1) of A33, with `K = 4πG` and `Λ_bare c²/3 = H0²`:

```
3(2+3β) H² = 2 Λ_bare c² + 4K ρ ,      ρ = ρ_m + ρ_c + ρ_r ,      β = (2/3)Ω_m ,  Λ_bare = 3H0²/c²
```

Solving for `H²` and defining `Ω_m = 8πGρ_m0/(3H0²)`, `Ω_r = 8πGρ_r0/(3H0²)`:

> **E²(z) ≡ H²(z)/H0² = [ 1 + Ω_m(1+z)³ + Ω_r(1+z)⁴ ] / (1 + Ω_m + Ω_r)**   (K1, sympy residual 0)

Three statements the task asks for explicitly:

- **`ρ_c ∝ a⁻³`.** The cold sector is a collisionless Vlasov medium whose stress is dust:
  `p_c = ρ_c σ_c²` with `σ_c = 8.33 km/s`, i.e. `w_c ≈ 7.7×10⁻¹⁰`. It has **no vacuum term** — `L_cold`
  contains no constant (A42 §4). So `ρ_c = ρ_c0(1+z)³` and it is counted inside `Ω_m`.
- **The clock's negative stress is accounted for, and it is the whole story.** From (F1),
  `ρ_β = −9βH²/(4K) = −(3/2)β E² ρ_crit`. At `z = 0`, `E = 1` and `β = (2/3)Ω_m`, so
  `ρ_β(z=0) = −Ω_m ρ_crit` **exactly** (K2: residual `< 10⁻¹²`). That is what cancels the excess:
  `ρ_m + ρ_Λ + ρ_β = Ω_mρ_crit + ρ_crit − Ω_mρ_crit = ρ_crit`, so the effective budget is critical and
  `E(0) = 1` with no curvature. The `(1+Ω_m)` in the denominator of `E²` *is* `ρ_β` divided out.
- Radiation carries the same `(2+3β)` factor, so the exact closure reads `β = (2/3)(Ω_m+Ω_r)`;
  the difference from `(2/3)Ω_m` is `6×10⁻⁵` and is used in K3 (`E(0)=1` to `10⁻¹⁴`).

Two consequences worth stating because A42 states them differently:

| quantity | value | note |
|---|---|---|
| `Λ_bare/ρ_crit` | `1` | by construction: `Λ_bare = 3H0²/c²` |
| `Λ_eff/ρ_crit` (coefficient of the `Λ` term in `E²`) | `1/(1+Ω_m)` | the `(2+3β)` rescaling, not a density |
| `Λ_bare/Λ_obs = ρ_crit(H0)/ρ_DE` | `1/Ω_DE` | at `H0 = 67.4`: `1.4624`; at the fitted `H0 = 56.8`: `1.038` |

So `1.4626 = 1/(1−Ω_m)` is exact but is an **identity of the flat budget at `H0 = 67.4`**, not a prediction:
it says `ρ_crit(67.4) = ρ_DE/Ω_DE`. Change `H0` and the ratio changes with `H0²`. A42's "the excess *is*
the matter density" is right, and that is exactly why the ratio cannot also be evidence for the footing.

## 2. The degeneracy theorem

Write `Ω_eff ≡ Ω_m/(1+Ω_m)`. Then

```
E²_model(z) = Ω_eff(1+z)³ + Ω_r(1−Ω_eff)(1+z)⁴ + (1−Ω_eff)
E²_ΛCDM(z)  = Ω_L(1+z)³ + Ω_r(1+z)⁴ + (1−Ω_L−Ω_r)
```

identical for `Ω_L = Ω_eff` and `Ω_r,L = Ω_r(1−Ω_eff)`, i.e. `h_L² = h²/(1−Ω_eff)`, i.e.

> **h = h_L √(1−Ω_m,L) ,   H0,model = H0,ΛCDM √(1−Ω_m,LCDM) = 0.835 H0,ΛCDM** (0.830 at the fit).

Every distance ratio is invariant because `D_M`, `D_H`, `r_d` and `r_*` all scale as `1/H0` at fixed
shape. The only non-invariant background quantities are **absolute lengths and `H0`**. Numerically, at
the ΛCDM best fit mapped through the identity (K5, K17):

| quantity | ΛCDM | model at the map | ratio |
|---|---|---|---|
| `E(z)` | — | — | `1 + 4.5×10⁻⁵` (the `Ω_r` inside `Λ`) |
| `r_d` | 147.41 Mpc | 177.02 Mpc | **1.2009** |
| `D_M/r_d`, `D_H/r_d` | — | — | max deviation **0.33%** |
| `R`, `l_A` | 1.7422, 301.390 | 1.7421, 300.652 | 0.006%, 0.25% |
| `χ²_SN` | 1389.31 | 1389.31 | `Δ = 0.005` |

The 0.33% is not physics: it is the `z_*`/`z_drag` fitting formulae, which receive `ω_m,eff` in the model
and `ω_m` in ΛCDM. The formulae are 1–2% accurate, so no significance attaches to it — the degeneracy is
exact at the level this data set can resolve.

**The physical content is one number:** at fixed physical densities the model's sound horizon is
`1/√(1−Ω_eff) = 1.20` times ΛCDM's, because `G_eff = G/(1+Ω_m)` slows the early expansion.
That single fact is what breaks the degeneracy once `H0` is fixed.

## 3. The data, computed properly

All three sets are on disk or are labelled external tables; every number below is in `a46_results.json`.

| set | points | content | source |
|---|---|---|---|
| BAO | **13** | BGS `D_V/r_d`; LRG1, LRG2, LRG3+ELG1, ELG2, QSO, Lya `D_M/r_d` **and** `D_H/r_d`, with per-tracer `D_M–D_H` correlations (−0.40 to −0.50) | DESI DR2, arXiv:2503.14738 Table 1 (identical to frozen lane CFG681) |
| SNe | **1580** | Pantheon+ `m_b_corr`, full STAT+SYS covariance, `M` marginalised analytically, `IS_CALIBRATOR=0`, `zHD>0.01` | `prep_2026/sne_lambda/pantheonplus_full.dat` sha `1cb0fc37…`, cov `1ddcdf8b…` |
| CMB | **3** | `R = 1.7502±0.0046`, `l_A = 301.471±0.0895` (⇒ `θ_* = π/l_A = 0.010421`), `Ω_b h² = 0.02236±0.00015`, 3×3 correlation (0.46, −0.66, −0.33) | Planck 2018 distance priors, Chen–Huang–Wang arXiv:1808.05724 Table I |

`r_d` and `r_*` are **computed in each model** (Hu–Sugiyama `z_*`, Eisenstein–Hu `z_drag`, calibrated once
so that the Planck point gives `z_* = 1089.92`, `z_d = 1059.94`, `r_d = 147.09`, `r_* = 144.43` — K15), never
assumed. The `Ω_b h²` point is part of the published compressed likelihood and is what BBN independently
measures; the 2-point variant `(θ_*, R)` is reported alongside so the reader can see how much of the
verdict rests on it.

## 4. Results

Both models have **three parameters** (`Ω_m`, `h`, `Ω_b h²`); the "H0 fixed" rows have two.

| fit | `Ω_m` | `h` | `Ω_b h²` | `χ²` | `Δχ²` | `ΔAIC` | dof | `χ²/dof` |
|---|---|---|---|---|---|---|---|---|
| ΛCDM, CMB 3pt | 0.30203 | 0.68418 | 0.02252 | **1404.65** | 0 | 0 | 1593 | 0.882 |
| **MODEL, CMB 3pt** | **0.43473** | **0.56772** | 0.02251 | **1404.07** | **−0.58** | **−0.58** | 1593 | 0.881 |
| MODEL, `H0 = 67.40` | 0.28051 | (0.674) | 0.02436 | **2153.98** | **+749.34** | **+747.34** | 1594 | 1.352 |
| ΛCDM, CMB 2pt | 0.31001 | 0.66466 | 0.01955 | 1401.40 | 0 | 0 | 1592 | — |
| MODEL, CMB 2pt | 0.44964 | 0.54992 | 0.01983 | 1401.46 | +0.06 | +0.06 | 1592 | — |
| MODEL, `H0 = 67.40`, 2pt | 0.37544 | (0.674) | 0.03892 | 1460.22 | **+58.82** | **+56.82** | 1593 | — |

Components (`BAO / SNe / CMB`):

| fit | BAO (13) | SNe (1580) | CMB (3) | CMB (2) |
|---|---|---|---|---|
| ΛCDM | 12.28 | 1389.31 | 3.06 | 0.66 |
| MODEL | 12.15 | 1389.13 | 2.79 | 0.70 |
| MODEL, `H0 = 67.40` | 495.05 | 1432.28 | 226.65 | 28.19 |

- **The model's best fit is the canonical footing, not the alt one.** `H0 = 56.77` (fit) / `57.16` (exact map),
  `Ω_m = 0.4347`, `Ω_m,eff = 0.3030`, `ω_b = 0.02251` — and
  `a0 = cH0/Z = 9.53×10⁻¹¹ m/s²` (fit) / `9.59×10⁻¹¹` (map). Against `9.3603e-11` (canonical): **+1.8%**;
  against `1.1312e-10` (A42): **−15.8%**; against A9's SPARC fit `1.1033e-10`: −13.6%.
- **At `H0 = 67.40` the fit is not close.** `R` is 14σ low (`−0.0645`), `l_A` 7σ low (`−0.649`),
  `Ω_b h²` 13σ high (`+0.00200`), the BAO `D_M/r_d` pulls run `+2.9` to `+9.2` (BGS `D_V` is −10.2, a shape
  mismatch of the compromise), and `r_d = 169.8 Mpc` where BAO needs 147.09. SNe: `+43` out of 1389.
- **Δχ² significance:** 58.8 → 7.7σ (1 dof); 749.3 → 27.4σ. ΔAIC gives the 2-parameter model its
  2-unit bonus (ΔAIC = +56.8 / +747.3), which changes nothing.

## 5. Verdict

**Is the minimal-vacuum cosmology excluded?** Not by the background data — **it is flat ΛCDM in different
units**, and no combination of BAO, SNe and CMB distance priors can tell them apart (`Δχ² = −0.58`,
`ΔAIC = −0.58`). A42's 10.3σ does not survive a correct comparison.

**Is *the theory* excluded?** Yes, on its own `a0` clause. The degeneracy is exact only if `H0` is allowed to
move: the data require `H0 = 57`, and `a0 = cH0/Z` then gives `9.5×10⁻¹¹`, not `1.1312×10⁻¹⁰`. Conversely,
holding `H0` at the value `a0 = 1.1312×10⁻¹⁰` demands costs **Δχ² = +58.8 (7.7σ)** even with the baryon
prior removed, and **+749.3 (27σ)** with it.

**Where does it fail?** In the **ruler**, not in the expansion rate. The shape of `H(z)` is untouched
(SNe `+43`); `r_d` is **15.5% too large** at `H0 = 67.40`, which shifts every `D_M/r_d`, `D_H/r_d` and
`θ_*` coherently. That is the `G_eff = G/(1+Ω_m)` signature: at fixed physical densities the model's early
expansion is slower, so its sound horizon is `20%` longer, and the only way to hide that is a lower `H0`.

**Which branch does the closure select — 67.4 or 77.3?** Neither as a prediction. The closure
`β = (2/3)Ω_m` with `Λ_bare = 3H0²/c²` is **flat by construction** (`Ω_k = 0`; `ρ_β` cancels the excess), and
on that branch `H0` is an input, fixed in A42 at 67.4 by the `a0` normalisation. The **77.33** number belongs
to the `β = 0` + matter + `Λ_bare = ρ_crit` branch (`Ω_k = −Ω_m = −0.3163`, K14), which does **not** satisfy
the closure (`β = 0 ≠ 0.211`) and is excluded by Planck+BAO at 167σ (A42 K22). So the closure selects the
flat branch; the data then fix its `H0` at **57**, not 67.4.

## 6. Checks (`a46_checks.py`, 17/17 PASS, exit 0, ≈15 s)

| id | proves | measured | threshold |
|---|---|---|---|
| K1 | `E²` from (F1), `β=2Ω_m/3`, `Λ=3H0²` (sympy) | residual 0 | 0 |
| K2 | `ρ_β/ρ_crit = −Ω_m` at `z=0` | −0.316300 | −Ω_m |
| K3 | `E(0)=1` with `β=2(Ω_m+Ω_r)/3` | 0 | 1e−14 |
| K4 | ΛCDM fit is sane | `χ²/dof = 0.880` | 1 ± 0.1 |
| K5 | degeneracy at the mapped point (4 ratios + SNe) | max 0.33%, `Δχ²_SN = 0.005` | 0.5% |
| K6 | `r_d` is 20% larger at the map | 1.2009 | > 1.15 |
| K17 | `E_model/E_ΛCDM − 1` at the map, `z∈[0,1200]` | 4.46e−5 | 2e−4 |
| K7 | `Δχ²(model − ΛCDM)`, 3 par each, CMB 2pt | +0.065 | < 5 |
| K8 | model `Ω_b h²`/Planck | 1.0069 | < 1.10 |
| K9 | `a0` from the best-fit `H0` vs alt | 0.842 | < 0.90 |
| K10 | `Δχ²` at `H0 = 67.40` (2pt / 3pt) | 58.8 / 749.3 | > 20 |
| K11 | at fixed `H0`, SNe `Δχ²` / BAO+CMB `Δχ²` | 0.061 | < 0.15 |
| K12 | `r_d` at the `a0` branch | 169.8 (1.155×) | > 1.05 |
| K13 | A42's `Ω_eff h²` vs `Ω_m h²` | 0.1092 vs 0.1437 | — |
| K14 | 77.33 = `β=0` + curvature branch | 77.328, `Ω_k=−0.3163` | 77.33 |
| K15 | `r_d`(ΛCDM fit) calibration | 147.41 | < 0.3% |
| K16 | `H0`(fit)/`H0`(map) = `H0√(1−Ω_m)` | 0.962 | < 6% |

K16's 3.8% is the honesty check on the degeneracy: the χ² is flat along the map direction, so the fit lands
anywhere in `H0 ∈ [55, 57.2]` with `Δχ² < 0.1`. The `H0` quoted above is 57.2 from the exact map and 56.8
from the 3pt fit (55.0 from the 2pt fit); all give `a0` 15–18% below `1.1312e-10`.

## 7. What this does not do

1. **No Boltzmann.** The CMB enters as the published distance prior `(R, l_A, Ω_b h²)`, not as a power
   spectrum. The model's full CMB would differ further: with `ω_b` and `ω_m` matched by the fit, its
   `H(z)` at recombination is 17% lower (`h = 0.568` against 0.684), which moves the photon-diffusion
   damping scale and the peak heights (`z_eq` is matched to 1%, so the peak *positions* are not the
   discriminator). The distance prior cannot see any of that; a real `C_L` calculation would almost
   certainly exclude it faster, not slower.
2. **No BBN.** `H ∝ √(1−Ω_m)` at `T ~ 1 MeV` with `ω_b` fixed changes `Y_p` and `D/H`. Not computed; it is
   the sharpest independent channel and it points the same way.
3. **No perturbations.** `G_eff = G/1.435` at fixed `E(z)` changes growth; A40's `f σ₈` should be redone at
   `Ω_m = 0.435`, `H0 = 57`.
4. **`z_*`, `z_drag` are fitting formulae**, one-point calibrated at Planck; 1–2% accuracy is the floor on
   the 0.33% residual and on any claim of a sub-percent breaking.
5. **No `w`, no curvature, no `Σm_ν`**; both models are the same 3-parameter family.
6. **Footings not pooled** (CFG960): the canonical and alt `a0` are compared, never averaged. The result is
   that the data select the canonical one — which is the opposite of what A42's chain was built to show.

## 8. Next

1. **Boltzmann run with `G_eff = G/(1+Ω_m)`.** This is the only way to turn the 7.7σ distance-prior result
   into a full CMB exclusion, and it is a one-afternoon job with a modified CLASS.
2. **BBN at `H/H_ΛCDM = 0.836`.** If `Y_p` and `D/H` move by more than the few-per-mille BBN errors, the
   model dies independently of cosmology.
3. **Growth at `(Ω_m, H0) = (0.435, 57)`** — the `σ₈` prediction is the third leg, and unlike the background
   it is not degenerate with ΛCDM.
