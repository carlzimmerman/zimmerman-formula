"""Finite trace shooting classification at fixed beta, using pinned IVP code."""
import argparse,json
from pathlib import Path
import numpy as np
parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
source=Path('sol61_push/expansion_bridge_radial_ivp.py')
# Load only the reviewed definitions, leaving its old evidence driver untouched.
namespace={}
definitions=source.read_text().split('\nparser=argparse.ArgumentParser();')[0]
assert 'def integrate(' in definitions and 'def diagnostics(' in definitions
exec(compile(definitions,str(source),'exec'),namespace)
integrate=namespace['integrate'];diagnostics=namespace['diagnostics']
def trial(factor,cutoff=1e-6,tight=True):
 sol=integrate(.01,factor=factor,cutoff=cutoff,tight=tight)
 row=diagnostics([np.exp(sol.t[-1])],sol.y[:,-1:])[0]
 return {'factor':factor,'event_reached':sol.status==1,'endpoint':row}
scan=[trial(f) for f in [0,.1,.2,.3,.305,.31,.32,.5]]
low=.305;high=.31;history=[]
assert trial(low)['event_reached'] and not trial(high)['event_reached']
for _ in range(12):
 mid=(low+high)/2;row=trial(mid);history.append(row)
 if row['event_reached']:low=mid
 else:high=mid
ends=[trial(low),trial(high)]
checks=[trial(low,tight=False),trial(high,tight=False)]
rechecks=[trial(f,cutoff=c) for f in [low,high] for c in [1e-7,1e-8]]
for row in rechecks: row['cutoff_note']='Further D cutoffs: see sequence low/1e-7, low/1e-8, high/1e-7, high/1e-8'
out={'near_transition_cutoff_rechecks':rechecks,'fixed_parameters':{'beta':10,'lambda':2,'H':1,'GM_initial_flux':1e-16},
 'definition':'deltaTheta0=factor beta P0^3/[9(lambda-1)], deltaW0=0; stop at D=-1e-6 or r=0.01',
 'scan':scan,'bisection_history':history,'tight_bracket':[low,high],'bracket_endpoints':ends,
 'standard_tolerance_rechecks':checks,
 'scope':'Finite event classification, not a root of D=R=0, smooth crossing, cosmological match, source solution or beta selection.'}
Path(args.output).parent.mkdir(parents=True,exist_ok=True);Path(args.output).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'bracket':out['tight_bracket'],'endpoints':[{'factor':v['factor'],'event_reached':v['event_reached'],'r':v['endpoint']['r'],'D':v['endpoint']['D'],'R':v['endpoint']['compatibility_numerator']} for v in ends],
 'standard_rechecks':[{'factor':v['factor'],'event_reached':v['event_reached']} for v in checks]},indent=2))
