import sympy as sp

print("="*78)
print("SKEPTIC VERIFY: the prior agent's c_s^2 sign-by-branch for K(Q)=mu^2(Q-1)^2")
print("="*78)

Q, mu, dQ = sp.symbols('Q mu dQ', real=True)
K = mu**2*(Q-1)**2
Kp = sp.diff(K,Q)
Kpp = sp.diff(K,Q,2)

# Prior agent's formula: c_s^2 = K'/(K'+2 Q K'')  [k-essence form with Q as the kinetic var]
cs2 = Kp/(Kp + 2*Q*Kpp)
cs2 = sp.simplify(cs2)
print("\n[A] c_s^2 = K'/(K'+2 Q K'') treating Q as the kinetic variable (prior agent):")
print("    c_s^2(Q) =", cs2)
cs2_dQ = sp.simplify(cs2.subs(Q, 1+dQ))
print("    c_s^2(dQ=Q-1) =", cs2_dQ)
print("    matches prior's dQ/(3dQ+2)?", sp.simplify(cs2_dQ - dQ/(3*dQ+2))==0)
print("\n  sign check (prior formula):")
for v in [0.1, -0.1, 0.5, -0.5]:
    print(f"    dQ={v:+.2f} -> c_s^2 = {float(cs2_dQ.subs(dQ,v)):+.4f}")

print("\n" + "="*78)
print("[B] CRITICAL CONVENTION CHECK: is c_s^2=K'/(K'+2QK'') the right formula here?")
print("="*78)
print("""
 Standard k-essence: c_s^2 = P_X/(P_X+2X P_XX), X=(1/2)(dphi)^2, P=P(X).
 AeST/khronon Q = A^mu d_mu phi is LINEAR in dphi (X = Q^2/2 in the rest frame).
 So the formula must be applied to P(X):=K(Q(X)) with Q=sqrt(2X), NOT to K(Q)
 with 'Q' textually substituted for 'X'.
""")
X = sp.symbols('X', positive=True)
Q_of_X = sp.sqrt(2*X)
P_of_X = sp.simplify(K.subs(Q, Q_of_X))
print("  P(X) = K(Q=sqrt(2X)) =", P_of_X)
PX  = sp.diff(P_of_X, X)
PXX = sp.diff(P_of_X, X, 2)
cs2_correct = sp.simplify(PX/(PX + 2*X*PXX))
print("  c_s^2_correct = P_X/(P_X+2X P_XX) =", cs2_correct)
cs2_correct_Q = sp.simplify(cs2_correct.subs(X, Q**2/2))
print("  in Q (X=Q^2/2):", cs2_correct_Q)
cs2_correct_dQ = sp.simplify(cs2_correct_Q.subs(Q,1+dQ))
print("  in dQ:", sp.simplify(cs2_correct_dQ))
print("\n  sign check (CORRECT k-essence formula via P(X)):")
for v in [0.1, -0.1, 0.5, -0.5, -0.9]:
    val = cs2_correct_dQ.subs(dQ, v)
    print(f"    dQ={v:+.2f} -> c_s^2 = {float(val):+.4f}")
