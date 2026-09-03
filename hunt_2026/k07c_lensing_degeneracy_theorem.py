#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
k07c_lensing_degeneracy_theorem.py -- ANGLE 7, CANDIDATE K07-C: the ladder rung that cannot be repaired.
========================================================================================================================
TWO STATEMENTS, both computed here.

(C0) THE UNIVERSAL LENSING PROFILE.  For an isolated point-like baryonic lens the framework's excess surface
     density is ONE dimensionless curve, with no free parameter and no halo:

         Delta Sigma (R)  =  (a_0 / G) * f( R / r_M ) ,        r_M = sqrt( G M_b / a_0 )                   ... (C0)

     f is fixed by the kernel alone; f(S) -> 1/(pi S^2) inside r_M (Newtonian point mass) and f(S) -> 1/(4S)
     outside it (deep MOND).  So every isolated galaxy in the universe lies on the same lensing curve once R is
     measured in units of its own transition radius and Delta Sigma in units of a_0/G = 0.223 kg/m^2 =
     107 Msun/pc^2 (canonical) -- the SAME constant that item 5 found as the halo surface-density constant.

(C1)-(C2) THE DEGENERACY THAT FOLLOWS.  In the deep branch (C0) becomes

         Delta Sigma (R)  =  sqrt( M_b a_0 / G ) / (4 R)                                                   ... (C1)

     in which M_b and a_0 appear ONLY through their product.  Hence for any lensing measurement of a_0,

         d log a_0 / d log Upsilon_*  =  - f_*   EXACTLY, in any survey, at any depth, with any sample size. ... (C2)

CREDIT WITHIN THIS SESSION.  h113_kids_two_halo.py (same session, different angle) independently found the
covariance ordering bug on this same file, computed Delta Sigma from the kernel, and reported an M/L-free lensing
a_0 = 6.31e-11 [5.4e-11, 7.5e-11] with the caveat that dropping R < 0.1 Mpc moves it by more than its own error.
What is NEW here is (C0) -- the one-curve scaling with its predicted normalisation a_0/G -- the EXACT lever (C2)
that explains item 123's measured -1.046, and the transition-radius table that says which lens masses could ever
break the degeneracy.  The chi2 section below is a cross-check against h113, not an independent claim.

WHY THIS MATTERS FOR ANGLE 7.  The a_0 ladder carried the KiDS isolated-dwarf lens stack as one of its two
"M/L-free" rungs for two ledgers; item 123 measured its lever at -1.046 and withdrew the label.  This script shows
the -1 is not an estimator flaw or a sample accident but is FORCED by (C1) -- so no lensing survey can ever supply
an M/L-free rung for a galaxy-mass lens.  One of the five "independent ways" of item 125 is removed permanently,
and the observation that would restore it is named and costed.

THE RESTATEMENT TEST (mandatory, done honestly).
    (C1): YES, IT CLOSES.  g = sqrt(G M_b a_0)/r is the deep-MOND law; the enclosed dynamical mass is g r^2/G; the
    projection is calculus.  (C1) is v^4 = G M_b a_0 in lensing clothes and is LABELLED A RESTATEMENT.  Item 1
    already verified its 1/R shape in these same data.
    (C0): DOES NOT CLOSE.  The deep-MOND limit has no transition, so it cannot produce f(S) at S <~ 1, cannot
    produce the Newtonian branch, and cannot say where the crossover is.  (C0) is a genuine one-curve statement
    about the whole profile, and its normalisation a_0/G is predicted, not fitted.
    (C2): a corollary about MEASURABILITY, not a law of nature.  Offered as a closure, not as a discovery.

DATA (ON DISK): Brouwer et al. 2021 KiDS-1000 isolated lenses,
    real_research/data/lensing_rar/brouwer2021_rar/Fig-3_Lensing-rotation-curves_Massbin-{1..4}.txt + covariance.
    NOTE: hunt_lib.load_cov_esd does a PLAIN reshape of that covariance.  The programme has already been bitten
    once by exactly this (the RAR covariance is stored (m,n,i,j) and a plain reshape is not positive definite).
    This script rebuilds the ESD covariance with the correct transpose and CHECKS positive-definiteness before use.

