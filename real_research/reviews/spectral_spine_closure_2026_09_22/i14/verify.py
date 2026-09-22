"""Independent finite-matrix checks and exact source-Hessian algebra.

Run from repository root with one output-JSON path argument. No source files
are executed. Floating matrix checks are regression evidence, not the proof
of the universal diagonalization. Exact symbolic claims are also derived in
DERIVATION.md and SOURCE_BRIDGE.md.
"""
import json
import sys
from pathlib import Path
import numpy as np
import sympy as sp

rows = []
for N in (2, 3, 4, 8, 31, 128):
    # Build the ORIGINAL squared form, not the claimed tridiagonal answer.
    B = np.zeros((N, N - 1))
    for n in range(N):
        if 1 <= n + 1 < N:
            B[n, n] += 1.0
        if 1 <= n < N:
            B[n, n - 1] -= 1.5
    for kappa2, mu2, q0 in ((0, 0, 0), (.25, 0, 0), (1, 1, 1),
                              (1.5, 1, 1), (-2, -3, .5)):
        b = .25 - kappa2 + mu2 * q0
        H = B.T @ B + (-kappa2 + mu2 * q0) * np.eye(N - 1)
        j = np.arange(1, N)
        expected = 6 * np.sin(j * np.pi / (2 * N)) ** 2 + b
        V = np.sin(np.outer(j, j) * np.pi / N)
        eigen_error = float(np.max(np.abs(np.linalg.eigvalsh(H) - expected)))
        recurrence_error = float(np.max(np.abs(H @ V - V * expected)))
        gram_error = float(np.max(np.abs(V.T @ V - (N / 2) * np.eye(N - 1))))
        assert eigen_error < 1e-12
        assert recurrence_error < 1e-11
        assert gram_error < 1e-10
        rows.append(dict(N=N, kappa2=kappa2, mu2=mu2, q0=q0,
                         eigen_error=eigen_error, recurrence_error=recurrence_error,
                         gram_error=gram_error, lowest=float(expected[0])))
# Independent minimal box: E/U = 3.25-kappa2+mu2*q0, since A(0,1,0)=3.25.
assert rows[0]['lowest'] == 3.25 or abs(rows[0]['lowest'] - 3.25) < 1e-14

x = sp.symbols('x', positive=True)  # G155's u = sqrt(K), not lattice mode u_n.
f = x**2 - 2*sp.log(1+x) - 2/(1+x) + 1
mu = x*(x+2)/(1+x)**2
assert sp.simplify(sp.diff(f,x)/(2*x) - mu) == 0
ar = sp.factor(mu + x*sp.diff(mu,x))
assert sp.simplify(ar - x*(x*x+3*x+4)/(1+x)**3) == 0
w = sp.factor(ar/x)  # overall positive radius scale omitted
s = sp.factor(-x*sp.diff(w,x)/(2*w))
potential = sp.factor(s*s-x*sp.diff(s,x))
assert sp.limit(potential,x,0) == 0
assert sp.limit(potential,x,sp.oo) == sp.Rational(1,4)
flux = sp.factor(mu/x)  # r² μ φ'/(C a), phi'=C/r and x=a/r
flux_radial_log_derivative = sp.factor(-x*sp.diff(flux,x))
assert sp.simplify(flux_radial_log_derivative - x*(x+3)/(1+x)**3) == 0
assert sp.limit(flux,x,0) == 2
# The frozen f in THE_THEORY L5 is not G155's interpolant.
K = sp.symbols('K', nonnegative=True)
L5_f = K - 1/(1+K)
assert sp.diff(L5_f,K).subs(K,0) == 2
assert sp.limit(mu,x,0) == 0
# General power-law radial gradient coefficient a_r(r)=r^{-p}:
# w(t)=exp((1-p)t), v=sqrt(w)*eta, V=(1-p)^2/4.
p = sp.symbols('p', real=True)
power_potential = (1-p)**2/4
assert power_potential.subs(p,1) == 0
assert power_potential.subs(p,0) == sp.Rational(1,4)

result = dict(
    matrix_checks=rows,
    matrix_case_count=len(rows),
    exact_source_algebra={
        'G155_mu':str(mu), 'G155_radial_hessian_coefficient':str(ar),
        'log_weight_over_radius_scale':str(w), 'dressing_drift':str(s),
        'dressed_potential':str(potential),
        'flux_over_Ca':str(flux),
        'r_dflux_dr_over_Ca':str(flux_radial_log_derivative),
        'deep_dressed_potential':0, 'canonical_dressed_potential':'1/4',
        'L5_fprime_at_zero':2, 'G155_fprime_at_zero':0},
    interpretation='All declared finite checks passed. Universal spectrum uses the written proof; physical Hessian identification remains unestablished.')
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'matrix_cases':len(rows),
    'max_eigen_error':max(r['eigen_error'] for r in rows),
    'max_recurrence_error':max(r['recurrence_error'] for r in rows),
    'max_gram_error':max(r['gram_error'] for r in rows),
    'symbolic_checks':'passed'},indent=2))
