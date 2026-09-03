#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k_unexplained-regularities_closure.py

THE CLOSURE TEST FOR THE 'UNEXPLAINED REGULARITIES' ANGLE.

Two candidates computed this session -- the Bosma factor (k_unexplained-regularities_bosma.py) and the HI
size-mass corollary (k_unexplained-regularities_hisize.py) -- both turned out to be restatements, and both proofs
looked the SAME: the extra measured quantity cancelled out of the framework-vs-data ratio, leaving the RAR
residual reparametrised.  Nine earlier hunt items died the same way.  This script asks whether that is a
coincidence or a THEOREM, and it draws the boundary of the class.

THE CLAIM UNDER TEST (the closure theorem):

    Let a candidate regularity be a statistic X = F(g_bar, g_obs; Z) evaluated at ONE radius, where Z is any
    collection of other measured quantities (a gas surface density, a luminosity, a radius, a size, an HI mass).
    Compare the framework's value X_fw = F(g_bar, nu(y) g_bar; Z) with the measured X_obs = F(g_bar, g_obs; Z).
    If Z enters F multiplicatively -- which it does for every 'dark-to-something' ratio ever proposed -- then Z
    CANCELS from log(X_fw/X_obs), and the candidate's residual is a deterministic function of the RAR residual
    and y alone.  It is therefore a RESTATEMENT, carrying no information the RAR does not already carry.

THE TEST, and it CAN FAIL.  For every candidate, SHUFFLE the extra measured inputs Z across galaxies at random
and recompute the residual.  If the residual is unchanged to machine precision, Z genuinely cancelled and the
candidate is inside the closure -- a restatement.  If the residual moves, the candidate carries information the
RAR does not, and it is a live second-law candidate.  Two deliberate ESCAPE candidates are included to prove the
test is not vacuous: a two-radius statistic and a non-multiplicative one.  Both must MOVE.

WHY THIS IS WORTH A SCRIPT.  The hunt's own summary says criterion (5) -- 'it is not a restatement' -- is what
killed several apparent wins.  This makes criterion (5) mechanical: any proposed regularity can be run through
the shuffle in a minute, before anyone spends a day on it.  And the escapes tell you where to look: the only
places a non-restatement can live are MORE THAN ONE RADIUS, NON-MULTIPLICATIVE COMBINATIONS, and QUANTITIES THE
RAR DOES NOT CONTAIN AT ALL (environment, redshift, gas structure).  The third was tested this session by
k_unexplained-regularities_hisize.py Q1 and FAILED: a_0 does not set the HI surface density.

