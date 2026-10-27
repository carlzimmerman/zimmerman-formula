"""Finite-stock, whole-core Plummer fluid free boundary, G=a0=Mb=1.

python3 THIS_SCRIPT NEW_RUN/results.json
Version4: tighter boundary residual independently of unchanged ODE gates.
Version3: linear hydrostatic seed at H=5, then physical branch continuation.
Original v1/v2 initialization failures preserved; equations and gates unchanged.
u=r*v, m=r^3*v.  -H*Delta_vector(u)+u^2/(1-u)=Q(r)/r^2
on positive-density support; m=S outside; density and pressure vanish at edge.
This changes independent-field vacuum variations to conserved-fluid variations.
"""
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import solve_bvp, quad
from scipy.optimize import brentq

checks=[]


def ck(name,ok,detail=None):
    checks.append(dict(name=name,passed=bool(ok),detail=detail))
    if not ok:
        raise AssertionError((name,detail))


def zero_edge(S,A):
    def f(r):
        Q=r**3/(r*r+A*A)**1.5
        return Q*(r*r-S)-S*S
    lo=math.sqrt(S)*(1+1e-8)
    hi=max(2.,2*lo,A)
    while f(hi)<0:
        hi*=2
    return brentq(f,lo,hi)


def solve(S,A,H,tol=2e-6,n=350,seed=None):
    global last_solution
    E0=zero_edge(S,A)
    E=E0+2*math.sqrt(H)
    x=np.linspace(0,1,n)
    v=S/E**3*(2.5-1.5*x*x)
    z=-3*S/E**3*x

    def fun(xx,yy,p):
        edge=np.exp(p[0]);r=edge*xx
        vv,zz=yy
        return np.vstack((zz,edge*edge/H*(r*vv*vv/(1-r*vv)-1/(r*r+A*A)**1.5)))

    def bc(ya,yb,p):
        edge=np.exp(p[0])
        return np.array([ya[1],yb[0]-S/edge**3,yb[1]+3*S/edge**3])

    # solve_bvp imposes its regular-singular condition z(0)=0 automatically.
    initial=np.vstack((v,z)) if seed is None else seed.sol(x)
    initial_p=[math.log(E)] if seed is None else seed.p
    sol=solve_bvp(fun,bc,x,initial,p=initial_p,S=np.array([[0.,0.],[0.,-4.]]),tol=tol,bc_tol=1e-11,max_nodes=20000)
    ck('free-boundary solver converges',sol.success,dict(S=S,A=A,H=H,status=int(sol.status)))
    E=math.exp(sol.p[0])
    xx=np.linspace(0,1,1601);rr=E*xx
    vv,zz=sol.sol(xx);u=rr*vv
    mass=rr**3*vv
    rho=(3*vv+xx*zz)/(4*math.pi)
    ck('physical nonsaturated branch',np.all((u>=0)&(u<1)),float(max(u)))
    ck('positive occupied density',min(rho[:-1])>0,float(min(rho[:-1])))
    ck('density vanishes at free edge',abs(rho[-1])<1e-8,float(rho[-1]))
    ck('stock fixed',abs(mass[-1]-S)<2e-7*max(1,S),float(mass[-1]-S))
    ck('nonnegative monotone enclosed stock',min(np.diff(mass))>=-1e-9,float(min(np.diff(mass))))
    ck('stiff edge beyond zero-pressure cap',E>E0,dict(edge=E,zero_edge=E0))
    Qe=E**3/(E*E+A*A)**1.5
    exterior_drive=S*S/(E*E-S)-Qe
    ck('exterior chemical inequality at edge',exterior_drive<0,float(exterior_drive))
    # r²*H_force=S²/(r²-S)-Q(r) is strictly decreasing beyond the edge.
    outer=np.geomspace(E,100*E,500)
    force_mass=S*S/(outer*outer-S)-outer**3/(outer*outer+A*A)**1.5
    ck('vacuum KKT sign outside',np.all(force_mass<0) and np.all(np.diff(force_mass)<0))

    # Interior integrated field equation. The unexpanded regular-singular ODE
    # gives (r^4 v')'=r^3/H*(R(rv)-Q/r²).
    def integrand(r):
        if r==0:
            return 0.
        w=float(sol.sol(r/E)[0]);uu=r*w
        return r**3/H*(uu*uu/(1-uu)-r/(r*r+A*A)**1.5)
    integ=quad(integrand,0,E,epsabs=1e-7,epsrel=1e-7,limit=200)[0]
    flux=E**3*float(sol.sol(1)[1])
    ck('integrated radial equation',abs(integ-flux)<3e-5*max(1,abs(flux)),abs(integ-flux))
    # Local e=2pi H rho² reproduces vector-gradient energy globally, including
    # the exterior tail H S²/E³. Independent derivative/quadrature identity.
    def grad_integrand(r):
        w,zx=sol.sol(r/E);ur=w+(r/E)*zx
        return .5*H*(r*r*ur*ur+2*(r*w)**2)
    def pressure_integrand(r):
        w,zx=sol.sol(r/E);density=(3*w+(r/E)*zx)/(4*math.pi)
        return 4*math.pi*r*r*2*math.pi*H*density*density
    eg=quad(grad_integrand,0,E,epsabs=1e-8,epsrel=1e-8,limit=200)[0]+H*S*S/E**3
    ep=quad(pressure_integrand,0,E,epsabs=1e-8,epsrel=1e-8,limit=200)[0]
    ck('global stiffness equals positive pressure energy',abs(eg-ep)<3e-6*max(1,ep),dict(gradient=eg,pressure=ep))
    # No claim of a stable covariant parent. This is the positive radial fluid
    # Hessian at prescribed baryon source; dimensionless inertia is conserved mass.
    last_solution=sol
    return dict(S=S,A=A,H=H,edge=E,zero_stiffness_edge=E0,max_u=float(max(u)),
                central_density=float(rho[0]),edge_density=float(rho[-1]),
                exterior_force_mass_at_edge=float(exterior_drive),
                max_rms_residual=float(max(sol.rms_residuals)),nodes=len(sol.x),
                pressure_gradient_energy_error=abs(eg-ep),
                sample_x=xx[::20].tolist(),sample_mass=mass[::20].tolist(),sample_rho=rho[::20].tolist())



