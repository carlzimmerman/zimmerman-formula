#!/usr/bin/env python3
"""
XR31 -- IS k04's 'STABLE (F6)' RIGHT?  The four-form promotion's slaved kernel, on k04's own kernel and couplings
=================================================================================================================
THE RESULT UNDER REVIEW.  kappa_closure/k04_four_form_promotion_consistency.py (2fb80ca12, with its .out) promotes the MOND
scale to a four-form flux, a0 = beta sqrt(G)|q|, P(q) = Z q^2/2, on the candidate's saturated nu_RAR kernel: the scalar's force
is g_phi = a0 Delta(s), s = g_N/a0, Delta = s/(e^sqrt(s) - 1) up to its maximum (s_sat = 2.540, Delta = 0.6476) and flat beyond.
Its F6 records the construction as stable: 'the effective flux stiffness Z_eff = Z + (2 - K_B) beta^2 (s Delta - j)/(8 pi) is
positive everywhere'.  Review lane XR20 (a075ad7f7) read that F6 tests the flux stiffness at fixed s, not the monotonicity of the
slaved kernel, and reported (T2f) that under k04's kernel the slaved boost already falls above y ~ 2.4 / 2.3.  This lane checks
that claim independently, from k04's definitions, and says whether F6 is wrong, right, or right only in a restricted sense.

THIS LANE'S ALGEBRA (written from k04's code and docstring; XR20's code was not used for it).  Per beta^2 q0^2, with r = q/q0 =
a0_loc/a0 and everything in units of the vacuum a0:
  L(r, Y) = r^2 Zt/2 - k r^2 j(s),   Y = (r Delta(s))^2  (the scalar's gradient squared),   k = (2 - K_B)/(16 pi),
  j(s) = 2 Int_0^s t Delta'(t) dt  (k04's j),  Zt = Z/beta^2 + 2b = 2/kappa^2  (k04's F1 constant b is absorbed; Zt = 8 is k04's F3).
  The three-form's equation d_mu(dL/dq) = 0 makes the conjugate constant: Pi = dL/dr|_Y = r [Zt + (2 - K_B) F(s)/(8 pi)] = Zt,
  F = s Delta - j; the scalar's law J_Y g_phi = g_N reads y = s r (y = g_N/a0).  This is k04's F3 equation, r (1 + c F(y/r)) = 1
  with c = (2 - K_B)/(8 pi Zt).  Because Pi is constant in space and time, q has no local mode and follows the scalar instantly;
  the scalar then obeys the reduced (Routh) Lagrangian L - Pi q, whose channel coefficients are C_L,eff = dy/du and
  C_T,eff = y/u along the slaved law u(y) = r Delta(y/r) (u = g_phi/a0).  F6's Z_eff is Pi/q, the SECANT stiffness; it equals
  Zt (1 + c F) >= Zt whenever F >= 0.
  Zt is the four-form's coupling ratio, NOT the framework's Z = 5.7888; kappa = 1/2 stays FITTED -- nothing here derives it.

TWO INDEPENDENT ROUTES TO THE FOLD, and a third to the band's C_L:
  A  the Legendre map q -> Pi at fixed Y (40-digit finite differences of L itself; the kernel's inverse and j by root-finding and
     quadrature; no closed form used): the fold is where dPi/dq|_Y = L_rr|_Y = 0 on shell;
  B  direct root-finding of the coupled static equations (the four-form equation with the scalar's law) at each y, in double
     precision, and the peak of the slaved force u(y) (4-point finite differences);
  C  the dual (flux) formulation at fixed matter flux y: Lstar(r, y) = r^2 Zt/2 + k r^2 (2 s Delta - j) - Zt r, s = y/r (smooth
     on the saturated branch too); du/dy|_Pi = [Lstar_yy - Lstar_ry^2/Lstar_rr]/(2k) (the Schur complement), 40 digits.

PRE-DECLARED (written into this docstring before any code of this lane ran; expectations come from pencil-and-paper algebra,
informed by XR20's reported T2f numbers 2.40 / 2.31, which this lane was asked to verify):
  CASES  k04's convention, Zt = 8 (kappa = 1/2) for both footings, K_B = 0 and 0.25 (so the fold in y is footing-free; the
         footings differ only in g_N = y a0); and the TIED alt footing, kappa = 0.6043 on the observed rho_Lambda
         (Zt = 2/kappa^2 = 5.48, K_B = 0) -- XR20's 'alt'.  XR20's 'canonical' is k04's K_B = 0 case (c = 1/32 pi either way).
  H0  CONTROLS.  C0: k04's own script, run unmodified, reproduces its committed .out verbatim (rc = 0).  C0b: this lane's route B
      in k04's convention reproduces k04's committed F3 rows (K_B = 0, 0.25) and F5 rows (both footings) to the printed digits.
      C1: XR20's own script, run unmodified from a scratch mirror (its inputs copied; nothing in the repository written),
      reproduces its committed T2f line for k04's kernel verbatim.  C1b: this lane's route B in XR20's convention
      (c = kappa^2/8 pi, K_B = 0) on XR20's own 400-point grid returns the same peaks (2.40 / 2.31) and u(100), and the precise
      fold lies within one grid step of them.  C2: the SPARC loader (FP1's convention) reads 175 galaxies and 3391 points at
      Upsilon = 0.7 (FP7's count).  C3: the kernel's constants equal the record's printed ones (s_sat 2.540, Delta_sat 0.6476,
      I = j_sat = 0.4525).
  A1-A5 (sympy + numeric)  A1: dL/dr|_Y = r [Zt + (2 - K_B) F/(8 pi)] and J_Y = s/Delta (k04's F3 equation re-derived).  A2: on
      shell L_rr|_Y = Zt N(s)/Delta'(s) and du/ds = N(s)/(1 + cF)^2 with N = Delta'(1 + c(F + s Delta)) - c Delta^2: the Legendre
      map folds exactly where the slaved force peaks, and C_L,eff = (1 + c(F - s F'))/N.  A3: F' = Delta - s Delta' > 0 and F >= 0
      for k04's kernel (F' = Delta_sat on the saturated branch): F6's Z_eff >= Z identically.  A4: on the saturated branch the
      flux equation is linear, r = (1 - c D_sat y)/(1 - c j_sat), du/dy = -c D_sat^2/(1 - c j_sat), y_off = 1/(c D_sat),
      C_L,eff = -(1 - c j_sat)/(c D_sat^2).  A5: dy/ds = (1 + c(s^2 Delta' - j))/(1 + cF)^2 >= (1 - c j_sat)/(1 + cF)^2 > 0: the
      flux equation has exactly one root at every y (0 < a0_loc <= a0).  EXPECT TRUE.
  H1  THE FOLD.  In every case the slaved scalar force u(y) rises, peaks at y_f in [2.2, 2.6] (pencil: 2.39 at K_B = 0, 2.41 at
      K_B = 0.25, 2.32 tied alt), and falls -- linearly on the saturated branch -- to zero at y_off = 1/(c D_sat) (155, 177, 106).
      Routes A and B agree on y_f to < 1e-6; du/dy > 0 at every grid point below y_f and < 0 at every grid point of
      (y_f, y_off); route B's y_off equals A4's to 1e-9.  EXPECT TRUE.
  H2  THE RAR STAYS MONOTONE: dg_obs/dg_N = 1 + du/dy >= 0.99 everywhere below y_off -- the fold is in the scalar's own force,
      not in g_obs.  EXPECT TRUE.
  H3  F6 IS VACUOUS: F6's criterion Z_eff/Z - 1 = c F >= 0 holds at every s of k04's own grid and on the band where C_L,eff < 0;
      the TANGENT stiffness L_rr|_Y (route A) changes sign at the fold (> 0 at y_f - 0.05, < 0 at y_f + 0.05); the dual stiffness
      Lstar_rr|_y (route C) stays > 0 everywhere (the flux equation is well-posed: the restricted sense in which F6 is right).
      EXPECT TRUE.
  H4  STATIC ELLIPTICITY FAILS ON THE BAND: C_L,eff < 0 and C_T,eff > 0 at y = 2.45, 3, 5, 10, 20, 50, 100, 150 (those below
      y_off), routes B and C agreeing to 1e-6 (relative); on the saturated branch C_L,eff equals A4's constant to 1e-8 (-239 at
      K_B = 0); in the unsaturated slice the primal Schur complement (route A's Hessian) gives the same C_L,eff.  EXPECT TRUE.
  H5  DYNAMICS.  (a) the scalar's own sector: omega^2(k || grad phi)/omega^2(k perp) = C_L,eff/C_T,eff < 0 -- for either sign
      of the inertia one channel grows, at a rate ~ k (Hadamard); (b) the chain root's committed quadratic form (FP7 C1's T and V,
      parsed from its .out; alpha_c = 3.2e-9, c_2 = 7.29e-3, sigma = 1; lambda = 1, 277, 1.07e7 from FP7's text) with
      C_phi = C_L,eff has exactly one omega^2 < 0 at every band point (pencil: -0.86 (ck)^2 at lambda = 1 on the saturated
      branch), and FP14 L2's lambda = 0 one-mode formulas (c_2 finite and -> oo) are negative too; CONTROLS: at fixed a0 (no
      four-form) both roots are positive at y = 1 and in the saturated wall's limit C_phi -> oo.  EXPECT TRUE.
  MONO (reported; pre-declared EXPECT FALSE here and TRUE under MUTATE): the slaved force is monotone non-decreasing on
      (0, y_off).
  H6  WHERE THE BAND SITS (reported, both footings a0 = 9.3603e-11 / 1.1312e-10): SPARC points in (y_f, y_off) at Upsilon =
      0.5 / 0.7 / 0.9 (pencil 10-30%); around a 1-Msun star the scalar is off inside ~640 AU and unstable out to ~5100 AU in
      isolation (the Galactic field g_ext = 2.32e-10 (FP7 A4) moves the outer edge with direction); wide binaries (1.5 Msun) at
      2, 3, 5 kAU sit in the band, 10 and 20 kAU below it in isolation.  Load-bearing: the 2 kAU bin lies in the band on both
      footings, in isolation and for every orientation of the Galactic field.
  H7  k04's OTHER CLAIMS vs F6.  F1-F2 live on the Y = 0 background (r = 1, outside the band): untouched.  F3's rows s = 0.01,
      0.1, 1 lie below the fold, s = 2.54, 10, 100 in the band, s = 1000 in the switched-off core.  F4's planets all lie in the
      switched-off core (y > y_off): the monopole screening is a static statement F6 does not touch, but it is wrapped in the
      unstable shell.  F5's 2 kAU bin (k04's own inputs) lies in the band.  EXPECT TRUE.  Reported, EXPECT FALSE: k04's quoted
      '205 AU' is the radius where g_N = y_off a0 around 1 Msun (pencil: 639 AU).
MUTATE=1: route B's slaved force law is replaced by its running maximum (a kernel made monotone by hand).  MONO then passes, and
every check that requires the fold -- H1 (route B), H4 (route B's sign and its agreement with C), H5 (route B's C_L,eff), H6's
2 kAU bin and H7's classifications -- must FAIL: rc = 1.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR31_k04_f6_stability.py  (MUTATE=1 for the
control).  Writes XR31_k04_f6_stability[_MUTATE].out and XR31_k04_f6_stability_results[_MUTATE].json next to itself.  The XR20
cross-check writes only into a scratch directory (XR31_SCRATCH if set, else a system temporary directory).  One thread.

AFTER DEBUG RUN 1 (MUTATE; disclosed in XR31_README.md; no hypothesis text or threshold above was changed):
  (i)  C2 re-specified: FP7's 3391 counts V_obs > 0 and errV > 0 with no g_bar > 0 cut; with FP1's RAR cuts the loader reads 3389
       at Upsilon = 0.7 (two points whose gas term makes g_bar <= 0).  The control now reproduces FP7's own selection and prints
       the RAR-cut count beside it.
  (ii) the MUTATE envelope: a bounded minimiser had put the cap 4.5e-4 PAST the true peak (K0), leaving a sliver of non-monotone
       law, and the 4-point stencil did not cancel exactly on a flat stretch (rounding of 7u - 8u); the cap now sits 1e-6 below the
       bracketed peak and the stencil is written in differences.
AFTER RUN 2 (a complete ordered pair, MUTATE rc = 1 then main rc = 0; superseded by run 3, no number changed):
  (iii) the correction note's wording '(Z_eff/beta^2 = 8)' corrected to '(F3's Z = 8 beta^2)', and H5 now tests the k^2 scaling
        behind its pre-declared 'rate ~ k (Hadamard)' wording explicitly (omega^2(10 k)/omega^2(k) = 100).
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import re, sys, json, math, time, shutil, hashlib, subprocess, tempfile
import numpy as np
import sympy as sp
import mpmath as mp
from scipy.optimize import brentq

T_START = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
NAME = "XR31_k04_f6_stability"
MUTATE = os.environ.get("MUTATE", "0") == "1"
TXT = os.path.join(HERE, NAME + ("_MUTATE.out" if MUTATE else ".out"))
JSN = os.path.join(HERE, NAME + ("_results_MUTATE.json" if MUTATE else "_results.json"))
K04_PY = "kappa_closure/k04_four_form_promotion_consistency.py"
K04_OUT = "kappa_closure/k04_four_form_promotion_consistency.out"
K01_OUT = "kappa_closure/k01_zero_mode_theorem_and_lambda_free_vacuum.out"
XR20_PY = "real_research/cross_thread_review_2026_09_26/XR20_a0_lambda_tie.py"
XR20_OUT = "real_research/cross_thread_review_2026_09_26/XR20_a0_lambda_tie.out"
XR20_INPUTS = ["real_research/derivation_chain_2026/FP0_core_postulates_results.json",
               "real_research/derivation_chain_2026/FP1_static_sector_results.json",
               "real_research/derivation_chain_2026/FP5_dof_and_a0_field_results.json",
               "real_research/derivation_chain_2026/FP7_aqual_type_repair.out",
               "real_research/derivation_chain_2026/FP7_aqual_type_repair_results.json",
               "real_research/derivation_chain_2026/FP14_zero_knob_core.out",
               "kappa_closure/k02_global_constraint_average.out",
               "kappa_closure/k04_four_form_promotion_consistency.out",
               "fable_independent_2026/L37_recombination_footing.out"]
FP7_OUT = "real_research/derivation_chain_2026/FP7_aqual_type_repair.out"
FP14_OUT = "real_research/derivation_chain_2026/FP14_zero_knob_core.out"
SPARC_DIR = "real_research/data/sparc_data"


class Tee:
    """everything printed goes to the terminal and to this script's own .out"""
    def __init__(self, path):
        self._f = open(path, "w", encoding="utf-8")
        self._o = sys.__stdout__

    def write(self, t):
        self._o.write(t)
        self._f.write(t)

    def flush(self):
        self._o.flush()
        self._f.flush()

    def close(self):
        self._f.close()


