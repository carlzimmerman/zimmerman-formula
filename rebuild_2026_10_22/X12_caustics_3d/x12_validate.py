#!/usr/bin/env python3
"""X12 validation collector (FROZEN_CRITERIA §4): R-X10, V-a1, V-cm, X-ISO, X-B0.
  python3 x12_validate.py            -> x12_validate.out, x12_validate_results.json        (exit 0 iff all PASS)
  X12_MUTATE=1 python3 x12_validate.py -> x12_validate_MUTATE.out, _results_MUTATE.json (V-cm and X-ISO on MUTATE runs)
"""
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
X10 = HERE.parent / "X10_caustics_comoving"
MUTATE = os.environ.get("X12_MUTATE", "0") == "1"
SUF = "_MUTATE" if MUTATE else ""
W_A = 18.067 - 9.0
lines, out = [], {"mutate_wrong_sign": MUTATE, "checks": []}


def say(s=""):
    print(s)
    lines.append(s)


def load(p):
    p = Path(p)
    return json.loads(p.read_text()) if p.exists() else None


def run3(tag):
    return load(HERE / "runs" / f"{tag}{SUF}.json")


def tol_of(t2d, t_i):
    return max(0.5, 0.1 * (t2d - t_i))


def g(d, *ks):
    for k in ks:
        if d is None:
            return None
        d = d.get(k) if isinstance(d, dict) else None
    return d


checks = out["checks"]
# ---------------- R-X10
if not MUTATE:
    ref = load(X10 / "x10_validate_results.json")
    ok, rows = True, []
    for row in ref["D_ISO"]:
        if row["mass"] != "MW":
            continue
        for h, p in row["per_h"].items():
            r = load(HERE / "work" / f"x2d_iso_MW_{row['foot']}_h{h}.json")
            if r is None:
                ok = False
                rows.append({"foot": row["foot"], "h": h, "missing": True})
                continue
            w = r["wake"]
            pairs = {"down_event.t": (g(p, "down_event", "t"), g(w, "down", "event", "t")),
                     "down_min.J": (g(p, "down_min", "J"), g(w, "down", "min", "J")),
                     "up_min.J": (g(p, "up_min", "J"), g(w, "up", "min", "J")),
                     "up_event.t": (g(p, "up_event", "t"), g(w, "up", "event", "t")),
                     "D_EDGE.J": (g(p, "D_EDGE", "J"), g(r, "D_EDGE", "J")),
                     "D_STIFF.J": (g(p, "D_STIFF", "J"), g(r, "D_STIFF", "J"))}
            rr = {}
            for k, (a, b) in pairs.items():
                if a is None or b is None:
                    good, diff = (a is None and b is None), None
                else:
                    diff = abs(a - b)
                    good = diff <= 1e-9 * max(1.0, abs(a))
                ok &= good
                rr[k] = {"x10": a, "here": b, "abs_diff": diff, "ok": good}
            rows.append({"foot": row["foot"], "h": int(h), "fields": rr,
                         "Wa": {"down_event_t": g(r, "wake_Wa", "down", "event", "t"),
                                "down_min_J": g(r, "wake_Wa", "down", "min", "J"),
                                "up_min_J": g(r, "wake_Wa", "up", "min", "J")}, "wall_s": r["wall_s"]})
    checks.append({"check": "R-X10", "pass": bool(ok), "rows": rows})
    say(f"R-X10  {'PASS' if ok else 'FAIL'}  X10's 2D D-ISO (MW, both footings, h 20/10/5) reproduced, tol 1e-9 rel")
    for r in rows:
        if r.get("missing"):
            say(f"       {r['foot']} h {r['h']}: missing")
            continue
        say(f"       {r['foot']:9s} h {r['h']:2d}: " + "; ".join(f"{k} {v['here']} (diff {v['abs_diff']})"
                                                         for k, v in r["fields"].items()))
        say(f"                       window [0, {W_A:.3f}]: down event {r['Wa']['down_event_t']}, down min "
            f"{r['Wa']['down_min_J']:.4f}, up min {r['Wa']['up_min_J']:.4f}")
    # ---------------- V-a1
    ok, rows = True, []
    for foot in ("canonical", "alt"):
        for h in (20, 15, 10):
            r = run3(f"static_M31_{foot}_h{h}")
            if r is None:
                ok = False
                rows.append({"foot": foot, "h": h, "missing": True})
                continue
            v = r["vstat"]
            good = v["mx_all"] <= 1e-4 and v["disp_all"] <= 1e-2 and not any(r["flags"].values())
            ok &= good
            rows.append({"foot": foot, "h": h, "max_absJm1": v["mx_all"], "max_disp_kpc": v["disp_all"],
                         "flags": r["flags"], "pass": good})
    checks.append({"check": "V-a1", "pass": bool(ok), "rows": rows})
    say(f"V-a1   {'PASS' if ok else 'FAIL'}  static M31, 10 Gyr: max|J-1| <= 1e-4 and displacement <= 1e-2 kpc at every h")
    for r in rows:
        say(f"       {r['foot']:9s} h {r['h']:2d}: " + ("missing" if r.get("missing") else
                                                     f"max|J-1| {r['max_absJm1']:.2e}  disp {r['max_disp_kpc']:.2e} kpc"))
