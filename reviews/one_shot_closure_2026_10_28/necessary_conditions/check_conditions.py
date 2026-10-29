#!/usr/bin/env python3
"""Bounded, independent necessary-condition checks. No fits or source mutations."""
import ast
import csv
import json
import math
import sys
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
G, MSUN, KPC = 6.67430e-11, 1.98847e30, 3.0856775814913673e19
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}


def B(x):
    return math.log1p(x*x) + 2*math.log1p(x) - 2*math.atan(x)


def Bprime(x):
    return 4*x*x/((1+x)*(1+x*x))


def g_law(gn, a0):
    return (gn + math.sqrt(gn*gn + 4*a0*gn))/2


def mass_required(v_kms, r_kpc, a0):
    r = r_kpc*KPC
    g = (v_kms*1e3)**2/r
    gn = g*g/(g+a0)
    return gn*r*r/G/MSUN


def main():
    target = Path(sys.argv[1])
    # Extract only the pure B definition, avoiding X43's substantial import-time work.
    src = ROOT/'rebuild_2026_10_22/X43_collapse_core_floor/x43_collapse_core.py'
    tree = ast.parse(src.read_text())
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'B')
    pure = ast.Module(body=[node], type_ignores=[])
    ns = {'np': np}
    exec(compile(pure, str(src), 'exec'), ns)
    checks = {}
    errors = []
    for x in (.01, .1, 1., 10., 100.):
        b_integral = 4*quad(lambda t: t*t/((1+t)*(1+t*t)), 0, x,
                            epsabs=1e-13, epsrel=1e-12)[0]
        errors.append(abs(B(x)-b_integral)/b_integral)
        assert abs(float(ns['B'](x))-B(x)) < 1e-12
    checks['burkert_mass_vs_density_integral'] = max(errors) < 1e-9
    peak = brentq(lambda x: x*Bprime(x)-2*B(x), .7, 1.5, xtol=1e-14)
    cap = B(peak)/(2*peak*peak)
    y_limit = cap*cap/(1-cap)
    checks['root_stationary'] = abs(peak*Bprime(peak)-2*B(peak)) < 1e-13
    checks['cap_below_exact_one_third_bound'] = cap < 1/3
    checks['inverse_extra_acceleration'] = abs((g_law(y_limit, 1)-y_limit)-cap) < 1e-13
    # Unique maximum is established analytically in RESULT.md, not by this grid.
    grid = np.geomspace(.01, 1e5, 500)
    checks['finite_grid_below_cap'] = all(B(float(x))/(2*x*x) <= cap+1e-13 for x in grid)
    checks['simple_law_identity'] = all(abs(g_law(y,1)**2-y*(g_law(y,1)+1)) < 1e-11
                                         for y in (.001, .01, .1, 1., 10.))
    floor = dict(x_peak=peak, max_g_h_over_a0=cap, maximum_y_for_exact_simple_law=y_limit,
                 numerical_mass_integral_max_relative_error=max(errors),
                 exact_conservative_cap=1/3, exact_conservative_y_limit=1/6,
                 at_y_one_required_extra=g_law(1,1)-1,
                 at_y_one_max_total=1+cap, at_y_one_required_total=g_law(1,1))
    source = json.loads((HERE/'SOURCES.json').read_text())['sources'][0]['extracted']
    rhalf = (4/3)*source['Re_kpc']
    rerr = (4/3)*source['Re_error_kpc']
    rows = list(csv.DictReader((ROOT/'rebuild_2026_10_22/X1_hosted_recount/x1_per_system.csv').open()))
    x1 = next(r for r in rows if r['footing']=='canonical' and r['name']=='IC 1613')
    fd = json.loads((ROOT/'rebuild_2026_10_22/FD1_field_dwarf_audit/fd1_field_dwarf_audit_results.json').read_text())
    ic = next(r for r in fd['footings']['canonical']['runs']['M only']['rows'] if r['name']=='IC 1613')
    # Same half-stellar-mass convention as FD1, explicitly conditional; zero gas is a lower bound.
    mstar_enclosed = 0.5*10**ic['logMb']
    ic_result = dict(rhalf_kpc=rhalf, rhalf_error_kpc=rerr,
                     fd1_half_stellar_mass_Msun=mstar_enclosed,
                     x1_half_stellar_mass_Msun=0.5*10**float(x1['logMstar']), footings={})
    for name,a0 in A0.items():
        m = mass_required(source['vcirc_rhalf_kms'], rhalf, a0)
        # A rectangle of quoted marginal ±1 errors, not a joint confidence interval.
        corners = [mass_required(v,r,a0) for v in (13.,17.) for r in (rhalf-rerr,rhalf+rerr)]
        r = rhalf*KPC
        gnstar = G*mstar_enclosed*MSUN/r**2
        speed_min = math.sqrt(g_law(gnstar,a0)*r)/1e3
        g = (source['vcirc_rhalf_kms']*1e3)**2/r
        checks['mass_inversion_'+name] = abs(g_law(G*m*MSUN/r**2,a0)/g-1)<1e-12
        ic_result['footings'][name] = dict(required_enclosed_baryons_Msun=m,
            one_error_rectangle_range_Msun=[min(corners),max(corners)],
            fd1_stars_only_min_vcirc_kms=speed_min,
            fd1_stars_to_required_mass_ratio=mstar_enclosed/m)
    assert all(checks.values()), checks
    output = {'claim_id':'OSC28_NECESSARY', 'checks':checks, 'burkert_floor':floor,
              'IC1613_conditional_spherical_inversion':ic_result,
              'non_claims':['No re-fit of galaxy data or uncertainty posterior',
                            'No exclusion of non-spherical or external-field theory',
                            'No claim a floor is an upper bound for all X43 halos',
                            'No claim that a finite-radius fit must obey an all-radius identity']}
    target.write_text(json.dumps(output, indent=2, sort_keys=True)+'\n')
    print(json.dumps(output,indent=2))


if __name__=='__main__':
    main()
