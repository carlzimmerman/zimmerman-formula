#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG179 S2 -- Q-merge, numbers beside the record's committed tests (FROZEN_QUESTION.md M4-M9).  Seconds.

Read-only inputs (committed): CFG8_chae_kernel_results.json (per-galaxy fits V4 = P2 canonical, V5 = P2 alt, and CFG8's
environmental fits), real_research/reviews/directional_efe_2026/laneB_data/chae21_env.csv, real_research/data/
freundlich2022_coma_udgs.tsv (with L23's conventions), CFG7_hierarchy_fg001.out (the H0 scorecard lines).

  T   the quench table: how much of a system's own boost survives inside a larger river (P2 1-D and E7)
  M5  Chae (gate 1.15): the zero-intercept amplitude A of e_fit = A e_env; ownership A = 0, 1-D merge A = 1, E7 A in [0.46, 0.71]
  M6  Coma UDGs (gate 1.16): the E7 merge offset at the beta-model field (0.845 a0 at 1.13 Mpc), against 0.235 dex
  M7  DR4 (gate 4.06): point-field gamma estimates (never scored) beside the committed Arm A / MI / Arm C numbers
  M8  Solar System (G5): the alpha = 1 monopole control and the external-field quadrupole scale
  M9  the committed scorecard (CFG7 H0)

MUTATE=1: every external field set to 0 (the ownership rule): the Coma headline must flip; DR4 merge rows become 1.000.
"""
import os, csv, json, math
import numpy as np
from scipy.stats import spearmanr
from cfg179_common import (Run, MUTATE, REPO, A0, FOOTS, C_SI, G_SI, MSUN, SJ_EARTH, Q2_BOUND, SIGMA_TOT_DR4,
                           F_p2, M_p2, L_p2, nu_p2, mu_fw, e7_root, qumond1d)

R = Run("cfg179_s2_merge_numbers")
CFG = os.path.join(REPO, "campaign_fresh_gravity")
EXT = 0.0 if MUTATE else 1.0                                        # MUTATE: the ownership rule (no external field)
R.P(f"external-field scale = {EXT}  ({'OWNERSHIP: no external field anywhere' if MUTATE else 'merging rivers: the host field acts'})")

# =============================================================================================== T quench table
R.banner("T   HOW MUCH OF A SYSTEM'S OWN BOOST SURVIVES INSIDE A LARGER RIVER  (x_merge / x_isolated, x = g_int/a0)")
cases = [("SPARC median env field (CFG8 V4/V5 med e_env)", {"canonical": 0.0479 * A0["canonical"], "alt": 0.0435 * A0["alt"]}),
         ("Coma UDG, beta-model at 1.13 Mpc (L23: 0.845 a0)", {f: 0.845 * 9.3619e-11 for f in FOOTS}),
         ("wide binary / the Sun in the Milky Way (1.778e-10)", {f: 1.778e-10 for f in FOOTS})]
T = {}
for foot in FOOTS:
    a0 = A0[foot]
    for name, gx in cases:
        g = gx[foot] * EXT
        e = g / a0
        row = []
        for bb in (0.01, 0.1, 1.0, 10.0):
            xi = F_p2(bb)
            x1 = qumond1d(bb, e)
            x7 = e7_root(bb, math.sqrt(2) * e)
            row.append((bb, x1 / xi, x7 / xi))
        T[f"{foot}|{name}"] = row
        R.P(f"  {foot:9s} {name:52s} g_ext/a0 = {e:.4f}:  " +
            "  ".join(f"b={bb:g}: 1D {r1:.3f} / E7 {r7:.3f}" for bb, r1, r7 in row))
R.num("quench", T)
R.P("  reading: deep inside a strong host river (g_ext ~ a0) a faint system keeps only a fraction of its own MOND boost;")
R.P("  at b >> 1 both are ~1 (Newtonian).  The E7 form quenches less than the 1-D form at small g_ext (susceptibility 0.71x).")

# =============================================================================================== M5 Chae
R.banner("M5  CHAE'S EXTERNAL-FIELD SIGNAL (gate 1.15): does the fitted e track the environment with amplitude 0 or 1?")
J = json.load(open(os.path.join(CFG, "CFG8_chae_kernel_results.json")))
FITS, CORR8 = J["numbers"]["FITS"], J["numbers"]["CORR"]
env = {r["galaxy"].strip(): r for r in csv.DictReader(open(os.path.join(
    REPO, "real_research", "reviews", "directional_efe_2026", "laneB_data", "chae21_env.csv")))}
GDAG = 1.2e-10
VAR = {"canonical": "V4", "alt": "V5"}
M5 = {}
ctrl_ok = True
for foot in FOOTS:
    vk, a0 = VAR[foot], A0[foot]
    rows = [r for r in FITS[vk] if r["name"] in env]
    y = np.array([r["e50"] for r in rows])
    w = np.array([1.0 / max(0.5 * (r["e84"] - r["e16"]), 1e-3) ** 2 for r in rows])
    w = np.minimum(w, 1.0 / 0.005 ** 2)

    def e_env(which):
        out = []
        for r in rows:
            E_ = env[r["name"]]
            if which == "mean":
                lN = 0.5 * (float(E_["log_eN_maxclu"]) + float(E_["log_eN_noclu"]))
            else:
                lN = float(E_[f"log_eN_{which}"])
            out.append(F_p2(10 ** lN * GDAG / a0))
        return np.array(out) * EXT

    x = e_env("mean")
    # control C1: CFG8's weighted fit with intercept
    A = np.vstack([np.ones_like(x), x]).T * np.sqrt(w)[:, None]
    beta = np.linalg.lstsq(A, y * np.sqrt(w), rcond=None)[0] if EXT else np.array([np.nan, np.nan])
    cov = np.linalg.inv(A.T @ A) if EXT else np.full((2, 2), np.nan)
    rho = spearmanr(x, y)[0] if EXT else float("nan")
    c8 = CORR8[vk]
    dev = max(abs(beta[0] - c8["intercept"]), abs(beta[1] - c8["slope"]), abs(math.sqrt(cov[0, 0]) - c8["e_int"]),
              abs(math.sqrt(cov[1, 1]) - c8["e_slope"]), abs(rho - c8["rho"]), abs(np.median(x) - c8["med_env"])) if EXT else float("nan")
    this_ok = (len(rows) == c8["n"]) and (dev < 1e-3 if EXT else True)
    ctrl_ok &= this_ok
    R.P(f"  C1 {foot} ({vk}): N = {len(rows)} (CFG8 {c8['n']}); intercept {beta[0]:+.4f} (CFG8 {c8['intercept']:+.4f}), slope "
        f"{beta[1]:+.4f} +- {math.sqrt(cov[1, 1]):.4f} (CFG8 {c8['slope']:+.4f} +- {c8['e_slope']:.4f}), Spearman {rho:+.3f} "
        f"(CFG8 {c8['rho']:+.3f}), median e_env {np.median(x):.4f}; max deviation {dev:.1e}")
    res = {}
    for which in ("mean", "maxclu", "noclu"):
        xx = e_env(which)
        sxx = float(np.sum(w * xx * xx))
        if sxx <= 0:
            res[which] = dict(A=float("nan"), note="no external field: the amplitude is undefined (ownership predicts e = 0)")
            R.P(f"  {foot:9s} env={which:6s}: no external field (MUTATE) -> the amplitude test is undefined; ownership's e = 0 stands")
            continue
        Ah = float(np.sum(w * xx * y) / sxx)
        sf = 1.0 / math.sqrt(sxx)
        chi2 = float(np.sum(w * (y - Ah * xx) ** 2))
        dof = len(y) - 1
        sp_ = sf * math.sqrt(max(1.0, chi2 / dof))
        z0, z1 = Ah / sp_, (Ah - 1.0) / sp_
        z7 = [(Ah - a) / sp_ for a in (0.46, 0.71)]
        z7min = 0.0 if 0.46 <= Ah <= 0.71 else min(abs(q) for q in z7)
        merge_ok = (abs(z1) <= 2) or (z7min <= 2)
        if merge_ok and abs(z0) > 2:
            cls = "SUPPORTS THE MERGE EFE"
        elif abs(z0) <= 2 and not merge_ok:
            cls = "SUPPORTS OWNERSHIP"
        else:
            cls = "NON-DIAGNOSTIC"
        res[which] = dict(A=Ah, sig_formal=sf, sig=sp_, chi2=chi2, dof=dof, z_own=z0, z_1D=z1, z_E7=z7min, cls=cls,
                          med_env=float(np.median(xx)))
        R.P(f"  {foot:9s} env={which:6s}: A = {Ah:+.3f} +- {sp_:.3f} (formal {sf:.3f}; chi2/dof {chi2 / dof:.2f});  "
            f"ownership A=0 at {z0:+.2f} sigma, 1-D merge A=1 at {z1:+.2f} sigma, E7 bracket [0.46,0.71] at {z7min:.2f} sigma  "
            f"-> {cls}  (median e_env {np.median(xx):.4f})")
    # ---------------- M5-R: ADDED AFTER THE FIRST RUN (post hoc, labelled; cfg179_s2_merge_numbers_firstrun.out holds the run
    # without it).  Reason: the frozen zero-intercept amplitude cannot tell galaxy-by-galaxy tracking of the environment from a
    # uniform positive offset of e_fit (e_env > 0 for every galaxy), chi2/dof ~ 9-11, and CFG8 names NGC 5055 / NGC 5033 as
    # carrying its weighted slope.  These rows qualify the declared result; they do not replace it.
    if EXT:
        xm = e_env("mean")

        def classify(Ah, s):
            z0, z1 = Ah / s, (Ah - 1.0) / s
            z7 = 0.0 if 0.46 <= Ah <= 0.71 else min(abs((Ah - a) / s) for a in (0.46, 0.71))
            mo = abs(z1) <= 2 or z7 <= 2
            return ("SUPPORTS THE MERGE EFE" if (mo and abs(z0) > 2) else
                    "SUPPORTS OWNERSHIP" if (abs(z0) <= 2 and not mo) else "NON-DIAGNOSTIC"), z0, z1, z7

        Aw = np.vstack([np.ones_like(xm), xm]).T * np.sqrt(w)[:, None]
        bb = np.linalg.lstsq(Aw, y * np.sqrt(w), rcond=None)[0]
        cv = np.linalg.inv(Aw.T @ Aw)
        chi2i = float(np.sum(w * (y - bb[0] - bb[1] * xm) ** 2))
        infl = math.sqrt(max(1.0, chi2i / (len(y) - 2)))
        sl, ssl = float(bb[1]), math.sqrt(cv[1, 1]) * infl
        ca = classify(sl, ssl)
        keep = np.array([r["name"] not in ("NGC5055", "NGC5033") for r in rows])
        sxx2 = float(np.sum(w[keep] * xm[keep] ** 2))
        A2 = float(np.sum(w[keep] * xm[keep] * y[keep]) / sxx2)
        chi22 = float(np.sum(w[keep] * (y[keep] - A2 * xm[keep]) ** 2))
        s2 = math.sqrt(max(1.0, chi22 / (keep.sum() - 1)) / sxx2)
        cb = classify(A2, s2)
        rng = np.random.default_rng(179)
        A3 = float(np.sum(xm * y) / np.sum(xm * xm))
        boot = []
        for _ in range(4000):
            ii = rng.integers(0, len(y), len(y))
            boot.append(np.sum(xm[ii] * y[ii]) / np.sum(xm[ii] * xm[ii]))
        s3 = float(np.std(boot))
        cc = classify(A3, s3)
        lo = np.array([r["x0"] < -10.3 for r in rows])
        A4 = float(np.median(y[lo]) / np.median(xm[lo]))
        boot4 = []
        for _ in range(4000):
            ii = rng.integers(0, lo.sum(), lo.sum())
            boot4.append(np.median(y[lo][ii]) / np.median(xm[lo][ii]))
        s4 = float(np.std(boot4))
        cd = classify(A4, s4)
        post = dict(free_intercept=dict(intercept=float(bb[0]), slope=sl, sig_infl=ssl, chi2dof=chi2i / (len(y) - 2), cls=ca[0],
                                        z_own=ca[1], z_1D=ca[2], z_E7=ca[3]),
                    drop_NGC5055_5033=dict(A=A2, sig=s2, n=int(keep.sum()), cls=cb[0], z_own=cb[1], z_1D=cb[2], z_E7=cb[3]),
                    equal_weight_boot=dict(A=A3, sig=s3, cls=cc[0], z_own=cc[1], z_1D=cc[2], z_E7=cc[3]),
                    lowacc_median_ratio=dict(A=A4, sig=s4, n=int(lo.sum()), cls=cd[0], z_own=cd[1], z_1D=cd[2], z_E7=cd[3]))
        res["POSTHOC"] = post
        R.P(f"  {foot:9s} M5-R [POST HOC, added after the first run]:")
        R.P(f"      (a) free intercept (the tracking test), chi2-inflated: intercept {bb[0]:+.4f}, slope {sl:+.3f} +- {ssl:.3f} "
            f"(chi2/dof {chi2i / (len(y) - 2):.1f}) -> A=0 at {ca[1]:+.2f}, A=1 at {ca[2]:+.2f} sigma -> {ca[0]}")
        R.P(f"      (b) zero intercept without NGC 5055 and NGC 5033 (N = {keep.sum()}): A = {A2:+.3f} +- {s2:.3f} -> A=0 at "
            f"{cb[1]:+.2f}, A=1 at {cb[2]:+.2f}, E7 at {cb[3]:.2f} sigma -> {cb[0]}")
        R.P(f"      (c) zero intercept, equal weights, bootstrap error: A = {A3:+.3f} +- {s3:.3f} -> A=0 at {cc[1]:+.2f}, A=1 at "
            f"{cc[2]:+.2f}, E7 at {cc[3]:.2f} sigma -> {cc[0]}")
        R.P(f"      (d) low-acceleration galaxies (x0 < -10.3, N = {lo.sum()}), ratio of medians, bootstrap: A = {A4:+.3f} +- "
            f"{s4:.3f} -> A=0 at {cd[1]:+.2f}, A=1 at {cd[2]:+.2f}, E7 at {cd[3]:.2f} sigma -> {cd[0]}")
    M5[foot] = res
R.check("C1 CONTROL: CFG8's V4 and V5 environmental fits (N, intercept, slope and their errors, Spearman rho, median e_env) "
        "reproduced to 1e-3 from its committed per-galaxy fits", ctrl_ok, "see the C1 rows above")
R.num("M5", M5)
if not MUTATE:
    cls_c, cls_a = M5["canonical"]["mean"]["cls"], M5["alt"]["mean"]["cls"]
    R.check("M5 (reported) Chae, geometric-mean field: the declared reading rule's class on both footings",
            True, f"canonical: {cls_c}; alt: {cls_a}.  Carried beside it (committed, CFG8 H2): no rank correlation, Spearman p "
            f"0.87 / 0.76, and the weighted slope rests on a few precise galaxies (NGC 5055, NGC 5033)", load_bearing=False)
R.P("  committed beside it: B's zero is 1.7 sigma (P2 canonical) / 2.7 sigma (P2 alt) from Chae's refit medians (CFG8 H1);")
R.P("  low-acceleration median fitted e = +0.021 +- 0.012 (canonical) / +0.032 +- 0.012 (alt) against median e_env 0.048 / 0.044.")

# =============================================================================================== M6 Coma
R.banner("M6  THE COMA UDGs (gate 1.16) under a merging river: the E7 merge offset (stars only)")
Gl, MSl, KPCl = 6.674e-11, 1.989e30, 3.0857e19                   # L23's constants (its data conventions)
A0_L23 = 9.3619e-11
rows = [l.rstrip("\n").split("\t") for l in open(os.path.join(REPO, "real_research", "data", "freundlich2022_coma_udgs.tsv"))
        if l.strip() and not l.startswith("#")]
hd = {h: i for i, h in enumerate(rows[0])}
UDG = []
for r in rows[1:]:
    f_ = lambda k: float(r[hd[k]])
    r12 = 4.0 / 3.0 * f_("Re_kpc") * KPCl
    Mst = f_("L_1e8") * 1e8 * f_("ML") * MSl
    UDG.append(dict(name=r[hd["name"]], gobs=3.0 * (f_("sig") * 1e3) ** 2 / r12, gbar=Gl * (Mst / 2.0) / r12 ** 2,
                    err=math.hypot(f_("elgobs"), f_("elgbar"))))
W = np.array([1.0 / u["err"] ** 2 for u in UDG])


def wmean(off):
    off = np.asarray(off)
    return float(np.sum(W * off) / np.sum(W))


nu_rar = lambda yy: 1.0 / (1.0 - math.exp(-math.sqrt(yy)))
iso_rar = wmean([math.log10(u["gobs"] / (nu_rar(u["gbar"] / A0_L23) * u["gbar"])) for u in UDG])
R.check("C2 CONTROL: L23's isolated stars-only offset reproduced (its nu_RAR, a0 = 9.3619e-11, its estimator and weights)",
        len(UDG) == 11 and abs(iso_rar - 0.3965) < 0.003, f"N = {len(UDG)}; offset {iso_rar:+.4f} dex (L23 +0.3965)")
SIG_TOT = 0.235
RATIOS = (0.427, 0.653, 0.845, 1.059)
M6 = {}
for foot in FOOTS:
    a0 = A0[foot]
    iso = wmean([math.log10(u["gobs"] / (a0 * F_p2(u["gbar"] / a0))) for u in UDG])
    rowset = {}
    for q in RATIOS:
        g = q * A0_L23 * EXT
        e = g / a0
        off7 = wmean([math.log10(u["gobs"] / (a0 * e7_root(u["gbar"] / a0, math.sqrt(2) * e))) for u in UDG])
        off1 = wmean([math.log10(u["gobs"] / (a0 * qumond1d(u["gbar"] / a0, e))) for u in UDG])
        if e > 0:
            ze = M_p2(e)
            coup = nu_p2(ze) * (1 + L_p2(ze) / 3)
            offi = wmean([math.log10(u["gobs"] / (coup * u["gbar"])) for u in UDG])
        else:
            offi = iso
        rowset[q] = dict(E7=off7, P2_1D=off1, P2_iso=offi, s_E7=off7 / SIG_TOT, s_1D=off1 / SIG_TOT, s_iso=offi / SIG_TOT)
        R.P(f"  {foot:9s} g_ext = {q:.3f} x 9.3619e-11 (g_ext/a0 = {e:.3f}): E7 {off7:+.3f} dex ({off7 / SIG_TOT:.1f} sigma) | "
            f"P2 1-D {off1:+.3f} ({off1 / SIG_TOT:.1f}) | P2 isotropic EFE-dominated {offi:+.3f} ({offi / SIG_TOT:.1f})")
    M6[foot] = dict(iso_P2=iso, rows=rowset)
    R.P(f"  {foot:9s} isolated P2, stars only (no merge): {iso:+.3f} dex ({iso / SIG_TOT:.1f} sigma at the EFE reading's 0.235)")
R.num("M6", {f: dict(iso_P2=M6[f]["iso_P2"], rows={str(k): v for k, v in M6[f]["rows"].items()}) for f in FOOTS})
hc, ha = M6["canonical"]["rows"][0.845]["s_E7"], M6["alt"]["rows"][0.845]["s_E7"]
R.check("M6 [HEADLINE] the E7 merging river FAILS the Coma UDGs: its stars-only offset at the beta-model field (0.845 a0, "
        "1.13 Mpc) exceeds 2 sigma of the 0.235-dex total error on both footings",
        hc > 2 and ha > 2, f"canonical {M6['canonical']['rows'][0.845]['E7']:+.3f} dex = {hc:.1f} sigma; alt "
        f"{M6['alt']['rows'][0.845]['E7']:+.3f} dex = {ha:.1f} sigma.  Committed beside it: L23 EFE rival +1.159 / +1.112 "
        f"(4.9 / 4.7 sigma); CFG31 B (ownership + infall gas) +0.234 / +0.195 (1.3 / 1.1 sigma); first infall 2.7 sigma (L23)")

# =============================================================================================== M7 DR4
R.banner("M7  GAIA DR4 WIDE BINARIES (gate 4.06): what a merging river predicts")
M7 = {}
ctrl3 = True
for foot in FOOTS:
    a0 = A0[foot]
    for gname, gx in (("primary 1.778e-10", 1.778e-10), ("alt convention 2.078e-10", 2.078e-10)):
        e = gx / a0
        ze = M_p2(e)
        nu, L = nu_p2(ze), L_p2(ze)
        rows_ = dict(perp=math.sqrt(nu), par=math.sqrt(nu * (1 + L)), iso=math.sqrt(nu * (1 + L / 3)),
                     E7=math.sqrt(1.0 / mu_fw(math.sqrt(2) * e)))
        if MUTATE:
            rows_ = {k: 1.0 for k in rows_}
        M7[f"{foot}|{gname}"] = dict(z_e=ze, **rows_)
        R.P(f"  {foot:9s} g_ext {gname:25s}: z_e = {ze:.4f}; point-field gamma: P2 perp {rows_['perp']:.4f}, par "
            f"{rows_['par']:.4f}, isotropic {rows_['iso']:.4f}; E7 {rows_['E7']:.4f}")
    ze_c = M_p2(1.778e-10 / A0[foot])
    if foot == "canonical":
        ctrl3 &= abs(ze_c - 1.4647) < 2e-3 and abs(math.sqrt(nu_p2(ze_c)) - 1.1389) < 1e-3
    else:
        ctrl3 &= abs(ze_c - 1.1513) < 2e-3
R.check("C3 CONTROL: the P2 inversion of g_ext = 1.778e-10 gives the prereg's y_extN = 1.4647 (canonical) / 1.1513 (alt) and "
        "sqrt(nu) = 1.1389 (the prereg's framework-as-MG point field)", ctrl3,
        f"canonical z_e {M_p2(1.778e-10 / A0['canonical']):.4f}, sqrt(nu) {math.sqrt(nu_p2(M_p2(1.778e-10 / A0['canonical']))):.4f}; "
        f"alt z_e {M_p2(1.778e-10 / A0['alt']):.4f}")
COMMITTED = [("Arm A: merge, P2 as modified gravity, full nonlinear solve (canonical)", 1.1614, 1.1814),
             ("Arm A (alt)", 1.1917, 1.2267),
             ("MI merge, Theorem-B quadrature, alpha = 1 (Amendment 2, canonical/primary)", 1.0799, 1.0799),
             ("Arm C: no merge (ownership) -- B's rule", 1.000, 1.000)]
for nm, lo, hi in COMMITTED:
    R.P(f"  committed  {nm:78s}: {lo:.4f}{'' if hi == lo else ' - %.4f' % hi}  -> distance of gamma-hat = 1.000 "
        f"from it: {(lo - 1.0) / SIGMA_TOT_DR4:.1f}{'' if hi == lo else ' - %.1f' % ((hi - 1.0) / SIGMA_TOT_DR4)} sigma_tot")
R.num("M7", dict(point=M7, committed=COMMITTED))
R.P("  reading: every merging-river composition predicts a boost (gamma > 1); only the no-merge rule (Arm C) predicts 1.000.")
R.P("  A Newtonian DR4 kills the MG merge (>= 5.8 sigma_tot) and disfavours the MI merge (2.9 sigma_tot); the point-field")
R.P("  estimates above are the external-dominated limits, not the registered estimator, and are never scored.")

# =============================================================================================== M8 Solar System
R.banner("M8  THE SOLAR SYSTEM INSIDE THE GALAXY'S RIVER (G5)")
GMsun = G_SI * MSUN
M8 = {}
for foot in FOOTS:
    a0 = A0[foot]
    mono = (a0 / 2) / SJ_EARTH
    rM = math.sqrt(GMsun / a0)
    q2s = a0 / rM
    M8[foot] = dict(monopole_over_bound=mono, r_M_AU=rM / 1.495978707e11, a0_over_rM=q2s, scale_over_Q2=q2s / Q2_BOUND)
    R.P(f"  {foot:9s}: P2 alpha = 1 tail a0/2 = {a0 / 2:.3e} m/s^2 = {mono:.0f} x the Earth 2-sigma bound (not merge-specific); "
        f"r_M(Sun) = {rM / 1.495978707e11:.0f} AU; the external-field quadrupole scale a0/r_M = {q2s:.2e} s^-2 = "
        f"{q2s / Q2_BOUND:.1f} x the Q2 ceiling")
R.check("C4 CONTROL: the alpha = 1 monopole liability reproduced (canonical a0/2 over 3.66e-14 = 1278-1279)",
        1278.0 <= M8["canonical"]["monopole_over_bound"] <= 1279.5, f"{M8['canonical']['monopole_over_bound']:.1f}")
R.P("  committed (GATES 4.01, not recomputed): the strict law's external-field quadrupole is 4.0-5.7 x the Q2 ceiling, i.e. the")
R.P("  quadrupole coefficient is ~0.3-0.4 of a0/r_M; ownership (no merge) leaves only the host tide 1.6-2.6e-31 s^-2.")
R.num("M8", M8)

# =============================================================================================== M9 scorecard
R.banner("M9  THE COMMITTED POPULATION SCORECARD (CFG7 H0): merging rivers = 'the law with the external field'")
tot = [l.strip() for l in open(os.path.join(CFG, "CFG7_hierarchy_fg001.out")) if "TOTAL: FG001 passes" in l]
for l in tot:
    R.P("  " + l)
R.check("M9 (reported) CFG7's H0 lines read from the committed .out: ownership 9/14, the external-field (merge) reading 6/14, "
        "both footings", len(tot) == 2 and all("9/14" in l and "rival 6/14" in l for l in tot), "; ".join(tot), load_bearing=False)

R.banner("VERDICT (Q-merge numbers)")
if not MUTATE:
    R.P(f"  Chae: {M5['canonical']['mean']['cls']} (canonical) / {M5['alt']['mean']['cls']} (alt);  Coma: the E7 merge is "
        f"{hc:.1f} / {ha:.1f} sigma (FAIL);  DR4: merge predicts gamma > 1 (Arm A, or MI 1.08), no-merge 1.000;")
    R.P("  Solar System: the merge's quadrupole is the strict law's 4.0-5.7x (G5 FAIL unless screened).  Scorecard 6/14 vs 9/14.")
else:
    R.P("  MUTATE (no external field): the merge rows collapse onto ownership's; the Coma headline flips.")
R.finish()
