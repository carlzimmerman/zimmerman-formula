# AS133 — Derive the terminal heat boundary condition (Tier-0 seed)

Run: `AS133-r1-20260928T160117Z-dsv4f-hermes` · worker dsv4f-hermes
(deepseek/deepseek-v4-flash-0731, provider openrouter, Hermes Agent focused
subagent; identity taken from the executing system context) · task_sha256
`1a03b8f0f6c756a04f63fe4556d76805dda29e4f68608b98b30381869984a30b` (verified
on disk before execution).

## 0. Pinned target and conventions (seed step 1)

Source: `real_research/common_action_2026_09_26/action/FINAL_ACTION.md`
(sha256 `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e`,
verified against SOURCE_MANIFEST.json). Seed branch: CA5-GNC-R with inherited
CA4-GNC host; heat sector eqs. (3)–(7) of FINAL_ACTION.md:

```
Y_h = J(DW_b) + ell Delta_h W_b - theta,     f = G'(Y_h),        (3)
J_p = 4 (nu_mono(|p|/a0) - 1) p                                    (oper. branch)
R_W = -div_N(f J_p + ell a) + ell N^-1 Delta_h (N f),  a = D ln N  (5)
partial_r W = Delta_h W,  W_0 = U,  partial_r L = -N^-1 Delta_h(N L),
L_b = -R_W,  lambda_0 = L_0                                       (7)
div_N = N^-1 div_h (N .)
```

