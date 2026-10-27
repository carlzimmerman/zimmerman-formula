import json,argparse
from pathlib import Path
import numpy as np
from checks import manufactured
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out={'benchmarks':[]}
    for n in (4096,8192):
        rows=[manufactured(n,2,'gaussian',s,.25) for s in range(170,178)]
        for name in ('overlap','flux'):
            ratio=np.array([r[name]/r[name+'_reference'] for r in rows]);out['benchmarks'].append(dict(nspace=n,nvel=2,max_width=.25,observable=name,ratio_mean=float(ratio.mean()),ratio_se=float(ratio.std(ddof=1)/np.sqrt(8)),seeds=8))
    Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
