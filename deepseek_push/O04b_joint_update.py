#!/usr/bin/env python3
"""O04b -- THREE-CHANNEL JOINT DEEP a0_eff SYNTHESIS (door: O04, register:
'inverse-variance joint update is next-lane arithmetic'). Conductor-run lane
2026-09-24. All channel values read from landed lane files at runtime.
Pre-registered kills in PWAVE_BRIEF.md (K1-K4), written before this run."""
import json, math, os, sys

BASE = os.path.dirname(os.path.abspath(__file__))

def load(name):
    return json.load(open(os.path.join(BASE, name)))

def find_first(d, key, pred=lambda v: True):
    """first occurrence of key with numeric value satisfying pred"""
    if isinstance(d, dict):
        if key in d and isinstance(d[key], (int, float)) and pred(d[key]):
            return d[key]
        for v in d.values():
            r = find_first(v, key, pred)
            if r is not None:
                return r
    elif isinstance(d, list):
        for v in d:
            r = find_first(v, key, pred)
            if r is not None:
                return r
    return None

def dig(d, path):
    cur = d
    for k in path.split('/'):
        cur = cur[k]
    return cur

checks = []
def check(name, ok, detail=""):
    checks.append({"name": name, "pass": bool(ok), "detail": detail})
    return bool(ok)

n05 = load("N05_results.json")
o01 = load("O01_results.json")
o03 = load("O03_results.json")

# --- channel 1: SPARC-deep (N05 sparc-deep block)
delta  = find_first(n05, "Delta",     lambda v: -1e-21 < v < 0)
secl   = find_first(n05, "se_clustered", lambda v: 1e-24 < v < 1e-21)
frac   = find_first(n05, "fraction_a0E", lambda v: 0.1 < v < 0.5)
x_sparc = find_first(n05, "a0eff_a0", lambda v: 0.5 < v < 1.5)
z_sparc = find_first(n05, "z_clustered", lambda v: -10 < v < 0)
a0E = abs(delta) / frac                      # a0 * E[g_bar] in SI
se_sparc = secl / a0E                        # SE on a0eff_a0, derived not quoted
ok = True
ok &= check("C1 SPARC-deep channel found and SE derived from Delta/se/fraction",
            None not in (delta, secl, frac, x_sparc, z_sparc),
            f"Delta={delta:.4e} se_cl={secl:.4e} frac={frac:.4f} -> SE={se_sparc:.4f}")
# cross-check vs O03's quoted cross-block (0.7241 / 0.0662)
xl = dig(o03, "cross_channel_summary/L06/a0eff_a0") if False else find_first(o03, "a0eff_a0", lambda v: 0.5 < v < 1.5)
sl = dig(o03, "L06/se") if "L06" in o03 else None
# O03 stores cross-block under key 'L06' at top level? find it robustly:
def dig2(d, path):
    cur = d
    try:
        for k in path.split('/'):
            cur = cur[k]
        return cur
    except Exception:
        return None
sl = dig2(o03, "cross_check/L06/se")
xl = dig2(o03, "cross_check/L06/a0eff_a0")
if xl is None:
    import re as _re
    for cand in [k for k in o03 if isinstance(o03.get(k), dict) and "L06" in o03[k]]:
        xl = o03[cand]["L06"]["a0eff_a0"]; sl = o03[cand]["L06"]["se"]; break
if xl is None or sl is None:
    ok &= check("C2 O03 cross-block locate", False, "L06 block keys missing")
else:
    ok &= check("C2 SE derivation agrees with O03-quoted cross-block (2e-3)",
                abs(se_sparc - sl) < 2e-3 and abs(x_sparc - xl) < 2e-3,
                f"derived {x_sparc:.4f}+/-{se_sparc:.4f} vs quoted {xl:.4f}+/-{sl:.4f}")

# --- channel 2: G114 dwarfs (O01 primary LT-deep)
x_dwarf = find_first(o01, "a0eff_over_a0", lambda v: 0.3 < v < 0.8)
s_dwarf = find_first(o01, "a0eff_over_a0_SE", lambda v: 0.05 < v < 0.5)
z_dwarf = find_first(o01, "z_vs_1", lambda v: -10 < v < 10)
ok &= check("C3 G114 dwarf channel found", None not in (x_dwarf, s_dwarf, z_dwarf),
            f"{x_dwarf} +/- {s_dwarf}, z_vs_1={z_dwarf}")

