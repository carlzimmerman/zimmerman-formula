#!/usr/bin/env python3
"""Exact conformal dictionary for the new degenerate action candidate.

It supplies independent radial checks and a NEW common-function compatibility
condition, not a full Dirac, PPN, or stability certificate.
"""
import json
import sympy as s


def derive():
    r,g,h,B,C,F,m,P,X,CX,GX=s.symbols('r g h B C F m P X CX GX',nonzero=True)
    D=1+r*h/2
    # C=2F/m, R=sqrt(C)r, Btilde=B/D², gtilde=(g+h/2)/(sqrt(C)D).
    # Use the rational equivalent of the independently checked EF radial equation.
    ptilde=m/(C*r*r)*((D*D+2*r*(g+h/2)*D)/B-1)
    radial=s.factor(C*C*ptilde)
    desired_B=(1+2*r*g+r*r*(g+2/r)*h+s.Rational(3,4)*r*r*h*h)/(1+r*r*P/(2*F))
    solved_B=s.solve(s.Eq(P,radial),B)[0].subs(C,2*F/m)
    no_slip_pressure=s.factor(s.solve(s.Eq(desired_B,1+2*r*g),P)[0])
    # chi=X/C(X); the inverse map must be nonsingular, not merely C>0.
    chi_X=(C-X*CX)/C**2
    mapped_G_chi=GX/(C*chi_X)
    sigma=s.Symbol('sigma',positive=True)
    linearC=1+sigma*X
    linear_map=s.factor((C-X*CX).subs({C:linearC,CX:sigma}))
    chi=s.Symbol('chi',positive=True)
    inverseX=chi/(1-sigma*chi)
    e=s.Symbol('e')
    perturbation=s.diff(desired_B.subs({g:e*g,h:e*h,P:e*P}),e).subs(e,0)
    psi_prime=s.factor(perturbation/(2*r))
    omega_prime=s.Symbol('omega_prime')
    gt,rt,pt=s.symbols('gt rt pt')
    physical_phi=gt-omega_prime
    physical_psi=gt-rt*pt/(2*m)+omega_prime
    omega_required=s.solve(s.Eq(physical_phi,physical_psi),omega_prime)[0]
    return dict(B=desired_B,radial_variation_bridge_residual=s.factor(solved_B-desired_B),
        exact_B_equals_T_pressure=no_slip_pressure,
        weak_Phi_prime=g,weak_Psi_prime=psi_prime,
        weak_no_slip_pressure=s.solve(s.Eq(psi_prime,g),P)[0],
        conformal_scalar_map_derivative=chi_X,
        mapped_G_chi=s.factor(mapped_G_chi),
        G_derivative_bridge=s.factor(mapped_G_chi-GX*C/(C-X*CX)),
        linear_C_invertibility_numerator=linear_map,
        linear_inverse_residual=s.factor(inverseX/(1+sigma*inverseX)-chi),
        linear_extra_operator_coefficient=3*m*sigma**2/(4*linearC),
        EF_no_slip_omega_prime=omega_required,
        EF_Weyl_residual=s.factor((physical_phi+physical_psi)/2-(gt-rt*pt/(4*m))),
        qualifications='C>0, C-X*C_X !=0; radial R map D!=0; weak-field slope is not gamma_PPN')


def universal_condition():
    m,P,L,r1,r2,z1,z2=s.symbols('m P L r1 r2 z1 z2',nonzero=True)
    # L=d log(Ctilde)/dchi is ONE common function, zi=dchi/dRi.
    equations=[s.Eq(L*z1,r1*P/(2*m)),s.Eq(L*z2,r2*P/(2*m))]
    solved=s.solve(equations,(z1,z2))
    residual=s.factor((z1/r1-z2/r2).subs(solved))
    return dict(shared_clock_radial_ratio=P/(2*m*L),residual=residual,
                zero_pressure_case='If Ptilde=0 and L!=0, no-slip forces chi_prime=0; nonzero-gradient old seeds cannot be copied unchanged.',
                constant_conformal_case='If L=0 and r,m!=0, no-slip requires Ptilde=0 at this order; division by L is not allowed.')


def main():
    for name,value in [('DICTIONARY',derive()),('UNIVERSAL',universal_condition())]:
        print(name+'='+json.dumps({k:str(v) for k,v in value.items()},indent=2))
    return 0


if __name__=='__main__':raise SystemExit(main())
