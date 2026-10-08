#!/usr/bin/env python3
"""CFG486: CFG352's caustic edge (0.232 r_ta) re-scored on CFG413's FREE-two-halo floor.
Criteria: FROZEN_CRITERIA.md (committed alone first, 02ef5356e).

Stack P (VERDICT): CFG377's primary KiDS-1000 isolated-lens stack (15 g_bar bins, 50-patch jackknife, Hartlap), with
  CFG413's model and chi^2 code (copied from cfg413_kids.py): BARE law (cfg100 nu_mono phantom, shell projector), phantom
  frozen beyond r_on = x r_ta (cfg100 r_ta_law per lens group), plus a free R^-0.8 two-halo amplitude, profiled.
Stack F (CONTROL + reported): CFG352's own scorer (FP1/L355 KiDS machinery, Brouwer+21 Fig-3, 4 mass bins), code path
  copied from cfg352_caustic_edge.py; Amax = 0 reproduces CFG352; Amax = 2 and inf are reported.
Usage: nice -n 15 python3 cfg486_rescore.py ;  CFG486_MUTATE=1 nice -n 15 python3 cfg486_rescore.py  (adds x = 0.05)
"""
import os, sys
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, math, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(LANES, ".."))
sys.path.insert(0, LANES)
sys.path.insert(0, os.path.join(LANES, "CFG100_kids_mass_rederivation"))
import cfg100_lib as C                                                       # read-only import (CFG413's)
import CFG4_common as C4                                                     # read-only import (CFG352's)
DATA = os.path.join(REPO, "real_research", "data", "lensing_rar")
MUTATE = os.environ.get("CFG486_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
try:
    os.nice(15)
except OSError:
    pass
FOOTS = ("canonical", "alt")
EDGE, FIRST, REF, CTRL = 0.232, 0.359, 1.0, 0.23
XS = [CTRL, EDGE, FIRST, REF] + ([0.05] if MUTATE else [])
LOG, CHK = [], {}


def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); LOG.append(s)


def check(name, ok, msg):
    CHK[name] = bool(ok); P("  [%s] %s: %s" % ("PASS" if ok else "FAIL", name, msg))


np.set_printoptions(linewidth=200, precision=4)
T0 = time.time()
J352 = json.load(open(os.path.join(LANES, "CFG352_caustic_edge_vs_data", "cfg352_caustic_edge_results.json")))
J352M = json.load(open(os.path.join(LANES, "CFG352_caustic_edge_vs_data", "cfg352_caustic_edge_MUTATE_results.json")))
J413 = json.load(open(os.path.join(LANES, "CFG413_on_radius_kids_vs_growth", "cfg413_kids_results.json")))
LAW352 = {"canonical": 162.6053, "alt": 154.7582}                             # cfg352_caustic_edge.out line 2 (4 d.p. as printed)
P(f"CFG486  MUTATE={MUTATE}  rows x = {XS}")

# ================================================================================================ A range from CFG413 (frozen rule)
ARANGE = {}
for f in FOOTS:
    As = [J413["primary"][f][k]["free"]["A"] for k in J413["primary"][f]]
    ARANGE[f] = (min(As) / 1.5, 1.5 * max(As), min(As), max(As))
P("A plausibility range from CFG413's committed free-A grid ([min/1.5, 1.5 max]): "
  + ", ".join(f"{f} CFG413 {ARANGE[f][2]:.3f}-{ARANGE[f][3]:.3f} -> [{ARANGE[f][0]:.3f}, {ARANGE[f][1]:.3f}]" for f in FOOTS))

# ================================================================================================ STACK F: CFG352's own scorer (copied code path)
t = time.time()
GK = {"np": np, "math": math, "os": os, "REPO": C4.REPO, "G_SI": 6.67430e-11, "_trap": C4._trap}
GK = C4.exec_slices(os.path.join(C4.CHAIN, "FP1_static_sector.py"),
                    [("# ---- KiDS: L355's machinery", "w0 = np.zeros(len(ES)); w0[0] = 1.0")], ns=GK, name="fp1_kids")[0]
