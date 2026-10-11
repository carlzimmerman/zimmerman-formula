"""Finite passing-stream capture during prescribed Plummer contraction.

G=M=1. Planar test particles; optional point-host Hill tide with r_H=1.
No self-gravity, target density, vacuum coupling, or inferred abundance.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

BI, BF, R0 = .5, .05, 2.
JVALUES = np.array([-.6, -.25, -.05, .05, .25, .6])
CHECKS = []


def check(name, passed, value=None):
    CHECKS.append(dict(name=name, passed=bool(passed), value=value))


def shape(t, duration, mode):
    if mode == 'initial':
        return BI, 0.
    if mode == 'final':
        return BF, 0.
    u = np.clip(t / duration, 0., 1.)
    return BI+(BF-BI)*(3*u*u-2*u*u*u), (BF-BI)*6*u*(1-u)/duration


def initial(energy, nphase=8):
    theta = np.repeat((np.arange(nphase)+.5)*2*np.pi/nphase, len(JVALUES))
    j = np.tile(JVALUES, nphase)
    er = np.column_stack((np.cos(theta), np.sin(theta)))
    et = np.column_stack((-np.sin(theta), np.cos(theta)))
    speed2 = 2*(energy+1/np.sqrt(R0**2+BI**2))
    vr = -np.sqrt(speed2-(j/R0)**2)
    return np.column_stack((R0*er, vr[:, None]*er+(j/R0)[:, None]*et, np.zeros(len(j))))


def diagnostics(z, b, omega):
    r2 = np.sum(z[..., :2]**2, axis=-1)
    potential = -1/np.sqrt(r2+b*b)
    energy = .5*np.sum(z[..., 2:4]**2, axis=-1)+potential-1.5*omega**2*z[..., 0]**2
    j = z[..., 0]*z[..., 3]-z[..., 1]*z[..., 2]
    return energy, j, np.sqrt(r2)


def closed(z, b, omega, tolerance=1e-7):
    energy, _, _ = diagnostics(z, b, omega)
    if omega == 0:
        return energy < -tolerance, -energy
    rh = (3*omega**2)**(-1/3)
    xl = np.sqrt(rh*rh-b*b)
    es = -1.5/rh+.5*b*b/rh**3
    margin = es-energy
    return (margin > tolerance) & (np.abs(z[..., 0]) < xl), margin


def rhs(omega, duration, mode, mutate=False):
    def evaluate(t, flat):
        z = flat.reshape(-1, 5)
        b, bd = shape(t, duration, mode)
        den = (np.sum(z[:, :2]**2, axis=1)+b*b)**1.5
        out = np.zeros_like(z)
        out[:, :2] = z[:, 2:4]
        out[:, 2:4] = -z[:, :2]/den[:, None]
        out[:, 2] += 2*omega*z[:, 3]+3*omega**2*z[:, 0]
        out[:, 3] -= 2*omega*z[:, 2]
        out[:, 4] = (-1 if mutate else 1)*b*bd/den
        return out.ravel()
    return evaluate


def run_cell(energy, duration, mode, environment, nphase=8, refined=False, mutate=False):
    omega = 0. if environment == 'isolated' else np.sqrt(1/3)
    z0 = initial(energy, nphase)
    n = len(z0)
    rtol, atol, step = (2e-12, 2e-14, .01) if refined else (1e-10, 1e-12, .02)
    fun = rhs(omega, duration, mode, mutate)
    # End exactly at contraction completion; freeze the potential thereafter.
    a = solve_ivp(fun, (0., duration), z0.ravel(), method='DOP853',
                  rtol=rtol, atol=atol, max_step=step, dense_output=True)
    if not a.success:
        raise RuntimeError(a.message)
    b = solve_ivp(fun, (duration, duration+12.), a.y[:, -1], method='DOP853',
                  rtol=rtol, atol=atol, max_step=step, dense_output=True)
    if not b.success:
        raise RuntimeError(b.message)
    ts = np.linspace(0., duration, int(np.ceil(duration/.02))+1)
    zs = a.sol(ts).T.reshape(-1, n, 5)
    bs = np.array([shape(float(t), duration, mode)[0] for t in ts])
    ec, jc, _ = diagnostics(zs, bs[:, None], omega)
    zc, zf = a.y[:, -1].reshape(n, 5), b.y[:, -1].reshape(n, 5)
    bi, _ = shape(0., duration, mode)
    bf, _ = shape(duration, duration, mode)
    e0, j0, _ = diagnostics(z0, bi, omega)
    ef, jf, _ = diagnostics(zf, bf, omega)
    capture, gap = closed(zc, bf, omega)
    final_capture, _ = closed(zf, bf, omega)
    initial_capture, _ = closed(z0, bi, omega)
    err = float(max(np.max(np.abs(ec-e0[None, :]-zs[:, :, 4])),
                    np.max(np.abs(ef-e0-zf[:, 4]))))
    # Midpoint residence quadrature; compare two grids, never count visits.
    occupations = []
    for dt in (.02, .01):
        times = duration+np.arange(int(round(12/dt)))*dt+dt/2
        zp = b.sol(times).T.reshape(-1, n, 5)
        ep, _, radii = diagnostics(zp, bf, omega)
        occupations.append([float(np.mean(radii < R)) for R in (.1, .5, 1.)])
        post_energy_error = float(np.max(np.abs(ep-ec[-1])))
    name = f'{environment}_{mode}_E{energy}_T{duration}_N{n}'
    if not mutate:
        check(name+'_work_identity', err < 2e-7, err)
        check(name+'_post_energy', post_energy_error < 2e-7, post_energy_error)
        check(name+'_initially_outside_closed_component', not np.any(initial_capture), int(initial_capture.sum()))
        check(name+'_closed_component_preserved', np.array_equal(capture, final_capture), [int(capture.sum()), int(final_capture.sum())])
        if environment == 'isolated':
            jerr = float(max(np.max(np.abs(jc-j0)), np.max(np.abs(jf-j0))))
            check(name+'_angular_momentum', jerr < 2e-7, jerr)
        else:
            xl = np.sqrt(1-bf*bf)
            circular = (gap > 1e-7) & (np.linalg.norm(zc[:, :2], axis=1) < xl)
            check(name+'_central_component_geometry', np.array_equal(capture, circular))
        if mode != 'contract':
            check(name+'_static_no_closed_capture', not np.any(capture), int(capture.sum()))
    return dict(name=name, environment=environment, mode=mode, energy_input=energy,
                duration=duration, n=n, work_error=err, post_energy_error=post_energy_error,
                capture_count=int(capture.sum()), final_capture_count=int(final_capture.sum()),
                minimum_abs_final_gap=float(np.min(np.abs(gap))),
                work_mean=float(np.mean(zf[:, 4])), energy_change_mean=float(np.mean(ef-e0)),
                late_residence_fractions=occupations[1],
                residence_grid_disagreement=float(np.max(np.abs(np.array(occupations[0])-occupations[1]))),
                captures_by_initial_j={str(j): int(np.sum(capture & np.isclose(j0, j)))
                                       for j in JVALUES},
                initial_j=j0.tolist(), final_energy=ef.tolist(),
                final_gap=gap.tolist(), capture_mask=capture.tolist(),
                final_positions=zf[:, :2].tolist(), work_per_parcel=zf[:, 4].tolist())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    # Orthogonal force/work benchmarks from finite differences of the potential.
    point = np.array([.31, -.27])
    omega, t, duration = np.sqrt(1/3), .7, 2.
    bb, bd = shape(t, duration, 'contract')
    h = 1e-5
    def pot(x, b):
        return -1/np.sqrt(np.dot(x, x)+b*b)-1.5*omega**2*x[0]**2
    grad = np.array([(pot(point+h*np.eye(2)[k], bb)-pot(point-h*np.eye(2)[k], bb))/(2*h) for k in range(2)])
    z = np.r_[point, 0., 0., 0.]
    check('force_gradient', np.max(np.abs(rhs(omega, duration, 'contract')(t, z)[2:4]+grad)) < 2e-8)
    pd = (pot(point, shape(t+h, duration, 'contract')[0])-pot(point, shape(t-h, duration, 'contract')[0]))/(2*h)
    check('work_partial_derivative', abs(pd-bb*bd/(np.dot(point, point)+bb*bb)**1.5) < 2e-8)
    xl = np.sqrt(1-bb*bb)
    check('hill_saddle_energy', abs(pot(np.array([xl, 0.]), bb)-(-1.5+.5*bb*bb)) < 1e-13)
    check('hill_saddle_force', abs(rhs(omega, duration, 'contract')(t, np.array([xl, 0., 0., 0., 0.]))[2]) < 1e-13)
    rows = []
    for environment in ('isolated', 'hill'):
        for energy in (.03, .3, .8):
            for mode, duration in [('initial', 2.), ('final', 2.), ('contract', .5), ('contract', 2.), ('contract', 8.)]:
                row = run_cell(energy, duration, mode, environment)
                rows.append(row)
                print(row['name'], 'capture', row['capture_count'], '/', row['n'], flush=True)
    refined = []
    for environment in ('isolated', 'hill'):
        ref = run_cell(.03, 2., 'contract', environment, refined=True)
        orig = next(r for r in rows if r['environment']==environment and r['mode']=='contract' and r['energy_input']==.03 and r['duration']==2.)
        check(environment+'_refined_classification', ref['capture_mask']==orig['capture_mask'])
        diff = float(np.max(np.abs(np.array(ref['final_energy'])-orig['final_energy'])))
        check(environment+'_refined_energies', diff < 3e-7, diff)
        refined.append(ref)
    mutation = run_cell(.03, 2., 'contract', 'isolated', mutate=True)
    check('wrong_work_sign_rejected', mutation['work_error'] > 1e-3, mutation['work_error'])
    result = dict(base_revision='43730771f161904fa9a77c8fb360dac732143344',
                  model='Finite planar Plummer contraction; optional fixed Hill tide; external work ledger',
                  cells=rows, refined=refined, mutation_work_error=mutation['work_error'],
                  checks=CHECKS, assertions=len(CHECKS), passed=sum(c['passed'] for c in CHECKS))
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print('checks', result['passed'], '/', result['assertions'])
    raise SystemExit(0 if result['passed']==result['assertions'] else 1)


if __name__ == '__main__':
    main()
