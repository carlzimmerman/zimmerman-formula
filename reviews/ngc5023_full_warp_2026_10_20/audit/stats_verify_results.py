#!/usr/bin/env python3
"""Independent saved-array algebra check; no production imports or cube render."""
import argparse
import json
from pathlib import Path
import numpy as np
from scipy.optimize import lsq_linear

HERE = Path(__file__).resolve().parents[1]


def direct_boxes(a, ku):
    """Sum with explicit offsets, accumulating in float64."""
    a = np.asarray(a, dtype=float)
    nv, nz, nx = a.shape[-3:]
    out = np.zeros(a.shape[:-3] + (nv-ku+1, nz-1, nx-1), dtype=float)
    for du in range(ku):
        for dz in range(2):
            for dx in range(2):
                out += a[..., du:du+nv-ku+1, dz:dz+nz-1, dx:dx+nx-1]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run', required=True)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    run = HERE / args.run
    report = json.loads((run/'results.json').read_text())
    z = np.load(run/'arrays.npz')
    data, blanks, predictions, components = [z[k] for k in ['data', 'blanks', 'predictions', 'components']]
    dco = z['amplitude_blank_deltas']
    masks = {'validation':z['validation_mask'], 'guarded':z['guarded_mask']}
    train = z['training_mask']
    records = []
    for name in ['family_run001', 'trace_run001']:
        records += json.loads((HERE/name/'results.json').read_text())['cases']
    # Reproduce the specified fixed weights; accumulation below is independent.
    sd0 = blanks.std(0, ddof=1)
    floor = np.median(sd0[train])*.5
    sd = np.maximum(sd0, floor)
    rms = np.sqrt(np.mean(((data[None,...]-predictions)[...,train]/sd[train])**2, axis=1))
    ratios = rms/rms[0]
    checks = []
    checks.append({'name':'case/blank counts and finite values',
                   'passed':bool(len(records)==len(predictions)==118 and len(blanks)==20
                            and np.isfinite(dco).all() and np.isfinite(predictions).all())})
    ratio_diff = float(np.max(abs(ratios-z['training_ratio'])))
    checks.append({'name':'training gate ratios', 'max_abs_difference':ratio_diff,
                   'passed':ratio_diff<1e-6})
    # Test gate decisions themselves, not only numerical proximity of ratios.
    for gate in [1.1,1.25,1.5]:
        keep = ratios<=gate
        checks.append({'name':'retained membership '+str(gate),
                       'passed':[r['id'] for r,k in zip(records,keep) if k]
                                == report['finite_family'][str(gate)]['ids']})
    controls = np.load(HERE/'controls_run001/arrays.npz')['predictions']
    numerical = np.max(abs(controls-controls[0]),axis=0)
    checks.append({'name':'finite numerical per-bin discrepancy',
                   'passed':bool(np.array_equal(numerical,z['numerical_discrepancy']))})
    scans = []
    for ku in [2,3]:
        db, pb, bb, nb = [direct_boxes(a,ku) for a in [data,predictions,blanks,numerical]]
        bsd = bb.std(0,ddof=1)
        bsd = np.maximum(bsd,np.median(bsd)*.5)
        local = [r for r in report['search'] if r['velocity_bins']==ku]
        nullmax = {(r['region'],r['training_ratio_gate']):np.full(len(blanks),-np.inf) for r in local}
        safe = {region:direct_boxes(mask,ku)==ku*4 for region,mask in masks.items()}
        for i,m in enumerate(components):
            response = (dco[i]@m.astype(float).reshape(3,-1)).reshape((len(blanks),)+data.shape)
            nr = (bb-direct_boxes(response,ku))/bsd
            for r in local:
                key = r['region'],r['training_ratio_gate']
                if ratios[i]<=r['training_ratio_gate']:
                    nullmax[key] = np.maximum(nullmax[key],abs(nr[:,safe[r['region']]]).max(axis=1))
        for r in local:
            region,gate = r['region'],r['training_ratio_gate']
            keep = ratios<=gate
            lo = pb[keep].min(0)-nb
            hi = pb[keep].max(0)+nb
            dist = np.where(db>hi,db-hi,np.where(db<lo,db-lo,0))
            stat = dist/bsd
            m = safe[region]
            saved = z['distance_ku%d_%s_g%s'%(ku,region,gate)]
            delta = float(np.max(abs(stat[m]-saved[m])))
            peak = float(abs(stat[m]).max())
            null_delta = float(np.max(abs(nullmax[(region,gate)]-
                np.asarray(r['blank_search_maxima_after_training_refit_worst_retained_case']))))
            # Float32 saved cubes and production float32 sums differ slightly
            # from the separate float64 offset accumulation used here.
            ok = (delta<1e-4 and null_delta<1e-4
                  and abs(peak-r['max_abs_persistent_distance_blank_scatter'])<1e-4
                  and int(m.sum())==r['number_correlated_box_positions'])
            scans.append({'velocity_bins':ku,'region':region,'gate':gate,
                          'boxes':int(m.sum()),'max_saved_stat_difference':delta,
                          'max_null_stat_difference':null_delta,
                          'independent_peak':peak,
                          'independent_blank_max_range':[float(nullmax[(region,gate)].min()),
                                                         float(nullmax[(region,gate)].max())],
                          'passed':bool(ok)})
    checks.append({'name':'all 12 full-box scans and worst-retained-case blank maxima',
                   'passed':len(scans)==12 and all(s['passed'] for s in scans)})
    sampled = []
    scale = sd[train]
    for i,j in [(0,0),(len(records)//2,7),(len(records)-1,19)]:
        rec = records[i]['bounded_fit']
        lo,hi = np.array(rec['coefficient_bounds'])
        A = components[i][:,train].T.astype(float)/scale[:,None]
        yy = (data[train]+blanks[j,train]).astype(float)/scale
        fit = lsq_linear(A,yy,bounds=(lo,hi),tol=1e-10)
        delta = float(np.max(abs(fit.x-np.asarray(rec['coefficients'])-dco[i,j])))
        sampled.append({'case':records[i]['id'],'blank':j,'maximum_coefficient_difference':delta,
                        'passed':bool(fit.success and delta<1e-7)})
    checks.append({'name':'three independently repeated saved bounded amplitude perturbation fits',
                   'passed':all(s['passed'] for s in sampled)})
    result = {'scope':'Saved binned arrays and finite scan algebra only; not cube/render/model validation or probability calibration.',
              'tested_run':args.run,'all_checks_passed':all(c['passed'] for c in checks),
              'checks':checks,'scans':scans,'sampled_refits':sampled,
              'tolerance_note':'Direct offset sums accumulate saved float32 values in float64; 1e-4 empirical-scatter-unit agreement is required. This is a finite implementation check, not a rigorous numerical error bound.'}
    Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'all_checks_passed':result['all_checks_passed'],
                      'checks':checks,'scan_count':len(scans),'sampled_refits':sampled},indent=2))
    return 0 if result['all_checks_passed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
