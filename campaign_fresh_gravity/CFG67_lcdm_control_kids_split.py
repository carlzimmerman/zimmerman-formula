#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG67 -- THE LCDM CONTROL FOR CFG61: do standard halos, run through CFG61's exact machinery, reproduce the KiDS-1000 early/late lensing split?

Criteria frozen and committed before this script: campaign_fresh_gravity/CFG67_FROZEN_CRITERIA.md (commit 5f9c56bc8).  CFG61's data, lenses, forward
model, projector, K1 bins and floor are exec'd read-only from CFG61_kids_colour_split.py (up to its model-profile section; its MUTATE forced off).
Comparator: Delta Sigma = point mass M_gal + NFW(M_200c), M_200c = CFG36 collapse(M_*, red for early / blue for late) (Mandelbaum+2016; HEADLINE),
Dutton-Maccio concentration and the enclosed mass as implemented in CFG36's nfw_enclosed (saturating at 5 R_200c); the colour-blind Moster+13
halo_mass as a reported variant.
PRE-DECLARED (from the frozen file)
  C1  CONTROL  CFG61's committed law chi2_L = 28.1/7 (canonical) reproduced by the exec'd machinery (its committed law stacks) to +-0.1.
  C2  CONTROL  CFG36's NFW gives M(<R_200c) = M_200c to 1e-6, and the projector reproduces Wright & Brainerd's untruncated NFW to 1e-3.
  H1  [HEADLINE; MUTATE must fail] LCDM with the colour-split relation reproduces the difference: chi2_Lambda p > 0.01 and |A_hat - 1| < 2 sigma_A.
  H2  the data prefer LCDM's split over a colour-blind prediction: A_hat / sigma_A > 3.
  H3  (reported) the absolute profiles on K1 against LCDM (early with C_ee, late with C_ll).
  R1-R4 (reported) the colour-blind Moster variant; the Sersic replicate; all 15 bins; the clamped weight fraction.
