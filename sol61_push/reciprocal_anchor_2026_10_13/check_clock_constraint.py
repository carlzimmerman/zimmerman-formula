import json,sys
from pathlib import Path
import sympy as s

checks=[]
def check(name,c,detail):
    checks.append(dict(name=name,passed=bool(c),detail=str(detail)))
    if not c:raise AssertionError(name)
eps=s.symbols('epsilon',real=True)
vx,vy,vz,Px,Py,Pz=s.symbols('vx vy vz Px Py Pz',real=True)
v=s.Matrix([vx,vy,vz]);P=s.Matrix([Px,Py,Pz]);v2=v.dot(v);pv=P.dot(v)
n0=1+eps*eps*v2/2
Pt=eps*pv/n0
B0=n0*P-eps*v*Pt
expanded=B0.applyfunc(lambda x:s.series(x,eps,0,3).removeO())
expected=P+eps*eps*(v2*P/2-v*pv)
check('normal/polarization antisymmetric current expansion',all(s.simplify(x)==0 for x in expanded-expected),expanded)
norm2=s.series(P.dot(P)-Pt*Pt,eps,0,3).removeO()
check('polarization norm clock correction',s.simplify(norm2-P.dot(P)+eps*eps*pv*pv)==0,norm2)
kap=s.symbols('kappa_perp',positive=True)
# On-shell weak acceleration g=kap*P. Rest-mass lapse and potential terms are both retained.
rest=kap*(v2*P.dot(P)/2-pv*pv)
potential=kap*pv*pv/2
clock=s.expand(rest+potential)
check('onshell clock potential transverse to background',s.simplify(clock-kap*(P.dot(P)*v2-pv*pv)/2)==0,clock)

kx,ky,kz=s.symbols('kx ky kz',real=True)
kk=s.Matrix([kx,ky,kz]);k2=kk.dot(kk)
Q=-k2*P+kk*(kk.dot(P))
check('clock spatial current operator transverse',s.expand(Q.dot(kk))==0,Q)
check('clock operator norm',s.simplify(Q.dot(Q)-k2*(k2*P.dot(P)-kk.dot(P)**2))==0,Q.dot(Q))

n,R,h,k,Pperp,Kp,gamma=s.symbols('n R h k Pperp Kp gamma',positive=True)
ed,pd,pi,p,pe,pp=s.symbols('etadot Pdot pi p p_eta p_P',real=True)
w=n*ed-pd
L=(w-k*k*Pperp*pi)**2/(2*R)+h*ed*ed/2+kap*k*k*Pperp*Pperp*pi*pi/2-(Kp+gamma*k*k)*p*p/2
pisol=s.solve(s.diff(L,pi),pi)[0]
Lclock=s.simplify(L.subs(pi,pisol))
expected=w*w/(2*(R+k*k/kap))+h*ed*ed/2-(Kp+gamma*k*k)*p*p/2
check('clock constraint reduction',s.simplify(Lclock-expected)==0,pisol)
esol=s.solve(s.diff(Lclock,ed),ed)[0]
Lred=s.simplify(Lclock.subs(ed,esol))
I=1/(n*n/h+R+k*k/kap)
check('zero conserved reference momentum inertia',s.simplify(Lred-I*pd*pd/2+(Kp+gamma*k*k)*p*p/2)==0,I)
Hess=s.hessian(Lclock,(ed,pd))
check('clock-reduced matter kinetic positive',s.simplify(Hess.det()-h/(R+k*k/kap))==0,Hess)
velocity=s.solve([s.Eq(pe,s.diff(Lclock,ed)),s.Eq(pp,s.diff(Lclock,pd))],(ed,pd),dict=True)[0]
Ham=s.simplify((pe*ed+pp*pd-Lclock).subs(velocity))
positive=(pe+n*pp)**2/(2*h)+(R+k*k/kap)*pp*pp/2+(Kp+gamma*k*k)*p*p/2
check('positive constrained matter Hamiltonian',s.simplify(Ham-positive)==0,positive)
omega2=(Kp+gamma*k*k)/I
check('quartic high wave number frequency',s.limit(omega2/k**4,k,s.oo)==gamma/kap,omega2)
check('stiffness-free comparison speed',s.simplify(s.limit(omega2.subs(gamma,0)/k**2,k,s.oo)-Kp/kap)==0,'gamma0 comparison, not screened theory')
# At Pperp=0 the pi-dependent block vanishes instead of this reduction.
parallel=s.simplify(L.subs(Pperp,0))
check('parallel angle is a different clock block',s.diff(parallel,pi)==0,parallel)

rows=[]
for kval in [s.Rational(1,10),s.Integer(1),s.Integer(10),s.Integer(100)]:
    vals={n:1,R:1,h:1,kap:1,Kp:1,gamma:s.Rational(1,10),k:kval}
    rows.append(dict(k=str(kval),Ieff=str(I.subs(vals)),omega_squared=str(omega2.subs(vals)),omega_squared_over_k_squared=str((omega2/k**2).subs(vals))))
out=dict(checks=checks,clock_solution=str(pisol),reduced_inertia=str(I),reduced_Hamiltonian=str(positive),frequency_squared=str(omega2),controls=rows,scope='Clock-varied but metric-frozen local nonzero-P matter comparison; not a fully reduced Einstein/current/clock system.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
