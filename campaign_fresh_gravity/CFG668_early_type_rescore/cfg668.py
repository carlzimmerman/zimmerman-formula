#!/usr/bin/env python3
"""CFG668 (FROZEN_CRITERIA.md, 2352c8767): is the KiDS early-type excess a stellar-mass artefact?  Morphology-blind test on raw
lensing: early vs late at matched baryonic mass, LePhare (table Mgal) vs Taylor+11 (M*_T (1 + per-type f_cold(M*_T))).
CFG585's head and CFG531's esd_loo executed unedited.  No LCDM ingredient; CFG529/531 epsilon not used.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg668.py ; CFG668_MUTATE=1 CFG668_M=M1|M2 -> _MUTATE outputs, exit 1 iff the tooth bites."""
import os, io, json, math, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); ROOT = os.path.dirname(LANES)
MUT = os.environ.get("CFG668_MUTATE", "0") == "1"; MODE = os.environ.get("CFG668_M", "") if MUT else ""
TAG = f"_MUTATE{MODE}" if MUT else ""
OUT, RES = [], {"lane": "CFG668", "criteria": "2352c8767", "mutate": MUT, "mode": MODE}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


for v in ("CFG585_MUTATE", "CFG531_MUTATE"):
    os.environ.pop(v, None)
path = os.path.join(LANES, "CFG585_age_settling", "cfg585_age.py")
ns = {"__file__": path, "__name__": "head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(path).read().split('P("=" * 100)')[0], path, "exec"), ns)
F30, TYP, LMSL, esd_loo, NPATCH = (ns[k] for k in ("F30", "TYP", "LMSL", "esd_loo", "NPATCH"))
Lp, o, ix = ns["Lp"], ns["o"], ns["ix"]
G = esd_loo.__globals__
WG0, WW0 = G["WG"].copy(), G["WW"].copy()
LT = np.load(os.path.join(ROOT, "real_research", "data", "lensing_rar", "lr_lenses.npz"))
assert len(LT["logM"]) == len(TYP)
LMG = np.log10(LT["Mgal"].astype(float))
FC = LT["Mgal"] / 10 ** LT["logM"] - 1
K9 = list(range(6, 15)); KIN = list(range(9, 15))

# Taylor+11 masses and per-type f_cold relation
gabs = np.array(Lp["MAG_ABS_g"], "f8")[o[ix]]; iabs = np.array(Lp["MAG_ABS_i"], "f8")[o[ix]]
LMT = -0.68 + 0.70 * (gabs - iabs) + 0.4 * (4.58 - iabs)
LMBT = np.full(len(TYP), np.nan)
for ty in (0, 1):
    m = TYP == ty
    edges = np.arange(np.floor(LT["logM"][m].min() * 10) / 10, LT["logM"][m].max() + 0.1, 0.1)
    cen, med = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        s = m & (LT["logM"] >= a) & (LT["logM"] < b)
        if s.sum() >= 20:
            cen.append(0.5 * (a + b)); med.append(np.median(FC[s]))
    fc_t = np.interp(LMT[m], cen, med)                     # clamped at the ends by np.interp
    LMBT[m] = LMT[m] + np.log10(1 + fc_t)
fin = np.isfinite(LMBT) & np.isfinite(LMG)
E = F30 & (TYP == 1) & fin; Lt = F30 & (TYP == 0) & fin
dall, Call, _ = esd_loo(F30 & fin)
W = 1.0 / np.diag(Call)


def matched(lmb, rng=None):
    """returns (early mask, late mask, per-lens weight factor r, bin info)."""
    qb = np.quantile(lmb[E], np.linspace(0, 1, 11)); qb[-1] += 1e-9
    r = np.zeros(len(TYP)); emask = np.zeros(len(TYP), bool); lmask = np.zeros(len(TYP), bool); info = []
    for i in range(10):
        be = E & (lmb >= qb[i]) & (lmb < qb[i + 1]); bl = Lt & (lmb >= qb[i]) & (lmb < qb[i + 1])
        if rng is not None:                                   # M1: shuffle labels within the bin
            both = np.where(be | bl)[0]; lab = np.r_[np.ones(be.sum(), bool), np.zeros(bl.sum(), bool)]
            lab = rng.permutation(lab); be = np.zeros(len(TYP), bool); bl = np.zeros(len(TYP), bool)
            be[both[lab]] = True; bl[both[~lab]] = True
        nE, nL = int(be.sum()), int(bl.sum())
        if nE < 300 or nL < 300:
            info.append(dict(bin=i, nE=nE, nL=nL, dropped=True)); continue
        emask |= be; lmask |= bl; r[be] = 1.0; r[bl] = nE / nL
        info.append(dict(bin=i, nE=nE, nL=nL, dropped=False, med_E=float(np.median(lmb[be])), med_L=float(np.median(lmb[bl]))))
    return emask, lmask, r, info


def amp(emask, lmask, r, eboost=1.0):
    G["WG"] = WG0 * r[:, None]; G["WW"] = WW0 * r[:, None]
    if eboost != 1.0:
        G["WG"][emask] *= eboost
    de, _, Le = esd_loo(emask); dl, _, Ll = esd_loo(lmask)
    G["WG"], G["WW"] = WG0.copy(), WW0.copy()
    out = {}
    for nm, ks in (("K9", K9), ("Kin+mid", KIN)):
        a = math.log10((W[ks] @ de[ks]) / (W[ks] @ dl[ks]))
        al = np.log10((Le[:, ks] @ W[ks]) / (Ll[:, ks] @ W[ks]))
        out[nm] = dict(A=a, loo=al, s=math.sqrt((NPATCH - 1) / NPATCH * ((al - al.mean()) ** 2).sum()))
    return out


P(f"CFG668  early-type excess, morphology-blind re-score (raw lensing)  {('MUTATE ' + MODE) if MUT else 'PRIMARY'}")
RESX = {}
for nm, lmb in (("L", LMG), ("T", LMBT)):
    rng = np.random.default_rng(668) if MODE == "M1" else None
    em, lm_, r, info = matched(lmb, rng)
    a = amp(em, lm_, r, eboost=(0.8 if MODE == "M2" else 1.0))
    RESX[nm] = dict(amp={k: dict(A=v["A"], s=v["s"]) for k, v in a.items()}, info=info, _loo={k: v["loo"] for k, v in a.items()})
    mx = max((abs(b["med_E"] - b["med_L"]) for b in info if not b["dropped"]), default=float("nan"))
    P(f"\n[{nm}] bins used {sum(not b['dropped'] for b in info)}/10; N early {int(em.sum())}, late {int(lm_.sum())}; "
      f"max |median log M_b early - late| per bin {mx:.4f}")
    for k, v in a.items():
        P(f"   {k:8s} A_{nm} = {v['A']:+.4f} +- {v['s']:.4f}  (Z {v['A'] / v['s']:+.2f})")
D = {}
for k in ("K9", "Kin+mid"):
    dl = RESX["L"]["_loo"][k] - RESX["T"]["_loo"][k]
    d = RESX["L"]["amp"][k]["A"] - RESX["T"]["amp"][k]["A"]
    sd = math.sqrt((NPATCH - 1) / NPATCH * ((dl - dl.mean()) ** 2).sum())
    D[k] = dict(delta=d, s=sd)
    P(f"Delta (A_L - A_T) {k}: {d:+.4f} +- {sd:.4f} (paired jackknife)")
offs = float(np.median((LMT - LMSL)[E]) - np.median((LMT - LMSL)[Lt]))
P(f"median (log M*_T - log M*_L): early minus late = {offs:+.4f} dex")
AT, sT = RESX["T"]["amp"]["K9"]["A"], RESX["T"]["amp"]["K9"]["s"]
if abs(AT) < 2 * sT and D["K9"]["delta"] >= 0.10:
    lab = "ARTEFACT EXPLAINS THE EXCESS"
elif AT >= 0.15 and AT / sT >= 3:
    lab = "EXCESS PERSISTS"
else:
    lab = "PARTIAL"
for v in RESX.values():
    v.pop("_loo")
RES.update(X=RESX, delta=D, early_minus_late_T_minus_L=offs)
rc = 0
if MUT:
    if MODE == "M1":
        bite = abs(RESX["L"]["amp"]["K9"]["A"]) < 2 * RESX["L"]["amp"]["K9"]["s"]
    else:
        J = json.load(open(os.path.join(HERE, "cfg668_results.json")))
        bite = abs((RESX["L"]["amp"]["K9"]["A"] - J["X"]["L"]["amp"]["K9"]["A"]) - math.log10(0.8)) <= 0.002
    RES["tooth_bites"] = bool(bite); P(f"\nMUTATE {MODE}: tooth bites: {bite}"); rc = 1 if bite else 0
else:
    RES["label"] = lab; P(f"\nLABEL (K9): {lab}")
json.dump(RES, open(os.path.join(HERE, f"cfg668_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg668{TAG}.out"), "w").write("\n".join(OUT) + "\n")
raise SystemExit(rc)
