#!/usr/bin/env python3
"""Exact finite-mode Dirac chains and the finite-susceptibility MOND gate.

This is the frozen, fixed-metric scalar/clock principal action, not a nonlinear
Dirac certificate for the gravitational theory. Ranks/counts are computed,
not hard-coded. The braiding formulas use an affine, zero-Hessian jet.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import sympy as S


def mond_residual(g, gn, a0):
    return -math.expm1(-g / a0) * g - gn


def constraint_cases():
    x, z, p, r, u = S.symbols('pi sigma p_pi p_sigma multiplier', real=True)
    K, k, A, B, C = S.symbols('K k A B C', nonzero=True, real=True)
    variables = [x, z, p, r]
    def pb(f, g):
        return S.expand(sum(S.diff(f, a)*S.diff(g, b)-S.diff(f, b)*S.diff(g, a)
                            for a, b in [(x, p), (z, r)]))
    cases = {}
    # Each substitution is made BEFORE constructing the Hamiltonian/chain.
    for name, kk, bb, cc in [('regular', k, B, C), ('homogeneous_principal', 0, B, C),
                              ('singular_clock_with_mixing', k, B, 0),
                              ('clock_absent', k, 0, 0)]:
        v, w = S.symbols('pi_dot sigma_dot', real=True)
        L = K*v**2/2-kk**2*(A*x**2+2*bb*x*z+cc*z**2)/2
        hessian = S.hessian(L, [v, w])
        p_velocity = S.solve(S.diff(L, v)-p, v)[0]
        primary = r-S.diff(L, w)
        H = S.simplify((p*v-L).subs(v, p_velocity))
        HT = H+u*primary
        constraints = [primary]
        multiplier = None
        for _ in range(6):
            raw = pb(constraints[-1], HT)
            ideal = S.groebner(constraints, *variables, domain='EX')
            preserved = S.factor(ideal.reduce(raw)[1])
            if preserved == 0:
                break
            if S.diff(preserved, u) != 0:
                multiplier = S.solve(preserved, u)[0]
                break
            constraints.append(preserved)
        else:
            raise RuntimeError('constraint preservation did not close')
        matrix = S.Matrix([[S.factor(pb(f, g)) for g in constraints] for f in constraints])
        rank = matrix.rank()
        n_first, n_second = len(constraints)-rank, rank
        finalH = HT if multiplier is None else HT.subs(u, multiplier)
        ideal = S.groebner(constraints, *variables, domain='EX')
        preservation = [S.factor(ideal.reduce(pb(f, finalH))[1]) for f in constraints]
        if any(expr != 0 for expr in preservation):
            raise AssertionError((name, preservation))
        cases[name] = dict(L=L, kinetic_hessian=hessian, kinetic_rank=hessian.rank(),
                          H=H, constraints=constraints, bracket_matrix=matrix,
                          bracket_determinant=S.factor(matrix.det()),
                          bracket_rank=rank, first_class=n_first, second_class=n_second,
                          scalar_canonical_pairs=S.Rational(len(variables)-2*n_first-n_second, 2),
                          fixed_multiplier=multiplier, preservation=preservation)
    return cases


def derive():
    e = S.symbols('eps', real=True)
    q, s, PX, PXX, W0, WY = S.symbols('q s PX PXX W0 WY', positive=True)
    vt, vx, wt, wx = S.symbols('pi_t pi_x sigma_t sigma_x', real=True)
    X = (q+e*vt)**2-e**2*vx**2
    clocknorm = S.sqrt((s+e*wt)**2-e**2*wx**2)
    scalarproduct = -(s+e*wt)*(q+e*vt)+e**2*vx*wx
    Y = -X+scalarproduct**2/clocknorm**2
    L = PX*(X-q*q)+PXX*(X-q*q)**2/2+clocknorm*(W0+WY*Y)
    L2 = S.simplify(S.diff(L, e, 2).subs(e, 0)/2)
    K = S.diff(L2, vt, 2)
    A, B, C = [-S.diff(L2, *args) for args in [(vx, vx), (vx, wx), (wx, wx)]]
    G0 = S.factor(A-B**2/C)
    checks = {}
    def check(name, expr):
        residual = S.simplify(expr)
        if residual != 0:
            raise AssertionError((name, residual))
        checks[name] = True
    check('raw_clock_velocity_is_absent', S.diff(L2, wt))
    check('raw_action_coefficients_rebuild', L2-(K*vt**2-A*vx**2-2*B*vx*wx-C*wx**2)/2)
    check('exact_schur_reduction', G0-(2*PX-2*s*WY*W0/(W0-2*q*q*WY)))
    check('zero_W0_is_not_zero_clock_block', C.subs(W0, 0)+2*q*q*WY/s)
    check('zero_W0_leaves_P_gradient', G0.subs(W0, 0)-2*PX)
    gamma, M2 = S.symbols('gamma M2', nonzero=True, real=True)
    beta = 2*gamma**2*q**4/M2  # braiding correction, not L207 beta.
    Geff = G0-beta
    Keff = K+3*beta
    R = 1+beta/Geff
    check('enhancement_sound_speed_tradeoff', R*(Geff/Keff)-G0/Keff)
    check('decoupled_gamma_control', S.cancel(R).subs(gamma, 0)-1)
    check('zero_W0_still_has_braided_response',
          R.subs(W0, 0)-(1+beta/(2*PX-beta)))
    cases = constraint_cases()
    g, gn, a0 = S.symbols('g gn a0', positive=True)
    y = S.symbols('y', positive=True)
    mu = 1-S.exp(-y)
    check('deep_mond_coefficient_limit', S.limit(mu/y, y, 0, dir='+')-1)
    check('newtonian_mu_limit', S.limit(mu, y, S.oo)-1)
    check('exponential_primitive', S.diff(y*y+2*(1+y)*S.exp(-y)-2, y)-2*y*mu)
    # Numerical illustration of the exact Lean inequality; not a parameter fit.
    trials = []
    for response in (1., 10., 100.):
        gn_value = 1./(4*response**2)
        linear_g = response*gn_value
        trials.append(dict(response=response, a0=1., gn=gn_value, g=linear_g,
                           residual=mond_residual(linear_g, gn_value, 1.),
                           forbidden_if_g_le_response_gn=gn_value < 1./response**2))
        if mond_residual(linear_g, gn_value, 1.) >= 0:
            raise AssertionError('finite response unexpectedly saturated MOND lower bound')
    return dict(scope='Frozen fixed-metric principal Dirac chains; local regular-response obstruction, not full gravity closure',
                base_revision='f59fad6c7',
                raw_action=L2, coefficients=dict(K=K, A=A, B=B, C=C, G0=G0),
                constraint_cases=cases,
                braiding=dict(Bgrav=beta, G=Geff, K=Keff, enhancement=R,
                              identity='enhancement * sound_speed_squared = G0/Keff'),
                mond=dict(exact='g*(1-exp(-g/a0))=gN', lower_bound='g² >= a0*gN',
                          finite_response_obstruction='0<gN<a0/C² and 0<=g<=C*gN contradict exact MOND; C>0',
                          non_claim='Nonanalytic/degenerate/external-field/boundary-dependent branches not excluded',
                          numerical_controls=trials), checks=checks,
                provenance=dict(python=platform.python_version(), sympy=S.__version__,
                                sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = json.dumps(derive(), indent=2, default=str)+'\n'
    if args.output:
        args.output.write_text(result)
    else:
        print(result, end='')
