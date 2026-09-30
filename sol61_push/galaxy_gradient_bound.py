"""Check a conditional Poisson comparison bound against retained BVP samples."""
import argparse
import json
import math
from pathlib import Path
from scipy.integrate import quad
from scipy.special import beta

data=json.loads(Path('sol61_push/runs/galaxy_scalar_boundary/results.json').read_text())
qs=data['qstar']; G=1/(8*math.pi); K=16.
I=0.5*float(beta(1.75,0.5))
integral=quad(lambda x:x**2.5/(1+x*x)**2.25,0,math.inf,epsabs=1e-12,epsrel=1e-12)[0]
checks=[{'name':'beta integral matches independent quadrature','passed':abs(integral/I-1)<1e-10}]
rows=[]
for row in data['samples']:
    if row['Z']!=1: continue
    eps=row['compactness_GM_over_R']; R=row['source_radius']; Z=row['Z']
    bound=2**1.5*K/(12*math.pi*G*K*qs)**1.5*eps**1.5*math.sqrt(R)*I/Z
    departure=qs*row['maximum_relative_q_departure']
    checks.append({'name':'sampled branch lies in bound domain '+str((R,row['outer_radius'])),'passed':row['minimum_q']>=qs/2})
    checks.append({'name':'sampled scalar departure below comparison bound '+str((R,row['outer_radius'])),'passed':departure<bound})
    rows.append({'R':R,'Z':Z,'outer_radius':row['outer_radius'],'sampled_maximum_q_departure':departure,'conditional_uniform_upper_bound':bound})
result={'passed':all(c['passed'] for c in checks),'checks':checks,'beta_integral':I,'samples':rows}
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
args=parser.parse_args()
with open(args.output,'w') as f: json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
raise SystemExit(0 if result['passed'] else 1)
