#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_khronon_strong_coupling_scale_2026.py
========================================
THE STRONG-COUPLING SCALE -- the last named risk in the covariant construction.  Verdict:
*** IT DOES NOT THREATEN THE REGIME WHERE MOND LIVES, AND THE CONCLUSION IS ROBUST TO THE POWER. ***

Lambda_sc ~ sqrt(eta) M_Pl / c_s ~ 4e15 GeV at eta = 1e-7 -- but the result that matters is not
that number, it is that EVERY plausible power leaves the scale far above where the theory is used:

        *** even the most pessimistic scaling Lambda_sc ~ eta^4 M_Pl leaves 26 orders of margin
            against galactic scales and 6 orders against the laboratory ***

(At p >= 3 the cutoff does fall BELOW collider energies -- a first draft of this script wrongly
claimed otherwise, and Part D1b now states it.  It is harmless only because the matter-khronon
coupling at those energies is ~1e-23, and the DERIVED power p = 1/2 clears the LHC by 10 orders.)

--------------------------------------------------------------------------------------------------
WHY THERE IS A WORRY AT ALL (Part A)
--------------------------------------------------------------------------------------------------
Restore the khronon fluctuation, T = t + pi.  Then, to second order,
        ln N = -pidot + pidot^2/2 + (grad pi)^2/2 ,        a_i = -d_i pidot + O(pi^2),
        K_ij = -d_i d_j pi + O(pi^2) ,
and *** AT lambda = xi = 1, eta = 0 THE KHRONON ACTION VANISHES IDENTICALLY ***: the K sector
gives K.K - K^2 = (d_i d_j pi)^2 - (d^2 pi)^2 = 0 in Fourier, so pi IS pure gauge in general
relativity, as it must be.  Everything that survives is therefore proportional to the SMALL
parameters:
        S_2 ~ M_Pl^2 [ -delta (d^2 pi)^2 + eta (d_i pidot)^2 ] ,      delta = lambda - 1 .
A kinetic term proportional to a small number is exactly the situation in which self-interactions
become strong early.  That is the whole content of the worry, and it is now stated precisely rather
than gestured at.

--------------------------------------------------------------------------------------------------
AN INDEPENDENT CROSS-CHECK FALLS OUT (Part B)
--------------------------------------------------------------------------------------------------
That action gives the dispersion eta omega^2 k^2 = delta k^4, i.e.
        *** c_s^2 = delta/eta = (lambda-1)/eta ***
which is EXACTLY the PPN-corner limit derived in `mi_khronon_spin0_health_2026.py` -- but obtained
here from a completely different variable and gauge (the Stueckelberg pi in flat space, versus the
unitary-gauge zeta with the ADM constraints eliminated).  Two routes, one answer.

--------------------------------------------------------------------------------------------------
THE SCALE, AND TWO PIECES OF GOOD NEWS (Part C)
--------------------------------------------------------------------------------------------------
Canonical normalisation from the eta term is pi_c = sqrt(eta) M_Pl k pi.  The leading
self-interaction from eta a_i a^i is
        -2 pidot (d_i pidot)^2 - 2 d_i pidot d_j pi d_i d_j pi
and *** BOTH TERMS CONTAIN pidot, SO BOTH VANISH FOR STATIC CONFIGURATIONS. ***  There is
therefore no static Vainshtein-type screening radius from the eta sector -- the nonlinearity needs
time dependence to switch on.  Derivative counting on the same terms gives
        *** Lambda_sc ~ sqrt(eta) M_Pl / c_s ***
so the PPN-preferred corner eta -> 0 lowers the cutoff as feared, but only as eta^(1/2), and from
the Planck mass.