FIX = C4.ESDFix(GK["rrK"], GK["Rp"], GK["PCm2"], GK["MS"])
RRK, RPK, MPCK, MSK = GK["rrK"], GK["Rp"], GK["MPCm"], GK["MS"]
LM, NPB = GK["LM"], GK["npb"]
W0 = np.zeros(len(GK["ES"])); W0[0] = 1.0
GN = 6.67430e-11
A0K = C4.A0
RHOM_ZL = GK["rho_m_z"] * MSK / C4.MPC ** 3
DTA_025 = json.load(open(os.path.join(LANES, "CFG4_switch_results.json")))["numbers"]["D1"]["0.25"]["one_plus_delta_ta"]


def M_law(Mb, a0):
    return Mb * C4.nu_mono(GN * Mb / RRK ** 2 / a0)


def r_bound(M, Delta, ef):
    """CFG352's r_bound (copied; EDGE_FRAC passed as ef): first radius where the enclosed mean density falls to Delta rho_m(z_l)."""
    D = M / (4.0 / 3.0 * math.pi * RRK ** 3 * RHOM_ZL)
    k = np.where(D < Delta)[0]
    if not len(k) or k[0] == 0:
        return RRK[-1] if not len(k) else RRK[0]
    i = k[0]
    return ef * float(math.exp(np.interp(math.log(Delta), [math.log(D[i]), math.log(D[i - 1])], [math.log(RRK[i]), math.log(RRK[i - 1])])))


def kids_chi2(Mfun, foot, Amax):
    T = np.zeros((len(GK["ES"]), len(LM), 4, NPB))
    for im, lm in enumerate(LM):
        Mb = 10 ** lm * MSK
        dS = FIX(Mfun(Mb, A0K[foot]), Mb)
        T[0, im] = [np.interp(GK["Rd"][b], RPK / MPCK, dS) for b in range(4)]
    return GK["kfit"]({foot: T}, foot, W0, Amax)


def M_edge(ef):
    def f_(Mb, a0):                                                          # CFG352 smear_mass sharp path, fin = 1
        Ml = M_law(Mb, a0)
        a = r_bound(Ml, DTA_025, ef)
        Mt = np.interp(a, RRK, Ml)
        return Mb + (np.where(RRK <= a, Ml, Mt) - Mb)
    return f_


EFS = [REF, FIRST, EDGE] + ([0.05] if MUTATE else [])
AMAXES = (("A0", 0.0), ("Amax2", 2.0), ("Afree", np.inf))
SF = {}
for tag, am in AMAXES:
    SF[tag] = {}
    for f in FOOTS:
        law = kids_chi2(M_law, f, am)
        rows = {str(ef): kids_chi2(M_edge(ef), f, am) for ef in EFS}
        SF[tag][f] = dict(law=dict(chi2=law[0], A=law[1]),
                          rows={k: dict(chi2=v[0], A=v[1], dchi2_vs_law=v[0] - law[0], dchi2_vs_ref=v[0] - rows[str(REF)][0])
                                for k, v in rows.items()})
P(f"\n=== STACK F: CFG352's own scorer (FP1/L355, Brouwer+21 Fig-3, 4 mass bins; {time.time() - t:.0f} s)")
P("  Amax   foot      | law chi2 | x=1.0 chi2 (dlaw) | x=0.359 chi2 (dlaw) | x=0.232 chi2 (dlaw) | dchi2_edge (0.232 vs 1.0) | A per mass bin at 0.232 / 1.0")
for tag, am in AMAXES:
    for f in FOOTS:
        s = SF[tag][f]; r = s["rows"]
        P(f"  {tag:6s} {f:9s} | {s['law']['chi2']:8.3f} | {r['1.0']['chi2']:8.3f} ({r['1.0']['dchi2_vs_law']:+7.2f}) | "
          f"{r['0.359']['chi2']:8.3f} ({r['0.359']['dchi2_vs_law']:+7.2f}) | {r['0.232']['chi2']:8.3f} ({r['0.232']['dchi2_vs_law']:+7.2f}) | "
          f"{r['0.232']['dchi2_vs_ref']:+8.2f} | {r['0.232']['A']} / {r['1.0']['A']}")
        if MUTATE:
            P(f"           MUTATE x=0.05: chi2 {r['0.05']['chi2']:.3f} (dlaw {r['0.05']['dchi2_vs_law']:+.2f}, vs 1.0 {r['0.05']['dchi2_vs_ref']:+.2f}), A {r['0.05']['A']}")

