#!/usr/bin/env python3
"""Exact local WYY turning gate; no gravitational force-law interpretation."""
import sympy as S
Y,U,d,ell,beta,z=S.symbols('Y U d ell beta z',positive=True)
W=U+2*d*ell*(S.sqrt(1+Y/ell)-1)+beta*Y**S.Rational(3,2)
wy=S.diff(W,Y);wyy=S.diff(wy,Y)
checks=[]
def eq(name,a,b=0):
    assert S.simplify(a-b)==0,(name,S.simplify(a-b))
    checks.append(name);print('PASS',name)
eq('direct WYY derivative',wyy,-d/(2*ell)*(1+Y/ell)**(-S.Rational(3,2))+3*beta/(4*S.sqrt(Y)))
beta_at_root=S.solve(wyy,beta)[0]
eq('positive-root equation squared without sign ambiguity',beta_at_root**2,4*d*d/(9*ell)*(Y/ell)/(1+Y/ell)**3)
f=z/(1+z)**3
eq('turning profile derivative',S.diff(f,z),(1-2*z)/(1+z)**4)
eq('sharp profile maximum',f.subs(z,S.Rational(1,2)),S.Rational(4,27))
eq('exact global bound factorization',4*(1+z)**3-27*z,(2*z-1)**2*(z+4))
eq('beta threshold',4*d*d/(9*ell)*S.Rational(4,27),16*d*d/(243*ell))
eq('near-origin WYY positive leading coefficient',S.limit(S.sqrt(Y)*wyy,Y,0),3*beta/4)
eq('large-Y WYY positive leading coefficient',S.limit(S.sqrt(Y)*wyy,Y,S.oo),3*beta/4)
# beta=1/6, d=ell=1: 9 beta²/4=1/16. Derive polynomial first.
poly=S.Poly((1+z)**3-16*z,z)
computed=S.nroots(poly,maxsteps=100)
positive=sorted(float(S.re(x)) for x in computed if abs(float(S.im(x)))<1e-12 and float(S.re(x))>0)
assert len(positive)==2
checks.append('computed below-threshold polynomial has two positive roots')
print('ROOTS below threshold beta=1/6,d=ell=1:',computed)
sample=(positive[0]/2,(positive[0]+positive[1])/2,2*positive[1])
signs=[float(wyy.subs({Y:x,d:1,ell:1,beta:S.Rational(1,6)})) for x in sample]
assert signs[0]>0 and signs[1]<0 and signs[2]>0
checks.append('computed roots give plus minus plus derivative signs')
print('WYY samples',list(zip(sample,signs)))
eq('double root polynomial at threshold',4*(1+z)**3-27*z,(2*z-1)**2*(z+4))
above=S.Poly((1+z)**3-z,z)
above_roots=S.nroots(above,maxsteps=100)
assert not any(abs(float(S.im(x)))<1e-12 and float(S.re(x))>0 for x in above_roots)
checks.append('computed above-threshold polynomial has no positive roots')
print('ROOTS above threshold beta=2/3,d=ell=1:',above_roots)
assigned=(3*beta*ell/(2*d))**2
small_parameter=9*beta**2*ell/(4*d*d)
eq('assigned Y is lower-root small-beta approximation',assigned/ell,small_parameter)
P=-U*S.log((U+2*d*Y)/U)/2
C=-2*S.diff(P+W,Y)
eq('physical scalar stiffness positive-beta leading sign',S.limit(C/S.sqrt(Y),Y,0),-3*beta)
eq('physical radial stiffness leading sign',S.limit((C+2*Y*S.diff(C,Y))/S.sqrt(Y),Y,0),-6*beta)
eq('negative added operator reverses leading scalar stiffness',S.limit(C.subs(beta,-beta)/S.sqrt(Y),Y,0),3*beta)
print('ALL',len(checks),'CHECKS PASSED')
