#!/usr/bin/env python3
"""Bounded fixed-canonical-state minimization; no halo or time evolution."""
import json
import pathlib
import sys

import scipy.optimize as opt
import sympy as s

OUT = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parent / 'run' / 'results.json'
a, m2, lam, y, K, dK = s.symbols('a m2 lam y K dK', positive=True)
W = K / (1 + a*y) + m2*y/2 + lam*y*y/4
Ky = (m2 + lam*y)*(1 + a*y)**2/(2*a)
D = lam + 2*a*m2
Kstar = m2/(2*a)
Wbranch = s.factor(W.subs(K, Ky))
Pbranch = s.factor((s.Rational(5, 3)*K/(1+a*y)-W).subs(K, Ky))
dPdK = s.factor(s.diff(Pbranch, y)/s.diff(Ky, y))
dPdK_target = (2*lam-a*m2+a*lam*y)/(3*(1+a*y)*(D+3*a*lam*y))
assert s.simplify(dPdK-dPdK_target) == 0
assert s.simplify(s.diff(Wbranch, y)/s.diff(Ky, y)-1/(1+a*y)) == 0
assert s.simplify(Pbranch-(m2/(3*a)+(lam/(3*a)-m2/6)*y+lam*y*y/12)) == 0
series = s.series(W.subs({K: Kstar+dK, y: 2*a*dK/D}), dK, 0, 3).removeO()
assert s.simplify(series-(Kstar+dK-a*a*dK*dK/D)) == 0
# The y^2 coefficient in K(y) fixes the next threshold order if needed.
assert s.simplify(s.diff(Ky, y).subs(y, 0)-D/(2*a)) == 0


def state(k, aa=1., mm=1., ll=1.):
    threshold = mm/(2*aa)
    if k <= threshold:
        yy = 0.
    else:
        upper = max(1., (2*k/(aa*ll))**(1/3))
        yy = opt.brentq(lambda z: mm+ll*z-2*aa*k/(1+aa*z)**2,
                        0., upper, xtol=1e-14, rtol=1e-14)
    ww = k/(1+aa*yy)+mm*yy/2+ll*yy*yy/4
    pp = (5/3)*k/(1+aa*yy)-ww
    slope = ((2*ll-aa*mm+aa*ll*yy)/(3*(1+aa*yy)*(ll+2*aa*mm+3*aa*ll*yy))
             if k > threshold else 2/3)
    return yy, ww, pp, slope


checks = []
max_pressure_error = 0.
max_compressibility_error = 0.
max_minimizer_relative_error = 0.
for ll in (.1, .5, 1., 3.):
    for k in (.25, 1., 10., 100.):
        yy, ww, pp, slope = state(k, ll=ll)
        eps = 1e-5
        # Independent pressure check: E(b)=b^3 Wmin(K0/b^5), V(b)=b^3.
        energy = lambda b: b**3 * state(k/b**5, ll=ll)[1]
        pfd = -(energy(1+eps)-energy(1-eps))/(6*eps)
        h = eps*k
        dfd = (state(k+h, ll=ll)[2]-state(k-h, ll=ll)[2])/(2*h)
        max_pressure_error = max(max_pressure_error, abs(pfd-pp)/max(1., abs(pp)))
        max_compressibility_error = max(max_compressibility_error, abs(dfd-slope))
        if k > .5:
            upper = 2*(2*k/ll)**(1/3)
            objective = lambda z: k/(1+z)+z/2+ll*z*z/4
            independent = opt.minimize_scalar(objective, bounds=(0., upper), method='bounded', options={'xatol': 1e-11})
            assert independent.success
            err = abs(independent.x-yy)/max(1., yy)
            max_minimizer_relative_error = max(max_minimizer_relative_error, err)
            assert objective(yy) <= objective(0.)
        checks.append(dict(a=1., m_squared=1., lambda_=ll, K=k, y=yy, W=ww,
                           pressure=pp, pressure_from_volume_derivative=pfd,
                           dP_dK=slope, dP_dK_finite_difference=dfd))
assert max_pressure_error < 2e-8
assert max_compressibility_error < 2e-8
assert max_minimizer_relative_error < 2e-7

threshold = []
for delta in (1e-3, 1e-4, 1e-5):
    yy, ww, pp, _ = state(.5+delta)
    threshold.append(dict(delta_K=delta, y_linear_ratio=yy/(2*delta/3),
                          W_quadratic_ratio=(.5+delta-ww)/(delta*delta/3)))
assert abs(threshold[-1]['y_linear_ratio']-1) < 2e-5
assert abs(threshold[-1]['W_quadratic_ratio']-1) < 2e-5

asymptotic = []
for k in (1e3, 1e6, 1e9, 1e12):
    yy, ww, pp, _ = state(k)
    yasym = (2*k)**(1/3)
    wasym = .75*(2*k)**(2/3)
    kslope = k/((1+yy)*ww)
    asymptotic.append(dict(K=k, y_to_asymptote=yy/yasym, W_to_asymptote=ww/wasym,
                           dlogW_dlogK=kslope, dlogW_dlogrho=(5/3)*kslope,
                           pressure_to_W=pp/ww))
assert abs(asymptotic[-1]['W_to_asymptote']-1) < 2e-4
assert abs(asymptotic[-1]['dlogW_dlogrho']-10/9) < 2e-4
assert abs(asymptotic[-1]['pressure_to_W']-1/9) < 2e-4

ll = .1
yend = (1-2*ll)/ll
kend = (1+ll*yend)*(1+yend)**2/2
assert state(1., ll=ll)[3] < 0
assert state(kend*1.01, ll=ll)[3] > 0

result = dict(
    assertion_tested='Constrained mediator minimization and fixed-canonical affine-family pressure, not a full equation of state for arbitrary distributions',
    exact=dict(K_of_y=str(Ky), W_of_y=str(Wbranch), pressure_of_y=str(Pbranch),
               dP_dK=str(dPdK), threshold_energy_series=str(s.simplify(series)),
               large_K_y='(2*K/(a*lambda))^(1/3)',
               large_K_W='(3/4)*lambda^(1/3)*(2*K/a)^(2/3)'),
    max_relative_pressure_error=max_pressure_error,
    max_absolute_compressibility_error=max_compressibility_error,
    max_relative_minimizer_error=max_minimizer_relative_error,
    finite_checks=checks, threshold_checks=threshold, asymptotic_checks=asymptotic,
    negative_compressibility_example=dict(a=1., m_squared=1., lambda_=ll,
                                         K_start=.5, y_end=yend, K_end=kend),
    non_claims=['No universal density-only EOS without an ensemble or kinetic closure',
                'No covariant field-to-kinetic derivation, halo evolution, or phase formation',
                'Reduced negative compressibility is not a complete coupled mode-spectrum calculation',
                'No exclusion of a tuned approximation to a logarithm on a short finite interval',
                'No derived Lambda normalization'])
OUT.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k: v for k, v in result.items() if k != 'finite_checks'}, indent=2))
