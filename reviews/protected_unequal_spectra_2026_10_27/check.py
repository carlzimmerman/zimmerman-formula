import os,sys
import sympy as S
mutate=os.environ.get('MUTATE')=='1'
checks=[]
def eq(name,a,b): checks.append((name,S.simplify(a-b)==0))
x,A,B,m,s,d,T,phi,R,C=S.symbols('x A B m s d T phi R C',positive=True)
f=S.sqrt(A+B*s)
eq('gapped first derivative',S.diff(f,s),B/(2*S.sqrt(A+B*s)))
eq('gapped second derivative',S.diff(f,s,2),-B**2/(4*(A+B*s)**S.Rational(3,2)))
eq('gapped third derivative',S.diff(f,s,3),3*B**3/(8*(A+B*s)**S.Rational(5,2)))
eq('Taylor remainder bound coefficient',S.diff(f,s,3).subs(s,0)/6,B**3/(16*A**S.Rational(5,2)))
eq('fractional third derivative singular',S.diff(s**S.Rational(5,2),s,3),15/(8*S.sqrt(s)))
# KK counterfactual: twist 1/2 has no fermion zero mode; twist 0 restores it.
alpha=S.Integer(0) if mutate else S.Rational(1,2)
minFgap=alpha/R
net_gapless=S.Integer(1)-S.Integer(alpha==0)
eq('twisted fermion gap',minFgap,1/(2*R))
eq('unmatched gapless IR coefficient',net_gapless,1)
eq('zero twist restores gapless pairing',S.Integer(1)-S.Integer(S.Integer(0)==0),0)
expo=2*d/(d-2)
eq('ten-dimensional Weyl exponent',expo.subs(d,10),S.Rational(5,2))
V=T*S.exp(S.Rational(5,2)*phi)
eq('dilaton slope nonzero',S.diff(V,phi)/V,S.Rational(5,2))
eq('dilaton curvature',S.diff(V,phi,2)/V,S.Rational(25,4))
eq('one-scale Casimir no finite stationary point',S.diff(C/R**d,R),-d*C/R**(d+1))
# A polynomial-moment identity is not a fractional-moment identity.
w=[15,-6,1];t=[S.Integer(1),S.Integer(4),S.Integer(9)]
eq('fixture first moment',sum(a*b for a,b in zip(w,t)),0)
eq('fixture second moment',sum(a*b*b for a,b in zip(w,t)),0)
eq('fixture fractional moment survives',sum(a*b**S.Rational(5,2) for a,b in zip(w,t)),66)
print('mode:', 'MUTATE zero twist' if mutate else 'baseline half twist')
for name,ok in checks:print('PASS' if ok else 'FAIL',name)
print('checks:',sum(ok for _,ok in checks),'/',len(checks))
sys.exit(0 if all(ok for _,ok in checks) else 1)
