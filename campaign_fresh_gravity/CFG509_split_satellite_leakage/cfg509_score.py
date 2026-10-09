#!/usr/bin/env python3
"""CFG509 lensing re-score (FROZEN_CRITERIA.md, dfc467df4): the early/late split with CLASS-DEPENDENT satellite leakage.

Machinery read-only: CFG261's L-law cell tables via CFG505's prefix loader (copied here, not edited), CFG505's re-staged per-lens
sums and mass sets, CFG503's environment table E_moster_nlz_W10 decomposed as E = A + f_W B (A = hole + centrals' two-halo,
B = leaked-satellite host term per unit leaked fraction), mapped to g_bar bins with cfg495_lenslib.finish (CFG505 R3 verbatim).
Class leakage: E_c = A + lambda_c f_W B, with lambda_c from the photometric companion counts (cfg509_counts_results.json).
Settings: L-none (E = 0), L-cb (lambda 1/1), L-f0 (lambda 0), L-meas (HEADLINE), L-match, L-unw, L-2sd, L-lit (LCDM-calibrated,
flagged), stripping of the leaked fraction's own law profile (tfac 0.066), and a lambda_early scan (diagnostic).
MUTATE (CFG509_MUTATE=1, outputs *_MUTATE.*): MU1 swapped lambdas; MU0 zero leakage.
Run: nice -n 15 python3 -u cfg509_score.py ; CFG509_MUTATE=1 nice -n 15 python3 -u cfg509_score.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import io, json, math, time, shutil, contextlib
import numpy as np
from scipy.stats import chi2 as CHI2, norm
from scipy.interpolate import RegularGridInterpolator

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
EXT = os.path.abspath(os.path.join(REPO, "..", "_external_data"))
W505 = os.path.join(EXT, "cfg505_work")
WORK = os.path.join(EXT, "cfg509_work"); os.makedirs(WORK, exist_ok=True)
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
MUTATE = os.environ.get("CFG509_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
LOG, CHK, RES = [], {}, {"lane": "CFG509", "script": "cfg509_score", "mutate": MUTATE}
FOOTS = ("canonical", "alt")
TF_STRIP = 0.066


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


def zs(p):
    return float(norm.isf(p / 2)) if p > 0 else float("inf")


# ------------------------------------------------------------------ CFG261 prefix (CFG505's loader, verbatim logic), own cache
C261 = os.path.join(LANES, "CFG261_kids_absolute_a0_zthirds")
CACHE = os.path.join(WORK, "cache261"); os.makedirs(CACHE, exist_ok=True)
for fn in os.listdir(os.path.join(C261, "_cache")):
    if "eps+0.00000_gasf+1.00000_kernmono_shift+0.00000_tfac+0.40000" in fn and not os.path.exists(os.path.join(CACHE, fn)):
        shutil.copy2(os.path.join(C261, "_cache", fn), os.path.join(CACHE, fn))
_env = {k: os.environ.get(k) for k in ("STAGE", "MUTATE", "SELFTEST", "CFG261_CACHE")}
os.environ.update(STAGE="B", MUTATE="0", SELFTEST="0", CFG261_CACHE=CACHE)
src = open(os.path.join(C261, "cfg261_kids_abs.py")).read()
g = {"__file__": os.path.join(C261, "cfg261_kids_abs.py"), "__name__": "lane_cfg261"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("\n# ------------------------------------------------------------------ the data actually used")], "cfg261", "exec"), g)
for k, v in _env.items():
    os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
tables, cells, build_cells, LSN, Model = g["tables"], g["cells"], g["build_cells"], g["LSN"], g["Model"]
nodes_for, LMG, ZGL, K1, NPAT, KG, patch, H12 = g["nodes_for"], g["LMG"], g["ZG"], g["K1"], g["NPAT"], g["KG"], g["patch"], g["H12"]
A0C, A0A = g["A0C"], g["A0A"]
nA, nB = len(LMG), len(ZGL)
LS_ALT = math.log10(A0A / A0C)
TB = tables("base")
I0 = int(np.argmin(np.abs(LSN)))
P(f"CFG509 score MUTATE={int(MUTATE)}; CFG261 prefix loaded ({time.time() - T0:.0f} s); K1 = {K1}; alt at log s = {LS_ALT:.5f}")

# ------------------------------------------------------------------ lenses, mass sets, per-lens sums (CFG505's files, read-only)
ln = np.load(os.path.join(DATA, "lr_lenses.npz"))
typ0, zl = ln["typ"].astype(int), ln["z"].astype(float)
NL = len(typ0)
MS = np.load(os.path.join(W505, "cfg505_masses.npz"))
SETS = ["M0"] if MUTATE else ["M0", "M2"]
PL = {s: np.load(os.path.join(W505, f"cfg505_perlens_{s}.npz")) for s in SETS}
iz = np.clip(np.round((zl - 0.05) / 0.10).astype(int), 0, nB - 1)


class MassSet:
    def __init__(self, name):
        self.name = name
        self.lm = MS["logM_" + name].astype(float); self.Mg = MS["Mgal_" + name].astype(float)
        self.im = np.clip(np.round((self.lm - LMG[0]) / 0.05).astype(int), 0, nA - 1)
        self.WG, self.WW = PL[name]["WG"], PL[name]["WW"]

    def cellw(self, mask, extra=None):
        w = np.zeros((nA, nB)); np.add.at(w, (self.im[mask], iz[mask]), self.Mg[mask] * (1.0 if extra is None else extra[mask])); return w

    def sums(self, mask, cols):
        pa = patch[mask]
        Sg = np.stack([np.bincount(pa, weights=self.WG[mask][:, k], minlength=NPAT) for k in cols], 1)
        Sw = np.stack([np.bincount(pa, weights=self.WW[mask][:, k], minlength=NPAT) for k in cols], 1)
        return Sg, Sw


def row_data(S, mask, cols):
    Sg, Sw = S.sums(mask, cols)
    tg, tw = Sg.sum(0), Sw.sum(0)
    d = tg / tw / KG; loo = (tg[None] - Sg) / (tw[None] - Sw) / KG
    R_ = loo - loo.mean(0); cov = (NPAT - 1) / NPAT * (R_.T @ R_)
    return d, loo, cov


def split_data(S, cols):
    dl, ll, _ = row_data(S, typ0 == 0, cols); de, le, _ = row_data(S, typ0 == 1, cols)
    D = de - dl; Dp = le - ll
    Rd = Dp - Dp.mean(0); CK = (NPAT - 1) / NPAT * (Rd.T @ Rd)
    return D, CK, dl, de


ALL15 = list(range(15)); INN9 = list(range(6, 15)); OUT6 = list(range(6))
SETB = {"K1": K1, "inner9": INN9}

# ------------------------------------------------------------------ law tables: base (spline on s-nodes, CFG505) + stripped (direct at s = 1 / alt)
base_alt = np.load(os.path.join(W505, "cache261", "r1_shift+0.000.npz"))["alt"]
t = time.time()
strip_can = cells(0.0, shift=0.0, kern="mono", tfac=TF_STRIP, gasf=1.0, eps=0.0)
pa = os.path.join(CACHE, f"alt_tfac{TF_STRIP:.3f}.npy")
if os.path.exists(pa):
    strip_alt = np.load(pa)
else:
    strip_alt = build_cells(LS_ALT, tfac=TF_STRIP); np.save(pa, strip_alt)
P(f"  stripped law tables ready ({time.time() - t:.0f} s)")
if not MUTATE:
    pr = os.path.join(CACHE, "rebuild_base_ls0.npy")
    if os.path.exists(pr):
        rb = np.load(pr)
    else:
        rb = build_cells(0.0); np.save(pr, rb)
    dv = float(np.max(np.abs(rb - TB[I0])))
    check("C4 build_cells(0, tfac 0.40) rebuilt here equals the cached CFG261 base table at s = 1", dv <= 1e-9, f"max |diff| {dv:.1e} Msun/pc^2")
STRIP = {"canonical": strip_can - TB[I0], "alt": strip_alt - base_alt}       # own-profile change of a stripped lens per cell

# ------------------------------------------------------------------ environment: CFG503 table, decomposition E = A + f_W B
sys.path.insert(0, os.path.join(LANES, "CFG495_drawdown_shell"))
import cfg495_lenslib as LL                                                    # noqa: E402 (read-only)
ET = np.load(os.path.join(EXT, "cfg503_work", "cfg503_env_table.npz"))
LMS, ZGE, RGE = ET["LMS"], ET["ZG"], ET["RG"]
fT = ET["moster_W10_f"]; fpT = ET["moster_W10_fpar"]
A_T = ET["moster_HOLE"] + ET["moster_W10_bc"][..., None] * ET["moster_S2H_nlz"]
B_T = (ET["E_moster_nlz_W10"] - A_T) / fT[..., None]
dmax = float(np.max(np.abs(A_T + fT[..., None] * B_T - ET["E_moster_nlz_W10"]) / (np.abs(ET["E_moster_nlz_W10"]) + 1e3)))
check("C3 A + f_W B reproduces CFG503's E_moster_nlz_W10 (relative, +1e3 Msun/Mpc^2 floor) to 1e-9", dmax <= 1e-9, f"{dmax:.1e}")
EI = {k: RegularGridInterpolator((LMS, ZGE), v, bounds_error=False, fill_value=None) for k, v in (("E", ET["E_moster_nlz_W10"]), ("A", A_T), ("fB", fT[..., None] * B_T))}
FI = RegularGridInterpolator((LMS, ZGE), fT, bounds_error=False, fill_value=None)
FPI = RegularGridInterpolator((LMS, ZGE), fpT, bounds_error=False, fill_value=None)


def env_perlens(S):
    """CFG505's env_perlens, for the three tables E, A and f_W B."""
    lmg = np.log10(S.Mg)
    key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(zl / 0.03).astype(np.int64)
    _, gi, cnt = np.unique(key, return_inverse=True, return_counts=True); gi = gi.ravel()
    GM = 10 ** (np.bincount(gi, weights=lmg) / cnt); GZ = np.bincount(gi, weights=zl) / cnt; GS = np.bincount(gi, weights=S.lm) / cnt
    X = np.c_[np.clip(GS, LMS[0], LMS[-1]), np.clip(GZ, ZGE[0], ZGE[-1])]
    LR = np.log(RGE); out = {}
    for k in ("E", "A", "fB"):
        Eg = EI[k](X)
        out[k] = np.array([LL.finish(lambda R, e=Eg[j]: np.interp(np.log(R), LR, e), GM[j]) for j in range(len(GM))])
    return gi, out


