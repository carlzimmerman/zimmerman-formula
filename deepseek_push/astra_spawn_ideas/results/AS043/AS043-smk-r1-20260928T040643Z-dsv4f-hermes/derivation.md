# AS043 — Smoothing kernel statistical interpretation

Run: `AS043-smk-r1-20260928T040643Z-dsv4f-hermes`
Worker: hermes-agent subagent (deepseek/deepseek-v4-flash-0731 via openrouter)
Started: 2026-09-28T04:06:43Z — Finished: 2026-09-28T04:48:55Z

> **Seed-file notice.** The dispatched file `AS043_smoothing_kernel_statistical_interpretation.md`
> does not exist in the repository (verified by file search, `git log --all`, `git rev-list --all
> --objects`, and catalog/manifest scans). The repo's AS043 slot is the different task
> *"Constant acceleration and the external field"*, owned by worker sa-4-bd5c1481 (running;
> `results/AS043/` contains no files from that worker — this run's unique directory does not
> collide). Task content is therefore executed from the dispatch text, reproduced in
> `seed_as_dispatched.md` (hashed as task_sha256). No claims file was created or altered.

---

## 1. Precise claim audited

**Dispatch claim.** The heat filter

```
S = exp[(xi^2/2) Delta]
```

can be read statistically: "Gaussian smoothing kernel of width xi in Euclidean measure".

**Audit verdict (strongest surviving statement).**

Let M = R^3 with the flat Euclidean metric, measure d^3x, free/bounded domain chosen
appropriately, and let S = exp[(xi^2/2) Delta] with Delta the flat Laplacian.

1. **Exact kernel form.** On the Euclidean cell, S is convolution with the exact Gaussian
   probability kernel of width xi (standard deviation xi per axis, covariance xi^2 I_3):

   ```
   (S f)(x) = ∫_{R^3} G_xi(x-y) f(y) d^3y,   G_xi(r) = (2 pi xi^2)^(-3/2) exp(-|r|^2/(2 xi^2)),
   ∫_{R^3} G_xi = 1  (Leaned),   ∫ x^2 G_xi dx = xi^2  (width exact, C2c).
   ```

   Equivalently (S f)(x) = E[f(x + xi Z)] with Z ~ N(0, I_3) (C3, MC residual 6.7e-4 ~ 1/sqrt(M)).
   Fourier symbol: exp(-xi^2 |k|^2 / 2). Kernel form verified to machine precision (C1: 4.4e-16,
   C1b: 3D separability 4.9e-17). This is the heat kernel of |xi-scaled| Laplacian at time xi^2/2.

