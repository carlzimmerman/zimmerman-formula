#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR9_cosmic_shear.py -- THE SMALL-REGION DOOR, part 2 of 3: cosmic shear on MS3/MS4's resolution-free halo model as the
vacuum gate's threshold is raised, with MS5's kappa-form cap and without any cap.  Independent cross-thread review
(2026-09-26, night).  Read-only on every committed file: MS4's machinery (which loads MS3's and L363's) is loaded
unedited; its committed numbers are the control.

THE DOOR (XR9_kids_flagship.py's docstring has the full statement and the pre-declared hypothesis).  Raising x_c0 shrinks
every MOND region, r_e ~ v_f/(H sqrt(x_c,eff)), and MS5's kappa-form cap shrinks with it: every spherical region stops at
l_cap(z) = v_cap/(H(z) sqrt(x_c,eff(z))) (61a3a0858; 1.75 Mpc at z = 0.5 at the converged cell).  Smaller regions carry
less phantom, so cosmic shear should get easier.  This lane verifies it cell by cell.

THE MODEL AS SCORED: MS4's R_smooth (L363's halo model at z = 0.5: Sheth-Tormen + NFW P_NL, GP0's observed bound baryons,
the MOND-sector door variable x = 1.5 Omega_m(z)(f_b rho_host + rho_ph)/rho_bar_m with the ungated phantom, DE7/DE9's
smooth gate at w = 0.25, L388's carrier retention by halo mass at 600 km/s), at x_c = x_c0 E(0.5)^(2p) for p in {1, 1.5},
x_c0 in {2.5, 3.5, 5, 7, 10, 14, 20}:
  capped    MS4's hard cut at l_cap(0.5) = 1.75 Mpc sqrt(x_lin/x_c) -- MS5's kappa form on a spherical halo (MS5 S1 shows
            it reproduces MS3's K1 exactly at 1.75 Mpc; v_cap = 325.3 km/s is MS3's, defined by that radius);
  uncapped  no cap (the region ends where the door's density falls below the threshold).
  kappa-smooth (reported at three cells) the cap inside the smooth gate, U = min(x, x_c (l_cap/r)^2), in place of the hard
            cut: it bounds the difference between the two ways of writing MS5's cap.
Pass = worst R <= 1.2 over k = 0.1-1 h/Mpc on both footings (GP3's gate, MS3/MS4's rule).

CHECKS
  C1 CONTROL: at p = 1, x_c0 = 2.5, w = 0.25 MS4's committed numbers are reproduced exactly (capped 1.75 Mpc:
     1.0491/1.1243; uncapped 2.7191/3.1809; 1e-12).
  S1 [load-bearing; MUTATE must fail] the converged cell passes with the cap on both footings.
  S2 (reported) the worst R per cell, capped and uncapped; SMALLER REGIONS HELP: along each p the capped and the uncapped
     worst R do not rise as x_c0 rises (pre-declared expectation from the task, reported either way).
  S3 (reported) the cells at which even the uncapped model passes (where the cap would no longer be needed).
  S4 (reported) the kappa-smooth variant beside the hard cut at three cells.
  S5 (reported) the smallest R(k) with the cap (the carrier's clearing lowers small-scale power), against a two-sided
     reading 0.8 <= R <= 1.2 shown beside the committed one-sided rule.
MUTATE=1 removes the cap in the gated column: S1 must FAIL (rc = 1).

SCOPE.  MS3/MS4's: isolated regions per halo (the halo model over-counts phantoms in crowded places), one lens epoch,
P(k) not xi_+-, the observed bound baryons, L388's retention (its kick is fixed at 600 km/s here; the carrier does not
depend on the gate).  The gate variable reads the ungated phantom.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR9_cosmic_shear.py   (MUTATE=1)
"""
import os, sys, json, math, time, io, contextlib, warnings
os.environ.setdefault("OMP_NUM_THREADS", "1"); os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1"); os.environ.setdefault("MKL_NUM_THREADS", "1")
import numpy as np
from scipy.special import spherical_jn
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MSDIR = os.path.join(REPO, "real_research", "mond_sector_gate_2026")
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR9_cosmic_shear"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "XR9 part 2 (cosmic shear)", "mutate": MUTATE, "checks": {}, "numbers": {}}
PS = (1.0, 1.5)
XC0S = (2.5, 3.5, 5.0, 7.0, 10.0, 14.0, 20.0)
CELLS = [(p, x0) for p in PS for x0 in XC0S]
W = 0.25
ck = lambda p, x0: f"p{p:g}_x{x0:g}"


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok); CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 118); P(t); P("=" * 118)


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: no cap in the gated column; S1 must FAIL ***")
    p4 = os.path.join(MSDIR, "MS4_smooth_gate_shear.py")
    M4 = {"__name__": "ms4", "__file__": p4}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(p4).read().split('banner("C1  CONTROL: a near-sharp gate')[0]
             .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), M4)
    R_smooth, E2, A0, Wg = M4["R_smooth"], M4["E2"], M4["A0"], M4["Wg"]
    GP0, KC, RHO, PNL, PLIN, h, ZS, aS = (M4[k_] for k_ in ("GP0", "KC", "RHO", "PNL", "PLIN", "h", "ZS", "aS"))
    G, MS, MPC, nu_mono, Omz, I1, nfw_uk = (M4[k_] for k_ in ("G", "MS", "MPC", "nu_mono", "Omz", "I1", "nfw_uk"))
    FB, dn, bh, LMH, dlnM, XLIN, KG = (M4[k_] for k_ in ("FB", "dn", "bh", "LMH", "dlnM", "XLIN", "KG"))
    rho_bar_phys, rho_c_phys, ret_L388 = M4["rho_bar_phys"], M4["rho_c_phys"], M4["ret_L388"]
    MS4R = json.load(open(os.path.join(MSDIR, "MS4_smooth_gate_shear_results.json")))["numbers"]["table"]
    P(f"  MS4/MS3/L363 loaded: z = {ZS}, E(0.5)^2 = {E2:.6f}, x_lin = {XLIN:.6f}   [{time.time() - T0:.0f}s]")
    lcap = lambda xc: 1.75 * math.sqrt(XLIN / xc)                       # MS5's kappa cap at z = 0.5 (Mpc, physical)

    # ------------------------------------------------------------------------------ the kappa-smooth variant (reported)
    def transform_ks(M, Mb, xc, a0, lc, w):
        """MS4's transform_smooth with the cap inside the gate: U = min(x, x_c (l_cap/r)^2) (MS5's form, smooth)."""
        c = 10 ** (0.905 - 0.101 * math.log10(M / (1e12 / h))) * (1 + ZS) ** -0.5
        r200 = (3 * M / (4 * math.pi * 200 * rho_c_phys)) ** (1 / 3); rs = r200 / c; mc = math.log(1 + c) - c / (1 + c)
        r = np.geomspace(1e-3 * r200, 30.0, 4000)
        y = G * Mb * MS / (r * MPC) ** 2 / a0
        Mph = (nu_mono(y) - 1) * Mb
        rho_ph = np.gradient(Mph, r) / (4 * math.pi * r ** 2)
        rho_h = np.where(r < r200, M / (4 * math.pi * rs ** 3 * mc) / ((r / rs) * (1 + r / rs) ** 2), 0.0)
        x = 1.5 * Omz * ((FB * rho_h + np.maximum(rho_ph, 0)) / rho_bar_phys)
        t = (np.minimum(x, xc * (lc / r) ** 2) / xc - 1) / (2 * w) + 0.5
        f = Wg(t)
        off = np.where(t <= 0)[0]
        if off.size: f[off[0]:] = 0.0
        rc = r / aS; kr = np.outer(KC, rc)
        return np.trapz((f * Mph)[None, :] * KC[:, None] * spherical_jn(1, kr), rc, axis=1)

    def R_full(xc, a0, rcap, w, ret=ret_L388, tf=None):
        """MS4's R_smooth line for line, returning R(k) at every gated k (not only its maximum); tf = transform_ks for the
        kappa-smooth variant (then rcap is l_cap)."""
        P1 = np.zeros_like(KC); X1 = np.zeros_like(KC); B = np.zeros_like(KC); rm = np.zeros_like(KC)
        for lm in LMH:
            M = 10 ** lm; n = float(np.interp(lm, GP0.LM, dn)); b = float(np.interp(lm, GP0.LM, bh))
            Mb = float(GP0.M_bound(M, ZS, "observed"))
            tr = (M4["transform_smooth"] if tf is None else tf)(M, Mb, xc, a0, rcap, w); uk = nfw_uk(M, KC)
            P1 += n * tr ** 2 * dlnM / RHO ** 2; B += n * b * tr * dlnM / RHO
            fr = ret(M); mass_1h = (FB + (1 - FB) * fr) * M
            rm += n * ((M * uk) ** 2 - (mass_1h * uk) ** 2) * dlnM / RHO ** 2
            X1 += n * mass_1h * uk * tr * dlnM / RHO ** 2
        R = (PNL - rm + 2 * (X1 + I1 * B * PLIN) + P1 + B ** 2 * PLIN) / PNL
        return {q: float(np.interp(math.log(q * h), np.log(KC), R)) for q in KG}

    # ============================================================================================ C1
    banner("C1  CONTROL: MS4's committed numbers at the converged cell (w = 0.25, x_c0 = 2.5)")
    ref_c = MS4R["0.25/2.5/1.75"]; ref_u = MS4R["0.25/2.5/inf"]
    full_c = {f: R_full(XLIN, A0[f], 1.75, W) for f in A0}
    full_u = {f: R_full(XLIN, A0[f], math.inf, W) for f in A0}
    mine_c = {f: max(full_c[f].values()) for f in A0}; mine_u = {f: max(full_u[f].values()) for f in A0}
    d1 = max(max(abs(mine_c[f] - ref_c[f]), abs(mine_u[f] - ref_u[f])) for f in A0)
    d1b = abs(R_smooth(XLIN, A0["canonical"], 1.75, W) - mine_c["canonical"])
    check("C1 CONTROL: MS4's committed worst R at w = 0.25, x_c0 = 2.5 reproduced exactly -- capped at 1.75 Mpc and uncapped, "
          "both footings (this lane's R(k) is MS4's R_smooth before its maximum is taken)",
          f"capped {mine_c['canonical']:.6f}/{mine_c['alt']:.6f} vs {ref_c['canonical']:.6f}/{ref_c['alt']:.6f}; uncapped "
          f"{mine_u['canonical']:.6f}/{mine_u['alt']:.6f} vs {ref_u['canonical']:.6f}/{ref_u['alt']:.6f} (max |diff| {d1:.1e}; "
          f"against MS4's R_smooth called directly {d1b:.1e})", d1 < 1e-12 and d1b < 1e-12)

    # ============================================================================================ the scan
    banner("THE SCAN: R(k) over k = 0.1-1 h/Mpc, capped (kappa form) and uncapped, both footings (max gated; min reported)")
    TAB = {}
    for (p, x0) in CELLS:
        key = ck(p, x0); xc = x0 * E2 ** p; lc = lcap(xc)
        if (p, x0) == (1.0, 2.5):
            fc_, fu_ = full_c, full_u                                     # the control's own evaluations (same arguments)
        else:
            fc_ = {f: R_full(xc, A0[f], lc, W) for f in A0}
            fu_ = {f: R_full(xc, A0[f], math.inf, W) for f in A0}
        cap_ = {f: max(fc_[f].values()) for f in A0}; unc_ = {f: max(fu_[f].values()) for f in A0}
        capmin = {f: min(fc_[f].values()) for f in A0}; uncmin = {f: min(fu_[f].values()) for f in A0}
        gated = unc_ if MUTATE else cap_
        TAB[key] = dict(p=p, xc0=x0, xc_05=xc, l_cap_05_Mpc=lc, capped=cap_, uncapped=unc_, gated=gated,
                        capped_min=capmin, uncapped_min=uncmin, R_k_capped=fc_, R_k_uncapped=fu_,
                        pass_=all(v_ <= 1.2 for v_ in gated.values()), pass_capped=all(v_ <= 1.2 for v_ in cap_.values()),
                        pass_uncapped=all(v_ <= 1.2 for v_ in unc_.values()),
                        two_sided_capped=all(0.8 <= v_ <= 1.2 for f in A0 for v_ in fc_[f].values()))
        P(f"  {key:9s} x_c(0.5) {xc:6.2f}  l_cap {lc:4.2f} Mpc: capped max {cap_['canonical']:.3f}/{cap_['alt']:.3f} (min "
          f"{capmin['canonical']:.3f}/{capmin['alt']:.3f}) {'ok' if TAB[key]['pass_capped'] else 'FAIL'};  uncapped max "
          f"{unc_['canonical']:.3f}/{unc_['alt']:.3f} (min {uncmin['canonical']:.3f}/{uncmin['alt']:.3f}) "
          f"{'ok' if TAB[key]['pass_uncapped'] else 'FAIL'}   [{time.time() - T0:.0f}s]")
    OUT["numbers"]["table"] = TAB

    banner("S1-S5")
    c0 = TAB["p1_x2.5"]["gated"]
    check("S1 THE CONVERGED CELL PASSES WITH THE CAP: worst R <= 1.2 on both footings at p = 1, x_c0 = 2.5 (the gated column) -- "
          "MUTATE (no cap) must fail this", f"{c0['canonical']:.3f}/{c0['alt']:.3f}", all(v_ <= 1.2 for v_ in c0.values()))
    mono = {}
    for p in PS:
        for lab in ("capped", "uncapped"):
            seq = [max(TAB[ck(p, x0)][lab].values()) for x0 in XC0S]
            mono[f"p{p:g}/{lab}"] = all(b_ <= a_ + 1e-6 for a_, b_ in zip(seq, seq[1:]))
    check("S2 (reported, pre-declared expectation) SMALLER REGIONS HELP: along each p the worst R (worse footing), capped and "
          "uncapped, does not rise as x_c0 rises", "; ".join(f"{k_}: {'monotone' if v_ else 'NOT monotone'}" for k_, v_ in mono.items())
          + "; capped worst by cell: " + ", ".join(f"{k_} {max(v_['capped'].values()):.3f}" for k_, v_ in TAB.items()),
          all(mono.values()), load_bearing=False)
    unc_pass = [k_ for k_, v_ in TAB.items() if v_["pass_uncapped"]]
    check("S3 (reported) the cells where even the UNCAPPED model passes cosmic shear (the cap no longer needed for shear)",
          f"{unc_pass or 'none'}; uncapped worst by cell: " + ", ".join(f"{k_} {max(v_['uncapped'].values()):.2f}" for k_, v_ in TAB.items()),
          True, load_bearing=False)
    KS = {}
    for (p, x0) in ((1.0, 2.5), (1.0, 7.0), (1.0, 20.0)):
        xc = x0 * E2 ** p
        KS[ck(p, x0)] = {f: max(R_full(xc, A0[f], lcap(xc), W, tf=transform_ks).values()) for f in A0}
    check("S4 (reported) MS5's cap written inside the smooth gate (U = min(x, x_c (l_cap/r)^2)) against MS4's hard cut at l_cap",
          "; ".join(f"{k_}: smooth {v_['canonical']:.3f}/{v_['alt']:.3f} vs hard {TAB[k_]['capped']['canonical']:.3f}/"
                    f"{TAB[k_]['capped']['alt']:.3f}" for k_, v_ in KS.items()), True, load_bearing=False)
    OUT["numbers"]["kappa_smooth"] = KS
    low = {k_: min(v_["capped_min"].values()) for k_, v_ in TAB.items()}
    check("S5 (reported) THE OTHER SIDE: the smallest R(k) over k = 0.1-1 h/Mpc with the cap (the kicked carrier removes "
          "small-scale power; the gate's rule is one-sided, R <= 1.2, and a two-sided reading 0.8 <= R <= 1.2 is shown beside it)",
          ", ".join(f"{k_} {v_:.3f}" for k_, v_ in low.items()) + f"; two-sided band held at "
          f"{sum(v_['two_sided_capped'] for v_ in TAB.values())}/{len(TAB)} cells", True, load_bearing=False)

    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
      f"[{time.time() - T0:.0f}s]")
    sys.exit(1 if nlb else 0)
