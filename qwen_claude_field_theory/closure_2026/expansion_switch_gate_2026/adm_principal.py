"""Independent static transverse ADM principal-symbol derivation.

Conventions: M^2=m>0, N_bar=1 at the evaluation point, h_bar=delta,
K_ij=(dot(h_ij)-Lie_shift(h_ij))/(2N), k perpendicular to a_bar.
The nonzero Fourier mode of varphi is removed by D_i varphi=0 only after
varying its multiplier. The remaining homogeneous-varphi trace term is a
boundary term up to terms without two perturbation derivatives. Its local
principal contribution vanishes. This script starts from the resulting
action R/2+K_T^2/2+f(s)+s B(K), not from a proposed quadratic action.

Background coefficients are frozen locally. A=|a_bar| is assigned derivative
degree zero; it is a coefficient, not a perturbation derivative. In the
quadratic real-mode average, k and zd each carry perturbation derivative
degree one. Keeping total degree two in (k,zd) retains the two-derivative
principal action. Amplitude expansion precedes this projection.

This finite symbolic calculation neither solves a global static background
nor counts nonlinear degrees of freedom. It supplies no expected ranks or
constraint counts. Run: python3 adm_principal.py
"""

from functools import lru_cache

import sympy as s


@lru_cache(None)
def derive():
    """Return the action-derived principal L and exact identity residuals."""
    epsilon, theta = s.symbols("epsilon theta", real=True)
    m, k, alpha = s.symbols("m k alpha", positive=True)
    b, z, zd, n, v = s.symbols("b z zd n v", real=True)
    A, K0, a0 = s.symbols("A K0 a0", positive=True)
    sin, cos = s.sin(theta), s.cos(theta)
    zeta = epsilon*z*cos
    lapse = 1+epsilon*n*cos
    shift = epsilon*v*sin
    hfactor = s.exp(2*zeta)
    volume = s.exp(3*zeta)
    dx = lambda expr: k*s.diff(expr, theta)
    derivative = lambda expr, i: dx(expr) if i == 0 else s.S.Zero

    # Compute actual Christoffels and the Ricci tensor of h_ij. No Ricci
    # scalar or quadratic curvature coefficient is inserted as an input.
    h, hi = s.eye(3)*hfactor, s.eye(3)/hfactor
    gamma = [[[
        s.simplify(sum(hi[i, ell]*(derivative(h[ell, q], j)
                      + derivative(h[ell, j], q)
                      - derivative(h[j, q], ell))
                       for ell in range(3))/2)
        for q in range(3)] for j in range(3)] for i in range(3)]
    ricci = s.Matrix(3, 3, lambda i, j: sum(
        derivative(gamma[ell][i][j], ell)
        - derivative(gamma[ell][i][ell], j)
        + sum(gamma[ell][i][j]*gamma[q][ell][q]
              - gamma[q][i][ell]*gamma[ell][j][q]
              for q in range(3))
        for ell in range(3)))
    curvature = s.simplify(sum(hi[i, j]*ricci[i, j]
                               for i in range(3) for j in range(3)))

    # Lie_shift h is kept before forming K and its traceless contraction.
    hdot = 2*epsilon*zd*cos*hfactor
    kmixed = s.diag(*[
        (hdot-shift*dx(hfactor)
         -(2*hfactor*dx(shift) if i == 0 else 0))/(2*lapse*hfactor)
        for i in range(3)])
    ktrace = s.trace(kmixed)
    kt_squared = s.simplify(s.trace(kmixed*kmixed)-ktrace**2/3)

    # Locally N_bar=exp(A x^2), evaluated at x^2=0, while the perturbation
    # has wavevector along x^1. Thus d_i ln N=(d_x ln lapse, A, 0).
    # Background derivatives beyond this coefficient are lower-order terms
    # in the local principal expansion, not claimed to vanish globally.
    acceleration_squared = (A**2+(dx(lapse)/lapse)**2)/hfactor

    s_argument = s.symbols("s_argument", positive=True)
    f = 2*a0**2*(1-(1+s.sqrt(s_argument)/a0)
                 * s.exp(-s.sqrt(s_argument)/a0))
    f_derivatives = tuple(s.simplify(s.diff(f, s_argument, order)
                                     .subs(s_argument, A**2))
                          for order in range(3))
    f0, fs, fss = s.symbols("f0 fs fss", real=True)
    delta_s = acceleration_squared-A**2
    f_expansion = f0+fs*delta_s+fss*delta_s**2/2

    k_argument = s.symbols("k_argument", real=True)
    switch = -k_argument**2/(k_argument**2+K0**2)
    switch_derivatives = tuple(s.diff(switch, k_argument, order)
                               .subs(k_argument, 0)
                               for order in range(3))
    switch_expansion = (switch_derivatives[0]
                        + switch_derivatives[1]*ktrace
                        + switch_derivatives[2]*ktrace**2/2)
    raw_action = lapse*volume*(curvature/2+kt_squared/2
                              + f_expansion
                              + acceleration_squared*switch_expansion)
    quadratic = s.expand(s.series(raw_action, epsilon, 0, 3)
                          .removeO()).coeff(epsilon, 2)
    quadratic = s.expand_trig(s.expand(quadratic))
    # Twice the real-mode spatial average. At quadratic order all terms
    # contain either cos^2 or sin^2; both have average 1/2.
    average = s.expand(2*quadratic.subs(
        {cos**2: s.Rational(1, 2), sin**2: s.Rational(1, 2)}))
    polynomial = s.Poly(average, k, zd)
    principal = s.expand(sum(coefficient*k**i*zd**j
                             for (i, j), coefficient in polynomial.terms()
                             if i+j == 2))
    physical_L = m*principal.subs(dict(zip((f0, fs, fss), f_derivatives)))
    # Rename derived physical coefficients for the canonical calculation:
    # alpha=f_s(A^2), b=A^2 B''(0)/2=-A^2/K0^2.
    alpha_definition = f_derivatives[1]
    b_definition = A**2*switch_derivatives[2]/2
    L = s.expand(physical_L.subs(K0**2, -A**2/b)
                 .subs(s.exp(-A/a0), alpha))

    # Independent identity checks are diagnostics only. L above is the
    # computed raw-action projection; it is not assigned this target form.
    compact_L = m*(b*(3*zd-k*v)**2+k**2*v**2/3
                   + k**2*(z**2+2*n*z+alpha*n**2))
    conformal_curvature = s.exp(-2*zeta)*(-4*dx(dx(zeta))-2*dx(zeta)**2)
    residuals = {
        "ricci_identity": s.simplify(curvature-conformal_curvature),
        "trace_linearization": s.simplify(
            s.diff(ktrace, epsilon).subs(epsilon, 0)-(3*zd-k*v)*cos),
        "traceless_linearization": s.simplify(
            s.diff(kt_squared, epsilon, 2).subs(epsilon, 0)/2
            - s.Rational(2, 3)*k**2*v**2*cos**2),
        "alpha_derivative": s.simplify(alpha_definition-s.exp(-A/a0)),
        "static_switch_value": switch_derivatives[0],
        "static_switch_first_derivative": switch_derivatives[1],
        "switch_second_derivative": s.simplify(
            switch_derivatives[2]+2/K0**2),
        "compact_action": s.simplify(L-compact_L),
        "physical_coefficient_reconstruction": s.simplify(
            L.subs({alpha: alpha_definition, b: b_definition})-physical_L),
    }
    return dict(m=m, b=b, alpha=alpha, k=k, z=z, zd=zd, n=n, v=v, L=L,
                A=A, K0=K0, a0=a0, alpha_definition=alpha_definition,
                b_definition=b_definition, f=f, f_derivatives=f_derivatives,
                B=switch, B_second=s.factor(s.diff(switch, k_argument, 2)),
                curvature=curvature, kmixed=kmixed, ktrace=ktrace,
                acceleration_squared=acceleration_squared,
                raw_quadratic_average=average, physical_L=physical_L,
                residuals=residuals, validation_residuals=residuals,
                principal_degree="degree(k)=degree(zd)=1; frozen A has degree 0; retain total degree 2")


if __name__ == "__main__":
    result = derive()
    print("SymPy:", s.__version__)
    print("Principal degree:", result["principal_degree"])
    print("alpha:", result["alpha_definition"])
    print("b:", result["b_definition"])
    print("L:", s.factor(result["L"]))
    for name, residual in result["residuals"].items():
        print(name+":", residual)
        assert residual == 0, (name, residual)
