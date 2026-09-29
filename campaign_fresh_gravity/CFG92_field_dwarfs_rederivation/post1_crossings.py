"""POST-RUN diagnostic (labelled post-hoc, changes no frozen number): where are the two sign changes of h(M_b) for M_* = M_b?"""
import numpy as np, sys
sys.argv=['x']; import importlib.util
spec=importlib.util.spec_from_file_location('c','cfg92.py'); c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
base=c.Cfg()
for foot in ('canonical','alt'):
  for ratio in (0.5,1.0):
    a0=c.A0[foot]; grid=np.linspace(3,11.5,1701)
    h=np.array([c.edge_phantom(10**l,a0,'RAR')[0]-(1-c.FB)*c.mcoll(ratio*10**l,base) for l in grid]); s=h>=0
    idx=np.where(s[1:]!=s[:-1])[0]; print(foot,ratio,[ (round(10**grid[i],-5), 'off->on' if s[i+1] else 'on->off') for i in idx])
