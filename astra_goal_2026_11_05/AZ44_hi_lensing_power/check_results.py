#!/usr/bin/env python3
"""Audit convergence, independent rerun, and the unsuccessful frozen control."""
import hashlib,json,math
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
checks=[]
def check(name,passed,value=None):checks.append(dict(name=name,passed=bool(passed),value=value))
def compare(a,b,path=''):
    if isinstance(a,dict):
        return a.keys()==b.keys() and all(compare(a[k],b[k],path+'/'+k) for k in a)
    if isinstance(a,list):return len(a)==len(b) and all(compare(x,y,path) for x,y in zip(a,b))
    if isinstance(a,float):return math.isclose(a,b,rel_tol=1e-10,abs_tol=0.)
    return a==b
base=HERE/'main';coarse=base/'chunk20000';fine=base/'chunk10000';repeat=HERE/'repeat/chunk20000'
p=read(coarse/'prepared.json');q=read(fine/'prepared.json')
check('preparation_chunk_pair',compare(p,q))
with np.load(coarse/'prepare_checkpoint.npz',allow_pickle=False) as a,np.load(fine/'prepare_checkpoint.npz',allow_pickle=False) as b:
    for key in ['pix','usable','bgs']:check(key+'_pixels_exact',np.array_equal(a[key],b[key]))
check('same_size_preparation_bytes', (coarse/'prepared.json').read_bytes()==(repeat/'prepared.json').read_bytes())
for mode in ['main','mutate']:
    a=read(coarse/mode/'forecast.json');b=read(fine/mode/'forecast.json')
    check(mode+'_scientific_chunk_pair',compare(a['scientific'],b['scientific']))
    for foot in ['canonical','alt']:
        x=a['scientific']['results'][foot]['Fisher_upper'];y=b['scientific']['results'][foot]['Fisher_upper']
        check(mode+'_'+foot+'_Fisher_relative',abs(x-y)/abs(x)<=1e-10,abs(x-y)/abs(x))
check('same_size_forecast_bytes',(coarse/'main/forecast.json').read_bytes()==(repeat/'main/forecast.json').read_bytes())
main=read(coarse/'main/forecast.json')['scientific'];mut=read(coarse/'mutate/forecast.json')['scientific']
check('mutation_rejects_original_count',not next(c['passed'] for c in mut['checks'] if c['name']=='original_count_preserved'))
drop=1-mut['lenses']/main['lenses']
# Keep this separately: a failed expected outcome is not a passing control.
frozen_control=dict(name='rotation_count_drop_over_50_percent',passed=drop>.5,value=drop)
out=dict(label='NO VERDICT on a fully validated FN4e stage0; conditional STOP: NOT ENOUGH POWER on both footings',
         checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),
         frozen_control=frozen_control,provisional_area_check=p['checks'][1],
         shape_noise_model='Constant variance; conditional point-source Fisher bound, not measured shear SNR',
         caveat='amplitude_SNR_upper in forecast.json is a deep-MOND amplitude proxy; not an upper bound on total Newtonian-plus-modified stack SNR',
         hashes={str(f.relative_to(HERE)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [coarse/'prepared.json',fine/'prepared.json',coarse/'main/forecast.json',fine/'main/forecast.json',coarse/'mutate/forecast.json',fine/'mutate/forecast.json',repeat/'prepared.json',repeat/'main/forecast.json']},
         scope='kappa = 1/2 FITTED; not theory closed')
(HERE/'result_checks.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
raise SystemExit(int(not all(c['passed'] for c in checks) or not frozen_control['passed']))