TEE = Tee(TXT)
sys.stdout = TEE
OUT = {"lane": "XR31", "subject": "kappa_closure/k04 F6: is the four-form promotion stable?", "mutate": MUTATE,
       "checks": {}, "numbers": {}}
W = 118


def P(*a):
    print(*a, flush=True)


def banner(t):
    P("\n" + "=" * W)
    P(t)
    P("=" * W)


def check(cid, name, measured, ok, reading="", load_bearing=True):
    P(f"  [{'PASS' if ok else 'FAIL'}] {cid} {name}" + ("" if load_bearing else "  [reported]"))
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    OUT["checks"][cid] = dict(ok=bool(ok), load_bearing=bool(load_bearing), name=name, measured=str(measured))


def rd(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def f_(x):
    return float(x)


P("XR31 -- IS k04's 'STABLE (F6)' RIGHT?  The four-form promotion's slaved kernel on k04's own kernel and couplings")
P("  (independent derivation from k04's definitions; XR20's code is run only as a cross-check of its T2f number)")
if MUTATE:
    P("\n  *** MUTATE=1: route B's slaved force law is replaced by its running maximum (a kernel made monotone by hand); every check "
      "that requires the fold must FAIL ***")

# ---------------------------------------------------------------------------------------------------------------- constants
G = 6.674e-11; CLIGHT = 2.998e8; MSUN = 1.989e30; AU = 1.496e11            # k04's constants
KPC = 3.0857e19; YR = 3.15576e7                                             # FP1's kpc; Julian year
A0_FP0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}                      # FP0's footings: this lane's physical mapping
A0_K04 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}                      # k04's own inputs: used to reproduce its rows
KAPPA = {"canonical": 0.5, "alt": 0.5 * A0_FP0["alt"] / A0_FP0["canonical"]}   # kappa on the observed rho_Lambda (FP0)
G_EXT = 2.32e-10; G_EXT_RANGE = (2.00e-10, 2.64e-10)                       # the Sun's Galactic field and its gate range (FP7 A4)

# ---------------------------------------------------------------------------------------------------------------- the kernel (double)
_GLX, _GLW = np.polynomial.legendre.leggauss(40)


def int_delta(s):
    """Int_0^s Delta(t) dt = Int_0^sqrt(s) 2 w^3/(e^w - 1) dw: 40-point Gauss-Legendre (the integrand is analytic within 2 pi of
    the real axis, so the rule is exact to rounding on [0, 1.6])"""
    if s <= 0:
        return 0.0
    b = math.sqrt(s)
    x = 0.5 * b * (_GLX + 1.0)
    return 0.5 * b * float(np.dot(_GLW, 2.0 * x ** 3 / np.expm1(x)))


def delta(s):
    return s / math.expm1(math.sqrt(s)) if s > 0 else 0.0


def ddelta(s):
    """Delta'(s) (used only for the fixed-a0 controls)"""
    t = math.sqrt(s)
    e = math.expm1(t)
    return (e - 0.5 * t * (e + 1.0)) / e ** 2


T_SAT = brentq(lambda t: math.exp(t) * (1 - t / 2) - 1, 1.2, 1.9, xtol=1e-15, rtol=1e-15)   # Delta'(s) = 0 <=> e^t (1 - t/2) = 1
S_SAT = T_SAT ** 2
D_SAT = delta(S_SAT)
J_SAT = 2 * (S_SAT * D_SAT - int_delta(S_SAT))


def D_l(s):
    return delta(s) if s <= S_SAT else D_SAT


def j_l(s):
    return 2 * (s * delta(s) - int_delta(s)) if s <= S_SAT else J_SAT


def F_l(s):
    return s * D_l(s) - j_l(s)


# ---------------------------------------------------------------------------------------------------------------- route B
def c_of(KB, Zt):
    return (2.0 - KB) / (8.0 * math.pi * Zt)


def r_of(y, c):
    """route B: the four-form equation with the scalar's law substituted, r (1 + c F(y/r)) = 1, solved on (0, 1] by bracketing;
    no root -> the flux sits at the |q| kink (q = 0: the scalar is off)"""
    if y <= 0:
        return 1.0
    h = lambda r: r * (1.0 + c * F_l(y / r)) - 1.0
    lo = 1e-14
    if h(lo) >= 0:
        return 0.0
    return brentq(h, lo, 1.0, xtol=1e-17, rtol=1e-15, maxiter=500)


def u_raw(y, c):
    r = r_of(y, c)
    return r * D_l(y / r) if r > 0 else 0.0


def fd4(fun, y):
    """4-point central derivative, written as differences so that a flat stretch gives exactly 0"""
    h = min(1e-3, 0.02 * y)
    return (8 * (fun(y + h) - fun(y - h)) - (fun(y + 2 * h) - fun(y - 2 * h))) / (12 * h)


class Case:
    def __init__(self, cid, label, KB, Zt):
        self.cid, self.label, self.KB, self.Zt = cid, label, KB, Zt
        self.c = c_of(KB, Zt)
        # used only by the MUTATE envelope: the peak of the unmutated law (bracketed root of its derivative), capped 1e-6 below
        # it so that the capped law is non-decreasing everywhere
        ur = lambda y: u_raw(y, self.c)
        ys = np.linspace(1.5, 3.2, 171)
        ds = [fd4(ur, y) for y in ys]
        i = next(i for i in range(len(ys) - 1) if ds[i] > 0 > ds[i + 1])
        self.y_env = brentq(lambda y: fd4(ur, y), ys[i], ys[i + 1], xtol=1e-13) - 1e-6

    def u(self, y):
        if MUTATE:
            y = min(y, self.y_env)                    # MUTATE: the running maximum -- a kernel made monotone by hand
        return u_raw(y, self.c)

    def du(self, y):
        return fd4(self.u, y)

    def CL(self, y):
        d = self.du(y)
        return math.inf if d == 0 else 1.0 / d


CASES = [Case("K0", "k04 convention, K_B = 0, Zt = 8 (kappa = 1/2; = XR20 'canonical')", 0.0, 8.0),
         Case("K25", "k04 convention, K_B = 0.25, Zt = 8", 0.25, 8.0),
         Case("TA", "tied alt footing: kappa = 0.6043 on rho_Lambda, Zt = 2/kappa^2, K_B = 0 (= XR20 'alt')", 0.0,
              2.0 / KAPPA["alt"] ** 2)]
CASE = {cs.cid: cs for cs in CASES}

# ---------------------------------------------------------------------------------------------------------------- routes A and C (mpmath)
mp.mp.dps = 40
MH1 = mp.mpf("1e-12")
MH2 = mp.mpf("1e-9")


def d1(f, x, h=MH1):
    return (f(x + h) - f(x - h)) / (2 * h)


def d2(f, x, h=MH2):
    return (f(x + h) - 2 * f(x) + f(x - h)) / h ** 2


