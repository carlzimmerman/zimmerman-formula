#!/usr/bin/env python3
"""Re-evaluate the SAME stored DOP853 trajectory at arbitrary precision.

This separates evaluation/differencing roundoff from integration error. ODE
coefficients, initial data and stored dense-polynomial coefficients remain
float64 inputs. This is NOT arbitrary-precision integration or convergence
of the radial PDE. No equation is used to assign metric time derivatives.
"""
import argparse
import json
from pathlib import Path
from types import FunctionType, SimpleNamespace
import mpmath as mp
import numpy as np
from scipy.integrate import solve_ivp
from transfer_evolve import (Background, FIELDS, ALIASES, mode_system,
                             original_euler_operator, diagnose)
from transfer_jets import _evaluator


def object_array(value):
    return np.array(value, dtype=object)


def mp_solve(matrix, rhs):
    """Actual arbitrary-precision linear solve; no assumed rank/determinant."""
    matrix = mp.matrix(np.asarray(matrix, dtype=object).tolist())
    rhs = np.asarray(rhs, dtype=object)
    if rhs.ndim == 1:
        return object_array(list(mp.lu_solve(matrix, mp.matrix(rhs.tolist()))))
    columns = [list(mp.lu_solve(matrix, mp.matrix(rhs[:, j].tolist())))
               for j in range(rhs.shape[1])]
    return object_array(columns).T


MP_NUMPY = SimpleNamespace(array=object_array,
    zeros=lambda shape: np.zeros(shape, dtype=object),
    isfinite=lambda values: object_array([mp.isfinite(x) for x in np.asarray(values).flat]),
    all=np.all, linalg=SimpleNamespace(solve=mp_solve))


def precision_clone(function):
    """Reuse original compiled arithmetic, changing numerical backend only.

    Numeric literals remain those of the source. In particular pre-evaluated
    float constants are NOT claimed to become exact symbolic rationals.
    The source function and its module globals are never mutated.
    """
    namespace = dict(function.__globals__)
    namespace.update(np=MP_NUMPY, sqrt=mp.sqrt, log=mp.log, array=object_array)
    return FunctionType(function.__code__, namespace, function.__name__,
                        function.__defaults__, function.__closure__)


def dense_mp(solution, t):
    """SciPy 1.11 DOP853 nested polynomial, with the same segment selection."""
    if not solution.t_min <= t <= solution.t_max:
        raise ValueError('no extrapolation beyond the integrated dense solution')
    side = 'left' if solution.ascending else 'right'
    index = int(np.searchsorted(solution.ts_sorted, t, side=side))
    segment = min(max(index-1, 0), solution.n_segments-1)
    if not solution.ascending:
        segment = solution.n_segments-1-segment
    polynomial = solution.interpolants[segment]
    if type(polynomial).__name__ != 'Dop853DenseOutput':
        raise TypeError('only verified DOP853 polynomial layout is supported')
    x = (t-mp.mpf(float(polynomial.t_old)))/mp.mpf(float(polynomial.h))
    values = [mp.mpf(0) for _ in polynomial.y_old]
    for i, coefficients in enumerate(reversed(polynomial.F)):
        factor = x if i % 2 == 0 else 1-x
        values = [(value+mp.mpf(float(coefficient)))*factor
                  for value, coefficient in zip(values, coefficients)]
    return object_array([value+mp.mpf(float(initial))
                         for value, initial in zip(values, polynomial.y_old)])


