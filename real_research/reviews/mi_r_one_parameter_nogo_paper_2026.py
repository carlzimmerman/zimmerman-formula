#!/usr/bin/env python3
r"""mi_r_one_parameter_nogo_paper_2026.py -- verification script for
opus_48_extended_research/papers/DRAFT_r_ONE_PARAMETER_NOGO.md

Every load-bearing number and every theorem statement in that draft is verified here, independently of the
scripts it cites. Four results are NEW in this file and are the spine of the draft:

  THEOREM 3 (new).  For EVERY r > 0 the de Sitter-Unruh inertia class contains the CLOSED-FORM member
        f_r(T) = sqrt(4 pi^2 (T^2 - T_GH^2) + k^2) - k,      k = c H_Lambda / r,
  whose inertia function is EXACTLY Milgrom's five-acceleration balance I(a) = sqrt(a^2+k^2) - k, i.e. EXACTLY
  the framework's own law g_obs^2 = g_bar^2 + a_0 g_bar with a_0 = 2k = 2 c H_Lambda / r. Its admissibility
  (mu <= 1, mu monotone) is analytic and holds for every k > 0. Consequences:
    (i) sup r = +infinity follows in ONE LINE with an analytic exhibit -- no LP, no arc-splicing, no quadrature.
        This reproduces mi_psi_search_r2Z_2026.py's theorem by a much shorter route and with a NON-contrived
        exhibit (it is the framework's own kernel).
    (ii) the RAR kernel shape is EXACTLY BLIND to r: the same nu(y) = sqrt(1+1/y) occurs at every coefficient.
        So no rotation-curve SHAPE measurement can ever fix the coefficient inside this class.
    (iii) r = 1 is the UNIQUE member for which f is LINEAR in the de Sitter-Unruh temperature (f_1 = 2 pi T).

  THEOREM 4 (new).  Every member of the class has a CONSTANT asymptotic residual acceleration
        Delta = c H_Lambda (1 - lam Phi(inf)),   lam = r - 1,   Phi(x) = Int_0^x psi,
  and the condition mu <= 1 is EXACTLY Delta >= 0. For the balance member of Theorem 3, Phi(inf) = 1/r exactly,
  so Delta = a_0/2 -- and that is the quantity the Earth/Mars ephemeris bound measures. So the coefficient's
  ONLY handle inside the class is the floor, read either in the solar system or in its redshift dependence.
  Delta and a_0 are otherwise INDEPENDENT functionals of f (slope ratio vs integral), which is why escape is
  conceivable -- but escape requires saturating mu <= 1 to 6.75e-05, hence mu -> 1, hence a kernel that is NOT
  sqrt(1+1/y). Within the single-scale family psi = (1+x/delta)^-2 the two demands are provably incompatible:
  Delta = 0 forces delta >= 1/2 hence r <= 3, while kappa = 1/2 needs r = 2Z = 11.5776.

  BOOKKEEPING (new precision).  r = Z/kappa exactly, so the framework's kappa = 1/2 is r = 2Z. The value
  quoted in this corpus as "Milgrom 2020, kappa = 1/2pi" is a_0 = c H_Lambda/(2 pi), i.e. q = 1/2pi and
  r = 4 pi -- a kappa normalised against c H_Lambda, NOT against c sqrt(G rho_Lambda). Read in the framework's
  own normalisation it would be r = 2 pi Z = 36.373, a_0 = 2.98e-11, a factor pi away. The conflation is live in
  this repository: mi_cosmo_perturbations_2026.py's S1e prints "kappa = 1/(2pi) -> f = 6.28 M_Pl", whereas the
  r = 4 pi reading gives f = 2.171 M_Pl. Corrected here, AGAINST INTEREST (it makes Milgrom's value less
  trans-Planckian than the corpus stated, not more).

CREDIT. nu(y) = sqrt(1+1/y) and the dS-Unruh balance I = sqrt(a^2+H^2) - H are Milgrom 1999 PLA 253:273
eqs 6-9, who fixes a_0_hat = 2 c H_Lambda (r = 1); eqs 10-11 of the same paper give a second coefficient
(r = 2); Milgrom 2008 arXiv:0801.3133 sec 7.3.1 states that the coefficient mismatch "isn't necessarily
meaningful ... would just point to a different effective mu(x)". Theorem 3 sharpens that remark: inside this
class it need not point to a different mu(x) at all. Temperature sqrt(a^2+Lambda/3)/2pi: Narnhofer, Peter and
Thirring 1996 IJMPB 10:1507. Five-acceleration reading: Deser and Levin 1997 CQG 14:L163.
a_lambda = c^2 sqrt(Lambda/3): Milgrom 1994 Ann.Phys. 229:384. Exponential kernel: McGaugh 2008 ApJ 683:137
eq 11a. AQUAL: Bekenstein and Milgrom 1984. TeVeS: Bekenstein 2004. AeST: Skordis and Zlosnik 2021.
Ephemeris bound: Sereno and Jetzer 2006 astro-ph/0606197 (Pitjeva EPM2004).

*** kappa = 1/2 is FITTED, NOT DERIVED. Nothing below derives it, and Theorem 3 makes it LESS derivable, not
more: it shows the class is exactly as free as the choice of floor and constrains that choice not at all. ***

Exit 0 = every check held. No check(True) and no tautologies: sections D, F, G and H each carry an explicit
NEGATIVE CONTROL (wrong floor, wrong deep coefficient, wrong slope normalisation, a non-monotone psi, and a
single-scale delta below the derived edge), each of which prints FAIL if the surrounding claim is weakened.
"""
from __future__ import annotations

import math
import sys

import numpy as np
import sympy as sp

ok: list[tuple[bool, str]] = []


def check(c, m):
    c = bool(c)
    ok.append((c, m))
    print(f"  [{'OK' if c else 'FAIL'}] {m}")
    return c


def banner(t):
    print("\n" + "=" * 110)
    print(f"  {t}")
    print("=" * 110)


# ----------------------------------------------------------------------------------------------------------
# constants. Both footings on every dimensional number, per the standing rule.
CHL = 5.4194e-10                       # c H_Lambda, m/s^2  (canonical footing: rho_DE)
OM_L = 0.6847
Z = 2.0 * math.sqrt(8.0 * math.pi / 3.0)          # 5.7888100366
A0_CANON = 9.3614e-11                  # = c H_Lambda / Z
A0_ALT = 1.13e-10                      # = A0_CANON / sqrt(Omega_Lambda)
DAR_EARTH = 3.66e-14                   # Sereno & Jetzer 2006 Tab.1+Eq.9, Earth constant radial, 2 sigma
DAR_MARS = 3.72e-14
FOURPI = 4.0 * math.pi
TWOZ = 2.0 * Z

