#!/usr/bin/env python3
"""Exact exterior identities and bounded, independent finite checks.

No full nonlinear global PDE solver, observational fit, or novelty certificate.
Run: python3 verify.py OUTPUT_DIRECTORY
"""
import json
import math
from pathlib import Path
import sys

import numpy as np
import scipy
from scipy.integrate import quad
import sympy as S

OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
checks = []


def zero(name, value):
    result = S.factor(value)
    assert result == 0, (name, result)
    checks.append(name)


# Differentiate the actual vector constitutive flux, without a chosen kernel.
vx, vy, vz = S.symbols('vx vy vz', real=True)
ge, mu0 = S.symbols('ge mu0', positive=True)
L, M = S.symbols('L M', real=True)
mu = S.Function('mu')
variables = [vx, vy, vz]
norm = S.sqrt(vx**2 + vy**2 + vz**2)
F = [mu(norm) * v for v in variables]
background = {vx: 0, vy: 0, vz: ge}
e = [0, 0, 1]
for i in range(3):
    for j in range(3):
        for k in range(3):
            actual = S.diff(F[i], variables[j], variables[k]).subs(background).doit()
            actual = actual.subs({S.diff(mu(ge), ge, 2): mu0*M/ge**2,
                                  S.diff(mu(ge), ge): mu0*L/ge})
            expected = mu0/ge * (L*(e[k]*int(i == j) + e[j]*int(i == k)
                                    + e[i]*int(j == k))
                                    + (M-L)*e[i]*e[j]*e[k])
            zero('constitutive_hessian_%d%d%d' % (i, j, k), actual-expected)

# Stretched cylindrical coordinates: physical z=h*Z, h^2=1+L.
R, Z = S.symbols('R Z', real=True)
h, C = S.symbols('h C', positive=True)
ss = S.sqrt(R**2 + Z**2)
t = Z/ss
A = (L+M/2)/h**2
phi1 = -C/ss
uR, uz = S.diff(phi1, R), S.diff(phi1, Z)/h
BR = mu0/ge * L*uz*uR
Bz = mu0/ge * (L*uR**2/2 + (L+M/2)*uz**2)
divB = S.diff(R*BR, R)/R + S.diff(Bz, Z)/h
phi2 = C**2/(ge*h*ss**3) * ((A-L/2)*t + (3*L/2-A)*t**3)
linear_op_phi2 = mu0*(S.diff(R*S.diff(phi2, R), R)/R
                       + S.diff(phi2, Z, 2))
zero('quadratic_exterior_PDE', linear_op_phi2 + divB)
zero('quadratic_potential_odd', phi2.subs(Z, -Z) + phi2)
zero('linear_potential_even', phi1.subs(Z, -Z) - phi1)
r, K = S.symbols('r K', positive=True)
axis_phi2 = S.simplify(phi2.subs({R: 0, Z: r/h, C: K/h}))
zero('axial_tail_independent_of_mu_second_derivative', axis_phi2-L*K**2/(ge*r**3))
zero('axial_tail_force', -S.diff(axis_phi2, r)-3*L*K**2/(ge*r**4))

# Independent spherical harmonic inversion, including homogeneous ambiguity.
s, tt = S.symbols('s tt', positive=True)
P1, P3 = tt, (5*tt**3-3*tt)/2
a, b = -7*L+2*A, 9*L-6*A
c1, c3 = 2*(L+A)/5, (3*L-2*A)/5
zero('source_harmonics', a*tt+b*tt**3-(-8*(L+A)/5*P1+(18*L-12*A)/5*P3))
zero('P1_inverse', 4*c1-8*(L+A)/5)
zero('P3_inverse', -6*c3+(18*L-12*A)/5)
zero('axial_harmonic_sum', c1+c3-L)

