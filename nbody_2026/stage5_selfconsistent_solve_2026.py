#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage5_selfconsistent_solve_2026.py
===================================
THE SELF-CONSISTENT SOLVE -- AND IT KILLS THE STAGE-4 SUPPRESSOR, FOR A REASON MY GATES COULD NOT SEE.

Stage 4 built a rising Y-dependent Q-mass, F ⊃ A_s S(Y/a_0^2)(Q-Q_0)^2, showed it drives the field
amplitude u -> 0 in galaxy interiors, passed eight gates, and left ONE thing undetermined: where the
expelled charge settles.  This is that solve.  It returns a verdict, and the verdict is that the
mechanism runs BACKWARDS.

--------------------------------------------------------------------------------------------------
THE ERROR IN STAGE 4, NAMED FIRST
--------------------------------------------------------------------------------------------------
Every stage-4 gate tested u, the field amplitude.  *** THE OBSERVABLE IS NOT u.  IT IS THE CONSERVED
SHIFT CHARGE. ***  With the suppressor included, exactly (sympy, Part A):

        n    = (mu^2 + 2 A_s S) u                 <- shift-charge density, J^0 = dL/d(phi-dot)
        rho  = Q_0 n + O(u^2)                     <- energy density is Q_0 TIMES THE CHARGE
        cost = n^2 / (2(mu^2 + 2 A_s S))          <- field energy at FIXED charge

So suppressing u at fixed charge does NOT remove mass: it means the SAME charge is carried by a
SMALLER amplitude.  And worse, d(cost)/d(A_s S) < 0: turning the suppressor on makes a region a
CHEAPER place to store charge.  *** The suppressor ATTRACTS the charge it was built to expel. ***

--------------------------------------------------------------------------------------------------
THE SOLVE
--------------------------------------------------------------------------------------------------
Minimise E = int [Q_0 n + n^2/(2(mu^2+2 A_s S))] dV + E_grav[rho = Q_0 n] at FIXED total charge.
Euler-Lagrange with multiplier lambda gives the equilibrium profile in closed form:

        n(r) = (mu^2 + 2 A_s S(r)) * (lambda - Q_0 - Phi(r)) ,    truncated where the bracket <= 0.

Both factors rise inward: -Phi is deepest in the centre, AND S is largest in the centre (that is what
the suppressor was for).  The profile is therefore DOUBLY centrally concentrated -- the opposite of
the flat, evacuated configuration the framework needs.

AND INCLUDING THE DUST'S OWN SELF-GRAVITY (Part D) UNCOVERS AN ERROR IN STAGES 2 AND 3, in the
theory's FAVOUR: rho = Q_0 n with p = n^2/(2 mu^2) means p = K rho^2, so c_s^2 = 2 K rho RISES with
density.  Stages 2-3 used the DBI background MAXIMUM sound speed and wrongly concluded "no support";
the correct statement is that the dust is an n = 1 POLYTROPE with a mass-independent equilibrium
radius of ~105 pc.  That equilibrium is nevertheless OUT OF REACH -- its density exceeds the DBI
saturation density by 14x, where the sound speed collapses -- and would be excluded by the Galactic
Centre anyway.  Stage 3's endpoint survives by a longer and better-understood route.

