#!/usr/bin/env python3
"""Solve the local kinetic-curvature window without choosing a separate action
at every point. Local jets are exploratory; global integrability is not assumed.
"""
import importlib.util
import json
from pathlib import Path
import numpy as np

spec=importlib.util.spec_from_file_location('pressure',Path(__file__).with_name('shared_pressure.py'))
source=importlib.util.module_from_spec(spec);spec.loader.exec_module(source)


def window(I,cross,radial,beta):
    """Exact quadratic stationary-point reduction, evaluated in floating point.

    Accessible matrix diag(K,radial,beta*(K-I),beta*(K-I)), with C01=cross.
    Require canonical time sign, hyperbolicity and strict interior light cone.
    """
    if I<=0 or beta<=0:return dict(exists=False,reason='nonpositive invariant or beta')
    d=abs(cross);a=beta*I;b=radial+beta*I;e=1+beta
    points=[0.,1.]
    coefficients=[beta*d,beta*a-b*e,d*e]
    if coefficients[0]!=0:
        roots=np.roots(coefficients)
    elif coefficients[1]!=0:
        roots=[-coefficients[2]/coefficients[1]]
    else:roots=[]
    points.extend(float(np.real(t)) for t in roots if abs(np.imag(t))<1e-10 and 0<float(np.real(t))<1)
    light=max((a-b*t*t+2*d*t)/(e-beta*t*t) for t in points)
    lower=max(0.,d,light);upper=I
    if radial>0:upper=min(upper,cross*cross/radial)
    if radial==0 and cross==0:return dict(exists=False,reason='degenerate radial principal')
    ok=upper-lower>1e-10*max(abs(upper),abs(lower),1e-100)
    return dict(exists=bool(ok),lower=lower,upper=upper,light_bound=light,
                chosen_K=(upper+lower)/2 if ok else None,
                reason='nonempty strict causal window' if ok else 'empty strict causal window')


def choose(eps,y,u,z,P,PX):
    row=source.local(eps,y,u,z,PX,pressure=P)
    a=window(row['health_invariant'],row['cross'],row['radial'],row['beta'])
    if not a['exists']:return dict(window=a,base=row,selected=None)
    E=row['enthalpy_stable']
    if E==0:return dict(window=a,base=row,selected=None)
    PXX=PX*(a['chosen_K']-row['kinetic'])/E
    # Independently reevaluate the original principal expression with the jet.
    selected=source.local(eps,y,u,z,PX,pressure=P,pxx=PXX)
    return dict(window=a,base=row,PXX=PXX,selected=selected,
                local_only='P,P_X,P_XX are a jet; no globally integrable or universal functions are claimed')


def main():
    rows=[]
    # Probe local freedom across the transition. Shared parameters are NOT yet
    # an action because their radial derivative consistency has not been solved.
    for y in (.1,1.,2.,10.,20.):
        for PX in (1.,1e4,1e8):
            for z in (.05,.2,.5,2.):
                a=choose(1e-6,y,0,z,0.,PX)
                rows.append(dict(y=y,PX=PX,z=z,exists=a['window']['exists'],
                    I=a['base']['health_invariant'],window=a['window'],
                    PXX=a.get('PXX'),selected=a['selected']))
    print(json.dumps(dict(local_jets=rows,feasible=sum(r['exists'] for r in rows),
                         status='Local feasibility only; not a universal field theory'),indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
