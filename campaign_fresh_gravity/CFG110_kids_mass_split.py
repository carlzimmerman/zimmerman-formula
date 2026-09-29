#!/usr/bin/env python3
"""CFG110 -- DOES THE KiDS LENSING SIGNAL AT FIXED g_bar DEPEND ON LENS MASS WITHIN A COLOUR CLASS?  B's law predicts no dependence in the
deep regime (all of CFG61's K1 bins are << a0); a standard halo predicts a rising one.  The high-mass minus low-mass difference within
each class, in the repo's own June re-measurement, against B's law and CFG67's LCDM computed on the identical lens subsets.

Criteria frozen and committed before any subset number: campaign_fresh_gravity/CFG110_FROZEN_CRITERIA.md (f870b217a).
  data     real_research/data/lensing_rar/cfg110_perlens.npz (CFG110_stage_perlens.py: each lens's per-bin sums from one pass of the June
           estimator) with lr_lenses.npz; June patch labels (lr_esd_jackknife.npz); ESD = sum wgE / sum W in Msun/pc^2.
  subsets  mass halves within each class at the class median log10 M_gal (late 10.448, early 10.810; the median lens goes up); redshift
           halves (reported) at the class median z.
  stat     D = [D_late, D_early], D_c = ESD(c, high) - ESD(c, low) on K1 (14 bins); joint leave-one-patch-out covariance (50 patches);
           chi2 = (D - D_model)^T C^-1 (D - D_model) x 34/49 (Hartlap, p = 14), 14 dof.
  models   B: CFG61's law stack (both footings) on each subset's lenses.  LCDM: CFG67's colour-split stack (red early, blue late) on the same
           subsets.  LCDM_m (reported): CFG67's colour-blind Moster variant.  No fit.
PRE-DECLARED (from the frozen file)
  C1  CONTROL  the per-lens sums, summed by (patch, class), reproduce the June per-patch sums to 1e-9 relative.
  C2  CONTROL  the mass halves and the redshift halves partition each class exactly.
  C3  CONTROL  with the full-class mask the model machinery reproduces CFG61's committed law stacks and CFG67's committed LCDM stacks
               (ml, me; canonical) to 1e-9 relative.
  C4  CONTROL  covariance calibration: 200 random within-class halvings (seed 110), mean Hartlap chi2 of D_null in [9.8, 18.2] (14 +- 30%).
  H1  [HEADLINE] B's law is consistent with the within-class mass dependence: p > 0.01, both footings.
  H2  CFG67's colour-split LCDM is consistent: p > 0.01.
  R0-R4 (reported): the power Delta chi2_pred(LCDM vs B) from the covariance alone; per-class 7-bin chi2; the mass-split amplitude per
               class (pair-weighted mean log10 ratio over K1, jackknife sigma) for data and models; LCDM_m; the redshift split.
MUTATE=1: the high-mass half's wgE multiplied per K1 bin by [ESD_LCDM(hi)/ESD_LCDM(lo)] / [ESD_B(hi)/ESD_B(lo)] (canonical) in each
class -- H1 must FAIL (rc = 1); if it does not, the test is declared NON-DISCRIMINATING.
Run: python3 campaign_fresh_gravity/CFG110_kids_mass_split.py   (MUTATE=1 for the control; needs CFG110_stage_perlens.py's output)
"""
import os, sys, io, json, math, contextlib
import numpy as np
from scipy.stats import chi2 as CHI2, norm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG110_kids_mass_split", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: LCDM's predicted within-class mass dependence injected into the data -- H1 must FAIL ***")
FOOTS = ("canonical", "alt")


def lane_prefix(fname, marker):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    src = open(os.path.join(HERE, fname)).read()
    g = {"__file__": os.path.join(HERE, fname), "__name__": "lane_" + fname}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:src.index(marker)], fname, "exec"), g)
    finally:
        os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return g


