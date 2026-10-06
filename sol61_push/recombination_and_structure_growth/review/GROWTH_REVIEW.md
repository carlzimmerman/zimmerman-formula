# Independent growth/identity audit

Primary verdict: **proved as written**, for the displayed restricted
pressureless common-force linear relative invariant, the EdS four-state
transfer and growing projection, and the constant-pressure single-velocity
stress identity. No actionable mathematical error was found. This verdict is
not a proof of a full acoustic transfer function, a cosmological likelihood,
cold creation/abundance, or nonlinear multistream equivalence.

## Normalized claims and raw reconstruction

The EdS transfer assumes linear perturbations, subhorizon Newtonian growth,
pressureless species after drag, identical force potentials, and conserved
constant mass fractions 0<f_b<1. Let N=ln a and x=a/a_d. Weighted common matter
and relative density are delta_m=f_c delta_c+f_b delta_b and
Delta=delta_b-delta_c. Adding and subtracting the two species' growth equations
then gives

    delta_m,NN + (1/2)delta_m,N -(3/2)delta_m=0,
    Delta_NN +(1/2)Delta_N=0.

Their characteristic roots are 1,-3/2 and 0,-1/2, respectively. Enforcing
all four independent initial data (u,v,w,z) at x=1 forces

    A=(3u+2v)/5, B=2(u-v)/5,
    delta_m=Ax+Bx^-3/2,
    Delta=w+2z(1-x^-1/2), Delta_N=z x^-1/2.

Independent SymPy reconstruction confirms both ODE residuals vanish and the
initial state is exactly (u,v,w,z). Species recovery
(delta_b,delta_c)=(delta_m+f_c Delta,delta_m-f_b Delta) follows by solving the
two definitions; it is not an assumption that their perturbations already
coincide.

The common transfer block has determinant x^-1/2: its equation has first-order
state trace -1/2. The relative block has the same determinant. Their direct
product has determinant x^-1, independently verified by direct Jacobian
calculation. Thus the finite-time four-state transfer is invertible. Its
asymptotic growing projection is not invertible and does not retain all four
modes: this is consistent with, rather than a contradiction of, the report's
finite-time statement.

The potential scales as a^2 rho_m delta_m proportional to delta_m/x, hence
A+B x^-5/2 in this matter-era model. The surviving amplitude depends on both
species' initial density and logarithmic derivative, with coefficients 3/5
and 2/5. Oscillatory initial baryon phases therefore can remain in the common
growing amplitude even after relative density becomes small. This is a
transfer-of-data statement, not a prediction of actual BAO amplitudes or phases.
A(k) can accidentally cancel for particular initial phases; the report does
not claim every mode necessarily produces a nonzero acoustic feature.

For the example cold density/derivative 1 and baryon density/derivative 0,
(u,v,w,z)=(f_c,f_c,-1,-1). Independent substitution gives exactly

    delta_b=f_c[x-3+2x^-1/2],
    delta_c=f_c x+f_b[3-2x^-1/2].

The script's catch-up ratio is delta_b/delta_c. Its deficit thresholds are
therefore baryon deficits *relative to the cold perturbation* in this chosen
shape, not a universal catch-up time or a recombination redshift. The report
keeps the EdS starting-state and illustrative-redshift qualifications. Scaling
both species' initial amplitudes arbitrarily small is needed for the whole
finite-x exercise to stay linear; the report makes that qualification.
The A=0 exception to density catch-up is explicitly retained.

## General expansion invariant and force/pressure departures

Use the stated conformal Newtonian-gauge dust equations

    delta_i'=-theta_i+3Phi',
    theta_i'=-Hcal theta_i+k^2 Psi.

For species sharing the same potential and continuity law, subtraction yields
Delta'=-Delta_theta and Delta_theta'=-Hcal Delta_theta. The metric terms
cancel without a Poisson/subhorizon approximation. Therefore

    U=a Delta'=a^2 Delta_dot=a^2 H Delta_N,
    U'=0, U_dot=0,
    Delta=Delta_d+U_d integral da/(a^3 H).

The report's general-H invariant, including the factors of a, is correct.
For two separately conserved dust backgrounds, their density-contrast gauge
shifts match, so the difference is gauge invariant at linear order. Separate
background exchange, pressure or modified continuity terms can invalidate
that statement and the derivation.

To check the source correction, define the conformal Euler difference source

    S=k^2(Psi_b-Psi_c)+c_b^2 k^2 delta_b-c_c^2 k^2 delta_c
      +Gamma_b(theta_gamma-theta_b).

Then Delta_theta'=-Hcal Delta_theta+S. Since U=-a Delta_theta,
U'=-a S and U_dot=U'/a=-S. This independently recovers all signs and scale-factor
factors in report equation (5). In particular there is no extra factor a
multiplying the displayed cosmic-time derivative. Gamma_b there is the
conformal drag coefficient; it would have a different expression if defined
in cosmic time. The report defines it consistently.

