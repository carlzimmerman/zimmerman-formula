# AS132 — Derivation: the fixed-compensator stress (Tier-0)

Run: `AS132-r1-20260928T171600Z-dsv4f-hermes` · worker: `dsv4f-hermes`
Pinned action: CA4-GNC host (`real_research/common_action_2026_09_26/action/FINAL_ACTION.md` eq. (4)); branch CA5-GNC-R (reciprocal dark sector).
Seed: `deepseek_push/astra_spawn_ideas/AS132_derive_the_fixed_compensator_stress.md`
(sha256 `fa52d91c5d929421deb7030b49d3dc3403a804f4412c49df145f4dfae405fed1`, verified).

## 1. Task and exact claim

The fixed compensator is the gravity-stress released when the dark-sector continuation
field `W_b` is compensated on a closed spacelike leaf at fixed lapse flow:

```
S_comp = (M_P^2 c_N ell/2) ∫ dτ ∫_Σ N sqrt(h) a^i D_i W_b ,        a = D ln N ,
```

with the RAISED acceleration `a^i = h^{ij} D_j ln N` and the LOWERED gradient
covector `(D W_b)_i`; `N` the shift-lapse (lapse flow), `sqrt(h)` the leaf measure,
`ell` the compensator length, `c_N = 1 - alpha/2` the C4 slope-normalization, and
`M_P^2 = (8 pi G_bare)^(-1)` (bare-Planck). Coefficient cell adopted:
`0 < ell < 4`, `c_N = 1 - alpha/2`, `kappa = 1/2`, instance `ellS = 2/5`.

**S2 (metric variation).** Varying only the leaf metric `h -> h + eps*s` at fixed
`(N, W_b)`:

```
delta_h S_comp = (M_P^2 c_N ell/2) ∫ N sqrt(h) Theta_comp^{ij} s_ij ,  Theta_comp^{ij} = (1/2) h^{ij} (a·DW_b) - a^{(i} D^{j)} W_b,
```

i.e. the stress tensor of the compensator is symmetric with trace `(1/2)h^{ij}(a·DW_b)`
(measure channel) and traceless part `-a^{(i}D^{j)}W_b` (contraction channel; the
inverse-metric variation supplies the minus sign through
`d/deps (h+eps s)^{-1}|_0 = -h^{-1}s h^{-1}`).

**S3 (lapse variation).** Varying only the lapse flow at fixed `(h, W_b)`,
`ln N -> ln N + eta phi`:

```
delta_lnN S_comp = (M_P^2 c_N ell/2) ∫ dτ (-∫ N sqrt(h) phi a·DW_b  pre-IBP  =  -∫ N sqrt(h) phi Delta_N W_b  reduced)
```

i.e. the pre-IBP pointwise statement is
`δ_lnN = -N sqrt(h) phi [ a·DW_b ]` with `a = D ln N`, which integrates by parts to
`-∫ N sqrt(h) phi [ Delta_h W_b + (D phi)·(D W_b) ]` and to the reduced form
`-∫ N sqrt(h) phi Delta_N W_b`, tying the lapse channel to the AS145
gate-lapse contribution `delta_lnN S_gate = C_N ∫ N sqrt(h) phi [G(Y_h) - ell Delta_h W_b]`.

**P (pair consistency).** The mixed second variation is order-independent:
`d/dlnN d/dh = d/dh d/dlnN` as one functional on the closed leaf. Symbolically the
h-first closed form `R1 = N sqrt(h)[phi·Theta(s) + Theta(D phi)(s)]` matches the mixed
expansion exactly (pointwise); the lapse-first reduction `R2` differs only by an
integration-by-parts remainder (pointwise non-vanishing, integral zero on the closed
leaf — verified numerically, see D-checks).

**NC (f-multiplied compensator).** Replacing the continuation by `f·W_b` with a
smooth `f = G(Y_h)` on the gate yields the extra stress
`-∫ N phi [(f-1) Delta_h W_b + <D f, D W_b>]` over the fixed compensator; the fixed
stress by itself FAILS against the f-action (negative control, residual ~ -1).

**Negative control (capable of failing).** A smooth control witness `W_CONTROL` is
swept along the C4 ramp; for the tuned gate centroid the FIXED compensator does not
reproduce the f-action lapse flow: `(FD_f - S_fix)/|FD_f|` = **-0.9965 (64^2)** /
**-0.9934 (96^2)** (target residual `|.| <= 1e-3` FAILS by O(1) as required), while the
`Theta_f` and extra-stress closed forms pass at 3.3e-5 / 1.8e-5 (tolerance 1e-4).

## 2. Framework cell, data, conventions

- `a0 = kappa c sqrt(G rho_Lambda)`, `kappa = 1/2` ADOPTED as input.
- Numerics: `G = 6.67430e-11`, `c = 299792458`, `M_sun = 1.98847e30`,
  `pc = 3.085677581491367e16` (SI).
- `G_N/G_bare/G_cosmo` kept separate: `G_bare = (8 pi M_P^2)^(-1)` enters only through
  the `M_P^2` cell; Newton scale `G_N`, cosmological scale `G_cosmo` are distinct
  constants (unified only at the closure cell, not in this seed).
