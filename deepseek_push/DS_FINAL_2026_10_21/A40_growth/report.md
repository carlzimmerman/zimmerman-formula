# A40 — LINEAR GROWTH: f(z), σ8(z), and the two forks that decide them

**Lane:** A40_growth · **Date:** 2026-10-21 · **Base:** `THEORY.md`, `A33_master_action/MASTER_ACTION.md`,
`A4_ppn/report.md` (D7). **Script:** `a40_checks.py` (17/17 PASS, exit 0, 3.2 s) · **Output:** `a40.out` ·
**Data:** `a40_results.json`.

## Claim

The canonical law `g_N = g²/(g+a₀)` makes the gravitational response to a perturbation **algebraic**:
`dg/dg_N = (1+s)²/(4s)`, `s = √(1+4a₀/g_N)` — a function of the local Newtonian field and of nothing
else: no wavenumber, no derivative, no horizon scale. So the linear growth equation of the theory is
`δ'' + (2 + dlnH/dlna)δ' = (3/2)Ω_m(a)(G_eff/G)δ` with `G_eff/G ≡ dg/dg_N`, and it is **scale-free**:
every k obeys the same ODE, so `f(z)` is universal and `P(k)` changes only in amplitude. On the theory's
own β = 0 background (`Λ_bare = 3H₀²/c²`, `Ω_Λ,eff = 1`, `Ω_c = 0.2666`, `Ω_b = 0.0497`):
`f = (0.4546, 0.6972, 0.8348, 0.9052, 0.9420)` at `z = (0, 0.5, 1, 1.5, 2)`, **σ8(0) = 0.7619**;
against the 8-point fσ8 compilation on disk **χ² = 14.21/8** vs **7.85/8** for the ΛCDM control
(Δχ² = +6.36), with σ8 **6.0 % below** Planck-ΛCDM's 0.811. Two forks decide whether that is the
theory's answer at all. (i) The cold sector: the action resolves it in favour of the total-matter
source, which then **contradicts the baryon-only SPARC fits by 2.52×**. (ii) The reference field at
which `dg/dg_N` is evaluated: cosmic `cH(z)` (scale-free, 1.4 % boost) or the perturbation's own rms
field (**σ8 = 2.27**, excluded, and scale-dependent). Scale-independence is exact at fixed `g_N` and
**fails** under the amplitude closure. A third fork — `Ω_Λ,eff = 1`, `Ω_m = 0.3163` and `H(0) = H₀` are
over-determined — moves σ8 over `0.762 / 0.813 / 1.170`: the growth observable tests *which background
the theory means* more than it tests the law.

## 1. Derivation

`c = 1` in the algebra; `K = 4πG`; signature `(−+++)`; `' ≡ d/dlna`; `Φ_N` the Newtonian potential
(`Φ_N < 0` in a well); `ρ̄_m` the mean **total** matter density (b + c).
### 1.1 The response of the law (exact, no expansion)

```
g_N = g²/(g+a₀)   ⟺   g = (g_N/2)(1+s),   s ≡ √(1 + 4a₀/g_N) ≥ 1                 (1)
g = 2a₀/(s−1),      g_N = 4a₀/(s²−1)                                             (2)
dg/dg_N = (dg/ds)/(dg_N/ds) = (1+s)²/(4s) = (s+2+1/s)/4 = g²/[g_N(2g−g_N)]       (3)
dg/dg_N = 1 + ε² + O(ε³),      ε ≡ a₀/g_N                                        (4)
```

