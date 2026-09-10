#!/usr/bin/env python3
"""Regular zero-braiding inverse: exact discriminator and finite matching gate.

No dark-matter particles, per-halo acceleration scales, or assigned PPN/ranks.
The principal certificate is conditional, local, exterior-vacuum and EF only.
"""
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import mpmath as mp
import sympy as s

HERE=Path(__file__).resolve().parent
CLOSURE=HERE.parents[1]


def _load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


inverse=_load('zero_braiding_closed_inverse',CLOSURE/'kgb_universal_clock_2026/structure/closed_inverse.py')
ef=_load('zero_braiding_general_ef',CLOSURE/'kgb_nonaffine_clock_2026/dictionary/general_ef.py')
original=_load('zero_braiding_original_kgb',CLOSURE/'ticking_kgb_inverse_2026/kgb_inverse.py')


def zero_state(eps,y,X='.5',U='1e-7',F='.525'):
    """Gamma=0 is imposed algebraically, not assumed along the later flow."""
    eps,y,X,U,F=map(mp.mpf,(eps,y,X,U,F))
    a=inverse.geometry(eps,y,backend=mp)
    r,g,B,rho=(a[k] for k in ('r','g','B','rho'))
    if min(F,X,U,r,g,B,rho)<=0 or r*g>=1:
        raise ValueError('outside the regular positive-w galactic chart')
    w=F*(g+2/r)*rho*r*r*B/(2*(1-r*g))
    return inverse.normalized(eps,y,X,U,w,F,backend=mp)


def pressure_pair(y1,second_guess,eps1='1e-6',eps2='2e-6'):
    """One explicitly seeded pressure root, not an all-y root enumeration."""
    first=zero_state(eps1,y1,U='1e-7')
    root=mp.findroot(lambda y:zero_state(eps2,y,U='2e-7')['P']-first['P'],
        mp.mpf(second_guess),tol=mp.mpf(10)**(-mp.mp.dps+10))
    return first,zero_state(eps2,root,U='2e-7')


def flow(a,f,j=0):
    return [f/(a['ry']*a['w']),mp.mpf(1),-2-2*f*a['g']*a['Q']/a['w'],
        f*a['W']/a['w'],f,j]


def normalized_derivatives(a,f):
    point=[a[k] for k in ('y','X','U','w','F')];direction=flow(a,f)[:5]
    return mp.matrix([mp.diff(lambda t:inverse.normalized(a['eps'],
        *[x+t*v for x,v in zip(point,direction)],backend=mp)[key],0)
        for key in ('kappa','gamma')])


def action_jets(a,f,j=0):
    """Actual derivatives along the original inverse, not along S=0 projection."""
    E=normalized_derivatives(a,f)
    return mp.matrix([a['P'],f*a['kappa'],f*a['gamma'],
        j*a['kappa']+f*E[0],j*a['gamma']+f*E[1]])


def next_derivatives(a,f,j=0):
    point=[a[k] for k in ('y','X','U','w','F')]+[f];direction=flow(a,f,j)
    def value(t,index):
        moved=[x+t*v for x,v in zip(point,direction)]
        return normalized_derivatives(inverse.normalized(a['eps'],*moved[:5],backend=mp),moved[5])[index]
    return mp.matrix([mp.diff(lambda t:value(t,index),0) for index in range(2)])


def matching_coefficients(a):
    """GXX/f²=K sqrt(U)/Q; H GXX/f²=t*x+v, x=U/Q."""
    point=[a[k] for k in ('y','X','U','w','F')]
    # D_X S=f*Sbar because S is independent of X,U.
    direction=[1/(a['ry']*a['w']),0,0,a['W']/a['w'],1]
    Sbar=mp.diff(lambda t:inverse.normalized(a['eps'],
        *[x+t*v for x,v in zip(point,direction)],backend=mp)['S'],0)
    K=mp.sqrt(a['B'])*a['r']*Sbar/(2*a['w'])
    aa=2/a['r']+a['w']/a['F'];bb=2*a['g']+a['w']/a['F']
    return K,K*(aa+bb/2)/mp.sqrt(a['B']),-K*bb/(2*mp.sqrt(a['B']))


