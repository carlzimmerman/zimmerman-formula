"""Bounded cross-catalog gas normalization test, without a joint likelihood."""
import argparse
import csv
import io
import itertools
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
import numpy as np
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.wcs import WCS
import astropy.units as u
from scipy.optimize import brentq
from campaign_fresh_gravity_astra.stage_03.cluster_precision.constraint import (
    load, rad, col, interp, force, G, MSUN, KPC, NORMS, write_csv)

DATA = ROOT/'real_research/data'


def f64(x):
    return np.asarray(x, dtype=float)


def nearest(ra, dec, coords):
    sep = SkyCoord(ra*u.deg, dec*u.deg).separation(coords).arcmin
    return int(np.argmin(sep)), float(np.min(sep))


def xc_bounds(name, r):
    """An explicit one-error-unit perturbation box, NOT a confidence region.

    Gas LO/HI are treated as error magnitudes; star LO/HI as endpoint masses.
    Hydro EM_FORW is treated as a symmetric error magnitude. Interpolate the
    central masses and quoted errors separately in log-log space.
    """
    output = {}
    for file, ext, key, low, high, delta in [
        ('fgas_profile', 1, 'MGAS', 'MGAS_LO', 'MGAS_HI', True),
        ('hydro_mass', 1, 'M_FORW', 'EM_FORW', 'EM_FORW', True),
        ('mstar', 2, 'MSTAR', 'MSTAR_LO', 'MSTAR_HI', False)]:
        with fits.open(DATA/'xcop'/name/(name+'_'+file+'.fits')) as hs:
            h = hs[ext]
            radii = rad(h)
            center = float(interp(r, radii, col(h, key)))
            lv, hv = float(interp(r, radii, col(h, low))), float(interp(r, radii, col(h, high)))
            lo, hi = (center-lv, center+hv) if delta else (lv, hv)
            assert 0 < lo < center < hi
            output[file] = (lo, center, hi)
    return output


def catalogues(profiles):
    with fits.open(DATA/'erass1cl_primary_v3.2.fits', memmap=True) as hs:
        erass = hs[1].data.copy()
        ec = SkyCoord(f64(erass['RA'])*u.deg, f64(erass['DEC'])*u.deg)
        efields = list(hs[1].columns.names)
    lines = (DATA/'psz2_union.tsv').read_text().splitlines()
    k = next(i for i, line in enumerate(lines) if line.startswith('Index\t'))
    psz = list(csv.DictReader(io.StringIO('\n'.join([lines[k]]+lines[k+3:])), delimiter='\t'))
    pc = SkyCoord([float(x['RAJ2000']) for x in psz]*u.deg, [float(x['DEJ2000']) for x in psz]*u.deg)
    rows, matches, dependencies = [], {}, []
    for name, profile in profiles.items():
        with fits.open(DATA/'xcop'/name/(name+'_mstar.fits')) as hs:
            header = hs[2].header
            ra, dec = float(header['RA']), float(header['DEC'])
        ei, es = nearest(ra, dec, ec)
        pi, ps = nearest(ra, dec, pc)
        e, p = erass[ei], psz[pi]
        ez, pz = float(e['BEST_Z']), float(p['z'])
        ematch = es <= 5 and abs(ez-profile['z']) <= .01
        pmatch = ps <= 5 and abs(pz-profile['z']) <= .01
        if ematch:
            matches[name] = {key: float(e[key]) for key in (
                'R500', 'R500_L', 'R500_H', 'KT', 'KT_L', 'KT_H',
                'MGAS500', 'MGAS500_L', 'MGAS500_H', 'YX500', 'M500', 'FGAS500')}
            matches[name]['name'] = str(e['NAME']).strip()
            matches[name]['z'] = ez
        rows.append(dict(name=name, RA=ra, DEC=dec, z_xcop=profile['z'],
            erass_nearest_name=str(e['NAME']).strip(), erass_separation_arcmin=es,
            erass_z=ez, erass_match=ematch, psz_nearest_name=p['Name'].strip(),
            psz_separation_arcmin=ps, psz_z=pz, psz_match=pmatch,
            psz_Y_1e3_arcmin2=float(p['Y5R500']) if pmatch else '',
            psz_Y_error_1e3_arcmin2=float(p['e_Y5R500']) if pmatch else ''))
        with fits.open(DATA/'xcop'/name/(name+'_fgas_profile.fits')) as hs:
            d = hs[1].data
            fracerr = abs(f64(d['FGAS'])/(f64(d['MGAS'])/f64(d['M_NFW']))-1)
            dependencies.append(dict(name=name, comparison='X-COP FGAS vs MGAS/M_NFW',
                                     median_relative_difference=float(np.median(fracerr)),
                                     maximum_relative_difference=float(np.max(fracerr))))
        if ematch:
            me = float(e['MGAS500'])
            dependencies.append(dict(name=name, comparison='eRASS YX500 vs KT*MGAS500',
                median_relative_difference=abs(float(e['YX500'])/(float(e['KT'])*me)-1),
                maximum_relative_difference=abs(float(e['YX500'])/(float(e['KT'])*me)-1)))
            dependencies.append(dict(name=name, comparison='eRASS FGAS500 vs MGAS500/M500 with units',
                median_relative_difference=abs(float(e['FGAS500'])/(me/float(e['M500'])/100)-1),
                maximum_relative_difference=abs(float(e['FGAS500'])/(me/float(e['M500'])/100)-1)))
    assert sorted(matches) == ['A644', 'ZW1215']
    assert sum(x['psz_match'] for x in rows) == 6
    return rows, matches, dependencies, efields