# ------------------------------------------------------------------ data
LR = os.path.join(C.REPO, "real_research", "data", "lensing_rar")
PL = np.load(os.path.join(LR, "cfg110_perlens.npz"))
LN = np.load(os.path.join(LR, "lr_lenses.npz"))
J = np.load(os.path.join(LR, "lr_esd_jackknife.npz"))
KG = 1.989e30 / (3.0857e16) ** 2
WG, WW, NNL = PL["WG"].astype(float), PL["WW"].astype(float), PL["NN"].astype(float)
typ, Mgal, zlen = LN["typ"], LN["Mgal"], LN["z"]
patch = J["patch"]
NPAT = 50
K1 = [8, 9, 10, 11, 12, 13, 14]
HART = (NPAT - 14 - 2) / (NPAT - 1)
lmg = np.log10(Mgal)
MED_M = {c: float(np.median(lmg[typ == c])) for c in (0, 1)}
MED_Z = {c: float(np.median(zlen[typ == c])) for c in (0, 1)}
HI = {c: (typ == c) & (lmg >= MED_M[c]) for c in (0, 1)}
LO = {c: (typ == c) & (lmg < MED_M[c]) for c in (0, 1)}
ZH = {c: (typ == c) & (zlen >= MED_Z[c]) for c in (0, 1)}
ZL = {c: (typ == c) & (zlen < MED_Z[c]) for c in (0, 1)}

# ================================================================== C1 / C2
R.banner("C1 / C2  CONTROLS (data)")
dev = 0.0
for name, A, Jk in (("wgE", WG, "wgE"), ("W", WW, "W"), ("NN", NNL, "NN")):
    S = np.zeros((NPAT, 2, 15))
    np.add.at(S, (patch, typ), A)
    dev = max(dev, float(np.max(np.abs(S - J[Jk]) / np.maximum(np.abs(J[Jk]), 1e-300))))
check("C1 CONTROL: the per-lens sums, summed by (patch, class), reproduce the June per-patch sums (wgE, W, NN) to 1e-9 relative",
      f"max relative deviation {dev:.1e}", dev < 1e-9)
part = all(np.array_equal(HI[c] ^ LO[c], typ == c) and not np.any(HI[c] & LO[c]) and np.array_equal(ZH[c] ^ ZL[c], typ == c) for c in (0, 1))
check("C2 CONTROL: the mass halves and the redshift halves partition each class exactly",
      "; ".join(f"class {c}: median log M_gal {MED_M[c]:.3f} (hi {int(HI[c].sum()):,} / lo {int(LO[c].sum()):,}), median z {MED_Z[c]:.3f} "
                f"(hi {int(ZH[c].sum()):,} / lo {int(ZL[c].sum()):,})" for c in (0, 1)), part)

# ------------------------------------------------------------------ the data difference and its jackknife
WGd = WG.copy()


def esd_and_loo(mask, wg=None):
    wg = WGd if wg is None else wg
    g = wg[mask][:, K1]; w = WW[mask][:, K1]; pa = patch[mask]
    tg, tw = g.sum(0), w.sum(0)
    Sg = np.zeros((NPAT, len(K1))); Sw = np.zeros((NPAT, len(K1)))
    np.add.at(Sg, pa, g); np.add.at(Sw, pa, w)
    return tg / tw / KG, (tg[None] - Sg) / (tw[None] - Sw) / KG


def diff_vec(pairs, wg=None):
    """pairs: [(maskA_late, maskB_late), (maskA_early, maskB_early)] -> D (14), loo replicates (50 x 14)."""
    D, L = [], []
    for A, B in pairs:
        ea, la = esd_and_loo(A, wg); eb, lb = esd_and_loo(B, wg)
        D.append(ea - eb); L.append(la - lb)
    return np.concatenate(D), np.concatenate(L, axis=1)


def jcov(L):
    Rr = L - L.mean(0)
    return (NPAT - 1) / NPAT * (Rr.T @ Rr)


