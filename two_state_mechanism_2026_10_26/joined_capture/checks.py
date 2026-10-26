"""Independent operator identities, free dispersion, and stoichiometric ledger."""
import sys,json,argparse,subprocess
from pathlib import Path
import numpy as np
from fourth import diagonal,link,response
from feshbach_v2 import eliminate
sys.path.insert(0,str(Path(__file__).resolve().parent.parent/'nuclear_flux'))
from lead import modes
from branch_energy import event_sources
p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();checks={}
# Independent full block inversion versus Schur elimination with P propagation.
Hp=np.array([[.2,.08],[.08,.5]]);Hq=np.array([[-.2,.04],[.04,.1]]);V=np.array([[.07,.03],[-.02,.05]]);B=np.array([[.2,.1],[0,.3]]);L=np.array([.1+.7j,-.2+.4j]);E=.35
S,A,err=eliminate(E,Hp,V,B,L);Kp=E*np.eye(2)-Hp+B.T@(L[:,None]*B);full=np.block([[E*np.eye(2)-Hq,-V],[-V.T,Kp]]);rhs=np.vstack([np.zeros((2,2)),B.T*np.sqrt(2*L.imag)]);direct=np.linalg.solve(full,rhs)[:2];schur=np.linalg.solve(E*np.eye(2)-Hq-S,A)
checks['direct_vs_schur']=float(np.linalg.norm(direct-schur));assert checks['direct_vs_schur']<1e-12
Sc=np.eye(2)-1j*A.conj().T@schur;checks['effective_channel_unitarity']=float(np.linalg.norm(Sc.conj().T@Sc-np.eye(2)));assert checks['effective_channel_unitarity']<1e-12
checks['optical_identity']=err
# The scalar fourth-order band has known analytic dispersion and h^4 error.
errs=[]
for h in [.2,.1,.05]:
 t=1/(100*h*h);H=diagonal(np.array([0.]),np.array([0.]),np.eye(1),t);W=link(np.eye(1),np.eye(1),np.eye(1),t);G=None
 for i in range(10):
  M=.05*np.eye(2)-H
  if i:M-=W.T@G@W
  G=np.linalg.inv(M)
 row=response(M,H,W,.05,modes);assert row['unitarity_error']<1e-12
 k=1.;disp=t*(2.5-8/3*np.cos(k*h)+1/6*np.cos(2*k*h));errs.append(abs(disp-k*k/100))
checks['dispersion_refinement_ratios']=[errs[i]/errs[i+1] for i in [0,1]];assert all(15<x<17 for x in checks['dispersion_refinement_ratios'])
# Random-looking but deterministic signed events, independent constituent vectors.
D=.03;d=event_sources(D,[.12,-.07,.09],line_event=.04)
checks['charge_error']=float(abs(np.dot([1,-1,0,0,0,1,0,0],d)))
checks['X_error']=float(abs(np.dot([1,0,1,1,1,2,0,0],d)))
checks['C_error']=float(abs(np.dot([0,1,1,1,1,1,0,0],d)))
checks['energy_error']=float(abs(np.dot([0,0,-.5,-.125,-.125,-.5-D,1,.375],d)))
assert max(checks[k] for k in ['charge_error','X_error','C_error','energy_error'])<1e-14
Path(a.output).write_text(json.dumps(dict(checks=checks,scope='Operator/software checks, no physical DR or galaxy result'),indent=2)+'\n')
