import sympy as sp

# ============================================================
# PART 1: The Yukawaon "derivation" of R = [PhiPhi]/[Phi]^2 = 2/3
# Koide 0811.3470 — is 2/3 FORCED or does it hinge on xi=-3 (a chosen coefficient)?
# ============================================================

xi = sp.symbols('xi', real=True)

# Eq (2.15): R_e = 1 - 2*xi/(9*(1+xi))
R = 1 - 2*xi/(9*(1+xi))
print("Eq(2.15) R(xi) =", sp.simplify(R))

# Solve R = 2/3 for xi
sol = sp.solve(sp.Eq(R, sp.Rational(2,3)), xi)
print("R = 2/3  <=>  xi =", sol)

# So 2/3 requires xi = -3 EXACTLY. Check what R is for nearby xi (xi = -3 + eps)
eps = sp.symbols('epsilon', positive=True)
R_pert = R.subs(xi, -3 + eps)
print("R(xi=-3+eps) =", sp.simplify(R_pert))
print("  -> as eps->0, R ->", sp.limit(R_pert, eps, 0))
print("  series:", sp.series(R_pert, eps, 0, 2))

# ============================================================
# PART 2: connect R=[PhiPhi]/[Phi]^2 to the Koide Q and to r=sqrt2
# In the Yukawaon model the VEV v_i = <(Phi_e)_ii> with sqrt(m_i) ~ v_i
# Koide Q = (sum m)/(sum sqrt m)^2 = (sum v^2)/(sum v)^2 = [PhiPhi]/[Phi]^2 = R
# So R = Q. The relation 2/3 here IS the Koide Q (with v_i = sqrt(m_i)).
# Now Q = 1/3 + r^2/6 where r is the std-component amplitude. Check Q=2/3 <=> r=sqrt2.
# ============================================================
r = sp.symbols('r', positive=True)
Q_of_r = sp.Rational(1,3) + r**2/6
sol_r = sp.solve(sp.Eq(Q_of_r, sp.Rational(2,3)), r)
print("\nQ = 1/3 + r^2/6 ;  Q=2/3 <=> r =", sol_r, " (sqrt2 =", float(sp.sqrt(2)), ")")

# ============================================================
# PART 3: Does the SPECIFIC potential force xi=-3, or is xi=-3 a structural CHOICE?
# Eq (2.11): c2 = -(2/3)*xi/(1+xi)*[Phi]  must equal -[Phi]  (the cubic's c2 = -[Phi] identically, Eq 2.10)
# => -(2/3)*xi/(1+xi) = -1  => solve:
# ============================================================
lhs = -sp.Rational(2,3)*xi/(1+xi)
sol_c2 = sp.solve(sp.Eq(lhs, -1), xi)
print("\nEq(2.11/2.12): c2-consistency  -(2/3)xi/(1+xi) = -1  =>  xi =", sol_c2)
print("  i.e. (xi+3)[Phi]=0, and since [Phi]!=0 is REQUIRED (nonzero masses) => xi=-3 forced")

# So WITHIN the chosen term structure (the Phi_e Phihat_e Phihat_e term, Eq 2.5/2.8),
# xi=-3 is forced by [Phi]!=0. But xi itself (Eq 2.6) is a RATIO of chosen couplings
# lambda''_A / (lambda'_A - (mu'_A/mu_A) lambda_A). The structural input is the CHOICE
# that only the traceless-cubed term Phihat^3 appears (Z2 / U(1)_X engineering).