# C1: Amax = 0 reproduces CFG352
diffs = []
for f in FOOTS:
    diffs.append(abs(SF["A0"][f]["law"]["chi2"] - LAW352[f]))
    for ef in ("1.0", "0.359", "0.232"):
        diffs.append(abs(SF["A0"][f]["rows"][ef]["dchi2_vs_law"] - J352["rows"][ef]["kids"][f]))
    if MUTATE:
        diffs.append(abs(SF["A0"][f]["rows"]["0.05"]["dchi2_vs_law"] - J352M["rows"]["0.05"]["kids"][f]))
check("C1 stack F, Amax = 0 reproduces CFG352 (law chi2 + row dchi2) to 0.01", max(diffs) <= 0.01, f"max |diff| {max(diffs):.5f} over {len(diffs)} numbers")

# ================================================================================================ STACK P: CFG413's floor (CFG377 primary stack; code copied from cfg413_kids.py)
t = time.time()
NPATCH = 50
KG = 1.98847e30 / (3.0857e16) ** 2
lens = np.load(os.path.join(DATA, "lr_lenses.npz"))
z = lens["z"].astype(float); Mgal = lens["Mgal"].astype(float)
jk = np.load(os.path.join(DATA, "lr_esd_jackknife.npz")); patch = jk["patch"]
pl = np.load(os.path.join(DATA, "cfg110_perlens.npz")); WG, WW = pl["WG"], pl["WW"]
assert np.allclose(pl["gbar_edges"], C.GEDGE)
nL = len(z)
check("C3 stack P has 181,477 lenses and 15 bins", nL == 181477 and WG.shape[1] == 15, f"lenses {nL}, bins {WG.shape[1]}")


def esd_full_loo(mask):
    wg = np.zeros((NPATCH, 15)); w = np.zeros((NPATCH, 15))
    for k in range(15):
        wg[:, k] = np.bincount(patch[mask], weights=WG[mask, k], minlength=NPATCH)
        w[:, k] = np.bincount(patch[mask], weights=WW[mask, k], minlength=NPATCH)
    tg, tw = wg.sum(0), w.sum(0)
    full = tg / tw / KG; loo = (tg[None] - wg) / (tw[None] - w) / KG
    dev = loo - loo.mean(0)
    return full, (NPATCH - 1) / NPATCH * dev.T @ dev


def hart(p):
    return (NPATCH - p - 2) / (NPATCH - 1)


lmg = np.log10(Mgal)
key = np.floor(lmg / 0.01).astype(np.int64) * 1000 + np.floor(z / 0.03).astype(np.int64)
_, gi, cnt = np.unique(key, return_inverse=True, return_counts=True)
gi = gi.ravel()
GM = 10 ** (np.bincount(gi, weights=lmg) / cnt); GZ = np.bincount(gi, weights=z) / cnt
NG = len(cnt)
ALL = np.ones(nL, bool)


def pstack(tab, mask=ALL):
    out = np.zeros(15)
    for k in range(15):
        w = np.bincount(gi[mask], weights=WW[mask, k], minlength=NG)
        out[k] = (w @ tab[:, k]) / w.sum()
    return out


gcen = np.sqrt(C.GEDGE_K[:-1] * C.GEDGE_K[1:])
Rik = np.sqrt(C.G_MPC * Mgal[:, None] / gcen[None, :])
RM = (WW * Rik).sum(0) / WW.sum(0)                                           # pair-weighted mean R per bin [Mpc]


def law_vec(Mg, re, a0):
    r = np.geomspace(1e-4, re, 1500)
    Md = Mg * (C.nu_mono(C.G_MPC * Mg / r ** 2 / a0) - 1.0)
    return C._finish(lambda R: C.dsigma(R, r, Md) + Mg / (math.pi * R ** 2), Mg)


