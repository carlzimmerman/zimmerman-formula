"""Self-consistent leading valley profile aligned with the retained tree pole."""
import os,sys
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import json,time,resource
import mpmath as mp
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/gravity_completion_2026_11_03/protected'))
import solve_protected as p


def main(output):
    started=time.monotonic();mp.mp.dps=110
    p.MU=mp.mpf('2000000');p.M=mp.mpf('2.435e18')/p.MU;p.ALPHA=1/p.M
    pole=mp.sqrt(60/(31*p.E));target=mp.mpf('2.52e-47')/p.MU**4
    def parameters(eps):
        p.EPS=eps;p.NEXP=3-eps;p.WBASE=p.M*p.F/mp.sqrt(eps)
    def prepare(ds,w,ee):
        parameters(ee*mp.mpf('.01'))
        return mp.mpf('.5')+p.EPS/p.BC*ds/2
    def pot(x,ds,w,ee):
        tau=prepare(ds,w,ee)
        return p.data(tau,[mp.sqrt(31)*x,mp.mpf(0),p.Q0],w)['V']+p.cw(x,p.E,p.E,p.G)
    def eq(ds,w,ee):
        dx=mp.diff(lambda x:pot(x,ds,w,ee),pole)
        dt=mp.diff(lambda d:pot(pole,d,w,ee),ds)
        v=pot(pole,ds,w,ee)
        return dx/p.E**2,dt/(p.EPS/p.BC),v-target
    root=mp.findroot(eq,(-mp.mpf('1')/(24*mp.mpf('2.975')),1,mp.mpf('2.49')),tol=mp.mpf('1e-90'),maxsteps=25)
    ds,w,ee=root;tau=prepare(*root)
    def V(x):return pot(x,*root)
    base=V(0)
    # Extra near-pole nodes are necessary because a.1 grid can displace a
    # cubic-spline stationary point by more than the vacuum pole width.
    grid=sorted(set([mp.mpf(j)/10 for j in range(401)]
        +[pole+mp.mpf(j)/10000 for j in range(-120,121)]
        +[pole+mp.mpf(j)/500 for j in range(-150,151)]))
    values=[V(x)-base for x in grid]
    g=np.array([float(x) for x in grid]);vv=np.array([float(x) for x in values])
    # Subtracting absolute values loses precision near the minimum. Export
    # force directly as well, for an independently interpolated
    # local force and potential-offset representation.
    local_grid=[pole+mp.mpf(j)/100000 for j in range(-200,201)]
    vp=V(pole)
    local=[dict(x=float(x),dx=str(x-pole),delta_V_mu4=str(V(x)-vp),force_mu3=str(mp.diff(V,x))) for x in local_grid]
    spl=CubicSpline([q['x'] for q in local],[float(q['force_mu3']) for q in local])
    interpolated=brentq(spl,float(pole)-.001,float(pole)+.001,xtol=1e-13)
    curvature=mp.diff(V,pole,2)
    phase_curvature=-mp.diff(lambda x:p.data(tau,[mp.sqrt(31)*x,0,p.Q0],w)['V'],pole)/pole
    # Modulus curvature is in the dimensionless ds coordinate; its positive
    # sign is the relevant local stability diagnostic in this restricted profile.
    modulus_curvature=mp.diff(lambda d:pot(pole,d,w,ee),ds,2)
    checks=dict(stationarity=max(abs(q) for q in eq(*root))<mp.mpf('1e-78'),
        vacuum_residual=abs(V(pole)/target-1)<mp.mpf('1e-12'),
        epsilon_domain=0<p.EPS<mp.mpf('.1') and p.NEXP>0,
        radial_curvature=curvature>0,phase_curvature=phase_curvature>0,
        modulus_curvature=modulus_curvature>0,
        spline_force_alignment=abs(interpolated-float(pole))<1e-9)
    constants={name:str(getattr(p,name)) for name in ('E','EPS','NEXP','BC','MU','M','ALPHA','F','AA','KK','Q0','Z','R0','WBASE','G')}
    packet=dict(mu_GeV=2000000.,actual_x=str(pole),tau=str(tau),w=str(w),constants=constants,
        root=[str(q) for q in root],net_V_GeV4=str(V(pole)*p.MU**4),
        global_profile=dict(grid=g.tolist(),V0_origin_subtracted_mu4=vv.tolist(),origin_force=float(mp.diff(V,0)),origin_curvature=float(mp.diff(V,0,2)),origin_reference_mu4=str(base)),
        local_profile=dict(reference_x=str(pole),reference_V_origin_subtracted_mu4=str(vp-base),radial_curvature_mu2=str(curvature),third_derivative_mu=str(mp.diff(V,pole,3)),fourth_derivative=str(mp.diff(V,pole,4)),samples=local),
        phase_curvature_mu2=str(phase_curvature),modulus_ds_curvature=str(modulus_curvature))
    result=dict(claim_id='CT09_MATCHED_LEADING_RESONANCE_PROFILE',checks={k:bool(v) for k,v in checks.items()},packet=packet,
        numerical_force_spline_zero=interpolated,force_spline_zero_error=interpolated-float(pole),
        scope='Aligned leading rigid-valley tree-gravity+CW trajectory action. Not the separately exported finite normal/two-loop local packet or a matched quantum resonance mass.',
        runtime_seconds=time.monotonic()-started,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=result['checks'],epsilon=str(p.EPS),runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'])))
    assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
