#!/usr/bin/env python3
"""AUDIT (lens gate_b, part a-ii): is a forced germ that CANCELS ALGEBRAICALLY detected?

Gate B credits a factor if its germ KEY appears among the expression's constant leaves
(exhaust.gate_candidate_for reads node.leaf_consts()). The enumerator's germ layer assigns a
NET SIGNED EXPONENT per germ key (exhaust_depthN_forced._germ_recipes / _net_exps), and 0 is in
that set whenever a key gets >=2 steps -- i.e. `* sqrt(8pi/3)` then `/ sqrt(8pi/3)`.

This script, using the REAL committed machinery only:
  (1) proves _net_exps() contains 0, so the enumerator DOES generate cancelling forced germs;
  (2) builds such an expression with the real DN._decorate on a real skeleton, evaluates it with
      the real Alphabet, and pushes it through the REAL gate_candidate_for + validate;
  (3) shows the germ-deleted expression has the IDENTICAL value (mpmath, 40 dps) -> the credited
      germ is not load-bearing;
  (4) quantifies it on the COMMITTED depth-10 artifacts: what fraction of the 82,613 in-window
      hits carry a forced germ whose net exponent is 0.

Local-only project. Exit 0.
"""
from __future__ import annotations
import json
import sqlite3
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

import mpmath as mp
import numpy as np

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

mp.mp.dps = 40

import exhaust_depthN_forced as DN                                       # noqa: E402
import exhaust_depth5_forced as D5                                       # noqa: E402
from engine.expr_tree import ExprNode, OpType                            # noqa: E402
from engine.scoring import score_value, measurement_tol                  # noqa: E402
from exhaust import (build_alphabet, Reachable, gate_candidate_for,       # noqa: E402
                     resolve_target)
from gate import validate, forced_kernel_detector                        # noqa: E402
from exhaust_parallel import sm_target_keys                              # noqa: E402
import targets.pdg_constants as pdg                                      # noqa: E402

bar = "=" * 104
checks = []


def check(msg, cond):
    checks.append(bool(cond))
    print(f"   [{'PASS' if cond else 'FAIL'}] {msg}")


print(bar)
print("DOES GATE B DETECT A FORCED GERM THAT CANCELS ALGEBRAICALLY?")
print(bar)

alpha = build_alphabet(None, None)
FORCED = D5._FORCED_KEYS
print(f"\nalphabet: {len(alpha.leaves)} leaves, {len(alpha.germs)} germs; "
      f"forced germ keys = {FORCED}")

# ---------------------------------------------------------------------------------------------
# (1) the enumerator's own net-exponent set contains ZERO
# ---------------------------------------------------------------------------------------------
print("\n" + "-" * 104)
print("(1) DN._net_exps(n): the NET signed exponents the germ layer can put on ONE germ key")
print("-" * 104)
for n in range(1, 5):
    nets = [float(x) for x in DN._net_exps(n)]
    print(f"   n_steps={n}: {nets}   contains 0 -> {0.0 in nets}")
check("net exponent 0 is reachable for a single germ key at n_steps=2 "
      "(=> `*g` then `/g`: the germ cancels)", 0.0 in [float(x) for x in DN._net_exps(2)])
check("net exponent 0 NOT reachable at n_steps=1 (a single step always leaves the germ)",
      0.0 not in [float(x) for x in DN._net_exps(1)])

# ---------------------------------------------------------------------------------------------
# (2) build one with the REAL machinery and run the REAL gate
# ---------------------------------------------------------------------------------------------
print("\n" + "-" * 104)
print("(2) a REAL enumerated expression whose sqrt(8pi/3) net exponent is 0")
print("-" * 104)
free_keys = D5._free_germ_keys(alpha)
# depth 6 -> budget_splits(6) = [(b_s, g_s)] with b_s+g_s=5, g_s>=3
splits = DN.budget_splits(6)
print(f"   DN.budget_splits(6) = {splits}")
b_s, g_s = splits[0]
skeletons = DN._skeleton_value_nodes(alpha, b_s)
print(f"   skeleton layer at b_s={b_s}: {len(skeletons)} value-distinct skeletons")


def net_exponents(recipe):
    """Net signed exponent per germ key for a recipe of (key, OpType, exp) steps."""
    net = {}
    for gk, op, e in recipe:
        s = Fraction(str(e)) if op == OpType.MUL else -Fraction(str(e))
        net[gk] = net.get(gk, Fraction(0)) + s
    return net


# find the first enumerated recipe (g_s=3 is impossible: every key gets exactly 1 step) with a
# net-zero FORCED germ -- use g_s from the split that allows >=2 steps on a forced key.
target_recipe = None
for (bb, gg) in splits:
    for recipe in DN._germ_recipes(alpha, free_keys, gg):
        ne = net_exponents(recipe)
        zeros = [k for k in FORCED if ne.get(k, Fraction(0)) == 0]
        if zeros:
            target_recipe = (bb, gg, recipe, ne, zeros)
            break
    if target_recipe:
        break

