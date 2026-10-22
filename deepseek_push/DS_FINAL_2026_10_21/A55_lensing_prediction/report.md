# A55 — lensing computed, not assumed

> ## ⚠️ ERRATUM (2026-10-22, A70 evidence re-audit) — the "factor 1.28 / 4.9σ" is an arithmetic artifact
>
> The headline below converts the Einstein-radius shortfall into a mass boost with `1/median²`, i.e. it
> assumes `M₂D ∝ R²`. The model's actual response, computed by finite-differencing this lane's own
> lens-equation solver, is **`dlnR/dlnB = 0.7775`**; root-finding the lens equation gives
> **`B = 1.174 ± 0.039 ×` Salpeter**, not 1.283 (the response route reproduces it to 10⁻⁴). At 1.174 the
> required IMF normalisation sits **1.80σ** from the same survey's dynamical calibration (Treu+2010,
> `1.00 ± 0.036` dex, 95 % `[0.850, 1.177]`) — **inside the 95 % bound by 0.25 %**, not outside it. With
> this lane's 1.283 it would have been outside at ~3σ, so the arithmetic error is the difference between
> "allowed" and "excluded".
>
> Also corrected: `R_E` is **model-derived** (SIE fit) and the catalogue carries no `R_E` error column —
> the 2 % used here is an assumption, and two independent pipelines scatter by 6.9 %; with the real scatter
> χ²/dof falls 6.21 → **4.20**, so a real residual survives but is much weaker. The failure is **mostly
> amplitude**: at fixed amplitude the density slope matches Etherington+2022 (`Δγ = +0.012 ± 0.039`), and
> the σ-residual flattens with the measured IMF(σ) trend. One shape term survives at **2.9σ**:
> `R_E/R_e = +0.172 ± 0.060`, inner lenses `0.216` dex low, degenerate with the assumed Sérsic `n = 4`.
> Lensing does **not** measure `a₀`: with the IMF free, `Δχ² = 0.26` over `κ ∈ [0.20, 0.80]`.
>
> **Corrected verdict: 1.8σ, at the 95 % edge of the same survey's IMF calibration — not a 4.9σ
> falsification.** See `A70_slacs_audit/report.md` (25/25 checks, 12/12 mutations exit 1).

**Lane:** A55_lensing_prediction · **Date:** 2026-10-21 · **Base:** `deepseek_push/DS_FINAL_2026_10_21`
**Script:** `a55_checks.py` (25/25 PASS, exit 0) · **Output:** `a55.out` · **Data:** `a55_results.json`
**Frozen inputs (read, not re-derived):** `THEORY.md` §3.5; `A3_lensing_gw/report.md` §2; `A12_slip_theorem/report.md`;
`A18_two_ratios/report.md` identity I. Data: `real_research/data/slacs_auger2009_lenses.tsv` (Auger+2009, SLACS IX,
VizieR J/ApJ/705/1099).

---

## 0. Claim, in four numbers

1. **The deflection is the dynamical prediction, and the correction is derived rather than assumed.**
   For a spherical lens `α(b) = (2/c²)∫∇⊥(Φ+Ψ)dl`. The P-sector's traceless spatial stress is `O(ε²)`, so `Φ = Ψ` at
   `O(ε)` and `α = (4/c²)∫∇⊥Ψ dl = α_dyn` **exactly at the order the potentials are defined**. The first correction is
   `δα/α = −c_n Ψ(R)`, with `c_n = B(2n+1)/B(n+1)`, `B(m) = ∫₁^∞ u^{-m}du/√(u²−1)`, `c_n ∈ [0.750, 0.835]` for slopes
   between `r^{-1/2}` and `r^{-2}`. **`δα/α = 2.31×10⁻⁶` for a galaxy-scale lens, `5.01×10⁻⁵` for a cluster.**