# QUMOND: its second-order RHS has the opposite sign and uses the Newtonian
# monopole in ordinary coordinates. nu_e and n_e replace mu_e and g_e.
kappa_n, mn = S.symbols('kappa_n mn', real=True)
ne, nue, GM = S.symbols('ne nue GM', positive=True)
AN = kappa_n+mn/2
qphi2 = -nue*GM**2/(ne*ss**3)*((AN-kappa_n/2)*t+(3*kappa_n/2-AN)*t**3)
nuR, nuz = GM*R/ss**3, GM*Z/ss**3
NBR = nue/ne*kappa_n*nuz*nuR
NBz = nue/ne*(kappa_n*nuR**2/2+(kappa_n+mn/2)*nuz**2)
zero('QUMOND_quadratic_PDE', S.diff(R*S.diff(qphi2, R), R)/R+S.diff(qphi2, Z, 2)
     -S.diff(R*NBR, R)/R-S.diff(NBz, Z))
zero('QUMOND_axial_tail', S.simplify(qphi2.subs({R: 0, Z: r}))
     +kappa_n*nue*GM**2/(ne*r**3))
zero('QUMOND_physical_normalization', nue*GM**2/ne-(GM*nue)**2/(ne*nue))

# Nuisance multipoles are retained, rather than assigned zero.
d, B, o = S.symbols('d B o', real=True)
asym = 2*d/r**3+3*B/r**4+4*o/r**5
filtered = S.expand(asym-8*asym.subs(r, 2*r))
zero('two_radius_filter', filtered-3*B/(2*r**4)-3*o/r**5)
three = S.expand(asym-40*asym.subs(r, 2*r)+256*asym.subs(r, 4*r))
zero('three_radius_filter', three+3*B/(2*r**4))
beta = (L-1)/(2*(1+L))
zero('AQUAL_orbit_elimination', L*(1-2*beta)-(1+2*beta))
zero('QUMOND_orbit_elimination', 2*L/(1+L)-(1+2*beta))
zero('Newtonian_quadratic_potential', phi2.subs({L: 0, M: 0}))
# A freely selectable dipole invalidates a raw asymmetry inference.
zero('unfiltered_dipole_contamination', ge*r**4*asym/(3*K**2)
     -(2*ge*d*r/(3*K**2)+ge*B/K**2+4*ge*o/(3*K**2*r)))
# Integration by parts giving the induced dipole for a regular radial source.
qfun = S.Function('q')(s)
zero('dipole_energy_integration_by_parts',
     3*s**3*qfun*S.diff(qfun, s)+2*s**2*qfun**2
     -(S.diff(3*s**3*qfun**2/2, s)-5*s**2*qfun**2/2))

# Direct full nonlinear operator residual, evaluated from potential derivatives.
# A quadratic exterior construction must improve r^-5 to r^-7 for these cases.
# This tests actual mu, not the Taylor polynomial used above.
g = S.symbols('g', positive=True)
kernels = {'deep': g, 'simple': g/(1+g),
           'rational': g*(g+2)/(1+g)**2, 'standard': g/S.sqrt(1+g*g)}
def differential_data(potential):
    return S.lambdify((R, Z, h, C, ge, L, M),
                     [S.diff(potential, R), S.diff(potential, Z)/h,
                      S.diff(potential, R, 2), S.diff(potential, Z, 2)/h**2,
                      S.diff(potential, R, Z)/h, S.diff(potential, R)/R], 'numpy')

first_data, second_data = differential_data(phi1), differential_data(phi1+phi2)
residual_rows = []
for name, expr in kernels.items():
    muf = S.lambdify(g, expr, 'numpy')
    dmuf = S.lambdify(g, S.diff(expr, g), 'numpy')
    lm = S.lambdify(g, g*S.diff(expr, g)/expr, 'numpy')
    mm = S.lambdify(g, g*g*S.diff(expr, g, 2)/expr, 'numpy')
    for background_g in [0.2, 1.0, 5.0]:
        lv, mv = float(lm(background_g)), float(mm(background_g))
        hv = math.sqrt(1+lv)
        cv = background_g/hv  # K=ge, so axial |u1|/ge=1/r^2.
        before, after = [], []
        for rad in [8.0, 16.0, 32.0, 64.0]:
            values = []
            for evaluator in [first_data, second_data]:
                residuals = []
                for theta in [0.29, 0.63, 1.02, 1.37, 2.22]:
                    rr, zz = rad*math.sin(theta), rad*math.cos(theta)/hv
                    ur, uz_, hrr, hzz, hrz, hyy = evaluator(rr, zz, hv, cv, background_g, lv, mv)
                    vz_ = background_g+uz_
                    mag = math.hypot(ur, vz_)
                    residual = muf(mag)*(hrr+hzz+hyy)+dmuf(mag)/mag*(ur*ur*hrr+2*ur*vz_*hrz+vz_*vz_*hzz)
                    residuals.append(float(residual))
                values.append(float(np.linalg.norm(residuals)))
            before.append(values[0])
            after.append(values[1])
        order1 = math.log2(before[-2]/before[-1])
        order2 = math.log2(after[-2]/after[-1])
        assert 4.9 < order1 < 5.1, (name, background_g, order1)
        assert 6.85 < order2 < 7.15, (name, background_g, order2)
        residual_rows.append(dict(kernel=name, ge=background_g, L=lv, M=mv,
                                  linear_residuals=before, quadratic_residuals=after,
                                  linear_order=order1, quadratic_order=order2))

