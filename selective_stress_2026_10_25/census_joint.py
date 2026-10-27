"""Untested combination: larger census supply, purified independent carrier,
virial-reference F entropy, and an inside-out prepared initial basin.
"""
import argparse,json
from pathlib import Path
from types import FunctionType
import numpy as np,torch
from thermal_branch_checked import Thermal
from two_field import TwoField
from two_field_refine import transfer
from variable_mass_solver import finish
from joint import T,RESERVOIR

class CensusJoint(Thermal):
 def __init__(self,K=10.228244731903267,total_mass=53.6432722396066):
  super().__init__(scale=1.,K=K,h=.5);self.total_mass=total_mass;self.beta=40.;self.ell2=(3*np.sqrt(2/40)/self.rm)**2
  # Reuse the exact canonical native equations with an instance-local mass
  # constant. No shared module globals are modified. Both functions have no
  # free variables and their source files are pinned in the run contract.
  assert not TwoField.energy.__code__.co_freevars and not TwoField.report.__code__.co_freevars
  self.native_energy=FunctionType(TwoField.energy.__code__,dict(TwoField.energy.__globals__,RESERVOIR=total_mass))
  self.native_report=FunctionType(TwoField.report.__code__,dict(TwoField.report.__globals__,RESERVOIR=total_mass))
 def energy(self,z,p):return self.native_energy(self,z,p)
 def report(self,v):
  r=self.native_report(self,v);rho=np.array(r['mass'])/self.vol.numpy();r.update(model='Independent canonical material/carrier fields, larger census supply and virial-reference entropy; all variables free',total_dark_mass_Mb=self.total_mass,rho=rho.tolist(),maximum_fractional_law_error_percent=float(100*max(abs(np.r_[np.array(r['g_total'])/r['g_law']-1][(np.array(r['r'])>=1.5)&(np.array(r['r'])<=50)]))),edge_mass_fraction=float(sum(r['mass'][-4:])/self.total_mass),thermal_policy='Initial200critical virial-reference F entropy, assumed adiabatic');return r

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);ent=json.loads(Path('selective_stress_2026_10_25/run_census_entropy_checked/results.json').read_text())['runs'][0];m=CensusJoint(K=ent['K_dimensionless']);old=json.loads(Path('physical_completion_2026_10_25/run_two_field/J_30.0.json').read_text());v=transfer(m,old);n=m.n;mt=v[:n]*np.sin(np.pi*v[2*n:]/2)**2
 # Add the newly specified reservoir outside the prepared converted object.
 # This is initialization only: no gap, radius or phase restrictions persist.
 r=m.r.numpy()*m.rm;edges=[0.]
 for rr in r:edges.append(2*rr-edges[-1])
 source_r=np.array(ent['r_kpc']);cum=np.r_[0,ent['mass_profile']];extra=np.maximum(np.diff(np.interp(np.array(edges)**3,np.r_[0,source_r**3],cum)),0)
 R=old['scaled_boundary_kpc'];extra*=.5*(1+np.tanh((r-1.2*R)/5));extra*=((m.total_mass-RESERVOIR)/sum(extra));mass=v[:n]+extra;y=2/np.pi*np.arcsin(np.sqrt(np.clip(mt/mass,0,1)));vv=np.r_[mass,v[n:2*n],y]
 assert abs(sum(mass)-m.total_mass)<1e-10 and min(m.cap(vv))>0
 z=np.r_[np.log(mass),vv[n:]];E,g=m.fg(z);d=.01*np.sin(np.arange(3*n));errors=[]
 for dt in [1e-6,3e-7]:
  fd=(m.fg(z+dt*d)[0]-m.fg(z-dt*d)[0])/(2*dt);errors.append(float(abs(fd-g@d)/max(1,abs(fd))))
 assert max(errors)<1e-7
 r=finish(m,vv,dest.with_name('state.json'),initial_iterations=0,newton_iterations=240);out={'state':r,'gradient_checks':errors,'changed_mass_budget':m.total_mass,'initialization':'Prior converted core plus smooth outside reservoir from the derived virial reference. All fields and matter freed in minimization.','non_claim':'Prepared branch test, not formation; no fixed-5.364 or universal claim.'};dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['total_dark_mass_Mb','K','energy','scaled_boundary_kpc','maximum_fractional_law_error_percent','scaled_density_rebound','density_KKT_max','gradient_max','free_exterior_T_fraction','interpolated_crossings_kpc','optimizer']},flush=True)