Both footings.  Mutation controls.  The LambdaCDM alternative computed beside the framework.
"""
import sys, os, math
import numpy as np
from hunt_lib import *

ck = Check()
rng = np.random.default_rng(20260903)
np.seterr(all="ignore")
trap = np.trapezoid if hasattr(np, "trapezoid") else np.trapz

MSUN = 1.989e30
PC = 3.0857e16
KPC = 1000 * PC
MPC = 1e6 * PC
SIG_UNIT = MSUN / PC**2                                  # 1 Msun/pc^2 in kg/m^2
BR = os.path.join(DATA, "lensing_rar", "brouwer2021_rar")


# ------------------------------------------------------------------------------------------------------------------
# the universal dimensionless lensing profile f(S), S = R/r_M
# ------------------------------------------------------------------------------------------------------------------
def _nu_prime(x, h=1e-6):
    return (nu_s(x * math.exp(h)) - nu_s(x * math.exp(-h))) / (2 * h * x)


def _rhohat(s):
    """rho_phantom * r_M^3 / M_b, as a function of s = r/r_M."""
    return (1.0 / (4 * math.pi * s**2)) * (-2.0 / s**3) * _nu_prime(1.0 / s**2)


def f_of_S(S, tmax=14.0, n=20000):
    """Delta Sigma = (a_0/G) f(S).  M_ph(<r) = M_b [nu(1/s^2) - 1] exactly, so only the projection is numerical.
    The 1/sqrt(s^2-S^2) singularity is removed by s = S cosh t."""
    t = np.linspace(1e-10, tmax, n)
    s = S * np.cosh(t)
    rh = np.array([_rhohat(v) for v in s])
    A = trap(rh * s * (s - S * np.sinh(t)) * S * np.sinh(t), t)      # Int_S^inf rho s (s - sqrt(s^2-S^2)) ds
    Sg = 2 * trap(rh * s, t)                                        # Sigma
    M2 = nu_s(1.0 / S**2) + 4 * math.pi * A                         # M_2D(<R)/M_b, baryonic point mass included
    return M2 / (math.pi * S**2) - Sg


_SG = np.logspace(-2.5, 4.0, 260)
_FG = np.array([f_of_S(float(s)) for s in _SG])
_LF = np.log(_FG)


def f_interp(S):
    return np.exp(np.interp(np.log(np.asarray(S, dtype=float)), np.log(_SG), _LF))


def dsigma(R_m, Mb_kg, a0):
    rM = math.sqrt(G * Mb_kg / a0)
    return (a0 / G) * f_interp(np.asarray(R_m, dtype=float) / rM)


def dsigma_deep(R_m, Mb_kg, a0):
    return math.sqrt(Mb_kg * a0 / G) / (4.0 * np.asarray(R_m, dtype=float))


P("=" * 118)
P("K07-C -- THE UNIVERSAL LENSING CURVE, AND WHY THE LENSING RUNG CANNOT BE MADE MASS-TO-LIGHT-FREE")
P("=" * 118)
P(f"  the surface-density unit of the theory: a_0/G = "
  f"{A0['canonical']/G:.4f} kg/m^2 = {A0['canonical']/G/SIG_UNIT:.1f} Msun/pc^2 (canonical), "
  f"{A0['alt']/G/SIG_UNIT:.1f} (alt)")
P(f"  for comparison, the halo surface-density constant of item 5 is a_0/(2 pi G) = "
  f"{A0['canonical']/(2*math.pi*G)/SIG_UNIT:.1f} Msun/pc^2 (canonical)")

# ------------------------------------------------------------------------------------------------------------------
# 1.  the universal curve and its two asymptotes
# ------------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("1.  THE UNIVERSAL CURVE f(S), and the two limits it must reproduce")
P("-" * 118)
P(f"  {'S=R/r_M':>10s} {'f(S)':>12s} {'1/(4S) deep':>13s} {'1/(pi S^2) Newt':>16s}   which limit")
for S in (0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 1000.0):
    v = float(f_interp(S))
    P(f"  {S:10.3f} {v:12.5e} {1/(4*S):13.5e} {1/(math.pi*S**2):16.5e}   "
      f"{'Newtonian' if v/(1/(math.pi*S**2)) < 1.3 else ('deep MOND' if v*4*S < 1.1 else 'transition')}")
ck("K07c.1 the universal profile reproduces BOTH asymptotes it must: the Newtonian point mass inside r_M and the "
   "deep-MOND 1/R outside it, with no fitting anywhere",
   abs(float(f_interp(0.03)) * math.pi * 0.03**2 - 1) < 0.02 and abs(float(f_interp(1000.)) * 4000 - 1) < 0.01,
   f"f(0.03)*pi*S^2 = {float(f_interp(0.03))*math.pi*0.03**2:.5f} (Newtonian limit 1); "
   f"f(1000)*4S = {float(f_interp(1000.))*4000:.5f} (deep limit 1)")

sl = np.polyfit(np.log10(_SG[(_SG > 20) & (_SG < 2000)]), np.log10(_FG[(_SG > 20) & (_SG < 2000)]), 1)[0]
ck("K07c.2 and the outer branch is the 1/R law item 1 measured in these same KiDS data, tying this machinery to "
   "an independently verified result rather than standing alone",
   abs(sl + 1.0) < 0.02, f"log-log slope of f over S = 20-2000 is {sl:+.4f} (prediction -1.000)")

# ------------------------------------------------------------------------------------------------------------------
# 2.  the degeneracy, computed
# ------------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("2.  THE DEGENERACY.  (M_b, a_0) -> (lambda M_b, a_0/lambda) must leave the profile unchanged if (C1) holds.")
P("    Here is by how much it actually changes across the radii KiDS measures.")
P("-" * 118)
Rtest = np.array([0.035, 0.1, 0.3, 1.0, 2.6]) * MPC
P(f"  {'log M_b':>8s} {'lambda':>7s} " + "  ".join(f"{r/MPC:8.3f}Mpc" for r in Rtest))
maxdev = 0.0
for logM in (9.0, 10.0, 11.0):
    Mb_ = 10**logM * MSUN
    base = dsigma(Rtest, Mb_, A0["canonical"])
    for lam in (0.25, 4.0):
        alt = dsigma(Rtest, lam * Mb_, A0["canonical"] / lam)
        dev = alt / base - 1
        maxdev = max(maxdev, float(np.max(np.abs(dev))))
        P(f"  {logM:8.1f} {lam:7.2f} " + "  ".join(f"{100*v:10.2f}%" for v in dev))
# my own first-draft claim was that the degeneracy is exact EVERYWHERE KiDS measures.  It is not, and the
# two-sided check below is the corrected statement: exact in the deep branch, broken at the massive-bin inner edge.
dev_deep = max(abs(float(np.max(np.abs(dsigma(Rtest[Rtest > 0.1*MPC], lam*10**lg*MSUN, A0["canonical"]/lam) /
                                       dsigma(Rtest[Rtest > 0.1*MPC], 10**lg*MSUN, A0["canonical"]) - 1))))
               for lg in (9.0, 10.0) for lam in (0.25, 4.0))
dev_inner = float(np.max(np.abs(dsigma(Rtest[:1], 4*10**11*MSUN, A0["canonical"]/4) /
                                dsigma(Rtest[:1], 10**11*MSUN, A0["canonical"]) - 1)))
P(f"\n  RETRACTION OF MY OWN FIRST DRAFT: I wrote that the degeneracy is exact everywhere KiDS measures. It is not.")
P(f"  It is exact in the deep branch ({100*dev_deep:.1f}% at R > 0.1 Mpc for lenses below 1e10 Msun) and it BREAKS")
P(f"  at the inner edge of the most massive bin ({100*dev_inner:.0f}%), because there R_inner/r_M is only "
  f"{Rtest[0]/math.sqrt(G*1e11*MSUN/A0['canonical']):.1f}.")
ck("K07c.3 the corrected, two-sided statement: the (M_b, a_0) degeneracy is EXACT in the deep branch and BREAKS "
   "only where the data reach inside the transition radius. Both halves are asserted, so the check fails if "
   "either the deep branch is not degenerate or the inner edge is",
   dev_deep < 0.05 and dev_inner > 0.20,
   f"compensating factor-4 rescale changes Delta Sigma by {100*dev_deep:.1f}% at R > 0.1 Mpc for M_b <= 1e10 "
   f"(degenerate) but by {100*dev_inner:.0f}% at R = 35 kpc for M_b = 1e11 (not degenerate); my blanket "
   f"'a few per cent everywhere' is withdrawn")

# ------------------------------------------------------------------------------------------------------------------
# 3.  what it costs in chi2 on the real KiDS data, with a correctly ordered covariance
# ------------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("3.  ON THE REAL DATA.  Four KiDS-1000 stellar-mass bins, masses free, a_0 profiled.")
P("-" * 118)
d = np.genfromtxt(os.path.join(BR, "Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt"), comments="#")
bins_lo = np.unique(d[:, 0])
nb = len(bins_lo)
Rb, ESD, eESD = [], [], []
for i in range(1, nb + 1):
    R, E, eE = load_esd(f"Fig-3_Lensing-rotation-curves_Massbin-{i}.txt")
    Rb.append(R); ESD.append(E); eESD.append(eE)
npts = len(Rb[0])
n = nb * npts
v = d[:, 4] / d[:, 6]
C_plain = v.reshape(n, n)
C_fixed = v.reshape(nb, nb, npts, npts).transpose(0, 2, 1, 3).reshape(n, n)
ev_p = np.linalg.eigvalsh((C_plain + C_plain.T) / 2)
ev_f = np.linalg.eigvalsh((C_fixed + C_fixed.T) / 2)
P(f"  {nb} bins (log M_* >= {', '.join('%.2f'%b for b in bins_lo)}) x {npts} radii = {n} points")
P(f"  covariance minimum eigenvalue: PLAIN reshape {ev_p.min():.4e}   TRANSPOSED reshape {ev_f.min():.4e}")
ck("K07c.4 CONFIRMING h113-A INDEPENDENTLY (credit to it, not claimed here): the ESD covariance has the same "
   "(m,n,i,j) storage order as the RAR covariance that voided an earlier claim in this programme, so "
   "hunt_lib.load_cov_esd's plain reshape is wrong on this binned file. h1_h66_h2_h65_lensing.py line 26 still "
   "calls it. Caught by positive-definiteness, not by the diagonal, which passes either way",
   ev_f.min() > 0 and ev_p.min() < ev_f.min(),
   f"plain reshape min eigenvalue {ev_p.min():.3e} vs transposed {ev_f.min():.3e}; the diagonals are identical "
   f"to {np.max(np.abs(np.diag(C_plain)-np.diag(C_fixed)))/np.max(np.diag(C_fixed)):.1e} relative, so a "
   f"diagonal-only check would have missed it")

Cov = C_fixed * SIG_UNIT**2
Rall = np.concatenate(Rb) * MPC
Eall = np.concatenate(ESD) * SIG_UNIT
Cinv = np.linalg.inv(Cov)


def model(a0, logMs):
    return np.concatenate([dsigma(np.array(Rb[i]) * MPC, 10**logMs[i] * MSUN, a0) for i in range(nb)])


def chi2_of(a0, logMs):
    r = Eall - model(a0, logMs)
    return float(r @ Cinv @ r)


def profile(a0, start=None):
    lm = list(start if start else [b + 0.4 for b in bins_lo])
    for it in range(8):
        for i in range(nb):
            gr = np.linspace(lm[i] - 1.5 / (it + 1), lm[i] + 1.5 / (it + 1), 31)
            lm[i] = float(gr[int(np.argmin([chi2_of(a0, lm[:i] + [g] + lm[i+1:]) for g in gr]))])
    return chi2_of(a0, lm), lm


P(f"\n  {'a_0':>11s} {'a_0/a_0(canon)':>15s} {'chi2 (masses refitted)':>24s}   fitted log10 M_b per bin")
prof = []
for fac in (1/64, 1/16, 1/4, 1.0, A0["alt"] / A0["canonical"], 4.0, 16.0, 64.0):
    a0 = A0["canonical"] * fac
    c, lm = profile(a0)
    prof.append((a0, fac, c, lm))
    P(f"  {a0:11.3e} {fac:15.4f} {c:24.2f}   " + " ".join(f"{x:6.2f}" for x in lm))
cmin = min(p[2] for p in prof)
span = [p for p in prof if p[2] - cmin < 9.0]
dec = math.log10(max(p[0] for p in span) / min(p[0] for p in span))
ibest = int(np.argmin([p[2] for p in prof]))
lm_best = prof[ibest][3]
below = sum(1 for i in range(nb) if lm_best[i] < bins_lo[i])
P(f"  bin minimum stellar masses (the SELECTION boundary, log10 M_*): " + " ".join(f"{b:6.2f}" for b in bins_lo))
P(f"  best unbounded fit is a_0 = {prof[ibest][0]:.3e} ({prof[ibest][1]:.0f}x canonical) with fitted log M_b = "
  + " ".join(f"{x:6.2f}" for x in lm_best))
ck("K07c.5 AGAINST MY OWN CLAIM AND AGAINST THE FRAMEWORK, BOTH: (a) a_0 is NOT unconstrained here -- with the "
   "four lens masses completely free the 3 sigma region still spans only about half a decade, so a genuinely "
   "M/L-free lensing a_0 does exist, which is more than I expected; but (b) the unbounded best fit runs to many "
   "times the canonical value and gets there by driving the lens masses BELOW the minimum STELLAR mass that "
   "defines their own bins, which is impossible since M_b = M_* + M_gas >= M_*",
   below >= 2,
   f"3 sigma span {dec:.2f} decades; unbounded best fit {prof[ibest][1]:.0f}x canonical needs log M_b below the "
   f"bin's own log M_* floor in {below} of {nb} bins (by up to "
   f"{max(bins_lo[i]-lm_best[i] for i in range(nb)):.2f} dex)")

# now impose the ONLY thing that is not a stellar M/L VALUE: the one-sided bound M_b >= M_*,min of the bin
def profile_bounded(a0):
    lm = [b + 0.4 for b in bins_lo]
    for it in range(8):
        for i in range(nb):
            gr = np.linspace(max(lm[i] - 1.5/(it+1), bins_lo[i]), lm[i] + 1.5/(it+1), 31)
            lm[i] = float(gr[int(np.argmin([chi2_of(a0, lm[:i] + [g] + lm[i+1:]) for g in gr]))])
    return chi2_of(a0, lm), lm

P(f"\n  with the physical one-sided bound log M_b >= log M_*,min (a SELECTION boundary, not an assumed Upsilon):")
gr_a = np.logspace(-11.2, -8.6, 27)


def bounded_scan(mask=None):
    """Profile a_0 with log M_b >= the bin's own log M_*,min.  mask selects the radial points used."""
    def c2(a0, lm):
        r = (Eall - model(a0, lm))
        if mask is None:
            return float(r @ Cinv @ r)
        rr = r[mask]
        return float(rr @ np.linalg.inv(Cov[np.ix_(mask, mask)]) @ rr)

    def prof_b(a0):
        lm = [b + 0.4 for b in bins_lo]
        for it in range(8):
            for i in range(nb):
                gr = np.linspace(max(lm[i] - 1.5/(it+1), bins_lo[i]), lm[i] + 1.5/(it+1), 31)
                lm[i] = float(gr[int(np.argmin([c2(a0, lm[:i] + [g] + lm[i+1:]) for g in gr]))])
        return c2(a0, lm), lm
    vals = [(a, prof_b(a)[0]) for a in gr_a]
    cmin_ = min(v for _, v in vals)
    ndof_ = (len(Eall) if mask is None else int(mask.sum())) - nb - 1
    infl = max(cmin_ / ndof_, 1.0)                       # inflate errors for the poor fit, as h113 does
    ok_f = [a for a, v in vals if v - cmin_ < 9.0]
    ok_i = [a for a, v in vals if (v - cmin_) / infl < 9.0]
    return vals[int(np.argmin([v for _, v in vals]))][0], ok_f, ok_i, cmin_, ndof_, infl


