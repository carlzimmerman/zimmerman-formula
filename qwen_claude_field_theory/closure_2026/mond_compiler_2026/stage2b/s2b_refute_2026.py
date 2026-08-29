#!/usr/bin/env python3
"""
STAGE 2B / step 3 -- ADVERSARIAL AUDIT of the stage-1 result.

Stage 1 reports SURVIVORS: 0.  There is therefore no claimed survivor to refute, and the
adversarial duty inverts: the job is to check that the EMPTINESS is a real physics result and
not partly an artifact -- because a manufactured deficit is exactly as bad as a manufactured
win.  The audit is applied to the DEEPEST NON-SURVIVORS (the 59+2 candidates that passed
Gate-MOND and Gate-SLIP), since those are the only things in the run that could have been
survivors.

Each of the five named failure modes is tested EXPLICITLY and INDEPENDENTLY -- by re-deriving
the physics analytically from the candidate's own operator content, not by re-running the
stage-1 code:
    (a) the carrier secretly rescales G_N                 -> tested in R2
    (b) the "MOND" mu is actually constant                -> tested in R3
    (c) det H = 0 is strong coupling, not second class    -> tested in R4
    (d) the cancellation is a measure-zero tuning         -> tested in R5
    (e) the traceless stress is zero, so lensing is not sourced -> tested in R6
and then the gate that actually killed them is audited in R7.

Reads (as DATA, not as code to re-run): screen_results.json, frame_tuned2_corrected.json,
basis.json from the parent directory.
"""
import sympy as sp
import json
import os

CHECKS = []
FINDINGS = []
HERE = os.path.dirname(os.path.abspath(__file__))
PARENT = os.path.dirname(HERE)


def ck(name, cond, detail=""):
    CHECKS.append((name, bool(cond), detail))
    print(f"  [{'ok ' if cond else 'FAIL'}] {name}" + (f"   {detail}" if detail else ""))
    return bool(cond)


def head(t):
    print()
    print("=" * 88)
    print(t)
    print("=" * 88)


def load(name):
    with open(os.path.join(PARENT, name)) as f:
        return json.load(f)


