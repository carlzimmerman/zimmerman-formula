# Cubic clock completion: derived equations, not a derived theory of nature

Base: `86dbf3b3c667fbe0674ff56fa2c54177a070aaaf`. Original goal remains **OPEN**.
Carl explicitly requires an underlying derivation, not merely phenomenological
functions reconstructed to match a desired history. This calculation respects
that distinction: it derives consequences of one explicit action and tests a
particular inverse reconstruction. It does not explain why nature selects it.
No acceleration scale, local a0 prescription, exponential kernel, or fitted
kappa has been inserted into these tests. None is derived here either.

## Same action, exact homogeneous variation

Use signature -+++, X=-grad(chi)^2, s=sqrt(-grad(tau)^2),
n_mu=-grad_mu(tau)/s, Q=n.grad(chi), and Y=Q^2-X. The action is

    S = integral sqrt(-g) [M²(R-2 Lambda)/2 + P(X,tau)
          + s W(Y,tau) - V(tau) + gamma X Box(chi)] + S_m[g,psi].

Gamma is constant and free. The cubic interaction is the known operator
documented in `../mond_braiding_completion/SOURCE.md`, not a claimed discovery.
Ordinary matter remains minimally coupled. Its on-shell Ward identity is
separate from conservation of the clock stress. The independent variation in
`../cubic_current_audit/REPORT.md` supplies the exact current, cubic stress, and
the full homogeneous off-shell energy identity, including the tau equation.

In tau=t gauge, alpha=log(a), H=alpha_dot/N, Q=chi_dot/N,

    L = N a³ f + a³ W(0,tau),
    f = -3M² H² + P(Q²,tau) - V - M² Lambda - 2 gamma Q³ H.

The script differentiates this density, rather than assigning a kinetic matrix:

    p_alpha/a³ = -6M²H - 2 gamma Q³,
    j = p_chi/a³ = 2Q P_X - 6 gamma H Q²,
    rho = 2Q² P_X - P + V - 6 gamma H Q³,
    pressure = P - V + W0 + 2 gamma Q² Qdot,
    C/a³ = -3M²H² + rho + M² Lambda.

With B=2P_X+4Q²P_XX, the actual two-velocity Hessian is

    K = [[-6M²,          -6 gamma Q²],
         [-6 gamma Q²,  B - 12 gamma H Q]].
    Bhat = B - 12 gamma H Q + 6 gamma² Q⁴/M².

Inverse-based equations below require M² != 0 and Bhat != 0. They cannot be
continued through Bhat=0 by substitution into a cancelled expression.

## Reconstructing the old background — and why that is insufficient

The earlier log/sqrt clock has

    q=Qc/(1+m), A=I/a³, U=m q A,
    d=A U/[2q(qA+U)], ell=q²m/2,
    P0=-(U/2) log[(U-2dX)/(U-2dq²)],
    W0=U+2d ell [sqrt(1+Y/ell)-1], V0=U,
    B0=A/q+2A²/U.

Its history m,v is derived in `../nonlinear_transport/stationary.py`.
Requiring unchanged j=A, rho=qA+U, pressure=0, with delta P(q²)=0, yields

    P_gamma = P0 + 3 gamma q H (X-q²),
    W_gamma = W0 - 2 gamma q² qdot,
    V_gamma = U.

These are the solution of three matching equations, **not** a principle that
selects the theory or gamma. They restore the prescribed background exactly.
The script independently verifies C=T=0, the charge, pressure, the Hamiltonian
flow for (H,q), and the lapse equation with its proper fixed-momentum source.

An explicit non-uniqueness witness is also checked: adding

    delta P = lambda(tau) (X-q²)²/2

leaves P and P_X on the history unchanged but shifts the background kinetic
coefficient by 4 lambda q². Background matching therefore cannot determine
perturbative physics or all coefficients. This extra counterterm is **not**
included in the scanned candidate; it limits the scope of its exclusions.

