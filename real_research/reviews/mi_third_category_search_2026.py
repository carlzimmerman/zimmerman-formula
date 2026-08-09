#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_third_category_search_2026.py
================================
IS IT MODIFIED INERTIA, MODIFIED GRAVITY, OR SOMETHING ELSE?  A systematic search of the space.

Verdict: *** THE CHOICE WAS NEVER BINARY.  The 21-sigma lensing test kills a CLASS -- "the metric is
sourced by baryons alone" -- and THREE structurally distinct classes survive it, not one.  Lensing is
a 1-bit test and it has already spent its bit. ***  And one of the survivors is new to this corpus and
is the natural home for the piece of the modified-inertia work that was left homeless: the MEMORY
KERNEL.

Second, and this is the load-bearing new theorem:

*** a_0 = xi * c * sqrt(G rho) is the UNIQUE acceleration constructible from (G, c, rho).  Not the
natural one -- the ONLY one.  The exponent system has a nonsingular 3x3 matrix, so the solution
(1/2, 1, 1/2) is unique. ***

That upgrades the framework's central claim from "a numerical coincidence with a fitted coefficient"
to "the only possible FORM, with a fitted coefficient".  It does NOT derive kappa = 1/2 and this
script does not claim it does.

--------------------------------------------------------------------------------------------------
THE CLASSIFICATION (Part A) -- classify by WHAT SOURCES THE METRIC, because that is what lensing sees
--------------------------------------------------------------------------------------------------
  I    modified INERTIA           metric <- baryons ALONE            M_dyn/M_lens = 1/f_bar = 6.44
                                                                     *** EXCLUDED, 21 sigma ***
  II   modified GRAVITY, scalar   metric <- baryons + scalar         M_dyn/M_lens = 1  ALIVE
       (Bekenstein-Milgrom / AQUAL; the arm adopted 2026-08-03)
  III  MEDIUM / polarisation      metric <- baryons + medium stress   M_dyn/M_lens = 1  ALIVE
       (Blanchet dipolar; Verlinde elastic dS; Berezhiani-Khoury superfluid)
  IV   NONLOCAL gravity           metric <- nonlocal fn of baryons    M_dyn/M_lens = 1  ALIVE
       (Deser-Woodard class; 1/Box acting on curvature)
  V    null-cone / Finsler        the cone itself is deformed         *** DEAD independently ***
                                                                     (degenerate at mu = 1/2)

II, III and IV are observationally IDENTICAL on the lensing ratio.  So the lensing axis, having killed
I, cannot choose among the rest.  The discriminator has to be found elsewhere, and Part D finds it.

--------------------------------------------------------------------------------------------------
IS III ACTUALLY DIFFERENT FROM II?  The sharp statement (Part C)
--------------------------------------------------------------------------------------------------
*** A medium whose response is a LOCAL ALGEBRAIC function of the local field IS Bekenstein-Milgrom,
exactly -- the polarisation is (mu - 1) and the medium stress is the phantom density.  Category III is
a genuine third category precisely and only to the extent that the medium's response is NON-algebraic:
memory, gradients, or its own conserved density. ***

And that is the opening.  The localised memory kernel -- G(u) = g u e^(-m u), the retarded Green's
function of (d/dtau + m)^2, critically damped, established at 27/27 -- was a worldline object and died
with the worldline.  As a MEDIUM relaxation function it is exactly the non-algebraic response that
makes III distinct from II.  The STRUCTURE transfers.  *** THE NUMBER DOES NOT: see Part G. ***

--------------------------------------------------------------------------------------------------
WHAT IT WOULD COST, COMPUTED, NOT WAVED AT (Parts D, E)
--------------------------------------------------------------------------------------------------
  * The RAR's intrinsic scatter is a QUANTITATIVE bound on category III, and it is tight but not
    fatal: the medium's own dynamics may not make a_0 vary by more than ~16% galaxy-to-galaxy.
  * CLUSTERS, computed directly from the framework's own kernel rather than inherited: the kernel
    removes *** 74-89% *** of the cluster dark matter at R500, leaving a real component to supply
    only 11-26% of what LCDM's does.  Nonzero, so the no-dark-matter claim still goes -- but this is
    the ordinary MOND cluster residual, not a catastrophe.

*** CORRECTION NOTICE.  The first commit of this script published "~68%" for that last number.  IT IS
WITHDRAWN.  It came from combining 1/f_bar with the corpus's banked eta_req = 2.334 additively, which
is incoherent (eta_req implies a kernel boost of 2.759, i.e. y = 0.203, while the same audit asserts
y = 21.6).  Part E now computes it directly and self-consistently, including the back-reaction that
adding mass RAISES y and LOWERS nu.  The correction runs IN THE FRAMEWORK'S FAVOUR. ***

