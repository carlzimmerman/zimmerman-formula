#!/usr/bin/env python3
"""Construct an all-Q,Y Hamiltonian-bracket repair, preserving the FLRW two-jet.

F=P(X_chi,tau)+sqrt(X_tau)*W(Y,tau)-V(tau), with X_chi=Q^2-Y.
W=U+dY-bY^2/4 and P=aX+bX^2/4+k0. Coefficients reconstruct the
previous background values K=0, KQ=A, KQQ=B, C=C_target at Q=q.
This does not prove global constraint invertibility or full nonlinear stability.
"""
import argparse
import json
from pathlib import Path
import sympy as s
import mpmath as mp


def derive():
    Q,Y,q,A,B,U=s.symbols('Q Y q A B U',positive=True)
    ctarget=A**2/(2*(q*A+U))
    b=(B-A/q)/(2*q**2); a=(3*A/q-B)/4
    d=A/(2*q)-ctarget; c=ctarget-(B-A/q)/4
    k0=-a*q*q-b*q**4/4
    K=a*Q**2+b*Q**4/4+k0
    C=c+b*Q**2/2
    D=d*Y-b*Y**2/4
    P=a*(Q**2-Y)+b*(Q**2-Y)**2/4+k0
    assert all(s.factor(x)==0 for x in [K.subs(Q,q),s.diff(K,Q).subs(Q,q)-A,
               s.diff(K,Q,2).subs(Q,q)-B,C.subs(Q,q)-ctarget,K-C*Y-D-P])
    # Exact, not just at Q=q: the Hamiltonian scalar density is Lorentz invariant.
    defect=s.factor(-2*Q*s.diff(P,Y)-s.diff(P,Q))
    assert defect==0
    # Full local derivative expansion of the repaired COVARIANT action.
    ep,pt,px,st,sx,g,v,pa,sa=s.symbols('ep pt px st sx g v pa sa',real=True)
    aa,bb,dd=s.symbols('aP bP dW',real=True)
    norm=s.sqrt((1+ep*pt)**2-ep**2*px**2)
    qe=((1+ep*pt)*(Q+ep*st)-ep*px*(g+ep*sx))/norm
    ye=-(Q+ep*st)**2+(g+ep*sx)**2+qe**2
    X=(Q+ep*st)**2-(g+ep*sx)**2
    density=aa*X+bb*X**2/4+norm*(U+dd*ye-bb*ye**2/4)
    l2=s.expand(s.diff(density,ep,2).subs(ep,0)/2)
    symbol=s.hessian(l2.subs({pt:-v*pa,px:pa,st:-v*sa,sx:sa}),(pa,sa))
    determinant=s.factor(symbol.det())
    assert s.Poly(determinant,v).coeff_monomial(v**3)==0
    assert s.diff(symbol[0,0],v)==0 and s.diff(symbol[0,1],v)==0
    reduced=s.factor(symbol[1,1]-symbol[0,1]**2/symbol[0,0])
    # Homogeneous derivative two-jet equals the old K-CY plus U norm action.
    old=U*norm+A*(qe-Q)+B*(qe-Q)**2/2-ctarget*ye
    old2=s.expand(s.diff(old,ep,2).subs({ep:0,g:0,Q:q})/2)
    assert s.factor(l2.subs({aa:a,bb:b,dd:d,g:0,Q:q})-old2)==0
    # Sample epochs and longitudinal inhomogeneous events, not a CMB/data fit.
    numeric=s.lambdify((Q,U,aa,bb,dd,g),[symbol[0,0],s.Poly(reduced,v).all_coeffs()],'mpmath',cse=True)
    mp.mp.dps=70
    rows=[]
    for shape in (29,7):
        for j in range(37):
            av=mp.power(10,-6+mp.mpf(j)/4);mass=mp.mpf('0.1')*av**2;qb=1/(1+mass);Ab=mp.mpf('0.1')/av**3
            om=1/(1+7*av**3);vv=(1+28*av**3)/(1+(28+shape)*av**3)
            eb=qb*mass/(1+mass)*(mp.mpf('1.5')*om-2);Bb=-3*Ab*vv/eb;Ub=mass*qb*Ab
            bp=(Bb-Ab/qb)/(2*qb**2);ap=(3*Ab/qb-Bb)/4;dw=Ab/(2*qb)-Ab*Ab/(2*(qb*Ab+Ub))
            for ratio in (mp.mpf('0.001'),mp.mpf('0.01'),mp.mpf('0.1')):
                clock,co=numeric(qb,Ub,ap,bp,dw,ratio*qb)
                kin,lin,const=co;disc=lin*lin-4*kin*const
                roots=[(-lin-mp.sqrt(disc))/(2*kin),(-lin+mp.sqrt(disc))/(2*kin)] if disc>=0 else None
                rows.append(dict(shape=shape,a=str(av),gradient_over_Q=str(ratio),clock_symbol=str(clock),
                    kinetic=str(kin),discriminant=str(disc),roots=None if roots is None else [str(x) for x in roots],
                    local_longitudinal_gate=bool(clock<0 and kin>0 and roots is not None and max(abs(x) for x in roots)<=1)))
    return dict(coefficients={'aP':str(a),'bP':str(b),'dW':str(d),'k0':str(k0)},
        Hamiltonian_density_identity='K(Q)-C(Q)Y-D(Y)=P(Q^2-Y)',exact_bracket_defect=str(defect),
        background_and_quadratic_matching=True,local_quadratic=str(l2),principal_symbol=str(symbol),
        characteristic_degree=s.Poly(determinant,v).degree(),eliminated_clock_symbol=str(reduced),
        samples=rows,summary={str(shape):{'passed':sum(r['local_longitudinal_gate'] for r in rows if r['shape']==shape),
            'total':sum(r['shape']==shape for r in rows)} for shape in (29,7)},precision_digits=mp.mp.dps,
        remaining=['global nonlinear Dirac operator invertibility','transverse/mixed-direction characteristics',
                   'strong coupling and caustics','radiation/baryons','same-action MOND and PPN'],full_theory_status='OPEN')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--result-file',type=Path);a=p.parse_args()
    r=derive();encoded=json.dumps(r,indent=2)+'\n'
    if a.result_file:a.result_file.write_text(encoded)
    print(encoded)
