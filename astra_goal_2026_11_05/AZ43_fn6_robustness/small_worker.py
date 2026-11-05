#!/usr/bin/env python3
"""One resumable FN6 small-gate point/rung; parent enforces memory limit."""
import argparse, hashlib, json, math, os, resource, signal, time
from pathlib import Path
import engines as E
ap=argparse.ArgumentParser();ap.add_argument('--index',type=int,required=True)
ap.add_argument('--rung',type=int,choices=[1,2],required=True);ap.add_argument('--mutate',action='store_true')
args=ap.parse_args(); start=time.time(); stopped=False
def stopping(signum,frame):
    global stopped
    stopped=True
signal.signal(signal.SIGTERM,stopping);signal.signal(signal.SIGINT,stopping)
HERE=Path(__file__).resolve().parent
MODE='mutate' if args.mutate else 'main'
OUT=HERE/MODE/'small';OUT.mkdir(parents=True,exist_ok=True)
path=OUT/('p%03d_r%d.json'%(args.index,args.rung))
hashes=E.hashes()
for name in ['small_worker.py','engines.py','FROZEN_CRITERIA.md']:
    hashes[name]=hashlib.sha256((HERE/name).read_bytes()).hexdigest()
if path.exists():
    old=json.loads(path.read_text())
    if old['source_hashes']!=hashes: raise RuntimeError('Checkpoint input hashes differ; preserve and inspect before reuse')
    print('Existing complete checkpoint',path.name);raise SystemExit(0)
ns=E.small();np=ns['np'];checks=[]
def check(name,ok,value=None): checks.append(dict(name=name,passed=bool(ok),value=value))

# Construct the same matrix in row chunks to bound temporary allocations.
original_kmat=ns['kmat']
def kmat(r,s):
    n=len(r);out=np.empty((n,n));dd=np.diff(r);w=np.empty(n)
    w[0]=dd[0]/2;w[-1]=dd[-1]/2;w[1:-1]=(dd[:-1]+dd[1:])/2
    Rp=r[None,:]
    for begin in range(0,n,128):
        R=r[begin:begin+128,None]
        out[begin:begin+128]=(Rp/(math.sqrt(2*math.pi)*s*R))*(np.exp(-(R-Rp)**2/(2*s*s))-np.exp(-(R+Rp)**2/(2*s*s)))*w[None,:]
    return out
rr=np.geomspace(.01,20,129)
for ss in [.1,1.,3.]:
    old=original_kmat(rr,ss);new=kmat(rr,ss)
    err=float(np.max(np.abs(new-old))/max(float(np.max(np.abs(old))),1e-300))
    check('chunked_kernel_'+str(ss),err<=1e-10,err)
ns['kmat']=kmat
quadrupole=ns['CV'].quadrupole
def qwrap(*a,**kw):
    kw.setdefault('nr',20000*args.rung);kw.setdefault('nm',200*args.rung)
    if args.mutate: kw['newtonian']=True
    return quadrupole(*a,**kw)
ns['CV'].quadrupole=qwrap
if args.rung==2:
    ns['rgrid'].__defaults__=(4000,)
    ns['profiles'].__defaults__=(3000,)
    ns['outer_field'].__defaults__=(40000,1e-10)
    ns['grade_R_num'].__defaults__=(320,)
    # The engine uses fixed orbital order256 inside its functions.
    # Its rate function accepts N explicitly, so refine that argument.
    rate=ns['rate']
    ns['rate']=lambda A,a,e,n,N:rate(A,a,e,n,2*N)
if args.mutate:
    ns['nu']=lambda y:np.ones_like(y)
    ns['dnu']=lambda y:np.zeros_like(y)

observed={}
old_sigma=ns['Dwarf'].sigma
def tracked_sigma(self,mass,a0,ge,form):
    val=old_sigma(self,mass,a0,ge,form)
    foot=min(ns['A0SI'],key=lambda f:abs(ns['A0SI'][f]*ns['CONV']-a0))
    key=self.d['name']+'|'+foot+'|'+format(float(mass),'.17g')
    observed[key]=dict(name=self.d['name'],footing=foot,mass=float(mass),width=self.L,sigma=val)
    return val
ns['Dwarf'].sigma=tracked_sigma
p,L=E.points()[args.index]
got=ns['run_point'](p,L)
# Refine every recorded coarse witness even if fine search passed earlier.
coarse=OUT/('p%03d_r1.json'%args.index)
if args.rung==2 and coarse.exists():
    old=json.loads(coarse.read_text())
    for key,row in old['dwarf_evaluations'].items():
        if key not in observed:
            d=next(d for d in ns['rows'] if d['name']==row['name'])
            dw=ns['Dwarf'](d,row['width']);a0=ns['A0SI'][row['footing']]*ns['CONV']
            dw.sigma(row['mass'],a0,ns['GEV']['E1'](d,a0),'R')
            del dw
for foot in ns['A0SI']:
    check(foot+'_finite',all(math.isfinite(got[t][foot][key]) for t,key in [('T1','Q2'),('T4','Z'),('T2','fornax_U2'),('T3','d_rms')]))
result=dict(mode=MODE,index=args.index,p=p,L_MW=L,rung=args.rung,result=got,
 dwarf_evaluations=observed,checks=checks,source_hashes=hashes,
 seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
tmp=path.with_suffix('.json.tmp')
with tmp.open('w') as f: json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
os.replace(tmp,path)
print(json.dumps(dict(index=args.index,rung=args.rung,mode=MODE,seconds=result['seconds'],rss_native=result['peak_rss_native'],checks=checks)),flush=True)
raise SystemExit(75 if stopped else int(any(not c['passed'] for c in checks)))
