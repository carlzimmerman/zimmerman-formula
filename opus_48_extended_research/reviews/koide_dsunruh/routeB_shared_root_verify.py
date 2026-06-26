import sympy as sp
import mpmath as mp
mp.mp.dps = 50

print("="*78)
print("ROUTE B SHARED-ROOT TEST: does ONE forced invariant feed BOTH a0 AND delta?")
print("="*78)

# ---------------------------------------------------------------
# (A) The framework's a0 normalization invariant (the GRAVITY side)
#     a0 = c^2 sqrt(Lambda/32pi);  the dimensionless normalization that fixes
#     a0 from Lambda is the geometric factor (3/8pi)^(1/4) = sqrt(2/Z), Z=sqrt(32pi/3).
#     This is the CKN-saturation / Friedmann-3 x Einstein-8pi geometry (banked).
# ---------------------------------------------------------------
pi = sp.pi
Z2 = sp.Rational(32,3)*pi
Z  = sp.sqrt(Z2)
a0_norm = (sp.Rational(3,1)/(8*pi))**sp.Rational(1,4)     # the gravity-side invariant
print("\n(A) GRAVITY-SIDE forced invariant (sets a0 from Lambda):")
print("    Z = sqrt(32pi/3)              =", mp.mpf(sp.N(Z,40)))
print("    a0 normalization (3/8pi)^1/4  =", mp.mpf(sp.N(a0_norm,40)))
print("    sqrt(2/Z) == (3/8pi)^1/4 ?    ", sp.simplify(sp.sqrt(2/Z) - a0_norm)==0)

# ---------------------------------------------------------------
# (B) The Koide-forcing invariant (the FLAVOR side): delta=sqrt(3/2) gives K=2/3.
#     Singh's EJA fixes delta by the characteristic cubic + coassociativity +
#     Dirac/Majorana neutrino nature.  delta_Dirac^2 = 3/2 ; delta_Majorana^2 = 3/8.
# ---------------------------------------------------------------
delta_Dirac = sp.sqrt(sp.Rational(3,2))
delta_Maj   = sp.sqrt(sp.Rational(3,8))
print("\n(B) FLAVOR-SIDE Koide-forcing invariant:")
print("    delta_Dirac = sqrt(3/2)       =", mp.mpf(sp.N(delta_Dirac,40)), " -> K=2/3 exact")
print("    delta_Maj   = sqrt(3/8)       =", mp.mpf(sp.N(delta_Maj,40)),  " -> mass ratios fit")

# ---------------------------------------------------------------
# (C) SHARED ROOT TEST: is the gravity-side invariant EQUAL to (or simply related to)
#     the flavor-side delta?  If YES (sympy-exact, no smuggling) -> the bridge.
# ---------------------------------------------------------------
print("\n(C) SHARED-ROOT comparisons (sympy-exact):")
tests = {
  "a0_norm == delta_Dirac ?"            : sp.simplify(a0_norm - delta_Dirac),
  "a0_norm == delta_Maj ?"              : sp.simplify(a0_norm - delta_Maj),
  "a0_norm == 1/delta_Dirac ?"          : sp.simplify(a0_norm - 1/delta_Dirac),
  "Z relates to delta_Dirac? (Z=...)"   : sp.simplify(Z - delta_Dirac),
  "a0_norm^2 == 3/8 ? (=delta_Maj^2)"   : sp.simplify(a0_norm**2 - sp.Rational(3,8)),
  "a0_norm^4 == 3/8pi vs delta_Maj^2=3/8": sp.simplify(a0_norm**4 - sp.Rational(3,8)),
}
for name, expr in tests.items():
    print(f"    {name:42s} residual = {expr}  -> {'MATCH' if expr==0 else 'NO'}")

print("""
    NOTE the near-miss trap:  a0_norm = (3/8pi)^(1/4)  and  delta_Maj^2 = 3/8.
    They share the rational 3/8 but a0_norm has a 1/pi INSIDE and a 4th root;
    delta_Maj^2 = 3/8 is pi-FREE.  a0_norm^4 = 3/(8pi) != 3/8 = delta_Maj^2.""")
print("    a0_norm^4 = 3/(8pi) =", mp.mpf(sp.N(a0_norm**4,30)), " vs delta_Maj^2 = 3/8 =", mp.mpf(sp.N(sp.Rational(3,8),30)))
print("    ratio (a0_norm^4)/(delta_Maj^2) = 1/pi =", mp.mpf(sp.N(a0_norm**4/sp.Rational(3,8),30)))

# ---------------------------------------------------------------
# (D) SMUGGLE CHECK on "delta=sqrt(3/2) is forced".  delta=sqrt(3/2) <=> K=2/3 <=> r=sqrt2.
#     Does ANY independent (non-Koide) principle yield delta^2=3/2?
#     Singh's OWN selection rule: delta is fixed by the EJA cubic to delta_Maj^2=3/8 for
#     charged fermions (Majorana neutrino), NOT 3/2.  delta^2=3/2 is the UNBROKEN/Dirac
#     value, which Singh REJECTS because it breaks the mass ratios.  So inside Singh,
#     "force sqrt(3/2)" = "assume Dirac + assume the unbroken triple" = which gives 2/3 by
#     construction (it IS the symmetric (1-d,1,1+d) at the 45-deg point).  That is circular
#     w.r.t. Koide UNLESS an external (gravity/dS) principle picks Dirac+unbroken.
#     Singh provides NO such gravity/dS principle (verified: no Lambda in 2508.10131).
# ---------------------------------------------------------------
print("\n(D) SMUGGLE CHECK: is delta=sqrt(3/2) forced WITHOUT assuming Koide?")
# The map delta^2 -> K is monotone & invertible; K=2/3 <=> delta^2=3/2 EXACTLY.
dvar = sp.symbols('delta', positive=True)
K_of_d = sp.Rational(1,3) + 2*dvar**2/9
sol = sp.solve(sp.Eq(K_of_d, sp.Rational(2,3)), dvar)
print("    K(delta)=1/3+2 delta^2/9 ; K=2/3 <=> delta =", sol, " = sqrt(3/2)")
print("    => 'force delta=sqrt(3/2)' is LOGICALLY IDENTICAL to 'impose K=2/3'.")
print("       Any route to sqrt(3/2) that does not invoke an INDEPENDENT gravity/dS")
print("       constraint is a re-labeling of Koide. Singh selects delta by the")
print("       neutrino nature + MASS-RATIO FIT, NOT by Lambda/a0.")
