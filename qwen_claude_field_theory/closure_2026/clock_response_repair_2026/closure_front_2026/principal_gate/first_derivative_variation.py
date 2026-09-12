#!/usr/bin/env python3
"""Differentiate exact metric/clock invariants before imposing a local frame.

Checks the non-cubic stress and both variational currents of P-V+sW. Cubic
curvature variation is separate in metric_response and earlier braiding work.
"""
import json
import sympy as S


def derive():
    q, s = S.symbols('q s', positive=True)
    P, V, W, PX, WY = S.symbols('P V W PX WY', real=True)
    vv = S.Matrix(S.symbols('v0:4', real=True))
    tt = S.Matrix(S.symbols('t0:4', real=True))
    ij = [(i, j) for i in range(4) for j in range(i, 4)]
    entries = S.symbols('h0:10', real=True)
    inv = S.zeros(4)
    for pair, value in zip(ij, entries):
        i, j = pair
        inv[i, j] = inv[j, i] = value
    metricpoint = dict(zip(entries, [-1, 0, 0, 0, 1, 0, 0, 1, 0, 1]))
    frame = {tt[0]: s, tt[1]: 0, tt[2]: 0, tt[3]: 0, vv[0]: q}
    X = -(vv.T*inv*vv)[0]
    norm = S.sqrt(-(tt.T*inv*tt)[0])
    Q = -(tt.T*inv*vv)[0]/norm
    Y = -X+Q**2
    eta = S.diag(-1, 1, 1, 1)
    n = S.Matrix([-1, 0, 0, 0])
    covv = vv.subs(frame)
    projected = covv+q*n
    L = P-V+s*W
    expected = L*eta+2*PX*covv*covv.T+s*W*n*n.T-2*s*WY*projected*projected.T
    checks = {}
    def check(name, expr):
        result = S.simplify(expr)
        if result != 0:
            raise AssertionError((name, result))
        checks[name] = True
    def atpoint(expr):
        return S.simplify(expr.subs(metricpoint).subs(frame))
    actual = S.zeros(4)
    for (i, j), value in zip(ij, entries):
        deriv = atpoint(PX*S.diff(X, value)+W*S.diff(norm, value)+norm*WY*S.diff(Y, value))
        # A single off-diagonal variable changes g^{ij} AND g^{ji}.
        actual[i, j] = actual[j, i] = L*eta[i, j]-(2 if i == j else 1)*deriv
        check('stress_'+str(i)+str(j), actual[i, j]-expected[i, j])
    for i in range(4):
        chideriv = atpoint(PX*S.diff(X, vv[i])+norm*WY*S.diff(Y, vv[i]))
        expected_chi = -2*PX*(eta*covv)[i]+2*s*WY*(eta*projected)[i]
        check('scalar_current_'+str(i), chideriv-expected_chi)
        tauderiv = atpoint(W*S.diff(norm, tt[i])+norm*WY*S.diff(Y, tt[i]))
        expected_tau = W*(eta*n)[i]-2*q*WY*(eta*projected)[i]
        check('clock_current_'+str(i), tauderiv-expected_tau)
    # Canonical scalar limit fixes the stress/energy sign, independently.
    canonical = actual.subs({PX:S.Rational(1,2), P:(q*q-sum(x*x for x in vv[1:]))/2,
                             V:0, W:0, WY:0})
    check('canonical_scalar_positive_energy', canonical[0,0]-(q*q+sum(x*x for x in vv[1:]))/2)
    return dict(scope='Exact local invariant variations in a clock-rest orthonormal frame; not full cubic Dirac analysis',
                tensor=str(actual), checks=checks,
                general_formulas={
                    'u_mu':'partial_mu chi + Q n_mu',
                    'T_PVW':'(P-V+sW)g_mu_nu+2PX chi_mu chi_nu+sW n_mu n_nu-2sWY u_mu u_nu',
                    'E_chi_noncubic':'2 nabla_mu(PX nabla^mu chi-sWY u^mu)',
                    'E_tau':'P_tau-V_tau+s W_tau - nabla_mu(W n^mu-2Q WY u^mu)'},
                software={'sympy':S.__version__})


if __name__ == '__main__':
    print(json.dumps(derive(), indent=2))
