#!/usr/bin/env python3
"""X8 verdict (FROZEN_CRITERIA §5 with AMENDMENTS A1, A2): classify the 12 cases from runs/*.json, apply the N-checks and
the validation results, and write x8_production.out / x8_production_results.json (X8_MUTATE=1: the frozen-F set, written
to *_MUTATE, with the MUT-R expectation reported). Exit 0 iff every check PASSES (main)."""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MUTATE = os.environ.get("X8_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
RUNS = HERE / "runs"
JCRIT = 0.05
T0 = 13.8
lines, out = [], {"mutate": MUTATE}


def say(s=""):
    print(s)
    lines.append(s)


def load(tag):
    f = RUNS / f"{tag}{SUF}.json"
    return json.loads(f.read_text()) if f.exists() else None


def flag_time(r):
    ts = [v for v in r["flags"].values() if v is not None]
    return min(ts) if ts else None


def fmt_rec(rec):
    if rec is None:
        return "none"
    return (f"J {rec['J']:+.4g} at t {rec['t']:.3f} (t0{rec['t_minus_t0']:+.2f}), label ({rec['label'][0]:.0f}, "
            f"{rec['label'][1]:.0f}), pos ({rec['pos'][0]:.0f}, {rec['pos'][1]:.0f}), {min(rec['dist_MW'], rec['dist_M31']):.0f} kpc "
            f"from {'MW' if rec['dist_MW'] < rec['dist_M31'] else 'M31'}, z - z_null {rec['z_rel_null']:+.0f}")


cases = [(f, o, t) for f in ("canonical", "alt") for o in ("O1", "O2") for t in (3, 6, 9)]
classes = {}
say(f"X8 production {'(MUTATE: frozen F)' if MUTATE else ''}: per-case statistic S = min soft J (validated region, "
    f"[t_i, t_end]); threshold J < {JCRIT} sustained 0.1 Gyr")
for f, o, t in cases:
    key = f"{f}|{o}|t_i {t}"
    rs = {h: load(f"{f}_{o}_ti{t}_h{h}") for h in (20, 10, 5)}
    row = {}
    for h, r in rs.items():
        if r is None:
            row[h] = None
            continue
        row[h] = {"S": r["S"]["J"] if r["S"] else None, "event_t": r["event"]["t"] if r["event"] else None,
                  "flag_t": flag_time(r), "flags": r["flags"], "S_by_t0": r["S_by_t0"]["J"] if r["S_by_t0"] else None,
                  "S_by_ti_plus_TH": r["S_by_ti_plus_TH"]["J"] if r["S_by_ti_plus_TH"] else None,
                  "t_end": r["t_end"], "first_fold_t": r["first_fold"]["t"] if r["first_fold"] else None,
                  "D_STIFF_J": r["D_STIFF"]["J"] if r["D_STIFF"] else None,
                  "D_STIFF_t": r["D_STIFF"]["t"] if r["D_STIFF"] else None,
                  "peak_footprint_GB": r.get("peak_footprint_GB_sampled"), "peak_rss_GB": r.get("peak_rss_GB")}
    cls, why = None, ""
    if row[10] is None or row[5] is None:
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
    classes[key] = {"class": cls, "why": why, "rows": row}
    say(f"  {key:22s} {cls:10s} {why}")
    for h in (20, 10, 5):
        rr = row[h]
        if rr is None:
            say(f"      h {h:2d}: missing")
            continue
        say(f"      h {h:2d}: S {rr['S']:+.4g}  event {rr['event_t']}  S(t0) {rr['S_by_t0']}  S(t_i+TH) "
            f"{rr['S_by_ti_plus_TH']}  flags {rr['flag_t']}  stiff min {rr['D_STIFF_J']} at {rr['D_STIFF_t']}")
out["cases"] = classes

checks = []


def record(cid, ok, detail):
    checks.append({"check": cid, "pass": bool(ok), "detail": detail})
    say(f"{cid:6s} {'PASS' if ok else 'FAIL'}  {detail}")


say()
vfile = HERE / f"x8_validate_results{SUF}.json"
val = json.loads(vfile.read_text()) if vfile.exists() else {}
for p in ("R0", "Va1", "Va2", "Vb"):
    record(p, p in val and val[p]["pass"], f"from {vfile.name}" if p in val else "missing")
if not MUTATE:
    base = load("canonical_O2_ti3_h10")
    for var, cid in (("dthalf", "N-dt"), ("boxhalf", "N-box"), ("toltight", "N-tol")):
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
ncls = {c: sum(v["class"] == c for v in classes.values()) for c in ("CAUSTIC", "NO-CAUSTIC", "UNDECIDED")}
val_ok = all(c["pass"] for c in checks)
if MUTATE:
    o2 = [k for k in classes if "|O2|" in k]
    mutr = all(classes[k]["rows"][10] is not None and classes[k]["rows"][10]["S"] is not None
               and classes[k]["rows"][10]["S"] <= 0 for k in o2)
    say(f"MUT-R  {'YES' if mutr else 'NO'}  (reported, no pass weight): every O2 case reaches J <= 0 for a soft element "
        f"by t_end at h 10 in frozen F")
    out["MUT_R"] = mutr
    verdict = "MUTATE"
elif not val_ok:
    verdict = "UNDECIDED (validation: " + ", ".join(c["check"] for c in checks if not c["pass"]) + ")"
elif ncls["CAUSTIC"] >= 1:
    verdict = "CAUSTICS FORM"
elif ncls["NO-CAUSTIC"] == 12:
    verdict = "NO CAUSTICS TO T_H"
else:
    verdict = "UNDECIDED (cases)"
say(f"classes: {ncls}")
say(f"VERDICT: {verdict}")
out["checks"] = checks
out["verdict"] = verdict
out["class_counts"] = ncls
(HERE / f"x8_production{SUF}.out").write_text("\n".join(lines) + "\n")
(HERE / f"x8_production_results{SUF}.json").write_text(json.dumps(out, indent=1, default=float))
sys.exit(0 if (MUTATE or val_ok) else 1)
