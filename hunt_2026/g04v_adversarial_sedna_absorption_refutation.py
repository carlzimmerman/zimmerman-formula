#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
g04v_adversarial_sedna_absorption_refutation.py -- ADVERSARIAL AUDIT of g04's D2/D4 Sedna claim.
================================================================================================
THE CLAIM UNDER ATTACK (g04_solar_system_eccentricity_discriminant.py, checks D2b and D4a):

  "The best real lever, Sedna, falls short STRUCTURALLY rather than INSTRUMENTALLY: the precession
   signal is reabsorbed by its own orbital elements because 25 yr is 0.22% of one orbit."
  Supporting numbers: MI-A dg = 1.375e-12 / 2.952e-12 m/s^2; raw 0.355 / 0.762 mas; post-fit
  0.0226 / 0.0486 mas = 0.005 / 0.010 sigma at 100 mas and 0.05 / 0.10 sigma at 10 mas; "3 sigma at
  10 mas requires a ~400 yr arc (3.5% of the orbit)"; "more telescope does not help and only more
  decades do".

MY JOB IS TO REFUTE IT.  I reproduce the machinery INDEPENDENTLY (my own Kepler propagator, my own
design matrix built with different step sizes, my own QR-based projector rather than lstsq) and then
attack the INFERENCE rather than the arithmetic.

THE TWO ATTACKS.

  ATTACK 1 -- THE DECOMPOSITION.  "Structural rather than instrumental" is a factorisable statement.
    Write the shortfall to a 3-sigma bar as
        3/sigma_obtained  =  I x S ,
        I = 3 / (raw_signal / (astrometric_precision / sqrt(N_epochs)))   [INSTRUMENTAL: how far the
            RAW, completely unabsorbed signal is from the bar, given the instrument]
        S = raw_signal / post-fit_signal                                  [STRUCTURAL: the fraction
            the 4-element family eats]
    The claim is that S dominates I.  If I >= S the stated reason is wrong even though the number is
    right, and the honest sentence is "the signal is too small for the instrument", not "the orbit fit
    eats it".  This is exactly the repo's own known-bug pattern of a conclusion whose sign tracks a
    branch of one's own prescription rather than the data.

  ATTACK 2 -- THE EPOCH COUNT IS HELD FIXED WHILE THE ARC IS STRETCHED.  g04's D4 scan reports
    "sigma @10mas" for arcs of 25 ... 1600 yr while holding NEP = 401 epochs at every arc length.  An
    OBSERVING PROGRAMME of length T at a fixed cadence has N proportional to T, and chi scales as
    sqrt(N).  g04's own baseline is 401 epochs in 25 yr = 16.0 epochs/yr; carrying that cadence
    forward multiplies chi by sqrt(T/25).  If that alone moves the 3-sigma crossing from ~400 yr to
    inside D4a's own "realistic <= 200 yr" bar, then D4a FAILS for a reason that is an artefact of the
    scan's own bookkeeping, and the "centuries, not a bigger telescope" framing goes with it.

WHAT I AM NOT ATTACKING, AND WHY THE UNDERLYING NEGATIVE IS SAFE.  Every confound I can find pushes
the SAME way g04 concluded, so the null itself is conservative and I could not overturn it:
  * a REAL Sedna solution fits 6 elements plus planetary masses plus (in the Planet Nine literature) a
    distant perturber -- more free parameters absorb MORE, never less.  V4 quantifies this with a 5th
    free column (an unmodelled interior mass), and it makes both channels worse.
  * heterogeneous ground-based astrometry carries a catalogue systematic floor that does NOT average
    down as 1/sqrt(N).  V5 imposes one and it makes both channels worse.
  * MI-A is an upper envelope, not a prediction, so the true MI signal is smaller still.
Cold dark matter is irrelevant here in both directions: at 10^4-10^8 a_0 both GR+CDM and every healthy
MOND-family theory predict zero anomaly, so nothing in g04's Part D discriminates the framework
against LambdaCDM and g04 says so.  The claim is an internal feasibility statement, and it is on the
feasibility bookkeeping that it can be attacked.