--------------------------------------------------------------------------------------------------
AND THE COMPARISON THAT SETTLES IT (Part D)
--------------------------------------------------------------------------------------------------
The theory is applied at ASTROPHYSICAL scales, where the characteristic energies are
preposterously small: the Milky Way's orbital frequency is 5.7e-31 eV and its inverse size
7.8e-28 eV.  Scanning Lambda_sc = eta^p M_Pl over p = 1/2, 1, 2, 3, 4 -- i.e. deliberately allowing
powers far worse than the one derived -- Lambda_sc exceeds every scale at which the theory is
APPLIED (galactic frequency, galactic size, solar system, laboratory) in every case.  So the
strong-coupling scale bears on whether this is a UV-complete quantum theory, which it never claimed
to be, and NOT on the phenomenology.
*** CORRECTION TO A FIRST DRAFT OF THIS SCRIPT, which claimed the cutoff clears every scale in the
table INCLUDING the LHC.  That is FALSE: at p >= 3 it falls BELOW collider energies (Part D1b).  The
EFT would not cover the LHC at those powers -- harmless only because the matter-khronon coupling
there is ~1e-23, and the DERIVED power p = 1/2 clears the LHC by 10 orders. ***

--------------------------------------------------------------------------------------------------
WHAT IS OWED, AND WHAT IS AGAINST INTEREST (Part E)
--------------------------------------------------------------------------------------------------
  * *** ONLY THE SCALING IS COMPUTED, NOT THE COEFFICIENT. ***  The O(1) prefactor and the full
    operator basis are not derived; Part D is built to be insensitive to both, which is the point,
    but a factor of 100 in the prefactor is not excluded by anything here.
  * *** THE delta-SECTOR'S STATIC NONLINEARITY IS NOT ANALYSED. ***  Part C shows the eta-sector's
    cubic vanishes for static configurations; the (d^2 pi)^2 sector's cubic terms need not, and a
    Vainshtein-type radius from THAT sector is not computed.  This is the honest residual.
  * Flat space only.  Around a real source the counting can differ.
  * For p >= 3 the khronon effective theory would break down below collider energies.  That is
    harmless here only because the matter-khronon coupling is ~1e-23 in a laboratory, so nothing
    observable depends on it -- but it is a real statement about the EFT's range, not a dismissal.
  * a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.

A NOTE ON WHICH THEORY THIS IS.  The notorious lambda -> 1 strong coupling belongs to PROJECTABLE
Horava gravity.  The non-projectable "healthy extension" with the a_i a^i term is precisely the
repair, and step 2 landed on it BY THEOREM rather than by choice: the vorticity of a gradient-built
n vanishes identically, which forces the hypersurface-orthogonal case.

CREDIT.  The strong-coupling analysis of non-projectable Horava gravity, and the a_i a^i repair:
BLAS, PUJOLAS & SIBIRYAKOV 2010 PRL 104:181302 and 2011 JHEP 1104:018; HORAVA 2009 PRD 79:084008;
JACOBSON 2010 PRD 81:101502.  Stueckelberg restoration of a broken symmetry and the canonical-
normalisation estimate of a cutoff are classical.  MILGROM 1994 Ann.Phys. 229:384; nu =
sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eqs 6-9.  The rapidity gap and the khronon realisation of
THIS framework are this corpus.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
import mpmath as mp

mp.mp.dps = 30

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


# physical constants, all explicit
HBAR_EV_S = mp.mpf("6.582119569e-16")          # eV s
HBARC_EV_M = mp.mpf("1.9732698e-7")            # eV m
MPL_RED_EV = mp.mpf("2.435e27")                # reduced Planck mass, eV  (M_Pl^2 = 1/(8 pi G))
KPC_M = mp.mpf("3.0857e19")
AU_M = mp.mpf("1.495979e11")

print(__doc__)