Both sides of (3) are rational in `s`, so the chain rule gives it with no expansion (sympy residuals
`0`, K1/K2; it is A4's D7 eq. 19). `s = 1` (`g_N ≫ a₀`) gives 1; `s ≫ 1` gives `s/4 = √(a₀/g_N)`. (4)
has **no linear term**, so `a₀ → 0` is an exact limit; `dg/dg_N` is strictly decreasing in `g_N`,
minimum 1 at `g_N = ∞`, divergent at `g_N = 0` (the deep-MOND cusp A4 K11 records; positive, integrable).

**`G_eff ≡ G·dg/dg_N`.** The field sourced by `g_N` is `g = ν g_N`, `ν = (1+s)/2`, so
`δg = (dg/dg_N)δg_N`: `(G, δρ)` enters exactly as `(G_eff, δρ)` does in Poisson. Since (3) has no `k`,
no `∂_i`, no `H`, **`G_eff/G` is a pure number at fixed local field** — scale-independent, whether the
source is baryons or total matter (§5 decides which). That is what "the law is algebraic" means.
### 1.2 The growth equation

Quasi-static, sub-horizon (`k ≫ aH`), total matter as one pressureless fluid with `δ_c = δ_b`
(adiabatic; the cold sector is collisionless with `σ_c = 8.33 km/s`, so it is dust here):

```
δ' = −θ ,                                            θ ≡ ∇·v/(aH)              (5)
θ' + (2 + dlnH/dlna) θ = (k²/a²H²) Φ_N                                         (6)
(k²/a²) Φ_N = −4πG ρ̄_m (G_eff/G) δ                                             (7)
δ'' + (2 + dlnH/dlna) δ' = (3/2) Ω_m(a) (G_eff/G) δ                            (8)
Ω_m(a) ≡ 8πGρ̄_m(a)/(3H²),   dlnH/dlna = −(3/2)Ω_m(a) − Ω_K(a)                  (9)
```

(5) continuity, (6) Euler with Hubble drag, (7) the modified Poisson equation — the only change from GR
is `G → G_eff`, because the response is algebraic and multiplies the source pointwise. (9) is exact for
dust + Λ + curvature; `Ω_K(a) ≡ Ω_K a⁻²/E²`, `Ω_K = 0` flat. Symbols: `δ` matter contrast, `θ` velocity
divergence in Hubble units, `a` scale factor, `H = ȧ/a`, `Ω_m(a)` total matter fraction,
`G_eff/G = dg/dg_N` from (3). Equation (8) is the equation the task names.

**What (8) is not.** Not a strict linearisation of the A33 action: about `P = 0`, `KW'(u)/u → 1` as
`u → 0`, so `P_i` is a slave of `∂_iΦ_N`, its charge `d = D·P` is slaved to `∇²Φ_N`, and at leading
order the charge cancels the source it was to add — the "zero-field k² runaway" the record already hit
(FP22 B0–B4; CFG `AUDIT_SIGMA8_2026-10-03/README.md`). (8) is the **quasi-static closure**: the exact
law applied to the perturbation — this lane's premise (`CONDITIONAL(closure)`).
### 1.3 Scale-independence: what is proved, what is not

`G_eff/G = F(g_N)` with no `k` ⇒ the coefficient of `δ` in (8) is k-free ⇒ `D(k,z) = D(z)` for all k at
a **fixed reference field**. If instead `g_N` is the perturbation's own field,
`g_N(R) ≈ (4πG/3)ρ̄_m δ_R R ∝ δ/k`, then `G_eff` becomes k- and amplitude-dependent and (8) is no longer
linear: `G_eff(0.05 h/Mpc)/G_eff(0.2 h/Mpc) = 0.630` (n_eff = −2.4 assumed, K13) — **30 % more boost on
5 h⁻¹ Mpc than on 20**, a *blue* distortion. "Scale-free" is a theorem about the law and a *choice*
about the reference field, not a theorem about the cosmology.
## 2. The theory's own background

A33 (F1) with `β = 0`, `Λ = Λ_bare = 3H₀²/c²`, `K = 4πG`, `ρ = ρ_b + ρ_c`:

```
6H² = 2Λ + 4Kρ  ⟹  H² = H₀² + (8πG/3)ρ  ⟹  E²(a) = Ω_Λ,eff + Ω_m a⁻³ = 1 + 0.3163 a⁻³     (10)
```

`E(0) = 1.1473` ⇒ the model's **present expansion rate is 77.33 km/s/Mpc** if `H₀ = 67.4` is the de
Sitter rate defining `Λ_bare`; equivalently `Ω_K = −Ω_m` (closed). `Ω_m(a=1) = 0.2403`. This literal
reading of "`Ω_Λ,eff = 1`" is used for every number below except §7. Inputs: `Ω_b = 0.0497`,
`Ω_c = 0.2666`, `a₀ = 1.132×10⁻¹⁰ m/s²` (THEORY.md P3).
## 3. Results

`G_eff/G` with the cosmic reference field `g_ref(a) = cH(a)` — the only background acceleration the
theory has, and the record's own convention (`glm53_push/L180`: "G_eff/G = ν(cH(z)/a₀)"):

| z | a | f(z) = dlnD/dlna | D(z) | σ8(z) | G_eff/G |
|---|---|---|---|---|---|
| 0.0 | 1.0000 | **0.4546** | 0.7409 | **0.7619** | 1.0140 |
| 0.5 | 0.6667 | **0.6972** | 0.5864 | 0.6030 | 1.0097 |
| 1.0 | 0.5000 | **0.8348** | 0.4698 | 0.4832 | 1.0062 |
| 1.5 | 0.4000 | **0.9052** | 0.3867 | 0.3977 | 1.0039 |
| 2.0 | 0.3333 | **0.9420** | 0.3267 | 0.3360 | 1.0026 |

`σ8(0) = 0.7619 = 0.811 × D_th(1)/D_ΛCDM(1) = 0.811 × 0.74085/0.78856`. The ΛCDM control at the same
`Ω_m` gives `f = (0.5283, 0.7620, 0.8773, 0.9316, 0.9588)`: the theory's `f` is **14.0 % lower at
z = 0** and 1.8 % lower at z = 2, so the signal is at low z where DESI DR2 has 1–2 % precision. The
boost is **1.4 % at z = 0**, 0.3 % at z = 2 — at `g_ref = cH ≈ 6.6 a₀` the universe is Newtonian by the
law's own standard. Sensitivities: 0.7615 (canonical `a₀ = 9.36e−11`, 0.06 %), 0.7836 (trace-average
response `(2ν+dg/dg_N)/3`, +2.9 %), 0.8132 (flat), 1.1695 (closed) — the background is the only large
one (**54 %**).
## 4. The data on disk, and the score