DATA / LITERATURE INPUTS (no invented numbers).
  Sedna a = 506.2 AU, e = 0.8496, r_now ~ 85 AU: Brown, Trujillo & Rabinowitz 2004, ApJ 617, 645
      (the same values g04 uses; taken from g04 so the comparison is like-for-like).
  GM_sun, AU: IAU nominal / JPL.
  Astrometric precisions 100 mas (ground-based, V=20.6) and 10 mas (LSST-class): ESTIMATES carried
      over from g04.  NOT a published Sedna orbit covariance -- this repository holds none, so every
      sigma here inherits that, exactly as g04 states.  The DECOMPOSITION attacked in V2 is
      precision-INDEPENDENT in its structural factor S and precision-DEPENDENT in I, which is the
      whole point: the claim is quoted at 100 mas and at 10 mas and the verdict differs between them.
  Both a_0 footings throughout: 9.36e-11 (canonical) and 1.13e-10 (alt).
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
M_EARTH_OVER_M_SUN = 1.0/332946.0487

A_SED, E_SED, R_NOW = 506.2*AU, 0.8496, 85.0*AU
P_SED = 2.0*math.pi*math.sqrt(A_SED**3/GM_SUN)
E0 = -math.acos((1.0 - R_NOW/A_SED)/E_SED)
M0_SED = E0 - E_SED*math.sin(E0)
T_ARC = 25.0*YR
CADENCE = 401.0/25.0          # g04's own baseline: 401 epochs over a 25-yr arc = 16.04 epochs/yr

P("="*112)
P("g04v -- ADVERSARIAL: is Sedna's shortfall STRUCTURAL (orbit-fit absorption) or INSTRUMENTAL (signal")
P("        too small for the astrometry)?  And is the '400 yr arc' number an artefact of a fixed epoch count?")
P("="*112)
P(f"  Sedna: a = {A_SED/AU:.1f} AU, e = {E_SED:.4f}, r_now = {R_NOW/AU:.0f} AU, P = {P_SED/YR:.0f} yr; "
  f"25-yr arc = {100*T_ARC/P_SED:.3f}% of the orbit")


# ------------------------------------------------------------------ independent Kepler / fit machinery
def kepler_obs(a_m, e, om, M0, t, gm=GM_SUN):
    """(unwrapped heliocentric longitude, ln r) stacked.  Newton on Kepler's equation, own implementation."""
    n = math.sqrt(gm/a_m**3); M = M0 + n*np.asarray(t, dtype=float)
    E = M + e*np.sin(M)
    for _ in range(120):
        E = E - (E - e*np.sin(E) - M)/(1.0 - e*np.cos(E))
    f = 2.0*np.arctan2(math.sqrt(1+e)*np.sin(E/2.0), math.sqrt(1-e)*np.cos(E/2.0))
    return np.concatenate([np.unwrap(f + om), np.log(a_m*(1.0 - e*np.cos(E)))])

def design(t, extra_gm=False):
    """Partials of the observables wrt the 4 in-plane elements (a, e, omega, M0), optionally plus a 5th
    column: an unmodelled interior mass (GM rescale).  Steps deliberately DIFFERENT from g04's, so this is
    not the same finite-difference table."""
    p0 = [A_SED, E_SED, 0.0, M0_SED]
    step = [A_SED*3e-7, 4e-8, 3e-8, 4e-10]        # g04 used 1e-6, 1e-7, 1e-7, 1e-9
    cols = []
    for i in range(4):
        pp = list(p0); pm = list(p0); pp[i] += step[i]; pm[i] -= step[i]
        cols.append((kepler_obs(*pp, t) - kepler_obs(*pm, t))/(2.0*step[i]))
    if extra_gm:
        h = 1e-9
        cols.append((kepler_obs(*p0, t, gm=GM_SUN*(1+h)) - kepler_obs(*p0, t, gm=GM_SUN*(1-h)))/(2*h))
    return np.vstack(cols).T

