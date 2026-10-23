"""Independent Hamiltonian checks of other loss channels already in the action."""
from pathlib import Path
import json,sys,math
import numpy as np
from quantum_fock_solver import Model
P=Path(__file__).resolve().parent;O=P/sys.argv[1];O.mkdir(exist_ok=True)
rows=[]
for channel in ['31','22','pair']:
 M=2*np.sqrt(1+.02**2);p=np.sqrt(M*M-1) if channel=='pair' else np.sqrt(3)
 mo=Model(energy_cut=12,number_cut=8,charge=2 if channel=='31' else 0,volume=100.,p=p)
 a=np.zeros(12,dtype=int);b=a.copy()
 if channel=='31':a[1]=3;a[4]=1;b[[0,2]]=1
 elif channel=='22':a[1]=2;a[4]=2;b[[2,3]]=1
 else:a[[7,10]]=1;b[[2,3]]=1
 i=mo.index[tuple(a)];f=mo.index[tuple(b)];delta=mo.free[i]-mo.free;inv=np.zeros_like(delta);mask=abs(delta)>1e-10;inv[mask]=1/delta[mask]
 h=mo.H3 if channel=='pair' else mo.H4;coupling=mo.g if channel=='pair' else mo.lam
 calculated=float(h[f].toarray().ravel()@(inv*h[:,i].toarray().ravel()))*coupling**2
 if channel=='31':expected=-18*mo.lam**2/(16*mo.volume**2*np.sqrt(6))
 elif channel=='22':expected=-12*mo.lam**2/(16*mo.volume**2*2)
 else:expected=-mo.g**2/(M**4*mo.volume)
 rows.append(dict(channel=channel,states=len(mo.states),Hamiltonian=calculated,covariant_normalized=expected,relative_error=abs(calculated/expected-1)))
checks={r['channel']+'_tree_matches':r['relative_error']<1e-10 for r in rows}
out=dict(checks=checks,all_pass=all(checks.values()),channels=rows,scope='Leading pair g^2 and contact 4-to-2 lambda^2 amplitudes in finite-mode Hamiltonian. Cubic-containing 4-to-2 interference and continuum collision rates are not validated here.')
(O/'results.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2));sys.exit(0 if out['all_pass'] else 1)
