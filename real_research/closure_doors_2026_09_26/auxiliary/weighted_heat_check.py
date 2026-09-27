#!/usr/bin/env python3
"""Weighted auxiliary convexity: explicit counterexample and constructive repair.

Periodic x in [0,2pi]. S=exp(b d_xx). N>0 is an independent fixed lapse.
Exact Fourier identities plus deterministic quadrature/eigenvalue checks.
No inference of full physical-time hyperbolicity or of an on-shell spacetime.
"""
import argparse
import json
from pathlib import Path
import math
import numpy as np
import sympy as sp


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    args=ap.parse_args(); checks={}
    def exact(name, expr):
        r=sp.simplify(expr); assert r==0,(name,r)
        checks[name]={'passed':True,'residual':str(r)}
    def bounded(name, value, ok):
        assert bool(ok),(name,value)
        checks[name]={'passed':True,'measured':value}

    # f=sin x - sin(10x)/50, N=1+(4/5)cos(9x): exact integrals / pi.
    t=sp.symbols('t',real=True)
    energy=sp.exp(-2*t)+sp.exp(-200*t)/25-sp.Rational(4,25)*sp.exp(-101*t)
    exact('weighted_initial_energy_over_pi',energy.subs(t,0)-sp.Rational(22,25))
    exact('weighted_heat_increases_energy_initially',sp.diff(energy,t).subs(t,0)-sp.Rational(154,25))
    uniform=sp.exp(-2*t)+sp.exp(-200*t)/25
    exact('uniform_lapse_control_derivative',sp.diff(uniform,t).subs(t,0)+10)
    bounded('finite_positive_time_counterexample',float(energy.subs(t,sp.Rational(1,1000))),
            float(energy.subs(t,sp.Rational(1,1000)))>22/25+0.005)

    # Exact exponential inverse, bisection in x in [0,2] (t<=t(2)).
    def inv_source(s):
        lo=np.zeros_like(s); hi=np.full_like(s,2.)
        for _ in range(58):
            mid=(lo+hi)/2; f=mid*(-np.expm1(-mid))
            mask=f<s; lo=np.where(mask,mid,lo); hi=np.where(mask,hi,mid)
        return (lo+hi)/2
    rows=[]; b=0.02; s2=2*(-math.expm1(-2))
    for n in [2048,4096,8192,16384]:
        x=2*math.pi*(np.arange(n)+0.5)/n
        N=1e-8+np.exp(1000*(np.cos(x)-1))
        vp=np.cos(x)-np.cos(10*x)
        Svp=math.exp(-b)*np.cos(x)-math.exp(-100*b)*np.cos(10*x)
        # SU_base' = t(2)cos x. U_base = exp(b)t(2)sin x.
        xx=inv_source(np.abs(s2*np.cos(x)))
        C=(1-xx)/(np.expm1(xx)+xx)
        first=2*math.pi*np.mean(N*vp**2)
        filtered=2*math.pi*np.mean(N*Svp**2)
        hess=4*2*math.pi*np.mean(N*(vp**2+C*Svp**2))
        rows.append({'n':n,'unfiltered_energy':float(first),
                     'filtered_energy':float(filtered),'ratio':float(filtered/first),
                     'exact_exponential_energy_second_variation':float(hess)})
    bounded('actual_exponential_nonconvex_fixed_lapse_example',rows,
            all(r['exact_exponential_energy_second_variation'] < -0.015 for r in rows))
    bounded('quadrature_refinement_control',abs(rows[-1]['exact_exponential_energy_second_variation']-rows[-2]['exact_exponential_energy_second_variation']),
            abs(rows[-1]['exact_exponential_energy_second_variation']-rows[-2]['exact_exponential_energy_second_variation'])<1e-8)

    # Repair: S_N=e^{-b M^-1 K}, M=diag(N), K=D^T N_edge D.
    n=48; x=2*math.pi*np.arange(n)/n; dx=2*math.pi/n
    N=np.exp(2*np.cos(x)); edge=np.exp(2*np.cos(x+dx/2))
    D=(np.roll(np.eye(n),-1,axis=1)-np.eye(n))/dx
    K=D.T@np.diag(edge)@D
    sq=np.sqrt(N); isq=1/sq
    H=isq[:,None]*K*isq[None,:]
    vals,V=np.linalg.eigh(H); vals=np.maximum(vals,0)
    S=isq[:,None]*((V*np.exp(-b*vals))@V.T)*sq[None,:]
    contract=K-S.T@K@S
    scale=np.linalg.norm(K,2)
    mn=float(np.linalg.eigvalsh((contract+contract.T)/2).min())
    bounded('lapse_adapted_filter_Dirichlet_contraction',{'min_eigenvalue':mn,'scale':float(scale)},mn>-1e-10*scale)
    C=-np.ones(n)/8 # conservative exact exponential lower bound
    Hess=K+S.T@D.T@np.diag(edge*C)@D@S
    gap=Hess-sp.Rational(7,8).__float__()*K
    mg=float(np.linalg.eigvalsh((gap+gap.T)/2).min())
    bounded('repaired_auxiliary_lower_bound_7_over_8',mg,mg>-1e-10*scale)
    bounded('weighted_self_adjointness',float(np.max(np.abs(N[:,None]*S-S.T*N[None,:]))),
            np.max(np.abs(N[:,None]*S-S.T*N[None,:]))<1e-10)

    # Algebra behind corrected original-filter bound, Cmin=-1/8.
    ratio=sp.symbols('r_N',positive=True)
    exact('corrected_lower_bound_factor',1-ratio/8-(8-ratio)/8)
    xvar=sp.symbols('x',positive=True)
    CL=(1-xvar)/(sp.exp(xvar)+xvar-1)
    exact('exponential_CL_minimum_derivative',sp.diff(CL,xvar)-sp.exp(xvar)*(xvar-2)/(sp.exp(xvar)+xvar-1)**2)
    output={'result':'weighted-contraction counterexample, lapse-dependent bound, and weighted-filter repair verified in stated scope',
            'checks':checks,'counterexample_domain':'flat closed circle (or T3 with fields depending only on x); positive prescribed lapse; no full field equations imposed',
            'exact_results':{'counterexample_Eprime_over_pi':'154/25 > 0',
                             'original_filter_convexity_sufficient':'Nmax/Nmin < e^2+1 (or simpler <8)',
                             'modified_filter':'Delta_N=N^-1 D_i(N D^i); S_N=exp(b Delta_N)',
                             'modified_filter_convexity_lower_bound':'4(1-1/(e^2+1)) ||D v||_N^2 for exact exponential kernel'},
            'non_claims':['No full metric/clock well-posedness','No proof empirical gates survive filter replacement',
                          'Finite binary64 quadrature/eigenvalue examples supplement the exact continuum argument',
                          'Negative Hessian at an off-shell prescribed lapse is not itself a physical ghost']}
    p=Path(args.output);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))

if __name__=='__main__': main()