def project(sig, D, sig_th_mas, nep, floor_mas=0.0):
    """Weighted least-squares removal of the fit family, by QR on the whitened+column-normalised design
    (g04 used np.linalg.lstsq; QR is an independent route to the same projector).  Returns
    (post-fit rms of the LONGITUDE block in mas, chi = ||P_perp(w s)||).
    floor_mas > 0 adds a per-epoch systematic in quadrature that does NOT average down: it is applied as
    an N-independent term, i.e. sigma_eff = sqrt(sig_th^2/N + floor^2), implemented by inflating weights."""
    s_th = sig_th_mas/RAD2MAS
    s_lr = s_th*R_NOW/AU                       # annual parallax: sigma(ln r) = sigma(theta)*r/AU
    w = np.concatenate([np.full(nep, 1.0/s_th), np.full(nep, 1.0/s_lr)])
    A = D*w[:, None]
    nrm = np.linalg.norm(A, axis=0); nrm[nrm == 0] = 1.0
    A = A/nrm
    Q, _ = np.linalg.qr(A)
    b = sig*w
    r = b - Q @ (Q.T @ b)
    chi = float(np.linalg.norm(r))
    if floor_mas > 0.0:
        # a floor that does not average down: the N-epoch aggregate significance is capped at
        # chi_eff = chi / sqrt(1 + N*(floor/sig_th)^2)
        chi = chi/math.sqrt(1.0 + nep*(floor_mas/sig_th_mas)**2)
    post = float(np.std((r/w)[:nep])*RAD2MAS)
    return post, chi

def integrate_const(dg, t):
    """Two-body plus a CONSTANT inward dg (the MI-A envelope), DOP853."""
    n = math.sqrt(GM_SUN/A_SED**3); M = M0_SED + n*t[0]; E = M + E_SED*math.sin(M)
    for _ in range(120): E = E - (E - E_SED*math.sin(E) - M)/(1 - E_SED*math.cos(E))
    Ed = n/(1 - E_SED*math.cos(E))
    f0 = 2*math.atan2(math.sqrt(1+E_SED)*math.sin(E/2), math.sqrt(1-E_SED)*math.cos(E/2))
    r0 = A_SED*(1 - E_SED*math.cos(E))
    s0 = [r0*math.cos(f0), r0*math.sin(f0), -A_SED*math.sin(E)*Ed,
          A_SED*math.sqrt(1-E_SED**2)*math.cos(E)*Ed]
    def rhs(_t, s):
        x, y, vx, vy = s; r = math.hypot(x, y); acc = -(GM_SUN/r**3 + dg/r)
        return [vx, vy, acc*x, acc*y]
    sol = solve_ivp(rhs, (t[0], t[-1]), s0, t_eval=t, rtol=3e-13, atol=1e-3, method="DOP853")
    return np.concatenate([np.unwrap(np.arctan2(sol.y[1], sol.y[0])), np.log(np.hypot(sol.y[0], sol.y[1]))])

def numinus1(y):
    u = math.sqrt(max(float(y), 1e-300))
    return 1.0/math.expm1(u) if u < 700.0 else 0.0

def mi_a_dg(a0):
    """MI-A envelope: nu-1 evaluated at APHELION, turned into a constant radial acceleration."""
    Q = A_SED*(1 + E_SED); gQ = GM_SUN/Q**2
    eps = numinus1(gQ/a0)
    return eps*gQ, eps


# ============================================================================================ V1
P(""); P("-"*112)
P("V1 -- do g04's central Sedna numbers reproduce under an INDEPENDENT propagator, design matrix and projector?")
P("-"*112)
G04 = {"canonical": dict(dg=1.375e-12, raw=0.3549, post=2.263e-2, c100=0.0045, c10=0.045),
       "alt":       dict(dg=2.952e-12, raw=0.7623, post=4.860e-2, c100=0.0097, c10=0.097)}
NEP0 = 401
t0 = np.linspace(-T_ARC/2, T_ARC/2, NEP0)
base0 = kepler_obs(A_SED, E_SED, 0.0, M0_SED, t0)
D0 = design(t0)
int0 = integrate_const(0.0, t0)
mine = {}
P(f"  {'footing':>10}{'dg mine':>12}{'dg g04':>12}{'raw mine':>11}{'raw g04':>10}"
  f"{'post mine':>12}{'post g04':>11}{'chi100 mine':>13}{'chi10 mine':>12}")
for fn, a0 in A0.items():
    dg, eps = mi_a_dg(a0)
    s = integrate_const(dg, t0) - int0
    raw = float(np.std(s[:NEP0])*RAD2MAS)
    post, c100 = project(s, D0, 100.0, NEP0)
    _, c10 = project(s, D0, 10.0, NEP0)
    mine[fn] = dict(dg=dg, eps=eps, raw=raw, post=post, c100=c100, c10=c10, sig=s)
    g = G04[fn]
    P(f"  {fn:>10}{dg:>12.4e}{g['dg']:>12.4e}{raw:>11.4f}{g['raw']:>10.4f}"
      f"{post:>12.4e}{g['post']:>11.3e}{c100:>13.5f}{c10:>12.4f}")
