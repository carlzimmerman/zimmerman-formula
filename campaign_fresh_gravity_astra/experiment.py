"""AFG-001: direct framework deductions and cached-profile diagnostics.

Run with --out DIR, an existing fresh computation-run directory.
No network, fitting, imported gravity solver, or shared-file writes.
"""
import argparse
import csv
import json
from pathlib import Path

import numpy as np
import sympy as sp
from astropy.io import fits
from scipy.integrate import cumulative_trapezoid, quad
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'real_research/data'
G, MSUN, KPC = 6.67430e-11, 1.98847e30, 3.085677581491367e19
A0 = {'canonical': 9.3619e-11, 'alternative': 1.1279e-10}


def hprime(y):
    t = np.sqrt(y)
    e = np.exp(-t)
    d = -np.expm1(-t)
    return e / d - t * e / (2 * d**2)


YP = brentq(hprime, 1., 5.)
HP = YP / np.expm1(np.sqrt(YP))
LOGGRID = np.linspace(-12, 12, 240001)
YGRID = 10**LOGGRID
HGRID = YGRID[0] / np.expm1(np.sqrt(YGRID[0])) + cumulative_trapezoid(
    np.maximum(hprime(YGRID), 0.05 * HP / (YGRID + YP)), YGRID, initial=0)


def f(y, kernel):
    y = np.asarray(y)
    if np.any(y <= 0):
        raise ValueError('Positive source required')
    if kernel == 'Q':
        return np.sqrt(y * (1 + y))
    if kernel == 'R':
        return y / (-np.expm1(-np.sqrt(y)))
    if kernel == 'M':
        if np.any((y < YGRID[0]) | (y > YGRID[-1])):
            raise ValueError('Outside pinned monotone-kernel grid')
        return y + np.interp(np.log10(y), LOGGRID, HGRID)
    raise ValueError(kernel)


def inverse(t, kernel):
    if kernel == 'Q':
        return 2 * t**2 / (np.sqrt(1 + 4 * t**2) + 1)
    return brentq(lambda y: float(f(y, kernel)) - t, 1e-12, max(1., t),
                  xtol=1e-24, rtol=1e-13)


def symbolic_and_spectral():
    b, a = sp.symbols('b a', positive=True)
    F = sp.sqrt(b*b + a*b)
    second = sp.simplify(sp.diff(F, b, 2))
    assert sp.simplify(second + a*a/(4*(b*b+a*b)**sp.Rational(3, 2))) == 0
    y = sp.symbols('y', positive=True)
    R = y/(1-sp.exp(-sp.sqrt(y)))
    R2 = sp.lambdify(y, sp.diff(R, y, 2), 'numpy')
    curvature_zero = brentq(R2, 5., 100.)
    curvature_errors = []
    for yy in [0.01, 0.1, 1., 10., 100.]:
        step = yy * 1e-3
        numerical = (f(yy+step, 'R')-2*f(yy, 'R')+f(yy-step, 'R'))/step**2
        curvature_errors.append(abs(numerical-R2(yy))/max(abs(R2(yy)), 1e-12))
    assert max(curvature_errors) < 1e-4

    w = np.array([0.10, 0.25, 0.30, 0.35])
    source = np.array([0.004, 0.015, 0.055, 0.15])  # B/a0
    response = f(source, 'Q')
    avg = lambda x: float(w @ x)
    variance = lambda x: avg((x-avg(x))**2)
    invariant = (avg(response**2)-avg(source**2))/avg(source)
    naive_mean = (avg(response)**2-avg(source)**2)/avg(source)
    correction = (variance(response)-variance(source))/avg(source)
    assert abs(invariant-1) < 1e-13
    assert abs(naive_mean+correction-1) < 1e-13
    assert naive_mean < 1

    # Constant r and projection factor: v_unit = sqrt(r*a0), u=sin(i)*sqrt(g/a0).
    sini = np.sin(np.deg2rad(60.))
    u = sini*np.sqrt(response)
    line_cases = []
    for sigma in [0.03, 0.15, 0.4]:
        def density(v):
            return float(np.sum(w*np.exp(-0.5*((v-u)/sigma)**2)/(sigma*np.sqrt(2*np.pi))))
        lo, hi = float(min(u)-12*sigma), float(max(u)+12*sigma)
        moments = [quad(lambda v: v**n*density(v), lo, hi, epsabs=1e-12)[0]
                   for n in [0, 2, 4]]
        m2, m4 = moments[1:]
        recovered4 = m4-6*sigma*sigma*m2+3*sigma**4
        a_est = (recovered4/sini**4-avg(source**2))/avg(source)
        wrong_s = 0.8*sigma
        wrong4 = m4-6*wrong_s**2*m2+3*wrong_s**4
        wrong_a = (wrong4/sini**4-avg(source**2))/avg(source)
        assert abs(moments[0]-1) < 1e-11 and abs(a_est-1) < 1e-10
        line_cases.append(dict(sigma_over_sqrt_r_a0=sigma, a_recovered=a_est,
                               a_with_20percent_underestimated_width=wrong_a))
    assert abs(line_cases[-1]['a_with_20percent_underestimated_width']-1) > .5

    inversions = {}
    for kernel in ['Q', 'R', 'M']:
        grid = np.logspace(-6, 6, 121)
        recovered = np.array([inverse(float(f(x, kernel)), kernel) for x in grid])
        error = float(np.max(abs(recovered/grid-1)))
        assert error < 1e-9
        inversions[kernel] = error
    return dict(quadrature_second_derivative=str(second),
                rar_curvature_zero_y=float(curvature_zero),
                rar_curvature_fd_max_relative_error=max(curvature_errors),
                inverse_max_relative_errors=inversions,
                moment_invariant=invariant, naive_mean_a0_ratio=naive_mean,
                variance_correction=correction, spectral_cases=line_cases)


