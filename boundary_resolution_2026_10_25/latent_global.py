import argparse,json
from pathlib import Path
import numpy as np
from latent_verify import model,hessian
from fast_complete import finish
from surface_checked import transfer_species
from joint import T

def rebuild(m,core,tail,shift):
 h=m.h
 fine=np.r_[np.arange(35+h/2,80,h),80] if shift else np.arange(35+h,80+.1*h,h)
 ed=np.r_[35*np.linspace(0,1,core+1)**2,fine,np.geomspace(80,m.R*m.rm,tail+1)[1:]]/m.rm;m.n=len(ed)-1;r=(ed[1:]+ed[:-1])/2;m.r=T(r);m.vol=T(np.diff(ed**3)/3);m.dr=T(np.diff(r));m.rf=T((r[1:]+r[:-1])/2);m.B=T(np.tril(np.ones((m.n,m.n)),-1)+.5*np.eye(m.n));m.A=m.B/m.r[:,None]**2;m.grav=T(1/np.maximum(r[:,None],r[None,:]));m.phib=-1/(m.r**2+m.b**2)**.5
 return m
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('boundary_resolution_2026_10_25/run_latent_verify/base_0.125.json').read_text());out={'runs':[]}
 for label,core,tail,shift in [('all_grid',160,128,False),('half_cell_shift',80,64,True)]:
  m=rebuild(model(.125),core,tail,shift);v,info=transfer_species(m,old);r=finish(m,v,dest.with_name(label+'.json'),initial_iterations=0,newton_iterations=60);r.update(stage=label,core_cells=core,outer_cells=tail,half_cell_shift=shift,transfer=info,hessian=hessian(m,r));out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print(label,{k:r[k] for k in ['n','law_endpoint_error_dex','density_KKT_max','gradient_max','mass_outside50','density_rebound_full','explicit_exterior_mass','explicit_exterior_T_fraction','interpolated_crossings_kpc','optimizer','hessian']},flush=True)
