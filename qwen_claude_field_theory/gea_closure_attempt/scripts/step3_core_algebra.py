"""
Step 3: Core algebra of the exact exponential MOND law in GEA (Sec 4-6).

Conventions: signature (-,+,+,+), c=1.
  K = kappa * y^2,  kappa = -a0^2 c1 / M^2   (from Step 1).
  C = c1 - c4.
  Exact MOND law:  mu(y) = 1 - exp(-y).

We:
  (Sec 4) verify the Living-Reviews weak-field relation
        mu = F_K + (1-F_K)/(1-C/2)
    is mutually consistent with mu = 1-e^{-y}, and solve for F_K(K).
    Verify F_K(0) = 2/C.
  (Sec 5) derive the MOND identity  cbar1 - cbar4 = 2,  cbar_i = F_K(0) c_i.
  (Sec 6) integrate F_K to get F(K), verify by differentiating, and expand
        F = F0 + F1 K + F_{3/2} K^{3/2} + O(K^2),  computing F1, F_{3/2}.
"""
import sympy as sp

# ---- symbols ----
C = sp.symbols('C', real=True)              # C = c1 - c4
kappa = sp.symbols('kappa', positive=True)  # kappa = -a0^2 c1/M^2 (assume >0 on MOND branch)
y = sp.symbols('y', positive=True)
K = sp.symbols('K', positive=True)
c1, c2, c3, c4 = sp.symbols('c1 c2 c3 c4', real=True)
M, a0 = sp.symbols('M a0', positive=True)

print("="*70)
print("SEC 4:  Exact F_K and the MOND relation")
print("="*70)

# Living-Reviews weak-field relation:
#   mu = F_K + (1 - F_K)/(1 - C/2).
# Solve for F_K in terms of mu:
FK = sp.symbols('FK')
mu = sp.symbols('mu')
D = 1 - C/2
sol_FK = sp.solve(sp.Eq(mu, FK + (1-FK)/D), FK)[0]
sol_FK = sp.simplify(sol_FK)
print("F_K(mu) =", sol_FK)

# Impose mu = 1 - e^{-y}:
mu_MOND = 1 - sp.exp(-y)
FK_of_y = sp.simplify(sol_FK.subs(mu, mu_MOND))
print("F_K(y)  =", FK_of_y)

# Express in terms of K: y = sqrt(K/kappa).
FK_of_K = sp.simplify(FK_of_y.subs(y, sp.sqrt(K/kappa)))
print("F_K(K)  =", FK_of_K)

# The assignment's claimed form:
FK_claim = ((1-C/2)*(1-sp.exp(-sp.sqrt(K/kappa)))-1)/(-C/2)
print("Claimed F_K(K) =", sp.simplify(FK_claim))
print("Difference (should be 0):", sp.simplify(FK_of_K - FK_claim))

# Verify F_K(0) = 2/C:
FK0 = sp.simplify(FK_of_y.subs(y, 0))
print("\nF_K(0) =", FK0)
print("2/C     =", sp.simplify(2/C))
print("F_K(0) - 2/C =", sp.simplify(FK0 - 2/C))

print("\n" + "="*70)
print("SEC 4b:  Verify mu = 1-e^{-y} by substituting F_K back into the relation")
print("="*70)
mu_back = sp.simplify(FK_of_y + (1-FK_of_y)/D)
print("mu from F_K(y) =", mu_back)
print("mu - (1-e^{-y}) =", sp.simplify(mu_back - mu_MOND))

print("\n" + "="*70)
print("SEC 5:  MOND identity  cbar1 - cbar4 = 2")
print("="*70)
# cbar_i = F_K(0) c_i.
cbar1 = FK0*c1
cbar2 = FK0*c2
cbar3 = FK0*c3
cbar4 = FK0*c4
# cbar1 - cbar4 = F_K(0)(c1-c4) = (2/C)*C = 2.
identity = sp.simplify(cbar1 - cbar4)
print("cbar1 - cbar4 =", identity)
# Note c1-c4 = C by definition, so (2/C)*C = 2 exactly.
print("cbar1-cbar4 (using c1-c4=C) =", sp.simplify(FK0*C))

print("\n" + "="*70)
print("SEC 6:  Exact F(K), verification, and expansion")
print("="*70)
# Integrate F_K(K) to get F(K).
F_of_K = sp.integrate(FK_of_K, (K, 0, K))   # F(K) - F(0); F(0) is an additive constant
F_of_K = sp.simplify(F_of_K)
print("F(K) - F(0) =", F_of_K)

# Verify by differentiating: dF/dK should equal F_K(K).
dF_dK = sp.simplify(sp.diff(F_of_K, K))
print("dF/dK =", dF_dK)
print("dF/dK - F_K(K) =", sp.simplify(dF_dK - FK_of_K))

# Expansion F = F0 + F1 K + F_{3/2} K^{3/2} + O(K^2).
# Work in s = sqrt(K).  F(K) = F0 + int_0^K F_K(K') dK'.  With K'=s'^2, dK'=2s'ds':
#   F = F0 + int_0^s F_K(s'^2) 2 s' ds'.
s = sp.symbols('s', positive=True)
FK_s = FK_of_K.subs(K, s**2)
# Expand F_K(s^2) in s up to s^3 (need up to K^{3/2}=s^3 in F, i.e. F_K up to s^2... )
# Actually F ~ F0 + F1 s^2 + F_{3/2} s^3 + ... so F_K = dF/dK = (1/(2s)) dF/ds
#   = F1 + (3/2) F_{3/2} s + ...  So F_K series in s up to s^1 gives F1, F_{3/2}.
FK_ser = sp.series(FK_s, s, 0, 3).removeO()   # terms s^0, s^1, s^2
FK_ser = sp.simplify(FK_ser)
print("\nF_K(s^2) series in s:", FK_ser)
# Integrate: F - F0 = int_0^s FK_ser(s') 2 s' ds'
F_ser = sp.simplify(sp.integrate(FK_ser*2*s, (s, 0, s)))
print("F(K) series (in s):", F_ser)
# Convert to K: s^2 = K, s^3 = K^{3/2}
F_series_K = sp.simplify(F_ser.subs(s**2, K).subs(s, K**sp.Rational(1,2)))
print("F(K) = F0 + ... :", F_series_K)

# Extract coefficients: F_ser is in s; expand then read coeff of s^2 (=K) and s^3 (=K^{3/2}).
F_check = sp.expand(F_ser)
print("F(K) series expanded in s:", F_check)
F1 = sp.simplify(F_check.coeff(s, 2))
F32 = sp.simplify(F_check.coeff(s, 3))
F2 = sp.simplify(F_check.coeff(s, 4))
print("\nF1      =", F1)
print("F_{3/2} =", F32)
print("F2 (K^2 coeff) =", F2)

# Cross-check F1 = F_K(0) = 2/C.
print("F1 - 2/C =", sp.simplify(F1 - 2/C))

# Express F_{3/2} in terms of a0, M, c1, C  (kappa = -a0^2 c1/M^2).
F32_phys = sp.simplify(F32.subs(kappa, -a0**2*c1/M**2))
print("F_{3/2} (physical) =", F32_phys)