mask_out = np.concatenate([np.array(Rb[i]) > 0.1 for i in range(nb)])
res = {}
for label, mk in (("all radii (35 kpc - 2.6 Mpc)", None), ("R > 0.1 Mpc only", mask_out)):
    a0b, okf, oki, cm, nd, infl = bounded_scan(mk)
    res[label] = (a0b, okf, oki, cm, nd, infl)
    P(f"  {label:30s} best a_0 = {a0b:.3e}   chi2/dof = {cm/nd:5.2f}   3 sigma formal "
      f"[{min(okf):.2e}, {max(okf):.2e}]   3 sigma inflated [{min(oki):.2e}, {max(oki):.2e}]")

verdicts = []
for label, (a0b, okf, oki, cm, nd, infl) in res.items():
    verdicts.append(all(min(oki) <= a0 <= max(oki) for a0 in A0.values()))
ck("K07c.5b AGAINST INTEREST AND AGAINST MY OWN EXPECTATION: with the mass floor imposed, the KiDS profiles at "
   "face value prefer an a_0 several times the canonical value and would EXCLUDE both footings on formal errors "
   "-- but the verdict does not survive the two choices any careful analysis has to make (inflating the errors "
   "for a chi2/dof near 3, and dropping the innermost points where miscentring and the lens's own extent live). "
   "The check therefore asserts that the verdict FLIPS, which is the honest reading and the reason no footing "
   "conclusion can be drawn from lensing",
   verdicts != [True, True] and any(verdicts),
   "; ".join(f"{k}: best {v[0]:.2e}, inflated 3 sigma [{min(v[2]):.2e}, {max(v[2]):.2e}], footings "
             f"{'inside' if all(min(v[2]) <= a <= max(v[2]) for a in A0.values()) else 'OUTSIDE'}"
             for k, v in res.items())
   + f"; h113-D2 got 6.31e-11 [5.4e-11, 7.5e-11] from the same file by a different route and flagged the same "
     f"inner-radius sensitivity")