if target_recipe is None:
    print("   no cancelling recipe at depth 6 -- escalating to depth 7")
    for (bb, gg) in DN.budget_splits(7):
        for recipe in DN._germ_recipes(alpha, free_keys, gg):
            ne = net_exponents(recipe)
            zeros = [k for k in FORCED if ne.get(k, Fraction(0)) == 0]
            if zeros:
                target_recipe = (bb, gg, recipe, ne, zeros)
                break
        if target_recipe:
            break

assert target_recipe is not None, "no cancelling forced germ found in the enumerator"
bb, gg, recipe, ne, zeros = target_recipe
sk = DN._skeleton_value_nodes(alpha, bb)[0]
node = sk.node
for gk, op, e in recipe:
    node = DN._decorate(node, op, gk, e)
value, label = node.evaluate(alpha)
formula = node.to_string(alpha)
print(f"   split (b_s={bb}, g_s={gg}); recipe steps = "
      f"{[(k, o.name, str(e)) for k, o, e in recipe]}")
print(f"   net exponents  = { {k: str(v) for k, v in ne.items()} }")
print(f"   CANCELLING forced germ(s) = {zeros}")
print(f"   formula = {formula}")
print(f"   value   = {mp.nstr(value, 25)}")

# the germ-DELETED expression: drop every step on the cancelling key
recipe_del = tuple(s for s in recipe if s[0] not in zeros)
node_del = DN._skeleton_value_nodes(alpha, bb)[0].node
for gk, op, e in recipe_del:
    node_del = DN._decorate(node_del, op, gk, e)
v_del, _ = node_del.evaluate(alpha)
print(f"   germ-DELETED formula = {node_del.to_string(alpha)}")
print(f"   germ-DELETED value   = {mp.nstr(v_del, 25)}")
print(f"   |value - value_deleted| = {mp.nstr(abs(value - v_del), 5)}")
check("deleting the credited forced germ changes NOTHING (value identical at 40 dps) "
      "-> the germ is not load-bearing", abs(value - v_del) == 0)

# now the REAL gate on it
tkey = "koide_Q_down"
tspec = resolve_target(tkey)
r = Reachable(value=value, label=label, formula=formula,
              canonical=node.canonical_hash(), node=node)
gc = gate_candidate_for(r, alpha, tkey, tspec.pdg_target, 19)
b = forced_kernel_detector(gc)
print(f"\n   REAL gate_candidate_for -> coefficient factors:")
for f in gc.coefficient.factors:
    print(f"      value={f.value:.12g}  provenance={f.provenance}  appears_in={f.appears_in}")
print(f"   free_params declared = {gc.coefficient.free_params}")
print(f"   REAL Gate B: passed={b.passed} n_free={b.n_free_params} "
      f"n_appearances={b.n_independent_appearances}")
print(f"   Gate B tell: {b.tell[:170]}")
check(f"Gate B credits the CANCELLED germ {zeros} as forced (passed={b.passed}) "
      f"-> cancellation is NOT detected", b.passed is True)
prov_credited = sorted(f.provenance for f in gc.coefficient.factors)
check("the credited provenance list includes a0_kernel_8pi3 even though its net exponent is 0"
      if "sqrt(8pi/3)" in zeros else
      "the credited provenance list includes Ngen_3 even though its net exponent is 0",
      len(prov_credited) == 2)

# ---------------------------------------------------------------------------------------------
# (2b) THE COMMITTED DEPTH-6 GROUND-TRUTH TIGHTEST HIT is one of these
# ---------------------------------------------------------------------------------------------
print("\n" + "-" * 104)
print("(2b) the COMMITTED depth-6 replay ground truth (grind.REPLAY_COMMITTED[6]) profiled")
print("-" * 104)
import grind                                                             # noqa: E402
com6 = grind.REPLAY_COMMITTED[6]
print(f"   committed tightest_target  = {com6['tightest_target']}")
print(f"   committed tightest_formula = {com6['tightest_formula']}")
print(f"   committed tightest_rel     = {com6['tightest_rel']:.6e}")

sk_cc = None
for s in DN._skeleton_value_nodes(alpha, 1):
    if s.node.to_string(alpha) == "(c / c)":
        sk_cc = s
        break
assert sk_cc is not None, "skeleton (c / c) not found at b_s=1"
one = mp.mpf(1)
rec6 = (("3", OpType.DIV, one), ("sqrt(8pi/3)", OpType.MUL, one),
        ("sqrt(8pi/3)", OpType.DIV, one), ("2", OpType.MUL, one))
n6 = sk_cc.node
for gk, op, e in rec6:
    n6 = DN._decorate(n6, op, gk, e)
