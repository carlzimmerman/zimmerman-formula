# Master Lagrangian of candidate B (assembled from the record, 2026-10-05)

This is an assembly. Every term below is already in a committed lane. Nothing new is added: no new physics, no new
constants, no scans. kappa = 1/2 is FITTED, not derived. The theory is not closed. Two terms carry open or partial
status, and those are marked.

## 1. The action in one display

Signature (-+++), x^0 = ct, alpha = a0/c^2, b = xi^2/2.

```
S_B = c^3/(16 pi G) Int d^4x sqrt(-g) {
        R - 2 Lambda                                                    [EH + Lambda]
      + f(sigma) [ 2 h^{mu nu}(D_mu U - a_mu)(D_nu U - a_nu)                [C-H MOND sector,
                 + 2 alpha^2 q( h^{mu nu} D_mu W_b D_nu W_b / alpha^2 )      gated by the switch]
                 + Int_0^b dz L(z,x) [d_z W - Delta_h W]                    [heat filter, z-slice]
                 + lambda_0 (W(0,x) - U) ]                                  [filter endpoint]
      + alpha_c a_mu a^mu - c_2 (K - <K>_Sigma)^2 }                         [khronon, beta = 0]
    + GHY cap terms (C-H)
    + Int d^4x sqrt(-g) [ -(1/2)(d sigma)^2 + (1/2) mu0^2 T(U_r) sigma^2 - (lambda/4) sigma^4 ]   [switch: PARTIAL]
    + S_m[g; psi_baryon, A_mu]                                           [matter, minimal on g only]
    + S_cold[g; dust u^mu, rho_c]                                        [cold component: dust stress only]
```

with q from the monotone kernel nu_mono, a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 (FITTED),
f = sigma^2/v^2, v^2 = mu0^2/lambda, T(U_r) = 1 - 1/U_r, and n_mu = -d_mu tau/sqrt(X), N = X^(-1/2),
a_mu = D_mu ln N, K = nabla_mu n^mu (the clock tau is varied).

**Status of each term**

| term | source (file, commit) | status |
|---|---|---|
| R - 2 Lambda, GHY caps | C-H `qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md:95-106` (301b154544) | standard |
| 2\|DU - a\|^2, 2 alpha^2 q, heat slice, lambda_0 | same ACTION.md; plane-symmetric form `campaign_fresh_gravity/CFG329_g9_g0_structure/cfg329_g9_g0.py:183-185` (86085d6ef) | G9 PASS (CFG329); G0 CONDITIONAL |
| kernel nu_mono inside q | `real_research/g03_audit_2026/L340_filtered_khronon_completion.py:104-118` (9ea5ab2c63) | L340 A1/H2 pass; K2 SPARC tie with nu_RAR (\|Delta chi^2\| <= 2) |
| alpha_c a^2 - c_2 (K - <K>)^2, beta = 0 | L340 (9ea5ab2c63); leaf average as a function of tau: CFG329 S2/S4 (86085d6ef) | healthy at the orders computed (L340 11/11); CFG292 (918b331834) principal symbol; CFG294 (e92012b82) CONDITIONAL |
| f(sigma) gate on the MOND sector + switch action | `campaign_fresh_gravity/CFG337_stable_switch_action/README.md` Part 3 (4256f91a3) | **PARTIAL: transition fails at data level (CFG346, 689065960)** |
| matter minimal on g | CFG329 G9 (86085d6ef); ACTION.md point masses + Maxwell | PASS (nabla T = 0 on shell) |
| cold component | `campaign_fresh_gravity/CFG4_README.md` T5 (8cedf6757d); CFG345 README (b8abeb0ff) | **bookkeeping only, no committed microphysics** |

**Switch choice.** CFG347 (`campaign_fresh_gravity/CFG347_first_principles_switch/`, criteria 9c57125bd) has a
results JSON in the working tree. It is not committed and has no README. Its frozen verdict is **PARTIAL**: every
route fails gate (b), bound fidelity and reach; R1 saturated and R2 are NO-GO. It has no healthy candidate. So the
record's switch term stays CFG337's inverted symmetron. In it, U_r is the reader: C1 is the MOND-sector door, C2 is
rho_b/(Delta_e <rho_b>_leaf). Both are PARTIAL.

**Cold component.** B needs Omega_c h^2 = 0.120. No dark-matter particle is added. What the record specifies is
CFG4 T5 "identity bookkeeping": in a bound region the dark mass is max(M_ph, (Omega_c/Omega_b) M_b), and the max rule
is DECLARED. Scoring uses rule S (CFG344). CFG345 states that "B as frozen specifies no microphysics for its cold
component". So S_cold is written only at the record's level of specification: a pressureless dust stress tensor
T_c^{mu nu} = rho_c u^mu u^nu, conserved, minimally coupled. This is a stress tensor, not a field Lagrangian. The one
live microphysical construction is CFG288's wave field with undeclared mass m. CFG345 shows it is CDM-like only if
m >= 2.29e-20 eV. It is not part of B.

