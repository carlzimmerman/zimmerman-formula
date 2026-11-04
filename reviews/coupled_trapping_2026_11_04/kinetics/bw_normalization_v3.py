"""Independent NWA/finiteBW inclusive numbernormalization control."""
import sys
sys.dont_write_bytecode=True
import json,time,math,resource
from pathlib import Path
import numpy as np
from scipy.linalg import solve_continuous_lyapunov
from finite_bw import pair_fast,pole
from two_species import Two,ROOT,HERE,PREF

def main(out):
 start=time.monotonic();p=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal_kinetic/run_stationary_002/result.json').read_text())['points'][1];s=json.loads((ROOT/'reviews/gravity_completion_2026_11_03/thermal/run_static_001/result.json').read_text())['points'][1]['spins'][0];rows=[]
 for bins in (32,64,128):
  model=Two(p,s,bins=bins,orbitn=16);model.scalar=[dict(r,parents=[[M,W] for M,W in r['parents'] if abs(M-pole.M)<1e-8]) for r in model.scalar];x=25.399;t=.0005;m=float(pole.mass(x));beta=math.sqrt(1-4*m*m/pole.M**2);G=pole.GRAM;Gi=144*G*beta/(32*math.pi*pole.M);total=pole.WIDTH+Gi;rho=solve_continuous_lyapunov(total/2,G);prob=float(np.trace(pole.WIDTH@rho).real/np.trace(G).real)
  K=model.scalar_kernel(x,t);f=model.f0;wn=model.W*f;nwa=float(wn@(K@f/(t**3*model.W))/(model.W@f));sig=pair_fast(x,t,model.q,24);bw=PREF*t**3/2*float(wn@sig@wn)/(model.W@f);row=next(r for r in model.scalar if abs(r['x']-x)<1e-10);widthsum=sum(W for M,W in row['parents']);gramwidth=float(np.trace(Gi).real)
  rows.append(dict(bulk_bins=bins,x=x,t=t,production_width_sum=widthsum,Gram_production_width=gramwidth,relative_production_width_error=abs(widthsum/gramwidth-1),neutral_exit_probability=prob,NWA_numberloss_rate_mu=nwa,BW_numberloss_rate_mu=bw,BW_over_NWA=bw/nwa,relative_NWA_branching_agreement=abs((bw/nwa)/prob-1)))
 checks={'production_Gram_normalization':max(r['relative_production_width_error'] for r in rows)<.005,'inclusive_degeneracy_number_normalization':rows[-1]['relative_NWA_branching_agreement']<.03,'momentum_refinement':abs(rows[-1]['BW_over_NWA']/rows[-2]['BW_over_NWA']-1)<.02};result=dict(claim_id='CT09_BW_NWA_NUMBER_NORMALIZATION',checks=checks,cases=rows,runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,scope='Off-threshold narrowwidthwindow andfrozenFDscalaroccupation; directfiniteBWloss atcellcenters comparedwith independentfinitevolumeNWApartialwidthproduction timesneutralexitprobability. No medium/Markov claim.')
 result['checks']={k:bool(v) for k,v in checks.items()};Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));assert all(checks.values())
if __name__=='__main__':main(sys.argv[1])
