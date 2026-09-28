# AS131 — Derive the heat-field metric stress (Tier-0 seed)

Run: `AS131-r1-20260928T153400Z-dsv4f-hermes` · worker dsv4f-hermes (deepseek/deepseek-v4-flash-0731, openrouter, Hermes host) · task_sha256 `c196e1f9ba3087b89d01be20450dd2b49484e263c86157342ca29c987cce9de4`

## 0. Target (action (4), CA4-GNC; inherited by CA5-GNC-R per breakthrough review CONTRACT.md)

Heat-constraint block of the action, flat-leaf expression quoted by the seed:

```
S_heat = (M_P² c_N / 2) ∫ dτ ∫_Σ N √h ∫_0^b dr  L(r,x) [ ∂_r W − Δ_h W ],   b = ξ²/2
```

with lapse N = e^σ on a closed leaf Σ, multiplier L, heat field W, Δ_h the leaf
Laplacian, M_P² the reduced Planck mass squared and c_N the G-ratio factor of
the Friedman kernel. Framework input adopted: `a0 = κ c √(G ρ_Λ)` with κ = 1/2.

## 1. Integration by parts with varying lapse (the seed's first derivation)

On a closed leaf (no boundary), for the weighted inner product
`⟨f,g⟩ := ∫_Σ N √h f g` the geometric Laplacian `Δ_h = div_h ∘ grad_h` integrates
by parts by parts on the *unweighted* measure `√h`:

```
∫_Σ √h f Δ_h g = −∫_Σ √h ⟨Df, Dg⟩         (standard, N ≡ 1)
```

With the lapse weight N = e^σ inside, the N does not commute with ∂:

```
∫_Σ N √h f Δ_h g  =  −∫_Σ N √h ⟨Df, Dg⟩  −  ∫_Σ N √h f ⟨Dσ, Dg⟩
```

because `div_h (N Dg) = N Δ_h g + ⟨D N, D g⟩` (product rule for the weighted
divergence), i.e. the integration by parts picks up a lapse-gradient term. With
N = e^σ and `D N = N Dσ = N D ln N`:

```
∫_Σ N√h L Δ_h W  =  − ∫_Σ N√h [ ⟨DL, DW⟩ + L ⟨D ln N, DW⟩ ]      (IBP-σ)
```

The NEGATIVE CONTROL is the naive identity that drops the second term,
`∫ N√h L Δ_h W = −∫ N√h ⟨DL,DW⟩`; it is false for nonconstant lapse and
*must* fail numerically (section 4).

## 2. The heat-field metric stress (the seed's second derivation)

Variation of the block under `h → h_ε = e^{2εχ} h` (δh_ij = 2εχ h_ij at ε=0).
The conformal Laplacian identity `Δ_{e^{2f}h} φ = e^{−2f} ( Δ_h φ + ⟨Df, Dφ⟩_h )`
carries the derivative into the leaf measure and the differential operators:

- `δ(N√h) = N√h · ½ h^{ij} δh_ij` (volume element),
- `δΔ` contributes from both the conformal shift of the operator and the
  derivative of the kernel argument (∂_r W term is ε-independent),
- the IBP-σ identity of §1 converts every `∫ N√h L·(−δΔ)W·…` back into
  `½h^{ij} B0`-type contractions.

Result: with

```
B0(x)          = L ∂_r W + ⟨DL, DW⟩ + L ⟨D ln N, DW⟩,
Θ^{ij}(x)      = ½ h^{ij} B0 − D^{(i} L D^{j)} W − L D^{(i} ln N D^{j)} W,
```

the first variation of the heat block is

```
δ_h S_heat = (M_P² c_N / 2) ∫ dτ ∫_0^b dr ∫_Σ N √h Θ^{ij} δh_ij
```

i.e. Θ^{ij} is the heat-field metric stress (traceless part from the
`½h^{ij}B0` vs `B0` contraction; the D^{(i}·D^{j)} pieces carry the L↔W
correlations and the lapse-gradient correlation with W).