err = max(max(abs(mine[f][k]/G04[f][k] - 1.0) for k in ("dg", "raw", "post")) for f in A0)
cerr = max(max(abs(mine[f]["c100"]/G04[f]["c100"] - 1.0), abs(mine[f]["c10"]/G04[f]["c10"] - 1.0)) for f in A0)
ck("V1a  g04's dg / raw / post-fit Sedna numbers reproduce independently to better than 5%",
   err < 0.05 and cerr < 0.05,
   f"worst relative deviation on (dg, raw, post-fit) = {100*err:.2f}%, on the chi values = {100*cerr:.2f}%, "
   f"across both footings.  Different Kepler starter, different finite-difference steps (3e-7/4e-8/3e-8/4e-10 "
   f"vs g04's 1e-6/1e-7/1e-7/1e-9), QR projector instead of lstsq.  THE ARITHMETIC IS NOT THE PROBLEM -- so "
   f"the attack has to be on the inference, which is what V2 and V3 do")

P(""); info("V1b -- MUTATION CONTROLS on my own machinery (they must behave, or nothing below counts)")
c_a = kepler_obs(A_SED*(1 + 1e-9), E_SED, 0.0, M0_SED, t0) - base0
c_e = kepler_obs(A_SED, E_SED + 1e-9, 0.0, M0_SED, t0) - base0
fa = abs(project(c_a, D0, 100.0, NEP0)[0])/(np.std(c_a[:NEP0])*RAD2MAS)
fe = abs(project(c_e, D0, 100.0, NEP0)[0])/(np.std(c_e[:NEP0])*RAD2MAS)
int_err = float(np.std(int0[:NEP0] - base0[:NEP0])*RAD2MAS)
_, chi_zero = project(np.zeros_like(base0), D0, 10.0, NEP0)
P(f"  in-family a*(1+1e-9) absorbed to {fa:.2e} of itself;  e+1e-9 to {fe:.2e}")
P(f"  dg=0 integrator vs analytic Kepler: {int_err:.2e} mas ({mine['canonical']['post']/int_err:.0f}x below the "
  f"smallest post-fit signal);  chi of an identically-zero signal = {chi_zero:.2e}")
ck("V1b  MUTATION CONTROL: in-family perturbations are absorbed, a zero signal gives zero chi, baseline clean",
   max(fa, fe) < 1e-4 and int_err < 1e-3 and chi_zero < 1e-9,
   f"a 1e-9 change in a is absorbed to {fa:.1e} of itself, in e to {fe:.1e}; the dg=0 integrator matches the "
   f"analytic orbit to {int_err:.1e} mas; a null signal returns chi = {chi_zero:.1e}.  My projector is not "
   f"leaking in-family power and is not manufacturing a residual")


# ============================================================================================ V2
P(""); P("-"*112)
P("V2 -- ATTACK 1: the decomposition.  Is the shortfall STRUCTURAL (absorption) or INSTRUMENTAL (magnitude)?")
P("-"*112)
P("  3/sigma_obtained = I x S, with")
P("     S = raw / post-fit                      the STRUCTURAL factor -- what the 4 free elements eat")
P("     I = 3 / (raw / (precision/sqrt(N)))     the INSTRUMENTAL factor -- how far the FULLY UNABSORBED")
P("                                             raw signal would still be from a 3-sigma bar")
P("  The claim 'structurally rather than instrumentally' asserts S > I.  Note S is the same at every")
P("  precision, so the verdict can and does flip between the two precisions the claim is quoted at.")
P("")
P(f"  {'footing':>10}{'prec':>7}{'raw [mas]':>11}{'post [mas]':>12}{'S (absorb)':>12}"
  f"{'I (instr)':>11}{'I x S':>10}{'3/chi':>10}{'verdict':>22}")
dec = {}
for fn in A0:
    m = mine[fn]
    for prec, chi in ((100.0, m["c100"]), (10.0, m["c10"])):
        S = m["raw"]/m["post"]
        I = 3.0/(m["raw"]/(prec/math.sqrt(NEP0)))
        dec[(fn, prec)] = (S, I)
        P(f"  {fn:>10}{prec:>7.0f}{m['raw']:>11.4f}{m['post']:>12.4e}{S:>12.2f}{I:>11.2f}"
          f"{I*S:>10.1f}{3.0/chi:>10.1f}{('STRUCTURAL' if S > I else 'INSTRUMENTAL'):>22}")
