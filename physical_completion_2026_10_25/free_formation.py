import argparse,json
from pathlib import Path
import numpy as np,torch
from vacuum_checked import Vacuum
from fast_complete import finish
from joint import RESERVOIR,T,outer
class FreeVacuum(Vacuum):
 def __init__(self,h=.25,domain=120,tail=96):
  super().__init__(h=h);self.R=domain*outer(self.b);ed=np.r_[35*np.linspace(0,1,81)**2,np.arange(35+h,80+.1*h,h),np.geomspace(80,self.R*self.rm,tail+1)[1:]]/self.rm;self.n=len(ed)-1;r=(ed[1:]+ed[:-1])/2;self.r=T(r);self.vol=T(np.diff(ed**3)/3);self.dr=T(np.diff(r));self.rf=T((r[1:]+r[:-1])/2);self.B=T(np.tril(np.ones((self.n,self.n)),-1)+.5*np.eye(self.n));self.A=self.B/self.r[:,None]**2;self.grav=T(1/np.maximum(r[:,None],r[None,:]));self.phib=-1/torch.sqrt(self.r**2+self.b**2);nd,wt=np.polynomial.legendre.leggauss(48);self.tt=T((nd+1)/(2*self.R));self.tw=T(wt/(2*self.R))
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);m=FreeVacuum();z=m.initial(scale=60)[:m.n];mass=np.exp(z-max(z));mass*=RESERVOIR/sum(mass);v=np.r_[mass,np.zeros(m.n)];allF=finish(m,v,dest.with_name('all_F.json'),initial_iterations=180,newton_iterations=100);out={'all_F':allF};dest.write_text(json.dumps(out,indent=2)+'\n');print('ALL_F',{k:allF.get(k) for k in ['energy','edge_mass_fraction','density_KKT_max','gradient_max','optimizer']},flush=True)
 assert allF['optimizer']['success'] and allF['edge_mass_fraction']<1e-7,'baseline must be force-converged and clear of box'
 xx=T(np.zeros(m.n)).requires_grad_(True);zz=T(np.log(allF['mass']));H=torch.autograd.functional.hessian(lambda x:m.energy(zz,x),xx).detach().numpy();sv=np.sqrt(m.vol.numpy());ev,vec=np.linalg.eigh(H/(sv[:,None]*sv[None,:]));seed=np.abs(vec[:,0]/sv);seed*=.02/max(seed);v=np.r_[allF['mass'],seed];out['seed']={'minimum_phase_H':float(ev[0]),'seed_energy_change':m.direct(v)[0]-allF['energy']};dest.write_text(json.dumps(out,indent=2)+'\n');assert ev[0]<0 and out['seed']['seed_energy_change']<0
 # Every accepted Newton step is mass-normalized, phase-bounded, cap-feasible and decreases energy.
 formed=finish(m,v,dest.with_name('formed.json'),initial_iterations=0,newton_iterations=240);out['formed']=formed;out['released_energy_Eunit']=allF['energy']-formed['energy'];out['path_check']={'energy_increase_max':float(max(np.diff([x['energy_before'] for x in formed['newton_trace']]+[formed['energy']]))),'final_cap':formed['cap_slack_min'],'mass_error':formed['mass_constraint_error'],'qualification':'Accepted steps are a feasible energy relaxation, not a Hamiltonian time history.'};dest.write_text(json.dumps(out,indent=2)+'\n');print('FORMED',{k:formed.get(k) for k in ['energy','scaled_law_error_bound_percent','scaled_density_rebound','scaled_boundary_kpc','density_KKT_max','gradient_max','free_exterior_mass','free_exterior_T_fraction','edge_mass_fraction','optimizer']},flush=True)
