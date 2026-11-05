#!/usr/bin/env python3
"""Atomic mask, baryon-map, stellar-profile and ring preparation after raw_cube."""
import argparse,json,math,os,platform,resource,signal,time
from pathlib import Path
import numpy as np
import scipy
import astropy
import raw_cube as R
import io_beam as B
import masking as M
import stars as S

def geometry(east,north,pa=73.7,inc=48.):
    p=math.radians(pa);a=east*math.sin(p)+north*math.cos(p);b=(-east*math.cos(p)+north*math.sin(p))/math.cos(math.radians(inc))
    radius=np.hypot(a,b);return radius,a/np.maximum(radius,1e-9)
def crop_map(path,crop,binning,raw_header):
    h,offset=B.metadata(path)
    for key in ['CRPIX1','CRPIX2','CRVAL1','CRVAL2','CDELT1','CDELT2']:
        if h[key]!=raw_header[key]:raise ValueError('Map/cube grid mismatch: '+key)
    n=crop['size'];nb=n//binning;xlo,ylo=crop['xlo'],crop['ylo'];total=np.zeros((nb,nb));counts=np.zeros((nb,nb),int)
    for lo,a in B.rows(path,h,offset,row_chunk=32):
        start=max(lo,ylo);end=min(lo+len(a),ylo+n)
        if end<=start:continue
        x=a[start-lo:end-lo,xlo:xlo+n];finite=np.isfinite(x);iy=(np.arange(start,end)-ylo)//binning
        np.add.at(total,iy,np.where(finite,x,0).reshape(len(x),nb,binning).sum(axis=2))
        np.add.at(counts,iy,finite.reshape(len(x),nb,binning).sum(axis=2))
    mean=np.full(total.shape,np.nan);np.divide(total,counts,out=mean,where=counts>0)
    return mean,h

