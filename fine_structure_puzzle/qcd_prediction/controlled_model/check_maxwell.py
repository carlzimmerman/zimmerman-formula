#!/usr/bin/env python3
"""Bounded exact-flux checks; no observational data, fits, or Monte Carlo."""
import argparse
import json
from pathlib import Path
import mpmath as mp


def serial(x):
    if isinstance(x, dict):
        return {k: serial(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [serial(v) for v in x]
    if isinstance(x, (mp.mpf, mp.mpc)):
        return mp.nstr(x, 65)
    return x


def fd1(f, x, step):
    return (f(x - 2*step) - 8*f(x-step) + 8*f(x+step) - f(x+2*step))/(12*step)


def fd2(f, x, step):
    return (-f(x+2*step) + 16*f(x+step) - 30*f(x) + 16*f(x-step) - f(x-2*step))/(12*step**2)


def tail_bound(a, offset, order, cutoff):
    """Bounds both tails of sum |n-offset|^order exp(-a(n-offset)^2)."""
    b = mp.mpf(cutoff+1)-abs(offset)
    ratio = ((b+1)/b)**order * mp.exp(-a*(2*b+1))
    assert b > 0 and ratio < 1
    return 2*b**order*mp.exp(-a*b*b)/(1-ratio)


def electric(u, x, e2, cutoff):
    ys = [mp.mpf(n)-x for n in range(-cutoff, cutoff+1)]
    q0 = min(y*y for y in ys)
    ws = [mp.exp(-u*(y*y-q0)) for y in ys]
    zscaled = mp.fsum(ws)
    # Separate the exactly minimal terms so logZ remains stable even at tiny gaps.
    degeneracy = sum(y*y == q0 for y in ys)
    exc = mp.fsum(w for y, w in zip(ys, ws) if y*y != q0)
    logz = -u*q0 + mp.log(degeneracy) + mp.log1p(exc/degeneracy)
    m1 = mp.fsum(y*w for y, w in zip(ys, ws))/zscaled
    m2 = mp.fsum(y*y*w for y, w in zip(ys, ws))/zscaled
    m4 = mp.fsum(y**4*w for y, w in zip(ys, ws))/zscaled
    delta = e2*mp.fsum((y*y-q0)*w for y, w in zip(ys, ws))/(2*zscaled)
    area = 2*u/e2
    energy = e2*m2/2
    chi = e2/(4*mp.pi**2) - e2**2*area*(m2-m1*m1)/(4*mp.pi**2)
    dlogcoupling_energy = energy - e2*u*(m4-m2*m2)/2
    return dict(logz=logz, energy=energy, delta=delta, chi=chi,
                e0=e2*q0/2, degeneracy=degeneracy, m2=m2,
                coupling_derivative=dlogcoupling_energy)


def magnetic(u, x, e2, cutoff):
    theta = 2*mp.pi*x
    v = mp.pi**2/u
    ks = range(-cutoff, cutoff+1)
    ws = [mp.exp(-v*k*k+1j*k*theta) for k in ks]
    zflux = mp.fsum(ws)
    k1 = mp.fsum(k*w for k, w in zip(ks, ws))/zflux
    k2 = mp.fsum(k*k*w for k, w in zip(ks, ws))/zflux
    area = 2*u/e2
    logz = mp.log(mp.sqrt(mp.pi/u)*zflux)
    prefactor_stress = 1/(2*area)
    flux_stress = -2*mp.pi**2*k2/(e2*area**2)
    return dict(logz=logz, energy=prefactor_stress+flux_stress,
                chi=(k2-k1*k1)/area, prefactor_stress=prefactor_stress,
                flux_stress=flux_stress, k2=k2)


def gaussian(t, cutoff):
    """Stable S(t), log S(t), M(t)=<k²>, and Var(k²), real t>0."""
    ws = [mp.exp(-t*k*k) for k in range(1, cutoff+1)]
    extra = 2*mp.fsum(ws)
    z = 1+extra
    m2 = 2*mp.fsum(k*k*w for k, w in enumerate(ws, 1))/z
    m4 = 2*mp.fsum(k**4*w for k, w in enumerate(ws, 1))/z
    return dict(z=z, logz=mp.log1p(extra), m2=m2, var=m4-m2*m2)


def flux4(alpha, r, cutoff, length=1):
    a = mp.pi/(2*alpha)
    mag, elec = gaussian(a*r, cutoff), gaussian(a/r, cutoff)
    rho = 3*a/length**4*(mag['m2']-elec['m2']/r**2)
    derivative = 3*a/length**4*(-mag['m2']+elec['m2']/r**2
        + a*r*mag['var']-a/r**3*elec['var'])
    return dict(logz=3*(mag['logz']+elec['logz']), rho=rho,
                alpha_derivative_rho=derivative,
                alpha_derivative_logz=3*a*(r*mag['m2']+elec['m2']/r),
                stress_scale=3*a*(mag['m2']+elec['m2']/r**2)/length**4)


def general_flux4_logz(alpha, lengths, cutoff):
    volume = mp.fprod(lengths)
    a = mp.pi/(2*alpha)
    return mp.fsum(gaussian(a*volume/(lengths[i]**2*lengths[j]**2), cutoff)['logz']
                   for i in range(4) for j in range(i+1, 4))


def run(inputs, dps):
    mp.mp.dps = dps
    cutoff = inputs['numerics']['integer_cutoff']
    step = mp.mpf(inputs['numerics']['finite_difference_step'])
    sumtol = mp.mpf(inputs['numerics']['sum_relative_tolerance'])
    derivtol = mp.mpf(inputs['numerics']['derivative_relative_tolerance'])
    checks = []

    def check(name, error, scale, tol):
        normalized = abs(error)/max(abs(scale), mp.mpf('1e-400'))
        ok = normalized < tol
        checks.append(dict(name=name, normalized_error=normalized, tolerance=tol, passed=bool(ok)))
        if not ok:
            raise AssertionError('%s error=%s tolerance=%s' % (name, normalized, tol))

    rows2 = []
    for us in inputs['model_2d']['u_values']:
        u = mp.mpf(us)
        e2 = mp.mpf(inputs['model_2d']['coupling_e_squared'])
        area = 2*u/e2
        for xs in inputs['model_2d']['theta_over_two_pi']:
            x = mp.mpf(xs)
            e, m = electric(u, x, e2, cutoff), magnetic(u, x, e2, cutoff)
            label = 'u=%s,x=%s' % (us, xs)
            check('Poisson logZ '+label, e['logz']-m['logz'], 1+abs(e['logz']), sumtol)
            check('metric duality '+label, e['energy']-m['energy'], e['energy'], sumtol)
            check('susceptibility duality '+label, e['chi']-m['chi'], e['chi'], sumtol)
            d_area = -fd1(lambda aa: electric(e2*aa/2, x, e2, cutoff)['logz'], area, step)
            check('area derivative '+label, e['energy']-d_area, e['energy'], derivtol)
            d_theta = -fd2(lambda th: electric(u, th/(2*mp.pi), e2, cutoff)['logz'],
                           2*mp.pi*x, step)/area
            check('theta derivative '+label, e['chi']-d_theta, e['chi'], derivtol)
            d_coupling = e2*fd1(lambda gg: electric(gg*area/2, x, gg, cutoff)['energy'], e2, step)
            check('coupling derivative '+label, e['coupling_derivative']-d_coupling,
                  max(abs(e['energy']), abs(e['coupling_derivative'])), derivtol)
            ep = electric(u, x+1, e2, cutoff)
            em = electric(u, -x, e2, cutoff)
            check('theta periodicity '+label, e['logz']-ep['logz'], 1, sumtol)
            check('theta reflection '+label, e['logz']-em['logz'], 1, sumtol)
            rows2.append(dict(u=u, theta_over_two_pi=x, electric=e, magnetic=m,
                electric_m4_tail=tail_bound(u, x, 4, cutoff),
                flux_m4_tail=tail_bound(mp.pi**2/u, 0, 4, cutoff),
                intensive_action=-e['logz']/area))

    # Haar normalization and gluing: numerical integration of independently built kernels.
    def kernel(u, phi):
        return 1+2*mp.fsum(mp.exp(-u*n*n)*mp.cos(n*phi) for n in range(1, 31))
    norm = mp.quad(lambda phi: kernel(mp.mpf('.7'), phi), [-mp.pi, 0, mp.pi])/(2*mp.pi)
    glue = mp.quad(lambda phi: kernel(mp.mpf('.7'), phi)*kernel(mp.mpf('1.1'), -phi),
                   [-mp.pi, 0, mp.pi])/(2*mp.pi)
    check('normalized Haar kernel', norm-1, 1, sumtol)
    check('sphere gluing independent Haar integral', glue-gaussian(mp.mpf('1.8'), cutoff)['z'], 1, sumtol)

    spheres = []
    for hs in inputs['model_2d']['h_over_e_sphere']:
        h = mp.mpf(hs)
        u = 2*mp.pi/h**2  # e²=1, A=4π/H².
        e, m = electric(u, mp.mpf(0), mp.mpf(1), cutoff), magnetic(u, mp.mpf(0), mp.mpf(1), cutoff)
        check('sphere stress duality h='+hs, e['energy']-m['energy'], e['energy'], sumtol)
        spheres.append(dict(h_over_e=h, u=u, energy_over_e2=e['energy'],
            energy_over_He=e['energy']/h,
            energy_over_leading_exp=e['energy']/mp.exp(-u),
            chi_over_infinite_limit=e['chi']*4*mp.pi**2,
            prefactor_stress=m['prefactor_stress'], summed_flux_stress=m['flux_stress']))

    rows4 = []
    for alpha_label in inputs['model_4d']['alpha_M_labels']:
        numerator, denominator = alpha_label.split('/')
        alpha = mp.mpf(numerator)/mp.mpf(denominator)
        for rs in inputs['model_4d']['aspect_ratios']:
            r = mp.mpf(rs)
            f = flux4(alpha, r, cutoff)
            label = 'alpha=%s,r=%s' % (alpha_label, rs)
            metric_fd = -fd1(lambda rr: flux4(alpha, rr, cutoff)['logz'], r, step)
            check('4D beta metric derivative '+label, f['rho']-metric_fd, f['stress_scale'], derivtol)
            # Differentiate all six independently constructed bundle actions.
            lengths = [r, mp.mpf(1), mp.mpf(1), mp.mpf(1)]
            volume = r
            tensor = []
            for i in range(4):
                def variation(s):
                    ls = list(lengths)
                    ls[i] *= mp.exp(s)
                    return general_flux4_logz(alpha, ls, cutoff)
                tensor.append(-mp.diff(variation, 0)/volume)
            check('4D independent six-flux beta derivative '+label, tensor[0]-f['rho'], f['stress_scale'], sumtol)
            check('4D metric trace '+label, mp.fsum(tensor), f['stress_scale'], sumtol)
            check('4D aspect inversion '+label, f['logz']-flux4(alpha, 1/r, cutoff)['logz'], f['logz'], sumtol)
            scaled = flux4(alpha, r, cutoff, mp.mpf(3))
            check('4D inverse-fourth-length scaling '+label, f['rho']-81*scaled['rho'], f['stress_scale'], sumtol)
            d_alpha_rho = mp.diff(lambda aa: flux4(aa, r, cutoff)['rho'], alpha)*alpha
            d_alpha_logz = mp.diff(lambda aa: flux4(aa, r, cutoff)['logz'], alpha)*alpha
            check('4D alpha derivative energy '+label, f['alpha_derivative_rho']-d_alpha_rho,
                  f['stress_scale']*(1+mp.pi/(2*alpha)), sumtol)
            check('4D alpha derivative logZ '+label, f['alpha_derivative_logz']-d_alpha_logz,
                  f['alpha_derivative_logz'], sumtol)
            if r == 1:
                assert f['rho'] == 0
                assert f['alpha_derivative_rho'] == 0
                assert all(abs(t) < sumtol*f['stress_scale'] for t in tensor)
            if alpha == mp.mpf(1)/2:
                check('4D self-dual stationary stress '+label, f['alpha_derivative_rho'], f['stress_scale'], sumtol)
                check('4D self-dual logZ derivative '+label, f['alpha_derivative_logz']-mp.mpf(3)/2, 1, sumtol)
            rows4.append(dict(alpha_label=alpha_label, alpha=alpha, aspect=r, observables=f,
                              euclidean_metric_components=tensor))

    return dict(precision=dps, cutoff=cutoff, cases_2d=len(rows2), cases_4d=len(rows4),
                checks=checks, all_checks_passed=all(c['passed'] for c in checks),
                rows_2d=rows2, sphere_rows=spheres, rows_4d=rows4,
                normalization=dict(haar_integral=norm, sphere_gluing_integral=glue))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--inputs', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    inputs = json.loads(Path(args.inputs).read_text())
    results = [run(inputs, dps) for dps in inputs['numerics']['precisions_decimal']]
    # Check the independently rerun precision against every displayed observable.
    lo, hi = results
    tol = mp.mpf(inputs['numerics']['precision_relative_tolerance'])
    precision_errors = []
    for lowrow, highrow in zip(lo['rows_2d'], hi['rows_2d']):
        for key in ['energy', 'chi', 'logz', 'delta', 'coupling_derivative']:
            a, b = lowrow['electric'][key], highrow['electric'][key]
            scale = max(abs(b), mp.mpf('1e-400'))
            err = abs(a-b)/scale
            assert err < tol, ('precision', key, err)
            precision_errors.append(err)
    for lowrow, highrow in zip(lo['rows_4d'], hi['rows_4d']):
        for key in ['logz', 'rho', 'alpha_derivative_rho', 'alpha_derivative_logz']:
            a, b = lowrow['observables'][key], highrow['observables'][key]
            # The coupling derivative is exactly zero at the self-dual coupling.
            # Normalize its rounding residual by the noncancelled stress scale,
            # as in the independent derivative check, not by a zero observable.
            scale = abs(b)
            if key in ['rho', 'alpha_derivative_rho']:
                scale = highrow['observables']['stress_scale']
            err = abs(a-b)/max(scale, mp.mpf('1e-400'))
            assert err < tol, ('precision4', key, err)
            precision_errors.append(err)
    result = dict(assertion_tested='Flux duality, metric/coupling derivatives, normalization, branches, and 4D scale/trace checks on the contracted finite grids.',
                  outcome='implementation and finite assertion verified in the stated range',
                  precision_max_relative_error=max(precision_errors),
                  floating_point_caveat='Arbitrary-precision floating checks; analytic Gaussian tail bounds do not certify all rounding errors.',
                  runs=results)
    Path(args.output).write_text(json.dumps(serial(result), indent=2)+'\n')
    print(json.dumps(dict(cases_2d_per_precision=hi['cases_2d'], cases_4d_per_precision=hi['cases_4d'],
                          checks_per_precision=len(hi['checks']), all_checks_passed=hi['all_checks_passed'],
                          max_precision_error=mp.nstr(max(precision_errors), 10)), indent=2))


if __name__ == '__main__':
    main()
