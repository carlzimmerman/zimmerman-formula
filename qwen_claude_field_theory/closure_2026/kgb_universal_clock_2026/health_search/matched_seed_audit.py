#!/usr/bin/env python3
"""Independent five-variable real-differentiation audit of actual matched seeds.

Root-finding uses all five normalized jets, not the author's preservation
determinant. Curvatures use mp.diff along the full X-flow, never complex-step.
The next-drift check also has a finite-difference original-raw-jet control.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sys
import mpmath as mp
import numpy as np

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'health'))
sys.path.insert(0,str(HERE.parents[1]/'kgb_nonaffine_clock_2026/dictionary'))
import common_interval as health
import general_ef as ef
import signed_search

INITIAL={
    '.03':('259.685368537699','4164.89539996314','.15379369346185284','.026005824599963194'),
    '.128':('235.45226850741827','4208.575837390598','.15396770014297004','.11071593259911547'),
    '.5':('175.63751211836782','4367.021404532058','.15457280483846908','.4292194505706435')}


def normalized(eps,y,X,U,w,F):
    mu=-mp.expm1(-y);lam=mu+y*mp.exp(-y)
    r=eps/mp.sqrt(y*mu);ry=-r*lam/(2*y*mu);yr=1/ry
    B=1/(1-2*r*y);Br=2*(y+r*yr)*B*B;g=y*B;gr=yr*B+y*Br
    rho=4*y*y*mp.exp(-y)/(r*lam);p=mp.sqrt(B*U);Q=2*X+U
    aa=g+2/r;b=Br/(2*B)
    P=(2*w*aa+3*w*w/(2*F))/B
    L=2*F*rho+2*w*(g+b)/B+3*w*w/(F*B)
    S=2*F*aa*rho+4*w*(r*g-1)/(r*r*B)
    gamma=p*r*S/(2*Q*w);W=B*(L-X*r*S/Q)/2
    H=((2/r+w/F)*U-(2*g+w/F)*X)/p
    return dict(eps=eps,y=y,X=X,U=U,w=w,F=F,r=r,ry=ry,g=g,gr=gr,B=B,Br=Br,
        rho=rho,p=p,Q=Q,P=P,kappa=2*P/F+H*gamma,gamma=gamma,W=W,Dcoord=1+r*w/(2*F))


def flow(a,f,j=0):
    return [f/(a['ry']*a['w']),mp.mpf(1),-2-2*f*a['g']*a['Q']/a['w'],
        f*a['W']/a['w'],f,j]


def first_derivatives(a,f):
    point=[a[k] for k in ('y','X','U','w','F')];direction=flow(a,f)[:5]
    return mp.matrix([mp.diff(lambda t:normalized(a['eps'],*[x+t*v for x,v in zip(point,direction)])[key],0)
        for key in ('kappa','gamma')])


def jets(a,f,j=0):
    E=first_derivatives(a,f)
    return mp.matrix([a['P'],f*a['kappa'],f*a['gamma'],j*a['kappa']+f*E[0],j*a['gamma']+f*E[1]])


def next_derivatives(a,f,j=0):
    point=[a[k] for k in ('y','X','U','w','F')]+[f];direction=flow(a,f,j)
    def fun(t,index):
        moved=[x+t*v for x,v in zip(point,direction)]
        return first_derivatives(normalized(a['eps'],*moved[:5]),moved[5])[index]
    return mp.matrix([mp.diff(lambda t:fun(t,i),0) for i in range(2)])


def seed(u1):
    eps1,eps2,y1,X,F=map(mp.mpf,('1e-6','2e-6','.1','.5','.525'))
    f,dw,y2,u2=map(mp.mpf,INITIAL[u1]);U1=eps1*mp.mpf(u1)
    m1=normalized(eps1,y1,X,U1,-1,F);w1=-mp.mpf('.05')*dw*m1['g']
    a=normalized(eps1,y1,X,U1,w1,F);m2=normalized(eps2,y2,X,eps2*u2,-1,F)
    aa=m2['g']+2/m2['r'];w2=m2['B']*a['P']/(aa+mp.sqrt(aa*aa+3*m2['B']*a['P']/(2*F)))
    start=(f,w1,y2,u2,w2)
    scale=jets(a,f);scale=[max(abs(v),mp.mpf(1)) for v in scale]
    def equations(ff,ww1,yy2,uu2,ww2):
        first=jets(normalized(eps1,y1,X,U1,ww1,F),ff)
        second=jets(normalized(eps2,yy2,X,eps2*uu2,ww2,F),ff)
        return tuple((first[i]-second[i])/scale[i] for i in range(5))
    f,w1,y2,u2,w2=mp.findroot(equations,start,tol=mp.mpf(10)**(-mp.mp.dps+12),maxsteps=20)
    return f,[normalized(eps1,y1,X,U1,w1,F),normalized(eps2,y2,X,eps2*u2,w2,F)]


def evaluate(a,f,j):
    z=a['w']/f;U=a['U'];B=a['B'];p=a['p'];X=a['X']
    Ur=-2*a['g']*a['Q']-2*z
    bg=dict(r=a['r'],A=1/a['Q'],B=B,g=a['g'],BrB=a['Br']/B,p=p,
        pr=p*(a['Br']/B+Ur/U)/2,X=X,Xr=z,C=2*a['F'],C1=2*f,q=-mp.mpf(1))
    vector=jets(a,f,j);jet=dict(zip(('P','PX','GX','PXX','GXX'),vector))
    out=ef.evaluate(mp.mpf(1),bg,jet,2*j)
    C,h,D,R,Bt,gt,pt=(out['background'][k] for k in ('C','h','D','R','B','g','p'))
    hp=a['W']/a['F']-a['w']**2/a['F']**2
    Dp=h/2+a['r']*hp/2
    BrBt=(a['Br']/B-2*Dp/D)/(mp.sqrt(C)*D)
    gRt=(a['gr']+hp/2-(a['g']+h/2)*(h/2+Dp/D))/(C*D*D)
    geometry=[(1-1/Bt)/R**2+BrBt/(Bt*R),(1/Bt-1)/R**2+2*gt/(Bt*R),
        (gRt+gt*gt-gt*BrBt/2+(gt-BrBt/2)/R)/Bt]
    stress=out['stress'];scale=max(abs(v) for v in geometry)
    error=max(abs(stress[0,0]-geometry[0]),abs(stress[1,1]-geometry[1]),
        abs(stress[2,2]-geometry[2]),abs(stress[0,1]))/scale
    box=-out['background']['H'][0][0]+sum(out['background']['H'][i][i] for i in (1,2,3))
    chiR=(C-2*X*f)*z/(C**mp.mpf('2.5')*D)
    current=[out['action']['P1']*pt/Bt,-out['action']['G1']*box*pt/Bt,-out['action']['G1']*chiR/Bt]
    return dict(**{key:out[key] for key in ('kinetic','cross','radial','angular','light_margin')},
        strict_EF=out['strict_EF_scalar_cone'],Einstein_relative_error=error,
        current_relative_error=abs(sum(current))/sum(abs(v) for v in current),
        Dfield=C-2*X*f,Dcoord=D,physical_jets=vector)


def finite_raw_next(rows,f,j,reference):
    f,j=float(f),float(j);output=[]
    for step in (1e-9,3e-10,1e-10,3e-11,1e-11,3e-12):
        derivatives=[]
        for a in rows:
            point=np.array([float(a[k]) for k in ('y','X','U','w','F')]);direction=np.array(list(map(float,flow(a,mp.mpf(f),mp.mpf(j))[:5])))
            values=[]
            for sign in (-1,1):
                moved=point+sign*step*direction;ff=f+sign*step*j
                moved[4]+=j*step*step/2
                yy,xx,uu,ww,FF=moved
                _,raw=signed_search.s.raw_jet(float(a['eps']),yy,xx,uu,ww/ff,FF,ff,j)
                values.append(raw[3:])
            derivatives.append((values[1]-values[0])/(2*step*f))
        drift=derivatives[0]-derivatives[1]
        output.append(dict(step=step,drift=drift.tolist(),
            scaled_error=[float(abs(mp.mpf(drift[i])-reference[i])/max(abs(reference[i]),abs(reference[1]),1)) for i in range(2)]))
    return output


@lru_cache(None)
def run(dps=80,u1='.03'):
    with mp.workdps(dps):
        f,rows=seed(u1);initial=[jets(a,f) for a in rows]
        rel=lambda vv:max(abs(vv[0][i]-vv[1][i])/max(abs(vv[0][i]),abs(vv[1][i]),mp.mpf('1e-100')) for i in range(5))
        j=mp.mpf('1e10');halos=[evaluate(a,f,j) for a in rows];base=[evaluate(a,f,0) for a in rows]
        pencils=[]
        for a,zero,chosen in zip(rows,base,halos):
            beta=a['U']/(2*a['X']);A=(chosen['kinetic']-zero['kinetic'])/j
            pencils.append(health.Pencil(zero['kinetic'],A,zero['kinetic']-zero['angular']/beta,
                zero['radial'],zero['cross'],beta))
        common=health.common_interval(pencils,sqrt=mp.sqrt)
        N=next_derivatives(rows[0],f)-next_derivatives(rows[1],f)
        B=(next_derivatives(rows[0],f,1)-next_derivatives(rows[1],f,1))-N
        pivot=-N[0]/B[0];remaining=N[1]+pivot*B[1]
        required_health=[evaluate(a,f,pivot) for a in rows]
        return dict(u1=u1,dps=dps,f=f,states=[{k:a[k] for k in ('eps','y','X','U','w','F')} for a in rows],
            five_jet_relative_error=rel(initial),shared_j=j,
            shared_curvature_five_jet_relative_error=rel([jets(a,f,j) for a in rows]),
            common=common,halos=halos,next_N=N,next_B=B,pivot_j=pivot,pivot_remaining=remaining,
            normalized_next_obstruction=(N[0]*B[1]-N[1]*B[0])/(mp.norm(N)*mp.norm(B)),
            required_j_health=required_health,
            finite_original_raw_checks=finite_raw_next(rows,f,pivot,N+pivot*B),
            scope='Five-equation local point match and shared health control; next preservation obstructed at this seed, not a universal exclusion or CMB result')


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path);args=parser.parse_args()
    result={u:run(80,u) for u in ('.03','.128','.5')}
    payload=json.dumps(ef.serial(result),indent=2,allow_nan=False)+'\n'
    if args.result_file:args.result_file.write_text(payload)
    else:print(payload)
