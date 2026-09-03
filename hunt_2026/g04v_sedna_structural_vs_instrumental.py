#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g04v_sedna_structural_vs_instrumental.py -- ADVERSARIAL AUDIT of one claim in
g04_solar_system_eccentricity_discriminant.py.

THE CLAIM UNDER TEST (g04 check D2b, verbatim): "THE REASON IS STRUCTURAL, NOT INSTRUMENTAL: 25 yr is 0.22%
of Sedna's orbit ... the four free elements absorb 94% of the raw signal (a factor 16)."  Restated by the
orchestrator as: "The best real lever, Sedna, falls short STRUCTURALLY RATHER THAN INSTRUMENTALLY: the
precession signal is reabsorbed by its own orbital elements because 25 yr is 0.22% of one orbit."

WHAT THIS SCRIPT DOES.  It does not dispute that Sedna falls short -- it re-derives that and confirms it.
It disputes the ATTRIBUTION.  The total shortfall against a 3-sigma bar factorises exactly:

    3 / chi_postfit  =  [ 3 / chi_raw ]  x  [ chi_raw / chi_postfit ]
                          INSTRUMENTAL       STRUCTURAL
                          (the signal is       (the 4-element fit
                           small vs the         eats part of it)
                           astrometry)

"Structural rather than instrumental" is a claim that the SECOND factor dominates the first.  The test is
therefore a direct numerical comparison of the two factors, at both quoted precisions and both footings.
chi_raw is computed with the SAME weights, the SAME 401 epochs and the SAME two observables as g04's
chi_postfit -- the ONLY difference is that the 4-element projector is not applied.  The design matrix,
integrator, and postfit() are lifted verbatim from g04 so that any disagreement is about the decomposition
and not about the machinery.

CHECKS (all can fail; V4 is a mutation control):
  V1  chi_postfit reproduces g04's published Sedna table (both footings, both precisions)
  V2  the two factors multiply back to the total shortfall (the decomposition is exact)
  V3  the CLAIM: is the structural factor larger than the instrumental factor?
  V4  MUTATION CONTROL: an out-of-family perturbation (1/r^3) must be absorbed far LESS than the
      in-family element changes, and an in-family change (omega shift) must be absorbed essentially
      completely -- i.e. the projector discriminates, it does not eat everything
  V5  the precision route the claim forecloses: what per-epoch astrometry reaches 3 sigma at the
      PRESENT 25-yr arc?  ("more telescope does not help" is a quantitative claim, not a qualitative one)

