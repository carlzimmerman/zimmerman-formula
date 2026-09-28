# AS232 — Derive β from the second-order static weak-field equation

**Run:** `AS232-r1-20260928T194100Z-dsv4f-hermes`
**Worker:** deepseek-v4-flash-0731 (OpenRouter; Hermes subagent)
**Seed hash:** `23e5f6b2b8fe75dfa4acd651e16e38128e58228fd935d18d606b5db995658c0c` (verified at start and at write time)
**Branch:** CA5-GNC-R physical-metric branch. Q, RAR, MU2, EXP, MONO treated as distinct; only this branch is used for conclusions (criterion B / filtered MONO target unrelated to this derivation step).
**Status:** supports a scoped claim (β = 1 in the window-vacuum; α-deformation in the spatial shell). Not gravity closure.

---

## 1. Pinned conventions and gauge

- Action: `real_research/common_action_2026_09_26/action/FINAL_ACTION.md`, sha256
  `b8c04d4e365f1c8e1c2ec3bf8d14629618d1ac162e97e3fdf809382fb147546e` (matches manifest).
- Amendment target: `qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md`, sha256
  `98d9149fcebb3a15a1d01b0142587b7d346b3471b007b52457b17a3bcb5d8e3f` (matches manifest).
- Declared PPN coordinate convention (this derivation, natural units c = 1 in the algebra):

  ```
  g00 = -e^{2 Phi},   g_ij = (1 - 2 Psi) delta_ij,   Phi = ln N,  a = D0(Phi)
  g00 = -1 + 2 U_N - 2 beta U_N^2        (target, order c^-4)
  ```

- First order (AS226 conventions, machine-verified gate G1 below):
  `Phi_1 = Psi_1 = -U_N` (lapse from AS226 geodesic equation E1; spatial no-slip shell).
  Point source `U_N = G_N M / r = sqrt(GM2)/r`, `GM2 := (G_N M)^2`; mean-normalized
  nonzero modes; homogeneous/k=0 and the `-2 Λ·hat(Phi)(k)` source projected out (AS226 C6);
  `G_N`, `G_bare`, `G_cosmo` kept separate; `c_N := G_bare/G_N` (AS226 convention).
- Second order: `Phi = -U_N + phi_2`, `Psi = -U_N + psi_2`, ansatz
  `phi_2 = A·U_N^2`, `psi_2 = B·U_N^2` (so `A = phi_2/U_N^2`, `B = psi_2/U_N^2`).
- Window (this seed's domain): inactive gate `G(Y_h) = 0`, dust `rho_d = 0`,
  heat suppression `S_k -> 0` ⇒ tie `Z = (ell S_k/4) Phi -> 0`, `Uaux = Phi - Z -> Phi`.
- Framework inputs (adopted, not derived here): `a0 = kappa·c·sqrt(G·rho_Lambda)`,
  `kappa = 1/2`. Both footings carried below; the result is dimensionless, so both footings
  apply unchanged.

## 2. The static scalar equation of the branch (window-vacuum)

For the static warped ansatz the exact 4D Ricci scalar is (verified, Gate G2):

```
w   = ln(1 - 2 Psi)/2
R3  = -4 e^{-2w} L0(w) - 2 e^{-2w} (D0 w)^2
Rbar = R3 - 2 e^{-2w}[ L0(Phi) + (D0 Phi)^2 + (D0 Phi)(D0 w) ]
Dens = e^{Phi} (1 - 2 Psi)^{3/2} (Rbar + V_a)
Va   = alpha e^{-2w} (D0 Phi)^2                    (window limit of the lapse kinetic)
E1   = 4 c_N L0(Phi_1 - Z_1)                       (AS226 lapse equation, epsilon^1)
```

Gate G1 (linear): the epsilon-order lapse EL of `Dens` equals `E1` identically in the
window-vacuum: residual `0` (all runs). The linear spatial EL is the shell identity
`Psi_1 = Phi_1`, residual `0`.

Gate G2 (curvature slot): `Rbar` evaluated on the exact Schwarzschild-isotropic vacuum
`Phi_S = ln((1-GM/(2r))/(1+GM/(2r)))`, `w_S = 2 ln(1+GM/(2r))` is **exactly 0**
(`vacuum_gate.out`: `GATE-A Rbar = 0`). The unique static spherically symmetric vacuum of
the branch at α = 0 is therefore the Einstein isotropic one, and

```
Phi_S = ln((1-x)/(1+x)) = -2(x + x^3/3 + ...),  x = GM/(2r) = U_N/2
      = -U_N - U_N^3/12 - ...      (no U_N^2 term)
```

i.e. `phi_2 = 0` at α = 0. With the gauge identity (Lean-certified, §4)

```
beta = 1 + phi_2/U_N^2
```

this gives **β = 1 exactly at α = 0** (Einstein limit, gate G3 passes: `A0 = 0`, and the
shell `B0 = -3/4` from the exact `-3 U_N^2/4` term of the isotropic shell).

## 3. Second-order content and the α-deformation

On-shell ε² quadratics of `Dens` at the point mass (machine-verified, `final6.out`,
`vacuum_gate.out`):

```
[Dens]_eps^2 |_{point, window}  =  GM2 (6 + alpha) / r^4          (leading 1/r^4 harmonic)
```

Interpreting the branch's "same equations" prolongation (lapse slot `4 c_N L0(phi_2 - z_2)`
with `z_2 -> 0` in the window is homogeneous; the shell slot `4 L0(psi_2 - phi_2)` carries
the on-shell source family), the ε² system on the point class reads

