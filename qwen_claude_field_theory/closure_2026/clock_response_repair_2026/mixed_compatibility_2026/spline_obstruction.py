#!/usr/bin/env python3
"""Exact local compatibility test; no continuum or physics no-go is inferred."""
import argparse
import json
from pathlib import Path
import sympy as s


def compute():
    z, knot, x = s.symbols('z knot x', real=True)
    a = s.symbols('a0:4', real=True)
    jump = sum(a[i]*(z-knot)**i for i in range(4))
    # u_t(r)=r G(r^2): d_r u_t = G(z)+2z G'(z).
    radial = x*jump.subs(z,x*x)
    transformed = jump+2*z*s.diff(jump,z)
    assert s.expand(s.diff(radial,x)-transformed.subs(z,x*x)) == 0
    # G is C2. Requiring the transformed function to be C2 adds its
    # second z-derivative jump. All four rows are derived, not prescribed.
    conditions = [s.diff(jump,z,i).subs(z,knot) for i in range(3)]
    conditions += [s.diff(transformed,z,2).subs(z,knot)]
    matrix, rhs = s.linear_eq_to_matrix(conditions,a)
    jump_identity = s.diff(transformed,z,2) - (5*s.diff(jump,z,2)+2*z*s.diff(jump,z,3))
    assert s.expand(jump_identity) == 0
    # Independent generic smooth C2 cubic join: zero left, (z-knot)^3 right.
    counterexample = [s.simplify(c.subs(dict(zip(a,[0,0,0,1])))) for c in conditions]
    return dict(matrix=str(matrix), determinant=str(s.factor(matrix.det())),
                generic_rank=matrix.rank(), origin_rank=matrix.subs(knot,0).rank(),
                generic_nullspace=[str(v) for v in matrix.nullspace()],
                origin_nullspace=[str(v) for v in matrix.subs(knot,0).nullspace()],
                cubic_join_condition_jumps=list(map(str,counterexample)),
                exact_chain_rule_checked=True, exact_jump_identity_checked=True,
                interpretation='At nonzero knots, simultaneous C2 regularity forces the third derivative jump to vanish; piecewise cubics then join as one cubic.',
                non_claims=['Approximation can still converge', 'No physics or gravitational degree-of-freedom no-go', 'No proof of the remaining numerical error cause'])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--result-file',type=Path,required=True)
    args=parser.parse_args();result=compute()
    args.result_file.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
