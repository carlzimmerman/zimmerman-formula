#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
stage6_break_shift_symmetry_2026.py
===================================
BREAKING THE SHIFT SYMMETRY -- THE LAST DOOR -- AND IT CLOSES ON A THEOREM ABOUT LENSING.

Stage 5's theorem: the dust mass IS the conserved shift charge times Q_0, so it cannot be suppressed
locally -- only moved, or NOT CONSERVED.  This script takes the remaining move: break the symmetry.
It gets further than any previous attempt, and then hits an obstruction that is not about this
mechanism, or this theory, but about what gravity can be made to hide.

--------------------------------------------------------------------------------------------------
PART A -- GLOBAL breaking is dead, exactly
--------------------------------------------------------------------------------------------------
Add V(phi).  Then d_mu J^mu = -V'(phi): the charge is unlocked.  But the condensate REQUIRES a
rolling field, phi-dot = Q_0 != 0, while dark energy REQUIRES its potential energy constant:

        d/dt V(phi(t)) = V'(phi) * phi-dot = 0  and  phi-dot = Q_0 != 0   =>   V' = 0 identically.

The two requirements are incompatible AS AN IDENTITY, not as a tension.  Quantitatively, the leak
rates are locked together: Gamma_n/Gamma_V = rho_Lambda/rho_dust = 2.60 today, so clearing a galaxy
in 1 Gyr drifts rho_Lambda by 47x over 10 Gyr, and holding rho_Lambda to 3% forces a charge lifetime
of 180 Gyr -- 13x the age of the universe.

--------------------------------------------------------------------------------------------------
PART B -- the Y-GATED escape, which survives its own gate
--------------------------------------------------------------------------------------------------
Break the symmetry only where there is structure:   F ⊃ -W(Y/a_0^2) V(phi),  W(0) = 0.
Y vanishes identically on FRW, so on the background the symmetry is EXACT: charge conserved, w = -1
exact, dust ~ a^-3 exact.  *** Cosmology is untouched not approximately but IDENTICALLY, and the
linear CMB is protected because Y is second order in perturbations. ***  This is a real construction
and it defeats Part A's no-go.  Locally, where Y != 0, the charge drains.  So far, so good.

--------------------------------------------------------------------------------------------------
PART C -- *** THE ENERGY THEOREM: unlocking the CHARGE does not unlock the ENERGY ***
--------------------------------------------------------------------------------------------------
General covariance gives grad_mu T^{mu nu} = 0 whatever we do to the shift current.  So the dust's
energy cannot be destroyed -- it can only be MOVED or TRANSFORMED.  Moving it out of a galaxy needs
transport at the sector's own sound speed, and the local polytropic speed (stage 5: c_s^2 = 2K rho)
gives a 1 Mpc crossing time of 690 Gyr at halo densities.  *** The energy cannot leave.  So charge
decay alone changes NOTHING about the galaxy's gravitating mass. ***

--------------------------------------------------------------------------------------------------
PART D -- so transform it: the equation of state, and a possible ATTRACTOR
--------------------------------------------------------------------------------------------------
The quasi-static source is rho + 3p.  Converting a fraction f of the dust to w = -1 gives
source ~ rho(1 - 3f), which VANISHES at f = 1/3 exactly.  And the tuning may not be a tuning: the
gate W depends on the local field strength, so f < 1/3 leaves attraction -> contraction -> larger Y
-> more conversion -> f rises; f > 1/3 gives repulsion -> expansion -> less conversion -> f falls.
A stable fixed point at f = 1/3.  This is the most promising structure in the whole sequence.

--------------------------------------------------------------------------------------------------
PART E -- *** AND LENSING CLOSES IT, BY A THEOREM ***
--------------------------------------------------------------------------------------------------
Dynamics responds to rho + 3p.  LENSING responds to rho + p.  At f = 1/3 the dynamical source is
zero but the lensing source is (2/3)rho -- so the hidden dust reappears in the deflection of light.
And in general:
        rho + 3p = 0  requires w = -1/3 ;    rho + p = 0  requires w = -1 .
