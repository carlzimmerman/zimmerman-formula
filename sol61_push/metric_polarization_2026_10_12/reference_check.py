"""Bounded reference-field probe; all outputs are conditional model predictions."""
import json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.integrate import solve_bvp, simpson

checks=[]
def ck(name,p,value=None): checks.append(dict(name=name,passed=bool(p),value=value))
x,A,C,D,eps,K=s.symbols('x A C D eps K',positive=True)
L=lambda z:s.diff(z,x,2)+2*s.diff(z,x)/x-2*z/x**2
w=A/2+C/x**2+D*x
ck('exact exterior sum mode',s.simplify(-L(w)-A/x**2)==0)
u,v,d,ww,f=s.symbols('u v d ww f',real=True)
uu=(ww+K*d)/(K+eps); vv=(ww-eps*d)/(K+eps)
ck('difference reconstruction',s.simplify(uu-vv-d)==0)
ck('sum reconstruction',s.simplify(eps*uu+K*vv-ww)==0)
Ad,k,mu=s.symbols('Ad k mu',positive=True)
Schur=Ad+eps*k*k-Ad**2/(Ad+K*k*k)
ck('effective stiffness',s.simplify(Schur-(eps*k*k+Ad*K*k*k/(Ad+K*k*k)))==0)
ck('pinning restores zero wave stiffness',s.simplify((Ad-Ad**2/(Ad+mu**2))-Ad*mu**2/(Ad+mu**2))==0)
# Background subtraction in the full polarization equation, for any vector component.
q0,q,rr,gn,G4=s.symbols('q0 q rr gn G4')
ck('uniform background drops from linear force',s.expand(G4*q0+gn+G4*q-G4*(q0+q)-gn)==0)

def force(z): return z/(1+z*z)**1.5
def boundary(ya,yb,lo): return np.array([ya[1]-ya[0]/lo,yb[0]])
rows=[]
for lo,hi in [(1e-4,300.),(5e-5,600.)]:
    mesh=np.geomspace(lo,hi,1600)
    guess=.5*mesh/(1+mesh)*(1-mesh/hi)
    ws=solve_bvp(lambda z,y:np.array([y[1],-2*y[1]/z+2*y[0]/z**2-force(z)]),
        lambda a,b:boundary(a,b,lo),mesh,np.array([guess,np.gradient(guess,mesh)]),tol=1e-7,max_nodes=30000)
    ck('linear sum convergence '+str(hi),ws.success,ws.message)
    base_guess=np.sqrt(force(mesh))*(1-mesh/hi)
    for kap in [1.,10.,100.,1000.]:
        ep=.01
        eff=ep*kap/(ep+kap)
        ff=kap/(ep+kap)
        ds=solve_bvp(lambda z,y:np.array([y[1],-2*y[1]/z+2*y[0]/z**2+(y[0]*abs(y[0])-ff*force(z))/eff]),
            lambda a,b:boundary(a,b,lo),mesh,np.array([base_guess,np.gradient(base_guess,mesh)]),tol=1e-7,max_nodes=30000)
        ck('difference convergence '+str((hi,kap)),ds.success,ds.message)
        z=np.geomspace(lo,hi,40001)
        dv,dp=ds.sol(z); wv,wp=ws.sol(z)
        uv=(wv+kap*dv)/(ep+kap); rv=(wv-ep*dv)/(ep+kap)
        # Integral identity for the nonlinear difference BVP; boundary terms retained.
        lhs=simpson(eff*(z*z*dp*dp+2*dv*dv)+z*z*abs(dv)**3,x=z)
        rhs=simpson(z*z*ff*force(z)*dv,x=z)+eff*((z*z*dv*dp)[-1]-(z*z*dv*dp)[0])
        err=abs(lhs-rhs)/max(abs(lhs),abs(rhs),1e-30)
        ck('integrated difference equation '+str((hi,kap)),err<1e-5,float(err))
        rec=float(max(np.max(abs(uv-rv-dv)),np.max(abs(ep*uv+kap*rv-wv))))
        ck('full profile reconstruction '+str((hi,kap)),rec<1e-11,rec)
        at=np.array([3.,10.,30.,100.]); dd=ds.sol(at)[0]; wd=ws.sol(at)[0]
        up=(wd+kap*dd)/(ep+kap); rp=(wd-ep*dd)/(ep+kap)
        rows.append(dict(inner=lo,outer=hi,K=kap,radii=at.tolist(),polarization_over_zero_stiffness=(up/np.sqrt(force(at))).tolist(),reference_over_polarization=(rp/up).tolist(),sum_at_radii=wd.tolist(),integrated_residual=err,max_bvp_residual=float(max(ds.rms_residuals)),nodes=len(ds.x)))

# Local 6x6 Hessian, includes both transverse sectors and relative cubic curvature.
minimum=float('inf'); cases=0
for mag in [0.,.01,1.,100.]:
    for wave in [.001,.1,1.,100.]:
        for theta in [0.,np.pi/4,np.pi/2]:
            nv=np.array([np.sin(theta),0.,np.cos(theta)])
            B=mag*(np.eye(3)+np.outer(nv,nv))
            H=np.block([[np.diag([1.,1.,0.])+.01*wave**2*np.eye(3)+B,-B],[-B,10*wave**2*np.eye(3)+B]])
            minimum=min(minimum,float(np.linalg.eigvalsh(H)[0]));cases+=1
ck('two-field Hessian sample',minimum>0,dict(cases=cases,minimum=minimum))
# Wrong reference sign destroys convexity: this is not a friction-only repair.
B=np.eye(3)
bad=np.block([[np.diag([1.,1.,0.])+B,-B],[-B,-10*np.eye(3)+B]])
ck('wrong reference gradient sign detected',np.linalg.eigvalsh(bad)[0]<0,float(np.linalg.eigvalsh(bad)[0]))
result=dict(all_pass=all(c['passed'] for c in checks),checks=checks,profiles=rows,
 scope='Fixed-source reduced Newtonian model. Co-shifted static uniform backgrounds only. No covariant, formation, or data claim.')
out=Path(__file__).parent/'reference_run';out.mkdir(exist_ok=True)
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['all_pass'] else 1)
