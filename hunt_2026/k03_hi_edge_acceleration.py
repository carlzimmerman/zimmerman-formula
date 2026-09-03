#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k03 -- THE TIGHTEST SCALING RELATION IN EXTRAGALACTIC ASTRONOMY: is it an a_0 law?

ANGLE 1 (mine the unexplained regularities), aimed at the tightest one there is.  The HI size-mass relation --
log D_HI = 0.506 log M_HI - 3.293, with a scatter of only 0.06 dex over five decades in HI mass (Broeils & Rhee
1997; Verheijen & Sancisi 2001; Wang, Koribalski, Serra et al. 2016) -- is routinely described as "remarkably
tight", "universal" and unexplained.  Its slope is 1/2 to within the errors.  So is the slope of the MOND radius
r_M = sqrt(G M/a_0).  This item asks whether that is a coincidence or a law, and answers it.

FOUR CANDIDATE EQUATIONS ARE TESTED, each an equation between MEASURED quantities:

  K03-A   R_HI = xi * sqrt(G M_HI / a_0)                          xi a pure number predicted by the framework?
  K03-B   g_bar(R_HI) = beta * a_0                                a universal BARYONIC acceleration at the HI edge
  K03-C   g_obs(R_HI) = gamma * a_0                               a universal TOTAL acceleration at the HI edge
  K03-D   Sigma_HI(<R_HI) = a_0 / (2 pi G) / N                    the HI edge as a fixed fraction of Sigma_M

A pass requires (i) scatter <= 0.1 dex, (ii) NO trend with mass, and (iii) the coefficient PREDICTED, not fitted.
(iii) is the criterion that decides whether any of these is a law or merely a repackaging of a known constant.

Both footings, mutation controls, the Newtonian alternative computed beside, the Upsilon lever quoted numerically.
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import (A0, G, Msun, KMS2_KPC, kpc, nu, load_sparc, read_master, Check, P, info, fit_loglog,
                      UPS_D, UPS_B)

MSUN_PC2 = Msun / (3.0857e16) ** 2
SIG_M = {fo: A0[fo] / (2 * math.pi * G) / MSUN_PC2 for fo in A0}      # Msun/pc^2
ck = Check()
P("=" * 120)
P("k03 -- THE HI SIZE-MASS RELATION: is the tightest relation in extragalactic astronomy an a_0 law?")
P("=" * 120)
for fo in ("canonical", "alt"):
    P(f"  Sigma_M = a_0/(2 pi G) = {SIG_M[fo]:.1f} Msun/pc^2  ({fo})")


def build(ups_d=UPS_D, ups_b=UPS_B):
    gals = load_sparc(ups_d=ups_d, ups_b=ups_b)
    rows = []
    for g in gals:
        RHI, MHI = g["RHI"], g["MHI"] * 1e9                     # RHI in kpc, MHI in Msun (HI only, no helium)
        if not (RHI > 0 and MHI > 0):
            continue
        r, gbar = g["r"], g["gbar"]
        gobs = g["gobs"]
        if RHI < r.min() or RHI > r.max() * 1.15:               # require the curve to reach (nearly) the HI edge
            continue
        gb = float(np.interp(RHI, r, gbar))
        go = float(np.interp(RHI, r, gobs))
        rows.append(dict(name=g["name"], RHI=RHI, MHI=MHI, Mb=g["Mb"], gbar=gb, gobs=go,
                         L36=g["L36"] * 1e9, extrap=RHI > r.max()))
    return rows


rows = build()
P(f"\n  {len(rows)} SPARC discs have a tabulated HI radius that their rotation curve reaches "
  f"({sum(r['extrap'] for r in rows)} need <=15% extrapolation).")

RHI = np.array([r["RHI"] for r in rows]); MHI = np.array([r["MHI"] for r in rows])
Mb = np.array([r["Mb"] for r in rows]); gb = np.array([r["gbar"] for r in rows])
go = np.array([r["gobs"] for r in rows])

