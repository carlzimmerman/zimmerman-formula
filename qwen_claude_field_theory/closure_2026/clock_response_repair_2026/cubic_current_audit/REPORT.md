# Exact cubic current and stress: independent sign audit

Base 86dbf3b3c667fbe0674ff56fa2c54177a070aaaf. This is a bounded audit of
the same P/W clock action with **+ gamma X Box(chi)**, constant gamma.
Signature is -+++, X=-grad(chi)^2, and K=+div(n). No new coefficient,
MOND kernel, cosmology, or health certificate is inferred.

## Covariant variation

Define u_mu=grad_mu chi, B=Box chi, s=sqrt(X_tau),
h^{mu nu}=g^{mu nu}+n^mu n^nu, and E_chi=(delta S/delta chi)/sqrt(-g).
Choose the sign of the shift current by E_chi=-div(J), so its homogeneous
future temporal component is positive for a canonical positive-energy scalar.
Direct variation, integrating X Box(delta chi) once, gives

    J^mu = -2 P_X u^mu + 2 s W_Y h^{mu nu} u_nu
           -2 gamma B u^mu - gamma grad^mu X.

The equation is div(J)=0. Dependence of P and W on tau does not break
chi shift symmetry. Overall reversal of J is conventional; mixing that
reversal with the formulas below would change the energy-identity sign.

For T_munu=-2 delta S/(sqrt(-g) delta g^{mu nu}), the cubic stress is

    T3_munu = 2 gamma B u_mu u_nu
              + gamma (u_mu grad_nu X + u_nu grad_mu X)
              - gamma g_munu u^alpha grad_alpha X.

To derive it, the inverse-metric variation satisfies

    delta(Box chi) = delta g^{mu nu} nabla_mu nabla_nu chi
                    + u_mu nabla_nu(delta g^{mu nu})
                    - (1/2) u^alpha nabla_alpha(g_munu delta g^{mu nu}).

After integrating the last two terms, the X nabla_mu nabla_nu chi
terms cancel, and the XB measure terms cancel. The remaining metric
Euler coefficient is

    gamma[-B u_mu u_nu - u_(mu grad_nu)X
          + (1/2)g_munu u.grad(X)],

whose multiplication by -2 gives the displayed stress. Parentheses include
the factor 1/2. With curvature convention
Box grad_mu chi = grad_mu Box chi + R_munu grad^nu chi,

    E3_chi = 2 gamma[(Box chi)^2
                    - (nabla_mu nabla_nu chi)(nabla^mu nabla^nu chi)
                    - R_munu u^mu u^nu].

It obeys nabla^mu T3_munu=E3_chi u_nu. The script checks both components
of its arbitrary-chi(t,x), flat 1+1 specialization independently. That
coordinate check is not itself the full curved-space proof.

## Homogeneous variation and energy identity

Use ds^2=-N(t)^2 dt^2+a(t)^2 dx^2 and increasing tau(t), with
Q=chi_dot/N, H=a_dot/(Na), s=tau_dot/N. Dots in the following final
formulas mean **proper-time derivatives**, N^{-1}d/dt. Y=0 and W0=W(0,tau).

The exact cubic homogeneous Lagrangian, after a boundary term, is

    L3 = -2 gamma a^2 a_dot (chi_dot/N)^3.

The removed boundary is d[-gamma a^3 Q^3/3]/dt. Independently varying
lapse, scale, and chi_dot before choosing N=1 gives

    rho3 = -6 gamma H Q^3,
    p3   =  2 gamma Q^2 Qdot,
    J3   = -6 gamma H Q^2.

Here J=J^0 in proper-time FLRW coordinates; with coordinate lapse N the
coordinate component is J^t=J/N. The full nongravitational clock density,
pressure and current are

    rho = 2Q^2 P_X - P + V - 6 gamma H Q^3,
    p   = P - V + s W0 + 2 gamma Q^2 Qdot,
    J   = 2Q P_X - 6 gamma H Q^2.

The homogeneous clock Euler derivative is

    E_tau = P_tau - V_tau - 3H W0,

where partial tau derivatives hold X,Y fixed. The W0_tau terms cancel
between variation of W0 and integration of the tau velocity variation.
The **off-shell** energy identity is therefore

    rhodot + 3H(rho+p)
      = Q(Jdot+3HJ) - s E_tau
      = Q(Jdot+3HJ) + s(V_tau-P_tau+3H W0).

Cubic alone satisfies the requested identity without the final clock source.
P plus cubic alone instead gives an extra -s P_tau. For the full P/W/V
sector, the unsourced identity holds on the tau equation, and conservation
also requires the chi current equation. Bare minimally coupled matter
retains its own separate Ward identity; it has not been inserted into J.

## Verification and limits

Run `python3 -B derive.py` in this directory. The script writes no files and
prints source hash, revision, Python/SymPy versions and each exact residual
check as JSON. It independently checks the raw homogeneous boundary term,
lapse/scale/velocity variations, total P/W/V formulas, clock Euler equation,
and the full off-shell energy identity. Arithmetic is exact symbolic, with
arbitrary smooth P(X,tau), W0(tau), V(tau), and no random samples.

Recorded run `run_001/` completed with exit 0: all 13 exact checks passed
under Python 3.9.6 and SymPy 1.14.0. Its bounded-run manifest validates
against the current script hash. Actual argv, output, dirty-state provenance,
runtime and resource limits are retained in that directory. Manifest
validation verifies the evidence record; it does not extend the mathematics.

This does not certify invertibility of the full Legendre map, the nonlinear
Dirac chain, scalar/tensor stability, caustics, PPN, or the MOND source law.
The audit uses mathbox proof-audit and computation-audit; no external theorem
or imported KGB sign convention is needed for the displayed derivation.
Mathbox proofread-math self-review covered this report's displayed formulas
and conventions; no mathematical-token correction was required.
