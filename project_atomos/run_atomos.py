#!/usr/bin/env python3
"""
run_atomos.py — the long-running overnight autoresearch loop for project_atomos.

WHAT IT IS. A timed (default 24h, --hours override) loop that, for each precisely-known SM target
from targets/pdg_constants.py: searches candidate relations with the engine, SCORES each by
agreement WITHIN the measurement uncertainty (n-sigma + surplus bits relative to the target's own
tolerance, NOT a raw digit count), passes survivors to the 3-part gate (gate/verdict.py: FDR ∧
forced-kernel ∧ interlock), ACCUMULATES results (checkpoint every K iters: best-so-far, tried-set,
near-misses, building-block scores, per-target stats), on STAGNATION does a radical mutation /
strategy shift, and periodically writes a human-readable CLUES.md.

THE PORTING RULE (the project's whole thesis — OVERNIGHT_RUNNER_SPEC §intro). hali_flow ranked by
R²/closeness; THAT is the move that produces FDR-dead numerology. We keep every hali_flow CONTROL
mechanic (timed loop, knowledge accumulation, stagnation→radical-mutation, checkpointing, clue
surfacing) but replace the fitness function with the 3-part GATE. Engine closeness (n-sigma,
fit-bits) is ADVISORY ranking only — it decides what to hand the gate, never what counts as a
discovery. Same bar both ways: a long night yields FDR-DEAD honestly if the SM sector is
kernel-free, and promotes a LEAD only when all three gates pass.

CLI:
  python3 run_atomos.py --all                       # sweep all precise targets, 24h
  python3 run_atomos.py --target r_mu_e --hours 8   # one target, 8h
  python3 run_atomos.py --all --checkpoint 100      # checkpoint every 100 gate-evals
  python3 run_atomos.py --resume                    # resume from results/checkpoint.json
  python3 run_atomos.py --calibrate                 # run the acceptance test (a0 + Koide + dead) and exit

Pure stdlib + numpy + scipy + sympy + mpmath. Local, no network.
"""
from __future__ import annotations

import argparse
import gc
import hashlib
import json
import math
import random
import time
import traceback
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import mpmath as mp

# ---- project imports (run from project_atomos/) -----------------------------------------------
from engine.alphabet import (Alphabet, Const,
                             _geometry_germs, _geometric_germs, _group_invariants, _exponents)
from engine.expr_tree import ExprNode, OpType, Label, DIMENSIONLESS
from engine.search import Grammar
from engine.scoring import score_value, measurement_tol, ScoreCard
from gate.candidate import (Candidate as GateCandidate, SearchSpace, Coefficient,
                            Factor, Interlock)
from gate.verdict import validate, Verdict
import targets.pdg_constants as pdg

mp.mp.dps = 40

HERE = Path(__file__).resolve().parent
RESULTS = HERE / "results"


# ===============================================================================================
# CONFIG  (ported verbatim-in-spirit from haliflow_8hr_cosmos lines 37-40; OVERNIGHT_RUNNER §1)
# ===============================================================================================

@dataclass
class Config:
    run_hours: float = 24.0
    checkpoint_interval: int = 200      # gate-evals between checkpoint + strategy-evolve
    stagnation_threshold: int = 800     # gate-evals with no new best-bits before the ladder CLIMBS
    max_depth: int = 4                  # engine tree depth (radical-mutation can bump to 5)
    top_near_misses: int = 100          # cap on the in-RAM near-miss list (haliflow's [:100])
    seed: int = 1234                    # deterministic-seedable (logged) for reproducibility
    hard_filter: str = "interlock"      # default per ENGINE_RE §6 (interlock/symmetry, not dimension)
    min_interlock: int = 3              # Koide signature: tie >=3 measured leaves
    # the three generation strategies' mix (haliflow's 50/25/25); resampled on radical mutation
    p_enumerate: float = 0.50
    p_combine: float = 0.25
    p_mutate: float = 0.25
    rng_state: Optional[list] = None    # restored on --resume
    # GEOMETRIC MODE (Carl's a0-discipline refinement, 2026-06-25): when True the engine's
    # DIMENSIONLESS-FACTOR (germ) pool is restricted to the FORCED-GEOMETRIC primitives of
    # targets/geometric_primitives.forced_pool() (rep dims, |G|, measure-pi, root/polytope angles,
    # Coxeter/Dynkin/Casimir, forced structural rationals) INSTEAD of arbitrary integers +
    # transcendentals. The physics LEAVES (masses/couplings) stay available; only the dimensionless
    # decoration factors get restricted -> a sparser reachable set, so a hit earns real bits.
    geometric_mode: bool = False


# files (OVERNIGHT_RUNNER §1)
def _paths(results: Path) -> dict:
    return dict(
        knowledge=results / "knowledge.json",
        leads=results / "leads.jsonl",
        dead=results / "fdr_dead.jsonl",
        clues=results / "CLUES.md",
        checkpoint=results / "checkpoint.json",
        progress=results / "progress.log",
        stats=results / "stats.json",
        bloom=results / "seen.bloom",        # the tried-set, persisted compactly (NOT in knowledge.json)
    )


# ===============================================================================================
# KNOWLEDGE  (accumulate tried-set / best-bits-per-target / near-misses / building-block scores)
#            ported from haliflow KnowledgeBase + autonomous_law_discovery MethodologyKnowledge.
#            OVERNIGHT_RUNNER §2. Figure of merit = GATE BITS, never R².
# ===============================================================================================

@dataclass
class NearMiss:
    target: str
    formula: str
    fdr_bits: float
    n_sigma: float
    gate_failed: str      # which gate it died at (A/B/C)
    tell: str
    n_distinct_leaves: int
    status: str           # the verdict status


@dataclass
class TargetStat:
    n_tried: int = 0
    n_passed_A: int = 0
    best_bits: float = 0.0
    best_formula: str = ""
    best_n_sigma: float = float("inf")
    gate_wall: Dict[str, int] = field(default_factory=dict)  # which gate kills most candidates

    def record_wall(self, gate: str):
        self.gate_wall[gate] = self.gate_wall.get(gate, 0) + 1

    def dominant_wall(self) -> str:
        if not self.gate_wall:
            return "—"
        return max(self.gate_wall.items(), key=lambda kv: kv[1])[0]


DEFAULT_BLOOM_BITS = 1 << 23      # 1 MB; main() sizes the real one from --hours
BLOOM_SAVE_INTERVAL = 120.0       # seconds: the tried-set is the heavy artifact -> decoupled cadence


def _bloom_bits_for_hours(hours: float) -> int:
    """Size the tried-set bloom to the run length so memory+disk stay bounded. ~6e7 enumerated
    trees/hour was observed; ~16 bits/item gives a ~4e-4 false-dup rate while unsaturated. Clamped
    to [2^20 (128 KB), 2^31 (256 MB)] so neither a 30-second smoke test nor a 24-hour night blows up.
    If a very long run saturates the filter, the novelty rate simply collapses — which is exactly the
    signal that fires radical mutation (a graceful 'dead end -> readjust', not a crash)."""
    est_items = max(1.0, 6e7 * float(hours))
    want = int(16 * est_items)
    nbits = 1 << max(20, min(31, want.bit_length()))   # round up to a power of two, clamped
    return nbits