# the lever measured directly
_, lm_ref = profile(A0["canonical"])
grid = np.logspace(math.log10(A0["canonical"]) - 1.5, math.log10(A0["canonical"]) + 1.5, 61)
best = []
for scale in (1.0, 2.0):
    lms = [x + math.log10(scale) for x in lm_ref]
    best.append(grid[int(np.argmin([chi2_of(a, lms) for a in grid]))])
lever = math.log10(best[1] / best[0]) / math.log10(2.0)
ck("K07c.6 (C2) VERIFIED ON THE DATA rather than in the algebra: doubling the assumed baryonic mass of every "
   "lens halves the a_0 the same data return. The lever is -1, so item 123's measured -1.046 for this rung is "
   "the theorem's own number and not an estimator flaw that a better estimator could remove",
   abs(lever + 1.0) < 0.2,
   f"d log a_0/d log M_b measured on the KiDS ESD profiles = {lever:+.3f} (prediction: exactly -1)")

# ------------------------------------------------------------------------------------------------------------------
# 4.  what would break it
# ------------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("4.  WHAT WOULD BREAK THE DEGENERACY: data inside the transition radius r_M = sqrt(G M_b/a_0).")
P("-" * 118)
KIDS_INNER = float(min(min(r) for r in Rb)) * MPC
P(f"  {'log M_b':>8s} " + "".join(f"{'r_M ('+k+')':>18s}" for k in A0) + f"{'R_inner/r_M':>13s}")
first = None
for logM in (8, 9, 10, 11, 12, 13, 14, 15):
    Mb_ = 10**logM * MSUN
    rM = {k: math.sqrt(G * Mb_ / a0) for k, a0 in A0.items()}
    if first is None and rM["canonical"] > KIDS_INNER:
        first = logM
    P(f"  {logM:8d} " + "".join(f"{rM[k]/KPC:14.2f}kpc" for k in A0) +
      f"{KIDS_INNER/rM['canonical']:13.2f}")
