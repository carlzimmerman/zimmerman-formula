#!/usr/bin/env python3
"""Per-source triangle Fisher bound, with independent RA-rotation output."""
import argparse,hashlib,json,math,os,resource,signal,time
from pathlib import Path
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[name]='1'
import numpy as np
from scipy.spatial import cKDTree
import catalogues as C
ap=argparse.ArgumentParser();ap.add_argument('--chunk',type=int,choices=[10000,20000],required=True)
ap.add_argument('--tag',default='main');ap.add_argument('--max-chunks',type=int,default=200)
ap.add_argument('--mutate',action='store_true');args=ap.parse_args()
HERE=Path(__file__).resolve().parent;BASE=HERE/args.tag/('chunk'+str(args.chunk))
prep_path=BASE/'prepared.json';prep=json.loads(prep_path.read_text())
mode='mutate' if args.mutate else 'main';OUT=BASE/mode;OUT.mkdir(parents=True,exist_ok=True)
start=time.time();stop=False
def stopping(sig,frame):
    global stop
    stop=True
signal.signal(signal.SIGTERM,stopping);signal.signal(signal.SIGINT,stopping)
info,dt=C.metadata(C.PATHS['shear'],['RAJ2000','DECJ2000','Z_B','e1','e2','weight'])
identity=dict(shear=info,prepared_sha256=hashlib.sha256(prep_path.read_bytes()).hexdigest(),
              scripts={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'catalogues.py',HERE/'FROZEN_CRITERIA.md']})
rows=[dict(r) for r in prep['lenses'] if r['rotated_in_footprint' if args.mutate else 'in_source_footprint']]
if args.mutate:
    for row in rows:row['ra']=(row['ra']+180)%360
def unit(ra,dec):
    rr=np.radians(ra);dd=np.radians(dec);cc=np.cos(dd)
    return np.column_stack((cc*np.cos(rr),cc*np.sin(rr),np.sin(dd)))
lv=unit([r['ra'] for r in rows],[r['dec'] for r in rows])
dist=np.array([r['distance_Mpc'] for r in rows]);zl=np.array([r['z'] for r in rows])
thlo=.03/dist;thhi=np.minimum(1./dist,math.pi)
radius=2*np.sin(thhi/2)
a0can=9.3603e-11
v2=np.sqrt(6.67430e-11*np.array([r['Mb'] for r in rows])*1.98847e30*a0can)
coeff=math.log(10)*math.pi*v2/(2*299792458.**2)
ck=OUT/'forecast_checkpoint.json'
state=dict(identity=identity,next_row=0,sum_squared='0',source_count=0,pair_count=0,contributing_sources=0,chunk_hashes=[])
if ck.exists():
    state=json.loads(ck.read_text())
    if state['identity']!=identity:raise RuntimeError('Forecast checkpoint inputs changed')
total=np.longdouble(state['sum_squared']);used=0
for lo,arr,digest in C.raw_chunks(C.PATHS['shear'],info,dt,args.chunk,state['next_row']):
    if stop or used>=args.max_chunks:break
    ra=arr['RAJ2000'].astype('f8');dec=arr['DECJ2000'].astype('f8');zs=arr['Z_B'].astype('f8')
    w=arr['weight'].astype('f8');e1=arr['e1'].astype('f8');e2=arr['e2'].astype('f8')
    good=np.isfinite(ra)&np.isfinite(dec)&(ra>=0)&(ra<360)&(abs(dec)<=90)&np.isfinite(zs)&np.isfinite(w)&(w>0)&np.isfinite(e1)&np.isfinite(e2)
    sv=unit(ra[good],dec[good]);zz=zs[good];bound=np.zeros(len(sv))
    if len(sv):
        tree=cKDTree(sv)
        near=tree.query_ball_point(lv,radius,workers=1)
        for i,indices in enumerate(near):
            if not indices:continue
            ix=np.array(indices,dtype=np.int64)
            # atan2 avoids loss of relative precision at tiny separations.
            vv=sv[ix];theta=np.arctan2(np.linalg.norm(np.cross(vv,lv[i]),axis=1),vv@lv[i])
            use=(theta>=thlo[i])&(theta<=thhi[i])&(zz[ix]>zl[i]+.2)
            idx=ix[use]
            if len(idx):bound[idx]+=coeff[i]/theta[use]
            state['pair_count']+=int(len(idx))
    total+=np.sum(bound.astype(np.longdouble)**2,dtype=np.longdouble)
    state['source_count']+=int(len(sv));state['contributing_sources']+=int(np.count_nonzero(bound))
    state['next_row']=lo+len(arr);state['chunk_hashes'].append(digest);state['sum_squared']=str(total)
    used+=1
    if used%20==0:C.atomic_json(ck,state)
C.atomic_json(ck,state)
if state['next_row']<info['rows']:
    print(json.dumps(dict(status='checkpoint',row=state['next_row'],seconds=time.time()-start)),flush=True);raise SystemExit(75)
variance=prep['scientific']['sigma_e_squared'];results={}
for foot,a0 in [('canonical',a0can),('alt',1.1312e-10)]:
    F=float(total/variance)*(a0/a0can);err=1/math.sqrt(F) if F>0 else None
    results[foot]=dict(Fisher_upper=F,sigma_log10a0_lower=err,
                      amplitude_SNR_upper=2*math.sqrt(F)/math.log(10),
                      gap_009dex_significance_upper=.09*math.sqrt(F),
                      footing_gap_significance_upper=math.log10(1.1312e-10/a0can)*math.sqrt(F),
                      even_optimistic_precision_fails=err is None or err>.05)
original=prep['scientific']['in_footprint'];rotated=prep['scientific']['rotated_in_footprint']
checks=[dict(name='original_count_preserved',passed=len(rows)==original,value=dict(original=original,this_mode=len(rows))),
        dict(name='frozen_rotation_drop_over_half',passed=rotated<original/2,value=rotated/original if original else None),
        dict(name='source_selection_matches_preparation',passed=state['source_count']==prep['scientific']['source_usable']),
        dict(name='both_footings_Fisher_scaling',passed=abs(results['alt']['Fisher_upper']/results['canonical']['Fisher_upper']-1.1312e-10/a0can)<1e-12)]
science=dict(mode=mode,lenses=len(rows),source_count=state['source_count'],pair_count=state['pair_count'],
             contributing_sources=state['contributing_sources'],shape_variance=variance,results=results,checks=checks,
             interpretation='Conditional point-source upper bound; full stage0 validity and frozen controls must be assessed separately')
C.atomic_json(OUT/'forecast.json',dict(scientific=science,input_identity=identity))
C.atomic_json(OUT/'runtime.json',dict(seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
print(json.dumps(science,indent=2),flush=True)
raise SystemExit(int(any(not c['passed'] for c in checks)))
