import json
import numpy as np
from scipy.integrate import solve_bvp

def solve(d,L,tol=1e-9,bc_kind='natural',seed=1.,origin_factor=1e-4):
    x0=d*origin_factor
    x=np.unique(np.r_[np.geomspace(x0,L,850),np.linspace(x0,L,8001),d])
    x=x[np.r_[True,np.diff(x)>1e-12*(1+np.abs(x[:-1]))]]
    def fun(x,y):
        mass=x**3/(x*x+d*d)**1.5
        return np.array([y[1],(y[0]*np.abs(y[0])-mass)/x+2*y[0]/x**2])
    def bc(a,b):
        end=b[0]+L*b[1] if bc_kind=='natural' else b[0]-(1-1/L-(.5+.75*d*d)/L**2)
        return np.array([a[1]-2*a[0]/x0+x0**3/(5*d**3)-a[0]*abs(a[0])/6-3*x0**5/(14*d**5),end])
    v=seed*x*x/(x*x+d*d)
    sol=solve_bvp(fun,bc,x,np.array([v,2*seed*x*d*d/(x*x+d*d)**2]),
                  tol=tol,bc_tol=1e-12,max_nodes=100000)
    assert sol.success,sol.message
    # Differentiate the returned interpolant; do not substitute the ODE for w'.
    test=np.unique(np.r_[np.geomspace(x0,L,5000),d])
    vv,ww=sol.sol(test); wp=sol.sol(test,1)[1]
    h=vv/test
    flux=vv*np.abs(vv)-test*wp+2*vv/test
    enclosed=test**3/(test*test+d*d)**1.5
    fluxerr=float(np.max(np.abs(flux-enclosed)))
    assert fluxerr<2e-6,(d,L,tol,fluxerr)
    assert np.min(h)>0,float(np.min(h))
    assert np.max(np.abs(bc(sol.sol(x0),sol.sol(L))))<1e-9
    pts=np.array([5.,10.,20.,30.,40.])
    rr=sol.sol(pts)[0]
    graph=np.geomspace(.01,L,300)
    return {'source_radius':d,'outer_radius':L,'tol':tol,'boundary':bc_kind,'seed':seed,
            'origin_radius':x0,'nodes':len(sol.x),'max_collocation_residual':float(max(sol.rms_residuals)),
            'max_absolute_flux_error':fluxerr,'origin_slope':float(sol.sol(x0)[0]/x0**2),
            'sample_radii':pts.tolist(),'force_over_leading':rr.tolist(),
            'graph_radius':graph.tolist(),'graph_force_over_leading':sol.sol(graph)[0].tolist()}

cases=[solve(d,L) for d in [.2,1.,5.] for L in [50.,200.,800.]]
cases += [solve(1.,200.,1e-10),solve(1.,800.,1e-10),
          solve(1.,50.,bc_kind='asymptotic'),solve(1.,200.,bc_kind='asymptotic'),
          solve(1.,200.,seed=.25),solve(1.,200.,seed=4.),solve(.2,200.,origin_factor=1e-5)]
base=cases[4]; refined=cases[9]
refdiff=max(abs(np.array(base['force_over_leading'])-refined['force_over_leading']))
assert refdiff<2e-6,refdiff
seeddiff=max(max(abs(np.array(base['force_over_leading'])-c['force_over_leading'])) for c in cases[13:15])
assert seeddiff<2e-6,seeddiff
out={'origin_cutoff_difference':float(max(abs(np.array(cases[1]['force_over_leading'])-cases[-1]['force_over_leading']))),'count':len(cases),'refinement_max_absolute_difference':refdiff,
     'initial_guess_max_absolute_difference':seeddiff,'cases':cases,
     'scope':'Finite dimensionless Plummer-source BVP, prescribed frame; no gravitational or quantum completion'}
print(json.dumps(out,indent=2))
