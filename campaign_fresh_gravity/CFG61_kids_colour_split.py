#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG61 -- DOES B's DERIVED RULE REPRODUCE THE KiDS-1000 EARLY/LATE LENSING SPLIT, WHERE THE COLOUR-BLIND LAW CANNOT?

The criteria were frozen and committed BEFORE this script existed: campaign_fresh_gravity/CFG61_FROZEN_CRITERIA.md (commit d7aecf12b).  This script
implements them; the checks below are copied from that file.  Summary:
  data     Brouwer+2021 Fig. 8 colour bins (u-r < 2.5 late, >= 2.5 early), 15 g_bar bins each, the 30x30 covariance (bias-corrected); the Sersic
           bins as a reported replicate.
  lenses   lr_lenses.npz (181,477; Mgal = M*(1+f_cold), Brouwer's g_bar mass; typ 1 early / 0 late, rest-frame u-r > 2.0 -- a declared proxy).
  model    lens by lens: in g_bar bin k the pairs sit at R = sqrt(G M_gal / g), g inside the bin; within a bin weight 1/g, across lenses weight
           M_gal.  Delta Sigma of a spherical enclosed-mass profile, point baryons plus the dark mass, with the lane's own projector (C2).
           L: M_L(<r) = M_gal nu_mono(G M_gal / r^2 a0) to r_e = 0.40 r_ta (CFG7_common.r_ta_law at the lens redshift), frozen beyond.
           S: M_L + f_ex (1 - f_b) M_NFW(<r; M_coll) truncated at r_e, M_coll = CFG36 collapse(M_*, red for early / blue for late),
              f_ex = max(0, 1 - M_ph,edge / [(1 - f_b) M_coll]) (CFG35's conservation form, x_e = 0.40), M_* = 10^logM.
  K1       the 1-halo bins: lens-weighted median R of BOTH classes < 0.3 Mpc (fixed by the lens distribution, before any comparison).
  stat     D_obs = d_early - d_late on K1, C_D = C_ee + C_ll - C_el - C_le; D_L, D_S the model differences; one amplitude A (0 = law, 1 = rule),
           A_hat = D'C^-1(D_obs - D_L) / D'C^-1 D with D = D_S - D_L; sigma_A = stat (+) half the spread of A_hat under a colour-dependent
           +-0.1 dex M_* calibration of the early class.  chi2_L, chi2_S with |K1| dof.
PRE-DECLARED (from the frozen file)
  C1  CONTROL  the released profiles give the committed split chi2 = 119.9/15 (u-r) and 69.1/15 (Sersic), all 15 bins, to +-0.5.
  C2  CONTROL  the projector reproduces a point mass and an untruncated NFW (Wright & Brainerd) to 1e-3.
  C3  CONTROL  lr_lenses: 93,398 late and 88,079 early; median logM 10.328 / 10.744.
  C4  CONTROL  the law's Delta Sigma at fixed g_bar <= 1e-12 m/s^2 is mass-independent to 3% between M_gal = 1e10 and 1e11 (edge excluded).
  H1  the colour-blind law is rejected by the split in the 1-halo regime: A_hat / sigma_A > 3 on both footings (chi2_L p < 0.0027 reported).
  H2  [HEADLINE; MUTATE must fail] B's derived rule accounts for the split: |A_hat - 1| < 2 sigma_A on both footings and chi2_S p > 0.01.
  H3  (reported) the absolute early profile on K1 against S and L (C_ee), the late profile against L (C_ll).
  R1-R5 (reported) the Sersic replicate; the Sigma_crit^-2 weighting bracket (z_s = 0.75); the class-definition medians; the point-mass hot gas
      the early class would need for the law alone; all 15 bins including the 2-halo range (out of the isolation-reliable range).
MUTATE=1: the early and late data swapped (profiles and covariance blocks) -- H2 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG61_kids_colour_split.py   (MUTATE=1 for the control)
"""
import os, sys, io, math, json, contextlib
import numpy as np
from scipy.stats import chi2 as chi2d
from scipy.optimize import minimize_scalar
from scipy.special import erf
trapz = getattr(np, "trapezoid", None) or np.trapz

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG61_kids_colour_split", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: early and late data swapped -- H2 must FAIL ***")
FOOTS = ("canonical", "alt")
G_SI, MSUN, MPC = 6.67430e-11, 1.98892e30, C.MPC_M

# ------------------------------------------------------------------ CFG36's collapse masses and CFG35's edge phantom, read-only
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG36_colour_split_collapse.py")).read()
g36 = {"__file__": os.path.join(HERE, "CFG36_colour_split_collapse.py"), "__name__": "cfg36"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ================================================================================================ H1")], "CFG36", "exec"), g36)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
collapse, edge_phantom, FB, nfw_enclosed = g36["collapse"], g36["edge_phantom"], g36["FB"], g36["nfw_enclosed"]

# ------------------------------------------------------------------ data
B21 = os.path.join(C.REPO, "real_research", "data", "lensing_rar", "brouwer2021_rar")


def load_split(kind):
    d = [np.loadtxt(os.path.join(B21, f"Fig-8_RAR-KiDS-isolated_{kind}_{i}.txt")) for i in (1, 2)]
    g = d[0][:, 0]
    esd = [x[:, 1] / x[:, 4] for x in d]; err = [x[:, 3] / x[:, 4] for x in d]
    cv = np.loadtxt(os.path.join(B21, f"Fig-8_RAR-KiDS-isolated_{kind}s_covmatrix.txt"))
    C30 = (cv[:, 4] / cv[:, 6]).reshape(2, 2, 15, 15).transpose(0, 2, 1, 3).reshape(30, 30)
    return g, esd[0], esd[1], err[0], err[1], C30


def split_chi2(dl, de, C30, sel=slice(0, 15)):
    idx = np.arange(15)[sel]
    Cll, Cee = C30[:15, :15][np.ix_(idx, idx)], C30[15:, 15:][np.ix_(idx, idx)]
    Cel, Cle = C30[15:, :15][np.ix_(idx, idx)], C30[:15, 15:][np.ix_(idx, idx)]
    D = (de - dl)[idx]; CD = Cee + Cll - Cel - Cle
    return float(D @ np.linalg.solve(CD, D)), CD


R.banner("C1-C4  CONTROLS")
DATA = {k: load_split(k) for k in ("Colorbin", "Sersicbin")}
c1 = {k: split_chi2(v[1], v[2], v[5])[0] for k, v in DATA.items()}
errchk = max(float(np.max(np.abs(np.sqrt(np.diag(v[5])) / np.concatenate([v[3], v[4]]) - 1))) for v in DATA.values())
check("C1 CONTROL: the released profiles give the committed early-vs-late split (119.9/15 u-r, 69.1/15 Sersic) to +-0.5",
      f"u-r chi2 {c1['Colorbin']:.1f}, Sersic {c1['Sersicbin']:.1f}; sqrt(diag C) vs the error column: max rel. dev. {errchk:.1e}",
      abs(c1["Colorbin"] - 119.9) <= 0.5 and abs(c1["Sersicbin"] - 69.1) <= 0.5)
gdat, d_late, d_early, e_late, e_early, C30 = DATA["Colorbin"]
if MUTATE:
    d_late, d_early = d_early, d_late
    C30 = np.block([[C30[15:, 15:], C30[15:, :15]], [C30[:15, 15:], C30[:15, :15]]])
EDGES = np.logspace(np.log10(1e-15), np.log10(5e-12), 16)
midchk = float(np.max(np.abs(0.5 * (EDGES[1:] + EDGES[:-1]) / gdat - 1)))


# ------------------------------------------------------------------ projector
def project(r, Md, Rs):
    """Delta Sigma [Msun/Mpc^2] at projected radii Rs of a spherical dark-mass profile Md(<r) (r in Mpc, Md in Msun), by x = sqrt(r^2 - R^2)."""
    dMdr = np.gradient(Md, r)
    lr = np.log(r)
    out = np.empty(len(Rs))
    for i, Rp in enumerate(Rs):
        X = math.sqrt(max(r[-1] ** 2 - Rp ** 2, 0.0))
        x = np.concatenate([[0.0], np.geomspace(1e-5 * Rp, X, 1200)])
        rr = np.sqrt(x * x + Rp * Rp)
        dm = np.interp(np.log(rr), lr, dMdr, right=0.0)
        Sig = trapz(dm / rr ** 2, x) / (2 * math.pi)
        Mcyl = np.interp(math.log(Rp), lr, Md) + trapz(dm * (1 - x / rr) * (x / rr), x)
        out[i] = Mcyl / (math.pi * Rp * Rp) - Sig
    return out


def nfw_ds_wb(Rs, M200, c, r200):
    """Wright & Brainerd (2000) Delta Sigma of an untruncated NFW [Msun/Mpc^2]."""
    rs = r200 / c; dc = (200.0 / 3) * c ** 3 / (math.log(1 + c) - c / (1 + c))
    rho_c = M200 / (4 / 3 * math.pi * r200 ** 3 * 200.0)
    x = Rs / rs; out = np.empty_like(x)
    for i, xi in enumerate(x):
        if xi < 1:
            a = math.sqrt((1 - xi) / (1 + xi))
            g = 8 * math.atanh(a) / (xi * xi * math.sqrt(1 - xi * xi)) + 4 / xi ** 2 * math.log(xi / 2) - 2 / (xi * xi - 1) + \
                4 * math.atanh(a) / ((xi * xi - 1) * math.sqrt(1 - xi * xi))
        elif xi > 1:
            a = math.sqrt((xi - 1) / (1 + xi))
            g = 8 * math.atan(a) / (xi * xi * math.sqrt(xi * xi - 1)) + 4 / xi ** 2 * math.log(xi / 2) - 2 / (xi * xi - 1) + \
                4 * math.atan(a) / ((xi * xi - 1) ** 1.5)
        else:
            g = 10 / 3 + 4 * math.log(0.5)
        out[i] = rs * dc * rho_c * g
    return out


# C2: NFW (untruncated, extended far) and a point mass
r_t = np.geomspace(1e-6, 200.0, 6000)
M200, cc, r200 = 1e13, 6.0, 0.4
rs_ = r200 / cc; mfun = lambda y: np.log(1 + y) - y / (1 + y)
Mn = M200 * mfun(r_t / rs_) / mfun(cc)
Rt = np.geomspace(0.02, 2.0, 12)
dev_nfw = float(np.max(np.abs(project(r_t, Mn, Rt) / nfw_ds_wb(Rt, M200, cc, r200) - 1)))
dev_pm = 0.0     # point baryons enter analytically as M/(pi R^2): projector not involved (the dark profile of a point mass is zero)
check("C2 CONTROL: the projector reproduces an untruncated NFW (Wright & Brainerd) to 1e-3; the point mass is exact (M/pi R^2)",
      f"max rel. deviation (NFW, 0.02-2 Mpc) {dev_nfw:.1e}", dev_nfw < 1e-3)

# ------------------------------------------------------------------ lenses
LZ = np.load(os.path.join(C.REPO, "real_research", "data", "lensing_rar", "lr_lenses.npz"))
lM, Mg, typ, zl = LZ["logM"], LZ["Mgal"], LZ["typ"].astype(int), LZ["z"]
fcold = lambda lm: 10 ** (-0.69 * lm + 6.63)
mgchk = float(np.max(np.abs(Mg / (10 ** lM * (1 + fcold(lM))) - 1)))
n_l, n_e = int((typ == 0).sum()), int((typ == 1).sum())
med = (float(np.median(lM[typ == 0])), float(np.median(lM[typ == 1])))
check("C3 CONTROL: lr_lenses has 93,398 late and 88,079 early lenses, median logM 10.328 / 10.744 (and Mgal = M*(1+f_cold) exactly)",
      f"late {n_l}, early {n_e}; median logM {med[0]:.3f} / {med[1]:.3f}; Mgal identity max rel. dev. {mgchk:.1e}; bin midpoints vs file {midchk:.1e}",
      n_l == 93398 and n_e == 88079 and abs(med[0] - 10.328) < 5e-4 and abs(med[1] - 10.744) < 5e-4 and mgchk < 1e-9)

# ------------------------------------------------------------------ the model profiles on a (logM, z) grid
LMG = np.round(np.arange(8.00, 11.801, 0.05), 3)
ZG = np.array([0.05, 0.15, 0.25, 0.35, 0.45, 0.55])
RG = np.geomspace(1e-3, 12.0, 260)                    # projected radii for the Delta Sigma tables [Mpc]
rgrid = np.geomspace(1e-6, 60.0, 3000)                # 3D radii [Mpc]


def profiles(lm, z, foot, colour):
    Ms = 10 ** lm; Mb = Ms * (1 + fcold(lm)); a0 = C.A0[foot]
    rta = float(C.r_ta_law(Mb, a0, C.nu_mono, 1.0 / (1.0 + z)))
    re = 0.40 * rta
    rc = np.minimum(rgrid, re)
    ML = np.asarray(C.M_law(Mb, rc, a0, C.nu_mono), float)
    dsL = project(rgrid, ML - Mb, RG)
    Mh = float(collapse(Ms, colour))
    fx = max(0.0, 1.0 - edge_phantom(Mb, foot, 0.40) / ((1 - FB) * Mh))
    if fx > 0:
        Md = fx * (1 - FB) * np.asarray(nfw_enclosed(Mh, rc * 1e3), float)
        dsS = dsL + project(rgrid, Md, RG)
    else:
        dsS = dsL.copy()
    return dict(Mb=Mb, re=re, dsL=dsL, dsS=dsS, fex=fx, Mh=Mh)


PROF = {}
for foot in FOOTS:
    for colour in ("blue", "red"):
        for lm in LMG:
            for z in ZG:
                PROF[(foot, colour, lm, z)] = profiles(lm, z, foot, colour)

# C4: the law's Delta Sigma at fixed g_bar is mass-independent (untruncated law, deep regime)
def law_ds_untrunc(Mb, Rs, a0):
    ML = np.asarray(C.M_law(Mb, rgrid, a0, C.nu_mono), float)
    return project(rgrid, ML - Mb, Rs) + Mb / (math.pi * Rs ** 2)


c4 = []
for gg in (1e-13, 1e-12):
    ds = [law_ds_untrunc(Mb, np.array([math.sqrt(G_SI * Mb * MSUN / gg) / MPC]), C.A0["canonical"])[0] for Mb in (1e10, 1e11)]
    c4.append(abs(ds[1] / ds[0] - 1))
check("C4 CONTROL: the law's Delta Sigma at fixed g_bar (1e-13, 1e-12 m/s^2) is mass-independent to 3% between M_gal = 1e10 and 1e11 (untruncated)",
      f"relative differences {c4[0]:.1e}, {c4[1]:.1e}", max(c4) < 0.03)

# ------------------------------------------------------------------ stacking
iz = np.clip(np.round((zl - 0.05) / 0.10).astype(int), 0, len(ZG) - 1)
im = np.clip(np.round((lM - LMG[0]) / 0.05).astype(int), 0, len(LMG) - 1)


def dcomov(z, Om=0.3):
    zz = np.linspace(0, z, 400); return float(trapz(1 / np.sqrt(Om * (1 + zz) ** 3 + 1 - Om), zz))


def scrit_w(z, zs=0.75):
    if z >= zs: return 0.0
    dl, ds = dcomov(z), dcomov(zs)
    return ((dl / (1 + z)) * ((ds - dl) / (1 + zs)) / (ds / (1 + zs))) ** 2


SW = np.array([scrit_w(z) for z in ZG])


def weights(cls, scrit=False):
    w = np.zeros((len(LMG), len(ZG)))
    sel = typ == cls
    np.add.at(w, (im[sel], iz[sel]), Mg[sel])
    return w * (SW[None, :] if scrit else 1.0)


SUB = 8


def stack(cls, foot, model, colour, dshift=0, scrit=False, extra=1.0):
    """model stack in each of the 15 g_bar bins; dshift = grid-node shift of the TRUE mass (early-class calibration); extra = point-mass factor."""
    w = weights(cls, scrit)
    out = np.zeros(15)
    for k in range(15):
        lg = np.linspace(math.log(EDGES[k]), math.log(EDGES[k + 1]), SUB + 1)
        gs = np.exp(0.5 * (lg[1:] + lg[:-1]))
        num = den = 0.0
        for a in range(len(LMG)):
            for b in range(len(ZG)):
                if w[a, b] <= 0: continue
                Mtab = 10 ** LMG[a] * (1 + fcold(LMG[a]))
                aa = min(max(a + dshift, 0), len(LMG) - 1)
                pr = PROF[(foot, colour, LMG[aa], ZG[b])]
                Rj = np.sqrt(G_SI * Mtab * MSUN / gs) / MPC
                ds = np.interp(np.log(Rj), np.log(RG), pr["dsL" if model == "L" else "dsS"]) + extra * pr["Mb"] / (math.pi * Rj ** 2)
                wj = w[a, b] / gs
                num += float(np.sum(wj * ds)); den += float(np.sum(wj))
        out[k] = num / den / 1e12
    return out


# K1: lens-weighted median R (weights M_gal) at each bin's geometric centre, both classes < 0.3 Mpc
gc = np.sqrt(EDGES[1:] * EDGES[:-1])


def wmedian(x, w):
    o = np.argsort(x); cw = np.cumsum(w[o]); return float(x[o][np.searchsorted(cw, 0.5 * cw[-1])])


medR = {cls: [wmedian(np.sqrt(G_SI * Mg[typ == cls] * MSUN / g) / MPC, Mg[typ == cls]) for g in gc] for cls in (0, 1)}
K1 = [k for k in range(15) if medR[0][k] < 0.3 and medR[1][k] < 0.3]


def amp(dl, de, CC, ml, me, sl, se, sel):
    idx = np.array(sel)
    Cll, Cee = CC[:15, :15][np.ix_(idx, idx)], CC[15:, 15:][np.ix_(idx, idx)]
    Cel, Cle = CC[15:, :15][np.ix_(idx, idx)], CC[:15, 15:][np.ix_(idx, idx)]
    CD = Cee + Cll - Cel - Cle
    Dobs = (de - dl)[idx]; DL = (me - ml)[idx]; DS = (se - sl)[idx]; Dv = DS - DL
    Ci = np.linalg.inv(CD)
    F = float(Dv @ Ci @ Dv)
    Ahat = float(Dv @ Ci @ (Dobs - DL)) / F
    x2L = float((Dobs - DL) @ Ci @ (Dobs - DL)); x2S = float((Dobs - DS) @ Ci @ (Dobs - DS))
    return dict(A=Ahat, sA=1 / math.sqrt(F), chi2L=x2L, chi2S=x2S, n=len(idx), pL=float(chi2d.sf(x2L, len(idx))), pS=float(chi2d.sf(x2S, len(idx))),
                DL=DL.tolist(), DS=DS.tolist(), Dobs=Dobs.tolist())


RES = {}
for foot in FOOTS:
    ml, sl = stack(0, foot, "L", "blue"), stack(0, foot, "S", "blue")
    me, se = stack(1, foot, "L", "red"), stack(1, foot, "S", "red")
    base = amp(d_late, d_early, C30, ml, me, sl, se, K1)
    sh = [amp(d_late, d_early, C30, ml, stack(1, foot, "L", "red", dshift=s), sl, stack(1, foot, "S", "red", dshift=s), K1)["A"] for s in (+2, -2)]
    sys_ = 0.5 * abs(sh[0] - sh[1]); sA = math.sqrt(base["sA"] ** 2 + sys_ ** 2)
    RES[foot] = dict(base, sys=sys_, sAtot=sA, zlaw=base["A"] / sA, zrule=(base["A"] - 1) / sA, ml=ml, me=me, sl=sl, se=se)

R.banner("THE STACKS (canonical): per g_bar bin, lens-weighted median R, data and models [Msun/pc^2]")
c = RES["canonical"]
for k in range(15):
    tag = "K1" if k in K1 else "  "
    P(f"    {tag} g_bar {gdat[k]:.2e}: R_med late {medR[0][k]:.3f} early {medR[1][k]:.3f} Mpc | late {d_late[k]:7.2f} (L {c['ml'][k]:7.2f}, S {c['sl'][k]:7.2f}) "
      f"| early {d_early[k]:7.2f} (L {c['me'][k]:7.2f}, S {c['se'][k]:7.2f})")
fx_e = [PROF[("canonical", "red", lm, 0.25)]["fex"] for lm in LMG]
fx_l = [PROF[("canonical", "blue", lm, 0.25)]["fex"] for lm in LMG]
P(f"\n    K1 = {len(K1)} bins {K1}; f_ex (z = 0.25, canonical) red > 0 for log M* >= {min([lm for lm, f in zip(LMG, fx_e) if f > 0] or [np.nan])}, "
  f"blue > 0 for log M* >= {min([lm for lm, f in zip(LMG, fx_l) if f > 0] or [np.nan])}")
for foot in FOOTS:
    v = RES[foot]
    P(f"    {foot:9s}: A_hat {v['A']:+.3f} +- {v['sA']:.3f} (stat) +- {v['sys']:.3f} (early M* +-0.1 dex) = +- {v['sAtot']:.3f}; A/sigma {v['zlaw']:+.2f}, "
      f"(A-1)/sigma {v['zrule']:+.2f}; chi2_L {v['chi2L']:.1f}/{v['n']} (p {v['pL']:.1e}), chi2_S {v['chi2S']:.1f}/{v['n']} (p {v['pS']:.1e})")

R.banner("H1 / H2")
check("H1 THE COLOUR-BLIND LAW IS REJECTED BY THE SPLIT (1-halo bins): A_hat / sigma_A > 3 on both footings",
      "; ".join(f"{f}: A {RES[f]['A']:+.3f} +- {RES[f]['sAtot']:.3f} ({RES[f]['zlaw']:+.1f} sigma); chi2_L p {RES[f]['pL']:.1e}" for f in FOOTS),
      all(RES[f]["zlaw"] > 3 for f in FOOTS))
check("H2 [HEADLINE] B's DERIVED RULE ACCOUNTS FOR THE SPLIT: |A_hat - 1| < 2 sigma_A and chi2_S p > 0.01, both footings"
      + ("  [MUTATE: early/late swapped]" if MUTATE else ""),
      "; ".join(f"{f}: A {RES[f]['A']:+.3f} ((A-1)/sigma {RES[f]['zrule']:+.2f}); chi2_S {RES[f]['chi2S']:.1f}/{RES[f]['n']} p {RES[f]['pS']:.1e}" for f in FOOTS),
      all(abs(RES[f]["zrule"]) < 2 and RES[f]["pS"] > 0.01 for f in FOOTS))

R.banner("H3, R1-R5 (reported)")
idx = np.array(K1)
def absx2(d, m, blk):
    Cb = C30[blk, blk][np.ix_(idx, idx)]; r_ = (d - m)[idx]; return float(r_ @ np.linalg.solve(Cb, r_))
sE, sL_ = slice(15, 30), slice(0, 15)
check("H3 (reported, canonical) absolute profiles on K1: early vs S and vs L (C_ee); late vs L (C_ll)",
      f"early vs S chi2 {absx2(d_early, c['se'], sE):.1f}, vs L {absx2(d_early, c['me'], sE):.1f}; late vs L {absx2(d_late, c['ml'], sL_):.1f} (dof {len(K1)})",
      True, load_bearing=False)
gS, dlS, deS, _, _, CS = DATA["Sersicbin"]
rs_ = amp(dlS, deS, CS, c["ml"], c["me"], c["sl"], c["se"], K1)
check("R1 (reported, canonical) the Sersic replicate (n >= 2 early; the same colour-proxy lens masses)",
      f"A_hat {rs_['A']:+.3f} +- {rs_['sA']:.3f} (stat); chi2_L {rs_['chi2L']:.1f}, chi2_S {rs_['chi2S']:.1f} /{rs_['n']}", True, load_bearing=False)
r2 = amp(d_late, d_early, C30, stack(0, "canonical", "L", "blue", scrit=True), stack(1, "canonical", "L", "red", scrit=True),
         stack(0, "canonical", "S", "blue", scrit=True), stack(1, "canonical", "S", "red", scrit=True), K1)
check("R2 (reported, canonical) the Sigma_crit^-2 weighting bracket (source plane z_s = 0.75)",
      f"A_hat {r2['A']:+.3f} +- {r2['sA']:.3f} (stat); chi2_L {r2['chi2L']:.1f}, chi2_S {r2['chi2S']:.1f}", True, load_bearing=False)
mg_med = (float(np.median(np.log10(Mg[typ == 0]))), float(np.median(np.log10(Mg[typ == 1]))))
check("R3 (reported) the class-definition proxy: median log M_gal by lr typ (rest-frame u-r > 2.0; Brouwer's classes use GAaP u-r >= 2.5)",
      f"late {mg_med[0]:.3f}, early {mg_med[1]:.3f}", True, load_bearing=False)


def hot_chi2(f):
    # the true mass M_gal (1 + f_hot) at the tabulated R: the node is shifted by log10(1 + f_hot) (baryons and phantom; point-mass upper bound)
    sh = int(round(math.log10(1 + f) / 0.05))
    me_h = stack(1, "canonical", "L", "red", dshift=sh)
    return amp(d_late, d_early, C30, c["ml"], me_h, c["sl"], c["se"], K1)["chi2L"]


fgrid = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0]
hx = [hot_chi2(f) for f in fgrid]
fb_ = fgrid[int(np.argmin(hx))]
check("R4 (reported, canonical) the hot gas (a point mass, an upper bound on its effect) the early class would need for the law alone",
      "chi2_L of the difference vs f_hot (M_true = M_gal (1 + f_hot)): " + ", ".join(f"{f:g}: {x:.1f}" for f, x in zip(fgrid, hx)) + f"; best f_hot {fb_:g}",
      True, load_bearing=False)
all15 = amp(d_late, d_early, C30, c["ml"], c["me"], c["sl"], c["se"], list(range(15)))
check("R5 (reported, canonical) all 15 bins, including the 2-halo range (out of the isolation-reliable range; no 2-halo term modelled)",
      f"A_hat {all15['A']:+.3f} +- {all15['sA']:.3f}; chi2_L {all15['chi2L']:.1f}, chi2_S {all15['chi2S']:.1f} /15", True, load_bearing=False)

# ---- DISCLOSED DEPARTURE (added after the first run, kept as reported rows; the load-bearing verdicts above are unchanged) ----
# The frozen H1 was written as "A_hat / sigma_A > 3 ..., equivalently chi2_L p < 0.0027".  The two forms agree only when the rule predicts a
# split.  At KiDS lens masses (log M* <= 11.0, capped by the sample) f_ex = 0 for both colours with the measured collapse masses, so
# D_S - D_L ~ 0 and the amplitude statistic is degenerate (sigma_A enormous).  Both frozen forms are reported.
dnorm = {f: float(np.max(np.abs(np.array(RES[f]["DS"]) - np.array(RES[f]["DL"])) / np.sqrt(np.diag(split_chi2(d_late, d_early, C30, np.array(K1))[1]))))
         for f in FOOTS}
lm_all = lM[(typ == 1)]
fx_red = {lm: PROF[("canonical", "red", lm, 0.25)]["fex"] for lm in LMG}
bite = [lm for lm in LMG if lm >= 10.28 and fx_red[lm] > 0]
check("H1 chi2 form (reported; frozen as equivalent to H1): the early-minus-late difference rejects the law at p < 0.0027, both footings",
      "; ".join(f"{f}: chi2_L {RES[f]['chi2L']:.1f}/{RES[f]['n']}, p {RES[f]['pL']:.1e}" for f in FOOTS), True, load_bearing=False)
check("DEGENERACY (reported): the rule's predicted split relative to the data errors on K1, and where the rule bites",
      "max |D_S - D_L| / sigma_D: " + ", ".join(f"{f} {v:.1e}" for f, v in dnorm.items()) +
      f"; red f_ex > 0 inside Mandelbaum's measured range (log M* >= 10.28) from log M* {min(bite) if bite else 'none on the grid'}; "
      f"the lens sample's max log M* {lm_all.max():.3f}; below 10.28 f_ex > 0 only through the clamped collapse mass (the standing artefact)",
      True, load_bearing=False)
h1 = all(RES[f]["zlaw"] > 3 for f in FOOTS); h2 = all(abs(RES[f]["zrule"]) < 2 and RES[f]["pS"] > 0.01 for f in FOOTS)
if h1 and h2:
    reading = "the KiDS early/late split is the colour dependence B's derived rule imports from SDSS: B needs the rule; the law alone is rejected"
elif h1:
    reading = ("the law is rejected, and the rule's colour-dependent debris does not reproduce the split either (A_hat = "
               + ", ".join(f"{RES[f]['A']:+.2f}" for f in FOOTS) + ")")
else:
    reading = "in the 1-halo regime, with B's own lens-by-lens model, the split does not reject the colour-blind law"
P(f"\n    READING (declared, mechanical): {reading}")
P("    DISCLOSED (post hoc): the mechanical reading follows H1's amplitude form, which is degenerate here (the rule predicts no split at "
  "KiDS lens masses). H1's frozen chi2 form rejects the law -- and the rule, which equals it here -- at p = "
  + ", ".join(f"{RES[f]['pL']:.1e}" for f in FOOTS) + " (chi2_L = chi2_S). See the DEGENERACY row and the README.")
R.num("K1", K1); R.num("medR", {str(k): v for k, v in medR.items()})
R.num("RES", {f: {k: v for k, v in RES[f].items() if k not in ("ml", "me", "sl", "se")} | {k: RES[f][k].tolist() for k in ("ml", "me", "sl", "se")} for f in FOOTS})
R.num("C1", c1); R.num("R1", rs_); R.num("R2", r2); R.num("R4", dict(f=fgrid, chi2=hx)); R.num("R5", all15); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
