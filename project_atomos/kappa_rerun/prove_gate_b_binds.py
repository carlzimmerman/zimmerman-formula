#!/usr/bin/env python3
"""prove_gate_b_binds.py -- does GATE B still BIND when the forced pair is {3, kappa}?

THE RISK THIS SCRIPT EXISTS TO FIND
-----------------------------------
kappa = 1/2 = 2^(-1), and '2' is a germ, and the germ-decorate step is  node (MUL|DIV) germ^e
with e in {1, 1/2, -1, -1/2}.  So "MUL by kappa" and "DIV by 2" are THE SAME VALUE OPERATION.
If gate.forced_kernel credited forced factors by VALUE, then every expression could pick up the
"forced" kappa for free by dividing by 2, Gate B would stop binding, and the whole re-run would
be meaningless.  This script does not reason about that -- it pushes explicit expressions through
the REAL committed gate code (exhaust.gate_candidate_for -> gate.validate -> KernelResult.passed)
and through the REAL build-time pre-filter (exhaust_depth4_forced._leaf_tag / _keep_completed),
and prints what actually happens.

Every expression is a real ExprNode built with the committed builders D5._leaf_node /
D5._germ_pow_node / D5._decorate, on the committed dimensionless skeleton (c / c) -- the same
skeleton the committed depth-6 tightest hit uses.

Exit 0 = every expectation held.  Nonzero = Gate B does NOT behave as the re-run requires.
"""
from __future__ import annotations

import os
import sys
from typing import List, Optional, Tuple

import mpmath as mp

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

import exhaust as EX                                        # noqa: E402
from exhaust import Reachable, gate_candidate_for, resolve_target   # noqa: E402
from engine.expr_tree import ExprNode, OpType               # noqa: E402
from gate import validate                                   # noqa: E402
import exhaust_depth5_forced as D5                          # noqa: E402
import exhaust_depth4_forced as D4                          # noqa: E402
from exhaust_depth5_forced import N_TARGETS                 # noqa: E402

from kappa_forced import (                                  # noqa: E402
    forced_pair, KAPPA_GERM_KEY, KAPPA_REGISTRY_KEY,
    germ_provenance_map, assert_field_exists, assert_no_holdout,
)

mp.mp.dps = 40

_ok = True


def _check(cond: bool, msg: str) -> bool:
    global _ok
    if not cond:
        _ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")
    return bool(cond)


def _banner(s: str):
    print("\n" + "=" * 100)
    print(s)
    print("=" * 100)


# --------------------------------------------------------------------------------------------
# expression construction: (c / c) decorated by a list of (germ_key, signed_exponent)
# --------------------------------------------------------------------------------------------
def build_expr(alpha, decorations: List[Tuple[str, float]]) -> ExprNode:
    """(c / c) then one decorate step per (germ_key, e). e<0 -> DIV by germ^|e| (the committed
    encoding: op MUL/DIV x exp in _GERM_EXPONENTS gives the signed exponent)."""
    node = ExprNode(OpType.DIV, children=[D5._leaf_node("c"), D5._leaf_node("c")])
    for gk, e in decorations:
        op = OpType.MUL if e > 0 else OpType.DIV
        node = D5._decorate(node, op, gk, mp.mpf(abs(e)))
    return node


def as_reachable(alpha, node: ExprNode) -> Reachable:
    value, label = node.evaluate(alpha)
    return Reachable(value=value, label=label, formula=node.to_string(alpha),
                     canonical=node.canonical_hash(), node=node)


def run_gate(alpha, node: ExprNode, target_key: str = "r_mu_e"):
    """Push a node through the REAL gate. Returns (gate_b_passed, prefilter_kept, kres, Fset, Rset)."""
    r = as_reachable(alpha, node)
    tspec = resolve_target(target_key)
    gc = gate_candidate_for(r, alpha, target_key, tspec.pdg_target, N_TARGETS)
    v = validate(gc)
    # field-name guard (bug #1): never filter on a field that does not exist
    assert_field_exists(v, "kernel", "gate verdict")
    assert_field_exists(v.kernel, "passed", "KernelResult")
    assert_field_exists(v, "status", "gate verdict")
    # the build-time pre-filter, on the same node
    F: frozenset = frozenset()
    R: frozenset = frozenset()
    for k in set(node.leaf_consts()):
        f, rr = D4._leaf_tag(alpha, k)
        F |= f
        R |= rr
    kept = D4._keep_completed(D4.Tagged(node, F, R))
    return v.kernel.passed, kept, v.kernel, F, R


