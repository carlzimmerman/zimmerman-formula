#!/usr/bin/env python3
"""Debug: inspect per-cluster gradient fit details."""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import G209_beta_profile as G209
DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "G203_data")

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
        d_ra = (g_ra[i] - c_ra[j]) * math.cos(math.radians(c_dec[j])) * math.pi / 180.0
        d_dec = (g_dec[i] - c_dec[j]) * math.pi / 180.0
        X = G209.D_A(c_z[j]) * d_ra / t4[name]["r500"]
        Y = G209.D_A(c_z[j]) * d_dec / t4[name]["r500"]
        rows.append(dict(cl=name, R=R, v=v, e=g["ec"], X=X, Y=Y))
    R = np.array([r["R"] for r in rows]); V = np.array([r["v"] for r in rows])
    cl = np.array([r["cl"] for r in rows]); e = np.array([r["e"] for r in rows])
    X = np.array([r["X"] for r in rows]); Y = np.array([r["Y"] for r in rows])
    for _ in range(2):
        med, mad = np.median(V), 1.4826*np.median(np.abs(V-np.median(V)))
        ok = np.abs(V-med) <= 3.5*mad
        R, V, cl, e, X, Y = R[ok], V[ok], cl[ok], e[ok], X[ok], Y[ok]
    return dict(R=R, V=V, cl=cl, e=e, X=X, Y=Y)

d = load_xy()
print("ec distribution: min", d["e"].min(), "med", np.median(d["e"]), "max", d["e"].max())
shell = (d["R"] >= 0.2) & (d["R"] < 1.5)
clusters = np.unique(d["cl"])
print("X rms (shell):", d["X"][shell].std().round(4), " Y rms:", d["Y"][shell].std().round(4))
rng = np.random.default_rng(1)
for k in clusters[:8]:
    m = (d["cl"]==k) & shell
    n = int(m.sum())
    if n < 10: continue
    X, Y, v, e = d["X"][m], d["Y"][m], d["V"][m], d["e"][m]
    print(f"\n{k}: n={n} Xstd={X.std():.3f} vstd={v.std():.0f} med e={np.median(e):.1f}")
    A = np.column_stack([np.ones_like(X), X, Y]); W = np.sqrt(np.where(e>0,1.0/e**2,1.0))
    coef,*_ = np.linalg.lstsq(A*W[:,None], v*W, rcond=None)
    print("  fit (v0,a,b):", np.round(coef,2), "amp:", round(math.hypot(coef[1],coef[2]),2))
    # unweighted
    coef2,*_ = np.linalg.lstsq(A, v, rcond=None)
    print("  unweighted amp:", round(math.hypot(coef2[1],coef2[2]),2))
    # null: 3 shuffles
    for _ in range(3):
        vs = rng.permutation(v)
        c = np.linalg.lstsq(A*W[:,None], vs*W, rcond=None)[0]
        print("    null amp:", round(math.hypot(c[1],c[2]),2), end="")
    print()
