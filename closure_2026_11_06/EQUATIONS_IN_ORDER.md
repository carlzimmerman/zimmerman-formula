# The equation chain, in order (2026-11-06, lane QX1)

Kappa = 1/2 FITTED; not theory closed. Adopts nothing. Criteria: QX1_equation_chain/FROZEN_CRITERIA.md (0bc8da973b).

Every step carries one tag:
- **LEAN**: a machine-checked theorem. Files are in `fable_independent_2026/lean_2026/`. Check them with
  `lake env lean <file>`; the only axioms are propext, Classical.choice and Quot.sound, and each file has a `_MUTATE` twin.
- **SYMPY**: a symbolic derivation with a committed script.
- **NUM**: a numerical lane result.
- **POSTULATED / FITTED**: a hand input.

"QX1." means `QX1_closure_chain.lean`. Lean certifies only that the premises imply the conclusions. It does not certify
the action, any numerical lane, or any PDE-level statement.

---

## 0. Hand inputs (nothing below derives these)

| Input | Tag | Where |
|---|---|---|
| kappa = 1/2 | FITTED. Proved not derivable from the framework's premises | LEAN `KAPPA_LOGIC_2026_10_20.half_not_derivable`, `every_kappa` |
| J(Y) = Lambda - 2 a^2 [u - ln(1+u)], u = sqrt(Y)/a, a = a0/c^2 | POSTULATED (outside the Blanchet-Skordis admissible class) | V3_FULL_PICTURE section 1 |
| Lstar >= 21.7 / 22.9 pc (canonical / alt), gamma_L = K Lstar^2/2 | POSTULATED, lower bound only (outer globulars) | D10, X3 |
| mu_K, dust abundance (v3s only) | free / initial condition; mu_K = 0 in galaxies | V3_FULL_PICTURE section 1 |
| rho_DE | measured input (framework-native); the clock bound s^2 = phidot^2 <= 2 rho_DE | AC6/AC7 |
| Both footings: a0 = 9.3603e-11 / 1.1312e-10 m/s^2, never pooled | convention | standing rule |

## 1. The action

**v3s** (adopted 11-04, scoped: isolated galaxies, Solar System, galaxy lensing, GWs):

    S = (c^3/16 pi G) Int sqrt(-g) [ R - 2 J(Y) + 2 K(Q) ]  -  (gamma_L/2) Int sqrt(-g) [max(D.P, 0)]^2  +  S_m

Tag: POSTULATED. It is deposited standalone in PAPER68 v1.0 (DOI 10.5281/zenodo.23990944). tau is the khronon,
A its acceleration, Y = A.A/c^4, P an independent spatial covector, and K(Q) = mu_K^2 (Q - 1)^2.

**AC2q** (candidate successor, not adopted; AC7 d063cd6e5f). The dark-energy scalar phi is the clock, so there is
no dust sector and no K(Q). The stiffness is switched on the khronon charge:

    L_stiff = -(gamma/2) { [max(D.P + 2X, 0)]^2 - (2X)^2 },   X = s^2/(2 N^2) (unitary gauge),  s^2 = phidot^2 <= 2 rho_DE

| Step | Statement | Tag |
|---|---|---|
| 1.1 | At X = 0 the AC2q stiffness equals v3s's | LEAN `QX1.ac2q_reduces_to_v3s` |
| 1.2 | On-region (D.P + 2X >= 0): -(gamma/2)(D.P)^2 + T_on, with T_on = -2 gamma X D.P | LEAN `QX1.ac2q_on` |
| 1.3 | Off-region: T_off = +2 gamma X^2 | LEAN `QX1.ac2q_off` |
| 1.4 | The two pieces agree on the switch surface D.P = -2X | LEAN `QX1.ac2q_continuous_at_switch` |
| 1.5 | X >= 0 in unitary gauge | LEAN `QX1.X_nonneg` |

## 2. Field equations

| Step | Statement | Tag |
|---|---|---|
| 2.1 | dJ/du = -2 a^2 u/(1+u) | LEAN `QX1.J_hasDerivAt` |
| 2.2 | J_Y = (dJ/du)/(dY/du) = -1/(1+u), with Y = a^2 u^2 | LEAN `QX1.JY_value` |
| 2.3 | 1 + J_Y = mu(u) = u/(1+u). The khronon term turns GR's div grad Xi into AQUAL's div(mu grad Xi) | LEAN `QX1.one_add_JY_is_mu` |
| 2.4 | Weak-field system: Xi = phi - sigmadot + grad(sigma)^2/2; 4 pi G rho_tau = -[div(J_Y grad Xi) + mu_K^2 Xi]; Poisson for all mass | SYMPY (BS24 PN system; C4 K1, residual 0) |
| 2.5 | Static limit: div[mu(grad psi/a0) grad psi] + mu_K^2 psi = 4 pi G rho_b, with phi = psi | SYMPY (C4 K1; BS24 Eq. 3.21) |
| 2.6 | The khronon weight is fixed: alpha = 1 gives exactly law S; alpha < 1 gives a floor; alpha > 1 is never deep | LEAN `V3_PICTURE_2026_10_23.coupling_one_is_law`, `coupling_floor`, `coupling_not_deep` |
| 2.7 | The leaf (constraint) problem is strictly convex, so its solution is unique | LEAN `XC2_wellposedness_certificates.strict_convexity`, `XC5_lapse_convexity_certificates.convex_for_monotone_kernel` |

