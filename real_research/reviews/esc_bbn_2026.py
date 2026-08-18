#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
esc_bbn_2026.py
===============
ROUTE 2 OF THE OPTION-1 ESCAPE PRICING: WHAT DOES THE COSMOLOGICAL/LOCAL NEWTON-CONSTANT SPLIT
G_tilde/G_N COST AT BIG-BANG NUCLEOSYNTHESIS?

THE ESCAPE BEING PRICED (not mine; handed to me).  Option 1 replaces AeST's F(Y,Q) by F(Z,Q),
Z = J^mu J_mu.  Both surviving sector conditions constrain only the TOTAL Z-coefficient
M(Z) = script-F'(Z): static attraction needs M > 0, vector no-ghost needs M < K_B.  Rescaling the
free function, script-J -> s * script-J, gives M = (2-K_B) s mu_phys, satisfying BOTH at EVERY
acceleration provided

        s  <  K_B/(2 - K_B)          [= 0.142857 at K_B = 0.25]

and solar-system screening is untouched because mu_phys -> 1 regardless of s.  The stated but
UNCOMPUTED price: the free-function normalisation is the sole source of the Newton constant under
F(Z), so G_N = Ghat/s, and no-ghost becomes the normalisation-free statement 2 G_tilde < K_B G_N,
i.e. G_tilde/G_N <= K_B/2 = 0.125 versus AeST's 0.875.  That is a ~7x split between the constant
in the Friedmann equation and the constant in the Cavendish experiment.  This file prices it at
BBN.

--------------------------------------------------------------------------------------------------
WHAT THIS FILE DOES, AND WHAT IT DOES NOT
--------------------------------------------------------------------------------------------------
DOES:  (a) establishes which G sits in the Friedmann equation and which is measured locally, and
           derives the ratio as a function of s from the corpus's own committed Option-1 reduction;
       (b) computes Y_p from a from-scratch n<->p freeze-out integration (Born weak rates
           normalised to the neutron lifetime, e+/- annihilation and neutrino decoupling included,
           deuterium-bottleneck closure), validated against the standard-BBN control BEFORE any new
           number is quoted;
       (c) reports the s window BBN allows and intersects it with the no-ghost window;
       (d) re-examines the corpus's standing BBN cap K_B <= 0.25 under this escape -- and finds it
           does NOT survive unchanged, which cuts BOTH ways and is reported as such.

DOES NOT:  a nuclear reaction network.  D/H is NOT COMPUTED here.  Only its direction is stated,
           and it is labelled as such.  Nothing in the verdict rests on it.

--------------------------------------------------------------------------------------------------
THE HEADLINE, STATED BEFORE THE ARITHMETIC SO IT CAN BE CHECKED AGAINST IT
--------------------------------------------------------------------------------------------------
1. G_tilde IS the Friedmann constant here and G_N IS the Cavendish constant, and the ratio is
   R_G = G_tilde/G_N = (1 - K_B/2) * s exactly.  At s = 1 this reproduces published AeST's 0.875
   (the lambda_s -> infinity limit recorded in stage50 PART A) -- that is the control.

2. BBN sees G_tilde.  At K_B = 0.25 the no-ghost ceiling R_G <= 0.125 gives an expansion-rate
   factor S = sqrt(R_G) = 0.354 and Y_p = 0.086 against an observed 0.2449 +/- 0.0040.  That is a
   KILL by ~42 standard deviations of the observational error -- and unlike the corpus's earlier
   linear-fit sigmas, this one comes from an integration that is valid at S = 0.35 because it is
   not a fit.  AND THE KILL DOES NOT DEPEND ON THE ONE MODELLING CHOICE THIS FILE MAKES: a
   CLOSURE-FREE UPPER BOUND, Y_p <= 2 X_n(T = 0.2 MeV) = 0.176, holds whatever the deuterium
   bottleneck does, because X_n only ever decreases and at 0.2 MeV the Saha deuterium fraction is
   1.4e-10, five orders below the observed D/H, so nucleosynthesis provably has not happened yet.
   That bound alone is -17 sigma.  MY FIRST ATTEMPT AT THIS FILE SET THE BOTTLENECK CRITERION AT
   n_D/n_b = 1 AND ITS STANDARD-BBN CONTROL RETURNED Y_p = 0.2175 -- IT FAILED, AND THE FIX WAS TO
   CORRECT THE CRITERION, NOT THE TOLERANCE.  That is recorded here deliberately.

3. BUT THE KILL IS NOT UNIFORM IN K_B, AND SAYING SO WOULD BE THE SEVENTH ERROR.  The no-ghost
   ceiling is R_G < K_B/2, so BBN's requirement R_G ~ 1 is not empty for all K_B -- it demands
   K_B > 2 R_G_min = 1.748, i.e. K_B pushed into the top 13% of its stability range (0, 2).  The
   honest verdict is therefore: DEAD at every K_B the corpus, AeST's own CMB fits, or any published
   AeST value has ever used (0.1 / 0.25 / 0.3 / 0.5), and alive only in a corner K_B in [1.748, 2)
   that no published fit occupies and that costs s >= 7.0, i.e. a free function at least seven
   times its AQUAL-normalised size.  That corner is NAMED, not dismissed, and it is handed on.

4. AND THE ESCAPE VOIDS THE DERIVATION OF THE CORPUS'S OWN K_B <= 0.25 CAP.  That cap (stage50 B3)
   came from R_G = (1 - K_B/2) lambda_s/(1 + lambda_s) with the free-function factor SATURATING at
   1, so BBN's bound on R_G translated into a bound on K_B.  Under F(Z) that factor is 1/s and does
   NOT saturate, so BBN alone no longer caps K_B at all -- it caps the PRODUCT (1 - K_B/2)s.  The
   cap is not "still 0.25"; it is replaced by a one-line constraint on the pair.  Reported against
   interest in both directions: this removes a bound the corpus was leaning on, AND it is what
   opens the K_B -> 2 corner in point 3.

--------------------------------------------------------------------------------------------------
PROVENANCE OF EVERY INPUT (read in this session unless marked)
--------------------------------------------------------------------------------------------------
* Ghat = G_tilde/(1 - K_B/2) and the Option-1 Newtonian coupling
  G_eff = G_tilde/[(1 - K_B/2) J_Z(infinity)]:
  READ from real_research/reviews/opt1_gates_2026.py checks D6a/D6b/D7 and
  real_research/reviews/opt1_legality_2026.py (the Psi equation div[J_Z grad Psi] = 4 pi Ghat rho).
* AeST action, background relations 8 pi G_tilde rho = Q K' - K etc., and Ybar = 0:
  READ from real_research/bridge1_aest_equations.md (verbatim-from-source section, 2026-08-14).
* G_cos = G_ae/(1 + (c_13 + 3c_2)/2) = G_tilde for AeST, and the helium bound
  |G_cos/G_N - 1| <~ 1/8 (Oost, Mukohyama & Wang PRD 97, 124023, Eqs. 3.6/3.7, sourced there to
  Carroll & Lim): SECOND-HAND, read from nbody_2026/stage50_kb_settled_bbn_bound_2026.py.
  Marked UNVERIFIED against the papers themselves.  It is used ONLY as a cross-check on this
  file's own independently computed bound, never as the bound.
* Y_p(obs) = 0.2449 +/- 0.0040: corpus standing value (stage50 line 109); consistent with
  Aver, Olive & Skillman 2015 -- UNVERIFIED against that paper in this session.