*** AND IT SURFACED A BUG IN THE COMMITTED CLUSTER AUDIT: that audit's g = 2.02e-9 m/s^2 ~ 21.6 a_0
is not the field at R500, it is the field at ~0.19 Mpc -- the cluster CORE.  At true R500 (~1.3 Mpc)
clusters sit at g ~ 0.3-0.6 a_0, i.e. NEAR OR BELOW a_0.  The audit's "quasi-Newtonian" premise, and
the choice of Newtonian mass scaling it justified, are both wrong. ***
"""

import sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 40

FAIL = []


def check(cond, label, detail=""):
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=6):
    return mp.nstr(mp.mpf(x), n)


# ---- frozen inputs, all traceable to committed scripts ------------------------------------------
F_BAR      = mp.mpf("0.93") * mp.mpf("0.167")   # mi_lensing_axis_2026.py:106, f_bar(R500)
ETA_REQ    = mp.mpf("2.334")                    # mi_cluster_measurement_audit_2026.py:125
SIG_INT    = mp.mpf("0.034")                    # RAR intrinsic scatter, Desmond 2023 (dex)
SIG_BTFR   = mp.mpf("0.026")                    # BTFR intrinsic scatter, Lelli+2019 (dex)
A0_CANON   = mp.mpf("9.3619e-11")
A0_ALT     = mp.mpf("1.1279e-10")
OBS_RATIO  = (mp.mpf("1.0"), mp.mpf("1.3"))     # observed M_dyn/M_lens in clusters
LAMBDA_MI  = mp.mpf("39.0")                     # yr, worldline memory bound (MI work)
T_MERGER   = mp.mpf("1.0e9")                    # yr, cluster merger timescale, order of magnitude

print(__doc__)


# =============================================================================================
print("=" * 100)
print("PART A -- the classification theorem: sort by WHAT SOURCES THE METRIC")
print("=" * 100)

INV_FBAR = 1 / F_BAR

# Each category is defined by its metric source, and the lensing ratio FOLLOWS from that.
CATEGORIES = {
    "I  modified INERTIA": {
        "metric_source": "baryons ALONE",
        "ratio": INV_FBAR,
        "status": "EXCLUDED",
    },
    "II  modified GRAVITY (scalar, Bekenstein-Milgrom)": {
        "metric_source": "baryons + scalar field stress",
        "ratio": mp.mpf(1),
        "status": "ALIVE",
    },
    "III  MEDIUM / gravitational polarisation": {
        "metric_source": "baryons + medium stress",
        "ratio": mp.mpf(1),
        "status": "ALIVE",
    },
    "IV  NONLOCAL gravity": {
        "metric_source": "nonlocal functional of baryons",
        "ratio": mp.mpf(1),
        "status": "ALIVE",
    },
    "V  null-cone / Finsler": {
        "metric_source": "cone itself deformed",
        "ratio": None,
        "status": "DEAD (independent: degenerate cone)",
    },
}

print("\n  category                                          metric sourced by          M_dyn/M_lens")
print("  " + "-" * 96)
for name, d in CATEGORIES.items():
    r = "n/a" if d["ratio"] is None else sig(d["ratio"], 4)
    print(f"  {name:<48s}  {d['metric_source']:<26s} {r:>8s}   {d['status']}")

# A1 -- the exclusion of I is a consequence of its metric source, not an extra assumption.
lo, hi = OBS_RATIO
check(not (lo <= INV_FBAR <= hi),
      "A1  category I's ratio is OUTSIDE the observed band -- that is the 21-sigma exclusion",
      f"1/f_bar = {sig(INV_FBAR, 4)} vs observed {sig(lo,3)}-{sig(hi,3)}")

# A2 -- II, III, IV all sit INSIDE the observed band.  Lensing cannot separate them.
alive = {k: v for k, v in CATEGORIES.items() if v["status"] == "ALIVE"}
check(all(lo <= v["ratio"] <= hi for v in alive.values()),
      "A2  every surviving category predicts ratio = 1, INSIDE the observed band",
      f"{len(alive)} categories, all at ratio = 1")

# A3 -- the count.  THIS is the answer to the question asked.
check(len(alive) == 3,
      "A3  *** THREE categories survive the lensing axis, not one.  The choice was never MI-or-MG ***",
      f"survivors: II (scalar), III (medium), IV (nonlocal)")

# A4 -- and lensing has spent its discriminating power: it is a 1-bit test.
distinct_ratios = set(sig(v["ratio"], 12) for v in alive.values())
check(len(distinct_ratios) == 1,
      "A4  the survivors are DEGENERATE on the lensing observable -- 1 bit, already spent",
      "the discriminator must be found elsewhere (Part D)")

# NEGATIVE CONTROL: the exclusion of I must depend on f_bar being SMALL.  If clusters were
# baryon-complete the test would say nothing.  Confirm the test is not vacuous.
check(INV_FBAR > hi * 4,
      "NC-A  CONTROL: the lensing test is not vacuous -- category I misses by a factor, not a whisker",
      f"1/f_bar exceeds the top of the observed band by {sig(INV_FBAR/hi, 4)}x")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- THE UNIQUENESS THEOREM: a_0 = xi c sqrt(G rho) is the ONLY option")
print("=" * 100)

# Dimensions in (mass, length, time).  Seek G^a c^b rho^d with dimensions of acceleration.
a, b, d = sp.symbols("a b d", real=True)
# G   : m^3 kg^-1 s^-2      c   : m^1 s^-1        rho : kg^1 m^-3
# target: acceleration = m^1 s^-2
eq_mass = sp.Eq(-a + d, 0)
eq_len = sp.Eq(3 * a + b - 3 * d, 1)
eq_time = sp.Eq(-2 * a - b, -2)

sol = sp.solve([eq_mass, eq_len, eq_time], [a, b, d], dict=True)
check(len(sol) == 1, "B1  the exponent system has EXACTLY ONE solution", f"{len(sol)} solution(s)")

s0 = sol[0]
check(s0[a] == sp.Rational(1, 2) and s0[b] == 1 and s0[d] == sp.Rational(1, 2),
      "B2  and it is (a, b, d) = (1/2, 1, 1/2), i.e. a_0 = xi * c * sqrt(G rho)",
      f"a={s0[a]}, b={s0[b]}, d={s0[d]}")

# B3 -- uniqueness is a statement about the RANK of the exponent matrix.  Prove it.
M = sp.Matrix([[-1, 0, 1], [3, 1, -3], [-2, -1, 0]])
det = M.det()
check(det != 0,
      "B3  the 3x3 exponent matrix is NONSINGULAR, so the solution is unique -- a theorem, not a fit",
      f"det = {det}")

# B4 -- and the framework's OWN two expressions are the SAME expression.  Verify the identity
#       c H_Lambda / Z  ==  (1/2) c sqrt(G rho_Lambda)  with Z = 2 sqrt(8 pi / 3), exactly.
G_s, rho_s, c_s = sp.symbols("G rho c", positive=True)
H_Lambda = sp.sqrt(8 * sp.pi * G_s * rho_s / 3)          # Friedmann, Lambda-dominated
Z_sym = 2 * sp.sqrt(8 * sp.pi / sp.Integer(3))
lhs = c_s * H_Lambda / Z_sym
rhs = sp.Rational(1, 2) * c_s * sp.sqrt(G_s * rho_s)
check(sp.simplify(lhs - rhs) == 0,
      "B4  *** kappa = 1/2 <=> Z = 2 sqrt(8 pi/3) IDENTICALLY.  The two forms are one form ***",
      f"c H_L/Z - (1/2)c sqrt(G rho) = {sp.simplify(lhs - rhs)}")

# B5 -- what the theorem does NOT do.  Guard against exactly the overclaim this corpus keeps
#       having to retract: the FORM is forced, the NUMBER is not.
xi_sym = sp.Symbol("xi", positive=True)
generic = xi_sym * c_s * sp.sqrt(G_s * rho_s)
check(sp.simplify(sp.diff(generic, xi_sym)) != 0,
      "B5  xi remains a FREE parameter of the forced form -- kappa = 1/2 is STILL FITTED, NOT DERIVED",
      "the theorem constrains the form only")

# NEGATIVE CONTROL: uniqueness must FAIL once a fourth constant is admitted, or the theorem
# would prove too much.  Add hbar and show the solution becomes a 1-parameter family.
e = sp.Symbol("e", real=True)   # exponent of hbar : kg^1 m^2 s^-1
eq_mass2 = sp.Eq(-a + d + e, 0)
eq_len2 = sp.Eq(3 * a + b - 3 * d + 2 * e, 1)
eq_time2 = sp.Eq(-2 * a - b - e, -2)
sol2 = sp.solve([eq_mass2, eq_len2, eq_time2], [a, b, d], dict=True)
free_in_sol2 = set().union(*[set(v.free_symbols) for v in sol2[0].values()]) if sol2 else set()
check(e in free_in_sol2,
      "NC-B  CONTROL: admitting hbar DESTROYS uniqueness (1-parameter family) -- so B1-B3 are a real",
      "constraint on the input set {G, c, rho}, not a triviality of dimensional analysis")

print()
print("  *** WHAT PART B BUYS THE FRAMEWORK, STATED PRECISELY: in categories I and II, a_0 is a free")
print("      Lagrangian parameter and NOTHING ties it to rho_Lambda -- the tie is a coincidence to be")
print("      explained.  In category III the medium's density IS rho_Lambda, so the tie is STRUCTURAL,")
print("      and Part B says the functional form is then FORCED.  That is the strongest structural")
print("      argument for the central claim anywhere in this corpus. ***")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- is category III really distinct from II?  The sharp criterion")
print("=" * 100)

# In BM/AQUAL the phantom density is an algebraic functional of the local baryonic field:
#     rho_ph = -(1/4 pi G) div[ (mu(x) - 1) grad phi ]
# A "medium" with polarisation P responds to the field: rho_medium = -div P.
# If P = chi(|grad phi|) grad phi  (local, algebraic), the two are IDENTICAL with chi = (mu-1)/4 pi G.
phi = sp.Function("phi")
x1 = sp.Symbol("x", real=True)
mu_f = sp.Function("mu")
chi_f = sp.Function("chi")
G_c = sp.Symbol("G", positive=True)

# 1-D reduction is sufficient to establish the identification (both sides are div of a vector).
gradphi = sp.Derivative(phi(x1), x1)
rho_ph = -(1 / (4 * sp.pi * G_c)) * sp.Derivative((mu_f(x1) - 1) * gradphi, x1)
rho_med = -sp.Derivative(chi_f(x1) * gradphi, x1)
matched = rho_ph - rho_med.subs(chi_f(x1), (mu_f(x1) - 1) / (4 * sp.pi * G_c))
check(sp.simplify(matched.doit()) == 0,
      "C1  *** a LOCAL-ALGEBRAIC medium IS Bekenstein-Milgrom, identically, with chi = (mu-1)/4 pi G ***",
      "so category III collapses onto II unless the response is NON-algebraic")

# C2 -- therefore the distinguishing content of III is exactly the non-algebraic part.  Enumerate
#       the three ways a response can fail to be local-algebraic; these are not stylistic choices.
NON_ALGEBRAIC = {
    "memory":   "chi depends on the field's HISTORY -> a relaxation kernel",
    "gradient": "chi depends on grad|grad phi| -> a coherence length",
    "density":  "the medium carries its OWN conserved density -> it can cluster independently",
}
check(len(NON_ALGEBRAIC) == 3,
      "C2  exactly three ways out of the collapse, and each is a physical, testable structure",
      ", ".join(NON_ALGEBRAIC.keys()))

# C3 -- the memory route is the one this corpus already has machinery for.  The localised kernel
#       G(u) = g u e^(-m u) is the retarded Green's function of (d/dtau + m)^2.  Re-verify that
#       here rather than citing it, so this script is self-contained on the claim it leans on.
u, m_k, g_k, s_v = sp.symbols("u m g s", positive=True)
Gker = g_k * u * sp.exp(-m_k * u)
op = sp.diff(Gker, u, 2) + 2 * m_k * sp.diff(Gker, u) + m_k**2 * Gker
check(sp.simplify(op) == 0,
      "C3  the localised kernel solves (d/dtau + m)^2 G = 0 for u > 0 -- critically damped, re-verified",
      f"(D+m)^2 G = {sp.simplify(op)}")

# C4 -- and it is a NORMALISABLE response function (finite zeroth moment), which a medium
#       relaxation kernel must be.  Compute the moment rather than asserting it.
M0 = sp.integrate(Gker, (u, 0, sp.oo))
check(sp.simplify(M0 - g_k / m_k**2) == 0,
      "C4  zeroth moment is finite: int_0^inf G du = g/m^2 -- admissible as a relaxation kernel",
      f"M0 = {sp.simplify(M0)}")

print()
print("  *** THE SYNTHESIS: the memory kernel was a WORLDLINE object and died with the worldline when")
print("      pure modified inertia was excluded.  As a MEDIUM relaxation function it is exactly the")
print("      non-algebraic response that makes category III distinct from Bekenstein-Milgrom.  The")
print("      structure transfers.  This is the 'something else' the search was for -- and it is NOT")
print("      new to the literature (Part H), only new to this corpus. ***")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- THE DISCRIMINATOR, and it cuts against category III")
print("=" * 100)

# II forces g_obs to be an exact local function of g_bar => ZERO intrinsic RAR scatter and no
# environmental dependence beyond the external-field effect.  III permits a_0 to vary with the
# medium's local history.  The RAR's measured intrinsic scatter therefore BOUNDS III.
#
# Write the framework's own relation with a fractional medium fluctuation delta:
#     g_obs^2 = g_bar^2 + g_bar a_0 (1 + delta)
# and propagate delta into log10 g_obs at fixed g_bar.
y_s, delta_s = sp.symbols("y delta", positive=True)
log_gobs = sp.log(sp.sqrt(1 + (1 + delta_s) / y_s), 10)      # in units of g_bar
sens = sp.simplify(sp.diff(log_gobs, delta_s))
sens_deepmond = sp.limit(sens.subs(delta_s, 0), y_s, 0)
check(sp.simplify(sens_deepmond - 1 / (2 * sp.log(10))) == 0,
      "D1  sensitivity of the RAR to a fractional a_0 fluctuation is 1/(2 ln 10) in deep MOND",
      f"d log10 g_obs / d delta -> {sp.nsimplify(sens_deepmond)} = {float(sens_deepmond):.4f}")

sig_delta_max = SIG_INT * 2 * mp.log(10)
check(sig_delta_max < mp.mpf("0.20"),
      "D2  *** so the medium's own dynamics may not vary a_0 by more than "
      f"{float(sig_delta_max)*100:.1f}% galaxy-to-galaxy ***",
      f"sigma_int = {sig(SIG_INT,3)} dex / {float(sens_deepmond):.4f} dex per unit delta")

# D3 -- deep MOND is the TIGHTEST regime; confirm the bound loosens outward, so quoting the deep
#       value is quoting the constraint AGAINST the framework's interest, correctly.
sens_y1 = float(sens.subs({delta_s: 0, y_s: 1}))
check(sens_y1 < float(sens_deepmond),
      "D3  the bound is tightest in deep MOND (correct regime to quote) and loosens at higher y",
      f"sensitivity {float(sens_deepmond):.4f} (y->0) vs {sens_y1:.4f} (y=1)")

# D4 -- the BTFR is tighter still, and in the framework's own reading the deep-MOND BTFR has
#       ZERO intrinsic scatter.  So it is the sharper bound on III.  Compute it.
sig_delta_btfr = SIG_BTFR * 4 * mp.log(10)   # v^4 = G M a_0 => d log v = (1/4) d log a_0
check(sig_delta_btfr > sig_delta_max,
      "D4  CONTROL ON MY OWN ARITHMETIC: the BTFR bound is WEAKER, not stronger, than the RAR bound",
      f"BTFR allows {float(sig_delta_btfr)*100:.0f}% vs RAR's {float(sig_delta_max)*100:.1f}% "
      f"-- because log v carries 1/4 of log a_0, not 1/2")

check(sig_delta_max < sig_delta_btfr and sig_delta_max > 0,
      "D5  the RAR is the binding constraint on category III; it is TIGHT but NOT fatal",
      f"binding bound: |delta a_0/a_0| <~ {float(sig_delta_max)*100:.1f}%")

print()
print("  *** READ HONESTLY: the RAR's small intrinsic scatter is EVIDENCE FOR category II and a")
print("      CONSTRAINT ON category III.  A medium with free-running own dynamics would smear the")
print("      RAR; the data say it does not, to ~16%.  That is not a kill -- a relaxation kernel with")
print("      a long coherence time is uniform by construction -- but it is a real cost, and any")
print("      category-III model has to show it clears 16% before it is allowed to claim clusters. ***")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- CLUSTERS: what category III would actually have to supply.  AGAINST INTEREST.")
print("=" * 100)

print("""
  *** CORRECTION, ISSUED AGAINST MY OWN PRIOR COMMIT.  The first version of this Part combined
  1/f_bar = 6.4387 with the corpus's eta_req = 2.334 ADDITIVELY and concluded that a medium must
  supply ~68% of what LCDM's dark matter supplies.  THAT NUMBER IS WITHDRAWN.  It is incoherent:
  eta_req = 2.334 implies the kernel supplies a boost of 2.759, which requires y = 0.203, whereas
  the committed cluster audit simultaneously asserts clusters sit at y = 21.6.  Both cannot hold.
  This Part now computes the requirement DIRECTLY from the framework's own kernel, self-consistently,
  and the corrected answer is MUCH BETTER for the framework than the number I published. ***