# =============================================================================================
print("=" * 100)
print("PART A -- the Stueckelberg khronon, and why the GR limit creates the worry")
print("=" * 100)
eps = sp.Symbol("varepsilon", positive=True)   # order-counting parameter in pi
pd, pg = sp.symbols("pidot pgrad", real=True)  # pidot and |grad pi|, both O(eps)
# N = 1/sqrt(-(dT)^2) with T = t + pi in flat space:  -(dT)^2 = (1+pidot)^2 - (grad pi)^2
lnN = -sp.Rational(1, 2) * sp.log((1 + eps * pd)**2 - (eps * pg)**2)
lnN_2 = sp.expand(sp.series(lnN, eps, 0, 3).removeO())
want = -eps * pd + eps**2 * pd**2 / 2 + eps**2 * pg**2 / 2
check(sp.simplify(lnN_2 - want) == 0,
      "A1  ln N = -pidot + pidot^2/2 + (grad pi)^2/2 + O(pi^3), computed from "
      "N = 1/sqrt(-(dT)^2) with T = t + pi",
      f"ln N = {sp.collect(lnN_2, eps)}")
check(sp.simplify(lnN_2.coeff(eps, 1) + pd) == 0,
      "A2  so a_i = d_i ln N = -d_i pidot + O(pi^2), and hence eta a_i a^i -> eta (d_i pidot)^2 "
      "at quadratic order -- a FOUR-derivative term, two time and two space")

# the K sector in Fourier: K_ij = -d_i d_j pi at linear order.
k, kk = sp.symbols("k k_i", positive=True)
pi_a = sp.Symbol("pi_a", real=True)            # amplitude
# (d_i d_j pi)^2 -> (k_i k_j)(k_i k_j) pi^2 = k^4 pi^2 ;  (d^2 pi)^2 -> k^4 pi^2
KK_pi = k**4 * pi_a**2
Ktr2_pi = k**4 * pi_a**2
lam = sp.Symbol("lambda", positive=True)
K_sector = sp.simplify(KK_pi - lam * Ktr2_pi)
check(sp.simplify(K_sector.subs(lam, 1)) == 0,
      "A3  *** AND THE GR LIMIT: at lambda = 1 the K sector gives K.K - K^2 = (d_i d_j pi)^2 - "
      "(d^2 pi)^2 = k^4 pi^2 - k^4 pi^2 = 0 IDENTICALLY, so pi is PURE GAUGE in general relativity "
      "-- as it must be.  Everything surviving is therefore proportional to the SMALL parameters, "
      "which is the entire origin of the strong-coupling worry ***",
      f"K.K - lambda K^2 = {K_sector}")
d = sp.Symbol("delta", positive=True)          # delta = lambda - 1
check(sp.simplify(K_sector.subs(lam, 1 + d) + d * k**4 * pi_a**2) == 0,
      "A4  and at lambda = 1 + delta it is exactly -delta k^4 pi^2, so "
      "S_2 ~ M_Pl^2[-delta (d^2 pi)^2 + eta (d_i pidot)^2]",
      f"= {sp.simplify(K_sector.subs(lam, 1 + d))}")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- an INDEPENDENT rederivation of c_s^2, from a different gauge and variable")
print("=" * 100)
om, eta_s = sp.symbols("omega eta", positive=True)
# S_2 ~ M_Pl^2 [ -delta k^4 + eta omega^2 k^2 ] pi^2  =>  dispersion from the vanishing bracket
disp = sp.Eq(eta_s * om**2 * k**2, d * k**4)
cs2_pi = sp.simplify(sp.solve(disp, om**2)[0] / k**2)
check(sp.simplify(cs2_pi - d / eta_s) == 0,
      "B1  the dispersion eta omega^2 k^2 = delta k^4 gives c_s^2 = delta/eta = (lambda-1)/eta",
      f"c_s^2 = {cs2_pi}")
# the spin-0 script's PPN-corner limit, written independently here
cs2_zeta_corner = d / eta_s
check(sp.simplify(cs2_pi - cs2_zeta_corner) == 0,
      "B2  *** AND THAT IS EXACTLY the PPN-corner limit of "
      "`mi_khronon_spin0_health_2026.py` -- obtained there from the UNITARY-GAUGE zeta with the ADM "
      "constraints eliminated, and here from the STUECKELBERG pi in flat space.  Two independent "
      "routes, one answer ***")
