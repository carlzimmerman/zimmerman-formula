import argparse,json
from pathlib import Path
import numpy as np,torch
from physical_model import Physical
from fast_complete import finish
from surface_checked import transfer_species
from joint import RESERVOIR,T
class Vacuum(Physical):
 def __init__(self,*args,vacuum_length=.01,**kw):super().__init__(*args,**kw);self.vacuum_length=vacuum_length
 def energy(self,z,x):
  return super().energy(z,x)+.5*(self.vacuum_length/self.rm)**2*torch.sum(self.rf**2/self.dr*(x[1:]-x[:-1])**2)
 def report(self,v):
  r=super().report(v);r.update(vacuum_gradient_length_kpc=self.vacuum_length,model='Independent phase carrier with nonzero vacuum gradient, canonical two-component matter kinetic energy, constant phase-volume and mass-splitting energies');return r
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);m=Vacuum();old=json.loads(Path('physical_completion_2026_10_25/run_screen_checked/base_1.0_fixed_entropy.json').read_text());v,info=transfer_species(m,old);base=finish(m,v,dest.with_name('prepared.json'),initial_iterations=0,newton_iterations=60);out={'prepared':base};dest.write_text(json.dumps(out,indent=2)+'\n');print('PREPARED',{k:base.get(k) for k in ['scaled_law_error_bound_percent','scaled_density_rebound','scaled_boundary_kpc','density_KKT_max','gradient_max','optimizer']},flush=True)
 # Independently prepare an all-F hydrostatic state, without the prepared density.
 z=m.initial(scale=12)[:m.n];mass=RESERVOIR*np.exp(z-max(z));mass*=RESERVOIR/sum(mass);v=np.r_[mass,np.zeros(m.n)];allF=finish(m,v,dest.with_name('all_F.json'),initial_iterations=160,newton_iterations=80);out['all_F']=allF;dest.write_text(json.dumps(out,indent=2)+'\n');print('ALL_F',{k:allF.get(k) for k in ['energy','density_KKT_max','gradient_max','optimizer']},flush=True)
 if not allF['optimizer']['success']:raise RuntimeError('all-F density must converge before seed test')
 xx=T(np.zeros(m.n)).requires_grad_(True);zz=T(np.log(allF['mass']));H=torch.autograd.functional.hessian(lambda x:m.energy(zz,x),xx).detach().numpy();sv=np.sqrt(m.vol.numpy());ev,vec=np.linalg.eigh(H/(sv[:,None]*sv[None,:]));seed=np.abs(vec[:,0]/sv);seed*=.02/max(seed);v=np.r_[allF['mass'],seed];Es=m.direct(v)[0];out['seed']={'minimum_volume_normalized_phase_H':float(ev[0]),'energy_change':float(Es-allF['energy']),'max_x':float(max(seed))};dest.write_text(json.dumps(out,indent=2)+'\n');print('SEED',out['seed'],flush=True)
 if ev[0]<0 and Es<allF['energy']:
  formed=finish(m,v,dest.with_name('formed.json'),initial_iterations=320,newton_iterations=100);out['formed']=formed;out['released_energy_Eunit']=allF['energy']-formed['energy'];dest.write_text(json.dumps(out,indent=2)+'\n');print('FORMED',{k:formed.get(k) for k in ['scaled_law_error_bound_percent','scaled_density_rebound','scaled_boundary_kpc','density_KKT_max','gradient_max','free_exterior_mass','free_exterior_T_fraction','optimizer']},flush=True)
