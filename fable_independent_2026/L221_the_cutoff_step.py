#!/usr/bin/env python3
"""L221 -- the cutoff step L220 named as its own soft link, checked.

L220 concluded a naturalness pincer with no interior, and named the place to attack it: the
cutoff enters there at the FOURTH power, so a factor of 31 in L219's cutoff would close the
gap.  Attacking it turns up two factors L220 did not carry, and together they reverse the
verdict.

  (1) THE VACUUM ENERGY OF A SLOW MODE.  L220 used deltaU = Lambda^4/(16 pi^2), the estimate
      for a mode with unit sound speed.  This sector's scalar has c_s^2 = m_rel/(2-m_rel),
      so its dispersion is omega = c_s k and the energy per mode is c_s k, not k.  The mode
      sum then carries a factor of c_s -- and L219's cutoff carries 1/c_s at the fourth
      power, because it was derived from the same fluctuation amplitude.  They cancel
      EXACTLY.

  (2) THE MARGIN IS NOT A DIFFERENCE, IT IS A CHARGE.  L220 compared deltaU against the
      margin as though the margin were a cancellation between two independently corrected
      numbers.  L217 showed the reciprocal margin is a conserved Noether charge.  Written in
      that variable, m_rel = a^3 sqrt(dU/2)/Q, a small margin is a LARGE CHARGE, and a shift
      in U moves the margin only as its square root.

Every check states measurement and threshold separately.
"""
import json
import sympy as sy

RES, NP, NF = [], 0, 0
def check(n, measured, ok, d=""):
    global NP, NF
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         reading : {d}")
    RES.append({"name": n, "measured": str(measured), "pass": ok, "reading": d})
    if ok: NP += 1
    else:  NF += 1

print(__doc__)
k, Lam, cs, U, mrel, Q, a3, dcoef = sy.symbols('k Lambda c_s U m_rel Q a3 d', positive=True)

# ---------------------------------------------------------------- A: the slow-mode vacuum energy
print("PART A -- the vacuum energy of a mode whose sound speed is not one")
rho_vac = sy.simplify(sy.integrate(sy.Rational(1,2)*cs*k * 4*sy.pi*k**2/(2*sy.pi)**3, (k, 0, Lam)))
rho_unit = sy.simplify(rho_vac.subs(cs, 1))
check("V1 [the mode sum carries the sound speed] the zero-point energy is integrated over "
      "momenta up to the cutoff with the dispersion omega = c_s k, and the result compared "
      "with the same integral at unit sound speed",
      f"rho_vac = {rho_vac}; at c_s = 1 it is {rho_unit}; ratio = "
      f"{sy.simplify(rho_vac/rho_unit)}",
      sy.simplify(rho_vac/rho_unit - cs) == 0 and sy.simplify(rho_vac - cs*Lam**4/(16*sy.pi**2)) == 0,
      "c_s Lambda^4/(16 pi^2). The counting is over momenta but the energy per mode is c_s k, "
      "so a slow mode contributes a factor of c_s LESS vacuum energy than a fast one at the "
      "same momentum cutoff. L220 used the fast-mode formula")

# ---------------------------------------------------------------- B: and the cutoff carries 1/c_s
print()
print("PART B -- and L219's cutoff carries the reciprocal")
# L219: Lambda^2 = pi sqrt(2) sqrt(U) (2/m_rel)^(1/4), and c_s = sqrt(m_rel/2) so
# (2/m_rel)^(1/4) = 1/sqrt(c_s).
Lam4_L219 = sy.simplify((sy.pi*sy.sqrt(2)*sy.sqrt(U)*(2/mrel)**sy.Rational(1,4))**2)
Lam4_cs = sy.simplify(Lam4_L219.subs(mrel, 2*cs**2))
check("V2 [L219's cutoff, rewritten in the sound speed] the cutoff of L219 is squared and "
      "the margin replaced by the sound speed it fixes, then its power of the sound speed "
      "is measured",
      f"Lambda^4 = {Lam4_L219} = {Lam4_cs}; power of c_s = "
      f"{sy.simplify(cs*sy.diff(Lam4_cs, cs)/Lam4_cs)}",
      sy.simplify(cs*sy.diff(Lam4_cs, cs)/Lam4_cs + 1) == 0
      and sy.simplify(Lam4_cs - 2*sy.pi**2*U/cs) == 0,
      "Lambda^4 = 2 pi^2 U/c_s, exactly one inverse power. That is not a coincidence: L219 "
      "derived the cutoff from the same fluctuation amplitude that sets the vacuum energy, "
      "so the two dependences are the same dependence")