def report(alpha, name: str, decorations, expect_pass: bool, target_key: str = "r_mu_e"):
    node = build_expr(alpha, decorations)
    passed, kept, kres, F, R = run_gate(alpha, node, target_key)
    value, _ = node.evaluate(alpha)
    verdict = "PASS" if passed else "FAIL"
    good = (passed == expect_pass)
    _check(good, f"{name:<52} Gate B={verdict:<4} (expected {'PASS' if expect_pass else 'FAIL'})")
    print(f"          formula   : {node.to_string(alpha)}")
    print(f"          value     : {mp.nstr(value, 22)}")
    print(f"          forced    : {sorted(F)}   free germ keys: {sorted(R)}   n_free={kres.n_free_params}")
    print(f"          prefilter : _keep_completed={kept}  (must agree with Gate B)")
    print(f"          tell      : {kres.tell[:150]}")
    if kept != passed:
        _check(False, f"{name}: build-time pre-filter and the real gate DISAGREE")
    return value


def main() -> int:
    _banner("prove_gate_b_binds -- pushing explicit expressions through the REAL gate code")
    assert_no_holdout(["r_mu_e"], "the target used by this proof")

    # ==========================================================================================
    # PART 1 -- PUBLISHED pair {3, sqrt(8pi/3)}: the control. The gate must behave as published.
    # ==========================================================================================
    _banner("PART 1. control: PUBLISHED forced pair {3, sqrt(8pi/3)}  (switch OFF)")
    with forced_pair(mode="published"):
        a = EX.build_alphabet(None, None)
        print(f"  forced germ keys present: {D5._forced_keys_present(a)}")
        half_key_pub = "flv_koide_cos2_angle"        # the 0.5-valued germ under the published pool
        print(f"  the 0.5-valued germ here is {half_key_pub!r}, provenance="
              f"{germ_provenance_map(a)[half_key_pub]}")
        report(a, "neither forced germ  {pi, 2, 4}", [("pi", 1), ("2", 1), ("4", 1)], False)
        report(a, "only 3               {3, pi, 2}", [("3", 1), ("pi", 1), ("2", 1)], False)
        report(a, "only 3, one free     {3, pi}", [("3", 1), ("pi", 1)], False)
        report(a, "only sqrt(8pi/3)     {sqrt(8pi/3), pi}", [("sqrt(8pi/3)", 1), ("pi", 1)], False)
        report(a, "published pair + 1 free {3, sqrt(8pi/3), pi}",
               [("3", 1), ("sqrt(8pi/3)", 1), ("pi", 1)], True)
        report(a, "published pair + 2 free {3, sqrt(8pi/3), pi, 2}",
               [("3", 1), ("sqrt(8pi/3)", 1), ("pi", 1), ("2", 1)], False)
        report(a, "3 + the 1/2 germ + 1 free (kappa NOT registered)",
               [("3", 1), (half_key_pub, 1), ("pi", 1)], False)

    # ==========================================================================================
    # PART 2 -- KAPPA pair {3, kappa}: the four required cases + the impostor test.
    # ==========================================================================================
    _banner("PART 2. the re-run pair {3, kappa}  (switch ON)")
    with forced_pair(mode="kappa"):
        a = EX.build_alphabet(None, None)
        print(f"  forced germ keys present: {D5._forced_keys_present(a)}")
        print(f"  registry: {KAPPA_REGISTRY_KEY} -> "
              f"{__import__('gate.registry', fromlist=['x']).forced_value(KAPPA_REGISTRY_KEY)}")

        # ---- the four cases the task requires -------------------------------------------------
        report(a, "1. NEITHER forced germ  {pi, 2, 4}", [("pi", 1), ("2", 1), ("4", 1)], False)
        report(a, "2. ONLY 3               {3, pi, 2}", [("3", 1), ("pi", 1), ("2", 1)], False)
        report(a, "2b. ONLY 3, one free    {3, pi}", [("3", 1), ("pi", 1)], False)
        report(a, "3. ONLY kappa           {kappa, pi, 2}",
               [(KAPPA_GERM_KEY, 1), ("pi", 1), ("2", 1)], False)
        report(a, "3b. ONLY kappa, one free {kappa, pi}", [(KAPPA_GERM_KEY, 1), ("pi", 1)], False)
        v_pass = report(a, "4. BOTH + exactly ONE free  {3, kappa, pi}",
                        [("3", 1), (KAPPA_GERM_KEY, 1), ("pi", 1)], True)
        report(a, "4b. BOTH + TWO free     {3, kappa, pi, 2}",
               [("3", 1), (KAPPA_GERM_KEY, 1), ("pi", 1), ("2", 1)], False)

        # ---- the retired GR+FRW pair must now FAIL --------------------------------------------
        report(a, "5. retired pair {3, sqrt(8pi/3), pi} (sqrt(8pi/3) now FREE)",
               [("3", 1), ("sqrt(8pi/3)", 1), ("pi", 1)], False)

        # ---- THE IMPOSTOR TEST: same VALUE via 2^(-1), must NOT get kappa's credit -------------
        _banner("PART 2b. THE IMPOSTOR TEST -- is kappa reachable as 2^(-1) for Gate-B credit?")
        v_imp = report(a, "6. {3, 2^(-1), pi}  == same value as case 4",
                       [("3", 1), ("2", -1), ("pi", 1)], False)
        _check(v_pass == v_imp,
               f"the impostor has the IDENTICAL value: {mp.nstr(v_pass, 25)} == {mp.nstr(v_imp, 25)} "
               f"(diff {mp.nstr(abs(v_pass - v_imp), 5)})")
        print("          => same VALUE, opposite Gate-B verdict: the gate credits the germ KEY")
        print("             (exhaust.gate_candidate_for loops over set(node.leaf_consts()) and calls")
        print("             _germ_provenance on the germ's BASE value, never on germ^exponent),")
        print("             so 2^(-1) stays a FREE parameter. GATE B STILL BINDS.")

        # also the half-exponent route, for completeness
        v_h1 = report(a, "6b. {3, kappa^(1/2), pi}", [("3", 1), (KAPPA_GERM_KEY, 0.5), ("pi", 1)], True)
        v_h2 = report(a, "6c. {3, 2^(-1/2), pi}  == same value as 6b",
                      [("3", 1), ("2", -0.5), ("pi", 1)], False)
        _check(v_h1 == v_h2, f"half-exponent impostor also value-identical "
                             f"({mp.nstr(v_h1, 22)} == {mp.nstr(v_h2, 22)})")

    # ==========================================================================================
    # PART 3 -- the switch really switches: the SAME expression flips verdict between modes.
    # ==========================================================================================
    _banner("PART 3. the switch is a genuinely different search (same expression, opposite verdict)")
    dec_pub = [("3", 1), ("sqrt(8pi/3)", 1), ("pi", 1)]
    with forced_pair(mode="published"):
        a = EX.build_alphabet(None, None)
        p_pub_in_pub, _, _, _, _ = run_gate(a, build_expr(a, dec_pub))
        p_kap_in_pub, _, _, _, _ = run_gate(
            a, build_expr(a, [("3", 1), ("flv_koide_cos2_angle", 1), ("pi", 1)]))
    with forced_pair(mode="kappa"):
        a = EX.build_alphabet(None, None)
        p_pub_in_kap, _, _, _, _ = run_gate(a, build_expr(a, dec_pub))
        p_kap_in_kap, _, _, _, _ = run_gate(
            a, build_expr(a, [("3", 1), (KAPPA_GERM_KEY, 1), ("pi", 1)]))
    print(f"  expression {{3, sqrt(8pi/3), pi}}  : published mode Gate B = {p_pub_in_pub} | "
          f"kappa mode = {p_pub_in_kap}")
    print(f"  expression {{3, 1/2, pi}}          : published mode Gate B = {p_kap_in_pub} | "
          f"kappa mode = {p_kap_in_kap}")
    _check(p_pub_in_pub and not p_pub_in_kap, "the GR+FRW pair passes ONLY in published mode")
    _check(p_kap_in_kap and not p_kap_in_pub, "the {3, kappa} pair passes ONLY in kappa mode")

    _banner("VERDICT")
    if _ok:
        print("  GATE B BINDS UNDER THE NEW PAIR.")
        print("  - an expression with NEITHER forced germ FAILS")
        print("  - with ONLY 3 FAILS (1 forced provenance -> not overdetermined)")
        print("  - with ONLY kappa FAILS (same reason)")
        print("  - with BOTH + exactly one free germ PASSES")
        print("  - the value-identical impostor 2^(-1) FAILS -> credit is by germ KEY, not by VALUE")
        print("  So the {3, kappa} re-run is a REAL search, not a relabel of the published one.")
    else:
        print("  ** SOME EXPECTATION FAILED -- read the FAIL lines above before running anything **")
    print("=" * 100)
    return 0 if _ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
