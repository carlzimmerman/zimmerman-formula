#!/usr/bin/env python3
"""
expr_tree.py — the (value, Label) expression-tree spine.

PORTED VERBATIM IN SHAPE from hali_flow/bruteflow/symbolic_search.py's ExprNode + Dimension,
with three adapter upgrades demanded by notes/ENGINE_REVERSE_ENGINEERING.md §5:

  1. value arithmetic upgraded to mpmath (SM ratios like m_mu/m_e ~ 206.768 need >double
     precision to make FDR tolerances at the 1e-4..1e-6 level meaningful).
  2. `Dimension` generalized to `Label` = (L,M,T physical dimension) + optional discrete-group
     `rep` tag, so a SYMMETRY/REP constraint can prune the way dimension did for a0. For the
     default dimensionless SM targets the L/M/T part is all-zero and `rep` carries the structure.
  3. POW exponent set extended with small rationals {1/2,1/3,1/4,2/3,3/4,...} (in alphabet.py).

The load-bearing design choice kept exactly: EVERY node evaluates to (value, Label) at once, so
the label can prune BEFORE the value is scored. That is what made a0's depth-5 search tractable.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Tuple

import mpmath as mp

mp.mp.dps = 40  # 40 decimal digits — enough for SM ratios + FDR tolerances


# =============================================================================
# LABEL  (generalizes hali_flow's Dimension: physical dim + optional rep tag)
# =============================================================================

@dataclass(frozen=True)
class Label:
    """A structural tag carried alongside a value through the tree.

    L,M,T  : physical-dimension exponents (Length, Mass, Time) — kept so the engine still
             works on a DIMENSIONFUL target (e.g. re-deriving a0, the calibration positive).
    rep    : an optional discrete-group representation/sector tag (string). For SM-ratio /
             angle / coupling targets the default is dimensionless (L=M=T=0) and `rep` is the
             hard filter (e.g. only combine objects from the same flavor multiplet). `None`
             means "no rep constraint" (rep filter is then vacuous, like is_acceleration on a
             dimensionless target — see ENGINE_REVERSE_ENGINEERING §4).

    Arithmetic on L,M,T mirrors hali_flow exactly (add on *, subtract on /, scale on **).
    `rep` composition is conservative: ops that would mix two DIFFERENT non-None reps produce
    a poisoned rep ("MIX") that the rep-filter rejects, so the rep tag prunes like a dimension.
    """
    L: float = 0.0
    M: float = 0.0
    T: float = 0.0
    rep: Optional[str] = None

    # --- physical-dimension algebra (verbatim shape from hali_flow Dimension) ---
    def __mul__(self, other: "Label") -> "Label":
        return Label(self.L + other.L, self.M + other.M, self.T + other.T,
                     _combine_rep(self.rep, other.rep))

    def __truediv__(self, other: "Label") -> "Label":
        return Label(self.L - other.L, self.M - other.M, self.T - other.T,
                     _combine_rep(self.rep, other.rep))

    def __pow__(self, exp: float) -> "Label":
        # raising a multiplet to a power has no clean rep meaning; keep singlet reps, poison others
        new_rep = self.rep if (self.rep is None or self.rep == "singlet") else f"{self.rep}^{exp}"
        return Label(self.L * exp, self.M * exp, self.T * exp, new_rep)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Label):
            return False
        return (abs(self.L - other.L) < 1e-3 and
                abs(self.M - other.M) < 1e-3 and
                abs(self.T - other.T) < 1e-3 and
                self.rep == other.rep)

    def __hash__(self):
        return hash((round(self.L, 3), round(self.M, 3), round(self.T, 3), self.rep))

    # --- dimension predicates (the hard filter on a dimensionful target) ---
    def dims_equal(self, other: "Label") -> bool:
        return (abs(self.L - other.L) < 1e-3 and
                abs(self.M - other.M) < 1e-3 and
                abs(self.T - other.T) < 1e-3)

    def is_dimensionless(self) -> bool:
        return abs(self.L) < 1e-3 and abs(self.M) < 1e-3 and abs(self.T) < 1e-3

    def is_acceleration(self) -> bool:
        return self.dims_equal(ACCELERATION)

    def rep_ok(self) -> bool:
        """A non-poisoned rep (the rep-filter pass condition)."""
        return self.rep != "MIX"

    def __repr__(self):
        parts = []
        if self.L: parts.append(f"L^{self.L:g}")
        if self.M: parts.append(f"M^{self.M:g}")
        if self.T: parts.append(f"T^{self.T:g}")
        dim = " ".join(parts) if parts else "1"
        return dim if self.rep is None else f"{dim}[{self.rep}]"


def _combine_rep(a: Optional[str], b: Optional[str]) -> Optional[str]:
    """Conservative rep composition. None is the identity (no constraint)."""
    if a is None:
        return b
    if b is None:
        return a
    if a == b:
        return a
    if a == "singlet":
        return b
    if b == "singlet":
        return a
    return "MIX"  # mixing two distinct multiplets -> poisoned, rejected by rep filter


DIMENSIONLESS = Label(0, 0, 0)
ACCELERATION = Label(1, 0, -2)  # for the a0 calibration positive


# =============================================================================
# EXPRESSION TREE  (ported from symbolic_search.ExprNode, mpmath values)
# =============================================================================

class OpType(Enum):
    CONST = "const"
    MUL = "*"
    DIV = "/"
    POW = "**"
    SQRT = "sqrt"
    CBRT = "cbrt"
    INV = "1/"
    ADD = "+"      # dim/rep-matched only (kept optional; off by default like hali_flow)
    NEG = "-"


@dataclass
class ExprNode:
    """A node in an expression tree. Leaves = constants; internal nodes = operators.

    `const` is a key into an Alphabet (resolved at evaluate-time). Carrying the key rather than
    the value keeps trees ANONYMIZED-by-structure: canonical_hash() canonicalizes the structure,
    not the physics label, exactly as in hali_flow.
    """
    op: OpType
    const: Optional[str] = None
    children: List["ExprNode"] = field(default_factory=list)
    exp: object = 1.0  # mpmath-friendly exponent for POW (float or mp.mpf)

    def evaluate(self, alpha) -> Tuple[object, Label]:
        """Evaluate to (mpmath value, Label). `alpha` is an Alphabet (provides .value/.label).

        Returns (mp.nan, label) for invalid branches so the caller can prune, matching
        hali_flow's "reject non-finite" contract.
        """
        op = self.op
        if op == OpType.CONST:
            return alpha.value(self.const), alpha.label(self.const)

        if op == OpType.SQRT:
            v, d = self.children[0].evaluate(alpha)
            if v < 0:
                return mp.nan, d ** mp.mpf("0.5")
            return mp.sqrt(v), d ** 0.5

        if op == OpType.CBRT:
            v, d = self.children[0].evaluate(alpha)
            return mp.cbrt(v), d ** (mp.mpf(1) / 3)

        if op == OpType.INV:
            v, d = self.children[0].evaluate(alpha)
            if abs(v) < mp.mpf("1e-100"):
                return mp.nan, d ** -1
            return 1 / v, d ** -1

        if op == OpType.NEG:
            v, d = self.children[0].evaluate(alpha)
            return -v, d

        if op == OpType.MUL:
            v1, d1 = self.children[0].evaluate(alpha)
            v2, d2 = self.children[1].evaluate(alpha)
            return v1 * v2, d1 * d2

        if op == OpType.DIV:
            v1, d1 = self.children[0].evaluate(alpha)
            v2, d2 = self.children[1].evaluate(alpha)
            if abs(v2) < mp.mpf("1e-100"):
                return mp.nan, d1 / d2
            return v1 / v2, d1 / d2

        if op == OpType.ADD:
            v1, d1 = self.children[0].evaluate(alpha)
            v2, d2 = self.children[1].evaluate(alpha)
            if not d1.dims_equal(d2):  # addition requires matching physical dimension
                return mp.nan, DIMENSIONLESS
            return v1 + v2, Label(d1.L, d1.M, d1.T, _combine_rep(d1.rep, d2.rep))

        if op == OpType.POW:
            v1, d1 = self.children[0].evaluate(alpha)
            e = mp.mpf(self.exp)
            if v1 < 0 and (e != int(e)):
                return mp.nan, d1 ** float(e)
            return v1 ** e, d1 ** float(e)

        return mp.nan, DIMENSIONLESS

    # --- string rendering (human-readable, hali_flow shape) ---
    def to_string(self, alpha) -> str:
        op = self.op
        if op == OpType.CONST:
            return alpha.symbol(self.const)
        if op == OpType.SQRT:
            return f"sqrt({self.children[0].to_string(alpha)})"
        if op == OpType.CBRT:
            return f"cbrt({self.children[0].to_string(alpha)})"
        if op == OpType.INV:
            return f"1/({self.children[0].to_string(alpha)})"
        if op == OpType.NEG:
            return f"-({self.children[0].to_string(alpha)})"
        if op == OpType.MUL:
            return f"({self.children[0].to_string(alpha)} * {self.children[1].to_string(alpha)})"
        if op == OpType.DIV:
            return f"({self.children[0].to_string(alpha)} / {self.children[1].to_string(alpha)})"
        if op == OpType.ADD:
            return f"({self.children[0].to_string(alpha)} + {self.children[1].to_string(alpha)})"
        if op == OpType.POW:
            return f"({self.children[0].to_string(alpha)})^{_fmt_exp(self.exp)}"
        return "?"

    def sympy_expr(self, alpha):
        """A sympy expression with the constants kept SYMBOLIC (for the forced-kernel gate).

        Lets gate/forced_kernel.py substitute forced identities (Friedmann, Einstein 8pi, group
        dimensions) into the candidate and test whether the coefficient factors into pre-fit
        pieces — exactly the a0 post-mortem step (ENGINE_REVERSE_ENGINEERING §2 step 5).
        """
        import sympy as sp
        op = self.op
        if op == OpType.CONST:
            return alpha.sym(self.const)
        if op == OpType.SQRT:
            return sp.sqrt(self.children[0].sympy_expr(alpha))
        if op == OpType.CBRT:
            return sp.cbrt(self.children[0].sympy_expr(alpha))
        if op == OpType.INV:
            return 1 / self.children[0].sympy_expr(alpha)
        if op == OpType.NEG:
            return -self.children[0].sympy_expr(alpha)
        if op == OpType.MUL:
            return self.children[0].sympy_expr(alpha) * self.children[1].sympy_expr(alpha)
        if op == OpType.DIV:
            return self.children[0].sympy_expr(alpha) / self.children[1].sympy_expr(alpha)
        if op == OpType.ADD:
            return self.children[0].sympy_expr(alpha) + self.children[1].sympy_expr(alpha)
        if op == OpType.POW:
            return self.children[0].sympy_expr(alpha) ** sp.nsimplify(self.exp)
        raise ValueError(f"bad op {op}")

    def complexity(self) -> int:
        """Node count = expression complexity (used by the score penalty)."""
        if self.op == OpType.CONST:
            return 1
        return 1 + sum(c.complexity() for c in self.children)

    def leaf_consts(self) -> List[str]:
        if self.op == OpType.CONST:
            return [self.const]
        out: List[str] = []
        for c in self.children:
            out.extend(c.leaf_consts())
        return out

    def canonical_hash(self) -> str:
        """Structural canonical hash — the engine's only 'anonymization' (structure, not labels).

        Ported verbatim from symbolic_search.canonical_hash: commutative MUL/ADD sort children,
        POW keys by exponent, others keep child order. Dedups G*c vs c*G.
        """
        if self.op == OpType.CONST:
            return f"C:{self.const}"
        if self.op in (OpType.MUL, OpType.ADD):
            child_hashes = sorted(c.canonical_hash() for c in self.children)
            return f"{self.op.value}:{':'.join(child_hashes)}"
        if self.op == OpType.POW:
            return f"POW:{self.children[0].canonical_hash()}:{_fmt_exp(self.exp)}"
        child_hashes = [c.canonical_hash() for c in self.children]
        return f"{self.op.value}:{':'.join(child_hashes)}"


def _fmt_exp(e) -> str:
    """Stable, readable exponent string (1/2 not 0.5) for hashing + printing."""
    f = float(e)
    table = {0.5: "1/2", 1 / 3: "1/3", 2 / 3: "2/3", 0.25: "1/4", 0.75: "3/4",
             1.5: "3/2", -0.5: "-1/2", -1.0: "-1", -2.0: "-2"}
    for k, v in table.items():
        if abs(f - k) < 1e-9:
            return v
    if abs(f - round(f)) < 1e-9:
        return str(int(round(f)))
    return f"{f:g}"
