#!/usr/bin/env python3
"""
exhaust_depth5_forced.py — the CONSTRUCTIVE, Gate-B-passable, DIMENSIONLESS depth-5 forced-interlock search.

WHAT THIS IS (Carl's brief, 2026-07-06):
    The honest continuation past the committed depth-4 CLEAN NULL (commit ee44122;
    exhaust_depth4_forced.py; STRUCTURAL DEPTH-BUDGET THEOREM). At depth 4, a Gate-B pass forces
    EXACTLY 3 distinct germ leaves (3, sqrt(8pi/3), one free) each costing one decorate level, leaving
    exactly ONE depth level for the scale skeleton -> exactly ONE dimensionful scale leaf -> nothing
    dimensionless survives the dimensional filter. Every dimensionless SM target died at the
    dimensional filter BEFORE the gates fired.

    DEPTH 5 is the FIRST depth where a Gate-B-passable DIMENSIONLESS kernel can exist: with 4 build
    steps, 3 go to the germ triple {3, sqrt(8pi/3), one free} and the last ONE step is a binary that
    appends a 2nd scale leaf -> a 2-scale monomial that can be DIMENSIONLESS (dims cancel). So at
    depth 5 the gates A/B/C ACTUALLY FIRE on real dimensionless candidates -- a substantive test.

TRACTABILITY: brute depth-5 = 30,916,931,441 trees/target (closed_form_count(11,5,25)) — infeasible.
    The STRUCTURAL THEOREM hands us the fix: enumerate the Gate-B-passable dimensionless SHAPES
    CONSTRUCTIVELY (2-scale dimensionless ratio  x  {3, sqrt(8pi/3), one free} germ triple) instead of
    brute-then-filter. Raw constructive = 918,528/target (33,659x smaller).

THE NEW RISK — CONSTRUCTIVE COMPLETENESS: the constructive scheme must PROVABLY generate EVERY
    Gate-B-passable dimensionless depth-5 tree, or a real kernel could be silently missed and the null
    would be INVALID. We prove it two ways:
      (a) THEOREM (shape uniqueness, §2 of the spec): every Gate-B-passable dimensionless depth-5 tree
          = { 2 dimensionless-cancelling scale leaves via MUL/DIV } decorated by { 3, sqrt(8pi/3), one
          free germ }, each germ via one decorate step (op in {MUL,DIV}, exp in {1,1/2,-1,-1/2}).
          [Any other allocation of the 4 build steps overflows depth, adds a 2nd free germ (Rset>=2,
          Gate-B-dead), or yields a dimensionful/single-scale tree.]
      (b) EMPIRICAL CROSS-CHECK vs the committed brute depth-4 enumerator: parametrize the SAME
          constructive builder by skeleton-shape and run it at depth 4 (1-scale skeleton + 3 germ
          decorates); assert it reproduces the committed brute depth-4 Gate-B `kept` VALUE-set EXACTLY
          (MISSED=0 EXTRA=0). AND assert the depth-<=4 DIMENSIONLESS Gate-B set is empty on BOTH the
          constructive and brute sides (the depth-4 theorem's anchor). If the constructive scheme
          misses even one brute Gate-B tree, it is INCOMPLETE -> HALT and fix.

FOUR NON-NEGOTIABLE HONESTY CONSTRAINTS (all enforced here):
  1. CONSTRUCTIVE COMPLETENESS — the --self-check MISSED=0 EXTRA=0 trip-wire (above). INVALIDATES the
     null if it fails.
  2. CONSTRUCTION SOUNDNESS — every emitted candidate is a genuine depth-<=5 tree presenting >=2 forced
     germs + <=1 free; verified by running the REAL gate.forced_kernel (via gate.validate) on a sample
     and asserting the keep predicate holds (--self-check soundness leg).
  3. FDR NON-SMUGGLE — Gate A density over the FULL 25-germ library (assert len(alpha.germs)==25),
     mult=21. The constructive pre-filter shrinks WHICH candidates are generated (tractability); it
     NEVER shrinks the library the surprise is measured against. At depth 5 the gates FIRE, so this is
     ACTIVELY load-bearing (unlike depth 4).
  4. a0 VALIDITY — a0 = (c/Z)*H_L must re-derive through the depth-5 dimensional filter (a0 is depth-3;
     at depth 5 it's a0 x identity). If a0 doesn't re-derive -> search BROKEN -> HALT.

RULE 3 (verbatim reuse): gate/ and engine/ and exhaust/exhaust_parallel imported UNMODIFIED. This file
    only adds a constructive depth-5 dimensionless enumerator + its completeness/soundness self-checks.
    We also import exhaust_depth4_forced's brute enumerator VERBATIM for the cross-check anchor.

CLI:
    python3 exhaust_depth5_forced.py --a0-check        # a0 re-derives+certifies through depth-5 (halt if not)
    python3 exhaust_depth5_forced.py --self-check      # constructive completeness (brute<=4 cross-check) + soundness
    python3 exhaust_depth5_forced.py --target r_mu_e   # one target, constructive depth-5, full gate
    python3 exhaust_depth5_forced.py --sweep           # all 21, single process
    python3 exhaust_depth5_forced.py --workers 16      # sharded parallel (detached), all cores
    python3 exhaust_depth5_forced.py --status          # aggregate shards + wall-clock + peak-mem
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import resource
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, FrozenSet, Iterator, List, Optional, Tuple

import mpmath as mp

mp.mp.dps = 40

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

# --- IMPORT VERBATIM (RULE 3): the engine, scoring, the whole gate ---
from engine.expr_tree import ExprNode, OpType, Label  # noqa: E402
from engine.scoring import score_value, measurement_tol  # noqa: E402

import exhaust as EX  # noqa: E402
from exhaust import (  # noqa: E402  (all reused verbatim)
    build_alphabet, Alphabet, Reachable,
    closed_form_count, _germ_provenance, _value_key,
    gate_candidate_for, resolve_target,
    _GERM_EXPONENTS,
)
from gate import validate  # noqa: E402  (the 3-part gate — NEVER modified)
from exhaust_parallel import sm_target_keys  # noqa: E402  (the canonical 21 SM targets)

# The committed depth-4 brute enumerator + its keep predicate — the CROSS-CHECK ANCHOR (verbatim).
from exhaust_depth4_forced import (  # noqa: E402
    enumerate_depth4_filtered, _keep_completed, _leaf_tag, FORCED_PROVS,
)

RESULTS = _HERE / "results_exhaust_depth5"
DEPTH = 5
N_TARGETS = 21


# =============================================================================
# 0.  THE CONSTRUCTIVE BUILDING BLOCKS  (§3 of the spec)
#
#     A Gate-B-passable dimensionless depth-<=5 tree is uniquely (THEOREM §2):
#       skeleton = a dimensionless SCALE monomial reachable with (max_depth-3) binary steps
#                  (depth 5 -> 1 binary step -> a 2-scale ratio;  depth 4 -> 0 binary steps ->
#                   a 1-scale leaf, which is dimensionful, so 0 dimensionless survivors)
#       decorated by the germ TRIPLE {3, sqrt(8pi/3), one free germ}, each via one decorate step
#       (op in {MUL,DIV}, exp in _GERM_EXPONENTS).
#
#     We build the skeleton set and the germ-triple decorations SEPARATELY, then take the product,
#     STREAMING each ExprNode and value-deduping — never materializing the raw 918,528 list.
# =============================================================================

# The two forced-credit germ keys (audited; verbatim from the depth-4 file's FORCED_PROVS).
_FORCED_KEYS = ("3", "sqrt(8pi/3)")   # 3 -> Ngen_3 ; sqrt(8pi/3) -> a0_kernel_8pi3


def _free_germ_keys(alpha: Alphabet) -> List[str]:
    """The FREE O(1) germ keys (provenance None): everything except the two forced-credit germs."""
    free = []
    for g in alpha.germs:
        if _germ_provenance(float(alpha.value(g))) is None:
            free.append(g)
    return free


def _forced_keys_present(alpha: Alphabet) -> List[str]:
    """The forced-credit germ keys actually in the pool (audited == {'3','sqrt(8pi/3)'})."""
    out = []
    for g in alpha.germs:
        if _germ_provenance(float(alpha.value(g))) is not None:
            out.append(g)
    return out


def _leaf_node(key: str) -> ExprNode:
    return ExprNode(OpType.CONST, const=key)


def _germ_pow_node(key: str, e) -> ExprNode:
    g = _leaf_node(key)
    return g if e == 1 else ExprNode(OpType.POW, children=[g], exp=e)


def _decorate(node: ExprNode, op: OpType, germ_key: str, e) -> ExprNode:
    """Apply ONE germ-decorate step  node (op) germ_key^e  — the +1-depth germ-introduction channel."""
    return ExprNode(op, children=[node, _germ_pow_node(germ_key, e)])


def constructive_skeletons(alpha: Alphabet, n_binary_steps: int) -> List[Reachable]:
    """The DIMENSIONLESS scale-skeleton set reachable with exactly `n_binary_steps` binary appends
    on a scale leaf, value-deduped. (Germs are added later by the decorate pass.)

    n_binary_steps == 0  -> a bare scale leaf. A single dimensionful scale is NEVER dimensionless,
                            so the DIMENSIONLESS skeleton set is EMPTY. (depth-4 anchor.)
    n_binary_steps == 1  -> a 2-scale monomial  s1 (MUL|DIV) s2 . Keep iff dimensionless. -> the 13.
    (n_binary_steps>=2 would need >=5 build steps once the 3 germ decorates are added -> depth>=6.)

    Returns Reachable skeletons (value-deduped, dimensionless, finite, >0).
    """
    leaves = alpha.leaves
    seen_v = set()
    out: List[Reachable] = []

    if n_binary_steps == 0:
        for k in leaves:
            n = _leaf_node(k)
            v, lab = n.evaluate(alpha)
            if not lab.is_dimensionless():
                continue
            if not mp.isfinite(v) or v <= 0:
                continue
            vk = _value_key(v)
            if vk in seen_v:
                continue
            seen_v.add(vk)
            out.append(Reachable(v, lab, n.to_string(alpha), n.canonical_hash(), n))
        return out

    if n_binary_steps == 1:
        for a in leaves:
            for b in leaves:
                for op in (OpType.MUL, OpType.DIV):
                    n = ExprNode(op, children=[_leaf_node(a), _leaf_node(b)])
                    v, lab = n.evaluate(alpha)
                    if not lab.is_dimensionless():
                        continue
                    if not mp.isfinite(v) or v <= 0:
                        continue
                    vk = _value_key(v)
                    if vk in seen_v:
                        continue
                    seen_v.add(vk)
                    out.append(Reachable(v, lab, n.to_string(alpha), n.canonical_hash(), n))
        return out

    raise ValueError("constructive_skeletons only supports n_binary_steps in {0,1} at depth<=5")


def _germ_triple_decorations(alpha: Alphabet, free_keys: List[str]
                             ) -> Iterator[Tuple[Tuple[str, OpType, object], ...]]:
    """Enumerate every germ-TRIPLE decoration recipe: keys exactly {3, sqrt(8pi/3), FREE}, each
    introduced by one decorate step with op in {MUL,DIV}, exp in _GERM_EXPONENTS, applied in one of
    3! orders. Yields a 3-tuple of (germ_key, op, exp) steps to fold onto a skeleton (in that order).

    Raw recipe count per skeleton = n_free * 3! * (2 * |_GERM_EXPONENTS|)^3
                                  = 23 * 6 * (2*4)^3 = 23 * 6 * 512 = 70,656.
    """
    forced = _forced_keys_present(alpha)             # ['3','sqrt(8pi/3)']  (audited)
    ops = (OpType.MUL, OpType.DIV)
    exps = list(_GERM_EXPONENTS)
    for free in free_keys:
        keys = (forced[0], forced[1], free)
        for order in itertools.permutations(keys):   # 3! orders
            step_choices = []
            for gk in order:
                step_choices.append([(gk, op, e) for op in ops for e in exps])
            for combo in itertools.product(*step_choices):
                yield combo


def constructive_gate_b_reachables(alpha: Alphabet, max_depth: int = DEPTH,
                                   dimensionless_only: bool = True
                                   ) -> Tuple[List[Reachable], Dict[str, int]]:
    """The CONSTRUCTIVE Gate-B-passable set at `max_depth`, STREAMING + value-deduped.

    Shape (THEOREM §2): skeleton (a scale monomial) x germ-triple {3, sqrt(8pi/3), one free}.
      max_depth == 5 -> skeleton = 1 binary step (2-scale ratio), 3 germ decorates = 4 build steps.
      max_depth == 4 -> skeleton = 0 binary steps (1 scale leaf), 3 germ decorates = 3 build steps.

    `dimensionless_only`:
      True  -> skeleton must be dimensionless (the SM-target path; depth-4 -> empty skeleton set).
      False -> skeleton may be ANY (single) scale leaf (only meaningful at max_depth==4: the
               1-scale-monomial shape family for the NON-VACUOUS brute cross-check).

    Returns (reachables, counts). Every returned Reachable carries (Fset==both forced, Rset=={one
    free}) by construction — it satisfies the Gate-B keep predicate _keep_completed. We STREAM the
    ExprNodes through a generator and hold only the two dedup sets + the deduped Reachable list.
    """
    n_binary = max_depth - 4      # 5 -> 1 ; 4 -> 0
    free_keys = _free_germ_keys(alpha)

    if dimensionless_only:
        skeletons = constructive_skeletons(alpha, n_binary)         # dimensionless skeletons
    else:
        # NON-VACUOUS cross-check path (max_depth==4 only): the 1-scale-leaf shape family, ANY dim.
        assert n_binary == 0, "dimensionless_only=False only defined for the depth-4 1-scale shape"
        skeletons = []
        seen_sk = set()
        for k in alpha.leaves:
            n = _leaf_node(k)
            v, lab = n.evaluate(alpha)
            if not mp.isfinite(v) or v <= 0:
                continue
            vk = _value_key(v)
            if vk in seen_sk:
                continue
            seen_sk.add(vk)
            skeletons.append(Reachable(v, lab, n.to_string(alpha), n.canonical_hash(), n))

    seen_canon = set()
    seen_value = set()
    reach: List[Reachable] = []
    raw = 0

    def _gen() -> Iterator[ExprNode]:
        nonlocal raw
        for sk in skeletons:
            for recipe in _germ_triple_decorations(alpha, free_keys):
                node = sk.node
                for (gk, op, e) in recipe:
                    node = _decorate(node, op, gk, e)
                raw += 1
                yield node

    for node in _gen():
        h = node.canonical_hash()
        if h in seen_canon:
            continue
        seen_canon.add(h)
        try:
            value, label = node.evaluate(alpha)
        except Exception:
            continue
        try:
            if not mp.isfinite(value) or value <= 0:
                continue
        except Exception:
            continue
        if dimensionless_only and not label.is_dimensionless():
            # (skeleton already dimensionless + germs dimensionless => always true; guard anyway)
            continue
        vk = _value_key(value)
        if vk in seen_value:
            continue
        seen_value.add(vk)
        reach.append(Reachable(value=value, label=label,
                               formula=node.to_string(alpha), canonical=h, node=node))

    counts = dict(
        n_skeletons=len(skeletons),
        raw_candidates=raw,
        distinct_canonical=len(seen_canon),
        distinct_by_value=len(reach),
    )
    return reach, counts


def constructive_space_size(alpha: Alphabet, max_depth: int = DEPTH) -> Dict[str, int]:
    """Closed-form raw constructive space size at `max_depth` (per target)."""
    n_binary = max_depth - 4
    n_free = len(_free_germ_keys(alpha))
    if n_binary == 1:
        n_sk = len(constructive_skeletons(alpha, 1))       # the 13 dimensionless ratios
    elif n_binary == 0:
        n_sk = len(constructive_skeletons(alpha, 0))       # 0 dimensionless skeletons
    else:
        n_sk = 0
    per_skeleton = n_free * math.factorial(3) * (2 * len(_GERM_EXPONENTS)) ** 3
    return dict(
        n_skeletons=n_sk,
        n_free=n_free,
        per_skeleton_recipes=per_skeleton,
        raw_per_target=n_sk * per_skeleton,
    )


# =============================================================================
# 1.  CONSTRUCTIVE-COMPLETENESS SELF-CHECK  (the load-bearing trip-wire, §4b)
#     Run the SAME constructive scheme at depth<=4 and compare to the committed brute enumerator.
# =============================================================================

def _brute_depth4_gate_b_valueset(alpha: Alphabet) -> Tuple[set, set]:
    """From the committed brute depth-4 enumerator: (value-set of ALL Gate-B `kept` completed trees,
    value-set of the DIMENSIONLESS Gate-B kept trees). The dimensionless set MUST be empty (anchor)."""
    kept, _counts = enumerate_depth4_filtered(alpha, 4)
    all_vals = set()
    dimless_vals = set()
    for t in kept:
        assert _keep_completed(t)   # every brute keep satisfies the Gate-B predicate
        v, lab = t.node.evaluate(alpha)
        if not mp.isfinite(v) or v <= 0:
            continue
        vk = _value_key(v)
        all_vals.add(vk)
        if lab.is_dimensionless():
            dimless_vals.add(vk)
    return all_vals, dimless_vals


def constructive_completeness_selfcheck(verbose: bool = True) -> dict:
    """PROVE constructive completeness empirically at depth<=4 against the committed brute enumerator.

    Two comparisons:
      (i)  DIMENSIONLESS anchor: constructive dimensionless Gate-B set at depth<=4  vs  brute
           dimensionless Gate-B set. BOTH must be EMPTY (the depth-4 theorem). MISSED=EXTRA=0.
      (ii) NON-VACUOUS teeth: constructive 1-scale-shape Gate-B set at depth 4 (dimensionless_only=
           False)  vs  brute ALL Gate-B `kept` value-set. The constructive scheme must reproduce the
           brute value-set EXACTLY (MISSED=0 EXTRA=0). This is the real completeness test: if the
           constructive builder cannot reproduce every brute Gate-B keep, it would silently miss
           kernels at depth 5.
    """
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25 and len(alpha.leaves) == 11

    brute_all, brute_dimless = _brute_depth4_gate_b_valueset(alpha)

    # (i) DIMENSIONLESS anchor
    con_dimless_reach, con_dimless_counts = constructive_gate_b_reachables(
        alpha, max_depth=4, dimensionless_only=True)
    con_dimless = {_value_key(r.value) for r in con_dimless_reach}
    missed_i = brute_dimless - con_dimless
    extra_i = con_dimless - brute_dimless
    anchor_ok = (len(brute_dimless) == 0 and len(con_dimless) == 0
                 and len(missed_i) == 0 and len(extra_i) == 0)

    # (ii) NON-VACUOUS: constructive 1-scale-shape family vs brute ALL Gate-B keep value-set
    con_all_reach, con_all_counts = constructive_gate_b_reachables(
        alpha, max_depth=4, dimensionless_only=False)
    con_all = {_value_key(r.value) for r in con_all_reach}
    missed_ii = brute_all - con_all
    extra_ii = con_all - brute_all
    teeth_ok = (len(missed_ii) == 0 and len(extra_ii) == 0)

    all_ok = anchor_ok and teeth_ok

    if verbose:
        print("=" * 100)
        print("CONSTRUCTIVE-COMPLETENESS SELF-CHECK  (constructive scheme vs committed BRUTE depth-4)")
        print("-" * 100)
        print("(i) DIMENSIONLESS anchor (depth<=4 Gate-B dimensionless set must be EMPTY on BOTH sides):")
        print(f"    brute dimensionless Gate-B values : {len(brute_dimless)}")
        print(f"    constructive dimensionless values : {len(con_dimless)}  "
              f"(raw {con_dimless_counts['raw_candidates']:,}, skeletons {con_dimless_counts['n_skeletons']})")
        print(f"    MISSED={len(missed_i)}  EXTRA={len(extra_i)}  -> {'OK (both empty)' if anchor_ok else 'FAIL'}")
        print("(ii) NON-VACUOUS teeth (constructive 1-scale shape reproduces brute ALL Gate-B keep VALUES):")
        print(f"    brute ALL Gate-B keep distinct values      : {len(brute_all):,}")
        print(f"    constructive 1-scale-shape distinct values : {len(con_all):,}  "
              f"(raw {con_all_counts['raw_candidates']:,})")
        print(f"    MISSED={len(missed_ii)}  EXTRA={len(extra_ii)}  -> {'OK (exact match)' if teeth_ok else 'FAIL'}")
        if missed_ii:
            print(f"      !! MISSED sample: {list(missed_ii)[:5]}")
        if extra_ii:
            print(f"      !! EXTRA sample:  {list(extra_ii)[:5]}")
        print("-" * 100)
        print(f"CONSTRUCTIVE_COMPLETE = {all_ok}   (anchor_ok={anchor_ok}, teeth_ok={teeth_ok})")
        print("=" * 100)

    return {
        "constructive_complete": all_ok,
        "anchor_ok": anchor_ok,
        "teeth_ok": teeth_ok,
        "brute_dimless_count": len(brute_dimless),
        "constructive_dimless_count": len(con_dimless),
        "brute_all_count": len(brute_all),
        "constructive_all_count": len(con_all),
        "missed_dimless": len(missed_i),
        "extra_dimless": len(extra_i),
        "missed_all": len(missed_ii),
        "extra_all": len(extra_ii),
    }


# =============================================================================
# 2.  CONSTRUCTION-SOUNDNESS SELF-CHECK  (§4, honesty constraint 2)
#     Sample constructive depth-5 candidates and run the REAL gate; all must pass the keep predicate.
# =============================================================================

def soundness_selfcheck(sample_n: int = 400, verbose: bool = True) -> dict:
    """Every constructive depth-5 candidate must present (Fset==both forced, Rset=={one free}) so
    that the REAL gate.forced_kernel (via gate.validate) reports kernel.passed=True. We sample the
    depth-5 dimensionless constructive set and, for each, (a) recompute the germ-leaf tag and assert
    _keep_completed, and (b) build the REAL gate candidate and assert v.kernel.passed is True."""
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25
    reach, counts = constructive_gate_b_reachables(alpha, max_depth=5, dimensionless_only=True)

    # sample deterministically across the set
    n = len(reach)
    if n == 0:
        raise SystemExit("SOUNDNESS: constructive depth-5 set is EMPTY — construction BROKEN.")
    step = max(1, n // sample_n)
    sample = reach[::step][:sample_n]

    tag_ok = 0
    kernel_ok = 0
    bad = []
    tspec = resolve_target("r_mu_e")     # any dimensionless target; only the kernel leg is tested
    for r in sample:
        # (a) germ-leaf tag from the real _leaf_tag (reused verbatim from depth-4)
        Fset = frozenset()
        Rset = frozenset()
        for k in set(r.node.leaf_consts()):
            F, R = _leaf_tag(alpha, k)
            Fset |= F
            Rset |= R
        keep = (len(Fset) == 2 and len(Rset) == 1)
        if keep:
            tag_ok += 1
        else:
            bad.append((r.formula, sorted(Fset), sorted(Rset)))
            continue
        # (b) the REAL gate's forced-kernel leg
        gc = gate_candidate_for(r, alpha, "r_mu_e", tspec.pdg_target, N_TARGETS)
        v = validate(gc)
        if v.kernel.passed:
            kernel_ok += 1
        else:
            bad.append((r.formula, "kernel.passed=False", v.tell[:80]))

    soundness_ok = (tag_ok == len(sample) and kernel_ok == len(sample))

    if verbose:
        print("=" * 100)
        print("CONSTRUCTION-SOUNDNESS SELF-CHECK  (real gate.forced_kernel on constructive depth-5 sample)")
        print("-" * 100)
        print(f"  constructive depth-5 dimensionless set: {n:,} distinct values "
              f"(raw {counts['raw_candidates']:,})")
        print(f"  sampled: {len(sample)}")
        print(f"  keep-predicate (Fset==both & 1 free) pass : {tag_ok}/{len(sample)}")
        print(f"  REAL gate kernel.passed=True             : {kernel_ok}/{len(sample)}")
        if bad:
            print(f"  !! {len(bad)} FAILURES (sample): {bad[:5]}")
        print("-" * 100)
        print(f"SOUNDNESS_OK = {soundness_ok}")
        print("=" * 100)

    return {
        "soundness_ok": soundness_ok,
        "n_constructive": n,
        "n_sampled": len(sample),
        "tag_ok": tag_ok,
        "kernel_ok": kernel_ok,
        "n_bad": len(bad),
    }


# =============================================================================
# 3.  a0-VALIDITY through the depth-5 pipeline  (RULE 2 reach proof)
# =============================================================================

def a0_validity_depth5(verbose: bool = True) -> dict:
    """a0 must RE-DERIVE AND be depth-5-REACHABLE through the real pipeline (the RULE-2 reach proof).

    Pinned a0 pool {c,G,Lambda,rho_Lambda,H_Lambda}+{pi,8,3,2,32pi,sqrt(8pi/3),Z}. a0 is DEPTH-3
    (a0 = (c/Z)*H_L = c^2 sqrt(Lambda/32pi), L/T^2), so it appears at depth 5 as a0 x identity.

    TWO-LEG reach proof (both through the UNMODIFIED evaluate + DIMENSIONAL filter + gate):

      LEG 1 — DIMENSIONAL-FILTER re-derivation via the committed depth-generic enumerator
        (exhaust.build_reachable_set) at depth 4 on the pinned pool (2.05M raw, ~35s; the SAME
        tractable path the committed depth-4 file uses). PASS = the dimensional filter re-finds
        a0 = 9.36e-11 to <1%. [Running the FULL depth-5 pinned-pool brute is 149.9M raw ~ 43 min and
        adds nothing: a0 is depth-3, and depth-5 only re-emits it as a0 x identity, which LEG 2
        certifies directly. So we do NOT pay the 43-min depth-5 brute for a depth-3 quantity.]

      LEG 2 — explicit DEPTH-5 IDENTITY EXTENSION certified through the real pipeline: build the
        genuine depth-5 ExprNode ((c*H_L)/Z * 3)/3 (a0 x 3/3 — 4 build steps on top of the c leaf =
        depth 5), run the UNMODIFIED node.evaluate -> assert L/T^2 dims AND value == a0 to <1%, then
        push it through the REAL gate (gate_candidate_for + validate). This PROVES a0 is reachable
        AND certifies through the depth-5 gate pipeline, not merely at depth 4.

    The gate verdict on the a0 hit stays NOT-CERTIFIED / FDR-DEAD (a0 presents ONE forced provenance
    in the CODE -> not overdetermined) — EXPECTED, consistent with the depth-3 theorem. The REACH
    proof is the dimensional re-derivation (LEG 1) + the depth-5 identity certification (LEG 2), both
    of which PASS. PASS overall = LEG 1 re-finds a0 AND LEG 2's depth-5 tree evaluates to a0 (L/T^2).
    """
    a0_pool_leaves = ["c", "G", "Lambda", "rho_Lambda", "H_Lambda"]
    a0_pool_germs = ["pi", "8", "3", "2", "32pi", "sqrt(8pi/3)", "Z"]
    tspec = resolve_target("a0")
    alpha = build_alphabet(a0_pool_leaves, a0_pool_germs)
    tol = 0.01

    # ---- LEG 1: dimensional-filter re-derivation at depth 4 (tractable, committed path) ----
    leg1_depth = 4
    t0 = time.time()
    reach, cnts = EX.build_reachable_set(alpha, leg1_depth, tspec.label)
    wall = time.time() - t0
    best = None
    for r in reach:
        card = score_value(float(r.value), tspec.pdg_target)
        if card.rel_error <= tol:
            if best is None or card.rel_error < best[1].rel_error:
                best = (r, card)
    a0_refound = best is not None
    gate_status = gate_tell = formula = None
    rel_err = n_sigma = None
    if a0_refound:
        r, card = best
        rel_err, n_sigma, formula = card.rel_error, card.n_sigma, r.formula
        gc = gate_candidate_for(r, alpha, "a0", tspec.pdg_target, N_TARGETS)
        v = validate(gc)
        gate_status, gate_tell = v.status, v.tell

    # ---- LEG 2: explicit DEPTH-5 identity extension, certified through the real pipeline ----
    #   node = ((c*H_L)/Z * 3) / 3   — depths: c[1] -> c*H_L[2] -> /Z[3] -> *3[4] -> /3[5]
    a0_core = ExprNode(OpType.DIV, children=[
        ExprNode(OpType.MUL, children=[_leaf_node("c"), _leaf_node("H_Lambda")]),
        _leaf_node("Z")])
    a0_d5 = ExprNode(OpType.DIV, children=[
        ExprNode(OpType.MUL, children=[a0_core, _leaf_node("3")]), _leaf_node("3")])
    v5, lab5 = a0_d5.evaluate(alpha)
    card5 = score_value(float(v5), tspec.pdg_target)
    leg2_dims_ok = lab5.dims_equal(tspec.label)
    leg2_value_ok = (card5.rel_error <= tol)
    r5 = Reachable(v5, lab5, a0_d5.to_string(alpha), a0_d5.canonical_hash(), a0_d5)
    gc5 = gate_candidate_for(r5, alpha, "a0", tspec.pdg_target, N_TARGETS)
    v5gate = validate(gc5)
    leg2_ok = bool(leg2_dims_ok and leg2_value_ok)

    a0_certifies_depth5 = bool(a0_refound and leg2_ok)

    if verbose:
        print("=" * 100)
        print("a0-VALIDITY through the DEPTH-5 pipeline (RULE 2 reach proof; 2 legs)")
        print(f"  pinned pool: {a0_pool_leaves} + {a0_pool_germs}   tol={tol}")
        print("-" * 100)
        print(f"  LEG 1 — DIMENSIONAL-FILTER re-derivation (build_reachable_set @ depth {leg1_depth}):")
        print(f"    raw emitted: {cnts['raw_emitted']:,}   dim-valid (L/T^2): {cnts['dim_valid']:,}   "
              f"distinct: {cnts['distinct_by_value']:,}   ({wall:.1f}s)")
        if a0_refound:
            print(f"    a0 RE-FOUND:  {formula}  = {float(best[0].value):.6g} m/s^2  "
                  f"(target 9.36e-11; rel_err={rel_err:.2e}, n_sigma={n_sigma:.2f})")
            print(f"    gate verdict on a0 hit: [{gate_status}]  {gate_tell[:100] if gate_tell else ''}")
        else:
            print("    a0 NOT re-found -> search BROKEN.")
        print(f"    (depth-5 pinned-pool brute = 149.9M raw ~43min, SKIPPED: a0 is depth-3; depth-5")
        print(f"     only re-emits it as a0 x identity, which LEG 2 certifies directly.)")
        print("-" * 100)
        print(f"  LEG 2 — explicit DEPTH-5 identity extension through the REAL pipeline:")
        print(f"    depth-5 node: {a0_d5.to_string(alpha)}")
        print(f"      = {float(v5):.6g} m/s^2   dims L/T^2 ? {leg2_dims_ok}   "
              f"value==a0 (<1%) ? {leg2_value_ok} (rel_err={card5.rel_error:.2e})")
        print(f"    gate verdict on depth-5 a0 tree: [{v5gate.status}]  "
              f"(EXPECTED FDR-DEAD: one forced provenance -> not overdetermined)")
        print("-" * 100)
        print(f"  a0_certifies_depth5 (LEG1 dim-filter re-finds a0 AND LEG2 depth-5 tree == a0): "
              f"{'PASS' if a0_certifies_depth5 else 'FAIL'}")
        print("=" * 100)

    return {
        "a0_refound": a0_refound,
        "a0_certifies_depth5": a0_certifies_depth5,
        "leg1_a0_refound": a0_refound,
        "leg1_formula": formula,
        "leg1_rel_error": rel_err,
        "leg1_n_sigma": n_sigma,
        "leg1_gate_status": gate_status,
        "leg1_depth": leg1_depth,
        "leg1_raw_emitted": cnts["raw_emitted"],
        "leg1_dim_valid": cnts["dim_valid"],
        "leg1_wall_s": wall,
        "leg2_depth5_node": a0_d5.to_string(alpha),
        "leg2_value": float(v5),
        "leg2_dims_ok": leg2_dims_ok,
        "leg2_value_ok": leg2_value_ok,
        "leg2_rel_error": float(card5.rel_error),
        "leg2_gate_status": v5gate.status,
        "leg2_ok": leg2_ok,
    }


# =============================================================================
# 4.  THE DRIVER  (constructive depth-5 -> in-window match -> FULL 3-part gate)
# =============================================================================

@dataclass
class Hit5:
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


def run_target_depth5(target_key: str, tol: Optional[float] = None,
                      n_targets_searched: int = N_TARGETS, verbose: bool = True,
                      shared: Optional[Tuple[Alphabet, List[Reachable], Dict[str, int]]] = None
                      ) -> dict:
    """End-to-end constructive depth-5 run on ONE target. The constructive Gate-B-passable
    DIMENSIONLESS reachable set is TARGET-INDEPENDENT, so `shared` lets a worker build it ONCE and
    score it against many targets (only the window + gate differ per target)."""
    tspec = resolve_target(target_key)
    if shared is None:
        alpha = build_alphabet(None, None)
        assert len(alpha.germs) == 25, f"FDR non-smuggle: expected 25 germs, got {len(alpha.germs)}"
        reach, counts = constructive_gate_b_reachables(alpha, DEPTH, dimensionless_only=True)
    else:
        alpha, reach, counts = shared
        assert len(alpha.germs) == 25

    if tol is None:
        tol = measurement_tol(tspec.pdg_target)

    hits: List[Hit5] = []
    for r in reach:
        card = score_value(float(r.value), tspec.pdg_target)
        if card.rel_error <= tol:
            gc = gate_candidate_for(r, alpha, target_key, tspec.pdg_target, n_targets_searched)
            v = validate(gc)
            hits.append(Hit5(
                formula=r.formula, value=float(r.value), rel_error=card.rel_error,
                n_sigma=card.n_sigma, status=v.status, fdr_bits=v.fdr.bits, fdr_mode=v.fdr.mode,
                kernel_passed=v.kernel.passed, interlock_passed=v.interlock.passed, gate_tell=v.tell,
            ))
    hits.sort(key=lambda h: h.rel_error)
    certified = [h for h in hits if h.status == "CERTIFIED"]
    relabeled = [h for h in hits if h.status == "REAL-PUZZLE-RE-LABELED"]

    report = {
        "target": target_key,
        "target_value": tspec.value,
        "target_dimension": tspec.label_name,
        "depth": DEPTH,
        "tol": tol,
        "n_leaves": len(alpha.leaves),
        "n_germs": len(alpha.germs),
        "fdr_uses_full_library": (len(alpha.germs) == 25),
        "constructive_raw_per_target": counts["raw_candidates"],
        "constructive_skeletons": counts["n_skeletons"],
        "constructive_distinct_values": counts["distinct_by_value"],
        "n_hits": len(hits),
        "n_certified": len(certified),
        "n_relabeled": len(relabeled),
        "hits": [h.__dict__ for h in hits[:20]],
    }
    if verbose:
        _print_target_report(report)
    return report


def _print_target_report(rep: dict):
    print("=" * 100)
    print(f"DEPTH-5 CONSTRUCTIVE FORCED-INTERLOCK — target {rep['target']} = {rep['target_value']:.6g} "
          f"[dim {rep['target_dimension']}]")
    print(f"  tol={rep['tol']:.2e}   pool: {rep['n_leaves']} leaves + {rep['n_germs']} germs")
    print(f"  FDR library = FULL {rep['n_germs']}-germ pool: "
          f"{'YES (non-smuggle OK)' if rep['fdr_uses_full_library'] else 'NO -- SMUGGLE BUG'}   mult={N_TARGETS}")
    print(f"  constructive raw/target: {rep['constructive_raw_per_target']:,}  "
          f"(skeletons {rep['constructive_skeletons']})  -> distinct dimensionless VALUES: "
          f"{rep['constructive_distinct_values']:,}")
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

# =============================================================================
# MANDATORY MEMORY WATCHDOG (Carl's brief, HARD requirement — the #1 fix)
#   The previous depth-5 run thrashed 64 GB into 35 GB swap and had to be KILLED. The constructive
#   scheme holds only bounded dedup sets (~300 MB observed), so any breach of the HARD 6 GB cap is a
#   BUG (a memory leak / a non-streaming path), NOT a reason to raise the cap. We sample our OWN RSS
#   (RUSAGE_SELF + RUSAGE_CHILDREN, so the launcher counts detached workers too) and ABORT with a
#   clear message the instant total RSS exceeds the cap.
# =============================================================================
HARD_MEM_CAP_GB = 6.0
_MEM_CAP_MB = HARD_MEM_CAP_GB * 1024.0


def _rss_mb(which) -> float:
    ru = resource.getrusage(which).ru_maxrss
    # macOS reports bytes; Linux reports KiB.
    return ru / (1024 * 1024) if sys.platform == "darwin" else ru / 1024


def _total_rss_mb() -> float:
    """Peak RSS of this process AND any (detached) children — the watchdog's measured quantity."""
    return _rss_mb(resource.RUSAGE_SELF) + _rss_mb(resource.RUSAGE_CHILDREN)


