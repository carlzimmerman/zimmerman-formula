# CDE-L4C MOND (Cuscuton Dark-Energy + Laplacian 4-Constraint MOND) — structural gates: ALL PASS (2026-09-01)

**Provisional strict-2-DOF horse. Architecture: Einstein tensor sector + cuscuton DE (constraint-like scalar,
no propagating DOF) + four Laplacian second-class scalar auxiliary constraints (Yao-Oliosi-Gao-Mukohyama
arXiv:2302.02090; Laplacian zero-mode trick arXiv:2607.26031) + exponential-MOND in the lapse-gradient sector
+ minimally-coupled matter. Verdict = OPEN (structurally coherent; the decisive Dirac/PPN gates are owed).**

Script: `cde_l4c_structural_gate.py` (rc=0, every check can fail). Division of labor:
Einstein -> 2 tensor waves + Newtonian baseline; 4-AC -> remove scalar graviton; C_slip=3R-4D^2 lnN -> Phi=Psi;
F(y) -> mu=1-e^{-y}; cuscuton chi -> rho_DE(t); V(chi) -> a0(t).

## Structural gates (ALL PASS)
1. **F(y) correction (no Newtonian double-counting).** Einstein already supplies the y^2 Newtonian stiffness,
   so the MOND term ADDS F with (y^2+F)'/(2y)=mu, i.e. **F'(y)=-2y e^{-y}, F(y)=2(1+y)e^{-y}+C**, and
   1+F'/(2y)=1-e^{-y}=mu EXACTLY. Deep MOND: the y^2 CANCELS, leaving (2/3)y^3 (cubic AQUAL, |gradPhi|^3).
   GR recovery: F'(y)->0 exponentially. [The earlier version adding the full G(y) on top of Einstein
   double-counted y^2 -- corrected here.]
2. **Velocity-freeness.** y = c^2|D_i lnN|/a0(chi) has NO time derivative (spatial gradient of lnN + algebraic
   chi), so a0^2(chi)F(y) contributes 0 to the kinetic Hessian: it cannot add a scalar graviton or a chi-kinetic term.
3. **Cuscuton non-dynamical under a0(chi).** Cuscuton momentum is bounded as chidot->oo (primary constraint);
   a0(chi) is algebraic (no chidot), adds no chidot^2. The degeneracy that removes the scalar survives.
4. **No-slip weak field.** C_slip = 3R - 4 D^2 lnN -> (4/c^2) nabla^2(Psi-Phi) (3R=(4/c^2)nabla^2 Psi verified);
   D^2 C_slip=0 gives Phi=Psi for k!=0; on FLRW (Psi=Phi=0, D_iN=0) C_slip=0 automatically -> does NOT freeze H.
5. **a0 promotion.** a0^2(chi)=G V(chi)/4 -> a0=(1/2)c sqrt(G rho_Lambda)=c^2 sqrt(Lambda/32pi) when V=rho_L c^2;
   a0(z) proportional to sqrt(rho_DE(z)), NOT forced to H(z) unless rho_DE~H^2. The a0<->Lambda relation is now a
   field-dependent constitutive relation, not pasted on.

## Owed (NOT-COMPUTED, flagged honestly -- the decisive gates)
- **Gate A**: the full 4x4 Dirac matrix Delta_AB={C_A,C_B} with INVERSE-DESIGNED C_2,3,4 (do NOT guess them):
  rank 4, N_grav=2, on k!=0 while keeping BOTH Phi and Psi nonzero (the exact place the 2026 Laplacian-MMG
  example fails -- its own constraints force Phi=Psi=0 on k!=0). Combined Hessian with cuscuton+4AC+a0(chi) live.
- **Gate B**: MOND + no-slip from the full field equations (multipliers solved, not assumed zero).
- **Gate C**: boosted PPN alpha_1, alpha_2, alpha_3.
- **PREDICTION (to test, not assume)**: preferred-foliation + elliptic (Laplacian) k!=0 constraint => alpha_3
  is the likely killer (the DC-019/York instantaneity wall). The Laplacian trick fixes the FLRW zero mode, not
  the instantaneity of the k!=0 constraint. If Gate A/B pass and Gate C gives alpha_3=O(1), the horse dies there.

STATUS: the cleanest structurally-coherent strict-2-DOF chassis to date; the make-or-break Dirac closure (Gate A)
is the next single job.
