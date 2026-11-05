#!/usr/bin/env python3
"""AZ31: new graded-radius W2 run, with per-solve checkpoints."""
import argparse
import hashlib
import json
import math
import multiprocessing as mp
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time

sys.dont_write_bytecode = True
for key in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','VECLIB_MAXIMUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[key]='1'
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
sys.path.insert(0,str(ROOT/'rebuild_2026_10_22/V3X_v3s_close_undecided'))
import numpy as np
import scipy
import v3x_solver as V

AP=argparse.ArgumentParser()
AP.add_argument('--mutate',action='store_true')
AP.add_argument('--resume',action='store_true')
AP.add_argument('--max-tasks',type=int)
args=AP.parse_args()
MODE='mutate' if args.mutate else 'main'
OUT=HERE/MODE
OUT.mkdir(exist_ok=True)
STOP=[]
signal.signal(signal.SIGTERM,lambda s,f: STOP.append(s))
signal.signal(signal.SIGINT,lambda s,f: STOP.append(s))

def atomic(path,obj):
    tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w') as f:
        json.dump(obj,f,indent=2,allow_nan=False); f.write('\n'); f.flush(); os.fsync(f.fileno())
    os.replace(tmp,path)

FILES=[
 'astra_goal_2026_11_05/AZ31_w2_graded_radius/FROZEN_CRITERIA.md',
 'astra_goal_2026_11_05/AZ31_w2_graded_radius/run.py',
 'rebuild_2026_10_22/V3X_v3s_close_undecided/v3x_solver.py',
 'covariant_push_2026_10_22/C6_literal_cassini/c6_solver.py',
 'doors_push_2026_10_22/D7d_screened_q2/d7d_solver.py',
 'doors_push_2026_10_22/D7b_cassini_Q2/d7b_cassini_q2_results.json',
 'rebuild_2026_10_22/V3W_v3s_weak_spots/w2_c6_rerun.json']
HASH={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in FILES}
FINGERPRINT=hashlib.sha256(json.dumps(HASH,sort_keys=True).encode()).hexdigest()
PROVENANCE=dict(inputs=HASH,mode=MODE,source_fingerprint=FINGERPRINT,
 commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
 software=dict(python=sys.version.split()[0],numpy=np.__version__,scipy=scipy.__version__),
 numerical_policy='single thread; child RSS watchdog 0.85e9 bytes; checkpoint every solve')
atomic(OUT/'provenance.json',PROVENANCE)
def read(rel): return json.loads((ROOT/rel).read_text())
GEJ=read(FILES[-2]); KNOWN=read(FILES[-1])
GM=1.32712440018e20; PC=3.0857e16; RSAT=9.58*1.495978707e11
FOOT={'canonical':9.3603e-11,'alt':1.1312e-10}
LADDER=[(40,64),(50,80),(60,96),(70,112)]

def worker(lam,xe,a0,grid,method,mu,conn):
    signal.signal(signal.SIGTERM,signal.SIG_DFL)
    signal.signal(signal.SIGINT,signal.SIG_DFL)
    try:
        g=V.grid(lam,grid)
        U,res,it=V.solve_v(g,lam,xe,method=method,permc='COLAMD',mu=mu,polish=3)
        rm=math.sqrt(GM/a0)
        q=[float(-V.S.q2_raw(g,U[0],r*RSAT/rm)*a0/rm) for r in (1,10,100)]
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*(1 if sys.platform=='darwin' else 1024)
        conn.send(dict(ok=True,Q2=q,residual=float(res),iterations=int(it),rss_bytes=float(rss),N=int(g.N)))
    except Exception as ex:
        conn.send(dict(ok=False,error=f'{type(ex).__name__}: {ex}'))
    finally: conn.close()

def solve(foot,grid,method='A',mu=1e-12):
    key=f'{foot}_{grid[0]}_{grid[1]}_{method}_{mu:.0e}'
    path=OUT/(key+'.json')
    if path.exists():
        if not args.resume: raise RuntimeError('Existing checkpoint requires --resume')
        rec=json.loads(path.read_text())
        if rec['source_fingerprint']!=FINGERPRINT: raise RuntimeError('Input hashes changed; do not reuse checkpoint')
        print('RESUME',key,flush=True); return rec
    a0=FOOT[foot]; xe=GEJ['grid'][foot]['none']['E2']['ge_total']/a0
    lam=0 if args.mutate else 24*PC/math.sqrt(GM/a0)
    ctx=mp.get_context('fork'); a,b=ctx.Pipe(False)
    child=ctx.Process(target=worker,args=(lam,xe,a0,grid,method,mu,b))
    start=time.monotonic(); child.start(); b.close(); peak=0; failure=None
    while child.is_alive():
        if a.poll(.2): break
        if STOP:
            child.terminate(); child.join(); raise InterruptedError('yield requested; completed rungs retained')
        proc=subprocess.run(['ps','-o','rss=','-p',str(child.pid)],text=True,capture_output=True)
        if proc.returncode != 0 and child.is_alive():
            failure='RSS monitor unavailable'; child.terminate(); break
        try: rss=float(proc.stdout.strip() or 0)*1024
        except ValueError: rss=0
        peak=max(peak,rss)
        if rss>0.85e9:
            failure='RSS watchdog exceeded'; child.kill(); break
    rec=a.recv() if failure is None and a.poll(5) else dict(ok=False,error=failure or 'no child result')
    child.join(); rec.update(seconds=time.monotonic()-start,source_fingerprint=FINGERPRINT,footing=foot,grid=list(grid),method=method,shift=mu)
    rec['rss_bytes']=max(peak,rec.get('rss_bytes',0))
    atomic(path,rec)
    print('SOLVE',key,json.dumps(rec),flush=True)
    return rec

