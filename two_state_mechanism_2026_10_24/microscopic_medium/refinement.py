"""Independent tighter-tolerance check following long-trajectory sensitivity."""
import json
import argparse
import numpy as np
from experiment import run
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
rows=[]
for h in [.04,.08,.16]:
    for duration in [.25,2.]:
        a,x=run(17,.9,False,h,1e-10,duration)
        b,y=run(17,.9,False,h,1e-12,duration)
        rows.append(dict(coarse=a,fine=b,final_state_relative_difference=float(np.linalg.norm(x-y)/np.linalg.norm(y))))
with open(args.output,'w') as f: json.dump(rows,f,indent=2,allow_nan=False)
print(json.dumps([dict(h=r['fine']['softening'],duration=r['fine']['duration'],state_error=r['final_state_relative_difference'],energy_error=r['fine']['max_relative_energy_drift']) for r in rows]))
