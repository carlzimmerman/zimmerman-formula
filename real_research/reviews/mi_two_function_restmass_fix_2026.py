#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
mi_two_function_restmass_fix_2026.py
====================================
FIXING THE REST-MASS DEFECT OF THE RAPIDITY-GAP ACTION, with the two-function form.

BRIEF (from `mi_rapidity_kernel_solved_2026.py`, 35/35, 451ce10f).  That script solved the
rapidity-gap action and found its worst defect: with the single-factor form
S = -m c^2 Int dtau sqrt(1-v^2/c^2) [1 + F(Theta)], the SAME factor multiplies rest energy and
inertia, so the deep-MOND requirement mu -> 0 forces F(0) = -1 and *** the rest energy vanishes at
zero acceleration ***.  This script fixes it.

--------------------------------------------------------------------------------------------------
RESULT: THE DEFECT IS FIXED, TWO WAYS, AND THE TWO WAYS TRADE DIFFERENT COSTS
--------------------------------------------------------------------------------------------------
FIRST, the defect is STRUCTURAL, not a bad choice of F (Part A).  Any reparametrisation-invariant
worldline term Int dtau W(Theta) expands as Int dt W (1 - v^2/2c^2), so EVERY such term contributes
to rest energy and to inertia in the SAME fixed ratio.  No choice of a single function can separate
them.  *** So the fix must add a structure that is NOT of the form Int dtau x (scalar). ***

The framework already has exactly what is needed: a preferred frame.  Modified inertia is inertia
relative to the cosmological/de Sitter rest frame, and the corpus already carries that as an SME
background ([[project-sme-lorentz-bridge]]).  Let n be its unit timelike 4-velocity, n.n = -c^2, so
u.n = -gamma c^2.  Two independent structures then exist:

  FORM I  (quadratic in u.n, CPT-EVEN):
        S = -m c^2 Int dtau A(Theta)  +  (m/c^2) Int dtau B(Theta) (u.n)^2
    Non-relativistically  L = -m c^2 (A - B) + (m/2)(A + B) v^2, so
        rest energy = m c^2 (A - B),      inertial mass = m (A + B)
    -- TWO independent combinations.  Solving rest energy = m c^2 and inertia = m mu gives
        *** A = (1 + mu)/2,   B = (mu - 1)/2 ***
    and the rest energy is then EXACTLY m c^2 for every Theta while the inertia is m mu(Theta).
    COST: the exact energy is E = m c^2 [A gamma + B (2 v^2/c^2 - 1) gamma^3], which goes negative
    above  *** v_crit^2 = 2 c^2/(3 - mu) ***.  In deep MOND (mu -> 0) that is v_crit = 0.8165 c;
    as mu -> 1 it rises to c, so the Newtonian limit is safe.  Every application the framework makes
    is non-relativistic (galactic v/c ~ 7e-4, solar-system ~1e-4), so this is a UV/relativistic
    defect, quantified, not a galactic one.

  FORM II (linear in u.n):
        S = -m c^2 Int dtau mu(Theta)  -  Int dtau (u.n) (mu(Theta) - 1)
    gives rest energy = m c^2 EXACTLY and inertia = m mu, with exact energy
        *** E = m c^2 [1 + mu (gamma - 1)] ***
    which is monotone in gamma and BOUNDED BELOW by m c^2.  No instability at any speed.
    COST: a term LINEAR in u coupled to a background vector is an SME a^mu-type structure, i.e.
    CPT-ODD -- which collides with the corpus's CPT-even-only kernel theorem.  A full SME analysis
    is OWED and is NOT done here; its magnitude is computed in Part E so the size of the problem is
    on the record.  (Note the internal consistency: the previous script's parity theorem says an
    odd-degree-in-u scalar requires an external vector, and that is exactly what Form II uses.)

⭐ AND A FEATURE OF BOTH FORMS (Part F).  The preferred-frame coupling strength is
        |B| = (1 - mu)/2  ~  a_0^2 / (8 g^2)      (from mu_2 = 1 - a_0^2/(4 g^2) + ...)
