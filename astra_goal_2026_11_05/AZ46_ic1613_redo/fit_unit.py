#!/usr/bin/env python3
"""One restartable AZ46 model/inclination/start fit; production is queue-only."""
import argparse,json,os,platform,resource,signal,time
from pathlib import Path
import numpy as np
import scipy
import fitting as F
import model as M
import raw_cube as R
import io_beam as B

def main():
 parser=argparse.ArgumentParser(description=__doc__)
 parser.add_argument('--prepared',required=True);parser.add_argument('--tag',required=True)
 parser.add_argument('--model',choices=['free','law','nc','newton'],required=True)
 parser.add_argument('--foot',choices=list(M.A0),default='canonical')
 parser.add_argument('--dataset',choices=['real','mutate','ka1','ka2'],default='real')
 parser.add_argument('--mock-source',help='Relative directory of a hash-verified constructed mock')
 parser.add_argument('--inclination',type=float,help='Fixed inclination; omit for free-inclination fit')
 parser.add_argument('--start-inc',type=float,choices=[35.,48.],default=48.)
 parser.add_argument('--budget',type=int,choices=[2,100,200],default=100)
 parser.add_argument('--mstar',type=float,choices=[2.88e7,1.9e8],default=2.88e7)
 parser.add_argument('--thickness',type=float,choices=[100.,200.,300.],default=200.)
 parser.add_argument('--initial',help='Relative path to a verified fit result for grid-best refinement')
 parser.add_argument('--resume',action='store_true')
 args=parser.parse_args();t0=time.time();stop=[False]
 def handler(signum,frame):stop[0]=True
 signal.signal(signal.SIGTERM,handler);signal.signal(signal.SIGINT,handler)
 out=R.HERE/args.tag
 if out.resolve()==R.HERE.resolve() or R.HERE.resolve() not in out.resolve().parents:raise ValueError('Tag must be inside lane')
 if args.dataset=='mutate' and 'mutate' not in out.parts:raise ValueError('Mutation must use separate mutate output tree')
 if args.model=='free' and args.inclination is not None:raise ValueError('Free model cannot have fixed inclination')
 if args.inclination is not None and not 15<=args.inclination<=60:raise ValueError('Inclination outside frozen range')
 P=M.load_prepared(args.prepared)
 if (P['binning']!=8 or args.budget!=2) and not os.environ.get('HEAVYQ_JOB_ID'):raise RuntimeError('Full fits require heavyq; only bin8 budget2 is an unqueued pilot')
 sources=[Path(__file__),Path(F.__file__),Path(M.__file__),M.OLD,R.HERE/'io_beam.py',R.HERE/'raw_cube.py',R.HERE/'FROZEN_CRITERIA.md',R.HERE/'AMENDMENTS.md',R.HERE/'MODEL_NUMERICS.md',R.ROOT/'rebuild_2026_10_22/RQ3_acceptance_v2/candidates/law.py']
 identity=dict(arguments={k:v for k,v in vars(args).items() if k not in ('tag','resume','prepared','initial','mock_source')},
               preparation_sha256=P['manifest_sha256'],source_hashes={str(p.relative_to(R.ROOT)):R.sha(p) for p in sources},
               versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
 mock_data=None
 if args.dataset in ('ka1','ka2'):
  if not args.mock_source:raise ValueError('Mock dataset requires --mock-source')
  mock_dir=R.HERE/args.mock_source;mock_path=mock_dir/'mock_manifest.json';mock=json.loads(mock_path.read_text())
  mi=mock['identity']
  if mi['preparation_sha256']!=P['manifest_sha256'] or mi['footing']!=args.foot or mi['mock']!=('law' if args.dataset=='ka1' else 'slow'):raise ValueError('Mock preparation/footing/type mismatch')
  if mi['versions']!=identity['versions']:raise ValueError('Mock environment mismatch')
  for name,digest in mi['source_hashes'].items():
   if R.sha(R.ROOT/name)!=digest:raise ValueError('Stale mock engine')
  for stage in mock['stages'].values():
   for name,digest in stage['outputs'].items():
    if R.sha(mock_dir/name)!=digest:raise ValueError('Changed mock array')
  identity['mock_manifest_sha256']=R.sha(mock_path);mock_data=np.load(mock_dir/'cube.npy',mmap_mode='r',allow_pickle=False)
  if mock_data.shape!=P['cube'].shape:raise ValueError('Mock shape mismatch')
 elif args.mock_source:raise ValueError('Mock source supplied for non-mock dataset')
 initial=None
 if args.initial:
  ipath=R.HERE/args.initial;initial=json.loads(ipath.read_text());identity['initial_sha256']=R.sha(ipath)
  if initial['identity']['preparation_sha256']!=P['manifest_sha256']:raise ValueError('Refinement preparation mismatch')
  if initial['identity'].get('mock_manifest_sha256')!=identity.get('mock_manifest_sha256'):raise ValueError('Refinement mock mismatch')
  if initial['identity']['source_hashes']!=identity['source_hashes'] or initial['identity']['versions']!=identity['versions']:raise ValueError('Refinement engine mismatch')
  prior=initial['identity']['arguments']
  for name in ('model','foot','dataset','mstar','thickness'):
   if prior[name]!=identity['arguments'][name]:raise ValueError('Refinement model mismatch')
  if args.model=='free' or args.inclination is not None or prior['inclination'] is None:raise ValueError('Initial result must refine a fixed-inclination law family')
 out.mkdir(parents=True,exist_ok=True);checkpoint=out/'checkpoint.json'
 if checkpoint.exists():
  if not args.resume:raise RuntimeError('Existing fit requires --resume')
  state=json.loads(checkpoint.read_text())
  if state['identity']!=identity:raise RuntimeError('Stale fit identity')
  if state['status']=='complete':
   if R.sha(out/'result.json')!=state['result_sha256']:raise RuntimeError('Changed completed fit')
   print('Verified complete fit');return 0
 elif args.resume and any(out.iterdir()):raise RuntimeError('Uncheckpointed nonempty output')
 state=dict(identity=identity,status='preparing');B.atomic(checkpoint,state)
 def runtime(status):B.atomic(out/'runtime.json',dict(status=status,seconds=time.time()-t0,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
 if stop[0]:runtime('yield');return 75
 permutation=None;data=mock_data
 if args.dataset=='mutate':
  permutation=np.random.default_rng(7).permutation(len(P['v']));data=np.asarray(P['cube'])[permutation]
 cube=M.Cube(P,data=data)
 if args.model=='free':
  model=F.Free(cube,P,stop=lambda:stop[0]);start=model.start(args.start_inc)
 else:
  model=F.Law(cube,P,M.Baryons(P,args.mstar),M.A0[args.foot],modified=args.model!='newton',nc=args.model=='nc',thickness=args.thickness,stop=lambda:stop[0])
  start=model.start(args.start_inc if args.inclination is None else None)
  if initial is not None:start=np.r_[prior['inclination'],initial['fit']['parameters']]
 state['status']='fitting';B.atomic(checkpoint,state)
 try:
  result=model.fit(start,budget=args.budget) if args.model=='free' else model.fit(start,inc=args.inclination,budget=args.budget)
  if stop[0]:raise F.YieldRequested('Signal after optimizer')
 except F.YieldRequested:
  state['status']='interrupted';B.atomic(checkpoint,state);runtime('yield');return 75
 fit=F.summarize(result,cube,model,args.budget)
 if args.model=='free':fit['inclination']=float(result.x[3]);fit['vc_at_2kpc']=None
 else:
  inc=args.inclination if args.inclination is not None else float(result.x[0]);p=result.x if args.inclination is not None else result.x[1:]
  _,rr,vc=model.rotation(*p[:3],inc,p[4:10]);fit['inclination']=float(inc);fit['vc_at_2kpc']=float(np.interp(2000/M.C.arcsec_to_pc(1.),rr,vc))
 obj=dict(identity=identity,fit=fit,start=start.tolist(),channel_permutation=None if permutation is None else permutation.tolist(),
          scope='Individual optimizer unit only; numerical, control, convergence and local-cube verdicts remain separate; kappa=1/2 FITTED; not theory closed')
 B.atomic(out/'result.json',obj);state.update(status='complete',result_sha256=R.sha(out/'result.json'));B.atomic(checkpoint,state);runtime('complete')
 print(json.dumps(dict(status=fit['status'],nfev=fit['nfev'],chi2_red=fit['chi2_red'],scope=fit['scope'])));return 0

if __name__=='__main__':raise SystemExit(main())
