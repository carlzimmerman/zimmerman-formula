"""Parameter feasibility and nonlinear follow-up, with no morphology branch."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh_tridiagonal
from gate import Field,PROFILES,checks

LENGTHS=(.024,.1,.3,1.,3.,10.,30.,100.,300.)
FS=(0.,.3,.7,.95,.99)


def eigen(field,f,beta):
    C=field.kinematics(f)['C']
    curvature,_=field.stability(beta,C)
    D=field.mobility_denom
    diag=(curvature+np.diag(field.Lmat))/D
    off=np.diag(field.Lmat,1)/np.sqrt(D[:-1]*D[1:])
    value=float(eigh_tridiagonal(diag,off,select='i',select_range=(0,0),
                                eigvals_only=True,lapack_driver='stebz',tol=1e-10)[0])
    return dict(lowest_eigenvalue=value,uniform_rayleigh=float(np.sum(curvature)/np.sum(D)))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--mode',choices=['spectrum','evolve','refine'],required=True)
    ap.add_argument('--output',required=True);ap.add_argument('--spectrum')
    args=ap.parse_args()
    result=dict(checks=checks())
    if args.mode=='spectrum':
        rows=[]
        for i,(_,mass,b,_) in enumerate(PROFILES):
            for length in LENGTHS:
                field=Field(mass,b,64,length)
                for beta in (20.,40.):
                    for f in FS:
                        row=dict(profile_index=i,mass_msun=mass,b_kpc=b,n=64,length_kpc=length,beta=beta,f=f,**eigen(field,f,beta))
                        rows.append(row)
        candidates=[]
        for length in LENGTHS:
            for beta in (20.,40.):
                subset=[r for r in rows if r['length_kpc']==length and r['beta']==beta]
                protected=[r for r in subset if r['f']>=.95]
                converting=[r for r in subset if r['f']<=.3]
                ok=all(r['lowest_eigenvalue']>1e-4 for r in protected) and all(r['lowest_eigenvalue']< -1e-4 for r in converting)
                if ok: candidates.append(dict(length_kpc=length,beta=beta))
        result.update(rows=rows,candidates=candidates,selected=candidates[0] if candidates else None,
                      interpretation='post-hoc common-parameter feasibility, not a predicted parameter')
        print(json.dumps(dict(candidates=candidates,selected=result['selected']),indent=2))
    else:
        selected=json.loads(Path(args.spectrum).read_text())['selected']
        if selected is None: raise ValueError('No feasible candidate to evolve')
        rows=[]
        settings=[(64,f,seed) for f,seed in ((0.,.999),(.3,.999),(.7,.999),(.95,.999),(.99,.999),(.99,.001))] if args.mode=='evolve' else [
            (n,f,seed) for n in (128,256) for f,seed in ((.3,.999),(.95,.999),(.99,.001))]
        for i,(_,mass,b,_) in enumerate(PROFILES):
            for n,f,seed in settings:
                field=Field(mass,b,n,selected['length_kpc'])
                row=field.evolve(f,selected['beta'],seed)
                row.update(profile_index=i,mass_msun=mass,b_kpc=b,**eigen(field,f,selected['beta']))
                rows.append(row)
                print(json.dumps({k:row[k] for k in ('profile_index','n','f','seed','tethered_mass_fraction','energy_receiver_balance_max','lowest_eigenvalue')}),flush=True)
        result.update(selected=selected,runs=rows)
    Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')


if __name__=='__main__': main()
