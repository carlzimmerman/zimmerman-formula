import sympy as sp
# Authoritative: v = (sqrt m_0, sqrt m_1, sqrt m_2). n_hat=(1,1,1)/sqrt3.
# singlet proj norm^2 = (v.n_hat)^2 = (sum sqrt m)^2/3 = (TrV)^2/3
# doublet proj norm^2 = |v|^2 - (v.n_hat)^2 = TrV2 - (TrV)^2/3
# Koide K = (sum m)/(sum sqrt m)^2 = TrV2/(TrV)^2.   <-- NOTE: K uses TrV2/(TrV)^2, NOT (TrV)^2/(3 TrV2)!
# I had K inverted. Let's be careful: Q_Koide = (sum m_i)/(sum sqrt m_i)^2 = TrV2 / (TrV)^2.
TrV, TrV2 = sp.symbols('TrV TrV2', positive=True)
Q = TrV2/TrV**2
print("Koide Q = (sum m)/(sum sqrt m)^2 = TrV2/(TrV)^2")
# balance: singlet^2 = doublet^2:  (TrV)^2/3 = TrV2 - (TrV)^2/3  => TrV2 = 2(TrV)^2/3
sol = sp.solve(sp.Eq(TrV**2/3, TrV2 - TrV**2/3), TrV2)[0]
print("balance => TrV2 =", sol, " => Q =", sp.simplify(Q.subs(TrV2, sol)), " <-- should be 2/3")
# singlet:doublet per-STATE equal (doublet/2 = singlet): (TrV2-(TrV)^2/3)/2 = (TrV)^2/3 => TrV2 = (TrV)^2
sol2 = sp.solve(sp.Eq((TrV2-TrV**2/3)/2, TrV**2/3), TrV2)[0]
print("per-state equal => TrV2 =", sol2, " => Q =", sp.simplify(Q.subs(TrV2,sol2)), " <-- should be 1")
