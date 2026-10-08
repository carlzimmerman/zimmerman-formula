#!/usr/bin/env python3
"""CFG485 -- DOES SETTLING COMPLETENESS PRODUCE THE KiDS EARLY/LATE SPLIT?  Criteria: FROZEN_CRITERIA.md (019eb965a, committed alone first).
  calib    CFG95's stellar-mass calibration, executed read-only from CFG95_kids_split_own_calibration.py up to its C1-C3 banner (MUTATE off).
  ages     no stellar-population age on disk -> declared proxy P1 = LePhare sSFR formation time t_age = min(10^(MASS_BEST - SFR_BEST) yr, t_U(z)).
  settle   f_i = 1 - exp(-sqrt(4 pi G rho_bar_i) t_age_i), lambda = 1, rho_bar = (M_b/f_b)/(4pi/3 r_edge^3), r_edge = r_M/ln(1/(1-f_b)) = 5.850 r_M,
           r_M = sqrt(G M_b,true/a0), f_b = 0.02237/0.14237 (engine).
  model    nu_mono phantom (CFG7_common.M_law) truncated at r_edge(M_b), x f, + true point mass; CFG95's stack (CFG61 grid, log-M_b interpolation);
           CFG413's free two-halo amplitude on the difference (one amplitude, exact; 6 dof).
  data     CFG95's released split (C_D) and re-measured split (CFG88 jackknife, Hartlap 41/49) on K1.
  compare  S (per-lens f) vs B2 (uniform f = all-lens M_gal-weighted mean) vs B1 (CFG95's calibrated law to 0.40 r_ta, f = 1).
VERDICT  per cell (data set x footing): S if p_S > 0.05 and dchi2 >= 4 vs B1 and vs B2; C if s_hat/sigma_s <= -2; else N.
         SUPPORTED = all four S; CONTRADICTED = all four C; else NOT DIAGNOSTIC.
MUTATE   CFG485_MUTATE=1: t_age permuted across all lenses (default_rng(485)); H1 must FAIL.
Run: nice -n 15 python3 campaign_fresh_gravity/CFG485_kids_split_settling_completeness/cfg485_settling_split.py   (CFG485_MUTATE=1 for the control)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import io, json, math, contextlib, time
import numpy as np
from scipy.stats import chi2 as CHI2, norm
from astropy.io import fits

HERE = os.path.dirname(os.path.abspath(__file__))
CFGDIR = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, CFGDIR)
import CFG7_common as C
MUTATE = os.environ.get("CFG485_MUTATE", "0") == "1"
try:
    os.nice(15)
except OSError:
    pass
R = C.Report("cfg485_settling_split", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: nice")[0].strip())
if MUTATE:
    P("\n  *** CFG485_MUTATE=1: t_age permuted across all lenses (default_rng(485)) -- H1 must FAIL ***")
FOOTS = ("canonical", "alt")
FB = 0.02237 / 0.14237                         # engine f_b (CFG423/CFG424)
LNE = math.log(1.0 / (1.0 - FB))               # r_edge = r_M / LNE  (= 5.850 r_M)
F_RET = 0.10                                   # R5 census-retention edge


# ================================================================== Step 0: CFG95 read-only (its calibration, data, covariances, stack)
def lane_prefix(fname, marker):
    _e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
    path = os.path.join(CFGDIR, fname)
    src = open(path).read()
    g = {"__file__": path, "__name__": "lane_" + fname}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(src[:src.index(marker)], fname, "exec"), g)
    finally:
        os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
    return g


T0 = time.time()
g95 = lane_prefix("CFG95_kids_split_own_calibration.py", "# ================================================================== C1-C3")
g61 = g95["g61"]
LMG, ZG, RG, EDGES, SUB, LRG, LOGMB = (g95[k] for k in ("LMG", "ZG", "RG", "EDGES", "SUB", "LRG", "LOGMB"))
weights, fcold, G_SI, MSUN, MPC = g95["weights"], g95["fcold"], g95["G_SI"], g95["MSUN"], g95["MPC"]
delta_early, delta_late, stack_true, x2_95 = g95["delta_early"], g95["delta_late"], g95["stack_true"], g95["x2"]
DSL, PROF, K1, idx = g95["DSL"], g95["PROF"], g95["K1"], g95["idx"]
CD, CK, HART, DOBS, DREM, C30 = g95["CD"], g95["CK"], g95["HART"], g95["DOBS"], g95["DREM"], g95["C30"]
d_late, d_early = g95["d_late"], g95["d_early"]
project, rgrid = g61["project"], g61["rgrid"]
lM, Mg, typ, zl, iz, im = g61["lM"], g61["Mg"], g61["typ"], g61["zl"], g61["iz"], g61["im"]
NLMG, NZG, PK = len(LMG), len(ZG), len(K1)
NL = len(lM)
P(f"\n  Step 0: CFG95 executed read-only ({time.time() - T0:.0f} s); K1 = {K1}; lenses {NL:,} (late {(typ == 0).sum():,}, early {(typ == 1).sum():,})")
P(f"  f_b = {FB:.6f}; r_edge / r_M = 1/ln(1/(1-f_b)) = {1 / LNE:.5f}; CFG61's own FB (not used) = {g61['FB']}")

# covariance inverses (re-measured: Hartlap-scaled), as in CFG95's x2
CI = {"released": np.linalg.inv(CD), "remeasured": HART * np.linalg.inv(CK)}
DATA = {"released": DOBS, "remeasured": DREM}
SETS = ("released", "remeasured")


def chi2_free(r, Ci, T):
    A = float((T @ Ci @ r) / (T @ Ci @ T))
    rr = r - A * T
    return float(rr @ Ci @ rr), A


def chi2_none(r, Ci):
    return float(r @ Ci @ r)


def pv(x, dof):
    return float(CHI2.sf(x, dof))


def zs(p):
    return float(norm.isf(p / 2)) if p > 0 else float("inf")


# ================================================================== C1: CFG95's machinery reproduces its committed H numbers
R.banner("C1-C6  CONTROLS")
J95 = json.load(open(os.path.join(CFGDIR, "CFG95_kids_split_own_calibration_results.json")))["numbers"]["H"]
B1RAW = {}
c1dev = 0.0
for foot in FOOTS:
    ml = stack_true(0, foot, lambda lm, f=foot: delta_late(f))
    me = stack_true(1, foot, lambda lm, f=foot: delta_early(lm, f))
    D = (me - ml)[idx]
    B1RAW[foot] = dict(ml=ml, me=me, D=D)
    for s_, key in (("released", "released"), ("remeasured", "remeasured")):
        c1dev = max(c1dev, abs(x2_95(D, s_) - J95[foot][key]))
check("C1 CONTROL: CFG95's machinery (read-only) reproduces CFG95's committed H numbers to 1e-6 (released 20.3037 / 18.5935; "
      "re-measured 26.6775 / 24.7862)",
      "; ".join(f"{f}: released {x2_95(B1RAW[f]['D'], 'released'):.4f}, re-measured {x2_95(B1RAW[f]['D'], 'remeasured'):.4f}" for f in FOOTS)
      + f"; max |diff| {c1dev:.1e}", c1dev < 1e-6)


# ================================================================== this lane's vectorised stack (CFG95's arithmetic, split into parts)
def contrib(cls, foot, tables, dfun):
    """per-cell, per-bin sums of CFG95's stack: phantom part (f = 1), point-mass part, two-halo template; den per bin.
    tables[(foot, b)] -> (NLMG, len(RG)) array of the phantom Delta Sigma [Msun/Mpc^2] at the node masses."""
    w = weights(cls)
    fc = np.array([fcold(lm) for lm in LMG])
    dl = np.array([dfun(lm) for lm in LMG])
    lmbt = np.log10(10 ** LMG * (10 ** dl + fc))
    ii = np.clip(np.searchsorted(LOGMB, lmbt, side="right") - 1, 0, NLMG - 2)
    tt = np.clip((lmbt - LOGMB[ii]) / (LOGMB[ii + 1] - LOGMB[ii]), 0.0, 1.0)
    NP_ = np.zeros((NLMG, NZG, 15)); NB_ = np.zeros((NLMG, NZG, 15)); NT_ = np.zeros((NLMG, NZG, 15)); den = np.zeros(15)
    for k in range(15):
        lg = np.linspace(math.log(EDGES[k]), math.log(EDGES[k + 1]), SUB + 1)
        gs = np.exp(0.5 * (lg[1:] + lg[:-1]))
        for a in range(NLMG):
            for b in range(NZG):
                if w[a, b] <= 0:
                    continue
                t = tt[a]
                Mtab = 10 ** LMG[a] * (1 + fc[a])
                Rj = np.sqrt(G_SI * Mtab * MSUN / gs) / MPC
                xr = np.log(Rj)
                prof = tables[(foot, b)]
                dsl = (1 - t) * np.interp(xr, LRG, prof[ii[a]]) + t * np.interp(xr, LRG, prof[ii[a] + 1])
                wj = w[a, b] / gs
                NP_[a, b, k] = float(np.sum(wj * dsl))
                NB_[a, b, k] = float(np.sum(wj * (10 ** lmbt[a] / (math.pi * Rj ** 2))))
                NT_[a, b, k] = float(np.sum(wj * Rj ** -0.8 * 1e12))
                den[k] += float(np.sum(wj))
    return dict(NP=NP_, NB=NB_, NT=NT_, den=den, w=w)


def parts(cb, qbar=None):
    """stack = Ph + Bar - Q  [Msun/pc^2]; Q = sum qbar*NP / den (qbar per cell); T = two-halo template."""
    sc = cb["den"] * 1e12
    Ph = cb["NP"].sum((0, 1)) / sc; Bar = cb["NB"].sum((0, 1)) / sc; T = cb["NT"].sum((0, 1)) / sc
    Q = np.zeros(15) if qbar is None else np.einsum("ab,abk->k", qbar, cb["NP"]) / sc
    return Ph, Bar, T, Q


DF = {foot: {0: (lambda lm, f=foot: delta_late(f)), 1: (lambda lm, f=foot: delta_early(lm, f))} for foot in FOOTS}
t1 = time.time()
CB95 = {(foot, c): contrib(c, foot, DSL, DF[foot][c]) for foot in FOOTS for c in (0, 1)}
c2dev = 0.0; c2x = 0.0
for foot in FOOTS:
    Phl, Barl, _, _ = parts(CB95[(foot, 0)]); Phe, Bare, _, _ = parts(CB95[(foot, 1)])
    D = ((Phe + Bare) - (Phl + Barl))[idx]
    c2dev = max(c2dev, float(np.max(np.abs(D / B1RAW[foot]["D"] - 1))))
    c2x = max(c2x, abs(chi2_none(DOBS - D, CI["released"]) - J95[foot]["released"]), abs(chi2_none(DREM - D, CI["remeasured"]) - J95[foot]["remeasured"]))
check("C2 CONTROL: this lane's vectorised stack (CFG61's 0.40 r_ta tables, f = 1, no two-halo) reproduces CFG95's model D on K1 to 1e-9 "
      "and its chi2 to 1e-6, both footings",
      f"max relative deviation of D {c2dev:.1e}; max |chi2 diff| {c2x:.1e} ({time.time() - t1:.0f} s)", c2dev < 1e-9 and c2x < 1e-6)


# ================================================================== truncated phantom tables at the mass-conserving edge (and the census edge, R5)
def r_M(Mb, foot):
    return np.sqrt(C.GMPC * np.asarray(Mb, float) / C.A0[foot])          # Mpc


def edge_tables(foot, lnfac):
    out = np.zeros((NLMG, len(RG)))
    for a, lm in enumerate(LMG):
        Mb = 10 ** lm * (1 + fcold(lm))
        re = float(r_M(Mb, foot)) / lnfac
        rc = np.minimum(rgrid, re)
        ML = np.asarray(C.M_law(Mb, rc, C.A0[foot], C.nu_mono), float)
        out[a] = project(rgrid, ML - Mb, RG)
    return {(foot, b): out for b in range(NZG)}


LN_CENSUS = math.log(1.0 + F_RET * FB / (1.0 - FB))
t1 = time.time()
TE = {}; TCEN = {}
for foot in FOOTS:
    TE.update(edge_tables(foot, LNE)); TCEN.update(edge_tables(foot, LN_CENSUS))
P(f"  edge tables built ({time.time() - t1:.0f} s): mass-conserving edge {1 / LNE:.4f} r_M; census edge (f_ret {F_RET}) {1 / LN_CENSUS:.2f} r_M")

c3 = []
for foot in FOOTS:
    for Mb in (1e9, 10 ** 10.5, 1e12):
        re = float(r_M(Mb, foot)) / LNE
        Mph = float(C.M_law(Mb, re, C.A0[foot], C.nu_mono)) - Mb
        c3.append(abs(Mph / ((1 - FB) / FB * Mb) - 1))
check("C3 CONTROL: the nu_mono phantom at r = r_M/ln(1/(1-f_b)) = 5.850 r_M equals (1-f_b)/f_b M_b = 5.364 M_b to 1e-3 (M_b 1e9, 1e10.5, 1e12; both footings)",
      f"(1-f_b)/f_b = {(1 - FB) / FB:.4f}; max relative deviation {max(c3):.1e}", max(c3) < 1e-3)

gc = np.sqrt(EDGES[1:] * EDGES[:-1])
c4 = []
for lm in (10.325, 10.775, 11.125):
    Mb = 10 ** lm * (1 + fcold(lm)); lmb = math.log10(Mb)
    re = float(r_M(Mb, "canonical")) / LNE
    ML = np.asarray(C.M_law(Mb, np.minimum(rgrid, re), C.A0["canonical"], C.nu_mono), float)
    Rk = np.sqrt(G_SI * Mb * MSUN / gc[idx]) / MPC
    direct = project(rgrid, ML - Mb, Rk) + Mb / (math.pi * Rk ** 2)
    i = int(np.clip(np.searchsorted(LOGMB, lmb, side="right") - 1, 0, NLMG - 2))
    t = (lmb - LOGMB[i]) / (LOGMB[i + 1] - LOGMB[i])
    prof = TE[("canonical", 2)]
    interp = (1 - t) * np.interp(np.log(Rk), LRG, prof[i]) + t * np.interp(np.log(Rk), LRG, prof[i + 1]) + Mb / (math.pi * Rk ** 2)
    c4.append(float(np.max(np.abs(interp / direct - 1))))
check("C4 CONTROL: the log-M_b interpolation of the truncated phantom Delta Sigma (+ point mass) matches direct profiles at three off-node masses to 1% (K1 radii)",
      f"max relative deviations at log M* 10.325 / 10.775 / 11.125: {', '.join(f'{x:.1e}' for x in c4)}", max(c4) < 0.01)

t1 = time.time()
CBE = {(foot, c): contrib(c, foot, TE, DF[foot][c]) for foot in FOOTS for c in (0, 1)}
CBC = {(foot, c): contrib(c, foot, TCEN, DF[foot][c]) for foot in FOOTS for c in (0, 1)}
P(f"  edge / census stacks built ({time.time() - t1:.0f} s)")
c5 = 0.0
for foot in FOOTS:
    Te = parts(CBE[(foot, 1)])[2][idx]; Tl = parts(CBE[(foot, 0)])[2][idx]
    rr = Te / Tl
    c5 = max(c5, float(np.max(np.abs(rr / rr.mean() - 1))))
check("C5 CONTROL: the early and late two-halo templates are proportional over K1 (max rel. deviation of T_e/T_l from its mean < 1e-9)",
      f"max relative deviation {c5:.1e}; T_e/T_l = {float((parts(CBE[('canonical', 1)])[2] / parts(CBE[('canonical', 0)])[2])[idx].mean()):.4f}", c5 < 1e-9)

# ================================================================== C6: lenses <-> LePhare (CFG446's key); the age proxy
LR = os.path.join(C.REPO, "real_research", "data", "lensing_rar")
LN = np.load(os.path.join(LR, "lr_lenses.npz"))
bs = fits.open(os.path.join(LR, "KiDS_DR4_brightsample.fits"), memmap=True)[1].data
lp = fits.open(os.path.join(LR, "KiDS_DR4_brightsample_LePhare.fits"), memmap=True)[1].data
ids_ok = bool(np.array_equal(bs["ID"], lp["ID"]))
ra = np.array(bs["RAJ2000"], "f8"); dec = np.array(bs["DECJ2000"], "f8")
key = lambda a, d: np.round(a * 1e7).astype(np.int64) * 10 ** 10 + np.round((d + 90) * 1e7).astype(np.int64)
kb, kl = key(ra, dec), key(LN["ra"], LN["dec"])
order = np.argsort(kb, kind="stable"); ks = kb[order]
pos = np.minimum(np.searchsorted(ks, kl), len(ks) - 1)
ix = order[pos]
matched = bool(np.all(ks[pos] == kl)) and bool(np.all(ra[ix] == LN["ra"])) and bool(np.all(dec[ix] == LN["dec"]))
ur = np.array(lp["MAG_ABS_u"][ix] - lp["MAG_ABS_r"][ix], "f8")
typ_ok = bool(np.array_equal((ur > 2.0).astype(int), typ))
lm_ok = bool(np.array_equal(np.array(lp["MASS_MED"][ix], "f8") + 0.15, lM))
same_order = bool(np.array_equal(LN["logM"], lM)) and bool(np.array_equal(LN["z"], zl))
check("C6 CONTROL: every lens matches the LePhare file by exact position (IDs row-aligned); u - r > 2 reproduces typ; log M* = MASS_MED + 0.15",
      f"{NL:,} lenses; IDs aligned {ids_ok}; exact match {matched}; typ {typ_ok}; logM {lm_ok}; lr_lenses order = CFG61's {same_order}",
      ids_ok and matched and typ_ok and lm_ok and same_order)

mbest = np.array(lp["MASS_BEST"][ix], "f8"); sbest = np.array(lp["SFR_BEST"][ix], "f8")
H0 = 100 * C.H_PL; OMm = C.OM_PL; OL = 1 - OMm


def t_univ(z):                                   # Gyr, flat LCDM
    a = 1.0 / (1.0 + np.asarray(z, float))
    return 2.0 / (3.0 * H0 * math.sqrt(OL)) * np.arcsinh(math.sqrt(OL / OMm) * a ** 1.5) * C.UNIT_GYR


TU = t_univ(zl)
bad = ~np.isfinite(mbest) | ~np.isfinite(sbest) | (mbest < -90) | (sbest < -90)
logt = np.where(bad, 3.0, np.minimum(mbest - sbest - 9.0, 3.0))           # log10 Gyr
TAGE = np.where(bad, TU, np.minimum(10 ** logt, TU))
capped = (~bad) & (10 ** logt >= TU)
if MUTATE:
    TAGE = TAGE[np.random.default_rng(485).permutation(NL)]
EARLY, LATE = typ == 1, typ == 0
med_e, med_l = float(np.median(TAGE[EARLY])), float(np.median(TAGE[LATE]))
check("C7 (proxy sanity): the age proxy orders the classes -- median t_age(early) >= median t_age(late)",
      f"median t_age early {med_e:.2f} Gyr, late {med_l:.2f} Gyr; fallback (bad MASS_BEST/SFR_BEST) {int(bad.sum()):,}; "
      f"capped at t_U(z) early {int((capped & EARLY).sum()):,} / late {int((capped & LATE).sum()):,}", med_e >= med_l)


# ================================================================== per-lens settled fractions
def mb_true(foot):
    d = np.where(EARLY, delta_early(lM, foot), delta_late(foot))
    return 10 ** lM * (10 ** d + fcold(lM))


def x_edge(foot, lnfac, ages, mtot_over_mb, local=False):
    """lambda * sqrt(4 pi G rho) * t_age for every lens (dimensionless); rho = mean inside the edge (or local at the edge: /3)."""
    Mb = mb_true(foot)
    re = r_M(Mb, foot) / lnfac
    k = 1.0 if local else 3.0
    rate = np.sqrt(k * C.GMPC * Mb * mtot_over_mb / re ** 3)            # (km/s)/Mpc
    return rate * ages / C.UNIT_GYR


def cellmean(q, cls):
    sel = typ == cls
    num = np.zeros((NLMG, NZG)); w = np.zeros((NLMG, NZG))
    np.add.at(num, (im[sel], iz[sel]), Mg[sel] * q[sel]); np.add.at(w, (im[sel], iz[sel]), Mg[sel])
    return np.where(w > 0, num / np.where(w > 0, w, 1.0), 0.0)


def score(CB, q, foot, label):
    """D for S, B2; chi2 (free 2h and none) for S, B2, B1; sign test; SNR of the increment.  q per lens (= 1 - f)."""
    cbl, cbe = CB[(foot, 0)], CB[(foot, 1)]
    qall = float(np.sum(Mg * q) / np.sum(Mg))
    Phl, Barl, _, Ql = parts(cbl, cellmean(q, 0)); Phe, Bare, _, Qe = parts(cbe, cellmean(q, 1))
    # the all-lens template (both classes, same stack weights); proportional to each class's (C5), so one amplitude is exact
    wl, we = cbl["den"], cbe["den"]
    T = ((cbl["NT"].sum((0, 1)) + cbe["NT"].sum((0, 1))) / (wl + we) / 1e12)[idx]
    D1 = ((Phe + Bare) - (Phl + Barl))[idx]
    DB2 = D1 - (qall * Phe - qall * Phl)[idx]
    inc = -((Qe - qall * Phe) - (Ql - qall * Phl))[idx]                    # D_S - D_B2, from q differences
    DS = DB2 + inc
    DB1 = B1RAW[foot]["D"]
    out = dict(label=label, qall=qall, qe=float(np.sum(Mg[EARLY] * q[EARLY]) / np.sum(Mg[EARLY])),
               ql=float(np.sum(Mg[LATE] * q[LATE]) / np.sum(Mg[LATE])), DS=DS.tolist(), DB2=DB2.tolist(), DB1=DB1.tolist(), inc=inc.tolist())
    for s_ in SETS:
        Ci, d = CI[s_], DATA[s_]
        rB2 = d - DB2
        rS = rB2 - inc
        xS, AS = chi2_free(rS, Ci, T); xB2, AB2 = chi2_free(rB2, Ci, T); xB1, AB1 = chi2_free(d - DB1, Ci, T)
        nS, nB2, nB1 = chi2_none(rS, Ci), chi2_none(rB2, Ci), chi2_none(d - DB1, Ci)
        nrm = float(np.sqrt(inc @ inc))
        if nrm > 0 and np.isfinite(nrm):
            u = inc / nrm
            X = np.stack([u, T], 1)
            F = X.T @ Ci @ X
            beta = np.linalg.solve(F, X.T @ Ci @ rB2)
            cov = np.linalg.inv(F)
            s_hat, s_sig = float(beta[0] / nrm), float(math.sqrt(cov[0, 0]) / nrm)
            ratio = float(beta[0] / math.sqrt(cov[0, 0]))
            snr = float(math.sqrt(inc @ Ci @ inc))
        else:
            s_hat = s_sig = ratio = float("nan"); snr = 0.0
        pS = pv(xS, PK - 1)
        dB1, dB2_ = xB1 - xS, xB2 - xS
        if pS > 0.05 and dB1 >= 4 and dB2_ >= 4:
            cell = "S"
        elif np.isfinite(ratio) and ratio <= -2:
            cell = "C"
        else:
            cell = "N"
        out[s_] = dict(chi2_S=xS, chi2_B2=xB2, chi2_B1=xB1, A_S=AS, A_B2=AB2, A_B1=AB1, p_S=pS, p_B2=pv(xB2, PK - 1), p_B1=pv(xB1, PK - 1),
                       dchi2_B1=dB1, dchi2_B2=dB2_, nofree_S=nS, nofree_B2=nB2, nofree_B1=nB1, s_hat=s_hat, s_sig=s_sig, s_ratio=ratio,
                       snr_inc=snr, cell=cell)
    return out


def show(res, tag):
    for foot in FOOTS:
        v = res[foot]
        P(f"    [{tag}] {foot:9s} M_gal-weighted mean q = 1 - f: early {v['qe']:.3e}, late {v['ql']:.3e}, all {v['qall']:.3e}")
        P(f"        increment D_S - D_B2 on K1 [Msun/pc^2]: {np.array2string(np.array(v['inc']), precision=3, separator=', ')}")
        for s_ in SETS:
            c = v[s_]
            P(f"        {s_:10s}: chi2 S {c['chi2_S']:.3f} (p {c['p_S']:.2e}) | B2 {c['chi2_B2']:.3f} | B1 {c['chi2_B1']:.3f} (p {c['p_B1']:.2e}) /6 "
              f"| dchi2 vs B1 {c['dchi2_B1']:+.3f}, vs B2 {c['dchi2_B2']:+.3e} | s_hat/sigma {c['s_ratio']:+.2f}, SNR_inc {c['snr_inc']:.2e} -> {c['cell']}")


# ================================================================== H1 / H2: the primary prediction
R.banner("PRIMARY  f = 1 - exp(-sqrt(4 pi G rho_bar) t_age), rho_bar inside r_edge = 5.850 r_M, P1 ages, free two-halo (6 dof)")
MTOT_E = 1.0 / FB
QP = {}
RES = {}
for foot in FOOTS:
    x = x_edge(foot, LNE, TAGE, MTOT_E)
    QP[foot] = np.exp(-x)
    RES[foot] = score(CBE, QP[foot], foot, "primary")
show(RES, "primary")
P("    data released   : " + np.array2string(DOBS, precision=2, separator=", "))
P("    data re-measured: " + np.array2string(DREM, precision=2, separator=", "))
for foot in FOOTS:
    P(f"    {foot:9s} model D_S  : " + np.array2string(np.array(RES[foot]["DS"]), precision=3, separator=", ")
      + "\n              model D_B1 : " + np.array2string(np.array(RES[foot]["DB1"]), precision=3, separator=", "))
cells = {(s_, f): RES[f][s_]["cell"] for s_ in SETS for f in FOOTS}
if all(v == "S" for v in cells.values()):
    VERDICT = "SUPPORTED"
elif all(v == "C" for v in cells.values()):
    VERDICT = "CONTRADICTED"
else:
    VERDICT = "NOT DIAGNOSTIC"
check("H1 [HEADLINE; MUTATE must fail] SUPPORTED: all four cells have p_S > 0.05 and dchi2 >= 4 vs B1 and vs B2"
      + ("  [MUTATE: ages shuffled]" if MUTATE else ""),
      "; ".join(f"{s_}/{f}: {RES[f][s_]['cell']} (p_S {RES[f][s_]['p_S']:.2e}, dB1 {RES[f][s_]['dchi2_B1']:+.2f}, dB2 {RES[f][s_]['dchi2_B2']:+.2e})"
                for s_ in SETS for f in FOOTS), VERDICT == "SUPPORTED")
check("H2 the prediction's sign survives: no cell has s_hat/sigma_s <= -2",
      "; ".join(f"{s_}/{f}: s_hat/sigma {RES[f][s_]['s_ratio']:+.2f} (SNR_inc {RES[f][s_]['snr_inc']:.1e})" for s_ in SETS for f in FOOTS),
      all(not (np.isfinite(RES[f][s_]["s_ratio"]) and RES[f][s_]["s_ratio"] <= -2) for s_ in SETS for f in FOOTS))
small = all(RES[f][s_]["snr_inc"] < 2 for s_ in SETS for f in FOOTS)
P(f"\n    VERDICT (frozen rule): {VERDICT}   [cells {cells}]")
if small:
    P("    The settling increment's own signal-to-noise is < 2 in every cell: at lambda = 1 and the 5.85 r_M edge the reading cannot produce the split.")

# ================================================================== reported rows
R.banner("REPORTED ROWS (no verdict weight)")
# R1 distributions
r1 = {}
for foot in FOOTS:
    q = QP[foot]; Mb = mb_true(foot); re = r_M(Mb, foot) / LNE
    tdyn = C.UNIT_GYR / np.sqrt(3 * C.GMPC * Mb * MTOT_E / re ** 3)
    row = {}
    for nm, m in (("early", EARLY), ("late", LATE)):
        row[nm] = dict(t_age_pct=np.percentile(TAGE[m], [5, 50, 95]).tolist(), t_dyn_pct=np.percentile(tdyn[m], [5, 50, 95]).tolist(),
                       q_pct=np.percentile(q[m], [5, 50, 95]).tolist(), q_wmean=float(np.sum(Mg[m] * q[m]) / np.sum(Mg[m])),
                       n_q_gt_1e3=int((q[m] > 1e-3).sum()), n_q_gt_0p1=int((q[m] > 0.1).sum()), n=int(m.sum()))
    r1[foot] = row
check("R1 (reported) per-class t_age, t_dyn (mean density inside r_edge) and q = 1 - f",
      " | ".join(f"{foot}: " + "; ".join(f"{nm} t_age 5/50/95% {np.round(r['t_age_pct'], 2).tolist()} Gyr, t_dyn {np.round(r['t_dyn_pct'], 3).tolist()} Gyr, "
                                         f"q 5/50/95% {[float(f'{v:.2e}') for v in r['q_pct']]}, M_gal-mean q {r['q_wmean']:.2e}, "
                                         f"N(q>1e-3) {r['n_q_gt_1e3']:,}, N(q>0.1) {r['n_q_gt_0p1']:,} of {r['n']:,}"
                                         for nm, r in r1[foot].items()) for foot in FOOTS)
      + f" | fallback {int(bad.sum()):,}", True, load_bearing=False)


def row_summary(res):
    return "; ".join(f"{f}/{s_}: S {res[f][s_]['chi2_S']:.2f} (p {res[f][s_]['p_S']:.1e}), dB1 {res[f][s_]['dchi2_B1']:+.2f}, dB2 {res[f][s_]['dchi2_B2']:+.2e}, "
                     f"s/sig {res[f][s_]['s_ratio']:+.2f}, SNR {res[f][s_]['snr_inc']:.1e} [{res[f][s_]['cell']}]; q_e {res[f]['qe']:.1e} q_l {res[f]['ql']:.1e}"
                     for f in FOOTS for s_ in SETS)


ROWS = {}
# R2 local density at the edge (slowest shell); R3 P2 ages; R4 both
for nm, ages, local in (("R2_local_edge_density", TAGE, True), ("R3_P2_half_age", 0.5 * TAGE, False), ("R4_local_and_P2", 0.5 * TAGE, True)):
    ROWS[nm] = {f: score(CBE, np.exp(-x_edge(f, LNE, ages, MTOT_E, local=local)), f, nm) for f in FOOTS}
    show(ROWS[nm], nm)
# R5 census-retention edge (f_ret = 0.10)
MTOT_C = 1.0 + (1 - FB) / (FB * F_RET)
ROWS["R5_census_edge"] = {f: score(CBC, np.exp(-x_edge(f, LN_CENSUS, TAGE, MTOT_C)), f, "R5_census_edge") for f in FOOTS}
show(ROWS["R5_census_edge"], "R5_census_edge")
# R6 CFG95's own edge (0.40 r_ta), cell-level density M_law(<r_e) / (4pi/3 r_e^3), per-lens ages
R6 = {}
for foot in FOOTS:
    rate = np.zeros((NLMG, NZG))
    for a, lm in enumerate(LMG):
        Mb = 10 ** lm * (1 + fcold(lm))
        for b, z in enumerate(ZG):
            re = PROF[(foot, "red", lm, z)]["re"]
            Mt = float(C.M_law(Mb, re, C.A0[foot], C.nu_mono))
            rate[a, b] = math.sqrt(3 * C.GMPC * Mt / re ** 3)
    R6[foot] = score(CB95, np.exp(-rate[im, iz] * TAGE / C.UNIT_GYR), foot, "R6_cfg95_edge")
ROWS["R6_cfg95_edge"] = R6
show(R6, "R6_cfg95_edge")
for nm in ROWS:
    check(f"{nm} (reported)", row_summary(ROWS[nm]), True, load_bearing=False)

# R7 no two-halo (CFG95's exact statistic, 7 dof)
check("R7 (reported) no two-halo term (7 dof): S, B2, B1 on the primary prediction",
      "; ".join(f"{f}/{s_}: S {RES[f][s_]['nofree_S']:.2f} (p {pv(RES[f][s_]['nofree_S'], PK):.1e}), B2 {RES[f][s_]['nofree_B2']:.2f}, "
                f"B1 {RES[f][s_]['nofree_B1']:.2f} (p {pv(RES[f][s_]['nofree_B1'], PK):.1e})" for f in FOOTS for s_ in SETS), True, load_bearing=False)

# R8 absolute per-class profiles (released per-class blocks), two-halo profiled per class
r8 = {}
for foot in FOOTS:
    r8[foot] = {}
    for cls, nm, dd, blk in ((1, "early", d_early, slice(15, 30)), (0, "late", d_late, slice(0, 15))):
        cb = CBE[(foot, cls)]
        q = QP[foot]
        Ph, Bar, T, Qc = parts(cb, cellmean(q, cls))
        mS = (Ph + Bar - Qc)[idx]
        cb1 = CB95[(foot, cls)]; Ph1, Bar1, T1, _ = parts(cb1)
        m1 = (Ph1 + Bar1)[idx]
        Cb = C30[blk, blk][np.ix_(idx, idx)]; Ci = np.linalg.inv(Cb)
        xs_, As_ = chi2_free(dd[idx] - mS, Ci, T[idx]); x1_, A1_ = chi2_free(dd[idx] - m1, Ci, T1[idx])
        r8[foot][nm] = dict(chi2_S=xs_, A_S=As_, chi2_B1=x1_, A_B1=A1_, model_S=mS.tolist(), model_B1=m1.tolist(), data=dd[idx].tolist(),
                            nofree_S=chi2_none(dd[idx] - mS, Ci), nofree_B1=chi2_none(dd[idx] - m1, Ci))
check("R8 (reported) absolute per-class profiles on K1 (released blocks, two-halo profiled per class, 6 dof)",
      " | ".join(f"{f}: " + "; ".join(f"{nm} S {r['chi2_S']:.1f} (A {r['A_S']:.2f}; no-2h {r['nofree_S']:.1f}), B1 {r['chi2_B1']:.1f} (A {r['A_B1']:.2f}; no-2h {r['nofree_B1']:.1f})"
                                      for nm, r in r8[f].items()) for f in FOOTS), True, load_bearing=False)
for f in FOOTS:
    for nm, r in r8[f].items():
        P(f"      {f:9s} {nm:5s} data {np.round(r['data'], 2).tolist()}\n                      S (1-halo) {np.round(r['model_S'], 2).tolist()}\n"
          f"                      B1 (1-halo) {np.round(r['model_B1'], 2).tolist()}")

# R9 total-D sign
r9 = {f: dict(DS_pos=int((np.array(RES[f]["DS"]) > 0).sum()), DOBS_pos=int((DOBS > 0).sum()), DREM_pos=int((DREM > 0).sum())) for f in FOOTS}
check("R9 (reported) total-D sign: bins of K1 with D > 0 (prediction / released / re-measured)",
      "; ".join(f"{f}: D_S > 0 in {r9[f]['DS_pos']}/7; data {r9[f]['DOBS_pos']}/7 and {r9[f]['DREM_pos']}/7" for f in FOOTS), True, load_bearing=False)

# MUTATE note
if MUTATE:
    P("\n    MUTATE: ages shuffled across all lenses; class contrast of M_gal-mean q per footing: "
      + "; ".join(f"{f}: early {RES[f]['qe']:.3e} vs late {RES[f]['ql']:.3e}" for f in FOOTS))

P(f"\n    READING: verdict {VERDICT} (frozen rule).  kappa = 1/2 fitted; footings never pooled; cold mass still required; no particle.")
R.num("verdict", VERDICT); R.num("cells", {f"{s_}|{f}": v for (s_, f), v in cells.items()})
R.num("primary", RES); R.num("rows", ROWS); R.num("R1", r1); R.num("R8", r8); R.num("R9", r9)
R.num("ages", dict(median_early=med_e, median_late=med_l, fallback=int(bad.sum()), capped_early=int((capped & EARLY).sum()),
                   capped_late=int((capped & LATE).sum())))
R.num("constants", dict(f_b=FB, edge_over_rM=1 / LNE, census_edge_over_rM=1 / LN_CENSUS, f_ret=F_RET, lam=1.0))
nf = R.write(HERE)
sys.exit(1 if nf else 0)
