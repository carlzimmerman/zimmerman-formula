"""Raw catalogue operator and adversarial positivity construction; no theory verdict."""
import copy
import json
import math
import re
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
DATA = ROOT / 'sol61_push/cluster_projection_2026_10_11/sources/tablea1.dat'


def parse(text):
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        ident = line[:6].strip()
        m = re.fullmatch(r'([KN]\d+)([a-z]?)\.(\d+)', ident)
        if m is None:
            raise ValueError('Malformed image identifier: ' + ident)
        rows.append(dict(id=ident, feature=ident.rsplit('.', 1)[0], galaxy=m[1],
                         ra=float(line[7:17]), dec=float(line[18:28]),
                         zsys=float(line[64:70]) if line[64:70].strip() else None,
                         quality=line[71:72]))
    return rows


def validate(rows):
    if len(rows) != 199 or len({r['id'] for r in rows}) != 199:
        raise ValueError('Catalogue count or duplicate identifier')
    counts = {k: sum(r['quality'] == k for r in rows) for k in ('G', 'S', 'B')}
    if counts != dict(G=135, S=21, B=43):
        raise ValueError('Quality classes/counts')
    for r in rows:
        if not (math.isfinite(r['ra']) and math.isfinite(r['dec']) and
                0 <= r['ra'] < 360 and -90 < r['dec'] < 90):
            raise ValueError('Invalid sky coordinates')
    gold = [r for r in rows if r['quality'] == 'G']
    if len({r['feature'] for r in gold}) != 49 or len({r['galaxy'] for r in gold}) != 27:
        raise ValueError('Feature/galaxy counts')
    for r in gold:
        if r['zsys'] is None or not math.isfinite(r['zsys']) or r['zsys'] <= .296:
            raise ValueError('Gold redshift missing/invalid')
    for key in ('feature', 'galaxy'):
        for group in {r[key] for r in gold}:
            rr = [r for r in gold if r[key] == group]
            if len(rr) < 2 or len({r['zsys'] for r in rr}) != 1:
                raise ValueError('Source grouping/redshift inconsistency')
    return gold


def tangent(rows):
    ra, dec = np.deg2rad(np.array([[r['ra'], r['dec']] for r in rows])).T
    a0, d0 = ra.mean(), dec.mean()
    da = ra-a0
    den = np.sin(d0)*np.sin(dec)+np.cos(d0)*np.cos(dec)*np.cos(da)
    x = np.cos(dec)*np.sin(da)/den
    y = (np.cos(d0)*np.sin(dec)-np.sin(d0)*np.cos(dec)*np.cos(da))/den
    rho = np.hypot(x, y)
    c = np.arctan(rho)
    invdec = np.arcsin(np.cos(c)*np.sin(d0)+np.divide(y*np.sin(c)*np.cos(d0), rho,
                          out=np.zeros_like(rho), where=rho > 0))
    invra = a0 + np.arctan2(x*np.sin(c), rho*np.cos(d0)*np.cos(c)-y*np.sin(d0)*np.sin(c))
    err = np.rad2deg(np.max(np.abs(np.array([invra-ra, invdec-dec]))))
    return np.column_stack((x, y))*206264.80624709636, np.rad2deg([a0, d0]), err


def helmert(n):
    h = np.zeros((n-1, n))
    for k in range(1, n):
        h[k-1, :k] = 1/math.sqrt(k*(k+1))
        h[k-1, k] = -k/math.sqrt(k*(k+1))
    return h


def lens_matrix(points, masses_at):
    delta = points[:, None, :] - masses_at[None, :, :]
    rr = np.sum(delta**2, axis=2)
    if np.any(rr == 0):
        raise ValueError('Singular collocation')
    return (delta/rr[:, :, None]).transpose(0, 2, 1).reshape(2*len(points), -1)


def clump_fit(points, targets, epsilon, B):
    n = len(points)
    axes = np.array([[1., 0], [-1., 0], [0, 1.], [0, -1.]])
    centres = (points[:, None, :] - epsilon*axes).reshape(-1, 2)
    K = lens_matrix(points, centres)
    L = np.zeros((4*n, 2*n))
    for i in range(n):
        L[4*i, 2*i] = L[4*i+2, 2*i+1] = epsilon/2
        L[4*i+1, 2*i] = L[4*i+3, 2*i+1] = -epsilon/2
    baseline = np.full(4*n, epsilon*B/2)
    A = K @ L
    v = np.linalg.solve(A, targets.reshape(-1)-K@baseline)
    weights = baseline+L@v
    residual = (K@weights).reshape(n, 2)-targets
    return dict(epsilon=epsilon, total_mass=float(weights.sum()),
                analytic_total_mass=2*n*epsilon*B, min_mass=float(weights.min()),
                max_relative_residual=float(np.max(np.abs(residual))/max(1, np.max(np.abs(targets)))),
                condition_number=float(np.linalg.cond(A)),
                cross_talk_norm_inf=float(np.linalg.norm(A-np.eye(2*n), ord=np.inf)))


