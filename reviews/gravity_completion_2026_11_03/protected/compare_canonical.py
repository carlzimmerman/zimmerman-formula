"""Independent leading-CW check of the canonical finite production row."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,time,resource
from pathlib import Path
import mpmath as mp
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import solve_protected as p
mp.mp.dps=80


def main(out):
    start=time.monotonic()
    raw=json.loads((HERE.parent/'canonical/run_solve/result.json').read_text());r=raw['points'][-1]
    e=mp.mpf(str(r['e']));t=mp.mpf(str(r['t']));MP=mp.mpf('2.435e18')
    def psi(t):return p.cw(p.Z/mp.sqrt(31*e)*t,e,e,mp.sqrt(mp.mpf(29)/200)*e)/e**2
    d1=mp.diff(psi,t);d2=mp.diff(psi,t,2)
    mu=31*mp.sqrt(3)*MP*e**mp.mpf('2.5')/(4*p.Z)*d1
    ms=mu*mp.sqrt(e**3*d2/(2*p.Z**2));ma=mu*mp.sqrt(e**3*d1/(2*p.Z**2*t))
    m32=mu**2/(mp.sqrt(93)*MP)
    mchi=mp.mpf(str(r['gauginos_GeV']['U1']))*mu/mp.mpf(str(r['mu_GeV']))
    measured=dict(mu_GeV=float(mu),m_sigma_GeV=float(ms),m_phase_GeV=float(ma),m32_GeV=float(m32),mchi_GeV=float(mchi),phase_over_radial=float(ma/ms))
    target=dict(mu_GeV=r['mu_GeV'],m_sigma_GeV=r['rows'][-1]['m_sigma_GeV'],m_phase_GeV=r['rows'][-1]['m_phase_GeV'],m32_GeV=r['m32_GeV'],mchi_GeV=r['gauginos_GeV']['U1'],phase_over_radial=r['rows'][-1]['phase_over_radial'])
    errors={k:abs(measured[k]/target[k]-1) for k in target}
    checks=dict(independent_leading_vs_finite_below_half_percent=max(errors.values())<.005,phase_pair_closed_both=ma/ms>.5 and target['phase_over_radial']>.5,gravitino_light_both=m32<mchi and target['m32_GeV']<target['mchi_GeV'])
    result=dict(claim_id='PG06_CANONICAL_CROSSCHECK',checks=checks,leading=measured,finite_canonical=target,relative_differences=errors,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                scope='Independent leading exact-CW profile consistency check, not an independent reproduction of the finite canonical action or its full loop-current certificate.')
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values()),checks


if __name__=='__main__':main(sys.argv[1])
