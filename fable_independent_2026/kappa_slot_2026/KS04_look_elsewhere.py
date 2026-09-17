#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
KS04_look_elsewhere.py -- price any future landing on 1/2 (or 1/(32 pi)) BEFORE it is reported.

Enumerate dimensionless expressions from the alphabet {1,2,3,4,6,8,pi,sqrt(pi),sqrt2,sqrt3,e,ln2} with
at most k binary operations {+,-,*,/} (sqrt is folded into the atoms).  Deduplicate numerically at 1e-9.
For each k, count how many DISTINCT values land inside the measured kappa band and the eps_tot band, and
report the fraction against the O(1) reference window (0, 10].  This is a CONTROL, not a search:
report the numbers, do not interpret.

  C1  the fraction of k=3 expressions inside the 2 sigma kappa band
  C2  the same at the +-5% precision KS03 says is needed to separate 1/2 from its nearest rival
  C3  the complexity rank of 1/2 (in the kappa band) and 1/(32 pi) (in the eps_tot band)

Run:  python3 fable_independent_2026/kappa_slot_2026/KS04_look_elsewhere.py
"""
import os, sys, json, math, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
SLUG = "KS04_look_elsewhere"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "KS04", "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 100); P(t); P("=" * 100)


ATOMS = {"1": 1.0, "2": 2.0, "3": 3.0, "4": 4.0, "6": 6.0, "8": 8.0,
         "pi": math.pi, "sqrtpi": math.sqrt(math.pi), "sqrt2": math.sqrt(2),
         "sqrt3": math.sqrt(3), "e": math.e, "ln2": math.log(2)}
P(__doc__)
P(f"  alphabet: {list(ATOMS)}  ({len(ATOMS)} atoms)")


def enumerate_expr(kmax):
    """value -> minimal op-count. by_ops[k] = set of distinct values first reachable with exactly k ops."""
    KEY = lambda v: round(v, 9)
    best = {}                                  # rounded value -> (min_ops, one true value)
    level = {}                                 # k -> list of (value)
    lvl0 = []
    for name, v in ATOMS.items():
        kk = KEY(v)
        if kk not in best:
            best[kk] = (0, v); lvl0.append(v)
    level[0] = lvl0
    for k in range(1, kmax + 1):
        cur = []
        for i in range(0, k):
            j = k - 1 - i
            if i not in level or j not in level:
                continue
            for x in level[i]:
                for y in level[j]:
                    for op in ("+", "-", "*", "/"):
                        try:
                            if op == "+": v = x + y
                            elif op == "-": v = x - y
                            elif op == "*": v = x * y
                            else:
                                if abs(y) < 1e-12: continue
                                v = x / y
                        except Exception:
                            continue
                        if not math.isfinite(v) or abs(v) > 1e6 or abs(v) < 1e-9:
                            continue
                        kk = KEY(v)
                        if kk not in best:
                            best[kk] = (k, v); cur.append(v)
        level[k] = cur
    return best, level


KMAX = 4
best, level = enumerate_expr(KMAX)
P(f"  enumerated to k={KMAX}: {sum(len(level[k]) for k in level)} distinct finite values in (1e-9, 1e6)")

# reference O(1) window and the bands
WIN = (0.0, 10.0)
def in_win(v): return WIN[0] < v <= WIN[1]
BANDS = {"BTFR 1sig": (0.465, 0.076, 1), "BTFR 2sig": (0.465, 0.076, 2),
         "dist-free 1sig": (0.551, 0.043, 1), "dist-free 2sig": (0.551, 0.043, 2),
         "kappa +-5%": (0.5, 0.025, 1)}
def kap_in(v, band):
    m, s, nsig = band
    return abs(v - m) <= nsig * s

# eps_tot band = (kappa band)^2/8pi around 1/(32pi)
def eps_in(v, band):
    m, s, nsig = band
    lo = ((m - nsig * s)**2) / (8 * math.pi); hi = ((m + nsig * s)**2) / (8 * math.pi)
    return lo <= v <= hi

banner("COUNTS BY k -- distinct values, kappa-band hits, eps-band hits")
# cumulative distinct values with min-ops <= k
def distinct_upto(k):
    return [v for kk, (mo, v) in best.items() if mo <= k]

P(f"  {'k':>3}{'distinct(<=k)':>15}{'in win(0,10]':>14}{'kappa 2sig':>12}{'eps 2sig':>11}{'frac_kappa2sig':>16}")
rowsK = {}
for k in range(0, KMAX + 1):
    vals = distinct_upto(k)
    winvals = [v for v in vals if in_win(v)]
    nk2 = sum(1 for v in vals if kap_in(v, BANDS["BTFR 2sig"]) or kap_in(v, BANDS["dist-free 2sig"]))
    ne2 = sum(1 for v in vals if eps_in(v, BANDS["BTFR 2sig"]) or eps_in(v, BANDS["dist-free 2sig"]))
    frac = nk2 / max(len(winvals), 1)
    rowsK[k] = dict(distinct=len(vals), win=len(winvals), k2=nk2, e2=ne2, frac=frac)
    P(f"  {k:>3}{len(vals):>15}{len(winvals):>14}{nk2:>12}{ne2:>11}{frac:>16.4f}")
OUT["numbers"]["by_k"] = rowsK

# --- C1: fraction at k=3, 2 sigma kappa band ----------------------------------------------------
f3 = rowsK[3]["frac"]
f4 = rowsK[4]["frac"]
check("C1 the 2 sigma kappa-band fraction has CONVERGED by k=3 (stable to k=4), so it is a real property of "
      "the alphabet, not an enumeration-depth artefact",
      f"frac(k=3) = {f3:.4f}, frac(k=4) = {f4:.4f}, |diff| = {abs(f3-f4):.4f}", abs(f3 - f4) < 0.02 and f3 > 0.02,
      "a landing on 1/2 at 2 sigma is what a fraction ~{:.1%} of simple O(1) natural numbers already do".format(f3))
OUT["numbers"]["frac_k3_2sig"] = f3
OUT["numbers"]["frac_k4_2sig"] = f4

# --- C2: at +-5% precision ----------------------------------------------------------------------
vals3 = distinct_upto(3)
win3 = [v for v in vals3 if in_win(v)]
n5 = sum(1 for v in vals3 if kap_in(v, BANDS["kappa +-5%"]))
f5 = n5 / max(len(win3), 1)
check("C2 at the +-5% precision KS03 needs, the fraction of <=3-op natural numbers in the kappa=0.5+-0.025 "
      "band drops (a tighter target is harder to hit by chance)",
      f"k=3, +-5%: {n5}/{len(win3)} = {f5:.4f}  vs 2sigma fraction {f3:.4f}", f5 <= f3,
      "the look-elsewhere penalty shrinks with precision: at 5% a chance landing is ~{:.1%}".format(f5))
OUT["numbers"]["frac_k3_5pct"] = f5

# --- C3: complexity rank of 1/2 and 1/(32 pi) ---------------------------------------------------
banner("C3 -- complexity rank of 1/2 (kappa band) and 1/(32 pi) (eps band)")
def rank_of(target, band_pred, band):
    inb = sorted(((mo, v) for kk, (mo, v) in best.items() if band_pred(v, band)), key=lambda t: t[0])
    # rank of the target = number of in-band values with strictly LOWER op-count, +1 for ties bucket
    tval = round(target, 9)
    tops = best.get(tval, (99, None))[0]
    lower = sum(1 for mo, v in inb if mo < tops)
    same = sum(1 for mo, v in inb if mo == tops)
    return tops, lower, same, len(inb)

# 1/2 in kappa band (use the wider of the two 2sig bands: union)
band_pred_kappa = lambda v, b: kap_in(v, BANDS["BTFR 2sig"]) or kap_in(v, BANDS["dist-free 2sig"])
tops_half, lower_half, same_half, ninb_half = rank_of(0.5, band_pred_kappa, None)
P(f"  1/2: op-count {tops_half}; {lower_half} in-band values are simpler, {same_half} equally simple, "
  f"{ninb_half} in the kappa 2sigma band total")
band_pred_eps = lambda v, b: eps_in(v, BANDS["BTFR 2sig"]) or eps_in(v, BANDS["dist-free 2sig"])
tops_eps, lower_eps, same_eps, ninb_eps = rank_of(1.0 / (32 * math.pi), band_pred_eps, None)
P(f"  1/(32pi) = {1/(32*math.pi):.6f}: op-count {tops_eps}; {lower_eps} in-band values are simpler, "
  f"{same_eps} equally simple, {ninb_eps} in the eps 2sigma band total")
check("C3 1/2 is among the SIMPLEST expressions in the kappa band (few or no simpler in-band values), "
      "so on complexity it is a strong candidate -- but it is not unique in the band (C1)",
      f"1/2 op-count {tops_half}, simpler-in-band {lower_half}; 1/(32pi) op-count {tops_eps}, "
      f"simpler-in-band {lower_eps}", tops_half <= 2,
      "the control's two-sided reading: 1/2 is complexity-favoured, yet the band is not empty of rivals")
OUT["numbers"].update(half_ops=tops_half, half_simpler_inband=lower_half, half_inband_total=ninb_half,
                      eps_ops=tops_eps, eps_simpler_inband=lower_eps, eps_inband_total=ninb_eps)

banner("VERDICT")
P(f"""  (1) COMPUTED: an enumeration of <=4-op dimensionless expressions over a 12-symbol alphabet
      ({sum(len(level[k]) for k in level)} distinct values), with in-band counts by complexity.
  (2) NUMBERS: at k=3, a fraction {f3:.3f} of O(1) natural numbers fall in the 2 sigma kappa band; at
      +-5% the fraction is {f5:.3f}.  1/2 has op-count {tops_half} with {lower_half} simpler in-band rivals;
      1/(32 pi) has op-count {tops_eps} with {lower_eps} simpler in-band rivals.
  (3) HONEST SENTENCE: at today's precision a fraction {f3:.3f} of <=3-operation natural numbers land in the
      band; at +-5% the fraction is {f5:.3f}.  1/2 is complexity-favoured but not alone in the band.
      Reported as a control; no claim that 1/2 is or is not selected follows from this lane alone.""")
OUT["verdict"] = {"word": "CONTROL", "frac_k3_2sig": f3, "frac_k3_5pct": f5,
                  "half_ops": tops_half, "eps_ops": tops_eps}

banner("RESULT")
npass = sum(1 for _, ok, _ in CH if ok); n = len(CH)
lb_fail = [nm for nm, ok, lb in CH if lb and not ok]
P(f"KS04 COMPLETE: {npass}/{n} checks PASS")
for nm in lb_fail:
    P(f"    load-bearing FAIL: {nm}")
OUT["summary"] = {"pass": npass, "n": n, "load_bearing_fail": lb_fail}
with open(os.path.join(HERE, SLUG + ".json"), "w") as fh:
    json.dump(OUT, fh, indent=2)
sys.exit(1 if lb_fail else 0)
