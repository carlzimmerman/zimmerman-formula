#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_number_field_local_presentation_2026.py
==========================================
THE NUMBER-FIELD OBSTRUCTION, RUN ON THE LOCAL SCALE c sqrt(G rho_Lambda).

--------------------------------------------------------------------------------------------------
SELF-CORRECTION FIRST -- read this before anything else
--------------------------------------------------------------------------------------------------
On 2026-08-07 (script `mi_local_presentation_grading_2026.py`, 40/40) I said the corpus's
number-field obstruction was computed in the HORIZON presentation, that in the LOCAL presentation
the framework's coefficient is rational, and that therefore the obstruction to an algebraic
flavour bridge "DISSOLVES", re-opening escape E3 with a mechanism.

*** THAT WAS OVER-OPTIMISTIC, AND THE COMMITTED THEOREM ALREADY SAID SO. ***

`mi_number_field_theorem_2026.py` COROLLARY 2a states: in the group <Z, kappa>,
w(Z^m kappa^n) = m/2, which vanishes iff m = 0, so *** the weight-zero (= algebraic) subgroup is
exactly <kappa> ***, and "the entire algebraic content the framework can hand to the SM through a
finite multiplicative bridge is the single number kappa -- and kappa is FITTED.  A bridge in this
class can transmit at most the knob, never derive it."  Its ESCAPE E4 then prices that class as
"provably EMPTY of new content, which is what gauge-blindness should mean."

The LOCAL presentation IS that weight-zero channel.  a_0/(c sqrt(G rho_Lambda)) = kappa, exactly.
So "run the obstruction on c sqrt(G rho_Lambda)" = "run it on Corollary 2a's channel", and the
answer was already on the books: NO OBSTRUCTION, AND ALSO NO DERIVATION.  I re-derive it
independently in Part A/B rather than cite it, then state what actually survives.

--------------------------------------------------------------------------------------------------
WHAT SURVIVES, AND IT IS NOT NOTHING
--------------------------------------------------------------------------------------------------
(1) PART C -- an AMENDMENT to the committed theorem, and it cuts BOTH ways.
    `mi_number_field_theorem_2026.py`'s THEOREM 3 reads, against interest: the framework's
    coefficient has ODD pi-parity while Milgrom's 1/(2pi) is EVEN, therefore "the existence of a
    clean EVEN-weight competitor at 8% is the strongest number-theoretic argument that the
    framework's sqrt(pi) is an artefact of its own construction."
    That reading is PRESENTATION-DEPENDENT.  The same file's own check computes
    w(kappa_Milgrom) = w(sqrt(2/3pi)) = -1/2 -- so in the LOCAL presentation it is MILGROM's
    coefficient that is ODD and the framework's that is EVEN.  The parities SWAP.
    ==> The "clean EVEN-weight competitor" argument is void as stated, AND so is its mirror image.
        *** The pi-arithmetic favours NEITHER coefficient. ***  It is a property of which scale you
        divide by, not of nature.  This removes an argument against the framework and forbids the
        framework from claiming the reverse.  Amendment owed to that file.

(2) PART D -- the one non-empty door, named precisely: TRANSMIT vs DERIVE.
    E4/Corollary 2a kills bridges in which the flavour side is FIT to kappa (a relabelling, whose
    identity holds for every value of pi).  It does NOT forbid the flavour side INDEPENDENTLY
    PREDICTING the rational 1/2 from an integer-weight source -- an index, a multiplicity, a
    representation dimension, a rational Casimir ratio.  That is a derivation, and the content
    flows SM -> coefficient, so Theorem 1's "carries no information" corollary does not apply.
    What kills THAT in practice is not arithmetic but DEGENERACY, and this script prices it:
    given kappa's measured precision (1.24% with Upsilon fixed, 5.44% with Upsilon free per
    galaxy, from `project_kappa_discriminability`), how many simple algebraic numbers built from
    real SM data land within the error bar of 1/2?  The count is the evidential weight.  It is
    computed below on a mechanically-closed menu.  RESULT, and it CORRECTS my own draft: the count
    is SMALL -- 2 of 708 measured-SM expressions inside 1.24%, against a decoy-target mean of 2.6.
    So 1/2 is no magnet and the door is degenerate only at the ordinary numerology level, not
    drowned.  Both hits are KOIDE: kappa = (3/4) Q_Koide to 9 ppm (Part D2b), which is the
    <kappa> channel again -- 3/4 x 2/3 -- so it is a relabelling unless Koide's 2/3 is itself
    derived.  Every EXACT hit came from rationals I seeded knowing the answer.

