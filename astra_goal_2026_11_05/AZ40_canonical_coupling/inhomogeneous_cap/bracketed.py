"""Same action and integrator; globally safeguarded monotone cap root."""
from planar import Model as OriginalModel, check_model, evolve, BranchError
import numpy as np
import argparse,json
from pathlib import Path
class Model(OriginalModel):
    def lam(self,rA,rB,star):
        if not self.cap:return np.zeros_like(rA)
        center=-(rA+rB+2*star)/3
        lo=center-2*self.T/3;hi=center+2*self.T/3;la=center.copy()
        for j in range(100):
            hyp=np.hypot(la,self.b*self.T)
            res=1.5*(la-center)+self.T*la/hyp
            if np.max(abs(res)/(1+abs(center)))<1e-13:return la
            lo=np.where(res<0,la,lo);hi=np.where(res>=0,la,hi)
            trial=la-res/(1.5+self.T*(self.b*self.T)**2/hyp**3)
            la=np.where((trial>lo)&(trial<hi),trial,(lo+hi)/2)
        raise BranchError('bracketed cap root failed residual test')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['check','evolve'],required=True);ap.add_argument('--n',type=int,default=17);ap.add_argument('--uncapped',action='store_true');ap.add_argument('--rtol',type=float,default=1e-7);ap.add_argument('--end',type=float,default=3.);ap.add_argument('--wall',type=float,default=280);ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=True);m=Model(a.n,not a.uncapped)
    if a.mode=='check':
        r=check_model(m)
        from scipy.optimize import brentq
        c=np.array([1.319752267106786,-20.,-2.,0.,2.,20.]);got=m.lam(c,np.zeros_like(c),np.zeros_like(c));ref=np.array([brentq(lambda x:1.5*x+v/2+x/np.hypot(x,.1),-v/3-2/3,-v/3+2/3,xtol=1e-14) for v in c]);err=float(max(abs(got-ref)));r['brent_reference_error']=err;r['checks']['bracketed_root_reference']=err<1e-12
        try:OriginalModel().lam(c,np.zeros_like(c),np.zeros_like(c));reproduced=False
        except BranchError:reproduced=True
        r['original_failure_reproduced']=reproduced;r['checks']['original_root_failure_witness']=reproduced
        (out/'results.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));ok=all(r['checks'].values())
    else:ok=evolve(m,a,out)
    raise SystemExit(not ok)
