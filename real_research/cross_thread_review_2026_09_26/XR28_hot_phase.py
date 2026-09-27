#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR28 -- THE RECAPTURED HOT PHASE: does the chain's two-phase dark sector leave its own signature in cluster outskirts (a
shallower dark-matter slope minimum, a second caustic, a galaxy-lensing offset), and does the L-verdict of XR28_outskirts_L
depend on how the dark fluid converts?

THE DARK SECTOR (FK1/FP10/XR19; nothing added).  The fluid converts phi_H phi_H -> phi_L phi_L with an isotropic kick v_k
(575-650 km/s, FK1) in the parent's frame; the daughters are kernel-invisible and feel Newtonian gravity only.  Per shell, at
the observation epoch: F_halo - F_b (FP10 A6: bound in sub-haloes, cold on the cluster's scale), F_b (escaped from sub-haloes
at z ~ 5-13), the smooth remainder 1 - F_halo, which XR19 converts in the web (nominal f_web(z)), near turnaround (XR19 I1), or
which reaches the host's front (FP10 A6: 0.95 r200c).  BRACKETS (each a reading of the chain's own rules, run in full):
  cold        every dark particle cold (the LCDM dark sector with the chain's phantom): no hot phase -- the reference
  halo        FP10's escape only; the smooth remainder stays cold for ever (the largest cold phase the histories allow)
  nominal     escape + XR19's web epochs + the remainder at the front (XR28_outskirts_L's configuration), v_k = 575/600/650
  turnaround  escape + the smooth remainder converts at max(its turnaround, z = 1.5) (XR19 I1's zone reading)
  front       escape + the smooth remainder converts at the front on first infall (FP10's history reading without XR19)
Baryons feel the band-passed phantom at H_Y's L0 = 1.688 Mpc (both footings); a no-phantom run isolates the hot phase alone.

CHECKS (pre-declared; load-bearing unless marked)
  HP1 THE SIGNATURE EXISTS: in every hot bracket the stacked 3D dark-matter slope minimum is shallower than in the cold
      reference (same ICs, phantom and L) by >= 0.5, both samples, both footings.
  HP2 THE L-VERDICT IS NOT A DARK-SECTOR CHOICE: across the brackets and kicks, the DK14 WL r_sp/r200m moves by <= 0.10 and
      the WL gamma by <= 0.5 relative to the nominal bracket (below the published WL errors, 0.15-0.29 and 0.4-0.5).
  HP3 (reported) a SECOND CAUSTIC: a second local minimum of the 3D dark-matter slope in [0.4, 3] r200m, deeper than -3 and
      >= 0.15 dex from the main one, in any bracket.
  HP4 (reported) the GALAXY-LENSING OFFSET x_gal/x_WL per bracket against the data (ACT-DR5 1.10/1.16; DES-Y1 0.82/0.97).
  HP5 (reported) the hot phase alone (no phantom, nominal vs cold) against LCDM.
MUTATE=1: every bracket is forced cold (the recaptured phase removed): HP1 must FAIL -- rc = 1.

HISTORY (stated).  A scratch run (ACT-DR5 mass, t = 0 member, N_q = 800, 6 kick nodes) came first: the nominal hot phase made
the 3D DM slope minimum shallower (-6.7 -> -5.2) and moved the DM r_sp inward (1.04 -> 0.94 r200m).  The checks were written
after it and before this script's first run, with the production settings fixed in XR28_controls K6b (apocentre
scatter 0.12, [0.5, 3] r200m read-out, ds = 0.00075, 4 kick nodes).

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR28_hot_phase.py   (~8 min, 2 workers)
"""
import os, sys, math, json, time, warnings
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
warnings.filterwarnings("ignore")
import numpy as np
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import XR28_common as X
from XR28_outskirts_L import run_member, observe, NQ

MUTATE = os.environ.get("MUTATE", "0") == "1"
SAMPLES = ["ACT-DR5 x DES-Y3 (Shin+2021)", "DES-Y1 redMaPPer (Chang+2018)"]
BRACKETS = [("cold", 600.0), ("halo", 600.0), ("nominal", 600.0), ("turnaround", 600.0), ("front", 600.0), ("nominal", 575.0),
            ("nominal", 650.0)]


def point(key, dark, vk, L0, a0, Mf_guess, tol=0.06):
    d = X.DATA[key]; z = d["z"]; Mt = d["M200m"] * 1e14 / X.HD
    fp10 = X.fp10_budget(vk, "185"); fweb = X.fweb_history(fp10)
    drk = "cold" if (MUTATE and dark != "lcdm") else dark
    Mf = Mf_guess; t0 = None
    for _ in range(3):
        t0 = run_member(Mf, z, 0.0, drk, L0, a0, "p2", fp10, fweb, vk=vk, nmu=4)
        Mm = X.stack([(1.0, s_) for s_ in t0])["M200m_lens"]
        if abs(Mm / Mt - 1) <= tol:
            break
        Mf *= Mt / Mm; t0 = None
    if t0 is None:
        t0 = run_member(Mf, z, 0.0, drk, L0, a0, "p2", fp10, fweb, vk=vk, nmu=4)
    items = [(X.GH3[1][1] / 7.0, s_) for s_ in t0]
    for tt, w_ in (X.GH3[0], X.GH3[2]):
        items += [(w_ / 7.0, s_) for s_ in run_member(Mf, z, tt, drk, L0, a0, "p2", fp10, fweb, vk=vk, nmu=4)]
    st = X.stack(items)
    out = observe(st, 1 / (1 + z), L0)
    out.update(Mf=Mf, mass_ratio=st["M200m_lens"] / Mt)
    return out


def job(args):
    key, foot, what = args
    d = X.DATA[key]; Mt = d["M200m"] * 1e14 / X.HD
    rows = []
    if what == "nophantom":
        for dark in ("lcdm", "nominal"):
            r = point(key, dark, 600.0, None, None, Mt * 1.25); r.update(bracket=dark + "-noMOND", vk=600.0, foot=None); rows.append(dict(key=key, **r))
        return rows
    guess = Mt * 1.0
    for dark, vk in BRACKETS:
        r = point(key, dark, vk, X.L0_HY, X.A0[foot], guess)
        guess = r["Mf"]
        r.update(bracket=dark, vk=vk, foot=foot); rows.append(dict(key=key, **r))
    return rows


if __name__ == "__main__":
    R = X.Report("XR28 hot phase", "XR28_hot_phase", MUTATE)
    P, check = R.P, R.check
    P(__doc__.split("CHECKS")[0].strip())
    if MUTATE:
        P("\n  *** MUTATE=1: every bracket forced cold (the recaptured hot phase removed) -- HP1 must FAIL ***")
    jobs = [(k_, f_, "phantom") for k_ in SAMPLES for f_ in X.FOOTS] + [(k_, None, "nophantom") for k_ in SAMPLES]
    with Pool(2) as pool:
        res = [r_ for rows in pool.imap_unordered(job, jobs) for r_ in rows]
    P(f"  runs done {R.el()}")
    T = {(r_["key"], r_["foot"], r_["bracket"], r_["vk"]): r_ for r_ in res}
    R.numbers["runs"] = {f"{k_[0]}|{k_[1]}|{k_[2]}|{k_[3]:.0f}": v_ for k_, v_ in T.items()}

    R.banner("THE BRACKETS at H_Y's L0 (lensing and galaxies by the DK14 forward-fit; dark matter in 3D)")
    for key in SAMPLES:
        P(f"\n  {key}")
        P(f"    {'bracket':>16s} {'foot':>9s} | {'WL x':>6s} {'g':>6s} | {'gal x':>6s} {'g':>6s} | {'DM3D x':>6s} {'g':>6s} | DM slope minima [r/r200m, slope]")
        for f_ in X.FOOTS:
            for dark, vk in BRACKETS:
                r_ = T[(key, f_, dark, vk)]
                P(f"    {dark + ' ' + str(int(vk)):>16s} {f_:>9s} | {r_['xwl']:6.3f} {r_['gwl']:6.2f} | {r_['xgal']:6.3f} {r_['ggal']:6.2f} | "
                  f"{r_['x3_dm']:6.3f} {r_['g3_dm']:6.2f} | {r_['minima_dm']}")
        for dark in ("lcdm-noMOND", "nominal-noMOND"):
            r_ = T[(key, None, dark, 600.0)]
            P(f"    {dark:>16s} {'-':>9s} | {r_['xwl']:6.3f} {r_['gwl']:6.2f} | {r_['xgal']:6.3f} {r_['ggal']:6.2f} | "
              f"{r_['x3_dm']:6.3f} {r_['g3_dm']:6.2f} | {r_['minima_dm']}")

    R.banner("CHECKS")
    hot = [b_ for b_ in BRACKETS if b_[0] != "cold"]
    dg = {f"{k_}|{f_}|{b_[0]}|{b_[1]:.0f}": T[(k_, f_, b_[0], b_[1])]["g3_dm"] - T[(k_, f_, "cold", 600.0)]["g3_dm"]
          for k_ in SAMPLES for f_ in X.FOOTS for b_ in hot}
    check("HP1 THE SIGNATURE EXISTS: every hot bracket makes the 3D dark-matter slope minimum shallower than the cold reference by "
          ">= 0.5 (both samples, both footings)", f"Delta gamma_DM {min(dg.values()):+.2f} to {max(dg.values()):+.2f}",
          min(dg.values()) >= 0.5)
    dx = {}; dgw = {}
    for k_ in SAMPLES:
        for f_ in X.FOOTS:
            nom = T[(k_, f_, "nominal", 600.0)]
            for b_ in BRACKETS:
                r_ = T[(k_, f_, b_[0], b_[1])]
                dx[f"{k_}|{f_}|{b_[0]}|{b_[1]:.0f}"] = r_["xwl"] - nom["xwl"]; dgw[f"{k_}|{f_}|{b_[0]}|{b_[1]:.0f}"] = r_["gwl"] - nom["gwl"]
    check("HP2 THE L-VERDICT IS NOT A DARK-SECTOR CHOICE: across the brackets and kicks the DK14 WL r_sp/r200m moves by <= 0.10 and "
          "the WL gamma by <= 0.5 from the nominal bracket", f"Delta x_WL {min(dx.values()):+.3f} to {max(dx.values()):+.3f}; Delta gamma_WL "
          f"{min(dgw.values()):+.2f} to {max(dgw.values()):+.2f}", max(abs(v_) for v_ in dx.values()) <= 0.10 and max(abs(v_) for v_ in dgw.values()) <= 0.5)
    sec = {}
    for k_, v_ in T.items():
        mins = [m_ for m_ in (v_["minima_dm"] or []) if m_[1] < -3.0]
        if len(mins) >= 2 and np.isfinite(v_["x3_dm"]):
            far = [m_ for m_ in mins if abs(math.log10(m_[0] / v_["x3_dm"])) >= 0.15]
            if far:
                sec[f"{k_[0]}|{k_[1]}|{k_[2]}|{k_[3]:.0f}"] = far
    check("HP3 (reported) a SECOND CAUSTIC in the dark matter (a second slope minimum < -3 at >= 0.15 dex from the main one)",
          f"{len(sec)} of {len(T)} runs: " + "; ".join(f"{k_.split(' (')[1]}: {v_}" for k_, v_ in list(sec.items())[:6]), True, load_bearing=False)
    off = {f"{k_}|{f_}|{b_[0]}|{b_[1]:.0f}": T[(k_, f_, b_[0], b_[1])]["xgal"] / T[(k_, f_, b_[0], b_[1])]["xwl"]
           for k_ in SAMPLES for f_ in X.FOOTS for b_ in BRACKETS}
    check("HP4 (reported) THE GALAXY-LENSING OFFSET x_gal/x_WL (data: ACT-DR5 1.10/1.16 = 0.95; DES-Y1 0.82/0.97 = 0.85)",
          "; ".join(f"{k_.split(' (')[0][:8]}|{k_.split('|', 1)[1]} {v_:.2f}" for k_, v_ in off.items() if "|canonical|" in k_), True, load_bearing=False)
    nm = {k_: (T[(k_, None, "nominal-noMOND", 600.0)], T[(k_, None, "lcdm-noMOND", 600.0)]) for k_ in SAMPLES}
    check("HP5 (reported) THE HOT PHASE ALONE (no phantom): nominal vs LCDM", "; ".join(
        f"{k_.split(' (')[0]}: DM x_sp {a_['x3_dm']:.3f} vs {b_['x3_dm']:.3f}, gamma {a_['g3_dm']:.2f} vs {b_['g3_dm']:.2f}; WL x {a_['xwl']:.3f} vs "
        f"{b_['xwl']:.3f}, gamma {a_['gwl']:.2f} vs {b_['gwl']:.2f}" for k_, (a_, b_) in nm.items()), True, load_bearing=False)
    R.numbers["HP"] = dict(dgamma_dm=dg, dx_wl=dx, dgamma_wl=dgw, second=sec, offset=off)
    sys.exit(R.finish())
