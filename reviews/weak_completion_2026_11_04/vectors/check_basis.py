import sys,json,time,resource
from pathlib import Path
from basis import invariants
start=time.monotonic();cases=[]
for x in (3.,5.,25.4000254000381):
 d=invariants(x);cases.append(d);print(x,d['controls'],len(d['invariants']),flush=True)
checks=dict(Goldstones=all(c['controls']['gold_physical_overlap']<1e-10 for c in cases),scalar_Ward=all(c['controls']['scalar_Goldstone_Ward']<1e-10 for c in cases),fermion_Ward=all(c['controls']['fermion_Goldstone_Ward']<1e-10 for c in cases))
Path(sys.argv[1]).write_text(json.dumps(dict(cases=cases,checks=checks,runtime_seconds=time.monotonic()-start,peak_rss_bytes_macos=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss),indent=2)+'\n')
assert all(checks.values()),checks
