#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR4_efe_under_region_kernel.py -- the two 09-03 external-field (EFE) liabilities re-scored under L361's bound-region
kernel.  Independent cross-thread review, 2026-09-26.  Read-only on every committed file: it IMPORTS the loaders and
prediction functions of hunt_2026/k_contrarian_clusterbtfr.py and hunt_2026/k_contrarian_dwarfefe.py (their main()
is never called) and changes ONE thing, the external field the kernel reads.

WHAT L361 SAYS THE EFE IS (real_research/g03_audit_2026/L361_bound_region_kernel.py, lines 16-32).
    (lap - M^2) w = 4 pi G f rho_b,  M^2 = m^2 (1 - f);   (lap - M^2) P = div[f (nu(|grad w|/a0) - 1) grad w] + M^2 w;
    in-region baryons move in phi + f P.
  * Inside a bound region (f = 1, M = 0) w is the Newtonian potential of ALL in-region baryons, so nu's argument is
    |g_N,int + g_N,ext(in-region baryons)|: the ordinary QUMOND external-field effect, sourced by BARYONS only (the
    carrier and the web gas never enter w).
  * Fields from OUTSIDE the region are screened (L361 R1: 9.5e-5 transmitted through a 2 Mpc gap at 1/m = 0.2 Mpc).
  * Region edge (DE1 closed form, L352 Z6): r_e = v_f/(H0 sqrt(x_c0 + 1.5 Omega_m)), v_f = (G M_b a0)^(1/4):
    ~2 Mpc for the Local Group, ~8-10 Mpc for a PSZ2 cluster.  Both samples' galaxies sit INSIDE their host's region.
  So the construction predicts the SAME mechanism as standard QUMOND for both samples.  The only change is the
  AMPLITUDE of the external field: the host's BARYONIC Newtonian field.
    (i)  cluster infall (k_contrarian_clusterbtfr): the committed prediction fed nu the Newtonian-EQUIVALENT of the
         cluster's TRUE (SZ-mass NFW) field, e_N = nu^-1(g_true) ~ g_true^2/a0.  Under L361 it is
         e_N = G M_b,cl(<r)/r^2 = f_b(r) g_true, which is linear, not quadratic, in g_true.  This can change the slope.
    (ii) Local Volume dwarfs (k_contrarian_dwarfefe): the committed prediction ALREADY used the hosts' baryonic
         Newtonian field (MW 6e10, M31 1.2e11 Msun).  Under L361 the only differences are in-region hot gas (CGM) in the
         hosts, which raises e_N, and field dwarfs beyond the Local Group's region edge, which lose it.

CHECKS (PASS/FAIL; controls first; both footings everywhere)
  C1  CONTROL: the committed cluster numbers are reproduced (observed +0.0033 +- 0.0304; framework -0.1348 / -0.1290).
  C2  CONTROL: the committed dwarf numbers are reproduced (statistic C: observed +0.0800 +- 0.0467; framework -0.1006 /
      -0.1026).
  M1  MUTATION: kernel off (nu = 1) under the L361 prescription -> predicted cluster slope = 0 (SEP restored).
  E1  (reported) the construction's cluster e_N against the committed one: median ratio and d log e_N / d log g_e.
  E2  THE CLUSTER RE-SCORE: predicted slope and sigma from the observed, f_b(R500) in {0.10, 0.13, 0.157}; scalar-sum
      (the committed form) and the QUMOND 1-D subtract form; plus the zero-point version (members - field).
      Pre-declared reading: the liability is "materially weakened" only if every variant is < 3 sigma from the data.
  E3  THE DWARF RE-SCORE: host CGM x{1, 1.5, 2}; field dwarfs beyond the LG edge screened (e_N = 0).
      Pre-declared reading: the liability stands if every variant stays >= 3 sigma.
