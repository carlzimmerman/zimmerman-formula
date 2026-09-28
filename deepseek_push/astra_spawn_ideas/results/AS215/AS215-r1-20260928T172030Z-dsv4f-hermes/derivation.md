# AS215 — Construct a criterion-B characteristic ordering test (Tier-0 seed)

**Run:** `AS215-r1-20260928T172030Z-dsv4f-hermes`
**Worker:** deepseek/deepseek-v4-flash-0731 via OpenRouter, platform=subagent,
worker id `dsv4f-hermes` (Hermes agent executing seed AS215 on macOS 26.5.2).
**Started:** 2026-09-28T17:03Z · **Finished:** 2026-09-28T17:57Z (UTC).

---

## 1. Pinned inputs (all hashes verified before computing)

| Item | SHA-256 |
|---|---|
| Task `deepseek_push/astra_spawn_ideas/AS215_construct_a_criterion_b_characteristic_ordering_test.md` | `249144dce0828cd350f62d351660a1c723a254e635961146db6f79a4def5c9c9` ✓ matches pin |
| `real_research/common_action_2026_09_26/action/FINAL_ACTION.md` (CA4-GNC) | `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e` ✓ |
| `real_research/breakthrough_review_2026_09_26/vacuum/ACTION.md` (CA5-GNC-R) | `290e5cbe83eca682fb68888375bb60f9230f677cbb3176ae6ec27557e777211d` ✓ |
| `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md` | `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f` ✓ |
| `deepseek_push/astra_spawn_ideas/FRAMEWORK_CONTRACT.md` | `ca696c7fe7cccbe21d754eff833a4c59df6dee962ea61f50f04b5d20d80dddf9` |
| `deepseek_push/astra_spawn_ideas/RESULT_CONTRACT.json` | `621fdad0067c731654a0fa95eb7a4dd112f8829b96503d8d57c2ee8ca2cc1517` |

**Upstream:** `results/AS151/` landed (primary constraints of the localized
CA5-GNC-R action: 18 primaries, kinetic map rank 8, `pi_U = pi_W = pi_L =
pi_lambda0 = pi_Z = pi_N = pi_t = 0` on the bounded prototype) — used for the
constraint-character claim of the degenerate sector. `results/AS658/` landed
(three-form vacuum: zero propagating modes; gate for the fluctuation sector
open). `results/AS208/` (heat-operator metric derivative) not landed — *not
required* by this seed: the ordering certificate is built from the frozen
local symbol and the action's displayed equations only. Explicit prerequisite
`AS198` (high-frequency mixed-background symbol) is **not landed**; its deliverable
(the direction-dependent principal symbol with stated omissions) is here
replaced by the block-wise frozen symbol assembled directly from the pinned
action's own stated frozen quantities (FINAL_ACTION §6, eq. (17); vacuum R7),
each algebraically re-verified — the *full* elimination reduction remains an
open dependency (recorded in §12).

## 2. Conventions

Signature `−+++`, `c = 1` in action units (SI conversion at the end).
Foliation (FINAL_ACTION §1):

```
X_tau = -g^{mu nu} tau_mu tau_nu > 0,     n_mu = -tau_mu / sqrt(X_tau),
N = X_tau^(-1/2),   h_{mu nu} = g_{mu nu} + n_mu n_nu,    tau_mu = d_mu tau.
```

Adapted frame: `g_00 = -N^2`, `tau_mu = (1,0,0,0)`, `n^mu = (1/N, 0,0,0)`,
`sqrt(X_tau) = 1/N`, `tau^mu = (-1/N^2, 0,0,0)`.
**Invariant identity** (used throughout):

```
tau_mu = -n_mu / N   =>   xi_mu tau^mu = -xi(n) / N           (I)
```

