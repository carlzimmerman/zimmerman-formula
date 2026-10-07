#!/usr/bin/env python3
"""SCAN: coincidences between OpenAI's math manuscript abstracts and the record's numbers.  Frozen: FROZEN_CRITERIA.md (e4f290229).
Input: ../../../_external_data/openai_math/CONTENTS.md (read-only, data).  SCAN_MUTATE=1 multiplies every extracted value by 1.037."""
import os, re, math, json
from scipy.stats import poisson
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.abspath(os.path.join(HERE, "..", "..", "..", "_external_data", "openai_math", "CONTENTS.md"))
MUTATE = os.environ.get("SCAN_MUTATE") == "1"; SLUG = "scan" + ("_MUTATE" if MUTATE else "")
LOG, OUT = [], {"mutate": MUTATE}
def P(s=""): print(s); LOG.append(s)
TARGETS = {"kappa 1/2": 0.5, "1/sqrt(32pi)": 1 / math.sqrt(32 * math.pi), "32pi": 32 * math.pi, "1/(2pi)": 1 / (2 * math.pi),
           "Omega_c/Omega_b 5.364": 5.364, "Z 5.7888": 5.7888, "Delta_ta(0) 11.806": 11.806, "Delta_ta(0.25) 8.893": 8.893,
           "level 0.13": 0.13, "level 0.60": 0.60, "e^-2": math.exp(-2), "beta 6.684": 6.684}
TRIVIAL = {1.0, 2.0, 3.0, 4.0}
text = open(SRC, encoding="utf-8").read()
# split into result entries to keep context
entries = re.split(r"\n\*\*(\d{3})\. ", text)
ctx = {}
for i in range(1, len(entries) - 1, 2):
    ctx[entries[i]] = entries[i + 1]
PIW = {"": 1.0, "\\pi": math.pi, "π": math.pi}
vals = []
num = r"(\d+(?:\.\d+)?)"
for rid, body in ctx.items():
    b = body.replace("\\tfrac", "\\frac").replace("\\dfrac", "\\frac")
    for m in re.finditer(r"\\frac\{" + num + r"\}\{" + num + r"\s*(\\pi)?\}", b):          # \frac{a}{b} and \frac{a}{b\pi}
        a, c = float(m.group(1)), float(m.group(2)); v = a / c / (math.pi if m.group(3) else 1.0)
        vals.append((v, rid, m.group(0)))
    for m in re.finditer(r"(?<![\w.])" + num + r"\s*/\s*\(?" + num + r"\s*(\\pi|π)?\)?", b):   # a/b, a/(b pi)
        a, c = float(m.group(1)), float(m.group(2))
        if c == 0: continue
        vals.append((a / c / (math.pi if m.group(3) else 1.0), rid, m.group(0)))
    for m in re.finditer(r"(?<![\w.\\])(\d+)\s*(\\pi|π)", b):                                 # k pi
        vals.append((float(m.group(1)) * math.pi, rid, m.group(0)))
    for m in re.finditer(r"(?<![\w.])(\d+\.\d+)", b):                                        # decimals
        vals.append((float(m.group(1)), rid, m.group(0)))
    for m in re.finditer(r"\\sqrt\{" + num + r"\}", b):
        vals.append((math.sqrt(float(m.group(1))), rid, m.group(0)))
vals = [(v * (1.037 if MUTATE else 1.0), r, s) for v, r, s in vals if v > 0 and v not in TRIVIAL]
# dedupe identical (value, result) pairs
seen, V = set(), []
for v, r, s in vals:
    k = (round(v, 9), r)
    if k not in seen:
        seen.add(k); V.append((v, r, s))
P(f"SCAN{' MUTATE' if MUTATE else ''}: {len(ctx)} result entries; {len(V)} distinct non-trivial constants extracted")
xs = [v for v, _, _ in V]; lo, hi = min(xs), max(xs)
for tol in (0.01, 0.0025):
    hits = []
    for name, t in TARGETS.items():
        for v, r, s in V:
            if abs(math.log(v / t)) < math.log(1 + tol):
                hits.append((name, t, v, r, s))
    p1 = 2 * math.log(1 + tol) / math.log(hi / lo); lam = len(V) * len(TARGETS) * p1
    pval = float(poisson.sf(len(hits) - 1, lam)) if hits else 1.0
    OUT[f"tol{tol}"] = dict(n_hits=len(hits), expected=lam, p=pval, hits=[dict(target=h[0], value=h[2], result=h[3], text=h[4]) for h in hits])
    P(f"\n  tolerance {tol:.2%}: matches {len(hits)} vs chance expectation {lam:.1f} (range {lo:.3g}..{hi:.3g}); Poisson p(>= obs) = {pval:.3f}")
    for name, t, v, r, s in hits:
        title = ctx[r].split("**")[0][:90]
        P(f"     {name:24s} <- {v:.5g}  [result {r}: {title}]  text: {s}")
verdict = "EXCESS" if OUT["tol0.01"]["p"] < 0.01 else "CONSISTENT WITH CHANCE"
OUT["verdict"] = verdict; P(f"\n{'MUTATE ' if MUTATE else ''}VERDICT (1% tolerance): {verdict}")
open(os.path.join(HERE, SLUG + ".out"), "w").write("\n".join(LOG) + "\n")
json.dump(OUT, open(os.path.join(HERE, SLUG + "_results.json"), "w"), indent=1)
