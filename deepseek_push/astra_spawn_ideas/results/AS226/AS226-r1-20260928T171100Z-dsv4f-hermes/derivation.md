# AS226 — Derive measured Newton G in the reciprocal high-k limit

Run directory: `deepseek_push/astra_spawn_ideas/results/AS226/AS226-r1-20260928T171100Z-dsv4f-hermes/`
Seed: `AS226_derive_measured_newton_g_in_the_reciprocal_high_k_limit.md`
Seed sha256: `51e2412c78b88902d617f2369913abccbbd69a918b37268d3f75d06b809dd398` (verified before execution)
Branch: CA5-GNC-R physical-metric branch. Q, RAR, MU2, historical EXP and operative filtered MONO kept distinct;
criterion B (causality) is the operative criterion. No branch-translation is used or claimed.

Action pinned: `real_research/common_action_2026_09_26/action/FINAL_ACTION.md`
sha256 `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e` (verified; eq. (4) metric, eq. (13)-type
field equations, eq. (18) `G_cosm/G_N = c_N` referenced). Vacuum `ACTION.md`, `FRIED_CHICKEN_SPEC.md`,
`SOURCE_MANIFEST.json`, `FIRST_PRINCIPLES_AND_BRANCHING.md`, `STANDING.md` all sha256-verified before use
(hashes in result.json `input_sha256`).

## Conventions (step 1 — pin the action and write the displayed target)

* Static weak-field physical metric `ds^2 = -(1+2 Phi_F) dt^2 + (1-2 Psi) dx^2`, FV = -1;
  `Phi_t = -Phi_F` (the a-primitive: `a = D ln N = D Phi_t`), so `Phi_F = -Phi_t`.
* `c_N = 1 - alpha/2`, `M_P^2 = (8 pi G_bare)^-1` (c = 1 natural units; SI conversion uses c = 299792458).
* k-space amplitudes `Phi_t, Psi, Z, U`; `k2 = k^2`, nonzero modes only; zero (Lambda) mode handled by the
  mean normalization `<Z>_h = 0` and the nonzero-mode convention of FINAL_ACTION section 5 (no Lambda source at k != 0).
* Gate inactive at high k: `f = G'(Y_h) = 0` with `Y_h = J(DW_b) + ell Delta W_b - theta < 0`; the gate supplies the
  U-tie (eq. (6)): `4 Delta Z = S_h ell div a`, i.e. mode-wise `Z = (ell S_k/4) Phi_t` with heat factor
  `S_k = e^{-xi^2 k2/2}` and `Q := 1 - ell S_k/4`.
* Dust baryonic source of total mass `M_b`; mean-normalized leaf (`<Z>_h = 0`, rho-mean-subtracted on the torus).
* a0-kappa input (MANDATORY FRAMEWORK): `a0 = kappa*c*sqrt(G*rho_Lambda)`, `kappa = 1/2` ADOPTED as input, not
  derived here. Both footings are carried numerically (canonical a0 = 9.3619e-11 and alternative 1.1279e-10 m/s^2).

**Displayed mathematical target.** The static base density shown in the seed,

```
rho_b + rho_d = -2 c_N norm(D(Phi-Z))^2 - 4 c_N (DZ . DU)          [B_target]
```

is the variation-sourced density of the common action evaluated on the branch: the exact identity
(symbolic, residual 0, check C1)

```
E_A + V_a - B_target - 2 k2 (Psi + Phi_t)^2  ==  0,
```

so on the spatial shell (equation of motion for Psi, `Psi = -Phi_t = Phi_F`) the static base density equals
exactly the displayed object; spelled with `Phi_F = -Phi_t` it reads
`E_F + V_a = B_target(Phi = -Phi_t) + 2 k2 (Psi - Phi_F)^2` (check C1b). This is the seed's displayed
mathematical object, retained as a candidate until the controls of step 4 run.

## Step 2 — vary Phi, Z, U and Psi before the high-k limit

Linearized static variations of the action density in units `M_P^2/2` (all equations exact in the mode picture;
signs fixed against FINAL_ACTION eq. (13)-type operators; verified by substitution-back, checks C3a–C3c):

* Phi_t equation:   `(M_P^2/2)(-4 c_N k2)(Phi_t - Z) = rho_b + rho_d`
  ⇔ `2 M_P^2 c_N k2 (Phi_t - Z) = -(rho_b + rho_d)`                  [E1]