# The same direct-operator test for QUMOND, where the potential is driven by
# the independently specified Newtonian field, rather than by its own gradient.
qphi1 = -nue*GM/ss*(1+kappa_n*(1-t*t)/2)
q_laps = [S.lambdify((R, Z, nue, GM, ne, kappa_n, mn),
                    S.diff(R*S.diff(p, R), R)/R+S.diff(p, Z, 2), 'numpy')
          for p in [qphi1, qphi1+qphi2]]
q_residual_rows = []
nu_kernels = {'deep': g**(-S.Rational(1, 2)),
              'simple_dual': S.Rational(1, 2)+S.sqrt(S.Rational(1, 4)+1/g),
              'standard_dual': S.sqrt(S.Rational(1, 2)+S.sqrt(S.Rational(1, 4)+1/g**2))}
for name, expr in nu_kernels.items():
    nuf = S.lambdify(g, expr, 'numpy')
    dnuf = S.lambdify(g, S.diff(expr, g), 'numpy')
    kf = S.lambdify(g, g*S.diff(expr, g)/expr, 'numpy')
    mf = S.lambdify(g, g*g*S.diff(expr, g, 2)/expr, 'numpy')
    for en in [0.2, 1.0, 5.0]:
        nv, kv, mv, mass = float(nuf(en)), float(kf(en)), float(mf(en)), en
        errors = [[], []]
        for rad in [8.0, 16.0, 32.0, 64.0]:
            for j, lap in enumerate(q_laps):
                residuals = []
                for theta in [0.29, 0.63, 1.02, 1.37, 2.22]:
                    rr, zz = rad*math.sin(theta), rad*math.cos(theta)
                    nr, nz = mass*rr/rad**3, en+mass*zz/rad**3
                    hrr, hzz = mass*(1/rad**3-3*rr*rr/rad**5), mass*(1/rad**3-3*zz*zz/rad**5)
                    hrz = -3*mass*rr*zz/rad**5
                    mag = math.hypot(nr, nz)
                    rhs = dnuf(mag)/mag*(nr*nr*hrr+2*nr*nz*hrz+nz*nz*hzz)
                    residuals.append(lap(rr, zz, nv, mass, en, kv, mv)-rhs)
                errors[j].append(float(np.linalg.norm(residuals)))
        orders = [math.log2(e[-2]/e[-1]) for e in errors]
        assert 4.9 < orders[0] < 5.1 and 6.85 < orders[1] < 7.15, (name, en, orders)
        q_residual_rows.append(dict(kernel=name, ne=en, K_nu=kv, M_nu=mv,
                                    linear_residuals=errors[0], quadratic_residuals=errors[1],
                                    linear_order=orders[0], quadratic_order=orders[1]))

