#!/usr/bin/env python3
"""
alphabet.py — the constant pool. THE CURATION IS THE PHYSICS INPUT.

ENGINE_REVERSE_ENGINEERING §2 step 2: "Constant curation is the highest-leverage knob and it is
a physics judgment, not a search parameter." The a0 breakthrough came ONLY after constrained_search
DELETED every EM/quantum constant ('alpha has no business in galactic dynamics'). We keep that
discipline: an Alphabet is a small, deliberately-chosen pool, not a kitchen sink.

Three constant classes (mirrors §5 of the adapter spec):
  - LEAF constants     : the dimensionful/measured inputs of the target's sector
                         (gravity+cosmology for a0; sqrt-masses / ratios for SM).
  - GEOMETRY germs     : pi, e, small ints, sqrt(...), and the framework's own kernels
                         {Z=sqrt(32pi/3), kernel=sqrt(8pi/3), kappa=1/2, 8pi, 3/8pi, 4pi/3}.
                         Injected as a SEPARATE 'decorate by a dimensionless factor' pass so every
                         skeleton gets O(1) decorations without exploding the leaf set.
  - GROUP invariants   : dimensions/orders/Casimirs of candidate flavor groups (S3, A4, S4,
                         Delta(27), Spin8-triality) — the FORCED-coefficient pool the kernel gate
                         matches against (a forced group dimension, not a free integer).

All values carried at mpmath precision. Each constant exposes value (mpmath), Label (dim+rep),
human symbol, and a sympy symbol (kept symbolic for the forced-kernel gate).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import mpmath as mp
import sympy as sp

from .expr_tree import Label, DIMENSIONLESS, ACCELERATION

mp.mp.dps = 40


@dataclass
class Const:
    key: str
    symbol: str
    value: object              # mpmath mpf
    label: Label
    role: str                  # 'leaf' | 'germ' | 'group' | 'target'
    sym: object = None         # sympy symbol/expr kept symbolic for the kernel gate

    def __post_init__(self):
        self.value = mp.mpf(self.value) if not isinstance(self.value, mp.mpf) else self.value
        if self.sym is None:
            self.sym = sp.Symbol(self.symbol, positive=True)


@dataclass
class Alphabet:
    """A resolved pool: dict of key -> Const, plus the leaf / germ / group / exponent partitions
    the Grammar consumes. The Search and the gate both read from one Alphabet so values never
    drift between search and validation.
    """
    consts: Dict[str, Const] = field(default_factory=dict)
    leaves: List[str] = field(default_factory=list)   # depth-1 leaf keys
    germs: List[str] = field(default_factory=list)     # dimensionless decoration keys
    groups: List[str] = field(default_factory=list)    # forced group-invariant keys
    exponents: List[object] = field(default_factory=list)

    def add(self, c: Const):
        self.consts[c.key] = c
        if c.role == "leaf":
            self.leaves.append(c.key)
        elif c.role == "germ":
            self.germs.append(c.key)
        elif c.role == "group":
            self.groups.append(c.key)

    # accessors the ExprNode evaluator / printer use
    def value(self, key): return self.consts[key].value
    def label(self, key): return self.consts[key].label
    def symbol(self, key): return self.consts[key].symbol
    def sym(self, key): return self.consts[key].sym


# =============================================================================
# GEOMETRY GERMS  (shared across every Alphabet — the framework's own germ pool)
# =============================================================================

def _geometry_germs() -> List[Const]:
    pi = mp.pi
    Z2 = 32 * pi / 3
    Z = mp.sqrt(Z2)
    kernel = mp.sqrt(8 * pi / 3)  # = Z/2
    sp_pi = sp.pi
    germs = [
        Const("pi", "pi", pi, DIMENSIONLESS, "germ", sp_pi),
        Const("e", "e", mp.e, DIMENSIONLESS, "germ", sp.E),
        Const("2", "2", 2, DIMENSIONLESS, "germ", sp.Integer(2)),
        Const("3", "3", 3, DIMENSIONLESS, "germ", sp.Integer(3)),
        Const("4", "4", 4, DIMENSIONLESS, "germ", sp.Integer(4)),
        Const("5", "5", 5, DIMENSIONLESS, "germ", sp.Integer(5)),
        Const("6", "6", 6, DIMENSIONLESS, "germ", sp.Integer(6)),
        Const("8", "8", 8, DIMENSIONLESS, "germ", sp.Integer(8)),
        Const("9", "9", 9, DIMENSIONLESS, "germ", sp.Integer(9)),
        Const("12", "12", 12, DIMENSIONLESS, "germ", sp.Integer(12)),
        Const("16", "16", 16, DIMENSIONLESS, "germ", sp.Integer(16)),
        # framework kernels (forced O(1)'s from the a0 program)
        Const("8pi", "8pi", 8 * pi, DIMENSIONLESS, "germ", 8 * sp_pi),
        Const("2pi", "2pi", 2 * pi, DIMENSIONLESS, "germ", 2 * sp_pi),
        Const("4pi", "4pi", 4 * pi, DIMENSIONLESS, "germ", 4 * sp_pi),
        Const("4pi/3", "4pi/3", 4 * pi / 3, DIMENSIONLESS, "germ", 4 * sp_pi / 3),
        Const("3/8pi", "3/8pi", 3 / (8 * pi), DIMENSIONLESS, "germ", 3 / (8 * sp_pi)),
        Const("Z", "Z", Z, DIMENSIONLESS, "germ", sp.sqrt(32 * sp_pi / 3)),
        Const("kernel", "kern", kernel, DIMENSIONLESS, "germ", sp.sqrt(8 * sp_pi / 3)),
        Const("kappa", "kap", mp.mpf("0.5"), DIMENSIONLESS, "germ", sp.Rational(1, 2)),
    ]
    return germs


# =============================================================================
# GEOMETRIC-MODE GERMS  (the REDUCED, forced-geometric decoration pool — Carl's refinement)
#   Restrict the dimensionless-factor alphabet to FORCED-GEOMETRIC primitives
#   (rep dims, |G|, measure-pi, root/polytope angles, Coxeter/Dynkin/Casimir, forced
#   structural rationals) from targets/geometric_primitives.forced_pool(), INSTEAD of the
#   arbitrary integers/transcendentals of _geometry_germs(). A sparser reachable set means a
#   hit carries real bits (notes/GEOMETRIC_WEB.md). The a0/Z/kappa kernels are NOT injected
#   here (that would regenerate the 164 FDR-dead re-labelings); this is pure SM-sector geometry.
# =============================================================================

# Forced primitives that are the SEARCH TARGET'S OWN ANSWER (not a building block) — these are
# quarantined OUT of the germ pool so the engine cannot use the answer as a decoration (the FDR-
# dead failure mode). The forced STRUCTURAL rationals (1/3 floor, 1/6 amplitude, 1/2 democratic
# angle, 3/8 trace, 1/2 Dynkin) stay IN — they are forced building blocks, not target answers.
_GEOMETRIC_GERM_QUARANTINE = {
    "koide_Q_target",        # 2/3 IS the Koide answer
    "tbm_sin2_12", "tbm_sin2_23", "tbm_sin2_13",  # the PMNS-angle answers
    "qlc_target_45",         # the complementarity answer (also a degrees value, not dimensionless)
    "th13_over_thetaC_sqrt2",  # numeric coincidence target (carries no exact sym)
    "8pi",                   # gravity-forced; explicitly NOT a gauge/SM building block (per the web)
}


def _geometric_germs() -> List[Const]:
    """Map targets/geometric_primitives.forced_pool() -> germ Consts (the reduced alphabet).

    Each forced primitive becomes a dimensionless 'decorate by this factor' germ whose sympy
    `sym` carries the EXACT symbolic form (so the forced-kernel gate can read its provenance).
    Zero-valued (division-unsafe) and target-answer primitives are quarantined out.
    """
    try:
        from targets.geometric_primitives import forced_pool as _forced_pool
    except Exception:
        # fall back to absolute import if run from a different cwd
        import importlib
        _forced_pool = importlib.import_module(
            "targets.geometric_primitives").forced_pool
    germs: List[Const] = []
    seen_keys = set()
    for p in _forced_pool():
        if p.key in _GEOMETRIC_GERM_QUARANTINE:
            continue
        if p.value == 0.0:           # division-unsafe (tbm_sin2_13); skip
            continue
        if p.key in seen_keys:
            continue
        seen_keys.add(p.key)
        sym = p.sym if (p.sym is not None) else sp.nsimplify(p.value)
        germs.append(Const(p.key, p.key, mp.mpf(str(p.value)), DIMENSIONLESS, "germ", sym))
    return germs


# =============================================================================
# GROUP INVARIANTS  (forced-coefficient pool for the kernel gate)
# =============================================================================

def _group_invariants() -> List[Const]:
    """Orders / irrep dimensions / Casimir-flavored invariants of candidate flavor groups.

    These are the ONLY integers/rationals the forced-kernel gate treats as 'pre-fit forced'
    (a representation dimension is fixed by the group BEFORE any data). A bare free integer is
    not in this pool. Values are exact small numbers; the point is the *provenance tag*.
    """
    inv = [
        # S3 (smallest non-abelian; where Koide's 1+2 democratic/circulant split lives)
        Const("|S3|", "|S3|", 6, DIMENSIONLESS, "group", sp.Integer(6)),
        Const("dimS3_2", "2_S3", 2, DIMENSIONLESS, "group", sp.Integer(2)),   # 2-dim irrep
        # A4 (canonical tri-bimaximal flavor group): irreps 1,1',1'',3 ; order 12
        Const("|A4|", "|A4|", 12, DIMENSIONLESS, "group", sp.Integer(12)),
        Const("dimA4_3", "3_A4", 3, DIMENSIONLESS, "group", sp.Integer(3)),
        # S4 : order 24 ; irreps 1,1',2,3,3'
        Const("|S4|", "|S4|", 24, DIMENSIONLESS, "group", sp.Integer(24)),
        # Delta(27): order 27
        Const("|D27|", "|D27|", 27, DIMENSIONLESS, "group", sp.Integer(27)),
        # number of generations (the empirical 3)
        Const("Ngen", "Ngen", 3, DIMENSIONLESS, "group", sp.Integer(3)),
    ]
    return inv


# =============================================================================
# EXPONENT SET  (extended with small rationals per §5)
# =============================================================================

def _exponents() -> List[object]:
    return [mp.mpf(2), mp.mpf(3), mp.mpf("0.5"), mp.mpf(-1), mp.mpf(-2),
            mp.mpf("1.5"), mp.mpf("-0.5"), mp.mpf(1) / 3, mp.mpf(2) / 3,
            mp.mpf("0.25"), mp.mpf("0.75")]


# =============================================================================
# DEFAULT BUILDERS
# =============================================================================

def build_default_alphabet(extra_leaves: Optional[List[Const]] = None,
                           with_groups: bool = True,
                           with_germs: bool = True) -> Alphabet:
    """A bare alphabet = geometry germs (+ group invariants). Leaves supplied per target.

    For a SM-ratio target the leaves are the relevant measured inputs (e.g. the 3 sqrt-masses
    for the Koide toy). The germs/groups are shared. This keeps the pool SMALL and curated.
    """
    a = Alphabet(exponents=_exponents())
    if with_germs:
        for c in _geometry_germs():
            a.add(c)
    if with_groups:
        for c in _group_invariants():
            a.add(c)
    if extra_leaves:
        for c in extra_leaves:
            a.add(c)
    return a


def build_a0_alphabet() -> Alphabet:
    """The COSMOLOGY pool that re-finds a0 — the calibration positive (must re-derive
    a0 = c sqrt(G rho_c)/2 -> cH0/sqrt(32pi/3)). Ported from constrained_search.CONSTANTS:
    gravity+cosmology leaves + geometry numbers only, NO QED.
    """
    G = Label(3, -1, -2)
    c_dim = Label(1, 0, -1)
    a = Alphabet(exponents=_exponents())
    # geometry germs (small ints + pi suffice for a0; include the full germ pool)
    for g in _geometry_germs():
        a.add(g)
    # leaves: gravity + cosmology (values from constrained_search.py)
    leaves = [
        Const("G", "G", mp.mpf("6.67430e-11"), G, "leaf", sp.Symbol("G", positive=True)),
        Const("c", "c", mp.mpf("2.99792458e8"), c_dim, "leaf", sp.Symbol("c", positive=True)),
        Const("H0", "H0", mp.mpf("2.184e-18"), Label(0, 0, -1), "leaf", sp.Symbol("H0", positive=True)),
        Const("Lambda", "Lam", mp.mpf("1.1e-52"), Label(-2, 0, 0), "leaf", sp.Symbol("Lambda", positive=True)),
        Const("rho_c", "rho_c", mp.mpf("9.5e-27"), Label(-3, 1, 0), "leaf", sp.Symbol("rho_c", positive=True)),
    ]
    for l in leaves:
        a.add(l)
    return a
