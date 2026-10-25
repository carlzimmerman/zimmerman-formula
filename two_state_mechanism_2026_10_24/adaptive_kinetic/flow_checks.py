import argparse,json
from pathlib import Path
import numpy as np
from octree import leaves,cell_pairs
from checks import manufactured

def main():
    out={'cold_flow':[],'fine_gaussian':[]}
    rng=np.random.default_rng(119);n=1024;x=rng.uniform(-1,1,(2*n,3));m=np.full(2*n,1/n)
    for width in (1.,.5,.25):
        tree=leaves(x,width,target=100000)
        row={'width':width}
        for name,v in [('coflow',np.tile([1.,2.,3.],(2*n,1))),('rotation',np.cross([0,0,2.],x)),('compression',-x)]:
            i,j,_,speed,_,volume=cell_pairs(x,v,n,tree,119);keep=j>=n
            row[name]=float(np.sum(m[i[keep]]*m[j[keep]]*speed[keep]/volume[keep]))
        out['cold_flow'].append(row)
    assert max(r['coflow'] for r in out['cold_flow'])==0
    assert max(r['rotation'] for r in out['cold_flow'])<1e-14
    assert out['cold_flow'][-1]['compression']<.4*out['cold_flow'][0]['compression']
    for ns in (2048,4096):
        rows=[manufactured(ns,2,'gaussian',s,.5) for s in range(170,178)]
        for observable in ('overlap','flux'):
            ratios=np.array([r[observable]/r[observable+'_reference'] for r in rows])
            out['fine_gaussian'].append(dict(nspace=ns,nvel=2,max_width=.5,seeds=8,observable=observable,ratio_mean=float(ratios.mean()),ratio_se=float(ratios.std(ddof=1)/np.sqrt(len(rows)))))
    return out
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=main();Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
