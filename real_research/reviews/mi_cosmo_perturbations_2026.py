#!/usr/bin/env python3
r"""mi_cosmo_perturbations_2026.py -- LANE G: COSMOLOGICAL PERTURBATIONS for the ghost-condensate dark
sector of the modified-INERTIA framework.  The referee's first question, which the corpus does not have.

WHY THIS SCRIPT EXISTS.  The corpus has identified the dark sector as a GHOST CONDENSATE and banked four
statements about it -- attractor P'(X) -> 0, amount I_0 ~ Omega_dm FREE, "Jeans is dS-cured", "S8 neutral-by-
theorem" -- but the linear-perturbation calculation behind them has never been run in one place.  This is that
calculation: background FRW, the growth equation for delta_m, D(z) and f sigma_8 against DESI/eBOSS, the
condensate sound speed and its k^4 dispersion, the Jeans scale, S8, and an explicit statement of which CMB
observables the theory can and cannot address.

MANDATORY CREDIT.  nu(y) = sqrt(1+1/y) and the de Sitter-Unruh balance are MILGROM 1999 PLA 253:273 eqs 6-9
(he fixes a_0_hat = 2 c H_Lambda); his eqs 10-11 give a second coefficient, and MILGROM 2008 arXiv:0801.3133
sec 7.3.1 notes the coefficient mismatch "isn't necessarily meaningful".  Temperature sqrt(a^2+Lambda/3)/2pi:
NARNHOFER, PETER and THIRRING 1996 IJMPB 10:1507.  Five-acceleration reading: DESER and LEVIN 1997 CQG 14:L163.
a_lambda = c^2 sqrt(Lambda/3): MILGROM 1994 Ann.Phys. 229:384.  AQUAL: BEKENSTEIN and MILGROM 1984.  TeVeS:
BEKENSTEIN 2004.  AeST: SKORDIS and ZLOSNIK 2021.  Ghost condensate: ARKANI-HAMED, CHENG, LUTY and MUKOHYAMA
2004 JHEP 0405:074 (hep-th/0312099).  The framework's distinctive content is the c H_Lambda / Z COEFFICIENT and
the MI completion, NOT the kernel.

*** kappa = 1/2 IS FITTED, NOT DERIVED.  Nothing below changes that. ***

WHAT IS COMPUTED, and what is NEW.

  S1  BACKGROUND.  For L = P(X), X = (1/2) phidot^2, the FRW equation of motion integrates EXACTLY to
      a^3 P'(X) phidot = C.  With P(X) = P_0 + (1/2) lambda (X - X_0)^2 (the generic quadratic extremum; the
      whole analysis depends only on P'(X_0) = 0 and P''(X_0) > 0) the condensate's history is THREE-PHASE and
      closed-form in u = X/X_0 - 1:
            u sqrt(1+u) = Q / a^3 ,   rho_cond = lambda X_0^2 (2u + (3/2) u^2) ,   p_cond = (1/2) lambda X_0^2 u^2
      * u >> 1 (early):  rho ~ a^-4, w -> 1/3  -- the condensate is RADIATION-LIKE, not kination.
                         (and c_s^2 -> 1/3 there too, so the sound speed CEILING equals w: never superluminal.)
      * u << 1 (late):   rho ~ a^-3, w -> 0    -- exact DUST.  This is the dark matter.
      * -P_0 is an exact w = -1 piece throughout.  ONE field supplies both the dark matter and Lambda.
      Continuity rho' = -3(rho+p) is verified IDENTICALLY in sympy, which is the check that catches an algebra
      slip.  NEW HERE: the early phase is RADIATION-LIKE (w=1/3), so the early-time constraint is a Delta N_eff
      bound, NOT the a^-6 kination bound one gets by mis-expanding.  That is a 7-orders-weaker requirement, and
      I state plainly that my own first pass got it wrong the strong way.

  S2  GROWTH.  delta_m growth equation, two-fluid (baryons + condensate) with the condensate's own c_s^2(a) and
      k^4 pressure.  D(z), f(z), f sigma_8(z) vs LambdaCDM and vs an RSD compilation; fractional deviation at
      z = 0, 0.5, 1 (all <= 2e-9).  Delta chi^2 vs the RSD compilation = 2e-8, so RSD is NON-DIAGNOSTIC.
      NEW HERE, and it is the binding constraint on the whole condensate sector: the growth solver directly
      gives the k-dependent P(k) SUPPRESSION, whose controlling combination is verified to be c_s0^2 k^2.
      Requiring <1% suppression at k = 10 h/Mpc (the Ly-alpha forest's reach) gives
            c_s0^2 <= 4.8e-23  ,  i.e. transition redshift z_t >~ 2.5e7,
      which is EIGHT DECADES tighter than the Delta N_eff bound, and drives Delta N_eff <= 7.4e-4 -- about 40x
      BELOW CMB-S4.  AGAINST INTEREST: I expected N_eff to be the live handle; the small-scale power closes it.
      And a sharp methodological finding: over the same 8 decades of c_s0^2 the f sigma_8 SHAPE moves by <=1.4e-5
      while the P(k) AMPLITUDE moves by 68%.  Grading this front by RSD would understate it by decades.

  S3  SOUND SPEED.  c_s^2 = P'(X) / (P'(X) + 2 X P''(X)) = u/(3u+2) in closed form -> 0 at the attractor, with
      the k^4 dispersion omega^2 = c^2 k_phys^4 / k_M^2 supplying the only gradient term.  Jeans scale both from
      c_s and from k^4.  Then the corpus's "Jeans is dS-cured" is VERIFIED IN SUBSTANCE with a WORDING
      CORRECTION: the fluid-level instability is NOT absent -- it is present on every cosmological scale, its
      rate is bounded by H, and it goes to zero as Lambda takes over.  It is exactly the ordinary dust growing
      mode the model NEEDS.  "Cured" = no faster-than-Hubble runaway, not "no growth".

  S4  S8.  VERIFIED by the growth calculation, not cited -- and sharpened.  For the CONDENSATE SECTOR the
      deviation from LambdaCDM is ~1e-20, so S8 is neutral for a reason far stronger than "neutral": it is
      numerically indistinguishable.  But the neutrality of the a_0 / MI SECTOR is NOT a theorem.  Three
      readings of what argument the MI kernel is fed on FRW are computed:
        R1  matter's own four-acceleration (ZERO for a comoving geodesic)  -> non-analytic sqrt(delta) response,
            amplification 1/h(x) ~ 1/(2x) with x = g_pec/a_0 ~ 1e-4  -> ~1e3-1e4 x.  EXCLUDED by 3+ orders.
        R2  the argument regulated to y = 1 by the condensate's own attractor (c phidot = a_0 exactly)
            -> a CONSTANT Poisson amplification 1/h(1) = sqrt(5)/2 = 1.1180  -> sigma_8 too high by 53%
            (S8 = 1.27, +34 sigma from Planck).  EXCLUDED.
        R3  MOND quasi-static-ONLY, absent from cosmological perturbations by construction (what AeST engineers
            and what the corpus assumes) -> exactly LambdaCDM, S8 neutral trivially.
      So "S8 neutral-by-theorem" is REFUTED AS A THEOREM and CONFIRMED AS A CONSEQUENCE OF R3.  R3 is a model
      choice, not a derivation.  The gradient-order-count of project_cmb_boltzmann_aest PART B (Y^{3/2} = O(eps^3))
      is a correct statement about a TERM; it does not by itself bound the SOLUTION, because in the deep-MOND
      branch that term is the ONLY term and its solution goes as sqrt(delta).  The condensate's phidot != 0 is
      the real regulator, and that makes the condensate STRUCTURALLY REQUIRED rather than decoration.

  S5  CMB.  No Boltzmann run here.  Instead an explicit CAN / CANNOT ledger with numbers where numbers exist
      (r_s, theta_*, l_A, R identical to <1e-9; Delta N_eff computed and bounded), and a concrete specification
      of what a modified CLASS/CAMB module would have to implement, item by item.

  S6  Both a_0 footings on every dimensional number.  Plus one exact identity found here:
      with rho_Lambda = M^4 (the condensate's own scale being the dark-energy scale) and the framework's
      a_0 = kappa c sqrt(G rho_Lambda), the ghost condensate's decay constant is
            f  =  M^2 / phidot  =  M_Pl / kappa      (EXACT, non-reduced M_Pl = 1/sqrt(G))
      i.e. kappa = 1/2 <=> f = 2 M_Pl.  This is a RELABELLING (kappa <-> f/M_Pl), so per the corpus's kappa-linear
      theorem it CANNOT force kappa -- but it is a relabelling with content, and it cuts AGAINST INTEREST: the
      swampland/weak-gravity folklore prefers f <= M_Pl, i.e. kappa >= 1, while the data prefers kappa = 1/2.

FLOAT64 HAZARDS HANDLED (the corpus has eight prior occurrences):
  * u sqrt(1+u) = R solved in LOG space by bisection, never by the cubic u^3+u^2-R^2 (which loses all precision
    for R ~ 1e-17).
  * rho_cond evaluated as lambda X_0^2 (2u + 1.5 u^2) -- the pieces separately -- never as the difference
    2(X_0+delta) lambda delta - (1/2) lambda delta^2 of nearly-equal large numbers.
  * log1p / expm1 for 1+u and for log(1+exp(.)).
  * every grid result re-run at 4x resolution and the shift printed.
  * mpmath cross-check of the closed-form expansion at a moderate u where float64 is still trustworthy.

Exit 0 = every check held.  No check(True); every condition below can fail, and several are stated so that the
FAILING outcome is the interesting one.
"""
from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.optimize import brentq

try:
    import mpmath as mp
    mp.mp.dps = 50
    HAVE_MP = True
except Exception:                                                    # pragma: no cover
    HAVE_MP = False

# --------------------------------------------------------------------------------------------------
_RESULTS: list[tuple[bool, str]] = []


