#!/usr/bin/env python3
"""Exact safe constants for the total simple-nu phantom tidal bound."""
import argparse
import ast
from fractions import Fraction as F
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT/'rebuild_2026_10_22'


def literal_assignment(path, name):
    for node in ast.parse(path.read_text()).body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target,ast.Name) and target.id==name:
                return ast.literal_eval(node.value)
            if isinstance(target,ast.Tuple):
                names=[x.id for x in target.elts]
                if name in names:
                    return ast.literal_eval(node.value)[names.index(name)]
    raise ValueError(name)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path)
    args=ap.parse_args()
    source=BASE/'KT33_reciprocal_filter/cassini/cassini_v2.py'
    p4=BASE/'P4_v3_galaxy_tiles/p4_solver.py'
    a0code=literal_assignment(source,'A0')
    ceiling_code=literal_assignment(source,'CEILING')
    kpc_code=literal_assignment(p4,'KPC')
    pi_lower=4*sum((F(1 if k%2==0 else -1,2*k+1) for k in range(64)),F(0))
    c0_bound=F(2,3)*F(4,5)*F(23,4)
    checks=dict(pi_lower_gt_25over8=pi_lower>F(25,8),
                sqrt33_lt_23over4=F(33)<F(23,4)**2,
                C0_bound_equals_46over15=c0_bound==F(46,15),
                Q2_bound_equals_92over15=2*c0_bound==F(92,15))
    # Lower denominator and upper numerator include intended decimals and
    # the exact binary64 input represented by the inspected source constants.
    kpc=min(F('3.085677581491367e19'),F(kpc_code))
    ceiling=min(F('5.2e-27'),F(ceiling_code))
    rows=[]
    for foot,dec in [('canonical','9.3603e-11'),('alt','1.1312e-10')]:
        a0=max(F(dec),F(a0code[foot]))
        for length in [F('2.5'),F(3),F('3.5')]:
            q_upper=F(92,15)*a0/(length*kpc)
            ratio=q_upper/ceiling
            assert ratio<F(1,500)
            if length==3:assert ratio<F(3,2000)
            rows.append(dict(footing=foot,ell_kpc=str(length),
                a0_upper_exact=str(a0),Q2_upper_exact=str(q_upper),
                Q2_upper_s_minus2=float(q_upper),ratio_upper_exact=str(ratio),
                ratio_upper=float(ratio)))
    result=dict(assertion_tested='Exact rational constants for total phantom projected quadrupole |Q2|<(92/15)a0/ell under whole-space simple-nu universal Gaussian law',
        outcome='exact rational arithmetic verified; analytic derivation separate',
        pi_lower_exact=str(pi_lower),kpc_lower_exact=str(kpc),ceiling_lower_exact=str(ceiling),
        checks=checks,all_checks_pass=all(checks.values()),rows=rows,
        non_claims=['ordinary Newtonian tide bound','ephemeris likelihood','Milky Way numerical pass','general interpolation function'])
    assert result['all_checks_pass']
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
