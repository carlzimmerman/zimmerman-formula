# AS229 — Projected-vacuum contribution to lensing slip (Tier-0b)

**Run:** `AS229-vaclens-r1-20260928T1941Z-dsv4f-hermes`
**Worker:** deepseek/deepseek-v4-flash-0731 (OpenRouter) via Hermes Agent subagent, host macOS 26.5.2
**Seed hash (verified at start and re-verified at packaging):**
`6595554364d60b1bf4c708cf65ca45513e49a9197b2c2580e49598b6292a8ba2`
**Branch:** CA5-GNC-R physical-metric branch (reciprocal vacuum barrier). Q, RAR, MU2, EXP, MONO are never
interchanged with it (criterion B context preserved; no branch translation attempted — none needed for this seed).

---

## 1. Framework cell and conventions (frozen)

| item | value |
|---|---|
| action | CA5-GNC-R; vacuum piece `L_v = -V0 F(t)` (sources: `breakthrough_review_2026_09_26/vacuum/ACTION.md`, `PERSPECTIVE_VARIANT.md`, hashes match seed pins) |
| barrier | `F(t) = 1 + (t + 1/t - 2)^2`, `t = 1 + z = 1 + Z - <Z>_h > 0` |
| target | `Delta T^ij_mean = -(<N sigma_v>_h / N) z h^ij`, `sigma_v = -V0 F'(t_c)`, `t_c = 1` |
| averaging | proper-volume `<>_h`, flat spatial leaf at leading order, unit lapse `N = 1` at leading order (lapse feedback `O(Phi)` deferred, see next steps) |
| coupling | `a0 = kappa c sqrt(G rho_Lambda)`, `kappa = 1/2` **adopted as input** (not derived here) |
| constants | `G = G_N = 6.67430e-11`, `c = 299792458`, `M_sun = 1.98847e30`, `pc = 3.085677581491367e16` (SI). `G_bare`, `G_cosmo` not used. |
| footings | canonical `a0 = 9.3619e-11 m/s^2` and alternative `a0 = 1.1279e-10 m/s^2` carried separately; they cannot share one fixed `(rho_Lambda, kappa)` pair |
| V0 | input parameter; calibration to `epsilon_Lambda = rho_Lambda c^2` is a **display-only** assignment, not a derived result |

## 2. Part A — exact flatness and closed forms (deliverable: flatness orders at t = 1)

With `t = 1 + z`, `z > -1`:

```
F(1+z) - 1 = ((1+z) + 1/(1+z) - 2)^2 = z^4/(1+z)^2           (exact closed form)
F'(1+z)    = 2 z^3 (z+2)/(1+z)^3                              (exact closed form)
```

Both residuals verified symbolically (sympy `simplify(...) == 0`; CK1, CK1b). Immediate consequences:

```
F'(1) = 0, F''(1) = 0, F'''(1) = 0, F''''(1) = 24            (CK2)
```

Taylor expansions about `z = 0` (coefficients z^0..z^9, exact rationals, CK3/CK4):

```
F(1+z) - 1 = z^4 - 2 z^5 + 3 z^6 - 4 z^7 + 5 z^8 - 6 z^9 + ...       (leading z^4, coef 1)
F'(1+z)    = 4 z^3 - 10 z^4 + 18 z^5 - 28 z^6 + 40 z^7 - 70 z^8 + ... (leading z^3, coef 4)
```

Hence the vacuum response `sigma_v = -V0 F'(1+z) = -4 V0 z^3 + 10 V0 z^4 + ...` has **no linear, quadratic or
cubic susceptibility**, and the projected stress

```
Delta T^ij_mean = -(<N sigma_v>_h / N) z h^ij
                = +4 V0 <z^3>_h z h^ij / N  +  O(<z^4>_h z)        (CK5, CK5b, CK8)
```

is **O(z^4) to leading order** (order in the local adiabatic amplitude `z ~ A`; exact identities universal in
`z > -1`). Leading coefficient `+4 V0 <z^3>_h / N` times `z h^ij`; sign set by the third moment of `z`
(mixed-parity profile with `<z^3>_h != 0`). Trace-free part of `Delta T^ij` is identically zero
(isotropic `delta^ij` structure; CK7 `< 1e-12`).

