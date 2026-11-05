#!/usr/bin/env python3
"""Stream source/BGS footprints and source shape variance with bounded memory."""
import argparse,hashlib,json,os,resource,signal,tempfile,time
from pathlib import Path
for name in ['OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS']:os.environ[name]='1'
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'az44_mpl'))
import numpy as np
import healpy as hp
import catalogues as C
ap=argparse.ArgumentParser();ap.add_argument('--chunk',type=int,choices=[10000,20000],required=True)
ap.add_argument('--tag',default='main');ap.add_argument('--max-chunks',type=int,default=200)
args=ap.parse_args();HERE=Path(__file__).resolve().parent;OUT=HERE/args.tag/('chunk'+str(args.chunk));OUT.mkdir(parents=True,exist_ok=True)
start=time.time();stop=False;used=0
def stopping(sig,frame):
    global stop
    stop=True
signal.signal(signal.SIGTERM,stopping);signal.signal(signal.SIGINT,stopping)
checkpoint=OUT/'prepare_checkpoint.npz'
colS=['RAJ2000','DECJ2000','Z_B','e1','e2','weight'];colB=['RA','DEC','Z_not4clus','ZWARN']
sm,sd=C.metadata(C.PATHS['shear'],colS);bm,bd=C.metadata(C.PATHS['bgs'],colB)
ident=dict(shear=sm,bgs=bm,scripts={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__),HERE/'catalogues.py',HERE/'FROZEN_CRITERIA.md']})
NPIX=hp.nside2npix(512);pix=np.zeros(NPIX,bool);usable=np.zeros(NPIX,bool);bgs=np.zeros(NPIX,bool)
state=dict(identity=ident,source_next=0,bgs_next=0,source_positions=0,source_usable=0,bgs_positions=0,bgs_good_z=0,
           moments=['0']*5,source_chunk_hashes=[],bgs_chunk_hashes=[])
if checkpoint.exists():
    with np.load(checkpoint,allow_pickle=False) as ck:
        state=json.loads(str(ck['state']))
        if state['identity']!=ident:raise RuntimeError('Preparation checkpoint inputs changed')
        pix=np.unpackbits(ck['pix'],count=NPIX).astype(bool);usable=np.unpackbits(ck['usable'],count=NPIX).astype(bool);bgs=np.unpackbits(ck['bgs'],count=NPIX).astype(bool)
mom=np.array(state['moments'],dtype=np.longdouble)
def save():
    state['moments']=[str(x) for x in mom]
    tmp=checkpoint.with_suffix('.npz.tmp')
    with tmp.open('wb') as f:
        np.savez_compressed(f,state=np.array(json.dumps(state)),pix=np.packbits(pix),usable=np.packbits(usable),bgs=np.packbits(bgs))
        f.flush();os.fsync(f.fileno())
    os.replace(tmp,checkpoint)
def limited():
    return stop or used>=args.max_chunks
for lo,arr,digest in C.raw_chunks(C.PATHS['shear'],sm,sd,args.chunk,state['source_next']):
    if limited():break
    ra=arr['RAJ2000'].astype('f8');dec=arr['DECJ2000'].astype('f8')
    pos=np.isfinite(ra)&np.isfinite(dec)&(ra>=0)&(ra<360)&(abs(dec)<=90)
    pp=hp.ang2pix(512,ra[pos],dec[pos],lonlat=True);pix[pp]=True
    zz=arr['Z_B'].astype('f8');e1=arr['e1'].astype('f8');e2=arr['e2'].astype('f8');w=arr['weight'].astype('f8')
    good=pos&np.isfinite(zz)&np.isfinite(e1)&np.isfinite(e2)&np.isfinite(w)&(w>0)
    usable[hp.ang2pix(512,ra[good],dec[good],lonlat=True)]=True
    ww=w[good].astype(np.longdouble);ee1=e1[good].astype(np.longdouble);ee2=e2[good].astype(np.longdouble)
    mom+=np.array([np.sum(ww),np.sum(ww*ee1),np.sum(ww*ee2),np.sum(ww*ee1*ee1),np.sum(ww*ee2*ee2)],dtype=np.longdouble)
    state['source_positions']+=int(pos.sum());state['source_usable']+=int(good.sum());state['source_next']=lo+len(arr)
    state['source_chunk_hashes'].append(digest);used+=1
    if used%20==0:save()