The d-tau contraction of a covector is `-1/N` times its future-normal
contraction — one sign number controls the whole ordering test.
Numerics: `G = 6.67430e-11`, `c = 299792458`, `M_sun = 1.98847e30`,
`pc = 3.085677581491367e16` (SI); footings `a0 = 9.3619e-11` (canonical) and
`1.1279e-10 m/s^2` (alternative) carried separately. `kappa = 1/2` ADOPTED
(campaign mandate); `G_N`, `G_bare`, `G_cosmo` kept separate (not needed by
this seed's geometric content). Operative branch: CA5-GNC-R with the filtered
`nu_mono` gate (criterion B; the amended thirteen-item target).

## 3. The target (seed, verbatim) and the test definition

> `n_mu = -tau_mu/sqrt(X_tau); every characteristic trajectory must have
> nondecreasing tau, including leafwise degenerate propagation.`

**Test T (local frozen-symbol certificate), per block B with principal symbol
`X_B`:** at a frozen local background (adapted frame, leaf frame, frozen
`N, t_c, z, alpha_eff, gate data`):

- **T1 hyperbolicity w.r.t. dτ:** ∀ spatial `k ≠ 0` all roots of
  `s ↦ X_B(s·dτ + k)` are real (real scalar, tensor and carrier roots);
- **T2 ordering / future sheet:** the future sheet
  `F_B = {xi : X_B(xi) = 0, xi(n) > 0}` has a *uniform* dτ-contraction sign
  (`xi_mu tau^mu < 0` by (I) on the sheet `xi(n) > 0`), and the
  forward-oriented bicharacteristics of `F_B` satisfy `dτ/dλ > 0`
  (strictly nondecreasing τ);
- **T3 degenerate (leaf) sector:** leaf-elliptic blocks (heat filter
  `S_h = e^{b Δ_h}`, gate `G(Y_h)`, the `U,W,L,lambda0,Z` equations) have
  symbols *independent of ω* — no real ω-root at `k ≠ 0`; their characteristic
  trajectories are leaf-confined with `dτ/dλ = 0` (nondecreasing, zero elapse);
- **T4 no metric-cone restriction:** no bound `v ≤ c` is imposed or needed;
  superluminal blocks are ordered, not vetoed.

## 4. Block derivation from the pinned action

### 4.1 Tensor block
FINAL_ACTION §6: tensor principal action is Einstein's,
`M_P^2 a^3 [hdot_ij^2 - a^{-2}(Dh_ij)^2]/8`, speed one:

```
X_T(omega,k) = -omega^2 + |k|^2,    roots omega = ±|k|  (real).
```

### 4.2 Carrier block (CA5-GNC-R, vacuum/ACTION.md R1)
Dark Lagrangian `L_d = t K_d - W_exc/t`, `K_d = (1/2) Σ_A (n·∂φ_A)^2`,
`t = 1 + Z - <Z>_h > 0` (reciprocal barrier). Wave-operator symbol
(`C_d^{mu nu} = (1/t) h^{mu nu} - t n^mu n^nu`), physical frequency:

```
X_C(omega,k) = -omega^2 + t_c^{-2} |k|^2,    roots omega = ± t_c^{-1} |k|,
v_c = c / t_c   (five identical blocks).
```

Composite carrier metric `g_d = g + (1 - t_c^{-2}) n⊗n` satisfies the block
lapse identity

```
-g_d^{mu nu} tau_mu tau_nu = t_c^{-2} X_tau > 0   for EVERY t_c > 0    (L2)
```

— the foliation is a time function of the carrier metric for **all** `t_c > 0`:
superluminal carriers (`t_c < 1`) stay ordered (Lean-certified).
This is the operative form of AS198's "local `t_c > 0` sets carrier speed `1/t_c`".

### 4.3 Host scalar block — two declared frozen samples
**(a) Plateau sample** (FINAL_ACTION §6, frozen principal with the gate):

```
L_{2,red} = [2(2+3c2)/c2] psidot^2 - [2(2-alpha_eff)/alpha_eff] k^2 psi^2
c_s^2 = c2 (2 - alpha_eff) / ((2 + 3 c2) alpha_eff)
Q = 1 - (1-f) ell S_k / 4,  D = 1 + f C S_k^2 + (G''/4) S_k^2 [(J')^2 + ell^2 k^2],
alpha_eff = 2 - (2-alpha) Q^2 / D,   S_k = exp(-xi^2 k^2 / 2).
```

Verified: `1 - ell/4 ≤ Q ≤ 1`, `D ≥ 1`, `0 < alpha_eff < 2` (numeric scan,
12 corners), `c_s^2 > 0` (real roots). **Superluminal window** (corrected — see
§9): `c_s^2 > 1  ⟺  alpha_eff < c2/(1 + 2 c2)` (identified symbolically, verified
numerically, Lean-certified `scalar_speed_gt_one_iff`). Sample P2
(`c2=0.5, alpha=0.05, f=1, C=0.1` at small k) gives `alpha_eff = 0.226870`,
`c_s = 1.1165` — a **healthy scalar channel > c**.

**(b) Vacuum (de Sitter) sample** (vacuum/ACTION.md R7):

```
K_s = 2(2+3c2)/c2,  u = xi^2 x/2,  r = r0 S,  r0 = ell/4,  S = e^{-u},
d = 2-(2-alpha)(1-r)^2,  2 x d_x = -4(2-alpha) u r (1-r),  E = K_s H^2 + x d,
A = K_s x d / E > 0,   C_I = -(2 x^2/E^2)[K_s H^2 (2+d+2 x d_x) + x d (2-d)] < 0
=> X_S = -A omega^2 - C_I |k|^2,   speed^2 = -C_I/A > 0   (real roots).
```

`A > 0, C_I < 0` verified at three declared corners (V1–V3); corner V2
(`H^2=0.01, x=10`) is superluminal: `speed/c = 2.270`.

### 4.4 Degenerate (leaf) sector — T3
The heat/gate content of the action: `partial_r W = Δ_h W` (r = semigroup
direction, **not** physical time — FINAL_ACTION §1), `W_0 = U`,
`L_b = -R_W`, `lambda0 = L_0`; the U, Z, W, L equations (5)–(7), R4 contain no
`partial_tau`. Symbols: `Δ_h ↔ -|k|^2`, `S_h ↔ e^{-b|k|^2}` — verified ω-free
(d/dω ≡ 0, symbolic). Hence the degenerate sector has **no real characteristic
speed in τ**: its "cone" degenerates to the leaf; characteristic trajectories
are leaf-confined with `dτ/dλ ≡ 0`. Constraint character: `pi_U = pi_W = pi_L =
pi_lambda0 = pi_Z = 0` (AS151 bounded prototype); the static U-solve is elliptic
(J convex: `J' ≥ 0`, verified on both footings' p-grids; `nu_mono ≥ 1` verified
on `[1e-2, 1e2]`).

### 4.5 Clock block
`X_tau > 0` by declaration; the clock is the time function. Relabeling
controls are in §7 (NC-c).

## 5. The ordering computation (seed step 2)

For each block the two sheets are `omega = ± v |k|` with `v ∈ {1, t_c^{-1},
sqrt(|C_I|/A), c_s}`. In the adapted frame:

```
future sheet F_B:  xi(n) = omega/N > 0  <=>  omega = +v|k| > 0
dτ-contraction:    xi_mu tau^mu = -omega/N^2 = -v|k|/N^2 < 0   (uniform, (I))
forward-oriented bicharacteristic tangent T^0 = +2|omega| > 0  (dτ/dλ > 0)
```

Numerical certificate on the k-grid `[0.05, 20]`, N=17 (refined once to N=33):
min discriminant ≥ 0, max substitution residual `|X_B(omega_i,k)| < 6e-14`
(0.0 tensor), min `xi(n) > 0`, max `xi_mu tau^mu < 0`, and the invariant
identity `|xi·dτ + xi(n)/N| = 2.2e-16` — all four propagating blocks (tensor,
carrier at `t_c ∈ {1.3, 1.0, 0.7}`, plateau scalar P1–P3, vacuum scalar V1–V3)
**pass T1–T2**. Degenerate sector passes T3 (§4.4). The superluminal blocks
(carrier `t_c = 0.7` → `v = 1.4286 c`; scalar P2 → `1.1165 c`; vacuum V2 →
`2.270 c`) are certified forward, not vetoed (T4).

## 6. Global foliation obligation (seed step 3)

Local cone compatibility extends to **absence of closed causal curves** under
the following explicitly stated global conditions (each is *stated* here; only
their local parts are proved in this seed):

- **G1** `X_tau > 0` on all of M (τ a proper global time function; the adapted
  chart covers M; N finite and positive everywhere).
- **G2** Leaves compact, connected, closed and spacelike (declared for
  CA4-GNC / CA5-GNC-R).
- **G3** The degenerate leaf sector is constraint-like at the primary level
  (`pi_U = pi_W = pi_L = pi_lambda0 = pi_Z = 0`; AS151 bounded prototype) and
  elliptic-solvable per leaf datum (`J' ≥ 0`, J convex) — no leafwise signal
  *dynamics*.
- **G4** The heat-semigroup kernels are symmetric positive on each leaf
  (compact connected closed leaf, `S_h = e^{b Δ_h}`, `K(x,y) > 0` symmetric) —
  no directed leaf loop.

**Argument.** Any closed causal curve γ has `∮ dτ = 0`; by local cone
compatibility `dτ ≥ 0` a.e. along γ, so `dτ = 0` along γ: γ lies in one leaf.
Within a leaf the only channels are the degenerate-sector solves (G3); these
are unique per leaf datum and carry symmetric positive kernels (G4), so no
closed *signal* loop exists; finite-speed channels have strict `Δτ > 0`.
The continuum heat-operator lift on the general compact leaf (G2–G4 rigor) is
the AS151.C01-style open item (§12). The certificate is a **necessary**
condition for criterion B; the mixed Cauchy well-posedness estimate remains a
separate obligation (seed's own stop rule — see §12).

## 7. Negative controls (each capable of failing; all fired as designed)

- **C0 (substitution-back, algebra control):** every derived root solves its
  own block equation — symbolic residual `0` (A1–A2) and grid residuals
  `< 6e-14` (B1).
- **NC-a (healthy superluminal must pass; the metric-cone veto is the error):**
  carrier `t_c = 0.7`, `v = 1.4286 c`. The naive veto (`v > c ⇒ reject`)
  rejects it (`veto_rejects = True`); the criterion-B test passes all of T1–T3
  (measured residuals above) — the test **distinguishes** the veto error.
- **NC-b (ghost must fail):** kinetic sign flipped (`A = -t_c`):
  `X = +omega^2 + v^2 k^2` has no real root — measured max discriminant
  `-2.041e-02 < 0` on the whole grid — hyperbolicity T1 fails, certificate
  FAILS. (Lean: `ghost_no_real_root`.)
- **NC-c (negative-time clock must fail; finite-speed check is the error):**
  `T' = -tau` gives `X_{T'} = -X_tau = -5.917e-01 < 0` while all block speeds
  are finite — a finite-speed-only check accepts T' (`True`); the ordering
  check fails (sign flipped). The criterion-B test **distinguishes**.

## 8. Gate (MONO) static-sector inputs to T3

Actual crossing solved, not assumed: `y_p = 2.5396382822` (peak of
`h_RAR`), `y_star = 2.3374124053` (`h'_RAR` = `δ h_p/(y+y_p)` crossing),
matching the contract's rounded landmarks to relative `1.5e-5` / `5.3e-6`.
`nu_mono ≥ 1` on `[1e-2, 1e2]` (min excess `7.46e-3`); `J'(p) ≥ 0` and
`J'` nondecreasing on both footings' p-grids (convexity input; J'(0)=0 by
`q(0)=0`).

## 9. Corrected superluminal window (a control-caught error)

First draft of the scalar window used threshold `c2/(1+c2)`; the symbolic
numerator check failed and the corrected identity is

```
(c_s^2 - 1) (2+3c2) alpha_eff = 2 c2 - 2 (1 + 2 c2) alpha_eff,
c_s^2 > 1  ⟺  alpha_eff < c2/(1 + 2 c2).
```

Verified symbolically (residual 0), on 24 random gate samples (max residual
`3.55e-15`), and cross-checked sample-wise (B3: window ⟺ cs2 > 1 both ways).
P2 remains superluminal under the corrected threshold (`0.226870 < 0.25`).

## 10. Footings and dimensional speeds

The ordering certificate is a statement about speed ratios `v/c`; the cone
geometry is a0-independent (a0 enters only the static gate amplitude
`J ~ 2 a0^2 q(...)`, never the principal symbols — verified E2). Both footings:

| channel | v/c | SI (m/s) |
|---|---|---|
| tensor | 1 | 2.997925e8 |
| carrier (t_c=0.7) | 1.428571 | 4.282749e8 |
| carrier (t_c=1.3) | 0.769231 | 2.306096e8 |
| scalar plateau P2 | 1.116516 | 3.347231e8 |
| scalar vacuum V1 | 0.778802 | 2.334789e8 |

Footing bookkeeping: canonical `rho_Lambda = 5.844412e-27 kg/m^3` at kappa=1/2;
alternative at *fixed* rho_Lambda gives `kappa_eff = 0.60238840` (≠ 1/2 — the
two footings share neither a fixed density nor a fixed kappa; E1).

## 11. Domain, bounds, refinement

- Frozen local background; identity leaf frame (exact algebra) + general-symmetric-h
  fiber numerics; k-grid `[0.05, 20]` N=17 → **refined once** to N=33;
  carrier `t_c ∈ {0.7, 1.0, 1.3}`; plateau scalar P1–P3 (+12-corner bound scan);
  vacuum scalar V1–V3; MONO y/p-grids 401 pts (seed 20260928; A3 random-sample
  seed 7).
- **Enforced bounds:** wall `0.111 s` (declared ≤ 120 s); peak RSS `82.42 MiB`
  (declared ≤ 512 MB); 1 thread (`OMP/OPENBLAS/MKL/VECLIB/NUMEXPR_THREADS=1`,
  `threading.active_count() = 1`, single process). macOS refused `RLIMIT_AS`
  (recorded verbatim: "*RLIMIT_AS not settable: current limit exceeds maximum
  limit*") — measured peak far below the declared cap (same limitation
  recorded by AS151).
- All 37 checks PASS with actual residuals (not booleans) in `residuals.json`.

## 12. Classification and open implications

**Classification: derived (scoped).** A local time-orientation certificate for
the CA5-GNC-R frozen local symbol: every characteristic trajectory of the
propagating blocks (tensor at c, five carriers at c/t_c, host scalar at c·c_s)
has strictly nondecreasing τ; the degenerate heat/gate sector is leaf-confined
with dτ = 0; superluminal channels are certified forward-in-τ under criterion B.
The global obligation (G1–G4) is stated explicitly, with the no-closed-causal-
curves argument conditional on it; **not** promoted to gravity closure.

**next_unresolved_implication:** the mixed (hyperbolic + elliptic-constraint)
Cauchy well-posedness estimate for the coupled CA5-GNC-R system in the physical
norm — the local orientation certificate is necessary, not sufficient, for
criterion B's "well-posed mixed Cauchy problem"; requires (i) the continuum
lift of the heat/gate operators on a general compact leaf (AS151.C01 scope),
(ii) a Kreiss-type energy estimate / weak-strong uniqueness (AS1043/AS1118
scope), and (iii) the full frozen-scalar reduction re-derivation (AS198 scope,
prerequisite not landed — the plateau scalar symbol here uses the pinned
action's stated reduction, algebraically verified, not re-derived from the full
nonlinear variation).

**Child proposal (ready spec, not dispatched — runner cannot spawn):**
`AS215.C01` — *Uniform τ-margin and coupled well-posedness*: (a) bound
`X_tau` away from zero along finite clock/gate packets (AS1084 fixture:
`X_tau ≥ x0 > 0` for the declared background and finite momentum band),
(b) derive the energy inequality for the constrained hyperbolic-elliptic system
using this certificate's block decomposition (tensor/carrier/scalar speed
coefficients) as input; discriminating control: the NC-b ghost symbol must
violate the energy inequality, the superluminal carrier must not. Dependencies:
this run, AS1084, AS1043, AS1118. Dispatch state: *not dispatched*.