# --- channel 3: Milky Way (O03 deepest probe primary_R22)
x_mw = dig2(o03, "deep_fit/deepest_probes/primary_R22/a0eff_over_a0")
s_mw = dig2(o03, "deep_fit/deepest_probes/primary_R22/SE_lin")
ok &= check("C4 MW channel found", None not in (x_mw, s_mw),
            f"{x_mw} +/- {s_mw}")

# --- joint (inverse variance)
xs  = [x_sparc, x_dwarf, x_mw]
ses = [se_sparc, s_dwarf, s_mw]
w   = [1.0/s**2 for s in ses]
xbar = sum(x*wi for x, wi in zip(xs, w)) / sum(w)
se   = 1.0/math.sqrt(sum(w))
chi2 = sum((x-xbar)**2/s**2 for x, s in zip(xs, ses))
zj   = (1.0 - xbar)/se
# route 2: pairwise-fold verification (fold ch1+ch2, then fold with ch3)
x12, s12 = (x_sparc/se_sparc**2 + x_dwarf/s_dwarf**2), (1.0/se_sparc**2 + 1.0/s_dwarf**2)
x12 /= s12; s12 = 1.0/math.sqrt(s12)
x123, s123 = (x12/s12**2 + x_mw/s_mw**2), (1.0/s12**2 + 1.0/s_mw**2)
x123 /= s123; s123 = 1.0/math.sqrt(s123)
ok &= check("C5 joint reproduced by two independent fold routes (1e-12)",
            abs(xbar-x123) < 1e-12 and abs(se-s123) < 1e-12,
            f"xbar={xbar:.6f} se={se:.6f} route2={x123:.6f}+/-{s123:.6f}")
het = chi2 > 5.991   # pre-registered K1 threshold, df=2
res = {
  "lane": "O04b_joint_update",
  "date": "2026-09-24",
  "channels": [
    {"name": "SPARC_deep", "file": "N05_results.json", "x": x_sparc, "se": se_sparc, "z_vs_1": z_sparc},
    {"name": "G114_dwarfs", "file": "O01_results.json", "x": x_dwarf, "se": s_dwarf, "z_vs_1": z_dwarf},
    {"name": "MilkyWay_primary_R22", "file": "O03_results.json", "x": x_mw, "se": s_mw},
  ],
  "joint": {"method": "inverse-variance", "xbar": xbar, "se": se,
            "chi2_df2": chi2, "heterogeneous": het,
            "z_vs_a0": zj,
            "z_vs_a0_dex": math.log10(xbar)/ (se/ (xbar*math.log(10)))},
  "mightee_excluded": {"a0eff_a0": find_first(n05, "a0eff_a0", lambda v: v > 1.5),
                        "z": find_first(n05, "z", lambda v: v > 5),
                        "reason": "K2 pre-registered: opposite-sign mirror, N05 program card arbitrates"},
  "verdict": ("CHANNELS HETEROGENEOUS (K1 fired): joint flagged, not banked"
              if het else
              f"CHANNELS CONSISTENT (chi2={chi2:.3f} <= 5.991, df=2): joint deep a0_eff/a0 = "
              f"{xbar:.4f} +/- {se:.4f}, {zj:.2f} sigma below the canonical a0 = 9.3619e-11 "
              "(C-class observable; two-sided caution: MIGHTEE mirror excluded by pre-registration K2)"),
  "checks": checks,
}
npass = sum(1 for c in checks if c["pass"])
res["summary"] = f"{npass}/{len(checks)} checks PASS"
res["exit_ok"] = ok
with open(os.path.join(BASE, "O04b_joint_update.json"), "w") as f:
    json.dump(res, f, indent=1)
lines = [f"O04b JOINT DEEP a0_eff: {res['summary']}", res["verdict"]]
for c in checks:
    lines.append(f"  [{'PASS' if c['pass'] else 'FAIL'}] {c['name']}  {c['detail']}")
with open(os.path.join(BASE, "O04b.out"), "w") as f:
    f.write("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(0 if ok else 1)