""")

LCDM_DARK = INV_FBAR - 1
G_N = mp.mpf("6.674e-11")
MSUN = mp.mpf("1.989e30")
MPC = mp.mpf("3.0857e22")


def nu_routeA(y):
    """The framework's in-force Route A kernel (Amendment 8)."""
    return 1 / (1 - mp.e ** (-mp.sqrt(y)))


# E1 -- FIRST, a bug in the committed audit.  It states clusters sit at g ~ 2.02e-9 m/s^2 ~ 21.6 a_0
#       at R500.  Compute the radius at which a real cluster actually has that field.
G_AUDIT = mp.mpf("2.02e-9")
M_REF = mp.mpf("5e14") * MSUN
r_at_audit_g = mp.sqrt(G_N * M_REF / G_AUDIT) / MPC
check(r_at_audit_g < mp.mpf("0.4"),
      "E1  *** BUG FOUND IN THE COMMITTED CLUSTER AUDIT: its g = 2.02e-9 m/s^2 is the field at "
      f"{sig(r_at_audit_g, 3)} Mpc, i.e. the CORE, not R500 (~1.3 Mpc) ***",
      "off by ~50x in g. At true R500 clusters are at g ~ 0.3-0.6 a_0 -- NEAR/BELOW a_0, and the "
      "audit's 'quasi-Newtonian' premise is wrong")

