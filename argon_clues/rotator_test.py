import json, re, numpy as np
rng=np.random.default_rng(20261014)
cls={}
for ln in open('../_external_data/atlas3d_emsellem11/tableb1.tsv'):
    if ln.startswith('#') or not ln.strip(): continue
    p=ln.rstrip('\n').split('\t')
    if len(p)>11 and p[1].strip().startswith('NGC'):
        cls[int(re.sub(r'\D','',p[1]))]=(p[11].strip() or p[10].strip(), p[10].strip(), p[11].strip())
d=json.load(open('../campaign_fresh_gravity/CFG330_sluggs_icgc_clip/cfg330_icgc_K0_results.json'))['per_galaxy']
for foot in ('nu_mono|canonical','nu_mono|alt'):
    g=d[foot]; names=sorted(g,key=int)
    rows=[(int(n),g[n]['off'],g[n]['lMjamlaw'],cls[int(n)]) for n in names if int(n) in cls]
    miss=[n for n in names if int(n) not in cls]
    print('== %s: %d matched, missing %s'%(foot,len(rows),miss))
    for use,idx in (('F/S (epsilon_e criterion)',1),('F/S2 (epsilon_e/2? alt column)',2)):
        S=np.array([r[3][idx]=='S' for r in rows]); off=np.array([r[1] for r in rows]); M=np.array([r[2] for r in rows])
        print(' %s: slow %s'%(use,[r[0] for r in rows if r[3][idx]=='S']))
        if S.sum()<4 or (~S).sum()<6: print('   NOT DIAGNOSTIC (n_slow=%d n_fast=%d)'%(S.sum(),(~S).sum())); continue
        D=off[S].mean()-off[~S].mean()
        perm=[ (lambda s: off[s].mean()-off[~s].mean())(rng.permutation(S)) for _ in range(100000)]
        p=np.mean(np.array(perm)>=D)
        X=np.c_[np.ones_like(M),M-M.mean(),S.astype(float)]; beta,res,rk,sv=np.linalg.lstsq(X,off,rcond=None)
        resid=off-X@beta; s2=resid@resid/(len(off)-3); cov=s2*np.linalg.inv(X.T@X); se=np.sqrt(np.diag(cov))
        # mass matched
        mm=[]
        for i in np.where(S)[0]:
            c=np.where(~S & (np.abs(M-M[i])<0.25))[0]
            if len(c): mm.append(off[i]-off[c].mean())
        print('   n_slow %d n_fast %d ; mean off slow %.3f fast %.3f ; D = %+.3f dex, permutation p = %.4f'%(S.sum(),(~S).sum(),off[S].mean(),off[~S].mean(),D,p))
        print('   mass-controlled slow coefficient %.3f +- %.3f (%.1f sigma); slope vs logM %.3f +- %.3f ; mass-matched slow-minus-fast %.3f (n=%d)'%(beta[2],se[2],beta[2]/se[2],beta[1],se[1],np.mean(mm),len(mm)))
        print('   <logM> slow %.2f fast %.2f'%(M[S].mean(),M[~S].mean()))
        # mutation: shuffle labels within mass terciles
        order=np.argsort(M); Sm=S.copy(); mutD=[]
        for _ in range(2000):
            Sm=S.copy()
            for chunk in np.array_split(order,3): Sm[chunk]=rng.permutation(S[chunk])
            mutD.append(off[Sm].mean()-off[~Sm].mean())
        print('   MUTATION (labels shuffled within mass terciles): mean D %.3f (sd %.3f) -> real D is %.1f sd from it'%(np.mean(mutD),np.std(mutD),(D-np.mean(mutD))/np.std(mutD)))