def x2(r, Cm):
    return float(r @ np.linalg.solve(Cm, r)) * HART


def pv(x, k=14):
    return float(CHI2.sf(x, k))


def zs(p):
    return float(norm.isf(p / 2)) if p > 0 else float("inf")


# ------------------------------------------------------------------ the models on masks (CFG61 law, CFG67 LCDM), read-only
g61 = lane_prefix("CFG61_kids_colour_split.py", "\nRES = {}\n")
PROF, LMG, ZG, RG, EDGES, SUB = g61["PROF"], g61["LMG"], g61["ZG"], g61["RG"], g61["EDGES"], g61["SUB"]
fcold, G_SI, MSUN, MPC, im61, iz61, Mg61 = g61["fcold"], g61["G_SI"], g61["MSUN"], g61["MPC"], g61["im"], g61["iz"], g61["Mg"]
assert np.array_equal(Mg61, Mgal) and np.array_equal(g61["typ"], typ)
g67 = lane_prefix("CFG67_lcdm_control_kids_split.py", "def stack(cls, kind, dshift=0):")
TAB, im67 = g67["TAB"], g67["im"]
LRG = np.log(RG)


def law_stack(mask, foot):
    w = np.zeros((len(LMG), len(ZG)))
    np.add.at(w, (im61[mask], iz61[mask]), Mg61[mask])
    out = np.zeros(15)
    for k in range(15):
        lg = np.linspace(math.log(EDGES[k]), math.log(EDGES[k + 1]), SUB + 1)
        gs = np.exp(0.5 * (lg[1:] + lg[:-1]))
        num = den = 0.0
        for a in range(len(LMG)):
            for b in range(len(ZG)):
                if w[a, b] <= 0: continue
                Mtab = 10 ** LMG[a] * (1 + fcold(LMG[a]))
                pr = PROF[(foot, "red", LMG[a], ZG[b])]
                Rj = np.sqrt(G_SI * Mtab * MSUN / gs) / MPC
                ds = np.interp(np.log(Rj), LRG, pr["dsL"]) + pr["Mb"] / (math.pi * Rj ** 2)
                wj = w[a, b] / gs
                num += float(np.sum(wj * ds)); den += float(np.sum(wj))
        out[k] = num / den / 1e12
    return out


def lcdm_stack(mask, kind):
    w = np.zeros(len(LMG))
    np.add.at(w, im67[mask], Mgal[mask])
    out = np.zeros(15)
    for k in range(15):
        lg = np.linspace(math.log(EDGES[k]), math.log(EDGES[k + 1]), 9)
        gs = np.exp(0.5 * (lg[1:] + lg[:-1]))
        num = den = 0.0
        for a in range(len(LMG)):
            if w[a] <= 0: continue
            Mtab = 10 ** LMG[a] * (1 + fcold(LMG[a]))
            pr = TAB[kind][LMG[a]]
            Rj = np.sqrt(G_SI * Mtab * MSUN / gs) / MPC
            ds = np.interp(np.log(Rj), LRG, pr["ds"]) + pr["Mb"] / (math.pi * Rj ** 2)
            num += float(np.sum(w[a] / gs * ds)); den += float(np.sum(w[a] / gs))
        out[k] = num / den / 1e12
    return out


R.banner("C3  CONTROL (models)")
c61 = json.load(open(os.path.join(HERE, "CFG61_kids_colour_split_results.json")))["numbers"]["RES"]["canonical"]
c67 = json.load(open(os.path.join(HERE, "CFG67_lcdm_control_kids_split_results.json")))["numbers"]["lcdm"]
full = {c: typ == c for c in (0, 1)}
d3 = max(float(np.max(np.abs(law_stack(full[0], "canonical") / np.array(c61["ml"]) - 1))),
         float(np.max(np.abs(law_stack(full[1], "canonical") / np.array(c61["me"]) - 1))),
         float(np.max(np.abs(lcdm_stack(full[0], "blue") / np.array(c67["ml"]) - 1))),
         float(np.max(np.abs(lcdm_stack(full[1], "red") / np.array(c67["me"]) - 1))))