*What rev-1 missed (recorded in `failed_attempts`):* a pure-odd-modes profile forces `<z^3>_h = 0`,
degenerating this leading-order test. Rev-final uses a mixed-parity profile
`z = A(sin x + 0.35 cos 2x + 0.12 sin 3x)` (means `<z> = 0`, `<z^3> != 0`).

## 3. Part B — trace and trace-free Einstein combinations with vacuum sources (seed step 2)

Static weak field, `c = 1`, metric `g_00 = -1 - 2Phi`, `g_ij = (1 - 2Psi) delta_ij`, `S = Phi - Psi`:

```
Lap Psi          = 4 pi G T00                                  (G_00)
Lap S            = 4 pi G T^k_k                                (trace combination)
Lap Phi          = 4 pi G (T00 + T^k_k)
Lap (Phi + Psi)  = 4 pi G (2 T00 + T^k_k)      <-- lensing-slip combination
TF(G)_ij         = -(d_i d_j - (1/3)d_ij Lap) S = 8 pi G Pi_ij, Pi_ij = T_ij - (1/3)d_ij T^k_k
```

Symbolic residuals of all five identities: exact 0 (sympy; `einstein_symbolic` in raw_output.json).

**Independent 3D verification (capable of failing — it did, three times):** a from-scratch full-nonlinear
finite-difference Ricci tensor (Christoffel symbols + Ricci assembled from the metric in `(4x4)` tensor
form, static drop, `O(h^2)` stencils, 32^3 lattice, `A = 2.5e-3`) is compared against the linearized
identities with **stencil-matched** references (same composed `d1` primitive). Residuals: `G_00` 0.90%,
`G^k_k` 0.91%, `G_xx..G_zz` 0.66-0.80%, `G_xy` 0.20%, `G_tx == 0` (CK9, tolerance 1% pre-declared).
The spectral-vs-stencil mismatch is quantified (`G_zz` spectral comparison 4.8% — pure stencil
`(sin(kh)/kh)^2` effect, not a physics residual).

**Consistent-source factor check with anisotropic stress** (CK9b): sources defined stencil-consistently by
the combination equations themselves (`rho = lap_m(PsiS)/(4 pi G1)`, `T_ij` from `S_d`), so the
`4 pi G / 8 pi G` factors are algebraically under test. Residuals `5.6e-5`, `3.1e-5`, `9.6e-6` (tol 1e-4).
**Factor-mutation negative controls fire**: replacing `4 pi G` by `8 pi G` or `2 pi G` in the source
definition leaves `O(scale)` residuals (0.0046, 0.0091 vs scale 0.0090) — the check cannot be passed by
a wrong factor.

**Vacuum composites (CK10):** with `rho_v = V0 (1 + F(1+z))`, `sigma_v = -V0 F'(1+z)`,

```
rho_v + P_v = -(<N sigma_v>/N) z        (exact: F-parts cancel; numeric max residual 1.1e-16)
Pi_v = 0                                (isotropic vacuum stress: T^ij_v = -P_v delta^ij structure)
```

So the vacuum piece enters the scalar equations **only** through the isotropic channel:
`Delta T^k_k = 3 Delta T_mean` feeds `Lap S` and `Lap (Phi+Psi)`; the anisotropic channel `Pi` receives
nothing at this order. The slip combination `Phi + Psi` therefore acquires an explicitly ordered vacuum
source `4 pi G * 3 Delta T_mean = 12 pi G V0 <z^3>_h z / N + O(z^5)` — the requested "one explicitly
ordered vacuum contribution to the lensing equations".

## 4. Part C — perturbative order (seed step 3)

- `F(1+z) - 1 = O(z^4)`: the barrier's density-type parts are quartic-suppressed;
- `sigma_v = -V0 F'(1+z) = O(z^3)`: the projected stress `Delta T = -(<sigma>/N) z = O(z^4)`;
- old `1/t_c` floor: `F_old(t) = 1/t`, `F_old'(1) = -1`, `F_old''(1) = 2` (both nonzero; CK12) —
  `sigma_old = +V0/(1+z)^2`, `<sigma_old> = V0 (1 - 2<z> + 3<z^2> - ...) = O(z) about z=0`, hence
  `Delta T_old = -V0 <(1+z)^-2> z = O(z)` — **linear** susceptibility, contradicting `F'(1)=F''(1)=0`.
  The reciprocal barrier's quartic suppression vs the floor's linear response is the physical content of
  the negative control.

