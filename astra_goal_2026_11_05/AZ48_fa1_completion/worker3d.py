#!/usr/bin/env python3
"""Atomic full3D field worker; production grids are heavyq-only."""
import argparse,json,os,platform,resource,signal,time
from pathlib import Path
import numpy as np
import scipy
import audit_inputs as A
import bullet_source as B
import grid3d as D
import spherical_boundary as R
import newton3d as N

def atomic_array(path,writer):
    temp=path.with_name(path.name+'.tmp')
    with temp.open('wb') as stream:
        writer(stream);stream.flush();os.fsync(stream.fileno())
    os.replace(temp,path)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--tag',required=True);parser.add_argument('--source',choices=['bullet','plummer'],required=True)
    parser.add_argument('--n',type=int,required=True);parser.add_argument('--foot',choices=list(B.A0),required=True)
    parser.add_argument('--half-width',type=float,choices=[4000.,8000.],default=4000.)
    parser.add_argument('--homotopy',action='store_true');parser.add_argument('--resume',action='store_true')
    args=parser.parse_args();started=time.monotonic();stop=[False]
    def handler(signum,frame):stop[0]=True
    signal.signal(signal.SIGTERM,handler);signal.signal(signal.SIGINT,handler)
    out=(A.HERE/args.tag).resolve()
    if A.HERE.resolve() not in out.parents:raise ValueError('Tag must be inside lane')
    if args.n>16 and not os.environ.get('HEAVYQ_JOB_ID'):raise RuntimeError('Production grids require heavyq')
    if args.n not in [8,16,32,64,128,256]:raise ValueError('Unsupported resolution')
    if args.source=='plummer' and args.half_width!=4000.:raise ValueError('Known-answer box is fixed')
    sources=[Path(__file__).resolve(),Path(B.__file__).resolve(),Path(D.__file__).resolve(),Path(R.__file__).resolve(),Path(N.__file__).resolve(),Path(A.__file__).resolve(),B.SOURCE,A.HERE/'FROZEN_BULLET.md']
    identity=dict(arguments={k:v for k,v in vars(args).items() if k not in ['tag','resume']},source_hashes={A.relative(p):A.sha(p) for p in sources},versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__))
    out.mkdir(parents=True,exist_ok=True);checkpoint=out/'checkpoint.npz'
    state=None;phi=None
    if checkpoint.exists():
        if not args.resume:raise RuntimeError('Existing output requires --resume')
        with np.load(checkpoint,allow_pickle=False) as saved:
            state=json.loads(str(saved['state']));phi=saved['phi'].copy()
        if state['identity']!=identity:raise RuntimeError('Stale checkpoint identity')
        if state['status']=='complete':
            for filename,digest in state['outputs'].items():
                if A.sha(out/filename)!=digest:raise RuntimeError('Changed completed artifact')
            print('Verified complete field');return 0
    elif any(out.iterdir()):raise RuntimeError('Nonempty output without checkpoint')
    rows=B.components() if args.source=='bullet' else np.array([[2e14,565.,0.,0.,0.]])
    centre=B.centroid(rows);alpha=3. if args.half_width==4000. else D.expanded_alpha(args.half_width)
    grid=D.Grid(args.n,args.half_width,alpha,centre);x,y,z=grid.coordinates()
    radius=np.sqrt(sum((v-c/B.L0_KPC)**2 for v,c in zip([x,y,z],centre)))
    source=B.density(x*B.L0_KPC,y*B.L0_KPC,z*B.L0_KPC,rows)[1:-1,1:-1,1:-1]/B.RHO_REF
    epsilon=B.normalization(args.foot)['epsilon'];multipliers=[100.,10.,1.] if args.homotopy else [1.]
    max_radius=1.1*np.sqrt(3)*args.half_width/B.L0_KPC
    if state is None:
        state=dict(identity=identity,status='running',level=0,history=None,reports=[])
        phi=R.RadialPotential(epsilon*multipliers[0],max_radius,rows=rows)(radius)
    if phi.shape!=grid.shape or not np.all(np.isfinite(phi)):raise RuntimeError('Invalid checkpoint field')
    def save():
        encoded=np.array(json.dumps(state,sort_keys=True,separators=(',',':')))
        atomic_array(checkpoint,lambda stream:np.savez(stream,phi=phi,state=encoded))
    def runtime(status):
        A.atomic(out/'runtime.json',dict(status=status,seconds=time.monotonic()-started,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
    save()
    while state['level']<len(multipliers):
        if stop[0]:runtime('yield');return 75
        level=state['level'];eps=epsilon*multipliers[level]
        def accepted(field,history):
            nonlocal phi
            phi=field;state['history']=history;save()
        phi,report=N.solve(grid,source,eps,phi,accepted=accepted,stop=lambda:stop[0],history=state['history'])
        state['history']=report['history'];save()
        if report['status']=='interrupted' or stop[0]:runtime('yield');return 75
        state['reports'].append(dict(epsilon_multiplier=multipliers[level],report=report))
        if report['status']!='converged':break
        state['level']+=1;state['history']=None
        if state['level']<len(multipliers):
            old_radial=R.RadialPotential(eps,max_radius,rows=rows)(radius)
            new_radial=R.RadialPotential(epsilon*multipliers[state['level']],max_radius,rows=rows)(radius)
            phi+=new_radial-old_radial
        save()
    complete=state['level']==len(multipliers)
    # Complete refers to the bounded task, not to a successful physical result.
    atomic_array(out/'field.npy',lambda stream:np.save(stream,phi,allow_pickle=False))
    result=dict(identity=identity,status='RESIDUAL CONVERGED' if complete else 'UNDECIDED',reports=state['reports'],field_sha256=A.sha(out/'field.npy'),source_components=rows.tolist(),centre_kpc=centre.tolist(),alpha=alpha,scope='Single-grid solve only; no field-convergence or Bullet classification. kappa=1/2 FITTED; not theory closed')
    # Canonical key ordering is invariant to checkpoint serialization/loading.
    A.atomic(out/'result.json',json.loads(json.dumps(result,sort_keys=True)))
    state.update(status='complete',outputs={name:A.sha(out/name) for name in ['field.npy','result.json']});save();runtime('complete')
    print(json.dumps(dict(status=result['status'],levels=len(state['reports']),residual=state['reports'][-1]['report']['residual'])));return 0

if __name__=='__main__':raise SystemExit(main())
