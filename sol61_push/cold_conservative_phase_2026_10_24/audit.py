"""Read-only data/provenance and independent invariant audit; writes only declared audit result."""
import json,pathlib,hashlib,sys,numpy as np
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[1];checks=[]
def check(name,value):
 checks.append(dict(name=name,passed=bool(value)));assert value,name
for f in sorted((P/'runs').glob('*.json')):
 d=json.loads(f.read_text());check(f.stem+' pins',d['inputs_before']==d['inputs_after'])
 for path,h in d['inputs_after'].items():check(f.stem+' '+path,hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h)
 field=np.load(f.with_suffix('.npz'));m=abs(field['u'])**2;q=field['q'];h=d['history']
 check(f.stem+' actual saved subset',q.min()>-1e-10 and (q-m).max()<1e-10)
 check(f.stem+' actual saved mass',abs(m.sum()-h[-1]['M'])<1e-12 and abs(q.sum()-h[-1]['tag_mass'])<1e-12)
 check(f.stem+' all local/global ledgers',all(z['tag_min']>-1e-10 and z['tag_excess']<1e-10 and abs(z['M']-h[0]['M'])<1e-10 and abs(z['tag_mass']-h[0]['tag_mass'])<1e-10 for z in h))
 check(f.stem+' no aperture overcount',all(z['tag_aperture_Msun']<=z['field_aperture_Msun']+1e-5 for z in h))
 check(f.stem+' measured memory',d['peak_RSS_bytes']<1_000_000_000)
b=json.loads((P/'bench.json').read_text());check('CN independent dense reference',b['CN_dense_error']<1e-12);check('flux identity',b['bond_identity']<1e-12);check('complement',b['complement_error']<1e-12);check('Poisson derivative',b['poisson_derivative_error']<1e-9);check('chirp refinement',all(b['chirp'][i+1]['relative_L2']<b['chirp'][i]['relative_L2']/3 for i in range(2)))
# Independent deliberate invalid transport: moving 0.7 from a cell holding 0.1
# using its old fraction without upstream arrivals makes the tag negative.
m=np.array([1.,.1,.1]);q=np.array([.5,.02,.01]);F=np.array([.8,.7]);oldqF=F*q[:-1]/m[:-1];bad=q.copy();bad[:-1]-=oldqF;bad[1:]+=oldqF
# More stringent source tag: first donor untagged; second fully tagged.
q=np.array([0.,.1,0.]);bad=q.copy();Q=F*q[:-1]/m[:-1];bad[:-1]-=Q;bad[1:]+=Q
check('naive frozen old fraction mutation rejected',bad.min()<0)
from solver import transport
fixed=transport(m,q,F);mm=m.copy();mm[:-1]-=F;mm[1:]+=F
check('throughflow repair survives same mutation',fixed.min()>=-1e-14 and np.max(fixed-mm)<1e-14 and abs(sum(fixed)-sum(q))<1e-14)
out=dict(checks=checks,case_count=len(list((P/'runs').glob('*.json'))),interpretation='finite local transport and pins verified; stopped galaxy runs are not physical dwarf closure')
path=pathlib.Path(sys.argv[1]);path.write_text(json.dumps(out,indent=2)+'\n');print('checked',len(checks),'checks',out['case_count'],'cases')