The on-shell measure statement (seed's third derivation): on `∂_r W = Δ_h W`
the direct leaf integral of the density vanishes,

```
∫_Σ N √h B0 = ∫_Σ N √h L (∂_r W − Δ_h W) = 0   (on-shell; 1D mode form: μW = W″)
```

while off-shell the IBP-σ identity gives the constraint-weighted equality
`∫N√h B0 = ∫N√h L(∂_rW − Δ_hW)` exactly.

## 3. Algebraic core, certified in Lean 4

`AS131_heat_stress_cert.lean` (verified with `lake env lean`, mathlib 4.34,
host compile only — the run dir holds the only copy):

- `periodic_integral_deriv_zero` — FTC + periodicity: ∫₀^{2π} f′ = 0 for C¹
  periodic f.
- `heat_ibp_correct` — for periodic C¹ σ, L, W with periodic W′,
  `∫ e^σ [μLW + L′W′ + Lσ′W′] = ∫ e^σ L (μW − W″)` (1D flat leaf, ∂_rW = μW).
  Proof: the integrand difference is the derivative of e^σ L W′; FTC +
  periodicity ⇒ 0. This is the IBP-σ identity of §1, lapse-gradient included.
- `heat_onshell_measure` — on μW = W″ the leaf integral is 0.
- `wrong_residual_eq` — the wrong side's defect equals the lapse-gradient
  moment `∫ e^σ L σ′ W′` exactly.
- `ibp_bracket_zero` / `wrong_ibp_bracket` + witness example — mode algebra
  W = e^{ikx}, L = e^{iqx}: correct bracket = direct bracket identically; the
  wrong bracket misses −k(q+k)Φ, and −k(q+k) ≠ 0 at (k,q) = (1,2).

`#print axioms` on every theorem: `[propext, Classical.choice, Quot.sound]`
(zero sorry, subset bar satisfied). Output kept in `lean_cert_output.txt`.

## 4. Bounded numerical verification (real residuals, controls that can fail)

Witness strategy: bandlimited functions with exactly computable spectra
(periodic spectral quadrature on T³, Gauss–Legendre×trapezoid on S²), so every
agreement below is a genuine computation, not a boolean. Nonconstant lapse
(N = e^{0.4cos θ} on S²; N = e^{0.3cos x1} on T³) so the lapse-gradient term is
nonzero. Complete stdout: `run_stdout.txt`.

| check | content | residual | tolerance | verdict |
|---|---|---|---|---|
| A1 | flat T³: direct == correct IBP (lapse-gradient included) | 2.22e-16 | 2.0e-10 | PASS |
| A2 | **negative control**: wrong-IBP (lapse term dropped) | 1.249795e-01 | > 1e-4 | PASS (fails as required) |
| A3 | constant-lapse limit of the identity | 9.02e-17 | 2.0e-10 | PASS |
| B1 | curved T³ (Γ present): direct == correct IBP | 0.0 | 5.0e-10 | PASS |
| B2 | **negative control** curved T³: wrong-IBP | 1.352703e-01 | > 1e-3 | PASS (fails as required) |
| C1 | stress: IBP-eval == operator-eval (ε=+1e-6) | 2.22e-16 | 5.0e-10 | PASS |
| C2 | stress: FD dS/dε (central) == Θ^{ij} prediction | 7.49e-11 | 2.0e-09 | PASS |
| C3 | stress: FD dS/dε (5-point) == Θ^{ij} prediction | 5.64e-11 | 2.0e-09 | PASS |
| C4 | **negative control**: wrong stress (lapse term dropped) | 5.203229e-03 | > 1e-6 | PASS (fails as required) |
| D1 | anisotropic variation: FD == Θ^{ij} prediction | 3.18e-18 | 2.0e-09 | PASS |
| E1 | on-shell measure: ∫N√h B0 = 0 (closed leaf) | 6.29e-18 | 5.0e-10 | PASS |
| E2 | on-shell identity: B0 = div_N(L DW) pointwise (sup norm) | 1.91e-12 | 5.0e-09 | PASS |
| E3 | off-shell identity: ∫N√h B0 = ∫N√h L(∂_rW−Δ_hW) | 2.22e-16 | 5.0e-10 | PASS |
| F1 | S² leaf (96×192): direct == correct IBP | 7.28e-14 | 2.0e-07 | PASS |
| F2 | S² leaf refined (192×384): direct == correct IBP | 3.66e-13 | 2.0e-09 | PASS |
| F3 | **negative control** S²: wrong-IBP | 8.693067e-01 | > 1e-4 | PASS (fails as required) |

16/16 pass; 4/4 negative controls fail exactly as required. Bounds actually
enforced: wall 0.30 s ≤ 120 s (script-timed + `/usr/bin/time` real 0.33),
maxrss 215.7 MiB ≤ 512 MiB (measured via resource.getrusage; the RLIMIT_AS
soft cap could not be *set* on macOS — soft > hard — so enforcement is by
measured usage on grids sized to fit: 64³ T³, 96×192/192×384 S²), threads 1.

Witness phases were tuned so the discarded lapse term has nonzero integral
(cos(2x2) lapse-coupling on T³; L2 = cos(2x1+x2), W2 = cos(x1+x2); L = P3, W = P2
on S²) — the controls genuinely bite.

## 5. Failed attempts (preserved in the patch history of verify_heat_stress.py)

- Run 1: B2/C4 witness flaws (discarded term integrated to zero for the
  chosen modes — control not biting) and F1/F2 quadrature errors (double
  Jacobian; dropped L factor).  Fixes: S² quadrature via u-domain GL, exact
  lpmv derivatives, L-carrier restored.
- Run 2: B2/C4 still vanishing — orthogonal phases; fixed by mode retuning.
- Run 3: C4 self-cancellation (4×-harmonic orthogonality); final phase fix.
Final run: 16/16 pass, exit 0.

## 6. What this does not establish

1D-flat/2-sphere-embedded witnesses only; the full quotient-leaf/torus assembly
of the constraint across the r-interval with the truncated kernel argument
b = ξ²/2 is not here computed; no statement about the other blocks of + and −
GNC actions or about observable values; κ = 1/2 is adopted input, not derived;
both footings (9.3619e-11, 1.1279e-10 m/s²) appear only as constants of the
kernel cell (constants line in run_stdout.txt), the metric stress itself is
scale-free in the witness normalization.