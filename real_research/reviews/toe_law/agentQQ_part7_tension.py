import sympy as sp
import numpy as np
import mpmath as mp
mp.mp.dps = 30

print("="*78)
print("PART 7 — THE DEEP TENSION, adjudicated: does the active fold RE-VIOLATE the")
print("         specific stability/causality premise X2 USES, or stay inside it?")
print("="*78)

print("""
The worry (from the brief): X2 is a PASSIVITY bound; an active medium that violates
Cauchy-Schwarz risks violating the passivity/stability X2 USES. Adjudicate precisely
which premise each theorem RELIES ON vs CONCLUDES:

  X2 RELIES ON:   (P1) causality/retardation (analyticity in UHP),
                  (P2) convergent unsubtracted dispersion relation,
                  (P3) stability (unique fixed point, no runaway: X dynamics 6c).
  X2 CONCLUDES:   the medium is NON-passive (active) at the secular channel.
  PP RELIES ON:   passive (rho>=0) => Herglotz/Pick => monotone => no fold.
  PP CONCLUDES:   bounded fold needs NON-passive (rho<0 band).

So PP's 'non-passive' is X2's CONCLUSION, not X2's PREMISE. No logical clash THERE.
The ONLY genuine clash is if the active band needed for the fold breaks P1 or P3
(the premises X2 truly needs). Test P1 (causality) and P3 (stability) under the
fold-bounding active response.
""")

# ---- P1 test: causality of the full chi with the active k^6 floor. ----
# The temporal response at fixed k is chi(omega;k). Causality <=> poles in LHP.
# The spatial dispersion omega^2(k) = c^2 k^2 - alpha k^4 + beta k^6 gives, at each k,
# a pole at omega = +- omega(k) (real if om2>0). For om2>0 (the no-ghost window,
# s6>s6*), omega(k) is REAL => poles ON the real axis (undamped oscillator) => the
# retarded prescription omega -> omega + i0 puts them in LHP => CAUSAL. No UHP pole.
print("P1 (causality): in the no-ghost window (om2(k)>0 all k, i.e. s6>s6*), omega(k) is")
print("  REAL => retarded poles omega=+-omega(k)-i0 sit in LHP => CAUSAL. No runaway.")
print("  A GHOST (om2<0, s6<s6*) gives omega imaginary => a UHP pole => runaway. So the")
print("  SAME condition s6>s6* that bounds the fold also SECURES causality. NOT in tension.\n")

# ---- P3 test: positivity of energy / stability of the active gain band ----
# X §6c stability = unique fixed point of the MOND root + damped Picard. The k^6 floor
# does not touch the (algebraic) MOND root structure (that's the temporal/secular DC
# channel); it lives at finite k>0 in the SPATIAL sector. Check that the group velocity
# stays real and bounded (no superluminal-front / no gradient instability) in the window.
print("P3 (stability): check group velocity and that om2>0 (no gradient instability) in")
print("  the bounded-fold window.")
c2v, s4v = 1.0, -0.5
for s6 in [0.07, 0.10, 0.25]:
    # om2(u)=c2 u + s4 u^2 + s6 u^3, u=k^2. group vel^2 = (d omega/dk)^2; check om2>0
    us = np.linspace(0.001, 6, 4000)
    om2 = c2v*us + s4v*us**2 + s6*us**3
    om = np.sqrt(np.clip(om2, 0, None))
    k = np.sqrt(us)
    vg = np.gradient(om, k)
    okpos = np.all(om2 > -1e-12)
    print(f"  s6={s6}: om2>0 all k? {okpos};  group vel range [{vg.min():+.3f},{vg.max():+.3f}]  (vg=0 at roton min, finite => stable, no instability)")
print()
print("=> In the window s6>s6*: om2>0 (no gradient/ghost instability), vg real & finite")
print("   (vg=0 only at the roton minimum, the soft point, which is the EDGE itself).")
print("   P1 and P3 are SATISFIED by the very response that bounds the fold.\n")

print("VERDICT PART 7: NO CONTRADICTION between X2 and the bounded fold.")
print(" - PP-non-passivity = X2's CONCLUSION (not its premise); they AGREE the medium is active.")
print(" - The premises X2 actually USES (causality P1, stability P3) are PRESERVED in the")
print("   bounded-fold window s6>s6*: om2>0 secures both. The fold is bounded by a STABLE,")
print("   CAUSAL active response. The tension is APPARENT (premise/conclusion conflation),")
print("   resolved in favor of consistency.")
print(" - The cost is NOT a contradiction; it is a TUNING (s6>=s6*) the smooth bath fails to")
print("   supply (gives s6<0). So: CONSISTENT WINDOW EXISTS, but entering it is not forced.")