check("C3 CONTROL: with the full-class mask the model machinery reproduces CFG61's law stacks and CFG67's LCDM stacks (ml, me; canonical) to 1e-9",
      f"max relative deviation {d3:.1e}", d3 < 1e-9)
KIND = {0: "blue", 1: "red"}


def model_diff(pairs, fn):
    return np.concatenate([(fn(A, c) - fn(B, c))[K1] for c, (A, B) in enumerate(pairs)])


MPAIRS = [(HI[0], LO[0]), (HI[1], LO[1])]
ZPAIRS = [(ZH[0], ZL[0]), (ZH[1], ZL[1])]
MOD = {}
for tag, pairs in (("mass", MPAIRS), ("z", ZPAIRS)):
    MOD[tag] = dict(B={f: model_diff(pairs, lambda m, c, f=f: law_stack(m, f)) for f in FOOTS},
                    L=model_diff(pairs, lambda m, c: lcdm_stack(m, KIND[c])),
                    Lm=model_diff(pairs, lambda m, c: lcdm_stack(m, "moster")))
    if tag == "mass":
        HILO = {c: dict(Bhi=law_stack(HI[c], "canonical")[K1], Blo=law_stack(LO[c], "canonical")[K1],
                        Lhi=lcdm_stack(HI[c], KIND[c])[K1], Llo=lcdm_stack(LO[c], KIND[c])[K1]) for c in (0, 1)}

# ------------------------------------------------------------------ MUTATE: inject LCDM's contrast into the high-mass halves
if MUTATE:
    for c in (0, 1):
        ratio = (HILO[c]["Lhi"] / HILO[c]["Llo"]) / (HILO[c]["Bhi"] / HILO[c]["Blo"])
        idx = np.where(HI[c])[0]
        WGd[np.ix_(idx, K1)] = WG[np.ix_(idx, K1)] * ratio[None, :]
        P(f"  MUTATE class {c}: per-bin hi/lo contrast injected x{np.round(ratio, 3).tolist()}")

# ================================================================== R0, C4, H1, H2
D, L = diff_vec(MPAIRS)
Cm = jcov(L)
R.banner("R0 / C4  POWER AND COVARIANCE CALIBRATION")
pow_ = x2(MOD["mass"]["L"] - MOD["mass"]["B"]["canonical"], Cm)
check("R0 (reported) the power: Delta chi2_pred = (D_LCDM - D_B)^T C^-1 (D_LCDM - D_B) x 34/49 (covariance only; >= 9 means discriminating)",
      f"{pow_:.1f}  (LCDM_m vs B: {x2(MOD['mass']['Lm'] - MOD['mass']['B']['canonical'], Cm):.1f})", True, load_bearing=False)
rng = np.random.default_rng(110)
nulls = []
for t in range(200):
    pairs = []
    for c in (0, 1):
        idx = np.where(typ == c)[0]
        pick = rng.random(len(idx)) < 0.5
        A = np.zeros(len(typ), bool); B = np.zeros(len(typ), bool)
        A[idx[pick]] = True; B[idx[~pick]] = True
        pairs.append((A, B))
    Dn, Ln = diff_vec(pairs)
    nulls.append(x2(Dn, jcov(Ln)))
mn = float(np.mean(nulls))
check("C4 CONTROL: covariance calibration -- mean Hartlap chi2 of 200 random within-class halvings (14 bins) in [9.8, 18.2]",
      f"mean {mn:.2f}, median {np.median(nulls):.2f}, 16-84% {np.percentile(nulls, 16):.1f}-{np.percentile(nulls, 84):.1f}; "
      f"fraction p < 0.01: {np.mean([pv(x) < 0.01 for x in nulls]):.3f}", 9.8 <= mn <= 18.2)