**fσ8** — eight points, `campaign_fresh_gravity/CFG4_cosmology.py` 85–88 with its bibliography: 6dFGS
(Beutler+2012), SDSS MGS (Howlett+2015), BOSS DR12 (Alam+2017), eBOSS DR16 LRG/ELG/QSO (Alam+2021).
`σ² = err²` (no correlation matrix on disk).

| z | fσ8 obs | σ | theory | pull | ΛCDM | pull |
|---|---|---|---|---|---|---|
| 0.067 | 0.423 | 0.055 | 0.364 | −1.07 | 0.447 | +0.43 |
| 0.15 | 0.530 | 0.160 | 0.383 | −0.92 | 0.464 | −0.41 |
| 0.38 | 0.497 | 0.045 | 0.414 | −1.84 | 0.488 | −0.20 |
| 0.51 | 0.458 | 0.038 | 0.421 | −0.98 | 0.489 | +0.81 |
| 0.61 | 0.436 | 0.034 | 0.422 | −0.42 | 0.485 | +1.45 |
| 0.70 | 0.473 | 0.041 | 0.420 | −1.29 | 0.480 | +0.16 |
| 0.85 | 0.315 | 0.095 | 0.413 | +1.04 | 0.467 | +1.60 |
| 1.48 | 0.462 | 0.045 | 0.362 | −2.23 | 0.397 | −1.45 |

**χ²(theory) = 14.21 for N = 8** (1.78/point); **χ²(ΛCDM control) = 7.85 for N = 8** (0.98/point).
Δχ² = **+6.36** at equal parameter count — disfavoured at ≈2.5σ (one effective dof). Every pull but one
is negative: the theory grows **too slowly**, both `f` and `σ8` below ΛCDM's.

**σ8/S8.** σ8(0) = **0.7619**, i.e. **0.0491 = 6.05 % below** Planck-ΛCDM's 0.811 (which is 8.2σ in
Planck's 0.006 bar, but that bar belongs to a ΛCDM fit; the honest statement is "6 % below, toward the
lensing surveys"). `S8 = σ8√(Ω_m/0.3)` has two defensible `Ω_m` here: with the Lagrangian
`Ω_m = 0.3163`, S8 = 0.7824 (KiDS-1000 0.759 ± 0.021 → **+1.11σ**, DES Y3 0.776 ± 0.017 → +0.37σ,
KiDS-Legacy 0.815 → −1.55σ, Planck 0.832 → −3.82σ); with the dynamical `Ω_m(a=1) = 0.2403`,
S8 = 0.6819 (−3.67, −5.53, −6.34, −11.54σ respectively). Observed values:
`campaign_fresh_gravity/CFG1_evidence_audit.py` L838. So with the Lagrangian `Ω_m` the theory sits
**between** KiDS-1000 and Planck, inside the S8 tension; with the dynamical `Ω_m` (which S8's
definition uses) it is **10 % low, 3.7σ from KiDS-1000**. The 15 % split between the two is §7 showing
up as an observable.
## 5. Fork 1 — does `dg/dg_N` already carry the cold sector?

The cold sector is `M_c = 5.3643 M_b` and it gravitates in F1, so it must be somewhere in the
perturbation equations. Three branches, same law, same background:

