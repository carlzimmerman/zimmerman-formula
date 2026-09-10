#!/usr/bin/env python3
"""Arbitrary-precision same-action reference for the logarithmic no-slip target.

Every action derivative follows the general-pressure inverse. There is no
projection onto a matching surface, independently chosen PXX/GXX, or scan.
"""
import importlib.util
import json
from pathlib import Path
import mpmath as mp

HERE=Path(__file__).resolve().parent
CLOSURE=HERE.parents[1]
PATH=CLOSURE/'kgb_pressure_freedom_2026/general_inverse/pressure_inverse.py'
spec=importlib.util.spec_from_file_location('logslip_general_pressure_inverse',PATH)
general=importlib.util.module_from_spec(spec);spec.loader.exec_module(general)
ef=general.ef
STATE_KEYS=('y','X','U','w','F')
GEOMETRY_KEYS=('r','B','Br','g','gr','rho','pr','pt','prr','Ricci')


def geometry(eps,y):
    eps,y=map(mp.mpf,(eps,y))
    if eps<=0 or y<=0:raise ValueError('positive eps,y required')
    mu=-mp.expm1(-y);lam=mu+y*mp.exp(-y)
    r=eps/mp.sqrt(y*mu);ry=-r*lam/(2*y*mu);yr=1/ry
    t=r*y
    if t>=mp.mpf('.25'):raise ValueError('outside regular logarithmic branch: r*y<1/4')
    radical=mp.sqrt(1-4*t);sqrtB=2/(1+radical);B=sqrtB*sqrtB
    Br=2*sqrtB**3*(y+r*yr)/radical
    g=y*B;gr=yr*B+y*Br
    return dict(**general.metric_invariants(r,B,Br,g,gr),eps=eps,y=y,ry=ry)


def normalized(eps,y,X,U,w,F):
    return general.normalized(geometry(eps,y),X,U,w,F)


def flow(a,f,j=0):
    """Actual X flow of (y,X,U,w,F,f); j=FXX is one shared action jet."""
    f,j=mp.mpf(f),mp.mpf(j)
    if f==0:raise ValueError('regular clock-gradient chart requires f!=0')
    return [f/(a['ry']*a['w']),mp.mpf(1),-2-2*f*a['g']*a['Q']/a['w'],
        f*a['W']/a['w'],f,j]


def first_derivatives(a,f):
    """E=D_X(kappa,Gamma) by total real differentiation."""
    point=[a[k] for k in STATE_KEYS];direction=flow(a,f)[:5]
    return mp.matrix([mp.diff(lambda t:normalized(a['eps'],
        *[x+t*v for x,v in zip(point,direction)])[key],0) for key in ('kappa','gamma')])


def jets(a,f,j=0):
    f,j=mp.mpf(f),mp.mpf(j);E=first_derivatives(a,f)
    return mp.matrix([a['P'],f*a['kappa'],f*a['gamma'],
        j*a['kappa']+f*E[0],j*a['gamma']+f*E[1]])


def next_derivatives(a,f,j=0):
    """D_X E includes df/dX=j; this is not itself the physical third jet."""
    f,j=mp.mpf(f),mp.mpf(j)
    point=[a[k] for k in STATE_KEYS]+[f];direction=flow(a,f,j)
    def moved(t,index):
        values=[x+t*v for x,v in zip(point,direction)]
        return first_derivatives(normalized(a['eps'],*values[:5]),values[5])[index]
    return mp.matrix([mp.diff(lambda t:moved(t,index),0) for index in (0,1)])


def third_jets(a,f,j=0,ell=0):
    """(PXXX,GXXX), with ell=FXXX retained explicitly."""
    f,j,ell=map(mp.mpf,(f,j,ell));v=mp.matrix([a['kappa'],a['gamma']])
    return ell*v+2*j*first_derivatives(a,f)+f*next_derivatives(a,f,j)


def matching_gap(first,second,f,j=0):
    if any(first[k]!=second[k] for k in ('F','X')):
        raise ValueError('the matching gate requires identical F and X')
    return jets(first,f,j)-jets(second,f,j)