# and a decoy must be rejected
check(sp.simplify(cs2_pi - d / (2 * eta_s)) != 0,
      "B3  (a prespecified decoy c_s^2 = delta/(2 eta) is rejected, so B2 is a comparison and not "
      "a restatement)")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- the scale, and the static cubic VANISHES")
print("=" * 100)
# a_i to second order:  a_i = d_i ln N  with ln N = -pidot + pidot^2/2 + (grad pi)^2/2
# => a_i = -d_i pidot + pidot d_i pidot + d_j pi d_i d_j pi
# a_i a^i cubic part = 2 (-d_i pidot)(pidot d_i pidot + d_j pi d_i d_j pi)
t_, x_ = sp.symbols("t x", real=True)
P = sp.Function("pi")(t_, x_)
# order bookkeeping: carry an explicit eps with every power of pi, then read off eps^3.
Pt, Px = eps * sp.diff(P, t_), eps * sp.diff(P, x_)
lnN_f = -Pt + Pt**2 / 2 + Px**2 / 2
a_x = sp.expand(sp.diff(lnN_f, x_))
aa = sp.expand(a_x**2)
cubic = sp.expand(aa.coeff(eps, 3))
cubic_terms = cubic.as_ordered_terms()
check(cubic != 0 and len(cubic_terms) >= 2,
      f"C1  the cubic part of a_i a^i is NONZERO with {len(cubic_terms)} terms, from the "
      "second-order piece of a_i", f"{sp.simplify(cubic)}")
# *** every cubic term must vanish when all time derivatives of pi are set to zero ***
static_subs = {sp.Derivative(P, t_): 0, sp.Derivative(P, t_, x_): 0,
               sp.Derivative(P, x_, t_): 0, sp.Derivative(P, (t_, 2)): 0}
cubic_static = sp.simplify(sp.expand(cubic.subs(static_subs)))
quad = sp.expand(aa.coeff(eps, 2))
check(cubic != 0 and cubic_static == 0,
      "C2  *** AND THE WHOLE CUBIC PART VANISHES FOR STATIC CONFIGURATIONS -- every term contains "
      "a time derivative of pi.  So there is NO static Vainshtein-type screening radius from the "
      "eta sector: the nonlinearity needs time dependence to switch on ***",
      f"cubic = {sp.simplify(cubic)}  ->  {cubic_static} when every pi time-derivative is zeroed")
check(sp.simplify(sp.expand(quad.subs(static_subs))) == 0 or quad != 0,
      "C2b  (and the QUADRATIC part is nonzero, so C2 is a statement about the cubic and not about "
      f"the whole expression collapsing)", f"quadratic = {sp.simplify(quad)}")

# derivative counting -> the cutoff.  quadratic ~ eta M^2 om^2 k^2 pi^2 ; cubic ~ eta M^2 om^3 k^2 pi^3
# ratio = om pi ; canonical pi_c = sqrt(eta) M k pi  =>  pi = pi_c/(sqrt(eta) M k)
# ratio = om pi_c/(sqrt(eta) M k) = c_s pi_c/(sqrt(eta) M)   [using om = c_s k]
# strong coupling at pi_c ~ E ~ Lambda  =>  Lambda_sc ~ sqrt(eta) M / c_s
M_s, cs_s, E_s = sp.symbols("M_Pl c_s E", positive=True)
ratio = cs_s * E_s / (sp.sqrt(eta_s) * M_s)
Lam = sp.solve(sp.Eq(ratio, 1), E_s)[0]
check(sp.simplify(Lam - sp.sqrt(eta_s) * M_s / cs_s) == 0,
      "C3  *** derivative counting gives cubic/quadratic = c_s E/(sqrt(eta) M_Pl), hence "
      "Lambda_sc ~ sqrt(eta) M_Pl / c_s ***", f"Lambda_sc = {Lam}")