HONESTY: this is a fourth self-caught error in this sequence, and the largest -- a whole mechanism --
plus a fifth (stages 2-3's support analysis) found while fixing it.  Negative controls establish that
the kills are properties of the theory rather than of the method: a sector with quadratic-in-u energy
WOULD be suppressible (NC-A), and a stiffer sector WOULD give a kpc-scale core (NC-D).
"""

import sys
import mpmath as mp
import sympy as sp

mp.mp.dps = 25
FAIL = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def sig(x, n=4):
    return mp.nstr(mp.mpf(x), n)


# --- framework numbers ---
A0 = {"canon": mp.mpf("9.3619e-11"), "alt": mp.mpf("1.1279e-10")}
G_KMS = mp.mpf("4.300e-9")           # Mpc (km/s)^2/Msun
MPC_M = mp.mpf("3.0857e22")
M_BAR = mp.mpf("6e10")               # Msun, L* baryons
M_DUST = mp.mpf("2.51e12")           # Msun, the smooth-accretion allocated share
R_MIN, R_MAX = mp.mpf("0.001"), mp.mpf("1.0")     # Mpc
N_S = 8                              # the stage-4 surviving shape power
A_S = mp.mpf("5000")                 # Mpc^-2, the amplitude stage 4's Gate 2 demanded
MU2 = mp.mpf("100")                  # the bump machinery's mu^2 units
RAR_SCAT = mp.mpf("0.034")           # dex, intrinsic RAR scatter
V_C = mp.mpf("200")                  # km/s

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- the exact relations: what the observable actually is")
print("=" * 100)

u_, Q0_, mu_, As_, S_, n_ = sp.symbols("u Q_0 mu A_s S n", positive=True)
L_ = mu_ ** 2 * u_ ** 2 / 2 + As_ * S_ * u_ ** 2
n_of_u = sp.simplify(sp.diff(L_, u_))
rho_ = sp.simplify((Q0_ + u_) * sp.diff(L_, u_) - L_)
rho_lead = sp.simplify(sp.series(rho_, u_, 0, 2).removeO())

check(sp.simplify(n_of_u - (mu_ ** 2 + 2 * As_ * S_) * u_) == 0,
      f"A1  the conserved shift-charge density is n = dL/d(phi-dot) = {sp.factor(n_of_u)} -- the "
      "suppressor enters here, multiplying u",
      "shift symmetry phi -> phi + c is intact (Q is shift-invariant), so n is conserved")

check(sp.simplify(rho_lead - Q0_ * n_of_u) == 0,
      "A2  *** AND THE ENERGY DENSITY IS rho = Q_0 * n TO LEADING ORDER -- proportional to the "
      "CONSERVED CHARGE, not to the field amplitude.  Suppressing u at fixed n removes NO mass; it "
      "only means the same charge is carried by a smaller amplitude ***",
      "this is the relation every stage-4 gate was blind to")

cost = sp.simplify((rho_ - Q0_ * n_of_u).subs(u_, n_ / (mu_ ** 2 + 2 * As_ * S_)))
dcost = sp.simplify(sp.diff(cost, As_))
check(sp.simplify(cost - n_ ** 2 / (2 * (mu_ ** 2 + 2 * As_ * S_))) == 0 and dcost.could_extract_minus_sign(),
      f"A3  *** AND THE DIRECTION IS BACKWARDS: the field energy at FIXED charge is "
      f"{cost}, whose derivative in (A_s S) is NEGATIVE ({dcost}).  Turning the suppressor ON makes "
      "a region a CHEAPER place to store charge -- it ATTRACTS what it was built to expel ***",
      "the mechanism's sign is wrong, not its magnitude")

# NC-A (negative control): if the leading term vanished (rho ~ u^2 instead of Q_0 n), suppression
# WOULD reduce the mass.  Verify the machinery would say so, or A2/A3 is an artefact of the setup.
rho_nolead = sp.simplify(rho_ - Q0_ * n_of_u)          # the u^2 remainder
check(sp.simplify(rho_nolead.subs(u_, n_ / (mu_ ** 2 + 2 * As_ * S_))) == cost and cost != 0,
      "NC-A  CONTROL: the u^2 remainder alone DOES fall as A_s S grows (it is exactly the cost "
      "above), so a theory whose dust energy were quadratic in u would be suppressible.  The kill is "
      "specific to the LINEAR rho = Q_0 n term, i.e. to shift-charge conservation",
      "which is why the diagnosis is structural rather than numerical")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- THE THEOREM: no Y-dependent Q-mass can change how much dust a galaxy has")
print("=" * 100)
print("""
  rho = Q_0 n  and  d/dt int n dV = 0  (shift symmetry) together give, for ANY function S(Y) and ANY
  amplitude A_s:
                    M_dust(region) = Q_0 * N(region) ,
  and the total charge in a collapsing basin is fixed by what fell in -- which the smooth-accretion
  theorem already settled.  A local mass term redistributes u, never N.
""")
check(sp.simplify(sp.diff(rho_lead / n_of_u, As_)) == 0
      and sp.simplify(rho_lead / n_of_u - Q0_) == 0,
      "B1  *** THEOREM: rho/n = Q_0 is INDEPENDENT of A_s and of S -- verified symbolically.  So no "
      "Y-dependent Q-mass, of any shape or amplitude, alters the dust mass associated with a given "
      "charge.  The stage-4 mechanism could not have worked ***",
      "d(rho/n)/dA_s = 0 identically")

# B2 -- and the theorem must be SPECIFIC to shift symmetry.  The right test is not rho/n but
# CONSERVATION itself: the Noether current obeys d_mu J^mu = dL/dphi, which vanishes iff phi appears
# only through derivatives.  Add an explicit potential and it stops vanishing.
phi_ = sp.Symbol("varphi", real=True)
m_ = sp.Symbol("m", positive=True)
L_shift = mu_ ** 2 * u_ ** 2 / 2 + As_ * S_ * u_ ** 2          # phi enters only via u = Q - Q_0
L_broken = L_shift - m_ ** 2 * phi_ ** 2 / 2                    # explicit shift breaking
check(sp.diff(L_shift, phi_) == 0 and sp.simplify(sp.diff(L_broken, phi_)) == -m_ ** 2 * phi_,
      "B2  *** and the theorem is SPECIFIC to shift symmetry: d_mu J^mu = dL/dvarphi is IDENTICALLY "
      "ZERO for the shift-symmetric sector and equals -m^2 varphi once an explicit potential is "
      "added.  So breaking the symmetry is the one move that unlocks the charge -- which retro-"
      "explains why the IC route, the Phi^n response and the stage-4 suppressor all died: each tried "
      "to suppress a locally CONSERVED quantity by local means ***",
      "one structural statement covers three withdrawn mechanisms and names the fourth door")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- the equilibrium profile, in closed form")
print("=" * 100)
print("""
  Minimising E = int[Q_0 n + n^2/(2(mu^2+2A_s S))]dV + E_grav at fixed total charge gives
        n(r) = (mu^2 + 2 A_s S(r)) * (lambda - Q_0 - Phi(r)) ,   truncated where the bracket <= 0.
  BOTH factors rise toward the centre: -Phi is deepest there, and S is largest there BY DESIGN.
""")

lam_sym, Phi_sym = sp.symbols("lambda Phi", real=True)
n_eq = (mu_ ** 2 + 2 * As_ * S_) * (lam_sym - Q0_ - Phi_sym)
check(sp.simplify(sp.diff(n_eq, S_)) == 2 * As_ * (lam_sym - Q0_ - Phi_sym),
      "C1  dn/dS = 2 A_s (lambda - Q_0 - Phi) > 0 wherever the profile exists: *** the suppressor "
      "INCREASES the equilibrium charge density exactly where it is strongest ***",
      "the doubly-concentrating structure, read straight off the Euler-Lagrange solution")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- THE SELF-GRAVITATING SOLVE: a support mechanism STAGES 2-3 BOTH MISSED")
print("=" * 100)
print("""
  A first pass here used only the baryons' potential and returned a benign 0.015 dex -- WRONG,
  because it omitted the dust's own self-gravity, which is the whole problem.  Including it turns the
  system into a standard object, and doing so uncovers an error in stages 2 and 3 that runs IN THE
  THEORY'S FAVOUR:

     rho = Q_0 n  and  p = n^2/(2 mu^2)   =>   p = K rho^2 ,  K = 1/(2 Q_0^2 mu^2)
     so  c_s^2 = dp/drho = 2 K rho  --  the sound speed RISES WITH DENSITY.

  *** Stages 2 and 3 used the DBI background formula's MAXIMUM sound speed (0.385 Lam_D) and
  concluded "no support".  That was the wrong quantity: a self-gravitating cloud is supported by its
  LOCAL polytropic stiffness, which grows as it compresses.  p ~ rho^2 is an n = 1 polytrope, the
  same structure as a Bose star, and it HAS a finite-radius equilibrium. ***
""")
C_SI = mp.mpf("2.99792458e8")
G_SI = mp.mpf("6.674e-11")
PC_M = mp.mpf("3.086e16")
MSUN_KG = mp.mpf("1.989e30")
CS2_REC = mp.mpf("2.9e-8") * C_SI ** 2                     # banked anchor, in m^2/s^2
RHO_DM0_SI = mp.mpf("0.264") * mp.mpf("8.6e-27")
RHO_REC = RHO_DM0_SI * (1 + mp.mpf("1090")) ** 3
K_POLY = CS2_REC / (2 * RHO_REC)                            # from c_s^2 = 2 K rho at recombination
R_POLY = mp.pi * mp.sqrt(K_POLY / (2 * mp.pi * G_SI))       # n=1 Lane-Emden, xi_1 = pi

check(abs(mp.log(R_POLY / PC_M / mp.mpf("104.5"), 10)) < mp.mpf("0.02"),
      f"D1  *** THE EQUILIBRIUM EXISTS AND IS MASS-INDEPENDENT: the n = 1 polytrope radius is "
      f"R = pi sqrt(K/2 pi G) = {sig(R_POLY/PC_M,4)} pc, independent of how much dust it holds "
      "(the n = 1 exponent cancels the central density).  So stages 2-3's 'nothing stops it' was "
      "too strong -- polytropic stiffening does ***",
      f"K = {sig(K_POLY,4)} SI, anchored to the banked c_s^2(recombination)")

# D2 -- but does that equilibrium lie inside the DBI's validity?  Saturation caps the stiffening.
M_D_KG = M_DUST * MSUN_KG
rho_core = M_D_KG / (mp.mpf(4) / 3 * mp.pi * R_POLY ** 3)
RHO_SAT = mp.mpf("1.09e12") * RHO_DM0_SI                    # stage 1, at Lam_D = 8.4e-7 (the ceiling)
check(rho_core > RHO_SAT,
      f"D2  *** AND THE EQUILIBRIUM IS OUT OF REACH: that core's mean density is "
      f"{sig(rho_core/RHO_DM0_SI,4)} rho_dm0, which EXCEEDS the DBI saturation density "
      f"{sig(RHO_SAT/RHO_DM0_SI,4)} rho_dm0 by {sig(rho_core/RHO_SAT,4)}x.  Past saturation the DBI "
      "sound speed FALLS to zero (stage 3 Part B), so the stiffening that would have supported the "
      "core switches off before the core can form ***",
      "the polytropic support is real but is cut off by the theory's own cap -- so stage 3's "
      "black-hole endpoint stands, now by a longer and better-understood route")

# D3 -- and even if the 105 pc core DID form, the Galactic Centre excludes it.
MW_ENCL_100PC = mp.mpf("1e9")            # ~enclosed mass within ~100 pc of the Galactic Centre, Msun
check(M_DUST / MW_ENCL_100PC > 100,
      f"D3  and the escape is closed on the other side too: even if the {sig(R_POLY/PC_M,3)} pc core "
      f"did form, it would hold {sig(M_DUST,3)} Msun where the Galaxy is measured to hold "
      f"~{sig(MW_ENCL_100PC,2)} Msun -- {sig(M_DUST/MW_ENCL_100PC,4)}x too much",
      "so both branches of D2 fail, which is why the verdict does not hinge on the saturation call")

# D4 -- the suppressor's effect on the polytrope, for consistency with Parts A and C.
K_supp = K_POLY * MU2 / (MU2 + 2 * A_S)
R_supp = mp.pi * mp.sqrt(K_supp / (2 * mp.pi * G_SI))
check(R_supp < R_POLY,
      f"D4  and the stage-4 suppressor makes it WORSE, consistently with Parts A and C: it enters K "
      f"as 1/(mu^2 + 2 A_s S), shrinking the equilibrium radius from {sig(R_POLY/PC_M,4)} pc to "
      f"{sig(R_supp/PC_M,4)} pc -- a denser, more compact core",
      f"a factor {sig(R_POLY/R_supp,3)} smaller, i.e. {sig((R_POLY/R_supp)**3,3)}x denser")

# NC-D (negative control): the radius formula must respond to K as sqrt(K), or D1/D4 are not
# measuring anything -- and a K large enough must give a kpc-scale core.
K_big = K_POLY * mp.mpf("1e4")
R_big = mp.pi * mp.sqrt(K_big / (2 * mp.pi * G_SI))
check(abs(R_big / R_POLY - 100) < mp.mpf("0.01") and R_big > mp.mpf("10") * mp.mpf("3.086e19"),
      f"NC-D  CONTROL: the solver scales exactly as sqrt(K) (1e4 in K gives 100x in R) and a "
      f"sufficiently stiff sector WOULD give a {sig(R_big/PC_M/1000,3)} kpc core -- so D1-D4 are "
      "measurements of this theory's stiffness, not artefacts of the formula",
      "the favourable outcome is reachable in principle; this K does not reach it")

# =============================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  *** THE STAGE-4 SUPPRESSOR IS DEAD, AND IT WAS DEAD ON ARRIVAL FOR A REASON I MISSED. ***

  1. THE OBSERVABLE IS THE CONSERVED CHARGE, NOT THE FIELD AMPLITUDE.  Exactly:
     rho = Q_0 n with n = (mu^2 + 2 A_s S)u.  Every stage-4 gate tested u and every one of them was
     right about u -- and irrelevant, because rho tracks n.

  2. THEOREM (Part B): rho/n = Q_0 independently of A_s and S.  *** NO Y-dependent Q-mass, of any
     shape or amplitude, can change the dust mass a galaxy carries. ***  The mechanism could not have
     worked, and the eight gates it passed were measuring the wrong quantity.

  3. AND THE SIGN IS BACKWARDS.  At fixed charge the field energy is n^2/(2(mu^2+2A_s S)), which
     DECREASES as the suppressor strengthens -- so high-acceleration regions become CHEAPER places to
     keep charge.  The equilibrium profile, in closed form, is
     n(r) = (mu^2 + 2 A_s S(r))(lambda - Q_0 - Phi(r)): BOTH factors rise inward, so the suppressor
     makes the concentration WORSE.

  4. AND THE SOLVE CORRECTED STAGES 2-3 ALONG THE WAY, in the theory's favour: the dust is an
     n = 1 POLYTROPE (p = K rho^2, c_s^2 = 2K rho RISING with density), so polytropic stiffening
     really does provide support -- stages 2-3 used the DBI background MAXIMUM sound speed and
     wrongly concluded "nothing stops it".  The equilibrium is a MASS-INDEPENDENT
     {sig(R_POLY/PC_M,4)} pc core.  But it is out of reach: its density exceeds the DBI saturation
     density by {sig(rho_core/RHO_SAT,3)}x, where the sound speed falls to zero -- so the support
     switches off before the core forms, and stage 3's endpoint stands by a longer route.  Even if it
     DID form, {sig(M_DUST,3)} Msun inside {sig(R_POLY/PC_M,3)} pc is {sig(M_DUST/mp.mpf('1e9'),3)}x the
     measured Galactic-Centre mass.  Both branches fail, so the verdict does not hinge on the call.

  5. *** WHAT THIS BUYS, AND IT IS THE MOST USEFUL THING IN THE SEQUENCE: ONE STRUCTURAL STATEMENT
     NOW EXPLAINS EVERY FAILED ATTEMPT.  The dust mass IS the conserved shift charge times Q_0.  A
     conserved charge cannot be suppressed locally -- only MOVED (and gravity moves it inward), or
     NOT CONSERVED.  The IC route, the Phi^n response and this suppressor all tried to suppress a
     conserved quantity by local means, which is why all three died. ***

  6. THE ONLY DOOR LEFT IS THEREFORE SHARP AND NAMED: *** BREAK THE SHIFT SYMMETRY. ***  And its
     price is already on the books -- shift symmetry is what makes the excitation behave as DUST
     (rho ~ a^-3 from charge conservation) and what protects the sector's structure; breaking it
     generically reintroduces a potential, endangering w = -1 at the condensate minimum and the
     dust scaling that the CMB requires.  That is the next calculation, and unlike this one it is a
     THEORY-CONSTRUCTION problem rather than a solve.  I am not going to guess its outcome.

  Non-claim 2d stands where stage 3 left it: FALSIFIED within the theory as written, now with the
  repair space narrowed to one structural move whose costs are known in advance.
""")

if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED (incl. 2 negative controls)")
sys.exit(0)