def d11(f, x, y, h=MH2):
    return (f(x + h, y + h) - f(x + h, y - h) - f(x - h, y + h) + f(x - h, y - h)) / (4 * h * h)


M_T_SAT = mp.findroot(lambda t: mp.exp(t) * (1 - t / 2) - 1, mp.mpf("1.59"))
M_S_SAT = M_T_SAT ** 2


def m_delta(s):
    return s / mp.expm1(mp.sqrt(s)) if s > 0 else mp.mpf(0)


M_D_SAT = m_delta(M_S_SAT)


def m_int(s):
    return mp.quad(lambda w: 2 * w ** 3 / mp.expm1(w), [0, mp.sqrt(s)], method="gauss-legendre")


def m_j(s):
    return 2 * (s * m_delta(s) - m_int(s))


M_J_SAT = m_j(M_S_SAT)


def m_sinv(v):
    """the kernel's rising branch inverted: s with Delta(s) = v (0 < v < Delta_sat), bracketed in t = sqrt(s)"""
    t = mp.findroot(lambda t: t ** 2 / mp.expm1(t) - v, (v, M_T_SAT), solver="anderson", tol=mp.mpf("1e-36"),
                    verify=False, maxsteps=400)
    return t ** 2


def A_L(r, Y, KB, Zt):
    """route A: the four-form + MOND-scalar Lagrangian at FIXED scalar gradient Y (per beta^2 q0^2)"""
    s = m_sinv(mp.sqrt(Y) / r)
    return r * r * Zt / 2 - (2 - KB) / (16 * mp.pi) * r * r * m_j(s)


def A_Pi(r, Y, KB, Zt):
    return d1(lambda x: A_L(x, Y, KB, Zt), r)


def A_Lrr(r, Y, KB, Zt):
    return d2(lambda x: A_L(x, Y, KB, Zt), r)


WALL = mp.mpf("1e-8")


def A_Y_on(r, KB, Zt):
    """the on-shell gradient on the fibre through r: Pi(r, Y) = Zt (Pi rises with Y at fixed r)"""
    Yw = (r * M_D_SAT) ** 2 * (1 - WALL)
    return mp.findroot(lambda Y: A_Pi(r, Y, KB, Zt) - Zt, (mp.mpf("1e-10"), Yw), solver="anderson",
                       tol=mp.mpf("1e-28"), verify=False, maxsteps=400)


def A_fold(KB, Zt):
    """route A: the Legendre map q -> Pi at fixed Y degenerates (L_rr|_Y = 0) on shell"""
    rw = mp.findroot(lambda r: A_Pi(r, (r * M_D_SAT) ** 2 * (1 - WALL), KB, Zt) - Zt, (mp.mpf("0.9"), mp.mpf("0.99999")),
                     solver="anderson", tol=mp.mpf("1e-24"), verify=False, maxsteps=400)
    g = lambda r: A_Lrr(r, A_Y_on(r, KB, Zt), KB, Zt)
    ra, rb = rw + mp.mpf("2e-5"), mp.mpf("0.9999")
    ga, gb = g(ra), g(rb)
    r_f = mp.findroot(g, (ra, rb), solver="anderson", tol=mp.mpf("1e-16"), verify=False, maxsteps=400)
    Y_f = A_Y_on(r_f, KB, Zt)
    JY = d1(lambda YY: r_f * r_f * m_j(m_sinv(mp.sqrt(YY) / r_f)), Y_f)
    return dict(r=r_f, Y=Y_f, u=mp.sqrt(Y_f), y=JY * mp.sqrt(Y_f), JY=JY, r_wall=rw, g_lo=ga, g_hi=gb,
                resid_Pi=A_Pi(r_f, Y_f, KB, Zt) - Zt, resid_Lrr=A_Lrr(r_f, Y_f, KB, Zt))


def A_schur(r, Y, KB, Zt):
    """route A's primal Schur complement: C_L,eff = J_Y + 2 Y [J_YY + k J_Yr^2 / L_rr|_Y] (valid off the kernel's wall)"""
    k = (2 - KB) / (16 * mp.pi)
    Jf = lambda rr, YY: rr * rr * m_j(m_sinv(mp.sqrt(YY) / rr))
    JY = d1(lambda YY: Jf(r, YY), Y)
    JYY = d2(lambda YY: Jf(r, YY), Y)
    JYr = d11(Jf, r, Y)
    Lrr = A_Lrr(r, Y, KB, Zt)
    return dict(y=JY * mp.sqrt(Y), CL=JY + 2 * Y * (JYY + k * JYr ** 2 / Lrr), Lrr=Lrr)


def m_Dl(s):
    return m_delta(s) if s <= M_S_SAT else M_D_SAT


def m_jl(s):
    return m_j(s) if s <= M_S_SAT else M_J_SAT


def C_Ls(r, y, KB, Zt):
    """route C: the dual (flux) function at fixed matter flux y"""
    s = y / r
    return r * r * Zt / 2 + (2 - KB) / (16 * mp.pi) * r * r * (2 * s * m_Dl(s) - m_jl(s)) - Zt * r


def C_state(y, KB, Zt):
    y = mp.mpf(y)
    r = mp.findroot(lambda x: d1(lambda z: C_Ls(z, y, KB, Zt), x), (mp.mpf("1e-6"), mp.mpf(1)), solver="anderson",
                    tol=mp.mpf("1e-28"), verify=False, maxsteps=400)
    f = lambda a, b: C_Ls(a, b, KB, Zt)
    Lrr = d2(lambda a: f(a, y), r)
    Lyy = d2(lambda b: f(r, b), y)
    Lry = d11(f, r, y)
    k = (2 - KB) / (16 * mp.pi)
    duy = (Lyy - Lry ** 2 / Lrr) / (2 * k)
    s = y / r
    u = r * m_Dl(s)
    return dict(y=y, r=r, s=s, u=u, Lrr=Lrr, Lry=Lry, Lyy=Lyy, duy=duy, CL=1 / duy, CT=y / u)


def C_fold(KB, Zt):
    prev = None
    for i in range(200, 252, 2):
        y = mp.mpf(i) / 100
        st = C_state(y, KB, Zt)
        if st["s"] > M_S_SAT - mp.mpf("0.005"):
            return None
        if prev is not None and prev[1] > 0 > st["duy"]:
            return mp.findroot(lambda yy: C_state(yy, KB, Zt)["duy"], (prev[0], y), solver="anderson",
                               tol=mp.mpf("1e-16"), verify=False, maxsteps=200)
        prev = (y, st["duy"])
    return None


# ================================================================================================================ C controls
banner("C   CONTROLS: k04's committed rows, XR20's T2f number, the SPARC loader, the kernel's constants")
env1 = dict(os.environ)
env1.pop("MUTATE", None)
p04 = subprocess.run([sys.executable, os.path.join(REPO, K04_PY)], cwd=REPO, env=env1, capture_output=True, text=True,
                     timeout=900)
k04_committed = rd(K04_OUT)
k04_lines = k04_committed.rstrip("\n").split("\n")
k04_body = "\n".join(k04_lines[:-1])
c0_ok = (p04.returncode == 0 and k04_lines[-1].strip() == "rc=0" and p04.stdout.rstrip("\n") == k04_body.rstrip("\n"))
f6_line = next((l for l in p04.stdout.splitlines() if "F6 [stability]" in l), "")
check("C0", "CONTROL: k04's own script, run unmodified from the repository root, reproduces its committed .out verbatim",
      f"rc = {p04.returncode}; {len(k04_lines) - 1} lines identical: {p04.stdout.rstrip(chr(10)) == k04_body.rstrip(chr(10))}; "
      f"committed F6 row: '{f6_line.strip()[:150]}...'", c0_ok,
      "every F-row this lane re-examines is k04's own, as committed")
# C0b: route B in k04's convention against k04's printed F3 and F5 rows
c0b_rows = []
for KB in (0.0, 0.25):
    parts = []
    for s0 in (0.01, 0.1, 1.0, 2.54, 10.0, 100.0, 1e3):
        a0 = A0_K04["canonical"]
        gN = s0 * a0
        r = r_of(s0, c_of(KB, 8.0))
        s = gN / (a0 * r) if r > 0 else math.inf
        gobs_p = gN + a0 * r * (D_l(s) if r > 0 else 0.0)
        gobs_0 = gN + a0 * D_l(s0)
        parts.append(f"s={s0:g}: {r:.4f} ({math.log10(gobs_p / gobs_0):+.4f} dex)")
    c0b_rows.append(f"    F3: K_B = {KB:.2f} canonical: a0_loc/a0 (Delta log g_obs): " + ", ".join(parts))
for foot, a0 in A0_K04.items():
    parts = []
    for kau in (2, 3, 5, 10, 20):
        gN = G * 1.5 * MSUN / (kau * 1e3 * AU) ** 2
        r = r_of(gN / a0, c_of(0.0, 8.0))
        parts.append(f"{r:.3f} (dgamma_v {0.1155 * math.log(r):+.4f})")
    c0b_rows.append(f"    F5: {foot:9s} a0_loc/a0 at 2, 3, 5, 10, 20 kAU (1.5 Msun): " + ", ".join(parts))
c0b_hit = [row in k04_committed.split("\n") for row in c0b_rows]
check("C0b", "CONTROL: this lane's route B (bracketed root of the flux equation, its own quadrature) in k04's convention "
      "reproduces k04's committed F3 rows (K_B = 0, 0.25) and F5 rows (both footings) to the printed digits",
      f"{sum(c0b_hit)}/{len(c0b_hit)} rows found verbatim in k04's committed .out", all(c0b_hit),
      "route B solves k04's own equation; k04 iterates it, route B brackets it")
# C1: XR20's own code, run unmodified from a scratch mirror
scratch = os.environ.get("XR31_SCRATCH") or tempfile.mkdtemp(prefix="xr31_")
mirror = os.path.join(scratch, "xr20_mirror" + ("_mutate" if MUTATE else "_main"))
if os.path.isdir(mirror):
    shutil.rmtree(mirror)
