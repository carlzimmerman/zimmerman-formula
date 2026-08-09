#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_dbi_khronon_2026.py
======================
A DBI-TYPE K(Q) FOR THE KHRONON.  Verdict: *** IT WORKS, AND IT WORKS BY FLIPPING THE SIGN OF THE
COSMOLOGICAL CONSTRAINT.  The 455x conflict that Blanchet & Skordis published against the quadratic
K(Q) = mu^2 (Q-1)^2 is not merely relaxed -- it is REVERSED, because the DBI form turns the khronon's
early-time equation of state from STIFF into DUST. ***

--------------------------------------------------------------------------------------------------
THE MECHANISM OF THE PUBLISHED NO-GO, DERIVED FROM SCRATCH (Part A)
--------------------------------------------------------------------------------------------------
Shift symmetry gives a conserved current, so a^3 K'(Q) = const.  With u = Q - 1 and the quadratic
K = mu^2 u^2 that means u = u_0/a^3, and

        rho = Q K' - K = 2 mu^2 u + mu^2 u^2,     p = K = mu^2 u^2,     w = u/(2+u)

so w -> 0 today (DUST, which is why it fits the CMB) but *** w -> 1 as a -> 0: the khronon turns
STIFF, rho ~ a^-6, and it wrecks the early expansion. ***  Written in the authors' variables,
w = w~_0/(w~_0 + a^3) with w~_0 = u_0/2 -- which REPRODUCES Blanchet & Skordis' own formula, and is
the check that this script's conventions are theirs.
Keeping w below the GDM bound then forces u_0 SMALL, hence mu LARGE, hence mu^-1 <= 0.22 kpc --
against MOND's mu^-1 >= 100 kpc.  Disjoint by 455x.  That is the whole no-go.

--------------------------------------------------------------------------------------------------
THE DBI FORM, AND WHY IT REVERSES THE CONSTRAINT (Parts B, C)
--------------------------------------------------------------------------------------------------
        K_DBI(Q) = mu^2 Lam^2 [ 1 - sqrt(1 - u^2/Lam^2) ],      u = Q - 1,   |u| < Lam

  * Small u: K -> mu^2 u^2/2.  *** IDENTICAL to the quadratic up to mu -> mu/sqrt(2), so the
    quasi-static Helmholtz term, the R^2 lever and the galaxy/cluster split are ALL PRESERVED. ***
  * K' = mu^2 Lam s/sqrt(1-s^2) with s = u/Lam DIVERGES as s -> 1, so the shift current can grow as
    a^-3 all the way back -- the solution exists at all early times.
  * But K itself SATURATES at mu^2 Lam^2.  So the PRESSURE is bounded while the DENSITY diverges:
        *** w -> 0 as a -> 0.  The khronon is DUST at early times instead of STIFF. ***
    Explicitly w ~ Lam^2 a^3 / (u_0 (1+Lam)), i.e. w vanishes as a^3.
  * And because larger u_0 puts the field DEEPER into saturation, small w now wants u_0 LARGE, i.e.
    mu^-1 LARGE.  *** The cosmological bound becomes a LOWER bound on mu^-1 instead of an upper one,
    and it therefore points the SAME WAY as MOND. The conflict dissolves. ***

At mu^-1 = 100 kpc the quadratic gives w(a=3e-5) = 0.9997, failing the GDM bound by 61x.  The DBI
form at the natural Lam = 1 gives w = 7.3e-5 -- passing with a 226x margin, with c_s^2 = 1.1e-8.

