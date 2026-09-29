#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CFG167 attacks (a1)-(a5) and (c), frozen procedures.  ZF_REPO=<repo> python3 CFG167_attacks_ac.py [SEED] > CFG167_attacks_ac.out (rc 0). SEED default 167 (re-run 168)."""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
import CFG167_referee_diff_p4 as D67
M = D67.M
P = lambda *a: print(*a, flush=True)
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 167
rng = np.random.default_rng(SEED)
SK, SR, AS = D67.load_all("inc_star_deg")
P4 = D67.P4
OUT = dict(seed=SEED)
P(f"CFG167 attacks (a) and (c), seed {SEED}, repo=<repo>")
main = D67.diff(SK, SR, P4, P4)
D0, sD0, DH0 = main["D"], main["sD"], main["DH"]
P(f"nominal: D {D0:+.4f} +- {sD0:.4f}  D_H {DH0:+.4f}  z_flat {main['zf']:+.2f} z_rival {main['zh']:+.2f}")
kd, ke_, kh, keh = main["kpo"]["d_flat"], main["kpo"]["e_flat"], main["kpo"]["d_H"], main["kpo"]["e_H"]
rd, re_, rh, reh = main["rpo"]["d_flat"], main["rpo"]["e_flat"], main["rpo"]["d_H"], main["rpo"]["e_H"]


def pool_rows(d, e):
    """vectorised M.pool for arrays (N, n): returns mean, err (with chi2/dof inflation)"""
    w = 1.0 / e ** 2
    sw = w.sum(1)
    m = (w * d).sum(1) / sw
    chi = (w * (d - m[:, None]) ** 2).sum(1) / max(d.shape[1] - 1, 1)
    return m, np.sqrt(1.0 / sw) * np.sqrt(np.maximum(chi, 1.0))


def cls_vec(D, DH, sD):
    nf, nh = np.abs(D) <= 2 * sD, np.abs(D - DH) <= 2 * sD
    return dict(both=float(np.mean(nf & nh)), flat=float(np.mean(nf & ~nh)), rival=float(np.mean(~nf & nh)), manuf=float(np.mean(~nf & ~nh)))


# ============================================================================================ (a1) bootstrap
P("\n" + "=" * 100 + "\n(a1) nonparametric bootstrap of D (10 KURVS, 390 KROSS resampled independently), N = 20000\n" + "=" * 100)
N = 20000
ik = rng.integers(0, 10, (N, 10))
ir = rng.integers(0, 390, (N, 390))
km, ker = pool_rows(kd[ik], ke_[ik])
kmh, _ = pool_rows(kh[ik], keh[ik])
rm, rer = pool_rows(rd[ir], re_[ir])
rmh, _ = pool_rows(rh[ir], reh[ir])
Db = km - rm
DHb = (km - kmh) - (rm - rmh)
sDb = np.hypot(ker, rer)
q = np.percentile(Db, [2.5, 16, 50, 84, 97.5])
ratio = float(Db.std() / sD0)
P(f"   SD(D_boot) = {Db.std():.4f} vs analytic sigma_D {sD0:.4f}: ratio {ratio:.2f};  mean {Db.mean():+.4f}; percentiles 2.5/16/50/84/97.5: " + " ".join(f"{v:+.3f}" for v in q))
P(f"   bootstrap mean analytic sigma_D {sDb.mean():.4f}; P(D_boot <= 0) = {np.mean(Db <= 0):.4f}; P(D_boot > D_H + 2 sigma_D... (manufactures edge {DH0+2*sD0:+.3f})) = {np.mean(Db > DH0 + 2*sD0):.3f}")
cb = cls_vec(Db, DHb, sDb)
P(f"   class fractions over bootstrap draws (each with own D_H, sigma_D): {cb}")
a1_ok = 0.75 <= ratio <= 1.33
P(f"   (a1) VERDICT: {'ROBUST' if a1_ok else 'NOT ROBUST'} (ratio {ratio:.2f} in [0.75, 1.33]?)")
loo = []
for j in range(10):
    m = np.arange(10) != j
    a = D67.pool_ = None
    f_, fe_ = M.pool(kd[m], ke_[m])[:2]
    h_ = M.pool(kh[m], keh[m])[0]
    D_ = f_ - main["rf"]; DH_ = (f_ - h_) - (main["rf"] - main["rh"]); sD_ = math.hypot(fe_, main["re"])
    loo.append((SK.name[j], D_, sD_, DH_, D67.classify_D(D_, DH_, sD_)))