for rel in [XR20_PY] + XR20_INPUTS:
    dst = os.path.join(mirror, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(os.path.join(REPO, rel), dst)
shutil.copytree(os.path.join(REPO, SPARC_DIR), os.path.join(mirror, SPARC_DIR))
same_src = sha(os.path.join(REPO, XR20_PY)) == sha(os.path.join(mirror, XR20_PY))
env20 = dict(os.environ)
env20["MUTATE"] = "0"
p20 = subprocess.run([sys.executable, os.path.join(mirror, XR20_PY)], cwd=mirror, env=env20, capture_output=True,
                     text=True, timeout=1800)
key20 = lambda l: "k04's saturated nu_RAR" in l and "peaks at y =" in l
l20_new = next((l for l in p20.stdout.splitlines() if key20(l)), None)
l20_old = next((l for l in rd(XR20_OUT).splitlines() if key20(l)), None)
c1_ok = p20.returncode == 0 and same_src and l20_new is not None and l20_old is not None and l20_new.strip() == l20_old.strip()
P(f"    XR20's T2f line (fresh run, scratch mirror): {(l20_new or 'NOT FOUND').strip()}")
check("C1", "CONTROL: XR20's own script (byte-identical copy, run from a scratch mirror with its inputs copied; nothing in the "
      "repository written) reproduces its committed T2f line for k04's kernel verbatim",
      f"XR20 rc = {p20.returncode}; source sha256 identical: {same_src}; line identical to the committed .out: "
      f"{l20_new is not None and l20_old is not None and l20_new.strip() == l20_old.strip()}", c1_ok)
m20 = re.search(r"peaks at y = ([0-9.]+) \(canonical\) / ([0-9.]+) \(alt\).*u\(100\) = ([0-9.]+)", l20_old or "")
xr20_pk = {"canonical": float(m20.group(1)), "alt": float(m20.group(2))} if m20 else {}
xr20_u100 = float(m20.group(3)) if m20 else float("nan")
# C1b: this lane's route B in XR20's convention, on XR20's own grid (argmax), and the precise fold vs the grid value
c1b = {}
for foot in ("canonical", "alt"):
    eps = KAPPA[foot] ** 2 / (8 * math.pi)
    ys_ = np.logspace(-1, math.log10(0.9 * 2.0 / eps), 400)
    us_ = np.array([u_raw(y, eps) for y in ys_])
    i_pk = int(np.argmax(us_))
    step = float(ys_[i_pk + 1] - ys_[i_pk])
    yfine = brentq(lambda y: (u_raw(y + 1e-4, eps) - u_raw(y - 1e-4, eps)), 2.0, 2.49, xtol=1e-12)
    c1b[foot] = dict(grid_peak=float(ys_[i_pk]), grid_step=step, fold=yfine, u100=u_raw(100.0, eps))
c1b_ok = (bool(xr20_pk) and all(f"{c1b[f]['grid_peak']:.2f}" == f"{xr20_pk[f]:.2f}" for f in c1b)
          and all(abs(c1b[f]["fold"] - xr20_pk[f]) <= c1b[f]["grid_step"] for f in c1b)
          and f"{c1b['canonical']['u100']:.3f}" == f"{xr20_u100:.3f}")
check("C1b", "CROSS-CHECK: this lane's solver in XR20's convention (c = kappa^2/8 pi, K_B = 0) on XR20's own 400-point grid "
      "returns XR20's printed peaks and u(100); the precise fold lies within one grid step of each",
      "; ".join(f"{f}: grid argmax {v['grid_peak']:.4f} (XR20 {xr20_pk.get(f, float('nan')):.2f}), precise fold {v['fold']:.4f}, "
                f"grid step {v['grid_step']:.3f}" for f, v in c1b.items()) + f"; u(100) {c1b['canonical']['u100']:.4f} "
      f"(XR20 {xr20_u100:.3f})", c1b_ok,
      "XR20's 2.40 / 2.31 are grid values of a real fold; the precise numbers are H1's")
OUT["numbers"]["C1b"] = c1b
# C2: SPARC loader
GAL = []
for fn in sorted(os.listdir(os.path.join(REPO, SPARC_DIR))):
    if not fn.endswith("_rotmod.dat"):
        continue
    try:
        d_ = np.genfromtxt(os.path.join(REPO, SPARC_DIR, fn), comments="#")
    except Exception:
        continue
    if d_.ndim != 2 or d_.shape[1] < 6:
        continue
    GAL.append(d_[:, :6])


def sparc_y(U, a0):
    ys, gid = [], []
    for ig, d_ in enumerate(GAL):
        R, Vobs, eV, Vgas, Vdisk, Vbul = (d_[:, i] for i in range(6))
        Rm = R * KPC
        Vbar2 = np.sign(Vgas) * Vgas ** 2 + U * Vdisk ** 2 + 1.4 * U * Vbul ** 2
        gb = Vbar2 * 1e6 / Rm
        go = (Vobs * 1e3) ** 2 / Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vobs > 0)
        ys.extend((gb[ok] / a0).tolist())
        gid.extend([ig] * int(ok.sum()))
    return np.array(ys), np.array(gid)


n70 = len(sparc_y(0.7, A0_FP0["canonical"])[0])
n_fp7 = int(sum(((d_[:, 1] > 0) & (d_[:, 2] > 0)).sum() for d_ in GAL))
check("C2", "CONTROL: the SPARC loader reads 175 galaxies and reproduces FP7's count of 3391 points under FP7's own selection "
      "(V_obs > 0, errV > 0); the RAR cuts of FP1 (Upsilon_bul = 1.4 Upsilon, g_bar > 0, g_obs > 0) leave the reported number at "
      "Upsilon = 0.7", f"{len(GAL)} galaxies; FP7 selection {n_fp7} points; with FP1's RAR cuts at Upsilon = 0.7: {n70} points",
      len(GAL) == 175 and n_fp7 == 3391,
      "C2 was re-specified after debug run 1 (see the README): the pre-declared text compared FP7's count with FP1's RAR cuts, "
      "which drop the 2 points whose gas term makes g_bar <= 0")
# C3: the kernel's constants
k01 = rd(K01_OUT)
m01 = re.search(r"nu_RAR saturates at s = ([0-9.]+), Delta = ([0-9.]+)", k01)
m04 = re.search(r"I = ([0-9.]+)\)", k04_committed)
c3_ok = bool(m01 and m04) and f"{S_SAT:.3f}" == m01.group(1) and f"{D_SAT:.4f}" == m01.group(2) and f"{J_SAT:.4f}" == m04.group(1)
check("C3", "CONTROL: the kernel's constants (exact saturation point: e^t (1 - t/2) = 1, t = sqrt(s)) equal the record's printed "
      "values (k01: s_sat, Delta_sat; k04 F2: I = j_sat)",
      f"s_sat = {S_SAT:.6f} (k01 {m01.group(1) if m01 else '?'}), Delta_sat = {D_SAT:.6f} ({m01.group(2) if m01 else '?'}), "
      f"j_sat = {J_SAT:.6f} ({m04.group(1) if m04 else '?'}); 40-digit route: s_sat {mp.nstr(M_S_SAT, 12)}, Delta_sat "
      f"{mp.nstr(M_D_SAT, 12)}, j_sat {mp.nstr(M_J_SAT, 12)}", c3_ok)
OUT["numbers"]["kernel"] = dict(s_sat=S_SAT, D_sat=D_SAT, j_sat=J_SAT)

# ================================================================================================================ A algebra
banner("A   THE ALGEBRA (sympy on generic kernels, then k04's): k04's F3 equation, the fold identity, F6's quantity, the "
       "saturated branch")
r_, Zt_, KB_, s_, D_, Dp_, jv_, F_, c_ = sp.symbols("r Z_t K_B s Delta Deltap j F c", real=True)
kk = (2 - KB_) / (16 * sp.pi)
# A1: dL/dr at fixed Y, by the chain rule with j'(s) = 2 s Delta'(s) and ds/dr|_Y from Y = r^2 Delta(s)^2 = const
ds_dr = sp.solve(sp.Eq(sp.diff(r_ ** 2, r_) * D_ ** 2 + r_ ** 2 * 2 * D_ * Dp_ * sp.Symbol("sr"), 0), sp.Symbol("sr"))[0]
dL_dr = r_ * Zt_ - 2 * kk * r_ * jv_ + (-kk * r_ ** 2 * 2 * s_ * Dp_) * ds_dr
a1_eq = sp.simplify(dL_dr - r_ * (Zt_ + (2 - KB_) * (s_ * D_ - jv_) / (8 * sp.pi))) == 0
JY_ = sp.simplify((r_ ** 2 * 2 * s_ * Dp_) / (r_ ** 2 * 2 * D_ * Dp_))     # dJ/dY at fixed r: J = r^2 j(s), Y = r^2 Delta^2
a1_JY = sp.simplify(JY_ - s_ / D_) == 0
check("A1", "k04's F3 equation re-derived: dL/dr|_Y = r [Zt + (2 - K_B)(s Delta - j)/(8 pi)] (the three-form's conserved "
      "conjugate) and J_Y = s/Delta, so the scalar's law J_Y g_phi = g_N is y = s r",
      f"ds/dr|_Y = {ds_dr}; conjugate identity {a1_eq}; J_Y = s/Delta {a1_JY}", a1_eq and a1_JY)
# A2: the fold identity
rr_ = 1 / (1 + c_ * F_)
Fp = D_ - s_ * Dp_                                                        # dF/ds = Delta - s Delta'
du_ds = sp.diff(rr_ * D_, F_) * Fp + sp.diff(rr_ * D_, D_) * Dp_      # u = r(F) Delta along the curve
dy_ds = sp.diff(s_ * rr_, s_) + sp.diff(s_ * rr_, F_) * Fp
Nexp = Dp_ * (1 + c_ * (F_ + s_ * D_)) - c_ * D_ ** 2
Lrr_on = Zt_ * (1 + c_ * F_ - c_ * Fp * D_ / Dp_)                         # d/dr[r (Zt + 2k F)] at fixed Y, 2k = c Zt
a2_u = sp.simplify(du_ds - Nexp / (1 + c_ * F_) ** 2) == 0
a2_L = sp.simplify(Lrr_on - Zt_ * Nexp / Dp_) == 0
a2_y = sp.simplify(dy_ds - (1 + c_ * (F_ - s_ * Fp)) / (1 + c_ * F_) ** 2) == 0
check("A2", "THE FOLD IDENTITY: on shell L_rr|_Y = Zt N/Delta' and du/ds = N/(1 + cF)^2 with N = Delta'(1 + c(F + s Delta)) - "
      "c Delta^2, so the Legendre map q -> Pi at fixed Y degenerates exactly where the slaved force peaks; dy/ds = "
      "(1 + c(F - s F'))/(1 + cF)^2, so C_L,eff = dy/du = (1 + c(F - sF'))/N",
      f"du/ds {a2_u}; L_rr|_Y {a2_L}; dy/ds {a2_y}", a2_u and a2_L and a2_y,
      "F6's Z_eff = Pi/q = Zt (1 + cF) is the secant; the stability-relevant quantity is the tangent L_rr|_Y ~ N, or C_L,eff ~ 1/N")
