import os
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
import argparse,hashlib,json,math,pathlib,resource,time
import numpy as np
import fit_v2 as f
from physics import *
from data import load,P,ROOT

def cut_profile(name):
 row=next(x for x in f.profiles(name) if x['tag']==('Draco_fine_late' if name=='Draco' else 'Sextans_legacy_late'))
 R=float(f.json.loads(f.PREV.read_text())['galaxies'][name]['observations']['rhalf_sph_physical']);x=row['r']/R;win=np.where(x<=.75,1.,np.where(x<1,np.cos(.5*np.pi*(x-.75)/.25)**2,0.));return row['r'],row['dm']*win**2,row

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);a=ap.parse_args();dest=pathlib.Path(a.out);dest.mkdir(exist_ok=True,parents=True);assert not (dest/'result.json').exists();start=time.time();files=sorted(set(f.artifacts()+[P/'fit_v2.py',P/'core_floor.py',P/'CORE_CONTRACT.md',P/'fit_002/result.json']));hashes=lambda:{str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest() for x in files};before=hashes();reference=json.loads((P/'fit_002/result.json').read_text());rows=[]
 for name in ['Draco','Sextans']:
  d=load(name);d['logprior']=f.prior(d);meta=reference['datasets'][name];a=meta['observed_rhalf_pc'];ms=meta['stellar_mass_Msun'];supply=meta['supply_Msun'];r,dm,profile=cut_profile(name);mc=float(dm.sum());bs=a*np.geomspace(.125,512,121);lb=np.log(bs)
  for beta in [-.5,0.]:
   corevar=np.array([project(d['R'],ar,lambda q:g_cold(q,r,dm),beta) for ar in d['aa']]).T;kernels=np.array([[project(d['R'],ar,lambda r,b=b:plummer_g(r,1e8,b),beta) for ar in d['aa']] for b in bs]).transpose(0,2,1)
   for foot in A0:
    base=np.array([project(d['R'],ar,lambda r:baryon_g(r,ms,d['aa'],foot),beta) for ar in d['aa']]).T;free=next(x for x in reference['rows'] if x['name']==name and x['footing']==foot and x['beta']==beta)['free_Plummer'];only=f.nuisance(d,base+corevar);only.update(two_delta_nll=2*(only['nll']-free['nll']),position_rms_sigma_kms=f.rms_sigma(d,base+corevar,only['mu'],only['logit']));fits=[]
    for fraction in [.25,.5,1.]:
     mass=fraction*supply-mc;assert mass>0;z=f.family_fit(d,base+corevar,kernels,lb,mass);env=mass/1e8*f.interpolate(kernels,lb,math.log(z['scale_pc']));z.update(retention=fraction,core_Msun=mc,total_Msun=mc+mass,two_delta_nll=2*(z['nll']-free['nll']),position_rms_sigma_kms=f.rms_sigma(d,base+corevar+env,z['mu'],z['logit']),minimum_added_variance_kms2=float(env.min()));assert np.min(env)>=0;fits.append(z)
    out=dict(name=name,beta=beta,footing=foot,core_Msun=mc,core_radius_pc=a,profile_tag=profile['tag'],core_only=only,core_plus_envelope=fits);rows.append(out);print(name,foot,beta,'core mass',mc,'core dNLL',only['two_delta_nll'],'half plus envelope',fits[1]['two_delta_nll'],fits[1]['scale_pc'],flush=True)
 result=dict(scope='fixed density-cut stellar-force floor plus nonnegative exterior envelope, not tagged remnant or self-consistent capture',rows=rows,inputs_before=before,inputs_after=hashes(),seconds=time.time()-start,peak_RSS_bytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss);assert before==result['inputs_after'];assert result['peak_RSS_bytes']<750_000_000;(dest/'result.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