def r_bound352_mpc(Mg, foot, ef):
    """CFG352's r_ta definition (r_bound, Delta = DTA_025 vs rho_m at z_l = 0.25) for a lens of baryonic mass Mg [Msun], in Mpc."""
    Mb = Mg * MSK
    return r_bound(M_law(Mb, A0K[foot]), DTA_025, ef) / MPCK


RTA, RTA352, TAB, TAB352 = {}, {}, {}, {}
for foot in FOOTS:
    a0 = C.A0[foot]
    RTA[foot] = np.array([C.r_ta_law(GM[g], a0, GZ[g]) for g in range(NG)])
    RTA352[foot] = np.array([r_bound352_mpc(GM[g], foot, 1.0) for g in range(NG)])
    TAB[foot] = {x: np.array([law_vec(GM[g], x * RTA[foot][g], a0) for g in range(NG)]) for x in XS}
    TAB352[foot] = {x: np.array([law_vec(GM[g], x * RTA352[foot][g], a0) for g in range(NG)]) for x in (EDGE, REF)}
    P(f"  stack P tables {foot}: {time.time() - t:.0f} s; groups {NG}; r_ta_law median {np.median(RTA[foot]):.3f} Mpc; "
      f"CFG352 r_bound median {np.median(RTA352[foot]):.3f} Mpc; ratio r_bound/r_ta_law median {np.median(RTA352[foot] / RTA[foot]):.4f} "
      f"(10-90% {np.percentile(RTA352[foot] / RTA[foot], 10):.4f}-{np.percentile(RTA352[foot] / RTA[foot], 90):.4f})")
TT = np.array([C._finish(lambda R: R ** -0.8 * 1e12, GM[g]) for g in range(NG)])   # CFG377's two-halo template


def chi2(d, C_, h, m, t_, mode="free"):
    Ci = np.linalg.inv(C_); r = d - m
    if mode == "none":
        return float(h * r @ Ci @ r), 0.0
    A = float((t_ @ Ci @ r) / (t_ @ Ci @ t_))
    if mode == "pos":
        A = max(A, 0.0)
    rr = r - A * t_
    return float(h * rr @ Ci @ rr), A


D_ALL, CV_ALL = esd_full_loo(ALL)
TM = pstack(TT)
MST = {f: {x: pstack(TAB[f][x]) for x in XS} for f in FOOTS}
MST352 = {f: {x: pstack(TAB352[f][x]) for x in (EDGE, REF)} for f in FOOTS}


def score(models, sel=None, modes=("free", "pos", "none")):
    d, Cv, tm = D_ALL, CV_ALL, TM
    if sel is not None:
        d, Cv, tm = d[sel], Cv[np.ix_(sel, sel)], tm[sel]
    h = hart(len(d)); out = {}
    for x, m in models.items():
        mm = m if sel is None else m[sel]
        out[x] = {mo: chi2(d, Cv, h, mm, tm, mo) for mo in modes}
    return out


SP = {}
for f in FOOTS:
    s = score(MST[f])
    SP[f] = {str(x): {mo: dict(chi2=s[x][mo][0], A=s[x][mo][1], dchi2_vs_ref=s[x][mo][0] - s[REF][mo][0]) for mo in s[x]} for x in XS}
P(f"\n=== STACK P: CFG413's floor (CFG377 primary, {nL} lenses, 15 bins, jackknife + Hartlap {hart(15):.4f})")
P("  pair-weighted mean R [Mpc]:", np.round(RM, 3))
for f in FOOTS:
    P(f"  [{f}]   x    | chi2 free   dchi2    A_2h  | chi2 A>=0  dchi2 | chi2 A=0   dchi2")
    for x in XS:
        r = SP[f][str(x)]
        P(f"        {x:5.3f} | {r['free']['chi2']:8.3f} {r['free']['dchi2_vs_ref']:+8.3f} {r['free']['A']:7.4f} | "
          f"{r['pos']['chi2']:8.3f} {r['pos']['dchi2_vs_ref']:+7.2f} | {r['none']['chi2']:8.2f} {r['none']['dchi2_vs_ref']:+8.2f}")

