#!/usr/bin/env python3
import argparse,json
from pathlib import Path
import sympy as s

u=s.symbols('u',nonnegative=True);S=(1-u**3)**3;at=2**(-s.Rational(1,3))
checks={'origin_positive':S.subs(u,0)==1,
        'flat_first':s.diff(S,u).subs(u,0)==0,
        'flat_second':s.diff(S,u,2).subs(u,0)==0,
        'C2_zero_join':all(s.diff(S,u,k).subs(u,1)==0 for k in range(3)),
        'positive_witness':s.simplify(S.subs(u,at))==s.Rational(1,8),
        'positive_curvature_witness':s.simplify(s.diff(S,u,2).subs(u,at))>0,
        'negative_principal_limit_at_positive_S':s.simplify((2*S-s.diff(S,u)**2/s.diff(S,u,2)).subs(u,at))==-s.Rational(1,32)}
a=argparse.ArgumentParser();a.add_argument('--output',required=True);args=a.parse_args()
out={'checks':{k:bool(v) for k,v in checks.items()},'all_pass':all(checks.values()),'count':len(checks),
     'scope':'Exact illustrative compact-zero gate; general theorem proved in GATE_LEMMA_EXTENSION'}
Path(args.output).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2));assert out['all_pass']
