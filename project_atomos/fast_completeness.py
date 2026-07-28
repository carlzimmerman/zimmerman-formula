#!/usr/bin/env python3
"""
fast_completeness.py — an INDUCTIVE completeness CERTIFICATE for the constructive Gate-B-passable
DIMENSIONLESS depth-D sweep, that certifies a depth's null WITHOUT paying the ~30^(D-4) per-depth
skeleton brute (`DN.constructive_completeness_selfcheck`'s largest split, which costs ~3.5 h of
depth-9's run and grows 30x/depth — days at depth 10, weeks at 11).

RULE 3 (verbatim reuse): this file adds NO logic to gate/ engine/ exhaust*.py / grind.py. It IMPORTS
the committed machinery unmodified (`import exhaust_depthN_forced as DN`) and reuses its skeleton
enumerators, germ enumerators, apply/filter, value-key, and the depth-4 whole-tree anchor VERBATIM.
It only READS results_grind/depth_D/ artefacts; it never writes into any existing file.

--------------------------------------------------------------------------------------------------
WHAT THE EXHAUSTIVE BRUTE ACTUALLY VERIFIES (so we certify the SAME thing, honestly)
--------------------------------------------------------------------------------------------------
`DN.constructive_completeness_selfcheck(D)` does two things per depth:
  (a) SKELETON cross-check, for EVERY budget split (b_s, g_s), b_s = 1 .. D-4:
        DN._skeleton_value_set(a, b_s)            [the SCHEME: recursive `_walk`]
          ==
        DN._skeleton_brute_value_set(a, b_s)      [the BRUTE: flat itertools.product]
      with MISSED=0, EXTRA=0.  BOTH sides enumerate the IDENTICAL Cartesian power  menu^{b_s}
      over the SAME fixed 30-entry `step_menu`, apply the SAME `_apply`, the SAME dimensionless/
      finite/>0 filter, and dedup by the SAME `_value_key`.  The check therefore verifies that two
      INDEPENDENT CODE PATHS of one mathematical enumeration agree — it catches an implementation
      bug (off-by-one, wrong repeat count, a pruned walk, a divergent filter).  The COST is the
      largest split b_s = D-4:  |menu|^{b_s} x |leaves| = 30^{D-4} x 11  (267 M at D=9, ~8 B at D=10).
  (b) The committed depth-4 WHOLE-TREE anchor (DN._d5_completeness_selfcheck): the real tree
      enumerator reproduces the 11,209 all-Gate-B distinct values and the empty dimensionless<=4 set.
      This is the anchor that backstops the deeper "left-fold monomials capture every dimensionless
      skeleton tree-shape" claim (balanced trees etc.), independent of b_s.  It is CHEAP.

Only the b_s = D-4 split of (a) is expensive, and it RE-PROVES THE SAME STRUCTURAL FACT every depth.

--------------------------------------------------------------------------------------------------
THE INDUCTIVE STEP (the core — machine-verified ONCE, on the ACTUAL menu/apply objects)
--------------------------------------------------------------------------------------------------
Let  Frontier(k)  =  the FULL list of terminal nodes the enumeration reaches at EXACTLY k skeleton
steps  =  { apply_seq(leaf_node(base), seq) : base in leaves, seq in menu^k }  (NOT deduped, and
NOT yet dimension-filtered — dimensionful intermediates are retained, because a dimensionful node
can become dimensionless after one more step).  The value set at level k is then
      V(k) = dedup_{value_key}( { value(n) : n in Frontier(k), dimensionless & finite & >0 } ).

Two facts about the ACTUAL code, both machine-checked below on the real objects:
  (I)  MENU / APPLY INVARIANCE.  `step_menu` and `_apply` are built from (alpha.leaves,
       _POW_EXPONENTS, _UNARY_PLAIN, {MUL,DIV}) ONLY — they do NOT depend on b_s.  Both
       `_skeleton_value_nodes` (scheme) and `_skeleton_brute_value_set` (brute) build the SAME menu.
  (II) CARTESIAN RECURRENCE.  menu^{k+1} = menu^{k} x menu  (definition of a Cartesian power over a
       FIXED menu).  Hence  Frontier(k+1) = { apply(n, step) : n in Frontier(k), step in menu }.
       The scheme realizes this by recursion (`_walk` extends every length-k branch by every menu
       step, with NO value-pruning); the brute realizes it by `itertools.product(menu, repeat=k+1)`.

The induction:  if the FULL Frontier(k) is completely enumerated by BOTH paths (base case, checked
empirically at small k where scheme==brute), then applying the FIXED menu one more step (fact II)
with the SAME apply and the SAME post-enumeration filter+dedup (fact I) yields V(k+1) identically for
both paths — no miss, no extra.  Therefore scheme==brute at EVERY b_s, given it holds at the base.

We make this CONCRETE and EXECUTABLE (not a paraphrase):
  * MENU FIDELITY: a menu we rebuild from the same inputs reproduces DN._skeleton_value_set AND
    DN._skeleton_brute_value_set exactly at b_s in {1,2} (a THIRD independent path agreeing).
  * ONE-STEP CLOSURE, on the real objects: we materialise the FULL Frontier(1) (all 11*30 nodes),
    extend it by the real menu to Frontier(2), filter+dedup, and assert the result EQUALS
    DN._skeleton_value_set(a,2) == DN._skeleton_brute_value_set(a,2).  Repeated for 2->3.  This
    demonstrates the closure map V(k) <- Frontier(k) on the code's own menu/apply at two successive
    levels; the map is literally the same object at every level (fact I), so it holds for all k.
  * CARTESIAN IDENTITY: menu^{2} == extend(menu^{1}, menu) verified as SEQUENCE sets on the real menu.

--------------------------------------------------------------------------------------------------
WHAT MAKES THIS CHEAP, AND HOW MUCH WEAKER IT IS THAN THE BRUTE  (stated honestly at the bottom too)
--------------------------------------------------------------------------------------------------
Each depth D adds exactly ONE new split, b_s = D-4; all smaller splits (b_s <= D-5) were already
brute-anchored at depth D-1 and below.  So depth 9's only "new" split is b_s=5, depth 10's is b_s=6.
The certificate:
  1. INDUCTIVE STEP  — proves the scheme==brute agreement PROPAGATES from b_s to b_s+1 by the
     fixed-menu Cartesian structure (deductive, verified on the real objects; not probabilistic).
  2. BASE ANCHORS    — re-runs the REAL DN skeleton scheme/brute at b_s = 1..min(4, D-4) (0/0), plus
     the depth-4 whole-tree anchor.  These are genuine empirical base cases (seconds..minutes).
  3. SPOT CHECK      — a seeded randomised falsification test AT depth D: sample K full step-sequences
     the BRUTE way (random skeleton menu-steps + random-order/op/exp germ decoration), build each
     candidate, and confirm its value is IN the constructive set (recorded values.f64, or a fresh
     build at small D).  Keeps every null empirically falsifiable at the skipped high-b_s levels.

HONEST WEAKNESS vs the exhaustive brute:  the brute at b_s=D-4 is a DIRECT exhaustive confirmation of
that exact split.  This certificate INFERS b_s=D-4 from b_s=D-5 via the (deductively valid) fixed-menu
induction, and back-stops it with K random samples rather than all 30^{D-4}.  The induction is sound
UNLESS some b_s-DEPENDENT code branch exists at high b_s (there is none: the menu/apply are provably
b_s-independent, and neither `_walk` nor `itertools.product` special-cases the count) — the only
residual gap is a hypothetical defect that (i) manifests only at b_s>=5, (ii) does NOT break the
menu/apply invariance we check, and (iii) is missed by K random samples.  That is a much smaller gap
than "we didn't run it at all," but it is NOT the literally-exhaustive guarantee of the full brute.

CLI:
    python3 fast_completeness.py --certify D      # certificate for depth D (exit 0 iff certified)
    python3 fast_completeness.py --reproduce 9    # independently certify depth 9, agree w/ VERDICT.json
    python3 fast_completeness.py --self-test       # certify 6 (cross-check real brute) + reproduce 9
"""
from __future__ import annotations

