# AS147 — Derivation: the diagonal U(1) Noether current of the five-field carrier

- Run: `AS147-r1-20260928T145834Z-dsv4f-hermes`
- Task file: `deepseek_push/astra_spawn_ideas/AS147_derive_the_diagonal_u_1_noether_current.md`,
  verified `sha256 = cf210c8fc5db2990f3a24815a98675fc9cd24cba112a0db48391d63fbfe5d551` **before** execution (unchanged on disk; no rename, no paraphrase).
- Tier-0 of the 2000-task gravity-closure campaign. Siblings: `results/AS137` (matter Ward identity),
  `results/AS142` (carrier Legendre transform). This seed derives and numerically verifies the diagonal
  U(1) Noether current of the five-field carrier (CA5-GNC-R / CA4-GNC host).

---

## 0. Framework cell (inputs, adopted, not derived here)

| symbol | value | status |
|---|---|---|
| `a0` | `kappa * c * sqrt(G * rho_Lambda)` | framework normalization |
| `kappa` | `1/2` | **ADOPTED as input** (mandated) |
| `a0_canon` | `9.3619e-11 m/s^2` | footing 1 |
| `a0_alt` | `1.1279e-10 m/s^2` | footing 2 (separate footing, `a0_alt/a0_can = 1.20478`) |
| `G, c` | `6.67430e-11`, `299792458` (SI) | numerics constants |
| `M_sun, pc` | `1.98847e30 kg`, `3.085677581491367e16 m` | SI |
| branches | Q, RAR, MU2, EXP, MONO | criterion B NOT exercised (Tier-0 algebra) |
| `B` | `B = t^{-1}` (CA5-GNC-R); exponential host `B = e^{-z}` | identical U(1) sector |

The U(1) sector derived below is **branch-agnostic**: it is fixed by the carrier action's potential
and the metric sector (`C^{mu nu}`), which are common to all five branches. No branch kernel is
imported into any identity; branch labels appear only in the limitations and follow-up sections.

---

## 1. Action and conventions

The five-field carrier action (CA5-GNC-R, `FINAL_ACTION` eqs. 1,8; `PERSPECTIVE_VARIANT` P1):

```
S = int d^4x sqrt(-g) [ (1/2) C^{mu nu} ( d_mu phi_a d_nu phi_a + d_mu chi_a d_nu chi_a )
                        - B V(phi, chi, s) ]
C^{mu nu} = t^{-1} h^{mu nu} - t n^mu n^nu,      t = t_c = 1 + Z - <Z>_h > 0
V = (1/2) mH^2 |phi|^2 + (1/2) mL^2 |chi + gamma s phi|^2 + (1/2) mu^2 s^2
B = t^{-1}
```

Conventions used throughout (flat unit-lapse leaf for the numerics, `t = 1`, `B = 1`):
`g_{mu nu} = diag(-1, 1, 1, 1)`, `n^mu = (1, 0, 0, 0)`, `h^{mu nu} = g^{mu nu} + n^mu n^nu`,
so `C^{00} = -1`, `C^{ij} = delta^{ij}`, `C^{0i} = 0`; `C^{mu nu}` is **symmetric**.
`epsilon_ab` is the 2D Levi-Civita tensor, `epsilon_12 = +1`.
The `|chi + gamma s phi|^2` contraction mixes the two doublets with coefficient `gamma` (a `M^{-1}`
coupling in natural units) via the singlet `s`.

## 2. Symmetry

Diagonal U(1) (common phase rotation of both doublets):

```
phi_a -> phi_a + d * eps_ab phi_b + O(d^2),     chi_a -> chi_a + d * eps_ab chi_b + O(d^2),     s -> s
```

Check each term of V under this rotation (exact, symbolic):

- `|phi|^2` is invariant (rotates within the doublet).
- `s` is invariant by `delta s = 0`.
- `chi + gamma s phi` transforms as a doublet (`delta(chi_a + gamma s phi_a) = d eps_ab (chi_b + gamma s phi_b)`),
  so `|chi + gamma s phi|^2` is invariant.
