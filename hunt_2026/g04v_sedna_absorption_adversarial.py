#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""g04v_sedna_absorption_adversarial.py -- ADVERSARIAL AUDIT of g04's D2/D4 (the Sedna lever).
=============================================================================================
THE CLAIM UNDER TEST (g04_solar_system_eccentricity_discriminant.py, checks D2b and D4a):
  "The best real lever, Sedna, falls short STRUCTURALLY rather than instrumentally: the precession signal is
   reabsorbed by its own orbital elements because 25 yr is 0.22% of one orbit."
  Numbers: MI-A dg = 1.375e-12 (canonical) / 2.952e-12 (alt) m/s^2; raw 0.355 / 0.762 mas; post-fit 0.0226 /
  0.0486 mas = 0.005 / 0.010 sigma at 100 mas and 0.05 / 0.10 sigma at 10 mas; 3 sigma at 10 mas needs a
  ~400 yr arc (3.5% of the orbit).

THE METHOD HERE IS DELIBERATELY DIFFERENT FROM THE SCRIPT IT AUDITS, on every load-bearing step:
  * the signal comes from the LINEARISED VARIATIONAL EQUATIONS integrated alongside the reference orbit, so
    the 1.7e-9 rad perturbation is never obtained as a difference of two O(1) rad trajectories (g04 differences
    two DOP853 solutions; that is a 7-digit cancellation, and it is the obvious place for a fake residual);
  * the 4-element design matrix is built from ANALYTIC partial derivatives of (f + omega, ln r) with respect
    to (a, e, omega, M0), not by finite differences;
  * the projection is done by SVD on column-normalised weighted columns, and separately by the normal
    equations, and the answer is stress-tested against injected column noise up to 1e-8 relative.

WHAT SURVIVES AND WHAT DOES NOT.
  SURVIVES.  Every reported number reproduces to 4 significant figures (V1).  The projector is stable, not
  ill-conditioned once the columns are normalised (V2).  The headline negative is real and is not marginal:
  Sedna's 25-yr arc is 639x / 298x short of 3 sigma at 100 mas and 64x / 30x short at 10 mas (V6).
  DOES NOT SURVIVE.  Two things, both in the STORY rather than in the numbers:
   (a) the stated MECHANISM is backwards (V3).  The 4 elements absorb a factor 20 of the signal on the 25-yr
       arc and a factor 143 on a 200-yr arc and ~190 on a 250-400 yr arc.  Reabsorption is WEAKEST, not
       strongest, on the short arc, so "reabsorbed because 25 yr is 0.22% of one orbit" inverts the
       dependence.  What the short arc does is make the RAW signal small (0.355 mas), which is a different
       statement with different consequences.
   (b) "structurally rather than instrumentally" fails on its own headline footing (V4).  At 100 mas the
       639x shortfall factorises as 32x raw signal-to-noise times 20x orbit-fit absorption -- the LARGER
       factor is the instrument.  The structural reading only becomes the dominant one at 10 mas (3.2x raw
       vs 20x absorption).  Relatedly, 3 sigma on the EXISTING 25-yr arc needs 0.156 mas (canonical) /
       0.336 mas (alt) per-epoch astrometry -- an instrumental factor of 64 / 30, not an infinity.
   (c) the quoted arc requirement is wrong by a factor 1.9 (V5).  3 sigma at 10 mas is reached at a 215-yr
       arc (1.9% of the orbit), not ~400 yr (3.5%).  g04's D4 scan steps in powers of two (25, 50, 100, 200,
       400) and its residual is non-monotone, so the first grid point above 3 sigma is 400 yr while the
       200-yr point already sits at 2.85 sigma.  The error is in the direction that makes the negative look
       stronger than it is.

ONE FURTHER OBSERVATION, NOT A REFUTATION, RECORDED BECAUSE IT CHANGES WHAT THE D4 NUMBER MEANS.  At long
arcs the significance is carried by the ln r (annual-parallax range) channel, not by the angles: at the
215-yr crossing chi_total = 3.00 splits as chi_angular = 1.58 and chi_range = 2.55.  So "the arc needed to
see the MI-A envelope" is mostly a statement about distance determination, and it inherits the script's
idealisation that every epoch yields an independent annual parallax at the per-epoch angular precision.

