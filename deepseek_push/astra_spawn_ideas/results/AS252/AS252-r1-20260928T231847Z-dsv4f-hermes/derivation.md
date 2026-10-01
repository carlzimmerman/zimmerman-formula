# AS252 — Match the cosmological Einstein coefficient to measured Newton gravity

**Run:** `AS252-r1-20260928T231847Z-dsv4f-hermes`
**Worker:** deepseek/deepseek-v4-flash-0731 via openrouter (Hermes subagent, hermes-agent runtime on macOS)
**Seed:** `deepseek_push/astra_spawn_ideas/AS252_match_the_cosmological_einstein_coefficient_to_measured_newton_gravity.md`
sha256 `6de8d3e8bd3b8da9fe7e2953e04d0055d54382adafaaac64826ee12bbff1f5d2` (verified at start, == mandated value)
**Action:** `real_research/common_action_2026_09_26/action/FINAL_ACTION.md` sha256
`b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e` (verified on disk, == pinned)
**Support pinned:** `.../transport/HOMOGENEOUS_FRW.md` `ecc93b07...685c1d`, `.../vacuum/ACTION.md` `290e5cbe...7211d` (verified on disk)
**Tier:** 0b — the G_cosm/G_N link of the cosmological Einstein coefficient to measured Newton gravity.
**Branch:** CA5-GNC-R homogeneous inactive branch (Q, RAR, MU2, EXP, MONO untouched; criterion B operative).

---

## 0. Summary of the result

On the CA5-GNC-R homogeneous inactive branch with the local reciprocal high-k
normalization (upstream `results/AS226`, same frozen action):

```
G_cosm := (8 pi M_P^2)^(-1) = G_bare ,        M_P^2 = (8 pi G_bare)^(-1)   (action normalization)
G_N     = G_bare / c_N ,                      c_N = 1 - alpha/2 ,           0 < alpha < 2
G_cosm / G_N = c_N = 1 - alpha/2        in (0,1)                      (FINAL_ACTION eq. (18))
```

The seed's specific deliverable is the **vacuum-scale dictionary** that carries
this ratio into every a0-vacuum ↔ cosmological quantity:

```
rho_Lambda = 4 a0^2/(G_N c^2)                        [kg m^-3]   (operational a0 scale, kappa = 1/2)
Lambda_eff = 8 pi G_cosm rho_Lambda / c^2 = 32 pi c_N a0^2 / c^4   [m^-2]
H_vac^2    = Lambda_eff / 3 = (32 pi / 3) c_N a0^2 / c^4           [s^-2]
```

A premature `G_cosm = G_N` replacement mis-sets `Lambda_eff -> Lambda_naive =
32 pi a0^2/c^4` (factor `1/c_N = 1/(1 - alpha/2) in (1,2)` too large): the
negative control fires, and the term it removes is the `alpha`-sector of the
compensated gate (`+2 alpha DZ.DU` and `-(alpha/2)[G(Y_h) - ell Delta_h W_b]` in
the lapse density, units `M_P^2/2`), i.e. it silently enforces `alpha = 0`, off
the declared open domain. `alpha -> 0` recovers the standard Einstein
normalization (`G_N = G_bare`, `Lambda_eff = Lambda_naive`, coefficient
`8 pi G_bare/3` in H^2) — control A passes.

Outcome: **supports_scoped_claim** (a normalized dictionary; does not close the
thirteen requirements; `alpha` and `kappa` remain free).

---

## 1. Framework inputs (adopted, not derived here)

- `a0 = kappa c sqrt(G rho_Lambda)`, **kappa = 1/2 adopted** (seed mandate; the
  AS138.C01 continuum `kappa(r) = sqrt(2/(r+2b))` shows kappa is not pinned by
  that conservation identity — see Limitations).
- Constants (SI): `G_N = 6.67430e-11 m^3 kg^-1 s^-2`, `c = 299792458 m/s`,
  `M_sun = 1.98847e30 kg`, `pc = 3.085677581491367e16 m`.
