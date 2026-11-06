# PF06: constrained planar dynamics

Scalar-clock gauge phi=s t, s>0. Metric
 ds^2=-N^2dt^2+e^(2lambda)(dx+w dt)^2+e^(2beta)(dy^2+dz^2).
P is the proper spatial polarization magnitude. Let V3=e^(lambda+2beta),
D=e^-lambda(P_x+2P beta_x), X=s^2/(2N^2). The on-branch matter F is as in
JUNCTION_RESULT.md. F_D=-1-gamma(D+2X), F_X=1-2gamma D.

After spatial integration by parts,

    L_G=Mpl^2 N V3[-2 Kx Ky-Ky^2
                     +e^-2lambda(2 N_x beta_x/N+beta_x^2)],
    Kx=(lambda_t-w lambda_x-w_x)/N,
    Ky=(beta_t-w beta_x)/N.

The canonical momenta and kinetic Hamiltonian density are

    p_lambda=-2Mpl^2 V3 Ky,
    p_beta=-2Mpl^2 V3(Kx+Ky),
    h_K=(p_lambda^2-2p_lambda p_beta)/(4Mpl^2 V3).

The constraints retained before spatial gauge fixing are

    p_lambda,x-lambda_x p_lambda-beta_x p_beta=0,
    h_K+Mpl^2 e^(-lambda+2beta)
          (2beta_xx-2lambda_x beta_x+3beta_x^2)=V3(F-2X F_X),
    (N F_D)_x=-N e^lambda W_P.

The last is the native polarization equation, not an imposed smoothing rule.
For the on-branch, F-2XF_X=-D-X-V-W-gamma D^2/2+2gamma D X.
The exact W used in the fixture is
 W=a0^2/K[-r-log(1-r)], r=K|P|/a0<1,
 W_P=K P/(1-r), W_PP=K/(1-r)^2.

## Evolution in spatially uniform lambda gauge

Set lambda_x=0 but evolve its spatially constant value. Choose lambda_t as the
spatial mean of N(p_lambda-p_beta)/(2Mpl^2 V3), and obtain zero-mean w from
 w_x=lambda_t-N(p_lambda-p_beta)/(2Mpl^2 V3).
Then

    beta_t=-N p_lambda/(2Mpl^2 V3)+w beta_x,
    p_lambda,t=N h_K+N V3(F-F_D D)-L_sp+(w p_lambda)_x,
    p_beta,t=2N h_K+2N V3 F+2L_sp
      -partial_x[2Mpl^2 e^(-lambda+2beta)(N_x+N beta_x)
                   +2N e^(2beta)P F_D]+(w p_beta)_x,
    L_sp=Mpl^2 e^(-lambda+2beta)(2N_x beta_x+N beta_x^2).

At each stage, solve the Hamiltonian and polarization constraints for N,P.
Momentum remains an independent residual. The current implementation is a
pre-break numerical experiment; it must NOT be used beyond its demonstrated
space/time convergence or interpreted as a weak continuation.

## Constraint-satisfying initial family

At lambda=beta=0 choose P=(A/k)sin(kx), D=A cos(kx), p_lambda=-2Mpl^2 H0,
H0^2=(s^2/2+V)/(3Mpl^2). Momentum is identically satisfied. Let z=cos(kx),
eta=K A/(k a0), and Z=N(1+gamma A z)+gamma s^2/N.
The polarization equation becomes

    dZ/dz=-N K A/[k^2(1-eta sqrt(1-z^2))].

Set N(z=1)=1 and choose the positive lapse branch continuously connected to it:

    N=[Z+sqrt(Z^2-4gamma s^2(1+gamma A z))]/[2(1+gamma A z)].

Integrate the rescaled Z increment to avoid subtracting nearly equal constants.
Set X=s^2/(2N^2) and solve the Hamiltonian algebraically for p_beta:

    p_beta=p_lambda/2-(2Mpl^2/p_lambda)(F-2XF_X).

This is an exact construction at the equation level, with numerical integration
of the one-dimensional lapse ODE. The fixture in ADM_CONTRACT.md stays in X>0,
q=D+2X>0 and far inside the flux cap. Grids 256–2048 give monotonically decreasing
polarization residual, down to about 1.57e-6 relative; Hamiltonian residual is
below 6e-18 and momentum is identically zero. Tightening the ODE tolerance
changes N by less than 1e-9. These are dimensionless test parameters, not adopted
physical values or new canonical/alternative-footing grades.

## Validation and limits

The homogeneous constant-V scalar solution in scalar time is

    y=e^-3beta=sqrt(2V/s^2) sinh[asinh(sqrt(s^2/(2V)))
                                  -sqrt(3s^2/(2Mpl^2)) t],
    N=1/y, lambda=beta, p_lambda=-2Mpl^2 beta_t,
    p_beta=2p_lambda.

The centered-derivative implementation matches this at t=.1 to 9.4e-17;
its analytic elliptic Jacobian agrees with a directional finite difference to
1.6e-9 relative. These benchmarks do not validate nonlinear evolution by themselves.

The first initial-data run could not serialize a NumPy boolean; initial002
preserves the same computation with that output bug corrected. Both records
are retained. The first evolution code differentiated large constant backgrounds
with dense matrices; centering inputs fixes that cancellation (v2), without
changing the equations or adding viscosity. Further resolution tests are
necessary; consult live status rather than treating any stopped run as physics.