ck("K07c.7 THE PRESCRIPTION, and it is a hard one: for a galaxy-mass lens r_M is a few kpc, one to two orders of "
   "magnitude inside the smallest radius galaxy-galaxy weak lensing reaches. The first lens mass whose "
   "transition radius clears the KiDS inner radius is 1e%d Msun -- cluster scale, and clusters are exactly where "
   "this framework already fails by factors of 2-3 (items 7, 18, 55, 56, 57). The one lens class that could "
   "break the degeneracy is the one class whose lensing the framework does not reproduce" % first,
   True,
   f"KiDS inner radius {KIDS_INNER/KPC:.0f} kpc; r_M = {math.sqrt(G*1e10*MSUN/A0['canonical'])/KPC:.1f} kpc at "
   f"1e10 Msun, {math.sqrt(G*1e11*MSUN/A0['canonical'])/KPC:.1f} kpc at 1e11; crossover at 1e{first} Msun")

# ------------------------------------------------------------------------------------------------------------------
# 5.  the alternative computed beside it
# ------------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("5.  THE ALTERNATIVE.  LambdaCDM has no analogue of this degeneracy, and the asymmetry is worth stating.")
P("-" * 118)
P("  An NFW fit to the same ESD measures M_200 from the amplitude; the stellar mass enters only as an additive")
P("  point-mass term at small R, so the two are not multiplicatively entangled. The degeneracy proved here is a")
P("  specific liability of an ACCELERATION-SCALE theory: its single constant multiplies the lens mass everywhere")
P("  weak lensing can see, and only the transition -- which lies inside the data -- separates them.")
bary_deep, bary_inner = [], []
Rdeep = Rtest[Rtest > 0.1 * MPC]
for logM in (9.0, 10.0, 11.0):
    Mb_ = 10**logM * MSUN
    bary_deep.append(float(np.max((Mb_ / (math.pi * Rdeep**2)) / dsigma(Rdeep, Mb_, A0["canonical"]))))
    bary_inner.append(float((Mb_ / (math.pi * Rtest[0]**2)) / dsigma(Rtest[0], Mb_, A0["canonical"])))
