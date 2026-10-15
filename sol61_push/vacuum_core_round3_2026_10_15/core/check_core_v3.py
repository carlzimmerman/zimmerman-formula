#!/usr/bin/env python3
"""Bounded exact audit of VC3-CORE-001; never a full-theory pass flag."""
import json
import math
import sys
from pathlib import Path
import sympy as s
import mpmath as mp

checks = []


def eq(name, left, right=0):
    value = s.simplify(left - right)
    if value != 0:
        raise AssertionError((name, value))
    checks.append(name)


def interval_add(a, b):
    return a[0] + b[0], a[1] + b[1]


def interval_mul(a, b):
    values = [x*y for x in a for y in b]
    return min(values), max(values)


def scale(value, factor):
    return interval_mul(value, (factor, factor))


def atan_interval(z, terms=24):
    total = sum((-1)**k*z**(2*k+1)/s.Integer(2*k+1)
                for k in range(terms))
    next_term = (-1)**terms*z**(2*terms+1)/s.Integer(2*terms+1)
    return min(total, total+next_term), max(total, total+next_term)


r, u, G, M, b, f, q, bq = s.symbols('r u G M b f q bq', positive=True)
rho = 3*M*b*b/(4*s.pi*(r*r+b*b)**s.Rational(5, 2))
mass = M*r**3/(r*r+b*b)**s.Rational(3, 2)
psi = G*M/s.sqrt(r*r+b*b)
gc = G*M*r/(r*r+b*b)**s.Rational(3, 2)
eq('Plummer enclosed mass', s.diff(mass, r), 4*s.pi*r*r*rho)
eq('potential acceleration', s.diff(psi, r), -gc)
eq('density logarithmic derivative', s.diff(rho, r)/rho,
   -5*r/(r*r+b*b))
x = q*(r/b)/(1+(r/b)**2)**s.Rational(3, 2)
cc2 = psi/s.Integer(5)*((1+f)-bq*bq/(1-x))
eq('core hydrostatic inverse EOS', cc2*s.diff(rho, r),
   -rho*gc*((1+f)-bq*bq/(1-x)))
eq('neutral hydrostatic EOS', (1+f)*psi/s.Integer(5)*s.diff(f*rho, r),
   -f*rho*(1+f)*gc)
y = s.symbols('y', positive=True)
eq('charge profile in density variable',
   (q*(r/b)/(1+(r/b)**2)**s.Rational(3, 2))**2,
   (q*(b/s.sqrt(r*r+b*b))**2*s.sqrt(1-b*b/(r*r+b*b)))**2)
eq('charge field maximum', s.diff(q*r/(1+r*r)**s.Rational(3, 2), r)
   .subs(r, 1/s.sqrt(2)), 0)
eq('charge maximum value', (q*r/(1+r*r)**s.Rational(3, 2))
   .subs(r, 1/s.sqrt(2)), 2*q/(3*s.sqrt(3)))

Y = 25*r**3/((1+r*r)**2*(25+r*r))
YP = s.diff(Y, r)
A = (1+r*r)**2/(15*r*r)
B = Y*Y/(r*r)
phi = r/(1+r*r)**s.Rational(3, 2)
ia = s.Rational(1375, 93312)*s.pi
ib = s.Rational(3125, 124416)*s.pi
ib2 = s.Rational(948125, 429981696)*s.pi
iap = (-s.Rational(40715125, 55037657088)*s.sqrt(6)*s.pi
       +s.Rational(40715125, 27518828544)*s.sqrt(6)*s.atan(s.sqrt(6)/12)
       +s.Rational(266435675, 16052649984))
ibp = (-s.Rational(2796875, 9172942848)*s.sqrt(6)*s.pi
       +s.Rational(2796875, 4586471424)*s.sqrt(6)*s.atan(s.sqrt(6)/12)
       +s.Rational(64913125, 2675441664))
