from cold_limit_response import model
from scipy.optimize import brentq
import json,sys
rows=[]
for A in [10,100,1000,10000]:
 calls=[]
 def residual(pc):
  r=model(A,pc,1,tol=2e-11,gamma=.01);calls.append((pc,r['status'],r['mass']))
  return r['mass']-1 if r['status']=='edge' else 1.
 lo=1e-5;hi=1.
 root=brentq(residual,lo,hi,xtol=1e-14)
 result=model(A,root,1,tol=2e-13,gamma=.01)
 result['shoot_calls']=len(calls);result['mass_error']=abs(result['mass']-1)
 rows.append(result)
checks=dict(valid_edges=all(r['status']=='edge' for r in rows),fixed_mass=all(r['mass_error']<1e-5 for r in rows),bound=all(r.get('depth_to_infinity',-1)>0 for r in rows),cap=all(r.get('max_q',2)<1 for r in rows))
from cold_reference import cold_reference
cold=cold_reference();fine=cold_reference(2e-10)
checks['cold_reference']=cold['status']==0 and fine['status']==0 and cold['max_q']<1 and cold['min_density']>-1e-10
checks['cold_refinement']=abs(cold['edge']/fine['edge']-1)<1e-6
for row in rows:
 errors=[]
 for warm,ref in zip(row['common_profile'],fine['profile']):
  r=warm['r'];gn=r/(1+r*r)**1.5
  warm['total_g_over_cold_stiff']=(gn+warm['q'])/(gn+ref['q'])
  errors.append(abs(warm['total_g_over_cold_stiff']-1))
 row['max_sampled_cold_stiff_error']=max(errors)
 row['occupation_peak_proxy']=row['A']*row['Psi_c']
out=dict(cold_reference=cold,cold_refined=fine,rows=rows,checks=checks,all_pass=all(checks.values()),scope='fixed-mass family, chosen occupation parameter; no formation')
with open(sys.argv[1],'w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
