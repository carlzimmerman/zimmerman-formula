#!/usr/bin/env python3
"""Coupled shared-scalar vacuum test; no MOND completion or 32pi solution.

S=sqrt(-g)[F R/2-(grad chi)^2/2-U]. Constant chi vacuum equations are
Lambda=U/F and F_prime R/2=U_prime, R=4 Lambda in four dimensions.
An assigned a0=gamma chi is a response dictionary, not a derived force.
Tensor Newton coupling is 1/(8piF); scalar exchange is not scored.
"""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    args=ap.parse_args(); checks=[]; rows=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    chi,xi,lam,A,v,gamma=s.symbols('chi xi lambda A v gamma',positive=True)
    F=xi*chi**2
    U=chi**4*(lam+A*(chi**2/v**2-1)**2)
    curvature=4*U/F
    residual=s.factor(s.diff(F,chi)*curvature/2-s.diff(U,chi))
    check('coupled_metric_scalar_residual',s.simplify(residual+4*A*chi**5*(chi**2-v**2)/v**4)==0,
          str(residual))
    check('vacuum_scalar_value_does_not_fix_lambda',residual.subs(chi,v)==0 and s.diff(residual,lam)==0,
          'chi=v solves full constant-scalar equations for every positive lambda, not just a fixed-metric minimum')
    GT=1/(8*s.pi*F.subs(chi,v)); vacuum=U.subs(chi,v)
    Lambda=s.simplify((U/F).subs(chi,v)); a0=gamma*v
    coefficient=s.simplify(Lambda/a0**2)
    check('vacuum_and_tensor_coupling',s.simplify(Lambda-8*s.pi*GT*vacuum)==0,
          f'G_tensor={GT}; rho_vac={vacuum}; Lambda={Lambda}')
    check('shared_field_coefficient_is_free',coefficient==lam/(xi*gamma**2),str(coefficient))
    check('target_is_extra_coupling_relation',s.solve(s.Eq(coefficient,32*s.pi),lam)==[32*s.pi*xi*gamma**2],
          'lambda=32pi xi gamma² is not imposed by the field equations')
    Z=s.simplify(1/F+s.Rational(3,2)*(s.diff(F,chi)/F)**2)
    VE=s.simplify(U/F**2)
    check('Einstein_scalar_kinetic_sign',Z==(6*xi+1)/(chi**2*xi),
          f'Z={Z}>0 for chi,xi>0; tensor F>0')
    hessian=s.simplify(s.diff(VE,chi,2).subs(chi,v))
    mass=s.simplify(hessian/Z.subs(chi,v))
    check('stabilized_Einstein_vacuum',s.diff(VE,chi).subs(chi,v)==0 and hessian==8*A/(xi**2*v**2),
          f'Einstein potential Hessian={hessian}>0; physical scalar mass factor={mass}')
    check('vacuum_height_does_not_set_mass',s.diff(mass,lam)==0 and s.diff(VE,lam)==1/xi**2,
          'lambda shifts Einstein potential height while its minimum and Hessian stay fixed')
    # Check the conformal kinetic convention against the special-case
    # formula in Galtsov EPJC80(2020)443, Eq (9), metric scalar formulation.
    z=s.symbols('z',real=True)
    special=1-z*chi**2
    generic=1/special+s.Rational(3,2)*(s.diff(special,chi)/special)**2
    published=(1-z*(1-6*z)*chi**2)/special**2
    check('conformal_kinetic_convention_crosscheck',s.simplify(generic-published)==0,
          'special F=1-z chi² matches [1-z(1-6z)chi²]/F² on F>0')
    # Dimension fixes a homogeneous power, not the coupling coefficient.
    d,m,n=s.symbols('d m n',positive=True)
    general_power=s.simplify(d*m/(d-2)-n)
    check('dimension_fixes_power_not_height',general_power.subs({d:4,m:2,n:4})==0,
          'constant-scalar monomials F~chi^m,U~chi^n require n=d*m/(d-2); lambda cancels')
    for target in (16*s.pi,32*s.pi,64*s.pi):
        pars={xi:s.Integer(1),gamma:s.Integer(1),A:s.Integer(1),v:s.Integer(1),lam:target}
        ok=(residual.subs(chi,v).subs(pars)==0 and
            Z.subs(chi,v).subs(pars)>0 and hessian.subs(pars)>0 and Lambda.subs(pars)>0)
        check(f'counterfamily_C={target}',ok,
              'same scalar vacuum, response assignment, tensor coupling and kinetic signs; different positive de Sitter curvature')
        rows.append(dict(coefficient=str(target),coupling_lambda=str(target),scalar_vacuum=1,tensor_G=str(GT.subs(pars)),assigned_a0=1))
    # Euclidean round four-sphere: R=12/L², Vol=8pi²L⁴/3.
    L=s.symbols('L',positive=True)
    SE=-s.Rational(8,3)*s.pi**2*L**4*(F.subs(chi,v)*12/L**2/2-vacuum)
    on_shell=s.simplify(SE.subs(L**2,3/Lambda))
    check('Euclidean_on_shell_action',on_shell==-24*s.pi**2*xi**2/lam,str(on_shell))
    check('regular_period_exists_for_all_positive_lambda',s.simplify((2*s.pi*s.sqrt(3/Lambda))**2-12*s.pi**2/Lambda)==0,
          'beta=2pi sqrt(3/Lambda); no externally fixed beta or relation to a0 supplied')
    check('extra_lambda_extremization_has_no_interior_stationary_point',s.diff(on_shell,lam)==24*s.pi**2*xi**2/lam**2,
          'positive derivative; varying a coupling is not a field equation without an added mechanism')
    # Four equal scalar gradients in a local Lorentz frame. Stress includes
    # the determinant variation, not merely a trace of four components.
    q,K,U0=s.symbols('q K U0',positive=True)
    metric=s.diag(-1,1,1,1)
    def stress(internal):
        C=K*q*q*internal
        kinetic=s.trace(metric*C)
        lag=-kinetic/2-U0
        return s.simplify(C+metric*lag),lag
    positive,lag_positive=stress(s.eye(4))
    lorentz,lag_lorentz=stress(metric)
    check('positive_four_gradients_not_vacuum',positive==s.diag(2*K*q*q+U0,-U0,-U0,-U0),
          'rho=2Kq²+U0, p=-U0: rho+p=2Kq²>0')
    check('Lorentz_internal_gradient_stress_is_vacuum',lorentz==-(K*q*q+U0)*metric,
          'rho=Kq²+U0, not four times Kq²; metric variation subtracts the Lagrangian')
    check('Lorentz_internal_metric_has_ghost',list((K*metric).diagonal())==[-K,K,K,K],
          'time-derivative Hessian is K eta_ab: one negative eigenvalue in four free unconstrained scalars')
    # Independent diagonal-metric differentiation of the matter action.
    lapse,b1,b2,b3=s.symbols('N b1 b2 b3',positive=True)
    cov=s.diag(-lapse*lapse,b1*b1,b2*b2,b3*b3)
    inv=cov.inv(); determinant=lapse*b1*b2*b3
    for label,internal in [('positive',s.eye(4)),('lorentz',metric)]:
        action=determinant*(-K*q*q*s.trace(inv*internal)/2-U0)
        # dS/dN=-volume*rho, dS/db_i=N*other-volume*p_i at unit metric.
        origin={lapse:1,b1:1,b2:1,b3:1}
        rho=-s.diff(action,lapse).subs(origin)
        pressure=s.diff(action,b1).subs(origin)
        T,_=stress(internal)
        check(f'independent_metric_variation_{label}',s.simplify(rho-T[0,0])==0 and s.simplify(pressure-T[1,1])==0,
              f'rho={rho}; p={pressure}')
    data=dict(checks=checks,rows=rows,scalar_equation_residual=str(residual),coefficient=str(coefficient),
              Einstein_kinetic=str(Z),Einstein_Hessian=str(hessian),Euclidean_action=str(on_shell),
              verdict='32pi remains OPEN. Sharing a dynamical scalar with nonminimal gravity and stabilizing its vacuum still leaves the coefficient free; four-component counting does not fix it.',
              non_claims=['No derived MOND response; a0=gamma chi is assigned','Tensor G is not full measured Newton coupling with scalar exchange','Local vacuum signs are not a full galaxy/cosmology health proof','Four-gradient stress is local, not a global de Sitter solution','Euclidean regularity is not a quantum measure or coefficient-selection mechanism'])
    Path(args.output).write_text(json.dumps(data,indent=2)+'\n')
    failed=sum(not c['passed'] for c in checks)
    print(f'{len(checks)-failed}/{len(checks)} scoped checks pass; 32pi OPEN.')
    return int(failed>0)


if __name__=='__main__': raise SystemExit(main())