2. **On 70 SLACS lenses, at the theory's own `a₀ = 1.132×10⁻¹⁰` and Salpeter baryons, the zero-parameter prediction is
   `R_E,pred/R_E,obs = 0.885`** — 12 % short, **4.9σ**, `χ²/dof = 6.21`, median lens `R_E = 4.07 kpc`, `θ_E = 1.21"`.
   With Chabrier: `0.553` (20.2σ). Both IMF branches are reported; neither is fitted.

3. **The sharp test is the amplitude, and it is already possible.** The missing deflection is **0.176" on 1.21"**, 7.3×
   the 2 % SLACS error. The *shape* is not a discriminator: at fixed `θ_E` the phantom and an NFW halo have the same
   logarithmic slope to 0.013 at `R_E` and differ by 0.17 only at `30 R_E` (0.08 Mpc), while the radial image moves
   by 0.7 %. The *slip* is
   `2.8×10⁻⁶` arcsec, 8600× below the measurement error, and no planned survey reaches it.

4. **Verdict: the zero-parameter lensing gate FAILS, in the amplitude.** The deficit is a uniform `0.108 dex`
   (`1.28×`) mass shortfall inside `R_E`, not a profile-shape error. It is absorbed exactly by one number,
   `M_*/L = 1.28 × Salpeter`, which is inside the observed IMF band for massive ellipticals. So the theory **passes
   lensing only with a fitted mass-to-light ratio** — the freedom the gate was supposed to do without.

---

## 1. Conventions

`c = 1` in the theory algebra, SI in the numbers. `K = 4πG` for the printed action (`R3/(4K)`; A3 §1). Metric
`ds² = −(1−2Ψ)dt² + (1+2Φ)dx²` with `Ψ, Φ` the **positive well depths** — the standard lensing convention, in which a
point mass has `α = 4GM/(bc²)` and the SIS has `α = 4πσ²/c²`. Both are recovered exactly (K2, K3), which is what fixes
the convention and the factor 2.

Cosmology: Auger's own flat ΛCDM (`Ω_m = 0.3`, `Ω_Λ = 0.7`, `h = 0.7`), because `R_E` and `M_E` are tabulated in it;
`M_E` is reproduced from `θ_E, z_l, z_s` to 0.0008 ± 0.0032 dex (K8), so the geometry is not a source of error.

---

## 2. Task 1 — the derivation

### 2.1 The lens, in a two-potential metric

For a static, spherically symmetric lens the deflection of a light ray at impact parameter `b` is

```
α(b) = (2/c²) ∫ ∇⊥(Φ+Ψ) dl = (4/c²) ∫_b^∞ g_eff(r) dr/√(r²−b²),
```

with `g_eff = dΨ_eff/dr` and `Ψ_eff ≡ (Φ+Ψ)/2`. (K2: point mass to `1.6×10⁻¹³`; K3: SIS to `6.4×10⁻⁷`,
impact-parameter-independent as it must be.) The convergence is the usual `κ = Σ_tot/Σ_cr`, `Σ_cr = c²D_s/(4πG D_lD_ls)`,
and the Einstein radius solves the mean-convergence condition

```
κ̄(<R_E) = 1   ⟺   M_2D(<R_E) = π R_E² Σ_cr,      M_2D(<R) = (R²/G) ∫_R^∞ g dr/√(r²−R²).
```

The second form is exact for a spherical lens, needs only the *acceleration* (no numerical differentiation of a density),
and is cross-checked against a direct line-of-sight integral of `ρ_tot` at `1.4×10⁻⁴` (K4c).

### 2.2 Why the deflection equals the dynamical prediction

The action's extra sector is a **charge** sector at leading order (A12, A3): exactly one `O(ε)` lapse source, the clock
term, and every traceless stress is a product of two first-order objects, hence `O(ε²)`. The slip lemma
`G^i_j − ⅓δ^i_jG^k_k = (∂^i∂_j − ⅓δ^i_j∇²)(Φ−Ψ)` — verified symbolically to a zero residual over all nine components
(K1) — then gives `Φ = Ψ` at `O(ε)`. With `Φ = Ψ`, `Ψ_eff = Ψ` and the lensing mass is the *dynamical* mass:

