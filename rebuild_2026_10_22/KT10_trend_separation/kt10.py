#!/usr/bin/env python3
"""KT10: does KT8's trend follow bulge share or radius and resolution? See FROZEN_CRITERIA.md."""
import glob, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, "../../real_research/data/sparc_data")
MRT = os.path.join(HERE, "../../real_research/data/SPARC_Lelli2016c.mrt")
MUT = os.environ.get("KT10_MUTATE") == "1"
KPC, GN, MSUN = 3.0857e19, 6.674e-11, 1.989e30
ND = 500 if MUT else 2000
tab = {}
for line in open(MRT):
    p = line.split()
    if len(p) >= 18 and p[1].isdigit():
        tab[p[0]] = dict(D=float(p[2]), Inc=float(p[5]), Q=int(p[17]))
RAW = []
for fn in sorted(glob.glob(os.path.join(D, "*_rotmod.dat"))):
    try: d = np.genfromtxt(fn, comments="#")
    except Exception: continue
    if d.ndim != 2 or d.shape[1] < 6 or len(d) < 3: continue
    RAW.append((os.path.basename(fn).replace("_rotmod.dat", ""), d))
c, Gv = 2.99792458e8, 6.674e-11
rc = 3 * (67.4e3 / 3.0857e22) ** 2 / (8 * math.pi * Gv)
S = {"rho_DE": c * math.sqrt(Gv * .685 * rc), "rho_crit": c * math.sqrt(Gv * rc)}
def pred(gb, s):
    lo, hi = gb.copy(), gb * 10 + np.sqrt(gb * s) * 10
    for _ in range(70):
        mid = .5 * (lo + hi); f = mid * (1 - (1 + mid / s) ** -2.0) - gb
        lo, hi = np.where(f < 0, mid, lo), np.where(f < 0, hi, mid)
    return .5 * (lo + hi)
def build(ub=.7):
    """list of galaxies: name, has_bulge, R, Vo, Vg2, Vd2, Vb2, r_kpc mask applied at ub"""
    o = []
    for name, d in RAW:
        R0, V0, e0, Vg0, Vd0, Vb0 = (d[:, j] for j in range(6))
        m = (R0 > 0) & (V0 > 0) & (e0 > 0) & (e0 / V0 < .1)
        if m.sum() < 3: continue
        R, V, Vg, Vd, Vb = R0[m], V0[m], Vg0[m], Vd0[m], Vb0[m]
        G2, D2, B2 = Vg * abs(Vg), .5 * Vd * abs(Vd), Vb * abs(Vb)
        k = G2 + D2 + ub * B2 > 0
        if k.sum() < 3: continue
        o.append(dict(name=name, bulge=bool(np.any(Vb0 != 0)), R=R[k], V=V[k], G2=G2[k], D2=D2[k], B2=B2[k], L=(Vb0[R0 > 0][-1] * 1e3) ** 2 * R0[R0 > 0][-1] * KPC / GN / MSUN, **tab.get(name, dict(D=float("nan"), Inc=float("nan"), Q=9))))
    return o
GL = build()
def fields(g, s, ub=.7, gobs=None):
    tot = g["G2"] + g["D2"] + ub * g["B2"]
    keep = tot > 0
    gb = tot[keep] * 1e6 / (g["R"][keep] * KPC)
    go = (g["V"][keep] ** 2 * 1e6 / (g["R"][keep] * KPC)) if gobs is None else gobs[keep]
    r = np.log10(go) - np.log10(pred(gb, s))
    return np.log10(gb) + 10.5, r, (ub * g["B2"][keep]) / tot[keep], g["R"][keep], keep
def wfit(items, idx):
    """within-galaxy slope(s); items: list of (x, f, r); f may be None"""
    A = None
    for i in idx:
        x, f, r = items[i]
        if len(x) < 2: continue
        X = np.c_[x - x.mean()] if f is None else np.c_[x - x.mean(), f - f.mean()]
        if A is None: A, b = np.zeros((X.shape[1],) * 2), np.zeros(X.shape[1])
        A += X.T @ X; b += X.T @ (r - r.mean())
    return np.linalg.lstsq(A, b, rcond=None)[0]
def boot(items, nd=ND, seed=20261102):
    n = len(items); rng = np.random.default_rng(seed)
    p = wfit(items, range(n)); B = np.zeros((nd, len(p)))
    for k in range(nd): B[k] = wfit(items, rng.integers(0, n, n))
    ci = [[round(float(np.percentile(B[:, j], 2.5)), 4), round(float(np.percentile(B[:, j], 97.5)), 4)] for j in range(len(p))]
    return [round(float(v), 4) for v in p], ci
has0 = lambda ci: ci[0] <= 0 <= ci[1]
def s1(gset, s, ub=.7, obs=None, shuffle=False):
    it = []; rng = np.random.default_rng(3)
    for g in gset:
        x, r, f, _, _ = fields(g, s, ub, None if obs is None else obs[g["name"]])
        it.append((x, rng.permutation(f) if shuffle else f, r))
    return boot(it)
if MUT:
    bs = [g for g in GL if g["bulge"]]
    p, ci = s1(bs, S["rho_DE"], shuffle=True)
    print("S1 shuffled f_b: x", p[0], ci[0], "f_b", p[1], ci[1]); print("MUTATE bites" if has0(ci[1]) else "MUTATE FAILED"); sys.exit(1)
out = {}
GRID = np.round(np.arange(.1, 1.5001, .05), 3)
def s5(gset, s, obs=None, within=False):
    res = {}
    for g in gset:
        best, bv = None, 1e9
        for u in GRID:
            _, r, _, _, _ = fields(g, s, u, None if obs is None else obs[g["name"]])
            v = np.mean((r - r.mean()) ** 2) if within else np.mean(r**2)
            if v < bv: bv, best = v, u
        res[g["name"]] = best
    return res
