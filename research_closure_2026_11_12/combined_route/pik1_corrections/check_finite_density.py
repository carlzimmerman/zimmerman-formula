#!/usr/bin/env python3
"""Finite-Pi continuation: exact fixed-clock polarization Hessian only.

This is not a dispersion calculation on an on-shell inhomogeneous solution.
It tests the Hessian block, its loss of invertibility, and the flat gate's
curvature. Gamma is the active two-sided local quadratic stiffness on Pi_bar>0.
"""
import argparse
import json
from pathlib import Path

import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    checks = []

    def equal(name, value, target=0):
        residual = s.simplify(s.expand(value-target))
        checks.append({"name":name,"passed":residual==0,"residual":str(residual)})

    u, eps, dPi, dp = s.symbols("u epsilon delta_Pi delta_P", real=True)
    F, pc, h, gamma = s.symbols("F Pi_c h gamma", positive=True)
    gate = s.exp(-u**3)
    derivative2 = s.diff(gate,u,2)
    equal("flat_gate_curvature", derivative2, s.exp(-u**3)*(9*u**4-6*u))
    threshold = s.real_root(s.Rational(2,3),3)
    equal("curvature_threshold", (9*u**4-6*u).subs(u,threshold))
    equal("positive_curvature_at_u_one", derivative2.subs(u,1), 3/s.E)
    direct_L = F*s.exp(-(u+eps*dPi/pc)**3)-h*eps**2*dp**2/2-gamma*(pc*u+eps*dPi)**2/2
    direct2 = s.diff(direct_L,eps,2).subs(eps,0)/2
    Dnet = F*derivative2/pc**2-gamma
    equal("direct_second_variation_at_finite_density", direct2, -h*dp**2/2+Dnet*dPi**2/2)
    # Anisotropic positive constitutive Hessian in its eigenbasis. The exact
    # rank-one update tests every direction, not only k parallel to P_bar.
    h1,h2,h3,D = s.symbols("h1 h2 h3 D",positive=True)
    kx,ky,kz = s.symbols("kx ky kz",real=True)
    kv=s.Matrix([kx,ky,kz]); H=s.diag(h1,h2,h3)
    operator=H-D*kv*kv.T
    equal("anisotropic_constraint_determinant", operator.det(), h1*h2*h3*(1-D*(kx*kx/h1+ky*ky/h2+kz*kz/h3)))
    equal("principal_axis_zero", operator.det().subs({ky:0,kz:0,kx:s.sqrt(h1/D)}))
    # Real law W at K|P|/a0=1/2 has h_parallel=4K, h_perp=2K.
    kval=s.sqrt(4*s.E/3)
    finite_op=operator.subs({h1:4,h2:2,h3:2,D:3/s.E,ky:0,kz:0,kx:kval})
    equal("flat_gate_finite_density_degenerate_witness", finite_op.det())
    beyond=operator.subs({h1:4,h2:2,h3:2,D:3/s.E,ky:0,kz:0,kx:s.sqrt(2)*kval})
    equal("flat_gate_finite_density_negative_direction", beyond[0,0], -4)
    # The full dynamical obstruction is not implied by this block alone.
    b=s.symbols("b",nonzero=True)
    equal("coupled_block_can_remove_P_block_singularity", s.Matrix([[0,b],[b,1]]).det(), -b*b)
    result={"status":"PASS" if all(c['passed'] for c in checks) else "FAIL", "checks":checks,
            "threshold_u":str(threshold),"threshold_u_decimal":float(threshold),
            "finite_density_coefficient":str(Dnet),
            "scope":"Exact fixed-clock/metric local polarization Hessian; local jets, not solved on-shell backgrounds.",
            "uniform_argument":"A C2 nonnegative nonincreasing nonconstant gate on [0,infinity) must have S''>0 somewhere: it has S'<0 somewhere by the mean value theorem; if curvature never becomes positive afterwards, its negative slope stays bounded away from zero and positivity fails at finite u.",
            "conclusion":"Flatness at Pi=0 moves the positive-curvature polarization-block obstruction to finite Pi. A full constrained calculation is required to call a region dynamically unhealthy.",
            "non_claims":["No full coupled-gravity no-go", "No assertion that every sampled physical halo reaches the curvature region", "No derived ultraviolet cutoff", "No bound saying active gamma is too small", "No viable completion demonstrated"]}
    for c in checks:
        print(("PASS " if c['passed'] else "FAIL ")+c['name']+": "+c['residual'])
    print("threshold_u="+str(float(threshold)))
    print(result['conclusion']);print('STATUS='+result['status'])
    if args.output: args.output.write_text(json.dumps(result,indent=2)+'\n')
    return 0 if result['status']=='PASS' else 1


if __name__=='__main__':
    raise SystemExit(main())
