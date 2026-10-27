#!/usr/bin/env python3
"""Bounded exact checks for the uniform charged-exterior hand proof."""
import json
from pathlib import Path
import sympy as s

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'runs/exterior-001/results.json'
x=s.symbols('x',positive=True)
n,d,z=s.symbols('n d z',positive=True)
k=s.symbols('k',integer=True,positive=True)
checks=[]

def check(name,condition):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)

examples=[]
for ell in range(1,31):
    C=ell*(ell+1)
    coeff=[s.S.One]
    for j in range(1,ell):
        coeff.append(s.factor(coeff[-1]*(j*(j+1)-C)/(2*j)))
    f=sum(a/x**j for j,a in enumerate(coeff))
    # Equation after factoring e^x/x, avoiding expansion of exponentials.
    residual=s.diff(f,x,2)+(2-2/x)*s.diff(f,x)+(2-C)*f/x**2
    check(f'exact_growing_polynomial_l{ell}',s.simplify(residual)==0)
    check(f'termination_l{ell}',ell*(ell+1)-C==0)
    for j,a in enumerate(coeff):
        closed=(-1)**j*s.factorial(ell-1)*s.factorial(ell+j+1)/(s.factorial(ell-j-1)*s.factorial(ell+1)*2**j*s.factorial(j))
        check(f'factorial_coefficient_l{ell}_n{j}',s.simplify(a-closed)==0)
    if ell<=5:
        examples.append({'ell':ell,'C':C,'f':str(s.expand(f))})

# Algebra supporting the analytic product and infinite-series inequalities.
sum_subtraction=s.summation(k*(k+1)-2,(k,1,n))
check('product_subtraction_sum',s.simplify(sum_subtraction-n*(n-1)*(n+4)/3)==0)
F=s.exp(z)
D=lambda a:s.expand(z*s.diff(a,z))
moment=D(D(D(F)))+3*D(D(F))-4*D(F)
check('Poisson_moment',s.simplify(moment-s.exp(z)*(z**3+6*z**2))==0)
for ell in range(2,31):
    C=ell*(ell+1)
    # This proves the last vanishing factor forces the tail bound >=1;
    # monotonicity in n thereafter is an elementary positive polynomial fact.
    at_termination=s.Rational(ell*(ell-1)*(ell+4),3*(C-2))
    check(f'termination_tail_bound_l{ell}',at_termination>=1)
    check(f'coefficient_factors_in_unit_interval_l{ell}',all(0<=1-s.Rational(j*(j+1)-2,C-2)<=1 for j in range(1,ell)))

J,N=s.symbols('J N',integer=True,positive=True)
C=J*(J+1)
cm=J*(J-1)
cp=(J+1)*(J+2)
check('exterior_Gaussian_a1',s.simplify(((cm-2)+(cp-2))/2-(C-1))==0)
sumC=s.summation((2*J+1)*J*(J+1),(J,2,N))
sumA=s.summation((2*J+1)*(J*(J+1)-1),(J,2,N))
check('summed_C_bound_polynomial',s.simplify(sumC-(N*(N+1)**2*(N+2)/2-6))==0)
check('finite_cutoff_A_formula',s.simplify(sumA-((N+1)**4-3*(N+1)**2)/2+2)==0)

OUT.parent.mkdir(parents=True,exist_ok=True)
result={'status':'all-exact-checks-passed','number_checks':len(checks),'checks':checks,
        'finite_ell_range':[1,30],'examples':examples,
        'product_subtraction_sum':str(s.factor(sum_subtraction)),
        'Poisson_moment':str(s.factor(moment)),
        'sum_weighted_C_J2_N':str(s.factor(sumC)),
        'sum_weighted_a1_J2_N':str(s.factor(sumA)),
        'interpretation':'Supports the analytic uniform inequality; does not prove a J-uniform regular-origin connection bound, full angular determinant or physical matching.'}
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'number_checks':len(checks),'ell_range':[1,30],'output':str(OUT)}))
