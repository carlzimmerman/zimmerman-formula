#!/usr/bin/env python3
"""Independent leading-order audit of the local dipole response experiment.

Solves its longitudinal forced oscillator analytically. Does not solve
transport, pumping, Poisson feedback, or the full nonlinear field theory.
"""
import argparse
import json
import math
from pathlib import Path


def cosine_average(w, lo, hi):
    return 1.0 if w == 0 else (math.sin(w*hi)-math.sin(w*lo))/(w*(hi-lo))


def coefficient(gap, lo, hi, a=0.5, b=0.5):
    w1, w2, w3 = 0.3, 1.0, 1.0+gap
    return math.sqrt(3)*a*b/12*sum(
        w1*w1/(w1*w1-w*w)*(cosine_average(w,lo,hi)-cosine_average(w1,lo,hi))
        for w in (w3-w2,w3+w2))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--output', required=True)
    p.add_argument('--input', default='sol61_push/nonabelian_results.json')
    args=p.parse_args()
    prior=json.loads(Path(args.input).read_text())
    checks=[]
    def check(name, ok, detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    predicted=coefficient(.002,100,600)
    actual=next(x for x in prior['rows'] if x['g']==.0002 and x['kind']=='coherent')['mean_D_over_g_squared']
    check('orthogonal_analytic_ODE_check',abs(predicted-actual)/abs(actual)<.001,
          f'leading order={predicted:.12g}, numerical={actual:.12g}')
    check('zero_initial_response',coefficient(.002,100,600,a=0)==0,
          'no transverse correlation implies no longitudinal response at this order')
    check('chirality_dependence',coefficient(.002,100,600,b=-.5)==-predicted,
          'reversing one transverse displacement reverses response')
    windows=[]
    for end in (600,6000,60000,600000):
        windows.append(dict(start=100,end=end,gap=.002,coefficient=coefficient(.002,100,end)))
    check('dephasing_long_window',abs(windows[-1]['coefficient'])<abs(predicted)/100,
          str(windows))
    degenerate=coefficient(0,100,600000)
    limit=math.sqrt(3)*.25/12
    check('frequency_lock_retains_response',abs(degenerate-limit)<1e-5,
          f'equal-frequency limit={limit:.12g}, finite average={degenerate:.12g}')
    # Physical xi_a=2g z_a/omega_a^2. Fixed dimensionless transverse
    # amplitude therefore makes physical displacement proportional to g.
    gref=.0002
    rows=[]
    for g in (.0002,.0004,.0008):
        field_selected=g*g*predicted
        fixed_physical=g*g*coefficient(.002,100,600,a=.5*gref/g,b=.5*gref/g)
        rows.append(dict(g=g,D_field_selected=field_selected,D_fixed_physical=fixed_physical))
    check('field_selected_amplitudes_insert_scaling',abs(rows[-1]['D_field_selected']/rows[0]['D_field_selected']-16)<1e-10,
          'physical oscillation amplitude proportional to g gives D proportional to g^2')
    check('fixed_physical_amplitudes_do_not_give_MON_D',max(x['D_fixed_physical'] for x in rows)-min(x['D_fixed_physical'] for x in rows)<1e-20,
          'fixed physical transverse amplitude gives field-independent leading response in this local truncation')
    data=dict(checks=checks,leading_coefficient=predicted,windows=windows,amplitude_rows=rows,
              interpretation='Quadratic response requires field-dependent amplitude selection AND maintained phase correlation. Neither is dynamically derived here.',
              original_nonlinear_check_failure='18/19: amplitude doubling departs from factor two by up to 0.187 over the finite window; preserved, not retuned.',
              limits=['leading perturbative order','constant local g','finite-window average','no pump or capture mechanism','no complete theory'])
    Path(args.output).write_text(json.dumps(data,indent=2)+'\n')
    failures=sum(not x['passed'] for x in checks)
    print(f'{len(checks)-failures}/{len(checks)} checks pass; theory remains OPEN.')
    return int(failures>0)


if __name__=='__main__':
    raise SystemExit(main())