- Branches kept distinct throughout: Q, RAR, MU2, EXP, MONO (criterion B: the
  monotone branch B is the active policy — AS133 landmarks `y* = 2.3374124`,
  `y_p = 2.5396394`; the torus-leaf numerics of this seed use the C4-ramp geometry and
  their own sintonic point `y_star = 5.0`; the MONO landmarks are referenced, not
  re-derived).
- Footings (both required): canonical `a0 = 9.3619e-11 m/s^2` with
  `rho_Lambda = 5.844412454e-27 kg/m^3` (roundtrip
  `(c/2)·sqrt(G·rho_can) = 9.3619e-11` exact); alternative footing
  `a0 = 1.1279e-10 m/s^2` with `rho_Lambda = 8.483089620e-27 kg/m^3`, i.e.
  `kappa_eff = 1.2048` at fixed canonical density. Both values match the seed's
  stated footings.
- `c_N = 1 - alpha/2`, `alpha = 1/2` (C4 ramp), so `c_N = 3/4`; `ellS = 2/5`.

## 3. Symbolic core (sympy, exact rational arithmetic on a concrete leaf)

Instance (as in the seed's symbolic layer): `h11 = 1+xy`, `h12 = x^2/3`,
`h22 = 2+y/2`; `s11 = x`, `s12 = y^2`, `s22 = 1+xy/2`; `ln N = xy+x`; `W = x^2 y + xy^2/2`;
`phi = x+y^2`; lifted via `g -> g + eps*s` and `ln N -> ln N + eta*phi`, exact
differentiation at `(eps, eta) = 0` with the full `sqrt(det)` measure and the FULL
covariant Laplacian (Christoffel terms included; `laplace_sym` validated against the
conformal identity `Delta_{e^{2w}delta} f = e^{-2w} Delta_delta f` and an independent
Gamma-summation).

- S2 pointwise: `d/deps [sqrt(det(h+eps s)) a(h+eps s)·DW] = (1/2)h^{ij}s_ij (a·DW) - s_ij a^{(i} w^{j)}`  — **True** (exact cancellation).
- S3 pointwise: `d/deta [sqrt(h) a(ln N + eta phi)·DW] = phi [Delta_h W + <D phis'>...]`-contracted form — **True** (exact).
- P h-first: `mixed - R1 == 0` pointwise — **True**. Lapse-first `mixed - R2` is an IBP remainder (see §1, P); integral equality verified numerically.
- NC: on the flat leaf with generic `F, J`, the f-compensator derivative matches the closed form
  `N [ (1/2)(s11+s22) F(Y_0) (a·DW) - F(Y_0) s_ij a^i w^j + F'(Y_0) (a·DW) (J'(-2 w^i s_ij w^j) + ell d(D_h W)) ]`
  with the pass-through `Y = J(|DW|^2) + ell Delta_h W - theta` (AS145 gate structure) — **True** (exact, after normalization of `Subs(Derivative)` atoms; see statement in result.json).

## 4. Numeric verification (torus leaf, 64^2 and 96^2, single thread)

Test data: base metric `h* = delta` (with a non-conformal control metric used only to
validate `laplace()` independently), `N = exp(xy+x)`, `W` as above, C4 ramp
`Gp(Y)` gate as AS145/AS133 (MONO-consistent tables), `ell = 2/5`, theta tuned at
64^2 to maximize `|∫ N·extra|` subject to >= 0.5% of sites strictly inside the gate:
`theta_star = 2005.93`, in-gate fraction `0.88%`, `|extra| = 285.7`.

All 39 checks PASS (2 grid sizes × 19 + ratios), including:

| check | 64^2 value | tol | meaning |
|---|---|---|---|
| A metric FD == Θ-integral (S2) | −1.06e-11 | 1e-8 | variation of the density equals `N√h Θ^{ij} s_ij` |
| A64b no-measure target fails | 0.517 | min | the wrong (measure-less) target is rejected |
| C lapse FD == pre-IBP bilinear | 2.45e-11 | 1e-8 | `δS = ∫N√h[φ a·DW + <Dφ,DW>]` machine-grade |
| C-c transpose | −1.7e-16 | 1e-12 | `⟨Nφ, D^2 W⟩ = −⟨D(Nφ), DW⟩` (unweighted IBP) |
| C-d reduced `−∫Nφ Δ_h W` | −9.96e-05 | 1e-4 | sits at the O(h^4) stencil defect, ratio (64/96)^4 = 0.198 ✓ |
| D mixed == R1 (h-first) | 6.07e-06 | 1e-4 | pair-consistency, first ordering |
| D R2 (lapse-first) == R1 | −7.66e-04 | 1e-3 | pair-consistency, second ordering at stencil defect; ratio ✓ |
| E remainder | −0.250 | 0.75 | ε-scaling is ε²..ε³ (cubic or better), no linear leakage |
| F1 f-compensator FD == Θ_f | 3.29e-05 | 1e-4 | the GOOD target for the f-action (table-knot limited) |
| F2 FIXED stress vs f-action | −0.9965 | FAIL | **negative control bites** (required) |
| F5 (FD_f − S_fix) == extra | 3.29e-05 | 1e-4 | the extra stress is exactly the difference |
| F3 lapse FD == pre-IBP | 3.30e-11 | 1e-8 | `−∫Nφ[f·Δ_NW]`-reduced form incl. `⟨Df,DW⟩` |
| F4 extra lapse == `−∫Nφ[(f−1)Δ_hW + ⟨Df,DW⟩]` | 2.46e-05 | 1e-4 | NC lapse channel |
| G1/G2/G3 constant N / W vanish | ≤ 1.1e-16 | 1e-12 | kernel sanity: no phantom sources |

Contract details (seed REQUIRES): G, c, M_sun, pc as in §2 (used in the footing
block); G_N/G_bare/G_cosmo separate; all six branches distinct; the negative control
is a real failing test (F2 residuals −0.997/−0.993, i.e. the fixed compensator is
NOT the f-action response — the extra stress is order 1, exactly the NC claim).

## 5. Controls and bounds (recorded, actually enforced)

- Wall: measured `perf_counter` over both grids **26.9 s < 120 s bound** (single run);
  `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1`, no FFT/BLAS; one process.
- RSS: `getrusage` maxrss **≈ 150 MiB < 512 MB bound** (macOS reports bytes:
  157286400 B; grids sized with > 7x headroom vs the 512 MB cap).
- All checks executed for real (residuals recorded, not booleans); scheme defects are
  honestly reported at their measured size with cross-grid (64/96)^4 = 0.1975 ratio
  guards rather than machine-exact claims.

## 6. Lean certificate (algebraic core, compile-verified)

`AS132_stress_variation.lean` (self-contained) certifies the S2 flat-core identity:

```
d/deps |_0  sqrt(g(eps)) * (A(eps) . w)  =
   (s11+s22)/2 * (a1 w1 + a2 w2) - (s11 a1 w1 + s12 a1 w2 + s12 a2 w1 + s22 a2 w2)
```

with `g = det(I + eps S)`, `A = (I + eps S)^{-1} a` via the 2x2 adjugate
(`A1`, `A2`), i.e. the measure channel `(1/2) h^{ij} s_ij (a·DW)` plus the
contraction channel `-s_ij a^i w^j` (the inverse-metric derivative `-S`). Theorems:
`g_value_at_zero`, `g_deriv_at_zero`, `raise_deriv_1`, `raise_deriv_2`,
`contraction_variation`, `sqrtg_deriv_at_zero`, and the headline
`stress_variation_flat`. Verified with `lake env lean` (exit 0, zero errors);
`#print axioms` = **{propext, Classical.choice, Quot.sound}** — no sorry, hard bar met.

## 7. Conclusions, limitations, next steps

**Strongest statement (S2, verified on the curved symbolic leaf + torus numerics):**
the metric variation of the pointwise compensator density is exactly
`(1/2)h^{ij}s_ij(a·DW) - s_ij a^{(i}w^{j)}` — the stress tensor is
`Θ_comp^{ij} = (1/2)h^{ij}(a·DW_b) - a^{(i}D^{j)}W_b`; the S3 lapse channel reduces to
`-∫N√h φ Δ_N W_b` (machine-grade pre-IBP, stencil-defect post-IBP), the P pair
consistency holds in both orderings numerically and in the h-first ordering
pointwise, and the NC/negative control closes: the f-multiplied compensator adds
exactly `-∫Nφ[(f-1)Δ_hW + ⟨Df,DW⟩]` and the fixed stress alone fails at order 1.

**Limitations.** (1) Numeric torus is a flat-base (`h* = δ`) 2D leaf; curved-base
perturbations are covered symbolically and by the independent laplace-validations,
not by a full curved-grid run. (2) R2 (lapse-first symbolic) is an integral-level
statement: pointwise it carries the IBP remainder by construction; the integral
equality is certified numerically at the O(h^4) stencil defect. (3) F1/F5 sit at
table-knot precision (1e-4) because `Y_h` enters through `np.interp` on the AS145
J-tables (secant derivative used throughout). (4) MONO landmarks (2.3374124 /
2.5396394) are referenced from AS133; the torus test geometry has its own sintonic
point (y* = 5.0) and is not a MONO re-derivation.

**Next unresolved implication:** the lapse channel `δ_lnN S_comp = -∫N√h φ Δ_N W_b`
is the SAME operator that drives the gate-lapse `δ_lnN S_gate` of AS145
(`C_N ∫ N√h φ [G(Y_h) - ℓ Δ_h W_b]`): the compensator and the gate share the
Laplacian-of-W source, so a common sink exists in `P` (pair) consistency for the
TWO-functionals closure.  Suggested follow-up: AS-sibling on the mixed
compensator×gate second variation (or the `delta_lnN` pair sum) to test whether the
two functionals merge into one at the closure cell (B-branch, MONO).

**Suggested followup:** seed AS1xx "mixed compensator x gate lapse variation"
(continuation of the P-lane), with a curved-base numeric 64^2 run to lift
limitation (1).