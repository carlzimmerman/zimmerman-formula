#!/usr/bin/env python3
"""Exact inverse construction for a hypothetical mean-magnitude response.

The P2 target is INPUT here. Deriving a distribution that reproduces it does
not derive MOND or a vacuum theory. R is fluctuation acceleration magnitude,
not spatial radius. Lambda=lambda*a_star² and a_star²=2*variance are extra
dictionary assumptions when changed from the published Yukawa state.
"""
import argparse
import json
import math
from pathlib import Path
from scipy.integrate import quad
import sympy as s


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    args=ap.parse_args(); checks=[]; rows=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    R,h=s.symbols('R h',positive=True)
    lap=lambda f:s.diff(R**2*s.diff(f,R),R)/R**2
    response=s.sqrt(R**2+h**2)-h
    density=15*h**4/(8*s.pi*(R**2+h**2)**s.Rational(7,2))
    check('P2_inverse_bilaplacian_density',s.simplify(-lap(lap(response))/(8*s.pi)-density)==0,
          'Delta² |x-y|=-8pi delta³(x-y); unique density for this convolution and finite first moment')
    # R=h*u. Moment integral is a beta integral. This explicitly computes
    # normalization, inverse radius, mean, variance, without quadrature fit.
    def moment(power):
        # integral u^(power+2) (1+u²)^(-7/2) du = B((p+3)/2,(4-p)/2)/2
        aa=s.Rational(power+3,2); bb=s.Rational(4-power,2)
        return s.simplify(s.Rational(15,4)*h**power*s.gamma(aa)*s.gamma(bb)/s.gamma(s.Rational(7,2)))
    for power,expected in ((0,1),(-1,3/(2*h)),(1,h),(2,3*h*h/2)):
        check(f'density_exact_moment_power={power}',s.simplify(moment(power)-expected)==0,str(moment(power)))
    # psi=sqrt(density); its regular gradient norm is finite and exact.
    # |psi'|²=(49/4) R²/(R²+h²)² * density.
    kinetic=s.simplify(s.Rational(49*15,16)/h**2*s.gamma(s.Rational(5,2))*s.gamma(3)/s.gamma(s.Rational(11,2)))
    check('regular_finite_gradient_norm',kinetic==7/(3*h*h),f'ordinary integral |grad psi|²={kinetic}; smooth at zero and decays at infinity')
    psi=s.sqrt(density)
    potential=s.simplify(lap(psi)/psi)
    check('inverse_ground_state_operator',s.simplify(potential-(35*R**2-42*h**2)/(4*(R**2+h**2)**2))==0,
          'H=-Delta+V, V=Delta(psi)/psi, has this state; V constructed from target, not independently selected')
    # Independent direct angular/radial quadrature for h=1.
    pdf=lambda rr:7.5*rr*rr/(1+rr*rr)**3.5
    for gg in (.01,.1,1.,10.):
        inner=quad(lambda rr:pdf(rr)*(gg+rr*rr/(3*gg)-rr),0,gg,epsabs=1e-13)[0]
        outer=quad(lambda rr:pdf(rr)*gg*gg/(3*rr),gg,math.inf,epsabs=1e-13)[0]
        measured=inner+outer
        expected=gg*gg/(math.sqrt(1+gg*gg)+1)
        check(f'independent_full_response_g_over_h={gg}',abs(measured/expected-1)<2e-10,
              f'quadrature={measured:.12g}, exact sqrt(g²+1)-1={expected:.12g}')
        rows.append(dict(g_over_h=gg,measured_response=measured,exact_response=expected))
    lam=s.symbols('lambda',positive=True)
    # h=a0/2; variance=3h²/2. Match variance to a_star²/2 only as an EXTRA
    # comparison dictionary. Its quantum operator need not have same scale.
    a0=2*h; astar2=2*moment(2)
    coefficient=s.simplify(lam*astar2/a0**2)
    check('variance_matched_vacuum_dictionary',coefficient==3*lam/4,
          'under Lambda=lambda*a_star² and a_star²=2 variance, Lambda/a0²=3lambda/4')
    check('target_still_requires_extra_ordering',s.solve(s.Eq(coefficient,32*s.pi),lam)==[128*s.pi/3],
          'lambda=3 gives 9/4; exact target would require lambda=128pi/3')
    # Independent physical dictionary: if a_star² * integral|grad psi|²=1,
    # the SAME regular state gives a different inferred acceleration scale.
    operator_scale2=1/kinetic
    operator_C=s.simplify(lam*operator_scale2/a0**2)
    check('variance_and_operator_dictionaries_are_distinct',operator_C==3*lam/28 and s.simplify(astar2/operator_scale2)==7,
          'a_star² times gradient norm=1 instead gives C=3lambda/28; no license to transfer the Yukawa operator dictionary')
    data=dict(checks=checks,rows=rows,density=str(density),moments={str(p):str(moment(p)) for p in (-1,0,1,2)},
              inverse_potential=str(potential),gradient_norm=str(kinetic),variance_dictionary_coefficient=str(coefficient),operator_dictionary_coefficient=str(operator_C),
              verdict='An exact regular distribution realizes P2 under a hypothetical mean-magnitude constitutive rule. The target was used to reconstruct the state; neither its selection nor 32pi is derived.',
              non_claims=['Not a theory of modified inertia or gravity','Distribution and operator reconstructed from desired law','No covariant field equations or source-conditioned state selection','Vacuum dictionary not derived','Configuration variable is acceleration, not spatial radius','No astrophysical data fit or new physical coefficient prediction'])
    Path(args.output).write_text(json.dumps(data,indent=2)+'\n')
    failed=sum(not c['passed'] for c in checks)
    print(f'{len(checks)-failed}/{len(checks)} inverse-construction checks pass; 32pi OPEN.')
    return int(failed>0)


if __name__=='__main__': raise SystemExit(main())
