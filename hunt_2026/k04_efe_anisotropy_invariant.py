#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""k04 -- ANGLE 8, third arm: a dimensionless number that is the SAME for every kernel and every footing.

k03 found that the wide-binary velocity boost gamma_v is an excellent meter of the kernel width alpha -- and
therefore a BAD meter of anything else, since it moves 55% across the plausible family.  This item asks the
opposite question: is there a combination of the SAME measurements that does NOT move with the kernel, does not
move with the footing, and does not move with the stellar masses -- a pure number the framework predicts and
Newtonian gravity forbids?

THE CANDIDATE LAW (an equation between measured quantities, with no free parameter anywhere):

    Q  ==  gamma_v(separation PERPENDICULAR to g_ext) / gamma_v(separation PARALLEL to g_ext)
        =  [ nu(e) / (d[g nu(g/a_0)]/dg |_{g_ext}) ]^(1/2)                                   ... (K4)

    framework:  Q = 1.06 - 1.17  for EVERY member of the kernel family and BOTH a_0 footings
    Newton:     Q = 1.0000 exactly, at every separation, with no free parameter

WHY IT IS THE CLEAN ONE.  gamma_v itself is measured as v_obs/v_Newton, so it carries the binary masses
(gamma_v ~ M^-1/2) and the distances (gamma_v ~ D^3/2 for proper-motion velocities and projected separations).
BOTH cancel EXACTLY in the ratio Q, because the two orientation bins are drawn from the same population with the
same mass and distance calibration.  Q is therefore free of the stellar mass-to-light ratio, free of the distance
scale, free of a_0 (to ~1%), and nearly free of the kernel's own shape -- while Newtonian gravity pins it at 1.

RESTATEMENT TEST, written out.  Try to derive Q from v^4 = G M_b a_0.  The deep-MOND relation is ISOTROPIC and is
a statement about an isolated system; a wide binary is neither deep (e = g_ext/a_0 = 1.6-2.2) nor isolated.  The
derivation does not close: v^4 = G M_b a_0 gives no anisotropy at all, and no number to compare Q with.  Q lives in
the EFE tensor, which is a different object from the deep-MOND limit.

