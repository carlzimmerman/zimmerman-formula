#!/usr/bin/env python3
"""AG7: power pre-flight. Can Epps & Hudson 2017's stacked LRG-pair lensing (arXiv:1702.08485) tell PAPER49 v1.1's 'no saddle
trough' from AQUAL/QUMOND's negative midpoint strip?  Criteria: FROZEN_CRITERIA.md (committed alone, before this script).
All choices favour detection (no EFE suppression, full strip fill, larger AG6C coefficient).  Published numbers only; no data.
Run: python3 ag7.py      AG7_MUTATE=1: trough x100 must read DIAGNOSTIC (exit 1 = bites).   kappa = 1/2 fitted; not theory closed."""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
MUT = os.environ.get("AG7_MUTATE") == "1"; TAG = "_MUTATE" if MUT else ""
OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
FAILS = []
def check(n, ok, d=""):
    P(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f": {d}" if d else "")); (None if ok else FAILS.append(n)); return ok

G, MSUN, PC = 6.674e-11, 1.98847e30, 3.0857e16; MPC = 1e6 * PC; SIG_UNIT = MSUN / PC ** 2      # kg/m^2 per Msun/pc^2
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}; h = 0.7
C_LINE = {"grid h": 0.2064, "h/2 (used, larger)": 0.2158}; STRIP = 0.1                           # |z| <= 0.05 d  ->  0.1 d along the axis
# Epps & Hudson 2017 (verified from the paper text)
N_PAIRS, D_MEAN, D_MIN, DX, DY, M_FIL, SIG_M, LOGMSTAR = 23000, 8.23, 6.0, 7.1, 2.5, 1.6e13, 0.3e13, 11.3
P("AG7 power pre-flight: AQUAL saddle trough vs PAPER49 v1.1 (no trough) in Epps & Hudson 2017's stacked LRG pairs" + ("   *** MUTATE x100 ***" if MUT else ""))
P("kappa = 1/2 fitted; not theory closed. A pre-flight decides only whether the test is possible.")


def sigma_line(Mb_msun, d_mpc, a0, C):
    return C * math.sqrt(Mb_msun * MSUN * a0 / G) / (d_mpc * MPC) / SIG_UNIT * (100.0 if MUT else 1.0)


P("\nControls")
f1 = json.load(open(os.path.join(REPO, "argon_push", "AG6C_relativistic_completion", "ag6c_s0_saddle_results.json")))["numbers"]["fiducials"]["F1_MW-M31_canonical"]["Sigma_neg_AQUAL_Msun_pc2"]
k1 = sigma_line(8e10, 0.77, A0["canonical"], C_LINE["grid h"]) / (100.0 if MUT else 1.0)
check("K1 AG6C F1 AQUAL column reproduced within 1%", abs(k1 / abs(f1) - 1) <= 0.01, f"{k1:.4f} vs {abs(f1):.4f} Msun/pc^2")
A_box = (DX / h) * (DY / h) * 1e12                                            # pc^2
sig_box = SIG_M / A_box; mean_box = M_FIL / A_box
P(f"  K2 (reported): box {DX / h:.2f} x {DY / h:.2f} Mpc; mean filament Sigma {mean_box:.3f} +- {sig_box:.3f} Msun/pc^2 -> {mean_box / sig_box:.1f} sigma (paper: ~5 sigma)")

RES = {"lane": "AG7", "mutate": MUT, "sigma_box": sig_box, "mean_box": mean_box, "rows": []}
P(f"\n{'footing':9s} {'M_b [Msun]':>11s} {'d [h-1 Mpc]':>11s} {'Sigma_line':>10s} {'box mean':>9s} {'S/N box':>8s} {'S/N strip':>9s}")
prim = None
for foot in ("canonical", "alt"):
    for Mb in (10 ** LOGMSTAR, 2e12):
        for dh in (D_MEAN, D_MIN):
            d = dh / h; sl = sigma_line(Mb, d, A0[foot], C_LINE["h/2 (used, larger)"])
            frac = STRIP * d / (DX / h); box_tr = sl * frac
            A_strip = STRIP * d * (DY / h) * 1e12; sig_strip = sig_box * math.sqrt(A_box / A_strip)
            sa, sb = box_tr / sig_box, sl / sig_strip
            row = dict(foot=foot, Mb=Mb, d_hMpc=dh, Sigma_line=sl, box_trough=box_tr, SN_box=sa, SN_strip=sb)
            RES["rows"].append(row)
            if foot == "canonical" and Mb == 10 ** LOGMSTAR and dh == D_MEAN:
                prim = row
            P(f"{foot:9s} {Mb:11.2e} {dh:11.2f} {sl:10.3f} {box_tr:9.4f} {sa:8.2f} {sb:9.2f}")