P("   KURVS leave-one-out: " + "; ".join(f"-{n.split('-')[1]}: {d:+.3f} ({c})" for n, d, s, h, c in loo))
OUT["a1"] = dict(sd=float(Db.std()), ratio=ratio, pct=list(map(float, q)), loo=[(n, float(d), c) for n, d, s, h, c in loo], verdict="ROBUST" if a1_ok else "NOT ROBUST", cls=cb)

# ============================================================================================ (a2) correlated systematics MC
P("\n" + "=" * 100 + "\n(a2) correlated-systematics Monte Carlo (N = 4000 draws; D re-evaluated through the pipeline)\n" + "=" * 100)
NS = 4000
xK = SK.R / SK.Reff - 1
xR = SR.R / SR.Reff - 1


def spec_ab(s=1.0, t=0.0):
    return M.spec("alpha", fn=lambda S_, a: s * M.alpha_K(S_.R / S_.Reff - 1) * (1.0 + t * (S_.R / S_.Reff - 1 - 2.0)))


def draw(kind):
    sK = sR = 1.0; tt = 0.0; dK = dR = 0.0; g = 1.0
    if kind in ("i", "common", "cal_common"):
        s = math.exp(rng.normal(0, 0.4)); sK = sR = s
    if kind in ("ii", "indep"):
        sK = math.exp(rng.normal(0, 0.4)); sR = math.exp(rng.normal(0, 0.4))
    if kind in ("iii", "common", "indep"):
        tt = rng.normal(0, 0.15)
    if kind in ("iv", "indep"):
        dK = rng.normal(0, 0.15); dR = rng.normal(0, 0.15)
    if kind in ("ivc", "common"):
        dK = dR = rng.normal(0, 0.15)
    if kind in ("v", "indep"):
        g = math.exp(rng.normal(0, 0.5))
    return sK, sR, tt, dK, dR, g


sysres = {}
for kind, label in (("i", "(i) common alpha scale lnN(0,0.4)"), ("ii", "(ii) independent alpha scales, each lnN(0,0.4)"), ("iii", "(iii) common tilt t~N(0,0.15)"),
                    ("iv", "(iv) independent mass zero-points 0.15 dex each"), ("ivc", "(iv-c) common mass zero-point 0.15 dex"), ("v", "(v) gas ratio lnN(0,0.5)"),
                    ("common", "COMMON set = (i)+(iii)+(iv-c)"), ("indep", "INDEPENDENT set = (ii)+(iii)+(iv)+(v)")):
    Ds, DHs, sDs = [], [], []
    for _ in range(NS):
        sK, sR, tt, dK, dR, g = draw(kind)
        x = D67.diff(SK, SR, spec_ab(sK, tt), spec_ab(sR, tt), 0.67 * g, 0.67, dK, dR)
        Ds.append(x["D"]); DHs.append(x["DH"]); sDs.append(x["sD"])
    Ds, DHs, sDs = np.array(Ds), np.array(DHs), np.array(sDs)
    sd = float(Ds.std())
    tot = math.hypot(sD0, sd)
    cf = cls_vec(Ds, DHs, sDs)
    sysres[kind] = dict(label=label, sd_sys=sd, mean_shift=float(Ds.mean() - D0), total_sigma=tot, z_flat_tot=D0 / tot, z_riv_tot=(D0 - DH0) / tot, P_rival_class=cf["rival"], cls=cf)
    P(f"   {label:46s}: sd_sys {sd:.4f}  mean(D_draw)-D {Ds.mean()-D0:+.4f}  total sigma {tot:.4f}  z_flat {D0/tot:+.2f}  z_rival {(D0-DH0)/tot:+.2f}   class of D_draw: {cf}")
