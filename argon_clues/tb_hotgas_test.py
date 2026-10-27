import json, re, itertools, numpy as np
from scipy.stats import rankdata, spearmanr
cls={}
for ln in open('../_external_data/atlas3d_emsellem11/tableb1.tsv'):
    if ln.startswith('#') or not ln.strip(): continue
    p=ln.rstrip('\n').split('\t')
    if len(p)>11 and p[1].strip().startswith('NGC'): cls[int(re.sub(r'\D','',p[1]))]=p[10].strip()
fz={}
rows=[l.rstrip('\n').split('\t') for l in open('../real_research/data/cfg57_gas_sources/fukazawa2006_table4.tsv',encoding='latin-1') if l.strip() and not l.startswith('#')]
h=rows[0]
for r in rows[1:]: fz[r[0]]=dict(zip(h,r))
gal=[3377,3607,4365,4374,4494,4649,4697,5846]
per=json.load(open('../campaign_fresh_gravity/CFG330_sluggs_icgc_clip/cfg330_icgc_K0_results.json'))['per_galaxy']
for foot in ('nu_mono|canonical','nu_mono|alt'):
    off=np.array([per[foot][str(n)]['off'] for n in gal])
    ne=np.array([float(fz['NGC%d'%n]['ne10_1e-3cm3']) if fz['NGC%d'%n]['ne10_1e-3cm3']!='nan' else -1.0 for n in gal])   # VCXG ranked lowest (tied)
    slow=np.array([cls[n]=='S' for n in gal],float)
    rk=rankdata(ne)
    rho,_=spearmanr(rk,off)
    # exact one-sided permutation over all 8! orderings of offsets
    cnt=0; tot=0
    for perm in itertools.permutations(range(8)):
        r2,_=spearmanr(rk,off[list(perm)]); tot+=1; cnt+= r2>=rho-1e-12
    p=cnt/tot
    X=np.c_[np.ones(8),slow,rk-rk.mean()]; beta=np.linalg.lstsq(X,off,rcond=None)[0]; res=off-X@beta; s2=res@res/(8-3); se=np.sqrt(np.diag(s2*np.linalg.inv(X.T@X)))
    print('== %s'%foot)
    print('  galaxies, ne10(1e-3 cm^-3), class, offset:'); 
    for n,a,c,o in zip(gal,ne,[cls[n] for n in gal],off): print('    NGC%-5d ne10 %5s  %s  off %+.3f'%(n,'VCXG' if a<0 else '%.2f'%a,c,o))
    print('  Spearman(off, rank ne10) = %+.2f, exact one-sided p = %.3f (n=8)'%(rho,p))
    print('  OLS off ~ slow + rank(ne10): slow coef %+.3f +- %.3f ; gas-rank coef %+.4f +- %.4f (per rank)'%(beta[1],se[1],beta[2],se[2]))
    # mutation: shuffle gas ranks among galaxies -> rho distribution
    rng=np.random.default_rng(1); m=[spearmanr(rng.permutation(rk),off)[0] for _ in range(5000)]
    print('  MUTATION (gas ranks shuffled): rho mean %+.2f sd %.2f'%(np.mean(m),np.std(m)))