```
M_tot(<r) = M_b(<r)[1 + F(y)],   F(y) = ½(√(1+4/y) − 1),   y = G M_b(<r)/(a₀ r²),
```

which is exact at every radius (K4, residual `3.7×10⁻¹⁶`) and whose phantom density
`ρ_ph = (1/4πr²) d(M_bF)/dr = (1/4πGr²) d[r²(g−g_N)]/dr` agrees between the two routes to `7.6×10⁻¹⁰` (K4b).

**So the lensing prediction is not a new assumption**: it is the law, projected. The only place the theory can differ
from "lensing = dynamics" is the `O(ε²)` slip of §2.3.

### 2.3 The correction, exactly

Write `Φ = Ψ(1+δ)`, `δ = (Φ−Ψ)/Ψ = O(Ψ)`. Then `Ψ_eff = Ψ(1+δ/2)` and

```
δα/α = [∫∇⊥(Ψδ) dl] / [2∫∇⊥Ψ dl] = −⟨Ψ⟩_g + O(Ψ²),
```

where `⟨Ψ⟩_g` is the `g`-weighted mean of the potential depth along the line of sight. For a power-law profile
`Ψ = A r^{−n}` the integral is elementary and the `O(1)` coefficient is exact:

```
δα/α = −c_n Ψ(R),     c_n = B(2n+1)/B(n+1).
```

| n (profile) | 0.5 | 1.0 | 1.5 | 2.0 |
|---|---|---|---|---|
| `c_n` | 0.8346 | **0.7854** (=π/4) | 0.7628 | 0.7500 |

K6 confirms these against the full line-of-sight integral to `2.5×10⁻¹⁰`. The sign is fixed by A12's result
`1 − Φ/Ψ = −Ψ` (i.e. `δ = −Ψ`): the correction **suppresses** the deflection. With `δ = −Ψ`,
`Ψ_eff = Ψ(1 − Ψ/2) = Ψ − Ψ²/2 < Ψ` — the same mass produces a slightly shallower lensing potential than it does a
Newtonian force, which is the same statement as `γ_PPN < 1`.

The first integral of the slip ODE, `f′ = −3K r ∫_r^∞ Π/r′ dr′`, satisfies `(f′/r)′ = 3KΠ` to `5×10⁻⁹` (K5).

### 2.4 Size of the correction

`Ψ(R_E) = GM_2D(<R_E)/(R_E c²)`, and `α = 4GM_2D/(R_E c²) = 4Ψ`, so the potential depth is a quarter of the
(deflection in radians). Numerically:

| lens | `R_E` | `M_2D(<R_E)` | `Ψ(R_E)` | `δα/α` | `α` | `δα` |
|---|---|---|---|---|---|---|
| SLACS-like galaxy | 4.07 kpc | `2.5×10¹¹ M⊙` | `2.94×10⁻⁶` | **`2.31×10⁻⁶`** | 2.43" | `5.6×10⁻⁶`" |
| massive cluster | 150 kpc | `2.0×10¹⁴ M⊙` | `6.38×10⁻⁵` | **`5.01×10⁻⁵`** | 52.6" | `2.6×10⁻³`" |

**So: 2.3 parts per million for a galaxy, 50 ppm for a cluster.** The cluster number is 22× the galaxy number
because `Ψ ∝ M/R` and the cluster's `M/R` is 22× larger (800× the mass inside 37× the radius).

### 2.5 Two discrepancies found in the upstream lanes (recorded, not fixed there)

1. **A12's slip coefficient.** A12 writes `f″ − f′/r = 2KΠ` and hence `f′ = −2K r∫Π/r′`. The chain is
   `(2/3)(f″−f′/r) = 2KΠ ⇒ f″−f′/r = 3KΠ ⇒ f′ = −3K r∫Π/r′` — a factor 1.5. K1 verifies the trace-free identity
   exactly and K5 verifies the `3K` first integral; the `2K` version fails K5. The coefficient multiplies an `O(1)`
   number, so **no conclusion in A3 or A12 changes**, but the slip values in A12's table should be read as
   order-of-magnitude (its `−9.13×10⁻⁸` at 10 kpc is not reproducible from either coefficient together with its own
   `|1−Φ/Ψ| = 2.6×10⁻⁷`).