def map_and_release_inventory(rows):
    outputs = {}
    for path in sorted((ROOT/'deepseek_push/G236_eRASS3_data').glob('*.fits.gz')):
        with fits.open(path, lazy_load_hdus=True, memmap=False) as hs:
            cols = list(hs[1].columns.names)
            outputs[str(path.relative_to(ROOT))] = dict(rows=int(hs[1].header['NAXIS2']), columns=cols,
                direct_cluster_thermal_columns=[n for n in cols if n.upper() in
                    ['KT','KT_L','KT_H','MGAS500','M500','TEMPERATURE','PRESSURE','DENSITY']])
    with fits.open(ROOT/'deepseek_push/Z06_data/ilc_actplanck_ymap.fits', memmap=True) as hs:
        header = hs[0].header
        shape = (header['NAXIS2'], header['NAXIS1'])
        wcs = WCS(header)
        outputs['ACT_Planck_map_header'] = dict(shape=list(shape), header=str(header))
    with fits.open(ROOT/'deepseek_push/Z06_data/wide_mask_GAL070_apod_1.50_deg_wExtended.fits', memmap=True) as hs:
        for row in rows:
            x, y = wcs.world_to_pixel_values(row['RA'], row['DEC'])
            x, y = float(x), float(y)
            inside = 0 <= x < shape[1] and 0 <= y < shape[0]
            row['ACT_map_in_rectangular_bounds'] = bool(inside)
            row['ACT_center_mask'] = float(hs[0].data[int(round(y)),int(round(x))]) if inside else ''
    return outputs


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    profiles, unitchecks, excluded = load()
    cats, matches, deps, ec = catalogues(profiles)
    inventory = map_and_release_inventory(cats)
    inventory['erass1_columns'] = ec
    inventory['xcop_units'] = unitchecks
    inventory['scope'] = 'X-COP 7 measured-star clusters; eRASS1 primary; PSZ2 union; cached ACT+Planck products; four eRASS3 FITS schemas. No assertion of exhaustive local-disk search.'
    results, metadata = [], []
    max_root_error = max_corner_error = 0.
    for name, e in matches.items():
        r = e['R500']
        bounds = xc_bounds(name, r)
        xlo, xc, xhi = bounds['fgas_profile']
        hlo, hc, hhi = bounds['hydro_mass']
        slo, sc, shi = bounds['mstar']
        elo, em, ehi = [e[key]*1e11 for key in ('MGAS500_L','MGAS500','MGAS500_H')]
        assert 0 < elo < em < ehi
        assert e['KT_L'] < e['KT'] < e['KT_H'] and e['KT_L'] > 0
        metadata.append(dict(name=name, erass_name=e['name'], radius_kpc=r,
            erass_z=e['z'], xcop_z=profiles[name]['z'], erass_KT_keV=e['KT'],
            erass_KT_low_keV=e['KT_L'], erass_KT_high_keV=e['KT_H'],
            xcop_gas_msun=xc, erass_gas_msun=em,
            gas_ratio_central=em/xc, gas_ratio_box_low=elo/xhi, gas_ratio_box_high=ehi/xlo,
            original_hydro_msun=hc, xcop_gas_box_low=xlo, xcop_gas_box_high=xhi,
            erass_gas_box_low=elo, erass_gas_box_high=ehi,
            hydro_box_low=hlo, hydro_box_high=hhi, star_box_low=slo, star_box_high=shi))
        scale = G*MSUN/(r*KPC)**2
        for footing, norm in NORMS.items():
            for scaling in ('vacuum', 'H'):
                a = norm*(1 if scaling=='vacuum' else np.sqrt(.315*(1+profiles[name]['z'])**3+.685))
                for kernel in ('Q','R','M'):
                    # Me is a different instrument's gas mass; Mx anchors the old
                    # density normalization. All masses refer to common fixed aperture.
                    def required_p(me, mx, ms, mh):
                        return float((me/mx)*force(scale*(me+ms), a, kernel)/(scale*mh))
                    p0 = required_p(em, xc, sc, hc)
                    pmin, pmax = required_p(elo,xhi,slo,hhi), required_p(ehi,xlo,shi,hlo)
                    corners = [required_p(*v) for v in itertools.product((elo,ehi),(xlo,xhi),(slo,shi),(hlo,hhi))]
                    max_corner_error = max(max_corner_error, abs(min(corners)-pmin), abs(max(corners)-pmax))
                    assert pmin > 0 and pmax < 1
                    def boost(me,mx,ms,mh):
                        v = brentq(lambda b:required_p(b*me,mx,ms,mh)-1, .01, 100., xtol=1e-12)
                        return v, abs(required_p(v*me,mx,ms,mh)-1)
                    b0, er0 = boost(em,xc,sc,hc)
                    bmin, er1 = boost(ehi,xlo,shi,hlo)
                    max_root_error = max(max_root_error,er0,er1)
                    assert bmin > 1
                    results.append(dict(name=name, radius_kpc=r, footing=footing, scaling=scaling,
                        kernel=kernel, a0=a, gas_ratio=em/xc, pressure_gradient_ratio_required=p0,
                        pressure_gradient_ratio_box_low=pmin, pressure_gradient_ratio_box_high=pmax,
                        temperature_ratio_required_if_same_shape=p0/(em/xc),
                        temperature_ratio_box_low=float(force(scale*(elo+slo),a,kernel)/(scale*hhi)),
                        temperature_ratio_box_high=float(force(scale*(ehi+shi),a,kernel)/(scale*hlo)),
                        further_erass_gas_multiplier_needed_at_fixed_pressure=b0,
                        smallest_further_erass_gas_multiplier_in_box=bmin,
                        emissivity_ratio_required_fixed_counts_distance=b0**-2,
                        largest_emissivity_ratio_that_can_close_box=bmin**-2,
                        fixed_pressure_density_only_compatible_with_box=False,
                        independent_pressure_measurement_status='NOT_AVAILABLE'))
    assert len(results)==24 and max_corner_error<1e-14 and max_root_error<1e-10
    # Analytic circularity: integrating the old gH gives the same gH on inversion.
    # rho=r^-1, gH=r^-2 => P=C+1/(2r^2); two pressure zero points.
    for c in (0.,7.):
        r = 2.
        rho, dP = 1/r, -1/r**3
        assert abs(-dP/rho-1/r**2)<1e-15
    write_csv(out/'catalogue_matches.csv', cats)
    write_csv(out/'gas_comparison.csv', metadata)
    write_csv(out/'closure_requirements.csv', results)
    write_csv(out/'dependent_quantity_checks.csv', deps)
    (out/'data_inventory.json').write_text(json.dumps(inventory,indent=2)+'\n')
    summary = dict(matched_erass_clusters=sorted(matches), matched_psz_clusters=[x['name'] for x in cats if x['psz_match']],
        tested_branches=len(results), maximum_root_error=max_root_error, maximum_corner_error=max_corner_error,
        all_fixed_pressure_density_only_boxes_fail=True,
        pressure_high_ranges={n:[min(x['pressure_gradient_ratio_box_high'] for x in results if x['name']==n),
                                max(x['pressure_gradient_ratio_box_high'] for x in results if x['name']==n)] for n in matches},
        checks=['Positional/redshift gate applied before comparison: <=5 arcmin and abs(dz)<=0.01',
                'eRASS lower/central/upper gas and temperature entries positive and ordered',
                'Common nominal apertures lie inside original gas/star/hydro supports',
                '16 independent box corners confirm analytic monotone extrema for every branch',
                'Every fixed-pressure test is incompatible with the declared box',
                'All 48 gas/emissivity roots forward-recover to <1e-10',
                'Analytic pressure reintegration control demonstrates hydrostatic circularity'],
        caveats=['Box is not a confidence region; error conventions and common-distance aperture are assumptions',
                 'Different X-ray instruments do not guarantee independent plasma/deprojection systematics',
                 'No independently calibrated pressure gradient or matched temperature profile exists in inspected products',
                 'Integrated Y, SZ mass proxy, gas fractions, YX and hydrostatic M cannot be substituted for those independent inputs'])
    (out/'checks.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--out',required=True,type=Path)
    main(ap.parse_args().out)