Constants, elements, kernel and fit machinery: identical to g04.  Sedna elements from Brown, Trujillo &
Rabinowitz 2004, ApJ 617, 645 (a = 506.2 AU, e = 0.8496), as used in g04.
"""
import sys, math
import numpy as np
from scipy.integrate import solve_ivp
from hunt_lib import Check, P, info, A0

ck = Check()
np.seterr(all="ignore")

GM_SUN = 1.32712440018e20
AU     = 1.495978707e11
YR     = 3.155760000e7
RAD2MAS = 180.0/math.pi*3600.0*1000.0

A_SED, E_SED, R_NOW, T_ARC = 506.2*AU, 0.8496, 85.0*AU, 25.0*YR
E0 = -math.acos((1.0 - R_NOW/A_SED)/E_SED)
M0_SED = E0 - E_SED*math.sin(E0)
NEP = 401

P("="*114)
P("g04v -- ADVERSARIAL: is Sedna's shortfall STRUCTURAL (orbit-fit absorption) or INSTRUMENTAL (small signal)?")
P("="*114)


def numinus1_routeA(y):
    u = math.sqrt(max(float(y), 1e-300))
    return 1.0/math.expm1(u) if u < 700.0 else 0.0


def kepler_obs(a_m, e, om, M0, t, gm=GM_SUN):
    n = math.sqrt(gm/a_m**3); M = M0 + n*np.asarray(t); E = M.copy()
    for _ in range(200): E = E - (E - e*np.sin(E) - M)/(1.0 - e*np.cos(E))
    f = 2.0*np.arctan2(math.sqrt(1+e)*np.sin(E/2.0), math.sqrt(1-e)*np.cos(E/2.0))
    return np.concatenate([np.unwrap(f + om), np.log(a_m*(1.0 - e*np.cos(E)))])


def build(T):
    t = np.linspace(-T/2.0, T/2.0, NEP)
    base = kepler_obs(A_SED, E_SED, 0.0, M0_SED, t)
    p0 = [A_SED, E_SED, 0.0, M0_SED]; step = [A_SED*1e-6, 1e-7, 1e-7, 1e-9]
    cols = []
    for i in range(4):
        pp = list(p0); pm = list(p0); pp[i] += step[i]; pm[i] -= step[i]
        cols.append((kepler_obs(*pp, t) - kepler_obs(*pm, t))/(2.0*step[i]))
    return t, base, np.vstack(cols).T


def weights(sig_th_mas):
    """Identical weighting to g04.postfit: angles at sigma_theta, ln r at sigma_theta * r/AU (annual
    parallax: p = 1 AU / r, so sigma(ln r) = sigma(theta)/p = sigma(theta) * r / AU)."""
    s_th = sig_th_mas/RAD2MAS; s_lr = s_th*R_NOW/AU
    return np.concatenate([np.full(NEP, 1.0/s_th), np.full(NEP, 1.0/s_lr)])


def chi_raw(sig, sig_th_mas):
    """chi of the signal with NO orbit fit applied -- the same quadrature form g04 uses post-fit."""
    w = weights(sig_th_mas)
    return float(math.sqrt(np.sum((sig*w)**2)))


def postfit(sig, D, sig_th_mas):
    """Verbatim from g04."""
    w = weights(sig_th_mas)
    A = D*w[:, None]; nrm = np.linalg.norm(A, axis=0); A = A/nrm
    c, *_ = np.linalg.lstsq(A, sig*w, rcond=1e-14)
    res = (sig*w - A @ c)/w
    return res, float(math.sqrt(np.sum(((sig*w - A @ c))**2)))


def integrate_const(dg, t):
    n = math.sqrt(GM_SUN/A_SED**3); M = M0_SED + n*t[0]; E = M
    for _ in range(200): E = E - (E - E_SED*math.sin(E) - M)/(1 - E_SED*math.cos(E))
    Ed = n/(1 - E_SED*math.cos(E))
    f0 = 2*math.atan2(math.sqrt(1+E_SED)*math.sin(E/2), math.sqrt(1-E_SED)*math.cos(E/2))
    r0 = A_SED*(1 - E_SED*math.cos(E))
    s0 = [r0*math.cos(f0), r0*math.sin(f0), -A_SED*math.sin(E)*Ed,
          A_SED*math.sqrt(1-E_SED**2)*math.cos(E)*Ed]
    def rhs(_t, s):
        x, y, vx, vy = s; r = math.hypot(x, y); acc = -(GM_SUN/r**3 + dg/r)
        return [vx, vy, acc*x, acc*y]
    sol = solve_ivp(rhs, (t[0], t[-1]), s0, t_eval=t, rtol=3e-13, atol=1e-3, method="DOP853")
    return np.concatenate([np.unwrap(np.arctan2(sol.y[1], sol.y[0])),
                           np.log(np.hypot(sol.y[0], sol.y[1]))])


def integrate_pow(amp, p, t):
    """dg = amp*(AU/r)^p inward, for the out-of-family mutation control."""
    n = math.sqrt(GM_SUN/A_SED**3); M = M0_SED + n*t[0]; E = M
    for _ in range(200): E = E - (E - E_SED*math.sin(E) - M)/(1 - E_SED*math.cos(E))
    Ed = n/(1 - E_SED*math.cos(E))
    f0 = 2*math.atan2(math.sqrt(1+E_SED)*math.sin(E/2), math.sqrt(1-E_SED)*math.cos(E/2))
    r0 = A_SED*(1 - E_SED*math.cos(E))
    s0 = [r0*math.cos(f0), r0*math.sin(f0), -A_SED*math.sin(E)*Ed,
          A_SED*math.sqrt(1-E_SED**2)*math.cos(E)*Ed]
    def rhs(_t, s):
        x, y, vx, vy = s; r = math.hypot(x, y)
        acc = -(GM_SUN/r**3 + amp*(AU/r)**p/r)
        return [vx, vy, acc*x, acc*y]
    sol = solve_ivp(rhs, (t[0], t[-1]), s0, t_eval=t, rtol=3e-13, atol=1e-3, method="DOP853")
    return np.concatenate([np.unwrap(np.arctan2(sol.y[1], sol.y[0])),
                           np.log(np.hypot(sol.y[0], sol.y[1]))])


PER = 2.0*math.pi*math.sqrt(A_SED**3/GM_SUN)
P(f"\n  Sedna: a = {A_SED/AU:.1f} AU, e = {E_SED:.4f}, aphelion Q = {A_SED*(1+E_SED)/AU:.1f} AU, "
  f"P = {PER/YR:.1f} yr;  25 yr = {100*T_ARC/PER:.3f}% of one orbit  [g04 quotes 0.22%]")

tt, base, DES = build(T_ARC)
int0 = integrate_const(0.0, tt)

# ------------------------------------------------------------------ V1 / V2 / V3
info("V1-V3 -- the exact factorisation of the shortfall, MI-A envelope, both footings")
P(f"  {'footing':>10}{'sig_th':>9}{'dg [m/s2]':>12}{'raw mas':>10}{'post mas':>10}"
  f"{'chi_raw':>10}{'chi_post':>10}{'INSTR':>9}{'STRUCT':>9}{'total':>9}{'product':>9}")
G04_PUBLISHED = {("canonical", 100.0): 0.005, ("canonical", 10.0): 0.05,
                 ("alt", 100.0): 0.010, ("alt", 10.0): 0.10}
rep_err, prod_err, verdict = [], [], {}
for fn, a0 in A0.items():
    Q_sed = A_SED*(1 + E_SED)
    eps = numinus1_routeA(GM_SUN/Q_sed**2/a0)
    dgA = eps*GM_SUN/Q_sed**2
    sA = integrate_const(dgA, tt) - int0
    for sth in (100.0, 10.0):
        cr = chi_raw(sA, sth)
        rA, cp = postfit(sA, DES, sth)
        instr = 3.0/cr; struct = cr/cp; tot = 3.0/cp
        prod_err.append(abs(instr*struct/tot - 1.0))
        rep_err.append(abs(cp/G04_PUBLISHED[(fn, sth)] - 1.0))
        verdict[(fn, sth)] = (instr, struct, tot, cr, cp)
        P(f"  {fn:>10}{sth:>9.0f}{dgA:>12.3e}{np.std(sA[:NEP])*RAD2MAS:>10.3e}"
          f"{np.std(rA[:NEP])*RAD2MAS:>10.3e}{cr:>10.4f}{cp:>10.4f}{instr:>9.1f}{struct:>9.1f}"
          f"{tot:>9.1f}{instr*struct:>9.1f}")
P("    INSTR  = 3/chi_raw   : how far short the signal is BEFORE any orbit fit -- pure sensitivity")
P("    STRUCT = chi_raw/chi_post : how much the 4 free elements eat -- the 'structural' factor")
P("    total  = 3/chi_post  : the shortfall g04 quotes (639x at 100 mas canonical, 64x at 10 mas)")

ck("V1a  this audit reproduces g04's published Sedna MI-A significances",
   max(rep_err) < 0.12,
   f"worst relative deviation from g04's printed 0.005/0.05 (canonical) and 0.010/0.10 (alt) is "
   f"{100*max(rep_err):.1f}%, which is the rounding of the 1-2 significant figures g04 prints.  The "
   f"integrator, design matrix, weights and projector are lifted verbatim, so the machinery is not in "
   f"dispute -- only the attribution of the shortfall is")

ck("V2a  the shortfall factorises exactly into instrumental x structural",
   max(prod_err) < 1e-9,
   f"worst |INSTR*STRUCT/total - 1| = {max(prod_err):.1e}.  The decomposition is an identity, not a "
   f"model: 3/chi_post = (3/chi_raw)(chi_raw/chi_post).  There is no third factor to hide in")

can100 = verdict[("canonical", 100.0)]
alt100 = verdict[("alt", 100.0)]
can10  = verdict[("canonical", 10.0)]
alt10  = verdict[("alt", 10.0)]
ck("V3a  THE CLAIM: the shortfall is STRUCTURAL rather than INSTRUMENTAL at the headline precision",
   can100[1] > can100[0] and alt100[1] > alt100[0],
   f"IT IS NOT, at the 100 mas footing that carries the headline 0.005 sigma / 639x.  There the "
   f"INSTRUMENTAL factor is {can100[0]:.0f}x (canonical) / {alt100[0]:.0f}x (alt) and the STRUCTURAL factor "
   f"is only {can100[1]:.0f}x / {alt100[1]:.0f}x.  The signal is {can100[0]:.0f}x too small for 100 mas "
   f"astrometry BEFORE a single orbital element is fitted; switching the 4-element absorption off entirely "
   f"still leaves {can100[3]:.3f} sigma, {can100[0]:.0f}x short of 3.  The orbit-fit absorption is the "
   f"SMALLER of the two effects at the headline precision, so 'structural, NOT instrumental' inverts the "
   f"actual ranking.  (At 10 mas the ranking does flip -- INSTR {can10[0]:.1f}x vs STRUCT {can10[1]:.0f}x -- "
   f"so the honest statement is that BOTH factors independently suffice at 10 mas and the instrumental one "
   f"dominates at 100 mas.  The negative itself is untouched: Sedna falls short either way)")

# ------------------------------------------------------------------ V4 mutation control on the projector
info("V4 -- MUTATION CONTROL: does the projector discriminate, or does it eat everything?")
om_shift = kepler_obs(A_SED, E_SED, 1e-9, M0_SED, tt) - base          # IN-family, must vanish
s_p3 = integrate_pow(1e-12, 3.0, tt) - int0                            # OUT-of-family 1/r^3
s_p0 = integrate_const(1e-12, tt) - int0                               # OUT-of-family constant
rows = []
for nm, s in (("omega+1e-9 (IN-family)", om_shift), ("dg = 1e-12 (AU/r)^3", s_p3),
              ("dg = 1e-12 const", s_p0)):
    cr = chi_raw(s, 100.0); _, cp = postfit(s, DES, 100.0)
    rows.append((nm, cr, cp, cr/cp))
    P(f"  {nm:<26} chi_raw {cr:>11.4e}  chi_post {cp:>11.4e}  absorbed factor {cr/cp:>11.3e}")
in_fam = rows[0][3]; out_fam = max(rows[1][3], rows[2][3])
ck("V4a  MUTATION CONTROL: in-family absorbed >1e4x more strongly than out-of-family",
   in_fam/out_fam > 1e4,
   f"a pure omega shift (which IS one of the 4 fitted elements) is absorbed by a factor {in_fam:.1e}, while "
   f"the out-of-family radial perturbations are absorbed by only {out_fam:.1e}.  A ratio of "
   f"{in_fam/out_fam:.1e}.  So the factor-16 absorption reported for MI-A is a REAL partial degeneracy and "
   f"not a projector that flattens everything -- g04's structural mechanism is genuine, it is only its "
   f"RANKING against the instrumental factor that this audit disputes")

# ------------------------------------------------------------------ V5 the foreclosed route
info("V5 -- 'more telescope does not help, only more decades do' -- quantified at the PRESENT 25-yr arc")
fn = "canonical"; a0 = A0[fn]
Q_sed = A_SED*(1 + E_SED); eps = numinus1_routeA(GM_SUN/Q_sed**2/a0); dgA = eps*GM_SUN/Q_sed**2
sA = integrate_const(dgA, tt) - int0
_, cp10 = postfit(sA, DES, 10.0)
sig_need = 10.0*cp10/3.0                       # chi scales as 1/sigma at fixed epochs
P(f"  MI-A on the existing 25-yr arc reaches 3 sigma at a per-epoch astrometric precision of "
  f"{sig_need*1000:.0f} micro-arcsec ({sig_need:.3f} mas), at {NEP} epochs.")
P(f"  Equivalently, at 10 mas it needs {NEP*(3.0/cp10)**2:.2e} epochs -- which is the route that really is shut.")
P(f"  g04's D4a scan instead extends the ARC and finds 3 sigma at ~400 yr.  Both statements are true; g04")
P(f"  scans only one axis and then asserts the other axis is closed.  {sig_need:.3f} mas is {10.0/sig_need:.0f}x")
P(f"  beyond LSST-class but it is not centuries away, and Sedna is V=20.6 -- within reach of a dedicated")
P(f"  space-astrometry programme in principle.  Reported as a caveat on the framing, not as a live proposal.")
ck("V5a  the precision axis is as closed as the arc axis (needs > 1e6 x better astrometry)",
   sig_need < 1e-5,
   f"NOT AT THAT LEVEL.  The required per-epoch precision on the existing arc is {sig_need:.3f} mas = "
   f"{sig_need*1000:.0f} uas, only {10.0/sig_need:.0f}x beyond the 10 mas LSST-class figure g04 uses -- not "
   f"the 'centuries, not a bigger telescope' dichotomy D4a asserts.  The epoch count route is genuinely "
   f"shut ({NEP*(3.0/cp10)**2:.1e} epochs at 10 mas), and the overall NEGATIVE stands, but the specific "
   f"claim that only more decades help is not established by the scan D4a actually ran")

# ------------------------------------------------------------------ V6 is MI-A really the MOST GENEROUS MI?
info("V6 -- is MI-A an envelope over MODIFIED INERTIA, or only over Route A's own kernel?")
P("  Milgrom's theorem (1994, Ann. Phys. 229, 384) fixes MI = MG for CIRCULAR orbits.  Sedna's orbit is")
P("  nowhere near circular and nowhere near deep-MOND: its APHELION sits at y = g_N/a_0 = %.0f (canonical),"
  % (GM_SUN/(A_SED*(1+E_SED))**2/A0["canonical"]))
P("  sqrt(y) = %.1f, i.e. DEEP NEWTONIAN.  No theorem constrains MI there.  So MI-A/MI-B are not envelopes"
  % math.sqrt(GM_SUN/(A_SED*(1+E_SED))**2/A0["canonical"]))
P("  derived from MI; they are Route A's EXPONENTIAL kernel evaluated at the orbit's minimum acceleration.")
P("  But the exponential approach to Newton is a MODIFIED-GRAVITY fit choice.  MI's own kernel is not fixed")
P("  by it -- that is the whole content of the fork.  The standard MOND interpolating families approach")
P("  Newton as a POWER law, nu - 1 ~ 1/y (the 'simple'/RAR family), not as exp(-sqrt y).  On Sedna's")
P("  aphelion that is the difference between 1/(e^8.5-1) = 2.0e-4 and 1/72 = 1.4e-2: a factor ~68.")
P("")
P(f"  {'MI reading':<34}{'dg [m/s2]':>12}{'/ a_0':>9}{'post mas':>11}{'sig@100':>9}{'sig@10':>9}")
mi_rows = {}
for fn, a0 in A0.items():
    Q_sed = A_SED*(1 + E_SED); gQ = GM_SUN/Q_sed**2; yQ = gQ/a0
    cases = [("MI-A, Route A exp kernel", numinus1_routeA(yQ)*gQ),
             ("MI-A, power-law nu-1 = 1/(2y)", 0.5/yQ*gQ),
             ("MI-A, anomaly of order a_0",    a0)]
    for nm, dg in cases:
        s = integrate_const(dg, tt) - int0
        _, c100 = postfit(s, DES, 100.0); _, c10 = postfit(s, DES, 10.0)
        r, _ = postfit(s, DES, 100.0)
        mi_rows[(fn, nm)] = (dg, c100, c10)
        P(f"  {fn[:3]+' '+nm:<34}{dg:>12.3e}{dg/a0:>9.3f}{np.std(r[:NEP])*RAD2MAS:>11.3e}"
          f"{c100:>9.3f}{c10:>9.2f}")
pl_can = mi_rows[("canonical", "MI-A, power-law nu-1 = 1/(2y)")]
a0_can = mi_rows[("canonical", "MI-A, anomaly of order a_0")]
a0_alt = mi_rows[("alt", "MI-A, anomaly of order a_0")]
P("")
P("  BUT THE COUNTEREXAMPLE MUST ITSELF SURVIVE THE INNER PLANETS.  Under the SAME MI-A ansatz, Mars's")
P("  anomaly is keyed to MARS's aphelion, so any MI kernel generous at Sedna is also generous at Mars.")
P("  Scan the one-parameter power-law family nu - 1 = y^-p (normalised so nu - 1 = 1 at y = 1, which is")
P("  what galaxy rotation curves require of any MOND-class kernel) and impose EVERY planetary bound:")

# JPL mean elements + the delta-g bounds g04 validates in its A1a against BOUNDS.md sec 1.2
# (Fienga & Minazzoli 2024, Living Rev. Relativ. 27:1, arXiv:2303.01821, Table 10).
PLANETS = [("Mercury", 0.38709927, 0.20563593, 0.006), ("Venus", 0.72333566, 0.00677672, 0.015),
           ("Earth", 1.00000261, 0.01671123, 0.0019), ("Mars", 1.52371034, 0.09339410, 0.00037),
           ("Jupiter", 5.20288700, 0.04838624, 0.28), ("Saturn", 9.53667594, 0.05386179, 0.0047)]

def dg_bound(a_m, e, sw):
    Pyr = 2.0*math.pi*math.sqrt(a_m**3/GM_SUN)/YR
    return (sw/RAD2MAS)*Pyr*GM_SUN/(2.0*math.pi*a_m**2*math.sqrt(1.0 - e*e))

P(f"  {'p':>6}{'binding planet':>16}{'dg(Sedna)/a_0':>15}{'dg [m/s2]':>12}{'sigma @10mas':>14}")
best = (0.0, None, 0.0)
a0 = A0["canonical"]
yS = GM_SUN/(A_SED*(1 + E_SED))**2/a0
for p in (1.0, 1.25, 1.5, 1.656, 1.75, 2.0, 2.5, 3.0):
    ok, binder = True, None
    for nm, aAU, e, sw in PLANETS:
        a_m = aAU*AU; Qp = a_m*(1 + e); yP = GM_SUN/Qp**2/a0
        dgP = yP**(-p)*GM_SUN/Qp**2
        if dgP > dg_bound(a_m, e, sw):
            ok = False; binder = nm; break
    dgS = yS**(-p)*GM_SUN/(A_SED*(1 + E_SED))**2
    sigS = 0.05*dgS/mi_rows[("canonical", "MI-A, Route A exp kernel")][0]   # chi is linear in dg
    P(f"  {p:>6.3f}{(binder if binder else 'ALLOWED'):>16}{dgS/a0:>15.4f}{dgS:>12.3e}"
      f"{(sigS if ok else float('nan')):>14.2f}")
    if ok and dgS > best[0]*a0:
        best = (dgS/a0, p, sigS)
P(f"  The planetary bounds force p > ~1.66 (Mars binds); at the boundary the Sedna anomaly is capped at")
P(f"  {best[0]:.3f} a_0 = {best[0]*a0:.2e} m/s^2, giving {best[2]:.2f} sigma at 10 mas on the 25-yr arc.")
ck("V6a  MI-A bounds every modified-inertia reading, so 'shut for the most generous is shut for all'",
   best[2] < 3.0 and a0_can[2] > 3.0,
   f"UPHELD, BUT NOT FOR THE REASON g04 GIVES, AND ITS SCOPE MUST BE NARROWED.  Taken at face value the "
   f"envelope claim fails: MI-A is the most generous reading of ROUTE A'S EXPONENTIAL kernel, not of "
   f"modified inertia, and Sedna's aphelion sits at y = {yS:.0f} -- DEEP NEWTONIAN, where Milgrom's "
   f"circular-orbit theorem says nothing and MI's interpolating behaviour is not fixed by the MG fit.  A "
   f"free anomaly of order a_0 along the orbit gives {a0_can[2]:.1f} sigma (canonical) / {a0_alt[2]:.1f} "
   f"(alt) at 10 mas, ABOVE 3, so MI-A is NOT an envelope over the class.  What rescues the conclusion is a "
   f"constraint g04 never invokes here: under the SAME MI-A ansatz the inner planets are bound too, and "
   f"Mars forces any power-law kernel nu-1 = y^-p (normalised to O(1) at y ~ 1, as rotation curves require) "
   f"to p > 1.66, capping Sedna at {best[0]:.3f} a_0 = {best[2]:.2f} sigma at 10 mas.  So the NEGATIVE "
   f"survives on the one-parameter power-law family -- by an inner-planet argument, not by MI-A being an "
   f"envelope.  It is NOT established for kernels with intrinsic eccentricity dependence, which a genuinely "
   f"nonlocal MI has and which Mars (e = 0.09) cannot constrain from Sedna (e = 0.85)")

# ------------------------------------------------------------------ V7 where the arc scan actually crosses 3
info("V7 -- the arc length at which MI-A crosses 3 sigma: g04's grid says '~400 yr', the grid is coarse")
dg_can = mi_rows[("canonical", "MI-A, Route A exp kernel")][0]
P(f"  {'arc [yr]':>10}{'% of orbit':>12}{'post mas':>12}{'sigma @10mas':>14}")
scan = []
for T_yr in (150.0, 175.0, 200.0, 225.0, 250.0, 300.0, 400.0):
    T = T_yr*YR; t2, b2, D2 = build(T)
    i0 = integrate_const(0.0, t2)
    s2 = integrate_const(dg_can, t2) - i0
    r2, c2 = postfit(s2, D2, 10.0)
    scan.append((T_yr, c2))
    P(f"  {T_yr:>10.0f}{100*T/PER:>12.2f}{np.std(r2[:NEP])*RAD2MAS:>12.3e}{c2:>14.2f}")
cross = [T for T, c in scan if c > 3.0]
first_cross = min(cross) if cross else float("inf")
ck("V7a  3 sigma at 10 mas genuinely requires an arc of ~400 yr, as g04's D4a states",
   first_cross > 350.0,
   f"IT DOES NOT.  On a finer grid the MI-A residual crosses 3 sigma at an arc of ~{first_cross:.0f} yr "
   f"({100*first_cross*YR/PER:.1f}% of the orbit), not ~400 yr.  g04's D4a scanned octaves (25, 50, 100, 200, "
   f"400) and quoted the first grid point above 3 sigma; its own printed row at 200 yr already reads 2.85 "
   f"sigma.  This overstates the required arc by roughly a factor 2 -- in the direction of a STRONGER "
   f"negative, so it is conservative for the conclusion but wrong as a number.  The qualitative statement "
   f"(centuries, not decades) survives")

P("")
P("="*114)
P("VERDICT OF THIS AUDIT")
P("="*114)
P(f"""
 CONFIRMED.  Sedna's MI-A precession channel falls short.  chi_post = {can100[4]:.4f} sigma at 100 mas and
 {can10[4]:.3f} sigma at 10 mas (canonical), {alt100[4]:.4f} / {alt10[4]:.3f} (alt), reproducing g04's table
 to within its printed precision.  The mutation controls confirm the projector is not manufacturing the
 negative (V4a: in-family absorbed {in_fam:.0e}x, out-of-family {out_fam:.0e}x).  25 yr really is
 {100*T_ARC/PER:.2f}% of the orbit and the 4-element family really does eat a factor {can100[1]:.0f} of the signal.

 REFUTED, THE CAUSAL CLAUSE (V3a).  "The reason is STRUCTURAL, NOT INSTRUMENTAL" inverts the ranking at the
 headline 100 mas canonical footing -- the one that carries the quoted 0.005 sigma and 639x.  There the
 instrumental factor is {can100[0]:.0f}x and the structural factor {can100[1]:.0f}x.  With the 4-element fit switched off
 entirely the signal is still only {can100[3]:.3f} sigma, {can100[0]:.0f}x short of 3.  The correct statement is: at 100 mas
 the shortfall is mostly instrumental ({can100[0]:.0f}x) with a factor {can100[1]:.0f} of orbit-fit absorption on top; at
 10 mas the absorption becomes the larger single factor ({can10[1]:.0f}x vs {can10[0]:.1f}x); at neither precision does
 either factor alone explain the shortfall, and at both precisions either alone would suffice to close it.
 The bottom line is untouched.  The error is in the attribution, not the arithmetic.

 TWO SECONDARY NUMBERS OVERSTATED, BOTH TOWARD A STRONGER NEGATIVE.
  * V7a: 3 sigma at 10 mas is reached at an arc of ~{first_cross:.0f} yr, not the ~400 yr D4a quotes -- D4a scanned
    octaves and reported the first grid point above 3 sigma while its own 200-yr row already read 2.85.
  * V5a: "more telescope does not help, only more decades do" is not what the numbers say.  On the EXISTING
    25-yr arc, {sig_need:.3f} mas per epoch reaches 3 sigma -- {10.0/sig_need:.0f}x beyond LSST-class, not centuries away.  The
    epoch-count route is the one genuinely shut ({NEP*(3.0/cp10)**2:.1e} epochs at 10 mas).

 ONE SCOPE NARROWING, NOT A REFUTATION (V6a).  "MI-A is the most generous reading, and a route shut for the
 most generous is shut for every reading" is false as stated: MI-A is the most generous reading of ROUTE A'S
 EXPONENTIAL kernel, and Sedna's aphelion is at y = {yS:.0f}, DEEP NEWTONIAN, where Milgrom's circular-orbit
 theorem constrains nothing and MI's interpolating behaviour is not fixed by the MG fit.  A free O(a_0)
 anomaly gives {a0_can[2]:.1f} / {a0_alt[2]:.1f} sigma at 10 mas.  The conclusion is nevertheless rescued, by an argument g04
 does not make: under the same ansatz Mars binds too, forcing nu-1 = y^-p to p > 1.66 and capping Sedna at
 {best[0]:.3f} a_0 = {best[2]:.2f} sigma.  It remains unestablished for kernels with intrinsic eccentricity dependence.

 WHAT SURVIVES INTACT.  Milgrom's theorem is stated conservatively and is not leaned on anywhere it does not
 apply; the deep-MOND limit is never invoked on Sedna (the full kernel is used at y = {yS:.0f} to 1e4); and both
 a_0 footings genuinely propagate -- dg differs by {mi_rows[('alt','MI-A, Route A exp kernel')][0]/mi_rows[('canonical','MI-A, Route A exp kernel')][0]:.2f}x between footings against an a_0 ratio of
 {A0['alt']/A0['canonical']:.2f}x, i.e. through the exponential, not decoratively.
""")
sys.exit(ck.done())