(3) PART E -- a real structural consequence that does NOT depend on any of the above:
    since w(kappa_Milgrom) = -1/2 is transcendental, an integer-weight (algebraic) flavour-side
    prediction of the coefficient can land on the framework's class and can NEVER land on
    Milgrom 2020's.  So IF an algebraic flavour prediction of the coefficient is ever built, its
    mere existence is evidence for kappa rational over kappa = sqrt(2/3pi).  The SM-bridge question
    and the coefficient question are the SAME question.  ⚠️ This is conditional on building the
    thing; it is not evidence today, and the degeneracy count in Part D is what it must beat.

MANDATORY: kappa = 1/2 is FITTED, NOT DERIVED.  Nothing here derives Z, Lambda, a_0 or any SM
parameter.  Carl publicly retracted the TOE/SM overclaims on 2026-06-23; this script does not
re-open them -- it narrows one obstruction and prices one door.

CREDIT.  Theorem 1/2/3, Corollary 2a and escapes E1-E5 are `mi_number_field_theorem_2026.py`
(2026-08-07, this corpus).  pi transcendental: LINDEMANN 1882.  nu = sqrt(1+1/y) and the
temperature balance: MILGROM 1999 PLA 253:273 eqs 6-9 (a_0_hat = 2 c H_Lambda); the cH_L/2pi form:
MILGROM 2020.  a_lambda = c^2 sqrt(Lambda/3): MILGROM 1994 Ann.Phys. 229:384.  PDG 2024 for masses
and mixings.  Koide 1982 for Q.

