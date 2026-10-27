import argparse,json
from pathlib import Path
import numpy as np
from fine_material import FineMaterial
from fine_initial import fine_initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=FineMaterial(material_h_kpc=.125,wave_R_kpc=10000.);a,x,chi,pi,meta=fine_initial(m,'dilated','nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');d=np.cos(m.r)*a+1j*np.sin(2*m.r)*a;d/=np.linalg.norm(d);mu=m.pot(a,x,True)[1];H=(m.kd+mu)*a+m.J*m.alignment(a,x,chi);H[:,:-1]+=m.ko*a[:,1:];H[:,1:]+=m.ko*a[:,:-1];analytic=2*np.real(np.vdot(H,d));rows=[]
for h in [1e-5,3e-6,1e-6]:
 fd=(m.energy(a+h*d,x,chi,pi)-m.energy(a-h*d,x,chi,pi))/(2*h);rows.append({'h':h,'relative_error':float(abs(fd-analytic)/max(1,abs(analytic)))})
assert max(v['relative_error'] for v in rows)<1e-6
out={'n':m.n,'material_force_checks':rows,'initial':m.diagnostics(a,x,chi,pi),'meta':meta,'scope':'Directional complete material force on fine geometry; inherited finite carrier/source identities unchanged. No new force-certified static equilibrium or formation conclusion.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
