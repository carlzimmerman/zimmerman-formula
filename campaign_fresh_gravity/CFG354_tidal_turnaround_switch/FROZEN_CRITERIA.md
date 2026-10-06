# CFG354 FROZEN CRITERIA: a turnaround switch on the tidal eigenvalues of the leaf overdensity potential

Frozen before any script. kappa = 1/2 fixed (fitted); nu_mono; no DM particle (the cold MASS is still required).
Owner decision 2026-10-06: the switch may read the cold component (MS1 relaxed). Under the original MS1 this reader is
NOT ADMISSIBLE. Owner goal: "find a switch that does both" (fires at turnaround AND is legal).

## 1. Object
- Same leaf constraint as CFG353: lap Phi_d = 4 pi G (rho - <rho>_Sigma), rho = cold + baryons. Units:
  psi = Phi_d / (4 pi G rho_bar), lap psi = delta. Tidal tensor t_ij = d_i d_j psi (trace = delta), eigenvalues
  l1 >= l2 >= l3. t has NO zero point (invariant under psi -> psi + c), and is also invariant under psi -> psi + b.x.
- Sphere: tangential eigenvalue (double) l_t = psi'/r = dbar_enc/3 (dbar_enc = enclosed mean overdensity);
  radial l_r = delta(r) - 2 l_t. Turned around <=> dbar_enc >= Delta_ta - 1 <=> l_t >= tau, tau = (Delta_ta - 1)/3.
- Delta_ta(z): CFG353's Lambda-CDM shell ODE (must match CFG4_switch within 1% at z = 0, 0.25); EdS 9 pi^2/16.
- Switch: f = H_strict(R(t, grad psi) - tau). Rules, all frozen and all scored:
  - **T1:** R = l2 (at least two axes over threshold). For EVERY spherical distribution l2 = l_t exactly
    (sorted {l_t, l_t, l_r}: the middle one is always l_t).
  - **T2:** R = l3 (all three axes). For a sphere R = min(l_t, l_r).
  - **T3:** analytic step done before freezing:
    - (i) No function F of the eigenvalue triple alone can equal l_t on all spheres and vanish inside uniform
      cylinders. A sphere with delta = 2 dbar/3 at r (e.g. rho ∝ r^-1) has the triple (c, c, 0), the same as a
      uniform cylinder interior (delta_f/2, delta_f/2, 0). This is a theorem; Lean certifies it.
    - (ii) A rule that does exist uses the field direction n = grad psi / |grad psi|:
      R = min over unit e ⊥ grad psi of e.t.e (the smaller eigenvalue of t projected onto the plane ⊥ grad psi;
      if grad psi = 0, the minimum over all e, i.e. l3).
      - Sphere: exactly l_t (both ⊥ directions are tangential).
      - Infinite cylinder, inside or outside: 0, because the axial direction is ⊥ grad psi with eigenvalue 0.
      - Plane: 0.
      **T3 = this rule.**
    - Known before any number: T3 is NOT invariant under psi -> psi + b.x (a uniform external gradient tilts n).
      Flagged as a risk for (b).
  - Ordering (Courant-Fischer): l3 <= T3 <= l2. So ON(T2) ⊂ ON(T3) ⊂ ON(T1).
- **Primary rule (chosen a priori):** T3. It is the only rule that equals l_t on spheres AND vanishes in ideal
  filaments and sheets, i.e. the best separator by construction. T1 and T2 are scored with the same lines and
  reported. None is substituted after the results.
- Action: S ⊃ Int_Sigma sqrt(h) N [ mu (lap Phi_d - 4 pi G (rho - <rho>)) + nu Phi_d ]
  + Int sqrt(-g) f(D_i D_j Phi_d, D Phi_d) L_MOND.

## 2. Tests and pass lines (each rule)
- **L legality / well-posedness:**
  - L1: Euler-Lagrange equations (sympy) for Phi_d and mu.
  - L2: every term is a leaf scalar density (eigenvalues of h^ik D_k D_j Phi_d; CFG329 method).
  - L3: no d_t of Phi_d, mu or nu, so no momenta and no Ostrogradsky DOF. t = d d lap^-1 (4 pi G delta rho) is an
    order-0 (Riesz) operator on the source; this is verified spectrally (|t_hat_ij| = |k_i k_j / k^2| delta_hat).
  - L4: on a 1D periodic leaf with a smoothed switch, the adjoint gradient matches finite differences to 1e-5 and the
    translation Noether sum vanishes to 1e-8.
  - **Well-posedness (scored in (c)):** the matter potential dE/drho = K(f' P L_M), where P = dR/dt and K is order 0.
    For a sharp H, f' is a surface delta. The local part of K on a surface with normal n_s is n_s n_s, so dE/drho
    contains a surface-delta layer of coefficient c_d = n_s.P.n_s.
    - If c_d = 0: finite potential jump only (the CFG353 class). Bounded.
    - If c_d != 0: sup |dE/drho| ∝ 1/w as the width w -> 0. Unbounded; the sharp switch is ill-posed.
    - Shown numerically on a spherical layer (T1/T3: tangential P, jump stays finite; T2: radial P, grows as 1/w) and
      on the 1D leaf (P = n n, grows as 1/w).
- **(a) FRW / linear:** PASS iff
  - (i) FRW is OFF; and
  - (ii) in CFG353's linear Lambda-CDM Gaussian field (EH no-wiggle, sigma_8 0.81, D(z) at z = 0, 1, 3, 10, 1000;
    Gaussian smoothing R = 8, 20, 50 h^-1 Mpc; thresholds as CFG353: Delta_ta(0) at z = 0, Delta_ta(1) at z = 1,
    EdS above) the ON volume fraction is < 1e-6 everywhere; and
  - (iii) the UNSMOOTHED field (grid cutoff k <= 50 Mpc^-1, stated) at z = 1000 has ON fraction < 1e-6.
  - Method: t is a Gaussian symmetric tensor, <t_ij t_kl> = sigma^2/15 (d_ij d_kl + d_ik d_jl + d_il d_jk); grad psi
    is independent of t at a point (parity). Monte Carlo with 4e6 samples, OR the rigorous bound
    l2 >= tau => |t|_F^2 >= 2 tau^2, P <= P(chi2_6 >= 6 tau^2 / sigma^2). This bound also covers T2 and T3.
  - Reported, not scored: unsmoothed at z = 10, 3, 0 (those scales are nonlinear, real collapse), and the reference
    fraction P(delta_lin >= 1.062).
