#!/usr/bin/env python3
"""Exact/finite constraints on 32pi; no derivation of its physical selection.

Published dipole coefficient: arXiv:2502.14686v2 Eqs 3.26, 3.35.
Hypothetical Lambda=q/alpha^2 is an EXTRA premise, not a paper result.
Magnetic route is L=-V(sum F_a^2/4), not the full dipole theory.
"""
import argparse
import json
import math
from pathlib import Path
import sympy as s


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output',required=True)
    p.add_argument('--mutate-product',action='store_true')
    args=p.parse_args()
    checks=[]; results={}
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    x=s.symbols('x',positive=True)
    mu=(s.sqrt(1+4*x*x)-1)/(2*x)
    F=x*s.sqrt(1+4*x*x)/2+s.asinh(2*x)/4-x
    check('P2_inverse',s.simplify((x*mu)**2+x*mu-x*x)==0,'b/a0=(sqrt(1+4x^2)-1)/2')
    check('P2_action_derivative',s.simplify(s.diff(F,x)-2*x*mu)==0,'F(x^2), F_prime(y)=mu(sqrt(y))')
    check('P2_zero_field',s.limit(F,x,0)==0,'chosen reference only; F+C gives the same force equation')
    check('P2_deep_limit',s.limit(F/x**3,x,0)==s.Rational(2,3),'deep-MOND cubic action primitive')
    check('P2_large_field_offset_diverges',s.limit((F-x*x)/x,x,s.oo)==-1,'F-x^2=-x+log(4x)/4+1/8+o(1); cannot impose finite Newtonian offset')
    C=s.symbols('C',real=True)
    check('additive_offset_invisible',s.diff(F+C,x)==s.diff(F,x),'force normalization does not determine absolute vacuum energy')
    check('vacuum_target_is_extra_constant',s.simplify((32*s.pi)/(8*s.pi))==4,'under rho_v=a0^2 C/(8piG), target requires C=32pi')

    q,alpha,k,eta=s.symbols('q alpha K eta_product',positive=True)
    a0=8*eta/(3*alpha*k) # magnitude, attractive sign selected separately
    coeff=s.simplify((q/alpha**2)/a0**2)
    check('dipole_alpha_elimination',coeff==9*q*k*k/(64*eta*eta),str(coeff))
    symmetric=s.simplify(coeff.subs(eta,3*s.sqrt(3)))
    check('symmetric_charge_coefficient',symmetric==q*k*k/192,str(symmetric))
    # u_a=eta_a^-2, sum u_a=1; AM-GM: product u_a <= 1/27.
    check('cancellation_AMGM_reduction',s.simplify(1/(s.Rational(1,3)**3))==27,'eta_product^2>=27 for positive real eta_a')
    required=6144*s.pi/q
    candidate=required if not args.mutate_product else required/2
    check('required_product_lower_bound',s.simplify((q*candidate/192)/(32*s.pi))==1,'K^2>=6144pi/q, K=|k2 k3 sin(theta)|; equality requires equal charge ratios')
    rows=[]
    for qq in (.1,1.,10.,100.):
        need=math.sqrt(6144*math.pi/qq)
        kk=math.sqrt(need)
        rows.append(dict(q=qq,minimum_oriented_product=need,equal_amplitudes_at_maximal_orientation=kk))
        check(f'finite_required_product_q={qq}',abs(qq*need**2/192-32*math.pi)<1e-10,f'K_min={need:.10g}; equal k2=k3={kk:.10g}')
    check('order_one_unit_choices_do_not_match',1/192<32*math.pi,'q=1, |k2|,|k3|<=1 imply Lambda/a0^2<=1/192, not 32pi')
    cancellation=s.symbols('S',positive=True)
    check('approximate_cancellation_bound',s.simplify((3/cancellation)**3)==27/cancellation**3,'if sum eta^-2=S, eta_product^2>=27/S^3; bound becomes K^2>=6144pi/(q S^3)')
    # A uniformly distributed relative phase has half the required sign.
    check('phase_average_induction_zero',s.integrate(s.sin(x),(x,0,2*s.pi))==0,'symmetric phase ensemble cannot select an attractive induction')
    check('phase_average_inverse_scale_diverges',s.integrate(1/s.sin(x),(x,s.pi/100,s.pi/2)).is_finite is True and s.limit(s.log(s.tan(x/2)),x,0)==-s.oo,'mean 1/|sin(theta)| diverges; average induction then invert is not average a0')
    phase_rows=[]
    for eps in (.02,.04,.13):
        best=1-2/math.pi*math.asin((1-eps)/(1+eps))
        phase_rows.append(dict(relative_window=eps,max_fraction_within_window_given_attractive_sign=best,unconditioned_fraction=best/2))
    check('phase_squared_relative_scatter',s.simplify(s.sqrt(s.Rational(3,8)-s.Rational(1,4))/s.Rational(1,2))==1/s.sqrt(2),'sin^2(theta) relative standard deviation=1/sqrt(2)')

    X,V,Vp=s.symbols('X V V_prime',positive=True)
    rho=V; pressure=-V+4*X*Vp/3
    check('magnetic_stress_trace',s.simplify(-rho+3*pressure-(-4*V+4*X*Vp))==0,'rho=V, p=-V+(4/3)X V_prime for isotropic magnetic fields')
    check('magnetic_deSitter_condition',s.simplify((rho+pressure).subs(Vp,0))==0,'for finite nonzero X, rho+p=0 implies V_prime=0')
    e=s.symbols('E0:9',real=True)
    perturbation=Vp*sum(ee**2 for ee in e)/2
    H=s.hessian(perturbation,e)
    check('electric_kinetic_matrix',H==Vp*s.eye(9),'L=-V(X_B-E^2/2) has electric Hessian V_prime times identity')
    check('magnetic_vacuum_kinetic_degeneracy',H.subs(Vp,0)==s.zeros(9),'same nonzero magnetic stationary point erases the quadratic electric kinetic term in this subclass')
    # Independent metric variation for an explicit three-field magnetic
    # triad and a quadratic polynomial, without inserting fluid pressures.
    u0,u1,u2,u3=s.symbols('u0 u1 u2 u3',real=True)
    B,v1,v2=s.symbols('B v1 v2',real=True)
    inv=[u0,u1,u2,u3]
    volume=1/s.sqrt(-u0*u1*u2*u3)
    Xm=B*B*(u1*u2+u2*u3+u1*u3)/2
    Lm=-(v1*Xm+v2*Xm*Xm+C)
    flat={u0:-1,u1:1,u2:1,u3:1}
    components=[s.simplify((-2*s.diff(volume*Lm,u)/volume).subs(flat)) for u in inv]
    Xb=3*B*B/2
    vb=v1*Xb+v2*Xb*Xb+C
    pb=-vb+4*Xb*(v1+2*v2*Xb)/3
    check('independent_metric_variation',s.simplify(components[0]-vb)==0 and all(s.simplify(t-pb)==0 for t in components[1:]),'explicit triad T00 and all three Tii agree with general magnetic formula')
    Xe=Xb-s.Add(*(ee**2 for ee in e))/2
    fullL=-(v1*Xe+v2*Xe*Xe+C)
    exactH=s.hessian(fullL,e).subs({ee:0 for ee in e})
    check('independent_full_Lagrangian_Hessian',exactH==(v1+2*v2*Xb)*s.eye(9),'direct differentiation before electric perturbations are set to zero')
    # V(X) -> V(X)+C changes rho and p, but not field stationary point
    # or kinetic Hessian. No gauge-field symmetry forbids that scalar term.
    check('condensate_vacuum_height_unfixed',s.diff(V+C,C)==1 and s.diff(Vp,C)==0,'vacuum height shifts independently of stationary/response data')

    # Most general rotationally covariant linear matrix built from one
    # velocity and scalar coefficients: a I+b vv^T+c [v]_cross.
    g=s.symbols('g',real=True)
    vx,vy,vz=s.symbols('vx vy vz',real=True)
    a2,b2,c2,a3,b3,c3=s.symbols('a2 b2 c2 a3 b3 c3',real=True)
    gv=s.Matrix([g,0,0]); vv=s.Matrix([vx,vy,vz])
    z2=a2*gv+b2*vv*(vv.dot(gv))+c2*vv.cross(gv)
    z3=a3*gv+b3*vv*(vv.dot(gv))+c3*vv.cross(gv)
    crossx=s.factor(z2.cross(z3)[0])
    expected=g*g*vx*(vy*vy+vz*vz)*(b3*c2-b2*c3)
    check('stream_longitudinal_cross_term',s.expand(crossx-expected)==0,str(crossx))
    check('parity_even_linear_stream_zero',crossx.subs({c2:0,c3:0})==0,'polar dipoles built from polar g,v have c=0 absent a pseudoscalar response coefficient')
    check('single_stream_not_spherically_uniform',crossx.subs(vx,0)==0 and crossx.subs({vy:0,vz:0})==0,'longitudinal response vanishes for perpendicular and parallel g/v')
    check('stream_reversal_flips_longitudinal_term',s.simplify(crossx.subs({vx:-vx,vy:-vy,vz:-vz})+crossx)==0,'symmetric counter-stream ensemble cancels this term at fixed coefficients')
    check('fixed_linear_dipoles_have_wrong_g_reversal',crossx.subs(g,-g)==crossx,'cross(M2 g,M3 g) is even in g, whereas deep-MOND induction |g|g is odd; global closure needs state-dependent matrices or a nonlinear branch')
    results.update(P2_primitive=str(F),dipole_coefficient=str(coeff),dipole_bound=str(required),dipole_rows=rows,phase_rows=phase_rows)
    results['stream_longitudinal_cross_term']=str(crossx)
    data=dict(checks=checks,results=results,mutated=args.mutate_product,
              verdict='32pi selection remains OPEN; coefficient is not fixed by tested force reconstruction, local dipole response, phase averaging, or simple magnetic vacuum extremum.',
              scope=['P2 spherical algebraic inverse mapped into AQUAL; no full covariant completion','positive charge ratios and exact linear cancellation','hypothetical q=Lambda alpha^2 not derived','purely magnetic isotropic L=-V(X), excludes extra invariants, derivatives, matter and electric backgrounds'])
    Path(args.output).write_text(json.dumps(data,indent=2)+'\n')
    failed=sum(not c['passed'] for c in checks)
    print(f'{len(checks)-failed}/{len(checks)} checks pass; coefficient puzzle OPEN.')
    return int(failed>0)


if __name__=='__main__':
    raise SystemExit(main())