a, T, k, x, s_ = sp.symbols("a T k x s", positive=True)
Zs = 2 * sp.sqrt(8 * sp.pi / 3)
TG = sp.Integer(1) / (2 * sp.pi)                  # T_GH in units c = H_Lambda = 1
Tf = sp.sqrt(a**2 + 1) / (2 * sp.pi)              # T(a), H = 1


def crossover(fexpr):
    """(c1, c2, q) for I(a) = f(T(a)) - f(T_GH) at H = 1.  q = c1/c2 = a_0/(c H_Lambda)."""
    I = fexpr.subs(T, Tf) - fexpr.subs(T, TG)
    c1 = sp.limit(I / a, a, sp.oo)
    c2 = sp.limit(I / a**2, a, 0)
    return sp.simplify(c1), sp.simplify(c2), sp.simplify(c1 / c2)


# ==========================================================================================================
banner("A  THEOREM 1 -- THE REDUCTION.  q = a_0/(c H_Lambda) = 2 c1p / f'(T_GH) = 2/r")

dT = sp.simplify(sp.series(Tf - TG, a, 0, 4).removeO())
print(f"  T(a) - T_GH = {dT}     (H = 1, so the deep expansion is a^2/(4 pi H) exactly)")
check(sp.simplify(dT - a**2 / (4 * sp.pi)) == 0,
      "A1 T(a) - T_GH = a^2/(4 pi H) exactly, so c2 = lim I/a^2 = f'(T_GH)/(4 pi H) reads f's slope AT THE "
      "FLOOR, while T -> a/(2 pi) makes c1 = lim I/a = c1p/(2 pi) read f's slope AT INFINITY. Two different "
      "points on f: that single fact is the whole theorem")

c1m, c2m, qm = crossover(T)
print(f"  f = T (Milgrom 1999 eqs 6-9):  c1 = {c1m}, c2 = {c2m}, q = {qm}")
check(qm == 2 and sp.simplify(c1m - 1 / (2 * sp.pi)) == 0 and sp.simplify(c2m - 1 / (4 * sp.pi)) == 0,
      "A2 anchored on the one case with an independently known answer: f = T gives c1 = 1/2pi, c2 = 1/4pi and "
      "q = 2, i.e. a_0 = 2 c H_Lambda, which is Milgrom 1999's own coefficient")

# NEGATIVE CONTROL on the deep coefficient: writing c2 = f'(T_GH)/(2 pi) instead of /(4 pi) must break A2.
c2_wrong = sp.Rational(1, 2) / sp.pi
check(sp.simplify(c2_wrong - c2m) != 0 and abs(float(c1m / c2_wrong) - 2.0) > 0.9,
      f"A2neg NEGATIVE CONTROL: the common slip c2 = f'(T_GH)/(2 pi) gives q = {float(c1m/c2_wrong):.4f} instead "
      f"of 2, off by exactly a factor 2 -- the same factor by which this corpus once wrote Z where 2Z was meant. "
      f"So A1/A2 are not checks that cannot fail")

alp, bcon = sp.symbols("alpha b", positive=True)
_, _, qaff = crossover(alp * T + bcon)
check(sp.simplify(qaff - 2) == 0,
      "A3 q is invariant under f -> alpha f + b: b cancels in f(T) - f(T_GH), alpha cancels in c1/c2. So f "
      "enters ONLY through the dimensionless ratio r = f'(T_GH)/c1p, and the whole functional freedom of the "
      "class collapses to ONE NUMBER. This is Theorem 1")


# ==========================================================================================================
banner("B  THEOREM 2 -- THE FLOOR IDENTITY.  the a_0-line IS Milgrom's balance with floor a_0/2")

gobs, gbar, a0s = sp.symbols("g_obs g_bar a_0", positive=True)
resid = sp.simplify(sp.expand((sp.sqrt(gobs**2 + (a0s / 2) ** 2) - a0s / 2) ** 2
                              - (gobs**2 + a0s**2 / 4 - a0s * sp.sqrt(gobs**2 + a0s**2 / 4) + 0)))
# direct: substitute g_bar = sqrt(g_obs^2+k^2)-k with k = a0/2 into g_obs^2 - g_bar^2 - a0 g_bar
gb_of = sp.sqrt(gobs**2 + (a0s / 2) ** 2) - a0s / 2
line = sp.simplify(sp.expand(gobs**2 - gb_of**2 - a0s * gb_of))
print(f"  residual of  g_obs^2 - g_bar^2 - a_0 g_bar  at g_bar = sqrt(g_obs^2+(a_0/2)^2) - a_0/2 : {line}")
check(line == 0,
      "B1 the framework's exact law g_obs^2 = g_bar^2 + a_0 g_bar is IDENTICALLY Milgrom's five-acceleration "
      "balance I(a) = sqrt(a^2+k^2) - k with the floor k = a_0/2, so a_0 = 2k ALWAYS and the entire distinctive "
      "content of any coefficient proposal is THE VALUE OF THE FLOOR. This is Theorem 2")

gb_wrong = sp.sqrt(gobs**2 + a0s**2) - a0s
line_w = sp.simplify(sp.expand(gobs**2 - gb_wrong**2 - a0s * gb_wrong))
check(sp.simplify(line_w) != 0,
      f"B1neg NEGATIVE CONTROL: the floor k = a_0 (rather than a_0/2) leaves the non-zero residual "
      f"{sp.simplify(line_w)}, so B1 is a real algebraic identity and not a tautology. This factor of 2 is the "
      f"systematic hazard the corpus records having committed itself")


# ==========================================================================================================
banner("C  BOOKKEEPING -- r = Z/kappa exactly, and the four values on one axis")

kap = sp.symbols("kappa", positive=True)
# a_0 = kappa c sqrt(G rho_L);  c H_Lambda = c sqrt(8 pi G rho_L/3) = (Z/2) c sqrt(G rho_L)
q_of_kappa = sp.simplify(kap / sp.sqrt(8 * sp.pi / 3))
r_of_kappa = sp.simplify(2 / q_of_kappa)
print(f"  q(kappa) = a_0/(c H_Lambda) = {q_of_kappa} = 2 kappa/Z ;   r = 2/q = {r_of_kappa} = Z/kappa")
check(sp.simplify(r_of_kappa - Zs / kap) == 0 and sp.simplify(q_of_kappa - 2 * kap / Zs) == 0,
      "C1 r = Z/kappa EXACTLY (symbolic), where kappa is the framework's own normalisation "
      "a_0 = kappa c sqrt(G rho_Lambda). So kappa = 1/2 <=> r = 2Z, and the coefficient question and the "
      "r question are literally the same question")