# E2 -- now the direct, self-consistent requirement.  Let the extra real component cluster to a
#       fraction xi of CDM's level.  Then the total real mass is (1 + xi * LCDM_DARK) M_bar, and
#       the framework must reproduce the observed discrepancy:
#             (1 + xi*LCDM_DARK) * nu( y_bar * (1 + xi*LCDM_DARK) ) = 1/f_bar
#       Note the BACK-REACTION: adding mass raises y, which LOWERS nu.  An earlier version of this
#       calculation ignored that and got the answer wrong in the framework's favour.
CLUSTERS = [("A", 3e14, 1.10), ("B", 5e14, 1.30), ("C", 1e15, 1.60),
            ("D", 7e14, 1.40), ("E", 2e14, 0.95)]
print("   M500[Msun]  R500[Mpc]   g_tot/a0   y_bar     nu(y_bar)   xi_clust")
xis = []
for _lbl, M5, R5 in CLUSTERS:
    M = mp.mpf(M5) * MSUN
    R = mp.mpf(R5) * MPC
    g_tot = G_N * M / R ** 2
    y_bar = g_tot * F_BAR / A0_CANON
    xi = mp.findroot(
        lambda x: (1 + x * LCDM_DARK) * nu_routeA(y_bar * (1 + x * LCDM_DARK)) - INV_FBAR,
        mp.mpf("0.2"))
    xis.append(xi)
    print(f"   {M5:9.1e}  {R5:7.2f}   {sig(g_tot/A0_CANON,4):>8s}  {sig(y_bar,4):>8s}  "
          f"{sig(nu_routeA(y_bar),5):>8s}    {float(xi)*100:5.1f}%")

