#!/usr/bin/env python3
"""Bounded read-only source-cell audit and separate spherical-kernel edge check."""
import ast
import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent

def source(rel):
    return (ROOT / rel).read_text()

def literal_assignment(rel, name):
    for node in ast.parse(source(rel)).body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == name:
                    return ast.literal_eval(node.value)
                if isinstance(target, ast.Tuple):
                    names = [n.id for n in target.elts if isinstance(n, ast.Name)]
                    if name in names:
                        return ast.literal_eval(node.value)[names.index(name)]
    raise AssertionError((rel, name))

L70 = 'real_research/merger_infall_2026/L370_boosted_infall_mergers.py'
L71 = 'real_research/merger_infall_2026/L371_harvey_slow_kick_carrier.py'
L77 = 'real_research/dark_sector_2026/L377_full_construction_pm.py'
L81 = 'real_research/dark_sector_2026/L381_harvey_on_pooled_window.py'
L87 = 'real_research/dark_sector_2026/L387_harvey_window_slow_end.py'

switch = literal_assignment(L70, 'SWITCH')
active = literal_assignment(L70, 'SW_DEF')
harvey_cell = switch[active]
pm_cell = (literal_assignment(L77, 'P_GATE'), literal_assignment(L77, 'X_C0'))
# Check the propagation points, not just the default declaration.
stores71 = [n.lineno for n in ast.walk(ast.parse(source(L71)))
            if isinstance(n, ast.Name) and n.id == 'SW_DEF' and isinstance(n.ctx, ast.Store)]
assert stores71 == [79]
assert '"A0K", "SW_DEF", "Grid", "phantom_felt"' in source(L71)
assert '.lensing(A0K["canonical"], SW_DEF, kernel)' in source(L71)
assert source(L71).count('A0K["canonical"], SW_DEF, [') == 2
assert 'SW_DEF' not in source(L81) and 'SW_DEF' not in source(L87)
assert harvey_cell != pm_cell
h = .6736
om = (.02237 + .1200) / h**2
orad70 = 4.18e-5 / h**2 * (1 + .2271*3.046)
e2harvey = om*1.4**3 + 1-om-orad70
gate_values = {"z": .4, "E2_L370": e2harvey,
               "inherited_harvey": harvey_cell[1]*e2harvey**harvey_cell[0],
               "p2_on_same_background": pm_cell[1]*e2harvey**pm_cell[0]}

# Independently recompute pooled halo medians and downstream gate arithmetic;
# this does not reproduce the costly PM or lensing simulations.
a = json.loads(source('real_research/dark_sector_2026/L380_pooled_window_fixed_cell_clearing_results.json'))['numbers']
b = json.loads(source('real_research/dark_sector_2026/L381_harvey_on_pooled_window_results.json'))['numbers']
bins = [(6e13, 1e14), (1e14, 1.5e14), (1.5e14, 2.5e14), (2.5e14, 1e17)]
max_delta = 0.0
for kick, reported in a['retention_by_mass'].items():
    pairs = [(mass, eps) for halo in a['halos'].values()
             for mass, eps in zip(halo['M_lt_1Mpc_h'], halo['eps'][kick])]
    for lo, hi in bins:
        values = [eps for mass, eps in pairs if lo <= mass < hi]
        reference, count = reported[f'{lo:.1e}-{hi:.1e}']
        assert count == len(values)
        max_delta = max(max_delta, abs(statistics.median(values)-reference))
    cluster_median = statistics.median(eps for mass, eps in pairs if mass >= 1e14)
    max_delta = max(max_delta, abs(cluster_median-a['table']['pooled'][kick]['eps_cl']))
assert max_delta < 1e-14
assert a['windows']['pooled'] == b['window']
pass_cells = []
for kick, result in b['results'].items():
    for shape in ('S1_med', 'S2_med', 'S3_med'):
        accepted = all(result['MEAN'][shape][est] <= .10 for est in ('100', '150', 'fit'))
        assert accepted == b['passes'][f'{kick}|{shape}']
        if accepted:
            pass_cells.append([kick, shape])

