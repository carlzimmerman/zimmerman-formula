#!/usr/bin/env python3
"""CFG191_s4_scorecard -- item (d): recount of CFG7's H0 scorecard (ownership 9/14 vs external-field rival 6/14) from the committed .out.
Sigma values are PARSED (not recomputed; the underlying data are not in this session). Counting, flags and variants are mine.
MUTATE=1: M6 as frozen (G1 rival set to pass; rival threshold on G9 2.5 sigma) -- and M6' (labelled deviation) -- 'ownership strictly more' must fail."""
import re, math, itertools
from CFG191_common import Run, REPO, rel
R = Run("CFG191_s4_scorecard", "item (d): the 9/14 vs 6/14 scorecard, recounted")
MUT = R.mutate
SRC = REPO/"campaign_fresh_gravity/CFG7_hierarchy_fg001.out"
R.p(f"input: {rel(SRC)} (H0 block); sigma values as printed; pass line 2.0 sigma as CFG7 states")
pat = re.compile(r"^\s+(canonical|alt)\s+G(\d+)\s+(.+?)\s*:\s+FG001\s+([\d.]+|inf)\s+(pass|FAIL)\s+\|\s+rival\s+([\d.]+|inf)\s+(pass|FAIL)\s*$")
rows = {"canonical": {}, "alt": {}}
totals = {}
for ln in SRC.read_text().splitlines():
    m = pat.match(ln)
    if m:
        f, g, nm, s1, p1, s2, p2 = m.groups()
        rows[f][int(g)] = dict(name=nm.strip(), own=float("inf") if s1 == "inf" else float(s1), rival=float("inf") if s2 == "inf" else float(s2), own_pass=p1 == "pass", riv_pass=p2 == "pass")
    m = re.match(r"^\s+(canonical|alt)\s+TOTAL: FG001 passes (\d+)/14, the rival (\d+)/14", ln)
    if m: totals[m.group(1)] = (int(m.group(2)), int(m.group(3)))
R.sec("D1 control")
for f in rows:
    R.p(f"  {f}: {len(rows[f])} rows parsed; printed TOTAL {totals.get(f)}")
R.check("D1a 14 rows parsed on each footing", all(len(rows[f]) == 14 for f in rows))
def count(f, keep=None, thr=2.0, own_thr=None, riv_thr=None, force_riv=(), swap=False):
    o = r = 0
    for g, d in rows[f].items():
        if keep is not None and g not in keep: continue
        ot = thr if own_thr is None else own_thr; rt = thr if riv_thr is None else riv_thr
        op = d["own"] <= ot
        rp = (d["rival"] <= rt) or (g in force_riv)
        o += op; r += rp
    return (r, o) if swap else (o, r)
ALL = set(range(1, 15))
def show(lbl, f, **kw):
    c = count(f, **kw); R.p(f"  {lbl:62s} {f:9s}: ownership {c[0]} vs rival {c[1]}"); return c
c14 = {f: show("all 14 rows, 2.0 sigma (as CFG7)", f) for f in rows}
c13 = {f: show("13 physical rows (G1 dropped)", f, keep=ALL-{1}) for f in rows}
R.check("D1b parsed counts reproduce 9/14 vs 6/14 on both footings (from sigmas and the 2-sigma line, not from the printed TOTAL)", all(c14[f] == (9, 6) for f in rows) and all(totals[f] == (9, 6) for f in rows))
R.check("D1c 13 physical rows give 8 vs 6 on both footings", all(c13[f] == (8, 6) for f in rows))

R.sec("D2 row classification from the printed sigmas")
cls = {}
for g in range(1, 15):
    d = rows["canonical"][g]; a = rows["alt"][g]
    def cl(dd):
        if dd["own_pass"] and dd["riv_pass"]: return "tie-pass"
        if (not dd["own_pass"]) and (not dd["riv_pass"]): return "tie-fail"
        return "ownership-only" if dd["own_pass"] else "rival-only"
    cls[g] = (cl(d), cl(a))
    R.p(f"  G{g:<2d} {d['name'][:46]:46s} own {d['own']:5.2f}/{a['own']:5.2f}  rival {d['rival']:5.2f}/{a['rival']:5.2f}   {cls[g][0]}" + ("" if cls[g][0] == cls[g][1] else f"   (alt: {cls[g][1]})"))
