# A51 — κ measured: a joint fit with a real error bar, and why it does not decide ½

**Lane:** A51_kappa_measured · **Date:** 2026-10-21 · **Base:** `THEORY.md` P3/§3.6/§4,
`A9_lcdm_audit`, `A14_upsilon_free`, `A18_two_ratios`, `A42_minimal_vacuum`, `A44_no_edge`,
`A46_cosmology_fit`.
**Script:** `a51_checks.py` (17/17 PASS, exit 0, ~30 s cold) · **Output:** `a51.out` ·
**Data:** `a51_results.json`. Five mutations, each exit 1: `MUTATE.md`, `a51_MUTATE_*.out`.

## Claim

**κ = 0.371 ± 0.026 (stat) ± 0.116 (syst) = 0.371 ± 0.119.** In the theory's own convention
(`κ ≡ a0/(c√(Gρ_bare))`, `ρ_bare = ρ_DE/Ω_Λ = ρ_crit`, so `κ = a0√(8π/3)/(cH₀)` and
`κ = ½ ⇔ a0 = 1.1312×10⁻¹⁰ m/s²`):

- **½ is 1.09σ away.** It is *outside* the 1σ interval `[0.252, 0.490]`, *inside* 2σ and 3σ.
  It is admitted, not confirmed, and not excluded.
- **Statistically ½ is excluded at 4.9σ.** The whole distance between "excluded" and
  "admitted" is the error model, not the data. That is the lane's central finding.
