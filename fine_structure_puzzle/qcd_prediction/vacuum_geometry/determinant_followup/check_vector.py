"""Exact two-channel static BPS Hessian determinant, with independent ODE QA."""
import argparse
import json
from pathlib import Path
import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import solve_ivp
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", required=True)
    args = parser.parse_args()
    x = s.symbols("x", positive=True)
    h = s.coth(x)-1/x
    K = x/s.sinh(x)
    W = s.Matrix([[h, s.sqrt(2)*K/x], [s.sqrt(2)*K/x, -1/x]])
    U = s.Matrix([[h*h+(3*K*K-1)/x**2, 2*s.sqrt(2)*K*h/x],
                  [2*s.sqrt(2)*K*h/x, 2*K*K/x**2]])
    assert (W*W-W.diff(x)-U).applyfunc(s.simplify) == s.zeros(2)
    y0 = s.Matrix([x*s.diff(K, x), x*(h+x*s.diff(h, x))/s.sqrt(2)])
    assert (y0.diff(x)+W*y0).applyfunc(s.simplify) == s.zeros(2, 1)
    assert (y0.diff(x, 2)-U*y0).applyfunc(s.simplify) == s.zeros(2, 1)
    a = s.Matrix([-s.Rational(1, 3), s.sqrt(2)/3])
    assert s.simplify((a.T*a)[0]) == s.Rational(1, 3)
    integrand = h*h+(s.cosh(x)/x-1/s.sinh(x))**2/2
    assert s.simplify(integrand-(s.sinh(x)/x**2)**2*(y0.T*y0)[0]) == 0
    assert s.simplify(s.diff(s.sinh(x)/x**2, x)-s.trace(W)*s.sinh(x)/x**2) == 0
    V0s = s.Matrix([[-1, 2*s.sqrt(2)/3], [2*s.sqrt(2)/3, -s.Rational(2, 3)]])
    V2s = s.Matrix([[s.Rational(14, 45), -7*s.sqrt(2)/45],
                    [-7*s.sqrt(2)/45, s.Rational(2, 15)]])
    for i in range(2):
        for j in range(2):
            assert s.simplify(s.series(U[i, j], x, 0, 4).removeO()
                              -(2/x**2 if i == j else 0)-V0s[i, j]-x*x*V2s[i, j]) == 0
    V0 = np.array(V0s.evalf(), dtype=float)
    V2 = np.array(V2s.evalf(), dtype=float)
    A = V0/10
    B = (V0@A+V2)/28
    def potential(r):
        if r < 0.002:
            return 2/r**2*np.eye(2)+V0+V2*r*r
        hr = 1/np.tanh(r)-1/r
        kr = r/np.sinh(r)
        return np.array([[hr*hr+(3*kr*kr-1)/r**2, 2*np.sqrt(2)*kr*hr/r],
                         [2*np.sqrt(2)*kr*hr/r, 2*kr*kr/r**2]])
    def ode(r, z):
        Y = z[:4].reshape((2, 2))
        P = z[4:].reshape((2, 2))
        return np.concatenate([P.ravel(), (potential(r)@Y).ravel()])
    mp.mp.dps = 60
    def exact_det(X):
        def f(t):
            if abs(t) < mp.mpf("1e-10"):
                return t*t/3  # next terms below 1e-40 at this cutoff
            return (mp.coth(t)-1/t)**2+(mp.cosh(t)/t-1/mp.sinh(t))**2/2
        return 9*X*X/mp.sinh(X)*mp.quad(f, [0, X])
    rows = []
    for X in [2, 5, 8]:
        det_exact = exact_det(mp.mpf(X))
        for eps in [0.001, 0.0005]:
            Ystart = np.eye(2)+A*eps**2+B*eps**4
            Pstart = 2/eps*np.eye(2)+4*A*eps+6*B*eps**3
            start = np.concatenate([Ystart.ravel(), Pstart.ravel()])
            sol = solve_ivp(ode, (eps, X), start, method="DOP853", rtol=1e-12, atol=1e-14)
            assert sol.success
            Yend = eps**2*sol.y[:4, -1].reshape((2, 2))
            det_numeric = float(np.linalg.det(Yend))
            relative = abs(mp.mpf(det_numeric)/det_exact-1)
            assert relative < mp.mpf("2e-7")
            ref = 3*(mp.cosh(X)-mp.sinh(X)/X)*X*X
            rows.append({"x": X, "origin_cutoff": eps,
                         "exact_integral_detY": mp.nstr(det_exact, 30),
                         "independent_matrix_ode_detY": det_numeric,
                         "relative_discrepancy": mp.nstr(relative, 12),
                         "relative_det_to_auxiliary_free_block": mp.nstr(det_exact/ref, 30),
                         "ODE_evaluations": sol.nfev})
    asymptotic = []
    for X in [mp.mpf(10), mp.mpf(20), mp.mpf(40)]:
        d = exact_det(X)/(3*(mp.cosh(X)-mp.sinh(X)/X)*X*X)
        asymptotic.append({"x":str(X), "det_ratio":mp.nstr(d, 30),
                           "x_times_normalized_ratio_minus_one":mp.nstr(X*(d*4*X*X/3-1), 30)})
    result = {"status":"passed", "assertion_tested":"Two-channel Q-dagger-Q Hessian, BPS kernel and determinant-integrand identities; independent matrix initial-value determinant versus exact scalar quadrature",
              "software":{"sympy":s.__version__,"mpmath":mp.__version__,"numpy":np.__version__,"scipy":scipy.__version__},
              "checks":rows,"asymptotic_diagnostic":asymptotic,
              "non_claims":["Static real spherical block only, not full vector Hessian", "Auxiliary reference not complete physical vacuum", "No full gauge-compatible domain or collective-coordinate cancellation established", "Finite numerical checks do not replace the hand determinant derivation"]}
    Path(args.result).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"passed","result":args.result}))


if __name__ == "__main__":
    main()
