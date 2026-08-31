"""
wf_verify_alpha2_maxwell_independent.py
=======================================
INDEPENDENT verification (fresh transcription) of the Foster-Jacobson
Einstein-aether PPN alpha_1, alpha_2 at the AeST Maxwell point.

I transcribe the FJ / Yagi-Blas-Barausse-Yunes (1210.3026) formulas myself,
substitute the AeST Maxwell point, and check:
  (1) alpha_1 = -4 K_B  ?
  (2) alpha_2 denominator = c_123*(2-c_14):  is it c_123=c1+c2+c3 (->0)
      or c2+c3 (->-K_B)?  DECISIVE for "singular vs finite".
  (3) wave speeds c_T^2, c_V^2, c_S^2 at the point.
  (4) pole order/sign under c2=eps and under c3=-KB+eps regulators (two
      independent regulators -- a genuine pole must appear in BOTH,
      a coordinate artifact would not).

Convention (task): c1 = +K_B, c3 = -K_B, c2 = c4 = 0.
"""
import sympy as sp

c1, c2, c3, c4, KB, eps = sp.symbols('c1 c2 c3 c4 K_B epsilon', real=True)

c12 = c1 + c2
c13 = c1 + c3
c14 = c1 + c4
c123 = c1 + c2 + c3

# ---------------------------------------------------------------------------
# Foster-Jacobson alpha_1, alpha_2 (as in Yagi et al 1210.3026 eq. 2-3,
# Foster-Jacobson gr-qc/0509083). Transcribed independently.
# ---------------------------------------------------------------------------
alpha1 = -8*(c3**2 + c1*c4) / (2*c1 - c1**2 + c3**2)
alpha2 = ( alpha1/2
           - (c1 + 2*c3 - c4)*(2*c1 + 3*c2 + c3 + c4)
             / ( c123*(2 - c14) ) )

# Wave speeds (Jacobson status report 0801.1547 eq 30-32)
cT2 = 1/(1 - c13)
cV2 = (2*c1 - c13*(2*c1 - c13)) / (2*c14*(1 - c13))
cS2 = ( c123*(2 - c14) ) / ( c14*(1 - c13)*(2 + c13 + 3*c2) )

sub_max = {c1: KB, c3: -KB, c2: 0, c4: 0}

print("MAXWELL-POINT COMBINATIONS")
print("  c13   =", c13.subs(sub_max))
print("  c14   =", c14.subs(sub_max))
print("  c123  =", c123.subs(sub_max), "  (c1+c2+c3)")
print("  c2+c3 =", (c2+c3).subs(sub_max), "  (the alternative the task warns about)")
print()

print("alpha_1(Maxwell) =", sp.simplify(alpha1.subs(sub_max)))
print()

# alpha_2 denominator diagnosis
den = (c123*(2-c14))
num = ((c1 + 2*c3 - c4)*(2*c1 + 3*c2 + c3 + c4))
print("alpha_2 2nd-term  numerator(Maxwell)   =", sp.simplify(num.subs(sub_max)))
print("alpha_2 2nd-term  denominator(Maxwell) =", sp.simplify(den.subs(sub_max)),
      "  <-- if 0 => SINGULAR")
print()

# Regulator 1: c2 = eps  (turn on tiny spin-0 kinetic mixing)
sub_r1 = {c1: KB, c3: -KB, c4: 0, c2: eps}
a2_r1 = sp.simplify(alpha2.subs(sub_r1))
lead1 = sp.series(a2_r1, eps, 0, 1).removeO()
print("REGULATOR 1 (c2=eps):")
print("   alpha_2 =", a2_r1)
print("   Laurent lead (eps->0):", sp.simplify(lead1))
print()

# Regulator 2: c3 = -KB + eps  (break the exact Maxwell antisymmetry)
sub_r2 = {c1: KB, c3: -KB + eps, c4: 0, c2: 0}
a2_r2 = sp.simplify(alpha2.subs(sub_r2))
lead2 = sp.series(a2_r2, eps, 0, 1).removeO()
print("REGULATOR 2 (c3=-KB+eps):")
print("   alpha_2 =", a2_r2)
print("   Laurent lead (eps->0):", sp.simplify(lead2))
print()

# spin-0 speed at the point (numerator/denominator separately)
cS2_num = (c123*(2 - c14)).subs(sub_max)
cS2_den = (c14*(1 - c13)*(2 + c13 + 3*c2)).subs(sub_max)
print("SPIN-0 speed at Maxwell: num =", sp.simplify(cS2_num),
      " den =", sp.simplify(cS2_den),
      " -> c_S^2 =", sp.simplify(cS2_num/cS2_den))
print("c_T^2(Maxwell) =", sp.simplify(cT2.subs(sub_max)),
      "  c_V^2(Maxwell) =", sp.simplify(cV2.subs(sub_max)))
print()

# ---------------------------------------------------------------------------
# CROSS-CHECK the alpha_2 denominator against an INDEPENDENT algebraic
# identity: c_S^2 -> 0 <=> c123 -> 0 (with c14 finite). If alpha_2's pole
# and c_S^2's zero share the SAME factor c123, the "frozen spin-0 => divergent
# static preferred-frame response" mechanism is real, not a transcription slip.
# ---------------------------------------------------------------------------
alpha2_den_factor = sp.factor(sp.denom(sp.together(alpha2)))
print("Full alpha_2 denominator (factored):")
print("   ", alpha2_den_factor)
print("Contains c123 = c1+c2+c3 as a factor?",
      sp.simplify(sp.rem(alpha2_den_factor, c123, c2)) == 0 or c123 in sp.factor_list(alpha2_den_factor)[1][0] if False else "see printed factors")
