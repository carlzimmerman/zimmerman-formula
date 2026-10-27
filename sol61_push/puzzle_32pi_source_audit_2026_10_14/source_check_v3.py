import json
import numpy as np
from scipy.integrate import solve_bvp

def solve(d,L,tol=1e-7,bc_kind='natural',seed=1.):
    x=np.unique(np.r_[0.,np.geomspace(1e-6,L,850),np.linspace(0,L,4001),d])
    def fun(x,y):
        ratio=np.full_like(x,1/d**3)
        np.divide(1.,x**3,out=ratio,where=x>d)
        return np.array([y[1],x*y[0]*np.abs(y[0])-ratio])
    def bc(a,b):
        end=3*b[0]+L*b[1] if bc_kind=='natural' else L*b[0]-(1/L-1/L**2-.5/L**3)
        return np.array([a[1],end])
    v=seed/(x*x+d*d)
    sol=solve_bvp(fun,bc,x,np.array([v,-2*seed*x/(x*x+d*d)**2]),
                  S=np.array([[0.,0.],[0.,-4.]]),tol=tol,max_nodes=50000)
    assert sol.success,sol.message
    # Differentiate the returned interpolant; do not substitute the ODE for w'.
    test=np.unique(np.r_[np.geomspace(1e-4,L,5000),d])
    vv,ww=sol.sol(test); wp=sol.sol(test,1)[1]
    h=test*vv
    flux=test**4*vv*np.abs(vv)-test**2*(test*wp+4*ww)
    enclosed=np.minimum((test/d)**3,1.)
    fluxerr=float(np.max(np.abs(flux-enclosed)))
    assert fluxerr<2e-6,fluxerr
    assert np.min(h)>0,float(np.min(h))
    assert np.max(np.abs(bc(sol.sol(0),sol.sol(L))))<1e-9
    pts=np.array([5.,10.,20.,30.,40.])
    rr=pts**2*sol.sol(pts)[0]
    graph=np.geomspace(.01,L,300)
    return {'source_radius':d,'outer_radius':L,'tol':tol,'boundary':bc_kind,'seed':seed,
            'nodes':len(sol.x),'max_collocation_residual':float(max(sol.rms_residuals)),
            'max_absolute_flux_error':fluxerr,'origin_slope':float(sol.sol(0)[0]),
            'sample_radii':pts.tolist(),'force_over_leading':rr.tolist(),
            'graph_radius':graph.tolist(),'graph_force_over_leading':(graph**2*sol.sol(graph)[0]).tolist()}

cases=[solve(d,L) for d in [.2,1.,5.] for L in [50.,200.,800.]]
cases += [solve(1.,200.,1e-8),solve(1.,800.,1e-8),
          solve(1.,50.,bc_kind='asymptotic'),solve(1.,200.,bc_kind='asymptotic'),
          solve(1.,200.,seed=.25),solve(1.,200.,seed=4.)]
base=cases[4]; refined=cases[9]
refdiff=max(abs(np.array(base['force_over_leading'])-refined['force_over_leading']))
assert refdiff<2e-6,refdiff
seeddiff=max(max(abs(np.array(base['force_over_leading'])-c['force_over_leading'])) for c in cases[-2:])
assert seeddiff<2e-6,seeddiff
out={'count':len(cases),'refinement_max_absolute_difference':refdiff,
     'initial_guess_max_absolute_difference':seeddiff,'cases':cases,
     'scope':'Finite dimensionless uniform-sphere BVP, prescribed frame; no gravitational or quantum completion'}
print(json.dumps(out,indent=2))
