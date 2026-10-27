#!/usr/bin/env python3
"""Bounded independent checks for horizon normalization and thermal saturation.

Run only through the command in reproduce.sh, or supply a new output JSON path.
No input data fitting. Symbolic identities plus 60-digit numerical quadrature.
"""
import json
import sys
from pathlib import Path

import mpmath as mp
import sympy as s

mp.mp.dps = 60
checks = []
expressions = {}


def ck(name, value):
    if not bool(value):
        raise AssertionError(name)
    checks.append(name)


def eq(name, expression):
    ck(name, s.simplify(expression) == 0)


def fmt(x):
    return mp.nstr(x, 30)


a0, g, u, K, H, c, rho, G, kappa = s.symbols(
    'a0 g u K H c rho G kappa', positive=True)
q, x, zeta, eps = s.symbols('q x zeta eps', positive=True)
Z = s.sqrt(32*s.pi/3)
aH = c*s.sqrt(8*s.pi*G*rho/3)
eq('a0/aH normalization', (kappa*c*s.sqrt(G*rho))/aH
   - kappa*s.sqrt(3/(8*s.pi)))
eq('kappa half implies q0=1/Z', (kappa*s.sqrt(3/(8*s.pi))).subs(kappa,s.Rational(1,2))-1/Z)

W = (-a0*u-a0*a0*s.log(1-u/a0))/K
Wrem = W-u*u/(2*K)
eq('full derivative', K*s.diff(W,u)-a0*u/(a0-u))
eq('remainder derivative', K*s.diff(Wrem,u)-u*u/(a0-u))
usol = a0*g/(a0+g)
eq('simple law from corrected action', g-usol-g*g/(g+a0))
eq('half saturation total field', usol.subs(g,a0)-a0/2)
eq('half saturation baryonic field', (g-usol).subs(g,a0)-a0/2)

simple = g*g/(g+a0)
quadratic = (s.sqrt(a0*a0+4*g*g)-a0)/2
expressions['simple_gN_series'] = str(s.series(simple,g,0,5))
expressions['quadratic_gN_series'] = str(s.series(quadratic,g,0,6))
eq('simple nonzero cubic coefficient',s.expand(s.series(simple,g,0,4).removeO()).coeff(g,3)+1/a0**2)
eq('quadratic zero cubic coefficient',s.expand(s.series(quadratic,g,0,4).removeO()).coeff(g,3))
eq('simple capacity',s.limit(g-simple,g,s.oo)-a0)
eq('quadratic capacity',s.limit(g-quadratic,g,s.oo)-a0/2)
eq('simple at a0',simple.subs(g,a0)-a0/2)
eq('quadratic at a0',quadratic.subs(g,a0)-a0*(s.sqrt(5)-1)/2)

thermal = s.sqrt(1+q*q)
inv = ((1+eps)**2-1)/(s.sqrt((1+eps)**2-1)+zeta)
expressions['inverse_simple_thermal_readout_series'] = str(s.series(inv,eps,0,2))
eq('inverse readout nonanalytic coefficient',s.limit((inv-2*eps/zeta)/eps**s.Rational(3,2),eps,0)+2*s.sqrt(2)/zeta**2)
eq('Milgrom DeltaT deep coefficient',s.limit((thermal-1)/q**2,q,0)-s.Rational(1,2))

# KMS thermal-rate formula checked independently by the shifted Wightman contour.
# W(t-i*pi/alpha)=alpha^2/[16*pi^2*cosh(alpha*t/2)^2].
# r=omega/alpha. Coupling and detector matrix element are divided out.
fourier = []
for r in map(mp.mpf,['0.05','0.2','0.5','1','2']):
    integral = mp.quad(lambda v:mp.cos(2*r*v)/mp.cosh(v)**2,[-mp.inf,0,mp.inf])
    by_integral = mp.exp(-mp.pi*r)*integral/(8*mp.pi**2)
    by_planck = r/(2*mp.pi*mp.expm1(2*mp.pi*r))
    rel = abs(by_integral/by_planck-1)
    ck('Wightman Fourier at omega/alpha='+str(r),rel<mp.mpf('1e-35'))
    fourier.append({'omega_over_alpha':fmt(r),'rate_over_alpha':fmt(by_integral),'relative_difference':fmt(rel)})

