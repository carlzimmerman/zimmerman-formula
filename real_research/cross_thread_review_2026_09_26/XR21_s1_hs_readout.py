#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR21_s1_hs_readout -- STAGE 1 (code tests for FP13's separator H_S read ON THE FLY): the box reads L and y_th from its own
nonlinear matter field, and how that reading compares with FP13's committed (halofit) readout.

STATUS OF H_S (the coordinator, relaying XR18, after this lane was specified): FP13's H_S is linearly ILL-POSED as written at
z <= 0.635 -- the state term's leaf average puts an O(1) local force into the lapse and phi equations (R_B = 6.9-8.1 on FP13's
headline state; the psi-constraint's symbol k^2 (1 - R_B) changes sign on k = 0.12-1.62 h/Mpc).  The repair belongs to the chain
lead.  This script is therefore a CODE TEST of the live-readout machinery only; no H_S box number here is physics.  The box
applies the readout as a prescribed functional: the state term's own force is NOT in the quasi-static operator, so these boxes
can neither show nor rule out XR18's ill-posedness (no blow-up here means nothing about it).  The readout rules are pluggable
(XR21_pm_core.HSLive: L_rule, y_rule) so a repaired readout -- B fixed by dS/dB = 0, or a <K>_h-type state -- drops in.

WHY.  FP13 (27faacc84) replaced FP9's four declared constants with state functionals: L from <(S_B delta_m)^2>_h = delta_c^2
(delta_c = 1.686, the MATTER readout, the ACTUAL nonlinear field) and y_th = c_y <|g_bp|^2>_h^(1/2)/a0 x max(0, 2q).  FP13 is
explicit that its result is conditional on the action reading the actual nonlinear field, for which it used halofit LCDM as
a stand-in.  A particle-mesh box can read its own field -- but only the field it resolves (the mesh, the fundamental mode,
its particle noise).  Stage 1 builds the live readout (XR21_pm_core.HSLive), tests its arithmetic (XR21_s1_separator_linear
H1), and here measures (i) the live reading of LCDM boxes against FP13's committed tables, at two resolutions and two box
sizes, and (ii) the live readout feeding back inside a small H_S box, against the frozen (FP13) readout.  Whether delta_c stays
inside the theory's own window (FP13: 1.3-2.6) on the actual field is stage 2's question; stage 1 supplies the instrument.