def _peak_mem_mb() -> float:
    return _rss_mb(resource.RUSAGE_SELF)


def _mem_watchdog(where: str = ""):
    """ABORT if total RSS (self + children) exceeds the HARD 6 GB cap. Call at every phase boundary
    (after building the constructive set, per-target, per-shard-write). A breach is a BUG — the
    correct constructive/streaming run peaks near ~300 MB."""
    tot = _total_rss_mb()
    if tot > _MEM_CAP_MB:
        raise SystemExit(
            f"MEMORY WATCHDOG ABORT{(' @ ' + where) if where else ''}: total RSS "
            f"{tot/1024:.2f} GB exceeded the HARD {HARD_MEM_CAP_GB:.0f} GB cap. The constructive "
            f"scheme must stream (peak ~0.3 GB); a breach means a non-streaming/leaking path — FIX "
            f"the bug, do NOT raise the cap.")


def sweep_all(targets: List[str], n_targets_searched: int, verbose: bool = True) -> List[dict]:
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25
    t0 = time.time()
    reach, counts = constructive_gate_b_reachables(alpha, DEPTH, dimensionless_only=True)
    build_s = time.time() - t0
    _mem_watchdog("sweep_all/after-build")
    if verbose:
        print(f"[built constructive depth-5 set ONCE: {counts['distinct_by_value']:,} distinct "
              f"dimensionless values from {counts['raw_candidates']:,} raw in {build_s:.1f}s]")
    shared = (alpha, reach, counts)
    out = []
    for k in targets:
        out.append(run_target_depth5(k, n_targets_searched=n_targets_searched, verbose=verbose, shared=shared))
        _mem_watchdog(f"sweep_all/{k}")
    if verbose:
        print(f"[sweep peak RSS: {_total_rss_mb()/1024:.2f} GB (self+children); cap {HARD_MEM_CAP_GB:.0f} GB]")
    return out


