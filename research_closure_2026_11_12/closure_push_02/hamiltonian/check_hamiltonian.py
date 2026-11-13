"""Exact local Hamiltonian checks for the stated leading Newtonian action.

This establishes a reduced-model calculation, not the full relativistic theory.
The homogeneous self-gravity comparison uses background subtraction explicitly.
"""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    parser=safe_parser()
    args=parser.parse_args()
    checks=[]
    def eq(label,a,b=0):
        residual=s.simplify(a-b)
        checks.append(dict(name=label,passed=residual==0,residual=str(residual)))
        assert residual==0,(label,residual)
    A,w,k,K,n0=s.symbols('A w k K n0',positive=True)
    b,D=s.symbols('b D',real=True)
    c=1+b
    # H_QQ=A, H_QPi=b, H_PiPi-Gamma''=D.
    # e(n,Pi)=(n-Pi)x-H(1+x,Pi)+Gamma(Pi), n=H_Q+Pi.
    enn=1/A
    enp=-c/A
    epp=c*c/A-D
    Hlocal=s.Matrix([[enn,enp],[enp,epp]])
    eq('joint material Hessian determinant',Hlocal.det(),-D/A)
    Ck=epp+w/k**2
    hf=s.factor(enn-enp**2/Ck)
    expected=(w-D*k**2)/(A*w+(c*c-A*D)*k**2)
    eq('polarization-eliminated charge coefficient',hf,expected)
    eq('inverse coefficient agrees with phase Lagrangian',1/hf,A+c*c*k**2/(w-D*k**2))
    eq('fixed-charge curvature is not joint convexity',epp-enp**2/enn,-D)
    eq('full n/Pi determinant including W',s.det(s.Matrix([[enn,enp],[enp,Ck]])),(w/k**2-D)/A)
    hg=hf-K/k**2
    omega2=n0*k*k*hg
    eq('Poisson contribution is ordinary Jeans term',omega2-n0*k*k*hf,-K*n0)
    ungated=s.factor(omega2.subs({b:0,D:0,w:K}))
    eq('ungated density dispersion',ungated,-n0*A*K*K/(A*K+k*k))
    eq('ungated long-wave Jeans limit',s.limit(ungated,k,0),-n0*K)
    eq('ungated short-wave gravitational cancellation',s.limit(ungated,k,s.oo),0)
    eps,dd=s.symbols('eps dd',positive=True)
    phase_kin=A+c*c*k*k/(w-D*k*k)
    pole_limit=s.limit(eps*phase_kin.subs({k:s.sqrt((1+eps)*w/dd),D:dd}),eps,0,dir='+')
    eq('near P-block pole phase coefficient',pole_limit,-c*c/dd)
    # Physical density coordinate has positive kinetic coefficient, even for Jeans growth.
    z,zdot,ph=s.symbols('density density_dot phase',real=True)
    phase_solution=zdot/(n0*k*k)
    Ldensity=ph*zdot-n0*k*k*ph*ph/2-hg*z*z/2
    eq('density-coordinate kinetic is positive',s.diff(Ldensity.subs(ph,phase_solution),zdot,2),1/(n0*k*k))
    # Explicit separable quadratic gate; independently differentiate its Legendre transform.
    N,P,C,pc=s.symbols('N Pi C Pi_c',positive=True)
    gamma=s.symbols('gamma',nonnegative=True)
    for label,S in [('ungated',s.Integer(1)),('exponential',s.exp(-P/pc)),('flat',s.exp(-(P/pc)**3))]:
        x=(N-P)/(2*C*S)
        H=lambda xx: C*xx**2*S
        e=(N-P)**2/(4*C*S)+gamma*P**2/2
        aq=2*C*S
        bq=2*C*x*s.diff(S,P)
        dq=C*x*x*s.diff(S,P,2)-gamma
        eq(label+' Legendre identity',(N-P)*x-H(x)+gamma*P**2/2,e)
        eq(label+' e_n',s.diff(e,N),x)
        eq(label+' e_nn',s.diff(e,N,2),1/aq)
        eq(label+' e_nPi',s.diff(e,N,P),-(1+bq)/aq)
        eq(label+' e_PiPi',s.diff(e,P,2),(1+bq)**2/aq-dq)
        eq(label+' Schur curvature',s.diff(e,P,2)-s.diff(e,N,P)**2/s.diff(e,N,2),-dq)
    result={'scope':'Exact local leading-Newtonian Hamiltonian identities; homogeneous gravity is background-subtracted',
            'passed':len(checks),'checks':checks,
            'formulas':{'charge_hessian':str(Hlocal),'effective_charge_coefficient_no_gravity':str(hf),
                        'density_dispersion_with_gravity':str(omega2),'ungated_dispersion':str(ungated)},
            'non_claims':['No full relativistic constraint proof or on-shell finite-Pi background.',
                          'No formation or mass retention prediction.',
                          'Negative phase kinetic by itself does not distinguish Jeans/gradient instability from a fundamental ghost.']}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':len(checks),'ungated_dispersion':str(ungated)},indent=2))


def safe_parser():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('output',type=Path)
    return p


if __name__=='__main__':
    main()