def sparc():
    with (DATA/'sparc_master_clean.csv').open() as stream:
        catalog = {r['name']: r for r in csv.DictReader(stream)}
    rows, exclusions = [], {'catalog_quality_or_inclination': 0, 'invalid_points': 0}
    for file in sorted((DATA/'sparc_data').glob('*_rotmod.dat')):
        name = file.name.replace('_rotmod.dat', '')
        meta = catalog[name]
        if int(meta['Q']) > 2 or float(meta['inc']) < 30:
            exclusions['catalog_quality_or_inclination'] += 1
            continue
        points = np.loadtxt(file, comments='#', ndmin=2)
        for r, v, err, gas, disk, bulge, *_ in points:
            vbar2 = gas*abs(gas) + 0.5*disk**2 + 0.7*bulge**2
            if r <= 0 or v <= 0 or err <= 0 or vbar2 <= 0:
                exclusions['invalid_points'] += 1
                continue
            B, obs = vbar2*1e6/(r*KPC), v*v*1e6/(r*KPC)
            rows.append(dict(name=name, radius_kpc=float(r), B=float(B), obs=float(obs),
                             acceleration_discrepancy=float(obs/B), velocity_error_kms=float(err)))
    summary = []
    for footing, a0 in A0.items():
        for kernel in ['Q', 'R', 'M']:
            errors = np.array([np.log10(row['obs']/(a0*f(row['B']/a0, kernel))) for row in rows])
            names = sorted(set(row['name'] for row in rows))
            medians = [float(np.median([e for e, row in zip(errors, rows) if row['name']==name]))
                       for name in names]
            summary.append(dict(footing=footing, kernel=kernel, points=len(rows), galaxies=len(names),
                                median_residual_dex=float(np.median(errors)),
                                rms_residual_dex=float(np.sqrt(np.mean(errors**2))),
                                median_galaxy_median_dex=float(np.median(medians))))
    return rows, dict(selection=exclusions, summaries=summary)


def radius(hdu):
    col = hdu.columns['RADIUS']
    factor = {'kpc': 1., 'Mpc': 1000., 'R/R500': hdu.header.get('R500')}.get(col.unit)
    if factor is None or factor <= 0:
        raise ValueError('Unknown radius convention')
    return np.array(hdu.data['RADIUS'], float)*factor


def mass(hdu, name):
    assert hdu.columns[name].unit in ['Msun', 'M_sun']
    return np.array(hdu.data[name], float)


def interp(x, r, values):
    assert np.all(np.diff(r)>0) and np.all(r>0) and np.all(values>0)
    return np.exp(np.interp(np.log(x), np.log(r), np.log(values), left=np.nan, right=np.nan))