## 2. Parameters

| parameter | value / window | class | source |
|---|---|---|---|
| kappa | 1/2 | **FITTED** | CFG4_common.py:51 |
| a0 | kappa c sqrt(G rho_Lambda): 9.36e-11 (canonical) / 1.13e-10 (alt) m/s^2 | derived from kappa + Lambda (both footings, never pooled) | CFG4_common.py:7-8 |
| Lambda (rho_Lambda) | observed | input | ACTION.md:21 |
| xi (b = xi^2/2) | >= 0.03 pc (Solar floors 0.031/0.045 pc canonical, 0.033/0.049 alt) | DECLARED (one universal length) | L340 S1 |
| alpha_c | (9.6e-14, 3.2e-9) | DECLARED, windowed | L340 P1 (.out:104) |
| c_2 (= lambda_BPS) | (7.2e-3, 0.067); BBN gives c_2 < 1/15 | DECLARED, windowed | L340 P1 |
| beta | 0 (c_T = 1) | DECLARED | L340, CFG292 |
| nu_mono shape | y_p = 2.540, h_p = 0.6476 a0, delta = 0.05 | y_p, h_p DERIVED from nu_RAR; delta DECLARED | L340 A1 |
| Omega_c h^2 | 0.120 | input (CMB) | CFG4, CFG345 |
| max rule (T5) | max(M_ph, (Omega_c/Omega_b) M_b) | DECLARED, no constant | CFG4 T5 |
| switch mu0 (or length ell), lambda (or E_c, R = E_c/B), Delta_e (C2 door) | single-E_c version needs ell >= 29 Mpc; lenient C2 ell_min 183-378 kpc | DECLARED, new constants (CFG346: all configurations add constants) | CFG337, CFG346 |

## 3. Field equations, in words

- **Metric.** G_mu nu + Lambda g_mu nu = 8 pi G/c^4 (T_m + T_c + T_switch) + the stress of the gated C-H sector + the
  khronon stress. CFG329 G9 shows the generalized Bianchi identity holds off shell. So on the tau, U, W, L, lambda_0
  shell nabla_mu T_m^{mu nu} = 0 exactly, and the clock equation is implied.
- **L and lambda_0.** d_z W = Delta_h W, W(0) = U, W_b = S U. This is the heat filter: W_b is U smoothed over xi.
- **U.** -4 N^-1 D_i[N(D^i U - a^i)] = lambda_0. The filtered kernel source enters through lambda_0, and the
  weak-field limit is Delta Phi = 4 pi G rho + S* div[(nu(|grad S u|/a0) - 1) grad S u] (QUMOND, ACTION.md:208).
- **Clock tau.** Second order in time (CFG329 T2). The lapse equation is elliptic, with coefficient
  (2C + alpha_c(1+C))/(1+C) > 0. c_2 gives the phantom momentum (tracking, L340 H1). alpha_c removes the
  negative-lobe pole (L340 H4).
- **sigma.** box sigma = V'(sigma) - f'(sigma) x (MOND-sector energy). On FRW sigma = 0 is exact at linear order
  (Z2). In bound interiors sigma^2 = mu0^2 T/lambda.
- **Matter and dust** follow geodesics of g.

## 4. Limits

- **GR when a0 -> 0.** The kernel term 2 alpha^2 q(p^2/alpha^2) <= 2 M p^{3/2} sqrt(alpha) -> 0, given the deep bound
  q ~ (4/3) s^{3/2} (CFG329 T1) (Lean section C). U then sources nothing, and with the khronon coefficients in their
  window, alpha_c only renormalises G by about 1e-9 (L340 H5). Switch OFF on FRW with homogeneous lapse (a = 0) and
  K = <K> also leaves R - 2 Lambda + L_m (Lean `switch_off_frw`).
- **MOND/RAR in the deep regime.** nu_mono = nu_RAR below y_p. On that branch g/sqrt(g_N a0) = sqrt(y) nu lies in
  [1, 1 + sqrt y] -> 1 (Lean `deep_mond_sandwich`, `deep_mond_limit`). Newtonian side: nu - 1 <= 1/sqrt y -> 0.
  Above y_p the phantom keeps rising at slope delta h_p/(y + y_p) > 0, which is the monotone condition L340 needs.
  The Solar tail of that branch is hidden by the filter at xi >= 0.03 pc (L340 S1).
- **LCDM growth on FRW.** The switch is exactly OFF at linear order (CFG337 (a)): mass^2 = mu0^2(1/U - 1) > 0 for
  U < 1. Linear growth is the dust plus baryons of LCDM. The cold mass is the Omega_c h^2 = 0.12 input.

## 5. What is NOT established

- **Switch stability at the edge.** CFG337 H4 fails in the transition: sharpness and stability trade off, giving
  ell >= c_g/Gamma_g at Mpc scale. CFG346 is PARTIAL at data level: the best configuration passes KiDS and growth
  and fails SPARC, and all configurations add constants. CFG347 (uncommitted) is PARTIAL with no route passing bound
  fidelity.
