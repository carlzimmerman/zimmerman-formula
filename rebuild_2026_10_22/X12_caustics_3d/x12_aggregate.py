#!/usr/bin/env python3
"""X12 verdicts (FROZEN_CRITERIA §5) and diagnostics (§6).
  python3 x12_aggregate.py               -> x12_production.out, x12_production_results.json  (exit 0 iff checks PASS)
  X12_MUTATE=1 python3 x12_aggregate.py  -> x12_production_MUTATE.out / _results_MUTATE.json (reported, no pass weight)
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MUTATE = os.environ.get("X12_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
JCRIT = 0.05
FEET = ("canonical", "alt")
HS = (20, 15, 10)
lines, OUT = [], {"mutate_wrong_sign": MUTATE}


def say(s=""):
    print(s)
    lines.append(s)


def load(tag):
    p = HERE / "runs" / f"{tag}{SUF}.json"
    return json.loads(p.read_text()) if p.exists() else None


def first_flag(r):
    fl = [v for v in r["flags"].values() if v is not None]
    return min(fl) if fl else None


def cell_stats(r, gal, window):
    """Wake cell statistics of one run. window 'W' (t_i + W_a) or 'full'."""
    if r is None:
        return None
    wd, wu = r["wake"].get(f"{gal}_down"), r["wake"].get(f"{gal}_up")
    if wd is None:
        return None
    end = r["t_wake_end"] if window == "W" else r["t_win"]
    ev = wd["event"]
    if ev is not None and ev["t"] > end + 1e-9:
        ev = None
    key = "min_W" if window == "W" else "min_full"
    return {"event": ev, "t_c": ev["t"] if ev else None, "J_down": wd[key]["J"] if wd[key] else None,
            "J_up": wu[key]["J"] if wu[key] else None, "t_i": r["t_i"], "end": end, "flag": first_flag(r),
            "up_first_below": wu["first_below"]["t"] if wu["first_below"] else None,
            "follow": wd.get("follow")}


def cell_class(a, b):
    """FROZEN §5a per-cell rule; a = h_mid, b = h_fine statistics."""
    if a is None or b is None:
        return "MISSING", "runs missing"
    for s in (a, b):
        if s["flag"] is not None and s["flag"] <= s["end"] and (s["t_c"] is None or s["flag"] < s["t_c"]):
            return "UNDECIDED", f"BREAKDOWN FLAG at {s['flag']:.3f}"
    if a["t_c"] is not None and b["t_c"] is not None:
        tol = max(0.5, 0.1 * (b["t_c"] - b["t_i"]))
        conv = abs(b["t_c"] - a["t_c"]) <= tol
        up_ok = (a["J_up"] is None or a["J_up"] > 0.5) and (b["J_up"] is None or b["J_up"] > 0.5)
        why = f"t_c {a['t_c']:.3f} / {b['t_c']:.3f} (tol {tol:.2f}); J_up {fmt(a['J_up'])} / {fmt(b['J_up'])}"
        if conv and up_ok:
            return "PRESENT", why
        if not up_ok:
            return "UNDECIDED", "NOT SINGLED OUT: " + why
        return "UNDECIDED", "NOT CONVERGED: " + why
    if a["t_c"] is None and b["t_c"] is None and a["J_down"] is not None and b["J_down"] is not None and \
            a["J_down"] >= JCRIT and b["J_down"] >= JCRIT and abs(a["J_down"] - b["J_down"]) <= 0.05:
        return "ABSENT", f"J_down {a['J_down']:.4f} / {b['J_down']:.4f}"
    return "UNDECIDED", (f"NOT CONVERGED: events {a['t_c'] is not None} / {b['t_c'] is not None}; J_down "
                         f"{fmt(a['J_down'])} / {fmt(b['J_down'])}")


def soft_stats(r):
    if r is None:
        return None
    so = r["soft"]
    return {"t_c": so["event"]["t"] if so["event"] else None, "S": so["S"]["J"] if so["S"] else None,
            "t_i": r["t_i"], "end": r["t_win"], "flag": first_flag(r), "event": so["event"],
            "S_t0": so["S_t0"]["J"] if so["S_t0"] else None, "fold": so["fold"]["t"] if so["fold"] else None,
            "n_event_max": so["n_event_max"], "follow": so.get("follow")}


def soft_class(a, b):
    if a is None or b is None:
        return "MISSING", "runs missing"
    for s in (a, b):
        if s["flag"] is not None and s["flag"] <= s["end"] and (s["t_c"] is None or s["flag"] < s["t_c"]):
            return "UNDECIDED", f"BREAKDOWN FLAG at {s['flag']:.3f}"
    if a["t_c"] is not None and b["t_c"] is not None:
        tol = max(0.5, 0.1 * (b["t_c"] - b["t_i"]))
        if abs(b["t_c"] - a["t_c"]) <= tol:
            return "CAUSTIC", f"t_c {a['t_c']:.3f} / {b['t_c']:.3f} (tol {tol:.2f})"
        return "UNDECIDED", f"NOT CONVERGED: t_c {a['t_c']:.3f} / {b['t_c']:.3f} (tol {tol:.2f})"
    if a["t_c"] is None and b["t_c"] is None and b["S"] is not None and b["S"] >= JCRIT and \
            abs(b["S"] - a["S"]) <= 0.05:
        return "NO-CAUSTIC", f"S {a['S']:.4f} / {b['S']:.4f}"
    return "UNDECIDED", f"NOT CONVERGED: events {a['t_c'] is not None} / {b['t_c'] is not None}; S {fmt(a['S'])} / {fmt(b['S'])}"


def fmt(v, n=4):
    return "None" if v is None else f"{v:.{n}f}"


def sv(ev):
    if not ev:
        return ""
    s = ev.get("sv_at_confirm")
    s0 = ev.get("sv_at_start")
    return (f" sv@start {[round(v, 3) for v in s0[1]] if s0 else None} sv@confirm "
            f"{[round(v, 3) for v in s] if s else None}")


# ---------------- validation
val = {}
vf = HERE / "x12_validate_results.json"
if vf.exists():
    for c in json.loads(vf.read_text())["checks"]:
        val[c["check"]] = c
OUT["validation"] = {k: {"pass": v["pass"], "not_run": v.get("not_run", False),
                         **({"pass_i": v["pass_i"], "pass_ii": v["pass_ii"]} if k == "X-B0" else {})}
                     for k, v in val.items()}
base_ok = all(val.get(k, {}).get("pass", False) for k in ("R-X10", "V-a1", "V-cm", "X-ISO"))
xb = val.get("X-B0", {})
say("X12_caustics_3d verdicts" + (" (MUTATE: wrong-sign boost; reported only)" if MUTATE else ""))
say("Validation (x12_validate_results.json): " + ", ".join(
    f"{k} {'NOT RUN' if v.get('not_run') else ('PASS' if v['pass'] else 'FAIL')}" for k, v in val.items())
    + (f" [X-B0(i) {'PASS' if xb.get('pass_i') else 'FAIL'}, X-B0(ii) {'PASS' if xb.get('pass_ii') else 'FAIL'}]"
       if xb and not xb.get("not_run") else ""))
validated = base_ok and xb.get("pass", False)
if not validated:                                            # FROZEN §4 stop rule: no production run exists
    failed = [k for k in ("R-X10", "V-a1", "V-cm", "X-ISO", "X-B0")
              if not val.get(k, {}).get("pass", False) and not val.get(k, {}).get("not_run", False)]
    notrun = [k for k in ("X-ISO", "X-B0") if val.get(k, {}).get("not_run", False)]
    v = (f"UNDECIDED (3D NOT VALIDATED: {', '.join(failed)} FAILED"
         + (f"; {', '.join(notrun)} not run by the stop rule)" if notrun else ")"))
    say()
    say(f"VERDICT (a): {v}")
    say(f"VERDICT (b): {v}")
    say("Stop rule (FROZEN §4): the W, E, b > 0, N-check and production MUTATE runs are not made.")
    OUT["verdict_a"] = OUT["verdict_b"] = v
    (HERE / f"x12_production{SUF}.out").write_text("\n".join(lines) + "\n")
    (HERE / f"x12_production_results{SUF}.json").write_text(json.dumps(OUT, indent=1, default=float))
    sys.exit(1)

# ---------------- wake cells
say()
say("(a) Wake cells: window [t_i, t_i + 9.067] (FROZEN §5a), h_mid 15 / h_fine 10; h 20 for the trend")
cells = {}
specs = [("W", f, "MW", f"wake_{f}") for f in FEET] + \
        [(f"E b{b}", f, g_, f"enc_b{b}_{f}") for b in (0, 50, 150) for f in FEET for g_ in ("MW", "M31")]
for case, foot, gal, base in specs:
    st = {h: cell_stats(load(f"{base}_h{h}"), gal, "W") for h in HS}
    stf = {h: cell_stats(load(f"{base}_h{h}"), gal, "full") for h in HS}
    cl, why = cell_class(st[15], st[10])
    cl20, why20 = cell_class(st[20], st[10])
    clf, whyf = cell_class(stf[15], stf[10]) if case != "W" else (None, None)
    key = f"{case}|{foot}|{gal}"
    cells[key] = {"class": cl, "why": why, "D20_class": cl20, "D20_why": why20, "DFULL_class": clf, "DFULL_why": whyf,
                  "per_h": {h: ({k: v for k, v in st[h].items() if k != "event"} | {"event": st[h]["event"]}
                                if st[h] else None) for h in HS},
                  "per_h_full": {h: ({k: v for k, v in stf[h].items() if k not in ("event", "follow")}
                                     if stf[h] else None) for h in HS}}
    say(f"  {key:26s} {cl:9s} {why}")
    for h in HS:
        s = st[h]
        if s is None:
            continue
        ev = s["event"]
        loc = (f" at {[round(v) for v in ev['pos']]}, dz {ev[f'dz_{gal}']:.0f}, Rperp {ev[f'Rperp_{gal}']:.0f}, label "
               f"{[round(v) for v in ev['label']]}, class {ev['start_class']}" + sv(ev)) if ev else ""
        say(f"      h {h:2d}: t_c {fmt(s['t_c'], 3)}; J_down {fmt(s['J_down'])}; J_up {fmt(s['J_up'])}; up first < 0.05 "
            f"{fmt(s['up_first_below'], 3)}{loc}")
    say(f"      D-20 (h 20 / 10): {cl20}; D-FULL: {clf} {whyf if clf else ''}")
OUT["wake_cells"] = cells
verdict_cells = [f"E b{b}|{f}|MW" for b in (50, 150) for f in FEET]
w_cells = [f"W|{f}|MW" for f in FEET]
n_p = sum(cells[k]["class"] == "PRESENT" for k in verdict_cells)
n_a = sum(cells[k]["class"] == "ABSENT" for k in verdict_cells)

# ---------------- soft cases
say()
say("(b) Soft-side folds: window [3, 18.067] (X8 §5), h_mid 15 / h_fine 10")
cases = {}
for b in (0, 50, 150):
    for f in FEET:
        st = {h: soft_stats(load(f"enc_b{b}_{f}_h{h}")) for h in HS}
        cl, why = soft_class(st[15], st[10])
        cl20, why20 = soft_class(st[20], st[10])
        key = f"E b{b}|{f}"
        cases[key] = {"class": cl, "why": why, "D20_class": cl20, "D20_why": why20, "per_h": st}
        say(f"  {key:18s} {cl:10s} {why}")
        for h in HS:
            s = st[h]
            if s is None:
                continue
            ev = s["event"]
            loc = (f" at {[round(v) for v in ev['pos']]}, dist MW {ev['dist_MW']:.0f}, Rperp MW {ev['Rperp_MW']:.0f}, "
                   f"|y| {abs(ev['pos'][1]):.0f}, rel null {ev.get('along_sep_rel_null', 0):.0f}, label "
                   f"{[round(v) for v in ev['label']]}, class {ev['start_class']}" + sv(ev)) if ev else ""
            say(f"      h {h:2d}: t_c {fmt(s['t_c'], 3)}; S {fmt(s['S'])}; S by t0 {fmt(s['S_t0'])}; first fold "
                f"{fmt(s['fold'], 3)}; n_event_max {s['n_event_max']}{loc}")
        say(f"      D-20 (h 20 / 10): {cl20}")
OUT["soft_cases"] = cases
vcases = [f"E b{b}|{f}" for b in (50, 150) for f in FEET]
n_c = sum(cases[k]["class"] == "CAUSTIC" for k in vcases)
n_n = sum(cases[k]["class"] == "NO-CAUSTIC" for k in vcases)
ctrl_ok = all(cases[f"E b0|{f}"]["class"] == "CAUSTIC" for f in FEET)

# ---------------- N-checks
say()
say("N-checks (h 15): dt/2, B_out 2500 kpc, hold tol 1e-8 (two-branch rule, X8 A2 / X10)")
nres = {"N-a W": [], "N-a E": [], "N-b": []}
for var in ("dthalf", "boxhalf", "toltight"):
    for nm, base, kindc in (("N-a W", "wake_canonical_h15", "W"), ("N-a E", "enc_b150_canonical_h15", "E"),
                            ("N-b", "enc_b150_canonical_h15", "S")):
        r0, r1 = load(base), load(f"{base}_{var}")
        if r0 is None or r1 is None:
            nres[nm].append({"variant": var, "pass": False, "missing": True})
            continue
        if kindc in ("W", "E"):
            a, b_ = cell_stats(r0, "MW", "W"), cell_stats(r1, "MW", "W")
            if a["t_c"] is not None:
                ok = b_["t_c"] is not None and abs(b_["t_c"] - a["t_c"]) <= 0.2
            else:
                ok = b_["t_c"] is None and abs(b_["J_down"] - a["J_down"]) <= 0.02
            ok = ok and ((a["J_up"] > 0.5) == (b_["J_up"] > 0.5))
            row = {"variant": var, "t_c": [a["t_c"], b_["t_c"]], "J_down": [a["J_down"], b_["J_down"]],
                   "J_up": [a["J_up"], b_["J_up"]], "pass": bool(ok)}
        else:
            a, b_ = soft_stats(r0), soft_stats(r1)
            if a["t_c"] is not None:
                ok = b_["t_c"] is not None and abs(b_["t_c"] - a["t_c"]) <= 0.2
            else:
                ok = b_["t_c"] is None and abs(b_["S"] - a["S"]) <= 0.02
            row = {"variant": var, "t_c": [a["t_c"], b_["t_c"]], "S": [a["S"], b_["S"]], "pass": bool(ok)}
        nres[nm].append(row)
for nm, rows in nres.items():
    ok = bool(rows) and all(r["pass"] for r in rows)
    say(f"  {nm:6s} {'PASS' if ok else 'FAIL'}")
    for r in rows:
        say(f"      {r['variant']:9s} {'missing' if r.get('missing') else {k: v for k, v in r.items() if k != 'variant'}}")
OUT["N_checks"] = nres
n_ok = {nm: bool(rows) and all(r["pass"] for r in rows) for nm, rows in nres.items()}

# ---------------- verdicts
say()
if not validated:
    failed = [k for k in ("R-X10", "V-a1", "V-cm", "X-ISO", "X-B0")
              if not val.get(k, {}).get("pass", False) and not val.get(k, {}).get("not_run", False)]
    notrun = [k for k in ("X-ISO", "X-B0") if val.get(k, {}).get("not_run", False)]
    va = vb = (f"UNDECIDED (3D NOT VALIDATED: {', '.join(failed)} FAILED"
               + (f"; {', '.join(notrun)} not run by the stop rule)" if notrun else ")"))
else:
    checks_a = n_ok["N-a W"] and n_ok["N-a E"]
    if not checks_a:
        va = "UNDECIDED (N-a check FAILED)"
    elif all(cells[k]["class"] == "PRESENT" for k in w_cells) and n_p == 4:
        va = "WAKE FOCUS PERSISTS IN 3D"
    elif n_a == 4:
        va = "WAKE FOCUS REMOVED"
    else:
        va = (f"UNDECIDED (PARTIAL: {n_p} PRESENT, {n_a} ABSENT of 4; W cells "
              f"{[cells[k]['class'] for k in w_cells]})")
    if not n_ok["N-b"]:
        vb = "UNDECIDED (N-b check FAILED)"
    elif n_c == 4:
        vb = "FOLDS PERSIST AT b > 0"
    elif n_n == 4 and ctrl_ok:
        vb = "FOLDS REMOVED AT b > 0"
    else:
        vb = f"UNDECIDED (PARTIAL: {n_c} CAUSTIC, {n_n} NO-CAUSTIC of 4; b = 0 controls " \
             f"{[cases[f'E b0|{f}']['class'] for f in FEET]})"
say(f"VERDICT (a): {va}")
say("    verdict cells: " + "; ".join(f"{k} {cells[k]['class']}" for k in verdict_cells))
say("    controls: " + "; ".join(f"{k} {cells[k]['class']}" for k in w_cells + [f"E b0|{f}|MW" for f in FEET]))
say(f"VERDICT (b): {vb}")
say("    verdict cases: " + "; ".join(f"{k} {cases[k]['class']}" for k in vcases))
say("    controls: " + "; ".join(f"{k} {cases[k]['class']}" for k in (f"E b0|{f}" for f in FEET)))
OUT["verdict_a"], OUT["verdict_b"] = va, vb

# ---------------- run resources
res = []
for p in sorted((HERE / "runs").glob(f"*{SUF}.json")):
    if not MUTATE and "MUTATE" in p.name:
        continue
    r = json.loads(p.read_text())
    res.append({"tag": r["tag"], "nodes": r["grid"]["shape"], "steps": r["steps"],
                "hold_iters_per_call": r["hold_iters_per_call"], "xmax": r["xmax_seen"], "dt_min": r["dt_min_seen"],
                "flags": r["flags"], "footprint_GB": r["peak_footprint_GB_sampled"], "rss_GB": r["peak_rss_GB"]})
OUT["runs"] = res
say()
say(f"Runs: {len(res)}; max sampled footprint {max((r['footprint_GB'] for r in res), default=0):.2f} GB, max ru_maxrss "
    f"{max((r['rss_GB'] for r in res), default=0):.2f} GB; flags fired: "
    f"{[(r['tag'], {k: v for k, v in r['flags'].items() if v is not None}) for r in res if any(v is not None for v in r['flags'].values())]}")
(HERE / f"x12_production{SUF}.out").write_text("\n".join(lines) + "\n")
(HERE / f"x12_production_results{SUF}.json").write_text(json.dumps(OUT, indent=1, default=float))
sys.exit(0 if (MUTATE or (validated and all(n_ok.values()))) else 1)
