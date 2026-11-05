"""Exact rational interval proof for cutoff p=6, t>=3/2; no floating arithmetic.

The reduction, exponential enclosures and analytic tails are in
MONOTONICITY_PROOF.md. This script proves the remaining compact interval.
"""
import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path

ROOT_SCALE=10**10
EXP_N=128


def integer_nth_root(n,k):
    if n<0 or k<1:raise ValueError('nonnegative integer and positive order required')
    if n==0:return 0
    lo=0;hi=1<<((n.bit_length()+k-1)//k)
    while hi-lo>1:
        mid=(lo+hi)//2
        if mid**k<=n:lo=mid
        else:hi=mid
    return lo


def root_bounds(x,k):
    """Adjacent decimal rationals enclosing the exact positive kth root."""
    scaled=x.numerator*ROOT_SCALE**k//x.denominator
    n=math.isqrt(scaled) if k==2 else integer_nth_root(scaled,k)
    low=F(n,ROOT_SCALE);high=F(n+1,ROOT_SCALE)
    assert low**k<=x<high**k
    return low,high


def excess_bounds(z):
    rlo,rhi=root_bounds(z,6)
    innerlo=1+4/(F(3,2)*rhi);innerhi=1+4/(F(3,2)*rlo)
    slo,_=root_bounds(innerlo,2);_,shi=root_bounds(innerhi,2)
    return (slo-1)/2,(shi-1)/2


def exp_bounds(z):
    assert 0<=z<EXP_N
    return (1-z/EXP_N)**EXP_N,(1+z/EXP_N)**(-EXP_N)


def interval_lower(a,b):
    _,s_upper=excess_bounds(a);s_lower,_=excess_bounds(b)
    e_lower,_=exp_bounds(b)
    maximizer=F(1) if a<=1<=b else (b if b<1 else a)
    _,e_upper=exp_bounds(maximizer)
    positive=e_lower*s_lower*s_lower/(2*s_lower+1)
    negative=6*maximizer*e_upper*s_upper
    return 1+positive-negative


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args()
    for k in [2,3,6]:
        for n in [0,1,2,10,100]:
            assert integer_nth_root(n**k,k)==n
            if n:assert integer_nth_root(n**k-1,k)==n-1
    start=F(1,12);end=F(10);step=F(1,500)
    a=start;n=0;minimum=F(1);worst=None
    while a<end:
        b=min(a+step,end);bound=interval_lower(a,b)
        assert bound>0, f'nonpositive exact lower bound on {a},{b}'
        if bound<minimum:minimum=bound;worst=[str(a),str(b)]
        n+=1;a=b
    assert a==end and n==4959
    # A smaller short rational is more readable and remains an exact claim.
    displayed=F(minimum.numerator*10**6//minimum.denominator,10**6)
    assert 0<displayed<=minimum
    result=dict(assertion_tested='Exact rational lower bounds for d[y nu(y)]/dy at p6 t=3/2 on z in[1/12,10]',
                interval_count=n,domain=[str(start),str(end)],step=str(step),
                endpoint_coverage_exact=True,all_lower_bounds_strictly_positive=True,
                uniform_compact_lower_bound=str(displayed),worst_interval=worst,
                minimum_exact_fraction=str(minimum),root_scale=ROOT_SCALE,exponential_power=EXP_N,
                tail_reduction='Analytic proof in MONOTONICITY_PROOF.md extends to every y>0,t>=3/2',
                non_claims=['Not a dynamical or relativistic stability theorem','Not an observational pass'])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print('exact intervals',n,'uniform compact lower bound',displayed,'worst',worst,flush=True)


if __name__=='__main__':main()
