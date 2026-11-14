"""NUF1 collector: applies FROZEN_CRITERIA.md to the per-mode JSON files. Usage: python3 nuf1_collect.py"""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
def load(m):
    p = os.path.join(HERE, f"nuf1_{m}.json")
    return json.load(open(p)) if os.path.exists(p) else None
lines = []
def say(s=""): print(s); lines.append(s)

checks = {k: load(k) for k in ("K1", "K2A", "K2B", "K3")}
ok = all(c is not None and c.get("passed") for c in checks.values())
say("NUF1 collector")
for k, c in checks.items():
    say(f"  {k}: {'MISSING' if c is None else ('PASS' if c['passed'] else 'FAIL')}")
say(f"  all known-answer checks pass: {ok}")

def word(D):
    if D >= 9: return "FLOOR EXCLUDED AT 3 SIGMA"
    if D >= 4: return "FLOOR DISFAVOURED"
    return "FLOOR ALLOWED"
def sig(D): return float(np.sqrt(max(D, 0.0)))
def fmt(x): return "open" if x is None else f"{x:+.3f}"

rows = {}
say("")
say("mode | best m [eV] | 68% | 95% | chi2_min | D(0.059) | D(0.10) | word (NO floor)")
for m in ("primary", "ctl_noLRG1", "ctl_noLRG2", "ctl_lyaAP", "ctl_zgt06",
          "ro_w0wa", "ro_widen", "ro_hfixed", "ro_thetamean"):
    r = load(m)
    if r is None: say(f"{m}: MISSING"); continue
    S = r["summary"]; w = word(S["D_floor_NO"])
    rows[m] = dict(m_best=S["m_best"], ci68=S["ci68"], ci95=S["ci95"], chi2_min=S["chi2_min"],
                   D_NO=S["D_floor_NO"], D_IO=S["D_floor_IO"], sqrtD_NO=sig(S["D_floor_NO"]),
                   sqrtD_IO=sig(S["D_floor_IO"]), D_m0=S["D_m0"], word=w, at_grid_edge=S["at_grid_edge"])
    say(f"{m} | {S['m_best']:+.3f} | [{fmt(S['ci68'][0])}, {fmt(S['ci68'][1])}] | [{fmt(S['ci95'][0])}, "
        f"{fmt(S['ci95'][1])}] | {S['chi2_min']:.2f} | {S['D_floor_NO']:.2f} ({sig(S['D_floor_NO']):.2f} sig) | "
        f"{S['D_floor_IO']:.2f} ({sig(S['D_floor_IO']):.2f} sig) | {w}")

first = rows.get("primary", {}).get("word")
ctl = [c for c in ("ctl_noLRG1", "ctl_noLRG2", "ctl_lyaAP", "ctl_zgt06") if c in rows]
changed = [c for c in ctl if rows[c]["word"] != first]
second = None if first is None or len(ctl) < 4 else ("ROBUST" if not changed else "FRAGILE")
say("")
if not ok:
    say("FROZEN WORDS: NOT EVALUABLE (a known-answer check failed or is missing)")
    say(f"  reading (not a verdict): {first} / {second}" + (f" (changed by {', '.join(changed)})" if changed else ""))
else:
    say(f"FROZEN WORDS: {first} / {second}" + (f" (changed by {', '.join(changed)})" if changed else ""))
res = dict(checks={k: (None if c is None else c.get("passed")) for k, c in checks.items()}, checks_pass=ok,
           word1=first if ok else "NOT EVALUABLE", word2=second if ok else "NOT EVALUABLE",
           reading=dict(word1=first, word2=second, changed_by=changed), rows=rows)
json.dump(res, open(os.path.join(HERE, "nuf1_results.json"), "w"), indent=1)
open(os.path.join(HERE, "nuf1_collect.out"), "w").write("\n".join(lines) + "\n")
