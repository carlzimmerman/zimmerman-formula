# Actual dust/Weyl perturbation closure on the charged mixed background

The retained nonminimal complex-carrier action admits a closed, constraint-preserving linear scalar system with ordinary dust and ideal radiation on its audited mixed background. It requires independent carrier perturbations and radiation variables. A carrier phase-velocity perturbation changes the Weyl potential for unchanged initial dust perturbations. This does not prevent computing transfer once full initial data are supplied; it prevents obtaining the physical transfer from a dust-only EdS surrogate or a switch-OFF test.

## Direct continuation of the actual Claude gap
Read-only inspection of CFG355 README, frozen criteria, main script and edge harness finds its `score_G` tests linear switch inactivity and a finite-radius gate tail. It does not evolve the carrier, dust and radiation perturbation equations. The reported growth pass is therefore evidence about gate leakage within that harness, not a demonstrated dust/Weyl transfer function of the coupled carrier action. The rank/tidal rule's linear-OFF property does not eliminate a nonminimal carrier's independent stress or charge perturbations.

This child varies the actual retained curvature-carrier+dust+radiation action used by `self_consistent_history`, not the full CFG355 Vlasov/rank/leaf-constraint action. If a smooth MOND gate is exactly OFF with zero first variation, its interaction drops out locally; any additional switch/constraint stress still requires its own variation. No imported gate legality, likelihood or global cold-formation claim is made. Claude scripts were neither executed nor edited; their inspected hashes are recorded separately.

## Declared action, background and gauge
Use four-dimensional units with c=1,

S=integral sqrt(−g)[M R/2−partial_mu chi* partial^mu chi−xi R|chi|^2]+S_d+S_r.

M>0; the background has F=M−2xi f>0, f=|chi|^2, q=chidot, E=|q|^2, Fdot=−4xi Re(chi* q), B=F+12xi^2 f. Its actual constraint and geometric trace closure are

3F H^2+3Fdot H=rho_d+rho_r+E,
B R=rho_d+2(6xi−1)E,
R=6(Hdot+2H^2).

Dust and radiation are separately conserved, rho_d proportional to a^−3 and rho_r to a^−4. The charge Q=a^3 Im(chi* q) is conserved by the same action. No material mass is assigned to Q and no particle identity is inferred. Here dust is an explicitly supplied ordinary pressureless species, not the carrier relabeled as dust.

For k>0 use the completely fixed scalar Newton gauge

ds^2=−(1+2Psi)dt^2+a^2(1−2Phi)delta_ij dx^i dx^j.

Phi/Psi are Bardeen potentials and all matter perturbations below are their Newton-gauge gauge-invariant completions. Define u_i=partial_i v for each fluid, delta_d=delta rho_d/rho_d, delta_r=delta rho_r/rho_r, p^2=k^2/a^2, and W=(Phi+Psi)/2. The dust rest-frame perturbation is Delta_d=delta_d−3H v_d. Ordinary radiation is an ideal barotropic fluid with delta p_r=delta rho_r/3 and zero scalar anisotropic stress. These assumptions do not represent free-streaming photons, photon polarization, baryon drag, thermal distributions or recombination rates.

Let

delta f=2Re(chi* delta chi), delta F=−2xi delta f,
delta Fdot=−4xi Re(q* delta chi+chi* delta chidot),
delta E=2Re(q* delta chidot)−2Psi E,
delta rho=rho_d delta_d+rho_r delta_r+delta E,
delta mathfrak q=rho_d v_d+(4rho_r/3)v_r−2Re(q* delta chi).

Operationally delta T^0_i=partial_i delta mathfrak q for the canonical carrier plus ordinary fluids. All nonminimal derivative stress is retained on the metric side, not discarded as an effective phantom density.

## Exact constraints and a non-dust Weyl source
The traceless spatial, mixed momentum and mixed00 metric variations give, respectively,

F(Phi−Psi)=delta F,
2F Y=−delta mathfrak q+delta Fdot−H delta F−Fdot Psi, Y=Phidot+H Psi,
2F[p^2Phi+3HY]−3H^2delta F
 =−delta rho+p^2delta F+3H delta Fdot−3Fdot Phidot−6HFdot Psi.

