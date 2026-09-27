#!/usr/bin/env python3
"""Finite weighted-graph audit of the fixed-metric lapse variation.

This discretizes the energy on oriented cycle edges, using geometric endpoint
lapse interpolation. Node masses and edge conductances are both varied. The
graph identity is exact for this discretization, not a continuum Leibniz rule.
"""
import argparse
import json
import math
from pathlib import Path

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import expm, expm_frechet


def kernel(p, alpha):
    """Exact inverse constitutive kernel, to stated binary64 tolerance.

    s=x(1-exp(-x)), J=2 alpha^2 q(s^2), j=4 alpha x exp(-x) sign(p).
    Bisection bracket [0,s+1] works for every s>=0. The tiny-x polynomial
    avoids cancellation; its omitted term is below binary64 at x<1e-3.
    """
    p = np.asarray(p, dtype=float)
    s = np.abs(p) / alpha
    lo, hi = np.zeros_like(s), s + 1
    for _ in range(64):
        mid = (lo + hi) / 2
        below = mid * (-np.expm1(-mid)) < s
        lo, hi = np.where(below, mid, lo), np.where(below, hi, mid)
    x = np.where(s == 0, 0, (lo + hi) / 2)
    q = 2 - 2 * (1 + x) * np.exp(-x) - x*x*np.exp(-2*x)
    coefficients = [4/3, -7/4, 19/15, -47/72, 37/140, -17/192,
                    115/4536, -1279/201600, 563/399168, -6143/21772800]
    small_q = x**3 * np.polynomial.polynomial.polyval(x, coefficients)
    q = np.where(x < 1e-3, small_q, q)
    return 2*alpha*alpha*q, 4*alpha*x*np.exp(-x)*np.sign(p), x


def cycle(size):
    dx = 2*math.pi/size
    D, P = np.zeros((size, size)), np.zeros((size, size))
    for i in range(size):
        j = (i + 1) % size
        D[i, i], D[i, j] = -1/dx, 1/dx
        P[i, i], P[i, j] = .5, .5
    return dx, D, P


def operators(logN, D, P, dx):
    M = dx*np.exp(logN)
    W = dx*np.exp(P@logN)
    L = -(D.T@(W[:, None]*D))/M[:, None]
    return M, W, L


def state(logN, U, D, P, dx, b, alpha):
    M, W, L = operators(logN, D, P, dx)
    S = expm(b*L)
    a = D@logN
    J, j, inverse_x = kernel(D@(S@U), alpha)
    v = D@U-a
    density = 2*v*v+J
    energy = float(W@density)
    return dict(M=M, W=W, L=L, S=S, a=a, v=v, J=J, j=j,
                inverse_x=inverse_x, density=density, energy=energy)