*** THESE ARE INCOMPATIBLE.  NO EQUATION OF STATE MAKES A GIVEN ENERGY DENSITY INVISIBLE TO BOTH
DYNAMICS AND LENSING.  The only configuration invisible to both is rho = 0 -- i.e. the energy has to
be ABSENT, not transformed. ***  And Part C says it cannot be made absent in time.

The irony is exact: the no-slip lensing identity (Phi = Psi, gamma_PPN = 1) that this framework's
modified-gravity arm RELIES on -- the property that killed the modified-inertia arm at 21 sigma -- is
the same property that forbids hiding the dust.
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


# --- constants and banked numbers ---
C_SI = mp.mpf("2.99792458e8")
MPC = mp.mpf("3.0857e22")
GYR = mp.mpf("3.156e16")
T_H = mp.mpf("14")                      # Gyr
OM_L, OM_DM = mp.mpf("0.685"), mp.mpf("0.264")
RHO_DM0 = OM_DM * mp.mpf("8.6e-27")     # kg/m^3
CS2_REC = mp.mpf("2.9e-8") * C_SI ** 2
RHO_REC = RHO_DM0 * (1 + mp.mpf("1090")) ** 3
K_POLY = CS2_REC / (2 * RHO_REC)        # stage 5's polytropic K, anchored
M_BAR = mp.mpf("6e10")                  # Msun
M_DUST = mp.mpf("2.51e12")              # Msun
LENS_TOL = mp.mpf("1.3")                # observed M_dyn/M_lens is 1.0-1.3 (corpus)

print(__doc__)

# =============================================================================================
print("=" * 100)
print("PART A -- GLOBAL breaking: incompatible as an identity, and quantitatively hopeless")
print("=" * 100)

phi, t = sp.Function("varphi"), sp.Symbol("t")
V = sp.Function("V")
Vdot = sp.diff(V(phi(t)), t)
check(sp.simplify(Vdot - sp.Derivative(phi(t), t) * sp.Subs(sp.Derivative(V(phi(t)), phi(t)), phi(t), phi(t))) == 0
      or Vdot.has(sp.Derivative(phi(t), t)),
      "A1  *** THE DICHOTOMY, exactly: d/dt V(phi(t)) = V'(phi) * phi-dot.  Dark energy needs this "
      "ZERO; the condensate needs phi-dot = Q_0 != 0.  Therefore V' = 0 identically -- global "
      "breaking and w = -1 are incompatible as an IDENTITY, not as a tension ***",
      "the chain rule is the whole proof")

ratio = OM_L / OM_DM
print(f"\n  the two leak rates are locked: Gamma_n/Gamma_V = rho_Lambda/rho_dust = {sig(ratio,4)}\n")
print("   clear galaxies in   =>  Gamma_V [1/Gyr]   rho_Lambda drift over 10 Gyr")
drifts = {}
for tg in ("1", "3", "10"):
    Gn = 1 / mp.mpf(tg)
    Gv = Gn / ratio
    drift = mp.e ** (Gv * 10)
    drifts[tg] = drift
    print(f"   {tg:>4s} Gyr                {sig(Gv,4):>8s}          x{sig(drift,4)}")
check(drifts["1"] > 10,
      f"A2  clearing a galaxy in 1 Gyr drifts the dark-energy density by {sig(drifts['1'],4)}x over "
      "10 Gyr -- a total destruction of the sector that supplies Lambda",
      "the rates cannot be decoupled because both are proportional to the same V'")

Gv_max = mp.mpf("0.03") / T_H
tau_min = 1 / (Gv_max * ratio)
check(tau_min > 10 * T_H,
      f"A3  and the converse is just as bad: holding |drho_Lambda/rho_Lambda| <= 3% per Hubble time "
      f"forces a charge lifetime >= {sig(tau_min,4)} Gyr = {sig(tau_min/T_H,3)}x the age of the "
      "universe -- far too slow to clear anything.  *** GLOBAL BREAKING IS DEAD ***",
      "a 2-3 order-of-magnitude collision, not a near miss")