def summ(res, seed=20261102):
    a = np.array(list(res.values())); rng = np.random.default_rng(seed)
    m = [np.median(rng.choice(a, len(a))) for _ in range(ND)]
    return dict(median=float(np.median(a)), p16=float(np.percentile(a, 16)), p84=float(np.percentile(a, 84)), med95=[float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))], edges=int(((a <= GRID[0]) | (a >= GRID[-1])).sum()))
bs = [g for g in GL if g["bulge"]]
print(f"{len(GL)} galaxies, {len(bs)} with bulges")
# planted, rho_DE
s0 = S["rho_DE"]
real = {g["name"]: fields(g, s0, .7) for g in GL}
def mock(true_u, radial=0.0):
    o = {}
    for g in GL:
        tot = g["G2"] + g["D2"] + true_u * g["B2"]
        gb = np.maximum(tot, 1e-6) * 1e6 / (g["R"] * KPC)
        x_, r_, _, _, kp = fields(g, s0, .7)
        sc = np.zeros_like(gb); rr = np.random.default_rng(abs(hash(g["name"])) % 2**32 if False else len(g["name"]) + int(g["R"].sum() * 10) % 9973).permutation(r_ - r_.mean())
        sc[kp] = rr
        xfull = np.log10(gb) + 10.5
        o[g["name"]] = pred(gb, s0) * 10 ** (sc + radial * (xfull - xfull[kp].mean()))
    return o
m1 = mock(.5)
p, ci = s1(bs, s0, .7, m1); print("PLANTED mass error (true 0.5, analysed 0.7): x", p[0], ci[0], "f_b", p[1], ci[1])
s5p = summ(s5(bs, s0, m1)); print("   S5 recovers:", s5p)
ok1 = not has0(ci[1]) and s5p["p16"] <= .5 <= s5p["p84"]
m2 = mock(.7, -.03)
p, ci = s1(bs, s0, .7, m2); print("PLANTED radial -0.03: x", p[0], ci[0], "f_b", p[1], ci[1])
ok2 = not has0(ci[0]); okf = has0(ci[1])
print(f"Planted: mass {'PASS' if ok1 else 'FAIL'}; radial x {'PASS' if ok2 else 'FAIL'}; radial f_b contains 0 {okf}")
out["planted"] = [bool(ok1), bool(ok2), bool(okf)]
for f_, s in S.items():
    print("\n==", f_)
    p, ci = s1(bs, s); print(f"S1 joint: x {p[0]} {ci[0]}; f_b {p[1]} {ci[1]}"); out[f_ + "_S1"] = dict(p=p, ci=ci)
    its2 = []; its2b = []
    for g in GL:
        x, r, fb, _, _ = fields(g, s)
        k = fb < .1
        if k.sum() >= 3:
            its2.append((x[k], None, r[k]))
            if g["bulge"]: its2b.append((x[k], None, r[k]))
    a2, c2 = boot(its2); b2, d2 = boot(its2b)
    print(f"S2 f_b<0.1: all {len(its2)} gal T2 {a2[0]} {c2[0]}; bulge {len(its2b)} gal T2 {b2[0]} {d2[0]}"); out[f_ + "_S2b"] = dict(p=b2, ci=d2)
    s3r = {}
    for cut in (0, 15, 30):
        its = []
        for g in GL:
            x, r, _, R, _ = fields(g, s)
            ang = R / g["D"] * 1e-3 * 206265
            k = ang >= cut
            if k.sum() >= 3: its.append((x[k], None, r[k]))
        a3, c3 = boot(its); s3r[cut] = c3[0]
        print(f"S3 >= {cut} arcsec: {len(its)} gal, T2 {a3[0]} {c3[0]}")
    def split(tag, test):
        for lab, want in (("yes", True), ("no", False)):
            its = [(fields(g, s)[0], None, fields(g, s)[1]) for g in bs if test(g) == want]
            a4, c4 = boot(its)
            print(f"S4 {tag} {lab}: {len(its)} gal T2 {a4[0]} {c4[0]}")
    md = np.median([g["D"] for g in bs])
    split(f"D>{md:.1f}", lambda g: g["D"] > md); split("Inc>75", lambda g: g["Inc"] > 75); split("Q=1", lambda g: g["Q"] == 1)
    r1 = s5(bs, s); r2 = s5(bs, s, within=True)
    e1, e2 = summ(r1), summ(r2)
    print("S5 level + shape:", e1); print("S5 shape only:", e2)
    aa = np.array([r1[g["name"]] for g in bs]); 
    print("S5 corr log L", round(float(np.corrcoef(aa, np.log10([g["L"] for g in bs]))[0, 1]), 3), "log D", round(float(np.corrcoef(aa, np.log10([g["D"] for g in bs]))[0, 1]), 3))
    out[f_ + "_S5"] = dict(level=e1, shape=e2, per=r1)
    cf, cx = out[f_ + "_S1"]["ci"][1], out[f_ + "_S1"]["ci"][0]
    lab = "FOLLOWS BULGE SHARE" if not has0(cf) and has0(cx) and has0(d2[0]) else "FOLLOWS RADIUS OR RESOLUTION" if (not has0(cx) and has0(cf)) or (has0(cf) and (has0(s3r[15]) or has0(s3r[30])) and not has0(s3r[0])) else "NOT SEPARATED"
    print("LABEL", f_, ":", lab); out[f_ + "_label"] = lab
json.dump(out, open(os.path.join(HERE, "kt10.json"), "w"), indent=1)
sys.exit(0 if ok1 and ok2 else 2)