def variation(logN, n, U, D, P, dx, b, alpha, quadrature_order=32):
    z = state(logN, U, D, P, dx, b, alpha)
    M, W, L = z['M'], z['W'], z['L']
    # Differentiate L=-M^{-1} D^T W D, including the inverse node mass.
    deltaL = -n[:, None]*L-(D.T@((W*(P@n))[:, None]*D))/M[:, None]
    deltaS = expm_frechet(b*L, b*deltaL, compute_expm=False)
    direct = float(W@((P@n)*z['density']-4*z['v']*(D@n)))
    heat_frechet = float((W*z['j'])@(D@(deltaS@U)))
    # y=-div_N j; L is self-adjoint in node mass M, not the Euclidean norm.
    y = (D.T@(W*z['j']))/M
    nodes, weights = leggauss(quadrature_order)
    integral = 0.
    deltaS_integral = np.zeros_like(L)
    mass_vertex, edge_vertex = 0., 0.
    for node, weight in zip(nodes, weights):
        s = b*(node+1)/2
        left, right = expm((b-s)*L), expm(s*L)
        r, w = left@y, right@U
        factor = b*weight/2
        integral += factor*float((M*r)@(deltaL@w))
        deltaS_integral += factor*(left@deltaL@right)
        mass_vertex += factor*float(-np.dot(M*n*r, L@w))
        edge_vertex += factor*float(-np.dot(W*(P@n)*(D@r), D@w))
    return dict(state=z, deltaL=deltaL, deltaS=deltaS,
                deltaS_integral=deltaS_integral, direct=direct,
                heat_frechet=heat_frechet, heat_duhamel=integral,
                mass_vertex=mass_vertex, edge_vertex=edge_vertex,
                total=direct+heat_frechet)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    checks = {}

    def check(name, measured, passed):
        assert bool(passed), (name, measured)
        checks[name] = {'passed': True, 'measured': measured}

    size, b, alpha = 12, .11, .8
    dx, D, P = cycle(size)
    x = dx*np.arange(size)
    logN = .8*np.cos(x)+.25*np.sin(2*x)
    U = 1.7*np.sin(x+.2)+.5*np.cos(3*x-.1)
    n = .4*np.sin(x-.7)+.55*np.cos(2*x+.1)+.15
    v = variation(logN, n, U, D, P, dx, b, alpha)
    z, deltaL = v['state'], v['deltaL']
    M, W, L = z['M'], z['W'], z['L']
    check('weighted_generator_self_adjoint',
          float(np.max(np.abs(M[:, None]*L-L.T*M[None, :]))),
          np.max(np.abs(M[:, None]*L-L.T*M[None, :])) < 2e-13)
    check('generator_and_variation_preserve_constants',
          [float(np.max(np.abs(L@np.ones(size)))),
           float(np.max(np.abs(deltaL@np.ones(size))))],
          np.max(np.abs(L@np.ones(size))) < 2e-13 and
          np.max(np.abs(deltaL@np.ones(size))) < 2e-13)
    step = 1e-5
    plus = state(logN+step*n, U, D, P, dx, b, alpha)
    minus = state(logN-step*n, U, D, P, dx, b, alpha)
    L_error = float(np.max(np.abs((plus['L']-minus['L'])/(2*step)-deltaL)))
    S_error = float(np.max(np.abs((plus['S']-minus['S'])/(2*step)-v['deltaS'])))
    check('generator_variation_central_difference', L_error, L_error < 2e-9)
    check('heat_operator_variation_central_difference', S_error, S_error < 2e-9)
    matrix_error = float(np.max(np.abs(v['deltaS']-v['deltaS_integral'])))
    heat_error = abs(v['heat_duhamel']-v['heat_frechet'])
    check('Duhamel_vs_Frechet_full_matrix', matrix_error, matrix_error < 2e-12)
    check('weighted_adjoint_Duhamel_vs_Frechet_energy', heat_error, heat_error < 2e-12)
    split_error = abs(v['mass_vertex']+v['edge_vertex']-v['heat_duhamel'])
    check('node_mass_plus_edge_conductance_vertices', split_error, split_error < 2e-12)

    rows = []
    for step in [1e-2, 1e-3, 1e-4, 1e-5]:
        ep = state(logN+step*n, U, D, P, dx, b, alpha)['energy']
        em = state(logN-step*n, U, D, P, dx, b, alpha)['energy']
        central = (ep-em)/(2*step)
        rows.append({'step': step, 'central_derivative': central,
                     'absolute_error': abs(central-v['total'])})
    check('full_lapse_energy_central_difference', rows,
          rows[-1]['absolute_error'] < 2e-8 and rows[-2]['absolute_error'] < 2e-7)
    check('central_difference_second_order_control',
          rows[0]['absolute_error']/rows[1]['absolute_error'],
          80 < rows[0]['absolute_error']/rows[1]['absolute_error'] < 120)

    # Discriminating controls: freezing the filter or omitting its inverse mass
    # variation changes the derivative for this deterministic nonconstant case.
    check('negative_control_freezing_filter_fails', abs(v['heat_frechet']),
          abs(v['heat_frechet']) > 1e-4)
    check('negative_control_omitting_node_mass_vertex_fails', abs(v['mass_vertex']),
          abs(v['mass_vertex']) > 1e-4)

    # Constant log-lapse perturbations scale E but leave a and L unchanged.
    vc = variation(logN, np.ones(size), U, D, P, dx, b, alpha)
    check('leafwise_constant_lapse_rescaling',
          {'generator_error': float(np.max(np.abs(vc['deltaL']))),
           'energy_derivative_error': abs(vc['total']-z['energy'])},
          np.max(np.abs(vc['deltaL'])) < 2e-13 and
          abs(vc['total']-z['energy']) < 2e-12)
    # b=0 removes the nonlocal lapse vertex exactly.
    v0 = variation(logN, n, U, D, P, dx, 0., alpha)
    check('zero_heat_time_control', abs(v0['heat_frechet']), v0['heat_frechet'] == 0)
    # At U=0 the filtered gradient and j vanish. No Hessian is used at this join.
    vz = variation(logN, n, np.zeros(size), D, P, dx, b, alpha)
    ep = state(logN+1e-5*n, np.zeros(size), D, P, dx, b, alpha)['energy']
    em = state(logN-1e-5*n, np.zeros(size), D, P, dx, b, alpha)['energy']
    zero_error = abs((ep-em)/2e-5-vz['total'])
    check('zero_gradient_C1_join_control',
          {'energy_derivative_error': zero_error, 'heat_term': vz['heat_frechet']},
          zero_error < 2e-8 and vz['heat_frechet'] == 0 and
          np.max(np.abs(vz['state']['j'])) == 0)
    p = np.array([1e-4, 1e-6, 1e-8])
    J, j, xx = kernel(p, alpha)
    ratios = J/p
    asymptotic_ratio = float(ratios[-1]/((8/3)*math.sqrt(alpha*p[-1])))
    check('kernel_one_sided_C1_join_scaling',
          {'J_over_p': ratios.tolist(), 'last_asymptotic_ratio': asymptotic_ratio},
          bool(np.all(np.diff(ratios) < 0)) and abs(asymptotic_ratio-1) < 1e-3)
    inversion_error = float(np.max(np.abs(xx*(-np.expm1(-xx))-p/alpha)))
    check('inverse_kernel_residual', inversion_error, inversion_error < 1e-14)

    output = {
        'result': 'fixed-h lapse variation verified for the stated weighted graph; continuum identity derived separately',
        'number_of_checks': len(checks), 'checks': checks,
        'generic_derivative': {key: v[key] for key in
                               ['direct', 'heat_frechet', 'heat_duhamel',
                                'mass_vertex', 'edge_vertex', 'total']},
        'generic_energy': z['energy'],
        'graph': {'nodes': size, 'heat_time': b, 'alpha': alpha,
                  'node_mass': 'dx exp(logN)',
                  'edge_conductance': 'dx exp(P logN)',
                  'D': '(u[i+1]-u[i])/dx, periodic',
                  'P': 'arithmetic endpoint interpolation'},
        'non_claims': ['No continuum convergence theorem from this finite graph',
                       'No full metric or clock variation, constraint count or causal-response result',
                       'No exact finite-graph continuum Leibniz identity; both graph weights are differentiated',
                       'Binary64 matrix exponential, quadrature and inverse-kernel calculations are tolerance-dependent']}
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(output, indent=2)+'\n')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
