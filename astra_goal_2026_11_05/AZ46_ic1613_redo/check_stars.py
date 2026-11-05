#!/usr/bin/env python3
"""Row-size convergence and original photometry recovery, no new physical gate."""
import hashlib,json,math,resource,time
from pathlib import Path
import stars as S
import io_beam as B
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1];DATA=ROOT.parent/'_external_data/fn4a_ic1613_2026_11'
start=time.time();checks=[];profiles={}
def check(n,ok,value=None):checks.append(dict(name=n,passed=bool(ok),value=value))
for label,ring in [('original',13.2),('natural',13.19112),('robust',7.69068)]:
    a=S.profile(DATA/'ic1613v.fits',ring,32);b=S.profile(DATA/'ic1613v.fits',ring,64)
    check(label+'_row_chunks_byte_identical',json.dumps(a,sort_keys=True)==json.dumps(b,sort_keys=True))
    profiles[label]=a
old=json.loads((ROOT/'finish_2026_11_04/FN4_galaxy_rows_data/FN4a_ic1613_cube_model/fn4a_s0.json').read_text())['stars']
for k in ['background','profile_cut_arcsec','half_light_arcsec']:
    value=profiles['original'][k];check('original_'+k,math.isclose(value,old[k],rel_tol=1e-10,abs_tol=1e-10),dict(new=value,old=old[k]))
try:S.profile(DATA/'ic1613v.fits',13.2,32,lambda:True);interrupted=False
except S.YieldRequested:interrupted=True
check('cooperative_stop_observed',interrupted)
obj=dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),profiles=profiles,
         source_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),Path(S.__file__),Path(B.__file__),HERE/'FROZEN_CRITERIA.md',DATA/'ic1613v.fits']},
         scope='Preparation checks only; no cube fit, no calibrated stellar mass claim; kappa=1/2 FITTED; not theory closed')
B.atomic(HERE/'stars_checks.json',obj);B.atomic(HERE/'stars_runtime.json',dict(seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
print(json.dumps(dict(passed=obj['passed'],total=obj['total'],profiles={k:{x:v[x] for x in ['background','half_light_arcsec','profile_cut_arcsec']} for k,v in profiles.items()}),indent=2))
raise SystemExit(int(not all(c['passed'] for c in checks)))