def main():
    checks = []
    def ck(name, ok, value=None):
        checks.append(dict(name=name, passed=bool(ok), value=value))
    rows = parse(DATA.read_text())
    gold = validate(rows)
    from source_audit import audit
    audit_result = audit()
    ck('HTML_CDS_all_classes', audit_result['same_all_rows'])
    ck('published_catalogue_structure', len(gold) == 135)
    for mutation in ('duplicate', 'redshift', 'missing_z', 'quality'):
        rr = copy.deepcopy(rows)
        if mutation == 'duplicate': rr[1]['id'] = rr[0]['id']
        elif mutation == 'redshift': rr[0]['zsys'] += .1
        elif mutation == 'missing_z': rr[0]['zsys'] = None
        else: rr[0]['quality'] = 'X'
        try:
            validate(rr)
            caught = False
        except ValueError:
            caught = True
        ck('MUTATE_parser_'+mutation, caught)
    xy, centre, inverse_error = tangent(gold)
    ck('sky_roundtrip', inverse_error < 1e-8, inverse_error)
    features = sorted({r['feature'] for r in gold})
    H = np.zeros((len(gold)-len(features), len(gold)))
    target = np.empty_like(xy)
    feature_records = []
    offset = 0
    for feature in features:
        ids = [i for i, r in enumerate(gold) if r['feature'] == feature]
        h = helmert(len(ids))
        H[np.ix_(range(offset, offset+len(ids)-1), ids)] = h
        offset += len(ids)-1
        target[ids] = xy[ids]-xy[ids].mean(axis=0)
        ck('Helmert_'+feature, np.max(np.abs(h@h.T-np.eye(len(ids)-1))) < 1e-10 and
           np.max(np.abs(h@np.ones(len(ids)))) < 1e-10)
        feature_records.append(dict(feature=feature, galaxy=gold[ids[0]]['galaxy'],
                                    zsys=gold[ids[0]]['zsys'], image_indices=ids))
    ck('contrast_dimension', 2*offset == 172, 2*offset)
    ck('contrast_equals_demeaning', np.max(np.abs(H.T@H@xy-target)) < 1e-10)
    # Exact point lens: theta-beta-w*m/theta=0 on x axis.
    beta, w, m = .3, .7, 1.2
    xx = np.array([(beta+math.sqrt(beta*beta+4*w*m))/2,
                   (beta-math.sqrt(beta*beta+4*w*m))/2])
    inferred = xx-w*m/xx
    ck('point_lens', np.max(np.abs(inferred-beta)) < 1e-10)
    ck('MUTATE_wrong_sign', np.ptp(xx+w*m/xx) > 1)
    ck('MUTATE_wrong_efficiency', np.ptp(xx-.5*w*m/xx) > .1)
    lam = .65
    sheet_a = lam*m/xx+(1-lam)*xx/w
    ck('single_source_mass_sheet', np.max(np.abs(xx-w*sheet_a-lam*beta)) < 1e-10)
    p = np.array([.7, 1.3]); step = 1e-6
    analytic = np.eye(2)/(p@p)-2*np.outer(p, p)/(p@p)**2
    def f(q): return q/(q@q)
    numerical = np.column_stack([(f(p+step*e)-f(p-step*e))/(2*step) for e in np.eye(2)])
    ck('point_lens_Jacobian', np.max(np.abs(numerical-analytic)) < 1e-6)
    ck('Jacobian_symmetry', np.max(np.abs(numerical-numerical.T)) < 1e-6)
    # Two features of one galaxy need distinct source positions.
    true_sources = np.array([[.2, .1], [.2, .1], [-.2, .3], [-.2, .3]])
    ck('MUTATE_merge_features', np.linalg.norm(helmert(4)@true_sources) > .1 and
       np.linalg.norm(helmert(2)@true_sources[:2]) < 1e-10)
    separations = np.linalg.norm(xy[:, None, :]-xy[None, :, :], axis=2)
    np.fill_diagonal(separations, np.inf)
    sep = float(separations.min())
    ck('distinct_positions', sep > 0, sep)
    scaled, desired = xy/sep, target/sep
    B = float(2*np.max(np.abs(desired))+1)
    cells = []
    for eps in (1e-3, 1e-4, 1e-5, 1e-6):
        cell = clump_fit(scaled, desired, eps, B)
        cells.append(cell)
        ck('positive_fit_'+str(eps), cell['min_mass'] > 0 and cell['max_relative_residual'] <= 1e-6,
           cell['max_relative_residual'])
        ck('mass_identity_'+str(eps), math.isclose(cell['total_mass'], cell['analytic_total_mass'], rel_tol=1e-12))
    result = dict(status='operator_audit_not_theory_verdict', checks=checks,
                  passed=sum(c['passed'] for c in checks), total=len(checks),
                  tangent_origin_degrees=centre.tolist(), minimum_separation_arcsec=sep,
                  gold_rows=gold, features=feature_records, clump_cells=cells,
                  units='Fit positions in minimum-separation units; lensing coefficient=1; masses not astrophysical',
                  fixed_B=B)
    out = HERE/'run_v2'
    (out/'results.json').write_text(json.dumps(result, indent=2)+'\n')
    np.savez_compressed(out/'operator.npz', theta_arcsec=xy, helmert=H,
                        contrast_arcsec=H@xy, target_demo_arcsec=target)
    print('%d/%d checks; %d images, %d features, %d galaxies, %d scalar contrasts' %
          (result['passed'], len(checks), len(gold), len(features), len({r['galaxy'] for r in gold}), 2*offset))
    print('minimum separation arcsec', sep)
    for cell in cells: print(json.dumps(cell))
    assert all(c['passed'] for c in checks)

if __name__ == '__main__': main()