- The kinetic term is invariant because `C^{mu nu}` is symmetric and `epsilon_ab d_mu phi_a d_nu phi_b`
  contracts antisymmetrically: `eps_ab A_a B_b + eps_ab B_a A_b = 0` (Lean `curl_term_antisym`).

Hence the diagonal U(1) is an exact symmetry with **Noether current** (symbolic extraction,
`delta L = -d * div J`):

```
J_psi^mu = eps_ab psi_a C^{mu nu} d_nu psi_b,        psi in {phi, chi}
J^mu = J_phi^mu + J_chi^mu.
```

Sign conventions verified by direct substitution: under `delta psi_a = d eps_ab psi_b`,
`delta L_kin = -d * d_mu [eps_ab psi_a C^{mu nu} d_nu psi_b]` — i.e. `J^mu` as written with
`+eps_ab psi_a` (Lean `sym_gauge_extraction` verifies the extraction identity
`(p1 - f2 d)^2 + (p2 + f1 d)^2 - p1^2 - p2^2 - 2 d (f1 p2 - f2 p1) - d^2 |f|^2 = 0`).

## 3. Divergence identity (the theorem)

For any field configuration satisfying the phi, chi equations of motion:

```
d_mu J_phi^mu = eps_ab phi_a [C^{mu nu} d_mu d_nu phi_b]
              = eps_ab phi_a [nabla^2 phi_b]                        (C symmetric kills the dpsi dpsi term)
              = eps_ab phi_a [mH^2 phi_b + gamma mL^2 s (chi_b + gamma s phi_b)]      (EOM, B = 1)
              = + gamma mL^2 s (phi_1 chi_2 - phi_2 chi_1)          (mass terms eps-contract to 0)
```

Every intermediate sign:

1. `d_mu J^mu = eps_ab d_mu psi_a C^{mu nu} d_nu psi_b + eps_ab psi_a C^{mu nu} d_mu d_nu psi_b`.
2. First term vanishes: `eps_ab A_a B_b + eps_ab B_a A_b = 0` with `A_mu = d_mu psi`, `B_nu = d_nu psi` (symmetric
   contraction with `C^{mu nu}`; Lean `curl_term_antisym`). **Without** symmetric C (corrupt
   `C^{01} != C^{10}`) this term survives — symbolic control `sym_epsC_asymmetric = -p1 q2 + p2 q1 != 0`.
3. `C^{00} = -1`, `C^{ii} = +1` give `C^{mu nu} d_mu d_nu = -d_tau^2 + d_x^2 = nabla^2` (Minkowski).
4. On shell with `B = 1`: `nabla^2 phi_b = V_{phi_b}`; the diagonal mass term
   `eps_ab phi_a mH^2 phi_b = mH^2 (phi_1 phi_2 - phi_2 phi_1) = 0` (Lean `diag_mass_antisym`).
5. The mixing term `gamma mL^2 s eps_ab phi_a phi_b` also vanishes; only
   `gamma mL^2 s eps_ab phi_a chi_b = gamma mL^2 s (phi_1 chi_2 - phi_2 chi_1)` survives.

Same computation for chi (EOM `nabla^2 chi_b = mL^2 (chi_b + gamma s phi_b)`):

```
d_mu J_chi^mu = eps_ab chi_a [mL^2 (chi_b + gamma s phi_b)]
              = - gamma mL^2 s (phi_1 chi_2 - phi_2 chi_1)
```

**Signed exchange-source pair:**

```
E := gamma mL^2 s (phi_1 chi_2 - phi_2 chi_1)
d_mu J_phi^mu = +E        (chi -> phi leak)
d_mu J_chi^mu = -E        (chi <- phi leak)
d_mu J_total^mu = d_mu (J_phi + J_chi)^mu = 0      (total diagonal charge conserved)
```

Lean-certified: `exchange_phi`, `exchange_chi`, `exchange_pair_cancels` (all `ring`, axioms
`{propext, Classical.choice, Quot.sound}`, zero sorry).

**Normalized conserved current** (charge form):

