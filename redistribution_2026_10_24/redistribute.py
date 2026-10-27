import sys,json,argparse
from pathlib import Path
import numpy as np,torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'material_interface_2026_10_24'))
from mixed_carrier import Mixed,transfer_species
from polish import polish
from joint import RESERVOIR
class Capillary(Mixed):
 def __init__(self,*args,L=0,**kw):super().__init__(*args,**kw);self.L=L
 def energy(self,z,x):
  E=super().energy(z,x)
  if self.L:
   mass=RESERVOIR*torch.softmax(z,dim=0);amp=torch.sqrt(mass/self.vol);q=torch.sin(torch.pi*x/2)**2;qf=(q[1:]+q[:-1])/2;b=(4*qf*(1-qf))**2
   E=E+.5*(self.L/self.rm)**3*torch.sum(self.rf**2/self.dr*b*(amp[1:]-amp[:-1])**2)
  return E
 def report(self,v):
  r=super().report(v);r['density_stiffness_length_kpc']=self.L;rad=np.array(r['r']);err=np.log10(np.array(r['g_total'])/r['g_law']);window=(rad>=1.5)&(rad<=50);r['law_endpoint_error_dex']=float(max(max(abs(err[window])),abs(np.interp(50,rad,err)),abs(np.interp(1.5,rad,err))))
  R=r['interpolated_crossings_kpc'][-1] if r['interpolated_crossings_kpc'] else 0;mass=np.array(r['mass']);q=np.array(r['q']);outside=rad>max(50,1.2*R);r['explicit_exterior_mass']=float(sum(mass[outside]));r['explicit_exterior_T_fraction']=float(mass[outside]@q[outside]/sum(mass[outside]));r['empty_transition_cells']=int(sum((mass<1e-8)&(rad>15)&(rad<R)));return r
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('material_interface_2026_10_24/run_final_recovery/base_192.json').read_text());forced=json.loads(Path('transition_force_2026_10_24/run_required/results.json').read_text())['state'];out={'runs':[],'checks':[]}
 for start,L in [('release',0),('old',1),('old',3),('old',10)]:
  m=Capillary(n=96,domain=12,beta=.5,K=15,charge=0,L=L);m.ell2=(10/m.rm)**2;v,info=transfer_species(m,forced if start=='release' else old)
  E,g=m.direct(v);d=np.sin(np.arange(192));d[:96]*=1e-7;errors=[]
  for eps in [1e-5,3e-6,1e-6]:
   fd=(m.direct(v+eps*d)[0]-m.direct(v-eps*d)[0])/(2*eps);errors.append(abs(fd-g@d)/max(1,abs(fd)))
  assert max(errors)<1e-6;out['checks'].append(errors)
  r=polish(m,v,dest.with_name(f'checkpoint_{start}_{L}.json'),maxiter=1400);r.update(start=start,transfer=info);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r[k] for k in ['start','density_stiffness_length_kpc','law_endpoint_error_dex','density_KKT_max','explicit_exterior_mass','explicit_exterior_T_fraction','empty_transition_cells','interpolated_crossings_kpc','optimizer']},flush=True)