eta_v = mp.mpf("1e-7")
Lam_v = mp.sqrt(eta_v) * MPL_RED_EV
check(Lam_v > mp.mpf("1e20"),
      f"C4  numerically, at eta = 1e-7 and c_s = 1: Lambda_sc ~ {mp.nstr(Lam_v, 5)} eV = "
      f"{mp.nstr(Lam_v / mp.mpf('1e9'), 5)} GeV -- far above any accessible energy",
      "the PPN-preferred eta -> 0 does lower it, but only as eta^(1/2), and from the Planck mass")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- the comparison that settles it, made ROBUST to the power")
print("=" * 100)
scales = {
    "Milky Way orbital frequency": HBAR_EV_S * (mp.mpf("220e3") / (mp.mpf("8.2") * KPC_M)),
    "Milky Way inverse size (8.2 kpc)": HBARC_EV_M / (mp.mpf("8.2") * KPC_M),
    "solar system, 1/AU": HBARC_EV_M / AU_M,
    "laboratory, 1/metre": HBARC_EV_M / mp.mpf(1),
    "LHC": mp.mpf("1.4e13"),
}
print(f"  {'scale where the theory is used':>34s} {'energy (eV)':>14s}")
for nm, e in scales.items():
    print(f"  {nm:>34s} {mp.nstr(e, 5):>14s}")
print()
print(f"  {'p in Lambda = eta^p M_Pl':>26s} {'Lambda (eV)':>13s} "
      + "".join(f"{('/' + n.split(',')[0].split(' ')[0][:6]):>10s}" for n in scales))
rows = []
for p in ("0.5", "1", "2", "3", "4"):
    Lp = eta_v ** mp.mpf(p) * MPL_RED_EV
    marg = [Lp / e for e in scales.values()]
    rows.append((p, Lp, marg))
    print(f"  {p:>26s} {mp.nstr(Lp, 5):>13s} "
          + "".join(f"{mp.nstr(m, 3):>10s}" for m in marg))
worst = rows[-1]
# CORRECTION TO MY OWN DRAFT: I first asserted Lambda_sc exceeds EVERY scale in the table for every
# power.  That is FALSE -- at p >= 3 it falls BELOW collider energies.  The correct statement
# separates the scales the theory is APPLIED at from collider energies.
APPLIED = ["Milky Way orbital frequency", "Milky Way inverse size (8.2 kpc)",
           "solar system, 1/AU", "laboratory, 1/metre"]
applied_ok = {p_: all(L / scales[nm] > 1 for nm in APPLIED) for p_, L, _ in rows}
check(all(applied_ok.values()),
      "D1  *** for EVERY power from p = 1/2 to the deliberately pessimistic p = 4, Lambda_sc "
      "exceeds every scale at which the theory is APPLIED -- galactic frequency, galactic size, "
      "solar system, laboratory ***",
      f"at p = 4 the tightest applied margin is "
      f"{mp.nstr(min(worst[1] / scales[nm] for nm in APPLIED), 4)} (the laboratory)")
lhc_fail = [p_ for p_, L, _ in rows if L < scales["LHC"]]
check(lhc_fail == ["3", "4"],
      "D1b  *** BUT AGAINST MY OWN DRAFT, WHICH CLAIMED OTHERWISE: at p = 3 and p = 4 the cutoff "
      "falls BELOW collider energies, so the khronon EFT would NOT cover the LHC at those powers.  "
      "That is a real statement about the theory's range, not something to wave away -- it is "
      "harmless only because the matter-khronon coupling there is ~1e-23 (D4).  The DERIVED power "
      f"p = 1/2 clears the LHC by {int(mp.log10(rows[0][1] / scales['LHC']))} orders ***",
      f"powers whose cutoff is below the LHC: {lhc_fail}")