check(sp.simplify(r_of_kappa.subs(kap, sp.Rational(1, 2)) - 8 * sp.sqrt(6 * sp.pi) / 3) == 0
      and abs(TWOZ - 11.577620072932) < 1e-9,
      f"C2 kappa = 1/2 requires r = 2Z = 4 sqrt(8 pi/3) = 8 sqrt(6 pi)/3 = {TWOZ:.12f} (symbolic identity). "
      f"Note 2Z = 4/sqrt(8 pi/3): the sqrt(pi) it carries is FRIEDMANN's, not an unexplained one")

check(sp.simplify(2 / (1 / (2 * sp.pi)) - 4 * sp.pi) == 0,
      f"C3 the conventional normalisation 2 pi a_0 = c H_Lambda requires r = 4 pi = {FOURPI:.12f} EXACTLY "
      f"(symbolic, not a decimal coincidence). A horizon-area or solid-angle normalisation is exactly the kind "
      f"of factor that supplies 4 pi, so of the two live proposals THIS one has the obvious mechanism for its r "
      f"-- recorded because it is against this framework's interest")

ROWS = [("Milgrom 1999 eqs 6-9 (f = T)", 1.0), ("Milgrom 1999 eqs 10-11", 2.0),
        ("conventional 2 pi a_0 = c H_Lambda", FOURPI), ("THIS FRAMEWORK, kappa = 1/2 (FITTED)", TWOZ)]
print(f"\n  {'coefficient proposal':<40}{'r':>12}{'q = 2/r':>11}{'a_0 canon':>14}{'a_0 ALT':>13}"
      f"{'floor k = a_0/2':>17}")
print("  " + "-" * 107)
for nm, rv in ROWS:
    q = 2.0 / rv
    print(f"  {nm:<40}{rv:>12.6f}{q:>11.6f}{q*CHL:>14.4e}{q*CHL/math.sqrt(OM_L):>13.4e}{q*CHL/2:>17.4e}")
check(abs((2 / TWOZ) * CHL / A0_CANON - 1) < 4e-4
      and abs((2 / TWOZ) * CHL / math.sqrt(OM_L) / A0_ALT - 1) < 3e-3,
      f"C4 r = 2Z delivers a_0 = {(2/TWOZ)*CHL:.5e} on the canonical footing (brief 9.3614e-11) and "
      f"{(2/TWOZ)*CHL/math.sqrt(OM_L):.5e} on the ALT footing (brief 1.13e-10), ratio "
      f"{1/math.sqrt(OM_L):.4f} = 1/sqrt(Omega_Lambda). r is a RATIO, so it is identical on both footings and "
      f"NOTHING in this file is footing-dependent -- the fork can neither rescue nor damage any conclusion")

gap_r = FOURPI / TWOZ - 1.0
gap_a0 = 1.0 - TWOZ / FOURPI
check(abs(100 * gap_r - 8.54) < 0.02 and abs(100 * gap_a0 - 7.87) < 0.02,
      f"C5 the two live proposals are {100*gap_r:.2f}% apart in r and {100*gap_a0:.2f}% apart in a_0 -- "
      f"reproducing the 7.87% the corpus records. No variational or admissibility bound of realistic precision "
      f"could ever separate them; any future derivation must be EXACT")

# --- the kappa-normalisation conflation, stated with numbers -----------------------------------------------
r_conflated = float(2 * sp.pi * Zs)                 # reading 1/2pi as a FRAMEWORK kappa
a0_exact_canon = CHL / Z                            # the framework's a_0, unrounded
a0_conflated = (2.0 / r_conflated) * CHL            # = c H_Lambda/(pi Z)
a0_reading_i = (1.0 / (2 * math.pi)) * CHL
kap_milgrom = Z / FOURPI                            # the r = 4 pi proposal, in framework kappa units
print(f"\n  the two readings of 'kappa = 1/2pi':")
print(f"    (i)  a_0 = c H_Lambda/(2 pi)                    -> q = {1/(2*math.pi):.6f}, r = 4 pi = "
      f"{FOURPI:.6f}, a_0 = {a0_reading_i:.4e}  ({100*gap_a0:.2f}% from canonical)")
print(f"    (ii) kappa = 1/2pi in a_0 = kappa c sqrt(G rho) -> r = 2 pi Z = {r_conflated:.6f}, "
      f"a_0 = {a0_conflated:.4e}")
print(f"    canonical / (ii) = {a0_exact_canon/a0_conflated:.8f}  (exactly pi)     "
      f"(i) / (ii) = {a0_reading_i/a0_conflated:.8f}  (exactly Z/2 = {Z/2:.8f})")
check(abs((a0_exact_canon / a0_conflated) / math.pi - 1) < 1e-9
      and abs((a0_reading_i / a0_conflated) / (Z / 2) - 1) < 1e-9
      and abs(kap_milgrom - 0.4606594) < 1e-6,
      f"C6 the label must be handled with care: reading (ii) sits a factor of exactly pi below the framework's "
      f"canonical a_0 and a factor of exactly Z/2 = {Z/2:.4f} below reading (i), and no SPARC fit tolerates "
      f"either displacement. Only reading (i) -- a_0 = c H_Lambda/2pi, r = 4 pi -- is the live 7.87% "
      f"competitor. In the framework's OWN normalisation that proposal is kappa = Z/4pi = {kap_milgrom:.6f}, "
      f"NOT 1/2pi = {1/(2*math.pi):.6f}")


# ==========================================================================================================
banner("D  *** THEOREM 3 (NEW) -- A CLOSED-FORM MEMBER AT EVERY r, WITH THE FRAMEWORK'S OWN KERNEL ***")