R.banner("H1 / H2  THE WITHIN-CLASS MASS SPLIT ON K1 (14 bins)")
P(f"  data D (late | early): {np.round(D[:7], 2).tolist()} | {np.round(D[7:], 2).tolist()}")
P(f"  jackknife sigma:       {np.round(np.sqrt(np.diag(Cm))[:7], 2).tolist()} | {np.round(np.sqrt(np.diag(Cm))[7:], 2).tolist()}")
for nm, v in (("B canonical", MOD["mass"]["B"]["canonical"]), ("B alt", MOD["mass"]["B"]["alt"]), ("LCDM", MOD["mass"]["L"]),
              ("LCDM_m", MOD["mass"]["Lm"])):
    P(f"  {nm:12s}          {np.round(v[:7], 2).tolist()} | {np.round(v[7:], 2).tolist()}")
XB = {f: x2(D - MOD["mass"]["B"][f], Cm) for f in FOOTS}
XL = x2(D - MOD["mass"]["L"], Cm)
XLm = x2(D - MOD["mass"]["Lm"], Cm)
check("H1 [HEADLINE] B's LAW IS CONSISTENT WITH THE WITHIN-CLASS MASS DEPENDENCE: p > 0.01, both footings" + ("  [MUTATE: LCDM contrast injected]" if MUTATE else ""),
      "; ".join(f"{f}: chi2 {XB[f]:.2f}/14, p {pv(XB[f]):.2e} ({zs(pv(XB[f])):.2f} sigma)" for f in FOOTS), all(pv(XB[f]) > 0.01 for f in FOOTS))
check("H2 CFG67's COLOUR-SPLIT LCDM IS CONSISTENT WITH IT: p > 0.01",
      f"chi2 {XL:.2f}/14, p {pv(XL):.2e} ({zs(pv(XL)):.2f} sigma)", pv(XL) > 0.01)

# ================================================================== reported rows
R.banner("REPORTED ROWS")
blk = {0: slice(0, 7), 1: slice(7, 14)}
per = []
for c in (0, 1):
    Cc = Cm[blk[c], blk[c]]
    xs = {nm: float((D[blk[c]] - v[blk[c]]) @ np.linalg.solve(Cc, D[blk[c]] - v[blk[c]])) * (NPAT - 7 - 2) / (NPAT - 1)
          for nm, v in (("B", MOD["mass"]["B"]["canonical"]), ("LCDM", MOD["mass"]["L"]), ("LCDM_m", MOD["mass"]["Lm"]))}
    per.append(f"{'late' if c == 0 else 'early'}: " + ", ".join(f"{k} {v:.1f}/7 (p {pv(v, 7):.1e})" for k, v in xs.items()))
check("R1 (reported) per-class 7-bin chi2 (canonical B; Hartlap p = 7)", "; ".join(per), True, load_bearing=False)
amp = []
for c in (0, 1):
    eh, lh = esd_and_loo(HI[c]); el, ll = esd_and_loo(LO[c])
    wk = NNL[typ == c][:, K1].sum(0)
    a = float(np.sum(wk * np.log10(eh / el)) / np.sum(wk))
    reps = np.array([np.sum(wk * np.log10(lh[p] / ll[p])) / np.sum(wk) for p in range(NPAT)])
    sa = float(np.sqrt((NPAT - 1) / NPAT * np.sum((reps - reps.mean()) ** 2)))
    mods = {nm: float(np.sum(wk * np.log10(hi / lo)) / np.sum(wk)) for nm, hi, lo in
            (("B", HILO[c]["Bhi"], HILO[c]["Blo"]), ("LCDM", HILO[c]["Lhi"], HILO[c]["Llo"]))}
    amp.append(f"{'late' if c == 0 else 'early'}: data {a:+.3f} +- {sa:.3f} dex; B {mods['B']:+.3f}; LCDM {mods['LCDM']:+.3f}")
