#!/usr/bin/env python3
"""Checkpointed full retained-hit G3 census; sqlite keeps unique formulas bounded."""
import argparse,collections,gzip,hashlib,json,math,os,platform,resource,signal,sqlite3,time
from pathlib import Path
import g3 as G
import numpy as np
ap=argparse.ArgumentParser();ap.add_argument('--foot',choices=G.FOOTS,required=True)
ap.add_argument('--mode',choices=['real','control'],required=True);ap.add_argument('--level',choices=['L1','L2'],required=True)
ap.add_argument('--chunk',type=int,choices=[1000,2000],required=True);ap.add_argument('--tag',default='census')
ap.add_argument('--max-chunks',type=int,default=0);ap.add_argument('--resume',action='store_true')
ap.add_argument('--light-budget-seconds',type=int,choices=[0,180],default=0)
ap.add_argument('--verify-templates',action='store_true');args=ap.parse_args()
if not os.environ.get('HEAVYQ_JOB_ID') and not (0<args.max_chunks<=20 or args.light_budget_seconds==180):
    raise RuntimeError('Outside heavyq only a bounded pilot of at most20 chunks is permitted')
stop=False
def stopping(*_):
    global stop
    stop=True
signal.signal(signal.SIGTERM,stopping);signal.signal(signal.SIGINT,stopping)
start=time.time();W=G.BK/'chunks'/f'{args.level}_{args.foot}_{args.mode}'
OUT=G.HERE/args.tag/f'{args.level}_{args.foot}_{args.mode}'/f'chunk{args.chunk}';OUT.mkdir(parents=True,exist_ok=True)
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
files=[W/'hits.jsonl',W/'names.json.gz',W/'order.json.gz',G.HERE/'scatter.json',G.HERE/'FROZEN_CRITERIA.md',G.HERE/'AMENDMENTS.md',G.HERE/'g3.py',Path(__file__),G.BK/'bk2_lib.py']
for rel,expected in G.SCATTER['source_hashes'].items():
    if rel.startswith('real_research/data/xcop/'):
        p=G.ROOT/rel
        if sha(p)!=expected:raise RuntimeError('Mass-profile input changed since scatter measurement')
        files.append(p)
identity=dict(files={str(p.relative_to(G.ROOT)):sha(p) for p in files},foot=args.foot,mode=args.mode,level=args.level,chunk=args.chunk,
              versions=dict(python=platform.python_version(),numpy=np.__version__))
db=sqlite3.connect(OUT/'checkpoint.sqlite');db.execute('PRAGMA journal_mode=WAL');db.execute('PRAGMA synchronous=FULL')
db.execute('CREATE TABLE IF NOT EXISTS state (id INTEGER PRIMARY KEY, data TEXT NOT NULL)')
db.execute('CREATE TABLE IF NOT EXISTS formula (hash BLOB PRIMARY KEY, accepted INTEGER, stable INTEGER, mutated INTEGER) WITHOUT ROWID')
old=db.execute('SELECT data FROM state WHERE id=1').fetchone()
def counters():return dict(valid=0,invalid=0,line=0,legacy_err=0,diagonal_err=0,covariance_err=0,stable_covariance_err=0,unstable=0,mutation_changes=0,
                          min_Z_cov=None,max_Z_cov=None,min_Z_legacy=None,max_Z_legacy=None,min_Z_diagonal=None,max_Z_diagonal=None)
state=json.loads(old[0]) if old else dict(identity=identity,offset=0,rows=0,checks=0,max_scalar_error=0.,main=counters(),mutate=counters(),complete=False)
if state['identity']!=identity:raise RuntimeError('Checkpoint identity mismatch')
if old and not args.resume:raise RuntimeError('Existing checkpoint requires --resume')
if state['complete']:print('Verified completed census',state['rows']);raise SystemExit(0)
if state.get('queue_required') and not os.environ.get('HEAVYQ_JOB_ID'):raise RuntimeError('This census exceeded the light envelope; remaining work requires heavyq')
N=json.load(gzip.open(W/'names.json.gz','rt'));order=json.load(gzip.open(W/'order.json.gz','rt'))
order={k:np.asarray(v,dtype=np.int64) for k,v in order.items()}
T=G.dataset(args.foot,args.mode);nr=len(T['go']);KG=np.logspace(-3,3,81)
cache={k:np.empty((len(v),nr)) for k,v in N.items()};ready={k:np.zeros(len(v),bool) for k,v in N.items()}
def basis(kind,indices):
    ix=np.asarray(indices,int)
    if kind in ['A','D']:ix=order['oa' if kind=='A' else 'oD'][ix]
    for j in np.unique(ix[~ready[kind][ix]]):
        cache[kind][j]=G.B.ev(N[kind][j],T);ready[kind][j]=True
    return cache[kind][ix]