Independent fields on the CA5-GNC-R common action, before elimination: lapse
`N = e^sigma > 0`, leaf metric `h` (flat leaf here), heat field `W(r,x)`,
multiplier `L(r,x)`, residual `U`, clock source `Z` (not exercised); gate
`G(Y_h)` smooth with compact ramp, `G'(Y_h) = f`; coefficients fixed inputs:
`ell > 0` (0.04), `theta > 0`, gate ramp width `dG`, `b = xi^2/2 > 0`, `c_N`,
`kappa = 1/2` adopted with `a0 = kappa c sqrt(G rho_Lambda)`. Kernel bills of
the gate: MONO is operative (`nu_mono` = filtered monotone continuation of
RAR, splice `delta = 0.05`, computed landmarks y_star = 2.3374124486855816,
y_p = 2.539639390200043 vs pinned 2.3374/2.5396, |err| = 5.3e-6, splice
continuity 1.3e-11); Q, RAR, MU2, EXP are distinct branches not exercised
(out of scope for this seed's conclusions).

## 1. Variation of the heat block under delta W_b (seed step 2)

Heat block of the action, measure `N sqrt(h)`:

```
S_heat = int N sqrt(h) { c_N [ G(Y_h) + ell a . DW_b ] + c_N int_0^b dr L [partial_r W - Delta_h W ] }
```

(signs/conventions of FINAL_ACTION eq. (4); constant prefactors M_P^2/2, c_N
cancel in every identity below). Terminal free variation: `delta W_b`
supported at one point of the closed leaf (`W(r)`, `L`, `U` fixed; only the
r = b endpoint data varies, `delta W_b` arbitrary pointwise).

Gate variation (the three constituents of step 2, each integration by parts
explicit):

```
delta S_gate = c_N int N sqrt(h) [ f (J_p . D delta W_b) + ell f (Delta_h delta W_b) + ell a . D delta W_b ]
```

Using the closed-leaf IBP with the weighted divergence `div_N = N^-1 div_h(N .)`:

```
int N sqrt(h) u . D v  = - int N sqrt(h) v div_N u,
int N sqrt(h) u Delta_h v = int N sqrt(h) v [N^-1 Delta_h (N u)]   (Delta_h self-adjoint in sqrt(h))
```

Hence, for `delta W_b = d` supported at the site:

```
delta S_gate / delta W_b  =  c_N N sqrt(h) [ -div_N (f J_p + ell a) + ell N^-1 Delta_h (N f) ]  =  c_N N sqrt(h) R_W
```

which is check B below (direct central finite difference of `S_gate` w.r.t.
`W_b` at the site vs `N sqrt(h) R_W`).

Flux variation: the transport term only couples to `delta W_b` through the
r-endpoint term of its r-integration by parts,

```
int_0^b dr L partial_r W = [ L W ]_0^b - int_0^b dr W partial_r L
        =>  delta S_flux / delta W_b  =  c_N N sqrt(h) L_b
```

Total terminal coefficient of the free variation `delta W_b`:

```
delta S_heat / delta W_b  =  c_N N sqrt(h) ( L_b + R_W )
```

## 2. Terminal heat adjoint boundary condition and its sign (seed step 3)

Stationarity of the free endpoint variation requires the total terminal
coefficient to vanish pointwise; with the on-shell backward heat equation
(7) `partial_r L = -N^-1 Delta_h (N L)`, the r-profile is fixed by its
terminal datum, and the derived condition is

```
L_b = - R_W          (terminal heat adjoint boundary condition; sign negative)
```

Equivalently `L_b + R_W = 0` (certified as `endpoint_closed`; Lean T3).
With `L_b^naive = -R_W^naive` the terminal coefficient of a naive candidate
is `N sqrt(h) (L_b^naive + R_W) = -ell N sqrt(h)[ (Delta_h(Nf))/N - Delta_h f ]`
(Lean T4/T5), which survives for nonconstant N — the seed's mandated negative
control, required to fail (section 4).

Discrete substitution-back (exact, symbolic, 2 spatial cells, periodic flat
leaf, r slices k = 0,1 with slice 2 = b): residues of the full r-variation
reduce by discrete integration by parts to

```
(i)   raw gate coefficient  ==  N_i R_W,i            (residual 0 exactly)
(iii) total coefficient of delta W_b == N_i (L_1,i + R_W,i)   (residual 0 exactly)
```

with `L_1 = L_2 + dr (Delta_N L)_2` the discrete backward heat step. This is
check A2 (exact zeros; the seed's "substitute back into the original
equation").

Continuum terminal condition, numerically: the backward profile is solved
exactly in the spectral semigroup after the substitution `L~ = N L`,
`partial_r L~ = -Delta_h L~`, so

```
L(r) = N^-1 e^{(b-r) Delta_h} (N L_b),   L_b = -R_W
```

The discrete contact value `L(b - dr) + R_W` is the terminal-coefficient
residual on a grid with slice spacing dr; it measures exactly the semigroup
damping `(1 - e^{-dr k^2})` per Fourier mode and decays to 0 as
`dr * lambda_max -> 0` (chain below, check C-on).

## 3. Numerics and the two R_W forms (checks A, A2, B, C, D)

Model: flat 32x32 torus (leaf torus, h = 1 in the flat-leaf limit so
`sqrt(h) = 1`, `Delta_h = Delta`, `c_N sqrt(h) = 1` at the site),
`N = exp(0.30 sin(2 pi X) + 0.20 cos(2 pi Y))` (positive, nonconstant),
`Wb = 1.40 (cos(2pi X) + 0.5 sin(2pi Y))`, `ell = 0.04`, gate ramp
`G(Y) = 0 (Y<=0), dG(7r^5-14r^6+10r^7-2.5r^8) (0<Y<dG), Y-dG/2 (Y>=dG)`,
`r = Y/dG`, `dG = 40`, `theta = 8`, `b = 0.5`, eps values in each check.

- A (two forms of R_W, check A1): canonical `R_W = -div_N(f J_p + ell a) +
  ell N^-1 Delta(N f)` vs the explicit form `R_W = -div_N(f J_p) + ell (f-1)
  div_N a + 2 ell a . Df + ell Delta f` — symbolic difference simplifies to
  0 (exact); the bridge identity `(Na)'/N - N''/N = 0` also exactly 0.
- B (gate direct FD): central FD `eps = 1e-5` of `S_gate = sum N (G(Y_h) +
  ell a . DW)` w.r.t. `W_b` at site (16,10) vs `N[s] R_W[s]`:
  analytic-jmode rel 4.85e-6 (canonical form), 4.07e-6 (alternative form);
  MONO-jmode rel 6.9e-8 / 1.5e-7. Tolerance 1e-4. PASS both footings.
- C (terminal condition): `L(r) = N^-1 e^{(b-r)Delta}(N L_b)` with
  `L_b = -R_W`; discrete identity (`raw = L_low + R_W`) rel 5.0e-5 (n=16;
  residual dominated by the non-band-limited ramp f, aliasing-quantified).
  Continuum limit, canonical, n=8: `L_low + R_W` = 20.31259 (Nr=40),
  11.84598 (320), 2.29079 (2560), 0.30507 (20480), 0.07680 (81920) —
  monotone decay to 0 at the semigroup rate `1 - e^{-dr k^2}`; alternative
  footing: 19.87363, 11.32557, 2.17918, 0.29020, 0.07306 — same behavior.
  NAIVE replacement (`L_b^naive = -R_W^naive`): terminal value 30.2651
  (Nr=40) vs on-shell 29.5157 at identical (n,Nr): residual 0.75 differs and
  survives refinement — the endpoint residual does NOT vanish for the naive
  candidate.
- D (on-shell chain through U): `W_b = S_h U` (`S_h = e^{b Delta}`);
  variation of the full action w.r.t. `delta U` at site (8,5) equals
  `N (S_h^dag R_W)`: analytic-jmode rel 2.2e-8 (canonical) / 3.3e-8
  (alternative); MONO-jmode 3.42e-4 (limited by the J-quadrature derivative
  interpolation, tolerance 1e-3). PASS.

## 4. Negative control (seed step 4; must be capable of failing)

Replace `Delta_h (N f)/N` by `Delta_h f` at nonconstant N (a "lapse-free"
misreading of the weighted Laplacian):

```
R_W^true - R_W^naive = ell [ (Delta_h(N f))/N - Delta_h f ]
                    = ell [ 2 a . D f + f (Delta_h N)/N ]     (exact identity)
```

- exact identity: product rule core `Delta(Nf) - N Delta f - 2 DN . Df - f
  Delta N = 0` on band-limited data: max abs 4.5e-12 (= machine zero); full
  identity rel residual 1.8e-6 (n=32) -> < 1e-15 (n=64): exponential aliasing
  decay of the non-band-limited pieces `1/N`, `ln N` (stated and quantified).
- survival on real data: `|endpoint R_true - R_naive|_max = 3.64`, matches
  `ell [(Delta(Nf))/N - Delta f]` to 0.0; pointwise lapse residue max 91.0.
- degenerate sector: constant N collapses the residual to 3.6e-12 —
  the control is capable of failing and only passes trivially there.

Summary: control FAILS AS REQUIRED (survives) at nonconstant N; the seed's
mandated replacement is falsified exactly by the lapse-residue terms.

## 5. Lean certificate

`AS133_terminal_heat_boundary.lean`, compiled with
`cd fable_independent_2026/lean_2026 && lake env lean <abs>.lean` (exit 0),
mathlib/lean 4.34.0-rc2, six theorems, zero `sorry`:

- `Nf_double_deriv` — `(N f)'' = N'' f + 2 N' f' + N f''` (deriv-mul, twice);
- `measure_residual` — `(Nf)''/N - f'' = 2 (N'/N) f' + (N''/N) f` (the measure
  residue / canonical-relation identity, field_simp + ring);
- `endpoint_closed` — `Lb = -R => Lb + R = 0` (terminal closing);
- `terminal_control_residual` — `R - Rnaive = ell*measure, Lb = -R,
  Lbnaive = -Rnaive => Lb - Lbnaive = -ell*measure` (control failure mode);
- `terminal_control_residual_deriv` — analytic instance with the measure
  residue of `measure_residual`;
- `rw_forms_1d` — the two R_W forms agree iff `(Na)'/N = N''/N` and the
  measure identity hold (check A core).

Unfiltered `#print axioms` for all six: exactly
`[propext, Classical.choice, Quot.sound]` — inside the allowed set; no
additional axioms, no sorry.

## 6. Domain, bounds, footings

- Domain: flat compact torus leaf, 32x32 (16x16 and 8x8 for the refinement
  chain), positive nonconstant N, smooth gate jets and constant ramp,
  `b > 0`, free supported-at-b endpoint variation; no spatial boundary terms
  (closed leaf). Exact: 2-cell periodic torus, 3 r-slices.
- Bounds actually enforced: SIGALRM at 120 s (in-process), single thread
  (`OPENBLAS/OMP/MKL/VECLIB_NUM_THREADS=1`), measured wall 7.54 s
  (final full run; all research runs < 14 s), measured peak RSS 309 MB
  < 512 MB declared ceiling; macOS RLIMIT_AS is unavailable as in AS131 —
  the measured peak is the guarantee.
- Footings: the derived boundary condition is a dimensionless identity in a0
  (a0 enters only through the footing ratio `y = |DW_b|/a0` inside `nu_mono`
  and cancels in `L_b = -R_W`): one proof applies identically to canonical
  a0 = 9.3619e-11 m/s^2 (rho_Lambda = 5.8444e-27 kg/m^3, r_M(M_sun) =
  0.038586 pc, v_flat = 333.87 m/s) and alternative a0 = 1.1279e-10 m/s^2
  (rho_Lambda = 8.4831e-27 kg/m^3, r_M(M_sun) = 0.035154 pc, v_flat =
  349.78 m/s); footing ratio 1.20478; fixed-rho effective kappa 0.60239;
  fixed-kappa rho ratio 1.45149 — the two footings never share fixed rho AND
  fixed kappa. `G_N`, `G_bare`, `G_cosmo` kept as separate symbols
  (FINAL_ACTION eq. (18) `G_cosm/G_N = c_N`); c_N cancels in the identity.

## 7. Exact claim (scoped)

On the CA5-GNC-R common action heat sector (FINAL_ACTION.md pinned hash,
eqs. (3)–(7)), on a compact flat closed leaf with positive lapse and smooth
gate jets, under the N sqrt(h) measure with each integration by parts
explicit, the terminal heat adjoint boundary condition is

```
delta S_heat / delta W_b = c_N N sqrt(h) (L_b + R_W),   L_b = -R_W,
R_W = -div_N (f J_p + ell a) + ell N^-1 Delta_h (N f),
```

verified by (i) exact 2-cell symbolic substitution-back (raw gate = N R_W,
total = N(L_1 + R_W); residuals 0), (ii) direct gate finite difference at
32x32 (rel 5e-6 analytic / 7e-8 MONO vs tolerance 1e-4), (iii) on-shell
semigroup chain with monotone terminal residual -> 0 (0.077 at Nr = 81920),
(iv) the seed's negative control surviving exactly at nonconstant N
(r = ell[(Delta(Nf))/N - Delta f], max 3.64; naive terminal value 30.27 vs
29.52 on-shell) and collapsing at constant N (3.6e-12), and (v) Lean 4
certificate, 6 theorems, zero sorry, axioms exactly
{propext, Classical.choice, Quot.sound}. The condition is a0-free
(`J_p = 4(nu_mono-1)p`), hence holds under BOTH canonical and alternative
footings; MONO is the operative gate branch. This is a derived conditional
identity of the candidate's heat sector — not a promotion to complete
gravity closure.