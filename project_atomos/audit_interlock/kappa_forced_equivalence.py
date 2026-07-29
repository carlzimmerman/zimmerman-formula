#!/usr/bin/env python3
"""kappa_forced_equivalence.py -- would FORCING kappa change the atomos null?

THE QUESTION. mi_kappa_spectral_reduction_2026 proved a0 = kappa c sqrt(G rho_Lambda) exactly,
so the framework's OWN distinctive number is kappa = 1/2, while the germ actually forced by the
search, sqrt(8pi/3), is Einstein's 8pi times Friedmann's 1/3 (GR + FRW). Natural request: re-run
the whole search with kappa in the FORCED set instead, since that is the framework's real input.

BEFORE burning the compute, check whether it could possibly change anything. Two facts from
engine/alphabet.py:
    line 110:  Const("kappa", "kap", 0.5, DIMENSIONLESS, "germ", Rational(1,2))   <- kappa IS a germ
    line  93:  Const("2",     "2",   2,   DIMENSIONLESS, "germ", Integer(2))      <- so is 2
and the germ-decorate step is  node (MUL|DIV) germ^e  with e in {1, 1/2, -1, -1/2}.

So "MUL by kappa" and "DIV by 2" are THE SAME VALUE OPERATION. Since the pipeline deduplicates
by VALUE (grind sweeps the deduped values array), forcing kappa can only relabel which
expressions satisfy Gate B -- it cannot add a single new value. This script tests that claim
instead of asserting it, and reports either way. If the value sets DIFFER, a full re-run is
warranted and this script says so.

Exit 0 = all checks ran. No hard-coded verdicts.
"""
from __future__ import annotations
import itertools
import os
import sys

import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

mp.mp.dps = 40

ok = True
def check(cond, msg):
    global ok
    if not cond:
        ok = False
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")
    return cond

def banner(s):
    print("\n" + "=" * 96); print(s); print("=" * 96)


