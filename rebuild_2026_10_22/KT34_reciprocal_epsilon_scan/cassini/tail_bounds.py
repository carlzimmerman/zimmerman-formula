#!/usr/bin/env python3
"""Exact rational slack checks for the uniform Cassini upper bound, epsilon>=4.

The analytic inequalities are documented in README.md. This arithmetic checks
their constants; it is distinct from the numerical quadrupole integrations.
"""
import argparse
from fractions import Fraction as F
import importlib.util
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
SOURCE=ROOT/'rebuild_2026_10_22/KT33_reciprocal_filter/cassini/cassini_v2.py'
spec=importlib.util.spec_from_file_location('kt33_cassini_v2',SOURCE)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    i1=F(64,100)/75+F(8,10)*F(607,1000)
    i2=F(64,100)/225+F(1,3)
    k=F(77,100)*(F(62,100)*i1+F(135,100)*(i1+2*i2))
    checks={
        '4_over_3sqrt3_lt_.77':F(16,27)<F(77,100)**2,
        'A_one_lt_.62':F(224,100)**2>5,
        'three_over_sqrt5_lt_1.35':F(9,5)<F(135,100)**2,
        'exp_half_lower_series_gt_1000_over_607':sum(F(1,2)**j/math.factorial(j) for j in range(5))>F(1000,607),
        '31K_lt_45':31*k<45,
        '45_over_4cubed_lt_one':F(45,64)<1}
    out={'analytic_domain':'epsilon >= 1 for bound; epsilon >= 4 for guaranteed passing tail',
         'bound':'abs(Q2)/ceiling < 45/epsilon**3',
         'at_epsilon_4_upper_bound':float(F(45,64)),
         'rational_K_upper_bound':str(k),'rational_31K_upper_bound':str(31*k),
         'footings':{},'checks':checks}
    c=math.sqrt(2/math.pi)
    for foot,a0 in m.A0.items():
        eta=m.GEXT/a0; h=eta/2
        avec=.5+math.sqrt(.25+1/h)-1
        l=.5/(h*h*math.sqrt(.25+1/h))
        I1=c*c/75+c*math.exp(-.5); I2=c*c/225+1/3
        K=4/(3*math.sqrt(3))*(avec*I1+1.5*eta*l*(I1+2*I2))
        pref=1.5*a0/math.sqrt(m.GM/a0)/m.CEILING
        checks[foot+'|eta_ge_two']=F(str(m.GEXT))>=2*F(str(a0))
        checks[foot+'|physical_pref_lt_31']=F(9,4)*F(str(a0))**3 <31**2*F(str(m.GM))*F(str(m.CEILING))**2
        out['footings'][foot]={'eta':eta,'K_q_upper_bound':K,'prefactor_over_ceiling':pref,
            'ratio_coefficient_upper_bound':K*pref,'ratio_upper_bound_at_4':K*pref/64,
            'asymptotic_q_epsilon_cubed':-1/(45*math.sqrt(math.pi)*eta*math.sqrt(.25+1/eta))}
    out['all_checks_pass']=all(checks.values())
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
    print(json.dumps(out,indent=2))
    assert out['all_checks_pass']


if __name__=='__main__':main()