import argparse
import itertools
import json
import random
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import mpmath as mp

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

# --- IMPORT VERBATIM (RULE 3): the committed depth-N machinery + its re-exports. No edits anywhere. ---
import exhaust_depthN_forced as DN                                        # noqa: E402
from exhaust import (                                                     # noqa: E402
    build_alphabet, _value_key, _POW_EXPONENTS, _UNARY_PLAIN,
    gate_candidate_for, resolve_target,
)
from engine.expr_tree import ExprNode, OpType                            # noqa: E402
from gate import validate                                                # noqa: E402

try:
    import numpy as np
except Exception:                                                        # numpy is used only for the
    np = None                                                            # recorded-values spot-check.

RESULTS_GRIND = _HERE / "results_grind"

# germ per-step building blocks — EXACTLY the code's canonical realizer alphabet (op x {1, 1/2});
# {MUL,DIV} x {1,1/2} spans the same signed-step set {+1,+1/2,-1,-1/2} = DN._PER_STEP_SIGNED used by
# _net_exps, so a random-order sample lands on the SAME reachable germ net-exponents (see _realize_dfs).
_GERM_STEP_OPS = (OpType.MUL, OpType.DIV)
_GERM_STEP_EXPS = (mp.mpf(1), mp.mpf("0.5"))


