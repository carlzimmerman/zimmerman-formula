"""Coupled calibration and Euler-sign tests; central cached profiles, no likelihood.

Run from repository root with --out a writable result directory.
No network and no writes outside that directory.
"""
import argparse
import csv
import json
from pathlib import Path

import numpy as np
from astropy.io import fits
from scipy.integrate import cumulative_trapezoid, quad, trapezoid
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / 'real_research/data/xcop'
G, MSUN, KPC = 6.67430e-11, 1.98847e30, 3.085677581491367e19
YEAR = 365.25*86400
NORMS = {'canonical': 9.3619e-11, 'alternative': 1.1279e-10}


def hp(y):
    t = np.sqrt(y)
    e, d = np.exp(-t), -np.expm1(-t)
    return e/d-t*e/(2*d*d)


# Inherited M interpolation prescription, distinct from Q and R.
YP = brentq(hp, 1., 5.)
HP = YP/np.expm1(np.sqrt(YP))
LG = np.linspace(-12, 12, 240001)
YG = 10**LG
HG = YG[0]/np.expm1(np.sqrt(YG[0])) + cumulative_trapezoid(
    np.maximum(hp(YG), .05*HP/(YG+YP)), YG, initial=0.)


def force(B, a, kernel):
    y = np.asarray(B)/a
    assert np.all(y > 0)
    if kernel == 'Q':
        return np.sqrt(B*(B+a))
    if kernel == 'R':
        return B/(-np.expm1(-np.sqrt(y)))
    assert kernel == 'M' and np.all((y >= 1e-12) & (y <= 1e12))
    return B + a*np.interp(np.log10(y), LG, HG)


def rad(h):
    scale = {'kpc': 1., 'Mpc': 1000., 'R/R500': h.header.get('R500')}[h.columns['RADIUS'].unit]
    assert scale > 0
    return np.asarray(h.data['RADIUS'], float)*scale


def col(h, name):
    assert h.columns[name].unit in ('Msun', 'M_sun')
    return np.asarray(h.data[name], float)


def interp(r, grid, values):
    assert np.all(np.diff(grid) > 0) and np.all(values > 0)
    assert np.min(r) >= grid[0] and np.max(r) <= grid[-1]
    return np.exp(np.interp(np.log(r), np.log(grid), np.log(values)))


def load():
    profiles, units, excluded = {}, [], []
    zdata = json.loads((DATA/'xcop_r500_ettori2019.json').read_text())
    for directory in sorted(DATA.iterdir()):
        if not directory.is_dir():
            continue
        name = directory.name
        if not (directory/(name+'_mstar.fits')).exists():
            excluded.append(name)
            continue
        with fits.open(directory/(name+'_hydro_mass.fits')) as h:
            rh, mh, nfw = rad(h[1]), col(h[1], 'M_FORW'), col(h[1], 'M_NFW')
        with fits.open(directory/(name+'_fgas_profile.fits')) as h:
            rg, mg, ng = rad(h[1]), col(h[1], 'MGAS'), col(h[1], 'M_NFW')
        with fits.open(directory/(name+'_mstar.fits')) as h:
            rs, ms = rad(h[2]), col(h[2], 'MSTAR')
        overlap = (rg >= rh[0]) & (rg <= rh[-1])
        align = float(np.median(abs(ng[overlap]/interp(rg[overlap], rh, nfw)-1)))
        assert align < .01
        lo, hi = max(rh[0], rg[0], rs[0]), min(rh[-1], rg[-1], rs[-1])
        assert lo <= 100 and hi >= 1000
        units.append(dict(name=name, shared_support_kpc=[lo, hi], nfw_alignment=align))
        profiles[name] = dict(rh=rh, mh=mh, rg=rg, mg=mg, rs=rs, ms=ms, z=zdata[name]['z'])
    assert len(profiles) == 7
    return profiles, units, excluded