```
Q := int_leaf d^3x sqrt(h) n_mu J^mu        (n_mu = (-1, 0, 0, 0): n.J = -J^0 = eps psi d_tau psi)
j^mu := J^mu / Q
dQ/dtau = int_leaf sqrt(h) d_mu J^mu = 0    (total divergence; leaf periodic, no boundary)
```

The charge density is `n.J = eps_ab psi_a d_tau psi_b = omega |psi|^2` for a rotating in-phase mode,
so `Q != 0` whenever the mode is populated.

## 4. Static sector (limiting case, exact)

Static on-shell configurations of the phi, chi subsystem at fixed `s` solve
`(-Delta + V_stat) psi = 0` on the compact leaf, with

```
V_stat = [[ mH^2 + gamma^2 mL^2 s^2,  gamma mL^2 s ],
          [ gamma mL^2 s,             mL^2          ]]
det V_stat = mH^2 mL^2 > 0   (Lean `potmat_det`)
```

`-Delta + V_stat` is positive definite (`lambda_min = k_min^2 + v_min = 1.4996 > 0` in the
prototype cell), so by the maximum principle the **only static state is the trivial one**
(phi = chi = 0): with positive masses there are **no nontrivial static carrier states on the compact
leaf**, and the exchange source`E` requires **time-dependent** states. Recorded limiting case `LC1`;
the homogeneous rotating mode is an exact on-shell time-dependent state (below).

## 5. On-shell demonstration states (exact, closed form)

### 5.1 Coupled two-mode state (the NC1 arena: nonzero exchange source required)

For a mode pair at common frequency `omega = sqrt(P)`, `y_j = k_j^2`, the coupled EOMs at fixed
background `s` are

```
(P - y - a)(P - y - b) = c,     a = mH^2 + gamma^2 mL^2 s^2,  b = mL^2,  c = gamma^2 mL^4 s^2
r_j := chi-hat_j / phi-hat_j = (P - y_j - a) / (gamma mL^2 s)          (amplitude ratio)
```

**Cell chosen with integer wavenumbers** `k_1 = 2`, `k_2 = 1` on `[0, 2 pi)` (band-limited,
FFT-exact): the mixing field `s` is the bisection root of `(a - b)^2 + 4 c = (y_1 - y_2)^2 = 9`
with `P = (y_1 + y_2 + a + b)/2` (root-sum `y_1 + y_2 = 2P - (a + b)`, Lean `cell_sum`);
`mH = 1.0`, `mL = 1.3`, `gamma = 0.7` fixed. Resulting cell: `s = s* = 1.243...`,
`a = 2.27988665, b = 1.69, c = 2.16300844, P = 4.48494332, r_1 = -1.22045461, r_2 = 0.81936681`.

State (exact on shell for phi, chi at fixed background s, seed input "s fixed"):

```
phi_1 = A_1 cos(theta_1) + A_2 cos(theta_2),   phi_2 = A_1 sin(theta_1) + A_2 sin(theta_2)
chi_a = r_1 A_1 e_a(theta_1) + r_2 A_2 e_a(theta_2),   theta_j = omega t - k_j x,  A_1 = A_2 = 1/2
```

On-shell witnesses (residuals `(d_x^2 + omega^2) psi - V_psi` since `d_tau^2 = -omega^2`):
`max |res| ~ 1e-15/1e-16` on 128- and 512-point grids. The mode-ratio consistency
`(P - y - a)/(gamma mL^2 s) = gamma mL^2 s/(P - y - b)` is Lean-certified
(`mode_ratio_consistency`), as is the on-shell coefficient collapse
`mH^2 + gamma mL^2 s r + gamma^2 mL^2 s^2 = P - y` (`onshell_coefficient`).

Exchange source of this state:

```
E(x) = gamma mL^2 s A_1 A_2 (r_1 - r_2) sin((k_2 - k_1) x),     max |E| = 0.7500000000  (measured)
```