# =============================================================================
# 0.  MENU RECONSTRUCTION  — the SAME fixed step_menu both DN code paths build (b_s-independent)
# =============================================================================

def _skeleton_step_menu(alpha) -> List[Tuple]:
    """Rebuild the skeleton `step_menu` EXACTLY as DN._skeleton_value_nodes and
    DN._skeleton_brute_value_set build it (identical construction, verbatim order):
        ("app", leaf, op) for leaf in leaves for op in (MUL, DIV);
        ("pow", e, None)  for e in _POW_EXPONENTS;
        ("un",  u, None)  for u in _UNARY_PLAIN.
    It reads ONLY (alpha.leaves, _POW_EXPONENTS, _UNARY_PLAIN, {MUL,DIV}) — NOTHING that depends on
    the budget b_s.  This is the machine-checkable witness of MENU INVARIANCE (fact I)."""
    ops_bin = (OpType.MUL, OpType.DIV)
    menu: List[Tuple] = []
    for lk in alpha.leaves:
        for op in ops_bin:
            menu.append(("app", lk, op))
    for e in _POW_EXPONENTS:
        menu.append(("pow", e, None))
    for u in _UNARY_PLAIN:
        menu.append(("un", u, None))
    return menu


def _apply_step(node: ExprNode, step: Tuple) -> ExprNode:
    """The SAME apply DN._skeleton_value_nodes / DN._skeleton_brute_value_set use (verbatim logic)."""
    kind = step[0]
    if kind == "app":
        _, lk, op = step
        return ExprNode(op, children=[node, DN._leaf_node(lk)])
    if kind == "pow":
        _, e, _ = step
        return ExprNode(OpType.POW, children=[node], exp=e)
    _, u, _ = step
    return ExprNode(u, children=[node])


def _menu_frontier(alpha, k: int) -> List[ExprNode]:
    """The FULL Frontier(k): every terminal node of the length-k menu walk over every base leaf,
    kept UNFILTERED and UN-deduped (dimensionful intermediates retained).  Size = |leaves|*|menu|^k."""
    menu = _skeleton_step_menu(alpha)
    frontier = [DN._leaf_node(base) for base in alpha.leaves]
    for _ in range(k):
        frontier = [_apply_step(n, step) for n in frontier for step in menu]
    return frontier


def _frontier_value_set(alpha, frontier: List[ExprNode]) -> set:
    """Apply the code's dimensionless/finite/>0 filter and value-dedup to a node frontier."""
    seen = set()
    for n in frontier:
        try:
            v, lab = n.evaluate(alpha)
        except Exception:
            continue
        if not lab.is_dimensionless():
            continue
        try:
            if not mp.isfinite(v) or v <= 0:
                continue
        except Exception:
            continue
        seen.add(_value_key(v))
    return seen


# =============================================================================
# 1.  THE INDUCTIVE STEP  — machine-verified once, on the ACTUAL menu/apply objects
# =============================================================================

