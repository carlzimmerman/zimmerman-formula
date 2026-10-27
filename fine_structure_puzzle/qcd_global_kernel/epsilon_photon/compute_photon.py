#!/usr/bin/env python3
"""New photon correction, not a repeated compact-Haar numerical grid."""
import json
import pathlib
import sys
import time
import mpmath as mp
import sympy as sp

START = time.monotonic()
mp.mp.dps = 50


def fmt(v):
    return mp.nstr(v, 35)


def exact_pauli_and_gauge():
    I = sp.I
    tau = [sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, -I], [I, 0]]), sp.diag(1, -1)]
    aa = sp.symbols('a0:4', real=True)
    a0, a1, a2, a3 = aa
    unit = a0*a0+a1*a1+a2*a2+a3*a3-1
    U = a0*sp.eye(2)+I*sum((aa[j+1]*tau[j] for j in range(3)), sp.zeros(2))
    Q = sp.eye(2)/6+tau[2]/2
    B = Q*U-U*Q
    bmat = sp.expand(U.conjugate().T*B)
    b = [sp.expand(sp.trace(t*bmat)/2) for t in tau]
    assert sp.expand(sp.trace(B*B.conjugate().T)-2*(a1*a1+a2*a2)) == 0
    assert sp.rem(sp.expand(sum(v*v for v in b)-(a1*a1+a2*a2)), unit, a0) == 0
    assert sp.expand(bmat-sum((b[j]*tau[j] for j in range(3)), sp.zeros(2))) == sp.zeros(2)
    F, e, A = sp.symbols('F e A', real=True, nonzero=True)
    p = sp.symbols('p1:4', real=True)
    P = sum((p[j]*tau[j] for j in range(3)), sp.zeros(2))
    du = U*I*P/F-I*e*A*B
    dud = -I*P*U.conjugate().T/F+I*e*A*B
    action = sp.expand(F**2*sp.trace(du*dud)/4)
    target = sum(v*v for v in p)/2-e*F*A*sum(b[j]*p[j] for j in range(3))
    target += e**2*F**2*A**2*(a1*a1+a2*a2)/2
    assert sp.rem(sp.expand(action-target), unit, a0) == 0
    lamroot, m, alpha = sp.symbols('r m alpha', positive=True)
    K = sp.Matrix([[lamroot**2/alpha+m*m, -m*lamroot], [-m*lamroot, lamroot**2]])
    assert sp.factor(K.det()-lamroot**4/alpha) == 0
    K0 = K.subs(m, 0)
    K1 = K.diff(m).subs(m, 0)
    K2 = K.diff(m, 2).subs(m, 0)/2
    seagull = sp.trace(K0.inv()*K2)/2
    two_mixing = -sp.trace(K0.inv()*K1*K0.inv()*K1)/4
    assert sp.factor(seagull+two_mixing) == 0
    return {'b_components': [str(v) for v in b], 'longitudinal_seagull_coefficient': str(seagull),
            'two_mixing_coefficient': str(two_mixing), 'block_determinant': str(sp.factor(K.det()))}


def heat_coefficients():
    x = sp.Symbol('x')
    a = sp.Rational(9, 4)
    ss = sp.Rational(1, 2)/x**2-a/(2*x)
    for k in range(13):
        z3 = (sp.Rational(2)**(-3-2*k)-1)*sp.zeta(-3-2*k)
        z1 = (sp.Rational(2)**(-1-2*k)-1)*sp.zeta(-1-2*k)
        ss += (-x)**k/sp.factorial(k)*(z3-a*z1)
    # n=1/2 contributes -1 with zero eigenvalue, n=3/2 contributes zero.
    series = sp.series(sp.exp(x/4)*ss+1, x, 0, 11).removeO().expand()
    coeff = {j: series.coeff(x, j) for j in range(-2, 11)}
    assert [coeff[j] for j in range(-2, 3)] == [sp.Rational(1, 2), -1, sp.Rational(19, 30),
                                                -sp.Rational(5, 63), -sp.Rational(11, 630)]
    return coeff


