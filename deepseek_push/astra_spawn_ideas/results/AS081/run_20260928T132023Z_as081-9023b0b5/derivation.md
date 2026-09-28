# AS081 — Self-source and imposed baryon well are different

**Run:** `run_20260928T132023Z_as081-9023b0b5` (unique)
**Task file:** `deepseek_push/astra_spawn_ideas/AS081_self_source_and_imposed_baryon_well_are_different.md`
**Task SHA-256:** `9023b0b523fff46f3a3e14d636a7553adcf9289de99f406c2b7fb64ece08f3e8` (verified on disk before execution)
**Branch cell:** Conditional deep-equilibrium sector (G084/G091/G233 equilibrium of the log well); **no** Q/RAR/MU2/EXP/MONO kernel evaluated or transferred. Operative target elsewhere = filtered MONO, criterion B — explicitly **not** invoked here.
**Footings:** canonical `a0 = 9.3619e-11 m/s²` and alternative `1.1279e-10 m/s²`, kept **separately** (fixed `kappa = 1/2` adopted ⇒ the two footings cannot share one vacuum density).

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions

### Claim (the exact statement delivered)

> **Self-source and imposed baryon well are different.** On every open annulus
> `r > 0` of flat space,
>
> ```text
> Δ(C·ln r) = C/r²        (exact, C > 0)
> Δ(−G·M_b/r) = 0         (exact harmonic exterior; the baryon's source is 4πG·M_b·δ³ at r = 0)
> C/r² > 0  ⇒  Δ(C·ln r) ≠ Δ(−G·M_b/r) + Δ h   for any harmonic completion h (Δh = 0).
> ```
>
> Consequently the logarithmic well `C·ln r` **is not** the potential of a point
> Newtonian baryon `−G·M_b/r` (nor of that potential plus any harmonic function)
> on `r > 0` **without a modified equation**. The Poisson source of the log well is
> the extended phantom density `ρ_src = C/(4πG r²) = A/r²` with the G084/G091
> equipartition amplitude `A = C/(4πG)`. The baryon enters the equilibrium only
> through (i) the amplitude `C = √(G·M_b·a0)` (equipartition normalization
> `M_ph(<r_M) = M_b`, i.e. `4πA·r_M = M_b`), and (ii) the *true* `1/r` baryon
> well in the virial coupling `W_bar = ∫ρ_ph·(−G·M_b/r)dV = −M_b·C·ln(r_break/r_b)`
> (G091 V1c) — never as the point source of the log.

