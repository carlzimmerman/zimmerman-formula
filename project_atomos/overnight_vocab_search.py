#!/usr/bin/env python3
"""
overnight_vocab_search.py — the FORCED-VOCABULARY overnight search.

WHAT THIS IS (Carl's brief, 2026-07-07)
    Depth is EXHAUSTED over the committed forced vocabulary {3 (Ngen_3), sqrt(8pi/3)
    (a0_kernel_8pi3)}: depth-3/4/5 are committed CLEAN NULLS. The ONLY remaining axis that could
    surface a certified SM hit is a NEW FORCED GERM that legitimately OVERDETERMINES — a germ whose
    value is pinned by a declared symmetry law BEFORE fitting AND that appears in >=2 independent
    forced places. This runner tests candidate new forced germs (pre-registered symmetry invariants,
    each WITH its forcing law) across depths and all 21 SM targets, logging at each level, all night.

    THE HONEST PRIOR IS NULL (the committed number-field obstruction: a0/Z carries sqrt(pi),
    transcendental; the flavor data is algebraic -> a0/Z is structurally gauge-blind). This is honest
    due diligence, NOT a promise of a hit. A clean null is the expected, valid outcome.

RULE 3 (verbatim reuse). gate/ and engine/ and exhaust*/ are imported UNMODIFIED. This file:
  * reuses exhaust_depth5_forced's CONSTRUCTIVE, STREAMING, Gate-B-passable per-(depth) enumerator
    (peak ~0.4 GB, ~28 s to build; completeness+soundness self-checked);
  * registers each CANDIDATE FORCED GERM in a COPY of gate.registry.FORCED_CONSTRAINTS (with its
    law) so _germ_provenance can grant it forced credit — WITHOUT weakening the gate;
  * wires the FULL look-elsewhere multiplicity mult = n_targets x n_germs x n_depths x n_recipes
    into the gate's n_targets_searched (the #1 anti-fabrication invariant);
  * bounds the seen-set (streaming value-dedup only) + a HARD RSS watchdog < 4 GB;
  * logs one structured line PER LEVEL (level = one candidate germ x depth) all night.

WHY ADDING CANDIDATE GERMS CANNOT CHEAT THE GATE (the core of the design)
  * Gate B (forced_kernel) requires OVERDETERMINATION: len(Fset)==2 DISTINCT forced provenance keys
    present in the tree (exhaust_depth4_forced._keep_completed, verbatim). A germ registered ONCE is a
    definition, not a kernel -> it supplies at most ONE forced key -> the tree still needs a SECOND
    independent forced appearance. Registering candidate germs does NOT relax that.
  * Gate A (fdr) folds the ENTIRE search into the look-elsewhere multiplicity. Trying MORE candidate
    germs RAISES the bar: a hit must clear PASS_BITS=10 surplus bits AFTER dividing by
    n_targets x n_germs x n_depths x n_recipes. Volume cannot buy a certification.
  * The germ POOL stays FIXED at 25 (assert len(alpha.germs)==25 preserved). A candidate germ is
    injected as a per-config REGISTRY entry (provenance law), not as a new pool member that would
    inflate the FDR library. The FDR library the surprise is measured against is unchanged.

CLI
    python3 overnight_vocab_search.py --list-germs     # print the curated candidate germ list + laws
    python3 overnight_vocab_search.py --dry-run        # one (germ,depth) config, print the FDR mult
    python3 overnight_vocab_search.py --hours 10       # the overnight loop (default 10h)
    python3 overnight_vocab_search.py --hours 10 --resume
"""
from __future__ import annotations

import argparse
import json
import math
import os
import resource
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

# --- RULE 3: import the gate, engine, and the committed constructive machinery VERBATIM ---
import gate.registry as REG                                   # noqa: E402  (we COPY, never mutate)
from targets import geometric_primitives as GP                # noqa: E402
import exhaust as EX                                          # noqa: E402
from exhaust import build_alphabet, Alphabet, Reachable       # noqa: E402
from exhaust_parallel import sm_target_keys                   # noqa: E402  (the canonical 21 targets)
import exhaust_depth5_forced as D5                            # noqa: E402
from engine.scoring import score_value, measurement_tol       # noqa: E402
from gate import validate                                     # noqa: E402

