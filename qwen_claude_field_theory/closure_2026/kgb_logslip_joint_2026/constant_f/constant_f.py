#!/usr/bin/env python3
"""Direct constant-F KGB inverse, outside the w=f*Xr normalized chart.

One local logarithmic-no-slip control, actual action derivatives, and original
coupled EF diagnostics. No particle sector or per-halo acceleration parameter.
"""
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

HERE=Path(__file__).resolve().parent
path=HERE.parent/'reference/logslip_reference.py'
spec=importlib.util.spec_from_file_location('constant_F_logslip_reference',path)
reference=importlib.util.module_from_spec(spec);spec.loader.exec_module(reference)
ef=reference.ef


def geometry_ratio(eps,y):
    a=reference.geometry(eps,y)
    enthalpy=a['rho']+a['pr']
    if enthalpy==0:raise ValueError('separate zero-enthalpy sector required')
    return (a['pt']-a['pr'])/enthalpy


def state(eps,y,X='.5',F='.525'):
    eps,y,X,F=map(mp.mpf,(eps,y,X,F));a=reference.geometry(eps,y)
    if min(F,X)<=0:raise ValueError('positive tensor coupling and timelike X required')
    c=geometry_ratio(eps,y);cr=mp.diff(lambda yy:geometry_ratio(eps,yy),y)/a['ry']
    if c<=0:raise ValueError('positive radial clock square requires c>0')
    U=2*X*c;z=-X*(2*a['g']+cr/(1+c))
    if z==0:raise ValueError('separate constant-X inverse sector required')
    p=mp.sqrt(a['B']*U);Q=2*X+U
    P=2*F*a['pr'];PX=2*F*a['prr']/z
    GX=F*p*(a['rho']+a['pr'])/(X*z)
    return dict(**a,X=X,F=F,c=c,cr=cr,U=U,z=z,p=p,Q=Q,P=P,PX=PX,GX=GX)


def jets(a):
    """(P,PX,GX,PXX,GXX); no freely specified P/G curvatures."""
    dy,dx=1/a['ry'],a['z']
    curvature=[mp.diff(lambda t:state(a['eps'],a['y']+t*dy,a['X']+t*dx,a['F'])[key],0)/a['z']
        for key in ('PX','GX')]
    return mp.matrix([a['P'],a['PX'],a['GX'],*curvature])


def evaluate(eps='1e-6',y='.1',X='.5',F='.525'):
    a=state(eps,y,X,F);jet=jets(a)
    r,B,Br,g,X,F,U,z,p,Q=(a[key] for key in ('r','B','Br','g','X','F','U','z','p','Q'))
    Ur=-2*g*Q-2*z;pp=p*(Br/B+Ur/U)/2
    bg=dict(r=r,A=1/Q,B=B,g=g,BrB=Br/B,p=p,pr=pp,X=X,Xr=z,C=2*F,C1=mp.mpf(0),q=-mp.mpf(1))
    out=ef.evaluate(mp.mpf(1),bg,dict(zip(('P','PX','GX','PXX','GXX'),jet)),mp.mpf(0))
    P,PX,GX=jet[:3];box=(pp+(g-Br/(2*B)+2/r)*p)/B
    physical_current=[PX*p/B,-GX*box*p/B,-GX*z/B]
    physical_stress=[(2*X*GX*z/p-P)/(2*F),P/(2*F),(P+GX*p*z/B)/(2*F)]
    scale=max(abs(a['rho']),abs(a['pr']),abs(a['pt']),1)
    metric_error=max(abs(physical_stress[i]-a[key]) for i,key in enumerate(('rho','pr','pt')))/scale
    C=2*F;stress=out['stress'];EF_error=max(abs(stress[0,0]-a['rho']/C),
        abs(stress[1,1]-a['pr']/C),abs(stress[2,2]-a['pt']/C),abs(stress[0,1]))/max(scale/C,1)
    Hess=out['background']['H'];boxE=-Hess[0][0]+sum(Hess[i][i] for i in (1,2,3))
    ptE=out['background']['p'];BE=out['background']['B'];chiR=z/C**mp.mpf('1.5')
    current=[out['action']['P1']*ptE/BE,-out['action']['G1']*boxE*ptE/BE,-out['action']['G1']*chiR/BE]
    Udirect=2*z*a['c']+2*X*a['cr']
    derivative_P=mp.diff(lambda yy:2*F*reference.geometry(a['eps'],yy)['pr'],a['y'])/a['ry']
    return dict(state={key:a[key] for key in ('eps','y','X','F','rho','pr','pt','c','cr','U','z')},
        physical_jets=jet,Dfield=C,Dcoord=mp.mpf(1),
        physical_metric_error=metric_error,
        physical_current_error=abs(sum(physical_current))/max(sum(abs(value) for value in physical_current),1),
        EF_metric_error=EF_error,EF_current_error=abs(sum(current))/max(sum(abs(value) for value in current),1),
        clock_U_derivative_error=abs(Udirect-Ur)/max(abs(Udirect),abs(Ur),1),
        P_derivative_error=abs(derivative_P-PX*z)/max(abs(derivative_P),abs(PX*z),1),
        **{key:out[key] for key in ('kinetic','cross','radial','angular','light_margin',
            'bounded_EF_static_quadratic_energy','strict_EF_scalar_cone',
            'relative_clock_norm_error','relative_clock_derivative_error')},
        scope='One constant-F exterior vacuum point. A regular field map, but this actual point fails local scalar health; no all-geometry or common-mass exclusion.')


def symbolic_checks():
    r,g,gr,X,rho,pr,pt=s.symbols('r g gr X rho pr pt',nonzero=True)
    c,cr=s.symbols('c cr',real=True)
    B=(1+r*g)**2;Br=2*(1+r*g)*(g+r*gr)
    a=reference.general.metric_invariants(r,B,Br,g,gr)
    answer=[s.factor(a['pr']+g*g/B),s.factor(a['pt']-g*g/B)]
    ratio=(pt-pr)/(rho+pr);U=2*X*ratio
    answer.append(s.factor((U/(X*r)-g)*(rho+pr)-(-g*(rho+pr)+2*(pt-pr)/r)))
    z=-X*(2*g+cr/(1+c))
    answer.append(s.factor(2*z*c+2*X*cr+2*g*(2*X+2*X*c)+2*z))
    return answer


serial=reference.serial


def run(dps=65):
    with mp.workdps(dps):
        return dict(dps=dps,symbolic_residuals=symbolic_checks(),control=evaluate())


if __name__=='__main__':print(json.dumps(serial(run()),indent=2))