v6, lab6 = n6.evaluate(alpha)
f6 = n6.to_string(alpha)
ne6 = net_exponents(rec6)
print(f"   rebuilt formula = {f6}")
check("the rebuilt expression IS the committed depth-6 tightest formula, character for "
      "character", f6 == com6["tightest_formula"])
print(f"   net exponents = { {k: str(v) for k, v in ne6.items()} }")
print(f"   value = {mp.nstr(v6, 25)}   (2/3 = {mp.nstr(mp.mpf(2)/3, 25)})")
check("its sqrt(8pi/3) net exponent is 0 -- the kernel germ CANCELS",
      ne6["sqrt(8pi/3)"] == 0)
check("its measured-leaf skeleton is c/c == 1 -- the two measured leaves cancel too",
      abs(sk_cc.node.evaluate(alpha)[0] - 1) == 0)
check("the expression is therefore EXACTLY 2/3 (a bare rational, no germ content in value)",
      abs(v6 - mp.mpf(2) / 3) == 0)
r6 = Reachable(value=v6, label=lab6, formula=f6, canonical=n6.canonical_hash(), node=n6)
ts6 = resolve_target("koide_Q_lep")
gc6 = gate_candidate_for(r6, alpha, "koide_Q_lep", ts6.pdg_target, 21)
v6g = validate(gc6)
print(f"   REAL gate profile: status={v6g.status}")
print(f"      A: passed={v6g.fdr.passed} bits={v6g.fdr.bits:.2f} mode={v6g.fdr.mode}")
print(f"      B: passed={v6g.kernel.passed} n_free={v6g.kernel.n_free_params} "
      f"factors={[f.provenance for f in gc6.coefficient.factors]}")
print(f"      C: passed={v6g.interlock.passed} mode={v6g.interlock.mode} "
      f"n_constants_tied={gc6.interlock.n_constants_tied}")
check("Gate B PASSES on the bare rational 2/3 whose kernel germ cancels "
      "(the germ requirement is satisfied vacuously)", v6g.kernel.passed)
check("what actually kills it is Gate A/C, not Gate B", not v6g.certified)

# ---------------------------------------------------------------------------------------------
# (3) does the whole germ layer ever cancel BOTH forced germs at once?
# ---------------------------------------------------------------------------------------------
print("\n" + "-" * 104)
print("(3) enumerator census at depth 10: how many canonical germ recipes cancel a forced germ?")
print("-" * 104)
tot = 0
n_one = 0
n_both = 0
for (bb2, gg2) in DN.budget_splits(10):
    for recipe in DN._germ_recipes(alpha, free_keys, gg2):
        ne2 = net_exponents(recipe)
        z = [k for k in FORCED if ne2.get(k, Fraction(0)) == 0]
        tot += 1
        if z:
            n_one += 1
        if len(z) == 2:
            n_both += 1
print(f"   canonical germ recipes over all depth-10 splits : {tot:,}")
print(f"   with >=1 forced germ cancelling (net exp 0)      : {n_one:,}  ({100.0*n_one/tot:.2f}%)")
print(f"   with BOTH forced germs cancelling                : {n_both:,}  "
      f"({100.0*n_both/tot:.2f}%)")
check("the enumerator generates recipes where BOTH forced germs cancel "
      "(the expression is then germ-content-free in value but Gate-B-credited)", n_both > 0)

# ---------------------------------------------------------------------------------------------
# (4) the COMMITTED depth-10 hit set: how many of the 82,613 hits carry a cancelling germ?
# ---------------------------------------------------------------------------------------------
print("\n" + "-" * 104)
print("(4) the committed depth-10 hits (results_grind/depth_10) -- real artifacts")
print("-" * 104)
d10 = _ROOT / "results_grind" / "depth_10"
vals = np.fromfile(d10 / "values.f64", dtype=np.float64)
meta = json.loads((d10 / "build_meta.json").read_text())
print(f"   values.f64: {len(vals):,} distinct values "
      f"(build_meta distinct_by_value={meta['distinct_by_value']:,})")
check("values.f64 length == committed distinct_by_value",
      len(vals) == meta["distinct_by_value"])

con = sqlite3.connect(str(d10 / "records.sqlite"))
n_rec = con.execute("SELECT COUNT(*) FROM records").fetchone()[0]
print(f"   records.sqlite: {n_rec:,} retained in-window records")

search_keys = sm_target_keys()
print(f"   sweep target list (sm_target_keys(), holdout EXCLUDED) = {len(search_keys)} targets")

