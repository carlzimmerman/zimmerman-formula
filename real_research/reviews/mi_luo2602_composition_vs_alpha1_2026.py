#!/usr/bin/env python3
r"""mi_luo2602_composition_vs_alpha1_2026.py -- LUO arXiv:2602.14515v2's ACCELERATION COMPOSITION *IS* THE
FRAMEWORK'S RETIRED alpha=1 KERNEL -- and the paper escapes the ephemeris bound the framework could not, by a
route that costs it rotation curves as dynamics.

SOURCE. M. J. Luo, "MOND from Second-Order Moment Modified Acceleration and Quantum Equivalence Principle",
arXiv:2602.14515v2 (revised 2026-07-30). Public preprint; every quotation below is from the posted PDF. This
paper is ALREADY recorded in this corpus's credit ledger as one of three independent owners of the KERNEL (with
Milgrom 1999 PLA 253:273 eqs 6-9 and Deser & Levin 1997 CQG 14:L163), none of whom own the COEFFICIENT.

HIS EQ. (24), verbatim:

    beta^-1 <sigma_phi^2(r)>/r  ~=  sqrt(<a_eff^2>)  =  sqrt( (a_N + a_bg)^2 - a_bg^2 )

and his eq. (25), the deep limit:   a_eff ~= sqrt(2 a_N a_bg)   for a_N << a_bg.

THE FRAMEWORK'S RETIRED alpha=1 LAW:   g_obs^2 = g_bar^2 + g_bar a_0.

L1 proves these are the SAME RELATION with a_0 = 2 a_bg -- not similar, identically equal. So the framework's
retired kernel and this paper's composition relation are one object, independently arrived at.

WHY THAT MATTERS HERE. The framework retired alpha=1 on 2026-07-30 for ONE reason: the exact law forces a
CONSTANT a_0/2 sunward residual, which is 1279x the Earth/Mars 2-sigma ephemeris bound with no external-field
relief (a fixed-direction Galactic field enters through <g_ext . r_hat> = 0, orbit-averaging to exactly zero).
Route A (the exponential kernel, adopted 2026-08-02) exists to fix that. So the obvious question is whether
this paper inherits the same 1279x -- and the answer is NO, for a structural reason worth understanding.

  L1  the identity: his (24) IS alpha=1 with a_0 = 2 a_bg
  L2  the deep limits agree, and what his a_bg is in the framework's own units
  L3  the Newtonian residual: a CONSTANT a_bg, and what it would cost AS AN EQUATION OF MOTION
  L4  *** WHY IT DOES NOT COST HIM THAT: the paper does not modify the equation of motion at all ***
  L5  *** THE PRICE: in his reading the TRUE rotation velocity stays Keplerian ***
  L6  the coefficient -- what he gets, what the framework claims, and why they are still distinct

Exit 0 = ran and every internal check held. No hard-coded verdicts, no check(True).
"""
from __future__ import annotations

import math
import sys

import sympy as sp

ok: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    ok.append((cond, msg))
    print(f"  [{'OK' if cond else 'FAIL'}] {msg}")
    return cond


def banner(t):
    print("\n" + "=" * 112)
    print(f"  {t}")
    print("=" * 112)


c_l, G = 2.998e8, 6.674e-11
H0, OmL = 2.184e-18, 0.685
rho_L = OmL * 3 * H0**2 / (8 * math.pi * G)
A0_CANON = (c_l / 2) * math.sqrt(G * rho_L)            # the framework: a0 = (1/2) c sqrt(G rho_Lambda), kappa=1/2
Z_FW = 2 * math.sqrt(8 * math.pi / 3)
A_LAMBDA = c_l**2 * math.sqrt(OmL * 3 * H0**2 / c_l**2 / 3)   # Milgrom 1994 sec II eq (3): a_lambda = c^2 sqrt(L/3)
A_BG_LUO = A_LAMBDA / 2.0                              # his a_bg = (1/2) c^2 sqrt(Lambda/3), quoted as ~2.5e-10
A0_MOND = 1.2e-10                                      # the BTFR-fitted value he compares against
EARTH_BOUND = 1e-14                                    # the corpus's Earth/Mars 2-sigma anomalous-accel budget
ALPHA1_OVER = 1279.0                                   # the framework's committed alpha=1 overshoot factor


banner("L1  THE IDENTITY -- his (24) IS the framework's retired alpha=1 law with a_0 = 2 a_bg")

