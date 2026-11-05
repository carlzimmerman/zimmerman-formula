# Single-clock exact-density candidate: next discriminating calculation

Continuation of CONTRACT.md route 3 after its two-clock obstruction. New
candidate, not an adopted replacement for v3s. No coefficient derivation.
Written before its algebra/numerical script. Read-only base: AC2 ACTION.md.

Take c=1, X=-grad(phi)^2/2>0, n=-grad(phi)/sqrt(2X), K=4 pi G,
M^2=1/(8 pi G). Use AC2's action with its smooth unswitched stiffness but
replace a0(phi)^2=xi G V by a0(X,phi)^2=b [X+V(phi)], b>0.
The density on the RHS is the canonical scalar's bare rest-frame energy,
not the total interacting polarization-plus-scalar energy. This distinction
must remain explicit. The tie is imposed; b remains free. Changes to that
definition are separate candidates.

The scalar itself supplies the clock. In unitary gauge phi=phi_bar(t),
X=phidot_bar^2/(2N^2), A_i=partial_i log N, so a0 depends on N without
introducing Ndot. Check whether coupling matter introduces a cosmological
kinetic obstruction before attempting charged backgrounds.

## Exact test

Flat FRW background, P=0, H>0, canonical clock kinetic q^2/2>0. Add a
minimally coupled, shift-symmetric matter scalar psi with L=F(Y),
Y=-grad(psi)^2/2, background psidot=v>0. Write F0,F1=F_Y,F2=F_YY,
Rm=F1+v^2 F2>0, F1>0. No actual radiation, baryon or CMB fit claimed.
The sound speed F1/Rm may approach zero from above, but an exact dust
constraint action is outside this finite-Rm calculation.

Use planar perturbations zeta=Z cos(kx), delta psi=C cos(kx), lapse alpha,
scalar shift B. Expand ADM Einstein action and scalar/matter actions to
second order. Integrate out longitudinal P on the homogeneous background;
its induced term is M^2 cY k_phys^2 alpha^2, cY=1/(1+Lstar^2 k_phys^2/2).
Reconstruct Y including shift times spatial matter gradient. Use Friedmann
to eliminate the clock potential only as a background relation. Solve lapse
and shift constraints; obtain the Hessian in (Zdot,Cdot). Check exact
determinant, symmetry, P-decoupled limit, matter momentum in shift constraint,
and whether a0/b can enter at quadratic order. No gradient, causality,
constraint-rank or full health inference from positive kinetic coefficients.

Finite fixtures M=H=a_FRW=1; clock epsilon=.05,.5; v=.1,1;
F1=1; matter sound speed squared=1,1/3,1/10000; cY=0,1/2,1;
k=1,100. Total 72 cases. 40/80-digit direct matrix Hessian versus symbolic
formula <=1e-30. Mutation reverses the induced lapse-gradient sign and must
violate the intended positive kinetic check on at least one frozen fixture,
with separate output and nonzero exit. No scan selects b.

General degree count: the nonlinear a0 dependence starts at |P|^3,
including its lapse dependence. No statement about cubic strong coupling
or physical inhomogeneous backgrounds is made by the FRW test.