MUTATE=1: early and late data swapped -- H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG67_lcdm_control_kids_split.py   (MUTATE=1 for the control)
"""
import os, sys, io, math, json, contextlib
import numpy as np
from scipy.stats import chi2 as chi2d

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG67_lcdm_control_kids_split", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: early and late data swapped -- H1 must FAIL ***")

# ------------------------------------------------------------------ CFG61's machinery, read-only
_e = os.environ.get("MUTATE"); os.environ["MUTATE"] = "0"
src = open(os.path.join(HERE, "CFG61_kids_colour_split.py")).read()
g = {"__file__": os.path.join(HERE, "CFG61_kids_colour_split.py"), "__name__": "cfg61"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index("# ------------------------------------------------------------------ the model profiles on a (logM, z) grid")], "CFG61", "exec"), g)
os.environ.pop("MUTATE") if _e is None else os.environ.__setitem__("MUTATE", _e)
DATA, project, nfw_ds_wb, collapse, nfw_enclosed = g["DATA"], g["project"], g["nfw_ds_wb"], g["collapse"], g["nfw_enclosed"]
lM, Mg, typ, EDGES, fcold = g["lM"], g["Mg"], g["typ"], g["EDGES"], g["fcold"]
G_SI, MSUN, MPC = g["G_SI"], g["MSUN"], g["MPC"]
halo_mass = g["g36"].get("halo_mass") or nfw_enclosed.__globals__.get("halo_mass")
gdat, d_late, d_early, e_late, e_early, C30 = DATA["Colorbin"]
if MUTATE:
    d_late, d_early = d_early, d_late
    C30 = np.block([[C30[15:, 15:], C30[15:, :15]], [C30[:15, 15:], C30[:15, :15]]])
c61 = json.load(open(os.path.join(HERE, "CFG61_kids_colour_split_results.json")))["numbers"]
K1 = c61["K1"]


def diffstats(dl, de, CC, D_model, sel):
    idx = np.array(sel)
    Cll, Cee = CC[:15, :15][np.ix_(idx, idx)], CC[15:, 15:][np.ix_(idx, idx)]
    Cel, Cle = CC[15:, :15][np.ix_(idx, idx)], CC[:15, 15:][np.ix_(idx, idx)]
    Ci = np.linalg.inv(Cee + Cll - Cel - Cle)
    Dobs = (de - dl)[idx]; Dm = np.asarray(D_model)[idx]
    F = float(Dm @ Ci @ Dm)
    x2 = float((Dobs - Dm) @ Ci @ (Dobs - Dm))
    return dict(A=float(Dm @ Ci @ Dobs) / F, sA=1 / math.sqrt(F), chi2=x2, n=len(idx), p=float(chi2d.sf(x2, len(idx))))


R.banner("C1 / C2  CONTROLS")
rc = c61["RES"]["canonical"]
c1 = diffstats(d_late if not MUTATE else d_early, d_early if not MUTATE else d_late, DATA["Colorbin"][5],
               np.array(rc["me"]) - np.array(rc["ml"]), K1)["chi2"]
check("C1 CONTROL: CFG61's committed law chi2_L = 28.1/7 (canonical) reproduced by the exec'd machinery (its committed law stacks)",
      f"chi2_L {c1:.2f} (CFG61 committed {rc['chi2L']:.2f}); K1 = {K1}", abs(c1 - 28.1) <= 0.1 and abs(c1 - rc["chi2L"]) < 1e-6)
Mh0 = 1e12
R200 = float((3 * Mh0 / (4 * math.pi * 200 * nfw_enclosed.__globals__["_RHO_C"])) ** (1 / 3) * 1000.0)
m200 = float(nfw_enclosed(Mh0, R200)) / Mh0 - 1
r_t = np.geomspace(1e-6, 200.0, 6000); cc_, r200_ = 6.0, 0.4
mfun = lambda y: np.log(1 + y) - y / (1 + y)
Rt = np.geomspace(0.02, 2.0, 12)
dwb = float(np.max(np.abs(project(r_t, 1e13 * mfun(r_t / (r200_ / cc_)) / mfun(cc_), Rt) / nfw_ds_wb(Rt, 1e13, cc_, r200_) - 1)))
check("C2 CONTROL: CFG36's NFW gives M(<R_200c) = M_200c (1e-6); the projector reproduces Wright & Brainerd (1e-3)",
      f"M(<R200)/M200 - 1 = {m200:.1e}; projector vs WB max rel. dev. {dwb:.1e}", abs(m200) < 1e-6 and dwb < 1e-3)

# ------------------------------------------------------------------ LCDM profiles on the CFG61 mass grid (z-independent)
LMG = np.round(np.arange(8.00, 11.801, 0.05), 3)
RG = np.geomspace(1e-3, 12.0, 260)
rgrid = np.geomspace(1e-6, 60.0, 3000)


def lcdm_table(kind):
    tab = {}
    for lm in LMG:
        Ms = 10 ** lm
        Mh = float(collapse(Ms, kind)) if kind in ("red", "blue") else float(halo_mass(Ms))
        Mn = np.asarray(nfw_enclosed(Mh, rgrid * 1e3), float)
        tab[lm] = dict(Mb=Ms * (1 + fcold(lm)), ds=project(rgrid, Mn, RG), Mh=Mh)
    return tab


TAB = {k: lcdm_table(k) for k in ("red", "blue")}
if halo_mass is not None:
    TAB["moster"] = lcdm_table("moster")
im = np.clip(np.round((lM - LMG[0]) / 0.05).astype(int), 0, len(LMG) - 1)


def stack(cls, kind, dshift=0):
    w = np.zeros(len(LMG)); sel = typ == cls
    np.add.at(w, im[sel], Mg[sel])
    out = np.zeros(15)
    for k in range(15):
        lg = np.linspace(math.log(EDGES[k]), math.log(EDGES[k + 1]), 9)
        gs = np.exp(0.5 * (lg[1:] + lg[:-1]))
        num = den = 0.0
        for a in range(len(LMG)):
            if w[a] <= 0: continue
            Mtab = 10 ** LMG[a] * (1 + fcold(LMG[a]))
            pr = TAB[kind][LMG[min(max(a + dshift, 0), len(LMG) - 1)]]
            Rj = np.sqrt(G_SI * Mtab * MSUN / gs) / MPC
            ds = np.interp(np.log(Rj), np.log(RG), pr["ds"]) + pr["Mb"] / (math.pi * Rj ** 2)
            num += float(np.sum(w[a] / gs * ds)); den += float(np.sum(w[a] / gs))
        out[k] = num / den / 1e12
    return out


ml, me = stack(0, "blue"), stack(1, "red")
D = me - ml
base = diffstats(d_late, d_early, C30, D, K1)
shA = [diffstats(d_late, d_early, C30, stack(1, "red", dshift=s) - ml, K1)["A"] for s in (+2, -2)]
sysA = 0.5 * abs(shA[0] - shA[1]); sA = math.sqrt(base["sA"] ** 2 + sysA ** 2)

R.banner("THE STACKS: LCDM (colour-split SHMR) against the data [Msun/pc^2], and CFG61's law")
for k in range(15):
    tag = "K1" if k in K1 else "  "
    P(f"    {tag} g_bar {gdat[k]:.2e}: late {d_late[k]:7.2f} (LCDM {ml[k]:7.2f}, law {rc['ml'][k]:7.2f}) | early {d_early[k]:7.2f} "
      f"(LCDM {me[k]:7.2f}, law {rc['me'][k]:7.2f})")
P(f"\n    LCDM (colour-split): A_hat {base['A']:+.3f} +- {base['sA']:.3f} (stat) +- {sysA:.3f} (early M* +-0.1 dex) = +- {sA:.3f}; "
  f"chi2_Lambda {base['chi2']:.1f}/{base['n']} (p {base['p']:.2e})")

R.banner("H1 / H2")
h1 = base["p"] > 0.01 and abs(base["A"] - 1) < 2 * sA
check("H1 [HEADLINE] LCDM with the colour-split SHMR reproduces the early-minus-late difference: chi2 p > 0.01 and |A_hat - 1| < 2 sigma_A"
      + ("  [MUTATE: early/late swapped]" if MUTATE else ""),
      f"chi2_Lambda {base['chi2']:.1f}/{base['n']} p {base['p']:.2e}; A_hat {base['A']:+.3f} +- {sA:.3f} ((A-1)/sigma {(base['A'] - 1) / sA:+.2f})", h1)
check("H2 the data prefer LCDM's split over a colour-blind prediction: A_hat / sigma_A > 3",
      f"A_hat / sigma_A = {base['A'] / sA:+.2f}", base["A"] / sA > 3)

R.banner("H3, R1-R4 (reported)")
idx = np.array(K1)
def absx2(d, m, blk):
    Cb = C30[blk, blk][np.ix_(idx, idx)]; r_ = (d - m)[idx]; return float(r_ @ np.linalg.solve(Cb, r_))
check("H3 (reported) absolute profiles on K1 against LCDM (colour-split): early (C_ee), late (C_ll)",
      f"early chi2 {absx2(d_early, me, slice(15, 30)):.1f}, late {absx2(d_late, ml, slice(0, 15)):.1f} (dof {len(K1)}); "
      f"CFG61's law: early 51.9, late 12.6", True, load_bearing=False)
if "moster" in TAB:
    mo = diffstats(d_late, d_early, C30, stack(1, "moster") - stack(0, "moster"), K1)
    r1 = f"A_hat {mo['A']:+.2f} +- {mo['sA']:.2f} (stat); chi2 {mo['chi2']:.1f}/{mo['n']} (p {mo['p']:.1e})"
else:
    mo = None; r1 = "halo_mass not available in the exec'd namespace"
check("R1 (reported) the colour-blind Moster+13 variant (the a-priori LCDM: halo mass depends on M_* only)", r1, True, load_bearing=False)
gS, dlS, deS, _, _, CS = DATA["Sersicbin"]
if MUTATE:
    dlS, deS = deS, dlS
    CS = np.block([[CS[15:, 15:], CS[15:, :15]], [CS[:15, 15:], CS[:15, :15]]])
rs_ = diffstats(dlS, deS, CS, D, K1)
check("R2 (reported) the Sersic replicate (same colour-proxy LCDM stacks)",
      f"A_hat {rs_['A']:+.3f} +- {rs_['sA']:.3f} (stat); chi2 {rs_['chi2']:.1f}/{rs_['n']} (p {rs_['p']:.1e})", True, load_bearing=False)
a15 = diffstats(d_late, d_early, C30, D, list(range(15)))
check("R3 (reported) all 15 bins (out of the isolation-reliable range; no 2-halo term)",
      f"A_hat {a15['A']:+.3f} +- {a15['sA']:.3f}; chi2 {a15['chi2']:.1f}/15 (p {a15['p']:.1e})", True, load_bearing=False)
fcl = {c: float(Mg[(typ == c) & (lM < lim)].sum() / Mg[typ == c].sum()) for c, lim in ((1, 10.28), (0, 10.24))}
check("R4 (reported) the M_gal-weighted fraction of lenses below Mandelbaum's measured range (clamped collapse mass)",
      f"early (red, < 10.28): {fcl[1]:.3f}; late (blue, < 10.24): {fcl[0]:.3f}", True, load_bearing=False)

if h1:
    reading = ("standard halos with the measured colour-split halo masses reproduce the KiDS split through the same machinery: CFG61's failure is "
               "specific to a colour-blind dark mass, not an artefact of the machinery")
else:
    reading = "LCDM with measured halos also misses: CFG61's failure is not (only) framework-specific; H2 and R1 say how"
P(f"\n    READING (declared): {reading}")
R.num("lcdm", dict(ml=ml.tolist(), me=me.tolist(), base=base, sysA=sysA, sA=sA))
R.num("R1_moster", mo); R.num("R2_sersic", rs_); R.num("R3_all15", a15); R.num("R4_clamped", fcl); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