## Homogeneous constraint block

With the conventional canonical Poisson bracket, the lapse primary gives C,
then T/a³=V_tau-P_tau+3HW0. Define

    b=(3W0,-2Q P_tauX),
    Rc=(3f-3H f_H,-3H f_Q).
    Delta/a³ = {T,C}/a³ = 3H(T/a³) + b^T K^-1 Rc.
    F0 = V_tautau-P_tautau+3H W0_tau + b^T K^-1 b.

Here P_tau derivatives hold X fixed. Homogeneous lapse preservation is
N Delta/a³ + F0=0. The actual repaired branch gives F0=-Delta/a³ and

    -Delta/a³ = 9 A² [(H+gamma q³/M²)²/Bhat_gamma - v H²/B0],
    Bhat_gamma = B0 - 6 gamma qH + 6 gamma² q⁴/M².

Thus N=1 is obtained when Delta != 0, not assigned as a certification result.
The inverse and both source terms are generated from the action. A zero Delta
requires continuation of the Dirac analysis there; negative Delta alone is
not a proof of a ghost. This homogeneous calculation is **not** the full spatial
Poisson-bracket matrix, first/second-class count, or N_grav=2 certificate.

For R=B0 q²/(M²H²) and z=gamma q³/(M²H), put D=R-6z+6z². The normalized gap is

    (1+z)²/D - v/R
      = [R(1-v)+(2R+6v)z+(R-6v)z²]/(R D).

`HomogeneousGap.lean` verifies this identity, the positive-denominator sign
equivalence, and a sufficient positivity condition. Its assumptions are
explicit; it proves no action variation, empirical validity, or full health.

## Numerical falsification scope

`numerical.py` integrates the existing history independently with DOP853 and
Radau. It tests 13 specified gamma values at 361 epochs, a=1e-6 to 1e3,
using 70-digit algebra on float64-integrated profiles. Parameters are
M²=Qc=1, I=.1, Lambda=.7, m(1)=.1, v(1)=.5. This is a dimensionless example,
not a measured coefficient range. Gamma=0 is a control.

The history has **no radiation or baryons**: its early-a diagnostics cannot
be called a recombination, third-peak, or CMB-safety calculation.
Crossings are bracketed and numerically located; they are not rigorous interval
ODE enclosures. A grid pass is not a continuum theorem. The exact commands,
source hashes, outputs, statuses and finite diagnostics are in `run_001/`.

## What comes next

The same repaired action's high-frequency calculation has now been executed:
`../cubic_principal_audit/REPORT.md` includes both metric mixing and the elliptic
tau constraint. In its notation the reduced scalar coefficients are

    Kscalar = Bhat_gamma,
    Sgamma = S0 - 2 gamma q² qdot,
    Nscalar = 2[C0-gamma(qH+2qdot)] - 4q²d²/Sgamma
              - 2 gamma² q⁴/M²,
    c_principal² = Nscalar/Kscalar,
    C0=P0_X-d, S0=U-2q²d.

The code varies the quadratic action and derives the metric feedback from
the cubic stress; it does not input a desired speed. The old exact dust
principal response Nscalar=0 is generally lost even though the homogeneous
pressure remains exactly zero. This distinction is physical information the
background match alone missed. See `RESULTS.md` for the bounded scan outcome.

Next: the **full finite-wavelength** scalar equations and nonlinear spatial
Dirac operator, and the sourced weak-field equations (Phi and Psi independently),
before PPN or data fitting. The radiation-containing background must also be
varied from the action, not patched onto this radiation-free example.
Deriving a unique constitutive law and the a0–Lambda relation remains a separate,
unsolved physical requirement. These tests do not derive kappa=1/2.

The mathbox computation-audit workflow determines the bounded execution and
evidence record. Independent proof-audit checked the lapse normalization and
source chain rule; proofread-math self-review checked the displayed conventions.
No evidence metadata or number of passing assertions constitutes theory closure.