The pressure formula assumes continuity laws unchanged from the displayed
dust form. A general relativistic nonzero-pressure fluid has additional
continuity terms and does not obey equation (5) by simple Euler replacement.
The report explicitly warns about this limit. Linear Schrödinger quantum
pressure in its subhorizon nonrelativistic regime does retain the mass
continuity form and gives c_c^2=hbar^2 k^2/(4m^2a^2), yielding the displayed
positive cold contribution hbar^2 k^4 delta_c/(4m^2a^2) in U_dot. This is not
an all-scale relativistic scalar pressure formula.

The radiation-era logarithmic cold solution follows only after suppressing
its gravitational forcing, while the smooth-baryon EdS exponent follows from
p^2+p/2-3f_c/2=0. The report labels these approximations. Its tight-coupling
photon oscillator also checks directly: substituting
 theta=-(3/4)(delta_gamma'-4Phi') into the displayed shared Euler equation
produces equation (1), including its damping, forcing signs and equilibrium
-4(1+R_b)Psi for constant potentials/loading. No photon hierarchy or actual
drag epoch is solved here.

## Constant-pressure stress degeneracy

Starting with T^{mu nu}=(rho+p)u^mu u^nu+p g^{mu nu}, exact constant
p=-rho_Lambda gives

    T^{mu nu}=(rho-rho_Lambda)u^mu u^nu-rho_Lambda g^{mu nu}.

This is a tensor identity in every local frame, not just the single boosted
frame tested in code. Define rho_c=rho-rho_Lambda>=0. Metric compatibility and
spacetime-constant rho_Lambda make the vacuum divergence zero. Contracting
conservation of rho_c u^mu u^nu with u_nu gives
nabla_mu(rho_c u^mu)=0; its orthogonal projection gives
rho_c u^mu nabla_mu u^nu=0. Hence there is dust continuity and geodesic motion
where rho_c>0. At rho_c=0 the velocity is not fixed by stress conservation;
the report correctly restricts its dynamical assertion to positive density.

FRW conservation integrates to rho=rho_Lambda+C a^-3. C is an independent
integration constant. dp/drho=0 and delta p=0 require exactly constant pressure
throughout the admissible perturbed state, not merely a background pressure
fit. This accounts for the report's refusal to transfer the degeneracy to a
canonical scalar, an approximate oscillating scalar without residual bounds,
or nonminimal auxiliaries that separately detect the two variables.

A single u does not describe arbitrary intersecting collisionless streams;
multiple streams generally generate velocity dispersion/anisotropic stress.
The before-caustics limitation is essential and is stated. This exact stress
repackaging does not identify particles, select wave mass, or select cold
charge C from the vacuum value.

## Mutation and numerical evidence scope

The code's dropped-velocity mutation changes A to 3u/5 and B to 2u/5.
The resulting common solution still solves the ODE and has initial density u,
but its initial logarithmic derivative is 0, independent of v. Independent
calculation shows its four-state Jacobian determinant becomes 0. The named
initial-velocity and finite-time-invertibility checks therefore detect a real
loss of input data. An ODE residual alone would miss it. The separate positive
projection derivative check uses the unmutated closed-form expression; it does
not itself diagnose the mutant, but the two decisive checks do.

I did not execute the author's script or overwrite its outputs. Inspection
shows the five coupled ODE controls integrate the original two-species system
and compare against the analytic common/relative solution; this is an
appropriate orthogonal finite implementation check. Those five samples and
23-check count cannot establish the universal statements: the derivations
above establish their exact scoped claims. The finite tests do not supply
initial cosmological transfer functions or nonlinear evolution.

## Verdict, provenance and next implication

Passed: EdS four-mode formulas and determinant; growing density/velocity
projection; arbitrary-background dust relative invariant; force/pressure/drag
correction with unchanged continuity; constant-pressure tensor decomposition
and conservation consequence; mutation detects dropped velocity.

Conditional/out of scope: actual pressure/drag residuals through recombination,
real initial transfer functions, full Boltzmann spectra, massive-wave
relativistic extension, nonlinear caustic completion, abundance and microscopic
identity. No substantive wording repair is required by this audit.

Reviewed SHA256:

    checks.py: be56affaeb5da6f7242f843ed8ce73da9f6fbc412eb0a86492b3d9833ca3f650
    REPORT.md: 2b6292f75061fcc9dbacaa6490dc9d90b24ae4c35e86fbde6c46f8dbe47fb56c

Independent review used raw equation reconstruction and an inline exact
SymPy Jacobian/ODE/mutation calculation, writing only this review file.
External Ma-Bertschinger/Kunz authentication is not repeated here; the key
identities were derived directly from the equations and stress definition.
The remaining same-action implication is to derive the actual forces,
continuity and pressure terms, and initialize the invariant/transfer with
physical density **and velocity** data. This audit does not imply those inputs
have been supplied for candidate B or the assembled gravity action.
