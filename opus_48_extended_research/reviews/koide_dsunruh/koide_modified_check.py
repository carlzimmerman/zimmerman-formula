import sympy as sp

# ============================================================
# Liang-Sun 2020 (arXiv:2007.05878) — the COMPLETE-potential result.
# Eq(41): the MODIFIED Koide formula when ALL SU(3)-invariant terms are kept.
# K = (2/3)*(1 - (a0+2*a02-18*a4)/(2*(a0+2*a02-3*a2)))
# Question: is K=2/3 generic, or does it require tuning a parameter relation?
# ============================================================
a0, a02, a2, a4 = sp.symbols('a0 a02 a2 a4', real=True)

K = sp.Rational(2,3)*(1 - (a0 + 2*a02 - 18*a4)/(2*(a0 + 2*a02 - 3*a2)))
K = sp.simplify(K)
print("Eq(41) K =", K)

# K = 2/3 requires the numerator-shift to vanish:
cond = sp.solve(sp.Eq(K, sp.Rational(2,3)), a4)
print("K = 2/3  <=>  a4 =", cond, "  i.e.  a0 + 2*a02 - 18*a4 = 0  =>  a4=(a0+2a02)/18")
print("  => exact 2/3 is a CODIMENSION-1 (tuned) surface in the parameter space, NOT generic.\n")

# Confirm K sweeps a continuous range as the free params vary -> can fit up-quarks 8/9, etc.
import random
vals = []
for _ in range(8):
    s = {a0: random.uniform(-2,2), a02: random.uniform(-2,2),
         a2: random.uniform(-2,2), a4: random.uniform(-2,2)}
    try:
        vals.append(float(K.subs(s)))
    except Exception:
        pass
print("Sample K over random params (continuous, fits any sector):")
print(" ", [round(v,3) for v in vals])

# Up-quark Koide ~ 8/9; show it's just another point on the same family:
sol_up = sp.solve(sp.Eq(K, sp.Rational(8,9)), a4)
print("\nK = 8/9 (up-quarks) <=> a4 =", sol_up, " -> SAME family, different tuned point.")

# ============================================================
# VERDICT logic: Koide 0811.3470 got 'parameter-free 2/3' ONLY by DROPPING
# symmetry-allowed terms (keeping only Phi_hat^3 via Z2/U(1)_X engineering),
# which forced xi=-3. Liang-Sun keep ALL terms -> 2/3 is non-generic (tuned a4).
# So NO radiative/Yukawaon model FORCES r=sqrt2; they ENGINEER the term subset
# that yields it, or PROTECT a 2/3 imposed at tree level (Sumino).
# ============================================================
print("\n--- KNIFE 1 verdict: ASSUMES/ENGINEERS, does NOT force r=sqrt2 ---")
