#!/usr/bin/env python3
"""X10 verdicts (FROZEN_CRITERIA §4, §5): classify the 12 cases for (a) and the 24 wake cells for (b) from runs/*.json,
apply the checks (R-X8a, R-X8b, V-cm from x10_validate_results.json; N-dt/N-box/N-tol on the deciding cases), and write
x10_production.out / x10_production_results.json. X10_MUTATE=1: the wrong-sign-boost runs (h 10), reported with no pass
weight, to *_MUTATE. Exit 0 iff every check PASSES (main). The case classification follows X8's x8_aggregate.py."""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
X8DIR = HERE.parent / "X8_soft_side_caustics"
MUTATE = os.environ.get("X10_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
RUNS = HERE / "runs"
JCRIT = 0.05
T0 = 13.8
HS = (10,) if MUTATE else (20, 10, 5)
lines, out = [], {"mutate_wrong_sign": MUTATE}


def say(s=""):
    print(s)
    lines.append(s)


def load(tag, base=RUNS, suf=SUF):
    f = base / f"{tag}{suf}.json"
    return json.loads(f.read_text()) if f.exists() else None


def flag_time(r):
    ts = [v for v in r["flags"].values() if v is not None]
    return min(ts) if ts else None


def g(d, k):
    return d[k] if d else None


cases = [(f, o, t) for f in ("canonical", "alt") for o in ("O1", "O2") for t in (3, 6, 9)]

# ------------------------------------------------------------------ (a) soft folds, per case (X8 §5)
classes = {}
say(f"X10 production {'(MUTATE: wrong-sign boost, h 10 only)' if MUTATE else '(co-moving start)'}: (a) S = min soft J "
    f"(validated region, straddle labels excluded), threshold J < {JCRIT} sustained 0.1 Gyr")
for f, o, t in cases:
    key = f"{f}|{o}|t_i {t}"
    rs = {h: load(f"{f}_{o}_ti{t}_h{h}") for h in HS}
    x8 = {h: load(f"{f}_{o}_ti{t}_h{h}", X8DIR / "runs", "") for h in (20, 10, 5)}
    row = {}
    for h, r in rs.items():
        if r is None:
            row[h] = None
            continue
        row[h] = {"S": g(r["S"], "J"), "event_t": g(r["event"], "t"), "event": r["event"], "flag_t": flag_time(r),
                  "flags": r["flags"], "S_by_t0": g(r["S_by_t0"], "J"), "S_by_ti_plus_TH": g(r["S_by_ti_plus_TH"], "J"),
                  "t_end": r["t_end"], "first_fold_t": g(r["first_fold"], "t"),
                  "D_STIFF_J": g(r["D_STIFF"], "J"), "D_STIFF_t": g(r["D_STIFF"], "t"),
                  "D_STIFF_first_below_t": g(r["D_STIFF_first_below"], "t"),
                  "D_EDGE_min_J": g(r["D_EDGE"]["min"], "J"), "D_EDGE_first_fold_t": g(r["D_EDGE"]["first_fold"], "t"),
                  "D_FOLLOW": r["D_FOLLOW"], "D_HELD": r["D_HELD"], "n_event_elements_max": r["n_event_elements_max"],
                  "peak_footprint_GB": r.get("peak_footprint_GB_sampled"), "peak_rss_GB": r.get("peak_rss_GB"),
                  "x8_S": g(x8[h]["S"], "J") if x8.get(h) else None,
                  "x8_event_t": g(x8[h]["event"], "t") if x8.get(h) else None}
    cls, why = None, ""
    if MUTATE:
        cls, why = "REPORTED", ""
    elif row.get(10) is None or row.get(5) is None:
        cls, why = "UNDECIDED", "MISSING RUN"
    else:
        brk = []
        for h in (10, 5):
            ft, ev = row[h]["flag_t"], row[h]["event_t"]
            if ft is not None and ft <= row[h]["t_end"] and (ev is None or ft < ev):
                brk.append(h)
        e10, e5 = row[10]["event_t"], row[5]["event_t"]
        if brk:
            cls, why = "UNDECIDED", f"STRONG-COUPLING / BREAKDOWN FLAG at h {brk}"
        elif e10 is not None and e5 is not None:
            tol = max(0.5, 0.1 * (e5 - t))
            if abs(e5 - e10) <= tol:
                cls, why = "CAUSTIC", f"t_c {e10:.3f} (h 10) / {e5:.3f} (h 5), |dt| {abs(e5 - e10):.3f} <= {tol:.3f}"
            else:
                cls, why = "UNDECIDED", f"NOT CONVERGED: t_c {e10:.3f} / {e5:.3f}, |dt| {abs(e5 - e10):.3f} > {tol:.3f}"
        elif e10 is None and e5 is None:
            s10, s5 = row[10]["S"], row[5]["S"]
            if s5 is not None and s10 is not None and s5 >= JCRIT and abs(s5 - s10) <= 0.05:
                cls, why = "NO-CAUSTIC", f"S {s10:.4f} (h 10) / {s5:.4f} (h 5)"
            else:
                cls, why = "UNDECIDED", f"NOT CONVERGED: S {s10} / {s5}, no event"
        else:
            cls, why = "UNDECIDED", f"NOT CONVERGED: event only at h {'10' if e10 is not None else '5'}"
    x8cls = None
    x8res = X8DIR / "x8_production_results.json"
    if x8res.exists():
        x8cls = json.loads(x8res.read_text())["cases"].get(key, {}).get("class")
    classes[key] = {"class": cls, "why": why, "x8_class": x8cls, "rows": row}
    say(f"  {key:22s} {cls:10s} {why}   [X8: {x8cls}]")
    for h in HS:
        rr = row[h]
        if rr is None:
            say(f"      h {h:2d}: missing")
            continue
        say(f"      h {h:2d}: S {rr['S']:+.4g}  event {rr['event_t']}  S(t0) {rr['S_by_t0']}  flags {rr['flag_t']}  "
            f"stiff first<0.05 {rr['D_STIFF_first_below_t']}  edge fold {rr['D_EDGE_first_fold_t']}  "
            f"[X8: S {rr['x8_S']}, event {rr['x8_event_t']}]")
out["cases"] = classes

# ------------------------------------------------------------------ (b) wake cells (FROZEN §5b)
say()
say("(b) wake: stiff non-straddle labels on the axis (R <= 30 kpc), downstream vs upstream of each galaxy's current motion")
cells = {}
for f, o, t in cases:
    for gal in ("MW", "M31"):
        key = f"{f}|{o}|t_i {t}|{gal}"
        per = {}
        for h in HS:
            r = load(f"{f}_{o}_ti{t}_h{h}")
            if r is None:
                per[h] = None
                continue
            dn, up = r["WAKE_5b"][f"{gal}_down"], r["WAKE_5b"][f"{gal}_up"]
            per[h] = {"down_min": g(dn["min"], "J"), "down_min_t": g(dn["min"], "t"), "down_min_pos": g(dn["min"], "pos"),
                      "down_event_t": g(dn["event"], "t"), "down_event": dn["event"], "up_min": g(up["min"], "J"),
                      "up_min_t": g(up["min"], "t"), "up_event_t": g(up["event"], "t"),
                      "down_any_sign": g(r["WAKE_5b_any_sign"][f"{gal}_down"], "J"),
                      "up_any_sign": g(r["WAKE_5b_any_sign"][f"{gal}_up"], "J"),
                      "down_wind_only": g(r["WAKE_5b_wind_only"][f"{gal}_down"], "J"),
                      "up_wind_only": g(r["WAKE_5b_wind_only"][f"{gal}_up"], "J"),
                      "flag_t": flag_time(r), "t_end": r["t_end"]}
        cl, why = "REPORTED", ""
        if not MUTATE:
            if per.get(10) is None or per.get(5) is None:
                cl, why = "UNDECIDED", "MISSING RUN"
            else:
                p10, p5 = per[10], per[5]
                e10, e5 = p10["down_event_t"], p5["down_event_t"]
                brk = [h for h in (10, 5) if per[h]["flag_t"] is not None and per[h]["flag_t"] <= per[h]["t_end"]
                       and (per[h]["down_event_t"] is None or per[h]["flag_t"] < per[h]["down_event_t"])]
                up_ok = all(per[h]["up_min"] is None or per[h]["up_min"] > 0.5 for h in (10, 5))
                if brk:
                    cl, why = "UNDECIDED", f"BREAKDOWN FLAG at h {brk}"
                elif e10 is not None and e5 is not None:
                    tol = max(0.5, 0.1 * (e5 - t))
                    if not up_ok:
                        cl, why = "UNDECIDED", f"NOT SINGLED OUT: t_c {e10:.3f} / {e5:.3f}; J_up {p10['up_min']} / {p5['up_min']}"
                    elif abs(e5 - e10) <= tol:
                        cl, why = "PRESENT", f"t_c {e10:.3f} / {e5:.3f}; J_up {p10['up_min']:.3f} / {p5['up_min']:.3f}"
                    else:
                        cl, why = "UNDECIDED", f"NOT CONVERGED: t_c {e10:.3f} / {e5:.3f}"
                elif e10 is None and e5 is None:
                    d10, d5 = p10["down_min"], p5["down_min"]
                    if d10 is not None and d5 is not None and d10 >= JCRIT and d5 >= JCRIT and abs(d5 - d10) <= 0.05:
                        cl, why = "ABSENT", f"J_down {d10:.4f} / {d5:.4f}; J_up {p10['up_min']} / {p5['up_min']}"
                    else:
                        cl, why = "UNDECIDED", f"NOT CONVERGED: J_down {d10} / {d5}, no event"
                else:
                    cl, why = "UNDECIDED", f"NOT CONVERGED: downstream event only at h {'10' if e10 is not None else '5'}"
        cells[key] = {"class": cl, "why": why, "per_h": per}
        say(f"  {key:26s} {cl:10s} {why}")
        for h in HS:
            p = per[h]
            if p is None:
                continue
            say(f"      h {h:2d}: down min {p['down_min']} (t {p['down_min_t']}) event {p['down_event_t']} | up min "
                f"{p['up_min']} (t {p['up_min_t']}) event {p['up_event_t']} | any-sign {p['down_any_sign']} / "
                f"{p['up_any_sign']} | wind-only {p['down_wind_only']} / {p['up_wind_only']}")
out["cells"] = cells

# ------------------------------------------------------------------ checks
checks = []


def record(cid, ok, detail):
    checks.append({"check": cid, "pass": bool(ok), "detail": detail})
    say(f"{cid:8s} {'PASS' if ok else 'FAIL'}  {detail}")


say()
if not MUTATE:
    vfile = HERE / "x10_validate_results.json"
    val = json.loads(vfile.read_text()) if vfile.exists() else {"checks": []}
    vmap = {c["check"]: c["pass"] for c in val["checks"]}
    for p in ("R-X8a", "R-X8b", "V-cm"):
        record(p, vmap.get(p, False), f"from {vfile.name}" if p in vmap else "missing")
    # (a) N-checks on canonical O2 t_i 3, h 10 (X8 A2 rule)
    base = load("canonical_O2_ti3_h10")
    for var, cid in (("dthalf", "N-dt(a)"), ("boxhalf", "N-box(a)"), ("toltight", "N-tol(a)")):
        r = load(f"canonical_O2_ti3_h10_{var}")
        if base is None or r is None:
            record(cid, False, "missing")
            continue
        be, ve = base["event"], r["event"]
        if be is not None:
            ok = ve is not None and abs(ve["t"] - be["t"]) <= 0.2
            det = f"t_c {be['t']:.3f} -> {ve['t'] if ve else None}; S {base['S']['J']:.4g} -> {r['S']['J']:.4g}"
        else:
            ok = ve is None and abs(r["S"]["J"] - base["S"]["J"]) <= 0.02
            det = f"no event; S {base['S']['J']:.5f} -> {r['S']['J']:.5f} (event {ve['t'] if ve else None})"
        record(cid, ok, det)
    # (b) deciding cell: the PRESENT cell with the earliest h 10 downstream event, else (canonical, O2, t_i 3, MW)
    pres = [(c["per_h"][10]["down_event_t"], k) for k, c in cells.items() if c["class"] == "PRESENT"]
    dkey = min(pres)[1] if pres else "canonical|O2|t_i 3|MW"
    df, do_, dt_, dg = dkey.split("|")
    dti = int(dt_.split()[1])
    out["b_deciding_cell"] = dkey
    say(f"(b) deciding cell: {dkey}" + ("" if pres else " (no PRESENT cell: the frozen default)"))
    bb = load(f"{df}_{do_}_ti{dti}_h10")
    for var, cid in (("dthalf", "N-dt(b)"), ("boxhalf", "N-box(b)"), ("toltight", "N-tol(b)")):
        r = load(f"{df}_{do_}_ti{dti}_h10_{var}")
        if bb is None or r is None:
            record(cid, False, f"missing (run: x10_batch.py --set numtests --case {df},{do_},{dti})")
            continue
        b5, v5 = bb["WAKE_5b"][f"{dg}_down"], r["WAKE_5b"][f"{dg}_down"]
        bu, vu = g(bb["WAKE_5b"][f"{dg}_up"]["min"], "J"), g(r["WAKE_5b"][f"{dg}_up"]["min"], "J")
        side_ok = (bu is None and vu is None) or (bu is not None and vu is not None and (bu > 0.5) == (vu > 0.5))
        if b5["event"] is not None:
            ok = v5["event"] is not None and abs(v5["event"]["t"] - b5["event"]["t"]) <= 0.2 and side_ok
            det = f"down t_c {b5['event']['t']:.3f} -> {g(v5['event'], 't')}; up min {bu} -> {vu}"
        else:
            bd, vd = g(b5["min"], "J"), g(v5["min"], "J")
            ok = v5["event"] is None and bd is not None and vd is not None and abs(vd - bd) <= 0.02 and side_ok
            det = f"no down event; down min {bd} -> {vd} (event {g(v5['event'], 't')}); up min {bu} -> {vu}"
        record(cid, ok, det)

ncls = {c: sum(v["class"] == c for v in classes.values()) for c in ("CAUSTIC", "NO-CAUSTIC", "UNDECIDED")}
o2 = {k: v["class"] for k, v in classes.items() if "|O2|" in k}
nb = {c: sum(v["class"] == c for v in cells.values()) for c in ("PRESENT", "ABSENT", "UNDECIDED")}
if MUTATE:
    va = vb = "MUTATE (reported only)"
else:
    base_ok = all(c["pass"] for c in checks if c["check"] in ("R-X8a", "R-X8b", "V-cm"))
    a_ok = base_ok and all(c["pass"] for c in checks if c["check"].endswith("(a)"))
    b_ok = base_ok and all(c["pass"] for c in checks if c["check"].endswith("(b)"))
    fa = [c["check"] for c in checks if not c["pass"] and not c["check"].endswith("(b)")]
    fb = [c["check"] for c in checks if not c["pass"] and not c["check"].endswith("(a)")]
    n_o2c = sum(v == "CAUSTIC" for v in o2.values())
    n_o2n = sum(v == "NO-CAUSTIC" for v in o2.values())
    if a_ok and n_o2c == 6:
        va = "FOLDS PERSIST"
    elif a_ok and n_o2n == 6:
        va = "FOLDS REMOVED BY THE CO-MOVING START"
    elif not a_ok:
        va = f"UNDECIDED (checks: {', '.join(fa)}; O2 cases CAUSTIC {n_o2c}/6, NO-CAUSTIC {n_o2n}/6)"
    else:
        va = f"UNDECIDED (PARTIAL: O2 cases CAUSTIC {n_o2c}/6, NO-CAUSTIC {n_o2n}/6)"
    if b_ok and nb["PRESENT"] >= 1:
        vb = f"FOCAL LINE PRESENT ({nb['PRESENT']}/24 cells: " + ", ".join(
            k for k, v in cells.items() if v["class"] == "PRESENT") + ")"
    elif b_ok and nb["ABSENT"] == 24:
        vb = "FOCAL LINE ABSENT"
    elif not b_ok:
        vb = f"UNDECIDED (checks: {', '.join(fb)}; cells {nb})"
    else:
        vb = f"UNDECIDED (cells {nb})"
say()
say(f"(a) case classes: {ncls}; O2: {o2}")
say(f"(b) cell classes: {nb}")
say(f"VERDICT (a): {va}")
say(f"VERDICT (b): {vb}")
out.update({"checks": checks, "verdict_a": va, "verdict_b": vb, "class_counts_a": ncls, "class_counts_b": nb})
(HERE / f"x10_production{SUF}.out").write_text("\n".join(lines) + "\n")
(HERE / f"x10_production_results{SUF}.json").write_text(json.dumps(out, indent=1, default=float))
sys.exit(0 if (MUTATE or all(c["pass"] for c in checks)) else 1)