# C2: stack P reproduces CFG413's committed rows
diffs = []
for f in FOOTS:
    for xs_, xk in ((str(CTRL), "0.23"), (str(REF), "1.0")):
        for mo in ("free", "none"):
            diffs.append(abs(SP[f][xs_][mo]["chi2"] - J413["primary"][f][xk][mo]["chi2"]))
check("C2 stack P reproduces CFG413's committed x = 0.23 and 1.0 chi2 (free and A = 0) to 0.01", max(diffs) <= 0.01,
      f"max |diff| {max(diffs):.5f}")

# ================================================================================================ verdict (frozen rule, stack P, free A)
DE = {f: SP[f][str(EDGE)]["free"]["dchi2_vs_ref"] for f in FOOTS}
AIN = {f: all(ARANGE[f][0] <= SP[f][str(x)]["free"]["A"] <= ARANGE[f][1] for x in (EDGE, REF)) for f in FOOTS}


def rule(de, ain):
    if any(v > 9.0 for v in de.values()):
        return "STILL KILLED"
    if all(v <= 4.0 for v in de.values()) and all(ain.values()):
        return "REVIVED"
    return "MARGINAL"


VERDICT = rule(DE, AIN)
P(f"\nDECISION (stack P, free A): dchi2_edge (0.232 vs 1.0) = {DE['canonical']:+.3f} / {DE['alt']:+.3f}; "
  f"A(0.232) = {SP['canonical'][str(EDGE)]['free']['A']:.4f} / {SP['alt'][str(EDGE)]['free']['A']:.4f}, "
  f"A(1.0) = {SP['canonical'][str(REF)]['free']['A']:.4f} / {SP['alt'][str(REF)]['free']['A']:.4f}; A in range: {AIN}")
P(f"VERDICT: {VERDICT}")

# ================================================================================================ reported only
REP = {}
# R1: the 9 bins Brouwer+21 trust
trusted = np.nonzero(RM <= 0.3 / 0.6736)[0]
check("R1 setup: the trusted range (R <= 0.3/h Mpc) holds 9 bins", len(trusted) == 9, f"bins {trusted.tolist()}")
R1 = {}
for f in FOOTS:
    s = score({x: MST[f][x] for x in (EDGE, FIRST, REF)}, trusted, ("free", "none"))
    R1[f] = {str(x): {mo: dict(chi2=s[x][mo][0], A=s[x][mo][1], dchi2_vs_ref=s[x][mo][0] - s[REF][mo][0]) for mo in s[x]} for x in s}
R1_DE = {f: R1[f][str(EDGE)]["free"]["dchi2_vs_ref"] for f in FOOTS}
R1_AIN = {f: all(ARANGE[f][0] <= R1[f][str(x)]["free"]["A"] <= ARANGE[f][1] for x in (EDGE, REF)) for f in FOOTS}
REP["R1_trusted_9_bins"] = dict(bins=trusted.tolist(), meanR=RM[trusted].tolist(), hartlap=hart(9), rows=R1, dchi2_edge=R1_DE,
                                A_in_range=R1_AIN, rule_outcome=rule(R1_DE, R1_AIN))
P(f"\nR1 trusted 9 bins (R <= {0.3 / 0.6736:.3f} Mpc; Hartlap {hart(9):.4f}):")
for f in FOOTS:
    r = R1[f]
    P(f"  [{f}] chi2 free x=0.232 {r[str(EDGE)]['free']['chi2']:.3f} (A {r[str(EDGE)]['free']['A']:.3f}), x=0.359 {r[str(FIRST)]['free']['chi2']:.3f} "
      f"(A {r[str(FIRST)]['free']['A']:.3f}), x=1.0 {r[str(REF)]['free']['chi2']:.3f} (A {r[str(REF)]['free']['A']:.3f}); "
      f"dchi2_edge free {r[str(EDGE)]['free']['dchi2_vs_ref']:+.3f}; A=0 {r[str(EDGE)]['none']['dchi2_vs_ref']:+.2f}")
