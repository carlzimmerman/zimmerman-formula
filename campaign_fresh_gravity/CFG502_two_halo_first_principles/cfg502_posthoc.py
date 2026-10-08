#!/usr/bin/env python3
"""CFG502 POST-HOC diagnostics (NOT in FROZEN_CRITERIA.md; written after the frozen gate failed; nothing here is a verdict).

Question: what is missing from the frozen environment term E, and how do the five models order if E's SHAPE is kept but pieces are freed?
  PH1 per-bin pulls of LCDM + E (stack P, ALL, f30).
  PH2 LCDM own halo mass shifted by -0.2 / +0.2 dex (CFG495's tables) + frozen E.
  PH3 one profiled amplitude s on the frozen E (shape fixed), every model, both footings; and s with the LCDM mass shift.
  PH4 satellite fraction x 0.5 / x 1.5 inside E (T2h and T_host kept).
  PH5 two profiled amplitudes: the central two-halo piece and the satellite piece of E separately (every model).
Run: nice -n 15 python3 cfg502_posthoc.py   -> cfg502_posthoc.out, cfg502_posthoc_results.json
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "4"
import math, json, time
import numpy as np
from scipy import stats
from scipy.interpolate import RegularGridInterpolator

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE); REPO = os.path.dirname(LANES)
sys.path.insert(0, os.path.join(LANES, "CFG487_settled_fraction_switch"))
sys.path.insert(0, os.path.join(LANES, "CFG100_kids_mass_rederivation"))
sys.path.insert(0, os.path.join(LANES, "CFG495_drawdown_shell"))
import cfg487_lib as LB                                                      # noqa: E402
import cfg100_lib as C                                                       # noqa: E402
import cfg495_lenslib as LL                                                  # noqa: E402

WORK = os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg502_work"))
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
FOOTS = ("canonical", "alt")
LOG = []
RES = {"lane": "CFG502", "script": "cfg502_posthoc", "status": "POST-HOC, not a verdict"}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


NPATCH = 50; KG = 1.98847e30 / (3.0857e16) ** 2


def esd_full_loo(WG, WW, patch, mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch[mask], weights=WG[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch[mask], weights=WW[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev


h15 = (NPATCH - 15 - 2) / (NPATCH - 1)
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
z = lens["z"].astype(float); Mgal = lens["Mgal"].astype(float); logMs = lens["logM"].astype(float)
patch = np.load(os.path.join(DATA, "lr_esd_jackknife.npz"))["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
f30 = np.load(os.path.join(DATA, "cfg96_isoflags.npz"))["f30"].astype(bool)
ALLM = np.ones(len(z), bool)
lmg = np.log10(Mgal)
key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(z / 0.03).astype(np.int64)
_, gi, cnt = np.unique(key, return_inverse=True, return_counts=True); gi = gi.ravel()
GM = 10 ** (np.bincount(gi, weights=lmg) / cnt); GZ = np.bincount(gi, weights=z) / cnt; GS = np.bincount(gi, weights=logMs) / cnt
NG = len(GM)
T495 = np.load(os.path.abspath(os.path.join(REPO, "..", "_external_data", "cfg495_work", "cfg495_pred_tables.npz")))
assert np.array_equal(T495["gi"], gi)


def pstack(tab, mask):
    out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG); out[k] = (w @ tab[:, k]) / w.sum()
    return out


ET = np.load(os.path.join(WORK, "cfg502_env_table.npz"))
LMS, ZG, RG = ET["LMS"], ET["ZG"], ET["RG"]; LRG = np.log(RG)


def env_vec(tab, mask):
    f = RegularGridInterpolator((LMS, ZG), tab, bounds_error=False, fill_value=None)
    Eg = f(np.c_[np.clip(GS, LMS[0], LMS[-1]), np.clip(GZ, ZG[0], ZG[-1])])
    out = np.array([LL.finish(lambda R, e=Eg[g]: np.interp(np.log(R), LRG, e), GM[g]) for g in range(NG)])
    return pstack(out, mask)


def pieces(W):
    f = ET[f"{W}_f"][..., None]; bc = ET[f"{W}_bc"][..., None]; bh = ET[f"{W}_bh"][..., None]
    cen = ET["HOLE"] + (1 - f) * bc * ET["S2H"]                        # hole + centrals' two-halo
    sat = f * (ET[f"{W}_Thost"] + bh * ET["S2H"])                      # leaked satellites
    return cen, sat, f, bc, bh


SC = LB.ShellClock(Om=C.OM); RHO_M0_MPC = C.OM * C.RHOC0


def kids_vec(Mg, zl, a0, rout, mfun=None):
    r = np.geomspace(1e-4, rout, 1500)
    Md = Mg * (C.nu_mono(C.G_MPC * Mg / r ** 2 / a0) - 1.0)
    if mfun is not None:
        mm = mfun(r); dM = np.diff(np.concatenate([[0.0], Md])); mmid = np.concatenate([[mm[0]], 0.5 * (mm[1:] + mm[:-1])])
        Md = np.cumsum(mmid * dM)
    return C._finish(lambda R: C.dsigma(R, r, Md) + Mg / (math.pi * R ** 2), Mg)


OWN = {}
for foot in FOOTS:
    a0 = C.A0[foot]; rows = {k: np.zeros((NG, 15)) for k in ("LAW_RTA", "EDGE", "V1")}
    for g in range(NG):
        Mg, zl = GM[g], GZ[g]; ao = 1 / (1 + zl); rta = C.r_ta_law(Mg, a0, zl); re1 = float(LB.r_edge(Mg, C.G_MPC, a0))
        rho1 = lambda r: Mg * C.nu_mono(C.G_MPC * Mg / r ** 2 / a0) / (4 * math.pi / 3 * r ** 3) / RHO_M0_MPC
        rows["LAW_RTA"][g] = kids_vec(Mg, zl, a0, rta); rows["EDGE"][g] = kids_vec(Mg, zl, a0, re1)
        rows["V1"][g] = kids_vec(Mg, zl, a0, rta, lambda r: SC.m_of_rho(rho1(r), ao, conservative=False)[0])
    rows["LCDM"] = T495[f"{foot}_lcdm"]; rows["F_DD"] = T495[f"{foot}_nodd"] + T495[f"{foot}_prop"]
    for dl in ("-0.2", "+0.2"):
        rows[f"LCDM_dlogM{dl}"] = T495[f"{foot}_lcdm_dlogM{dl}"]
    OWN[foot] = rows
MODELS = ("LCDM", "LAW_RTA", "EDGE", "V1", "F_DD")


def chi2(d, C_, m, h=h15):
    r = d - m; return float(h * r @ np.linalg.inv(C_) @ r)


def prof(d, C_, base, temps, h=h15):
    """profile linear amplitudes of the template list on top of base; returns chi2, amplitudes."""
    Ci = np.linalg.inv(C_); Tm = np.array(temps); r = d - base
    F = Tm @ Ci @ Tm.T; A = np.linalg.solve(F, Tm @ Ci @ r); rr = r - A @ Tm
    return float(h * rr @ Ci @ rr), A.tolist()


d, Cv = esd_full_loo(WG, WW, patch, ALLM)
sig = np.sqrt(np.diag(Cv))
cen10, sat10, *_ = pieces("W10")
Ecen = env_vec(cen10, ALLM); Esat = env_vec(sat10, ALLM); E10 = Ecen + Esat
Rm = np.array(json.load(open(os.path.join(LANES, "CFG377_kids_reservoir_dip", "cfg377_results.json")))["primary"]["meanR"])
lc = pstack(OWN["canonical"]["LCDM"], ALLM)
P("POST-HOC diagnostics (not frozen; no verdict)")
P("PH1 pulls (data - LCDM - E) / sigma, stack P:")
P("  R [Mpc] : " + " ".join(f"{x:6.3f}" for x in Rm))
P("  pull    : " + " ".join(f"{x:+6.2f}" for x in (d - lc - E10) / sig))
P("  E_cen   : " + " ".join(f"{x:6.3f}" for x in Ecen))
P("  E_sat   : " + " ".join(f"{x:6.3f}" for x in Esat))
RES["PH1"] = dict(R=Rm.tolist(), pull=((d - lc - E10) / sig).tolist(), E_cen=Ecen.tolist(), E_sat=Esat.tolist())
S_ = json.load(open(os.path.join(HERE, "cfg502_score_results.json")))["MAIN"]
for nm, blk in (("ALL", S_["N2_ALL"]), ):
    pu = (np.array(blk["data"]) - np.array(blk["LCDM_model"])) / np.array(blk["sigma"])
    P(f"  {nm} pulls : " + " ".join(f"{x:+6.2f}" for x in pu))
    RES["PH1"][f"pull_{nm}"] = pu.tolist()

P("\nPH2 LCDM halo-mass shift (CFG495 tables) + frozen E: chi2 / 15")
RES["PH2"] = {}
for dl in ("-0.2", "+0.2"):
    m = pstack(OWN["canonical"][f"LCDM_dlogM{dl}"], ALLM) + E10
    c_ = chi2(d, Cv, m); RES["PH2"][dl] = dict(chi2=c_, p=float(stats.chi2.sf(c_, 15)))
    P(f"  dlogM {dl}: chi2 {c_:.2f} (p {stats.chi2.sf(c_, 15):.2e})")

P("\nPH3 one profiled amplitude s on the frozen E (shape fixed); 14 dof")
P("  model    | canonical chi2  s     | alt chi2  s")
RES["PH3"] = {}
for k in MODELS + ("LCDM_dlogM-0.2", "LCDM_dlogM+0.2"):
    row = {}
    for foot in FOOTS:
        c_, A = prof(d, Cv, pstack(OWN[foot][k], ALLM), [E10]); row[foot] = dict(chi2=c_, s=A[0], p=float(stats.chi2.sf(c_, 14)))
    RES["PH3"][k] = row
    P(f"  {k:15s}| {row['canonical']['chi2']:8.2f} {row['canonical']['s']:6.3f} | {row['alt']['chi2']:8.2f} {row['alt']['s']:6.3f}")
for foot in FOOTS:
    b = min(MODELS, key=lambda k: RES["PH3"][k][foot]["chi2"])
    P(f"  [{foot}] best of (i)-(v) with s profiled: {b} {RES['PH3'][b][foot]['chi2']:.2f}; EDGE - best = "
      f"{RES['PH3']['EDGE'][foot]['chi2'] - RES['PH3'][b][foot]['chi2']:+.2f}")
    RES["PH3"][f"edge_minus_best_{foot}"] = RES["PH3"]["EDGE"][foot]["chi2"] - RES["PH3"][b][foot]["chi2"]

P("\nPH4 satellite fraction inside E scaled (frozen otherwise): LCDM chi2")
RES["PH4"] = {}
f = ET["W10_f"][..., None]; bc = ET["W10_bc"][..., None]; bh = ET["W10_bh"][..., None]
for fs in (0.5, 1.5, 2.0):
    ff = np.clip(f * fs, 0, 1)
    tab = ET["HOLE"] + (1 - ff) * bc * ET["S2H"] + ff * (ET["W10_Thost"] + bh * ET["S2H"])
    m = lc + env_vec(tab, ALLM); c_ = chi2(d, Cv, m)
    RES["PH4"][str(fs)] = c_
    P(f"  f_W x {fs}: chi2 {c_:.2f}")

P("\nPH5 two profiled amplitudes (centrals' two-halo piece a_c, satellite piece a_s); 13 dof")
P("  model    | canonical chi2  a_c   a_s   | alt chi2  a_c   a_s")
RES["PH5"] = {}
for k in MODELS:
    row = {}
    for foot in FOOTS:
        c_, A = prof(d, Cv, pstack(OWN[foot][k], ALLM), [Ecen, Esat]); row[foot] = dict(chi2=c_, a_c=A[0], a_s=A[1])
    RES["PH5"][k] = row
    P(f"  {k:8s} | {row['canonical']['chi2']:8.2f} {row['canonical']['a_c']:6.2f} {row['canonical']['a_s']:6.2f} | "
      f"{row['alt']['chi2']:8.2f} {row['alt']['a_c']:6.2f} {row['alt']['a_s']:6.2f}")
for foot in FOOTS:
    b = min(MODELS, key=lambda k: RES["PH5"][k][foot]["chi2"])
    P(f"  [{foot}] best: {b} {RES['PH5'][b][foot]['chi2']:.2f}; EDGE - best = {RES['PH5']['EDGE'][foot]['chi2'] - RES['PH5'][b][foot]['chi2']:+.2f}")
    RES["PH5"][f"edge_minus_best_{foot}"] = RES["PH5"]["EDGE"][foot]["chi2"] - RES["PH5"][b][foot]["chi2"]
RES["elapsed_s"] = round(time.time() - T0, 1)
json.dump(RES, open(os.path.join(HERE, "cfg502_posthoc_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg502_posthoc.out"), "w").write("\n".join(LOG) + "\n")
