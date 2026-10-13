#!/usr/bin/env python3
"""CFG669 (FROZEN_CRITERIA.md, c42424774): the KiDS age signal (T1) and early-type excess (T2) on near-IR Ks stellar masses, with
LePhare and Taylor+11 recomputed side by side.  CFG585's head and CFG531's esd_loo executed unedited; raw lensing; no LCDM ingredient.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg669.py ; CFG669_MUTATE=1 CFG669_M=M1|M2 -> _MUTATE outputs, exit 1 iff the tooth bites."""
import os, io, json, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); ROOT = os.path.dirname(LANES)
MUT = os.environ.get("CFG669_MUTATE", "0") == "1"; MODE = os.environ.get("CFG669_M", "") if MUT else ""
TAG = f"_MUTATE{MODE}" if MUT else ""
OUT, RES = [], {"lane": "CFG669", "criteria": "c42424774", "mutate": MUT, "mode": MODE}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


for v in ("CFG585_MUTATE", "CFG531_MUTATE"):
    os.environ.pop(v, None)
path = os.path.join(LANES, "CFG585_age_settling", "cfg585_age.py")
ns = {"__file__": path, "__name__": "head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(path).read().split('P("=" * 100)')[0], path, "exec"), ns)
U, F30, TYP, LMSL, esd_loo, NPATCH = (ns[k] for k in ("U", "F30", "TYP", "LMSL", "esd_loo", "NPATCH"))
Lp, o, ix = ns["Lp"], ns["o"], ns["ix"]
G = esd_loo.__globals__
WG0, WW0 = G["WG"].copy(), G["WW"].copy()
LT = np.load(os.path.join(ROOT, "real_research", "data", "lensing_rar", "lr_lenses.npz"))
LMG = np.log10(LT["Mgal"].astype(float)); FC = LT["Mgal"] / 10 ** LT["logM"] - 1
K9 = list(range(6, 15)); KIN = list(range(9, 15))
col = lambda name: np.array(Lp[name], "f8")[o[ix]]
gabs, iabs, kabs = col("MAG_ABS_g"), col("MAG_ABS_i"), col("MAG_ABS_Ks")
LMT = -0.68 + 0.70 * (gabs - iabs) + 0.4 * (4.58 - iabs)
LK = 0.4 * (5.08 - kabs)
cK = float(np.median(LMSL[F30]) - np.median(LK[F30]))
LMK = LK + cK


def fcold_rel():
    rel = {}
    for ty in (0, 1):
        m = TYP == ty
        edges = np.arange(np.floor(LT["logM"][m].min() * 10) / 10, LT["logM"][m].max() + 0.1, 0.1)
        cen, med = [], []
        for a, b in zip(edges[:-1], edges[1:]):
            s = m & (LT["logM"] >= a) & (LT["logM"] < b)
            if s.sum() >= 20:
                cen.append(0.5 * (a + b)); med.append(np.median(FC[s]))
        rel[ty] = (np.array(cen), np.array(med))
    return rel


REL = fcold_rel()


def baryonic(lms):
    out = np.full(len(TYP), np.nan)
    for ty in (0, 1):
        m = TYP == ty
        out[m] = lms[m] + np.log10(1 + np.interp(lms[m], *REL[ty]))
    return out


EST = {"L": (LMSL, LMG), "T": (LMT, baryonic(LMT)), "K": (LMK, baryonic(LMK))}
fin = np.all([np.isfinite(v[0]) & np.isfinite(v[1]) for v in EST.values()], axis=0)
C = F30 & (TYP == 1) & fin; E = C; Lt = F30 & (TYP == 0) & fin
dall, Call, _ = esd_loo(F30 & fin)
W = 1.0 / np.diag(Call)


def k9(ma, mb, ra=None, rb=None, boost_a=1.0):
    r = np.ones(len(TYP))
    if ra is not None:
        r = ra
    G["WG"] = WG0 * r[:, None]; G["WW"] = WW0 * r[:, None]
    if boost_a != 1.0:
        G["WG"][ma] *= boost_a
    da, _, La = esd_loo(ma); db, _, Lb = esd_loo(mb)
    G["WG"], G["WW"] = WG0.copy(), WW0.copy()
    out = {}
    for nm, ks in (("K9", K9), ("inner", KIN)):
        a = math.log10((W[ks] @ da[ks]) / (W[ks] @ db[ks]))
        al = np.log10((La[:, ks] @ W[ks]) / (Lb[:, ks] @ W[ks]))
        out[nm] = (a, math.sqrt((NPATCH - 1) / NPATCH * ((al - al.mean()) ** 2).sum()))
    return out


def t1(lms):
    qb = np.quantile(lms[C], np.linspace(0, 1, 11)); qb[-1] += 1e-9
    ter = np.full(len(U), -1)
    for i in range(10):
        idx = np.where(C & (lms >= qb[i]) & (lms < qb[i + 1]))[0]
        dc = U[idx] - np.median(U[idx]); od = np.argsort(dc, kind="stable"); n = len(idx)
        for k in range(3):
            ter[idx[od[k * n // 3:(k + 1) * n // 3]]] = k
    young, old = (ter == 0) & C, (ter == 2) & C
    return old, young


def t2(lmb, shuffle=False):
    rng = np.random.default_rng(669)
    qb = np.quantile(lmb[E], np.linspace(0, 1, 41)); qb[-1] += 1e-9
    r = np.zeros(len(TYP)); em = np.zeros(len(TYP), bool); lm = np.zeros(len(TYP), bool); offs = []
    for i in range(40):
        be = E & (lmb >= qb[i]) & (lmb < qb[i + 1]); bl = Lt & (lmb >= qb[i]) & (lmb < qb[i + 1])
        if shuffle:
            both = np.where(be | bl)[0]; lab = rng.permutation(np.r_[np.ones(be.sum(), bool), np.zeros(bl.sum(), bool)])
            be = np.zeros(len(TYP), bool); bl = np.zeros(len(TYP), bool); be[both[lab]] = True; bl[both[~lab]] = True
        if be.sum() < 100 or bl.sum() < 100:
            continue
        em |= be; lm |= bl; r[be] = 1.0; r[bl] = be.sum() / bl.sum()
        offs.append(float(np.median(lmb[be]) - np.median(lmb[bl])))
    return em, lm, r, offs


P(f"CFG669  near-IR (Ks) stellar-mass re-score  {('MUTATE ' + MODE) if MUT else 'PRIMARY'};  global constant c_K = {cK:+.4f}")
T1, T2 = {}, {}
for nm, (lms, lmb) in EST.items():
    old, young = t1(lms)
    a1 = k9(old, young, boost_a=(0.8 if (MODE == "M2" and nm == "K") else 1.0))
    T1[nm] = dict(K9=a1["K9"], inner=a1["inner"], d_old_young_vs_L=float(np.median((lms - LMSL)[old]) - np.median((lms - LMSL)[young])))
    em, lm, r, offs = t2(lmb, shuffle=(MODE == "M1" and nm == "K"))
    a2 = k9(em, lm, ra=r)
    T2[nm] = dict(K9=a2["K9"], inner=a2["inner"], n_bins=len(offs), mean_off=float(np.mean(offs)), max_off=float(np.max(np.abs(offs))),
                  d_early_late_vs_L=float(np.median((lms - LMSL)[E]) - np.median((lms - LMSL)[Lt])))
    P(f"\n[{nm}] T1 age (OLD/YOUNG, early): K9 {a1['K9'][0]:+.4f} +- {a1['K9'][1]:.4f} (Z {a1['K9'][0] / a1['K9'][1]:+.2f}); "
      f"inner {a1['inner'][0]:+.4f} +- {a1['inner'][1]:.4f};  median(logM_X - logM_L) OLD-YOUNG {T1[nm]['d_old_young_vs_L']:+.4f}")
    P(f"     T2 early/late at matched M_b: K9 {a2['K9'][0]:+.4f} +- {a2['K9'][1]:.4f} (Z {a2['K9'][0] / a2['K9'][1]:+.2f}); "
      f"inner {a2['inner'][0]:+.4f} +- {a2['inner'][1]:.4f};  bins {len(offs)}, mean offset {np.mean(offs):+.4f}, max {np.max(np.abs(offs)):.4f};  "
      f"median(logM_X - logM_L) early-late {T2[nm]['d_early_late_vs_L']:+.4f}")

aK, sK = T1["K"]["K9"]
c1 = "M* BIAS EXPLAINS" if (aK <= 0.05 and abs(aK / sK) < 1) else ("SIGNAL PERSISTS" if (aK >= 0.12 and aK / sK >= 2) else "PARTIAL")
bK, sbK = T2["K"]["K9"]
c2 = "EXCESS NOT SIGNIFICANT" if bK < 2 * sbK else ("EXCESS PERSISTS" if (bK >= 0.15 and bK / sbK >= 3) else "INTERMEDIATE")
if abs(T2["K"]["mean_off"]) > 0.01:
    c2 = "NOT CLEAN (" + c2 + ")"
robust = all(T1[n]["K9"][0] / T1[n]["K9"][1] >= 2 and T2[n]["K9"][0] / T2[n]["K9"][1] >= 2 for n in EST)
notrob = (aK / sK < 2) or (bK / sbK < 2)
comb = "ESTIMATOR-ROBUST" if robust else ("NOT ROBUST" if notrob else "MIXED")
RES.update(c_K=cK, T1={k: {kk: (list(vv) if isinstance(vv, tuple) else vv) for kk, vv in v.items()} for k, v in T1.items()},
           T2={k: {kk: (list(vv) if isinstance(vv, tuple) else vv) for kk, vv in v.items()} for k, v in T2.items()})
rc = 0
if MUT:
    if MODE == "M1":
        bite = abs(bK) < 2 * sbK
    else:
        J = json.load(open(os.path.join(HERE, "cfg669_results.json")))
        bite = abs((aK - J["T1"]["K"]["K9"][0]) - math.log10(0.8)) <= 0.002
    RES["tooth_bites"] = bool(bite); P(f"\nMUTATE {MODE}: tooth bites {bite}"); rc = 1 if bite else 0
else:
    RES.update(T1_class=c1, T2_class=c2, combined=comb)
    P(f"\nT1 (Ks): {c1};  T2 (Ks): {c2};  COMBINED: {comb}")
json.dump(RES, open(os.path.join(HERE, f"cfg669_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg669{TAG}.out"), "w").write("\n".join(OUT) + "\n")
raise SystemExit(rc)
