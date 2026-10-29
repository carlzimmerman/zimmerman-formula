import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import scipy.sparse as sp

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];REB=HERE.parent


def operator(R,rg,tt,tail):
    x=np.log(rg);n=len(rg);dx=np.diff(x)
    rows=[0,0,n-1,n-1];cols=[0,1,n-2,n-1]
    vals=[-1/dx[0]/rg[0],1/dx[0]/rg[0],-1/dx[-1]/rg[-1],1/dx[-1]/rg[-1]]
    for i in range(1,n-1):
        a,b=dx[i-1],dx[i];rows.extend([i]*3);cols.extend([i-1,i,i+1]);vals.extend([-b/(a*(a+b))/rg[i],(b-a)/(a*b)/rg[i],a/(b*(a+b))/rg[i]])
    D=sp.csr_matrix((vals,(rows,cols)),shape=(n,n))
    F=np.zeros((len(R),n));E=np.zeros_like(F)
    w=np.full(len(tt),tt[1]-tt[0]);w[[0,-1]]*=.5
    for k,r in enumerate(R):
        q=np.log(r*np.cosh(tt));kernel=w*((1-np.tanh(tt))*np.sinh(tt)/(np.pi*r)-1/(2*np.pi*r*np.cosh(tt)))
        inside=(q>=x[0])&(q<=x[-1]);ids=np.clip(np.searchsorted(x,q[inside],side='right')-1,0,n-2);frac=(q[inside]-x[ids])/(x[ids+1]-x[ids])
        np.add.at(F[k],ids,kernel[inside]*(1-frac));np.add.at(F[k],ids+1,kernel[inside]*frac)
        F[k,0]+=kernel[q<x[0]].sum()
        if tail=='linear':F[k,-1]+=kernel[q>x[-1]].sum()
        v=np.log(r)
        if v<=x[0]:E[k,0]=1
        elif v>=x[-1]:E[k,-1]=1
        else:
            i=np.searchsorted(x,v,side='right')-1;t=(v-x[i])/(x[i+1]-x[i]);E[k,i]=1-t;E[k,i+1]=t
        E[k]/=np.pi*r*r
    return E+(D.T@F.T).T


if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--mutate',action='store_true');args=ap.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    aq=REB/'F2_outer_lensing/f2_aqual.py';f2=REB/'F2_outer_lensing/f2_outer_lensing.py'
    data=ROOT/'real_research/data/lensing_rar/brouwer2021_rar';rp=[data/f'Fig-3_Lensing-rotation-curves_Massbin-{b}.txt' for b in range(1,5)]
    files=[Path(__file__),HERE/'OPERATOR_CRITERIA.md',aq,f2,*rp];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();hashes={str(p.relative_to(ROOT)):sha(p) for p in files}
    assert 'RGRID_PC = np.logspace(1.0, 10.0, 3601)' in f2.read_text()
    ns=dict(__name__='aq_readonly',__file__=str(aq));exec(compile(aq.read_text(),str(aq),'exec'),ns)
    rg=np.logspace(1.,10.,3601);rng=np.random.default_rng(20261029)
    profiles=dict(point=np.ones_like(rg),linear=rg,compact=rg**2/(rg+1e5),burkert=np.log1p((rg/1e4)**2)+2*np.log1p(rg/1e4)-2*np.arctan(rg/1e4),nonmonotone=1+.2*rng.standard_normal(len(rg)))
    errors=[];records={}
    for b,p in enumerate(rp,1):
        R=np.loadtxt(p)[:,0]*1e6
        for tail in ('const','linear'):
            A=operator(R,rg,ns['TT'],tail)
            if args.mutate:A*=1.01
            for name,m in profiles.items():
                expected=ns['delta_sigma'](R,rg,m,tail);actual=A@m
                err=float(np.max(np.abs(actual-expected))/max(np.max(np.abs(expected)),1e-300));errors.append(err);records[f'{b}|{tail}|{name}']=err
    checks=dict(forty_cases=len(errors)==40,operator_matches_source=max(errors)<1e-10,inputs_stable=all(sha(ROOT/p)==h for p,h in hashes.items()))
    result=dict(checks=checks,mutate=args.mutate,max_relative_maxnorm_error=max(errors),errors=records,input_sha256=hashes,scope='Discrete linear identity only; no L-family exclusion')
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(checks=checks,max_error=max(errors)),indent=2));raise SystemExit(0 if all(checks.values()) else 1)