def formula(h):
    b,i,j=h[:3];a=lambda k:N['A'][order['oa'][k]];d=lambda k:N['D'][order['oD'][k]]
    if b.startswith('T1'):return f'{b[3:]}({a(i)},{a(j)})'
    if b=='T2p':return f'({a(i)}+{a(j)})'
    if b=='T2m':return f'({a(i)}-{a(j)})'
    if b.startswith('T3'):
        _,k,op=b.split('|');return f'{k}(gb,a0)*({d(i)}{op}{d(j)})'
    if b=='T4':return f"{N['A0'][i]}*{d(j)}"
    if b.startswith('T5m'):return f'{b[4:]}(gb,a0)*(1+{KG[i]!r}*{d(j)})'
    if b.startswith('T5a'):return f'({b[4:]}(gb,a0)+{KG[i]!r}*{a(j)})'
    raise RuntimeError('Unknown retained template '+b)
def predictions(hits):
    result=np.empty((len(hits),nr));groups=collections.defaultdict(list)
    for n,h in enumerate(hits):groups[h[0]].append(n)
    for b,pos in groups.items():
        i=[hits[n][1] for n in pos];j=[hits[n][2] for n in pos]
        with np.errstate(all='ignore'):
            if b.startswith('T1'):v=G.B.IK[b[3:]](basis('A',i),basis('A',j))
            elif b=='T2p':v=basis('A',i)+basis('A',j)
            elif b=='T2m':v=basis('A',i)-basis('A',j)
            elif b.startswith('T3'):
                _,k,op=b.split('|');x,y=basis('D',i),basis('D',j)
                if op=='+':prod=x+y
                elif op=='*':prod=x*y
                elif op=='-':prod=x-y
                elif op=='/':prod=x/y
                else:raise RuntimeError('Unknown operator '+op)
                v=G.B.IK[k](T['gb'],T['a0'])*prod
            elif b=='T4':v=basis('A0',i)*basis('D',j)
            elif b.startswith('T5m'):v=G.B.IK[b[4:]](T['gb'],T['a0'])*(1+KG[i,None]*basis('D',j))
            elif b.startswith('T5a'):v=G.B.IK[b[4:]](T['gb'],T['a0'])+KG[i,None]*basis('A',j)
            else:raise RuntimeError('Unknown template '+b)
        result[pos]=v
    return result,groups
if args.verify_templates:
    fixtures=[]
    for fn in G.B.IK:
        fixtures.append(['T1|'+fn,0,1,1])
        for op in ['+','-','*','/']:fixtures.append(['T3|'+fn+'|'+op,0,1,1])
        fixtures.extend([['T5m|'+fn,40,1,1],['T5a|'+fn,40,1,1]])
    fixtures.extend([['T2p',0,1,1],['T2m',0,1,1],['T4',0,1,1]])
    values,_=predictions(fixtures);checks=[]
    for i,h in enumerate(fixtures):
        with np.errstate(all='ignore'):direct=G.B.ev(formula(h),T)
        ok=np.allclose(values[i],direct,rtol=1e-12,atol=0,equal_nan=True)
        checks.append(dict(template=h[0],passed=bool(ok)))
    G.atomic(OUT/'template_checks.json',dict(identity=identity,checks=checks))
    print('template checks',sum(c['passed'] for c in checks),'/',len(checks));db.close()
    raise SystemExit(int(not all(c['passed'] for c in checks)))
blocks=[G.Shape(T,C) for C in [G.CINT,*G.LOO,np.zeros((5,5))]]
var=T['se']**2+T['sm']**2;extra=np.tile(np.diag(G.CINT),4);df=nr-1;den=math.sqrt(2*df)
def qscore(d,shape):
    mu=d@shape.weights/shape.den;r=d-mu[:,None]
    return np.einsum('bi,ij,bj->b',r,shape.W,r,optimize=False)
def scores(d):
    mean=d.mean(1);rms=np.sqrt((d*d).mean(1));cm=d.reshape(-1,4,5).mean(2)
    zm=mean/np.hypot(cm.std(axis=1,ddof=1)/2,.12)
    zold=(((d-mean[:,None])**2/var).sum(1)-df)/den
    zdiag=(((d-mean[:,None])**2/(var+extra)).sum(1)-df)/den
    z=[(qscore(d,b)-df)/den for b in blocks];passed=[(abs(zm)<=2)&(zz<=2) for zz in z]
    stable=np.all(np.stack([a==passed[0] for a in passed[1:5]]),axis=0)
    return dict(line=(abs(mean)<=.05)&(rms<=.10),legacy=(abs(zm)<=2)&(zold<=2),diagonal=(abs(zm)<=2)&(zdiag<=2),
                accepted=passed[0],stable=stable,mutated=passed[5],Zold=zold,Zdiag=zdiag,Zcov=z[0],Zmut=z[5])