disc = [g for g in cls if cls[g][0] in ("ownership-only", "rival-only")]
tiep = [g for g in cls if cls[g][0] == "tie-pass"]; tief = [g for g in cls if cls[g][0] == "tie-fail"]
R.p(f"  tie-pass {['G%d' % g for g in tiep]}; tie-fail {['G%d' % g for g in tief]}; discriminating {['G%d' % g for g in disc]}")
R.check("D2 classification agrees between footings and gives 4 tie-pass, 3 tie-fail, 7 discriminating (5 ownership-only, 2 rival-only)",
        all(cls[g][0] == cls[g][1] for g in cls) and len(tiep) == 4 and len(tief) == 3 and len(disc) == 7 and sum(cls[g][0] == "ownership-only" for g in disc) == 5)

R.sec("D3 flags (frozen)")
FLAGS = {"F-conv": [1], "F-dup(second of pair)": [6, 10, 12, 14], "F-best-variant rival": [8, 9, 10, 11]}
for k, v in FLAGS.items(): R.p(f"  {k}: {['G%d' % g for g in v]}")
R.p("  F-post: only H8 (fossil gas) is stated post hoc in the record and it is not among the 14; whether the class-A rule was formed after h43 / f13 was NOT checkable from the documents I read (not scored).")
R.p("  G1 rival 'inf' is a declared convention (the strict law fails Cassini by construction); ownership's G1 pass is by construction (the Sun owns no phantom).")

R.sec("D4 recounts (each footing)")
V = {}
for f in rows:
    V[("all14", f)] = c14[f]; V[("13", f)] = c13[f]
    V[("disc7", f)] = show("discriminating rows only (7)", f, keep=set(disc))
    V[("disc6", f)] = show("discriminating rows, G1 dropped (6)", f, keep=set(disc)-{1})
    dd = ALL - {6, 10, 12, 14}
    V[("dedup10", f)] = show("dedup (drop G6, G10, G12, G14): 10 rows", f, keep=dd)
    V[("dedup9", f)] = show("dedup and G1 dropped: 9 rows", f, keep=dd-{1})
    V[("thr2.5", f)] = show("threshold 2.5 sigma (both columns)", f, thr=2.5)
    V[("thr3.0", f)] = show("threshold 3.0 sigma (both columns)", f, thr=3.0)
    V[("thr3.0-13", f)] = show("threshold 3.0 sigma, G1 dropped", f, thr=3.0, keep=ALL-{1})
    V[("swap", f)] = show("column swap (control)", f, swap=True)
    lo = []
    for g in range(1, 15):
        c = count(f, keep=ALL-{g}); lo.append(c[0]-c[1])
    V[("loo", f)] = (min(lo), max(lo)); R.p(f"  leave-one-row-out (ownership minus rival): {min(lo)} to {max(lo)}")
    # equal-flag exclusion: all flagged rows out (G1, dup seconds, best-variant rival rows)
    ex = ALL - {1, 6, 10, 12, 14, 8, 9, 11}
    V[("noflag", f)] = show("[ADDED after the freeze, not a frozen variant] all flagged rows out (G1, G6, G10, G12, G14, G8, G9, G11): 6 rows", f, keep=ex)
def binom_tail(k, n): return sum(math.comb(n, i) for i in range(k, n+1))/2**n
nown = sum(cls[g][0] == "ownership-only" for g in disc)
R.p(f"  one-sided sign test on the 7 discriminating rows: {nown} of 7 favour ownership, p = {binom_tail(nown, 7):.3f}; on the 6 physical ones: {nown-1} of 6, p = {binom_tail(nown-1, 6):.3f}")
R.p("  [ADDED after the freeze, reported as a finding] with every flagged row out the count is a tie: " + str({f: V[("noflag", f)] for f in rows}) + "; it is not a reversal.")
R.data["variants"] = {f"{k[0]}|{k[1]}": v for k, v in V.items()}
def strictly_more(f, **kw):
    c = count(f, **kw); return c[0] > c[1]