**Exact premise needed to call the log well "baryonic"** (the seed's question):
the log well equals the *total* potential of a two-source system
`Φ_tot(r) = −G·M_b/r + C·ln r + const` only in the phantom-dominated regime
`4πA·r ≫ M_b`; under equipartition the crossover radius is exactly
`r_b = G·M_b/C = r_M` (so `M_ph(<r_M) = M_b`, `C = a0·r_M`), and on the deep
exterior shells the neglected `1/r` term is a 0.4–14% correction of the log
(**F2**). Calling `C·ln r` itself "the baryon well" without these premises
attributes the phantom's own source `C/(4πG r²)` to the baryon — the error the
negative control (E1) quantifies.

### Symbol dictionary (SI unless noted)

| symbol | meaning | value / relation |
|---|---|---|
| `G` | Newton coupling | `6.67430e-11 m³ kg⁻¹ s⁻²` (campaign default) |
| `c` | speed of light | `299792458 m/s` |
| `M_sun` | solar mass | `1.98847e30 kg` |
| `pc` | parsec | `3.085677581491367e16 m` |
| `a0` | framework scale | `κ c √(G ρ_Λ)`, `κ = 1/2` **adopted input** |
| `ρ_Λ` | vacuum mass density | `4 a0²/(G c²)` = `5.844412e-27` (can) / `8.483090e-27` (alt) `kg/m³` |
| `ρ_src` | log-well Poisson source | `C/(4πG r²)` `[kg/m³]` |
| `A` | profile amplitude | `C/(4πG)` `[kg/m]` (G084/G091 coefficient) |
| `C` | `v_flat²` | `√(G M_b a0)` `[m²/s²]` |
| `r_M` | equipartition radius | `√(G M_b/a0)` `[m]` |
| `M_b` | baryon mass | `7e10 M_sun` fiducial (deepseek_push MW proxy) |
| `Φ_b` | baryon potential | `−G M_b/r` (point source) |
| `Φ_log` | log potential | `C ln r` |
| `L[f](r)` | radial Laplacian | `f″(r) + (2/r) f′(r)` (spherical symmetry) |
| `δ³` | 3-D delta | baryon source support `{r = 0}` |

### Boundary conditions and assumptions

- **Domain:** finite shell `r_in ≤ r ≤ R` with `r_in > 0`, `R ≤ r_M` for the
  interior diagnostics; the identity itself holds on every annulus `0 < a ≤ r ≤ b`.
  `r = 0` excluded (open domain; log diverges there, the source is not normalizable
  at the origin without an inner cutoff — stated, not hidden).
- **Equilibrium premises (taken as the framework's declared conditional
  deep-equilibrium targets, G084/G091, not re-derived):** profile `ρ = A/r²`,
  `σ² = C/2`, `P = σ² ρ`, equipartition `M_ph(<r_M) = M_b`.
- **Assumptions:** `G, M_b, a0, C, r_M, r_in, R > 0`, `r_in < R`; spherical
  symmetry; flat-space Poisson `ΔΦ = 4πGρ`; `κ = 1/2` adopted; one footing at a
  time; `G_N = G_bare = G_cosmo = G` **not** assumed — this task does not touch
  the vacuum-curvature couplings, so no ratio is quoted.
- **No fit performed.** Tolerances set before evaluation (see checks).

---

## 2–3. Derivation with every scale factor, sign and unit

### Step A — the Poisson source of the log well

Spherical coordinates, `Φ(r) = C ln r`, `C > 0`:

```text
∇Φ = C/r · e_r                         [unit: m²/s² · 1/m = m/s²]   (acceleration units)
∇²Φ = (1/r²) d/dr ( r² · C/r ) = (1/r²) d/dr (C r) = C/r²           [s⁻²]
```

Explicitly `Φ′ = C/r`, `Φ″ = −C/r²`, so `Φ″ + (2/r)Φ′ = −C/r² + 2C/r² = C/r²`.
Poisson: `ΔΦ = 4πG ρ_src` ⇒

```text
ρ_src(r) = C / (4πG r²) = A/r²,   A := C/(4πG)      [kg/m³]
```

`A` is exactly the G084/G091 equipartition amplitude: `M_ph(<r) = ∫0^r 4πr'² (A/r'²) dr' = 4πA·r = C·r/G` — **linear growth** in `r`. At `r_M`:
`M_ph(<r_M) = C·r_M/G = M_b` (using `C² = G M_b a0`, `r_M² = G M_b/a0` ⇒ `C/r_M = a0` and `C r_M = G M_b`, both certified in Lean). Units: `C/r² : m²/s²·m⁻² = s⁻² = 4πG·(kg/m³)·(m³/(kg s²))` ✓.

### Step B — the baryon well

`Φ_b = −G M_b/r`, `r > 0`: `Φ_b′ = G M_b/r²`, `Φ_b″ = −2G M_b/r³` ⇒
`ΔΦ_b = −2GM_b/r³ + (2/r)(GM_b/r²) = 0` — **harmonic** on every annulus. The
source is distributional: Gauss flux through any sphere `Σ_r`:

```text
∮ ∇Φ_b·n dA = 4πr² · (G M_b/r²) = 4π G M_b   (independent of r)  ⇒  ΔΦ_b = 4πG M_b δ³
```

Consistent with a point baryon whose whole mass sits at `r = 0`. Units:
`G M_b/r² : m/s²` ✓.

### Step C — Gauss flux of the log well

`g(r) = C/r`; flux `= 4πr²·(C/r) = 4π C r = 4π G (C r/G) = 4πG M_enc(<r)` with
`M_enc(<r) = C r/G` — the flux identity that ties source normalization to the
enclosed mass (verified numerically and in Lean T10–T11).

### Step D — the two wells cannot coincide

If `C ln r = −G M_b/r + h` pointwise on an open set with `h` harmonic
(`L[h] = 0`), then by additivity of the Laplacian (Lean T7, conditional on the
stated differentiability premises)

```text
L[C ln r] = L[−G M_b/r] + L[h] = 0 + 0 = 0,
```

but `L[C ln r] = C/r² > 0` (Lean T2, T5, T8 ⇒ contradiction). The additive
regularity hypotheses are exactly the seed's static-profile premises
(Φ differentiable; the harmonic completion twice differentiable). No modified
equation, no coincidence.

### Step E — the single-radius coincidence (equipartition)

`M_enc,log(<r) = M_b` iff `C r/G = M_b` iff `r = G M_b/C = r_M` (Lean T12–T13).
The log well's enclosed mass equals the baryon mass at **exactly one radius**;
at `2r_M` it is `2M_b` (Lean T15). This is the quantitative content of
"self-source ≠ imposed baryon well": a point baryon's enclosed mass is `M_b` at
*every* radius.

### Step F — finite boundaries (both explicit)

On `r_in ≤ r ≤ R`, `r_in > 0`:

```text
M([r_in, R]) = 4πA(R − r_in) = C(R − r_in)/G          (finite; Lean T16)
Φ(R) − Φ(r_in) = C ln(R/r_in)                          (finite for r_in > 0)
```

`r_in → 0⁺` and `R → ∞` individually diverge: the log well is not normalizable
on the unbounded domain without the inner cutoff and the outer cap (the
equilibrium's own EFE cap `r_break = 0.62 r_M`, G03B/G091, and the finite inner
edge keep all bookkeeping finite — this run records the shell forms; the virial
budget at `r_in > 0` is a *separate* obligation, listed as the next
implication).

### Step G — deep exterior and the leading neglected term

Two-source total potential `Φ_tot = −G M_b/r + C ln r + const` has
`ΔΦ_tot = C/r² + 4πG M_b δ³`. In the phantom-dominated regime (`r ≫ r_M`,
equivalently `4πA r ≫ M_b`) the log term dominates; the leading neglected term
is the `1/r` baryon term with relative magnitude at the shell inner cap

```text
|Φ_b| / |C ln(R/r_in)| = (G M_b/r_in) / (C ln(R/r_in)) = {14.4%, 4.3%, 1.44%, 0.43%}
```

on the four deep-exterior shells (`r_in/r_M,R/r_in`) = (10,2),(10,10),(100,2),(100,10) — see residuals `leading_neglected_term_PhiB_over_Pl`. On those shells the phantom mass carried is `q(s−1) M_b = {10, 90, 100, 900} M_b` (residuals `deep_exterior_shells`): an interior log-well ansatz extended outside `r_M` at the interior amplitude is **not** a point-source deep-MOND domain (no interior→MONO transfer; per seed).

---

## 4. Independent checks with actual residuals

| check | representation | residual (actual, saved) |
|---|---|---|
| A1 | sympy symbolic `d²/dr² + (2/r)d/dr` of `C ln r` | difference `0` (exact) |
| A2 | FD Laplacian on a 40001-pt log grid, interior | max rel `1.73e-07` |
| A3 | mpmath 60-digit five-point O(h⁴) stencils at 5 radii | max rel `2.67e-37` |
| B1 | Poisson residual `ΔΦ − 4πGρ_src` | max rel `1.73e-07` |
| C1 | flux identity `4πr²(C/r) = 4πCr` | rel `1.98e-16` |
| C2 | `M_enc = C r/G = 4πAr` | rel `1.11e-16` |
| D1 | baryon FD Laplacian on the same grid (harmonic) | max rel `7.08e-07` |
| D2 | baryon Gauss flux at `10 r_M` vs `4πG M_b` | rel `1.54e-16` |
| F1 | deep regime down to `r/r_M = 1e-6` | max rel `1.46e-07` |
| G1 | `M([r_in,R]) = C(R−r_in)/G` on the six fixtures | ≤ `1.54e-16` |
| G2 | `M_shell/M_b = q(s−1)` on the deep shells | ≤ `1e-14` (exact) |
| H1 | framework identity `a0 = (c/2)√(G ρ_Λ)` back-calc | rel `< 1e-15` |
| H2 | footing ratio `(a0_alt/a0_can)² = 1.451487`; fixed `ρ_Λ(can)` ⇒ `κ_eff = 0.602388` | exact |

The FD residuals `~1e-7` are grid-truncation limited (np.gradient on a log
grid, 2nd order); the closed forms are separately certified exactly in Lean
(18 theorems, zero sorry).

## 5. Negative control(s) — capable of failing, and how they behaved

**E1 (the seed's control — assign the log potential to a point Newtonian baryon
without a modified equation):** on the annulus `r > 0` the baryon's source is
`4πG M_b δ³ ≡ 0`, while `Δ(C ln r) = C/r²`. Normalized mismatch
`max |ΔΦ_log − 0|/|C/r²| = 1.000` — **the control FAILS** (pass criterion
"mismatch ≈ 0 if the assignment were true"): the log well's source is fully
extended, so the assignment is impossible without a modified equation. The
control is not vacuous: it would pass only if the log well were the baryon's
well, and the machinery demonstrably registers the difference (E3: min
`|Δ_log − Δ_bar|/|Δ_log| = 1.0` on the whole annulus, Lean-certified).

**E2 (enclosed-mass arm):** `M_enc,log(<r)/M_b = r/r_M ∈ {1, 2, 10}` at
`{r_M, 2r_M, 10r_M}` — a point baryon keeps the ratio `1` at every radius; the
log well equals it at the single equipartition radius (Lean T12/T13/T15).

**D1/D2 (Newtonian regime):** the baryon well is exactly harmonic outside its
source (residual `7e-07`) and carries the full flux `4πG M_b` — its Newtonian
regime is *exact*, in contrast to the log well, which has **no** Newtonian
limit (Laplacian never vanishes, potential diverges at infinity).

All controls and checks: `out/residuals.json`, `out/stdout_capture.log`.

---

## Strongest surviving statement

**Theorem (self-source ≠ imposed baryon well).** On `r > 0` in flat space with
the Poisson equation, for `C > 0`, `G > 0`, `M_b > 0`:

1. `Δ(C ln r) = C/r² = 4πG ρ_src` with `ρ_src = C/(4πG r²)` — the log well's
   source is the extended phantom density (exact identity; Lean T2/T9;
   residuals A1–A3, B1).
2. The log well is not the baryon's Newtonian potential, nor that potential
   plus any harmonic completion, on any open annulus (Lean T8;
   `no_imposed_baryon_log_well`, conditional on the explicitly listed
   differentiability premises; controls E1/E3).
3. The only "baryonic" reading: the amplitude `C = √(G M_b a0)` from
   equipartition `M_ph(<r_M) = M_b` (single-radius coincidence, Lean T12–T13),
   with the true `1/r` baryon well appearing only as the neglected term
   `−G M_b/r` in the phantom-dominated exterior (F2) and as the virial
   coupling `W_bar = −M_b C ln(r_break/r_b)` (cited, G091 V1c).
4. Finite-shell bookkeeping is finite and exact with both boundaries explicit
   (G1, Lean T16); dimensionless form is identical on both a0 footings (H3,
   Lean T17); dimensional examples stated per footing (H).

**Domain:** open annuli `0 < r_in ≤ r ≤ R` (flat, static, spherical);
footings `a0 ∈ {9.3619e-11, 1.1279e-10} m/s²` separately; `M_b = 7e10 M_sun`
fiducial; no time dependence, no kernel/MONO evaluation, no fit.

**Both-footing application of the dimensionless theorem:** the identity
`Δ(C ln r) = C/r²` and the coincidence `r = G M_b/C = r_M` are scale-free in
`a0` (Lean theorems are stated for arbitrary positive `C, G, M_b, r`): they
apply to both footings verbatim, with footings entering only through the
dimensional `C, r_M, ρ_Λ, ρ_src` values, which are quoted **separately**
(canonical vs alternative; `κ = 1/2` fixed ⇒ `ρ_Λ(alt)/ρ_Λ(can) = 1.451487`;
`ρ_Λ(can)` fixed ⇒ `κ_eff = 0.602388`).

## First additional implication needed to transfer to the full theory

The transfer to the operative gravity law (filtered MONO, criterion B) requires
the missing step: **derive the static potential admitted by the operative
filtered-MONO field equation** `Δu = 4πG ρ_b + S⁎[div((ν_mono(|∇Su|/a0) − 1) ∇Su)]`
with the phantom source `ρ_src = C/(4πG r²)` on the shell `[r_in, R]`, and show
whether the log well `C ln r` is its exact deep solution or gets a kernel
correction (asymptotically `C_eff ln r` with renormalized amplitude), plus the
matching of `C_eff` to `√(G M_b a0)`. Until that exists, the log well and its
source identity are statements about the **conditional deep-equilibrium
sector**, not about MONO: no interior ansatz is transferred (seed requirement,
recorded in G2/F2).

---

## Limitations

- Numerical checks are finite evidence (float64 FD grids, mpmath 60-digit
  stencils, sympy); the identities are separately certified exactly in Lean
  (18 theorems, zero sorry, axioms ⊆ {propext, Classical.choice, Quot.sound}).
- `κ = 1/2` and the equilibrium relations (`ρ = A/r²`, `σ² = C/2`, equipartition)
  are adopted inputs, not derived here.
- No kernel (Q/RAR/MU2/EXP/MONO) is evaluated; no filtered-MONO transfer
  claimed; no time-dependent or dynamical statement; `G_bare`/`G_cosmo`
  separate-symbol issues untouched (no vacuum-curvature coupling used).
- The log well is not normalizable on the unbounded domain without the inner
  cutoff + outer cap (stated in F/Step F); the finite-shell **virial** budget
  at `r_in > 0` (T, W_self, W_bar, surface term closed forms) is not derived
  here — it is the nearest separate obligation.
- Historical sources (G084/G091/G233) used `G = 6.674e-11`, `M_sun =
  1.98892e30` vs campaign defaults; combined difference < 0.05% on dimensional
  examples, no structural effect (recorded).
- macOS cannot enforce RLIMIT_AS (`ulimit -v` rejected): the 512 MB memory
  bound was enforced by monitoring only (recorded peak RSS 91.6 MB), CPU bound
  `ulimit -t 120 s` was enforced, wall 0.285 s; 1 thread enforced via
  environment variables and a single-process run.

## Artifacts

- `as081_derive.py` — the bounded prototype (wall 0.285 s, RSS 91.6 MB, 1 thread)
- `out/stdout_capture.log`, `out/results.json` (= `out/residuals.json`) — raw
  outputs and residuals
- `out/failed_attempts_notes.txt` — iteration causes (A3 stencil, D1 space bug,
  H print bug, RLIMIT_AS environment note)
- `AS081_cert.lean` (+ `AS081_cert.olean`) — Lean 4 certificate, 18 theorems,
  zero `sorry`; `out/axioms_check.out` — axiom transcript