# A3: F >= 0 for k04's kernel
ss = sp.symbols("s", positive=True)
Dk = ss / (sp.exp(sp.sqrt(ss)) - 1)
ratio_expr = (Dk - ss * sp.diff(Dk, ss)) / Dk - sp.sqrt(ss) / 2 * sp.exp(sp.sqrt(ss)) / (sp.exp(sp.sqrt(ss)) - 1)
ratio_sym = sp.simplify(ratio_expr) == 0
ratio_num = max(abs(float(ratio_expr.subs(ss, sp.Rational(v)).evalf(30))) for v in ("1/1000", "1/10", "1", "5/2", "7", "40"))
ratio = 0 if (ratio_sym or ratio_num < 1e-25) else ratio_num
sgrid = np.geomspace(1e-3, 1e4, 60)                                      # k04's own F6 grid
Fk04 = [F_l(s) for s in sgrid]
sdense = np.geomspace(1e-6, 1e4, 4001)
Fd = np.array([F_l(s) for s in sdense])
dF_ok = all((delta(s) - s * ddelta(s)) > 0 for s in np.geomspace(1e-6, S_SAT, 400))
a3_ok = ratio == 0 and min(Fk04) > 0 and Fd.min() > 0 and dF_ok
check("A3", "F6'S QUANTITY IS POSITIVE BY CONSTRUCTION: for k04's kernel F' = Delta - s Delta' = Delta (sqrt(s)/2) e^sqrt(s)/"
      "(e^sqrt(s) - 1) > 0 (F' = Delta_sat on the saturated branch) and F(0) = 0, so F >= 0 and F6's Z_eff = Z (1 + cF) >= Z at "
      "every s -- whatever the slaved kernel does",
      f"identity (sympy {ratio_sym}, 30-digit spot values {ratio_num:.1e}) {ratio == 0}; F' > 0 on (0, s_sat) {dF_ok}; min F on k04's own 60-point grid {min(Fk04):.3e} (k04 printed "
      f"1.05e-05); min F on 1e-6..1e4 {Fd.min():.3e}", a3_ok,
      "F = Y J_Y - J >= 0 is the Legendre-positivity of any kernel convex in Y: F6 can only fail for a kernel that is not a kernel")
# A4: the saturated branch
cs_, Ds_, js_, yv_ = sp.symbols("c D_sat j_sat y", positive=True)
rr_sat = sp.solve(sp.Eq(r_ * (1 + cs_ * (Ds_ * yv_ / r_ - js_)), 1), r_)[0]
du_sat = sp.simplify(sp.diff(rr_sat * Ds_, yv_))
yoff_sat = sp.solve(sp.Eq(rr_sat, 0), yv_)[0]
CL_sat = sp.simplify(1 / du_sat)
a4_ok = (sp.simplify(rr_sat - (1 - cs_ * Ds_ * yv_) / (1 - cs_ * js_)) == 0 and sp.simplify(du_sat + cs_ * Ds_ ** 2 / (1 - cs_ * js_)) == 0
         and sp.simplify(yoff_sat - 1 / (cs_ * Ds_)) == 0)
CLsat_num = {cs.cid: -(1 - cs.c * J_SAT) / (cs.c * D_SAT ** 2) for cs in CASES}
YOFF_A4 = {cs.cid: 1.0 / (cs.c * D_SAT) for cs in CASES}
check("A4", "THE SATURATED BRANCH: the flux equation is linear there, r = (1 - c D_sat y)/(1 - c j_sat); the slaved force FALLS "
      "at du/dy = -c D_sat^2/(1 - c j_sat) to zero at y_off = 1/(c D_sat); C_L,eff = -(1 - c j_sat)/(c D_sat^2) < 0",
      f"r = {rr_sat}; du/dy = {du_sat}; y_off = {yoff_sat}; C_L,eff: " +
      ", ".join(f"{cid} {v:.2f} (y_off {YOFF_A4[cid]:.2f})" for cid, v in CLsat_num.items()), a4_ok,
      "k04's kernel is FLAT above s_sat (the bounded boost); a0_loc falling with g_N tilts that flat branch downward")
# A5: uniqueness of the flux root (the restricted sense)
a5_sym = sp.simplify((s_ * D_ - jv_) - s_ * (D_ - s_ * Dp_) - (s_ ** 2 * Dp_ - jv_)) == 0
a5_min = {cs.cid: min(1 + cs.c * ((s * s * ddelta(s) - j_l(s)) if s <= S_SAT else -J_SAT) for s in sdense) for cs in CASES}
check("A5", "THE FLUX EQUATION IS WELL-POSED (the restricted sense of F6): dy/ds = (1 + c(s^2 Delta' - j))/(1 + cF)^2 >= "
      "(1 - c j_sat)/(1 + cF)^2 > 0, so r(y) is single-valued: exactly one root, 0 < a0_loc <= a0, at every y below y_off",
      f"F - sF' = s^2 Delta' - j: {a5_sym}; min_s (1 + c(F - sF')): " + ", ".join(f"{k} {v:.5f}" for k, v in a5_min.items()),
      a5_sym and all(v > 0 for v in a5_min.values()))

# ================================================================================================================ H1 the fold
banner("H1  THE FOLD: route A (Legendre map at fixed Y, 40 digits) vs route B (root-finding of the field equations, peak of u)")
FOLD = {}
for cs in CASES:
    t0 = time.time()
    # route B
    ys_scan = np.linspace(0.5, 3.2, 271)
    dsc = [cs.du(y) for y in ys_scan]
    yfB = None
    for i in range(len(ys_scan) - 1):
        if dsc[i] > 0 > dsc[i + 1]:
            yfB = brentq(cs.du, ys_scan[i], ys_scan[i + 1], xtol=1e-13)
            break
    lo_, hi_ = 10.0, 1e4                                                  # route B's switch-off: where the flux root disappears
    for _ in range(200):
        mid = 0.5 * (lo_ + hi_)
        if r_of(mid, cs.c) > 0:
            lo_ = mid
        else:
            hi_ = mid
    yoffB = 0.5 * (lo_ + hi_)
    below = np.geomspace(1e-3, (yfB or 2.3) - 1e-3, 120)
    band = np.concatenate([np.linspace((yfB or 2.3) + 1e-3, 3.0, 40), np.geomspace(3.0, yoffB * (1 - 1e-3), 160)])
    d_below = np.array([cs.du(y) for y in below])
    d_band = np.array([cs.du(y) for y in band])
    ufB = cs.u(yfB) if yfB else float("nan")
    # route A
    A = A_fold(cs.KB, cs.Zt)
    # route C
    yfC = C_fold(cs.KB, cs.Zt)
    FOLD[cs.cid] = dict(yfB=yfB, ufB=ufB, yoffB=yoffB, yfA=f_(A["y"]), ufA=f_(A["u"]), rfA=f_(A["r"]),
                        sfA=f_(A["y"] / A["r"]), yfC=(f_(yfC) if yfC is not None else None), dmin_below=float(d_below.min()),
                        dmax_band=float(d_band.max()), n_below=len(below), n_band=len(band),
                        residA=(f_(A["resid_Pi"]), f_(A["resid_Lrr"])), secs=time.time() - t0)
    fd = FOLD[cs.cid]
    sB = "None" if yfB is None else f"{yfB:.12f}"
    sC = "None" if yfC is None else f"{f_(yfC):.12f}"
    P(f"    {cs.cid:4s} {cs.label}")
    P(f"         route A (L_rr|_Y = 0 on shell): y_f = {fd['yfA']:.12f}, u_f = {fd['ufA']:.10f}, a0_loc/a0 = "
      f"{fd['rfA']:.10f}, local s = {fd['sfA']:.8f} (s_sat {S_SAT:.5f}); residuals Pi - Zt = "
      f"{f_(A['resid_Pi']):.1e}, L_rr = {f_(A['resid_Lrr']):.1e}; bracket L_rr {f_(A['g_lo']):.4g} .. {f_(A['g_hi']):.4g}")
    P(f"         route B (peak of u(y)):          y_f = {sB}, u_f = {ufB:.10f}; switch-off y_off = {yoffB:.9f} "
      f"(A4: {YOFF_A4[cs.cid]:.9f})")
    P(f"         route C (dual Schur = 0):         y_f = {sC}")
    P(f"         du/dy: min below the fold {fd['dmin_below']:.3e} ({fd['n_below']} points), max on the band {fd['dmax_band']:.3e} "
      f"({fd['n_band']} points); g_N at the fold = {fd['yfA'] * A0_FP0['canonical']:.3e} / {fd['yfA'] * A0_FP0['alt']:.3e} "
      f"m/s^2 (can / alt a0); {fd['secs']:.1f} s")
    okA_B = yfB is not None and abs(fd["yfA"] - yfB) < 1e-6 and abs(fd["ufA"] - ufB) < 1e-8
    ok_rng = yfB is not None and 2.2 <= yfB <= 2.6
    ok_sgn = yfB is not None and fd["dmin_below"] > 0 and fd["dmax_band"] < 0
    ok_off = abs(yoffB / YOFF_A4[cs.cid] - 1) < 1e-9
    dAB = "n/a" if yfB is None else f"{abs(fd['yfA'] - yfB):.1e}"
    check(f"H1-{cs.cid}", f"THE SLAVED KERNEL FOLDS ({cs.cid}): u(y) peaks at y_f in [2.2, 2.6], routes A and B agree to < 1e-6, "
          "du/dy > 0 below and < 0 on the whole band up to the switch-off y_off = 1/(c D_sat)",
          f"y_f A {fd['yfA']:.9f} / B {sB[:11]} / C {sC[:11]}; |A - B| = {dAB}; y_off {yoffB:.4f}; signs below/band "
          f"{fd['dmin_below'] > 0}/{fd['dmax_band'] < 0}", okA_B and ok_rng and ok_sgn and ok_off,
          "the fold sits just below the kernel's own saturation point: the whole flat (saturated) branch turns non-monotone")
OUT["numbers"]["H1"] = FOLD

# ================================================================================================================ H2 / MONO
banner("H2  THE RAR ITSELF STAYS MONOTONE (the fold is in the scalar's force, not in g_obs); MONO (reported)")
h2 = {}
mono = {}
for cs in CASES:
    yy = np.concatenate([np.geomspace(1e-3, 2.0, 60), np.linspace(2.0, 3.0, 101)[1:], np.geomspace(3.0, FOLD[cs.cid]["yoffB"] * 0.999, 120)])
    dd = np.array([cs.du(y) for y in yy])
    h2[cs.cid] = float(1 + dd.min())
    mono[cs.cid] = bool(dd.min() >= -1e-12)
check("H2", "dg_obs/dg_N = 1 + du/dy >= 0.99 everywhere below y_off (all cases)",
      ", ".join(f"{k}: min {v:.5f}" for k, v in h2.items()), all(v >= 0.99 for v in h2.values()),
      "the RAR shows no fold: the non-monotone quantity is the scalar's own force, which is what its field equation's "
      "ellipticity depends on (the record's health theorem: C_L >= 0 <=> the phantom is non-decreasing, FP7 C1 / FP14 X5)")
check("MONO", "the slaved scalar force u(y) is monotone non-decreasing on (0, y_off) (pre-declared EXPECT FALSE on the main run, "
      "TRUE under MUTATE)", ", ".join(f"{k}: {v}" for k, v in mono.items()), all(mono.values()), load_bearing=False)

