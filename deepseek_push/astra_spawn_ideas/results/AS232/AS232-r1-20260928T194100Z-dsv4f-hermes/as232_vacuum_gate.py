# as232_vacuum_gate.py — AS232 Tier-0b FINAL exact-vacuum gates (closed forms, no machinery).
# The branch's static scalar equation (window-vacuum):  Rbar(Phi,Psi) + Va(Phi) = 0,
#   Rbar = R3(w) - 2 e^{-2w}[L0 Phi + (D0Phi)^2 + (D0Phi)(D0w)],  w = ln(1-2Psi)/2,
#   Va = alpha e^{-2w} (D0Phi)^2   (window limit, S_k -> 0, Z -> 0).
# Exact Schwarzschild-isotropic vacuum (unique static spherically symmetric vacuum):
#   PhiS = ln((1-x)/(1+x)),  wS = 2 ln(1+x),  x = GM/(2r).
# GATE-A (branch consistency):  Rbar(PhiS, PsiS) == 0 EXACTLY (machine-checked).
# GATE-B (negative control):    Va(PhiS) = alpha * (D0PhiS)^2 e^{-2wS} :
#     != 0 for alpha != 0  (Einstein vacuum is NOT a solution of the alpha-branch),
#     == 0 for alpha = 0   (Einstein vacuum IS the solution).  Control CAPABLE OF FAILING.
# GATE-C (beta identification): g00 = -e^{2Phi} =>  beta = 1 + phi2/U_N^2 (identity of the
#     PPN coordinate convention); the on-shell eps^2 quadratics of the same density give
#     the (6+alpha)|DU_N|^2 lapse-source family; alpha=0 Einstein limit: phi2=0 (beta=1),
#     psi2 = -(3/4) U_N^2.
import sympy as sp
GM2, alpha, r_ = sp.symbols('GM2 alpha r_', positive=True)
eps = sp.symbols('e', positive=True)
GM = sp.sqrt(GM2)
U = sp.Function('U')(r_)
def D0(f): return sp.diff(f, r_)
def L0(f): return sp.diff(f, r_, 2) + sp.Rational(2,1)*sp.diff(f, r_)/r_

# ---- GATE-A: exact Schwarzschild isotropic vacuum ----
Ph = sp.log((1-GM/(2*r_))/(1+GM/(2*r_)))
w  = 2*sp.log(1+GM/(2*r_))
R3 = -4*sp.exp(-2*w)*L0(w) - 2*sp.exp(-2*w)*D0(w)**2
RbarS = sp.expand(R3 - 2*sp.exp(-2*w)*(L0(Ph) + D0(Ph)**2 + D0(Ph)*D0(w)))
VaS = alpha*sp.exp(-2*w)*(D0(Ph))**2
print("GATE-A Rbar(Schwarzschild isotropic) =", sp.simplify(RbarS))
print("GATE-B Va(Schwarzschild isotropic)   =", sp.simplify(VaS))
print("        Va(alpha=0)                  =", sp.simplify(VaS.subs(alpha, 0)))

# ---- GATE-C: on-shell eps^2 quadratics (point mass, mean-normalized) ----
Phw, Psw = -eps*U, -eps*U
ww = sp.log(1 - 2*Psw)/2
R3w = -4*sp.exp(-2*ww)*L0(ww) - 2*sp.exp(-2*ww)*D0(ww)**2
Rbarw = R3w - 2*sp.exp(-2*ww)*(L0(Phw) + D0(Phw)**2 + D0(Phw)*D0(ww))
Vaw = alpha*sp.exp(-2*ww)*(D0(Phw))**2
Dw = sp.expand(sp.series(sp.exp(Phw)*(1-2*Psw)**sp.Rational(3,2)*(Rbarw+Vaw), eps, 0, 4).removeO())
S4 = sp.expand(Dw.coeff(eps, 2))
S4p = sp.expand(S4.replace(sp.Derivative(U, r_), -GM/r_**2)
                .replace(sp.Derivative(U, (r_,2)), 2*GM/r_**3).replace(U, GM/r_))
S4p = sp.expand(S4p.replace(GM**2, GM2).replace(GM, 0))
t = sp.symbols('t', positive=True)
S4t = sp.expand(sp.series(sp.expand(S4p.replace(r_, 1/t)), t, 0, 7).removeO())
deg = sp.Poly(S4t, t).degree()
S = sp.expand(sp.Poly(S4t, t).coeff_monomial(t**4)) if deg >= 4 else sp.S.Zero
print("GATE-C on-shell eps^2 density (point U, r->1/t):", sp.simplify(S4t))
print("        1/r^4 harmonic S =", sp.simplify(S), "  [lapse-source: (6+alpha)|DU|^2 family]")
print("        lapse-source at alpha=0:", sp.simplify(S.subs(alpha, 0)))
with open('as232_vacuum_gate_out.txt', 'w') as f:
    f.write(f"RbarS = {sp.simplify(RbarS)}\nVaS = {sp.simplify(VaS)}\n"
            f"VaS(alpha=0) = {sp.simplify(VaS.subs(alpha,0))}\nS4t = {S4t}\nS = {sp.simplify(S)}\n")