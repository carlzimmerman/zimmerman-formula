#!/usr/bin/env python3
"""Independent exact response controls; no source-density or action fit."""
import json
import sympy as S
from derive_boosted import derive


def main():
    result=derive()
    # Independent direct inversion of the raw two-field Fourier matrix.
    p,r,W,d,q,s,k,omega,J=S.symbols('p r W d q s k omega J',nonzero=True)
    A=2*p+4*q*q*r
    C=(2*q*q*d-W)/s
    raw=S.Matrix([[A*omega**2+(-2*p+2*s*d)*k*k,-2*q*d*k*k],[-2*q*d*k*k,C*k*k]])
    solution=raw.inv()*S.Matrix([J,0])
    Geff=2*p-2*s*d*W/(W-2*q*q*d)
    assert S.factor(solution[0]-J/(A*omega**2-Geff*k*k))==0
    assert S.factor(solution[1]-2*q*d*solution[0]/C)==0
    # k=0 is directly evaluated before inversion: clock row identically zero.
    assert raw.subs(k,0)==S.diag(A*omega**2,0)
    # Exact positive-sound cone fixture, only an algebra control (not model jets).
    K=S.Rational(3);G=S.Rational(3,10000);w=S.Rational(1,10)
    mu=S.Rational(1,10)
    assert G-K*w*w*mu*mu==0
    # Covariant boost of scalar gradient and normal gives nonzero perturbation
    # projection even though the aligned background has exactly Y=0.
    eta=S.diag(-1,1);b=1/S.sqrt(1-w*w)
    n=S.Matrix([b,-b*w]);projector=eta+n*n.T
    v=-q*eta*n
    assert S.simplify((v.T*projector*v)[0])==0
    perturb=S.Matrix([0,1])
    assert S.simplify((perturb.T*projector*perturb)[0]-b*b)==0
    # Dust forcing from explicit components in source rest frame.
    T=S.diag(S.Symbol('rho'),0)
    rho,gam,M=S.symbols('rho gamma M2',nonzero=True)
    n4=S.Matrix([b,-b*w,0,0]);g4=S.diag(-1,1,1,1)
    tm=S.diag(rho,0,0,0);rev=tm-g4*S.trace(g4*tm)/2
    source=2*gam*q*q*(n4.T*rev*n4)[0]/M
    assert S.simplify(source-gam*q*q*rho*(1+w*w)/(M*(1-w*w)))==0
    print(json.dumps({'derivation_checks':len(result['checks']),'independent_controls':['direct_two_field_inverse','zero_k_singular_clock_row','exact_positive_sound_cone','boosted_background_zero_but_perturbation_nonzero','source_rest_dust_trace_reversal'],'all_passed':True},indent=2))


if __name__=='__main__':main()
