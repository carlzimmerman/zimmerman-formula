#!/usr/bin/env python3
"""Exact reduction checks and a bounded, non-interval shooting illustration."""
import json
import math
import sys
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import solve_ivp, quad
from scipy.optimize import brentq

checks = []


def eq(name, left, right=0):
    residual = s.simplify(left-right)
    if residual != 0:
        raise AssertionError((name, residual))
    checks.append(name)


t, k, R, G, K, alpha, rho, c = s.symbols('t k R G K alpha rho c', positive=True)
theta = s.sin(k*t)/(k*t)
mass = -t*t*s.diff(theta, t)/(k*k)
psi = (1+theta)/(k*k)
eq('base enclosed core mass', s.diff(mass, t), t*t*theta)
eq('base core Euler equation', s.diff(theta, t), -k*k*mass/(t*t))
eq('base Poisson potential equation', s.diff(psi, t), -mass/(t*t))
eq('base first zero', theta.subs(t, s.pi/k), 0)
eq('base mass at edge', mass.subs(t, s.pi/k), s.pi/k**3)
eq('base potential at edge', psi.subs(t, s.pi/k), 1/k**2)
eq('base center potential', s.limit(psi, t, 0), 2/k**2)
eq('transverse core boundary', s.diff(theta, t).subs(t, s.pi/k), -k/s.pi)
pc = s.symbols('pc', real=True)
Fbase = pc-1/k**2-(s.pi/k**3)/(s.pi/k)
eq('matching mismatch at base', Fbase, pc-2/k**2)
eq('matching derivative', s.diff(Fbase, pc), 1)
L0sq = s.pi*K/(2*G*(1-alpha))
eq('base radial coercivity margin',
   K*(s.pi**2+2)/(2*s.pi*L0sq*G*(1-alpha))-1, 2/s.pi**2)
hcore = rho*c*c+2*K*rho*rho
score = 2*K*rho/(c*c+2*K*rho)
eq('Gamma2 relativistic effective inertia', hcore*(1-score), rho*c*c)
ell, eps, eta = s.symbols('ell eps eta', positive=True)
# rho=eps c²/(4pi G ell²), a0=sqrt(alpha) eps c²/(eta ell)
a0 = s.sqrt(alpha)*eps*c*c/(eta*ell)
rho_star = eps*c*c/(4*s.pi*G*ell*ell)
eq('electric-to-material energy normalization',
   a0*a0/(4*s.pi*G*rho_star*c*c), alpha*eps/(eta*eta))
z, mu = s.symbols('z mu', positive=True)
Z1 = (1+mu)/z-mu/(3*z**3)
eq('exterior first Picard edge', Z1.subs(z, 1), 1+2*mu/3)
eq('exterior first Picard asymptotic mass', s.limit(z*Z1, z, s.oo), 1+mu)

ALPHA = 0.5
DELTA = 1e-6
ETA = 1e-3
T0 = 1e-6
RTOL = 2e-11
ATOL = 2e-13
K2 = 1-ALPHA
KROOT = math.sqrt(K2)
RBASE = math.pi/KROOT
MBASE = math.pi/KROOT**3
PCBASE = 2/K2


def integrate_interior(pc, delta=DELTA, eta=ETA):
    neutral0 = delta*pc**5
    initial = [1-(K2+neutral0)*T0*T0/6+ALPHA*eta*T0**3/27,
               T0**3/3, neutral0*T0**3/3,
               pc-(1+neutral0)*T0*T0/6]

    def rhs(rr, y):
        th, mc, ms, ps = y
        xx = eta*mc/(rr*rr)
        if xx >= 0.9:
            raise ValueError('Exploratory sample left declared pole-safe domain')
        return [-(mc+ms-ALPHA*mc/(1-xx))/(rr*rr),
                rr*rr*th, delta*rr*rr*ps**5, -(mc+ms)/(rr*rr)]

    def edge(rr, y):
        return y[0]

    edge.terminal = True
    edge.direction = -1
    sol = solve_ivp(rhs, (T0, 2*RBASE), initial, events=edge,
                    rtol=RTOL, atol=ATOL, method='DOP853', dense_output=True)
    if not sol.success or len(sol.t_events[0]) != 1:
        raise AssertionError('Interior did not reach a simple first zero')
    radius = float(sol.t_events[0][0])
    state = sol.y_events[0][0]
    return radius, state, sol


def integrate_exterior(radius, state, outer, delta=DELTA):
    mc = float(state[1])

    def rhs(rr, y):
        ms, ps = y
        return [delta*rr*rr*ps**5, -(mc+ms)/(rr*rr)]

    sol = solve_ivp(rhs, (radius, outer), [state[2], state[3]],
                    rtol=RTOL, atol=ATOL, method='DOP853', dense_output=True)
    if not sol.success:
        raise AssertionError('Exterior shooting integration failed')
    ms, ps = sol.y[:, -1]
    mtotal = mc+ms
    # Exterior first Picard boundary value m/T + delta m^5/(3T^3).
    boundary = mtotal/outer+delta*mtotal**5/(3*outer**3)
    residual = ps-boundary
    mu_tail = delta*mtotal**4/(2*outer**2)
    q_tail = 80*mu_tail  # C=2 contraction bound, deliberately conservative
    assert q_tail < 1 and 1+32*mu_tail < 2
    # ||Z-Z1|| <= q ||Z1-Z0||/(1-q) <= q mu/(1-q).
    picard_error = mtotal/outer*q_tail*mu_tail/(1-q_tail)
    return residual, sol, mtotal, mu_tail, picard_error