class LinearSeed:
    """Exact R(u)=0 Plummer hydrostatic limit, used only as Newton initial data."""
    def __init__(self,S,A,H):
        def J(r):
            return .5*(r*math.sqrt(r*r+A*A)-A*A*math.asinh(r/A))
        def mass(E):
            return (J(E)-E**3/(3*math.sqrt(E*E+A*A)))/H
        hi=max(1.,A,math.sqrt(6*H*S))
        while mass(hi)<S:hi*=2
        E=brentq(lambda r:mass(r)-S,1e-5*A,hi)
        self.p=np.array([math.log(E)]);self.E=E;self.A=A;self.H=H
    def sol(self,x):
        E,A,H=self.E,self.A,self.H
        r=E*np.asarray(x);q=r/A
        J=.5*(r*np.sqrt(r*r+A*A)-A*A*np.arcsinh(q))
        small=q<1e-3
        J[small]=r[small]**3/(3*A)-r[small]**5/(10*A**3)+3*r[small]**7/(56*A**5)-5*r[small]**9/(144*A**7)
        m=(J-r**3/(3*math.sqrt(E*E+A*A)))/H
        v=np.empty_like(r);z=np.zeros_like(r)
        v[0]=(1/A-1/math.sqrt(E*E+A*A))/(3*H)
        v[1:]=m[1:]/r[1:]**3
        mp=r*r/H*(1/np.sqrt(r*r+A*A)-1/math.sqrt(E*E+A*A))
        z[1:]=E*(mp[1:]/r[1:]**3-3*m[1:]/r[1:]**4)
        return np.vstack((v,z))


rows=[];seeds={};continuation_profiles=[]
for A in [.3,1.,3.]:
    for S in [.1,1.,5.364]:
        continuation=LinearSeed(S,A,5.)
        for H in [5.,2.,1.,.5,.2,.1,.05,.02,.01,.005]:
            row=solve(S,A,H,seed=continuation)
            continuation=last_solution
            seeds[(A,S,H)]=last_solution
            continuation_profiles.append(row)
            if H in [.005,.05,.5]:rows.append(row)
refinements=[]
for A,S,H in [(1.,.1,.005),(1.,1.,.05),(.3,5.364,.5),(3.,1.,.005)]:
    coarse=next(r for r in rows if (r['A'],r['S'],r['H'])==(A,S,H))
    fine=solve(S,A,H,tol=2e-7,n=700,seed=seeds[(A,S,H)])
    err=abs(fine['edge']/coarse['edge']-1)
    ck('edge refinement',err<2e-5,err)
    refinements.append(dict(A=A,S=S,H=H,relative_edge_error=err))
out=dict(claim_id='CE-CONT-FREE-EDGE-2026-10-18-V4',n_checks=len(checks),checks=checks,profiles=rows,continuation_profiles=continuation_profiles,refinements=refinements,
         scope='Fixed external Plummer baryons; Newtonian radial conserved-fluid comparison. Smooth free boundary and finite total cold stock. Local EOS e=P=2pi H rho². No microscopic derivation of full response energy, formation, exchange, metric, empirical fit or cosmology.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(dict(n_checks=len(checks),profiles=[{k:r[k] for k in ['S','A','H','edge','zero_stiffness_edge','max_u','central_density']} for r in rows],refinements=refinements),indent=2))
