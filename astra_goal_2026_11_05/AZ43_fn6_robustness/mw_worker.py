#!/usr/bin/env python3
"""Bounded MW cell batches; same frozen local grid on both footings."""
import argparse, ast, gc, hashlib, json, math, os, resource, signal, time
from pathlib import Path
import engines as E
ap=argparse.ArgumentParser();ap.add_argument('--index',type=int,required=True)
ap.add_argument('--footing',choices=['canonical','alt'],required=True)
ap.add_argument('--rung',type=int,choices=[1,2],required=True)
ap.add_argument('--max-cells',type=int,default=16);ap.add_argument('--mutate',action='store_true')
args=ap.parse_args();start=time.time();stop=False
def stopping(signum,frame):
    global stop
    stop=True
signal.signal(signal.SIGTERM,stopping);signal.signal(signal.SIGINT,stopping)
HERE=Path(__file__).resolve().parent;mode='mutate' if args.mutate else 'main'
OUT=HERE/mode/'mw';OUT.mkdir(parents=True,exist_ok=True)
path=OUT/('%s_p%03d_r%d.json'%(args.footing,args.index,args.rung))
hashes=E.hashes()
for name in ['mw_worker.py','engines.py','FROZEN_CRITERIA.md']:
    hashes[name]=hashlib.sha256((HERE/name).read_bytes()).hexdigest()
res=dict(mode=mode,footing=args.footing,index=args.index,rung=args.rung,source_hashes=hashes,cells={},complete=False)
if path.exists():
    res=json.loads(path.read_text())
    if res['source_hashes']!=hashes: raise RuntimeError('Checkpoint input mismatch')
    if res['complete']: print('Already complete',flush=True);raise SystemExit(0)
def save():
    res['peak_rss_native']=max(res.get('peak_rss_native',0),resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    tmp=path.with_suffix('.json.tmp')
    with tmp.open('w') as f:json.dump(res,f,separators=(',',':'));f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)
K=E.mw();C=K.C;np=K.np
cells=[c for c in E.local_cells() if C.L.RD_TAG[0]<=c['rd']<=C.L.RD_TAG[1] and C.L.MSTAR_TAG[0]<=K.rho_cell(c)[1]<=C.L.MSTAR_TAG[1]]
res['grid_cells']=cells
gm=K.gas_mass();mass=[K.rho_cell(c)[1]+gm for c in cells]
p,L=E.points()[args.index];width=[L*(m/6e10)**p for m in mass]
res.update(p=p,L_MW=L,mass=mass,width=width)
g,mu=K.make_grid(C.A0[args.footing],args.rung,1);sol=K.Solver(g,mu,C.A0[args.footing])
if args.mutate:sol.phantom=lambda pn,mut=False:np.zeros_like(pn)
used=0
for i in sorted(range(len(cells)),key=lambda i:width[i]):
    if str(i) in res['cells']:continue
    if stop or used>=args.max_cells:
        save();print(json.dumps(dict(checkpoint=path.name,completed_cells=len(res['cells']),total=len(cells),seconds=time.time()-start)),flush=True)
        raise SystemExit(75)
    got=sol.solve(cells[i],width[i],lmax=2*(g.Nt-1))
    res['cells'][str(i)]={k:got['corrected'][k] for k in ['vc','K0','cK','cO','h','D','L1','L2a','L2b','L3','Lh','all_four']}
    used+=1;save()
# Reuse the original separable-reference V1 calculation with this grid.
src=E.FN6/'fn6_mw.py';tree=ast.parse(src.read_text())
names={'kt14_defs','interp_f','parts','v1row'}
funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
ns=dict(os=os,ast=ast,np=np,math=math,gc=gc,RB=str(E.ROOT/'rebuild_2026_10_22'),MUT=False,
        K33=K,g=g,Mu=mu,sol=sol,LU=sol.LU,LMAXF=2*(g.Nt-1))
exec(compile(ast.Module(body=funcs,type_ignores=[]),str(src),'exec'),ns)
ns['K14']=ns['kt14_defs']()
for key in ['RIN','ROUT','ZIN','WIN','radial_matrix','vsmooth','HI','H2','HIr','H2r','HIz','H2z','amps']:
    ns[key]=ns['K14'][key]
ns['VC1']=dict(box='BV2',sb=53.9,mbb=2.12e10,rd=2.6,ht=.35,hk=1.08,fk=.35,rdk=2.)
res['V1']={str(w):ns['v1row'](w) for w in sorted({min(width),max(width)})}
res['complete']=True
res['passing']=[int(i) for i,row in res['cells'].items() if row['all_four']]
save()
print(json.dumps(dict(checkpoint=path.name,complete=True,passing=len(res['passing']),seconds=time.time()-start,rss_native=res['peak_rss_native'])),flush=True)
raise SystemExit(75 if stop else 0)
