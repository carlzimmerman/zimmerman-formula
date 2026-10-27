import os,sys
import sympy as S
mutate=os.environ.get('MUTATE')=='1'
checks=[]
def eq(name,a,b): checks.append((name,S.simplify(a-b)==0))
T=list(map(S.Integer,[1,4,9,16]))
A=S.Matrix([[t**p for t in T] for p in [1,2,S.Rational(5,2)]])
w=A.nullspace()[0]
w=w*S.ilcm(*[x.q for x in w])
# Both signs are allowed; display orientation with positive M0.
if sum(w)<0:w=-w
if mutate:w[3]+=1
M=lambda p:sum(w[i]*T[i]**p for i in range(4))
for p in [1,2,S.Rational(5,2)]:eq('moment '+str(p),M(p),0)
eq('positive orientation M0',M(0),755)
eq('cubic moment',M(3),-14400)
u=S.symbols('u',real=True)
a3=S.integrate((1+u*u)**3,(u,0,1))
eq('angular cubic',a3,S.Rational(96,35))
eq('positive cutoff cubic',-M(3)*a3/64,S.Rational(4320,7))
x=S.symbols('x',positive=True)
eq('strict convexity for Jensen',S.diff(x**S.Rational(3,2),x,2),3/(4*S.sqrt(x)))
# Homogeneous spectator and zero-momentum bosonic Hessian.
f,g,lam,h,chi,m=S.symbols('f g lam h chi m',positive=True)
V=(f+g*chi**2+lam*h**2)**2/2
E=S.expand(V.subs(chi,0))
eq('spectator energy',E,f**2/2+f*lam*h**2+lam**2*h**4/2)
eq('spectator mass squared',S.diff(V,chi,2).subs(chi,0),2*g*(f+lam*h**2))
eq('no cubic',E.coeff(h,3),0)
eq('source current',S.diff(E,h),2*f*lam*h+2*lam**2*h**3)
eq('vacuum scaling',E.subs({h:0,f:2*f}),4*E.subs(h,0))
eq('lambda removal',E.subs(lam,0),f**2/2)
W=f*chi+g*chi**3/3+lam*chi*h**2
eq('fermion zero momentum Hessian',S.diff(W,chi,2).subs(chi,0),0)
Vm=(f+m*chi+lam*h**2)**2/2
eq('massive spectator relaxation',Vm.subs(chi,-(f+lam*h**2)/m),0)
print('mode:', 'MUTATE' if mutate else 'baseline')
print('signed weights:',list(w));print('M0:',M(0),'M3:',M(3))
print('E_spectator:',E)
for name,ok in checks:print('PASS' if ok else 'FAIL',name)
print('checks:',sum(ok for _,ok in checks),'/',len(checks))
sys.exit(0 if all(ok for _,ok in checks) else 1)
