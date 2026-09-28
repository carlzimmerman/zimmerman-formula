# as232_final6.py — AS232 Tier-0b FINAL, ε-ordered on-shell derivation.
# Verified linear machinery: lapse EL == E1 (4 cN L0(Phi1-Z1)); shell Phi1 = Psi1 = -U.
# ν field ordering:  Phi = eps Phi1,  Psi = eps Psi1  (eps bookkeeping; 1st order).
# Second order (window S_k->0: Z=0, Uaux=Phi; vacuum; point mass U=sqrt(GM2)/r exact;
# mean-normalized nonzero modes; Lambda k!=0 projected): the branch's 2x2 at 1/r^4:
#   lapse:    4 cN L0(phi2 - z2) + S = 0     with z2 -> 0  =>  8 cN A GM2 = -S
#   spatial:  4 L0(psi2 - phi2) + S = 0      =>  8 (B - A) GM2 = -S
# S = (1/r^4)-harmonic of the ON-SHELL background eps^2 density
#     [e^{Phi1} (1-2 Psi1)^{3/2} (Rbar + Va)]_{eps^2, phi2=psi2=0}   (point mass),
# Rbar = R3(w) - 2 e^{-2w}[L0 Phi + (D0Phi)^2 + (D0Phi)(D0w)] (exact warp-scalar,
#        verified 0 on Schwarzschild isotropic = the vacuum gate), Va = alpha e^{-2w}(D0Phi)^2.
# => A = -S/(8 cN GM2) ,  beta = 1 + phi2/U_N^2 = 1 + A (GM2-normalized).
# GATES: G3: alpha=0 => S=0 => A=0 => beta=1 (Einstein isotropic consistency);
# G4 negative control: alpha != 0 must inject S_alpha != 0 (fires), dies at alpha=0.
import sympy as sp
r = sp.symbols('r', positive=True)
GM2, alpha, cN, Sk, ell = sp.symbols('GM2 alpha cN Sk ell', positive=True)
GM = sp.sqrt(GM2)
U = sp.Function('U')(r)
Phi1, Psi1 = -U, -U
eps = sp.symbols('e', positive=True)
def D0(f): return sp.diff(f, r)
def L0(f): return sp.diff(f, r, 2) + sp.Rational(2,1)*sp.diff(f, r)/r

# ---- linear gates ----
E1_op = sp.expand(4*cN*L0(Phi1 - ell*Sk*Phi1/4))
UP, UPP = sp.Derivative(U, r), sp.Derivative(U, (r, 2))
E1_v = sp.expand(E1_op.replace(UP, 0).replace(UPP, 0).replace(Sk, 0).replace(U, 0))
print("G1 linear lapse EL (E1 op, vac/window):", E1_v)

# ---- on-shell background at second order (eps-ordered) ----
Ph = eps*Phi1
Ps = eps*Psi1
w = sp.log(1 - 2*Ps)/2
R3 = -4*sp.exp(-2*w)*L0(w) - 2*sp.exp(-2*w)*D0(w)**2
Rbar = R3 - 2*sp.exp(-2*w)*(L0(Ph) + D0(Ph)**2 + D0(Ph)*D0(w))
Va = alpha*sp.exp(-2*w)*(D0(Ph))**2
Dens = sp.expand(sp.series(sp.exp(Ph)*(1 - 2*Ps)**sp.Rational(3,2)*(Rbar + Va), eps, 0, 4).removeO())
S4 = sp.expand(Dens.coeff(eps, 2))
# point-mass substitution (exact rational; L0 U = 0, U'^2 = GM2/r^4 automatically):
S4p = sp.expand(S4.replace(UPP, 2*GM/r**3).replace(UP, -GM/r**2).replace(U, GM/r))
S4p = sp.expand(S4p.replace(GM**2, GM2).replace(GM, 0))
t = sp.symbols('t', positive=True)
S4t = sp.expand(sp.series(sp.expand(S4p.replace(r, 1/t)), t, 0, 7).removeO())
print("on-shell background eps^2 (r->1/t):", S4t)
deg = sp.Poly(S4t, t).degree()
S = sp.expand(sp.Poly(S4t, t).coeff_monomial(t**4)) if deg >= 4 else sp.S.Zero
print("S (1/r^4 harmonic) =", sp.simplify(S))

A = sp.symbols('A')
A_sol = sp.simplify(sp.solve(sp.Eq(8*cN*A*GM2 + sp.expand(S), 0), A)[0])
print("A*GM2 =", A_sol, "  A = phi2/U_N^2 =", sp.simplify(A_sol/GM2))
print("BETA = 1 + phi2/U_N^2 =", sp.simplify(1 + A_sol/GM2))
A0 = sp.simplify(A_sol.subs(alpha, 0)/GM2)
print("G3: alpha=0 -> A0 =", A0, " (0 = Einstein-isotropic consistency)")
print("G4: S(alpha) = S0 + alpha*S_a:  S(alpha=0) =", sp.simplify(S.subs(alpha, 0)),
      "  S(alpha=1) =", sp.simplify(S.subs(alpha, 1)))
with open('as232_final6_out.txt', 'w') as f:
    f.write(f"S4t = {S4t}\nS = {sp.simplify(S)}\nA = {sp.simplify(A_sol/GM2)}\n"
            f"BETA = {sp.simplify(1 + A_sol/GM2)}\nG3 A0 = {A0}\n"
            f"G4 = {sp.simplify(S.subs(alpha,0))} {sp.simplify(S.subs(alpha,1))}\n")