RULES: both footings; the shuffle is the mutation control and is seeded; the Newtonian/LambdaCDM alternative is
stated; the Upsilon lever is measured by re-running at Upsilon x 1.5; report against interest.
"""
import os, sys, math
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, G, KMS2_KPC, Msun, nu, load_sparc, read_master, Check, P, UPS_D, UPS_B

MSUN_PC2 = Msun / (3.0857e16) ** 2
HE = 1.33
SEED = 20260903

ck = Check()
P("=" * 118)
P("k_unexplained-regularities_closure -- is 'it is a restatement of the RAR' a coincidence or a theorem?")
P("=" * 118)

master = read_master()


# ---------------------------------------------------------------------------------------------------------------
def build(ups_d=UPS_D, ups_b=UPS_B):
    """One row per galaxy: dynamics at an OUTER radius, plus the extras Z, plus an INNER radius for the escapes."""
    gals = load_sparc(ups_d=ups_d, ups_b=ups_b)
    rows = []
    for g in gals:
        if len(g["r"]) < 8:
            continue
        io, ii = len(g["r"]) - 1, len(g["r"]) // 3        # outer point and an inner point
        m = master[g["name"]]
        vgas2 = g["vg"] * np.abs(g["vg"])
        gHI = vgas2 / g["r"] * KMS2_KPC / HE               # hydrogen-only acceleration
        gstar = (ups_d * g["vd"] ** 2 + ups_b * g["vb"] ** 2) / g["r"] * KMS2_KPC
        if gHI[io] <= 0 or gstar[io] <= 0 or g["gbar"][io] <= 0 or g["gobs"][io] <= 0:
            continue
        if g["gbar"][ii] <= 0 or g["gobs"][ii] <= 0:
            continue
        rows.append(dict(
            name=g["name"],
            gbar=float(g["gbar"][io]), gobs=float(g["gobs"][io]),
            Z=dict(gHI=float(gHI[io]), gstar=float(gstar[io]), r=float(g["r"][io]),
                   L36=float(m["L36"]), MHI=float(m["MHI"]), RHI=float(m["RHI"]), Dist=float(m["D"]),
                   SigHI=float(m["MHI"] * 1e9 / (math.pi * (max(m["RHI"], 1e-6) * 1e3) ** 2)),
                   gbar_in=float(g["gbar"][ii]), gobs_in=float(g["gobs"][ii]))))
    return rows


# --------------------------------------------------------------- the candidate statistics, X = F(gbar, gobs; Z)
# Every one of these has been proposed, somewhere, as an 'unexplained regularity' of galaxy dynamics.
# Signature F(gb, go, Z, go_in): go is the OUTER observed-or-predicted acceleration, go_in the INNER one.
# Single-radius candidates ignore go_in; the two-radius escape uses it, and that is exactly what makes it escape.
#
# BUG FOUND BY THIS SCRIPT'S OWN VACUITY CHECK (C2), and fixed here: the first version of escape K carried the
# inner radius inside Z, so the SAME inner value entered the framework and the measured branch and cancelled --
# the "escape" was a multiplicative constant and did not move.  A control that cannot move is not a control.
CANDIDATES = {
    "A  Bosma factor  (v_dark^2/v_HI^2)":              lambda gb, go, Z, gi: (go - gb) / Z["gHI"],
    "B  mass discrepancy  (g_obs/g_bar)":              lambda gb, go, Z, gi: go / gb,
    "C  dark matter fraction  (1 - g_bar/g_obs)":      lambda gb, go, Z, gi: 1.0 - gb / go,
    "D  dark-to-luminous speed ratio":                 lambda gb, go, Z, gi: math.sqrt(max(go - gb, 1e-300) / gb),
    "E  phantom surface density  ((g_o-g_b)/2piG)":    lambda gb, go, Z, gi: (go - gb) / (2 * math.pi * G),
    "F  Bosma factor on the STARS instead of the HI":  lambda gb, go, Z, gi: (go - gb) / Z["gstar"],
    "G  phantom enclosed mass  ((g_o-g_b) r^2/G)":     lambda gb, go, Z, gi: (go - gb) * Z["r"] ** 2 / G,
    "H  dynamical-to-HI surface density":              lambda gb, go, Z, gi: go / (2 * math.pi * G * Z["SigHI"] * MSUN_PC2),
    "I  dark mass per unit HI mass":                   lambda gb, go, Z, gi: (go - gb) * Z["r"] ** 2 / (G * Z["MHI"]),
    "J  V_flat^4 / (G M_b a_0)  [the BTFR itself]":    lambda gb, go, Z, gi: (go * Z["r"]) ** 2 / (G * Z["L36"] + 1e-300),
    # ---- deliberate ESCAPES: these MUST move under the shuffle, or the test is vacuous
    "K  ESCAPE: outer/inner discrepancy (2 radii)":    lambda gb, go, Z, gi: (go / gb) / (gi / Z["gbar_in"]),
    "L  ESCAPE: non-multiplicative  (g_o-g_b)/(g_o+g_HI)": lambda gb, go, Z, gi: (go - gb) / (go + Z["gHI"]),
}


def residuals(rows, a0, F, Zsource=None):
    """log10(X_framework / X_measured) per galaxy.  Zsource lets the extras come from a DIFFERENT galaxy."""
    out = []
    for i, r in enumerate(rows):
        Z = r["Z"] if Zsource is None else rows[Zsource[i]]["Z"]
        gb, go = r["gbar"], r["gobs"]
        gfw = float(nu(gb / a0)) * gb
        gi_obs = Z["gobs_in"]
        gi_fw = float(nu(Z["gbar_in"] / a0)) * Z["gbar_in"]   # the framework must predict the INNER radius too
        try:
            xo, xf = F(gb, go, Z, gi_obs), F(gb, gfw, Z, gi_fw)
        except Exception:
            out.append(np.nan); continue
        out.append(math.log10(xf / xo) if (xo > 0 and xf > 0) else np.nan)
    return np.array(out, dtype=float)


rows = build()
P(f"\n  {len(rows)} SPARC discs with >= 8 radii, an outer point and an inner point, positive gas and stars.\n")
rng = np.random.default_rng(SEED)
perm = rng.permutation(len(rows))
# guarantee the shuffle actually moves every galaxy's extras (a derangement), else the control is weak
for i in range(len(perm)):
    if perm[i] == i:
        j = (i + 1) % len(perm); perm[i], perm[j] = perm[j], perm[i]
P(f"  shuffle: a seeded derangement of the extras Z across galaxies (seed {SEED}); "
  f"{int((perm != np.arange(len(rows))).sum())}/{len(rows)} galaxies get someone else's Z.\n")

P("-" * 118)
P("THE CLOSURE TEST.  max |residual - residual with the extras shuffled|, per candidate, per footing.")
P("  ~0  => the extras CANCEL => the candidate is the RAR reparametrised => RESTATEMENT.")
P("  >0  => the candidate carries information beyond the RAR => LIVE.")
P("-" * 118)
P(f"  {'candidate':52s} {'canonical':>14s} {'alt':>14s}   verdict")
closed, live = [], []
for label, F in CANDIDATES.items():
    mx = {}
    for foot, a0 in A0.items():
        r0 = residuals(rows, a0, F)
        r1 = residuals(rows, a0, F, Zsource=perm)
        ok = np.isfinite(r0) & np.isfinite(r1)
        mx[foot] = float(np.nanmax(np.abs(r0[ok] - r1[ok]))) if ok.sum() else np.nan
    isclosed = max(mx.values()) < 1e-10
    (closed if isclosed else live).append(label)
    P(f"  {label:52s} {mx['canonical']:14.3e} {mx['alt']:14.3e}   "
      f"{'RESTATEMENT' if isclosed else 'LIVE (escapes the closure)'}")

ck("C1 THE THEOREM.  Every single-radius statistic in which the extra measured inputs enter multiplicatively "
   "must be shown to be the RAR reparametrised -- the shuffle must not move it at all.  A PASS here is a "
   "NEGATIVE result for the hunt: it means this whole class of candidate cannot contain a second law",
   all(c in closed for c in list(CANDIDATES)[:10]),
   f"{len(closed)} of {len(CANDIDATES)} candidates are inside the closure: "
   f"{[c.split()[0] for c in closed]}")
ck("C2 THE TEST MUST NOT BE VACUOUS.  The two deliberate escapes -- a two-radius statistic and a "
   "non-multiplicative one -- must MOVE under the same shuffle, or the test detects nothing",
   all(c in live for c in list(CANDIDATES)[10:]),
   f"escapes that moved: {[c.split()[0] for c in live]}")

P("\n" + "-" * 118)
P("HOW FAR the escapes move, so that 'it moved' is a number and not a word")
P("-" * 118)
for label in list(CANDIDATES)[10:]:
    F = CANDIDATES[label]
    r0 = residuals(rows, A0["canonical"], F)
    r1 = residuals(rows, A0["canonical"], F, Zsource=perm)
    ok = np.isfinite(r0) & np.isfinite(r1)
    P(f"  {label:52s} rms shift {float(np.sqrt(np.mean((r0[ok]-r1[ok])**2))):.4f} dex, "
      f"max {float(np.max(np.abs(r0[ok]-r1[ok]))):.4f} dex")

# ---------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("THE UPSILON LEVER on the closure itself")
P("-" * 118)
rows15 = build(1.5 * UPS_D, 1.5 * UPS_B)
perm15 = np.roll(np.arange(len(rows15)), 1)
worst = 0.0
for label, F in list(CANDIDATES.items())[:10]:
    for foot, a0 in A0.items():
        r0 = residuals(rows15, a0, F); r1 = residuals(rows15, a0, F, Zsource=perm15)
        ok = np.isfinite(r0) & np.isfinite(r1)
        if ok.sum():
            worst = max(worst, float(np.nanmax(np.abs(r0[ok] - r1[ok]))))
P(f"  at Upsilon x 1.5 the worst closure violation among the ten closed candidates is {worst:.3e} dex.")
P(f"  d [closure violation] / d log Upsilon = 0 EXACTLY: the closure is an algebraic identity, not a fit, so it")
P(f"  is the one quantity in this hunt with a strictly zero mass-to-light lever.  What Upsilon DOES move is the")
P(f"  VALUE of every residual inside the closure -- which is precisely why nine items measured Upsilon and")
P(f"  reported a_0.")
ck("UPS the closure must survive a 1.5x change in the stellar mass-to-light ratio with a strictly zero lever, "
   "since it is an identity", worst < 1e-10, f"worst violation {worst:.3e} dex at Upsilon x 1.5")

# ---------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("THE NEWTONIAN / LambdaCDM ALTERNATIVE")
P("-" * 118)
P("""  There is no LambdaCDM analogue of this theorem, and that is the honest asymmetry to record.  LambdaCDM does
  not predict g_obs from g_bar by a single function, so its 'dark-to-something' ratios are NOT reparametrisations
  of one relation -- each carries independent halo information.  The closure is a property of ONE-FUNCTION
  gravity laws, this framework and MOND alike.  It is therefore a statement about what the framework CAN say,
  not evidence for it.  Against interest: the same theorem says the framework's supply of independent galactic
  predictions is far smaller than the number of galactic 'successes' the ledger lists, because most of those
  successes are the same success.""")

P("\n" + "=" * 118)
P("VERDICT -- and it is a negative one")
P("=" * 118)
P(f"""  {len(closed)} of {len(CANDIDATES)} candidate regularities are PROVED restatements by shuffle, to machine precision, on both
  footings.  They include the Bosma factor, the mass discrepancy, the dark-matter fraction, the phantom surface
  density, the phantom enclosed mass, the dark-mass-per-HI-mass ratio and the BTFR itself.  Every 'dark-to-
  something' ratio anyone has proposed is the RAR wearing different clothes, and no amount of searching inside
  that class can produce a second law.

  THE BOUNDARY, which is the useful output.  A non-restatement must use at least one of:
    (i)   more than one radius       -- where hunt item 115 already lives (Renzo's rule at second order,
                                        beta = 0.944 +- 0.135 against a predicted 1.000), and it survived;
    (ii)  a non-multiplicative combination of dynamics and something else;
    (iii) a quantity the RAR does not contain at all -- environment, redshift, or gas structure.
  Route (iii) was tested this session on the tightest such quantity available, the HI surface density that sets
  the HI size-mass relation, and a_0 does not set it (k_unexplained-regularities_hisize.py Q1).

  This does not weaken the first law.  It bounds where a second one could be, and it says the 'unexplained
  regularities' angle -- mining the literature's list of surprising galactic coincidences -- is exhausted,
  because that list is almost entirely inside the closure.""")
sys.exit(ck.done())