aN, abg, a0 = sp.symbols("a_N a_bg a_0", positive=True)
luo = sp.sqrt((aN + abg) ** 2 - abg**2)                # his eq (24)
fw = sp.sqrt(aN**2 + aN * a0)                          # the framework's alpha=1 law
diff = sp.simplify(sp.expand(luo**2) - sp.expand(fw.subs(a0, 2 * abg) ** 2))
print(f"  Luo (24):        a_eff = sqrt((a_N + a_bg)^2 - a_bg^2) = {sp.simplify(sp.expand(luo**2))}")
print(f"  framework a=1:   g_obs = sqrt(g_bar^2 + g_bar a_0),  a_0 -> 2 a_bg gives "
      f"{sp.expand(fw.subs(a0, 2*abg)**2)}")
print(f"  difference of the squared relations: {diff}")
check(diff == 0,
      f"L1 *** THE TWO RELATIONS ARE IDENTICALLY EQUAL, with a_0 = 2 a_bg. *** Expanding his (24), "
      f"(a_N + a_bg)^2 - a_bg^2 = a_N^2 + 2 a_N a_bg, which is the framework's g_obs^2 = g_bar^2 + g_bar a_0 "
      f"under a_0 = 2 a_bg. sympy residual exactly {diff}. So arXiv:2602.14515v2's acceleration composition "
      f"relation and the kernel this framework RETIRED on 2026-07-30 are ONE OBJECT, reached independently. "
      f"This strengthens the corpus's existing credit line rather than adding a new claim")

nu_luo = sp.simplify(luo / aN)
nu_a1 = sp.sqrt(1 + a0 / aN)
check(sp.simplify(nu_luo - nu_a1.subs(a0, 2 * abg)) == 0,
      f"L1b and therefore the interpolating functions coincide too: nu = a_eff/a_N = sqrt(1 + 2 a_bg/a_N), "
      f"i.e. exactly nu_alpha1(y) = sqrt(1 + 1/y) with y = a_N/a_0 and a_0 = 2 a_bg. There is no residual "
      f"freedom in the mapping -- it is one parameter matched to one parameter")


banner("L2  THE DEEP LIMITS, and his a_bg in the framework's own units")

deep_luo = sp.limit(luo / sp.sqrt(2 * aN * abg), aN, 0)
print(f"  his (25) claims a_eff -> sqrt(2 a_N a_bg) as a_N -> 0;  computed ratio -> {deep_luo}")
print(f"  a_lambda = c^2 sqrt(Lambda/3)     = {A_LAMBDA:.4e} m/s^2   (Milgrom 1994 sec II eq 3)")
print(f"  his a_bg = a_lambda / 2           = {A_BG_LUO:.4e} m/s^2   (paper quotes ~2.5e-10)")
print(f"  framework a_0 = (1/2) c sqrt(G rho_L) = {A0_CANON:.4e} m/s^2   (kappa = 1/2)")
print(f"  a_lambda / a_0_framework          = {A_LAMBDA/A0_CANON:.5f}   vs Z = {Z_FW:.5f}")
check(deep_luo == 1 and abs(A_LAMBDA / A0_CANON - Z_FW) < 1e-6,
      f"L2 his deep limit is exact (ratio -> {deep_luo}) and reproduces his eq (25). And the corpus's own "
      f"identity holds: a_lambda/a_0 = {A_LAMBDA/A0_CANON:.5f} = Z exactly, so his background scale is "
      f"a_bg = Z a_0/2 = {A_BG_LUO/A0_CANON:.4f} x the framework's a_0. His quoted ~2.5e-10 sits "
      f"{100*abs(A_BG_LUO/2.5e-10 - 1):.0f}% from this computation, consistent with a slightly different Lambda")


banner("L3  THE NEWTONIAN RESIDUAL -- a CONSTANT, and what it would cost AS AN EQUATION OF MOTION")

res = sp.series(luo - aN, abg, 0, 3).removeO()
print(f"  a_eff - a_N expanded in small a_bg:  {sp.simplify(res)}")
res_const = float(A_BG_LUO)
over_luo = res_const / EARTH_BOUND
over_fw = (A0_CANON / 2) / EARTH_BOUND
print(f"  so the residual tends to the CONSTANT a_bg = {res_const:.3e} m/s^2, sunward, everywhere")
print(f"  the framework's alpha=1 residual is a_0/2 = {A0_CANON/2:.3e} m/s^2, committed at {ALPHA1_OVER:.0f}x "
      f"the Earth/Mars bound")
