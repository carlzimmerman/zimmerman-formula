"""Same CC Hamiltonian, scalar nodes collocated with resolved inner matter."""
import sys
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'compression_current_2026_10_25'))
from krylov_checked import Krylov
class Resolved(Krylov):
 def __init__(self,**kw):
  super().__init__(**kw);R=kw.get('wave_R_kpc',10000.);h=kw.get('wave_h_kpc',2.);inner=self.r[self.r*self.rm<80.];outer=np.arange(80.,R+h*.1,h)/self.rm;self.wr=np.r_[inner,outer];edges=np.r_[0.,(self.wr[1:]+self.wr[:-1])/2,self.wr[-1]+(self.wr[-1]-self.wr[-2])/2];self.wvol=np.diff(edges**3)/3;self.ww=edges[1:-1]**2/np.diff(self.wr);self.wdiag=np.r_[self.ww[0],self.ww[:-1]+self.ww[1:],self.ww[-1]];self.gamma=30*self.c/(2000/self.rm)*np.clip((self.wr-(R-2000)/self.rm)/(2000/self.rm),0,1)**2;self.ids=np.clip(np.searchsorted(self.wr,self.r)-1,0,len(self.wr)-2);self.frac=np.clip((self.r-self.wr[self.ids])/(self.wr[self.ids+1]-self.wr[self.ids]),0,1);self.wcache={};assert np.all(self.wvol>0)