OUT["a2"] = sysres
zc, zi = sysres["common"]["z_flat_tot"], sysres["indep"]["z_flat_tot"]
a2 = "ROBUST" if (zc >= 2 and zi >= 2) else ("SOFT" if zc >= 2 else "NOT ROBUST")
P(f"   (a2) VERDICT: {a2}  (z_flat under common set {zc:.2f}, under independent set {zi:.2f})")
OUT["a2_verdict"] = a2

# ============================================================================================ (a3) permutation null
P("\n" + "=" * 100 + "\n(a3) permutation null of the error model: 10 random KROSS galaxies as pseudo-KURVS, N = 20000\n" + "=" * 100)
NP = 20000
idx = np.argsort(rng.random((NP, 390)), axis=1)
ip, io = idx[:, :10], idx[:, 10:]
pm, pe = pool_rows(rd[ip], re_[ip])
om, oe = pool_rows(rd[io], re_[io])
Dp = pm - om
sDp = np.hypot(pe, oe)
rp = float(Dp.std() / sDp.mean())
P(f"   SD(D_perm) = {Dp.std():.4f}; mean analytic hypot pooled error {sDp.mean():.4f} (median {np.median(sDp):.4f}); ratio {rp:.2f}; mean D_perm {Dp.mean():+.4f}")
P(f"   fraction of draws with |D_perm| > 2*analytic sigma: {np.mean(np.abs(Dp) > 2*sDp):.4f} (nominal 0.0455); z-score SD {np.std(Dp/sDp):.2f}")
P(f"   informational: real D = {D0:+.3f} sits at percentile {100*np.mean(Dp < D0):.2f} of D_perm (real KURVS have different x, sigma_out and errors)")
a3 = 0.75 <= rp <= 1.33
P(f"   (a3) VERDICT: {'ROBUST' if a3 else 'NOT ROBUST'} (ratio {rp:.2f})")
OUT["a3"] = dict(sd=float(Dp.std()), mean_sigma=float(sDp.mean()), ratio=rp, tail=float(np.mean(np.abs(Dp) > 2 * sDp)), verdict="ROBUST" if a3 else "NOT ROBUST")

# ============================================================================================ (a4) anchor geometry
P("\n" + "=" * 100 + "\n(a4) anchor-geometry adjustment: SPARC z=0 offset vs x = R/R_eff - 1 and vs R/R_d\n" + "=" * 100)
pa = M.per_object(AS, P4, None, 0.0, D67.FOOT, anchor=True)
da, ea = pa["d_flat"], pa["e_flat"]
xa = AS.R / AS.Reff - 1
ua = AS.R / AS.Rd
wK = 1.0 / ke_ ** 2
wK = wK / wK.sum()
uK = SK.R / SK.Rd
uR = SR.R / SR.Rd


def wfit(xv, y, e):
    w = 1.0 / e ** 2
    A = np.vstack([np.ones_like(xv), xv]).T
    C = A.T @ (A * w[:, None])
    b = np.linalg.solve(C, A.T @ (w * y))
    return b


def shift(xv, xK_, xR_, y, e):
    b = wfit(xv, y, e)
    return float(np.sum(wK * (b[0] + b[1] * xK_)) - np.mean(b[0] + b[1] * xR_)), b