check("R2 (reported) the mass-split amplitude per class: pair-weighted mean over K1 of log10[ESD(high)/ESD(low)], jackknife sigma", "; ".join(amp),
      True, load_bearing=False)
amp2 = []
for c in (0, 1):
    eh, lh = esd_and_loo(HI[c]); el, ll = esd_and_loo(LO[c])
    wk = NNL[typ == c][:, K1].sum(0)
    a = float(np.log10(np.sum(wk * eh) / np.sum(wk * el)))
    reps = np.array([np.log10(np.sum(wk * lh[p]) / np.sum(wk * ll[p])) for p in range(NPAT)])
    sa = float(np.sqrt((NPAT - 1) / NPAT * np.sum((reps - reps.mean()) ** 2)))
    mods = {nm: float(np.log10(np.sum(wk * hi) / np.sum(wk * lo))) for nm, hi, lo in
            (("B", HILO[c]["Bhi"], HILO[c]["Blo"]), ("LCDM", HILO[c]["Lhi"], HILO[c]["Llo"]))}
    amp2.append(f"{'late' if c == 0 else 'early'}: data {a:+.3f} +- {sa:.3f} dex; B {mods['B']:+.3f}; LCDM {mods['LCDM']:+.3f}")
check("R2b (reported; ADDED AFTER THE FIRST RUN, disclosed: R2's per-bin log ratio is undefined where a noisy K1 bin's jackknife ESD goes "
      "negative) the mass-split amplitude as log10 of the ratio of pair-weighted sums over K1, jackknife sigma", "; ".join(amp2), True, load_bearing=False)
check("R3 (reported) LCDM_m (colour-blind Moster) on the 14 bins", f"chi2 {XLm:.2f}/14, p {pv(XLm):.2e}", True, load_bearing=False)
Dz, Lz = diff_vec(ZPAIRS)
Cz = jcov(Lz)
zrow = {nm: x2(Dz - v, Cz) for nm, v in (("zero", np.zeros(14)), ("B", MOD["z"]["B"]["canonical"]), ("LCDM", MOD["z"]["L"]))}
check("R4 (reported) the redshift split (high-z minus low-z within class; the photo-z check): chi2/14 against zero, B and LCDM",
      ", ".join(f"{k} {v:.1f} (p {pv(v):.1e})" for k, v in zrow.items()) + f"; data late {np.round(Dz[:7], 2).tolist()} early {np.round(Dz[7:], 2).tolist()}",
      True, load_bearing=False)

h1 = all(pv(XB[f]) > 0.01 for f in FOOTS)
h2 = pv(XL) > 0.01
if h1 and not h2 and pow_ >= 9:
    reading = "the data follow B's mass-independence and reject LCDM's mass dependence: a LCDM-specific failure in shared machinery"
elif (not h1) and h2:
    reading = "the lensing signal at fixed g_bar rises with mass as LCDM predicts: a second B-specific failure"
elif h1 and h2:
    reading = "both models are acceptable" + (" (NON-DISCRIMINATING: power below 9)" if pow_ < 9 else "")
elif h1 and not h2:
    reading = "B passes and LCDM fails, but the power is below 9: weakly discriminating"
else:
    reading = "neither model describes the within-class mass dependence"
P(f"\n    READING (declared): {reading}")
R.num("D", D.tolist()); R.num("sigma", np.sqrt(np.diag(Cm)).tolist()); R.num("chi2", dict(B=XB, LCDM=XL, LCDM_m=XLm)); R.num("power", pow_)
R.num("null_mean", mn); R.num("models", {k: (v.tolist() if isinstance(v, np.ndarray) else {f: x.tolist() for f, x in v.items()})
                                         for k, v in MOD["mass"].items()})
R.num("zsplit", zrow); R.num("medians", dict(M=MED_M, z=MED_Z)); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