RESULTS = _HERE / "results_overnight_vocab"
RESULTS.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# HARD MEMORY WATCHDOG < 4 GB  (Carl's brief: a depth-5 run thrashed 64 GB; fix is non-negotiable)
#   The constructive scheme streams (bounded dedup sets only), peaking ~0.4 GB. Any breach of 4 GB is
#   a BUG, not a reason to raise the cap. We sample SELF+CHILDREN RSS and ABORT with a clear message.
# ---------------------------------------------------------------------------
HARD_MEM_CAP_GB = 4.0
_MEM_CAP_MB = HARD_MEM_CAP_GB * 1024.0


def _rss_mb(which) -> float:
    ru = resource.getrusage(which).ru_maxrss
    return ru / (1024 * 1024) if sys.platform == "darwin" else ru / 1024


def _total_rss_mb() -> float:
    return _rss_mb(resource.RUSAGE_SELF) + _rss_mb(resource.RUSAGE_CHILDREN)


def _mem_watchdog(where: str = ""):
    tot = _total_rss_mb()
    if tot > _MEM_CAP_MB:
        raise SystemExit(
            f"MEMORY WATCHDOG ABORT{(' @ ' + where) if where else ''}: total RSS {tot/1024:.2f} GB "
            f"exceeded the HARD {HARD_MEM_CAP_GB:.0f} GB cap. The constructive scheme must stream "
            f"(peak ~0.4 GB); a breach means a non-streaming/leaking path — FIX the bug, do NOT raise "
            f"the cap.")


# ===========================================================================
# 1. THE CANDIDATE FORCED-GERM LIST  (pre-registered symmetry invariants, each WITH its law)
#
#    CURATED from targets.geometric_primitives.forced_pool() + gate.registry — the discrete-flavor
#    rep dims / group orders / Clebsch rationals and GUT norms already in the corpus. Each candidate
#    is a (key, value, law) triple: the value is pinned by the named symmetry BEFORE fitting; the law
#    is the pre-fit declaration Gate B's discipline requires. NO number is hand-typed to fit a target
#    — every value is pulled from the pre-registered forced primitive.
#
#    NOTE ON PROVENANCE COLLISIONS (honest, load-bearing): _germ_provenance returns the FIRST matching
#    registry key, and Gate B counts DISTINCT provenance keys. Several candidates share a VALUE with an
#    already-forced germ (A4_irrep3=3.0 == Ngen_3; S3_irrep2=2.0; etc.). A candidate that merely
#    re-labels an existing forced value adds NO new independent forced place -> cannot manufacture the
#    2nd overdetermined appearance. That is the mechanism, not a bug: it is WHY volume cannot cheat.
# ===========================================================================

@dataclass(frozen=True)
class CandidateGerm:
    key: str          # the NEW forced-provenance registry key
    value: float      # forced value (pulled from a pre-registered forced primitive)
    law: str          # the symmetry law that forces it (the pre-fit declaration)
    source: str       # the geometric_primitives / registry key it is drawn from


def _gp(key: str) -> float:
    return float(GP.get(key).value)


