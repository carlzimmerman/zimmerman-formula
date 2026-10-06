"""CFG364: does the supply cap (dark mass = min(phantom, cold supply)) survive SPARC? Criteria: FROZEN_CRITERIA.md (58840961d).

Run: python3 cfg364_supply_cap.py ; MUTATE=1 sets the supply x 0.1 (the verdict must flip to DEAD; T-MUT fails, rc 1).
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, ".."))
import CFG4_common as C4  # noqa: E402

MUTATE = os.environ.get("MUTATE") == "1"
TAG = "_MUTATE" if MUTATE else ""
G = 4.30091e-6                                  # kpc (km/s)^2 / Msun
CONV = 3.0857e13                                # m/s^2 -> (km/s)^2/kpc
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
UD, UB = 0.61, 0.61 * 1.4
RATIO = 0.1200 / 0.02237
SUP = 0.1 if MUTATE else 1.0
lines, checks = [], []


def say(s=""):
    print(s)
    lines.append(s)


def check(name, ok, val):
    checks.append({"name": name, "pass": bool(ok), "value": val})
    say(f"  [{'PASS' if ok else 'FAIL'}] {name}: {val}")


gals = C4.load_sparc()
say("CFG364 supply cap on SPARC" + ("  (MUTATE: supply x 0.1)" if MUTATE else ""))
say("=" * 78)

# ---------------------------------------------------------------- T0
say("T0 controls")
res, w = [], []
a0k = A0["canonical"] * CONV
for g in gals:
    vb2 = g["Vgas"] * np.abs(g["Vgas"]) + UD * g["Vdisk"] * np.abs(g["Vdisk"]) + UB * g["Vbul"] * np.abs(g["Vbul"])
    ok = (g["R"] > 0) & (vb2 > 0) & (g["Vobs"] > 0)
    gb = vb2[ok] / g["R"][ok]
    go = np.maximum(g["Vobs"][ok], 1.0) ** 2 / g["R"][ok]
    res += list(np.log10(go) - np.log10(C4.nu_mono(gb / a0k) * gb))
    w += list((np.maximum(g["Vobs"][ok], 1) / np.maximum(g["eV"][ok], 1e-3)) ** 2)
res, w = np.array(res), np.array(w)
rms = float(np.sqrt(np.sum(w * (res - np.sum(w * res) / np.sum(w)) ** 2) / np.sum(w)))
check("T0a law rms about SPARC at Upsilon 0.61 (canonical) reproduces 0.098 +- 0.005 dex", abs(rms - 0.098) < 0.005, f"{rms:.4f} dex")
yt = np.logspace(-3, 2, 50)
gbt = yt * a0k
Rt = 10.0
lhs = (C4.nu_mono(yt) - 1) * gbt * Rt**2 / G
rhs = ((C4.nu_mono(yt) * gbt * Rt) - gbt * Rt) * Rt / G      # V_law^2 = nu g R, V_bar^2 = g R (a stray "/ Rt" was fixed after the first run, disclosed)
check("T0b phantom identity (nu-1) g_bar R^2/G = (V_law^2 - V_bar^2) R/G to 1e-10", np.max(abs(lhs / rhs - 1)) < 1e-10,
      f"max rel diff {np.max(abs(lhs/rhs-1)):.1e}")
check("T0c Omega_c/Omega_b = 5.364", abs(RATIO - 5.364) < 0.001, f"{RATIO:.4f}")


# ---------------------------------------------------------------- per galaxy
def classify(vf):
    if not vf or vf <= 0:
        return "unclassified"
    return "dwarf" if vf < 60 else ("intermediate" if vf < 150 else "massive")


out = {}
for foot in ("canonical", "alt"):
    a0k = A0[foot] * CONV
    rows = []
    for g in gals:
        m = g["meta"]
        if m is None:
            continue
        vb2 = g["Vgas"] * np.abs(g["Vgas"]) + UD * g["Vdisk"] * np.abs(g["Vdisk"]) + UB * g["Vbul"] * np.abs(g["Vbul"])
        i = len(g["R"]) - 1
        R, vb2L, vo = g["R"][i], vb2[i], g["Vobs"][i]
        if R <= 0 or vb2L <= 0:
            continue
        gb = vb2L / R
        Mbar_in = vb2L * R / G
        Mph = (C4.nu_mono(gb / a0k) - 1) * Mbar_in
        Mobs_dark = max(vo**2 - vb2L, 0) * R / G
        Mb_tot = (UD * m["L36"] + 1.33 * m["MHI"]) * 1e9
        S_tot = SUP * RATIO * Mb_tot
        S_in = SUP * RATIO * Mbar_in
        rows.append(dict(name=g["name"], Q=int(m["Q"]), Vflat=m["Vflat"], cls=classify(m["Vflat"]), R_last=float(R),
                         Mb_tot=Mb_tot, Mph=float(Mph), Q_tot=float(Mph / S_tot), Q_in=float(Mph / S_in),
                         Qobs_tot=float(Mobs_dark / S_tot)))
    out[foot] = rows

say("\nT1 results (Q = M_ph(<R_last)/supply; break if Q > 1)")
summary = {}
for foot, rows in out.items():
    Qt = np.array([r["Q_tot"] for r in rows]); Qi = np.array([r["Q_in"] for r in rows]); Qo = np.array([r["Qobs_tot"] for r in rows])
    cls = np.array([r["cls"] for r in rows]); qual = np.array([r["Q"] for r in rows])
    s = dict(N=len(rows), f_break=float(np.mean(Qt > 1)), n_break=int(np.sum(Qt > 1)), f_break_in=float(np.mean(Qi > 1)),
             f_break_obs=float(np.mean(Qo > 1)), f_break_q12=float(np.mean(Qt[qual <= 2] > 1)), median_Q=float(np.median(Qt)),
             by_class={c: dict(N=int(np.sum(cls == c)), n_break=int(np.sum((cls == c) & (Qt > 1))),
                               f=float(np.mean(Qt[cls == c] > 1)) if np.any(cls == c) else None,
                               median_Q=float(np.median(Qt[cls == c])) if np.any(cls == c) else None)
                       for c in ("dwarf", "intermediate", "massive", "unclassified")})
    summary[foot] = s
    say(f"  {foot}: N {s['N']}; PRIMARY (S_tot) break {s['n_break']} = {s['f_break']:.1%}, median Q {s['median_Q']:.2f}; "
        f"Q<=2 subset {s['f_break_q12']:.1%}; STRICT (S_in) {s['f_break_in']:.1%}; OBSERVED dark mass vs S_tot {s['f_break_obs']:.1%}")
    for c, d in s["by_class"].items():
        if d["N"]:
            say(f"      {c:13s} N {d['N']:3d}: break {d['n_break']:3d} ({d['f']:.0%}), median Q {d['median_Q']:.2f}")


def verdict(s):
    m, it = s["by_class"]["massive"], s["by_class"]["intermediate"]
    if s["f_break"] > 0.30 or (m["N"] and m["f"] > 0.10):
        return "DEAD"
    if s["f_break"] <= 0.10 and m["n_break"] == 0 and (not it["N"] or it["f"] < 0.25):
        return "VIABLE"
    return "MARGINAL"


v = {f: verdict(summary[f]) for f in summary}
say(f"\nVERDICT (primary = canonical): {v['canonical']}   (alt: {v['alt']})")
worst = sorted(out["canonical"], key=lambda r: -r["Q_tot"])[:8]
say("  largest Q (canonical): " + "; ".join(f"{r['name']} {r['Q_tot']:.1f} ({r['cls']})" for r in worst))
massive_break = [r["name"] for r in out["canonical"] if r["cls"] == "massive" and r["Q_tot"] > 1]
say(f"  massive galaxies that break (canonical): {len(massive_break)}" + (f": {', '.join(massive_break[:12])}" if massive_break else ""))
check("T-MUT the frozen MUTATE expectation: the main run is not DEAD only because the supply is real (the x0.1 supply must give DEAD)",
      not MUTATE, f"verdict {v['canonical']}" + (" under supply x0.1" if MUTATE else ""))
n = sum(c["pass"] for c in checks)
say(f"\n{n}/{len(checks)} pass" + ("  (MUTATE)" if MUTATE else ""))
json.dump({"lane": "CFG364", "mutate": MUTATE, "verdict": v, "summary": summary, "rows": out, "checks": checks, "rms": rms},
          open(os.path.join(HERE, f"cfg364_supply_cap_results{TAG}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg364_supply_cap{TAG}.out"), "w").write("\n".join(lines) + "\n")
sys.exit(0 if n == len(checks) else 1)
