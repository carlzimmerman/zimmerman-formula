"""Restricted 30-kpc feasibility test; retains all counterfactual failures."""
import argparse
import json
from pathlib import Path
from angular_gate import Field,PROFILES,checks
import numpy as np
from scipy.linalg import eigh_tridiagonal

def eigen(field,f,beta):
    curvature,_=field.stability(beta,field.kinematics(f)['C'])
    D=field.mobility_denom
    diag=(curvature+np.diag(field.Lmat))/D
    off=np.diag(field.Lmat,1)/np.sqrt(D[:-1]*D[1:])
    value=float(eigh_tridiagonal(diag,off,select='i',select_range=(0,0),eigvals_only=True,lapack_driver='stebz',tol=1e-10)[0])
    return dict(lowest_eigenvalue=value,uniform_rayleigh=float(np.sum(curvature)/np.sum(D)))


ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--n',type=int,default=64)
args=ap.parse_args()
rows=[]
for i,(_,mass,b,_) in enumerate(PROFILES):
    for f,seed in ((.3,.999),(.95,.999),(.99,.999),(.99,.001)):
        field=Field(mass,b,args.n,30.,grid='uniform')
        spec=eigen(field,f,20.)
        if seed>.5 and f>=.95 and spec['lowest_eigenvalue']<0:
            row=dict(f=f,seed=seed,n=args.n,beta=20.,length_kpc=30.,grid='uniform',
                     disposition='T endpoint unstable; failed protection before nonlinear integration')
        else:
            try:
                row=field.evolve(f,20.,seed,gradient_damping=True)
                row['disposition']='integrated'
            except (ValueError,RuntimeError) as err:
                row=dict(f=f,seed=seed,n=args.n,beta=20.,length_kpc=30.,grid='uniform',
                         disposition='numerical failure',reason=str(err))
        row.update(profile_index=i,mass_msun=mass,b_kpc=b,**spec)
        rows.append(row)
        print(json.dumps({k:v for k,v in row.items() if k in ('profile_index','n','f','seed','tethered_mass_fraction','energy_receiver_balance_max','disposition','reason','lowest_eigenvalue')}),flush=True)
payload=dict(checks=checks(),runs=rows,scope='Bounded mixing-angle 30-kpc variant; all counterfactual failures retained')
Path(args.output).write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