# Isolated point mass only.  t=g_N/a0, x=g/a0.  These are separate
# constitutive laws; neither calculation calls or replaces nu_mono.
def exp_inverse(t):
    lo, hi = 0.0, max(2.0, 2*t)
    for _ in range(100):
        mid = (lo+hi)/2
        if mid*(-math.expm1(-mid)) < t:
            lo = mid
        else:
            hi = mid
    return (lo+hi)/2

def kernel(t, branch):
    if branch == 'published_nu_RAR':
        s = math.sqrt(t)
        den = -math.expm1(-s)
        return 1/den, -math.exp(-s)/(2*s*den**2)
    x = exp_inverse(t)
    dx = 1/(1+(x-1)*math.exp(-x))
    return x/t, (t*dx-x)/t**2

G, MS, MPC, c = 6.67430e-11, 1.98892e30, 3.0856775814913673e22, 2.99792458e8
H0 = 100*h*1e3/MPC
rho_crit = 3*H0**2/(8*math.pi*G)
og = 4*5.670374419e-8*2.7255**4/c**3/rho_crit
orr = og*(1+3.046*(7/8)*(4/11)**(4/3))
z, t, xc0, p = 2.5, .1, 2., 2.
hz2 = H0**2*(om*(1+z)**3+1-om-orr)
xbar = 1.5*om*(1+z)**3*H0**2/hz2
e_gate = .3138*(1+z)**3+1-.3138
rows = []
for branch in ('published_nu_RAR', 'closure_mu_exp'):
    nu, dn = kernel(t, branch)
    for foot, a0 in {'canonical':9.3619e-11, 'alt':1.1279e-10}.items():
        for logmass in (10.,10.5,11.):
            mb = 10**logmass*MS
            r = math.sqrt(G*mb/(a0*t))
            # M_dyn(r)=Mb*nu(t), t=GMb/(a0*r^2).
            # Xflag=4*pi*G*rho_dyn/H^2-xbar; rho_dyn=M'_dyn/(4*pi*r^2).
            xf = G*mb/(r**3*hz2)*(-2*t*dn)-xbar
            eps = 1e-5
            def mass_at(radius):
                return mb*kernel(G*mb/(a0*radius**2),branch)[0]
            dm = (mass_at(r*(1+eps))-mass_at(r*(1-eps)))/(2*eps*r)
            x_fd = G*dm/(r*r*hz2)-xbar
            assert abs((x_fd-xf)/xf) < 2e-7
            gate = xc0*e_gate**p
            rows.append({'branch':branch,'foot':foot,'log10_Mb':logmass,
                         'nu_at_t_0_1':nu,'r_flag_kpc':r/(MPC/1000),
                         'X_at_flag':xf,'pmax_at_xc0_2':math.log(xf/xc0)/math.log(e_gate),
                         'p2_gate':gate,'flag_inside_p2':xf>=gate,
                         'outside_shift_dex':-2*math.log10(nu),
                         'finite_difference_relative_error':abs((x_fd-xf)/xf)})
assert kernel(.1,'published_nu_RAR')[0] != kernel(.1,'closure_mu_exp')[0]
assert [r['flag_inside_p2'] for r in rows] == [True,True,False,True,True,True]*2

out = {'verdict':'finite checks verified; same-gate identification refuted',
       'pm_cell':pm_cell,'active_harvey_cell':harvey_cell,'active_harvey_key':active,
       'gate_witness':gate_values,'retention_median_max_absolute_error':max_delta,
       'stored_Harvey_pass_cells':pass_cells,
       'S2_fit_at_600':b['results']['v600']['MEAN']['S2_med']['fit'],
       'separate_kernel_flagship_rows':rows,
       'non_claims':['No PM or Harvey simulation rerun',
                     'Point-mass on-branch diagnostic only; not an action or a nonspherical QUMOND/AQUAL equivalence',
                     'No inference that the corrected Harvey p2 gate passes or fails',
                     'No field-derived carrier dynamics or complete-theory certificate']}
(HERE/'run_001'/'results.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps(out,indent=2))