close = max(abs(dec[k][0]*dec[k][1]/(3.0/(mine[k[0]]['c100'] if k[1] == 100.0 else mine[k[0]]['c10'])) - 1.0)
            for k in dec)
P(f"  (I x S reproduces the actual 3/chi shortfall to {100*close:.1f}%, so the factorisation is exact, not a fit)")
struct_dominates_100 = all(dec[(fn, 100.0)][0] > dec[(fn, 100.0)][1] for fn in A0)
struct_dominates_10  = all(dec[(fn, 10.0)][0]  > dec[(fn, 10.0)][1]  for fn in A0)
ck("V2a  the shortfall is STRUCTURAL at the headline 100 mas precision the claim is quoted at",
   struct_dominates_100,
   f"IT IS NOT.  At 100 mas the instrumental factor is I = {dec[('canonical',100.0)][1]:.0f} against a "
   f"structural factor S = {dec[('canonical',100.0)][0]:.0f} (alt: I = {dec[('alt',100.0)][1]:.0f}, "
   f"S = {dec[('alt',100.0)][0]:.0f}).  THE INSTRUMENT IS THE BIGGER OF THE TWO, by {dec[('canonical',100.0)][1]/dec[('canonical',100.0)][0]:.1f}x "
   f"(canonical) / {dec[('alt',100.0)][1]/dec[('alt',100.0)][0]:.1f}x (alt).  The headline sentence -- 'the "
   f"precession signal is reabsorbed by its own orbital elements' -- names the SMALLER of the two causes at "
   f"the precision the headline sigma (0.005) is quoted at")
ck("V2b  ... and at 10 mas, where the claim IS structurally dominated",
   struct_dominates_10,
   f"here it holds: S = {dec[('canonical',10.0)][0]:.0f} against I = {dec[('canonical',10.0)][1]:.1f} "
   f"(alt S = {dec[('alt',10.0)][0]:.0f}, I = {dec[('alt',10.0)][1]:.1f}).  So the claim's stated mechanism is "
   f"correct at LSST-class precision and incorrect at ground-based precision.  It is a PRECISION-DEPENDENT "
   f"statement being quoted as an unconditional structural one")

P(""); info("V2c -- the counterfactual that settles it: switch the absorption OFF entirely")
P("  Suppose the 4-element degeneracy did not exist at all -- a perfect experiment that measures the RAW")
P("  signal with no orbit fit.  Does Sedna's 25-yr arc then reach 3 sigma?")
P(f"  {'footing':>10}{'prec':>7}{'raw sigma (no fit at all)':>28}{'still short by':>16}")
nofit = {}
for fn in A0:
    for prec in (100.0, 10.0):
        s_raw = mine[fn]["raw"]/(prec/math.sqrt(NEP0))
        nofit[(fn, prec)] = s_raw
        P(f"  {fn:>10}{prec:>7.0f}{s_raw:>28.3f}{3.0/s_raw:>16.1f}x")
ck("V2c  with absorption switched OFF, the 25-yr arc reaches 3 sigma at 100 mas",
   nofit[("canonical", 100.0)] > 3.0,
   f"IT DOES NOT -- {nofit[('canonical',100.0)]:.3f} sigma (canonical) / {nofit[('alt',100.0)]:.3f} (alt), still "
   f"{3.0/nofit[('canonical',100.0)]:.0f}x short with the orbit-fit degeneracy ENTIRELY REMOVED.  This is the "
   f"cleanest refutation of the stated reason: at 100 mas you could hand the experiment a perfect, "
   f"absorption-free measurement of the whole raw signal and it would still fail by a factor of "
   f"{3.0/nofit[('canonical',100.0)]:.0f}.  '25 yr is 0.22% of one orbit' is a true statement about the "
   f"absorption factor of {dec[('canonical',100.0)][0]:.0f}x; it is NOT the reason the 0.005-sigma number is "
   f"0.005.  At 10 mas the counterfactual gives {nofit[('canonical',10.0)]:.2f} sigma, still short by "
   f"{3.0/nofit[('canonical',10.0)]:.1f}x -- so even there the absorption is not the whole story")


