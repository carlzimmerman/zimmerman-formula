#!/usr/bin/env python3
"""CN1 POST-RESULT, reported only: how much net response can the clusters take? No contraction anywhere; collapse-branch cluster S multiplied by a stated net factor R_c, SPARC and groups as FC1.
R_c 1.126 = cold concentration +10 % through eta ~ c^(5/4), the size non-radiative hydro runs report for dust + gas (Rasia+04, Lin+06; literature value, not an input to any grade).
R_c 1 must reproduce FC1's cluster numbers. kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); CE1 = os.path.join(RB, "CE1_converged_eta_grade"); SLOPE = "2.7774425603108597"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
T = open(os.path.join(HERE, "cn1_x74.py")).read()
for a, b in (('if a_ and ETA_USE["v"] == ETA and CN1_MODE != "off":\n            M2 = M200 * MSUNE', 'if False:\n            M2 = M200 * MSUNE'),
             ('Mbf = pp["Mb"] + BCGF[int(i)] * MSUNE * RM ** 2 / (RM + 10 * 3.0857e19) ** 2', 'Mbf = pp["Mb"]'),
             ('Mf_, _c, _x = contract(RM, Mbf, M0, Fc_, gnedin=(0.85, 0.8, pp["rta"]) if CN1_MODE == "gnedin" else None)', 'Mf_ = M0')):
    assert T.count(a) == 1, a; T = T.replace(a, b)
WD = os.path.join(RB, "_cn1c_work"); os.makedirs(WD, exist_ok=True)
open(os.path.join(WD, "cn1c_x74.py"), "w").write(T.replace('HERE = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(HERE)', f'HERE = {WD!r}; REB = {RB!r}'))
def grade(tag, Rc, fs):
    names = [f"x74_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.out", f"x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json"]
    env = dict(os.environ, CN1_R=str(Rc), CN1_MODE="blum", X74_CF=os.path.join(CE1, f"CE1_med_fs{fs}_cf_table.json"), X73_FSTAR=fs, X73_SLOPE=SLOPE, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    p = subprocess.run(["nice", "-n", "15", sys.executable, "cn1c_x74.py"], cwd=WD, env=env, capture_output=True, text=True); out = {}
    for n in names:
        f = os.path.join(WD, n)
        if os.path.exists(f):
            if f.endswith(".json"): out = json.load(open(f))
            os.remove(f)
    if not out: raise SystemExit(f"NOT DECIDED: {tag} wrote no results (exit {p.returncode}): {p.stderr[-400:]}")
    return out
RES = {}
for fs, Rc in (("0.034", 1.0), ("0.034", 0.9), ("0.034", 0.95), ("0.034", 1.05), ("0.034", 1.126), ("0.0615", 1.0), ("0.0615", 1.126)):
    o = grade(f"Rc{Rc}_fs{fs}", Rc, fs); key = f"Rc{Rc:g}_fs{fs}"; RES[key] = {}
    for f in ("canonical", "alt"):
        F = o["footings"][f]; c = F["clusters"]["cells"]; z = {hk: {kk: v["Z"] for kk, v in c[hk].items()} for hk in c}; w = max(((kk, hk, zz) for hk in z for kk, zz in z[hk].items()), key=lambda t: abs(t[2]))
        bad = sorted({kk for hk in z for kk, zz in z[hk].items() if abs(zz) > 2})
        RES[key][f] = dict(inmall=z["h0672"]["G-IN-Mall"], t3=z["h0672"]["G-MID-T3"], m3=z["h0672"]["G-OUT-M3"], out_all=z["h0672"]["G-OUT-all"], worst=w, keys_over_2=bad)
        r = RES[key][f]; P(f"  R_c {Rc:g} f* {fs} [{f}] G-IN-Mall {r['inmall']:+.2f}; G-MID-T3 {r['t3']:+.2f}; G-OUT-M3 {r['m3']:+.2f}; G-OUT-all {r['out_all']:+.2f}; worst {w[0]} {w[1]} {w[2]:+.2f}; keys over |Z| 2: {bad}")
F1 = json.load(open(os.path.join(RB, "FC1_cold_share_native_eta", "FC1_med_fs0.034_x74_results_fs0.034_nat_s2.7774.json"))) if os.path.exists(os.path.join(RB, "FC1_cold_share_native_eta", "FC1_med_fs0.034_x74_results_fs0.034_nat_s2.7774.json")) else None
if F1:
    d = max(abs(F1["footings"][f]["clusters"]["cells"]["h0672"][k]["Z"] - RES["Rc1_fs0.034"][f][n]) for f in ("canonical", "alt") for k, n in (("G-IN-Mall", "inmall"), ("G-MID-T3", "t3")))
    P(f"K R_c 1 reproduces FC1's cluster Z: max |d| {d:.1e}: {'PASS' if d <= 1e-9 else 'FAIL'}")
json.dump(RES, open(os.path.join(HERE, "cn1c_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, "cn1c.out"), "w").write("\n".join(OUT) + "\n"); shutil.rmtree(WD, ignore_errors=True)