# Independent second-order global weak-source calculation. Compact positive
# densities (1-s^2)^p inside s=1 in stretched coordinates; smooth at the edge.
# Derive forcing by integrating its angular components, then solve radial
# Green integrals including the complete source interior and exterior.
nodes, weights = np.polynomial.legendre.leggauss(16)
compact_rows = []
for lv, mv in [(1.0, 0.0), (1/3, -1/3), (0.8, -0.3), (0.0, 0.0)]:
    hv = math.sqrt(1+lv)
    av = (lv+mv/2)/(1+lv)
    cv, eg = 0.02, 1.0
    kval = cv*hv
    for power in [2, 4, 6]:
        coeff = [(-1)**j*math.comb(power, j)/(2*j+3) for j in range(power+1)]
        normalization = sum(coeff)
        def enclosed(x):
            if x >= 1:
                return 1.0, 0.0
            mass = sum(c*x**(2*j+3) for j, c in enumerate(coeff))/normalization
            dm = x*x*(1-x*x)**power/normalization
            return mass, dm
        def forcing(x, ell):
            mass, dm = enclosed(x)
            q = cv*mass/x**2
            dq = cv*(dm/x**2-2*mass/x**3)
            aa = 3*lv*q*dq+(2*av-lv)*q*q/x
            bb = (2*av-3*lv)*(q*dq-q*q/x)
            angular = -(aa*nodes+bb*nodes**3)/(eg*hv)
            leg = nodes if ell == 1 else (5*nodes**3-3*nodes)/2
            return (2*ell+1)/2*float(np.dot(weights, angular*leg))
        def radial_derivative(radius, ell):
            # d/ds of the Green solution; boundary terms cancel analytically.
            inner = quad(lambda x: x**(ell+2)*forcing(x, ell), 0, 1,
                         epsabs=1e-24, epsrel=1e-10)[0]
            inner += quad(lambda x: x**(ell+2)*forcing(x, ell), 1, radius,
                          epsabs=1e-24, epsrel=1e-10)[0]
            outer = quad(lambda x: x**(1-ell)*forcing(x, ell), radius, np.inf,
                         epsabs=1e-24, epsrel=1e-10)[0]
            return ((ell+1)*inner/radius**(ell+2)-ell*radius**(ell-1)*outer)/(2*ell+1)
        def odd_force(rad):
            return -(radial_derivative(rad/hv, 1)+radial_derivative(rad/hv, 3))/hv
        energy_integral = quad(lambda x: (cv*enclosed(x)[0]/x)**2, 0, 1,
                               epsabs=1e-24, epsrel=1e-10)[0]+cv*cv
        predicted_dipole = -(lv+av)*hv/(3*eg)*energy_integral
        dipole_source_integral = quad(lambda x: x**3*forcing(x, 1), 0, 1,
                                      epsabs=1e-24, epsrel=1e-10)[0]
        dipole_source_integral += quad(lambda x: x**3*forcing(x, 1), 1, np.inf,
                                       epsabs=1e-24, epsrel=1e-10)[0]
        integrated_dipole = -hv*hv*dipole_source_integral/3
        assert abs(predicted_dipole-integrated_dipole) < 1e-14
        def estimator(rad):
            return 2*eg*rad**4/(3*kval**2)*(odd_force(rad)-8*odd_force(2*rad))
        for rad in [4*hv, 8*hv, 16*hv]:
            est = estimator(rad)
            rich = 2*estimator(2*rad)-est
            assert abs(rich-lv) < 2e-7, (lv, mv, power, rad, rich)
            compact_rows.append(dict(L=lv, M=mv, density_power=power, r=rad,
                                     physical_dipole=predicted_dipole,
                                     integrated_dipole=integrated_dipole,
                                     raw_inference=eg*rad**4*odd_force(rad)/(3*kval**2),
                                     two_radius=est, three_radius=rich, expected=lv))

result = {'status': 'exact quadratic identities and stated finite checks passed',
          'exact_checks': checks, 'exact_check_count': len(checks),
          'nonlinear_residual_cases': residual_rows,
          'qumond_residual_cases': q_residual_rows,
          'compact_source_cases': compact_rows,
          'max_compact_three_radius_error': max(abs(x['three_radius']-x['expected']) for x in compact_rows),
          'software': {'python': sys.version, 'numpy': np.__version__,
                       'scipy': scipy.__version__, 'sympy': S.__version__},
          'non_claims': ['No existence/completeness proof of the asymptotic series for all sources',
                         'No full nonlinear global PDE solve',
                         'No observational detection or forecast', 'No global novelty established']}
(OUT/'result.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'exact_check_count': len(checks), 'nonlinear_residual_cases': len(residual_rows),
                  'qumond_residual_cases': len(q_residual_rows),
                  'compact_source_cases': len(compact_rows),
                  'max_compact_three_radius_error': result['max_compact_three_radius_error']}, indent=2))