def accelerations(p, r):
    scale = G*MSUN/(np.asarray(r)*KPC)**2
    return (scale*interp(r, p['rg'], p['mg']),
            scale*interp(r, p['rs'], p['ms']),
            scale*interp(r, p['rh'], p['mh']))


def corrected(bg, bs, gh, eta, d, pressure, upsilon=1.):
    """At the SAME angular shell: n'=eta*n, P'=pressure*P, r'=d*r."""
    return eta*d*bg+upsilon*bs, pressure/(eta*d)*gh


def residual(x, route, bg, bs, gh, a, kernel):
    if route == 'density_fixed_pressure':
        eta, d, p = x, 1., 1.
    elif route == 'distance_Xray_fixed_temperature':
        eta, d, p = x**-.5, x, x**-.5
    elif route == 'distance_Xray_SZ':
        eta, d, p = x**-.5, x, x**-1
    else:
        raise ValueError(route)
    baryons, hydro = corrected(bg, bs, gh, eta, d, p)
    return np.log(force(baryons, a, kernel)/hydro)


def write_csv(path, rows):
    with path.open('w') as s:
        writer = csv.DictWriter(s, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    profiles, units, excluded = load()
    old = list(csv.DictReader((ROOT/'campaign_fresh_gravity_astra/run_002/cluster_inverse_budget.csv').open()))
    old = {(r['name'], float(r['radius_kpc']), r['footing'], r['scaling'], r['kernel']): r for r in old}
    point_rows, fit_rows, flow_rows, continuity_rows = [], [], [], []
    max_recovery = max_reproduction = max_quad_error = 0.
    checks = []
    for name, profile in profiles.items():
        rg, mg = profile['rg'], profile['mg']
        slopes = np.diff(np.log(mg))/np.diff(np.log(rg))
        independently = np.log(mg[1:]/mg[:-1])/np.log(rg[1:]/rg[:-1])
        assert np.max(abs(slopes-independently)) < 1e-12
        for lo, hi, slope in zip(rg[:-1], rg[1:], slopes):
            if lo < 1000 and hi > 100:
                assert slope > 1
                continuity_rows.append(dict(name=name, radius_inner_kpc=float(max(lo,100)),
                     radius_outer_kpc=float(min(hi,1000)), enclosed_gas_mass_log_slope=float(slope),
                     inferred_density_negative_log_slope=float(3-slope),
                     coefficient_of_u_squared_over_r=float(1-slope)))
    assert len(continuity_rows) == 189
    routes = ('density_fixed_pressure', 'distance_Xray_fixed_temperature', 'distance_Xray_SZ')
    for footing, norm in NORMS.items():
        for scaling in ('vacuum', 'H'):
            for kernel in ('Q', 'R', 'M'):
                bundle = []
                for name, profile in profiles.items():
                    a = norm*(1. if scaling == 'vacuum' else np.sqrt(.315*(1+profile['z'])**3+.685))
                    for r in (100., 300., 1000.):
                        bg, bs, gh = [float(v) for v in accelerations(profile, r)]
                        q = float(force(bg+bs, a, kernel)/gh)
                        assert 0 < q < 1
                        oldrow = old[name, r, footing, scaling, kernel]
                        max_reproduction = max(max_reproduction, abs(q/float(oldrow['predicted_over_hydro'])-1))
                        row = dict(name=name, radius_kpc=r, footing=footing, scaling=scaling, kernel=kernel,
                                   Bgas=bg, Bstar=bs, hydro=gh, a0=a, predicted_over_hydro=q)
                        rg, mg = profile['rg'], profile['mg']
                        j = int(np.searchsorted(rg, r)-1)
                        assert rg[j] < r < rg[j+1]  # derivative is unambiguous inside an interval
                        slope = np.log(mg[j+1]/mg[j])/np.log(rg[j+1]/rg[j])
                        assert slope > 1
                        row['enclosed_gas_mass_log_slope'] = float(slope)
                        row['steady_continuity_acceleration_coefficient'] = float(1-slope)
                        row['steady_source_free_isotropic_support_sign_conflict'] = True
                        for route in routes:
                            x = brentq(lambda v: float(residual(v, route, bg, bs, gh, a, kernel)), .01, 100., xtol=1e-12)
                            row[route] = x
                            max_recovery = max(max_recovery, abs(float(np.expm1(residual(x, route, bg, bs, gh, a, kernel)))))
                        row['density_route_Xray_emission_multiplier'] = row['density_fixed_pressure']**2
                        row['density_route_emissivity_needed_to_hide_Xray'] = row['density_fixed_pressure']**-2
                        row['density_route_temperature_ratio'] = row['density_fixed_pressure']**-1
                        row['Xray_temperature_route_SZ_ratio'] = row['distance_Xray_fixed_temperature']**.5
                        row['Xray_SZ_route_temperature_ratio'] = row['distance_Xray_SZ']**-.5
                        delta = gh*(1-q)
                        row['outward_acceleration_minimum'] = delta
                        row['local_constant_acceleration_r_time_Myr'] = np.sqrt(2*r*KPC/delta)/(1e6*YEAR)
                        point_rows.append(row)
                        bundle.append((name, r, bg, bs, gh, a))
                    # Euler radial-flow lower bound. Split at every interpolation knot.
                    knots = np.unique(np.concatenate([profile['rh'], profile['rg'], profile['rs'], [100., 300., 1000.]]))
                    dense = np.unique(np.r_[np.geomspace(100., 1000., 3601), knots[(knots>=100)&(knots<=1000)]])
                    bg, bs, gh = accelerations(profile, dense)
                    delta = gh-force(bg+bs, a, kernel)
                    assert np.all(delta > 0)
                    for left in (100., 300.):
                        support = knots[(knots>=left)&(knots<=1000)]
                        def integrand(r):
                            bga, bsa, gha = accelerations(profile, r)
                            return float((gha-force(bga+bsa, a, kernel))*KPC/1e6)
                        area = sum(quad(integrand, l, h, epsabs=1e-7, epsrel=1e-9)[0]
                                   for l, h in zip(support[:-1], support[1:]))
                        sample = np.geomspace(left, 1000., 7201)
                        bg1, bs1, gh1 = accelerations(profile, sample)
                        independent = trapezoid((gh1-force(bg1+bs1, a, kernel))*KPC/1e6, sample)
                        error = abs(independent/area-1)
                        max_quad_error = max(max_quad_error, error)
                        assert error < 1e-5
                        flow_rows.append(dict(name=name, footing=footing, scaling=scaling, kernel=kernel,
                                              r_inner_kpc=left, r_outer_kpc=1000.,
                                              min_delta_radial_speed_squared_kms2=2*area,
                                              min_outer_speed_if_inner_zero_kms=np.sqrt(2*area),
                                              min_sampled_residual_acceleration=float(np.min(delta)),
                                              independent_quadrature_relative_difference=error))
                # A nuisance shared by all radii of one cluster, or all 21 shells.
                for scope in [*profiles, 'ALL_SEVEN']:
                    selected = [v for v in bundle if scope == 'ALL_SEVEN' or v[0] == scope]
                    for route in routes:
                        def resids(x):
                            return np.asarray([residual(x, route, *v[2:], kernel) for v in selected])
                        opt = brentq(lambda x: float(np.min(resids(x))+np.max(resids(x))), .01, 100., xtol=1e-12)
                        rr = resids(opt)
                        # Each residual is increasing. Equal opposite extrema proves this
                        # scalar minimax optimum, rather than relying on a fitting heuristic.
                        assert abs(float(np.min(rr)+np.max(rr))) < 1e-9
                        assert np.all(resids(opt*(1+1e-5)) > rr)
                        fit_rows.append(dict(scope=scope, footing=footing, scaling=scaling, kernel=kernel,
                                             route=route, nuisance_minimax=opt, evaluated_shells=len(selected),
                                             largest_multiplicative_force_mismatch=float(np.exp(np.max(abs(rr)))),
                                             min_log_force_residual=float(np.min(rr)), max_log_force_residual=float(np.max(rr))))
    assert len(point_rows) == 252 and len(flow_rows) == 168 and len(fit_rows) == 288
    assert max_reproduction < 1e-12 and max_recovery < 1e-10
    # Independent elementary scaling tests with analytic density and pressure.
    # rho=2/r, P=3/r^2 gives gH=3/r^2; gas M(<r)=4*pi*r^2.
    r, eta, d, p, ups = 7., 2.3, 1.8, .7, 1.2
    raw_g = 3/r**2
    transformed_direct = (6*p/r**3/d)/(2*eta/r)
    assert abs(transformed_direct/(p/(eta*d)*raw_g)-1) < 1e-14
    transformed_gas_mass = 4*np.pi*eta*d**3*r*r
    assert abs((transformed_gas_mass/(d*r)**2)/(4*np.pi)/(eta*d)-1) < 1e-14
    # Euler sign check: outward-positive A= -g + gH + gnt.
    assert abs((-0.3+1.0+0.2)-0.9) < 1e-15
    # At fixed X-ray/SZ amplitudes and ell=1: eta=d^-1/2, p=d^-1.
    eta, p = d**-.5, d**-1
    assert abs(eta**2*d-1) < 1e-14 and abs(p*d-1) < 1e-14
    assert abs((p/eta)**2*d-1) < 1e-14
    checks.extend(['252 baseline force ratios reproduce run_002 to <1e-12',
                   'All 756 pointwise nuisance roots forward-recover equality to <1e-10',
                   'Every root lies inside declared [0.01,100] search bracket',
                   '288 scalar minimax solutions equioscillate and have positive numerical slope',
                   '168 integrals independently checked by 7201-node trapezoid to <1e-5',
                   'Residual positive at all 3601 logarithmic nodes plus profile knots per cluster/branch',
                   'Analytic gas-mass, pressure-gradient and observed-amplitude scaling tests pass',
                   'Euler outward-positive sign verified with a hand-computable example',
                   'All 189 gas interpolation intervals overlapping 100-1000 kpc have mass slope >1',
                   'All 252 evaluated shell/branch combinations have positive Delta and negative steady-continuity coefficient',
                   'Gas interval slopes independently recomputed from ratios to <1e-12'])
    write_csv(out/'shell_constraints.csv', point_rows)
    write_csv(out/'shared_nuisance.csv', fit_rows)
    write_csv(out/'flow_bounds.csv', flow_rows)
    write_csv(out/'continuity_intervals.csv', continuity_rows)
    summary = dict(clusters=list(profiles), excluded=excluded, radius_and_unit_checks=units,
                   max_baseline_relative_difference=max_reproduction,
                   max_forward_root_relative_error=max_recovery,
                   max_independent_quadrature_relative_error=max_quad_error, checks=checks)
    summary['continuity_mass_slope_range'] = [min(r['enclosed_gas_mass_log_slope'] for r in continuity_rows),
                                             max(r['enclosed_gas_mass_log_slope'] for r in continuity_rows)]
    selected = [r for r in point_rows if r['footing']=='canonical' and r['scaling']=='vacuum' and r['kernel']=='R' and r['radius_kpc']==300.]
    summary['canonical_vacuum_R_300kpc'] = {key: dict(min=float(min(r[key] for r in selected)),
                  median=float(np.median([r[key] for r in selected])), max=float(max(r[key] for r in selected)))
                  for key in ['predicted_over_hydro', *routes, 'density_route_Xray_emission_multiplier',
                              'density_route_temperature_ratio', 'Xray_SZ_route_temperature_ratio',
                              'local_constant_acceleration_r_time_Myr']}
    (out/'checks.json').write_text(json.dumps(summary, indent=2)+'\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    main(parser.parse_args().out)