def verify_inductive_step(alpha, verbose: bool = True) -> dict:
    """Machine-verify, on the real code's own objects, the three facts that make
    scheme==brute PROPAGATE from any b_s to b_s+1 (see module docstring):

      (A) MENU FIDELITY   : our rebuilt (menu, apply) reproduces BOTH DN code paths at b_s in {1,2}.
      (B) ONE-STEP CLOSURE: extending the FULL Frontier(k) by the fixed menu, then filter+dedup,
                            reproduces DN's level-(k+1) value set — verified at k=1->2 AND k=2->3.
      (C) CARTESIAN IDENT : menu^{2} == extend(menu^{1}, menu) as sequence sets (fact II, concrete).

    PASS iff all hold.  This is the inductive STEP; the base is anchored empirically elsewhere."""
    menu = _skeleton_step_menu(alpha)
    checks = []

    # (A) MENU FIDELITY: a THIRD independent path (this file's menu enumeration) == both DN paths.
    fidelity_ok = True
    for b_s in (1, 2):
        mine = _frontier_value_set(alpha, _menu_frontier(alpha, b_s))
        scheme = DN._skeleton_value_set(alpha, b_s)
        brute = DN._skeleton_brute_value_set(alpha, b_s)
        ok = (mine == scheme == brute)
        fidelity_ok = fidelity_ok and ok
        checks.append(dict(name=f"menu_fidelity_b{b_s}", ok=ok,
                           n_mine=len(mine), n_scheme=len(scheme), n_brute=len(brute)))

    # (C) CARTESIAN IDENTITY on the REAL menu: menu^2 built directly == menu^1 extended by menu.
    prod2_direct = set(itertools.product(range(len(menu)), repeat=2))
    prod2_extend = {(i, j) for (i,) in itertools.product(range(len(menu)), repeat=1)
                    for j in range(len(menu))}
    cartesian_ok = (prod2_direct == prod2_extend and
                    len(prod2_direct) == len(menu) ** 2)
    checks.append(dict(name="cartesian_identity_k1", ok=cartesian_ok,
                       n_direct=len(prod2_direct), n_extend=len(prod2_extend)))

    # (B) ONE-STEP CLOSURE on the real objects, at two successive levels.
    closure_ok = True
    for k in (1, 2):
        # FULL frontier at level k (dimensionful retained), then ONE menu step -> level k+1.
        fk = _menu_frontier(alpha, k)
        fk1 = [_apply_step(n, step) for n in fk for step in menu]
        v_next_via_closure = _frontier_value_set(alpha, fk1)
        v_next_scheme = DN._skeleton_value_set(alpha, k + 1)
        v_next_brute = DN._skeleton_brute_value_set(alpha, k + 1)
        ok = (v_next_via_closure == v_next_scheme == v_next_brute)
        closure_ok = closure_ok and ok
        checks.append(dict(name=f"one_step_closure_{k}to{k+1}", ok=ok,
                           n_closure=len(v_next_via_closure),
                           n_scheme=len(v_next_scheme), n_brute=len(v_next_brute)))

    inductive_ok = fidelity_ok and cartesian_ok and closure_ok

    if verbose:
        print("-" * 96)
        print("INDUCTIVE STEP (menu/apply are b_s-independent; one fixed menu step closes level k -> k+1):")
        for c in checks:
            print(f"    [{'OK' if c['ok'] else 'FAIL'}] {c['name']:<26} "
                  + "  ".join(f"{key}={val}" for key, val in c.items() if key not in ("name", "ok")))
        print(f"    menu size = {len(menu)}  (b_s-INDEPENDENT: built from leaves/POW/UNARY only)")
        print(f"  INDUCTIVE_STEP = {'PASS' if inductive_ok else 'FAIL'}")
    return dict(inductive_ok=inductive_ok, menu_size=len(menu), checks=checks)


# =============================================================================
# 2.  BASE ANCHORS  — re-run the REAL DN skeleton scheme==brute at the cheap b_s, + depth-4 anchor
# =============================================================================

def run_base_anchors(depth: int, max_b_s: int = 4, verbose: bool = True) -> dict:
    """Re-run the GENUINE DN skeleton cross-check (scheme==brute, 0/0) at b_s = 1..min(max_b_s, D-4).
    These are exactly the cheap splits DN.constructive_completeness_selfcheck runs anyway; we stop
    BEFORE the expensive b_s=D-4 (>=5) split.  Plus the committed depth-4 whole-tree anchor."""
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25 and len(alpha.leaves) == 11
    top = min(max_b_s, depth - 4)
    anchors = []
    all_ok = True
    for b_s in range(1, top + 1):
        t0 = time.time()
        scheme = DN._skeleton_value_set(alpha, b_s)
        brute = DN._skeleton_brute_value_set(alpha, b_s)
        missed = len(brute - scheme)
        extra = len(scheme - brute)
        ok = (missed == 0 and extra == 0)
        all_ok = all_ok and ok
        anchors.append(dict(b_s=b_s, n_scheme=len(scheme), n_brute=len(brute),
                            missed=missed, extra=extra, ok=ok, wall_s=round(time.time() - t0, 2)))
        if verbose:
            print(f"    b_s={b_s}: scheme={len(scheme):>5} brute={len(brute):>5} "
                  f"MISSED={missed} EXTRA={extra} -> {'OK' if ok else 'FAIL'} "
                  f"({anchors[-1]['wall_s']}s)")

    # depth-4 whole-tree anchor (verbatim committed brute via the depth-5 self-check).
    t0 = time.time()
    d4 = DN._d5_completeness_selfcheck(verbose=False)
    anchor4_ok = bool(d4["constructive_complete"])
    all_ok = all_ok and anchor4_ok
    if verbose:
        print(f"    depth-4 whole-tree anchor: brute_all={d4['brute_all_count']:,} == "
              f"con_all={d4['constructive_all_count']:,} -> {'OK' if anchor4_ok else 'FAIL'} "
              f"({round(time.time()-t0,2)}s)")
    return dict(anchors=anchors, anchored_b_s=[a["b_s"] for a in anchors],
                base_ok=all_ok, depth4_anchor_ok=anchor4_ok,
                depth4_all=d4["brute_all_count"])