P(f"   SPARC anchor n = {len(AS.ids)}; x range {xa.min():.2f}..{xa.max():.2f}; R/R_d range {ua.min():.2f}..{ua.max():.2f}; pooled offset {M.pool(da, ea)[0]:+.4f}")
for lo, hi in ((-9, 1.5), (1.5, 2.5), (2.5, 99)):
    m = (xa >= lo) & (xa < hi)
    if m.sum() > 2:
        P(f"   x in [{lo},{hi}): n={m.sum():2d} pooled offset {M.pool(da[m], ea[m])[0]:+.3f}")
res4 = {}
for nm, xv, xk_, xr_ in (("x", xa, xK, xR), ("R/Rd", ua, uK, uR)):
    sh, b = shift(xv, xk_, xr_, da, ea)
    bs = []
    for _ in range(2000):
        ii = rng.integers(0, len(da), len(da))
        bs.append(shift(xv[ii], xk_, xr_, da[ii], ea[ii])[0])
    bs = np.array(bs)
    Dadj = D0 - sh
    cl = D67.classify_D(Dadj, DH0, sD0)
    P(f"   fit vs {nm:5s}: offset(x) = {b[0]:+.4f} + {b[1]:+.4f}*{nm}; KURVS-weighted minus KROSS offset = {sh:+.4f} (bootstrap sd {bs.std():.4f}); D_adj = {Dadj:+.4f}  class {cl};  |D_adj - D| = {abs(sh):.4f}")
    res4[nm] = dict(shift=sh, sd=float(bs.std()), Dadj=Dadj, cls=cl, slope=float(b[1]))
a4 = all(abs(v["shift"]) <= 0.02 for v in res4.values())
P(f"   (a4) VERDICT: {'ROBUST' if a4 else 'GEOMETRY-SENSITIVE'} (|D_adj - D| <= 0.02 for both fits?)")
OUT["a4"] = dict(res=res4, verdict="ROBUST" if a4 else "GEOMETRY-SENSITIVE")

# ============================================================================================ (a5) gas-ratio surface
P("\n" + "=" * 100 + "\n(a5) gas-ratio surface (informational)\n" + "=" * 100)
gs = (0.5, 1, 1.5, 2, 3, 4)
res5 = {}
for g in gs:
    x = D67.diff(SK, SR, P4, P4, 0.67 * g, 0.67)
    res5[g] = (x["D"], x["DH"], x["sD"], D67.classify_D(x["D"], x["DH"], x["sD"]))
    P(f"   g = {g:3.1f} (mu_K = {0.67*g:.2f}, mu_R = 0.67): D {x['D']:+.3f} +- {x['sD']:.3f}  D_H {x['DH']:+.3f}  -> {res5[g][3]}")
gg = np.exp(np.linspace(math.log(0.25), math.log(12), 60))
Dg, DHg = [], []
for g in gg:
    x = D67.diff(SK, SR, P4, P4, 0.67 * g, 0.67)
    Dg.append(x["D"]); DHg.append(x["DH"])
Dg, DHg = np.array(Dg), np.array(DHg)


def crossing(y, level=0.0):
    s = np.sign(y - level)
    i = np.where(np.diff(s) != 0)[0]
    return [float(np.exp(np.interp(level, [y[k], y[k + 1]] if y[k] < y[k + 1] else [y[k + 1], y[k]], [math.log(gg[k]), math.log(gg[k + 1])] if y[k] < y[k + 1] else [math.log(gg[k + 1]), math.log(gg[k])]))) for k in i]


