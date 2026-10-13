#!/usr/bin/env python3
"""CFG722 (FROZEN_CRITERIA.md, d3a4df1e1): colour x structure cross-split of the KiDS early-type lensing excess.
Structure: seeing/tile-corrected aperture concentration C_res = MAG_APER_4 - MAG_APER_14 (KiDS DR4.1, owner-approved ESO download in
_external_data/kids_dr4_structure/); gate V1 vs lensfit bulge_fraction.  Raw lensing (CFG585 head + CFG531 esd_loo, unedited).
CFG722_MUTATE=1 CFG722_M=M1|M2 -> _MUTATE outputs, exit 1 iff the tooth bites."""
import os, io, glob, json, math, contextlib
import numpy as np
from astropy.io import fits
from scipy.spatial import cKDTree
from scipy.stats import spearmanr

HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); ROOT = os.path.dirname(LANES)
EXT = os.path.join(os.path.dirname(ROOT), "_external_data")
MUT = os.environ.get("CFG722_MUTATE", "0") == "1"; MODE = os.environ.get("CFG722_M", "") if MUT else ""
TAG = f"_MUTATE{MODE}" if MUT else ""
OUT, RES = [], {"lane": "CFG722", "criteria": "d3a4df1e1", "mutate": MUT, "mode": MODE}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)


# ---------------------------------------------------------------- structure download -> C_res per lens
cols = ("RAJ2000", "DECJ2000", "KIDS_TILE", "MAG_AUTO", "MAG_APER_4", "MAG_APER_14", "MAG_APER_8", "MAG_APER_20")
parts = {c: [] for c in cols}
for f in sorted(glob.glob(os.path.join(EXT, "kids_dr4_structure", "strip_*.fits"))):
    with fits.open(f, memmap=False) as h:
        if h[1].header["NAXIS2"] == 0:
            continue
        d = h[1].data
        for c in cols:
            parts[c].append(np.asarray(d[c]).astype(str) if c == "KIDS_TILE" else np.asarray(d[c], float))
S = {c: np.concatenate(v) for c, v in parts.items()}
ok = np.isfinite(S["MAG_APER_4"]) & np.isfinite(S["MAG_APER_14"]) & (S["MAG_APER_4"] < 90) & (S["MAG_APER_14"] < 90)
C1 = S["MAG_APER_4"] - S["MAG_APER_14"]; C2 = S["MAG_APER_8"] - S["MAG_APER_20"]
ok2 = ok & np.isfinite(C2) & (S["MAG_APER_8"] < 90) & (S["MAG_APER_20"] < 90)
key = np.char.add(S["KIDS_TILE"], np.floor(S["MAG_AUTO"] * 2).astype(int).astype(str))


def tile_correct(Cv, good):
    out = np.full(Cv.size, np.nan)
    u, inv = np.unique(key[good], return_inverse=True)
    med = np.array([np.median(x) for x in np.split(Cv[good][np.argsort(inv, kind="stable")], np.cumsum(np.bincount(inv))[:-1])])
    out[good] = Cv[good] - med[inv]
    return out


C1r = tile_correct(C1, ok); C2r = tile_correct(C2, ok2)
P(f"CFG722 colour x structure cross-split  {('MUTATE ' + MODE) if MUT else 'PRIMARY'}")
P(f"download: {len(C1)} bright galaxies; C defined for {ok.sum()} (C2 {ok2.sum()})")

LT = np.load(os.path.join(ROOT, "real_research", "data", "lensing_rar", "lr_lenses.npz"))


def xyz(r, dd):
    r = np.radians(r); dd = np.radians(dd); return np.c_[np.cos(dd) * np.cos(r), np.cos(dd) * np.sin(r), np.sin(dd)]


tr = cKDTree(xyz(S["RAJ2000"], S["DECJ2000"]))
dist, ix = tr.query(xyz(LT["ra"], LT["dec"]), distance_upper_bound=np.radians(1 / 3600))
mt = np.isfinite(dist)
CL = np.where(mt, C1r[np.where(mt, ix, 0)], np.nan); CL2 = np.where(mt, C2r[np.where(mt, ix, 0)], np.nan)
P(f"lenses matched (<1\"): {mt.sum()} of {len(mt)}; with C_res {np.isfinite(CL).sum()}")

