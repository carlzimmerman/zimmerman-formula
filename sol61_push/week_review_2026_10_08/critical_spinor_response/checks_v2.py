"""Analytic critical spinor source mechanism, with scoped spatial tests."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_bvp, simpson
from scipy.linalg import eigh_tridiagonal

ap=argparse.ArgumentParser()
ap.add_argument('--output',required=True)
ap.add_argument('--mutate',choices=['geometry','kinetic'])
args=ap.parse_args()
checks=[]
def check(name,ok,detail=''):
    checks.append(dict(name=name,passed=bool(ok),detail=str(detail)))
    print(('PASS ' if ok else 'FAIL ')+name+': '+str(detail),flush=True)

a,b,c,d=s.symbols('a b c d',real=True)
q=a*a+b*b+c*c+d*d
p=s.Matrix([2*(a*c+b*d),2*(a*d-b*c),a*a+b*b-c*c-d*d])
check('Pauli density identity p squared equals q squared',s.expand(p.dot(p)-q*q)==0)
h,lam,D,Q,A=s.symbols('h lambda6 D Q A',positive=True)
qstar=s.sqrt(h*D/lam)
potential=lam*Q**3/3-h*D*Q
check('Sextic minimum',s.simplify(s.diff(potential,Q).subs(Q,qstar))==0)
check('Sextic minimum radial curvature',s.diff(potential,Q,2).subs(Q,qstar)>0)
H=s.simplify(-potential.subs(Q,qstar))
a0=h**3/lam
g=s.diff(H,D)
check('Dual positive flux energy',s.simplify(H-2*s.sqrt(a0)*D**s.Rational(3,2)/3)==0)
check('Deep MOND from varied flux',s.simplify(g*g-a0*D)==0)
check('Convex radial flux energy',s.diff(H,D,2)>0)
check('Convex transverse flux energy',s.diff(H,D)/D>0)
x,y,z,w=s.symbols('x y z w',real=True)
qq=(A+x)**2+y*y+z*z+w*w
ppz=(A+x)**2+y*y-z*z-w*w
V=lam*qq**3/3-h*D*ppz
hessian=s.hessian(V,(x,y,z,w)).subs({x:0,y:0,z:0,w:0}).subs(D,lam*A**4/h)
check('Auxiliary potential Hessian physical signs',hessian==s.diag(8*lam*A**4,0,4*lam*A**4,4*lam*A**4),hessian)

# Explicit local sections and their induced connection; theta in (0,pi).
theta,phi=s.symbols('theta phi',real=True)
zn=s.Matrix([s.cos(theta/2),s.exp(s.I*phi)*s.sin(theta/2)])
zs=s.exp(-s.I*phi)*zn
an=s.simplify(-s.I*(zn.conjugate().T*s.diff(zn,phi))[0])
asouth=s.simplify(-s.I*(zs.conjugate().T*s.diff(zs,phi))[0])
check('North section normalized',s.trigsimp((zn.conjugate().T*zn)[0]-1)==0)
check('North Berry connection',s.trigsimp(an-(1-s.cos(theta))/2)==0)
check('Patch connection transition',s.simplify(asouth-an+1)==0)
curvature=s.diff(an,theta)
check('Unit Chern flux',s.integrate(curvature,(theta,0,s.pi))*2*s.pi==2*s.pi)
dtheta=s.diff(zn,theta)
dphi=s.diff(zn,phi)-s.I*an*zn
angular=s.trigsimp((dtheta.conjugate().T*dtheta)[0]+(dphi.conjugate().T*dphi)[0]/s.sin(theta)**2)
check('Covariant angular gradient',s.trigsimp(angular-s.Rational(1,2))==0,angular)
lapang=s.diff(s.sin(theta)*dtheta,theta)/s.sin(theta)+(s.diff(dphi,phi)-s.I*an*dphi)/s.sin(theta)**2
check('Covariant angular eigenvalue',all(s.simplify(s.expand_trig(v.subs(theta,2*theta)))==0 for v in lapang+zn/2))

r,eps,B,Z=s.symbols('r epsilon B Z',positive=True)
f=A/s.sqrt(r)
ang=0 if args.mutate=='geometry' else s.Rational(1,2)
laprad=s.diff(f,r,2)+2*s.diff(f,r)/r-ang*f/r**2
check('Full radial and angular factor three quarters',s.simplify(laprad/f+3/(4*r*r))==0,s.simplify(laprad/f))
amplitude4=(h*B-s.Rational(3,4)*eps)/lam
eom=s.simplify((eps*laprad+(h*B/r**2-lam*f**4)*f)/f*r*r)
check('Spherical branch Euler equation',s.simplify(eom.subs(A**4,amplitude4))==0,eom)
check('Source mass subtraction',s.simplify(h*h*amplitude4-a0*(B-3*eps/(4*h)))==0)

# Exact logarithmic radial reduction, including its boundary derivative.
t=s.symbols('t',real=True)
yy=s.Function('Y')(t)
kinetic=(s.diff(yy,t)-yy/2)**2+yy**2/2
reduced=s.diff(yy,t)**2+3*yy**2/4
check('Log radius action boundary identity',s.expand(kinetic-reduced+s.diff(yy**2,t)/2)==0)
fvariation=eps*s.diff(yy,t)**2+(3*eps/4-h*B)*yy**2+lam*yy**6/3
EL=s.diff(s.diff(fvariation,s.diff(yy,t)),t)-s.diff(fvariation,yy)
check('Log radius exact ODE',s.simplify(EL/2-(eps*s.diff(yy,t,2)+(h*B-3*eps/4)*yy-lam*yy**5))==0)
L=s.symbols('L',positive=True)
critical=eps/h*(s.Rational(3,4)+s.pi**2/L**2)
check('Dirichlet threshold',s.simplify((h*B-3*eps/4-eps*s.pi**2/L**2).subs(B,critical))==0)

# Local constrained time-dependent perturbations, after U(1) elimination.
g0,k2,kparallel2=s.symbols('g0 k2 kparallel2',positive=True)
Zeff=-Z if args.mutate=='kinetic' else Z
T=Zeff*k2/(4*h*g0)
Slocal=g0/(2*a0)*(k2+kparallel2)
Sgrad=eps*k2**2/(4*h*g0)
omega=s.simplify((Slocal+Sgrad)/T)
expected=eps/Z*k2+2*h*g0*g0/(Z*a0)*(1+kparallel2/k2)
check('Nonzero field scalar kinetic positive',T>0,T)
check('Constrained scalar dispersion',s.simplify(omega-expected)==0,omega)

# Relevant operators spoil the exact critical response.
m2,u,gg=s.symbols('m2 u g',positive=True)
constitutive=(lam*(gg/h)**2+u*(gg/h)+m2)/h
check('Relevant quadratic spinor term creates source threshold',s.simplify(constitutive.subs(gg,0)-m2/h)==0)
check('Relevant quartic spinor term restores linear flux',s.simplify(s.diff(constitutive,gg).subs(gg,0)-u/h**2)==0)
check('Simple Newtonian addition is not P2',s.simplify((D+s.sqrt(a0*D))**2-(D*D+a0*D))==2*D*s.sqrt(a0*D))

# Independently solve zero-boundary shell problem with two initial meshes.
length=math.log(30.)
numeric=[]
for BB in [1.,2.,4.,10.]:
    delta=BB-.75
    solutions=[]
    for nodes in [150,300]:
        xx=np.linspace(0,length,nodes)
        scale=max(delta,0.)**.25
        init=np.vstack([scale*np.sin(np.pi*xx/length),scale*np.pi/length*np.cos(np.pi*xx/length)])
        sol=solve_bvp(lambda tt,v:np.vstack([v[1],-delta*v[0]+v[0]**5]),
                      lambda left,right:np.array([left[0],right[0]]),
                      xx,init,tol=1e-8,max_nodes=10000)
        check('BVP converged B='+str(BB)+' nodes='+str(nodes),sol.success,sol.message)
        solutions.append(sol)
    mesh=np.linspace(0,length,2001)
    vals=solutions[-1].sol(mesh)
    disagreement=np.max(np.abs(solutions[0].sol(mesh)[0]-vals[0]))
    check('BVP mesh comparison B='+str(BB),disagreement<2e-7,disagreement)
    energy=simpson(vals[1]**2-delta*vals[0]**2+vals[0]**6/3,x=mesh)
    integral=vals[1]**2+delta*vals[0]**2-vals[0]**6/3
    drift=float(np.ptp(integral))
    check('ODE first integral B='+str(BB),drift<2e-6,drift)
    peak=float(solutions[-1].sol(length/2)[0])
    threshold=.75+math.pi**2/length**2
    if BB<threshold:
        check('Below threshold gives zero state',abs(peak)<1e-7,peak)
    else:
        check('Above threshold positive lower energy B='+str(BB),peak>0 and energy<0,(peak,energy))
    n=799; dx=length/(n+1)
    eigx=np.linspace(dx,length-dx,n)
    field=solutions[-1].sol(eigx)[0]
    diag=2/dx**2+5*field**4-delta
    off=np.full(n-1,-1/dx**2)
    eig=float(eigh_tridiagonal(diag,off,select='i',select_range=(0,0))[0][0])
    check('Bounded radial Hessian positive B='+str(BB),eig>0,eig)
    numeric.append(dict(B=BB,threshold=threshold,peak=peak,bulk=max(delta,0)**.25,energy=float(energy),
                        first_integral_drift=drift,mesh_disagreement=float(disagreement),radial_eigenvalue=eig,
                        log_r=mesh[::10].tolist(),amplitude=vals[0,::10].tolist()))

result=dict(checks=checks,numeric=numeric,mutation=args.mutate,
            formulas=dict(a0='h^3/lambda6',Bcritical='epsilon/h*(3/4+pi^2/L^2)',mass_shift='3 epsilon/(4 h G)'),
            non_claims=['Not full P2','Not covariant gravity','No vacuum coefficient selected','No all-background stability'])
Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
passed=sum(v['passed'] for v in checks)
print(str(passed)+'/'+str(len(checks))+' checks passed',flush=True)
raise SystemExit(0 if passed==len(checks) else 1)
