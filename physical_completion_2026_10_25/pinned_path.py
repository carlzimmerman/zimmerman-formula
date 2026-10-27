import argparse,json
from pathlib import Path
import numpy as np
from free_formation import FreeVacuum
from pinned_solver import finish
class Pinned(FreeVacuum):
 def pin(self,R):
  rad=self.r.numpy()*self.rm;i=np.searchsorted(rad,R)-1;w=(R-rad[i])/(rad[i+1]-rad[i]);self.C=np.zeros(self.n);self.C[i]=1-w;self.C[i+1]=w;self.boundary_constraint=np.r_[np.zeros(self.n),self.C];self.pinR=R;self.pin_i=i
 def report(self,v):
  r=super().report(v);_,g=self.fg(v);gx=g[self.n:];lam=float(gx@self.C/(self.C@self.C));proj=g.copy();proj[self.n:]-=lam*self.C;p=v[self.n:];proj[self.n:][((p<=1e-8)&(proj[self.n:]>0))|((p>=1-1e-8)&(proj[self.n:]<0))]=0;rad=self.r.numpy()*self.rm;i=self.pin_i;xp=(p[i+1]-p[i])/(rad[i+1]-rad[i]);r.update(raw_gradient_max=r['gradient_max'],gradient_max=float(max(abs(proj))),constrained_radius=self.pinR,phase_constraint_error=float(self.C@p-.5),boundary_multiplier=lam,outward_generalized_force_Eunit_per_kpc=float(lam*xp));return r
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);old=json.loads(Path('physical_completion_2026_10_25/run_free_finish/prepared.json').read_text());out={'runs':[]}
 for R in [50.,40.,30.,20.,10.]:
  m=Pinned();m.pin(R);rad=m.r.numpy()*m.rm;oldR=old['interpolated_crossings_kpc'][-1];x=np.interp(rad+oldR-R,rad,old['v'][m.n:],left=1,right=0);x+=m.C*(.5-m.C@x)/(m.C@m.C);assert min(x)>=0 and max(x)<=1;v=np.r_[old['mass'],x];assert min(m.cap(v))>0;r=finish(m,v,dest.with_name(f'R_{R}.json'),initial_iterations=0,newton_iterations=100);out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:r.get(k) for k in ['constrained_radius','energy','outward_generalized_force_Eunit_per_kpc','density_KKT_max','gradient_max','phase_constraint_error','interpolated_crossings_kpc','optimizer']},flush=True)
  if not r['optimizer']['success']:break
  old=r
