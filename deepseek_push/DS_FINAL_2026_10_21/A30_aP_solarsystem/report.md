# A30 — the `a_P` anomaly as a Solar-System prediction

**Lane:** A30_aP_solarsystem · **Date:** 2026-10-21 · **Base:** `BRIEF.md`, `FINAL_THEORY.md` §3, **A22 D4**
· **Script:** `a30_checks.py` (11/11 PASS, exit 0) · **Output:** `a30.out` · **Data:** `a30_results.json`
· **Precision:** every value is rounded (4 s.f.) from `a30_results.json`, where it is stored at full
precision; external inputs are labelled. · **Footing:** canonical `a0 = 9.36e-11`, `L* = 24 pc` (A20 candidate 1), `B_E = 3.66e-14` (A4).

## Claim

The P-sector static hedgehog (A22 D4) gives, **exactly**,

> **`a_P = GM/L*²`** — a constant-*magnitude*, sunward acceleration: `2.4198e-16 m/s²` for the Sun
> (`= 2.585e-6 a0 = 6.61e-3 B_E`), `7.27e-22` for the Earth, `2.31e-19` for Jupiter, `1.217e-46` for a
> 1 kg source at 1 m.

It scales as `M/L*²` — **per source, not universal** — so it is not degenerate with a cosmological
constant (which is universal and `∝ r`). Its *observable* signature is **not** the 10-yr range drift
(0.07–8 m, of which the orbital-element fit absorbs 86–93 % of the arc maximum) but the **retrograde secular perihelion
advance** `a_P√(1-e²)/(n a)`. Against the existing 1σ's on a constant radial acceleration, `a_P` sits at
**1/5.7** (Mars, formal `1.378e-15`) to **1/151** (`B_E`); the joint 8-planet fit measures it at
**0.17σ** (`Δχ² = 0.028`). **Status: NUMERICAL — the number is earned; the anomaly is unobservable with
existing ranging, by a factor 5.7–151, and this is the honest result.**

## Derivation

**D1. The hedgehog.** For `r ≪ λ = L*/√2 = 17 pc` the gradient term in the P equation beats the mass
term, so `|P| = GM/(2γ)` spatially constant (A22 eq. 9). With `γ = K L*²/2 = 2πG L*²` (A22 K11, exact),

  (1)  `|P| = M/(4πL*²)`   and   `u ≡ K|P| = GM/L*²`.                                    [K2: `u_P = GM/L*²`]

**D2. The charge.** `ψ = D·P` obeys the exact identity `∇²ψ = −(K/γ)ρ` (A22 eq. 7), so for a point mass

  (2)  `ψ = GM/(γ r) = M/(2πL*² r)`.

**D3. The potential.** The static lapse/trace system is (A22 eqs 4–6)
`∇²Ψ = K(ψ+ρ)`, `∇²(Φ−Ψ) = 0`, `γ∇²ψ = Kψ − ∇²Φ`. The second gives `Φ = Ψ` (no anisotropic stress, A22
F2). Substituting (2) into the first:

  (3)  `∇²Φ = Kρ + 2GM/(L*² r)`  ⟹  **`Φ = −GM/r + (GM/L*²) r`**.

(3) satisfies both Poisson equations **identically** — verified in real space (`r>0`) and in Fourier
space, where the point-mass delta and `γ` both enter and the residual is exactly `0` [K1]. `γ` cancels
only because `γ = KL*²/2`; a different `γ` breaks the second equation.

**D4. The force is constant.** `a = −∇Φ = −(GM/r²) r̂ − (GM/L*²) r̂`. The non-Newtonian part has
`d/dr = 0` exactly [K2], magnitude `GM/L*²`, direction sunward. This is the functional form ranging
constrains best — the same `r⁰` shape as a Pioneer-type term (contrast the `r¹` of `Λ`).

**D5. Numbers and scaling** [K3]. `a_P ∝ M` (mass ×2 ⟹ `a_P` ×2.000) and `a_P ∝ L*⁻²` (L\* ×2 ⟹ ×0.250).

| source | `GM` (m³/s²) | `a_P` (m/s²) | ratio to Sun |
|---|---|---|---|
| Sun | 1.32712e20 | **2.4198e-16** | 1 |
| Jupiter | 1.26687e17 | 2.3100e-19 | 9.546e-4 |
| Earth | 3.98600e14 | 7.2680e-22 | 3.003e-6 |
| Moon | 4.90487e12 | 8.9434e-24 | 3.696e-8 |
| 1 kg @ 1 m | 6.6743e-11 | 1.2170e-46 | 5.03e-31 |