orders = {k: (v[0] > v[1]) if k[0] not in ("loo", "swap", "noflag") else True for k, v in V.items()}
noflag_tie = [f for f in rows if V[("noflag", f)][0] <= V[("noflag", f)][1]]
reversed_any = [k for k, v in V.items() if k[0] not in ("loo", "swap") and v[0] < v[1]]
R.p("  variants where ownership is NOT strictly ahead: " + (", ".join(f"{k[0]}|{k[1]}={V[k]}" for k, ok in orders.items() if not ok) or "none"))
if not MUT:
    R.check("D4 ownership is strictly ahead of the rival in every FROZEN recount variant (all 14, 13, discriminating, dedup, thresholds 2.5/3.0) on both footings", all(orders.values()))
else:
    ex = {f: count(f, force_riv=(1,), riv_thr=2.5) for f in rows}
    R.p(f"  M6 AS FROZEN (G1 rival forced to pass; rival threshold 2.5 on all rows): {ex}   [frozen text predicted 8 vs 8; the arithmetic is 9 vs 8 -- wrong expectation, kept]")
    R.check("D4 [M6 as frozen] ownership strictly more (frozen expectation: this FAILS; it does not)", all(v[0] > v[1] for v in ex.values()), lb=False)
    ex2 = {}
    for f in rows:
        o = sum(rows[f][g]["own"] <= 2.0 for g in rows[f])
        r = sum((rows[f][g]["rival"] <= 3.0) or g == 1 for g in rows[f]); ex2[f] = (o, r)
    R.p(f"  M6' (labelled deviation): G1 rival forced to pass AND rival scored at 3.0 sigma while ownership stays at 2.0: {ex2}")
    R.check("D4' [M6'] ownership strictly more -- must FAIL", all(v[0] > v[1] for v in ex2.values()))

R.sec("D5 README double-count audit")
names = {g: rows["canonical"][g]["name"] for g in rows["canonical"]}
chae = [g for g, n in names.items() if "Chae" in n]; cass = [g for g, n in names.items() if "Cassini" in n]
coma = [g for g, n in names.items() if "Coma" in n or "UDG" in n]; dr4 = [g for g, n in names.items() if "DR4" in n or "wide" in n.lower()]
R.p(f"  README list item -> scorecard rows: Chae -> {['G%d' % g for g in chae]}; Solar System (Cassini) -> {['G%d' % g for g in cass]}; Coma UDGs -> {coma}; DR4 -> {dr4}")
R.check("D5 Chae = G13+G14, Solar System = G1; Coma UDGs and DR4 are not scorecard rows (two of the README's 'against committed tests' items are also inside the 9/14 vs 6/14)", chae == [13, 14] and cass == [1] and not coma and not dr4)
R.p("  R8 note: the rival column is the record's 1-D QUMOND EFE recipe (h43 / Famaey-McGaugh 2012 eq 60; read in CFG7_common/h43 headers) -- not E7 and not exactly F(z+ze)-F(ze).")

R.sec("VERDICT (frozen rule)")
if not MUT:
    R.finding("(d) scorecard", "AGREES WITH QUALIFICATION" if not reversed_any else "DISAGREES",
              f"9/14 vs 6/14 reproduced; 8 vs 6 without G1. Only 7 rows differ (5 ownership, 2 rival; sign test p={binom_tail(5,7):.3f}); 4 tie-pass, 3 tie-fail. Dedup 7 vs 3 of 10; all flagged rows out {V[('noflag','canonical')]}. Threshold 3.0: {V[('thr3.0','canonical')]} canonical / {V[('thr3.0','alt')]} alt. G1 is a declared convention; G13/G14 (Chae) and G1 (Cassini) are counted twice in the README's list. The order never reverses in any variant run (a tie appears in one variant added after the freeze), but the margin is threshold- and row-dependent and the rival is the QUMOND-1D recipe, not E7.")
R.finish()