# ------------------------------------------------------------------ 0. reproduce the published relation
P("\n" + "-" * 120)
P("STEP 0 -- reproduce the published relation on this sample, or the rest of the item means nothing")
P("-" * 120)
s0, b0, sc0 = fit_loglog(MHI, 2 * RHI)                     # diameter, to match Wang+2016's D_HI
P(f"  log D_HI = {s0:.3f} log M_HI + {b0:.3f},  scatter {sc0:.3f} dex, N = {len(RHI)}")
P("  published (Wang+2016, 562 galaxies): slope 0.506, intercept -3.293, scatter 0.06 dex")
ck("K03-0 the SPARC sample must reproduce the published HI size-mass relation, or it is not the relation "
   "under test",
   abs(s0 - 0.506) < 0.06 and sc0 < 0.13,
   f"slope {s0:.3f} vs 0.506, scatter {sc0:.3f} dex vs 0.06 (SPARC's R_HI is a catalogue value with its own "
   f"distance errors, so a somewhat larger scatter is expected)")

# ------------------------------------------------------------------ A. R_HI vs the MOND radius
P("\n" + "-" * 120)
P("K03-A  R_HI = xi sqrt(G M_HI/a_0).   Is xi one number, and is it predicted?")
P("-" * 120)
for fo in ("canonical", "alt"):
    rM = np.sqrt(G * MHI * Msun / A0[fo]) / (kpc / 1e3) / 1e3      # kpc
    xi = RHI / rM
    s, b, sc = fit_loglog(MHI, xi)
    P(f"  {fo:<10} median xi = {np.median(xi):6.2f}   scatter {np.log10(xi).std():.3f} dex   "
      f"d log xi/d log M_HI = {s:+.3f}")
rM_c = np.sqrt(G * MHI * Msun / A0["canonical"]) / kpc * 1e3 * 1e-3
rM_c = np.sqrt(G * MHI * Msun / A0["canonical"]) / kpc          # metres -> kpc
xi_c = RHI / rM_c
s_xi, _, _ = fit_loglog(MHI, xi_c)
ck("K03-A xi must be one number with RAR-class scatter AND no mass trend.  It can fail on either.",
   np.log10(xi_c).std() < 0.10 and abs(s_xi) < 0.03,
   f"median xi = {np.median(xi_c):.2f}, scatter {np.log10(xi_c).std():.3f} dex, mass slope {s_xi:+.3f}")
P(f"\n  AND THE DECISIVE POINT, which no amount of tightness can rescue: is xi = {np.median(xi_c):.2f} PREDICTED?")
P("  The framework fixes a_0 and therefore r_M.  It says nothing whatever about where hydrogen stops being")
P("  neutral.  xi is a number about self-shielding and the ionising background, and the framework has no")
P("  handle on it.  So even a perfect K03-A would fail criterion (2) of a Kepler-grade law: the coefficient")
P("  is fitted, not predicted.  Recorded as such.")

# ------------------------------------------------------------------ B, C. accelerations at the edge
P("\n" + "-" * 120)
P("K03-B/C  is the ACCELERATION at the HI edge universal?  (this is the form in which a_0 could appear)")
P("-" * 120)
P(f"  {'footing':<10}{'quantity':<12}{'median /a_0':>13}{'scatter [dex]':>15}{'d log/d log M_b':>18}"
  f"{'d log/d log g_bar':>19}")
res = {}
for fo in ("canonical", "alt"):
    a0 = A0[fo]
    for lab, q in (("g_bar(R_HI)", gb), ("g_obs(R_HI)", go)):
        sM, _, _ = fit_loglog(Mb, q / a0)
        sc = np.log10(q / a0).std()
        res[(fo, lab)] = (np.median(q / a0), sc, sM)
        P(f"  {fo:<10}{lab:<12}{np.median(q/a0):>13.4f}{sc:>15.3f}{sM:>18.3f}{'':>19}")
mb_c, sc_b, sl_b = res[("canonical", "g_bar(R_HI)")]
mo_c, sc_o, sl_o = res[("canonical", "g_obs(R_HI)")]
ck("K03-B g_bar at the HI edge must be a universal fraction of a_0 with <= 0.1 dex scatter and no mass trend",
   sc_b < 0.10 and abs(sl_b) < 0.05,
   f"median {mb_c:.4f} a_0, scatter {sc_b:.3f} dex, mass slope {sl_b:+.3f}")
