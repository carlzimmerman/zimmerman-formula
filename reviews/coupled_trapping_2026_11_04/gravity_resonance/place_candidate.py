"""Apply the finite placement solver to the lighter same-family candidate."""
import sys,os
sys.dont_write_bytecode=True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):
    os.environ[key]='1'
from pathlib import Path
import json,time,resource
import mpmath as mp
import place as placement


def main(output):
    start=time.monotonic();p=placement.p;f=placement.f
    old_mu=p.MU
    p.MU=mp.mpf('2000000');p.M=mp.mpf('2.435e18')/p.MU;p.ALPHA=1/p.M
    f.DE=mp.mpf('2.52e-47')/p.MU**4
    scale=(old_mu/p.MU)**2
    original=placement.parameters
    # The sixth solver coordinate is rescaled for conditioning only. The
    # recorded constants include the actual epsilon used by the action.
    placement.parameters=lambda epsilon:original(epsilon*scale)
    original(mp.mpf('.0003')*scale)
    pole=mp.sqrt(60/(31*p.E));target=pole-mp.mpf('.001')
    rows=[placement.solve(target,nodes) for nodes in (21,29)]
    checks=dict(stationarity=all(mp.mpf(r['max_scaled_equation_residual'])<mp.mpf('1e-75') for r in rows),
        positive_extended_epsilon=all(0<mp.mpf(r['constants']['EPS'])<mp.mpf('.1') for r in rows),
        exact_positive_n=all(mp.mpf(r['constants']['NEXP'])>0 for r in rows),
        neutral_scalar_Hessian=all(min(r['scalar_masses_GeV'])>0 for r in rows),
        positive_metric=all(mp.mpf(r['min_metric_eigenvalue'])>0 and mp.mpf(r['Y'])>0 and mp.mpf(r['DH'])>0 for r in rows),
        vacuum_normalization=all(mp.mpf(r['relative_DE_error'])<mp.mpf('1e-10') for r in rows),
        placement=all(abs(mp.mpf(r['actual_x'])-target)<mp.mpf('1e-60') for r in rows),
        finite_table_convergence=abs(mp.mpf(rows[0]['constants']['EPS'])/mp.mpf(rows[1]['constants']['EPS'])-1)<mp.mpf('1e-5'))
    result=dict(claim_id='CT09_LIGHT_PROTECTED_RESONANCE_CANDIDATE',checks={k:bool(v) for k,v in checks.items()},
        prior_mu_GeV=str(old_mu),new_mu_GeV=str(p.MU),epsilon_solver_coordinate_scale=str(scale),
        rigid_tree_pole_x=str(pole),rows=rows,runtime_seconds=time.monotonic()-start,
        peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        scope='Same exact Kahler family with changed mu and epsilon, finite local scalar action; no physical threshold/current/kinetic success from placement alone.')
    Path(output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(checks=result['checks'],epsilon=rows[-1]['constants']['EPS'],mu=str(p.MU),scalar_masses=rows[-1]['scalar_masses_GeV'],runtime_seconds=result['runtime_seconds'],peak_rss_bytes=result['peak_rss_bytes'])))
    assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