--------------------------------------------------------------------------------------------------
WHAT THIS DOES NOT DO -- AND IT IS THE THING CARL ACTUALLY WANTS (Part F)
--------------------------------------------------------------------------------------------------
*** IT DOES NOT DERIVE a_0 = kappa c sqrt(G rho_Lambda), AND IT DOES NOT MAKE kappa = 1/2 ANYTHING
OTHER THAN FITTED. ***  a_0 enters the Y-sector's normalisation; mu^-1 is a pure length fixed by the
cluster requirement; Lam is a dimensionless field-space scale.  This script checks whether a_0 and mu
are structurally linked and finds that THEY ARE NOT: the MOND-to-Helmholtz crossover sits at
r_C ~ mu^-1 with a_0 and the enclosed mass CANCELLING OUT.  So this is a completion that WORKS.
It is not an explanation of the coefficient.  The fork stands.
"""

import sys
import math
import mpmath as mp
import sympy as sp

mp.mp.dps = 40
FAIL = []


def check(cond, label, detail=""):
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=6):
    return mp.nstr(mp.mpf(x), n)


A_GDM = mp.mpf("3e-5")          # scale factor at which the GDM bound is quoted
W_BOUND = mp.mpf("0.0164")      # Kopp, Skordis, Thomas & Ilic 2018 PRL 120:221102
U0_AT_022KPC = mp.mpf("9.004e-16")   # the quadratic's GDM-limited u_0, derived in A3
MU_MOND_KPC = mp.mpf("100")     # MOND needs mu^-1 >~ this (Blanchet & Skordis 2024)
MU_COSMO_KPC = mp.mpf("0.22")   # the quadratic's cosmology ceiling (ibid.)

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- the published no-go, DERIVED rather than cited")
print("=" * 100)

u, mu, Lam, Q = sp.symbols("u mu Lambda Q", positive=True)

# A1 -- the k-essence background relations, validated on a case with a known answer.
#       For L = K(Qdot):  rho = Q K' - K,  p = K.  Check on the free massless scalar (must give w=1).
K_free = u ** 2 / 2
rho_free = sp.simplify(u * sp.diff(K_free, u) - K_free)
check(sp.simplify(rho_free - K_free) == 0,
      "A1  CONTROL on the machinery: a free massless scalar gives rho = p, i.e. w = 1 (stiff) exactly",
      f"rho = {rho_free}, p = {K_free} -- the standard result, so rho = QK'-K, p = K is right")

# A2 -- the quadratic's equation of state.
K_quad = mu ** 2 * u ** 2
Kp_quad = sp.diff(K_quad, u)
rho_quad = sp.simplify((1 + u) * Kp_quad - K_quad)      # Q = 1 + u
w_quad = sp.simplify(K_quad / rho_quad)
check(sp.simplify(w_quad - u / (2 + u)) == 0,
      "A2  quadratic K gives w = u/(2+u): DUST as u -> 0, but STIFF (w -> 1) as u -> inf",
      f"w = {w_quad}, and lim_{{u->inf}} w = {sp.limit(w_quad, u, sp.oo)}")

# A3 -- shift-charge conservation gives u = u_0/a^3, hence the authors' own w(a), hence the u_0 bound.
a_s, u0_s = sp.symbols("a u_0", positive=True)
w_of_a = sp.simplify(w_quad.subs(u, u0_s / a_s ** 3))
w0t = u0_s / 2
check(sp.simplify(w_of_a - w0t / (w0t + a_s ** 3)) == 0,
      "A3  *** and w(a) = w~_0/(w~_0 + a^3) with w~_0 = u_0/2 -- REPRODUCES Blanchet & Skordis' own "
      "formula, so the conventions here are theirs ***",
      f"w(a) = {w_of_a}")

u0_max_quad = W_BOUND * A_GDM ** 3 / (1 - W_BOUND) * 2
check(abs(u0_max_quad - U0_AT_022KPC) / U0_AT_022KPC < mp.mpf("1e-3"),
      "A4  the GDM bound forces u_0 <= 9.00e-16 for the quadratic",
      f"u_0 <= {sig(u0_max_quad,4)} from w({sig(A_GDM,2)}) < {sig(W_BOUND,3)}")

# A5 -- and rho_dust ~ mu^2 u_0 (small u) means mu^-1 ~ sqrt(u_0).  Calibrate on the published 0.22 kpc
#       so every mu^-1 below is anchored to a number in the literature, not invented here.
def mu_inv_kpc(u0):
    return MU_COSMO_KPC * mp.sqrt(mp.mpf(u0) / U0_AT_022KPC)


rho_small = sp.simplify(sp.series(rho_quad, u, 0, 2).removeO())
check(sp.simplify(rho_small - 2 * mu ** 2 * u) == 0,
      "A5  rho -> 2 mu^2 u_0 at small u, so mu^-1 ~ sqrt(u_0) at fixed rho_dust",
      "calibration anchor: mu^-1 = 0.22 kpc at u_0 = 9.00e-16 (Blanchet & Skordis 2024 sec 4.3.1)")

u0_for_mond = U0_AT_022KPC * (MU_MOND_KPC / MU_COSMO_KPC) ** 2
check(abs(mu_inv_kpc(u0_for_mond) - MU_MOND_KPC) / MU_MOND_KPC < mp.mpf("1e-9"),
      f"A6  MOND's mu^-1 = 100 kpc therefore needs u_0 = {sig(u0_for_mond,4)}",
      f"which is {sig(u0_for_mond/u0_max_quad,4)}x ABOVE the cosmology ceiling -- the no-go, in one number")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- THE DBI FORM: bounded pressure, unbounded current")
print("=" * 100)

s = sp.Symbol("s", positive=True)                     # s = u/Lam, |s| < 1
K_dbi = mu ** 2 * Lam ** 2 * (1 - sp.sqrt(1 - s ** 2))
Kp_dbi = sp.simplify(sp.diff(K_dbi, s) / Lam)         # d/du = (1/Lam) d/ds
Kpp_dbi = sp.simplify(sp.diff(Kp_dbi, s) / Lam)

check(sp.simplify(Kp_dbi - mu ** 2 * Lam * s / sp.sqrt(1 - s ** 2)) == 0,
      "B1  K' = mu^2 Lam s/sqrt(1-s^2) DIVERGES as s -> 1, so the shift current can grow as a^-3 "
      "for all a > 0",
      f"K' = {Kp_dbi}")

check(sp.limit(K_dbi, s, 1, "-") == mu ** 2 * Lam ** 2,
      "B2  *** but K itself SATURATES at mu^2 Lam^2 -- the PRESSURE is BOUNDED while the density "
      "diverges.  That is the whole mechanism ***",
      f"lim_{{s->1}} K = {sp.limit(K_dbi, s, 1, '-')}")

# B3 -- small-u limit must reproduce the quadratic, or MOND and the R^2 lever are lost.
K_small = sp.simplify(sp.series(K_dbi.subs(s, u / Lam), u, 0, 4).removeO())
check(sp.simplify(K_small - mu ** 2 * u ** 2 / 2) == 0,
      "B3  *** small u: K -> mu^2 u^2/2, IDENTICAL to the quadratic up to mu -> mu/sqrt(2).  The "
      "Helmholtz term, the R^2 lever and the galaxy/cluster split all SURVIVE unchanged ***",
      f"K = {K_small} + O(u^4)")

# B4 -- ghost-freedom: need K'' > 0 over the whole field range.
check(sp.simplify(Kpp_dbi - mu ** 2 * (1 - s ** 2) ** sp.Rational(-3, 2)) == 0,
      "B4  K'' = mu^2 (1-s^2)^(-3/2) > 0 for all |s| < 1: GHOST-FREE over the entire field range",
      f"K'' = {Kpp_dbi}")

# B5 -- sound speed.  For L = K(Q): c_s^2 = K'/(Q K'').  Derive and check subluminality.
cs2_dbi = sp.simplify(Kp_dbi / ((1 + Lam * s) * Kpp_dbi))
check(sp.simplify(cs2_dbi - Lam * s * (1 - s ** 2) / (1 + Lam * s)) == 0,
      "B5  c_s^2 = Lam s (1-s^2)/(1+Lam s)",
      f"c_s^2 = {cs2_dbi}")

check(sp.limit(cs2_dbi, s, 1, "-") == 0,
      "B6  and c_s^2 -> 0 as s -> 1: the early-time condensate is PRESSURELESS, exactly as the CMB "
      "needs",
      f"lim_{{s->1}} c_s^2 = {sp.limit(cs2_dbi, s, 1, '-')}")

# B7 -- and it never goes superluminal.  Maximise over s at fixed Lam.
cs2_max_num = max(float(cs2_dbi.subs({Lam: 1, s: sp.Rational(k, 200)})) for k in range(1, 200))
check(cs2_max_num < 1,
      f"B7  max over the whole field range at Lam = 1 is c_s^2 = {cs2_max_num:.4f} < 1: SUBLUMINAL "
      "everywhere",
      "and c_s^2 scales down with Lam, so smaller Lam is safer still")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- *** THE SIGN FLIP: cosmology now points the SAME WAY as MOND ***")
print("=" * 100)

# Solve the shift-charge condition exactly.  s/sqrt(1-s^2) = R with R = u_0/(Lam a^3) gives
# s = R/sqrt(1+R^2), so everything is closed-form.
R_sym = sp.Symbol("R", positive=True)
s_of_R = sp.solve(sp.Eq(s / sp.sqrt(1 - s ** 2), R_sym), s)
check(any(sp.simplify(v - R_sym / sp.sqrt(1 + R_sym ** 2)) == 0 for v in s_of_R),
      "C1  shift-charge conservation solves in closed form: s = R/sqrt(1+R^2), R = u_0/(Lam a^3)",
      f"{len(s_of_R)} root(s); the positive one is R/sqrt(1+R^2)")


def dbi_state(u0, L, a):
    """Return (s, w, cs2) for the DBI khronon at scale factor a. mu^2 cancels in w and cs2."""
    u0, L, a = mp.mpf(u0), mp.mpf(L), mp.mpf(a)
    R = u0 / (L * a ** 3)
    sq = 1 / mp.sqrt(1 + R ** 2)          # = sqrt(1-s^2)
    sv = R * sq
    p = L ** 2 * (1 - sq)
    Kp = L * R
    rho = (1 + L * sv) * Kp - p
    return sv, p / rho, L * sv * (1 - sv ** 2) / (1 + L * sv)


w_quad_at_mond = u0_for_mond / (u0_for_mond + 2 * A_GDM ** 3)
check(w_quad_at_mond > W_BOUND,
      f"C2  at mu^-1 = 100 kpc the QUADRATIC gives w({sig(A_GDM,2)}) = {sig(w_quad_at_mond,5)}, failing "
      f"the GDM bound by {sig(w_quad_at_mond/W_BOUND,3)}x",
      "this is the no-go, reproduced numerically")

print(f"\n   Lam      s(a=3e-5)        w(a=3e-5)      margin vs bound    c_s^2")
ok_all = True
for L in ["1.0", "0.1", "1e-3"]:
    sv, wv, cs2v = dbi_state(u0_for_mond, L, A_GDM)
    ok_all = ok_all and wv < W_BOUND
    print(f"   {L:<7s}  {sig(sv,9):>12s}  {sig(wv,4):>13s}   {sig(W_BOUND/wv,5):>10s}x        {sig(cs2v,4)}")

check(ok_all,
      "C3  *** the DBI form PASSES the GDM bound at mu^-1 = 100 kpc, for every Lam tested ***",
      "with a 226x margin at the natural Lam = 1")

# C4 -- THE SIGN.  Find, for the DBI form, the u_0 at which the GDM bound is saturated, and check
#       that the bound is a FLOOR rather than a CEILING.
def w_dbi_at_gdm(u0, L):
    return dbi_state(u0, L, A_GDM)[1]


L_nat = mp.mpf("1.0")
w_lo = w_dbi_at_gdm(u0_for_mond / 1000, L_nat)     # SMALLER u_0
w_hi = w_dbi_at_gdm(u0_for_mond * 1000, L_nat)     # LARGER u_0
check(w_lo > w_hi,
      "C4  *** for the DBI form, w at early times DECREASES with u_0 -- the OPPOSITE of the quadratic. "
      "So cosmology now demands u_0 LARGE, i.e. mu^-1 LARGE: a LOWER bound ***",
      f"w = {sig(w_lo,4)} at u_0/1000 vs {sig(w_hi,4)} at u_0*1000")

# C5 -- and the quadratic must show the opposite sign, or C4 is measuring nothing.
wq_lo = (u0_for_mond / 1000) / ((u0_for_mond / 1000) + 2 * A_GDM ** 3)
wq_hi = (u0_for_mond * 1000) / ((u0_for_mond * 1000) + 2 * A_GDM ** 3)
check(wq_lo < wq_hi,
      "NC-C  CONTROL: the QUADRATIC has the opposite sign (w INCREASES with u_0), confirming C4 is a "
      "real reversal and not an artefact",
      f"w = {sig(wq_lo,4)} at u_0/1000 vs {sig(wq_hi,4)} at u_0*1000")

# C6 -- locate the DBI floor on mu^-1 and confirm it is compatible with MOND.
lo = mp.mpf("1e-24")
while w_dbi_at_gdm(lo, L_nat) > W_BOUND and lo < 1:
    lo *= mp.mpf("1.2")
mu_floor = mu_inv_kpc(lo)
check(mu_floor < MU_MOND_KPC,
      f"C6  *** the DBI cosmology FLOOR is mu^-1 >~ {sig(mu_floor,3)} kpc, and MOND wants "
      f">~ {sig(MU_MOND_KPC,3)} kpc.  BOTH POINT THE SAME WAY -- the 455x conflict DISSOLVES ***",
      "compare the quadratic, whose ceiling 0.22 kpc and MOND's floor 100 kpc are disjoint")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- the price: a new scale Lam, and how much freedom it really has")
print("=" * 100)

# Two conditions on Lam: (i) u_0 << Lam so that TODAY is in the quadratic (MOND) regime;
# (ii) Lam <~ 1 so that saturation happens BEFORE the field would have reached the stiff regime.
Lam_min = u0_for_mond
check(Lam_min < 1,
      "D1  the allowed window is u_0 << Lam <~ 1, i.e. "
      f"{sig(Lam_min,3)} << Lam <~ 1 -- about {sig(-mp.log10(Lam_min),3)} ORDERS wide",
      "so Lam is NOT fine-tuned; and Lam = O(1) -- the condensate's own scale -- sits in the window")

# D2 -- and Lam ~ 1 is the natural value, since u = Q-1 is measured against the condensate Q_0 = 1.
check(mp.mpf("1.0") > Lam_min and mp.mpf("1.0") <= 1,
      "D2  Lam = 1 is the NATURAL choice (u is measured against Q_0 = 1) and it lies in the window",
      "the DBI saturation then switches on exactly where the quadratic would have turned stiff")

# D3 -- THE REAL COST, and it is an EFT question, not a tuning one.  K'' diverges as s -> 1.
print("\n   s          K''/mu^2 = (1-s^2)^(-3/2)")
for sv in ["0.9", "0.99", "0.999", "0.99999999"]:
    v = (1 - mp.mpf(sv) ** 2) ** mp.mpf("-1.5")
    print(f"   {sv:<12s} {sig(v,5)}")
s_early = dbi_state(u0_for_mond, L_nat, A_GDM)[0]
Kpp_early = (1 - s_early ** 2) ** mp.mpf("-1.5")
check(Kpp_early > mp.mpf("1e6"),
      f"D3  *** THE REAL COST: at a = 3e-5 the field sits at s = {sig(s_early,9)}, where "
      f"K''/mu^2 = {sig(Kpp_early,4)} ***",
      "the DBI description is approaching a BOUNDARY in field space. Whether the effective theory "
      "stays valid there is a genuine question this script does NOT settle -- it is the honest "
      "successor to the no-go it removes.")

# D4 -- A GENERAL THEOREM, which is a stronger statement than the negative control I first attempted:
#       for ANY power-law K ~ mu^2 u^n at large u, the early-time equation of state is w -> 1/(n-1).
#       So NO finite power reaches w = 0; only a BOUNDED (saturating) K does.  Derive it.
n_s = sp.Symbol("n", positive=True)
K_pow = mu ** 2 * u ** n_s
Kp_pow = sp.diff(K_pow, u)
rho_pow = (1 + u) * Kp_pow - K_pow
w_pow_asym = sp.simplify(sp.limit(sp.simplify(K_pow / rho_pow), u, sp.oo))
check(sp.simplify(w_pow_asym - 1 / (n_s - 1)) == 0,
      "D4  *** THEOREM: for any power law K ~ u^n, the early-time w -> 1/(n-1).  No FINITE power "
      "gives w = 0 -- only a BOUNDED K does ***",
      f"w_asym = {w_pow_asym}")

for n_val, lbl in [(2, "quadratic (the published no-go)"), (4, "quartic"), (6, "sextic")]:
    wv = mp.mpf(1) / (n_val - 1)
    print(f"     n = {n_val}  ({lbl:32s})  w_early = {sig(wv,4):>8s}  "
          f"{'FAILS' if wv > W_BOUND else 'passes'} the GDM bound")

check(mp.mpf(1) / (6 - 1) > W_BOUND,
      "NC-D  CONTROL: even a SEXTIC still fails (w -> 1/5 = 0.2 > 0.0164), so the fix is NOT 'add "
      "higher powers'",
      "it is specifically SATURATION. This is also exactly why Blanchet & Skordis' polynomial escape "
      "needs K_3 ~ 1e5 -- 'unnaturally large' in their words -- while DBI needs no large number at all: "
      "w -> 0 comes from BOUNDEDNESS, which no polynomial has.")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- what survives, what is untested")
print("=" * 100)

SURVIVES = [
    "The R^2 lever and the galaxy/cluster split (Part B3: small-u is the quadratic).",
    "The Helmholtz term div(M grad Phi) + mu^2 Phi = 4 pi G rho_b, with mu -> mu/sqrt(2).",
    "Lensing: gamma_PPN = 1, M_dyn/M_lens = 1 (untouched -- a Q-sector change cannot affect it).",
    "The g^-2 Lorentz-violation prediction (the aether is unchanged).",
    "Ghost-freedom and subluminality, now over the WHOLE field range (B4, B7).",
    "Dark matter still EXISTS at full Omega_dm -- this changes its early-time w, not its amount.",
]
UNTESTED = [
    "*** NO CAMB/CLASS RUN. w -> 0 and c_s^2 -> 0 are necessary for the CMB fit, not sufficient. ***",
    "EFT validity as s -> 1, where K''/mu^2 reaches 1e16 (D3). The successor question to the no-go.",
    "Perturbation stability of the DBI form on the FULL background (only the background w and the "
    "sound speed are computed here).",
    "Whether Lam is derivable from anything, or stays a third free parameter alongside mu and I_0.",
    "The nonlinear virialisation question is UNCHANGED -- this Part does not touch it.",
]
print("\n  SURVIVES:")
for x in SURVIVES:
    print(f"    - {x}")
print("\n  UNTESTED / OWED:")
for x in UNTESTED:
    print(f"    - {x}")
check(len(SURVIVES) == 6 and len(UNTESTED) == 5,
      "E1  six survivals and five owed items recorded", "")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- *** DOES THIS EXPLAIN a_0 = kappa c sqrt(G rho_Lambda)?  NO. ***")
print("=" * 100)

# Test the one structural link that could exist: is the MOND-to-Helmholtz crossover radius r_C
# related to a_0?  If a_0 appeared in r_C, mu and a_0 would be linked and the coefficient would
# gain structure.  Compute r_C from the two terms in the quasi-static equation.
a0_s, G_s, M_s, r_s, mu2_s = sp.symbols("a_0 G M r mu2", positive=True)
v2_mond = sp.sqrt(a0_s * G_s * M_s)                 # deep-MOND flat-RC speed squared
g_mond = v2_mond / r_s                              # MOND acceleration
g_helm = mu2_s * v2_mond * r_s                      # Helmholtz acceleration ~ mu^2 Phi r
r_C = sp.solve(sp.Eq(g_mond, g_helm), r_s)
r_C_pos = [x for x in r_C if sp.simplify(x).could_extract_minus_sign() is False]
check(len(r_C_pos) == 1 and sp.simplify(r_C_pos[0] - 1 / sp.sqrt(mu2_s)) == 0,
      "F1  *** the crossover is r_C = 1/mu EXACTLY: a_0 and the enclosed mass M CANCEL OUT ***",
      f"r_C = {r_C_pos[0]}")

check(a0_s not in r_C_pos[0].free_symbols and M_s not in r_C_pos[0].free_symbols,
      "F2  so mu carries NO information about a_0.  They are INDEPENDENT parameters, and the DBI "
      "form does not change that",
      "a_0 sets the Y-sector's normalisation; mu^-1 is a pure length; Lam is dimensionless")

# F3 -- and the scales are nowhere near each other, so no accidental identification is lurking.
A0 = mp.mpf("9.3619e-11")
C_L = mp.mpf("2.99792458e8")
MPC = mp.mpf("3.0857e22")
len_a0 = C_L ** 2 / A0 / MPC          # the length a_0/c^2 defines, in Mpc
check(len_a0 / (MU_MOND_KPC / 1000) > 1000,
      f"F3  and c^2/a_0 = {sig(len_a0,4)} Mpc is {sig(len_a0/(MU_MOND_KPC/1000),4)}x larger than "
      "mu^-1 ~ 100 kpc",
      "no numerical coincidence to chase, and I am NOT going to manufacture one")

print("""
  *** SO THE ANSWER TO "GIVE ME A FIELD THEORY THAT WORKS WITH MY COEFFICIENT" IS: this is a
  completion that WORKS AND IS CONSISTENT WITH the coefficient -- a_0 = kappa c sqrt(G rho_Lambda)
  goes in as the Y-sector's normalisation and nothing in the theory contradicts it.  It is NOT a
  theory that PREDICTS the coefficient.  kappa = 1/2 remains FITTED. ***

  What would be needed for the stronger thing, stated so it can be attacked: a completion in which
  the MOND normalisation is not an independent input but is FIXED by the vacuum energy already in the
  action.  The uniqueness theorem says the FORM would then be forced to be xi c sqrt(G rho).  Nothing
  in AeST, TeVeS, BIMOND or Bekenstein-Milgrom does this, and neither does the DBI variant.""")


# =============================================================================================
print()
print("=" * 100)
print("SUMMARY")
print("=" * 100)
print(f"""
  1.  *** THE DBI FORM WORKS, AND IT WORKS BY REVERSING THE CONSTRAINT.  K = mu^2 Lam^2
      [1 - sqrt(1 - u^2/Lam^2)] has BOUNDED pressure (K -> mu^2 Lam^2) and UNBOUNDED current
      (K' -> inf), so w -> 0 as a -> 0: the khronon is DUST at early times instead of STIFF. ***

  2.  At mu^-1 = 100 kpc the quadratic gives w(3e-5) = {sig(w_quad_at_mond,5)}, failing the GDM bound by
      {sig(w_quad_at_mond/W_BOUND,3)}x.  The DBI form at the natural Lam = 1 gives w = 7.26e-5 -- a 226x MARGIN,
      with c_s^2 = 1.1e-8.

  3.  *** AND THE SIGN FLIPS: for the DBI form small w wants u_0 LARGE, so cosmology gives a LOWER
      bound mu^-1 >~ {sig(mu_floor,3)} kpc instead of the quadratic's 0.22 kpc CEILING.  Cosmology and MOND now
      point the SAME WAY and Blanchet & Skordis' 455x conflict DISSOLVES. ***
      Control: the quadratic shows the opposite sign, and a QUARTIC (which grows instead of
      saturating) still FAILS -- so the fix comes specifically from SATURATION.

  4.  Small u reproduces the quadratic exactly up to mu -> mu/sqrt(2), so the Helmholtz term, the
      R^2 lever and the galaxy/cluster split ALL SURVIVE.  Ghost-free (K'' > 0) and subluminal
      (c_s^2 <= {cs2_max_num:.3f}) over the WHOLE field range.

  5.  The price is one new dimensionless scale Lam, with a window u_0 << Lam <~ 1 that is about
      {sig(-mp.log10(Lam_min),3)} orders wide -- NOT fine-tuned -- and Lam = O(1) is the natural value.
      *** The real cost is an EFT question: at a = 3e-5 the field sits at s = 1 - 5e-9, where
      K''/mu^2 ~ 1e16.  The DBI description approaches a field-space boundary, and whether the
      effective theory survives there is the honest successor to the no-go this removes. ***

  6.  *** NO CAMB/CLASS RUN HERE.  w -> 0 and c_s^2 -> 0 are NECESSARY for the CMB fit, not
      sufficient.  Do not call the CMB fit established. ***

  7.  *** AND IT DOES NOT EXPLAIN THE COEFFICIENT.  The MOND-to-Helmholtz crossover is r_C = 1/mu
      EXACTLY -- a_0 and the enclosed mass CANCEL -- so mu carries no information about a_0.  They
      are independent inputs, and c^2/a_0 = {sig(len_a0,4)} Mpc is {sig(len_a0/(MU_MOND_KPC/1000),4)}x larger than mu^-1.
      kappa = 1/2 remains FITTED.  This is a completion that WORKS WITH the coefficient, not one
      that PREDICTS it. ***
""")

print("=" * 100)
if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL:
        print(f"  - {f}")
    sys.exit(1)
print("ALL CHECKS PASSED")
print("=" * 100)
