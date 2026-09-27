#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
DE10 -- KiDS-1000 FOR THE MODEL THE THREADS HAVE CONVERGED ON: the carrier-blind MOND-sector switch, the linear gate,
MS3's cap, and the triggered carrier resolved around each lens.

WHY.  Every KiDS pass on the record scores a different model: L390 and L392 put the switch on the curvature branch,
and DE9 is switch-only with no carrier.  MS1/MS2 moved the switch to the MOND sector's own density, lap(Phi - v) =
baryons + their phantom.  That reading is leak-free when the gate is varied, and it never reads the carrier.  MS3 added
a region cap for cosmic shear (v_cap = 325 km/s), and MS4 found the smooth gate keeps that shear pass at w = 0.25.
DE9 put the common cell at w <~ 0.25 for p = 1, x_c0 = 2.5.  Nobody has scored this model's KiDS gate.  This lane does.

THE MODEL (each piece loaded from its committed source, unedited):
  the switch: DE8's region operator (L361/CV1: screened w, gated phantom P with sigma M^2 w, lensing on
    Phi = u + f P including f' P), sigma = 1, 1/m = 0.1 Mpc, on the MOND-sector reading
    x = 4 pi G (rho_b + rho_ph - f_b rho_bar_m)/H^2 (MS2's door, carrier-blind), p = 1, x_c0 = 2.5 at z_l = 0.25, with
    the transition width w = 0.02 (hard) and w = 0.25;
  MS3's cap, in its local form: the threshold is scaled by max(1, v_loc^2/v_cap^2), v_loc^2 = |grad Phi|^2/lap Phi of the
    MOND-sector potential, v_cap = 325 km/s (it should not bind for KiDS lenses, v_f <= 247 km/s);
  the carrier: L375's shell-model halo(), imported unchanged, re-run exactly as L390 ran it at the linear gate (L390's
    refitted baryonic masses, alpha = 0.75, gamma = 10, N = 60000, L390's seeds) at kicks 600 and 650 km/s (L388's
    window).  Its projected profile enters the lens at amplitude 1 through L375's template(), exactly as in L390.
    The gate does not read it.
  the fit: L352's KiDS machinery through DE8 (M_b profiled per bin, a free linear 2-halo term, full covariance);
    Delta chi^2 against L352's unswitched model; pass = <= +4 on both footings (L352/L360/L390's criterion).

CHECKS
  C1 CONTROL: with L360's switch (curvature branch, L352's compensated hard edge at x_c,eff(0.25) = 3.2477), the re-run
     carrier templates reproduce L390's committed KiDS scores at 600 and 650 km/s exactly (1e-6): same halos, same
     templates.  (Not load-bearing under MUTATE, whose carrier is not kicked.)
  C2 (reported) the contrast: the resolved carrier moves the curvature reading's gate, and it is not an input of the
     MOND-sector gate.
  S1 (reported) the cap's largest threshold scaling on each lens's transition (1 means it does not bind).
  H1 [pre-declared hypothesis, load-bearing] the converged model passes KiDS: Delta chi^2 <= +4 on both footings, at
     both widths and both kicks.
  V1 (reported) every score, beside L390's curvature-branch scores, and the carrier amplitude KiDS prefers (0-1.2).