- Footings kept **separate** (never both fixed density AND fixed kappa):
  - canonical `a0 = 9.3619e-11 m/s^2` → `rho_Lambda = 5.844412e-27 kg m^-3`,
  - alternative `a0 = 1.1279e-10 m/s^2` → `rho_Lambda = 8.483090e-27 kg m^-3`.
  Both give `kappa_backcheck = 0.500000000` exactly. Holding the canonical
  density fixed with the alternative a0 gives effective `kappa = 0.602388 != 1/2`
  (check N2 fires, per the contract's two-footing discipline).

---

## 2. Step 1 — coefficient multiplying homogeneous energy in the lapse equation

Exact fixed-h lapse equation, FINAL_ACTION eq. (13), units `M_P^2/2`:

```
(M_P^2/2){ R^(3) - T_K - 2 Lambda + c_2[-Q_K^2 + 2 K Q_K - 2 K A_K/N]
           + V_a - div_N[2 alpha(a-DZ) + 4 DZ] + c_N[G(Y_h) - ell Delta_h W_b] } = rho_b + rho_d
```

On the homogeneous inactive branch: `R^(3) = 0` (flat k=0 slices), `K_ij = H h_ij`
so `T_K = K_ij K^ij - K^2 = 3H^2 - 9H^2 = -6H^2`, `Q_K = 0`, `A_K = <N Q_K>_h = 0`,
`V_a = 0` (`a = DZ = DU = 0`), gate inactive (`f = G'(Y_h) = 0`, `Y_h = -theta < 0`).
Inserting: `(M_P^2/2)(6 H^2 - 2 Lambda) = rho_b + rho_d`, i.e.

```
3 M_P^2 H^2 = M_P^2 Lambda + rho_b + rho_d          (Friedmann constraint, exact on branch)
```

- The **coefficient multiplying homogeneous energy** on the right is `1`; in the
  H^2 form, `H^2 = Lambda/3 + (8 pi G_cosm/3) (rho_b + rho_d)` with
  `G_cosm := (8 pi M_P^2)^(-1) = G_bare` — the standard Einstein coefficient
  `8 pi G/3`, now with the *bare* constant. Checked symbolically (C1–C1d,
  residuals 0).

Every factor and sign: `T_K = -6H^2` (sign from `K_ij K^ij - K^2` with
`K_ij = H h_ij`, `K = 3H`); lapse prefactor `(M_P^2/2)`; the `-2 Lambda` inside
moves with `M_P^2` to the right as `M_P^2 Lambda`.

## 3. Step 2 — local normalization supplied by the compensated host (trace)

Section 5 of FINAL_ACTION: the compensated gate makes the base quadratic
density (units `M_P^2/2`) equal to `-2 c_N |D(Phi-Z)|^2 - 4 c_N DZ.DU`; the
locally measured high-k Newton constant is

```
G_N = G_bare / c_N ,   c_N = 1 - alpha/2        (derived; FINAL_ACTION sec. 5, eq. (18))
```

This matching derivation exists and is recorded upstream: `results/AS226/`
(`G_N = G_bare/c_N`, `4 pi G_N = 1/(2 M_P^2 c_N)`, negative control firing with
residual `(1+c_N)(rho_b+rho_d)`), sibling `results/AS236/` (homogeneous centered
clock: same ratio from the Friedmann sector, uncentered-variant control
fires). This seed does **not** re-derive it; it records the normalization and
**carries the ratio** — the task's stated alternative to guessing an absent
matching derivation is satisfied because the derivation exists on the same
pinned action. Symbolic trace: C2–C2b residuals 0.

## 4. Step 3 — H^2 and the vacuum-scale relation in G_N and the ratio; conversion into rho_Lambda

The framework scale relation is operational — it runs on the **measured**
constant:

```
rho_Lambda = 4 a0^2 / (G_N c^2)          [kg m^-3]      (a0 = (c/2) sqrt(G_N rho_Lambda))
```

The Friedmann sector runs on the **cosmological** coefficient `G_cosm`.
Propagating the ratio (each step an identity, all residuals 0, C3–C3e):

```
Lambda_eff  = 8 pi G_cosm rho_Lambda/c^2 = 8 pi (c_N G_N) [4 a0^2/(G_N c^2)]/c^2
            = 32 pi c_N a0^2 / c^4                          [m^-2]
H_vac^2     = Lambda_eff / 3 = (32 pi/3) c_N a0^2 / c^4     [s^-2]
rho_Lambda  = 4 c_N a0^2 / (G_cosm c^2)                     [kg m^-3]
3 H^2       = Lambda + 8 pi G_cosm (rho_b + rho_d)
            = Lambda + 8 pi c_N G_N (rho_b + rho_d)         [s^-2]   (full matter sector)
```

Naive same-G comparison (`G_cosm = G_N` silently):

```
Lambda_naive = 32 pi a0^2 / c^4 ,   Lambda_eff = c_N Lambda_naive ,
Lambda_naive - Lambda_eff = (alpha/2) Lambda_naive
```

Because `c_N = 1 - alpha/2 in (0,1)`, the correct cosmological vacuum curvature
lies **below** the naive same-G value at every `alpha in (0,2)`; at `alpha = 1/2`
it is already `3/4` of it, at `alpha = 1` half of it. The framework-contract
mandate `Lambda_eff = 32 pi (G_E/G_N) a0^2/c^4` is enforced verbatim with
`G_E = G_cosm`.

## 5. Step 4 — the relation, its assumptions, and the single downstream calculation

**Relation (the seed's principal object):**

```
G_cosm / G_N = c_N = 1 - alpha/2 ,    0 < alpha < 2 ,    G_cosm = G_bare = (8 pi M_P^2)^(-1)
```

with the dictionary of Sec. 4 as its forced translation into the a0-vacuum
sector. Every assumption used (none invented):

1. CA5-GNC-R common action, FINAL_ACTION.md eq. (4)/(13)/(18), pinned hash
   b8c04d4e…; homogeneous inactive branch (flat k=0 slices, `Q_K=A_K=0`,
   carrier/gate homogeneous, `z=0`);
2. local high-k normalization `G_N = G_bare/c_N` from the same action (AS226);
3. `c_N` shared between sectors (same `alpha`, same action — no branch
   translation; the shared parameter cell is the same-theory discipline);
4. `kappa = 1/2` adopted (seed input); `alpha in (0,2)` free parameter;
5. vacuum mass density enters the Friedmann sector with the cosmological
   coefficient `G_cosm` and the a0-scale relation with the operational `G_N`.

**Single downstream calculation enabled:** the vacuum-curvature mapping of any
a0-footing to the cosmological sector without mismatched couplings — every
future homogeneous-scale statement derived from `rho_Lambda` (e.g. the de
Sitter attractor of HOMOGENEOUS_FRW's `H_min = sqrt(V0/(3 M_P^2))` scale, or an
a0-calibrated `Lambda`) must use `Lambda_eff = 32 pi c_N a0^2/c^4`, not the
same-G `32 pi a0^2/c^4`. **Blocks:** any inconsistent cosmological calibration
that silently identifies `G_cosm` and `G_N`. This is a normalized dictionary
for the common-action closure witness of this seed; it does not close the
thirteen requirements.

## 6. Controls (both capable of failing; both exercised)

**Control A — alpha → 0 recovers the Einstein normalization.**
At `alpha = 0`: `c_N = 1`, `G_N = G_bare`, `Lambda_eff = Lambda_naive =
32 pi a0^2/c^4`, and H^2 carries the standard coefficient `8 pi G_bare/3` with
the standard lapse prefactor `1/(16 pi G_bare)`. Symbolic A1–A4 residuals 0;
numeric A1 both footings PASS.

**Control B — negative control: set G_cosm = G_N prematurely.**
`G_cosm = G_N` forces `c_N = 1`, i.e. `alpha = 0` against the open domain
`(0,2)` — the premature identification is *equivalent to deleting the whole
alpha-sector of the compensated gate*: in the lapse density (units `M_P^2/2`),
`-4 c_N DZ.DU -> -4 DZ.DU` removes `+2 alpha DZ.DU`; `alpha |a-DZ|^2 -> 0`;
`c_N[G(Y_h) - ell Delta_h W_b] -> [G - ell Delta_h W_b]` removes
`-(alpha/2)[G - ell Delta_h W_b]`. In the dictionary it removes the factor
`c_N` from `Lambda_eff`: residual `Lambda_naive - Lambda_eff =
(alpha/2) Lambda_naive != 0` for `alpha in (0,2)`.
Symbolic B1–B4 residual 0; numeric N6 on both footings: `residual = 1 - c_N =
0.150000 != 0` at `alpha = 0.3` (fires; capacity to fail confirmed by the
`alpha = 0` limit closing the same residual to zero).

## 7. Numerics (bounded prototype)

Bounds actually enforced: `ulimit -t 120` CPU on each lane; thread caps
`OMP/OPENBLAS/MKL/VECLIB/NUMEXPR = 1`; `/usr/bin/time -l` RSS.
Observed: derive 0.22 s real, 55 MB RSS; numeric 0.01 s real, 12 MB RSS.
(<< 120 s, << 512 MB, 1 thread.)

| quantity (alpha = 0.3, c_N = 0.85) | canonical a0 | alternative a0 |
|---|---:|---:|
| rho_Lambda [kg m^-3] | 5.844412e-27 | 8.483090e-27 |
| Lambda_eff [m^-2] | 9.271798e-53 | 1.345790e-52 |
| Lambda_naive [m^-2] | 1.090800e-52 | 1.583282e-52 |
| H_vac = c sqrt(Lambda_eff/3) [s^-1] | 1.666641e-18 | 2.007930e-18 |
| r_dS = sqrt(3/Lambda_eff) [Gpc] | 5.8295 | 4.8386 |
| Lambda_eff/Lambda_naive | 0.8500000000 (= c_N) | 0.8500000000 |
| kappa back-check | 0.500000000 | 0.500000000 |

alpha-sweep (canonical footing): `c_N in {0.9750, 0.9500, 0.9000, 0.8500,
0.7500, 0.5000, 0.2500}` at `alpha in {0.05, 0.1, 0.2, 0.3, 0.5, 1.0, 1.5}`;
`Lambda_eff` drops monotonically from 1.063530e-52 to 2.726999e-53 m^-2; `H_vac`
from 1.784986e-18 to 9.038630e-19 s^-1 (`r_dS` from 5.4430 to 10.7490 Gpc);
naive-over-correct factor `1/c_N` from 1.0256 to 4.0000. SI check
(alpha = 0.3): `G_cosm = G_bare = c_N G_N = 5.673155e-11`,
`G_cosm/G_N = 0.8500000000`.

Numerical coincidence noted, **not claimed**: at `c_N = 1` the a0-vacuum Hubble
scale is `c sqrt(Lambda_naive/3) = sqrt(32 pi/3) a0/c = 1.808e-18 s^-1`, within
~20% of the measured `H0 ~ 2.2e-18 s^-1` — the familiar a0–H0 coincidence,
which this dictionary converts into the explicit `Lambda_eff` mapping; it is
not a prediction of H0 (V0 and Lambda are free inputs of the action), and the
dictionary's job is exactly to attach the `c_N` factor when such a comparison
is attempted.

## 8. Lean 4 certificate

`AS252_vacuum_dictionary.lean` — 7 theorems, all real arithmetic:
1. `lambda_eff_of_rho_Lambda` — `Lambda_eff = 32 pi c_N a0^2/c^4` from
   `rho_Lambda = 4 a0^2/(G_N c^2)`, `G_cosm = c_N G_N`, `Lambda_eff = 8 pi G_cosm rho_Lambda/c^2`;
2. `h_vac_square` — `H_vac^2 = (32 pi/3) c_N a0^2/c^4`;
3. `rho_lambda_in_gcosm` — `4 a0^2/(G_N c^2) = 4 c_N a0^2/(G_cosm c^2)`;
4. `coeff_of_rho_in_H2` — Einstein coefficient extraction `8 pi G_bare/3`
   from `3 M_P^2 H^2 = M_P^2 Lambda + rho`;
5. `negative_control_mismatch` — `Lambda_naive - Lambda_eff = (alpha/2) Lambda_naive`;
6. `negative_control_fires` — `Lambda_naive != Lambda_eff` for `alpha != 0`, `a0 != 0`;
7. `alpha_zero_recovers` — `Lambda_eff = Lambda_naive` at `alpha = 0`.

Verified: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>` —
exit 0, zero errors, zero `sorry`, and `#print axioms` on all seven theorems is
exactly `[propext, Classical.choice, Quot.sound]` (house bar met). Compile host
used read-only; no files written into `fable_independent_2026/lean_2026`.

## 9. Domain, limitations, and next steps

**Domain:** homogeneous inactive branch of the pinned action; `alpha in (0,2)`;
both a0 footings; exact symbolic identities over positive symbol parameters,
plus the finite numeric sweep above. **Exclusions:** no gate-active or
inhomogeneous sectors, no RAR/MU2/EXP/MONO passes, no PPN, no k-dependence
(upstream AS226/AS142), no H0/Omega calibrations.

**Limitations:** does not derive `alpha` (the ratio is a one-parameter family);
`kappa = 1/2` remains adopted (AS138.C01's continuum `kappa(r) =
sqrt(2/(r+2b))` does not pin it — a matching condition on `r`, not a
derivation of kappa); the local→homogeneous transfer rests on the shared
`c_N` (`alpha` cell); the H0 proximity is a noted coincidence, not a
prediction; the numerics are a bounded dictionary prototype, exactness rests on
the symbolic lane and the Lean certificates.

**next_unresolved_implication:** the value of `alpha` (= `c_N`): the dictionary
`Lambda_eff = 32 pi c_N a0^2/c^4` and the Friedmann sector fix `G_cosm` only
through the ratio; the first missing bridge is an independent same-action
observable pinning `c_N in (0,1)` (vacuum DOF count of AS658, or the deep
flatness sector `v_flat^4 = G_N M_b a0` at measured `(a0, G_N)`, or the
AS138.C01 four-form continuum point `r* = 8 - 2b` evaluated at `kappa = 1/2`).

**suggested_followup (child specs recorded in result.json):**
- AS252.C01: contract the dictionary with the AS138.C01 conservation
  continuum: at `kappa = 1/2` the four-form datum is `r* = 8 - 2b`; target:
  verify `Lambda_eff = 32 pi c_N a0^2/c^4` holds at the continuum point
  `r*(kappa = 1/2)` and that every other continuum point fires the dictionary
  mismatch — a same-action consistency statement linking the vacuum density to
  the four-form coefficient.
- AS252.C02: conditional deep-equilibrium transfer: `r_M = sqrt(G_N M_b/a0)`
  and `v_flat^4 = G_N M_b a0` re-expressed via `rho_Lambda(G_N)` on both
  footings; negative control: replacing `G_N` by `G_bare` in the a0-relations
  rescales `rho_Lambda` by `1/c_N` (fires for `alpha > 0`).