#!/usr/bin/env python3
"""Codex arrival audit, Part B: reproduce sol61_push/compatible_gas_2026_10_23 numbers (frozen in FROZEN_CRITERIA.md).

B1 cooling scale (rerun of Codex's cooling_scale.py from a hashed copy), B2 arithmetic on Codex's committed
analysis_v2/result.json against the numbers printed in RESULT.md, B3 leaf-by-leaf comparison of two bounded reruns
(crossing_base n128, ultra n512) against the committed result.json files.  Reads only; edits nothing in sol61_push/.
"""
import hashlib
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parents[1] / "sol61_push" / "compatible_gas_2026_10_23"
MUTATE = "--mutate" in sys.argv
checks = []


def record(name, ok, detail):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"{name:4s} {'PASS' if ok else 'FAIL'}  {detail}")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


# ---- B1 ----------------------------------------------------------------------------------------
mine = json.loads((HERE / "cg_rerun" / "cooling_scale_result.json").read_text())
theirs_path = SRC / "cooling_scale" / "result.json"
byte_same = sha(HERE / "cg_rerun" / "cooling_scale_result.json") == sha(theirs_path)
row = {(r["T"], r["fH2"]): r for r in mine}
r3, r4 = row[(200, 0.001)], row[(200, 0.0001)]
if MUTATE:
    r3 = dict(r3, ncrit=r3["ncrit"] * 1.01)
ok = (abs(r3["ncrit"] - 758) <= 0.5 and abs(r3["tcool_over_tff_min"] / 0.902 - 1) <= 1e-3
      and abs(r4["tcool_over_tff_min"] / 9.02 - 1) <= 1e-3 and abs(r3["isothermal_gas_Jeans_Msun"] - 3276) <= 1)
record("B1", ok, f"byte-identical {byte_same}; ncrit(200 K) {r3['ncrit']:.2f}; min tcool/tff {r3['tcool_over_tff_min']:.4f} "
                 f"(f 1e-3), {r4['tcool_over_tff_min']:.3f} (f 1e-4); Jeans {r3['isothermal_gas_Jeans_Msun']:.1f} Msun")

# ---- B2 ----------------------------------------------------------------------------------------
A = json.loads((SRC / "analysis_v2" / "result.json").read_text())
runs = [("128", "crossing_base"), ("256", "crossing_fine"), ("512", "ultra")]
table = {"128": (110.1, 163, 14.03, 7182, 980401), "256": (55.06, 2691, 5.879, 28618, 488262),
         "512": (27.53, 24825, 3.500, 123577, 263537)}     # RESULT.md rows as printed
aper = {"128": 4.738, "256": 4.812, "512": 4.821}             # million Msun, RESULT.md
key_ap = [k for k in A["ultra"] if k.startswith("mass_0.32")][0]
rows, all_ok = {}, True
for n, r in runs:
    d = A[r]
    cell_pc = d["field_cell_kpc"] * 1e3
    rad_pc = d["gas_r001_volume_kpc"] * 1e3
    ap = (d[key_ap]["cold"] + d[key_ap]["gas"]) / 1e6
    got = (cell_pc, d["nHmax"], rad_pc, d["peak_c"], d["central_cold_cell_mass_Msun"])
    want = table[n]
    if MUTATE and n == "512":
        want = (want[0], want[1] * 1.05) + want[2:]
    digits_ok = (abs(got[0] - want[0]) <= 0.05 + 0.01 * (n == "256") and abs(got[1] - want[1]) <= 0.5
                 and abs(got[2] - want[2]) <= 0.005 * max(1, want[2] / 10) + 5e-4 and abs(got[3] - want[3]) <= 0.5
                 and abs(got[4] - want[4]) <= 0.5 and abs(ap - aper[n]) <= 5e-4)
    all_ok &= digits_ok
    rows[n] = {"field_cell_pc": cell_pc, "peak_nH": d["nHmax"], "r_fixed_gas_pc": rad_pc, "peak_cold_contrast": d["peak_c"],
               "first_cell_cold_Msun": d["central_cold_cell_mass_Msun"], "aperture_1e6Msun": ap,
               "r_over_cell": rad_pc / cell_pc, "densest_T": d["densest_cell_T"],
               "peak_nH_over_ncrit": d.get("peak_nH_over_local_ncrit")}
    record("B2", digits_ok, f"n{n}: cell {cell_pc:.2f} pc, peak nH {d['nHmax']:.1f}, r {rad_pc:.3f} pc, contrast "
                            f"{d['peak_c']:.0f}, first cell {d['central_cold_cell_mass_Msun']:.0f}, aperture {ap:.4f}e6, "
                            f"r/cell {rad_pc / cell_pc:.3f}")