## 3. FRW limit

| Step | Statement | Tag |
|---|---|---|
| 3.1 | a0 = kappa c sqrt(G rho_DE) = c^2 sqrt(Lambda/32 pi) at kappa = 1/2 | LEAN `TOE_BEST_ATTEMPT_2026_10_12.a0_lambda_form`, `a0_hubble_form` |
| 3.2 | Clock bound at kappa = 1/2: rho_DE = 4 a0^2/(G c^2), so s^2 <= 8 a0^2/(G c^2) | LEAN `QX1.clock_bound` |
| 3.3 | AC2q: the stiffness vanishes on FRW (D.P = 0, X >= 0), so the background is the canonical scalar's | LEAN `QX1.ac2q_frw_background` |
| 3.4 | [ERRATUM 11-06, see end] AC2q FRW quadratic action: the lapse term is multiplied by (1 - 2 gamma phidot^2)^2; healthy on 72/72 fixtures | SYMPY + NUM (AC7 Q1) |
| 3.5 | v3s's literal K has a stiff partner that beats radiation iff a^2 < A/R; BBN needs mu_K >= 1.84e8 h/Mpc | LEAN `V3_PICTURE.stiff_beats_radiation_iff`, `crossing_redshift_linear`; NUM Q6 |

## 4. Static weak field: law S and the deep law

With x = g/a0 and mu(x) = x/(1+x):

| Step | Statement | Tag |
|---|---|---|
| 4.1 | Balance mu(g/a0) g = g_N  <=>  g^2 = g_N (g + a0) (law S) | LEAN `QX1.balance_iff_lawS` |
| 4.2 | Positive root g = [g_N + sqrt(g_N^2 + 4 g_N a0)]/2 solves law S | LEAN `QX1.lawS_root_solves`, `lawS_root_pos` |
| 4.3 | The positive solution is unique | LEAN `QX1.lawS_unique` |
| 4.4 | g_N < g < g_N + a0 | LEAN `QX1.lawS_bounds` |
| 4.5 | mu limits: x - x^2 <= mu <= x (deep); 1 - 1/x <= mu < 1 (Newtonian) | LEAN `QX1.mu_deep`, `mu_newton` |
| 4.6 | Exact Tully-Fisher of law S: v^4 = G M (a0 + v^2/r), so flat curves give v^4 = G M a0 | LEAN `QX1.lawS_tully_fisher`; also `TOE_BEST_ATTEMPT.deep_tully_fisher` |
| 4.7 | Law S is not the squared-excess law B; B's landmarks need their own premise | LEAN `EQB_A0LINE_uniqueness.simple_nu_not_linear` (TP01 correction) |
| 4.8 | SPARC RAR rms 0.054 / 0.054 dex (one Upsilon per galaxy, EFE solved for 109) | NUM P4 |

## 5. PPN

| Step | Statement | Tag |
|---|---|---|
| 5.1 | gamma = beta = 1 to 1e-12 | SYMPY + NUM, V3W W1 (17d7b7ecdc). It is a PDE statement, not Lean-certifiable here |
| 5.2 | [ERRATUM 11-06, see end] AC2q: the static difference from v3s is proportional to s^2 (Poisson + s^2(1 - 2 gamma div P)/(1+phi)^3; P eq + 2 gamma s^2 grad phi/(1+phi)^3), relative <= 2.2e-10 | SYMPY AC8 (bc4a81ee47) |

## 6. Tensor speed

| Step | Statement | Tag |
|---|---|---|
| 6.1 | v3s: c_T = c to 6e-32 | NUM V3W W4a |
| 6.2 | AC2q: no (dh)^2 term at O(h^2); the principal part is GR's | SYMPY AC9 T1a (0111fe2269, 29eb0c2bf9) |
| 6.3 | Massive dispersion: 1 - v_g^2/c^2 = m^2 c^2/omega^2 | LEAN `QX1.tensor_group_velocity` |
| 6.4 | The new masses m^2 = 16 pi gamma s^2(G_xx + G_yy - A_z P0_z) (on) and 8 pi gamma s^4 (off) vanish at s = 0 | SYMPY AC9 T1b; LEAN `QX1.ac9_masses_vanish` |
| 6.5 | Record masses 1.1e-57 / 1.7e-57 m^-2 give dv/c < 1.3e-46 / 2e-46 at 100 Hz, inside GW170817's band | LEAN `QX1.ac9_dv_bounds`, `omega_lower` (the masses themselves are NUM) |

