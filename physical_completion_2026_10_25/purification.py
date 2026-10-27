"""Test common strong first-order carrier barrier at fixed leading wall tension."""
import argparse,json
from pathlib import Path
import numpy as np,torch
from two_field import TwoField
from two_field_refine import transfer
from three_field_solver import finish
from joint import T
SOURCE={1.:'physical_completion_2026_10_25/run_two_field/J_30.0.json',2.:'physical_completion_2026_10_25/run_resume_scale/virial_scaled.json',.5:'physical_completion_2026_10_25/run_screen_checked/base_0.5_fixed_entropy.json'}
class Pure(TwoField):
 def __init__(self,scale,center):
  super().__init__(J=30/scale,scale=scale,thermal='virial_scaled');self.beta=40;self.ell2=(3*np.sqrt(2/40)/self.rm)**2;self.band=(max(35,np.floor((center-6)*2)/2),min(150,np.ceil((center+6)*2)/2));lo,hi=self.band;h=.03125;rm0=self.rm/scale;ed=np.r_[35*np.linspace(0,1,81)**2,np.arange(35.5,lo+.1,.5),np.arange(lo+h,hi+.1*h,h),np.arange(hi+.5,160.1,.5),np.geomspace(160,self.R*rm0,65)[1:]]/rm0;self.n=len(ed)-1;r=(ed[1:]+ed[:-1])/2;self.r=T(r);self.vol=T(np.diff(ed**3)/3);self.dr=T(np.diff(r));self.rf=T((r[1:]+r[:-1])/2);self.B=T(np.tril(np.ones((self.n,self.n)),-1)+.5*np.eye(self.n));self.A=self.B/self.r[:,None]**2;self.grav=T(1/np.maximum(r[:,None],r[None,:]));self.phib=-1/torch.sqrt(self.r**2+self.b**2)
 def report(self,v):
  r=super().report(v);rad=np.array(r['r']);err=np.log10(np.array(r['g_total'])/r['g_law']);s=self.scale;ss=(rad>=1.5*s)&(rad<=50*s);ee=np.r_[err[ss],np.interp([1.5*s,50*s],rad,err)];r.update(law_test_window_kpc=[1.5*s,50*s],scaled_law_error_bound_percent=float((10**max(abs(ee))-1)*100),maximum_fractional_law_error_percent=float(max(abs(10**ee-1))*100),fine_band_scaled_kpc=list(self.band),fine_spacing_physical_kpc=.03125*s,ell_physical_kpc=3*np.sqrt(2/40),thermal_policy='virial_scaled',Mb_Msun=6e10*s*s)
  if r['interpolated_crossings_kpc']:
   R=r['interpolated_crossings_kpc'][-1];rho=np.array(r['mass'])/self.vol.numpy();rr=rho[(rad>15*s)&(rad<1.2*R)];r.update(scaled_boundary_kpc=R/s,boundary_physical_kpc=R,scaled_density_rebound=float(max(rr/np.minimum.accumulate(rr))) if len(rr) else None,wall_inside_fine_band=bool(self.band[0]+1<R/s<self.band[1]-1))
  return r
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--scale',type=float,required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path(SOURCE[a.scale]).read_text());center=old['interpolated_crossings_kpc'][-1]/a.scale;out={'runs':[],'scope':'Common beta40, fixed physical wall tension, finite physical alignment and fixed physical wave/binding/volume coefficients. Virial-scaled entropy is still a policy, not a derived closure.'}
 for attempt in range(3):
  m=Pure(a.scale,center);v=transfer(m,old);assert min(m.cap(v))>0;r=finish(m,v,dest.with_name(f'attempt_{attempt}.json'),initial_iterations=0,newton_iterations=60);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['physical_scale','n','scaled_boundary_kpc','maximum_fractional_law_error_percent','scaled_density_rebound','density_KKT_max','gradient_max','wall_inside_fine_band','interpolated_crossings_kpc','optimizer']},flush=True)
  if r['optimizer']['success'] and r.get('wall_inside_fine_band'):break
  old=r;center=r['scaled_boundary_kpc']