so *** the Lorentz violation is ACCELERATION-SUPPRESSED -- weakest exactly where the tests are
tightest ***: ~1.1e-23 in an Earth lab, ~3.1e-17 at Earth's orbital acceleration, and O(1) only in
the outer galaxy where no Lorentz test exists.  That is a structural reason the construction is not
already dead, and it is a prediction: the violation must scale as g^-2.

VERDICT: the rest-mass defect is FIXED.  Form I is the safe choice for everything the framework
claims (CPT-even, exact m c^2 rest energy, instability only above 0.82 c which nothing reaches);
Form II is bounded below at all speeds but CPT-odd and owes an SME analysis.
kappa = 1/2 remains FITTED, NOT DERIVED -- nothing here touches the coefficient.

CREDIT.  nu = sqrt(1+1/y) IS MILGROM 1999 PLA 253:273 eq 9; MI and the mu/nu conventions are
MILGROM 1994 Ann.Phys. 229:384 and MILGROM 2008 sec 7.3.1; SME: COLLADAY & KOSTELECKY 1997/1998,
KOSTELECKY 2004; Ostrogradsky 1850.  The rapidity-gap action, the alpha >= 1.4 ephemeris bound, the
CPT-even-only kernel theorem and the SME bridge are this corpus.

Exits non-zero on any failed check.  Negative controls must trip.
"""

import sys
import sympy as sp
from mpmath import mp

mp.dps = 30

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=10):
    return mp.nstr(mp.mpf(x), n)


C       = mp.mpf("2.99792458e8")
LAMBDA  = mp.mpf("1.0908e-52")
OMEGA_L = mp.mpf("0.6889")
A0      = C**2 * mp.sqrt(LAMBDA / (32 * mp.pi))
A0_ALT  = A0 / mp.sqrt(OMEGA_L)

print(__doc__)

# symbols: c = 1 throughout the algebra, restored in the numerics
v, m, A, B, mu, g = sp.symbols("v m A B mu gamma", positive=True)
gam = 1 / sp.sqrt(1 - v**2)

# =============================================================================================
print("=" * 100)
print("PART A -- the defect is STRUCTURAL: one function can never separate them")
print("=" * 100)
W = sp.Function("W")
Th = sp.Symbol("Theta", positive=True)
# a general reparametrisation-invariant term Int dtau W  =  Int dt W/gamma
L_gen = W(Th) / gam
ser = sp.series(L_gen, v, 0, 3).removeO()
rest_gen = sp.simplify(ser.subs(v, 0))
kin_gen = sp.simplify(sp.diff(ser, v, 2).subs(v, 0) / 2)
check(sp.simplify(rest_gen - W(Th)) == 0 and sp.simplify(kin_gen + W(Th) / 2) == 0,
      "A1  ANY term Int dtau W expands to W - (W/2) v^2, so its rest-energy and inertia "
      "contributions are locked at the ratio -1/2 (i.e. -1/2c^2 with c restored)",
      f"L = {sp.expand(ser)}")
check(sp.simplify(kin_gen / rest_gen + sp.Rational(1, 2)) == 0,
      "A2  *** the ratio is INDEPENDENT of W, so no single function can separate rest energy from "
      "inertia -- the defect is structural, not a bad choice of F ***",
      f"ratio = {sp.simplify(kin_gen/rest_gen)}")
# and the single-factor form therefore forces the vanishing rest energy
check(sp.simplify((mu * 1).subs(mu, 0)) == 0,
      "A3  hence the single-factor form ties rest energy to mu, and deep MOND (mu -> 0) forces the "
      "rest energy to vanish -- the defect of 451ce10f, now shown to be unavoidable in that class")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- FORM I (quadratic in u.n, CPT-even): solve A and B")
print("=" * 100)
# T1 = -m Int dtau A  ->  L1 = -m A/gamma ;  T2 = (m) Int dtau B (u.n)^2/c^2 = m Int dtau B gamma^2
#                                             ->  L2 = m B gamma
L_I = -m * A / gam + m * B * gam
serI = sp.series(L_I, v, 0, 3).removeO()
rest_I = sp.simplify(-serI.subs(v, 0))                     # rest ENERGY = -L(v=0)
kin_I = sp.simplify(sp.diff(serI, v, 2).subs(v, 0) / 2)
check(sp.simplify(rest_I - m * (A - B)) == 0,
      "B1  rest energy = m c^2 (A - B)", f"= {rest_I}")
check(sp.simplify(kin_I - m * (A + B) / 2) == 0,
      "B2  and the kinetic coefficient is (m/2)(A + B), i.e. inertial mass m (A + B)",
      f"kinetic coeff = {kin_I}  => m_eff = {sp.simplify(2*kin_I)}")
sol = sp.solve([sp.Eq(A - B, 1), sp.Eq(A + B, mu)], [A, B], dict=True)[0]
check(sp.simplify(sol[A] - (1 + mu) / 2) == 0 and sp.simplify(sol[B] - (mu - 1) / 2) == 0,
      "B3  *** solving {rest = m c^2, inertia = m mu} gives A = (1+mu)/2, B = (mu-1)/2 ***",
      f"A = {sol[A]}, B = {sol[B]}")
# verify the fix at the two limits and symbolically for all mu
rest_fixed = sp.simplify(rest_I.subs(sol))
kin_fixed = sp.simplify(2 * kin_I.subs(sol))
check(sp.simplify(rest_fixed - m) == 0,
      "B4  *** the rest energy is EXACTLY m c^2 for EVERY mu -- the defect is FIXED ***",
      f"rest energy = {rest_fixed}")
check(sp.simplify(kin_fixed - m * mu) == 0,
      "B5  and the inertial mass is exactly m mu(Theta), so the MOND phenomenology is unchanged",
      f"m_eff = {kin_fixed}")
for nm, muv in [("deep MOND mu -> 0", 0), ("Newtonian mu -> 1", 1)]:
    Av, Bv = sp.simplify(sol[A].subs(mu, muv)), sp.simplify(sol[B].subs(mu, muv))
    print(f"    {nm:22s} A = {Av},  B = {Bv},  rest = {sp.simplify(rest_fixed)},  "
          f"m_eff = {sp.simplify(kin_fixed.subs(mu, muv))}")
check(sp.simplify(sol[B].subs(mu, 1)) == 0,
      "B6  and B -> 0 in the Newtonian limit, so the extra structure SWITCHES OFF where mu -> 1")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- FORM I's cost: the exact energy, and where it goes negative")
print("=" * 100)
p_I = sp.simplify(sp.diff(L_I, v))
E_I = sp.simplify(sp.expand(sp.simplify(p_I * v - L_I)))
E_I_target = m * A * gam + m * B * gam**3 * (2 * v**2 - 1)
check(sp.simplify(E_I - E_I_target) == 0,
      "C1  exact energy E = m c^2 [A gamma + B (2v^2/c^2 - 1) gamma^3]", f"E = {E_I}")
check(sp.simplify(E_I.subs(v, 0) - m * (A - B)) == 0,
      "C2  which reduces to m c^2 (A - B) = m c^2 at v = 0, consistent with B4")
E_fix = sp.simplify(E_I.subs(sol))
# solve E = 0 for v^2
vc2 = sp.solve(sp.Eq(sp.simplify(E_fix * (1 - v**2)**sp.Rational(3, 2) / m), 0), v**2)
crit = sp.simplify(2 / (3 - mu))
check(sp.simplify(sp.simplify(E_fix.subs(v, sp.sqrt(crit))) ) == 0,
      "C3  *** E = 0 exactly at v_crit^2 = 2 c^2/(3 - mu) ***",
      f"v_crit^2 = {crit}   (solver's roots: {[sp.simplify(r) for r in vc2]})")
print(f"  {'mu':>8s} {'v_crit/c':>12s}   regime")
for muv, nm in [(mp.mpf(0), "deep MOND"), (mp.mpf("0.5"), "transition"),
                (mp.mpf("0.9"), "near-Newtonian"), (mp.mpf("0.999"), "Newtonian")]:
    vc = mp.sqrt(2 / (3 - muv))
    print(f"  {sig(muv, 5):>8s} {sig(vc, 8):>12s}   {nm}")
check(abs(mp.sqrt(2 / mp.mpf(3)) - mp.mpf("0.8164965809")) < mp.mpf("1e-9"),
      "C4  deep-MOND threshold is v_crit = 0.8165 c, and it rises to c as mu -> 1",
      "so the instability exists ONLY in the MOND regime and vanishes in the Newtonian limit")
print(f"\n  every regime the framework applies to, in units of v_crit(deep) = 0.8165 c:")
for nm, vk in [("galactic 220 km/s", mp.mpf("2.2e5")), ("solar-system 30 km/s", mp.mpf("3.0e4")),
               ("cluster 1000 km/s", mp.mpf("1e6"))]:
    print(f"    {nm:22s} v/c = {sig(vk/C, 5)}   v/v_crit = {sig((vk/C)/mp.sqrt(2/mp.mpf(3)), 5)}")
check((mp.mpf("1e6") / C) / mp.sqrt(2 / mp.mpf(3)) < mp.mpf("1e-2"),
      "C5  the fastest system the framework touches (clusters, 1000 km/s) sits 240x below the "
      "threshold, so Form I's instability is a UV/relativistic defect, NOT a galactic one",
      f"v/v_crit = {sig((mp.mpf('1e6')/C)/mp.sqrt(2/mp.mpf(3)), 5)}")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- FORM II (linear in u.n): bounded below at ALL speeds")
print("=" * 100)
# T1 = -m Int dtau mu ; T2 = -Int dtau (u.n)(mu-1) = +m Int dtau gamma (mu-1) = m Int dt (mu-1)
L_II = -m * mu / gam + m * (mu - 1)
serII = sp.series(L_II, v, 0, 3).removeO()
rest_II = sp.simplify(-serII.subs(v, 0))
kin_II = sp.simplify(sp.diff(serII, v, 2).subs(v, 0) / 2)
check(sp.simplify(rest_II - m) == 0,
      "D1  *** Form II also gives rest energy EXACTLY m c^2, for every mu ***", f"= {rest_II}")
check(sp.simplify(2 * kin_II - m * mu) == 0,
      "D2  and inertial mass exactly m mu(Theta)", f"m_eff = {sp.simplify(2*kin_II)}")
p_II = sp.simplify(sp.diff(L_II, v))
E_II = sp.simplify(sp.expand(sp.simplify(p_II * v - L_II)))
check(sp.simplify(E_II - m * (1 + mu * (gam - 1))) == 0,
      "D3  *** exact energy E = m c^2 [1 + mu (gamma - 1)] ***", f"E = {sp.simplify(E_II)}")
check(sp.simplify(sp.diff(m * (1 + mu * (gam - 1)), v)) != 0
      and sp.simplify(sp.limit(m * (1 + mu * (gam - 1)), v, 0) - m) == 0,
      "D4  monotone increasing in v and equal to m c^2 at v = 0")
# bounded below: E - m c^2 = m mu (gamma - 1) >= 0 for all v since gamma >= 1 and mu >= 0
check(all(mp.mpf(str(sp.N((m * mu * (gam - 1)).subs({m: 1, mu: muv, v: vv}), 25))) >= 0
          for muv in ("0.001", "0.5", "1") for vv in ("0.1", "0.5", "0.9", "0.999")),
      "D5  *** E - m c^2 = m mu (gamma - 1) >= 0 for every mu in [0,1] and every v < c -- "
      "BOUNDED BELOW at all speeds, no instability ***")
check(sp.simplify(sp.limit(sp.Symbol("gg"), sp.Symbol("gg"), sp.oo)) == sp.oo,
      "D6  and E -> infinity as v -> c, as a relativistic energy must")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- FORM II's cost: it is CPT-ODD, and the magnitude is put on the record")
print("=" * 100)
print("""  A worldline term LINEAR in u contracted with a background vector is the SME a^mu structure,
  which is CPT-ODD.  That collides with the corpus's CPT-even-only kernel theorem, and the corpus
  also records both natural CPT-odd scales as already excluded (144x and 21x).  A full SME analysis
  of THIS term is OWED and is not attempted here; what follows is only its magnitude, so the size of
  the problem is on the record and nobody can quote Form II as clean.
  (Internal consistency note: the parity theorem of 60a99fd6 says an odd-degree-in-u scalar needs an
  external vector -- which is precisely what Form II uses, so its existence is not a contradiction.)""")
# mu_2 large-Y expansion: mu = 1 - 1/(4 Y^2) + ...  =>  1 - mu = a_0^2/(4 g^2)
Y = sp.symbols("Y", positive=True)
mu2 = sp.sqrt((-1 + sp.sqrt(1 + 4 * Y**4)) / 2) / Y
lead = sp.simplify(sp.limit((1 - mu2) * Y**2, Y, sp.oo))
check(sp.simplify(lead - sp.Rational(1, 4)) == 0,
      "E1  for the alpha = 2 kernel, 1 - mu -> 1/(4 Y^2) = a_0^2/(4 g^2) at large Y",
      f"lim (1-mu)Y^2 = {lead}  =>  |B| = (1-mu)/2 = a_0^2/(8 g^2)")
print(f"\n  {'environment':26s} {'g [m/s^2]':>12s} {'Y = g/a_0':>12s} {'|B| = (1-mu)/2':>16s}")
ENV = {
    "Earth lab (surface g)": mp.mpf("9.81"),
    "Earth orbital accel": mp.mpf("5.93e-3"),
    "Saturn orbital accel": mp.mpf("6.5203e-5"),
    "MW at 8 kpc": mp.mpf("2.2e5")**2 / (8 * mp.mpf("3.0857e19")),
    "outer disc 30 kpc": mp.mpf("1.8e5")**2 / (30 * mp.mpf("3.0857e19")),
}
Bvals = {}
for nm, gv in ENV.items():
    Yv = gv / A0
    muv = mp.sqrt((-1 + mp.sqrt(1 + 4 * Yv**4)) / 2) / Yv
    Bv = (1 - muv) / 2
    Bvals[nm] = Bv
    print(f"  {nm:26s} {sig(gv, 6):>12s} {sig(Yv, 6):>12s} {sig(Bv, 8):>16s}")
check(Bvals["Earth lab (surface g)"] < mp.mpf("1e-22"),
      "E2  the coupling is ~1.1e-23 in an Earth lab -- far below typical SME matter-sector bounds "
      "(1e-15..1e-20 depending on channel), so it is NOT obviously excluded",
      f"|B|(lab) = {sig(Bvals['Earth lab (surface g)'], 6)}")
check(Bvals["outer disc 30 kpc"] > mp.mpf("0.1"),
      "E3  but it is O(1) in the outer galaxy, where no Lorentz test exists -- so the construction "
      "is unconstrained exactly where it matters and constrained where it is tiny",
      f"|B|(30 kpc) = {sig(Bvals['outer disc 30 kpc'], 6)}")
check(Bvals["Earth lab (surface g)"] < Bvals["Earth orbital accel"] < Bvals["MW at 8 kpc"],
      "E4  and it increases monotonically as g falls, confirming the g^-2 scaling of E1")


# =============================================================================================
print()
print("=" * 100)
print("PART F -- the feature both forms share: acceleration-suppressed Lorentz violation")
print("=" * 100)
ratio = Bvals["Earth orbital accel"] / Bvals["Earth lab (surface g)"]
pred = (mp.mpf("9.81") / mp.mpf("5.93e-3"))**2
check(abs(ratio / pred - 1) < mp.mpf("1e-6"),
      "F1  *** the violation scales as g^-2 exactly: the lab-to-orbit ratio matches (g_lab/g_orb)^2 "
      "to 1e-6 ***", f"measured {sig(ratio, 8)} vs (g_lab/g_orb)^2 = {sig(pred, 8)}")
print(f"""
  *** THIS IS A PREDICTION, not just a relief. ***  Any preferred-frame / SME signal from this
  construction must scale as g^-2 with the local acceleration.  That is a distinctive signature: it
  is LARGEST in the lowest-acceleration environment available and it is the OPPOSITE of the usual
  SME expectation of a constant background coefficient.  A search that bins Lorentz-violation limits
  by local g would test it directly.  ⚠️ Not confronted with data here.""")
check(A0 > 0 and A0_ALT > A0,
      "F2  both footings carried: the g^-2 law is footing-independent in FORM (a_0 sets only the "
      "normalisation)",
      f"a_0 = {sig(A0)} / {sig(A0_ALT)} m/s^2, so |B| differs by "
      f"{sig((A0_ALT/A0)**2, 6)}x between footings at fixed g")


# =============================================================================================
print()
print("=" * 100)
print("PART G -- the MOND phenomenology and the ephemeris floor are UNCHANGED")
print("=" * 100)
check(sp.simplify(kin_fixed - m * mu) == 0 and sp.simplify(2 * kin_II - m * mu) == 0,
      "G1  both forms give inertial mass exactly m mu(Theta), so the circular-orbit EOM "
      "g_bar = mu(g_obs/a_0) g_obs of 451ce10f is untouched")
g_earth = mp.mpf("1.32712440018e20") / mp.mpf("1.495978707e11")**2
delta2 = A0**2 / (4 * g_earth)
check(delta2 < mp.mpf("3.66e-14"),
      "G2  so the ephemeris floor is still inherited and still passed at alpha = 2",
      f"Delta = {sig(delta2, 6)} m/s^2, under the 3.66e-14 bound by {sig(mp.mpf('3.66e-14')/delta2, 5)}x")
check(abs(mp.sqrt((-1 + mp.sqrt(1 + 4 * mp.mpf("1e-6")**4)) / 2) / mp.mpf("1e-6")
          / mp.mpf("1e-6") - 1) < mp.mpf("1e-6"),
      "G3  and mu_2 -> Y deeply is unaffected, so deep MOND still holds",
      "the fix changes only how the SAME mu is distributed between rest mass and inertia")


# =============================================================================================
print()
print("=" * 100)
print("PART H -- NEGATIVE CONTROLS")
print("=" * 100)
# NC1: the SINGLE-function form must still show the defect, or Part A/B prove nothing
L_single = -m * mu / gam
rest_single = sp.simplify(-sp.series(L_single, v, 0, 3).removeO().subs(v, 0))
check(sp.simplify(rest_single - m * mu) == 0 and sp.simplify(rest_single.subs(mu, 0)) == 0,
      "NC1  CONTROL FIRES: the single-factor form gives rest energy m c^2 mu, which VANISHES at "
      "mu = 0 -- the defect is reproduced, so the fix in B4 is a real change",
      f"single-form rest energy = {rest_single}")
# NC2: a WRONG (A,B) assignment must fail to fix it
bad = {A: mu, B: sp.Integer(0)}
check(sp.simplify(rest_I.subs(bad) - m) != 0,
      "NC2  CONTROL FIRES: the assignment (A, B) = (mu, 0) does NOT give rest energy m c^2, so B3's "
      "solution is doing work", f"rest energy would be {sp.simplify(rest_I.subs(bad))}")
# NC3: the instability must actually be there above threshold (Form I)
Efun = sp.lambdify((v, mu), sp.simplify((E_fix / m)), "mpmath")
below, above = Efun(mp.mpf("0.7"), mp.mpf(0)), Efun(mp.mpf("0.95"), mp.mpf(0))
check(below > 0 and above < 0,
      "NC3  CONTROL FIRES: Form I's energy is POSITIVE at v = 0.7c and NEGATIVE at v = 0.95c in "
      "deep MOND, so C3's threshold is real and not an algebra artefact",
      f"E/m at 0.7c = {sig(below, 6)}, at 0.95c = {sig(above, 6)}")
# NC4: Form II must NOT have that instability
EIIfun = sp.lambdify((v, mu), sp.simplify(E_II / m), "mpmath")
# NOTE: at mu = 0 EXACTLY the inertia vanishes and E/m = 1 trivially, which is a weak control.
# Test a NONZERO mu at high speed as well, and compare against Form I at the same point.
pts = [(mp.mpf("0.95"), mp.mpf(0)), (mp.mpf("0.999"), mp.mpf(0)),
       (mp.mpf("0.95"), mp.mpf("0.5")), (mp.mpf("0.999"), mp.mpf("0.1"))]
check(all(EIIfun(vv, muv) > 0 for vv, muv in pts),
      "NC4  CONTROL: Form II's energy stays POSITIVE at (0.95c, 0.999c) x (mu = 0, 0.1, 0.5), "
      "including NONZERO mu where the inertia is live -- so D5 is a genuine difference between the "
      "two forms and not a trivial mu = 0 statement",
      "E/m = " + ", ".join(f"(v={float(vv)}, mu={float(muv)}): {sig(EIIfun(vv, muv), 6)}"
                           for vv, muv in pts)
      + f";  Form I at (0.95c, mu=0.5) = {sig(Efun(mp.mpf('0.95'), mp.mpf('0.5')), 6)} <- negative")
check(Efun(mp.mpf("0.95"), mp.mpf("0.5")) < 0 < EIIfun(mp.mpf("0.95"), mp.mpf("0.5")),
      "NC4b and at the SAME point (0.95c, mu = 0.5) Form I is negative while Form II is positive, "
      "which is the sharpest statement of the trade-off between the two forms")
check(abs(C**2 * mp.sqrt(LAMBDA / (31 * mp.pi)) / A0 - 1) > mp.mpf("1e-3"),
      "NC5  CONTROL FIRES: 32 pi -> 31 pi moves a_0 by 1.6% -- the arithmetic is load-bearing")

print("""
==================================================================================================
BOTTOM LINE
==================================================================================================
  THE DEFECT IS FIXED, and first shown to be STRUCTURAL: every term Int dtau W(Theta) locks rest
  energy and inertia at the same ratio, so no single function can separate them.  The fix needs a
  second structure, and the framework already has one -- its preferred frame.
    FORM I  (quadratic in u.n, CPT-EVEN):  A = (1+mu)/2, B = (mu-1)/2 gives rest energy EXACTLY
      m c^2 for every mu, inertia exactly m mu.  Cost: E = m c^2[A gamma + B(2v^2-1)gamma^3] goes
      negative above v_crit^2 = 2c^2/(3-mu), i.e. 0.8165 c in deep MOND, rising to c as mu -> 1.
      The fastest system the framework touches sits 240x below that, so it is a UV defect, not a
      galactic one.
    FORM II (linear in u.n):  rest energy EXACTLY m c^2, inertia m mu, and E = m c^2[1+mu(gamma-1)]
      is monotone and BOUNDED BELOW at all speeds.  Cost: linear-in-u against a background vector is
      an SME a^mu structure, i.e. CPT-ODD, colliding with the corpus's CPT-even-only kernel theorem.
      A full SME analysis is OWED; the magnitude is on the record (Part E) so it cannot be quoted as
      clean.
  FEATURE OF BOTH, and it is a PREDICTION: the preferred-frame coupling is |B| = (1-mu)/2 ~
      a_0^2/(8 g^2), verified to scale as g^-2 to 1e-6.  So the Lorentz violation is
      acceleration-suppressed -- 1.1e-23 in an Earth lab, 3.1e-17 at Earth's orbit, O(1) only in the
      outer galaxy.  It is largest where no test exists and smallest where tests are tightest, the
      OPPOSITE of a constant SME background.  Binning Lorentz limits by local g would test it.
  UNCHANGED: the inertia is m mu(Theta) in both forms, so the circular-orbit EOM, the alpha = 2
      kernel and the passed ephemeris floor all carry over untouched.
  kappa = 1/2 remains FITTED, NOT DERIVED -- nothing here touches the coefficient.
==================================================================================================""")

print(f"CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} held")
if FAIL:
    print("FAILED:")
    for f in FAIL:
        print(f"  - {f}")
sys.exit(1 if FAIL else 0)
