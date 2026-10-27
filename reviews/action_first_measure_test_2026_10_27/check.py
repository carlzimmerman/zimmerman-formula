import os,sys
import sympy as S
A,D,delta,X=S.symbols('A D delta X',positive=True)
d=S.symbols('d',positive=True)
mutate=os.environ.get('MUTATE')=='1'
P=X-(A+delta*X)**2/(4*D)
U=-P.subs(X,0);Z=S.diff(P,X).subs(X,0)
B=S.diff(P,X,2)/2
if mutate:B=-B
checks=[]
def eq(name,a,b):checks.append((name,S.simplify(a-b)==0))
eq('general kinetic scale weight',d/2-(d-2)/2-1,0)
eq('general potential scale weight',d/2-d/2,0)
eq('effective decomposition',P,-U+Z*X+B*X**2)
eq('shared constraint identity',4*U*B+(1-Z)**2,0)
eq('canonical invariant',U*B/Z**2,-A**2*delta**2/(4*(2*D-A*delta)**2))
eq('vacuum independent of kinetic deformation',S.diff(U,delta),0)
eq('canonical ratio varies',S.diff(U*B/Z**2,delta),-A**2*D*delta/(2*D-A*delta)**3)
r=S.symbols('r',positive=True)
eq('field normalization invariant',U*(B/r**4)/(Z/r**2)**2,U*B/Z**2)
h=S.symbols('h',nonnegative=True)
E=-P.subs(X,-h*h/2)
eq('static energy',E,U+Z*h*h/2-B*h**4/4)
eq('no static cubic',S.expand(E).coeff(h,3),0)
print('mode:', 'MUTATE sign reversal' if mutate else 'baseline')
print('U=',U,'Z=',Z,'B=',B)
print('d(U B/Z^2)/dDelta=',S.factor(S.diff(U*B/Z**2,delta)))
for name,ok in checks:print('PASS' if ok else 'FAIL',name)
print('checks:',sum(ok for _,ok in checks),'/',len(checks))
sys.exit(0 if all(ok for _,ok in checks) else 1)