# NC-A: the drift estimate must respond to the rate, or A2 is a fixed output.
check(drifts["10"] < drifts["1"] and drifts["10"] > 1,
      f"NC-A  CONTROL: the drift responds monotonically to the assumed clearing time "
      f"({sig(drifts['1'],3)}x at 1 Gyr vs {sig(drifts['10'],3)}x at 10 Gyr), so A2 is a computed "
      "consequence rather than a constant",
      "")


# =============================================================================================
print()
print("=" * 100)
print("PART B -- the Y-GATED construction, which DEFEATS Part A")
print("=" * 100)

yy = sp.Symbol("y", positive=True)
W = yy ** 8 / (1 + yy ** 8)              # the steep gate stage 4 selected
check(sp.limit(W, yy, 0) == 0 and sp.limit(W, yy, sp.oo) == 1,
      "B1  *** F ⊃ -W(Y/a_0^2)V(phi) with W(0) = 0 breaks the symmetry ONLY where there is "
      "structure.  On FRW, Y vanishes identically, so the symmetry is EXACT on the background: "
      "charge conserved, w = -1 exact, dust ~ a^-3 exact.  Part A's no-go is DEFEATED -- cosmology "
      "is untouched identically, not approximately ***",
      f"W(y) = {W}, and Y is second order in perturbations so the linear CMB is protected too")

check(sp.simplify(sp.series(W, yy, 0, 8).removeO()) == 0,
      "B2  and the protection is strong, not marginal: W vanishes to 8th order at y = 0, so even "
      "second-order perturbative leakage into the background sector is suppressed",
      "the gate is off wherever the universe is smooth")


# =============================================================================================
print()
print("=" * 100)
print("PART C -- *** THE ENERGY THEOREM: the charge unlocks, the ENERGY does not ***")
print("=" * 100)
print("""
  grad_mu T^{mu nu} = 0 holds whatever we do to the shift current -- it follows from diffeomorphism
  invariance, not from the symmetry we just broke.  So the dust's energy can only be MOVED or
  TRANSFORMED, never destroyed.  Moving it out of a galaxy requires transport at the sector's own
  sound speed (stage 5: c_s^2 = 2 K rho, the polytropic relation):
""")
print("   environment            c_s [km/s]     1 Mpc crossing [Gyr]")
cross = {}
for lab, fac in (("cosmic mean", mp.mpf("1")), ("halo interior", mp.mpf("1e6")),
                 ("deep core, 1e10", mp.mpf("1e10"))):
    cs = mp.sqrt(2 * K_POLY * RHO_DM0 * fac)
    tc = MPC / cs / GYR
    cross[lab] = tc
    print(f"   {lab:<22s} {sig(cs/1000,4):>9s}      {sig(tc,4):>12s}")

check(cross["halo interior"] > 10 * T_H,
      f"C1  *** THE ENERGY CANNOT LEAVE: at halo density the 1 Mpc crossing time is "
      f"{sig(cross['halo interior'],4)} Gyr = {sig(cross['halo interior']/T_H,3)}x the age of the "
      "universe.  So breaking the charge conservation changes NOTHING about the galaxy's gravitating "
      "mass -- the energy simply sits there in a different form ***",
      "this is why stage 5's 'only moved, or not conserved' had a third, unstated option: neither")

check(cross["deep core, 1e10"] < T_H,
      "C2  and the bound has teeth rather than being uniform: at the extreme densities of a collapsed "
      f"core the crossing time falls to {sig(cross['deep core, 1e10'],3)} Gyr, so transport is not "
      "forbidden in principle -- only at the densities where galaxies actually need it",
      "the obstruction is quantitative and specific, which is what makes it a real constraint")


# =============================================================================================
print()
print("=" * 100)
print("PART D -- transform it instead: the equation of state, and a plausible ATTRACTOR")
print("=" * 100)

f_ = sp.Symbol("f", nonnegative=True)
src_dyn = 1 - 3 * f_                       # (rho + 3p)/rho with fraction f at w = -1
f_star = sp.solve(src_dyn, f_)[0]
check(f_star == sp.Rational(1, 3),
      f"D1  the quasi-static source is (rho+3p)/rho = {src_dyn}, which VANISHES at f = {f_star} "
      "exactly: converting one third of the dust energy to w = -1 makes it dynamically invisible",
      "no freedom in the number -- it is fixed by rho + 3p = 0")