def pstack(gi, Etab, WW, mask, lam=None):
    NG = Etab.shape[0]; out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG)
        wn = w if lam is None else np.bincount(gi[mask], weights=(WW[:, k] * lam)[mask], minlength=NG)
        out[k] = (wn @ Etab[:, k]) / w.sum()
    return out


# ------------------------------------------------------------------ leakage settings
CJ = json.load(open(os.path.join(HERE, "cfg509_counts_results.json")))
cw, cu, cm = CJ["classes"]["stack_weighted"], CJ["classes"]["unweighted"], CJ["matched"]
LAM = {"L-none": None, "L-cb": (1.0, 1.0), "L-f0": (0.0, 0.0),
       "L-meas": (cw["late"]["lambda"], cw["early"]["lambda"]),
       "L-match": (cm["lambda_late"], cm["lambda_early"]),
       "L-unw": (cu["late"]["lambda"], cu["early"]["lambda"]),
       "L-2sd": (cw["late"]["lambda"] - 2 * cw["late"]["lambda_jk"], cw["early"]["lambda"] + 2 * cw["early"]["lambda_jk"])}
if MUTATE:
    LAM = {"L-none": None, "L-f0": (0.0, 0.0), "L-meas": LAM["L-meas"], "MU1-swap": (LAM["L-meas"][1], LAM["L-meas"][0])}


