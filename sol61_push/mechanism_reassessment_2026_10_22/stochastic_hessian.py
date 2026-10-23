"""Full instantaneous potential Hessian on the generated field ensemble."""
import json,sys
from pathlib import Path
import numpy as np
p=Path(__file__).parent;d=json.loads((p/'stochastic_source_run/results.json').read_text())
z=np.array(d['final_field_samples_over_H']);H=d['H_inf_GeV'];m=.001;M=2*m*np.sqrt(1+.02**2);g=2.168e-6;lam=.00881292
f=z[:,:2];x=z[:,2:];r2=np.sum(f*f,axis=1);c=np.sqrt(2)*g/H
A=lam*(r2[:,None,None]*np.eye(2)+2*f[:,:,None]*f[:,None,:])+(m/H)**2*np.eye(2)
A[:,0,0]+=c*x[:,0];A[:,1,1]-=c*x[:,0];A[:,0,1]+=c*x[:,1];A[:,1,0]+=c*x[:,1]
C=c*np.stack([np.stack([f[:,0],f[:,1]],axis=1),np.stack([-f[:,1],f[:,0]],axis=1)],axis=1)
# Block positivity avoids an ill-conditioned full 4x4 eigenvalue calculation.
S=(M/H)**2*np.eye(2)-np.swapaxes(C,1,2)@np.linalg.solve(A,C)
ae=np.linalg.eigvalsh(A);se=np.linalg.eigvalsh(S)/(M/H)**2
checks=dict(phi_block_positive=bool(np.all(ae>0)),source_schur_positive=bool(np.all(se>0)))
out=dict(checks=checks,all_pass=all(checks.values()),patches=len(z),min_phi_eigenvalue_over_H2=float(ae.min()),
    min_source_schur_eigenvalue_over_M2=float(se.min()),
    empty_phi_negative_fraction=float(np.mean((m/H)**2-c*np.sqrt(np.sum(x*x,axis=1))<0)),
    scope='Instantaneous potential Hessian only, on 4096 generated samples; no dynamical/Floquet stability or later particle-production prediction.')
Path(sys.argv[1]).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
