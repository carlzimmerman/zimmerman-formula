#!/usr/bin/env python3
"""Bounded common-action/health continuation in one shared pressure coefficient."""
import argparse,json
from pathlib import Path
import mpmath as mp
import numpy as np
from scipy.optimize import least_squares
import pressure_target as target

SEED=[306704.14969910035,.1800733802025929,3057.782903435222,4754.976363865769]

def pair(x,eta,y1=.1,f=1.):
    dw,y2,u2,u1=np.exp(x);X,F=.5,.525
    g=target.single(1e-6,y1,X,1e-6*u1,-1,F,f,eta)['geometry']['g']
    a=target.single(1e-6,y1,X,1e-6*u1,-.05*dw*g,F,f,eta)
    bb=target.single(2e-6,y2,X,2e-6*u2,-1,F,f,eta);geo=bb['geometry']
    aa=geo['g']+2/geo['r'];P=a['P']-2*F*geo['pr'];disc=aa*aa+1.5*geo['B']*P/F
    if disc<=0:raise ValueError('pressure root outside regular chart')
    w2=geo['B']*P/(aa+np.sqrt(disc))
    b=target.single(2e-6,y2,X,2e-6*u2,w2,F,f,eta)
    if min(a['Dcoord'],b['Dcoord'])<=0:raise ValueError('orientation failed')
    return a,b

def linear_control(A,B,scale):
    a,b=A/scale,B/scale
    if not np.dot(b,b):raise ValueError('zero control needs a separate chart')
    return -np.dot(a,b)/np.dot(b,b)

def angle(A,B,scale):
    a,b=A/scale,B/scale;den=np.linalg.norm(a)*np.linalg.norm(b)
    if not den:raise ValueError('zero-vector chart')
    return (a[0]*b[1]-a[1]*b[0])/den

def inspect(x,eta,y1=.1):
    a,b=pair(x,eta,y1);A=a['A']-b['A'];B=a['B']-b['B']
    scale=np.maximum(np.maximum(abs(a['A']),abs(b['A'])),1.)
    f=linear_control(A,B,scale);a,b=pair(x,eta,y1,f)
    if not f or not a['Dfield']:raise ValueError('singular field map')
    N=a['N']-b['N'];ns=np.maximum(np.maximum(abs(a['N']),abs(b['N'])),1.)
    j=linear_control(N,B,ns)
    residual=np.array([(a['H']-b['H'])/(1+abs(a['H'])+abs(b['H'])),
        (a['Gamma']-b['Gamma'])/(1+abs(a['Gamma'])+abs(b['Gamma'])),angle(A,B,scale),angle(N,B,ns)])
    def jets(r):return np.r_[r['P'],f*r['K'],f*r['Gamma'],j*np.array([r['K'],r['Gamma']])+f*(r['A']+f*r['B'])]
    ja,jb=jets(a),jets(b)
    rel=np.r_[(ja-jb)/np.maximum(np.maximum(abs(ja),abs(jb)),1),
        (N+j*B)/(1+abs(N)+abs(j*B))]
    return dict(eta=eta,y1=y1,parameters=np.exp(x).tolist(),f=float(f),j=float(j),
        residual=residual.tolist(),matching_relative=rel.tolist(),
        perturbative_ratio=max(a['second_order_to_first_order'],b['second_order_to_first_order']),
        states=[{k:float(r['geometry'][k] if k in ('eps','y') else r[k]) for k in ('eps','y','X','U','w','F')} for r in (a,b)])

def solve(seed,eta,y1=.1,max_nfev=80):
    out=least_squares(lambda x:inspect(x,eta,y1)['residual'],np.log(seed),
        bounds=(np.log([.01,1e-4,1e-6,1e-4]),np.log([1e7,10,5000,10000])),
        jac='3-point',x_scale='jac',ftol=3e-12,gtol=3e-12,xtol=3e-12,max_nfev=max_nfev)
    row=inspect(out.x,eta,y1);row.update(nfev=out.nfev,optimizer_status=out.status)
    return row

def health(row,dps=40):
    ref=target.reference(row['eta'])
    with mp.workdps(dps):
        f,j=map(lambda k:mp.mpf(str(row[k])),('f','j'))
        states=[ref.normalized(*[mp.mpf(str(a[k])) for k in ('eps','y','X','U','w','F')]) for a in row['states']]
        jets=[ref.jets(a,f,j) for a in states];nxt=[ref.next_derivatives(a,f,j) for a in states]
        relative=[abs(a-b)/max(abs(a),abs(b),1) for a,b in zip(list(jets[0])+list(nxt[0]),list(jets[1])+list(nxt[1]))]
        checks=[ref.evaluate(a,f,j) for a in states]
        match=bool(max(relative)<mp.mpf('1e-7'))
        return dict(dps=dps,actual_matching_relative=float(max(relative)),matched=match,
            strict=[c['strict_EF_scalar_cone'] for c in checks],
            angular_speed_squared=[float(-c['angular']/c['kinetic']) for c in checks],
            kinetic=[float(c['kinetic']) for c in checks],
            on_shell_error=float(max(c[k] for c in checks for k in ('EF_Einstein_error','EF_current_error'))),
            promote=match and all(c['strict_EF_scalar_cone'] for c in checks) and row['perturbative_ratio']<.01)

def run(etas):
    records=[];known={0:SEED}
    for eta in etas:
        try:
            seed=known[min(known,key=lambda k:abs(k-eta))]
            row=solve(seed,eta);row['health']=health(row)
            if row['health']['matched']:known[eta]=row['parameters']
            records.append(row)
            print(json.dumps(dict(eta=eta,nfev=row['nfev'],health=row['health'])),flush=True)
        except (ArithmeticError,ValueError) as exc:
            records.append(dict(eta=eta,error=str(exc)));print(json.dumps(records[-1]),flush=True)
    return dict(rows=records,theory_status='OPEN',scope='One finite pressure continuation, not a universal no-go or a forward source/PPN derivation.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path,required=True)
    p.add_argument('--etas',nargs='+',type=float,default=[0,1,-1,10,-10,100,-100,1000,-1000,5000,-5000])
    a=p.parse_args();a.result_file.write_text(json.dumps(run(a.etas),indent=2,allow_nan=False)+'\n')
