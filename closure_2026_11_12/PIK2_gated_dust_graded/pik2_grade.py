#!/usr/bin/env python3
"""PIK2 label (criteria 95edd35e0b section 4) from pik2_row0.json, pik2_row2.json and pik2_static.json.
  window      = row 2 and rows 3-7 and K-SC and row 8 (8a <= 0.02, 8b <= 1) at one (S, xi), graded gates only
  CMB-ONLY    = no window, and some (S, xi) passes row 2, rows 5, 6, 7 and row 8 at the galaxy radii, none of which also
                passes rows 3 and 4
  NO VALUE    = otherwise;  NO VERDICT if a known answer or a row-0 check fails.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pik2_common as CM
H = CM.HERE
R0 = json.load(open(os.path.join(H, "pik2_row0.json"))); R2 = json.load(open(os.path.join(H, "pik2_row2.json")))
ST = json.load(open(os.path.join(H, "pik2_static.json")))
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
ka_ok = bool(R0["all_pass"] and ST["KA_all_pass"])
RES = dict(lane="PIK2", criteria="95edd35e0b", KA_and_row0_pass=ka_ok, labels={})
P(f"Row 0 checks and KA3/KA4: {'PASS' if R0['all_pass'] else 'FAIL'}; static known answers: {'PASS' if ST['KA_all_pass'] else 'FAIL'}")
for f in CM.FOOT:
    RES["labels"][f] = {}
    for mlab in ("primary_Jeans", "secondary_B1a", "reported_BBN"):
        win, gal, galclu, per = [], [], [], {}
        for g in CM.GRADED:
            t2 = {r["logxi"]: r for r in R2["rows"][f][mlab][g]["table"]}
            rows = ST["scan"]["primary"][f][mlab][g]["rows"]
            n2 = 0; ng = 0; best = None
            for r in rows:
                r2 = t2[r["logxi"]]["row2_pass"]; n2 += r2
                g8 = max(r["r5"]["r8a"], r["r6"]["r8a"]) <= 0.02 and max(r["r5"]["r8b"], r["r6"]["r8b"]) <= 1.0
                if r2 and r["p37"] and r["KSC"] and r["p8"]: win.append((g, r["logxi"]))
                if r2 and r["galaxy_ok"] and g8:
                    gal.append((g, r["logxi"])); ng += 1
                    if r["cluster_ok"]: galclu.append((g, r["logxi"]))
                if best is None or r["r3"]["rms"] < best["r3"]["rms"]: best = r
            per[g] = dict(row2_pass_xi=n2, galaxy_side_xi=ng, xcop_best_rms=best["r3"]["rms"], xcop_best_mean=best["r3"]["mean"], xcop_best_logxi=best["logxi"],
                          visibility=R2["rows"][f][mlab][g]["visibility"])
        if not ka_ok: lab = "NO VERDICT"
        elif win: lab = "KEY OPENS A WINDOW (hit; awaits an independent re-grade)"
        elif gal and not galclu: lab = "CMB-ONLY"
        else: lab = "NO VALUE"
        RES["labels"][f][mlab] = dict(label=lab, windows=win, galaxy_side=gal, galaxy_and_cluster=galclu, per_gate=per)
        gs = sorted(set(g for g, _ in gal))
        P(f"[{f}] {mlab}: {lab}. windows {len(win)}; galaxy side (rows 2, 5-7, 8 at galaxy radii) passes for gates {gs} "
          + "; ".join(f"{g}: log xi {min(x for gg, x in gal if gg == g)}..{max(x for gg, x in gal if gg == g)}" for g in gs))
        for g, d in per.items():
            P(f"     {g}: {d['visibility']}; row 2 passes {d['row2_pass_xi']}/281 xi; galaxy side {d['galaxy_side_xi']}; X-COP best rms {d['xcop_best_rms']:.3f} "
              f"(mean {d['xcop_best_mean']:+.3f}) at log xi {d['xcop_best_logxi']}")
P(CM.NOTE)
json.dump(CM.clean(RES), open(os.path.join(H, "pik2_grade.json"), "w"), indent=1)
open(os.path.join(H, "pik2_grade.out"), "w").write("\n".join(OUT) + "\n")
