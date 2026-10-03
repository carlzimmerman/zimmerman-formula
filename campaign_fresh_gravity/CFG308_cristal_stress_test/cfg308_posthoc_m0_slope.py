#!/usr/bin/env python3
"""CFG308 POST HOC (written after the MUTATE run's M0 precondition FAILED; not part of the frozen criteria; the FAIL is kept).
M0 asked that d log nu_mono / d log y lie in [-1/2, 0] (tolerance 1e-6) on y in [1e-10, 1e10]; the run found -0.500012.
Question: is that a property of the committed nu_mono implementation (FP1 / L340: 1 + interp(log10 y, table, H_M)/y, a cumulative-trapezoid table
with step 1e-4 in log10 y, linearly interpolated) or an artefact of the finite-difference probe, and does it affect M2 (the >= 2.25^2 rise bound)?
History: the first run of this post hoc script had a wrongly posed P3 (FAIL, kept in cfg308_posthoc_m0_slope_firstrun.out); P3 was then corrected.
Run:  python3 campaign_fresh_gravity/CFG308_cristal_stress_test/cfg308_posthoc_m0_slope.py
"""
import os, sys, io, csv, json, math, contextlib
sys.dont_write_bytecode = True
import numpy as np

LANE = os.path.dirname(os.path.abspath(__file__))
CFG = os.path.dirname(LANE)
OUT, CHK = [], []


def P(s=""):
    print(s, flush=True); OUT.append(s)


def check(name, val, ok):
    CHK.append(bool(ok)); P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


P(__doc__.split("Run:")[0].strip())
F223 = os.path.join(CFG, "CFG223_a0_over_cosmic_time", "cfg223_a0_over_time.py")
src = open(F223).read()
ns = {"__file__": F223, "__name__": "cfg308_posthoc"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(src[:src.index('P("\\nCONTROLS")')], "cfg223", "exec"), ns)
NU, K, A0L = ns["NU"], ns["K"], ns["A0L"]
KNS = K._KNS
LYG, HM = KNS["LYG"], KNS["_HM"]
assert NU is K.nu_mono

# 1. exact piecewise slopes of the committed interpolant (no finite-difference probe): on each table cell [u_k, u_k+1] (u = log10 y), h(u) is linear,
#    so nu = 1 + h(u)/y and d ln nu / d ln y = [h'(u)/ln10 - h] / (y + h) evaluated at both ends of every cell (cells are 1e-4 dex wide).
u0, u1 = LYG[:-1], LYG[1:]
h0, h1 = HM[:-1], HM[1:]
hp = (h1 - h0) / (u1 - u0)
y0, y1 = 10 ** u0, 10 ** u1
s_left = (hp / math.log(10) - h0) / (y0 + h0)
s_right = (hp / math.log(10) - h1) / (y1 + h1)
smin = np.minimum(s_left, s_right); smax = np.maximum(s_left, s_right)
P("\n1. EXACT PIECEWISE LOG-SLOPES OF THE COMMITTED nu_mono INTERPOLANT (both ends of each of the 280,000 table cells)")
P(f"  over the whole table (y 1e-14..1e14): min {smin.min():.7f} at y {y0[np.argmin(smin)]:.3e}; max {smax.max():.2e}")
for lo, hi in ((1e-14, 1e-6), (1e-6, 1e-3), (1e-3, 1e5), (1e5, 1e14)):
    m = (y0 >= lo) & (y1 <= hi)
    P(f"  y in [{lo:.0e}, {hi:.0e}]: min slope {smin[m].min():.7f}, excess below -1/2: {max(0.0, -0.5 - smin[m].min()):.2e}")
exc = max(0.0, -0.5 - smin.min())
P(f"  -> the committed kernel's log-slope reaches -(1/2 + {exc:.1e}) at the lower end of its table cells in the deep-MOND tail: the chord of h ~ sqrt(y) over a"
  f" 1e-4-dex cell, linearly interpolated in log y, is steeper than 1/2 at the cell's left end by about (ln10 x 1e-4)/8 = {math.log(10) * 1e-4 / 8:.1e}")
check("P1 the M0 excess is a property of the committed interpolant (exact cell-end slopes reach below -1/2) and is below 1e-4 everywhere",
      f"excess {exc:.2e}", 0 < exc < 1e-4)
fd_y = np.geomspace(1e-10, 1e10, 400001)
fd = np.diff(np.log(NU(fd_y))) / np.diff(np.log(fd_y))
check("P2 the run's finite-difference probe (400,001 points, 1e-10..1e10) reproduces M0's -0.500012 and lies within the exact cell-end range",
      f"probe min {fd.min():.7f}; exact min {smin.min():.7f}", abs(fd.min() + 0.5000119) < 2e-6 and fd.min() >= smin.min() - 1e-9)

