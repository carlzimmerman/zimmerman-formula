import json,argparse
from pathlib import Path
import numpy as np
from simulate import Simulation,PROFILES
from field_exact_self import ExactSelfField

class ExactSelfSimulation(Simulation):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        old=self.field3d;self.field3d=ExactSelfField(old.kappa,old.sigma,old.extent,old.spacing)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--suite',choices=['scan','refinement','interval'],required=True)
    a=ap.parse_args();out={'runs':[]}
    n=128 if a.suite=='refinement' else 64
    for p in (range(2) if a.suite=='interval' else range(4)):
        _,mass,b,_=PROFILES[p]
        for f in (0.,.95):
            for flat in ((1.,.25) if a.suite=='scan' else (.25,)):
                s=ExactSelfSimulation(mass,b,n=n,f=f,flat=flat,dt_motion=.1 if a.suite=='interval' else .2)
                row=s.run(2,.01 if a.suite=='interval' else .02);row['profile_index']=p
                out['runs'].append(row);Path(a.output).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
                print(json.dumps({k:row[k] for k in ('profile_index','f','flat','status','final','stats')}),flush=True)
