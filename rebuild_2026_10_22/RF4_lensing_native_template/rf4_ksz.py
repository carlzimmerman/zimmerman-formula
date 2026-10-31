#!/usr/bin/env python3
"""RF4_lensing_native_template (criteria 5632124ef4) G4: GH10's published DR2 kSZ points, GH11's text unchanged through its templates and checks, with f = 0.28, measured sigma_off, three same-halo holes. Run after rf4_grade.py (reads sigma_off and k*).
    PYTHONHASHSEED=0 OMP_NUM_THREADS=1 nice -n 15 python3 -I rf4_ksz.py
kappa = 1/2 FITTED; c_f EXTERNAL; not theory closed; nothing here says the data favour the framework."""
import os, sys, json, math
os.environ["OMP_NUM_THREADS"] = "1"
RF4 = os.path.dirname(os.path.abspath(__file__)); REB = os.path.dirname(RF4); F = os.path.join(REB, "GH11_ksz_two_halo_miscentring", "gh11.py"); T = open(F).read(); CUT = 'KS = (1.0, 1.8, 3.0, 5.0, 8.0)'; assert T.count(CUT) == 1
__file__ = F; exec(compile(T[:T.index(CUT)], F, "exec"))
SO = json.load(open(os.path.join(RF4, "rf4_miscentring.json")))["sigma_off_Mpc"] * 1e3; RJ = json.load(open(os.path.join(RF4, "rf4_results.json"))); KST = RJ["kstar"]; print(f"sigma_off {SO:.0f} kpc; k* {KST}", flush=True)
O = dict(sigma_off_kpc=SO, checks=RES["checks"], holes={}, rows={})
Tn25, _ = template("n", 250.); Hs = {"1000": Tn, "500": Tn5, "250": Tn25}; norm = lambda t: t / np.abs(t).max()
m18 = model(1.8, .28, SO); m1 = model(1.0, .28, SO)
for h_, t_ in Hs.items():
    f_ = fit(m18, norm(t_)); O["holes"][h_] = dict(A=f_["A"], s=f_["s"], b=f_["b"], sb=f_["sb"], chi2=f_["chi2"], p=f_["p"]); print(f"hole {h_} kpc: A(1.8) {f_['A']:.3f}+-{f_['s']:.3f}, b {f_['b']:.2f}+-{f_['sb']:.2f}, chi2 {f_['chi2']:.1f}", flush=True)
As = [O["holes"][h]["A"] for h in Hs]; sa = O["holes"]["1000"]["s"]; h1 = O["holes"]["1000"]; built = (max(As) - min(As) < sa) and (h1["sb"] > 0 and h1["b"] / h1["sb"] >= 2); O["ksz_two_halo"] = "BUILT" if built else "two-halo UNSEPARABLE"; print("kSZ two-halo:", O["ksz_two_halo"], flush=True)
# K6: GH11's 0.54 at its own numbers, GH10's 0.448 with no miscentring
a_g11 = fit(model(1.8, .24, 300.), tn := norm(Tn))["A"]; a_g10 = fit(model(1.8, 0., 300.))["A"]; O["K6c"] = dict(gh11=a_g11, gh10=a_g10, ok=bool(abs(a_g11 - 0.54) <= 0.005 and abs(a_g10 - 0.448) <= 0.005)); print(f"K6c GH11 {a_g11:.3f} vs 0.54, GH10 {a_g10:.3f} vs 0.448: {'PASS' if O['K6c']['ok'] else 'FAIL'}", flush=True)
sel3 = th <= 3.0
def cl(A, e): return "BELOW" if A + 2 * e < 1 else ("ABOVE" if A - 2 * e > 1 else ("NOT DETECTED" if A / e < 3 else "CONSISTENT"))
ks = {1.0, 1.8}
for foot, d in KST.items():
    for nm, v in d.items():
        if v is not None: ks.add(round(v, 2))
for k in sorted(ks):
    for fs in (.28, .12, .49):
        m = model(k, fs, SO); a = fit(m); a3 = fit(m, None, sel3); e = math.hypot(a["s"], .1 * a["A"]); e3 = math.hypot(a3["s"], .1 * a3["A"]); O["rows"][f"k{k}|f{fs}"] = dict(all_theta=dict(A=a["A"], s=a["s"], e=e, chi2=a["chi2"], p=a["p"], cls=cl(a["A"], e)), theta3=dict(A=a3["A"], s=a3["s"], e=e3, chi2=a3["chi2"], p=a3["p"], cls=cl(a3["A"], e3))); print(f"k {k} f {fs}: all theta A {a['A']:.3f}+-{a['s']:.3f} ({cl(a['A'], e)}); theta<=3' A {a3['A']:.3f}+-{a3['s']:.3f} ({cl(a3['A'], e3)})", flush=True)
json.dump(O, open(os.path.join(RF4, "rf4_ksz.json"), "w"), indent=1, default=float)
sys.exit(0 if O["K6c"]["ok"] and all(RES["checks"].values()) else 1)