def accumulate(c,s,mut=False):
    n=len(s['line']);accept=s['mutated'] if mut else s['accepted'];stable=np.ones(n,bool) if mut else s['stable']
    c['valid']+=n;c['line']+=int(s['line'].sum());c['legacy_err']+=int(s['legacy'].sum())
    c['diagonal_err']+=int((s['legacy'] if mut else s['diagonal']).sum());c['covariance_err']+=int(accept.sum())
    c['stable_covariance_err']+=int((accept&stable).sum());c['unstable']+=int((~stable).sum());c['mutation_changes']+=int(np.count_nonzero(s['accepted']!=s['mutated']))
    for label,v in [('Z_cov',s['Zmut'] if mut else s['Zcov']),('Z_legacy',s['Zold']),('Z_diagonal',s['Zold'] if mut else s['Zdiag'])]:
        if n:
            for direction,fn in [('min',min),('max',max)]:
                k=direction+'_'+label;value=float(np.min(v) if direction=='min' else np.max(v));c[k]=value if c[k] is None else fn(c[k],value)
chunks=0
with (W/'hits.jsonl').open('rb') as f:
    f.seek(state['offset'])
    while not stop and (not args.max_chunks or chunks<args.max_chunks):
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if platform.system()=='Darwin' else 1024)
        if not os.environ.get('HEAVYQ_JOB_ID') and (rss>950_000_000 or (args.light_budget_seconds and time.time()-start>=args.light_budget_seconds)):
            state['queue_required']=True;break
        lines=[]
        for _ in range(args.chunk):
            line=f.readline()
            if not line:break
            lines.append(line)
        if not lines:state['complete']=True;break
        hits=[json.loads(line) for line in lines];pred,groups=predictions(hits);valid=np.all(np.isfinite(pred)&(pred>0),axis=1)
        indices=np.flatnonzero(valid);d=np.log10(T['go']/pred[valid]);s=scores(d)
        # Every template in every chunk gets an independent expanded-expression check.
        for positions in groups.values():
            ii=next((i for i in positions if valid[i]),None)
            if ii is None:continue
            ftext=formula(hits[ii]);direct=G.B.ev(ftext,T)
            if not np.allclose(pred[ii],direct,rtol=1e-12,atol=0):raise RuntimeError('Template decoding mismatch')
            jj=int(np.searchsorted(indices,ii));scalar=G.evaluate(ftext,T)
            err=abs(float(s['Zcov'][jj])-scalar['covariance']['Z_cov'])
            if not math.isclose(float(s['Zcov'][jj]),scalar['covariance']['Z_cov'],rel_tol=1e-10,abs_tol=1e-10):raise RuntimeError('Vector/scalar shape mismatch')
            if bool(s['accepted'][jj])!=scalar['conditional_err'] or bool(s['stable'][jj])!=scalar['stable']:raise RuntimeError('Vector/scalar flag mismatch')
            state['checks']+=1;state['max_scalar_error']=max(state['max_scalar_error'],err)
        for tree in ['main','mutate']:state[tree]['invalid']+=int((~valid).sum())
        accumulate(state['main'],s);accumulate(state['mutate'],s,True)
        for j,i in enumerate(indices):
            digest=hashlib.sha256(formula(hits[i]).encode()).digest()
            db.execute('INSERT OR IGNORE INTO formula VALUES (?,?,?,?)',(digest,int(s['accepted'][j]),int(s['accepted'][j] and s['stable'][j]),int(s['mutated'][j])))
        state['offset']=f.tell();state['rows']+=len(hits);chunks+=1
        db.execute('INSERT OR REPLACE INTO state VALUES (1,?)',(json.dumps(state),));db.commit()
if state['offset']==(W/'hits.jsonl').stat().st_size:state['complete']=True
db.execute('INSERT OR REPLACE INTO state VALUES (1,?)',(json.dumps(state),));db.commit()
unique=db.execute('SELECT count(*),coalesce(sum(accepted),0),coalesce(sum(stable),0),coalesce(sum(mutated),0) FROM formula').fetchone();db.close()
for tree in ['main','mutate']:
    science=dict(status='complete retained-hit census' if state['complete'] else 'INCOMPLETE PREFIX ONLY',rows=state['rows'],statistics=state[tree],
                 unique_valid_formulas=unique[0],unique_covariance_err=unique[3] if tree=='mutate' else unique[1],
                 unique_stable_covariance_err=unique[3] if tree=='mutate' else unique[2],checks=state['checks'],max_scalar_error=state['max_scalar_error'],
                 scope='Conditional G3 bookkeeping; not full grammar census or calibrated p-value; kappa = 1/2 FITTED; not theory closed')
    G.atomic(OUT/tree/'result.json',dict(scientific=science,identity=identity))
G.atomic(OUT/'runtime.json',dict(seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,new_chunks=chunks))
print(json.dumps(dict(rows=state['rows'],complete=state['complete'],new_chunks=chunks,seconds=time.time()-start,unique=unique)),flush=True)
raise SystemExit(0 if state['complete'] else 75)