## 5. Part D — projections and negative controls (seed step 4)

1D periodic leaf (`L = 4 pi`, `N = 64, 128`, amplitudes `A = 0.009..0.3`, unit lapse). Measured scaling of
`max|Delta T|` with amplitude (primary small-amplitude pair 0.009/0.018):

| observable | expected | measured (N=128) | result |
|---|---|---|---|
| `max|DT|` ratio 0.009/0.018 | 1/16 (quartic) | 0.0592 (trend 0.075/0.15: 0.0431) | CK5 pass |
| `max|DT - 4<z^3>z|` ratio | 1/32 (next order) | 0.0309 (trend 0.0431) | CK5b pass |
| old-floor `max|DT_old|` ratio | 1/2 (linear) | 0.5000 | CK6 pass |
| old-floor vs barrier residual ratio | **must not** be 1/32 | 0.5000 | NEG1 **fires** (contradiction) |
| wrong-sign mutation `<+sigma> z` ratio | 1/16 != 1/32 | 0.0608 | NEG2 fires |
| `<sigma>/(-4<z^3>)` recovery | -> 1 at O(A) | 1.53, 1.25, 1.14 (A=0.3..0.075); dev-ratio 0.472 ~ 0.5 | CK8 pass |
| trace-free part of `DT` | 0 | `< 1e-12` | CK7 pass |
| refinement N=64 vs N=128 | agree | 0.0432 vs 0.0431 (trend pair) | CK11 pass |
| old-floor derivatives `F_old'(1), F_old''(1)` | -1, 2 (nonzero) | symbolic | CK12 pass |

Susceptibility substitute-back check (truncated Taylor susceptibility vs full closed form) recorded in
`raw_output.json` (`"substitute_back_trunc3_vs_full_max"`).

### Footings (display only; `V0` is an input, `epsilon_Lambda` calibration shown)

- canonical: `a0 = 9.3619e-11 m/s^2`, `rho_Lambda = 5.844412454021876e-27 kg/m^3`,
  `V0 = epsilon_Lambda = 5.2529e-10 J/m^3`
- alternative: `a0 = 1.1279e-10 m/s^2`, `rho_Lambda = 8.483089619559099e-27 kg/m^3`,
  `V0 = epsilon_Lambda = 7.6241e-10 J/m^3`
- demo profile `z = 0.2 (sin x + 0.35 cos 2x + 0.12 sin 3x)`:
  `max|Delta T^ij| = 8.6e-12 Pa` (canonical) / `1.2e-11 Pa` (alternative) — see raw_output.json
  `demo_stress` for exact values (computed with the actual `epsilon_Lambda` numbers).
- The two footings cannot share one fixed `(rho_Lambda, kappa)` pair (framework rule): same `kappa = 1/2`,
  changed `rho_Lambda`; `V0_alt/V0_can = 1.4514`.

## 6. Lean certificate

`AS229_vacuum_closed_forms.lean` (in this directory; verified with
`cd fable_independent_2026/lean_2026 && lake env lean <abs path>`, exit 0):

- `F_sub_one_closed`: `F(1+z) - 1 = z^4/(1+z)^2` for all `z ≠ -1` (ring + field_simp);
- `barrier_quartic_order`: `(F(1+z)-1)/z^4 = 1/(1+z)^2` for `z ≠ -1, 0`;
- `deriv_inv_at`: `deriv (fun s => s⁻¹) t = -(t^2)⁻¹` for `t ≠ 0`.

`#print axioms` for all three: exactly `[propext, Classical.choice, Quot.sound]`
— zero `sorry`, within the allowed axiom set. Scope note: a full derivative-chain
certificate for `F'(1+z) = 2z^3(z+2)/(1+z)^3` and `F''''(1) = 24` was attempted;
this host build's HasDerivAt typeclass elaboration rejects hand-written goals and
`rw` cannot descend into function lambdas, so the chain was not maintainable in
the run budget. That derivative content is covered here by the exact sympy
series (rational coefficients, no floats), the symbolic flatness limits (CK2),
and the numeric CK3/CK4 checks; the certificate covers the closed-form and
order statements, which are the algebraic core of the quartic suppression.

