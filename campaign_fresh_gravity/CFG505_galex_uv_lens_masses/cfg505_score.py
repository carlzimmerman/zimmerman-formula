#!/usr/bin/env python3
"""CFG505 scoring (FROZEN_CRITERIA.md sections 4-7; 398405fc8): the M*-dependent KiDS lensing tests re-scored with each mass set.

Machinery read-only: CFG261's cfg261_kids_abs.py prefix (CFG61's L law stack as cell tables on the 10-node log s grid, its solver), whose
cached base tables are copied (not edited) into this lane's cache in the data dir. Each lens is assigned to its (log M*, z) cell by the
NEW log M* and weighted by the NEW M_gal; the data are the re-staged per-lens sums of cfg505_stage.py (pairs binned by the NEW M_gal).
  T1 (headline) re-measured early/late split on K1 (bins 8-14), jackknife covariance x Hartlap 41/49, law at s = 1, both footings.
  T2 CFG261's implied-a0 scale s* (diagonal jackknife weights, fine-grid solve, jackknife SD of log s*) for 7 rows.
  R1 the early-class differential the split wants; R2 the UV-class split; R3 CFG503's E term (inner / outer bins reported apart);
  R4 M1b / M1c / M2i; R5 pair-weighted mean R per bin.
MUTATE (CFG505_MUTATE=1, outputs *_MUTATE.*): the shuffled-UV set M2_MUT replaces M2; MU1 / MU2 of the criteria.
Run: nice -n 15 python3 cfg505_score.py ; CFG505_MUTATE=1 nice -n 15 python3 cfg505_score.py
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import io, json, math, time, shutil, contextlib
import numpy as np
from scipy.stats import chi2 as CHI2, norm, spearmanr
from scipy.interpolate import CubicSpline, RegularGridInterpolator

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.dirname(LANES)
WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg505_work"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
MUTATE = os.environ.get("CFG505_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
LOG, CHK, RES = [], {}, {"lane": "CFG505", "script": "cfg505_score", "mutate": MUTATE}
FOOTS = ("canonical", "alt")


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg, lb=True):
    CHK[name] = dict(ok=bool(ok), load_bearing=lb, msg=msg); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {msg}")


def zs(p):
    return float(norm.isf(p / 2)) if p > 0 else float("inf")


# ------------------------------------------------------------------ CFG261 prefix (read-only), its base tables copied to this lane's cache
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
tables, cells, build_cells, LSN, LSF, Model = g["tables"], g["cells"], g["build_cells"], g["LSN"], g["LSF"], g["Model"]
solve1, solve_many, nodes_for, jack_sd = g["solve1"], g["solve_many"], g["nodes_for"], g["jack_sd"]
LMG, ZG, K1, NPAT, KG, patch, H12 = g["LMG"], g["ZG"], g["K1"], g["NPAT"], g["KG"], g["patch"], g["H12"]
A0C, A0A, fcold = g["A0C"], g["A0A"], g["fcold"]
nA, nB = len(LMG), len(ZG)
LS_ALT = math.log10(A0A / A0C)
TB = tables("base")                                     # (10 s-nodes, nA, nB, 15)
P(f"CFG505 score  MUTATE={int(MUTATE)}; CFG261 prefix loaded ({time.time() - T0:.0f} s); K1 = {K1}; alt footing at log s = {LS_ALT:.5f}")

# ------------------------------------------------------------------ lenses, mass sets, re-staged sums
ln = np.load(os.path.join(DATA, "lr_lenses.npz"))
typ0, zl = ln["typ"].astype(int), ln["z"].astype(float)
NL = len(typ0)
MS = np.load(os.path.join(WORK, "cfg505_masses.npz"))
SETS = ["M0", "M1", "M2_MUT"] if MUTATE else ["M0", "M1", "M2", "M1b", "M1c", "M2i"]
UVSET = "M2_MUT" if MUTATE else "M2"
PL = {s: np.load(os.path.join(WORK, f"cfg505_perlens_{s}.npz")) for s in SETS}
ref = np.load(os.path.join(DATA, "cfg110_perlens.npz"))
dev = 0.0
for k in ("WG", "WW", "NN"):
    a, b = PL["M0"][k], ref[k]
    nz = b != 0
    dev = max(dev, float(np.max(np.abs(a[nz] / b[nz] - 1))), float(np.max(np.abs(a[~nz]))))
check("C1 re-staged M0 per-lens sums equal cfg110_perlens.npz (max relative deviation <= 1e-12)", dev <= 1e-12, f"max deviation {dev:.1e}")
iz = np.clip(np.round((zl - 0.05) / 0.10).astype(int), 0, nB - 1)


class MassSet:
    def __init__(self, name, typ=None):
        self.name = name
        self.lm = MS["logM_" + name].astype(float); self.Mg = MS["Mgal_" + name].astype(float)
        self.typ = typ0 if typ is None else typ
        self.im = np.clip(np.round((self.lm - LMG[0]) / 0.05).astype(int), 0, nA - 1)
        self.WG, self.WW, self.NN = PL[name]["WG"], PL[name]["WW"], PL[name]["NN"]

    def cellw(self, mask):
        w = np.zeros((nA, nB)); np.add.at(w, (self.im[mask], iz[mask]), self.Mg[mask]); return w

    def sums(self, mask, cols=K1):
        pa = patch[mask]
        Sg = np.stack([np.bincount(pa, weights=self.WG[mask][:, k], minlength=NPAT) for k in cols], 1)
        Sw = np.stack([np.bincount(pa, weights=self.WW[mask][:, k], minlength=NPAT) for k in cols], 1)
        return Sg, Sw


def row_data(S, mask, cols=K1):
    Sg, Sw = S.sums(mask, cols)
    tg, tw = Sg.sum(0), Sw.sum(0)
    d = tg / tw / KG; loo = (tg[None] - Sg) / (tw[None] - Sw) / KG
    R_ = loo - loo.mean(0); cov = (NPAT - 1) / NPAT * (R_.T @ R_)
    return d, loo, cov


def class_model(S, mask, T=TB, cols=K1):
    return Model(nodes_for(T, S.cellw(mask)), cols)


# ------------------------------------------------------------------ T1: the early/late split
HART7 = (NPAT - len(K1) - 2) / (NPAT - 1)


def split_data(S, typ):
    dl, ll, _ = row_data(S, typ == 0); de, le, _ = row_data(S, typ == 1)
    D = de - dl; Dp = le - ll
    Rd = Dp - Dp.mean(0); CK = (NPAT - 1) / NPAT * (Rd.T @ Rd)
    return D, CK


def split_score(S, typ=None, Te=None, Tl=None, extraE=None):
    typ = S.typ if typ is None else typ
    D, CK = split_data(S, typ)
    ml = class_model(S, typ == 0, TB if Tl is None else Tl); me = class_model(S, typ == 1, TB if Te is None else Te)
    out = {}
    for foot in FOOTS:
        ls = 0.0 if foot == "canonical" else LS_ALT
        Dm = me.at(ls) - ml.at(ls)
        if extraE is not None:
            Dm = Dm + extraE
        r = D - Dm
        x2 = float(r @ np.linalg.solve(CK, r)) * HART7
        p = float(CHI2.sf(x2, len(K1)))
        out[foot] = dict(chi2=x2, p=p, sigma=zs(p), D=D.tolist(), Dmodel=Dm.tolist())
    return out


# ------------------------------------------------------------------ T2: implied-a0 levels (CFG261 estimator)
def t2_rows(S):
    typ = S.typ
    Q1 = {c: float(np.quantile(zl[typ0 == c], 1 / 3)) for c in (0, 1)}
    Q2 = {c: float(np.quantile(zl[typ0 == c], 2 / 3)) for c in (0, 1)}
    rows = {}
    for c, cn in ((0, "late"), (1, "early")):
        rows[f"T-{cn}-LO"] = (typ == c) & (zl < Q1[c])
        rows[f"T-{cn}-HI"] = (typ == c) & (zl >= Q2[c])
    rows["late"] = typ == 0; rows["early"] = typ == 1; rows["ALL"] = np.ones(NL, bool)
    return rows


def t2_fit(S, mask):
    d, loo, cov = row_data(S, mask)
    sig = np.sqrt(np.diag(cov)); W = np.diag(1 / sig ** 2)
    m = class_model(S, mask)
    ls0, unb = solve1(d, W, m.fine)
    jl, _ = solve_many(loo, W, m.fine)
    p = len(d); Ci = np.linalg.inv(cov) * H12(p)
    mm, m1 = m.at(ls0), m.at(0.0)
    chis, chi1 = float((d - mm) @ Ci @ (d - mm)), float((d - m1) @ Ci @ (d - m1))
    s = 10 ** ls0
    return dict(n=int(mask.sum()), ls=ls0, s=s, jsd=jack_sd(jl), unb=bool(unb), a0=s * 9.3603e-11, kappa_can=0.5 * s, kappa_alt=0.5 * s * A0C / A0A,
                chi_s=chis, p_s=float(CHI2.sf(chis, p - 1)), chi_1=chi1, p_1=float(CHI2.sf(chi1, p)))


# ================================================================== run every set
MSET = {s: MassSet(s) for s in SETS}
T1, T2 = {}, {}
for s in SETS:
    S = MSET[s]
    T1[s] = split_score(S)
    T2[s] = {r: t2_fit(S, m) for r, m in t2_rows(S).items()}
    P(f"\n  [{s}] T1 split (K1, re-measured): canonical chi2 {T1[s]['canonical']['chi2']:.2f}/7 (p {T1[s]['canonical']['p']:.2e}, "
      f"{T1[s]['canonical']['sigma']:.2f} sigma); alt {T1[s]['alt']['chi2']:.2f}/7 (p {T1[s]['alt']['p']:.2e}, {T1[s]['alt']['sigma']:.2f} sigma)")
    P(f"       data D  : " + " ".join(f"{x:6.2f}" for x in T1[s]["canonical"]["D"]))
    P(f"       model D : " + " ".join(f"{x:6.2f}" for x in T1[s]["canonical"]["Dmodel"]) + "  (canonical)")
    for r, v in T2[s].items():
        P(f"       T2 {r:10s} N {v['n']:6d}: s* {v['s']:.3f} (log {v['ls']:+.3f} +- {v['jsd']:.3f} jk){' [UNBOUNDED]' if v['unb'] else ''}; a0 {v['a0']:.3e}; "
          f"kappa_implied can {v['kappa_can']:.3f} / alt {v['kappa_alt']:.3f}; chi2(s*) {v['chi_s']:.1f}/6 (p {v['p_s']:.2g}), chi2(s=1) {v['chi_1']:.1f}/7 (p {v['p_1']:.2g})")
RES["T1"] = T1; RES["T2"] = T2

# ------------------------------------------------------------------ controls C2 / C3
c2c, c2a = T1["M0"]["canonical"]["chi2"], T1["M0"]["alt"]["chi2"]
check("C2 T1 with M0 reproduces CFG95-MUTATE's re-measured split chi2 35.025 (canonical, +-0.01) and 35.026 (alt, +-0.05)",
      abs(c2c - 35.025399) <= 0.01 and abs(c2a - 35.026335) <= 0.05, f"canonical {c2c:.4f}, alt {c2a:.4f}")
J261 = json.load(open(os.path.join(C261, "cfg261_stageB_results.json")))["numbers"]["rows"]
d3 = {r: T2["M0"][r]["ls"] - J261[r]["ls"] for r in ("T-late-LO", "T-late-HI", "T-early-LO", "T-early-HI")}
dj = {r: T2["M0"][r]["jsd"] - J261[r]["jsd"] for r in d3}
check("C3 T2 with M0 reproduces CFG261's s* for the four T rows within 0.005 dex", max(abs(v) for v in d3.values()) <= 0.005,
      ", ".join(f"{r} {T2['M0'][r]['s']:.3f} (d log {v:+.1e}; jsd {T2['M0'][r]['jsd']:.3f} vs {J261[r]['jsd']:.3f})" for r, v in d3.items()))

# ------------------------------------------------------------------ R5: pair-weighted mean R per bin
GC = np.sqrt(g["EDGES"][1:] * g["EDGES"][:-1])
RM = {}
for s in SETS:
    S = MSET[s]
    Rk = np.sqrt(6.67430e-11 * S.Mg[:, None] * 1.98892e30 / GC[None, :]) / 3.0856775814913673e22
    RM[s] = ((S.WW * Rk).sum(0) / S.WW.sum(0)).tolist()
P("\n  R5 pair-weighted mean R per bin [Mpc] (bins 0-14; K1 = 8-14):")
for s in SETS:
    P(f"    {s:6s}: " + " ".join(f"{x:5.3f}" for x in RM[s]) + f"   K1 max {max(RM[s][k] for k in K1):.3f}")
RES["R5_meanR"] = RM

# ------------------------------------------------------------------ R1: the early-class differential the split wants (model-side shift)
DG = np.round(np.arange(0.0, 0.5001, 0.05), 3)
SH = {}
I0 = int(np.argmin(np.abs(LSN)))
for Dv in DG:
    key = os.path.join(CACHE, f"r1_shift{Dv:+.3f}.npz")
    if os.path.exists(key):
        z_ = np.load(key); SH[(Dv, "canonical")], SH[(Dv, "alt")] = z_["can"], z_["alt"]
        continue
    can = TB[I0] if Dv == 0 else cells(0.0, shift=float(Dv), kern="mono", tfac=0.40, gasf=1.0, eps=0.0)
    alt = build_cells(LS_ALT, shift=float(Dv))
    np.savez(key, can=can, alt=alt); SH[(Dv, "canonical")], SH[(Dv, "alt")] = can, alt
P(f"\n  R1 tables ready ({time.time() - T0:.0f} s)")
R1 = {}
for s in [x for x in SETS if x in ("M0", "M1", UVSET)]:
    S = MSET[s]; D, CK = split_data(S, S.typ)
    R1[s] = {}
    for foot in FOOTS:
        ml = nodes_for(SH[(0.0, foot)][None], S.cellw(S.typ == 0))[0][K1]
        x2s = []
        for Dv in DG:
            me = nodes_for(SH[(Dv, foot)][None], S.cellw(S.typ == 1))[0][K1]
            r = D - (me - ml); x2s.append(float(r @ np.linalg.solve(CK, r)) * HART7)
        ok05 = [float(Dv) for Dv, x in zip(DG, x2s) if CHI2.sf(x, 7) > 0.05]
        R1[s][foot] = dict(chi2=x2s, best=float(DG[int(np.argmin(x2s))]), chi2_best=float(min(x2s)), p05=[min(ok05), max(ok05)] if ok05 else None)
        P(f"    [{s}] {foot:9s}: chi2 vs early shift 0..0.5 dex: " + " ".join(f"{x:.1f}" for x in x2s)
          + f" | best {R1[s][foot]['best']:.2f} ({R1[s][foot]['chi2_best']:.1f}); p > 0.05 for {R1[s][foot]['p05']}")
RES["R1"] = R1

# ------------------------------------------------------------------ R2: the UV-class split (UV star-forming early lenses -> late)
uvsf = MS["uvsf_mut"] if MUTATE else MS["uvsf"]
typ_uv = np.where((typ0 == 1) & uvsf, 0, typ0)
R2 = split_score(MassSet(UVSET, typ_uv))
P(f"\n  R2 UV-class split ({UVSET} masses; {int(((typ0 == 1) & uvsf).sum())} UV star-forming early lenses moved to late): "
  + "; ".join(f"{f} chi2 {R2[f]['chi2']:.2f}/7 (p {R2[f]['p']:.2e}, {R2[f]['sigma']:.2f} sigma)" for f in FOOTS))
R2b = split_score(MassSet(UVSET, np.where((typ0 == 1) & uvsf, -1, typ0)))
P("     (variant: UV star-forming early lenses dropped from both classes, reported) "
  + "; ".join(f"{f} chi2 {R2b[f]['chi2']:.2f}/7 ({R2b[f]['sigma']:.2f} sigma)" for f in FOOTS))
RES["R2"] = dict(moved=R2, dropped=R2b, n=int(((typ0 == 1) & uvsf).sum()))

# ------------------------------------------------------------------ R3: CFG503's environment term E (nlz, W10, Moster), restacked per set
sys.path.insert(0, os.path.join(LANES, "CFG495_drawdown_shell"))
import cfg495_lenslib as LL                                                    # noqa: E402 (read-only)
ET = np.load(os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg503_work", "cfg503_env_table.npz")))
LMS, ZGE, RGE = ET["LMS"], ET["ZG"], ET["RG"]
EI = RegularGridInterpolator((LMS, ZGE), ET["E_moster_nlz_W10"], bounds_error=False, fill_value=None)


def env_perlens(S):
    lmg = np.log10(S.Mg)
    key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(zl / 0.03).astype(np.int64)
    _, gi, cnt = np.unique(key, return_inverse=True, return_counts=True); gi = gi.ravel()
    GM = 10 ** (np.bincount(gi, weights=lmg) / cnt); GZ = np.bincount(gi, weights=zl) / cnt; GS = np.bincount(gi, weights=S.lm) / cnt
    Eg = EI(np.c_[np.clip(GS, LMS[0], LMS[-1]), np.clip(GZ, ZGE[0], ZGE[-1])])
    LR = np.log(RGE)
    Etab = np.array([LL.finish(lambda R, e=Eg[j]: np.interp(np.log(R), LR, e), GM[j]) for j in range(len(GM))])
    return gi, Etab


def pstack(gi, Etab, WW, mask):
    NG = Etab.shape[0]; out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG); out[k] = (w @ Etab[:, k]) / w.sum()
    return out


INN9 = list(range(6, 15)); OUT6 = list(range(0, 6))
R3 = {}
for s in [x for x in SETS if x in ("M0", "M1", UVSET)]:
    S = MSET[s]
    gi, Etab = env_perlens(S)
    El, Ee, Ea = (pstack(gi, Etab, S.WW, S.typ == 0), pstack(gi, Etab, S.WW, S.typ == 1), pstack(gi, Etab, S.WW, np.ones(NL, bool)))
    sp = split_score(S, extraE=(Ee - El)[K1])
    # inner-9 split with E
    dl9, ll9, _ = row_data(S, S.typ == 0, INN9); de9, le9, _ = row_data(S, S.typ == 1, INN9)
    Dp = le9 - ll9; Rd = Dp - Dp.mean(0); CK9 = (NPAT - 1) / NPAT * (Rd.T @ Rd); H9 = H12(len(INN9))
    full = list(range(15))
    dA, _, cA = row_data(S, np.ones(NL, bool), full)
    mA = class_model(S, np.ones(NL, bool), cols=full)
    ml9 = class_model(S, S.typ == 0, cols=INN9); me9 = class_model(S, S.typ == 1, cols=INN9)
    R3[s] = dict(E_late=El.tolist(), E_early=Ee.tolist(), E_all=Ea.tolist(), split_K1=sp)
    for foot in FOOTS:
        ls = 0.0 if foot == "canonical" else LS_ALT
        r9 = (de9 - dl9) - (me9.at(ls) - ml9.at(ls) + (Ee - El)[INN9])
        x9 = float(r9 @ np.linalg.solve(CK9, r9)) * H9
        mod = mA.at(ls) + Ea
        rI, rO = (dA - mod)[INN9], (dA - mod)[OUT6]
        xI = float(rI @ np.linalg.solve(cA[np.ix_(INN9, INN9)], rI)) * H12(9)
        xO = float(rO @ np.linalg.solve(cA[np.ix_(OUT6, OUT6)], rO)) * H12(6)
        modn = mA.at(ls); rIn = (dA - modn)[INN9]
        xIn = float(rIn @ np.linalg.solve(cA[np.ix_(INN9, INN9)], rIn)) * H12(9)
        R3[s][foot] = dict(split_inner9=x9, split_inner9_p=float(CHI2.sf(x9, 9)), all_inner9=xI, all_outer6=xO, all_inner9_noE=xIn)
        P(f"    R3 [{s}] {foot:9s}: split + E on K1 {sp[foot]['chi2']:.2f}/7 ({sp[foot]['sigma']:.2f} sigma), on inner 9 {x9:.2f}/9 "
          f"({zs(CHI2.sf(x9, 9)):.2f} sigma); ALL-lens law + E: inner 9 {xI:.1f}/9 (no E {xIn:.1f}), OUTER 6 {xO:.1f}/6 (outer: reported only)")
RES["R3"] = R3

# ================================================================== verdicts / MUTATE
P("\n=============== VERDICTS (frozen rules) ===============" if not MUTATE else "\n=============== MUTATE CHECKS ===============")


def dsig(a, b, foot): return T1[a][foot]["sigma"] - T1[b][foot]["sigma"]


def cls(vals):
    n = sum(abs(v) >= 1.0 for v in vals)
    return "MATERIAL" if n == len(vals) else ("PARTIAL" if n else "NOT MATERIAL")


TROWS = ("T-late-LO", "T-late-HI", "T-early-LO", "T-early-HI", "late", "early")
if not MUTATE:
    V = {}
    for a, b, nm in (("M2", "M0", "V1 headline: M2 vs M0"), ("M2", "M1", "UV-only: M2 vs M1"), ("M1", "M0", "method: M1 vs M0"),
                     ("M2i", "M0", "reported: M2i vs M0"), ("M1b", "M0", "reported: M1b vs M0"), ("M1c", "M0", "reported: M1c vs M0")):
        ds = [dsig(a, b, f) for f in FOOTS]
        V[nm] = dict(dsigma=ds, verdict=cls(ds))
        P(f"  {nm:22s}: d sigma_split canonical {ds[0]:+.2f}, alt {ds[1]:+.2f} -> {cls(ds)}")
    closed = all(T1["M2"][f]["p"] > 0.01 for f in FOOTS)
    V["split_closed_M2"] = closed
    P(f"  SPLIT with M2: canonical p {T1['M2']['canonical']['p']:.2e}, alt p {T1['M2']['alt']['p']:.2e} -> {'SPLIT CLOSED' if closed else 'the split stands'}")
    V2 = {}
    for a, b, nm in (("M2", "M0", "V2: M2 vs M0"), ("M2", "M1", "UV-only: M2 vs M1"), ("M1", "M0", "method: M1 vs M0")):
        V2[nm] = {}
        for r in TROWS:
            dl = T2[a][r]["ls"] - T2[b][r]["ls"]; thr = max(T2[b][r]["jsd"], 0.05)
            V2[nm][r] = dict(dlog=dl, thr=thr, verdict="MATERIAL" if abs(dl) >= thr else "NOT MATERIAL")
        P(f"  {nm:18s}: " + "; ".join(f"{r} {V2[nm][r]['dlog']:+.3f} (thr {V2[nm][r]['thr']:.3f}) {V2[nm][r]['verdict']}" for r in TROWS))
    V["V2"] = V2
    MSj = json.load(open(os.path.join(HERE, "cfg505_masses_results.json")))
    for r, need in (("T-early-LO", J261["T-early-LO"]["need"]), ("T-early-HI", J261["T-early-HI"]["need"])):
        P(f"  {r}: CFG261 needed +{need:.2f} dex for s* = 1; the early class mean shift M2 - M0 is {MSj['cmp_M2']['mean_early']:+.3f} dex "
          f"(s* {T2['M0'][r]['s']:.2f} -> {T2['M2'][r]['s']:.2f})")
    RES["verdict"] = V
else:
    MSj = json.load(open(os.path.join(HERE, "cfg505_masses_results.json")))
    rho_m = MSj["rho_mut"]
    check("MU1 the shuffle destroys the UV-optical link: |rho(NUV-r, u-r)| over detections < 0.05 (real +0.80)", abs(rho_m) < 0.05, f"rho {rho_m:+.3f}")
    ds = [dsig("M2_MUT", "M1", f) for f in FOOTS]
    dls = {r: T2["M2_MUT"][r]["ls"] - T2["M1"][r]["ls"] for r in ("T-late-LO", "T-late-HI", "T-early-LO", "T-early-HI")}
    elm = MSj["uvonly_M2_MUT"]["early_minus_late"]; elr = MSj["uvonly_M2"]["early_minus_late"]
    ok = all(abs(x) < 0.3 for x in ds) and all(abs(v) < 0.02 for v in dls.values()) and abs(elm) < 0.005
    check("MU2 the UV-driven change disappears with shuffled UV: |d sigma_split| < 0.3 (both footings), |d log s*| < 0.02 (T rows), early-late UV shift "
          "within 0.005 of zero", ok, f"d sigma {ds[0]:+.3f} / {ds[1]:+.3f}; d log s* " + ", ".join(f"{r} {v:+.4f}" for r, v in dls.items())
          + f"; early - late mean shift {elm:+.4f} (real M2 - M1: {elr:+.4f})")
    RES["MUTATE"] = dict(dsigma=ds, dls=dls, el_mut=elm, el_real=elr)

RES["checks"] = CHK
RES["elapsed_s"] = round(time.time() - T0, 1)
nlb = sum(1 for c in CHK.values() if c["load_bearing"] and not c["ok"])
P(f"\n{sum(c['ok'] for c in CHK.values())}/{len(CHK)} checks pass; elapsed {RES['elapsed_s']} s")
json.dump(RES, open(os.path.join(HERE, f"cfg505_score_results{SUF}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg505_score{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(1 if nlb else 0)
