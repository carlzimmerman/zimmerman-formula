#!/usr/bin/env python3
"""General invertible derivative-conformal dictionary for vacuum KGB evaluation.

C=2F/m, chi=X/C. Supply real coherent physical metric/clock jets. This helper
does not solve their background equations. Its local EF diagnostics are not a
full physical-frame Hamiltonian, matter, or Dirac certificate.
"""
from functools import lru_cache
import importlib.util
from pathlib import Path
import mpmath as mp
import sympy as s

SOURCE=Path(__file__).resolve().parents[2]/'ticking_kgb_inverse_2026/kgb_inverse.py'


def action_dictionary(X,C,C1,C2,P,PX,PXX,GX,GXX):
    """C1=dC/dX, C2=d²C/dX²; symbolic or numeric, with C*Dfield != 0.

    d/dchi=C²/Dfield d/dX. No third C jet occurs at fixed physical P/G jets.
    The cubic-term transformation includes its integration-by-parts term.
    """
    D=C-X*C1
    return dict(C=C,Dfield=D,chi=X/C,chi_X=D/C**2,P=P/C**2,
        P1=(PX-2*C1*P/C)/D,
        P2=(C*C*D*PXX+C*(C*X*C2-2*C1*D)*PX+2*(C1*C1*D-C*C*C2)*P)/D**3,
        G1=C*GX/D,
        G2=C*C*((C*GXX+C1*GX)*D+C*X*C2*GX)/D**3)


def background_dictionary(r,A,B,g,BrB,p,pr,X,Xr,C,C1,q=-1,sqrt=mp.sqrt):
    """Physical derivatives: g=A'/2A, BrB=B'/B, pr=p', Xr=X'.

    D below is the areal-coordinate Jacobian, not the field Jacobian Dfield.
    The displayed orthonormal orientation assumes D>0. No X'' or C2 is needed.
    """
    h=C1*Xr/C;D=1+r*h/2;omega=sqrt(C)
    H00=-(g+h/2)*p/(C*B)
    H01=-q*(g+h/2)/(C*sqrt(A*B))
    H11=(pr-(BrB+h)*p/2)/(C*B)
    H22=p*D/(C*B*r)
    return dict(C=C,Dfield=C-X*C1,h=h,D=D,R=omega*r,A=C*A,B=B/D**2,
        g=(g+h/2)/(omega*D),p=p/(omega*D),chi=X/C,
        v=[q/sqrt(C*A),p/sqrt(C*B),0,0],
        H=[[H00,H01,0,0],[H01,H11,0,0],[0,0,H22,0],[0,0,0,H22]])


@lru_cache(None)
def evaluator():
    """Load the original coupled scalar principal and stress, not old-frame jets."""
    spec=importlib.util.spec_from_file_location('general_conformal_original_kgb',SOURCE)
    model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
    a=model.principal_template()
    args=[a['m'],a['G1'],a['G2'],a['P'],a['P1'],a['P2']]
    args+=list(a['v'])+[a['H'][i,j] for i in range(4) for j in range(i,4)]
    return s.lambdify(args,(a['M'],a['T']),'mpmath',cse=True)


def evaluate(m,background,physical_jet,C2):
    """Evaluate transformed KGB M/T; background equations remain caller's gate.

    The field Jacobian may have either sign, but cannot vanish. This real
    timelike positive-areal-orientation chart requires m,A,B,C,r,X,D>0.
    Pass mpmath inputs inside workdps for arbitrary-precision computation.
    """
    X,C,C1=[background[key] for key in ('X','C','C1')]
    if min(m,X,C,background['r'],background['A'],background['B'])<=0:
        raise ValueError('outside positive timelike metric chart')
    if C-X*C1==0:
        raise ValueError('singular derivative-conformal field map')
    if 1+background['r']*C1*background['Xr']/(2*C)<=0:
        raise ValueError('outside positive areal-coordinate orientation')
    bg=background_dictionary(**background)
    a=action_dictionary(X,C,C1,C2,**physical_jet)
    q=background.get('q',-1)
    norm=(q*q/background['A']-background['p']**2/background['B'])/2
    norm_prime=(-q*q*background['g']/background['A']
        -background['p']*background['pr']/background['B']
        +background['p']**2*background['BrB']/(2*background['B']))
    principal,stress=evaluator()(m,a['G1'],a['G2'],a['P'],a['P1'],a['P2'],
        *bg['v'],*[bg['H'][i][j] for i in range(4) for j in range(i,4)])
    K,cross,radial,angular=principal[0,0],principal[0,1],principal[1,1],principal[2,2]
    points=[mp.mpf(0),mp.mpf(1)]
    if radial>angular:
        t=abs(cross)/(radial-angular)
        if 0<t<1:points.append(t)
    margin=min(K+angular-2*abs(cross)*t+(radial-angular)*t*t for t in points)
    bounded=bool(K>0 and radial<0 and angular<0)
    return dict(action=a,background=bg,principal=principal,stress=stress,
        kinetic=K,cross=cross,radial=radial,angular=angular,
        radial_discriminant=cross*cross-K*radial,light_margin=margin,
        relative_clock_norm_error=abs(norm-X)/abs(X),
        relative_clock_derivative_error=abs(norm_prime-background['Xr'])/max(
            abs(norm_prime),abs(background['Xr']),mp.mpf('1e-100')),
        bounded_EF_static_quadratic_energy=bounded,
        strict_EF_scalar_cone=bool(bounded and K>abs(cross) and margin>0),
        scope='Local vacuum EF reduced-principal diagnostic; requires on-shell background and regular constrained-mode equivalence, not a full physical-frame certificate')


def serial(value):
    if isinstance(value,dict):return {key:serial(item) for key,item in value.items()}
    if isinstance(value,(list,tuple)):return [serial(item) for item in value]
    if isinstance(value,mp.matrix):return [[serial(value[i,j]) for j in range(value.cols)] for i in range(value.rows)]
    if isinstance(value,(bool,int,str)):return value
    if isinstance(value,s.Basic):return str(value)
    return mp.nstr(value,50)