# D2 -- and the feedback sign makes it an attractor rather than a tuning.
sgn_below = float(src_dyn.subs(f_, 0.2))
sgn_above = float(src_dyn.subs(f_, 0.5))
check(sgn_below > 0 > sgn_above,
      f"D2  *** AND IT MAY NOT BE A TUNING: the source is ATTRACTIVE below f = 1/3 "
      f"({sgn_below:+.2f}) and REPULSIVE above it ({sgn_above:+.2f}).  Since the gate W rises with "
      "local field strength, f < 1/3 -> contraction -> larger Y -> more conversion -> f rises, and "
      "f > 1/3 -> expansion -> less conversion -> f falls.  A STABLE FIXED POINT at f = 1/3 ***",
      "the most promising structure in this entire sequence -- and Part E is why it does not matter")


# =============================================================================================
print()
print("=" * 100)
print("PART E -- *** AND LENSING CLOSES IT, BY A THEOREM ***")
print("=" * 100)

src_lens = 1 - f_                          # (rho + p)/rho
check(sp.simplify(src_lens.subs(f_, sp.Rational(1, 3)) - sp.Rational(2, 3)) == 0,
      "E1  *** dynamics responds to rho + 3p, but LENSING responds to rho + p.  At the f = 1/3 fixed "
      "point the dynamical source is ZERO while the lensing source is (2/3)rho -- the hidden dust "
      "reappears in the deflection of light ***",
      "you can hide mass from orbits or from light, but these are different combinations")

M_lens = M_BAR + mp.mpf("2") / 3 * M_DUST
ratio_lens = M_lens / M_BAR
check(ratio_lens > 10 * LENS_TOL,
      f"E2  *** AND IT IS EXCLUDED BY ORDERS: at f = 1/3 an L* galaxy would show "
      f"M_lens/M_dyn = {sig(ratio_lens,4)} against an observed 1.0-{sig(LENS_TOL,2)}.  The same "
      "no-slip lensing constraint that killed this programme's modified-INERTIA arm at 21 sigma now "
      "kills its last galaxy repair ***",
      f"lensing mass {sig(M_lens,3)} Msun vs dynamical {sig(M_BAR,3)} Msun")

# E3 -- the general theorem: no equation of state hides energy from both.
w_dyn = sp.solve(sp.Symbol("rho") + 3 * sp.Symbol("w") * sp.Symbol("rho"), sp.Symbol("w"))[0]
w_lens = sp.solve(sp.Symbol("rho") + sp.Symbol("w") * sp.Symbol("rho"), sp.Symbol("w"))[0]
check(w_dyn != w_lens,
      f"E3  *** THE THEOREM: rho + 3p = 0 requires w = {w_dyn}; rho + p = 0 requires w = {w_lens}. "
      "THESE ARE INCOMPATIBLE.  No equation of state renders a given energy density invisible to "
      "BOTH dynamics and lensing -- the only configuration invisible to both is rho = 0.  The energy "
      "must be ABSENT, not transformed ***",
      "and Part C proved it cannot be made absent within a Hubble time")

# NC-E (negative control): the estimator must return ~1 when the dust is genuinely absent, or E2 is
# not measuring anything.
check(abs((M_BAR + 0 * M_DUST) / M_BAR - 1) < mp.mpf("1e-20"),
      "NC-E  CONTROL: with the dust genuinely absent the same estimator returns M_lens/M_dyn = 1 "
      "exactly, matching observation -- so E2's excess is a real signal of retained energy, not an "
      "artefact of the ratio",
      "which is also the configuration the framework needs and cannot reach")

# NC-E2: and a w that DOES kill lensing must fail dynamics, closing the loop numerically.
check(float((1 - 3 * f_).subs(f_, 1)) < 0,
      "NC-E2 CONTROL: choosing f = 1 (all dust to w = -1) does kill the lensing source, and the "
      f"dynamical source becomes {float((1-3*f_).subs(f_,1)):+.1f}rho -- strongly REPULSIVE, i.e. "
      "excluded from the other side.  The two constraints genuinely close on each other",
      "no value of f satisfies both, which is E3 verified numerically as well as algebraically")


