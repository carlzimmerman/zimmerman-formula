# AS056 r01 — Static Einstein channel count versus propagating DOF — derivation

**Run:** `AS056_r01_20260928` · **Seed:** `AS056_static_einstein_channel_count_versus_propagating_dof.md`
(sha256 `22b5ecb9afec2a00e3a7146f3af472debb221c8066e836877c341f48ac30c059`, verified at start)
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter), Hermes Agent subagent, single-run worker seed
**Executed:** 2026-09-28T08:11:32Z – 2026-09-28T08:33:14Z UTC

---

## 1. The precise claim under test, symbol dictionary, boundary data, assumptions

**Claim examined (seed "Mathematics and principal test"):**

> In 3D, `G^(1)_00 = 2*Delta(Psi)`, `sum_i G^(1)_ii = 2*Delta(Phi-Psi)`.

This is PD01's B1 "two static Poisson channels" statement, the load-bearing *channel-count*
step of the PD01→PD08 chain that ends at `kappa = 1/2`. AS056's assignment: re-derive the
operators in the stated convention, decide what the static rank does and does not certify,
and run the required controls (including the seed's own stochastic-mode control).

**Symbol dictionary and conventions (all scale factors, signs and units explicit):**

| symbol | meaning | value/unit |
|---|---|---|
| `eta = diag(-1,1,1,1)` | flat (Minkowski) background, mostly-plus | — |
| `g = eta + h` | linearized metric | — |
| `h_00 = -2 Phi`, `h_ij = -2 Psi delta_ij`, `h_0i = 0` | two-potential static ansatz (PD01 convention) | Phi, Psi dimensionless (weak field) |
| `h = eta^{mu nu} h_mu nu = 2 Phi - 6 Psi` | trace of the perturbation | — |
| `Delta` | flat Laplacian `d_x^2 + d_y^2 + d_z^2`, static sector (`d_t = 0`) | 1/m² |
| `deltaGamma^l_mn` | linearized Christoffel symbol, `(1/2) eta^{l s}(d_m h_sn + d_n h_sm - d_s h_mn)` | — |
| `R^(1)_mn = d_l deltaGamma^l_mn - d_n deltaGamma^l_ml` | linearized Ricci (definitional) | 1/m² |
| `G^(1)_mn = R^(1)_mn - (1/2) eta_mn R^(1)`, `R^(1) = eta^{mn} R^(1)_mn` | linearized Einstein tensor (trace-reversed Ricci) | 1/m² |
| `rho, p` | dust density, isotropic pressure (stress `T_00 = rho`, `T_ii = p`) | kg/m³, N/m² |

**Boundary conditions:** asymptotically flat potentials (`Phi, Psi -> 0` at infinity),
compact support for the pressureless baryonic source, Dirichlet data in the numerical
exercises. **Assumptions:** (A1) static, weak-field, linearized regime; (A2) the diagonal
two-potential ansatz with `h_0i = 0` (gauge-fixed form); (A3) mostly-plus and the Ricci/
Einstein-tensor definitions above; (A4) pressureless dust baryons in the sourced sector.
**Framework inputs (adopted, not derived by this task):** `a0 = kappa c sqrt(G rho_Lambda)`
with `kappa = 1/2`, `rho_Lambda = 4 a0^2/(G c^2)`, `r_M = sqrt(G M_b / a0)`,
`v_flat^4 = G M_b a0`, `G = 6.67430e-11`, `c = 299792458`, `M_sun = 1.98847e30`, `pc = 3.085677581491367e16` (all SI).
`G_N`, `G_bare`, `G_cosmo` kept as separate symbols; in the *linearized static sector of this
task* the Newtonian channel exercises `G_N = G_bare` (same symbol, stated, not globally matched).

**Branches:** the task's declared branch is **CORE coefficient; conditional MU_n statistical
response**. The OR-class algebra is shared with the MU2 family (`mu_n(Y) = 1-(1+Y)^(-n)`,
`Y = g/(2 a0)` at n=2, framework row MU2) — we use it only as the *algebra* under test; no
Q/RAR/EXP/MONO law is transferred, fitted or used as a conclusion. Task conclusion: the counts
and premises examined, `kappa = 1/2` remains ADOPTED input.

## 2. Re-derivation of the operators (all factors, signs, units)

### 2.1 Linearized Ricci, definitional construction

With `deltaGamma` from the Christoffel formula (linear order only: `g^(mn) = eta^(mn) + O(h)`),
the static linearized Ricci for the two-potential ansatz is (verified in sympy, generic
**non-radial** `Phi(x,y,z)`, `Psi(x,y,z)`, and cross-checked against PD01's explicit
per-component formulas):

```
R^(1)_00 = Delta Phi
R^(1)_ii = Delta Psi + d_i^2 Psi - d_i^2 Phi                 (no sum over i)
sum_i R^(1)_ii = 4 Delta Psi - Delta Phi
R^(1)_0i = 0,   R^(1)_ij = -d_i d_j (Phi - Psi)  (i != j)
```

### 2.2 Trace reversal and the seed's equations

```
R^(1) = -R^(1)_00 + sum_i R^(1)_ii = 4 Delta Psi - 2 Delta Phi
G^(1)_00 = R^(1)_00 - (1/2) eta_00 R^(1) = Delta Phi + (1/2)(4 Delta Psi - 2 Delta Phi)
         = 2 Delta Psi                                                    [seed eq 1  PASS]
sum_i G^(1)_ii = sum_i R^(1)_ii - (1/2) 3 R^(1)
         = 4 Delta Psi - Delta Phi - 6 Delta Psi + 3 Delta Phi = 2 Delta(Phi - Psi)
                                                                         [seed eq 2  PASS]
```

Exact identity-level results (sympy residuals identically 0, generic potentials; matching
finite-difference residuals 1.28e-16 / 2.13e-16 on non-radial anisotropic Gaussians, NC-E;
the 2h-stencil FD Laplacian agrees to 1e-16 because both potentials are smooth and the
identity is algebraic). The seed's principal equations are **confirmed** under these
conventions: factors ±2 exact, difference `Phi - Psi` exact, sign convention as defined.

### 2.3 What the static equations contain: dust collapse, pressure channel

Linearized field equations `G^(1)_mn = 8 pi G T_mn` (convention as defined) give for dust with
isotropic pressure:

```
first channel:   2 Delta Psi = 8 pi G rho        =>  Delta Psi = 4 pi G rho      (Newton limit, G_N = G)
second channel:  2 Delta(Phi-Psi) = 8 pi G (3 p) =>  Delta(Phi-Psi) = 12 pi G p  (pressure-only)
off-diagonal:    G^(1)_ij = -d_i d_j (Phi-Psi) = 0
```

For **pressureless dust the second channel is homogeneous**; with `Phi - Psi -> 0` at infinity
the maximum principle/Liouville gives `Phi = Psi` exactly — the PPN `gamma = 1` degeneracy.
So the *operator* rank of the static linearized system is **2** (two independent rescaled
Laplacians on the functions `Psi` and `Phi - Psi`), while the *dust response* carries exactly
**one** function (the collapse `Phi = Psi`). This distinction is the crux of what the static
rank certifies (see §6).

Independent second representation (harmonic/relaxed gauge): with
`hbar = h - (1/2) eta h`, the static vacuum conditions
`Delta hbar_00 = 0 = Delta hbar_ii |i` read `Delta(Phi + 3 Psi) = 0`, `Delta(Phi - Psi) = 0`;
the change of unknowns `(Psi, Phi-Psi) -> (Phi+3Psi, Phi-Psi)` has determinant 4 — same rank-2
family (checks P1g, P1h).

### 2.4 The OR-class slope algebra (count → kappa chain) and its exact domain

`mu(Y) = 1 - (1 - p(Y))^2` with any completion `p`, `p(0)=0`, `p'(0)=1`:

```
mu'(0) = 2 p'(0) (1-p(0)) = 2        -- completion-independent (generic c2, c3: 0 residual, P2a)
Sum-class 2 p(Y) saturates at 2, not at 1  ->  excluded by the L230 normalisation mu(inf) = 1 (P2b)
deep-MOND Poisson with mu ~ n g/s  =>  a0 = s/n, kappa = 1/n;  n = 2  =>  kappa = 1/2 (P2c)
```

The n-channel identity `(1-(1-p)^n)'(0) = n` for every completion and every `n >= 1` is
**Lean 4-certified** (`AS056_channel_count.lean`, `or_slope`), along with the trace-reversal
combination (`trace_reversal`) and the tail `a0 = s/2 => kappa = 1/2` (`kappa_half`). Axioms:
`{propext, Classical.choice, Quot.sound}` — no `sorry`.

**Domain of the count result:** the origin-slope statement is exact for the whole OR class;
the *finite* response is not determined by the count — diagnostic counterexamples at
`lambda = 1/2, 1, 2` spread by 0.155/0.193/0.110 across four completions (P2d, NC-B). An
observational preference at finite acceleration is **not** a proof of the count.

## 3. Constraints needed before counting propagating modes

A propagating-mode count requires, at minimum: (i) the dynamical (time-dependent) linearized
equations of the same action; (ii) a gauge choice (harmonic/TT) and the residual-gauge
freedom; (iii) the constraint algebra on initial data (Hamiltonian + momentum constraints).
The static elliptic rank does not supply any of these. Concretely (NC-F):

- **Massless scalar:** static rank 1 (`Delta phi`); propagating rank 1 (no gauge freedom).
- **Massless vector:** static rank 1 (`Delta A_0`); propagating rank 2
  (lightlike plane wave: harmonic gauge `k^m a_m = 0` and residual gauge `a ~ a + lambda k`,
  computed rank of the quotient = 2). *Same static rank, different propagating rank* —
  the static rank alone certifies nothing about propagation.
- **Metric (GR):** static operator rank 2; propagating physical content = 2
  (TT-gauge nullity computed = 2; Hamiltonian count `10 - 4 constraints - 4 gauge = 2`,
  standard theorem, cited). The equality of the two numbers for GR is a fact about the
  Hamiltonian constraint algebra of the *full linearized dynamics*, not a consequence of the
  two static Poisson equations.

## 4. Framework footings (canonical and alternative, separately)

```
canonical   a0 = 9.3619e-11 m/s^2 : rho_Lambda = 5.8444e-27 kg/m^3 (kappa = 1/2, adopted),
            s = c sqrt(G rho_Lambda) = 1.87238e-10 m/s^2 = 2 a0,
            r_M(M_sun) = 1.1906e15 m = 3.859e-2 pc,  v_flat = 333.9 m/s
alternative a0 = 1.1279e-10 m/s^2 : at FIXED rho_Lambda: kappa_eff = 0.6024  (changed kappa)
            at FIXED kappa = 1/2 : changed density rho_Lambda' = 8.4831e-27 kg/m^3
            r_M(M_sun) = 1.0847e15 m = 3.515e-2 pc,  v_flat = 349.8 m/s
```

The two footings cannot share both fixed vacuum density and fixed kappa (framework contract) —
quantified above. The two-channel theorem is dimensionless algebra: it applies identically to
both footings (it contains no `a0`), and the slope-count-landing `kappa = 1/2` is the adopted
canonical normalization; the alternative footing is a separate hypothesis of the framework,
not an output of this task.

## 5. Independent checks (actual residuals, not booleans)

| # | check | measured | tolerance set first | result |
|---|---|---|---|---|
| P1a | definitional Ricci = explicit per-component forms | max residual 0 (exact) | 0 | PASS |
| P1b | `G00 = 2 Delta Psi` | symbolic residual 0 | 0 | PASS |
| P1c | `sum Gii = 2 Delta(Phi-Psi)` | symbolic residual 0 | 0 | PASS |
| P1d,e | `G_0i = 0`; `G_ij = -d_i d_j(Phi-Psi)` | residuals 0 | 0 | PASS |
| P1g,h | harmonic-gauge representation; det(map) = 4 | residuals 0 | 0 | PASS |
| P2a | OR origin slope = 2, generic completion | `mu'_2(0) = 2` | 2 | PASS |
| P2b,c | SUM excluded; `kappa = 1/n`, n=2 → 1/2 | limit = n; a0 = s/n | — | PASS |
| P2d | finite-λ diagnostics spread | 0.1551/0.1932/0.1098 | > 0.10 each | PASS |
| NC-A | stochastic independence control | corr = 1.000 (res 1.65e-2); corr = −0.434 (res 1.96e-2) | corr > 0.999 / < 0.5, res < 2e-2 | PASS (fires: count ⇒ independence unsupported) |
| NC-B | finite-λ float spread | 0.1551/0.1932/0.1098 | > 0.10 | PASS |
| NC-C | Newtonian limit `Delta Psi = 4 pi G rho` | L2 rel residual 2.04e-3 (h = 0.025) | < 5e-3 | PASS |
| NC-D | collapse: boundary-data Laplace solve | dev 2.2e-16 (Jacobi fixed point, exact for harmonic polynomials) | < 1e-3 | PASS |
| NC-E | two channels, non-radial FD | 1.28e-16 / 2.13e-16 | < 5e-2 | PASS |
| NC-F1 | scalar 1/1 vs vector 1/2 propagating | quotient rank = 2 | = 2 | PASS |
| NC-F2 | metric TT nullity | 2 | = 2 | PASS |

**21/21 PASS.** Every check states measurement and threshold separately; the negative control
NC-A is *capable of failing* and — in its role — fires: the unsupported inference is marked,
not disguised.

## 6. What the static rank does and does not certify

**Certifies** (proved here, two symbolic representations + FD + Lean algebra core):
1. the static linearized response of the two-potential metric sector is carried by exactly
   two independent rescaled Laplacian operators, `2Delta` on `Psi` and `2Delta` on `Phi - Psi`
   — exact factors, general non-radial potentials, no gauge freedom beyond the ansatz;
2. for pressureless dust the *dust response* collapses to one function (`Phi = Psi`, γ = 1),
   the second operator being sourced only by isotropic pressure;
3. within the OR identification (premise) the origin slope of the response is the channel
   count, so `kappa = 1/(count) = 1/2` **under the adopted framework normalization** —
   the count step itself is valid algebra.

**Does NOT certify** (explicitly, with counterexamples):
1. the **propagating** degree-of-freedom count (NC-F1: static rank 1 with propagating ranks
   1 and 2; the GR two+two is a dynamical constraint-algebra fact);
2. **stochastic independence** of two modes (NC-A: correlation 1.000 and −0.43 realized by
   the same two equations — independence is an extra stipulation, PD01's D1 premise);
3. the **finite response shape** (NC-B/P2d: completions differ at every finite λ);
4. the OR identification itself, the one-scale action, or the data-selection step — all are
   premises of the PD01/PD08 chain; `kappa = 1/2` is therefore **adopted**, not independently
   derived by this task. The seed's assignment ("a count is useful only with its physical
   identification separately justified") is answered: the two operators are identified
   physically as (energy/Newton constraint channel; PPN-γ/anisotropic-stress channel), and the
   response-level OR-composition reading is explicitly *not* certified by the equations.

## 7. Strongest surviving statement

> **Theorem (AS056, scoped).** In the static, weak-field, two-potential metric convention of
> PD01 (`h_00 = -2 Phi`, `h_ij = -2 Psi delta_ij`, `h_0i = 0`, mostly-plus, linearized Ricci
> and Einstein tensor as defined), the seed's equations hold **identically for generic
> non-radial potentials**: `G^(1)_00 = 2 Delta Psi` and `sum_i G^(1)_ii = 2 Delta(Phi - Psi)`;
> the operator pair is a diagonal pair of rescaled Laplacians (exact factor 2), the dust
> response collapses to the single function `Psi` with `Phi = Psi` (γ = 1), and the OR-class
> origin slope equals the channel count for every completion (Lean-certified, `or_slope`).
> The static rank **does not** certify the propagating DOF count, stochastic independence, or
> the finite response shape (counterexamples NC-A, NC-B, NC-F1 executed). Conditional on the
> OR identification and the one-scale action premises, the count step of the PD01/PD08
> kappa-chain is sound; `kappa = 1/2` remains an adopted framework input.

**Domain:** 3D Euclidean static sector, formal smooth potentials (symbolic), uniform grids
`h ∈ [0.025, 0.05]`, boxes `L ∈ [1.0, 2.0]`, `lambda ∈ {1/2, 1, 2}`, four completions, both
footings. Exact identity vs finite numerical check: the two-channel statements are exact
identities (residual 0 / 1e-16); NC-C is a numerical consistency check at FD accuracy.

## 8. Negative controls (capable of failing) — summary

- **NC-A (seed's stochastic control):** the same two Poisson equations realized with mode
  correlation 1.000 and with correlation −0.43: the inference "two static elliptic equations
  ⇒ two stochastic independent modes" is unsupported and marked; the OR independence is a
  premise. **Fires.**
- **NC-B:** "the count fixes the response" is falsified at every finite λ (spread ≥ 0.11). **Fires.**
- **NC-C/D:** limiting regimes and boundary cases pass with preset tolerances (Newtonian
  `4 pi G`, collapse to machine precision). **Do not fire.**
- **NC-F:** static rank ≠ propagating rank, by explicit scalar/vector counterexample. **Fires.**

## 9. Execution bounds (declared vs actually enforced)

- Declared: prototype wall ≤ 120 s; memory ≤ 512 MB; 1 thread.
- Enforced: GNU `timeout 120` around both runs (hard kill at 120 s); 1 thread by environment
  (`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1`, all
  used libraries single-threaded); memory: `ulimit -v 524288` **attempted and NOT enforceable
  on this macOS host** (EINVAL, recorded) — memory bounded by problem design (grids ≤ 81³,
  ≤ 4.2 MB per array; CG/Jacobi solves, O(nnz) memory) and **measured**: derive peak RSS
  60.2 MB, controls peak RSS 123.4 MB (both < 512 MB; macOS `/usr/bin/time -l` reports bytes).
- Actual wall times (script-measured): derive 0.39 s, controls 0.19 s (first controls
  attempt with sparse-LU solves: 18 s wall, **2.1 GB** peak > bound → solver refactored to
  CG/Jacobi; see failed_attempts).
- A first closed-form Ricci implementation produced a wrong residual (`13 ΔΨ − 4 ΔΦ`,
  index/η insertion bug) — replaced by the definitional δΓ→δR construction, cross-verified
  with PD01's explicit formulas to identity; see failed_attempts.

## 10. What this result does not establish (limitations)

- Not a derivation of `kappa = 1/2` from nothing: `kappa = 1/2` is the adopted framework
  input; the premises of the PD01/PD08 chain (OR identification, L230 one-scale normalisation,
  carrier taxonomy {metric, scalar, static vector}) are inherited premises, named, not proved.
- Not a propagating-DOF theorem for any action; the wave-sector analysis of the candidate
  action (including the MONO heat filter's linearization) is not performed here.
- Not a statement about non-linear, non-static, non-flat, or non-two-potential regimes;
  statements restricted to the ansatz and to static weak-field physics.
- No observational claim: no SPARC/BTFR data re-fitted; the committed zero-point readings are
  quoted in PD01 only, not re-derived here (and deliberately not used as a proof).
- The alternative footing's `kappa_eff = 0.6024` is bookkeeping, not a measurement.

## 11. Next unresolved implication and suggested follow-up

**First missing bridge:** the wave-sector degree-of-freedom count of the *same* linearized
candidate action — prove exactly two physical propagating metric polarizations survive in the
full linearized evolution system (weak-field about Minkowski, two-potential ansatz, pressureless
baryons, including the linearization of the operative MONO/heat-filter regulator `S` raised as
a gate in FRAMEWORK_CONTRACT §MONO), and verify no extra propagating mode enters through the
filter. Until that bridge is proved, the framework gate "exactly two gravitational propagating
degrees of freedom" is **not** closed by the static channel count; the equality
2 = 2 for GR rests on the dynamical constraint algebra (NC-F2), not on the static equations.

**Suggested follow-up (child specification written, not dispatched):**
`AS056.C01` — "wave-sector DOF count of the linearized candidate action"
(`branches/AS056/AS056.C01.md`): claim, fingerprint, controls, dependencies are recorded
there for orchestrator dispatch; no runner mechanism exists in this session, so no execution
is claimed.

## 12. File inventory of this run

```
derivation.md                 this file
result.json                   schema-v2 result (all fields)
as056_derive.py               symbolic re-derivation (14 checks, 14 PASS)
as056_controls.py             negative controls + independent numerics (7 checks, 7 PASS)
derive_raw.out, controls_raw.out   full raw outputs
derive_checks.json, controls_checks.json   machine-readable check records
AS056_channel_count.lean      Lean 4 certificate (or_slope, trace_reversal, kappa_half)
lean_raw.out                  `lake env lean` compile log + #print axioms
time_mem.txt                  measured peak RSS (controls)
```