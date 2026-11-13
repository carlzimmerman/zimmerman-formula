#!/usr/bin/env python3
"""FRZ3R reading T grading (AMENDMENT_A1; reported, never the frozen label). Same shared gate set-up as frz3r_grade.py.
Usage: nice -n 19 python3 frz3r_grade_turn.py <footing> -> frz3r_turn_<footing>.json/.out and _MUTATE.json/.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, glob, warnings
warnings.filterwarnings("ignore")
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
FOOT = sys.argv[1]
src = open(os.path.join(HERE, "frz3r_grade.py")).read(); cut = src.index("# ------------------------------------------------------------------ parts")
g = {"__file__": os.path.join(HERE, "frz3r_grade.py"), "__name__": "frz3r_grade_setup"}; sys.argv = ["frz3r_grade.py", FOOT]
exec(compile(src[:cut], "frz3r_grade_setup", "exec"), g)
FD, BGB, forest_eval, amp, dchi2_sel, ZB, ASEL, ALL, ANCH, bin_sel, md5ok = (g[k] for k in ("FD", "BGB", "forest_eval", "amp", "dchi2_sel", "ZB", "ASEL", "ALL", "ANCH", "bin_sel", "md5ok"))
CLIGHT = 299792.458
OUT, OUTM = [], []
def P(*a, m=False):
    s = " ".join(str(x) for x in a); print(s, flush=True); (OUTM if m else OUT).append(s)
F1 = json.load(open(g["FRZ1J"])); KF1 = np.array(F1["k"]); f1R = {z: F1["cases"][f"primary|{FOOT}"][f"{z:.1f}"]["R_cold"] for z in ZB}
D_FRZ1 = float(forest_eval(FD, BGB, amp(f1R, KF1))["dchi2"])
PARTS = {}
for z in ZB:
    PARTS[z] = {}
    for f in sorted(glob.glob(os.path.join(HERE, "parts", f"turn_z{z:.1f}_s*_{FOOT}_N384.json"))):
        d = json.load(open(f)); PARTS[z][d["seed"]] = d
def RF(parts, tag, wB="B", wR="R", seeds=None):
    S = sorted(parts) if seeds is None else [s for s in seeds if s in parts]
    arr = np.array([np.array(parts[s]["flux"][tag][wB]["p"]) / np.array(parts[s]["flux"][tag if tag != "M2_doubled" else "primary"][wR]["p"]) for s in S])
    return np.array(parts[S[0]]["kv"]), arr.mean(0), arr
def r_at(kvz, Rz):
    r = np.ones(FD["NB"])
    for z in Rz:
        s_ = FD["zs"] == round(z, 2); r[s_] = np.interp(FD["ks"][s_], kvz[z][1:], Rz[z][1:])
    return r
def dchi(kvz, Rz, sel): return dchi2_sel(r_at(kvz, Rz), sel)
RES = dict(lane="FRZ3R", reading="T (AMENDMENT_A1; reported, not the frozen label)", footing=FOOT, FRZ1_through_gate=D_FRZ1, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
kvz, RFz, ps, ns_ = {}, {}, {}, {}
for z in ZB:
    kvz[z], RFz[z], ps[z] = RF(PARTS[z], "primary"); ns_[z] = len(ps[z])
Dflux = dchi(kvz, RFz, ALL); Danch = dchi(kvz, RFz, ASEL)
perbin = {f"{z:.1f}": dchi(kvz, RFz, bin_sel(z)) for z in ZB}
def Rpaint(parts):
    S = sorted(parts); k = np.array(parts[S[0]]["P3D"]["k"]); arr = np.array([np.array(parts[s]["P3D"]["B"]) / np.array(parts[s]["P3D"]["R"]) for s in S]); return k, arr.mean(0)
kp, Rp = {}, {}
for z in ZB:
    k, R = Rpaint(PARTS[z]); m = (k <= 10) & np.isfinite(R); kp[z], Rp[z] = k[m], R[m]   # empty low-k bins dropped
Dmat = float(forest_eval(FD, BGB, amp(Rp, kp))["dchi2"])
RES.update(flux=dict(dchi2=Dflux, anchor=Danch, per_bin=perbin, seeds=ns_), matter_same_fields=Dmat, softening=Dflux / Dmat,
           posthoc_FRZ1_scaled=D_FRZ1 * Dflux / Dmat)
P(f"[{FOOT}] reading T: FLUX Delta chi^2 {Dflux:.2f} (anchor bins {Danch:.2f}); matter, same fields {Dmat:.1f}; ratio {Dflux / Dmat:.4g}; POST HOC FRZ1 {D_FRZ1:.1f} x ratio = {D_FRZ1 * Dflux / Dmat:.2f}")
P(f"[{FOOT}] per bin: " + " ".join(f"{k}:{v:.2f}" for k, v in perbin.items()))
tab = {}
for z in ZB:
    kv = kvz[z]; at = lambda x: float(np.interp(x, kv[1:], RFz[z][1:]))
    ek = np.array(PARTS[z][0]["expected_ratio_KT"]["k"]); er = np.array(PARTS[z][0]["expected_ratio_KT"]["R"])
    tab[f"{z:.1f}"] = dict(R_F=[at(x) for x in (0.003, 0.005, 0.01, 0.02, 0.03)], R_paint=[float(np.exp(np.interp(np.log(x), np.log(kp[z]), np.log(Rp[z])))) for x in (1, 3, 5)],
                           R_expected_ta=[float(np.interp(math.log(x), np.log(ek), er)) for x in (1, 3, 5)], R_FRZ1=[float(np.interp(x, KF1, f1R[z])) for x in (1, 3, 5)], seeds=ns_[z])
    t = tab[f"{z:.1f}"]
    P(f"[{FOOT}] T z {z:.1f}: R_F at 0.003/0.005/0.01/0.02/0.03 s/km " + "/".join(f"{v:.4f}" for v in t["R_F"]) + "; R_paint k1/3/5 " + "/".join(f"{v:.4f}" for v in t["R_paint"])
      + " (halo model ta " + "/".join(f"{v:.4f}" for v in t["R_expected_ta"]) + "; FRZ1 " + "/".join(f"{v:.4f}" for v in t["R_FRZ1"]) + f"); seeds {ns_[z]}")
RES["table"] = tab
KA = {}
a_ok = all(np.all(np.array(d["flux"]["KA_a_zero"]["B0"]["p"]) == np.array(d["flux"]["primary"]["R"]["p"])) for z in ANCH for d in PARTS[z].values())
KA["a"] = dict(exact=bool(a_ok), pass_=bool(a_ok and md5ok))
rows = {}; ok = True
for z in ANCH:
    t = tab[f"{z:.1f}"]
    for i, x in enumerate((1, 3, 5)):
        e = t["R_expected_ta"][i]; tol = 0.01 + 0.25 * abs(e - 1); rows[f"z{z} k{x}"] = dict(R_paint=t["R_paint"][i], expected=e, tol=tol, ok=bool(abs(t["R_paint"][i] - e) <= tol)); ok &= abs(t["R_paint"][i] - e) <= tol
KA["b_T"] = dict(rows=rows, pass_=bool(ok))
rows = {}; ok = True
for z in ANCH:
    d = PARTS[z][0]; kv = np.array(d["kv"]); kmax = 0.5 * math.pi / (CLIGHT * 0.8 / ((1 + z) * 1215.67)); sel = (kv > 0) & (kv <= kmax)
    rf = np.array(d["flux"]["KA_c_thin"]["B"]["p"]) / np.array(d["flux"]["KA_c_thin"]["R"]["p"]); rm = np.array(d["gas1d"]["matter_los"]["B"]) / np.array(d["gas1d"]["matter_los"]["R"])
    dev = np.abs(rf - rm)[sel]; tol = (1e-3 + 0.01 * np.abs(rm - 1))[sel]; rows[f"{z}"] = dict(max_dev=float(dev.max()), ok=bool(np.all(dev <= tol))); ok &= bool(np.all(dev <= tol))
KA["c"] = dict(rows=rows, pass_=bool(ok))
dmax = 0.0
for z in ZB:
    for d in PARTS[z].values():
        for tag, fl in d["flux"].items():
            if tag in ("KA_c_thin",): continue
            for w, v in fl.items(): dmax = max(dmax, abs(v["meanF"] - math.exp(-(0.751 * ((1 + z) / 4.5) ** 2.90 - 0.132))))
KA["d"] = dict(max_abs=dmax, pass_=bool(dmax <= 1e-4))
rows = {}; ok = True
for z in ANCH:
    kv = kvz[z]; kmax = 0.5 * math.pi / (CLIGHT * 0.8 / ((1 + z) * 1215.67)); sel = (kv > 0) & (kv <= kmax)
    E = float(np.sqrt(np.mean((RFz[z][sel] - 1) ** 2))); Sm = float(np.sqrt(np.mean((ps[z][:, sel].std(0, ddof=1) / math.sqrt(ns_[z])) ** 2)))
    rows[f"{z}"] = dict(E=E, S_mean=Sm, ok=bool(Sm <= E / 3)); ok &= Sm <= E / 3
KA["e"] = dict(rows=rows, pass_=bool(ok))
RES["known_answers"] = KA
for k, v in KA.items(): P(f"[{FOOT}] T known answer ({k}): {'PASS' if v['pass_'] else 'FAIL'} " + json.dumps({kk: vv for kk, vv in v.items() if kk != 'pass_'})[:700])
def anch(tag, wB="B", seeds=None):
    kz, Rz = {}, {}
    for z in ANCH: kz[z], Rz[z], _ = RF(PARTS[z], tag, wB=wB, seeds=seeds)
    return dchi(kz, Rz, ASEL)
MU = {}
m1 = anch("M1_lin"); m2 = anch("M2_doubled", "B2")
MU["M1_saturation_removed"] = dict(dchi2_anchor=m1, primary=Danch, factor=m1 / Danch, bites=bool(max(m1 / Danch, Danch / m1) >= 1.25))
MU["M2_doubled"] = dict(dchi2_anchor=m2, primary=Danch, factor=m2 / Danch, bites=bool(m2 / Danch >= 2))
RES["mutations"] = MU
for k, v in MU.items(): P(f"[{FOOT}] T MUTATE {k}: anchor {v['dchi2_anchor']:.2f} vs primary {v['primary']:.2f} (x {v['factor']:.3f}) -> {'bites' if v['bites'] else 'DOES NOT BITE'}", m=True)
BR = {}
for nm, tg in (("lambda_P x 0.5", "lam_x0.5"), ("lambda_P x 2", "lam_x2"), ("lambda_P = 100 proper kpc (record)", "lam_rec")):
    db = anch(tg, seeds=(0, 1)); dp = anch("primary", seeds=(0, 1)); BR[nm] = dict(anchor=db, primary_same_seeds=dp, est_12bin=Dflux * db / dp)
    P(f"[{FOOT}] T bracket {nm}: anchor {db:.2f} (primary same seeds {dp:.2f}) -> 12-bin estimate {Dflux * db / dp:.2f}")
RES["brackets"] = BR
fl = [v for z in ZB for d in PARTS[z].values() for k, v in d.get("floored", {}).items() if k.startswith("primary|")]
RES["floored_primary_max"] = max(fl); P(f"[{FOOT}] T floored fraction, primary fields: max {max(fl):.2e}")
kaok = all(v["pass_"] for v in KA.values()); muok = all(v["bites"] for v in MU.values())
if not (kaok and muok): lab = "NO VERDICT"
elif Dflux > 4:
    cr = [k for k, v in BR.items() if v["est_12bin"] <= 4]; lab = "FOREST ROW FAILS AT FLUX LEVEL" + (", FRAGILE (" + "; ".join(cr) + ")" if cr else "")
else:
    cr = [k for k, v in BR.items() if v["est_12bin"] > 4]; lab = "FOREST ROW HOLDS AT FLUX LEVEL (not a pass; a hit awaiting a further independent check)" + (", FRAGILE (" + "; ".join(cr) + ")" if cr else "")
RES["label_reading_T"] = lab
P(f"[{FOOT}] reading T (reported, not the frozen label): {lab}")
json.dump(RES, open(os.path.join(HERE, f"frz3r_turn_{FOOT}.json"), "w"), indent=1)
open(os.path.join(HERE, f"frz3r_turn_{FOOT}.out"), "w").write("\n".join(OUT) + "\n")
json.dump(dict(lane="FRZ3R", reading="T", footing=FOOT, mutations=MU, note=RES["note"]), open(os.path.join(HERE, f"frz3r_turn_{FOOT}_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, f"frz3r_turn_{FOOT}_MUTATE.out"), "w").write("\n".join(OUTM) + "\n")
