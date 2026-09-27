#!/usr/bin/env python3
"""Exact prescribed-gate promotion and a regular partial-domain gate construction.

c=1; L361's NR density, all field/gradient jets independent for this partial
variation. This is not a covariant completion or a test of an empirical window.
The smooth candidate has Lambda,R,xc>0; K is real. K=R=0 is excluded.
"""
import argparse
import json
from pathlib import Path
import sympy as s


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    f, rb, rd, phi, psi, w, chi, gp, gs, gw, gc, Q, lam = s.symbols(
        'f rho_b rho_d phi psi w chi grad_phi grad_psi grad_w grad_chi Q lambda', real=True)
    G, a0, m, Lambda, R, xc = s.symbols('G a0 m Lambda R xc', positive=True)
    K = s.symbols('K', real=True)
    M2 = m**2 * (1-f)
    L = (-(rb+rd)*phi-gp**2/(8*s.pi*G)-f*rb*psi
         -(2*gs*gw+2*M2*psi*w-a0**2*f*Q-(1-f)*gw**2)/(8*s.pi*G)
         +f*rb*chi+(gc**2+M2*chi**2)/(8*s.pi*G))
    B = rb*(chi-psi)+(2*m**2*psi*w+a0**2*Q-gw**2-m**2*chi**2)/(8*s.pi*G)
    checks = {}

    def exact(name, expression):
        residual = s.simplify(expression)
        checks[name] = {'residual': str(residual), 'passed': residual == 0}
        assert residual == 0, (name, residual)

    exact('gate_source_from_L361', s.diff(L, f)-B)
    exact('L361_is_affine_in_gate', s.diff(L, f, 2))
    A = 27*Lambda*R/4
    smooth = A/(A+xc*K**4)
    constrained = L+lam*(f-smooth)
    exact('auxiliary_multiplier_is_minus_gate_source', s.diff(constrained, f).subs(lam, -B))
    exact('auxiliary_constraint', s.diff(constrained, lam)-(f-smooth))
    direct = s.diff(L.subs(f, smooth), K)
    constrained_K = s.diff(constrained, K).subs(lam, -B)
    exact('eliminate_then_vary_equals_vary_then_eliminate', direct-constrained_K)
    exact('gate_clock_momentum_correction', direct-B*s.diff(smooth, K))
    dfK = -4*A*xc*K**3/(A+xc*K**4)**2
    exact('smooth_clock_derivative', s.diff(smooth, K)-dfK)
    u = A/K**4
    F = s.Function('F')
    exact('bare_ratio_derivative', s.diff(u, K)+4*u/K)
    exact('generic_gate_clock_correction', s.diff(F(u), K)+4*u*s.Subs(s.diff(F(s.Symbol('u')), s.Symbol('u')), s.Symbol('u'), u)/K)
    exact('smooth_gate_is_ratio_gate_for_K_nonzero', smooth-u/(u+xc))
    exact('turnaround_gate', smooth.subs(K, 0)-1)
    exact('turnaround_first_derivative', s.diff(smooth, K).subs(K, 0))
    exact('turnaround_second_derivative', s.diff(smooth, K, 2).subs(K, 0))
    exact('turnaround_curvature_derivative', s.diff(smooth, R).subs(K, 0))
    exact('gate_reversal_symmetry', smooth.subs(K, -K)-smooth)
    exact('fixed_gate_omits_generic_term', direct-B*dfK)
    # A nonzero exact witness makes the fixed-gate omission detectable.
    witness = {G: 1, a0: 1, m: 1, Lambda: 1, R: 1, xc: 1, K: 1,
               rb: 0, chi: 0, psi: 0, w: 0, gw: 0, Q: 1}
    missed = s.simplify(direct.subs(witness))
    assert missed != 0
    checks['fixed_gate_negative_control'] = {'missed_term': str(missed), 'passed': missed != 0}
    # Along R=b*K^4 the value depends on b: no continuous joint-origin extension.
    b = s.symbols('b', positive=True)
    path_limit = s.simplify(s.limit(smooth.subs(R, b*K**4), K, 0))
    exact('joint_origin_path_dependence', path_limit-27*Lambda*b/(27*Lambda*b+4*xc))
    assert s.simplify(path_limit.subs(b, 1)-path_limit.subs(b, 2)) != 0
    result = {'result': 'exact partial-variation identities verified', 'checks': checks,
              'expressions': {'B': str(B), 'smooth_gate': str(smooth),
                              'clock_momentum_correction': str(s.factor(direct)),
                              'joint_origin_path_limit': str(path_limit)},
              'domain': 'Lambda,R,xc,G,a0,m positive; K real; ratio equivalence K nonzero',
              'non_claims': ['No complete relativistic action or full canonical count',
                             'No assertion smooth gate preserves previous hard-gate data windows',
                             'No regular extension through R=K=0 or negative-curvature sector',
                             'B depends on the field jets held fixed in this partial variation']}
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
