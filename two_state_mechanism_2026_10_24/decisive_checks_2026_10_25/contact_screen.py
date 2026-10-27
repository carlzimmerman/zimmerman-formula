"""One-zone contact-thermalization proxy; not a collision integral or force law."""
import argparse,json
import numpy as np
from scipy.special import zeta
G=6.67430e-11;HB=1.054571817e-34;MS=1.98847e30;KP=3.085677581491367e19;EV=1.7826619216279e-36
eta=5.364;eps=.1;age=10*365.25*86400*1e9
profiles=[]
for M,b in [(3e5,.3),(1e8,1),(6e10,3),(1e14,300)]:
 rho=3*eta*M*MS/(4*np.pi*(b*KP)**3);v=np.sqrt(G*(1+eta)*M*MS/(6*b*KP))
 profiles.append((rho,v))
def interval(rates):
 lo=np.log(5)/(rates[2]*age)
 hi=min(-np.log(.8)/(rates[i]*age) for i in [0,1,3])
 return lo,hi
classical=np.array([rho*v for rho,v in profiles]);lo,hi=interval(classical)
rows=[]
for m in np.geomspace(1e-24,1e6,301):
 mass=m*EV
 occupation=np.array([rho/(mass*(1+eps))*(np.sqrt(2*np.pi)*HB/(mass*v))**3 for rho,v in profiles])
 rates=classical*(1+occupation)
 a,b=interval(rates)
 rows.append(dict(m_eV=float(m),disk_occupation=float(occupation[2]),disk_degenerate=bool(occupation[2]>=zeta(1.5)),gate_feasible=bool(a<=b),coefficient_interval_m2_kg=[float(a),float(b)]))
R=(profiles[0][0]/profiles[0][1]**3)/(profiles[2][0]/profiles[2][1]**3)
rate_ratio=classical[2]/classical[0]
bound=rate_ratio*(1+zeta(1.5))/(1+R*zeta(1.5))
required=np.log(5)/(-np.log(.8))
assert bound<required
r=dict(classical_gate_interval_m2_kg=[float(lo),float(hi)],classical_gate_interval_cm2_g=[float(lo*10),float(hi*10)],
 required_disk_to_dwarf_exposure_ratio=float(required),max_proxy_rate_ratio_if_disk_degenerate=float(bound),
 joint_points=sum(x['gate_feasible'] and x['disk_degenerate'] for x in rows),
 classical_or_weakly_occupied_gate_points=sum(x['gate_feasible'] for x in rows),rows=rows)
p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
with open(args.output,'w') as f:json.dump(r,f,indent=2,allow_nan=False)
print(json.dumps({k:v for k,v in r.items() if k!='rows'}))
