import sympy as sp

# ============================================================
# STEP 1: Laurent / analytic structure of the FREE pullback as
# a function of b near b = c_chi. The "perturbative series" in
# Route B is the free expansion; we ask what its singular data
# at b=c_chi is.
# ============================================================
H, c, b, tau, x = sp.symbols('H c_chi b tau x', positive=True)
# x = c_chi - b  (small parameter; the "coupling" approaches the singular point)

kappa = H/sp.sqrt(1-b**2)
# Free pullback (drop the universal sinh^2 stationary factor; keep b-dependence)
A = H**2/(16*sp.pi**2*c*(c**2 - b**2))   # amplitude prefactor

# --- (1a) Amplitude as a function of x = c - b ---
A_x = A.subs(b, c - x)
A_x = sp.simplify(A_x)
print("A(b=c-x) =", A_x)
ser_A = sp.series(A_x, x, 0, 3)
print("Laurent of A about x=0:", ser_A)

# residue of the simple pole in b at b=c
res = sp.residue(A, b, c)
print("residue_b A at b=c:", sp.simplify(res))

# --- (1b) kappa near b=c : the Deser-Levin sqrt structure ---
kappa_x = kappa.subs(b, c - x)
print("\nkappa(b=c-x) =", sp.simplify(kappa_x))
# u = 2 pi / kappa
u = 2*sp.pi/kappa
u_x = u.subs(b, c - x)
print("u(b=c-x) =", sp.simplify(u_x))
ser_u = sp.series(u_x, x, 0, 2)
print("u about x=0:", ser_u)

# Is u ~ sqrt(x)?  Only if c=1 (luminal). For c=c_chi>1, b->c means b>1, 1-b^2<0.
# CRITICAL CHECK: at b -> c_chi with c_chi>1, what is 1-b^2 ?
print("\n1-b^2 at b=c_chi:", sp.simplify((1-b**2).subs(b,c)))
# kappa = H/sqrt(1-b^2): for b=c_chi>1 this is imaginary. The edge b->c_chi is
# NOT the same as the deep-MOND edge b->1. Record this carefully.