* K_B standing range [2.1e-4, 2) no-ghost, [2.1e-4, 0.25] with BBN: READ from RETRACTIONS.md
  (the 2026-08-17 adjudication entry) and opus_48_extended_research/papers/THE_FIELD_THEORY.md.
* Weak-interaction physics (Q = 1.29333 MeV, m_e = 0.511 MeV, tau_n = 879.4 s, B_D = 2.22457 MeV):
  standard particle data.  The Born rate structure is written out and normalised inside this file;
  no rate formula is copied from anywhere, and the implementation is validated by exact detailed
  balance and by reproducing the free-neutron lifetime by construction.

a0 = kappa c sqrt(G rho_Lambda): canonical 9.3619e-11, alt 1.1279e-10 m/s^2, kappa = 1/2 FITTED
(0.529 +/- 0.034).  Both are reported below for the standing record.  NOTE HONESTLY: a_0 does not
enter this calculation at all.  BBN is a background-expansion test and, by the order-counting
theorem in bridge1_aest_equations.md (Zbar = 0, delta Z = 0), a_0 is absent from the background and
from linear perturbations.  Quoting it here is bookkeeping, not usage.
"""

import sys

import numpy as np
import sympy as sp
from scipy.integrate import quad, solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import brentq

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"\n         {detail}" if detail else ""))
    return True


print(__doc__)

# ---------------------------------------------------------------------------------------------
# standing constants of the framework (reported, per the standing rules; not used in the physics)
# ---------------------------------------------------------------------------------------------
A0_CANON, A0_ALT = 9.3619e-11, 1.1279e-10
KAPPA, KAPPA_ERR = 0.529, 0.034
print("=" * 100)
print("STANDING RECORD (reported per the rules; a_0 does not enter a background-expansion test)")
print("=" * 100)
print(f"    a_0 canonical = {A0_CANON:.4e} m/s^2   a_0 alt = {A0_ALT:.4e} m/s^2")
print(f"    kappa = 1/2 FITTED, measured {KAPPA:.3f} +/- {KAPPA_ERR:.3f}")
print(f"    a_0(alt)/a_0(canon) = {A0_ALT/A0_CANON:.4f} -- a background test cannot distinguish them;")
print("    both footings give the SAME BBN answer because Zbar = 0 removes a_0 from the background.")
print()

# =============================================================================================
print("=" * 100)
print("PART A -- WHICH G IS WHICH, AND THE RATIO AS A FUNCTION OF s")
print("=" * 100)

# --- A1/A2: the background is bit-identical to AeST's, verified on the FRW metric itself -------
t, r = sp.symbols("t r", positive=True)
a = sp.Function("a", positive=True)(t)
x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
coords = [t, x1, x2, x3]
g = sp.diag(-1, a**2, a**2, a**2)
ginv = g.inv()

Gam = [[[sp.simplify(sum(ginv[l, s_] * (sp.diff(g[s_, m], coords[n]) + sp.diff(g[s_, n], coords[m])
                                        - sp.diff(g[m, n], coords[s_])) for s_ in range(4)) / 2)
         for n in range(4)] for m in range(4)] for l in range(4)]

A_lo = sp.Matrix([-1, 0, 0, 0])                      # A_mu, unit timelike: A^mu A_mu = -1
A_up = sp.Matrix([sp.simplify(sum(ginv[m, n] * A_lo[n] for n in range(4))) for m in range(4)])
norm = sp.simplify(sum(A_up[m] * A_lo[m] for m in range(4)))

# nabla_mu A_nu
nab = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        nab[m, n] = sp.simplify(sp.diff(A_lo[n], coords[m])
                                - sum(Gam[l][m][n] * A_lo[l] for l in range(4)))
Fmn = sp.simplify(nab - nab.T)                       # F_mu nu = 2 nabla_[mu A_nu]

# J^mu = A^nu nabla_nu A^mu  (the aether acceleration)
nab_up = sp.zeros(4, 4)
for m in range(4):
    for n in range(4):
        nab_up[m, n] = sp.simplify(sp.diff(A_up[n], coords[m])
                                   + sum(Gam[n][m][l] * A_up[l] for l in range(4)))
J_up = sp.Matrix([sp.simplify(sum(A_up[n] * nab_up[n, m] for n in range(4))) for m in range(4)])
theta = sp.simplify(sum(nab_up[m, m] for m in range(4)))

check(sp.simplify(norm + 1) == 0,
      "A1  the FRW aether A_mu = (-1,0,0,0) satisfies the unit-norm constraint A^mu A_mu = -1",
      f"computed A^mu A_mu = {norm}")

check(Fmn == sp.zeros(4, 4) and all(sp.simplify(J_up[m]) == 0 for m in range(4)),
      "A2  ON FRW, F_mu nu = 0 IDENTICALLY AND J^mu = 0 IDENTICALLY (computed from the metric, not "
      "assumed) -- so Zbar = J^mu J_mu = 0 exactly, matching the task's established premise",
      f"F_mu nu = 0 matrix: {Fmn == sp.zeros(4,4)};  J^mu = {list(J_up)};  and the expansion "
      f"theta = nabla_mu A^mu = {theta} = 3H is nonzero, so the vanishing of F and J is NOT the "
      f"trivial statement that the aether is covariantly constant")

info("A3  CONSEQUENCE (the derivation part (a) asks for).  Option 1 changes the action ONLY by "
     "replacing the free function's first argument Y -> Z.  Both vanish on FRW (Ybar = 0 is "
     "bridge1_aest_equations.md's order-counting result; Zbar = 0 is A2 above), and the terms "
     "2(2-K_B) J.grad phi and -(2-K_B) Y are untouched by Option 1 and vanish on the background "
     "as well.  So the FRW background sector of Option 1 is BIT-IDENTICAL to published AeST's, "
     "whose background relations (bridge1, verbatim from the arXiv source) read "
     "8 pi G_tilde rho_bar = Q K' - K and 8 pi G_tilde P_bar = K.",
     "*** THEREFORE THE FRIEDMANN CONSTANT IS G_tilde -- the coefficient of R in the action -- with "
     "NO K_B renormalisation, which is also what Oost et al. Eq. (3.6) gives for AeST since "
     "c_13 + 3c_2 = 0 (second-hand via stage50, and here corroborated structurally by A2). ***")

# --- A4: the local constant, from the corpus's own committed Option-1 reduction ---------------
KB, s_, lam_s = sp.symbols("K_B s lambda_s", positive=True)
Gt = sp.symbols("G_tilde", positive=True)

Ghat = Gt / (1 - KB / 2)                            # opt1_gates D6a/D7, opt1_legality
G_N = Ghat / s_                                     # G_eff = Gt/[(1-K_B/2) J_Z(inf)], J_Z(inf) = s
R_G = sp.simplify(Gt / G_N)

check(sp.simplify(R_G - (1 - KB / 2) * s_) == 0,
      "A4  *** THE RATIO, DERIVED:  R_G = G_tilde/G_N = (1 - K_B/2) * s = s(2 - K_B)/2 ***",
      "chain: (i) matter is minimally coupled, S_m[g], so the Cavendish constant IS the "
      "quasi-static Poisson coefficient; (ii) opt1_gates_2026.py D7 (READ) gives the Option-1 "
      "Newtonian coupling G_eff = G_tilde/[(1 - K_B/2) J_Z(infinity)]; (iii) the rescaling "
      "script-J -> s script-J sends J_Z -> s mu_phys, hence J_Z(infinity) = s.  "
      f"Result: G_N = {sp.simplify(G_N)}")

# CONTROL: s = 1 must reproduce published AeST
R_AeST_full = (1 - KB / 2) * lam_s / (1 + lam_s)     # stage50 PART A, the F(Y) theory
ctrl = sp.simplify(R_G.subs(s_, 1) - sp.limit(R_AeST_full, lam_s, sp.oo))
check(ctrl == 0 and abs(float(R_G.subs({s_: 1, KB: sp.Rational(1, 4)})) - 0.875) < 1e-12,
      "A5  CONTROL (NAMED): at s = 1 the derived ratio reproduces PUBLISHED AeST's own "
      "G_cosmo/G_local = (1 - K_B/2) lambda_s/(1 + lambda_s) in its lambda_s -> infinity limit, "
      f"= 1 - K_B/2 = {float(R_G.subs({s_:1, KB:sp.Rational(1,4)})):.4f} at K_B = 0.25",
      "control source: nbody_2026/stage50_kb_settled_bbn_bound_2026.py PART A (which in turn "
      "quotes Skordis & Zlosnik's theorem 'G_N > G_tilde always').  This is the structural "
      "difference the task named: in F(Y) the free-function factor SATURATES (lambda_s/(1+lambda_s) "
      "-> 1) and drops out; in F(Z) it is 1/s and does not.")

# --- A6: no-ghost <=> the normalisation-free statement -----------------------------------------
noghost_s = sp.Lt(s_, KB / (2 - KB))
equiv = sp.simplify(sp.solve(sp.Eq(s_, KB / (2 - KB)), s_)[0] * (2 - KB) / 2 - KB / 2)
check(equiv == 0,
      "A6  no-ghost  s < K_B/(2 - K_B)   <=>   R_G < K_B/2   IDENTICALLY (the (2 - K_B) cancels), "
      "i.e. the normalisation-free statement 2 G_tilde < K_B G_N -- the task's claim, verified",
      f"substituting s = K_B/(2-K_B) into R_G = s(2-K_B)/2 gives exactly K_B/2; residual {equiv}")

KB_NUM = 0.25
S_MAX = KB_NUM / (2 - KB_NUM)
RG_MAX = KB_NUM / 2
check(abs(S_MAX - 0.1428571428571) < 1e-10 and abs(RG_MAX - 0.125) < 1e-14,
      f"A7  numbers at the corpus's operative K_B = {KB_NUM}:  s < {S_MAX:.6f},  R_G < {RG_MAX:.4f}",
      f"against AeST's own R_G = {1 - KB_NUM/2:.4f} at s = 1 -- a factor "
      f"{(1 - KB_NUM/2)/RG_MAX:.1f} split between the cosmological and local Newton constants")

info("A8  ASSUMPTIONS, ALL FOUR NAMED (part (a) requires this):",
     "(i) matter minimally coupled to g, so Cavendish measures the quasi-static Poisson "
     "coefficient -- explicit in the action's S_m[g];\n"
     "         (ii) Ghat = G_tilde/(1 - K_B/2) and G_eff = G_tilde/[(1-K_B/2) J_Z(inf)] are taken "
     "from opt1_gates_2026.py D6a/D7, a committed corpus script READ in this session, NOT "
     "re-derived here.  If that reduction is wrong, this route's ratio is wrong with it;\n"
     "         (iii) the rescaling acts on the Z-sector free function only, leaving K(Q) -- and "
     "hence the dust and Lambda -- alone, which is what makes G_tilde the untouched Friedmann "
     "constant;\n"
     "         (iv) eta = n_b/n_gamma inferred from the CMB is insensitive to the split, because "
     "the CMB constrains the baryon LOADING R = 3 rho_b/(4 rho_gamma), a G-free ratio.  If instead "
     "one insisted on reading eta off Omega_b h^2 with a G_N-based critical density, eta would "
     "shift and the BBN numbers below would move -- direction NOT COMPUTED.")

# =============================================================================================
print()
print("=" * 100)
print("PART B -- THE BBN CALCULATION (from scratch; controls first, new numbers only after)")
print("=" * 100)

# --- units: energies in MeV, times in MeV^-1 --------------------------------------------------
HBAR_MEV_S = 6.582119569e-22        # MeV s
G_N_MEV = 6.708830e-45              # Newton's constant in MeV^-2 (= 1/M_Pl^2)
Q_NP = 1.29333                      # MeV, m_n - m_p
M_E = 0.5109989                     # MeV
TAU_N = 879.4                       # s
B_D = 2.224566                      # MeV, deuteron binding energy
M_N = 938.918                       # MeV, mean nucleon mass
ZETA3 = 1.2020569
ETA10 = 6.14                        # 10^10 * n_b/n_gamma, CMB value
ETA = ETA10 * 1e-10

YP_OBS, YP_ERR = 0.2449, 0.0040     # corpus standing value (stage50)


def fd(E, T):
    """Fermi-Dirac occupation, overflow-safe."""
    return 1.0 / (np.exp(np.clip(E / T, -700.0, 700.0)) + 1.0)


# ---- electron/positron thermodynamics (needed for neutrino decoupling and for rho) -----------
def rho_epm(T):
    if T < M_E / 60.0:
        return 0.0
    f = lambda p: p * p * np.sqrt(p * p + M_E * M_E) * fd(np.sqrt(p * p + M_E * M_E), T)
    return 4.0 / (2 * np.pi ** 2) * quad(f, 0.0, 60.0 * T + 20.0 * M_E, limit=200)[0]


def p_epm(T):
    if T < M_E / 60.0:
        return 0.0
    f = lambda p: p ** 4 / np.sqrt(p * p + M_E * M_E) * fd(np.sqrt(p * p + M_E * M_E), T)
    return 4.0 / (6 * np.pi ** 2) * quad(f, 0.0, 60.0 * T + 20.0 * M_E, limit=200)[0]


def g_s_em(T):
    """entropy dof of the electromagnetic plasma (photons + e+-)."""
    s_g = (4.0 * np.pi ** 2 / 45.0) * T ** 3
    s_e = (rho_epm(T) + p_epm(T)) / T
    return (45.0 / (2 * np.pi ** 2 * T ** 3)) * (s_g + s_e)


G_S_HIGH = 2.0 + 3.5                # photons + relativistic e+-  = 5.5


def T_nu_of_T(T):
    """instantaneous-decoupling entropy relation: T_gamma (g_s^EM)^{1/3} a = const, T_nu a = const."""
    return T * (g_s_em(T) / G_S_HIGH) ** (1.0 / 3.0)


rat_late = T_nu_of_T(1e-3) / 1e-3
check(abs(rat_late - (4.0 / 11.0) ** (1.0 / 3.0)) < 2e-4,
      "B1  CONTROL (NAMED: the standard e+- reheating ratio): the entropy relation implemented here "
      f"gives T_nu/T_gamma -> {rat_late:.6f} at T << m_e, against (4/11)^(1/3) = "
      f"{(4.0/11.0)**(1.0/3.0):.6f}",
      "this validates the g_s^EM integration, which sets both the neutrino temperature and the "
      "radiation density that H depends on")

check(abs(g_s_em(50.0) - 5.5) < 1e-3,
      f"B2  CONTROL: g_s^EM(T = 50 MeV) = {g_s_em(50.0):.5f} against the relativistic value 5.5")


def rho_rad(T):
    """total radiation density in MeV^4 at photon temperature T."""
    Tn = T_nu_of_T(T)
    rho_g = (np.pi ** 2 / 15.0) * T ** 4
    rho_n = 3.0 * (7.0 / 8.0) * (np.pi ** 2 / 15.0) * Tn ** 4
    return rho_g + rho_n + rho_epm(T)


gstar_hi = rho_rad(50.0) / ((np.pi ** 2 / 30.0) * 50.0 ** 4)
check(abs(gstar_hi - 10.75) < 2e-3,
      f"B3  CONTROL: g_*(T = 50 MeV) = {gstar_hi:.4f} against the textbook 10.75 "
      "(2 photons + 3.5 e+- + 5.25 nu)")

# ---- Born weak rates, normalised to the neutron lifetime --------------------------------------
# n + nu_e <-> p + e-,  n + e+ <-> p + nubar_e,  n <-> p + e- + nubar_e.
# The Born matrix element is constant; the rate is the phase-space integral
#   int dE_nu E_nu^2 * p_e E_e * (occupations),   with energy conservation fixing the pairing.
# The single overall constant A is fixed by requiring the vacuum decay rate to equal 1/tau_n.

def _pe(Ee):
    return np.sqrt(max(Ee * Ee - M_E * M_E, 0.0))


I_VAC = quad(lambda Ee: _pe(Ee) * Ee * (Q_NP - Ee) ** 2, M_E, Q_NP, limit=200)[0]
GAMMA_N = HBAR_MEV_S / TAU_N        # 1/tau_n expressed in MeV
A_WEAK = GAMMA_N / I_VAC            # MeV^-4


def lam_np(Tg, Tn):
    """total n -> p rate (MeV): n nu -> p e,  n e+ -> p nubar,  n -> p e nubar."""
    hi_n, hi_e = 60.0 * Tn + 5.0, 60.0 * Tg + 5.0
    i1 = quad(lambda Ev: Ev ** 2 * _pe(Ev + Q_NP) * (Ev + Q_NP) * fd(Ev, Tn)
              * (1.0 - fd(Ev + Q_NP, Tg)), 0.0, hi_n, limit=200)[0]
    i2 = quad(lambda Ee: _pe(Ee) * Ee * (Ee + Q_NP) ** 2 * fd(Ee, Tg)
              * (1.0 - fd(Ee + Q_NP, Tn)), M_E, hi_e, limit=200)[0]
    i3 = quad(lambda Ee: _pe(Ee) * Ee * (Q_NP - Ee) ** 2 * (1.0 - fd(Ee, Tg))
              * (1.0 - fd(Q_NP - Ee, Tn)), M_E, Q_NP, limit=200)[0]
    return A_WEAK * (i1 + i2 + i3)


def lam_pn(Tg, Tn):
    """total p -> n rate (MeV): p e -> n nu,  p nubar -> n e+,  p e nubar -> n."""
    hi_n, hi_e = 60.0 * Tn + 5.0, 60.0 * Tg + 5.0
    j1 = quad(lambda Ee: _pe(Ee) * Ee * (Ee - Q_NP) ** 2 * fd(Ee, Tg)
              * (1.0 - fd(Ee - Q_NP, Tn)), Q_NP, hi_e + Q_NP, limit=200)[0]
    j2 = quad(lambda Ev: Ev ** 2 * _pe(Ev - Q_NP) * (Ev - Q_NP) * fd(Ev, Tn)
              * (1.0 - fd(Ev - Q_NP, Tg)), Q_NP + M_E, hi_n + Q_NP, limit=200)[0]
    j3 = quad(lambda Ee: _pe(Ee) * Ee * (Q_NP - Ee) ** 2 * fd(Ee, Tg)
              * fd(Q_NP - Ee, Tn), M_E, Q_NP, limit=200)[0]
    return A_WEAK * (j1 + j2 + j3)


# CONTROL 1: exact detailed balance when the two baths share a temperature.
db_err = []
for T in (0.3, 0.7, 1.0, 2.0, 5.0):
    ratio = lam_pn(T, T) / lam_np(T, T)
    db_err.append(abs(ratio / np.exp(-Q_NP / T) - 1.0))
check(max(db_err) < 1e-8,
      "B4  CONTROL (NAMED: detailed balance): with T_nu = T_gamma the implemented rates satisfy "
      "lambda_pn/lambda_np = exp(-Q/T) to machine precision at T = 0.3, 0.7, 1, 2, 5 MeV",
      f"max relative deviation {max(db_err):.2e}.  This is a nontrivial check on all six phase-space "
      "integrals, their Pauli-blocking factors and their pairings simultaneously")

# CONTROL 2: the cold limit of lambda_np is the free neutron decay rate.
cold = lam_np(1e-4, 1e-4) / GAMMA_N
check(abs(cold - 1.0) < 1e-6,
      f"B5  CONTROL: lambda_np(T -> 0) / (1/tau_n) = {cold:.8f} -- the normalisation reproduces the "
      f"measured neutron lifetime {TAU_N} s by construction")

# CONTROL 3 (NAMED, and the strongest): reproduce the textbook closed-form rate in ITS OWN
# approximation, from this file's own integrals -- no formula is imported, the coefficient is
# DERIVED.  The closed form lambda_np = (255/(tau_n y^5))(12 + 6y + y^2), y = Q/T, is exactly this
# machinery with (i) Maxwell-Boltzmann statistics and no Pauli blocking, (ii) massless electrons in
# the THERMAL integrals, (iii) the physical (massive-electron) tau_n normalisation.  Under (i)+(ii)
#   i1 = i2 = int_0^inf E^2 (E+Q)^2 e^{-E/T} dE = 2T^5 (12 + 6y + y^2),
# so lambda_np = A * 4T^5(12+6y+y^2) = [120 (Q^5/30)/I_vac] * (12+6y+y^2)/(tau_n y^5).
coef_derived = 120.0 * (Q_NP ** 5 / 30.0) / I_VAC
check(abs(coef_derived - 255.0) / 255.0 < 0.01,
      f"B5b CONTROL (NAMED: the textbook closed-form n->p rate).  Taking this file's OWN integrals "
      f"to Maxwell-Boltzmann statistics with massless thermal phase space and the physical tau_n "
      f"normalisation DERIVES the coefficient {coef_derived:.2f}, against the textbook 255 in "
      f"lambda_np = (255/(tau_n y^5))(12 + 6y + y^2)",
      f"agreement {abs(coef_derived-255.)/255.*100:.2f}% (the textbook value is rounded).  The full "
      f"rates used below sit {(1 - lam_np(1.0, 1.0)/(GAMMA_N*255.0/(Q_NP/1.0)**5*(12+6*Q_NP+Q_NP**2)))*100:.0f}% "
      f"below that closed form at T = 1 MeV, which is the known size of the Fermi-blocking plus "
      f"electron-mass correction the closed form drops.  I_vac = {I_VAC/M_E**5:.4f} m_e^5 against "
      f"the standard beta-decay f-value 1.636 (Coulomb correction, ~3%, NOT included -- an omission "
      f"that makes the rates slightly too slow and Y_p slightly too HIGH, i.e. it works AGAINST "
      f"this file's adverse conclusion)")

# ---- tabulate the rates once (they are G-independent) ----------------------------------------
T_HI, T_LO = 12.0, 0.015
TGRID = np.exp(np.linspace(np.log(T_HI), np.log(T_LO), 260))
LNP = np.array([lam_np(T, T_nu_of_T(T)) for T in TGRID])
LPN = np.array([lam_pn(T, T_nu_of_T(T)) for T in TGRID])
TNU = np.array([T_nu_of_T(T) for T in TGRID])
RHO = np.array([rho_rad(T) for T in TGRID])

u = np.log(TGRID)[::-1]
sp_lnp = CubicSpline(u, np.log(LNP[::-1]))
sp_lpn = CubicSpline(u, np.log(LPN[::-1]))
sp_tnu = CubicSpline(u, np.log(TNU[::-1]))
sp_rho = CubicSpline(u, np.log(RHO[::-1]))
sp_dtnu = sp_tnu.derivative()


def solve_Xn(R_G, T_start=10.0, T_end=0.02):
    """integrate dX_n/d(ln T_gamma); R_G = G_Friedmann/G_Cavendish multiplies G in H."""
    Geff = G_N_MEV * R_G

    def rhs(uu, y):
        Tn_ = np.exp(sp_tnu(uu))
        rho = np.exp(sp_rho(uu))
        H = np.sqrt(8.0 * np.pi * Geff * rho / 3.0)
        # a ~ 1/T_nu  =>  dt = -dT_nu/(T_nu H);  d ln T_nu/d ln T_gamma = sp_dtnu
        dt_du = -sp_dtnu(uu) / H
        lnp = np.exp(sp_lnp(uu))
        lpn = np.exp(sp_lpn(uu))
        return [dt_du * (-lnp * y[0] + lpn * (1.0 - y[0]))]

    u0, u1 = np.log(T_start), np.log(T_end)
    Xeq = 1.0 / (1.0 + np.exp(Q_NP / T_start))
    sol = solve_ivp(rhs, (u0, u1), [Xeq], rtol=1e-9, atol=1e-12, dense_output=True,
                    method="LSODA")
    return sol


# THE ONE MODELLING CHOICE IN THIS FILE, STATED PLAINLY.
# The deuterium bottleneck is closed with the Saha criterion n_D/n_b = D_THRESH.  D_THRESH is a
# one-parameter closure standing in for the full reaction network.  It is NOT tuned to Y_p: it is
# fixed at 1e-3, the value at which the textbook bottleneck temperature T_nuc ~ 78 keV comes out at
# the CMB eta, and the standard-BBN control is then checked against 0.247 with no further freedom.
# Its influence on the verdict is scanned over four decades in B11, and the verdict is additionally
# established WITHOUT it in B10b.
D_THRESH = 1.0e-3


def T_nuc_of(sol, thresh=D_THRESH):
    """deuterium bottleneck: Saha n_D/n_b = thresh, with n_D/(n_n n_p) = (3/4)(4pi/(m_N T))^{3/2} e^{B/T}."""
    def f(T):
        uu = np.log(T)
        Xn = float(sol.sol(uu)[0])
        n_g = 2.0 * ZETA3 * T ** 3 / np.pi ** 2
        n_b = ETA * n_g
        val = Xn * (1.0 - Xn) * n_b * 0.75 * (4.0 * np.pi / (M_N * T)) ** 1.5 * np.exp(B_D / T)
        return np.log(val / thresh)
    return brentq(f, 0.02, 0.30, xtol=1e-10)


def Yp_of(R_G, thresh=D_THRESH):
    sol = solve_Xn(R_G)
    Tn_ = T_nuc_of(sol, thresh)
    Xn = float(sol.sol(np.log(Tn_))[0])
    return 2.0 * Xn, Tn_, sol


# ================= CONTROL RUN: standard BBN, R_G = 1 =========================================
Yp_std, Tnuc_std, sol_std = Yp_of(1.0)
np_ratio = None

check(0.238 <= Yp_std <= 0.262,
      f"B6  *** CONTROL (NAMED: STANDARD BBN).  This integrator, run at R_G = 1, gives "
      f"Y_p = {Yp_std:.4f} ***, against the accepted standard-BBN value 0.247 +/- 0.002 -- "
      f"{(Yp_std/0.247-1)*100:+.1f}%",
      "the residual is the expected SIGN and size for a Born-level treatment: Coulomb and "
      "zero-temperature radiative corrections to the weak rates (omitted) SPEED the rates, delaying "
      "freeze-out and LOWERING Y_p by ~1-2%; finite nucleon mass and non-instantaneous neutrino "
      "decoupling contribute at the same level.  So this file's control is high by about the right "
      "amount for the right reason.  NO NEW NUMBER IS QUOTED BELOW WITHOUT THIS CONTROL HAVING "
      "PASSED, and every new number is ALSO quoted as a DIFFERENCE from this control so the offset "
      "cancels to first order")

check(0.072 <= Tnuc_std <= 0.086,
      f"B7  CONTROL: at the fixed closure D_THRESH = {D_THRESH:g} the deuterium bottleneck closes "
      f"at T_nuc = {Tnuc_std*1000:.1f} keV for eta_10 = {ETA10}, against the textbook ~78 keV")

Xn_nuc = Yp_std / 2.0
np_ratio = Xn_nuc / (1.0 - Xn_nuc)
check(0.125 <= np_ratio <= 0.165,
      f"B8  CONTROL: the neutron-to-proton ratio at the bottleneck is n/p = {np_ratio:.4f} = 1/"
      f"{1/np_ratio:.1f}, against the textbook 1/7 at the onset of nucleosynthesis (having frozen "
      f"out near 1/6 and decayed since)")

# ================= the sensitivity, and the corpus cross-check ================================
eps = 0.02
Yp_p, _, _ = Yp_of((1.0 + eps) ** 2)      # S = 1+eps
Yp_m, _, _ = Yp_of((1.0 - eps) ** 2)
dYp_dS = (Yp_p - Yp_m) / (2 * eps)

check(0.12 <= dYp_dS <= 0.24,
      f"B9  CROSS-CHECK AGAINST THE CORPUS (NAMED): dY_p/dS at S = 1 is {dYp_dS:.4f} here, against "
      f"stage50's independent freeze-out integration 0.1753 ({abs(dYp_dS/0.1753-1)*100:.1f}% apart) "
      f"and the published fits' ~0.16 ({abs(dYp_dS/0.16-1)*100:.1f}% apart)",
      "two independent integrations, written years and agents apart, agreeing to this level is the "
      "strongest single validation available here")

# ================= THE NEW NUMBERS ============================================================
print()
print("    R_G = G_tilde/G_N   |   S = sqrt(R_G)   |   T_nuc    |    Y_p    |  (Y_p - obs)/sigma")
print("    " + "-" * 92)
rows = []
for lab, RG in (("no-ghost ceiling, K_B=0.25", RG_MAX),
                ("no-ghost ceiling, K_B=0.10", 0.05),
                ("AeST s=1, K_B=0.25", 1 - KB_NUM / 2),
                ("AeST s=1, K_B=0.10", 0.95),
                ("standard (control)", 1.0),
                ("no-ghost ceiling, K_B=1.75", 0.875),
                ("no-ghost ceiling, K_B=1.99", 0.995)):
    Y, Tn_, _ = Yp_of(RG)
    S = np.sqrt(RG)
    rows.append((lab, RG, S, Tn_, Y))
    print(f"    {lab:26s} {RG:8.4f}  {S:9.4f}   {Tn_*1000:7.2f} keV  {Y:8.4f}   "
          f"{(Y - Yp_std + (Yp_std - YP_OBS) * 0):+9.4f} -> {(Y - Yp_std)/YP_ERR:+7.1f} sig")
print("    (last column: the SHIFT relative to this integrator's own R_G = 1 control, in units of "
      "the observational error 0.0040 -- differencing removes the integrator's ~1% absolute offset)")

Y_kill, Tn_kill, _ = Yp_of(RG_MAX)
shift_kill = (Y_kill - Yp_std) / YP_ERR

check(Y_kill < 0.15 and abs(shift_kill) > 20,
      f"B10 *** THE PRICE, COMPUTED.  At the no-ghost ceiling R_G = {RG_MAX} (K_B = 0.25) the "
      f"expansion rate at T ~ 1 MeV is S = {np.sqrt(RG_MAX):.4f} of standard and "
      f"Y_p = {Y_kill:.4f}, a shift of {shift_kill:+.1f} sigma of the observational error against "
      f"an observed {YP_OBS} +/- {YP_ERR}. ***",
      "mechanism, stated so it can be attacked: a smaller G means a smaller H, so the weak "
      "interactions hold n/p in equilibrium to LOWER temperature (freeze-out T_f ~ G^{1/6}), "
      "leaving fewer neutrons; and the slower expansion then gives those neutrons ~1/S = 2.8x "
      "LONGER to beta-decay before the deuterium bottleneck opens.  Both effects push the same "
      "way, which is why the result is not marginal")

# ---- THE CLOSURE-FREE BOUND: the kill without any bottleneck model at all ---------------------
sol_kill = solve_Xn(RG_MAX)
T_BOUND = 0.2                                        # MeV
Xn_bound = float(sol_kill.sol(np.log(T_BOUND))[0])
Yp_bound = 2.0 * Xn_bound
Xn_bound_std = float(sol_std.sol(np.log(T_BOUND))[0])
n_g_b = 2.0 * ZETA3 * T_BOUND ** 3 / np.pi ** 2
nD_at_bound = (Xn_bound_std * (1 - Xn_bound_std) * ETA * n_g_b * 0.75
               * (4.0 * np.pi / (M_N * T_BOUND)) ** 1.5 * np.exp(B_D / T_BOUND))

check(Yp_bound < 0.20 and nD_at_bound < 1e-8,
      f"B10b *** AND THE KILL SURVIVES WITHOUT ANY BOTTLENECK MODEL AT ALL -- THE DECISIVE CHECK. "
      f"X_n decreases monotonically after freeze-out (only beta decay acts), so for ANY T_nuc below "
      f"{T_BOUND} MeV, Y_p <= 2 X_n({T_BOUND} MeV) = {Yp_bound:.4f}.  And T_nuc IS below "
      f"{T_BOUND} MeV, unconditionally: the Saha deuterium fraction there is n_D/n_b = "
      f"{nD_at_bound:.2e}, {abs(np.log10(nD_at_bound/2.5e-5)):.0f} orders below the observed D/H, so "
      f"nucleosynthesis provably has not begun.  Y_p <= {Yp_bound:.4f} against "
      f"{YP_OBS} +/- {YP_ERR} is {(Yp_bound-YP_OBS)/YP_ERR:+.0f} sigma. ***",
      f"this bound uses only the weak rates (controlled in B4/B5/B5b), the expansion rate, and "
      f"monotonicity of X_n -- no D_THRESH, no network, no fitting formula.  For comparison the "
      f"same bound in the standard case is {2*Xn_bound_std:.4f}, comfortably ABOVE the observed "
      f"value as it must be")

# robustness of the bottleneck criterion (the one modelling choice with real freedom)
rob = []
for th in (1e-5, 1e-4, 1e-3, 1e-2, 1e-1):
    Yc, Tc, _ = Yp_of(1.0, th)
    Yk, Tk, _ = Yp_of(RG_MAX, th)
    rob.append((th, Yc, Tc, Yk, Tk, (Yk - Yc) / YP_ERR))
print()
print("    bottleneck-closure robustness (Saha threshold n_D/n_b, scanned over four decades):")
for th, Yc, Tc, Yk, Tk, sg in rob:
    print(f"      n_D/n_b = {th:8.0e}:  control Y_p = {Yc:.4f} (T_nuc {Tc*1000:5.1f} keV)   "
          f"escape Y_p = {Yk:.4f} (T_nuc {Tk*1000:5.1f} keV)   shift {sg:+6.1f} sigma")
check(all(abs(r[5]) > 25 for r in rob),
      "B11 the verdict is ROBUST to the bottleneck closure over four decades in the threshold "
      "(T_nuc from ~90 keV to ~66 keV): the escape's shift never falls below 25 sigma",
      f"shifts {[f'{r[5]:+.1f}' for r in rob]} -- this was the modelling choice most able to rescue "
      f"the escape, and it does not.  The control's own spread over the same range "
      f"({min(r[1] for r in rob):.4f} to {max(r[1] for r in rob):.4f}) is the honest systematic on "
      f"this file's absolute Y_p, and it is ~20x smaller than the effect being measured")

# ---- the honest rescue attempt: can extra energy density restore H? ---------------------------
need_extra = 1.0 / RG_MAX - 1.0                      # rho must grow by this factor to restore H
dNeff = need_extra * 10.75 / (7.0 / 8.0 * 2.0)
check(dNeff > 20,
      f"B12 RESCUE ATTEMPTED AND FAILED (checked because a favourable result must be attacked as "
      f"hard as an adverse one): H could be restored by ADDING energy density, since only the "
      f"product G_tilde * rho enters.  Restoring H at R_G = {RG_MAX} needs rho_rad to grow by "
      f"{need_extra:.1f}x, i.e. Delta N_eff = {dNeff:+.1f}",
      "against BBN's own N_eff bound and Planck's N_eff = 2.99 +/- 0.17 (the latter second-hand, "
      "UNVERIFIED here) this is excluded by two orders of magnitude in the error.  And it is not "
      "even available in this theory: AeST's dark sector is DUST (rho ~ a^-3, bridge1's background "
      "relations), which at T = 1 MeV is ~1e-6 of the radiation density and cannot be raised to "
      "7x it without destroying the CMB fit it exists to provide")

# ---- second-hand cross-check, used only as corroboration --------------------------------------
OOST_BOUND = 0.125
check(abs(RG_MAX - 1.0) / OOST_BOUND > 5,
      f"B13 CORROBORATION (SECOND-HAND, UNVERIFIED: Oost, Mukohyama & Wang PRD 97, 124023 Eq. 3.7 "
      f"via Carroll & Lim, read from stage50): |G_cos/G_N - 1| <~ 1/8.  The escape's ceiling sits "
      f"at |R_G - 1| = {abs(RG_MAX-1):.3f} = {abs(RG_MAX-1)/OOST_BOUND:.1f}x that published bound",
      "this is quoted ONLY as corroboration of the independent calculation above; the verdict does "
      "not rest on it")

# ---- D/H: NOT COMPUTED -------------------------------------------------------------------------
info("B14 D/H IS **NOT COMPUTED**.  It requires a nuclear reaction network (D(p,g)He3, D(d,n)He3, "
     "D(d,p)T and the He3/T channels), which this file does not implement, and no fitting formula "
     "for it is valid at S = 0.35 -- applying one there would be exactly the 'formula used off its "
     "stated domain' error this project has already made once.",
     "DIRECTION ONLY, and labelled as such: a slower expansion leaves deuterium longer at "
     "burning temperatures, so D/H falls.  Observed D/H = (2.53 +/- 0.03)e-5 (Cooke et al. 2018 -- "
     "quoted from memory, UNVERIFIED, and used for NOTHING here).  Since the observational error is "
     "~1.2% and the escape changes the expansion rate by a factor of 2.8, D/H can only make the "
     "verdict worse.  The verdict below rests on Y_p ALONE and does not need D/H.")

# =============================================================================================
print()
print("=" * 100)
print("PART C -- THE ALLOWED s WINDOW, AND THE INTERSECTION")
print("=" * 100)

# BBN-allowed R_G: |Y_p(R_G) - Y_p(1)| <= n_sigma * sigma_obs, solved numerically
def dY(RG):
    return (Yp_of(RG)[0] - Yp_std) / YP_ERR


bbn_lo = brentq(lambda R: dY(R) + 3.0, 0.30, 1.0, xtol=1e-6)
bbn_hi = brentq(lambda R: dY(R) - 3.0, 1.0, 2.5, xtol=1e-6)
print(f"    BBN-allowed (3 sigma of the helium error, this file's own integration):")
print(f"        R_G = G_tilde/G_N  in  [{bbn_lo:.4f}, {bbn_hi:.4f}]")
print(f"    no-ghost (Option 1, any K_B):  R_G < K_B/2")
print()
print(f"    {'K_B':>8} {'no-ghost R_G <':>16} {'BBN R_G >=':>12} {'compatible?':>13} "
      f"{'required s range':>24}")
print("    " + "-" * 80)
kb_rows = []
for kb in (2.1e-4, 0.1, 0.25, 0.3, 0.5, 1.0, 1.5, 1.75, 1.9, 1.99):
    rg_ceil = kb / 2.0
    ok = rg_ceil > bbn_lo
    if ok:
        s_lo = bbn_lo / (1 - kb / 2)
        s_hi = min(bbn_hi, rg_ceil) / (1 - kb / 2)
        srange = f"[{s_lo:.3f}, {s_hi:.3f})"
    else:
        srange = "EMPTY"
    kb_rows.append((kb, rg_ceil, ok))
    print(f"    {kb:8.4f} {rg_ceil:16.4f} {bbn_lo:12.4f} {('YES' if ok else 'NO'):>13} "
          f"{srange:>24}")

kb_crit = 2.0 * bbn_lo
check(all(not r[2] for r in kb_rows if r[0] <= 0.5),
      f"C1  *** THE INTERSECTION IS EMPTY AT EVERY K_B EVER USED.  For K_B <= 0.5 -- which covers "
      f"the corpus's operative 0.25, its fiducial 0.1, and ALL THREE of AeST's own published CMB "
      f"fits (0.1 / 0.3 / 0.5) -- the no-ghost ceiling R_G < K_B/2 <= 0.25 lies entirely below "
      f"BBN's floor R_G >= {bbn_lo:.3f}.  KILL. ***")

check(kb_crit > 1.7,
      f"C2  AND THE CORNER THAT SURVIVES, NAMED RATHER THAN SUPPRESSED: compatibility first "
      f"becomes possible at K_B > 2 * {bbn_lo:.4f} = {kb_crit:.4f}, i.e. K_B in "
      f"[{kb_crit:.3f}, 2) -- the top {(2-kb_crit)/2*100:.0f}% of the stability range 0 < K_B < 2, "
      f"{kb_crit/0.25:.1f}x above the corpus's operative cap and {kb_crit/0.5:.1f}x above the "
      f"largest K_B AeST itself has ever fitted",
      f"and it is not free: at K_B = 1.9 it requires s in "
      f"[{bbn_lo/(1-1.9/2):.2f}, {min(bbn_hi, 0.95)/(1-1.9/2):.2f}), i.e. a free function "
      f"{bbn_lo/(1-1.9/2):.0f}x its AQUAL normalisation, and R_G < 1 STRICTLY for every K_B < 2, so "
      "this escape can never do BETTER at BBN than AeST already does -- it can only claw back to "
      "AeST's own position by driving K_B to the stability boundary")

info("C3  THE BBN-ALONE CONSTRAINT, handed on in a form any other route can intersect directly:",
     f"BBN alone:      s in [{bbn_lo:.4f}, {bbn_hi:.4f}] / (1 - K_B/2)\n"
     f"         no-ghost:       s < K_B/(2 - K_B)\n"
     f"         joint (both):   EMPTY for K_B <= {kb_crit:.3f}; nonempty only for "
     f"K_B in ({kb_crit:.3f}, 2).")

# --- C4: route 1's window, now visible -------------------------------------------------------
S_ROUTE1 = {0.25: 0.13822, 0.10: 0.050924}          # read from esc_s_window_2026.py header
s_bbn_lo = {kb: bbn_lo / (1 - kb / 2) for kb in S_ROUTE1}
s_bbn_hi = {kb: bbn_hi / (1 - kb / 2) for kb in S_ROUTE1}
gaps = {kb: s_bbn_lo[kb] / S_ROUTE1[kb] for kb in S_ROUTE1}
print()
print("    intersection with ROUTE 1 (its window read from real_research/reviews/esc_s_window_2026.py):")
for kb in (0.25, 0.10):
    print(f"      K_B = {kb:.2f}:  route 1 allows 0 < s < {S_ROUTE1[kb]:.5f};  BBN requires "
          f"s in [{s_bbn_lo[kb]:.4f}, {s_bbn_hi[kb]:.4f}]  ->  EMPTY, gap {gaps[kb]:.1f}x")
check(all(g > 5 for g in gaps.values())
      and all(S_ROUTE1[kb] < kb / (2 - kb) + 1e-9 for kb in S_ROUTE1),
      f"C4  *** INTERSECTION WITH ROUTE 1: EMPTY, BY A FACTOR OF {gaps[0.25]:.1f} AT K_B = 0.25 AND "
      f"{gaps[0.10]:.1f} AT K_B = 0.10. ***  Route 1 (sibling file, READ; its numbers are quoted, "
      f"not recomputed here) reports 0 < s < {S_ROUTE1[0.25]:.5f} at K_B = 0.25 and "
      f"0 < s < {S_ROUTE1[0.10]:.5f} at K_B = 0.10; BBN requires s >= {s_bbn_lo[0.25]:.4f} and "
      f"{s_bbn_lo[0.10]:.4f} respectively",
      "AND THE CONCLUSION IS ROBUST TO WHATEVER ROUTE 1 FINALLY SETTLES ON, by monotonicity: its "
      "window is a SUBSET of the no-ghost window s < K_B/(2 - K_B) (verified numerically above for "
      "both quoted values), and C1 already shows BBN excludes the WHOLE no-ghost window for every "
      "K_B <= 0.5.  So any tightening on route 1's side can only make the intersection emptier, and "
      "this check cannot be overturned by a revision there -- only by a revision to route 1's "
      "no-ghost condition itself, which is the shared premise of both routes")

# --- C5: does the surviving corner ALSO clear route 1?  Asked against my own conclusion. -------
ELL_MAX = 1.0335                                     # route 1's operative tightening factor, READ
print()
print("    the K_B -> 2 corner, tested against ROUTE 1 as well (asked against this file's own "
      "verdict):")
corner_ok = []
for kb in (1.75, 1.80, 1.90, 1.99):
    s1 = kb / ((2 - kb) * ELL_MAX)                   # route 1's operative ceiling
    sl, sh = bbn_lo / (1 - kb / 2), min(bbn_hi / (1 - kb / 2), kb / (2 - kb))
    nonempty = sl < min(sh, s1)
    corner_ok.append(nonempty)
    print(f"      K_B = {kb:.2f}:  route 1 allows s < {s1:8.3f};  BBN+no-ghost needs s in "
          f"[{sl:8.3f}, {sh:8.3f})  ->  {'NON-EMPTY' if nonempty else 'EMPTY'}")
check(any(corner_ok),
      "C5  STATED AGAINST MY OWN VERDICT: the K_B -> 2 corner is NOT killed by route 1 either.  "
      "Applying route 1's own operative ceiling s < K_B/[(2-K_B) * 1.0335] at K_B = 1.9 leaves "
      f"s in [{bbn_lo/(1-1.9/2):.2f}, {1.9/(0.1*ELL_MAX):.2f}) satisfying BOTH routes.  So this "
      "file must NOT be reported as 'the escape is dead full stop'.",
      "what it IS reported as: dead at every K_B the framework, the corpus, or AeST has ever used, "
      "and alive only where K_B sits within 13% of its stability boundary with a free function 7-18x "
      "its AQUAL normalisation -- a region against which NO CMB fit has ever been run, and which "
      "Death 2 (the linear-cosmology degeneracy, where the vector kinetic coefficient enters as "
      "K_B - F_Z(0)) has not been priced at.  That is the next calculation, and it is NOT this one.")

# =============================================================================================
print()
print("=" * 100)
print("PART D -- DOES THIS CHANGE THE CORPUS'S STANDING BBN CAP K_B <= 0.25?")
print("=" * 100)

info("D1  THE STANDING CAP, STATED.  RETRACTIONS.md (2026-08-17 adjudication) and "
     "THE_FIELD_THEORY.md carry: K_B in [2.1e-4, 2) on no-ghost, [2.1e-4, 0.25] with BBN.  The "
     "0.25 comes from stage50 B3: with R_G = (1 - K_B/2) lambda_s/(1 + lambda_s) and the published "
     "helium bound |R_G - 1| <~ 1/8, the lambda_s -> infinity limit gives 1 - K_B/2 >= 7/8, "
     "i.e. K_B <= 0.25.")

kb_cap_derived = 2 * (1 - (1 - OOST_BOUND))
check(abs(kb_cap_derived - 0.25) < 1e-12,
      f"D2  that derivation reproduced: 2 * (1 - 7/8) = {kb_cap_derived:.4f}.  It works ONLY "
      "because the F(Y) free-function factor lambda_s/(1+lambda_s) SATURATES at 1, so BBN's bound "
      "on R_G transfers wholly onto K_B")

check(sp.simplify(sp.limit(lam_s / (1 + lam_s), lam_s, sp.oo) - 1) == 0
      and sp.limit(1 / s_, s_, sp.oo) == 0,
      "D3  *** AND THAT IS EXACTLY WHAT OPTION 1 BREAKS.  Under F(Z) the free-function factor is "
      "1/s, which is UNBOUNDED, not saturating.  So BBN no longer constrains K_B at all on its "
      "own -- it constrains the PRODUCT (1 - K_B/2) s.  THE STANDING CAP K_B <= 0.25 IS NOT VALID "
      "UNDER OPTION 1 AS DERIVED; it must be restated. ***",
      "STATED IN BOTH DIRECTIONS, because it cuts both ways: (i) AGAINST the corpus -- a bound it "
      "has been leaning on since stage50 (and which RETRACTIONS.md notes 'strengthens arguments "
      "that used the BBN cap') simply does not follow in the F(Z) theory, and every downstream "
      "argument that used K_B <= 0.25 must be re-checked if Option 1 is adopted; (ii) FOR the "
      "escape -- removing that cap is the ONLY reason the K_B -> 2 corner in C2 exists at all")

check(True,
      "D4  THE REPLACEMENT, stated so it can be quoted: under Option 1, BBN's content is\n"
      f"         *** (1 - K_B/2) * s  in  [{bbn_lo:.3f}, {bbn_hi:.3f}] ***\n"
      "         and combined with no-ghost s < K_B/(2 - K_B) it becomes a joint constraint whose "
      f"projection onto K_B is  K_B > {kb_crit:.3f}  -- a FLOOR, where the old bound was a CEILING. "
      "The two are incompatible: the corpus's [2.1e-4, 0.25] and Option 1's ({:.3f}, 2) do not "
      "overlap.".format(kb_crit),
      "so the honest one-line summary is not 'the cap is unchanged' and not 'the cap is gone'.  It "
      "is: THE CAP INVERTS INTO A FLOOR, AND THE FLOOR IS SEVEN TIMES THE OLD CEILING")

info("D5  WHAT IS *NOT* PRICED HERE, listed so nobody reads this file as more than it is:",
     "(i) whether K_B in [1.75, 2) survives the OTHER constraints -- the committed CLASS pass, the "
     "third-peak fit, the scalar sound-speed floor 2.1e-4, and Death 2 (the CMB degeneracy) -- is "
     "NOT COMPUTED.  All published AeST CMB fits sit at K_B <= 0.5, so that corner has never been "
     "run;\n"
     "         (ii) whether s >= 8 is compatible with the RAR normalisation is route 1's business, "
     "not this file's.  Note only that mu_phys -> 1 in the Newtonian limit is what makes s drop out "
     "of screening, and it is NOT what makes s drop out of the RAR, where the kernel's own "
     "normalisation is measured;\n"
     "         (iii) GW amplitudes: the task named them as a possible additional cost of the split. "
     "NOT COMPUTED here.")

# =============================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
    ROUTE 2 RESULT:  **KILL** at every K_B the theory has ever been fitted or bounded at, with a
    NAMED surviving corner that is not this framework's.

    (a) DERIVED:  R_G = G_tilde/G_N = (1 - K_B/2) s, from the corpus's own Option-1 reduction
        (opt1_gates D7) plus minimal matter coupling.  Control: s = 1 reproduces published AeST's
        0.875.  No-ghost <=> R_G < K_B/2 verified symbolically.
    (b) PRICED:  at K_B = 0.25 the no-ghost ceiling R_G = 0.125 gives S = {np.sqrt(RG_MAX):.3f},
        Y_p = {Y_kill:.4f} against 0.2449 +/- 0.0040 -- a {abs(shift_kill):.0f} sigma shift from a
        from-scratch freeze-out integration whose R_G = 1 control returns Y_p = {Yp_std:.4f} and
        whose dY_p/dS agrees with stage50's independent integration to {abs(dYp_dS/0.1753-1)*100:.0f}%.
        D/H NOT COMPUTED (no network); it can only make this worse.
    (c) WINDOW:  BBN alone allows R_G in [{bbn_lo:.3f}, {bbn_hi:.3f}], i.e. s in that range divided
        by (1 - K_B/2) -- at K_B = 0.25 that is s in [{s_bbn_lo[0.25]:.3f}, {s_bbn_hi[0.25]:.3f}].
        Intersection with no-ghost is EMPTY for all K_B <= {kb_crit:.3f}, and the intersection with
        ROUTE 1's own window (0 < s < {S_ROUTE1[0.25]:.5f} at K_B = 0.25) is EMPTY by a factor of
        {gaps[0.25]:.1f} -- robustly, since route 1's window is a subset of the no-ghost window.
    (d) THE K_B CAP CHANGES, AND NOT IN THE CORPUS'S FAVOUR IN EITHER DIRECTION: the derivation of
        K_B <= 0.25 does not survive the switch to F(Z) (the saturating factor becomes 1/s), so the
        standing cap must be restated -- and what replaces it is a FLOOR K_B > {kb_crit:.3f}, seven
        times the old ceiling and outside every published AeST fit.

    THE SINGLE DECISIVE NUMBER:  Y_p = {Y_kill:.4f} at the no-ghost ceiling, against 0.2449 +/- 0.0040
    -- and a closure-free UPPER bound Y_p <= {Yp_bound:.4f} that needs no nucleosynthesis model at all.
""")

print("=" * 100)
if FAIL:
    print(f"RESULT: {NCHK[0] - len(FAIL)}/{NCHK[0]} checks passed -- FAILURES: {FAIL}")
    sys.exit(1)
print(f"RESULT: {NCHK[0]}/{NCHK[0]} checks passed.")
sys.exit(0)
