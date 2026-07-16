#!/usr/bin/env python3
"""
overnight_pair_search.py — the GERM-PAIR forced-interlock overnight search.

WHAT THIS IS (Carl's brief, 2026-07-07)
    The single-germ vocabulary was EXHAUSTED (~80 s, clean null, commit b7f1f75): every one of the
    27 candidate forced germs, injected alone across depths {5,6,7} x 21 SM targets, is FDR-DEAD
    (everything collapses to the same Koide-2/3 near-miss). Depths 3-7 over the committed forced
    vocabulary {3, sqrt(8pi/3)} are also committed clean nulls.

    THIS runner tests the last genuinely-untested large compute space: whether any PAIR of candidate
    forced germs (two pre-registered symmetry invariants, e.g. A4_irrep3 x S3_order) JOINTLY produces
    a certified overdetermined interlock — a real 2-symmetry hypothesis that a single germ cannot
    express. 351 pairs = C(27,2), x depths {5,6,7}, x 21 targets -> 1053 configs, ~13 h/pass.

    THE HONEST PRIOR IS STRONGLY NULL. A pair faces a x351-HIGHER FDR bar (the look-elsewhere mult
    grows by the pair count, ~+8.4 bits harsher than the single-germ mult), and every near-miss still
    collapses to the same FDR-DEAD Koide 2/3. This is honest due diligence, NOT a promise of a hit.
    A clean null is the expected, valid outcome.

RULE 3 (verbatim reuse). gate/ engine/ exhaust.py exhaust_parallel.py exhaust_depth*_forced.py and
    overnight_vocab_search.py are IMPORTED UNMODIFIED. This file only:
      * iterates PAIRS instead of singles (itertools.combinations of the 27 candidate germs);
      * registers BOTH germs of a pair (each with its law) into a COPY of FORCED_CONSTRAINTS via a
        pair context manager (extends candidate_registered's refuse-overwrite/restore semantics);
      * folds the FULL PAIR multiplicity mult = n_targets x n_PAIRS x sum_depth(n_recipes) into the
        gate's n_targets_searched (the #1 anti-fabrication invariant — the x n_pairs factor is
        load-bearing; omitting it is the fabrication bug this file's self-check forbids);
      * builds the depth-{5,6,7} reachable sets ONCE (germ-value-independent, same 25-germ pool) and
        REUSES them across all 351 pairs (only Gate-B credit changes per pair);
      * bounds memory (all three depth reach-lists held ~1.6 GB, measured) with a HARD < 4 GB RSS
        watchdog, and logs one structured line PER (pair, depth) level, flushed+fsynced.

WHY ADDING A PAIR CANNOT CHEAT THE GATE (the core of the design)
  * Gate B (forced_kernel) grants forced credit ONLY via a registered law AND requires
    OVERDETERMINATION (>=2 DISTINCT forced provenance keys present). A pair supplies up to 4 forced
    appearances (2 injected + base {3, sqrt(8pi/3)}), so it CAN overdetermine — but a lone appearance
    is still "a definition, not a kernel". CERTIFIED iff Gate A & B & C all pass. Else FDR-DEAD /
    REAL-PUZZLE-RE-LABELED, honestly.
  * Gate A (fdr) folds the ENTIRE search into the look-elsewhere multiplicity. Trying MORE pairs
    RAISES the bar: a hit must clear PASS_BITS=10 surplus bits AFTER dividing by
    n_targets x n_PAIRS x sum_depth(n_recipes). Volume cannot buy a certification.
  * The germ POOL stays FIXED at 25 (assert len(alpha.germs)==25). Candidate germs are ALREADY in
    the 25-germ FDR library (build_value_set); injection changes only Gate-B CREDIT, not the FDR
    density library. germ_pool == 25 is asserted.

CLI
    python3 overnight_pair_search.py --list-pairs          # list the 351 candidate pairs
    python3 overnight_pair_search.py --self-check          # depthN completeness+soundness+a0, halt-on-fail
    python3 overnight_pair_search.py --dry-run             # print the FULL pair mult + -log2 bits + RSS
    python3 overnight_pair_search.py --injected-positive   # detector control: overdet pair CERTIFIES,
                                                           #   single-appearance version dies FDR-DEAD
    python3 overnight_pair_search.py --max-configs 12      # short smoke over a few pairs x depths 5/6/7
    python3 overnight_pair_search.py --hours 13            # the genuine overnight pass (ONE forward pass)
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

# --- RULE 3: import the gate, engine, committed machinery, and the single-germ runner VERBATIM ---
import gate.registry as REG                                   # noqa: E402  (we COPY, never mutate)
import exhaust as EX                                          # noqa: E402
from exhaust import build_alphabet, Alphabet, Reachable       # noqa: E402
from exhaust_parallel import sm_target_keys                   # noqa: E402  (the canonical 21 targets)
from engine.scoring import score_value, measurement_tol       # noqa: E402
from engine.expr_tree import ExprNode, OpType                 # noqa: E402
from gate import validate                                     # noqa: E402

# The committed depth-{5,6,7} constructive builder (depth-parametric signature).
import exhaust_depthN_forced as DN                            # noqa: E402
from exhaust_depthN_forced import (                           # noqa: E402
    constructive_gate_b_reachables,
    constructive_completeness_selfcheck, soundness_selfcheck, a0_validity_depthN,
    _leaf_node, _decorate,
)

# The single-germ runner: reuse its candidate list, watchdog, per-level-log pattern, BestHit, and the
# score_config streamer VERBATIM (RULE 3 — we do NOT modify it; we import its helpers).
import overnight_vocab_search as VOCAB                        # noqa: E402
from overnight_vocab_search import (                          # noqa: E402
    CandidateGerm, candidate_germs,
    _total_rss_mb, _mem_watchdog, HARD_MEM_CAP_GB,
    BestHit, score_config,
)

DEPTHS = [5, 6, 7]

RESULTS = _HERE / "results_overnight_pairs"
RESULTS.mkdir(exist_ok=True)


# ===========================================================================
# 1. PAIR REGISTRATION  (inject BOTH germs, each with its law, into a COPY of the forced registry)
#
#    Extends overnight_vocab_search.candidate_registered's semantics to a PAIR: snapshot the real
#    FORCED_CONSTRAINTS once, add BOTH candidate keys (refuse-overwrite each — a candidate key that
#    collides with a base forced key is SKIPPED, never overwritten, matching the single-germ refusal),
#    restore the exact original dict on exit. RULE 3: patches the SAME dict object exhaust._germ_
#    provenance iterates by reference; touches NO gate threshold.
# ===========================================================================

class candidate_pair_registered:
    """Context manager: temporarily register BOTH germs of a pair (each key,value,law) in the forced
    registry, restoring the exact original dict on exit. Refuses to overwrite any existing key."""

    def __init__(self, cg1: CandidateGerm, cg2: CandidateGerm):
        self.cgs = (cg1, cg2)
        self._orig: Optional[dict] = None

    def __enter__(self):
        self._orig = dict(REG.FORCED_CONSTRAINTS)   # shallow snapshot of the REAL registry
        for cg in self.cgs:
            if cg.key not in REG.FORCED_CONSTRAINTS:            # refuse-overwrite (single-germ semantics)
                REG.FORCED_CONSTRAINTS[cg.key] = dict(
                    value=cg.value, desc=f"[candidate] {cg.source}", law=cg.law)
        return self

    def __exit__(self, *exc):
        REG.FORCED_CONSTRAINTS.clear()
        REG.FORCED_CONSTRAINTS.update(self._orig)
        return False


def candidate_pairs() -> List[Tuple[CandidateGerm, CandidateGerm]]:
    """The FIXED set of C(27,2)=351 unordered candidate germ pairs (declared BEFORE running)."""
    return list(itertools.combinations(candidate_germs(), 2))


# ===========================================================================
# 2. THE FULL PAIR-MULTIPLICITY  (the #1 anti-fabrication invariant)
#
#    mult = n_targets x n_PAIRS x sum_over_depths(n_recipes_at_depth)  — EVERY (target, pair, depth,
#    expression) trial the whole overnight run performs. The x n_PAIRS factor is LOAD-BEARING: trying
#    more pairs RAISES the bar. Folding only n_targets (or n_targets x depths without pairs) is the
#    FABRICATION BUG; _assert_full_pair_multiplicity below asserts the exact product and aborts if
#    it is ever wrong.
#
#    Threads into the gate via EX.gate_candidate_for(..., n_targets_searched=mult) (exhaust.py:536),
#    which sets SearchSpace.n_targets_searched, consumed at gate/fdr.py:150 (mult=max(1,...)) and
#    penalized bits = surplus - log2(mult).
# ===========================================================================

def full_multiplicity_pairs(n_targets: int, n_pairs: int, depths: List[int],
                            n_recipes_by_depth: Dict[int, int]) -> int:
    """mult = n_targets x n_pairs x sum_depth(n_recipes). Every (target, pair, depth, expression)
    trial in the whole night is counted exactly once. The x n_pairs factor is load-bearing."""
    total_recipes = sum(int(n_recipes_by_depth.get(d, 0)) for d in depths)
    return max(1, n_targets * n_pairs * total_recipes)


def _assert_full_pair_multiplicity(mult: int, n_targets: int, n_pairs: int,
                                   depths: List[int], n_recipes_by_depth: Dict[int, int]):
    """The anti-fabrication trip-wire: the mult MUST equal n_targets x n_pairs x sum(recipes)
    EXACTLY. If it folds only n_targets, or omits n_pairs, this HALTS the run (that is the bug the
    brief warns about)."""
    total_recipes = sum(int(n_recipes_by_depth.get(d, 0)) for d in depths)
    expected = n_targets * n_pairs * total_recipes
    if n_pairs != 351:
        raise SystemExit(f"FABRICATION GUARD: n_pairs={n_pairs} != C(27,2)=351 — the pair count is "
                         f"wrong, so the look-elsewhere bar is wrong. HALT.")
    if mult != expected:
        raise SystemExit(
            f"FABRICATION GUARD: fdr_mult={mult} != n_targets x n_pairs x sum(recipes) = "
            f"{n_targets} x {n_pairs} x {total_recipes} = {expected}. The FULL pair multiplicity is "
            f"NOT folded into the look-elsewhere — a hit under this mult would be FABRICATED. HALT.")


# ===========================================================================
# 3. DEPTH-{5,6,7} REACH-BUILD  (reuse depthN's depth-parametric constructive builder VERBATIM)
#
#    CORRECTNESS FLAG (from the brief): the single-germ runner's build_reach_for_depth called
#    D5.constructive_gate_b_reachables(alpha, max_depth=.., dimensionless_only=True). The depthN
#    builder has a DIFFERENT signature — constructive_gate_b_reachables(alpha, depth, value_cap) —
#    positional `depth`, NO dimensionless_only kwarg. We call the depthN one so depths 6/7 work.
# ===========================================================================

def build_reach_for_depth(alpha: Alphabet, depth: int,
                          value_cap: Optional[int] = None) -> Tuple[List[Reachable], int]:
    """Build the constructive Gate-B-passable dimensionless reachable set at `depth` ONCE (streamed,
    value-deduped) via the depthN depth-parametric builder. Returns (reach, n_recipes)."""
    reach, counts = constructive_gate_b_reachables(alpha, depth=depth, value_cap=value_cap)
    return reach, int(counts.get("distinct_by_value", len(reach)))


# ===========================================================================
# 4. PER-LEVEL LOGGING  (Carl's explicit ask: "log at each level" = one line per (pair, depth))
# ===========================================================================

def _log_paths(stamp: str) -> Tuple[Path, Path, Path]:
    return (RESULTS / f"pair_search_{stamp}.jsonl",
            RESULTS / f"pair_search_{stamp}.summary.txt",
            RESULTS / f"pair_search_{stamp}.header.json")


def append_level_log(jsonl: Path, summary: Path, row: dict):
    with jsonl.open("a") as f:
        f.write(json.dumps(row, default=str) + "\n")
        f.flush()
        os.fsync(f.fileno())
    b = row["best"]
    line = (f"[{row['counter']:04d}] {row['germ1_key']}+{row['germ2_key']} d={row['depth']} "
            f"ntgt={row['n_targets']} recipes={row['n_recipes']:>6} "
            f"best={b['target']}:{b['status']} rel_err={b['rel_err']:.2e} "
            f"FDRbits={b['fdr_bits']:+.1f} gateAsurplus={row['gate_A_surplus_bits']:+.1f} "
            f"mult={row['fdr_mult']:.3e} CERTcum={row['certified_cumulative']} "
            f"t={row['elapsed_s']:.0f}s peakRSS={row['peak_rss_gb']:.2f}GB")
    with summary.open("a") as f:
        f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())
    print(line)


# ===========================================================================
# 5. THE --hours SINGLE-PASS OVERNIGHT LOOP  (ONE genuine forward pass, NO re-confirmation re-loop)
# ===========================================================================

def run_overnight(hours: float, max_configs: Optional[int] = None, verbose_targets: bool = True):
    stamp = time.strftime("%Y%m%dT%H%M%S")
    jsonl, summary, headerf = _log_paths(stamp)
    t0 = time.time()
    deadline = t0 + hours * 3600.0

    targets = sm_target_keys()
    n_targets = len(targets)
    germs = candidate_germs()
    assert len(germs) == 27, (f"committed candidate-germ count changed: got {len(germs)}, expected "
                              f"27 (the brief's count). ABORT — re-audit the vocabulary before a run.")
    pairs = candidate_pairs()
    n_pairs = len(pairs)
    assert n_pairs == math.comb(len(germs), 2) == 351

    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25, f"FDR non-smuggle: germ pool must be 25, got {len(alpha.germs)}"
    _mem_watchdog("startup")

    # Build each depth's reachable set ONCE (target- AND pair-independent, same 25-germ pool) for the
    # recipe counts + reuse across all 351 pairs. All three held simultaneously (~1.6 GB measured).
    reach_by_depth: Dict[int, List[Reachable]] = {}
    n_recipes_by_depth: Dict[int, int] = {}
    for d in DEPTHS:
        reach_by_depth[d], n_recipes_by_depth[d] = build_reach_for_depth(alpha, d)
        _mem_watchdog(f"build-depth-{d}")
        print(f"[built depth {d}: {n_recipes_by_depth[d]:,} recipes; "
              f"peakRSS={_total_rss_mb()/1024:.2f}GB]")

    mult = full_multiplicity_pairs(n_targets, n_pairs, DEPTHS, n_recipes_by_depth)
    _assert_full_pair_multiplicity(mult, n_targets, n_pairs, DEPTHS, n_recipes_by_depth)

    header = {
        "run_started": stamp, "hours": hours, "n_targets": n_targets, "n_candidate_germs": len(germs),
        "n_pairs": n_pairs, "depths": DEPTHS, "n_recipes_by_depth": n_recipes_by_depth,
        "fdr_full_multiplicity": mult,
        "fdr_mult_formula": "21 x 351 x sum_depth(recipes) "
                            f"= {n_targets} x {n_pairs} x {sum(n_recipes_by_depth.values())}",
        "fdr_look_elsewhere_bits": math.log2(mult),
        "germ_pool_size": len(alpha.germs), "fdr_uses_full_library": len(alpha.germs) == 25,
        "n_configs_full_pass": n_pairs * len(DEPTHS), "max_configs": max_configs,
        "prior": "STRONGLY NULL. Pairs face a x351-higher FDR bar; every near-miss collapses to the "
                 "same FDR-DEAD Koide 2/3. A clean null is the expected outcome. Any CERTIFIED line is "
                 "a CANDIDATE-NEEDING-SCRUTINY logged for human verification — NOT a TOE, NOT auto-trusted.",
    }
    with headerf.open("w") as f:
        json.dump(header, f, indent=2, default=str)
    with summary.open("a") as f:
        f.write(f"# overnight_pair_search {stamp}  FULL-PAIR-mult={mult:.4e}  "
                f"({header['fdr_mult_formula']})  -log2={math.log2(mult):.1f} bits\n")
        f.write(f"# {n_pairs} pairs x {len(DEPTHS)} depths = {n_pairs*len(DEPTHS)} configs; "
                f"targets={n_targets}; germ_pool={len(alpha.germs)}\n")
        f.write(f"# PRIOR: {header['prior']}\n")

    certified_cumulative = 0
    counter = 0
    completed_full_pass = True

    # SINGLE genuine forward pass over the 351 pairs x 3 depths (NO re-confirmation re-loop). The
    # deadline stops it mid-pass and finalizes cleanly; it does NOT re-loop to burn remaining time.
    for (cg1, cg2) in pairs:
        for d in DEPTHS:
            if time.time() > deadline:
                print(f"[deadline reached at pair={cg1.key}+{cg2.key} depth={d}; stopping cleanly]")
                completed_full_pass = False
                _finalize(summary, t0, certified_cumulative, counter, n_pairs * len(DEPTHS),
                          completed_full_pass)
                return
            if max_configs is not None and counter >= max_configs:
                print(f"[--max-configs {max_configs} reached; stopping smoke cleanly]")
                completed_full_pass = False
                _finalize(summary, t0, certified_cumulative, counter, n_pairs * len(DEPTHS),
                          completed_full_pass)
                return
            counter += 1
            reach = reach_by_depth[d]
            with candidate_pair_registered(cg1, cg2):
                # Under this pair's registry, forced credit is decided inside gate_candidate_for ->
                # _germ_provenance; the constructive reach is germ-value-independent (same 25-germ
                # pool), so we REUSE it verbatim and let the GATE decide credit under the pair.
                best, n_cert, n_relabel = score_config(alpha, reach, targets, mult)
            certified_cumulative += n_cert
            _mem_watchdog(f"config pair={cg1.key}+{cg2.key} d={d}")
            # Gate-A surplus bits AFTER the full pair-multiplicity look-elsewhere (the honest number).
            gate_a_surplus = best.fdr_bits if best.fdr_bits == best.fdr_bits else float("nan")
            row = {
                "counter": counter, "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "germ1_key": cg1.key, "germ2_key": cg2.key,
                "germ1_law": cg1.law, "germ2_law": cg2.law,
                "germ1_value": cg1.value, "germ2_value": cg2.value,
                "depth": d, "n_targets": n_targets, "n_pairs": n_pairs,
                "n_recipes": len(reach), "fdr_mult": mult,
                "best": best.as_dict(),
                "gate_A_surplus_bits": gate_a_surplus,
                "n_certified_this_config": n_cert, "n_relabeled_this_config": n_relabel,
                "certified_cumulative": certified_cumulative,
                "elapsed_s": time.time() - t0, "peak_rss_gb": _total_rss_mb() / 1024.0,
            }
            append_level_log(jsonl, summary, row)

    _finalize(summary, t0, certified_cumulative, counter, n_pairs * len(DEPTHS), completed_full_pass)


def _finalize(summary: Path, t0: float, certified_cumulative: int, counter: int,
              n_configs_full: int, completed_full_pass: bool):
    if certified_cumulative == 0:
        verdict = "CLEAN NULL (expected)"
    else:
        verdict = (f"{certified_cumulative} CERTIFIED CANDIDATE(S) — CANDIDATE-NEEDING-SCRUTINY, "
                   f"logged for human verification, NOT a TOE, NOT auto-trusted")
    pass_state = ("FULL PASS COMPLETED" if completed_full_pass
                  else f"PARTIAL ({counter}/{n_configs_full} configs before stop)")
    line = (f"# DONE  elapsed={time.time()-t0:.0f}s  {pass_state}  "
            f"peakRSS={_total_rss_mb()/1024:.2f}GB  CERTIFIED_total={certified_cumulative}  "
            f"-> {verdict}")
    with summary.open("a") as f:
        f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())
    print(line)


# ===========================================================================
# 6. INJECTED-POSITIVE CONTROL  (the detector works; volume/pairs cannot cheat)
#
#    Build a SYNTHETIC candidate whose coefficient is a genuine 2-forced-appearance kernel with
#    exactly one free O(1) param, tying >=3 measured constants -> A & B & C all pass -> CERTIFIED,
#    EVEN under the full ~4.6e9 pair mult (a real overdetermined signal clears the bar). Then the
#    SAME structure with only ONE forced appearance must die FDR-DEAD @ Gate B (not overdetermined) —
#    proving a lone appearance / volume cannot manufacture a certification.
# ===========================================================================

def _synthetic_pdg_target(value: float, rel: float = 1e-4):
    """A minimal PDG-like target shim (value, sigma, rel_precision, n_digits) for the control."""
    class _T:
        pass
    t = _T()
    t.value = float(value)
    t.sigma = float(value) * rel
    t.rel_precision = rel
    t.n_digits = 6
    return t


def injected_positive_control(verbose: bool = True) -> dict:
    """Detector control. Two synthetic candidates built through the REAL gate pipeline:

    (POS) OVERDETERMINED: coefficient = (einstein_8pi) x (friedmann_third) x (one free O(1)), i.e.
          TWO distinct forced provenance keys (two independent forced appearances) + exactly one free
          germ, tying >=3 measured constants. Under the FULL pair mult, a genuinely surprising value
          must still CERTIFY (A & B & C pass) — the detector fires on a real overdetermined signal.
    (NEG) SINGLE-APPEARANCE: the SAME value/structure but only ONE forced provenance key present ->
          not overdetermined -> Gate B FAILS -> FDR-DEAD. Volume/pairs cannot cheat overdetermination.
    """
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25
    # a comfortably-large mult (>= the real pair mult) so the control proves the bar is cleared for real.
    mult = 21 * 351 * 700000

    leaves = alpha.leaves
    # pick 3 distinct measured leaves whose product with the forced kernel lands somewhere sparse.
    m = leaves[:3]

    def _build_node(forced_keys: List[str]):
        # node = m0 * m1 * m2, decorated by each forced key^1 and one free germ^1.
        node = _leaf_node(m[0])
        for k in m[1:]:
            node = ExprNode(OpType.MUL, children=[node, _leaf_node(k)])
        for fk in forced_keys:
            node = _decorate(node, OpType.MUL, fk, 1)
        # one free O(1) germ (provenance None) -> exactly one free param.
        free = next(g for g in alpha.germs
                    if EX._germ_provenance(float(alpha.value(g))) is None and g not in forced_keys)
        node = _decorate(node, OpType.MUL, free, 1)
        return node

    # forced germ KEYS in the pool that carry DISTINCT registry provenance (einstein/friedmann/3/kernel).
    # Use the two Friedmann/Einstein factors so provenance keys are DISTINCT and forced (overdetermined).
    def _germ_key_for_value(target_val: float) -> Optional[str]:
        for g in alpha.germs:
            if abs(float(alpha.value(g)) - target_val) / abs(target_val) < 1e-9:
                return g
        return None

    k_3 = _germ_key_for_value(3.0)                       # -> Ngen_3 / A4_dim_3 (forced)
    k_kernel = _germ_key_for_value(math.sqrt(8 * math.pi / 3.0))  # -> a0_kernel_8pi3 (forced)
    if k_3 is None or k_kernel is None:
        raise SystemExit("injected-positive control: could not find the forced germ keys in the pool.")

    # (POS) two DISTINCT forced provenance keys -> overdetermined.
    pos_node = _build_node([k_3, k_kernel])
    pos_val, pos_lab = pos_node.evaluate(alpha)
    pos_target = _synthetic_pdg_target(float(pos_val))
    pos_reach = Reachable(pos_val, pos_lab, pos_node.to_string(alpha),
                          pos_node.canonical_hash(), pos_node)
    pos_gc = EX.gate_candidate_for(pos_reach, alpha, "SYN_POS", pos_target, mult)
    pos_v = validate(pos_gc)

    # (NEG) ONE forced provenance key only -> a definition, not a kernel -> Gate B FAILS.
    neg_node = _build_node([k_3])
    neg_val, neg_lab = neg_node.evaluate(alpha)
    neg_target = _synthetic_pdg_target(float(neg_val))
    neg_reach = Reachable(neg_val, neg_lab, neg_node.to_string(alpha),
                          neg_node.canonical_hash(), neg_node)
    neg_gc = EX.gate_candidate_for(neg_reach, alpha, "SYN_NEG", neg_target, mult)
    neg_v = validate(neg_gc)

    pos_certifies = (pos_v.status == "CERTIFIED")
    neg_fdr_dead = (neg_v.status != "CERTIFIED")
    control_ok = pos_certifies and neg_fdr_dead

    if verbose:
        print("=" * 100)
        print("INJECTED-POSITIVE CONTROL  (detector works; a lone appearance / volume cannot cheat)")
        print("-" * 100)
        print(f"  mult used (>= real pair mult): {mult:.4e}  (-log2 = {math.log2(mult):.1f} bits)")
        print(f"  (POS) overdetermined pair [2 distinct forced provenance keys, 1 free]:")
        print(f"        node: {pos_node.to_string(alpha)}")
        print(f"        gate: [{pos_v.status}]  A.passed={pos_v.fdr.passed}(bits={pos_v.fdr.bits:.1f}) "
              f"B.passed={pos_v.kernel.passed}(appear={pos_v.kernel.n_independent_appearances}) "
              f"C.passed={pos_v.interlock.passed}")
        print(f"        -> CERTIFIES ? {pos_certifies}  (EXPECTED True: real overdetermined signal "
              f"clears the bar)")
        print(f"  (NEG) single-appearance [1 forced provenance key, 1 free]:")
        print(f"        node: {neg_node.to_string(alpha)}")
        print(f"        gate: [{neg_v.status}]  B.passed={neg_v.kernel.passed}"
              f"(appear={neg_v.kernel.n_independent_appearances})  tell={neg_v.tell[:80]}")
        print(f"        -> FDR-DEAD (not CERTIFIED) ? {neg_fdr_dead}  (EXPECTED True: one appearance "
              f"is a definition, not a kernel)")
        print("-" * 100)
        print(f"  CONTROL_OK (POS certifies AND NEG dies) = {control_ok}")
        print("=" * 100)

    return dict(control_ok=control_ok, pos_status=pos_v.status, pos_certifies=pos_certifies,
                pos_bits=float(pos_v.fdr.bits), pos_appearances=pos_v.kernel.n_independent_appearances,
                neg_status=neg_v.status, neg_fdr_dead=neg_fdr_dead,
                neg_appearances=neg_v.kernel.n_independent_appearances, mult=mult)


# ===========================================================================
# 7. CLI HELPERS
# ===========================================================================

def _list_pairs():
    pairs = candidate_pairs()
    print(f"{len(pairs)} CANDIDATE GERM PAIRS  (C(27,2) unordered; each injected with BOTH laws):")
    for i, (a, b) in enumerate(pairs):
        print(f"  [{i:03d}] {a.key:<16} + {b.key:<16}  ({a.value:.4g}, {b.value:.4g})")


def _dry_run():
    targets = sm_target_keys()
    germs = candidate_germs()
    assert len(germs) == 27
    pairs = candidate_pairs()
    n_pairs = len(pairs)
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25
    nrec = {}
    for d in DEPTHS:
        _, nrec[d] = build_reach_for_depth(alpha, d)
        _mem_watchdog(f"dry-run/build-{d}")
        print(f"  depth {d}: recipes={nrec[d]:,}  peakRSS={_total_rss_mb()/1024:.2f}GB")
    mult = full_multiplicity_pairs(len(targets), n_pairs, DEPTHS, nrec)
    _assert_full_pair_multiplicity(mult, len(targets), n_pairs, DEPTHS, nrec)
    print(f"n_targets={len(targets)}  n_candidate_germs={len(germs)}  n_pairs={n_pairs}  depths={DEPTHS}")
    print(f"n_recipes_by_depth={nrec}  (sum={sum(nrec.values()):,})")
    print(f"FULL PAIR look-elsewhere multiplicity mult = {mult:.4e}")
    print(f"  = {len(targets)} x {n_pairs} x {sum(nrec.values())}   (the x{n_pairs} PAIR factor is "
          f"load-bearing)")
    print(f"look-elsewhere penalty on surplus bits = -log2(mult) = {math.log2(mult):.1f} bits "
          f"(vs single-germ ~{math.log2(mult/n_pairs):.1f}; +{math.log2(n_pairs):.1f} from the pairs)")
    print(f"peak RSS so far: {_total_rss_mb()/1024:.2f} GB  (cap {HARD_MEM_CAP_GB} GB)")


def _self_check():
    """depthN completeness + soundness + a0 validity per depth, halt-on-fail (so the null is valid)."""
    for d in DEPTHS:
        print("#" * 100)
        print(f"# SELF-CHECK depth {d}")
        print("#" * 100)
        comp = constructive_completeness_selfcheck(d, verbose=True)
        if not comp["constructive_complete"]:
            raise SystemExit(f"CONSTRUCTIVE-COMPLETENESS FAILED (depth {d}) — null INVALID. HALT.")
        _mem_watchdog(f"self-check/completeness/{d}")
        snd = soundness_selfcheck(d, verbose=True)
        if not snd["soundness_ok"]:
            raise SystemExit(f"SOUNDNESS FAILED (depth {d}) — construction emits non-Gate-B candidates. HALT.")
        _mem_watchdog(f"self-check/soundness/{d}")
        a0 = a0_validity_depthN(d, verbose=True)
        if not a0["a0_ok"]:
            raise SystemExit(f"a0-VALIDITY FAILED (depth {d}) — search BROKEN. HALT.")
        _mem_watchdog(f"self-check/a0/{d}")
    print(f"[self-check ALL depths PASS; peak RSS {_total_rss_mb()/1024:.2f} GB, cap {HARD_MEM_CAP_GB} GB]")


def main():
    ap = argparse.ArgumentParser(description="Overnight GERM-PAIR forced-interlock search "
                                             "(C(27,2)=351 pairs x depths {5,6,7} x 21 SM targets).")
    ap.add_argument("--hours", type=float, default=8.0, help="overnight run length (default 8h)")
    ap.add_argument("--max-configs", type=int, default=None, help="stop after N configs (smoke)")
    ap.add_argument("--list-pairs", action="store_true", help="print the 351 candidate pairs")
    ap.add_argument("--dry-run", action="store_true", help="print the FULL pair FDR multiplicity + bits")
    ap.add_argument("--self-check", action="store_true",
                    help="depthN completeness+soundness+a0 per depth (halt-on-fail)")
    ap.add_argument("--injected-positive", action="store_true",
                    help="detector control: overdet pair CERTIFIES; single-appearance dies FDR-DEAD")
    args = ap.parse_args()

    if args.list_pairs:
        _list_pairs(); return
    if args.dry_run:
        _dry_run(); return
    if args.self_check:
        _self_check(); return
    if args.injected_positive:
        out = injected_positive_control(verbose=True)
        if not out["control_ok"]:
            raise SystemExit(f"INJECTED-POSITIVE CONTROL FAILED: {out} — the detector is broken. HALT.")
        return
    run_overnight(args.hours, max_configs=args.max_configs)


if __name__ == "__main__":
    main()
