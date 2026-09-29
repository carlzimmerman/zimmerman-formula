"""POST-HOC attack diagnostics (declared as such): leave-out sensitivity, corrected-key SLUGGS-mass law, gamma x rule, using the lane's-equivalent config
(nu_RAR everywhere, M_JAM ~ D), which reproduces CFG55 to 2e-6."""
import json, math, numpy as np, os, io, contextlib
src=open('cfg76_sluggs_jam.py').read(); src=src[:src.index('ALL = {}')]
os.environ['MUTATE']='0'
g={'__file__':os.path.abspath('cfg76_sluggs_jam.py'),'__name__':'x'}
with contextlib.redirect_stdout(io.StringIO()): exec(compile(src,'cfg76','exec'),g)
run=g['run']; summ=g['summ']; fmt=g['fmt']; SEL=g['SEL']; BINS=g['BINS']; BINSC=g['BINS_c']
r=run(SEL,'nu_rar','canonical',dist_mode='dyn')
law=np.array([r['law'][n] for n in SEL]); rule=np.array([r['rule'][n] for n in SEL])
def z(a): return a.mean()/(a.std(ddof=1)/math.sqrt(len(a)))
print("full: law %.3f (%.2fs) rule %.3f (%.2fs)"%(law.mean(),z(law),rule.mean(),z(rule)))
jl=[np.delete(law,i).mean() for i in range(16)]; jr=[np.delete(rule,i).mean() for i in range(16)]
print("leave-one-out law range %.3f..%.3f (worst removal NGC%d); rule %.3f..%.3f"%(min(jl),max(jl),SEL[int(np.argmin(jl))],min(jr),max(jr)))
cen=[4365,4374,4486,5846]; keep=[i for i,n in enumerate(SEL) if n not in cen]
print("without M87,4365,4374,5846 (N=12): law %.3f (%.2fs); rule %.3f (%.2fs)"%(law[keep].mean(),z(law[keep]),rule[keep].mean(),z(rule[keep])))
lo=[i for i,n in enumerate(SEL) if BINS[n]['lMs']<11.2]; hi=[i for i,n in enumerate(SEL) if BINS[n]['lMs']>=11.2]
print("SLUGGS logM*<11.2 (N=%d): law %.3f rule %.3f ; >=11.2 (N=%d): law %.3f rule %.3f"%(len(lo),law[lo].mean(),rule[lo].mean(),len(hi),law[hi].mean(),rule[hi].mean()))
# corrected key, SLUGGS masses (law), all galaxies
allc=sorted(BINSC); rc=run(allc,'nu_rar','canonical',sluggs_mass=True,bins=BINSC)
a=np.array([rc['law'][n] for n in allc]); print("corrected-key SLUGGS-mass law, N=%d: %.3f +- %.3f; NGC720: %s NGC821: %s"%(len(a),a.mean(),a.std(ddof=1)/math.sqrt(len(a)),rc['law'].get(720),rc['law'].get(821)))
# gamma scan with rule and both footings
for gam in (2.0,2.4,3.0,3.6):
    for f in ('canonical','alt'):
        rr=run(SEL,'nu_rar',f,dist_mode='dyn',gamma=gam); s=summ(rr); print("gamma %.1f %s: %s"%(gam,f,fmt(s)))
# what gamma zeroes the law / rule offset?
from scipy.optimize import brentq
for kind in ('law','rule'):
    fz=lambda gm: summ(run(SEL,'nu_rar','canonical',dist_mode='dyn',gamma=gm))[kind][0]
    try: print(kind,'offset = 0 at gamma =',brentq(fz,1.5,3.0))
    except Exception as e: print(kind,'no zero in [1.5,3.0]',e)
# bin-error-weighted? (not available: statistic is unweighted) report per-galaxy scatter
print("per-galaxy scatter law %.3f rule %.3f"%(law.std(ddof=1),rule.std(ddof=1)))