def sample(outer):
    calls = [0]

    def residual(pc):
        calls[0] += 1
        radius, state, _ = integrate_interior(pc)
        return integrate_exterior(radius, state, outer)[0]

    pc = brentq(residual, PCBASE-.1, PCBASE+.1, xtol=2e-13, rtol=2e-14)
    radius, state, interior = integrate_interior(pc)
    residual_value, exterior, mtotal, mu_tail, tail_error = integrate_exterior(radius, state, outer)
    mc = float(state[1])
    # Bounds below are diagnostics from non-interval ODE values.
    # C=2 gives an analytic remaining neutral mass cap from the outer shell.
    remaining_neutral_cap = 32*mu_tail*mtotal
    total_neutral_cap = mtotal-mc+remaining_neutral_cap
    # Central neutral potential delta int r psi^5 dr, with C=2 tail cap.
    int_core = quad(lambda rr: DELTA*rr*float(interior.sol(rr)[3])**5,
                    T0, radius, epsabs=1e-12, epsrel=1e-10)[0]
    int_ext = quad(lambda rr: DELTA*rr*float(exterior.sol(rr)[1])**5,
                   radius, outer, epsabs=1e-12, epsrel=1e-10)[0]
    central_tail_cap = DELTA*(2*mtotal)**5/(3*outer**3)
    neutral_central_cap = int_core+int_ext+central_tail_cap
    ratio_cap = max(neutral_central_cap*radius/mc, total_neutral_cap/mc)
    qs = 5*ratio_cap
    kap = (math.pi**2+2)/(K2*radius**2)-1
    coercivity_det = kap*K2*(1-qs)-qs  # units G=1
    grid_inside = np.geomspace(T0, radius, 240)
    grid_outside = np.geomspace(radius, outer, 160)
    x_values = [ETA*float(interior.sol(rr)[1])/(rr*rr) for rr in grid_inside]
    assert min(interior.sol(grid_inside)[3]) > 0
    assert min(exterior.sol(grid_outside)[1]) > 0
    assert radius < 1.01*RBASE and coercivity_det > 0
    return {'outer_radius': outer, 'psi_center': pc,
            'core_radius': radius, 'base_radius': RBASE,
            'charged_mass': mc, 'neutral_mass_upper_diagnostic': total_neutral_cap,
            'central_neutral_potential_upper_diagnostic': neutral_central_cap,
            'qs_upper_diagnostic': qs, 'kappa_diagnostic': kap,
            'radial_Schur_margin_diagnostic_G1': coercivity_det,
            'matching_residual': residual_value,
            'tail_mu': mu_tail,
            'tail_first_Picard_error_bound_given_ODE_state': tail_error,
            'max_x_sampled_not_uniform_bound': max(x_values),
            'shooting_evaluations': calls[0]}


# Orthogonal implementation benchmark against the exact uncharged-atmosphere base.
rbase_num, state_base, _ = integrate_interior(PCBASE, delta=0, eta=0)
assert abs(rbase_num-RBASE) < 1e-8
assert abs(state_base[1]-MBASE) < 1e-8
assert abs(state_base[3]-1/K2) < 1e-8
samples = [sample(outer) for outer in [100., 200., 400.]]
assert abs(samples[-1]['psi_center']-samples[-2]['psi_center']) < 1e-8
result = {
    'claim_id': 'VC3-STIFF-001',
    'exact_checks': len(checks), 'check_names': checks,
    'sample_parameters': {'alpha': ALPHA, 'delta': DELTA, 'eta': ETA},
    'ODE': {'method': 'DOP853', 'rtol': RTOL, 'atol': ATOL,
            'central_start': T0, 'outer_radii': [100, 200, 400]},
    'base_benchmark': {'radius_error': rbase_num-RBASE,
                       'mass_error': float(state_base[1])-MBASE},
    'samples': samples,
    'interpretation': 'Exact reduction checks passed; bounded non-interval shooting illustrates a small positive branch and radial Schur margin. Existence and positivity for sufficiently small parameters rest on the analytic proof, not this finite sample.',
    'nonclaims': ['No interval ODE certification of the listed sample.',
                  'No quantified universal sufficiently-small threshold.',
                  'No angular, full Einstein, nonlinear free-boundary or vacuum-phase closure.',
                  'Subcritical charge changes the original critical-charge model.']
}
Path(sys.argv[1]).write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({'exact_checks':len(checks), 'sample':samples[-1]}))
