"""
The candidate schema the gate consumes.

A `Candidate` is a *claim* that some target number equals some closed-form relation
built from a declared symbol pool, with a declared coefficient provenance and a
declared interlock. The gate never trusts the claim — it re-derives the FDR null
from the declared search space, re-checks each declared forced factor against a
registry of pre-registered physical constraints, and re-checks the interlock against
data. The candidate only tells the gate *what to test*; the gate decides pass/fail.

Design note (same bar both ways): every field that could be used to manufacture a
win is independently re-verified by the gate. The candidate cannot assert "this
factor is forced" or "this is special" — it can only point at a named constraint in
the registry and at a reproducible null, and the gate runs them.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Optional


# ---------------------------------------------------------------------------
# GATE A inputs — the FDR / look-elsewhere search-space declaration
# ---------------------------------------------------------------------------
@dataclass
class SearchSpace:
    """How the brute-force engine could have produced this candidate.

    The FDR gate reconstructs the REACHABLE SET from this spec (not the reported
    formula) and scores the set's density at the target. Two pool styles, mirroring
    the lineage:
      - `germ_pool`: a dict {name: value} of O(1) geometry germs + small integers.
        The gate builds the 1/2/3-symbol product/ratio/sum library (attack5_fdr_partB).
      - `rational_target`: if True, the target is a small-denominator rational; Gate A
        on the *value* is uninformative (a rational is re-described for free), so the
        gate routes to the structural-null instead (see `structural_null`).
    """
    germ_pool: dict = field(default_factory=dict)
    # measurement / claim tolerance (fractional) used for the tight window.
    # CARL'S EMPHASIS (a): this should be the TARGET'S OWN relative precision (sigma/|value|),
    # NOT an arbitrary 1e-4 — so a 6-digit match to a 2-digit-known constant is not credited.
    # run_atomos sets tol = target.rel_precision (clamped) via engine.scoring.measurement_tol.
    tol: float = 1e-4
    # the target's measured 1-sigma (absolute) and how many sig figs it pins. Gate A CAPS the
    # surplus bits at n_digits_known*log2(10): a match tighter than the measurement earns nothing.
    target_sigma: Optional[float] = None
    n_digits_known: Optional[float] = None
    # is the target a small-denominator rational (Koide's 2/3)? then Gate-A-on-value
    # is uninformative and we use the structural null below.
    rational_target: bool = False
    # For STRUCTURAL relations (Koide): a callable that draws N random "no-physics"
    # instances of the relation's inputs and returns the relation's output array.
    # The gate measures P(|output - target| < eps) over these. This is the
    # random-mass-triple null. None => not a structural relation.
    structural_null: Optional[Callable] = None
    structural_eps: float = 1e-5
    structural_N: int = 4_000_000
    # COMPARATIVE structural null (the koide_fdr_sqrt2 measure for MECHANISM claims like
    # "dS-Unruh forces sqrt2"). For an ABSOLUTE structural relation (Koide), P(land on
    # target) over random no-physics inputs IS the chance rate and bits=-log2(P). For a
    # MECHANISM/density claim the meaningful quantity is P(target) RELATIVE to P(a random
    # O(1) target) drawn from the SAME pool: surplus = -log2( P_target / P_random ). This
    # can go NEGATIVE => "not special / -1.08 bits" (sqrt2 is no denser than a random O(1)).
    # If `structural_baseline` is set, the structural route uses the comparative measure;
    # the callable draws M random O(1) targets and returns the mean P(hit) at those targets.
    structural_baseline: Optional[Callable] = None
    structural_baseline_M: int = 2000
    # how many independent targets the broader search swept (look-elsewhere
    # multiplicity); folded into the bit budget.
    n_targets_searched: int = 1


# ---------------------------------------------------------------------------
# GATE B inputs — the forced-kernel declaration
# ---------------------------------------------------------------------------
@dataclass
class Factor:
    """One multiplicative factor of the candidate's coefficient.

    `value`     : the numeric value of the factor.
    `provenance`: a KEY into the forced-constraint registry (gate/registry.py).
                  None or a key absent from the registry => UNFORCED (a free fit param).
    `appears_in`: list of independent named places this same factor is forced
                  (Einstein, Friedmann, dS-Unruh-form, ...). Overdetermination needs >=2
                  distinct entries OR the form forced a third independent way.
    """
    value: float
    provenance: Optional[str] = None
    appears_in: list = field(default_factory=list)


@dataclass
class Coefficient:
    """The candidate's overall coefficient, declared as a product of Factors plus a
    count of genuinely-free O(1) numbers.

    `factors`    : the forced/claimed-forced factors.
    `free_params`: the genuinely unforced O(1) numbers the derivation needs to land the
                   target (a0: exactly 1, namely kappa=1/2). The gate INDEPENDENTLY
                   recomputes this from the factor provenances, so a candidate cannot
                   under-report it.
    `target_value`: the numeric coefficient the factors must reproduce (for the exactness
                    check via the kernel identity).
    `form_forced_independently`: number of independent ways the FORM (not the coefficient)
                   is forced (a0's sqrt(Lambda) form is forced a 3rd way by dS-Unruh).
    """
    factors: list = field(default_factory=list)
    free_params: int = 0
    target_value: Optional[float] = None
    form_forced_independently: int = 0


# ---------------------------------------------------------------------------
# GATE C inputs — the interlock declaration
# ---------------------------------------------------------------------------
@dataclass
class Interlock:
    """The over-determination claim.

    Mode C1 (multi-observable): `n_independent_observables` forced by the SAME
        parameters (a0: Einstein + Friedmann + dS-Unruh form = 3 anchors, 1 free kappa).
    Mode C2 (Koide-class): `n_constants_tied` measured constants tied with
        `n_free_in_interlock` free parameters (Koide: 3 masses, 0 params).

    `cross_sector`: optional callable -> dict of {sector_name: predicted_vs_measured}
        the gate runs the SAME relation on independent sectors and demands consistency
        (the cross-fermion falsification). If the relation is claimed family-universal
        and fails elsewhere, C is FAIL unless `sector_specific_ingredient` names the
        charged-lepton-specific ingredient that legitimately restricts it.
    """
    n_independent_observables: int = 0   # C1
    n_constants_tied: int = 0            # C2
    n_free_in_interlock: int = 99        # C2 (0 = parameter-free, like Koide)
    cross_sector: Optional[Callable] = None
    claimed_universal: bool = False
    sector_specific_ingredient: Optional[str] = None


@dataclass
class Candidate:
    name: str
    target_value: float          # the measured number being explained
    relation_value: float        # what the candidate's closed form evaluates to
    search: SearchSpace
    coefficient: Coefficient
    interlock: Interlock
    note: str = ""
