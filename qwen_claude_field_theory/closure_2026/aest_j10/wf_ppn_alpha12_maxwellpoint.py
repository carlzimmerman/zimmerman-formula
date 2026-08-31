"""
wf_ppn_alpha12_maxwellpoint.py
================================
PPN preferred-frame parameters alpha_1, alpha_2 for AeST+J10.

STRATEGY (honest):
  - AeST's aether kinetic term is EXACTLY the Maxwell/F^2 Einstein-aether point:
        c_1 = -c_3 = K_B,   c_2 = c_4 = 0    (task convention: c_1=+K_B, c_3=-K_B)
  - Foster-Jacobson (gr-qc/0509083) give closed forms for alpha_1, alpha_2(c_1..c_4),
    cross-checked verbatim against Oost-Mukohyama-Wang (arXiv:1802.04303) eq (1.1),(3.4).
  - We (a) evaluate the AETHER-SECTOR alpha_1, alpha_2 at the Maxwell point,
        (b) evaluate the spin-2/1/0 wave speeds there,
        (c) expose the c_123 -> 0 degeneracy that makes the pure-aether alpha_2 SINGULAR
            (this is the "missing scalar mode" that AeST's phi must supply).
  We do NOT fabricate the AeST scalar correction; we localise exactly where it enters.

Foster-Jacobson / Oost-Mukohyama-Wang formulas (verbatim):
  alpha_1 = -8(c_3^2 + c_1 c_4) / (2 c_1 - c_1^2 + c_3^2)
  alpha_2 =  alpha_1/2
             - (c_1 + 2 c_3 - c_4)(2 c_1 + 3 c_2 + c_3 + c_4) / [ c_123 (2 - c_14) ]
  c_T^2 = 1/(1 - c_13)
  c_V^2 = [2 c_1 - c_13(2 c_1 - c_13)] / [2 c_14 (1 - c_13)]
  c_S^2 = c_123 (2 - c_14) / [ c_14 (1 - c_13)(2 + c_13 + 3 c_2) ]
  with c_ij = c_i + c_j, c_123 = c_1 + c_2 + c_3.
"""
import sympy as sp

c1, c2, c3, c4, KB, eps = sp.symbols('c1 c2 c3 c4 K_B epsilon', real=True)

c13 = c1 + c3
c14 = c1 + c4
c123 = c1 + c2 + c3

alpha1 = -8*(c3**2 + c1*c4) / (2*c1 - c1**2 + c3**2)
alpha2 = alpha1/2 - (c1 + 2*c3 - c4)*(2*c1 + 3*c2 + c3 + c4) / (c123*(2 - c14))

cT2 = 1/(1 - c13)
cV2 = (2*c1 - c13*(2*c1 - c13)) / (2*c14*(1 - c13))
cS2 = c123*(2 - c14) / (c14*(1 - c13)*(2 + c13 + 3*c2))

print("="*70)
print("GENERAL (symbolic) Einstein-aether PPN + wave speeds")
print("="*70)
print("alpha_1 =", alpha1)
print("alpha_2 =", sp.simplify(alpha2))
print("c_T^2   =", cT2)
print("c_V^2   =", sp.simplify(cV2))
print("c_S^2   =", sp.simplify(cS2))

# ---- Maxwell point of AeST: c1 = KB, c3 = -KB, c2 = c4 = 0 -----------------
sub_max = {c1: KB, c3: -KB, c2: 0, c4: 0}
print("\n" + "="*70)
print("AeST MAXWELL POINT  c1=K_B, c3=-K_B, c2=c4=0")
print("="*70)
print("c_13  =", (c13).subs(sub_max))
print("c_14  =", (c14).subs(sub_max))
print("c_123 =", (c123).subs(sub_max), "   <-- ZERO (spin-0 aether frozen)")

a1_max = sp.simplify(alpha1.subs(sub_max))
print("\nalpha_1(Maxwell) =", a1_max, "   [SOLID: aether sector]")