- **(a') unbound sheets and filaments:** CFG353's compensated cells (planes delta_w 0.5, 1, 2, 3; cylinders delta_f
  1, 2, 5, 10; cell ratio 3, 5, 10; delta_v < -1 excluded), EdS threshold scored, z = 0 threshold reported. PASS iff
  the ON fraction is 0 in all cells. False-ON fractions and max R/tau are tabulated.
  - Reported (not scored): finite uniform prolate filaments and oblate sheets (aspect 5, 10; delta 1-10; Ferrers
    interior tidal tensor l_i = delta A_i / 2), with the ON volume fraction per rule.
- **(b) bound hosts (CFG347's 24: z 0.25/1/2.5/4, M_b 1e10/1e11/1e12, both footings, DE12 NFW + CFG353's EdS
  self-similar exterior scaled to Delta_ta):**
  - External field: the linear LSS at the host, uniform over the host. Tidal tensor sigma_delta(2 r_L) with
    CFG353's smoothing (2x the comoving Lagrangian radius of M_ta, IR cut H0/c). For T3 also the gradient (CFG353's
    s1). 2000 realisations.
  - PASS iff, on 24/24, the rule is ON at 30 kpc with probability >= 0.99, AND a 10% gas compression at 30 kpc
    (CFG353's bound) does not flip it.
  - Reported: |t_ext| / tau at r_ta and g_ext / g_host at r_ta.
- **(c) edge:** PASS iff
  - the median edge (outermost radius continuously ON from 30 kpc) satisfies |r_e - r_ta| <= 100 kpc on 24/24, AND
  - the switch is well-posed: sharp-H layer coefficient c_d = 0 at the edge, to 1e-8, over the realisations.
  - If only the c_d condition fails, the rule may be re-scored with one declared constant, a smooth-switch width
    eps (n = 1). Set eps by V_b / V_c^2 <= 1, with V_b / V_c^2 ≈ c_d (g_ph/g)^2 Delta / (6 eps) and the bound
    (g_ph/g) <= 1, giving eps_min = c_d Delta / 6. The resulting edge smearing ~ eps / (2 tau) r_ta is reported.
- **(d) data:** the CFG352/CFG353 harness copied with scoring unchanged. Rows: control 1.0; then each rule's median
  edge fraction on the KiDS-like lens bins (z 0.25, isothermal law mass, the same external field). Rows at the min
  and the max over bins. PASS iff KiDS d chi2 <= +9 on both footings, plus SPARC A3 and growth, at both rows.

## 3. Verdict (primary T3; T1, T2 reported with the same lines)
- SWITCH DOES BOTH: L, a, a', b, c, d all pass with 0 fitted constants.
- WITH COST: all pass with n >= 1 (e.g. the width eps).
- PARTIAL: at most one failure.
- NO-GO: two or more failures. State the obstruction and certify it in Lean if it is a theorem.
- Constants: Delta_ta is derived. Any switch smoothing or width counts as a constant. The LSS smoothing at 2 r_L is
  a model of the environment, not a switch constant.

## 4. Controls
- K1: point mass and uniform sphere (inside and outside). The numerical l_t equals (4 pi G/3) rho_enc to 1e-10, and
  T1 = T3 = l_t.
- K2: infinite cylinder (inside (d/2, d/2, 0), outside (a, 0, -a)) and plane ((d, 0, 0)). Analytic eigenvalues are
  checked numerically from finite-difference Hessians; each rule's response is tabulated.
- K3: FRW OFF.
- K4: Delta_ta vs CFG4_switch.
- MUTATE (CFG354_MUTATE=1, outputs *_MUTATE): replace the tidal reader by the potential reader (CFG353's E0). It
  must reproduce CFG353's failure: the (a) linear ON fraction at R8 z0 and the (a') E0 cell fractions equal
  CFG353's JSON values (to 1e-12 in fraction, same RNG); the run exits 1.

## 5. Lean (Lean 4 + Mathlib, no sorry)
- Sphere identity g/r = GM/r^3 = (4 pi G/3) rho_enc, and trace = 4 pi G rho.
- Middle-of-three and min-of-three responses for the cylinder (inside and outside), plane and sphere triples.
- T3 eigenvalue-only no-go (i).
- Monotone-rule no-go: a monotone rule ON at a host edge (tau, tau, l_r < 0) is ON in a filament (c, c, 0), c >= tau.
- Filament firing threshold 2(9 pi^2/16 - 1)/3 > 3.
- FRW off.
- Frobenius bound l1 >= l2 >= tau > 0 => sum l^2 >= 2 tau^2.
- Layer inequality: a profile of integral A on width w has sup >= A/w (unbounded as w -> 0).
- c_d = (n.e)^2 = 0 iff n ⊥ e.
