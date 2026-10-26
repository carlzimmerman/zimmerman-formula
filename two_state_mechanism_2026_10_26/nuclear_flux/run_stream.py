"""Stream the full radial recursion; retain compact reproducible results only."""
import argparse,json,time
from pathlib import Path
import numpy as np
from electronic import states,overlap
from lead import modes
p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--basis',required=True);p.add_argument('--h',type=float,required=True);p.add_argument('--end',type=float,default=30);a=p.parse_args()
R=np.arange(round((a.end-.5)/a.h)+1)*a.h+.5;energies=[-.62,-.6,-.58];t=1/(100*a.h*a.h);Gs=[None]*len(energies);prev=None;sample=[];start=time.monotonic()
for i,r in enumerate(R):
 s=states(r,a.basis);n=len(s[3]);I=np.eye(n);H=np.diag(s[3])+2*t*I
 if prev is not None:W=-t*overlap(prev,s)
 As=[]
 for j,E in enumerate(energies):
  A=E*I-H
  if i:A=A-W.T@Gs[j]@W
  Gs[j]=np.linalg.inv(A);As.append(A)
 if i%100==0:print('grid',i,len(R),'seconds',time.monotonic()-start,flush=True);sample.append(dict(R=float(r),energies=s[3][:10].tolist()))
 prev=s
future=states(R[-1]+a.h,a.basis);O=overlap(prev,future);O=O*np.sign(np.diag(O));W=-t*O;rows=[]
for j,E in enumerate(energies):
 m=modes(H,W,E);op=m['open'];G=np.linalg.inv(As[j].astype(complex)-m['sigma']);Uin=m['U'][:,op].conj();lin=m['lambda'][op].conj();forcing=W@(Uin*lin-m['F']@Uin);psi=G@forcing;S=np.linalg.solve(m['U'],psi-Uin)[op,:]
 unitarity=float(np.linalg.norm(S.conj().T@S-np.eye(len(op))));reciprocity=float(np.linalg.norm(S-S.T));assert unitarity<1e-7 and reciprocity<1e-7
 rows.append(dict(energy=E,probabilities=(abs(S)**2).tolist(),unitarity_error=unitarity,reciprocity_error=reciprocity,mode_weights=(abs(m['U'][:,op])**2/np.sum(abs(m['U'][:,op])**2,axis=0)).tolist(),mode_residual=m['residual']))
 print('flux',E,rows[-1]['probabilities'],flush=True)
Path(a.output).write_text(json.dumps(dict(settings=dict(basis=a.basis,h=a.h,end=float(R[-1]),Rmin=.5,electronic_states=n,nuclear_reduced_mass=50,rotation='omitted, fixed molecular axis; not a total-J resolved calculation'),rows=rows,samples=sample,seconds=time.monotonic()-start,physical_DR_rates_derived=False,scope='Finite-basis neutral radial scattering with stationary coupled lead; no electron capture and no DR branching'),indent=2)+'\n')