Also `a_P/a0 = 2.585e-6` (the P field is unsaturated, the premise of the linear branch) and
`a_P/g_N(r) = (r/L*)²` — `4.081e-14` at 1 AU: the anomaly is a `10⁻¹⁴` relative effect on the Newtonian
field, i.e. `a_P` is *not* a MOND-regime effect.

**D6. `L* = c²/a0` is FALSE, and the number does not need it.** The tasking asserts it; the check
refutes it [K4]: `c²/a0_can = 9.602e26 m = 31.1 Gpc = 1.297e9 L*`. Imposing it would give
`a_P = 1.439e-34 m/s²`, `1.7e18` times smaller — the headline number would vanish. The `2.42e-16` value
rests on **A20's measured** `L* = σ_c²/a0` with `σ_c = 8.23 km/s`, which reproduces `23.45 pc ≈ 24 pc`.
So: `a_P = GM/L*²` is exact; the identification of `L*` with the MOND length `L = c²/a0`
(`FINAL_THEORY.md` line 517) is a *different* length and must not be substituted. `L* ∈ [24, 90] pc`
(A20) moves `a_P` over `[1.72e-17, 2.42e-16]`; `24 pc` is the worst case.

**D7. Response of a bound orbit (the observable form).** A constant sunward `a_P` does *not* give
`½a_Pt²`: the planet is bound, and the force is absorbed into a shifted, precessing orbit. Integrating
the linearised (variational) equations about the exact Kepler orbit [K5, K6]:

  (4)  radial: an epicyclic oscillation of amplitude `δr = a_P r³/μ` about a shifted equilibrium
       (Mercury: `3.541e-4 m`, numerical/analytic agreement `2.4e-6`);
  (5)  along-track: secular drift `δs = 2 a_P t/n` for the circular case (the `h = r²θ̇`-conserved
       coefficient is 2, not the naive `3/2`; verified to `5.1e-6`);
  (6)  perihelion: secular, **retrograde**, `dω/dt = −a_P√(1−e²)/(n a)` — from the Gauss equation with
       the *time* average `⟨cos f⟩_t = −e` (angle average is 0; verified to `1e-9`) [K7].

(6) is the only channel that survives a long-arc fit: (4) and (5) are absorbed by `(a, e, M0)` at fixed
`GM`, and even (6) is 86–93 % absorbed over a *single* 10-yr arc (D8) — but its signature grows with the
arc length while an element change does not, which is why the ephemerides constrain it at all.

**D8. Range drift over 10 yr** [K6], both bodies perturbed, `Δ|r_planet − r_Earth|`, median [max] over 8
relative phases:

| system | `Δrange`(10 yr) | max over arc | radial `δr` | post-fit residual | absorbed `δa/a` |
|---|---|---|---|---|---|
| Mercury–Earth | 0.069 m | 0.25 m | 0.056 m | 0.018 m | −8.1e-15 |
| Mars–Earth | 0.198 m | 0.56 m | 0.205 m | 0.061 m | −1.3e-13 |
| Saturn–Earth | 8.19 m | 9.39 m | 8.17 m | 1.28 m | −2.0e-12 |

The free-fall scale `½a_Pt² = 12.05 m` (all bodies) is *not* the answer; the bound response is 1.3–48×
smaller, and 86–93 % of the arc maximum is a mean-motion ramp that any ephemeris fit absorbs (7–14 %
survives). Current
ranging: MESSENGER 5 m, Mercury ephemeris < 1 m (Genova 2018); Juno 20 m; LLR mm (all in
`prep_2026/planetary_doors/BOUNDS.md`). **The raw drift is at or below the per-point noise for all three
systems, and the post-fit residual is below it too.**

**D9. The operative channel and the existing bounds** [K7]. Converting each published 1σ on the
supplementary perihelion advance (FM24 Table 10, EPM2013/INPOP10a) with the same Gauss factor
`δg = σ_ω n a/√(1−e²)` reproduces laneR's tabulated bounds to **2.0 %** (independent validation), then:

| planet | `a_P` precession (mas/yr) | 1σ (mas/yr) | 1σ on `δg` (m/s²) | margin | 10-yr signal vs 1σ |
|---|---|---|---|---|---|
| Mercury | 3.220e-5 | 0.006 | 4.509e-14 | 186× | 0.09 m vs 16.8 m |
| Venus | 4.498e-5 | 0.015 | 8.070e-14 | 334× | 0.24 m vs 78.7 m |
| Earth | 5.288e-5 | 0.0019 | 8.695e-15 | 36× | 0.38 m vs 13.8 m |
| **Mars** | 6.499e-5 | 0.00037 | **1.378e-15** | **5.69×** | 0.72 m vs 4.09 m |
| Jupiter | 1.204e-4 | 0.28 | 5.627e-13 | 2325× | 4.54 m vs 10.6 km |
| Saturn | 1.631e-4 | 0.0047 | 6.973e-15 | 29× | 11.3 m vs 325 m |
| Uranus† | 2.312e-4 | (0.0047) | 4.918e-15 | 20× | 32 m vs 654 m |
| Neptune† | 2.898e-4 | (0.0047) | 3.924e-15 | 16× | 63 m vs 1.0 km |

† no published σ; A4's Saturn stand-in carried (flagged). **Mars is binding at 5.69×**; `B_E` gives 151×.
The bracket `[5.7, 151]` is the honest statement of the margin: the tight number is a *formal*
supplementary-precession σ, which FM24 §5 explicitly discourages reading as a theory bound.

**D10. Not degenerate with `Λ`** [K8, K9]. A cosmological constant contributes `a_Λ = (1/3)Λc² r`
(outward, universal, `∝ r`); `a_P` is inward, per-source, `∝ r⁰`.
`a_Λ(1 AU) = 4.881e-25`, `a_Λ(30 AU) = 1.464e-23`, so `a_P/a_Λ = 4.958e8` at 1 AU; they cross at
`r_c = 2.404 kpc`. Two independent discriminators: (i) shape — fitting `{1, r}` templates to the 8
planets gives correlation `ρ = −0.524` and, with the D9 1σ's, `σ(a_P) = 1.437e-15`,
`σ(k) = 8.94e-28 s⁻²`; (ii) source-scaling — `a_P(Jup)/a_P(Sun) = 9.55e-4`, `a_P(Earth)/a_P(Sun) =
3.00e-6`, which no universal term can mimic. **The discrimination number: `a_P` is a `0.168σ` effect
(`Δχ² = 0.028`), the `Λ` amplitude is `3.65e-9σ`.** So the fit *can* separate them in shape, but the
separation is vacuous with existing data: the `Λ` term is 8 orders of magnitude further from detection
than `a_P` already is.

**D11. Small scales, and the tidal structure** [K9, K10]. `a_P`'s gradient is `−a_P/r` (a `1/r` tide,
not zero): the lunar range feels a `15.7 μm` solar-`a_P` tide (bound response `a/ω_annual²`), and the
Earth's own `a_P` offsets the Moon by `0.10 nm` (bound: `a/ω_m²`; the `36 μm` free-fall figure is not
the answer) with `δμ_E/μ_E = 2.69e-19`. A 1 kg source at 1 m gives `1.217e-46 m/s² = 1.8e-36` of its own
Newtonian field.

## Status

**`NUMERICAL`.** The derivation is exact and premise-free beyond A22's (`static`, `r ≪ λ`, unsaturated
cap, `L*` an input). The *number* is `CONDITIONAL(L* = 24 pc)`: `a_P ∝ L*⁻²`, worst case of A20's window.
The prediction is sharp and falsifiable in form, but **unobservably small with existing data** (5.7–151×
below the 1σ bounds; 0.17σ in the joint fit). No existing dataset excludes it; none confirms it.

## Checks (`a30_checks.py`, 11/11 PASS, exit 0, 7 s)