def physical_state(a,f,j=0):
    f,j=mp.mpf(f),mp.mpf(j)
    if f==0:raise ValueError('regular physical gradient chart requires f!=0')
    return general.coefficients({key:a[key] for key in GEOMETRY_KEYS},
        a['X'],a['U'],a['w']/f,a['F'],f,j)


def evaluate(a,f,j=0):
    """Physical residuals plus independently transformed original EF M,T."""
    f,j=mp.mpf(f),mp.mpf(j);physical=physical_state(a,f,j);jet=jets(a,f,j)
    X,U,B,p,z=(physical[key] for key in ('X','U','B','p','z'))
    r,g,Br=(a[key] for key in ('r','g','Br'));Q=2*X+U
    Ur=-2*g*Q-2*z;pp=p*(Br/B+Ur/U)/2
    bg=dict(r=r,A=1/Q,B=B,g=g,BrB=Br/B,p=p,pr=pp,X=X,Xr=z,C=2*a['F'],C1=2*f,q=-mp.mpf(1))
    out=ef.evaluate(mp.mpf(1),bg,dict(zip(('P','PX','GX','PXX','GXX'),jet)),2*j)
    C,h,D,R,Bt,gt,pt=(out['background'][key] for key in ('C','h','D','R','B','g','p'))
    hp=a['W']/a['F']-a['w']**2/a['F']**2;Dp=h/2+r*hp/2
    BrBt=(Br/B-2*Dp/D)/(mp.sqrt(C)*D)
    gRt=(a['gr']+hp/2-(g+h/2)*(h/2+Dp/D))/(C*D*D)
    ge=general.metric_invariants(R,Bt,Bt*BrBt,gt,gRt)
    stress=out['stress'];scale=max(abs(ge['rho']),abs(ge['pr']),abs(ge['pt']),1)
    error=max(abs(stress[0,0]-ge['rho']),abs(stress[1,1]-ge['pr']),abs(stress[2,2]-ge['pt']),abs(stress[0,1]))/scale
    Hess=out['background']['H'];box=-Hess[0][0]+sum(Hess[i][i] for i in (1,2,3))
    chiR=(C-2*X*f)*z/(C**mp.mpf('2.5')*D)
    current=[out['action']['P1']*pt/Bt,-out['action']['G1']*box*pt/Bt,-out['action']['G1']*chiR/Bt]
    return dict(**general.physical_residuals(physical),EF_Einstein_error=error,
        EF_current_error=abs(sum(current))/max(sum(abs(v) for v in current),1),
        physical_jets=jet,Dfield=C-2*X*f,Dcoord=D,
        normalized_physical_first_jet_error=max(abs(jet[i]-physical[key])/max(abs(jet[i]),abs(physical[key]),1)
            for i,key in enumerate(('P','PX','GX'))),
        **{key:out[key] for key in ('kinetic','cross','radial','angular','light_margin',
            'bounded_EF_static_quadratic_energy','strict_EF_scalar_cone',
            'relative_clock_norm_error','relative_clock_derivative_error')},
        scope='Same-action local exterior-vacuum EF diagnostic under a regular invertible map; not a full physical-frame mode/stability or CMB certificate.')


def control(eps='1e-6'):
    a=geometry(eps,'.1');X=mp.mpf('.5');U=mp.mpf('.25')*X*a['r']*a['g']
    return normalized(eps,'.1',X,U,-mp.mpf('.05')*mp.mpf('1.5')*a['g'],mp.mpf('.525'))


def run(dps=65):
    with mp.workdps(dps):
        f,j=mp.mpf('.05'),mp.mpf('-3000');rows=[control(eps) for eps in ('1e-6','2e-6')]
        return dict(dps=dps,states=[{key:a[key] for key in ('eps','y','X','U','w','F','pr')} for a in rows],
            f=f,j=j,local=[evaluate(a,f,j) for a in rows],
            first_five_jet_gap=matching_gap(*rows,f,j),
            next_E_gap=next_derivatives(rows[0],f,j)-next_derivatives(rows[1],f,j),
            physical_third_jet_gap=third_jets(rows[0],f,j)-third_jets(rows[1],f,j),
            scope='Two actual locally healthy controls at common F,X,f,j; deliberately NOT a matched common action. The nonzero matching gap is a search gate, not a universal obstruction.')


serial=general.serial
if __name__=='__main__':print(json.dumps(serial(run()),indent=2))