class BloomFilter:
    """Fixed-size Bloom filter standing in for the cross-checkpoint tried-set. Replaces an UNBOUNDED
    `set` that was re-serialized whole into knowledge.json every checkpoint (it hit tens of MB after
    ~1k evals because it tracks every ENUMERATED tree, ~470x the gate-evals, and would OOM/thrash a
    24h run). Bounded RAM (one bytearray) + a compact binary file (results/seen.bloom). FALSE
    POSITIVES ONLY: it never reports a true duplicate as novel, so it never wastes gate-work
    re-judging a tree; at worst it occasionally skips a genuinely-novel tree at a tiny accepted rate
    — strictly safe for a dedup-to-save-work set. Drop-in for the `in` / `.add()` the set supported."""

    __slots__ = ("nbits", "k", "bits", "n_added")

    def __init__(self, nbits: int = DEFAULT_BLOOM_BITS, k: int = 7):
        self.nbits = max(8, int(nbits))
        self.k = int(k)
        self.bits = bytearray((self.nbits + 7) // 8)
        self.n_added = 0

    def _indices(self, item):
        # one blake2b -> two 64-bit hashes -> k indices by double hashing (Kirsch–Mitzenmacher)
        d = hashlib.blake2b(str(item).encode("utf-8"), digest_size=16).digest()
        h1 = int.from_bytes(d[:8], "little")
        h2 = int.from_bytes(d[8:], "little") | 1          # odd step -> good spread
        n = self.nbits
        for i in range(self.k):
            yield (h1 + i * h2) % n

    def add(self, item) -> None:
        for b in self._indices(item):
            self.bits[b >> 3] |= (1 << (b & 7))
        self.n_added += 1

    def __contains__(self, item) -> bool:
        return all((self.bits[b >> 3] >> (b & 7)) & 1 for b in self._indices(item))

    def __len__(self) -> int:
        return self.n_added

    def to_bytes(self) -> bytes:
        hdr = (self.nbits.to_bytes(8, "little") + self.k.to_bytes(2, "little")
               + self.n_added.to_bytes(8, "little"))
        return hdr + bytes(self.bits)

    @classmethod
    def from_bytes(cls, blob: bytes) -> "BloomFilter":
        nbits = int.from_bytes(blob[:8], "little")
        k = int.from_bytes(blob[8:10], "little")
        n_added = int.from_bytes(blob[10:18], "little")
        bf = cls(nbits=nbits, k=k)
        bf.bits = bytearray(blob[18:])
        bf.n_added = n_added
        return bf


class Knowledge:
    """The single persistent accumulator. Saved to knowledge.json every checkpoint; the
    tried-set (seen_canonical, a Bloom filter in results/seen.bloom) + best-bits survive restarts
    so successive nights compound."""

    def __init__(self, bloom_bits: int = DEFAULT_BLOOM_BITS):
        # the cross-checkpoint tried-set: a fixed-size Bloom filter (bounded RAM), persisted to its
        # own compact binary file (results/seen.bloom), NOT inlined unbounded into knowledge.json.
        self.seen_canonical = BloomFilter(bloom_bits)
        self._last_bloom_save: float = 0.0                    # throttle for the heavy bloom write
        self.best_bits_per_target: Dict[str, float] = {}      # figure of merit = gate bits
        self.near_misses: List[NearMiss] = []                 # Gate-A survivors that failed B/C
        self.building_block_scores: Dict[str, float] = {}     # leaf/germ/group/op -> summed bits
        self.per_target_stats: Dict[str, TargetStat] = {}
        self.best_bits_overall: float = 0.0
        self.best_bits_history: List[float] = []              # rolling, drives stagnation
        self.n_eval: int = 0
        self.n_leads: int = 0
        self.evals_since_best: int = 0                        # stagnation counter
        # for the novelty-collapse half of the stagnation test: fraction of newly-proposed trees
        # already in seen_canonical (the alphabet×depth is exhausted when this -> ~1).
        self._recent_novel = []                               # rolling list of 0/1 (novel?)

    # ---- record one gate evaluation ----
    def record(self, target_key: str, cand: GateCandidate, verdict: Verdict,
               card: ScoreCard, canonical: str, leaves_germs_ops: List[str]):
        self.n_eval += 1
        ts = self.per_target_stats.setdefault(target_key, TargetStat())
        ts.n_tried += 1

        bits = verdict.fdr.bits if math.isfinite(verdict.fdr.bits) else 0.0
        passed_A = verdict.fdr.passed

        # which gate killed it (for the wall stat + near-miss tagging)
        if verdict.status == "CERTIFIED":
            gate_failed = "—(LEAD)"
        elif not verdict.fdr.passed:
            gate_failed = "A"
        elif not verdict.kernel.passed:
            gate_failed = "B"
        elif not verdict.interlock.passed:
            gate_failed = "C"
        else:
            gate_failed = "—"
        ts.record_wall(gate_failed)

        if passed_A:
            ts.n_passed_A += 1
            # credit the building blocks this Gate-A survivor used (OVERNIGHT_RUNNER §2)
            for b in leaves_germs_ops:
                self.building_block_scores[b] = self.building_block_scores.get(b, 0.0) + bits
            # near-miss: passed A but not certified
            if verdict.status != "CERTIFIED":
                self.near_misses.append(NearMiss(
                    target=target_key, formula=cand.note or "", fdr_bits=bits,
                    n_sigma=card.n_sigma, gate_failed=gate_failed, tell=verdict.tell,
                    n_distinct_leaves=cand.interlock.n_constants_tied, status=verdict.status))
                self.near_misses.sort(key=lambda nm: -nm.fdr_bits)
                self.near_misses = self.near_misses[:100]

        # per-target best (by bits, tie-broken by closeness)
        if bits > ts.best_bits or (bits == ts.best_bits and card.n_sigma < ts.best_n_sigma):
            ts.best_bits = bits
            ts.best_formula = cand.note or ""
            ts.best_n_sigma = card.n_sigma
        self.best_bits_per_target[target_key] = ts.best_bits

        # overall best + stagnation counter
        if bits > self.best_bits_overall + 1e-9:
            self.best_bits_overall = bits
            self.evals_since_best = 0
        else:
            self.evals_since_best += 1

    def note_novelty(self, was_novel: bool):
        self._recent_novel.append(1 if was_novel else 0)
        if len(self._recent_novel) > 400:
            self._recent_novel = self._recent_novel[-400:]

    def novelty_rate(self) -> float:
        if not self._recent_novel:
            return 1.0
        return sum(self._recent_novel) / len(self._recent_novel)

    # ---- stagnation (OVERNIGHT_RUNNER §3): DEAD-END -> CLIMB COMPLEXITY ----
    def stagnant(self, threshold: int, eps: float = 1e-6) -> bool:
        # Fire the escalation ladder (deepen tree depth 4->5, then rotate flavor group
        # none->S3->A4->S4->D27 + extra exponents, switch filter, randomize mix) whenever best_bits
        # has stayed FLAT for `threshold` evals — regardless of novelty. The OLD gate also required
        # novelty<0.05 (alphabet×depth exhausted, re-seeing >95% of trees), which a hard null never
        # reaches (novelty sits ~0.25 while bits stay flat), so the ladder NEVER fired and the search
        # never climbed past the base complexity. Flat best-bits alone IS the dead-end signal — that
        # is what turns this into the climbing search. (Carl 2026-06-25)
        return self.evals_since_best >= threshold

    def reset_stagnation(self):
        self.evals_since_best = 0
        self._recent_novel = []

    # ---- (de)serialization (tried-set + best-bits survive restarts) ----
    def to_dict(self) -> dict:
        return dict(
            # the tried-set (seen_canonical) is persisted SEPARATELY as results/seen.bloom — never
            # inlined here (inlining it unbounded every checkpoint was the OOM/thrash bug).
            best_bits_per_target=self.best_bits_per_target,
            near_misses=[asdict(nm) for nm in self.near_misses],
            building_block_scores=self.building_block_scores,
            per_target_stats={k: dict(n_tried=v.n_tried, n_passed_A=v.n_passed_A,
                                      best_bits=v.best_bits, best_formula=v.best_formula,
                                      best_n_sigma=v.best_n_sigma, gate_wall=v.gate_wall)
                              for k, v in self.per_target_stats.items()},
            best_bits_overall=self.best_bits_overall,
            best_bits_history=self.best_bits_history,
            n_eval=self.n_eval, n_leads=self.n_leads,
            evals_since_best=self.evals_since_best,
        )

    @classmethod
    def from_dict(cls, d: dict) -> "Knowledge":
        k = cls()
        # seen_canonical (the tried-set) is restored from results/seen.bloom by the --resume caller,
        # not from this dict — it is no longer inlined in knowledge.json.
        k.best_bits_per_target = d.get("best_bits_per_target", {})
        k.near_misses = [NearMiss(**nm) for nm in d.get("near_misses", [])]
        k.building_block_scores = d.get("building_block_scores", {})
        for key, v in d.get("per_target_stats", {}).items():
            ts = TargetStat(n_tried=v["n_tried"], n_passed_A=v["n_passed_A"],
                            best_bits=v["best_bits"], best_formula=v.get("best_formula", ""),
                            best_n_sigma=v.get("best_n_sigma", float("inf")),
                            gate_wall=v.get("gate_wall", {}))
            k.per_target_stats[key] = ts
        k.best_bits_overall = d.get("best_bits_overall", 0.0)
        k.best_bits_history = d.get("best_bits_history", [])
        k.n_eval = d.get("n_eval", 0)
        k.n_leads = d.get("n_leads", 0)
        k.evals_since_best = d.get("evals_since_best", 0)
        return k


# ===============================================================================================
# THE ENGINE↔GATE BRIDGE  (the load-bearing adapter)
#   Turns an engine ExprNode + a PDG Target into a gate.candidate.Candidate, declaring:
#     - SearchSpace  : germ pool + the MEASUREMENT tolerance (target rel_precision) + sigma + digits
#     - Coefficient  : the candidate's germ/group factors, with provenance auto-tagged from the
#                      registry (a free integer gets NO provenance -> Gate B will fail it honestly)
#     - Interlock    : C2 = how many distinct MEASURED leaves it ties (the Koide signature)
#   This is where the engine's "closeness" candidate becomes a structured CLAIM the gate re-checks.
# ===============================================================================================

# the germ pool the FDR null reconstructs over (geometry germs + group invariants as O(1)'s)
def _fdr_germ_pool(alpha: Alphabet) -> dict:
    pool = {}
    for key in list(alpha.germs) + list(alpha.groups):
        try:
            pool[alpha.symbol(key)] = float(alpha.value(key))
        except Exception:
            pass
    return pool


# --- Koide structural null: the random-mass-triple measure (koide_fdr_sqrt2) -------------------
# For a Koide-invariant target (Q over a fermion triple), Gate-A-on-value is uninformative (2/3 is
# a baked rational); the certified path is the STRUCTURAL null: P(Q over random no-physics mass
# triples lands on the target). This recovers the documented ~1-in-44,000 for the leptons. We
# attach it so Koide targets reach the REAL-PUZZLE-RE-LABELED verdict honestly instead of dying
# generic-Gate-A. The triple's log-uniform range mirrors the lineage.
import numpy as _np

def _koide_null_factory(lo: float = 1e-2, hi: float = 1e4):
    def _null(N):
        m = _np.exp(_np.random.uniform(_np.log(lo), _np.log(hi), size=(int(N), 3)))
        sm = _np.sqrt(m)
        return m.sum(1) / sm.sum(1) ** 2
    return _null


def _is_koide_target(target) -> bool:
    return target.sector == "koide" and "Q" in target.key


# auto-tag a germ/group const's forced provenance from the registry (best-effort).
# Only group-invariant dimensions / the a0 kernel pieces carry provenance; bare integers/pi do NOT.
from gate.registry import FORCED_CONSTRAINTS

def _auto_provenance(key: str, value: float) -> Optional[str]:
    """Map an alphabet key -> a registry provenance key IF it is a pre-registered forced constant.
    A bare free integer (2,3,4,...) or pi returns None => Gate B treats it as a free fit param."""
    # exact group-dimension matches (forced by a declared symmetry)
    for prov, entry in FORCED_CONSTRAINTS.items():
        if abs(value - entry["value"]) / (abs(entry["value"]) or 1) < 1e-9:
            # but ONLY count group/kernel provenance, not a coincidental integer match:
            # the a0 kernel pieces + group dims are legitimate; '3' matching A4_dim_3 is allowed
            # because 3 IS the A4 triplet dim — that's the point of the forced pool. Still, the
            # gate's OVERDETERMINATION test (>=2 independent appearances) prevents a lone match
            # from passing, so this is safe.
            return prov
    return None


def build_gate_candidate(tree: ExprNode, alpha: Alphabet, target_key: str,
                         target, value: float, n_targets_searched: int,
                         card: ScoreCard) -> Tuple[GateCandidate, List[str]]:
    """Construct the gate's structured claim from an engine tree. Returns (candidate, blocks)
    where blocks = the leaf/germ/group/op names used (for building-block crediting)."""
    leaf_consts = tree.leaf_consts()
    measured = set(alpha.leaves)
    distinct_measured = sorted(set(leaf_consts) & measured)

    # --- SearchSpace: the FDR null + the MEASUREMENT-AWARE tolerance ---
    germ_pool = _fdr_germ_pool(alpha)
    # Koide special-casing: if this is a Koide invariant AND the relation genuinely ties all three
    # sqrt-masses (the real interlock, not a one-mass monomial), route Gate A through the
    # STRUCTURAL random-mass-triple null (the certified path: ~1-in-44,000 for the leptons). A
    # Koide relation that does NOT tie all three masses is just a generic value-match and stays on
    # the Poisson route (it will die generic-Gate-A, correctly).
    structural_null = None
    rational_target = False
    # Only attach the Koide null when the relation BOTH ties all three sqrt-masses AND actually
    # evaluates to the Koide-Q form (within a loose band). A 3-mass product that merely happens to
    # hit 2/3 is NOT the Koide interlock and must not borrow Koide's surprise — the structural null
    # is the random-triple measure of the SPECIFIC Q relation, so it is only honest for it.
    if (_is_koide_target(target) and len(distinct_measured) >= 3
            and abs(float(value) - float(target.value)) / abs(float(target.value)) < 1e-3):
        structural_null = _koide_null_factory()
        rational_target = True
    search = SearchSpace(
        germ_pool=germ_pool,
        tol=measurement_tol(target),                      # = target rel_precision (clamped)
        target_sigma=float(target.sigma),
        n_digits_known=float(target.n_digits),            # the bit-cap (Carl's emphasis a)
        n_targets_searched=n_targets_searched,            # look-elsewhere multiplicity
        structural_null=structural_null,
        structural_eps=1e-5,                              # recovers the documented ~1-in-44k
        structural_N=2_000_000,                           # enough samples for the ~15-bit estimate
        rational_target=rational_target,
    )

    # --- Coefficient: germ/group factors with auto provenance (free ints get None) ---
    factors = []
    free_params = 0
    for key in set(leaf_consts):
        if key in measured:
            continue  # measured leaves are inputs, not coefficient factors
        val = float(alpha.value(key))
        prov = _auto_provenance(key, val)
        if prov is None:
            free_params += 1  # a bare germ/integer with no forced provenance = free param
        else:
            factors.append(Factor(value=val, provenance=prov, appears_in=[prov]))
    coefficient = Coefficient(
        factors=factors,
        free_params=free_params,
        target_value=None,                # the engine candidate is a value-match, not a coeff claim
        form_forced_independently=0,
    )

    # --- Interlock: C2 = how many distinct MEASURED leaves it ties. With <=1 free param this is
    #     the Koide signature (3 masses, 0 free). The engine's interlock filter already pushes
    #     toward >=min_interlock; here we DECLARE it for Gate C to re-check. ---
    interlock = Interlock(
        n_independent_observables=0,                       # engine value-matches don't force C1
        n_constants_tied=len(distinct_measured),           # C2 count
        n_free_in_interlock=free_params,                   # how many free O(1)'s the relation needs
        cross_sector=None,                                 # value-match: no universal claim to test
        claimed_universal=False,
    )

    cand = GateCandidate(
        name=f"{target_key}:{tree.to_string(alpha)}",
        target_value=float(target.value),
        relation_value=float(value),
        search=search,
        coefficient=coefficient,
        interlock=interlock,
        note=tree.to_string(alpha),
    )
    # building blocks credited = the distinct leaves/germs/groups used + the op types
    blocks = sorted(set(leaf_consts)) + [_op_name(tree)]
    return cand, blocks


def _op_name(tree: ExprNode) -> str:
    return f"op:{tree.op.value}"


# ===============================================================================================
# ALPHABETS PER TARGET
#   Each target gets a SMALL, curated alphabet: the relevant measured leaves (the inputs whose
#   ratios/relations could explain it) + shared geometry germs + group invariants. Curation is the
#   physics input (ENGINE_RE §2 step 2). The radical-mutation menu toggles which group sub-pool and
#   which exponents/depth are active.
# ===============================================================================================

import sympy as sp

def _leaf_for(target) -> List[Const]:
    """The measured-leaf inputs for a given target. For a ratio r_a_b the leaves are a and b (as
    dimensionless values); for a Koide Q the leaves are the three sqrt-masses; for a coupling/angle
    the leaf is the dimensionless value itself plus sibling sector values. We keep it SMALL."""
    ds = pdg.load()
    sector = target.sector
    leaves: List[Const] = []

    def mk(key: str) -> Optional[Const]:
        if key not in ds:
            return None
        t = ds.target(key)
        return Const(key, key, mp.mpf(str(float(t.value))), DIMENSIONLESS, "leaf",
                     sp.Symbol(key.replace("/", "_"), positive=True))

    # ratios: expose the two constituent masses (the tautology fix in build_target_alphabet drops the
    # target's OWN two, so r_X_Y ends up germ-only — see NOTE). A sibling-mass leaf pool was tried
    # (2026-06-25) but stalls the enumerator: raw masses span 6 orders of magnitude (m_u..m_t), so the
    # near-target prefilter rejects every tree -> 0 evals. Mass-ratio targets are the FDR-dead sector
    # anyway; the productive geometric targets are Koide + the mixing matrices (which keep real leaves).
    # Proper sibling-mass support needs mass-scale normalization in the enumerator — a separate pass.
    if target.sector in ("ratio",):
        parts = target.key.split("_")
        if len(parts) == 3 and parts[0] == "r":
            for k in (parts[1], parts[2]):
                for full in (f"m_{k}", k):
                    c = mk(full)
                    if c:
                        leaves.append(c)
                        break
    # koide: the three sqrt-masses of the relevant triple
    if target.sector == "koide":
        triple = {
            "koide_Q_lep": ("m_e", "m_mu", "m_tau"),
            "koide_theta_lep": ("m_e", "m_mu", "m_tau"),
            "koide_Q_up": ("m_u", "m_c", "m_t"),
            "koide_Q_down": ("m_d", "m_s", "m_b"),
        }.get(target.key, ())
        for k in triple:
            t = ds.target(k) if k in ds else None
            if t is not None:
                leaves.append(Const(f"sqrt_{k}", f"√{k}",
                                    mp.sqrt(mp.mpf(str(float(t.value)))), DIMENSIONLESS, "leaf",
                                    sp.Symbol(f"sqrt_{k}", positive=True)))
    # for couplings/angles/sin^2 with no obvious decomposition, expose sibling sector values as the
    # interlock pool (so a relation must tie >=min_interlock of them, Koide-style)
    if not leaves:
        sib = [t for t in ds.sector(sector) if t.units == "" and t.key != target.key]
        for t in sib[:6]:
            leaves.append(Const(t.key, t.key, mp.mpf(str(float(t.value))), DIMENSIONLESS, "leaf",
                                sp.Symbol(t.key.replace("/", "_"), positive=True)))
    return leaves


# group sub-pools the radical-mutation menu toggles (ENGINE_RE: A4 -> S4 -> Delta27 -> triality)
_GROUP_POOLS = {
    "none": [],
    "S3": ["|S3|", "dimS3_2", "Ngen"],
    "A4": ["|A4|", "dimA4_3", "Ngen"],
    "S4": ["|S4|", "dimA4_3", "Ngen"],
    "D27": ["|D27|", "Ngen"],
}


def _defining_leaf_keys(target) -> set:
    """The TARGET'S OWN defining constants — the leaf keys the search must NOT use to reconstruct
    the target from its own parts (the tautology fix, Carl 2026-06-25).

    A ratio r_X_Y = m_X/m_Y is DEFINED as m_X/m_Y; if both m_X and m_Y are in the leaf pool the
    engine trivially rebuilds 'm_mu/m_e = m_mu/m_e' — it sails through Gate A (an exact value-match)
    then dies at Gate B (zero forced kernel, just two free measured numbers) having taught nothing.
    Excluding the defining constants forces the search to express the target in OTHER terms (other
    masses, forced-geometric primitives), which is the only way a hit can carry bits.

    We return the LEAF KEYS as _leaf_for() names them (the same `m_X`/`m_Y` resolution heuristic),
    so the exclusion lines up with what build_target_alphabet would otherwise add. Koide Q targets
    are NOT excluded: their three sqrt-masses ARE the genuine interlock (3 masses tied by 1
    relation, the Koide signature) — that is over-determination, not a one-step tautology.
    """
    keys: set = set()
    if target.sector == "ratio":
        # r_X_Y -> the numerator/denominator leaves, resolved exactly as _leaf_for does
        ds = pdg.load()
        parts = target.key.split("_")
        if len(parts) == 3 and parts[0] == "r":
            for k in (parts[1], parts[2]):
                for full in (f"m_{k}", k):
                    if full in ds:
                        keys.add(full)
                        break
    return keys


def build_target_alphabet(target, active_group: str = "none",
                          extra_exponents: bool = False,
                          geometric_mode: bool = False) -> Alphabet:
    """A small curated alphabet for one target. `active_group` selects which flavor-group
    invariants are ON (the highest-leverage radical-mutation lever).

    GEOMETRIC MODE (geometric_mode=True): the DIMENSIONLESS-FACTOR (germ) pool is swapped from the
    arbitrary-integer/transcendental _geometry_germs() to the FORCED-GEOMETRIC _geometric_germs()
    (the forced_pool() primitives). Leaves + group invariants are unchanged — only the decoration
    pool is restricted, so the reachable set is sparser and a hit earns real bits.

    TAUTOLOGY FIX: the target's own defining constants (_defining_leaf_keys) are excluded from the
    leaf pool, so the search cannot reconstruct the target from its own parts (no
    'm_mu/m_e = m_mu/m_e' trivial Gate-A pass)."""
    a = Alphabet(exponents=_exponents())
    if extra_exponents:
        a.exponents = a.exponents + [mp.mpf(4), mp.mpf(-3), mp.mpf(5), mp.mpf(1) / 4,
                                     mp.mpf(3) / 4, mp.mpf(-1) / 3]
    # germ pool: forced-geometric primitives in geometric mode, else the default germ pool
    germs = _geometric_germs() if geometric_mode else _geometry_germs()
    for g in germs:
        a.add(g)
    # only the active group's invariants (curated, not the kitchen sink)
    want = set(_GROUP_POOLS.get(active_group, []))
    for c in _group_invariants():
        if c.key in want:
            a.add(c)
    # tautology fix: drop the target's own defining constants from the leaf pool
    exclude = _defining_leaf_keys(target)
    for c in _leaf_for(target):
        if c.key in exclude:
            continue
        a.add(c)
    return a


# ===============================================================================================
# STRATEGY  (enumerate / combine / mutate) + StrategyEvolver  (OVERNIGHT_RUNNER §3)
# ===============================================================================================

class StrategyState:
    """The current generation strategy + the StrategyEvolver knobs. One per target sweep."""
    def __init__(self, cfg: Config, rng: random.Random):
        self.cfg = cfg
        self.rng = rng
        self.active_group = "none"
        self.extra_exponents = False
        self.geometric_mode = cfg.geometric_mode   # restrict germ pool to forced-geometric primitives
        self.max_depth = cfg.max_depth
        self.mutation_rate = 0.3
        self.complexity_bias = 0.0
        # the radical-mutation escalation ladder (ENGINE_RE / OVERNIGHT §3), tried in order
        self.escalation = 0
        self.escalation_log: List[str] = []
        # the live enumerator (lazily (re)built when alphabet/depth changes)
        self._grammar: Optional[Grammar] = None
        self._gen = None
        self._alpha: Optional[Alphabet] = None
        self._target = None

    def bind_target(self, target):
        """(Re)bind to a target: rebuild the curated alphabet + the enumerator.

        Koide-sector targets enable ADDITION: the genuine Koide Q = (Σm)/(Σ√m)^2 needs a SUM in
        the denominator, which the default product/ratio grammar cannot build. Addition is
        dimension/rep-matched (the three sqrt-masses are all dimensionless singlets), so the
        enumerator can reach the real Koide relation only here. For every other sector we keep
        addition OFF (the a0 lineage default — sums explode the space and a0 needed none)."""
        self._target = target
        self._alpha = build_target_alphabet(target, self.active_group, self.extra_exponents,
                                            geometric_mode=self.geometric_mode)
        use_add = (target.sector == "koide")
        self._grammar = Grammar(self._alpha, max_depth=self.max_depth, use_addition=use_add)
        self._gen = self._grammar.generate_all()

    @property
    def alpha(self) -> Alphabet:
        return self._alpha

    # --- propose the next engine tree (enumerate / combine / mutate) ---
    def propose(self, knowledge: Knowledge) -> Optional[Tuple[ExprNode, bool]]:
        """Returns (tree, was_novel) or None if the enumerator is exhausted (a stagnation signal).
        was_novel tracks whether this canonical hash was new (drives novelty-collapse detection)."""
        r = self.rng.random()
        tree = None
        if r < self.cfg.p_enumerate:
            tree = self._next_enumerated()
        elif r < self.cfg.p_enumerate + self.cfg.p_combine:
            tree = self._combine(knowledge) or self._next_enumerated()
        else:
            tree = self._mutate(knowledge) or self._next_enumerated()
        if tree is None:
            return None
        h = tree.canonical_hash()
        was_novel = h not in knowledge.seen_canonical
        return tree, was_novel

    def _next_enumerated(self) -> Optional[ExprNode]:
        if self._gen is None:
            return None
        try:
            return next(self._gen)
        except StopIteration:
            self._gen = None
            return None

    def _combine(self, knowledge: Knowledge) -> Optional[ExprNode]:
        """Combine two high-bits survivors (OVERNIGHT_RUNNER §3 combine). We use leaves of the
        current alphabet as the building blocks (the survivors' formulas live as strings; to keep
        the engine tree-typed we recombine fresh subtrees from high-scoring building blocks)."""
        keys = self._high_score_leaves(knowledge, 4)
        if len(keys) < 2:
            return None
        a, b = self.rng.sample(keys, 2)
        na = ExprNode(OpType.CONST, const=a)
        nb = ExprNode(OpType.CONST, const=b)
        op = self.rng.choice([OpType.MUL, OpType.DIV])
        node = ExprNode(op, children=[na, nb])
        # optionally decorate with a high-scoring germ / wrap in sqrt (quadrature, Koide-flavored)
        if self.rng.random() < 0.5 and self.alpha.germs:
            g = self.rng.choice(self.alpha.germs)
            node = ExprNode(self.rng.choice([OpType.MUL, OpType.DIV]),
                            children=[node, ExprNode(OpType.CONST, const=g)])
        if self.rng.random() < 0.3:
            node = ExprNode(OpType.SQRT, children=[node])
        return node

    def _mutate(self, knowledge: Knowledge) -> Optional[ExprNode]:
        """Wrap a high-scoring leaf in an op / swap a leaf for a transformed leaf (StrategyEvolver
        _mutate), biased by building_block_scores."""
        keys = self._high_score_leaves(knowledge, 6)
        if not keys:
            return None
        k = self.rng.choice(keys)
        node = ExprNode(OpType.CONST, const=k)
        op = self.rng.choice([OpType.SQRT, OpType.CBRT, OpType.INV, OpType.POW])
        if op == OpType.POW:
            node = ExprNode(OpType.POW, children=[node], exp=self.rng.choice(self.alpha.exponents))
        else:
            node = ExprNode(op, children=[node])
        # add/remove a germ factor
        if self.rng.random() < self.mutation_rate and self.alpha.germs:
            g = self.rng.choice(self.alpha.germs)
            node = ExprNode(self.rng.choice([OpType.MUL, OpType.DIV]),
                            children=[node, ExprNode(OpType.CONST, const=g)])
        return node

    def _high_score_leaves(self, knowledge: Knowledge, n: int) -> List[str]:
        pool = list(self.alpha.leaves) + list(self.alpha.groups)
        scored = sorted(pool, key=lambda k: -knowledge.building_block_scores.get(k, 0.0))
        # always include at least the measured leaves so combine/mutate can build interlocks
        keys = scored[:n]
        for m in self.alpha.leaves:
            if m not in keys:
                keys.append(m)
        return keys

    # --- StrategyEvolver.evolve: gradual per-checkpoint nudge ---
    def evolve(self, knowledge: Knowledge):
        hist = knowledge.best_bits_history
        if len(hist) >= 2 and hist[-1] <= hist[-2] + 1e-9:
            self.mutation_rate = min(0.9, self.mutation_rate * 1.1)   # flat -> explore more
        else:
            self.mutation_rate = max(0.1, self.mutation_rate * 0.95)  # improving -> exploit

    # --- radical mutation menu (OVERNIGHT_RUNNER §3), tried in escalation order ---
    def radical_mutation(self, target) -> str:
        menu = [
            self._esc_deepen_alphabet,
            self._esc_switch_filter,    # handled by the runner (filter lives on the gate side)
            self._esc_reweight_targets, # handled by the runner (scheduler)
            self._esc_randomize_mix,
        ]
        idx = self.escalation % len(menu)
        msg = menu[idx](target)
        self.escalation += 1
        self.escalation_log.append(msg)
        return msg

    def _esc_deepen_alphabet(self, target) -> str:
        # bump depth 4->5 once, else rotate the active flavor group A4->S4->D27->triality + sqrt-ratios
        if self.max_depth < 5:
            self.max_depth += 1
            self.bind_target(target)
            return f"DEEPEN: max_depth -> {self.max_depth}"
        order = ["none", "S3", "A4", "S4", "D27"]
        cur = order.index(self.active_group) if self.active_group in order else 0
        self.active_group = order[(cur + 1) % len(order)]
        self.extra_exponents = True
        self.bind_target(target)
        return f"RE-SCOPE ALPHABET: active flavor group -> {self.active_group}, extra exponents ON"

    def _esc_switch_filter(self, target) -> str:
        return "SWITCH FILTER: (runner toggles interlock<->rep<->dimension; see runner log)"

    def _esc_reweight_targets(self, target) -> str:
        return "REWEIGHT SCHEDULER: (runner abandons wall target, pours evals into best-bits target)"

    def _esc_randomize_mix(self, target) -> str:
        self.cfg.p_enumerate = self.rng.uniform(0.3, 0.6)
        rem = 1.0 - self.cfg.p_enumerate
        self.cfg.p_combine = rem * self.rng.uniform(0.3, 0.7)
        self.cfg.p_mutate = rem - self.cfg.p_combine
        self.mutation_rate = self.rng.uniform(0.2, 0.8)
        return (f"RANDOMIZE MIX: enum/comb/mut = "
                f"{self.cfg.p_enumerate:.2f}/{self.cfg.p_combine:.2f}/{self.cfg.p_mutate:.2f}, "
                f"mutation_rate={self.mutation_rate:.2f}; novelty tracker reset")


# ===============================================================================================
# TARGET SCHEDULER  (promising-target weighting; OVERNIGHT_RUNNER §3 esc #3)
# ===============================================================================================

class TargetScheduler:
    """Picks which target to attack each step. Weighted by per-target best-bits & Gate-A pass-rate
    (promising), down-weighted for walls (many tried, 0 surprising). Round-robin warm-start."""
    def __init__(self, target_keys: List[str], rng: random.Random):
        self.keys = list(target_keys)
        self.rng = rng
        self.idx = 0
        self.abandoned: set = set()

    def next_target(self, knowledge: Knowledge) -> str:
        live = [k for k in self.keys if k not in self.abandoned] or self.keys
        # 70% round-robin (systematic coverage), 30% weighted toward promising targets
        if self.rng.random() < 0.3:
            weights = []
            for k in live:
                ts = knowledge.per_target_stats.get(k)
                w = 1.0 + (ts.best_bits if ts else 0.0)
                weights.append(w)
            return self.rng.choices(live, weights=weights, k=1)[0]
        k = live[self.idx % len(live)]
        self.idx += 1
        return k

    def abandon(self, key: str):
        self.abandoned.add(key)


# ===============================================================================================
# CLUE SURFACING  (OVERNIGHT_RUNNER §4) — rewrite results/CLUES.md every checkpoint
# ===============================================================================================

def surface_clues(knowledge: Knowledge, cfg: Config, paths: dict, strat: StrategyState,
                  sched: TargetScheduler, t_start: float, t_end: float):
    now = time.time()
    h_left = max(0.0, (t_end - now) / 3600.0)
    lines = []
    lines.append("# project_atomos — CLUES")
    lines.append("")
    lines.append(f"_Rewritten each checkpoint. {time.strftime('%Y-%m-%d %H:%M:%S')} — "
                 f"{knowledge.n_eval:,} gate-evals, {knowledge.n_leads} certified leads, "
                 f"{h_left:.1f}h left._")
    lines.append("")
    lines.append("Every number below is **uncertainty-aware**: n-sigma agreement with the PDG "
                 "value and **surplus bits relative to the measurement tolerance** (a 6-digit "
                 "match to a 2-digit-known constant is demoted, not credited).")
    lines.append("")

    # --- CERTIFIED LEADS ---
    lines.append("## CERTIFIED LEADS (all three gates pass)")
    leads = _read_jsonl(paths["leads"])
    if not leads:
        lines.append("_None yet. Expected to be empty or Koide-class — that is the honest, "
                     "predicted output if the SM sector is kernel-free._")
    else:
        for L in leads[-20:]:
            lines.append(f"- **{L.get('target')}**: `{L.get('formula')}` — "
                         f"n_sigma={L.get('n_sigma', float('nan')):.2f}, "
                         f"bits={L.get('bits', float('nan')):.1f}, "
                         f"interlock={L.get('interlock_mode')}, "
                         f"forced_factors={L.get('forced_factors')}")
    lines.append("")

    # --- TOP NEAR-MISSES (Gate-A survivors that failed B/C; the leads-in-waiting) ---
    lines.append("## TOP NEAR-MISSES (passed FDR Gate A, failed forced-kernel B or interlock C)")
    lines.append("_These are statistically surprising AND within measurement error, but not yet "
                 "interlocking. The most actionable clue — each tagged with its failing-gate TELL._")
    if not knowledge.near_misses:
        lines.append("")
        lines.append("_None yet._")
    else:
        lines.append("")
        lines.append("| target | formula | n_sigma | fdr_bits | died@ | tell |")
        lines.append("|---|---|---|---|---|---|")
        for nm in knowledge.near_misses[:25]:
            tell = nm.tell.replace("|", "\\|")[:90]
            lines.append(f"| {nm.target} | `{nm.formula[:40]}` | {nm.n_sigma:.2f} | "
                         f"{nm.fdr_bits:.1f} | {nm.gate_failed} | {tell} |")
    lines.append("")

    # --- RECURRING BUILDING BLOCKS ---
    lines.append("## RECURRING BUILDING BLOCKS (appear in Gate-A survivors)")
    lines.append("_A recurring forced-coefficient candidate is the strongest hint at where a real "
                 "kernel might live._")
    bb = sorted(knowledge.building_block_scores.items(), key=lambda kv: -kv[1])
    if not bb:
        lines.append("")
        lines.append("_None yet._")
    else:
        lines.append("")
        for name, sc in bb[:20]:
            lines.append(f"- `{name}` — summed surprise {sc:.1f} bits")
    lines.append("")

    # --- PROMISING vs WALL TARGETS ---
    lines.append("## PROMISING vs WALL TARGETS")
    lines.append("_best-bits & Gate-A pass-rate per target; `wall` = which gate kills most "
                 "candidates (the honest prior: most mass ratios are a Gate-B wall, no forced kernel)._")
    lines.append("")
    lines.append("| target | tried | passed_A | best_bits | best_nσ | wall | best formula |")
    lines.append("|---|---|---|---|---|---|---|")
    stats = sorted(knowledge.per_target_stats.items(),
                   key=lambda kv: -kv[1].best_bits)
    for key, ts in stats:
        ab = " (ABANDONED)" if key in sched.abandoned else ""
        bn = f"{ts.best_n_sigma:.2f}" if math.isfinite(ts.best_n_sigma) else "—"
        lines.append(f"| {key}{ab} | {ts.n_tried} | {ts.n_passed_A} | {ts.best_bits:.1f} | "
                     f"{bn} | {ts.dominant_wall()} | `{ts.best_formula[:36]}` |")
    lines.append("")

    # --- STAGNATION / READJUST LOG ---
    lines.append("## STAGNATION / READJUST LOG (autonomous course-corrections)")
    if not strat.escalation_log:
        lines.append("_No radical mutations fired yet._")
    else:
        for i, e in enumerate(strat.escalation_log[-20:], 1):
            lines.append(f"{i}. {e}")
    lines.append("")
    lines.append(f"_Active strategy: group={strat.active_group}, max_depth={strat.max_depth}, "
                 f"mix enum/comb/mut={cfg.p_enumerate:.2f}/{cfg.p_combine:.2f}/{cfg.p_mutate:.2f}, "
                 f"mutation_rate={strat.mutation_rate:.2f}, novelty_rate={knowledge.novelty_rate():.2f}._")

    paths["clues"].write_text("\n".join(lines))


def _read_jsonl(p: Path) -> List[dict]:
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except Exception:
                pass
    return out


# ===============================================================================================
# LEDGERS + CHECKPOINT
# ===============================================================================================

def ledger_lead(paths: dict, cand: GateCandidate, verdict: Verdict, card: ScoreCard):
    rec = dict(
        target=cand.name.split(":")[0], formula=cand.note,
        n_sigma=card.n_sigma, bits=verdict.fdr.bits,
        status=verdict.status, tell=verdict.tell,
        interlock_mode=verdict.interlock.mode,
        forced_factors=[p for _v, p, _a in verdict.kernel.forced_factors],
        rel_error=card.rel_error,
    )
    with open(paths["leads"], "a") as fh:
        fh.write(json.dumps(rec) + "\n")


def ledger_dead(paths: dict, cand: GateCandidate, verdict: Verdict, card: ScoreCard):
    rec = dict(
        target=cand.name.split(":")[0], formula=cand.note,
        n_sigma=card.n_sigma, bits=verdict.fdr.bits, status=verdict.status,
        tell=verdict.tell,
    )
    with open(paths["dead"], "a") as fh:
        fh.write(json.dumps(rec) + "\n")


def save_checkpoint(paths: dict, knowledge: Knowledge, cfg: Config, strat: StrategyState,
                    sched: TargetScheduler, rng: random.Random, force_bloom: bool = False):
    paths["knowledge"].write_text(json.dumps(knowledge.to_dict()))   # small now (no tried-set inlined)
    ck = dict(
        cfg=dict(run_hours=cfg.run_hours, checkpoint_interval=cfg.checkpoint_interval,
                 stagnation_threshold=cfg.stagnation_threshold, max_depth=cfg.max_depth,
                 seed=cfg.seed, hard_filter=cfg.hard_filter, min_interlock=cfg.min_interlock,
                 p_enumerate=cfg.p_enumerate, p_combine=cfg.p_combine, p_mutate=cfg.p_mutate),
        rng_state=list(rng.getstate()[1]),     # store the mersenne tuple's int list
        rng_pos=rng.getstate()[2],
        strat=dict(active_group=strat.active_group, max_depth=strat.max_depth,
                   extra_exponents=strat.extra_exponents, escalation=strat.escalation,
                   escalation_log=strat.escalation_log, mutation_rate=strat.mutation_rate),
        sched=dict(idx=sched.idx, abandoned=list(sched.abandoned)),
        n_eval=knowledge.n_eval,
    )
    paths["checkpoint"].write_text(json.dumps(ck))
    stats = {k: dict(n_tried=v.n_tried, n_passed_A=v.n_passed_A, best_bits=v.best_bits,
                     wall=v.dominant_wall())
             for k, v in knowledge.per_target_stats.items()}
    paths["stats"].write_text(json.dumps(stats, indent=2))
    # tried-set: compact Bloom filter -> its OWN binary file, on a THROTTLED cadence (decoupled from
    # the per-checkpoint JSON above), written atomically (tmp + replace) so --resume never reads a
    # half-written file. This is the durability fix: knowledge.json stays small, this file is fixed-size.
    now = time.time()
    if force_bloom or (now - knowledge._last_bloom_save) >= BLOOM_SAVE_INTERVAL:
        tmp = paths["bloom"].with_suffix(".bloom.tmp")
        tmp.write_bytes(knowledge.seen_canonical.to_bytes())
        tmp.replace(paths["bloom"])
        knowledge._last_bloom_save = now


def log_progress(paths: dict, msg: str):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(paths["progress"], "a") as fh:
        fh.write(line + "\n")


# ===============================================================================================
# THE MAIN LOOP  (OVERNIGHT_RUNNER §1 skeleton)
# ===============================================================================================

def select_targets(args, ds: pdg.PDGDataset) -> List:
    """Which targets to sweep. --target NAME -> just that one; --all -> the precise dimensionless
    targets (the GOOD search targets, Carl's precision emphasis: aim at the sharp ones)."""
    if args.target:
        if args.target not in ds:
            raise SystemExit(f"unknown target {args.target!r}; known: {', '.join(ds.keys())}")
        return [ds.target(args.target)]
    # --all: precise + dimensionless (ratios/couplings/angles/Q), skip bounds & blunt
    precise = ds.precise_targets(rel_thresh=1e-2)         # rel err < 1% = usable target
    dimless = {t.key for t in ds.dimensionless()}
    out = [t for t in precise if t.key in dimless]
    # always include the live Koide interlock + the famous ratios even if borderline
    for k in ("koide_Q_lep", "r_mu_e", "r_p_e", "pmns_sin2_13", "ckm_lambda"):
        if k in ds and ds.target(k) not in out:
            out.append(ds.target(k))
    return out


def run(args):
    results = Path(args.results_dir) if getattr(args, "results_dir", None) else RESULTS
    results.mkdir(parents=True, exist_ok=True)
    paths = _paths(results)
    ds = pdg.load()

    cfg = Config(run_hours=args.hours, checkpoint_interval=args.checkpoint, seed=args.seed,
                 geometric_mode=bool(getattr(args, "geometric", False)))
    rng = random.Random(cfg.seed)
    knowledge = Knowledge(_bloom_bits_for_hours(args.hours))   # size the tried-set to the run length

    # --- resume (OVERNIGHT_RUNNER §1: load_checkpoint_if_exists) ---
    if args.resume and paths["checkpoint"].exists():
        ck = json.loads(paths["checkpoint"].read_text())
        if paths["knowledge"].exists():
            knowledge = Knowledge.from_dict(json.loads(paths["knowledge"].read_text()))
        # restore the tried-set from its compact binary (not from knowledge.json)
        if paths["bloom"].exists():
            knowledge.seen_canonical = BloomFilter.from_bytes(paths["bloom"].read_bytes())
        c = ck.get("cfg", {})
        cfg.max_depth = c.get("max_depth", cfg.max_depth)
        cfg.p_enumerate = c.get("p_enumerate", cfg.p_enumerate)
        cfg.p_combine = c.get("p_combine", cfg.p_combine)
        cfg.p_mutate = c.get("p_mutate", cfg.p_mutate)
        try:
            rng.setstate((3, tuple(ck["rng_state"]) + (ck["rng_pos"],), None))
        except Exception:
            pass
        log_progress(paths, f"RESUMED from checkpoint at {knowledge.n_eval:,} evals.")

    targets = select_targets(args, ds)
    sched = TargetScheduler([t.key for t in targets], rng)
    target_by_key = {t.key: t for t in targets}
    n_targets = len(targets)

    strat = StrategyState(cfg, rng)
    # restore strategy state on resume
    if args.resume and paths["checkpoint"].exists():
        s = json.loads(paths["checkpoint"].read_text()).get("strat", {})
        strat.active_group = s.get("active_group", "none")
        strat.max_depth = s.get("max_depth", cfg.max_depth)
        strat.extra_exponents = s.get("extra_exponents", False)
        strat.escalation = s.get("escalation", 0)
        strat.escalation_log = s.get("escalation_log", [])
        strat.mutation_rate = s.get("mutation_rate", 0.3)

    # per-target enumerators: we bind the strategy to whichever target the scheduler picks; to keep
    # enumerators alive across steps we cache one StrategyState-bound generator per target.
    bound: Dict[str, StrategyState] = {}

    def strat_for(target) -> StrategyState:
        st = bound.get(target.key)
        if st is None:
            st = StrategyState(cfg, rng)
            st.active_group = strat.active_group
            st.max_depth = strat.max_depth
            st.extra_exponents = strat.extra_exponents
            st.geometric_mode = strat.geometric_mode   # carry the forced-geometric germ restriction
            st.mutation_rate = strat.mutation_rate
            st.escalation_log = strat.escalation_log  # share the readjust log
            st.bind_target(target)
            bound[target.key] = st
        return st

    t_start = time.time()
    t_end = t_start + cfg.run_hours * 3600.0
    log_progress(paths, f"START: {n_targets} targets, {cfg.run_hours}h, seed={cfg.seed}, "
                        f"filter={cfg.hard_filter}, geometric_mode={cfg.geometric_mode}, "
                        f"checkpoint every {cfg.checkpoint_interval} evals.")
    log_progress(paths, f"targets: {', '.join(t.key for t in targets)}")

    consecutive_exhausted = 0
    while time.time() < t_end:
        tkey = sched.next_target(knowledge)
        target = target_by_key[tkey]
        st = strat_for(target)

        proposal = st.propose(knowledge)
        if proposal is None:
            # this target's enumerator is exhausted -> a per-target stagnation signal
            consecutive_exhausted += 1
            knowledge.note_novelty(False)
            if consecutive_exhausted >= n_targets:
                # every target exhausted at current depth/group -> force a radical mutation
                _fire_radical_mutation(knowledge, cfg, strat, st, sched, target, paths, bound)
                consecutive_exhausted = 0
            continue
        consecutive_exhausted = 0
        tree, was_novel = proposal
        knowledge.note_novelty(was_novel)
        if not was_novel:
            continue  # already judged this canonical tree (cross-checkpoint dedup) — skip gate work
        knowledge.seen_canonical.add(tree.canonical_hash())

        # --- evaluate the tree, score uncertainty-aware ---
        try:
            value, label = tree.evaluate(st.alpha)
        except Exception:
            continue
        if not _finite_pos(value):
            continue
        card = score_value(float(value), target)

        # ADVISORY pre-gate cut (engine closeness): only hand the gate candidates that at least
        # land within a generous multiple of the measurement window. Far-off trees are not even
        # candidates (this is the engine's cheap structural+closeness filter; the gate decides
        # real-vs-coincidence on what survives). We use 3-sigma OR within the search tolerance.
        if not (card.within_2sigma or card.rel_error < measurement_tol(target) * 3):
            # still credit the tried-set; just don't gate it
            continue

        # --- build the gate's structured claim + run the 3-part gate (THE fitness function) ---
        cand, blocks = build_gate_candidate(tree, st.alpha, tkey, target, float(value),
                                            n_targets, card)
        try:
            verdict = validate(cand)
        except Exception:
            traceback.print_exc()
            continue

        knowledge.record(tkey, cand, verdict, card, tree.canonical_hash(), blocks)
        if verdict.status == "CERTIFIED":
            knowledge.n_leads += 1
            ledger_lead(paths, cand, verdict, card)
            log_progress(paths, f"*** LEAD on {tkey}: {cand.note} "
                                f"(n_sigma={card.n_sigma:.2f}, bits={verdict.fdr.bits:.1f}) ***")
        else:
            ledger_dead(paths, cand, verdict, card)

        # --- checkpoint + evolve + stagnation (by gate-eval count) ---
        if knowledge.n_eval % cfg.checkpoint_interval == 0:
            knowledge.best_bits_history.append(knowledge.best_bits_overall)
            strat.evolve(knowledge)
            st.evolve(knowledge)
            if knowledge.stagnant(cfg.stagnation_threshold):
                _fire_radical_mutation(knowledge, cfg, strat, st, sched, target, paths, bound)
                knowledge.reset_stagnation()
            surface_clues(knowledge, cfg, paths, strat, sched, t_start, t_end)
            save_checkpoint(paths, knowledge, cfg, strat, sched, rng)
            h_left = max(0.0, (t_end - time.time()) / 3600.0)
            log_progress(paths, f"CKPT | {knowledge.n_eval:,} evals | {knowledge.n_leads} leads | "
                                f"best_bits={knowledge.best_bits_overall:.1f} | "
                                f"near_misses={len(knowledge.near_misses)} | "
                                f"novelty={knowledge.novelty_rate():.2f} | {h_left:.1f}h left")
            gc.collect()

    # --- finalize ---
    knowledge.best_bits_history.append(knowledge.best_bits_overall)
    surface_clues(knowledge, cfg, paths, strat, sched, t_start, t_end)
    save_checkpoint(paths, knowledge, cfg, strat, sched, rng, force_bloom=True)  # final: flush the tried-set
    log_progress(paths, f"DONE: {knowledge.n_eval:,} gate-evals, {knowledge.n_leads} certified "
                        f"leads, {len(knowledge.near_misses)} near-misses. See {paths['clues']}.")
    _finalize_report(knowledge, paths)


def _fire_radical_mutation(knowledge, cfg, strat, st, sched, target, paths, bound):
    """Fire the next escalation. Escalations 2 (switch filter) & 3 (reweight scheduler) are
    runner-side; 1 (deepen/re-scope alphabet) & 4 (randomize mix) live on the StrategyState."""
    msg = strat.radical_mutation(target)
    # propagate alphabet/depth/group/mix changes to ALL bound enumerators (re-scope is global)
    for st2 in bound.values():
        st2.active_group = strat.active_group
        st2.max_depth = strat.max_depth
        st2.extra_exponents = strat.extra_exponents
        st2.mutation_rate = strat.mutation_rate
    # rebind so the change takes effect immediately
    bound.clear()
    # runner-side escalation #3: abandon the worst wall target, if we have many
    if "REWEIGHT" in msg:
        walls = [(k, v) for k, v in knowledge.per_target_stats.items()
                 if v.n_tried > 50 and v.best_bits < 1.0 and k not in sched.abandoned]
        if walls and len(sched.keys) - len(sched.abandoned) > 1:
            worst = max(walls, key=lambda kv: kv[1].n_tried)[0]
            sched.abandon(worst)
            msg += f" -> abandoned wall target '{worst}'"
    log_progress(paths, f"RADICAL MUTATION #{strat.escalation}: {msg}")


def _finalize_report(knowledge: Knowledge, paths: dict):
    log_progress(paths, "=" * 70)
    log_progress(paths, "FINAL REPORT")
    log_progress(paths, f"  certified leads : {knowledge.n_leads}")
    log_progress(paths, f"  near-misses     : {len(knowledge.near_misses)} (Gate-A survivors)")
    promising = sorted(knowledge.per_target_stats.items(), key=lambda kv: -kv[1].best_bits)[:5]
    log_progress(paths, "  top targets by best-bits:")
    for k, ts in promising:
        log_progress(paths, f"    {k}: best_bits={ts.best_bits:.1f}, wall={ts.dominant_wall()}, "
                            f"tried={ts.n_tried}")


def _finite_pos(v) -> bool:
    try:
        return mp.isfinite(v) and v > 0
    except Exception:
        return False


# ===============================================================================================
# CALIBRATION  (the acceptance test — re-find a0, certify Koide, reject the dead re-labelings)
# ===============================================================================================

def calibrate():
    """Run the GATE_SPEC acceptance test directly (no overnight loop): the gate must certify a0's
    forced kernel + Koide, and reject the 164-class dead re-labelings. Imports the calibration
    module if present, else runs an inline minimal check on the engine + gate."""
    print("=" * 70)
    print("CALIBRATION — acceptance test (must certify a0 + Koide, reject dead re-labelings)")
    print("=" * 70)
    # 1) engine re-finds the a0 candidate c*H0/Z
    from engine.alphabet import build_a0_alphabet
    from engine.expr_tree import ACCELERATION
    from engine.search import Search
    a = build_a0_alphabet()
    s = Search(a, target_value=1.2e-10, target_label=ACCELERATION, tol=0.10,
               max_depth=3, hard_filter="dimension")
    cands = s.run(top_k=10, verbose=False)
    found = any("Z)" in c.formula or "kern" in c.formula for c in cands)
    print(f"[1] engine re-finds a0 forced-kernel candidate (cH0/Z): "
          f"{'PASS' if found else 'FAIL'}")
    for c in cands[:5]:
        print(f"      {c.rel_error:7.4f}  {c.formula}")

    # 2) gate certifies a0's forced kernel (hand-built canonical candidate)
    a0 = GateCandidate(
        name="a0", target_value=1.19e-10, relation_value=1.19e-10,
        search=SearchSpace(germ_pool={"2": 2.0, "pi": math.pi, "3": 3.0}, tol=0.01,
                           n_digits_known=2.0),
        coefficient=Coefficient(
            factors=[Factor(math.sqrt(8 * math.pi), "einstein_8pi", ["Einstein"]),
                     Factor(math.sqrt(1 / 3), "friedmann_third", ["Friedmann"])],
            free_params=1, target_value=None, form_forced_independently=1),
        interlock=Interlock(n_independent_observables=3),
    )
    va0 = validate(a0)
    print(f"[2] gate certifies a0 forced kernel: "
          f"{'PASS' if va0.kernel.passed and va0.interlock.passed else 'FAIL'} "
          f"(B={va0.kernel.passed}, C={va0.interlock.passed}) — {va0.kernel.tell[:70]}")

    # 3) Koide: real interlock (C2), kernel-free mechanism -> REAL-PUZZLE-RE-LABELED
    import numpy as np
    ds = pdg.load()
    Q = ds.target("koide_Q_lep")
    def koide_null(N):
        m = np.exp(np.random.uniform(np.log(1e-2), np.log(1e4), size=(N, 3)))
        sm = np.sqrt(m)
        return m.sum(1) / sm.sum(1) ** 2
    koide = GateCandidate(
        name="koide", target_value=2 / 3, relation_value=float(Q.value),
        # eps=1e-5 recovers the documented ~1-in-44,000 (15.4 bits) random-mass-triple null;
        # n_digits_known=16 so the precision cap doesn't bite (2/3 is exact, not measured).
        search=SearchSpace(rational_target=True, structural_null=koide_null,
                           structural_eps=1e-5, structural_N=2_000_000, n_digits_known=16.0),
        coefficient=Coefficient(
            factors=[Factor(math.sqrt(2), "S3_doublet_amp_sqrt2", ["S3"])],
            free_params=2, target_value=None),  # r=sqrt2 + per-fermion k = TWO free numbers
        interlock=Interlock(n_constants_tied=3, n_free_in_interlock=0, claimed_universal=False),
    )
    vk = validate(koide)
    print(f"[3] Koide -> {vk.status} "
          f"({'PASS' if vk.status == 'REAL-PUZZLE-RE-LABELED' else 'CHECK'}): "
          f"A={vk.fdr.passed}(bits={vk.fdr.bits:.1f}), B={vk.kernel.passed}, C={vk.interlock.passed}")

    # 4) reject a dead re-labeling (4Z^2+3 -> alpha_inv); BAKED / no provenance
    Z = math.sqrt(32 * math.pi / 3)
    dead = GateCandidate(
        name="4Z2+3", target_value=137.035999, relation_value=4 * Z ** 2 + 3,
        search=SearchSpace(germ_pool={f"{i}": float(i) for i in range(2, 20)} |
                          {"pi": math.pi, "Z": Z, "Z2": Z ** 2}, tol=1e-4, n_digits_known=9.0),
        coefficient=Coefficient(factors=[Factor(4.0, None), Factor(3.0, None)], free_params=2),
        interlock=Interlock(n_independent_observables=0, n_constants_tied=1),
    )
    vd = validate(dead)
    print(f"[4] 4Z^2+3 (dead re-labeling) -> {vd.status} "
          f"({'PASS-rejected' if vd.status == 'FDR-DEAD' else 'FAIL-not-rejected'}): {vd.tell[:80]}")
    print("=" * 70)
    print("calibration/ acceptance harness: see calibration/ for the full 164-dead ledger.")


# ===============================================================================================
# CLI
# ===============================================================================================

def main():
    ap = argparse.ArgumentParser(
        description="project_atomos overnight autoresearch runner — uncertainty-aware, gate-scored.")
    ap.add_argument("--hours", type=float, default=24.0, help="run duration (default 24)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--target", type=str, default=None, help="single target key (e.g. r_mu_e)")
    g.add_argument("--all", action="store_true", help="sweep all precise dimensionless targets")
    ap.add_argument("--checkpoint", type=int, default=200, help="gate-evals between checkpoints")
    ap.add_argument("--resume", action="store_true", help="resume from results/checkpoint.json")
    ap.add_argument("--seed", type=int, default=1234, help="RNG seed (logged, reproducible)")
    ap.add_argument("--results-dir", type=str, default=None,
                    help="output dir (default results/); the parallel launcher gives each worker its own shard")
    ap.add_argument("--calibrate", action="store_true",
                    help="run the acceptance test (a0 + Koide + dead) and exit")
    ap.add_argument("--geometric", action="store_true",
                    help="GEOMETRIC MODE: restrict the dimensionless-factor (germ) pool to the "
                         "FORCED-GEOMETRIC primitives of targets/geometric_primitives.forced_pool() "
                         "(rep dims, |G|, measure-pi, root/polytope angles, Coxeter/Dynkin/Casimir, "
                         "forced structural rationals) instead of arbitrary integers + transcendentals "
                         "— the a0 discipline: a sparser reachable set means a hit earns real bits")
    args = ap.parse_args()

    if args.calibrate:
        calibrate()
        return
    if not args.target and not args.all:
        args.all = True  # default to sweeping all precise targets
    run(args)


if __name__ == "__main__":
    main()
