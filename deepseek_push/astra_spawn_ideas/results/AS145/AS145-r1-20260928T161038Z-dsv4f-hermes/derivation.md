# AS145 — Derive the gate contribution to the lapse equation (CA5-GNC-R / CA4-GNC host)

**Run:** `AS145-r1-20260928T161038Z-dsv4f-hermes`
**Worker:** `deepseek/deepseek-v4-flash-0731` (provider openrouter), Hermes Agent focused subagent; identity from the executing agent's own system context.
**Branches:** conclusion branch only CA5-GNC-R with inherited CA4-GNC host. Q, RAR, MU2, EXP are untouched comparison branches. The operative filtered MONO branch enters through the gate argument `J` (`q'(y^2) = nu_mono(y) - 1`, FRAMEWORK_CONTRACT MONO definition) and is used with its actual derivative-floor splice (landmarks reproduced below). Criterion B is untouched: this derivation is a static same-action first-variation identity, not a propagation statement.
**Outcome classification:** **derived** (scoped candidate result for the frozen unweighted gate construction; not gravity closure).

---

## 1. Pinned action and conventions (task step 1)

Sources verified at execution (hashes match the pins in the task, `SOURCE_MANIFEST.json`, and `input_hashes.txt`):

| Source | SHA-256 |
|---|---|
| `real_research/common_action_2026_09_26/action/FINAL_ACTION.md` (CA4-GNC host) | `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e` |
| `real_research/common_action_2026_09_26/assembly/REPORT.md` | `5009af86e7b8c72aaafa3aa17314c75e4e8f8e97edc6e24aa1757961212c011c` |
| Task file `AS145_derive_the_gate_contribution_to_the_lapse_equation.md` | `f8e05f134ef6a6b052166559e18f9e40acb456c73efb3e96df7ca0b83dca4503` |

Conventions (FINAL_ACTION §1–§2): `c=1`, signature `-+++`, `M_P^2 = (8 pi G_bare)^(-1)`; foliation `n_mu = -tau_mu/sqrt X_tau`, `N = X_tau^(-1/2)`, `h = g + n (x) n`, `a_mu = D_mu ln N`; leaves compact, connected, closed, spacelike; mean `<A>_h = (int sqrt h A)/(int sqrt h)` — **not lapse-weighted**; `W_b = S_h U` with `S_h = e^(b Delta_h)`, `b = xi^2/2`, `U` an independent heat-field endpoint datum; no spatial boundary terms. `Delta_h W = div_h D W`; `Delta_N W := N^(-1) D_i(N D^i W)` (FINAL_ACTION §3). `G_N = G_bare/c_N` (derived in §5 of the action); `G_N`, `G_bare`, `G_cosmo` kept separate (relations from the action: `G_N = G_bare/c_N`, `G_cosmo = c_N G_N = G_bare`; eq. (18) — recorded, not conflated).

Gate sector of the action (FINAL_ACTION eq. (4); the only term varied here):

```
Y_h := J(DW_b) + ell * Delta_h W_b - theta        (FINAL_ACTION eq. (3))
S_gate := C_N * int N sqrt(h) [ G(Y_h) + ell a . DW_b ]
with  J(p) = 2 a0^2 q(|p|^2/a0^2),  q'(y^2) = nu_mono(y) - 1,
      G = C4 ramp:  0 (Y <= 0),  delta(7r^5 - 14r^6 + 10r^7 - 2.5 r^8), r = Y/delta (0<Y<delta),  Y - delta/2 (Y >= delta),
      0 < alpha < 2,  c_N = 1 - alpha/2,  0 < ell < 4,  theta > 0,  delta > 0.   (1)
```

**Target (task math):** `delta_lnN S_gate = C_N * int N sqrt(h) dlnN * [G(Y_h) - ell Delta_h W_b]` — the exact gate lapse source entering the lapse equation (FINAL_ACTION eq. (13), `+ c_N[G(Y_h) - ell Delta_h W_b]`), with `Y = J(DW_b) + ell Delta_h W_b - theta` — reproduced as eq. (12) of the pinned action.

Variation data (independent fields fixed): `delta ln N = phi` arbitrary smooth on the leaf, `delta h = 0`, `delta U = 0` (so `delta W_b = 0`, `delta(DW_b) = 0`, `delta(Delta_h W_b) = 0`), `delta N^i = 0`, clock/matter/carrier fields and Z fixed. All variations BEFORE any field elimination.

## 2. First variation: measure and acceleration (task step 2)

1. **Y_h is lapse-independent at fixed (h, U):** `W_b = e^(b Delta_h) U` contains no `N` at fixed `h`; `J(DW_b)`, `Delta_h W_b`, `theta` likewise. Hence, pointwise,
   ```
   delta_lnN Y_h = 0,   delta_lnN G(Y_h) = G'(Y_h) * 0 = 0,   delta_lnN G'(Y_h) = 0.   (2)
   ```
