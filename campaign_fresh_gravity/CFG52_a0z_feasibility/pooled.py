import runpy, numpy as np, math, io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    ns = runpy.run_path("feas.py")
res = ns["res"]
def pool(label, S):
    if not S: print(label, "none"); return
    Df = np.array([o["can"]["Df"] for o in S]); Dr = np.array([o["can"]["Dr"] for o in S]); sg = np.array([o["can"]["sig"] for o in S])
    so = np.array([o["can"]["s_obs"] for o in S]); sf = np.array([o["can"]["sf"] for o in S])
    w = 1 / sg**2; mf = (w*Df).sum()/w.sum(); mr = (w*Dr).sum()/w.sum()
    si = 1/math.sqrt(w.sum()); sc = math.sqrt(1/np.sum(1/so**2) + (sf.mean()*0.2)**2)
    print(f"{label:52} N={len(S):2d} zmed={np.median([o['z'] for o in S]):.2f} <sep>={np.mean([o['can']['sep'] for o in S]):.3f}  <Df>={mf:+.3f} <Dr>={mr:+.3f}  sig_ind={si:.3f} sig_corr={sc:.3f}  Df {mf/si:+.1f}/{mf/sc:+.1f}s  Dr {mr/si:+.1f}/{mr/sc:+.1f}s  sep/sig_corr={np.mean([o['can']['sep'] for o in S])/sc:.2f}")
for zc in (1.4, 1.5, 2.0):
    S = [o for o in res if o["ds"] in ("RC100","MSA-3D stars+gas","KMOS3D","lensed/CO ledger") and o["z"]>=zc and o["can"]["y"]<1 and o["name"]!="GS4 01529"]
    pool(f"z>={zc}, g_bar<a0, RC100+MSA(gas)+KMOS3D+ledger, excl GS4 01529", S)
    S2 = [o for o in S if o["ds"]=="RC100"]
    pool(f"   RC100 only", S2)
S = [o for o in res if o["ds"] in ("RC100","MSA-3D stars+gas","KMOS3D","lensed/CO ledger","MUSE-DARK II") and o["can"]["y"]<0.3 and o["z"]>=1.0 and o["name"]!="GS4 01529"]
pool("z>=1.0, g_bar<0.3 a0, above + MUSE-DARK II", S)
S = [o for o in res if o["ds"] in ("MUSE-DARK II",) and o["can"]["y"]<0.3 and o["z"]>=1.0]
pool("z>=1.0, g_bar<0.3 a0, MUSE-DARK II only", S)
S = [o for o in res if o["ds"] in ("MUSE-DARK II",) and o["can"]["y"]<0.3]
pool("all z, g_bar<0.3 a0, MUSE-DARK II only", S)
# how many z>=1.5 objects have y<0.3 under point mass bound?
print("z>=1.5 objects with gb_pt/a0<0.3:", [(o['ds'],o['name'],round(o['can']['yp'],2)) for o in res if o['z']>=1.5 and o['can']['yp']<0.3])
print("z>=1.5 objects with gb_disc/a0<0.3:", [(o['ds'],o['name'],round(o['can']['y'],2)) for o in res if o['z']>=1.5 and o['can']['y']<0.3])
# unique galaxies overall with y<1 / <0.3 (primary: RC100, KMOS3D, MSA gas, KROSS gas, MUSE, ledger), no dedupe of RC100/KMOS overlap
prim = ["RC100","KMOS3D","MSA-3D stars+gas","KROSS stars+gas","MUSE-DARK II","lensed/CO ledger"]
for cut in (1.0,0.3):
    print(f"primary sets total gb<{cut} a0:", sum(1 for o in res if o['ds'] in prim and o['can']['y']<cut), "of", sum(1 for o in res if o['ds'] in prim))
print("primary total go<a0:", sum(1 for o in res if o['ds'] in prim and o['can']['yo']<1))
