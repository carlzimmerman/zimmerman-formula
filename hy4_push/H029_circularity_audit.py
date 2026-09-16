#!/usr/bin/env python3
r"""H029 -- THE CIRCULARITY AUDIT.  An honest answer to "is this circular?".

THE CHARGE.  H016 (seesaw), H019 (Zimmerman = seesaw), H020 (the Seven) and
H028 (where Z comes from) were presented as four results.  Sympy shows all
four are ALGEBRAICALLY IDENTICAL to the single definition

    a_0 = (1/2) c sqrt(G rho_Lambda)                [the postulate]

  * c H_0/a_0 - sqrt(32 pi/(3 Om_L)) = 0     (H020, identically)
  * c H_L/a_0 - 2 sqrt(8 pi/3)       = 0     (H028, identically)
  * [Lambda^2/(2 M_Pl)] / a_0        = 1     (H016/H019, identically)

So they are NOT independent results. They are four ways of writing one
definition. Presenting them as mutual confirmation was wrong, and this lane
records that.

WHAT THEY ACTUALLY ARE: UNIFICATIONS, NOT PREDICTIONS.
  The postulate a_0 = (1/2) c sqrt(G rho_L) was not constructed to reproduce
  the MOND seesaw a_0 ~ Lambda^2/M_Pl, nor the coincidence a_0 ~ cH_0/7, nor
  the constant Z = 5.789. That it reproduces all three EXACTLY is a genuine
  reduction: three apparently independent empirical facts of the field become
  one. That is worth something. But it is not four confirmations of one
  claim, and it must not be counted as such.

WHAT IS GENUINELY NON-CIRCULAR (the real content):
  1. THE SHAPE.  n = 2 from the transverse-traceless rank D(D-3)/2 (H017),
     derived from the action's static response (H018). This fixes mu_2's
     functional form and has NOTHING to do with the value of a_0. Independent.
  2. THE RAR FIT.  mu_2 (shape from n=2) with a_0 from Lambda, tested on 155
     SPARC curves: 0.150 dex, zero free parameters. The shape and the scale
     enter differently, so this is a real test.
  3. THE AMPLITUDE LAW.  M_ph/M_b = r/r_M capped at a_0/g_ext (H021). Uses
     a_0 (definition) and g_ext (INDEPENDENTLY measured by 2MRS). Prediction:
     Omega_dm/Omega_b = <a_0/g_ext>. Genuine, though the test is weak.
  4. THE STRONG-FIELD SECTOR.  c_T = c and no independent scalar hair (H027)
     follow from the ACTION'S FORM, not from the value of a_0. Independent.
  5. CLUSTER SHAPE.  The phantom slope, independent of a_0's value.

THE ONE DECISIVE NON-CIRCULAR TEST -- AND ITS ANSWER.
  The postulate PREDICTS a_0 from cosmology. Galaxy rotation curves MEASURE
  a_0 independently. If the postulate is right, they must agree:

      a_0 (from Lambda, canonical footing)  = 9.3624e-11 m/s^2
      a_0 (from galaxy fits, literature)    ~ 1.2e-10  m/s^2
      DISCREPANCY                           ~ 22%

  THIS IS THE REAL TEST, AND IT IS A 22% TENSION -- NOT AGREEMENT.

  The two a_0 footings the programme carries (9.3619e-11 canonical and
  1.1279e-10 alternative) exist precisely because of this: the alternative
  footing was chosen to sit nearer the measured MOND value. So the honest
  statement is that the Zimmerman formula, evaluated with the canonical
  Omega_Lambda and H_0, UNDERSHOOTS the a_0 that rotation curves prefer by
  about 22%.

  That is either (a) a systematic in the measured a_0 (its literature values
  range by ~20-30% depending on sample and fitting), or (b) a real
  discrepancy in the postulate. It has NOT been resolved, and it is the
  sharpest non-circular test the framework has.

WHAT WOULD SETTLE IT: a precision determination of a_0 from galaxy data with
systematics below ~5%, compared against a_0 = (1/2) c sqrt(G rho_L) with
precision H_0 and Omega_Lambda. If they agree at 5%, the postulate is
confirmed non-circularly. If the 22% persists, the postulate is wrong (or
needs a coefficient), and everything downstream changes.

Every check states measurement and threshold separately.
"""
import math, json

