"""
s2a_candidates_2026.py -- STAGE 2A shared definitions.

Stage 1 returned ZERO survivors.  The brief for stage 2A in that case is: take the three
candidates that got FURTHEST (died last) and prove SYMBOLICALLY, in exact rational
arithmetic, why they die.

The reached-gate profile of the stage-1 screen (mc_report.out) is

    reached Gate-H        76027
    reached Gate-CARRIER  48818
    reached Gate-MOND     15693
    reached Gate-SLIP      1173
    reached Gate-H2          61
    reached Gate-PPN         59      <-- the deepest gate anything reached
    survived                  0

so the deepest non-survivors are the 59 that reached Gate-PPN.  Their operator supports
collapse to THREE structurally distinct theories (mc_deep_audit.out D1); one
representative of each is certified here.  They are chosen to span the three distinct
mechanisms by which a candidate can supply the G2 traceless stress:

  C1  MAXWELL-AETHER / BEKENSTEIN  (46 of the 61 deep supports; the NAMED point)
        P2 = -1/2, V3 = 1/3, V15 = 1, K4 = -1/4 ; M1 = -1, M5 = -4
        AQUAL scalar (chi algebraic) + unit-timelike vector with a Maxwell kinetic term
        + Bekenstein's phi-dependent disformal matter frame.  This is TeVeS's skeleton.

  C2  ALGEBRAIC (KINETIC-FREE) AETHER   (screen_results.json deep_candidates[21])
        P2 = -1/2, V3 = 1/3, V15 = c15, V6 = -1, V9 = 1/4 ; M1, M5
        SAME scalar, but the vector has NO derivative operator at all -- V6 = A^2 and
        V9 = (A^2)^2 are CONSTANTS once the multiplier V15 imposes A^2 = -1.  This is the
        closest thing the whole 108k-candidate search produced to the Palatini DEGENERATE
        archetype (det H = 0 by construction, no propagating mode, no alpha_2 pole from
        a propagating aether).  It is the live lead's own family.

  C3  ALGEBRAIC SYMMETRIC-TRACELESS TENSOR   (screen_results.json deep_candidates[56])
        P2 = -1/2, V3 = 1/3, V4 = -1/5, V10 = -1, V13 = 3/10, V18 = c18 ; M1, M6
        NO vector at all.  The traceless stress is supplied by a rank-2 carrier S_mn with
        a norm multiplier V18 and a phi-dependent disformal S-coupling.  This is the
        "higher Lorentz irrep" escape route that the Part-I no-go explicitly does NOT
        cover.  It is the only tensor-route candidate that ever reached Gate-PPN.

Units throughout (inherited from stage 1): c = 1, a0 = 1, 16 pi G = 1.
In these units pure GR gives, for a sheet of surface density Sigma, Phi' = Psi' = Sigma/8.

Exact rational arithmetic ONLY.  The stage-1 floats are rationalised here and the
rationalisation is recorded so nothing is silently rounded: C1 is exactly rational
already (it is the NAMED Bekenstein point); C2 and C3 carry two stage-1 tuned floats
each, which are kept as exact Rationals of the printed decimal and, wherever a result
depends on them, ALSO carried symbolically so the conclusion is proved for the whole
one-parameter family rather than for one rounded number.
"""
import sympy as sp

# ----------------------------------------------------------------------------------
# symbols
# ----------------------------------------------------------------------------------
# NOTE: these carry NO sympy assumptions, so that they are the SAME objects as the jet
# symbols produced by the reduction (Symbol('phi1', real=True) != Symbol('phi1')).
M1, M2, M3, M4, M5, M6, M7, M8 = sp.symbols('M1 M2 M3 M4 M5 M6 M7 M8')
Sigma = sp.Symbol('Sigma', positive=True)          # sheet surface density
Phi1, Psi1, phi1 = sp.symbols('Phi1 Psi1 phi1')
chi0, chi1 = sp.symbols('chi0 chi1')
A00, A01, Az0, Az1 = sp.symbols('A00 A01 Az0 Az1')
S000, S001, Szz0, Szz1 = sp.symbols('S000 S001 Szz0 Szz1')
lam0, lam1 = sp.symbols('lam0 lam1')

# ----------------------------------------------------------------------------------
# the three deepest candidates, exact
# ----------------------------------------------------------------------------------