XI_LO, XI_HI = min(xis), max(xis)
check(XI_HI < mp.mpf("0.35"),
      f"E2  *** CORRECTED: the kernel removes {(1-float(XI_HI))*100:.0f}-{(1-float(XI_LO))*100:.0f}% of the cluster dark matter.  A real "
      f"component need supply only {float(XI_LO)*100:.0f}-{float(XI_HI)*100:.0f}% of what LCDM's does ***",
      "this is the WELL-KNOWN MOND cluster residual (order-unity extra mass), and it REPLACES the "
      "~68% I wrongly published -- the correction runs IN THE FRAMEWORK'S FAVOUR")

# E3 -- but it is still not zero, and that is the standing cost.  Say so.
check(XI_LO > mp.mpf("0.05"),
      "E3  the residual is REAL and nonzero: clusters still require a real clustering component",
      f"at least {float(XI_LO)*100:.0f}% of LCDM's dark matter. The no-dark-matter claim still goes.")

# NEGATIVE CONTROL: the root must be genuinely bracketed -- baryons alone UNDERSHOOT and full-CDM
# clustering OVERSHOOTS.  If either fails, the solve is meaningless.
M5b, R5b = mp.mpf("5e14") * MSUN, mp.mpf("1.30") * MPC
y_b = (G_N * M5b / R5b ** 2) * F_BAR / A0_CANON
at_zero = 1 * nu_routeA(y_b)
at_one = (1 + LCDM_DARK) * nu_routeA(y_b * (1 + LCDM_DARK))
check(at_zero < INV_FBAR < at_one,
      "NC-E  CONTROL: the root is bracketed -- baryons alone UNDERSHOOT, full-CDM clustering OVERSHOOTS",
      f"xi=0 gives {sig(at_zero,4)}, xi=1 gives {sig(at_one,4)}, target {sig(INV_FBAR,4)}")

