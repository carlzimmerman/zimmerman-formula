#!/usr/bin/env python3
"""Restartable conditional AZ46 signal-plus-noise mock construction."""
import argparse,json,os,platform,resource,signal,time
from pathlib import Path
import numpy as np
import scipy
import fitting as F
import model as M
import mock_noise as N
import raw_cube as R
import io_beam as B

def save_array(path,value):
    temporary=path.with_suffix(path.suffix+'.tmp')
    with temporary.open('wb') as handle:np.save(handle,value,allow_pickle=False);handle.flush();os.fsync(handle.fileno())
    os.replace(temporary,path)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepared',required=True);parser.add_argument('--tag',required=True)
    parser.add_argument('--foot',choices=list(M.A0),required=True);parser.add_argument('--mock',choices=['law','slow'],required=True)
    parser.add_argument('--resume',action='store_true');args=parser.parse_args();t0=time.time();stop=[False]
    def handler(signum,frame):stop[0]=True
    signal.signal(signal.SIGTERM,handler);signal.signal(signal.SIGINT,handler)
    directory=R.HERE/args.tag
    if directory.resolve()==R.HERE.resolve() or R.HERE.resolve() not in directory.resolve().parents:raise ValueError('Output must be inside lane')
    P=M.load_prepared(args.prepared)
    if P['binning']!=8 and not os.environ.get('HEAVYQ_JOB_ID'):raise RuntimeError('Production mock construction requires heavyq')
    sources=[Path(__file__),Path(N.__file__),Path(M.__file__),Path(F.__file__),M.OLD,R.HERE/'io_beam.py',R.HERE/'raw_cube.py',R.HERE/'FROZEN_CRITERIA.md',R.HERE/'AMENDMENTS.md',R.HERE/'MODEL_NUMERICS.md',R.HERE/'NOISE_CONTRACT.md',R.ROOT/'rebuild_2026_10_22/RQ3_acceptance_v2/candidates/law.py']
    identity=dict(preparation_sha256=P['manifest_sha256'],footing=args.foot,mock=args.mock,
      source_hashes={str(p.relative_to(R.ROOT)):R.sha(p) for p in sources},
      versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
    directory.mkdir(parents=True,exist_ok=True);cp=directory/'checkpoint.json'
    state=dict(identity=identity,status='preparing',stages={})
    if cp.exists():
        if not args.resume:raise RuntimeError('Existing mock requires --resume')
        state=json.loads(cp.read_text())
        if state['identity']!=identity:raise RuntimeError('Stale mock identity')
        for stage,record in state['stages'].items():
            for name,digest in record['outputs'].items():
                if R.sha(directory/name)!=digest:raise RuntimeError('Changed mock stage')
        if state['status']=='complete':
            if R.sha(directory/'mock_manifest.json')!=state['manifest_sha256']:raise RuntimeError('Changed mock manifest')
            print('Verified complete mock');return 0
    elif args.resume and any(directory.iterdir()):raise RuntimeError('Uncheckpointed output')
    B.atomic(cp,state)
    def runtime(status):B.atomic(directory/'runtime.json',dict(status=status,seconds=time.time()-t0,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    def save_stage(name,array,meta):
        save_array(directory/(name+'.npy'),array)
        state['stages'][name]=dict(scientific=meta,outputs={name+'.npy':R.sha(directory/(name+'.npy'))})
        B.atomic(cp,state)
    def yield_if_requested():
        if stop[0]:raise N.YieldRequested('Signal at mock stage boundary')
    try:
        yield_if_requested()
        if 'signal' not in state['stages']:
            state['status']='signal';B.atomic(cp,state)
            cube=M.Cube(P);bary=M.Baryons(P,2.88e7);law=F.Law(cube,P,bary,M.A0[args.foot],thickness=200.)
            rotation,rr,vc=law.rotation(0.,0.,73.7,35.,np.full(6,9.));scale=1. if args.mock=='law' else .505
            vl,sg,_=M.C.vfield(cube,0.,0.,73.7,35.,-232.2,lambda radius:scale*rotation(radius),lambda radius:np.full(radius.shape,9.))
            signal_cube=cube.model(vl,sg)
            meta=dict(geometry=dict(x0=0.,y0=0.,pa=73.7,inc=35.,vsys=-232.2),sigma=9.,rotation_scale=scale,
                mstar=2.88e7,thickness_pc=200.,vc_at_2kpc=float(np.interp(2000/M.C.arcsec_to_pc(1.),rr,vc)),
                rotation_at_2kpc=float(scale*rotation(2000/M.C.arcsec_to_pc(1.))),fallback_pixels=cube.fallback_last,
                shape=list(signal_cube.shape),intensity_template='own prepared observed intensity; unchanged conditional normalization')
            save_stage('signal',signal_cube,meta);del cube,bary,law,signal_cube
        yield_if_requested()
        if 'noise' not in state['stages']:
            state['status']='noise';B.atomic(cp,state)
            noise,meta=N.prepared_noise(P,args.foot,0 if args.mock=='law' else 1,stop=lambda:stop[0])
            save_stage('noise',noise,meta);del noise
        yield_if_requested()
        if 'cube' not in state['stages']:
            state['status']='combining';B.atomic(cp,state)
            signal_cube=np.load(directory/'signal.npy',mmap_mode='r');noise=np.load(directory/'noise.npy',mmap_mode='r')
            mock=signal_cube+noise;save_stage('cube',mock,dict(shape=list(mock.shape),finite=bool(np.all(np.isfinite(mock)))))
        yield_if_requested()
    except N.YieldRequested:
        state['status']='interrupted';B.atomic(cp,state);runtime('yield');return 75
    manifest=dict(identity=identity,stages=state['stages'],scope='Conditional synthetic cube only; frozen KA1/KA2 fit gates not evaluated; kappa=1/2 FITTED; not theory closed')
    B.atomic(directory/'mock_manifest.json',manifest);state.update(status='complete',manifest_sha256=R.sha(directory/'mock_manifest.json'));B.atomic(cp,state);runtime('complete')
    print(json.dumps(dict(mock=args.mock,foot=args.foot,weight=P['weight'],noise_rms=state['stages']['noise']['scientific']['scaled_rms'])));return 0

if __name__=='__main__':raise SystemExit(main())