The slip follows from the offdiagonal Hessian delta F. In the mixed00 row, variation of the spatial trace of covariant second derivatives contributes p^2delta F+3Hdelta Fdot−3Fdot Phidot−6HFdot Psi; it is not zero even when the carrier background looks approximately pressureless.

Eliminating momentum and slip yields the exact Weyl constraint

2F p^2 W=−delta rho+3H delta mathfrak q+6H^2delta F−3Fdot Y.

The +6H^2delta F is essential. This is not a Poisson law for ordinary dust alone. Carrier density, momentum, amplitude and metric derivative enter; radiation density/velocity also enter, despite its vanishing trace. A quasi-static or dust-only reduction needs a separate scale/initial-mode proof.

## Complete ideal-fluid evolution
The exact covariant trace can be written with X=partial_mu chi* partial^mu chi as B R=rho_d−2(6xi−1)X. On the homogeneous background X=−E and delta X=−delta E. Therefore

delta R=[rho_d delta_d+2(6xi−1)delta E+(6xi−1)R delta F]/B.

The metric Ricci perturbation must not be prescribed to vanish because radiation has trace zero. Direct Klein-Gordon variation gives

delta chiddot+3Hdelta chidot+(p^2+xi R)delta chi
 =q(Psidot+3Phidot)−2xi Rchi Psi−xi chi delta R.

The fluid continuity and Euler equations in the stated covariant-velocity convention are

d(delta_d)/dt=3Phidot+p^2 v_d, d(v_d)/dt=−Psi,
d(delta_r)/dt=4Phidot+(4/3)p^2 v_r,
d(v_r)/dt=H v_r−Psi−delta_r/4.


Slip fixes Psi; momentum fixes Phidot; differentiating slip supplies Psidot using delta Fdot. Together with the two real KG equations, this gives a first-order system for nine variables

(Re delta chi, Im delta chi, Re delta chidot, Im delta chidot, Phi, delta_d, v_d, delta_r, v_r).

The mixed00 row imposes one initial constraint, leaving eight scalar phase-space dimensions: two real carrier modes plus one dust and one ideal-radiation mode. No scalar metric degree of freedom is counted twice. A primordial transfer/power calculation needs a full initial mode vector or covariance and a choice of adiabatic/entropy preparation; the action does not fix these amplitudes.

## Exact sufficiency: constraint propagation, not only a sampled residual
Let mathcal E_mu nu=F G_mu nu−T_mu nu−nabla_mu nabla_nu F+g_mu nu box F be the metric residual. Build the evolution above with R_alg from the algebraic trace, provisionally distinct from geometric R_geo. Its KG equation gives box F=−4xi(X+xi R_alg f). Direct trace variation then yields

mathcal E^mu_mu=F(R_alg−R_geo).

Canonical stress divergence is xi R_alg partial_nu f=−R_alg partial_nu F/2. The metric derivative identity consequently gives

nabla_mu mathcal E^mu_nu=(partial_nu F/2)(R_alg−R_geo).

At linear order on a homogeneous background the spatial right side vanishes. Momentum and traceless spatial rows are imposed, so for k>0 the spatial identity forces the remaining isotropic pressure residual P=0. Let C=delta mathcal E^0_0, with exactly the mixed00 residual sign in growth.py. The trace is then C and the temporal divergence is Cdot+3HC. Thus

Cdot=[−3H+Fdot/(2F)]C.

Equivalently, before using P=0 the temporal divergence is Cdot+3H(C−P), with trace C+3P. Constraint-compatible initial data preserve C=0; for F nonzero this also forces R_alg=R_geo, proper scalar EL and every scalar metric row. This supplies an actual exact closure, not merely nine equations with a monitored but unexplained Hamiltonian residual. It excludes k=0 and the F=0 tensor boundary analyzed separately. The finite examples remain safely F>0.

## Charge transport and a sharp independent-seed witness
Write L=Im(chi* q)=Q/a^3. Direct current conservation gives the Newton-gauge coordinate-volume charge perturbation and transport