def lit_lambda(S):
    """L-lit: LCDM-calibrated colour-dependent parent satellite fractions (flagged); per-lens lambda = f_W,class / f_W."""
    X = np.c_[np.clip(S.lm, LMS[0], LMS[-1]), np.clip(zl, ZGE[0], ZGE[-1])]
    fw, fp = FI(X), FPI(X)
    rpc = fw * (1 - fp) / (fp * (1 - fw))                                    # P_s / P_c implied by CFG503's own f_W and f_par
    r = np.clip(2.0 - 0.6 * (S.lm - 10.0), 1.4, 2.0)
    # red share q of the ISO lenses in (log M* 0.25, z 0.05) cells
    kb = np.floor((S.lm - 8.5) / 0.25).astype(int) * 100 + np.floor((zl - 0.1) / 0.05).astype(int)
    _, inv = np.unique(kb, return_inverse=True); inv = inv.ravel()
    q = (np.bincount(inv, weights=(typ0 == 1).astype(float)) / np.bincount(inv))[inv]
    fb = fp / (q * r + 1 - q); fr = np.minimum(r * fb, 0.95)
    fpc = np.where(typ0 == 1, fr, fb)
    fwc = fpc * rpc / (fpc * rpc + 1 - fpc)
    return fwc / fw, fw


