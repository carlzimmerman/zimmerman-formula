#!/usr/bin/env python3
"""CFG927 survey noise models (FROZEN_CRITERIA.md section 5, commit 8791d53c3): flat-sky Hu & Okamoto (2002) quadratic-estimator
reconstruction noise N_L^phiphi (TT, TE, EE, EB, TB; MV = 1/sum(1/N_XY)) for declared white-noise + Gaussian-beam survey models, on the
on-disk FFP10 lensed CMB spectra.  K4 (numerical convergence), K5 (analytic flat-spectrum identity), K7 (reported noise anchors).

    OMP_NUM_THREADS=1 nice -n 10 python3 cfg927_noise.py          (-> cfg927_noise.out/json)
One process, numpy only, < 1 GB.  kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import os, sys, json, math, time, hashlib
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(CFG, "CFG917_cmb_lensing_gate"))
import cfg917_lib as LB                                    # read-only: PR4 data paths, FFP10 PP loader

OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
CHECKS = {}
def check(name, desc, ok, detail="", gating=True):
    CHECKS[name] = dict(desc=desc, ok=bool(ok), detail=detail, gating=gating)
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if gating else ' (reported)'} {name}: {desc} -- {detail}")
sha = lambda f: hashlib.sha256(open(f, "rb").read()).hexdigest()

LMAXF = 3000                                               # forecast L range top (FROZEN section 3)
LNODES = np.geomspace(2.0, float(LMAXF), 64)               # 64 log-spaced L nodes (FROZEN section 5)
ARCMIN = math.pi / 10800.0

# ------------------------------------------------------------------ FFP10 lensed CMB spectra (D_l in muK^2 -> C_l)
FLC = os.path.join(LB.PR4D, "FFP10_wdipole_lensedCls.dat")
t = np.loadtxt(FLC); lc = t[:, 0]; LCMAX = int(lc.max())
LL = np.arange(LCMAX + 1, dtype=float)
def _cl(col):
    a = np.zeros(LCMAX + 1); fac = 2 * math.pi / (lc * (lc + 1)); a[lc.astype(int)] = t[:, col] * fac
    return a
CTT, CEE, CBB, CTE = _cl(1), _cl(2), _cl(3), _cl(4)

def white(l, dT, fwhm):
    th = fwhm * ARCMIN
    return (dT * ARCMIN) ** 2 * np.exp(l * (l + 1) * th ** 2 / (8 * math.log(2)))

def spectra(cfg, flat=False):
    """response (r*) and total (t*) spectra on integer l.  flat=True: the K5 identity (C^TT = 1, no noise)."""
    if flat:
        one = np.ones_like(LL); z = np.zeros_like(LL)
        return dict(rTT=one, rEE=z, rTE=z, rBB=z, tTT=one, tEE=one, tBB=one)
    nT = white(LL, cfg["dT"], cfg["fwhm"]); nP = white(LL, math.sqrt(2) * cfg["dT"], cfg["fwhm"])
    return dict(rTT=CTT, rEE=CEE, rTE=CTE, rBB=np.zeros_like(LL), tTT=CTT + nT, tEE=CEE + nP, tBB=CBB + nP)

EST = ("TT", "TE", "EE", "EB", "TB")
def ho_inv(L, cfg, S, dl=4.0, nphi=256, ests=EST, chunk=160):
    """integrals I_XY(L) = int d^2 l1/(2pi)^2 f_XY F_XY, so N_XY = 1/I_XY (flat sky, L along x, phi in [0, pi] doubled)."""
    lmin, lT, lP = cfg["lmin"], cfg["lmaxT"], cfg["lmaxP"]
    ltop = max(lT, lP if any(e != "TT" for e in ests) else lT)
    l1all = np.arange(lmin + dl / 2, ltop, dl)
    phi = (np.arange(nphi) + 0.5) * math.pi / nphi; c, s = np.cos(phi), np.sin(phi)
    I = {e: 0.0 for e in ests}
    for i0 in range(0, len(l1all), chunk):
        l1c = l1all[i0:i0 + chunk]; l1 = l1c[:, None]
        l1x = l1 * c[None, :]; l1y = l1 * s[None, :]
        l2x = L - l1x; l2y = -l1y; l2 = np.sqrt(l2x ** 2 + l2y ** 2)
        Ld1 = L * l1x; Ld2 = L * l2x
        d = phi[None, :] - np.arctan2(l2y, l2x); c2 = np.cos(2 * d); s2 = np.sin(2 * d)
        w = l1 * dl * (math.pi / nphi) * 2.0 / (2 * math.pi) ** 2
        a1 = lambda k: np.interp(l1c, LL, S[k])[:, None]
        a2 = lambda k: np.interp(l2, LL, S[k])
        mT1 = ((l1 >= lmin) & (l1 <= lT)).astype(float); mP1 = ((l1 >= lmin) & (l1 <= lP)).astype(float)
        mT2 = ((l2 >= lmin) & (l2 <= lT)).astype(float); mP2 = ((l2 >= lmin) & (l2 <= lP)).astype(float)
        if "TT" in ests:
            f = a1("rTT") * Ld1 + a2("rTT") * Ld2
            I["TT"] += float((w * f * f / (2 * a1("tTT") * a2("tTT")) * mT1 * mT2).sum())
        if "TE" in ests:
            f = a1("rTE") * c2 * Ld1 + a2("rTE") * Ld2
            I["TE"] += float((w * f * f / (a1("tTT") * a2("tEE")) * mT1 * mP2).sum())
        if "EE" in ests:
            f = (a1("rEE") * Ld1 + a2("rEE") * Ld2) * c2
            I["EE"] += float((w * f * f / (2 * a1("tEE") * a2("tEE")) * mP1 * mP2).sum())
        if "EB" in ests:
            f = (a1("rEE") * Ld1 - a2("rBB") * Ld2) * s2
            I["EB"] += float((w * f * f / (a1("tEE") * a2("tBB")) * mP1 * mP2).sum())
        if "TB" in ests:
            f = a1("rTE") * s2 * Ld1
            I["TB"] += float((w * f * f / (a1("tTT") * a2("tBB")) * mT1 * mP2).sum())
    return I

def nl_curve(cfg, dl=4.0, nphi=256):
    S = spectra(cfg)
    Inodes = {e: [] for e in EST}
    for L in LNODES:
        I = ho_inv(L, cfg, S, dl=dl, nphi=nphi)
        for e in EST: Inodes[e].append(I[e])
    Inodes = {e: np.array(v) for e, v in Inodes.items()}
    Imv = sum(Inodes.values()); Nmv_nodes = 1.0 / Imv
    Lint = np.arange(2, LMAXF + 1, dtype=float)
    Nphi = np.exp(np.interp(np.log(Lint), np.log(LNODES), np.log(Nmv_nodes)))
    NX = np.zeros(LMAXF + 1); NX[2:] = (Lint * (Lint + 1)) ** 2 * Nphi / (2 * math.pi)
    return dict(NX=NX, Nmv_nodes=Nmv_nodes, N_nodes={e: (1.0 / np.where(v > 0, v, np.nan)) for e, v in Inodes.items()})

# ------------------------------------------------------------------ declared survey models (FROZEN section 5)
MODELS = {
    "ACT-DR6-like": dict(dT=15.0, fwhm=1.4, lmin=600, lmaxT=3000, lmaxP=3000, fsky=0.25, Lmin=40,
                         provenance="L_min 40 and baseline 40-763 from on-disk files (CFG649, CFG363); dT, beam, CMB l range, f_sky ILLUSTRATIVE"),
    "SO-baseline-like": dict(dT=6.0, fwhm=1.4, lmin=30, lmaxT=3000, lmaxP=5000, fsky=0.40, Lmin=30,
                             provenance="f_sky 0.40 from on-disk quote (SO lensing map over 40% sky); the rest ILLUSTRATIVE"),
    "S4-like": dict(dT=1.0, fwhm=1.4, lmin=30, lmaxT=3000, lmaxP=5000, fsky=0.40, Lmin=30, provenance="all ILLUSTRATIVE round values"),
    "Planck-like-anchor": dict(dT=30.0, fwhm=5.0, lmin=100, lmaxT=2048, lmaxP=2048, fsky=0.65, Lmin=8, provenance="ILLUSTRATIVE; K7 only"),
}
SCAN = [20.0, 10.0, 6.0, 3.0, 2.0, 1.0, 0.5]
SCANBASE = dict(fwhm=1.4, lmin=30, lmaxT=3000, lmaxP=5000, fsky=0.40, Lmin=30)

P("CFG927 noise models (flat-sky Hu-Okamoto QE, MV of TT/TE/EE/EB/TB; FFP10 lensed spectra; C^BB = 0 in the response)")
P(f"  FFP10 lensed spectra {LB.rel(FLC)} sha256 {sha(FLC)[:16]}; L nodes 64 log-spaced in [2, {LMAXF}]")
cache = {}
def key(c): return (c["dT"], c["fwhm"], c["lmin"], c["lmaxT"], c["lmaxP"])
def get(c):
    k = key(c)
    if k not in cache: cache[k] = nl_curve(c)
    return cache[k]

RES = dict(lane="CFG927", part="noise", criteria_commit="8791d53c3",
           settings="kappa = 1/2 FITTED; footings never pooled; not theory closed; noise model only (no run data); FFP10 (LCDM) lensed CMB "
                    "spectra as the shared reference for both arms; survey parameters ILLUSTRATIVE unless marked",
           ffp10_lensed=dict(file=LB.rel(FLC), sha256=sha(FLC)[:16]), L_nodes=LNODES.tolist(), models={}, scan={})
for nm, c in MODELS.items():
    r = get(c)
    RES["models"][nm] = dict(params={k: v for k, v in c.items() if k != "provenance"}, provenance=c["provenance"], NX=r["NX"].tolist(),
                             Nmv_nodes=r["Nmv_nodes"].tolist(), N_nodes={e: v.tolist() for e, v in r["N_nodes"].items()})
    iL = [int(np.argmin(abs(LNODES - q))) for q in (10, 100, 400, 1000, 2000, 3000)]
    P(f"  {nm}: dT {c['dT']} uK', beam {c['fwhm']}', CMB l T {c['lmin']}-{c['lmaxT']} / P {c['lmin']}-{c['lmaxP']}, f_sky {c['fsky']}; "
      "N_MV^kk = L^4 N^pp/4 at L~" + ", ".join(f"{LNODES[i]:.0f}: {LNODES[i] ** 4 * r['Nmv_nodes'][i] / 4:.2e}" for i in iL))
for dT in SCAN:
    c = dict(SCANBASE, dT=dT); r = get(c)
    RES["scan"][f"{dT:g}"] = dict(params=c, NX=r["NX"].tolist(), Nmv_nodes=r["Nmv_nodes"].tolist())
P(f"  noise scan (f_sky 0.40, beam 1.4', T 30-3000, P 30-5000): dT = {SCAN} uK-arcmin computed; {len(cache)} distinct HO configurations")

# ------------------------------------------------------------------ K tests
P("\nK tests")
# K5 analytic flat-spectrum identity
cfg5 = dict(lmin=30, lmaxT=3000, lmaxP=3000); S5 = spectra(None, flat=True); k5 = {}
for L in (100.0, 1000.0, 2000.0):
    num = 1.0 / ho_inv(L, cfg5, S5, ests=("TT",))["TT"]
    R = 3000.0; lens = 2 * R * R * math.acos(L / (2 * R)) - (L / 2) * math.sqrt(4 * R * R - L * L); area = lens - 2 * math.pi * 30.0 ** 2
    ana = 8 * math.pi ** 2 / (L ** 4 * area); k5[f"{L:g}"] = dict(numeric=num, analytic=ana, rel=num / ana - 1)
dev5 = max(abs(v["rel"]) for v in k5.values())
check("K5", "flat C^TT on [30, 3000], no noise, TT: N_L = 8 pi^2/(L^4 Area) at L 100/1000/2000 (<= 0.5%)", dev5 <= 0.005,
      ", ".join(f"L {k}: {v['rel']:+.2e}" for k, v in k5.items()))
RES["K5"] = k5
# K4 numerical convergence (halved dl, doubled angles)
k4 = {}
for nm, c in list(MODELS.items()) + [("scan 0.5", dict(SCANBASE, dT=0.5))]:
    base = get(c)["Nmv_nodes"]; S = spectra(c)
    fine = np.array([1.0 / sum(ho_inv(L, c, S, dl=2.0, nphi=512).values()) for L in LNODES])
    k4[nm] = float(np.max(np.abs(fine / base - 1)))
dev4 = max(k4.values())
check("K4", "halving dl and doubling the angle count changes N_L^MV by <= 1% at every L node (5 models)", dev4 <= 0.01,
      ", ".join(f"{k} {v:.1e}" for k, v in k4.items()))
RES["K4"] = k4
# K7 reported anchors: Fisher sigma(A) on FFP10 PP vs on-disk published amplitude errors
_tp = np.loadtxt(os.path.join(LB.PR4D, "FFP10_wdipole_lenspotentialCls.dat"))      # same file and PP column as LB.load_ffp10, to L 3000
XFFP = np.zeros(LMAXF + 1); _m = _tp[:, 0].astype(int) <= LMAXF; XFFP[_tp[_m, 0].astype(int)] = _tp[_m, 5]
assert np.array_equal(XFFP[:2501], LB.load_ffp10())
def sigA(nm, lo, hi):
    c = MODELS[nm]; NX = np.array(RES["models"][nm]["NX"]); L = np.arange(lo, hi + 1)
    return float((c["fsky"] * ((2 * L + 1) / 2 * XFFP[L] ** 2 / (XFFP[L] + NX[L]) ** 2).sum()) ** -0.5)
k7 = {}
for nm, lo, hi, pub in (("Planck-like-anchor", 8, 400, 0.028), ("ACT-DR6-like", 40, 763, 0.023)):
    s_ = sigA(nm, lo, hi); k7[nm] = dict(L=[lo, hi], sigma_A_forecast=s_, sigma_A_published_on_disk=pub, ratio=s_ / pub,
                                         anchored=bool(0.5 <= s_ / pub <= 2.0))
check("K7", "noise anchors: Fisher sigma(A) on FFP10 PP vs on-disk published (Planck 8-400 0.028; ACT DR6 40-763 0.023); flag outside [0.5, 2]",
      True, "; ".join(f"{k}: {v['sigma_A_forecast']:.4f} vs {v['sigma_A_published_on_disk']} (ratio {v['ratio']:.2f}, "
                      f"{'anchored' if v['anchored'] else 'UNANCHORED'})" for k, v in k7.items()), gating=False)
for nm in ("SO-baseline-like", "S4-like"):
    k7[nm] = dict(L=[30, 3000], sigma_A_forecast=sigA(nm, 30, 3000), note="no on-disk published value; context")
P("  context: Fisher sigma(A) on FFP10 PP over 30-3000: " + ", ".join(f"{nm} {k7[nm]['sigma_A_forecast']:.4f}" for nm in ("SO-baseline-like", "S4-like")))
RES["K7"] = k7
RES["checks"] = CHECKS; RES["all_gating_pass"] = all(v["ok"] for v in CHECKS.values() if v["gating"])
RES["runtime_s"] = time.time() - T0
try:
    import resource; RES["maxrss_gb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
except Exception:
    pass
P(f"\nall gating K pass: {RES['all_gating_pass']}; runtime {RES['runtime_s']:.0f} s; maxrss {RES.get('maxrss_gb', 0):.2f} GB. "
  "kappa = 1/2 FITTED; footings never pooled; not theory closed.")
json.dump(RES, open(os.path.join(HERE, "cfg927_noise.json"), "w"))
open(os.path.join(HERE, "cfg927_noise.out"), "w").write("\n".join(OUT) + "\n")
