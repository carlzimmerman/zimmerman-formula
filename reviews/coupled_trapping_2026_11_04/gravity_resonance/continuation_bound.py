"""Future pole-only depletion envelope from a completed kinetic endpoint."""
import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,math,time,resource
import numpy as np
ROOT=Path(__file__).resolve().parents[3]

def main(input_path,output):
 start=time.monotonic();path=ROOT/input_path
 transport=json.loads(path.read_text());case=transport['case'];end=case['history'][-1]
 manifest=json.loads((path.parent/'manifest.json').read_text())
 assert manifest['run']['status']=='completed' and all(transport['checks'].values())
 assert case['reason']=='target cooling reached'
 mu=case['mu_GeV'];Tc=end['Tc_over_mu'];Y=end['Y_charged'];Tsm=Tc*mu/.02
 p=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/microphysics/run_medium001/result.json').read_text())
 G=np.array(p['production_Gram_mu2']);M=p['Mpole'];m=p['mC'];MP=2.435e18;gs=106.75
 H=math.sqrt(math.pi**2*gs/90)*Tsm*Tsm/MP;s=2*math.pi**2/45*gs*Tsm**3
 gate=.1*.44e-9/(m*mu);rows=[]
 for name,field in [('vacuum','Gamma_other_matrix_mu'),('all_FFS_blocked','Gamma_SSS_matrix_mu')]:
  width=np.array(p[field]);sig=2/(m*M*M)*float(np.trace(G@np.linalg.inv(width)))/(mu*mu)
  L=s*sig/(2*H) # RD-only, sigma at its maximum forever; a_final=infinity.
  lower=1/(1/Y+L)
  rows.append(dict(width_choice=name,sigma_max_GeVm2=sig,all_future_loss_integral_upper=L,remaining_yield_lower=lower,charged_yield_gate=gate,remaining_over_gate=lower/gate))
 checks=dict(positive_widths=all(min(np.linalg.eigvalsh(np.array(p[k])))>0 for k in ('Gamma_other_matrix_mu','Gamma_SSS_matrix_mu')),
             positive_population=Y>0,positive_future_envelope=all(q['remaining_yield_lower']>0 for q in rows))
 result=dict(claim_id='CT09_ENDPOINT_FUTURE_POLE_ENVELOPE',checks={k:bool(v) for k,v in checks.items()},
  endpoint_input=input_path,mu_GeV=mu,Tc_end_over_mu=Tc,T_SM_end_GeV=Tsm,Y_endpoint=Y,comparisons=rows,
  scope='From the supplied conditional kinetic endpoint, grant permanent scalar-pole alignment and maximal fixed-coefficient pair cross section at all velocities forever, positive-rate widths and factorized gauge-covariant pair ensemble. Does not bound uncomputed early histories, pair correlations, other poles, or a full nonlocal medium collision operator.',
  runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1],sys.argv[2])