P(f"  rule outcome on the trusted bins (reported only): {REP['R1_trusted_9_bins']['rule_outcome']}")

# R3: drop-one-bin
R3 = {f: [] for f in FOOTS}
for k in range(15):
    sel = np.array([i for i in range(15) if i != k])
    for f in FOOTS:
        s = score({x: MST[f][x] for x in (EDGE, REF)}, sel, ("free",))
        R3[f].append(s[EDGE]["free"][0] - s[REF]["free"][0])
REP["R3_drop_one_bin_dchi2_edge"] = R3
for f in FOOTS:
    P(f"R3 drop-one-bin dchi2_edge [{f}]: {min(R3[f]):+.2f} .. {max(R3[f]):+.2f} (worst when dropping bin {int(np.argmax(R3[f]))}, "
      f"R {RM[int(np.argmax(R3[f]))]:.3f} Mpc); drops with dchi2 > 4: {sum(v > 4 for v in R3[f])}, > 9: {sum(v > 9 for v in R3[f])}")

# R4: stack F with the two-halo amplitude freed (rule stated)
R4 = {}
for tag in ("Amax2", "Afree"):
    de = {f: SF[tag][f]["rows"][str(EDGE)]["dchi2_vs_ref"] for f in FOOTS}
    R4[tag] = dict(dchi2_edge=de, rule_outcome_no_A_range=("STILL KILLED" if any(v > 9 for v in de.values())
                                                          else ("<= 4 both" if all(v <= 4 for v in de.values()) else "MARGINAL")))
    P(f"R4 stack F {tag}: dchi2_edge {de['canonical']:+.2f} / {de['alt']:+.2f} -> {R4[tag]['rule_outcome_no_A_range']}")
STACK_DEP = (R4["Afree"]["rule_outcome_no_A_range"] == "STILL KILLED") != (VERDICT == "STILL KILLED")
REP["R4_stack_F_freed"] = dict(R4, stack_dependent=STACK_DEP)
P(f"  stack-dependent (stack F Afree vs stack P disagree on KILLED vs not): {STACK_DEP}")

# R5: CFG352's own r_ta definition on stack P
R5 = {}
for f in FOOTS:
    s = score(MST352[f], None, ("free", "none"))
    R5[f] = dict(dchi2_edge_free=s[EDGE]["free"][0] - s[REF]["free"][0], A_edge=s[EDGE]["free"][1], A_ref=s[REF]["free"][1],
                 chi2_edge_free=s[EDGE]["free"][0], chi2_ref_free=s[REF]["free"][0], dchi2_edge_none=s[EDGE]["none"][0] - s[REF]["none"][0],
                 ratio_rbound_rtalaw_median=float(np.median(RTA352[f] / RTA[f])))
    P(f"R5 [{f}] CFG352 r_ta on stack P: dchi2_edge free {R5[f]['dchi2_edge_free']:+.3f} (A {R5[f]['A_edge']:.4f} / {R5[f]['A_ref']:.4f}); "
      f"A=0 {R5[f]['dchi2_edge_none']:+.2f}")
REP["R5_cfg352_rta_on_stack_P"] = R5

# R6: effective linear bias of the fitted template
w_proj, rho_m_z = GK["w_proj"], GK["rho_m_z"]
RL = np.geomspace(1e-4, 40.0, 700)
SL = rho_m_z * np.array([w_proj(R0) for R0 in RL]) / 1e12                     # Msun/pc^2, bias 1, z_l = 0.25
ML = np.concatenate([[0], np.cumsum(0.5 * (SL[1:] * RL[1:] + SL[:-1] * RL[:-1]) * np.diff(RL))]) * 2 * math.pi * 1e12 \
    + math.pi * RL[0] ** 2 * SL[0] * 1e12
