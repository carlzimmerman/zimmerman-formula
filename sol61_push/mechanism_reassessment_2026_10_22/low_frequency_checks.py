import json,sys
from backreaction_response import run
rows=[]
for w in [.01,.03]:
 for scale in [2,4,8]:
  rows.append(run(w,scale*20/w,tol=2e-9))
changes=[abs(rows[i+2]['power']/rows[i+1]['power']-1) for i in [0,3]]
checks=dict(converged=all(r['status']==r['background_status']==0 for r in rows),outward=all(r['power']>0 and r['chi_imag']>0 for r in rows),energy_balance=all(r['work_residual']<1e-4 for r in rows),flux_constant=all(r['flux_variation']<1e-4 for r in rows),outer_convergence=max(changes)<.01)
from low_frequency_static_moment import static
from scipy.special import hankel1,h1vp
import numpy as np
moment=static(60)
extension=run(.003,160/.003,tol=2e-9)
checks['extension_resolved']=extension['status']==0 and extension['work_residual']<1e-4 and extension['flux_variation']<1e-4
checks['static_moment']=moment['status']==0 and moment['identity_error']<1e-4
checks['hankel_flux']=all(abs(np.imag(np.conj(hankel1(0,z))*h1vp(0,z))*np.pi*z/2-1)<1e-10 for z in [.2,2,20])
predictions=[]
for r in [extension,rows[2],rows[5]]:
 pred=np.pi*moment['S0']**2*r['omega']**5/12
 predictions.append(dict(omega=r['omega'],power=r['power'],asymptotic_power=pred,ratio=r['power']/pred))
out=dict(extension=extension,static=moment,predictions=predictions,rows=rows,outer_changes=changes,checks=checks,all_pass=all(checks.values()),scope='slow prescribed source in reduced model; no autonomous matter mode')
with open(sys.argv[1],'w') as f:json.dump(out,f,indent=2)
print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