def candidate_germs() -> List[CandidateGerm]:
    """The FIXED candidate forced-germ set (declared BEFORE running; no fitting). Drawn from the
    pre-registered forced primitives: discrete-flavor group orders + irrep dims + Clebsch rationals,
    GUT rep dims / norms, Weyl/Coxeter invariants, Koide circulant rationals."""
    C: List[CandidateGerm] = []

    def add(key, value, law, source):
        C.append(CandidateGerm(key, float(value), law, source))

    # --- discrete flavor-group orders + irrep dims (the mixing/flavor Gate-B pool) ---
    add("A4_irrep3", _gp("A4_irrep3"), "A4 discrete flavor symmetry: dim of the 3-irrep (holds 3 "
        "generations); forced by the group's rep theory", "A4_irrep3")
    add("A4_order", _gp("A4_order"), "|A4| = 12 (tetrahedral group order), forced discrete invariant",
        "A4_order")
    add("S4_irrep3", _gp("S4_irrep3"), "S4: dim of a 3-irrep (octahedral), forced rep dimension",
        "S4_irrep3")
    add("S4_order", _gp("S4_order"), "|S4| = 24 (octahedral group order), forced discrete invariant",
        "S4_order")
    add("S3_order", _gp("S3_order"), "|S3| = 6 (smallest non-abelian; hosts the Koide circulant "
        "1+2 split), forced discrete invariant", "S3_order")
    add("S3_irrep2", _gp("S3_irrep2"), "S3: dim of the 2-irrep (the doublet), forced rep dimension",
        "S3_irrep2")
    add("D27_order", _gp("D27_order"), "|Delta(27)| = 27 = (Z3xZ3) rtimes Z3, forced discrete "
        "invariant", "D27_order")
    add("A4_n_vert", _gp("A4_n_vert"), "tetrahedron vertices = 4 (A4 polytope), forced count",
        "A4_n_vert")
    add("A4_n_edge", _gp("A4_n_edge"), "tetrahedron edges = 6 (A4 polytope), forced count",
        "A4_n_edge")
    add("cube_n_vert", _gp("cube_n_vert"), "cube vertices = 8 (S4 polytope), forced count",
        "cube_n_vert")
    add("cube_n_edge", _gp("cube_n_edge"), "cube edges = 12 (S4 polytope), forced count",
        "cube_n_edge")

    # --- GUT embedding invariants (rep dims, group orders, Weyl/Coxeter — forced by rep theory) ---
    add("dim_su5", _gp("dim_su5"), "dim SU(5) = 5^2-1 = 24, forced group dimension", "dim_su5")
    add("dim_so10", _gp("dim_so10"), "dim SO(10) = 10*9/2 = 45, forced group dimension", "dim_so10")
    add("dim_e6", _gp("dim_e6"), "dim E6 = 78, forced group dimension", "dim_e6")
    add("gen_su5", _gp("gen_su5"), "SU(5) one generation 5bar+10 = 15 (multiplet closure), forced "
        "rep dimension", "gen_su5")
    add("gen_so10", _gp("gen_so10"), "SO(10) spinor 16 = 15 + nu_R (one generation), forced rep "
        "dimension", "gen_so10")
    add("gen_e6", _gp("gen_e6"), "E6 fundamental 27 = 16+10+1 (one generation), forced rep "
        "dimension", "gen_e6")
    add("coxeter_su5", _gp("coxeter_su5"), "Coxeter number h(A4=SU5) = 5, forced root-system "
        "invariant", "coxeter_su5")
    add("coxeter_e6", _gp("coxeter_e6"), "Coxeter number h(E6) = 12, forced root-system invariant",
        "coxeter_e6")
    add("gut_norm_5_3", _gp("gut_norm_5_3"), "GUT hypercharge normalization g1^2_GUT = (5/3) g_Y^2, "
        "forced by the common Tr(T^2) over a complete SU(5) multiplet", "gut_norm_5_3")

    # --- GUT / gauge Clebsch + beta rationals (forced by trace identities / rep-dim sums) ---
    add("sin2_thetaW_tree", _gp("sin2_thetaW_tree"), "sin^2 theta_W (tree, GUT) = Tr(T3^2)/Tr(Q^2) "
        "= 3/8 over a complete SU(5) multiplet, forced Clebsch", "sin2_thetaW_tree")
    add("dynkin_fund", _gp("dynkin_fund"), "T(fund) = 1/2 for every SU(N) (Dynkin index "
        "normalization), forced", "dynkin_fund")

    # --- Koide / circulant + tri-bimaximal Clebsch rationals (the flavor-geometry pool) ---
    add("koide_floor", _gp("koide_floor"), "Koide democratic floor Q = 1/3 + r^2/6 (S3/Z3 circulant "
        "identity, delta-independent); the 1/3 is forced", "koide_floor")
    add("koide_ampl_coeff", _gp("koide_ampl_coeff"), "Koide doublet-amplitude coefficient 1/6 (the "
        "r^2/6 term of the circulant identity), forced", "koide_ampl_coeff")
    add("koide_cos2_angle", _gp("koide_cos2_angle"), "cos^2(sqrt-mass angle to (1,1,1)) = 1/(3Q); "
        "at Q=2/3 -> 1/2 (45 deg), forced-given-Q trig identity", "koide_cos2_angle")
    add("tbm_sin2_12", _gp("tbm_sin2_12"), "TBM sin^2 theta_12 = 1/3 (A4/S4 Clebsch), forced pattern "
        "value", "tbm_sin2_12")
    add("tbm_sin2_23", _gp("tbm_sin2_23"), "TBM sin^2 theta_23 = 1/2 (maximal, mu-tau symmetry), "
        "forced pattern value", "tbm_sin2_23")

    return C


