# Master Lagrangian of candidate B (assembled from the record, 2026-10-05)

This is an assembly. Every term below is already in a committed lane. Nothing new is added: no new physics, no new
constants, no scans. kappa = 1/2 is FITTED, not derived. The theory is not closed. Two terms carry open or partial
status, and those are marked.

**Update 2026-10-06.** On the owner's request the switch term is now CFG354's T1, the best switch on the record
(STANDING, CFG355 entry). It replaces CFG337's inverted symmetron, which is kept below as a superseded alternative.
T1 reads the total matter, which relaxes MS1; that relaxation is an owner decision (2026-10-06), not a result.

## 1. The action in one display

Signature (-+++), x^0 = ct, alpha = a0/c^2, b = xi^2/2.

```
S_B = c^3/(16 pi G) Int d^4x sqrt(-g) {
        R - 2 Lambda                                                    [EH + Lambda]
      + f [ 2 h^{mu nu}(D_mu U - a_mu)(D_nu U - a_nu)                       [C-H MOND sector,
                 + 2 alpha^2 q( h^{mu nu} D_mu W_b D_nu W_b / alpha^2 )      gated by the switch]
                 + Int_0^b dz L(z,x) [d_z W - Delta_h W]                    [heat filter, z-slice]
                 + lambda_0 (W(0,x) - U) ]                                  [filter endpoint]
      + alpha_c a_mu a^mu - c_2 (K - <K>_Sigma)^2 }                         [khronon, beta = 0]
    + GHY cap terms (C-H)
    + Int dt Int_Sigma d^3x sqrt(h) N [ mu (Delta_h Phi_d - 4 pi G (rho - <rho>_Sigma)) + nu Phi_d ]
                                                                         [switch reader T1: BEST ON RECORD]
    + S_m[g; psi_baryon, A_mu]                                           [matter, minimal on g only]
    + S_cold[g; dust u^mu, rho_c]                                        [cold component: dust stress only]
```

with q from the monotone kernel nu_mono, a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 (FITTED),
and n_mu = -d_mu tau/sqrt(X), N = X^(-1/2),
a_mu = D_mu ln N, K = nabla_mu n^mu (the clock tau is varied).

**The switch (CFG354 T1).** f = H_eps(l_2 - tau_ta), where
- Phi_d solves the leaf-elliptic constraint Delta_h Phi_d = 4 pi G (rho - <rho>_Sigma), with rho = cold + baryons
  (the total matter; owner decision 2026-10-06, relaxing MS1). mu and nu are the multiplier fields, as for the
  record's U, L and lambda_0 (CFG353/354 action form);
- psi = Phi_d/(4 pi G rho_bar), t_ij = D_i D_j psi, and l_1 >= l_2 >= l_3 are its eigenvalues; T1 reads the middle one;
- tau_ta = (Delta_ta - 1)/3, with Delta_ta the derived turnaround contrast (11.806 at z = 0 and 8.893 at z = 0.25 (footing-independent);
  CFG354 K4 = CFG4);
- H_eps is a step of width eps, one declared constant, eps >= eps_min = 0.077 (edge smearing <= 1.6% r_ta). The
  sharp step is ill-posed under the external tide (surface-delta layer, c_d != 0), so eps is required.

f depends on D_i D_j Phi_d only (an order-0 Riesz operator on the source). There are no time derivatives of Phi_d,
mu or nu, so no momenta and no Ostrogradsky degree of freedom (CFG354 L3). For every sphere l_2 = l_t =
(4 pi G/3)(rho_enc - rho_bar) in physical units, i.e. (Delta_enc - 1)/3 scaled, so an isolated host's edge is exactly r_ta.

**Superseded switch (CFG337, kept as an alternative).**
`Int d^4x sqrt(-g) [ -(1/2)(d sigma)^2 + (1/2) mu0^2 T(U_r) sigma^2 - (lambda/4) sigma^4 ]` with f = sigma^2/v^2,
v^2 = mu0^2/lambda, T(U_r) = 1 - 1/U_r. PARTIAL: the transition fails at the data level (CFG346).

**Status of each term**

