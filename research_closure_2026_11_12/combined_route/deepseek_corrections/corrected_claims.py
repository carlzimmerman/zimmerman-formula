#!/usr/bin/env python3
"""Corrected G238/G241/G242 assertions and regression witnesses.

Historical data/results are retained under archive/. No density-slope falsifier,
general MI theorem, completion selection, or forest/KiDS pass is asserted here.
"""
import argparse
import json
import math
from pathlib import Path
import sys
sys.dont_write_bytecode = True
import numpy as np
import sympy as sp
from corrected_core import (Y_EXTERNAL, physical_external_from_newtonian,
                            mu_simple, aqual_asymptote, qumond_asymptote,
                            qumond_monopole, aqual_density_factor)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--section', choices=['all','g238','g241','g242'], default='all')
    ap.add_argument('--output-dir', type=Path, required=True)
    args = ap.parse_args()
    out = args.output_dir.resolve()
    lane = Path(__file__).resolve().parent
    if lane not in out.parents:
        raise SystemExit('Output directory must be a child of the correction lane')
    out.mkdir(parents=True, exist_ok=True)
    checks = []
    def check(name, ok, measured):
        checks.append(dict(name=name, passed=bool(ok), measured=measured))
        print(('PASS' if ok else 'FAIL')+' '+name+': '+str(measured), flush=True)

    r, b, C = sp.symbols('r b C', positive=True)
    mass = C*(r+b)
    rho = sp.diff(mass,r)/(4*sp.pi*r**2)
    p = sp.simplify(r*sp.diff(mass,r)/mass)
    gamma = sp.simplify(r*sp.diff(rho,r)/rho)
    full = sp.simplify(p-3+r*sp.diff(p,r)/p)
    check('G238 local-density identity includes dlog(p)/dlog(r)', full==gamma== -2,
          dict(p=str(p), local_density_slope=str(gamma), mean_density_slope=str(p-3)))
    check('G238 original finite-radius slope counterexample detected',
          sp.simplify(p-3-gamma)!=0, str(sp.simplify(p-3-gamma)))
    # Preserve the table values, but use sigma_logM ~= sigma_M/M for a log fit.
    R=np.array([20,25,30,35,40,45,50,55,60,65,70,75,80],float)
    M=np.array([1.94,2.30,2.65,3.05,3.54,4.08,4.51,4.88,5.19,5.56,5.88,6.14,6.36])
    EL=np.array([.12,.11,.13,.15,.17,.21,.26,.31,.34,.38,.43,.46,.48])
    EH=np.array([.12,.12,.14,.16,.18,.22,.27,.32,.36,.40,.46,.50,.53])
    sigma_log=((EL+EH)/2)/M
    weights=1/sigma_log**2
    X=np.column_stack([np.ones(len(R)),np.log(R)])
    covariance=np.linalg.inv(X.T @ (weights[:,None]*X))
    beta=covariance @ (X.T @ (weights*np.log(M)))
    logfit=dict(p=float(beta[1]), sigma_p_diagonal_only=float(np.sqrt(covariance[1,1])),
                mean_enclosed_density_power_law_slope=float(beta[1]-3),
                local_density_slope=None, covariance_available=False,
                interpretation='Descriptive power-law mass fit; no calibrated significance or local density falsifier')
    # An exact power law and a pure mass offset distinguish this estimator from density differentiation.
    injected=X @ np.array([.7,.8])
    recovered=covariance @ (X.T @ (weights*injected))
    check('G238 log-fit recovers an exact power law', abs(recovered[1]-.8)<1e-12, recovered.tolist())

    y=Y_EXTERNAL
    x=physical_external_from_newtonian(y)
    check('G240 physical/Newtonian external fields match constitutively',
          abs(x*float(mu_simple(x))/y-1)<1e-14, dict(y_newtonian=y,x_physical=x))
    u,L=sp.symbols('u L', positive=True)
    f=(1+L*(1-u*u))**sp.Rational(-1,2)
    laplace_factor=sp.simplify(-sp.diff((1-u*u)*sp.diff(f,u),u))
    expected=L*((3+L)*u*u-(1+L))/(1+L*(1-u*u))**sp.Rational(5,2)
    check('AQUAL effective density independently differentiated from potential',
          sp.simplify(laplace_factor-expected)==0, str(laplace_factor))
    Lnum=1/(1+x)
    c,w=np.polynomial.legendre.leggauss(256)
    angular=float(w @ aqual_density_factor(c,Lnum)/2)
    equator=float(aqual_density_factor(0,Lnum)); pole=float(aqual_density_factor(1,Lnum))
    check('AQUAL EFE source changes sign and has zero shell monopole',
          equator<0<pole and abs(angular)<1e-13,
          dict(equator=equator,pole=pole,angular_average=angular))
    aqual_quad=float(w @ (1/np.sqrt(1+Lnum*(1-c*c)))/2)/float(mu_simple(x))
    check('AQUAL solid-angle Green integral matches closed form',
          abs(aqual_quad/aqual_asymptote(x)-1)<1e-13, dict(quadrature=aqual_quad,analytic=aqual_asymptote(x)))
    # Independent finite-radius quadrature approaches an independently differentiated asymptote.
    far=float(qumond_monopole([1e3], y, order=256)[0])
    check('QUMOND finite-radius flux approaches its own asymptote',
          abs(far/qumond_asymptote(y)-1)<1e-7,
          dict(flux_at_r1000=far,analytic=qumond_asymptote(y)))
    check('Original small-field AQUAL Green benchmark is rejected',
          abs(aqual_asymptote(.01273)-21.42)>40,
          dict(correct=aqual_asymptote(.01273),historical=21.42))

    # This is an algebraic map identity only. No general MI trajectory law is tested.
    inverse=sp.simplify(1/(u/(1+u))-u/(u*u/(1+u)))
    check('G241 constitutive inverse identity, restricted to supplied algebraic map', inverse==0, str(inverse))
    mi=dict(general_modified_inertia_efe='not derived', unique_aqual_completion='not derived',
            lensing_exclusion_scope='baryons-only GR metric plus inertia-only changes; no universal MI exclusion',
            removed_checks=['M_QUM returning M_MI','hard-coded True for field ontology implies AQUAL'],
            source='Milgrom astro-ph/9303012v1 section IV equations 53-55: circular orbits only')

    ratio=0.6087047874275476
    need=.70/1.25
    gcrit=(ratio/need)**6
    with_growth=ratio*3**(-1/6)
    check('G242 fixed-mass fails while conditional growth opens ratio inequality',
          ratio>need and with_growth<need and abs(ratio*gcrit**(-1/6)-need)<1e-15,
          dict(fixed_mass=ratio,need=need,at_growth3=with_growth,growth_threshold=gcrit))
    mass_symbol,density,coherence,G,a0=sp.symbols('M rho R G a0',positive=True)
    rset=sp.sqrt(G*mass_symbol/a0)/(sp.sqrt(G*density*a0*coherence)/a0)
    target=sp.sqrt(mass_symbol/(density*coherence))
    check('G242 cancellation leaves coherence-scale dependence',
          sp.simplify(rset-target)==0 and sp.simplify(coherence*sp.diff(target,coherence)/target)==-sp.Rational(1,2),
          dict(radius=str(target),coherence_log_elasticity='-1/2'))
    g242=dict(ratio_condition_only=True,growth_threshold=gcrit,growth_computed=False,
              fixed_mass_pass=False,absolute_normalization_pass=None,forest_likelihood_pass=None,
              kids_likelihood_pass=None,efe_equals_settled_radius='unproved',
              coherence_scale='assumed; controls absolute radius and history if evolving',
              population_mapping='forest and lensing samples not shown to be progenitor-descendant populations')
    result=dict(section=args.section,checks=checks,g238=logfit,g241=mi,g242=g242,
                aqual=dict(x_physical=x,y_newtonian=y,L=Lnum,monopole=aqual_asymptote(x),
                           qumond_monopole=qumond_asymptote(y),negative_source_belt_abs_cos_lt=math.sqrt((1+Lnum)/(3+Lnum)),
                           local_density='M L ((3+L)cos(theta)^2-(1+L))/(4 pi mu_e r^3 (1+L sin(theta)^2)^(5/2))',
                           interpretation='signed effective source, not a nonnegative cold-mass density'),
                theory_closed=False,non_claims=['No PDE rerun in this script','No data covariance recovered','No new empirical pass'])
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    if not all(x['passed'] for x in checks): raise SystemExit(1)

if __name__=='__main__': main()
