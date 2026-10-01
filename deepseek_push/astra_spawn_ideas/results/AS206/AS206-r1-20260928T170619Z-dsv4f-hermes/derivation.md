# AS206 — Derivation: the metric variation of the intrinsic (leaf) Laplacian

**Run**: `AS206-r1-20260928T170619Z-dsv4f-hermes` — seed `AS206_derive_the_metric_variation_of_the_intrinsic_laplacian.md`
(sha256 `42ec085e0ed297505d4f6e10362ac5db21c7e35e6c5c45a04d04739299b87bb8`).
**Worker**: deepseek/deepseek-v4-flash-0731 (openrouter) via dsv4f-hermes subagent, host macOS 26.5.2.
**Status**: completed — all 11 symbolic controls and all 12 numeric controls PASS; Lean certificate verified (zero `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound}).

---

## 1. Mandate and scope

Derive, follow every intermediate factor, sign and unit of, the **metric variation of the
intrinsic Laplacian** — the curved-leaf operator

```text
Δ_h u = (1/√det h) ∂_i ( √det h · h^{ij} ∂_j u )          (intrinsic/leaf Laplacian, coordinate form)
```

under a general symmetric metric variation `h → h + ε k` (`k_{ij} = k_{ji}`), with the
variation rate `δΔu := lim_{ε→0} (Δ_{h+εk} u − Δ_h u)/ε`. Deliverables per the seed:
(i) divergence-form master identity, (ii) independent connection-form cross-check,
(iii) conformal specialization matching the XC1 peer-review witness
(`REVIEW.md` lines 100–109: `δΔ = −2σΔ + grad σ·grad`, Fourier kernel
`(3|q|² − p·q) σ_{p−q}`), (iv) a negative control that **must fail** when the volume
variation is omitted, (v) machine-precision numeric Fourier-kernel witness, (vi) Lean
certificate of the algebraic cores, (vii) both framework footings kept separate.

Framework inputs (adopted, not derived here): `a0 = κ c √(G ρ_Lambda)`, `κ = 1/2`;
`G = 6.67430e-11 m³ kg⁻¹ s⁻²`, `c = 299792458 m/s`, `M_sun = 1.98847e30 kg`,
`pc = 3.085677581491367e16 m`. `G_N`, `G_bare`, `G_cosmo` are kept as **separate symbols**
— no equality of couplings is used anywhere in this seed. The branch dictionary
(Q, RAR, MU2, EXP, MONO) is untouched: this seed is pure leaf-operator machinery, the
interface through which the MONO filter `S = exp((ξ²/2)Δ_h)` is varied in an action under
criterion B. The identity itself is scale-free: `[Δ] = L⁻²`, `[k] = [σ] = 1`,
`[tr_h k] = 1`, `[3|q|² − p·q] = L⁻²`; `a0` enters this seed only as the declared footing
(§7).

## 2. Setup and conventions

- Leaf metric `h` (symmetric, positive, Riemannian, torsionless connection); `h^{-1}` has
  components `h^{ij}`; `k̂^{ij} := h^{ia} h^{jb} k_{ab} = −δ(h^{ij})` (the variation of the
  inverse metric); `T := h^{ij} k_{ij} = tr_h k`; `√g := √(det h)`.
- Christoffel symbols `Γ^m_{ij} := ½ h^{ml} (∂_i h_{lj} + ∂_j h_{il} − ∂_l h_{ij})`, with the
  upper index **last** (key `(i,j,m)`).
- `Δ_h u = (1/√g) ∂_i (√g h^{ij} ∂_j u) = h^{ij}(∂_i∂_j u − Γ^m_{ij} ∂_m u)`.
- The XC1 review writes `δΔ = −2σΔ + grad σ·grad` for the conformal case; its Fourier
  kernel is `(3|q|² − p·q) σ_{p−q}` (verified in §5 as `D3`; the identity of the two
  forms is checked symbolically as `D2`/`D2d`).

## 3. Master identity (divergence-form route) — symbolic, structural

Varying `Δ_h u = (1/√g)∂_i(√g h^{ij}∂_j u)` term by term with `δh^{ij} = −k̂^{ij}` and
`δ√g = ½√g·T`:

```text
δ(Δ_h u) = − k̂^{ij} ( ∂_i ∂_j u − Γ^m_{ij} ∂_m u )
          − ( ∂_i k̂^{ij} + Γ^i_{li} k̂^{lj} + Γ^j_{li} k̂^{il} − ½ h^{jm} ∂_m T ) ∂_j u
```

The first line is the curvature-free operator variation (the `−k̂^{ij}∇_i∇_j u` term with
`∇` the `h`-Levi-Civita covariant derivative); the second line collects the metric
divergence of the variation (`∂_i k̂^{ij}` plus the Christoffel contractions — the
`∇_i k̂^{ij}` covariant divergence) and the **volume variation** `−½ h^{jm}∂_m T`, which is
the term a naive `δ(h^{ij}∂_i∂_j u)` treatment drops. Keeping the volume term is exactly
what makes the identity a true metric variation (the residual-free `D1` result below;
`D4` shows the omission fails).

**Control D1** (SymPy, generic curved 2D leaf, fully symmetric symbolic `k`): residual of
the displayed formula vs the explicit `(1/√g)∂_i(√g h^{ij}∂_j u)` variation:
`0` — structural (residual == 0 identically, no case sampling).

## 4. Independent cross-check (connection-form route)

The same first variation computed through `δΓ^m_{ij}` (variation of the connection,
`2 δΓ^m_{ij} = h^{ml}(∇_i k_{lj} + ∇_j k_{il} − ∇_l k_{ij})` in covariant form, then the
coordinates re-expanded) must return the identical operator.

**Control D1b**: `(connection-form rate) − (divergence-form rate) == 0` structurally.
This cross-check is what caught and pinned an index-order slip in an early draft
(`Γ^m_{ij}` keyed `(i,m,j)` instead of `(i,j,m)`); after the fix both routes agree with
residual 0.

## 5. Conformal specialization and the XC1 witness

Conformal variation `k_{ij} = 2σ h_{ij}` ⇒ `k̂^{ij} = 2σ h^{ij}`, `T = 2nσ` in dimension
`n`. Substituting into the master identity (components: `−k̂^{ij}∇_i∇_j u =
−2σΔ_h u`; the metric-divergence bracket: `∇_i(2σ h^{ij}) = 2∇^j σ`; the volume term:
`−½ h^{jm}∂_m(2nσ) = −n∇^jσ`; total gradient coefficient `2 − n = −(n−2)`):

```text
δΔ u = −2σ Δ_h u + (n − 2) ⟨∇σ, ∇u⟩_h        (dimension n)
```

- `n = 2` (curved 2D leaf): `δΔu = −2σΔu` — gradient term vanishes (controls **D2c**,
  residual 0).
- `n = 3`: `δΔu = −2σΔu + ⟨∇σ,∇u⟩` — coefficient `+1 = n−2` (controls **D2**, **D2d**,
  residual 0; algebra control **D2b** verifies `2 − ½tr_h(2σh) = −(n−2)` identically).
- General-n kernel check **D3**: with `p = q + r`,
  `(2|q|² − r·q) − (3|q|² − p·q) = 0` structurally — i.e. the Fourier-symbol of
  `−2σΔ + ⟨∇σ,∇⟩` acting on mode `q` of `u` with `σ`-mode `r = p−q` is exactly the XC1
  kernel `(3|q|² − p·q)σ_{p−q}` **D3b** (1D fold): for `u = cos(Kx)`,
  `σ = cos((K−1)x)` the `cos x` coefficient of `δΔu` (XC1 kernel convention, n = 3
  grad-coefficient folded to 1D) is `K(3K−1)/2 = (3K²−K)/2`.

## 6. Negative control (must fail)

- **D4** (symbolic, 2D curved leaf, full symmetric `k`): the operator obtained by
  omitting the volume variation `−½h^{jm}∂_mT` differs from the true variation by a
  long nonzero residual (printed in full in `derive_raw.out`) — the omission is detected.
- **D4b** (conformal): the wrong gradient coefficient `−2` (double-counted `∇k̂` term
  without the `+n` volume compensation) vs the true `n−2 = +1` at `n = 3` — fires.
- **N4** (numeric, 3D torus, general `k`): omitting the volume term deviates from the
  true rate by 0.476 relative (threshold: must exceed 0.01).
- **N4b** (numeric, 1D witness): the wrong coefficient returns `K = 20` where the true
  value is `(3K²−K)/2 = 590` — fires.

## 7. Framework footings (kept separate)

With `ρ_Lambda = 4a0²/(G c²)` at fixed `κ = 1/2`:

```text
a0 = 9.3619e-11 m/s²   (canonical)  ->  ρ_Lambda = 5.84441245402e-27 kg/m³
a0 = 1.1279e-10 m/s²   (alternative)
    fixed ρ_Lambda           ->  κ_eff     = 0.6023884041  ≠ 1/2
    fixed κ = 1/2            ->  ρ_Lambda  = 8.483089620e-27 kg/m³
```

The two footings never share `(ρ_Lambda, κ)` — controls **D5** (symbolic) and **N7**
(numeric, same numbers) PASS with tolerance 1e-6 (relative; the constant `a0` carries 7
significant digits). `ε_Lambda = ρ_Lambda c²`, `Λ = 32π a0²/c⁴` (same-G convention noted
but **not** asserted: no identification `G_E = G_N` is made here).

## 8. Numeric controls (FFT-spectral torus; machine-precision rates)

Method: 2D/3D periodic boxes, spectral (FFT) differentiation — exact on band-limited
fields — so the residual isolates the *identity*, not the discretization; the ε→0 rate is
the intercept of a per-point linear fit over `ε ∈ {1e-4, 1e-5, 1e-6}`. Fields are 6-mode
random trig functions (seed 20260928, modes {1,2}), amplitudes 0.1/0.08 (metrics),
0.3 (k), 0.25 (σ). Operator-definition cross-check **N8**: 2nd-order finite-difference vs
spectral Laplacian agree at 1.35e-2 (h²-limited bound 5e-2) at N = 64, an independent
implementation check of `Δ_h` itself.

| id | content | observed | threshold |
|----|---------|----------|-----------|
| N1a | general k, curved 2D torus, rate == formula | 6.14e-9 | < 1e-8 |
| N1b | general k, curved 3D torus (N=48) | 6.42e-7 | < 1e-5 |
| N6  | flat-leaf limit h = δ (3D) | 2.39e-9 | < 1e-8 |
| N2  | conformal k = 2σδ, flat 3D: −2σΔu + ⟨∇σ,∇u⟩ | 2.57e-9 | < 1e-8 |
| N2b | conformal k = 2σh, curved 2D: −2σΔu (n−2 = 0) | 1.93e-9 | < 1e-8 |
| N3  | XC1 1D witness: cos x coeff (3K²−K)/2 = 590; cos((2K−1)x) = 210 | 590.0000000000 / 210.0000000000 | < 1e-9 rel |
| N3c | XC1 Duhamel-weighted coefficient, K=20, b=1/2 | 0.8968749104 | review value 0.896875, < 1e-4 rel |
| N4  | negative control (omit volume term), 3D general k | dev 0.476 | control must fire > 0.01 |
| N4b | negative control, 1D witness (wrong coeff K) | 20.000000 vs 590 | fires |
| N5  | refinement N = 32 → 48 | 2.153e-5 → 2.405e-8 | res48 < 1e-7 ∧ res48 < res32/100 |
| N8  | operator cross-check FD vs spectral | 1.35e-2 | < 5e-2 |
| N7  | footings separation | ρ_L = 5.844412e-27, κ_eff = 0.60238840 | never same (ρ_L, κ) |

**Grid-dependence of N1b (documented, not a defect of the identity).** The intermediates
`h^{-1}` and `√(det h)` are **not band-limited** (rational/radical functions of sines and
cosines carry infinitely many harmonics), so FFT derivatives act on the band-limited
reconstruction with a residual that is a constant-in-ε grid artifact, decreasing with N.
Independent same-field scans (`as206_gridscan.py`, separate bounded process):

```text
N = 32:  2.153e-05      N = 48:  2.405e-08      N = 64:  3.548e-09
```

The N=64 value sits at the pure ε-truncation floor (fit intercept ~1e-9); at N=48 the
6.42e-7 observed in N1b (its own field draw) is also the reconstruction artifact, with
40× margin below the 1e-5 threshold. All other checks are unaffected (their metrics are
either diagonal/small-amplitude or flat).

## 9. Lean certificate (`AS206_metric_variation.lean`, verified with `lake env lean`)

The algebraic cores of the witnesses, all over `ℝ`, zero `sorry`, axioms exactly
{propext, Classical.choice, Quot.sound} (`lean_check.out`):

1. `coef2_id (K x : ℝ)` — the times-two coefficient identity
   `2K²  cos((K−1)x)cos(Kx) + K(K−1) sin((K−1)x)sin(Kx)
    = ((3K²−K)/2)·(2cos x) + ...` in mode-expanded form (cos_sub/cos_add + ring).
2. `coef_id_half` — the witness form with `/2` coefficients (same identity, ring_nf).
3. `witness_K20` — the K = 20 instantiation: `cos x` coefficient **590**, `cos(39x)`
   coefficient **210** (== `(3K²−K)/2`, `K(K+1)/2`), pinning the XC1 kernel numerics.
4. `det_M2`, `adj_equiv`, `adjugate_2x2`, `inv_entry_00` — the 2×2 curved-leaf
   machinery: `det h = ac − b²`, `adjugate(M2) = Adj2`, `M2·Adj2 = det·1 = Adj2·M2`,
   and `(M2 · (1/det)·Adj2)₀₀ = 1` with `field_simp` + `ring`.

The certificate is scoped: it pins the coefficient/cofactor algebra actually executed by
the numeric witnesses; it does **not** restate the PDE calculus.

## 10. What this run does and does not establish

- **Established**: the divergence-form master identity for `δ(Δ_h u)` with every factor
  and sign (two independent routes agree); the conformal specialization with the exact
  `n−2` coefficient; the XC1 Fourier kernel `(3|q|² − p·q)` reproduced to machine
  precision (590/210 at K = 20, Duhamel-weighted 0.8968749104); the negative control
  fires; footings separate.
- **Not established**: nothing here touches the MONO filter `S = exp((ξ²/2)Δ_h)` — the
  variation of the *heat-semigroup* under metric variation is a further (Duhamel-type)
  identity (§11); no claim about the branch dynamics, the 13-item gravity target, or any
  `G`-identification; the numeric identity is verified on tori at the listed grids with
  the quantified reconstruction error, and the Lean certificate is restricted to the
  algebraic cores.

## 11. Next unresolved implication and suggested followup

The first missing bridge to the seed's parent machinery: the metric variation of the
**filtered** operator `d/dε S_{h+εk} u` with `S = exp((ξ²/2)Δ_h)` is
`∫₀^∞ exp(tΔ_h) · δΔ · exp(tΔ_h) u dt`-type (Duhamel, h-dependent kernels), *not* a plain
`δΔ` application — the two differ by the semigroup commutator `[Δ, d/dε]` factors.
Discriminating continuation `AS206.C1`: derive and numerically certify the Duhamel
rate for finite `ξ` on the same torus harness (the N3c Duhamel-weighted coefficient
0.896875 is the 1D fingerprint of exactly this object), then substitute the MONO
`h → S`-variation chain in the action under criterion B.