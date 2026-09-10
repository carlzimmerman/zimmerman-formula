# Cubic interaction: full scalar principal response on homogeneous FLRW

This bounded action-level calculation uses the same P/W clock sector plus
constant +gamma X Box(chi), signature -+++, K=+div(n). The proposed
background-preserving replacements are

    P_gamma(X,tau)=P0(X,tau)+3 gamma q(tau)H(tau)[X-q(tau)^2],
    W_gamma(Y,tau)=W0(Y,tau)-2 gamma q(tau)^2 qdot(tau), V=U.

q,H,qdot are fixed reconstructed coefficient functions, not local X/Y
variables when varying this action. This report concerns the order-two,
high-frequency principal scalar equations about the homogeneous background.
It does not certify the full finite-wavelength equations or a degree count.

## 1. Scalar and constrained clock variation before freezing coefficients

Use proper FLRW time, chi=chi_bar+sigma, tau=t+pi, chi_bar_dot=q, and
physical orthonormal spatial derivatives. At quadratic order

    X=q^2+2q sigma_dot+sigma_dot^2-|grad sigma|^2,
    sqrt(Xtau)=1+pi_dot-|grad pi|^2/2,
    Y=|grad sigma-q grad pi|^2.

Define background coefficients

    B0=2P0_X+4q^2 P0_XX, d=W0_Y(0,t),
    C0=P0_X-d, S0=W0(0,t)-2q^2d.

The cubic action must be integrated before freezing q,H. Direct expansion of
Box(chi)=-chi_ddot-3H chi_dot+a^-2 Delta chi gives

    L3^(2)/a^3=gamma[-6Hq sigma_dot^2
                       +2(qdot+2Hq)|grad sigma|^2].

For coordinate gradients, after a spatial integration by parts the temporal
boundary used here is d[-gamma a^3 q sigma_dot^2
-gamma a q |partial sigma|^2]/dt. The script verifies this identity for
arbitrary a(t),q(t). Thus the terms containing qdot and H are action-derived;
they are not set to zero by prematurely replacing the background by Minkowski.

Adding P_gamma and W_gamma gives the fixed-metric scalar principal density

    L2/a^3 = (K_fixed/2) sigma_dot^2
             -C_gamma |grad sigma|^2
             -2q d grad pi.grad sigma -(S_gamma/2)|grad pi|^2,

    K_fixed=B0-6 gamma qH,
    C_gamma=C0-gamma(qH+2qdot),
    S_gamma=S0-2 gamma q^2 qdot.

Explicit tau derivatives of the coefficient functions add lower derivative
terms, not another entry in this degree-two principal matrix. No pi_dot^2
or pi_dot sigma_dot survives in the displayed scalar action. At k!=0,
S_gamma!=0 the principal pi Euler equation gives

    pi=-(2q d/S_gamma)sigma,

up to the excluded spatial harmonic modes. Its Schur subtraction is
4q^2d^2/S_gamma from the chi spatial numerator. This is the constrained
clock response; setting pi=0 would give a different answer.

## 2. Keep the cubic metric mixing

The exact cubic stress and scalar Euler equation derived in
../cubic_current_audit/REPORT.md are

    T3_munu=2 gamma Box(chi) chi_mu chi_nu
             +gamma(chi_mu d_nu X+chi_nu d_mu X)
             -gamma g_munu grad(chi).grad(X),
    E3=2 gamma[(Box chi)^2-(nabla nabla chi)^2
               -R_munu grad^mu chi grad^nu chi].

In a local orthonormal frame, the second-perturbation-derivative pieces of
the homogeneous-background stress are independently expanded as

    delta T3_00=2 gamma q^2 Delta sigma,
    delta T3_0i=2 gamma q^2 partial_i sigma_dot,
    delta T3_ij=2 gamma q^2 delta_ij sigma_ddot.

P/W stress perturbations have at most one scalar derivative. Metric terms
in the clock equation likewise have at most one metric derivative. They
are lower derivative contributions in this homogeneous principal calculation.
The metric is not discarded: trace-reversed Einstein equations give

    delta R00=(gamma q^2/M2)(Delta sigma+3 sigma_ddot).

The curvature term in E3 is -2 gamma q^2 delta R00. Therefore its feedback
adds +6 gamma^2 q^4/M2 to the temporal kinetic coefficient and
-2 gamma^2 q^4/M2 to the spatial numerator. This sign follows from actual
stress variation and Einstein trace reversal, not an imported one-field
sound-speed formula. The script separately differentiates the six-metric/
one-scalar velocity Hessian and obtains the same temporal Schur coefficient.
That velocity check alone is not a physical degree-count proof.

## 3. Result and loss of automatic dust response

At nonzero high-frequency spatial momentum, on S_gamma!=0 and K!=0,

    K = B0-6 gamma qH+6 gamma^2 q^4/M2,
    N = 2C_gamma-4q^2 d^2/S_gamma-2 gamma^2 q^4/M2,
    c_principal^2=N/K.

The principal scalar equation is -K sigma_ddot+N Delta sigma=0.
N here labels the restoring numerator, not the ADM lapse.

Original stationary dust matching gives C0 S0=2q^2d^2, so N(0)=0.
For nonzero gamma, the exact numerator on that original dust relation is

    N=-2 gamma(qH+2qdot)
       -8 gamma q^4 d^2 qdot/(S0 S_gamma)
       -2 gamma^2 q^4/M2.

In particular,

    dN/dgamma at 0 = -2(qH+2qdot)-8q^4 d^2 qdot/S0^2.

For the original stationary coefficients d=AU/[2q(qA+U)] and
S0=U^2/(qA+U), equivalently U=mqA, this becomes

    dN/dgamma at 0 = -2[qH+(2+1/m^2)qdot].

This is not identically zero for an arbitrary smooth profile. Preserving
the old homogeneous density, pressure and current therefore does not by
itself preserve the zero-sound-speed principal property. Specific gamma
values/profile points could cancel N; neither sign nor a universal healthy
interval is assumed here. A further gradient reconstruction would be a
new action whose constraints and background must be checked again.

## 4. Scope and reproduction

This computes the asymptotic high-frequency principal structure for modes
with k!=0. It is not a finite-k dispersion relation, homogeneous-mode
classification, global lapse inverse, nonlinear Dirac theorem, or empirical
test. If S_gamma or K vanishes, the displayed divisions are invalid and the
unreduced equations must be studied. A zero N similarly requires the lower
derivative equations to determine its actual evolution. Other minimally
coupled matter perturbations are absent; their health is not certified.

Run `python3 -B derive.py`. It prints exact residual checks and provenance.
For numerical reuse, import `derive()` to obtain `(facts, ctx)`: ctx exposes
gamma,q,H,qdot,M2,C0,S0,d,B0,A,U and the exact expressions `kinetic`,
`restoring`, `tau_stiffness`, `speed_squared`. No profile data or desired
numerical result is read or inserted. All arithmetic in this derivation
is exact symbolic. No first-principles coefficient or MOND law is derived.

The recorded `run_001/` completed with exit 0 under Python 3.9.6 and
SymPy 1.14.0: all 26 exact checks passed. Its manifest validates against
the declared input hashes and retains argv, runtime, dirty-state provenance,
resource bounds and actual output. This validates the recorded computation,
not any broader physical conclusion. Mathbox proof-audit/computation-audit
guided the separation of action identities and principal-only conclusions;
proofread-math self-review found no mathematical-token corrections needed.
