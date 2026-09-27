#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR34_summary -- the before / after table of the kernel-argument re-score, assembled from the XR34 results files only.

Reads XR34_kernel_argument_results.json and XR34_rescore_<lane>_results.json (DE11b, DE11, L362, L347, L346, L359, L358)
and prints, per lane, the committed number, the committed line re-run, the corrected number and whether the lane's own
verdict flips; then the downstream numbers that read these lanes (DE2's constant-threshold forest crossing, L359's window
and DE2's dominance anchor, the PAPER34 rows).  It computes nothing new from the PM.
CHECKS
  S1 [load-bearing] every re-score it tabulates certified its argument (K1) and its controls (C1, C2) -- a table of
     'after' numbers whose argument check failed is refused.
  S2 (reported) the table and the downstream flags.
MUTATE=1 reads the _MUTATE results instead: their K1 fails (the doubled correction), so S1 must FAIL (rc = 1).

Run from the repository root after the XR34 lanes (MUTATE=1 first):
    python3 real_research/cross_thread_review_2026_09_26/XR34_summary.py
"""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import XR34_common as X                                                 # noqa: E402

MUTATE = os.environ.get("MUTATE", "0") == "1"
LN = X.Lane("XR34_summary", MUTATE)
P = LN.P
SUF = "_results_MUTATE.json" if MUTATE else "_results.json"
LANES = ("DE11b", "DE11", "L362", "L347", "L346", "L359", "L358")


def load(slug):
    fn = os.path.join(X.HERE, slug + SUF)
    return json.load(open(fn)) if os.path.exists(fn) else None


if __name__ == "__main__":
    P(__doc__.split("CHECKS")[0].strip())
    R = {ln: load(f"XR34_rescore_{ln}") for ln in LANES}
    KA = load("XR34_kernel_argument")

    LN.banner("S1  WHAT EACH RE-SCORE CERTIFIED")
    cert = {}
    for ln in LANES:
        r = R[ln]
        if r is None:
            cert[ln] = "missing"; P(f"    {ln:6s} no results file"); continue
        ch = r["checks"]
        need = [k for k in ("K1", "C1", "C2") if k in ch] if not MUTATE else ["K1"]
        ok = all(ch[k]["ok"] for k in need) and (MUTATE or all(k in ch for k in ("K1", "C1", "C2")))
        cert[ln] = "ok" if ok else "FAILED"
        P(f"    {ln:6s} " + ", ".join(f"{k} {'pass' if ch[k]['ok'] else 'FAIL'}" for k in ("K1", "C1", "C2") if k in ch)
          + f"   rc-equivalent {r['n_fail_load_bearing']}")
    ka_ok = KA is not None and all(KA["checks"][k]["ok"] for k in ("B0", "B1", "K1", "K2"))
    LN.check("S1 every tabulated re-score certified its argument and controls (K1, C1, C2), and the bug demonstration passed "
             "(B0, B1, K1, K2)", f"{cert}; kernel_argument {'ok' if ka_ok else 'FAILED'}",
             ka_ok and all(v == "ok" for v in cert.values()))
    if MUTATE:
        sys.exit(LN.finish())

    LN.banner("S2  BEFORE / AFTER (committed -> corrected argument, everything else the lane's own)")
    rows = []

    def row(lane, cell, before, rerun, after, rule, vb, va):
        rows.append(dict(lane=lane, cell=cell, before=before, rerun=rerun, after=after, rule=rule, verdict_before=vb,
                         verdict_after=va, flips=(vb != va)))
        rr = "" if rerun is None else f"{rerun:.4f}"
        P(f"    {lane:6s} {cell:34s} {before:8.4f} {rr:>8s} {after:8.4f}  x{after / before:5.2f}   {rule:22s} {vb:>8s} -> {va:8s}"
          + ("   <-- FLIPS" if vb != va else ""))
    P(f"    {'lane':6s} {'cell':34s} {'before':>8s} {'re-run':>8s} {'after':>8s}  {'ratio':>6s}   {'rule':22s} verdict")
    n = R["DE11b"]["numbers"]["R1"]
    for k in ("C_alt", "B_alt", "B_canonical"):
        row("DE11b", k, n["before"][k], n["rerun_committed_line"][k], n["after"][k], "worst <= 0.10",
            "PASS" if n["before"][k] <= 0.10 else "FAIL", "PASS" if n["after"][k] <= 0.10 else "FAIL")
    n = R["DE11"]["numbers"]["R1"]
    row("DE11", "worst over 8 cells x 2 z", n["worst_before"], None, n["worst_after"], "worst <= 0.10", n["F1_before"], n["F1_after"])
    n = R["L362"]["numbers"]["R1"]
    for t in ("A", "B", "C"):
        row("L362", f"box {t}, x_c = 3", n["worst_before"][t], None, n["worst_after"][t], "robust iff B,C > 0.10",
            "> 0.10" if n["worst_before"][t] > 0.10 else "<= 0.10", "> 0.10" if n["worst_after"][t] > 0.10 else "<= 0.10")
    n = R["L347"]["numbers"]["R1"]
    lab = lambda w: "PASS" if w <= 0.10 else ("FAIL-bl" if w < 0.15 else "FAIL")
    row("L347", "x_c = 5 (both boxes, footings)", n["before"]["worst5"], None, n["after"]["worst5"], "<= 0.10 (bl < 0.15)",
        lab(n["before"]["worst5"]), lab(n["after"]["worst5"]))
    row("L347", "x_c = 7 (canonical)", n["before"]["x7"], None, n["after"]["x7"], "<= 0.10", lab(n["before"]["x7"]), lab(n["after"]["x7"]))
    n = R["L346"]["numbers"]["R1"]
    row("L346", "x_c = 5 matter power, k = 1-4", n["before"]["worst"], None, n["after"]["worst"], "in [0.8, 1.2]",
        n["F2_before"], n["F2_after"])
    n = R["L358"]["numbers"]["R1"]
    for xc in ("2.0", "2.5", "3.0", "4.0"):
        row("L358", f"x_c = {xc} (L25 box)", n["before_L25"][xc], None, n["after_L25"][xc], "<= 0.10",
            lab(n["before_L25"][xc]), lab(n["after_L25"][xc]))
    row("L358", "x_c = 3, 50 Mpc/h alone (F3)", n["coarse_x3_before"], None, n["coarse_x3_after"], "<= 0.10",
        lab(n["coarse_x3_before"]), lab(n["coarse_x3_after"]))
    n = R["L359"]["numbers"]["R1"]
    for c, v in n["rows"].items():
        row("L359", f"(p, x_c0) = ({c.replace('/', ', ')}) L25", v["before_L25"], None, v["after_L25"], "<= 0.10",
            "PASS" if v["before_L25"] <= 0.10 else "FAIL", "PASS" if v["after_L25"] <= 0.10 else "FAIL")
    LN.out["numbers"]["table"] = rows

    LN.banner("S3  DOWNSTREAM: what reads these lanes")
    FT_b = sorted([(float(k), v) for k, v in R["L358"]["numbers"]["R1"]["before_all"].items()]
                  + [(5.0, R["L347"]["numbers"]["R1"]["before"]["worst5"]), (7.0, R["L347"]["numbers"]["R1"]["before"]["x7"])])
    FT_a = sorted([(float(k), v) for k, v in R["L358"]["numbers"]["R1"]["after_L25"].items()]
                  + [(5.0, R["L347"]["numbers"]["R1"]["after"]["worst5"]), (7.0, R["L347"]["numbers"]["R1"]["after"]["x7"])])

    def cross(FT):
        for (x0, d0), (x1, d1) in zip(FT[:-1], FT[1:]):
            if d0 > 0.10 >= d1:
                return x0 + (0.10 - d0) * (x1 - x0) / (d1 - d0)
        return None
    xb, xa = cross(FT_b), cross(FT_a)
    tail = lambda xx: f" -> passes above x_c = {xx:.2f}" if xx else " -> NO tested constant threshold (<= 7) passes"
    P("    DE2's constant-threshold forest table (L358 + L347): before " + ", ".join(f"{x:g}: {d:.3f}" for x, d in FT_b) + tail(xb))
    P("    (after: L358 on its 25 Mpc/h box)                 after  " + ", ".join(f"{x:g}: {d:.3f}" for x, d in FT_a) + tail(xa))
    w = R["L359"]["numbers"]["R1"]
    P(f"    L359's window (forest leg): before {len(w['window_before'])} cells -> after {len(w['window_after'])}: {w['window_after']}; "
      f"DE2's dominance anchor (0.5, 1.5): {w['rows']['0.5/1.5']['before_all']:.4f} -> {w['rows']['0.5/1.5']['after_L25']:.4f} "
      f"({'still passes' if w['rows']['0.5/1.5']['pass_after'] else 'FAILS'}); L360 pairs L359's window with KiDS")
    n58, n62 = R["L358"]["numbers"]["R1"], R["L362"]["numbers"]["R1"]
    p34 = {"L358 x_c = 2 / 2.5 / 3 (quoted 0.185 / 0.174 / 0.160)": [round(n58["after_L25"][k], 3) for k in ("2.0", "2.5", "3.0")],
           "L362 B / C (quoted 0.157 / 0.191)": [round(n62["worst_after"]["B"], 3), round(n62["worst_after"]["C"], 3)],
           "L359 window forest worst, low-high (quoted 0.2%-8.5%)": [round(100 * min(v["after_L25"] for v in w["rows"].values()), 1),
                                                                    round(100 * max(v["after_L25"] for v in w["rows"].values()), 1)],
           "L359 p >= 1 worst (quoted 4.0%)": round(100 * max(v["after_L25"] for c, v in w["rows"].items() if not c.startswith("0.5")), 1)}
    for k, v in p34.items():
        P(f"    PAPER34 row {k}: after {v}")
    LN.out["numbers"]["downstream"] = dict(DE2_constant_table_before=FT_b, DE2_constant_table_after=FT_a, X_forest_const_before=xb,
                                           X_forest_const_after=xa, L359_window_after=w["window_after"], PAPER34_rows_after=p34)
    flips = [f"{r_['lane']} {r_['cell']}" for r_ in rows if r_["flips"]]
    LN.check("S2 (reported) the before / after table and the downstream flags", f"verdict flips: {flips or 'none'}; DE2 constant "
             f"crossing {xb if xb is None else round(xb, 2)} -> {xa if xa is None else round(xa, 2)}", True, load_bearing=False)
    sys.exit(LN.finish())
