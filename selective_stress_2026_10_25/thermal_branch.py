"""Canonical independent-field branch with physically specified initial entropy."""
import sys,argparse,json
from pathlib import Path
import numpy as np,torch
from selective import Selective
from two_field import TwoField
from two_field_refine import transfer
from three_field_solver import finish
from joint import T,outer

class Thermal(TwoField):
 def __init__(self,scale=2.,K=30,h=.5):
  super().__init__(scale=scale,J=30/scale,thermal='virial_scaled');self.K=K;self.delta=1.;self.strength=1.;self.h=h;self.band=(30,90);self.R=120*outer(self.b)
  rm0=self.rm/scale;ed=np.r_[30*np.linspace(0,1,81)**2,np.arange(30+h,90+.1*h,h),np.geomspace(90,self.R*rm0,97)[1:]]/rm0
  self.n=len(ed)-1;r=(ed[1:]+ed[:-1])/2;self.r=T(r);self.vol=T(np.diff(ed**3)/3);self.dr=T(np.diff(r));self.rf=T((r[1:]+r[:-1])/2);self.B=T(np.tril(np.ones((self.n,self.n)),-1)+.5*np.eye(self.n));self.A=self.B/self.r[:,None]**2;self.grav=T(1/np.maximum(r[:,None],r[None,:]));self.phib=-1/torch.sqrt(self.r**2+self.b**2);nodes,weights=np.polynomial.legendre.leggauss(48);self.tt=T((nodes+1)/(2*self.R));self.tw=T(weights/(2*self.R))
 def report(self,v):
  r=Selective.report(self,v);r.update(constitutive_model='Previous canonical coherent material stress, independent vacuum field; only initial F entropy changed',thermal_policy='F entropy derived from initial200critical hydrostatic halo, then assumed conserved');return r

if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--scale',type=float,default=2.);a=ap.parse_args();dest=Path(a.output);ent=json.loads(Path('selective_stress_2026_10_25/run_virial_entropy/results.json').read_text());target=next(r for r in ent['runs'] if r['scale']==a.scale)['K_dimensionless']
 source='physical_completion_2026_10_25/run_resume_scale/virial_scaled.json' if a.scale==2 else 'physical_completion_2026_10_25/run_two_field/J_30.0.json'
 old=json.loads(Path(source).read_text());n=len(old['mass'])
 if len(old['v'])==2*n:old['v']=old['v']+old['v'][n:]
 out={'runs':[],'K_target':target,'qualification':'A changed initial entropy hypothesis, not fitted to the law. Static continuation only; no formation simulation.'}
 for K in [15.,7.5,3.75,target]:
  m=Thermal(scale=a.scale,K=K);v=transfer(m,old);assert min(m.cap(v))>0;r=finish(m,v,dest.with_name(f'K_{K:.6f}.json'),initial_iterations=0,newton_iterations=100);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['physical_scale','K','n','scaled_boundary_kpc','maximum_fractional_law_error_percent','scaled_density_rebound','density_KKT_max','gradient_max','free_exterior_T_fraction','edge_mass_fraction','optimizer']},flush=True);old=r
