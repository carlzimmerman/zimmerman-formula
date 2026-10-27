"""Put the absorbing layer outside all freely evolving material cells."""
import numpy as np
from stable import StableFull,StableBO

class ExteriorAbsorber:
 def __init__(self,*args,wave_R_kpc=10000.,**kwargs):
  super().__init__(*args,wave_R_kpc=wave_R_kpc,**kwargs);width=2000/self.rm;start=(wave_R_kpc-2000)/self.rm;assert start>self.edges[-1], 'sponge must lie outside material domain';self.gamma=30*self.c/width*np.maximum((self.wr-start)/width,0)**2

class OutgoingFull(ExteriorAbsorber,StableFull):pass
class OutgoingBO(ExteriorAbsorber,StableBO):pass