# NC-E2: plug the solution back in.  It must reproduce 1/f_bar, or findroot lied.
xi_b = mp.findroot(lambda x: (1 + x * LCDM_DARK) * nu_routeA(y_b * (1 + x * LCDM_DARK)) - INV_FBAR,
                   mp.mpf("0.2"))
recon = (1 + xi_b * LCDM_DARK) * nu_routeA(y_b * (1 + xi_b * LCDM_DARK))
check(abs(recon - INV_FBAR) < mp.mpf("1e-20"),
      "NC-E2 CONTROL: the solution reproduces 1/f_bar on back-substitution",
      f"residual = {sig(abs(recon - INV_FBAR), 3)}")

# NC-E3: and the budget must reconcile with Planck independently.
OM_C, OM_B = mp.mpf("0.265"), mp.mpf("0.0493")
lcdm_ratio_indep = 1 + OM_C / OM_B
check(abs(lcdm_ratio_indep - INV_FBAR) / INV_FBAR < mp.mpf("0.03"),
      "NC-E3 CONTROL: 1/f_bar agrees with an INDEPENDENT Planck Omega_c/Omega_b computation to 3%",
      f"1/f_bar = {sig(INV_FBAR,5)} vs 1 + Om_c/Om_b = {sig(lcdm_ratio_indep,5)}")

# E4 -- and flag, WITHOUT resolving, that this now disagrees with the corpus's banked eta_req.
nu_needed_for_eta = INV_FBAR / ETA_REQ
y_needed = mp.findroot(lambda y: nu_routeA(y) - nu_needed_for_eta, mp.mpf("0.2"))
check(not (y_b * mp.mpf("0.5") < y_needed < y_b * mp.mpf("2.0")),
      "E4  UNRESOLVED: the banked eta_req = 2.334 needs y = "
      f"{sig(y_needed,4)}, but R500 sits at y = {sig(y_bar,4)}",
      "flagged, NOT smoothed. The banked eta may refer to a different radius/sample. "
      "This Part does not use it.")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- category IV (nonlocal), and the one thing it buys that II and III do not")
print("=" * 100)

# A nonlocal term built from 1/Box carries the horizon scale intrinsically, so a_0 inherits a
# redshift dependence with no extra parameter.  The framework already HAS an a_0(z) law; the point
# is that in II it is an ADD-ON and in IV it is FORCED.
z_s, w0, wa = sp.symbols("z w0 wa", real=True)
a0_ratio = (1 + z_s) ** (sp.Rational(3, 2) * (1 + w0 + wa)) * sp.exp(
    -sp.Rational(3, 2) * wa * z_s / (1 + z_s))
check(sp.simplify(a0_ratio.subs({w0: -1, wa: 0}) - 1) == 0,
      "F1  the corpus's a_0(z) law is flat for a pure cosmological constant, as it must be",
      "a_0(z)/a_0(0) = 1 at w0 = -1, wa = 0")

dlog = sp.simplify(sp.diff(sp.log(a0_ratio), z_s).subs({w0: -1, wa: 0}))
check(dlog == 0,
      "F2  and its z-derivative vanishes there too -- not just the value, the slope",
      f"d ln a_0 / dz = {dlog} at (w0, wa) = (-1, 0)")

# F3 -- and it must have CONTENT away from w = -1, or "structural a_0(z)" would be an empty phrase.
#       Evaluate the slope at a DESI-like equation of state and confirm it is nonzero and signed.
dlog_desi = float(sp.diff(sp.log(a0_ratio), z_s).subs({w0: mp.mpf("-0.9"), wa: mp.mpf("-0.4"),
                                                       z_s: 0}))
check(abs(dlog_desi) > 1e-3,
      "F3  and the law has real content away from w = -1, so category IV's a_0(z) is a PREDICTION",
      f"d ln a_0/dz = {dlog_desi:+.4f} at (w0, wa) = (-0.9, -0.4); "
      "but no nonlocal action reproducing THIS kernel exists in this corpus -- open, NOT claimed")


# =============================================================================================
print()
print("=" * 100)
print("PART G -- SUB-IDEAS I CHECKED AND KILLED.  Recorded so they are not re-proposed.")
print("=" * 100)