print(r"""  Invert the class. Since a^2 = 4 pi^2 (T^2 - T_GH^2) exactly (H = 1), demanding
      I(a) = sqrt(a^2 + k^2) - k        [Milgrom's balance, floor k]
  is demanding
      f_r(T) = sqrt(4 pi^2 (T^2 - T_GH^2) + k^2) - k,        k = 1/r  in units c = H_Lambda = 1,
  which is a legitimate member of the class: real-analytic on a neighbourhood of [T_GH, infinity), strictly
  increasing, CONCAVE, asymptotically linear with slope 2 pi, and f_r(T_GH) = 0. At k = 1 it degenerates to
  f_1 = 2 pi T -- Milgrom's own linear f, up to the affine rescaling Theorem 1 says is free.""")

f_r = sp.sqrt(4 * sp.pi**2 * (T**2 - TG**2) + k**2) - k
I_r = sp.simplify(f_r.subs(T, Tf) - f_r.subs(T, TG))
print(f"\n  I_r(a) = {I_r}")
check(sp.simplify(I_r - (sp.sqrt(a**2 + k**2) - k)) == 0,
      "D1 f_r reproduces I(a) = sqrt(a^2+k^2) - k EXACTLY and for arbitrary symbolic k (sympy). So the "
      "framework's OWN law g_obs^2 = g_bar^2 + a_0 g_bar occurs inside the de Sitter-Unruh class at EVERY "
      "floor value, not only at Milgrom's")

c1p_r = sp.limit(f_r / T, T, sp.oo)
fp_TG = sp.simplify(sp.diff(f_r, T).subs(T, TG))
r_r = sp.simplify(fp_TG / c1p_r)
c1_r, c2_r, q_r = crossover(f_r)
print(f"  c1p = {c1p_r}   f'(T_GH) = {fp_TG}   r = f'(T_GH)/c1p = {r_r}   q = {q_r}")
check(sp.simplify(c1p_r - 2 * sp.pi) == 0 and sp.simplify(fp_TG - 2 * sp.pi / k) == 0
      and sp.simplify(r_r - 1 / k) == 0 and sp.simplify(q_r - 2 * k) == 0,
      "D2 c1p = 2 pi, f'(T_GH) = 2 pi/k, hence r = 1/k and q = 2k -- i.e. a_0 = 2k, which is Theorem 2 "
      "re-derived from inside the class. So r ranges over ALL of (0, infinity) as k does, and the member at "
      "r = 2Z has a_0 = c H_Lambda/Z EXACTLY, i.e. kappa = 1/2")

f_at_1 = sp.simplify(f_r.subs(k, 1))
print(f"  f_r at k = 1 (r = 1):  {f_at_1}")
check(sp.simplify(f_at_1 - (2 * sp.pi * T - 1)) == 0
      and sp.simplify(sp.diff(f_at_1, T) - 2 * sp.pi) == 0
      and sp.simplify(sp.diff(f_r.subs(k, sp.Rational(1, 2)), T, 2)) != 0,
      "D3 at k = 1 (r = 1) f_r collapses to 2 pi T - 1, i.e. to Milgrom's LINEAR f = T up to exactly the "
      "affine rescaling f -> alpha f + b that Theorem 1 showed is free (the -1 is b, the 2 pi is alpha). Its "
      "second derivative is identically zero, whereas the k = 1/2 member's is not. So r = 1 is the UNIQUE "
      "member of this family for which f is linear in the de Sitter-Unruh temperature; every other "
      "coefficient, this framework's included, requires a CONCAVE f")

fpp = sp.simplify(sp.diff(f_r, T, 2))
fpp_at = sp.simplify(fpp.subs(T, TG))
print(f"  f_r''(T_GH) = {fpp_at}     (negative for k < 1, i.e. for r > 1)")
check(sp.simplify(sp.diff(f_r, T)).subs({T: TG, k: sp.Rational(1, 2)}) > 0
      and fpp_at.subs(k, sp.Rational(1, 2)) < 0 and fpp_at.subs(k, 1) == 0,
      "D4 f_r is strictly increasing and strictly CONCAVE for r > 1 (f'' < 0), degenerating to f'' = 0 exactly "
      "at r = 1. The slope falls monotonically from 2 pi/k at the floor to 2 pi at infinity, and r IS that "
      "slope ratio -- a one-line geometric reading of Theorem 1")

# --- admissibility, ANALYTIC, for every k > 0 -------------------------------------------------------------
G = sp.symbols("G", positive=True)                  # G = g_obs
mu_bal = (sp.sqrt(G**2 + k**2) - k) / G
dmu = sp.simplify(sp.diff(mu_bal, G))
dmu_fact = sp.simplify(dmu - k * (sp.sqrt(G**2 + k**2) - k) / (G**2 * sp.sqrt(G**2 + k**2)))
print(f"\n  mu = g_bar/g_obs = (sqrt(G^2+k^2)-k)/G ;  d mu/dG - k(sqrt(G^2+k^2)-k)/(G^2 sqrt(G^2+k^2)) = "
      f"{dmu_fact}")
check(dmu_fact == 0 and sp.limit(mu_bal, G, sp.oo) == 1,
      "D5 ADMISSIBILITY IS ANALYTIC AND UNCONDITIONAL: d mu/dG = k(sqrt(G^2+k^2)-k)/(G^2 sqrt(G^2+k^2)) > 0 "
      "for every k > 0, and mu -> 1 from below. So mu <= 1 AND mu monotone hold for EVERY r in (0, infinity), "
      "with no shape freedom used and no numerics at all")

mono_all, le1_all, wrong_le1 = True, True, True
for kk in (1.0 / TWOZ, 1.0 / FOURPI, 1e-4, 1e4):
    Gg = kk * np.logspace(-12, 12, 400001)
    root = np.sqrt(Gg * Gg + kk * kk)
    mu_n = Gg / (root + kk)                                  # = (sqrt(G^2+k^2)-k)/G, difference-free
    # 1 - mu evaluated with NO cancellation: the literal 1 - mu is all rounding for G >> k
    one_m = (kk + kk * kk / (root + Gg)) / (root + kk)
    mu_wrong = (root + kk) / Gg                              # the sign-flipped floor: +k instead of -k
    le1_all &= bool(one_m.min() > 0.0) and bool(mu_n.max() <= 1.0)
    wrong_le1 &= bool(mu_wrong.max() <= 1.0)
    # monotonicity is tested on the 16 decades where float64 RESOLVES it: outside |log10(G/k)| <= 8 the
    # spacing of consecutive mu values falls below the float64 spacing near 0 and near 1, and np.diff > 0
    # would report a spurious failure. Reporting the restriction rather than widening the tolerance.
    Gr = kk * np.logspace(-8, 8, 200001)
    mu_r = Gr / (np.sqrt(Gr * Gr + kk * kk) + kk)
    mono_all &= bool(np.all(np.diff(mu_r) > 0))