# ================================================================================================================ H3 F6 vacuous
banner("H3  F6 IS VACUOUS: the secant stiffness stays >= Z on the band; the tangent stiffness flips at the fold; the dual stays > 0")
h3 = {}
for cs in CASES:
    yfA = FOLD[cs.cid]["yfA"]
    st_lo = C_state(yfA - 0.05, cs.KB, cs.Zt)
    st_hi = C_state(yfA + 0.05, cs.KB, cs.Zt)
    Llo = A_Lrr(st_lo["r"], (st_lo["r"] * m_delta(st_lo["s"])) ** 2, cs.KB, cs.Zt)
    Lhi = A_Lrr(st_hi["r"], (st_hi["r"] * m_delta(st_hi["s"])) ** 2, cs.KB, cs.Zt)
    band_s = [y / r_of(y, cs.c) for y in (2.45, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0) if r_of(y, cs.c) > 0]
    secant = min(cs.c * F_l(s) for s in band_s)
    dual = []
    for y in (0.5, 1.0, yfA - 0.05, yfA + 0.05, 3.0, 10.0, 50.0, 0.97 * YOFF_A4[cs.cid]):
        dual.append(f_(C_state(y, cs.KB, cs.Zt)["Lrr"]))
    h3[cs.cid] = dict(secant_min_on_band=secant, Lrr_below=f_(Llo), Lrr_above=f_(Lhi), s_above=f_(st_hi["s"]),
                      dual_Lrr_min=min(dual))
    P(f"    {cs.cid:4s} F6's Z_eff/Z - 1 = cF on the band: min {secant:.4f} (> 0); tangent L_rr|_Y at y_f -/+ 0.05: "
      f"{mp.nstr(Llo, 6)} / {mp.nstr(Lhi, 6)} (local s {mp.nstr(st_hi['s'], 6)} < s_sat); dual Lstar_rr|_y min over 8 states "
      f"{min(dual):.5f} (Zt {cs.Zt:.4f})")
check("H3", "F6'S CRITERION HOLDS ON THE UNSTABLE BAND (secant c F > 0 there), while the tangent stiffness L_rr|_Y changes sign at "
      "the fold (+ below, - above); the dual stiffness at fixed flux stays positive (the flux equation is well-posed)",
      "; ".join(f"{k}: secant {v['secant_min_on_band']:.3f}, L_rr {v['Lrr_below']:.3g} -> {v['Lrr_above']:.3g}, dual min "
                f"{v['dual_Lrr_min']:.3f}" for k, v in h3.items()),
      all(v["secant_min_on_band"] > 0 and v["Lrr_below"] > 0 > v["Lrr_above"] and v["dual_Lrr_min"] > 0 for v in h3.values()),
      "F6 tests Pi/q, which cannot fail; the Legendre map at fixed scalar gradient folds anyway")
OUT["numbers"]["H3"] = h3

# ================================================================================================================ H4 ellipticity
banner("H4  STATIC ELLIPTICITY ON THE BAND: C_L,eff (route B finite differences vs route C's dual Schur complement), C_T,eff")
YB = [2.45, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0, 150.0]
H4 = {}
for cs in CASES:
    rows = []
    for y in YB:
        if y >= FOLD[cs.cid]["yoffB"] * 0.999:
            continue
        CLb = cs.CL(y)
        st = C_state(y, cs.KB, cs.Zt)
        CLc = f_(st["CL"])
        CT = y / cs.u(y)
        rel = abs(CLb / CLc - 1) if math.isfinite(CLb) else float("inf")
        sat = y / r_of(y, cs.c) > S_SAT
        rows.append(dict(y=y, CL_B=CLb, CL_C=CLc, CT=CT, rel=rel, saturated=sat, s=y / r_of(y, cs.c),
                         CL_A4=(CLsat_num[cs.cid] if sat else None)))
    H4[cs.cid] = rows
    P(f"    {cs.cid:4s} y: C_L,eff route B / route C (rel diff), C_T,eff; saturated-branch constant {CLsat_num[cs.cid]:.4f}")
    for rw in rows:
        P(f"           y = {rw['y']:7.2f} (local s {rw['s']:8.3f}{', sat' if rw['saturated'] else ', unsat'}): C_L {rw['CL_B']:12.4f} / "
          f"{rw['CL_C']:12.4f} ({rw['rel']:.1e}), C_T {rw['CT']:9.4f}")
# the primal Schur complement in the unsaturated slice (route A's Hessian) vs route C at the same state
schur_rows = []
for cs in CASES:
    y = 2.45
    st = C_state(y, cs.KB, cs.Zt)
    AS = A_schur(st["r"], (st["r"] * m_delta(st["s"])) ** 2, cs.KB, cs.Zt)
    schur_rows.append(dict(cid=cs.cid, y=y, yA=f_(AS["y"]), CL_A=f_(AS["CL"]), CL_C=f_(st["CL"])))
    P(f"    {cs.cid:4s} primal Schur (route A's Hessian) at route C's state y = {y}: y back {mp.nstr(AS['y'], 12)}, C_L,eff "
      f"{mp.nstr(AS['CL'], 10)} vs dual {mp.nstr(st['CL'], 10)}")
h4_sign = all(rw["CL_B"] < 0 and rw["CT"] > 0 for rows in H4.values() for rw in rows)
h4_agree = all(rw["rel"] < 1e-6 for rows in H4.values() for rw in rows)
h4_sat = all(abs(rw["CL_B"] / rw["CL_A4"] - 1) < 1e-8 for rows in H4.values() for rw in rows if rw["saturated"])
h4_schur = all(abs(x["CL_A"] / x["CL_C"] - 1) < 1e-8 and abs(x["yA"] - x["y"]) < 1e-10 for x in schur_rows)
check("H4", "STATIC ELLIPTICITY FAILS ON THE BAND: C_L,eff < 0 (C_T,eff > 0) at every band point, route B = route C to 1e-6, "
      "= A4's constant on the saturated branch to 1e-8, and = route A's primal Schur complement in the unsaturated slice",
      f"sign {h4_sign}; B vs C {h4_agree} (max rel {max(rw['rel'] for rows in H4.values() for rw in rows):.1e}); saturated "
      f"constant {h4_sat}; primal Schur {h4_schur}; C_L,eff at y = 20: " +
      ", ".join(f"{k} {next(rw['CL_C'] for rw in v if rw['y'] == 20.0):.2f}" for k, v in H4.items()),
      h4_sign and h4_agree and h4_sat and h4_schur,
      "the scalar's static equation is not elliptic on the band: a static solution there is a saddle of its energy")
OUT["numbers"]["H4"] = {"rows": H4, "primal_schur": schur_rows, "CL_saturated": CLsat_num}

# ================================================================================================================ H5 dynamics
banner("H5  DYNAMICS: the scalar's own sector (inertia-free) and the chain root's committed quadratic form (FP7 C1, FP14 L2)")
fp7 = rd(FP7_OUT)
fp14 = rd(FP14_OUT)


def balanced(txt):
    depth = 0
    for i, ch in enumerate(txt):
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return txt[:i + 1]
    raise ValueError("unbalanced")


lt = next(l for l in fp7.splitlines() if "reduced (psi, phi) system after the lapse and shift constraints: T = " in l)
lv = next(l for l in fp7.splitlines() if l.strip().startswith("V = [["))
T_str = balanced(lt.split("T = ", 1)[1])
V_str = balanced(lv.split("V = ", 1)[1])
detV_str = re.search(r"det V = ([^;]+);", lv).group(1)
c2s, lams, ks, acs, sgs, Cps = sp.symbols("c_2 lam k alpha_c sigma C_phi", real=True)
LOC = {"c_2": c2s, "lam": lams, "k": ks, "alpha_c": acs, "sigma": sgs, "C_phi": Cps}


def S_(t):
    return sp.sympify(t.replace("lambda", "lam"), locals=LOC)


Tm = sp.Matrix(S_(T_str))
Vm = sp.Matrix(S_(V_str))
parse_ok = sp.simplify(Vm.det() - S_(detV_str)) == 0
mpar = re.search(r"alpha_c = ([0-9.eE+-]+), lambda = ([0-9.eE+-]+), c_2 = ([0-9.eE+-]+)", fp7)
ALPHA_C, LAM1, C2 = float(mpar.group(1)), float(mpar.group(2)), float(mpar.group(3))
mlam = re.search(r"lambda_sigma8 >= ([0-9.eE+-]+) vs tracking <= ([0-9.eE+-]+)", fp7)
LAM_S8, LAM_TR = float(mlam.group(1)), float(mlam.group(2))
m14 = re.search(r"omega\^2 = (.*?) \(c_2\), (.*?) \(c_2 -> oo\)", fp14)
W14_c2 = S_(m14.group(1))
W14_inf = S_(m14.group(2))
l2_ok = sp.simplify(W14_c2 - Vm.det() / (Vm[1, 1] * Tm[0, 0])) == 0
Tf = sp.lambdify((c2s, lams), Tm, "mpmath")
Vf = sp.lambdify((ks, acs, sgs, Cps), Vm, "mpmath")
w14c = sp.lambdify((ks, acs, sgs, Cps, c2s), W14_c2, "mpmath")
w14i = sp.lambdify((ks, acs, sgs, Cps), W14_inf, "mpmath")
P(f"    FP7 C1 (committed): T = {T_str};  V = {V_str[:90]}...;  det V parse identity {parse_ok}")
P(f"    FP7's parameters read from its .out: alpha_c = {ALPHA_C:g}, c_2 = {C2:g}, lambda = {LAM1:g} (default), {LAM_TR:g} (tracking "
  f"edge), {LAM_S8:g} (sigma_8 edge); FP14 L2's lambda = 0 formula = det V/(V_22 T_11): {l2_ok}")


def roots(Cphi, lam, sigma=1.0, kk_=1):
    Cphi = mp.mpf("1e30") if not math.isfinite(Cphi) else mp.mpf(Cphi)
    T = Tf(mp.mpf(C2), mp.mpf(lam))
    V = Vf(mp.mpf(kk_), mp.mpf(ALPHA_C), mp.mpf(sigma), Cphi)
    a = T[0, 0] * T[1, 1] - T[0, 1] * T[1, 0]
    b = T[0, 0] * V[1, 1] + T[1, 1] * V[0, 0] - T[0, 1] * V[1, 0] - T[1, 0] * V[0, 1]
    cc = V[0, 0] * V[1, 1] - V[0, 1] * V[1, 0]
    wp = (b + mp.sqrt(b * b - 4 * a * cc)) / (2 * a)
    return f_(cc / (a * wp)), f_(wp)


def efold_yr(w):
    return KPC / (CLIGHT * math.sqrt(-w)) / YR if w < 0 else float("inf")