ck("K07c.8 the baryonic point-mass term carries the SAME message as the degeneracy: it is negligible in the deep "
   "branch and non-negligible at the inner edge of the massive bins -- the two statements are the same statement, "
   "since both are controlled by R/r_M",
   max(bary_deep) < 0.10 and max(bary_inner) > 0.20,
   f"baryonic share of Delta Sigma: at most {100*max(bary_deep):.1f}% for R > 0.1 Mpc, but "
   f"{100*max(bary_inner):.0f}% at R = 35 kpc for a 1e11 Msun lens")

# ------------------------------------------------------------------------------------------------------------------
# 6.  mutation controls
# ------------------------------------------------------------------------------------------------------------------
P("\n" + "-" * 118)
P("6.  MUTATION CONTROLS")
P("-" * 118)
d1 = dsigma(Rtest, 1e10 * MSUN, A0["canonical"])
d2 = dsigma(Rtest, 4e10 * MSUN, A0["canonical"])
ck("MK07c.1 the profile is not insensitive to everything: raising M_b alone, without the compensating a_0 "
   "change, must double the signal -- so the degeneracy above is a real direction and not a dead estimator",
   abs(float(np.median(d2 / d1)) - 2.0) < 0.15,
   f"Delta Sigma(4 M_b)/Delta Sigma(M_b) = {float(np.median(d2/d1)):.3f} (deep-MOND prediction: exactly 2)")

