#!/usr/bin/env python3
"""XH1_xcop_native_rule (criteria 530debe21b): FC1's rule, unchanged, on X-COP's hydrostatic masses; HO1's pass line. Each run is FC1's full grader with xh1_tail.py in place of its last line.
    python3 xh1_xcop.py            # graded runs, what-ifs
    python3 xh1_xcop.py --mutate   # S x 2, separate outputs
    python3 xh1_xcop.py --A4       # same grade on CE1's A4 tables, separate outputs
kappa = 1/2 FITTED; footings never pooled; not theory closed."""
import json, math, os, re, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); SLOPE = "2.7774425603108597"
CE1 = os.path.join(RB, "CE1_converged_eta_grade"); FC1 = os.path.join(RB, "FC1_cold_share_native_eta")
if "--worker" in sys.argv:
    X74F = os.path.join(RB, "X74_all_measured_native_cf", "x74_native_cf.py"); TX = open(X74F).read()
    INJ = re.search(r"INJ = r'''(.*?)'''", open(os.path.join(FC1, "fc1_x74.py")).read(), re.S).group(1)
    MY = 'sub("sys.exit(0 if (n == len(checks) and x74ok) else 1)", open(os.path.join(HERE, "xh1_tail.py")).read())\n'
    A = "sys.argv = [SRC]\n"; assert TX.count(A) == 1; TX = TX.replace(A, INJ + MY + A); sys.argv = [X74F]
    exec(compile(TX, X74F, "exec"), {"__file__": os.path.join(HERE, "x74_native_cf.py"), "__name__": "__main__"})
