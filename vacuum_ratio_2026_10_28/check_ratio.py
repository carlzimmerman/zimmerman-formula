"""VR28 exact identities and bounded central-halo discriminators.

Run through the recorded computation-audit contract; argv[1] is result JSON.
The exact arguments are in DERIVATION.md. Finite floats do not prove them.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import scipy
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq


def symbolic_checks():
    s = sp.symbols('s', real=True)
    d, V, B, K, F, M, q0 = sp.symbols('d V B K F M q0', positive=True)
    C, alpha, mu = sp.symbols('C alpha mu', real=True)
    q = sp.symbols('q', positive=True)
    U = V*(d*sp.exp(3*s)+sp.exp(-3*d*s))/(1+d)
    A = sp.diff(U, s)-3*U
    P = sp.diff(U, s)/3-U
    pn = V+B*(sp.exp(3*s)-3*s-1)
    Apn = sp.diff(pn, s)-3*pn
    Fg = M**2*sp.exp(alpha*s*s)
    UE = M**4*pn/Fg**2
    eps = mu*q+V+B*(q/q0-sp.log(q/q0)-1)
    p, z, ap, aq = sp.symbols('p z ap aq', nonzero=True, real=True)
    tw = ap*sp.exp(p*s)+aq*sp.exp(z*s)
    checks = {}

    def eq(name, expression):
        checks[name] = bool(sp.simplify(expression) == 0)

    eq('vacuum_height', U.subs(s, 0)-V)
    eq('vacuum_stationarity', sp.diff(U, s).subs(s, 0))
    eq('vacuum_stiffness_ratio', sp.diff(U, s, 2).subs(s, 0)-9*d*V)
    eq('multiplicative_response', sp.diff(A, s)+3*d*A)
    eq('full_pressure', P+V*sp.exp(-3*d*s))
    eq('scalar_stationarity', (-2*K*sp.exp(-2*s)+sp.diff(U,s)).subs(K,sp.diff(U,s)*sp.exp(2*s)/2))
    eq('vacuum_shift_stiffness_unchanged', sp.diff(U+C,s,2)-sp.diff(U,s,2))
    eq('vacuum_shift_changes_total_ratio', sp.diff(U+C,s,2).subs(s,0)/(9*(U+C).subs(s,0))-d*V/(V+C))
    eq('shift_breaks_full_scaling_equation', sp.diff(A-3*C,s)+3*d*(A-3*C)+9*d*C)
    eq('PN_response', Apn-(9*B*s-3*V))
    eq('PN_response_ratio', -sp.diff(Apn,s).subs(s,0)/(3*Apn.subs(s,0))-B/V)
    eq('two_exponential_curvature_identity', (sp.diff(tw,s,2)+p*z*tw).subs(s,0).subs(aq,-p*ap/z))
    eq('Einstein_frame_curvature', sp.diff(UE,s,2).subs(s,0)-(9*B-4*alpha*V))
    eq('minimal_mass_Hubble_ratio', (9*B/F**2)/(V/(3*M**2))-27*B*M**2/(V*F**2))
    eq('medium_vacuum_height', (eps-q*sp.diff(eps,q)).subs(q,q0)-V)
    eq('medium_chemical_equilibrium', sp.diff(eps,q).subs(q,q0)-mu)
    eq('medium_constant_bulk_modulus', q*q*sp.diff(eps,q,2)-B)
    eq('medium_PN_pressure', -eps+q*sp.diff(eps,q)+V-B*sp.log(q/q0))
    eq('medium_PN_potential', (eps-mu*q).subs(q,q0*sp.exp(3*s))-pn)
    eps2 = mu*q+V*(d*q/q0+(q/q0)**(-d))/(1+d)
    eq('medium_scaling_bulk', q*q*sp.diff(eps2,q,2)-d*V*(q/q0)**(-d))
    eq('medium_scaling_pressure', -eps2+q*sp.diff(eps2,q)+V*(q/q0)**(-d))
    eq('PN_limit_subtracted_potential', sp.limit((U-V).subs(V,B/d),d,0,dir='+')-B*(sp.exp(3*s)-3*s-1))
    return checks


def logn(d, logy):
    return logy+0.6*(math.log(-math.expm1(-(1+d)*logy))-math.log1p(d))


def psi(d, logy):
    return (-math.expm1(-(1+d)*logy)/(1+d))**0.4


def energy_min(d, rho):
    # B=1 and k=3/2, hence rho_star=1. Direct scalar minimization.
    K=1.5*rho**(5/3)
    def slope(s):
        return -2*K*math.exp(-2*s)+3/(1+d)*(math.exp(3*s)-math.exp(-3*d*s))
    s=brentq(slope,-20,20,xtol=1e-13,rtol=1e-14)
    u=math.expm1(3*s)-3*s if d==0 else (math.expm1(3*s)+math.expm1(-3*d*s)/d)/(1+d)
    return K*math.exp(-2*s)+u, s


def pressure_checks():
    rows=[]
    for d in [0,0.001,0.01,0.1,1]:
        for K in [0.01,1,1000,1000000]:
            rho=(K/1.5)**0.6
            E,s=energy_min(d,rho)
            step=2e-4*rho
            em2=energy_min(d,rho-2*step)[0]
            em1=energy_min(d,rho-step)[0]
            ep1=energy_min(d,rho+step)[0]
            ep2=energy_min(d,rho+2*step)[0]
            p_fd=rho*(em2-8*em1+8*ep1-ep2)/(12*step)-E
            p_exact=3*s if d==0 else -math.expm1(-3*d*s)/d
            density_error=abs(math.exp(logn(d,3*s))/rho-1)
            pressure_error=abs(p_fd-p_exact)/(1+abs(p_exact))
            rows.append({'delta':d,'K_over_B':K,'s':s,'density_relative_error':density_error,'pressure_scaled_error':pressure_error})
    return rows


def source(d,yc,v):
    ec=math.exp(-(1+d)*math.log(yc))
    u=0.4*(1+d)*ec/(1-ec)*v
    if u>=1:
        return 0.0
    # expm1/log1p avoid subtracting nearly equal numbers for tiny cores.
    logone=math.log1p(-u)
    denom=1-(1/ec-1)*math.expm1(2.5*logone)
    return math.exp(1.5*logone-math.log(denom)/(1+d))


def finite_core(d,yc,rtol=1e-10,atol=1e-12):
    z0=1e-6
    def rhs(z,w):
        return [w[1],source(d,yc,w[0])-2*w[1]/z]
    def edge(z,w):
        return source(d,yc,w[0])-0.25
    edge.terminal=True
    edge.direction=-1
    sol=solve_ivp(rhs,[z0,50],[z0*z0/6,z0/3],method='DOP853',rtol=rtol,atol=atol,events=edge,dense_output=True)
    assert sol.success and len(sol.t_events[0])==1, (d,yc,sol.message)
    z=float(sol.t_events[0][0]); v,vp=map(float,sol.y_events[0][0])
    mass_quad=quad(lambda x:x*x*source(d,yc,float(sol.sol(x)[0])) if x>=z0 else x*x,0,z,epsabs=1e-10,epsrel=2e-10)[0]
    mass_error=abs(mass_quad/(z*z*vp)-1)
    L=math.log(yc)
    def enthalpy_integrand(t):
        if t==0: return 2.5
        x=t**2.5
        return 2.5*t**1.5*math.exp(-d*x-logn(d,x))
    h_quad=quad(enthalpy_integrand,0,L**0.4,epsabs=1e-11,epsrel=1e-11)[0]
    h_error=abs(h_quad/(2.5*psi(d,L))-1)
    return {'delta':d,'y_c':yc,'density_c_over_rho_star':math.exp(logn(d,L)),
            'quarter_radius_zeta':z,'quarter_v':v,'core_column_over_sqrt_B_4piG':z*math.exp(-d*L/2),
            'mass_integral_relative_error':mass_error,'enthalpy_integral_relative_error':h_error,
            'quarter_event_error':abs(source(d,yc,v)-0.25),'solver_steps':len(sol.t),'rtol':rtol,'atol':atol}


def limiting_core(d):
    # Independent theta equation, not the finite-source implementation.
    z0=1e-6; target=4**(1+d)
    def rhs(z,w):
        return [w[1],(1+d)*w[0]**(-1/(1+d))-2*w[1]/z]
    def edge(z,w): return w[0]-target
    edge.terminal=True; edge.direction=1
    sol=solve_ivp(rhs,[z0,50],[1+(1+d)*z0*z0/6,(1+d)*z0/3],method='DOP853',rtol=2e-12,atol=2e-13,events=edge)
    assert sol.success and len(sol.t_events[0])==1
    return float(sol.t_events[0][0])


def main(path):
    checks=symbolic_checks()
    pressure=pressure_checks()
    checks['20_independent_energy_pressure_derivatives']=bool(max(r['pressure_scaled_error'] for r in pressure)<1e-6)
    checks['20_scalar_minimizers_match_density']=bool(max(r['density_relative_error'] for r in pressure)<1e-8)
    deltas=[0,0.001,0.01,0.1,1]
    limits={str(d):limiting_core(d) for d in deltas}
    cases=[]
    for d in deltas:
        for yc in [10,1000,1000000]:
            row=finite_core(d,yc)
            row['limiting_xi']=limits[str(d)]
            row['core_coefficient_fractional_error']=row['quarter_radius_zeta']/limits[str(d)]-1
            cases.append(row)
    refinements=[]
    for d in [0,0.1,1]:
        original=next(r for r in cases if r['delta']==d and r['y_c']==1000000)
        repeat=finite_core(d,1000000,rtol=2e-12,atol=2e-14)
        repeat['fractional_radius_change']=repeat['quarter_radius_zeta']/original['quarter_radius_zeta']-1
        refinements.append(repeat)
    checks['all_15_quarter_crossings']=len(cases)==15
    checks['independent_core_mass_quadrature']=bool(max(r['mass_integral_relative_error'] for r in cases)<1e-7)
    checks['independent_enthalpy_quadrature']=bool(max(r['enthalpy_integral_relative_error'] for r in cases)<1e-8)
    checks['all_quarter_event_residuals']=bool(max(r['quarter_event_error'] for r in cases)<1e-10)
    checks['five_high_density_core_limits']=bool(max(abs(r['core_coefficient_fractional_error']) for r in cases if r['y_c']==1000000)<1e-5)
    checks['three_tolerance_refinements']=bool(max(abs(r['fractional_radius_change']) for r in refinements)<5e-8)
    checks['delta_zero_matches_prior_xi']=abs(limits['0']-5.84477267596773)<2e-8
    comparisons=[]
    for d in deltas:
        errors=[abs(r['core_coefficient_fractional_error']) for r in cases if r['delta']==d]
        comparisons.append({'delta':d,'errors_by_increasing_y':errors,'decreasing':bool(errors[0]>errors[1]>errors[2])})
    checks['convergence_errors_decrease_in_five_families']=all(r['decreasing'] for r in comparisons)
    out={'claim_id':'VR28_RATIO','checks':checks,'pressure_checks':pressure,'limiting_coefficients':limits,
         'core_cases':cases,'refinements':refinements,'convergence':comparisons,
         'old_target_comparison_only':{'B_over_V_for_old_log_kappa_half':1/(4*math.pi*limits['0']**2),'note':'Computed after all cases. Not an input delta or a predicted value.'},
         'software':{'Python':sys.version.split()[0],'SymPy':sp.__version__,'NumPy':np.__version__,'SciPy':scipy.__version__},
         'non_claims':['No microscopic delta or vacuum offset selection','No physical gradient-controlled infinite-density limit','No full halo numerical solve or kinetic formation/stability','No novelty claim for negative-power/log limit','No formal or interval proof certification']}
    Path(path).write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'checks':checks,'limiting_coefficients':limits,'max_mass_error':max(r['mass_integral_relative_error'] for r in cases),'max_pressure_error':max(r['pressure_scaled_error'] for r in pressure)},indent=2))
    assert all(checks.values()),checks


if __name__=='__main__':
    main(sys.argv[1])