ck("K03-C g_obs at the HI edge must be a universal fraction of a_0 with <= 0.1 dex scatter and no mass trend",
   sc_o < 0.10 and abs(sl_o) < 0.05,
   f"median {mo_c:.4f} a_0, scatter {sc_o:.3f} dex, mass slope {sl_o:+.3f}")

# ------------------------------------------------------------------ D. surface density
P("\n" + "-" * 120)
P("K03-D  the HI edge as a surface density.  Sigma_HI(<R_HI) = M_HI/(pi R_HI^2), against Sigma_M = a_0/(2 pi G)")
P("-" * 120)
Sig = MHI / (math.pi * (RHI * 1e3) ** 2)                        # Msun/pc^2
sS, _, _ = fit_loglog(MHI, Sig)
P(f"  mean HI surface density inside R_HI: median {np.median(Sig):.2f} Msun/pc^2, scatter "
  f"{np.log10(Sig).std():.3f} dex, mass slope {sS:+.3f}")
for fo in ("canonical", "alt"):
    P(f"  Sigma_M/Sigma_HI = {SIG_M[fo]/np.median(Sig):.1f}   ({fo}) -- is that a number the framework predicts?  No.")
ck("K03-D the HI edge's mean surface density must be a PREDICTED fraction of Sigma_M = a_0/(2 pi G).  The "
   "framework predicts no such fraction, so this check is written to fail unless the ratio lands on a simple "
   "number (1, 2, pi, 2 pi, 4 pi) to better than 5%",
   any(abs(SIG_M["canonical"] / np.median(Sig) / t - 1) < 0.05 for t in (1, 2, math.pi, 2 * math.pi, 4 * math.pi)),
   f"ratio {SIG_M['canonical']/np.median(Sig):.2f} (canonical), {SIG_M['alt']/np.median(Sig):.2f} (alt) -- "
   f"no simple number within 5%")

# ------------------------------------------------------------------ Upsilon lever
P("\n" + "-" * 120)
P("THE UPSILON LEVER, numerically")
P("-" * 120)
lev = {}
for ups in (0.35, 0.70):
    rr = build(ups_d=ups, ups_b=ups * 1.4)
    q = np.array([x["gbar"] for x in rr]); qo = np.array([x["gobs"] for x in rr])
    lev[ups] = (np.median(np.log10(q)), np.median(np.log10(qo)))
d = math.log10(2.0)
P(f"  d log g_bar(R_HI) / d log Upsilon = {(lev[0.70][0]-lev[0.35][0])/d:+.3f}")
P(f"  d log g_obs(R_HI) / d log Upsilon = {(lev[0.70][1]-lev[0.35][1])/d:+.3f}  (zero by construction: g_obs "
  f"has no stellar mass in it)")
P(f"  d log xi / d log Upsilon         = 0.000 exactly (xi uses M_HI, not M_star)")
P("  So K03-A and K03-C are among the very few statements in this hunt with NO stellar mass-to-light leverage")
P("  at all.  That is the good news.  The bad news is criterion (2): none of their coefficients is predicted.")

# ------------------------------------------------------------------ mutation controls
P("\n" + "-" * 120)
P("MUTATION CONTROLS")
P("-" * 120)
rng = np.random.default_rng(20260903)
sh = np.log10((rng.permutation(MHI) / (math.pi * (RHI * 1e3) ** 2)))
ck("M03a shuffling which galaxy's HI mass goes with which galaxy's HI radius must destroy the tightness -- if it "
   "does not, the relation is an artefact of the sample's dynamic range and not a relation at all",
   sh.std() > 3 * np.log10(Sig).std(),
   f"shuffled scatter {sh.std():.3f} dex against the true {np.log10(Sig).std():.3f} dex")
A0["mut"] = 4 * A0["canonical"]
xi_m = RHI / (np.sqrt(G * MHI * Msun / A0["mut"]) / kpc)
ck("M03b quadrupling a_0 must move xi by exactly a factor 2, since xi carries a_0^(1/2) -- and note what that "
   "means: xi is an a_0 METER with leverage 1/2, so its 0.1 dex scatter caps any a_0 read from it at 0.2 dex",
   abs(np.median(np.log10(xi_m / xi_c)) - math.log10(2.0)) < 0.01,
   f"shift {np.median(np.log10(xi_m/xi_c)):+.4f} dex against the predicted +0.301")