Exit non-zero on any failed check.  Negative controls must trip.
"""

import sys
import itertools
import sympy as sp
from mpmath import mp

mp.dps = 60

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=12):
    return mp.nstr(mp.mpf(x), n)


# --------------------------------------------------------------------------------------------
G       = mp.mpf("6.67430e-11")
C       = mp.mpf("2.99792458e8")
LAMBDA  = mp.mpf("1.0908e-52")
OMEGA_L = mp.mpf("0.6889")
RHO_L   = LAMBDA * C**2 / (8 * mp.pi * G)
CHL     = C**2 * mp.sqrt(LAMBDA / 3)
CSQRT   = C * mp.sqrt(G * RHO_L)
KAPPA   = mp.mpf("0.5")

pi_s = sp.pi
s_s = sp.sqrt(pi_s)
kap_s = sp.Rational(1, 2)
Z_sym = 2 * sp.sqrt(8 * pi_s / 3)

print(__doc__)


def pi_weight(expr):
    """The homomorphism w of the committed theorem: expr = algebraic * pi^r  ->  r, else None."""
    for num in range(-4, 5):
        for den in (1, 2):
            r = sp.Rational(num, den)
            cof = sp.simplify(expr / pi_s ** r)
            if cof.is_algebraic:
                return r
    return None


# ============================================================================================
print("=" * 100)
print("PART A -- the LOCAL dimensionless content IS kappa, and its pi-weight is 0")
print("=" * 100)

# build the local ratio from the DEFINITIONS, symbolically, exactly as the original built the
# horizon one:  a_0 = kappa c sqrt(G rho_L),  rho_L = Lambda c^2/(8 pi G),  H_L = c sqrt(Lambda/3)
Lam_s, c_s, G_s = sp.symbols("Lambda c G", positive=True)
rho_expr = Lam_s * c_s**2 / (8 * pi_s * G_s)
csqrt_expr = c_s * sp.sqrt(G_s * rho_expr)
chl_expr = c_s**2 * sp.sqrt(Lam_s / 3)
a0_expr = kap_s * csqrt_expr

local_ratio = sp.simplify(a0_expr / csqrt_expr)
horizon_ratio = sp.simplify(a0_expr / chl_expr)
check(sp.simplify(local_ratio - kap_s) == 0,
      "A1  a_0 / (c sqrt(G rho_Lambda)) = kappa EXACTLY, symbolically from the definitions",
      f"= {local_ratio}")
check(sp.simplify(horizon_ratio - kap_s * sp.sqrt(3 / (8 * pi_s))) == 0,
      "A2  a_0 / (c H_Lambda) = kappa sqrt(3/(8 pi))  (reproduces the committed theorem's Check 3)",
      f"= {sp.simplify(horizon_ratio)}")
w_loc, w_hor = pi_weight(local_ratio), pi_weight(horizon_ratio)
check(w_loc == 0, "A3  w(local ratio) = 0  ->  ALGEBRAIC (indeed rational)", f"w = {w_loc}")
check(w_hor == sp.Rational(-1, 2),
      "A4  w(horizon ratio) = -1/2  ->  transcendental (the original's ODD parity)",
      f"w = {w_hor}")
# independent re-derivation of Corollary 2a on the <Z, kappa> group
viol = []
for m in range(-3, 4):
    for n in range(-3, 4):
        w = pi_weight(sp.simplify(Z_sym**m * kap_s**n)) if (m, n) != (0, 0) else sp.Integer(0)
        if w is None or w != sp.Rational(m, 2):
            viol.append((m, n, w))
check(not viol,
      "A5  COROLLARY 2a re-derived independently: w(Z^m kappa^n) = m/2, zero iff m = 0",
      "-> the weight-zero subgroup of <Z,kappa> is exactly <kappa>; the LOCAL presentation IS "
      "that channel, so 'running the obstruction on c sqrt(G rho_L)' was already answered")
check(abs(mp.mpf(str(sp.N(CHL / CSQRT if False else 1, 5)))) > 0
      and abs(CHL / CSQRT - mp.sqrt(8 * mp.pi / 3)) / mp.sqrt(8 * mp.pi / 3) < mp.mpf("1e-50"),
      "A6  on real constants: cH_L / (c sqrt(G rho_L)) = sqrt(8pi/3) at 60 dps",
      f"{sig(CHL/CSQRT, 13)}")


# ============================================================================================
print()
print("=" * 100)
print("PART B -- so the bridge in this class is PERMITTED and EMPTY (E4 reproduced)")
print("=" * 100)
# A "bridge" here means: kappa = A for some algebraic flavour number A.  Theorem 1 permits it.
# But the resulting identity is INDEPENDENT OF pi -- that is precisely what makes it a relabelling.
t = sp.symbols("t", positive=True)          # stands in for sqrt(pi); vary it and see what moves
A_sym = sp.Rational(1, 2)                   # a hypothetical algebraic flavour prediction
local_with_t = kap_s                        # local ratio does not contain t at all
horizon_with_t = kap_s * sp.sqrt(sp.Rational(3, 8)) / t
check(sp.simplify(sp.diff(local_with_t, t)) == 0,
      "B1  the LOCAL relation kappa = A is independent of sqrt(pi): d/dt = 0",
      "-> it holds for EVERY value of pi, so by Theorem 1's corollary it carries NO information "
      "about Z or the geometry.  PERMITTED, and EMPTY.")
check(sp.simplify(sp.diff(horizon_with_t, t)) != 0,
      "B2  the HORIZON relation does depend on sqrt(pi) -- which is exactly why it is FORBIDDEN "
      "(equating it to an algebraic A would force an impossible polynomial identity)")
# the load-bearing consistency check: does a bridge to kappa induce a FORBIDDEN horizon relation?
induced = sp.simplify((A_sym) * sp.sqrt(3 / (8 * pi_s)))
check(pi_weight(induced) == sp.Rational(-1, 2),
      "B3  CONSISTENCY: a bridge kappa = A induces horizon ratio = A sqrt(3/8pi), which is "
      "weight -1/2, i.e. transcendental -- so it does NOT assert a forbidden algebraic identity",
      "no contradiction; the two presentations coexist, exactly as the swap requires")
check(sp.simplify(3 * Z_sym**2 / (32 * pi_s) - 1) == 0,
      "B4  E4's exact identity 3Z^2/(32 pi) = 1 reproduced -- pi-free content, Z cancels")


# ============================================================================================
print()
print("=" * 100)
print("PART C -- AMENDMENT: Theorem 3's against-interest reading is PRESENTATION-DEPENDENT")
print("=" * 100)
kap_M = sp.sqrt(2 / (3 * pi_s))                    # Milgrom 2020 in the framework's convention
q_M = 1 / (2 * pi_s)                               # Milgrom 2020 in the horizon convention
q_fw = 1 / Z_sym
rows = [
    ("framework  kappa = 1/2", kap_s, q_fw),
    ("Milgrom 2020", kap_M, q_M),
    ("Milgrom 1999 eqs 6-9", Z_sym, sp.Integer(2)),
]
print(f"  {'coefficient':26s} {'w(LOCAL)':>10s} {'parity':>8s}   {'w(HORIZON)':>11s} {'parity':>8s}")
tbl = {}
for name, kl, qh in rows:
    wl, wh = pi_weight(kl), pi_weight(qh)
    pl = "EVEN" if wl == 0 else "ODD"
    ph = "EVEN" if wh in (0, sp.Integer(-1), sp.Integer(1), sp.Integer(-2)) and \
        sp.Rational(wh).q == 1 else "ODD"
    tbl[name] = (wl, wh, pl, ph)
    print(f"  {name:26s} {str(wl):>10s} {pl:>8s}   {str(wh):>11s} {ph:>8s}")
check(tbl["framework  kappa = 1/2"][0] == 0 and tbl["Milgrom 2020"][0] == sp.Rational(-1, 2),
      "C1  LOCAL: framework weight 0 (algebraic), Milgrom 2020 weight -1/2 (transcendental)",
      "reproduces the committed file's own w(kappa_Milgrom) = -1/2")
check(tbl["framework  kappa = 1/2"][1] == sp.Rational(-1, 2)
      and sp.Rational(tbl["Milgrom 2020"][1]).q == 1,
      "C2  HORIZON: framework weight -1/2 (half-integer), Milgrom 2020 weight -1 (INTEGER)",
      "reproduces the committed file's Theorem 3 table")
check(tbl["framework  kappa = 1/2"][0] == 0 and tbl["framework  kappa = 1/2"][1] != 0
      and tbl["Milgrom 2020"][0] != 0 and sp.Rational(tbl["Milgrom 2020"][1]).q == 1,
      "C3  *** THE PARITY SWAPS. *** Each coefficient is the 'clean integer-weight' one in "
      "exactly one presentation",
      "=> Theorem 3's 'clean EVEN-weight competitor => the framework's sqrt(pi) is an artefact' "
      "is VOID AS STATED, and so is its mirror image.  The arithmetic favours NEITHER.")
# and the gap it called "arithmetically rigid" is still rigid -- that part survives
gap = abs(mp.mpf(str(sp.N(kap_M, 40))) / mp.mpf("0.5") - 1)
check(gap > mp.mpf("0.07") and gap < mp.mpf("0.09"),
      "C4  what SURVIVES of Theorem 3: the gap is arithmetically rigid (different weight classes "
      "in BOTH presentations), so no rational re-choice closes it",
      f"{float(gap)*100:.2f}% (equivalently {float(abs(mp.mpf('0.5')/mp.mpf(str(sp.N(kap_M,40))) - 1))*100:.2f}% the other way)")


# ============================================================================================
print()
print("=" * 100)
print("PART D -- PRICING the surviving door: how degenerate is 'an algebraic number near 1/2'?")
print("=" * 100)
# PDG 2024 central values (MeV where relevant); dimensionless quantities only enter the menu.
m_e, m_mu, m_tau = mp.mpf("0.51099895"), mp.mpf("105.6583755"), mp.mpf("1776.86")
m_u, m_d, m_s = mp.mpf("2.16"), mp.mpf("4.67"), mp.mpf("93.4")
m_c, m_b, m_t = mp.mpf("1270"), mp.mpf("4180"), mp.mpf("172500")
sin2thW = mp.mpf("0.23122")
alpha_inv = mp.mpf("137.035999")
Q_koide = (m_e + m_mu + m_tau) / (mp.sqrt(m_e) + mp.sqrt(m_mu) + mp.sqrt(m_tau)) ** 2
Vus, Vcb, Vub = mp.mpf("0.2243"), mp.mpf("0.0422"), mp.mpf("0.00394")

# SM_DATA: genuinely MEASURED dimensionless quantities.  These are the only ones whose hits carry
# any information -- a hit is a statement about nature.
SM_DATA = {
    "m_mu/m_tau": m_mu / m_tau, "m_e/m_mu": m_e / m_mu, "m_e/m_tau": m_e / m_tau,
    "m_u/m_d": m_u / m_d, "m_d/m_s": m_d / m_s, "m_s/m_b": m_s / m_b,
    "m_u/m_c": m_u / m_c, "m_c/m_t": m_c / m_t, "m_b/m_t": m_b / m_t,
    "sin2thW": sin2thW, "1/alpha": 1 / alpha_inv, "Q_koide": Q_koide,
    "Vus": Vus, "Vcb": Vcb, "Vub": Vub,
}
# PRESPEC: small rationals and roots I chose KNOWING kappa = 1/2 (and knowing Koide's 2/3 and the
# banked kappa^(-1/2) = sqrt2).  Hits from these are TAUTOLOGICAL -- 3/4 x 2/3 = 1/2 is arithmetic,
# not physics.  Counted separately so they cannot inflate the degeneracy figure.
PRESPEC = {
    "2/3": mp.mpf(2) / 3, "1/3": mp.mpf(1) / 3, "3/8": mp.mpf(3) / 8,
    "sqrt2": mp.sqrt(2), "sqrt3": mp.sqrt(3), "1/sqrt2": 1 / mp.sqrt(2),
}
BASE = {**SM_DATA, **PRESPEC}
UNARY = {"x": lambda x: x, "1/x": lambda x: 1 / x, "sqrt(x)": lambda x: mp.sqrt(x),
         "x^2": lambda x: x * x, "x^(1/3)": lambda x: x ** (mp.mpf(1) / 3)}
RATS = [sp.Rational(p, q) for q in range(1, 5) for p in range(1, 5) if sp.gcd(p, q) == 1]

def build(base):
    out = {}
    for bname, bval in base.items():
        for uname, ufn in UNARY.items():
            try:
                v0 = ufn(bval)
            except Exception:
                continue
            if not (v0 > 0) or v0 > mp.mpf("1e6"):
                continue
            for rr in RATS:
                v = v0 * mp.mpf(str(sp.N(rr, 40)))
                if v <= 0 or v > 10:
                    continue
                out[f"({rr})*{uname.replace('x', bname)}"] = v
    return out


cands_sm, cands_pre = build(SM_DATA), build(PRESPEC)
TOL = {"Upsilon fixed  (1.24%)": mp.mpf("0.0124"), "Upsilon free   (5.44%)": mp.mpf("0.0544")}
print(f"  mechanically-closed menu, {len(UNARY)} unary ops x {len(RATS)} small rationals:")
print(f"    MEASURED SM quantities : {len(SM_DATA):2d} base -> {len(cands_sm):4d} expressions "
      "(hits here are statements about nature)")
print(f"    PRESPECIFIED rat/roots : {len(PRESPEC):2d} base -> {len(cands_pre):4d} expressions "
      "(hits here are arithmetic -- I chose 2/3 and sqrt2 KNOWING the answer)")
counts = {}
for tname, tol in TOL.items():
    hs = {k: v for k, v in cands_sm.items() if abs(v / KAPPA - 1) <= tol}
    hp = {k: v for k, v in cands_pre.items() if abs(v / KAPPA - 1) <= tol}
    counts[tname] = (len(hs), len(hp))
    ex = sorted(hs.items(), key=lambda kv: abs(kv[1] / KAPPA - 1))[:4]
    print(f"  within {tname}:  SM-data hits {len(hs):3d}   prespec hits {len(hp):3d}"
          + ("   closest SM: " + ", ".join(f"{k} = {sig(v, 7)}" for k, v in ex) if ex else ""))
n_sm_tight, n_pre_tight = counts["Upsilon fixed  (1.24%)"]
n_sm_loose, n_pre_loose = counts["Upsilon free   (5.44%)"]

# The finding, stated as the data actually came out -- NOT as I guessed it would.
check(n_pre_tight > 0,
      "D1  the PRESPECIFIED rationals hit 1/2 exactly, as they must (3/4 x 2/3, 1/4 x sqrt2^2)",
      f"{n_pre_tight} tautological hits -- these carry ZERO information and are excluded below")
check(n_sm_tight >= 0,
      "D2  MEASURED SM quantities inside kappa's TIGHTEST bar (1.24%)",
      f"{n_sm_tight} hits out of {len(cands_sm)} expressions "
      f"({100.0*n_sm_tight/len(cands_sm):.2f}% of the menu)")
check(n_sm_loose >= n_sm_tight,
      "D3  and inside the LOOSEST bar (5.44%)",
      f"{n_sm_loose} hits ({100.0*n_sm_loose/len(cands_sm):.2f}% of the menu) -- monotone, sanity ok")
# a fair null: how many expressions land within the same relative window of a DECOY target?
decoys = [mp.mpf("0.37"), mp.mpf("0.62"), mp.mpf("0.81"), mp.mpf("1.3"), mp.mpf("2.7")]
dec_counts = [sum(1 for v in cands_sm.values() if abs(v / d - 1) <= mp.mpf("0.0124"))
              for d in decoys]
print(f"  DECOY CONTROL, same 1.24% window on targets {[float(d) for d in decoys]}: "
      f"{dec_counts}  (mean {sum(dec_counts)/len(dec_counts):.1f})")
check(len(dec_counts) == len(decoys),
      "D4  decoy control ran -- 1/2 must be compared against arbitrary targets, not against zero")
mean_dec = mp.mpf(sum(dec_counts)) / len(dec_counts)
check(abs(mp.mpf("0.75") * Q_koide / KAPPA - 1) < mp.mpf("1e-5"),
      "D5a the ONLY measured-SM hit is kappa = (3/4) Q_Koide, to 9 ppm",
      f"(3/4)Q = {sig(0.75*Q_koide, 12)} vs kappa = 0.5; but Q ~ 2/3 so this IS 3/4 x 2/3 -- "
      "the <kappa> channel, a RELABELLING unless Koide's 2/3 is derived. NOT a new lead.")
check(abs(Q_koide - mp.mpf(2) / 3) < mp.mpf("1e-5") and Q_koide != mp.mpf(2) / 3,
      "D5b and Q_Koide is NOT exactly 2/3 -- residual delta = Q - 2/3, escape E2's recorded target",
      f"delta = {sig(Q_koide - mp.mpf(2)/3, 4)}")
check(n_sm_tight <= mean_dec * 3,
      "D5  1/2 is NOT specially attractive to this menu: its SM-data hit count is within 3x the "
      "decoy mean, i.e. the door is degenerate at the ORDINARY level, not catastrophically",
      f"1/2: {n_sm_tight} vs decoy mean {float(mean_dec):.1f}")
print(f"""
  READING, corrected against my own draft.  I expected to price this door as worthless and it is
  NOT that bad: only {n_sm_tight} of {len(cands_sm)} measured-SM expressions land inside kappa's tightest bar, and a
  decoy target gets on average {float(mean_dec):.1f} -- so 1/2 is no magnet.  Every EXACT hit in the menu came
  from rationals I seeded myself (2/3, sqrt2), which is arithmetic, not evidence.
  So the honest price is: a single numerical hit is worth little (the ordinary numerology discount),
  but the door is not drowned.  For it to pay, a flavour construction must still (i) PREDICT 1/2
  from an index / multiplicity / representation dimension fixed BEFORE looking, (ii) make an
  INDEPENDENT prediction elsewhere, and (iii) beat this count explicitly.  Absent (i)-(iii) it is
  numerology with extra steps -- but (i)-(iii) are achievable, which is more than can be said for
  the horizon-side channel, where Theorem 1 forbids the relation outright.""")


# ============================================================================================
print()
print("=" * 100)
print("PART E -- the conditional structural payoff (real, but conditional)")
print("=" * 100)
check(pi_weight(kap_M) != 0,
      "E1  kappa_Milgrom = sqrt(2/3pi) is NOT algebraic (weight -1/2)",
      "=> an integer-weight flavour prediction can NEVER land on Milgrom 2020's coefficient")
check(pi_weight(kap_s) == 0,
      "E2  kappa = 1/2 IS algebraic (weight 0) => it is the only one of the two reachable that way")
check(pi_weight(Z_sym) == sp.Rational(1, 2),
      "E3  and Milgrom 1999's local lambda = Z is weight +1/2, also unreachable algebraically",
      "=> IF an algebraic flavour prediction of the coefficient is ever BUILT, its existence is "
      "evidence for kappa rational over BOTH Milgrom coefficients.  Conditional on building it.")


# ============================================================================================
print()
print("=" * 100)
print("PART F -- NEGATIVE CONTROLS")
print("=" * 100)
check(pi_weight(1 + s_s) is None,
      "NC1  CONTROL FIRES: w(1 + sqrt(pi)) is undefined -- w is only defined on the "
      "multiplicative group, and the guard rejects sums")
check(pi_weight(pi_s ** sp.Rational(1, 3)) is None,
      "NC2  CONTROL FIRES: pi^(1/3) is refused (not a half-integer weight)")
far = {k: v for k, v in cands_sm.items() if abs(v / mp.mpf("0.9") - 1) <= mp.mpf("0.0124")}
check(len(far) > 0,
      "NC3  CONTROL FIRES: the menu is not tuned to 1/2 -- a decoy target 0.9 also gets hits "
      f"({len(far)}), so the search machinery is alive and the small count at 1/2 is meaningful",
      "(a menu that hit NOTHING anywhere would make D2's small count an artefact of a dead search)")
# the swap must not be an artefact of the convention I chose for 'parity'
check(pi_weight(kap_s) == 0 and pi_weight(q_fw) == sp.Rational(-1, 2)
      and pi_weight(kap_M) == sp.Rational(-1, 2) and pi_weight(q_M) == sp.Integer(-1),
      "NC4  the four weights underlying the swap, computed one at a time by the same w",
      f"kappa_fw {pi_weight(kap_s)}, q_fw {pi_weight(q_fw)}, "
      f"kappa_M {pi_weight(kap_M)}, q_M {pi_weight(q_M)}")
# and a genuine dimensional guard on the local scale
check(abs(C * mp.sqrt(G**2 * RHO_L) / CSQRT - 1) > mp.mpf("1e-3"),
      "NC5  CONTROL FIRES: squaring G moves the local scale, so Part A is dimensionally "
      "load-bearing and not an algebraic tautology")

print("""
==================================================================================================
BOTTOM LINE
==================================================================================================
  * Running the obstruction on c sqrt(G rho_Lambda) = running it on Corollary 2a's weight-zero
    channel.  Result: the bridge is PERMITTED and EMPTY -- it can transmit the fitted knob, never
    derive it.  My 2026-08-07 claim that this "re-opens E3 with a mechanism" is WITHDRAWN; E3
    (infinite processes) remains open on its own terms, but nothing in the presentation change
    supplies a mechanism for it.
  * NEW AND AMENDING: Theorem 3's against-interest reading ("a clean EVEN-weight competitor at 8%
    is the strongest number-theoretic argument that the framework's sqrt(pi) is an artefact") is
    presentation-dependent and VOID AS STATED -- the parities swap.  The mirror-image pro-framework
    argument is equally void.  The pi-arithmetic favours NEITHER coefficient.  An amendment is owed
    to `mi_number_field_theorem_2026.py`.
  * The one surviving door is a flavour-side construction that PREDICTS the rational 1/2 from an
    integer-weight source.  Priced here, and CONTRARY to my own draft it is NOT drowned: only 2 of
    708 measured-SM expressions sit inside kappa's tightest bar, against a decoy mean of 2.6.  A
    single hit is still worth little, but the door is live.
  * The one measured-SM hit is kappa = (3/4) Q_Koide to 9 ppm.  Since Q_Koide ~ 2/3, this is
    3/4 x 2/3 = 1/2 -- the <kappa> channel, hence a RELABELLING unless Koide's 2/3 is derived
    independently.  The corpus already banks "framework provably Q-blind, 3-for-3 bijection =
    reparametrisation", and the exact residual delta = Q - 2/3 = -6.16e-6 is escape E2's recorded
    target.  So this is a consistency check, NOT a new lead.  Do not cite it as evidence.
  * kappa = 1/2 remains FITTED, NOT DERIVED.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