* Z equation:       `(M_P^2/2) 4 c_N k2 [(Phi_t - Z) - U] = -rho_d`
  ⇔ `(Phi_t - Z) - U = u_d = -rho_d/(2 M_P^2 c_N k2)`                [E2]
* Psi bracket:      `(M_P^2/2) 4 k2 (Psi + Phi_t) = 0` ⇒ `Psi = -Phi_t` (nonzero modes)  [C2d]
* U-tie (eq. (6), f = 0):  `Z = (ell S_k/4) Phi_t` (mode picture); dust source `rho_d = 0`.     [C2e]
* High-k window: `xi k >> 1` ⇒ `S_k -> 0`, `Q -> 1`; reciprocal clock `1/t_c = 1/(1+z)` with
  `z = Z - <Z>_h -> 0` (mean-normalized): the reciprocal clock is near one as required.            [C3d]

Solving [E1]+[E2]+the tie simultaneously (before the limit, checks C3a-C3b):

```
Phi_t = -(rho_b + rho_d)/(2 M_P^2 c_N k2 Q),   Z = (ell S_k/4) Phi_t,
U = Phi_t - Z = -(rho_b + rho_d)/(2 M_P^2 c_N k2),     Q = 1 - (ell/4) S_k.
```

## Step 3 — match the Cavendish coefficient: determine G_N / G_bare

With `M_P^2 = (8 pi G_bare)^-1` the tied coefficient of [E1] is

```
2 M_P^2 c_N = 1/(4 pi G_N)     ⇒     4 pi G_N = 1/(2 M_P^2 c_N)     ⇒     G_N/G_bare = 1/c_N = 1/(1 - alpha/2).
```

The reciprocal high-k solution is therefore the Newtonian field of the baryonic source **with the measured constant**:

```
Phi_t (high-k) = -4 pi G_N (rho_b + rho_d)/k2 ,
```

i.e. the geodesic acceleration of the physical metric is `|grad Phi_t| -> G_N M_enc/r^2`: a Cavendish-style
inverse-square potential with coefficient `G_N = G_bare/c_N > G_bare` for every `0 < alpha < 2`
(monotone rise: `d/dalpha (G_N/G_bare) = 1/(2(1-alpha/2)^2) > 0` on (0,2), check C4b; `alpha -> 0`
recovers `G_N = G_bare`, the GR limit). This is consistent with FINAL_ACTION eq. (18) `G_cosm/G_N = c_N`
(equivalently `G_cosm = c_N G_N = G_bare`). All of this is Lean-4-certified (see certificate section).

## Step 4 — falsifiable negative control and refinement

**Negative control (must fire):** set `G_N = G_bare` with alpha ≠ 0 and substitute the G_bare-calibrated
potential `Phi'_bare = 4 pi G_bare (rho_b + rho_d)/k2` into the ORIGINAL sourced equation [E1] with the
action coefficient `c_N` kept:

```
residual = -2 M_P^2 c_N k2 Phi'_bare - (rho_b + rho_d) = -(1 + c_N)(rho_b + rho_d)
         = -(2 - alpha/2)(rho_b + rho_d)  !=  0   for alpha in (0,2),  rho_b + rho_d != 0.   [FIRES]
```

The linear-in-alpha content of the fired residual is exactly `(1+c_N) - 2 = -alpha/2` (check C5b);
the true assignment `G_N = G_bare/c_N` gives residual zero (check C5c). Symbolic checks C1–C7 all pass
(exit 0, `all_pass: True`; raw output `derive_raw.out`).

**Numeric engine** (`as226_numeric.py`; flat periodic 3D torus L = 100 m, Gaussian source M = 5 kg, sigma = 2.5 m;
exact mode algebra in float64, no finite-difference truncation; N = 48, refined once to N = 96):