EL = ML / (math.pi * (RL * 1e6) ** 2) - SL                                   # linear two-halo ESD, Msun/pc^2
Rp_M = GK["Rp"] / MPCK
chk_lin = float(np.max(np.abs(np.interp(np.log(Rp_M[40:]), np.log(RL), EL) / GK["ESD2h"][40:] - 1)))
check("R6 setup: the wide-grid linear two-halo ESD matches FP1's ESD2h (R >= 0.05 Mpc) to 2%", chk_lin < 0.02, f"max rel diff {chk_lin:.4f}")
TL = np.array([C._finish(lambda R: np.interp(np.log(R), np.log(RL), EL) * 1e12, GM[g]) for g in range(NG)])
TLM = pstack(TL)
R6 = {}
for f in FOOTS:
    R6[f] = {}
    for x in (EDGE, REF):
        A = SP[f][str(x)]["free"]["A"]
        b = A * TM / TLM
        R6[f][str(x)] = dict(b_eff=b.tolist(), max=float(b.max()), outer_max=float(b[:6].max()),
                             flag_gt2_bins=[int(i) for i in np.nonzero(b > 2)[0]])
        P(f"R6 [{f}] x={x}: b_eff per bin (outer -> inner) {np.round(b, 2)}; outer 6 bins (R > 0.445 Mpc) max {b[:6].max():.2f}; "
          f"bins with b_eff > 2: {R6[f][str(x)]['flag_gt2_bins']}")
REP["R6_b_eff"] = R6
REP["R6_flag_any_gt2"] = any(R6[f][str(x)]["flag_gt2_bins"] for f in FOOTS for x in (EDGE, REF))
REP["R6_flag_outer_gt2"] = any(R6[f][str(x)]["outer_max"] > 2 for f in FOOTS for x in (EDGE, REF))
# two-halo share of the model at x = 0.232 (reported)
SH = {f: {str(x): (SP[f][str(x)]["free"]["A"] * TM / (MST[f][x] + SP[f][str(x)]["free"]["A"] * TM)).tolist() for x in (EDGE, REF)} for f in FOOTS}
REP["twohalo_share"] = SH
for f in FOOTS:
    P(f"  [{f}] two-halo share of the model at R = {RM[6]:.2f} / {RM[3]:.2f} / {RM[0]:.2f} Mpc: x=0.232 "
      f"{SH[f][str(EDGE)][6]:.2f}/{SH[f][str(EDGE)][3]:.2f}/{SH[f][str(EDGE)][0]:.2f}; x=1.0 {SH[f][str(REF)][6]:.2f}/{SH[f][str(REF)][3]:.2f}/{SH[f][str(REF)][0]:.2f}")

# ================================================================================================ POST-HOC (NOT in FROZEN_CRITERIA; added after the first main run)
PH = {}
# PH1: why the R6 setup check failed. FP1 starts its Sigma integral at 0.02 Mpc with a constant-Sigma core; this lane starts at 1e-4 Mpc.
RL2 = np.geomspace(0.02, 40.0, 700)
SL2 = rho_m_z * np.array([w_proj(R0) for R0 in RL2]) / 1e12
ML2 = np.concatenate([[0], np.cumsum(0.5 * (SL2[1:] * RL2[1:] + SL2[:-1] * RL2[:-1]) * np.diff(RL2))]) * 2 * math.pi * 1e12 \
    + math.pi * RL2[0] ** 2 * SL2[0] * 1e12
EL2 = ML2 / (math.pi * (RL2 * 1e6) ** 2) - SL2
rel1 = np.interp(np.log(Rp_M), np.log(RL), EL) / GK["ESD2h"] - 1
rel2 = np.interp(np.log(Rp_M), np.log(RL2), EL2) / GK["ESD2h"] - 1
PH["PH1_R6_check"] = dict(max_rel_same_inner_edge=float(np.max(np.abs(rel2))), max_rel_R_ge_0p076=float(np.max(np.abs(rel1[Rp_M >= 0.076]))),
                          max_rel_R_ge_0p445=float(np.max(np.abs(rel1[Rp_M >= 0.445]))))
