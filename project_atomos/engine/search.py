#!/usr/bin/env python3
"""
search.py — depth-stratified enumeration + hard filter + closeness ranking.

PORTED from hali_flow/bruteflow/constrained_search.ConstrainedGrammar +
ConstrainedSearchEngine. Same spine:
  - depth-stratified BNF enumerator (depth 1 = leaves; depth d = unary ops on depth-(d-1) trees
    + binary ops over subtree x subtree + a 'decorate by a dimensionless germ' pass),
  - canonical_hash dedup (G*c tested once),
  - dimension-first -> numeric-second scoring with a HARD filter then relative-error threshold,
  - matches streamed to candidates.jsonl, ranked by error.

ADAPTER CHANGES (ENGINE_REVERSE_ENGINEERING §5):
  - `--filter {dimension, rep, interlock, none}` selects the HARD structural cut that replaces
    is_acceleration() for dimensionless targets (mandatory; for the SM, default is NOT 'none').
    * dimension : keep only trees whose Label matches the target dimension (the a0 filter).
    * rep       : keep only trees with a non-poisoned rep tag (symmetry-multiplet matched).
    * interlock : keep only trees that USE >= min_interlock distinct measured leaves (so the
                  dimensionless freedom is spent on OVER-DETERMINATION, not on a free monomial in
                  one input — the Koide signature: 3 masses tied by 1 relation). This is the
                  manufactured replacement hard filter §4 demands.
    * none      : no structural cut (RAW look-elsewhere; use only to measure how unconstrained
                  the space is — expect the FDR gate to slaughter it).
  - score = closeness penalized by complexity AND by a search-space-size estimate, so the ENGINE
    ITSELF flags 'this match is cheap' (a high local density of reachable values near the target).
    The score is advisory ranking ONLY; the gate, not the score, decides real-vs-coincidence.
  - values at mpmath precision.

The engine RANKS BY CLOSENESS and hands candidates to the gate. It has NO notion of 'interlock'
beyond the optional usage filter; real interlock judgment is 100% downstream in gate/.
"""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Generator, List, Optional, Set

import mpmath as mp

from .expr_tree import ExprNode, OpType, Label
from .alphabet import Alphabet

mp.mp.dps = 40


# =============================================================================
# GRAMMAR  (depth-stratified, canonical-hash dedup) — ported from ConstrainedGrammar
# =============================================================================

class Grammar:
    def __init__(self, alphabet: Alphabet, max_depth: int = 4,
                 use_addition: bool = False, decorate: bool = True):
        self.A = alphabet
        self.max_depth = max_depth
        self.use_addition = use_addition
        self.decorate = decorate
        self.seen_hashes: Set[str] = set()
        # leaf pool = measured leaves + group invariants (forced integers usable as building blocks)
        self.leaf_keys = list(alphabet.leaves) + list(alphabet.groups)
        self.germ_keys = list(alphabet.germs)
        self.exponents = alphabet.exponents

    def generate_all(self) -> Generator[ExprNode, None, None]:
        for depth in range(1, self.max_depth + 1):
            for tree in self._generate_at_depth(depth):
                h = tree.canonical_hash()
                if h not in self.seen_hashes:
                    self.seen_hashes.add(h)
                    yield tree

    def _generate_at_depth(self, depth: int) -> Generator[ExprNode, None, None]:
        if depth == 1:
            for key in self.leaf_keys:
                yield ExprNode(OpType.CONST, const=key)
            return

        subtrees = list(self._generate_up_to_depth(depth - 1))

        # unary ops on depth-(d-1) trees
        for sub in self._generate_at_depth(depth - 1):
            yield ExprNode(OpType.SQRT, children=[sub])
            yield ExprNode(OpType.CBRT, children=[sub])
            yield ExprNode(OpType.INV, children=[sub])
            for e in self.exponents:
                yield ExprNode(OpType.POW, children=[sub], exp=e)

        # binary ops over subtree x subtree (commutative MUL once, DIV both orders)
        for i, left in enumerate(subtrees):
            for right in subtrees[i:]:
                yield ExprNode(OpType.MUL, children=[left, right])
                yield ExprNode(OpType.DIV, children=[left, right])
                if left.canonical_hash() != right.canonical_hash():
                    yield ExprNode(OpType.DIV, children=[right, left])
                if self.use_addition:
                    yield ExprNode(OpType.ADD, children=[left, right])

        # decorate-by-dimensionless-germ pass (keeps leaf set small)
        if self.decorate:
            for sub in self._generate_at_depth(depth - 1):
                for g in self.germ_keys:
                    gnode = ExprNode(OpType.CONST, const=g)
                    yield ExprNode(OpType.MUL, children=[sub, gnode])
                    yield ExprNode(OpType.DIV, children=[sub, gnode])

    def _generate_up_to_depth(self, max_d: int) -> Generator[ExprNode, None, None]:
        for d in range(1, max_d + 1):
            yield from self._generate_at_depth(d)


# =============================================================================
# SEARCH  (hard filter -> rel-error -> closeness rank; complexity+density penalty)
# =============================================================================