save()
if state['source_next']==sm['rows']:
    for lo,arr,digest in C.raw_chunks(C.PATHS['bgs'],bm,bd,args.chunk,state['bgs_next']):
        if limited():break
        ra=arr['RA'].astype('f8');dec=arr['DEC'].astype('f8');zz=arr['Z_not4clus'].astype('f8')
        pos=np.isfinite(ra)&np.isfinite(dec)&(ra>=0)&(ra<360)&(abs(dec)<=90)
        good=pos&np.isfinite(zz)&(zz>0)&(arr['ZWARN']==0)
        bgs[hp.ang2pix(512,ra[good],dec[good],lonlat=True)]=True
        state['bgs_positions']+=int(pos.sum());state['bgs_good_z']+=int(good.sum());state['bgs_next']=lo+len(arr)
        state['bgs_chunk_hashes'].append(digest);used+=1
        if used%20==0:save()
    save()
if state['source_next']<sm['rows'] or state['bgs_next']<bm['rows']:
    print(json.dumps(dict(status='checkpoint',source_rows=state['source_next'],bgs_rows=state['bgs_next'],seconds=time.time()-start)),flush=True)
    raise SystemExit(75)
ls,counts,hashes=C.lenses()
for row in ls:
    pixel=int(hp.ang2pix(512,row['ra'],row['dec'],lonlat=True))
    rotate=int(hp.ang2pix(512,(row['ra']+180)%360,row['dec'],lonlat=True))
    row.update(in_source_footprint=bool(pix[pixel]),in_usable_footprint=bool(usable[pixel]),
               rotated_in_footprint=bool(pix[rotate]),in_BGS_observed_pixel=bool(bgs[pixel]))
means=mom[1:3]/mom[0];vars=mom[3:5]/mom[0]-means*means
area=float(pix.sum()*hp.nside2pixarea(512,degrees=True));count=sum(r['in_source_footprint'] for r in ls);rot=sum(r['rotated_in_footprint'] for r in ls)
checks=[dict(name='K1_alpha_rows',passed=counts['alpha_rows']==31502,value=counts['alpha_rows']),
        dict(name='K2_provisional_area',passed=abs(area/777-1)<=.05,value=area),
        dict(name='rotation_expected_count_drop',passed=rot<count/2,value=dict(original=count,rotated=rot))]
science=dict(input_counts=counts,source_positions=state['source_positions'],source_usable=state['source_usable'],
             area_deg2=area,usable_area_deg2=float(usable.sum()*hp.nside2pixarea(512,degrees=True)),
             bgs_positions=state['bgs_positions'],bgs_good_z=state['bgs_good_z'],
             shape_means=[float(x) for x in means],shape_variances=[float(x) for x in vars],sigma_e_squared=float(np.mean(vars)),
             in_footprint=count,rotated_in_footprint=rot,usable_footprint_lenses=sum(r['in_usable_footprint'] for r in ls),
             observed_BGS_pixel_lenses=sum(r['in_BGS_observed_pixel'] and r['in_source_footprint'] for r in ls))
C.atomic_json(OUT/'prepared.json',dict(status='Catalogue preparation only; Fisher forecast pending',scientific=science,checks=checks,
                                     lenses=ls,input_identity=ident,small_input_hashes=hashes))
C.atomic_json(OUT/'prepare_runtime.json',dict(seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,chunk=args.chunk))
print(json.dumps(dict(status='prepared',scientific=science,checks=checks,seconds=time.time()-start),indent=2),flush=True)
# K2 is explicitly provisional and the mutation count diagnostic is reported.
raise SystemExit(0 if checks[0]['passed'] else 1)