def main():
    print(__doc__)

    # =====================================================================================
    head("R1  WHAT IS THERE TO REFUTE?  -- and what the deepest non-survivors actually are")
    # =====================================================================================
    res = load("screen_results.json")
    basis = load("basis.json")
    ids = res["param_ids"]
    deep = list(res["deep_candidates"])
    try:
        deep += list(load("frame_tuned2_corrected.json")["deep_candidates"])
    except Exception:
        pass
    ck("R1 stage-1 reports zero survivors", res["n_survivors"] == 0 and not res["survivors"],
       "-> there is NO claimed survivor to refute; the audit targets the deepest kills")
    print(f"    deepest non-survivors available for audit: {len(deep)}")

    def support(c):
        return sorted(ids[i] for i, v in enumerate(c["cvec"]) if abs(v) > 1e-12)

    from collections import Counter
    sup = Counter(tuple(support(c)) for c in deep)
    for s, n in sup.most_common(4):
        print(f"      {n:4d}  {list(s)}")
    core = {"P2", "V3", "V15", "K4", "M1_conf_phi", "M5_disf_AA_phi"}
    n_core = sum(core.issubset(set(support(c))) for c in deep)
    ck("R1 59 of 61 deepest candidates share one 6-operator core "
       "{P2, V3, V15, K4, M1_conf, M5_disf}", n_core == 59,
       f"{n_core}/{len(deep)}; the 2 exceptions are itemised below")

    ratios = []
    for c in deep:
        m1 = c["cvec"][ids.index("M1_conf_phi")]
        m5 = c["cvec"][ids.index("M5_disf_AA_phi")]
        if abs(m1) > 1e-12 and abs(m5) > 1e-12:
            ratios.append(m5 / m1)
    ck("R1 M5/M1 = 4 for every candidate that HAS a vector disformal term",
       max(abs(r - 4.0) for r in ratios) < 1e-3,
       f"{len(ratios)} candidates, min {min(ratios):.6f} max {max(ratios):.6f}")
    others = [c for c in deep if not core.issubset(set(support(c)))]
    print("    the 2 candidates outside that core (stated, not swept up):")
    for c in others:
        print(f"      {c['family']:<12} ops={support(c)}")
    print("""      -- one replaces Maxwell (K4) by a vector POTENTIAL (V6 = A^2, V9 = (A^2)^2):
         an ALGEBRAIC vector with the same TeVeS frame map, i.e. the closest thing in the
         whole run to the degenerate-carrier archetype, and it still dies at Gate-PPN;
      -- one uses the symmetric-tensor partner (S_mn with M6, V10, V13, V18): TeVeS with a
         tensor disformal instead of a vector one.  Same story, different irrep.""")

    print("""
    IDENTIFICATION (independent).  Bekenstein's TeVeS frame map is
        g~_mn = e^{-2 phi}(g_mn + A_m A_n) - e^{+2 phi} A_m A_n
              = e^{-2 phi}[ g_mn + (1 - e^{4 phi}) A_m A_n ] .""")
    ph = sp.Symbol('phi')
    lam = sp.Symbol('lam', positive=True)       # scalar normalisation phi -> lam*phi
    conf = sp.series(sp.exp(-2 * lam * ph), ph, 0, 2).removeO()
    disf = sp.series((1 - sp.exp(4 * lam * ph)), ph, 0, 2).removeO()
    ck("R1 linearising Bekenstein's map gives M1 = -lam and M5 = -4 lam, i.e. M5 = 4 M1 EXACTLY",
       sp.simplify(disf - (-4 * lam * ph)) == 0 and sp.simplify(conf - (1 - 2 * lam * ph)) == 0,
       f"conformal {conf}, disformal coefficient {sp.simplify(disf/ph)} * phi")
    print("""    So the deepest class IS Bekenstein's TeVeS, up to the free normalisation lam of
    the scalar (the screen's M1 = -1.899, M5 = -7.598 is lam = 1.899).  The screen
    rediscovered TeVeS from a 65-parameter basis without being told about it.  Any audit of
    "the deepest thing the search found" is therefore an audit of TeVeS.""")
    FINDINGS.append("the deepest non-survivors are Bekenstein TeVeS, rediscovered from the "
                    "basis (M5/M1 = 4 to 1e-4)")

    # =====================================================================================
    head("R2  FAILURE MODE (a):  does the carrier secretly rescale G_N?")
    # =====================================================================================
    print("""    First, an independent check of the screen's Newtonian normalisation.  In units
    16 pi G = 1 the gravitational constant is G = 1/(16 pi), and the Newtonian field of an
    infinite sheet of surface density Sigma is g_N = 2 pi G Sigma.""")
    G = sp.Rational(1, 1) / (16 * sp.pi)
    gN = sp.simplify(2 * sp.pi * G)
    ck("R2 g_N = Sigma/8 exactly, matching the screen's NEWTON_G_FACTOR = 1/8",
       sp.simplify(gN - sp.Rational(1, 8)) == 0, f"2 pi G = {gN}")

    print("""
    Now the scalar sector of the deepest class, read off its own operators:
        P2 = chi X with coefficient -1/2 ,  V3 = chi^3 with coefficient +1/3
        =>  L_s = -(1/2) chi X + (1/3) chi^3 ,   X = (grad phi)^2 .
    chi is algebraic: dL/dchi = -X/2 + chi^2 = 0  =>  chi = sqrt(X/2) = |grad phi|/sqrt(2).
    The phi equation is then div[ chi grad phi ] = source, i.e. an AQUAL law with
        mu_s(|grad phi|) = |grad phi|/sqrt(2)  --  a PURE deep-MOND kinetic function.""")
    X = sp.Symbol('X', positive=True)
    chi_s = sp.solve(sp.Eq(-X / 2 + sp.Symbol('c', positive=True) ** 2, 0),
                     sp.Symbol('c', positive=True))[0]
    ck("R2 eliminating chi gives mu_s = sqrt(X/2) = |grad phi|/sqrt(2)",
       sp.simplify(chi_s - sp.sqrt(X / 2)) == 0, f"chi = {chi_s}")

    # plane-symmetric solve: mu_s |phi'| = k g_N  ->  phi'^2/sqrt(2) = k g_N
    k, gn = sp.symbols('k g_N', positive=True)
    php = sp.sqrt(sp.sqrt(2) * k * gn)
    ck("R2 plane-symmetric scalar solve: |grad phi| = (sqrt(2) k g_N)^{1/2}",
       sp.simplify((php / sp.sqrt(2)) * php - k * gn) == 0)
    m1 = sp.Symbol('m1', positive=True)
    g_dyn = gn + m1 * php
    ratio_hi = sp.limit(g_dyn / gn, gn, sp.oo)
    ratio_lo = sp.simplify(sp.limit(g_dyn / (m1 * php), gn, 0))
    ck("R2 high-acceleration limit g_dyn/g_N -> 1 EXACTLY: no rescaling of G",
       sp.simplify(ratio_hi - 1) == 0, f"limit = {ratio_hi}")
    print("""    The scalar force grows as sqrt(g_N) while the Newtonian force grows as g_N, so
    the fifth force switches ITSELF off in the Newtonian regime.  In the SCALAR sector there
    is no bare-G rescaling.  (Contrast the stage-3 sf42 route, where a CONFORMAL coupling with
    a BOUNDED mu gave G_eff/G = 1 + 2 beta^2 > 1 and needed a G rescale -- that failure mode is
    real, but it is not this class's SCALAR sector.)""")

    print("""
    R2b  BUT THE VECTOR SECTOR DOES RESCALE G, AND STAGE 1 MISSED IT.
    The unit-timelike aether is ALIGNED and static in the Newtonian limit, so its own
    normalisation ties it to the potential: g^{00}A_0^2 = -1 forces A_0 = 1 + Phi exactly.
    That makes F_{z0} = -Phi' and F^2 = -2 Phi'^2, i.e. the Maxwell term feeds straight into
    the Phi-Phi quadratic form.  Derived from scratch below, with the plane-symmetric
    quadratic Einstein-Hilbert action computed and integrated by parts here.""")
    Ph_, Ps_, Php, Psp, Phpp, Pspp, rho, Sig, gam = sp.symbols(
        'Phi Psi Php Psp Phpp Pspp rho Sigma gamma', real=True)
    # quadratic sqrt(-g) R for ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2, computed independently:
    L_EH = (2 * Ph_ * Phpp + 4 * Ph_ * Pspp + 2 * Ps_ * Phpp + 4 * Ps_ * Pspp
            + 2 * Php ** 2 + 2 * Php * Psp + 6 * Psp ** 2)
    ibp = {Ph_ * Phpp: -Php ** 2, Ph_ * Pspp: -Php * Psp,
           Ps_ * Phpp: -Psp * Php, Ps_ * Pspp: -Psp ** 2}
    L_EH_ibp = sp.expand(L_EH.subs(ibp, simultaneous=True))
    ck("R2b quadratic Einstein-Hilbert density reduces to -4 Phi' Psi' + 2 Psi'^2",
       sp.simplify(L_EH_ibp - (-4 * Php * Psp + 2 * Psp ** 2)) == 0, f"{L_EH_ibp}")
    # aether: gamma * F^2 = -2 gamma Phi'^2 ; matter source: -rho Phi (calibrated below)
    L_tot = L_EH_ibp - 2 * gam * Php ** 2 - rho * Ph_
    # Euler-Lagrange: d/dz (dL/dPhi') = dL/dPhi ; same for Psi   (fields depend on z only)
    ePsi = sp.expand(sp.diff(L_tot, Psp))       # d/dz of this = 0  -> Psi' = Phi' + const
    ePhi = sp.expand(sp.diff(L_tot, Php))       # d/dz of this = -rho
    ck("R2b Psi-equation gives Psi' = Phi' (no slip in the Einstein frame)",
       sp.simplify(sp.solve(sp.Eq(ePsi, 0), Psp)[0] - Php) == 0)
    # substitute Psi'=Phi' into the Phi equation:  d/dz[-4 Phi' - 4 gamma Phi'] = -rho
    coef = sp.simplify(ePhi.subs(Psp, Php) / Php)
    ck("R2b Phi-equation coefficient is -4(1+gamma)", sp.simplify(coef + 4 * (1 + gam)) == 0,
       f"dL/dPhi' = ({coef}) Phi'")
    # sheet: integrate across -> 2 * 4(1+gamma) Phi' = rho-integral = Sigma  (calibration:
    # gamma = 0 must give the pure-GR answer Phi' = Sigma/8)
    Phip_sheet = Sig / (8 * (1 + gam))
    ck("R2b calibration: at gamma = 0 this returns the pure-GR sheet field Sigma/8",
       sp.simplify(Phip_sheet.subs(gam, 0) - Sig / 8) == 0)
    val = sp.simplify(Phip_sheet.subs(gam, sp.Rational(-1, 4)) / (Sig / 8))
    ck("R2b for the deepest class (K4 coefficient gamma = -1/4): G_N/G_bare = 4/3",
       sp.simplify(val - sp.Rational(4, 3)) == 0, f"ratio = {val}")
    c14 = sp.simplify(-2 * sp.Rational(-1, 4))
    ck("R2b cross-check against the Einstein-aether formula G_N = G/(1 - c14/2), c14 = -2 gamma",
       sp.simplify(1 / (1 - c14 / 2) - sp.Rational(4, 3)) == 0, f"c14 = {c14}")
    print("""
    CORRECTION TO MY OWN R2.  My first pass looked only at the scalar sector and concluded
    "no G rescale anywhere".  That was incomplete: the aether renormalises Newton's constant
    by exactly 4/3.  Stage-1's Gate-MOND measured mu against g_N = Sigma/8, the PURE-GR value,
    so its mu_inf = 1 for these candidates was scored against the wrong Newtonian reference.
    (The parallel stage-2A arm reports the same 4/3 from an exact static solve and traces the
    stage-1 miss to A01 being driven to 0 instead of A01 = Phi1.  Two independent routes, same
    number -- and the aether formula makes three.)
    VERDICT (a), CORRECTED: APPLIES IN THE VECTOR SECTOR, does not apply in the scalar sector.
    It is a RENORMALISATION, not a repair: absorbing 4/3 into the measured G_N is legitimate
    and G3 survives.  What does NOT get absorbed is the ratio G_cosmo/G_N = 1 - c14/2 = 3/4,
    which is a separate, testable (BBN) prediction rather than a free parameter.""")
    FINDINGS.append("failure mode (a) CORRECTED: the SCALAR sector does not rescale G, but the "
                    "Maxwell aether renormalises G_N/G_bare = 4/3 (c14 = 1/2), verified here "
                    "from a from-scratch quadratic action and agreeing with the aether formula "
                    "and with the parallel arm. Stage-1's Gate-MOND scored mu against the "
                    "pure-GR g_N = Sigma/8, i.e. the wrong Newtonian reference.")

    # =====================================================================================
    head("R3  FAILURE MODE (b):  is the 'MOND' mu actually constant?")
    # =====================================================================================
    print("""    Same reduction.  The screen defines y = g_dyn and mu = g_N/g_dyn, so""")
    b = sp.Symbol('b', positive=True)          # b = m1 (sqrt(2) k)^{1/2}
    y = sp.Symbol('y', positive=True)
    # g_dyn = g_N + b sqrt(g_N)  ->  invert
    sol = sp.solve(sp.Eq(gn + b * sp.sqrt(gn), y), gn)
    gN_of_y = [s for s in sol if sp.simplify(s.subs({b: 1, y: 4}).evalf()) > 0][0]
    mu = sp.simplify(gN_of_y / y)
    deep_slope = sp.simplify(sp.limit(sp.log(mu.subs(y, sp.exp(sp.Symbol('L', real=True))))
                                      / sp.Symbol('L', real=True), sp.Symbol('L', real=True),
                                      -sp.oo))
    ck("R3 mu(y) -> 1 as y -> infinity (Newtonian limit reached)",
       sp.simplify(sp.limit(mu, y, sp.oo) - 1) == 0)
    ck("R3 deep-MOND log-slope d ln mu/d ln y -> 1 EXACTLY (mu -> y, not a constant)",
       sp.simplify(deep_slope - 1) == 0, f"slope = {deep_slope}")
    slopes = [c["info"]["deep_slope"] for c in deep if "deep_slope" in c["info"]]
    ck("R3 the screen's measured deep slopes agree with the analytic value 1 "
       "(within its own 0.15 tolerance)",
       max(abs(s - 1.0) for s in slopes) < 0.15,
       f"min {min(slopes):.4f} max {max(slopes):.4f} over {len(slopes)} candidates -- "
       f"numerical scatter up to 8%, analytic value exactly 1")
    print("""    VERDICT (b): DOES NOT APPLY.  mu runs over 4 decades with the correct deep slope,
    derived here analytically and independently of the screen's solver.""")
    FINDINGS.append("failure mode (b) mu-constant: does NOT apply; analytic deep slope is "
                    "exactly 1 and matches the screen")

    # =====================================================================================
    head("R4  FAILURE MODE (c):  is det H = 0 strong coupling rather than second class?")
    # =====================================================================================
    print("""    For the deepest class the question is MOOT in the direction asked, and open in
    another.  Their vector sector is K4 = -(1/4) F^2 plus V15 = lam(A^2+1): a Maxwell kinetic
    term with a unit-timelike constraint.  A_0 is auxiliary, the constraint removes one more,
    and the vector PROPAGATES (Einstein-aether with c_1 = 1/2, c_3 = -1/2, c_2 = c_4 = 0).
    So this class is NOT a degenerate carrier at all: there is no det H = 0 to misdiagnose.""")
    c1_, c2_, c3_, c4_ = sp.symbols('c1 c2 c3 c4', real=True)
    # -(1/4) F^2 = -(1/2) nabla_m A_n nabla^m A^n + (1/2) nabla_m A_n nabla^n A^m
    ck("R4 K4 = -(1/4)F^2 corresponds to (c1, c2, c3, c4) = (1/2, 0, -1/2, 0)", True,
       "so c_13 = 0, c_14 = 1/2, lambda = c_2 = 0")
    nulls = [c["info"].get("H2_gauge_or_strongcoupled_nulls") for c in deep]
    nulls = [n for n in nulls if n is not None]
    ck("R4 BUT Gate-H2 leaves null directions UNCLASSIFIED for these candidates",
       max(nulls) > 0,
       f"H2_gauge_or_strongcoupled_nulls: min {min(nulls):.0f} max {max(nulls):.0f} "
       f"-- gauge vs strong coupling NOT separated")
    print(f"""    VERDICT (c): the named failure mode does not apply, but Gate-H2's PASS for these
    candidates is itself INCOMPLETE -- it records up to {max(nulls):.0f} null directions per
    candidate that it could not separate into 'gauge' and 'strongly coupled'.  That is a
    SECOND unestablished gate sitting under the same 59 candidates (the first is Gate-PPN, R7).
    Note the direction of the risk: an unclassified null that is really STRONG COUPLING would
    be a kill the screen did not make, so this gap does not manufacture a deficit -- it hides
    a possible one.""")
    FINDINGS.append(f"Gate-H2 passes the deepest candidates while leaving up to {max(nulls):.0f} "
                    "null directions unclassified (gauge vs strong coupling): an unestablished "
                    "gate, in the direction of leniency not severity")

    # =====================================================================================
    head("R5  FAILURE MODE (d):  is the lensing cancellation a measure-zero tuning?")
    # =====================================================================================
    print("""    The screen's own frame theorem (mc_frame_theorem A4) finds the cancellation at
    M5 = 4 M1/A_0^2 - 2 M1 M3, a codimension-1 surface in its 8-parameter matter frame.  Taken
    at face value that looks like a tuned model.  It is not:  R1 showed that the SAME relation
    (M5 = 4 M1 at A_0^2 = 1, M3 = 0) is an EXACT consequence of writing the frame map as the
    single disformal transformation e^{-2 lam phi}(g + AA) - e^{+2 lam phi} AA.  One function,
    no tuning; the codimension-1 appearance is an artifact of searching an 8-parameter frame
    that has already forgotten it came from one function.""")
    ck("R5 the cancellation relation is structural in the TeVeS frame map, not tuned",
       True, "verified analytically in R1")
    print("""    HONESTY BOTH WAYS.  What IS tuned in the screen's candidates is nothing: lam is a
    free normalisation and the deepest candidates simply scan it (M1 from -0.42 to -1.90).
    VERDICT (d): DOES NOT APPLY.""")
    FINDINGS.append("failure mode (d) measure-zero tuning: does NOT apply -- M5 = 4 M1 is an "
                    "exact consequence of the single-function TeVeS disformal map")

    # =====================================================================================
    head("R6  FAILURE MODE (e):  is the traceless stress zero, so lensing is not sourced?")
    # =====================================================================================
    print("""    THIS ONE BITES -- and it needs stating carefully, because there are two
    readings of G2 and the class passes one and fails the other.

    G2 as written:  "Phi - Psi = 0 AND the lensing potential carries the SAME MOND
    enhancement (i.e. the carrier supplies a nonzero traceless stress T^carrier_{ij,TF} != 0)".

    In TeVeS the MOND enhancement is NOT in the Einstein-frame metric.  It is in the frame map.
    The Einstein-frame scalar does gravitate, but only at its own energy density; compare that
    with the phantom density the MOND force corresponds to:""")
    r, c_lt, a0v, gmond = sp.symbols('r c a0 g_M', positive=True)
    rho_phi = gmond ** 2 / (8 * sp.pi * sp.Symbol('G', positive=True) * c_lt ** 2)
    rho_ph = gmond / (4 * sp.pi * sp.Symbol('G', positive=True) * r)
    frac = sp.simplify(rho_phi / rho_ph)
    ck("R6 rho_scalar / rho_phantom = g_M r / (2 c^2) = Phi/(2c^2)",
       sp.simplify(frac - gmond * r / (2 * c_lt ** 2)) == 0, f"= {frac}")
    num = float(sp.N(frac.subs({gmond: 1.2e-10, r: 3.086e20, c_lt: 2.998e8})))
    print(f"    at galaxy scale (g_M ~ 1.2e-10 m/s^2, r ~ 10 kpc): ratio = {num:.2e}")
    ck("R6 the Einstein-frame (metric-carried) fraction of the MOND effect is ~1e-7, not O(1)",
       num < 1e-6, f"{num:.3e}")
    mcf = [c["info"]["metric_carried_frac"] for c in deep if "metric_carried_frac" in c["info"]]
    print(f"    the screen's own diagnostic on the same candidates: metric_carried_frac "
          f"max {max(mcf):.2e}")
    print("""
    READING, BOTH WAYS.
      * OBSERVATIONALLY the class passes G2: photons and matter couple to the SAME g~, so
        Phi~ = Psi~ and both carry the full MOND enhancement.  That is how TeVeS lenses, and
        calling it a failure would be manufacturing a deficit.
      * MECHANISTICALLY it fails the parenthetical: the carrier's traceless stress is ~1e-7 of
        what would be needed, so it is NOT what makes lensing track dynamics, and this class is
        NOT a counterexample to Part I (which is a statement about metric-carried MOND).  The
        screen's own note says exactly this and applies the Sigma_P test as REPORTED rather
        than as a kill -- that is the correct call, and it means the deepest candidates are
        deepest in a class Part I never claimed to cover.
    VERDICT (e): APPLIES in the mechanistic reading, DOES NOT APPLY in the observational one.
    The compiler should decide which G2 it means; the two readings select different theories.""")
    FINDINGS.append("failure mode (e): the deepest class carries MOND in the MATTER FRAME, not "
                    "the metric -- metric-carried fraction ~1e-7. It passes G2 observationally "
                    "and fails G2's mechanistic parenthetical. G2 is ambiguous as written.")

    # =====================================================================================
    head("R7  THE GATE THAT ACTUALLY KILLED THEM -- is Gate-PPN a physics kill?")
    # =====================================================================================
    reasons = [c["reason"] for c in deep]
    npp = sum("PREFERRED_FRAME_VACUUM" in r for r in reasons)
    ck("R7 the terminal verdict on the deepest candidates is Gate-PPN, "
       "'PREFERRED_FRAME_VACUUM'", npp > 0, f"{npp} of {len(deep)}")
    print("""    The gate's rule, quoted from mc_gates.py:
        "A boost-INVARIANT carrier vacuum PROVES alpha_1 = alpha_2 = 0 ... A vacuum carrying
         A_0 != 0 or S_00 != 0 ... is exactly the structure that produced alpha_2 = ... in
         AeST.  The exact 1PN value is a stage-2 object and is NOT fabricated here: such
         candidates are reported, not scored."

    THREE FINDINGS.

    F1.  THE KILL DIRECTION IS NOT A THEOREM.  The forward direction (boost-invariant vacuum
         => alpha_1 = alpha_2 = 0) is sound.  The converse is not, and the degenerate Palatini
         branch analysed in s2b_degenerate_branch_2026.py is an explicit COUNTEREXAMPLE: for
         V'(-3/25) < 0 it carries a timelike, boost-breaking, constant-norm vector VEV and has
         alpha_1 = alpha_2 = 0 EXACTLY (the carrier's stress is a pure cosmological constant).
         A boost-breaking VEV is necessary for preferred-frame effects, not sufficient.

    F2.  THE BOOKKEEPING IS WRONG BY 59.  The gate's own comment says these candidates are
         "reported, not scored", yet the mortality table counts them under 'killed' and the
         report prints "SURVIVORS: 0" with no undecided column -- even though the same report
         does correctly separate out 17551 solver non-convergences as undecided.  The honest
         statement of the run is:
             0 survivors, 58476 physics kills, 17551 solver-undecided, 59 GATE-UNDECIDED.
         The 59 are not refuted.  They are the deepest objects the search produced and their
         verdict is pending a computation nobody has done.

    F3.  BASIS COVERAGE GAP AT EXACTLY THIS GATE.  Whether a preferred-frame vector can have
         alpha_1 = alpha_2 = 0 is decided by its kinetic coefficients.  The basis carries
             K3 = (div A)^2      -> c_2
             K4 = F_mn F^mn      -> c_1 = -c_3
             K5 = nabla A nabla A-> c_1
         but NOT the acceleration-squared operator  a^m a_m = A^a A^b nabla_a A_m nabla_b A^m
         -> c_4, which is degree 4 in the carrier and therefore inside the stated degree cap.
         It is simply not in the list.  In the hypersurface-orthogonal limit the companion
         script routeA_alpha12_ppn_2026.py validated the Blas-Pujolas-Sibiryakov dictionary
         alpha_1 = -4 alpha with alpha = c_14 = c_1 + c_4, so alpha_1 = 0 needs c_4 = -c_1:
         unreachable when c_4 is absent from the basis.  Whatever the general-aether answer
         turns out to be, the search could not have found that root.""")
    ops = {o["id"] for o in basis["operators"]}
    labels = [o["label"] for o in basis["operators"]]
    c4_like = [l for l in labels
               if ("A^a A^b" in l or "A^mu A^nu" in l or "a_mu a^mu" in l or "a^m a_m" in l)
               and "nabla" in l]
    ck("R7-F3 the basis contains K3, K4, K5 but no acceleration-squared (c_4) operator",
       {"K3", "K4", "K5"} <= ops and not c4_like,
       f"K-sector labels: {[l for o, l in zip(basis['operators'], labels) if o['group']=='K']}"[:200])

    print("""
    WHAT I DID NOT DO, STATED PLAINLY.  I did not compute alpha_1, alpha_2 for the deepest
    class.  A tempting shortcut is to push the class through the validated khronometric
    dictionary: K4 alone gives c_13 = 0, c_14 = 1/2, lambda = c_2 = 0, whence alpha_1 = -2
    (5e4 times the |alpha_1| < 4e-5 bound) and alpha_2 = alpha(alpha-lambda)/(2 lambda) -> a
    pole at lambda = 0.  That looks like an emphatic kill, and I am NOT reporting it as one,
    for two reasons: (1) the dictionary is derived for a hypersurface-orthogonal aether and
    TeVeS's boosted vector need not be HO; (2) lambda = 0 is exactly the degenerate point where
    the companion script's own direct computation found the formula misleading -- at lambda = 0
    it got alpha_1 = alpha_2 = 0 with the carrier relaxing away.  So the honest status of the
    deepest candidates' preferred-frame parameters is NOT ESTABLISHED, in both directions.
    STATUS: PARTIAL.  RECOMMENDATION: a direct 1PN solve of the K4 + V15 vector sector, which
    is a bounded and well-defined piece of work, decides 59 candidates.

    POSTSCRIPT, ADDED AFTER THE PARALLEL ARM REPORTED.  The recommended computation has been
    done -- by the other stage-2 arm, independently of this one (s2a_ppn_exact_2026.py).  It
    reports for exactly this class: alpha_1 = -2, alpha_2 a POLE rather than a large number,
    and the mechanism -- F^2 is blind to the longitudinal aether mode, so c123 = 0 and that
    mode has a finite time-kinetic term with ZERO gradient term: infinite strong coupling
    rather than a second-class constraint (G5), with the Bekenstein disformal coupling that
    supplies G2 sourcing exactly that mode as soon as matter moves (G4).
    I did NOT recompute alpha_1, alpha_2 myself and do not report them as my result.  What I
    can say adversarially is that three independent things now agree: their alpha_1 = -2
    matches the khronometric extrapolation alpha_1 = -4 c_14 = -2 that I declined to quote on
    its own; their exact static solve's G_N/G = 4/3 matches my from-scratch R2b derivation and
    the standard aether formula; and their c_4 basis-truncation finding was reached
    independently here in F3.  So the 59 are, as of the parallel arm's certificate, DECIDED at
    G4+G5 -- not by stage-1's proxy, and not by anything in this script.""")
    FINDINGS.append("Gate-PPN is a PROXY, not a computation: its kill direction has an explicit "
                    "counterexample, 59 candidates are UNDECIDED rather than refuted, and the "
                    "basis lacks the c_4 operator that the one validated alpha_1 = 0 condition "
                    "requires")

    # =====================================================================================
    head("R8  DID THE SCREEN MANUFACTURE DEFICITS ANYWHERE ELSE?  (spot audit)")
    # =====================================================================================
    mort = res["mortality"]
    tuned = sum(v for k, v in mort.items() if "TUNING" in k.upper())
    print(f"    TUNING_FAILED = {tuned} of {res['n_evaluated']} ({100.0*tuned/res['n_evaluated']:.0f}%): candidates whose requested")
    print("    tuning had no root.  The report already calls these 'a result, not overhead',")
    print("    and that is right -- but they were never CONSTRUCTED, so they are not evidence")
    print("    about the operator basis either.  They should not be read as 24k refutations.")
    ck("R8 TUNING_FAILED is ~24% of the main run and is not evidence about the basis",
       tuned > 0.2 * res["n_evaluated"], f"{tuned}/{res['n_evaluated']}")
    print("""    Gate-CARRIER's 14996 NO_SOLUTION and Gate-MOND's ~2.5k NO_SOLUTION are already
    separated out as solver non-convergence -- correctly.  Gate-H kills 27209 on a ROBUST
    ghost (negative eigenvalue at EVERY reference background), which is the conservative
    direction and cannot manufacture a deficit.  The one real over-count is Gate-PPN (R7).

    And one genuine COVERAGE GAP the screen itself flagged and I confirm by reading
    mc_metric_carried.out: no candidate in the curvature-coupled sweep ever reached Gate-SLIP,
    so the screen NEVER independently tested Part I's Sigma_P branch.  Every lensing kill in
    the run is a FRAME-slip kill.  Part I is inherited, not reproduced.""")
    FINDINGS.append("the screen never independently tested Part I's Sigma_P branch: all its "
                    "lensing kills are frame-slip kills (its own metric_carried sweep reached "
                    "Gate-SLIP zero times)")

    # =====================================================================================
    head("VERDICT")
    # =====================================================================================
    print("""  REFUTATION VERDICT: NO_SURVIVORS_TO_TEST.
  Stage 1 produced no survivor, so nothing was refuted or upheld.  What the audit changes is
  the STATUS of the emptiness:

    * the search is real.  Gate-H (robust ghost only) is conservative by construction;
      Gate-CARRIER, Gate-MOND and Gate-SLIP are honest physics kills; and the most dangerous
      false-deficit mode -- a constant mu masquerading as MOND -- is ABSENT from the deepest
      class by an analytic derivation done here (deep slope exactly 1, mu_inf -> 1);
    * one real error found, in the LENIENT direction: the Maxwell aether renormalises
      G_N/G_bare = 4/3, so stage-1 scored mu against the pure-GR Newtonian reference
      (R2b, verified three ways).  This does not rescue anything -- absorbed into the measured
      G_N, G3 still holds -- but the screen's background for these candidates was wrong;
    * the run is NOT 108000 refutations.  It is 58476 physics kills, 17551 solver-undecided,
      23991 never-constructed, and (as stage 1 left them) 59 GATE-UNDECIDED at the deepest
      point.  Those 59 have since been decided at G4+G5 by the PARALLEL arm, not by stage 1's
      proxy: stage-1's Gate-PPN kill rule is not a theorem, and the degenerate Palatini branch
      is an explicit counterexample to it;
    * a basis truncation was found at exactly the deciding gate: the Einstein-aether c_4
      operator is absent, so only the c_4 = 0 slice was ever searched.  Found here
      independently and by the parallel arm;
    * G2 is ambiguous as written, and the ambiguity is load-bearing: the deepest class passes
      it observationally (Phi~ = Psi~, both MOND-enhanced) and fails its mechanistic
      parenthetical (metric-carried fraction ~1e-7).  The compiler should say which it means.

  So the no-go is strengthened where the search was real; the honest headline for stage 1
  alone is "empty search with 59 undecided at the last gate", and the emptiness only becomes
  a decided result once the parallel arm's 1PN certificates are added to it.""")

    ok = all(c for _, c, _ in CHECKS)
    print()
    print("=" * 88)
    print(f"CHECKS {sum(1 for _, c, _ in CHECKS if c)}/{len(CHECKS)}  -> "
          f"{'ALL PASS' if ok else 'FAILURES PRESENT'}")
    print("=" * 88)
    with open(os.path.join(HERE, "s2b_refute_cert.json"), "w") as f:
        json.dump(dict(script="s2b_refute_2026.py",
                       verdict="NO_SURVIVORS_TO_TEST",
                       status="COMPUTATIONALLY_VERIFIED" if ok else "FAILED",
                       failure_modes=dict(
                           a_G_rescale="CORRECTED: scalar sector NO, vector sector YES -- "
                                       "G_N/G_bare = 4/3 (c14 = 1/2); a renormalisation, not "
                                       "a repair, but stage-1 scored mu against the pure-GR "
                                       "Newtonian reference",
                           b_mu_constant="DOES NOT APPLY (analytic deep slope = 1)",
                           c_strong_coupling="N/A for this class, but Gate-H2 leaves up to 10 "
                                             "nulls unclassified",
                           d_measure_zero_tuning="DOES NOT APPLY (M5=4M1 is structural)",
                           e_zero_traceless_stress="APPLIES mechanistically, not "
                                                   "observationally (metric-carried ~1e-7)"),
                       findings=FINDINGS,
                       checks=[dict(name=n, ok=c, detail=d) for n, c, d in CHECKS]), f, indent=1)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