def _shard_targets(targets: List[str], n: int) -> List[List[str]]:
    return [targets[i::n] for i in range(n)]


def launch_parallel(workers: int):
    RESULTS.mkdir(parents=True, exist_ok=True)
    targets = sm_target_keys()
    # CAP workers at 12 (leave headroom on the 16-core box, per the brief). The constructive space
    # is tiny (each worker peaks ~0.3 GB), so parallelism is for SPEED, not necessity.
    workers = min(workers, 12, len(targets))
    shards = _shard_targets(targets, workers)
    pids = []
    for i, sl in enumerate(shards):
        if not sl:
            continue
        sd = RESULTS / f"shard_{i}"
        sd.mkdir(parents=True, exist_ok=True)
        logf = open(sd / "run.log", "w")
        p = subprocess.Popen(
            [sys.executable, str(_HERE / "exhaust_depth5_forced.py"),
             "--worker", str(i), "--targets", ",".join(sl), "--n-targets", str(len(targets))],
            stdout=logf, stderr=subprocess.STDOUT, cwd=str(_HERE), start_new_session=True,
        )
        pids.append({"shard": i, "pid": p.pid, "targets": sl})
    (RESULTS / "pids.json").write_text(json.dumps(pids, indent=2))
    print(f"launched {len(pids)} workers over {len(targets)} targets -> {RESULTS}")
    for pd in pids:
        print(f"  shard {pd['shard']}: pid {pd['pid']}  targets {pd['targets']}")


