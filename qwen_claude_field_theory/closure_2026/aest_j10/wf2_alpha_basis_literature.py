"""
wf2_alpha_basis_literature.py
=============================
Question: what is the ACTUAL basis for alpha_1 = alpha_2 = 0 in AeST?

This script does the ONE symbolic cross-check that decides the literature claim:
does the Foster-Jacobson Einstein-aether alpha_1=alpha_2=0 SURFACE pass through
the AeST 'Maxwell point' (c1=K_B, c3=-K_B, c2=c4=0)?

Foster-Jacobson (gr-qc/0509083) closed forms, cross-checked verbatim against
Oost-Mukohyama-Wang 1802.04303 eq (3.4) and the published alpha=0 conditions
(quoted in Jacobson status report 0801.1547 / EA reviews):
      alpha_1=0, alpha_2=0  <=>  c2 = (-2 c1^2 - c1 c3 + c3^2)/(3 c1),
                                 c4 = -c3^2 / c1.
We (1) VERIFY those two conditions really zero the FJ formulas (self-consistency
of the transcription), then (2) test the Maxwell point against them.

NO fabricated numbers: every algebraic statement is a sympy identity, printed.
"""
import sympy as sp

c1, c2, c3, c4, KB = sp.symbols('c1 c2 c3 c4 K_B', real=True)

c13 = c1 + c3
c14 = c1 + c4
c123 = c1 + c2 + c3

# Foster-Jacobson PPN preferred-frame parameters (EA), verbatim transcription
alpha1 = -8*(c3**2 + c1*c4) / (2*c1 - c1**2 + c3**2)
alpha2 = ( alpha1/2
           - (c1 + 2*c3 - c4)*(2*c1 + 3*c2 + c3 + c4) / (c123*(2 - c14)) )

# EA linear-mode speeds (Jacobson 0801.1547)
cT2 = 1/(1 - c13)
cV2 = (2*c1 - c13*(2*c1 - c13)) / (2*c14*(1 - c13))
cS2 = c123*(2 - c14) / (c14*(1 - c13)*(2 + c13 + 3*c2))

print("="*72)
print("STEP 1  Self-consistency: do the PUBLISHED alpha=0 conditions zero the")
print("        Foster-Jacobson formulas?  (validates my transcription)")
print("="*72)
c2_null = (-2*c1**2 - c1*c3 + c3**2)/(3*c1)   # published condition
c4_null = -c3**2/c1                            # published condition
sub_null = {c2: c2_null, c4: c4_null}
a1_null = sp.simplify(alpha1.subs(sub_null))
a2_null = sp.simplify(alpha2.subs(sub_null))
print("  substitute c2=c2_null, c4=c4_null :")
print("    alpha_1 ->", a1_null)
print("    alpha_2 ->", a2_null)
print("  => transcription is",
      "CONSISTENT (both zero)" if (a1_null==0 and a2_null==0) else "INCONSISTENT")

print()
print("="*72)
print("STEP 2  Does the AeST MAXWELL POINT lie on that alpha=0 surface?")
print("        AeST aether kinetic term = -(K_B/2)F_{mn}F^{mn}")
print("        <=> Einstein-aether  c1=+K_B, c3=-K_B, c2=0, c4=0")
print("="*72)
req_c2 = sp.simplify(c2_null.subs({c1: KB, c3: -KB}))
req_c4 = sp.simplify(c4_null.subs({c1: KB, c3: -KB}))
print(f"  alpha=0 surface REQUIRES: c2 = {req_c2} ,  c4 = {req_c4}")
print(f"  AeST Maxwell point HAS  : c2 = 0 ,  c4 = 0")
print(f"    c2 condition: {'MET' if req_c2==0 else 'FAILED'}  (0 == 0)")
print(f"    c4 condition: {'MET' if req_c4==0 else 'FAILED'}  (need {req_c4}, have 0)"
      f"  <=== the Maxwell point is OFF the surface")

print()
print("="*72)
print("STEP 3  Aether-sector alpha_1, alpha_2 AT the Maxwell point")
print("="*72)
sub_max = {c1: KB, c3: -KB, c2: 0, c4: 0}
print("  alpha_1(Maxwell)   =", sp.simplify(alpha1.subs(sub_max)), " (finite, nonzero)")
a2_num = sp.simplify((c1 + 2*c3 - c4).subs(sub_max))
a2_den = sp.simplify((c123*(2 - c14)).subs(sub_max))
print("  alpha_2(Maxwell)   : 2nd-term denominator = c123*(2-c14) =", a2_den,
      " -> POLE (singular)")
print("  c_S^2(Maxwell)     =", sp.simplify(cS2.subs(sub_max)),
      " (spin-0 aether mode FROZEN)")
print("  c_T^2, c_V^2       =", sp.simplify(cT2.subs(sub_max)),
      ",", sp.simplify(cV2.subs(sub_max)))
print("  NOTE: c123 -> 0 SIMULTANEOUSLY freezes the spin-0 mode (c_S^2=0) and")
print("        makes alpha_2 singular. Same zero. This is the strong-coupling")
print("        point, NOT the 'extra-symmetry' alpha=0 point (which needs c4!=0).")

print()
print("="*72)
print("CONCLUSION (algebra):")
print("  The AeST Maxwell point is NOT on the Einstein-aether alpha_1=alpha_2=0")
print("  surface. The published EA route to alpha=0 REQUIRES c4 = -c3^2/c1 = -K_B")
print("  and c2 = 0; AeST FORCES c2=0 (met by luck) but c4=0 (violates the c4")
print("  condition). So alpha_1=alpha_2=0 CANNOT come from the aether/Maxwell")
print("  sector: aether alpha_1 = -4 K_B and aether alpha_2 is singular.")
print("  Any AeST alpha=0 must therefore be supplied/repaired by the SCALAR")
print("  sector (phi, Q=A.grad phi) -- which the AeST literature does NOT compute.")