delta mathcal Q=a^3[delta L−L(Psi+3Phi)],
delta mathcal Qdot+a k^2 Im(chi* delta chi)=0,
delta L=Im(delta chi* q+chi* delta chidot).

The charge disturbance has its own phase transport; conservation is not an algebraic dust-density closure. A nonzero Fourier charge perturbation has zero spatial mean, so it need not change the background total Q.

At an admissible initial point take delta chi=0, delta chidot=i chi omega, and zero initial ordinary dust/radiation density and velocity perturbations. The seed omega is a free phase-velocity perturbation, not the background rotation frequency. Then delta F=delta Fdot=delta mathfrak q=0, but

delta rho=2L omega−2Psi E.

Slip gives Phi=Psi and momentum gives Y=−Fdot Psi/(2F). The exact Weyl constraint requires

Phi=Psi=−2L omega/[2F p^2−2E−3Fdot^2/(2F)].

For Q omega nonzero and a nonzero denominator this is a distinct nonzero Weyl potential at the same zero initial dust perturbation. Choosing p^2>E/F+3Fdot^2/(4F^2) makes the denominator positive in this selected initial-data chart. A zero denominator is not by itself a physical singularity or kinetic-health condition: one can choose another constraint datum, for example solve for delta_d when rho_d>0. The seed is a local phase-velocity/charge-density variation, not a constant global U(1) rotation. Its initial charge-density disturbance is delta mathcal Q=a^3[f omega−4Psi L], including the metric volume/lapse perturbation, rather than just a^3 f omega. Its amplitude can be arbitrarily small. This is an exact initial-data obstruction to assigning W from dust data alone, not a no-go against solving the now-closed system once all seeds are supplied.

## Bounded finite transfer columns
The checks use the parent's actual initial family M=1, a=1, rho_d=4/3, rho_r=.01rho_d, S=.4, xi=100 or1000. Set fixed comoving k=10H_initial. Two normalized basis seeds are tested: the phase-velocity seed omega=H_initial with all ordinary perturbations initially zero, and a dust-density seed delta_d=1 with the other matter coordinates zero. Both solve the actual initial Hamiltonian constraint. These are unit transfer columns, not observed amplitudes or pure growing/adiabatic modes; multiplying a column by an arbitrarily small epsilon makes a physical linear perturbation.

DOP853 and Radau separately evolve each seed from a=1 to2, at rtol1e−9/atol1e−12 and41 common sample points. Each path has a declared 20000-evaluation check and standard execution caps. No early radiation era, F-guard extension, parameter survey or recombination calculation is attempted. Development values (authoritative runs are separate) are:

| xi | seed | W(a=1) | W(a=2) | Delta_d(a=2) |
|---|---|---:|---:|---:|
|100|phase|−8.61793e−7|+1.96065e−6|−2.22974e−4|
|1000|phase|−2.72504e−8|+1.11661e−7|−1.67864e−5|
|100|dust|−.0148665|−.0100447|1.35795|
|1000|dust|−.0148530|−.00995879|1.34252|

The independent phase seed generates dust response and time-dependent Weyl behavior; neither identifies the carrier as material CDM nor supplies a unique power spectrum. The unit dust column is not expected to equal a pure EdS growing mode because its initial velocity and other species seeds were specified differently. Background and perturbation constraints, exact current transport, common-vector solver comparisons and deliberate wrong closures are the relevant checks.

## What is still needed for physical recombination/structure predictions
The ideal-fluid system supplies a reproducible action-consistent transfer algorithm on a specified admitted background interval. Observational inference still needs a viable early-to-late background avoiding or completing its F boundary, justified primordial mode preparation, actual baryon-photon coupling/ionization/thermal evolution and photon angular/polarization transport. Nonzero radiation anisotropic stress would modify slip and require additional transport variables. A cold-sector abundance and pressure/phase identity do not follow from gate inactivity, F positivity, a conserved global charge or these two transfer columns.

This closes a concrete mathematical transfer-closure gap while preserving those physical gaps. There is no measured growth likelihood, CMB success, particle/no-particle identity proof, vacuum coefficient selector or world novelty claim.