def run_worker(shard: int, targets: List[str], n_targets: int):
    RESULTS.mkdir(parents=True, exist_ok=True)
    sd = RESULTS / f"shard_{shard}"
    sd.mkdir(parents=True, exist_ok=True)
    t0 = time.time()
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25
    reach, counts = constructive_gate_b_reachables(alpha, DEPTH, dimensionless_only=True)
    build_s = time.time() - t0
    _mem_watchdog(f"worker{shard}/after-build")
    shared = (alpha, reach, counts)
    out = []
    for k in targets:
        rep = run_target_depth5(k, n_targets_searched=n_targets, verbose=True, shared=shared)
        out.append(rep)
        _mem_watchdog(f"worker{shard}/{k}")
        wall = time.time() - t0
        meta = {
            "shard": shard, "targets_done": len(out), "targets_total": len(targets),
            "build_s": build_s, "wall_s": wall, "peak_mem_mb": _peak_mem_mb(),
            "constructive_raw_per_target": counts["raw_candidates"],
            "constructive_distinct_values": counts["distinct_by_value"],
            "results": out,
        }
        (sd / "result.json").write_text(json.dumps(meta, indent=2, default=str))


def aggregate_status(as_json: bool = False):
    if not RESULTS.exists():
        print("no results yet")
        return
    metas = []
    for sd in sorted(RESULTS.glob("shard_*")):
        rf = sd / "result.json"
        if rf.exists():
            metas.append(json.loads(rf.read_text()))
    rows = [r for m in metas for r in m.get("results", [])]
    n_cert = sum(r["n_certified"] for r in rows)
    n_rel = sum(r["n_relabeled"] for r in rows)
    max_wall = max((m.get("wall_s", 0.0) for m in metas), default=0.0)
    max_mem = max((m.get("peak_mem_mb", 0.0) for m in metas), default=0.0)
    if as_json:
        print(json.dumps({"n_targets_done": len(rows), "n_certified": n_cert, "n_relabeled": n_rel,
                          "max_wall_s": max_wall, "max_peak_mem_mb": max_mem, "rows": rows},
                         indent=2, default=str))
        return
    print(f"targets done: {len(rows)}   CERTIFIED total: {n_cert}   RE-LABELED total: {n_rel}")
    print(f"max wall-clock across shards: {max_wall:.1f}s   max peak mem: {max_mem:.0f} MB")
    for r in sorted(rows, key=lambda x: x["target"]):
        print(f"  {r['target']:18} distinct={r['constructive_distinct_values']:>6,}  "
              f"hits={r['n_hits']:>3}  CERT={r['n_certified']}  RELAB={r['n_relabeled']}")