def main() -> int:
    banner("kappa_forced_equivalence -- can forcing kappa change the reachable VALUE set?")

    from engine import alphabet as AL
    germs = {g.key: g for g in AL._geometry_germs()}
    print(f"  germ pool size: {len(germs)}")
    for k in ("kappa", "2", "3", "kernel", "Z", "8pi"):
        g = germs.get(k)
        print(f"    {k:<8} value = {mp.nstr(g.value, 20) if g else 'ABSENT'}")

    # -----------------------------------------------------------------------------------
    banner("S1. kappa is EXACTLY the germ 2 inverted")
    kap = germs["kappa"].value
    two = germs["2"].value
    check(kap == mp.mpf("0.5"), f"kappa germ = 1/2 exactly ({mp.nstr(kap,20)})")
    check(kap == 1 / two, f"kappa == 1/2 == 2^(-1) exactly (diff "
                          f"{mp.nstr(abs(kap - 1/two), 5)})")
    print("  The germ-decorate step is  node (MUL|DIV) germ^e,  e in {1, 1/2, -1, -1/2}.")
    print("  So:  x MUL kappa^1   ==   x DIV 2^1   as a VALUE operation.")
    print("  And: x MUL kappa^1/2 ==   x DIV 2^1/2 as a VALUE operation.")
    for e in (mp.mpf(1), mp.mpf("0.5")):
        lhs = kap ** e          # MUL by kappa^e
        rhs = two ** (-e)       # DIV by 2^e
        check(lhs == rhs, f"kappa^{mp.nstr(e,3)} == 2^(-{mp.nstr(e,3)}) exactly")

    # -----------------------------------------------------------------------------------
    banner("S2. Enumerate the germ-factor MULTISETS reachable with each forced set")
    # A germ decoration contributes a product of germ^(signed e). What matters for the VALUE
    # is the multiset of signed exponents applied to each germ VALUE. Build the set of
    # achievable germ-factor values at up to N decorate steps, under each forced-set rule.
    SIGNED = [mp.mpf(1), mp.mpf("0.5"), mp.mpf(-1), mp.mpf("-0.5")]
    NSTEP = 3          # the committed base is 3 germ steps (2 forced + 1 free)

    def reachable(forced_keys, free_keys, nstep=NSTEP):
        """set of achievable germ-factor VALUES using exactly nstep decorations, where every
        forced key must appear at least once and exactly one distinct free key is used."""
        vals = set()
        pool_forced = [germs[k].value for k in forced_keys]
        for free in free_keys:
            fv = germs[free].value
            keys = pool_forced + [fv]
            # assign each of nstep steps a (key, signed exponent); require all forced present
            for assign in itertools.product(range(len(keys)), repeat=nstep):
                if not all(i in assign for i in range(len(pool_forced))):
                    continue
                for exps in itertools.product(SIGNED, repeat=nstep):
                    v = mp.mpf(1)
                    for idx, e in zip(assign, exps):
                        v *= keys[idx] ** e
                    vals.add(mp.nstr(v, 25))
        return vals

    FREE = [k for k in germs if k not in ("3",)]
    A_forced = ("3", "kernel")      # as published: {3, sqrt(8pi/3)}
    B_forced = ("3", "kappa")       # the requested re-run: {3, kappa}

    print(f"  forced set A (published) = {A_forced}")
    print(f"  forced set B (requested) = {B_forced}")
    print(f"  free germ candidates: {len(FREE)};  decorate steps: {NSTEP}")
    setA = reachable(A_forced, FREE)
    setB = reachable(B_forced, FREE)
    print(f"\n  distinct germ-factor values, forced A: {len(setA):,}")
    print(f"  distinct germ-factor values, forced B: {len(setB):,}")
    onlyA = setA - setB
    onlyB = setB - setA
    print(f"  reachable ONLY under A: {len(onlyA):,}")
    print(f"  reachable ONLY under B: {len(onlyB):,}")
    inter = len(setA & setB)
    print(f"  shared: {inter:,}  ({100*inter/max(len(setA|setB),1):.2f}% of the union)")

    # -----------------------------------------------------------------------------------
    banner("S3. The decisive question: does B add anything A could not reach?")
    if not onlyB:
        print("  NO. Every germ-factor value reachable with kappa FORCED is already reachable")
        print("  with the published forced set. Forcing kappa adds ZERO new values.")
    else:
        print(f"  YES -- {len(onlyB):,} values are reachable only with kappa forced.")
        print("  Sample:")
        for v in list(onlyB)[:8]:
            print("   ", v)
    check(True, "comparison completed (result reported either way)")

    # -----------------------------------------------------------------------------------
    banner("VERDICT")
    if not onlyB:
        print("  FORCING kappa CANNOT CHANGE THE NULL. kappa = 1/2 is value-identical to the")
        print("  germ 2 used with DIV, both germs are in the pool, and the pipeline dedups by")
        print("  VALUE -- so the 42,534,139 distinct values already contain everything kappa")
        print("  can build. A re-run would reproduce the same value set and the same zero")
        print("  certified, changing only which expressions are LABELLED Gate-B-passing.")
        print("\n  IMPORTANT CONSEQUENCE, and it runs in the framework's favour as a matter of")
        print("  COVERAGE: the published null ALREADY tested the framework's own distinctive")
        print("  number. kappa = 1/2 was always inside the search space -- as the explicit")
        print("  `kappa` germ AND as 2^(-1) -- so the null is MORE relevant to the framework")
        print("  than the paper claimed, not less. There is no unexplored corner here.")
        print("\n  What is still true: the null says SM constants are not reachable from this")
        print("  vocabulary. It does NOT test the framework's physics, and it neither supports")
        print("  nor damages a0's value.")
    else:
        print("  A RE-RUN IS WARRANTED. Forcing kappa opens values the published search could")
        print("  not reach, so the null does not cover the framework's own number and the full")
        print("  depth 3-10 sweep should be repeated with forced = {3, kappa}.")
    print("=" * 96)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
