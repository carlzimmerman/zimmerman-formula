#!/usr/bin/env python3
"""First nonlinear self-interaction vertices of the unchanged P+sW sector.

Metric and clock are held fixed ONLY to isolate bare vertices. This is not a
constraint-reduced nonlinear action, Hamiltonian, or stability certificate.
The constant-gamma X Box chi term is at most cubic in chi on fixed geometry;
metric/clock exchange and generated harmonics remain necessary.
"""
import argparse
from functools import lru_cache
import json
from pathlib import Path
import sys

import numpy as np
import sympy as s

HERE = Path(__file__).resolve().parent
REPAIR = HERE.parents[1]
sys.path.insert(0, str(REPAIR / 'nonlinear_evolution_2026'))
from constitutive import Model

ARCHIVE = REPAIR / 'inhomogeneous_charge_2026/exterior/run_001/result.json'


@lru_cache(maxsize=1)
def symbolic_vertices():
    ep, q, amp, vel, p, a, clock, c, sn = s.symbols(
        'epsilon Q amplitude velocity p a clock cosine sine', real=True)
    P0, PX, PXX, PXXX, PXXXX, W0, WY, WYY = s.symbols(
        'P PX PXX PXXX PXXXX W WY WYY', real=True)
    Y = ep**2*p*amp**2*sn**2
    dX = (q+ep*vel*c)**2-q**2-Y
    raw = a**3*(P0+PX*dX+PXX*dX**2/2+PXXX*dX**3/6+
                PXXXX*dX**4/24+clock*(W0+WY*Y+WYY*Y**2/2))
    phase = s.symbols('phase', real=True)

    def average(expr):
        out = 0
        for (ic, isn), coef in s.Poly(s.expand(expr), c, sn).terms():
            moment = s.integrate(s.cos(phase)**ic*s.sin(phase)**isn,
                                 (phase, 0, 2*s.pi))/(2*s.pi)
            out += coef*moment
        return s.factor(out)

    derived = average(s.expand(raw).coeff(ep, 4))
    expected = a**3*(PXX*(3*vel**4-2*p*amp**2*vel**2+3*p**2*amp**4)/16+
        q**2*PXXX*(3*vel**4-p*amp**2*vel**2)/4+
        q**4*PXXXX*vel**4/4+3*clock*WYY*p**2*amp**4/16)
    Y2 = s.expand(Y).coeff(ep, 2)
    m1, m2 = average(Y2), average(Y2**2)
    # Independent local functional derivative at fixed Q, zero delta Q.
    x, k = s.symbols('x k', real=True)
    grad = -ep*amp*k*s.sin(k*x)
    localY = grad**2/a**2
    localL = -PX*localY+PXX*localY**2/2+clock*(WY*localY+WYY*localY**2/2)
    g = s.symbols('gradient', real=True)
    Lg = -PX*g**2/a**2+PXX*g**4/(2*a**4)+clock*(WY*g**2/a**2+WYY*g**4/(2*a**4))
    euler = -s.diff(s.diff(Lg, g).subs(g, grad), x)
    cubic = s.expand(euler).coeff(ep, 3)
    target = 3*(PXX+clock*WYY)*amp**3*k**4/(2*a**4)*(s.cos(k*x)-s.cos(3*k*x))
    checks = dict(
        quartic_action=s.expand(derived-expected)==0,
        static_vertex=s.expand(derived.subs(vel, 0)-3*a**3*p**2*amp**4*(PXX+clock*WYY)/16)==0,
        fourth_moment=s.simplify(m2-s.Rational(3,2)*m1**2)==0,
        meanfield_W_error=s.simplify(WYY*(m2-m1**2)/2-WYY*m1**2/4)==0,
        functional_derivative_harmonics=s.trigsimp(s.expand_trig(cubic-target))==0,
        zero_amplitude=s.expand(localL.subs(ep, 0))==0)
    if not all(checks.values()):
        raise AssertionError(checks)
    return dict(checks=checks, quartic_action=str(derived),
        static_quartic=str(s.factor(derived.subs(vel, 0))),
        cubic_spatial_euler=str(target), moment_ratio=s.simplify(m2/m1**2),
        scope='Bare P+sW scalar vertices on fixed metric/clock; NOT constraint-reduced nonlinear evolution')


@lru_cache(maxsize=1)
def model_and_sample():
    archived = json.loads(ARCHIVE.read_text())['rows'][0]
    model = Model(.1, gamma=archived['gamma'])
    jets = model.jets(archived['tau'], archived['physical_Q']**2, 0.)
    return model, archived, jets


def snapshot():
    _, row, j = model_and_sample()
    errors = [abs(j[name]-row['jets'][key]) for key, name in
              dict(PX='P_X', PXX='P_XX', WY='W_Y', WYY='W_YY').items()]
    return dict(a=row['a'], physical_Q=row['physical_Q'], clock_rate=row['clock_rate'],
        PXX=float(j['P_XX']), WYY=float(j['W_YY']),
        s_WYY=float(row['clock_rate']*j['W_YY']),
        PXX_plus_sWYY=float(j['P_XX']+row['clock_rate']*j['W_YY']),
        jet_archive_max_error=float(max(errors)),
        interpretation='P reverses the isolated W cubic spatial-vertex sign here; not the sign of the constraint-reduced Hamiltonian')


def nonlinear_third(amp, points):
    model, row, _ = model_and_sample()
    phase = np.arange(points)*2*np.pi/points
    # k=a=1 for this dimensionless Fourier control; Q is actual, not qbar.
    grad = -amp*np.sin(phase)
    Y = grad**2
    j = model.jets(row['tau'], row['physical_Q']**2-Y, Y)
    flux = 2*(row['clock_rate']*j['W_Y']-j['P_X'])*grad
    # E_spatial=-d_x(flux); integrate by parts, no numerical differentiation.
    return float(-6*np.mean(flux*np.sin(3*phase)))


def flux_controls():
    coefficient = -1.5*snapshot()['PXX_plus_sWYY']
    rows = []
    for amp in (.01, .003, .001):
        fine = nonlinear_third(amp, 4096)/amp**3
        coarse = nonlinear_third(amp, 1024)/amp**3
        rows.append(dict(amplitude=amp, third_harmonic_over_amplitude_cubed=fine,
            analytic_coefficient=coefficient,
            relative_error=float(abs(fine-coefficient)/max(abs(coefficient), 1e-30)),
            quadrature_difference=float(abs(fine-coarse))))
    return rows


def linear_flux_third():
    phase = np.arange(1024)*2*np.pi/1024
    return float(-6*np.mean((-2*np.sin(phase))*np.sin(3*phase)))


def run():
    symbolic = dict(symbolic_vertices())
    symbolic['moment_ratio'] = str(symbolic['moment_ratio'])
    controls = flux_controls()
    if controls[-1]['relative_error'] >= 2e-4:
        raise AssertionError('Exact constitutive flux failed cubic convergence')
    return dict(symbolic=symbolic, snapshot=snapshot(), flux_controls=controls,
        linear_control_third_harmonic=linear_flux_third(),
        next_required='Solve second-order metric/clock constraints and include exchange, zero/2k responses and 3k scalar evolution; no coefficient reconstruction',
        full_theory_status='OPEN')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--result-file', type=Path, required=True)
    args = parser.parse_args()
    result = run()
    args.result_file.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
