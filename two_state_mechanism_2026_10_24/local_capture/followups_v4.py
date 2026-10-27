"""Targeted numerical/time/cooling controls; no retuning by object identity."""
import json
import sys
from pathlib import Path
from capture_v4 import Capture,checks

out=dict(checks=checks(),runs=[])
settings=[('half_event_step',.95,.01,.2,True,4,5e-6,512),
          ('half_softening',.95,.02,.1,True,4,5e-5,512),
          ('no_cooling',.95,.02,.2,False,4,5e-5,256),
          ('long_rotating',.95,.02,.2,True,8,5e-5,256),
          ('long_unordered',0.,.02,.2,True,8,5e-5,256)]
for name,f,dt,soft,cool,duration,budget,nq in settings:
    row=Capture(1e8,1,n=32,nq=nq,f=f,flat=.25,beta=4,seed=11,soft=soft,
                cooling=cool,energy_budget=budget).run(duration,dt)
    row.update(profile_index=1,mass_msun=1e8,b_kpc=1,case=name)
    out['runs'].append(row)
    Path(sys.argv[1]).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in row.items() if k not in ('history','final_positions','final_velocities','final_states')}),flush=True)
