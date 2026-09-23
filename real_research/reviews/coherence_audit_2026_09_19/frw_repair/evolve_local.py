"""Bounded evolution checks of the two-mode, time-dependent FRW equations.

This integrates selected initial data over short intervals in log(a). It is
not a cosmic growth history, a nonlinear calculation, or interval arithmetic.
Initial data select the largest real instantaneous eigenvalue. Two independent
integrators and two tolerances check the resulting amplification.
"""
from pathlib import Path
import json
import math
import numpy as np
import sympy as s
import mpmath as mp
from scipy.integrate import solve_ivp

here = Path(__file__).resolve().parent
mp.mp.dps = 65
results = []
for label, directory, a_start, k_mpc, delta_n in (
    ('constant', 'run_adm', 0.1, 0.1, 0.01),
    ('response_n4', 'run_response_extended', 0.5, 0.001, 0.004),
):
    d = json.loads((here / directory / 'reduced.json').read_text())
    mass, rest = (s.sympify(d[key]) for key in ('mass', 'rest'))
    variables = [s.sympify(x) for x in d['vars']]
    # Cancel rational expressions symbolically before floating-point evaluation:
    # the nearly singular raw kinetic matrix is not inverted in float64.
    acceleration = (-(mass.inv()) * rest).applyfunc(s.factor)
    af = s.lambdify(variables, acceleration, 'numpy', cse=True)
    ap = s.lambdify(variables, acceleration, 'mpmath', cse=True)
    gc = float(s.sympify(d['Gc']))
    eps = 1e-9
    j0 = -1.86 / (1 - eps)
    lam = 3 * gc - (eps - 1) * j0 / 2
    hubble_mpc = 299792458 / 67400
    xi = 0.000004 / hubble_mpc
    k = k_mpc * hubble_mpc

    def background(n):
        a = math.exp(n)
        q = 1 - 3 * eps * n
        j = j0 / a**3
        h = math.sqrt(((eps - q) * j / 2 + lam) / (3 * gc))
        hd = q * j / (4 * gc)
        args = [a, h, q, j, eps, xi, k]
        if label == 'response_n4':
            v = 1e-7 * a**-4
            alpha = 0.5 * v / (0.5 + v)
            args += [alpha, -4 * h * alpha * (1 - alpha / 0.5)]
        return h, hd, args

    def matrix(n):
        h, hd, args = background(n)
        acc = np.asarray(af(*args), dtype=float)
        acc[:, [1, 3]] *= h
        acc /= h * h
        # q_ddot = H^2 q_NN + Hdot q_N.
        acc[0, 1] -= hd / h**2
        acc[1, 3] -= hd / h**2
        return np.array([[0, 1, 0, 0], acc[0], [0, 0, 0, 1], acc[1]])

    n0, n1 = math.log(a_start), math.log(a_start) + delta_n
    max_eval_error = 0.0
    for n in np.linspace(n0, n1, 7):
        _, _, args = background(n)
        high = np.asarray(ap(*[mp.mpf(x) for x in args]).tolist(), dtype=float)
        low = np.asarray(af(*args), dtype=float)
        err = np.max(np.abs(low - high) / (1 + np.abs(high)))
        max_eval_error = max(max_eval_error, float(err))
    assert max_eval_error < 1e-9, max_eval_error

    vals, vecs = np.linalg.eig(matrix(n0))
    index = int(np.argmax(vals.real))
    assert abs(vals[index].imag) < 1e-7
    y0 = vecs[:, index].real
    y0 /= np.linalg.norm(y0)
    trials = []
    for method, tol in (('DOP853', 1e-10), ('DOP853', 1e-12), ('Radau', 1e-11)):
        sol = solve_ivp(lambda n, y: matrix(n) @ y, (n0, n1), y0,
                        method=method, rtol=tol, atol=tol * 1e-3,
                        max_step=delta_n / 30)
        assert sol.success, sol.message
        trials.append({'method': method, 'rtol': tol, 'nfev': sol.nfev,
                       'end_state': sol.y[:, -1].tolist()})
    reference = np.array(trials[1]['end_state'])
    disagreement = max(np.linalg.norm(np.array(z['end_state']) - reference)
                       / np.linalg.norm(reference) for z in trials)
    assert disagreement < 1e-7, disagreement
    # An independent 50-digit RK4 convergence check also tests sensitivity to
    # cancellation in the evolving, coupled system rather than only its entries.
    mp.mp.dps = 50
    mgc, meps, mj0, mlam, mxi, mk = map(mp.mpf, (gc, eps, j0, lam, xi, k))
    def rhs_mp(n, y):
        aa = mp.exp(n)
        qq = 1 - 3 * meps * n
        jj = mj0 / aa**3
        hh = mp.sqrt(((meps - qq) * jj / 2 + mlam) / (3 * mgc))
        hhd = qq * jj / (4 * mgc)
        arguments = [aa, hh, qq, jj, meps, mxi, mk]
        if label == 'response_n4':
            vv = mp.mpf('1e-7') * aa**-4
            alpha = mp.mpf('0.5') * vv / (mp.mpf('0.5') + vv)
            arguments += [alpha, -4 * hh * alpha * (1 - 2 * alpha)]
        ac = ap(*arguments)
        z = mp.matrix([y[0], hh*y[1], y[2], hh*y[3]])
        acceleration_now = ac * z / hh**2
        return mp.matrix([y[1], acceleration_now[0] - hhd/hh**2*y[1],
                          y[3], acceleration_now[1] - hhd/hh**2*y[3]])
    high_trials = []
    for steps in (200, 400):
        step = mp.mpf(delta_n) / steps
        n = mp.mpf(n0)
        y = mp.matrix([mp.mpf(z) for z in y0])
        for unused in range(steps):
            k1 = rhs_mp(n, y)
            k2 = rhs_mp(n+step/2, y+step*k1/2)
            k3 = rhs_mp(n+step/2, y+step*k2/2)
            k4 = rhs_mp(n+step, y+step*k3)
            y += step*(k1+2*k2+2*k3+k4)/6
            n += step
        high_trials.append({'method': 'mpmath RK4', 'decimal_precision': 50,
                            'steps': steps, 'end_state': [float(z) for z in y]})
    high_reference = np.array(high_trials[-1]['end_state'])
    high_disagreement = np.linalg.norm(high_reference-reference)/np.linalg.norm(high_reference)
    rk4_convergence = np.linalg.norm(high_reference-np.array(high_trials[0]['end_state']))/np.linalg.norm(high_reference)
    assert high_disagreement < 1e-6, high_disagreement
    assert rk4_convergence < 1e-6, rk4_convergence
    row = {'case': label, 'a_start': a_start, 'a_end': math.exp(n1),
           'k_Mpc_inv': k_mpc, 'delta_log_a': delta_n,
           'state': ['Phi', 'dPhi/dlog(a)', 'P', 'dP/dlog(a)'],
           'initial_state': y0.tolist(),
           'initial_largest_eigenvalue_per_log_a': float(vals[index].real),
           'state_norm_amplification': float(np.linalg.norm(reference)),
           'Phi_amplification': float(reference[0] / y0[0]),
           'P_amplification': float(reference[2] / y0[2]),
           'float64_vs_65digit_coefficient_error': max_eval_error,
           'integrator_relative_disagreement': float(disagreement),
           'float64_vs_50digit_evolution_disagreement': float(high_disagreement),
           'RK4_step_doubling_disagreement': float(rk4_convergence),
           'trials': trials + high_trials}
    results.append(row)
    print(json.dumps(row), flush=True)
(here / 'local_evolution.json').write_text(json.dumps(results, indent=2) + '\n')
