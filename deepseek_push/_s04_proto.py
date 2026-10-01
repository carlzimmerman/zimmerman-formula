#!/usr/bin/env python3
"""S04 prototype: load the committed HeCS layer + per-cluster v_los gradient."""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import G209_beta_profile as G209

DATA = os.path.join(HERE, "G203_data")

def load_xy():
    c1 = G209.parse_table1(os.path.join(DATA, "table1.dat"))
    g2 = G209.parse_gals(os.path.join(DATA, "table2.dat"), "t2")
    g3 = G209.parse_gals(os.path.join(DATA, "table3.dat"), "t3")
    t4 = G209.parse_table4_tsv(os.path.join(DATA, "hecs2013_table4.tsv"))
    GALS = g2 + g3
    names = list(c1)
    g_ra = np.array([g["ra"] for g in GALS]); g_dec = np.array([g["dec"] for g in GALS])
    c_ra = np.array([c1[n]["ra"] for n in names]); c_dec = np.array([c1[n]["dec"] for n in names])
    c_z = np.array([c1[n]["z"] for n in names])
    rows = []
    for i, g in enumerate(GALS):
        if g["np"] < 1: continue
        sep = G209.angsep(g_ra[i], g_dec[i], c_ra, c_dec)
        j = int(np.argmin(sep)); name = names[j]
        R = G209.D_A(c_z[j]) * sep[j] / t4[name]["r500"]
        v = (g["cz"] - c1[name]["z"] * G209.C_KMS) / (1 + c_z[j])
        # projected offsets in R500 units
        d_ra = (g_ra[i] - c_ra[j]) * math.cos(math.radians(c_dec[j])) * math.pi / 180.0
        d_dec = (g_dec[i] - c_dec[j]) * math.pi / 180.0
        X = G209.D_A(c_z[j]) * d_ra / t4[name]["r500"]
        Y = G209.D_A(c_z[j]) * d_dec / t4[name]["r500"]
        rows.append(dict(cl=name, R=R, v=v, e=g["ec"], X=X, Y=Y))
    R = np.array([r["R"] for r in rows]); V = np.array([r["v"] for r in rows])
    cl = np.array([r["cl"] for r in rows]); e = np.array([r["e"] for r in rows])
    X = np.array([r["X"] for r in rows]); Y = np.array([r["Y"] for r in rows])
    # G203 iterative 3.5-sigma MAD clean (committed)
    for _ in range(2):
        med, mad = np.median(V), 1.4826*np.median(np.abs(V-np.median(V)))
        ok = np.abs(V-med) <= 3.5*mad
        R, V, cl, e, X, Y = R[ok], V[ok], cl[ok], e[ok], X[ok], Y[ok]
    return dict(R=R, V=V, cl=cl, e=e, X=X, Y=Y, c1=c1, t4=t4, names=names)

d = load_xy()
print("loaded", len(d["R"]), "members (paper total 10145)")
shell = (d["R"] >= 0.2) & (d["R"] < 1.5)
print("core shell [0.2,1.5) R500:", int(shell.sum()))
clusters = np.unique(d["cl"])
print("clusters:", len(clusters))
# per-cluster core counts
cnts = []
for k in clusters:
    m = (d["cl"]==k) & shell
    cnts.append(int(m.sum()))
cnts = np.array(cnts)
print("per-cluster core members: min", cnts.min(), "med", np.median(cnts), "max", cnts.max(), "ncl with >=10:", int((cnts>=10).sum()))

# --- per-cluster gradient fit prototype ---
def fit_grad(X, Y, v, w):
    A = np.column_stack([np.ones_like(X), X, Y])
    W = np.sqrt(w)
    coef, *_ = np.linalg.lstsq(A*W[:,None], v*W, rcond=None)
    return coef  # [v0, a, b]

amps, errs, nulls, angles = [], [], [], []
rng = np.random.default_rng(42)
for k in clusters:
    m = (d["cl"]==k) & shell
    n = int(m.sum())
    if n < 10: continue
    X, Y, v, e = d["X"][m], d["Y"][m], d["V"][m], d["e"][m]
    w = np.where(e>0, 1.0/e**2, 1.0)
    c = fit_grad(X, Y, v, w)
    a, b = c[1], c[2]
    amps.append(math.hypot(a,b)); angles.append(math.atan2(b,a))
    # bootstrap errors
    bs = []
    for _ in range(150):
        idx = rng.integers(0, n, n)
        c2 = fit_grad(X[idx], Y[idx], v[idx], w[idx])
        bs.append((c2[1], c2[2]))
    bs = np.array(bs)
    sa, sb = bs[:,0].std(), bs[:,1].std()
    cov = np.cov(bs[:,0], bs[:,1])
    # error on amplitude via delta method on (a,b) cov
    if a*a+b*b > 0:
        J = np.array([a/math.hypot(a,b), b/math.hypot(a,b)])
        eA = math.sqrt(J @ cov @ J)
    else:
        eA = math.sqrt(sa**2+sb**2)
    errs.append(eA)
    # null: shuffle v
    nv = []
    for _ in range(100):
        vs = rng.permutation(v)
        c3 = fit_grad(X, Y, vs, w)
        nv.append(math.hypot(c3[1], c3[2]))
    nulls.append(np.mean(nv))

amps = np.array(amps); errs = np.array(errs); nulls = np.array(nulls); angles = np.array(angles)
print("\nper-cluster gradient amplitude (km/s per R500):")
print(" mean A:", amps.mean().round(1), "median:", np.median(amps).round(1))
print(" null mean (shuffle):", nulls.mean().round(1))
print(" excess:", (amps-nulls).mean().round(1), " +/- ", (amps-nulls).std(ddof=1)/math.sqrt(len(amps)))
print(" A_null per-cluster scatter:", nulls.std(ddof=1).round(1))
# coherent vector mean
gm = np.array([np.mean([math.cos(t) for t in angles])*1, np.mean([math.sin(t) for t in angles])*1])
# coherent vector from (a,b) directly
gs = []
for k in clusters:
    m = (d["cl"]==k) & shell
    if int(m.sum()) < 10: continue
    X, Y, v, e = d["X"][m], d["Y"][m], d["V"][m], d["e"][m]
    w = np.where(e>0, 1.0/e**2, 1.0)
    c = fit_grad(X, Y, v, w)
    gs.append((c[1], c[2]))
gs = np.array(gs)
print(" coherent vector mean:", gs.mean(axis=0).round(1), "amp:", math.hypot(*gs.mean(axis=0)).round(1))
print(" z of coherent amplitude vs 0:", (math.hypot(*gs.mean(axis=0))/(gs.std(axis=0).mean()/math.sqrt(len(gs)))).round(2))
print(" n clusters fit:", len(amps), "n with A>3err:", int((amps > 3*errs).sum()))
