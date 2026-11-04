"""Protected same-family finite scalar vacuum placed near charged-pair pole."""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import json,math,time,resource
import mpmath as mp
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/gravity_completion_2026_11_03/protected'))
import solve_protected as p
import finite_normal as f
mp.mp.dps=110


def parameters(eps):
    p.EPS=mp.mpf(eps);p.NEXP=3-p.EPS;p.WBASE=p.M*p.F/mp.sqrt(p.EPS)


def solve(target,nodes):
    # Solve epsilon as a sixth physical parameter while fixing the target
    # outer field. The other five equations retain their established scales.
    def unpack(t,ns,qa,ds,w,ee):
        parameters(ee*mp.mpf('1e-4'))
        return f.unpack(t,ns,qa,ds,w)
    def potential(*args):
        tau,z,w=unpack(*args)
        return p.data(tau,z,w)['V']+f.loop(tau,z,w,nodes)
    def eq(*args):
        tau,z,w=unpack(*args)
        d=[mp.diff(lambda q:potential(*(list(args[:i])+[q]+list(args[i+1:]))),args[i]) for i in range(4)]
        # mp.diff temporarily changes the module parameters through potential;
        # restore the current epsilon before evaluating non-derivative terms.
        tau,z,w=unpack(*args)
        xx=(z[0]+mp.sqrt(30)*z[1])/mp.sqrt(31)
        return d[0]/p.E**2,d[1]/mp.mpf('1e-12'),d[2]/(p.Q0**2*mp.mpf('1e-16')),d[3]/(p.EPS/p.BC),potential(*args)-f.DE,xx-target
    guess=(target/(p.R0/mp.sqrt(31)),mp.mpf('-.6'),mp.mpf('2.4'),-1/(24*p.NEXP),1,mp.mpf('3.2'))
    root=mp.findroot(eq,guess,tol=mp.mpf('1e-87'),maxsteps=30)
    tau,z,w=unpack(*root);d=p.data(tau,z,w)
    p.ucw=lambda tau,z,w:f.loop(tau,z,w,nodes)
    mats=p.neutral_matrices(tau,z,w)
    xx=(z[0]+mp.sqrt(30)*z[1])/mp.sqrt(31)
    # Serialize enough precision to reconstruct the cancellation, including
    # every in-memory irrational constant used in this finite action.
    constants={name:str(getattr(p,name)) for name in ('E','EPS','NEXP','BC','MU','M','ALPHA','F','AA','KK','Q0','Z','R0','WBASE','G')}
    normal=dict(tau=str(tau),z=[str(q) for q in z],w=str(w))
    # Leading global action is used for the cosmological trajectory, with
    # normals on the rigid valley; do not extrapolate local two-loop fits.
    aa=p.Q0/mp.sqrt(30)
    def global_v(x):
        zz=[mp.sqrt(31)*x,mp.mpf(0),p.Q0]
        return p.data(tau,zz,w)['V']+p.cw(x,p.E,p.E,p.G)
    base=global_v(0)
    grid=[mp.mpf(j)/10 for j in range(401)]
    values=[global_v(x)-base for x in grid]
    result=dict(nodes=nodes,target_x=str(target),actual_x=str(xx),root=[str(q) for q in root],
                constants=constants,normalized=normal,net_V_GeV4=str(potential(*root)*p.MU**4),
                relative_DE_error=str(abs(potential(*root)/f.DE-1)),
                max_scaled_equation_residual=str(max(abs(q) for q in eq(*root))),
                scalar_masses_GeV=[float(mp.sqrt(q)*p.MU) for q in mats['scalar_masses2']],
                min_metric_eigenvalue=str(min(mats['metric_eigenvalues'])),Y=str(d['Y']),DH=str(d['DH']),
                global_profile=dict(grid=[float(q) for q in grid],V0_origin_subtracted_mu4=[float(q) for q in values],origin_force=float(mp.diff(global_v,0)),origin_curvature=float(mp.diff(global_v,0,2)),origin_reference_mu4=str(base)),
                scope='Finite local scalar stationarity plus tree-pole placement. Global profile omits local finite two-loop extrapolation. No matched resonance mass or SUGRA transverse fermion/current pole.')
    return result


def main(output):
    started=time.monotonic();pole=mp.sqrt(60/(31*p.E))
    # A finite offset resolves the thermally sampled pole without pretending
    # the uncomputed higher-order heavy pole is known to a sub-width precision.
    target=pole-mp.mpf('.001')
    rows=[solve(target,nodes) for nodes in (21,29)]
    checks=dict(stationarity=all(mp.mpf(r['max_scaled_equation_residual'])<mp.mpf('1e-75') for r in rows),
                positive_epsilon=all(0<mp.mpf(r['constants']['EPS'])<mp.mpf('.01') for r in rows),
                positive_scalar_Hessian=all(min(r['scalar_masses_GeV'])>0 for r in rows),
                positive_metric=all(mp.mpf(r['min_metric_eigenvalue'])>0 and mp.mpf(r['Y'])>0 and mp.mpf(r['DH'])>0 for r in rows),
                vacuum_residual=all(mp.mpf(r['relative_DE_error'])<mp.mpf('1e-10') for r in rows),
                target_field=all(abs(mp.mpf(r['actual_x'])-target)<mp.mpf('1e-60') for r in rows),
                finite_table_convergence=abs(mp.mpf(rows[0]['constants']['EPS'])/mp.mpf(rows[1]['constants']['EPS'])-1)<mp.mpf('1e-5'))
    result=dict(claim_id='CT09_PROTECTED_RESONANCE_PLACEMENT',checks={k:bool(v) for k,v in checks.items()},
                rigid_tree_pole_x=str(pole),rows=rows,runtime_seconds=time.monotonic()-started,
                peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=result['checks'],epsilon=rows[-1]['constants']['EPS'],target_x=str(target),runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'])))
    assert all(checks.values()), checks
if __name__=='__main__':main(sys.argv[1])