EXACT = heat_coefficients()
NUM = {j: mp.mpf(int(c.p))/int(c.q) for j, c in EXACT.items()}


def heat(t):
    n = int(mp.ceil(mp.sqrt(140/t)))+4
    assert n <= 1000
    return mp.fsum(mp.mpf(l*(l+3)*(2*l+3))/2*mp.exp(-t*(l+1)*(l+2)) for l in range(1, n+1))


def heat_finite_part(split=mp.mpf('.025'), order=10):
    low = mp.fsum(NUM[j]*split**(j+1)/(j+1) for j in range(0, order+1))
    def low_integrand(t):
        return heat(t)-1/(2*t*t)+1/t
    middle = mp.quad(low_integrand, [split, mp.mpf('.1'), mp.mpf('.5'), 1])
    high = mp.quad(heat, [1, 2, 4, 16, mp.inf])
    # zeta(p)=Mellin(K)/Gamma(p); residue=-1 contributes -gamma.
    return low+middle+high-mp.mpf('.5')-mp.euler


def spectral_checks():
    a, c, A = mp.mpf(9)/4, mp.mpf(1)/4, mp.mpf(5)/2
    N = 24
    closed = mp.mpf(2)/3-2*mp.euler
    series = (mp.zeta(-1, A)+(a-c)*mp.digamma(A)+c/2
              +(c-a)*mp.fsum(c**j*mp.zeta(2*j+1, A) for j in range(1, N)))
    ratio = c/(A*A)
    tail = 2*ratio**N*(1/A+mp.mpf(1)/(2*N))/(1-ratio)
    assert abs(series-closed) <= tail
    hv = heat_finite_part()
    hv2 = heat_finite_part(mp.mpf('.02'), 10)
    assert abs(hv-closed) < mp.mpf('1e-20')
    assert abs(hv2-closed) < mp.mpf('1e-20')
    laurent = []
    for eps in [mp.mpf('1e-6'), mp.mpf('1e-8'), mp.mpf('1e-10')]:
        p = 1+eps
        zz = mp.fsum(mp.rf(p, k)*c**k/mp.factorial(k)*
                    (mp.zeta(2*p+2*k-3, A)-a*mp.zeta(2*p+2*k-1, A)) for k in range(N))
        subtracted = zz+1/eps
        assert abs(subtracted-closed) < eps
        laurent.append({'epsilon': str(eps), 'pole_subtracted_finite_estimate': fmt(subtracted),
                        'difference_from_finite_limit': fmt(abs(subtracted-closed))})
    heat_points = []
    for tt in ['.025', '.05', '.1', '.5', '1', '4']:
        t = mp.mpf(tt)
        h = heat(t)
        heat_points.append({'t': tt, 'direct_harmonic_trace': fmt(h)})
    return {'residue_at_p1': '-1', 'finite_part_closed': fmt(closed),
            'finite_part_hurwitz_series': fmt(series), 'finite_series_tail_bound': fmt(tail),
            'finite_part_heat': fmt(hv), 'finite_part_heat_alternate_split': fmt(hv2),
            'heat_difference_from_closed': fmt(abs(hv-closed)),
            'laurent_checks': laurent, 'heat_points': heat_points}