```
lapse:   4 c_N L0(phi_2) = 0         =>  phi_2 = 0   (L0(phi_2) = 2 A GM2/r^4 != 0 for A != 0)
shell:   4 L0(psi_2 - phi_2) = -(6+alpha) U_N'^2     =>  B = -(6+alpha)/8,  A = 0
```

The coefficient used in the lapse slot, `L0(1/r^2) = 2/r^4`, is Lean-certified (§4).
Consequences:

- **β = 1 + phi_2/U_N^2 = 1 identically in the window-vacuum** (φ₂ = 0; A = 0).
- The α-deformation is **not** in the lapse: it lands in the spatial shell
  `psi_2/U_N^2 = B = -(6+α)/8`. At α = 0: `B = -3/4`, the exact Einstein isotropic shell
  (gate G3 passes).
- Consistent with the exact-vacuum gate: at α = 0 the source family is `6 GM2/r^4` and the
  unique vacuum is Schwarzschild-isotropic.

## 4. Negative control (capable of failing) — machine-verified

Seed requirement: *set β = 1 as an input and require the second-order Euler residual to
remain an independent test.* Executed: inject the β = 1 input + Einstein isotropic shell
(`phi_2 = 0`, `psi_2 = -3/4 U_N^2`) into the α-branch density and evaluate the residual.
`vacuum_gate.out`:

```
GATE-B residual = Va(Schwarzschild isotropic)
                = 256 alpha GM2 r^4 / ((sqrt(GM2) - 2 r)^2 (sqrt(GM2) + 2 r)^6)
GATE-B at alpha = 0: 0
```

- α ≠ 0: residual ≠ 0 — the Einstein shell **fails** the α-branch (control fires, with an
  actual nonzero symbolic residual, not a boolean).
- α = 0: residual = 0 — the Einstein shell is the solution (control dies).

The control is independent of the β-derivation: it evaluates the branch density at the
injected shell; it is capable of failing (it does, for every α ≠ 0).

## 5. Consistency check between footings (dimensionless result)

Framework: `a0 = kappa c sqrt(G rho_Lambda)`, `rho_Lambda = 4 a0^2/(G c^2)` with
`G = 6.67430e-11`, `c = 299792458`:

| footing | a0 (m/s²) | rho_Lambda (kg/m³) | implied kappa |
|---|---|---|---|
| canonical | 9.3619e-11 | 5.844412e-27 | 0.500000 |
| alternative | 1.1279e-10 | 8.483090e-27 | 0.500000 |

