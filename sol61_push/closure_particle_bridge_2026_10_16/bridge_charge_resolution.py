"""Independent adaptive radial integration with explicit occupation edges."""
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

out=Path(sys.argv[1]);assert out.is_dir()
base=Path(__file__).parent;parent=base/'reciprocal_density_bridge.py'
text=parent.read_text();marker='\ncoarse=[]';assert text.count(marker)==1
ns={'__file__':str(parent),'__name__':'bridge_definitions'}
exec(compile(text.split(marker)[0],str(parent),'exec'),ns)
previous=json.loads((base/'reciprocal_density_bridge_run_001/results.json').read_text())
local=ns['local'];source=ns['source'];cold=ns['cold'];rin=ns['rin']
check=ns['check'];rows=[]
def integrate(R,z,u,mu):
    def edge(r):return abs(mu-z*(cold(r)-1))-math.sqrt(source(r))
    grid=np.geomspace(rin,R,257);points=[rin,R]
    for l,r in zip(grid[:-1],grid[1:]):
        if edge(l)*edge(r)<0:points.append(brentq(edge,l,r,xtol=1e-12,rtol=1e-13))
    points=sorted(points);positive=negative=0.;neutral=[]
    for l,r in zip(points[:-1],points[1:]):
        mid=math.sqrt(l*r)
        if edge(mid)<=0:neutral.append([l,r]);continue
        value=quad(lambda rr:4*math.pi*rr*rr*local(rr,mu,z,u)[1],l,r,epsabs=1e-10,epsrel=2e-9,limit=200)[0]
        if value>0:positive+=value
        else:negative-=value
    return positive,negative,neutral

for old in previous['runs']:
    R,z,u=old['R'],old['coupling'],old['repulsion']
    mu=brentq(lambda mm:integrate(R,z,u,mm)[0]-integrate(R,z,u,mm)[1],0.,z*2+1,xtol=1e-13,rtol=1e-13)
    pos,neg,neutral=integrate(R,z,u,mu)
    check('adaptive charge balance '+str((R,z)),abs(pos-neg)/(pos+neg)<1e-7)
    check('independent global chemical potential '+str((R,z)),abs(mu/old['chemical_potential_relative_background']-1)<.003)
    check('independent positive charge '+str((R,z)),abs(pos/old['positive_charge']-1)<.003)
    check('independent negative charge '+str((R,z)),abs(neg/old['negative_charge_magnitude']-1)<.003)
    p0,n0,_=integrate(R,z,u,0.)
    check('uncompensated neutral-background choice fails '+str((R,z)),p0==0 and n0>0)
    check('surviving neutral cubic interval '+str((R,z)),len(neutral)>0)
    row=dict(R=R,coupling=z,mu=mu,positive_charge=pos,negative_charge_magnitude=neg,
        neutral_cubic_intervals=neutral,relative_Gauss_charge_difference=old['positive_charge']/pos-1,
        charge_at_mu_relative_background_zero=-n0)
    rows.append(row);print(json.dumps(row),flush=True)
result=dict(rows=rows,checks=ns['checks'],scope='Adaptive local-density fixed-charge comparison only; no nonlocal band, cold transport, physical halo or full stability claim')
(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
print('Completed %d controls.'%len(ns['checks']))
