"""CFG855 -- exhaustive closed-form search for Omega_c/Omega_b = 5.364 +- 0.065 with a look-elsewhere base rate.
Criteria: FROZEN_CRITERIA.md (f2fdd004a).  Run: python3 cfg855.py (CFG855_MUTATE=1: target x 1.07).  kappa = 1/2 FITTED; not theory closed."""
import os, json, math, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); MUT = os.environ.get("CFG855_MUTATE") == "1"; OUT = []
def P(s=""):
    print(s, flush=True); OUT.append(str(s))
R0, S = 0.1200 / 0.02237, 0.065
R = R0 * (1.07 if MUT else 1.0)
atoms = {str(i): float(i) for i in range(1, 10)}
atoms.update({"pi": math.pi, "e": math.e, "sqrt2": math.sqrt(2), "sqrt3": math.sqrt(3), "sqrt5": math.sqrt(5), "phi": (1 + 5 ** 0.5) / 2, "Z": 2 * math.sqrt(8 * math.pi / 3)})
key = lambda v: float(f"{v:.12g}")
seen = {}                                     # value key -> (expr, complexity)
L = {1: {}}
for n, v in atoms.items():
    k = key(v); seen.setdefault(k, (n, 1)); L[1][k] = n
def add(level, v, e):
    if not (0.01 <= v <= 100) or not math.isfinite(v): return
    k = key(v)
    if k in seen: return
    seen[k] = (e, level); L[level][k] = e
for c in range(2, 6):
    L[c] = {}
    for v, e in list(L[c - 1].items()):
        add(c, math.sqrt(v), f"sqrt({e})"); add(c, v * v, f"({e})^2")
    for i in range(1, c - 1):
        j = c - 1 - i
        for va, ea in L[i].items():
            for vb, eb in L[j].items():
                add(c, va + vb, f"({ea}+{eb})"); add(c, va - vb, f"({ea}-{eb})"); add(c, va * vb, f"{ea}*{eb}")
                if vb != 0: add(c, va / vb, f"{ea}/{eb}")
vals = np.array(sorted(seen)); P(f"CFG855  closed-form search" + ("  [MUTATE target x1.07]" if MUT else "") + f"   distinct values in [0.01, 100]: {len(vals)}")
P(f"  K1: Z = {key(2 * math.sqrt(8 * math.pi / 3)) in seen}  16/3 = {key(16 / 3) in seen}")
def nhit(t, rel=S / R0): return int(np.sum(np.abs(vals - t) <= rel * t))
n = nhit(R); P(f"  target R = {R:.4f} +- {S * R / R0:.4f}: {n} distinct values within 1 sigma")
close = sorted(((abs(v - R), v, *seen[v]) for v in vals[np.abs(vals - R) <= S * R / R0]), key=lambda x: (x[0], x[3]))
P("  closest 15 (|diff|/sigma, value, complexity, expression):")
for d, v, e, c in close[:15]: P(f"     {d / S:5.2f}  {v:.6f}  c{c}  {e}")
low = [(d, v, e, c) for d, v, e, c in close if c <= 3 and d <= 0.1 * S]
rng = np.random.default_rng(855); T = np.exp(rng.uniform(math.log(4), math.log(7), 1000)); NR = np.array([nhit(t) for t in T])
pct = float(np.mean(NR < n) * 100); P(f"  random targets (1000, log-uniform 4-7, same 1.2% window): median {np.median(NR):.0f} hits, 99th pct {np.percentile(NR, 99):.0f}; R sits at the {pct:.1f}th percentile")
P(f"  complexity <= 3 within 0.1 sigma: {[(round(v, 6), e) for d, v, e, c in low] or 'none'}")
cls = "SPECIAL" if (n > np.percentile(NR, 99) and low) else "ORDINARY (numerology level)"
P(f"\n  CLASS: {cls}   (no expression is a derivation unless it follows from physics)")
json.dump(dict(lane="CFG855", mutate=MUT, R=R, n_hit=n, closest=[dict(sigma=d / S, value=v, expr=e, complexity=c) for d, v, e, c in close[:30]],
               random_median=float(np.median(NR)), random_p99=float(np.percentile(NR, 99)), percentile=pct, low_complexity_close=[e for d, v, e, c in low], cls=cls),
          open(os.path.join(HERE, f"cfg855_results{'_MUTATE' if MUT else ''}.json"), "w"), indent=1)
open(os.path.join(HERE, f"cfg855{'_MUTATE' if MUT else ''}.out"), "w").write("\n".join(OUT) + "\n")
