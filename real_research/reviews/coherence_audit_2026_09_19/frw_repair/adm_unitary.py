"""Independent ADM derivation of the repaired action, unitary-clock gauge.

The action is the outside-kernel variant, c13=0, one physical metric.
No radiation or baryonic sector is imported into this bounded calculation.
The expanding background is supported by the scalar well and Lambda alone.
"""
from pathlib import Path
import json,time
import sympy as s

start=time.time()
out=Path(__file__).resolve().parent/'run_adm'
t,x=s.symbols('t x',real=True)
e=s.symbols('perturbation',real=True)
a=s.Function('a')(t)
Q,F0,F1,F2=[s.Function(n)(t) for n in ('Q','F0','F1','F2')]
c2,c14,KB,beta,xi,Lam=s.symbols('c2 c14 KB beta xi Lambda',real=True)
psi,B,phi,P=[s.Function(n)(t,x) for n in ('psi','B','phi','P')]
N=1+e*psi
A=a*s.exp(-e*phi)
H=s.diff(a,t)/a
localH=H-e*s.diff(phi,t)
shiftD=e*a*s.diff(B,x,2)+e**2*a*s.diff(phi,x)*s.diff(B,x)
shiftY=e**2*a*s.diff(phi,x)*s.diff(B,x)
Kx=localH/N-shiftD/(N*A**2)
Ky=localH/N+shiftY/(N*A**2)
theta=Kx+2*Ky
R3=s.exp(2*e*phi)/a**2*(4*e*s.diff(phi,x,2)-2*e**2*s.diff(phi,x)**2)
Qfield=(Q+e*s.diff(P,t)-e**2*a*s.diff(B,x)*s.diff(P,x)/A**2)/N
dQ=Qfield-Q
F=F0+F1*dQ+F2*dQ**2/2
Y=e**2*s.diff(P,x)**2/A**2
acc2=e**2*s.diff(psi,x)**2/(N**2*A**2)
accGrad=e**2*s.diff(psi,x)*s.diff(P,x)/(N*A**2)
L=N*A**3*(R3+Kx**2+2*Ky**2-(1+c2)*theta**2-2*Lam+
           c14*acc2+2*(2-KB)*accGrad-(2-KB)*beta*Y-F)
L2=s.expand(s.diff(L,e,2).subs(e,0)/2)-(2-KB)*xi**2/a*s.diff(P,x,2)**2
fields=[psi,B,phi,P]
def EL(f):
    eq=s.diff(L2,f)
    for d in L2.atoms(s.Derivative):
        if d.expr==f:
            vs=[v for v,n in d.variable_count for _ in range(n)]
            eq+=(-1)**len(vs)*s.diff(s.diff(L2,d),*vs)
    return s.expand(eq)
k=s.symbols('k',positive=True)
amps=[s.Function(n)(t) for n in ('p0','b0','f0','u0')]
wave=s.exp(s.I*k*x)
sub=dict(zip(fields,[f*wave for f in amps]))
eqs=[s.expand(EL(f).subs(sub).doit()/wave) for f in fields]
print('Independent ADM action and equations built',round(time.time()-start,3),'s',flush=True)
data={'ODE':[s.srepr(z) for z in eqs],
      'S':{str(n):s.srepr(v) for n,v in dict(t=t,k=k,a=a,Q=Q,F0=F0,F1=F1,F2=F2,c2=c2,c14=c14,KB=KB,beta=beta,xi=xi,Lam=Lam).items()},
      'amps':[s.srepr(f) for f in amps], 'L2':s.srepr(L2)}
(out/'equations.json').write_text(json.dumps(data,indent=1))
for i,eq in enumerate(eqs):
    print('row',i,'ops',s.count_ops(eq),flush=True)
    if i<2:
        assert not any(d.expr in amps[:2] for d in eq.atoms(s.Derivative))
        assert not any(sum(n for _,n in d.variable_count)>1 for d in eq.atoms(s.Derivative) if d.expr in amps)
print('Lapse and shift equations are constraints.',flush=True)