R = sp.Rational

C1 = dict(
    name="C1_MAXWELL_AETHER_BEKENSTEIN",
    origin="screen_results.json deep_candidates[3,6,7,...] (NAMED 'TeVeS_disformal'); "
           "46 of 61 deep supports; died Gate-PPN",
    ops={"P2": R(-1, 2), "V3": R(1, 3), "V15": R(1), "K4": R(-1, 4)},
    mpar={"M1_conf_phi": R(-1), "M5_disf_AA_phi": R(-4)},
    exact=True,
    note="exactly rational as recorded; no rationalisation needed",
)

# stage-1 record 21: V15 = 5.776112728794851, M1 = -0.5205591526195664,
#                    M5 = -2.0822366104783496   (M5/M1 = 4.000000... = Bekenstein)
C2 = dict(
    name="C2_ALGEBRAIC_AETHER_NO_KINETIC_TERM",
    origin="screen_results.json deep_candidates[21]; the only deep candidate with NO "
           "vector kinetic operator; died Gate-PPN",
    ops={"P2": R(-1, 2), "V3": R(1, 3), "V6": R(-1), "V9": R(1, 4),
         "V15": sp.nsimplify(sp.Rational('5.776112728794851'))},
    mpar={"M1_conf_phi": sp.Rational('-0.5205591526195664'),
          "M5_disf_AA_phi": sp.Rational('-2.0822366104783496')},
    exact=False,
    note="V15, M1, M5 are stage-1 tuned floats -> exact Rationals of the printed decimal; "
         "every stage-2A conclusion for C2 is ALSO proved with M1, M5, c15 symbolic",
)

# stage-1 record 56: V4 = -0.2, V13 = 0.3, V18 = -0.0978100052871879,
#                    M1 = -0.3435819022520667, M6 = -2.3804060855177314
C3 = dict(
    name="C3_ALGEBRAIC_TRACELESS_TENSOR",
    origin="screen_results.json deep_candidates[56]; the only tensor-route candidate that "
           "reached Gate-PPN; died Gate-PPN",
    ops={"P2": R(-1, 2), "V3": R(1, 3), "V4": R(-1, 5), "V10": R(-1), "V13": R(3, 10),
         "V18": sp.Rational('-0.0978100052871879')},
    mpar={"M1_conf_phi": sp.Rational('-0.3435819022520667'),
          "M6_disf_S_phi": sp.Rational('-2.3804060855177314')},
    exact=False,
    note="V18, M1, M6 are stage-1 tuned floats -> exact Rationals of the printed decimal; "
         "the tensor conclusions are ALSO proved with M1, M6, c18 symbolic",
)

CANDIDATES = [C1, C2, C3]

MFRAME_SYM = {"M1_conf_phi": M1, "M2_conf_chi": M2, "M3_disf_AA": M3, "M4_disf_S": M4,
              "M5_disf_AA_phi": M5, "M6_disf_S_phi": M6, "M7_disf_dphidphi": M7,
              "M8_disf_dphidphi_phi": M8}


def mpar_subs(cand):
    """substitution map  M1..M8 -> the candidate's exact values (absent = 0)."""
    out = {}
    for key, sym in MFRAME_SYM.items():
        out[sym] = cand["mpar"].get(key, sp.S.Zero)
    return out


# ----------------------------------------------------------------------------------
# certificate bookkeeping
# ----------------------------------------------------------------------------------
STATUSES = {"PROVEN", "COMPUTATIONALLY_VERIFIED", "PARTIAL", "ASSUMED", "FAILED"}
_CERTS = []


def cert(candidate, gate, status, claim, residual=None, detail=""):
    assert status in STATUSES, status
    rec = dict(candidate=candidate, gate=gate, status=status, claim=claim,
               residual=("" if residual is None else str(residual)), detail=detail)
    _CERTS.append(rec)
    print(f"\n  [{status:26s}] {candidate:34s} {gate}")
    print(f"      claim   : {claim}")
    if residual is not None:
        print(f"      residual: {residual}")
    if detail:
        for line in detail.strip().split("\n"):
            print(f"      {line}")
    return rec


def dump(path):
    import json
    with open(path, "w") as fh:
        json.dump(_CERTS, fh, indent=1)
    print(f"\n[certificates written -> {path}]  n = {len(_CERTS)}")
    return _CERTS
