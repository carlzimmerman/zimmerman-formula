import argparse,json
from pathlib import Path
import numpy as np
from reciprocal_wave import run
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();dest=Path(a.output);out={'runs':[]}
for h,dt,domain in [(.1,.04,24.),(.05,.02,24.),(.025,.01,24.),(.05,.02,36.)]:
 r=run(g=1.,h=h,dt=dt,duration=200.,domain=domain,sample_every=1);z=np.array(r['trace']);sel=np.where(z[:,1]>=.977191)[0];r['first_sampled_heat_threshold_time']=float(z[sel[0],0]) if len(sel) else None;r['exported_at_100']=float(np.interp(100,z[:,0],z[:,1]));out['runs'].append(r);dest.write_text(json.dumps(out,indent=2)+'\n');print({k:v for k,v in r.items() if k!='trace'},flush=True)
