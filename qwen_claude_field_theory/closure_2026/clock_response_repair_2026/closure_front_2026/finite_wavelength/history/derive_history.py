#!/usr/bin/env python3
"""Exact forward fixed-history sign reduction; no new parameter scan."""
import argparse
import importlib.util
import json
from pathlib import Path
import re
import sympy as s

HERE=Path(__file__).resolve().parent
BASE=HERE.parents[2]


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def derive():
    checks={}
    def check(name,expr):
        assert s.factor(s.cancel(expr))==0,(name,s.factor(expr))
        checks[name]=True
    m,j,H,gamma,R,v,O=s.symbols('m j H gamma R v O',positive=True)
    q=1/(1+m); U=m*q*j; d=m*j/2; Delta=m*m*j*q*q
    PX=U*d/Delta+3*gamma*q*H
    PXX=2*U*d*d/Delta**2
    W=U+2*gamma*q*q*R
    clock=W-2*q*q*d
    B0=j*(1+m)*(m+2)/m
    G=2*PX-2*W*d/clock-8*gamma*H*q+4*gamma*R-2*gamma**2*q**4
    K=2*PX+4*q*q*PXX-12*gamma*H*q+6*gamma**2*q**4
    compact=2*gamma*(2*R-H*q+j*R/(m*m*j+2*gamma*R)-gamma*q**4)
    check('canonical_G_factorization',G-compact)
    check('canonical_K_factorization',K-(B0-6*gamma*H*q+6*gamma**2*q**4))
    check('positive_clock_block',clock-q*q*(m*m*j+2*gamma*R))
    check('affine_versus_FLRW', (2*PX-2*W*d/clock-2*gamma**2*q**4)-(G+8*gamma*H*q-4*gamma*R))
    pcmod=load('prior_principal',BASE/'cubic_principal_audit/derive.py')
    facts,pc=pcmod.derive()
    assert facts['passed']
    substitutions={pc['gamma']:gamma,pc['q']:q,pc['H']:H,pc['qdot']:-R,
        pc['M2']:1,pc['B0']:B0,pc['S0']:Delta,pc['d']:d}
    check('independent_action_principal_G',pc['dust_restoring'].subs(substitutions)-compact)
    check('independent_action_principal_K',pc['kinetic'].subs(substitutions)-K)
    mp=3*m*(O*m+2*O+2*m*v+2*v)/(2*(m+2))
    vp=(v-1)*(9*O*m**3+42*O*m*m+66*O*m+36*O+6*m**3*v-4*m**3
        +18*m*m*v-20*m*m+24*m*v-32*m+12*v-16)/(2*(m+1)*(m+2)**2)
    u=3*m*v/(m+2)+3*m*O/(2*(m+1))
    check('flow_qdot_normalization',mp/(m+1)-u)
    check('upper_v_invariant',vp.subs(v,1))
    boundary=O*(9*m**3+42*m*m+66*m+36)-(m**3+11*m*m+20*m+10)
    check('lower_v_boundary',vp.subs(v,s.Rational(1,2))+boundary/(4*(m+1)*(m+2)**2))
    check('early_boundary_polynomial',boundary.subs(O,s.Rational(1,8))-(m**3-46*m*m-94*m-44)/8)
    check('late_boundary_polynomial',boundary.subs(O,s.Rational(1,9))-(-s.Rational(19,3)*m*m-s.Rational(38,3)*m-6))
    wlog=-3*(1-O)+mp/(m+2)
    check('coupled_w_upper_boundary',wlog.subs({O:1/(3*(m+2)),v:1})+5*(3*m+4)/(2*(m+2)**2))
    check('coupled_v_lower_boundary',vp.subs({v:s.Rational(1,2),O:1/(3*(m+2))})
        -(m**3+8*m*m+12*m+4)/(4*(m+1)*(m+2)**2))
    assert s.Rational(1,8)*(s.Rational(1,10)+2)==s.Rational(21,80)<s.Rational(1,3)
    checks['coupled_region_initial_value']=True
    check('m_log_growth_split',mp/m-(s.Rational(3,2)*O+3*(m+1)*v/(m+2)))
    invariant=j*m**4/(m+1)**2
    invariant_derivative=s.diff(invariant,m)*mp+s.diff(invariant,j)*(-3*j)
    check('history_invariant_log_derivative',invariant_derivative/invariant-(-3+6*v+3*O*(m+2)/(m+1)))
    check('initial_history_invariant',invariant.subs({j:s.Rational(1,10),m:s.Rational(1,10)})-s.Rational(1,121000))
    assert s.Rational(1,10)*s.Rational(3,2)**4<1
    assert 1/(1+7*s.Rational(3,2)**3)<s.Rational(1,9)
    assert s.Rational(2,5)**2<s.Rational(7,30)<s.Rational(4,15)<s.Rational(3,5)**2
    checks['exact_barrier_constants']=True
    # Rational comparison beta <= 2 gamma H q / lower(j).
    check('beta_history_bound',2*s.Rational(1,10**6)*s.Rational(3,5)*q*121000*m**4/(m+1)**2
        -s.Rational(363,2500)*m**4/(m+1)**3)
    assert s.Rational(363,2500)<s.Rational(3,20)
    assert s.Rational(1,10**6)/s.Rational(2,5)<s.Rational(1,100000)
    lo=3*m/(2*(m+2)); upper=3*m**4/(20*(m+1)**3)
    lower=2*lo-1+lo/(m*m+upper*lo)-s.Rational(1,100000)
    num=3*(2533320*m**6+10303237*m**5+9473074*m**4+1333000*m**3+2533120*m*m+8133280*m+4000000)
    den=100000*m*(m+2)*(40*m**4+209*m**3+360*m*m+280*m+80)
    check('normalized_positive_polynomial',lower-s.Rational(1,10)-num/den)
    assert all(c>0 for c in s.Poly(num,m).all_coeffs())
    assert all(c>=0 for c in s.Poly(den,m).all_coeffs())
    checks['positive_polynomial_coefficients']=True
    check('K_relative_subtraction_bound',6*s.Rational(1,10**6)*s.Rational(3,5)*q*121000*m**5/((m+1)**3*(m+2))
        -s.Rational(1089,2500)*m**5/((m+1)**4*(m+2)))
    assert all(c>0 for c in s.Poly(s.expand((m+1)**4*(m+2)-m**5),m).all_coeffs())
    checks['K_relative_polynomial_positive']=True
    # Exact algebraic bridge to the definitions actually compiled in Lean.
    lean=(HERE/'HistorySigns.lean').read_text()
    for name,expr in [('lowerU',lo),('upperBeta',upper),('positiveNumerator',num),('positiveDenominator',den)]:
        pattern=r'noncomputable def '+name+r' \(m : ℝ\) : ℝ :=\s*([^\n]+)'
        raw=re.search(pattern,lean).group(1)
        check('Lean_definition_'+name,s.sympify(raw.replace('^','**'),locals={'m':m})-expr)
    canonical=load('canonical_model',BASE/'nonlinear_evolution_2026/constitutive.py')
    model=canonical.Model(1,gamma=1e-6)
    rows=[]
    for time in (0,.1,1):
        b=model.background(time); jets=model.jets(time,b['q']**2,0)
        state=model.solution.sol(time)
        av,mv,vv=map(float,state); jv=.1/av**3; rv=-b['qdot']; hv=b['H']; qv=b['q']
        direct=2*jets['P_X']-2*jets['W']*jets['W_Y']/(jets['W']-2*qv*qv*jets['W_Y'])-8e-6*hv*qv+4e-6*rv-2e-12*qv**4
        reduced=2e-6*(2*rv-hv*qv+jv*rv/(mv*mv*jv+2e-6*rv)-1e-6*qv**4)
        assert abs(direct-reduced)<1e-13
        assert reduced>1e-6*hv*qv/5
        assert jv*mv**4/(mv+1)**2>=1/121000-1e-15
        rows.append(dict(t=time,a=av,m=mv,v=vv,G_direct=direct,G_reduced=reduced,
            normalized_G=reduced/(2e-6*hv*qv),absolute_bound=1e-6*hv*qv/5))
    return dict(checks=checks,exact_check_count=len(checks),prior_principal_checks=len(facts['checks']),
        numeric_alignment_controls=rows,formulae={'G':str(compact),'K':str(s.factor(K)),
            'lower_numerator':str(num),'lower_denominator':str(den),'invariant':str(invariant)},
        conclusion='G > gamma*H*q/5 > 0 throughout the maximal regular forward interval, by the recorded ODE invariant-region argument and pointwise rational bound.',
        limitations=['ODE first-exit and continuation argument is prose, not formalized in Lean.',
            'No past-history, finite-wavelength stability, CMB, sourced metric or asymptotic uniform gap claim.',
            'Three canonical Model points are consistency controls, not the proof of no crossing.'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path)
    args=parser.parse_args(); result=derive(); serialized=json.dumps(result,indent=2)+'\n'
    if args.output: args.output.write_text(serialized)
    print(serialized)
