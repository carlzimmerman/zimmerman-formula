#!/usr/bin/env python3
"""All archived stage2 near misses, explicitly not the retained-hit census."""
import hashlib,itertools,json,math,time,resource
import g3 as G
import numpy as np
import mpmath as mp
start=time.time();checks=[];records=[];mutrecords=[]
def check(name,passed,value):checks.append(dict(name=name,passed=bool(passed),value=value))
fixture=dict(gid=np.repeat(np.arange(4),5),se=np.full(20,.01),sm=np.zeros(20))
d=np.tile([-.1,-.05,0,.05,.1],4);C=np.eye(5)*.01
sf=G.Shape(fixture,C);sz=G.Shape(fixture,np.zeros((5,5)))
q=sf.score(d);z=sz.score(d)
check('equal_variance_OLS_fixture',abs(q['GLS_intercept']-d.mean())<=1e-12 and abs(q['Q']-float(np.sum(d*d)/.0101))<=1e-10,q)
check('constant_residual_zero_Q',abs(sf.score(np.ones(20)*.123)['Q'])<=1e-12,sf.score(np.ones(20)*.123)['Q'])
check('synthetic_mutation_bites',q['Z_cov']<=2 and z['Z_cov']>2,dict(main=q,mutate=z))
check('covariance_monotonicity_fixture',q['Q']<=z['Q'],dict(main=q['Q'],zero=z['Q']))
files=[];max_anchor=0.;changed=0
for foot,mode,level in itertools.product(G.FOOTS,['real','control'],['L1','L2']):
    path=G.BK/f'bk2_stage2_{level}_{foot}_{mode}.json';files.append(path)
    oldT=G.dataset(foot,mode,True);T=G.dataset(foot,mode)
    archive=json.loads(path.read_text())['rows']
    local_changes=0;newpass=0;stablepass=0;diagpass=0;oldpass=0
    for i,row in enumerate(archive):
        formula=row['F'];v=G.B.ev(formula,oldT);dold=np.log10(oldT['go']/v);anchor=G.legacy(dold,oldT)
        errs={k:abs(anchor[k]-row['X_train'][k]) for k in ['mean','rms','Zm','Zs']}
        ok=all(math.isclose(anchor[k],row['X_train'][k],rel_tol=1e-8,abs_tol=1e-10) for k in errs)
        check(f'archive_{level}_{foot}_{mode}_{i}',ok,errs);max_anchor=max(max_anchor,max(errs.values()))
        main=G.evaluate(formula,T);mut=G.evaluate(formula,T,True)
        record=dict(footing=foot,mode=mode,level=level,index=i,formula=formula,fitted=row['fit'])
        records.append(dict(record,**main));mutrecords.append(dict(record,**mut))
        check(f'zero_cov_legacy_{level}_{foot}_{mode}_{i}',math.isclose(mut['diagonal']['Zs'],main['legacy']['Zs'],rel_tol=1e-8,abs_tol=1e-10),mut['diagonal']['Zs']-main['legacy']['Zs'])
        local_changes+=main['conditional_err']!=mut['conditional_err'];newpass+=main['conditional_err'];stablepass+=main['conditional_err'] and main['stable'];diagpass+=main['diagonal']['err'];oldpass+=main['legacy']['err']
        if i==0:
            v=G.B.ev(formula,T);d=np.log10(T['go']/v);shape=G.Shape(T,G.CINT);q=shape.score(d)
            one=np.ones(len(d));inv=np.linalg.inv(shape.V);mu=float(one@inv@d/(one@inv@one));dense=float((d-mu)@inv@(d-mu))
            check(f'dense_block_{level}_{foot}_{mode}',abs(dense-q['Q'])<=1e-10,abs(dense-q['Q']))
            check(f'monotonic_{level}_{foot}_{mode}',q['Q']<=G.Shape(T,np.zeros((5,5))).score(d)['Q']+1e-10,None)
    changed+=local_changes
    print(json.dumps(dict(level=level,footing=foot,mode=mode,n=len(archive),old_err=oldpass,diagonal_err=diagpass,covariance_err=newpass,stable_covariance_err=stablepass,mutation_changes=local_changes)),flush=True)
# Independent high-precision matrix check for the law and first saved near miss.
for foot in G.FOOTS:
    T=G.dataset(foot,'real');first=next(r['formula'] for r in records if r['footing']==foot and r['mode']=='real')
    for label,formula in [('law','I1(gb,a0)'),('near_miss',first)]:
        d=np.log10(T['go']/G.B.ev(formula,T));shape=G.Shape(T,G.CINT);values=[]
        for prec in [40,80]:
            with mp.workdps(prec):
                V=mp.matrix([[mp.mpf(str(x)) for x in row] for row in shape.V]);dd=mp.matrix([mp.mpf(str(x)) for x in d]);one=mp.matrix([1]*len(d))
                wd=mp.lu_solve(V,dd);w1=mp.lu_solve(V,one);mu=(one.T*wd)[0]/(one.T*w1)[0];rr=dd-mu*one
                values.append(float((rr.T*mp.lu_solve(V,rr))[0]))
        check(f'precision_{foot}_{label}',abs(values[0]-values[1])<=1e-10 and abs(values[1]-shape.score(d)['Q'])<=1e-10,dict(mp40=values[0],mp80=values[1],float_Q=shape.score(d)['Q']))
identity={str(p.relative_to(G.ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files+[G.HERE/'scatter.json',G.HERE/'FROZEN_CRITERIA.md',G.HERE/'AMENDMENTS.md',G.HERE/'g3.py',G.HERE/'pilot.py']}
G.atomic(G.HERE/'main/pilot.json',dict(status='PILOT ONLY; full retained-hit census pending',rows=records,input_hashes=identity))
G.atomic(G.HERE/'mutate/pilot.json',dict(status='ZERO-COVARIANCE MUTATION; pilot only',rows=mutrecords,input_hashes=identity))
G.atomic(G.HERE/'pilot_checks.json',dict(checks=checks,passed=sum(c['passed'] for c in checks),total=len(checks),max_archive_absolute_difference=max_anchor,real_and_control_flags_changed=changed,
                                     scope='Conditional G3 bookkeeping only; no calibrated population p-value; kappa = 1/2 FITTED; not theory closed'))
G.atomic(G.HERE/'pilot_runtime.json',dict(seconds=time.time()-start,peak_rss_native=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
print('checks',sum(c['passed'] for c in checks),'/',len(checks),flush=True)
raise SystemExit(int(not all(c['passed'] for c in checks)))