def clusters(galaxies):
    profiles, excluded, alignment = [], [], []
    redshifts = json.loads((DATA/'xcop/xcop_r500_ettori2019.json').read_text())
    for directory in sorted((DATA/'xcop').iterdir()):
        if not directory.is_dir():
            continue
        name = directory.name
        starfile = directory/(name+'_mstar.fits')
        if not starfile.exists():
            excluded.append(name)
            continue
        with fits.open(directory/(name+'_hydro_mass.fits')) as hd:
            rh, mh = radius(hd[1]), mass(hd[1], 'M_FORW')
            nfw = mass(hd[1], 'M_NFW')
        with fits.open(directory/(name+'_fgas_profile.fits')) as hd:
            rg, mg, ng = radius(hd[1]), mass(hd[1], 'MGAS'), mass(hd[1], 'M_NFW')
        with fits.open(starfile) as hd:
            rs, ms = radius(hd[2]), mass(hd[2], 'MSTAR')
        aligned = float(np.nanmedian(abs(ng/interp(rg, rh, nfw)-1)))
        assert aligned < .01
        alignment.append(dict(name=name, median_relative_shared_mass_mismatch=aligned))
        for r in [100., 300., 1000.]:
            gas, stars, hydro = float(interp(r, rg, mg)), float(interp(r, rs, ms)), float(interp(r, rh, mh))
            if not np.all(np.isfinite([gas, stars, hydro])):
                continue
            baryon = gas+stars
            B = G*baryon*MSUN/(r*KPC)**2
            obs = G*hydro*MSUN/(r*KPC)**2
            matched = [row for row in galaxies if abs(np.log10(row['B']/B))<=.1]
            # Each galaxy contributes once to the matched diagnostic.
            by_galaxy = {}
            for row in matched:
                by_galaxy.setdefault(row['name'], []).append(np.log10(row['obs']/row['B']))
            matched_med = float(np.median([np.median(v) for v in by_galaxy.values()])) if matched else None
            z = redshifts[name]['z']
            E = np.sqrt(.315*(1+z)**3+.685)
            for footing, norm in A0.items():
                for scaling, factor in [('vacuum', 1.), ('H', E)]:
                    a0 = norm*factor
                    for kernel in ['Q', 'R', 'M']:
                        predicted = float(a0*f(B/a0, kernel))
                        source = a0*inverse(obs/a0, kernel)
                        profiles.append(dict(name=name, radius_kpc=r, redshift=z, footing=footing,
                            scaling=scaling, kernel=kernel, B=B, obs=obs, a0=a0,
                            baryonic_mass_msun=baryon, hydrostatic_equivalent_mass_msun=hydro,
                            predicted_over_hydro=predicted/obs,
                            extra_force_over_a0=(obs-predicted)/a0,
                            required_source_factor=source/B,
                            required_extra_source_msun=(source/B-1)*baryon,
                            matched_galaxies=len(by_galaxy),
                            matched_cluster_excess_dex=None if matched_med is None else float(np.log10(obs/B)-matched_med)))
    return profiles, dict(excluded_no_stellar_profile=excluded, unit_alignment=alignment)


def heterogeneity():
    rows = []
    for z in [0., .5, 1., 2., 3., 5.]:
        E = np.sqrt(.315*(1+z)**3+.685)
        # Deep-limit lognormal B: a_mean/a_true = exp(-s²/4).
        variance_log = 4*np.log(E)
        cv = np.sqrt(np.expm1(variance_log))
        rows.append(dict(z=z, E=float(E), H_branch_deep_velocity_ratio=float(E**.25),
                         log_variance_to_hide_H=float(variance_log),
                         source_cv_to_hide_H=float(cv),
                         intrinsic_line_m4_over_m2_squared_to_hide_H=float(E)))
    # Separate numerical quadrature checks the analytic lognormal half moment.
    tests = []
    for s2 in [.04, 1., 4.]:
        value = quad(lambda t: np.exp(.5*(-s2/2+np.sqrt(s2)*t)-t*t/2)/np.sqrt(2*np.pi),
                     -12, 12, epsabs=1e-12)[0]
        expected = np.exp(-s2/8)
        assert abs(value/expected-1)<1e-10
        tests.append(dict(log_variance=s2, ratio=value, analytic=expected))
    return dict(predictions=rows, quadrature_checks=tests,
                limitation='Deep-limit result requires negligible weight outside B << a0; lognormal is unbounded.')


def write_csv(path, rows):
    with path.open('w') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert args.out.is_dir()
    checks = symbolic_and_spectral()
    galaxy_rows, galaxy_summary = sparc()
    cluster_rows, cluster_meta = clusters(galaxy_rows)
    cluster_summary = []
    for footing in A0:
        for kernel in ['Q', 'R', 'M']:
            subset = [r for r in cluster_rows if r['footing']==footing and r['kernel']==kernel and r['scaling']=='vacuum']
            at300 = [r for r in subset if r['radius_kpc']==300]
            cluster_summary.append(dict(footing=footing, kernel=kernel, rows=len(subset),
                rows_needing_extra_source=int(sum(r['required_source_factor']>1 for r in subset)),
                source_factor_median_300kpc=float(np.median([r['required_source_factor'] for r in at300])),
                force_coverage_median_300kpc=float(np.median([r['predicted_over_hydro'] for r in at300]))))
    report = dict(checkpoint='AFG-001', checks=checks, sparc=galaxy_summary,
                  clusters=dict(metadata=cluster_meta, summaries=cluster_summary),
                  heterogeneity=heterogeneity())
    (args.out/'results.json').write_text(json.dumps(report, indent=2, allow_nan=False)+'\n')
    write_csv(args.out/'sparc_accelerations.csv', galaxy_rows)
    write_csv(args.out/'cluster_inverse_budget.csv', cluster_rows)
    print(json.dumps(report, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