# ===========================================================================
# 2. INJECT ONE CANDIDATE GERM INTO A COPY OF THE FORCED REGISTRY  (NEVER mutate the real one)
#
#    A candidate germ earns forced credit ONLY IF its value maps to a registry provenance key. We add
#    the candidate as a NEW entry (key -> value, law) in a COPY of FORCED_CONSTRAINTS, then swap that
#    copy in for the duration of one config via a context manager. gate.registry.FORCED_CONSTRAINTS is
#    the SAME dict object exhaust._germ_provenance iterates (imported by reference), so patching it
#    (and restoring it) is how the candidate germ becomes visible to the gate's forced-credit path —
#    without touching gate SCORING (RULE 3: we add a declared law, we do not weaken any threshold).
# ===========================================================================

class candidate_registered:
    """Context manager: temporarily register ONE candidate germ (key, value, law) in the forced
    registry, restoring the exact original dict on exit. Refuses to overwrite an existing key."""

    def __init__(self, cg: CandidateGerm):
        self.cg = cg
        self._orig: Optional[dict] = None

    def __enter__(self):
        self._orig = dict(REG.FORCED_CONSTRAINTS)   # shallow snapshot of the real registry
        if self.cg.key not in REG.FORCED_CONSTRAINTS:
            REG.FORCED_CONSTRAINTS[self.cg.key] = dict(
                value=self.cg.value, desc=f"[candidate] {self.cg.source}", law=self.cg.law)
        return self

    def __exit__(self, *exc):
        REG.FORCED_CONSTRAINTS.clear()
        REG.FORCED_CONSTRAINTS.update(self._orig)
        return False


# ===========================================================================
# 3. THE FULL LOOK-ELSEWHERE MULTIPLICITY  (the #1 anti-fabrication invariant)
#
#    mult = n_targets x n_germs x n_depths x n_recipes  — EVERY trial the overnight loop performs.
#    This is threaded into the gate via exhaust.gate_candidate_for(..., n_targets_searched=mult),
#    which sets SearchSpace.n_targets_searched, which gate/fdr.fdr_test reads at line 150
#    (mult = max(1, s.n_targets_searched)) and divides the chance probability by. Folding only
#    n_targets (the depth-5 default of 21) would be the BUG the brief warns about; here we fold the
#    WHOLE search.
#
#    n_recipes = the constructive recipe count PER (germ, depth) config = distinct dimensionless
#    Gate-B-passable VALUES generated at that depth (D5.constructive_gate_b_reachables count). This is
#    the exact number of expressions actually scored per target per config — the honest per-config
#    trial count.
# ===========================================================================

def full_multiplicity(n_targets: int, n_germs: int, depths: List[int], n_recipes_by_depth: Dict[int, int]) -> int:
    """mult = n_targets x n_germs x n_depths x (sum of per-depth recipe counts). We use the SUMMED
    recipe count across depths so the total equals n_targets x n_germs x (total expressions scored),
    i.e. every (target, germ, depth, expression) trial in the whole night is counted exactly once."""
    total_recipes = sum(n_recipes_by_depth.get(d, 0) for d in depths)
    return max(1, n_targets * n_germs * total_recipes)