**Nonzero** — the negative control `NC1` ("phi-only rotation with nonzero gamma*s requires a
nonzero exchange source") is satisfied: the rotating mixture of two non-collinear on-shell modes
is exactly the arena in which the exchange leaks.

Divergence identity on this state (grid 128 / refinement 512):

```
max |div J_phi - E|  = 1.33e-9 / 1.55e-9    (finite-difference d_tau J^0 truncation, delta = 1e-6; honest residual, not a boolean)
max |div J_chi + E|  = 1.33e-9 / 1.33e-9
max |div J_total|    = 9.33e-10 / 1.34e-9
max |d_tau J^0|      = 1.33e-9 / 1.55e-9    (J^0 is tau-independent to this noise floor)
EOM residuals        = 8.9e-16 / 8.9e-16 (all four fields, both grids)
```

### 5.2 Homogeneous rotating mode (charge normalization `LC2`)

In-phase rotation at constant `s_0 < 0`: `chi-hat = r phi-hat` with
`r = b/a` (positive root of `gamma mL^2 s r^2 + (mH^2 + gamma^2 mL^2 s^2 - mL^2) r - gamma mL^2 s = 0`),
amplitude fixed by the s-EOM: `a^2 = -mu^2 s / (gamma mL^2 (r + gamma s))` (Lean `sEOM_amplitude`),
`omega^2 = mH^2 + gamma mL^2 s (r + gamma s)`.

Measured (cell `mH = 1, mL = 1.3, mu^2 = 0.5, gamma = 0.7, s_0 = -0.8`):
`r = 0.91902778, a = 0.97045097, b = 0.89187140, omega = 0.81253684`;
EOM residuals `0.0 / -2.2e-16 / 5.6e-17`; `n.J = omega(a^2 + b^2) = 1.41154685 != 0`
(`Q != 0`), `E_homogeneous = -0.0` (modes collinear, no exchange), `dQ/dtau = 0`. Normalization
`j^tau = J^tau/Q = 1` on this state.

## 6. Negative controls (each capable of failing; actual residuals)

| id | statement | measured | verdict |
|---|---|---|---|
| NC1 | phi-only rotation with nonzero `gamma*s` requires **nonzero** exchange source | `max|E| = 0.7500000` | PASS (nonzero) |
| NC2 | corrupt sign (`div J_phi = -E`) does NOT satisfy the identity | `max |divJ_phi + E| = 1.5000000 = 2 max|E|` | PASS (fails as designed) |
| NC3 | collinear `chi = lambda phi` ⇒ `E identically 0` | `max|E_coll| = 1.63e-16` | PASS |
| NC4 | `gamma = 0` ⇒ separately conserved currents (two-mode states at per-mode frequencies) | `max|div J_phi^0| = 6.32e-11`, `max|div J_chi^0| = 5.02e-11`, EOM res `1.1e-15/8.9e-16` | PASS |
| LC1 | static sector: only the trivial state on the compact leaf | `lambda_min(-Delta+V) = 1.4996 > 0`, `det V = mH^2 mL^2` | PASS (limiting case) |
| LC2 | homogeneous rotating mode: `Q != 0`, `dQ/dtau = 0`, `E = 0` | `Q ∝ 1.41154685`, `E = -0.0`, res `~1e-16` | PASS |

Symbolic (sympy) checks: phi/chi exchange identities = 0 exactly; pair sum = 0; diagonal-mass
antisym = 0; gauge-extraction = 0; epsC symmetric-contraction = 0 **and** asymmetric-contraction
= `-p1 q2 + p2 q1 != 0`; phi-only potential variation = 0; `E |_{gamma=0} = 0`;
`det V = mH^2 mL^2`. All `ok: true`.

## 7. Bounds actually enforced

- Wall clock **`<= 120 s`**: `signal.alarm(120)` — alarm armed at start; observed compute wall
  `0.077 - 0.281 s` across runs (final 0.281 s), i.e. enforcement trivially satisfied.
- Memory **`<= 512 MB`**: `resource.setrlimit(RLIMIT_AS, 512MB)` **rejected by the macOS host**
  (`ValueError: current limit exceeds maximum limit`) — recorded honestly in `raw_output.json`
  (`memory_note`). Observed peak RSS: 82.4 MB (`ru_maxrss`), far below the bound; single process.
- Threads **1**: single process, `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`,
  `numpy_single_threaded: true`; no subprocesses, no BLAS threads.

## 8. Lean 4 certificate

`AS147_diagonal_u1_noether_current.lean` (12 theorems + 1 def), Mathlib `v4.34.0-rc2`:

```
exchange_phi, exchange_chi, exchange_pair_cancels, diag_mass_antisym, collinear_zero,
gamma0_zero, potmat_det, curl_term_antisym, onshell_coefficient, mode_ratio_consistency,
cell_sum, sEOM_amplitude
```

Verified: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>` → **exit 0**;
**zero `sorry`**; unfiltered `#print axioms` for all 13 objects →
`'<name>' depends on axioms: [propext, Classical.choice, Quot.sound]` (exactly the allowed set).
Compile log: `lean_compile_out.txt` in the run dir. Nothing was written into
`fable_independent_2026/lean_2026` (compile host only).

## 9. Footings and units

- Prototype cell in natural units (`c = 1`, fields and masses in powers of `M`, `gamma` in `M^{-1}`):
  `mH = 1.0`, `mL = 1.3`, `mu^2 = 0.5`, `gamma = 0.7`, `s` cell `1.2433...` (two-mode) / `-0.8`
  (homogeneous), `k_1 = 2`, `k_2 = 1`, `omega = 2.11777`.
- The U(1) sector does not contain `a0`; the framework footings enter at the closure level:
  `a0 = kappa c sqrt(G rho_Lambda)` with `kappa = 1/2` adopted — `9.3619e-11 m/s^2` (canonical) and
  `1.1279e-10 m/s^2` (alternative) are quoted **separately** (never mixed);
  with `G = 6.67430e-11`, `c = 299792458`, `M_sun = 1.98847e30`, `pc = 3.085677581491367e16` (SI).
- `G_N/G_bare/G_cosmo` kept separate: no gravitational coupling enters the current algebra here;
  the only mass parameters are the carrier's `mH, mL, mu, gamma`.
- Branches Q / RAR / MU2 / EXP / MONO: none imported into the derivation; criterion B untouched
  (Tier-0, algebra only). Any branch-specific statement is flagged in `result.json` limitations.

## 10. Failed attempts (recorded honestly — all caught by the controls)

1. **Residual sign convention** (`d_tau^2 = -omega^2`): first implementation used
   `(d2x - omega^2 psi) - V_psi` instead of `(d2x + omega^2 psi) - V_psi`; EOM residuals were
   `O(1)` (`res_f1 = 8.23`) — the substitute-back control failed as designed. Fixed after the
   algebra re-derivation of section 3.
2. **Non-integer wavenumbers ⇒ FFT leakage**: the first two-mode cell had
   `k_1 = 0.786, k_2 = 1.871`, i.e. non-periodic fields on `[0, 2 pi)`: the analytic EOM residual
   passed (1e-16 continued derivative check) but the grid divergence check measured
   `max|div J_phi - E| = 1.246` (boundary jump of the sampled extension). Root cause identified
   and fixed by the **integer-wavenumber cell** (bisection on `s`, `k_1 = 2`, `k_2 = 1`); divergence
   residual dropped to `1.3e-9` (finite-difference floor). This is exactly the "capable of failing"
   property exercised.
3. **Dispersion root-sum slip** in the cell construction: first attempt fixed `P = 5/2`; the correct
   constraint is `y_1 + y_2 = 2P - (a + b)` (Lean `cell_sum`), so `P` is determined by the cell —
   fixed, exactness witnesses `disp_res_1/2, sum_res ~ 1e-15`.
4. **NC4 trivial state + sign slip**: the gamma = 0 control initially used single modes (constant
   currents — vacuous) and inherited the `-omega^2` slip; upgraded to two-mode per-frequency states
   with centered finite differences; final residuals `6e-11` (threshold `1e-8`), EOM `1e-15`.
5. **Lean iterations** (5 compile rounds): `λ` is reserved (renamed `lam`); `ring` cannot close
   goals with `inv` monomials left by `field_simp` on this Mathlib build (replaced by pure-ring
   proofs with `div_mul_cancel₀`/`mul_left_cancel₀`/`field_simp`-free cross multiplication);
   `div_eq_iff` vs `eq_div_iff` orientation; `hden` parenthesization mismatch
   (`P - y - mH2 - x` vs `P - y - (mH2 + x)`); trailing-tactic-after-`field_simp` trap avoided by
   leaving `field_simp` as the final tactic where it closes.

## 11. Limitations

- Static compact-leaf sector carries no nontrivial on-shell carrier states (positive masses,
  maximum principle, `LC1`); the nonzero-exchange demonstration is **time-dependent** with
  `s` fixed background (the seed's own input), and the five-field full on-shellness (including the
  s-EOM with `mu^2 s + gamma mL^2 phi.(chi + gamma s phi) = 0`) is achieved only on the
  homogeneous mode `LC2` and for the phi,chi subsystem on the two-mode state.
- `B = t^{-1}` enters at `B = 1` (unit lapse, `t = 1`); the general-lapse factor is a one-line
  exact rescaling (`E -> B E`) but is not re-verified numerically here.
- The leaf-averaged exchange vanishes (`<E>_leaf = 0`, odd parity in `x`); the closure must show
  where the *local* exchange acts (see next implication).
- Natural-unit carrier cell is not yet numerically connected to the physical `a0` footings; the
  footings are quoted at the framework level only.
- `kappa = 1/2` remains adopted, not derived. RLIMIT_AS unavailable on this macOS host (recorded).
- Tier-0: no operative-branch (filtered MONO, criterion B) conclusion; branch labels are
  comparison/limitation references only.

## 12. Commands (as executed)

```
shasum -a 256 deepseek_push/astra_spawn_ideas/AS147_derive_the_diagonal_u_1_noether_current.md
  -> cf210c8fc5db2990f3a24815a98675fc9cd24cba112a0db48391d63fbfe5d551 (verified before execution)
time python3 results/AS147/AS147-r1-20260928T145834Z-dsv4f-hermes/compute_as147.py \
  > results/AS147/AS147-r1-20260928T145834Z-dsv4f-hermes/raw_output.json \
  2> results/AS147/AS147-r1-20260928T145834Z-dsv4f-hermes/raw_output.stderr
  (cwd: repo root; EXIT=0; real 0.281 s / user 0.247 s / sys 0.031 s; alarm(120) armed; 1 thread)
cd fable_independent_2026/lean_2026 && lake env lean <abs run dir>/AS147_diagonal_u1_noether_current.lean
  > run-dir/lean_compile_out.txt 2>&1   (EXIT=0; 13/13 axioms [propext, Classical.choice, Quot.sound]; 0 sorry)
```

## 13. Next unresolved implication & suggested follow-up

**Next unresolved implication:** the diagonal U(1) exchange is locally nonzero (`max|E| = 0.75` in
the cell) yet leaf-average-vanishing; the unresolved physical question is what *boundary-driven*
or *space-time-varying-s* sector makes `dQ/dtau != 0` locally (the toolbar for the matter Ward
identity sibling AS137), i.e. the coupling of the exchange pair to the lapse/expansion sector
(`B = t^{-1}`) and through it to the matter current `div J_matter = ...` of the closure.

**Suggested follow-up (ready child):** `AS147.C01` — "leaf-exchange theorem for the coupled
carrier: exact `div J_phi = E`, `div J_chi = -E` on general lapse `t != 1` (B rescaling) and the
existence/completeness of time-dependent on-shell states with `dQ/dtau != 0` on a driving leaf;
controls: B-rescaling identity, homogeneous-limit `E -> 0`, collinear limit, corrupt-sign control,
and a full 5-field (s dynamical) two-mode state with `s(x)` non-constant." Duplicate check vs
AS/MY manifests and the FGF queue: sibling AS137 (matter Ward identity) targets the *matter*
current, AS142 the *carrier Legendre transform*; no task targets the *exchange-source pair
transport theorem at general lapse*. Not dispatched (no subagent spawner in this worker); ready
spec returned per `FIRST_PRINCIPLES_AND_BRANCHING.md`.