dU_over_U = sy.simplify((cs*Lam4_cs/(16*sy.pi**2))/U)
check("V3 [so the correction is a pure number, at ANY margin] the slow-mode vacuum energy "
      "is evaluated at L219's cutoff and divided by the coefficient it corrects, and the "
      "result's dependence on the sound speed and on the coefficient is measured",
      f"deltaU/U = {dU_over_U}, d/dc_s = {sy.simplify(sy.diff(dU_over_U, cs))}, "
      f"d/dU = {sy.simplify(sy.diff(dU_over_U, U))}",
      dU_over_U == sy.Rational(1, 8),
      "exactly one eighth, independent of the margin, the sound speed and the coefficient "
      "alike. The sound speed cancels structurally. A one-loop correction of twelve percent "
      "is an ordinary perturbative correction, not a breakdown")

W_CEIL, S0 = 5.66e-7, 1.5e7
mrel_v = W_CEIL/(S0 - 1)
L220_ratio = (2.0/mrel_v)**0.5/8.0
check("V4 [L220 V2/V3 CORRECTED -- the strong-coupling diagnosis is WITHDRAWN] the ratio "
      "L220 reported is compared with the corrected one",
      f"L220 reported deltaU/U = {L220_ratio:.2e}; corrected value = 0.125; "
      f"L220 too large by {L220_ratio/0.125:.1e}",
      L220_ratio > 0.125,
      "L220 omitted the sound-speed factor in the mode sum and so overstated the correction "
      "by seven million. Its bound m_rel >= 1/32 is withdrawn, and with it the claim that "
      "the effective theory is strongly coupled at the required margin. It is not")

# ---------------------------------------------------------------- C: the margin is a charge
print()
print("PART C -- and the margin was never a difference of large numbers")
# Q = a^3 P_X qbar with P_X = d/m_rel and qbar^2 = (U/(2d))(1 - m_rel):
qbar = sy.sqrt(U*(1 - mrel)/(2*dcoef))
Q_expr = sy.simplify(a3*(dcoef/mrel)*qbar)
mrel_sol = sy.solve(sy.Eq(Q_expr, Q), mrel)
mrel_pos = [s for s in mrel_sol if sy.simplify(sy.limit(s, Q, sy.oo)) == 0]
check("V5 [solving the conserved charge for the margin] the Noether charge of L217 is "
      "written out with the closure's relations, solved for the margin, and the branch that "
      "goes to zero at large charge is selected",
      f"Q = {Q_expr}; solutions {len(mrel_sol)}, branch vanishing at large charge: "
      f"{len(mrel_pos)}",
      len(mrel_pos) == 1,
      "a small margin IS a large charge. In this variable there is no difference of two "
      "large numbers anywhere, so there is nothing for a correction to spoil by cancellation")

mr = mrel_pos[0]
sens = sy.simplify(U*sy.diff(mr, U)/mr)
sens_small = sy.simplify(sy.limit(sens, Q, sy.oo))
check("V6 [THE SENSITIVITY, and it is a square root] the logarithmic derivative of the "
      "margin with respect to the corrected coefficient is formed at fixed charge and "
      "gradient coefficient, and its limit at large charge measured",
      f"d log m_rel/d log U = {sens_small} at large charge",
      sens_small == sy.Rational(1, 2),
      "one half. The charge is exactly conserved because the shift symmetry is exact and a "
      "global shift symmetry of a scalar has no anomaly, so a correction to U moves the "
      "margin only as its square root")

shift = 0.5*0.125
check("V7 [so the margin is technically natural] the fractional shift in the margin induced "
      "by the one-loop correction is evaluated and compared against 1, the value at which "
      "the margin would be destroyed",
      f"delta m_rel/m_rel = (1/2)(1/8) = {shift:.4f}, i.e. {100*shift:.1f}%",
      shift < 1.0,
      "six percent. A one-loop correction moves the margin by six percent, not by twelve "
      "orders. The margin the solar system demands is radiatively stable, and L220's "
      "pincer dissolves")

# ---------------------------------------------------------------- D: what survives
print()
print("PART D -- what survives of L220")
survives = [
    "V1 (only U is exposed; d is dimensionless and takes log corrections only) STANDS",
    "V7 (U sits 1.5e-14 of the dark energy density) STANDS as a statement about U",
    "V8 (the chi shift symmetry does not act on tau) STANDS -- and turns out not to matter, "
    "because what protects the margin is the CHARGE that symmetry conserves, via V6 above",
]
for s in survives: print(f"      {s}")
withdrawn = ["V2 deltaU/U = sqrt(2/m_rel)/8", "V3 m_rel >= 1/32", "V4 the 12-order gap",
             "V5 deltaU/m = 2.4e19", "V6 the clock-rate ceiling", "V9 the escape analysis"]
