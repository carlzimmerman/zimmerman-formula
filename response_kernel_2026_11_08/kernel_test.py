#!/usr/bin/env python3
"""RK01: reproduce with the bounded-runner command in RESULT.txt.

No imports of historical research scripts. Reads native X-COP FITS directly.
This is an inverse-equilibrium and dispersion test, not a forward halo solve.
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import astropy
import numpy as np
import scipy
import sympy as sp
from astropy.io import fits
from scipy.integrate import quad
from scipy.optimize import nnls

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'real_research/data/xcop'
G, MS, KPC = 6.674e-11, 1.989e30, 3.0857e19  # original native loader conventions
MPC = 1000 * KPC
A0 = {'a0_1p2e-10': 1.2e-10, 'a0_1p1e-10': 1.1e-10}
NAMES = ['A1795', 'A2029', 'A2142', 'A2319', 'A644', 'A85', 'ZW1215']
AREF = 4 * math.pi * G * (MPC / 4)**2
ZREF = 4 * math.pi * G * (50 * KPC)**4


def glaw(gn, a0):
    return 0.5 * gn + np.sqrt(0.25 * gn**2 + a0 * gn)


def loginterp(r, mass, query, extrapolate=False):
    r, mass, query = np.asarray(r), np.asarray(mass), np.asarray(query)
    ok = np.isfinite(r) & np.isfinite(mass) & (r > 0) & (mass > 0)
    r, mass = r[ok], mass[ok]
    assert np.all(np.diff(r) > 0)
    y = np.interp(np.log(query), np.log(r), np.log(mass))
    if extrapolate:
        slope = np.log(mass[1]/mass[0])/np.log(r[1]/r[0])
        y = np.where(query < r[0], np.log(mass[0]) + slope*np.log(query/r[0]), y)
    else:
        y = np.where((query < r[0]) | (query > r[-1]), np.nan, y)
    return np.exp(y)


def load_cluster(name):
    folder = DATA/name
    with fits.open(folder/f'{name}_hydro_mass.fits') as h:
        hm = h[1].data.copy()
        r500 = float(h[1].header['R500'])
    with fits.open(folder/f'{name}_fgas_profile.fits') as h:
        gas = h[1].data.copy()
        rg500 = float(h[1].header['R500'])
    with fits.open(folder/f'{name}_mstar.fits') as h:
        stars = h[2].data.copy()
    hr, mh = np.array(hm['RADIUS'], float), np.array(hm['M_FORW'], float)
    gr, mg = np.array(gas['RADIUS'], float)*rg500, np.array(gas['MGAS'], float)
    sr, ms = np.array(stars['RADIUS'], float), np.array(stars['MSTAR'], float)
    def baryons(r, extrapolate=False):
        return loginterp(gr, mg, r, extrapolate)+loginterp(sr, ms, r, extrapolate)
    last = None
    for r in hr[::-1]:
        mb = float(baryons(r))
        if np.isfinite(mb):
            last = (float(r), mb, float(loginterp(hr, mh, r)))
            break
    assert last is not None
    rows = []
    for x in (0.1, 0.2, 0.3, 0.5, 0.7):
        r = x*r500
        mb, mo = float(baryons(r)), float(loginterp(hr, mh, r))
        if np.isfinite(mb) and np.isfinite(mo):
            rows.append({'r_kpc': r, 'Mb_Msun': mb, 'Mhse_Msun': mo, 'r_over_r500': x})
    return {'name': name, 'r500_kpc': r500, 'last': last,
            'baryons': baryons, 'rows': rows}


def density_functions(r, rc, rho0):
    x = np.asarray(r)/rc
    rho = rho0/(1+x*x)
    neg_first = 2*rho0*x/(rc*(1+x*x)**2)
    lap = 2*rho0*(x*x-3)/(rc*rc*(1+x*x)**3)
    lap_prime = 8*rho0*x*(5-x*x)/(rc**3*(1+x*x)**4)
    return rho, neg_first, lap, lap_prime


def enclosed(r, rc, rho0):
    x = np.asarray(r)/rc
    return 4*math.pi*rho0*rc**3*(x-np.arctan(x))


def fit_support(p, d, bmax=None):
    # Unitless coefficients a=A/AREF, b=zeta/ZREF. Target acceleration = 1.
    mat = np.column_stack([p, d])
    ab, _ = nnls(mat, np.ones_like(p))
    if bmax is not None and ab[1] > bmax:
        b = bmax
        a = max(0., float(np.dot(p, 1-b*d)/np.dot(p, p)))
        ab = np.array([a, b])
    support = mat@ab
    positive = bool(np.all(support > 0))
    return {'A_over_Aref': float(ab[0]), 'zeta_over_Zref': float(ab[1]),
            'mu_K_Mpc_inverse': None if ab[0] == 0 else 4/math.sqrt(ab[0]),
            'ell_kpc': 50*float(ab[1])**0.25,
            'fractional_support_rms': float(np.sqrt(np.mean((support-1)**2))),
            'log10_support_rms': float(np.sqrt(np.mean(np.log10(support)**2))) if positive else None,
            'all_support_positive': positive}


def exact_checks():
    n, Q, mu, A, z, q, rb, om = sp.symbols('n Q mu A z q rb om', positive=True)
    U = n+n*n/(4*mu*mu)
    ns = 2*mu*mu*(Q-1)
    assert sp.simplify((n*Q-U).subs(n, ns)-mu*mu*(Q-1)**2) == 0
    # Continuity: -i omega delta + i q v = 0.
    # Euler: -i omega v + i q rb (A+z q^2) delta = -i q Phi.
    det = sp.Matrix([[-sp.I*om, sp.I*q],
                     [sp.I*q*rb*(A+z*q*q), -sp.I*om]]).det()
    assert sp.simplify(det-(-om*om+rb*A*q*q+rb*z*q**4)) == 0
    r, rc, r0 = sp.symbols('r rc r0', positive=True)
    rho = r0/(1+(r/rc)**2)
    lap = sp.diff(r*r*sp.diff(rho, r), r)/(r*r)
    target = 8*r0*(r/rc)*(5-(r/rc)**2)/(rc**3*(1+(r/rc)**2)**4)
    assert sp.simplify(sp.diff(lap, r)-target) == 0
    # Independent numerical derivative and quadrature in dimensionless units.
    errors = []
    for step in (1e-3, 1e-4, 1e-5):
        errs = []
        for x in (0.1, 0.5, 1., 2., 3., 10.):
            fd = (density_functions(x+step, 1., 1.)[2]-density_functions(x-step, 1., 1.)[2])/(2*step)
            an = float(density_functions(x, 1., 1.)[3])
            errs.append(abs(fd-an)/max(abs(an), 1e-10))
        errors.append(max(errs))
    assert errors[-1] < 1e-7
    mass_errors = []
    for x in (0.1, 1., 10.):
        num = 4*math.pi*quad(lambda s: s*s/(1+s*s), 0, x, epsabs=1e-12)[0]
        mass_errors.append(abs(num/enclosed(x, 1., 1.)-1))
    assert max(mass_errors) < 1e-10
    # Exactly representable acceleration fixture; not observational data.
    xs = np.linspace(0.1, 1., 30)
    p, d = 1+xs, 1+xs*xs
    synthetic = 1.2*p+0.3*d
    sol, _ = nnls(np.column_stack([p, d]), synthetic)
    assert np.max(abs(sol-[1.2, 0.3])) < 1e-10
    return {'legendre_identity': True, 'kernel_determinant': str(sp.expand(det)),
            'radial_derivative_identity': True, 'finite_difference_max_errors': errors,
            'quadrature_max_relative_error': max(mass_errors),
            'synthetic_fit_error': float(np.max(abs(sol-[1.2, 0.3]))),
            'zero_zeta_limit': str(sp.expand(det).subs(z, 0)),
            'wrong_sign_mutation_detected': bool(sp.expand(det.subs(z, -z)).coeff(q, 4) < 0)}


def run(out_path, omit_redshift):
    checks = exact_checks()
    kcom, redshift = 0.3, 1100.
    qphysical = kcom*(1 if omit_redshift else 1+redshift)
    qcorrect = kcom*(1+redshift)
    unit_ratio = ((50*KPC)*(qcorrect/MPC))**4/(0.05*qcorrect)**4
    assert abs(unit_ratio-1) < 1e-14
    J50 = (0.05*qphysical)**4
    bmax = 1/J50
    kernel = {'z': redshift, 'kcom_max_Mpc_inverse': kcom,
              'qphysical_max_Mpc_inverse': qphysical,
              'physical_wavelength_kpc': [2*math.pi/(k*(1+redshift))*1000 for k in (0.3, 0.03)],
              'Jcap_at_ell_50kpc': J50, 'Jcap_at_ell_100kpc': (0.1*qphysical)**4,
              'ell_max_cold_kpc': 1000/qphysical,
              'ell_max_with_10x_gravity_kpc': 1000*10**0.25/qphysical,
              'correct_redshift_check': qphysical == qcorrect,
              'SI_vs_Mpc_ratio': unit_ratio}
    clusters = [load_cluster(n) for n in NAMES]
    assert len(clusters) == 7
    results = {}
    for footing, a0 in A0.items():
        results[footing] = {}
        for rc_kpc in (50., 75., 100.):
            rc = rc_kpc*KPC
            pp, dd, per, mass_residuals = [], [], {}, []
            for cl in clusters:
                rl, mbl, mol = cl['last']
                go = G*mol*MS/(rl*KPC)**2
                gn = go*go/(go+a0)
                mxlast = gn*(rl*KPC)**2/G-mbl*MS
                assert mxlast > 0
                assert abs(float(glaw(gn, a0))/go-1) < 1e-14
                xl = rl/rc_kpc
                rho0 = mxlast/(4*math.pi*rc**3*(xl-math.atan(xl)))
                r = np.geomspace(20., 0.7*cl['r500_kpc'], 120)*KPC
                mb = cl['baryons'](r/KPC, extrapolate=True)*MS
                mx = enclosed(r, rc, rho0)
                gravity = glaw(G*(mb+mx)/(r*r), a0)
                rho, p, lap, d = density_functions(r, rc, rho0)
                p, d = AREF*p/gravity, ZREF*d/gravity
                pp.extend(p); dd.extend(d)
                free = fit_support(p, d)
                bounded = fit_support(p, d, bmax)
                free['Jcap_recombination'] = free['zeta_over_Zref']*J50
                # Magnitude bound independent of fitted A; sign retained in rows.
                cap_fraction = bmax*d
                residuals = []
                rows = []
                for row in cl['rows']:
                    rm = row['r_kpc']*KPC
                    me = float(enclosed(rm, rc, rho0))/MS
                    mpred = float(glaw(G*(row['Mb_Msun']+me)*MS/rm**2, a0))*rm**2/G/MS
                    residual = math.log10(row['Mhse_Msun']/mpred)
                    residuals.append(residual); mass_residuals.append(residual)
                    rows.append(dict(row, MX_Msun=me, Mpred_Msun=mpred, delta_dex=residual))
                c = float(enclosed(.25*cl['r500_kpc']*KPC, rc, rho0)/
                          enclosed(.7*cl['r500_kpc']*KPC, rc, rho0))
                per[cl['name']] = {'r_last_kpc': rl, 'Mb_last_Msun': mbl,
                                  'MX_last_Msun': mxlast/MS, 'F_last': mxlast/MS/mbl,
                                  'rho0_kg_m3': rho0, 'concentration': c,
                                  'target_mass_rms_dex': float(np.sqrt(np.mean(np.array(residuals)**2))),
                                  'free_fit': free, 'CMB_bounded_fit': bounded,
                                  'max_cap_fraction_at_CMB_bound': float(np.max(abs(cap_fraction))),
                                  'max_cap_fraction_10x_gravity_bound': float(10*np.max(abs(cap_fraction))),
                                  'full_native_mass_rows': rows}
            pp, dd = np.array(pp), np.array(dd)
            free, bounded = fit_support(pp, dd), fit_support(pp, dd, bmax)
            free['Jcap_recombination'] = free['zeta_over_Zref']*J50
            bounded['Jcap_recombination'] = bounded['zeta_over_Zref']*J50
            # Force needed merely to make a 10% change somewhere on these targets.
            b10 = 0.1/np.max(abs(dd))
            results[footing][str(int(rc_kpc))] = {
                'common_free_fit': free, 'common_CMB_bounded_fit': bounded,
                'Jcap_for_10percent_cap_force_somewhere': float(b10*J50),
                'ell_for_10percent_cap_force_somewhere_kpc': 50*b10**0.25,
                'target_mass_rms_dex': float(np.sqrt(np.mean(np.array(mass_residuals)**2))),
                'native_mass_points': len(mass_residuals),
                'inverse_equilibrium_points': len(pp), 'clusters': per}
    all_cases = [v for ft in results.values() for v in ft.values()]
    summary = {'largest_cap_fraction_under_CMB_bound': max(
        p['max_cap_fraction_at_CMB_bound'] for v in all_cases for p in v['clusters'].values()),
        'least_Jcap_for_10percent_change': min(v['Jcap_for_10percent_cap_force_somewhere'] for v in all_cases),
        'candidate_status': 'not_a_full_solution; constant_coefficient_capillary_prescreen',
        'mutation_omits_redshift': omit_redshift}
    inputs = []
    for cl in NAMES:
        for suffix in ('hydro_mass', 'fgas_profile', 'mstar'):
            path = DATA/cl/f'{cl}_{suffix}.fits'
            inputs.append({'path': str(path.relative_to(ROOT)),
                           'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    output = {'assertion_tested': 'RK01 CONTRACT.txt; inverse equilibrium only, no forward halos',
              'software': {'python': sys.version, 'numpy': np.__version__, 'scipy': scipy.__version__,
                           'sympy': sp.__version__, 'astropy': astropy.__version__},
              'controls': checks, 'kernel': kernel, 'profiles': results,
              'summary': summary, 'raw_inputs': inputs}
    out_path = ROOT/out_path
    assert out_path.parent.is_dir()
    out_path.write_text(json.dumps(output, indent=2, allow_nan=False)+'\n')
    print(json.dumps({'kernel': kernel, 'summary': summary}, indent=2))
    for ft, cases in results.items():
        for rc, case in cases.items():
            print(ft, rc, json.dumps({'free': case['common_free_fit'],
                                     'bounded': case['common_CMB_bounded_fit'],
                                     'target_mass_rms_dex': case['target_mass_rms_dex']}))
    if omit_redshift:
        assert not kernel['correct_redshift_check'], 'mutation did not bite'
    else:
        assert kernel['correct_redshift_check']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--omit-redshift', action='store_true')
    args = parser.parse_args()
    run(args.output, args.omit_redshift)