## 13. Lean certificates

| File | Content | Verification |
|---|---|---|
| `AS215_carrier_ordering.lean` | L1 roots ±k/t_c substitute back; L1d sheet distinctness; L2 future-sheet contraction sign + invariant (I); L3 composite block lapse `X_tau/t^2 > 0` ∀ t > 0 (superluminal ordered); L4 ghost no-real-root; tensor t=1 case | `lake env lean` exit 0 |
| `AS215_scalar_window.lean` | W0 numerator identity; W1 `c_s^2 > 0`; W2 `c_s^2 > 1 ↔ alpha_eff < c2/(1+2c2)`; W3 window nonempty | exit 0 |
| `AS215_clock_and_degenerate.lean` | C1 `-X_tau < 0` (negative clock fired); C2 `k^2 ≠ 0` (no τ-root, degenerate sector); C3 `T^0 = 2ω > 0` (forward bicharacteristics) | exit 0 |
| `AS215_axioms_check.lean` | merged certificate + `#print axioms` for all 17 theorems | exit 0; **every** theorem: `[propext, Classical.choice, Quot.sound]` — zero sorry |

Compile host only: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>` —
no files written into the compile host.

## 14. Provenance

Commands:
```
shasum -a 256 <pinned task and source files>            (all verified, §1)
cd <run dir> && export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 NUMEXPR_NUM_THREADS=1 \
  && /usr/bin/time -l python3 compute_as215.py > raw_output.txt 2> time_mem.txt
cd fable_independent_2026/lean_2026 && lake env lean <abs>/AS215_*.lean
```
Artifacts (sha256 in `result.json`): `compute_as215.py`, `raw_output.txt`,
`residuals.json`, `time_mem.txt`, three certificate files, merged
`AS215_axioms_check.lean`, four lean output logs. No shared status file,
manifest, ledger or claims file was modified; no child was dispatched.