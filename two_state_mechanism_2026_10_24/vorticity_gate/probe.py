"""Restricted 30-kpc feasibility test; retains all counterfactual failures."""
import argparse
import json
from pathlib import Path
from gate import Field,PROFILES,checks
from stiffness import eigen

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
payload=dict(checks=checks(),runs=rows,scope='30-kpc post-hoc effective-interaction feasibility; all counterfactual failures retained')
Path(args.output).write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