MUT = "--mutate" in sys.argv; A4 = "--A4" in sys.argv; PRE = "CE1_A4" if A4 else "CE1"; TAG = "xh1_MUTATE" if MUT else "xh1_a4" if A4 else "xh1"; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
P(f"XH1 {TAG}: FC1's rule on X-COP (35 points, M_FORW); pass |mean| <= 0.05, rms <= 0.10; Delta > 0 = model too light; kappa = 1/2 FITTED; footings never pooled; not theory closed" + ("" if A4 else " [cluster masses ng 48]"))
TD = tempfile.mkdtemp()
def run(fs, g=1.0, smult=1.0, k0=False):
    T = json.load(open(os.path.join(CE1, f"{PRE}_med_fs{fs}_cf_table.json")))
    for k in ("1e+13", "1e+14"): T["cf_by_mass"][k] *= g ** 0.8   # eta ~ c^(5/4)
    t = os.path.join(TD, f"t_{fs}_{g:g}_{smult:g}.json"); json.dump(T, open(t, "w")); o = os.path.join(TD, f"o_{fs}_{g:g}_{smult:g}.json")
    env = dict(os.environ, FC1_MODE="cold", X74_CF=t, X73_FSTAR=fs, X73_SLOPE=SLOPE, XH1_OUT=o, XH1_SMULT=str(smult), PYTHONHASHSEED="0", OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    env.pop("XH1_K0_REF", None)
    if k0: env["XH1_K0_REF"] = os.path.join(FC1, f"FC1_med_fs{fs}_x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json")
    p = subprocess.run(["nice", "-n", "15", sys.executable, os.path.abspath(__file__), "--worker"], cwd=HERE, env=env, capture_output=True, text=True)
    if not os.path.exists(o): raise SystemExit(f"NOT DECIDED: f* {fs} g {g} wrote no result (exit {p.returncode}): {p.stderr[-600:]}")
    for n in (f"x74_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.out", f"x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json"):
        if os.path.exists(os.path.join(HERE, n)): os.remove(os.path.join(HERE, n))
    return json.load(open(o))
ok_ = lambda r: abs(r["mean"]) <= 0.05 and r["rms"] <= 0.10
def why(r):
    w = ([] if abs(r["mean"]) <= 0.05 else ["mean"]) + ([] if r["rms"] <= 0.10 else ["rms"])
    return "PASS" if not w else "FAIL (" + "+".join(w) + (", model too heavy)" if r["mean"] < 0 else ", model too light)")
def row(tag, r):
    b = r["band"]; P(f"  {tag}: mean {r['mean']:+.3f} rms {r['rms']:.3f} n {r['n']} sat {r['saturated']} floor {r['on_floor']} -> {why(r)}; by x " + " ".join(f"{k} {v:+.3f}" for k, v in r["by_x"].items()) + f"; band 0.15-0.46 Mpc n {b['n']} mean {b['mean']:+.3f} model/data {b['R_X']:.3f}")
def band_label(r): return "SHEAR BAND OUTLIER" if r["band"]["R_X"] <= 1.25 else "INNER OVER CONFIRMED" if r["band"]["R_X"] >= 1.5 else "IN BETWEEN"
if MUT:
    b = run("0.034"); m = run("0.034", smult=2.0); row("base f* 0.034", b["footings"]["canonical"]); row("S x 2", m["footings"]["canonical"]); dm = m["footings"]["canonical"]["mean"] - b["footings"]["canonical"]["mean"]
    bites = abs(dm) > 0.02; P(f"MUTATE moves mean by {dm:+.3f}: {'BITES' if bites else 'INSENSITIVE, lane UNDECIDED'}")
    json.dump(dict(base=b["footings"]["canonical"]["mean"], mut=m["footings"]["canonical"]["mean"], bites=bites), open(os.path.join(HERE, f"{TAG}.json"), "w"), indent=1); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(0 if bites else 1)
RES = dict(runs={}, checks={}); FS = ("0.034", "0.0615"); B0 = {fs: run(fs, k0=not A4) for fs in FS}
for fs in FS:
    RES["runs"][f"g1_fs{fs}"] = B0[fs]
    for f in ("canonical", "alt"): row(f"f* {fs} [{f}]", B0[fs]["footings"][f])
good = True
for fs in FS:
    R = B0[fs]; F = R["footings"]
    ck = dict(K1=R["k1_cs2"] <= 1e-9 and all(R["cs2_blockchecks"].values()), K2=max(F[f]["k2"] for f in F) <= 1e-8, K3=max(F[f]["k3"] for f in F) <= 1e-4, K4=max(F[f]["k4"] for f in F) <= 1e-9, shape=abs(R["B1"] - 4 * (math.asinh(1) - 1 / math.sqrt(2))) < 1e-12)
    if not A4: ck["K0"] = R["k0"] <= 1e-9
    RES["checks"][fs] = ck; good &= all(ck.values())
    P(f"checks f* {fs}: " + ", ".join(f"{k} {'PASS' if v else 'FAIL'}" for k, v in ck.items()) + f"; K0 |d| {R.get('k0', float('nan')):.1e}, K1 {R['k1_cs2']:.1e}, K2 {max(F[f]['k2'] for f in F):.1e}, K3 {max(F[f]['k3'] for f in F):.1e}, K4 {max(F[f]['k4'] for f in F):.1e}, RSS {R['rss_gb']:.2f} GB")
if not good: P("A CHECK FAILED: no verdict"); json.dump(RES, open(os.path.join(HERE, f"{TAG}_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n"); sys.exit(1)
def verdict(f):
    n = [fs for fs in FS if ok_(B0[fs]["footings"][f])]
    return "X-COP PASS" if len(n) == 2 else f"F*-DEPENDENT (passes at {n[0]})" if n else "X-COP FAIL: " + "; ".join(f"{fs} {why(B0[fs]['footings'][f])}" for fs in FS)
V = {f: verdict(f) for f in ("canonical", "alt")}; RES["verdict"] = V["canonical"] if V["canonical"] == V["alt"] else f"FOOTING-SPLIT: canonical {V['canonical']}; alt {V['alt']}"
P(("A4 READ: " if A4 else "VERDICT: ") + RES["verdict"])
HJ = json.load(open(os.path.join(RB, "HO1_xcop_hotgas_heldout", "ho1_heldout_results.json")))["footings"]["canonical"]["xcop"]; CJ = json.load(open(os.path.join(RB, "CS2_core_law_out_of_sample", "cs2_out_of_sample_results.json")))["footings"]
P(f"comparators: HO1 mean {HJ['mean']:+.3f} rms {HJ['rms']:.3f}, by x " + " ".join(f"{k} {v:+.3f}" for k, v in HJ["by_x"].items()) + f"; OS1 rms {CJ['canonical']['OS1']['xcop']['rms']:.3f} canonical, {CJ['alt']['OS1']['xcop']['rms']:.3f} alt; CS2 law rms {CJ['canonical']['CS2']['xcop']['rms']:.3f}")
for fs in FS:
    c = json.load(open(os.path.join(FC1, f"FC1_med_fs{fs}_x74_results_fs{float(fs):g}_nat_s{float(SLOPE):.4f}.json")))["footings"]["canonical"]["clusters"]["cells"]["h0672"]["G-IN-Mall"]
    r = B0[fs]["footings"]["canonical"]; RES.setdefault("band", {})[fs] = dict(R_X=r["band"]["R_X"], shear_pred_over_meas=c["pred"] / c["meas"], label=band_label(r))
    P(f"disputed band f* {fs}: X-COP model/data {r['band']['R_X']:.3f} (n {r['band']['n']}), G-IN-Mall pred/meas {c['pred'] / c['meas']:.2f}: {band_label(r)}")
P("per cluster, f* 0.034 canonical: " + "; ".join(f"{k} mean {v:+.3f} S {B0['0.034']['footings']['canonical']['info'][k]['S_pc2']:.0f} r0 {B0['0.034']['footings']['canonical']['info'][k]['r0_kpc']:.0f} kpc" for k, v in B0["0.034"]["footings"]["canonical"]["per_cluster"].items()))
if not A4:
    for fs in FS:
        for g in (0.90, 1.1144): r = run(fs, g=g); RES["runs"][f"g{g:g}_fs{fs}"] = r; row(f"what-if g {g:g} f* {fs}", r["footings"]["canonical"])
json.dump(RES, open(os.path.join(HERE, f"{TAG}_results.json"), "w"), indent=1, default=float); open(os.path.join(HERE, f"{TAG}.out"), "w").write("\n".join(OUT) + "\n")
