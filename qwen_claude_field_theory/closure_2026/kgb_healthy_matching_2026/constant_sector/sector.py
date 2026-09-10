#!/usr/bin/env python3
"""Constant-F normalization reduction and bounded exponential-target regimes.

No action change, particles, halo-specific a0, or common-mass claim. The exact
homogeneity removes redundant normalization searches, not geometry choices.
"""
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import time
import mpmath as mp
import sympy as s

HERE=Path(__file__).resolve().parent
CLOSURE=HERE.parents[1]


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


model=load('healthy_constant_F_model',CLOSURE/'kgb_logslip_joint_2026/constant_f/constant_f.py')
original=load('healthy_constant_F_original_principal',CLOSURE/'ticking_kgb_inverse_2026/kgb_inverse.py')
PRINCIPAL_KEYS=('kinetic','cross','radial','angular','light_margin')
EPS=('1e-6','1e-3','.03')
Y=('.001','.03','.3','1','3','6','10','20')


@lru_cache(None)
def symbolic_scaling():
    """X->a² X,F->b² F implies the original EF M->M/a² exactly."""
    template=original.principal_template();a,b=s.symbols('a b',positive=True)
    subs={template['P']:template['P']/b**2,template['P1']:template['P1']/a**2,
        template['P2']:template['P2']*b**2/a**4,
        template['G1']:template['G1']*b**2/a**3,
        template['G2']:template['G2']*b**4/a**5}
    subs.update({v:v*a/b for v in template['v']})
    subs.update({template['H'][i,j]:template['H'][i,j]*a/b**2 for i in range(4) for j in range(i,4)})
    return list((template['M'].subs(subs,simultaneous=True)-template['M']/a**2).applyfunc(s.factor))


@lru_cache(None)
def symbolic_angular_identity():
    t=original.principal_template()
    B,p,X=s.symbols('B p X',positive=True);g,z,r=s.symbols('g z r',nonzero=True)
    U=p*p/B;Q=2*X+U;GX,GXX=t['G1'],t['G2']
    H=s.diag(-g*p/B,-(g*Q+z)/p,p/(B*r),p/(B*r))
    H[0,1]=H[1,0]=g*s.sqrt(Q/B)
    subs={t['P1']:2*GX*(U/r-X*g)/p}
    subs.update(dict(zip(t['v'],[-s.sqrt(Q),p/s.sqrt(B),0,0])))
    subs.update({t['H'][i,j]:H[i,j] for i in range(4) for j in range(i,4)})
    expected=2*X*X*GX*GX/t['m']-2*GX*(g*X+z)/p+GXX*p*z/B
    return s.factor(t['M'][2,2].subs(subs)-expected)


def enthalpy(eps,y):
    a=model.reference.geometry(eps,y)
    return a['rho']+a['pr']


def zshape(eps,y):
    """Z=Xr/X without rejecting its zero, so an actual boundary can be found."""
    eps,y=mp.mpf(eps),mp.mpf(y);a=model.reference.geometry(eps,y)
    c=model.geometry_ratio(eps,y)
    cr=mp.diff(lambda yy:model.geometry_ratio(eps,yy),y)/a['ry']
    return -2*a['g']-cr/(1+c)


def angular_condition(eps,y):
    """Exact necessary condition for health: this expression must be negative.

    It equals X*M_EF[2,2], independently computed without calling the
    original principal evaluator or using PXX. All derivatives are radial.
    """
    eps,y=mp.mpf(eps),mp.mpf(y);a=model.state(eps,y)
    E=a['rho']+a['pr'];Z=a['z']/a['X'];c=a['c'];B=a['B']
    Er=mp.diff(lambda yy:enthalpy(eps,yy),y)/a['ry']
    Zr=mp.diff(lambda yy:zshape(eps,yy),y)/a['ry']
    logarithmic_GX=a['Br']/(2*B)+a['cr']/(2*c)+Er/E-3*Z/2-Zr/Z
    return B*c*E*E/(Z*Z)-E*(a['g']+Z)/Z+c*E*logarithmic_GX/Z


def boundaries(eps='1e-6'):
    eps=mp.mpf(eps)
    zz=mp.findroot(lambda y:zshape(eps,y),(mp.mpf('1'),mp.mpf('2')))
    ee=mp.findroot(lambda y:enthalpy(eps,y),(mp.mpf('14'),mp.mpf('15')))
    return dict(eps=eps,zero_z=zz,zero_enthalpy=ee,
        zero_z_residual=zshape(eps,zz),zero_enthalpy_residual=enthalpy(eps,ee))


def run(cpu_seconds=180):
    start=time.process_time();rows=[]
    with mp.workdps(40):
        for eps in EPS:
            for y in Y:
                if time.process_time()-start>cpu_seconds:raise TimeoutError('bounded CPU allowance exhausted')
                try:
                    row=model.evaluate(eps,y)
                    rows.append(dict(eps=eps,y=y,admissible=True,
                        **{key:row[key] for key in PRINCIPAL_KEYS},
                        z=row['state']['z'],c=row['state']['c'],
                        strict_EF=row['strict_EF_scalar_cone'],
                        EF_metric_error=row['EF_metric_error'],EF_current_error=row['EF_current_error']))
                except ValueError as exc:
                    rows.append(dict(eps=eps,y=y,admissible=False,reason=str(exc)))
    with mp.workdps(65):
        # A new positive-kinetic candidate, not the old y=.1 failed point.
        refined=model.evaluate('1e-6','3')
        condition=angular_condition('1e-6','3')
        roots=boundaries()
    return dict(cpu_seconds=time.process_time()-start,cpu_cap=cpu_seconds,
        coefficient_precision=40,refinement_precision=65,rows=rows,
        attempts=len(rows),admissible=sum(row['admissible'] for row in rows),
        healthy=sum(row.get('strict_EF',False) for row in rows),
        refined=refined,refined_angular_condition=condition,boundaries=roots,
        symbolic_principal_scaling_residuals=symbolic_scaling(),symbolic_angular_residual=symbolic_angular_identity(),
        scope='24 predetermined geometry regimes, no normalization scan; zero healthy samples is not a complete-domain exclusion. Exact normalization invariance and angular criterion are conditional analytic results.')


serial=model.serial
if __name__=='__main__':print(json.dumps(serial(run()),indent=2))