def exact_response_and_renormalization():
    V, u, aa, C = sp.symbols('V u a C', positive=True)
    x, y, t0, td, h, hd, q0, cov, var, kas, kss = sp.symbols('x y t tdot h hdot q c v K_ass K_sss')
    qq = sp.Function('q')
    tf = sp.Function('t')
    xarg, yarg = aa*V, C*u*V
    fun = tf(V, u)*qq(xarg, yarg)
    rho = sp.diff(fun, V)
    source_rho = sp.diff(fun, V, u)
    replacements = {
        tf(V, u): t0, sp.diff(tf(V, u), V): td/V,
        sp.diff(tf(V, u), u): h, sp.diff(tf(V, u), V, u): hd/V,
        qq(xarg, yarg): q0,
        sp.Subs(sp.Derivative(qq(sp.Symbol('_xi_1'), yarg), sp.Symbol('_xi_1')), sp.Symbol('_xi_1'), xarg): cov
    }
    # Replace AppliedUndef derivatives via Subs' variable/order metadata.
    def moment_replace(expr):
        for obj in sorted(expr.atoms(sp.Subs), key=str, reverse=True):
            derivative = obj.expr
            if isinstance(derivative, sp.Derivative) and derivative.expr.func == qq:
                orders = [0, 0]
                arguments = derivative.expr.args
                for variable, count in derivative.variable_count:
                    orders[arguments.index(variable)] += count
                mapping = {(1, 0): cov, (0, 1): -var, (1, 1): -kas, (0, 2): kss}
                if tuple(orders) in mapping:
                    expr = expr.xreplace({obj: mapping[tuple(orders)]})
        return expr
    rr = moment_replace(rho).subs(replacements).subs({aa: x/V, C*u: y/V})
    sr = moment_replace(source_rho).subs(replacements).subs({aa: x/V, C*u: y/V})
    target_rho = (td*q0+t0*(x*cov-y*var))/V
    target_source = (hd*q0+h*(x*cov-y*var))/V-C*((td+t0)*var+t0*(x*kas-y*kss))
    assert sp.simplify(rr-target_rho) == 0, rr
    assert sp.simplify(sr-target_source) == 0, sr
    H, F, mu, kk = sp.symbols('H F mu k', positive=True)
    B = -sp.log(mu**2/H**2)+sp.Rational(2, 3)-2*sp.EulerGamma-64*sp.pi**2*kk
    t = u*F**2*B/(2*H**2)
    dot = -H*sp.diff(t, H)/4
    assert sp.simplify(dot-t/2+u*F**2/(4*H**2)) == 0
    rg = mu*sp.diff(t, mu)-sp.diff(t, kk)/(32*sp.pi**2)
    assert sp.simplify(rg) == 0
    eps, R = sp.symbols('epsilon R', nonzero=True)
    pole = -u*F**2*R*V*q0/(64*sp.pi**2*eps)
    dk = sp.Rational(1, 2)/(16*sp.pi**2*(-2*eps))
    assert sp.simplify(pole-u*F**2*dk*R*V*q0) == 0
    return {'delta_rho': str(target_rho), 'u_derivative_delta_rho': str(target_source),
            'photon_delta_k15': str(dk), 'photon_beta15': '1/2',
            'RG_cancellation': 'exact for photon-only running in the declared finite scheme'}


def main(path):
    result = {'claim_id': 'FSP008_EPSILON_PHOTON_GLOBAL_NLO_COMPONENT',
              'exact_pauli_and_gauge': exact_pauli_and_gauge(),
              'heat_coefficients': {str(j): str(c) for j, c in EXACT.items()},
              'spectral_checks': spectral_checks(),
              'source_metric_renormalization': exact_response_and_renormalization(),
              'numerical_precision_decimal': mp.mp.dps,
              'new_Haar_integral_grid_run': False,
              'empirical_physical_inputs': [],
              'absolute_global_gauge_normalization_calculated': False,
              'pion_Z_counterterm_bridge_resolved': False,
              'full_NLO_partition_calculated': False,
              'alpha_or_full_QCD_ratio_calculated': False,
              'interval_certified': False,
              'software': {'python': sys.version.split()[0], 'mpmath': mp.__version__, 'sympy': sp.__version__},
              'runtime_seconds': time.monotonic()-START}
    pathlib.Path(path).write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({'status': 'finite exact and numerical assertions passed',
                      'residue': '-1', 'finite_part': result['spectral_checks']['finite_part_closed'],
                      'heat_difference': result['spectral_checks']['heat_difference_from_closed'],
                      'photon_beta15': '1/2'}))


if __name__ == '__main__':
    main(sys.argv[1])
