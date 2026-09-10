#!/usr/bin/env python3
"""Same-action static inverse with arbitrary spherical B(r),g(r), including pr.

The first-jet inverse needs r,B,Br,g,gr only. Curvatures need their next
derivatives. No empirical fit or general matter/Dirac certificate is returned.
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


ef=_load('pressure_freedom_general_ef',CLOSURE/'kgb_nonaffine_clock_2026/dictionary/general_ef.py')
closed=_load('pressure_freedom_old_closed',CLOSURE/'kgb_universal_clock_2026/structure/closed_inverse.py')


def metric_invariants(r,B,Br,g,gr):
    """Geometric Einstein rho,pr,pt and differentiated pr; m=1 convention."""
    rho=(1-1/B)/r**2+Br/(B*B*r)
    pr=(1/B-1)/r**2+2*g/(B*r)
    pt=(gr+g*g-g*Br/(2*B)+(g-Br/(2*B))/r)/B
    prr=-Br/(B*B*r*r)-2*(1/B-1)/r**3+2*gr/(B*r)-2*g*Br/(B*B*r)-2*g/(B*r*r)
    return dict(r=r,B=B,Br=Br,g=g,gr=gr,rho=rho,pr=pr,pt=pt,prr=prr,
        Ricci=rho-pr-2*pt)


def geometry(eps,y,eta=0):
    """One common eta, B=B0*(1+eta*(r*y)^2), g=y*B; no halo a0 retuning."""
    eps,y,eta=map(mp.mpf,(eps,y,eta))
    mu=-mp.expm1(-y);lam=mu+y*mp.exp(-y)
    r=eps/mp.sqrt(y*mu);ry=-r*lam/(2*y*mu);yr=1/ry
    t=r*y;tr=y+r*yr;B0=1/(1-2*t);B0r=2*tr*B0*B0
    correction=eta*t*t;B=B0*(1+correction)
    Br=B0r*(1+correction)+B0*2*eta*t*tr
    g=y*B;gr=yr*B+y*Br
    return dict(**metric_invariants(r,B,Br,g,gr),eps=eps,y=y,eta=eta,ry=ry,
        B0=B0,fractional_B_correction=correction)


def linear_system(a,X,U,z,F,f,j,sqrt=mp.sqrt):
    """The physical (zr,PX,GX) system, with unprojected total radial P derivative."""
    r,B,Br,g,gr,rho,pr,pt,prr=(a[k] for k in ('r','B','Br','g','gr','rho','pr','pt','prr'))
    K=3*f*f/(2*F);Kx=3*f*j/F-3*f**3/(2*F*F)
    aa=g+2/r;b=Br/(2*B);p=sqrt(B*U);Q=2*X+U
    N=2*f*z*aa+K*z*z;P=2*F*pr+N/B
    Pz=(2*f*aa+2*K*z)/B
    R0=2*f*z*pr+2*F*prr+(2*j*z*z*aa+Kx*z**3+2*f*z*(gr-2/r**2))/B-N*Br/B**2
    Cj=2*(U/r-X*g)/p
    Achi=f*(rho-pr-2*pt)-Kx*z*z/B-2*K*(g-b+2/r)*z/B
    Lbase=2*F*rho+P-2*f*(2/r-b)*z/B+(K-2*j)*z*z/B
    matrix=[[Pz,-z,0],[-2*K/B,1,-Cj],[2*f/B,0,2*X*z/p]]
    rhs=[-R0,-Achi,Lbase]
    return dict(matrix=matrix,rhs=rhs,P=P,Pz=Pz,R0=R0,Achi=Achi,K=K,Kx=Kx,Cj=Cj,p=p,Q=Q)


def coefficients(a,X,U,z,F,f,j=0):
    X,U,z,F,f,j=map(mp.mpf,(X,U,z,F,f,j))
    if min(X,U,F,a['r'],a['B'])<=0 or f==0 or z==0:
        raise ValueError('outside regular positive timelike inverse chart')
    system=linear_system(a,X,U,z,F,f,j)
    matrix=mp.matrix(system['matrix']);rhs=mp.matrix(system['rhs'])
    determinant=mp.det(matrix)
    if determinant==0:raise ValueError('singular actual inverse matrix')
    zr,px,gx=mp.lu_solve(matrix,rhs)
    return dict(**a,**{k:v for k,v in system.items() if k not in ('matrix','rhs')},
        matrix=matrix,rhs=rhs,inverse_determinant=determinant,
        X=X,U=U,z=z,F=F,f=f,j=j,zr=zr,PX=px,GX=gx,
        Echi=system['Achi']-2*system['K']*zr/a['B'],
        Dfield=2*(F-X*f),Dcoord=1+a['r']*f*z/(2*F))


def normalized(a,X,U,w,F):
    """Same inverse in (W=w',kappa=PX/f,Gamma=GX/f), independent of f,j."""
    X,U,w,F=map(mp.mpf,(X,U,w,F))
    if min(X,U,F,a['r'],a['B'])<=0 or w==0:
        raise ValueError('outside regular normalized inverse chart')
    r,B,Br,g,gr,rho,pr,pt,prr=(a[k] for k in ('r','B','Br','g','gr','rho','pr','pt','prr'))
    aa=g+2/r;b=Br/(2*B);p=mp.sqrt(B*U);Q=2*X+U
    N=2*w*aa+3*w*w/(2*F);P=2*F*pr+N/B
    Pw=(2*aa+3*w/F)/B;PF=2*pr-3*w*w/(2*F*F*B)
    Pr=2*F*prr+2*w*(gr-2/r**2)/B-N*Br/B**2
    Cj=2*(U/r-X*g)/p
    matrix=mp.matrix([[Pw,-w,0],[-3/(F*B),1,-Cj],[2/B,0,2*X*w/p]])
    rhs=mp.matrix([-(Pr+w*PF),-(rho-pr-2*pt)-3*w*w/(2*F*F*B)+3*(g-b+2/r)*w/(F*B),
        2*F*rho+P-2*(2/r-b)*w/B+3*w*w/(2*F*B)])
    determinant=mp.det(matrix)
    if determinant==0:raise ValueError('singular actual normalized inverse matrix')
    W,kappa,gamma=mp.lu_solve(matrix,rhs)
    return {**a,**dict(X=X,U=U,w=w,F=F,P=P,p=p,Q=Q,W=W,kappa=kappa,gamma=gamma,
        matrix=matrix,rhs=rhs,inverse_determinant=determinant,Dcoord=1+r*w/(2*F))}


def state(eps,y,eta,X,U,z,j=0,F0='.525',f0='.05',X0='.5'):
    X,j,F0,f0,X0=map(mp.mpf,(X,j,F0,f0,X0));dx=X-X0
    F=F0+f0*dx+j*dx*dx/2;f=f0+j*dx
    return coefficients(geometry(eps,y,eta),X,U,z,F,f,j)


def control(eps,y,eta=0,j=0):
    a=geometry(eps,y,eta);X=mp.mpf('.5');U=mp.mpf('.25')*X*a['r']*a['g']
    return state(eps,y,eta,X,U,-mp.mpf('1.5')*a['g'],j)


def curvatures(a):
    """Fixed local quadratic F: real total derivatives, not independent PXX/GXX."""
    point=[a[k] for k in ('y','X','U','z')]
    direction=[1/a['ry'],a['z'],-2*a['g']*(2*a['X']+a['U'])-2*a['z'],a['zr']]
    # Center the quadratic at this point with exactly the supplied F,f,j.
    def moved(t,key):
        values=[x+t*v for x,v in zip(point,direction)]
        return state(a['eps'],values[0],a['eta'],*values[1:],a['j'],
            F0=a['F'],f0=a['f'],X0=a['X'])[key]
    return tuple(mp.diff(lambda t:moved(t,key),0)/a['z'] for key in ('PX','GX'))


def physical_residuals(a):
    r,B,Br,g,X,U,z,zr,F,f,j,K,P,px,gx=(a[k] for k in ('r','B','Br','g','X','U','z','zr','F','f','j','K','P','PX','GX'))
    p=mp.sqrt(B*U);Q=2*X+U;Ur=-2*g*Q-2*z;pp=p*(Br/B+Ur/U)/2
    box=(pp+(g-Br/(2*B)+2/r)*p)/B
    current=[px*p/B,-gx*box*p/B,-gx*z/B,p*a['Echi']/B]
    boxF=(f*(zr+(g-Br/(2*B)+2/r)*z)+j*z*z)/B
    rho=(2*(f*(zr+(2/r-Br/(2*B))*z)+j*z*z)/B-K*z*z/B+2*X*gx*z/p-P)/(2*F)
    pr=(P-2*(g+2/r)*f*z/B-K*z*z/B)/(2*F)
    pt=(P+gx*p*z/B-2*(boxF-f*z/(B*r))+K*z*z/B)/(2*F)
    scale=max(abs(a['rho']),abs(a['pr']),abs(a['pt']),abs(P),1)
    return dict(physical_Einstein_error=max(abs(rho-a['rho']),abs(pr-a['pr']),abs(pt-a['pt']))/scale,
        physical_current_error=abs(sum(current))/max(sum(abs(v) for v in current),1))


def inspect_control(eps,y,eta=0,j=0):
    a=control(eps,y,eta,j);pxx,gxx=curvatures(a)
    r,B,Br,g,X,U,z,zr,F,f,j=(a[k] for k in ('r','B','Br','g','X','U','z','zr','F','f','j'))
    p=mp.sqrt(B*U);Q=2*X+U;Ur=-2*g*Q-2*z;pp=p*(Br/B+Ur/U)/2
    bg=dict(r=r,A=1/Q,B=B,g=g,BrB=Br/B,p=p,pr=pp,X=X,Xr=z,C=2*F,C1=2*f,q=-mp.mpf(1))
    jet=dict(P=a['P'],PX=a['PX'],GX=a['GX'],PXX=pxx,GXX=gxx)
    out=ef.evaluate(mp.mpf(1),bg,jet,2*j)
    C,h,D,R,Bt,gt,pt=(out['background'][key] for key in ('C','h','D','R','B','g','p'))
    hp=(f*zr+j*z*z)/F-f*f*z*z/F**2;Dp=h/2+r*hp/2
    BrBt=(Br/B-2*Dp/D)/(mp.sqrt(C)*D)
    gRt=(a['gr']+hp/2-(g+h/2)*(h/2+Dp/D))/(C*D*D)
    ge=metric_invariants(R,Bt,Bt*BrBt,gt,gRt)
    stress=out['stress'];scale=max(abs(ge['rho']),abs(ge['pr']),abs(ge['pt']),1)
    error=max(abs(stress[0,0]-ge['rho']),abs(stress[1,1]-ge['pr']),abs(stress[2,2]-ge['pt']),abs(stress[0,1]))/scale
    Hess=out['background']['H'];box=-Hess[0][0]+sum(Hess[i][i] for i in (1,2,3))
    chiR=(C-2*X*f)*z/(C**mp.mpf('2.5')*D)
    current=[out['action']['P1']*pt/Bt,-out['action']['G1']*box*pt/Bt,-out['action']['G1']*chiR/Bt]
    point=[a[k] for k in ('y','X','U','z')];direction=[1/a['ry'],z,Ur,zr]
    dP=mp.diff(lambda t:state(a['eps'],point[0]+t*direction[0],a['eta'],
        *[point[i]+t*direction[i] for i in range(1,4)],j,F0=F,f0=f,X0=X)['P'],0)
    return dict(state={key:a[key] for key in ('eps','y','eta','X','U','z','zr','F','f','j','P','PX','GX','pr','prr','Dfield','Dcoord')},
        **physical_residuals(a),EF_Einstein_error=error,
        EF_current_error=abs(sum(current))/max(sum(abs(v) for v in current),1),
        constitutive_P_error=abs(dP-a['PX']*z)/max(abs(dP),abs(a['PX']*z),1),
        inverse_determinant=a['inverse_determinant'],
        determinant_error=abs(a['inverse_determinant']/(4*f*z*Q/(B*p*r))-1),PXX=pxx,GXX=gxx,
        **{key:out[key] for key in ('kinetic','cross','radial','angular','light_margin','bounded_EF_static_quadratic_energy','strict_EF_scalar_cone')})


@lru_cache(None)
def symbolic_checks():
    r,B,Br,g,gr,rho,pr,pt,prr,X,U,z,F,f,j=s.symbols('r B Br g gr rho pr pt prr X U z F f j',nonzero=True)
    a=dict(r=r,B=B,Br=Br,g=g,gr=gr,rho=rho,pr=pr,pt=pt,prr=prr)
    d=linear_system(a,X,U,z,F,f,j,sqrt=s.sqrt);M=s.Matrix(d['matrix']);rhs=s.Matrix(d['rhs'])
    P=d['P'];Pdirect=sum(s.diff(P,x)*v for x,v in [(r,1),(B,Br),(g,gr),(pr,prr),(X,z),(F,f*z),(f,j*z)])
    # z' is kept separate from the explicit derivative.
    pressure=[s.factor(Pdirect-d['R0']),s.factor(s.diff(P,z)-d['Pz'])]
    determinant=s.factor(M.det())
    det_res=[s.factor(determinant-4*f*z*(2*X+U)/(B*s.sqrt(B*U)*r))]
    zr,px,gx=s.symbols('zr px gx');unknown=s.Matrix([zr,px,gx]);residual=M*unknown-rhs
    angular=P+gx*s.sqrt(B*U)*z/B-2*f*(zr+(g-Br/(2*B)+1/r)*z)/B+(d['K']-2*j)*z*z/B-2*F*pt
    row=s.Matrix([s.diff(angular,v) for v in (zr,px,gx)])
    weights=M.T.inv()*row
    remainder=s.factor(angular-(weights.T*residual)[0])
    inv=metric_invariants(r,B,Br,g,gr)
    angular_res=[s.factor(remainder.subs({rho:inv['rho'],pr:inv['pr'],pt:inv['pt'],prr:inv['prr']}))]
    shift=s.Matrix([-z*z/f,0,0]);j_res=list((M*shift-rhs.diff(j)).applyfunc(s.factor))
    metric_res=[s.factor(inv['prr']+g*(inv['rho']+inv['pr'])-2*(inv['pt']-inv['pr'])/r)]
    return dict(pressure_derivative=pressure,determinant=str(determinant),determinant_residual=det_res,
        angular_residual=angular_res,angular_remainder=str(remainder),j_shift_residual=j_res,metric_identity=metric_res)


def serial(value):
    if value is None or isinstance(value,(str,bool,int)):return value
    if isinstance(value,dict):return {key:serial(item) for key,item in value.items()}
    if isinstance(value,(list,tuple,mp.matrix)):return [serial(item) for item in value]
    if isinstance(value,s.Basic):return str(value)
    return mp.nstr(value,45)


def run(dps=65):
    with mp.workdps(dps):
        rows=[inspect_control(eps,'.1',eta,'-3000') for eps in ('1e-6','2e-6') for eta in ('-2','0','3')]
        return dict(dps=dps,symbolic=symbolic_checks(),controls=rows,
            scope='Six same-action local inverse/EF checks with common-eta metric controls; no common-mass action match, CMB fit or full physical-frame health certificate.')


if __name__=='__main__':print(json.dumps(serial(run()),indent=2))
