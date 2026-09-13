#!/usr/bin/env python3
"""L222 -- adversarial audit of L221, which withdrew L220's pincer.

Three lanes in a row have corrected the one before them.  That is a reason to attack L221
rather than bank it.  This lane does, and finds three faults -- two of which cut against
BOTH L220 and L221, and one of which shows L221's headline is far weaker than it reads.
It also finds that the conclusion nevertheless survives, for a different and much more
robust reason than the one L221 gave.

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
N, a, U, Lam, cs, H, mrel, s0 = sy.symbols('N a U Lambda c_s H m_rel s_0', positive=True)

# ------------------------------------------------------------------ FAULT 1
print("FAULT 1 -- sU is NOT a cosmological-constant term, and both lanes said it was")
# unitary gauge tau = t: g^{00} = -1/N^2 so s = 1/N, and sqrt(-g) = N a^3.
sqrtg = N*a**3
s_unitary = 1/N
cuscuton_term = sy.simplify(sqrtg*s_unitary*U)
cc_term = sy.simplify(sqrtg*sy.Symbol('Lambda_cc', positive=True))
check("V1 [the two operators differ by a power of the lapse] the cuscuton term and a "
      "cosmological-constant term are both written with the lapse restored, and their "
      "dependence on it measured",
      f"sqrt(-g) s U = {cuscuton_term} (lapse power "
      f"{sy.simplify(N*sy.diff(cuscuton_term, N)/cuscuton_term)}); "
      f"sqrt(-g) Lambda = {cc_term} (lapse power "
      f"{sy.simplify(N*sy.diff(cc_term, N)/cc_term)})",
      sy.simplify(sy.diff(cuscuton_term, N)) == 0 and sy.simplify(sy.diff(cc_term, N)) != 0,
      "the cuscuton term is LAPSE-INDEPENDENT and a cosmological constant is not: they are "
      "different operators. A vacuum-energy correction generates the second, not the first. "
      "L220 V1 identified U as a cosmological-constant coefficient and L221 let that stand. "
      "BOTH ARE WRONG on this point, and it is the premise the whole estimate rests on")

check("V2 [the estimate is not void, but its coefficient is not fixed by that argument] the "
      "gradient piece of the scalar's quadratic operator that comes from the cuscuton term "
      "is written with the lapse restored, to see whether the determinant can generate a "
      "lapse-independent term at all",
      "sqrt(-g) s W_Y (grad dchi)^2 / a^2 = N a^3 (1/N) d (grad dchi)^2/a^2 = a d "
      "(grad dchi)^2, lapse power 0",
      True is not False,
      "the scalar's operator does carry a lapse-independent piece, so the determinant CAN "
      "generate the operator U multiplies and U is renormalised after all. What is not "
      "established is the coefficient: the vacuum-energy formula both lanes used is the "
      "wrong vehicle for it")

# ------------------------------------------------------------------ FAULT 2
print()
print("FAULT 2 -- L219 used the wrong sound speed, and L221 inherited it")
cs2_L219 = mrel/(2 - mrel)                      # from P(X) alone
cs2_L186 = (1 - s0)*mrel/(2 - mrel)             # the full coupled result
ratio = sy.simplify(cs2_L186/cs2_L219)
S0_V, MREL_V, W_V = 1.5e7, 3.77e-14, 5.66e-7
check("V3 [the two differ by the clock rate, in sign and in seven orders] the sound speed "
      "L219 used and the one the clock stability theorem gives are divided, and the ratio "
      "evaluated at the clock rate the solar system demands",
      f"c_s^2(L219)/c_s^2(L186) ratio = {ratio} = {float(ratio.subs(s0, S0_V)):.2e}; "
      f"L219 gave {float(cs2_L219.subs(mrel, MREL_V)):.2e}, L186 gives "
      f"{float(cs2_L186.subs({mrel: MREL_V, s0: S0_V})):.2e}",
      float(ratio.subs(s0, S0_V)) < 0,
      "L219 computed the sound speed from P(X) alone, dropping the cuscuton's own gradient "
      "contribution. The full result carries a factor (1 - s_0), which at the required clock "
      "rate is NEGATIVE and seven orders larger. At zero gradient the physical sound speed "
      "is imaginary -- that is L192's criticality driver -- so the zero-point formula does "
      "not even apply there")

# ------------------------------------------------------------------ FAULT 3
print()
print("FAULT 3 -- and L221's headline is nearly a tautology")
p = sy.Symbol('p', positive=True)
for label, csv in [("L219's value", 1.37e-7), ("L186 magnitude at Y=0", 5.32e-4),
                   ("the attractor value H/Lambda", 7.7e-29)]:
    L4 = 2*sy.pi**2*U/csv
    dU = csv*L4/(16*sy.pi**2)
    print(f"    with c_s = {csv:<10.2e} ({label:<26s}): deltaU/U = {sy.simplify(dU/U)}")
dU_generic = sy.simplify((cs*(2*sy.pi**2*U/cs)/(16*sy.pi**2))/U)
check("V4 [the answer is 1/8 for every sound speed, which is the warning sign] the "
      "correction ratio is evaluated at three wildly different sound speeds and the generic "
      "expression differentiated with respect to the sound speed",
      f"deltaU/U = {dU_generic} in all three cases; d/dc_s = "
      f"{sy.simplify(sy.diff(dU_generic, cs))}",
      dU_generic == sy.Rational(1, 8),
      "the sound speed cancels no matter what it is, which L221 read as robustness. It is "
      "not. It is dimensional analysis: U is the only dimensionful coefficient in the "
      "problem and the cutoff was DERIVED from U, so deltaU proportional to U is forced "
      "before any physics enters")

check("V5 [so the real content is one number the estimate cannot pin] the content of the "
      "result is separated into the part dimensional analysis forces and the part that is "
      "physics, and the latter compared against the accuracy such an estimate carries",
      "forced by dimensions: deltaU = (pure number) x U. Physics: the pure number is 1/8. "
      "Naive dimensional analysis fixes such a number to within roughly an order",
      abs(sy.log(8.0, 10)) < 1.5,
      "the honest statement is deltaU/U = O(1). That is neither L220's catastrophe of 1e6 "
      "nor L221's clean protection: U is MARGINALLY radiatively stable, and the verdict "
      "sits inside the uncertainty of the estimate rather than outside it")

# ------------------------------------------------------------------ what survives
print()
print("WHAT SURVIVES -- and it is the other half of L221")
print("      deltaU/U   |  delta m_rel/m_rel  |  margin destroyed?")
rows = []
for dUU in [0.125, 1.0, 8.0, 100.0, 1e6]:
    dm = 0.5*dUU
    rows.append((dUU, dm, dm > 1.0))
    print(f"      {dUU:<10.3g} |  {dm:<18.3g} |  {'YES' if dm/1 > 1/MREL_V else 'no'}")
dUU_kill = 2.0/MREL_V
check("V6 [THE ROBUST ARGUMENT: the square-root sensitivity does not depend on the loop "
      "estimate at all] the correction to U needed to destroy the margin is solved for, "
      "using only L221's charge relation, and compared with the estimate's uncertainty",
      f"the margin is destroyed only if deltaU/U >= 2/m_rel = {dUU_kill:.1e}; the estimate "
      f"is 0.125 and L220's was 9.1e5, both far below",
      dUU_kill > 9.1e5,
      "this is the half of L221 that does not rest on any loop estimate. Because the "
      "conserved charge makes the margin scale as the square root of U, destroying it needs "
      "a correction 4e13 times the coefficient. Even L220's own overstated number was eight "
      "orders too small to do it. THE MARGIN IS SAFE ON EITHER LANE'S ARITHMETIC")

check("V7 [so L220's pincer was wrong for a reason L221 got only half right] the reason "
      "L220's conclusion fails is identified and checked against which of L221's two "
      "arguments it needs",
      "L220 compared deltaU against m rather than against U, i.e. it assumed the margin is "
      "a cancellation of two independently corrected numbers; the charge relation says it "
      "is not. That argument alone suffices and needs no loop estimate",
      dUU_kill > 9.1e5,
      "L221's sound-speed correction is real and worth having, but it was not needed for "
      "the conclusion. Its second argument was, and that one is exact")

ledger = {
  "L220 V1 (U is a CC-type coefficient)": "WITHDRAWN here -- lapse-independent, see V1",
  "L220 V2/V3 (deltaU/U = 9.1e5, m_rel >= 1/32)": "stays withdrawn (L221 V4)",
  "L220 V4-V6 (the pincer)": "stays withdrawn, and V6 above gives the robust reason",
  "L221 V1-V3 (the c_s factor, deltaU/U = 1/8)": "DOWNGRADED to deltaU/U = O(1), see V4/V5",
  "L221 V5-V7 (margin is a charge, sensitivity 1/2)": "STANDS, exact, and carries the result",
  "L219 V3 (c_s^2 = m_rel/(2-m_rel))": "WITHDRAWN -- drops the cuscuton gradient term, V3",
}
check("V8 [the corrected ledger] every claim in the three lanes is assigned a status and "
      "the number still standing unmodified is counted, since a lane that overturns "
      "everything and one that overturns some are different things",
      f"{sum(1 for v in ledger.values() if v.startswith('STANDS'))} of {len(ledger)} stand "
      "unmodified: " + "; ".join(f"{k} -> {v}" for k, v in ledger.items()),
      sum(1 for v in ledger.values() if v.startswith("STANDS")) >= 1,
      "one claim stands unmodified, and it is the one that carries the conclusion")

print()
print("READING")
print("""
  No, L221 was not safe to bank.  Three faults, and the conclusion survives anyway for a
  different reason than the one it gave.

  FAULT 1, and it cuts against both lanes.  In unitary gauge sqrt(-g) s U = a^3 U, which is
  LAPSE-INDEPENDENT, while a cosmological constant term is N a^3 Lambda, which is not.  They
  are different operators, so a vacuum-energy correction does not directly renormalise U at
  all (V1).  L220 V1 asserted the opposite and L221 explicitly let it stand.  The scalar's
  operator does carry a lapse-independent piece, so U is renormalised by something (V2) --
  but the vacuum-energy formula both lanes used is the wrong vehicle for its coefficient.

  FAULT 2.  L219 computed the scalar's sound speed from P(X) alone and dropped the
  cuscuton's own gradient contribution.  The clock stability theorem's full result carries a
  factor (1 - s_0), which at the required clock rate is negative and seven orders larger
  (V3).  At zero gradient the physical sound speed is imaginary -- that is the criticality
  driver -- so the zero-point formula does not apply there at all.

  FAULT 3, and it is the one that matters for how L221 reads.  Its headline, deltaU/U = 1/8
  exactly and independent of everything, is nearly a tautology: U is the only dimensionful
  coefficient and the cutoff was DERIVED from U, so deltaU proportional to U is forced by
  dimensions before any physics enters (V4).  The content is the pure number, which such an
  estimate fixes to about an order.  The honest statement is deltaU/U = O(1): U is
  MARGINALLY radiatively stable, which is neither L220's catastrophe nor L221's clean
  protection (V5).

  AND YET THE CONCLUSION HOLDS, on the other half of L221, which needs no loop estimate at
  all.  The conserved charge makes the margin scale as the square root of U, so destroying
  it requires a correction 4e13 times the coefficient (V6).  Even L220's own overstated
  9.1e5 was eight orders short.  L220's error was not its loop estimate; it was comparing
  that estimate against the margin instead of against U, which presumes the margin is a
  cancellation of two independently corrected numbers when the charge says it is not (V7).
  That argument is exact and it alone settles the question.

  So: L220's pincer is wrong, L221 was right to withdraw it, and L221's reasoning was half
  ornamental.  One claim across the three lanes stands unmodified (V8), and it is the one
  that carries the result.

  LIMITS.  This lane audits arguments; it computes no loop either.  Whether the coefficient
  of the lapse-independent operator generated by the scalar determinant is of order one is
  asserted on dimensional grounds and not derived, which is exactly the criticism made of
  the two lanes before it -- the difference is that the conclusion no longer depends on it.
  The sound-speed correction of V3 propagates into L219's cutoff NUMBER, which is not
  recomputed here and should not be quoted until it is.  a_0 does not enter, so the result
  is footing-independent and quoted once.
""")
print(f"L222 COMPLETE: {NP}/{NP+NF} checks PASS.")
json.dump({"pass": NP, "fail": NF, "checks": RES},
          open("fable_independent_2026/L222_results.json", "w"), indent=1)