# ---------------------------------------------------------------- V1 gate
SM = np.load(os.path.join(EXT, "kids_lens_structure_match.npz"))
bf = SM["bulge_fraction"]; g = np.isfinite(bf) & np.isfinite(CL)
rho = float(spearmanr(CL[g], bf[g]).correlation)
V1 = rho >= 0.3
P(f"V1 gate: Spearman(C_res, lensfit bulge_fraction) = {rho:+.3f} on {g.sum()} lenses -> {'PASS' if V1 else 'FAIL (VOID)'}")
RES["V1"] = dict(rho=rho, n=int(g.sum()), pass_=bool(V1))

# ---------------------------------------------------------------- lensing machinery (CFG669's Ks baryonic mass)
for v in ("CFG585_MUTATE", "CFG531_MUTATE"):
    os.environ.pop(v, None)
path = os.path.join(LANES, "CFG585_age_settling", "cfg585_age.py")
ns = {"__file__": path, "__name__": "head"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(open(path).read().split('P("=" * 100)')[0], path, "exec"), ns)
U, F30, TYP, LMSL, esd_loo, NPATCH = (ns[k] for k in ("U", "F30", "TYP", "LMSL", "esd_loo", "NPATCH"))
Lp, o, ixL = ns["Lp"], ns["o"], ns["ix"]
G = esd_loo.__globals__; WG0, WW0 = G["WG"].copy(), G["WW"].copy()
FC = LT["Mgal"] / 10 ** LT["logM"] - 1
kabs = np.array(Lp["MAG_ABS_Ks"], "f8")[o[ixL]]
LK = 0.4 * (5.08 - kabs); cK = float(np.median(LMSL[F30]) - np.median(LK[F30])); LMK = LK + cK
LMBK = np.full(len(TYP), np.nan)
for ty in (0, 1):
    m = TYP == ty
    edges = np.arange(np.floor(LT["logM"][m].min() * 10) / 10, LT["logM"][m].max() + 0.1, 0.1)
    cen, med = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        s = m & (LT["logM"] >= a) & (LT["logM"] < b)
        if s.sum() >= 20:
            cen.append(0.5 * (a + b)); med.append(np.median(FC[s]))
    LMBK[m] = LMK[m] + np.log10(1 + np.interp(LMK[m], cen, med))
ZL = LT["z"].astype(float)
SMP = F30 & np.isfinite(LMBK) & np.isfinite(CL)
K9 = list(range(6, 15))
dall, Call, Lall = esd_loo(SMP); W = 1.0 / np.diag(Call)
qd = np.quantile(LMBK[SMP], np.linspace(0, 1, 11)); qd[-1] += 1e-9
dec = np.clip(np.searchsorted(qd, LMBK, side="right") - 1, 0, 9)
qz = np.quantile(ZL[SMP], [0, 1 / 3, 2 / 3, 1]); qz[-1] += 1e-9
zt = np.clip(np.searchsorted(qz, ZL, side="right") - 1, 0, 2)
jb = dec * 3 + zt
red = TYP == 1


def structure(Cv):
    conc = np.zeros(len(TYP), bool)
    for t in range(3):
        mm = SMP & (zt == t); conc[mm] = Cv[mm] > np.median(Cv[mm])
    return conc


