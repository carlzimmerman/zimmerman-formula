#!/usr/bin/env python3
"""Finite hydrostatic checks for PN28-DISP's conditional reduced EOS."""
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as s
from scipy.integrate import quad, solve_ivp


def density(psi):
    if psi <= 0:
        return 0.
    # Stable at large central density.
    return psi**1.5/(-math.expm1(2.5*math.log(psi)))


def solve_core(pc, tol):
    nc=density(pc)
    eps=min(1e-6,1e-5/math.sqrt(nc))
    def rhs(r,y):
        psi,m=y
        return [-m/(r*r),r*r*density(psi)]
    def edge(r,y):
        return y[0]
    edge.terminal=True
    edge.direction=-1
    def quarter(r,y):
        return density(y[0])-nc/4
    quarter.direction=-1
    sol=solve_ivp(rhs,(eps,30),[pc-nc*eps**2/6,nc*eps**3/3],
                  events=[quarter,edge],rtol=tol,atol=tol*.01,
                  dense_output=True,max_step=.025)
    assert sol.success and len(sol.t_events[0])==len(sol.t_events[1])==1
    rq=sol.t_events[0][0]
    radius=sol.t_events[1][0]
    mass=sol.y_events[1][0,1]
    # Separate density integration verifies the mass ledger, not the all-r theorem.
    qmass=quad(lambda r:r*r*density(float(sol.sol(r)[0])),eps,radius,
               epsabs=2e-8,epsrel=2e-8,limit=300)[0]+nc*eps**3/3
    column=math.sqrt(2.5)*nc*rq
    return {'psi_c':pc,'rho_c_over_rho_star':nc,'radius_over_ell':radius,
            'mass_dimensionless':mass,'quarter_radius_over_ell':rq,
            'quarter_column_coefficient':column,
            'mass_quadrature_relative_error':abs(qmass/mass-1),
            'edge_slope':-mass/radius**2}


def main():
    checks={}
    t,B,rs=s.symbols('t B rho_star',positive=True)
    n=t**s.Rational(3,5)/(1-t)
    pressure=-B*s.log(1-t)
    enthalpy=s.Rational(5,2)*B/rs*t**s.Rational(2,5)
    checks['exact_enthalpy_derivative']=s.simplify(s.diff(enthalpy,t)-s.diff(pressure,t)/(rs*n))==0
    slope=5*B*t/(3+2*t)
    checks['exact_log_pressure_slope']=s.simplify(s.diff(pressure,t)/(s.diff(n,t)/n)-slope)==0
    # Reference logotropic equation, independently solved, not a fixed regression constant.
    eps=1e-7
    def rhs(r,y):
        th,der=y
        return [der,1/th-2*der/r]
    def quarter(r,y):
        return y[0]-4
    quarter.terminal=True
    quarter.direction=1
    ref=solve_ivp(rhs,(eps,10),[1+eps**2/6,eps/3],rtol=2e-12,atol=2e-14,events=quarter)
    assert ref.success and len(ref.t_events[0])==1
    xi=float(ref.t_events[0][0])
    checks['log_core_reference']=abs(xi-5.84477267596)<1e-9
    states=(.2,.5,.8,.95,.99,.999,.9999)
    rows=[solve_core(pc,2e-10) for pc in states]
    tighter=[solve_core(pc,2e-12) for pc in (.2,.95,.9999)]
    checks['all_seven_finite_edges']=all(r['radius_over_ell']<30 and r['mass_dimensionless']>0 and r['edge_slope']<0 for r in rows)
    checks['independent_mass_integrals']=max(r['mass_quadrature_relative_error'] for r in rows)<2e-6
    deviations=[]
    for fine in tighter:
        row=next(r for r in rows if r['psi_c']==fine['psi_c'])
        deviations.extend(abs(row[k]/fine[k]-1) for k in ('radius_over_ell','mass_dimensionless','quarter_column_coefficient'))
    checks['three_tolerance_refinements']=max(deviations)<2e-6
    checks['finite_high_density_core_approach']=abs(rows[-1]['quarter_column_coefficient']/xi-1)<.001
    # This is a finite discriminator, not a proof of monotonicity for all states.
    last_errors=[abs(r['quarter_column_coefficient']/xi-1) for r in rows[-4:]]
    checks['four_finite_convergence_errors_decrease']=all(a>b for a,b in zip(last_errors,last_errors[1:]))
    checks={k:bool(v) for k,v in checks.items()}
    result={'claim_id':'PN28_HALO','checks':checks,'reference_xi_quarter':xi,'states':rows,
            'max_tolerance_refinement_change':max(deviations),
            'finite_high_density_fractional_error':last_errors[-1],
            'non_claims':['No full scalar-gradient halo', 'No formation or stability proof',
                          'No empirical fit or predicted vacuum ratio',
                          'Finite convergence checks supplement the written asymptotic proof']}
    assert all(checks.values()),checks
    Path(sys.argv[1]).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