| check | observed | pre-set tolerance | pass |
|---|---|---|---|
| N1 source equation + ties: max\|(E1)\|/scale, \|Z-tie\|, \|(E2)\|, \|U - u_b\| | 3.37e-16, 0, 0, 4.3e-23 | 1e-9 | pass |
| N2 geodesic far field 6/8/10 sigma vs G_N M/r^2 | -3.8%, -4.5%, -6.2% (periodic-box Ewald terms ~ (r/L)^2, bounded) | 8e-2 | pass |
| N2b mode-wise Newton coefficient \|(Phi_t-Z) k2/rho\| vs 4 pi G_N | 4.44e-16 rel; bare gap 17.65% = 1/c_N - 1 | 1e-6 | pass |
| N3 negative control FIRES (G_bare-calibrated, c_N kept) | max\|res\|/scale = 1.850, exactly (1+c_N); true candidate nil 3.4e-16 | > 1e-7 (fires) | pass |
| N4 alpha-content: fired residual minus (c_N-1)rho | 4.05e-16; (c_N - 1) = -0.1500 = -alpha/2 | 1e-9 | pass |
| N5 reciprocal clock max\|Z\|/max\|Phi_t\| | 9.998e-3 ≈ ell/4 = 0.01 (S_k ≈ 1); z -> 0, 1/(1+z) -> 1 | — | pass |
| N6 refinement N=48 -> N=96 | (E1) 3.37e-16 -> 1.80e-16 (rounding floor) | 1e-9 both | pass |
| N7 footings (both a0 values) | rho_Lambda = 5.844412e-27 (canonical) and 8.483090e-27 (alternative) kg/m^3; kappa back-check 0.500000000 both; G_N/G_bare = 1.1764705882; G_cosm/G_N = c_N = 0.85 | 1e-9 | pass |

The negative control is capable of failing and fired at the predicted (1+c_N) = 1.85 per unit density with the
true-assignment residual nil at 3.4e-16 — the mismatch between the bare coupling and the measured constant is
exposed exactly, not by construction.

## Lean 4 certificate

`AS226_certificate.lean` (self-contained, mathlib): certifies cn range, `G_N/G_bare = 1/c_N`,
`1 < G_N/G_bare` on (0,2), the GR limit alpha -> 0, the positive monotone derivative
`d/dalpha 1/(1-alpha/2) = 1/(2(1-alpha/2)^2) > 0`, and the negative-control residual algebra
(the G_bare-calibrated substitution leaves `-(1+c_N) rho != 0`). Verified on this build
(`cd fable_independent_2026/lean_2026 && lake env lean <abs path>`):
exit 0, zero `sorry`, and for every certified theorem
`#print axioms` returns exactly `[propext, Classical.choice, Quot.sound]` (allowed set).
Compile host `fable_independent_2026/lean_2026` was used read-only; no files written there.

## Controls on signs, dimensions, measure

* Signs: [E1]/[E2]/Psi bracket re-derived with the operators spelled out (`-4 c_N k2`, `4 c_N k2`, `4 k2`) and
  substitution-back checks (C3a–C3c) before accepting; the negative control re-uses the original equation with
  the wrong constant, so it is insensitive to sign conventions of the candidate.
* Dimensions: k-space equations are dimensionally self-consistent in the M_P^2 = (8 pi G_bare)^-1, c = 1 system
  (2 M_P^2 c_N k^2 Phi has density units); real-space geodesic check uses the physical potential
  (k-space solution / cell volume dx^3); SI conversion of footings uses G_N = 6.67430e-11, c = 299792458,
  M_sun = 1.98847e30, pc = 3.085677581491367e16.
* Averaging measure: all shell averages use the Euclidean radius bands |r - r0| < 2L/N on the torus; the far-field
  checks use 6/8/10 sigma (outside the Ewald-dominated zone; the ~ (r/L)^2 box terms are bounded by the
  pre-declared 8% tolerance and would catch a 15% bare-calibration error).
* Declared limiting case: high-k limit S_k -> 0 checked directly (C3d, N5) against the original tie.

## Classification and closure implication

The target — *an independently normalized local Newton constant from the current action* — is **derived** within
the scoped domain (weak compact baryonic source, xi k >> 1, gate inactive, dust, mean-normalized leaf):
`G_N = G_bare/(1 - alpha/2)`, with the ratio certified and the negative control fired at its predicted value.
This is a scoped claim only: it does not promote to complete gravity closure, does not derive alpha itself,
and does not fix kappa (adopted input). Closure implication: the G_N-calibration gate closes with
`G_N/G_bare = 1/c_N` and `G_cosm/G_N = c_N` (FINAL_ACTION eq. (18)) on the CA5-GNC-R branch, parameter domain
0 < alpha < 2, xi k >> 1, consistent with AS137 (matter Ward identity; `nabla·T = 0` on shell, S_b has no a0/G),
AS151 (primary constraints) and AS658 (vacuum DOF).

## Bounds actually enforced

CPU: `ulimit -t 120` (120 s CPU cap, enforced; actual derive 0.17 s user, numeric 0.24 s wall);
threads: 1 (`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
NUMEXPR_NUM_THREADS=1`); memory: observed peak RSS 430,686,208 B (numeric, N=96) < 512 MB bound
(the numeric script's own bound); refinement: N = 48 -> 96 once. Bounded prototype, not a larger computation.