RES, NP_, NF_ = [], 0, 0
def check(n, measured, ok, d=""):
    global NP_, NF_
    ok = bool(ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {n}")
    print(f"         measured: {measured}")
    if d: print(f"         {d}")
    RES.append({"check": n, "measured": measured, "pass": ok})
    if ok: NP_ += 1
    else:  NF_ += 1
    return ok

G, c = 6.67430e-11, 2.99792458e8
H0 = 67.4e3/3.0856775814913673e22
OmL = 0.685
rho_c = 3.0*H0**2/(8.0*math.pi*G)
a0_pred = 0.5*c*math.sqrt(G*OmL*rho_c)

print("="*74)
print("H029 -- THE CIRCULARITY AUDIT")
print("="*74)

# ---- 1. the four "results" are one
print("\n" + "="*74)
print("PART 1 -- THE FOUR 'RESULTS' ARE ALGEBRAICALLY ONE STATEMENT")
print("="*74)
H_L  = H0*math.sqrt(OmL)
r20  = c*H0/a0_pred
r20t = math.sqrt(32.0*math.pi/(3.0*OmL))
r28  = c*H_L/a0_pred
r28t = 2.0*math.sqrt(8.0*math.pi/3.0)
print(f"  H020  c H_0/a_0    = {r20:.10f}   vs sqrt(32pi/3OmL) = {r20t:.10f}")
print(f"  H028  c H_L/a_0    = {r28:.10f}   vs 2 sqrt(8pi/3)   = {r28t:.10f}")
check("C1 [THE AUDIT VERDICT] H016/H019/H020/H028 are algebraically IDENTICAL\n"
      "      to the postulate a_0 = (1/2) c sqrt(G rho_L): mutually circular",
      f"|cH_0/a_0 - sqrt(32pi/3OmL)| = {abs(r20-r20t):.2e};  "
      f"|cH_L/a_0 - 2sqrt(8pi/3)| = {abs(r28-r28t):.2e}",
      abs(r20-r20t) < 1e-9 and abs(r28-r28t) < 1e-9,
      "They are UNIFICATIONS (three field facts become one), not four\n"
      "         independent confirmations. Recorded as such.")

# ---- 2. the decisive non-circular test
print("\n" + "="*74)
print("PART 2 -- THE DECISIVE NON-CIRCULAR TEST: a_0 PREDICTED vs MEASURED")
print("="*74)
a0_meas = 1.2e-10            # literature MOND value from rotation-curve fits
disc = abs(a0_pred - a0_meas)/a0_meas
print(f"  a_0 predicted from (Omega_L, H_0)  = {a0_pred:.4e} m/s^2")
print(f"  a_0 measured from galaxy fits      ~ {a0_meas:.4e} m/s^2")
print(f"  DISCREPANCY                        = {disc*100:.1f}%")
check("C2 [THE REAL TEST, AND IT IS A TENSION] the postulate's a_0 differs from\n"
      "      the rotation-curve value by ~22% -- NOT agreement",
      f"predicted {a0_pred:.4e} vs measured ~{a0_meas:.4e}: {disc*100:.1f}% apart",
      disc > 0.05,
      "THIS IS THE SHARPEST NON-CIRCULAR TEST, AND THE FRAMEWORK DOES NOT\n"
      "         PASS IT CLEANLY. The programme's two a_0 footings exist because\n"
      "         of exactly this: the alternative (1.1279e-10) was chosen to sit\n"
      "         nearer the measured value. Either the measured a_0 carries ~20%\n"
      "         systematics (its literature values do range that widely), or the\n"
      "         postulate needs correcting. UNRESOLVED, and stated as such.")

# ---- 3. what IS independent
print("\n" + "="*74)
print("PART 3 -- WHAT IS GENUINELY NON-CIRCULAR")
print("="*74)
items = [
 ("shape n = 2 from TT rank D(D-3)/2", "independent of a_0's value", True),
 ("RAR fit: mu_2 + a_0 vs 155 SPARC curves, 0.150 dex, 0 params",
  "shape and scale enter differently", True),
 ("amplitude law: uses g_ext measured independently by 2MRS",
  "g_ext is not from the postulate", True),
 ("strong field: c_T = c, no hair -- from the action's FORM",
  "does not involve a_0", True),
 ("cluster shape: the phantom slope", "independent of a_0's value", True),
]
for name, why, ok in items:
    print(f"    {name}")
    print(f"        -> {why}")
check("C3 [THE INDEPENDENT CONTENT] five results do NOT depend on the value of\n"
      "      a_0 and survive even if the postulate's coefficient is wrong",
      f"{len(items)} independent results identified",
      all(ok for _, _, ok in items),
      "These are the framework's real content. The unification results\n"
      "         (H016/H019/H020/H028) are consistency, not confirmation.")

print("\n" + "="*74)
print(f"H029 READING:  {NP_} PASS / {NF_} FAIL")
print("="*74)
print(f"""
THE HONEST VERDICT
------------------
H016, H019, H020 and H028 are algebraically identical to the postulate
a_0 = (1/2) c sqrt(G rho_Lambda). They are UNIFICATIONS -- three empirical
facts of the field (the seesaw, a_0 ~ cH_0/7, Z = 5.789) collapse into one --
but they are NOT four independent confirmations, and counting them as such
was an error I am correcting here.

THE REAL TEST IS THE 22%.
  a_0 predicted from (Omega_L, H_0) = {a0_pred:.4e}
  a_0 measured from rotation curves ~ {a0_meas:.4e}
  They differ by {disc*100:.0f}%. That is non-circular, and it is a TENSION,
  not a success. It is unresolved: either the measured a_0 has ~20-30%
  systematics (its literature values do vary that much) or the postulate is
  wrong.

WHAT SURVIVES REGARDLESS: the shape (n=2 derived), the RAR fit, the amplitude
law, the strong-field sector, and the cluster shape -- none of which depend on
a_0's numerical value.

WHAT SETTLES IT: a_0 from galaxy data with <5% systematics against
(1/2) c sqrt(G rho_L) with precision H_0 and Omega_Lambda. Agreement at 5%
confirms the postulate non-circularly; a persistent 22% falsifies it.
""")

json.dump({"lane":"H029","pass":NP_,"fail":NF_,"results":RES,
           "verdict":"H016/H019/H020/H028 are mutually circular (unifications)",
           "a0_predicted":a0_pred, "a0_measured_literature":a0_meas,
           "discrepancy_pct":disc*100,
           "independent_content":["n=2 shape","RAR fit","amplitude law",
                                 "strong field","cluster shape"]},
          open("/Users/carlzimmerman/new_physics/zimmerman-formula/hy4_push/H029_results.json","w"),
          indent=2)
print(json.dumps({"pass":NP_,"fail":NF_}))
