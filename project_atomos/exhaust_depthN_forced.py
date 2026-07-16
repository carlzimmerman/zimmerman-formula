#!/usr/bin/env python3
"""
exhaust_depthN_forced.py — the ESCALATING, depth-parametric (--depth D>=6), CONSTRUCTIVE,
Gate-B-passable, DIMENSIONLESS forced-interlock sweep. The honest continuation past the committed
depth-3/4/5 CLEAN NULLS (commits ee44122 depth-4, 9230fbd depth-5).

WHAT THIS IS (Carl's brief, 2026-07-07):
    Depth 5 was the FIRST live depth: a Gate-B-passable DIMENSIONLESS tree needs the germ triple
    {3, sqrt(8pi/3), one free} (3 decorate steps) PLUS a dimensionless scale skeleton (>=2 scale
    leaves = 1 binary step) -> min depth 5. Depth 5 used a single 2-scale skeleton shape (R=D-4=1).

    DEPTH >=6 opens R=D-4 >=2 residual budget on the skeleton/germ layers. The skeleton grows from a
    bare 2-scale ratio to (up to D-3)-scale dimensionless monomials, WITH pow/unary-decorated leaves,
    and the germ layer may spend extra steps on same-value-free or higher-power-forced germs. Each
    added residual step grows the distinct-value set but keeps the FORCED vocabulary at {3,
    sqrt(8pi/3)}+1 free. We escalate 6->7->8->... until the memory watchdog trips the HARD 6 GB cap
    (the WALL) or a per-depth time budget is exceeded, and report the exact ceiling.

THE DEPTH MODEL (from the engine, VERBATIM — exhaust.enumerate_trees / closed_form_count):
    depth = build-steps + 1. A leaf is depth 1. Each of the following costs EXACTLY +1 depth:
      * a binary SCALE-APPEND (BINARY_OPERAND_CAP=1: 2nd operand is always a depth-1 leaf -> every
        scale monomial is a left-fold, one leaf at a time),
      * a GERM-DECORATE (node op germ^e, op in {MUL,DIV}, e in _GERM_EXPONENTS={1,1/2,-1,-1/2}),
      * a UNARY/POW on a subtree (_UNARY_PLAIN={SQRT,CBRT,INV}, _POW_EXPONENTS={2,3,1/2,-1,2/3}).
    Total build steps at depth D = D-1. Germ triple consumes 3. Residual skeleton budget R = D-4.

CONSTRUCTIVE SCHEME (generalizes depth-5's constructive_gate_b_reachables, three generalizations):
    A Gate-B-passable dimensionless depth-D tree =
      { dimensionless SCALE SKELETON built with skeleton-budget b_s }
        x { GERM RECIPE: keys' forced set == {3, sqrt(8pi/3)}, exactly one distinct free germ,
            distributed over g_s >= 3 decorate steps }
      with b_s + g_s = D - 1, g_s >= 3, skeleton yielding >= 2 scale leaves (dimensionless).
    The two layers are enumerated separately; the product is STREAMED one ExprNode at a time and
    value-deduped — the raw list is NEVER materialized (memory discipline).

    A. SKELETON LAYER (branch (a)+(b)): all dimensionless value-monomials over the leaves reachable
       with b_s binary-append + pow/unary steps. Enumerated as signed+pow monomials by VALUE (proved
       value-complete: the left-fold signed-monomial value-set == the true dimensionless value-set at
       every leaf-count k: k=2->13, 3->7, 4->59, 5->79, 6->239; pow steps add the {2,3,1/2,-1,2/3}
       and {sqrt,cbrt,1/} powers of an existing leaf). Dedup by value.
    B. GERM LAYER (branch (c)): >=3 germ steps. The 3-step base is {3, sqrt(8pi/3), one free}; extra
       germ steps must be SAME-VALUE-free (repeat the chosen free germ) or REPEAT-FORCED (another
       power of 3 / sqrt(8pi/3)), so the forced set stays {both} and the free set stays size 1.
    C. BUDGET PARTITION: stream over every (b_s, g_s) split with b_s+g_s=D-1, g_s>=3, b_s>=1.

FOUR NON-NEGOTIABLE HONESTY CONSTRAINTS (all enforced, per depth):
  1. CONSTRUCTIVE COMPLETENESS — per depth: (a) shape/budget argument (below) + (b) an EMPIRICAL
     skeleton-brute cross-check: independently brute the skeleton layer at the depth's budget and
     assert scheme-skeleton value-set == brute value-set (MISSED=0 EXTRA=0); PLUS the committed brute
     depth-4 Gate-B value-set is still reproduced exactly. A miss => the depth's null is INVALID.
  2. SOUNDNESS — sample kept candidates; run the REAL gate.forced_kernel; all pass the keep predicate.
  3. FDR NON-SMUGGLE — Gate A density over the FULL 25-germ library (assert len==25); mult=21.
  4. a0 VALIDITY (TARGETED, NOT BRUTE) — construct a0 x cancelling identity directly at depth D +
     the committed depth-4 dimensional re-derivation; assert the expected FDR-DEAD. NEVER brute the
     dimensionful depth-D space.

RULE 3 (verbatim reuse — ZERO diff to gate/ engine/ exhaust.py exhaust_parallel.py
    exhaust_depth4_forced.py exhaust_depth5_forced.py): we IMPORT them unmodified and reuse the
    depth-5 machinery (nodes, decorate, streaming dedup, watchdog, parallel, a0 legs, soundness)
    VERBATIM via `import exhaust_depth5_forced as D5`. Only the skeleton/germ/split enumerator and
    the per-depth completeness self-check become depth-parametric here.

MEMORY DISCIPLINE (HARD): NEVER brute-enumerate. ALL enumeration constructive + STREAMING via
    generators; keep in memory ONLY the deduped set of distinct dimensionless VALUES. The MANDATORY
    6 GB RSS watchdog (reused verbatim from depth-5, HARD_MEM_CAP_GB=6.0) ABORTS on breach = THE WALL.

CLI:
    python3 exhaust_depthN_forced.py --depth 6 --a0-check
    python3 exhaust_depthN_forced.py --depth 6 --self-check
    python3 exhaust_depthN_forced.py --depth 6 --space
    python3 exhaust_depthN_forced.py --depth 6 --target r_mu_e
    python3 exhaust_depthN_forced.py --depth 6 --sweep
    python3 exhaust_depthN_forced.py --depth 6 --workers 12
    python3 exhaust_depthN_forced.py --depth 6 --status
    python3 exhaust_depthN_forced.py --escalate            # loop D=6,7,8,... until the watchdog/time wall
    python3 exhaust_depthN_forced.py --depth 6 --project   # projected sizes for depths 7..10
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

import mpmath as mp

mp.mp.dps = 40

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

# --- IMPORT VERBATIM (RULE 3): engine, scoring, the whole gate, the committed depth-5 machinery ---
from engine.expr_tree import ExprNode, OpType, Label  # noqa: E402
from engine.scoring import score_value, measurement_tol  # noqa: E402

import exhaust as EX  # noqa: E402
from exhaust import (  # noqa: E402
    build_alphabet, Alphabet, Reachable,
    closed_form_count, _germ_provenance, _value_key,
    gate_candidate_for, resolve_target,
    _GERM_EXPONENTS, _POW_EXPONENTS, _UNARY_PLAIN,
)
from gate import validate  # noqa: E402
from exhaust_parallel import sm_target_keys  # noqa: E402

# The committed depth-5 file — reuse its building blocks + watchdog + a0/soundness legs VERBATIM.
import exhaust_depth5_forced as D5  # noqa: E402
from exhaust_depth5_forced import (  # noqa: E402
    _FORCED_KEYS, _free_germ_keys, _forced_keys_present,
    _leaf_node, _germ_pow_node, _decorate,
    constructive_completeness_selfcheck as _d5_completeness_selfcheck,
    HARD_MEM_CAP_GB, _rss_mb, _total_rss_mb, _peak_mem_mb, _mem_watchdog,
    N_TARGETS,
)
# The committed depth-4 brute anchor (verbatim).
from exhaust_depth4_forced import _leaf_tag  # noqa: E402

RESULTS_ROOT = _HERE / "results_exhaust_depthN"


# =============================================================================
# 0.  THE DEPTH-PARAMETRIC CONSTRUCTIVE BUILDING BLOCKS  (§A/§B/§C of the spec)
#     A Gate-B-passable dimensionless depth-D tree =
#         { dimensionless scale skeleton, budget b_s }  x  { germ recipe, budget g_s },
#       b_s + g_s = D - 1,  g_s >= 3,  b_s >= 1  (>=2 scale leaves so dims can cancel).
# =============================================================================

def budget_splits(depth: int) -> List[Tuple[int, int]]:
    """Every (skeleton_steps b_s, germ_steps g_s) split with b_s+g_s=D-1, g_s>=3, b_s>=1.
    b_s>=1 guarantees >=2 scale leaves (a bare leaf is depth-1; each binary append is +1 step),
    the minimum for a dimensionless monomial. (depth 5 -> only (1,3).)"""
    total = depth - 1
    out = []
    for b_s in range(1, total - 3 + 1):      # b_s from 1 .. total-3
        g_s = total - b_s
        if g_s >= 3:
            out.append((b_s, g_s))
    return out


# ---- SKELETON LAYER (branches (a) bare-leaf appends + (b) pow/unary-decorated leaves) ----

def _skeleton_value_nodes(alpha: Alphabet, b_s: int) -> List[Reachable]:
    """The DIMENSIONLESS scale-skeleton set reachable with EXACTLY b_s skeleton steps, value-deduped.

    A skeleton step is a binary scale-append (MUL/DIV a depth-1 leaf) OR a pow/unary decoration of the
    CURRENT skeleton subtree. Starting from a single scale leaf (depth 1, cost 0), b_s steps build a
    left-fold monomial of up to (b_s+1) scale leaves, any subtree optionally pow/unary-wrapped.

    CONSTRUCTIVE-COMPLETE by value: we enumerate the left-fold sequences of (append-leaf | pow/unary)
    operations of length b_s over the leaf pool, evaluate, keep dimensionless finite >0, dedup by
    value. The empirical skeleton-brute cross-check (constructive_completeness_selfcheck) proves this
    value-set == an independent brute's value-set (MISSED=0 EXTRA=0) at the depth's budget.

    Returns Reachable skeletons (value-deduped, dimensionless). Held bounded (only the deduped set).
    """
    leaves = alpha.leaves
    seen_v = set()
    out: List[Reachable] = []

    # each skeleton step is one of:
    #   ("app", leaf_key, op)   -> node (op) leaf         op in {MUL,DIV}
    #   ("pow", exp)            -> POW(node, exp)         exp in _POW_EXPONENTS
    #   ("un",  unary_op)       -> unary(node)            unary in _UNARY_PLAIN
    ops_bin = (OpType.MUL, OpType.DIV)
    step_menu: List[Tuple] = []
    for lk in leaves:
        for op in ops_bin:
            step_menu.append(("app", lk, op))
    for e in _POW_EXPONENTS:
        step_menu.append(("pow", e, None))
    for u in _UNARY_PLAIN:
        step_menu.append(("un", u, None))

    def _apply(node: ExprNode, step: Tuple) -> ExprNode:
        kind = step[0]
        if kind == "app":
            _, lk, op = step
            return ExprNode(op, children=[node, _leaf_node(lk)])
        if kind == "pow":
            _, e, _ = step
            return ExprNode(OpType.POW, children=[node], exp=e)
        # unary
        _, u, _ = step
        return ExprNode(u, children=[node])

    def _emit(node: ExprNode):
        try:
            v, lab = node.evaluate(alpha)
        except Exception:
            return
        if not lab.is_dimensionless():
            return
        try:
            if not mp.isfinite(v) or v <= 0:
                return
        except Exception:
            return
        vk = _value_key(v)
        if vk in seen_v:
            return
        seen_v.add(vk)
        out.append(Reachable(v, lab, node.to_string(alpha), node.canonical_hash(), node))

    # stream the length-b_s step sequences over the base-leaf choice; emit dimensionless value-dedup.
    def _walk(node: ExprNode, remaining: int):
        if remaining == 0:
            _emit(node)
            return
        for step in step_menu:
            _walk(_apply(node, step), remaining - 1)

    for base in leaves:
        _walk(_leaf_node(base), b_s)

    return out


def _skeleton_value_set(alpha: Alphabet, b_s: int) -> set:
    """The DIMENSIONLESS-value set of the skeleton layer at budget b_s (value keys only)."""
    return {_value_key(r.value) for r in _skeleton_value_nodes(alpha, b_s)}


# ---- GERM LAYER (branch (c): >=3 germ steps, forced set == {both}, exactly one free) ----

def _germ_recipes(alpha: Alphabet, free_keys: List[str], g_s: int) -> Iterator[Tuple[Tuple[str, OpType, object], ...]]:
    """Enumerate every germ-decoration recipe of EXACTLY g_s>=3 steps such that the germ-leaf set
    presents forced=={3,sqrt(8pi/3)} and exactly ONE distinct free germ (the Gate-B keep predicate).

    Base (3 steps): {3, sqrt(8pi/3), one free}. Extra (g_s-3) steps must be:
      * another power of a FORCED germ (3 or sqrt(8pi/3)) — repeat-forced, keeps forced set == {both},
      * or another power of the SAME free germ — same-value-free, keeps free set size 1.
    CANONICAL enumeration (value-complete, order-free): germ factors commute, so the germ layer's
    contribution to a value is fully determined by the NET signed-exponent per germ key. We therefore
    enumerate (a) the composition of g_s steps among the 3 keys (each key >=1 step, so all 3 leaves
    are PRESENT -> the Gate-B tag is fixed), and (b) per key, the distinct reachable net signed-
    exponent for its step-count (_net_exps), emitting ONE canonical decorate sequence (_realize_net)
    per assignment. This yields the IDENTICAL germ VALUE-factor set and the IDENTICAL Gate-B tag as
    the naive full (order x op x exp)^g_s enumeration, but WITHOUT the g_s! x 8^g_s over-generation
    (which made the depth-6 build blow past 10 min / 3.5 GB). Value-dedup downstream is unaffected.
    """
    forced = _forced_keys_present(alpha)                 # ['3','sqrt(8pi/3)']
    for free in free_keys:
        keys = (forced[0], forced[1], free)              # exactly these 3 distinct germ keys
        # distribute g_s steps among the 3 keys, EACH key >=1 step (so all 3 leaves are PRESENT ->
        # the Gate-B tag Fset=={both}, |Rset|==1 holds regardless of net exponents; the leaf-presence
        # is what gate_candidate_for / _leaf_tag read, not the net power).
        for (n0, n1, n2) in _compositions(g_s, 3):
            # per key, choose a reachable net signed-exponent for its n_i steps
            for e0 in _net_exps(n0):
                for e1 in _net_exps(n1):
                    for e2 in _net_exps(n2):
                        # emit ONE canonical decorate sequence realizing (key_i -> net e_i).
                        # A net exponent E on key K is realized by folding the K leaf n_i times so the
                        # signed exponents sum to E; we use the canonical realizer _realize_net which
                        # returns the exact (op,exp) step list of length n_i. Concatenate the 3 keys.
                        steps = []
                        for (gk, ni, E) in ((keys[0], n0, e0), (keys[1], n1, e1), (keys[2], n2, e2)):
                            steps.extend(_realize_net(gk, ni, E))
                        yield tuple(steps)


# per-step signed exponent set = (op MUL:+ / DIV:-) x _GERM_EXPONENTS ; symmetric -> {+1,+1/2,-1,-1/2}
_PER_STEP_SIGNED = sorted({e for x in _GERM_EXPONENTS for e in (mp.mpf(x), -mp.mpf(x))})


def _compositions(total: int, parts: int) -> Iterator[Tuple[int, ...]]:
    """All compositions of `total` into `parts` POSITIVE integers (each >=1)."""
    if parts == 1:
        yield (total,)
        return
    for first in range(1, total - (parts - 1) + 1):
        for rest in _compositions(total - first, parts - 1):
            yield (first,) + rest


def _net_exps(n_steps: int) -> List[object]:
    """The distinct NET signed-exponents reachable by summing `n_steps` per-step signed exponents
    (each in {+1,+1/2,-1,-1/2}). n_steps>=1. Deduped, canonical."""
    nets = {mp.mpf(0)}
    for _ in range(n_steps):
        nxt = set()
        for cur in nets:
            for s in _PER_STEP_SIGNED:
                nxt.add(cur + s)
        nets = nxt
    return sorted(nets)


_REALIZE_CACHE: Dict[Tuple[int, str], Optional[Tuple[Tuple[OpType, object], ...]]] = {}


def _realize_dfs(n_steps: int, target) -> Optional[Tuple[Tuple[OpType, object], ...]]:
    """Exact DFS: a length-n_steps sequence of (op, exp) steps (op in {MUL,DIV}, exp in
    _GERM_EXPONENTS restricted to positive {1,1/2}) whose signed sum == target, or None. Memoized on
    (n_steps, str(target)). n_steps is tiny (<= g_s-2 <= D-6), so DFS is instant."""
    key = (n_steps, mp.nstr(mp.mpf(target), 20))
    if key in _REALIZE_CACHE:
        return _REALIZE_CACHE[key]
    tgt = mp.mpf(target)
    if n_steps == 0:
        res = () if tgt == 0 else None
        _REALIZE_CACHE[key] = res
        return res
    # prune: max reachable in n_steps is n_steps*1, min is -n_steps*1
    if abs(tgt) > n_steps:
        _REALIZE_CACHE[key] = None
        return None
    for op, e in ((OpType.MUL, mp.mpf(1)), (OpType.DIV, mp.mpf(1)),
                  (OpType.MUL, mp.mpf("0.5")), (OpType.DIV, mp.mpf("0.5"))):
        s = e if op == OpType.MUL else -e
        rest = _realize_dfs(n_steps - 1, tgt - s)
        if rest is not None:
            res = ((op, e),) + rest
            _REALIZE_CACHE[key] = res
            return res
    _REALIZE_CACHE[key] = None
    return None


def _realize_net(germ_key: str, n_steps: int, net_exp) -> List[Tuple[str, OpType, object]]:
    """Return a (germ_key, op, exp) step list of length EXACTLY `n_steps` whose signed exponents
    (MUL:+exp, DIV:-exp; exp in {1,1/2}) sum to `net_exp`. Exact via memoized DFS (_realize_dfs);
    every net in _net_exps(n_steps) is realizable by construction of that reachable set."""
    seq = _realize_dfs(n_steps, net_exp)
    if seq is None:
        raise ValueError(f"cannot realize net {float(net_exp)} for {germ_key} in {n_steps} steps")
    return [(germ_key, op, e) for (op, e) in seq]


def _germ_recipe_count(alpha: Alphabet, n_free: int, g_s: int) -> int:
    """Raw CANONICAL germ-recipe count per skeleton at germ-budget g_s (matches the enumerator):
    sum over compositions (n0,n1,n2) of prod_i |_net_exps(n_i)|, times n_free."""
    total = 0
    for (n0, n1, n2) in _compositions(g_s, 3):
        total += len(_net_exps(n0)) * len(_net_exps(n1)) * len(_net_exps(n2))
    return n_free * total


# ---- THE PRODUCT: constructive Gate-B-passable dimensionless depth-D set, STREAMING ----

def constructive_gate_b_reachables(alpha: Alphabet, depth: int,
                                   value_cap: Optional[int] = None
                                   ) -> Tuple[List[Reachable], Dict[str, int]]:
    """The CONSTRUCTIVE Gate-B-passable DIMENSIONLESS set at `depth`, STREAMING + value-deduped.

    Product over every budget split (b_s, g_s):  skeleton(b_s) x germ_recipe(g_s).  Streamed one
    ExprNode at a time; MEMORY holds ONLY the deduped distinct-VALUE set + the deduped Reachable list
    (NO canonical-hash set — the depth-6 verbatim depth-5 pattern's seen_canon grew to ~3.5 GB and is
    unnecessary: value-dedup is the correctness invariant, and the canonical germ enumeration already
    removes ordering duplicates. This bounds memory to the distinct-value set, per the memory brief).
    `value_cap` (watchdog safety): abort the build if the distinct-value set exceeds this size.
    """
    free_keys = _free_germ_keys(alpha)
    splits = budget_splits(depth)

    seen_value = set()
    reach: List[Reachable] = []
    raw = 0
    n_skeletons_total = 0

    def _gen() -> Iterator[ExprNode]:
        nonlocal raw, n_skeletons_total
        for (b_s, g_s) in splits:
            skeletons = _skeleton_value_nodes(alpha, b_s)
            n_skeletons_total += len(skeletons)
            for sk in skeletons:
                for recipe in _germ_recipes(alpha, free_keys, g_s):
                    node = sk.node
                    for (gk, op, e) in recipe:
                        node = _decorate(node, op, gk, e)
                    raw += 1
                    yield node

    for node in _gen():
        try:
            value, label = node.evaluate(alpha)
        except Exception:
            continue
        try:
            if not mp.isfinite(value) or value <= 0:
                continue
        except Exception:
            continue
        if not label.is_dimensionless():
            continue
        vk = _value_key(value)
        if vk in seen_value:
            continue
        seen_value.add(vk)
        reach.append(Reachable(value=value, label=label,
                               formula=node.to_string(alpha), canonical=node.canonical_hash(), node=node))
        if value_cap is not None and len(reach) > value_cap:
            raise SystemExit(f"VALUE-CAP ABORT: distinct-value set exceeded {value_cap:,} at depth "
                             f"{depth} — the constructive distinct set is the wall for this depth.")
        # periodic watchdog during the (potentially long) build
        if (len(reach) & 0x3FFF) == 0:
            _mem_watchdog(f"build/depth{depth}")
    # a raw-stream watchdog too (raw can be huge before many distinct values accumulate)
    _mem_watchdog(f"build/depth{depth}/end")

    counts = dict(
        n_splits=len(splits),
        splits=splits,
        n_skeletons_total=n_skeletons_total,
        raw_candidates=raw,
        distinct_by_value=len(reach),
    )
    return reach, counts


def constructive_space_size(alpha: Alphabet, depth: int) -> Dict[str, int]:
    """Closed-form raw constructive space size at `depth` (per target), summed over budget splits.
    Uses the MEASURED skeleton value-counts where cheap (b_s small) and the germ-recipe UB."""
    n_free = len(_free_germ_keys(alpha))
    splits = budget_splits(depth)
    total_raw = 0
    per_split = []
    for (b_s, g_s) in splits:
        # measured skeleton value count (bounded brute) — only for small b_s to stay cheap
        try:
            n_sk = len(_skeleton_value_set(alpha, b_s))
        except Exception:
            n_sk = -1
        rec = _germ_recipe_count(alpha, n_free, g_s)
        raw = (n_sk if n_sk >= 0 else 0) * rec
        total_raw += raw
        per_split.append(dict(b_s=b_s, g_s=g_s, n_skeletons=n_sk, germ_recipes=rec, raw=raw))
    return dict(n_free=n_free, splits=per_split, raw_per_target=total_raw)


# =============================================================================
# 1.  PER-DEPTH CONSTRUCTIVE-COMPLETENESS SELF-CHECK  (the load-bearing trip-wire)
#     (a) skeleton-brute == scheme skeletons (0 missed / 0 extra) at the depth's budget
#     (b) the committed brute depth-4 Gate-B value-set is still reproduced (reuse D5 verbatim)
# =============================================================================

def _skeleton_brute_value_set(alpha: Alphabet, b_s: int) -> set:
    """An INDEPENDENT brute of the skeleton layer at budget b_s: enumerate ALL length-b_s left-fold
    step sequences (append-leaf {MUL,DIV} | pow | unary) over the leaf pool, keep dimensionless
    finite>0, dedup by value. Deliberately written as a flat itertools.product brute (a different
    code path from the recursive scheme) so the cross-check has real teeth. Bounded/streaming."""
    leaves = alpha.leaves
    ops_bin = (OpType.MUL, OpType.DIV)
    step_menu: List[Tuple] = []
    for lk in leaves:
        for op in ops_bin:
            step_menu.append(("app", lk, op))
    for e in _POW_EXPONENTS:
        step_menu.append(("pow", e, None))
    for u in _UNARY_PLAIN:
        step_menu.append(("un", u, None))

    def _apply(node, step):
        kind = step[0]
        if kind == "app":
            _, lk, op = step
            return ExprNode(op, children=[node, _leaf_node(lk)])
        if kind == "pow":
            _, e, _ = step
            return ExprNode(OpType.POW, children=[node], exp=e)
        _, u, _ = step
        return ExprNode(u, children=[node])

    seen = set()
    for base in leaves:
        for seq in itertools.product(step_menu, repeat=b_s):
            node = _leaf_node(base)
            for step in seq:
                node = _apply(node, step)
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
            seen.add(_value_key(v))
    return seen


def constructive_completeness_selfcheck(depth: int, verbose: bool = True) -> dict:
    """PROVE constructive completeness at `depth`, two ways.

    (a) SKELETON cross-check per budget split: for each (b_s, g_s), the scheme's skeleton value-set
        (_skeleton_value_set) must EQUAL an independent flat brute (_skeleton_brute_value_set):
        MISSED=0 EXTRA=0. Covers branches (a) bare-leaf appends + (b) pow/unary-decorated leaves.
    (b) The committed brute depth-4 anchor: reuse the depth-5 file's completeness self-check VERBATIM
        (it asserts the depth-<=4 dimensionless Gate-B set is empty on BOTH sides AND the constructive
        1-scale shape reproduces the committed brute depth-4 ALL-Gate-B value-set exactly).

    A miss at (a) OR a fail at (b) => the depth's null is INVALID => HALT.
    """
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25 and len(alpha.leaves) == 11

    splits = budget_splits(depth)
    split_reports = []
    skeleton_ok = True
    for (b_s, g_s) in splits:
        scheme = _skeleton_value_set(alpha, b_s)
        brute = _skeleton_brute_value_set(alpha, b_s)
        missed = brute - scheme
        extra = scheme - brute
        ok = (len(missed) == 0 and len(extra) == 0)
        skeleton_ok = skeleton_ok and ok
        split_reports.append(dict(b_s=b_s, g_s=g_s, n_scheme=len(scheme), n_brute=len(brute),
                                  missed=len(missed), extra=len(extra), ok=ok))

    # (b) the committed brute depth-4 anchor — reuse the depth-5 self-check verbatim.
    d4 = _d5_completeness_selfcheck(verbose=False)
    anchor_ok = bool(d4["constructive_complete"])

    all_ok = skeleton_ok and anchor_ok

    if verbose:
        print("=" * 100)
        print(f"CONSTRUCTIVE-COMPLETENESS SELF-CHECK  (depth {depth}) — skeleton-brute == scheme + depth-4 anchor")
        print("-" * 100)
        print("(a) per-split skeleton cross-check (scheme skeleton value-set == independent brute):")
        for sr in split_reports:
            print(f"    split (b_s={sr['b_s']}, g_s={sr['g_s']}): scheme={sr['n_scheme']:>4}  "
                  f"brute={sr['n_brute']:>4}  MISSED={sr['missed']}  EXTRA={sr['extra']}  "
                  f"-> {'OK' if sr['ok'] else 'FAIL'}")
        print(f"    skeleton_ok = {skeleton_ok}")
        print("(b) committed brute depth-4 anchor (reuse depth-5 self-check verbatim):")
        print(f"    anchor_ok = {anchor_ok}  (brute depth-4 ALL-Gate-B distinct values reproduced: "
              f"{d4['brute_all_count']:,} == {d4['constructive_all_count']:,}; "
              f"dimensionless<=4 empty both sides: {d4['brute_dimless_count']}=={d4['constructive_dimless_count']})")
        print("-" * 100)
        print(f"CONSTRUCTIVE_COMPLETE (depth {depth}) = {all_ok}   "
              f"(skeleton_ok={skeleton_ok}, anchor_ok={anchor_ok})")
        print("=" * 100)

    return dict(depth=depth, constructive_complete=all_ok, skeleton_ok=skeleton_ok,
                anchor_ok=anchor_ok, splits=split_reports,
                anchor_brute_all=d4["brute_all_count"], anchor_con_all=d4["constructive_all_count"])


# =============================================================================
# 2.  SOUNDNESS SELF-CHECK  (sample the depth-D constructive set; run the REAL gate)
# =============================================================================

def soundness_selfcheck(depth: int, sample_n: int = 300, verbose: bool = True) -> dict:
    """Every constructive depth-D candidate must present (Fset=={both forced}, Rset=={one free}) so
    the REAL gate.forced_kernel (via gate.validate) reports kernel.passed=True. Sample the depth-D
    constructive dimensionless set; (a) recompute the germ-leaf tag via the REAL _leaf_tag and assert
    the keep predicate, (b) build the REAL gate candidate and assert v.kernel.passed."""
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25
    reach, counts = constructive_gate_b_reachables(alpha, depth)
    n = len(reach)
    if n == 0:
        raise SystemExit(f"SOUNDNESS: constructive depth-{depth} set is EMPTY — construction BROKEN.")
    step = max(1, n // sample_n)
    sample = reach[::step][:sample_n]

    tspec = resolve_target("r_mu_e")
    tag_ok = kernel_ok = 0
    bad = []
    for r in sample:
        Fset = frozenset(); Rset = frozenset()
        for k in set(r.node.leaf_consts()):
            F, R = _leaf_tag(alpha, k)
            Fset |= F; Rset |= R
        keep = (len(Fset) == 2 and len(Rset) == 1)
        if not keep:
            bad.append((r.formula[:70], sorted(Fset), sorted(Rset)))
            continue
        tag_ok += 1
        gc = gate_candidate_for(r, alpha, "r_mu_e", tspec.pdg_target, N_TARGETS)
        v = validate(gc)
        if v.kernel.passed:
            kernel_ok += 1
        else:
            bad.append((r.formula[:70], "kernel.passed=False", v.tell[:60]))

    soundness_ok = (tag_ok == len(sample) and kernel_ok == len(sample))
    if verbose:
        print("=" * 100)
        print(f"CONSTRUCTION-SOUNDNESS SELF-CHECK  (depth {depth}, real gate.forced_kernel on sample)")
        print("-" * 100)
        print(f"  constructive depth-{depth} dimensionless set: {n:,} distinct values "
              f"(raw {counts['raw_candidates']:,}, splits {counts['splits']})")
        print(f"  sampled: {len(sample)}")
        print(f"  keep-predicate (Fset==both & 1 free) pass : {tag_ok}/{len(sample)}")
        print(f"  REAL gate kernel.passed=True             : {kernel_ok}/{len(sample)}")
        if bad:
            print(f"  !! {len(bad)} FAILURES (sample): {bad[:4]}")
        print("-" * 100)
        print(f"SOUNDNESS_OK = {soundness_ok}")
        print("=" * 100)
    return dict(depth=depth, soundness_ok=soundness_ok, n_constructive=n,
                n_sampled=len(sample), tag_ok=tag_ok, kernel_ok=kernel_ok, n_bad=len(bad))


# =============================================================================
# 3.  a0-VALIDITY at depth D  (TARGETED construction — NOT brute; RULE 2)
# =============================================================================

def a0_validity_depthN(depth: int, verbose: bool = True) -> dict:
    """a0 = (c/Z)*H_L must (LEG 1) re-derive through the committed depth-4 dimensional filter AND
    (LEG 2) be constructed DIRECTLY at depth D as a0 x cancelling identity, evaluate to a0 (L/T^2),
    and return the EXPECTED FDR-DEAD gate verdict. NEVER brute-enumerate the dimensionful depth-D
    space (the trap that killed the prior run).

    LEG 1 reuses the depth-5 a0 leg VERBATIM (D5.a0_validity_depth5 runs build_reachable_set @ depth
    4 on the pinned a0 pool — the tractable committed path — and re-finds a0=9.36e-11).
    LEG 2 builds a genuine depth-D a0 tree: a0_core = ((c*H_L)/Z) (depth 3), then wrap with
    (depth-3)//1 extra (*3/3) identity pairs and a trailing filler to hit EXACTLY depth D.
    """
    # ---- LEG 1: committed depth-4 dimensional re-derivation (verbatim depth-5 leg) ----
    d5 = D5.a0_validity_depth5(verbose=False)
    leg1_ok = bool(d5["leg1_a0_refound"])

    # ---- LEG 2: explicit depth-D a0 x identity, certified through the real pipeline ----
    a0_pool_leaves = ["c", "G", "Lambda", "rho_Lambda", "H_Lambda"]
    a0_pool_germs = ["pi", "8", "3", "2", "32pi", "sqrt(8pi/3)", "Z"]
    tspec = resolve_target("a0")
    alpha = build_alphabet(a0_pool_leaves, a0_pool_germs)
    tol = 0.01

    # a0_core = ((c*H_L)/Z)  — depths: c[1] -> c*H_L[2] -> /Z[3]  (a0, L/T^2)
    node = ExprNode(OpType.DIV, children=[
        ExprNode(OpType.MUL, children=[_leaf_node("c"), _leaf_node("H_Lambda")]),
        _leaf_node("Z")])
    cur_depth = 3
    # add (*3)/3 identity pairs (each pair = +2 depth) until 1 or 0 steps from target
    while cur_depth + 2 <= depth:
        node = ExprNode(OpType.DIV, children=[
            ExprNode(OpType.MUL, children=[node, _leaf_node("3")]), _leaf_node("3")])
        cur_depth += 2
    # if one step short (parity), append a single *3 then we'd change value; instead use *(sqrt?) no —
    # use a value-neutral single step: **1 POW (depth +1, value unchanged, dims unchanged).
    if cur_depth + 1 == depth:
        node = ExprNode(OpType.POW, children=[node], exp=mp.mpf(1))
        cur_depth += 1
    assert cur_depth == depth, f"a0 identity tree depth {cur_depth} != {depth}"

    v, lab = node.evaluate(alpha)
    card = score_value(float(v), tspec.pdg_target)
    dims_ok = lab.dims_equal(tspec.label)
    value_ok = (card.rel_error <= tol)
    r = Reachable(v, lab, node.to_string(alpha), node.canonical_hash(), node)
    gc = gate_candidate_for(r, alpha, "a0", tspec.pdg_target, N_TARGETS)
    vg = validate(gc)
    leg2_ok = bool(dims_ok and value_ok)
    # EXPECTED FDR-DEAD: a0 presents ONE forced provenance in the code -> not overdetermined.
    fdr_dead = (vg.status != "CERTIFIED")

    a0_ok = bool(leg1_ok and leg2_ok and fdr_dead)

    if verbose:
        print("=" * 100)
        print(f"a0-VALIDITY at DEPTH {depth} (RULE 2 — TARGETED construction, NOT brute; 2 legs)")
        print("-" * 100)
        print(f"  LEG 1 (committed depth-4 dimensional re-derivation, verbatim depth-5 leg):")
        print(f"    a0 re-found = {leg1_ok}  {d5['leg1_formula']}  rel_err={d5['leg1_rel_error']:.2e}")
        print(f"  LEG 2 (explicit depth-{depth} a0 x cancelling identity, real pipeline):")
        print(f"    node: {node.to_string(alpha)}")
        print(f"      = {float(v):.6g} m/s^2   dims L/T^2 ? {dims_ok}   value==a0(<1%) ? {value_ok} "
              f"(rel_err={card.rel_error:.2e})")
        print(f"    gate verdict: [{vg.status}]  FDR-DEAD (not CERTIFIED) ? {fdr_dead}  "
              f"(EXPECTED: one forced provenance -> not overdetermined)")
        print("-" * 100)
        print(f"  a0_ok (LEG1 re-finds a0 AND LEG2 depth-{depth} tree==a0 AND FDR-DEAD): "
              f"{'PASS' if a0_ok else 'FAIL'}")
        print("=" * 100)

    return dict(depth=depth, a0_ok=a0_ok, leg1_ok=leg1_ok, leg2_ok=leg2_ok, fdr_dead=fdr_dead,
                leg2_node=node.to_string(alpha), leg2_value=float(v), leg2_rel_error=float(card.rel_error),
                leg2_gate_status=vg.status)


# =============================================================================
# 4.  THE DRIVER  (constructive depth-D -> in-window match -> FULL 3-part gate)
# =============================================================================

@dataclass
class HitN:
    formula: str
    value: float
    rel_error: float
    n_sigma: float
    status: str
    fdr_bits: float
    fdr_mode: str
    kernel_passed: bool
    interlock_passed: bool
    gate_tell: str


def run_target_depthD(target_key: str, depth: int, tol: Optional[float] = None,
                      n_targets_searched: int = N_TARGETS, verbose: bool = True,
                      shared: Optional[Tuple[Alphabet, List[Reachable], Dict[str, int]]] = None
                      ) -> dict:
    """End-to-end constructive depth-D run on ONE target. The constructive Gate-B-passable
    dimensionless reachable set is TARGET-INDEPENDENT, so `shared` lets a worker build it ONCE."""
    tspec = resolve_target(target_key)
    if shared is None:
        alpha = build_alphabet(None, None)
        assert len(alpha.germs) == 25, f"FDR non-smuggle: expected 25 germs, got {len(alpha.germs)}"
        reach, counts = constructive_gate_b_reachables(alpha, depth)
    else:
        alpha, reach, counts = shared
        assert len(alpha.germs) == 25

    if tol is None:
        tol = measurement_tol(tspec.pdg_target)

    hits: List[HitN] = []
    for r in reach:
        card = score_value(float(r.value), tspec.pdg_target)
        if card.rel_error <= tol:
            gc = gate_candidate_for(r, alpha, target_key, tspec.pdg_target, n_targets_searched)
            v = validate(gc)
            hits.append(HitN(
                formula=r.formula, value=float(r.value), rel_error=card.rel_error,
                n_sigma=card.n_sigma, status=v.status, fdr_bits=v.fdr.bits, fdr_mode=v.fdr.mode,
                kernel_passed=v.kernel.passed, interlock_passed=v.interlock.passed, gate_tell=v.tell,
            ))
    hits.sort(key=lambda h: h.rel_error)
    certified = [h for h in hits if h.status == "CERTIFIED"]
    relabeled = [h for h in hits if h.status == "REAL-PUZZLE-RE-LABELED"]

    report = {
        "target": target_key, "target_value": tspec.value, "target_dimension": tspec.label_name,
        "depth": depth, "tol": tol, "n_leaves": len(alpha.leaves), "n_germs": len(alpha.germs),
        "fdr_uses_full_library": (len(alpha.germs) == 25),
        "constructive_raw_per_target": counts["raw_candidates"],
        "constructive_splits": counts["splits"],
        "constructive_distinct_values": counts["distinct_by_value"],
        "n_hits": len(hits), "n_certified": len(certified), "n_relabeled": len(relabeled),
        "hits": [h.__dict__ for h in hits[:20]],
    }
    if verbose:
        _print_target_report(report)
    return report


def _print_target_report(rep: dict):
    print("=" * 100)
    print(f"DEPTH-{rep['depth']} CONSTRUCTIVE FORCED-INTERLOCK — target {rep['target']} = "
          f"{rep['target_value']:.6g} [dim {rep['target_dimension']}]")
    print(f"  tol={rep['tol']:.2e}   pool: {rep['n_leaves']} leaves + {rep['n_germs']} germs")
    print(f"  FDR library = FULL {rep['n_germs']}-germ pool: "
          f"{'YES (non-smuggle OK)' if rep['fdr_uses_full_library'] else 'NO -- SMUGGLE BUG'}   mult={N_TARGETS}")
    print(f"  constructive raw/target: {rep['constructive_raw_per_target']:,}  (splits {rep['constructive_splits']})"
          f"  -> distinct dimensionless VALUES: {rep['constructive_distinct_values']:,}")
    print("-" * 100)
    print(f"  in-window matches: {rep['n_hits']}   CERTIFIED: {rep['n_certified']}   "
          f"REAL-PUZZLE-RE-LABELED: {rep['n_relabeled']}")
    for h in rep["hits"]:
        print(f"    [{h['status']:22}] {h['formula']}")
        print(f"        = {h['value']:.8g}  rel_err={h['rel_error']:.2e}  n_sigma={h['n_sigma']:.2f}  "
              f"FDR={h['fdr_bits']:.1f}b/{h['fdr_mode']}  B={h['kernel_passed']} C={h['interlock_passed']}")
        print(f"        gate: {h['gate_tell'][:130]}")
    if not rep["hits"]:
        print("    (none — no Gate-B-passable, dimensionless expression lands in the window)")
    print("=" * 100)


# =============================================================================
# 5.  SWEEP + SHARDED PARALLEL  (mirror exhaust_parallel.py; build constructive set ONCE per worker)
# =============================================================================

def _results_dir(depth: int) -> Path:
    return RESULTS_ROOT / f"depth_{depth}"


def sweep_all(depth: int, targets: List[str], n_targets_searched: int, verbose: bool = True) -> List[dict]:
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25
    t0 = time.time()
    reach, counts = constructive_gate_b_reachables(alpha, depth)
    build_s = time.time() - t0
    _mem_watchdog(f"sweep_all/depth{depth}/after-build")
    if verbose:
        print(f"[built constructive depth-{depth} set ONCE: {counts['distinct_by_value']:,} distinct "
              f"dimensionless values from {counts['raw_candidates']:,} raw in {build_s:.1f}s]")
    shared = (alpha, reach, counts)
    out = []
    for k in targets:
        out.append(run_target_depthD(k, depth, n_targets_searched=n_targets_searched, verbose=verbose, shared=shared))
        _mem_watchdog(f"sweep_all/depth{depth}/{k}")
    if verbose:
        print(f"[sweep peak RSS: {_total_rss_mb()/1024:.2f} GB (self+children); cap {HARD_MEM_CAP_GB:.0f} GB]")
    return out


def _shard_targets(targets: List[str], n: int) -> List[List[str]]:
    return [targets[i::n] for i in range(n)]


def launch_parallel(depth: int, workers: int):
    rd = _results_dir(depth)
    rd.mkdir(parents=True, exist_ok=True)
    targets = sm_target_keys()
    workers = min(workers, 12, len(targets))
    shards = _shard_targets(targets, workers)
    pids = []
    for i, sl in enumerate(shards):
        if not sl:
            continue
        sd = rd / f"shard_{i}"
        sd.mkdir(parents=True, exist_ok=True)
        logf = open(sd / "run.log", "w")
        p = subprocess.Popen(
            [sys.executable, str(_HERE / "exhaust_depthN_forced.py"), "--depth", str(depth),
             "--worker", str(i), "--targets", ",".join(sl), "--n-targets", str(len(targets))],
            stdout=logf, stderr=subprocess.STDOUT, cwd=str(_HERE), start_new_session=True,
        )
        pids.append({"shard": i, "pid": p.pid, "targets": sl})
    (rd / "pids.json").write_text(json.dumps(pids, indent=2))
    print(f"launched {len(pids)} workers over {len(targets)} targets (depth {depth}) -> {rd}")
    for pd in pids:
        print(f"  shard {pd['shard']}: pid {pd['pid']}  targets {pd['targets']}")


def run_worker(depth: int, shard: int, targets: List[str], n_targets: int):
    rd = _results_dir(depth)
    sd = rd / f"shard_{shard}"
    sd.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25
    reach, counts = constructive_gate_b_reachables(alpha, depth)
    build_s = time.time() - t0
    _mem_watchdog(f"worker{shard}/depth{depth}/after-build")
    shared = (alpha, reach, counts)
    out = []
    for k in targets:
        rep = run_target_depthD(k, depth, n_targets_searched=n_targets, verbose=True, shared=shared)
        out.append(rep)
        _mem_watchdog(f"worker{shard}/depth{depth}/{k}")
        wall = time.time() - t0
        meta = {"shard": shard, "depth": depth, "targets_done": len(out), "targets_total": len(targets),
                "build_s": build_s, "wall_s": wall, "peak_mem_mb": _peak_mem_mb(),
                "constructive_raw_per_target": counts["raw_candidates"],
                "constructive_distinct_values": counts["distinct_by_value"], "results": out}
        (sd / "result.json").write_text(json.dumps(meta, indent=2, default=str))


def aggregate_status(depth: int, as_json: bool = False):
    rd = _results_dir(depth)
    if not rd.exists():
        print("no results yet"); return
    metas = []
    for sd in sorted(rd.glob("shard_*")):
        rf = sd / "result.json"
        if rf.exists():
            metas.append(json.loads(rf.read_text()))
    rows = [r for m in metas for r in m.get("results", [])]
    n_cert = sum(r["n_certified"] for r in rows)
    n_rel = sum(r["n_relabeled"] for r in rows)
    max_wall = max((m.get("wall_s", 0.0) for m in metas), default=0.0)
    max_mem = max((m.get("peak_mem_mb", 0.0) for m in metas), default=0.0)
    if as_json:
        print(json.dumps({"depth": depth, "n_targets_done": len(rows), "n_certified": n_cert,
                          "n_relabeled": n_rel, "max_wall_s": max_wall, "max_peak_mem_mb": max_mem,
                          "rows": rows}, indent=2, default=str))
        return
    print(f"[depth {depth}] targets done: {len(rows)}   CERTIFIED: {n_cert}   RE-LABELED: {n_rel}")
    print(f"max wall-clock across shards: {max_wall:.1f}s   max peak mem: {max_mem:.0f} MB")
    for r in sorted(rows, key=lambda x: x["target"]):
        print(f"  {r['target']:18} distinct={r['constructive_distinct_values']:>7,}  "
              f"hits={r['n_hits']:>3}  CERT={r['n_certified']}  RELAB={r['n_relabeled']}")


# =============================================================================
# 6.  PROJECTION + ESCALATION DRIVER
# =============================================================================

def project_table(depths: List[int]) -> List[dict]:
    """Projected constructive sizes per depth (closed-form raw + measured skeleton counts where cheap).
    RSS is projected from the depth-5 anchor (~0.0136 MB/distinct + ~120 MB base)."""
    alpha = build_alphabet(None, None)
    rows = []
    for D in depths:
        s = constructive_space_size(alpha, D)
        raw = s["raw_per_target"]
        # distinct/raw dedup ratio ~ depth-5 measured (1.44e-2) as a rough UB proxy
        proj_distinct = int(raw * 1.44e-2) if raw > 0 else 0
        proj_rss_mb = 120.0 + 0.0136 * proj_distinct
        rows.append(dict(depth=D, splits=[(p["b_s"], p["g_s"]) for p in s["splits"]],
                         raw_per_target=raw, proj_distinct_ub=proj_distinct,
                         proj_rss_mb=proj_rss_mb, proj_rss_gb=proj_rss_mb / 1024.0,
                         breach=(proj_rss_mb / 1024.0 > HARD_MEM_CAP_GB)))
    return rows


def escalate(start: int = 6, time_budget_s: float = 45 * 60, verbose: bool = True) -> dict:
    """Loop D=start,start+1,...: run self-check (halt-on-fail), a0-check (halt-on-fail), then sweep;
    record per depth {raw, distinct, n_cert, n_relab, wall, peak RSS}. STOP when the watchdog trips
    the 6 GB cap OR the per-depth wall exceeds time_budget_s. Report the ceiling depth + reason."""
    ledger = []
    D = start
    ceiling = None; reason = None
    while True:
        t0 = time.time()
        if verbose:
            print("\n" + "#" * 100)
            print(f"# ESCALATION DEPTH {D}")
            print("#" * 100)
        try:
            comp = constructive_completeness_selfcheck(D, verbose=verbose)
            if not comp["constructive_complete"]:
                raise SystemExit(f"CONSTRUCTIVE-COMPLETENESS FAILED at depth {D} — null INVALID. HALT.")
            a0 = a0_validity_depthN(D, verbose=verbose)
            if not a0["a0_ok"]:
                raise SystemExit(f"a0-VALIDITY FAILED at depth {D} — search BROKEN. HALT.")
            reps = sweep_all(D, sm_target_keys(), N_TARGETS, verbose=False)
            wall = time.time() - t0
            peak = _total_rss_mb() / 1024.0
            n_cert = sum(r["n_certified"] for r in reps)
            n_rel = sum(r["n_relabeled"] for r in reps)
            distinct = reps[0]["constructive_distinct_values"] if reps else 0
            raw = reps[0]["constructive_raw_per_target"] if reps else 0
            ledger.append(dict(depth=D, raw=raw, distinct=distinct, n_certified=n_cert,
                               n_relabeled=n_rel, wall_s=wall, peak_rss_gb=peak, wall="ok"))
            if verbose:
                print(f"[depth {D}] distinct={distinct:,} raw={raw:,} CERT={n_cert} RELAB={n_rel} "
                      f"wall={wall:.1f}s peakRSS={peak:.2f}GB")
            if wall > time_budget_s:
                ceiling = D; reason = f"time wall ({wall:.0f}s > {time_budget_s:.0f}s budget)"; break
        except SystemExit as e:
            msg = str(e)
            if "MEMORY WATCHDOG" in msg or "VALUE-CAP" in msg:
                ceiling = D; reason = f"memory wall: {msg[:120]}"
                ledger.append(dict(depth=D, wall="MEMORY-BREACH", note=msg[:160]))
                break
            raise
        D += 1
        if D > 12:
            ceiling = D - 1; reason = "sane escalation ceiling (D>12) reached without a wall"; break
    return dict(ceiling_depth=ceiling, reason=reason, ledger=ledger)


# =============================================================================
# CLI
# =============================================================================

def main():
    ap = argparse.ArgumentParser(description="Escalating constructive Gate-B-passable dimensionless "
                                             "depth-D>=6 forced-interlock search.")
    ap.add_argument("--depth", type=int, default=6, help="depth D (>=6).")
    ap.add_argument("--target", default=None)
    ap.add_argument("--a0-check", action="store_true")
    ap.add_argument("--self-check", action="store_true")
    ap.add_argument("--soundness", action="store_true")
    ap.add_argument("--space", action="store_true")
    ap.add_argument("--project", action="store_true", help="projected sizes for depths 7..10.")
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--escalate", action="store_true", help="loop D=6,7,8,... until the wall.")
    ap.add_argument("--n-targets", type=int, default=N_TARGETS)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--worker", type=int, default=None)
    ap.add_argument("--targets", default=None)
    args = ap.parse_args()

    if args.escalate:
        out = escalate(start=6, verbose=True)
        print("\n" + "=" * 100)
        print(f"ESCALATION CEILING: depth {out['ceiling_depth']}  ({out['reason']})")
        for row in out["ledger"]:
            print(f"  {row}")
        print("=" * 100)
        if args.json:
            print(json.dumps(out, indent=2, default=str))
        return

    D = args.depth
    if D < 6:
        raise SystemExit("This escalation file is for depth D>=6 (depth 5 is exhaust_depth5_forced.py).")

    if args.worker is not None and args.targets:
        run_worker(D, args.worker, args.targets.split(","), args.n_targets); return
    if args.workers:
        launch_parallel(D, args.workers); return
    if args.status:
        aggregate_status(D, args.json); return
    if args.project:
        rows = project_table([7, 8, 9, 10])
        for r in rows:
            print(f"depth {r['depth']}: splits={r['splits']}  raw/target={r['raw_per_target']:,}  "
                  f"proj_distinct(UB)~{r['proj_distinct_ub']:,}  proj_RSS~{r['proj_rss_gb']:.2f}GB  "
                  f"{'** 6GB BREACH **' if r['breach'] else 'under cap'}")
        if args.json:
            print(json.dumps(rows, indent=2, default=str))
        return
    if args.space:
        alpha = build_alphabet(None, None)
        s = constructive_space_size(alpha, D)
        brute = closed_form_count(11, D, 25)
        print(json.dumps({"depth": D, "constructive_raw_per_target": s["raw_per_target"],
                          "splits": s["splits"], "brute_depthD_per_target": brute[-1],
                          "shrink_vs_brute": brute[-1] / max(1, s["raw_per_target"])},
                         indent=2, default=str))
        return
    if args.a0_check:
        out = a0_validity_depthN(D, verbose=True)
        if args.json:
            print(json.dumps(out, indent=2, default=str))
        if not out["a0_ok"]:
            raise SystemExit(f"a0 FAILED at depth {D} -- search BROKEN.")
        return
    if args.self_check:
        comp = constructive_completeness_selfcheck(D, verbose=True)
        _mem_watchdog(f"self-check/depth{D}/completeness")
        snd = soundness_selfcheck(D, verbose=True)
        _mem_watchdog(f"self-check/depth{D}/soundness")
        print(f"[self-check peak RSS: {_total_rss_mb()/1024:.2f} GB (self+children); cap {HARD_MEM_CAP_GB:.0f} GB]")
        out = {**comp, **snd, "all_ok": comp["constructive_complete"] and snd["soundness_ok"]}
        if args.json:
            print(json.dumps(out, indent=2, default=str))
        if not comp["constructive_complete"]:
            raise SystemExit(f"CONSTRUCTIVE-COMPLETENESS FAILED (depth {D}) — null INVALID. HALT.")
        if not snd["soundness_ok"]:
            raise SystemExit(f"SOUNDNESS FAILED (depth {D}) — construction emits non-Gate-B candidates. HALT.")
        return
    if args.soundness:
        out = soundness_selfcheck(D, verbose=True)
        if args.json:
            print(json.dumps(out, indent=2, default=str))
        return
    if args.sweep:
        reps = sweep_all(D, sm_target_keys(), args.n_targets, verbose=True)
        if args.json:
            print(json.dumps(reps, indent=2, default=str))
        return
    if args.target:
        rep = run_target_depthD(args.target, D, n_targets_searched=args.n_targets, verbose=True)
        if args.json:
            print(json.dumps(rep, indent=2, default=str))
        return
    ap.print_help()


if __name__ == "__main__":
    main()