cT2_max = sp.simplify(cT2.subs(sub_max))
cV2_max = sp.simplify(cV2.subs(sub_max))
print("c_T^2(Maxwell)   =", cT2_max)
print("c_V^2(Maxwell)   =", cV2_max)
# c_S^2 has 0/0? evaluate numerator & denominator separately
cS2_num = (c123*(2 - c14)).subs(sub_max)
cS2_den = (c14*(1 - c13)*(2 + c13 + 3*c2)).subs(sub_max)
print("c_S^2 numerator  =", sp.simplify(cS2_num), " ; denominator =", sp.simplify(cS2_den))
print("  -> c_S^2(Maxwell) =", sp.simplify(cS2_num/cS2_den), " (spin-0 mode NON-propagating)")

# alpha_2 at Maxwell point: expect a pole because c_123 -> 0
print("\n--- alpha_2 at the Maxwell point ---")
a2_num = ((c1 + 2*c3 - c4)*(2*c1 + 3*c2 + c3 + c4)).subs(sub_max)
a2_den = (c123*(2 - c14)).subs(sub_max)
print("second-term numerator   =", sp.simplify(a2_num))
print("second-term denominator =", sp.simplify(a2_den), "  <-- ZERO => alpha_2 SINGULAR")

# Approach the point along c2 = eps (regulator) to see the pole sign/order
sub_reg = {c1: KB, c3: -KB, c4: 0, c2: eps}
a2_reg = alpha2.subs(sub_reg)
a2_series = sp.series(sp.simplify(a2_reg), eps, 0, 1).removeO()
print("\nRegulate c2 = eps ->0 (KB fixed): alpha_2 =")
print("   ", sp.simplify(a2_reg))
print("Leading Laurent term in eps:")
print("   ", sp.simplify(a2_series), "   => simple pole ~ (K_B/eps): DIVERGES")

# ---- Does the Maxwell point satisfy the alpha=0 null family? ----------------
# Foster-Jacobson null conditions: c2 = (-2c1^2 - c1 c3 + c3^2)/(3 c1); c4 = -c3^2/c1
c2_null = (-2*c1**2 - c1*c3 + c3**2)/(3*c1)
c4_null = -c3**2/c1
print("\n" + "="*70)
print("Is Maxwell point on the Foster-Jacobson alpha_1=alpha_2=0 family?")
print("="*70)
print("required c2_null(c1=KB,c3=-KB) =", sp.simplify(c2_null.subs({c1:KB, c3:-KB})),
      "  but AeST has c2 = 0")
print("required c4_null(c1=KB,c3=-KB) =", sp.simplify(c4_null.subs({c1:KB, c3:-KB})),
      "  but AeST has c4 = 0")
print("=> AeST aether sector is NOT on the null family; aether alpha_1 = -4 K_B != 0.")

# ---- numeric sanity + observational bound translation ----------------------
print("\n" + "="*70)
print("Numeric: alpha_1 = -4 K_B  vs observational bounds")
print("="*70)
for KBval in [0.25, 0.1, 0.01, 2.5e-5, 2.5e-6]:
    a1 = -4*KBval
    print(f"  K_B={KBval:>8}:  alpha_1(aether) = {a1:+.3e}")
print("Bounds: |alpha_1| <~ 1e-4 (LLR), <~ few e-5 (binary pulsars, Shao-Wex);")
print("        |alpha_2| <~ 4e-7 (LLR/solar-spin), <~ 2e-9 (solar spin-axis, Nordtvedt).")
print("=> If aether alpha_1=-4K_B is UNCANCELLED, |alpha_1|<1e-4 forces K_B<2.5e-5.")
print("   AeST phenomenology uses K_B up to ~0.25 => scalar sector MUST cancel/shift,")
print("   OR K_B is tiny. Which one: NOT-COMPUTED (needs full AeST O(v) PPN).")