Runtime ~20-60 s.  Writes XR4_efe_under_region_kernel_results.json next to this file.
Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR4_efe_under_region_kernel.py
"""
import os, sys, json, math, time, io, contextlib
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "hunt_2026"))
T0 = time.time()
P = lambda *a: print(*a, flush=True)
OUT = {"lane": "XR4_efe_under_region_kernel", "checks": {}, "numbers": {}}
CH = []


def check(name, ok, measured):
    ok = bool(ok); CH.append((name, ok)); OUT["checks"][name] = {"ok": ok, "measured": str(measured)}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}\n         measured: {measured}")


import k_contrarian_clusterbtfr as KC          # noqa: E402  (committed 09-03, d4343a4b3; main() NOT called)
import k_contrarian_dwarfefe as KD             # noqa: E402
from hunt_lib import A0, OM_M                  # noqa: E402

G, MSUN, MPC = KC.G, KC.MSUN, KC.MPC
FCOS = 0.157                                   # Omega_b/Omega_m


def edge_Mpc(Mb_msun, a0, xc0=2.5):
    """L361/DE1 region edge at z = 0: r_e = v_f/(H0 sqrt(x_c0 + 1.5 Om))."""
    vf = (G * Mb_msun * MSUN * a0) ** 0.25
    H0 = 67.4e3 / MPC
    return vf / (H0 * math.sqrt(xc0 + 1.5 * OM_M)) / MPC


# =============================================================================================== PART A: clusters
P("=" * 112); P("PART A -- cluster-infall BTFR slope (k_contrarian_clusterbtfr), external field read the L361 way"); P("=" * 112)
gal = KC.build(1.0); cls = KC.clusters()
idx, xr500, Rp = KC.assign(gal, cls)
memb = idx >= 0
V = np.array([x["V"] for x in gal]); Mb = np.array([x["Mb"] for x in gal]) * MSUN
lHIall = np.array([x["lMHI"] for x in gal]); RHI = KC.rhi_wang(lHIall); gN = G * Mb / RHI ** 2
ge = np.zeros(len(gal)); r_m = np.zeros(len(gal)); x_m = np.zeros(len(gal)); Mcl_b = np.zeros(len(gal))
for i in np.where(memb)[0]:
    c = cls[idx[i]]
    r = max(Rp[i], 0.05 * c["r500"]); r_m[i] = r; x_m[i] = r / c["r500"]
    ge[i] = G * KC.nfw_menc(r, c["M500"], c["r500"]) * MSUN / r ** 2          # the committed TRUE field
    Mcl_b[i] = FCOS * KC.nfw_menc(2.0 * c["r500"], c["M500"], c["r500"])     # cluster baryons for the edge law
P(f"  members N = {memb.sum()} (committed 314)")


def fb_profile(x, f500):
    """baryon fraction inside r = x R500: f500 inside R500, rising (log-linear) to cosmic at 2 R500."""
    t = np.clip(np.log(np.maximum(x, 1e-9)) / math.log(2.0), 0.0, 1.0)
    return f500 + (FCOS - f500) * t


def regress(D, m, lge):
    A = np.column_stack([np.ones(m.sum()), np.log10(Mb[m] / MSUN), lHIall[m], lge])
    return np.linalg.lstsq(A, D[m], rcond=None)[0][-1], A


def boot_err(D, m, lge, nb=3000, seed=3):
    s, A = regress(D, m, lge); rng = np.random.default_rng(seed); n = m.sum(); bs = np.empty(nb)
    for k in range(nb):
        kk = rng.integers(0, n, n); bs[k] = np.linalg.lstsq(A[kk], D[m][kk], rcond=None)[0][-1]
    return s, bs.std()


def zero_point(Dobs, Dpre, lMb_all):
    keep = np.isfinite(Dobs) & np.isfinite(lHIall) & np.isfinite(lMb_all)
    lo, hi = np.percentile(lMb_all[memb], 2), np.percentile(lMb_all[memb], 98)
    use = keep & (lMb_all > lo) & (lMb_all < hi); ind = memb.astype(float)
    Aj = np.column_stack([np.ones(use.sum()), lMb_all[use], lHIall[use], ind[use]])
    co = np.linalg.lstsq(Aj, Dobs[use], rcond=None)[0][-1]; cp = np.linalg.lstsq(Aj, Dpre[use], rcond=None)[0][-1]
    rng = np.random.default_rng(23); nn = use.sum(); bj = np.empty(1500)
    for k in range(1500):
        kk = rng.integers(0, nn, nn); bj[k] = np.linalg.lstsq(Aj[kk], Dobs[use][kk], rcond=None)[0][-1]
    return co, cp, bj.std()


lMb_all = np.log10(Mb / MSUN)
resA = {}
for foot, a0 in A0.items():
    Dobs = np.log10(V * 1e3) - 0.25 * np.log10(G * Mb * a0)
    lge = np.log10(ge[memb] / a0)
    sobs, eobs = boot_err(Dobs, memb, lge)
    # committed prescription (control)
    geN_c = np.zeros(len(gal)); geN_c[memb] = a0 * KC.newtonian_equivalent(ge[memb] / a0)
    Dpre_c = np.log10(np.sqrt(KC.nu((gN + geN_c) / a0) * G * Mb / RHI)) - 0.25 * np.log10(G * Mb * a0)
    spre_c, _ = regress(Dpre_c, memb, lge)
    row = dict(obs=sobs, err=eobs, committed=spre_c, variants={})
    P(f"\n  ---- {foot} footing, a0 = {a0:.3e} ----")
    P(f"  observed slope {sobs:+.4f} +/- {eobs:.4f};  committed framework {spre_c:+.4f}  ({abs(sobs - spre_c) / eobs:.2f} sigma)")
    for f500 in (0.10, 0.13, FCOS):
        eN = np.zeros(len(gal))
        eN[memb] = fb_profile(x_m[memb], f500) * ge[memb]                   # L361: baryonic Newtonian field
        # region edge: members beyond their cluster's edge are screened (e_N = 0)
        re = np.array([edge_Mpc(Mcl_b[i], a0) for i in np.where(memb)[0]]) * MPC     # Mcl_b is already in Msun
        outside = r_m[memb] > re; eN_m = eN[memb].copy(); eN_m[outside] = 0.0; eN[memb] = eN_m
        rat = eN[memb] / geN_c[memb]
        dl = np.polyfit(np.log10(ge[memb]), np.log10(np.maximum(eN[memb], 1e-300)), 1)[0]
        dl_c = np.polyfit(np.log10(ge[memb]), np.log10(geN_c[memb]), 1)[0]
        # scalar-sum form (the committed form)
        Dp = np.log10(np.sqrt(KC.nu((gN + eN) / a0) * G * Mb / RHI)) - 0.25 * np.log10(G * Mb * a0)
        sp, _ = regress(Dp, memb, lge)
        # QUMOND 1-D subtract form: g_int = nu(|gN + eN|) (gN + eN) - nu(eN) eN  (Famaey & McGaugh 2012 sec. 6.3 form)
        gi = KC.nu((gN + eN) / a0) * (gN + eN) - np.where(eN > 0, KC.nu(np.maximum(eN, 1e-30) / a0) * eN, 0.0)
        Dq = np.log10(np.sqrt(np.maximum(gi, 1e-30) * RHI)) - 0.25 * np.log10(G * Mb * a0)
        sq, _ = regress(Dq, memb, lge)
        # the committed prescription in the subtract form, for a like-for-like comparison
        gic = KC.nu((gN + geN_c) / a0) * (gN + geN_c) - np.where(geN_c > 0, KC.nu(np.maximum(geN_c, 1e-30) / a0) * geN_c, 0.0)
        sqc, _ = regress(np.log10(np.sqrt(np.maximum(gic, 1e-30) * RHI)) - 0.25 * np.log10(G * Mb * a0), memb, lge)
        co, cp, sej = zero_point(Dobs, Dp, lMb_all)
        v = dict(f500=f500, median_ratio_eN=float(np.median(rat)), dlogeN_dlogge=float(dl), dlogeN_dlogge_committed=float(dl_c),
                 frac_outside_edge=float(np.mean(outside)), slope_scalar=float(sp), sigma_scalar=float(abs(sobs - sp) / eobs),
                 slope_subtract=float(sq), sigma_subtract=float(abs(sobs - sq) / eobs), committed_subtract=float(sqc),
                 sigma_committed_subtract=float(abs(sobs - sqc) / eobs),
                 zp_obs=float(co), zp_pred=float(cp), zp_err=float(sej), zp_sigma=float(abs(co - cp) / sej))
        row["variants"][str(f500)] = v
        P(f"   f_b(R500) = {f500:.3f}: median e_N(L361)/e_N(committed) = {v['median_ratio_eN']:.2f}; "
          f"d log e_N/d log g_e = {dl:.2f} (committed {dl_c:.2f}); beyond edge {100 * v['frac_outside_edge']:.1f}%")
        P(f"       slope scalar-sum {sp:+.4f} ({v['sigma_scalar']:.2f} sigma) | subtract form {sq:+.4f} "
          f"({v['sigma_subtract']:.2f} sigma; committed prescription in that form {sqc:+.4f}, {v['sigma_committed_subtract']:.2f} sigma)")
        P(f"       zero point members - field: observed {co:+.4f} +/- {sej:.4f}, predicted {cp:+.4f} -> {v['zp_sigma']:.2f} sigma")
    # mutation: kernel off under the L361 prescription
    eN = np.zeros(len(gal)); eN[memb] = fb_profile(x_m[memb], 0.13) * ge[memb]
    Dm = np.log10(np.sqrt(np.ones_like(gN) * G * Mb / RHI)) - 0.25 * np.log10(G * Mb * a0)
    sm, _ = regress(Dm, memb, lge)
    row["mutation_nu1"] = float(sm)
    resA[foot] = row
OUT["numbers"]["clusters"] = resA

check("C1 CONTROL: the committed cluster-infall numbers reproduce (observed +0.0033 +- 0.0304; framework -0.1348 canonical / "
      "-0.1290 alt)",
      abs(resA["canonical"]["obs"] - 0.0033) < 5e-4 and abs(resA["canonical"]["err"] - 0.0304) < 2e-3
      and abs(resA["canonical"]["committed"] + 0.1348) < 5e-4 and abs(resA["alt"]["committed"] + 0.1290) < 5e-4,
      f"obs {resA['canonical']['obs']:+.4f} +/- {resA['canonical']['err']:.4f}; framework {resA['canonical']['committed']:+.4f} / "
      f"{resA['alt']['committed']:+.4f}")
check("M1 MUTATION: kernel off (nu = 1) under the L361 prescription gives a predicted slope of zero",
      all(abs(resA[f]["mutation_nu1"]) < 1e-9 for f in resA), {f: resA[f]["mutation_nu1"] for f in resA})
# guard against the first run's bug (cluster mass divided by Msun twice -> every member 'beyond the edge', e_N = 0):
# the members lie at <= 5 R500 projected and a PSZ2 cluster's edge is several Mpc, so almost none may be screened
fo = max(v["frac_outside_edge"] for f in resA for v in resA[f]["variants"].values())
check("G1 SANITY: the region edge screens (almost) no cluster member -- the members sit well inside their clusters' regions",
      fo < 0.05, f"largest fraction of members beyond the edge: {fo:.3f}")
allsig = [v[k] for f in resA for v in resA[f]["variants"].values() for k in ("sigma_scalar", "sigma_subtract")]
check("E2 THE CLUSTER RE-SCORE (pre-declared): the liability is 'materially weakened' only if EVERY L361 variant is < 3 sigma "
      "from the observed slope",
      max(allsig) < 3.0, f"sigma range over f_b x form x footing: {min(allsig):.2f} - {max(allsig):.2f}")

# =============================================================================================== PART B: dwarfs
P("\n" + "=" * 112); P("PART B -- Local Volume dwarf slope (k_contrarian_dwarfefe), external field read the L361 way"); P("=" * 112)
d = KD.load(ups_v=2.0)
lsig = np.log10(np.array([g["sig"] for g in d])); lM = np.log10(np.array([g["Mb"] for g in d]))
lrh = np.log10(np.array([g["rh"] / KD.PC for g in d])); grp = np.array([g["grp"] for g in d])
dmw = np.array([g["dmw"] for g in d]); dm31 = np.array([g["dm31"] for g in d])
gNe0 = np.array([g["gNe"] for g in d])        # committed: the larger of the two hosts' baryonic Newtonian fields
resB = {}
for foot, a0 in A0.items():
    lge = np.log10(KD.true_external_field(gNe0, a0) / a0)               # the committed regressor, held FIXED
    q = [lM, lrh, lM * lM, lrh * lrh, lM * lrh, lge]
    cobs, _ = KD.partial_slope(lsig, q); eobs = KD.boot_slope(lsig, q)
    row = dict(obs=float(cobs), err=float(eobs), variants={})

    def pred_slope(gNe_new):
        dd = [dict(g, gNe=gg) for g, gg in zip(d, gNe_new)]
        return KD.partial_slope(np.log10(KD.predict_sigma(dd, a0)), q)[0]

    row["committed"] = float(pred_slope(gNe0))
    for cgm in (1.0, 1.5, 2.0):
        for screen_mpc in (None, 1.2):
            g_new = gNe0 * cgm
            if screen_mpc is not None:
                far = np.fmin(np.where(np.isfinite(dmw), dmw, np.inf), np.where(np.isfinite(dm31), dm31, np.inf)) > 1e3 * screen_mpc
                g_new = np.where(far, 1e-30, g_new)
            sp = pred_slope(g_new)
            key = f"cgm{cgm}_screen{screen_mpc}"
            row["variants"][key] = dict(slope=float(sp), sigma=float(abs(cobs - sp) / eobs))
            P(f"  {foot:9s} host baryons x{cgm:.1f}, field dwarfs beyond {screen_mpc} Mpc screened: predicted {sp:+.4f} "
              f"(observed {cobs:+.4f} +/- {eobs:.4f}) -> {abs(cobs - sp) / eobs:.2f} sigma")
    resB[foot] = row
nfar = int(np.sum(np.fmin(np.where(np.isfinite(dmw), dmw, np.inf), np.where(np.isfinite(dm31), dm31, np.inf)) > 1.2e3))
OUT["numbers"]["dwarfs"] = resB; OUT["numbers"]["dwarfs_screened_count"] = nfar
check("C2 CONTROL: the committed dwarf numbers reproduce (statistic C: observed +0.0800 +- 0.0467; framework -0.1006 / -0.1026)",
      abs(resB["canonical"]["obs"] - 0.0800) < 5e-4 and abs(resB["canonical"]["err"] - 0.0467) < 2e-3
      and abs(resB["canonical"]["committed"] + 0.1006) < 5e-4 and abs(resB["alt"]["committed"] + 0.1026) < 5e-4,
      f"obs {resB['canonical']['obs']:+.4f} +/- {resB['canonical']['err']:.4f}; framework {resB['canonical']['committed']:+.4f} / "
      f"{resB['alt']['committed']:+.4f}; {nfar} dwarfs lie > 1.2 Mpc from both hosts")
sigB = [v["sigma"] for f in resB for v in resB[f]["variants"].values()]
check("E3 THE DWARF RE-SCORE (pre-declared): the liability STANDS if every L361 variant stays >= 3 sigma from the data",
      min(sigB) >= 3.0, f"sigma range {min(sigB):.2f} - {max(sigB):.2f}")

nf = sum(1 for _, ok in CH if not ok)
OUT["n_checks"], OUT["n_fail"] = len(CH), nf
json.dump(OUT, open(os.path.join(HERE, "XR4_efe_under_region_kernel_results.json"), "w"), indent=1, default=float)
P(f"\n  {len(CH) - nf}/{len(CH)} checks pass  [{time.time() - T0:.0f}s]")