## 7. Lensing = dynamics

| Step | Statement | Tag |
|---|---|---|
| 7.1 | phi = psi in the static limit: the Psi equation has no source at O(GM) | SYMPY V3W W1/W3 |
| 7.2 | AC2q: S_Psi = gamma s^2 (grad Phi . P)/(1+Phi)^2 and Pi_ij ~ gamma s^2 (P_(i d_j) Phi)^TF, beyond O(GM); slip <= 3.1e-17 | SYMPY + NUM AC9 T2 |
| 7.3 | KiDS galaxy lensing consistent (weak power alone) | NUM V3W W3 |

## 8. Solar System: Cassini hedgehog and the Lstar floor

| Step | Statement | Tag |
|---|---|---|
| 8.1 | Inside Lstar the Sun's field is the hedgehog GM/Lstar^2 r_hat with no quadrupole; all 24 Cassini cells pass by 4.8e7-5.1e9 | NUM C6 / C6P (8c5703da06) |
| 8.2 | The unscreened law fails Cassini 2.44-5.19x (why Lstar exists) | NUM E2 |
| 8.3 | The switched stiffness is well posed and leaves the statics unchanged (exact switch, no new scale) | NUM + SYMPY X3 (8aeba82a87); LEAN `V3_PICTURE.switched_*` (pointwise WKB) |
| 8.4 | The saddle: an unswitched stiffness is Hadamard ill-posed where rho_tau < 0 | LEAN `V3_PICTURE.saddle_unbounded` |
| 8.5 | [ERRATUM 11-06: bound 1.1e-10, see end] AC2q carries 8.1-8.3 with corrections <= 2.2e-10 (static shift <= 1.1e-5) | SYMPY AC8; NUM AC7 Q4 |

## 9. AC2q reductions and dynamics

| Step | Statement | Tag |
|---|---|---|
| 9.1 | AC10 S1: the planar AC2q system is v3s's label system with charge Pi = D.P + s^2; at N = 1 the stiffness is -(gamma/2)[max(D.P + s^2, 0)^2 - s^4] | SYMPY AC10 S1; LEAN `QX1.ac10_charge_form` |
| 9.2 | Clock-only stream J = 1 - A sin(Omega tau) solves J'' = Omega^2 (1 - J), J(0) = 1 | LEAN `QX1.Jstream_ode`, `Jstream_initial` |
| 9.3 | It folds (J <= 0 for some tau >= 0) iff A >= 1 iff Omega tau_f <= 1, with A = 1/(Omega tau_f), tau_f = w/(K Sigma) | LEAN `QX1.fold_iff_amplitude`, `fold_iff_threshold` |
| 9.4 | First fold of AC2q = v3s's to 0.3 % (12/240 rows); neither s^2 nor the switch regularizes | NUM AC10 (NO VERDICT as frozen); AC14 running |
| 9.5 | Galaxy health: no Gamma ~ k anywhere; off-region bounded; omega^2 -> K rho_q (M_theta - 1) | SYMPY + NUM AC7 Q2 |
| 9.6 | Moving Sun: linear NO VERDICT (AC11); kinematic halo subsonic at 1 AU but not self-consistent (AC12) | NUM; AC15 running |

## What the chain does not reach

- **kappa**: FITTED, and proved not derivable from the stated premises.
- **J(Y), Lstar**: postulated.
- **PPN, c_T and lensing**: PDE-level statements, held as SYMPY/NUM. Lean certifies only their algebraic kernels (2.3, 6.3).
- **Clusters, CMB-lensing shape, linear growth (AC2q has no dust), AGC 114905 and Malin 1**: outside this chain's passes.
  Their labels are in closure_2026_11_05/CLOSURE.md section 2.

## Addendum 11-06 (QX17): the full covariant field equations

The complete Euler-Lagrange set of v3s (metric equation with every stress tensor, khronon current, P constitutive law,
multiplier) is in `QX17_covariant_field_equations/RESULT.md`. It is CERTIFIED against a direct sympy variation (residuals
<= 1.2e-40, MUTATE fails). It is derived from the operative Legendre form P.A - W(K|P|). The printed J(Y) + independent-P
form in §1 / PAPER68 decouples P if read literally (erratum on the printed form only; no number changes).

