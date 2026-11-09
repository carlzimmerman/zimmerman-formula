# BI1 AMENDMENT A2: carrier (iii) as explicitly specified by the source (round 25) (committed alone, before any number under it)

Criteria 91e81dcd76; A1 f661cc7517 (carrier (iii) generic: FAIL); result 2c8af48c67. Adopts nothing. kappa = 1/2 FITTED; not theory
closed. Every number of the source is checked, none adopted.

## The specification, as relayed

**Gravity Lagrangian.** L = -(1/8 pi G)|grad Phi - f grad Phi_chi - grad Phi_Q|^2 - (1/8 pi G)|grad Phi_chi|^2 - rho_b Phi - rho_chi Phi_chi.
- grad Phi_Q = S_Q (nu(|grad Phi_b| / a0) - 1) grad Phi_b, with lap Phi_b = 4 pi G rho_b.

**Switch variable.** Xi = Psi_kin + (H / H0)^3 / (1 + Psi_coll^2).
- (-R_W^2 lap + 1) Psi_kin = rho_chi sigma^2 / (rho_ref v_stiff^2).
- (-R_0^2 lap + 1) Psi_coll = rho_b,coll / rho_b,crit.
- R_W = v_stiff / (2 H0); R_0 = 2 R_W.

**Couplings.** S_Q = 1 / (1 + Xi^2); f = [Xi^2 / (1 + Xi^2)][1/sqrt 2 + (1 - 1/sqrt 2) / (1 + Psi_coll^2)]; rho_ref = 200 Omega_chi rho_crit.
- rho_b,crit is given for M_b,min 1e9 and then changed to 1e8 in the same answer: recorded.

## Checks (B0(iii)-explicit; A1's line: PASS iff conserved and ghost-free with local fields AND the reaction force <= 1e-3 of the law's g)

1. **sympy:** the Euler-Lagrange equations of L against the source's claimed field equations. Any extra term where grad f is not
   zero is reported. The quadratic form (ghost) is checked, along with the effective baryon-baryon, baryon-component and
   component-component couplings for constant f.
2. **Conservation with the Helmholtz fields given an action** (coupling mu_0). Does the reaction force on rho_chi depend on mu_0?
   Is there a mu_0 that escapes both horns (force vs momentum violation)? This is stated from the field equations (static Noether
   identity), with the reaction force density = (dL/df)(df/dXi) grad Xi landing on the matter that sources Xi.
3. **Numbers in SI and in the record's a0 (both footings), beside a0 = 1.2e-10.**
   - The source's a_extra = (1/(4 pi G))(df/dXi) g_N,b g_N,chi (dXi/d rho_chi) / R for an L* galaxy at 250 kpc (claimed 4.6e-12,
     0.038 a0).
   - The same for a group at its 400 kpc boundary (claimed 2.6e-9, "21 a0"); SS1 primary halos; M_b,sys 5e12 for the group.
   - dXi/d rho_chi both unsmoothed (an upper bound) and with the Yukawa point response l^2 / (2 R_W^2), l the system scale.
   - R = R_W. The ratio to the law's g at the same radius.
4. **Reported, not graded:** the source's web unscreened fraction (12.5 %, sigma8 +6.5 %) and its proposed kill test (small spirals
   1.8-2.4 Mpc from rich clusters).

**Label.** Folds all three carriers: FAIL at B0 if (iii)-explicit fails the A1 line too.