# ---------------- V-cm
ok, rows = True, []
for mass in ("MW", "M31"):
    rr = {h: run3(f"vcm_{mass}_canonical_h{h}") for h in (20, 15, 10)}
    if rr[15] is None or rr[10] is None:
        ok = False
        rows.append({"mass": mass, "missing": True})
        continue
    v15, v10 = rr[15]["vstat"]["mx_out"], rr[10]["vstat"]["mx_out"]
    good = v15 <= 0.1 and v10 <= 0.1 and v10 <= v15
    ok &= good
    rows.append({"mass": mass, "pass": good,
                 "max_absJm1_outside": {h: (rr[h]["vstat"]["mx_out"] if rr[h] else None) for h in rr},
                 "t_of_max": {h: (rr[h]["vstat"]["t_mx_out"] if rr[h] else None) for h in rr},
                 "max_absJm1_inside_2eps": {h: (rr[h]["vstat"]["mx_in"] if rr[h] else None) for h in rr},
                 "max_comoving_disp_outside": {h: (rr[h]["vstat"]["disp_out"] if rr[h] else None) for h in rr},
                 "flags": {h: (rr[h]["flags"] if rr[h] else None) for h in rr},
                 "hold_iters_per_call": {h: (rr[h]["hold_iters_per_call"] if rr[h] else None) for h in rr}})
checks.append({"check": "V-cm", "pass": bool(ok), "rows": rows})
say(f"V-cm   {'PASS' if ok else 'FAIL'}  boosted single mass, 15.167 Gyr, canonical: max|J-1| (2eps..300 kpc) <= 0.1 at h 15 "
    f"and 10, h 10 <= h 15{' (WRONG-SIGN BOOST)' if MUTATE else ''}")
for r in rows:
    if r.get("missing"):
        say(f"       {r['mass']}: missing")
        continue
    o = r["max_absJm1_outside"]
    say(f"       {r['mass']:3s}: h20 {o[20]}  h15 {o[15]:.4e}  h10 {o[10]:.4e}  inside 2eps {r['max_absJm1_inside_2eps']}  "
        f"disp {r['max_comoving_disp_outside']}  F3 {[(h, (f or {}).get('F3')) for h, f in r['flags'].items()]}")
# ---------------- X-ISO
ok, rows = True, []
for foot in ("canonical", "alt"):
    for h in (20, 10):
        r2 = load(HERE / "work" / f"x2d_iso_MW_{foot}_h{h}.json")
        r3 = run3(f"wake_{foot}_h{h}")
        if r2 is None or r3 is None:
            ok = False
            rows.append({"foot": foot, "h": h, "missing": True})
            continue
        t2 = g(r2, "wake_Wa", "down", "event", "t")
        u2 = g(r2, "wake_Wa", "up", "min", "J")
        e3 = g(r3, "wake", "MW_down", "event")
        t3 = e3["t"] if e3 and e3["t"] <= r3["t_wake_end"] + 1e-9 else None
        u3 = g(r3, "wake", "MW_up", "min_W", "J")
        if t2 is not None and t3 is not None:
            tl = tol_of(t2, 0.0)
            good_t = abs(t3 - t2) <= tl
        else:
            tl, good_t = None, False
        good_u = (u2 is not None and u3 is not None and (u2 > 0.5) == (u3 > 0.5))
        good = good_t and good_u
        ok &= good
        rows.append({"foot": foot, "h": h, "t_c_2d": t2, "t_c_3d": t3, "tol": tl, "J_up_2d": u2, "J_up_3d": u3,
                     "J_down_3d": g(r3, "wake", "MW_down", "min_W", "J"), "pass": good,
                     "event_3d": e3})
notrun = all(r.get("missing") for r in rows)
checks.append({"check": "X-ISO", "pass": bool(ok), "not_run": notrun, "rows": rows})
say(f"X-ISO  {'NOT RUN (the lane stopped at V-cm, FROZEN §4)' if notrun else ('PASS' if ok else 'FAIL')}  3D wake (case W) vs 2D at matched h 20, 10: downstream t_c within max(0.5, 0.1 t_c), "
    f"J_up same side of 0.5")
