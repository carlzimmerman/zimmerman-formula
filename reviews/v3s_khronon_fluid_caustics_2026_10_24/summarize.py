#!/usr/bin/env python3
"""Score V3, V5, V6 and the frozen C reading from runs/*.json; list the h = 10 rung cases (frozen rule)."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = {p.stem: json.loads(p.read_text()) for p in (HERE / "runs").glob("*.json") if not p.stem.startswith(("smoke", "v4_"))}
checks, out = [], {}


def record(name, ok, detail):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"{name:4s} {'PASS' if ok else 'FAIL'}  {detail}")


def key(mode, foot, orb, ti, h):
    return f"{mode}_{foot}_{orb}_ti{ti:g}_h{h:g}"


cases = [(f, o, t) for f in ("canonical", "alt") for o in ("O1", "O2") for t in (3, 6, 9)]
sc20 = {c: R.get(key("sc", *c, 20)) for c in cases}
missing = [c for c, v in sc20.items() if v is None]
if missing:
    print("missing h=20 sc runs:", missing)
# V3
eq = [(c, v["eq_rel"], v.get("eq_rel_without_gammaL")) for c, v in sc20.items() if v]
record("V3", all(e[1] <= 1e-6 for e in eq), "equilibrium max|a|/max|grad phi| at t_i: " +
       ", ".join(f"{c[0][:3]} {c[1]} {c[2]}: {e1:.1e} (no gamma_L {e2:.1e})" for c, e1, e2 in eq))
# V5
mu = {c: R.get(key("mutate", *c, 20)) for c in cases}
v5 = [(c, v["disp_max"] / 20.0, max(abs(v["softJmin_to_ext"] - 1), abs(v["stiffJmin_to_t_end"] - 1))) for c, v in mu.items() if v]
record("V5", len(v5) == 12 and all(d <= 1e-3 and j <= 1e-3 for _, d, j in v5),
       f"static masses, {len(v5)} runs: max displacement {max(d for _, d, _ in v5):.1e} h, max |J - 1| {max(j for _, _, j in v5):.1e}")
# V6
prev = {3: 14.44, 6: 15.43, 9: 16.44}
v6 = []
for ti in (3, 6, 9):
    v = R.get(key("frozen", "canonical", "O2", ti, 20))
    if v:
        fc = v["first_cross"]
        v6.append((ti, fc["t_sc"] if fc else None))
record("V6", len(v6) == 3 and all(t is not None and abs(t - prev[ti]) <= 1.0 for ti, t in v6),
       "frozen-F mode, canonical O2: t_sc " + ", ".join(f"t_i {ti}: {t if t is None else round(t, 2)} (prev lane {prev[ti]})" for ti, t in v6))
# C at h = 20
rows = []
for c, v in sc20.items():
    if not v:
        continue
    fc = v["first_cross"]
    cross = fc is not None and fc["t_sc"] <= v["t_end"] + 1e-9
    rows.append({"case": c, "softJmin": v["softJmin_to_t_end"], "t_min": v["t_softJmin"], "cross": cross,
                 "t_sc": fc["t_sc"] if fc else None, "dist_gal": fc["dist_gal"] if fc else None,
                 "stiffJmin": v["stiffJmin_to_t_end"], "halo_i": v["halo_t_i"], "halo_end": v["halo_t_end"],
                 "gauss_worst": v.get("gauss_worst_residual"), "wall_s": v["wall_s"]})
    print(f"   h20 {c[0]:9s} {c[1]} t_i {c[2]}: soft Jmin {v['softJmin_to_t_end']:+9.3f} at {v['t_softJmin']:.2f}; "
          f"{'CROSS at %.2f (t0%+.2f), %.0f kpc from a galaxy' % (fc['t_sc'], fc['t_sc'] - 13.8, fc['dist_gal']) if cross else 'no crossing'}; "
          f"stiff Jmin {v['stiffJmin_to_t_end']:+.1f}; halo mass ratio MW {v['halo_t_end'][0]['mass'] / v['halo_t_i'][0]['mass']:.2f} "
          f"M31 {v['halo_t_end'][1]['mass'] / v['halo_t_i'][1]['mass']:.2f}; gauss worst {v.get('gauss_worst_residual', float('nan')):.1e}")
out["h20"] = rows
rung = set()
for foot in ("canonical", "alt"):
    fr = sorted([r for r in rows if r["case"][0] == foot], key=lambda r: r["softJmin"])[:2]
    rung |= {r["case"] for r in fr}
rung |= {r["case"] for r in rows if r["cross"]}
out["rung_cases"] = sorted(rung)
print("RUNG (h = 10):", sorted(rung))
# C reading if rung results exist
rung_done = {c: R.get(key("sc", *c, 10)) for c in rung}
if all(rung_done.values()) and rung_done:
    conf = []
    for c, v in rung_done.items():
        r20 = [r for r in rows if r["case"] == c][0]
        fc = v["first_cross"]
        cross10 = fc is not None and fc["t_sc"] <= v["t_end"] + 1e-9
        conf.append((c, r20["cross"], cross10, r20["t_sc"], fc["t_sc"] if fc else None, v["softJmin_to_t_end"]))
        print(f"   h10 {c}: soft Jmin {v['softJmin_to_t_end']:+.3f}; cross {cross10} at {fc['t_sc'] if fc else None}; h20 cross {r20['cross']} at {r20['t_sc']}")
    sc_cross = [x for x in conf if x[1] and x[2] and abs(x[3] - x[4]) <= 1.0]
    if sc_cross:
        reading = "SELF-CONSISTENT SHELL CROSSING"
    elif all(r["softJmin"] > 0.5 for r in rows) and all(x[5] > 0.5 for x in conf):
        reading = "NO SHELL CROSSING"
    else:
        reading = "UNDECIDED"
    disagree = [x[0] for x in conf if x[1] != x[2]]
    out.update({"reading": reading, "confirmed": [x[0] for x in sc_cross], "h20_h10_disagree": disagree})
    record("C", True, f"reading {reading}; confirmed crossings {[x[0] for x in sc_cross]}; h20/h10 disagree {disagree}")
out["checks"] = checks
(HERE / "summary.json").write_text(json.dumps(out, indent=1, default=str))
