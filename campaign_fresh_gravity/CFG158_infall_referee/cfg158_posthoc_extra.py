#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG158 post-hoc rows (added AFTER the frozen main run failed C2, C3 and C4; reported only, no frozen verdict depends on them).
 (a) C2: the EdS slope from window-averaged (not snapshot) cumulative masses, and the slope over other radius windows.
 (b) C4 attribution: two extra 5,000-shell runs of the C4 case that change ONE of (dt_s and eta_h) or (rtol) at a time.
 (c) C3/C4 noise floor: the 1e10 point q=0.1 case at N=5,000 with the initial shell grid offset (m/2 shift is not available), so instead
     the spread between the 5,000- and 20,000-shell runs over all 24 cases is tabulated by radius.
Run: python3 cfg158_posthoc_extra.py   (needs the cached main products in cfg158_sims/).
"""
import os, sys, subprocess, math, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
SIMS = "cfg158_sims"
G = 4.30091727e-6; H0 = 0.0674; MYR = 977.79222


def load(name):
    p = os.path.join(SIMS, name)
    meta = {}
    for ln in open(p + ".meta.txt"):
        k, v = ln.split(); meta[k] = float(v)
    N = int(meta["N"]); ng = int(meta["ng"]); ns = int(meta["nsamp"])
    fin = np.fromfile(p + ".final.bin").reshape(6, N)
    return dict(meta=meta, N=N, R=fin[0], t=np.fromfile(p + ".times.bin"), S=np.fromfile(p + ".samples.bin").reshape(ns, ng), rg=np.fromfile(p + ".rgrid.bin"))


def R_at(run, Mb, x, a0=9.3603e-11 * 3.0856775814913673e19 / 1e6):
    rm = math.sqrt(G * Mb / a0)
    rg, t, S = run["rg"], run["t"], run["S"]
    snap = S[-1]
    rho = (Mb * rg ** 3 / (rg * rg + (1e-3 * rm) ** 2) ** 1.5 + snap) / (4 * np.pi / 3 * rg ** 3)
    w = np.minimum(np.sqrt(3 * np.pi / (16 * G * rho)), 0.9 * t[-1])
    av = np.array([S[t >= t[-1] - w[j] - 1e-12, j].mean() for j in range(len(rg))])
    r = x * rm
    return np.interp(np.log(r), np.log(rg), av) / (Mb * (math.sqrt(1 + x * x) - 1))


def main():
    print("CFG158 post-hoc rows (reported only; added after C2, C3, C4 failed)")
    # (a) C2 windowed slope
    r = load("c2_eds_N20000")
    rta = 580.6   # EdS a=1 turnaround radius of the seed run (printed by the main run)
    rg, t, S = r["rg"], r["t"], r["S"]
    m = r["meta"]["m"]
    print("\n[a] EdS control: slope estimators (r_ta = %.1f kpc)" % rta)
    for lo, hi, nb in ((0.03, 0.15, 7), (0.05, 0.3, 8), (0.02, 0.1, 7), (0.03, 0.10, 5)):
        edges = lo * (hi / lo) ** (np.arange(nb + 1) / nb) * rta
        # snapshot counts
        cnt = np.histogram(r["R"], bins=edges)[0]
        rho_s = cnt * m / (4 * np.pi / 3 * (edges[1:] ** 3 - edges[:-1] ** 3))
        rc = np.sqrt(edges[1:] * edges[:-1])
        s_snap = np.polyfit(np.log(rc), np.log(rho_s), 1)[0]
        # window-averaged cumulative mass at the edges (window = 1 Gyr, i.e. the samples of the last 1 Gyr)
        for win_myr in (100.0, 1000.0):
            sel = t >= t[-1] - win_myr / MYR
            Me = np.array([np.interp(np.log(e), np.log(rg), S[sel].mean(axis=0)) for e in edges])
            rho_w = np.diff(Me) / (4 * np.pi / 3 * (edges[1:] ** 3 - edges[:-1] ** 3))
            s_w = np.polyfit(np.log(rc), np.log(rho_w), 1)[0]
            print("  r/r_ta in [%.2f,%.2f] (%d bins): snapshot slope %.3f | %d-Myr window-averaged slope %.3f" % (lo, hi, nb, s_snap, win_myr, s_w))
    # (b) C4 attribution
    base = open(os.path.join(SIMS, "point_1e+10_q0.10_N5000.spec")).read().strip()
    def variant(name, upd):
        d = dict(kv.split("=", 1) for kv in base.split()); d.update(upd); d["out"] = os.path.join(SIMS, name)
        return " ".join("%s=%s" % (k, d[k]) for k in sorted(d))
    variants = {"ph_dt05_eta15e-4_rtol10_N5000": dict(dt_myr="0.5", eta_h="1.5e-4"), "ph_dt1_rtol11_N5000": dict(rtol="1e-11")}
    procs = []
    for nm, upd in variants.items():
        if os.path.exists(os.path.join(SIMS, nm + ".meta.txt")):
            continue
        tf = os.path.join(SIMS, "tasks_ph_%s.txt" % nm)
        open(tf, "w").write(variant(nm, upd) + "\n")
        env = dict(os.environ); env["JULIA_NUM_THREADS"] = "1"
        procs.append(subprocess.Popen(["julia", "-O3", "--startup-file=no", "cfg158_shells.jl", tf], stdout=open(tf + ".log", "w"), stderr=subprocess.STDOUT, env=env))
    for p in procs:
        p.wait()
    print("\n[b] C4 attribution (1e10 point q=0.1, N=5000): R(1.12), R(28.2) window-averaged")
    rows = [("base: dt 1 Myr, eta 3e-4, rtol 1e-10", "point_1e+10_q0.10_N5000"), ("dt 0.5 Myr, eta 1.5e-4, rtol 1e-10", "ph_dt05_eta15e-4_rtol10_N5000"),
            ("dt 1 Myr, eta 3e-4, rtol 1e-11", "ph_dt1_rtol11_N5000"), ("dt 0.5, eta 1.5e-4, rtol 1e-11 (C4 run)", "c4_dt05_rtol11_N5000"),
            ("N=20000 base", "point_1e+10_q0.10_N20000")]
    for lab, nm in rows:
        if os.path.exists(os.path.join(SIMS, nm + ".meta.txt")):
            rr = load(nm)
            print("  %-42s R(1.12)=%.3f  R(28.2)=%.3f" % (lab, R_at(rr, 1e10, 1.12), R_at(rr, 1e10, 28.2)))
    # (c) spread by case
    print("\n[c] |R5k/R20k - 1| by case (window-averaged), x = 1.12 and 28.2")
    for geom in ("point", "exp"):
        for Mb in (1e9, 1e10, 1e11, 1e12):
            line = []
            for q in (0.05, 0.10, 0.20):
                a = load("%s_%.0e_q%.2f_N20000" % (geom, Mb, q)); b = load("%s_%.0e_q%.2f_N5000" % (geom, Mb, q))
                if geom == "point":
                    f = lambda run, x: R_at(run, Mb, x)
                    line.append("q=%.2f: %.2f/%.2f" % (q, f(b, 1.12) / f(a, 1.12) - 1, f(b, 28.2) / f(a, 28.2) - 1))
            if geom == "point":
                print("  point %.0e  %s" % (Mb, "   ".join(line)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