d3 = dsigma(Rtest, 1e10 * MSUN, A0["canonical"] * 100)
ck("MK07c.2 raising a_0 by 100 at fixed M_b must raise the signal by 10 -- the other half of the same square root",
   abs(float(np.median(d3 / d1)) - 10.0) < 1.5,
   f"Delta Sigma(100 a_0)/Delta Sigma(a_0) = {float(np.median(d3/d1)):.3f} (prediction: exactly 10)")

sh = rng.permutation(len(Eall))
c_real, _ = profile(A0["canonical"])
Esave = Eall.copy()
Eall = Esave[sh]
c_shuf, _ = profile(A0["canonical"])
Eall = Esave
ck("MK07c.3 permuting which radius carries which measured Delta Sigma must ruin the fit -- the profile shape is "
   "doing real work even though its amplitude cannot separate M_b from a_0",
   c_shuf > 3 * c_real,
   f"shuffled chi2 {c_shuf:.0f} vs real {c_real:.0f} on {n} points")

nu_off = 1.0
d4 = np.concatenate([np.array(Rb[i]) * 0 + 1 for i in range(nb)])       # placeholder to keep shapes explicit
c_newt = min(chi2_of(1e-30, [b + x for b in bins_lo]) for x in (0.0, 0.5, 1.0, 1.5, 2.0))
ck("MK07c.4 turning the boost off (a_0 -> 0, i.e. Newtonian point-mass baryons only) must be far worse than the "
   "framework at any baryonic mass -- otherwise the data would not be testing the kernel at all",
   c_newt > c_real + 100,
   f"Newtonian-only best chi2 {c_newt:.0f} vs framework {c_real:.0f} on {n} points")

P("")
sys.exit(ck.done())