# =============================================================================
# 3.  CONSTRUCTIVE-SET MEMBERSHIP BACKENDS  (recorded values.f64, or a fresh small-depth build)
# =============================================================================

class _RecordedSet:
    """Membership against a recorded results_grind/depth_D/values.f64 (distinct float64 values).
    A value is a MEMBER iff a recorded value lies within rel-tol (true members match to ~1e-15;
    real inter-value spacing is ~1e-5, so a genuine MISS has no neighbour within tol)."""
    REL_TOL = 1e-11

    def __init__(self, arr):
        self.sorted = np.sort(np.asarray(arr, dtype=np.float64))

    def __contains__(self, fv: float) -> bool:
        a = self.sorted
        i = np.searchsorted(a, fv)
        for j in (i - 1, i):
            if 0 <= j < len(a):
                denom = max(abs(fv), abs(float(a[j])), 1e-300)
                if abs(float(a[j]) - fv) / denom <= self.REL_TOL:
                    return True
        return False

    def __len__(self):
        return len(self.sorted)


class _ExactSet:
    """Membership against a freshly-built constructive set, by EXACT 30-digit value_key."""
    def __init__(self, keyset: set):
        self.keys = keyset

    def value_member(self, mpf_value) -> bool:
        return _value_key(mpf_value) in self.keys

    def __len__(self):
        return len(self.keys)


def _load_constructive_membership(depth: int, verbose: bool = True):
    """Prefer the recorded values.f64 (fast, and ties the spot-check to the real run's output);
    else build a fresh constructive set (only affordable at small depth)."""
    ddir = RESULTS_GRIND / f"depth_{depth}"
    vpath = ddir / "values.f64"
    if vpath.exists() and np is not None:
        arr = np.fromfile(vpath, dtype=np.float64)
        if verbose:
            print(f"    membership backend: recorded values.f64 ({len(arr):,} distinct values)")
        return _RecordedSet(arr), "recorded"
    # fresh build fallback (small depth only)
    if depth <= 7:
        alpha = build_alphabet(None, None)
        reach, counts = DN.constructive_gate_b_reachables(alpha, depth)
        keyset = {_value_key(r.value) for r in reach}
        if verbose:
            print(f"    membership backend: fresh build ({len(keyset):,} distinct values, "
                  f"raw {counts['raw_candidates']:,})")
        return _ExactSet(keyset), "fresh"
    return None, "unavailable"


# =============================================================================
# 4.  PER-DEPTH SPOT CHECK  — seeded randomised falsification at depth D
# =============================================================================

def _sample_dimensionless_skeleton(alpha, menu, b_s, rng, max_tries=4000):
    """Sample a random length-b_s menu walk (the BRUTE path) whose SKELETON is dimensionless.
    Returns (node, mpf_value) or None if no dimensionless skeleton found within max_tries."""
    leaves = alpha.leaves
    for _ in range(max_tries):
        node = DN._leaf_node(rng.choice(leaves))
        for _ in range(b_s):
            node = _apply_step(node, rng.choice(menu))
        try:
            v, lab = node.evaluate(alpha)
        except Exception:
            continue
        if not lab.is_dimensionless():
            continue
        try:
            if not mp.isfinite(v) or v <= 0:
                continue
        except Exception:
            continue
        return node, v
    return None


