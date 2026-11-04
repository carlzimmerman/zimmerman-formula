"""Full mixed Hessian of the four-real leading trajectory action."""
import sys,os
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
from pathlib import Path
import json,time,resource,mpmath as mp
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'reviews/gravity_completion_2026_11_03/protected'))
import solve_protected as p

def main(output):
 start=time.monotonic();mp.mp.dps=110
 packet=json.loads((ROOT/'reviews/coupled_trapping_2026_11_04/gravity_resonance/run_leading001/result.json').read_text())['packet']
 for key,value in packet['constants'].items():setattr(p,key,mp.mpf(value))
 xp=mp.mpf(packet['actual_x']);tau0=mp.mpf(packet['tau']);w=mp.mpf(packet['w'])
 def pot(*r):
  x=xp+(r[0]+1j*r[2])/mp.sqrt(62)
  tau=tau0+(r[1]+1j*r[3])/(mp.sqrt(2*p.NEXP)*p.M)
  return p.data(tau,[mp.sqrt(31)*x,0,p.Q0],w)['V']+p.cw(abs(x),p.E,p.E,p.G)
 H=mp.matrix(4);grad=[]
 for i in range(4):
  order=[0]*4;order[i]=1;grad.append(mp.diff(pot,[0]*4,order))
  for j in range(i,4):
   order=[0]*4;order[i]+=1;order[j]+=1
   H[i,j]=H[j,i]=mp.re(mp.diff(pot,[0]*4,order))
 values=mp.eigsy(H,eigvals_only=True)
 radial=H[0,0]-H[0,1]**2/H[1,1];phase=H[2,2]-H[2,3]**2/H[3,3]
 checks=dict(real_stationarity=max(abs(q) for q in grad)<mp.mpf('1e-75'),full_restricted_Hessian_positive=min(values)>0,radial_modulus_Schur_positive=radial>0,phase_modulus_Schur_positive=phase>0)
 result=dict(claim_id='CT09_LEADING_MIXED_HESSIAN',checks={k:bool(v) for k,v in checks.items()},Hessian_mu2=[[str(H[i,j]) for j in range(4)] for i in range(4)],gradient=[str(q) for q in grad],eigenvalues_mu2=[str(q) for q in values],masses_in_smallfield_canonical_coordinates_GeV=[float(mp.sqrt(q)*p.MU) for q in values],radial_modulus_Schur_mu2=str(radial),phase_modulus_Schur_mu2=str(phase),scope='FullmixedHessian forcomplexXandtau onrigidvalley; smallfieldcanonicalscaling, notfullheavy-normal/SU5quantumspectrum.',runtime_seconds=time.monotonic()-start,peak_rss_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(output).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','masses_in_smallfield_canonical_coordinates_GeV','runtime_seconds','peak_rss_bytes')}));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