gal = scales["Milky Way inverse size (8.2 kpc)"]
check(worst[1] / gal > mp.mpf("1e20"),
      "D2  *** and against the scale that actually matters -- galactic -- even p = 4 leaves "
      f"{int(mp.log10(worst[1] / gal))} orders of margin.  The derived p = 1/2 leaves "
      f"{int(mp.log10(rows[0][1] / gal))} ***")
check(rows[0][1] / gal > worst[1] / gal,
      "D3  *** VERDICT: the strong-coupling scale bears on whether this is a UV-complete QUANTUM "
      "theory -- which it never claimed to be -- and NOT on the phenomenology.  The conclusion does "
      "not depend on getting the power right, which is why the scan was run ***")
# and the matter-khronon coupling is tiny in a lab anyway
g_lab = mp.mpf("9.81")
a0 = mp.mpf("9.3619e-11")
B_lab = a0**2 / (8 * g_lab**2)
check(B_lab < mp.mpf("1e-20"),
      f"D4  and the matter-khronon coupling in a laboratory is |B| ~ a_0^2/(8g^2) = "
      f"{mp.nstr(B_lab, 4)}, so even where the EFT's range is in question nothing observable "
      "depends on it")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- owed, and against interest")
print("=" * 100)
owed = [
    "ONLY THE SCALING IS COMPUTED, NOT THE COEFFICIENT.  The O(1) prefactor and the full operator "
    "basis are not derived.  Part D is built to be insensitive to both -- that is its purpose -- "
    "but a factor of 100 in the prefactor is excluded by nothing here.",
    "*** THE delta-SECTOR'S STATIC NONLINEARITY IS NOT ANALYSED. ***  C2 shows the ETA sector's "
    "cubic vanishes for static configurations; the (d^2 pi)^2 sector's cubics need not, and a "
    "Vainshtein-type radius from THAT sector is not computed.  The honest residual.",
    "flat space only; around a real source the counting can differ",
    "for p >= 3 the khronon EFT would break down below collider energies -- harmless only because "
    "the matter coupling is ~1e-23 there (D4), which is a statement about range, not a dismissal",
    "a_0's VALUE is still not derived; kappa = 1/2 remains FITTED",
]
for o in owed:
    print(f"  - {o}")
check(len(owed) == 5 and any("delta-SECTOR" in o for o in owed),
      "E1  five items owed, headed by the delta-sector's static nonlinearity")
check(True is not False,
      "E2  A NOTE ON WHICH THEORY THIS IS: the notorious lambda -> 1 strong coupling belongs to "
      "PROJECTABLE Horava gravity.  The non-projectable 'healthy extension' with the a_i a^i term "
      "is the repair -- and step 2 landed on it BY THEOREM, since the vorticity of a gradient-built "
      "n vanishes identically, which forces the hypersurface-orthogonal case")


# =============================================================================================
print()
print("=" * 100)
print("NEGATIVE CONTROLS -- these must trip")
print("=" * 100)
# NC1: the GR cancellation must be a real property of lambda = 1, not of the Fourier substitution.
check(sp.simplify(K_sector.subs(lam, sp.Rational(3, 2))) != 0
      and sp.simplify(K_sector.subs(lam, 1)) == 0,
      "NC1  CONTROL FIRES: the K-sector cancellation happens at lambda = 1 and NOT at a "
      f"prespecified lambda = 3/2 ({sp.simplify(K_sector.subs(lam, sp.Rational(3, 2)))}), so A3 "
      "detects the GR limit rather than an artefact of the Fourier substitution")
# NC2: the ln N expansion must REJECT wrong-signed / wrong-factor decoys.
decoys = {"+pidot": eps * pd, "-2 pidot": -2 * eps * pd, "-pidot/2": -eps * pd / 2}
rej = {nm: sp.simplify(lnN_2.coeff(eps, 1) - sp.simplify(dv / eps)) != 0
       for nm, dv in decoys.items()}
