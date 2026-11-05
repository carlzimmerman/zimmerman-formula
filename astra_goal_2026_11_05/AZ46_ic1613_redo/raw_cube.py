#!/usr/bin/env python3
"""Restartable raw-cube crop/bin stage; does not build masks or grade fits."""
import argparse,hashlib,json,math,os,platform,resource,signal,time,warnings
from pathlib import Path
import numpy as np
import astropy
from astropy.wcs import WCS,FITSFixedWarning
from astropy.coordinates import SkyCoord
import astropy.units as u
import io_beam as B
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[1]
DATA=ROOT.parent/'_external_data/fn4a_ic1613_2026_11'
class YieldRequested(Exception):pass

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for x in iter(lambda:f.read(1<<20),b''):h.update(x)
    return h.hexdigest()
def save_array(path,array):
    path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix('.tmp')
    with tmp.open('wb') as f:np.save(f,array,allow_pickle=False);f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
def read_plane(path,header,offset,plane,xlo,ylo,size,binning,row_chunk,stop=lambda:False):
    if size%binning or min(xlo,ylo)<0 or xlo+size>header['NAXIS1'] or ylo+size>header['NAXIS2']:
        raise ValueError('Invalid bounded crop')
    nb=size//binning;out=np.zeros((nb,nb));bad=0
    for lo,raw in B.rows(path,header,offset,plane,row_chunk):
        if stop():raise YieldRequested()
        start=max(lo,ylo);end=min(lo+len(raw),ylo+size)
        if end<=start:continue
        a=raw[start-lo:end-lo,xlo:xlo+size];invalid=~np.isfinite(a);bad+=int(invalid.sum());a=np.where(invalid,0.,a)
        sums=a.reshape(len(a),nb,binning).sum(axis=2)
        np.add.at(out,(np.arange(start,end)-ylo)//binning,sums)
    return (out/binning**2).astype('f4'),bad

def velocity_axis(header,wcs):
    values=np.asarray(wcs.spectral.pixel_to_world_values(np.arange(header['NAXIS3'])))
    velocity=(values*u.Unit(wcs.spectral.world_axis_units[0])).to_value(u.km/u.s)
    linear=(header['CRVAL3']+(np.arange(header['NAXIS3'])+1-header['CRPIX3'])*header['CDELT3'])/1000
    return velocity,linear

def run(args):
    if args.max_planes<0:raise ValueError('max-planes must be nonnegative')
    if args.binning!=8 and not os.environ.get('HEAVYQ_JOB_ID'):raise RuntimeError('Full2x2/4x4 preparation requires heavyq')
    stop=False
    def stopping(*_):
        nonlocal stop
        stop=True
    signal.signal(signal.SIGTERM,stopping);signal.signal(signal.SIGINT,stopping)
    start=time.time();path=DATA/f'IC1613_{args.weight}_ICL001.FITS';header,offset=B.metadata(path)
    beam=B.clean_beam(header)
    with warnings.catch_warnings(record=True) as records:
        warnings.simplefilter('always',FITSFixedWarning);full_wcs=WCS(header);w=full_wcs.celestial
    ra=(1+4/60+49.6/3600)*15;dec=2+8/60+14.1/3600
    xc,yc=map(float,w.world_to_pixel(SkyCoord(ra*u.deg,dec*u.deg,frame='fk5')))
    xlo,ylo=int(round(xc))-600,int(round(yc))-600;size=1200;nb=size//args.binning;nz=header['NAXIS3']
    out=HERE/args.tag/f'{args.weight}_bin{args.binning}_rows{args.row_chunk}';out.mkdir(parents=True,exist_ok=True)
    files=[path,Path(__file__),Path(B.__file__),HERE/'FROZEN_CRITERIA.md',HERE/'AMENDMENTS.md']
    identity=dict(hashes={os.path.relpath(p,ROOT):sha(p) for p in files},weight=args.weight,binning=args.binning,row_chunk=args.row_chunk,
                  versions=dict(python=platform.python_version(),numpy=np.__version__,astropy=astropy.__version__))
    checkpoint=out/'checkpoint.json';final=out/'raw_manifest.json'
    if final.exists():
        v=json.loads(final.read_text())
        if not args.resume or v['identity']!=identity:raise RuntimeError('Completed-stage identity mismatch or missing --resume')
        if any(sha(out/n)!=h for n,h in v['output_hashes'].items()):raise RuntimeError('Completed raw-stage output changed')
        print('Verified complete raw preparation');return 0
    state=json.loads(checkpoint.read_text()) if checkpoint.exists() else dict(identity=identity,planes=[])
    if state['identity']!=identity or (checkpoint.exists() and not args.resume):raise RuntimeError('Checkpoint identity mismatch or missing --resume')
    for index,row in enumerate(state['planes']):
        if row['plane']!=index:raise RuntimeError('Noncontiguous plane checkpoint')
        if sha(out/'planes'/f"p{row['plane']:04d}.npy")!=row['sha256']:raise RuntimeError('Corrupt plane checkpoint')
    completed=len(state['planes']);new=0
    try:
        for plane in range(completed,nz):
            if stop or (args.max_planes and new>=args.max_planes):raise YieldRequested()
            a,bad=read_plane(path,header,offset,plane,xlo,ylo,size,args.binning,args.row_chunk,lambda:stop)
            f=out/'planes'/f'p{plane:04d}.npy';save_array(f,a)
            state['planes'].append(dict(plane=plane,sha256=sha(f),nonfinite_pixels=bad));B.atomic(checkpoint,state);new+=1
        if stop:raise YieldRequested()
    except YieldRequested:
        B.atomic(checkpoint,state);print('Checkpointed raw planes',len(state['planes']),flush=True);return 75
    cube=np.stack([np.load(out/'planes'/f'p{k:04d}.npy',allow_pickle=False) for k in range(nz)])
    save_array(out/'cube.npy',cube)
    centres=np.arange(nb)*args.binning+(args.binning-1)/2
    east=np.broadcast_to(((xlo+centres)-xc)[None,:]*header['CDELT1']*3600,(nb,nb))
    north=np.broadcast_to(((ylo+centres)-yc)[:,None]*header['CDELT2']*3600,(nb,nb))
    velocity,linear_velocity=velocity_axis(header,full_wcs)
    for name,a in [('east.npy',east),('north.npy',north),('velocity.npy',velocity)]:save_array(out/name,a)
    outputs={n:sha(out/n) for n in ['cube.npy','east.npy','north.npy','velocity.npy']}
    science=dict(shape=list(cube.shape),crop=dict(xlo=xlo,ylo=ylo,size=size,centre_pixel=[xc,yc]),beam_arcsec_deg=beam.tolist(),
                 pixel_arcsec=[abs(header['CDELT1'])*3600*args.binning,abs(header['CDELT2'])*3600*args.binning],
                 nonfinite_pixels=sum(r['nonfinite_pixels'] for r in state['planes']),max_spectral_WCS_minus_linear_kms=float(np.max(abs(velocity-linear_velocity))),wcs_header_repairs=[str(r.message) for r in records],
                 status='raw crop/bin stage complete; masks, baryon maps and fits NOT DONE',
                 scope='Both a0 footings share these geometric inputs; kappa=1/2 FITTED; not theory closed')
    B.atomic(final,dict(identity=identity,scientific=science,output_hashes=outputs))
    B.atomic(out/'runtime.json',dict(seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_planes=new))
    print(json.dumps(science),flush=True);return 0
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--weight',choices=['NA','R'],required=True);ap.add_argument('--binning',type=int,choices=[2,4,8],required=True)
    ap.add_argument('--row-chunk',type=int,choices=[32,64],default=32);ap.add_argument('--tag',default='raw_pilot')
    ap.add_argument('--resume',action='store_true');ap.add_argument('--max-planes',type=int,default=0);args=ap.parse_args()
    raise SystemExit(run(args))