def score(S, D, CK, cols, Dm):
    r = D - Dm
    x2 = float(r @ np.linalg.solve(CK, r)) * H12(len(cols))
    p = float(CHI2.sf(x2, len(cols)))
    return dict(chi2=x2, p=p, sigma=zs(p))


RUN = {}
for sname in SETS:
    S = MassSet(sname)
    gi, ET_ = env_perlens(S)
    m0, m1 = typ0 == 0, typ0 == 1
    pA = {c: pstack(gi, ET_["A"], S.WW, m) for c, m in ((0, m0), (1, m1))}
    pB = {c: pstack(gi, ET_["fB"], S.WW, m) for c, m in ((0, m0), (1, m1))}
    pE = {c: pstack(gi, ET_["E"], S.WW, m) for c, m in ((0, m0), (1, m1))}
    lam_lit, fwl = lit_lambda(S)
    pBl = {c: pstack(gi, ET_["fB"], S.WW, m, lam=lam_lit) for c, m in ((0, m0), (1, m1))}
    X = np.c_[np.clip(S.lm, LMS[0], LMS[-1]), np.clip(zl, ZGE[0], ZGE[-1])]
    fw_l = FI(X)
    # law models
    ML = {c: Model(nodes_for(TB, S.cellw(m)), ALL15) for c, m in ((0, m0), (1, m1))}
    law = {f: {c: ML[c].at(0.0 if f == "canonical" else LS_ALT) for c in (0, 1)} for f in FOOTS}
    Dfull, CKfull, dl, de = split_data(S, ALL15)
    lit_w = {c: float((S.Mg * fw_l * lam_lit)[m].sum() / (S.Mg * fw_l)[m].sum()) for c, m in ((0, m0), (1, m1))}
    P(f"\n================ mass set {sname} ================")
    P(f"  class leaked fraction (stack-weighted f_W model): late {float((S.WW.sum(1) * fw_l)[m0].sum() / S.WW.sum(1)[m0].sum()):.3f}, "
      f"early {float((S.WW.sum(1) * fw_l)[m1].sum() / S.WW.sum(1)[m1].sum()):.3f}")
    P(f"  L-lit (LCDM-calibrated, flagged): Mg-weighted mean lambda late {lit_w[0]:.3f}, early {lit_w[1]:.3f}")
    # stripping correction per class (Mg-weighted, leaked fraction lambda f_W per lens)
    def strip_corr(lam, foot):
        out = {}
        for c, m in ((0, m0), (1, m1)):
            ex = lam[c] * fw_l
            if lam[c] == 0:                     # no leaked fraction -> no stripping (avoids 0/0 in nodes_for; first run printed inf)
                out[c] = np.zeros(15); continue
            out[c] =nodes_for(STRIP[foot][None], S.cellw(m, extra=ex))[0] * (S.cellw(m, extra=ex).sum() / S.cellw(m).sum())
        return out

    def env_c(lamset):
        if lamset is None:
            return {0: np.zeros(15), 1: np.zeros(15)}
        if lamset == "lit":
            return {c: pA[c] + pBl[c] for c in (0, 1)}
        return {c: pA[c] + lamset[c] * pB[c] for c in (0, 1)}

    R = {}
    settings = dict(LAM)
    if not MUTATE:
        settings["L-lit"] = "lit"
    for nm, ls_ in settings.items():
        Ec = env_c(ls_)
        R[nm] = {"E_late": Ec[0].tolist(), "E_early": Ec[1].tolist()}
        for foot in FOOTS:
            Dm = law[foot][1] - law[foot][0] + Ec[1] - Ec[0]
            R[nm][foot] = {}
            for bn, cols in SETB.items():
                D, CK, _, _ = split_data(S, cols)
                R[nm][foot][bn] = score(S, D, CK, cols, Dm[cols])
            R[nm][foot]["all15"] = score(S, Dfull, CKfull, ALL15, Dm)
            R[nm][foot]["Dmodel"] = Dm.tolist()
            # stripping variant (not for L-none)
            if ls_ is not None and ls_ != "lit":
                sc = strip_corr(ls_, foot)
                Dms = Dm + sc[1] - sc[0]
                R[nm][foot]["strip"] = {bn: score(S, *split_data(S, cols)[:2], cols, Dms[cols]) for bn, cols in SETB.items()}
                R[nm][foot]["strip_Dmodel"] = Dms.tolist()
        P(f"  [{nm:8s}] " + " | ".join(
            f"{f[:3]}: K1 {R[nm][f]['K1']['chi2']:.2f}/7 ({R[nm][f]['K1']['sigma']:.2f}s), in9 {R[nm][f]['inner9']['chi2']:.2f}/9 ({R[nm][f]['inner9']['sigma']:.2f}s)"
            + (f", strip K1 {R[nm][f]['strip']['K1']['sigma']:.2f}s in9 {R[nm][f]['strip']['inner9']['sigma']:.2f}s" if "strip" in R[nm][f] else "")
            for f in FOOTS))
    # per-bin table (all 15 bins) for the headline and L-none
    sdD = np.sqrt(np.diag(CKfull) / H12(15))
    P("  per bin (canonical; outer 6 = bins 0-5 reported only): bin | D | sd | model L-none | model L-cb | model L-meas | E_e-E_l (L-meas) | pull L-meas")
    hd = "L-meas"
    for k in range(15):
        P(f"    {k:2d} {'IN ' if k >= 6 else 'OUT'} {Dfull[k]:7.2f} {sdD[k]:6.2f}  {R['L-none']['canonical']['Dmodel'][k]:7.2f}  "
          + (f"{R['L-cb']['canonical']['Dmodel'][k]:7.2f}  " if 'L-cb' in R else "    -    ")
          + f"{R[hd]['canonical']['Dmodel'][k]:7.2f}  {R[hd]['E_early'][k] - R[hd]['E_late'][k]:7.3f}  "
          f"{(Dfull[k] - R[hd]['canonical']['Dmodel'][k]) / sdD[k]:+6.2f}")
    RUN[sname] = dict(settings=R, D=Dfull.tolist(), sdD=sdD.tolist(), lit_lambda_mean=lit_w)
    # ---------------- step 4: the law per class (absolute), with class leakage (reported)
    if not MUTATE:
        P("  law per class (absolute, s = 1, + E_c), chi2 on K1 / inner 9 / outer 6 (outer reported only):")
        ab = {}
        for nm in ("L-none", "L-cb", "L-meas"):
            Ec = env_c(LAM[nm]); ab[nm] = {}
            for c, m, cn in ((0, m0, "late"), (1, m1, "early")):
                d, _, cov = row_data(S, m, ALL15)
                ab[nm][cn] = {}
                for foot in FOOTS:
                    mod = law[foot][c] + Ec[c]; out = {}
                    for bn, cols in (("K1", K1), ("inner9", INN9), ("outer6", OUT6)):
                        rr = (d - mod)[cols]
                        out[bn] = float(rr @ np.linalg.solve(cov[np.ix_(cols, cols)], rr)) * H12(len(cols))
                    ab[nm][cn][foot] = out
                P(f"    [{nm:7s}] {cn:5s}: " + " | ".join(f"{f[:3]} K1 {ab[nm][cn][f]['K1']:.1f}/7 in9 {ab[nm][cn][f]['inner9']:.1f}/9 out6 {ab[nm][cn][f]['outer6']:.1f}/6" for f in FOOTS))
        RUN[sname]["absolute"] = ab
        # ---------------- diagnostic: lambda_early needed for < 2 sigma on K1 (lambda_late fixed at L-meas)
        if sname == "M0":
            lgrid = np.round(np.arange(0.0, 20.0001, 0.25), 2)
            scan = {}
            D7, CK7, _, _ = split_data(S, K1)
            for foot in FOOTS:
                xs = []
                for le in lgrid:
                    Dm = law[foot][1] - law[foot][0] + (pA[1] + le * pB[1]) - (pA[0] + LAM["L-meas"][0] * pB[0])
                    xs.append(score(S, D7, CK7, K1, Dm[K1])["sigma"])
                ok = [float(l) for l, s_ in zip(lgrid, xs) if s_ < 2]
                scan[foot] = dict(sigma=xs, first_below2=min(ok) if ok else None, best=float(lgrid[int(np.argmin(xs))]), best_sigma=float(min(xs)))
                P(f"  diagnostic ({foot}): lambda_early needed for K1 < 2 sigma: {scan[foot]['first_below2']} (scan 0-20); best {scan[foot]['best']:.2f} "
                  f"({scan[foot]['best_sigma']:.2f} sigma); measured lambda_early {LAM['L-meas'][1]:.3f} (f_leak early {cw['early']['f_leak']:.3f}); "
                  f"lambda_early x f_W(early) at the first < 2 sigma = {(scan[foot]['first_below2'] or float('nan')) * cw['early']['fW_model']:.2f}")
            RUN[sname]["lambda_scan"] = dict(grid=lgrid.tolist(), **scan)
