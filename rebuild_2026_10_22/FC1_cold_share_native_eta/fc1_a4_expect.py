#!/usr/bin/env python3
"""FC1: what A4 could do to the edge, on record before A4's grade exists. Reported, not a grade; A4's own label (fc1_grade.py --A4) stands.
Grades FC1's rule with eta at 1e13 and 1e14 scaled by g and 1e12 unchanged, then sets the result against how far ng 48 -> 64 moved converged eta at 1e12.
Reads no A4 snapshot: 1e12 per-run eta from X80's check, CE1's ng 48 cluster tables.
    python3 fc1_a4_expect.py   kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, subprocess, sys, tempfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); CE1 = os.path.join(RB, "CE1_converged_eta_grade"); SLOPE = "2.7774425603108597"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P("FC1 before A4: eta at 1e13, 1e14 x g, 1e12 unchanged; canonical, X74's grader; reported, not a grade; kappa = 1/2 FITTED; footings never pooled; not theory closed")
# How far the grid moved converged eta at 1e12. X48 redraws the field at each ng, so these are two samples, not pairs.
S = json.load(open(os.path.join(RB, "X80_low_mass_floor_emergence", "x80_converged.json")))["summary"]
a48, a64 = np.array(S["1e+12_ng48"]["per_run"]), np.array(S["1e+12_ng64"]["per_run"]); shift = float(np.median(a64) / np.median(a48))
G = np.random.default_rng(20261031); med = lambda A: np.median(A[G.integers(0, len(A), (100000, len(A)))], axis=1); r = med(a64) / med(a48)
P(f"1e12 converged eta: ng 48 {np.median(a48):.2f}, ng 64 {np.median(a64):.2f}, ratio {shift:.4f} [68% {np.percentile(r, 16):.3f}, {np.percentile(r, 84):.3f}; 95% {np.percentile(r, 2.5):.3f}, {np.percentile(r, 97.5):.3f}]")
TD = tempfile.mkdtemp(); RES = dict(shift_1e12=shift, shift_68=[float(np.percentile(r, 16)), float(np.percentile(r, 84))], runs={})
def grade(g, fs):
    T = json.load(open(os.path.join(CE1, f"CE1_med_fs{fs}_cf_table.json"))); c = T["cf_by_mass"]
    for k in ("1e+13", "1e+14"): c[k] *= g ** 0.8   # eta ~ c^(5/4)
    t = os.path.join(TD, f"g{g:g}_fs{fs}.json"); json.dump(T, open(t, "w"))
    env = dict(os.environ, FC1_MODE="cold", X74_CF=t, X73_FSTAR=fs, X73_SLOPE=SLOPE, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    p = subprocess.run(["nice", "-n", "15", sys.executable, "fc1_x74.py"], cwd=HERE, env=env, capture_output=True, text=True); o = {}
    for n in (f"x74_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.out", f"x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json"):
        f = os.path.join(HERE, n)
        if os.path.exists(f):
            if f.endswith(".json"): o = json.load(open(f))
            os.remove(f)
    if not o: raise SystemExit(f"NOT DECIDED: g {g} f* {fs} wrote no results (exit {p.returncode}): {p.stderr[-400:]}")
    F = o["footings"]["canonical"]; s = F["sparc"]; c = F["clusters"]["cells"]; line = all(v["line"] for v in s.values()); bad = sorted({k for h in c for k, v in c[h].items() if abs(v["Z"]) > 2})
    d = dict(U=[s["A_c2b_refit"]["U_median"], s["B_cfg886_bg"]["U_median"]], rms=s["A_c2b_refit"]["rms"], sparc_line=line, groupsZ=F["groups"]["Z"], inmall=[c["h0672"]["G-IN-Mall"]["Z"], c["h0686"]["G-IN-Mall"]["Z"]], t3=[c["h0672"]["G-MID-T3"]["Z"], c["h0686"]["G-MID-T3"]["Z"]], keys_over_2=bad, failing=F["failing"])
    d["passes"] = bool(line and not F["failing"]); RES["runs"][f"g{g:g}_fs{fs}"] = d
    P(f"  g {g:.4f} f* {fs}: {'PASS' if d['passes'] else 'FAIL'}; SPARC U {d['U'][0]:.3f}/{d['U'][1]:.3f} rms {d['rms']:.4f} line {line}; groups Z {d['groupsZ']:+.2f}; G-IN-Mall {d['inmall'][0]:+.3f}/{d['inmall'][1]:+.3f}; G-MID-T3 {d['t3'][0]:+.3f}/{d['t3'][1]:+.3f}; keys over 2: {bad}"); return d
GRID = [0.90, 0.95, 1.0, 1.015, 1.05, 1.08, shift]; R34 = {g: grade(g, "0.034") for g in GRID}; R61 = {g: grade(g, "0.0615") for g in (0.95, 1.0, shift)}
# K: g 1 must reproduce FC1's frozen grade exactly.
good = True
for fs, R in (("0.034", R34), ("0.0615", R61)):
    F = json.load(open(os.path.join(HERE, f"FC1_med_fs{fs}_x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json")))["footings"]["canonical"]; c = F["clusters"]["cells"]
    d = max(abs(c["h0672"]["G-IN-Mall"]["Z"] - R[1.0]["inmall"][0]), abs(c["h0672"]["G-MID-T3"]["Z"] - R[1.0]["t3"][0]), abs(F["sparc"]["B_cfg886_bg"]["U_median"] - R[1.0]["U"][1])); ok = d <= 1e-9; good &= ok
    P(f"K g 1 reproduces FC1 at f* {fs}: max |d| {d:.1e}: {'PASS' if ok else 'FAIL'}")
gs = sorted(GRID); z = [R34[g]["inmall"][0] for g in gs]; cross = float(np.interp(2.0, [-q for q in z], gs)); first_fail = min((g for g in gs if not R34[g]["passes"]), default=None)
RES.update(cross_inmall=cross, first_fail_on_grid=first_fail, P_shift_le_cross=float(np.mean(r <= cross)), K=bool(good))
P(f"G-IN-Mall reaches -2 at f* 0.034 at g {cross:.3f}; lowest failing g on this grid {first_fail}; the 1e12 bootstrap puts {np.mean(r <= cross):.2f} of its ratios at or below that g")
P("Limits: 1e12's shift stands in for two other masses; the bootstrap is two small samples of different fields; nothing here reads A4.")
json.dump(RES, open(os.path.join(HERE, "fc1_a4_expect.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "fc1_a4_expect.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if good else 1)
