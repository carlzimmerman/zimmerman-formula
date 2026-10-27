#!/usr/bin/env python3
"""Independent fixed-box sums and empirical blank checks on saved arrays."""
import argparse
import json
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parents[1]


def direct_sum(a, c):
    x,z,u = c['center_major_minor_u']
    ku = c['velocity_bins']
    positions = [(x+280)/20, (z+100)/20, u/12.36+9.5-(ku-1)/2]
    ii,jj,kk = [int(round(t)) for t in positions]
    assert max(abs(t-round(t)) for t in positions)<1e-10
    out = np.zeros(a.shape[:-3],dtype=float)
    for du in range(ku):
        for dz in range(2):
            for dx in range(2):
                out += a[...,kk+du,jj+dz,ii+dx].astype(float)
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    cases = json.loads((HERE/'followup_candidates.json').read_text())['cases']
    report = json.loads((HERE/'followup_run001/results.json').read_text())
    ar = np.load(HERE/'followup_run001/arrays.npz')
    ratios = np.load(HERE/'analysis_run002/arrays.npz')['training_ratio']
    checks,summary = [],{}
    for which in ['HR','LR','WHISP']:
        summary[which] = {}
        for beam in ['native','40arcsec']:
            data = ar[which+'_'+beam+'_data']
            blank = ar[which+'_'+beam+'_blanks']
            records = report['datasets'][which]['data'][beam]['boxes']
            values = []
            for c,rec in zip(cases,records):
                assert c['id']==rec['id']
                flux = float(direct_sum(data,c))
                b = direct_sum(blank,c)
                mean,sd = float(b.mean()),float(b.std(ddof=1))
                signal = flux-mean
                discrepancies = [abs(flux-rec['flux_Jy_km_s']),
                    abs(mean-rec['blank_mean_Jy_km_s']),
                    abs(sd-rec['blank_scatter_Jy_km_s'])]
                ratio_error = abs(signal/sd-rec['flux_minus_blank_mean_scatter_units'])
                passed = max(discrepancies)<1e-7 and ratio_error<1e-4
                checks.append({'dataset':which,'beam':beam,'id':c['id'],
                    'max_flux_mean_scatter_discrepancy':max(discrepancies),
                    'scatter_ratio_discrepancy':ratio_error,'passed':bool(passed)})
                values.append({'id':c['id'],'raw_flux':flux,'blank_mean':mean,
                    'signal_minus_blank_mean':signal,'empirical_scatter':sd,
                    'descriptive_scatter_ratio':signal/sd})
            summary[which][beam] = values
        mf = ar[which+'_40arcsec_model_box_fluxes']
        for gate in [1.1,1.25,1.5]:
            keep = ratios<=gate
            expected = report['datasets'][which]['native_operator_model_checks'][str(gate)]
            delta = max(float(np.max(abs(mf[keep].min(0)-expected['box_prediction_min']))),
                        float(np.max(abs(mf[keep].max(0)-expected['box_prediction_max']))))
            checks.append({'dataset':which,'gate':gate,'name':'all 7 finite model ranges',
                           'max_discrepancy':delta,'passed':bool(delta<1e-12 and keep.sum()==expected['retained'])})
        nominal = ar[which+'_40arcsec_nominal_model']
        error = max(abs(float(direct_sum(nominal,c))-mf[0,j]) for j,c in enumerate(cases))
        checks.append({'dataset':which,'name':'7 nominal full-model aperture sums',
                       'max_discrepancy':error,'passed':bool(error<1e-12)})
    sensitivity = {}
    for cid in ['followup_03','guarded_broad_positive']:
        lookup = {which:{v['id']:v for v in summary[which]['40arcsec']} for which in summary}
        old_sd = lookup['WHISP'][cid]['empirical_scatter']
        sensitivity[cid] = {'expected_older_scatter_units_from_HR_amplitude':lookup['HR'][cid]['signal_minus_blank_mean']/old_sd,
                           'expected_older_scatter_units_from_LR_amplitude':lookup['LR'][cid]['signal_minus_blank_mean']/old_sd}
    result = {'scope':'Saved binned followup arrays:42 independent box/blank checks,9 family-range aggregations and21 nominal aperture sums. No raw-data rerender, significance or physical signal classification.',
              'all_checks_passed':all(c['passed'] for c in checks), 'checks':checks,
              'independent_values':summary,'older_amplitude_to_empirical_scatter':sensitivity,
              'warning':'Ratios are descriptive empirical-scatter units. HR/LR share observations, oldercube already unblinded, blanks overlap; none is a Gaussian significance or upper-limit construction.'}
    Path(args.output).write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'all_checks_passed':result['all_checks_passed'],
                      'checks':len(checks),'max_flux_mean_scatter_discrepancy':max(c.get('max_flux_mean_scatter_discrepancy',0) for c in checks),
                      'older_amplitude_to_empirical_scatter':sensitivity},indent=2))
    return 0 if result['all_checks_passed'] else 1


if __name__=='__main__':
    raise SystemExit(main())
