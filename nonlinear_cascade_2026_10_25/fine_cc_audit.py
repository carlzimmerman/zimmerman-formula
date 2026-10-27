import argparse,json
from pathlib import Path
import numpy as np
from fine_cc import FineCC
from fine_initial import fine_initial
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();m=FineCC(eta=.01,material_h_kpc=.125,wave_R_kpc=10000.);a,x,chi,pi,meta=fine_initial(m,'dilated','nonlinear_transfer_2026_10_25/run_exact_equilibrium/state.npz');chi=1e-6*np.sin(m.wr);d=(np.cos(m.r)+1j*np.sin(2*m.r))*a;d/=np.linalg.norm(d);mu=m.pot(a,x,True)[1];mu[0]+=m.transfer(a,x,chi)[0];U=m.geometry(a,chi)[3];H=(m.kd+mu)*a+m.J*m.alignment(a,x,chi);H[0,:-1]+=m.ko*U*a[0,1:];H[0,1:]+=m.ko*np.conj(U)*a[0,:-1];H[1,:-1]+=m.ko*a[1,1:];H[1,1:]+=m.ko*a[1,:-1];pred=2*np.real(np.vdot(H,d));rows=[]
for h in [1e-5,3e-6,1e-6]:
 fd=(m.energy(a+h*d,x,chi,pi)-m.energy(a-h*d,x,chi,pi))/(2*h);error=abs(fd-pred)/max(1,abs(pred));rows.append({'step':h,'relative_error':float(error)})
assert max(r['relative_error'] for r in rows)<1e-6
out={'material_nodes':m.n,'wave_nodes':len(m.wr),'g2':m.g2,'force_checks':rows,'initial_mass':float(np.sum(abs(a)**2)),'scope':'Complete nonzero-chi material force on refined CC geometry, same physical operator; no full evolution assertion.'};Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(out)