# ===========================================================================
# 4. PER-(germ, depth) CONFIG SEARCH  (reuse the committed constructive machinery, streamed)
# ===========================================================================

@dataclass
class BestHit:
    target: str = ""
    formula: str = ""
    value: float = float("nan")
    rel_err: float = float("inf")
    status: str = "NONE"
    fdr_bits: float = float("nan")

    def as_dict(self):
        return dict(target=self.target, formula=self.formula, value=self.value,
                    rel_err=self.rel_err, status=self.status, fdr_bits=self.fdr_bits)


def build_reach_for_depth(alpha: Alphabet, depth: int) -> Tuple[List[Reachable], int]:
    """Build the constructive Gate-B-passable dimensionless reachable set at `depth` ONCE (streamed,
    value-deduped). Returns (reach, n_recipes). depth 5 is the substantive level; depths 3/4 are the
    committed-null anchors (dimensionless Gate-B set is empty there -> n_recipes 0, fast)."""
    # exhaust_depth5_forced.constructive_gate_b_reachables supports depth in {4,5} for the
    # dimensionless path; depth 3 has no 2-scale dimensionless skeleton (empty), so we treat <5 via
    # the same builder (depth 4) and depth 3 as the trivial empty set.
    if depth >= 5:
        reach, counts = D5.constructive_gate_b_reachables(alpha, max_depth=5, dimensionless_only=True)
    elif depth == 4:
        reach, counts = D5.constructive_gate_b_reachables(alpha, max_depth=4, dimensionless_only=True)
    else:
        reach, counts = [], {"distinct_by_value": 0}
    return reach, int(counts.get("distinct_by_value", len(reach)))


def score_config(alpha: Alphabet, reach: List[Reachable], targets: List[str],
                 mult: int) -> Tuple[BestHit, int, int]:
    """Score the constructive reachable set against all targets under the FULL multiplicity `mult`.
    Returns (best_hit_across_targets, n_certified, n_relabeled). STREAMS: holds only the running
    best, never a materialized per-hit list."""
    best = BestHit()
    n_cert = 0
    n_relabel = 0
    for tk in targets:
        tspec = EX.resolve_target(tk)
        tol = measurement_tol(tspec.pdg_target)
        for r in reach:
            card = score_value(float(r.value), tspec.pdg_target)
            if card.rel_error > tol:
                continue
            gc = EX.gate_candidate_for(r, alpha, tk, tspec.pdg_target, mult)  # <-- FULL mult wired
            v = validate(gc)
            if v.status == "CERTIFIED":
                n_cert += 1
            elif v.status == "REAL-PUZZLE-RE-LABELED":
                n_relabel += 1
            if card.rel_error < best.rel_err:
                best = BestHit(target=tk, formula=r.formula, value=float(r.value),
                               rel_err=card.rel_error, status=v.status, fdr_bits=float(v.fdr.bits))
    return best, n_cert, n_relabel


# ===========================================================================
# 5. PER-LEVEL LOGGING  (Carl's explicit ask: "log at each level")
# ===========================================================================

def _log_paths(stamp: str) -> Tuple[Path, Path]:
    return (RESULTS / f"vocab_search_{stamp}.jsonl",
            RESULTS / f"vocab_search_{stamp}.summary.txt")


def append_level_log(jsonl: Path, summary: Path, row: dict):
    with jsonl.open("a") as f:
        f.write(json.dumps(row) + "\n")
        f.flush()
        os.fsync(f.fileno())
    line = (f"[{row['counter']:04d}] germ={row['germ_key']:<18} d={row['depth']} "
            f"ntgt={row['n_targets']:2d} recipes={row['n_recipes']:>6} "
            f"best={row['best']['target']}:{row['best']['status']} "
            f"rel_err={row['best']['rel_err']:.2e} FDRbits={row['best']['fdr_bits']:+.1f} "
            f"mult={row['fdr_mult']:.3e} CERTcum={row['certified_cumulative']} "
            f"t={row['elapsed_s']:.0f}s peakRSS={row['peak_rss_gb']:.2f}GB")
    with summary.open("a") as f:
        f.write(line + "\n")
        f.flush()
        os.fsync(f.fileno())
    print(line)