for name, expr, expected in [('IA', A*YP**2, ia), ('IB', B, ib),
                              ('IBphi2', B*phi**2, ib2)]:
    eq('exact integral '+name, s.integrate(expr, (r, 0, s.oo)), expected)
for name, expr, expected in [('IAphi', A*YP**2*phi, iap),
                              ('IBphi', B*phi, ibp)]:
    rational_u = s.simplify(s.powdenest(
        s.cancel(expr*u/r).subs(r*r, u*u-1), force=True))
    eq('exact integral '+name, s.integrate(rational_u, (u, 1, s.oo)), expected)
T = s.simplify(-iap+2*ibp)
expected_T = (s.Rational(512521825, 16052649984)
              +s.Rational(7152625, 55037657088)*s.sqrt(6)*s.pi
              -s.Rational(7152625, 27518828544)*s.sqrt(6)*s.atan(s.sqrt(6)/12))
eq('first-order field correction', T, expected_T)
k = s.Rational(8, 5)
L = s.simplify((1+k*k)*ia-2*k*ib+s.Rational(13, 5)*T)
coefficient_B = s.simplify(k*k*(ia-ib)
              +3*s.Rational(13, 5)**2/(1-s.Rational(1, 1000))**2*ib2)
eq('positive quadratic bound coefficient', coefficient_B,
   s.Rational(1101207665, 60405709824)*s.pi)
eq('mass conserved at center', s.limit(Y, r, 0), 0)
eq('mass conserved at infinity', s.limit(Y, r, s.oo), 0)
eq('finite-inertia mass tail power', s.limit(r**3*Y, r, s.oo), 25)
rho_unit = 3/(4*s.pi*(1+r*r)**s.Rational(5, 2))
eq('bounded displacement tail', s.limit(-Y/(4*s.pi*r*r*rho_unit), r, s.oo), -s.Rational(25, 3))
z = s.symbols('z', real=True)
eq('electric remainder identity', (1-z)**-2-1-2*z,
   z*z*(3-2*z)/(1-z)**2)
eq('charge bound rational comparison', s.Rational(13, 5)**2-s.Rational(27, 4),
   s.Rational(1, 100))

# Pi is bounded by Machin's identity and alternating arctangent series.
# tan(4 atan(1/5)-atan(1/239))=1 with angle in (0, pi/2).
tan_double = lambda v: 2*v/(1-v*v)
tan_four = tan_double(tan_double(s.Rational(1, 5)))
eq('Machin tangent identity',
   (tan_four-s.Rational(1, 239))/(1+tan_four/s.Integer(239)), 1)
pi_interval = interval_add(scale(atan_interval(s.Rational(1, 5)), 16),
                           scale(atan_interval(s.Rational(1, 239)), -4))
den = 10**30
sqrt_lower_n = math.isqrt(6*den*den)
sqrt_interval = (s.Rational(sqrt_lower_n, den),
                 s.Rational(sqrt_lower_n+1, den))
assert sqrt_interval[0]**2 < 6 < sqrt_interval[1]**2
sqrt_pi_interval = interval_mul(sqrt_interval, pi_interval)
# sqrt(6)*atan(sqrt(6)/12) has rational alternating terms.
terms = 18
tau_partial = sum((-1)**j*s.Rational(6**(j+1), 12**(2*j+1)*(2*j+1))
                  for j in range(terms))
tau_next = (-1)**terms*s.Rational(6**(terms+1), 12**(2*terms+1)*(2*terms+1))
tau_interval = (min(tau_partial, tau_partial+tau_next),
                 max(tau_partial, tau_partial+tau_next))