- **The joint fit is dominated by one channel.** SPARC supplies all of the κ information
  (±9.4%). The cluster amplitude adds a 11.0% measurement that pulls κ up to 0.393, but only
  by marginalising `u` — and `u` was derived from the same amplitudes. **The KiDS lensing
  vector carries exactly zero information** (an exact `(M_b, a0)` degeneracy, proved on the
  real 60×60 covariance: χ² is constant to 6 digits over a factor 2.9 in a0). **The BAO+SNe+CMB
  vector is κ-blind** — κ does not enter `E(z)` at all (A62's identity `a₀/(cH₀) = 2κ/Z` is
  the only place it appears) — and supplies no `H₀` either: the framework's background is an
  *exact* reparametrisation of flat ΛCDM, and its own `h` is modelling-dependent (0.470 in
  this lane's fit, 0.568 in A46). So the `H₀` that converts a0 → κ is a **prior**, and κ
  inherits it in full (12.5% below).
- **The fit is not prior-dominated in the stellar mass.** Freeing `Υ` per galaxy multiplies
  the κ error bar by **14.1** (0.67% → 9.4%) and collapses the IMF lever from ×0.44 to ×1.05.
  A9's `κ ∝ Υ^-1.23` is a *fixed*-`Υ` statement and does not survive the free-`Υ` fit.
- **It is analysis-dominated instead.** Seven defensible weightings of the same 3375 points
  give κ from **0.325 to 0.495** (half-span 20.8%) — six times the bootstrap error. That is
  the systematic that sets the answer, and it is not a prior on κ.
- **κ = ½ is not empirically decidable.** At N = 1000 galaxies of SPARC quality,
  σ_stat(κ) = 0.0144: the gap to 0.4824 (the literal one-twelfth, `Z/12`) is **1.2σ**, and to
  0.4979 it is **0.15σ**. With the coherent floor included, 0.15σ and 0.02σ. Three sigma on
  0.4824 needs **6,023 galaxies with the current systematics** — and no N reaches it while the
  coherent floor (21% estimator, 16% distance, 12.5% H₀, 10% law) stands, because it does not
  shrink. **Only a derivation settles ½.**

## 1. What was assembled (K1)

| block | content | in the likelihood as |
|---|---|---|
| SPARC | 175 `*_rotmod.dat` on disk; **171** with ≥5 points; **3375** points; `σ² = errV² + (0.05V)²` | 171 free `Υ`, profiled |
| clusters | A18's MID amplitude pair (CFG687, 318 eRASS1×KiDS) → `R_req = 5.552 ± 0.427`; `u = 0.45 ± 0.03` | one Gaussian on `R_tot(a0)` |
| lensing | KiDS-1000 Brouwer+21 Fig. 3: 4 bins × 15 radii + **60×60 covariance** | A44's model; zero Fisher info (K8) |
| BAO | DESI DR2, 7 tracers / 13 numbers | `D_M/r_d`, `D_H/r_d`, `D_V/r_d` |
| SNe | Pantheon+ `m_b_corr`, **1580** after the standard mask, full stat+sys covariance | `M` marginalised analytically |
| CMB | Planck-2018 distance priors `(R, l_A, Ω_b h²)` + 3×3 correlation | Gaussian |

sha256: SPARC `469f4f556dc813b2`, KiDS `e2568b34578a4752`. Nothing downloaded.

**The likelihood is the record's, not a new one (K2).** At `a0 = 1.132×10⁻¹⁰`, fixed
`Υ = 0.5`, it returns χ²/dof = **6.8651** (THEORY §4: 6.87); at `a0 = 9.36×10⁻¹¹`, **6.6312**
(6.63); with one `Υ` per galaxy, **2.4714** (2.42 — the 2% is the `Υ` window: the record's
`[0.05,2.5]` gives 2.471, `[0.02,4.0]` gives 2.400). The zero-parameter number reproduces to
four digits, so nothing below is an artefact of a different likelihood.

## 2. κ and its two conventions (K3)

`κ_P3 = a0√(8π/3)/(cH₀)`, and `κ_P3(1.131204×10⁻¹⁰) = 0.500000000` by construction. The record
also quotes κ per `ρ_DE` (A9 D2, A14, `kappa_closure`): `κ_DE = κ_P3/√Ω_Λ`, i.e.
`κ_DE(1.1312×10⁻¹⁰) = 0.604254`. **The same a0 is κ = ½ in one convention and 0.604 in the
other — a 20.9% relabelling with no measurement in it.** Every number below is `κ_P3`; K16
converts the record's values and finds this is where most of the apparent scatter came from.

## 3. The SPARC fit (K4–K6b)

With one `Υ` per galaxy, profiling each on a 240-point grid over the record's window:

```
a0      = 8.0815e-11 m/s^2      chi2 = 7115.9 / 3204 dof = 2.2209
kappa   = 0.3572                (kappa_DE = 0.4317)
```

**The likelihood peaks 28.6% below the theory's footing.** That direction was already visible
in the record's own table (χ²/dof 2.21 at 9.36×10⁻¹¹ vs 2.42 at 1.132×10⁻¹⁰); this lane
locates the minimum.

**The error bar is where the lane turns.**

| | a0 | κ | note |
|---|---|---|---|
| Δχ² = 1 | — | **0.0040** (1.13% in a0) | χ²/dof = 2.2, so this is not the truth |
| block bootstrap, 171 galaxies, 200 draws | 8.08e-11 ± 9.4% | **0.0335** | 8.3× the formal error |
| per-galaxy a0 | median 8.45e-11, **0.455 dex** scatter | — | 0.455/√171 = 8.3% = the bootstrap |

So the bootstrap error *is* the galaxy-to-galaxy scatter, and the formal error is wrong by a
factor 8. That is the first sign that κ is not a 1% measurement.

**The estimator ensemble (K6b)** decides whether the systematic is 3% or 21%. The same 3375
points, six defensible weightings:

| estimator | a0 | κ |
|---|---|---|
| χ², free Υ, all 171, 5% floor (**primary**) | 8.0815e-11 | 0.3572 |
| χ², free Υ, `errV/V < 0.10` (141 galaxies) | 8.6630e-11 | 0.3829 |
| χ², free Υ, 10% floor | 7.3417e-11 | 0.3245 |
| χ², free Υ, 3% floor | 8.5464e-11 | 0.3778 |
| unweighted V-space, free Υ | 1.0258e-10 | 0.4534 |
| log-space, fixed Υ, `errV/V < 0.10` (= A9's estimator) | 1.1207e-10 | 0.4954 |
| log-space, fixed Υ, all 171 | 9.1168e-11 | 0.4030 |

**Span 0.325 → 0.495, half-span 20.8%.** A9's 1.1033×10⁻¹⁰ reproduces here at 1.1207×10⁻¹⁰
(1.6%), and it is the *top* of the ensemble. This half-span is the estimator systematic used
below — measured, not assumed.

## 4. The other three channels, and why they do not measure κ

**Clusters (K7).** A18's machinery reproduces its anchor exactly (`r_v = 1.6863 Mpc`,
`F = 3.7702`, `R_tot = 2.6179`). The sensitivity is `dlnR_tot/dlna0 = +0.928` — *positive*,
because a larger a0 raises `F` and pushes `r_v` out. Inverting `R_tot(a0) = u·R_req` with
`u = 0.45 ± 0.03`:

```
a0 = 8.900e-11 +- 11.0%      kappa = 0.3934 +- 0.0432
```

That is a 11% measurement, not a 1% one, and it is **circular**: `u` was fitted by A18 to the
same amplitudes, so the constraint returns the a0 at which `u` was defined. Its honest status
is an 11–20% upper bound on a0's precision from clusters, not an independent measurement.

**Lensing (K8).** A44's model is `ΔΣ(R) = (a0/G) f(R√(a0/GM_b)) + M_b/(πR²)`. Under
`(a0, M_b) → (λa0, λM_b)` the argument is invariant and every term scales by λ, so with `M_b`
profiled per bin χ² is *exactly* invariant. On the real KiDS points and the real 60×60
covariance:

```
chi2 = 1876.978816   for a0 = 6.552e-11, 9.360e-11, 1.217e-10, 1.872e-10   (lambda = 0.7,1,1.3,2)
```

**Zero Fisher information on a0, hence on κ** — an exact degeneracy, not a weak constraint.
A44 says the amplitude is degenerate with the profiled `M_b`; this shows it is degenerate
*including* the baryon point mass, for every a0. No future isolated-lensing stack of this type
measures κ either.

**Cosmology (K9).** The real vector (DESI DR2 BAO 7 tracers/13 numbers, Pantheon+ 1580 SNe
with the full stat+sys covariance, Planck distance priors) fits flat ΛCDM at `Ω_m = 0.3020`,
`h = 0.6842`, `Ω_b h² = 0.02252`, χ²/dof = 0.882. Fitted with the framework's own background
`E² = [1 + Ω_m(1+z)³ + Ω_r(1+z)⁴]/(1+Ω_m)` it gives `Ω_m = 0.4376`, `h = 0.4704`,
χ² = 1403.24 — **Δχ² = −1.40 against ΛCDM**, i.e. the branch is *not* excluded. That is
because it is an exact reparametrisation: `E_fw(z;Ω_m) = E_ΛCDM(z; Ω_m/(1+Ω_m))` (verified to
7×10⁻¹⁵ in the shape, and the 19 distance numbers agree with the ΛCDM fit to **0.25%**). A42's
"10.3σ" compared an expansion coefficient to a density and is withdrawn in the current
`THEORY.md`.

Two consequences, and they are the reason this channel cannot help. First, **κ does not enter
`E(z)`**: `a₀` and `Λ_bare` are both set by `ρ_bare`, and `Λ = 32πa₀²/c⁴` is *the definition* of
κ = ½ (A42 K6), so `dχ²/dκ = 0` identically. Second, the branch's `h` is not robust: this fit
returns 0.470, A46 reports 0.568 for the same data, and the difference is how radiation is
carried inside the `1/(1+Ω_m)` normalisation. **The distance data therefore supply neither κ
nor a trustworthy `H₀`**; the conversion factor is the prior bracket 56.8 / 67.4 / 73.0, and
that 12.5% half-span is in the budget below.

## 5. The joint posterior (K10)

Multiplying the four channel posteriors, with the per-galaxy `Υ` profiled and the cluster `u`
marginalised:

| channel | κ | σ |
|---|---|---|
| SPARC (bootstrap) | 0.3572 | 0.0335 |
| clusters (`u` marginalised) | 0.3934 | 0.0432 |
| lensing | — | ∞ (exact degeneracy) |
| BAO+SNe+CMB | — | ∞ on κ (κ-blind) |
| **joint, statistical** | **0.3708** | **0.0265** |
| **joint, + systematics** | **0.3708** | **0.1188** |

The product is verified two ways: a 200,000-draw Monte Carlo reweighting gives
`0.3711 ± 0.0274`. (Summing the *raw* χ²'s instead peaks at 0.3574 — at the SPARC value —
because the raw curvature is 8.3× tighter than the bootstrap; that is precisely the error the
bootstrap exists to avoid, and it is printed as a control.)

**Declared systematics** (fractional, added in quadrature): estimator 20.8% (measured, K6b),
distance zero point 16.1% (A14's coherent floor), `H₀` footing 12.5% (56.8/67.4/73.0), law
choice 10.0% (A14), `Υ` window 5.0% (K13 below). Total **31.2%**.

**Where ½ sits.** `(0.5 − 0.3708)/0.1188 = 1.09σ` → **outside 1σ, inside 2σ and 3σ**.
Statistically, `(0.5 − 0.3708)/0.0265 = 4.88σ`. The two statements differ by a factor 4 and
the difference is entirely the error model. The lane's answer to "is ½ excluded?" is therefore:
**not by any honest total error bar; yes by the formal one; and the formal one is wrong by a
factor 8 (K6).**

## 6. The prior controls (K11–K13)

**Flat prior κ ∈ [0.3, 1.0] (K11).** The prior spans `a0 ∈ [6.79e-11, 2.26e-10]`; the
Δχ² = 9 interval is `[7.80e-11, 8.39e-11]`, strictly interior and 5σ from both edges. Refitting
inside the prior moves κ by 5×10⁻¹⁰. **The κ prior is not truncating and is not what sets the
error bar.**

**Fixed vs free Υ (K12).**

| | a0 | κ | σ(κ) | χ²/dof | IMF leverage on κ |
|---|---|---|---|---|---|
| fixed `Υ = 0.5` | 9.4422e-11 | **0.4174** | 0.0028 (0.67%) | 6.63 | Υ 0.5→0.87: ×0.439 |
| one Υ per galaxy | 8.0815e-11 | **0.3572** | 0.0335 (9.4%) | 2.22 | Υ window 0.3–1.0 vs 0.01–5: ×1.050 |

**The error bar moves by 14.1×, and the IMF lever collapses by a factor 2.4.** This is the
answer to the task's question, and it is the opposite of the expected one:

> With `Υ` fixed, κ is prior-dominated by a factor ~60 — a 0.67% statistical error against a
> ×0.44 swing from Chabrier→Salpeter. A9's `dln a0/dln Υ = −1.23` is exactly this statement.
> **Freeing `Υ` per galaxy defeats it**: the window no longer matters (5%), because each galaxy
> finds its own M/L. The cost is that the error bar grows to 9.4%. The prior is not removed —
> it is *traded* for a 21% estimator systematic, which no stellar prior can touch.

The fixed-`Υ` value, κ = 0.4174, lands on A19's `κ_meas = 0.417 ± 0.095` to three digits — a
useful cross-check that the two pipelines are the same one.

**A `Υ` law instead of 171 `Υ`s (K13).** `Υ_i = Υ₀(V_flat,i/150)^α` gives
`Υ₀ = 0.423`, `α = +0.635`, `a0 = 1.0379e-10`, **κ = 0.4588**, and **χ²/dof = 5.40** — 2.4×
worse than the per-galaxy fit. It is not an equivalent analysis: a single power law cannot
absorb the per-galaxy M/L scatter, and it lands +28% high, on the edge of the declared
systematic. The per-galaxy freedom is doing real work and is what keeps the 9.4% honest.

## 7. The decisive output: what the next generation can and cannot do (K14–K15)

Scaling the bootstrap error as `σ ∝ N^-1/2` at fixed per-galaxy quality
(`σ_stat(κ) = 0.0939·√(171/N)·0.3708`):

```
N = 171   sigma_stat(kappa) = 0.0265   1/2 at 4.9 sigma (stat)
N = 1000  sigma_stat(kappa) = 0.0144   (3.9%)
```

| gap | value | separation at N=1000, stat only | with the coherent floor |
|---|---|---|---|
| ½ − 0.4824 (`Z/12`, the literal twelfth) | 0.01760 | **1.22σ** | **0.15σ** |
| ½ − 0.4979 | 0.00210 | **0.15σ** | **0.02σ** |

- 3σ on 0.4824 needs **N = 6,023** *with the systematics unchanged*.
- 3σ on 0.4979 needs **N = 423,036**.
- The coherent floor is **0.116 in κ (31%)**. Since `0.116 > 0.0176/3`, **no N reaches 3σ on
  0.4824 while that floor stands.** The floor is made of the estimator/error-model choice (21%),
  the distance zero point (16%), the `H₀` footing (12.5%) and the law choice (10%), none of
  which is a counting error.

**So: κ = ½ is not empirically decidable from rotation-curve data.** The next generation at
N = 1000 improves the *statistical* error to 3.9% and still cannot separate ½ from 0.4824 at
3σ — and in total it separates them at 0.15σ, i.e. not at all. 0.4979 is out of reach by two
orders of magnitude in N. **Only a derivation settles it**, which is exactly the status
`THEORY.md` §3.6 assigns it ("a UV problem, not an EFT problem").

## 8. Audit: every κ in the record, in one convention (K16)

| source | value | convention | → κ_P3 |
|---|---|---|---|
| CFG493 via A19 | 0.417 ± 0.095 | P3 | **0.417 ± 0.095** |
| BTFR (`kappa_closure`) | 0.465 ± 0.076 | DE | 0.385 ± 0.063 |
| distance-free (`kappa_closure`) | 0.551 ± 0.043 | DE | 0.456 ± 0.036 |
| A15 combined | 0.530 ± 0.037 | DE | **0.439 ± 0.031** |
| A14 Υ-free | 0.354 ± 0.106 | DE | 0.293 ± 0.088 |
| A9 free SPARC | 0.5893 / 0.4876 | DE / P3 | 0.4876 |

Two corrections fall out. First, **the "0.87σ from ½" is `(0.5−0.417)/0.095 = 0.874`** — one
measurement, the one with the *largest* error bar, quoted in P3 units. The record's own
combination (A15) is `0.4386 ± 0.0306` in P3 units, i.e. **2.01σ below ½**; naively combining
all seven gives 3.4σ (correlated, so an upper bound). Nothing in the record confirms ½.
Second, **four of the seven numbers are quoted per `ρ_DE` and would be 21% larger if read as
P3** — the 0.29–0.49 span is mostly that relabelling, not physics.

This lane's `0.371 ± 0.119` sits inside the record's own span and below its centre. The
independent fixed-`Υ` cross-check (0.4174 vs A19's 0.417) says the pipelines agree; the
difference between 0.417 and 0.371 is entirely the `Υ` prior.

## 9. Status

| item | status |
|---|---|
| the data vector (SPARC 171/3375, KiDS 4×15+cov, DESI DR2, Pantheon+ 1580, Planck priors) | **ASSEMBLED**, on disk, hashed (K1) |
| the likelihood is the record's | **VERIFIED** (K2: 6.8651 vs 6.87) |
| κ identity and the two conventions | **DERIVED** (K3: 0.500000 = 0.604254/√Ω_Λ) |
| SPARC κ | **NUMERICAL**: 0.3572, σ_stat 9.4%, χ²/dof 2.22 (K4–K6) |
| cluster channel | **NUMERICAL but circular**: κ = 0.393 ± 0.043, degenerate with `u` (K7) |
| lensing channel | **NO-GO**: exact `(M_b,a0)` degeneracy, zero Fisher information (K8) |
| cosmology channel | **κ-BLIND**; branch is an exact ΛCDM reparametrisation (Δχ² = −1.4), its `h` not robust, so `H₀` is a prior (K9) |
| joint κ | **κ = 0.371 ± 0.026 (stat) ± 0.116 (sys)** (K10) |
| ½ | **1.09σ away: outside 1σ, inside 2σ**; 4.9σ on the formal error alone |
| prior domination | **NO in Υ** (freeing it costs 14× and kills the IMF lever); **YES in the error model** (21% estimator half-span) |
| κ = ½ decidable? | **NO** — 0.4824 at 1.2σ (stat) / 0.15σ (total) at N=1000; needs 6,023 galaxies and a floor 6× smaller |

## 10. What this does not do

1. **It does not measure κ to sub-percent, and it says why nobody can.** The sub-percent
   precision exists only in the formal Δχ² = 1 error (0.40% in κ), which is 8.3× smaller than
   the galaxy scatter and 50× smaller than the estimator spread. Quoting it would be the exact
   error A9 and A14 warn against.
2. **It does not use the 318-cluster stack directly.** The cluster block enters as A18's
   derived `R_req = 5.552 ± 0.427` and `u = 0.45 ± 0.03`, which A18 computed from CFG687's
   four published amplitudes on `cfg687_percluster.npz`. Re-running the stack is a different
   lane; the circularity of `u` is flagged, not fixed.
3. **The `Υ` window is a prior.** `[0.05, 2.5]` is the record's own (L232/`theory_prediction`);
   `[0.3, 1.0]` (Chabrier–Salpeter) moves κ by 5%, `[0.001, 10]` by 5% the other way. That 5%
   is in the budget.
4. **`H₀` is prior-supplied.** The BAO+SNe+CMB vector measures `Ω_m` and the shape, but the
   framework's `E(z)` is an exact ΛCDM reparametrisation and the `h` it returns is
   modelling-dependent (0.470 here, 0.568 in A46). The 12.5% `H₀` term is therefore the prior
   bracket 56.8/67.4/73.0, not a measurement: the background cannot supply `H₀` to this lane.
5. **No correlated-error model for SPARC.** The 5% floor plus `errV` is the standard one; a
   full covariance (beam smearing, inclination, non-circular motion) is not on disk. That is
   part of why the estimator spread is 21%.
6. **It does not re-derive any theory result.** κ = ½ is an input; this lane measures it.

## 11. Next

1. **The only route to a smaller κ error is the error model, not more galaxies.** A likelihood
   with a fitted intrinsic scatter per galaxy (or a hierarchical `a0`-scatter parameter) would
   remove the 21% estimator ambiguity; until then N is not the binding constraint (K14).
2. **A coherent distance scale ≤ 2.5%** on ~200 gas-dominated dwarfs is the other half (A14
   K10). SPARC has four galaxies that satisfy both conditions.
3. **Do not quote κ without its convention.** The 0.29–0.49 record span is mostly `ρ_DE` vs
   `ρ_bare`; A9's own instruction ("report κ on both densities, always") is still unmet in
   half the record.
4. **The decisive test of ½ is not empirical.** At the precision the data can reach, ½, 0.4824
   and 0.4979 are the same number. The lane that matters is the one that derives κ — and
   `THEORY.md` §3.6 already proves that is a UV problem.