RES["runs"] = RUN

# ================================================================== controls, verdict, MUTATE
R0 = RUN["M0"]["settings"]
c1c, c1a = R0["L-none"]["canonical"]["K1"]["chi2"], R0["L-none"]["alt"]["K1"]["chi2"]
check("C1 (= MU0) L-none reproduces CFG505's M0 split 35.025/7 canonical (+-0.01) and 35.026 alt (+-0.05) on K1",
      abs(c1c - 35.025399) <= 0.01 and abs(c1a - 35.026335) <= 0.05, f"canonical {c1c:.4f}, alt {c1a:.4f}")
if not MUTATE:
    c2k, c2i = R0["L-cb"]["canonical"]["K1"]["chi2"], R0["L-cb"]["canonical"]["inner9"]["chi2"]
    J5 = json.load(open(os.path.join(LANES, "CFG505_galex_uv_lens_masses", "cfg505_score_results.json")))["R3"]["M0"]
    check("C2 L-cb reproduces CFG505 R3 (M0, canonical): K1 35.58 (+-0.02), inner 9 50.31 (+-0.05)",
          abs(c2k - J5["split_K1"]["canonical"]["chi2"]) <= 0.02 and abs(c2i - J5["canonical"]["split_inner9"]) <= 0.05,
          f"K1 {c2k:.3f} (CFG505 {J5['split_K1']['canonical']['chi2']:.3f}); inner 9 {c2i:.3f} (CFG505 {J5['canonical']['split_inner9']:.3f})")
    P("\n=============== VERDICT (frozen rule, M0, L-meas) ===============")
    H = R0["L-meas"]
    below = all(H[f][b]["sigma"] < 2 for f in FOOTS for b in ("K1", "inner9"))
    strip_below = all(H[f]["strip"][b]["sigma"] < 2 for f in FOOTS for b in ("K1", "inner9"))
    drop = {f: R0["L-none"][f]["K1"]["sigma"] - H[f]["K1"]["sigma"] for f in FOOTS}
    if below and strip_below:
        verdict = "SPLIT EXPLAINED"
    elif below or all(d >= 1.0 for d in drop.values()):
        verdict = "PARTLY"
    else:
        verdict = "NOT EXPLAINED"
    for f in FOOTS:
        P(f"  {f:9s}: K1 sigma L-none {R0['L-none'][f]['K1']['sigma']:.2f} -> L-meas {H[f]['K1']['sigma']:.2f} (drop {drop[f]:+.2f}); "
          f"inner 9 {R0['L-none'][f]['inner9']['sigma']:.2f} -> {H[f]['inner9']['sigma']:.2f}; strip K1 {H[f]['strip']['K1']['sigma']:.2f}, inner 9 {H[f]['strip']['inner9']['sigma']:.2f}")
    alt_v = {}
    for nm in ("L-match", "L-unw", "L-2sd", "L-lit"):
        b2 = all(R0[nm][f][b]["sigma"] < 2 for f in FOOTS for b in ("K1", "inner9"))
        d2 = all(R0["L-none"][f]["K1"]["sigma"] - R0[nm][f]["K1"]["sigma"] >= 1.0 for f in FOOTS)
        alt_v[nm] = "EXPLAINED-level" if b2 else ("PARTLY-level" if d2 else "NOT EXPLAINED-level")
    P(f"  -> VERDICT: {verdict}.  Reported settings would read: " + ", ".join(f"{k} {v}" for k, v in alt_v.items()))
    RES["verdict"] = dict(verdict=verdict, drop_K1=drop, below2=below, strip_below2=strip_below, reported_settings=alt_v)
else:
    P("\n=============== MUTATE ===============")
    ok = all(R0["MU1-swap"][f]["K1"]["sigma"] >= R0["L-meas"][f]["K1"]["sigma"] for f in FOOTS)
    check("MU1 swapped lambdas do not explain the split: sigma_K1(swap) >= sigma_K1(L-meas) on both footings", ok,
          "; ".join(f"{f} swap {R0['MU1-swap'][f]['K1']['sigma']:.3f} vs meas {R0['L-meas'][f]['K1']['sigma']:.3f} "
                    f"(inner 9 {R0['MU1-swap'][f]['inner9']['sigma']:.3f} vs {R0['L-meas'][f]['inner9']['sigma']:.3f})" for f in FOOTS))
RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c in CHK.values() if c["load_bearing"] and not c["ok"])
P(f"\n{sum(c['ok'] for c in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg509_score_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg509_score{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