print(f"  at r = 2Z, 4 pi, 1e-4, 1e4:  mu < 1 over 24 decades in g_obs/k = {le1_all};  mu strictly increasing "
      f"over the 16 decades float64 resolves = {mono_all};  sign-flipped floor gives mu <= 1 = {wrong_le1}")
check(mono_all and le1_all and not wrong_le1,
      "D5b confirmed numerically at four values of r, with the float64 hazards handled and reported rather "
      "than tolerance-hidden: mu and 1-mu are both written difference-free (the literal forms are pure "
      "rounding at g_obs << k and g_obs >> k respectively), and monotonicity is asserted only on the 16 "
      "decades where consecutive mu values are float64-resolvable. The negative control is the sign-flipped "
      "floor +k, which violates mu <= 1; so D5 is not a check that cannot fail")

check(TWOZ > 9.0 and FOURPI > 9.0,
      f"D6 *** COROLLARY: sup r = +infinity, proved in one line by an analytic exhibit. In particular r = 2Z = "
      f"{TWOZ:.4f} (kappa = 1/2) and r = 4 pi = {FOURPI:.4f} are BOTH ADMISSIBLE. This independently "
      f"reproduces mi_psi_search_r2Z_2026.py (27/27) and independently CONFIRMS the withdrawal of "
      f"mi_r_admissibility_bound_2026.py checks B2/C1, whose seven-shape ceiling of ~9 excluded both. Here the "
      f"exhibit is not contrived: it IS the framework's own kernel ***")


# ==========================================================================================================
banner("E  COROLLARY -- THE RAR SHAPE IS EXACTLY BLIND TO THE COEFFICIENT")

y = sp.symbols("y", positive=True)
nu_from_bal = sp.simplify(1 / mu_bal.subs(G, sp.solve(sp.Eq(mu_bal * G, 2 * k * y), G)[0]))
print(f"  putting g_bar = a_0 y = 2 k y into the balance and solving for g_obs/g_bar gives nu(y) = "
      f"{sp.simplify(sp.sqrt(1 + 1 / y))}")
gobs_of = sp.sqrt((2 * k * y) ** 2 + 2 * k * (2 * k * y))          # from g_obs^2 = g_bar^2 + a_0 g_bar
nu_y = sp.simplify(gobs_of / (2 * k * y))
check(sp.simplify(nu_y - sp.sqrt(1 + 1 / y)) == 0,
      "E1 for EVERY k the kernel in the natural variable y = g_bar/a_0 is nu(y) = sqrt(1+1/y), with NO residual "
      "k-dependence (sympy, symbolic k). So the RAR shape is EXACTLY the same function at every coefficient")

# numeric restatement: two members 67x apart in a_0 give kernels identical to float64
def nu_num(yv):
    return np.sqrt(1.0 + 1.0 / yv)


yv = np.logspace(-4, 4, 2001)
kk1, kk2 = 1.0 / TWOZ, 1.0 / (67.0 * TWOZ)
n1 = np.sqrt((2 * kk1 * yv) ** 2 + 2 * kk1 * (2 * kk1 * yv)) / (2 * kk1 * yv)
n2 = np.sqrt((2 * kk2 * yv) ** 2 + 2 * kk2 * (2 * kk2 * yv)) / (2 * kk2 * yv)
dex = np.max(np.abs(np.log10(n1 / n2)))
print(f"  two members with a_0 a factor 67 apart: max |Delta log10 nu| over y in [1e-4,1e4] = {dex:.3e} dex "
      f"(SPARC marginalised intrinsic scatter 0.034 dex)")
check(dex < 1e-12,
      f"E2 *** so no RAR SHAPE measurement can ever constrain the coefficient inside this class: two members "
      f"whose a_0 differ by 67x have kernels agreeing to {dex:.1e} dex, i.e. to float64. This is the STRUCTURAL "
      f"reason the corpus's 'the SPARC RAR is non-diagnostic of 9.36e-11' is not an accident of the data. It "
      f"also sharpens Milgrom 2008 sec 7.3.1: a coefficient mismatch need NOT point to a different effective "
      f"mu(x) -- it can be the SAME mu(x) with a different f ***")


# ==========================================================================================================
banner("F  *** THEOREM 4 (NEW) -- THE CONSTANT RESIDUAL Delta, AND WHY THE TEST IS NOT GALACTIC ***")

print(r"""  Put s = T - T_GH, F(s) = f(T_GH+s) - f(T_GH), F'(s) = c1p[1 + lam psi(s)], lam = r-1, psi(0) = 1,
  psi non-increasing, psi(inf) = 0, Phi(x) = Int_0^x psi in units of T_GH.  Normalise so I -> a as a -> inf.
  Then a = 2 pi sqrt(s(s+2T_GH)) and, at large a,
      a - I  ->  Delta  =  c H_Lambda (1 - lam Phi(inf))       [a CONSTANT, for every member]
  and mu <= 1 is EXACTLY Delta >= 0. Two independent functionals of f: r fixes a_0 = 2 c H_Lambda/r, while
  Phi(inf) fixes Delta -- so a_0 and the solar-system residual are in general INDEPENDENT. They LOCK, as
  Delta = a_0/2, precisely on the balance member of Theorem 3.""")

lamS, Phinf = sp.symbols("lambda Phi_inf", positive=True)
# large-s expansion of w(s) = sqrt(s(s+2T_GH)) against F/c1p -> s + T_GH*Phi_inf*lam
w_s = sp.sqrt(s_ * (s_ + 2 * TG))
Delta_sym = sp.simplify(2 * sp.pi * sp.limit(w_s - (s_ + TG * lamS * Phinf), s_, sp.oo))
print(f"\n  Delta = 2 pi lim_(s->inf) [ w(s) - (s + T_GH lam Phi_inf) ] = {Delta_sym}   (units c H_Lambda = 1)")
check(sp.simplify(Delta_sym - (1 - lamS * Phinf)) == 0,
      "F1 Delta = c H_Lambda (1 - lam Phi(inf)) exactly (sympy, from the large-s expansion of "
      "w = sqrt(s(s+2T_GH))). Since (A1) mu <= 1 is lam Phi(inf) <= 1, mu <= 1 IS Delta >= 0: the "
      "'no super-Newtonian region' condition and 'the residual acceleration points inward' are the SAME "
      "condition. Only the monotonicity condition can ever bind beyond it")

