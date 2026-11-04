"""Exact rational monotonicity certificate: p=63/10, t>=3163/2000."""
import argparse,json
from fractions import Fraction as F
from pathlib import Path
from monotonicity_exact import root_bounds,exp_bounds

POWER=F(63,10)
SCALE=F(3163,2000)


def excess_bounds(z):
    rlo,rhi=root_bounds(z,POWER.numerator)
    low=rlo**POWER.denominator;high=rhi**POWER.denominator
    slo,_=root_bounds(1+4/(SCALE*high),2)
    _,shi=root_bounds(1+4/(SCALE*low),2)
    return (slo-1)/2,(shi-1)/2


def lower(a,b):
    _,shi=excess_bounds(a);slo,_=excess_bounds(b)
    elo,_=exp_bounds(b)
    m=F(1) if a<=1<=b else (b if b<1 else a)
    _,ehi=exp_bounds(m)
    return 1+elo*slo*slo/(2*slo+1)-POWER*m*ehi*shi


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    start=1/(2*POWER);end=F(10);step=F(1,500);x=start;n=0;minimum=F(1);worst=None
    while x<end:
        b=min(x+step,end);bound=lower(x,b)
        assert bound>0,f'nonpositive lower bound on{x},{b}'
        if bound<minimum:minimum=bound;worst=[str(x),str(b)]
        n+=1;x=b
    exact_count=(end-start)/step
    expected=(exact_count.numerator+exact_count.denominator-1)//exact_count.denominator
    assert n==expected and x==end
    short=F(minimum.numerator*10**6//minimum.denominator,10**6)
    assert 0<short<=minimum
    out=dict(power=str(POWER),minimum_scale=str(SCALE),domain=[str(start),str(end)],
             interval_count=n,uniform_compact_lower_bound=str(short),minimum_exact_fraction=str(minimum),
             worst_interval=worst,all_lower_bounds_strictly_positive=True,
             scope='Exact compact certificate plus FRACTIONAL_MONOTONICITY_PROOF.md implies monotonicity for all y>0 and t>=3163/2000 at p63/10; not full stability')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n')
    print('exact intervals',n,'uniform compact lower bound',short,'worst',worst,flush=True)


if __name__=='__main__':main()
