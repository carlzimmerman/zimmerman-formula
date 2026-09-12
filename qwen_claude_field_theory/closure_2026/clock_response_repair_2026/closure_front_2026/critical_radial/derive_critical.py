#!/usr/bin/env python3
"""Exact finite jets for a conditional critical radial derivative reduction.

No functions are fitted. No partially resummed equation is an exact field
equation of the full theory. stdout is the scientific result.
"""
import json
import platform
import sympy as S


def derive():
    checks = {}

    def zero(name, expression):
        remainder = S.factor(S.cancel(S.expand(expression)))
        checks[name] = remainder == 0
        if remainder != 0:
            raise AssertionError((name, remainder))

    eps = S.symbols("eps")
    r, M2, q, Wc, d, ell = S.symbols("r M2 q Wc d ell", positive=True)
    gamma, PX, PXX, PXXX, P0, V = S.symbols("gamma PX PXX PXXX P0 V", real=True)
    n, a, g, p, pi = S.symbols("n a g p pi", real=True)
    b = gamma*q**2
    alpha = b/M2
    C = Wc-2*d*q**2
    z1 = -2*d*q/C
    N, A = 1+eps*n, 1+eps*a
    pp, zz, gp = eps*p, eps*z1*p, eps*g
    X = q**2/N**2-pp**2/A**2
    s = S.sqrt(1/N**2-zz**2/A**2)
    Y = (pp-q*zz)**2/(A**2-N**2*zz**2)
    dx = S.series(X-q**2, eps, 0, 4).removeO()
    P = P0+PX*dx+PXX*dx**2/2+PXXX*dx**3/6
    # Y^2 starts at amplitude four: it cannot affect the cubic jet.
    W = Wc+d*Y
    LPW = S.series(N*A*(P-V+s*W), eps, 0, 4).removeO().expand()
    H0 = 2*PX-2*d*Wc/C
    H1 = 2*PX-4*q**2*PXX+8*d**2*q**2*Wc/C**2
    zero("clock_eliminated_quadratic_p_coefficient",
         LPW.coeff(eps, 2).coeff(p, 2)+H0/2)
    zero("clock_eliminated_cubic_metric_p_coefficient",
         LPW.coeff(eps, 3).coeff(p, 2)-(H0*a-H1*n)/2)

    NN = S.symbols("N", positive=True)
    # Taylor only PX(N) to the degree needed for its first lapse derivative.
    HN = 2*NN*(PX+PXX*(q**2/NN**2-q**2))-2*d*Wc/(Wc-2*d*q**2/NN**2)
    zero("independent_lapse_derivative", S.diff(HN, NN).subs(NN, 1)-H1)

    LEH = M2*(N*(A+1/A-2)+2*r*gp*(1/A-1))
    L3 = (2*b*r**2*gp*pp/(A*N**2)
          -S.Rational(2, 3)*gamma*r**2*gp*pp**3/A**3
          -S.Rational(4, 3)*gamma*N*r*pp**3/A**3)
    ejet = S.series(LEH, eps, 0, 4).removeO().expand()
    cjet = S.series(L3, eps, 0, 4).removeO().expand()
    zero("EH_radial_quadratic", ejet.coeff(eps, 2)-M2*(a*a-2*r*g*a))
    zero("EH_radial_cubic", ejet.coeff(eps, 3)-M2*(n*a*a-a**3+2*r*g*a*a))
    zero("cubic_braiding_quadratic", cjet.coeff(eps, 2)-2*b*r*r*g*p)
    zero("cubic_braiding_cubic", cjet.coeff(eps, 3)
         +2*b*r*r*g*p*(a+2*n)+S.Rational(4, 3)*gamma*r*p**3)

    H, Hprime = S.symbols("G0 G0_N", real=True)
    L2 = M2*(a*a-2*r*g*a)+2*b*r*r*g*p-H*r*r*p*p/2
    L2el = S.expand(L2.subs(a, r*g))
    zero("metric_spatial_constraint", S.diff(L2, a).subs(a, r*g))
    zero("metric_square_completion", L2el
         +M2*r*r*(g-alpha*p)**2+(H-2*b*b/M2)*r*r*p*p/2)
    Lcubic = (ejet.coeff(eps, 3)+cjet.coeff(eps, 3)
              +r*r*(H*a-Hprime*n)*p*p/2)
    critical = S.expand(Lcubic.subs({a: alpha*r*p, g: alpha*p, n: alpha*pi,
                                   H: 2*b*b/M2}))
    Q = -alpha*(Hprime+6*b*b/M2)/2
    expected = -S.Rational(4, 3)*gamma*r*p**3+Q*r*r*pi*p*p
    zero("critical_projected_cubic_with_metric_remainder", critical-expected)
    zero("critical_r3_p3_cancellation",
         S.expand(critical).coeff(pi, 0).coeff(p, 3)+S.Rational(4, 3)*gamma*r)

    # Variational operators: E = dL/dpi - d/dr(dL/dp).
    pir = S.Function("pi")(r)
    pr = S.diff(pir, r)
    Qs = S.symbols("Q", real=True)
    Lcorr = Qs*r*r*pir*pr**2
    E_corr = S.diff(Lcorr, pir)-S.diff(S.diff(Lcorr, pr), r)
    corr_expected = -Qs*(r*r*pr**2+2*pir*S.diff(r*r*pr, r))
    zero("metric_remainder_Euler_operator", E_corr-corr_expected)
    Lgal = -S.Rational(4, 3)*gamma*r*pr**3
    E_gal = -S.diff(S.diff(Lgal, pr), r)
    zero("Galileon_Euler_operator", E_gal-S.diff(4*gamma*r*pr**2, r))

    # Source follows from the minimally sourced metric constraint, not scalar
    # charge. Both equations are the declared retained hierarchy.
    G, gn = S.symbols("G gN", real=True)
    metric_g = gn+alpha*p
    scalar_flux = H*p-2*b*metric_g+4*gamma*p*p/r
    zero("metric_induced_source_flux",
         scalar_flux.subs(H, G+2*b*b/M2)-(G*p+4*gamma*p*p/r-2*b*gn))
    mass, gamma_pos = S.symbols("enclosed_mass gamma_positive", positive=True)
    gn_mass = mass/(8*S.pi*M2*r*r)
    pcritical = S.sqrt(q*q*mass/(16*S.pi*M2*r))
    zero("critical_sourced_square_law",
         (4*gamma*pcritical**2/r-2*b*gn_mass))
    zero("critical_radius_exponent", r*S.diff(pcritical, r)/pcritical+S.Rational(1, 2))
    zero("physical_scalar_force_correction_exponent",
         r*S.diff(alpha*pcritical, r)/(alpha*pcritical)+S.Rational(1, 2))

    # Frozen completion is an input history, not a tunable replacement.
    U, lamX, lamW = S.symbols("U lambda_X lambda_W", real=True)
    Delta = U-2*d*q*q
    canonical = {PX: U*d/Delta+lamX, PXX: 2*U*d*d/Delta**2, Wc: U+lamW}
    canonical_H0 = (2*lamX+4*d*d*q*q*lamW/(Delta*(Delta+lamW)))
    zero("canonical_completion_H0", H0.subs(canonical)-canonical_H0)
    canonical_H1 = (2*(U*d/Delta+lamX)-8*U*d*d*q*q/Delta**2
                    +8*d*d*q*q*(U+lamW)/(Delta+lamW)**2)
    zero("canonical_completion_lapse_derivative", H1.subs(canonical)-canonical_H1)

    # Explicit lower-derivative terms before any background subtraction.
    potjet = S.expand(LPW.subs(p, 0))
    zero("frozen_potential_quadratic_lapse",
         potjet.coeff(eps, 2).coeff(n, 2)-(q*q*PX+2*q**4*PXX))
    zero("frozen_potential_quadratic_cross",
         potjet.coeff(eps, 2).coeff(n, 1).coeff(a, 1)-(P0-V-2*q*q*PX))
    K1 = q*q*PX+2*q**4*PXX
    K2 = P0-V-2*q*q*PX
    Bpot = alpha**2*(K1-S.Rational(3, 2)*K2)
    projected_potential = alpha**2*(K1*r*r*pir**2+K2*r**3*pir*pr)
    potential_boundary = alpha**2*K2*r**3*pir**2/2
    zero("projected_unsubtracted_potential_IBP",
         projected_potential-Bpot*r*r*pir**2-S.diff(potential_boundary, r))

    # Independent exact sign/radius fixture for the algebraic retained model.
    fixture = []
    for rr in [S.Rational(1), S.Rational(4), S.Rational(16)]:
        pp_fixture = 1/S.sqrt(rr)
        zero("retained_fixture_at_"+str(rr), 4*rr*pp_fixture**2-4)
        fixture.append({"r": str(rr), "p": str(pp_fixture),
                        "r_times_p_squared": str(rr*pp_fixture**2),
                        "r_squared_times_p_squared": str(rr**2*pp_fixture**2)})

    return {
        "scope": "Exact jets and necessary ordering for a frozen local critical radial reduction; no nonlinear solution of the full fixed-history theory",
        "base_revision_supplied": "bba135b36acd2dc40039517ed6038d1e7c37a995",
        "software": {"python": platform.python_version(), "sympy": S.__version__},
        "conventions": {"signature": "-+++", "clock_epoch": "tau=t+sigma(r), timelike near zero", "metric": "-N^2 dt^2+A^2 dr^2+r^2 dOmega^2", "scalar": "chi=q t+pi(r), p=pi'", "flux": "regular-center zero scalar and clock flux in frozen stationary reduction", "matter": "minimal dust at leading source order; gN=Menc/(8 pi M2 r^2)"},
        "clock_regular_denominator": str(C),
        "G0": str(H0), "G0_lapse_derivative": str(H1),
        "critical_metric_cubic_coefficient_Q": str(Q),
        "critical_cubic_action": str(expected),
        "metric_remainder_Euler_operator": str(corr_expected),
        "retained_radial_flux": "G*p+4*gamma*p^2/r=2*b*gN; b=gamma*q^2",
        "critical_p_squared": str(pcritical**2),
        "canonical_G0": str(canonical_H0),
        "canonical_G0_lapse_derivative": str(canonical_H1),
        "unsubtracted_potential_quadratic": str(S.factor(potjet.coeff(eps, 2))),
        "projected_unsubtracted_potential_coefficient": str(Bpot),
        "retained_model_fixture": fixture,
        "checks": checks, "checks_passed": len(checks),
        "non_claims": ["No arbitrary direct scalar matter coupling", "No source charge identified with baryonic mass", "No nonlinear completion by mixing exact flat flux with selected metric terms", "No global regularity, boundary matching or stability certificate", "No proof the fixed histories admit the hierarchy or G=0", "No uniform arbitrarily-small-source limit at fixed radius", "Analytic regular clock exclusion of p|p| is branch-local"]
    }


if __name__ == "__main__":
    print(json.dumps(derive(), indent=2))