2. **The `2.63×10⁻⁷` headline is not the SLACS number.** That figure is for an MW-like model (`v_c ≈ 200 km/s`,
   `a₀ = 9.36×10⁻¹¹`). SLACS lenses are deeper (`σ = 241 km/s` median), so `Ψ(R_E) = 2.9×10⁻⁶` — **ten times larger**.
   The lensing correction quoted in `THEORY.md` §3.5 is therefore an underestimate of the *observable* correction at
   the accelerations where the lensing data actually live. It remains unobservable either way (§4.3).

---

## 3. Task 2 — SLACS, zero free parameters

### 3.1 Data

Auger+2009 (SLACS IX): 85 rows, **70 usable** (Einstein radius, Einstein mass, both stellar fractions, both stellar
masses, an effective radius). Median lens: `z_l = 0.1925`, `z_s = 0.6055`, `σ = 241 km/s`, `R_E = 4.07 kpc`,
`θ_E = 1.21"`. Stellar masses are SED estimates at a stated IMF; the `Re(V)`/`Re(I)` columns are in **arcsec** and are
converted with the lens angular-diameter distance (this is the one parsing trap in the file).

### 3.2 The model — nothing is fitted

For each lens:

1. `M_b(<r)`: spherical de Vaucouleurs (Sérsic `n = 4`), projected exactly via the incomplete gamma law, deprojected
   with the Prugniel–Simien gamma form. Normalised so that the **projected** stellar mass at the observed Einstein radius
   equals `f_* M_E` — i.e. the stellar mass inside `R_E` is Auger's *measured* one, not a model's.
2. `g_N = G M_b(<r)/r²`; `g = ½g_N(1+√(1+4a₀/g_N))` with **`a₀ = 1.132×10⁻¹⁰`** (the theory's P3 value, not fitted).
3. `M_tot(<r) = r²g/G`; project; solve `M_2D(<R) = πR²Σ_cr` for `R_E,pred`.
4. Compare with `R_E,obs`.

No per-lens parameter, no fitted `M/L`, no dark-matter profile. The two branches are the two **measured** IMF
normalisations (Salpeter `f_*`, Chabrier `f_*`). The reconstruction is self-consistent: the total stellar mass it
implies agrees with the tabulated SED mass at `+0.038 ± 0.038 dex` (K8b).

### 3.3 Results

| model | N | median `R_E,pred/R_E,obs` | `⟨ln⟩ ± sem` | significance | scatter | `χ²/dof` |
|---|---|---|---|---|---|---|
| **Salpeter, `a₀ = 1.132×10⁻¹⁰`** | 70 | **0.8852** | **−0.1245 ± 0.0255** | **4.9σ** | 0.093 dex | **6.21** |
| Chabrier, `a₀ = 1.132×10⁻¹⁰` | 70 | 0.5533 | −0.6048 ± 0.0299 | 20.2σ | 0.109 dex | 41.6 |
| Newton (baryons only) | 70 | 0.7536 | −0.2873 ± 0.0272 | 10.6σ | 0.099 dex | 13.0 |
| Salpeter, `a₀ = 9.3603×10⁻¹¹` (record footing) | 70 | 0.8664 | −0.1477 ± 0.0257 | 5.7σ | 0.093 dex | 6.91 |

`χ² = 428.2` for 69 dof in the headline row; 33 % of lenses land within 10 % of the measured radius.

### 3.4 Reading the table

- **The amplitude deficit is robust.** It does not depend on the footing (0.866 vs 0.885), on the light-profile index
  (`n = 3…6`: 0.877 → 0.893), on the line-of-sight cut (0.2 → 1000 Mpc: 0.879 → 0.885), or on the normalisation route
  (`f_*M_E` 0.885 vs tabulated total `M_*` 0.824, K13c). The range is **0.82–0.89**, always short.
- **The IMF is the dominant systematic, and it is the whole story.** Salpeter and Chabrier differ by 0.26 dex in
  `M_*`; the predicted `R_E` moves by 0.204 dex (0.885 → 0.553), because the projected light fraction at `R_E` is
  itself mass-dependent. The data sit between the two branches and closer to Salpeter: the required boost is
  `1.28 × Salpeter`.
- **The phantom helps, and is not enough.** Baryons alone give 0.754; adding the law's phantom lifts it to 0.885, closing
  53 % of the Newtonian radius gap. The remaining 47 % is what one fitted `M/L` buys.
- **There is excess per-lens scatter.** After removing the mean offset the model still scatters by 0.093 dex against
  0.045 dex of propagated error (`χ²/dof = 4.6`, K13b). That is not a radial-shape error (the shape agrees, §4.2); it is
  lens-to-lens variation in `M_*/L` and light-profile shape that the theory does not predict. **The theory is not a
  per-lens predictor at better than ~20 %.**

---

## 4. Task 3 — the sharp test against GR + dark matter

The theory's lensing mass is fixed by baryons and `a₀`; GR+DM fits an NFW halo. Three possible discriminators, in
decreasing order of usability:

### 4.1 Amplitude — sharp, and already measured

For the median SLACS lens the theory under-predicts the deflection by **0.176" on 1.21" (14.5 %)**. The 2 % SLACS
error is 0.024", so the difference is **7.3× the measurement error** (at a 5 % error it is still 2.9×, so the
conclusion does not rest on the error model). GR+DM matches `θ_E` by construction (it has
`M_200`, `c`). **Precision needed: `δθ_E/θ_E ≲ 7 %`; SLACS has 2 %; the test is possible now, and it fails.**
(Euclid/Roman will push `θ_E` errors to <1 % on ≳10⁵ lenses, which makes the amplitude test per-mass-bin rather than
per-lens — but it cannot change the sign of a 15 % deficit.)