H5 = {}
for cs in CASES:
    rows = []
    for rw in H4[cs.cid]:
        CLb = rw["CL_B"]
        rt = {lam: roots(CLb, lam) for lam in (LAM1, LAM_TR, LAM_S8)}
        rt01 = roots(CLb, LAM1, 0.1)
        Cc = mp.mpf("1e30") if not math.isfinite(CLb) else mp.mpf(CLb)
        f14c = f_(w14c(1, mp.mpf(ALPHA_C), 1, Cc, mp.mpf(C2)))
        f14i = f_(w14i(1, mp.mpf(ALPHA_C), 1, Cc))
        k_scal = roots(CLb, LAM1, 1.0, 10)[0] / rt[LAM1][0]                # Hadamard: omega^2 ~ k^2 (100 for k -> 10 k)
        rows.append(dict(y=rw["y"], CL=CLb, ratio_par_perp=(CLb / rw["CT"] if math.isfinite(CLb) else float("inf")),
                         w_lam1=rt[LAM1][0], w_track=rt[LAM_TR][0], w_s8=rt[LAM_S8][0], w_sig01=rt01[0],
                         w14_c2=f14c, w14_inf=f14i, efold_lam1=efold_yr(rt[LAM1][0]), efold_s8=efold_yr(rt[LAM_S8][0]),
                         n_neg=sum(1 for x in rt[LAM1] if x < 0), k_scaling=k_scal))
    H5[cs.cid] = rows
    P(f"    {cs.cid:4s} y: omega^2_par/omega^2_perp (scalar sector) | FP7 T,V omega^2_-/(ck)^2 at lambda = 1 / {LAM_TR:g} / "
      f"{LAM_S8:g} (sigma = 1), lambda = 1 sigma = 0.1 | FP14 lambda = 0: c_2 / c_2 -> oo | e-fold at k = 1/kpc (lambda = 1, {LAM_S8:g})")
    for x in rows:
        P(f"           y = {x['y']:7.2f}: {x['ratio_par_perp']:9.3f} | {x['w_lam1']:9.4f} / {x['w_track']:10.3e} / {x['w_s8']:10.3e}, "
          f"{x['w_sig01']:9.3f} | {x['w14_c2']:8.4f} / {x['w14_inf']:9.3f} | {x['efold_lam1']:.3g} yr, {x['efold_s8']:.3g} yr")
# controls at fixed a0 (no four-form)
ctl = {"y=1 (fixed a0, unsaturated)": 1.0 / ddelta(1.0), "saturated wall (fixed a0, C_phi -> oo)": math.inf}
ctl_rows = {}
for lab, Cv in ctl.items():
    rr = {lam: roots(Cv, lam) for lam in (LAM1, LAM_TR, LAM_S8)}
    Cc = mp.mpf("1e30") if not math.isfinite(Cv) else mp.mpf(Cv)
    ctl_rows[lab] = dict(C=Cv, min_root=min(min(v) for v in rr.values()), w14_c2=f_(w14c(1, mp.mpf(ALPHA_C), 1, Cc, mp.mpf(C2))),
                         w14_inf=f_(w14i(1, mp.mpf(ALPHA_C), 1, Cc)))
    P(f"    CONTROL {lab}: C_phi = {Cv:.4g}; smallest omega^2/(ck)^2 over lambda = 1, {LAM_TR:g}, {LAM_S8:g}: "
      f"{ctl_rows[lab]['min_root']:.4g}; FP14 lambda = 0: {ctl_rows[lab]['w14_c2']:.4g} / {ctl_rows[lab]['w14_inf']:.4g}")
h5_ok = (parse_ok and l2_ok and all(x["ratio_par_perp"] < 0 and x["w_lam1"] < 0 and x["w_track"] < 0 and x["w_s8"] < 0
                                     and x["w_sig01"] < 0 and x["w14_c2"] < 0 and x["w14_inf"] < 0 and x["n_neg"] == 1
                                     and abs(x["k_scaling"] / 100 - 1) < 1e-12 for rows in H5.values() for x in rows))
kscal_dev = max(abs(x["k_scaling"] / 100 - 1) for rows in H5.values() for x in rows)
check("H5", "DYNAMICAL INSTABILITY ON THE BAND: omega^2_par/omega^2_perp < 0 in the scalar's own sector (any inertia), and with "
      "C_phi = C_L,eff the chain root's committed quadratic form has exactly one omega^2 < 0 (lambda = 1, 277, 1.07e7; sigma = 1, "
      "0.1), scaling as k^2 (Hadamard), and FP14's lambda = 0 roots are negative, at every band point",
      "; ".join(f"{k}: omega^2_-(y = 20, lambda = 1) = {next(x['w_lam1'] for x in v if x['y'] == 20.0):.3f} (ck)^2, "
                f"e-fold {next(x['efold_lam1'] for x in v if x['y'] == 20.0):.3g} yr at k = 1/kpc" for k, v in H5.items())
      + f"; omega^2(10 k)/omega^2(k) = 100 to {kscal_dev:.1e}",
      h5_ok, "growth ~ k (Hadamard): shorter wavelengths grow faster; the rate depends on the inertia and the mixing, the sign "
      "does not")
check("H5c", "CONTROLS at fixed a0 (no four-form): both roots positive at y = 1 and in the saturated wall's limit; FP14's lambda "
      "= 0 roots positive", "; ".join(f"{k}: min root {v['min_root']:.4g}, FP14 {v['w14_c2']:.4g} / {v['w14_inf']:.4g}"
                                       for k, v in ctl_rows.items()),
      all(v["min_root"] > 0 and v["w14_c2"] > 0 and v["w14_inf"] > 0 for v in ctl_rows.values()))
OUT["numbers"]["H5"] = {"rows": H5, "controls": ctl_rows, "fp7_params": dict(alpha_c=ALPHA_C, c_2=C2, lam=[LAM1, LAM_TR, LAM_S8])}

# ================================================================================================================ H6 mapping
banner("H6  WHERE THE BAND SITS: SPARC, the shell around a solar-mass star, wide binaries (FP0 footings a0 = 9.3603e-11 / 1.1312e-10)")


def band_of(cid):
    fd = FOLD[cid]
    return (fd["yfB"], fd["yoffB"]) if fd["yfB"] is not None else (None, None)


def in_band(y, cid):
    lo, hi = band_of(cid)
    return lo is not None and lo < y < hi


def y_ext_of(g, a0, cs):
    target = g / a0
    return brentq(lambda y: y + cs.u(y) - target, 1e-3, FOLD[cs.cid]["yfA"] - 1e-6, xtol=1e-13)


sparc = {}
for foot, a0 in A0_FP0.items():
    for cid in (("K0", "K25", "TA") if foot == "alt" else ("K0", "K25")):
        for U in (0.5, 0.7, 0.9):
            ys, gid = sparc_y(U, a0)
            lo, hi = band_of(cid)
            m = (ys > lo) & (ys < hi) if lo is not None else np.zeros(len(ys), bool)
            sparc[(foot, cid, U)] = dict(n=len(ys), frac=float(m.mean()), n_band=int(m.sum()), gal=int(len(set(gid[m].tolist()))),
                                         y_max=float(ys.max()), n_off=int((ys >= hi).sum()) if hi else 0)
    P(f"    SPARC, {foot:9s}: fraction of points in the band (galaxies with >= 1 band point; points past y_off) at Upsilon "
      f"0.5 / 0.7 / 0.9:")
    for cid in (("K0", "K25", "TA") if foot == "alt" else ("K0", "K25")):
        P(f"           {cid:4s}: " + " / ".join(f"{sparc[(foot, cid, U)]['frac']:.3f} ({sparc[(foot, cid, U)]['gal']}; "
                                                f"{sparc[(foot, cid, U)]['n_off']})" for U in (0.5, 0.7, 0.9))
          + f"   (max y {sparc[(foot, cid, 0.9)]['y_max']:.1f} at Upsilon 0.9)")
# the RAR shift over SPARC, split by the fold (K0, Upsilon 0.7)
rar = {}
for foot, a0 in A0_FP0.items():
    ys, _ = sparc_y(0.7, a0)
    cs = CASE["K0"]
    sh = np.array([math.log10((y + u_raw(y, cs.c)) / (y + D_l(y))) for y in ys])
    lo, hi = band_of("K0")
    mb = (ys > lo) & (ys < hi) if lo is not None else np.zeros(len(ys), bool)
    rar[foot] = dict(max_below=float(np.abs(sh[ys <= (lo or 0)]).max()) if (lo and (ys <= lo).any()) else 0.0,
                     max_band=float(np.abs(sh[mb]).max()) if mb.any() else 0.0)
    P(f"    RAR shift (K0, Upsilon 0.7, {foot}): max |Delta log g_obs| below the fold {rar[foot]['max_below']:.5f} dex, in the band "
      f"{rar[foot]['max_band']:.5f} dex (static numbers; the band's static solution is unstable)")
check("H6a", "SPARC: the band holds a sizeable fraction of the inner points (reported)",
      "; ".join(f"{f}/{c}/U{U}: {v['frac']:.3f}" for (f, c, U), v in sparc.items() if U == 0.7), True, load_bearing=False)
# the shell around a solar-mass star
GM = G * MSUN
solar = {}
for foot, a0 in A0_FP0.items():
    cs = CASE["K0"]
    lo, hi = band_of("K0")
    rau = lambda yy: math.sqrt(GM / (yy * a0)) / AU
    if lo is None:
        solar[foot] = None
        continue
    ye = y_ext_of(G_EXT, a0, cs)
    ye_rng = [y_ext_of(g, a0, cs) for g in G_EXT_RANGE]
    outer = {"isolated": rau(lo), "aligned": (rau(lo - ye) if lo > ye else math.inf), "perpendicular": rau(math.sqrt(lo ** 2 - ye ** 2)),
             "anti-aligned": rau(lo + ye)}
    inner = {"isolated": rau(hi), "aligned": rau(hi - ye), "perpendicular": rau(math.sqrt(hi ** 2 - ye ** 2)), "anti-aligned": rau(hi + ye)}
    planets = {n: GM / (a * AU) ** 2 / a0 for n, a in {"Mercury": 0.387, "Earth": 1.0, "Saturn": 9.58, "Neptune": 30.05}.items()}
    solar[foot] = dict(y_ext=ye, y_ext_range=ye_rng, outer=outer, inner=inner, planets_y=planets)
    P(f"    1-Msun star ({foot}, K0): scalar OFF inside {inner['isolated']:.0f} AU (y > {hi:.1f}); UNSTABLE shell out to "
      f"{outer['isolated']:.0f} AU in isolation.  With the Galactic field g_ext = {G_EXT:.2e} (y_ext = {ye:.3f}; {ye_rng[0]:.3f}-"
      f"{ye_rng[1]:.3f} over {G_EXT_RANGE[0]:.2e}-{G_EXT_RANGE[1]:.2e}): outer edge aligned / perpendicular / anti-aligned "
      f"{outer['aligned']:.0f} / {outer['perpendicular']:.0f} / {outer['anti-aligned']:.0f} AU, inner edge "
      f"{inner['aligned']:.0f} / {inner['perpendicular']:.0f} / {inner['anti-aligned']:.0f} AU; planets' y: " +
      ", ".join(f"{n} {v:.3g}" for n, v in planets.items()))
