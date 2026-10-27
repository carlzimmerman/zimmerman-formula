#!/usr/bin/env python3
"""Finite exact and numerical checks of the explicitly defined S4 pion determinant."""
import argparse
import json
from pathlib import Path
import sympy as s
import mpmath as mp


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    checks = []

    def exact(name, lhs, rhs=0):
        delta = s.simplify(lhs-rhs)
        if delta != 0:
            raise AssertionError((name, delta))
        checks.append({'name': name, 'verified': True, 'value': str(s.simplify(lhs))})

    u, H, mass2, F, Z, e2 = s.symbols('u H mass2 F Z e2', positive=True)
    ell = s.symbols('ell', integer=True, nonnegative=True)
    harmonic_dim = (ell+1)*(ell+2)*(ell+3)*(ell+4)/24-(ell-1)*ell*(ell+1)*(ell+2)/24
    exact('S4 harmonic degeneracy from trace subtraction', harmonic_dim,
          (ell+1)*(ell+2)*(2*ell+3)/6)
    exact('shifted spectral polynomial',
          ((ell+s.Rational(3,2))**3-(ell+s.Rational(3,2))/4)/3,
          (ell+1)*(ell+2)*(2*ell+3)/6)
    exact('constant mode retained', harmonic_dim.subs(ell, 0), 1)
    residues = 0
    for j in range(4):
        zz3 = -s.bernoulli(4+2*j, s.Rational(1,2))/(4+2*j)
        zz1 = -s.bernoulli(2+2*j, s.Rational(1,2))/(2+2*j)
        residues += (-u)**j/s.factorial(j)*(zz3-zz1/4)
    heat = s.series(s.exp(9*u/4)*(1-u/4+2*u*u*residues), u, 0, 6).removeO().expand()
    coefficients = [s.expand(heat).coeff(u,j) for j in range(6)]
    targets = [1,2,s.Rational(29,15),s.Rational(74,63),s.Rational(149,315),s.Rational(358,3465)]
    for j, target in enumerate(targets):
        exact('heat coefficient a'+str(j),coefficients[j],target)
    exact('a2 independent curvature invariant', s.Rational(24-36,180)+s.Rational(12**2,72),coefficients[2])
    xi=s.symbols('xi',real=True)
    shifted=s.series(s.exp(-12*xi*u)*heat,u,0,3).removeO().expand()
    exact('curvature-coupled a1',shifted.coeff(u,1),2-12*xi)
    exact('curvature-coupled a2',shifted.coeff(u,2),s.Rational(-1,15)+72*(s.Rational(1,6)-xi)**2)
    a3=coefficients[3]
    f6=-a3*H**6/(32*s.pi**2*mass2)
    rho6=f6-H*s.diff(f6,H)/4
    exact('metric stress H6 factor',rho6,a3*H**6/(64*s.pi**2*mass2))
    delta=2*e2*F**2*Z
    drho=2*(rho6.subs(mass2,mass2+delta)-rho6)
    exact('charged pair curvature difference',drho,a3*H**6/(32*s.pi**2)*(1/(mass2+delta)-1/mass2))
    exact('zero-charge curvature response',s.diff(drho,e2).subs(e2,0),-a3*F**2*Z*H**6/(16*s.pi**2*mass2**2))
    exact('third mass derivative H6 coefficient',32*s.pi**2*mass2*s.diff(f6,mass2,3),s.Rational(148,21)*H**6/mass2**3)
    for expression,name in [(f6,'free density'),(rho6,'stress'),(drho,'charged difference')]:
        exact('linear H coefficient of retained '+name,s.limit(expression/H,H,0,dir='+'))

    mp.mp.dps=65
    numeric=[]
    def record(name, passed, **values):
        if not passed:
            raise AssertionError((name,values))
        checks.append({'name':name,'verified':True})
        numeric.append({'name':name,**{k:mp.nstr(v,35) for k,v in values.items()}})
    heat_N=400
    for ux in ['0.02','0.01','0.005','0.0025']:
        t=mp.mpf(ux)
        direct=mp.fsum(mp.mpf((l+1)*(l+2)*(2*l+3))/6*mp.exp(-t*l*(l+3)) for l in range(heat_N))
        poly=mp.fsum(mp.mpf(str(s.numer(a)))/mp.mpf(str(s.denom(a)))*t**j for j,a in enumerate(coefficients))
        scaled=6*t*t*direct
        tail=8*mp.exp(-t*heat_N**2)*(heat_N**3+(t*heat_N**2+1)/(2*t*t))
        record('spectral heat comparison '+ux,abs(scaled-poly)<5*t**6,
               absolute_residual=abs(scaled-poly),declared_tolerance=5*t**6,positive_heat_tail_bound=tail)
    N=2000
    for denominator in [4,8,16,32]:
        ratio=mp.mpf(1)/denominator
        a=ratio**-2-mp.mpf(9)/4
        mu=mp.sqrt(a); z=mp.mpf('.5')+1j*mu
        p1=mp.polygamma(1,z); p2=mp.polygamma(2,z)
        S2=-mp.im(p1)/(2*mu)
        S3=-mp.im(p1)/(8*mu**3)+mp.re(p2)/(8*mu**2)
        resolved=S2-(a+mp.mpf('.25'))*S3
        direct=mp.fsum((mp.mpf(k)+mp.mpf('.5'))*((mp.mpf(k)+mp.mpf('.5'))**2-mp.mpf('.25'))/((mp.mpf(k)+mp.mpf('.5'))**2+a)**3 for k in range(N))
        start=mp.mpf(N)+mp.mpf('.5')
        bound=1/start**3+1/(2*start**2)
        record('UV-finite resolvent positive-tail bracket M/H='+str(denominator),
               direct<=resolved+mp.mpf('1e-58') and resolved<=direct+bound,
               partial_sum=direct,polygamma_sum=resolved,tail_upper_bound=bound)
        normalized=4*resolved/ratio**2
        a3_est=(normalized-1-2*ratio**2-mp.mpf(58)/15*ratio**4)/ratio**6
        record('H6 mass-derivative asymptotic M/H='+str(denominator),
               abs(a3_est-mp.mpf(148)/21)<20*ratio**2,
               coefficient_estimator=a3_est,target=mp.mpf(148)/21,declared_tolerance=20*ratio**2)
    result={'checks_passed':len(checks),'checks':checks,'numerical_comparisons':numeric,
            'heat_coefficients':[str(x) for x in coefficients],
            'pion_determinant_linear_H_coefficient':'0 at every fixed positive mass in the defined subtracted determinant',
            'no_alpha_target_used':True,
            'limits':'H/M -> 0 at fixed positive M; not M -> 0 at fixed H',
            'non_claims':['No complete curved-space QCD path integral','No physical c_H or R(alpha) root','No full interacting QED response','No interval certification','No fitted or assigned numerical Z,F or alpha']}
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'checks_passed':len(checks),'linear_H_pion_coefficient':0}))


if __name__=='__main__':
    main()