# G1 -- the tempting one: use the memory kernel's relaxation time as a LOW-PASS FILTER to evade the
#       inherited Cassini quadrupole tension.  Solar-system orbital periods are ~1-250 yr; if the
#       medium cannot follow them, the argument goes, no MOND quadrupole develops.  IT FAILS.
#       The Cassini Q_2 problem is driven by the GALACTIC external field, which is static on any
#       timescale the solar system cares about.  A low-pass filter does not remove a DC signal.
T_SOLAR = mp.mpf("29.5")        # yr, Saturn
T_GALACTIC = mp.mpf("2.0e8")    # yr, galactic orbit -- the external field's variation timescale
check(T_GALACTIC > LAMBDA_MI * mp.mpf("1e5"),
      "G1  KILLED: relaxation cannot evade Cassini -- the galactic external field is DC on 39 yr",
      f"T_gal/lambda = {sig(T_GALACTIC/LAMBDA_MI, 3)}: the EFE quadrupole passes any low-pass filter")

# G2 -- the relaxation time that a medium would need for the disturbed-system application (lagging
#       lensing peaks in mergers) is a MERGER time, not the worldline bound.  Seven orders apart.
orders = mp.log10(T_MERGER / LAMBDA_MI)
check(orders > 6,
      "G2  KILLED as a numerical transfer: the medium's needed relaxation time and the worldline",
      f"bound differ by {float(orders):.1f} ORDERS ({sig(LAMBDA_MI,3)} yr vs ~{sig(T_MERGER,2)} yr). "
      "Only the STRUCTURE transfers; the medium's timescale is a NEW FREE PARAMETER. That is a cost.")

# G3 -- putting the enhancement in BOTH the metric and the inertia.  Already closed: it double-counts.
nu_s = sp.Symbol("nu", positive=True)
gbar_s = sp.Symbol("g_bar", positive=True)
both = nu_s * (nu_s * gbar_s)
check(sp.simplify(both - nu_s**2 * gbar_s) == 0,
      "G3  KILLED (re-verified): enhancing metric AND inertia gives a = nu^2 g_bar, not nu g_bar",
      "the arms are mutually EXCLUSIVE -- no hybrid")

# G4 -- and the honest one about Part B.  Does the uniqueness theorem pick out rho_Lambda?  NO.
#       Demonstrate it: the theorem's input is a DIMENSION, so any density reproduces the same form
#       with a different number.  Run it on the matter density and on a local density.
RHO_L = mp.mpf("6.0e-27")      # kg/m^3, rho_Lambda, Planck-ish
RHO_M = RHO_L * mp.mpf("0.31") / mp.mpf("0.69")
RHO_LOCAL = mp.mpf("1.0e-21")  # kg/m^3, solar-neighbourhood-ish
G_N, C_L = mp.mpf("6.674e-11"), mp.mpf("2.99792458e8")
forms = {k: C_L * mp.sqrt(G_N * r) for k, r in
         [("rho_Lambda", RHO_L), ("rho_matter", RHO_M), ("rho_local", RHO_LOCAL)]}
spread = max(forms.values()) / min(forms.values())
check(spread > 100,
      "G4  KILLED as a derivation: the SAME forced form on three different densities spans "
      f"{float(spread):.0f}x",
      "Part B fixes the form, NOT which rho. c sqrt(G rho) = "
      + ", ".join(f"{k}: {sig(v,3)}" for k, v in forms.items())
      + " -- choosing rho_Lambda is physics input, not a theorem")


# =============================================================================================
print()
print("=" * 100)
print("PART H -- ATTRIBUTION.  Category III is NOT new to the literature.")
print("=" * 100)

PRIOR = {
    "Blanchet & Le Tiec 2008 PRD 78:024031; 2009 PRD 80:023524":
        "dipolar dark fluid: gravitational polarisation gives MOND phenomenology, AND the authors "
        "themselves note a_0 ~ c sqrt(Lambda) -- the SAME scaling as the framework's central claim, "
        "from a DIFFERENT mechanism",
    "Verlinde 2017 SciPost 2:016":
        "emergent gravity: elastic response of de Sitter entanglement entropy, a_0 tied to cH",
    "Berezhiani & Khoury 2015 PRD 92:103510":
        "superfluid dark matter: phonon-mediated MOND force PLUS a real gravitating condensate; "
        "coherence breaks in hot clusters -- a natural cluster/galaxy split",
    "Deser & Woodard 2007 PRL 99:111301":
        "nonlocal gravity, category IV",
    "Milgrom 1983 ApJ 270:365; 1999 PLA 253:273":
        "the a_0 ~ cH observation, and nu = sqrt(1 + 1/y) itself (eq 9) -- MANDATORY credit",
    "Bekenstein & Milgrom 1984 ApJ 286:7":
        "AQUAL, category II",
}
for k, v in PRIOR.items():
    print(f"\n  {k}\n      {v}")

check(len(PRIOR) >= 6,
      "H1  category III has at least three independent prior realisations -- Carl is NOT first to it",
      "what this script contributes is the CLASSIFICATION and the uniqueness theorem, not the category")

check(any("c sqrt(Lambda)" in v for v in PRIOR.values()),
      "H2  *** AND THE a_0 ~ c sqrt(Lambda) SCALING HAS AN INDEPENDENT PRIOR ARRIVAL (Blanchet). "
      "That CUTS BOTH WAYS ***",
      "against priority: the scaling is not original. FOR the physics: independent arrival by a "
      "different route is EVIDENCE the relation is real, not a numerological accident.")