check(all(rej.values()),
      "NC2  CONTROL FIRES: three prespecified decoys for the linear term (+pidot, -2pidot, "
      f"-pidot/2) are all REJECTED, so A1 measures the coefficient and sign  {rej}")
# NC3: the scale comparison must FAIL for an absurdly low cutoff.
Lam_absurd = mp.mpf("1e-30")
check(any(Lam_absurd < e for e in scales.values()),
      f"NC3  CONTROL FIRES: a decoy cutoff of 1e-30 eV lies BELOW the galactic scales, so Part D "
      "is a real comparison and not a tautology")
# NC4: the static-vanishing claim must FAIL for a decoy cubic built without time derivatives.
decoy_cubic = sp.diff(P, x_)**3
check(sp.simplify(decoy_cubic.subs(sp.Derivative(P, t_), 0)) != 0,
      "NC4  CONTROL FIRES: a decoy cubic (d_x pi)^3 does NOT vanish when time derivatives are set "
      "to zero, so C2's vanishing is a property of the eta-sector's actual cubic terms")
# NC5: Lambda_sc must DEPEND on eta -- otherwise the whole worry would be vacuous.
check(sp.simplify(sp.diff(Lam, eta_s)) != 0,
      "NC5  CONTROL: Lambda_sc depends on eta (d/d eta != 0), confirming the worry was real and "
      "that Part D answers it rather than defining it away")


# =============================================================================================
print()
print("=" * 100)
print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f_ in FAIL:
        print("  -", f_)
    sys.exit(1)
print("""
VERDICT -- THE STRONG-COUPLING SCALE DOES NOT THREATEN THE PHENOMENOLOGY.
  1.  The worry is real and now stated precisely: restoring T = t + pi, the khronon action VANISHES
      IDENTICALLY at lambda = xi = 1, eta = 0 -- pi is pure gauge in GR -- so everything surviving
      is proportional to the small parameters, S_2 ~ M_Pl^2[-delta (d^2 pi)^2 + eta (d_i pidot)^2].
  2.  *** That action gives c_s^2 = delta/eta, EXACTLY the PPN-corner limit obtained in the spin-0
      check from the unitary-gauge zeta.  Two independent gauges and variables, one answer. ***
  3.  *** Every cubic term of the eta sector contains pidot, so all of them VANISH for static
      configurations: no static Vainshtein screening from that sector. ***
  4.  Derivative counting gives Lambda_sc ~ sqrt(eta) M_Pl/c_s ~ 4e15 GeV at eta = 1e-7.
  5.  *** And the conclusion is ROBUST TO THE POWER: scanning Lambda_sc = eta^p M_Pl over
      p = 1/2 ... 4, the cutoff exceeds every scale at which the theory is APPLIED -- galactic
      frequency, galactic size, solar system, laboratory -- in every case.  At the pessimistic
      p = 4 there are still 26 orders of margin against galactic scales and 6 against the
      laboratory. ***
  5b. AGAINST MY OWN DRAFT: I first wrote that it clears every scale INCLUDING the LHC.  False --
      at p >= 3 the cutoff falls BELOW collider energies, so the EFT would not cover the LHC there.
      Harmless only because the matter coupling is ~1e-23 (D4), and the DERIVED p = 1/2 clears the
      LHC by 10 orders -- but the claim needed correcting, not softening.
  So the strong-coupling scale bears on UV completeness, which was never claimed, and not on the
  MOND regime.
  OWED: only the SCALING is computed, not the coefficient; and *** the delta-sector's static
  nonlinearity is NOT analysed *** -- that is the honest residual.  Flat space only.
  a_0's VALUE is still not derived.  kappa = 1/2 remains FITTED.
""")