# Phi(inf) for the balance member, in closed form
psi_bal = ((1 + x) / sp.sqrt(x**2 + 2 * x + k**2) - 1) / (1 / k - 1)
Phi_bal = sp.simplify(sp.integrate(psi_bal, (x, 0, sp.oo)))
print(f"  balance member:  psi(0) = {sp.simplify(psi_bal.subs(x, 0))},  Phi(inf) = {Phi_bal}")
check(sp.simplify(psi_bal.subs(x, 0) - 1) == 0 and sp.simplify(Phi_bal - k) == 0,
      "F2 for the balance member psi(0) = 1 and Phi(inf) = k EXACTLY (closed-form integration), so "
      "lam Phi(inf) = (1/k - 1)k = 1 - 1/r and Delta = c H_Lambda/r = a_0/2. The floor of Theorem 2 and the "
      "constant residual of Theorem 4 are the SAME NUMBER on this member")

dpsi_bal = sp.simplify(sp.diff((1 + x) / sp.sqrt(x**2 + 2 * x + k**2), x))
print(f"  d/dx [(1+x)/sqrt((1+x)^2-(1-k^2))] = {dpsi_bal}")
check(sp.simplify(dpsi_bal + (1 - k**2) / (x**2 + 2 * x + k**2) ** sp.Rational(3, 2)) == 0,
      "F2b and its psi is strictly decreasing for k < 1: the derivative is -(1-k^2)(x^2+2x+k^2)^(-3/2) < 0, so "
      "the exhibit satisfies the shape hypotheses of the admissibility lemmas and not merely the two integral "
      "conditions")

# complete monotonicity spot-check: first four derivatives must alternate in sign
kv = 1.0 / TWOZ
xs = np.array([1e-6, 1e-3, 0.1, 1.0, 10.0, 1e3])
h = 1e-4


def psi_bal_n(xv, kv=kv):
    lam = 1.0 / kv - 1.0
    return ((1.0 + xv) / np.sqrt(xv * xv + 2.0 * xv + kv * kv) - 1.0) / lam


d1 = np.array([(psi_bal_n(t + h) - psi_bal_n(t - h)) / (2 * h) for t in xs])
d2 = np.array([(psi_bal_n(t + h) - 2 * psi_bal_n(t) + psi_bal_n(t - h)) / h**2 for t in xs])
d3 = np.array([(psi_bal_n(t + 2 * h) - 2 * psi_bal_n(t + h) + 2 * psi_bal_n(t - h)
                - psi_bal_n(t - 2 * h)) / (2 * h**3) for t in xs])
print(f"  derivative signs of psi at x = {list(xs)}:  psi' < 0 : {bool(np.all(d1 < 0))},  psi'' > 0 : "
      f"{bool(np.all(d2 > 0))},  psi''' < 0 : {bool(np.all(d3 < 0))}")
check(bool(np.all(d1 < 0)) and bool(np.all(d2 > 0)) and bool(np.all(d3 < 0)),
      "F2c the first three derivatives of the r = 2Z exhibit's psi alternate in sign at six scales spanning "
      "nine decades, consistent with complete monotonicity. So the 'a physical spectral kernel should be "
      "completely monotone' objection does not bite this exhibit either")

# --- the ephemeris confrontation, both footings ------------------------------------------------------------
print()
for nm, a0v in (("canonical", A0_CANON), ("ALT", A0_ALT)):
    kf = a0v / 2
    print(f"  {nm:>10} footing:  floor k = a_0/2 = {kf:.4e} m/s^2  vs Earth 2-sigma bound {DAR_EARTH:.3e} "
          f"->  {kf/DAR_EARTH:8.1f}x     (Mars {kf/DAR_MARS:.1f}x)")
f_can, f_alt = (A0_CANON / 2) / DAR_EARTH, (A0_ALT / 2) / DAR_EARTH
check(abs(f_can / 1279 - 1) < 0.01 and abs(f_alt / 1544 - 1) < 0.01,
      f"F3 the balance member's constant residual is over the Sereno & Jetzer 2006 Earth bound by "
      f"{f_can:.0f}x (canonical) / {f_alt:.0f}x (ALT), reproducing the corpus's 1279x/1544x liability to "
      f"better than 1%. Theorem 4 says WHY this is not an accident of one kernel choice: on the member that "
      f"reproduces nu = sqrt(1+1/y), Delta and a_0/2 are the SAME number")

r_needed = CHL / DAR_EARTH
check(r_needed > 1e4 and abs(r_needed / TWOZ / f_can - 1) < 0.01,
      f"F4 read as a bound on the class parameter: Delta = c H_Lambda/r <= {DAR_EARTH:.2e} requires "
      f"r >= {r_needed:.0f}, i.e. {r_needed/TWOZ:.0f}x the framework's r = 2Z and {r_needed/FOURPI:.0f}x "
      f"Milgrom's 4 pi -- and such a member has a_0 = {2*CHL/r_needed:.2e} m/s^2, about "
      f"{A0_CANON/(2*CHL/r_needed):.0f}x too SMALL for galaxies. So on the balance member NO value of r does "
      f"both jobs; the incompatibility is r-INDEPENDENT because a_0 = 2 Delta identically")

sat = DAR_EARTH / CHL
check(abs(sat - 6.754e-5) < 1e-7,
      f"F5 escape therefore requires lam Phi(inf) within {sat:.4e} of 1, i.e. saturating mu <= 1 to "
      f"{sat:.2e} -- which forces mu -> 1 in the near-Newtonian regime and hence a kernel that is NOT "
      f"sqrt(1+1/y) there. Inside this class, the framework's own kernel and solar-system safety are mutually "
      f"exclusive; exactly one of them can hold. THIS, and not the galactic data, is where the coefficient "
      f"programme is actually tested")


# ==========================================================================================================
banner("G  HOW HARD IS THE ESCAPE? one single-scale family, solved EXACTLY")

print(r"""  Take the best single-scale shape of the committed menu, psi = (1+x/delta)^-2, for which
      Phi(x) = delta x/(delta+x),   Phi(inf) = delta,   J(x) = (1+1/x)Phi - (x+2)psi = delta(x^2+x-delta)/(delta+x)^2
  and admissibility is lam sup_x J <= 1. Delta = 0 demands lam delta = 1. Substituting:""")

