# Reciprocal field continuation: pre-run contract

User request: continue the reciprocal field action with dynamical baryons; test growth, rotation curves and dwarf/cluster excess. Base 581d52210bced1231c2517b1d894221edd171f40; predecessor PC-2026-10-22-1 in parent_compliance_2026_10_22. New files only in this directory. No parameter fitting, external downloads or heavy simulation. No AGENTS.md or .mathbox ledger found. Preserve other active work.

The exact target remains one physical parent and a derived excess mechanism. This checkpoint tests a necessary nonrelativistic limit first. A failure there is not a no-go for every covariant theory. No prior shear result transfers.

## Declared reduced action

Conserved baryon and cold material currents with densities rho_b,rho_c and velocities v_b,v_c. Baryon internal energy U_b(rho_b) is optional for the circular cold-disc diagnostic; its pressure is retained symbolically. K=4piG, e=rho_c-rhobar-div P, chi>0, chi0>0. Lagrangian density:

 L = rho_b v_b^2/2 + rho_c v_c^2/2 - U_b(rho_b)
     -|grad Phi|^2/(2K) -(rho_b+rho_c)Phi
     +eta |dot P|^2/2 -W(K|P|) -e^2/(2chi)
     +MX |dot X|^2/2 -DX |grad X|^2/2 -chi |X|^2/2
     +Mchi dot chi^2/2 -Dchi |grad chi|^2/2
     -mu^2(chi-chi0)^2/2 +g X.curl v_b.

All displayed kinetic and gradient coefficients are positive, g is real and constant. Dots are in the chosen preferred Newtonian frame. Fluid variations must be material-current variations, not independent unconstrained velocity variations. W is the predecessor's logarithmic potential. No P spatial stiffness is included in this candidate; a later addition changes the static test. Gravity couples once to each density. These parameters are new model inputs, not derived constants. An expanding-background implementation is only a subhorizon EdS diagnostic, not a covariant completion.

## Checks and discriminators before execution

1. Derive reciprocal baryon momentum and circular radial force using fluid variations. Validate rigid rotation, zero vorticity and a flat curve; do not reuse the one-coordinate toy inertia as a field result.
2. Derive the transverse mediator spectrum with baryons dynamical, and show exactly whether the coupling appears in the linear scalar growing sector about P=X=0, chi=chi0. Check the characteristic-speed dependence on baryon density.
3. Integrate the inherited two-fluid quasistatic EdS equations from z=1100 to 0 at k=.01,.1,1/Mpc for the predecessor's .440422-kpc and 133.787-kpc illustrative lengths. This is not an observational likelihood. Repeat with tighter tolerance; compare to dust and the frozen-growth limiting equations.
4. For the stationary spherical nonrotating branch X=0 and regular centre, retain the P equation as well as cold chemical equilibrium. Write h=mu_c-Phi and e=chi h. With chi>=chi0, test a bound on the first zero of positive h. An enthalpy-only polytrope with P set to zero is not admissible unless it also solves the P equation.
5. Dimensionless radial checks: x=r/ell0, ell0=(K chi0)^(-1/2), s=h/(a0 ell0), Q=x^2 q(g/a0), q(y)=y^2/(1+y). In the local scalar equilibrium limit chi/chi0=1+lambda s^2, integrate Q'=x^2[B(x)+s+lambda s^3], s'=-(Q/x^2+sqrt((Q/x^2)^2+4Q/x^2))/2. Test s(0)=.01,.1,1,10,100, lambda=0,1, and B=0 or a declared Plummer source (dimensionless mass=1, scale=1). These are finite checks of a proposed analytic bound, not galaxies or a parameter fit.
6. Exact algebra tolerance zero; ODE event radii repeat within 1e-5 relative; illustrative growth repeat within 1e-7 absolute. Deliberate coupling-sign/force-omission and radial-sign controls must be detected.

Scope restrictions: a positive excess-density region is not automatically the whole cold halo. Compact surplus mass can lens at large radius; a radius bound alone is not a cluster-lensing likelihood. No predicted mass, capture, initial condition or retention claim without its conserved inventory. Self-review only. Per run <=60 seconds, single numerical-library thread, no dependency installation.
