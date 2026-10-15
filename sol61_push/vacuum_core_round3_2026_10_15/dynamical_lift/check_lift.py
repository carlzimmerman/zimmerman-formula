#!/usr/bin/env python3
"""Exact algebra and bounded quadratures for the counted NR S2 lift."""
import json
from pathlib import Path
import sys
import sympy as sp
import mpmath as mp

checks=[]
def exact(name,expr):
    residual=sp.simplify(expr)
    if isinstance(residual,sp.MatrixBase):
        ok=all(v==0 for v in residual)
    else:
        ok=residual==0
    assert ok,(name,residual)
    checks.append(name)
def yes(name,condition):
    assert bool(condition),name
    checks.append(name)
G,a,r,s,k,u,gamma=sp.symbols('G a r s k u gamma',positive=True)
W=(-a*a*sp.log(1-u/a)-a*u-u*u/2)/k
exact('frozen W derivative',k*sp.diff(W,u)-u*u/(a-u))
exact('positive radial W curvature formula',k*sp.diff(W,u,2)-u*(2*a-u)/(a-u)**2)
exact('tangential vector Hessian coefficient',k*k*sp.diff(W,u)/u-k*u/(a-u))
exact('radial vector Hessian coefficient',k*k*sp.diff(W,u,2)-k*u*(2*a-u)/(a-u)**2)
# Electric/longitudinal gravity cancellation in a Fourier basis with wavevector along z.
px,py,pz=sp.symbols('px py pz',real=True)
exact('H minus gravitational self-energy leaves transverse Maxwell energy',k*(px*px+py*py+pz*pz)/2-k*pz*pz/2-k*(px*px+py*py)/2)
# Full current, not an identification of current with a displacement time derivative.
rho=sp.symbols('rho',positive=True)
drho=sp.symbols('drho',real=True)
j=sp.Matrix(sp.symbols('jx jy jz',real=True)); dj=sp.Matrix(sp.symbols('djx djy djz',real=True))
T=j.dot(j)/(2*rho)
var=sp.Matrix([drho]+list(dj)); hess=sp.hessian(T,[rho]+list(j))
exact('joint rho-current kinetic convexity', (var.T*hess*var)[0]-(dj-j*drho/rho).dot(dj-j*drho/rho)/rho)
alpha=sp.symbols('alpha',real=True)
gth=sp.Matrix(sp.symbols('tx ty tz',real=True)); gbeta=sp.Matrix(sp.symbols('bx by bz',real=True))
v=gth-alpha*gbeta
first=T-j.dot(gth)+alpha*j.dot(gbeta)
exact('Clebsch current equation',sp.Matrix([sp.diff(first,q) for q in j]).subs(dict(zip(j,rho*v))))
exact('eliminated positive canonical kinetic Hamiltonian',first.subs(dict(zip(j,rho*v)))+rho*v.dot(v)/2)
# Exact radial Hodge boundary term and effective EOS.
q=sp.Function('q')(r); density=sp.diff(q,r)+2*q/r
exact('radial Hodge divergence identity',r*r*(sp.diff(q,r)**2+2*q*q/r**2-density**2)+2*sp.diff(r*q*q,r))
U=gamma*rho*rho/2
exact('existing stiffness pressure',rho*sp.diff(U,rho)-U-gamma*rho*rho/2)
exact('existing stiffness enthalpy',sp.diff(U,rho)-gamma*rho)
exact('effective sound speed',sp.diff(rho*sp.diff(U,rho)-U,rho)-gamma*rho)
# Canonical mass and exact finite-stock edge.
Mb=sp.symbols('Mb',positive=True); rM=sp.sqrt(G*Mb/a)
mc=Mb*(sp.sqrt(1+4*(r/rM)**2)-1)/2
uc=G*mc/r**2
exact('canonical rest polynomial',uc*uc+(G*Mb/r**2)*uc-a*(G*Mb/r**2))
rhoc=Mb/(2*sp.pi*rM*rM*r*sp.sqrt(1+4*(r/rM)**2))
exact('actual positive counted canonical density',sp.diff(mc,r)/(4*sp.pi*r*r)-rhoc)
R=rM*sp.sqrt(s*(s+1)); M=s*Mb
exact('finite edge mass equals inventory',mc.subs(r,R)-M)
exact('edge displacement continuous',G*M/R**2-a/(s+1))
t=sp.symbols('t',positive=True)
F=(G*M/r**2)**2/(a-G*M/r**2)-G*Mb/r**2
exact('outside force sign factor',F.subs(r,R*t)/a-(1-t*t)/(s*t*t*((s+1)*t*t-1)))
exact('zero force at edge',F.subs(r,R))
A,B=sp.symbols('A B',positive=True); ell=sp.sqrt(A/a)
lam=A/ell*sp.atanh(ell/r)-(A+B)/r
F_ab=A*A/(r*r*(a*r*r-A))-B/r**2
exact('exterior chemical potential derivative',sp.diff(lam,r)+F_ab)
exact('chemical potential at infinity',sp.limit(lam,r,sp.oo))
# Extended baryons: differentiate the exact rest polynomial, not a point-mass shortcut.
b=sp.Function('b')(r); m=sp.Function('m')(r)
relation=m*m+b*m-(a/G)*r*r*b
lhs=sp.diff(relation,r)
expected=(2*m+b)*sp.diff(m,r)-2*(a/G)*r*b-m*m*sp.diff(b,r)/b
exact('extended baryon monotonicity reduction',(lhs-expected).subs(a/G,(m*m+b*m)/(r*r*b)))
M0=sp.symbols('M0',positive=True)
ratio=G*M0*M0/(b*(a*r*r-G*M0))
exact('outside tether-to-baryon ratio logarithmic slope',sp.diff(ratio,r)/ratio+sp.diff(b,r)/b+2*a*r/(a*r*r-G*M0))
# Conservative bound for a divergence-free off-shell angular field variation.
x,y,z=sp.symbols('X Y Z',real=True); radial=sp.sqrt(x*x+y*y+z*z)
shape=sp.Function('shape')(radial)/radial
swirl=sp.Matrix([-y*shape,x*shape,0])
exact('nonradial transverse-current/field witness divergence',sp.diff(swirl[0],x)+sp.diff(swirl[1],y)+sp.diff(swirl[2],z))
# Bounded numerical consistency checks of the exact KKT relative-energy decomposition.
# G=a=Mb=1, prescribed point source; the comparison profile is a positive Plummer stock.
mp.mp.dps=55
quad_rows=[]
for stock_text in ['1','5.364']:
    stock=mp.mpf(stock_text); edge=mp.sqrt(stock*(stock+1)); width=edge
    eps=mp.mpf('0.05')
    def fields(rad):
        if rad<edge:
            root=mp.sqrt(1+4*rad*rad)
            u0=2/(1+root); gap0=4*rad*rad/(1+root)**2
            mass0=rad*rad*u0
        else:
            mass0=stock; u0=stock/(rad*rad); gap0=1-u0
        m1=stock*rad**3/(rad*rad+width*width)**mp.mpf('1.5')
        u1=m1/(rad*rad)
        ue=(1-eps)*u0+eps*u1
        gape=(1-eps)*gap0+eps*(1-u1)
        w0=-mp.log(gap0)-u0-u0*u0/2
        we=-mp.log(gape)-ue-ue*ue/2
        return u0,gap0,ue,gape,w0,we
    def energy(rad):
        u0,gap0,ue,gape,w0,we=fields(rad)
        return rad*rad*(we-w0)-(ue-u0)
    def bregman(rad):
        u0,gap0,ue,gape,w0,we=fields(rad)
        return rad*rad*(we-w0-u0*u0/gap0*(ue-u0))
    def exterior_term(rad):
        l=mp.sqrt(stock)
        lam0=stock/l*mp.atanh(l/rad)-(stock+1)/rad
        mu=stock/l*mp.atanh(l/edge)-(stock+1)/edge
        rho1_4pi=3*stock*width*width/(rad*rad+width*width)**mp.mpf('2.5')
        return (lam0-mu)*eps*rho1_4pi*rad*rad
    # Inverse radius on the tail avoids silently imposing a finite outer cutoff.
    def integral_full(fun):
        return mp.quad(fun,[mp.mpf('0'),edge])+mp.quad(lambda inv:fun(1/inv)/(inv*inv),[mp.mpf('0'),1/edge])
    delta=integral_full(energy); breg=integral_full(bregman)
    obstacle=mp.quad(lambda inv:exterior_term(1/inv)/(inv*inv),[mp.mpf('0'),1/edge])
    residual=abs(delta-breg-obstacle)
    assert delta>0 and breg>0 and obstacle>0,(stock_text,delta,breg,obstacle)
    assert residual<mp.mpf('1e-40'),(stock_text,residual)
    quad_rows.append({'M_over_Mb':stock_text,'comparison':'5 percent convex mixture with same-inventory Plummer density of scale R','delta_V':str(delta),'Bregman':str(breg),'outside_obstacle':str(obstacle),'identity_absolute_residual':str(residual)})
result={'claim_id':'VC3-DL-001','exact_check_count':len(checks),'exact_checks':checks,'quadrature_cases':quad_rows,'precision_decimal_digits':mp.mp.dps,'non_claims':['No physical nonzero-gamma equilibrium inferred from the gamma-zero profile','No relativistic cone, smooth global flow or microscopic substance certified','No universal proof by quadrature; the KKT proof supplies quantifiers']}
Path(sys.argv[1]).write_text(json.dumps(result,indent=2)+'\n')
print(str(len(checks))+' exact checks and '+str(len(quad_rows))+' bounded positive-density KKT energy-decomposition quadratures passed.')
