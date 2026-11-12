# Reads calibration-side content of the DESI DR2 III figure-data zip. Deliberately does NOT print the
# real-Milky-Way per-method values (fig10) or literature mass values (fig13), so a graded lane can freeze first.
import zipfile,sys,io,csv,math,collections
z=zipfile.ZipFile(sys.argv[1]); P='desi-dr2-mw-mass-figdata/'
def rd(name): return list(csv.DictReader(io.TextIOWrapper(z.open(P+name),encoding='utf-8')))
# (README bodies are not echoed; they describe the columns and carry the authors' contact lines.)
print('===== mock truths (figA1): true M(<r) of the six Auriga haloes')
t=rd('figA1/truths.csv'); H=collections.defaultdict(list)
for r in t: H[r['halo']].append((float(r['r_kpc']),float(r['Menc'])))
def interp(pts,x):
    pts=sorted(pts)
    for (a,ma),(b,mb) in zip(pts,pts[1:]):
        if a<=x<=b: 
            f=(math.log(x)-math.log(a))/(math.log(b)-math.log(a)); return math.exp(math.log(ma)+f*(math.log(mb)-math.log(ma)))
    return float('nan')
print('halo   r-range        M20   M50   M80 [1e11]   slope20-50  slope50-80')
for h,pts in sorted(H.items()):
    sc=1e11 if max(m for _,m in pts)>1e6 else 1.0   # file is already in 1e11 Msun
    m20,m50,m80=[interp(pts,x)/sc for x in (20,50,80)]
    print(f"{h:6s} {min(p[0] for p in pts):5.1f}-{max(p[0] for p in pts):6.1f}  {m20:5.2f} {m50:5.2f} {m80:5.2f}     {math.log(m50/m20)/math.log(2.5):.3f}       {math.log(m80/m50)/math.log(1.6):.3f}")
print('===== fig08 summary: mock bias per method (median, 16-84) at selected radii')
s=rd('fig08/summary.csv'); print('quantities:',sorted(set(r['quantity'] for r in s)),'methods:',sorted(set(r['method'] for r in s)))
for r in s:
    try: rk=float(r['r_kpc'])
    except: rk=None
    if rk in (20.0,30.0,50.0,65.0,80.0) or rk is None or r['r_kpc'] in ('','nan'):
        print(' ',r['quantity'],r['method'],r['tracer'],r['r_kpc'],r['0.16'][:7],r['0.5'][:7],r['0.84'][:7])
print('===== fig09 residual correlation matrix at 80 kpc')
print(z.read(P+'fig09/corr-menc-80.0.csv').decode()[:1500])
print('===== fig04 GME posterior summaries (real data): columns Phi0,gamma,alpha,beta per README')
for tr in ('rrl','bhb'):
    rows=[l for l in z.read(P+f'fig04/gme-posteriors-{tr}.csv').decode().splitlines() if l and not l.startswith('#')]
    cols=list(zip(*[[float(x) for x in l.split(',')] for l in rows]))
    def pct(v,q): v=sorted(v); return v[int(q*(len(v)-1))]
    print(tr,len(rows),'draws; medians(16,84):',' | '.join(f"{pct(c,.5):.3f} ({pct(c,.16):.3f},{pct(c,.84):.3f})" for c in cols))
    g=cols[1]; p0=cols[0]; n=len(g); mg=sum(g)/n; mp=sum(p0)/n
    cov=sum((a-mp)*(b-mg) for a,b in zip(p0,g))/n; sg=(sum((b-mg)**2 for b in g)/n)**.5; sp=(sum((a-mp)**2 for a in p0)/n)**.5
    print('   corr(Phi0,gamma)=%.3f; sd(gamma)=%.4f (prior sd 0.0458, prior mean 0.440); sd(Phi0)=%.2f (prior sd 6.90, mean 64.63)'%(cov/sg/sp,sg,sp))
print('===== fig13 literature compilation: counts only (no values printed)')
for f,col in (('fig13/literature-halo-stars.csv','halo_stars_tracer'),('fig13/literature-other-tracers.csv','tracer')):
    L=rd(f); c=collections.Counter()
    for r in L:
        rk=float(r['r_kpc']); band='<=80' if rk<=80 else ('80-100' if rk<=100 else ('100-150' if rk<=150 else '>150'))
        c[(r[col],band)]+=1
    print(f,len(L),'rows:',dict(sorted(c.items())))
print('===== fig10 real-MW per-method file: structure only')
L=rd('fig10/desi-dr2-menc.csv'); c=collections.defaultdict(list)
for r in L: c[(r['method'],r['tracer'])].append(float(r['r_kpc']))
for k,v in sorted(c.items()): print(' ',k,len(v),'radii',min(v),'-',max(v),'kpc')