# ===========================================================================
# 6. THE --hours OVERNIGHT LOOP
# ===========================================================================

def run_overnight(hours: float, resume: bool = False):
    stamp = time.strftime("%Y%m%dT%H%M%S")
    jsonl, summary = _log_paths(stamp)
    t0 = time.time()
    deadline = t0 + hours * 3600.0

    targets = sm_target_keys()
    n_targets = len(targets)
    germs = candidate_germs()
    n_germs = len(germs)
    depths = [5, 4, 3]                      # 5 = substantive; 4/3 = committed-null anchors

    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25, f"FDR non-smuggle: germ pool must be 25, got {len(alpha.germs)}"
    _mem_watchdog("startup")

    # Build each depth's reachable set ONCE (target- AND germ-independent), for n_recipes + reuse.
    reach_by_depth: Dict[int, List[Reachable]] = {}
    n_recipes_by_depth: Dict[int, int] = {}
    for d in depths:
        reach_by_depth[d], n_recipes_by_depth[d] = build_reach_for_depth(alpha, d)
        _mem_watchdog(f"build-depth-{d}")

    mult = full_multiplicity(n_targets, n_germs, depths, n_recipes_by_depth)

    header = {
        "run_started": stamp, "hours": hours, "n_targets": n_targets, "n_germs": n_germs,
        "depths": depths, "n_recipes_by_depth": n_recipes_by_depth,
        "fdr_full_multiplicity": mult,
        "fdr_mult_formula": "n_targets x n_germs x sum_depth(n_recipes) "
                            f"= {n_targets} x {n_germs} x {sum(n_recipes_by_depth.values())}",
        "germ_pool_size": len(alpha.germs), "fdr_uses_full_library": len(alpha.germs) == 25,
        "prior": "NULL (number-field obstruction: a0/Z carries sqrt(pi) transcendental, flavor "
                 "data algebraic -> a0/Z gauge-blind). A clean null is the expected outcome.",
    }
    with (RESULTS / f"vocab_search_{stamp}.header.json").open("w") as f:
        json.dump(header, f, indent=2)
    with summary.open("a") as f:
        f.write(f"# overnight_vocab_search {stamp}  FULL-mult={mult:.4e}  "
                f"({header['fdr_mult_formula']})\n")
        f.write(f"# {n_germs} candidate germs x {len(depths)} depths = "
                f"{n_germs*len(depths)} levels; targets={n_targets}\n")

    certified_cumulative = 0
    counter = 0
    sweep = 0
    n_levels = n_germs * len(depths)
    # OUTER SWEEP LOOP: the process stays ALIVE until the deadline (a genuine overnight run that
    # survives), re-verifying the deterministic 81 levels each sweep. Sweeps 2+ are RE-CONFIRMATION
    # passes, NOT new look-elsewhere breadth: they re-run the IDENTICAL (germ, depth, target,
    # expression) trials, so they do NOT inflate `mult` (re-running the same deterministic trial is not
    # a new independent test). This is honest: it keeps the process alive and catches any nondeterminism
    # / drift, without buying certifications by volume. NO state accumulates across sweeps beyond the
    # existing scalars (counter, certified_cumulative, sweep) -> the ~0.29 GB memory bound is preserved.
    while time.time() < deadline:
        sweep += 1
        for cg in germs:
            for d in depths:
                if time.time() > deadline:
                    print(f"[deadline reached at sweep={sweep} germ={cg.key} depth={d}; stopping cleanly]")
                    _finalize(summary, t0, certified_cumulative, sweep)
                    return
                counter += 1
                reach = reach_by_depth[d]
                with candidate_registered(cg):
                    # Under this candidate germ's registry, forced credit is decided inside
                    # gate_candidate_for -> _germ_provenance; the constructive reach is germ-value-
                    # independent (same 25-germ pool), so we reuse it and let the GATE decide credit.
                    best, n_cert, n_relabel = score_config(alpha, reach, targets, mult)
                # Count CERTIFIED only on the FIRST sweep so re-confirmation passes cannot inflate the
                # cumulative certified count (each distinct level is counted once).
                if sweep == 1:
                    certified_cumulative += n_cert
                _mem_watchdog(f"sweep={sweep} config germ={cg.key} d={d}")
                row = {
                    "counter": counter, "sweep": sweep, "level_in_sweep": ((counter - 1) % n_levels) + 1,
                    "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "germ_key": cg.key, "germ_value": cg.value, "germ_law": cg.law,
                    "germ_source": cg.source, "depth": d, "n_targets": n_targets,
                    "n_recipes": len(reach), "fdr_mult": mult,
                    "best": best.as_dict(), "n_certified_this_config": n_cert,
                    "n_relabeled_this_config": n_relabel,
                    "certified_cumulative": certified_cumulative,
                    "elapsed_s": time.time() - t0, "peak_rss_gb": _total_rss_mb() / 1024.0,
                }
                append_level_log(jsonl, summary, row)

    _finalize(summary, t0, certified_cumulative, sweep)