@dataclass
class Candidate:
    formula: str
    value: float
    target: float
    rel_error: float           # |val-target|/|target|
    complexity: int
    n_distinct_leaves: int     # how many distinct MEASURED leaves it ties (interlock hint)
    label: str
    score: float = 0.0         # advisory: closeness penalized by complexity + local density
    local_density: float = 0.0 # reachable-value count near target / window  (engine's own 'cheap?' flag)
    canonical: str = ""


class Search:
    def __init__(self, alphabet: Alphabet, target_value, target_label: Optional[Label] = None,
                 tol: float = 0.02, max_depth: int = 4, hard_filter: str = "interlock",
                 min_interlock: int = 3, use_addition: bool = False):
        self.A = alphabet
        self.target = mp.mpf(target_value)
        self.target_label = target_label
        self.tol = tol
        self.max_depth = max_depth
        self.hard_filter = hard_filter
        self.min_interlock = min_interlock
        self.use_addition = use_addition
        # how many distinct MEASURED leaves exist (interlock filter caps at this)
        self.n_measured = len(alphabet.leaves)
        self._reachable: List[float] = []   # all dimensionally/structurally-valid VALUES (for density)

    # --- the hard structural cut that replaces is_acceleration() ---
    def _passes_filter(self, label: Label, distinct_leaves: int) -> bool:
        f = self.hard_filter
        if f == "dimension":
            if self.target_label is None:
                return label.is_dimensionless()
            return label.dims_equal(self.target_label)
        if f == "rep":
            return label.rep_ok()
        if f == "interlock":
            # spend the dimensionless freedom on over-determination: must tie >= min_interlock
            # distinct measured leaves (Koide: 3 masses, 1 relation). Caps at what's available.
            need = min(self.min_interlock, self.n_measured)
            return distinct_leaves >= need
        if f == "none":
            return True
        raise ValueError(f"unknown hard_filter {f!r}")

    def run(self, out_path: Optional[Path] = None, top_k: int = 50,
            max_trees: Optional[int] = None, verbose: bool = True) -> List[Candidate]:
        grammar = Grammar(self.A, max_depth=self.max_depth,
                          use_addition=self.use_addition)
        cands: List[Candidate] = []
        n_gen = n_valid = 0
        measured = set(self.A.leaves)

        for tree in grammar.generate_all():
            if max_trees is not None and n_gen >= max_trees:
                break
            n_gen += 1
            try:
                value, label = tree.evaluate(self.A)
            except Exception:
                continue
            if not _finite_pos(value):
                continue
            distinct_leaves = len(set(tree.leaf_consts()) & measured)
            if not self._passes_filter(label, distinct_leaves):
                continue
            n_valid += 1
            fval = float(value)
            self._reachable.append(fval)
            rel = abs(value - self.target) / abs(self.target)
            if rel < self.tol:
                cands.append(Candidate(
                    formula=tree.to_string(self.A),
                    value=fval,
                    target=float(self.target),
                    rel_error=float(rel),
                    complexity=tree.complexity(),
                    n_distinct_leaves=distinct_leaves,
                    label=str(label),
                    canonical=tree.canonical_hash(),
                ))

        # local density of the reachable set near the target (the engine's own 'is this cheap?')
        local_density = self._local_density(self._reachable, float(self.target), self.tol)
        for c in cands:
            c.local_density = local_density
            c.score = self._score(c, local_density)
        cands.sort(key=lambda c: c.score)  # lower = better (closeness, simplicity, sparsity)

        if verbose:
            print(f"[engine] trees generated: {n_gen:,} | structurally-valid: {n_valid:,} | "
                  f"candidates < {self.tol:.0%}: {len(cands)} | "
                  f"local reachable density near target: {local_density:.3g}")

        cands = cands[:top_k]
        if out_path is not None:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w") as fh:
                for c in cands:
                    fh.write(json.dumps(asdict(c)) + "\n")
        return cands

    # --- score: closeness penalized by complexity AND search-space density ---
    @staticmethod
    def _score(c: Candidate, local_density: float) -> float:
        """Lower is better. Advisory ranking only — NOT a certification.

        bits_fit      ~ how many bits the closeness is worth: -log2(rel_error)  (bigger=closer)
        complexity_pen= each extra node costs ~1 bit of description length (Occam)
        density_pen   = -log2(1/(1+local_density)) ~ how cheap a near-target hit is: if MANY
                        reachable values already sit near the target, the match is unsurprising
                        (this is the engine pre-empting the FDR gate's verdict, advisory only).
        score = complexity_pen + density_pen - bits_fit   (we MINIMIZE)
        """
        rel = max(c.rel_error, 1e-30)
        bits_fit = -math.log2(rel)
        complexity_pen = c.complexity
        density_pen = math.log2(1.0 + local_density)
        return complexity_pen + density_pen - bits_fit

    @staticmethod
    def _local_density(reachable: List[float], target: float, tol: float) -> float:
        """Count reachable values within the match window, normalized to expected-per-window.

        High value => the pool densely covers the target neighborhood => a hit is cheap (the
        engine flags it; the gate quantifies it rigorously in gate/fdr.py)."""
        if not reachable:
            return 0.0
        lo, hi = target * (1 - tol), target * (1 + tol)
        if target < 0:
            lo, hi = hi, lo
        n_hit = sum(1 for v in reachable if lo <= v <= hi)
        return float(n_hit)


def _finite_pos(v) -> bool:
    try:
        return mp.isfinite(v) and v > 0
    except Exception:
        return False