br = [r for r in RES["rows"] if r["foot"] == "canonical"]
reading = "DIAGNOSTIC" if prim["SN_strip"] >= 3 else ("MARGINAL" if any(r["SN_strip"] >= 3 for r in br) else "NOT DIAGNOSTIC")
N3 = N_PAIRS * (3.0 / prim["SN_strip"]) ** 2
fut = prim["SN_strip"] * math.sqrt(100 * 2)
P(f"\nPRIMARY (canonical, M_b = 10^11.3, d = 8.23 h-1 Mpc): optimistic strip S/N = {prim['SN_strip']:.2f}, box S/N = {prim['SN_box']:.2f}")
P(f"READING: {reading}")
P(f"FORECAST (labelled; optimistic): 3 sigma needs ~{N3:.2e} CFHTLenS-like pairs (x{N3 / N_PAIRS:.0f}); a ~100x pair sample with ~2x source density gives S/N ~ {fut:.1f}")
# reported (added after the first run; no criterion, number or reading changed): AQUAL's NET column and the field near the saddle
import re
m = re.search(r"negative part ([-+0-9.]+), net ([-+0-9.]+)", open(os.path.join(REPO, "argon_push", "AG6C_relativistic_completion", "ag6c_s0_saddle.out")).read())
neg6, net6 = float(m.group(1)), float(m.group(2)); unit = sigma_line(10 ** LOGMSTAR, D_MEAN / h, A0["canonical"], 1.0) / (100.0 if MUT else 1.0)
P(f"REPORTED: AG6C's mid-plane column through the saddle (grid h) is negative part {neg6:+.4f} but NET {net6:+.4f} (dimensionless);")
P(f"  at the primary values that is {neg6 * unit:+.3f} and {net6 * unit:+.3f} Msun/pc^2. AQUAL's own projected column through the saddle is")
P("  POSITIVE: neither model predicts negative convergence there. The separating signal is a dip of depth ~|negative part| in the")
P("  positive bridge (AQUAL) versus no dip (a medium that cannot go below zero, if it keeps the positive part). That is what (a)/(b) size.")
d_m = D_MEAN / h * MPC; R_m = 0.2 * d_m; Mb_kg = 10 ** LOGMSTAR * MSUN
gN = 2 * G * Mb_kg * R_m / ((d_m / 2) ** 2 + R_m ** 2) ** 1.5; g_deep = math.sqrt(A0["canonical"] * gN)
P(f"REPORTED: field in the mid-plane at R = 0.2 d (primary pair, superposed deep-MOND estimate): g ~ {g_deep / A0['canonical']:.1e} a0.")
P("Not included (each weakens the test): any external field above that fills the null point (not modelled); the dip's real profile")
P("  (thinner than the 0.1 d strip, and smeared for pairs not seen edge-on); the d = 6 h-1 Mpc bracket keeps all 23,000 pairs; correlated")
P("  Kaiser-Squires noise; the positive filament and the medium's own departure from the law, which must be modelled to isolate the dip.")
RES.update(reading=reading, primary=prim, N3=N3, future_SN=fut, K1=k1, AG6C_mid_column=dict(negative=neg6, net=net6),
           primary_column_Msun_pc2=dict(negative=neg6 * unit, net=net6 * unit), saddle_field_over_a0=g_deep / A0["canonical"])
if MUT:
    bites = reading == "DIAGNOSTIC"
    P(f"MUTATE (trough x100): {'DIAGNOSTIC -> control BITES (exit 1, as designed)' if bites else 'did NOT bite (recorded)'}")
P(f"controls failed: {FAILS or 'none'}")
json.dump(RES, open(os.path.join(HERE, f"ag7_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"ag7{TAG}.out"), "w").write("\n".join(OUT) + "\n")
sys.exit(1 if (MUT and reading == "DIAGNOSTIC") or FAILS else 0)