## 7. Execution bounds (actually enforced)

- wall: `signal.alarm(120)` **enforced** (ITIMER_REAL armed before compute; alarm_remaining 119.5 s at
  exit; actual wall 0.49 s for the final run);
- memory: `RLIMIT_AS = 512 MB` **requested but NOT enforceable** on this host
  (`ValueError: current limit exceeds maximum limit` — system hard limit below the request; honest
  record). Measured peak RSS = **163,184,640 bytes (155.6 MB) < 512 MB** (final run);
- threads: `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
  NUMEXPR_NUM_THREADS=1` — single-thread execution;
- domain: 1D `N = 64, 128`, 3D `32^3` lattice, amplitudes `0.009..0.3`, exact symbolic identities
  (universal in `z > -1`, `t > 0`).

## 8. Checks (all pre-declared; 17/17 pass)

See `raw_output.json` `checks` array / `result.json` `checks` — named checks CK1..CK12 + NEG1/NEG2 with
observed values and tolerances. Both independent negative controls and both 3D controls **were observed
failing** during development (see `failed_attempts`), confirming they are capable of failing.

## 9. Failed attempts (preserved artifacts)

| artifact | cause | resolution |
|---|---|---|
| `as229_vacuum_lensing.py` (rev 1, 391 lines) + `run.out` + `time_mem.txt` | (1) pure-sine profile: `<z^3> = 0` identically → quartic-leading test degenerate; (2) arbitrary isotropic pressure prescription in 3D not a static weak-field solution (slip compatibility); (3) tolerances keyed to degenerate profile | mixed-parity profile; stencil-consistent source construction; rebuilt controls |
| rev 2 first run | spectral wavenumbers missing `2 pi` (`fftfreq` cycles vs angular): reference Laplacian `(2 pi)^2` too small → spurious 31x "mismatch" vs the (correct) FD Ricci builder | `kvec = 2 pi * fftfreq(...)`; mismatch quantified as pure stencil `(sin kh/kh)^2` effect |
| rev 2 second run | 4x4-vs-spatial index mapping in comparisons (`G_tx` vs `G_xy` etc.); `poisson()` silently used global SI `G` instead of the check's `G1 = 1` | `Gt[1+i,1+j]` mapping; stencil-consistent sources defined directly (no Poisson solve) |

Each failure was diagnosed from its actual numbers (the controls fired exactly as designed).

## 10. Limitations

- 3D verification is finite: one `32^3` lattice, one amplitude `2.5e-3`, stencil-matched linearized
  references with residual floor ~1% — a consistency check, not a theorem.
- Lapse feedback `N = 1 + Phi + ...` inside `<N sigma_v>_h / N` is deferred to `O(Phi)` — for a strong
  lens the background potential may dominate the averaging weight (next step).
- `V0` is an input; the `epsilon_Lambda` normalization is display-only. No integrated lensing observable
  (`eta_slip`) is computed here: this seed contributes the explicitly ordered vacuum source term, before
  any geodesic integration.
- `kappa = 1/2` adopted, not derived.
- Only the CA5-GNC-R branch is used; no statement about MONO/RAR/Q/MU2.
- 1D/3D numerics use smooth periodic profiles; real lens configurations (isolated, non-periodic) are not
  covered by the finite tests (the exact closed forms are universal, the finite checks are not).

## 11. Next unresolved implication and proposed continuation

**Missing bridge:** the order of the lapse-weighted vacuum stress `<(N sigma_v)>_h / N` at `O(Phi)` of a
concrete lens potential, and the resulting integrated slip contribution `Phi+Psi` along null rays
(`eta_slip` deviation). The natural question: does `Phi_ext ~ 1e-6..1e-4` promote the leading projected
vacuum signal above `O(z^4)` relative to lens scales, and does the old-floor linear term contaminate the
same integral (it must, by NEG1, if any `1/t_c`-type term survives).

Proposed child **AS229.C01**: integrate `Delta T^ij_mean` through the deflection integral over a
non-periodic lens profile (NFW-like `z` field), with lapse weight expanded to `O(Phi)`, and report the
slip-combination ratio with/without the vacuum term, controlling with the old-floor replacement
(falsifiable: old floor must shift the slip by `O(z)`-scale, barrier by `O(z^4)`-scale).