# 2. the y range the grid actually uses: y = g_bar / (a0 s) over the grid's g_bar and s in [1e-3, 1e3]
P("\n2. THE y RANGE THE GRID USES, AND THE M2 BOUND WITH THE MEASURED SLOPE")
# the exact g_bar span of the grid: every disc of the nine at R_e and at its outermost marker, lightest (stars only, M* -0.15) and heaviest
# (M* +0.15 plus the largest gas level: f + errhi for detections, the [CII] alpha 60 for CRISTAL-20 if larger, the table limit for the upper-limit discs)
F216 = os.path.join(CFG, "CFG216_rc100_within_sample", "cfg216_rc100.py")
s216 = open(F216).read()
n216 = {"__file__": F216, "__name__": "cfg308_posthoc"}
with contextlib.redirect_stdout(io.StringIO()):
    exec(compile(s216[:s216.index("# " + "-" * 96 + " data\n")], "cfg216", "exec"), n216)
kin = {r["id"]: r for r in csv.DictReader(open(os.path.join(os.path.dirname(CFG), "data_assembly", "arxiv_tables", "cristal2025_kinematics.csv"), newline=""))}
L20 = float({r["gid"]: r for r in csv.DictReader(open(os.path.join(CFG, "CFG228_alma_cubes", "cfg228_stage1_alpine_measurements.csv"), newline=""))}["DC494057"]["L_CII"])
vr = ns["n220"]["vec_rows"]("outermost_data_marker")
gbs = []
for i in ["02", "03", "07a", "08", "11", "12", "19", "20", "23b"]:
    g = ns["crbyid"][i]; Ms = 10 ** g["logMstar"]; f = g["f_molgas"]
    if i in ("08", "12", "23b"):
        Mg = Ms * f / (1 - f)
    else:
        fh = f + float(kin[i]["errhi"]); Mg = max(Ms * fh / (1 - fh), 60.0 * L20 if i == "20" else 0.0)
    for R in (g["Re"], vr[i][0]):
        x = n216["disc_v2"](1.0, g["Re"], R) / R * n216["G2SI"]
        gbs += [Ms * 10 ** -0.15 * x, (Ms * 10 ** 0.15 + Mg) * x]
gb_lo, gb_hi = min(gbs), max(gbs)
ylo, yhi = gb_lo / (A0L * 1e3), gb_hi / (A0L * 1e-3)
m = (y1 >= ylo) & (y0 <= yhi)
P(f"  exact g_bar span of the grid {gb_lo:.2e}..{gb_hi:.2e} m/s^2 with s in [1e-3, 1e3] -> y {ylo:.1e}..{yhi:.1e}; min exact slope there {smin[m].min():.7f}")
smin_used = smin[m].min()
bound = 10 ** (math.log10(2.25) / -smin_used)
mut = json.load(open(os.path.join(LANE, "cfg308_cristal_stress_MUTATE_results.json")))["mutate"]["M2"]
P(f"  M2 bound with the measured slope: 2.25^(1/{-smin_used:.7f}) = {bound:.5f} (frozen 5.0625); observed minimum rise {mut['factor_min']:.3f} over {mut['n_root']} roots")
check("P3 (corrected after the first post hoc run, whose P3 wrongly expected the deep tail inside the used range and FAILED; kept in "
      "cfg308_posthoc_m0_slope_firstrun.out) over the y range the grid uses the kernel's log-slope never goes below -1/2, so the frozen 5.0625 bound is "
      "conservative there, and every observed rise exceeds the tighter used-range bound",
      f"min slope over used range {smin_used:.7f} (>= -0.5); used-range bound {bound:.5f} >= 5.0625; min observed {mut['factor_min']:.3f}; M2 {mut['n_ok']}/{mut['n_root']}",
      smin_used >= -0.5 and bound >= 5.0625 and mut["factor_min"] > bound)
P(f"\n{sum(CHK)}/{len(CHK)} checks pass (post hoc; the frozen M0 FAIL stands as recorded)")
json.dump(dict(posthoc=True, excess_below_half=exc, exact_min_slope=float(smin.min()), probe_min_slope=float(fd.min()), y_used=[ylo, yhi], min_slope_used=float(smin_used),
               m2_bound_measured=bound, m2_observed_min=mut["factor_min"], checks=dict(passed=sum(CHK), n=len(CHK))),
          open(os.path.join(LANE, "cfg308_posthoc_m0_slope_results.json"), "w"), indent=1)
open(os.path.join(LANE, "cfg308_posthoc_m0_slope.out"), "w").write("\n".join(OUT) + "\n")