> **Addendum 2026-11-07 (QX17D, 6b16322464; owner adopted the Pi^6 blend, 71e4014cd5).** (Fix-forward: a second,
> consistent QX17D addendum was appended below at 6c36fac3d5 by another session; the two state the same rule.
> Neither is removed.) For the adopted stiffness
> F(Pi) = gamma b^2 f(Pi/b), b = rho_DE, the v3s Euler-Lagrange set above holds with Pi_+ -> F'(Pi) everywhere, and
> the stress-tensor term written 2F h_mn for the raw step becomes Pi F'(Pi) h_mn (the two coincide for the raw F,
> which is why QX17 could not separate them). Reading R1 (2F h kept) FAILS K3 at 9.1e-2 / 1.4e-1; reading R2 is
> CERTIFIED to 7.1e-40 on both test stiffnesses. Tag: SYMPY + NUM (QX17D).

## Erratum, 2026-11-06 (fix-forward; the rows above keep their original text)

Source: an independent FRW reconciliation by another session, `closure_2026_11_06/FRW_RECONCILIATION_CHAIN/CHAIN.md`. It landed
in 8d075bf20f with the Lean file `fable_independent_2026/lean_2026/FRW_correction.lean` (11 theorems, standard axioms; MUTATE 3/3 fail).
- **Row 3.4.** For AC2q as defined (D is the intrinsic leaf divergence, AC2 ACTION.md), the FRW lapse/polarization mixing is (1 - z),
  with z = gamma phidot^2/N^2. The induced factor is (1 - z)^2, not (1 - 2 gamma phidot^2)^2. The legacy factor is exact only when D is
  the spacetime divergence (control action A5). It is a coefficient error. The SIGNS survive: for any f >= 0, 0 < c_g <= c_ph <= 1
  (Lean, 11 theorems). So "healthy" stands, and only the coefficient identity and its quoted numbers change. AC23's PASS reproduces
  with the corrected insertion (max R 2.70011 vs 2.70014).
- **Row 5.2.** With the full measure, the static P-equation offset is gamma v^2 grad phi/(1+phi)^2, half the stated
  2 gamma s^2/(1+phi)^3. The bound becomes 1.1e-10 (was 2.2e-10). The conclusion (transfer to v3s) is unchanged.
- **QX19 (one action).** The same reconciliation marks the scorecard **CONDITIONAL** (its J3). TC03's finite-time gradient
  catastrophe transfers to the QX19 action if the bootstrap box can sit inside Sigma = D.P + 2X > X, where the blend equals AC2q.

## Addendum, 2026-11-07 (fix-forward; the rows above keep their original text): adopted blend stiffness and its field equations

- **Stiffness adopted.** Per the owner's decision (`closure_2026_11_07/OWNER_DECISION_2026-11-07_ADOPT_PI6_BLEND.md`,
  71e4014cd5), the stiffness in §1 is now the Pi^6 blend: -(gamma/2)[max(D.P, 0)]^2 becomes -gamma F(Pi), with
  F(Pi) = b^2 f(Pi/b) and b = rho_DE (AC21 iter_6; f is a pure q^6 below 1/2, C4 and convex, and q^2/2 for q >= 1).
  AC2q is not adopted. If it is, its L_stiff line carries the same blend with b = X (QX19).
- **Limits adopted with it.**
  - Row 8.3 ("well posed") is read with AC16, which labels the raw switch: well-posedness is local in time (TC1).
  - It is tested in curved 2D (AC22) and in spherical 3D (BL3); non-radial modes are untested.
  - Folds are unchanged.
- **Field equations (QX17D, 6b16322464, criteria 78b03d2973: R2 CERTIFIED).** The equations of the blended action are
  QX17's with Pi_+ -> F'(Pi) in the P equation, the khronon equation, the constitutive factor and J_P, **and with the
  stress-tensor term 2F h_mn replaced by Pi F'(Pi) h_mn.**
  - For the raw F the two terms are equal (Pi F' = 2F). So QX17's certification holds for v3s as printed but does not
    carry to the blend.
  - Keeping 2F h_mn fails the metric equation: K3 is 9.1e-2 for the generic test stiffness and 1.4e-1 for the blend's
    Pi^6 branch. The corrected form passes at <= 7.1e-40.
  - n n T = Pi + gamma F(Pi) is unchanged, so the static source and the Poisson limit are unchanged. No graded number
    moves.
- **QX19 CONDITIONAL**, noted in the erratum above, was later removed by TC1 (746f8b6fb4, FIRES). No PASS row was lost,
  and well-posedness is local-in-time.

Kappa = 1/2 FITTED; not theory closed.

> **Note (fix-forward, 2026-11-07):** the "Field equations (QX17D)" item of the addendum above repeats the earlier QX17D
> addendum after the QX17 section (1a6c3c46a0); the two agree (gamma written inside F there, outside here; same equations).
> That earlier addendum is the field-equation statement; this one adds the adopted stiffness, its limits and the TC1 note.
