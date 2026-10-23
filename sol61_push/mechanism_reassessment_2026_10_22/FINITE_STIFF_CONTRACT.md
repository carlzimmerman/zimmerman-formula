# Finite-stiffness extension, before computation

The gamma0 finite-distribution scan completed. In the same identity model, gradient energy gamma(divP)²/2 equals gamma rho²/2 (negligible background). It adds gamma rho to the medium chemical potential. Keeping the same f(Q), write rho=A Psi^(5/2)/(1+r²/ra²) and solve

 (1+gamma rho_Psi) Psi'=R-gNb-gamma (partial rho/partial r)_Psi.

The denominator is positive. This incorporates stiffness self-consistently rather than applying a chosen density after solving. Test A10,Psi_c0.5, ra0.5,1,3 and dimensionless gamma0.0001,0.01,0.1; rerun the same mass, confinement and refinement checks. Include native cold-law comparisons only as model diagnostics, not data verdicts. The momentum equation includes the stiffness force; the kinetic Jeans identity itself remains p_r'+2 beta p_r/r=rho Psi'. No stability or formation claim. The gamma0 evidence and scripts are preserved unchanged.
