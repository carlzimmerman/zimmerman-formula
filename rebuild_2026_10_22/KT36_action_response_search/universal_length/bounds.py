#!/usr/bin/env python3
"""Exact rational slack for the universal-length Solar quadrupole bound."""
import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    gm = F('6.6743e-11')*F('1.98892e30')
    kpc = F('3.085677581491367e19')
    ceiling = F('5.2e-27')
    # c<4/5 follows from pi>25/8; all remaining comparisons are rational.
    kk = F(2,3)*F(4,5)*F(23,4)*F(13,20)
    checks = {
        'sqrt33_lt_23over4': F(33) < F(23,4)**2,
        'cube_root_c_over3_lt_13over20': F(4,15) < F(13,20)**3,
        'K_bound_equals_299over150': kk == F(299,150),
        'K_lt2': kk < 2,
        'fourth_root_5_lt_3over2': F(5) < F(3,2)**4,
        'combined_hessian_constant_lt3': kk*F(3,2) < 3,
        'projected_Q2_constant_lt6': 2*kk*F(3,2) < 6,
    }
    rows = []
    for foot, a0s in [('canonical','9.3603e-11'), ('alt','1.1312e-10')]:
        a0 = F(a0s)
        radical = gm*a0
        upper = math.isqrt(radical.numerator//radical.denominator)+1
        assert F(upper)**2 > radical
        for length in [F('2.5'), F(3), F('3.5')]:
            ell = length*kpc
            ratio = 6*F(upper)/(ell*ell*ceiling)
            assert ratio < F(1,10000000)
            # A rational lower epsilon certifies the inherited45/epsilon^3 bound.
            eps_squared = ell*ell*a0/gm
            eps_lower = math.isqrt(eps_squared.numerator//eps_squared.denominator)
            assert F(eps_lower)**2 <= eps_squared and eps_lower >= 4
            constant_field_ratio = F(45,eps_lower**3)
            rows.append(dict(footing=foot,ell_kpc=str(length),
                solar_rM_m=math.sqrt(float(gm/a0)),
                epsilon_sun=math.sqrt(float(eps_squared)),
                epsilon_integer_lower=eps_lower,
                sqrt_GM_a0_integer_upper=upper,
                arbitrary_background_Q2_over_ceiling_upper=float(ratio),
                arbitrary_background_upper_exact=str(ratio),
                uniform_external_Q2_over_ceiling_upper=float(constant_field_ratio),
                uniform_external_upper_exact=str(constant_field_ratio)))
    result = dict(claim='incremental Solar anomalous trace-free quadrupole only',
        constants=dict(GM_exact=str(gm),KPC_exact=str(kpc),ceiling_exact=str(ceiling)),
        checks=checks,rows=rows,all_checks_pass=all(checks.values()),
        outcome='exact rational slack verified; analytic derivation in README',
        not_claimed=['total Galactic tide bound','full ephemeris fit',
                     'Milky Way or dwarf observational pass'])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2))
    if not result['all_checks_pass']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