P(f"   break-even g for D = 0: {crossing(Dg)};  for D = D_H(g): {crossing(Dg - DHg)}")
OUT["a5_g"] = {str(g): v for g, v in res5.items()}
OUT["a5_break"] = dict(D0=crossing(Dg), DH=crossing(Dg - DHg))
# joint absolute-level fit
mur = np.exp(np.linspace(math.log(0.1), math.log(4), 13))
muk = np.exp(np.linspace(math.log(0.1), math.log(8), 17))
ap = M.anchor_pool(P4, 0.0, D67.FOOT, AS)["flat"]
AP, AE = ap[0], ap[1]
KR_ = {m_: D67.pooled(SK, P4, m_) for m_ in muk}
RR_ = {m_: D67.pooled(SR, P4, m_) for m_ in mur}
best = {}
for law in ("flat", "H"):
    for constr in (True, False):
        bestc = (1e9, None)
        for mr in mur:
            for mk in muk:
                if constr and mk < mr:
                    continue
                kk, rr = KR_[mk], RR_[mr]
                yk = (kk["f"] if law == "flat" else kk["h"]) - AP
                yr = (rr["f"] if law == "flat" else rr["h"]) - AP
                C = np.diag([kk["fe"] ** 2, rr["fe"] ** 2]) + AE ** 2
                v = np.array([yk, yr])
                c2 = float(v @ np.linalg.solve(C, v))
                if c2 < bestc[0]:
                    bestc = (c2, (float(mr), float(mk), float(yk), float(yr)))
        best[(law, constr)] = bestc
        P(f"   law {law:4s} {'mu_K >= mu_R' if constr else 'unconstrained':14s}: best chi2 = {bestc[0]:.2f} at mu_R = {bestc[1][0]:.2f}, mu_K = {bestc[1][1]:.2f} (Dprime_K {bestc[1][2]:+.3f}, Dprime_R {bestc[1][3]:+.3f})")
mc = {}
for law in ("flat", "H"):
    kk, rr = KR_[min(muk, key=lambda v: abs(v - 0.67))], RR_[min(mur, key=lambda v: abs(v - 0.67))]
OUT["a5_joint"] = {f"{k[0]}|{'constr' if k[1] else 'free'}": dict(chi2=v[0], at=v[1]) for k, v in best.items()}
P("   (a5) informational, no pass line. With 2 data points and 2 grid parameters chi2 -> 0 wherever both levels are reachable; the useful output is WHICH (mu_R, mu_K) each law needs.")

# ============================================================================================ (c) KROSS selection
P("\n" + "=" * 100 + "\n(c) KROSS comparison sub-sample variants (min n = 30) and KURVS leave-one-out\n" + "=" * 100)
rowsK = {r["name"]: r for r in M.read_csv("data_assembly/high_z_tf_tables/kross_v2.csv")}
kin = np.array([rowsK[n]["kin_type"] for n in SR.name])
ba = np.cos(SR.inc)
vs = SR.V / SR.sig0
Vc_over = np.sqrt(main["rpo"]["Vc2_over_V2"]) - 1
import copy


def subset(S, mask):
    T = copy.copy(S)
    n = len(mask)
    for k, v in vars(S).items():
        if isinstance(v, np.ndarray) and v.shape[:1] == (n,):
            setattr(T, k, v[mask])
        elif isinstance(v, list) and len(v) == n:
            setattr(T, k, [x for x, m in zip(v, mask) if m])
    return T


medM = np.median(SR.logM)
variants = {
    "all 390 (main)": np.ones(390, bool),
    "kin RT only": kin == "RT",
    "kin RT+ only": kin == "RT+",
    "v/sigma0 >= 2": vs >= 2,
    "v/sigma0 >= 3": vs >= 3,
    "logM in KURVS range [9.55,10.68]": (SR.logM >= 9.55) & (SR.logM <= 10.68),
    "logM < median": SR.logM < medM,
    "logM >= median": SR.logM >= medM,
    "b/a > 0.5 (i < 60 deg)": ba > 0.5,
    "z < 0.85": SR.z < 0.85,
    "z >= 0.85": SR.z >= 0.85,
    "drop top 5% pressure correction": Vc_over < np.percentile(Vc_over, 95),
    "drop lowest-error 5%": re_ > np.percentile(re_, 5),
}
resc = {}
verdict_c = True
flips = []
for nm, mk in variants.items():
    if mk.sum() < 30:
        P(f"   {nm:36s}: n = {mk.sum()} < 30, skipped")
        continue
    T = subset(SR, mk)
    x = D67.diff(SK, T, P4, P4)
    cl = D67.classify_D(x["D"], x["DH"], x["sD"])
    ok = (0.098 <= x["D"] <= 0.198) and cl == "lands on the rival"
    if not ok and nm != "all 390 (main)":
        verdict_c = False; flips.append(nm)
    resc[nm] = dict(n=int(mk.sum()), D=x["D"], sD=x["sD"], DH=x["DH"], cls=cl, ok=bool(ok))
    P(f"   {nm:36s}: n = {mk.sum():3d}  D {x['D']:+.4f} +- {x['sD']:.4f}  D_H {x['DH']:+.4f}  -> {cl}{'' if ok else '   [OUTSIDE +-0.05 or class differs]'}")
