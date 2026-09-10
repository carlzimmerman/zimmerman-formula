#!/usr/bin/env python3
"""Exact unitary kinetic calculation, not a full constraint/health analysis."""
from functools import lru_cache
import sympy as s

@lru_cache(None)
def derive():
    F,f,D,v,sv,K,X=s.symbols('F f D v s K X',nonzero=True)
    A4=3*f*f/(2*F)-(F-X*f)*D/F-X*X*D*D/(2*F)
    A5=-(f+X*D)*D/F
    eta=s.diag(-1,1,1,1);a=s.Matrix(s.symbols('a1:4'))
    k11,k22,k33,k12,k13,k23=s.symbols('k11 k22 k33 k12 k13 k23')
    kij=s.Matrix([[k11,k12,k13],[k12,k22,k23],[k13,k23,k33]])
    H=s.zeros(4);H[0,0]=sv
    for i in range(3):
        H[0,i+1]=H[i+1,0]=-v*a[i]
        for j in range(3):H[i+1,j+1]=-v*kij[i,j]
    cov=s.Matrix([v,0,0,0]);con=eta*cov
    box=s.trace(eta*H);pair=(con.T*H*con)[0]
    L3=box*pair;L4=(con.T*H*eta*H*con)[0];L5=pair**2
    a2=(a.T*a)[0];trace=s.trace(kij)
    dX=-H*con
    contraction_residuals=[L3+v*v*sv*sv+v**3*sv*trace,
        L4+v*v*sv*sv-v**4*a2,L5-v**4*sv*sv,L4-(dX.T*eta*dX)[0]]
    ss=(-v*v*(D+A4)+v**4*A5).subs(X,v*v/2)
    T=f+v*v*D/2;lam=3*v*T/(2*F)
    trace_lagrangian=-2*F*K*K/3-(2*f*v+D*v**3)*K*sv+ss*sv*sv
    hessian=s.hessian(trace_lagrangian,(K,sv)).applyfunc(s.factor)
    square=-2*F*(K+lam*sv)**2/3
    null=s.Matrix([-3*v*T,2*F])
    kinetic_residuals=[trace_lagrangian-square,hessian.det(),*(hessian*null),
                      ss+3*v*v*T*T/(2*F)]
    # Canonical density momenta: Kij=(hdotij-Lie_shift hij)/(2N),
    # s=(vdot-Lie_shift v)/N. sqrt(h) is kept explicit.
    volume,G,GX=s.symbols('sqrt_h G GX',nonzero=True)
    full=F*(s.trace(kij*kij)-trace**2)-2*v*T*trace*sv+ss*sv*sv
    shear=kij-s.eye(3)*trace/3
    kinetic_residuals.append(full-F*s.trace(shear*shear)-trace_lagrangian.subs(K,trace))
    pi=volume*sum(s.diff(full,k) for k in (k11,k22,k33))/2
    pv=volume*s.diff(full,sv)
    bare=full+G*(sv+v*trace)
    bare_pi=volume*sum(s.diff(bare,k) for k in (k11,k22,k33))/2
    bare_pv=volume*s.diff(bare,sv)
    integrated=full-GX*v*v*sv
    integrated_pv=volume*s.diff(integrated,sv)
    momentum_residuals=[pv-v*T*pi/F,
        bare_pv-v*T*bare_pi/F-volume*G*(1-3*v*v*T/(2*F)),
        integrated_pv-v*T*pi/F+volume*GX*v*v,
        (bare-integrated)-((G+GX*v*v)*sv+G*v*trace)]
    D_zero_residuals=[A4.subs(D,0)-3*f*f/(2*F),A5.subs(D,0),
        trace_lagrangian.subs(D,0)+2*F*(K+3*v*f*sv/(2*F))**2/3]
    xs,fs=s.symbols('X_source F_source_derivative')
    source_A4=(48*fs**2-8*(F-xs*fs)*D-xs**2*D**2)/(8*F)
    source_A5=(4*fs+xs*D)*D/(2*F)
    translation_residuals=[source_A4.subs({xs:-2*X,fs:-f/2})-A4,
                           source_A5.subs({xs:-2*X,fs:-f/2})-A5]
    aa,ad,add=s.symbols('a adot addot',nonzero=True)
    raw=6*F*(aa*aa*add+aa*ad*ad)
    boundary_derivative=6*(f*v*sv*aa*aa*ad+F*(2*aa*ad*ad+aa*aa*add))
    bulk=-6*F*aa*ad*ad-6*aa*aa*ad*f*v*sv
    ricci_residuals=[raw-boundary_derivative-bulk,
                    bulk-aa**3*(-2*F*(3*ad/aa)**2/3-2*f*v*(3*ad/aa)*sv)]
    return locals()

if __name__=='__main__':
    d=derive()
    print('trace kinetic =',s.factor(d['trace_lagrangian']))
    print('Hessian =',d['hessian'])
    print('null vector =',d['null'])
    print('kinetic canonical pi =',s.factor(d['pi']))
    print('kinetic canonical p_v =',s.factor(d['pv']))
    for name in ('contraction_residuals','kinetic_residuals','momentum_residuals',
                 'D_zero_residuals','translation_residuals','ricci_residuals'):
        values=[s.factor(q) for q in d[name]]
        print(name,values)
        if any(q!=0 for q in values):raise SystemExit(1)
