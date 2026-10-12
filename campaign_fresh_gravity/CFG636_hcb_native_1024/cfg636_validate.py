#!/usr/bin/env python3
"""CFG636 validation gates (FROZEN_CRITERIA.md section 3), read-only on every CFG596 reference file.
  V-R  VBr (cfg636_pm.py, CFG636_SOURCE=b, lean RES can L100 N256 NSEED512 RMIN 0.78125) vs CFG596 VLr: every stored snapshot
       quantity identical (difference exactly 0) -> the copied engine with the OLD weight reproduces CFG596 bit for bit.
  V-H  VHr (CFG636_SOURCE=hcb, same configuration) completes and its gravitating P differs from VBr's; P_grav/P_S0 at
       k 0.3 / 0.5 / 1 (S0 = CFG596 VLs) reported as a PREVIEW, NOT a verdict (256^3 resolution).
  python3 cfg636_validate.py -> cfg636_validate.out / cfg636_validate.json
kappa = 1/2 FITTED; footings never pooled; cold energy mass required; not theory closed."""
import os, json, glob, math, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); EXT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data"))
W = os.path.join(EXT, "cfg636_work"); W596 = os.path.join(EXT, "cfg596_work")
OUT = []
def P(*a):
    s = " ".join(str(x) for x in a); print(s, flush=True); OUT.append(s)
def load(d, pat):
    f = glob.glob(os.path.join(d, pat)); return json.load(open(f[0])) if f else None
def peak(job):
    wl = os.path.join(W, job, "watch.log"); pk = 0.0; sg = 0.0
    if os.path.exists(wl):
        for line in open(wl):
            m = re.search(r"peak ([\d.]+) swap_used ([\d.]+) MB \(start ([\d.]+)\)", line)
            if m: pk = max(pk, float(m.group(1))); sg = max(sg, float(m.group(2)) - float(m.group(3)))
    return pk, sg
RES = dict(lane="CFG636 validation", date="2026-10-12", criteria_commit="89aeaae12", gates={})
KEYS_SKIP = ("t",)                                     # wall-clock time only

ref = load(os.path.join(W596, "VLr"), "cfg596_RES_*.json"); vb = load(os.path.join(W, "VBr"), "cfg636_b_RES_*.json")
if ref and vb and "z0" in vb["snap"]:
    diffs = {}; nq = 0
    for z, s in ref["snap"].items():
        t = vb["snap"].get(z)
        if t is None: diffs[z] = "missing"; continue
        for k, v in s.items():
            if k in KEYS_SKIP: continue
            nq += 1
            a, b = np.asarray(v, dtype=float), np.asarray(t.get(k), dtype=float)
            if a.shape != b.shape or not np.array_equal(a, b, equal_nan=True):
                diffs[f"{z}.{k}"] = float(np.max(np.abs(b / a - 1))) if a.shape == b.shape else "shape"
    ok = not diffs and set(ref["snap"]) == set(vb["snap"])
    pk, sg = peak("VBr")
    RES["gates"]["V-R"] = dict(PASS=ok, bitwise=ok, snapshots=sorted(vb["snap"]), quantities_compared=nq, differences=diffs,
                               peak_rss_gb=pk, swap_growth_mb=sg, reference="cfg596_work/VLr (cfg596_validate.py V-L reference)")
    P(f"V-R VBr (cfg636_pm.py, SOURCE b) vs CFG596 VLr: {nq} stored quantities over snapshots {sorted(vb['snap'])}; "
      f"differences {diffs if diffs else 'none (bit for bit)'} -> {'PASS' if ok else 'FAIL'}; peak RSS {pk:.2f} GB, swap growth {sg:.0f} MB")
else: P("V-R: not run / incomplete")

vh = load(os.path.join(W, "VHr"), "cfg636_hcb_RES_*.json"); s0 = load(os.path.join(W596, "VLs"), "cfg596_S0_*.json")
if vh and vb and s0 and "z0" in vh["snap"]:
    rec = dict(NOTE="PREVIEW at 256^3 (L100): NOT a verdict", snaps={})
    for z in ("z1", "z0.5", "z0"):
        k = np.array(vh["snap"][z]["k"]); assert np.allclose(k, np.array(s0["snap"][z]["k"]), rtol=1e-9)
        rh = np.array(vh["snap"][z]["P_grav"]) / np.array(s0["snap"][z]["P"]); rb = np.array(vb["snap"][z]["P_grav"]) / np.array(s0["snap"][z]["P"])
        m = k <= 1.0 + 1e-9; at = lambda r, kk: float(np.exp(np.interp(math.log(kk), np.log(k), np.log(r))))
        rec["snaps"][z] = dict(HCB_over_S0={str(kk): at(rh, kk) for kk in (0.3, 0.5, 1.0)}, B_over_S0={str(kk): at(rb, kk) for kk in (0.3, 0.5, 1.0)},
                               HCB_G_max_abs_k_le_1=float(np.max(np.abs(rh[m] - 1))), B_G_max_abs_k_le_1=float(np.max(np.abs(rb[m] - 1))),
                               HCB_min_k_le_1=float(np.min(rh[m] - 1)), HCB_max_k_le_1=float(np.max(rh[m] - 1)),
                               sigma8_grav_ratio_HCB=vh["snap"][z]["sigma8_grav"] / s0["snap"][z]["sigma8"],
                               sigma8_grav_ratio_B=vb["snap"][z]["sigma8_grav"] / s0["snap"][z]["sigma8"],
                               src_sum=[vh["snap"][z].get("src_sum"), vb["snap"][z].get("src_sum")], n_catch=[vh["snap"][z].get("n_catch"), vb["snap"][z].get("n_catch")])
    dif = float(np.max(np.abs(np.array(vh["snap"]["z0"]["P_grav"]) / np.array(vb["snap"]["z0"]["P_grav"]) - 1)))
    pk, sg = peak("VHr")
    rec.update(completed=True, max_rel_diff_Pgrav_HCB_vs_B_z0=dif, differs=bool(dif > 0), PASS=bool(dif > 0), peak_rss_gb=pk, swap_growth_mb=sg)
    RES["gates"]["V-H"] = rec
    z0 = rec["snaps"]["z0"]
    P(f"V-H VHr (SOURCE hcb) completed; max|P_grav(H-CB)/P_grav(B) - 1| at z0 = {dif:.3e} -> {'PASS (differs)' if dif > 0 else 'FAIL (identical)'}; peak RSS {pk:.2f} GB, swap growth {sg:.0f} MB")
    for z, r in rec["snaps"].items():
        P(f"  PREVIEW (256^3, NOT a verdict) {z}: P_grav/P_S0 at k 0.3/0.5/1: H-CB " + " / ".join(f"{v:.3f}" for v in r["HCB_over_S0"].values())
          + "; old weight B " + " / ".join(f"{v:.3f}" for v in r["B_over_S0"].values())
          + f"; max|P/P_S0-1| (k<=1) H-CB {r['HCB_G_max_abs_k_le_1']:.3f}, B {r['B_G_max_abs_k_le_1']:.3f}; sigma8_grav/S0 H-CB {r['sigma8_grav_ratio_HCB']:.4f}, B {r['sigma8_grav_ratio_B']:.4f}")
else: P("V-H: not run / incomplete")
json.dump(RES, open(os.path.join(HERE, "cfg636_validate.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg636_validate.out"), "w").write("\n".join(OUT) + "\n")