MUTATE=1: v_k = 0 in every carrier run (the trigger fires, nothing is kicked out, as L390's MUTATE): the retained carrier
is CDM-like and H1 must FAIL (rc = 1).

SCOPE.  Spherical, isolated lenses; one accretion history (L375's fiducial); the carrier's profile from the shell model;
the upper-branch phantom read ungated (on-branch convention); the heat filter omitted.  The cap is MS3's design target
in its local form, with no action yet.

Run from the repository root:  python3 real_research/dark_energy_2026/DE10_kids_converged_model.py
"""
import os, sys, json, math, time, io, contextlib, warnings
import numpy as np
from multiprocessing import Pool
warnings.filterwarnings("ignore")

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DS = os.path.join(REPO, "real_research", "dark_sector_2026")
sys.path.insert(0, DS)
from L375_triggered_carrier_galaxy_retention import halo, M200_BINS   # noqa: E402  (L375's shell model, unchanged)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "DE10_kids_converged_model"
T0 = time.time()
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "DE10", "mutate": MUTATE, "checks": {}, "numbers": {}}
VK = (600.0, 650.0)
WS = (0.02, 0.25)
V_CAP = 325e3                                                         # m/s (MS3)
EXPECT_PASS = True                                                    # H1, set before the run


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name.split()[0]] = {"pass": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading: P(f"         reading:  {reading}")
    return ok


def banner(t): P("\n" + "=" * 110); P(t); P("=" * 110)


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE: P("\n  *** MUTATE=1: v_k = 0 in every carrier run; H1 must FAIL ***")

    # ------------------------------------------------------------------------------ L360's switch (for C1), unedited
    P60 = os.path.join(REPO, "real_research", "g03_audit_2026", "L360_assembled_construction_kids.py")
    N60 = {"__name__": "l360", "__file__": P60}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(P60).read().split("BASE = {")[0], N60)
    fit_comb, fit_model, A052, XE59 = N60["fit_comb"], N60["fit_model"], N60["A0"], N60["XE59"]
    XE_LIN = round(XE59[(1.0, 2.5)], 4)
    # ------------------------------------------------------------------------------ DE8's operator and fit, unedited
    P8 = os.path.join(HERE, "DE8_kids_sigma_axis_both_branches.py")
    D8 = {"__name__": "de8", "__file__": P8}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(open(P8).read().split("# ============================================================================================ C1 C2 C3 controls")[0]
             .replace('MUTATE = os.environ.get("MUTATE", "0") == "1"', "MUTATE = False"), D8)
    (solve_region, esd_from_mlens, Wg, rr, rf, nu_vec, G, MS, A0, KPC_, N, Ed, Sd, Ci, twoh_cache, LM, project_M2,
     annulus_esd, Rp, Rd, MPCm) = [D8[k] for k in ("solve_region", "esd_from_mlens", "Wg", "rr", "rf", "nu_vec", "G", "MS",
                                                   "A0", "KPC_", "N", "Ed", "Sd", "Ci", "twoh_cache", "LM", "project_M2",
                                                   "annulus_esd", "Rp", "Rd", "MPCm")]
    BASE = D8["BASE"]; FB = D8["FB"]; rho_bar = D8["rho_bar"]; H_L = D8["H_L"]
    XCE = 2.5 * (0.3138 * 1.25 ** 3 + 0.6862)                           # x_c,eff(0.25) at p = 1, x_c0 = 2.5 (L359's background)
    P(f"  L360 and DE8 loaded; x_c,eff(0.25) = {XCE:.4f} (L359's K1 entry {XE_LIN})   [{time.time() - T0:.0f}s]")

    # ------------------------------------------------------------------------------ the carrier halos (L390's runs)
    R90 = json.load(open(os.path.join(DS, "L390_kids_resolved_linear_gate_results.json")))["numbers"]
    MB = R90["M_b"]["p=1, x_c0=2.5"]
    NPART = int(os.environ.get("DE10_N", "60000"))
    cfgs = [(f"b{b}_v{int(v)}", b, MB[b], 0.0 if MUTATE else v, 10.0, 0.75, True, NPART, 1200 + 10 * b + int(v) // 25)
            for b in range(4) for v in VK]
    with Pool(int(os.environ.get("DE10_POOL", "4"))) as pool:
        res = dict(pool.map(halo, cfgs, chunksize=1))
    P(f"  {len(cfgs)} carrier halos done (L390's masses {[f'{x:.2e}' for x in MB]}, seeds, N = {NPART})   [{time.time() - T0:.0f}s]")

    def carrier_rho_si(d):                                            # L375's template(), its density step
        e = d["edges"]; rm = np.sqrt(e[1:] * e[:-1]); vol = 4 / 3 * math.pi * (e[1:] ** 3 - e[:-1] ** 3)
        rho = d["hist"] * d["m"] / vol
        return np.interp(np.log(rr / MPCm * 1e3), np.log(rm), rho, left=rho[0], right=0.0) * MS / (MPCm / 1e3) ** 3

    TC, RHOC = {}, {}
    for v in VK:
        for b in range(4):
            rc = carrier_rho_si(res[f"b{b}_v{int(v)}"])
            RHOC[(v, b)] = rc
            M2 = project_M2(rc)
            TC[(v, b)] = annulus_esd(lambda R, M2=M2: np.interp(np.log(R), np.log(Rp), M2), Rd[b])

    # ============================================================================================ C1 control
    banner("C1  CONTROL: L360's curvature switch + the re-run carrier reproduces L390's committed scores")
    c1 = {}
    for v in VK:
        k = {f_: float(fit_comb(A052[f_], XE_LIN, [TC[(v, b)] for b in range(4)], [1.0])[0] - BASE[f_]) for f_ in ("canonical", "alt")}
        c1[v] = k
    ref = {v: R90["table"][f"v{int(v)}"]["kids"] for v in VK}
    d1 = max(abs(c1[v][f_] - ref[v][f_]) for v in VK for f_ in ("canonical", "alt"))
    check("C1 CONTROL: the re-run carrier halos + L360's switch reproduce L390's committed KiDS scores at 600 and 650 km/s",
          f"{ {v: {f_: round(x, 3) for f_, x in c1[v].items()} for v in VK} } vs L390 "
          f"{ {v: {f_: round(x, 3) for f_, x in ref[v].items()} for v in VK} } (max |diff| {d1:.1e})",
          d1 < 1e-6, "same shell-model halos, same template, same fit: the carrier is L390's (not applicable under MUTATE, "
          "whose carrier is not kicked)", load_bearing=not MUTATE)

    # ============================================================================================ the converged model
    def gate_mond(Mb, a0, w, cap=True):
        """MS2's MOND-sector door (baryons + phantom, carrier-blind), MS3's local cap, smooth width w, region connected."""
        Mdyn = Mb * nu_vec(G * Mb / rr ** 2 / a0)
        rho = np.gradient(Mdyn, rr) / (4 * math.pi * rr ** 2)             # the point-mass lens: its phantom
        x = 4 * math.pi * G * (rho - FB * rho_bar) / H_L ** 2
        g = G * Mdyn / rr ** 2
        vloc2 = g ** 2 / np.maximum(4 * math.pi * G * rho, 1e-300)       # |grad Phi|^2 / lap Phi
        scale = np.maximum(1.0, vloc2 / V_CAP ** 2) if cap else np.ones_like(rr)
        t = (x / (XCE * scale) - 1) / (2 * w) + 0.5
        f = Wg(t)
        off = np.where(t <= 0)[0]
        if off.size: f[off[0]:] = 0.0
        return f, scale

    _ESD = {}

    def model(b, lm, foot, w):
        key = (b, round(lm, 3), foot, w)
        if key not in _ESD:
            Mb = 10 ** lm * MS; a0 = A0[foot]
            f, _ = gate_mond(Mb, a0, w)
            extra = solve_region(Mb, a0, f, 100 * KPC_, 1.0)
            _ESD[key] = esd_from_mlens(Mb, extra, b)
        return _ESD[key]

    def fit(foot, w, v, fs=1.0):
        mods = []
        for b in range(4):
            best = None
            for lm in LM:
                mk0 = model(b, lm, foot, w) + fs * TC[(v, b)]
                t2 = twoh_cache[b]; wt = 1 / Sd[b] ** 2
                A = float(np.clip(np.sum(wt * t2 * (Ed[b] - mk0)) / np.sum(wt * t2 * t2), 0.0, 20.0)); mk = mk0 + A * t2
                c_ = float(np.sum(((Ed[b] - mk) / Sd[b]) ** 2))
                if best is None or c_ < best[0]: best = (c_, mk)
            mods.append(best[1])
        dv = np.concatenate(Ed) - np.concatenate(mods)
        return float(dv @ Ci @ dv) - BASE[foot]

    banner("C2 S1  THE GATE IS CARRIER-BLIND; THE CAP ON KiDS LENSES")
    # C2: the carrier moves the CURVATURE reading's gate (it is part of the density that reading sees) but it is not an
    # input of the MOND-sector gate at all -- the contrast the doors turn on (MS1)
    Mb_t = 10 ** 10.8 * MS
    f_curv_car = D8["gate_f"]("upper", Mb_t, A0["canonical"], XCE, 0.25, RHOC[(VK[0], 2)])
    f_curv_0 = D8["gate_f"]("upper", Mb_t, A0["canonical"], XCE, 0.25, np.zeros(N))
    dcurv = float(np.max(np.abs(f_curv_car - f_curv_0)))
    check("C2 (reported) the resolved carrier moves the curvature reading's gate (max |df| > 0 around bin 3) and is not an "
          "input of the MOND-sector gate", f"curvature reading: max |df| = {dcurv:.3f}; MOND-sector: carrier-blind by "
          "construction", True, load_bearing=False)
    S1 = {}
    for b in range(4):
        for lm in (10.4, 10.8, 11.2):
            f, sc = gate_mond(10 ** lm * MS, A0["canonical"], 0.25)
            trans = (f > 1e-6) & (f < 1 - 1e-6)
            S1[f"{b}/{lm}"] = float(sc[trans].max()) if trans.any() else 1.0
    check("S1 (reported) MS3's local cap on KiDS lenses: the largest threshold scaling on any transition",
          f"max {max(S1.values()):.4f}", True, "1 means the cap does not bind (v_loc = v_f <= 247 km/s < 325)", load_bearing=False)
    OUT["numbers"]["cap_scaling"] = S1

    banner("H1 V1  KiDS FOR THE CONVERGED MODEL")
    TAB = {}
    for v in VK:
        for w in WS:
            k = {f_: fit(f_, w, v) for f_ in ("canonical", "alt")}
            fsg = {}
            for f_ in ("canonical", "alt"):
                sc = [(fs_, fit(f_, w, v, fs_)) for fs_ in np.linspace(0.0, 1.2, 13)]
                fsg[f_] = min(sc, key=lambda t_: t_[1])
            TAB[f"v{int(v)}/w{w}"] = {"kids": k, "best_fs": fsg, "pass": all(x <= 4.0 for x in k.values())}
            P(f"    v_k = {v:.0f}, w = {w:4.2f}: Delta chi^2 {k['canonical']:+7.2f}/{k['alt']:+7.2f} "
              f"{'ok' if TAB[f'v{int(v)}/w{w}']['pass'] else 'FAIL'};  KiDS-preferred carrier amplitude "
              f"{fsg['canonical'][0]:.1f}/{fsg['alt'][0]:.1f} ({fsg['canonical'][1]:+.1f}/{fsg['alt'][1]:+.1f});  "
              f"L390 curvature branch {c1[v]['canonical']:+.1f}/{c1[v]['alt']:+.1f}   [{time.time() - T0:.0f}s]")
    OUT["numbers"]["table"] = TAB; OUT["numbers"]["L390_rerun"] = {str(v): c1[v] for v in VK}
    ok_all = all(d["pass"] for d in TAB.values())
    check("H1 [pre-declared] the converged model passes KiDS (<= +4, both footings) at w = 0.02 and 0.25, v_k = 600 and 650",
          "; ".join(f"{k_}: {d['kids']['canonical']:+.1f}/{d['kids']['alt']:+.1f}" for k_, d in TAB.items()),
          ok_all == EXPECT_PASS)
    check("V1 (reported) scores beside L390's and the KiDS-preferred carrier amplitude", "see table", True, load_bearing=False)

    nlb = sum(1 for _, ok, lb in CH if lb and not ok)
    OUT["n_checks"], OUT["n_fail_load_bearing"], OUT["elapsed_s"] = len(CH), nlb, round(time.time() - T0)
    fn = os.path.join(HERE, SLUG + ("_results_MUTATE.json" if MUTATE else "_results.json"))
    json.dump(OUT, open(fn, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    P(f"\n  {sum(ok for _, ok, _ in CH)}/{len(CH)} checks pass; load-bearing failures: {nlb}; wrote {os.path.basename(fn)}   "
      f"[{time.time() - T0:.0f}s]")
    sys.exit(1 if nlb else 0)