def _finalize(summary: Path, t0: float, certified_cumulative: int, sweep: int = 1):
    verdict = ("CLEAN NULL (expected)" if certified_cumulative == 0
               else f"{certified_cumulative} CERTIFIED CANDIDATE(S) — needs human scrutiny, NOT a TOE")
    line = (f"# DONE  elapsed={time.time()-t0:.0f}s  sweeps={sweep}  "
            f"peakRSS={_total_rss_mb()/1024:.2f}GB  "
            f"CERTIFIED_total={certified_cumulative}  -> {verdict}")
    with summary.open("a") as f:
        f.write(line + "\n")
    print(line)


# ===========================================================================
# 7. CLI
# ===========================================================================

def _print_germs():
    germs = candidate_germs()
    print(f"{len(germs)} CANDIDATE FORCED GERMS (pre-registered, drawn from forced primitives):")
    for cg in germs:
        print(f"  {cg.key:<18} = {cg.value:<10.6g}  <- {cg.law}")


def _dry_run():
    targets = sm_target_keys()
    germs = candidate_germs()
    alpha = build_alphabet(None, None)
    assert len(alpha.germs) == 25
    depths = [5, 4, 3]
    nrec = {}
    for d in depths:
        _, nrec[d] = build_reach_for_depth(alpha, d)
    mult = full_multiplicity(len(targets), len(germs), depths, nrec)
    print(f"n_targets={len(targets)}  n_germs={len(germs)}  depths={depths}")
    print(f"n_recipes_by_depth={nrec}  (sum={sum(nrec.values())})")
    print(f"FULL look-elsewhere multiplicity mult = {mult:.4e}")
    print(f"  = {len(targets)} x {len(germs)} x {sum(nrec.values())}")
    print(f"look-elsewhere penalty on surplus bits = -log2(mult) = {-math.log2(mult):.1f} bits")
    print(f"peak RSS so far: {_total_rss_mb()/1024:.2f} GB  (cap {HARD_MEM_CAP_GB} GB)")


def main():
    ap = argparse.ArgumentParser(description="Overnight FORCED-VOCABULARY search (candidate forced "
                                             "germs x depths x 21 SM targets).")
    ap.add_argument("--hours", type=float, default=10.0, help="overnight run length (default 10h)")
    ap.add_argument("--resume", action="store_true", help="resume (append) into the log dir")
    ap.add_argument("--list-germs", action="store_true", help="print the candidate germ list + laws")
    ap.add_argument("--dry-run", action="store_true", help="one pass: print the FULL FDR multiplicity")
    args = ap.parse_args()

    if args.list_germs:
        _print_germs()
        return
    if args.dry_run:
        _dry_run()
        return
    run_overnight(args.hours, resume=args.resume)


if __name__ == "__main__":
    main()