P(f"\nPOST-HOC PH1 (R6 check diagnosis): with FP1's own inner edge (0.02 Mpc) the linear ESD matches FP1 to {PH['PH1_R6_check']['max_rel_same_inner_edge']:.1e}; "
  f"with the 1e-4 Mpc edge the difference is FP1's core approximation, {PH['PH1_R6_check']['max_rel_R_ge_0p076']:.4f} at R >= 0.076 Mpc and "
  f"{PH['PH1_R6_check']['max_rel_R_ge_0p445']:.1e} at R >= 0.445 Mpc (the outer bins that carry the flag). The check FAIL is kept.")
# PH2: stack P with the linear two-halo SHAPE (stacked, bias-like amplitude free) in place of the R^-0.8 template
PH2 = {}
for f in FOOTS:
    s = {x: chi2(D_ALL, CV_ALL, hart(15), MST[f][x], TLM, "free") for x in (EDGE, FIRST, REF)}
    st = {x: chi2(D_ALL[trusted], CV_ALL[np.ix_(trusted, trusted)], hart(9), MST[f][x][trusted], TLM[trusted], "free") for x in (EDGE, REF)}
    PH2[f] = dict(chi2={str(x): s[x][0] for x in s}, b={str(x): s[x][1] for x in s}, dchi2_edge=s[EDGE][0] - s[REF][0],
                  dchi2_first=s[FIRST][0] - s[REF][0], trusted_dchi2_edge=st[EDGE][0] - st[REF][0],
                  trusted_b={str(x): st[x][1] for x in st})
    P(f"POST-HOC PH2 [{f}] stack P, LINEAR two-halo shape (b free): chi2 x=0.232 {s[EDGE][0]:.2f} (b {s[EDGE][1]:.2f}), x=0.359 {s[FIRST][0]:.2f} "
      f"(b {s[FIRST][1]:.2f}), x=1.0 {s[REF][0]:.2f} (b {s[REF][1]:.2f}); dchi2_edge {PH2[f]['dchi2_edge']:+.2f}; first caustic {PH2[f]['dchi2_first']:+.2f}; "
      f"trusted 9 bins dchi2_edge {PH2[f]['trusted_dchi2_edge']:+.2f}")
PH["PH2_linear_template_on_stack_P"] = PH2
PH["PH2_rule_outcome_no_A_range"] = rule({f: PH2[f]["dchi2_edge"] for f in FOOTS}, {f: True for f in FOOTS})
P(f"  PH2 rule outcome (A-range test not applicable, different template): {PH['PH2_rule_outcome_no_A_range']}")
REP["POST_HOC"] = PH

# ================================================================================================ MUTATE
if MUTATE:
    dm = {f: SP[f]["0.05"]["free"]["dchi2_vs_ref"] for f in FOOTS}
    mv = rule(dm, {f: True for f in FOOTS})
    check("MUTATE x = 0.05 on stack P (free A) is STILL KILLED (dchi2 vs x = 1 > 9 on >= 1 footing)", mv == "STILL KILLED",
          f"dchi2 {dm['canonical']:+.2f} / {dm['alt']:+.2f}; A {SP['canonical']['0.05']['free']['A']:.3f} / {SP['alt']['0.05']['free']['A']:.3f}")
    P(f"MUTATE {'DETECTED' if mv == 'STILL KILLED' else 'NOT DETECTED'}")
    REP["mutate"] = dict(dchi2=dm, outcome=mv, detected=mv == "STILL KILLED")

RES = dict(lane="CFG486", mutate=MUTATE, xs=XS, A_range=ARANGE, stack_F=SF, stack_P=SP, meanR_Mpc=RM.tolist(),
           decision=dict(dchi2_edge=DE, A_in_range=AIN, verdict=VERDICT), reported=REP, checks=CHK, n_lenses=nL, n_groups=NG)
P(f"\nchecks {CHK}; elapsed {time.time() - T0:.0f} s")
json.dump(RES, open(os.path.join(HERE, f"cfg486_rescore{SUF}_results.json"), "w"), indent=1, default=float)
open(os.path.join(HERE, f"cfg486_rescore{SUF}.out"), "w").write("\n".join(LOG) + "\n")
sys.exit(0 if all(CHK.values()) else 1)
