"""Existing CC action, both material and inner scalar meshes refined."""
from resolved import Resolved
from fine_material import FineMaterial
import numpy as np
class FineCC(Resolved):
 def __init__(self,material_h_kpc=.125,**kw):
  super().__init__(**kw)
  oldedges=self.edges.copy();inner=oldedges[oldedges*self.rm<.5];ed=np.r_[inner,.5/self.rm,np.arange(.5+material_h_kpc,320+material_h_kpc*.1,material_h_kpc)/self.rm,np.geomspace(320/self.rm,self.R,97)[1:]];self.edges=ed;self.r=(ed[1:]+ed[:-1])/2;self.vol=np.diff(ed**3)/3;self.n=len(self.r);self.w=((self.r[1:]+self.r[:-1])/2)**2/np.diff(self.r);self.gb=self.r/(self.r**2+self.b**2)**1.5;self.kd=.5*self.k*np.r_[self.w[0],self.w[:-1]+self.w[1:],self.w[-1]]/self.vol;self.ko=-.5*self.k*self.w/np.sqrt(self.vol[1:]*self.vol[:-1]);self.ids=np.clip(np.searchsorted(self.wr,self.r)-1,0,len(self.wr)-2);self.frac=np.clip((self.r-self.wr[self.ids])/(self.wr[self.ids+1]-self.wr[self.ids]),0,1);self.kcache={};self.wcache={};self.material_h_kpc=material_h_kpc
  R=kw.get('wave_R_kpc',10000.);h=kw.get('wave_h_kpc',2.);self.wr=np.r_[self.r[self.r*self.rm<80.],np.arange(80.,R+h*.1,h)/self.rm];ed=np.r_[0.,(self.wr[1:]+self.wr[:-1])/2,self.wr[-1]+(self.wr[-1]-self.wr[-2])/2];self.wvol=np.diff(ed**3)/3;self.ww=ed[1:-1]**2/np.diff(self.wr);self.wdiag=np.r_[self.ww[0],self.ww[:-1]+self.ww[1:],self.ww[-1]];self.gamma=30*self.c/(2000/self.rm)*np.clip((self.wr-(R-2000)/self.rm)/(2000/self.rm),0,1)**2;self.ids=np.clip(np.searchsorted(self.wr,self.r)-1,0,len(self.wr)-2);self.frac=np.clip((self.r-self.wr[self.ids])/(self.wr[self.ids+1]-self.wr[self.ids]),0,1);self.wcache={}
 pot=FineMaterial.pot