2. **Measure:** `delta_lnN (N sqrt(h)) = N sqrt(h)` (`h` fixed).
3. **Acceleration:** `a = D ln N` gives `delta_lnN a = D (delta ln N)` (at fixed `h`; the leaf connection `D` is independent of `N`), and `delta_lnN (DW_b) = 0`.
4. **First variation, BEFORE any integration by parts:**
   ```
   delta S_gate = C_N integral N sqrt(h) phi [ G(Y_h) + ell a . DW_b ]          (measure)
                + C_N ell integral N sqrt(h) (D phi) . DW_b                    (compensator argument)
   ```
   (the gate argument contributes nothing, because of (2): *no G' term inside the density, no G'' term at all* — see also §5).

## 3. Reduction on a closed leaf (task step 3)

With the `N sqrt(h)` measure, `div_N v = N^(-1) D_i (N v^i)`, integration by parts on the closed leaf (no boundary terms):

```
integral N sqrt(h) (D phi) . DW_b  =  - integral N sqrt(h) phi * Delta_N W_b.      (3)
```

The pivotal algebraic identity (pointwise, exact; product rule):

```
Delta_N W_b = N^(-1) D_i (N D^i W_b) = Delta_h W_b + (D_i ln N) D^i W_b = Delta_h W_b + a . DW_b.   (4)
```

Substituting (3)–(4) into §2.4:

```
delta S_gate = C_N integral N sqrt(h) phi * [ G(Y_h) + ell a . DW_b - ell Delta_N W_b ]
             = C_N integral N sqrt(h) phi * [ G(Y_h) - ell Delta_h W_b ].                          (5)
```

(5) is exactly eq. (12) of FINAL_ACTION, hence the **exact gate lapse source in eq. (13) is `+ c_N [G(Y_h) - ell Delta_h W_b]`** — the task's displayed object, **derived**.

**Why no G'' term occurs in this particular first variation:** a would-be `G''` contribution of the CA4-PN type would have to come from `delta G'(Y)` or `delta G(Y)` through a lapse-dependent argument: `dG = G' dY`, `dG' = G'' dY`; both vanish by (2), because `Y_h` is built from the **unweighted** Laplacian `Delta_h` and the frozen heat field, so `delta_lnN Y_h = 0` at fixed (h, U). The compensator sits *outside* `G` (FINAL_ACTION §2: fixed compensator, not multiplied by f), so its variation produces only the `-ell Delta_h W_b` term after (3)–(4). Contrast: with `Delta_N` inside `Y` (negative control, §4), `delta Y != 0` and the chain rule fires an explicit `G'' D Y_N . D W_b` term. This is the structural difference vs the weighted CA4-PN gate (`(c_N/2) G'' ell^2 |DW|^2` lapse-gradient term recorded as absent in FINAL_ACTION §6).

## 4. Controls (task step 4) — all capable of failing; residuals below

Numerical prototype (bounded): flat 2-torus leaf `[0,2 pi)^2` (compact, closed, no boundary), `NX = 64` probe and `NX = 96` refined grid (the required single refinement), 4th-order periodic stencils, rectangle-rule leaf integral, `alpha = 1` (`c_N = 0.5`), `ell = 0.4`, `theta = 5.5`, `delta = 0.05`, `a0 = 1`, smooth positive lapse `N = exp(0.35 cos x + 0.25 sin 2y)`, smooth nonconstant `W_b = 2.2 cos x cos y + 1.35 sin 2x sin 3y` (integer wavenumbers — non-integer wavenumbers break torus periodicity at the seam), test variation `phi = cos(2x - y) + 0.6 sin 3y + 0.4 cos(x + 2y)`, `eps = 1e-5` and `5e-6`. Finite differences recompute the action at `N e^(± eps phi)` with the compensator rebuilt from the perturbed lapse (`a(N~) = D ln N + eps D phi`) and the hot data frozen — exactly the varied action of §2.

| # | Control (capable of failing) | Method | Result |
|---|---|---|---|
| A | **Main finite difference of (5)** | `FD = [A(N e^(eps phi)) - A(N e^(-eps phi))]/(2 eps)` vs the analytic expression — in the identity-free form `C_N int N phi [G + ell a.DW - ell Delta_N W]` (the first-IPP form, exact on the grid) | **rel residual 8.9e-11** (NX=96, eps=1e-5); 2.4e-10 at eps=5e-6 — passes at 1e-8 tolerance |
| B | **(5) itself, i.e. the identity-reduced form** `C_N int N phi [G - ell Delta_h W]` | same FD; residual is the discrete defect of identity (4) | rel residual **9.7e-6** (NX=96), 4.9e-5 (NX=64): ratio 5.03 = (3/2)^4 — pure O(h^4) discretization, converged; identity (4) verified discretely at rel 4.8e-5 (96^2) |
| C | **Y_h lapse-independence, (2)** | recompute Y_h at perturbed lapse | max abs diff exactly 0.0 (by construction); the *phantom* G''-term integral `ell int N phi G''(Y_h) D Y_h . D W_b` (which (5) lacks) has magnitude 11.70 (96^2; 11.79 at 64^2; max |G''(Y_h)| = 43.7) — nonzero field content that the structural argument removes, FD confirms its absence |
| D | **Limiting case ell -> 0** | compensator off: `delta S_gate = C_N int N phi G(Y_h)` | rel residual 2.65e-11 |
| E | **Limiting case: inactive branch (Y <= -delta everywhere)** | theta shifted up; `G = 0`, source `= -C_N ell int N phi Delta_h W_b` | rel residual 1.98e-5 (O(h^4) level), sign correct |
| F | **Limiting case: active branch (Y >= delta everywhere)** | theta shifted down; the ell-split cancels exactly: source `= C_N int N phi [J(DW_b) - theta - delta/2]` | rel residual 5.6e-6 (O(h^4) level), sign correct |
| G | **Negative control (task-mandated): replace Delta_h by Delta_N INSIDE Y** | alternate action `S'_gate` with `Y_N = J + ell Delta_N W - theta`; finite difference vs four candidates | FD_N matches the derived swapped expression (`C_N int N phi [G(Y_N) + ell a.DW - ell divN((1+G')DW)]`) at **4.97e-9** (eps=1e-5; 1.60e-9 at eps=5e-6); the naive candidates `G(Y_N) - ell Delta_h W` and `G(Y_h) - ell Delta_h W` are rejected at **0.61 and 0.45 relative** (O(1)) — the control actively fails the naive forms; the newly generated lapse-derivative terms are quantified: explicit `G''`-proportional term `-ell int N phi G''(Y_N) D Y_N . D W_b` = 2.9x the FD scale, plus a divergence of the lapse-dependent flux `divN((1+G'(Y_N))DW)`, plus the shifted argument `G(Y_N) != G(Y_h)` inside the transition where `G' != const`. |
| H | **Dimension/sign bookkeeping** | [Y]=[G]=[theta]=[delta] = L^-2, [ell]=1, [W_b]=1, [a]=L^-1, [Delta_h]=L^-2 in c=1 units; every term of (5) is L^-2, consistent with the lapse-density layer of eq. (13) (rho/M_P^2 ~ L^-2). Signs: measure +1, gate +G, compensator -ell Delta_h W_b; directly confirmed by FD at all limiting cases. Averaging measure: `<A>_h` sqrt(h)-only — no lapse weight in the mean, and no mean projector in the gate sector. |
| I | **Substitution back / finite-domain refinement** | FD at eps and eps/2 agree at 1e-8-level against the same analytic value (eps-converged, residual flat in eps, dominated by the h^4 identity defect); grid refinement 64 -> 96 changes the (5)-form residual by exactly the h^4 factor | passed; tested domain: torus 96^2 = 9,216 sites, Y spanning all three regimes (inactive 4,072; transition 0<Y<delta: 52; active 5,092), eps in {1e-5, 5e-6}, parameters as listed |

Bound enforcement (actually enforced, not merely suggested): wall time `<= 120 s` enforced via `SIGALRM` (kill at 122 s); measured wall 0.10 s; single thread enforced via `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`, `NUMEXPR_NUM_THREADS=1` and no FFT/BLAS calls; memory: peak RSS measured 64.2 MB (`resource.getrusage`), grid sized so the 512 MB bound is exceeded by >7x margin — no hard RLIMIT_AS applied (unsafe with numpy on macOS; the 512 MB bound is a 7.8x headroom margin, stated as such).

## 5. Algebraic certificate (Lean 4, house build `fable_independent_2026/lean_2026`)

`AS145_gate_lapse.lean` — five theorems, zero `sorry`, unfiltered `#print axioms` = exactly `{propext, Classical.choice, Quot.sound}` for all five:

| Theorem | Content (1D flat prototype of the pointwise identity) |
|---|---|
| `divergence_reduction` | `(1/N)(N f')' = f'' + (N'/N) f'` — the pivotal identity (4) |
| `lapse_acceleration` | `HasDerivAt (log ∘ N) ((N z)^(-1) * N'(z)) z` — `a = D ln N` is the log derivative |
| `lapse_divergence_reduction` | `(1/N)(N W')' - (N'/N) W' = W''` — the subtraction used to reach (5) |
| `no_Gpp_term` | `Y` derivative-free (lapse-independent argument): `d/dx[G'(Y(x)) W'(x)] = G'(Y z) W''(z)` — NO G'' term |
| `Gpp_split` | `Y` with derivative `y'`: `d/dx[G'(Y(x)) W'(x)] = g'' y' W'(z) + G'(Y z) W''(z)` — the G'' term appears exactly when the gate argument is lapse-dependent (negative control) |

Semantic mapping (documented in the file header): prototype fields `(N, W, Y, G)` stand for (lapse, heat field, gate argument, C4 ramp); the prototype coordinate is a point on the flat leaf; "lapse-independence of Y" is modeled as vanishing derivative — the certificate is the *algebraic core* (product rule + chain rule) of §2–§3 and of the negative control, not a manifold theorem.

Compile: `cd fable_independent_2026/lean_2026 && lake env lean <abs run dir>/AS145_gate_lapse.lean` — exit 0; axioms output in `lean_compile_out.txt` / `lean_axioms_out.txt`. (Compile host only; no files written into `fable_independent_2026/lean_2026`.)

## 6. Footing application (contract: both footings)

The identity (5) contains **no `a0` coefficient**: `a0` enters only inside `J` through the dimensionless `nu_mono` argument `y = |DW_b|/a0`; any smooth `J` (hence either footing, and any branch) satisfies (5) with identical coefficients. Dimensionless result; applicability to both footings stated:

| Footing | a0 [m/s^2] | rho_Lambda = 4 a0^2/(G c^2) [kg/m^3] | Alternative reading |
|---|---|---|---|
| canonical | 9.3619e-11 | 5.8444e-27 | kappa = 1/2 adopted (input) |
| alternative | 1.1279e-10 | 8.4831e-27 (= 1.4515 x rho_can) | at fixed rho_Lambda (canonical density held), kappa_eff = 2 a0_alt/(c sqrt(G rho_can)) = **1.2048** (not 1/2); at fixed kappa = 1/2 the density must change by (a0_alt/a0_can)^2 = 1.4515 |

Round trip check: `(c/2) sqrt(G rho_Lambda_can) = 9.3619e-11 m/s^2` reproduces the canonical footing to all printed digits.

## 7. Scope, upstream state, limitations, next implication

**Upstream / siblings:** `results/AS127` (reciprocal lapse density, completed) — the carrier-sector lapse density `rho_R` that sits with the gate source in eq. (13); `results/AS131` (heat-field metric stress) and `results/AS151` (primary constraints) were in flight (run dirs present, no `result.json` at read time) — not read as dependencies, not modified; the gate term here is independent of those files. This result does not re-derive AS127, AS131 or AS151.

**What this result establishes (scoped):** for the frozen unweighted compensated gate construction (FINAL_ACTION eq. (4), `c_N[G(Y_h) + ell a.DW_b]`), varied at fixed (h, U, shift, matter, clock, Z), on compact closed spacelike leaves, the exact gate lapse source is `+ c_N [G(Y_h) - ell Delta_h W_b]` across the full C4 transition and both extreme branches, with no G'' term; the negative control (Delta_N inside Y) generates the identified lapse-derivative terms and fails the naive forms at O(1).

**What it does NOT establish:** it is not gravity closure (FINAL_ACTION §8 remains: full constraint count, global mixed Cauchy problem, PPN, general no-slip, GW sector are open). It does not derive kappa = 1/2 (adopted input). It does not cover lapse variations with `delta U != 0` (heat-field response) or metric variations (fixed-h premise). The h^4 discretization defect of (4) in control B is a scheme artifact, not a physics residual; the analytic identity (4) is exact and Lean-certified.

**next_unresolved_implication:** the first missing mathematical bridge: the *combined* lapse equation (13) solvability on a compact leaf — with the derived gate source `c_N[G - ell Delta_h W_b]` plus the projected carrier source `rho_d - <N rho_d>_h/N` (AS127) inside the nonlinear lapse problem `delta S_GNC/delta ln N = 0` — i.e., existence of a smooth positive lapse N for the frozen unweighted construction with the full C4 transition (the weighted-gate variant's failure mode, REPORT.md §3, is explicitly NOT inherited, but the unweighted compact-leaf lapse solvability is unproved).

**suggested_followup / child:** `AS145.C01` — lapse variation WITH the heat-field response (`delta U != 0`, i.e. `W_b = e^(b Delta_h) U` no longer frozen): derive the modified gate source containing the `G'(Y_h) [J_p D(delta W_b) + ell Delta_h(delta W_b)]` channel and the `S_h^*`-mediated U-response, with the R_W adjoint structure of eq. (5); exact setup in `branches/AS145/AS145.C01.md`. Not dispatched (no runner available); per FIRST_PRINCIPLES_AND_BRANCHING this is a ready child specification for the orchestrator.