### 4.2 Shape at fixed `θ_E` — degenerate, and this is the honest surprise

With both models normalised to the *same* `θ_E`, at a representative SLACS lens (`z_l = 0.19`, `z_s = 0.90`,
`θ_E = 0.865"`):

| `dlnM_2D/dlnR` at | `R_E` | `3R_E` | `10R_E` | `30R_E` |
|---|---|---|---|---|
| theory (stars + phantom) | 0.966 | 0.909 | 0.931 | 0.958 |
| stars + NFW (`c = 10`) | 0.979 | 0.942 | 0.945 | 0.788 |

The radial critical curve moves from 490 to 503 pc (2.7 %) and the radial image (source at half the caustic depth)
from 1800 to 1786 pc — **0.7 %**. **Over 1–10 `R_E` the MOND phantom (`ρ ∝ r^{-2}`) and an NFW halo are
shape-degenerate** — the slopes agree to 0.04, because both are approximately isothermal over exactly the range a
single Einstein radius measures. The difference appears only at ~30 `R_E` (0.08 Mpc here), where the phantom is still
isothermal (0.958) and the NFW is turning over (0.788). A shape test therefore needs `δ(dlnM/dlnR) ≲ 0.08` at
`0.05–0.3 Mpc`, i.e. stacked shear at ~5 % per radial bin over a decade in radius: **the KiDS-1000 stack used in A44
(4×15 bins, 0.035–2.6 Mpc), DES-Y3 and Euclid/LSST wide stacks have that; a single Einstein radius does not.** So the
shape is not where this theory dies — but it is where the next real test lives.

### 4.3 The slip — invisible, and it will stay invisible

`Δθ_E/θ_E = δα/α = −2.31×10⁻⁶`, i.e. **`2.8×10⁻⁶` arcsec on a 1.2" lens** — 8600× below the 2 % error, and 10⁴× below
the ~10 mas astrometric floor of any optical survey. Seeing it needs `10⁻⁶` *relative* astrometry. **No existing or
planned survey does this; the test is not "not yet possible", it is not possible with lensing at all.** The slip is
constrained far better by Solar-System PPN (`γ−1 = (1.7±1.6)×10⁻⁴`, A12), which the theory passes with a 10⁻⁹
prediction at Saturn.

