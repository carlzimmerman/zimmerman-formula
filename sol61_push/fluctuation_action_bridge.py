#!/usr/bin/env python3
"""Static action bridge for the reconstructed response; not a microtheory.

The response/distribution is a prior inverse construction. Averaging the
specified primitive and adding a covariant vacuum term are independent
operations until a microscopic action selects both.
"""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True)
    args=ap.parse_args(); checks=[]
    def check(name,ok,detail):
        checks.append(dict(name=name,passed=bool(ok),detail=detail))
        print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    g,h,G=s.symbols('g h G',positive=True)
    C=s.symbols('C',real=True)
    b=s.sqrt(g*g+h*h)-h
    W=(g*s.sqrt(g*g+h*h)+h*h*s.asinh(g/h))/2-h*g
    check('primitive_has_physical_constitutive_derivative',s.simplify(s.diff(W,g)-b)==0,
          'L_static=-W/(4piG)-rho_b Phi yields div[(b(g)/g) grad Phi]=4piG rho_b')
    check('deep_action_coefficient',s.limit(W/g**3,g,0)==1/(6*h),
          'a0=2h, W=g³/(3a0)+O(g^5): usual deep-MOND static action')
    check('Newtonian_action_normalization',s.limit(W/g**2,g,s.oo)==s.Rational(1,2),
          'L_static tends -g²/(8piG); same calibrated Newton G for all h')
    x=s.symbols('x',positive=True)
    F=x*s.sqrt(1+4*x*x)/2+s.asinh(2*x)/4-x
    check('same_P2_primitive_as_earlier_audit',s.simplify(W-2*h*h*F.subs(x,g/(2*h)))==0,
          'W=a0² F(g²/a0²)/2; this is the earlier reconstructed action, not a new physical completion')
    check('fixed_response_does_not_select_vacuum_height',s.simplify(s.diff(W+C*h*h,g)-b)==0,
          'constant C h² has no static force effect; a covariant completion must fix its physical vacuum stress')
    # This convention gives rho_v=C h²/(4piG), hence Lambda=2C h².
    # It is a diagnostic dictionary; not automatically covariant stress.
    coefficient=s.simplify((8*s.pi*G)*(C*h*h/(4*s.pi*G))/(4*h*h))
    check('chosen_vacuum_dictionary_requires_free_height',coefficient==C/2 and s.solve(s.Eq(coefficient,32*s.pi),C)==[64*s.pi],
          'under the stated vacuum dictionary, target requires C=64pi as an extra input')
    data=dict(checks=checks,primitive=str(W),
              verdict='The reconstructed response has a valid static variational bridge and the calibrated Newtonian limit. It reconstructs the prior P2 action, but does not supply a microscopic vacuum height or 32pi.',
              non_claims=['No covariant completion','No origin of fluctuation averaging rule','No state-selection dynamics','No vacuum energy prediction','No novelty claim for P2 AQUAL reconstruction'])
    Path(args.output).write_text(json.dumps(data,indent=2)+'\n')
    failed=sum(not c['passed'] for c in checks)
    print(f'{len(checks)-failed}/{len(checks)} static action checks pass; 32pi OPEN.')
    return int(failed>0)


if __name__=='__main__': raise SystemExit(main())