RUNS (L362's CLASS ICs, seed 7; the live readout reads the TOTAL matter field on the mesh, the box average standing in for
the leaf average)
  B1  LCDM, 50 Mpc/h, 128^3 mesh, 128^3 particles (0.39 Mpc/h: the production cell)
  B2  LCDM, 50 Mpc/h, 256^3 mesh, 256^3 particles (0.195 Mpc/h: 2x finer, the same box)
  B3  LCDM, 100 Mpc/h, 256^3 mesh, 256^3 particles (0.39 Mpc/h in a 2x larger box)
  M1  H_S LIVE, chain reading (the kernel reads the baryons; only baryons feel the phantom), 50 Mpc/h, 128^3 mesh, 2 x 128^3
      particles, canonical footing -- the readout recomputed every step and fed to the operator
  M2  H_S FROZEN (FP13's committed tables), otherwise M1
CHECKS
  D1 [code] the live yield obeys FP13's ramp: y_th = 0 exactly at every step with 2q <= 0 (z <= 0.635) and > 0 at every step
     with 2q > 0 once the band-pass is open, in M1 and in the LCDM readouts.
  D2 [code] in M1 the readout is taken at every step and is the one the operator uses (the operator's L equals the readout's L
     to 1e-12 at every step; the history has one entry per force evaluation).
  D3 [reported] the LCDM boxes' live readout against FP13's committed tables (L, y_th at z = 6 ... 0; both footings for y_th):
     the resolution (B1 vs B2) and box-size (B1 vs B3) dependence of 'the actual nonlinear field' as a box reads it, and the
     redshift above which the live L falls below 2 cells (the band-pass unresolved on that mesh).
  D4 [reported] H_S live vs frozen in the small nonlinear box: the L and y_th histories and the matter and lensing power
     live/frozen at z = 1, 0.5, 0 (a code-path demonstration of the feedback -- NOT physics: H_S is ill-posed as written, XR18).
MUTATE=1: the live readout loses its onset switch (FP13's MUTATE: y_th = the band-passed rms at every epoch): D1 must FAIL
(rc = 1).  Under MUTATE only B1 and M1 run, and D3/D4 are not reported.

HISTORY.  No run of this script preceded these declarations (the live readout's arithmetic was unit-tested in
XR21_s1_separator_linear, whose smoke run was in scratch).  SCOPE: code tests and reported comparisons; the QUMOND-type
approximation; no gate is scored.  kappa = 1/2 is FITTED (Z = 5.7888).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR21_s1_hs_readout.py
(~20 min, 3 worker processes (1 thread each), peak ~10 GB total)
"""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR21_common as X
X.pin_threads(1)
import numpy as np
from multiprocessing import get_context

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "XR21_s1_hs_readout"
ZO = (6.0, 4.0, 3.0, 2.5, 2.0, 1.5, 1.0, 0.7, 0.6, 0.5, 0.25, 0.0)


def lcdm_worker(cfg):
    X.pin_threads(1)
    import XR21_pm_core as C
    cos = C.Cosmo("l362"); P362 = X.l362_plin()
    box = C.Box(cfg["L"], cfg["NG"], cfg["NP"], cos, zi=49.0, seed=7, mode="single", gravity="newton",
                Pfun=lambda q: P362(q, 49.0))
    live = {f: C.HSLive(cos, cos.a0_code(f), switch="none" if MUTATE else "ramp") for f in C.FOOTS}

    def out(b, a, z):
        rb, rd = b.densities(); b.cb = b.cd = None
        Fd = b.mesh.rfft(rb + rd - 1.0)
        rec = {"a": a, "two_q": live["canonical"].two_q(a)}
        for f, hl in live.items():
            L_, y_, s0 = hl.readout(b.mesh, Fd, a)
            rec[f] = dict(L_com=L_, L_phys_kpc=1e3 * L_ * a / cos.h, y_th=y_, sigma0=s0)
        rec["L_cells"] = rec["canonical"]["L_com"] / b.mesh.d
        return rec
    t = time.time()
    r = box.run(list(ZO), on_output=out)
    return cfg["name"], dict(out=r, wall=time.time() - t, steps=box.nstep, rss=C.peak_rss_gb(), cfg=cfg)


def model_worker(cfg):
    X.pin_threads(1)
    import XR21_pm_core as C
    cos = C.Cosmo("l362"); P362 = X.l362_plin()
    if cfg["sep"] == "live":
        sep = C.HSLive(cos, cos.a0_code("canonical"), switch="none" if MUTATE else "ramp")
    else:
        sep = C.HSFrozen(cos, cfg["tables"][0], cfg["tables"][1], cfg["tables"][2])
    box = C.Box(50.0, 128, 128, cos, zi=49.0, seed=7, mode="two", gravity="hy", reading="chain", hy=sep, foot="canonical",
                Pfun=lambda q: P362(q, 49.0))
    used = []

    def on_step(b, a):
        used.append((a, b.diag.get("L_com", float("nan")), b.diag.get("y_th", float("nan"))))

    def out(b, a, z):
        dm, dph = b.lensing_delta(a)
        k, Pm, _ = b.mesh.power_shells(dm); _, Pl, _ = b.mesh.power_shells(dm + dph)
        return dict(a=a, k=k.tolist(), Pm=Pm.tolist(), Pl=Pl.tolist(), L_com=sep.L_com(a), y_th=sep.y_th(a))
    t = time.time()
    r = box.run([1.0, 0.5, 0.0], on_output=out, on_step=on_step)
    hist = getattr(sep, "hist", [])
    return cfg["name"], dict(out=r, used=used, hist=hist, wall=time.time() - t, steps=box.nstep, rss=C.peak_rss_gb())


if __name__ == "__main__":
    lane = X.Lane(SLUG, MUTATE)
    P, check, banner = lane.P, lane.check, lane.banner
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: the live readout without its onset switch; D1 must FAIL ***")
    import XR21_pm_core as C
    ns13 = X.load_fp13_state()
    tab = (list(ns13["LNA"]), list(ns13["HS_LH"]), list(ns13["HS_ytab"]["canonical"]))
    Lh, yh = ns13["HS_Lh"], ns13["HS_yh"]
    cfgs_l = [dict(name="B2", L=50.0, NG=256, NP=256), dict(name="B3", L=100.0, NG=256, NP=256), dict(name="B1", L=50.0, NG=128, NP=128)]
    cfgs_m = [dict(name="M1_live", sep="live"), dict(name="M2_frozen", sep="frozen", tables=tab)]
    if MUTATE:                                                   # the switch test needs only one LCDM box and the live H_S box
        cfgs_l = [c_ for c_ in cfgs_l if c_["name"] == "B1"]; cfgs_m = [c_ for c_ in cfgs_m if c_["name"] == "M1_live"]
    ctx = get_context("spawn")
    with ctx.Pool(3) as pool:
        jl = [pool.apply_async(lcdm_worker, (c_,)) for c_ in cfgs_l]
        jm = [pool.apply_async(model_worker, (c_,)) for c_ in cfgs_m]
        RL = dict(j.get() for j in jl); RM = dict(j.get() for j in jm)
    P(f"\n  runs done {lane.el()}: " + "; ".join(f"{k_} {v['wall']:.0f} s/{v['steps']} steps/{v['rss']:.1f} GB" for k_, v in {**RL, **RM}.items()))
    lane.out["runs"] = {k_: dict(wall=v["wall"], steps=v["steps"], rss_gb=v["rss"]) for k_, v in {**RL, **RM}.items()}

    banner("D1, D2  THE LIVE READOUT'S SWITCH AND ITS USE")
    viol = 0; n_on = 0; n_off = 0
    cos = C.Cosmo("l362")
    for k_, rr in RL.items():
        for z, v in rr["out"].items():
            tq = v["two_q"]
            for f in C.FOOTS:
                y_ = v[f]["y_th"]; L_ = v[f]["L_com"]
                if tq <= 0:
                    n_off += 1; viol += (y_ != 0.0)
                elif L_ > 0:
                    n_on += 1; viol += not (y_ > 0.0)
    for (a, L_, y_, s0) in RM["M1_live"]["hist"]:
        tq = C.HSLive(cos, 1.0).two_q(a)
        if tq <= 0:
            n_off += 1; viol += (y_ != 0.0)
        elif L_ > 0:
            n_on += 1; viol += not (y_ > 0.0)
    check("D1 [code] THE LIVE YIELD OBEYS FP13'S RAMP: y_th = 0 exactly wherever 2q <= 0 (z <= 0.635) and y_th > 0 wherever 2q > 0 "
          "with the band-pass open -- every LCDM readout (3 boxes, 12 epochs, both footings) and every step of the live H_S box",
          f"{n_off} readouts at 2q <= 0, {n_on} at 2q > 0 with the band-pass open; violations {viol}", viol == 0 and n_off > 0 and n_on > 0,
          "MUTATE removes the switch (FP13's own MUTATE): the yield then stays at the band-passed rms after z = 0.635" if not MUTATE else "")
    hist = RM["M1_live"]["hist"]; used = RM["M1_live"]["used"]
    n_match = min(len(hist), len(used))
    dmax = max(abs(h_[1] - u_[1]) for h_, u_ in zip(hist[-n_match:], used[-n_match:])) if n_match else float("nan")
    check("D2 [code] THE READOUT FEEDS THE OPERATOR: in the live H_S box the readout is taken at every force evaluation and the "
          "operator's band-pass length is the readout's (to 1e-12)",
          f"{len(hist)} readouts for {RM['M1_live']['steps']} steps (+1 initial); max |L_operator - L_readout| {dmax:.1e}",
          len(hist) == RM["M1_live"]["steps"] + 1 and dmax <= 1e-12)

    if MUTATE:
        banner("VERDICT")
        P("  MUTATE: without the onset switch the live yield stays on after the leaf accelerates, as FP13's own MUTATE says.")
        sys.exit(lane.finish())
    banner("D3  LCDM BOXES READ BY THE LIVE READOUT vs FP13'S COMMITTED (halofit) READOUT")
    D3 = {}
    for z in ZO:
        a = 1 / (1 + z)
        row = {"FP13": dict(L_kpc=1e3 * Lh(a), y_can=yh["canonical"](a), y_alt=yh["alt"](a))}
        line = f"    z {z:4.2f}: FP13 L {row['FP13']['L_kpc']:7.1f} kpc, y_th {row['FP13']['y_can']:.2e}"
        for k_ in ("B1", "B2", "B3"):
            v = RL[k_]["out"][str(z)]
            row[k_] = dict(L_kpc=v["canonical"]["L_phys_kpc"], L_cells=v["L_cells"], y_can=v["canonical"]["y_th"], y_alt=v["alt"]["y_th"],
                           sigma0=v["canonical"]["sigma0"])
            line += (f" | {k_} L {row[k_]['L_kpc']:7.1f} kpc ({row[k_]['L_cells']:4.1f} cells), y {row[k_]['y_can']:.2e}, "
                     f"sigma_mesh {row[k_]['sigma0']:.2f}")
        P(line)
        D3[str(z)] = row
    low_res = {k_: max([z for z in ZO if RL[k_]["out"][str(z)]["L_cells"] < 2.0] or [float("nan")]) for k_ in ("B1", "B2", "B3")}
    check("D3 [reported] the LIVE readout of LCDM boxes against FP13's halofit readout: resolution (B1 0.39 vs B2 0.195 Mpc/h, same "
          "50 Mpc/h box) and box size (B1 vs B3, same 0.39 Mpc/h cell); the band-pass is unresolved (L < 2 cells) above the printed z",
          "L(z = 0)/FP13: " + ", ".join(f"{k_} {D3['0.0'][k_]['L_kpc'] / D3['0.0']['FP13']['L_kpc']:.3f}" for k_ in ("B1", "B2", "B3"))
          + "; L(z = 1)/FP13: " + ", ".join(f"{k_} {D3['1.0'][k_]['L_kpc'] / D3['1.0']['FP13']['L_kpc']:.3f}" for k_ in ("B1", "B2", "B3"))
          + "; y_th(z = 1)/FP13: " + ", ".join(f"{k_} {D3['1.0'][k_]['y_can'] / max(D3['1.0']['FP13']['y_can'], 1e-30):.3f}" for k_ in ("B1", "B2", "B3"))
          + f"; highest z with L < 2 cells: {low_res}", True,
          "the live readout is the actual field only as far as the box resolves it: a mesh smooths the variance that sets L and the "
          "field that sets y_th -- a resolution systematic stage 2 must carry (converge in the mesh, or correct the unresolved power)",
          load_bearing=False)
    lane.out["numbers"]["D3"] = D3; lane.out["numbers"]["D3_unresolved_above_z"] = low_res

    banner("D4  H_S LIVE vs FROZEN in a small nonlinear box (chain reading, canonical): the feedback, as a code path")
    D4 = {}
    for z in ("1.0", "0.5", "0.0"):
        o1, o2 = RM["M1_live"]["out"][z], RM["M2_frozen"]["out"][z]
        k = np.array(o1["k"]); sel = (k >= 0.3) & (k <= 3.0)
        rm = np.array(o1["Pm"])[sel] / np.array(o2["Pm"])[sel]; rl = np.array(o1["Pl"])[sel] / np.array(o2["Pl"])[sel]
        D4[z] = dict(L_live=o1["L_com"], L_frozen=o2["L_com"], y_live=o1["y_th"], y_frozen=o2["y_th"],
                     Pm_live_over_frozen=[float(rm.min()), float(rm.max())], Pl_live_over_frozen=[float(rl.min()), float(rl.max())])
        P(f"    z {z}: L live {o1['L_com']:.3f} vs frozen {o2['L_com']:.3f} Mpc/h; y_th live {o1['y_th']:.2e} vs frozen {o2['y_th']:.2e}; "
          f"P_m live/frozen (0.3-3 h/Mpc) {rm.min():.3f}-{rm.max():.3f}; P_lens live/frozen {rl.min():.3f}-{rl.max():.3f}")
    check("D4 [reported] the live readout feeding back inside an H_S box (50 Mpc/h, 128^3, chain reading) against FP13's frozen "
          "readout: the band-pass length, the yield and the matter/lensing power (a code-path demonstration; no gate)",
          "; ".join(f"z {z}: L {v['L_live']:.2f}/{v['L_frozen']:.2f}, P_m {v['Pm_live_over_frozen'][0]:.2f}-{v['Pm_live_over_frozen'][1]:.2f}"
                    for z, v in D4.items()), True,
          "a code path only: H_S is linearly ill-posed as written at z <= 0.635 (XR18) and the box omits the state term's own force",
          load_bearing=False)
    lane.out["numbers"]["D4"] = D4
    lane.out["numbers"]["M1_hist"] = RM["M1_live"]["hist"][::5]

    banner("VERDICT")
    P("  " + ("MUTATE: without the onset switch the live yield stays on after the leaf accelerates, as FP13's own MUTATE says." if MUTATE
              else "The live H_S readout works as an instrument: FP13's ramp holds exactly, the operator uses the readout it takes each "
                   "step, and the LCDM boxes show how far a mesh's 'actual field' is from FP13's halofit stand-in (D3).  No H_S number "
                   "here is physics: XR18 finds H_S ill-posed as written at z <= 0.635, a force this quasi-static box does not contain."))
    sys.exit(lane.finish())
