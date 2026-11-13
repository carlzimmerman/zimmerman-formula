#!/usr/bin/env python3
"""Assemble numerical comparisons without modifying the original run evidence."""
import hashlib,json,math,sys
from pathlib import Path
sys.dont_write_bytecode=True
import numpy as np
from scipy.interpolate import PchipInterpolator

lane=Path(__file__).resolve().parent
def read(name): return json.loads((lane/name/'results.json').read_text())
def profile(name):
    z=np.load(lane/name/'profiles.npz')
    return PchipInterpolator(np.log(z['r']),z['mratio'])

coarse,fine=read('aqual_320_96'),read('aqual_512_128')
comparisons={}
for f in fine['physical']:
    a=np.array(coarse['physical'][f]['aqual_effective_mass_msun'])
    b=np.array(fine['physical'][f]['aqual_effective_mass_msun'])
    q=np.array(fine['physical'][f]['qumond_effective_mass_msun'])
    comparisons[f]=dict(radii_kpc=fine['physical'][f]['radii_kpc'],
        aqual_mass_msun=b.tolist(),qumond_mass_msun=q.tolist(),
        aqual_over_qumond=(b/q).tolist(),fine_over_coarse_minus_one=(b/a-1).tolist(),
        max_grid_relative_difference=float(np.max(abs(b/a-1))))

cap=read('capacity_512_128'); xe=cap['x_external_physical']; re=1/xe
apertures=np.array([.5,1.,2.,3.,5.,10.,20.,30.])
capacity={}
for name in ['capacity_320_96','capacity_512_128','boundary_1e4','boundary_1e5_verified']:
    p=profile(name); v=p(np.log(apertures*re)); dm=p.derivative()(np.log(apertures*re))
    grid=np.geomspace(1.,1000.,3000)
    vv=p(np.log(grid)); dd=p.derivative()(np.log(grid))
    capacity[name]=dict(r_over_RE=apertures.tolist(),M_eff_over_Mb=v.tolist(),cold_excess_if_identified=(v-1).tolist(),
        fraction_of_asymptotic_cold_excess=((v-1)/59.5).tolist(),dM_dlogr=dm.tolist(),
        sampled_range_rM=[1.,1000.],max_M_in_sample=float(vv.max()),min_dM_dlogr_in_sample=float(dd.min()),
        negative_derivative_count_in_sample=int(np.sum(dd<0)))

density=read('density_excess_run')
claims=read('claims_run')
tests=[dict(name='matched_field_resolution_20_300kpc_below_0p2percent',passed=all(x['max_grid_relative_difference']<.002 for x in comparisons.values())),
       dict(name='matched_field_scaled_residual_below_1e_minus_8',passed=fine['nonlinear_residual_max_scaled_r1_100']<1e-8),
       dict(name='matched_field_gauss_flux_below_0p1percent',passed=fine['gauss_flux_max_rel_error_r1_100']<.001),
       dict(name='capacity_two_grids_monotonic_in_sample_1_1000rM',passed=all(capacity[n]['negative_derivative_count_in_sample']==0 for n in ['capacity_320_96','capacity_512_128'])),
       dict(name='capacity_at_RE_below_asymptotic_cold_excess',passed=capacity['capacity_512_128']['fraction_of_asymptotic_cold_excess'][1]<.90),
       dict(name='Green_boundary_derivatives_positive_through_30RE_on_both_boxes',passed=all(min(capacity[n]['dM_dlogr'])>0 for n in ['boundary_1e4','boundary_1e5_verified'])),
       dict(name='cosmic_cold_background_can_cover_equatorial_lobes_at_5RE',passed=all(r['uniform_cosmic_cold_offset_nonnegative'] for r in density['rows'] if r['r_over_RE']==5.))]
inputs=[]
for name in ['aqual_320_96','aqual_512_128','capacity_320_96','capacity_512_128','boundary_1e4','boundary_1e5_verified','density_excess_run','claims_run']:
    p=lane/name/'results.json'; inputs.append(dict(path=str(p.relative_to(lane)),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
result=dict(tests=tests,matched_fields=comparisons,capacity_apertures=capacity,density=density,
            g238=claims['g238'],inputs=inputs,non_claims=['Sampled monotonicity is not a global theorem','No hard retention boundary','Signed effective source need not equal cold rest density','No repaired forest/KiDS likelihood'])
(lane/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
for test in tests: print(('PASS' if test['passed'] else 'FAIL')+' '+test['name'])
if not all(t['passed'] for t in tests): raise SystemExit(1)
