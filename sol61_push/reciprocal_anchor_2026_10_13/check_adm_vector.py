import json,sys
from pathlib import Path
import sympy as s
checks=[]
def check(name,c,detail):
    checks.append(dict(name=name,passed=bool(c),detail=str(detail)))
    if not c:raise AssertionError(name)
n,R,h,k,P,kap,gamma,M2=s.symbols('n R h k P kappa_perp gamma Mpl2',positive=True)
A=s.symbols('A',positive=True)
u1,u2,d1,d2,N1,N2=s.symbols('u1 u2 d1 d2 N1 N2',real=True)
u=s.Matrix([u1,u2]);d=s.Matrix([d1,d2]);N=s.Matrix([N1,N2])
C=s.Matrix([[n,-k*P],[k*P,n]]);D=R*s.eye(2)-C
Href=h+kap*P*P
cnorm=n*n+k*k*P*P;dnorm=(R-n)**2+k*k*P*P
check('metric current coordinate/normal dictionary',C*(u-N)-d+R*N==C*u-d+D*N,'u=eta_dot+N')
check('shift mixing norm',s.simplify(D.T*D-dnorm*s.eye(2))==s.zeros(2),dnorm)
current=C*u-d+D*N
L=current.dot(current)/(2*R)+Href*u.dot(u)/2+A*N.dot(N)/2
ns=s.solve([s.diff(L,N1),s.diff(L,N2)],(N1,N2),dict=True)[0]
reducedN=s.simplify(L.subs(ns));Reff=R+dnorm/A
expected=(C*u-d).dot(C*u-d)/(2*Reff)+Href*u.dot(u)/2
check('metric shift constraint reduction',s.simplify(reducedN-expected)==0,Reff)
us=s.solve([s.diff(reducedN,u1),s.diff(reducedN,u2)],(u1,u2),dict=True)[0]
red=s.simplify(reducedN.subs(us));I=1/(Reff+cnorm/Href)
check('metric and reference reduced inertia',s.simplify(red-I*d.dot(d)/2)==0,I)
# In spatial vector gauge K_xy=K_yx=-ikN_y/2. ADM M2(KijKij-K^2)/2.
Nprime=s.symbols('Nprime',real=True)
Kij=s.Matrix([[0,-Nprime/2,0],[-Nprime/2,0,0],[0,0,0]])
EH=s.simplify(M2*(sum(x*x for x in Kij)-s.trace(Kij)**2)/2)
check('Einstein vector shift coefficient',s.simplify(EH-M2*Nprime*Nprime/4)==0,EH)
IG=s.simplify(I.subs(A,M2*k*k/2))
omega=(kap+gamma*k*k)/IG
check('metric constraint finite inverse-inertia correction',s.simplify(1/IG-R-cnorm/Href-2*P*P/M2-2*(R-n)**2/(M2*k*k))==0,IG)
check('gravity decoupling restores frozen-metric comparison',s.simplify(s.limit(IG,M2,s.oo)-1/(R+cnorm/Href))==0,'FormalMpl->infinity;sourcegradient retainedlocally')
check('quartic branch survives vector metric constraint',s.simplify(s.limit(omega/k**4,k,s.oo)-gamma*P*P/Href)==0,omega)
rows=[]
for kval in [s.Integer(1),s.Integer(10),s.Integer(100)]:
 vals={n:1,R:1,h:1,P:1,kap:1,gamma:s.Rational(1,10),M2:10,k:kval}
 rows.append(dict(k=str(kval),Ieff=str(IG.subs(vals)),omega_squared=str(omega.subs(vals))))
out=dict(checks=checks,ADM_shift_coefficient=str(EH),reduced_inertia=str(IG),frequency_squared=str(omega),controls=rows,scope='One principal odd sector with ADM shift, reference-rest-frame alternative; scalar/tensor/clock and nonlinear backgroundhealth not certified.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
