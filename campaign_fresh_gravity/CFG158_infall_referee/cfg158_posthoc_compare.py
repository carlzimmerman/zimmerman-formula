#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CFG158 R5 (frozen in the criteria): AFTER the referee's own main and MUTATE runs were saved, CFG118's results JSON is opened and every
number it prints for the re-derived headline is tabulated against this lane's.  Reported only; no verdict here changes a frozen line.
Usage: python3 cfg158_posthoc_compare.py <path to CFG118_secondary_infall_results.json>
The path argument is not echoed.
"""
import os, sys, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
src = open("cfg158_referee.py").read().split("def main")[0].replace('sys.stdout = Tee("cfg158_referee%s.out" % TAG)', '')
exec(src)      # the referee's own functions and constants (no run is started)

theirs = json.load(open(sys.argv[1]))["numbers"]
mine = json.load(open("cfg158_referee_results.json"))
t0 = age(COSMO, 1.0)
print("CFG158 R5: CFG118's printed numbers against this lane's (tolerance for M_c ratios where conventions align: 5%; both codes reported as they are)")

print("\n[set-up] M_ta/M_b, r_ta(z=0) [kpc], M_out/M_b: CFG118 | CFG158 | relative difference")
worst = 0.0
for geom in ("point", "exp"):
    for M in MASSES:
        a = theirs["setup_%.0e_%s" % (M, geom)]; b = setups_ = mine["setup"]["%s_%.0e" % (geom, M)]
        vals = [(a["M_ta"] / M, b["Mta"] / M), (a["r_ta0"], b["rta"]), (a["M_out"] / M, b["Mout"] / M)]
        worst = max(worst, max(abs(y / x - 1) for x, y in vals))
        print("  %-5s %.0e  %7.3f | %7.3f   %8.2f | %8.2f   %7.2f | %7.2f" % (geom, M, vals[0][0], vals[0][1], vals[1][0], vals[1][1], vals[2][0], vals[2][1]))
print("  largest relative difference over all: %.2e" % worst)

print("\n[C1] Hubble flow: CFG118 dr=%.2e dv=%.2e | CFG158 dr=%.2e dv=%.2e" % (theirs["C1"]["dr"], theirs["C1"]["dv"], mine["C1"]["dr"], mine["C1"]["dv"]))
print("[C2] EdS slope: CFG118 %.3f (local %.2f..%.2f) | CFG158 %.3f (local %.2f..%.2f); M_ta/M_seed %.2f | %.2f" % (
    theirs["C2"]["slope"], min(theirs["C2"]["local"]), max(theirs["C2"]["local"]), mine["C2"]["slope"], min(mine["C2"]["local"]), max(mine["C2"]["local"]),
    56.4, mine["C2"]["Mta_over_seed"]))
print("     rho(lambda) CFG118: %s" % " ".join("%.3g" % v for v in theirs["C2"]["rho"]))

print("\n[cumulative M_c ratios] CFG118 (posthoc_Mc_vs_target, canonical, window-averaged by its convention) | CFG158 (window-averaged) at x=1.12 and 28.2, N=20000")
rows = []
for e in theirs["posthoc_Mc_vs_target"]:
    key = "%s_%.0e_q%.2f_N20000" % (e["geom"], e["M"], e["q"])
    r = mine["R"][key]
    rows.append((e["geom"], e["M"], e["q"], e["x1"], r["1.12"][0], e["x28"], r["28.2"][0], e["x1_5k"], mine["R"][key.replace("N20000", "N5000")]["1.12"][0], e["x28_5k"], mine["R"][key.replace("N20000", "N5000")]["28.2"][0]))
print("  %-5s %-7s %-5s | %8s %8s %7s | %8s %8s %7s" % ("geom", "M_b", "q", "118 R1.12", "158", "ratio", "118 R28.2", "158", "ratio"))
for r in rows:
    print("  %-5s %-7.0e %-5.2f | %8.3f %8.3f %7.3f | %8.3f %8.3f %7.3f" % (r[0], r[1], r[2], r[3], r[4], r[4] / r[3], r[5], r[6], r[6] / r[5]))
a1 = np.array([r[4] / r[3] - 1 for r in rows]); a28 = np.array([r[6] / r[5] - 1 for r in rows])
print("  CFG158/CFG118 - 1 at x=1.12: median %.3f, largest |.| %.3f, within 5%%: %d of 24" % (np.median(a1), np.abs(a1).max(), int((np.abs(a1) <= 0.05).sum())))
print("  CFG158/CFG118 - 1 at x=28.2: median %.3f, largest |.| %.3f, within 5%%: %d of 24" % (np.median(a28), np.abs(a28).max(), int((np.abs(a28) <= 0.05).sum())))
p1 = [r[3] for r in rows]; p28 = [r[5] for r in rows]
print("  envelopes: CFG118 R(1.12) [%.3f, %.3f], R(28.2) [%.3f, %.3f] | CFG158 [%.3f, %.3f], [%.3f, %.3f]" % (
    min(p1), max(p1), min(p28), max(p28), min(r[4] for r in rows), max(r[4] for r in rows), min(r[6] for r in rows), max(r[6] for r in rows)))
b1 = np.array([r[8] / r[7] - 1 for r in rows]); b28 = np.array([r[10] / r[9] - 1 for r in rows])
print("  5,000-shell runs, CFG158/CFG118 - 1: x=1.12 median %.3f largest %.3f; x=28.2 median %.3f largest %.3f" % (np.median(b1), np.abs(b1).max(), np.median(b28), np.abs(b28).max()))
print("  both codes' own noise (5k vs 20k), median |.|: CFG118 x=1.12 %.3f x=28.2 %.3f | CFG158 x=1.12 %.3f x=28.2 %.3f" % (
    np.median([abs(r[7] / r[3] - 1) for r in rows]), np.median([abs(r[9] / r[5] - 1) for r in rows]),
    np.median([abs(r[8] / r[4] - 1) for r in rows]), np.median([abs(r[10] / r[6] - 1) for r in rows])))

print("\n[R2] radius where M_c(<r) = M_b: exponent  CFG118 (20k) | CFG158 (20k)")
for geom in ("point", "exp"):
    for q in QS:
        e = theirs["posthoc_R2_Mc_equals_Mb"]["main|%s|q=%s" % (geom, {0.05: "0.05", 0.1: "0.1", 0.2: "0.2"}[q])]
        print("  %-5s q=%.2f  n = %.3f | %.3f    r1 [kpc] %s | %s" % (geom, q, e["exponent"], mine["exps"]["%s_q%.2f" % (geom, q)],
              ", ".join("%.2f" % v for v in e["r"]), "see .out"))
print("  turnaround exponent: CFG118 0.333 / 0.342 | CFG158 %.4f / %.4f" % (mine["turnaround_exp"]["point"], mine["turnaround_exp"]["exp"]))

print("\n[local C_infall/C_target] canonical, N=20000: CFG118 | CFG158 at x = 0.11, 1.12, 28.2 (the 0.11 bins hold ~0.1-20 time-averaged shells; noisy in both)")
cores = {(g, M): core_of(g, M) for g in ("point", "exp") for M in MASSES}
med = {0: [], 10: [], 24: []}
for g in ("point", "exp"):
    for M in MASSES:
        for q in QS:
            th = theirs["R1"]["canonical|q=%s|%.0e|%s" % ({0.05: "0.05", 0.1: "0.1", 0.2: "0.2"}[q], M, g)]["ratio"]
            run = load_run("%s_%.0e_q%.2f_N20000" % (g, M, q))
            rc, xc = ratio_curve(run, cores[(g, M)], t0, A0C)
            for i in med:
                med[i].append(rc[i] / th[i])
            if q == 0.1:
                print("  %-5s %.0e q=0.10: x=0.11 %.3g | %.3g   x=1.12 %.3g | %.3g   x=28.2 %.3g | %.3g" % (g, M, th[0], rc[0], th[10], rc[10], th[24], rc[24]))
for i, x in ((0, 0.11), (10, 1.12), (24, 28.2)):
    v = np.array(med[i])
    print("  CFG158/CFG118 local ratio at x=%.2f over 24 cases: median %.3f, 16-84%% [%.3f, %.3f]" % (x, np.median(v), np.percentile(v, 16), np.percentile(v, 84)))

print("\n[MUTATE] CFG118's own MUTATE evaluates G1 on the target itself (evaluator check). CFG158's MUTATE cells (core dropped, near-radial, no smooth background, sub-Hubble IC) are different controls.")