zm = mp.sqrt(32*mp.pi/3)
q0, qhalf = 1/zm, 1/(2*zm)
targets = {'a0_over_aH':q0,'ambient_A_over_aH':qhalf}
temperature = {name:{'q':fmt(qv),'fractional_temperature_excess':fmt(mp.sqrt(1+qv*qv)-1)} for name,qv in targets.items()}
rate_rows = []
for x0 in map(mp.mpf,['0.1','1','10','100']):
    qdouble=mp.sqrt((x0/mp.log(1+mp.expm1(x0)/2))**2-1)
    row={'x0_E_over_kBT0':fmt(x0),'q_rate_doubles':fmt(qdouble)}
    for name,qv in targets.items():
        t=mp.sqrt(1+qv*qv)
        row[name+'_rate_ratio']=fmt(mp.expm1(x0)/mp.expm1(x0/t))
    ck('rate doubling inversion at x0='+str(x0),abs(mp.expm1(x0)/mp.expm1(x0/mp.sqrt(1+qdouble*qdouble))-2)<mp.mpf('1e-50'))
    rate_rows.append(row)
root=mp.findroot(lambda xx:mp.expm1(xx)/mp.expm1(xx/mp.sqrt(1+qhalf*qhalf))-2,(180,200))
ck('target rate doubling gap',abs(mp.expm1(root)/mp.expm1(root/mp.sqrt(1+qhalf*qhalf))-2)<mp.mpf('1e-50'))

# Finite detector Gibbs relative entropy, independent trace expression and formula.
information=[]
def qubit_p(xx):
    return 1/(1+mp.exp(xx))
def rel_entropy(xx,qq):
    xx1=xx/mp.sqrt(1+qq*qq)
    p0,p1=qubit_p(xx),qubit_p(xx1)
    trace=p1*mp.log(p1/p0)+(1-p1)*mp.log((1-p1)/(1-p0))
    gibbs=(xx-xx1)*p1+mp.log1p(mp.exp(-xx))-mp.log1p(mp.exp(-xx1))
    ck('relative entropy trace identity '+str(xx)+' '+str(qq),abs(trace-gibbs)<mp.mpf('1e-55'))
    return trace
for x0 in map(mp.mpf,['0.1','1','10']):
    p0=qubit_p(x0)
    leading=x0*x0*p0*(1-p0)/8
    qsmall=mp.mpf('1e-5')
    leading_rel=abs(rel_entropy(x0,qsmall)/(leading*qsmall**4)-1)
    ck('relative entropy quartic asymptotic at x0='+str(x0),leading_rel<mp.mpf('1e-8'))
    information.append({'x0':fmt(x0),'D_at_qhalf':fmt(rel_entropy(x0,qhalf)),
                        'D_at_q0':fmt(rel_entropy(x0,q0)),'q4_coefficient':fmt(leading),
                        'asymptotic_relative_difference_q1e-5':fmt(leading_rel)})

# Ordinary saturating media with unit low-field susceptibility (critical tuning).
ising=s.tanh(x)
langevin=s.coth(3*x)-1/(3*x)
expressions['ising_gN_over_capacity_series']=str(s.series(x-ising,x,0,7))
expressions['langevin_gN_over_capacity_series']=str(s.series(x-langevin,x,0,7))
eq('Ising cubic critical response',s.limit((x-ising)/x**3,x,0)-s.Rational(1,3))
# SymPy 1.14.0 incorrectly returns oo for the unre-written coth expression.
# The series and its exp rewrite independently give 3/5; preserve run_001 failure.
eq('Langevin cubic critical response',s.limit(((x-langevin)/x**3).rewrite(s.exp),x,0)-s.Rational(3,5))
eq('Langevin series independently agrees',s.series(x-langevin,x,0,4).removeO()/x**3-s.Rational(3,5))
eq('Ising saturation',s.limit(ising,x,s.oo)-1)
eq('Langevin saturation',s.limit(langevin,x,s.oo)-1)
eq('simple critical response is quadratic',s.limit((x-x/(1+x))/x**2,x,0)-1)

result={'status':'completed','checks':checks,'symbolic_expressions':expressions,
        'normalization':{'Z':fmt(zm),'q0':fmt(q0),'qhalf':fmt(qhalf)},
        'temperature':temperature,'wightman_fourier':fourier,'detector_rates':rate_rows,
        'x0_required_to_double_at_qhalf':fmt(root),'baseline_qubit_population_at_that_gap':fmt(qubit_p(root)),
        'qubit_relative_entropy':information,
        'non_claims':['No derivation of kappa','No microscopic gravity coupling',
                      'No calculation of an actual galactic circular or geodesic detector',
                      'No universal QFT or quantum-gravity no-go']}
out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