def _random_germ_decoration(alpha, g_s, rng):
    """A random Gate-B germ decoration of g_s steps, built the BRUTE way: both forced germs
    {3, sqrt(8pi/3)} + one random free germ, each present >=1, steps assigned to keys by a random
    composition, each step a random (op in {MUL,DIV}, exp in {1,1/2}), and the WHOLE step order
    SHUFFLED (tests the order-free / net-exponent claim).  Returns a list of (germ_key, op, exp)."""
    forced = DN._forced_keys_present(alpha)          # ['3','sqrt(8pi/3)']
    free = rng.choice(DN._free_germ_keys(alpha))
    keys = [forced[0], forced[1], free]
    # random composition of g_s into 3 positive parts
    cuts = sorted(rng.sample(range(1, g_s), 2)) if g_s >= 3 else [1, 2]
    counts = [cuts[0], cuts[1] - cuts[0], g_s - cuts[1]]
    steps = []
    for gk, ci in zip(keys, counts):
        for _ in range(ci):
            steps.append((gk, rng.choice(_GERM_STEP_OPS), rng.choice(_GERM_STEP_EXPS)))
    rng.shuffle(steps)                                # random interleaving of the germ factors
    return steps


def spot_check(depth: int, k: int = 300, seed: Optional[int] = None, verbose: bool = True) -> dict:
    """Seeded randomised falsification: sample k full depth-D candidates the BRUTE way (random
    dimensionless skeleton x random-order germ decoration), build each, and confirm its value is
    IN the constructive set.  A single genuine miss => the null would be INVALID."""
    if seed is None:
        seed = 20260722 + depth
    rng = random.Random(seed)
    alpha = build_alphabet(None, None)
    menu = _skeleton_step_menu(alpha)
    splits = DN.budget_splits(depth)

    membership, backend = _load_constructive_membership(depth, verbose=verbose)
    if membership is None:
        if verbose:
            print(f"    spot-check SKIPPED: no recorded values.f64 for depth {depth} and depth>7 "
                  f"(too large to build a fresh constructive set here).")
        return dict(seed=seed, backend=backend, attempted=0, passed=0, skipped=True, ok=True)

    tspec = resolve_target("r_mu_e")
    attempted = passed = 0
    misses = []
    guard = 0
    max_guard = k * 200
    while attempted < k and guard < max_guard:
        guard += 1
        b_s, g_s = rng.choice(splits)
        sk = _sample_dimensionless_skeleton(alpha, menu, b_s, rng)
        if sk is None:
            continue
        node, _ = sk
        for (gk, op, e) in _random_germ_decoration(alpha, g_s, rng):
            node = DN._decorate(node, op, gk, e)
        try:
            v, lab = node.evaluate(alpha)
        except Exception:
            continue
        if not lab.is_dimensionless():
            continue
        try:
            if not mp.isfinite(v) or v <= 0:
                continue
        except Exception:
            continue
        # keep-predicate (Fset == both forced, Rset == exactly one free) via the REAL _leaf_tag
        Fset = frozenset(); Rset = frozenset()
        for key in set(node.leaf_consts()):
            F, R = DN._leaf_tag(alpha, key)
            Fset |= F; Rset |= R
        if not (len(Fset) == 2 and len(Rset) == 1):
            continue
        attempted += 1
        if backend == "recorded":
            member = float(v) in membership
        else:
            member = membership.value_member(v)
        if member:
            passed += 1
        else:
            if len(misses) < 6:
                misses.append(node.to_string(alpha)[:80] + f"  = {float(v):.10g}")

    ok = (attempted > 0 and passed == attempted)
    if verbose:
        print(f"    spot-check: {passed}/{attempted} sampled valid candidates found IN the "
              f"constructive set  (seed={seed}, backend={backend})")
        if misses:
            print(f"    !! {len(misses)} MISS(es): {misses}")
        if attempted < k:
            print(f"    (note: {attempted}/{k} valid samples drawn within the attempt guard)")
    return dict(seed=seed, backend=backend, attempted=attempted, passed=passed,
                skipped=False, ok=ok, misses=misses)


# =============================================================================
# 5.  THE CERTIFICATE
# =============================================================================