total_hits = 0
hit_idx_all = set()
per_target = {}
for k in search_keys:
    ts = resolve_target(k)
    tol = measurement_tol(ts.pdg_target)
    tv = float(ts.value)
    idxs = np.nonzero(np.abs(vals - tv) <= abs(tv) * tol * (1.0 + 1e-9))[0]
    keep = []
    for i in idxs:
        card = score_value(float(vals[i]), ts.pdg_target)
        if card.rel_error <= tol:
            keep.append(int(i))
    per_target[k] = keep
    total_hits += len(keep)
    hit_idx_all.update(keep)
print(f"   recomputed in-window hits over the 19 search targets: {total_hits:,} "
      f"(committed VERDICT.json: 82,613)")
committed = json.loads((d10 / "VERDICT.json").read_text())
check(f"recomputed hit total reproduces the committed null exactly "
      f"({total_hits:,} vs {committed['n_hits']:,})", total_hits == committed["n_hits"])

# net exponents for every hit record
q = "SELECT idx, recipe, formula FROM records WHERE idx IN (%s)"
idx_list = sorted(hit_idx_all)
rows = {}
CH = 900
for s in range(0, len(idx_list), CH):
    chunk = idx_list[s:s + CH]
    for i, rec, form in con.execute(q % ",".join("?" * len(chunk)), chunk):
        rows[i] = (rec, form)
print(f"   record rows found for hit indices: {len(rows):,} / {len(idx_list):,}")
check("every hit index has a spilled record (retention superset holds)",
      len(rows) == len(idx_list))

cnt = Counter()
zero_idx = set()
both_idx = set()
for i, (rec, form) in rows.items():
    net = {}
    for gk, opname, estr in json.loads(rec):
        s = Fraction(estr) if opname == "MUL" else -Fraction(estr)
        net[gk] = net.get(gk, Fraction(0)) + s
    z = [k for k in FORCED if net.get(k, Fraction(0)) == 0]
    cnt[len(z)] += 1
    if z:
        zero_idx.add(i)
    if len(z) == 2:
        both_idx.add(i)

n_hits_cancel = sum(len([i for i in v if i in zero_idx]) for v in per_target.values())
n_hits_both = sum(len([i for i in v if i in both_idx]) for v in per_target.values())
print(f"\n   distinct hit VALUES with >=1 cancelling forced germ : {len(zero_idx):,} / "
      f"{len(idx_list):,}  ({100.0*len(zero_idx)/len(idx_list):.2f}%)")
print(f"   distinct hit VALUES with BOTH forced germs cancelling: {len(both_idx):,}  "
      f"({100.0*len(both_idx)/len(idx_list):.2f}%)")
print(f"   HITS (target-weighted, of {total_hits:,}) with >=1 cancelling forced germ: "
      f"{n_hits_cancel:,}  ({100.0*n_hits_cancel/total_hits:.2f}%)")
print(f"   HITS (target-weighted) with BOTH forced germs cancelling: {n_hits_both:,}  "
      f"({100.0*n_hits_both/total_hits:.2f}%)")
print(f"   histogram over hit values (n forced germs cancelling -> count): {dict(cnt)}")

# a couple of concrete examples, with the real gate's Gate-B verdict on the string
print("\n   example hit formulas whose forced germ cancels:")
shown = 0
for i in sorted(both_idx)[:3] or sorted(zero_idx)[:3]:
    print(f"      idx {i}: {rows[i][1][:150]}")
    shown += 1
if shown == 0:
    for i in sorted(zero_idx)[:3]:
        print(f"      idx {i}: {rows[i][1][:150]}")

check("a non-trivial fraction of the committed depth-10 hits carry a Gate-B-credited "
      "forced germ that cancels algebraically", len(zero_idx) > 0)

# and: is Gate B passing on essentially ALL hits (i.e. is it filtering anything)?
print("\n" + "-" * 104)
print("(5) does Gate B ever FAIL on the enumerated path? (depth-9 committed target reports)")
print("-" * 104)
d9 = _ROOT / "results_grind" / "depth_9" / "targets"
tot9 = kp9 = 0
ip9 = 0
for f in sorted(d9.glob("*.json")):
    rep = json.loads(f.read_text())
    for h in rep.get("hits", []):
        tot9 += 1
        kp9 += 1 if h.get("kernel_passed") else 0
        ip9 += 1 if h.get("interlock_passed") else 0
print(f"   depth-9 recorded hit records (top-20 per target): {tot9}")
print(f"   Gate B (kernel) passed on: {kp9}/{tot9}"
      f"   Gate C (interlock) passed on: {ip9}/{tot9}")
check("Gate B passes on 100% of enumerated hits -> on this path Gate B is a "
      "CONSTRUCTIVE TAUTOLOGY, not a filter", tot9 > 0 and kp9 == tot9)

con.close()
print("\n" + bar)
n_fail = checks.count(False)
print(f"CHECKS: {len(checks) - n_fail}/{len(checks)} PASS")
print(bar)
sys.exit(0 if n_fail == 0 else 1)