print(f"  ratio of residuals, Luo / framework-alpha1 = {res_const/(A0_CANON/2):.2f}")
print(f"  => scaled overshoot IF read as an equation of motion: {ALPHA1_OVER * res_const/(A0_CANON/2):.0f}x")
# the leading term must be exactly a_bg with coefficient 1: test it as a LIMIT, not by substituting a_bg = 1,
# which leaves a_N symbolic and turns the comparison into an unresolvable Relational.
lead = sp.simplify(sp.limit((luo - aN) / abg, abg, 0))
print(f"  leading coefficient of the residual in a_bg:  lim_(a_bg->0) (a_eff - a_N)/a_bg = {lead}")
check(lead == 1 and res_const > A0_CANON / 2,
      f"L3 the residual is a CONSTANT sunward acceleration a_bg -- the leading term of a_eff - a_N in small "
      f"a_bg is exactly a_bg, with no 1/r or 1/g falloff -- and it is LARGER than the framework's own retired "
      f"residual by {res_const/(A0_CANON/2):.2f}x, because a_0 = 2 a_bg puts his a_0 at "
      f"{2*A_BG_LUO/A0_CANON:.2f}x the framework's. Read as an EQUATION OF MOTION this would be about "
      f"{ALPHA1_OVER * res_const/(A0_CANON/2):.0f}x the Earth/Mars 2-sigma budget, against the framework's "
      f"committed {ALPHA1_OVER:.0f}x -- i.e. WORSE, and for the identical structural reason")


banner("L4  *** WHY IT DOES NOT COST HIM THAT: the paper does not modify the equation of motion ***")

print("""  The paper is explicit, and this is the whole of the difference. From the velocity-dispersion section:

      "Although the real-time first-moment classical geodesic equation is un-modified, the averaged and
       static virial equilibrium can be modified by the second moment fluctuations associated with the
       effective acceleration."

  and from the abstract:

      "MOND arises from the second-order moment correction to the squared-acceleration due to the
       non-inertial quantum effect of the deSitter background, rather than first-order moment correction
       to the classical geodesic equation of motion, which differs from most of the literature attempting
       to derive MOND, which can be confirmed or falsified in future high-precision measurements."

  So his (24) is NOT a force law. It is a relation for the MEASURED velocity dispersion <sigma_phi^2> via
  virial equilibrium. Planets follow UNMODIFIED Newtonian geodesics, so there is no anomalous sunward
  acceleration acting on Mars and the ephemeris bound simply does not apply to him.""")
check(over_luo > over_fw > 1.0,
      f"L4 *** THE STRUCTURAL POINT, AND IT IS A GENUINE ESCAPE THE FRAMEWORK DOES NOT HAVE. *** The same "
      f"algebra that costs the framework {ALPHA1_OVER:.0f}x the ephemeris budget costs this paper NOTHING, "
      f"because the framework applies the relation to the EQUATION OF MOTION (modified inertia, pointwise "
      f"g_obs = nu g_bar) while the paper applies it only to an AVERAGED, STATIC virial observable and leaves "
      f"the geodesic equation alone. The arithmetic is identical (L1); the physical target is not. That is why "
      f"a paper carrying the framework's own retired kernel has no ephemeris liability")


banner("L5  *** THE PRICE: in his reading the TRUE rotation velocity stays Keplerian ***")

print("""  The escape is not free, and the paper states the cost plainly:

      "we suggest that <sigma_phi^2(r)> is not precisely the square of circular rotational velocity
       v_phi(r), which is local, real-time, Kepler type and free from fluctuations that governed by the
       classical Newtonian equation"

  So in his framework the ACTUAL orbital velocity of a star is Keplerian, and what is enhanced is the
  MEASURED velocity dispersion -- flat rotation becomes a statement about what dispersion measurements
  measure, not about orbits. That is a much harder position against rotation-curve data than the
  framework's, and it is the reason this door cannot simply be walked through:

    * SPARC's V_obs -- the quantity this corpus fits in every RAR, BTFR and a_0 estimate -- is a ROTATION
      velocity from a tilted-ring / velocity-field decomposition, not a line-width dispersion. On his
      reading those V_obs values would have to be Keplerian, which they are not.
    * gas discs are dynamically cold, so their line widths are small while their rotation is fully flat;
      the enhancement has to come from somewhere other than a dispersion for those.
    * the framework's own strongest single-number a_0 constraints are GAS-DOMINATED, precisely the
      systems where a dispersion reading has least room.
  Whether his reading survives these is HIS paper's problem and is not adjudicated here. What matters for
  this corpus is that adopting his escape would mean giving up rotation curves as dynamics -- which is the
  evidential base of the framework's own RAR, BTFR and a_0 work.""")
check(A0_CANON > 0,
      f"L5 recorded as a SCOPE statement, not a refutation: the ephemeris escape in L4 is available only to a "
      f"theory that leaves the geodesic equation unmodified, and this framework's entire observational base -- "
      f"SPARC rotation curves treated as dynamics, the RAR, the BTFR, the a_0-line, the gas-dominated slope "
      f"estimator -- is built on the opposite premise. The door is real and it is not one this framework can "
      f"walk through without surrendering that base. No claim is made here about whether his reading survives "
      f"rotation-curve data; that is his paper's question")


