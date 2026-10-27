import json,hashlib
from pathlib import Path
import numpy as np

p=Path(__file__).parent;source=p/'run_checkpoint/results.json';d=json.loads(source.read_text());out=dict(source=str(source),sha256=hashlib.sha256(source.read_bytes()).hexdigest(),states=[])
for key,rows in d.items():
    for r in rows:
        rad=np.array(r['r']);q=np.array(r['q']);idx=np.where((q[:-1]-.5)*(q[1:]-.5)<0)[0]
        crossings=[float(rad[i]+(.5-q[i])*(rad[i+1]-rad[i])/(q[i+1]-q[i])) for i in idx]
        out['states'].append(dict(kind=key,displacement_kpc=r.get('displacement_kpc'),interpolated_crossings_kpc=crossings,energy=r['energy'],law_windows_dex=r['law_windows_dex'],qouter=r['qouter'],density_KKT_max=r['density_KKT_max']))
base=out['states'][0]
for r in out['states'][1:]:r['front_change_kpc']=r['interpolated_crossings_kpc'][-1]-base['interpolated_crossings_kpc'][-1]
(p/'assessment.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
