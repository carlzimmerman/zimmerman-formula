#!/usr/bin/env python3
"""Scoped vacuum-to-MOND audit. No 32pi derivation or quantum-gravity validation.

Conventions and primary-source equations: TONIGHT_32PI_CONTRACT.md.
All acceleration variables dimensionless, with a_star=1 in quadrature.
"""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import gamma, exp1, gammainc
import sympy as s


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    args=ap.parse_args(); checks=[]; rows=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    b,g,h,astar,lam=s.symbols('b g h a_star lambda',positive=True)
    # b is imposed Newtonian acceleration; h is RMS fluctuation magnitude.
    rms=s.sqrt(b*b+h*h)
    shift=rms-h
    inverted=s.sqrt(g*g+2*h*g)
    claimed=s.sqrt(g*g+h*h)-h
    check('shifted_rms_exact_inverse',s.simplify(rms.subs(b,inverted)**2-(g+h)**2)==0,
          'g=sqrt(b²+h²)-h implies b²=g²+2hg, not b=sqrt(g²+h²)-h')
    check('shifted_rms_low_field_is_suppression',s.limit(shift/b**2,b,0)==1/(2*h),
          'g=b²/(2h)+O(b⁴); enhanced deep-MOND would require g²=2hb')
    check('claimed_constitutive_inverse_is_P2',s.simplify((b+h)**2-(b*b+2*h*b+h*h))==0,
          'claimed b(g) is instead inverted by g²=b²+2hb')
    check('two_maps_differ_at_crossover',abs(float(shift.subs({b:1,h:1}))-float(s.sqrt(3)))>1,
          'same b=h=1: actual shifted RMS sqrt(2)-1; P2 sqrt(3)')
    # An equal-weight +/- noise vector is an exact finite ensemble, no RNG.
    vectors=np.vstack((np.eye(3),-np.eye(3)))/math.sqrt(2)
    mean=vectors.mean(axis=0); variance=float(np.mean(np.sum(vectors**2,axis=1)))
    for bb in (.01,1.,10.):
        acceleration=np.array([bb,0,0])+vectors
        average=acceleration.mean(axis=0)
        second=float(np.mean(np.sum(acceleration**2,axis=1)))
        check(f'independent_vector_mean_and_second_moment_b={bb}',
              np.max(abs(average-[bb,0,0]))<1e-13 and abs(second-(bb*bb+variance))<1e-13,
              f'mean={average.tolist()}, squared RMS={second}; mean is Newtonian')
    check('P2_requires_source_dependent_variance',s.diff(2*h*b,b)==2*h,
          'zero-mean noise must have variance(b)=2hb to mimic P2 in RMS; constant vacuum variance cannot')
    # Homogeneous source-independent two-point noise has a source-independent
    # structure function, whereas P2 variance at radius r scales with mass.
    mass,r,a0,G=s.symbols('M r a0 G',positive=True)
    required=a0*G*mass/r**2
    check('relative_noise_requires_mass_dependent_correlations',s.diff(required,mass)==a0*G/r**2,
          'D(r)=E|xi(x)-xi(0)|² in a fixed homogeneous vacuum cannot equal a0 GM/r² for every M')
    # Distribution-level source normalization and coefficient dictionary.
    radial=s.symbols('R',positive=True)
    pdf=2/astar*s.exp(-2*radial/astar)
    check('Yukawa_radial_probability_normalized',s.integrate(pdf,(radial,0,s.oo))==1,
          'using the newer paper normalization, radial density is (2/a_star) exp(-2R/a_star)')
    second=s.integrate(radial**2*pdf,(radial,0,s.oo))
    check('Yukawa_variance',second==astar**2/2,str(second))
    ratio=s.simplify(lam*astar**2/(2*s.sqrt(second))**2)
    check('published_coefficient_dictionary',ratio==lam/2,'with a0=2h, Lambda/a0²=lambda/2; lambda=3 gives 3/2')
    check('published_dictionary_needs_extra_ordering',s.solve(s.Eq(ratio,32*s.pi),lam)==[64*s.pi],
          '32pi would require lambda=64pi, rather than the cited value 3')
    # A Yukawa function solves the modified Helmholtz equation only away
    # from zero. Surface flux displays its distributional delta source.
    psi=s.exp(-radial/astar)/radial
    lap=s.diff(radial**2*s.diff(psi,radial),radial)/radial**2
    check('Yukawa_equation_away_from_origin',s.simplify(lap-psi/astar**2)==0,'valid for R>0')
    flux=s.limit(4*s.pi*radial**2*s.diff(psi,radial),radial,0)
    check('Yukawa_has_point_source',flux==-4*s.pi,'(Delta-a_star^-2) exp(-R/a_star)/R=-4pi delta^3; not a free global eigenstate')
    check('Yukawa_gradient_norm_diverges',s.limit(radial**4*s.diff(psi,radial)**2,radial,0)==1,
          'R² |psi_prime|² ~ R^-2 near zero; ordinary H1 norm is infinite')
    # Concrete attempted rescue: b := mean |g e_z + xi| - mean |xi|.
    # This is deliberately a NEW constitutive hypothesis. Angular averaging
    # gives R+g²/(3R) for R>=g and g+R²/(3g) for R<=g.
    u,mu=s.symbols('u mu',positive=True)
    antiderivative=(u*u+g*g+2*u*g*s.Symbol('m'))**s.Rational(3,2)/(3*u*g)
    m=s.Symbol('m')
    check('angular_norm_antiderivative',s.simplify(s.diff(antiderivative,m)-s.sqrt(u*u+g*g+2*u*g*m))==0,
          'angular mean is ((R+g)^3-|R-g|^3)/(6Rg)')
    high=((u+g)**3-(u-g)**3)/(6*u*g)
    low=((u+g)**3-(g-u)**3)/(6*u*g)
    check('angular_piecewise_high',s.simplify(high-u-g*g/(3*u))==0,'R>=g')
    check('angular_piecewise_low',s.simplify(low-g-u*u/(3*g))==0,'R<=g')
    for gg in (1e-2,1e-4,1e-6):
        first=quad(lambda rr:2*math.exp(-2*rr)*(gg+rr*rr/(3*gg)-rr),0,gg,epsabs=1e-25)[0]
        rescue=first+gg*gg/3*2*exp1(2*gg)
        quotient=rescue/(gg*gg)
        remainder=quotient-(2/3)*math.log(1/gg)
        expected=-(2/3)*(np.euler_gamma+math.log(2))+11/9
        check(f'Yukawa_rescue_logarithmic_susceptibility_g={gg}',abs(remainder-expected)<4*gg,
              f'b/g²={quotient:.12g}, constant remainder={remainder:.12g}, limit={expected:.12g}')
        rows.append(dict(g_over_a_star=gg,response_over_g_squared=quotient))
    # Regularize via a gamma radial family, maintaining identical variance.
    # k>1 yields finite inverse-radius moment; k>2 yields finite H1 norm.
    shape=s.symbols('k',positive=True)
    theta=astar/s.sqrt(2*shape*(shape+1))
    inverse=1/((shape-1)*theta)
    rescued_a0=3/inverse
    C=s.simplify(lam*astar**2/rescued_a0**2)
    check('gamma_rescue_coefficient',s.simplify(C-2*lam*shape*(shape+1)/(9*(shape-1)**2))==0,str(C))
    check('gamma_coefficient_decreases_for_k_above_one',
          s.simplify(s.diff(C,shape)+2*lam*(3*shape+1)/(9*(shape-1)**3))==0,
          'strictly decreasing for k>1; H1 subfamily k>2 has C<4lambda/3')
    for kk in (2.1,3.,6.):
        tt=1/math.sqrt(2*kk*(kk+1))
        p=lambda rr:rr**(kk-1)*math.exp(-rr/tt)/(gamma(kk)*tt**kk)
        measured=quad(lambda rr:p(rr)/rr,0,np.inf,epsabs=1e-11)[0]
        exact=1/((kk-1)*tt)
        check(f'gamma_inverse_moment_k={kk}',abs(measured/exact-1)<2e-9,
              f'E[1/R]={measured:.12g}; at lambda=3 C={float(C.subs({lam:3,shape:kk})):.12g}')
    root=max(float(s.re(v)) for v in s.solve(s.Eq(C.subs(lam,3),32*s.pi),shape))
    check('gamma_target_is_tuned_and_outside_H1_subfamily',1<root<2,
          f'target k={root:.12g}; no equation selects it; ordinary gradient norm diverges in this subfamily')
    # Vacuum pressure lock removes additive freedom but not multiplicative
    # response normalization. Work with static AQUAL and a separate fixed
    # DBI pressure minimum. This is not a covariant health proof.
    Q,T,L,kappa=s.symbols('Q T L kappa',positive=True)
    # Q denotes displacement from the DBI minimum, so substitute zero.
    pressure=-T+T*(1-s.sqrt(1-Q*Q/L**2))
    check('fixed_DBI_vacuum_and_positive_Hessian',pressure.subs(Q,0)==-T and s.diff(pressure,Q,2).subs(Q,0)==T/L**2,
          'vacuum height and local pressure Hessian do not depend on kappa')
    physical_a02=kappa*kappa*G*T
    cosmological=8*s.pi*G*T
    check('pressure_locked_coefficient_remains_continuous',s.simplify(cosmological/physical_a02)==8*s.pi/kappa**2,
          'same vacuum T, different physical a0, because kappa remains multiplicative')
    xx=s.symbols('x',positive=True)
    interpolation=(s.sqrt(1+4*xx*xx)-1)/(2*xx)
    longitudinal=s.simplify(interpolation+xx*s.diff(interpolation,xx))
    check('P2_static_longitudinal_ellipticity',s.simplify(longitudinal-2*xx/s.sqrt(1+4*xx*xx))==0,
          'mu+x mu_prime = 2x/sqrt(1+4x²)>0 for every positive a0; mu>0 as well')
    for kap in (.4,.5,.6):
        check(f'pressure_locked_countermodel_kappa={kap}',
              kap>0 and all(float(interpolation.subs(xx,xx0))>0 and float(longitudinal.subs(xx,xx0))>0 for xx0 in (.01,1,100)),
              f'Lambda/a0²={8*math.pi/kap**2:.12g}; vacuum minimum and static ellipticity persist')
    result=dict(checks=checks,rows=rows,gamma_target_shape=root,
                gamma_coefficient=str(C),
                verdict='32pi remains OPEN. The published fluctuation inversion fails algebraically; a mean-magnitude rescue has distribution-dependent normalization; locking the vacuum height still leaves a multiplicative response coefficient.',
                non_claims=['No full quantum-gravity audit','RMS is not mean orbital acceleration','Rescue constitutive law is hypothetical','Gamma-family H1 bound is not a bound on all wavefunctions','Point-interaction extensions require a separate domain/measure analysis','Static ellipticity is not covariant health'])
    Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    failed=sum(not c['passed'] for c in checks)
    print(f'{len(checks)-failed}/{len(checks)} scoped checks pass; 32pi OPEN.')
    return int(failed>0)


if __name__=='__main__': raise SystemExit(main())
