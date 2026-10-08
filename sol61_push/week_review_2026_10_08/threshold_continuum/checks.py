#!/usr/bin/env python3
"""Bounded numerical examples for the continuum-coupling theorem."""
import argparse
import json
import math
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from scipy.special import beta as beta_fn, betainc

p = argparse.ArgumentParser()
p.add_argument("--output", required=True)
p.add_argument("--mutate", choices=["none", "omit_continuum", "omit_filter"], default="none")
args = p.parse_args()
checks, rows = [], []
A = (2 * math.pi / math.sqrt(3)) ** .75

def check(name, value):
    checks.append({"name": name, "passed": bool(value)})

def integral(e, d, alpha, b):
    # E=D^(3/2) u^3, u=exp(t). This resolves the moving threshold.
    k = b * d ** ((3 * alpha - 1) / 2)
    if args.mutate == "omit_continuum":
        k = 0.0
    def f(t):
        u = math.exp(t)
        a = u**3 + e
        shift = k * u**(3*alpha)
        return 1.5 * u*u * (1/(a-shift) + 1/(a+shift))
    val, err = quad(f, -40, -.5*math.log(d), epsabs=2e-10, epsrel=2e-10, limit=250)
    return val, err

def root(d, alpha, b):
    if alpha < 1:
        m = (1-alpha)*alpha**(alpha/(1-alpha))*(b*d)**(1/(1-alpha))
    else:
        m = 0.
    low = max(m/d**1.5 * 1.00001, 1e-5)
    hi = max(2*A, low*2)
    while hi-integral(hi,d,alpha,b)[0] < 0:
        hi *= 2
    e = brentq(lambda x: x-integral(x,d,alpha,b)[0],low,hi,xtol=2e-12)
    val, err = integral(e,d,alpha,b)
    check("root_residual_{}_{}".format(alpha,d), abs(e-val)<2e-8 and err<2e-8)
    return e

def unperturbed(d, c=1):
    # Exact complementary incomplete-beta representation, independent of log quadrature.
    def integ(eps):
        return c**(-2/3)*eps**(-1/3)*beta_fn(2/3,1/3)*(1-betainc(1/3,2/3,eps/(c+eps)))
    eps = brentq(lambda r:r-d**.5*integ(r*d**1.5), .01, 10,xtol=1e-12)
    return eps

for d in [1e-2,1e-4,1e-6,1e-8,1e-10]:
    base = unperturbed(d)
    check("baseline_quadrature_{}".format(d), abs(integral(base,d,.5,0)[0]-base)<2e-8)
    for alpha in [.5,1.]:
        e=root(d,alpha,1.)
        check("paired_coupling_increases_response_{}_{}".format(alpha,d), e>=base-2e-10)
        if alpha==1:
            lo,hi=unperturbed(d,1+d),unperturbed(d,1-d)
            check("alpha_one_form_squeeze_{}".format(d),lo-2e-9<=e<=hi+2e-9)
        if d==1e-10:
            check("safe_coefficient_{}".format(alpha),abs(e/A-1)<1e-4)
        rows.append({"D":d,"alpha":alpha,"epsilon_over_D_three_halves":e,"ratio_to_A":e/A})

# Critical coefficient: independent integration directly on u in (0,infinity).
mcrit=2/(3**1.5)
def crit_integral(e):
    def f(u):
        return 1.5*u*(1/(u**3-u+e)+1/(u**3+u+e))
    return quad(f,0,np.inf,epsabs=1e-11,epsrel=1e-11,limit=250)[0]
critical=brentq(lambda e:e-crit_integral(e),mcrit*1.01,10,xtol=1e-12)
check("critical_coefficient_strictly_changes",critical>A*1.01)
for d in [1e-4,1e-8,1e-10]:
    e=root(d,1/3,1)
    check("critical_not_unperturbed_{}".format(d),e>A*1.005)
    if d==1e-10:
        check("critical_independent_integral",abs(e-critical)<1e-4)
    rows.append({"D":d,"alpha":1/3,"epsilon_over_D_three_halves":e,"ratio_to_A":e/A})

# Exact continuum trial minimum. Does not claim an eigenstate or numerical root.
mins=[]
for d in [1e-2,1e-4,1e-6,1e-8]:
    alpha=.2
    estar=(alpha*d)**(1/(1-alpha))
    m=(1-alpha)*alpha**(alpha/(1-alpha))*d**(1/(1-alpha))
    check("subcritical_minimum_{}".format(d),abs((estar-d*estar**alpha)+m)<1e-14 and estar<1)
    mins.append(m/d**1.5)
check("subcritical_overwhelms",mins[-1]>10 and all(b>a for a,b in zip(mins,mins[1:])))

# Noncommuting matrix surrogate for source repair and its form bound.
energies=np.array([1e-12,1e-6,.02,1.,10.])
K=np.diag(energies)
B=np.array([[1,.2,-.1,.3,0],[.2,-.5,.4,0,.1],[-.1,.4,.7,.2,0],
            [.3,0,.2,-.3,.2],[0,.1,0,.2,.9]])
v=np.array([.2,.4,.1,.3,.15])
norm=float(np.linalg.norm(B,2))
Ec=.7
F=np.diag(np.sqrt(energies/(energies+Ec)))
if args.mutate=="omit_filter":
    F=np.eye(len(energies))
BF=F@B@F
repaired=np.zeros((6,6))
repaired[0,1:]=v
repaired[1:,0]=v
repaired[1:,1:]=BF
check("transition_vector_preserved",np.array_equal(repaired[1:,0],v))
check("continuum_not_zero",np.linalg.norm(BF)>1e-3)
check("example_noncommuting",np.linalg.norm(K@B-B@K)>1e-3)
check("upper_form_bound",np.linalg.eigvalsh(norm/Ec*K-BF).min()>-1e-12)
check("lower_form_bound",np.linalg.eigvalsh(norm/Ec*K+BF).min()>-1e-12)
# Generalized eigenvalues are a scale-sensitive cross-check of the same bound.
Ki=np.diag(1/np.sqrt(energies))
check("relative_bound",max(abs(np.linalg.eigvalsh(Ki@BF@Ki)))<=norm/Ec*(1+1e-12))

# SU(3) ray calculation, and the optimized scalar Young bound.
ray=[]
for R in [1,10,100,1000]:
    value=18*R**3/(1+14*R**2)**1.5
    ray.append(value)
check("SU3_ray_limit",abs(ray[-1]-18/14**1.5)<1e-7)
for alpha in [.2,1/3,.5,.8]:
    d,delta=.003,.07
    xstar=(alpha*d/delta)**(1/(1-alpha))
    rem=(1-alpha)*alpha**(alpha/(1-alpha))*d**(1/(1-alpha))*delta**(-alpha/(1-alpha))
    check("Young_bound_saturation_{}".format(alpha),abs(d*xstar**alpha-delta*xstar-rem)<1e-14)
    for x in [xstar/10,xstar*10]:
        check("Young_bound_off_max_{}_{}".format(alpha,x),d*x**alpha-delta*x<=rem+1e-14)

result={"mutate":args.mutate,"passed":all(c["passed"] for c in checks),
        "checks":checks,"summary":{"total":len(checks),"failed":sum(not c["passed"] for c in checks)},
        "A":A,"critical_coefficient":critical,"rows":rows,
        "subcritical_lower_bound_ratios":mins,"SU3_ray_values":ray,
        "non_claims":["No BFSS spectral calculation","No proof by finite numerics","No physical coefficient selection"]}
out=Path(args.output)
out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result["summary"]))
raise SystemExit(0 if result["passed"] else 1)
