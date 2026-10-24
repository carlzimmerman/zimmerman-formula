#!/usr/bin/env python3
"""X12 AMENDMENTS A1 and A2 (POST-RESULT diagnostics, no verdict weight): collects the V-cm failure diagnostics.
  python3 x12_amend.py  -> x12_amendments.out, x12_amendments_results.json
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
lines, out = [], {}


def say(s=""):
    print(s)
    lines.append(s)


def load(tag):
    p = HERE / "runs" / f"{tag}.json"
    return json.loads(p.read_text()) if p.exists() else None


def series(r, every=1.0):
    rows, nxt = [], 0.0
    for s in r["series"]:
        if s["t"] >= nxt - 1e-6:
            m = s.get("max_at")
            rows.append({"t": s["t"], "absJm1": s["absJm1_out_now"],
                         "max_rel_mass": [round(v, 1) for v in m["rel_mass"]] if m else None,
                         "max_label": m["label"] if m else None})
            nxt += every
    return rows


say("X12 AMENDMENTS A1 / A2 (POST-RESULT diagnostics; no verdict weight). Statistic: V-cm max|J-1| over validated labels")
say("with 2 eps <= |q| <= 300 kpc, canonical, 15.167 Gyr (FROZEN §4); frozen pass line <= 0.1 at h 15 and 10, h 10 <= h 15.")
rows = {}
for tag, what in (("vcm_MW_canonical_h15", "frozen"), ("vcm_MW_canonical_h10", "frozen"),
                  ("vcm_M31_canonical_h15", "frozen"), ("vcm_M31_canonical_h10", "frozen"),
                  ("vcm_M31_canonical_h15_A1loc", "A1-loc (frozen box rerun)"),
                  ("vcm_M31_canonical_h10_A1loc", "A1-loc (frozen box rerun)"),
                  ("vcm_MW_canonical_h15_A1box", "A1-box (z [-660, 1680])"),
                  ("vcm_MW_canonical_h10_A1box", "A1-box (z [-660, 1680])"),
                  ("vcm_M31_canonical_h15_A1box", "A1-box (z [-600, 1260])"),
                  ("vcm_M31_canonical_h10_A1box", "A1-box (z [-600, 1260])"),
                  ("vcm_M31_canonical_h10_A2mir", "A2-mir (full domain, no mirror planes)"),
                  ("vcm_M31_canonical_h10_A2dt", "A2-dt (dt0 and 0.15 halved)")):
    r = load(tag)
    if r is None:
        say(f"  {tag:34s} missing")
        continue
    v = r["vstat"]
    rows[tag] = {"what": what, "max_absJm1_outside": v["mx_out"], "t_of_max": v["t_mx_out"],
                 "max_absJm1_inside_2eps": v["mx_in"], "max_comoving_disp_outside": v["disp_out"], "flags": r["flags"],
                 "steps": r["steps"], "nodes": r["grid"]["shape"], "mirrors": r["grid"]["mirrors"],
                 "fine": r["grid"]["fine"], "peak_rss_GB": r["peak_rss_GB"],
                 "peak_footprint_GB": r["peak_footprint_GB_sampled"], "series_1Gyr": series(r)}
    say(f"  {tag:34s} {what:40s} max|J-1| {v['mx_out']:.4f} (t {v['t_mx_out']:.2f}); inside 2eps {v['mx_in']:.3f}; "
        f"F3 {r['flags'].get('F3')}")
for a, b in (("vcm_M31_canonical_h15", "vcm_M31_canonical_h15_A1loc"),
             ("vcm_M31_canonical_h10", "vcm_M31_canonical_h10_A1loc")):
    ra, rb = load(a), load(b)
    if ra and rb:
        same = ra["vstat"] == rb["vstat"]
        out[f"reproduced_{a}"] = same
        say(f"  A1-loc reproduces {a}: {same}")
say()
say("Time series at h 10, M31 (max|J-1| and where it sits relative to the mass, kpc):")
for tag in ("vcm_M31_canonical_h10", "vcm_M31_canonical_h10_A1loc", "vcm_M31_canonical_h10_A1box",
            "vcm_M31_canonical_h10_A2mir", "vcm_M31_canonical_h10_A2dt"):
    if tag in rows:
        say(f"  {tag}: " + "; ".join(f"{s['t']:.0f}: {s['absJm1']:.3f}" + (f" @{s['max_rel_mass']}" if s["max_rel_mass"]
                                                                              else "") for s in rows[tag]["series_1Gyr"][::2]))
out["rows"] = rows
say()
m15, m10 = rows.get("vcm_M31_canonical_h15", {}).get("max_absJm1_outside"), \
    rows.get("vcm_M31_canonical_h10", {}).get("max_absJm1_outside")
for tag in ("vcm_M31_canonical_h10_A1box", "vcm_M31_canonical_h10_A2mir", "vcm_M31_canonical_h10_A2dt"):
    if tag in rows and m15 is not None:
        v = rows[tag]["max_absJm1_outside"]
        say(f"  reading {tag}: {v:.4f} vs frozen h 15 {m15:.4f} -> {'BELOW (this change removes the non-monotonicity)' if v < m15 else 'NOT BELOW (this change is not the cause)'}")
(HERE / "x12_amendments.out").write_text("\n".join(lines) + "\n")
(HERE / "x12_amendments_results.json").write_text(json.dumps(out, indent=1, default=float))