| term | source (file, commit) | status |
|---|---|---|
| R - 2 Lambda, GHY caps | C-H `qwen_claude_field_theory/closure_2026/g03_covariant_action_2026/ACTION.md:95-106` (301b154544) | standard |
| 2\|DU - a\|^2, 2 alpha^2 q, heat slice, lambda_0 | same ACTION.md; plane-symmetric form `campaign_fresh_gravity/CFG329_g9_g0_structure/cfg329_g9_g0.py:183-185` (86085d6ef) | G9 PASS (CFG329); G0 CONDITIONAL |
| kernel nu_mono inside q | `real_research/g03_audit_2026/L340_filtered_khronon_completion.py:104-118` (9ea5ab2c63) | L340 A1/H2 pass; K2 SPARC tie with nu_RAR (\|Delta chi^2\| <= 2) |
| alpha_c a^2 - c_2 (K - <K>)^2, beta = 0 | L340 (9ea5ab2c63); leaf average as a function of tau: CFG329 S2/S4 (86085d6ef) | healthy at the orders computed (L340 11/11); CFG292 (918b331834) principal symbol; CFG294 (e92012b82) CONDITIONAL |
| f = H_eps(l_2 - tau_ta) gate on the MOND sector + Phi_d, mu, nu reader action | `campaign_fresh_gravity/CFG354_tidal_turnaround_switch/README.md` (criteria bd5ab6223, results 67b8311c5); smeared edge in `CFG355_tidal_plus_rank_switch/README.md` (be5eee875) | **BEST ON RECORD. Legal (L1-L4); OFF on the linear field; hosts ON with edge at 0.95-0.99 r_ta; passes KiDS (sharp and smeared), SPARC and growth; 1 declared width constant; FAILS dense filament cores (Lean theorem for eigenvalue-only readers); whether filament-core switching conflicts with data is under scoping.** |
| superseded: f(sigma) inverted symmetron | `campaign_fresh_gravity/CFG337_stable_switch_action/README.md` Part 3 (4256f91a3) | PARTIAL: transition fails at data level (CFG346, 689065960) |
| matter minimal on g | CFG329 G9 (86085d6ef); ACTION.md point masses + Maxwell | PASS (nabla T = 0 on shell) |
| cold component | `campaign_fresh_gravity/CFG4_README.md` T5 (8cedf6757d); CFG345 README (b8abeb0ff) | **bookkeeping only, no committed microphysics** |

**Switch choice.** The owner asked for CFG354's T1 as the best switch. CFG354's frozen primary rule (T3) is NO-GO;
T1 was a reported rule there, and its verdict is PARTIAL at a cost of 1 constant (the width). CFG355 ran the smeared
T1 through the harness: KiDS d chi2 -10.47 / -11.14 and -9.78 / -10.39 (pass), closing CFG354's open gap. CFG355 also
shows the width cannot be derived from framework scales (Poincare-Hopf degenerate points kill the tidal-split
candidate). The CFG355 rank veto itself is NO-GO and is not adopted.

**Switch history (CFG337 -> CFG355).**

| lane | reader | verdict | obstruction |
|---|---|---|---|
| CFG337 | inverted symmetron on U_r (C1 door / C2 rho_b ratio) | PARTIAL | sharpness vs stability trade-off; ell >= c_g/Gamma_g at Mpc scale |
| CFG346 | CFG337 smeared, scored on data | PARTIAL | best config passes KiDS and growth, fails SPARC; all configs add constants |
| CFG347 | baryon expansion theta_b | PARTIAL | zero-constant no-go: OFF in the Hubble flow forces theta_on <= 3H; ghost, flicker, range or over-coupling in hosts |
| CFG348 | energy eps_b = v_b^2/2 + U | NO-GO | FRW sits at eps = 0; no single width keeps linear wells OFF and every host ON |
| CFG349 | khronon-timed memory ratchet | PARTIAL, legality FAIL | multiplier action has unbounded energy; CTP action loses momentum conservation |
| CFG350 | baryon coarse-grained state (sigma_ij, entropy) | NO-GO | IGM hotter than the discs to be turned ON; cooling erases the record |
| CFG351 | cold full-rank dispersion H(det sigma_c) | PARTIAL, 4 of 5, 0 constants | edge at the second caustic, 0.23 r_ta, not at r_ta |
| CFG352 | CFG351's edge on data | PARTIAL | KiDS fails (+169 / +163): lensing needs the law out to turnaround |
| CFG353 | turnaround density from Phi_d | NO-GO, 0 constants | Phi_d's zero point set by the environment; edge 0.06-0.45 r_ta; KiDS +260 to +609 |
| CFG354 | tidal eigenvalues of psi (T1 middle, T2 smallest, T3 projected) | T3, T2 NO-GO; **T1 PARTIAL, n = 1** | T1: dense filament cores fire (theorem); width needed for well-posedness |
| CFG355 | T1 + rank-2 cold-stream veto | NO-GO, n = 1 | veto switches off the 3-stream shell in every host (KiDS +52); smeared T1 alone passes; width not derivable |

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
| switch width eps (T1) | eps >= eps_min = 0.077 (edge smearing <= 1.6% r_ta) | **DECLARED, 1 new constant; not derivable from framework scales (CFG355)** | CFG354, CFG355 |
| Delta_ta (T1 threshold tau_ta = (Delta_ta - 1)/3) | 11.806 at z = 0 and 8.893 at z = 0.25 (footing-independent); EdS 9 pi^2/16 | DERIVED (depends on Omega_m, Lambda and z); 0 fitted | CFG4, CFG354 K4 |
| MS1 relaxation (switch reads total matter) | rho = cold + baryons in Phi_d | OWNER DECISION 2026-10-06, not a result; under the original MS1 T1 is NOT ADMISSIBLE | CFG351, CFG354 |
| superseded CFG337 constants: mu0 (or ell), lambda (or E_c, R), Delta_e | single-E_c version needs ell >= 29 Mpc; lenient C2 ell_min 183-378 kpc | DECLARED (no longer in the action) | CFG337, CFG346 |