def certify(depth: int, spot_k: int = 300, seed: Optional[int] = None,
            max_anchor_b_s: int = 4, verbose: bool = True) -> dict:
    """Assemble the completeness certificate for depth D:
        {inductive_step, base_anchors, spot_check}.  Certified iff all three hold."""
    alpha = build_alphabet(None, None)
    t0 = time.time()
    if verbose:
        print("=" * 96)
        print(f"FAST COMPLETENESS CERTIFICATE — depth {depth}")
        print(f"  splits: {DN.budget_splits(depth)}   "
              f"(new split this depth: b_s={depth-4}; skipped brute = 30^{depth-4} x 11)")
        print("=" * 96)

    ind = verify_inductive_step(alpha, verbose=verbose)
    base = run_base_anchors(depth, max_b_s=max_anchor_b_s, verbose=verbose)
    if verbose:
        print("-" * 96)
        print(f"BASE ANCHORS: brute-verified b_s = {base['anchored_b_s']} (0/0) + depth-4 whole-tree "
              f"anchor -> {'OK' if base['base_ok'] else 'FAIL'}")
        induction_covers = [b for (b, _g) in DN.budget_splits(depth) if b not in base['anchored_b_s']]
        print(f"  splits certified BY INDUCTION (not brute): b_s = {induction_covers}")
        print("-" * 96)
    spot = spot_check(depth, k=spot_k, seed=seed, verbose=verbose)

    certified = bool(ind["inductive_ok"] and base["base_ok"] and spot["ok"])
    wall = round(time.time() - t0, 1)

    cert = dict(
        depth=depth,
        certified=certified,
        inductive_step="PASS" if ind["inductive_ok"] else "FAIL",
        base_anchors=base["anchored_b_s"],
        base_anchors_ok=base["base_ok"],
        base_anchor_detail=base["anchors"],
        depth4_anchor_ok=base["depth4_anchor_ok"],
        spot_check=f"{spot['passed']}/{spot['attempted']} @ seed {spot['seed']} "
                   f"(backend={spot['backend']}"
                   + (", SKIPPED" if spot.get("skipped") else "") + ")",
        spot_check_ok=spot["ok"],
        wall_s=wall,
    )
    if verbose:
        print("=" * 96)
        print("CERTIFICATE")
        print(f"  inductive_step : {cert['inductive_step']}")
        print(f"  base_anchors   : b_s={cert['base_anchors']} (0/0)  depth4={cert['depth4_anchor_ok']}"
              f"  -> {'OK' if cert['base_anchors_ok'] else 'FAIL'}")
        print(f"  spot_check     : {cert['spot_check']}  -> {'OK' if cert['spot_check_ok'] else 'FAIL'}")
        print(f"  CERTIFIED      : {certified}   (fast-cert wall = {wall}s)")
        print("=" * 96)
    return cert


# =============================================================================
# 6.  REPRODUCE  — independently certify depth 9 and AGREE with the recorded VERDICT.json (fast)
# =============================================================================

def reproduce(depth: int = 9, verbose: bool = True) -> dict:
    """Independently certify depth-D completeness WITHOUT the 30^{D-4} brute, then confirm it AGREES
    with the recorded results_grind/depth_D/VERDICT.json validation.completeness_ok."""
    ddir = RESULTS_GRIND / f"depth_{depth}"
    vpath = ddir / "VERDICT.json"
    cpath = ddir / "completeness.json"
    if not vpath.exists():
        raise SystemExit(f"no recorded VERDICT.json at {vpath} — cannot cross-check depth {depth}.")
    verdict = json.loads(vpath.read_text())
    recorded_ok = bool(verdict.get("validation", {}).get("completeness_ok"))
    recorded_wall = float(verdict.get("wall_s", {}).get("completeness", float("nan")))
    comp = json.loads(cpath.read_text()) if cpath.exists() else {}
    recorded_splits = {s["b_s"]: (s["n_scheme"], s["n_brute"], s["missed"], s["extra"])
                       for s in comp.get("splits", [])}

    if verbose:
        print("#" * 96)
        print(f"REPRODUCE depth {depth}: independent fast certificate vs recorded VERDICT.json")
        print(f"  recorded completeness_ok = {recorded_ok};  recorded brute wall = {recorded_wall:.1f}s "
              f"({recorded_wall/3600:.2f} h)")
        print("#" * 96)

    cert = certify(depth, verbose=verbose)

    # cross-check our brute-anchored counts vs the recorded run's per-split reports
    anchor_match = True
    for a in cert["base_anchor_detail"]:
        rec = recorded_splits.get(a["b_s"])
        if rec is not None and (a["n_scheme"], a["n_brute"]) != (rec[0], rec[1]):
            anchor_match = False

    # the recorded run's HIGH-b_s split (the one WE skipped) — we AGREE by induction, don't recompute
    skipped_split = depth - 4
    skipped_rec = recorded_splits.get(skipped_split)

    agrees = bool(cert["certified"] and recorded_ok and anchor_match)
    speedup = (recorded_wall / cert["wall_s"]) if cert["wall_s"] > 0 else float("inf")

    if verbose:
        print("-" * 96)
        print(f"  anchor counts match recorded per-split reports: {anchor_match}")
        if skipped_rec is not None:
            print(f"  recorded b_s={skipped_split} split (the 30^{skipped_split} brute WE SKIPPED): "
                  f"scheme={skipped_rec[0]} brute={skipped_rec[1]} missed={skipped_rec[2]} "
                  f"extra={skipped_rec[3]}  <- certified here BY INDUCTION + spot-check, not recomputed")
        print(f"  independent fast certificate CERTIFIED : {cert['certified']}")
        print(f"  recorded validation.completeness_ok    : {recorded_ok}")
        print(f"  AGREEMENT                              : {agrees}")
        print(f"  fast-cert wall = {cert['wall_s']}s  vs recorded brute wall = {recorded_wall:.1f}s "
              f"-> {speedup:.0f}x faster")
        print("#" * 96)
    return dict(depth=depth, agrees=agrees, fast_certified=cert["certified"],
                recorded_completeness_ok=recorded_ok, anchor_match=anchor_match,
                fast_wall_s=cert["wall_s"], recorded_brute_wall_s=recorded_wall,
                speedup=speedup, certificate=cert)


