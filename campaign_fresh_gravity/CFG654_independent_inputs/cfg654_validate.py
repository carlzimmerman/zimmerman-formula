#!/usr/bin/env python3
"""CFG654 validation at 256^3 (lean RES/S0 canonical L100 NSEED512 RMIN 0.78125, 3 threads, one process, nice 10), read only on
every CFG596 / CFG650 reference file.
  V-R  reproduction control: cfg654_pm.py with CFG654_INPUTS=inherited, all CFG650 modules OFF (job V0i) vs CFG596 VLr: every stored
       snapshot quantity identical (difference exactly 0).  Must pass.
  Addendum A1 (2026-10-13): V-N1/V-N2/V-C are evaluated for the PRIMARY CMB-pair set (VNcs, VNc12; labels [cmb]) and for the
  BBN bracket (VNs, VN12).
  V-N1 native ICs carry the predicted amplitude: VNs particle P(k) at z_i over CFG596 VLs at z_i (same seed, same box) vs the
       cfg654_ics prediction P_native(k, z_i)/P_inherited(k, z_i), k <= 1 h/Mpc: max |ratio/prediction - 1| <= 0.03 (1LPT + CIC,
       reported with the value).
  V-N2 native time integration: VNs P(k_f, z)/P(k_f, z_i) at the fundamental mode vs the native linear growth D(a)^2/D(a_i)^2
       (and VLs vs the inherited growth, the same check on the old run), reported; tolerance 5% (one-mode, mild nonlinearity).
  V-C  VN12 completes, finite, |src_sum|/e_sum <= 1e-5 at z = 1, 0.5, 0.
  PREVIEW (256^3, NOT a verdict): P_grav/P_S0 at k 0.3/0.5/1 for VN12/VNs (native) next to CFG650 VM12/CFG596 VLs (inherited).
  python3 cfg654_validate.py -> cfg654_validate.out / cfg654_validate.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, json, glob, math, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(EXT, "cfg654_work"); W596 = os.path.join(EXT, "cfg596_work"); W650 = os.path.join(EXT, "cfg650_work")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def load(d, pat):
    f = glob.glob(os.path.join(d, pat)); return json.load(open(f[0])) if f else None
def peak(job):
    wl = os.path.join(W, job, "watch.log"); pk = 0.0
    if os.path.exists(wl):
        for line in open(wl):
            m = re.search(r"peak ([\d.]+) swap_used", line)
            if m: pk = max(pk, float(m.group(1)))
    return pk
def identical(ref, run):
    diffs = {}; nq = 0
    for z, s in ref["snap"].items():
        t = run["snap"].get(z)
        if t is None: diffs[z] = "missing"; continue
        for k, v in s.items():
            if k == "t": continue
            nq += 1
            a, b = np.asarray(v, dtype=float), np.asarray(t.get(k), dtype=float)
            if a.shape != b.shape or not np.array_equal(a, b, equal_nan=True):
                diffs[f"{z}.{k}"] = float(np.max(np.abs(b / a - 1))) if a.shape == b.shape else "shape"
    return nq, diffs
RES = dict(lane="CFG654 validation", gates={}, previews={})
VLr = load(os.path.join(W596, "VLr"), "cfg596_RES_*.json"); VLs = load(os.path.join(W596, "VLs"), "cfg596_S0_*.json")
VM12 = load(os.path.join(W650, "VM12"), "cfg650_*_RES_*.json")
V0i = load(os.path.join(W, "V0i"), "cfg650_off_RES_*.json")
P("CFG654 validation (256^3). kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed.")
# V-R
if V0i and "z0" in V0i["snap"]:
    nq, diffs = identical(VLr, V0i); ok = not diffs and set(VLr["snap"]) == set(V0i["snap"])
    RES["gates"]["V-R"] = dict(PASS=ok, quantities=nq, differences=diffs, peak_rss_gb=peak("V0i"))
    P(f"V-R V0i (inherited inputs, modules OFF) vs CFG596 VLr: {nq} quantities over {sorted(V0i['snap'])}; differences {diffs if diffs else 'none (bit for bit)'} -> {'PASS' if ok else 'FAIL'}; peak RSS {peak('V0i'):.2f} GB")
else: P("V-R: not run / incomplete")
# V-N1, V-N2, V-C, preview -- per native input set (addendum A1: the CMB pair is PRIMARY, the frozen BBN set is a bracket)
import importlib.util
sp = importlib.util.spec_from_file_location("ics", os.path.join(HERE, "cfg654_ics.py")); ics = importlib.util.module_from_spec(sp); sp.loader.exec_module(ics)
inh = ics.inherited()
def prev(F, S):
    out = {}
    for key in ("z0", "z0.5", "z1"):
        kk = np.array(F["snap"][key]["k"]); r = np.array(F["snap"][key]["P_grav"]) / np.array(S["snap"][key]["P"])
        out[key] = {str(q): float(np.exp(np.interp(math.log(q), np.log(kk), np.log(r)))) - 1 for q in (0.3, 0.5, 1.0)}
    return out
if VM12 and VLs: RES["previews"]["inherited_VM12_vs_VLs"] = prev(VM12, VLs)
for setname, js, jr, sfx, pre in (("CMB pair (PRIMARY, addendum A1)", "VNcs", "VNc12", "_cmb", "cfg654cmb_"), ("BBN omega_b (frozen set, bracket)", "VNs", "VN12", "", "cfg654nat_")):
    Sn = load(os.path.join(W, js), pre + "*_S0_*.json"); Rn = load(os.path.join(W, jr), pre + "*_RES_*.json")
    T = np.load(os.path.join(HERE, f"cfg654_ics_tables{sfx}.npz")); tag = "" if sfx == "" else "[cmb]"
    P(f"\n== {setname}: {js} / {jr}")
    if Sn and "z0" in Sn["snap"]:
        k = np.array(Sn["snap"]["zi"]["k"]); m = k <= 1.0
        meas = np.array(Sn["snap"]["zi"]["P"]) / np.array(VLs["snap"]["zi"]["P"])
        pred = np.exp(np.interp(np.log(k), np.log(T["kh"]), np.log(T["P_zi"]))) / (inh["P0"](k) * inh["Dg"](1 / 50.0) ** 2)
        dev = float(np.max(np.abs(meas[m] / pred[m] - 1)))
        RES["gates"]["V-N1" + tag] = dict(PASS=dev <= 0.03, max_dev=dev, at={str(q): [float(np.interp(q, k, meas)), float(np.interp(q, k, pred))] for q in (0.1, 0.3, 0.5, 1.0)}, peak_rss_gb=peak(js))
        P(f"V-N1{tag} {js}/VLs particle P at z_i vs predicted native/inherited ratio (bin-centre, as frozen), k <= 1: max dev {dev:.4f} -> {'PASS' if dev <= 0.03 else 'FAIL'}; "
          + "; ".join(f"k {q}: meas {v[0]:.4f} pred {v[1]:.4f}" for q, v in RES["gates"]["V-N1" + tag]["at"].items()) + f"; peak RSS {peak(js):.2f} GB")
        lna, lnD = T["lna"], T["lnD"]; Dn = lambda a: math.exp(np.interp(math.log(a), lna, lnD))
        g2 = {}
        for key in ("z1", "z0.5", "z0"):
            a = Sn["snap"][key]["a"]
            rn = Sn["snap"][key]["P"][0] / Sn["snap"]["zi"]["P"][0] / (Dn(a) / Dn(1 / 50.0)) ** 2
            ri = VLs["snap"][key]["P"][0] / VLs["snap"]["zi"]["P"][0] / (inh["Dg"](a) / inh["Dg"](1 / 50.0)) ** 2
            g2[key] = dict(native=rn, inherited=ri)
        okg = all(abs(v["native"] - 1) <= 0.05 for v in g2.values())
        RES["gates"]["V-N2" + tag] = dict(PASS=okg, fundamental_mode_growth_over_linear=g2)
        P(f"V-N2{tag} fundamental-mode growth / linear growth (native run vs native D; inherited run vs inherited D): " + "; ".join(f"{z}: {v['native']:.4f} / {v['inherited']:.4f}" for z, v in g2.items()) + f" -> {'PASS' if okg else 'FAIL'}")
    else: P(f"V-N1/V-N2{tag}: {js} not run / incomplete")
    if Rn and "z0" in Rn["snap"] and Sn:
        cc = {key: abs(Rn["snap"][key].get("src_sum", 0.0)) / max(abs(Rn["snap"][key].get("e_sum", 1e-30)), 1e-30) for key in ("z1", "z0.5", "z0")}
        fin = all(Rn["snap"][key].get("finite", True) for key in Rn["snap"])
        RES["gates"]["V-C" + tag] = dict(PASS=fin and max(cc.values()) <= 1e-5, src_over_e=cc, peak_rss_gb=peak(jr))
        P(f"V-C{tag} {jr}: finite {fin}; |src_sum|/e_sum " + ", ".join(f"{z} {v:.1e}" for z, v in cc.items()) + f" -> {'PASS' if RES['gates']['V-C' + tag]['PASS'] else 'FAIL'}; peak RSS {peak(jr):.2f} GB")
        RES["previews"][f"native{sfx}_{jr}_vs_{js}"] = prev(Rn, Sn)
        RES["previews"][f"sigma8_z0{sfx}"] = dict(S0_native=Sn["snap"]["z0"]["sigma8"], S0_inherited=VLs["snap"]["z0"]["sigma8"],
                                                 grav_native=Rn["snap"]["z0"]["sigma8_grav"], grav_inherited_VM12=VM12["snap"]["z0"]["sigma8_grav"] if VM12 else None)
P("\nPREVIEW 256^3, NOT a verdict: P_grav/P_S0 - 1 at k 0.3/0.5/1")
for nm, d in RES["previews"].items():
    if nm.startswith("sigma8"): P(f"  {nm}: " + ", ".join(f"{k} {v:.4f}" for k, v in d.items() if v is not None)); continue
    P(f"  {nm}: " + "; ".join(f"{z}: " + "/".join(f"{v:+.3f}" for v in d[z].values()) for z in ("z0", "z0.5", "z1")))
json.dump(RES, open(os.path.join(HERE, "cfg654_validate.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg654_validate.out"), "w").write("\n".join(OUT) + "\n")