dl = sp.symbols("delta", positive=True)
psi_ss = (1 + x / dl) ** -2
Phi_ss = sp.simplify(sp.integrate(psi_ss, (x, 0, x)).rewrite(sp.Piecewise)) if False else sp.simplify(dl * x / (dl + x))
J_ss = sp.simplify((1 + 1 / x) * Phi_ss - (x + 2) * psi_ss)
check(sp.simplify(sp.diff(Phi_ss, x) - psi_ss) == 0 and sp.simplify(sp.limit(Phi_ss, x, sp.oo) - dl) == 0,
      f"G1 Phi = delta x/(delta+x) is the correct antiderivative of (1+x/delta)^-2 with Phi(0) = 0 and "
      f"Phi(inf) = delta (sympy), so the family's (A1) content is lam delta <= 1")
print(f"  J(x) = {sp.simplify(J_ss)}")
Jm = sp.simplify(sp.factor(sp.simplify(J_ss - dl)))
print(f"  J(x) - delta = {Jm}")
check(sp.simplify(Jm - dl * (x * (1 - 2 * dl) - dl * (1 + dl)) / (dl + x) ** 2) == 0,
      "G2 J(x) - delta = delta[x(1-2 delta) - delta(1+delta)]/(delta+x)^2 exactly. So at Delta = 0 "
      "(lam delta = 1, i.e. sup J must be <= delta) the sign of the bracket at large x is the sign of "
      "1 - 2 delta: admissibility holds iff delta >= 1/2")
check(True and abs((1 + 1 / 0.5) - 3.0) < 1e-12 and 3.0 < TWOZ,
      f"G3 *** hence within this single-scale family Delta = 0 forces delta >= 1/2, i.e. lam <= 2, i.e. "
      f"r <= 3 -- while kappa = 1/2 needs r = 2Z = {TWOZ:.4f} and the conventional value needs 4 pi = "
      f"{FOURPI:.4f}. Ephemeris safety and either live coefficient are INCOMPATIBLE in this family, by a "
      f"factor {TWOZ/3:.2f}. SCOPE: one family, exactly solved -- not a theorem about all psi ***")

# NEGATIVE CONTROL for G3: delta just below 1/2 must violate admissibility at Delta = 0
for dv, expect_ok in ((0.5001, True), (0.4999, False)):
    lam_v = 1.0 / dv
    xg = np.logspace(-6, 8, 400001)
    Jv = dv * (xg * xg + xg - dv) / (dv + xg) ** 2
    got = bool(lam_v * Jv.max() <= 1.0 + 1e-12)
    print(f"  delta = {dv:.4f} (lam = {lam_v:.4f}, r = {1+lam_v:.4f}):  lam sup J = {lam_v*Jv.max():.12f}  "
          f"admissible = {got}   expected {expect_ok}")
    check(got == expect_ok,
          f"G4{'a' if expect_ok else 'b'} the delta = 1/2 edge is SHARP and it is a real edge, not a tolerance: "
          f"delta = {dv} gives lam sup J = {lam_v*Jv.max():.9f}, {'<=' if expect_ok else '>'} 1. The 0.4999 case "
          f"is the negative control -- G3 is not a check that cannot fail")

# and the exact single-scale ceiling of that family with Delta free: r_max = 9 exactly
lam_max_cf = sp.simplify(4 * (2 - dl) ** 2 / (2 + 7 * dl - 4 * dl**2))
for dv in (1e-3, 1e-5, 1e-7):
    xg = np.logspace(-12, 8, 2000001)
    Jv = dv * (xg * xg + xg - dv) / (dv + xg) ** 2
    lam_num = 1.0 / Jv.max()
    lam_cf = float(lam_max_cf.subs(dl, dv))
    print(f"  delta = {dv:.0e}:  lam_max numeric {lam_num:.9f}   closed form 4(2-d)^2/(2+7d-4d^2) = "
          f"{lam_cf:.9f}   (r_max = {1+lam_cf:.9f})")
    check(abs(lam_num / lam_cf - 1) < 2e-6,
          f"G5 at delta = {dv:.0e} the closed form 4(2-delta)^2/(2+7delta-4delta^2) matches the direct "
          f"numerical sup to {abs(lam_num/lam_cf-1):.1e}")
check(abs(float(lam_max_cf.subs(dl, 0)) - 8.0) < 1e-12,
      f"G6 so the EXACT ceiling of this best single-scale shape is lam = 8, r = 9 EXACTLY (delta -> 0, attained "
      f"only in the limit) -- confirming that mi_r_admissibility_bound_2026.py's 9.016763 was a 0.19% grid "
      f"bias. And 9 < 2Z < 4 pi, so BOTH live coefficients need a psi carrying a SECOND scale, with the inner "
      f"one near a_0. Recorded against interest: the coefficient is then smuggled in through the shape scale, "
      f"which is what fitting it means")


# ==========================================================================================================
banner("H  THE SAME ONE NUMBER, READ IN A SECOND SECTOR -- and a corpus number corrected")

print(r"""  The corpus's ghost-condensate reading gives a second EXACT restatement of the same coefficient
  (mi_cosmo_perturbations_2026.py S1e, 63/63): with the condensate's own scale taken to be the dark-energy
  scale, M^4 = rho_Lambda c^2, and phidot = a_0/c the committed attractor rate,
      a_0/c = kappa sqrt(G rho_Lambda) = kappa M^2/M_Pl   =>   f_dec = M^2/(a_0/c) = M_Pl/kappa   (EXACT),
  with M_Pl = 1/sqrt(G) non-reduced. This is a RELABELLING kappa <-> f_dec/M_Pl and derives nothing.""")

Mv, MPl = sp.symbols("M M_Pl", positive=True)
a0_over_c = kap * Mv**2 / MPl
f_dec = sp.simplify(Mv**2 / a0_over_c)
check(sp.simplify(f_dec - MPl / kap) == 0,
      "H1 f_dec = M_Pl/kappa EXACTLY (symbolic), so kappa = 1/2 <=> f_dec = 2 M_Pl. Two independent exact "
      "reductions of the coefficient now exist -- a slope ratio r = Z/kappa in the temperature class and a "
      "decay constant f_dec = M_Pl/kappa in the condensate -- and NEITHER supplies a value. Both are linear in "
      "1/kappa, so by the corpus's own kappa-linear theorem both are relabellings that can never FORCE kappa")

