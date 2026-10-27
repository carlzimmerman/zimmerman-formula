import argparse,json
from pathlib import Path
import numpy as np,torch
from vacuum_checked import Vacuum
from fast_complete import finish
from surface_checked import transfer_species
from joint import T

def family(scale):
 m=Vacuum(scale=scale,thermal='virial_scaled',h=.5);m.volume_cost=.000125;m.material_length*=np.sqrt(8);ed=np.r_[35*np.linspace(0,1,81)**2,np.arange(35.5,140.1,.5),np.geomspace(140,m.R*m.rm/scale,65)[1:]]/(m.rm/scale);m.n=len(ed)-1;r=(ed[1:]+ed[:-1])/2;m.r=T(r);m.vol=T(np.diff(ed**3)/3);m.dr=T(np.diff(r));m.rf=T((r[1:]+r[:-1])/2);m.B=T(np.tril(np.ones((m.n,m.n)),-1)+.5*np.eye(m.n));m.A=m.B/m.r[:,None]**2;m.grav=T(1/np.maximum(r[:,None],r[None,:]));m.phib=-1/torch.sqrt(m.r**2+m.b**2);return m
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('physical_completion_2026_10_25/run_vacuum/prepared.json').read_text());out={'runs':[],'couplings':{'volume_cost':.000125,'Q_multiplier':8,'thermal':'virial_scaled'}}
 for scale in [1.,2.,.5]:
  m=family(scale);source=dict(old,r=(np.array(old['r'])*scale).tolist());v,info=transfer_species(m,source);r=finish(m,v,dest.with_name(f'scale_{scale}.json'),initial_iterations=0,newton_iterations=120);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['physical_scale','scaled_law_error_bound_percent','scaled_density_rebound','scaled_boundary_kpc','density_KKT_max','gradient_max','free_exterior_mass','free_exterior_T_fraction','optimizer']},flush=True)
