# AS061 — Vacuum energy does not fix linear susceptibility

**Group:** A03 — Coefficient mechanisms and their missing premises
**Run ID:** `AS061-r1-20260928T090150-7189aade`
**Task seed:** `deepseek_push/astra_spawn_ideas/AS061_vacuum_energy_does_not_fix_linear_susceptibility.md`
(sha256 `f374623b861fd37caa88a60abdb5ebf6afab59ec121b970aea88b6223691fc6f`, verified before execution)
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter; Hermes agent subagent, macOS host)
**Started / finished (UTC):** 2026-09-28T09:01:50Z / 2026-09-28T10:52:14Z

---

## 1. Precise claim, symbol dictionary, boundary conditions, assumptions (seed step 1)

**Claim (the seed's named statement, executed as written).** In the static scalar-kinetic
action of the PD08 particle-free class,

```
S = (1/8 pi G) INT s^2 K(|grad Phi|^2/s^2) d^3x - INT rho_b Phi d^3x,
K(X) = C0 + eps*X + alpha*X^(3/2),   alpha > 0,   X = |grad Phi|^2/s^2,
```

(i) the field equations are invariant under the vacuum-energy renormalisation
`C0 -> C0 + Delta` — vacuum energy is a **null direction** of the response;
(ii) the zero-gradient linear-response tensor is `chi_ij(0) = eps * delta_ij` exactly:
`eps > 0` gives a quasi-Newtonian (Poisson) linear response, `eps = 0` gives a
**degenerate** susceptibility with the deep MOND wedge `mu(Y) ~ (3 alpha/2) Y`
(`a0`-line `g^2 = a_deep g_N`, `a_deep = 2s/(3 alpha)`);
(iii) **choosing zero vacuum energy is not the same as imposing a degenerate MOND
susceptibility** — `C0 = 0` does not imply `mu(0) = 0`, and `eps = 0` does not imply
`C0 = 0` (both negative controls executed and capable of failing).

**Symbol dictionary.**
`Phi` = gravitational potential; `rho_b` = baryonic mass density; `G` = Newton's constant;
`s = c sqrt(G rho_Lambda)` = gradient normalisation (acceleration units, m/s²);
`Y = g/s` = dimensionless drive with `g = |grad Phi|`; `mu(Y) = K'(Y^2)` = flux coefficient;
`J_i = mu(Y) d_i Phi`; `a0 = (c/2) sqrt(G rho_Lambda)` (framework base, kappa = 1/2 adopted);
`r_M = sqrt(G M_b / a0)`; deep `v_flat^4 = G M_b a0`; `C0` = vacuum-energy constant
(J/m³-scaled in the action through `s^2`); `eps` = linear susceptibility; `alpha` = deep
coefficient; `lambda` = diagnostic value of `eps` in {1/2, 1, 2}; `n >= 1` = channel count
(no physics derived from `n`).

**Boundary conditions / regime.** Isolated static point-mass or smooth `rho_b`;
the response is read off the constitutive law `div(mu grad Phi) = 4 pi G rho_b` with
`mu(Y) = eps + (3/2) alpha Y` on the positive drive axis and `mu(0) = eps` at zero gradient.
The Taylor truncation `K = C0 + eps X + alpha X^(3/2)` has validity window `Y << 1`
(relative neglected term of the next Taylor term; quantified in step 3).

**Framework inputs vs conclusions.** INPUTS (adopted, not derived here): `kappa = 1/2`
(`a0 = (c/2) sqrt(G rho_Lambda)`), `G`, `c`, `rho_Lambda`, the two registered footings
`9.3619e-11` and `1.1279e-10 m/s^2`, and the shape `K(X) = C0 + eps X + alpha X^(3/2)`.
CONCLUSIONS (established here): C0-invariance of the EL equation; the exact tensor
`chi_ij(0) = eps delta_ij`; the exact degenerate limit `g^2 = (2s/3alpha) g_N` at `eps = 0`;
the scale pinning `alpha = 4/3` at kappa = 1/2; both negative controls.

**Sources inspected** (hashes verified against SOURCE_MANIFEST.json before computation):
`deepseek_push/PD01_polarization_count.py` (sha256 `37e39d1a…2c74d`),
`deepseek_push/PD08_particle_free_derivation.py` (sha256 `83f6054c…f0cfb`) — source of the
action class and of `mu(Y) = K'(Y^2)`,
`kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.py` (sha256 `8df5a3ab…35b25`) —
k01's K1 statement ("vacuum energy enters only through J'") is the mirror of C1b.

---

## 2. Variation of the static functional (seed step 2)

Vary `Phi -> Phi + dPhi` in `S`. With `X = |grad Phi|^2/s^2`, `delta X = 2 grad Phi · grad dPhi / s^2`,
the kinetic term gives

```
delta S_K = (1/4 pi G) INT s^2 K'(X) (grad Phi · grad dPhi)/s^2 d^3x
          = (1/4 pi G) INT [ s^2 (1/s^2) K'(X) ] grad Phi · grad dPhi d^3x
          = -(1/4 pi G) INT div( K'(X) grad Phi ) dPhi d^3x        (partial integration)
```

so stationarity yields the Euler–Lagrange equation

```
div( mu(Y) grad Phi ) = 4 pi G rho_b,      mu(Y) := K'(Y^2),   Y = g/s.
```

**Signs and units:** `[s] = m/s²`, `[Y] = 1`, `[mu] = 1`, `[rho_b] = kg/m³`, `[Phi] = m²/s²`,
`[K] = 1` (dimensionless in `X`); `C0·s²/(8πG)` carries the vacuum energy density in J/m³
(checked numerically: canonical `eps_vac(C0=1) = s²/(8πG) = 2.089981e-11 J/m³`).

**C0 invariance (i).** `dK/dX = eps + (3/2) alpha sqrt(X)` contains no `C0`. Adding any
`Delta` to `C0` leaves `mu`, the EL equation, and every response identical:
the field equations cannot see the vacuum energy. (k01 K1 mirror; C1b.)
Equivalently, `C0` is a **null direction** of the response functional.

**Zero-gradient linear-response tensor (ii).** From `J_i = mu(Y) d_i Phi`,

```
chi_ij = dJ_i / d(d_j Phi) = mu delta_ij + (mu'/sY) d_i Phi d_j Phi,   mu' = d mu/dY.
```

The second term carries the field components and is singular-looking at `Y = 0`
(`mu'/sY ~ alpha` — finite, but multiplied by `d_i Phi d_j Phi -> 0`). It is analysed by
**limit, not by point substitution**: scale probe `dPhi = t n` with unit directions
`n = (n1, n2, 0)`, `t -> 0`:

```
Y(t) = g(t)/s = t/s,
chi_ij(t) = mu(t/s) delta_ij + (3 alpha/2) t n_i n_j,
```

where `mu(t/s) = eps + (3 alpha/2)(t/s)`. Limits are exact and direction-independent:

```
chi_11 -> eps,  chi_22 -> eps,  chi_12 -> 0    (for t -> 0, every n, every alpha > 0, any C0).
```

Direct `d/dt` route confirms the diagonal: `chi_12`-type entries ~ `eps n1`.
Longitudinal/transverse decomposition: `chi_L = mu + Y mu' = eps + 3 alpha Y`,
`chi_T = mu = eps + (3 alpha/2) Y`, both `-> eps` at `Y -> 0` (C2b).

**Consequences.** `eps > 0`: linearisation around zero field gives the Poisson operator
`eps grad^2 dPhi = 4 pi G drho` — quasi-Newtonian response with bare coupling `G/eps`.
`eps = 0`: the `grad^2` term drops out and the leading response is the deep wedge
`mu ~ (3 alpha/2) Y`, i.e. `g^2 = a_deep g_N` with `a_deep = 2s/(3 alpha)` (C2c, C3b).
The susceptibility is set by `eps`; the deep scale is set by `alpha`; the vacuum energy
is set by `C0` — three independent Taylor freedoms, **no cross-constraint** (C5d:
`kappa_model = 2/(3 alpha) = 4/3, 2/3, 1/3` for alpha = 1/2, 1, 2 while `mu(0) = 0` for all).

---

## 3. Intermediate algebra, all scale factors, leading neglected term (seed step 3)

**Point-mass constitutive law.** For `M_b` at rest, `div(mu grad Phi) = 4 pi G rho_b`
integrates to `g mu(g/s) = G M_b / r^2 =: g_N` (the standard spherical first integral).
With `Y = g/s` and `mu = eps + (3 alpha/2) Y`:

```
(3 alpha / 2s) g^2 + eps g - g_N = 0
```

— an exact quadratic in `g` (all scale factors explicit; no limit taken on the axis
`Y >= 0` where `sqrt(g^2/s^2) = g/s` is an identity, C1a).

**Newtonian regime, `eps > 0`.** Exact positive root

```
g = ( -eps s + sqrt(s) sqrt(6 alpha g_N + eps^2 s) ) / (3 alpha)
```

expands near `g_N -> 0` (sympy series, exact):

```
g = g_N/eps - (3 alpha/(2s)) g_N^2/eps^3 + 2 (3 alpha/(2s))^2 g_N^3/eps^5 + O(g_N^4).
```

Substitution of the truncated series back into the constitutive law cancels
**identically through O(g_N^2)** (`resid_ser == 0`, exact); the leading neglected term is
`2 (3 alpha/(2s))^2 g_N^3/eps^5`, whose relative size is `(3 alpha/eps) Y` at
`Y << 2 eps/(3 alpha)`. The linear regime `g ~ g_N/eps` is exact at the origin
(relative residual `|eps g/g_N - 1| = 1.0e-12` at `g_N = eps^2 a0 · 1e-12`, C5b(i)).
The linear/deep crossover sits at `Y* = 2 eps/(3 alpha)`, `g_cross = 2 eps s/(3 alpha)
= lambda·a0` for `eps = lambda`; for `lambda >= 1` the crossover lies at or above the
model-validity edge `Y ~ 1/2` — the linear plateau spans the whole valid low-field
window and the deep window is **closed by `eps > 0`** (deep-law relative error at
`g_N = a0`: 0.3904 / 0.618 / 0.8284 for lambda = 1/2, 1, 2; C5b(ii)).

**Deep limit, `eps = 0`.** The quadratic degenerates to the **exact identity**
`s g mu = g_N` with `mu = (3 alpha/2)(g/s)`, i.e.

```
g^2 = (2s/(3 alpha)) g_N = a_deep g_N,     a_deep = 2s/(3 alpha).
```

This is an algebraic identity for every radius (C3b), not an asymptotic limit — the
`X^(3/2)` coefficient alone sets the `a0`-line; `C0` and `eps` are absent.
Model-scale match: `kappa_model = a_deep/s = 2/(3 alpha)`; adopting the framework
`kappa = 1/2` pins **`alpha = 4/3`** — and pins only the deep coefficient, not `eps`,
not `C0` (C3c; the adopted one-half is an input, see §5).

**Footings (both, kept separate per the framework base).**
Canonical `a0 = 9.3619e-11 m/s²`, kappa = 1/2: `s = 2a0 = 1.872380e-10 m/s²`,
`rho_L = 4 a0²/(G c²) = 5.84441245e-27 kg/m³` (cross-checked to 1e-33 against the
committed AS002 density), `eps_vac(C0=1) = s²/(8πG) = 2.089981e-11 J/m³`.
Alternative `a0 = 1.1279e-10 m/s²`, kappa = 1/2: `s = 2.255800e-10 m/s²`,
`rho_L = 8.48308961e-27 kg/m³`, `eps_vac(C0=1) = 3.033581e-11 J/m³`.
The two footings **cannot** share fixed `rho_Lambda` and fixed kappa: at the canonical
fixed density the alternative footing requires `kappa_eff = a0_alt/s_can = 112790/187238
= 0.602376… != 1/2` (exact rational comparison, tol 1e-12; C6b). The C0/eps/alpha
independence theorem is dimensionless and therefore applies to **both** footings
separately (C6c).

---

## 4. Independent checks in different representations (seed step 4)

All residuals are **actual measured numbers** (never booleans), tolerances set before
evaluation.

1. **Symbolic substitution (sympy).** The truncated series substituted back into the
   constitutive law cancels through O(g_N²) identically (`resid_ser == 0`, C3a);
   `mu(Y) - (eps + (3 alpha/2) sqrt(g²/s²)) == 0` exactly (C1a).
2. **60-digit closed-form residual (mpmath).** Exact quadratic root reassembled in
   `r² g mu(g/s) = GM`: `max |r² g mu - GM|/(GM)` over 10 log-spaced radii per lambda,
   `r in [1e-3, 1e6] pc`, C0 = 0, alpha = 4/3, eps = lambda:
   `8.346e-28` (lambda = 1/2), `2.049e-27` (1.0), `2.786e-27` (2.0); tol 1e-20 (C5a).
   Deep-law continuity at `eps = 1e-25`: residual `1.0e-25` (C5b(iii)).
3. **Float64 cross-representation (numpy).** Same identity at double precision:
   `1.78e-13 / 4.54e-14 / 1.01e-12` for lambda = 0.5/1.0/2.0; tol 1e-9 = float64 noise
   floor (exactness is established symbolically and at 60 digits) (C8b).
4. **Finite differences.** `dK/dX` at `X = Y²` by central differences vs
   `eps + (3 alpha/2) sqrt(X)` over `X in [1e-8, 1]`: max relative residual `7.62e-11`
   ~ O(h²); tol 1e-6 (C8a).
5. **Lean 4 certificate** (`AS061_vacuum_energy_susceptibility.lean`, compiled with
   `lake env lean`, EXIT 0). Formalises: flux identity `eps + (3α/2)√(Y²) = eps +
   (3α/2)Y` for `Y >= 0`; `flux(0) = eps`; `K(0) = C0`; C0-independence of the flux;
   the mandated control `K(0)=0 ∧ mu(0)=1 ∧ 1≠0` (C0=0, eps=1) and its reverse
   (`K(0)=1 ≠ 0` with `mu(0)=0` for eps=0, C0=1); the calculus step
   `K'(X) = eps + (3α/2)√X` at `X > 0` **and** at `X = 0` (including the normed-form
   limit argument for `x·√x` at 0); the bridge at `X = Y²`; the deep-line equivalence
   `g·((3α/2)(g/s)) = g_N ↔ (2s/3α)·g_N = g²`; and the kappa = 1/2 pinning
   `2s/(3α) = s/2 ↔ α = 4/3`. Axioms for every statement: exactly
   `{propext, Classical.choice, Quot.sound}` — zero `sorry` (axioms_out.txt).
6. **Branch distinctness (criterion B / framework).** The operative and historical
   branches Q (`g² = B² + a0 B`), RAR (`nu = 1/(1 - e^{-sqrt(B/a0)})`), MU2
   (`mu = 1 - (1 + g/(2a0))^{-2}`), historical EXP AQUAL (`mu = 1 - e^{-g/a0}`) and
   filtered MONO (`y/(y + h_RAR)` on the RAR segment) are evaluated at the deep end:
   all five satisfy `mu(0) = 0` — max `mu(y)` over `y in [1e-12, 1e-8]` is
   `1.00e-4 / 1.00e-4 / 2.24e-5 / 3.16e-5 / 1.00e-4` (Q/RAR/MU2/EXP/MONO; implicit
   solves via scipy.optimize.brentq for MU2 and EXP, tol 1e-3, C7a). The MU_n family
   `mu_n(Y) = 1 - (1+Y)^{-n}` has `mu_n(0) = 0` and deep-MOND slope exactly `n` for
   every `n >= 1` (C7b): a shared degenerate boundary condition, not a shared finite
   law — and none of the five branches derives the degeneracy from the vacuum energy.

---

## 5. Negative controls, strongest surviving statement, next implication (seed step 5)

**Mandated control (capable of failing):** `C0 = 0, eps = 1` gives `K(0) = 0`
(vacuum primitive vanishes, `rho_vac = 0`) **while** `mu(0) = K'(0) = 1 != 0` (linear
Newtonian response nonzero). The control *would fail* if zero vacuum energy forced zero
susceptibility; it does not (C4a; Lean theorem `control_zero_vac_nonzero_lin`).

**Reverse control:** `eps = 0, C0 = 1` gives `mu(0) = 0` (degenerate susceptibility)
**while** `rho_vac = C0 s²/(8πG) = 2.089981e-11 J/m³ != 0` (nonvanishing vacuum energy,
canonical footing). Degeneracy is a property of the response, not of the vacuum
energy (C4b; Lean `control_reverse_nondegenerate_vac`).

**Strongest surviving statement.** In the PD08 static scalar-kinetic class with
`K(X) = C0 + eps X + alpha X^(3/2)` (`s = c sqrt(G rho_Lambda)`, kappa = 1/2 adopted):

> (S1) `div(mu grad Phi) = 4πG rho_b` with `mu(Y) = eps + (3α/2)Y` is invariant under
> `C0 -> C0 + Δ` for all Δ — vacuum energy is exactly a null direction (dimensionless,
> holds on both registered footings).
> (S2) `chi_ij(0) = eps·delta_ij` exactly; `eps = 0` is exactly the deep-MOND input
> (`g² = (2s/3α) g_N`).
> (S3) `C0 = 0` does not imply `mu(0) = 0` and `eps = 0` does not imply `C0 = 0`.
> (S4) Matching kappa = 1/2 pins `α = 4/3`; it does not pin `eps` or `C0`.

**First additional implication needed to transfer to the full theory.** The linear
susceptibility `eps` of the truncated Taylor model is not fixed by anything in this
calculation (S4). Transferring the closure claim to the operative filtered-MONO branch
of the amended thirteen-item target requires (i) the filter-S specification (the exact
zero-field limit of operative MONO is outside this lane — noted in C7a), (ii) an
independent mechanism fixing `eps` (a channel count or adopted normalisation is not a
derivation unless its physical identification is separately justified — framework
base), and (iii) an explicit bridge from the high-field linear regime of this class to
the spliced MONO shape. These are open dependencies, not passes.

## 6. Execution bounds (actually enforced)

- Wall time: declared `<= 120 s`; enforced via `signal.alarm(120)` — alarm firing
  raises `TimeoutError` (bounded prototype, single run: **0.40 s wall**).
- Memory: declared `<= 512 MB`; `RLIMIT_AS` is **refused by macOS**
  (`ValueError: current limit exceeds maximum limit`) — recorded as an environment
  limitation; measured peak RSS `111,984,640 bytes` (~106.8 MB) via
  `resource.getrusage`, far below the bound.
- Threads: declared 1; enforced by construction — no threading, no subprocesses,
  `OMP_NUM_THREADS=MKL_NUM_THREADS=OPENBLAS_NUM_THREADS=1`.
- Sampling: 10 log-spaced radii per lambda, `r in [1e-3, 1e6] pc`; branch grids
  `y in [1e-12, 1e-8]`; lambda in {1/2, 1, 2}; 60-digit mpmath for C5a/C6; float64 for C8b.

## 7. Files in this run directory

- `checks_AS061.py` — bounded prototype (all 22 checks, 23 PASS lines; sha256 `7f82f6cf…aa35`)
- `result_checks_raw.txt` — full raw output with measured residuals (sha256 `fcdae50f…a8ca`)
- `stderr_time.txt` — `/usr/bin/time -p` record (real 0.46 s; sha256 `fab27d95…5d02`)
- `AS061_vacuum_energy_susceptibility.lean` — Lean 4 certificate, compiles EXIT 0
  (sha256 `3c3593fc…f3bc`)
- `lean_compile.txt` — final clean compile log (sha256 `f109d7f6…9846`)
- `axioms_check.lean` / `axioms_out.txt` — axiom audit: every statement depends on
  exactly `{propext, Classical.choice, Quot.sound}`, zero sorry
- `derivation.md`, `result.json` — this derivation and the contract result