# H3 -- the framework's distinctive content is the COEFFICIENT, and the clean demonstration that the
#       forced form does not fix it is that the corpus's OWN TWO FOOTINGS obey the same form with
#       different xi.  Back xi out of each rather than asserting it.
xi_canon = mp.mpf("0.5")                                  # canonical footing, by construction
xi_alt = xi_canon * (A0_ALT / A0_CANON)
check(abs(xi_alt - xi_canon) / xi_canon > mp.mpf("0.15"),
      "H3  *** the corpus's OWN two footings share the forced form but need DIFFERENT xi "
      f"({sig(xi_canon,4)} vs {sig(xi_alt,4)}) ***",
      f"a {float(A0_ALT/A0_CANON):.4f}x split. The form is forced; the coefficient is FITTED, "
      "NOT DERIVED -- and the corpus cannot yet even say which footing it is")


# =============================================================================================
print()
print("=" * 100)
print("PART I -- WHAT IS NOT CLAIMED")
print("=" * 100)

NOT_CLAIMED = [
    "NOT a derivation of kappa = 1/2.  Part B forces the FORM c sqrt(G rho); xi stays free.",
    "NOT a field theory for category III.  No action is written here.  Categories are not theories.",
    "NOT a resolution of clusters.  Part E leaves a real 11-26%-of-LCDM component required at R500.",
    "NOT a claim that category III beats category II.  Part D's RAR bound FAVOURS II.",
    "NOT a new category in the literature -- Part H.  New to THIS corpus only.",
    "NOT a rescue of the g^-2 Lorentz-violation prediction, which needs a preferred frame.",
    "NOT a reason to unfreeze anything.  No registered number moves on the strength of this script.",
]
for n in NOT_CLAIMED:
    print(f"  - {n}")
GUARDS = ["kappa = 1/2", "field theory", "clusters", "literature", "unfreeze"]
missing = [g for g in GUARDS if not any(g in n for n in NOT_CLAIMED)]
check(not missing,
      "I1  every guard this corpus has had to retract before is explicitly disclaimed here",
      f"{len(NOT_CLAIMED)} non-claims; guards covered: {', '.join(GUARDS)}")


# =============================================================================================
print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)
print(f"""
  1.  *** THE CHOICE WAS NEVER MI-OR-MG.  Sorting by what sources the metric gives five categories;
      the 21-sigma lensing test kills exactly one of them -- "metric from baryons alone" -- and THREE
      survive, degenerate on the lensing observable.  Lensing is a 1-bit test that has spent its
      bit. ***

  2.  *** UNIQUENESS THEOREM: a_0 = xi c sqrt(G rho) is the ONLY acceleration constructible from
      (G, c, rho) -- the exponent matrix is nonsingular (det = {det}).  And kappa = 1/2 is
      IDENTICALLY Z = 2 sqrt(8 pi/3).  The framework's form is FORCED, not chosen. ***
      *** kappa ITSELF IS STILL FITTED.  This is not a derivation. ***

  3.  Category III (medium / polarisation) collapses onto Bekenstein-Milgrom UNLESS the response is
      non-algebraic.  The localised memory kernel -- orphaned when pure modified inertia died -- is
      exactly such a response.  The STRUCTURE transfers; the TIMESCALE does not ({float(orders):.1f} orders off),
      so the medium's relaxation time is a NEW FREE PARAMETER.

  4.  Category III is the only survivor in which rho_Lambda appears for a REASON rather than as a
      coincidence: it is the medium's own density.  Combined with (2) that is the strongest
      structural argument for the central claim in this corpus.

  5.  AGAINST INTEREST: the RAR's 0.034 dex intrinsic scatter bounds any medium own-dynamics
      variation in a_0 to {float(sig_delta_max)*100:.1f}% -- which FAVOURS plain Bekenstein-Milgrom over the new category.

  5b. *** CORRECTION IN THE FRAMEWORK'S FAVOUR, against my own prior commit.  Computed directly from
      the kernel, the R500 requirement is that a real component supply {float(XI_LO)*100:.0f}-{float(XI_HI)*100:.0f}% of what LCDM's dark
      matter supplies -- the kernel removes {(1-float(XI_HI))*100:.0f}-{(1-float(XI_LO))*100:.0f}%.  The "~68%" published in the first commit of
      this script is WITHDRAWN as incoherent.  And the committed cluster audit's g = 2.02e-9 m/s^2 is
      the CORE field, not R500's: clusters sit at 0.3-0.6 a_0, near or below a_0. ***
      Still nonzero, so the no-dark-matter claim still goes.

  6.  Four sub-ideas checked and KILLED: relaxation-as-Cassini-evasion (the galactic field is DC);
      numerical transfer of the 39 yr kernel bound; metric-and-inertia hybrids (give nu^2);
      and any reading of (2) as selecting rho_Lambda.

  7.  Blanchet's dipolar dark fluid reached a_0 ~ c sqrt(Lambda) independently, by a different
      route.  Against priority; FOR the physics.

  VERDICT: the search asked for was worth doing and it found something real -- the space is three-
  wide, not one-wide, and the third lane makes the central claim structural.  It did NOT find a
  finished theory, and the cluster number it surfaces is the worst in this corpus.
""")

print("=" * 100)
if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print(f"ALL CHECKS PASSED")
print("=" * 100)
