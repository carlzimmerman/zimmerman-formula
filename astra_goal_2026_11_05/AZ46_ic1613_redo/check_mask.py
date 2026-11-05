#!/usr/bin/env python3
"""Independent mask building-block fixtures; no real-cube acceptance."""
import hashlib,json
from pathlib import Path
import numpy as np
import masking as M
import io_beam as B
checks=[]
def check(n,ok,v=None):checks.append(dict(name=n,passed=bool(ok),value=v))
a=np.zeros((8,30,30),bool);a[1,1:11,1:21]=True;a[4,20,20]=True;a[6,20,20:22]=True
kept,report=M.retain_components(a)
check('one_percent_component_cut',kept.sum()==202 and not kept[4,20,20] and kept[6,20,20],report)
try:M.retain_components(np.zeros((3,3,3),bool));rejected=False
except ValueError:rejected=True
check('empty_emission_rejected',rejected)
for pix in [3.,6.,12.]:
 k=M.dilation_kernel([pix,pix]);cy,cx=(np.array(k.shape[1:])-1)//2
 expected=np.array([[[((x-cx)*pix)**2+((y-cy)*pix)**2<=144 for x in range(k.shape[2])] for y in range(k.shape[1])] for z in range(5)])
 check('physical_dilation_'+str(pix),np.array_equal(k,expected))
rng=np.random.default_rng(46);cube=rng.normal(0,.002,(60,64,64)).astype('f4')
cube[25:35,25:39,25:39]+=.1
arrays,science=M.make_mask(cube,[3.,3.],[13.19112,10.98504,-4.95])
check('noise_recovers_planted_rms',abs(science['noise_Jy_per_beam']/.002-1)<.02,science['noise_Jy_per_beam'])
check('emission_retained',bool(arrays['mask'][30,32,32]))
check('native_lattice_origin',bool(arrays['lattice'][0,0,0]) and not arrays['lattice'][1].any())
check('intensity_independent_sum',np.array_equal(arrays['intensity'],np.maximum((cube*arrays['mask']).sum(0),0)))
# Swapping the positive source to negative must remove its mask centre.
mut=cube.copy();mut[25:35,25:39,25:39]-=.2
ma,ms=M.make_mask(mut,[3.,3.],[13.19112,10.98504,-4.95])
check('negative_source_mutation_bites',not bool(ma['mask'][30,32,32]))
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(M.__file__)]},scope='Synthetic mask controls; physical channel-shuffle mutation and cube fits remain pending; kappa=1/2 FITTED; not theory closed')
B.atomic(Path(__file__).with_name('mask_checks.json'),obj);print(json.dumps(obj,indent=2));raise SystemExit(int(not all(c['passed'] for c in checks)))