- **Ownership from an action.** No committed action produces B's bound-only ownership. The T5 max rule is declared.
- **Cold-component microphysics.** None is committed (CFG345). Only a dust stress tensor is written.
- **Nonlinear well-posedness.** CFG294 is CONDITIONAL: local in time, beta = 0, data away from zero-field regions.
- **G0 elliptic solvability.** CFG329 G0 is CONDITIONAL: nonlinear solvability of the elliptic, leaf-non-local
  lapse/U/W/L system is not proved.
- Cosmological perturbations of the C-H sector (C is singular at zero gradient), the full 1PN metric, and the
  CFG329 Noether test beyond its plane-symmetric reduced sector are not computed.
- **kappa = 1/2 is fitted, not derived.** The relation a0 = c^2 sqrt(Lambda/(32 pi)) is not imposed by the action
  (ACTION.md:21-22). Lean proves it only as an algebraic identity.

## 6. Lean

**What Lean certifies.** Algebra, inequalities and reductions of the scalar pieces as real functions:
- kernel limits and monotonicity;
- the switch potential's stationary points and masses;
- the reductions of the total density;
- positivity of the kinetic and principal coefficients in the stated windows;
- the kappa = 1/2 identity.

**What it cannot certify.**
- That nature obeys this action.
- Existence, uniqueness or stability of PDE solutions beyond the stated frozen-coefficient inequalities.
- The nu_mono numerical tail itself. Lean treats it through its derivative's positive floor.
- The covariance of the full 4D action. That is CFG329's numerical Noether test.

`MasterLagrangian.lean`: **34 theorems/lemmas, no sorry, rc 0**. Axioms are propext, Classical.choice and Quot.sound
only. The output is in `MasterLagrangian.out`. The sections are:
- A: nu_RAR > 1, nu - 1 <= 1/sqrt y, nu -> 1, and the deep sandwich and limit;
- B: nu_mono slope > 0, strict monotonicity, and C_T > 0;
- C: the kernel-term bound, and vanishing as a0 -> 0;
- D: the switch V, V', V'' derivatives, OFF stable for 0 < U < 1, the broken minimum stable for U > 1, f = 0 OFF,
  f = T at the minimum, and trigger concavity;
- E: switch-OFF/FRW, static, and MOND-removed reductions;
- F: L340 tracking c_s^2 > 0, CFG292 c_S^2 > 0 iff alpha_c > 0, the leading-matrix factor nonzero, the CFG329
  lapse coefficient > 0, the switch kinetic matrix positive definite, and the L340 P1 window implying every
  preferred-frame, BBN and positivity bound;
- G: kappa = 1/2 with rho_Lambda = Lambda c^2/(8 pi G) giving a0 = c^2 sqrt(Lambda/(32 pi)), and G rho_Lambda = 4 a0^2/c^2.

Compile: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>/MasterLagrangian.lean`.

**Certificate index** (re-compiled 2026-10-05 with the same command; the counts are `theorem|lemma` declarations):

| lane | file | theorems | rc |
|---|---|---|---|
| L340 chassis | fable_independent_2026/lean_2026/L340_chk_certificates.lean | 4 | 0 |
| CFG294 well-posedness core | CFG294_chassis_nonlinear_wellposedness/cfg294_algebraic_core.lean | 9 | 0 |
| CFG312 lapse condition | CFG312_lapse_condition_W/cfg312_lapse_condition_W.lean | 7 | 0 |
| CFG332 globulars | CFG332_globulars_three_routes/CFG332_certificate.lean | 29 | 0 |
| CFG333 ownership rule | CFG333_one_ownership_rule/CFG333_certificate.lean | 32 | 0 |
| CFG336 UFD epoch | CFG336_ufd_formation_epoch/CFG336_certificate.lean | 105 | 0 |
| CFG337 switch action | CFG337_stable_switch_action/CFG337_switch_certificates.lean | 9 | 0 |
| CFG340 pre-reion big systems | CFG340_preion_candidate_big_systems/CFG340_bounds.lean | 6 | 0 |
| CFG344 cold accretion | CFG344_postreion_cold_accretion/CFG344_certificate.lean | 25 | 0 |
| CFG345 cold small scales | CFG345_cold_component_small_scales/CFG345_certificate.lean | 7 | 0 |
| CFG346 smeared switch | CFG346_smeared_switch_vs_data/CFG346_smeared_certificates.lean | 13 | 0 |
| CFG347 first-principles switch (uncommitted) | CFG347_first_principles_switch/CFG347_switch_certificates.lean | 11 | 0 |
| **this file** | MASTER_LAGRANGIAN_2026-10-05/MasterLagrangian.lean | 34 | 0 |

Paths are relative to `campaign_fresh_gravity/` unless shown in full. No file in the index contains `sorry` as a
tactic. CFG332's one match is the phrase "Zero sorry" in its header. These certify each lane's algebra. They do not
certify the physics claims the lanes test.
