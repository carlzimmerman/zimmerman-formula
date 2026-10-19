"""Actual BPS ghost radial block: exact GY determinants and spectral checks."""
import argparse
import json
from pathlib import Path

import mpmath as mp
import sympy as s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--result", required=True)
    args = ap.parse_args()
    x, q, k, t = s.symbols("x q k t", positive=True)
    potential = 2/s.sinh(x)**2
    u0 = 3*(x*s.coth(x)-1)
    uq = 3*(q*s.cosh(q*x)-s.coth(x)*s.sinh(q*x))/(q*(q*q-1))
    ur = 3*(s.cosh(q*x)-s.sinh(q*x)/(q*x))/(q*q)
    u1 = s.Rational(3, 2)*(s.cosh(x)-x/s.sinh(x))
    assert s.simplify(-s.diff(u0, x, 2)+potential*u0) == 0
    assert s.simplify(-s.diff(uq, x, 2)+(potential+q*q)*uq) == 0
    assert s.simplify(-s.diff(ur, x, 2)+(2/x**2+q*q)*ur) == 0
    assert s.simplify(-s.diff(u1, x, 2)+(potential+1)*u1) == 0
    assert s.simplify(s.series(uq, x, 0, 4).removeO()/x**2) == 1
    assert s.simplify(s.series(ur, x, 0, 4).removeO()/x**2) == 1
    eigenfunction = s.coth(x)*s.sin(k*x)-k*s.cos(k*x)
    assert s.simplify(-s.diff(eigenfunction, x, 2)+(potential-k*k)*eigenfunction) == 0
    # Intertwiner boundary domain and removed free Robin eigenfunction.
    T = lambda v: s.diff(v, x)-s.coth(x)*v
    assert s.simplify(T(s.sinh(x))) == 0
    assert s.simplify(T(s.sin(k*x))+eigenfunction) == 0
    # Algebraic finite-radius expansions after exponentially small pieces.
    zero_log_series = s.series(s.log(1-t), t, 0, 4)
    pos_log_series = s.series(-s.log(1-t/q), t, 0, 4)
    assert zero_log_series.removeO().coeff(t, 1) == -1
    assert pos_log_series.removeO().coeff(t, 1) == 1/q

    mp.mp.dps = 60
    N = 256
    def root_z(n, c):
        # tan(delta)=c(n*pi+delta), unique root as 0<c<=1.
        lo = mp.mpf(0)
        hi = mp.pi/2
        for _ in range(110):
            mid = (lo+hi)/2
            if mp.tan(mid)-c*(n*mp.pi+mid) > 0:
                hi = mid
            else:
                lo = mid
        return n*mp.pi+(lo+hi)/2
    ref_roots = [root_z(n, mp.mpf(1)) for n in range(1, N+1)]
    rows = []
    for X in [mp.mpf(2), mp.mpf(5), mp.mpf(10)]:
        c = mp.tanh(X)/X
        roots = [root_z(n, c) for n in range(1, N+1)]
        for Q in [mp.mpf(0), mp.mpf(1), mp.mpf(2)]:
            if Q == 0:
                exact = 3*(X*mp.coth(X)-1)/X**2
            elif Q == 1:
                exact = (mp.cosh(X)-X/mp.sinh(X))/(2*(mp.cosh(X)-mp.sinh(X)/X))
            else:
                exact = Q/(Q*Q-1)*(Q*mp.cosh(Q*X)-mp.coth(X)*mp.sinh(Q*X))/(mp.cosh(Q*X)-mp.sinh(Q*X)/(Q*X))
            partial_log = mp.fsum(mp.log((z*z+(Q*X)**2)/(zr*zr+(Q*X)**2))
                                  for z, zr in zip(roots, ref_roots))
            a2 = -2*(1/c-1)
            a4 = -3/c**2+mp.mpf(2)/(3*c**3)+mp.mpf(7)/3+2*(Q*X)**2*(1/c-1)
            tail2 = a2*mp.polygamma(1, N+mp.mpf("1.5"))/mp.pi**2
            tail4 = a4*mp.polygamma(3, N+mp.mpf("1.5"))/(6*mp.pi**4)
            corrected_log = partial_log+tail2+tail4
            log_error = abs(corrected_log-mp.log(exact))
            assert log_error < mp.mpf("2e-8")
            # Independent variational comparison gives a rigorous loose bound
            # on the uncomputed spectral-product tail; no asymptotic fit needed.
            bound_a = mp.mpf(2)*X**2/3
            gamma = bound_a/mp.pi**2
            log_tail_bound = gamma/(N*(1-gamma/(N+1)**2))
            assert partial_log-log_tail_bound <= mp.log(exact) <= partial_log
            rows.append({"x": str(X), "q": str(Q),
                         "exact_gy_ratio": mp.nstr(exact, 30),
                         "N_eigenvalues_per_operator": N,
                         "partial_log_product": mp.nstr(partial_log, 30),
                         "tail_corrected_log_product": mp.nstr(corrected_log, 30),
                         "absolute_log_discrepancy": mp.nstr(log_error, 12),
                         "rigorous_loose_tail_log_bound": mp.nstr(log_tail_bound, 12)})
    result = {"status": "passed", "assertion_tested": "Exact radial ODE, Frobenius normalization and intertwiner identities; nine independent finite eigenvalue-product comparisons",
              "software": {"sympy": s.__version__, "mpmath": mp.__version__},
              "zero_frequency_log_residual_series": str(zero_log_series),
              "positive_frequency_log_residual_series": str(pos_log_series),
              "spectral_precision_digits": mp.mp.dps,
              "spectral_N": N, "spectral_rows": rows,
              "spectral_tail": "first two asymptotic terms checked numerically; separate loose variational bracket verified",
              "non_claims": ["Not a full vector/ghost determinant", "Auxiliary reference is not the matched physical vacuum block", "No cancellation of the four-coordinate Jacobian established", "No physical c_H or electromagnetic derivative predicted"]}
    Path(args.result).write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": "passed", "result": args.result}))


if __name__ == "__main__":
    main()