class PrecisionEvaluator:
    def __init__(self, background, solution, k):
        self.bg, self.solution, self.k = background, solution, mp.mpf(k)
        self.bg_coefficients = precision_clone(background.model.bgfunc)
        self.jets = precision_clone(background.model.jetfunc)
        self.background_system = precision_clone(background.fun)
        names, function = _evaluator()
        self.extra_names, self.extra = names, precision_clone(function)
        self.mode = precision_clone(mode_system)
        self.euler_names, function = original_euler_operator()
        self.euler = precision_clone(function)

    def at(self, t):
        a, H, q, tau, rho, rad = dense_mp(self.bg.solution.sol, t)
        raw = self.bg_coefficients(*dense_mp(self.bg.model.solution.sol, tau))
        if raw[1]-2*raw[2]*q*q <= 0 or raw[1]-2*raw[2]*raw[0]**2 <= 0:
            raise ValueError('constitutive logarithm domain lost')
        gamma = mp.mpf(self.bg.model.gamma)
        jets = dict(zip(self.bg.model.names, self.jets(*raw, q*q, mp.mpf(0), gamma)))
        jets.update(zip(self.extra_names, self.extra(*raw, q*q, gamma)))
        values = {name: jets[alias] for name, alias in ALIASES.items()}
        values.update(a=a, H=H, q=q, rho=rho, Cr=mp.mpf(1), M2=mp.mpf(1),
                      Lambda=mp.mpf(.7), gamma=gamma, qr=(rad/3)**mp.mpf('.25'))
        out = object_array(self.background_system(*[values[x] for x in self.bg.names]))
        Hd, qd, s0 = mp_solve(out[:9].reshape(3, 3), out[9:12])
        if s0 <= 0:
            raise ValueError('positive clock rate lost')
        values.update(Hd=Hd, qd=qd, sbar=s0, qrd=-H*values['qr'], rhod=-3*H*rho)
        return values

    def fields(self, t):
        values = self.at(t)
        u = dense_mp(self.solution.sol, t).reshape(6, 6)
        _, _, lapse, zrow, brow, current = self.mode(values, self.k)
        return object_array([zrow@u, np.zeros(6, dtype=object), u[0], u[2],
                             u[4], u[5], lapse@u, brow@u]), current@u

    def diagnose(self, step, tend):
        step = mp.mpf(step)
        maxima = np.zeros(8, dtype=object)
        momentum_max = slip_max = mp.mpf(0)
        for time in np.linspace(.2*tend, .8*tend, 7):
            t = mp.mpf(float(time))
            fm2, fm, f, fp, fp2 = [self.fields(t+j*step)[0] for j in (-2, -1, 0, 1, 2)]
            fd = (fm2-8*fm+8*fp-fp2)/(12*step)
            fdd = (-fp2+16*fp-30*f+16*fm-fm2)/(12*step*step)
            jets = np.stack([f, fd, fdd], axis=1).reshape(24, 6)
            values = dict(self.at(t), k=self.k)
            matrix = self.euler(*[values[x] for x in self.euler_names])
            scaled = abs(matrix@jets)/(1+abs(matrix)@abs(jets))
            maxima = np.maximum(maxima, np.max(scaled, axis=1))
            current = self.fields(t)[1]
            momentum = 2*values['M2']*(fd[0]-values['H']*f[6])+current
            momentum_max = max(momentum_max, max(abs(momentum)/
                (1+abs(2*values['M2']*fd[0])+abs(2*values['M2']*values['H']*f[6])+abs(current))))
            shear = -values['a']**2*f[7]/self.k
            shear_rate = -values['a']**2*(fd[7]+2*values['H']*f[7])/self.k
            Phi = f[6]+shear_rate
            Psi = -f[0]-values['H']*shear
            slip_max = max(slip_max, max(abs(Phi-Psi)/(1+abs(Phi)+abs(Psi))))
        return dict(step=float(step), max_scaled_euler=float(max(maxima)),
                    euler_by_field=dict(zip(FIELDS, map(float, maxima))),
                    max_scaled_momentum=float(momentum_max), max_scaled_slip=float(slip_max))


def precision_sweep(bg, sol, k, steps=(.002, .001, .0005, .00025, .000125), dps=(30, 50)):
    tend = float(sol.t[-1])
    ordinary = [diagnose(bg, sol, k, tend, step) for step in steps]
    for row in ordinary:
        row.pop('potentials')
    runs = []
    for precision in dps:
        with mp.workdps(precision):
            evaluator = PrecisionEvaluator(bg, sol, k)
            runs.append(dict(decimal_digits=precision,
                             diagnostics=[evaluator.diagnose(step, tend) for step in steps]))
    return dict(k=k, float64=ordinary, precision_runs=runs,
                trajectory_precision='float64 unchanged stored integration coefficients',
                scope='Reconstruction/differencing precision diagnostic, not integration convergence or CMB',
                full_theory_status='OPEN')


def run():
    bg = Background(.02)
    k = .3
    sol = solve_ivp(lambda t, u: (mode_system(bg.at(float(t))[0], k)[0]@u.reshape(6, 6)).ravel(),
                   [0, .02], np.eye(6).ravel(), method='DOP853', rtol=2e-10,
                   atol=2e-12, dense_output=True)
    if not sol.success:
        raise RuntimeError(sol.message)
    return precision_sweep(bg, sol, k)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file', type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.result_file.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
