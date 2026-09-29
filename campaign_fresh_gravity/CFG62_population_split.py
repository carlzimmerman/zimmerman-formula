#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG62 -- CAN ONE DECLARED VARIABLE SPLIT THE RULE'S POPULATIONS INTO GROUPS THAT EACH ADMIT A COMMON DEBRIS FRACTION?

Criteria frozen and committed before this script: campaign_fresh_gravity/CFG62_FROZEN_CRITERIA.md (commit dfe4d59ef).  Inputs are CFG59's committed
per-population phi intervals (1 sigma of the lane's own offset; phi in [0, 1]) and per-population variables (log M_*, log(M_ph,edge / M_coll)), plus
the declared support (rotation: U7, U8) and environment (satellite: U1-U4, U9, U10).  Nothing is refitted.
PRE-DECLARED (from the frozen file)
  C1  CONTROL  CFG59's committed answer reproduced from its JSON by this script's own intersection code: no common intersection of all ten on either
               footing; the binding pair SLUGGS vs M31 LVD with a 0.51 gap (canonical).
  H1  [HEADLINE; MUTATE must fail]  no split of the TEN populations by any of the four variables at any threshold gives non-empty intersections in
      both groups, either footing.
  H2  (declared after seeing U6's empty interval; disclosed) the same for the NINE without U6 (X-ray ellipticals).
  R1-R3 (reported) every split tested with each group's intersection; the fewest contiguous log M_* groups with non-empty intersections (nine) and
      their phi ranges; the phi_ext values (roots on [0, 6]).
MUTATE=1: every interval replaced by [0, 1] -- every split succeeds, so H1 must FAIL (rc = 1).
Run: python3 campaign_fresh_gravity/CFG62_population_split.py   (MUTATE=1 for the control)
"""
import os, sys, json, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import CFG7_common as C
MUTATE = os.environ.get("MUTATE", "0") == "1"
R = C.Report("CFG62_population_split", MUTATE)
P, check = R.P, R.check
P(__doc__.split("Run: python3")[0].strip())
if MUTATE:
    P("\n  *** MUTATE=1: every interval set to [0, 1] -- H1 must FAIL ***")
FOOTS = ("canonical", "alt")
N59 = json.load(open(os.path.join(HERE, "CFG59_universal_debris_fraction_results.json")))["numbers"]
TAB, ANS = N59["TAB"], N59["ANS"]
POPS = []
for k in TAB:
    n = k.split("|")[0]
    if n not in POPS:
        POPS.append(n)
tag = lambda n: n.split()[0]
SUPPORT = {n: ("rotation" if tag(n) in ("U7", "U8") else "pressure") for n in POPS}
ENV = {n: ("satellite" if tag(n) in ("U1", "U2", "U3", "U4", "U9", "U10") else "central") for n in POPS}


def segs(n, foot):
    return [[0.0, 1.0]] if MUTATE else [list(s) for s in TAB[f"{n}|{foot}"]["segs"]]


def meet(a, b):
    out = []
    for x in a:
        for y in b:
            lo, hi = max(x[0], y[0]), min(x[1], y[1])
            if lo <= hi:
                out.append([lo, hi])
    return out


def inter(names, foot):
    cur = [[0.0, 1.0]]
    for n in names:
        cur = meet(cur, segs(n, foot))
        if not cur:
            return []
    return cur


R.banner("C1  CONTROL: CFG59 reproduced")
c1 = {}
for f in FOOTS:
    allten = inter(POPS, f)
    s5, s4 = segs("U5 SLUGGS", f), segs("U4 M31 LVD", f)
    gap = (s5[0][0] - s4[-1][1]) if (s5 and s4) else float("nan")
    c1[f] = dict(empty=(allten == []), gap=gap, committed_yes=ANS[f]["yes"], committed_gap=ANS[f]["binding"][2])
check("C1 CONTROL: CFG59's answer reproduced by this script's intersection code (all ten empty; SLUGGS vs M31 LVD gap 0.51 canonical)",
      "; ".join(f"{f}: all-ten intersection empty {v['empty']} (committed yes={v['committed_yes']}), gap {v['gap']:.3f} (committed {v['committed_gap']:.3f})"
                for f, v in c1.items()),
      MUTATE or all(v["empty"] and not v["committed_yes"] and abs(v["gap"] - v["committed_gap"]) < 1e-9 for v in c1.values()))

VARS = {"log M_*": lambda n, f: TAB[f"{n}|{f}"]["meta"]["logMs"], "log(M_ph,edge/M_coll)": lambda n, f: TAB[f"{n}|{f}"]["meta"]["logratio"],
        "support": lambda n, f: SUPPORT[n], "environment": lambda n, f: ENV[n]}


def splits(names, foot):
    rows = []
    for vn, vf in VARS.items():
        vals = {n: vf(n, foot) for n in names}
        if isinstance(next(iter(vals.values())), str):
            cats = sorted(set(vals.values()))
            groups = [[n for n in names if vals[n] == c] for c in cats]
            thr = [f"{cats[0]} | {cats[1]}"] if len(cats) == 2 else []
            parts = [groups] if len(cats) == 2 else []
        else:
            order = sorted(names, key=lambda n: vals[n])
            parts, thr = [], []
            for i in range(1, len(order)):
                if vals[order[i]] == vals[order[i - 1]]:
                    continue
                parts.append([order[:i], order[i:]])
                thr.append(f"{0.5 * (vals[order[i - 1]] + vals[order[i]]):.2f}")
        for t, (a, b) in zip(thr, parts):
            ia, ib = inter(a, foot), inter(b, foot)
            rows.append(dict(var=vn, thr=t, A=[tag(n) for n in a], B=[tag(n) for n in b], IA=ia, IB=ib, ok=bool(ia) and bool(ib)))
    return rows


RES = {}
for f in FOOTS:
    RES[(f, 10)] = splits(POPS, f)
    RES[(f, 9)] = splits([n for n in POPS if tag(n) != "U6"], f)

R.banner("R1  EVERY SPLIT (canonical)")
fmt = lambda I: ("EMPTY" if not I else " u ".join(f"[{a:.3f},{b:.3f}]" for a, b in I))
for npop in (10, 9):
    P(f"    -- {npop} populations --")
    for r in RES[("canonical", npop)]:
        P(f"    {r['var']:22s} split {r['thr']:>20s}: {'+'.join(r['A']):28s} {fmt(r['IA']):22s} | {'+'.join(r['B']):28s} {fmt(r['IB']):22s} -> {'YES' if r['ok'] else 'no'}")

R.banner("H1 / H2")
h1 = {f: not any(r["ok"] for r in RES[(f, 10)]) for f in FOOTS}
h2 = {f: not any(r["ok"] for r in RES[(f, 9)]) for f in FOOTS}
check("H1 [HEADLINE] NO one-variable split reconciles the TEN populations (four variables, every threshold), either footing"
      + ("  [MUTATE: all intervals [0,1]]" if MUTATE else ""),
      "; ".join(f"{f}: {sum(r['ok'] for r in RES[(f, 10)])} of {len(RES[(f, 10)])} splits succeed" for f in FOOTS), all(h1.values()))
check("H2 (declared after seeing U6's empty interval) NO one-variable split reconciles the NINE populations without the X-ray ellipticals, either footing",
      "; ".join(f"{f}: {sum(r['ok'] for r in RES[(f, 9)])} of {len(RES[(f, 9)])} splits succeed" for f in FOOTS), all(h2.values()))

R.banner("R2 / R3 (reported)")


def min_groups(names, foot):
    """fewest contiguous log M_* blocks, each with a non-empty intersection (dynamic programming)."""
    order = sorted(names, key=lambda n: TAB[f"{n}|{foot}"]["meta"]["logMs"])
    m = len(order); best = [0] + [math.inf] * m; cut = [0] * (m + 1)
    for j in range(1, m + 1):
        for i in range(j):
            if inter(order[i:j], foot) and best[i] + 1 < best[j]:
                best[j], cut[j] = best[i] + 1, i
    if not math.isfinite(best[m]):
        return None
    blocks, j = [], m
    while j > 0:
        i = cut[j]; blocks.append(order[i:j]); j = i
    return blocks[::-1]


r2 = {}
for f in FOOTS:
    bl = min_groups([n for n in POPS if tag(n) != "U6"], f)
    r2[f] = [dict(members=[tag(n) for n in b], logMs=[round(TAB[f"{n}|{f}"]["meta"]["logMs"], 2) for n in b], phi=inter(b, f)) for b in (bl or [])]
    check(f"R2 (reported, {f}) the fewest contiguous log M_* groups with a common phi (nine populations)",
          f"{len(r2[f])} groups: " + "; ".join(f"{'+'.join(g['members'])} (log M* {min(g['logMs'])}-{max(g['logMs'])}) phi {fmt(g['phi'])}" for g in r2[f]),
          True, load_bearing=False)
check("R3 (reported, canonical) phi_ext = the root of each population's offset on [0, 6] (phi > 1 is more debris than the collapse mass holds)",
      ", ".join(f"{tag(n)} {TAB[f'{n}|canonical']['phi_ext']:.2f}" if isinstance(TAB[f'{n}|canonical']['phi_ext'], float) else f"{tag(n)} n/a"
                for n in POPS), True, load_bearing=False)

if all(h1.values()) and all(h2.values()):
    reading = (f"the rule's debris fraction is not a one-variable function of mass, the phantom/collapse ratio, support or environment on these lanes; "
               f"a reconciliation needs at least {len(r2['canonical'])} contiguous mass groups with their own phi (canonical)")
elif not all(h2.values()):
    reading = "a one-variable split exists for the nine: reported as a hypothesis for independent data, not a rule"
else:
    reading = "see the table"
P(f"\n    READING (declared): {reading}")
R.num("C1", c1); R.num("R2", r2)
R.num("splits", {f"{f}|{n}": RES[(f, n)] for (f, n) in RES}); R.num("reading", reading)
nf = R.write()
sys.exit(1 if nf else 0)
