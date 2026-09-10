#!/usr/bin/env python3
"""Two actual inverse-derived pencils, not a common-action construction."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path
import sys
import numpy as np
import common_interval as h

HERE=Path(__file__).resolve().parent
sys.path.append(str(HERE.parents[1]/'kgb_nonaffine_clock_2026'))
import nonaffine_inverse as n


def actual_pencil(state):
    state=dict(state)
    eps,y,X,U,z=(state[k] for k in ('eps','y','X','U','z'))
    F,f=state.get('F',.525),state.get('f',.05)
    kwargs=dict(F0=F,f0=f,X0=X)
    a=n.inspect(eps,y,X,U,z,j0=0,**kwargs)
    K,b,R,T=(a[k] for k in ('kinetic','cross','radial','angular'))
    beta=U/(2*X);C,C1,D=2*F,2*f,2*(F-X*f)
    p=np.sqrt(n.old.metric(eps,y)['B']*U)
    slope=4*C*X*a['GX']*z/(C1*D*D*p)
    pencil=h.Pencil(K,slope,K-T/beta,R,b,beta,label='eps='+str(eps))
    step=abs(f)/eps
    vector=np.array([K,b,R,T]);predicted=np.array([slope,0,0,beta*slope])
    residual=0.
    for j in (-step,step):
        other=n.inspect(eps,y,X,U,z,j0=j,**kwargs)
        v=np.array([other[k] for k in ('kinetic','cross','radial','angular')])
        scale=np.maximum(np.maximum(abs(vector),abs(j*predicted)),1.)
        residual=max(residual,float(np.max(abs(v-vector-j*predicted)/scale)))
    if residual>2e-8:raise ArithmeticError('actual principal does not match proposed pencil')
    return pencil,dict(state=state,base=a,pencil=asdict(pencil),correlation_residual=residual)


def run_control_pair():
    pencils=[];rows=[]
    for eps in (1e-6,2e-6):
        y=.1;X,U,_=n.old.initial(eps,y,.1,.25,1.5)
        state=dict(eps=eps,y=y,X=X,U=U,z=-1.5*n.old.metric(eps,y)['g'],F=.525,f=.05)
        pencil,row=actual_pencil(state);pencils.append(pencil);rows.append(row)
    common=h.common_interval(pencils)
    if common['status']=='nonempty':
        j=common['witness']
        for row in rows:
            s=row['state']
            row['at_shared_j']=n.inspect(s['eps'],s['y'],s['X'],s['U'],s['z'],
                j0=j,F0=s['F'],f0=s['f'],X0=s['X'])
    return dict(common=common,states=rows,common_action_demonstrated=False,
        scope='Two actual local vacuum EF pencils and one shared F_XX value; the independently reconstructed P/G jets are not matched between masses')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);args=parser.parse_args()
    result=run_control_pair();payload=json.dumps(result,indent=2,allow_nan=False)+'\n'
    if args.result_file:args.result_file.write_text(payload)
    else:print(payload)