2. **Adjoint in L2 vs the GALACTIC measure — specified.**
   - *L2 (Euclidean measure d^3x):* S is self-adjoint: `S* = S` (symmetric real Gaussian kernel;
     verification C4: |<Su,v> - <u,Sv>| = 3.5e-18).
   - *GALACTIC measure dmu_N = N sqrt(h) d^3x* (lapse-weighted proper-volume measure, the measure
     used in the operative leaf action and in AS205's pairing ⟨v,u⟩_N = ∫ N v u dvol_h):
     the adjoint is the **lapse-conjugated operator**

     ```
     S*_gal = N^{-1} S N        (flat leaf: sqrt(h)=1)
     S*_gal = N^{-1} S_h N      (general leaf, S_h = exp[(xi^2/2) Delta_h])
     ```

     i.e. ⟨v, S u⟩_N = ⟨N^{-1} S (N v), u⟩_N, matching AS205's identity. Verification C5:
     exact to 6.9e-18 for a nonconstant lapse N(x)=1+0.3cos(3x)+0.1sin(5x).
   - **Self-adjointness in the L2 measure does NOT carry to the galactic measure:** the negative
     control asserting ⟨v,Su⟩_N = ⟨u,Sv⟩_N (i.e. S* = S in galactic measure) FAILS for
     nonconstant lapse — gap 1.2e-3 (C5 control triggered). S is self-adjoint in dmu_N iff
     [S,N] = 0, which for a smoothing (nonlocal) operator on a nonconstant lapse is generically
     false. This confirms the framework-contract warning verbatim.

3. **Does the statistical reading add or subtract assumptions?**
   - **Subtracts nothing.** The Gaussian-kernel form is an exact identity on the Euclidean cell;
     the statistical reading is a faithful *representation* of S there, not a truncation.
   - **Adds (implicit) assumptions when transplanted off the Euclidean cell:**
     (i) Euclidean flat measure and coordinates (unit lapse N=1, sqrt(h)=1) — the operative
     definition does NOT assume these; (ii) domain/boundary conditions must be fixed — on a
     periodic domain the exact kernel is the *wrapped* Gaussian (sum over images), differing from
     the free Euclidean Gaussian by O(exp(-L^2/8 xi^2)) (C6 control triggered, l1 diff 6.9e-2);
     (iii) the statistical reading supplies a probability interpretation (expectation over
     Gaussian draws) that carries no dynamical content — it is a reading, not a mechanism; the
     operative MONO equation needs S only as a filter, and (iv) the *statistical reading by
     itself says nothing about the adjoint*, and the naive reflexive guess S* = S fails in the
     galactic measure. Net: as a claim about the operator on the flat Euclidean cell it is exact
     and assumption-neutral; as a claim about the operative galactic action it is exact only
     after adding (measure, lapse, domain) specification that the operative definition leaves
     open, and the adjoint must be computed in the chosen measure (N^{-1} S N), not read off the
     symmetric kernel.

Domain of the claim: flat Euclidean leaf (or flat periodic cell with wrapped kernel),
xi > 0 finite; scalar functions, standard Laplacian; galactic measure with positive lapse N
and leaf volume sqrt(h). Branch-agnostic (operator identity; no a0 or branch function enters).

## 2. Derivation

### 2.1 Kernel form

Free heat kernel of the flat Laplacian in d dimensions, time t = xi^2/2:

```
K_t(r) = (4 pi t)^(-d/2) exp(-|r|^2 / (4t)) ;  4t = 2 xi^2  =>  K = (2 pi xi^2)^(-d/2) exp(-|r|^2/(2 xi^2)).
```

Sanity: (4 pi t) = 4 pi (xi^2/2) = 2 pi xi^2; exponent |r|^2/(4t) = |r|^2/(2 xi^2). Gaussian
density with covariance matrix xi^2 I_d; width per axis = xi. Normalization: Euler-Gauss
integral ∫ exp(-x^2/(2 xi^2)) dx = sqrt(2 pi) xi, so ∫ G_xi = (sqrt(2 pi) xi / (sqrt(2 pi) xi))^d = 1.
Second moment: ∫ x^2 G_xi dx = xi^2 (Euler-Gauss with b = 1/(2xi^2): ∫ x^2 e^{-b x^2} = sqrt(pi)/(2 b^{3/2})).

### 2.2 Statistical reading

(S f)(x) = (G_xi * f)(x) = E_{Z~N(0,I_3)}[f(x + xi Z)] for a suitable class f. Verified by
Monte Carlo (C3): E[f(x0+xi Z)] vs (S f)(x0), residual 6.7e-4 with 4e5 samples (1/sqrt(M)=1.6e-3 noise floor).

### 2.3 Adjoint by measure (derivation)

L2 (Euclidean, flat leaf, d^3x): S symmetric kernel => S* = S.

Galactic measure dmu_N = N sqrt(h) d^3x (N>0 laps, h leaf metric; AS205 pairing:
⟨v,u⟩_N = ∫ N v u dvol_h). For any v,u in the domain:

```
⟨v, S u⟩_N = ∫ N v (S u) dvol_h = ⟨N v, S u⟩_{L2(dvol_h)}
           = ⟨S (N v), u⟩_{L2(dvol_h)}      (S self-adjoint in L2(dvol_h): heat semigroup of self-adjoint Delta_h)
           = ∫ (S (N v)) u dvol_h = ∫ N [N^{-1} S (N v)] u dvol_h
           = ⟨N^{-1} S (N v), u⟩_N.
```

Hence S*_gal = N^{-1} S N (operator composition: multiply by N, apply S, divide by N). For
flat leaf take S = S_h = heat filter; formula structure identical to AS205.

Self-adjointness in galactic measure: S*_gal = S <=> N^{-1} S (N ·) = S(·) <=> [S,N]=0 on the
domain; false for generic nonconstant lapse (S smooths, N multiplies) — demonstrated by the
negative control gap (1.2e-3 on a 512-cell periodic cell, N amplitude ~0.3-0.4).

### 2.4 Steps/units check

- xi is a length [m]; Delta [m^-2]; exponent (xi^2/2)Delta dimensionless. Kernel G_xi has
  [m^-d], ∫ G_xi d^dx = 1 dimensionless. No G, c, a0 or rho_Lambda appears in the operator
  identity: the audit is a0-independent and holds identically on both footings. Dimensional
  examples with the framework inputs are given in C7 only as anchors (r_M values).
- The framework's G_N/G_bare/G_cosmo separation is untouched: no coupling was set equal; the
  audit never needs any G.

## 3. Controls (all with pre-set tolerances)

| Check | What it verifies | Observed | Tolerance | Pass |
|---|---|---|---|---|
| C1 | kernel form, periodic 1D: FFT symbol vs direct Gaussian convolution | 4.4e-16 | 1e-8 | PASS |
| C1b | 3D kernel form via separability (3x 1D filters = 3D symbol) | 4.9e-17 | 1e-8 | PASS |
| C2 | 1D normalization ∫G_xi | 1.0000000000000002 | 1e-6 | PASS |
| C2b | 3D normalization = (∫_1D)^3 | 1.0000000000000007 | 1e-3 | PASS |
| C2c | second moment ∫x^2 G_xi = xi^2 | 2.4999998128e-3 | 1e-6 | PASS |
| C3 | statistical reading E[f(x0+xi Z)] = (S f)(x0) | 6.7e-4 | 3e-3 | PASS |
| C4 | L2 self-adjointness ⟨Su,v⟩=⟨u,Sv⟩ | 3.5e-18 | 1e-8 | PASS |
| C5 | galactic adjoint ⟨Su,v⟩_N = ⟨u, N^{-1}S(Nv)⟩_N | 6.9e-18 | 1e-8 | PASS |
| C5-neg | **negative control**: naive S* = S in galactic measure must FAIL | gap 1.2e-3 | detect >1e-3 | FAILED as required (control triggered) |
| C6-neg | **negative control**: free Euclidean Gaussian vs wrapped kernel on periodic domain — exact kernel is domain-dependent, must differ | l1 diff 6.9e-2 | detect >1e-3 | control triggered |

Bounded-prototype enforcement: single-threaded numpy (OPENBLAS/OMP/MKL/NUMEXPR threads pinned
to 1), wall 0.08 s (measured by /usr/bin/time; bound 120 s), peak RSS 38.8 MB (bound 512 MB),
grid 512 cells (1D) and 64^3 (3D), 400,000 MC samples, full enumeration of the 1D convolution.
Lean compile: lake env lean, 3.7 s, peak RSS measured 5.76 GB (lake+lean process family; the
Lean verification step is exempted from the numeric-prototype memory bound as a compiler-run
artifact, recorded in execution_bounds).

## 4. Lean certificate

File `as043_gaussian_kernel.lean`. Theorems (self-contained, import Mathlib):

- `AS043.gaussian_integral_1d : 0 < xi -> ∫_R exp(-x^2/(2 xi^2)) = sqrt(2 pi) * xi`
- `AS043.kernel_normalized_1d : 0 < xi -> ∫_R K xi = 1`  (K = kernel, unit-mass probability kernel)
- `AS043.kernel_normalized_3d : 0 < xi -> ∫_{R^3} K xi x * K xi y * K xi z = 1` (product separability)

Verified: `lake env lean as043_gaussian_kernel.lean`, exit 0, zero `sorry`,
axioms printed: `[propext, Classical.choice, Quot.sound]` for all three theorems
(see `.lean.out`). The 3D statement is proved via product-measure Fubini (integral_prod_mul)
twice; the 1D theorem via `integral_gaussian` + sqrt algebra. No `sorry`; no additional axioms.

## 5. Both footings

The operator identities (kernel form, normalization, adjoints) contain no a0, G, rho_Lambda
or c: they hold identically under both a0 = 9.3619e-11 m/s^2 (canonical) and
a0 = 1.1279e-10 m/s^2 (alternative). The alternative normalization would change a0-derived
scale anchors only (e.g. r_M for a 1e10 M_sun baryon mass: 1.1906e20 m canonical vs
1.0847e20 m alternative; rho_Lambda from 4a0^2/(G c^2): 5.844e-27 vs 8.483e-27 kg/m^3),
none of which this audit uses. The audit conclusion is therefore valid on both footings
without modification.

## 6. Limitations

- The audit establishes the kernel/adjoint identities for the **flat Euclidean cell** and the
  lapse-weighted measure with explicit N; it does not compute the heat kernel of a **curved**
  leaf metric h (S_h kernel form on curved leaves is not the Euclidean Gaussian — noted, not
  derived; candidate follow-up: small-xi heat-kernel expansion on curved leaves).
- No derivation of ξ from the action or from a0: ξ remains the free filter length in the
  operative definition (as the contract leaves it).
- The wrapped-kernel control (C6) establishes domain-dependence of the *exact* kernel; on the
  flat unbounded R^3 the free Gaussian is exact (C1).
- `S*` of the *vector* operator inside the MONO divergence term (S* div[...]) was not
  re-derived here; the audit covers the scalar S and its measure-adjoint, which is the
  dependence the contract's sentence "self-adjointness in one measure does not imply it in
  another" refers to. The vector case inherits the same measure weight (N^{-1} · N applied to
  the dual divergence) — flagged for AS600-type follow-up.
- The seed file does not exist in the repository; the audit follows the dispatch text
  (transparency section above). Repo-AS043 (constant acceleration) belongs to sa-4-bd5c1481
  and was not touched.
