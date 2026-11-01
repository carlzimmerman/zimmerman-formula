#!/usr/bin/env python3
"""NR1 (FROZEN_CRITERIA.md): version N on SPARC with eta(1e12) at ng 80, through NF1's grader, whose files are read only. Temporary outputs in NF1's directory are moved here at once.
    python3 nr1.py          # K1, K2, four runs, MUTATE
kappa = 1/2 FITTED; no a0 in the cold sector; not theory closed."""
import json, math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); NF = os.path.join(RB, "NF1_no_floor_rule"); CE1 = os.path.join(RB, "CE1_converged_eta_grade"); X81P = os.path.join(RB, "X81_core_convergence", "x80_core_convergence.py"); SLOPE = "2.7774425603108597"; FS = "0.034"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
c_of = lambda e: 4 * (e / 10.82) ** 0.8   # CE1's map (AMENDMENT A1)
T0 = json.load(open(os.path.join(CE1, f"CE1_A4_med_fs{FS}_cf_table.json")))["cf_by_mass"]; ETA10, ETA11 = 29.26, 24.34; NAMES = [f"x74_fs{float(FS):g}_nat_s{float(SLOPE):.4f}.out", f"x74_results_fs{float(FS):g}_nat_s{float(SLOPE):.4f}.json"]
ETACK = []
def run(tag, eta12, r10, r11, T=T0):
    tab = os.path.join(HERE, f"{tag}_cf_table.json"); json.dump(dict(note=tag, cf_by_mass={"1e+12": c_of(eta12), "1e+13": T[ "1e+13"], "1e+14": T["1e+14"]}), open(tab, "w"), indent=1)
    env = dict(os.environ, CN1_R="1.0", CN1_MODE="off", NF1_ON="1", NF1_TAB=json.dumps([math.log10(r10), math.log10(r11), 0.0]), X74_CF=tab, X73_FSTAR=FS, X73_SLOPE=SLOPE, PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    saved = {n: open(os.path.join(NF, n), "rb").read() for n in NAMES if os.path.exists(os.path.join(NF, n))}; o = {}
    try:
        p = subprocess.run(["nice", "-n", "5", sys.executable, "nf1_x74.py"], cwd=NF, env=env, capture_output=True, text=True); open(os.path.join(HERE, f"{tag}.log"), "w").write(p.stdout + p.stderr)
        for n in NAMES:
            f = os.path.join(NF, n)
            if os.path.exists(f):
                d = os.path.join(HERE, f"{tag}_{n}"); os.replace(f, d)
                if d.endswith(".json"): o = json.load(open(d)); o["x74"]["cf_src"] = os.path.basename(o["x74"]["cf_src"]); json.dump(o, open(d, "w"), indent=1)
    finally:
        for n, b in saved.items(): open(os.path.join(NF, n), "wb").write(b)
    if not o: raise SystemExit(f"NOT DECIDED: {tag} wrote no result (exit {p.returncode}): {p.stderr[-500:]}")
    ETACK.append(abs(o["x74"]["eta"]["1e12"] - eta12))
    return o
def line(lab, o):
    s = o["footings"]["canonical"]["sparc"]; q = {t: (v["U_median"], v["rms"], v["line"]) for t, v in s.items()}; P(f"  {lab}: " + "; ".join(f"{t} U {v[0]:.3f} rms {v[1]:.4f} line {'PASS' if v[2] else 'FAIL'}" for t, v in q.items()) + f"; groups Z {o['footings']['canonical']['groups']['Z']:+.2f}; failing {o['footings']['canonical']['failing']}"); return q
P("NR1: version N at ng 80's eta(1e12); kappa = 1/2 FITTED; not theory closed")
E0 = json.load(open(os.path.join(CE1, "ce1_a4_results.json")))["eta"]["12"]["med"]; ck = c_of(E0); k1 = abs(ck - T0["1e+12"]) <= 1e-3; P(f"K1 formula at 25.937: {ck:.5f} against {T0['1e+12']:.5f}: {'PASS' if k1 else 'FAIL'}")
TA3 = json.load(open(os.path.join(CE1, f"CE1_med_fs{FS}_cf_table.json")))["cf_by_mass"]; K = run("NR1_K2", E0, 1.0, 1.0, TA3); N0 = json.load(open(os.path.join(NF, f"NF1_N0_x74_results_fs{FS}_nat_s2.7774.json")))["footings"]; dk = 0.0
for f in ("canonical", "alt"):
    for t, v in K["footings"][f]["sparc"].items(): dk = max(dk, abs(v["U_median"] - N0[f]["sparc"][t]["U_median"]), abs(v["rms"] - N0[f]["sparc"][t]["rms"]))
    for hk, c in K["footings"][f]["clusters"]["cells"].items():
        for k, w in c.items(): dk = max(dk, abs(w["pred"] - N0[f]["clusters"]["cells"][hk][k]["pred"]))
k2 = dk <= 1e-9; P(f"K2 A3 table, rho 1, 1 against NF1_N0: max |d| {dk:.1e}: {'PASS' if k2 else 'FAIL'}")
XN = json.load(open(os.path.join(RB, "X80_low_mass_floor_emergence", "x80_converged.json"))); K3 = run("NR1_K3", E0, XN["r10"], XN["r11"]); NN = json.load(open(os.path.join(NF, f"NF1_NATIVE_x74_results_fs{FS}_nat_s2.7774.json")))["footings"]["canonical"]["sparc"]; d3 = max(max(abs(v["U_median"] - NN[t]["U_median"]), abs(v["rms"] - NN[t]["rms"])) for t, v in K3["footings"]["canonical"]["sparc"].items()); k3 = d3 <= 1e-9; P(f"K3 A4 table, rho {XN['r10']:.3f}, {XN['r11']:.3f} against NF1_NATIVE: max |d| {d3:.1e}: {'PASS' if k3 else 'FAIL'}")
E = 21.53; RUNS = dict(PRIMARY=(E, ETA10 / E, ETA11 / E), ALT=(E, 1.128, 0.938), LOW=(14.55, ETA10 / 14.55, ETA11 / 14.55), HIGH=(24.89, ETA10 / 24.89, ETA11 / 24.89)); RES = {}
for t, a in RUNS.items(): RES[t] = line(f"{t} eta12 {a[0]}, rho {a[1]:.3f}, {a[2]:.3f}, c_f(1e12) {c_of(a[0]):.3f}", run(f"NR1_{t}", *a))
M = line("MUTATE eta12 x 0.5, rho 1.359, 1.131", run("NR1_MUTATE", E / 2, ETA10 / E, ETA11 / E)); dm = abs(M["A_c2b_refit"][0] - RES["PRIMARY"]["A_c2b_refit"][0]); mt = dm > 0.02; P(f"MUTATE moves U by {dm:.3f}: {'BITES' if mt else 'INSENSITIVE'}")
ke = max(ETACK); P(f"K1 grader eta(1e12) against intended, every run: max |d| {ke:.1e}: {'PASS' if ke <= 0.01 else 'FAIL'}"); ok = k1 and k2 and k3 and mt and ke <= 0.01; L = lambda r: all(v[2] for v in RES[r].values()); V = "NOT DECIDED" if not ok else ("N PASSES AT NG 80" if L("PRIMARY") else "N FAILS AT NG 80") + (" [ANCHOR-DEPENDENT]" if L("ALT") != L("PRIMARY") else "") + (" [NOISE-LIMITED]" if (L("LOW") != L("PRIMARY") or L("HIGH") != L("PRIMARY")) else ""); P("VERDICT: " + V)
json.dump(dict(verdict=V, runs=RES, K1=ck, K2=dk, K3=d3, mutate=dm), open(os.path.join(HERE, "nr1_results.json"), "w"), indent=1); open(os.path.join(HERE, "nr1.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if ok else 1)