def order(q,n):
    d1=abs(q[1]-q[0]); d2=abs(q[2]-q[1]); h=[1/x for x in n]
    fn=lambda p:(h[1]**p-h[2]**p)/(h[0]**p-h[1]**p)-d2/d1
    lo,hi=.05,12.
    if d1==0 or fn(lo)*fn(hi)>0: return None
    for _ in range(200):
        mid=(lo+hi)/2
        if fn(lo)*fn(mid)<=0: hi=mid
        else: lo=mid
    return (lo+hi)/2

results={}; ntask=0
try:
    for foot,a0 in FOOT.items():
        tasks=[(g,'A',1e-12) for g in (LADDER if args.mutate else [(30,48)]+LADDER)]
        if not args.mutate: tasks += [((30,48),'B',1e-12),((40,64),'B',1e-12),((70,112),'A',1e-10)]
        records={}
        for g,method,mu in tasks:
            if STOP: raise InterruptedError('yield requested')
            records[(g,method,mu)]=solve(foot,g,method,mu); ntask+=1
            if args.max_tasks and ntask>=args.max_tasks: raise InterruptedError('requested checkpoint stop')
        checks={}; margins={}
        checks['all_solves']=all(r['ok'] for r in records.values())
        checks['RSS_below_1GB']=max(r['rss_bytes'] for r in records.values())<1e9
        if checks['all_solves']:
            vals={g:records[(g,'A',1e-12)]['Q2'][2] for g in (LADDER if args.mutate else [(30,48)]+LADDER)}
            q=[vals[g] for g in LADDER[1:]]; p=order(q,[50,60,70]); rich=q[2]+(q[2]-q[1])/((70/60)**2-1)
            xe=GEJ['grid'][foot]['none']['E2']['ge_total']/a0
            routeF=float(V.C.routeF_Q2(GM,24*PC,xe,0.0))
            margins.update(Q2_by_rung={str(g):v for g,v in vals.items()},richardson=rich,rich_vs_finest=rich/q[2]-1,observed_order=p,N_over_F=rich/routeF,routeF=routeF,
                           step50_60=abs(q[1]-q[0]),step60_70=abs(q[2]-q[1]),finest_Q2=q[2])
            checks.update(residuals=all(r['residual']<1e-9 for r in records.values()),
                          shrinking=abs(q[2]-q[1])<abs(q[1]-q[0]),richardson=abs(rich/q[2]-1)<.02,
                          observed_order=p is not None and 1.5<=p<=2.5,
                          routeF=rich*routeF>0 and abs(rich/routeF-1)<.05,physical_band=abs(q[2])<=9e-27)
            if not args.mutate:
                v3=KNOWN['C6prime'][f'{foot}|L24pc']['Q_by_rung_by_radius']
                k1=max(abs(vals[g]/ref[2]-1) for g,ref in zip([(30,48),(40,64)],v3[1:]))
                k2=max(abs(records[(g,'B',1e-12)]['Q2'][2]/vals[g]-1) for g in [(30,48),(40,64)])
                k3=abs(records[((70,112),'A',1e-10)]['Q2'][2]/vals[(70,112)]-1)
                margins.update(K1=k1,K2=k2,K3=k3); checks.update(K1=k1<=1e-6,K2=k2<=1e-6,K3=k3<=1e-6)
            numerical=all(checks.get(k,False) for k in ['all_solves','RSS_below_1GB','residuals','shrinking','richardson','observed_order'])
            label='PASS' if all(checks.values()) else ('FAIL' if numerical and (not checks['routeF'] or not checks['physical_band']) else 'UNDECIDED')
        else: label='NOT EVALUABLE'
        results[foot]=dict(label=label,checks=checks,margins=margins)
        atomic(OUT/'partial_results.json',results)
        print('FOOTING',foot,json.dumps(results[foot]),flush=True)
except InterruptedError as ex:
    print(str(ex),flush=True); sys.exit(75)

after={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in FILES}
stable=after==HASH
result=dict(lane='AZ31',mode=MODE,footings=results,inputs_unchanged=stable,source_fingerprint=FINGERPRINT,
            scope='W2 graded-radius numerical closure only; no other V3W gate promoted',statement='kappa = 1/2 FITTED; not theory closed')
atomic(OUT/'results.json',result)
passed=stable and all(r['label']=='PASS' for r in results.values())
print('FINAL',json.dumps(result),flush=True)
sys.exit(0 if passed else 1)