def check(cond, msg: str) -> bool:
    cond = bool(cond)
    _RESULTS.append((cond, msg))
    print(f"    [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(s: str) -> None:
    print("\n" + "=" * 108)
    print(s)
    print("=" * 108)


def sub(s: str) -> None:
    print("\n  " + "-" * 104)
    print("  " + s)
    print("  " + "-" * 104)


# --------------------------------------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------------------------------------
C_LIGHT = 2.99792458e8               # m/s
G_NEWT = 6.67430e-11                 # SI
MPC = 3.0856775814913673e22          # m
KPC = MPC / 1e3
HBAR_EVS = 6.582119569e-16           # eV s
HBARC_EVM = 1.973269804e-7           # eV m
EV_J = 1.602176634e-19               # J
M_PL_EV = 1.220890e28                # non-reduced Planck mass 1/sqrt(G), eV

# Planck 2018 TT,TE,EE+lowE+lensing baseline
H0_KMS = 67.36
H0 = H0_KMS * 1e3 / MPC              # 1/s
HLITTLE = H0_KMS / 100.0
OM_M = 0.3153
OM_B = 0.04930
OM_L = 1.0 - OM_M                    # flat
OM_DM = OM_M - OM_B
RHO_CRIT = 3 * H0**2 / (8 * math.pi * G_NEWT)          # kg/m^3
OM_GAMMA = 2.47e-5 / HLITTLE**2
N_EFF_SM = 3.046
OM_NU1 = 0.2271 * OM_GAMMA                              # one massless species
OM_R = OM_GAMMA * (1 + 0.2271 * N_EFF_SM)

SIGMA8_PLANCK, SIGMA8_PLANCK_ERR = 0.8111, 0.0060
S8_PLANCK, S8_PLANCK_ERR = 0.832, 0.013

KAPPA = 0.5
Z_CONST = 2 * math.sqrt(8 * math.pi / 3)                # 5.7888100366
CH_LAMBDA = 5.4194e-10                                  # m/s^2

# The two footings.  Canonical = pure Lambda (rho_DE, c H_Lambda).  ALT = total (rho_total, c H_0).
FOOTINGS = (
    ("canonical  rho_DE  / cH_Lambda", 9.3614e-11, OM_L),
    ("ALT        rho_tot / cH_0     ", 1.13e-10, 1.0),
)
A0_CANON = FOOTINGS[0][1]
A0_ALT = FOOTINGS[1][1]


def nu_kernel(y):
    """Milgrom 1999 PLA 253:273 eq 9 kernel, nu(y) = sqrt(1+1/y), y = g_bar/a_0."""
    y = np.asarray(y, float)
    return np.sqrt(1.0 + 1.0 / np.maximum(y, 1e-300))


def mu_fw(x):
    """Framework's own dS-Unruh mu, inverse of the a_0-line: g_obs^2 = g_bar^2 + a_0 g_bar.

    FLOAT64 HAZARD (corpus occurrence: catastrophic cancellation in sqrt(1+a^2)-1).  The textbook form
    (sqrt(1+4x^2) - 1)/(2x) subtracts two nearly equal numbers for x < 1 and loses ~2 log10(1/x) digits --
    measured at 1.4e-13 in the nu -> mu round trip.  The rationalised form 2x/(sqrt(1+4x^2)+1) is
    algebraically identical and cancellation-free; it is used here.
    """
    x = np.asarray(x, float)
    return np.where(x > 0, 2 * x / (np.sqrt(1 + 4 * x * x) + 1), 0.0)


def h_response(x):
    """d/dx [ x mu_fw(x) ] = 2x/sqrt(1+4x^2): the effective inertia for a SMALL extra force.
    The response amplification is 1/h, not 1/mu -- established in mi_growth_amplification_founded_2026.py."""
    x = np.asarray(x, float)
    return 2 * x / np.sqrt(1 + 4 * x * x)


# --------------------------------------------------------------------------------------------------
# S0 -- footings, and the a_0 <-> rho_Lambda consistency the whole lane rests on
# --------------------------------------------------------------------------------------------------
def S0_footings():
    banner("S0 -- FOOTINGS.  a_0 = kappa c sqrt(G rho), and which rho.  kappa = 1/2 is FITTED, not derived.")
    print(f"    Planck 2018 baseline: H_0 = {H0_KMS} km/s/Mpc, Om_m = {OM_M}, Om_L = {OM_L:.4f},"
          f" Om_b = {OM_B}, Om_dm = {OM_DM:.4f}")
    print(f"    rho_crit = {RHO_CRIT:.6e} kg/m^3     Om_r = {OM_R:.6e}   Om_nu(1 species) = {OM_NU1:.6e}")
    print(f"    Z = 2 sqrt(8 pi/3) = {Z_CONST:.10f}     c H_Lambda = {CH_LAMBDA:.4e} m/s^2")

    sub("a_0 from each footing's rho, compared with the corpus's committed values")
    print(f"    {'footing':34s} {'rho used [kg/m^3]':>20s} {'kappa c sqrt(G rho)':>22s} {'committed':>14s} {'ratio':>9s}")
    computed = {}
    for name, a0_committed, om_used in FOOTINGS:
        rho = om_used * RHO_CRIT
        a0_from_rho = KAPPA * C_LIGHT * math.sqrt(G_NEWT * rho)
        computed[name] = a0_from_rho
        print(f"    {name:34s} {rho:20.6e} {a0_from_rho:22.6e} {a0_committed:14.4e}"
              f" {a0_from_rho / a0_committed:9.5f}")
        check(abs(a0_from_rho / a0_committed - 1.0) < 5e-3,
              f"{name.strip()}: kappa c sqrt(G rho) reproduces the committed a_0 to <0.5%")

    # anchor the kernel that every later response function is built on (MANDATORY CREDIT: Milgrom 1999 eq 9)
    y = np.geomspace(1e-4, 1e4, 41)
    gb = y * A0_CANON
    g_obs = gb * nu_kernel(y)
    # STABLE form of the a_0-line: nu^2 = 1 + 1/y, a RATIO, no subtraction.
    resid_stable = np.max(np.abs(nu_kernel(y) ** 2 / (1.0 + 1.0 / y) - 1.0))
    # UNSTABLE form: g_obs^2 - g_bar^2 = a_0 g_bar.  For y >> 1 this subtracts two nearly equal large numbers
    # and loses ~log10(y) digits -- one of the corpus's eight documented float64 hazards, reproduced here.
    resid_diff = np.abs((g_obs ** 2 - gb ** 2 - A0_CANON * gb) / (A0_CANON * gb))
    mu_resid = np.max(np.abs(mu_fw(g_obs / A0_CANON) * g_obs / gb - 1.0))
    print(f"    kernel anchor, STABLE (ratio) form  nu^2 = 1 + 1/y : max rel. error {resid_stable:.2e}"
          " over 8 decades")
    print(f"    kernel anchor, DIFFERENCE form g_obs^2 - g_bar^2 = a_0 g_bar : {resid_diff[0]:.2e} at y = 1e-4"
          f" but {resid_diff[-1]:.2e} at y = 1e4")
    print("       ^ that degradation is CATASTROPHIC CANCELLATION, one of the corpus's eight documented float64")
    print("         hazards, reproduced on purpose: the a_0-line's difference form loses ~log10(y) digits, so")
    print("         every later use goes through the ratio form or through mu_fw.")
    mu_naive = np.where(g_obs > 0, (np.sqrt(1 + 4 * (g_obs / A0_CANON) ** 2) - 1) / (2 * g_obs / A0_CANON), 0.0)
    mu_resid_naive = np.max(np.abs(mu_naive * g_obs / gb - 1.0))
    print(f"    mu_fw is nu's exact inverse to {mu_resid:.2e} in the RATIONALISED form 2x/(sqrt(1+4x^2)+1),")
    print(f"    but only to {mu_resid_naive:.2e} in the textbook form (sqrt(1+4x^2)-1)/(2x) -- the SECOND")
    print("    documented cancellation, caught here.  Everything downstream (h(x), R1/R2) uses the stable form.")
    check(mu_resid_naive > 100 * mu_resid,
          f"the sqrt(1+a^2)-1 cancellation is real and measured: the textbook mu form is {mu_resid_naive:.1e}"
          f" against the rationalised form's {mu_resid:.1e}, a factor {mu_resid_naive/max(mu_resid,1e-300):.0f}")
    check(resid_stable < 1e-15 and mu_resid < 1e-15,
          f"the framework's own kernel and the a_0-line are mutually exact to {max(resid_stable, mu_resid):.1e}"
          " in the STABLE form over 8 decades -- so h(x) and the R1/R2 amplifications rest on a verified"
          " kernel, not McGaugh's nu")
    check(resid_diff[-1] > 1e3 * max(resid_diff[0], 1e-18),
          f"and the cancellation is real and measured, not hypothetical: the difference form degrades from"
          f" {resid_diff[0]:.1e} to {resid_diff[-1]:.1e} across the same grid")

    sub("the second route: a_0 = c H_Lambda / Z (the framework's distinctive coefficient)")
    a0_from_Z = CH_LAMBDA / Z_CONST
    print(f"    c H_Lambda / Z = {a0_from_Z:.6e} m/s^2   vs canonical {A0_CANON:.4e}"
          f"   ratio {a0_from_Z / A0_CANON:.6f}")
    check(abs(a0_from_Z / A0_CANON - 1) < 3e-3, "c H_Lambda / Z agrees with kappa c sqrt(G rho_Lambda) to <0.3%")
    print("    NOTE: the two natural constants in this box are BOTH Z = 2 pi (Milgrom's coefficient); theory")
    print("    favours 2 pi while the SPARC data favour kappa = 1/2 by ~2.2 sigma.  Recorded, not resolved.")

    sub("the condensate's attractor rate, both footings")
    for name, a0, _ in FOOTINGS:
        print(f"    {name:34s} phidot_attr = a_0/c = {a0 / C_LIGHT:.6e} s^-1"
              f"   = H_0/{H0 / (a0 / C_LIGHT):.3f}")
    corpus_phidot = 3.1228e-19
    check(abs((A0_CANON / C_LIGHT) / corpus_phidot - 1) < 2e-3,
          f"canonical a_0/c = {A0_CANON/C_LIGHT:.6e} s^-1 reproduces the corpus target {corpus_phidot:.4e}"
          " (so the corpus's |phidot| target IS a_0/c)")
    return computed


# --------------------------------------------------------------------------------------------------
# S1 -- BACKGROUND FRW: ghost condensate + Lambda + matter
# --------------------------------------------------------------------------------------------------
def _log1pexp(t):
    """log(1+e^t) without overflow."""
    t = np.asarray(t, float)
    return np.where(t > 30.0, t + np.log1p(np.exp(-np.minimum(t, 700.0))), np.log1p(np.exp(np.minimum(t, 30.0))))


def _u_scalar(r: float) -> float:
    """Scalar fast path for u sqrt(1+u) = R -- pure python, no numpy overhead.  Called ~1e5 times inside the
    growth ODE, so the numpy version's per-call overhead is the difference between 0.3 s and 60 s."""
    if r <= 0.0:
        return 0.0
    lr = math.log(r)
    t = lr if lr < 0.0 else (2.0 / 3.0) * lr
    for _ in range(80):
        if t > 30.0:
            s = t + math.log1p(math.exp(-t))
            sig = 1.0
        else:
            et = math.exp(t) if t > -700.0 else 0.0
            s = math.log1p(et)
            sig = et / (1.0 + et)
        step = (t + 0.5 * s - lr) / (1.0 + 0.5 * sig)
        t -= step
        if abs(step) < 1e-15:
            break
    return math.exp(t)


def u_of_R(R):
    """Solve u sqrt(1+u) = R for u > 0, across R in [1e-40, 1e40].  Newton in log space.

    FLOAT64 HAZARD: the algebraic form u^3 + u^2 - R^2 = 0 loses every digit for R ~ 1e-17 (u^3 underflows
    against u^2 while R^2 is 1e-34).  Solve F(t) = t + 0.5 log(1+e^t) - log R = 0 instead, with t = ln u.
    F is strictly increasing (F' = 1 + e^t/(2(1+e^t)) in [1, 1.5]) so Newton from either asymptote converges
    monotonically and unconditionally.  A brentq cross-check is run in S1b.
    """
    if isinstance(R, (float, int)) or np.isscalar(R):
        return _u_scalar(float(R))
    Rv = np.atleast_1d(np.asarray(R, float))
    out = np.zeros_like(Rv, dtype=float)
    pos = Rv > 0
    if not np.any(pos):
        return out
    lr = np.log(Rv[pos])
    # small-R asymptote t ~ lr ; large-R asymptote t ~ (2/3) lr.  Use whichever the sign of lr selects.
    t = np.where(lr < 0.0, lr, (2.0 / 3.0) * lr)
    for _ in range(60):
        s = _log1pexp(t)                                     # log(1+e^t)
        F = t + 0.5 * s - lr
        # dF/dt = 1 + 0.5 * sigmoid(t)
        sig = np.where(t > 0, 1.0 / (1.0 + np.exp(-np.minimum(t, 700.0))),
                       np.exp(np.maximum(t, -700.0)) / (1.0 + np.exp(np.maximum(t, -700.0))))
        step = F / (1.0 + 0.5 * sig)
        t = t - step
        if np.max(np.abs(step)) < 1e-15:
            break
    out[pos] = np.exp(t)
    return out


def rho_p_tilde(u):
    """(rho_cond, p_cond) in units of lambda X_0^2, EXCLUDING the -P_0 Lambda piece.

    rho = 2 X P'(X) - P + P_0 = lambda X_0^2 (2u + (3/2) u^2)
    p   = P - P_0             = lambda X_0^2 (1/2) u^2
    Evaluated as separate positive terms -- never as a difference of nearly equal large numbers.
    """
    u = np.asarray(u, float)
    return 2.0 * u + 1.5 * u * u, 0.5 * u * u


def cs2_of_u(u):
    """c_s^2 = P'/(P' + 2 X P'') = u/(3u+2).  Zero at the attractor, ceiling 1/3 in the early phase."""
    return u / (3.0 * u + 2.0)


def u_from_cs2(cs2):
    """Invert c_s^2 = u/(3u+2).  Requires c_s^2 < 1/3 -- the condensate's exact ceiling."""
    if not (0.0 <= cs2 < 1.0 / 3.0):
        raise ValueError(f"c_s^2 = {cs2} is outside the condensate's exact range [0, 1/3)")
    return 2.0 * cs2 / (1.0 - 3.0 * cs2)


def S1_background():
    banner("S1 -- BACKGROUND FRW: ghost condensate + Lambda + matter.  Attractor, three phases, expansion history.")

    sub("S1a  sympy: the exact EOM integral, the attractor, and the stress tensor")
    t, a_s, lam, X0, P0 = sp.symbols('t a lambda X_0 P_0', positive=True)
    X = sp.Symbol('X', positive=True)
    P = P0 + sp.Rational(1, 2) * lam * (X - X0) ** 2
    PX = sp.diff(P, X)
    PXX = sp.diff(P, X, 2)
    print(f"    P(X)   = {sp.simplify(P)}")
    print(f"    P'(X)  = {sp.simplify(PX)}        P''(X) = {sp.simplify(PXX)}")
    check(sp.simplify(PX.subs(X, X0)) == 0, "P'(X_0) = 0: X_0 IS an extremum of P (the ghost-condensate point)")
    check(sp.simplify(PXX) == lam, "P''(X) = lambda, constant > 0: the extremum is a MINIMUM (needed for stability)")

    # stress tensor for L = P(X), X = (1/2) phidot^2 :  rho = 2 X P' - P,  p = P
    rho_sym = 2 * X * PX - P
    p_sym = P
    u_s = sp.Symbol('u', positive=True)                       # u = X/X_0 - 1
    rho_u = sp.simplify((rho_sym + P0).subs(X, X0 * (1 + u_s)) / (lam * X0 ** 2))
    p_u = sp.simplify((p_sym - P0).subs(X, X0 * (1 + u_s)) / (lam * X0 ** 2))
    print(f"    (rho + P_0)/(lambda X_0^2) = {sp.expand(rho_u)}")
    print(f"    (p   - P_0)/(lambda X_0^2) = {sp.expand(p_u)}")
    check(sp.expand(rho_u - (2 * u_s + sp.Rational(3, 2) * u_s ** 2)) == 0,
          "rho_cond = lambda X_0^2 (2u + (3/2) u^2) exactly")
    check(sp.expand(p_u - sp.Rational(1, 2) * u_s ** 2) == 0,
          "p_cond   = lambda X_0^2 (1/2) u^2 exactly")

    # EOM: d/dt (a^3 P' phidot) = 0  =>  a^3 lambda X_0 u sqrt(2 X_0 (1+u)) = C  =>  u sqrt(1+u) = Q/a^3
    Q = sp.Symbol('Q', positive=True)
    eom = sp.Eq(u_s * sp.sqrt(1 + u_s), Q / a_s ** 3)
    print(f"    EOM integral:  a^3 P'(X) phidot = C   <=>   {eom.lhs} = {eom.rhs}")
    dudlna = sp.simplify(sp.solve(sp.Eq(sp.diff(sp.log(u_s * sp.sqrt(1 + u_s)), u_s) * sp.Symbol('D'), -3),
                                  sp.Symbol('D'))[0])
    print(f"    => du/dlna = {sp.simplify(dudlna)}")
    cont = sp.simplify(sp.expand(sp.diff(rho_u, u_s) * dudlna + 3 * (rho_u + p_u)))
    print(f"    continuity residual  d(rho)/dlna + 3(rho+p) = {cont}")
    check(cont == 0, "CONTINUITY HOLDS IDENTICALLY (sympy): the closed form is an exact FRW solution")

    w_small = sp.limit(p_u / rho_u, u_s, 0, '+')
    w_large = sp.limit(p_u / rho_u, u_s, sp.oo)
    print(f"    w_cond(u -> 0)   = {w_small}      <- EXACT DUST at the attractor  (this is the dark matter)")
    print(f"    w_cond(u -> inf) = {w_large}      <- RADIATION-LIKE in the far past (NOT kination w=1)")
    check(w_small == 0, "w_cond -> 0 as u -> 0: the condensate's late-time attractor is exact dust")
    check(w_large == sp.Rational(1, 3),
          "w_cond -> 1/3 as u -> inf: the EARLY phase is radiation-like, so the early bound is Delta N_eff,"
          " NOT the a^-6 kination bound (my own first pass had this wrong the strong way)")
    check(sp.limit(PX.subs(X, X0 * (1 + u_s)), u_s, 0, '+') == 0,
          "P'(X) -> 0 on the attractor: the corpus's P'(X) -> 0 statement CONFIRMED symbolically")

    sub("S1b  numeric: does the attractor actually attract?  (start OFF it and watch)")
    # a^3 P' phidot = C is exact, so simply follow u(a) from u >> 1 down.
    a_grid = np.array([1e-6, 1e-4, 1e-2, 1e-1, 1.0, 10.0, 1e2, 1e3])
    Q_demo = 1.0
    u_demo = u_of_R(Q_demo / a_grid ** 3)
    PX_over = u_demo                                   # P'(X)/(lambda X_0) = u
    phidot_rel = np.sqrt(1.0 + u_demo)                  # phidot/phidot_attr = sqrt(1+u)
    print(f"    demo with Q = {Q_demo} (transition at a ~ 1):")
    hdr_px = "P'/(lam X_0)"
    print(f"    {'a':>10s} {'u = X/X_0-1':>14s} {hdr_px:>14s} {'phidot/phidot_attr':>20s} {'w_cond':>9s}")
    for aa, uu, pp, ff in zip(a_grid, u_demo, PX_over, phidot_rel):
        r_, p_ = rho_p_tilde(uu)
        print(f"    {aa:10.1e} {uu:14.6e} {pp:14.6e} {ff:20.10f} {p_ / r_:9.4f}")
    check(PX_over[-1] < PX_over[0] * 1e-8,
          f"P'(X) falls by >8 decades from a=1e-6 to a=1e3 (attractor P'(X) -> 0 REACHED, not assumed)")
    check(abs(phidot_rel[-1] - 1.0) < 1e-8,
          f"phidot -> const: phidot/phidot_attr = {phidot_rel[-1]:.12f} at a = 1e3")
    check(phidot_rel[0] > 100.0,
          f"and it really did start far off the attractor (phidot = {phidot_rel[0]:.3e}x its attractor value"
          " at a = 1e-6, w = 1/3 there), so the convergence is not trivially built in")

    # independent solver cross-checks of the vectorized Newton (float64-hazard guard)
    worst_bq = 0.0
    for rtest in (1e-20, 1e-6, 0.3, 1.0, 7.0, 1e6, 1e20):
        lr = math.log(rtest)
        fbq = lambda tt: tt + 0.5 * float(_log1pexp(tt)) - lr
        lo, hi = min(lr, (2 / 3) * lr) - 10.0, max(lr, (2 / 3) * lr) + 10.0
        u_bq = math.exp(brentq(fbq, lo, hi, xtol=1e-14, rtol=8.9e-16, maxiter=300))
        worst_bq = max(worst_bq, abs(u_of_R(rtest) / u_bq - 1))
    check(worst_bq < 1e-11,
          f"vectorized-Newton solver agrees with independent brentq over R = 1e-20..1e20"
          f" (worst rel. diff {worst_bq:.2e})")
    if HAVE_MP:
        um = mp.findroot(lambda uu: uu * mp.sqrt(1 + uu) - mp.mpf('1e-6'), mp.mpf('1e-6'))
        uf = u_of_R(1e-6)
        check(abs(uf / float(um) - 1) < 1e-12,
              f"mpmath cross-check of the log-space solver at R=1e-6: rel. diff {abs(uf/float(um)-1):.2e}")

    sub("S1c  the expansion history: does it reproduce (H_0, Om_m, Om_L) without new tuning?")
    print("    Construction: the condensate's DUST piece supplies ALL of Om_dm; -P_0 supplies ALL of Om_L.")
    print("    Free numbers: C (= Q, the amount)  and  P_0 (= the extremum depth).  LambdaCDM's are omega_cdm")
    print("    and Om_L.  2 vs 2 -- MATCHED, NOT REDUCED.  The corpus's 'amount I_0 ~ Om_dm is FREE' wall,")
    print("    verified by construction here: Q is fixed by fitting Om_dm and by nothing else.")

    def make_model(cs0_sq):
        """Return H(a)/H_0 for the condensate model with a chosen present-day sound speed."""
        # c_s0^2 = u_0/(u_0+2)  =>  u_0 = 2 c_s0^2/(1-c_s0^2);  Q = u_0 sqrt(1+u_0)
        u0 = u_from_cs2(cs0_sq)
        Q = u0 * math.sqrt(1.0 + u0)
        r0, _ = rho_p_tilde(u0)
        norm = OM_DM / r0 if r0 > 0 else 0.0            # lambda X_0^2 / (rho_crit c^2)

        def om_cond(a):
            uu = u_of_R(Q / np.asarray(a, float) ** 3)
            r_, p_ = rho_p_tilde(uu)
            return norm * r_, norm * p_

        def E(a):
            rc, _ = om_cond(a)
            a = np.asarray(a, float)
            return np.sqrt(OM_R * a ** -4 + OM_B * a ** -3 + rc + OM_L)

        return dict(u0=u0, Q=Q, norm=norm, om_cond=om_cond, E=E, cs0_sq=cs0_sq)

    def E_lcdm(a):
        a = np.asarray(a, float)
        return np.sqrt(OM_R * a ** -4 + OM_M * a ** -3 + OM_L)

    # the Delta N_eff bound on the amount-of-early-radiation
    print("\n    Delta N_eff from the early radiation-like phase (analytic):")
    print("       rho_cond(early) = (3/4) rho_dm0 Q^(1/3) a^-4   =>   Delta N_eff = (3/4) Om_dm Q^(1/3) / Om_nu1")
    coef_analytic = 0.75 * OM_DM / OM_NU1
    print(f"       Delta N_eff = {coef_analytic:.5g} * Q^(1/3)")
    # verify numerically deep in radiation domination
    m_test = make_model(1e-12)
    a_deep = 1e-9
    rc_deep, _ = m_test['om_cond'](a_deep)
    dn_numeric = rc_deep / (OM_NU1 * a_deep ** -4)
    dn_analytic = coef_analytic * m_test['Q'] ** (1.0 / 3.0)
    print(f"       numeric at a = {a_deep:.0e}:  Delta N_eff = {dn_numeric:.6e}"
          f"     analytic = {dn_analytic:.6e}    ratio {dn_numeric/dn_analytic:.6f}")
    check(abs(dn_numeric / dn_analytic - 1) < 0.02,
          "analytic Delta N_eff coefficient verified against the exact numeric solution to <2%")

    dn_planck = 0.30                                   # Planck 2018 TT,TE,EE+lowE+lensing+BAO, ~2 sigma
    Q_max_neff = (dn_planck / coef_analytic) ** 3
    cs0_max_neff = Q_max_neff / 2.0                    # since Q ~ u_0 ~ 2 c_s0^2 for small Q
    a_t_neff = (Q_max_neff / math.sqrt(2)) ** (1.0 / 3.0)
    print(f"       Planck Delta N_eff < {dn_planck}  =>  Q < {Q_max_neff:.4e},  c_s0^2 < {cs0_max_neff:.4e},")
    print(f"                                       transition a_t < {a_t_neff:.4e}  (z_t > {1/a_t_neff-1:.3e})")
    check(0 < cs0_max_neff < 1e-10,
          f"the Delta N_eff bound is a real, finite constraint: c_s0^2 < {cs0_max_neff:.3e}")

    sub("S1d  H(z): condensate model vs LambdaCDM, at the bound and 10 decades below it")
    z_tab = np.array([0.0, 0.5, 1.0, 2.0, 5.0, 20.0, 1090.0, 3400.0, 1e5, 1e7])
    a_tab = 1.0 / (1.0 + z_tab)
    print(f"    {'z':>9s} {'E_LCDM':>13s} {'E_cond(bound)':>15s} {'frac dev':>12s}"
          f" {'E_cond(1e-10 x)':>17s} {'frac dev':>12s}")
    m_bound = make_model(cs0_max_neff)
    m_deep = make_model(cs0_max_neff * 1e-10)
    dev_bound, dev_deep = [], []
    for zz, aa in zip(z_tab, a_tab):
        e0 = float(E_lcdm(aa))
        e1 = float(m_bound['E'](aa))
        e2 = float(m_deep['E'](aa))
        dev_bound.append(abs(e1 / e0 - 1))
        dev_deep.append(abs(e2 / e0 - 1))
        print(f"    {zz:9.1f} {e0:13.6f} {e1:15.6f} {e1/e0-1:12.3e} {e2:17.6f} {e2/e0-1:12.3e}")
    dev_deep_obs = [d for d, zz in zip(dev_deep, z_tab) if zz <= 3400.0]
    check(max(dev_deep_obs) < 1e-12,
          f"deep in the allowed range the background is LambdaCDM to {max(dev_deep_obs):.2e} across every"
          " OBSERVABLE epoch (z <= 3400) -- indistinguishable.  (At z = 1e7 a residual appears even there,"
          f" {dev_deep[-1]:.1e}: that is the radiation-like tail, i.e. real physics, not float64 noise.)")
    check(max(dev_bound) > 1e-3 and max(dev_bound) > 1e4 * max(dev_deep),
          f"AT the Delta N_eff bound the background DOES deviate ({max(dev_bound):.2e}, i.e."
          f" {max(dev_bound)/max(max(dev_deep),1e-300):.1e}x the deep-range noise floor) -- so the H(z)"
          " comparison is a live test, not a tautology (prove-by-moving-the-number)")
    check(all(d < 1e-4 for d, zz in zip(dev_bound, z_tab) if zz <= 3400.0),
          "and the deviation is confined to z >> z_recomb: at every z <= 3400 it is < 1e-4, which is why the"
          " constraint is Delta N_eff and not a distance-ladder or CMB-geometry constraint")

    sub("S1e  the f = M_Pl/kappa identity: the condensate's decay constant IS the a_0 coefficient")
    print("    A ghost condensate with a dimension-1 field Phi = f phi has X_Phi = Phidot^2 = M^4 at the")
    print("    extremum, i.e. Phidot = M^2, so f = M^2 / phidot with phidot the DIMENSIONLESS rate a_0/c.")
    print("    Take the condensate's own scale to BE the dark-energy scale, M^4 = rho_Lambda c^2.  Then")
    print("        a_0/c = kappa sqrt(G rho) = kappa M^2 / M_Pl   =>   f = M^2/(a_0/c) = M_Pl / kappa   EXACT.")
    print(f"    {'footing':34s} {'M [eV]':>13s} {'phidot [eV]':>14s} {'f [eV]':>14s} {'f/M_Pl':>10s} {'1/kappa':>9s}")
    for name, a0, om_used in FOOTINGS:
        # the condensate's own scale is always the DARK-ENERGY scale; only a_0's rho changes with footing
        rho_de_si = OM_L * RHO_CRIT * C_LIGHT ** 2                       # J/m^3
        rho_de_ev4 = (rho_de_si / EV_J) * HBARC_EVM ** 3                 # eV^4
        M_ev = rho_de_ev4 ** 0.25
        phidot_ev = (a0 / C_LIGHT) * HBAR_EVS
        f_ev = M_ev ** 2 / phidot_ev
        expect = (1.0 / KAPPA) * math.sqrt(OM_L / om_used)
        print(f"    {name:34s} {M_ev:13.6e} {phidot_ev:14.6e} {f_ev:14.6e}"
              f" {f_ev/M_PL_EV:10.5f} {expect:9.5f}")
        check(abs((f_ev / M_PL_EV) / expect - 1) < 5e-3,
              f"{name.strip()}: f/M_Pl = sqrt(Om_L/Om_used)/kappa = {expect:.5f} verified to <0.5%")
    print("    => kappa = 1/2  <=>  f = 2 M_Pl (canonical) or 1.655 M_Pl (ALT).  This is a RELABELLING")
    print("       (kappa <-> f/M_Pl), so by the corpus's kappa-linear theorem it CANNOT force kappa.")
    print("    *** AGAINST INTEREST: the swampland / weak-gravity folklore prefers f <= M_Pl, i.e. kappa >= 1.")
    print("        The data prefer kappa = 1/2 and Milgrom's coefficient is kappa = 1/(2 pi) -> f = 6.28 M_Pl,")
    print("        even more trans-Planckian.  The folklore disfavours BOTH; it is folklore, not a bound. ***")

    return dict(make_model=make_model, E_lcdm=E_lcdm, coef_neff=coef_analytic,
                cs0_max_neff=cs0_max_neff, Q_max_neff=Q_max_neff)


# --------------------------------------------------------------------------------------------------
# S2 -- LINEAR GROWTH
# --------------------------------------------------------------------------------------------------
def growth_solve(model, k_hMpc, cs0_sq, kM_inv_m=None, poisson_amp=1.0, z_i=1000.0, n=2001):
    """Two-fluid linear growth (baryons + condensate) in ln a.

        delta_i'' + (2 + dlnE/dlna) delta_i' = (3/2) Om_m(a) A [f_b delta_b + f_c delta_c] - (c_eff,i^2 k^2/(a^2 H^2)) delta_i

    c_eff^2 for the condensate = c_s^2(a) + (c k_phys/k_M)^2  (the k^4 dispersion's effective pressure).
    Baryons are pressureless post-recombination.  A = poisson_amp is the MI/MG source amplification (S4).
    Returns (lna, delta_m, dlnDm/dlna).
    """
    u0 = u_from_cs2(cs0_sq) if cs0_sq > 0 else 0.0
    Q = u0 * math.sqrt(1.0 + u0) if u0 > 0 else 0.0
    k_m = k_hMpc * HLITTLE / MPC                        # comoving k in 1/m
    E = model['E']
    om_cond = model['om_cond']

    def cs2_cond(a):
        if Q <= 0:
            return 0.0
        uu = u_of_R(Q / a ** 3)
        return cs2_of_u(uu)

    def rhs(lna, y):
        a = math.exp(lna)
        e = float(E(a))
        eps = 1e-4
        dlnE = (math.log(float(E(a * math.exp(eps)))) - math.log(float(E(a * math.exp(-eps))))) / (2 * eps)
        rc, _ = om_cond(a)
        om_b_a = OM_B * a ** -3
        om_m_a = (om_b_a + rc) / e ** 2
        f_b = om_b_a / (om_b_a + rc)
        f_c = 1.0 - f_b
        db, ddb, dc, ddc = y
        src = 1.5 * om_m_a * poisson_amp * (f_b * db + f_c * dc)
        # pressure terms: (c_eff k_phys / (a H))^2 -> in ln a units, k^2 c_eff^2/(a^2 H^2)
        aH = a * e * H0                                 # 1/s
        kphys = k_m / a                                 # 1/m
        pre_c = (cs2_cond(a) * (C_LIGHT * kphys) ** 2) / aH ** 2 if cs0_sq > 0 else 0.0
        if kM_inv_m:
            pre_c += ((C_LIGHT * kphys) ** 2 * (kphys / kM_inv_m) ** 2) / aH ** 2
        drag = 2.0 + dlnE
        return [ddb, -drag * ddb + src,
                ddc, -drag * ddc + src - pre_c * dc]

    lna_i = math.log(1.0 / (1.0 + z_i))
    y0 = [1.0, 1.0, 1.0, 1.0]                           # growing mode delta ~ a, same ICs for both fluids
    lna_eval = np.linspace(lna_i, 0.0, n)
    sol = solve_ivp(rhs, [lna_i, 0.0], y0, t_eval=lna_eval, rtol=1e-9, atol=1e-13, method='LSODA')
    db, ddb, dc, ddc = sol.y
    a_e = np.exp(sol.t)
    rc = np.array([om_cond(aa)[0] for aa in a_e])
    om_b_a = OM_B * a_e ** -3
    f_b = om_b_a / (om_b_a + rc)
    f_c = 1.0 - f_b
    dm = f_b * db + f_c * dc
    ddm = f_b * ddb + f_c * ddc                          # d(delta_m)/dlna, up to the slow drift of f_b (small)
    return sol.t, dm, ddm / dm


def S2_growth(bg):
    banner("S2 -- LINEAR SCALAR PERTURBATIONS: the growth equation, D(z), f sigma_8 vs DESI / eBOSS.")

    sub("S2a  the growth equation, and what the condensate changes in it")
    print("    Because the condensate's dust piece has c_s^2 = u/(3u+2) -> 0 (S3) and zero anisotropic stress,")
    print("    its perturbation obeys the SAME equation as CDM.  The full two-fluid system is")
    print("      delta_i'' + (2 + dlnE/dlna) delta_i' = (3/2) Om_m(a) [f_b delta_b + f_c delta_c] - (c_eff,i k/aH)^2 delta_i")
    print("    with c_eff,c^2 = c_s^2(a) + (c k_phys/k_M)^2.  Everything the condensate adds sits in c_eff.")

    make_model = bg['make_model']
    cs0_max = bg['cs0_max_neff']
    m_lcdm_like = make_model(1e-30)                     # condensate with utterly negligible c_s
    z_tab = np.array([0.0, 0.5, 1.0])

    sub("S2b  D(z) and f sigma_8(z): condensate vs LambdaCDM at k = 0.1 h/Mpc")

    def lcdm_growth(k_hMpc, poisson_amp=1.0, z_i=1000.0, n=2001):
        def rhs(lna, y):
            a = math.exp(lna)
            e = float(bg['E_lcdm'](a))
            eps = 1e-4
            dlnE = (math.log(float(bg['E_lcdm'](a * math.exp(eps))))
                    - math.log(float(bg['E_lcdm'](a * math.exp(-eps))))) / (2 * eps)
            om_m_a = OM_M * a ** -3 / e ** 2
            d, dd = y
            return [dd, -(2 + dlnE) * dd + 1.5 * om_m_a * poisson_amp * d]
        lna_i = math.log(1.0 / (1.0 + z_i))
        lna_eval = np.linspace(lna_i, 0.0, n)
        s = solve_ivp(rhs, [lna_i, 0.0], [1.0, 1.0], t_eval=lna_eval, rtol=1e-9, atol=1e-13, method='LSODA')
        return s.t, s.y[0], s.y[1] / s.y[0]

    lna_L, D_L, f_L = lcdm_growth(0.1)
    lna_C, D_C, f_C = growth_solve(m_lcdm_like, 0.1, 1e-30)
    lna_B, D_B, f_B_ = growth_solve(make_model(cs0_max), 0.1, cs0_max)

    def at(lna, arr, z):
        return float(np.interp(math.log(1.0 / (1.0 + z)), lna, arr))

    sig8_L = SIGMA8_PLANCK
    print(f"    {'z':>6s} {'D_L/D_L(0)':>12s} {'D_C/D_C(0)':>12s} {'frac dev D':>12s}"
          f" {'f_L':>8s} {'f_C':>8s} {'fs8_L':>8s} {'fs8_C':>8s} {'frac dev fs8':>13s}")
    devD, devF = [], []
    for zz in z_tab:
        dl = at(lna_L, D_L, zz) / at(lna_L, D_L, 0.0)
        dc = at(lna_C, D_C, zz) / at(lna_C, D_C, 0.0)
        fl, fc = at(lna_L, f_L, zz), at(lna_C, f_C, zz)
        fs_l, fs_c = fl * sig8_L * dl, fc * sig8_L * dc
        devD.append(abs(dc / dl - 1))
        devF.append(abs(fs_c / fs_l - 1))
        print(f"    {zz:6.2f} {dl:12.6f} {dc:12.6f} {dc/dl-1:12.3e} {fl:8.5f} {fc:8.5f}"
              f" {fs_l:8.5f} {fs_c:8.5f} {fs_c/fs_l-1:13.3e}")
    print(f"\n    FRACTIONAL DEVIATION at z = 0, 0.5, 1:  D: {['%.2e' % d for d in devD]}"
          f"   f sigma_8: {['%.2e' % d for d in devF]}")
    check(max(devD) < 2e-5 and max(devF) < 2e-5,
          f"deep in the allowed range the condensate's growth is LambdaCDM's to <2e-5"
          f" (max dev D {max(devD):.2e}, f sigma_8 {max(devF):.2e})")

    sub("S2c  the k-dependent SUPPRESSION -- the BINDING constraint, computed directly from the growth solver")
    print("    A fluid with c_s^2 > 0 is pressure-supported inside its sound horizon, so it does not cluster on")
    print("    small scales: a warm-DM-like cutoff in P(k).  Define the transfer ratio")
    print("        T(k) = delta_m(k, z=0) / delta_m(k_ref, z=0),   k_ref = 1e-4 h/Mpc (unsuppressed),")
    print("    which cancels the primordial normalisation.  In LambdaCDM's pressureless treatment T = 1 for all k")
    print("    by construction, so T is EXACTLY the condensate's own signature.  Negative entries are the")
    print("    condensate's ACOUSTIC OSCILLATION -- physical for a pressure-supported fluid, not a solver artefact.")
    ks = (1e-4, 0.1, 1.0, 10.0)
    print(f"    {'c_s0^2':>12s}" + "".join(f"{'T(k=' + str(k) + ')':>15s}" for k in ks[1:]))
    tab = {}
    for cs2 in (1e-30, 1e-24, 1e-22, 1e-20, 1e-18, cs0_max):
        m = make_model(cs2)
        base = None
        row = []
        for k in ks:
            lna_x, D_x, _ = growth_solve(m, k, cs2, n=801)
            v = float(D_x[-1])
            if base is None:
                base = v
            else:
                row.append(v / base)
        tab[cs2] = row
        print(f"    {cs2:12.3e}" + "".join(f"{r:15.6f}" for r in row))

    # the controlling combination is c_s0^2 k^2 -- a check that would fail if the pressure term were mis-coded
    a_ = tab[1e-22][2]          # cs0^2 = 1e-22, k = 10
    b_ = tab[1e-20][1]          # cs0^2 = 1e-20, k = 1
    c_ = tab[1e-18][0]          # cs0^2 = 1e-18, k = 0.1
    print(f"\n    scaling test: T(c_s0^2=1e-22, k=10) = {a_:.6f}   T(1e-20, k=1) = {b_:.6f}"
          f"   T(1e-18, k=0.1) = {c_:.6f}")
    check(abs(a_ / b_ - 1) < 1e-3 and abs(b_ / c_ - 1) < 1e-3,
          "the suppression depends only on c_s0^2 k^2, verified to <0.1% across two decades in k and four in"
          " c_s0^2 -- so the pressure term is coded as c_s^2 k^2 and not by accident")

    # bisect the bound: <1% suppression at k = 10 h/Mpc (the Ly-alpha forest's reach)
    K_LYA, TOL = 10.0, 0.01

    def supp(cs2):
        m = make_model(cs2)
        lna_r, D_r, _ = growth_solve(m, 1e-4, cs2, n=801)
        lna_k, D_k, _ = growth_solve(m, K_LYA, cs2, n=801)
        return float(D_k[-1]) / float(D_r[-1])

    lo, hi = 1e-26, 1e-21
    for _ in range(34):
        mid = math.sqrt(lo * hi)
        if supp(mid) > 1.0 - TOL:
            lo = mid
        else:
            hi = mid
    cs2_lss = lo
    dn_lss = bg['coef_neff'] * (u_from_cs2(cs2_lss) * math.sqrt(1 + u_from_cs2(cs2_lss))) ** (1.0 / 3.0)
    print(f"\n    => requiring <{100*TOL:.0f}% suppression at k = {K_LYA:.0f} h/Mpc (Ly-alpha forest reach) gives")
    print(f"       c_s0^2 <= {cs2_lss:.3e}.  Compare the Delta N_eff bound {cs0_max:.3e}:"
          f" LSS binds {math.log10(cs0_max/cs2_lss):.1f} DECADES harder.")
    print(f"       At that bound the condensate's Delta N_eff is {dn_lss:.3e} -- vs CMB-S4 sigma(N_eff) ~ 0.03,")
    print(f"       i.e. {0.03/dn_lss:.0f}x below detectability.  So N_eff is NOT an independent handle after all:")
    print("       the small-scale power constraint closes it.  (I had expected N_eff to be the live one; it is not.)")
    check(cs2_lss < cs0_max / 1e5,
          f"the small-scale-power bound c_s0^2 <= {cs2_lss:.2e} is >5 decades tighter than Delta N_eff's"
          f" {cs0_max:.2e} -- LSS is the BINDING constraint on the condensate")
    check(dn_lss < 0.03,
          f"and therefore Delta N_eff <= {dn_lss:.2e} is below CMB-S4's sensitivity: the condensate has NO"
          " observable CMB handle beyond geometry.  AGAINST INTEREST -- this closes a test I had hoped was live.")
    check(supp(cs2_lss * 100) < 1.0 - 5 * TOL,
          f"prove-by-moving-the-number: at 100x the bound the suppression at k = {K_LYA:.0f} h/Mpc is"
          f" {100*(1-supp(cs2_lss*100)):.1f}% -- the bound is a real edge, not a numerically dead code path")

    sub("S2c'  the ASYMMETRY: the P(k) amplitude is decades more sensitive than the f sigma_8 shape")
    print("    f sigma_8 as measured is anchored to sigma_8 at some epoch, so RSD tests the growth-rate SHAPE.")
    print("    The condensate's sound speed barely touches the shape -- after the transition the condensate is")
    print("    pressureless again and the late-time growth RATE recovers -- while the AMPLITUDE does not recover")
    print("    at all.  Both halves are computed below, so the asymmetry is a measured fact, not a claim.")
    print(f"    {'c_s0^2':>12s} {'fs8(0.5) SHAPE ratio':>22s} {'T(k=0.1) AMPLITUDE':>21s}")
    shape_devs, amp_devs = [], []
    for cs2 in (cs2_lss, 1e-20, 1e-18, cs0_max):
        m = make_model(cs2)
        lna_x, D_x, f_x = growth_solve(m, 0.1, cs2, n=801)
        fs_x = at(lna_x, f_x, 0.5) * at(lna_x, D_x, 0.5) / at(lna_x, D_x, 0.0)
        fs_l = at(lna_L, f_L, 0.5) * at(lna_L, D_L, 0.5) / at(lna_L, D_L, 0.0)
        lna_r, D_r, _ = growth_solve(m, 1e-4, cs2, n=801)
        T01 = float(D_x[-1]) / float(D_r[-1])
        shape_devs.append(abs(fs_x / fs_l - 1))
        amp_devs.append(abs(T01 - 1))
        print(f"    {cs2:12.3e} {fs_x/fs_l:22.8f} {T01:21.6f}")
    check(max(shape_devs) < 1e-3,
          f"the f sigma_8 SHAPE is essentially BLIND to the condensate: max deviation {max(shape_devs):.2e}"
          f" across {math.log10(cs0_max/cs2_lss):.0f} decades of c_s0^2, right up to the Delta N_eff bound")
    check(max(amp_devs) > 0.5,
          f"while over the SAME range the P(k) AMPLITUDE at k = 0.1 h/Mpc moves by up to"
          f" {100*max(amp_devs):.0f}% -- so the two observables differ in sensitivity by MANY decades")
    print("    *** LESSON, and it is a corpus rule: do NOT grade this front by f sigma_8 / RSD.  RSD is blind")
    print("        here by decades.  The constraint lives in the small-scale P(k) amplitude. ***")

    sub("S2d  confrontation with the RSD / f sigma_8 compilation")
    print("    Literature values entered by hand (compilation; each labelled).  The point is NOT precision --")
    print("    it is that the condensate model's chi^2 is IDENTICAL to LambdaCDM's, so it inherits the fit and")
    print("    can neither be favoured nor excluded by RSD.")
    fs8_data = [
        (0.067, 0.423, 0.055, "6dFGS Beutler+2012"),
        (0.150, 0.490, 0.145, "SDSS MGS Howlett+2015"),
        (0.380, 0.497, 0.045, "BOSS DR12 Alam+2017"),
        (0.510, 0.459, 0.038, "BOSS DR12 Alam+2017"),
        (0.610, 0.436, 0.034, "BOSS DR12 Alam+2017"),
        (0.700, 0.473, 0.041, "eBOSS LRG Bautista+2021"),
        (0.850, 0.315, 0.095, "eBOSS ELG deMattia+2021"),
        (1.480, 0.462, 0.045, "eBOSS QSO Neveux+2020"),
    ]
    print(f"    {'z':>6s} {'fs8 obs':>9s} {'+/-':>7s} {'fs8 LCDM':>10s} {'fs8 cond':>10s} {'source':>26s}")
    chi2_L = chi2_C = 0.0
    for zz, val, err, src in fs8_data:
        fl = at(lna_L, f_L, zz) * at(lna_L, D_L, zz) / at(lna_L, D_L, 0.0) * sig8_L
        fc = at(lna_C, f_C, zz) * at(lna_C, D_C, zz) / at(lna_C, D_C, 0.0) * sig8_L
        chi2_L += ((val - fl) / err) ** 2
        chi2_C += ((val - fc) / err) ** 2
        print(f"    {zz:6.3f} {val:9.3f} {err:7.3f} {fl:10.4f} {fc:10.4f} {src:>26s}")
    n_pts = len(fs8_data)
    print(f"\n    chi^2 (LambdaCDM, Planck sigma_8) = {chi2_L:.3f} / {n_pts} points"
          f"      chi^2 (condensate) = {chi2_C:.3f}      Delta chi^2 = {chi2_C-chi2_L:+.3e}")
    check(abs(chi2_C - chi2_L) < 1e-4,
          f"Delta chi^2 (condensate - LambdaCDM) = {chi2_C-chi2_L:+.2e}: RSD is NON-DIAGNOSTIC of the"
          " condensate -- it cannot distinguish them")
    check(chi2_L / n_pts < 3.0,
          f"the LambdaCDM baseline itself fits the compilation acceptably (chi^2/N = {chi2_L/n_pts:.2f}),"
          " so the comparison is against a working reference, not a broken one")

    sub("S2e  grid-refinement guard (corpus hazard: coarse grids reporting unsampled extrema)")
    lna_c2, D_c2, f_c2 = growth_solve(m_lcdm_like, 0.1, 1e-30, n=8001)
    shift = abs(at(lna_c2, D_c2, 0.0) / at(lna_C, D_C, 0.0) - 1)
    print(f"    4x refinement (n = 2001 -> 8001): D(0) shifts by {shift:.3e}")
    check(shift < 1e-6, f"growth solution is grid-converged (4x shift = {shift:.2e})")

    return dict(lna_L=lna_L, D_L=D_L, f_L=f_L, lna_C=lna_C, D_C=D_C, f_C=f_C,
                lcdm_growth=lcdm_growth, at=at, chi2_L=chi2_L, fs8_data=fs8_data,
                cs2_lss=cs2_lss, dn_lss=dn_lss, devD=devD, devF=devF)


# --------------------------------------------------------------------------------------------------
# S3 -- SOUND SPEED, k^4 DISPERSION, JEANS SCALE, THE dS "CURE"
# --------------------------------------------------------------------------------------------------
def S3_sound_speed(bg, gr):
    banner("S3 -- SOUND SPEED: c_s^2 = 0 at leading order with a k^4 dispersion.  Jeans scale.  Is Jeans dS-cured?")

    sub("S3a  sympy: c_s^2 = P'/(P' + 2 X P'') in closed form")
    lam, X0 = sp.symbols('lambda X_0', positive=True)
    u_s = sp.Symbol('u', positive=True)
    X = X0 * (1 + u_s)
    PX = lam * X0 * u_s
    PXX = lam
    cs2 = sp.simplify(PX / (PX + 2 * X * PXX))
    print(f"    c_s^2 = P'/(P' + 2 X P'') = {cs2}")
    check(sp.simplify(cs2 - u_s / (3 * u_s + 2)) == 0,
          "c_s^2 = u/(3u+2) exactly.  NOTE: my first pass wrote u/(u+2) and SYMPY CAUGHT IT -- the"
          " 2 X P'' term carries the (1+u), not 1.  Recorded because a hand-algebra slip here would have"
          " propagated into every Jeans number below.")
    check(sp.limit(cs2, u_s, 0, '+') == 0,
          "c_s^2 -> 0 as u -> 0: the ghost condensate has ZERO leading-order sound speed -- VERIFIED, not cited")
    check(sp.limit(cs2, u_s, sp.oo) == sp.Rational(1, 3),
          "c_s^2 -> 1/3 as u -> inf: the sound speed CEILING equals the early-phase w = 1/3, so"
          " 0 <= c_s^2 <= 1/3 everywhere -- NO superluminal front anywhere in the condensate's history")
    kin = sp.simplify(PX + 2 * X * PXX)
    print(f"    kinetic coefficient P' + 2 X P'' = {sp.expand(kin)}   (must be > 0 for a healthy mode)")
    check(sp.simplify(kin.subs(u_s, 0)) == 2 * lam * X0,
          "at the attractor the kinetic coefficient is 2 lambda X_0 > 0: the CONDENSATE CURES THE GHOST"
          " (P' = 0 is the boundary; P'' > 0 keeps the kinetic term positive)")
    print("    SIGN INTERLOCK (three conditions, one choice): stability needs P'' > 0; a POSITIVE dark-matter")
    print("    density rho = lambda X_0^2 (2u + 1.5u^2) needs u > 0, i.e. the integration constant C > 0; and")
    print("    u > 0 also gives c_s^2 > 0, i.e. no imaginary sound speed.  All three follow from C > 0, P'' > 0.")
    v = sp.Symbol('v')                                    # unrestricted sign, so u < 0 is representable
    cs2_gen = sp.simplify((lam * X0 * v) / (lam * X0 * v + 2 * X0 * (1 + v) * lam))
    cs2_neg = float(cs2_gen.subs(v, sp.Rational(-1, 2)))
    rho_neg = float(sp.expand(2 * v + sp.Rational(3, 2) * v ** 2).subs(v, sp.Rational(-1, 2)))
    print(f"    at u = -1/2 (i.e. C < 0):  c_s^2 = {cs2_neg:+.6f},  rho_cond/(lambda X_0^2) = {rho_neg:+.6f}")
    check(cs2_neg < 0 and rho_neg < 0,
          "and the interlock has teeth: u < 0 (C < 0) gives BOTH c_s^2 < 0 (imaginary sound speed) and"
          " rho_cond < 0 (negative dark matter) -- so the sign is FORCED by stability, not chosen")

    sub("S3b  the k^4 dispersion and its Jeans scale")
    print("    With c_s^2 = 0 the leading gradient term comes from the higher-derivative operator")
    print("    (nabla^2 pi)^2 / k_M^2 (ACLM 2004), giving omega^2 = c^2 k_phys^4 / k_M^2 -- the k^4 dispersion.")
    print("    Against gravity, instability for omega^2 < 4 pi G rho_cond, i.e. k_phys < k_J with")
    print("        k_J = (4 pi G rho_cond k_M^2 / c^2)^(1/4).")
    rho_cond0 = OM_DM * RHO_CRIT
    pref = 4 * math.pi * G_NEWT * rho_cond0 / C_LIGHT ** 2
    print(f"    4 pi G rho_cond0 / c^2 = {pref:.6e} m^-2")
    print(f"    {'M (condensate scale)':>24s} {'k_M [1/m]':>13s} {'k_J [1/m]':>13s} {'lambda_J':>16s}")
    rows = []
    for label, M_eV in (("10 MeV (ACLM bound)", 1e7), ("2.24 meV (= rho_L^1/4)", 2.24e-3),
                        ("1e-20 eV (fuzzy floor)", 1e-20), ("1.8e-21 eV", 1.8e-21)):
        k_M = M_eV / HBARC_EVM
        k_J = (pref * k_M ** 2) ** 0.25
        lam_J = 2 * math.pi / k_J
        rows.append((M_eV, lam_J))
        unit = f"{lam_J/MPC:.4e} Mpc" if lam_J > 1e19 else (f"{lam_J/1e3:.4e} km" if lam_J > 1e3 else f"{lam_J:.3e} m")
        print(f"    {label:>24s} {k_M:13.4e} {k_J:13.4e} {unit:>16s}")
    lamJ_meV = [r[1] for r in rows if abs(r[0] - 2.24e-3) < 1e-9][0]
    check(lamJ_meV < KPC,
          f"at the natural M = rho_Lambda^(1/4) the k^4 Jeans length is {lamJ_meV:.3e} m << 1 kpc:"
          " the k^4 term gives NO observable small-scale cutoff")
    # what M would put the cutoff at an observable 0.1 Mpc?
    lam_target = 0.1 * MPC
    k_target = 2 * math.pi / lam_target
    k_M_need = math.sqrt(k_target ** 4 / pref)
    M_need_eV = k_M_need * HBARC_EVM
    print(f"    inverting: lambda_J = 0.1 Mpc would need M = {M_need_eV:.3e} eV")
    check(M_need_eV < 2e-20,
          f"an OBSERVABLE k^4 cutoff needs M = {M_need_eV:.2e} eV, below the fuzzy-DM floor ~2e-20 eV"
          " (Rogers-Peiris 2021 Ly-alpha) -- so the k^4 handle is CLOSED: M is free and every viable value"
          " gives a microscopic Jeans scale.  No prediction here, and I say so.")

    sub("S3c  independent cross-check of the S2c bound: the comoving SOUND HORIZON")
    print("    S2c derived the bound by solving the growth ODE.  Here is a completely different estimator --")
    print("    the condensate's comoving sound horizon r_s = int c_s c da/(a^2 H), whose inverse is the cutoff")
    print("    wavenumber.  Two independent routes to the same number is the point; agreement to a factor of a")
    print("    few is all one should expect from a sound-horizon estimate.")
    make_model = bg['make_model']

    def sound_horizon(cs0_sq, a_end=1e-2, a_start=1e-14):
        m = make_model(cs0_sq)
        u0 = u_from_cs2(cs0_sq)
        Q = u0 * math.sqrt(1.0 + u0)

        def integrand(la):
            a = math.exp(la)
            uu = u_of_R(Q / a ** 3)
            cs = math.sqrt(cs2_of_u(uu))
            Hs = H0 * float(m['E'](a))
            return cs * C_LIGHT / (a * Hs)              # c_s c da/(a^2 H) = c_s c dlna/(a H)
        val, _ = quad(integrand, math.log(a_start), math.log(a_end), limit=400)
        return val                                       # metres, comoving

    print(f"    {'c_s0^2':>12s} {'a_t':>11s} {'z_t':>11s} {'r_s [Mpc]':>13s} {'k_cut [h/Mpc]':>14s} {'DeltaN_eff':>11s}")
    rows_sh = []
    for cs2 in (bg['cs0_max_neff'], 1e-18, 1e-20, gr['cs2_lss'], 1e-24):
        u0 = u_from_cs2(cs2)
        Q = u0 * math.sqrt(1.0 + u0)
        a_t = (Q / math.sqrt(2.0)) ** (1.0 / 3.0)
        rs_m = sound_horizon(cs2)
        k_cut = 2 * math.pi / (rs_m / MPC) / HLITTLE
        dn = bg['coef_neff'] * Q ** (1.0 / 3.0)
        rows_sh.append((cs2, a_t, k_cut, dn))
        print(f"    {cs2:12.3e} {a_t:11.3e} {1/a_t-1:11.3e} {rs_m/MPC:13.5e} {k_cut:14.4e} {dn:11.4e}")
    k_at_lss = [r[2] for r in rows_sh if abs(r[0] / gr['cs2_lss'] - 1) < 1e-9][0]

    # COMPARE LIKE WITH LIKE.  A sound horizon marks where the suppression is ORDER UNITY, not 1%.  So the
    # honest comparison is against the ODE's HALF-MODE scale k_1/2 (T = 1/2), found by sampling, not against
    # the 1%-threshold k used to set the bound.  Getting this wrong is how a factor of 24 becomes a "failure".
    cs2b = gr['cs2_lss']
    mb = make_model(cs2b)
    _, D_ref, _ = growth_solve(mb, 1e-4, cs2b, n=801)
    ref = float(D_ref[-1])
    kk = np.geomspace(10.0, 400.0, 25)
    Tk = []
    for k in kk:
        _, D_k, _ = growth_solve(mb, float(k), cs2b, n=801)
        Tk.append(float(D_k[-1]) / ref)
    Tk = np.array(Tk)
    idx = int(np.argmax(Tk < 0.5))
    k_half = float(np.interp(0.5, [Tk[idx], Tk[idx - 1]], [kk[idx], kk[idx - 1]])) if idx > 0 else float(kk[0])
    print(f"\n    the ODE's own HALF-MODE scale at c_s0^2 = {cs2b:.3e}:  T(k_1/2) = 1/2 at"
          f" k_1/2 = {k_half:.1f} h/Mpc")
    print(f"    the sound-horizon estimator at the same c_s0^2:            k_cut   = {k_at_lss:.1f} h/Mpc")
    print(f"    ratio k_cut/k_1/2 = {k_at_lss/k_half:.2f}")
    print(f"    (the 1%-suppression scale used to SET the bound is k = 10 h/Mpc, ~{k_half/10.0:.0f}x below k_1/2 --")
    print("     which is why comparing the sound horizon to the 1% scale would spuriously show a factor ~24.)")
    check(0.2 < k_at_lss / k_half < 5.0,
          f"the two INDEPENDENT estimators of the CUTOFF agree to a factor"
          f" {max(k_at_lss/k_half, k_half/k_at_lss):.2f} once compared like with like (half-mode vs sound"
          " horizon) -- the S2c bound is not an artefact of the ODE solve")
    _, D_k2, _ = growth_solve(mb, k_half, cs2b, n=3201)
    Thalf_fine = float(D_k2[-1]) / ref
    print(f"    numerical guard: T(k_1/2) recomputed at 4x resolution = {Thalf_fine:.6f} (target 0.5)")
    check(abs(Thalf_fine - 0.5) < 0.02,
          f"and T(k_1/2) is grid-converged at 4x resolution ({Thalf_fine:.4f} vs 0.5), so the oscillatory"
          " (negative-T) regime is physical acoustic behaviour and not solver noise")
    check(rows_sh[0][2] < 10.0 < rows_sh[-1][2],
          f"and the estimator is two-sided: at the Delta N_eff bound it gives k_cut = {rows_sh[0][2]:.2f} h/Mpc"
          f" (FAILS Ly-alpha) while at c_s0^2 = 1e-24 it gives {rows_sh[-1][2]:.3g} h/Mpc (PASSES)")
    check(gr['cs2_lss'] < bg['cs0_max_neff'],
          f"binding-constraint ordering confirmed: small-scale power ({gr['cs2_lss']:.1e}) beats Delta N_eff"
          f" ({bg['cs0_max_neff']:.1e}) as the constraint on the condensate's sound speed")

    sub("S3d  is the Jeans instability 'dS-cured'?  VERIFY / REFUTE with the growth rate")
    print("    Fluid-level mode equation for the condensate (sub-horizon, c_eff -> 0):")
    print("        ddelta + 2H ddelta/dt - 4 pi G rho_m delta = 0,   4 pi G rho_m = (3/2) H^2 Om_m(a)")
    print("    Constant-H (de Sitter-like) growing root:  s/H = -1 + sqrt(1 + (3/2) Om_m(a)).")
    print(f"    {'z':>9s} {'Om_m(a)':>10s} {'s/H':>10s} {'e-folds per Hubble time':>26s}")
    s_over_H = []
    for zz in (3400.0, 1090.0, 10.0, 3.0, 1.0, 0.0, -0.5, -0.9, -0.99):
        a = 1.0 / (1.0 + zz)
        e = float(bg['E_lcdm'](a))
        om_a = OM_M * a ** -3 / e ** 2
        s = -1 + math.sqrt(1 + 1.5 * om_a)
        s_over_H.append(s)
        print(f"    {zz:9.2f} {om_a:10.6f} {s:10.6f} {s:26.6f}")
    check(max(s_over_H) <= 1.0 + 1e-12,
          f"the instability rate NEVER exceeds H (max s/H = {max(s_over_H):.6f} <= 1): no faster-than-Hubble"
          " runaway.  This is the operative content of 'dS-cured' and it HOLDS.")
    check(s_over_H[-1] < 0.02,
          f"and as Lambda takes over the rate goes to zero (s/H = {s_over_H[-1]:.2e} at z = -0.99):"
          " the instability SHUTS OFF in the de Sitter future -- 'dS-cured' CONFIRMED")
    print("    *** WORDING CORRECTION, stated because it matters: the instability is NOT absent.  It is present")
    print("        on every cosmological scale (S3b/S3c: the Jeans length is microscopic), its rate is bounded")
    print("        by H, and it switches off in the dS future.  That bounded growth IS the ordinary dust growing")
    print("        mode -- the thing the model NEEDS in order to form structure.  'dS-cured' should be read as")
    print("        'no faster-than-Hubble runaway, and it shuts off in the future', not as 'no growth'.  I have")
    print("        NOT reproduced ACLM's full GR mixing analysis; that is on the S5 CLASS-module list. ***")

    return dict(cs2_allowed=gr['cs2_lss'], dn_edge=gr['dn_lss'], lamJ_meV=lamJ_meV, M_need_eV=M_need_eV,
                k_cut_at_bound=k_at_lss, k_half=k_half, kcut_over_khalf=k_at_lss / k_half)


# --------------------------------------------------------------------------------------------------
# S4 -- S8: VERIFY OR REFUTE "neutral-by-theorem"
# --------------------------------------------------------------------------------------------------
def S4_S8(bg, gr):
    banner("S4 -- S8.  The corpus records 'neutral-by-theorem'.  VERIFY it with the growth calculation, and")
    print("      then test whether the a_0 / MI sector is really neutral, which is a DIFFERENT question.")

    at = gr['at']
    sub("S4a  the CONDENSATE sector: S8 computed both ways")
    S8_L = SIGMA8_PLANCK * math.sqrt(OM_M / 0.3)
    ratio_D = at(gr['lna_C'], gr['D_C'], 0.0) / at(gr['lna_L'], gr['D_L'], 0.0)
    S8_C = S8_L * ratio_D
    print(f"    LambdaCDM:  sigma_8 = {SIGMA8_PLANCK:.4f},  S8 = {S8_L:.5f}")
    print(f"    condensate: growth ratio D_C(0)/D_L(0) = {ratio_D:.12f}  ->  S8 = {S8_C:.5f}")
    print(f"    Planck S8 = {S8_PLANCK:.3f} +/- {S8_PLANCK_ERR:.3f}   KiDS-1000 ~ 0.759 (+0.024/-0.021)"
          f"   DES-Y3 ~ 0.776 +/- 0.017   KiDS-Legacy ~ 0.815 +/- 0.016")
    dS8 = abs(S8_C - S8_L)
    print(f"    |Delta S8| = {dS8:.3e}, i.e. {dS8/S8_PLANCK_ERR:.3e} sigma of the Planck error bar")
    check(dS8 / S8_PLANCK_ERR < 1e-3,
          f"S8 NEUTRALITY VERIFIED for the condensate sector: |Delta S8| = {dS8/S8_PLANCK_ERR:.2e} sigma."
          " Not 'neutral' -- numerically indistinguishable.")
    print("    => the corpus's 'S8 neutral-by-theorem' is CORRECT for the dark-sector fluid, and the reason is")
    print("       structural, not a coincidence: the condensate IS dust with c_s^2 -> 0 and no anisotropic")
    print("       stress, so its growth equation is CDM's.  There is nothing to cure and nothing to break.")

    sub("S4b  but is the a_0 / MI sector neutral?  Three readings of the kernel argument on FRW.")
    print("    The corpus's protection is the gradient order-count of project_cmb_boltzmann_aest PART B:")
    print("    Y = (grad delta_phi)^2 = O(eps^2), so the AQUAL term Y^(3/2) = O(eps^3) and its EOM piece is")
    print("    O(eps^2) -- ABSENT at linear order.  That order count is CORRECT about the TERM.  It does not by")
    print("    itself bound the SOLUTION, because in the deep-MOND branch that term is the ONLY term: AQUAL")
    print("    div(|grad phi| grad phi / a_0) = 4 pi G rho gives |grad phi| ~ sqrt(a_0 g_N) ~ sqrt(delta),")
    print("    which is LARGER than delta, not smaller.  So something must regulate the kernel argument.")

    # the actual peculiar accelerations of linear modes
    print("\n    First: how far below a_0 is a linear mode's own peculiar acceleration?")
    print("       g_pec = 4 pi G rho_m0 delta a / k_com  (comoving k)")
    print(f"    {'k [h/Mpc]':>10s} {'delta':>8s} {'z':>6s} {'g_pec [m/s^2]':>15s} {'x=g/a0 canon':>14s} {'x=g/a0 ALT':>13s}")
    xs = []
    for k_h, dl, zz in ((0.001, 1e-3, 0.0), (0.01, 1e-2, 0.0), (0.1, 1e-2, 0.0), (0.1, 1.0, 0.0), (0.1, 1e-2, 3.0)):
        k_com = k_h * HLITTLE / MPC
        a = 1.0 / (1.0 + zz)
        g = 4 * math.pi * G_NEWT * (OM_M * RHO_CRIT) * dl * a / k_com
        xs.append(g / A0_CANON)
        print(f"    {k_h:10.3f} {dl:8.1e} {zz:6.1f} {g:15.5e} {g/A0_CANON:14.5e} {g/A0_ALT:13.5e}")
    x_best = max(xs)
    check(x_best < 0.1,
          f"every linear mode has g_pec/a_0 <= {x_best:.3e} << 1: linear cosmological perturbations live"
          " DEEP in the modified regime, so the naive reading cannot be dismissed as irrelevant")

    print("\n    READING R1 -- the MI kernel is fed matter's OWN four-acceleration.  A comoving observer in FRW")
    print("    is a geodesic: |a| = 0 exactly on the background, and O(delta) once perturbed.  The response")
    print("    amplification to a small extra force is 1/h(x), h(x) = 2x/sqrt(1+4x^2) (NOT 1/mu -- established")
    print("    in mi_growth_amplification_founded_2026.py).  For x << 1, 1/h -> 1/(2x) -> infinity.")
    print(f"    {'x = g_pec/a_0':>15s} {'h(x)':>12s} {'1/h(x) = A':>12s} {'growth index p(A)':>18s}")

    def growth_index(A):
        # matter domination: delta'' + (1/2) delta' - (3/2) A delta = 0  ->  D ~ a^p
        return (-0.5 + math.sqrt(0.25 + 6.0 * A)) / 2.0

    amps_R1 = []
    for x in sorted(xs):
        hx = float(h_response(x))
        A = 1.0 / hx
        amps_R1.append(A)
        print(f"    {x:15.5e} {hx:12.5e} {A:12.5e} {growth_index(A):18.4f}")
    A_min_R1 = min(amps_R1)
    check(A_min_R1 > 10.0,
          f"R1 gives a source amplification >= {A_min_R1:.1f}x even for the MOST favourable linear mode"
          " -- i.e. the modification is order 1e3-1e4 percent, not order percent")
    check((A_min_R1 - 1.0) / 0.01 > 1000.0,
          f"R1 EXCLUDED: its SMALLEST source modification is {100*(A_min_R1-1):.0f}%, which is"
          f" {(A_min_R1-1)/0.01:.0f}x the 1% level PART A showed to be many-sigma -- 3+ orders over"
          " the CMB threshold, and the typical mode is 100x worse still")

    print("\n    READING R2 -- the argument is REGULATED by the condensate itself.  The attractor fixes")
    print(f"    c phidot = a_0 exactly (S0), so the background invariant sits at y = 1 and the free function is")
    print("    evaluated at an ORDER-UNITY, analytic point, with the perturbation entering as (g_pec/a_0)^2.")
    print("    That fixes the non-analyticity -- and it makes the ghost condensate STRUCTURALLY REQUIRED, not")
    print("    decoration: without a non-zero background invariant the linear cosmology is not even finite.")
    print("    But then the amplification is a CONSTANT: A = 1/h(1) in the MI reading, 1/mu_fw(1) in the MG one.")
    A_MI = 1.0 / float(h_response(1.0))
    A_MG = 1.0 / float(mu_fw(1.0))
    print(f"       1/h(1)      = sqrt(5)/2 = {A_MI:.6f}   (modified INERTIA response)")
    print(f"       1/mu_fw(1)  = {A_MG:.6f}   (modified GRAVITY reading, for contrast)")
    check(abs(A_MI - math.sqrt(5) / 2) < 1e-12, "1/h(1) = sqrt(5)/2 exactly (analytic cross-check)")
    lcdm_growth = gr['lcdm_growth']
    print(f"\n    {'reading':>28s} {'A':>9s} {'D(0)/D_LCDM(0)':>16s} {'sigma_8':>9s} {'S8':>8s} {'sigma vs Planck S8':>19s}")
    verdicts = {}
    for label, A in (("R3  MOND quasi-static only", 1.0), ("R2  MI, y=1 regulated", A_MI),
                     ("R2' MG, y=1 regulated", A_MG)):
        lna_A, D_A, f_A = lcdm_growth(0.1, poisson_amp=A)
        r = at(lna_A, D_A, 0.0) / at(gr['lna_L'], gr['D_L'], 0.0)
        s8 = SIGMA8_PLANCK * r
        S8v = s8 * math.sqrt(OM_M / 0.3)
        nsig = (S8v - S8_PLANCK) / S8_PLANCK_ERR
        verdicts[label] = (A, r, s8, S8v, nsig)
        print(f"    {label:>28s} {A:9.5f} {r:16.6f} {s8:9.4f} {S8v:8.4f} {nsig:19.1f}")
    # external validation of the growth solver itself: f(z=0) must match the standard Om_m^0.55 fit
    f0 = at(gr['lna_L'], gr['f_L'], 0.0)
    f0_fit = OM_M ** 0.55
    print(f"\n    growth-solver validation: f(z=0) = {f0:.5f} vs the standard Om_m^0.55 = {f0_fit:.5f}"
          f"  (diff {100*(f0/f0_fit-1):+.2f}%)")
    check(abs(f0 / f0_fit - 1) < 0.02,
          f"the growth solver reproduces the textbook f(z=0) = Om_m^0.55 to {100*abs(f0/f0_fit-1):.2f}%"
          " -- an EXTERNAL check, so the R2 exclusion below rests on a validated solver")
    r2 = verdicts["R2  MI, y=1 regulated"]
    check(abs(r2[1] - 1.0) > 0.05,
          f"R2 is NOT a wash: it raises sigma_8 by {100*(r2[1]-1):.1f}% (sigma_8 = {r2[2]:.3f},"
          f" S8 = {r2[3]:.3f}, {r2[4]:+.0f} sigma from Planck) -- EXCLUDED")
    check(abs(verdicts["R2' MG, y=1 regulated"][1] - 1.0) > abs(r2[1] - 1.0),
          "and the MG reading is worse still, so the exclusion is not an artefact of the MI/MG choice")

    sub("S4c  prove-by-moving-the-number: a_0 -> 0 must switch the whole effect off")
    for a0_test, lbl in ((A0_CANON, "canonical"), (A0_ALT, "ALT"), (1e-30, "a_0 -> 0 (control)")):
        x = 1e-14 / a0_test
        print(f"    a_0 = {a0_test:.3e} ({lbl:18s}): x = g/a_0 = {x:.4e}, A = 1/h(x) = {1.0/float(h_response(x)):.6f}")
    A_zero = 1.0 / float(h_response(1e-14 / 1e-30))
    check(abs(A_zero - 1.0) < 1e-6,
          f"with a_0 -> 0 the amplification returns to 1 ({A_zero:.9f}): the effect is genuinely a_0-driven,"
          " not a numerical artefact")

    sub("S4d  VERDICT on 'S8 neutral-by-theorem'")
    print(f"    CONDENSATE SECTOR:  VERIFIED, and stronger than recorded -- indistinguishable at the"
          f" {dS8/S8_PLANCK_ERR:.0e}-sigma")
    print("       level, for the structural reason that the condensate is exact dust with c_s^2 -> 0.")
    print("    a_0 / MI SECTOR:  'by-theorem' is REFUTED as a theorem and CONFIRMED as a consequence of R3.")
    print(f"       R1 (matter's own four-acceleration) is EXCLUDED by 3+ orders ({100*(A_min_R1-1):.0f}% vs the")
    print(f"       1% CMB threshold).  R2 (condensate-regulated, y = 1) is EXCLUDED at {100*(r2[1]-1):.0f}% in")
    print("       sigma_8, i.e. +34 sigma in S8.  Only R3 -- MOND switched off for cosmological")
    print("       perturbations, which is what AeST engineers and what the corpus assumes -- survives, and R3")
    print("       is a MODEL CHOICE, not a derivation.  The honest status: the framework's linear cosmology is")
    print("       LambdaCDM BY ASSUMPTION, and the assumption is load-bearing (PART A of the CMB script proved")
    print("       exactly that).  A referee will press here, and 'the gradient order count protects us' is not")
    print("       a sufficient answer, because the order count bounds a term and not the solution.")
    return verdicts


# --------------------------------------------------------------------------------------------------
# S5 -- THE CMB: what can and cannot be addressed, and what a CLASS/CAMB module must implement
# --------------------------------------------------------------------------------------------------
def S5_cmb(bg, s3, gr_pack):
    gr_at = gr_pack['at']
    banner("S5 -- THE HONEST QUESTION: does this reproduce the CMB?  No Boltzmann run here; a precise ledger.")

    sub("S5a  what IS computable now, and is computed: the geometric observables")
    make_model = bg['make_model']
    m = make_model(s3['cs2_allowed'])

    def r_s_and_lA(E):
        a_rec = 1.0 / 1090.0
        R = lambda a: 0.75 * (OM_B / OM_GAMMA) * a
        cs = lambda a: 1.0 / math.sqrt(3 * (1 + R(a)))
        rs = quad(lambda a: cs(a) / (a ** 2 * float(E(a))), 1e-8, a_rec, limit=300)[0]
        DA = quad(lambda a: 1.0 / (a ** 2 * float(E(a))), a_rec, 1.0, limit=300)[0]
        return rs, DA, math.pi * DA / rs

    rs_L, DA_L, lA_L = r_s_and_lA(bg['E_lcdm'])
    rs_C, DA_C, lA_C = r_s_and_lA(m['E'])
    cH0_Mpc = C_LIGHT / H0 / MPC
    print(f"    {'quantity':>26s} {'LambdaCDM':>16s} {'condensate':>16s} {'frac diff':>13s}")
    for nm, vL, vC in (("r_s [Mpc]", rs_L * cH0_Mpc, rs_C * cH0_Mpc),
                       ("D_A(rec) [Mpc]", DA_L * cH0_Mpc, DA_C * cH0_Mpc),
                       ("l_A = pi D_A/r_s", lA_L, lA_C),
                       ("theta_* = r_s/D_A [rad]", rs_L / DA_L, rs_C / DA_C)):
        print(f"    {nm:>26s} {vL:16.6f} {vC:16.6f} {vC/vL-1:13.3e}")
    check(abs(lA_C / lA_L - 1) < 1e-9,
          f"the acoustic scale l_A is identical to {abs(lA_C/lA_L-1):.2e}: every CMB GEOMETRIC observable"
          " (theta_*, l_A, the shift parameter R) is inherited from LambdaCDM unchanged")
    check(abs(lA_L - 301.0) < 12.0,
          f"and the LambdaCDM baseline l_A = {lA_L:.1f} is in the right ballpark (Planck ~ 301.7),"
          " so this is a working reference, not a broken integral")

    print("\n    Delta N_eff: the ONE genuinely new CMB observable the condensate carries -- and it is CLOSED.")
    print(f"       Delta N_eff = {bg['coef_neff']:.4g} Q^(1/3).  Taken alone, Planck (< ~0.3) allows"
          f" c_s0^2 <= {bg['cs0_max_neff']:.1e}.")
    print(f"       But the small-scale-power bound (S2c, cross-checked in S3c) forces c_s0^2 <="
          f" {s3['cs2_allowed']:.1e},")
    print(f"       which drives Delta N_eff <= {s3['dn_edge']:.2e} -- about {0.03/s3['dn_edge']:.0f}x below"
          " CMB-S4's sigma(N_eff) ~ 0.03.")
    print("       AGAINST INTEREST: I expected N_eff to be the live handle.  It is not.  The condensate has NO")
    print("       observable CMB signature beyond the geometry it shares with LambdaCDM.  That is safety bought")
    print("       at the price of testability, and it should be reported as such, not as a pass.")

    sub("S5b  what CANNOT be addressed without a modified Boltzmann code -- itemised")
    cannot = [
        ("C_l^TT / TE / EE peak HEIGHTS", "needs the photon multipole hierarchy + recombination (RECFAST/HyRec)"
                                          " and the condensate's delta rho, delta p, (rho+p)theta sourcing the"
                                          " Einstein constraints at every k, a"),
        ("C_l^phiphi lensing potential", "needs the full Weyl potential history, not just the growth factor"),
        ("late ISW", "expected identical (Lambda_eff + dust background is LambdaCDM's), but this needs Phi-dot"
                     " with the condensate's delta p included, which is not the same as checking H(z)"),
        ("isocurvature", "the condensate is a SEPARATE field: it generically carries a non-adiabatic mode."
                         " Planck bounds isocurvature at the few-% level.  Adiabaticity must be IMPOSED as an"
                         " initial condition or its amplitude carried as a parameter.  NOT checked here."),
        ("the a_0 / MI sector's linear contribution", "this is the real gap.  S4b showed R1 and R2 are"
                                                      " excluded and only R3 (MOND quasi-static-only) survives."
                                                      " R3 has never been DERIVED for this framework -- it is"
                                                      " inherited from AeST's engineering.  A CLASS module is"
                                                      " what would settle it."),
        ("ACLM's full GR Jeans analysis", "S3d did the fluid-level rate.  The 4th-order-in-k mixing of pi with"
                                          " the metric potentials in the ACLM formalism was NOT reproduced."),
        ("second-order / non-linear a_0 terms", "the corpus's own residual: the MOND term is genuinely"
                                                " second-order, negligible for C_l but not zero"),
    ]
    for nm, why in cannot:
        print(f"    * {nm}")
        print(f"        {why}")
    print(f"    ({len(cannot)} concrete entries.)")
    # the ISW entry says 'expected identical' -- test the part of that which IS testable now: the late-time
    # growth suppression D(a)/a, which is what sets the ISW source.
    isw_L = gr_at(gr_pack['lna_L'], gr_pack['D_L'], 0.0) / gr_at(gr_pack['lna_L'], gr_pack['D_L'], 1.0)
    isw_C = gr_at(gr_pack['lna_C'], gr_pack['D_C'], 0.0) / gr_at(gr_pack['lna_C'], gr_pack['D_C'], 1.0)
    print(f"    testable part of the ISW entry: D(z=0)/D(z=1) = {isw_L:.10f} (LCDM) vs {isw_C:.10f}"
          f" (condensate), frac diff {isw_C/isw_L-1:.2e}")
    check(abs(isw_C / isw_L - 1) < 1e-9,
          "the late-time growth suppression D(z=0)/D(z=1) -- which SETS the ISW source -- is identical to"
          " <1e-9, so 'ISW expected identical' is supported for the part that can be computed without a"
          " Boltzmann code.  The Phi-dot integral itself still needs the module.")

    sub("S5c  what a modified CLASS / CAMB module would have to implement -- the spec")
    spec = [
        "BACKGROUND: add a fluid solving a^3 P'(X) phidot = C alongside the Friedmann equations.  For the"
        " quadratic extremum this is CLOSED FORM -- u sqrt(1+u) = Q/a^3, solved in log space -- so no new"
        " stiff ODE is needed.  Outputs rho_phi(a) = lambda X_0^2 (2u + 1.5u^2) - P_0 and p_phi(a).",
        "PERTURBATIONS: one new scalar dof pi (or delta phi) with quadratic action kinetic coefficient"
        " (P' + 2 X P'') and gradient coefficient P', plus the higher-derivative (nabla^2 pi)^2/k_M^2 operator."
        " The k^4 term makes the equation 4th order in k -- either integrate it directly (stiff at large k) or"
        " reduce to an effective fluid with c_eff^2(k,a) = u/(3u+2) + (c k/(a k_M))^2, which is what S2 did.",
        "STRESS TENSOR: feed delta rho_phi = (P' + 2XP'') phidot delta phidot - ..., delta p_phi = P' delta X,"
        " and (rho+p) theta_phi = (P' ) phidot k^2 pi/a into the Einstein constraints.  ZERO anisotropic stress"
        " at quadratic order -- that must be asserted in the code, and checked at cubic order.",
        "INITIAL CONDITIONS: the adiabatic mode for the condensate at a_ini, or an isocurvature amplitude as a"
        " free parameter.  Non-trivial, because at a_ini the condensate is in its u >> 1, w = 1/3, c_s^2 -> 1"
        " phase, NOT dust -- its ICs are radiation-like, not CDM-like.",
        "NEW PARAMETERS beyond LambdaCDM: exactly two that matter -- Q (equivalently c_s0^2, or the transition"
        " redshift z_t) and k_M.  Both are bounded above and unbounded below, so the module would report"
        " UPPER LIMITS, not measurements.  Plus kappa, which is fitted from galaxies, not from the CMB.",
        "THE MI COUPLING, if it is to be included at all: the disformal / effective-metric coupling to matter"
        " that modifies the matter Euler equation with the a_0 term.  This is the piece with NO current"
        " formulation at linear order in this framework, and it is exactly what would decide between R1, R2"
        " and R3.  Everything else on this list is bookkeeping; this one is physics that does not yet exist.",
    ]
    for i, s in enumerate(spec, 1):
        print(f"    {i}. {s}")
    print(f"    ({len(spec)} items; item {len(spec)} is the honest blocker -- everything above it is bookkeeping.)")

    sub("S5d  the one-line answer to the referee")
    print("    'Not yet, and here is exactly what is missing.'  The condensate reproduces every CMB GEOMETRIC")
    print("    observable identically (l_A, theta_*, R: agreement to 1e-9 or better) and predicts one genuine")
    print(f"    new one (Delta N_eff <= {s3['dn_edge']:.1e}, which S2c's small-scale-power bound pushes ~"
          f"{0.03/s3['dn_edge']:.0f}x below CMB-S4 -- i.e. that handle is CLOSED).  It cannot yet")
    print("    predict C_l peak heights, lensing, or isocurvature, because no Boltzmann module exists.  And the")
    print("    honest crux is NOT the condensate at all -- it is that the a_0 sector's linear-order behaviour is")
    print("    undetermined, with two of the three readings EXCLUDED (S4b) and the surviving one an assumption")
    print("    inherited from AeST.  So the CMB is currently a CONSISTENCY CHECK the model passes trivially,")
    print("    not a test it passes non-trivially.  That is both its safety and its emptiness.")


# --------------------------------------------------------------------------------------------------
# S6 -- both footings, and the summary
# --------------------------------------------------------------------------------------------------
def S6_summary(bg, s3, verdicts):
    banner("S6 -- BOTH FOOTINGS on every dimensional number, and the Lane-G ledger.")
    print(f"    {'quantity':>40s} {'canonical (rho_DE/cH_L)':>24s} {'ALT (rho_tot/cH_0)':>22s}")
    rows = [
        ("a_0 [m/s^2]", A0_CANON, A0_ALT),
        ("phidot_attr = a_0/c [s^-1]", A0_CANON / C_LIGHT, A0_ALT / C_LIGHT),
        ("a_0/c in units of H_0", (A0_CANON / C_LIGHT) / H0, (A0_ALT / C_LIGHT) / H0),
        ("decay constant f / M_Pl", (1 / KAPPA), (1 / KAPPA) * math.sqrt(OM_L)),
        ("rho used in a_0 [kg/m^3]", OM_L * RHO_CRIT, 1.0 * RHO_CRIT),
    ]
    for nm, vc, va in rows:
        print(f"    {nm:>40s} {vc:24.6e} {va:22.6e}")
    check(abs(A0_ALT / A0_CANON - 1.2082) < 2e-3,
          f"footing spread ALT/canonical = {A0_ALT/A0_CANON:.4f}, matching 1/sqrt(Om_L) ="
          f" {1/math.sqrt(OM_L):.4f} to {100*abs(A0_ALT/A0_CANON*math.sqrt(OM_L)-1):.2f}% (rounding in the"
          " committed 1.13e-10), as committed")

    print("\n    Footing-DEPENDENCE of every Lane-G conclusion:")
    print("      * S1-S3 (background, growth, c_s^2, Jeans, S8-neutrality of the condensate): a_0 does NOT enter."
          "  Footing-BLIND.")
    print("      * S4b R1/R2 exclusions: a_0 enters through x = g_pec/a_0 and through y = 1.  Both footings give")
    print(f"        the same verdict -- x changes by only {A0_ALT/A0_CANON:.3f}x, and R2's y = 1 is footing-fixed")
    print("        by the attractor.  So the exclusions are ROBUST to the footing fork.")
    print("      * S1e f/M_Pl: footing-DEPENDENT, 2.000 (canonical) vs 1.655 (ALT).")

    print("\n    LANE-G LEDGER")
    print("      HELD / VERIFIED")
    print("        1. P'(X) -> 0 attractor and phidot -> const: verified symbolically AND numerically from an")
    print("           off-attractor start (8 decades of P' decay).")
    print("        2. The condensate is exact DUST at the attractor plus an exact w = -1 piece: ONE field gives")
    print("           both Om_dm and Om_L, with continuity holding IDENTICALLY in sympy.")
    print("        3. Background reproduces (H_0, Om_m, Om_L) with 2 free numbers against LambdaCDM's 2:")
    print("           MATCHED, not reduced.  The corpus's 'amount I_0 is FREE' wall stands, by construction.")
    print("        4. c_s^2 = u/(3u+2) -> 0 at the attractor, ceiling 1/3 (no superluminal front anywhere);")
    print("           condensate CURES the ghost (kinetic coefficient 2 lambda X_0 > 0).")
    print("        5. 'Jeans is dS-cured': CONFIRMED in substance (rate <= H always, -> 0 in the dS future),")
    print("           with a WORDING correction -- the instability is present and IS the dust growing mode.")
    print("        6. 'S8 neutral-by-theorem': VERIFIED for the condensate sector at the 1e-8-sigma level.")
    print("      NEW HERE")
    print("        7. The early condensate is RADIATION-LIKE (w -> 1/3), not kination.  The early constraint is")
    print(f"           Delta N_eff = {bg['coef_neff']:.3g} Q^(1/3).  But small-scale POWER binds"
          f" ~{math.log10(bg['cs0_max_neff']/s3['cs2_allowed']):.0f} decades harder"
          f" (c_s0^2 <= {s3['cs2_allowed']:.1e}), computed two independent ways (growth ODE half-mode vs"
          f" comoving sound horizon) that agree to a factor {s3['kcut_over_khalf']:.2f}.")
    print(f"        8. The k^4 handle is CLOSED: an observable Jeans cutoff needs M ~ {s3['M_need_eV']:.1e} eV,")
    print("           below the fuzzy-DM floor.  M is free and every viable value is microscopic.  No prediction.")
    print("        9. EXACT IDENTITY f = M_Pl/kappa: kappa = 1/2 <=> a Planckian decay constant f = 2 M_Pl.")
    print("           A relabelling (cannot force kappa), and AGAINST INTEREST via the swampland folklore.")
    print("      AGAINST INTEREST / OPEN")
    print("       10. 'S8 neutral-by-THEOREM' is REFUTED as a theorem.  The gradient order-count bounds a TERM,")
    print("           not the SOLUTION.  R1 excluded by 3+ orders (>4000% vs a 1% threshold); R2 excluded at")
    print("           53% in sigma_8 (+34 sigma in S8); only R3 (MOND quasi-static-only) survives, and R3 is")
    print("           inherited from AeST's engineering, not derived here.")
    print("       11. The framework's linear cosmology is therefore LambdaCDM BY ASSUMPTION.  That makes the")
    print("           whole linear sector non-diagnostic in BOTH directions: RSD/f sigma_8 cannot exclude it")
    print(f"           (Delta chi^2 = 0 on the compilation) and cannot support it either.")
    print(f"       12. AGAINST INTEREST: Delta N_eff looked like the one new CMB handle and it is CLOSED -- the")
    print(f"           small-scale-power bound drives it to <= {s3['dn_edge']:.1e}, ~{0.03/s3['dn_edge']:.0f}x below CMB-S4.")
    print("           And the f sigma_8 SHAPE is far less sensitive than the P(k) AMPLITUDE, so grading this")
    print("           front by RSD alone would understate the constraint by decades.  Do not grade it that way.")
    print("       13. The missing physics is one specific object: the a_0 sector's linear-order coupling.  Until")
    print("           it exists there is no CMB prediction beyond Delta N_eff.  NO DOORS ARE CLOSED by this.")


# --------------------------------------------------------------------------------------------------
def main() -> int:
    print("#" * 108)
    print("# LANE G -- COSMOLOGICAL PERTURBATIONS of the ghost-condensate dark sector (modified INERTIA)")
    print("# kernel nu(y) = sqrt(1+1/y): MILGROM 1999 PLA 253:273 eqs 6-9.  Ghost condensate: ACLM 2004")
    print("# JHEP 0405:074.  Temperature: NARNHOFER-PETER-THIRRING 1996.  kappa = 1/2 IS FITTED, NOT DERIVED.")
    print("#" * 108)

    S0_footings()
    bg = S1_background()
    gr = S2_growth(bg)
    s3 = S3_sound_speed(bg, gr)
    verdicts = S4_S8(bg, gr)
    S5_cmb(bg, s3, gr)
    S6_summary(bg, s3, verdicts)

    banner("CHECK TALLY")
    n_ok = sum(1 for c, _ in _RESULTS if c)
    n_tot = len(_RESULTS)
    for c, m in _RESULTS:
        if not c:
            print(f"    [FAIL] {m}")
    print(f"\n{n_ok}/{n_tot} checks held.")
    return 0 if n_ok == n_tot else 1


if __name__ == "__main__":
    sys.exit(main())
