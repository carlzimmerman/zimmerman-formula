"""Refresh irrational constants at120 digits; serialize/reconstruct tiny vacuum."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,time,resource,hashlib
from pathlib import Path
import mpmath as mp
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE))
import finite_normal as f
p=f.p


def main(out):
    start=time.monotonic();mp.mp.dps=120
    p.E=mp.mpf('.003');p.EPS=mp.mpf('.0001');p.NEXP=3-p.EPS;p.BC=mp.mpf('1e8')
    p.MU=mp.mpf('18170662.111498855');p.M=mp.mpf('2.435e18')/p.MU;p.ALPHA=1/p.M
    p.F=1/mp.sqrt(31);p.AA=mp.sqrt(mp.mpf(30)/31);p.KK=p.E*mp.sqrt(mp.mpf(31)/30)
    p.Q0=mp.sqrt(60/(31*p.E));p.Z=mp.mpf('7.3671437212785083116194');p.R0=p.Z/mp.sqrt(p.E)
    p.WBASE=p.M*p.F/mp.sqrt(p.EPS);p.G=mp.sqrt(mp.mpf(29)/200)*p.E
    f.A0=p.Q0/mp.sqrt(30);f.DE=mp.mpf('2.52e-47')/p.MU**4
    row=f.solve(29)
    # All inputs for independent reconstruction from serialized decimals.
    tau=mp.mpf(row['tau_real'])
    z=[mp.mpf(row[k])/p.MU for k in ('T_GeV','N_GeV','Q_GeV')]
    w=mp.mpf(row['W0_GeV3'])/(p.WBASE*p.MU**3)
    packet=dict(mp_dps=120,tau=str(tau),z=[str(v) for v in z],w0_normalized=str(w),
                constants={k:str(getattr(p,k)) for k in ('E','EPS','NEXP','BC','MU','M','ALPHA','F','AA','KK','Q0','Z','R0','WBASE','G')},
                coefficient_snapshot_sha256=hashlib.sha256((HERE/'canonical_coefficients_snapshot.json').read_bytes()).hexdigest())
    # Round trip through the exact bytes that will be delivered.
    packet=json.loads(json.dumps(packet))
    for k,v in packet['constants'].items():setattr(p,k,mp.mpf(v))
    f.A0=p.Q0/mp.sqrt(30)
    tau=mp.mpf(packet['tau']);z=list(map(mp.mpf,packet['z']));w=mp.mpf(packet['w0_normalized'])
    reconstructed=(p.data(tau,z,w)['V']+f.loop(tau,z,w,29))*p.MU**4
    error=abs(reconstructed/mp.mpf('2.52e-47')-1)
    checks=dict(serialized_tiny_vacuum_reconstructed=error<mp.mpf('1e-25'),positive_neutral_scalars=min(row['neutral_scalar_masses_GeV'])>0,phase_pair_open=row['phase_pair_open'])
    result=dict(claim_id='PG06_HIGH_PRECISION_EXPORT',checks=checks,preferred_row=row,normalized_packet=packet,reconstructed_net_V_GeV4=str(reconstructed),relative_target_error=str(error),runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                scope='Exact120-digit finite-action normalized packet with refreshed irrational constants and serialized-vacuum reconstruction; same finite-loop caveats as finite_normal.py.')
    Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert all(checks.values()),checks


if __name__=='__main__':main(sys.argv[1])