| id | what it proves | measured |
|---|---|---|
| K1 | (3) solves A22's (4) and (6) exactly, real (`r>0`) and Fourier (delta included) | residuals `0,0,0,0` |
| K2 | `−dΦ/dr = −GM/r² − GM/L*²`, `d/dr=0`, `u_P = K\|P\| = a_P`, sunward | exact |
| K3 | `a_P(Sun)=2.419848e-16`, `a_P(Earth)=7.268e-22`, `a_P(1kg@1m)=1.217e-46`; `∝M`, `∝L*⁻²` | rel. `1e-9` |
| K4 | `L*=c²/a0` is false by `1.297e9`; A20's `σ_c²/a0` recovers 24 pc | ratio `1.3e9` |
| K5 | bound-orbit response: `δr = a_P r³/μ` and `δs = 2a_Pt/n` vs variational integration | `2.4e-6 / 5.1e-6` |
| K6 | 10-yr range drift, radial shift, post-fit absorption, `δa/a` (table D8) | 0.07–8.2 m |
| K7 | `⟨cos f⟩_t = −e`; precession margins; reproduces laneR's bound table | `−0.093412`, `2.0 %` |
| K8 | 8-planet Fisher `{1, r}`: `σ(a_P)`, `σ(k)`, `ρ` | `1.437e-15`, `8.94e-28`, `−0.524` |
| K9 | `a_Λ(1AU)`, ratio, crossover, tidal ratio, lunar tide | `4.88e-25`, `4.958e8`, `2.404 kpc` |
| K10 | Earth–Moon offset, `δμ/μ`, lab source | `0.10 nm`, `2.69e-19`, `1.217e-46` |
| K11 | falsifier: prediction, needed σ, margin bracket | `2.42e-16`, `[5.69, 151]` |

Mutation (`--mutate`), 9/9 bite and exit 1: `drop_linear` (K1), `outward` (K2), `Lstar_1kpc` (K3, K7),
`identity_blind` (K4), `no_drift` (K5, K6), `fisher_forced` (K8), `tide_claim` (K9), `llr_blind` (K10),
`falsifier_flip` (K11). Recorded in `MUTATE.md`.

## The falsifier, numerically

> **Prediction:** `a_P = 2.42e-16 m/s²` sunward, **the same for every planet**, with `dω/dt =
> −6.50e-5 mas/yr` for Mars. **Null (pure-law reading): 0.**

To see it at 1σ: `σ(δg) ≤ 2.42e-16 m/s²` — **5.7×** better than the Mars formal bound (`1.378e-15`),
**151×** better than `B_E`; equivalently `σ(ω̇) ≤ 6.5e-5 mas/yr` at Mars (now `3.7e-4`), a coherent
0.72 m transverse displacement over a 10-yr arc against a 4.1 m 1σ. No existing dataset is close:
`Δχ² = 0.028` for the joint fit. A `Λ`-like term cannot masquerade as it (D10) and vice versa.

## What this does not do

- **No real ephemeris fit** (no INPOP/EPM data on disk): the drift and post-fit numbers are a
  two-body variational model with Keplerian elements, not a full 150-parameter planetary fit. The
  parameter-level bounds are the published ones, imported.
- **The 5.7× margin is formal.** FM24 §5 warns that un-refit supplementary-precession σ's are not theory
  bounds; `B_E = 3.66e-14` (151×) is the conservative reading. The truth is in `[5.7, 151]`.
- **No external field.** `a_P` is the isolated-source monopole; a galactic EFE would modify the P
  hedgehog (A22 "What this does not do"). Uncomputed.
- **No second-order / strong-field** treatment; `r ≪ λ` only. No `L*` derivation: `a_P ∝ L*⁻²` inherits
  A20's [24, 90] pc window.
- **No source-scaling test**: `a_P(Jup)` is 1000× smaller and the Earth's is `3e-6` of the Sun's, so the
  `∝GM` law itself is not testable in this system (it is only testable against `Λ` in principle).

## Next

1. **Pre-register the template.** `a_P` is a *fixed number*, not a fitted parameter: run INPOP/EPM with
   a constant radial acceleration fixed at `2.42e-16` and report `Δχ²` (predicted `0.028`). Anything
   above `~4` kills it.
2. **The EFE correction to the hedgehog.** If the galactic field enters the P equation at the same order
   as the Solar one, `a_P` acquires a direction dependence; compute it before any claimed detection.
3. **`L*` from the galaxy program** (A20): `a_P ∝ L*⁻²`, so narrowing `L*` from 24→90 pc moves the target
   by 14× — the prediction is only as sharp as `L*`.
4. **The honest summary for the record:** a second constant anomaly, `6.61e-3 B_E`, additive to the
   kernel's `a0` in the ephemeris budget, harmless today and a clean target for the next order of
   magnitude in ranging/precession precision.