### 4.4 Summary of the three

| discriminator | size | needed precision | available | verdict |
|---|---|---|---|---|
| amplitude `θ_E` | 14.5 % | ≲7 % | 2 % (SLACS) | **possible now — fails** |
| shape `dlnM/dlnR` | 0.17 at 30 `R_E` | ≲0.08 at 0.05–0.3 Mpc | ~0.02–0.05 (KiDS stacks) | marginal; not decisive |
| slip | `2.3×10⁻⁶` | `10⁻⁶` astrometry | none | **not possible** |

---

## 5. Task 4 — verdict

**The zero-parameter lensing gate FAILS.**

- **By how much:** `R_E,pred/R_E,obs = 0.885` at Salpeter and `a₀ = 1.132×10⁻¹⁰`; the radius is 11.5 % short, the mass
  inside `R_E` is `0.108 dex` low (a factor 1.28), at **4.9σ** on 70 lenses. At Chabrier it is 45 % short (20.2σ).
- **Amplitude or shape:** **amplitude.** The failure is a uniform mass normalisation: the logarithmic slope of the
  lensing mass profile agrees with an NFW fit to 0.013 at `R_E`, and the radial image position to 0.7 %. The theory
  gets the *shape* right and the *amount* wrong.
- **What would fix it:** one number per population, `M_*/L = 1.28 × Salpeter`. That is inside the observed range for
  massive ellipticals (bottom-heavy IMFs are measured at 1.2–2× Salpeter), so the theory is **not excluded** — but the
  gate it claimed to pass without a fitted `M/L` is passed only *with* one. That is the same status as ΛCDM's NFW fit,
  which is the thing the claim was supposed to beat.
- **The secondary tension:** the model's per-lens scatter (0.093 dex) is twice its propagated error, so even with a
  fitted normalisation it is not a 10 %-level per-lens predictor.

**One-line verdict:** lensing = dynamics is *derived* and holds to `2×10⁻⁶`; but the derived lensing mass is 22 % too
small at SLACS accelerations, so the gate fails on amplitude by 4.9σ and passes only by spending one fitted `M/L`.

---

## 6. Checks (`a55_checks.py`, 25/25 PASS, exit 0, 2 s)