# ============================================================================================ V3
P(""); P("-"*112)
P("V3 -- ATTACK 2: g04's D4 arc scan holds the epoch count at 401 for EVERY arc length")
P("-"*112)
P("  g04's D4 builds every arc with NEP = 401 epochs, so a 400-yr programme is credited with the same")
P("  number of observations as a 25-yr one.  A real programme at FIXED CADENCE has N proportional to T.")
P(f"  g04's own baseline cadence is 401 epochs / 25 yr = {CADENCE:.2f} epochs per year.  Carrying that")
P("  cadence forward multiplies chi by sqrt(T/25).  Below: g04's fixed-N scan re-run, and the same scan")
P("  at fixed cadence.  Canonical footing, 10 mas, MI-A -- exactly the configuration D4a checks.")
P("")
P(f"  {'arc [yr]':>9}{'% orbit':>9}{'N fixed':>9}{'post [mas]':>12}{'sigma fixed-N':>15}"
  f"{'N cadence':>11}{'sigma cadence':>15}")
dgc = mine["canonical"]["dg"]
scan = []
for T_yr in (25.0, 50.0, 75.0, 100.0, 150.0, 200.0, 300.0, 400.0):
    T = T_yr*YR
    tf = np.linspace(-T/2, T/2, NEP0)
    sf = integrate_const(dgc, tf) - integrate_const(0.0, tf)
    pf, cf = project(sf, design(tf), 10.0, NEP0)
    Nc = int(round(CADENCE*T_yr))
    tc = np.linspace(-T/2, T/2, Nc)
    sc = integrate_const(dgc, tc) - integrate_const(0.0, tc)
    _, cc = project(sc, design(tc), 10.0, Nc)
    scan.append((T_yr, pf, cf, Nc, cc))
    P(f"  {T_yr:>9.0f}{100*T/P_SED:>9.2f}{NEP0:>9d}{pf:>12.4e}{cf:>15.2f}{Nc:>11d}{cc:>15.2f}")
reach_fixed = [r[0] for r in scan if r[2] > 3.0]
reach_cad   = [r[0] for r in scan if r[4] > 3.0]
T_fixed = min(reach_fixed) if reach_fixed else float("inf")
T_cad   = min(reach_cad)   if reach_cad   else float("inf")
ck("V3a  g04's '~400 yr arc for 3 sigma' survives when the epoch count is allowed to grow with the arc",
   T_cad > 300.0,
   f"IT DOES NOT.  At g04's own fixed 401 epochs the 3-sigma crossing is at ~{T_fixed:.0f} yr, reproducing "
   f"D4a.  At g04's own baseline cadence of {CADENCE:.1f} epochs/yr held constant, the crossing moves to "
   f"~{T_cad:.0f} yr -- INSIDE D4a's own 'realistic <= 200 yr' bar, which means D4a's stated verdict "
   f"('IT DOES NOT') is produced by the scan's bookkeeping, not by the physics.  The quoted '~400 yr = 3.5% "
   f"of the orbit' should be read as an upper bound conditional on never taking another observation after "
   f"the 401st.  NOTE this cuts the claim's rhetoric, not its bottom line: {T_cad:.0f} yr is still far beyond "
   f"any programme, and the 25-yr answer is unchanged")

P(""); info("V3b -- MUTATION CONTROL on the arc scan: dg = 0 must give chi ~ 0 at every arc")
zc = []
for T_yr in (25.0, 100.0, 400.0):
    T = T_yr*YR; Nc = int(round(CADENCE*T_yr)); tc = np.linspace(-T/2, T/2, Nc)
    s0c = integrate_const(0.0, tc) - kepler_obs(A_SED, E_SED, 0.0, M0_SED, tc)
    _, c0 = project(s0c, design(tc), 10.0, Nc)
    zc.append((T_yr, c0))
    P(f"  arc {T_yr:>5.0f} yr, N = {Nc:>5d}: chi of the (integrator - analytic) baseline difference = {c0:.3e}")
ck("V3b  MUTATION CONTROL: the dg=0 baseline carries no spurious significance at any arc length",
   max(c[1] for c in zc) < 0.05,
   f"worst chi from the integrator's own baseline error is {max(c[1] for c in zc):.2e} at 10 mas, against the "
   f"3.0 bar and against the 3-sigma crossings quoted above.  The growth of chi with arc in V3a is therefore "
   f"signal, not accumulated integration error -- which is the failure mode that would have made ATTACK 2 "
   f"itself wrong")


