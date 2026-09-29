# POST-HOC diagnostic (NOT part of the frozen run): which velocity-radius / gas convention would bring KMOS3D, KROSS, MUSE counts to the README values?
import sys; sys.argv=['x']
import importlib.util, numpy as np
spec=importlib.util.spec_from_file_location('c','cfg90.py'); c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
R,aux=c.load()
for s,ref in (("KMOS3D",(16,5)),("KROSS",(106,15)),("MUSE2",(74,43))):
    q=R[R.survey==s].reset_index(drop=True)
    print(s,"README",ref)
    for x in (1.0,1.68,2.2,3.36,4.0):
        for mass in ("tab","kross_gas"):
            if mass=="kross_gas" and s!="KROSS": continue
            xx,gb,y=c.per_object(q,"can","xfix",xfix=x,mass=mass)
            print(f"   x={x:4.2f} Rd mass={mass:9s}: <a0 {int((y<1).sum()):4d}  <0.3a0 {int((y<0.3).sum()):4d} z>=1.5<a0 {int(((y<1)&(q.z>=1.5).values).sum())}")
    xx,gb,y=c.per_object(q,"can","native",pointmass=True); print(f"   point mass native: <a0 {(y<1).sum()} <0.3 {(y<0.3).sum()}")
