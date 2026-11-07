#!/usr/bin/env python3
"""OQ2 POST-FREEZE sensitivity (disclosed in RESULT.md; carries NO label). One bug fix only: OQ1's band_groups never merged
adjacent passing candidates, so every groups band was a set of isolated points (an S3 prediction can never land inside, and
S1 can miss an overlap with gap 0 dex). Fixed version: consecutive passing candidates (event points and midpoints, between
which the in-band count is constant) merge into one interval. Everything else is oq2.py / oq1.py unchanged.
Web excluded here (web bins sit at log q < 0.7, no host shares them in OQ1 / OQ2 main; disclosed).
    nice -n 15 python3 oq2_postfix.py   -> oq2_postfix.json / oq2_postfix.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math, time
sys.argv = [sys.argv[0]]
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import oq2 as Q
O = Q.O; P = Q.P

def band_groups_fixed(pts):
    iv = []
    for p in pts:
        a, b = max(O.Finv(p, p["D"] - 2 * p["sl"]), 0.0), O.Finv(p, p["D"] + 2 * p["sl"])
        if b >= a: iv.append((a, b))
    need = math.ceil(0.8 * len(pts)); ev = sorted({0.0} | {a for a, _ in iv} | {b for _, b in iv})
    cands = []
    for i, e in enumerate(ev):
        cands.append(e)
        if i + 1 < len(ev): cands.append(0.5 * (e + ev[i + 1]))
    out = []; prev_ok = False
    for F in cands:
        ok = sum(1 for a, b in iv if a <= F <= b) >= need
        if ok:
            if prev_ok: out[-1] = (out[-1][0], F)
            else: out.append((F, F))
        prev_ok = ok
    return out
O.band_groups = band_groups_fixed   # class_band looks the name up at call time

R = dict(lane="OQ2 post-freeze band_groups fix (no label)", criteria="97fdee2c2e", runs={}, main={}, note="kappa = 1/2 FITTED; not theory closed")
P("OQ2 POST-FREEZE: band_groups merge fix only; no label. kappa = 1/2 FITTED; not theory closed.")
for f, a0 in O.A0.items():
    for fst in (0, 1):
        pts, _ = O.points(f, a0, fst)
        for seed, F0 in [(21, F0) for F0 in (0, 1, 10)] + [(s, 1) for s in Q.SEEDS]:
            pp = Q.plant_seed(pts, Q.QMED[f], False, seed); cx = O.ctx_for(pp, f, 0.005, planted=True); r = O.s1_run(pp, cx, F0, None); ev = {}
            for N in Q.GRID:
                e = Q.s1_eval(r, N); d = dict(S1_holds=e["S1_holds"], n_dead=len(e["dead_bins"]),
                                              dead=[dict(log10q=x["log10q"], pair=x["worst_pair"], n={c: v["n"] for c, v in x["classes"].items()}) for x in e["dead_bins"]])
                if seed == 21: s3 = Q.s3_eval(pp, r, N); d["S3_holds"] = s3["S3_holds"]; d["S3"] = s3["per_class"]
                ev[str(N)] = d
            R["runs"][f"{f}|fst{fst}|seed{seed}|F0={F0}"] = ev
tab = {}
for f in O.A0:
    tab[f] = {}
    for N in Q.GRID:
        ens = [v[str(N)] for k, v in R["runs"].items() if k.startswith(f + "|") and "|seed21|" not in k]
        s21 = [v[str(N)] for k, v in R["runs"].items() if k.startswith(f + "|") and "|seed21|" in k]
        nf = sum(1 for e in ens if not e["S1_holds"])
        tab[f][str(N)] = dict(false_conflict_runs=nf, seed21_no_conflict=all(e["S1_holds"] for e in s21), seed21_S3_holds=all(e["S3_holds"] for e in s21),
                              S3_fail_classes=sorted({c for e in s21 for c, s in e["S3"].items() if s not in ("PASS", "NO POWERED BIN")}))
Nfull = next((N for N in Q.GRID if all(tab[f][str(N)]["false_conflict_runs"] <= Q.FALSE_MAX and tab[f][str(N)]["seed21_no_conflict"] and tab[f][str(N)]["seed21_S3_holds"] for f in O.A0)), None)
Ns1 = next((N for N in Q.GRID if all(tab[f][str(N)]["false_conflict_runs"] <= Q.FALSE_MAX and tab[f][str(N)]["seed21_no_conflict"] for f in O.A0)), None)
R["calibration"] = tab; R["N_min_star_frozen_rule"] = Nfull; R["N_min_S1_only"] = Ns1
P("calibration with the fix (false runs of 40; seed 21 no conflict; seed 21 S3; S3 failing classes):")
for N in Q.GRID:
    P(f"  N_min {N}: " + "; ".join(f"[{f}] {tab[f][str(N)]['false_conflict_runs']}/40 s21 {'Y' if tab[f][str(N)]['seed21_no_conflict'] else 'n'} S3 {'Y' if tab[f][str(N)]['seed21_S3_holds'] else 'n'} {tab[f][str(N)]['S3_fail_classes']}" for f in O.A0))
P(f"N_min* under the frozen rule (S1 + S3): {Nfull}; S1-only calibrated N_min: {Ns1}")
# main data + M2 at the S1-only N (information only)
N = Ns1 if Ns1 else 8
for f, a0 in O.A0.items():
    for fst in (0, 1):
        pts, _ = O.points(f, a0, fst); ctx = O.ctx_for(pts, f, Q.Q1J["foot"][f]["web"]["Fweb_max"])
        for tag, pl in (("main", None), ("M2", True)):
            src = pts if pl is None else Q.plant_seed(pts, Q.QMED[f], True, 21)
            cx = ctx if pl is None else O.ctx_for(src, f, 0.005, planted=True)
            for F0 in (0, 1, 10):
                r = O.s1_run(src, cx, F0, None); e = Q.s1_eval(r, N)
                R["main"][f"{tag}|{f}|fst{fst}|F0={F0}"] = dict(N_min=N, S1_holds=e["S1_holds"], dead_bins=e["dead_bins"], never_vote_points=Q.dropped(r, N))
                P(f"  [{tag}] {f} f*={fst} F0={F0} at N_min {N}: " + ("S1 HOLDS" if e["S1_holds"] else f"EMPTY in {len(e['dead_bins'])} bins, max gap {max((d['gap_dex'] or 0) for d in e['dead_bins']):.3f} dex: "
                  + "; ".join(f"{d['log10q']} {d['worst_pair'][0]}-{d['worst_pair'][1]} {d['gap_dex']:.3f} n{ {c: v['n'] for c, v in d['classes'].items()} }" for d in e["dead_bins"][:6])))
P("kappa = 1/2 FITTED; not theory closed.")
Q.save(os.path.join(HERE, "oq2_postfix.json"), R); open(os.path.join(HERE, "oq2_postfix.out"), "w").write("\n".join(Q.OUT) + "\n")