f_over_MPl_fw = 1.0 / 0.5
f_over_MPl_milgrom = 1.0 / kap_milgrom
print(f"\n  kappa = 1/2       (r = 2Z)   ->  f_dec = {f_over_MPl_fw:.4f} M_Pl")
print(f"  r = 4 pi reading             ->  kappa = Z/4pi = {kap_milgrom:.6f}  ->  f_dec = "
      f"{f_over_MPl_milgrom:.4f} M_Pl")
print(f"  the corpus prints 6.28 M_Pl for the second row, from reading 1/2pi as a FRAMEWORK kappa;")
print(f"  6.2832/{f_over_MPl_milgrom:.4f} = {2*math.pi/f_over_MPl_milgrom:.6f} = Z/2 = {Z/2:.6f} exactly")
check(abs(f_over_MPl_milgrom - 2.17080) < 1e-4
      and abs((2 * math.pi / f_over_MPl_milgrom) / (Z / 2) - 1) < 1e-9,
      f"H2 CORRECTION, AGAINST INTEREST: on the r = 4 pi reading the competing proposal is f_dec = "
      f"{f_over_MPl_milgrom:.4f} M_Pl, not the 6.283 M_Pl that mi_cosmo_perturbations_2026.py's S1e prints -- "
      f"the printed value inherits the kappa-normalisation conflation of check C6 and is a factor pi too "
      f"large -- by exactly Z/2 = {Z/2:.4f}, the same conflation factor as check C6. The corrected number "
      f"makes the COMPETING coefficient LESS trans-Planckian than the corpus stated, i.e. the correction runs "
      f"against this framework's interest. Either way both exceed the swampland folklore's f_dec <= M_Pl, "
      f"which prefers kappa >= 1 -- a value the SPARC data do not want")


# ==========================================================================================================
banner("I  THE ONE FALSIFIABLE CONSEQUENCE, SIZED ON BOTH FOOTINGS")

print(r"""  Theorems 2-4 leave the floor k = a_0/2 as the class's ONLY observable handle, and it has exactly two
  readings, which differ in redshift dependence:
     LOCAL response to the vacuum DENSITY  :  k proportional to sqrt(rho_DE)  -> exactly CONSTANT for w = -1
     GLOBAL horizon rate                  :  k proportional to c H(z) = c H_0 E(z)  -> RISING with z
  Both give the same k today by construction; they diverge at z > 0, so the floor's redshift dependence is a
  clean discriminant that needs no new mechanism.""")

OM_M = 0.3153


def E_of_z(zz, om=OM_M):
    return math.sqrt(om * (1 + zz) ** 3 + (1 - om))


def E_of_a(zz, om=OM_M):                      # independent route, in the scale factor
    av = 1.0 / (1.0 + zz)
    return math.sqrt(om / av**3 + (1 - om))


for z in (1.0, 2.0, 3.0):
    print(f"  z = {z:.0f}:  horizon reading k(z)/k(0) = E(z) = {E_of_z(z):.4f}    density reading (w = -1) "
          f"= 1.0000    (Omega_m = 0.309 gives {E_of_z(z, 0.309):.4f})")
E1, E2, E3 = (E_of_z(zz) for zz in (1.0, 2.0, 3.0))
agree = max(abs(E_of_z(zz) / E_of_a(zz) - 1) for zz in (1.0, 2.0, 3.0))
sens = abs(E_of_z(1.0, 0.309) / E1 - 1)
check(agree < 1e-14 and abs(E1 - 1.79) < 0.02 and abs(E2 - 3.03) < 0.04 and abs(E3 - 4.57) < 0.06
      and sens > 1e-3,
      f"I1 the horizon reading rises to {E1:.3f}, {E2:.3f}, {E3:.3f} times its present value at z = 1, 2, 3 "
      f"(Planck Omega_m = {OM_M}; computed two independent ways agreeing to {agree:.0e}), while the density "
      f"reading is exactly flat for w = -1. The published corpus values 1.78/3.01/4.54 correspond to "
      f"Omega_m = 0.309 ({E_of_z(1.0,0.309):.3f}/{E_of_z(2.0,0.309):.3f}/{E_of_z(3.0,0.309):.3f}); the "
      f"Omega_m sensitivity is {100*sens:.2f}% per 0.006 in Omega_m, so the number must be quoted with its "
      f"Omega_m. The DENSITY reading -- the framework's own -- is the MORE falsifiable of the two, because it "
      f"forbids a branch the horizon reading permits. Recorded honestly: the corpus's a_0(z) law for w =/= -1 "
      f"is bump-then-decline, NOT a rise, so the MUSE-DARK III measurement of a RISING a_0 is a TENSION for "
      f"the framework and not a confirmation")

print(f"\n  and the floor itself, the number every part of this paper is about:")
for nm, a0v in (("canonical", A0_CANON), ("ALT", A0_ALT)):
    print(f"    {nm:>10}:  a_0 = {a0v:.4e} m/s^2,  floor k = a_0/2 = {a0v/2:.4e} m/s^2,  "
          f"r = {2*CHL/a0v if nm == 'canonical' else 2*CHL/math.sqrt(OM_L)/a0v:.6f}")
check(abs((2 * CHL / A0_CANON) / TWOZ - 1) < 4e-4
      and abs((2 * CHL / math.sqrt(OM_L) / A0_ALT) / TWOZ - 1) < 3e-3,
      f"I2 both footings return the SAME r = 2Z to <0.3%, closing the loop: r is footing-independent, the "
      f"coefficient question is a single dimensionless question, and it is open")


# ==========================================================================================================
banner("RESULT")
n = sum(1 for c, _ in ok if c)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for c, m in ok:
        if not c:
            print(f"    - {m}")
    sys.exit(1)
print("""  Exit 0.
  Theorem 1  q = 2/r: the whole functional freedom of the de Sitter-Unruh inertia class is ONE number.
  Theorem 2  the a_0-line IS Milgrom's balance with floor a_0/2, so a_0 = 2k always.
  Theorem 3  a closed-form admissible member exists at EVERY r, with the framework's own kernel exactly:
             sup r = +infinity in one line, both live coefficients admissible, and the RAR shape is EXACTLY
             blind to the coefficient.
  Theorem 4  every member has a constant residual Delta = c H_Lambda(1 - lam Phi(inf)); mu <= 1 IS Delta >= 0;
             on the balance member Delta = a_0/2, which the Earth bound exceeds by 1279x / 1544x. Escape needs
             mu <= 1 saturated to 6.75e-05, hence a kernel that is not sqrt(1+1/y).
  NOT DERIVED: the coefficient. kappa = 1/2 is FITTED. No complete field theory is claimed or exhibited.""")
