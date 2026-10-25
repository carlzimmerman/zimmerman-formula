import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,hashlib,json,math,pathlib,resource,time
import numpy as np
import fit_v2 as f
from core_floor import cut_profile
from physics import *
from data import load,P,ROOT

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();dest=pathlib.Path(a.out);dest.mkdir(exist_ok=True,parents=True);assert not (dest/'result.json').exists();start=time.time();files=sorted(set(f.artifacts()+[P/'fit_v2.py',P/'core_floor.py',P/'core_fraction.py',P/'CORE_CONTRACT.md',P/'CORE_FRACTION_CONTRACT.md',P/'fit_002/result.json',P/'core_001/result.json']));hashes=lambda:{str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in files};before=hashes();ref=json.loads((P/'fit_002/result.json').read_text());prior=json.loads((P/'core_001/result.json').read_text());rows=[];checks=[]
 for name in ['Draco','Sextans']:
  d=load(name);d['logprior']=f.prior(d);meta=ref['datasets'][name];a=meta['observed_rhalf_pc'];ms=meta['stellar_mass_Msun'];total=.5*meta['supply_Msun'];r,dm,profile=cut_profile(name);mc=float(dm.sum());bs=a*np.geomspace(.125,512,121);lb=np.log(bs)
  for beta in [-.5,0.]:
   cv=np.array([project(d['R'],ar,lambda q:g_cold(q,r,dm),beta) for ar in d['aa']]).T;kernels=np.array([[project(d['R'],ar,lambda r,b=b:plummer_g(r,1e8,b),beta) for ar in d['aa']] for b in bs]).transpose(0,2,1)
   for foot in A0:
    base=np.array([project(d['R'],ar,lambda r:baryon_g(r,ms,d['aa'],foot),beta) for ar in d['aa']]).T;grid=[]
    for c in np.linspace(0,1,21):
     z=f.family_fit(d,base+c*cv,kernels,lb,total-c*mc);z.update(coefficient=float(c),central_cut_Msun=float(c*mc),total_Msun=total);grid.append(z)
    rf=next(x for x in ref['rows'] if x['name']==name and x['footing']==foot and x['beta']==beta);rp=next(x for x in prior['rows'] if x['name']==name and x['footing']==foot and x['beta']==beta);e0=abs(grid[0]['nll']-rf['fixed_supply_envelopes'][1]['nll']);e1=abs(grid[-1]['nll']-rp['core_plus_envelope'][1]['nll']);assert max(e0,e1)<1e-6
    best=min(grid,key=lambda x:x['nll']);rows.append(dict(name=name,footing=foot,beta=beta,original_cut_Msun=mc,total_Msun=total,grid=grid,best_grid_coefficient=best['coefficient'],best_grid_core_Msun=best['central_cut_Msun'],full_core_two_delta_nll=2*(grid[-1]['nll']-best['nll']),best_two_delta_nll_vs_free_Plummer=2*(best['nll']-rf['free_Plummer']['nll'])));checks.append(dict(name=name,footing=foot,beta=beta,c0_nll_match=e0,c1_nll_match=e1));print(name,foot,beta,'best fraction',best['coefficient'],'best mass',best['central_cut_Msun'],'full core dNLL',2*(grid[-1]['nll']-best['nll']),flush=True)
 result=dict(scope='conditional inverse central mass rearrangement at fixed total, no dynamical retention fraction or significance',rows=rows,endpoint_checks=checks,inputs_before=before,inputs_after=hashes(),seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);assert before==result['inputs_after'];assert result['peak_RSS_bytes']<750_000_000;(dest/'result.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
