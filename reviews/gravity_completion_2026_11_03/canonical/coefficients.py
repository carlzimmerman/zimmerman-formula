import os,sys
sys.dont_write_bytecode=True
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS'):os.environ[k]='1'
import json,math,time,resource
from pathlib import Path
import numpy as np
from numpy.polynomial import Chebyshev
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(ROOT/'reviews/finite_matching_2026_11_01/gauge_diagrams'))
sys.path.insert(0,str(ROOT/'reviews/finite_matching_2026_11_01/current_matching'))
sys.path.insert(0,str(ROOT/'reviews/radial_ir_cold_2026_11_01/radial'))
from full import calculate as vacuum
from current import calculate as angular
from radial_metric import calculate as radial
Z=7.367143721278508;DOMAIN=[-.02,.3];E=.03

def calculate(s,e):
 x0=Z/math.sqrt(31*e);x=x0*math.exp(s);g=math.sqrt(29/200)*e;q2=e/31+(e*x0)**2
 v=vacuum(x,e,e,g,1.,q2,True);a=angular(x,e,e,g,1.,q2);r=radial(x,e,e,g,1.,q2);n=v['normal_data']
 return dict(s=s,e=e,U2diag=v['V2_diagrams'],U2red=v['V2_reduced'],ja=n['CWa'],jb=n['CWb'],dFh=n['deltaF_angular'],rgraph=r['total'],kgraph=a['total'],CW=v['CW'],a0=n['a0'],b0=n['b0'],da=n['deltaa'],db=n['deltab'],Haa=n['Haa'],Hbb=n['Hbb'],min_positive_scalar_m2=r['min_positive_scalar_m2'],min_positive_fermion_m2=r['min_positive_fermion_m2'],min_positive_vector_m2=r['min_positive_vector_m2'])

def main(out):
 start=time.monotonic();fits={};raw=[];controls=[];powers=dict(U2diag=4,U2red=4,ja=2.5,jb=2.5,dFh=1,rgraph=1,kgraph=1)
 for n in (21,29):
  nodes=np.cos(np.pi*(np.arange(n)+.5)/n);ss=sum(DOMAIN)/2+nodes*(DOMAIN[1]-DOMAIN[0])/2
  values=[calculate(float(s),E) for s in ss];raw+=values
  fit={k:Chebyshev.fit(ss,[v[k] for v in values],n-1,domain=DOMAIN) for k in powers}
  fits[str(n)]={k:list(map(float,p.coef)) for k,p in fit.items()}
  for s,e in [(.113,.03),(.148,.003),(.22,.03)]:
   ex=calculate(s,e);raw.append(ex)
   errors={k:abs(float(p(s))*(e/E)**powers[k]-ex[k])/max(abs(ex[k]),1e-100) for k,p in fit.items()}
   controls.append(dict(nodes=n,s=s,e=e,errors=errors))
  print('fitted',n,flush=True)
 checks=dict(all_offnode_scaling_errors_below_2e_5=max(v for c in controls for v in c['errors'].values())<2e-5,heavy_relaxation_identity=max(abs(v['U2red']-v['U2diag']+.5*((v['ja']**2/v['Haa'])+(v['jb']**2/v['Hbb']))) for v in raw)<1e-16)
 result=dict(claim_id='CANONICAL_FINITE_COEFFICIENTS',checks=checks,domain=DOMAIN,e0=E,powers=powers,fits=fits,offnode_controls=controls,raw=raw,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
 Path(out).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('checks','runtime_seconds','peak_rss_bytes_macos')}));assert all(checks.values()),checks
if __name__=='__main__':main(sys.argv[1])