**Count.** Fitted: kappa (1). Declared constants: xi, alpha_c, c_2, beta (= 0), delta, and the switch width eps (the
switch adds exactly 1). Declared rules with no constant: the T5 max rule. Inputs: Lambda, Omega_c h^2. Derived:
a0, y_p, h_p, Delta_ta.

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
- **Phi_d, mu, nu (switch reader).** Varying mu gives Delta_h Phi_d = 4 pi G (rho - <rho>_Sigma). The Phi_d and mu
  Euler-Lagrange equations are CFG354's sympy L1; Phi_d, mu and nu are elliptic, with no time derivatives (L3).
  T1 reads only the Hessian, so it has no zero-point dependence (CFG353's failure mode). With width eps the
  reader's back-reaction on the matter is bounded; the sharp step would put a surface-delta layer into the matter
  potential (CFG354).
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
- **LCDM growth on FRW.** FRW has t = 0, so l_2 = 0 < tau_ta and T1 is OFF (Lean `t1_frw_off`, `t1_off_reduction`).
  In the linear field T1 is ON in 0 of 4e6 samples at R = 8/20/50 h^-1 Mpc at every z (chi2 bound <= 1.1e-77) and
  in the unsmoothed field at z = 1000 (CFG354 (a)). Linear growth is the dust plus baryons of LCDM. The cold mass is
  the Omega_c h^2 = 0.12 input.

## 5. What is NOT established

- **Dense-filament false positives (T1).** T1 fires inside every filament with delta_f >= 2 tau_ta (3.03 EdS, 7.20
  at z = 0), false ON in 1-11% of the cell (CFG354 (a')), and in pre-crossing regions of a Zel'dovich box at 0.9-4.1%
  of the volume (CFG355 A2). Lean (CFG354 S8, here `monotone_rule_fires_in_filament`) proves any monotone eigenvalue
  rule ON at a host edge fires there. Whether filament-core switching conflicts with data is under scoping.
- **The width is underived.** eps >= 0.077 is a declared constant needed for well-posedness. CFG355 shows the
  tidal-split candidate eps = l_1 - l_2 fails at Poincare-Hopf degenerate points, and neither a0 nor xi fixes a
  dimensionless width.
- **Ownership class E.** GCs and wide binaries sit inside the host's full-rank, T1-ON interior. The CFG333 R2
  ownership rule is still needed. No committed action produces B's bound-only ownership; the T5 max rule is declared.
- **The cold component as total matter.** T1 reads rho = cold + baryons, but the cold component has no committed
  microphysics (CFG345); only a dust stress tensor is written. The MS1 relaxation that admits this reader is an owner
  decision.
- **Superseded switch.** CFG337 H4 fails in the transition (sharpness vs stability, ell >= c_g/Gamma_g at Mpc scale);
  CFG346 is PARTIAL at data level.
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
- the superseded switch potential's stationary points and masses, and the T1 switch's sphere identity, threshold,
  OFF reduction, width positivity and filament obstruction;
- the reductions of the total density;
- positivity of the kinetic and principal coefficients in the stated windows;
- the kappa = 1/2 identity.

**What it cannot certify.**
- That nature obeys this action.
- Existence, uniqueness or stability of PDE solutions beyond the stated frozen-coefficient inequalities.
- The nu_mono numerical tail itself. Lean treats it through its derivative's positive floor.
- The covariance of the full 4D action. That is CFG329's numerical Noether test.

`MasterLagrangian.lean`: **47 theorems/lemmas, no sorry, rc 0** (re-compiled 2026-10-06). Axioms are propext, Classical.choice and Quot.sound
only. The output is in `MasterLagrangian.out`. The sections are:
- A: nu_RAR > 1, nu - 1 <= 1/sqrt y, nu -> 1, and the deep sandwich and limit;
- B: nu_mono slope > 0, strict monotonicity, and C_T > 0;
- C: the kernel-term bound, and vanishing as a0 -> 0;
- D (SUPERSEDED, kept compiling): the CFG337 switch V, V', V'' derivatives, OFF stable for 0 < U < 1, the broken minimum stable for U > 1, f = 0 OFF,
  f = T at the minimum, and trigger concavity;
- E: switch-OFF/FRW, static, and MOND-removed reductions;
- F: L340 tracking c_s^2 > 0, CFG292 c_S^2 > 0 iff alpha_c > 0, the leading-matrix factor nonzero, the CFG329
  lapse coefficient > 0, the switch kinetic matrix positive definite, and the L340 P1 window implying every
  preferred-frame, BBN and positivity bound;
- G: kappa = 1/2 with rho_Lambda = Lambda c^2/(8 pi G) giving a0 = c^2 sqrt(Lambda/(32 pi)), and G rho_Lambda = 4 a0^2/c^2;
- H: the T1 switch (13): the sphere identity g/r = GM/r^3 = (4 pi G/3) rho_enc; in scaled units l_t = (Delta_enc - 1)/3;
  l_2 = l_t for every sphere, so T1 is ON on a sphere iff Delta_enc >= Delta_ta; tau_ta > 0 for Delta_ta > 1 (EdS
  tau > 1; record values 11.806 (z = 0) / 8.893 (z = 0.25) positive); FRW OFF and the OFF reduction to R - 2 Lambda + L_m; f = 0
  removes the MOND sector; eps_min = 0.077 > 0; filament core l_2 = c; and the monotone-rule filament obstruction.

Compile: `cd fable_independent_2026/lean_2026 && lake env lean <abs path>/MasterLagrangian.lean`.

**Certificate index** (re-compiled 2026-10-05; CFG347-355 and this file re-compiled 2026-10-06; same command; the
counts are `theorem|lemma` declarations):

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
| CFG347 first-principles switch | CFG347_first_principles_switch/CFG347_switch_certificates.lean | 11 | 0 |
| CFG348 energy reader | CFG348_energy_reading_switch/CFG348_energy_certificates.lean | 9 | 0 |
| CFG349 memory ratchet | CFG349_khronon_memory_switch/CFG349_memory_certificates.lean | 10 | 0 |
| CFG350 emergent baryon state | CFG350_emergent_switch/CFG350_emergent_certificates.lean | 11 | 0 |
| CFG351 cold full-rank | CFG351_cold_threeaxis_switch/CFG351_threeaxis_certificates.lean | 17 | 0 |
| CFG352 caustic edge vs data | (no Lean file; numerical harness only) | - | - |
| CFG353 turnaround density | CFG353_turnaround_density_switch/CFG353_estimator_certificates.lean | 12 | 0 |
| CFG354 tidal switch (T1) | CFG354_tidal_turnaround_switch/CFG354_tidal_certificates.lean | 15 | 0 |
| CFG355 T1 + rank veto | CFG355_tidal_plus_rank_switch/CFG355_veto_certificates.lean | 19 | 0 |
| **this file** | MASTER_LAGRANGIAN_2026-10-05/MasterLagrangian.lean | 47 | 0 |

Paths are relative to `campaign_fresh_gravity/` unless shown in full. No file in the index contains `sorry` as a
tactic. CFG332's one match is the phrase "Zero sorry" in its header. These certify each lane's algebra. They do not
certify the physics claims the lanes test.