ratios = [rows[n]["r_over_cell"] for n in ("128", "256", "512")]
pc = (rows["256"]["peak_cold_contrast"] / rows["128"]["peak_cold_contrast"],
      rows["512"]["peak_cold_contrast"] / rows["256"]["peak_cold_contrast"])
cm = (rows["256"]["first_cell_cold_Msun"] / rows["128"]["first_cell_cold_Msun"],
      rows["512"]["first_cell_cold_Msun"] / rows["256"]["first_cell_cold_Msun"])
apch = rows["512"]["aperture_1e6Msun"] / rows["256"]["aperture_1e6Msun"] - 1
ok = (all(0.105 <= r <= 0.13 for r in ratios) and abs(pc[0] - 3.98) < 0.005 and abs(pc[1] - 4.32) < 0.005
      and abs(cm[0] - 0.498) < 5e-4 and abs(cm[1] - 0.540) < 5e-4 and abs(apch - 0.00185) < 5e-5)
record("B2", ok, f"r/cell {ratios[0]:.3f}/{ratios[1]:.3f}/{ratios[2]:.3f}; contrast ratios {pc[0]:.3f}/{pc[1]:.3f}; "
                 f"first-cell mass ratios {cm[0]:.4f}/{cm[1]:.4f}; last aperture change {100 * apch:.3f} %")

# ---- B3 ----------------------------------------------------------------------------------------


def leaves(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from leaves(v, f"{prefix}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from leaves(v, f"{prefix}[{i}]")
    else:
        yield prefix, obj


b3 = {}
for name in ("crossing_base", "ultra"):
    p_new = HERE / "cg_rerun" / f"{name}_result.json"
    p_old = SRC / name / "result.json"
    new, old = dict(leaves(json.loads(p_new.read_text()))), dict(leaves(json.loads(p_old.read_text())))
    same_keys = set(new) == set(old)
    worst, nnum, nbad = 0.0, 0, 0
    for kk in old:
        a, b = old[kk], new.get(kk)
        if isinstance(a, bool) or not isinstance(a, (int, float)):
            nbad += a != b
            continue
        nnum += 1
        if MUTATE and name == "ultra" and kk.endswith("nHmax"):
            b = b * (1 + 1e-6)
        if isinstance(a, float) and (math.isnan(a) or math.isnan(b)):
            nbad += not (math.isnan(a) and math.isnan(b))
            continue
        scale = max(abs(a), 1e-300)
        rel = abs(a - b) / scale if a != b else 0.0
        if abs(a - b) <= 1e-15 * max(abs(a), 1.0):
            rel = 0.0
        worst = max(worst, rel)
    byte = sha(p_new) == sha(p_old)
    b3[name] = {"byte_identical": byte, "numeric_leaves": nnum, "worst_rel": worst, "non_numeric_mismatch": int(nbad)}
    record("B3", same_keys and worst <= 1e-9 and nbad == 0,
           f"{name}: byte-identical {byte}; {nnum} numeric leaves, worst rel diff {worst:.1e}; non-numeric mismatches {nbad}")

rss = {}
for name in ("crossing_base", "ultra"):
    txt = (HERE / "cg_rerun" / f"{name}_stderr.txt").read_text()
    m = re.search(r"(\d+)\s+maximum resident set size", txt)
    rss[name] = int(m.group(1)) / 2 ** 30 if m else None
record("B3", all(v is not None and v < 1.0 for v in rss.values()),
       "peak RSS " + ", ".join(f"{k} {v:.3f} GB" for k, v in rss.items()) + " (bound 1 GB)")

npass = sum(c["pass"] for c in checks)
out = {"mutate": MUTATE, "B2_rows": rows, "B3": b3, "rss_GB": rss, "checks": checks,
       "summary": f"{npass}/{len(checks)} PASS",
       "copies_sha256": (HERE / "cg_copy" / "SHA256.txt").read_text().splitlines()}
(HERE / ("cg_repro_results_MUTATE.json" if MUTATE else "cg_repro_results.json")).write_text(json.dumps(out, indent=1))
print(out["summary"])
sys.exit(0 if npass == len(checks) else 1)