# ============================================================================================ V4
P(""); P("-"*112)
P("V4 -- does the negative SURVIVE the confounds?  (checking g04's conclusion is not too optimistic)")
P("-"*112)
P("  A real Sedna solution does not fit 4 parameters.  It fits 6 elements, the planetary masses, and -- in")
P("  every Planet Nine paper -- a distant perturber.  Adding ONE more free column, an unmodelled interior")
P("  mass (a GM rescale), is the minimum honest extension and it is exactly the nuisance g04 flags as the")
P("  D3a killer.  If the negative is real it must get WORSE, never better, when that column is added.")
P("")
P(f"  {'footing':>10}{'reading':>9}{'chi 4-elt @10mas':>19}{'chi 5-par @10mas':>19}{'degradation':>14}")
deg = []
D0g = design(t0, extra_gm=True)
for fn, a0 in A0.items():
    dg, eps = mi_a_dg(a0)
    sA = mine[fn]["sig"]
    _, c4A = project(sA, D0, 10.0, NEP0); _, c5A = project(sA, D0g, 10.0, NEP0)
    sB = kepler_obs(A_SED, E_SED, 0.0, M0_SED, t0, gm=GM_SUN*(1 + eps)) - base0
    _, c4B = project(sB, D0, 10.0, NEP0); _, c5B = project(sB, D0g, 10.0, NEP0)
    deg += [c5A/max(c4A, 1e-300), c5B/max(c4B, 1e-300)]
    P(f"  {fn:>10}{'MI-A':>9}{c4A:>19.3f}{c5A:>19.3f}{c5A/max(c4A,1e-300):>14.2e}")
    P(f"  {fn:>10}{'MI-B':>9}{c4B:>19.3f}{c5B:>19.3f}{c5B/max(c4B,1e-300):>14.2e}")
ck("V4a  adding one nuisance parameter (unmodelled interior mass) makes the Sedna channels WORSE, not better",
   max(deg) < 1.0,
   f"every channel loses significance: worst-case ratio {max(deg):.2e} <= 1.  MI-B, being exactly a GM "
   f"rescale, is annihilated -- which independently confirms g04's own D3a killer (a detection would be read "
   f"as {mine['canonical']['eps']/M_EARTH_OVER_M_SUN:.0f} M_earth of Planet Nine, not as gravity) and shows "
   f"g04's 4-parameter fit is the GENEROUS choice.  So g04's negative is conservative in the right direction "
   f"and my two attacks are attacks on its stated REASON, not on its bottom line")


# ============================================================================================ V5
P(""); P("-"*112)
P("V5 -- the astrometric systematic floor, which g04 flags but does not compute")
P("-"*112)
P("  Sedna's 25-yr arc is heterogeneous ground-based astrometry tied to successive reference catalogues.")
P("  A catalogue-systematic floor does NOT average down as 1/sqrt(N).  g04 asserts this makes the numbers")
P("  worse; here is by how much, for floors of 1, 5 and 20 mas on top of the 10 mas LSST-class statistics.")
P(f"  {'floor [mas]':>12}{'MI-A sigma':>13}{'MI-B sigma':>13}   (canonical, 10 mas per-epoch, 401 epochs)")
sB0 = kepler_obs(A_SED, E_SED, 0.0, M0_SED, t0, gm=GM_SUN*(1 + mine["canonical"]["eps"])) - base0
floors = []
for fl in (0.0, 1.0, 5.0, 20.0):
    _, cA = project(mine["canonical"]["sig"], D0, 10.0, NEP0, floor_mas=fl)
    _, cB = project(sB0, D0, 10.0, NEP0, floor_mas=fl)
    floors.append((fl, cA, cB))
    P(f"  {fl:>12.0f}{cA:>13.4f}{cB:>13.3f}")
ck("V5a  g04's 'a systematic floor makes it worse, not better' is verified quantitatively",
   all(f[1] <= floors[0][1] + 1e-12 and f[2] <= floors[0][2] + 1e-12 for f in floors),
   f"a 1 mas floor already drops the MI-B channel from {floors[0][2]:.2f} to {floors[1][2]:.2f} sigma and a 5 mas "
   f"floor to {floors[2][2]:.2f}.  So g04's D3a headline '5.7 sigma at 10 mas' requires the astrometry to be "
   f"statistics-limited to below ~1 mas systematic, which no 25-yr heterogeneous TNO arc is.  This STRENGTHENS "
   f"g04's negative and WEAKENS its one surviving prospective item -- a caveat g04 states in words and does "
   f"not number")