for n, d, s, h, c in loo:
    ok = (0.098 <= d <= 0.198) and c == "lands on the rival"
    if not ok:
        verdict_c = False; flips.append("LOO " + n)
    resc["LOO " + n] = dict(D=d, sD=s, DH=h, cls=c, ok=bool(ok))
    P(f"   KURVS leave-one-out {n:9s}: D {d:+.4f} +- {s:.4f}  D_H {h:+.4f}  -> {c}{'' if ok else '   [OUTSIDE +-0.05 or class differs]'}")
Ds_ = [v["D"] for v in resc.values()]
P(f"   range of D across all variants: {min(Ds_):+.3f} .. {max(Ds_):+.3f}")
# KROSS-internal redshift lever
lo, hi = SR.z < 0.85, SR.z >= 0.85
def kr_pool(mk):
    T = subset(SR, mk); r = D67.pooled(T, P4, 0.67); return r
a, b = kr_pool(lo), kr_pool(hi)
gap = b["f"] - a["f"]; gerr = math.hypot(a["fe"], b["fe"])
pred = (b["f"] - b["h"]) - (a["f"] - a["h"])
P(f"   KROSS-internal z split: Delta_flat(z>=0.85) - Delta_flat(z<0.85) = {gap:+.4f} +- {gerr:.4f} (flat predicts 0: {gap/gerr:+.2f}s; rival pipeline prediction {pred:+.4f}: {(gap-pred)/gerr:+.2f}s)   [median z: {np.median(SR.z[lo]):.3f} / {np.median(SR.z[hi]):.3f}]")
resc["z_split"] = dict(gap=gap, err=gerr, pred=pred)
# mass-matched draws
nn = [np.argsort(np.abs(SR.logM - m_))[:20] for m_ in SK.logM]
Dm, DHm, sDm = [], [], []
for _ in range(2000):
    pick = np.array([rng.choice(v) for v in nn])
    T = subset(SR, np.isin(np.arange(390), pick))    # unique picks
    x = D67.diff(SK, T, P4, P4)
    Dm.append(x["D"]); DHm.append(x["DH"]); sDm.append(x["sD"])
Dm, DHm, sDm = np.array(Dm), np.array(DHm), np.array(sDm)
P(f"   mass-matched KROSS (one of the 20 nearest-logM per KURVS galaxy, N = 2000; n <= 10, informational, excluded from the verdict): mean D {Dm.mean():+.4f}, sd {Dm.std():.4f}, class fractions {cls_vec(Dm, DHm, sDm)}")
resc["massmatch"] = dict(mean=float(Dm.mean()), sd=float(Dm.std()), cls=cls_vec(Dm, DHm, sDm))
P(f"   (c) VERDICT: {'ROBUST' if verdict_c else 'FRAGILE'}" + ("" if verdict_c else f"; variants outside: {flips}"))
OUT["c"] = dict(res=resc, verdict="ROBUST" if verdict_c else "FRAGILE", flips=flips)
json.dump(OUT, open(os.path.join(D67.HERE, f"CFG167_attacks_ac_results_seed{SEED}.json"), "w"), indent=1, default=float)
P("written results json; exit 0")