def evaluate(expr):
    pp, sp, tau = s.symbols('pp sp tau')
    poly = s.expand(expr).subs(s.sqrt(6)*s.atan(s.sqrt(6)/12), tau)
    poly = poly.subs(s.sqrt(6)*s.pi, sp).subs(s.pi, pp)
    result = (s.S(0), s.S(0))
    substitutions = {pp: pi_interval, sp: sqrt_pi_interval, tau: tau_interval}
    for variable in [pp, sp, tau]:
        coeff = s.expand(poly).coeff(variable)
        assert not coeff.free_symbols
        result = interval_add(result, scale(substitutions[variable], coeff))
        poly = s.expand(poly-coeff*variable)
    assert not poly.free_symbols
    return interval_add(result, (poly, poly))


T_interval = evaluate(T)
B_interval = evaluate(coefficient_B)
margin_interval = evaluate(L+coefficient_B/1000)
assert T_interval[0] > 0
assert B_interval[0] > 0
assert margin_interval[0] > -s.Rational(2369, 10**6)
assert margin_interval[1] < -s.Rational(2368, 10**6)
checks.extend(['positive T exact interval', 'positive B exact interval',
               'uniform family negative upper bound exact interval'])

fw = s.Rational(1, 1000)
qw = s.Rational(1, 400)
eps = s.Rational(1, 10**6)
assert s.simplify(fw/(1+fw)-2*qw/(3*s.sqrt(3))) > 0
gate_bound = eps*qw*s.Rational(1, 2)/(3*s.Rational(999, 1000)**3)
assert gate_bound < s.Rational(1, 10**9)
checks.extend(['assigned witness positive pressure', 'assigned witness principal gate bound'])

mp.mp.dps = 60
fm = mp.mpf(1)/1000
qm = mp.mpf(1)/400
km = mp.mpf(8)/5


def integrand(rr):
    xx = qm*rr/(1+rr*rr)**mp.mpf('1.5')
    yy = 25*rr**3/((1+rr*rr)**2*(25+rr*rr))
    yp = yy*(3/rr-4*rr/(1+rr*rr)-2*rr/(25+rr*rr))
    aa = (1+rr*rr)**2/(15*rr*rr)
    return (aa*yp*yp*((1+fm)-1/(1-xx)+fm*(1+fm)*km*km)
            +yy*yy/(rr*rr)*((1-xx)**-2-(1+fm*km)**2))


quadrature = mp.quad(integrand, [0, mp.mpf('0.5'), 1, 3, 10, mp.inf])
q0part = fw*(1+(1+fw)*k*k)*ia-(2*fw*k+fw*fw*k*k)*ib
upper_witness = s.simplify(q0part+qw*T
                +3*qw*qw/(1-s.Rational(1, 1000))**2*ib2)
upper_witness_interval = evaluate(upper_witness)
assert quadrature < mp.mpf(str(s.N(upper_witness_interval[0], 50))) < 0
result = {
    'claim_id': 'VC3-CORE-001',
    'exact_checks': len(checks),
    'check_names': checks,
    'family': 'Critical q/m; co-Plummer densities; 0<f<=1/1000; x_max<f/(1+f)',
    'family_Q_over_f_upper_rational_interval': [str(v) for v in margin_interval],
    'family_Q_over_f_upper_decimal_interval': [str(s.N(v, 40)) for v in margin_interval],
    'trial': 'delta m_c=25r^3/[(1+r^2)^2(25+r^2)], delta m_s=(8/5) f delta m_c',
    'assigned_witness': {'f': '1/1000', 'q0': '1/400', 'epsilon0': '1/1000000'},
    'witness_quadrature_60_digits': mp.nstr(quadrature, 55),
    'witness_analytic_upper_bound': str(s.N(upper_witness, 50)),
    'witness_hcrit_over_hstar_bound': str(gate_bound),
    'interpretation': 'Exact equilibrium but negative coupled radial density/Gauss energy; no full-theory closure or full spectral theorem.'
}
Path(sys.argv[1]).write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'exact_checks': len(checks),
                  'negative_family_margin': result['family_Q_over_f_upper_decimal_interval'],
                  'witness_Q': result['witness_quadrature_60_digits']}))