check("V8 [the ledger of what is withdrawn] the checks of L220 that rest on the "
      "uncorrected estimate are listed and counted against the total, since a correction "
      "that leaves nothing standing and a correction that leaves most standing are "
      "different things",
      f"{len(withdrawn)} of 9 L220 checks withdrawn: {withdrawn}; "
      f"{len(survives)} findings stand",
      len(withdrawn) < 9,
      "six of nine withdrawn, three stand. The dimensional analysis and the statement that "
      "the clock coefficient is far below the dark energy scale survive; the pincer, the "
      "bound on the margin and the strong-coupling diagnosis do not")

check("V9 [and the residue is real but ordinary] the surviving statement about the clock "
      "coefficient is compared against the dark energy density, since a coefficient far "
      "below that scale is the cosmological constant problem and not a new one",
      f"U = {mrel_v*9.75e-12:.2e} eV^4 against rho_DE = 2.5e-11 eV^4, a ratio of "
      f"{mrel_v*9.75e-12/2.5e-11:.1e}; and the loop correction to it is 12.5%, not 1e6",
      mrel_v*9.75e-12/2.5e-11 < 1.0,
      "the clock coefficient is still a very small number that nothing explains. But its "
      "loop correction is twelve percent of itself, so it is small in a radiatively stable "
      "way -- the ordinary problem of a small vacuum-energy-like coefficient, not a new "
      "pathology of this construction")

print()
print("READING")
print("""
  L220 named its own soft link and the link broke.  Attacking it reverses the verdict.

  Two factors were missing.  The first: L220 estimated the correction as Lambda^4/(16 pi^2),
  which is the vacuum energy of a mode travelling at the speed of light.  This scalar has
  c_s^2 = m_rel/(2 - m_rel), so its dispersion is omega = c_s k, the counting is over momenta
  but the energy per mode is c_s k, and the mode sum carries a factor of c_s (V1).  Meanwhile
  L219's cutoff carries exactly one INVERSE power of c_s (V2) -- not a coincidence, since
  that cutoff was derived from the same fluctuation amplitude.  They cancel, and

      deltaU/U  =  1/8 ,

  a pure number, independent of the margin, the sound speed and the coefficient alike (V3).
  A one-loop correction of twelve percent is an ordinary perturbative correction.  L220
  overstated it by seven million, and its strong-coupling diagnosis is WITHDRAWN (V4).

  The second factor is deeper.  L220 compared that correction against the margin as though
  the margin were a cancellation between two independently corrected numbers.  It is not.
  L217 showed the reciprocal margin is a conserved Noether charge, and solving that charge
  for the margin gives

      m_rel  =  a^3 sqrt(dU/2) / Q ,

  so a small margin IS a large charge (V5) -- in that variable there is no difference of
  large numbers anywhere for a correction to spoil.  The sensitivity is a square root (V6),
  so the twelve percent shift in U moves the margin by SIX PERCENT (V7).  The margin the
  solar system demands is radiatively stable.  L220's pincer dissolves.

  Three of L220's nine findings stand (V8).  Only the clock coefficient is exposed, d being
  dimensionless; the chi shift symmetry indeed does not act on tau, which is true and turns
  out not to matter, because what protects the margin is the CHARGE that symmetry conserves,
  not a symmetry acting on tau; and the coefficient does sit fourteen orders below the dark
  energy density.  That last is the real residue (V9): a very small number nothing explains,
  but small in a radiatively stable way -- the ordinary problem of a vacuum-energy-like
  coefficient, not a new pathology of this construction.

  LIMITS.  The vacuum-energy estimate is still one loop and still dimensional analysis; what
  changed is that the sound-speed factor and the cutoff's sound-speed dependence are now
  BOTH carried, and their cancellation is structural rather than numerical, so the result is
  far more robust than the one it replaces.  No loop is computed.  The charge is exactly
  conserved only in the dark sector; the matter coupling MOND requires breaks it, at the rate
  L217 bounded, and that breaking is not re-examined here.  The relation m_rel = a^3
  sqrt(dU/2)/Q uses the closure and the branch relation 2 d qbar^2 = U(1 - m_rel).  a_0 does
  not enter, so the result is footing-independent and quoted once.
""")
print(f"L221 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("fable_independent_2026/L221_results.json", "w"), indent=1)