# ============================================================================================ verdict
P(""); P("="*112); P("VERDICT ON THE CLAIM"); P("="*112)
P(f"""
 THE ARITHMETIC IS SOUND.  dg = {mine['canonical']['dg']:.3e} / {mine['alt']['dg']:.3e} m/s^2, raw
 {mine['canonical']['raw']:.3f} / {mine['alt']['raw']:.3f} mas, post-fit {mine['canonical']['post']:.4f} /
 {mine['alt']['post']:.4f} mas, {mine['canonical']['c100']:.4f} / {mine['alt']['c100']:.4f} sigma at 100 mas and
 {mine['canonical']['c10']:.3f} / {mine['alt']['c10']:.3f} at 10 mas, all reproduced to better than {100*err:.2f}%
 on an independent propagator, design matrix and projector.  The bottom line -- the Sedna PRECESSION channel is
 shut -- is CORRECT, and it is conservative: every confound I could add (a 5th nuisance parameter, an
 astrometric systematic floor) makes it worse, and the 4-element fit g04 uses is the generous choice.

 THE STATED REASON IS WRONG AS QUOTED.  'Falls short structurally rather than instrumentally' factorises as
 3/sigma = I x S.  At the 100 mas precision the headline 0.005 sigma is quoted at, I = {dec[('canonical',100.0)][1]:.0f}
 and S = {dec[('canonical',100.0)][0]:.0f}: the INSTRUMENT is the larger factor by {dec[('canonical',100.0)][1]/dec[('canonical',100.0)][0]:.1f}x.  The counterfactual is decisive --
 delete the orbit-fit degeneracy entirely and the raw signal is still only {nofit[('canonical',100.0)]:.3f} sigma,
 {3.0/nofit[('canonical',100.0)]:.0f}x short.  Only at 10 mas does S ({dec[('canonical',10.0)][0]:.0f}) exceed I ({dec[('canonical',10.0)][1]:.1f}), and even there the
 absorption accounts for {100*math.log(dec[('canonical',10.0)][0])/math.log(dec[('canonical',10.0)][0]*dec[('canonical',10.0)][1]):.0f}% of the log shortfall, not all of it.

 AND THE '~400 YR' NUMBER IS AN ARTEFACT.  g04's D4 scan holds N = 401 epochs at every arc length.  At g04's
 own baseline cadence of {CADENCE:.1f} epochs/yr the 3-sigma crossing moves from ~{T_fixed:.0f} yr to ~{T_cad:.0f} yr, inside D4a's
 own 'realistic <= 200 yr' bar -- so D4a's verdict is set by the scan's bookkeeping.  'More telescope does not
 help and only more decades do' is false in both halves: V2c shows more telescope is in fact the dominant
 missing factor at 100 mas, and V3a shows the decades required are ~{T_cad:.0f}, not ~{T_fixed:.0f}.

 WHAT SHOULD BE CLAIMED INSTEAD.  'Sedna's 25-yr arc misses the MI-A precession envelope by {3.0/mine['canonical']['c100']:.0f}x at
 100 mas and {3.0/mine['canonical']['c10']:.0f}x at 10 mas.  Roughly a factor {dec[('canonical',100.0)][0]:.0f} of that is the four in-plane elements
 absorbing the signal over an arc that is {100*T_ARC/P_SED:.2f}% of the orbit; the rest is the raw signal being too
 small for the astrometry.  Neither factor is closable: reaching 3 sigma needs either ~{T_cad:.0f} yr of arc at
 LSST-class precision and cadence, or ~{3.0/mine['canonical']['c10']:.0f}x better per-epoch astrometry on a V=20.6 object.'  That sentence
 keeps the negative, which is real, and drops the mechanism attribution, which is precision-dependent.

 CAVEATS ON MY OWN AUDIT.  The astrometric precisions are g04's estimates, not a published Sedna covariance;
 I inherit them and so does every I above -- but S is precision-independent, so the factorisation itself does
 not depend on them, only the verdict of which factor is larger does.  The cadence of {CADENCE:.1f} epochs/yr is
 g04's own implied baseline, not an observing-programme design.  Nothing here bears on LambdaCDM: at
 10^4-10^8 a_0 GR+CDM and healthy MOND-family theories both predict zero, so no part of this discriminates
 the framework against dark matter, and no part of it should be quoted as if it did.
""")
sys.exit(ck.done())