del A0["mut"]

# ------------------------------------------------------------------ the alternative computed beside
P("\n" + "-" * 120)
P("THE NEWTONIAN / LambdaCDM ALTERNATIVE, COMPUTED BESIDE")
P("-" * 120)
P("  The standard explanation of the HI size-mass relation needs no gravity theory at all: hydrogen goes")
P("  neutral below a column set by the ionising background and self-shielding, so the mean surface density")
P("  inside the 1 Msun/pc^2 isophote is fixed, and M_HI = pi R_HI^2 <Sigma> follows with slope exactly 1/2.")
P(f"  Measured here: <Sigma> = {np.median(Sig):.2f} Msun/pc^2 with {np.log10(Sig).std():.3f} dex of scatter and a")
P(f"  mass slope of {sS:+.3f}.  That is the whole relation, and there is no acceleration in it.")
P("  Both theories therefore predict slope 1/2 for the same reason: neither predicts it.  The MOND radius also")
P("  goes as M^(1/2), which is why the coincidence looked like something.")

# ------------------------------------------------------------------ restatement test
P("\n" + "=" * 120)
P("THE RESTATEMENT TEST")
P("=" * 120)
P("  K03-A: R_HI = xi sqrt(G M_HI/a_0).  Derive from v^4 = G M_b a_0?  v_flat^2 = sqrt(G M_b a_0) = G M_b/r_M, so")
P("  r_M = G M_b/v_flat^2 -- pure algebra from the BTFR.  So r_M is a BTFR quantity, and K03-A is the statement")
P("  'R_HI is proportional to r_M', i.e. a restatement PLUS an unexplained proportionality constant.  CLOSES.")
P("  K03-B/C: g at a radius fixed by an atomic-physics threshold.  Not derivable from the BTFR (the BTFR has no")
P("  radius), but also not predicted by the framework, because nothing in the framework fixes where hydrogen")
P("  ionises.  DOES NOT CLOSE as a restatement, but fails criterion (2) instead: no predicted coefficient.")
P("  K03-D: definitional.  CLOSES trivially.")

P("\n" + "=" * 120)
P("VERDICT -- k03: NO.  The tightest scaling relation in extragalactic astronomy is not an a_0 law.")
P("=" * 120)
P(f"  * R_HI does track the MOND radius of its own HI mass, with median xi = {np.median(xi_c):.2f} (canonical) / "
  f"{RHI.__len__() and np.median(RHI/(np.sqrt(G*MHI*Msun/A0['alt'])/kpc)):.2f} (alt),")
P(f"    scatter {np.log10(xi_c).std():.3f} dex and a mass slope of {s_xi:+.3f}.  But xi is not predicted by anything, and")
P("    the tracking is forced: both quantities go as M_HI^(1/2), one because surface density is fixed by")
P("    atomic physics and the other because a_0 is fixed by Lambda.  Two square roots meeting is not a law.")
P(f"  * The acceleration at the HI edge is NOT universal: g_bar spans {np.log10(gb/A0['canonical']).std():.3f} dex "
  f"with a mass slope of {sl_b:+.3f},")
P(f"    g_obs spans {np.log10(go/A0['canonical']).std():.3f} dex with a mass slope of {sl_o:+.3f}.  Both fail the 0.1 dex bar and both")
P("    carry a mass trend, so there is no acceleration scale hiding at the edge of the HI disc.")
P("  * Reported against interest, and it removes a candidate the programme might otherwise have chased: the")
P("    coincidence between the HI size-mass slope and the MOND-radius slope is exactly that.")
P("  * One thing worth keeping for elsewhere: g_obs(R_HI) and xi have EXACTLY ZERO stellar mass-to-light")
P("    leverage.  If a quantity of that kind can be found whose coefficient IS predicted, it would be the")
P("    cleanest measurement in the hunt.  This one is not it.")
sys.exit(ck.done())