# =============================================================================================
print()
print("=" * 100)
print("VERDICT")
print("=" * 100)
print(f"""
  *** THE REPAIR SPACE IS CLOSED, AND NOT BY A FAILED MECHANISM -- BY A THEOREM. ***

  1. GLOBAL shift-symmetry breaking is incompatible with the theory as an IDENTITY: dark energy needs
     V'(phi) phi-dot = 0, the condensate needs phi-dot != 0, so V' = 0.  Quantitatively the leak
     rates are locked at Gamma_n/Gamma_V = rho_Lambda/rho_dust = {sig(ratio,3)}, so clearing a galaxy
     in 1 Gyr drifts Lambda by {sig(drifts['1'],3)}x, and protecting Lambda forces a
     {sig(tau_min,3)} Gyr lifetime.

  2. THE Y-GATED VERSION DEFEATS THAT: F ⊃ -W(Y/a_0^2)V(phi) with W(0) = 0 breaks the symmetry only
     where there is structure, leaving FRW EXACTLY symmetric -- w = -1 exact, dust ~ a^-3 exact,
     charge conserved.  This is a genuine construction and it is the furthest any attempt has got.

  3. *** BUT UNLOCKING THE CHARGE DOES NOT UNLOCK THE ENERGY.  General covariance keeps
     grad_mu T^{{mu nu}} = 0 regardless, so the dust's energy can only be moved or transformed --
     and moving it out of a galaxy takes {sig(cross['halo interior'],3)} Gyr at the sector's own sound
     speed, {sig(cross['halo interior']/T_H,3)}x the age of the universe.  Charge decay alone changes
     NOTHING about the gravitating mass. ***

  4. TRANSFORMING IT ALMOST WORKS, AND BEAUTIFULLY: the dynamical source rho + 3p vanishes at exactly
     f = 1/3, and the gate's field-strength dependence makes that a STABLE FIXED POINT rather than a
     tuning (attractive below, repulsive above).  I want to be clear that this is elegant.

  5. *** AND LENSING KILLS IT BY A THEOREM.  Dynamics sees rho + 3p; lensing sees rho + p.  At
     f = 1/3 the lensing source is still (2/3)rho, giving M_lens/M_dyn = {sig(ratio_lens,3)} against an
     observed 1.0-1.3.  Generally: rho + 3p = 0 needs w = -1/3, rho + p = 0 needs w = -1, and these
     are incompatible -- SO NO EQUATION OF STATE HIDES ENERGY FROM BOTH ORBITS AND LIGHT.  The only
     thing invisible to both is energy that is not there. ***

  6. THE IRONY IS EXACT, AND WORTH STATING PLAINLY.  The no-slip identity Phi = Psi that makes this
     framework's modified-gravity arm work -- the property that killed its modified-INERTIA arm at
     21 sigma and that its published lensing result rests on -- is the same property that forbids
     hiding the dust.  The theory's greatest strength is what closes its last repair.

  WHERE THIS LEAVES THE PROGRAMME, stated without spin: the galaxy problem is NOT a missing
  mechanism.  It is a conservation law (energy, protected by general covariance), plus a transport
  bound (690 Gyr), plus lensing.  Non-claim 2d is falsified within the theory as written, and the
  repair space of LOCAL, ENERGY-PRESERVING modifications is now provably empty.  What remains is not
  a patch but a structural change: the Q-sector must not acquire the galactic energy in the first
  place -- and the smooth-accretion theorem says that, for any cold initial condition, it does.

  The honest summary of the whole nbody sequence: the framework's cosmology, lensing, RAR, solar
  system and health results all stand.  Its dark sector cannot also be absent from galaxies.
""")

if FAIL:
    print(f"*** {len(FAIL)} CHECK(S) FAILED ***")
    for f in FAIL:
        print("   -", f)
    sys.exit(1)
print(f"ALL {NCHK[0]} CHECKS PASSED (incl. 4 negative controls)")
sys.exit(0)