| branch | source in (8) | σ8(0) | f(0) | verdict |
|---|---|---|---|---|
| **S** total matter, one response | `(3/2)Ω_m(a)(dg/dg_N)δ` | **0.7619** | 0.4546 | the action's reading (§5.1) |
| **A** baryons only ("already carried") | `(3/2)Ω_b(a)(dg/dg_N)δ` | **0.0024** | 0.1312 | **excluded, 323× low** |
| **C** baryons boosted + cold Newtonian | `(3/2)[Ω_b(a)G_eff/G + Ω_c(a)]δ` | **0.7605** | 0.4526 | what the SPARC fits use |

**5.1 The action decides for S, and it is not double counting.** A33 §5's first integral is
`g = g_N + u`, `g_N = GM_src/r²`, from `(L)` differentiated with `(P-sph)` substituted. There `M_src` is
the lapse equation's source, `ρ_b + ρ_c` — **total matter**. So the law relates the total field to the
total Newtonian field; `g_N = G(M_b+M_c)/r²`, and `dg/dg_N` responds to a change of that total source.
Adding `ρ_cδ_c` on the right of (8) is therefore **not** double counting: the law contains only the
*sum*, and the cold sector's clustering is what `g_N` means. What *would* double count is adding the P
charge `d = D·P` on top of `dg/dg_N`; that is not done. Branch A ("already carried") is excluded at
**323×**: with only `Ω_b` in the source, matter-era growth is `δ ∝ a^0.30` instead of `a`,
σ8 = 0.0024.

**5.2 The price, stated.** Branch S is inconsistent with the baryon-only SPARC fits of THEORY.md §4:
with `M_src = 6.3643 M_b` the deep-MOND branch gives `g = √(a₀·6.3643 g_b) = 2.523√(a₀g_b)`, a factor
**2.52** above the fits' `√(a₀g_b)`. Both cannot be true: the record uses Branch C for galaxies and
Branch S's background (`Ω_c` in F1) without noticing they are different theories. In growth the two are
**degenerate** — `σ8(S)/σ8(C) = 1.0019` (0.19 %), the cold being 16 % of the source and unboosted — so
**the growth observable cannot settle this fork**; the galaxy normalisation must, and it says the first
integral and the SPARC fits disagree by 2.52×. That is a defect in the record, not in the data.
## 6. Fork 2 — the reference field (this one dominates)

`dg/dg_N` needs a `g_N`. On FRW the mean field is zero, so a reference must be named:

| closure | `g_ref` | `G_eff/G` at z=0 | σ8(0) | scale-free? |
|---|---|---|---|---|
| **cosmic** (used above) | `cH(z)` | 1.0140 | **0.7619** | yes, by construction |
| **amplitude** | `(4πG/3)ρ̄_m σ8(z) R₈` | 7.2–11.7 | **2.267** | no: `G_eff(0.05)/G_eff(0.2) = 0.63` |

`g_rms(8 h⁻¹Mpc, z=0) = 2.24×10⁻¹³ m/s² = 0.0020 a₀` — deep MOND. The amplitude closure is a nonlinear
ODE (`G_eff` depends on `σ8`); iterated to its fixed point it gives **σ8(0) = 2.267**, 2.8× the observed
value, `G_eff/G = 7.2` there — the failure L341/FP22 recorded for the chassis (σ8 = 18–27), milder only
because this background is more Λ-dominated. **The theory has no growth prediction until the reference
field is specified by the theory**, and it is not: the action gives the law at a point but says nothing
about which scale's field a linear mode uses. `CONDITIONAL(reference field)`; the closures differ by 3×
in σ8.
## 7. Fork 3 — the background is over-determined

`Ω_Λ,eff = 1`, `Ω_m = 0.3163` and `H(0) = H₀` cannot all hold with zero curvature. Three resolutions,
same growth equation (curvature enters the friction, eq. 9):

| reading | `Ω_Λ` | `Ω_K` | `H(0)` km/s/Mpc | σ8(0) | f(0) |
|---|---|---|---|---|---|
| literal (used above) | 1.0 | 0 | 77.33 | 0.7619 | 0.4546 |
| flat (`β`-stress cancels the excess) | 0.6837 | 0 | 67.40 | **0.8132** | 0.5317 |
| closed | 1.0 | −0.3163 | 67.40 | **1.1695** | 0.5441 |

The closed reading is excluded at tens of σ by σ8 (1.17 vs 0.811 ± 0.006). The flat reading is ΛCDM to
0.3 % — no distinct growth prediction. The literal reading predicts **H(0) = 77.3 km/s/Mpc** (the SH0ES
side of the Hubble tension, not the Planck side) and is the only one both distinct and not already
dead. It is a real, falsifiable background prediction, and it owns §3–§4.