for r in rows:
    if r.get("missing"):
        say(f"       {r['foot']} h {r['h']}: missing")
        continue
    e3 = r["event_3d"]
    where = (f"; 3D event label {[round(v) for v in e3['label']]} at {[round(v) for v in e3['pos']]}, dz {e3['dz_MW']:.0f}, "
             f"sv {[round(v, 3) for v in e3['sv_at_confirm']]}") if e3 else ""
    say(f"       {r['foot']:9s} h {r['h']:2d}: t_c 2D {r['t_c_2d']}  3D {r['t_c_3d']}  (tol {r['tol']}); J_up 2D "
        f"{r['J_up_2d']:.4f} 3D {r['J_up_3d']}{where}  {'ok' if r['pass'] else 'X'}")
# ---------------- X-B0
if not MUTATE:
    ok_i, ok_ii, rows = True, True, []
    for foot in ("canonical", "alt"):
        for h in (20, 10):
            r2 = load(X10 / "runs" / f"{foot}_O2_ti3_h{h}.json")
            r3 = run3(f"enc_b0_{foot}_h{h}")
            if r3 is None:
                ok_i = ok_ii = False
                rows.append({"foot": foot, "h": h, "missing": True})
                continue
            t2s, t3s = g(r2, "event", "t"), g(r3, "soft", "event", "t")
            t2w, t3w = g(r2, "WAKE_5b", "MW_down", "event", "t"), g(r3, "wake", "MW_down", "event", "t")
            gi = t2s is not None and t3s is not None and abs(t3s - t2s) <= tol_of(t2s, 3.0)
            gii = t2w is not None and t3w is not None and abs(t3w - t2w) <= tol_of(t2w, 3.0)
            ok_i &= gi
            ok_ii &= gii
            rows.append({"foot": foot, "h": h, "soft_t_c_2d": t2s, "soft_t_c_3d": t3s,
                         "soft_tol": tol_of(t2s, 3.0) if t2s else None, "pass_i": gi, "wake_t_c_2d": t2w,
                         "wake_t_c_3d": t3w, "wake_tol": tol_of(t2w, 3.0) if t2w else None, "pass_ii": gii,
                         "S_2d": g(r2, "S", "J"), "S_3d": g(r3, "soft", "S", "J"),
                         "soft_event_3d": g(r3, "soft", "event")})
    notrun = all(r.get("missing") for r in rows)
    checks.append({"check": "X-B0", "pass": bool(ok_i and ok_ii), "pass_i": bool(ok_i), "pass_ii": bool(ok_ii),
                   "not_run": notrun, "rows": rows})
    say(f"X-B0   {'NOT RUN (the lane stopped at V-cm, FROZEN §4)' if notrun else ('PASS' if ok_i and ok_ii else 'FAIL')}  3D encounter b = 0 vs X10 2D O2 t_i 3 at matched h 20, 10: (i) soft "
        f"t_c{'' if notrun else (' PASS' if ok_i else ' FAIL')}, (ii) MW downstream wake t_c"
        f"{'' if notrun else (' PASS' if ok_ii else ' FAIL')}; tol max(0.5, 0.1 (t_c - t_i))")
    for r in rows:
        if r.get("missing"):
            say(f"       {r['foot']} h {r['h']}: missing")
            continue
        say(f"       {r['foot']:9s} h {r['h']:2d}: soft t_c 2D {r['soft_t_c_2d']:.3f} 3D {r['soft_t_c_3d']} (tol "
            f"{r['soft_tol']:.2f}) {'ok' if r['pass_i'] else 'X'}; wake t_c 2D {r['wake_t_c_2d']:.3f} 3D "
            f"{r['wake_t_c_3d']} (tol {r['wake_tol']:.2f}) {'ok' if r['pass_ii'] else 'X'}")
npass = sum(c["pass"] for c in checks)
nnr = sum(bool(c.get("not_run")) for c in checks)
say(f"{npass}/{len(checks)} PASS, {len(checks) - npass - nnr} FAIL, {nnr} NOT RUN" + (" (MUTATE: wrong-sign boost; V-cm must FAIL)" if MUTATE else ""))
(HERE / f"x12_validate{SUF}.out").write_text("\n".join(lines) + "\n")
(HERE / f"x12_validate_results{SUF}.json").write_text(json.dumps(out, indent=1, default=float))
sys.exit(0 if (MUTATE or npass == len(checks)) else 1)