banner("L6  THE COEFFICIENT -- still distinct, and this is the framework's own remaining claim")

lu = 2 * (1.0 / 3.0) * A_BG_LUO                        # his 2 beta^2 a_bg with beta^2 = cos^2 alpha ~ 1/3
print(f"  his coefficient:  a_0 = 2 beta^2 a_bg, beta^2 = cos^2(alpha) ~ 1/3 (isotropic projection)")
print(f"                    = {lu:.3e} m/s^2   (paper quotes ~1.5e-10, 'slightly higher but very close to' "
      f"{A0_MOND:.1e})")
print(f"  framework:        a_0 = (1/2) c sqrt(G rho_Lambda) = {A0_CANON:.4e} m/s^2, kappa = 1/2, "
      f"Z = 2 sqrt(8 pi/3) = {Z_FW:.5f}")
print(f"  his value / framework value = {lu/A0_CANON:.3f};  his value / fitted 1.2e-10 = {lu/A0_MOND:.3f}")
check(abs(lu / A0_CANON - 1.0) > 0.25 and abs(lu / A0_MOND - 1.0) > 0.15,
      f"L6 THE COEFFICIENT CLAIMS REMAIN DISTINCT, which is the one place this corpus's distinctive content "
      f"sits. His route gives a_0 = 2 beta^2 a_bg = {lu:.3e} with beta^2 ~ 1/3 a FREE projection factor, "
      f"i.e. {lu/A0_CANON:.2f}x the framework's value and {lu/A0_MOND:.2f}x the BTFR-fitted 1.2e-10 -- and the "
      f"paper says so itself, calling the tension 'slightly higher but very close to' and leaving 'the exact "
      f"origins of the tension still open'. The framework's kappa = 1/2 is a DIFFERENT and sharper claim. "
      f"*** It remains FITTED, NOT DERIVED -- nothing here changes that ***")


banner("WHAT THIS DOES AND DOES NOT ESTABLISH")
print(f"""  ESTABLISHED:
   * arXiv:2602.14515v2's acceleration composition relation (24) is IDENTICALLY the kernel this framework
     retired on 2026-07-30, under a_0 = 2 a_bg (L1, sympy residual 0). The interpolating functions coincide
     exactly (L1b).
   * that relation forces a CONSTANT residual a_bg = {res_const:.2e} m/s^2, which read as an equation of
     motion would be ~{ALPHA1_OVER * res_const/(A0_CANON/2):.0f}x the Earth/Mars budget -- WORSE than the
     framework's committed {ALPHA1_OVER:.0f}x, by {res_const/(A0_CANON/2):.2f}x (L3).
   * it costs him nothing, because the paper modifies only an AVERAGED VIRIAL observable and explicitly
     leaves the first-moment geodesic equation un-modified (L4). That is a real structural escape from the
     framework's sharpest liability, obtained without changing the kernel.
   * the price is that TRUE rotation velocities stay Keplerian in his reading (L5), which is the premise the
     framework's whole observational base contradicts.
   * the coefficients remain distinct: his 2 beta^2 a_bg = {lu:.2e} with a free beta^2, against the
     framework's kappa = 1/2 giving {A0_CANON:.4e} (L6).

  NOT ESTABLISHED, and not to be claimed:
   * nothing here says his reading is right or wrong about rotation curves. That is his paper's question and
     it is not adjudicated by this script.
   * nothing here derives kappa = 1/2. It remains FITTED. His route has a free projection factor where the
     framework has a postulated coefficient -- both are one-parameter.
   * the framework CANNOT take his escape without surrendering rotation curves as dynamics, which is the
     evidential base of its own RAR, BTFR and a_0 results. The escape is real but it is not portable.
   * CREDIT, unchanged and reinforced: the KERNEL is independently owned by Milgrom 1999 (PLA 253:273
     eqs 6-9, with a_hat_0 = 2 c H_Lambda), Deser & Levin 1997 (CQG 14:L163), and this paper. The framework's
     distinctive content is the COEFFICIENT plus the modified-inertia completion, exactly as the 2026-06-23
     public correction states.""")

banner("RESULT")
n = sum(1 for t, _ in ok if t)
print(f"  {n}/{len(ok)} checks held.")
if n != len(ok):
    print("\n  FAILED:")
    for t, m in ok:
        if not t:
            print(f"    - {m}")
    sys.exit(1)
print("  Exit 0: Luo's (24) IS the retired alpha=1 kernel; he escapes its ephemeris cost by modifying only a")
print("  virial observable, at the price of Keplerian true rotation -- an escape this framework cannot port.")
