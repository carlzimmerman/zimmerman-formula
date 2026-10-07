#!/usr/bin/env python3
"""CFG413 KiDS leg: the law's phantom truncated at r_on = x r_ta, plus a FREE two-halo amplitude, against CFG377's
KiDS-1000 isolated-lens stack (15 g_bar bins, 50-patch jackknife, Hartlap).  Criteria: FROZEN_CRITERIA.md.
cfg100_lib is imported read-only (nu_mono, r_ta_law, dsigma, _finish); the stack/covariance code is CFG377's, copied.
Usage: nice -n 15 python3 cfg413_kids.py ;  CFG413_MUTATE=1 nice -n 15 python3 cfg413_kids.py  (adds x = 0.05)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "CFG100_kids_mass_rederivation"))
import cfg100_lib as C                                                       # read-only import
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
MUTATE = os.environ.get("CFG413_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
try:
    os.nice(15)
except OSError:
    pass
XS = [0.23, 0.3, 0.4, 0.5, 0.7, 1.0]
if MUTATE:
    XS = [0.05] + XS
FOOTS = ("canonical", "alt")
LOG, CHK = [], {}
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)
def check(name, ok, msg):
    CHK[name] = bool(ok); P("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, msg))
np.set_printoptions(linewidth=200, precision=4)
T0 = time.time()

# ---------------------------------------------------------------- data (CFG377 copy)
NPATCH = 50
KG = 1.98847e30 / (3.0857e16) ** 2
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
z = lens["z"].astype(float); Mgal = lens["Mgal"].astype(float)
jk = np.load(os.path.join(DATA, "lr_esd_jackknife.npz")); patch = jk["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
iso = np.load(os.path.join(DATA, "cfg96_isoflags.npz")); f30 = iso["f30"].astype(bool)
assert np.allclose(pl["gbar_edges"], C.GEDGE)
nL = len(z)

def esd_full_loo(mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch[mask], weights=WG[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch[mask], weights=WW[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev
def hart(p): return (NPATCH - p - 2) / (NPATCH - 1)

lmg = np.log10(Mgal)
key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(z / 0.03).astype(np.int64)
_, gi, cnt = np.unique(key, return_inverse=True, return_counts=True)
gi = gi.ravel()
GM = 10 ** (np.bincount(gi, weights=lmg) / cnt); GZ = np.bincount(gi, weights=z) / cnt
NG = len(cnt)
P(f"CFG413 KiDS leg  MUTATE={MUTATE}  x grid {XS}; lenses {nL}, groups {NG}, f30 {int(f30.sum())}")

def pstack(tab, mask):
    out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out
gcen = np.sqrt(C.GEDGE_K[:-1] * C.GEDGE_K[1:])
def mean_R(mask):
    Rik = np.sqrt(C.G_MPC * Mgal[mask][:, None] / gcen[None, :])
    return (WW[mask] * Rik).sum(0) / WW[mask].sum(0)

# ---------------------------------------------------------------- model tables: law truncated at x r_ta
def law_vec(Mg, re, a0):
    r = np.geomspace(1e-4, re, 1500)
    Md = Mg * (C.nu_mono(C.G_MPC * Mg / r ** 2 / a0) - 1.0)
    return C._finish(lambda R: C.dsigma(R, r, Md) + Mg / (math.pi * R ** 2), Mg)

RTA = {}; TAB = {}
t = time.time()
for foot in FOOTS:
    a0 = C.A0[foot]
    RTA[foot] = np.array([C.r_ta_law(GM[g], a0, GZ[g]) for g in range(NG)])
    TAB[foot] = {x: np.array([law_vec(GM[g], x * RTA[foot][g], a0) for g in range(NG)]) for x in XS}
    P(f"  tables {foot}: {time.time() - t:.0f} s; r_ta (Mpc) group median {np.median(RTA[foot]):.3f}, 10-90% "
      f"{np.percentile(RTA[foot], 10):.3f}-{np.percentile(RTA[foot], 90):.3f}")
TT = np.array([C._finish(lambda R: R ** -0.8 * 1e12, GM[g]) for g in range(NG)])   # CFG377's two-halo template

# ---------------------------------------------------------------- chi2 with the two-halo amplitude profiled
def chi2(d, C_, h, m, t, mode="free"):
    Ci = np.linalg.inv(C_); r = d - m
    if mode == "none":
        return float(h * r @ Ci @ r), 0.0
    A = float((t @ Ci @ r) / (t @ Ci @ t))
    if mode == "pos":
        A = max(A, 0.0)
    rr = r - A * t
    return float(h * rr @ Ci @ rr), A

def leg(mask, label, sel=None):
    d, Cv = esd_full_loo(mask); tm = pstack(TT, mask); Rm = mean_R(mask)
    if sel is not None:
        d, Cv, tm = d[sel], Cv[np.ix_(sel, sel)], tm[sel]
    h = hart(len(d)); out = dict(n=int(mask.sum()), nbins=len(d))
    for foot in FOOTS:
        rows = {}
        for x in XS:
            m = pstack(TAB[foot][x], mask)
            if sel is not None:
                m = m[sel]
            rows[x] = {mode: chi2(d, Cv, h, m, tm, mode) for mode in ("free", "pos", "none")}
        out[foot] = {str(x): {mode: dict(chi2=rows[x][mode][0], A=rows[x][mode][1], dchi2=rows[x][mode][0] - rows[1.0][mode][0])
                              for mode in rows[x]} for x in XS}
    return out, d, Cv, Rm

# ---------------------------------------------------------------- primary
ALL = np.ones(nL, bool)
RES = dict(mutate=MUTATE, xs=XS)
prim, d, Cv, Rm = leg(ALL, "primary")
RES["primary"] = prim; RES["meanR_Mpc"] = Rm.tolist(); RES["esd"] = d.tolist(); RES["sig"] = np.sqrt(np.diag(Cv)).tolist()
P("pair-weighted mean R [Mpc]:", np.round(Rm, 3))
P("ESD data / sigma          :", np.round(d, 3), "/", np.round(np.sqrt(np.diag(Cv)), 3))
for foot in FOOTS:
    rtm = float(np.median(RTA[foot]))
    P(f"\n[{foot}]  (typical r_ta {rtm:.2f} Mpc -> r_on per x: " + ", ".join(f"{x}:{x * rtm:.2f}" for x in XS) + ")")
    P("   x    | chi2 free  dchi2  A_2h      | chi2 A>=0  dchi2 | chi2 no-2h  dchi2")
    for x in XS:
        r = prim[foot][str(x)]
        P(f"  {x:5.2f} | {r['free']['chi2']:8.2f} {r['free']['dchi2']:+7.2f} {r['free']['A']:9.3g} | {r['pos']['chi2']:8.2f} {r['pos']['dchi2']:+7.2f} | {r['none']['chi2']:8.2f} {r['none']['dchi2']:+8.2f}")
    # model vs data for x = 0.23 and 1 (free)
    for x in (XS[0], 1.0):
        m = pstack(TAB[foot][x], ALL); A = prim[foot][str(x)]["free"]["A"]; tm = pstack(TT, ALL)
        P(f"   x={x}: law {np.round(m, 3)}\n          law+2h {np.round(m + A * tm, 3)}")

# ---------------------------------------------------------------- checks K1, K2 (CFG377 reproduction at x = 0.4)
ref = {"canonical": (9.7, 325.49), "alt": (11.9, 261.19)}
try:
    j377 = json.load(open(os.path.join(HERE, "..", "CFG377_kids_reservoir_dip", "cfg377_results.json")))
    ref = {f: (j377["primary"][f]["chi2_bare_nuis"], j377["primary"][f]["chi2_bare"]) for f in FOOTS}
except Exception as e:
    P("  (CFG377 json not read: %s; using README values)" % e)
k1 = max(abs(prim[f]["0.4"]["free"]["chi2"] - ref[f][0]) for f in FOOTS)
k2 = max(abs(prim[f]["0.4"]["none"]["chi2"] - ref[f][1]) for f in FOOTS)
check("K1 x=0.4 free-2h chi2 reproduces CFG377", k1 <= 0.05, "max |diff| %.4f (ref %s)" % (k1, {f: round(ref[f][0], 3) for f in FOOTS}))
check("K2 x=0.4 no-2h chi2 reproduces CFG377", k2 <= 0.05, "max |diff| %.4f (ref %s)" % (k2, {f: round(ref[f][1], 2) for f in FOOTS}))

# ---------------------------------------------------------------- x_min and drop-one-bin robustness
def xmin_of(res, foot, mode="free"):
    ok = [x for x in XS if x >= 0.2 and res[foot][str(x)][mode]["dchi2"] <= 4.0]
    return min(ok) if ok else None
RES["x_min"] = {f: xmin_of(prim, f) for f in FOOTS}
RES["x_min_pos"] = {f: xmin_of(prim, f, "pos") for f in FOOTS}
RES["x_min_none"] = {f: xmin_of(prim, f, "none") for f in FOOTS}
P(f"\nx_min (free 2h, Delta chi2 <= 4): {RES['x_min']} | A>=0: {RES['x_min_pos']} | no 2h: {RES['x_min_none']}")
# reported only (not frozen): x = 1 is not the best-fitting grid point, so also measure Delta chi2 against the best grid x
best = {}
for f in FOOTS:
    gx_ = [x for x in XS if x >= 0.2]; cb = min(prim[f][str(x)]["free"]["chi2"] for x in gx_)
    xb = [x for x in gx_ if prim[f][str(x)]["free"]["chi2"] == cb][0]
    rel = {str(x): prim[f][str(x)]["free"]["chi2"] - cb for x in gx_}
    best[f] = dict(x_best=xb, chi2_best=cb, dchi2_vs_best=rel, x_min_vs_best=min(x for x in gx_ if rel[str(x)] <= 4.0))
    P(f"  [{f}] REPORTED ONLY: best grid x {xb} (chi2 {cb:.2f}/15); Delta chi2 vs best: "
      + ", ".join(f"{x}:{v:+.2f}" for x, v in rel.items()) + f" -> x_min vs best {best[f]['x_min_vs_best']}")
RES["vs_best_x_reported"] = best
# reported only: share of the fitted model carried by the free "two-halo" template, per bin
tm_all = pstack(TT, ALL); share2h = {}
for f in FOOTS:
    share2h[f] = {}
    for x in [x for x in XS if x >= 0.2]:
        m = pstack(TAB[f][x], ALL); A = prim[f][str(x)]["free"]["A"]
        share2h[f][str(x)] = (A * tm_all / (m + A * tm_all)).tolist()
    P(f"  [{f}] REPORTED ONLY: two-halo share of the model at R = {Rm[6]:.3f} / {Rm[3]:.3f} / {Rm[0]:.3f} Mpc: "
      + ", ".join(f"x {x}: {s[6]:.2f}/{s[3]:.2f}/{s[0]:.2f}" for x, s in share2h[f].items()))
RES["twohalo_share_reported"] = share2h
drop = {f: [] for f in FOOTS}; dropd = {f: {} for f in FOOTS}
for k in range(15):
    sel = np.array([i for i in range(15) if i != k])
    r_, *_ = leg(ALL, f"drop{k}", sel)
    for f in FOOTS:
        drop[f].append(xmin_of(r_, f)); dropd[f][k] = {str(x): r_[f][str(x)]["free"]["dchi2"] for x in XS}
RES["drop_one_bin"] = dict(x_min=drop, dchi2=dropd)
for f in FOOTS:
    xm = [v if v is not None else float("nan") for v in drop[f]]
    P(f"  drop-one-bin x_min [{f}]: {xm} -> largest {np.nanmax(xm) if not all(np.isnan(xm)) else None}")
    P(f"     dchi2 range over drops per x: " + ", ".join(f"{x}: {min(dropd[f][k][str(x)] for k in range(15)):+.2f}..{max(dropd[f][k][str(x)] for k in range(15)):+.2f}" for x in XS))

# ---------------------------------------------------------------- reported only: f30, trusted range R <= 0.3/h Mpc
s1, *_ = leg(f30, "f30"); RES["S1_f30"] = s1
trusted = np.nonzero(Rm <= 0.3 / 0.6736)[0]
s3, *_ = leg(ALL, "trusted", trusted); RES["S3_trusted_bins"] = dict(bins=trusted.tolist(), **s3)
for f in FOOTS:
    P(f"  [{f}] f30 dchi2(free): " + ", ".join(f"{x}:{s1[f][str(x)]['free']['dchi2']:+.2f}" for x in XS))
    P(f"  [{f}] trusted {len(trusted)} bins (R <= 0.445 Mpc) dchi2(free): " + ", ".join(f"{x}:{s3[f][str(x)]['free']['dchi2']:+.2f}" for x in XS))

# ---------------------------------------------------------------- distinguishability
gx = [x for x in XS if x >= 0.2]
indist = all(prim[f][str(x)]["free"]["dchi2"] <= 4 for f in FOOTS for x in gx)
RES["cannot_distinguish_grid"] = indist
P(f"\nKiDS cannot distinguish the grid x (all Delta chi2 <= 4 on both footings): {indist}")

if MUTATE:
    dm = {f: prim[f]["0.05"]["free"]["dchi2"] for f in FOOTS}
    det = all(v > 4 for v in dm.values())
    check("MUTATE x=0.05 fails KiDS (Delta chi2 > 4, both footings, free 2h)", det, f"{ {f: round(v, 2) for f, v in dm.items()} }")
    P(f"MUTATE {'DETECTED' if det else 'NOT DETECTED'}")
    RES["mutate_detected"] = det

RES["checks"] = CHK
P(f"checks {CHK}; elapsed {time.time() - T0:.0f} s")
json.dump(RES, open(os.path.join(HERE, f"cfg413_kids_results{SUF}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg413_kids{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
