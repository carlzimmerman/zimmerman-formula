"""
The registry of PRE-REGISTERED forced physical constraints.

GATE B's discipline (GATE_SPEC B.1, "Provenance, not factorization"): mechanically
factoring a coefficient is trivial; a factor only counts as FORCED if it is traceable
to a NAMED physical constraint declared BEFORE the target is seen. This module is that
named list. A factor whose `provenance` key is NOT here is a free fit parameter, full
stop — that is how the gate refuses to be gamed by a candidate that just asserts
"this factor is forced".

Each entry: key -> (forced_value, human description, the law it is forced by).
The forced_value lets the gate VERIFY the candidate's declared numeric factor actually
equals the forced constant (a candidate cannot relabel 5.79 as "sqrt(8pi)").

To add a NEW forced constraint (e.g. an A4 representation dimension for a PMNS lead),
you register it HERE, before fitting, with its law — exactly the pre-fit declaration
the gate requires.
"""
import math

# tolerance for "the declared factor numerically equals the forced constant"
_FACTOR_MATCH_TOL = 1e-9

# key -> dict(value, desc, law)
FORCED_CONSTRAINTS = {
    # --- the a0 kernel: the two factors of sqrt(8pi/3), each forced by GR ---
    "einstein_8pi": dict(
        value=math.sqrt(8 * math.pi),
        desc="sqrt(8pi) from Einstein field-equation normalization rho_Lambda = Lambda c^2 / 8piG",
        law="Einstein field equations (the 8pi is forced by G_munu = 8piG T_munu)",
    ),
    "friedmann_third": dict(
        value=math.sqrt(1.0 / 3.0),
        desc="sqrt(1/3) from the Friedmann coefficient H^2 = 8piG rho / 3",
        law="Friedmann equation / FRW metric (the 3 is forced by the homogeneous metric)",
    ),
    # the full kernel, as a single forced object (for candidates that declare it whole)
    "a0_kernel_8pi3": dict(
        value=math.sqrt(8 * math.pi / 3.0),
        desc="sqrt(8pi/3) = sqrt(8pi)*sqrt(1/3); the a0 forced kernel",
        law="Einstein x Friedmann (overdetermined: appears in BOTH)",
    ),
    # --- group-theory / symmetry forced constants (the SM hooks, pre-registered) ---
    # These are the FORCED-coefficient pool the SM port must match against. They are
    # representation dimensions / invariants of candidate flavor groups. A SM candidate
    # passes Gate B ONLY if its coefficient is one of these (forced by a declared
    # symmetry), not a free integer.
    "Ngen_3": dict(
        value=3.0,
        desc="3 = number of fermion generations (rank of the family space)",
        law="SM family structure (3 generations, an observed-then-fixed integer)",
    ),
    "A4_dim_3": dict(
        value=3.0,
        desc="dim of the A4 triplet representation",
        law="A4 discrete flavor symmetry (the 3 is the irrep dimension)",
    ),
    "S3_doublet_amp_sqrt2": dict(
        # the S3/Z3 democratic-circulant amplitude; sqrt2 is the Koide amplitude.
        # IMPORTANT: this is registered as a constraint NAME but its forcing is the open
        # question. The gate still requires OVERDETERMINATION (>=2 independent
        # appearances) before it counts; a lone S3 amplitude appearance is a definition,
        # not a kernel. See Koide: r=sqrt2 is real as an EMPIRICAL interlock (Gate C2),
        # but it does NOT clear Gate B because it appears in only ONE forced place and
        # needs a second free number to set the per-fermion k_f. So registering it here
        # does NOT let Koide cheat Gate B.
        value=math.sqrt(2.0),
        desc="sqrt2 = Koide circulant amplitude (r) for the charged leptons",
        law="S3/Z3 democratic-circulant ansatz (amplitude NOT forced from first principles)",
    ),
}


def is_forced(provenance_key):
    """True iff this provenance key names a pre-registered forced constraint."""
    return provenance_key in FORCED_CONSTRAINTS


def forced_value(provenance_key):
    """The numeric value the constraint forces, or None if unregistered."""
    e = FORCED_CONSTRAINTS.get(provenance_key)
    return None if e is None else e["value"]


def factor_matches_forced(declared_value, provenance_key, rel_tol=_FACTOR_MATCH_TOL):
    """Verify a candidate's declared numeric factor actually equals the forced
    constant it claims provenance for. Refuses relabeling (5.79 != sqrt(8pi))."""
    fv = forced_value(provenance_key)
    if fv is None:
        return False
    if fv == 0:
        return abs(declared_value) < rel_tol
    return abs(declared_value - fv) / abs(fv) < rel_tol