def run(args):
    started=time.time();stop=False
    def stopping(*_):
        nonlocal stop
        stop=True
    signal.signal(signal.SIGTERM,stopping);signal.signal(signal.SIGINT,stopping)
    raw=R.HERE/args.raw;rp=raw/'raw_manifest.json';rawmeta=json.loads(rp.read_text());binning=rawmeta['identity']['binning']
    if binning!=8 and not os.environ.get('HEAVYQ_JOB_ID'):raise RuntimeError('Full preparation requires heavyq')
    for path,h in rawmeta['identity']['hashes'].items():
        if R.sha(R.ROOT/path)!=h:raise RuntimeError('Stale raw source identity')
    for path,h in rawmeta['output_hashes'].items():
        if R.sha(raw/path)!=h:raise RuntimeError('Stale raw array')
    weight=rawmeta['identity']['weight'];raw_header,_=B.metadata(R.DATA/f'IC1613_{weight}_ICL001.FITS')
    sources=[Path(__file__),Path(M.__file__),Path(S.__file__),Path(B.__file__),R.HERE/'FROZEN_CRITERIA.md',R.HERE/'AMENDMENTS.md']
    data=[R.DATA/n for n in ['IC1613_NA_X0_P_R.FITS','IC1613_NA_XMOM1.FITS','IC1613_NA_XMOM2.FITS','ic1613v.fits']]
    identity=dict(raw_manifest_sha256=R.sha(rp),hashes={os.path.relpath(p,R.ROOT):R.sha(p) for p in sources+data},
                  versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__,astropy=astropy.__version__))
    out=R.HERE/args.tag/f'{weight}_bin{binning}';out.mkdir(parents=True,exist_ok=True);manifest=out/'prep_manifest.json';done={};new=0
    if manifest.exists():
        old=json.loads(manifest.read_text())
        if not args.resume or old['identity']!=identity:raise RuntimeError('Complete preparation identity mismatch or missing --resume')
        for name,entry in old['stages'].items():
            p=out/(name+'.json')
            if R.sha(p)!=entry['sha256']:raise RuntimeError('Changed stage manifest')
            v=json.loads(p.read_text())
            if any(R.sha(out/n)!=h for n,h in v['outputs'].items()):raise RuntimeError('Changed prepared array')
        print('Verified complete preparation');return 0
    def stage(name,builder):
        nonlocal new
        p=out/(name+'.json')
        if stop:raise R.YieldRequested()
        if p.exists():
            obj=json.loads(p.read_text())
            if not args.resume or obj['identity']!=identity:raise RuntimeError('Stage identity mismatch or missing --resume')
            if any(R.sha(out/n)!=h for n,h in obj['outputs'].items()):raise RuntimeError('Stage array changed')
        else:
            if args.max_stages and new>=args.max_stages:raise R.YieldRequested()
            arrays,science=builder();outputs={}
            for key,value in arrays.items():
                f=out/(name+'_'+key+'.npy');R.save_array(f,value);outputs[f.name]=R.sha(f)
            obj=dict(identity=identity,scientific=science,outputs=outputs);B.atomic(p,obj);new+=1
        done[name]=dict(sha256=R.sha(p));B.atomic(out/'checkpoint.json',dict(identity=identity,stages=done))
        return obj
    cube=np.load(raw/'cube.npy',mmap_mode='r',allow_pickle=False);east=np.load(raw/'east.npy',allow_pickle=False);north=np.load(raw/'north.npy',allow_pickle=False)
    beam=rawmeta['scientific']['beam_arcsec_deg'];pixel=rawmeta['scientific']['pixel_arcsec'];crop=rawmeta['scientific']['crop']
    try:
        masked=stage('mask',lambda:M.make_mask(cube,pixel,beam))
        def maps():
            m0,h=crop_map(data[0],crop,binning,raw_header);m0=m0/1000
            natural_beam=B.clean_beam(h);frequency=h.get('RESTFREQ',raw_header['RESTFREQ'])
            tb=1.222e6/((frequency/1e9)**2*natural_beam[0]*natural_beam[1])
            gas=1.33*1.823e18*tb*np.nan_to_num(np.maximum(m0,0))/1.249e20
            m1,_=crop_map(data[1],crop,binning,raw_header);m2,_=crop_map(data[2],crop,binning,raw_header)
            return dict(gas_sky=gas,moment0=m0,moment1=m1/1000,moment2=m2/1000),dict(gas_mass_input='natural PB-corrected moment0 shared by both weighting fits',beam_arcsec_deg=natural_beam.tolist(),brightness_K_per_Jybeam=tb,helium_factor=1.33,diagnostic_moments='natural weighting only; not substituted for robust cube data',nonfinite_moment0=int((~np.isfinite(m0)).sum()))
        stage('maps',maps)
        stage('stars',lambda:({},S.profile(data[3],beam[0],32,lambda:stop)))
        def rings():
            mask=np.load(out/'mask_mask.npy',mmap_mode='r',allow_pickle=False).any(0)
            m0=np.load(out/'maps_moment0.npy',allow_pickle=False);m1=np.load(out/'maps_moment1.npy',allow_pickle=False);m2=np.load(out/'maps_moment2.npy',allow_pickle=False)
            radius,cth=geometry(east,north);width=beam[0];count=int(np.ceil(radius.max()/width));centres=(np.arange(count)+.5)*width
            coverage=np.zeros(count);rotation=np.full(count,np.nan);disp=rotation.copy();surface=rotation.copy();si=math.sin(math.radians(48.))
            for k in range(count):
                ring=(radius>=k*width)&(radius<(k+1)*width);coverage[k]=(ring&mask).sum()/max(ring.sum(),1)
                use=ring&mask&np.isfinite(m1)&(abs(cth)>=.5)
                if use.sum()>=8:rotation[k]=np.sum((m1[use]+232.2)*cth[use])/(si*np.sum(cth[use]**2))
                use=ring&mask&np.isfinite(m2)
                if use.sum()>=8:disp[k]=np.mean(m2[use]);surface[k]=np.mean(np.nan_to_num(m0[ring]))
            covered=np.flatnonzero(coverage>=.5)
            if not len(covered):raise ValueError('No ring reaches50% mask coverage')
            nring=int(covered[-1]+1)
            def sm3(a):
                b=a.copy();b[1:-1]=(a[:-2]+a[1:-1]+a[2:])/3;return b
            sd=sm3(disp);logq=np.log(np.clip(sm3(surface)*sd**2,1e-30,None));derivative=np.gradient(logq,np.log(centres))
            vc=np.sqrt(np.maximum(rotation**2-sd**2*derivative,0));good=np.isfinite(rotation)&np.isfinite(vc)
            benchmark_radius=2.71e3/(.7e6*math.pi/(180*3600))
            vals={} if not good.any() else dict(rotation_at_Oh_Rmax=float(np.interp(benchmark_radius,centres[good],rotation[good])),drift_at_Oh_Rmax=float(np.interp(benchmark_radius,centres[good],vc[good])))
            arrays=dict(radius=centres,coverage=coverage,rotation=rotation,dispersion=disp,surface=surface,drift_vc=vc)
            science=dict(ring_width_arcsec=width,nring=nring,R_out_arcsec=nring*width,holes_inside=int((coverage[:nring]<.5).sum()),diagnostic=vals,scope='Natural moment-map diagnostic under each own cube mask; not published bulk-field recovery')
            return arrays,science
        stage('rings',rings)
        if stop:raise R.YieldRequested()
    except (R.YieldRequested,S.YieldRequested):
        B.atomic(out/'checkpoint.json',dict(identity=identity,stages=done));print('Preparation checkpoint',list(done),flush=True);return 75
    B.atomic(manifest,dict(identity=identity,stages=done,raw_source=args.raw,weight=weight,binning=binning,
                          status='preparation complete; numerical/control cube fits NOT DONE',scope='kappa=1/2 FITTED; not theory closed'))
    B.atomic(out/'runtime.json',dict(seconds=time.time()-started,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_stages=new))
    print('Prepared',weight,binning,'stages',list(done),flush=True);return 0
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--raw',required=True);ap.add_argument('--tag',default='prepared_pilot');ap.add_argument('--resume',action='store_true');ap.add_argument('--max-stages',type=int,default=0);args=ap.parse_args()
    if args.max_stages<0:raise ValueError('max-stages must be nonnegative')
    raise SystemExit(run(args))