| id | what it proves | measured |
|---|---|---|
| K1 | trace-free Einstein identity `G^i_j − ⅓δ^i_jG^k_k = (∂^i∂_j − ⅓δ^i_j∇²)(Φ−Ψ)`, exact symbolic | residual 0 |
| K2 | deflection functional reproduces the point mass `4GM/(bc²)` | `1.6×10⁻¹³` |
| K3 | deflection functional reproduces the SIS `4πσ²/c²`, `b`-independent | `6.4×10⁻⁷` |
| K4 | law identity `M_tot = M_b[1+F(y)]` exact at every `r` | `3.7×10⁻¹⁶` |
| K4b | phantom density from `d(M_bF)/dr` = from `d[r²(g−g_N)]/dr` | `7.6×10⁻¹⁰` |
| K4c | projected mass: `g`-integral route = direct LOS integral of `ρ_tot` | `1.4×10⁻⁴` |
| K5 | slip first integral satisfies `(f′/r)′ = 3KΠ` (A12's `2K` fails this) | `5×10⁻⁹` |
| K6 | `δα/α = −c_nΨ`, `c_n = B(2n+1)/B(n+1)`, from the full LOS integral | `2.5×10⁻¹⁰` |
| K7 | correction size: 1–10 ppm (galaxy), 10–100 ppm (cluster) | `2.31×10⁻⁶` / `5.01×10⁻⁵` |
| K8 | `M_E` from `θ_E, z_l, z_s` reproduces Auger's mass | `0.0008 ± 0.0032` dex |
| K8b | `f_*M_E/(light fraction)` matches the SED `M_*` | `+0.038 ± 0.038` dex |
| K9 | headline: Salpeter zero-parameter `R_E` short by 10–16 %, >4σ | 0.8852, 4.9σ |
| K10 | Chabrier fails far harder | 0.5533, 20.2σ |
| K11 | baryons-only is worse; the phantom closes part of the gap | 0.754 → 0.885 (53 %) |
| K12 | the record's canonical footing gives the same verdict | 0.8664 |
| K13 | `χ²` with per-lens errors rejects the zero-parameter model | `χ²/dof = 6.21` |
| K13b | excess per-lens scatter after removing the offset | 0.093 vs 0.045 dex |
| K13c | normalisation-route independence (tabulated `M_*`) | 0.824, 7.5σ |
| K14 | the estimator is sensitive to `a₀` (`×100` over-predicts) | 5.32 |
| K15 | light-profile systematic `n = 3…6` | 0.877 → 0.893 |
| K16 | line-of-sight cut 0.2 / 0.5 / 1000 Mpc | 0.879 → 0.885 |
| K17 | shape at fixed `θ_E`: degenerate at `R_E`, discriminating at ~30 `R_E` | Δslope 0.013 → 0.17, image 0.7 % |
| K18 | the amplitude difference in arcsec vs the measurement error | 0.176" vs 0.024" |
| K19 | the slip correction to `θ_E` is unobservable | `2.8×10⁻⁶`" |
| K20 | the verdict is recorded and is reproducible | FAIL, amplitude, 4.9σ |

Mutations (`MUTATE.md`): `newton`, `chabrier`, `noproj`, `slipzero` — each exits 1 and breaks only its own group.

---

## 7. What this does not do

- **No cluster Einstein radii in the fit.** The cluster-scale numbers in §2.4 are a representative massive cluster, not a
  measured one; the cluster data on disk (A18 CFG686/687, A44 KiDS) are *stacked shear amplitudes and ESD profiles*, not
  Einstein radii, and forcing them into a `χ²` over `θ_E` would be a category error. A18's own numbers imply the cluster
  deficit is ~0.31 dex in mass — worse than the galaxy deficit, and in the same direction.
- **No EFE.** SLACS lenses sit in groups; an external field suppresses the phantom and would make the deficit *larger*.
  Ignoring it is the most generous choice available to the theory.
- **No gas.** The baryonic mass is stars only; quiescent ellipticals have <1 % gas, inside the quoted `M_*` errors.
- **The `M_*` normalisation uses the observed `R_E`.** That is how a measured `f_*` is defined; the alternative route
  (tabulated total `M_*`) is reported as K13c and gives the same verdict, 0.07 dex lower.
- **No per-lens Sérsic index.** The table has none; `n = 4` is assumed and the `n = 3…6` range is carried as a
  systematic (K15). This is the largest unmodelled systematic after the IMF and is the most likely origin of the excess
  scatter in K13b.
- **No cosmological-slip statement.** This lane covers the *static* lens; the `E²` term and an evolving `P̄` are outside
  it (as A12 says).

---

## 8. Next

1. **Do the cluster version properly**: take the four KiDS mass bins of A44 and ask what `R_E` the law predicts at
   `M_200 = 10^{13.5}–10^{14.5}`, then compare with the strong-lensing `θ_E`–`M_*` relation (Auger/LSAT). A18 already
   implies the cluster deficit is ~0.31 dex — if that holds, the amplitude failure is *worse* at cluster scales and the
   "one `M/L` fixes it" escape closes.
2. **Test the scatter prediction, not the mean.** The clean IMF-free statement is that the theory predicts *zero*
   intrinsic scatter in `R_E` at fixed `(M_b, R_e)`; the measured scatter is 0.093 dex. A homogeneous re-fit of the
   light profiles (Sérsic `n` free) would decide whether that scatter is astrophysical or a theory failure.
3. **Feed the `2.3×10⁻⁶` back into `THEORY.md` §3.5**: the observable slip at SLACS accelerations is 10× the quoted
   `2.63×10⁻⁷`, and the `2K`/`3K` coefficient in A12 should be corrected.