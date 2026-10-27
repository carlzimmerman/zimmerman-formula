import argparse,json
from pathlib import Path
import numpy as np
from hydro import Hydro as Old
from hydro_v2 import Hydro
p=argparse.ArgumentParser();p.add_argument('--output');a=p.parse_args();base=Path(__file__).parent;r=json.loads((base/'hydro_base/result.json').read_text());f=r['final'];m=Hydro();old=Old();U=np.array(f['U']);xc=np.array(f['xc']);t=f['time'];A=(t/m.ti)**(2/3);H=2/(3*t);g=m.gravity(xc,U,A)[4];rho,v,pr,cs=m.primitive(U)
new=m.gas_rhs(U,A,H,g)[0];nog=m.gas_rhs(U,A,H,np.zeros_like(g))[0];orig=old.gas_rhs(U,A,H,g)[0];err=max(abs((new[2]-nog[2])-v*(new[1]-nog[1])));idx=int(np.argmin(pr/rho));du=lambda q:q[2]-v*q[1]+.5*v*v*q[0]
checks=[dict(name='gravity_internal_energy_source_zero',passed=bool(err<1e-12),value=float(err))]
unit=6.67430e-11*m.M0*1.98847e30*(m.t0*1e9*365.25*86400)**2/(m.ell*3.085677581491367e19)**3;checks.append(dict(name='mass_length_time_G_normalization',passed=abs(unit-1)<1e-6,value=unit))
# Frozen-background quasistatic algebra, tested independently of evolution.
errors=[]
for q in [.01,1,10,100]:
 for c2 in [0,.001,1,100]:
  jb=.157;jc=.843;M=np.array([[jb-c2*q*q,jc],[jb,jc/(1+q*q)]]);det=-jc*q*q*(jb+c2)/(1+q*q);errors.append(abs(np.linalg.det(M)-det)/max(abs(det),1e-30))
checks.append(dict(name='quasistatic_determinant_identity',passed=max(errors)<1e-10,value=max(errors)))
Path(a.output).write_text(json.dumps(dict(checks=checks,failure_cell=idx,internal_energy=float(pr[idx]/(m.gamma-1)),old_internal_rate=float(du(orig)[idx]),new_internal_rate=float(du(new)[idx]),scope='Self-review; local-source check and finite algebra, not independent hydro solver.'),indent=2,default=lambda x:x.item())+'\n')