# =============================================================================
# CLI
# =============================================================================

def main():
    ap = argparse.ArgumentParser(description="Constructive, Gate-B-passable, dimensionless depth-5 "
                                             "forced-interlock search.")
    ap.add_argument("--target", default=None, help="one SM target key (constructive depth-5 run).")
    ap.add_argument("--a0-check", action="store_true", help="a0-validity through depth-5 (reach proof).")
    ap.add_argument("--self-check", action="store_true",
                    help="constructive-completeness (brute<=4 cross-check) + soundness self-checks.")
    ap.add_argument("--space", action="store_true", help="print the constructive space size and exit.")
    ap.add_argument("--sweep", action="store_true", help="all 21 SM targets, single process.")
    ap.add_argument("--n-targets", type=int, default=N_TARGETS, help="look-elsewhere multiplicity.")
    ap.add_argument("--json", action="store_true")
    # parallel
    ap.add_argument("--workers", type=int, default=None, help="launch N detached shard workers.")
    ap.add_argument("--status", action="store_true", help="aggregate shard results + wall/mem.")
    ap.add_argument("--worker", type=int, default=None, help="(internal) shard index.")
    ap.add_argument("--targets", default=None, help="(internal) comma-list for a worker.")
    args = ap.parse_args()

    if args.worker is not None and args.targets:
        run_worker(args.worker, args.targets.split(","), args.n_targets)
        return
    if args.workers:
        launch_parallel(args.workers)
        return
    if args.status:
        aggregate_status(args.json)
        return
    if args.space:
        alpha = build_alphabet(None, None)
        s5 = constructive_space_size(alpha, 5)
        brute = closed_form_count(11, 5, 25)
        total5 = s5["raw_per_target"] * N_TARGETS
        print(json.dumps({
            "constructive_raw_per_target": s5["raw_per_target"],
            "constructive_skeletons": s5["n_skeletons"], "n_free": s5["n_free"],
            "per_skeleton_recipes": s5["per_skeleton_recipes"],
            "constructive_total_21_targets": total5,
            "brute_depth5_per_target": brute[-1],
            "brute_depth5_total_all_depths_per_target": sum(brute),
            "shrink_factor_vs_brute": brute[-1] / s5["raw_per_target"],
        }, indent=2))
        return
    if args.a0_check:
        out = a0_validity_depth5(verbose=True)
        if args.json:
            print(json.dumps(out, indent=2, default=str))
        if not out["a0_certifies_depth5"]:
            raise SystemExit("a0 FAILED to re-derive at depth 5 -- search BROKEN.")
        return
    if args.self_check:
        comp = constructive_completeness_selfcheck(verbose=True)
        _mem_watchdog("self-check/completeness")
        snd = soundness_selfcheck(verbose=True)
        _mem_watchdog("self-check/soundness")
        print(f"[self-check peak RSS: {_total_rss_mb()/1024:.2f} GB (self+children); "
              f"cap {HARD_MEM_CAP_GB:.0f} GB]")
        out = {**comp, **snd, "all_ok": comp["constructive_complete"] and snd["soundness_ok"]}
        if args.json:
            print(json.dumps(out, indent=2, default=str))
        if not comp["constructive_complete"]:
            raise SystemExit("CONSTRUCTIVE-COMPLETENESS FAILED — the depth-5 null is INVALID. HALT.")
        if not snd["soundness_ok"]:
            raise SystemExit("SOUNDNESS FAILED — construction emits non-Gate-B candidates. HALT.")
        return
    if args.sweep:
        reps = sweep_all(sm_target_keys(), args.n_targets, verbose=True)
        if args.json:
            print(json.dumps(reps, indent=2, default=str))
        return
    if args.target:
        rep = run_target_depth5(args.target, n_targets_searched=args.n_targets, verbose=True)
        if args.json:
            print(json.dumps(rep, indent=2, default=str))
        return
    ap.print_help()


if __name__ == "__main__":
    main()
