"""Independent finite inspection and angular-kernel audit; no full dwarf solve."""
import argparse
import csv
import importlib.util
import json
import math
from pathlib import Path
import sys
sys.dont_write_bytecode=True
import numpy as np
from scipy.integrate import quad

ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/'rebuild_2026_10_22/KT36_action_response_search/dwarfs'


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,type=Path);args=ap.parse_args()
    d=json.loads((BASE/'run_001/results.json').read_text())
    old=json.loads((ROOT/'rebuild_2026_10_22/KT15_filtered_phantom_dsph/kt15.json').read_text())
    original=[]
    with (ROOT/'real_research/data/dsph/mcconnachie2012_dsph.csv').open() as f:
        for x in csv.DictReader(f):
            if not x['e_sigma*'] or float(x['VMag'])>-8 or x['Name'].startswith(('M32','NGC','Sagittarius')):continue
            original.append(dict(name=x['Name'],sub=x['SubG'],D=float(x['D']),L=10**(-.4*(float(x['VMag'])-4.83)),a=float(x['R2'])/1000,obs=float(x['sigma*']),err=float(x['e_sigma*']),MHI=1e6*float(x['M.HI']) if x['M.HI'] else 0.))
    assert original==d['sample'] and len(original)==24
    assert [x['name'] for x in original]==[x['name'] for x in old['A0|alt|isolated']['rows']]
    assert d['upsilon_grid']==np.linspace(1,3,41).tolist()
    counts={};n_grade=0
    for n,feet in d['cases'].items():
        counts[n]={}
        for foot,rows in feet.items():
            assert [r['name'] for r in rows]==[r['name'] for r in original]
            rr={}
            for form,key,flag in [('reciprocal','sigma','passed'),('plain','plain_sigma','plain_passed'),('newton','newton_sigma','newton_passed')]:
                grid=continuous=0
                for sample,row in zip(original,rows):
                    assert sample['name']==row['name']
                    vals=np.array(row[key]);lo=sample['obs']-2*sample['err'];hi=sample['obs']+2*sample['err']
                    assert len(vals)==41 and np.all(np.diff(vals)>0)
                    test=bool(np.any((vals>=lo)&(vals<=hi)))
                    assert test==row[flag]
                    grid+=test;continuous+=bool(vals[-1]>=lo and vals[0]<=hi);n_grade+=41
                rr[form]=dict(grid_pass=grid,continuous_endpoint_pass=continuous)
                assert grid==continuous
            counts[n][foot]=rr
    assert n_grade==11808
    focus={}
    for sample in original:
        name=sample['name']
        if name not in ('Sculptor','Fornax','Leo I'):continue
        focus[name]={}
        for foot in ('canonical','alt'):
            candidates=[next(x for x in d['cases'][n][foot] if x['name']==name) for n in ('1000','2000')]
            entry=d['selected_checks'][name]['footings'][foot]
            candidates += [entry['expanded_domain'],*entry['mixture'].values()]
            max_sigma=max(r['sigma_U3'] for r in candidates)
            max_tail=max(r['outer_virial_sigma_squared_tail_upper'][-1] for r in candidates)
            low=sample['obs']-2*sample['err']
            focus[name][foot]=dict(max_U3_over_saved_checks=max_sigma,observed_two_sigma_lower=low,
                deficit=low-max_sigma,measurement_tail_only_adjusted_max=math.sqrt(max_sigma**2+max_tail))
            assert max_sigma<low and math.sqrt(max_sigma**2+max_tail)<low
    # Independent angular integral of the original normalized 3D Gaussian.
    spec=importlib.util.spec_from_file_location('isolated_audited',BASE/'isolated.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    tests=[]
    for r,s,ell in [(.01,.02,3.),(.3,.8,3.),(3.,3.,3.),(5.,8.,3.),(12.,10.,3.),(.1,1.,1.),(.099,1.,1.),(.101,1.,1.)]:
        pref=2*math.pi*s*s/(2*math.pi*ell*ell)**1.5
        exact0=quad(lambda mu:pref*math.exp(-(r*r+s*s-2*r*s*mu)/(2*ell*ell)),-1,1,epsabs=1e-14,epsrel=1e-12)[0]
        exact1=quad(lambda mu:pref*mu*math.exp(-(r*r+s*s-2*r*s*mu)/(2*ell*ell)),-1,1,epsabs=1e-14,epsrel=1e-12)[0]
        k0,k1=m.kernels(np.array([r]),np.array([s]),ell)
        errors=[abs(k0[0,0]/exact0-1),abs(k1[0,0]/exact1-1)]
        assert max(errors)<1e-9
        tests.append(dict(r=r,s=s,ell=ell,relative_errors=errors))
    result=dict(outcome='finite records and angular kernels independently checked; not a full solver replay',
        sample_matches_original=True,grade_values_checked=n_grade,counts=counts,focus=focus,
        angular_kernel_checks=tests,max_angular_kernel_relative_error=max(max(x['relative_errors']) for x in tests),
        non_claims=['No primary satellite EFE grade','No certified total numerical error','Continuous-Upsilon endpoint grading uses separately proved monotonicity and numerical endpoint predictions'])
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