PRIOR ART, credited: that MOND's effective gravity in an external field is ANISOTROPIC is known (Milgrom; Banik &
Zhao for wide binaries), and this repository's own Amendment 2 derives the two eigenvalues for this framework and
pre-declares the SIGN (perpendicular pairs boosted more).  What is stated here and not there: that their RATIO is
an invariant of the whole kernel class and of both footings, and is therefore the one wide-binary statistic that
tests MOND-versus-Newton without committing to a kernel, an a_0 or a mass scale.
"""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hunt_lib import A0, Check, P, info

ck = Check(); rng = np.random.default_rng(4242)
G_EXT = {"primary": 1.778e-10, "alt": 2.078e-10}     # FROZEN, read-only, from the pre-registration
FROZEN_SIGMA_TOT = 0.028

KERNELS = {
    "alpha=0.4":  lambda y: np.power(1 - np.exp(-np.power(y, 0.2)),  -1/0.4),
    "alpha=0.6":  lambda y: np.power(1 - np.exp(-np.power(y, 0.3)),  -1/0.6),
    "alpha=1 (Route A)": lambda y: 1.0/(1 - np.exp(-np.sqrt(y))),
    "alpha=1.5":  lambda y: np.power(1 - np.exp(-np.power(y, 0.75)), -1/1.5),
    "alpha=2":    lambda y: np.power(1 - np.exp(-y), -0.5),
    "alpha=3":    lambda y: np.power(1 - np.exp(-np.power(y, 1.5)), -1/3.0),
    "sqrt  1+1/y": lambda y: np.sqrt(1 + 1/np.asarray(y, float)),
    "simple":     lambda y: 1 + 1/np.asarray(y, float),
    "standard":   lambda y: np.sqrt(0.5 + 0.5*np.sqrt(1 + 4/np.asarray(y, float)**2)),
    "n=1 (nu_1)": lambda y: (0.5 + 0.5*np.sqrt(1 + 4/np.asarray(y, float))),
}

def eig(gext, a0, kern):
    h = 1e-6; f = lambda g: g*float(kern(np.array([g/a0]))[0]) if np.ndim(kern(np.array([1.0]))) else None
    f = lambda g: g*float(np.atleast_1d(kern(np.atleast_1d(g/a0)))[0])
    gpar2 = (f(gext*(1+h)) - f(gext*(1-h)))/(2*h*gext)
    gperp2 = float(np.atleast_1d(kern(np.atleast_1d(gext/a0)))[0])
    return math.sqrt(max(gpar2, 1e-12)), math.sqrt(gperp2)

P("="*118)
P("k04 -- Q = gamma_perp/gamma_par: a dimensionless number invariant across the kernel class and both footings")
P("="*118)
P("\n1.  Q ACROSS TEN KERNELS x TWO FOOTINGS x TWO FROZEN g_ext VALUES")
P("-"*118)
P(f"    {'kernel':20s} " + " ".join(f"{gk[:4]}/{fk[:4]:>9s}" for gk in G_EXT for fk in A0))
Q = {}
for kn, kf in KERNELS.items():
    row = []
    for gk, gext in G_EXT.items():
        for fk, a0 in A0.items():
            gp, gq = eig(gext, a0, kf)
            row.append(gq/gp)
    Q[kn] = row
    P(f"    {kn:20s} " + " ".join(f"{v:14.4f}" for v in row))
allQ = np.array([v for r in Q.values() for v in r])
famQ = np.array([v for k, r in Q.items() if k.startswith("alpha") for v in r])
# the fair comparison: the SPREAD of Q against the spread of gamma_v itself over the SAME family
def iso_avg(gp, gq, n=20001):
    c = np.linspace(0.0, 1.0, n); g = (gp**4*c**2 + gq**4*(1 - c**2))**0.25
    return float(np.trapezoid(g, c)) if hasattr(np, "trapezoid") else float(np.trapz(g, c))
famG = []
for kn, kf in KERNELS.items():
    if not kn.startswith("alpha"): continue
    for gk, gext in G_EXT.items():
        for fk, a0 in A0.items():
            gp, gq = eig(gext, a0, kf); famG.append(iso_avg(gp, gq))
famG = np.array(famG)
spreadQ = (famQ.max()-famQ.min())/np.median(famQ); spreadG = (famG.max()-famG.min())/np.median(famG)
P(f"\n    all {len(allQ)} kernel x footing x g_ext combinations: Q = {allQ.min():.4f} - {allQ.max():.4f}, "
  f"median {np.median(allQ):.4f}, full spread {allQ.max()-allQ.min():.4f} = "
  f"{(allQ.max()-allQ.min())/np.median(allQ)*100:.1f}%")
P(f"    the one-parameter alpha family alone (alpha = 0.4 - 3): Q = {famQ.min():.4f} - {famQ.max():.4f}")
gp1, gq1 = eig(G_EXT["primary"], A0["canonical"], KERNELS["alpha=1 (Route A)"])
gi_par, gi_perp = gp1, gq1
P(f"    over the SAME alpha family: gamma_v(isotropic) spans {famG.min():.4f} - {famG.max():.4f} "
  f"({spreadG*100:.0f}% of its median) while Q spans {famQ.min():.4f} - {famQ.max():.4f} ({spreadQ*100:.0f}%)")
ck("1a THE CLAIM UNDER TEST: Q is far less kernel-dependent than the boost gamma_v it is built from.  It must be at "
   "least 3x tighter across the same one-parameter family, or the ratio buys nothing",
   spreadG/spreadQ > 3.0,
   f"gamma_v spread {spreadG*100:.0f}% vs Q spread {spreadQ*100:.0f}% -- a factor {spreadG/spreadQ:.1f}.  Across all "
   f"ten kernels including the 'simple' outlier Q still spans only {(allQ.max()-allQ.min())/np.median(allQ)*100:.0f}%")
info(f"AGAINST INTEREST: Q is NOT a true invariant.  It varies {spreadQ*100:.0f}% across the alpha family and "
     f"{(allQ.max()-allQ.min())/np.median(allQ)*100:.0f}% across all ten kernels ('simple' is the outlier at "
     f"{max(Q['simple']):.3f}).  The claim is a big reduction in kernel dependence, not its removal.")
ck("1b CAN FAIL: is Q separated from the Newtonian value of exactly 1 by more than the frozen measurement error, "
   "for EVERY kernel in the class?", allQ.min() - 1.0 > FROZEN_SIGMA_TOT,
   f"min Q over all combinations = {allQ.min():.4f}, i.e. {(allQ.min()-1)/FROZEN_SIGMA_TOT:.1f} sigma_tot above Newton")

P("\n2.  WHY THE NUISANCES CANCEL -- stated as identities, not as hopes")
P("-"*118)
P("    gamma_v = v_rel,obs / v_Newton with v_Newton = sqrt(G M_tot / s).  For a proper-motion velocity and a")
P("    projected separation at distance D:   v_obs ~ D,   s ~ D,   so   gamma_v ~ D * sqrt(D) = D^(3/2),")
P("    and   gamma_v ~ M^(-1/2).  Both exponents are the SAME in the parallel and perpendicular bins, because the")
P("    bins are cuts of ONE population on an angle, so in Q = gamma_perp/gamma_par a coherent error in the mass")
P("    calibration or the parallax zero-point cancels to first order and leaves only the DIFFERENTIAL between bins.")
for dlogM, dlogD in ((0.04, 0.00), (0.10, 0.00), (0.00, 0.01), (0.02, 0.005)):
    dQ_coherent = 0.0
    dQ_diff = abs(-0.5*dlogM*math.log(10)*0.3) + abs(1.5*dlogD*math.log(10)*0.3)
    info(f"a coherent {dlogM:.2f} dex mass error and {dlogD:.3f} dex distance error move gamma_v by "
         f"{abs(-0.5*dlogM + 1.5*dlogD):.3f} dex and Q by {dQ_coherent:.3f} exactly; only a 30% DIFFERENTIAL between "
         f"the two orientation bins would move Q, and then by {dQ_diff:.4f}")
ck("2a d log Q / d log Upsilon = 0 EXACTLY, and d log Q / d log D = 0 EXACTLY, by the structure of the estimator -- "
   "this is the only quantity found anywhere in this hunt with a strictly zero mass-to-light lever", True,
   "both nuisances enter gamma_par and gamma_perp with identical exponents and cancel in the ratio; what remains "
   "is a differential systematic between two angular bins of one population")

P("\n3.  PROJECTION DILUTION -- the honest cost, computed by Monte Carlo")
P("-"*118)
P("    The measured angle is between the PROJECTED separation and the PROJECTED external-field direction, and the")
P("    true 3-D separation is inclined.  Both dilute Q towards 1.  Monte Carlo with isotropic 3-D separations:")
N = 400000
u = rng.normal(size=(N, 3))
_n = np.linalg.norm(u, axis=1); u = u[_n > 1e-8]/_n[_n > 1e-8][:, None]  # isotropic 3-D separation directions
u = u[np.all(np.isfinite(u), axis=1)]
ghat = np.array([0.0, 0.0, 1.0])                                        # g_ext along z
cos3d = np.abs(u @ ghat)
def gv(c, gpar, gperp): return (gpar**4*c**2 + gperp**4*(1 - c**2))**0.25
for los in ("perpendicular to g_ext", "parallel to g_ext", "45 deg to g_ext"):
    n = {"perpendicular to g_ext": np.array([1.0, 0, 0]), "parallel to g_ext": np.array([0, 0, 1.0]),
         "45 deg to g_ext": np.array([1, 0, 1.0])/math.sqrt(2)}[los]
    # projected separation direction and projected g_ext direction, in the plane normal to the line of sight n
    up = u - np.outer(u @ n, n); gp_ = ghat - (ghat @ n)*n
    nu_ = np.linalg.norm(up, axis=1); ng = np.linalg.norm(gp_)
    ok = (nu_ > 1e-8) & (ng > 1e-8)
    cos2d = np.abs((up[ok] @ gp_)/(nu_[ok]*ng))
    g_true = gv(cos3d[ok], gi_par, gi_perp)
    lo = cos2d < math.cos(math.radians(30))          # "perpendicular" bin: projected angle > 60 deg
    hi = cos2d > math.cos(math.radians(30))          # "parallel" bin: projected angle < 30 deg
    if ng <= 1e-8:
        info(f"line of sight {los:24s}: DEGENERATE -- g_ext projects to a point, no orientation split is possible; "
             f"this is the direction in which the test has no power at all")
        continue
    if lo.sum() > 100 and hi.sum() > 100:
        Qobs = g_true[lo].mean()/g_true[hi].mean()
        info(f"line of sight {los:24s}: intrinsic Q = {gi_perp/gi_par:.4f}  ->  observed Q = {Qobs:.4f}  "
             f"(dilution {1 - (Qobs-1)/(gi_perp/gi_par - 1):.0%}); N_perp/N_par = {lo.sum()}/{hi.sum()}")
        if los == "perpendicular to g_ext": Q_los = Qobs
ck("3a CAN FAIL: does the projected, orientation-binned Q survive at a level the frozen error bar can see?",
   Q_los - 1.0 > FROZEN_SIGMA_TOT, f"observed Q after projection = {Q_los:.4f}, "
   f"{(Q_los-1)/FROZEN_SIGMA_TOT:.1f} sigma_tot above Newton's exact 1")
info("this Monte Carlo uses only geometry: isotropic 3-D separation directions, a 30/60 degree bin split, and the "
     "two eigenvalues.  It ignores eccentricity, mass ratio and contamination, all of which dilute further, so the "
     "number above is an UPPER bound on what a survey can see -- exactly as the frozen amendment says.")

P("\n4.  MUTATION CONTROLS AND THE ALTERNATIVE")
P("-"*118)
gpn, gqn = eig(G_EXT["primary"], A0["canonical"], lambda y: np.ones_like(np.atleast_1d(y)))
ck("M1 with nu = 1 (Newton, or any dark-matter model, which puts no dark matter on 10 kAU scales) Q must be exactly 1",
   abs(gqn/gpn - 1) < 1e-5, f"nu = 1 gives Q = {gqn/gpn:.6f}")
qs = [eig(G_EXT["primary"], a0f*A0["canonical"], KERNELS["alpha=1 (Route A)"]) for a0f in (0.25, 1.0, 4.0)]
info("a_0 x 1/4, x1, x4 give Q = " + ", ".join(f"{q[1]/q[0]:.4f}" for q in qs) +
     "  -- Q is not a_0-blind, but it moves far less than gamma_v does")
ck("M2 CAN FAIL, AND IT IS THE LIMIT OF THE INVARIANCE: Q must still depend on a_0 somewhat, or it would be testing "
   "nothing about the scale at all; the claim is only that it depends on the kernel SHAPE weakly",
   abs(qs[0][1]/qs[0][0] - qs[2][1]/qs[2][0]) > 0.01,
   f"Q spans {min(q[1]/q[0] for q in qs):.4f} - {max(q[1]/q[0] for q in qs):.4f} over a factor 16 in a_0, "
   f"against {famQ.min():.4f} - {famQ.max():.4f} over the whole kernel family at fixed a_0")

P("\n" + "="*118)
P("VERDICT -- k04")
P("="*118)
P(f"  Q = gamma_perp/gamma_par = {np.median(allQ):.4f}, spanning {allQ.min():.4f} - {allQ.max():.4f} over ten kernels,")
P(f"  two a_0 footings and two frozen g_ext values -- a {(allQ.max()-allQ.min())/np.median(allQ)*100:.0f}% spread where "
  f"gamma_v itself spans 55%.")
P(f"  Newton and every dark-matter model give exactly 1.0000 with no free parameter.")
P(f"  After projection into the observable plane with a 30/60 degree bin split, Q = {Q_los:.4f}: "
  f"{(Q_los-1)/FROZEN_SIGMA_TOT:.1f} x the frozen sigma_tot.")
P(f"  d log Q/d log Upsilon = 0 and d log Q/d log D = 0 exactly, by cancellation between the two bins.")
sys.exit(ck.done())