Both footings are the adopted-kappa = 1/2 normalization with the corresponding density
(they are not simultaneously fixed density and fixed kappa). The claim β = 1 (+ spatial
shell shift `-(6+α)/8`) is dimensionless and holds on both footings unchanged.

## 6. Lean certificate

`AS232_beta_gauge.lean` — verified with `lake env lean` (exit 0), zero `sorry`, axioms
exactly `{propext, Classical.choice, Quot.sound}` (`AS232_axioms_full.lean` output):
- `as232_gauge_beta`: `beta = 1 + phi2/U_N^2`, `U_N != 0`
  ⇒ `-(1 - 2U + 2U^2 + 2 phi2) = -1 + 2U - 2 beta U^2` (truncated −e^{2Φ} bookkeeping).
- `as232_l0_point_harmonic`: flat-Laplacian harmonic weight `6/r^4 - 4/r^4 = 2/r^4` for the
  `A/r^2` ansatz (given the derivative values of `1/r^2`).
- `as232_einstein_shell_limit`: `-(6+α)/8 = -3/4 - α/8` (shell gate at α = 0).

## 7. Gates summary (all machine-verified, residuals recorded in run outputs)

| Gate | Condition | Result |
|---|---|---|
| G1 | linear lapse EL == AS226 E1 (window-vacuum) | residual 0 (final7/8/9) |
| G1s | linear spatial EL == shell identity Ψ₁ = Φ₁ | residual 0 (final7/8/9) |
| G2 | Rbar ≡ 0 on Schwarzschild-isotropic vacuum | exact 0 (vacuum_gate.out) |
| G3 | α = 0 ⇒ A = 0 (β = 1), B = −3/4 | passed (exact shell term; G2 + B0) |
| G4 | negative control: β=1 + Einstein shell in α-branch | residual 256α·GM2·r⁴/((√GM2−2r)²(√GM2+2r)⁶): fires α≠0, dies α=0 |
| G5 | on-shell ε² source family | GM2(6+α)/r⁴ (final6.out, vacuum_gate.out) |

## 8. Limitations and unresolved implication

- The automated symbolic **functional variation** of `Dens` at ε² collapsed to 0 ≡ 0 on the
  point ansatz in the exact-EL/probe machinery (final8/final9; sympy fragility on the
  `e^{Phi}√h` composition — documented in `failed_attempts`). The β = 1 statement therefore
  rests on the exact-vacuum gate G2 + gauge identity + linear gates + G5, and on the
  consistent shell slot reading, rather than on an independently solved symbolic 2×2 at ε².
- No finite-domain / boundary completion (AS143-style) was executed; boundary terms of the
  ε² system are the declared unfinished business.
- No matter sector entered (dust-free window; AS137/AS151 used only as conventions).
- Does **not** establish α-dependence of β at order beyond c⁻⁴, nor tensor/light-deflection
  sector (γ) — distinct seeds.

**next_unresolved_implication:** the finite-domain (r ∈ [r₀, R]) ε² boundary completion of
the same Euler system for (φ₂, ψ₂) on the α-branch — the first missing bridge that would
certify directly that no α-dependence re-enters φ₂ at c⁻⁴ order and fix the shell
coefficient `-(6+α)/8` as the boundary-fixed value.

**suggested followup:** AS232.C01 — finite-domain static Galerkin/ODE on the ε² system with
boundary-compatible adjoints (AS143 measure), verifying β(α) continuity at α → 0 and the
shell coefficient −(6+α)/8 numerically-readable; distinct from this seed.

## 9. Execution evidence files

`as232_final6.py/.out` (G5), `as232_final7.py/.out` (linear gates; hand-IBP ε² rejected),
`as232_final8.py/.out`, `as232_final9.py/.out` (exact-EL collapse, documented),
`as232_vacuum_gate.py/.out` (G2, G4, G5), `AS232_beta_gauge.lean`,
`AS232_axioms_full.lean`, `lean_check.out`, `lean_axioms.out`, plus intermediate attempts
(`as232_derive.py` v9, `as232_final.py`, `as232_final2/3/4/5.py`, `as232_verify.py`,
`as232_galerkin*.py`) and their outputs. All files in this run directory.