def solve_matching_coefficients(K1,t1,v1,K2,t2,v2):
    """Finite exact-degree gate. Squaring never removes the original sign test."""
    K1,t1,v1,K2,t2,v2=map(mp.mpf,(K1,t1,v1,K2,t2,v2))
    if K1==0 and K2==0:
        if any(value!=0 for value in (t1,v1,t2,v2)):
            raise ValueError('inconsistent zero-GXX structural coefficients')
        return dict(sector='both_GXX_zero',accepted='all physical U pairs',candidates=[])
    if K1==0 or K2==0:
        return dict(sector='one_GXX_zero',accepted=[],candidates=[])
    if t2==0:
        raise ValueError('exceptional zero t2 outside this regular positive-w chart')
    u=t1/t2;v=(v1-v2)/t2;same=bool(K1*K2>0)
    aa=-K1*K1+K2*K2*u*u
    bb=K1*K1-K2*K2*u*(1-2*v)
    cc=-K2*K2*v*(1-v)
    base=dict(K1=K1,K2=K2,u=u,v=v,polynomial=[aa,bb,cc],same_K_sign=same)
    if aa==0 and bb==0:
        if cc!=0:return dict(**base,sector='constant_nonzero',accepted=[],candidates=[])
        lo,hi=mp.mpf(0),mp.mpf(1)
        if u==0:
            if not 0<v<1:hi=lo
        else:
            left,right=sorted([-v/u,(1-v)/u]);lo=max(lo,left);hi=min(hi,right)
        return dict(**base,sector='identity_polynomial',accepted=('continuous physical intersection'
            if same and lo<hi else []),open_x1_interval=[lo,hi],candidates=[])
    roots=[-cc/bb] if aa==0 else [(-bb+sign*mp.sqrt(bb*bb-4*aa*cc))/(2*aa) for sign in (-1,1)]
    candidates=[];accepted=[]
    for x1 in roots:
        x2=u*x1+v
        physical=bool(mp.im(x1)==0 and mp.im(x2)==0 and 0<mp.re(x1)<1 and 0<mp.re(x2)<1)
        error=None
        if physical:
            left=K1*mp.sqrt(x1*(1-x1));right=K2*mp.sqrt(x2*(1-x2))
            error=abs(left-right)/max(abs(left),abs(right),1)
        passes=bool(physical and same and error<mp.mpf(10)**(-mp.mp.dps//2))
        row=dict(x1=x1,x2=x2,physical=physical,unsquared_relative_error=error,accepted=passes)
        candidates.append(row)
        if passes:accepted.append(row)
    return dict(**base,sector='linear' if aa==0 else 'quadratic',candidates=candidates,accepted=accepted)


def curvature_matches(first,second):
    if any(first[k]!=second[k] for k in ('F','X')):
        raise ValueError('matching requires the same F and X')
    if abs(first['P']-second['P'])/max(abs(first['P']),1)>mp.mpf(10)**(-mp.mp.dps//2):
        raise ValueError('pressure must already match')
    return solve_matching_coefficients(*matching_coefficients(first),*matching_coefficients(second))


@lru_cache(None)
def symbolic_principal_check():
    """Differentiate/use original coupled EL, then impose explicit hypotheses."""
    a=original.principal_template();v0,v1,v2,v3=a['v']
    H00,H11,H22=(a['H'][i,i] for i in (0,1,2))
    subs={a['P1']:0,a['G1']:0,v2:0,v3:0,a['H'][0,1]:H00*v0/v1,
        a['H'][0,2]:0,a['H'][0,3]:0,a['H'][1,2]:0,a['H'][1,3]:0,
        a['H'][2,3]:0,a['H'][3,3]:H22}
    scalar=s.factor(a['E'].subs(subs));M=a['M'].subs(subs)
    P2=a['G2']*(H00*(v0*v0-v1*v1)/v1**2+2*H22)
    angular=a['G2']*(H00*v0*v0-H11*v1*v1)
    expected=s.diag((v0*v0-v1*v1)*angular/v1**2,0,angular,angular)
    residuals=list((M.subs(a['P2'],P2)-expected).applyfunc(s.factor))
    F,f,j,P,GXX,H,X=s.symbols('F f j P GXX H X',nonzero=True)
    mapped=ef.action_dictionary(X,2*F,2*f,2*j,P,2*f*P/F,
        2*P*j/F+2*P*f*f/F**2+H*GXX,0,GXX)
    return dict(matrix_residuals=residuals,scalar_factorization=str(scalar),
        scalar_residual=s.factor(scalar.subs(a['P2'],P2)),
        EF_ratio_residual=s.factor(mapped['P2']-H*mapped['G2']/(2*F)),
        matrix=str(expected),on_shell_P2=str(P2))


def evaluate(a,f,j):
    """Original EF scalar/stress with independent geometry and scalar residuals."""
    f,j=mp.mpf(f),mp.mpf(j)
    if f==0:raise ValueError('the regular w=f*Xr chart requires f!=0')
    z=a['w']/f;U,B,p,X=(a[k] for k in ('U','B','p','X'))
    Ur=-2*a['g']*a['Q']-2*z
    bg=dict(r=a['r'],A=1/a['Q'],B=B,g=a['g'],BrB=a['Br']/B,p=p,
        pr=p*(a['Br']/B+Ur/U)/2,X=X,Xr=z,C=2*a['F'],C1=2*f,q=-mp.mpf(1))
    jet=dict(zip(('P','PX','GX','PXX','GXX'),action_jets(a,f,j)))
    point=[a[k] for k in ('y','X','U','w','F')];direction=flow(a,f)[:5]
    derivative_P=mp.diff(lambda t:inverse.normalized(a['eps'],
        *[x+t*v for x,v in zip(point,direction)],backend=mp)['P'],0)
    out=ef.evaluate(mp.mpf(1),bg,jet,2*j)
    C,h,D,R,Bt,gt,pt=(out['background'][key] for key in ('C','h','D','R','B','g','p'))
    hp=a['W']/a['F']-a['w']**2/a['F']**2;Dp=h/2+a['r']*hp/2
    BrBt=(a['Br']/B-2*Dp/D)/(mp.sqrt(C)*D)
    gRt=(a['gr']+hp/2-(a['g']+h/2)*(h/2+Dp/D))/(C*D*D)
    geometry=[(1-1/Bt)/R**2+BrBt/(Bt*R),(1/Bt-1)/R**2+2*gt/(Bt*R),
        (gRt+gt*gt-gt*BrBt/2+(gt-BrBt/2)/R)/Bt]
    stress=out['stress'];scale=max([mp.mpf(1)]+[abs(v) for v in geometry])
    error=max(abs(stress[0,0]-geometry[0]),abs(stress[1,1]-geometry[1]),
        abs(stress[2,2]-geometry[2]),abs(stress[0,1]))/scale
    Hess=out['background']['H'];v0,v1=out['background']['v'][:2]
    box=-Hess[0][0]+sum(Hess[i][i] for i in (1,2,3))
    chiR=(C-2*X*f)*z/(C**mp.mpf('2.5')*D)
    current=[out['action']['P1']*pt/Bt,-out['action']['G1']*box*pt/Bt,-out['action']['G1']*chiR/Bt]
    required=out['action']['G2']*(Hess[0][0]*(v0*v0-v1*v1)/v1**2+2*Hess[2][2])
    scalar_error=abs(out['action']['P2']-required)/max(abs(out['action']['P2']),abs(required),1)
    angular=out['action']['G2']*(Hess[0][0]*v0*v0-Hess[1][1]*v1*v1)
    expected=mp.diag([(v0*v0-v1*v1)*angular/v1**2,0,angular,angular])
    principal_error=max(abs(out['principal'][i,k]-expected[i,k]) for i in range(4) for k in range(4))/max(abs(expected[0,0]),abs(angular),1)
    keep=('kinetic','cross','radial','angular','light_margin','bounded_EF_static_quadratic_energy','strict_EF_scalar_cone')
    return dict(**{key:out[key] for key in keep},Einstein_relative_error=error,
        scalar_relative_error=scalar_error,principal_identity_error=principal_error,
        current_scaled_error=abs(sum(current))/max(sum(abs(v) for v in current),1),
        Dfield=C-2*X*f,Dcoord=D,physical_jets=jet,EF_action=out['action'],
        P_derivative_relative_error=abs(derivative_P-jet['PX'])/max(abs(derivative_P),abs(jet['PX']),1),
        relative_clock_norm_error=out['relative_clock_norm_error'],
        relative_clock_derivative_error=out['relative_clock_derivative_error'])


def serial(value):
    if value is None or isinstance(value,(bool,int,str)):return value
    if isinstance(value,dict):return {key:serial(item) for key,item in value.items()}
    if isinstance(value,(list,tuple,mp.matrix)):return [serial(item) for item in value]
    if isinstance(value,s.Basic):return str(value)
    return mp.nstr(value,50)


def run(dps=80):
    with mp.workdps(dps):
        pairs=[]
        for y1,guess in (('.01','.014'),('.01','16'),('.1','.14'),('.1','10.5'),('1','1.8'),('1','3.8'),('10','.25'),('10','9')):
            rows=pressure_pair(y1,guess)
            pairs.append(dict(y1=y1,y2=rows[1]['y'],P=rows[0]['P'],
                relative_P_error=abs(rows[0]['P']/rows[1]['P']-1),matching=curvature_matches(*rows)))
        controls=[]
        for y in ('.1','10'):
            a=zero_state('1e-6',y,U='1e-7');f=mp.mpf('.05')
            first=evaluate(a,f,0);changed=evaluate(a,f,mp.mpf('1e10'))
            derivative=normalized_derivatives(a,f)
            n0=next_derivatives(a,f,0);n1=next_derivatives(a,f,1)
            controls.append(dict(y=y,w=a['w'],base=first,j1e10=changed,
                next_j_coefficient_error=[abs(n1[i]-n0[i]-derivative[i]/f)/max(abs(derivative[i]/f),1) for i in range(2)]))
        return dict(dps=dps,symbolic=symbolic_principal_check(),pressure_pairs=pairs,
            controls=controls,scope='Eight explicitly seeded pressure pairs and two actual vacuum controls; exact conditional zero-braiding principal obstruction, not a full-theory or observational certificate.')


if __name__=='__main__':print(json.dumps(serial(run()),indent=2))
