import argparse,json
import numpy as np
from reduced_system import ReducedSystem,rk4
from expanded_constraints import ExpandedPadded
from evolve_projected import rk4 as oldrk
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
s=ReducedSystem(31,evaluation=93);o=ExpandedPadded(31,evaluation=93);y=s.initial();z=o.initial()
for _ in range(200):y=rk4(s,y,.0025);z=oldrk(o,z,.0025)
f=s.fine.constrain(s.expand(y));g=o.fine.constrain(o.fine.project(o.lift(z,93)))
errors={k:float(max(abs(f[k]-g[k])))for k in ['q','N','b','pb']};diag=s.diagnostic(y,.5)
checks={'charge_equivalence':errors['q']<1e-8,'momentum_equivalence':errors['pb']<1e-4,'differentiated_constraint':diag['represented_rate_error']<1e-6}
out=dict(checks=checks,all_pass=bool(all(checks.values())),errors=errors,diagnostic=diag);open(a.output,'w').write(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));raise SystemExit(0 if out['all_pass']else 1)
