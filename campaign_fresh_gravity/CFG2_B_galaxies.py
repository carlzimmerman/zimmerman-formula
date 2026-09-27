#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG2_B -- THE GALAXY SCORES: the settled dark field's galaxy law against SPARC (175 galaxies), both footings.

The principle (CFG2_A): the vacuum fixes a stress scale P_Lambda = a0^2/(8 pi G); in a settled bound system the dark field
carries the stress the vacuum adds to gravity, P_g = P_N + sqrt(P_N P_Lambda).  Around a point mass that is a hydrostatic dark
medium with pressure sqrt(P_N P_Lambda) and the kernel is P2 (derived, unique).  For extended baryons there are two readings:
  E  the stress law holds locally in the field: |g|^2 = |g_N|^2 + a0 |g_N| at every radius (algebraic; = P2 applied pointwise);
  F  the medium's pressure law holds locally: P_d = a0 |g_N|/(8 pi G) with GR hydrostatic equilibrium (differential).
SPARC decides between them.  The design-constraint variants of CFG2_A are scored too (reported): the gravity-only pressure law
Pi(|g|) (P2 at a point mass), the stress-saturated law S, and the thermal sphere T (central pressure P_Lambda, BTFR sigma).
The scope rule (settle iff the settled state can hold the accreted dark mass; the record's Moster+13 accretion) is applied:
galaxies it leaves unsettled are scored with the record's LambdaCDM halo (Moster M_200, Dutton-Maccio c) instead.

STATISTIC AND DATA: the record's (real_research/rar_framework_a0_mlfit.py = FP1 C0/C2): weighted rms of log g_obs - log g_model,
weights (V_obs/e_V)^2 (both clipped at 1 km/s), Upsilon_bul = 1.4 Upsilon_disk, one global Upsilon_disk profiled on 0.30-1.20
step 0.01 (the obstruction variants Pi, S, T on step 0.05, declared, to keep the run short).  The dark medium of the
differential readings is integrated in the spherical (enclosed-mass) reading of the rotmod baryons, M_b(<r) = r V_bar^2/G.

PRE-DECLARED (written before the first full run; the readings' ladder was explored in disclosed scratch runs: E 0.108, F 0.145,
Pi 0.18, S 0.18, T 0.22 dex canonical):
  K1 CONTROL.  real_research/rar_framework_a0_mlfit.py, exec'd read-only, is reproduced exactly (its a0 = 9.3614e-11,
     Upsilon = 0.70: 0.108268467441 dex; its fine-grid optimum 0.70).  EXPECT TRUE.
  K2 CONTROL.  FP1 C2's committed SPARC rms and Upsilon for P2 and nu_mono on both footings are reproduced to < 1e-9.
     EXPECT TRUE.
  H1 [HEADLINE] READING E FITS SPARC: at the framework's a0 on both footings, with one global Upsilon profiled, reading E
     (the principle's P2) reaches a weighted rms <= 0.110 dex at a 3.6-um Upsilon_disk in 0.50-0.80.  EXPECT TRUE.
  H2 (reported) READING F FAILS SPARC'S TIGHTNESS: its best rms exceeds reading E's by >= 0.02 dex on both footings.
     EXPECT TRUE (the scratch ladder).  This is the test that selects the reading.
  H3 (reported) THE OBSTRUCTION VARIANTS FAIL: Pi, S and T all stay >= 0.15 dex on both footings.  EXPECT TRUE.
  H4 (reported) THE SCOPE ON SPARC: the galaxies the scope rule leaves unsettled (M* above ~10^10.65, CFG2_A A8) are scored
     with the record's LambdaCDM halo; the combined rms stays <= 0.120 dex.  UNCERTAIN.
  H5 THE BTFR: on the clean V_flat sample (Q <= 2, e_Vflat/Vflat <= 0.1) the free slope lies in 3.5-4.5 and, at slope 4, the
     observed normalisation agrees within 0.10 dex with reading E's own outer-radius prediction on both footings.  EXPECT TRUE.
  H6 THE HALO SURFACE DENSITY: Burkert fits to reading E's settled dark mass on SPARC (Q <= 2, fit rms < 0.1 dex) give a
     median log rho0 r0 within 0.2 dex of Donato+09's 2.15 on both footings.  EXPECT TRUE.
  H7 THE DIVERSITY: at fixed V_flat the observed inner speed V(2 kpc)/V_flat is predicted from the baryons by reading E with
     Pearson r >= 0.7 on both footings, and better than the record's LambdaCDM halo (Moster + Dutton-Maccio).  EXPECT TRUE.
MUTATE=1 sets the principle's a0 to 0 in every settled-law evaluation: reading E becomes Newton and H1 must FAIL (rc = 1).
"""
import os
import re
import sys
import math
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import least_squares
import CFG2_common as C

R = C.Run("CFG2_B_galaxies")
P, check = R.P, R.check
P(__doc__.split("PRE-DECLARED")[0].strip())
P(__doc__[__doc__.index("PRE-DECLARED"):].strip())
if C.MUTATE:
    P("\n  *** MUTATE=1: the principle's a0 is 0 in every settled-law evaluation; H1 must FAIL ***")
A0P = {f: (0.0 if C.MUTATE else C.A0[f]) for f in C.FOOTS}
A0KP = {f: A0P[f] * C.KPC_REC / 1e6 for f in C.FOOTS}                   # the principle's a0 in (km/s)^2/kpc
GAL = C.load_sparc()
NG = len(GAL)
P(f"\n  SPARC: {NG} galaxies, {sum(len(g['R']) for g in GAL)} points; master rows matched {sum(g['meta'] is not None for g in GAL)}; "
  f"Upsilon grid {C.UPS[0]:.2f}-{C.UPS[-1]:.2f} ({len(C.UPS)} values)")
UPS_C = np.round(np.arange(0.30, 1.2001, 0.05), 2)                     # coarse grid for the obstruction variants
iC = np.array([int(np.argmin(np.abs(C.UPS - u))) for u in UPS_C])

# =============================================================================================== K controls
R.banner("K  CONTROLS: the record's SPARC RAR fit (rar_framework_a0_mlfit.py, exec'd read-only) and FP1 C2")
ML = os.path.join(C.REPO, "real_research", "rar_framework_a0_mlfit.py")
ns, txt = C.exec_slices(ML, [(None, None)], name="rar_mlfit")
a0_ml = ns["a0_fw"]
theirs = ns["scatter"](0.70, 0.98, a0_ml)[0]
S70, W70 = [], []
for g in GAL:
    Vb2 = C.vbar2_grid(g, [0.70])
    s_, w_ = C.rar_sums(g, C.law_E(Vb2, g["R"], a0_ml * C.KPC_REC / 1e6, C.nu_p2), Vb2)
    S70.append(s_[0]); W70.append(w_[0])
mine = math.sqrt(sum(S70) / sum(W70))
m_opt = re.search(r"fine grid: Upsilon_disk = ([0-9.]+), scatter = ([0-9.]+)", txt)
P(f"    rar_framework_a0_mlfit.py: a0 = {a0_ml:.4e}; its scatter() at Upsilon 0.70 = {theirs:.12f}; this lane = {mine:.12f}; "
  f"its fine-grid optimum: {m_opt.group(1) if m_opt else '?'} at {m_opt.group(2) if m_opt else '?'} dex")
check("K1 CONTROL: the record's SPARC RAR fit (real_research/rar_framework_a0_mlfit.py, exec'd read-only) is reproduced exactly: "
      "at its own a0 and Upsilon_disk = 0.70 this lane's statistic equals its scatter() to < 1e-12, and its printed fine-grid "
      "optimum is 0.70 at 0.108 dex",
      f"|mine - theirs| = {abs(mine - theirs):.1e}; optimum {m_opt.group(1) if m_opt else '?'} / {m_opt.group(2) if m_opt else '?'}",
      abs(mine - theirs) < 1e-12 and m_opt is not None and m_opt.group(1) == "0.70" and m_opt.group(2) == "0.108")
fp1 = json.load(open(os.path.join(C.CHAIN, "FP1_static_sector_results.json")))["numbers"]["C2"]["sparc"]
K2, maxd = {}, 0.0
SUMS = {}


def sums_E(f, kernel, a0k):
    S, W = np.zeros((NG, len(C.UPS))), np.zeros((NG, len(C.UPS)))
    for ig, g in enumerate(GAL):
        Vb2 = C.vbar2_grid(g)
        S[ig], W[ig] = C.rar_sums(g, C.law_E(Vb2, g["R"], a0k, kernel), Vb2)
    return S, W


for f in C.FOOTS:
    for kn, kf in (("P2", C.nu_p2), ("mono", C.nu_mono)):
        S, W = sums_E(f, kf, C.A0K_REC[f])
        rm, um, _ = C.best_ups(S, W)
        K2[(f, kn)] = (rm, um)
        maxd = max(maxd, abs(rm - fp1[f][f"rms_{kn}"]), abs(um - fp1[f][f"ups_{kn}"]))
    P(f"    {f:9s}: P2 {K2[(f, 'P2')][0]:.12f} (U {K2[(f, 'P2')][1]:.2f}) vs committed {fp1[f]['rms_P2']:.12f} (U {fp1[f]['ups_P2']:.2f}); "
      f"mono {K2[(f, 'mono')][0]:.12f} (U {K2[(f, 'mono')][1]:.2f}) vs {fp1[f]['rms_mono']:.12f} (U {fp1[f]['ups_mono']:.2f})")
check("K2 CONTROL: FP1 C2's committed SPARC numbers (P2 and nu_mono, both footings, Upsilon profiled) are reproduced to < 1e-9",
      f"max |d| = {maxd:.1e}", maxd < 1e-9)
R.num("K", {"K1_mine": mine, "K1_theirs": theirs, "K2": {f"{k[0]}/{k[1]}": v for k, v in K2.items()}})

# =============================================================================================== H1-H3 the readings
R.banner("H1-H3  THE READINGS ON SPARC: E (stress law local), F (medium pressure local), and the obstruction variants Pi, S, T")
RES = {}
for f in C.FOOTS:
    a0k = A0KP[f]
    S, W = sums_E(f, C.nu_p2, a0k)
    SUMS[(f, "E")] = (S, W)
    RES[(f, "E")] = C.best_ups(S, W)
    SF, WF = np.zeros((NG, len(C.UPS))), np.zeros((NG, len(C.UPS)))
    for ig, g in enumerate(GAL):
        Vb2 = C.vbar2_grid(g)
        SF[ig], WF[ig] = C.rar_sums(g, C.law_F(Vb2, g["R"], a0k), Vb2)
    SUMS[(f, "F")] = (SF, WF)
    RES[(f, "F")] = C.best_ups(SF, WF)
    for kn in ("Pi", "S", "T"):
        Sx, Wx = np.full((NG, len(C.UPS)), np.nan), np.full((NG, len(C.UPS)), np.nan)
        for ig, g in enumerate(GAL):
            Vb2 = C.vbar2_grid(g, UPS_C)
            if kn == "T":
                Mbt = C.mass_budget(g, UPS_C)[0]
                V2 = C.law_T(Vb2, g["R"], a0k if a0k > 0 else 1e-30, Mbt)
            else:
                V2 = C.law_Pi(Vb2, g["R"], a0k if a0k > 0 else 1e-30, saturate=(kn == "S"))
            s_, w_ = C.rar_sums(g, V2, Vb2)
            Sx[ig, iC], Wx[ig, iC] = s_, w_
        keep = np.isfinite(Sx[0])
        Sk, Wk = Sx[:, keep], Wx[:, keep]
        with np.errstate(all="ignore"):
            mse = Sk.sum(0) / Wk.sum(0)
        i = int(np.argmin(mse))
        RES[(f, kn)] = (math.sqrt(mse[i]), float(UPS_C[i]), None)
    SN, WN = sums_E(f, lambda y: np.ones_like(np.asarray(y, float)), C.A0K_REC[f])
    RES[(f, "Newton")] = C.best_ups(SN, WN)
    P(f"    {f:9s}: " + "; ".join(f"{k} {RES[(f, k)][0]:.4f} (U {RES[(f, k)][1]:.2f})" for k in ("E", "F", "Pi", "S", "T", "Newton")) + f"   {R.el()}")
R.num("readings", {f"{k[0]}/{k[1]}": {"rms": v[0], "ups": v[1]} for k, v in RES.items()})
h1 = all(RES[(f, "E")][0] <= 0.110 and 0.50 <= RES[(f, "E")][1] <= 0.80 for f in C.FOOTS)
check("H1 [HEADLINE] READING E FITS SPARC: at the framework's a0 on both footings, one global Upsilon profiled, the principle's "
      "stress law read locally (= P2 at every radius) reaches <= 0.110 dex at Upsilon_disk 0.50-0.80",
      "; ".join(f"{f}: {RES[(f, 'E')][0]:.4f} dex at U {RES[(f, 'E')][1]:.2f}" for f in C.FOOTS), h1)
h2 = all(RES[(f, "F")][0] - RES[(f, "E")][0] >= 0.02 for f in C.FOOTS)
check("H2 (reported) READING F FAILS SPARC'S TIGHTNESS: the medium-pressure law read locally is worse than reading E by >= 0.02 dex "
      "on both footings -- the data select the field-stress (enclosed-mass) reading",
      "; ".join(f"{f}: F {RES[(f, 'F')][0]:.4f} (U {RES[(f, 'F')][1]:.2f}) vs E {RES[(f, 'E')][0]:.4f}" for f in C.FOOTS), h2,
      load_bearing=False,
      reading="F is the same principle around a point mass (P2) but inside extended baryons it under-supplies dark mass by "
              "sqrt((2-n)/(n+2)) (CFG2_A H6); SPARC's point-by-point tracking of g_bar is what rejects it")
h3 = all(RES[(f, k)][0] >= 0.15 for f in C.FOOTS for k in ("Pi", "S", "T"))
check("H3 (reported) THE OBSTRUCTION VARIANTS FAIL: the gravity-only pressure law Pi (P2 at a point mass), stress saturation S and "
      "the thermal sphere T all stay >= 0.15 dex on both footings (Newton for reference)",
      "; ".join(f"{f}: Pi {RES[(f, 'Pi')][0]:.3f}, S {RES[(f, 'S')][0]:.3f}, T {RES[(f, 'T')][0]:.3f}, Newton {RES[(f, 'Newton')][0]:.3f}"
                for f in C.FOOTS), h3, load_bearing=False,
      reading="a dark medium that responds only to its own support (potential depth or total-field magnitude) cannot track the "
              "baryons inside diffuse discs: the settled mass must be fixed by the enclosed baryonic field")

# =============================================================================================== H4 the scope on SPARC
R.banner("H4  THE SCOPE ON SPARC: galaxies the rule leaves unsettled scored with the record's LambdaCDM halo")
LC = {}
for f in C.FOOTS:
    a0k = A0KP[f]
    S_sc, W_sc = SUMS[(f, "E")][0].copy(), SUMS[(f, "E")][1].copy()
    S_lc, W_lc = np.zeros((NG, len(C.UPS))), np.zeros((NG, len(C.UPS)))
    unset = np.zeros((NG, len(C.UPS)), bool)
    for ig, g in enumerate(GAL):
        Mbt, Ms = C.mass_budget(g, C.UPS)
        Vb2 = C.vbar2_grid(g)
        V2lc = np.empty_like(Vb2)
        for iu in range(len(C.UPS)):
            Mh = C.Mh_of_Mstar(max(Ms[iu], 1e5))
            c = C.c_DM14(Mh)
            V2lc[iu] = Vb2[iu] + C.GK * C.M_nfw(g["R"] * C.KPC, Mh, c) / g["R"]
            eta = C.scope(max(Ms[iu], 1e5), Mbt[iu], A0P[f] if A0P[f] > 0 else 1e-300)[0]
            unset[ig, iu] = eta > 1.0
        S_lc[ig], W_lc[ig] = C.rar_sums(g, V2lc, Vb2)
        S_sc[ig] = np.where(unset[ig], S_lc[ig], S_sc[ig])
        W_sc[ig] = np.where(unset[ig], W_lc[ig], W_sc[ig])
    rs, us, iu_s = C.best_ups(S_sc, W_sc)
    rl, ul, _ = C.best_ups(S_lc, W_lc)
    nun = int(unset[:, iu_s].sum())
    names = [GAL[i]["name"] for i in np.where(unset[:, iu_s])[0]]
    LC[f] = dict(rms_E_scope=rs, ups=us, n_unsettled=nun, unsettled=names, rms_LCDM_Moster=rl, ups_LCDM=ul)
    P(f"    {f:9s}: reading E with the scope: {rs:.4f} dex (U {us:.2f}); {nun} galaxies unsettled at that U: {', '.join(names[:14])}"
      f"{' ...' if nun > 14 else ''}")
    P(f"               the record's LambdaCDM halo (Moster M_200 + Dutton-Maccio c) for ALL galaxies: {rl:.4f} dex (U {ul:.2f})")
R.num("scope", LC)
check("H4 (reported) THE SCOPE ON SPARC: with the galaxies the rule leaves unsettled scored with the record's LambdaCDM halo, the "
      "combined rms stays <= 0.120 dex on both footings",
      "; ".join(f"{f}: {LC[f]['rms_E_scope']:.4f} (U {LC[f]['ups']:.2f}, {LC[f]['n_unsettled']} unsettled)" for f in C.FOOTS),
      all(LC[f]["rms_E_scope"] <= 0.120 for f in C.FOOTS), load_bearing=False)

# =============================================================================================== H5 BTFR
R.banner("H5  THE BARYONIC TULLY-FISHER RELATION: slope, normalisation, and reading E's own outer-radius prediction")
BT = {}
for f in C.FOOTS:
    u = RES[(f, "E")][1]
    lm, lv, lvl = [], [], []
    for g in GAL:
        m = g["meta"]
        if m is None or m["Q"] > 2 or m["Vflat"] <= 0 or m["eVflat"] / m["Vflat"] > 0.1:
            continue
        Mbt = C.mass_budget(g, [u])[0][0]
        Vb2 = C.vbar2_grid(g, [u])
        V2 = C.law_E(Vb2, g["R"], A0KP[f], C.nu_p2)[0]
        vl = math.sqrt(max(V2[-1], 1e-6))
        lm.append(math.log10(Mbt)); lv.append(math.log10(m["Vflat"])); lvl.append(math.log10(vl))
    lm, lv, lvl = map(np.array, (lm, lv, lvl))
    b, a = np.polyfit(lv, lm, 1)
    A_obs = 10 ** np.median(lm - 4 * lv)
    A_law = 10 ** np.median(lm - 4 * lvl)
    A_deep = 1.0 / (C.GK * A0KP[f]) if A0KP[f] > 0 else float("inf")
    BT[f] = dict(n=len(lm), slope=b, A_obs=A_obs, A_law=A_law, A_deep=A_deep, obs_minus_law=math.log10(A_obs / A_law),
                 obs_minus_deep=(math.log10(A_obs / A_deep) if np.isfinite(A_deep) else float("nan")))
    P(f"    {f:9s} (U {u:.2f}, {len(lm)} galaxies): free slope {b:.3f}; at slope 4: A_obs = {A_obs:.1f} Msun/(km/s)^4; reading E's outer "
      f"velocities give {A_law:.1f} (obs - law {BT[f]['obs_minus_law']:+.3f} dex); deep limit 1/(G a0) = {A_deep:.1f} "
      f"(obs - deep {BT[f]['obs_minus_deep']:+.3f} dex)")
R.num("BTFR", BT)
check("H5 THE BTFR: on the clean V_flat sample the free slope lies in 3.5-4.5 and, at slope 4, the observed normalisation agrees "
      "within 0.10 dex with reading E's own outer-radius prediction on both footings",
      "; ".join(f"{f}: slope {v['slope']:.2f}, obs-law {v['obs_minus_law']:+.3f}, obs-deep {v['obs_minus_deep']:+.3f} dex" for f, v in BT.items()),
      all(3.5 <= v["slope"] <= 4.5 and abs(v["obs_minus_law"]) <= 0.10 for v in BT.values()))

# =============================================================================================== H6 Sigma
R.banner("H6  THE HALO SURFACE DENSITY: Burkert fits to the settled dark mass (reading E; reading F reported)")


def burkert_M(r, rho0, r0):
    x = r / r0
    return 2 * math.pi * rho0 * r0 ** 3 * (0.5 * np.log1p(x * x) + np.log1p(x) - np.arctan(x))


def fit_burkert(r, Md):
    ok = Md > 0
    if ok.sum() < 5:
        return None
    rr, mm = r[ok], Md[ok]

    def res(p):
        return np.log10(burkert_M(rr, 10 ** p[0], 10 ** p[1])) - np.log10(mm)
    best_ = None
    for l0 in (-1.0, 0.0, 1.0, 2.0):
        s = least_squares(res, [7.5, l0], method="lm")
        if best_ is None or s.cost < best_.cost:
            best_ = s
    rms = math.sqrt(np.mean(best_.fun ** 2))
    rho0, r0 = 10 ** best_.x[0], 10 ** best_.x[1]                   # Msun/kpc^3, kpc
    return rho0 * r0 / 1e6, r0, rms                                  # Msun/pc^2, kpc


SG = {}
for f in C.FOOTS:
    for rd in ("E", "F"):
        u = RES[(f, rd)][1]
        vals, core_rM = [], []
        for g in GAL:
            m = g["meta"]
            if m is None or m["Q"] > 2:
                continue
            Vb2 = C.vbar2_grid(g, [u])
            V2 = C.law_E(Vb2, g["R"], A0KP[f], C.nu_p2) if rd == "E" else C.law_F(Vb2, g["R"], A0KP[f])
            Md = (V2[0] - Vb2[0]) * g["R"] / C.GK
            fb = fit_burkert(g["R"], Md)
            if fb is None or fb[2] >= 0.1:
                continue
            Mbt = C.mass_budget(g, [u])[0][0]
            rM = math.sqrt(C.GK * Mbt / C.A0K_REC[f])
            vals.append(math.log10(fb[0])); core_rM.append(fb[1] / rM)
        vals = np.array(vals)
        SG[(f, rd)] = dict(n=len(vals), median_log_rho0r0=float(np.median(vals)) if len(vals) else float("nan"),
                           scatter=float(np.std(vals)) if len(vals) else float("nan"),
                           r0_over_rM=float(np.median(core_rM)) if core_rM else float("nan"))
        P(f"    {f:9s} reading {rd}: {len(vals)} galaxies (Q <= 2, Burkert fit rms < 0.1 dex): log rho0 r0 = {SG[(f, rd)]['median_log_rho0r0']:.3f} "
          f"+- {SG[(f, rd)]['scatter']:.3f} (Msun/pc^2; Donato+09 2.15 +- 0.2; ceiling a0/(2 pi G) = {math.log10(C.SIGMA_M[f]):.3f}); "
          f"core r0 = {SG[(f, rd)]['r0_over_rM']:.2f} r_M")
R.num("Sigma", {f"{k[0]}/{k[1]}": v for k, v in SG.items()})
check("H6 THE HALO SURFACE DENSITY: Burkert fits to reading E's settled dark mass on SPARC give a median log rho0 r0 within "
      "0.2 dex of Donato+09's 2.15 on both footings (the fitted Burkert product sits near the derived column ceiling a0/(2 pi G))",
      "; ".join(f"{f}: {SG[(f, 'E')]['median_log_rho0r0']:.3f} +- {SG[(f, 'E')]['scatter']:.3f} ({SG[(f, 'E')]['n']} galaxies), "
                f"core {SG[(f, 'E')]['r0_over_rM']:.2f} r_M" for f in C.FOOTS),
      all(abs(SG[(f, "E")]["median_log_rho0r0"] - 2.15) <= 0.2 for f in C.FOOTS))

# =============================================================================================== H7 diversity
R.banner("H7  THE DIVERSITY: V(2 kpc)/V_flat predicted from the baryons, at fixed V_flat")
DV = {}
for f in C.FOOTS:
    u = RES[(f, "E")][1]
    obs, prE, prF, prL = [], [], [], []
    for g in GAL:
        m = g["meta"]
        R_ = g["R"]
        if m is None or m["Q"] > 2 or m["Vflat"] <= 0 or not (R_[0] <= 2.0 <= R_[-1]):
            continue
        Vb2 = C.vbar2_grid(g, [u])
        VE = np.sqrt(np.maximum(C.law_E(Vb2, R_, A0KP[f], C.nu_p2)[0], 0))
        VF = np.sqrt(np.maximum(C.law_F(Vb2, R_, A0KP[f])[0], 0))
        Ms = C.mass_budget(g, [u])[1][0]
        Mh = C.Mh_of_Mstar(max(Ms, 1e5))
        VL = np.sqrt(np.maximum(Vb2[0] + C.GK * C.M_nfw(R_ * C.KPC, Mh, C.c_DM14(Mh)) / R_, 0))
        vf = m["Vflat"]
        obs.append(math.log10(np.interp(2.0, R_, g["Vobs"]) / vf))
        prE.append(math.log10(max(np.interp(2.0, R_, VE), 1e-3) / vf))
        prF.append(math.log10(max(np.interp(2.0, R_, VF), 1e-3) / vf))
        prL.append(math.log10(max(np.interp(2.0, R_, VL), 1e-3) / vf))
    obs, prE, prF, prL = map(np.array, (obs, prE, prF, prL))
    DV[f] = dict(n=len(obs), spread_obs=float(np.std(obs)),
                 r_E=float(np.corrcoef(obs, prE)[0, 1]), rms_E=float(np.sqrt(np.mean((obs - prE) ** 2))), spread_E=float(np.std(prE)),
                 r_F=float(np.corrcoef(obs, prF)[0, 1]), rms_F=float(np.sqrt(np.mean((obs - prF) ** 2))),
                 r_LCDM=float(np.corrcoef(obs, prL)[0, 1]), rms_LCDM=float(np.sqrt(np.mean((obs - prL) ** 2))), spread_LCDM=float(np.std(prL)))
    P(f"    {f:9s} ({len(obs)} galaxies with 2 kpc covered): observed spread of log V(2kpc)/V_flat {DV[f]['spread_obs']:.3f} dex; "
      f"reading E: r = {DV[f]['r_E']:.3f}, rms {DV[f]['rms_E']:.3f}, predicted spread {DV[f]['spread_E']:.3f}; reading F: r = {DV[f]['r_F']:.3f}, "
      f"rms {DV[f]['rms_F']:.3f}; LambdaCDM (Moster + DM14): r = {DV[f]['r_LCDM']:.3f}, rms {DV[f]['rms_LCDM']:.3f}, spread {DV[f]['spread_LCDM']:.3f}")
R.num("diversity", DV)
check("H7 THE DIVERSITY: at fixed V_flat the observed V(2 kpc)/V_flat is predicted from the baryons by reading E with Pearson "
      "r >= 0.7 on both footings, and with a smaller rms than the record's LambdaCDM halo",
      "; ".join(f"{f}: r_E {v['r_E']:.3f} (rms {v['rms_E']:.3f}) vs LCDM r {v['r_LCDM']:.3f} (rms {v['rms_LCDM']:.3f})" for f, v in DV.items()),
      all(v["r_E"] >= 0.7 and v["rms_E"] < v["rms_LCDM"] for v in DV.values()))

# =============================================================================================== W ledger
R.banner("W  LEDGER (galaxies)")
R.ledger("CFG2-B1", "PASS" if h1 else "FAIL", f"reading E (the principle's P2) on SPARC: {RES[('canonical', 'E')][0]:.4f} / {RES[('alt', 'E')][0]:.4f} dex", "H1")
R.ledger("CFG2-B2", "SELECTED", f"reading F rejected: {RES[('canonical', 'F')][0]:.4f} / {RES[('alt', 'F')][0]:.4f} dex", "H2")
R.ledger("CFG2-B3", "CONSTRAINT", f"gravity-only/thermal settling: Pi {RES[('canonical', 'Pi')][0]:.3f}, S {RES[('canonical', 'S')][0]:.3f}, "
         f"T {RES[('canonical', 'T')][0]:.3f} dex (canonical)", "H3")
R.ledger("CFG2-B4", "MEASURED", f"BTFR slope {BT['canonical']['slope']:.2f}/{BT['alt']['slope']:.2f}; obs-law {BT['canonical']['obs_minus_law']:+.3f}/"
         f"{BT['alt']['obs_minus_law']:+.3f} dex", "H5")
R.ledger("CFG2-B5", "MEASURED", f"Burkert log rho0 r0 {SG[('canonical', 'E')]['median_log_rho0r0']:.2f}/{SG[('alt', 'E')]['median_log_rho0r0']:.2f} "
         f"(Donato 2.15)", "H6")
sys.exit(R.finish())