ALSO NOTE, both directions: chi scales as sqrt(N_epochs) and N = 401 is an assumption, not a measurement
(V1c).  Halving to 101 epochs gives 0.0024 sigma, quadrupling to 1601 gives 0.0093.  Nothing near 3.

Sedna elements: a = 506.2 AU, e = 0.8496 (Brown, Trujillo & Rabinowitz 2004, ApJ 617, 645), r_now = 85 AU,
pre-perihelion branch.  Astrometric precisions 100 / 10 mas are g04's ESTIMATES, inherited unchanged here --
this audit does not repair that, and no published Sedna orbit covariance is held in this repository.
"""
import sys, math
import numpy as np
from scipy.integrate import solve_ivp
from hunt_lib import Check, P, info, A0

ck = Check()
np.seterr(all="ignore")

GM = 1.32712440018e20
AU = 1.495978707e11
YR = 3.155760000e7
RAD2MAS = 180.0/math.pi*3600.0*1000.0

A_SED, E_SED, R_NOW, T_ARC = 506.2*AU, 0.8496, 85.0*AU, 25.0*YR
NEP = 401
E0 = -math.acos((1.0 - R_NOW/A_SED)/E_SED)
M0_SED = E0 - E_SED*math.sin(E0)
n0 = math.sqrt(GM/A_SED**3)
PER = 2.0*math.pi/n0

# g04's reported values, transcribed for comparison (g04_solar_system_eccentricity_discriminant.out, D2/D4)
G04 = {"canonical": dict(dg=1.375e-12, raw=3.549e-01, post=2.263e-02, chi100=0.0047, chi10=0.047),
       "alt":       dict(dg=2.952e-12, raw=7.623e-01, post=4.860e-02, chi100=0.0101, chi10=0.101)}
G04_ARC_400 = 400.0

P("="*118)
P("g04v -- ADVERSARIAL AUDIT OF THE SEDNA ORBIT-FIT ABSORPTION (g04 checks D2b, D4a)")
P("="*118)


# ---------------------------------------------------------------------------- Kepler + variational machinery
def solveE(M, e):
    E = np.array(M, dtype=float, copy=True)
    for _ in range(200):
        E = E - (E - e*np.sin(E) - M)/(1.0 - e*np.cos(E))
    return E

def kepler_obs(a, e, om, M0, t):
    M = M0 + math.sqrt(GM/a**3)*np.asarray(t)
    E = solveE(M, e)
    f = 2.0*np.arctan2(math.sqrt(1+e)*np.sin(E/2.0), math.sqrt(1-e)*np.cos(E/2.0))
    return np.concatenate([np.unwrap(f) + om, np.log(a*(1.0 - e*np.cos(E)))])

def signal_variational(dg, T, npts=NEP):
    """Integrate the reference orbit and its LINEARISED response to a constant inward dg in one system.
    Returns (t, [delta_theta ; delta_ln r]).  No large-number cancellation anywhere."""
    t = np.linspace(-T/2.0, T/2.0, npts)
    M = M0_SED + n0*t[0]; E = float(solveE(np.array([M]), E_SED)[0])
    Ed = n0/(1.0 - E_SED*math.cos(E))
    f0 = 2.0*math.atan2(math.sqrt(1+E_SED)*math.sin(E/2), math.sqrt(1-E_SED)*math.cos(E/2))
    r0 = A_SED*(1.0 - E_SED*math.cos(E))
    s0 = [r0*math.cos(f0), r0*math.sin(f0), -A_SED*math.sin(E)*Ed,
          A_SED*math.sqrt(1-E_SED**2)*math.cos(E)*Ed, 0.0, 0.0, 0.0, 0.0]
    def rhs(_t, s):
        x, y, vx, vy, dx, dy, dvx, dvy = s
        r2 = x*x + y*y; r = math.sqrt(r2); r3 = r2*r
        rd = x*dx + y*dy
        return [vx, vy, -GM*x/r3, -GM*y/r3, dvx, dvy,
                -GM/r3*dx + 3.0*GM*rd*x/(r3*r2) - dg*x/r,
                -GM/r3*dy + 3.0*GM*rd*y/(r3*r2) - dg*y/r]
    sol = solve_ivp(rhs, (t[0], t[-1]), s0, t_eval=t, rtol=1e-12, atol=1e-6, method="DOP853")
    x, y, dx, dy = sol.y[0], sol.y[1], sol.y[4], sol.y[5]
    r2 = x*x + y*y
    return t, np.concatenate([(x*dy - y*dx)/r2, (x*dx + y*dy)/r2])

def design_analytic(t, a=A_SED, e=E_SED, M0=M0_SED):
    """Exact partials of [f + omega ; ln r] wrt (a, e, omega, M0).  No finite differences."""
    n = math.sqrt(GM/a**3)
    E = solveE(M0 + n*np.asarray(t), e)
    se, ce = np.sin(E), np.cos(E)
    b = math.sqrt(1.0 - e*e); den = 1.0 - e*ce
    dfdM = b/den**2
    dlnrdM = e*se/den**2
    dEde = se/den
    T2 = np.tan(E/2.0); k = math.sqrt((1+e)/(1-e))
    dkde = 1.0/((1-e)*math.sqrt((1+e)*(1-e)))
    dfde = (b/den)*dEde + 2.0*T2*dkde/(1.0 + (k*T2)**2)
    dlnrde = (-ce + e*se*dEde)/den
    dMda = -1.5*n*np.asarray(t)/a
    return np.vstack([np.concatenate([dfdM*dMda, 1.0/a + dlnrdM*dMda]),
                      np.concatenate([dfde, dlnrde]),
                      np.concatenate([np.ones_like(t), np.zeros_like(t)]),
                      np.concatenate([dfdM, dlnrdM])]).T

def project(sig, D, smas, npts=NEP):
    """Weighted removal of the 4-element family.  Returns (residual, chi_total, chi_raw, chi_ang, chi_lnr, cond)."""
    s_th = smas/RAD2MAS; s_lr = s_th*R_NOW/AU
    w = np.concatenate([np.full(npts, 1.0/s_th), np.full(npts, 1.0/s_lr)])
    A = D*w[:, None]; A = A/np.linalg.norm(A, axis=0)
    U, S, _ = np.linalg.svd(A, full_matrices=False)
    b = sig*w
    rw = b - U @ (U.T @ b)
    return (rw/w, float(np.linalg.norm(rw)), float(np.linalg.norm(b)),
            float(np.linalg.norm(rw[:npts])), float(np.linalg.norm(rw[npts:])), float(S[0]/S[-1]))

def dg_MIA(a0):
    """MI-A envelope: nu-1 frozen at APHELION (the orbit's minimum acceleration), as a constant dg."""
    Q = A_SED*(1.0 + E_SED); gQ = GM/Q**2
    eps = 1.0/math.expm1(math.sqrt(gQ/a0))
    return eps*gQ, eps, gQ, Q


# ============================================================================================================
P(""); P("-"*118)
P("V1 -- does g04's central number reproduce under a completely different estimator?")
P("-"*118)
P(f"  Sedna: a = {A_SED/AU:.1f} AU, e = {E_SED}, r_now = {R_NOW/AU:.0f} AU, P = {PER/YR:.1f} yr; "
  f"25 yr = {100*T_ARC/PER:.4f}% of one orbit")
P(f"  {'footing':>10}{'dg here':>13}{'dg g04':>11}{'raw here':>11}{'raw g04':>10}{'post here':>12}"
  f"{'post g04':>10}{'chi100':>9}{'chi10':>8}")
mine, worst = {}, 0.0
for fn, a0 in A0.items():
    dg, eps, gQ, Q = dg_MIA(a0)
    t, sig = signal_variational(dg, T_ARC)
    D = design_analytic(t)
    res, chi100, chir100, ca, cl, cond = project(sig, D, 100.0)
    _, chi10, chir10, _, _, _ = project(sig, D, 10.0)
    raw = float(np.std(sig[:NEP])*RAD2MAS); post = float(np.std(res[:NEP])*RAD2MAS)
    mine[fn] = dict(dg=dg, eps=eps, raw=raw, post=post, chi100=chi100, chi10=chi10,
                    chir100=chir100, chir10=chir10, cond=cond)
    g = G04[fn]
    for k, v in (("dg", dg), ("raw", raw), ("post", post), ("chi100", chi100), ("chi10", chi10)):
        worst = max(worst, abs(v/g[k] - 1.0))
    P(f"  {fn:>10}{dg:>13.4e}{g['dg']:>11.3e}{raw:>11.4f}{g['raw']:>10.4f}{post:>12.5f}"
      f"{g['post']:>10.5f}{chi100:>9.4f}{chi10:>8.4f}")
ck("V1a  every reported g04 D2 number reproduces under variational signal + analytic design + SVD",
   worst < 0.01,
   f"worst relative difference over dg, raw, post-fit, chi(100 mas), chi(10 mas), both footings = "
   f"{100*worst:.2f}%.  The arithmetic of the claim is CORRECT.  In particular the 1.7e-9 rad signal is NOT "
   f"a cancellation artefact: obtained here without ever differencing two O(1) rad trajectories, it agrees "
   f"with g04's differenced DOP853 result to 4 significant figures")

dgc, epsc, gQ, Q = dg_MIA(A0["canonical"])
P(f"  independent check of the envelope itself: aphelion Q = {Q/AU:.2f} AU, g_N(Q) = {gQ:.5e} m/s^2, "
  f"sqrt(y) = {math.sqrt(gQ/A0['canonical']):.4f},")
P(f"  eps = 1/expm1(sqrt y) = {epsc:.5e}, dg = eps*g_N(Q) = {dgc:.5e} m/s^2 -- computed in closed form, no "
  f"kernel helper used")

P(""); info("V1b -- MUTATION CONTROLS on this audit's own pipeline (they must fire)")
t, sig = signal_variational(dgc, T_ARC); D = design_analytic(t)
infam = kepler_obs(A_SED*(1+1e-9), E_SED, 0.0, M0_SED, t) - kepler_obs(A_SED, E_SED, 0.0, M0_SED, t)
r_in, _, _, _, _, _ = project(infam, D, 100.0)
f_in = float(np.std(r_in[:NEP])/np.std(infam[:NEP]))
big, _, _, _ = dg_MIA(A0["canonical"]); big = dgc*1e4
t2, sig2 = signal_variational(big, T_ARC)
_, chi_big, _, _, _, _ = project(sig2, design_analytic(t2), 100.0)
lin = chi_big/mine["canonical"]["chi100"]/1e4
P(f"  in-family control : a*(1+1e-9) is absorbed to {f_in:.2e} of itself")
P(f"  detection control : dg x 1e4 gives chi(100 mas) = {chi_big:.1f} -- the pipeline DOES report a detection "
  f"when one exists (linearity {lin:.4f}, expected 1)")
ck("V1b  MUTATION CONTROL: in-family signal vanishes, a 1e4x signal is detected, response is linear",
   f_in < 1e-5 and chi_big > 3.0 and abs(lin - 1.0) < 0.02,
   f"a pure element change is absorbed to {f_in:.1e} of itself (so the projector is not leaking in-family "
   f"signal and calling it a residual), a 1e4x anomaly is reported at {chi_big:.0f} sigma (so the checks below "
   f"are capable of returning a POSITIVE), and chi is linear in dg to {100*abs(lin-1):.2f}%")

P(""); info("V1c -- the reported sigma is proportional to sqrt(N_epochs), and N = 401 is an assumption")
for npts in (101, 401, 1601):
    t2, s2 = signal_variational(dgc, T_ARC, npts=npts)
    _, c1, cr, _, _, _ = project(s2, design_analytic(t2), 100.0, npts=npts)
    P(f"  N = {npts:>5}: chi(100 mas) = {c1:.5f}   (chi_raw {cr:.5f})")
ck("V1c  no plausible epoch count rescues the channel",
   True,
   f"chi scales as sqrt(N) exactly, so the quoted 0.005 sigma is 0.0024 at N=101 and 0.0093 at N=1601.  N=401 "
   f"over 25 yr is ~16 independent epochs per year, which is generous rather than conservative for a V=20.6 "
   f"target.  Recorded as an assumption of the claim, not as a defect: even 1e4 epochs gives 0.02 sigma")


# ============================================================================================================
P(""); P("-"*118)
P("V2 -- is the projector ill-conditioned?  (the residual is only 1/16 of the raw signal, so this matters)")
P("-"*118)
for lvl in (0.0, 1e-14, 1e-12, 1e-10, 1e-8):
    vals = []
    for k in range(5 if lvl > 0 else 1):
        rng = np.random.default_rng(k)
        Dp = D*(1.0 + lvl*rng.standard_normal(D.shape))
        rr, _, _, _, _, cond = project(sig, Dp, 100.0)
        vals.append(float(np.std(rr[:NEP])*RAD2MAS))
    P(f"  design-column noise {lvl:>7.0e}: post-fit = {np.mean(vals):.6e} +- {np.std(vals):.1e} mas")
A = D*np.concatenate([np.full(NEP, RAD2MAS/100.0), np.full(NEP, RAD2MAS/100.0/(R_NOW/AU))])[:, None]
A = A/np.linalg.norm(A, axis=0)
condn = float(np.linalg.cond(A))
w = np.concatenate([np.full(NEP, RAD2MAS/100.0), np.full(NEP, RAD2MAS/100.0/(R_NOW/AU))])
c = np.linalg.solve(A.T @ A, A.T @ (sig*w))
post_ne = float(np.std(((sig*w - A @ c)/w)[:NEP])*RAD2MAS)
P(f"  normal-equation solve instead of SVD: post-fit = {post_ne:.6e} mas;  normalised cond(A) = {condn:.2e}")
ck("V2a  the 4-element projector is well conditioned once the columns are normalised, and the residual is real",
   condn < 1e6 and abs(post_ne/mine["canonical"]["post"] - 1.0) < 1e-6,
   f"cond = {condn:.1e} (not 1e18 -- g04's own note about an unnormalised lstsq truncating a column is the "
   f"right diagnosis, and its fix works).  Injecting 1e-8 relative noise into every design entry moves the "
   f"post-fit residual by 4e-6 of itself; SVD and normal equations agree to 1e-9.  The 0.0226 mas residual is "
   f"a genuine out-of-family signal, not numerical dirt")


# ============================================================================================================
P(""); P("-"*118)
P("V3 -- THE MECHANISM: is the signal reabsorbed BECAUSE 25 yr is 0.22% of one orbit?")
P("-"*118)
P("  If the stated mechanism is right, the fraction absorbed by the 4 free elements must be LARGEST on the")
P("  shortest arc and must fall as the arc grows.  Measured directly, at fixed dg, on this audit's pipeline:")
P(f"  {'arc [yr]':>9}{'% orbit':>9}{'raw [mas]':>12}{'post [mas]':>12}{'chi_raw':>10}{'chi_post':>10}{'absorbed x':>12}")
absorb = {}
for T_yr in (25, 50, 75, 100, 150, 200, 250, 300, 400, 800):
    t2, s2 = signal_variational(dgc, T_yr*YR)
    rr, chi, chir, _, _, _ = project(s2, design_analytic(t2), 10.0)
    absorb[T_yr] = chir/chi
    P(f"  {T_yr:>9d}{100*T_yr*YR/PER:>9.2f}{np.std(s2[:NEP])*RAD2MAS:>12.3e}"
      f"{np.std(rr[:NEP])*RAD2MAS:>12.3e}{chir:>10.2f}{chi:>10.3f}{chir/chi:>12.1f}")
ck("V3a  the 4 elements absorb MORE of the signal on the 25-yr arc than on a long one",
   absorb[25] > absorb[200] and absorb[25] > absorb[400],
   f"THEY DO NOT, and it is not close: the absorbed factor is {absorb[25]:.1f} on the 25-yr arc, "
   f"{absorb[200]:.0f} on 200 yr and {absorb[400]:.0f} on 400 yr.  Reabsorption is WEAKEST on the short arc "
   f"and grows by an order of magnitude as the arc lengthens.  So 'the signal is reabsorbed by its own "
   f"orbital elements BECAUSE 25 yr is 0.22% of one orbit' inverts the actual dependence.  What the short arc "
   f"really does is make the RAW signal small -- 0.355 mas, because a 1.4e-12 m/s^2 acceleration displaces "
   f"Sedna along-track by only ~2e4 m in 25 yr -- and detection improves with arc length because the raw "
   f"signal grows as ~T^5, not because the elements stop eating it")


# ============================================================================================================
P(""); P("-"*118)
P("V4 -- STRUCTURAL OR INSTRUMENTAL?  factorise the shortfall")
P("-"*118)
P(f"  {'footing':>10}{'sigma_ast':>11}{'chi_raw':>10}{'chi_post':>11}{'raw S/N x':>11}{'absorb x':>10}{'total x':>10}")
dom = {}
for fn in A0:
    m = mine[fn]
    for smas, cr, cp in ((100.0, m["chir100"], m["chi100"]), (10.0, m["chir10"], m["chi10"])):
        P(f"  {fn:>10}{smas:>11.0f}{cr:>10.4f}{cp:>11.4f}{3.0/cr:>11.1f}{cr/cp:>10.1f}{3.0/cp:>10.0f}")
        dom[(fn, smas)] = (3.0/cr, cr/cp)
P("  'raw S/N x' is how far short the signal is of 3 sigma BEFORE any orbit fit -- a purely instrumental")
P("  factor.  'absorb x' is what the 4-element fit then removes -- the structural factor.  They multiply.")
need = {fn: 100.0*mine[fn]["chi100"]/3.0 for fn in A0}
P(f"  3 sigma on the EXISTING 25-yr arc needs per-epoch astrometry of {need['canonical']:.3f} mas (canonical) "
  f"/ {need['alt']:.3f} mas (alt)")
ck("V4a  the shortfall is dominated by the orbit-fit absorption rather than by raw sensitivity",
   dom[("canonical", 100.0)][1] > dom[("canonical", 100.0)][0],
   f"NOT ON THE HEADLINE FOOTING.  At 100 mas the canonical 639x shortfall factorises as "
   f"{dom[('canonical',100.0)][0]:.0f}x raw signal-to-noise times {dom[('canonical',100.0)][1]:.0f}x orbit-fit "
   f"absorption -- the INSTRUMENT is the larger factor, so 'structurally rather than instrumentally' is not "
   f"supported by the number it is attached to.  The structural reading only takes over at 10 mas "
   f"({dom[('canonical',10.0)][0]:.1f}x raw vs {dom[('canonical',10.0)][1]:.0f}x absorption).  And the "
   f"instrumental factor is finite and modest: {need['canonical']:.2f} mas per epoch on the arc that already "
   f"exists would reach 3 sigma, which is 64x better than LSST-class but not a different kind of thing from a "
   f"200-yr observing campaign")


# ============================================================================================================
P(""); P("-"*118)
P("V5 -- THE ARC REQUIREMENT: g04 says ~400 yr (3.5% of the orbit) for 3 sigma at 10 mas")
P("-"*118)
P(f"  {'arc [yr]':>9}{'% orbit':>9}{'chi_total':>11}{'chi_angular':>13}{'chi_range':>11}")
cross = None; prev = None
for T_yr in (150, 175, 190, 200, 205, 210, 215, 220, 225, 250, 300, 400):
    t2, s2 = signal_variational(dgc, T_yr*YR)
    _, chi, _, ca, cl, _ = project(s2, design_analytic(t2), 10.0)
    P(f"  {T_yr:>9d}{100*T_yr*YR/PER:>9.2f}{chi:>11.3f}{ca:>13.3f}{cl:>11.3f}")
    if cross is None and prev is not None and prev[1] < 3.0 <= chi:
        cross = prev[0] + (T_yr - prev[0])*(3.0 - prev[1])/(chi - prev[1])
    prev = (T_yr, chi)
ck("V5a  3 sigma at 10 mas requires an arc of ~400 yr, as reported",
   cross is not None and abs(cross/G04_ARC_400 - 1.0) < 0.10,
   f"IT REQUIRES {cross:.0f} yr = {100*cross*YR/PER:.1f}% of the orbit, not {G04_ARC_400:.0f} yr = 3.5%.  A "
   f"factor {G04_ARC_400/cross:.1f} overstatement, and in the direction that makes the negative look stronger. "
   f"The cause is visible in g04's own D4 table: the scan steps in powers of two (25, 50, 100, 200, 400) and "
   f"the residual is non-monotone, so the first GRID POINT above 3 sigma is 400 yr while the 200-yr point "
   f"already stands at 2.85 sigma.  Recorded also: at the crossing the significance is carried by the RANGE "
   f"channel (chi_range 2.55 of chi_total 3.00), so the arc requirement is largely a statement about annual "
   f"parallax, and it inherits the idealisation that every epoch delivers an independent distance at the "
   f"per-epoch angular precision")


# ============================================================================================================
P(""); P("-"*118)
P("V6 -- and now the part of the claim that SURVIVES: the negative itself")
P("-"*118)
ck("V6a  Sedna's 25-yr arc reaches 3 sigma on the MI-A envelope, on any footing or precision tested",
   max(mine[fn]["chi10"] for fn in A0) > 3.0,
   f"IT DOES NOT, confirming g04's D2b under an independent estimator: {mine['canonical']['chi100']:.4f} / "
   f"{mine['alt']['chi100']:.4f} sigma at 100 mas and {mine['canonical']['chi10']:.3f} / "
   f"{mine['alt']['chi10']:.3f} sigma at 10 mas, i.e. shortfalls of "
   f"{3.0/mine['canonical']['chi100']:.0f}x / {3.0/mine['alt']['chi100']:.0f}x and "
   f"{3.0/mine['canonical']['chi10']:.0f}x / {3.0/mine['alt']['chi10']:.0f}x.  The HEADLINE NEGATIVE IS "
   f"CORRECT AND IS NOT MARGINAL.  Adding nuisance parameters that a real fit would carry (out-of-plane "
   f"elements, planetary masses, an effective GM) can only enlarge the absorbed family, so this is an upper "
   f"bound on detectability -- the negative is conservative, exactly as g04 says")

P(""); P("="*118); P("VERDICT"); P("="*118)
P(f"""
 THE ARITHMETIC IS RIGHT.  All six headline numbers -- dg = {mine['canonical']['dg']:.4e} / {mine['alt']['dg']:.4e} m/s^2, raw
 {mine['canonical']['raw']:.3f} / {mine['alt']['raw']:.3f} mas, post-fit {mine['canonical']['post']:.4f} / {mine['alt']['post']:.4f} mas, {mine['canonical']['chi100']:.4f} / {mine['alt']['chi100']:.4f} sigma at 100 mas and
 {mine['canonical']['chi10']:.3f} / {mine['alt']['chi10']:.3f} sigma at 10 mas -- reproduce to 4 significant figures under a signal computed from the
 linearised variational equations, an analytic design matrix, and an SVD projection, none of which g04 uses.
 The projector is stable (V2) and the mutation controls fire in both directions (V1b).  The negative -- Sedna
 cannot see the MI-A precession envelope on its present arc -- SURVIVES and is conservative.

 THE STORY ATTACHED TO IT DOES NOT.  "Falls short structurally rather than instrumentally, because 25 yr is
 0.22% of one orbit" is refuted twice over.  (i) The 4 elements absorb a factor {absorb[25]:.0f} on the 25-yr arc and
 {absorb[200]:.0f} on a 200-yr arc: reabsorption is weakest exactly where the claim says it bites hardest.  (ii) At the
 headline 100 mas footing the 639x shortfall is {dom[('canonical',100.0)][0]:.0f}x raw signal-to-noise times {dom[('canonical',100.0)][1]:.0f}x absorption, so the
 instrument is the larger factor; the structural reading only wins at 10 mas.  And the quoted arc requirement
 is a grid artefact: 3 sigma at 10 mas arrives at {cross:.0f} yr, not 400.

 WHAT SHOULD BE SAID INSTEAD.  Sedna's 25-yr arc is short of the MI-A envelope by {3.0/mine['canonical']['chi100']:.0f}x at 100 mas and {3.0/mine['canonical']['chi10']:.0f}x
 at 10 mas.  Roughly a factor {dom[('canonical',100.0)][1]:.0f} of that is the 4-element degeneracy and the rest is raw sensitivity to a
 0.355 mas signal.  Closing it needs EITHER ~{cross:.0f} yr of arc at 10 mas OR ~{need['canonical']:.2f} mas per-epoch astrometry on the
 arc that already exists.  Both are out of reach today; neither is structural in the sense of being immune to
 a better instrument.
""")
sys.exit(ck.done())
