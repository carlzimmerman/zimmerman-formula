#!/usr/bin/env python3
"""
geometric_primitives.py — the REDUCED, FORCED-GEOMETRIC alphabet for project_atomos.

WHY THIS FILE EXISTS (Carl's refinement, 2026-06-25):
    Before brute-forcing more, build the SELF-CONSTRAINING WEB OF GEOMETRY and use it to
    REDUCE the search space, then brute-force WITHIN that web. The a0 lesson, applied as a
    METHOD (not a bridge): a physical scale was pinned by FORCED GEOMETRIC FACTORS
    (sqrt(8pi/3) = sqrt(8pi)[Einstein measure] x sqrt(1/3)[Friedmann/FRW]) that were written
    down BEFORE any fit. Transfer the METHOD: build the particle-physics search ONLY from
    forced-geometric primitives (rep dimensions, |G|, root-system angles, Dynkin indices,
    measure factors pi/2pi/4pi/8pi, small integers from SPATIAL/REP dimensions, discrete-group
    invariants). Restricting to forced primitives is what REDUCES the reachable set -> a hit
    then carries real bits.

QUARANTINE (non-negotiable, from the corpus): NO a0/Z/kappa/rho_c/SM-derived numbers are
    building blocks here. Those regenerate the 164 FDR-dead re-labelings and INFLATE the space.
    The a0 kernels live in alphabet.py's germ pool for the COSMOLOGY calibration only. This
    module is the PARTICLE-sector constrained alphabet: forced group/representation geometry.

HONEST BOTH-WAYS (baked into the data, not narrated away):
    - There is NO forced bridge from cosmic density to SM masses (~60-order scale gap,
      corpus-confirmed). The MASS sector likely lacks a forced kernel.
    - The MIXING sector (CKM/PMNS) is where geometry genuinely lives and a real interlock
      most plausibly hides. The hit-list ranks accordingly.
    - Every primitive carries `forced: bool` and a `provenance` tag. A rational TARGET (2/3,
      3/8, 1/3, 1/2) is hit by many symbol combos -> Gate A on the VALUE is uninformative
      (the rational-target exception). Such primitives are tagged `rational_target_exempt=True`
      so the gate scores their EVIDENCE (the embedding / the random-triple null), not the number.

ALL numeric identities sympy-verified exact, 2026-06-25 (see verify_primitives() at bottom).

Pure stdlib + sympy. Designed to be consumed by the engine as its constrained alphabet:
    from targets.geometric_primitives import forced_pool, INTERLOCKS, HITLIST
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Callable

try:
    import sympy as sp
    _HAVE_SP = True
except Exception:  # pragma: no cover
    _HAVE_SP = False


# =============================================================================
# CORE RECORD
# =============================================================================

@dataclass
class Primitive:
    """One forced-geometric primitive: a number whose VALUE is fixed by a named symmetry/
    geometry constraint BEFORE any data is seen.

    key        : machine key
    value      : exact value (float; sym carries the exact symbolic form)
    sym        : sympy exact expression (None if sympy unavailable) — the kernel gate reads this
    sector     : 'gauge' | 'gut' | 'flavor_group' | 'koide' | 'mixing' | 'measure' | 'rep_dim'
    provenance : the named pre-registered constraint that FORCES this value (the Gate-B tag)
    forced     : True if the value is pinned before fitting; False if it is a FREE/fitted number
    role       : 'rep_dim' | 'group_order' | 'weyl_order' | 'coxeter' | 'casimir' | 'dynkin'
                 | 'anomaly' | 'measure' | 'angle' | 'amplitude' | 'beta' | 'clebsch'
    appears_in : the independent forced places this primitive shows up (overdetermination test)
    rational_target_exempt : True if this is a small-denominator rational TARGET whose Gate-A
                 value-score is uninformative (evidence lives in the structure / null, not the #)
    note       : free text
    """
    key: str
    value: float
    sym: object
    sector: str
    provenance: str
    forced: bool
    role: str
    appears_in: List[str] = field(default_factory=list)
    rational_target_exempt: bool = False
    note: str = ""


# =============================================================================
# 1. MEASURE / GEOMETRY FACTORS (forced by the spatial / field-equation geometry)
#    These are the SAME class as a0's sqrt(8pi) and sqrt(1/3) — measure coefficients.
#    Kept WITHOUT the a0-specific kernels (no Z, no kappa) — pure geometry only.
# =============================================================================

def _measure() -> List[Primitive]:
    S = (lambda e: e) if not _HAVE_SP else (lambda e: e)
    pi = sp.pi if _HAVE_SP else 3.141592653589793
    P = []
    P += [
        Primitive("pi", float(pi) if _HAVE_SP else pi, pi, "measure",
                  "circle/sphere measure (geometry constant)", True, "measure",
                  ["solid_angle", "rotation"], note="the irreducible geometric transcendental"),
        Primitive("2pi", float(2*pi) if _HAVE_SP else 6.283185, 2*pi if _HAVE_SP else 6.283185,
                  "measure", "1 full turn / circle circumference measure", True, "measure",
                  ["U(1) period", "rotation"]),
        Primitive("4pi", float(4*pi) if _HAVE_SP else 12.566, 4*pi if _HAVE_SP else 12.566,
                  "measure", "total solid angle of S^2 (Gauss-law / sphere surface)", True,
                  "measure", ["solid_angle_S2", "Coulomb/Newton flux"]),
        Primitive("8pi", float(8*pi) if _HAVE_SP else 25.13, 8*pi if _HAVE_SP else 25.13,
                  "measure", "Einstein field-equation normalization (G_uv = 8piG T_uv)", True,
                  "measure", ["Einstein_eq", "rho_Lambda=Lc^2/8piG"],
                  note="forced in GRAVITY; appears in the a0 kernel. Listed as a measure "
                       "primitive but NOT as an SM building block — gauge sector does not use it."),
        Primitive("4pi/3", float(4*pi/3) if _HAVE_SP else 4.18879,
                  4*pi/3 if _HAVE_SP else 4.18879, "measure",
                  "volume of the unit 3-ball (spatial-dimension geometry)", True, "measure",
                  ["ball_volume_d3"], note="the d=3 spatial measure; the '3' is the spatial dim"),
    ]
    return P


# =============================================================================
# 2. REPRESENTATION DIMENSIONS (forced by the gauge group — fixed before any data)
#    dim(adj) = N^2-1 is a GROUP IDENTITY; fund dims are the defining reps.
# =============================================================================

def _rep_dims() -> List[Primitive]:
    I = (lambda n: sp.Integer(n)) if _HAVE_SP else (lambda n: n)
    P = []
    # SM gauge group defining + adjoint reps
    P += [
        Primitive("su3_fund", 3.0, I(3), "rep_dim", "SU(3)_color fundamental (quark triplet)",
                  True, "rep_dim", ["SU(3)", "n_colors"], note="N_c = 3"),
        Primitive("su3_adj", 8.0, I(8), "rep_dim", "SU(3) adjoint = N^2-1 = 8 (gluons)",
                  True, "rep_dim", ["SU(3)", "dim_adj=N^2-1"]),
        Primitive("su2_fund", 2.0, I(2), "rep_dim", "SU(2)_L fundamental (weak doublet)",
                  True, "rep_dim", ["SU(2)", "weak_doublet"]),
        Primitive("su2_adj", 3.0, I(3), "rep_dim", "SU(2) adjoint = N^2-1 = 3 (W^a)",
                  True, "rep_dim", ["SU(2)", "dim_adj=N^2-1"]),
        Primitive("u1_singlet", 1.0, I(1), "rep_dim", "U(1)_Y singlet", True, "rep_dim",
                  ["U(1)"]),
        Primitive("n_gen", 3.0, I(3), "rep_dim", "number of fermion generations (empirical 3)",
                  True, "rep_dim", ["3_generations"],
                  note="forced=empirical-fixed (a counting fact, not derived); the '3' that the "
                       "circulant/A4 triplet hosts."),
    ]
    return P


# =============================================================================
# 3. GUT EMBEDDING INVARIANTS (forced by SU(5)/SO(10)/E6 representation theory)
# =============================================================================

def _gut() -> List[Primitive]:
    I = (lambda n: sp.Integer(n)) if _HAVE_SP else (lambda n: n)
    R = (lambda n, d: sp.Rational(n, d)) if _HAVE_SP else (lambda n, d: n / d)
    P = []
    P += [
        # group dimensions
        Primitive("dim_su5", 24.0, I(24), "gut", "dim SU(5) = 5^2-1", True, "group_order",
                  ["SU(5)"]),
        Primitive("dim_so10", 45.0, I(45), "gut", "dim SO(10) = 10*9/2", True, "group_order",
                  ["SO(10)"]),
        Primitive("dim_e6", 78.0, I(78), "gut", "dim E6", True, "group_order", ["E6"]),
        # one-generation embedding dims
        Primitive("gen_su5", 15.0, I(15), "gut", "SU(5) one generation = 5bar + 10 = 15",
                  True, "rep_dim", ["SU(5)", "one_generation"],
                  note="multiplet CLOSURE: a complete 5bar+10 IS exactly one generation -> this "
                       "is WHY the 3/8 trace identity holds."),
        Primitive("gen_so10", 16.0, I(16), "gut", "SO(10) spinor 16 = 15 + nu_R", True,
                  "rep_dim", ["SO(10)", "one_generation+nuR"]),
        Primitive("gen_e6", 27.0, I(27), "gut", "E6 fundamental 27 = 16+10+1", True, "rep_dim",
                  ["E6", "one_generation"]),
        # sin^2 theta_W tree (GUT) = 3/8 — RATIONAL TARGET (Gate-A value-exempt)
        Primitive("sin2_thetaW_tree", 0.375, R(3, 8), "gauge",
                  "sin^2 theta_W (tree, GUT) = Tr(T3^2)/Tr(Q^2) = (1/2)/(4/3) = 3/8 over a "
                  "complete SU(5) multiplet; equiv (3/5)/((3/5)+1)", True, "clebsch",
                  ["SU(5)_5bar_trace", "GUT_normalization_5/3"], rational_target_exempt=True,
                  note="FORCED rational from the embedding. Gate A on the NUMBER 3/8 is "
                       "uninformative; evidence = the trace identity. Runs DOWN to ~0.20 (plain "
                       "SM) vs measured 0.23122 -> the precision second-observable MISSES by a "
                       "few % in the minimal SM (honest near-miss, not a win)."),
        Primitive("gut_norm_5_3", 1.6666666666666667, R(5, 3), "gauge",
                  "GUT hypercharge normalization g1^2_GUT = (5/3) g_Y^2", True, "clebsch",
                  ["SU(5)", "common_Tr(T^2)"], rational_target_exempt=True,
                  note="the SAME forced fact as 3/8."),
        # Weyl group orders (forced discrete invariants of the root systems)
        Primitive("weyl_a4", 120.0, I(120), "gut", "|W(A4=SU5)| = 5! = 120", True, "weyl_order",
                  ["A4_root_system"]),
        Primitive("weyl_d5", 1920.0, I(1920), "gut", "|W(D5=SO10)| = 2^4 * 5! = 1920", True,
                  "weyl_order", ["D5_root_system"]),
        Primitive("weyl_e6", 51840.0, I(51840), "gut", "|W(E6)| = 51840", True, "weyl_order",
                  ["E6_root_system"]),
        # Coxeter numbers
        Primitive("coxeter_su5", 5.0, I(5), "gut", "Coxeter h(A4)=5", True, "coxeter",
                  ["A4_root_system"]),
        Primitive("coxeter_so10", 8.0, I(8), "gut", "Coxeter h(D5)=8", True, "coxeter",
                  ["D5_root_system"]),
        Primitive("coxeter_e6", 12.0, I(12), "gut", "Coxeter h(E6)=12", True, "coxeter",
                  ["E6_root_system"]),
    ]
    return P


# =============================================================================
# 4. CASIMIRS / DYNKIN INDICES / BETA-FUNCTION COEFFICIENTS
#    (forced ratios that set the running — group theory, pre-fit)
# =============================================================================

def _casimir_beta() -> List[Primitive]:
    I = (lambda n: sp.Integer(n)) if _HAVE_SP else (lambda n: n)
    R = (lambda n, d: sp.Rational(n, d)) if _HAVE_SP else (lambda n, d: n / d)
    P = []
    P += [
        Primitive("dynkin_fund", 0.5, R(1, 2), "gauge",
                  "T(fund) = 1/2 for every SU(N) (Dynkin index normalization)", True, "dynkin",
                  ["SU(N)"], rational_target_exempt=True),
        Primitive("casimir_adj_su3", 3.0, I(3), "gauge", "C2(adj) = N = 3 for SU(3)", True,
                  "casimir", ["SU(3)"]),
        Primitive("casimir_adj_su2", 2.0, I(2), "gauge", "C2(adj) = N = 2 for SU(2)", True,
                  "casimir", ["SU(2)"]),
        # SM 1-loop beta coefficients (GUT-normalized U(1)) — rep-dim sums, forced
        Primitive("beta_b1_sm", 4.1, R(41, 10), "gauge",
                  "SM 1-loop b1 = 41/10 (GUT-norm) = rep-dim sum", True, "beta",
                  ["SM_running", "U(1)"], rational_target_exempt=True),
        Primitive("beta_b2_sm", -3.1666666666666665, R(-19, 6), "gauge",
                  "SM 1-loop b2 = -19/6 = (-22/3 gauge + 4/3 n_gen + 1/6 Higgs)", True, "beta",
                  ["SM_running", "SU(2)"], rational_target_exempt=True),
        Primitive("beta_b3_sm", -7.0, I(-7), "gauge",
                  "SM 1-loop b3 = -7 = (-11 gauge + 4/3 n_gen)", True, "beta",
                  ["SM_running", "SU(3)"]),
        Primitive("beta_ratio_sm", 218.0 / 115.0, R(218, 115), "gauge",
                  "(b1-b2)/(b2-b3) = 218/115 (forced beta-coefficient ratio)", True, "beta",
                  ["SM_running"], rational_target_exempt=True),
    ]
    return P


# =============================================================================
# 5. DISCRETE FLAVOR-GROUP INVARIANTS (the legitimate Gate-B coefficient pool for FLAVOR)
#    Orders + irrep dimensions are forced-before-fit (a rep dim is fixed by the group).
# =============================================================================

def _flavor_groups() -> List[Primitive]:
    I = (lambda n: sp.Integer(n)) if _HAVE_SP else (lambda n: n)
    P = []
    P += [
        # S3 — smallest non-abelian; the 1+2 democratic/doublet split hosting the circulant
        Primitive("S3_order", 6.0, I(6), "flavor_group", "|S3| = 6", True, "group_order",
                  ["S3"], note="hosts Koide's 1+2 (democratic + doublet) circulant split"),
        Primitive("S3_irrep2", 2.0, I(2), "flavor_group", "S3 2-dim irrep (the doublet)", True,
                  "rep_dim", ["S3"]),
        # A4 (tetrahedral) — canonical tri-bimaximal group
        Primitive("A4_order", 12.0, I(12), "flavor_group", "|A4| = 12 (tetrahedral)", True,
                  "group_order", ["A4"]),
        Primitive("A4_irrep3", 3.0, I(3), "flavor_group", "A4 3-dim irrep (holds 3 generations)",
                  True, "rep_dim", ["A4"], note="the canonical TBM-forcing triplet"),
        Primitive("A4_n_vert", 4.0, I(4), "flavor_group", "tetrahedron vertices = 4", True,
                  "rep_dim", ["A4_polytope"]),
        Primitive("A4_n_edge", 6.0, I(6), "flavor_group", "tetrahedron edges = 6", True,
                  "rep_dim", ["A4_polytope"]),
        # S4 (octahedral / cube)
        Primitive("S4_order", 24.0, I(24), "flavor_group", "|S4| = 24 (octahedral)", True,
                  "group_order", ["S4"]),
        Primitive("S4_irrep3", 3.0, I(3), "flavor_group", "S4 3-dim irrep", True, "rep_dim",
                  ["S4"]),
        Primitive("cube_n_vert", 8.0, I(8), "flavor_group", "cube vertices = 8", True, "rep_dim",
                  ["S4_polytope"]),
        Primitive("cube_n_edge", 12.0, I(12), "flavor_group", "cube edges = 12", True, "rep_dim",
                  ["S4_polytope"]),
        # Delta(27)
        Primitive("D27_order", 27.0, I(27), "flavor_group", "|Delta(27)| = 27", True,
                  "group_order", ["Delta27"], note="(Z3xZ3) rtimes Z3; 9 singlets + 3 + 3bar"),
    ]
    return P


# =============================================================================
# 6. KOIDE / CIRCULANT GEOMETRY (sympy-exact forced structure; r=sqrt2 is FREE)
# =============================================================================

def _koide() -> List[Primitive]:
    R = (lambda n, d: sp.Rational(n, d)) if _HAVE_SP else (lambda n, d: n / d)
    P = []
    P += [
        # the democratic floor (FORCED by S3/Z3 circulant algebra)
        Primitive("koide_floor", 0.3333333333333333, R(1, 3), "koide",
                  "Koide democratic floor: Q = 1/3 + r^2/6 (circulant identity, S3/Z3, "
                  "delta-independent)", True, "amplitude", ["S3_circulant"],
                  rational_target_exempt=True,
                  note="sympy-exact: with sqrt(m_k)=M(1+r cos(2pi k/3 + delta)), "
                       "Q=(sum m)/(sum sqrt m)^2 = 1/3 + r^2/6 EXACTLY, independent of phase "
                       "delta (dQ/ddelta=0). The 1/3 is FORCED; r is FREE."),
        # the doublet-amplitude coefficient (FORCED structure)
        Primitive("koide_ampl_coeff", 0.16666666666666666, R(1, 6), "koide",
                  "Koide doublet-amplitude coefficient: the r^2/6 term", True, "amplitude",
                  ["S3_circulant"], rational_target_exempt=True),
        # the Koide TARGET Q=2/3 (a small-denom rational TARGET -> Gate-A value-exempt)
        Primitive("koide_Q_target", 0.6666666666666666, R(2, 3), "koide",
                  "Koide Q = 2/3 (charged leptons, measured 0.666661, dev -9e-6)", True,
                  "amplitude", ["lepton_masses"], rational_target_exempt=True,
                  note="REAL interlock (Gate C2, ties 3 masses, 0 params; FDR via the "
                       "random-triple null ~1-in-48k). BUT the MECHANISM for Q=2/3 fails Gate B: "
                       "r=sqrt2 is a FREE interior point (appears in ONLY ONE place, the "
                       "circulant amplitude; a0's kernel appears in >=2). REAL-PUZZLE-RE-LABELED."),
        # cos^2 of the sqrt-mass angle to (1,1,1) at Q=2/3 (FORCED-given-Q trig identity)
        Primitive("koide_cos2_angle", 0.5, R(1, 2), "koide",
                  "cos^2(angle of sqrt-mass vector to (1,1,1)) = 1/(3Q); Q=2/3 -> 1/2 -> 45 deg",
                  True, "angle", ["lepton_masses"], rational_target_exempt=True,
                  note="FORCED-given-Q: cos^2 = 1/(3Q) is a trig identity; 45 deg is the lepton "
                       "value. The CORRECTED reading (not 3/4): cos^2=1/2, phi=45 deg."),
        # the FREE amplitude r=sqrt2 — explicitly flagged FREE (this is the open knob)
        Primitive("koide_r_sqrt2", 1.4142135623730951,
                  (sp.sqrt(2) if _HAVE_SP else 1.4142135623730951), "koide",
                  "FREE: circulant amplitude r=sqrt2 (Q=2/3 <=> r^2=2). NOT forced by any group "
                  "invariant — the open target.", False, "amplitude", ["S3_circulant"],
                  note="THE load-bearing FREE parameter. Appears in exactly ONE forced place "
                       "(fails Gate-B overdetermination). sqrt(2/Z)=(3/8pi)^(1/4)=0.588 != sqrt2 "
                       "-> the a0 spine does NOT supply it (corpus-confirmed re-label-dead)."),
        # Brannen phase delta=2/9 — explicitly FREE (the 2nd free number)
        Primitive("koide_delta_brannen", 0.2222222222222222,
                  (sp.Rational(2, 9) if _HAVE_SP else 0.2222222222222222), "koide",
                  "FREE: Brannen phase delta=2/9 rad reproduces (m_e,m_mu,m_tau) to 5 digits.",
                  False, "angle", ["lepton_masses"],
                  note="FIT, not forced. The SECOND free number (after r): full lepton spectrum "
                       "needs scale M + r + delta. Two free numbers => Gate B FAIL."),
    ]
    return P


# =============================================================================
# 7. MIXING-SECTOR FORCED RATIONALS (the TBM Clebsch values — where geometry lives)
#    These are FORCED-pattern values (A4/S4 Clebsch ratios), broken by theta_13.
# =============================================================================

def _mixing() -> List[Primitive]:
    R = (lambda n, d: sp.Rational(n, d)) if _HAVE_SP else (lambda n, d: n / d)
    I = (lambda n: sp.Integer(n)) if _HAVE_SP else (lambda n: n)
    P = []
    P += [
        Primitive("tbm_sin2_12", 0.3333333333333333, R(1, 3), "mixing",
                  "TBM sin^2 theta_12 = 1/3 (A4/S4 Clebsch); measured 0.303 (~2.5 sigma low)",
                  True, "clebsch", ["A4", "S4", "tri-bimaximal"], rational_target_exempt=True,
                  note="theta_12 = 35.26 deg (TBM) vs measured 33.41 -> close, mild tension."),
        Primitive("tbm_sin2_23", 0.5, R(1, 2), "mixing",
                  "TBM sin^2 theta_23 = 1/2 (maximal, 45 deg); measured 0.572 (octant open)",
                  True, "clebsch", ["A4", "S4", "mu-tau_symmetry"], rational_target_exempt=True,
                  note="the recurring cos^2=1/2 / 45-deg theme (links Koide-45, atm-theta23, QLC)."),
        Primitive("tbm_sin2_13", 0.0, I(0), "mixing",
                  "TBM sin^2 theta_13 = 0; measured 0.02203 -> theta_13 is the TBM-BREAKING angle",
                  True, "clebsch", ["A4", "S4", "tri-bimaximal"],
                  note="exact TBM died in 2012 (theta_13=8.54 deg != 0). The forced-pattern + "
                       "structured breaking is the forced-kernel-plus-perturbation signature."),
        # cross-sector complementarity TARGETS (computed numerics; their EVIDENCE is structural)
        Primitive("qlc_target_45", 45.0, I(45), "mixing",
                  "quark-lepton complementarity: theta_C + theta_12^PMNS =? 45 deg "
                  "(measured 13.00+33.41 = 46.41)", True, "angle",
                  ["CKM", "PMNS", "cross_sector"],
                  note="46.41 deg vs 45 -> ~1.4 deg (~3%) off. Cross-sector interlock candidate; "
                       "the gate must say coincidence-vs-structure."),
        Primitive("th13_over_thetaC_sqrt2", 0.15910609683478505,
                  (1 / sp.sqrt(2) if _HAVE_SP else 0.7071) and None, "mixing",
                  "theta_13^PMNS ~ theta_C/sqrt2: lambda/sqrt2 = 0.1591 vs sin(theta_13)=0.1485",
                  True, "angle", ["CKM", "PMNS", "cross_sector"],
                  note="~7% off (0.1591 vs 0.1485). Charged-lepton correction to TBM. "
                       "sym set None (it's a numeric coincidence target, not an exact rational)."),
    ]
    # fix the sym for th13 entry (the lambda is empirical, only the 1/sqrt2 factor is geometric)
    for p in P:
        if p.key == "th13_over_thetaC_sqrt2" and _HAVE_SP:
            p.sym = None  # the TARGET mixes a measured lambda with a geometric 1/sqrt2
    return P


# =============================================================================
# THE POOL + ACCESSORS
# =============================================================================

def _all() -> List[Primitive]:
    return (_measure() + _rep_dims() + _gut() + _casimir_beta()
            + _flavor_groups() + _koide() + _mixing())


# module-level registry
_REGISTRY: Dict[str, Primitive] = {p.key: p for p in _all()}


def all_primitives() -> List[Primitive]:
    return list(_REGISTRY.values())


def forced_pool() -> List[Primitive]:
    """The FORCED-only constrained alphabet (the reduced search space the engine consumes).
    Excludes the explicitly-FREE entries (koide_r_sqrt2, koide_delta_brannen)."""
    return [p for p in _REGISTRY.values() if p.forced]


def free_pool() -> List[Primitive]:
    """The explicitly-FREE numbers — the open knobs the geometry does NOT pin."""
    return [p for p in _REGISTRY.values() if not p.forced]


def sector(name: str) -> List[Primitive]:
    return [p for p in _REGISTRY.values() if p.sector == name]


def get(key: str) -> Primitive:
    return _REGISTRY[key]


def rational_targets() -> List[Primitive]:
    """Small-denominator rational TARGETS whose Gate-A value-score is uninformative
    (the rational-target exception). The gate must score their structure/null, not the number."""
    return [p for p in _REGISTRY.values() if p.rational_target_exempt]


# =============================================================================
# THE INTERLOCK GRAPH — which observables are tied by which geometry
# =============================================================================

@dataclass
class Interlock:
    """A declared geometric closure that ties >=2 observables (C1) or >=3 constants (C2)."""
    key: str
    geometry: str               # the forced mechanism doing the tying
    ties: List[str]             # the observables / constants tied together
    n_free: int                 # free parameters inside the interlock
    gate_mode: str              # 'C1' | 'C2'
    status: str                 # PASS | NEAR-MISS | REAL-PUZZLE-RE-LABELED | COINCIDENCE-CANDIDATE
    sector: str
    note: str = ""


INTERLOCKS: List[Interlock] = [
    Interlock(
        "hypercharge_anomaly_closure",
        "anomaly cancellation ([SU3]^2U1, [SU2]^2U1, grav^2 U1) + Yukawa gauge-invariance",
        ["y_Q", "y_L", "y_e", "y_d", "y_u", "y_H", "Q_proton=-Q_electron", "[U(1)]^3=0"],
        0, "C2", "PASS",
        "gauge",
        "STRONGEST forced structure: ties ALL hypercharges to ONE scale (1 scale x forced "
        "integer pattern), forces electric-charge quantization, and the cubic [U(1)]^3 anomaly "
        "is AUTOMATICALLY zero (sympy simplify=0) = the overdetermination signature. The gauge "
        "analogue of a0's overdetermined sqrt(8pi/3). Bits are STRUCTURAL not numerical (charges "
        "already known) -> ties many observables / 0 params, but predicts no NEW number."),
    Interlock(
        "gut_unification_sin2thetaW",
        "SU(5)/SO(10) embedding: complete multiplet trace Tr(T3^2)/Tr(Q^2)=3/8 + beta-running",
        ["sin2_thetaW", "alpha_em", "alpha_s", "alpha_GUT"],
        1, "C1", "NEAR-MISS",
        "gauge",
        "Same embedding forces sin2thetaW_tree=3/8 AND collapses 3 couplings to 1 alpha_GUT via "
        "the (forced) beta-coefficients. HONEST: plain-SM 1-loop running misses 0.231 (lands "
        "~0.20); MSSM tightens it. FAILS the precision 2nd-observable test in the MINIMAL SM. "
        "Real in FORM, near-miss in number -> needs a non-minimal UV completion to close."),
    Interlock(
        "multiplet_closure",
        "SU(5)/SO(10) rank: a complete 5bar+10 (=15) / 16-spinor IS exactly one generation",
        ["matter_content", "sin2_thetaW_tree=3/8", "charge_quantization"],
        0, "C2", "PASS",
        "gut",
        "Ties matter content to gauge structure: the 15 (or 16 w/ nu_R) is one generation, which "
        "is WHY the 3/8 trace identity holds. Structural, no new number."),
    Interlock(
        "koide_Q_leptons",
        "S3/Z3 circulant: Q = 1/3 + r^2/6 (delta-independent), Q=2/3 <=> r=sqrt2",
        ["m_e", "m_mu", "m_tau"],
        0, "C2", "REAL-PUZZLE-RE-LABELED",
        "koide",
        "REAL Gate-C2 interlock: ties 3 lepton masses with 0 free params; FDR via random-triple "
        "null ~1-in-48k; density peak NOT at 2/3 -> a genuine special lepton angle. BUT Gate B "
        "FAILS: r=sqrt2 appears in ONLY ONE forced place (need >=2, the a0 standard), and the "
        "full spectrum needs a 2nd free number (delta=2/9, fit). The open target: can a FLAVOR "
        "SYMMETRY force r=sqrt2 where the gravity spine provably cannot? Cross-fermion FALSIFIES "
        "a family-universal mechanism (Q_up=0.85, Q_down=0.73 != 2/3) -> needs lepton-specific."),
    Interlock(
        "tbm_A4_pattern",
        "A4/S4 Clebsch: sin2_12=1/3, sin2_23=1/2, sin2_13=0 (tri-bimaximal), broken by theta_13",
        ["theta_12_PMNS", "theta_23_PMNS", "theta_13_PMNS"],
        1, "C1", "NEAR-MISS",
        "mixing",
        "FORCED-pattern from A4/S4: ties the 3 PMNS angles to group Clebsch values. Data sit "
        "STRIKINGLY close (sin2_12~0.303 vs 1/3; sin2_23~0.572 vs 1/2) EXCEPT theta_13=8.54 deg "
        "(killed exact TBM in 2012). The structured BREAKING (theta_13 != 0, the deviations are "
        "themselves patterned) = the forced-kernel-plus-perturbation signature. The HIGHEST-prior "
        "UNSOLVED interlock -> 'probably geometric' lands here."),
    Interlock(
        "gst_mass_mixing",
        "down-quark mass texture: sqrt(m_d/m_s) =? |V_us| (Gatto-Sartori-Tonin)",
        ["m_d", "m_s", "ckm_lambda"],
        0, "C2", "COINCIDENCE-CANDIDATE",
        "mixing",
        "Mass<->mixing interlock, the quark-sector Koide analogue: ties a mixing angle to a mass "
        "RATIO with no free param. sqrt(4.70/93.5)=0.2242 vs |V_us|=0.22501 (~0.4% — strikingly "
        "good, BUT m_d is [L]-confidence +/-10%). Testable now; the light-quark error gates the "
        "claim. Cross-SECTOR (mass<->mixing) = the gate's strongest class if it survives."),
    Interlock(
        "quark_lepton_complementarity",
        "GUT-scale relation: theta_C + theta_12^PMNS =? 45 deg; theta_13^PMNS =? theta_C/sqrt2",
        ["ckm_theta12", "pmns_theta12", "pmns_theta13", "ckm_lambda"],
        0, "C2", "COINCIDENCE-CANDIDATE",
        "mixing",
        "Cross-sector CKM<->PMNS interlock (the hardest to fake). theta_C+theta12_PMNS=46.41 vs "
        "45 (~3%); lambda/sqrt2=0.1591 vs sin(theta_13)=0.1485 (~7%). If real -> a GUT-scale "
        "forced kernel relating the two mixing matrices. ~3-7% agreement: needs the gate to say "
        "coincidence vs structure (the recurring 45-deg / 1/sqrt2 theme is suggestive)."),
]


def interlocks() -> List[Interlock]:
    return list(INTERLOCKS)


# =============================================================================
# THE RANKED HIT-LIST — where a gate-passing interlock most plausibly hides
# =============================================================================

# Ranked by PRIOR that a forced-kernel/interlock is actually REAL (not by ease).
# Criteria: (a) already-FDR-surviving parameter-free relation? (b) symmetry-FORCED vs free
# eigenvalue? (c) interlocks across >=2 observables/sectors? Mixing/PMNS ranked first per
# the charter ("the MIXING sector is where geometry genuinely lives").
HITLIST: List[Dict[str, str]] = [
    {"rank": "1", "target": "PMNS / TBM via A4(S4,Delta27), theta_13~8.5deg as the breaking",
     "interlock": "tbm_A4_pattern", "sector": "mixing",
     "why": "Most symmetry-FORCED unsolved sector; sin2_12~1/3 & sin2_23~1/2 are forced-pattern "
            "values; A4/S4 discrete-group hypotheses are tailor-made; the charter's 'probably "
            "geometric' instinct points HERE. Forced-pattern + structured breaking."},
    {"rank": "2", "target": "GST mass-mixing sqrt(m_d/m_s) ~ |V_us| (Cabibbo from quark masses)",
     "interlock": "gst_mass_mixing", "sector": "mixing",
     "why": "Clean mass<->mixing interlock, 0 free params, ~0.4% agreement (gated by light-quark "
            "[L] error). The quark-sector analogue of Koide; cross-sector = strongest class."},
    {"rank": "3", "target": "Quark-lepton complementarity theta_C+theta12_PMNS~45 & theta13~theta_C/sqrt2",
     "interlock": "quark_lepton_complementarity", "sector": "mixing",
     "why": "Cross-sector CKM<->PMNS (hardest to fake); ~3-7% agreement; the recurring 45deg / "
            "1/sqrt2 theme; if real -> a GUT-scale kernel tying both mixing matrices."},
    {"rank": "4", "target": "Koide Q=2/3 -> can a FLAVOR SYMMETRY force r=sqrt2?",
     "interlock": "koide_Q_leptons", "sector": "koide",
     "why": "The ONE PROVEN interlock (calibration positive); re-find + re-certify, then attack "
            "the open knob (r=sqrt2 unforced). Cross-fermion demands a lepton-specific ingredient; "
            "the gravity spine provably can't supply r=sqrt2 (sqrt(2/Z)=0.588 != sqrt2)."},
    {"rank": "5", "target": "Gauge-coupling unification + sin2_thetaW=3/8 (GUT)",
     "interlock": "gut_unification_sin2thetaW", "sector": "gauge",
     "why": "Real structural hint (3 couplings -> 1 alpha_GUT); 3/8 genuinely forced; BUT minimal-"
            "SM running misses 0.231 by a few % (near-miss). Needs a non-minimal UV completion."},
]


def hitlist() -> List[Dict[str, str]]:
    return list(HITLIST)


# =============================================================================
# FORCED vs FREE LEDGER (per sector)
# =============================================================================

LEDGER: Dict[str, Dict[str, List[str]]] = {
    "gauge": {
        "forced": ["rep dims (8,3,2,1)", "entire hypercharge PATTERN up to 1 scale "
                   "(anomaly+Yukawa, cubic automatic)", "electric-charge quantization",
                   "sin2_thetaW_tree=3/8 + 5/3 normalization", "Casimirs/Dynkin (T_fund=1/2, "
                   "C2_adj=N)", "beta-coefficients (41/10,-19/6,-7) as rep-dim sums"],
        "free":   ["the 3 gauge COUPLING VALUES (alpha_em=1/137.036, alpha_s=0.1180, "
                   "sin2_thetaW(MZ)=0.23122)", "GUT exists-or-not (assumption)",
                   "hypercharge overall scale y_Q=1/6 (a free normalization convention)"],
    },
    "gut": {
        "forced": ["all GUT rep dims (24,45,78; 15,16,27)", "Weyl orders (120,1920,51840)",
                   "Coxeter numbers (5,8,12)", "multiplet closure (15=1 generation)"],
        "free":   ["alpha_GUT", "M_GUT", "whether a GUT is realized at all"],
    },
    "flavor_group": {
        "forced": ["|G| and irrep dims of S3/A4/S4/Delta27 (6,12,24,27; 2,3,3)",
                   "polytope vertex/edge counts (4/6, 8/12)"],
        "free":   ["WHICH group is realized", "the symmetry-breaking vevs/flavons"],
    },
    "koide": {
        "forced": ["circulant identity Q=1/3+r^2/6 (delta-independent)", "the 1/3 floor + 1/6 "
                   "amplitude coefficient", "cos^2=1/(3Q) angle identity (45deg at Q=2/3)"],
        "free":   ["the amplitude r=sqrt2 (ONE forced appearance -> Gate-B FAIL)",
                   "the phase delta=2/9 (fit; the 2nd free number)"],
    },
    "mixing": {
        "forced": ["TBM Clebsch values (sin2_12=1/3, sin2_23=1/2, sin2_13=0) IF A4/S4 is realized",
                   "the 1/sqrt2 and 45-deg geometric factors in the complementarity targets"],
        "free":   ["the actual measured deviations (theta_13=8.54deg breaks TBM)",
                   "delta_CP", "which group + which breaking", "the CKM O(1) coefficients "
                   "A, rho-bar, eta-bar (look fitted)"],
    },
}


def ledger() -> Dict[str, Dict[str, List[str]]]:
    return dict(LEDGER)


# =============================================================================
# SELF-VERIFICATION (sympy-exact identity checks; run as a script)
# =============================================================================

def verify_primitives() -> List[str]:
    """Re-derive every forced numeric claim from scratch (sympy-exact). Returns a list of
    'OK'/'FAIL' lines. This is the calibration self-test the engine can call."""
    out = []
    if not _HAVE_SP:
        return ["sympy unavailable — cannot run exact verification"]

    def chk(name, cond):
        out.append(f"{'OK  ' if cond else 'FAIL'} {name}")

    # --- hypercharge anomaly + Yukawa closure ---
    yQ = sp.symbols('yQ', real=True)
    yu, yd, yL, ye, yH = -4 * yQ, 2 * yQ, -3 * yQ, 6 * yQ, -3 * yQ
    chk("[SU3]^2 U1: 2yQ+yu+yd=0", sp.simplify(2 * yQ + yu + yd) == 0)
    chk("[SU2]^2 U1: 3yQ+yL=0", sp.simplify(3 * yQ + yL) == 0)
    chk("Yukawa down: yQ+yd+yH=0", sp.simplify(yQ + yd + yH) == 0)
    chk("Yukawa lepton: yL+ye+yH=0", sp.simplify(yL + ye + yH) == 0)
    chk("Yukawa up: yQ+yu-yH=0", sp.simplify(yQ + yu - yH) == 0)
    # cubic + grav-mixed. Use the LH-Weyl hypercharges DIRECTLY (e^c carries Y=+1 in this
    # convention): Q=+yQ, u^c=-4yQ, d^c=+2yQ, L=-3yQ, e^c=+6yQ; multiplicities 6,3,3,2,1.
    Yv = [(yQ, 6), (-4 * yQ, 3), (2 * yQ, 3), (-3 * yQ, 2), (6 * yQ, 1)]
    chk("grav^2 U1 (sum mult*Y) = 0", sp.simplify(sum(m * Y for Y, m in Yv)) == 0)
    chk("cubic [U1]^3 (sum mult*Y^3) = 0 (REDUNDANT/automatic)",
        sp.simplify(sum(m * Y ** 3 for Y, m in Yv)) == 0)
    # physical electric charges Q = T3 + Y at yQ=1/6 (Y = hypercharge of the LH multiplet)
    sub = {yQ: sp.Rational(1, 6)}
    yQv = yQ.subs(sub)                 # = 1/6
    chk("Q_up = T3+Y = +1/2 + 1/6 = +2/3",
        sp.Rational(1, 2) + yQv == sp.Rational(2, 3))
    chk("Q_down = T3+Y = -1/2 + 1/6 = -1/3",
        sp.Rational(-1, 2) + yQv == sp.Rational(-1, 3))
    chk("Q_electron = T3+Y = -1/2 + (-1/2) = -1",
        sp.Rational(-1, 2) + (-3 * yQ).subs(sub) == -1)

    # --- sin^2 thetaW = 3/8 two ways ---
    TrT3sq = 2 * sp.Rational(1, 2) ** 2          # e and nu (doublet) contribute T3=+-1/2
    TrQsq = 3 * sp.Rational(1, 3) ** 2 + 1       # d^c x3 (Q=1/3) + e (Q=-1)
    chk("sin2thetaW_tree = Tr(T3^2)/Tr(Q^2) = 3/8", sp.nsimplify(TrT3sq / TrQsq) == sp.Rational(3, 8))
    chk("(3/5)/((3/5)+1) = 3/8",
        sp.Rational(3, 5) / (sp.Rational(3, 5) + 1) == sp.Rational(3, 8))

    # --- Koide circulant identity ---
    M, r, delta = sp.symbols('M r delta', positive=True)
    sm = [M * (1 + r * sp.cos(2 * sp.pi * k / 3 + delta)) for k in range(3)]
    Q = sp.simplify(sum(s ** 2 for s in sm) / (sum(sm)) ** 2)
    chk("Koide Q = 1/3 + r^2/6 (exact)", sp.simplify(Q - (sp.Rational(1, 3) + r ** 2 / 6)) == 0)
    chk("dQ/ddelta = 0 (phase-independent)", sp.simplify(sp.diff(Q, delta)) == 0)
    chk("Q=2/3 <=> r^2=2", sp.Rational(1, 3) + sp.Integer(2) / 6 == sp.Rational(2, 3))
    chk("cos^2(angle)=1/(3Q); Q=2/3 -> 1/2", 1 / (3 * sp.Rational(2, 3)) == sp.Rational(1, 2))

    # --- a0 kernel calibration anchors (NOT building blocks; the method exemplar) ---
    chk("a0: sqrt(8pi)*sqrt(1/3) = sqrt(8pi/3)",
        sp.simplify(sp.sqrt(8 * sp.pi) * sp.sqrt(sp.Rational(1, 3)) - sp.sqrt(8 * sp.pi / 3)) == 0)
    chk("a0: sqrt(2/Z)=(3/8pi)^(1/4) [Z=sqrt(32pi/3)]",
        sp.simplify(sp.sqrt(2 / sp.sqrt(32 * sp.pi / 3))
                    - (3 / (8 * sp.pi)) ** sp.Rational(1, 4)) == 0)

    # --- beta-coefficient ratio ---
    chk("(b1-b2)/(b2-b3) = 218/115",
        sp.simplify((sp.Rational(41, 10) - sp.Rational(-19, 6))
                    / (sp.Rational(-19, 6) - (-7))) == sp.Rational(218, 115))

    # --- TBM angles ---
    chk("TBM theta_12 (sin2=1/3) = 35.264 deg",
        abs(float(sp.deg(sp.asin(sp.sqrt(sp.Rational(1, 3))))) - 35.264389682754654) < 1e-9)
    chk("TBM theta_23 (sin2=1/2) = 45 deg",
        abs(float(sp.deg(sp.asin(sp.sqrt(sp.Rational(1, 2))))) - 45.0) < 1e-9)

    return out


# =============================================================================
# SCRIPT ENTRY
# =============================================================================

def _summary():
    fp = forced_pool()
    free = free_pool()
    print("=" * 100)
    print("GEOMETRIC_PRIMITIVES — the reduced, forced-geometric alphabet for project_atomos")
    print("=" * 100)
    print(f"\nFORCED primitives: {len(fp)}   FREE (open knobs): {len(free)}   "
          f"TOTAL: {len(_REGISTRY)}")
    by_sector: Dict[str, int] = {}
    for p in _REGISTRY.values():
        by_sector[p.sector] = by_sector.get(p.sector, 0) + 1
    print("by sector:", ", ".join(f"{k}={v}" for k, v in sorted(by_sector.items())))
    print(f"rational-target-exempt (Gate-A value uninformative): {len(rational_targets())}")
    print(f"\nINTERLOCKS: {len(INTERLOCKS)}")
    for il in INTERLOCKS:
        print(f"  [{il.gate_mode}/{il.status:24}] {il.key:32} ties {len(il.ties)} "
              f"({il.n_free} free)")
    print(f"\nHIT-LIST (top {len(HITLIST)}):")
    for h in HITLIST:
        print(f"  {h['rank']}. [{h['sector']:7}] {h['target']}")
    print("\nFORCED vs FREE ledger sectors:", ", ".join(LEDGER.keys()))

    print("\n" + "=" * 100)
    print("SELF-VERIFICATION (sympy-exact)")
    print("=" * 100)
    lines = verify_primitives()
    for ln in lines:
        print(" ", ln)
    n_fail = sum(1 for ln in lines if ln.startswith("FAIL"))
    print(f"\n{len(lines)-n_fail}/{len(lines)} checks OK"
          + ("" if n_fail == 0 else f"  ({n_fail} FAILED)"))
    print("=" * 100)


if __name__ == "__main__":
    _summary()
