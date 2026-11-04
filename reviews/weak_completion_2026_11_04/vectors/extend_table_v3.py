import sys,json,time,resource
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent));from basis import invariants
import numpy as np
start=time.monotonic();prior=json.loads((Path(__file__).parent/'run_table002/result.json').read_text());cases=[]
for x in np.arange(.1,1.,.05):
 c=invariants(float(x));cases.append(c);print(float(x),flush=True)
cases+=prior['cases'];checks=dict(physical_Goldstone=all(c['controls']['gold_physical_overlap']<1e-9 for c in cases),scalar_Ward=all(c['controls']['scalar_Goldstone_Ward']<1e-10 for c in cases),fermion_Ward=all(c['controls']['fermion_Goldstone_Ward']<1e-10 for c in cases),positive_currents=all(a.get('A',0)>=abs(a.get('B',0))-1e-20 for c in cases for a in c['invariants']))
Path(sys.argv[1]).write_text(json.dumps(dict(cases=cases,checks=checks,coverage=prior['coverage'],runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n');assert all(checks.values()),checks
