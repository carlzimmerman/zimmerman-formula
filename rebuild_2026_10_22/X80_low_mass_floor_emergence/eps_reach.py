#!/usr/bin/env python3
"""X80 post-result note on 1e12 only, no low-mass number: would a smaller softening test the converged eta? On the committed ng 64 snapshots, X48's r_conv recomputed with eps/2 and eps/4, and the cusp eta at that cut. Rough: the snapshots were evolved at eps. kappa = 1/2 FITTED; not theory closed."""
import json, math, os, sys, glob
RB=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
X81P=os.path.join(RB,"X81_core_convergence","x80_core_convergence.py"); sys.argv=[X81P]
src=open(X81P).read(); src=src[:src.index("# K1: exact smooth core")]; NS=dict(__file__=X81P,__name__="x81_prefix"); exec(compile(src,X81P,"exec"),NS)
import numpy as np
XA,fit,a_fit,M_nfw,eta_of=NS["XA"],NS["fit"],NS["a_fit_profile"],NS["M_nfw"],NS["eta_of"]
rows=[]
for s in range(1,10):
    d=os.path.join(RB,"X48_native_cf_zoom","runs",f"M1e12_s{s}_ng64"); Z=np.load(os.path.join(d,"snap_zf.npz")); x,m=Z["x"],float(Z["m"]); meta=json.loads(str(Z["meta"])); rho=meta["Mf"]/(4/3*math.pi*meta["qM"]**3)*(1+meta["zf"])**3
    e=meta["eps"]; o=XA.measure(x,m,rho,e); o2=XA.measure(x,m,rho,e/2); o4=XA.measure(x,m,rho,e/4)
    c=o.get("c_nfw_fit"); rv=o["rvir"]
    rows.append(dict(s=s,xc=o["rconv"]/rv,x3e=3*e/rv,xc2=o2["rconv"]/rv,xc4=o4["rconv"]/rv,c=c,eta_cut=float(eta_of(a_fit(M_nfw(c),o["rconv"]/rv))),eta_c2=float(eta_of(a_fit(M_nfw(c),o2["rconv"]/rv))),eta_c4=float(eta_of(a_fit(M_nfw(c),o4["rconv"]/rv))),eta_0=float(eta_of(a_fit(M_nfw(c),0.001)))))
    r=rows[-1]; print("s%d xc %.4f (3eps %.4f) -> eps/2 %.4f, eps/4 %.4f | c %.2f | cusp eta at cut %.2f, eps/2 %.2f, eps/4 %.2f, converged %.2f"%(s,r["xc"],r["x3e"],r["xc2"],r["xc4"],r["c"],r["eta_cut"],r["eta_c2"],r["eta_c4"],r["eta_0"]))
med=lambda k: float(np.median([r[k] for r in rows]))
print("median xc %.4f, eps/2 %.4f, eps/4 %.4f; cusp eta %.2f, %.2f, %.2f; converged %.2f"%(med("xc"),med("xc2"),med("xc4"),med("eta_cut"),med("eta_c2"),med("eta_c4"),med("eta_0")))
print("expected rise eps/2: %.1f%%, eps/4: %.1f%%"%(100*(med("eta_c2")/med("eta_cut")-1),100*(med("eta_c4")/med("eta_cut")-1)))
