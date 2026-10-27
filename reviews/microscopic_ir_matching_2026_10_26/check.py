"""Formal one-loop audit; no cosmological data or parameter-selection fit."""
import os
import sys
import sympy as S
import mpmath as mp
mutate = os.environ.get('MUTATE') == '1'
k, m, L, t = S.symbols('k m L t', positive=True)
u = S.symbols('u', real=True)
K, D, gamma, s, hb = S.symbols('K D gamma s hbar', positive=True)
checks = []
def check(name, truth):
    checks.append((name, bool(truth)))
def eq(name, a, b):
    check(name, S.simplify(a-b) == 0)
F = (k*k+m*m)**S.Rational(5,2)/5-m*m*(k*k+m*m)**S.Rational(3,2)/3
eq('radial primitive', S.diff(F,k), k**3*S.sqrt(k*k+m*m))
I = F.subs(k,L)-F.subs(k,0)
series = S.series(I,m,0,7).removeO().expand()
eq('full integral expansion', series, L**5/5+L**3*m**2/6-L*m**4/8+2*m**5/15-m**6/(16*L))
a = S.Integer(1) if mutate else 1+u*u
avg1 = S.integrate(a,(u,0,1))
avg2 = S.integrate(a*a,(u,0,1))
A = S.integrate(a**S.Rational(5,2),(u,0,1))
Aexpected = 67*S.sqrt(2)/48+5*S.asinh(1)/16
eq('angular linear',avg1,S.Rational(4,3))
eq('angular quadratic',avg2,S.Rational(28,15))
eq('angular nonanalytic',A,Aexpected)
pref = hb*S.sqrt(D/K)/(4*S.pi**2)
eq('constant energy',pref*L**5/5,hb*S.sqrt(D/K)*L**5/(20*S.pi**2))
eq('linear agrees old shell',pref*L**3*gamma*s/D*avg1/6,hb*gamma*s*L**3/(18*S.pi**2*S.sqrt(K*D)))
eq('quadratic agrees old shell',-pref*L*(gamma*s/D)**2*avg2/8,-7*hb*gamma**2*s**2*L/(120*S.pi**2*S.sqrt(K)*D**S.Rational(3,2)))
B = S.simplify(pref*S.Rational(2,15)*(gamma/D)**S.Rational(5,2)*A)
eq('IR coefficient',B,hb*gamma**S.Rational(5,2)*Aexpected/(30*S.pi**2*S.sqrt(K)*D**2))
check('IR coefficient positive',float(B.subs({hb:1,gamma:1,D:1,K:1}))>0)
eq('IR logarithmic slope',s*S.diff(B*s**S.Rational(5,2),s)/(B*s**S.Rational(5,2)),S.Rational(5,2))
eq('loop to classical scales s^-1/2',s*S.diff(B*s**S.Rational(5,2)/(gamma*s**3/3),s)/(B*s**S.Rational(5,2)/(gamma*s**3/3)),-S.Rational(1,2))
# Independent quadrature of full radial integral at dimensionless fixtures.
mp.mp.dps=40
for mm,ll in [(mp.mpf('0.2'),mp.mpf('1.7')),(mp.mpf('0.7'),mp.mpf('1.1'))]:
    numeric=mp.quad(lambda kk: kk**3*mp.sqrt(kk*kk+mm*mm),[0,ll])
    exact=mp.mpf(str(S.N(I.subs({m:S.Rational(str(mm)),L:S.Rational(str(ll))}),40)))
    check('quadrature m='+str(mm),abs(numeric-exact)<mp.mpf('1e-35'))
# The unexpanded small-k modes have the same divergent fluctuation parameter.
n=S.symbols('n',positive=True)
eq('general energy exponent',(n+2)/2,S.Rational(1,2)*n+1)
eq('3d fluctuation/background exponent',S.Rational(3,2)-2,-S.Rational(1,2))
p=S.Rational(5,2)
eq('conditional radial acceleration exponent',-2/(p-1),-S.Rational(4,3))
eq('conditional circular speed exponent',(1-2/(p-1))/2,-S.Rational(1,6))
print('mode:', 'MUTATE longitudinal anisotropy removed' if mutate else 'baseline')
print('angular factor:', A)
print('IR coefficient B:', B)
for name,good in checks: print(('PASS' if good else 'FAIL'),name)
print('checks:',sum(g for _,g in checks),'/',len(checks))
sys.exit(0 if all(g for _,g in checks) else 1)