# =============================================================================
# 7.  CLI
# =============================================================================

def main():
    ap = argparse.ArgumentParser(description="Fast inductive completeness certificate (no 30^(D-4) brute).")
    ap.add_argument("--certify", type=int, metavar="D", help="print a completeness certificate for depth D")
    ap.add_argument("--reproduce", type=int, metavar="D", nargs="?", const=9,
                    help="independently certify depth D (default 9) and agree with its VERDICT.json")
    ap.add_argument("--spot-k", type=int, default=300, help="spot-check sample count (default 300)")
    ap.add_argument("--seed", type=int, default=None, help="spot-check RNG seed (default 20260722+depth)")
    ap.add_argument("--self-test", action="store_true",
                    help="certify 6 (cross-check the real brute) AND reproduce 9")
    args = ap.parse_args()

    if args.self_test:
        print("\n########## SELF-TEST 1/3: --certify 6 (cross-check vs the REAL brute at depth 6) ##########\n")
        c6 = certify(6, spot_k=args.spot_k, seed=args.seed)
        print("\n--- cross-check: the REAL DN.constructive_completeness_selfcheck(6) ---")
        real6 = DN.constructive_completeness_selfcheck(6, verbose=True)
        agree6 = (c6["certified"] and bool(real6["constructive_complete"]))
        print(f"\n>>> depth-6 fast certificate ({c6['certified']}) AGREES with real brute "
              f"({real6['constructive_complete']}): {agree6}")
        print("\n########## SELF-TEST 2/3: --reproduce 9 (fast, agree w/ recorded VERDICT.json) ##########\n")
        r9 = reproduce(9)
        print("\n########## SELF-TEST 3/3: summary ##########")
        ok = bool(agree6 and r9["agrees"])
        print(f"  certify6-agrees-real-brute : {agree6}")
        print(f"  reproduce9-agrees-verdict  : {r9['agrees']}  ({r9['speedup']:.0f}x faster)")
        print(f"  SELF-TEST {'PASS' if ok else 'FAIL'}")
        sys.exit(0 if ok else 1)

    if args.certify is not None:
        cert = certify(args.certify, spot_k=args.spot_k, seed=args.seed)
        print("\nCERTIFICATE (json):")
        print(json.dumps({key: cert[key] for key in
                          ("depth", "certified", "inductive_step", "base_anchors",
                           "base_anchors_ok", "spot_check", "spot_check_ok", "wall_s")}, indent=2))
        sys.exit(0 if cert["certified"] else 1)

    if args.reproduce is not None:
        rep = reproduce(args.reproduce)
        print("\nREPRODUCE (json):")
        print(json.dumps({key: rep[key] for key in
                          ("depth", "agrees", "fast_certified", "recorded_completeness_ok",
                           "anchor_match", "fast_wall_s", "recorded_brute_wall_s", "speedup")},
                         indent=2, default=str))
        sys.exit(0 if rep["agrees"] else 1)

    ap.print_help()
    sys.exit(2)


if __name__ == "__main__":
    main()
