import sys,json,time,resource
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from basis import invariants
import numpy as np
start=time.monotonic();cases=[]
xs=np.r_[np.arange(2.5,6.50001,.125),[8.,10.,15.,20.,25.,25.4000254000381,30.,40.,60.,100.]]
for x in xs:
 c=invariants(float(x));cases.append(c);print(float(x),len(c['invariants']),flush=True)
checks=dict(physical_Goldstone=all(c['controls']['gold_physical_overlap']<1e-9 for c in cases),scalar_Ward=all(c['controls']['scalar_Goldstone_Ward']<1e-10 for c in cases),fermion_Ward=all(c['controls']['fermion_Goldstone_Ward']<1e-10 for c in cases),positive_currents=all(a.get('A',0)>=abs(a.get('B',0))-1e-20 for c in cases for a in c['invariants']))
Path(sys.argv[1]).write_text(json.dumps(dict(cases=cases,checks=checks,coverage='Full canonical physical VSS/VFF/SVV gauge tensors, 12 Goldstones excluded; all24 vector generators; exact tree basis. Linear convex interpolation of invariant norms declared separately from exact background energies.',runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n');assert all(checks.values()),checks