def run(Cv, colour, rng_mode=None):
    conc = structure(Cv)
    col = colour.copy()
    rng = np.random.default_rng(722)
    if rng_mode == "M1":
        for b in np.unique(jb[SMP]):
            for cc in (True, False):
                idx = np.where(SMP & (jb == b) & (col == cc))[0]; conc[idx] = rng.permutation(conc[idx])
    if rng_mode == "M2":
        for b in np.unique(jb[SMP]):
            for ss in (True, False):
                idx = np.where(SMP & (jb == b) & (conc == ss))[0]; col[idx] = rng.permutation(col[idx])
    pall = np.bincount(jb[SMP], minlength=30) / SMP.sum()
    cells, A, L, N = {}, {}, {}, {}
    for nm, mk in (("RC", col & conc), ("RD", col & ~conc), ("BC", ~col & conc), ("BD", ~col & ~conc)):
        mk = mk & SMP
        r = np.zeros(len(TYP)); cnt = np.bincount(jb[mk], minlength=30); dropped = 0
        for b in range(30):
            if cnt[b] < 50:
                dropped += cnt[b]; continue
            r[mk & (jb == b)] = pall[b] / (cnt[b] / mk.sum())
        use = mk & (r > 0)
        G["WG"] = WG0 * r[:, None]; G["WW"] = WW0 * r[:, None]
        dk, _, Lk = esd_loo(use)
        G["WG"], G["WW"] = WG0.copy(), WW0.copy()
        A[nm] = math.log10((W[K9] @ dk[K9]) / (W[K9] @ dall[K9]))
        L[nm] = np.log10((Lk[:, K9] @ W[K9]) / (Lall[:, K9] @ W[K9]))
        N[nm] = dict(n=int(use.sum()), dropped=int(dropped))
    def comb(f):
        val = f(A); lo = f(L); return float(val), float(math.sqrt((NPATCH - 1) / NPATCH * ((lo - lo.mean()) ** 2).sum()))
    dcol = comb(lambda X: 0.5 * ((X["RC"] - X["BC"]) + (X["RD"] - X["BD"])))
    dstr = comb(lambda X: 0.5 * ((X["RC"] - X["RD"]) + (X["BC"] - X["BD"])))
    inter = comb(lambda X: (X["RC"] - X["RD"]) - (X["BC"] - X["BD"]))
    sig = {k: float(math.sqrt((NPATCH - 1) / NPATCH * ((L[k] - L[k].mean()) ** 2).sum())) for k in L}
    return dict(A=A, sig=sig, N=N, dcol=dcol, dstr=dstr, inter=inter)


R1 = run(CL, red, rng_mode=MODE if MODE in ("M1", "M2") else None)
for nm in ("RC", "RD", "BC", "BD"):
    P(f"   {nm}: N {R1['N'][nm]['n']:6d} (dropped {R1['N'][nm]['dropped']})  A {R1['A'][nm]:+.4f} +- {R1['sig'][nm]:.4f}")
P(f"Delta_col (colour at fixed structure) = {R1['dcol'][0]:+.4f} +- {R1['dcol'][1]:.4f}  (Z {R1['dcol'][0] / R1['dcol'][1]:+.2f})")
P(f"Delta_str (structure at fixed colour) = {R1['dstr'][0]:+.4f} +- {R1['dstr'][1]:.4f}  (Z {R1['dstr'][0] / R1['dstr'][1]:+.2f})")
P(f"interaction = {R1['inter'][0]:+.4f} +- {R1['inter'][1]:.4f}")
zc, zs = R1["dcol"][0] / R1["dcol"][1], R1["dstr"][0] / R1["dstr"][1]
cls = ("BOTH" if (zc >= 2 and zs >= 2) else "STRUCTURE CARRIES IT" if (zs >= 2 and zc < 2) else
       "COLOUR CARRIES IT" if (zc >= 2 and zs < 2) else "UNDECIDED")
RES["main"] = {k: (v if not isinstance(v, tuple) else list(v)) for k, v in R1.items()}
rc = 0
if MUT:
    bite = abs(zs) < 2 if MODE == "M1" else abs(zc) < 2
    RES["tooth_bites"] = bool(bite); P(f"MUTATE {MODE}: tooth bites {bite}"); rc = 1 if bite else 0
else:
    R2 = run(CL2, red)
    P(f"robustness C2 (APER_8 - APER_20): Delta_col {R2['dcol'][0]:+.4f} +- {R2['dcol'][1]:.4f}; Delta_str {R2['dstr'][0]:+.4f} +- {R2['dstr'][1]:.4f}")
    RES["C2"] = {k: (v if not isinstance(v, tuple) else list(v)) for k, v in R2.items()}
    lab = cls if V1 else "VOID (V1 fails)"
    RES["label"] = lab; P(f"\nLABEL: {lab}")
json.dump(RES, open(os.path.join(HERE, f"cfg722_results{TAG}.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg722{TAG}.out"), "w").write("\n".join(OUT) + "\n")
raise SystemExit(rc)
