#!/usr/bin/env python3
"""Exact design bound for the polarization block; no full-system health claim."""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path);args=parser.parse_args()
    q,C,pc,gamma,curv,eta=s.symbols('q C Pi_c gamma curvature eta',positive=True)
    checks=[]
    def equal(name,value,target=0):
        r=s.simplify(s.expand(value-target))
        checks.append({'name':name,'passed':r==0,'residual':str(r)})
    dnet=C*(q-1)**2*curv/pc**2-gamma
    qcrit=1+pc*s.sqrt(gamma/(C*curv))
    equal('exact_clock_threshold',dnet.subs(q,qcrit))
    equal('constructive_exceedance_for_every_finite_gamma',dnet.subs(q,1+2*pc*s.sqrt(gamma/(C*curv))),3*gamma)
    equal('threshold_with_fractional_margin',dnet.subs(q,1+(1+eta)*pc*s.sqrt(gamma/(C*curv))),gamma*(2*eta+eta**2))
    Qmax,curvmax=s.symbols('Qmax curvature_max',positive=True)
    bound=C*(Qmax-1)**2*curvmax/gamma
    equal('finite_box_stiffness_saturation',dnet.subs({q:Qmax,curv:curvmax,pc:s.sqrt(bound)}))
    u=s.symbols('u',positive=True);flat=s.exp(-u**3)
    third=s.diff(flat,u,3)
    equal('flat_gate_third_derivative',third,s.exp(-u**3)*(-27*u**6+54*u**3-6))
    vstar=1+s.sqrt(7)/3;ustar=vstar**s.Rational(1,3)
    equal('positive_curvature_maximum_stationary',(-27*u**6+54*u**3-6).subs(u,ustar))
    smax=s.simplify(s.diff(flat,u,2).subs(u,ustar))
    result={'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL','checks':checks,
            'unrestricted_Q_counterexample':str(1+2*pc*s.sqrt(gamma/(C*curv))),
            'finite_domain_bound':'Pi_c^2 >= sup_A [F(Q) max(S_second(Pi/Pi_c),0)] / gamma, gamma>0; implicit if A is in physical Pi coordinates',
            'flat_gate_u_at_curvature_max':str(ustar),'flat_gate_curvature_max':str(smax),'flat_gate_curvature_max_decimal':float(smax),
            'scope':'Necessary and sufficient coefficient condition D_net<=0 for positive fixed-background P block at all spatial k, given positive H_W; not full coupled system health.',
            'missing_input':'Current action/PIK1 criteria supply no finite joint Q,Pi admissible-state domain preserved by evolution.'}
    for c in checks: print(('PASS ' if c['passed'] else 'FAIL ')+c['name']+': '+c['residual'])
    print('flat_gate_curvature_max='+str(float(smax)));print('STATUS='+result['status'])
    if args.output:args.output.write_text(json.dumps(result,indent=2)+'\n')
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':raise SystemExit(main())
