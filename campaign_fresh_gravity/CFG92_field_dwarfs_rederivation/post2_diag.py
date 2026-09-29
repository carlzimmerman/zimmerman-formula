"""POST-RUN diagnostics (written AFTER reading CFG58's .out; label: post-hoc; changes no frozen number).  Tests the four candidate causes of the small differences
against CFG58's printed numbers: (i) np.std ddof=0 instead of ddof=1 in the analytic median error; (ii) Upsilon floor from the endpoints {1,4} only; (iii) Omega_m = 0.3134 (hunt_lib) in the edge;
(iv) rounded a0 pair 9.36e-11/1.13e-10."""
import numpy as np, math, importlib.util, sys
spec=importlib.util.spec_from_file_location('c','cfg92.py'); c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
ALL=c.load(); F=[s for s in ALL if s['pop']=='field']; base=c.Cfg()
def fd(ddof, ups_set, tag):
    res=[]
    for foot in ('canonical','alt'):
        def row(cfg, coll):
            x=c.offs(F,cfg); m=float(np.median(x)); stat=1.2533*float(np.std(x,ddof=ddof))/math.sqrt(len(x))
            ms=[float(np.median(c.offs(F,cfg.copy(ups=u)))) for u in ups_set]; fU=0.5*(max(ms)-min(ms)); fC=0
            if coll and cfg.phi!=0:
                mc=[float(np.median(c.offs(F,cfg.copy(small_mcoll=v)))) for v in (1e8,1e9,1e10)]; fC=0.5*(max(mc)-min(mc))
            return m, math.sqrt(stat**2+fU**2+fC**2), stat, fU
        mL,eL,sL,uL=row(base.copy(phi=0.0,foot=foot),False); mS,eS,sS,uS=row(base.copy(phi=1.0,foot=foot),True)
        res.append(f"{foot}: L {mL:+.4f}/{eL:.4f}={mL/eL:+.2f}s S {mS:+.4f}/{eS:.4f}={mS/eS:+.2f}s (Sstat {sS:.4f} U {uS:.4f}) S|Lerr {mS/eL:+.2f}s")
    print(f"{tag:46s}", " || ".join(res))
fd(1,(1,2,4),"frozen (ddof=1, ups {1,2,4})")
fd(0,(1,2,4),"post-hoc (i) ddof=0")
fd(0,(1,4),"post-hoc (i)+(ii) ddof=0, ups endpoints")
c.OMEGA_M=0.14237/0.674**2; c.RHO_M=c.OMEGA_M*c.RHO_C; c._EP.clear()
for ratio in (0.5,1.0):
    print('post-hoc (iii) Omega_m=%.4f'%c.OMEGA_M, ratio, {f:'%.3e'%c.switchoff(ratio,base,f)[0] for f in ('canonical','alt')})
c.OMEGA_M=0.3153; c.RHO_M=c.OMEGA_M*c.RHO_C; c._EP.clear()
fd(0,(1,4),"back to 0.3153")
c.A0={'canonical':9.36e-11,'alt':1.13e-10}; c._EP.clear()
fd(0,(1,4),"post-hoc (iv) rounded a0, ddof=0, ups endpoints")
print('switch rounded a0', {f:'%.3e'%c.switchoff(0.5,base,f)[0] for f in ('canonical','alt')})