## Status

**`CONDITIONAL(closure; reference field; background)` + `NUMERICAL`.** **DERIVED:** `dg/dg_N =
(1+s)²/(4s)` exactly; `G_eff = G dg/dg_N`; eq. (8); the `a₀ → 0` limit is exact (`1 + (a₀/g_N)² + …`)
and reproduces the ΛCDM growing mode to 1e-11; the response is k-free, so growth is scale-free *at fixed
`g_N`*. **NO-GO (conditional on the closure):** scale-independence does not survive the amplitude
closure (σ8 = 2.27, `G_eff` running 30 %), and the theory does not specify the reference field, so its
growth is not a prediction until it does. **NUMERICAL:** `f(z)`, σ8(0), χ² = 14.21/8, the branch tables.

## Checks (`a40_checks.py`, 17/17 PASS, exit 0, 3.2 s)

**Law and response.** K1 `g_N = g²/(g+a₀)` inverts exactly (residual 0). K2 `dg/dg_N = (1+s)²/(4s) =
g²/(g_N(2g−g_N))` (residuals 0, 0). K2b the coded response equals the finite difference of the coded law,
60 points over 6 decades (2.9e-10). K3 response ∈ [1, ∞), strictly decreasing in `g_N` (min 1, sign −1).
K4 no `k` in the response (`k ∉ free_symbols`). **Background and LCDM limit.** K5 `E²(0) = 1+Ω_m`,
`H(0) = 77.33` (exact). K6 `a₀ → 0` reproduces the exact integral growing mode (0.788559 vs 0.788559).
K7 LCDM control `f(0) = 0.52833` vs the integral solution 0.52833. K8 `f(z)` monotone and `< 1` (5/5).
K9 DOP853 vs LSODA agree to 3.2e-11. **Forks.** K10 branches S/A differ by 322.8. K11 `M_src = M_b+M_c`,
`M_c/M_ph = 0.207`, deep-MOND ratio 2.523. K12 amplitude closure drives σ8 to 2.267 (> 1.5, i.e. 1.8×
the observed band). K13 amplitude closure not scale-free (ratio 0.630). **Data.** K14 χ² arithmetic
verified twice, LCDM control sane (14.211 / 7.846). K15 σ8 6.05 % below Planck, S8(dyn) 3.7σ below
KiDS-1000. K16 the background over-determination is not degenerate in σ8 (0.762 / 0.813 / 1.170).
Mutations: `quad` breaks K2b (19 % off the derivative), `nocold` breaks K15 (σ8 = 0.0024), `bgflat`
breaks K5 — see `MUTATE.md`.
## What this does not do

- **It is not a linearisation of the action.** §1.2: the strict system about `P = 0` is degenerate and
  ill-posed. (8) is a closure; deriving it from the action is the missing piece and it is not small.
- **No transfer function, no CMB.** σ8(0) is anchored to Planck's `A_s` through a ΛCDM transfer at
  `z ≳ 10`, where the theory's only extra scale (`λ_P = 17 pc`) is 10⁹ times below the horizon, so the
  transfer is unchanged to any accuracy resolvable here — but "same `A_s` ⇒ same σ8 at z = 10" is an
  assumption, not a computation.
- **No scale dependence, no nonlinearities**: `D(k,z) = D(z)` by construction (K13 measures how badly
  that fails under the amplitude closure but does not integrate a scale-dependent `P(k)`); no halo
  model, no shear `S8` likelihood. **fσ8 are ΛCDM-fiducial**: AP/RSD modelling assumes a fiducial cosmology, and a 1.147× `H(0)` shifts
  the AP conversion by a few per cent — the size of the effect being measured. Not corrected.
- **The cold-sector fork is not resolved for galaxies** — only shown degenerate in growth and
  contradictory (2.52×) between A33 §5 and the SPARC fits.

## Next

1. **DESI DR2 fσ8 at z < 0.6** decides §7: `f(0) = 0.455` (literal) vs `0.532` (flat) is a 14 %
   difference against a 1–2 % error, a 7–14σ discriminant with no free parameters. It tests the
   *background*, not the law.
2. **The galaxy sector must settle S vs C**: 2.523× in the deep-MOND amplitude is not a correction; one
   of A33 §5's first integral or the SPARC fits is wrong, and growth cannot see it.
3. **Derive the closure** and **specify the reference field**: until both, every number here is
   conditional, and `cH(z)` vs the rms field differ by 3× in σ8.