check("H6b", "a solar-mass star: the scalar is off inside ~640 AU and unstable in a shell out to ~5000 AU (reported)",
      "; ".join(f"{f}: off < {v['inner']['isolated']:.0f} AU, band to {v['outer']['isolated']:.0f} AU (isolated)"
                for f, v in solar.items() if v), all(v is not None for v in solar.values()), load_bearing=False)
# wide binaries
wb = {}
wb_2k_ok = True
for foot, a0 in A0_FP0.items():
    cs = CASE["K0"]
    lo, hi = band_of("K0")
    ye = solar[foot]["y_ext"] if solar[foot] else float("nan")
    for kau in (2, 3, 5, 10, 20):
        yi = G * 1.5 * MSUN / (kau * 1e3 * AU) ** 2 / a0
        geo = {"isolated": yi, "aligned": yi + ye, "perpendicular": math.sqrt(yi ** 2 + ye ** 2), "anti-aligned": abs(yi - ye)}
        wb[(foot, kau)] = {g: (v, in_band(v, "K0")) for g, v in geo.items()}
        if kau == 2:
            wb_2k_ok = wb_2k_ok and all(b for (_, b) in wb[(foot, kau)].values())
    P(f"    wide binaries 1.5 Msun ({foot}, K0): " + "; ".join(
        f"{kau} kAU y = {wb[(foot, kau)]['isolated'][0]:.2f} [" + "".join("B" if wb[(foot, kau)][g][1] else "-" for g in
                                                                          ("isolated", "aligned", "perpendicular", "anti-aligned")) + "]"
        for kau in (2, 3, 5, 10, 20)) + "   ([B/-] = in the band or not: isolated, aligned, perpendicular, anti-aligned)")
check("H6c", "WIDE BINARIES: DR4's 2 kAU bin (1.5 Msun) lies in the unstable band on both footings, in isolation and for every "
      "orientation of the Galactic field",
      "; ".join(f"{f}: 2 kAU y = {wb[(f, 2)]['isolated'][0]:.2f}, all in band {all(b for (_, b) in wb[(f, 2)].values())}"
                for f in A0_FP0), wb_2k_ok)
OUT["numbers"]["H6"] = dict(sparc={f"{f}|{c}|{U}": v for (f, c, U), v in sparc.items()}, rar_shift=rar, solar=solar,
                            wide_binaries={f"{f}|{k}": {g: [v, b] for g, (v, b) in d.items()} for (f, k), d in wb.items()})

# ================================================================================================================ H7 k04's claims
banner("H7  k04's OTHER HEADLINE CLAIMS AGAINST THE BAND (k04's own inputs)")
h7a = CASE["K0"].u(0.0) == 0.0 and r_of(0.0, CASE["K0"].c) == 1.0 and not in_band(0.0, "K0")
check("H7a", "F1 (sign) and F2 (coefficient) live on the Y = 0 background: r = 1 there and y = 0 lies outside the band -- F6 does not "
      "touch them (F2 remains k04's own FAIL: Z/beta^2 is free)", f"r(0) = {r_of(0.0, CASE['K0'].c)}, 0 in band: {in_band(0.0, 'K0')}", h7a)
cls = {}
for cid in ("K0", "K25"):
    lo, hi = band_of(cid)
    cls[cid] = {s0: ("band" if in_band(s0, cid) else ("off" if (hi is not None and s0 >= hi) else "below")) for s0 in
                (0.01, 0.1, 1.0, 2.54, 10.0, 100.0, 1e3)}
exp_cls = {0.01: "below", 0.1: "below", 1.0: "below", 2.54: "band", 10.0: "band", 100.0: "band", 1e3: "off"}
check("H7b", "F3's rows: s = 0.01, 0.1, 1 lie below the fold (stable, their < 0.0005 dex shifts stand); s = 2.54, 10, 100 lie in "
      "the unstable band (static numbers of an unstable solution); s = 1000 in the switched-off core",
      "; ".join(f"{cid}: " + ", ".join(f"{s0:g} {v}" for s0, v in d.items()) for cid, d in cls.items()),
      all(d == exp_cls for d in cls.values()))
lo, hi = band_of("K0")
planet_y = {n: G * MSUN / (a * AU) ** 2 / A0_K04[f] for f in A0_K04 for n, a in
            {"Mercury": 0.387, "Venus": 0.723, "Earth": 1.0, "Mars": 1.524, "Jupiter": 5.203, "Saturn": 9.58, "Uranus": 19.2,
             "Neptune": 30.05}.items()}
h7c = hi is not None and all(v > hi for v in planet_y.values())
check("H7c", "F4 (monopole screening): every planet lies in the switched-off core (y > y_off) -- a static statement F6 does not "
      "touch; but the core is wrapped in the unstable shell, so its standing needs a stable exterior the construction lacks",
      f"min planet y {min(planet_y.values()):.1f} vs y_off {hi if hi is None else round(hi, 2)}", h7c)
r_off_k04 = math.sqrt(G * MSUN / (YOFF_A4["K0"] * A0_K04["canonical"])) / AU
quoted = [int(x) for x in re.findall(r"(?:inside|r <) (\d+) AU", k04_committed)]
check("H7d", "k04's quoted switch-off radius ('inside 205 AU', 'r < 205 AU') is the radius where g_N = y_off a0 around 1 Msun "
      "(pre-declared EXPECT FALSE)", f"quoted {sorted(set(quoted))} AU vs computed {r_off_k04:.1f} AU (y_off = {YOFF_A4['K0']:.2f}, "
      f"k04's a0 {A0_K04['canonical']:.4e}); ratio {r_off_k04 / (quoted[0] if quoted else float('nan')):.3f}",
      bool(quoted) and all(abs(q - r_off_k04) < 5 for q in quoted), load_bearing=False,
      reading="a hard-coded number in k04's text, not computed by its code; the planets (<= 30 AU) are inside either radius, "
              "so F4's verdict does not change")
f5 = {f: G * 1.5 * MSUN / (2e3 * AU) ** 2 / a0 for f, a0 in A0_K04.items()}
check("H7e", "F5 (DR4's 2 kAU bin, k04's own inputs): the bin lies in the unstable band on both footings, so its dgamma_v = -0.019 / "
      "-0.015 is a number of an unstable static solution, not a prediction",
      ", ".join(f"{f}: y = {v:.2f}, in band {in_band(v, 'K0')}" for f, v in f5.items()), all(in_band(v, "K0") for v in f5.values()))
OUT["numbers"]["H7"] = dict(F3_rows=cls, r_off_k04_AU=r_off_k04, quoted_AU=quoted, F5_2kAU_y=f5)

# ================================================================================================================ verdict
banner("VERDICT AND THE PROPOSED CORRECTION NOTE (for the coordinator; k04's files are not edited)")
fK0, fK25, fTA = FOLD["K0"], FOLD["K25"], FOLD["TA"]
cl20 = {k: next(rw["CL_C"] for rw in v if rw["y"] == 20.0) for k, v in H4.items()}
w20 = {k: next(x["w_lam1"] for x in v if x["y"] == 20.0) for k, v in H5.items()}
fr = {f: sparc[(f, "K0", 0.7)]["frac"] for f in A0_FP0}
if solar.get("canonical") is None:                       # no fold on route B (the MUTATE control): no band to map
    solar = {"canonical": {"inner": {"isolated": float("nan")}, "outer": {"isolated": float("nan")}}}
note = (f"k04 F6 (correction proposed by XR31): F6's Z_eff = Z + (2 - K_B) beta^2 (s Delta - j)/(8 pi) is the flux's secant "
        f"stiffness Pi/q; it is >= Z for every kernel convex in Y (F = s Delta - j = Y J_Y - J >= 0) and cannot fail, so it does not "
        f"test stability.  The test is the slaved scalar's longitudinal coefficient C_L,eff = dg_N/dg_phi at fixed Pi.  On k04's "
        f"own kernel and couplings (F3's Z = 8 beta^2) the slaved force g_phi = a0_loc Delta(g_N/a0_loc) peaks at g_N = "
        f"{fK0['yfA']:.3f} a0 (K_B = 0; {fK25['yfA']:.3f} at K_B = 0.25; {fTA['yfA']:.3f} with kappa tied on the alt footing) and falls "
        f"linearly to zero at {YOFF_A4['K0']:.1f} a0 ({YOFF_A4['K25']:.1f}; {YOFF_A4['TA']:.1f}), so C_L,eff < 0 on the whole band "
        f"({cl20['K0']:.1f} at 20 a0): the static scalar equation is not elliptic there and longitudinal perturbations grow at a rate "
        f"~ k (omega^2 = {w20['K0']:.2f} (ck)^2 in the chain root's quadratic form at lambda = 1).  The band holds "
        f"{100 * fr['canonical']:.0f}% / {100 * fr['alt']:.0f}% of SPARC points (Upsilon 0.7, can / alt), a shell from "
        f"{solar['canonical']['inner']['isolated']:.0f} to {solar['canonical']['outer']['isolated']:.0f} AU around every solar-mass "
        f"star, and wide binaries at 2-5 kAU.  'stable (F6)' should read 'UNSTABLE for {fK0['yfA']:.2f} < g_N/a0 < "
        f"{YOFF_A4['K0']:.0f}: the four-form's feedback tilts the saturated kernel's flat branch downward'.  F1-F2 are unaffected; "
        f"F3's RAR shift stands below {fK0['yfA']:.2f} a0; F4's planets sit in the switched-off core (the '205 AU' should read "
        f"~{r_off_k04:.0f} AU); F5's 2 kAU number is computed on an unstable solution.")
P("  " + note)
OUT["correction_note"] = note

# ================================================================================================================ result
lb_fail = [k for k, v in OUT["checks"].items() if v["load_bearing"] and not v["ok"]]
rep_fail = [k for k, v in OUT["checks"].items() if not v["load_bearing"] and not v["ok"]]
n_pass = sum(1 for v in OUT["checks"].values() if v["ok"])
OUT["summary"] = dict(n_checks=len(OUT["checks"]), n_pass=n_pass, load_bearing_failures=lb_fail, reported_failures=rep_fail,
                      seconds=time.time() - T_START)
rc = 1 if lb_fail else 0
P(f"\n  {n_pass}/{len(OUT['checks'])} checks pass; load-bearing failures: {len(lb_fail)} {lb_fail if lb_fail else ''}; reported "
  f"failures: {rep_fail}; wrote {os.path.basename(JSN)}  ({time.time() - T_START:.0f} s)")
P(f"rc = {rc}")


def _clean(o):
    if isinstance(o, dict):
        return {str(k): _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_clean(v) for v in o]
    if isinstance(o, (mp.mpf,)):
        return float(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, float) and not math.isfinite(o):
        return str(o)
    return o


with open(JSN, "w", encoding="utf-8") as fh:
    json.dump(_clean(OUT), fh, indent=1, default=str)
sys.stdout = sys.__stdout__
TEE.close()
sys.exit(rc)
