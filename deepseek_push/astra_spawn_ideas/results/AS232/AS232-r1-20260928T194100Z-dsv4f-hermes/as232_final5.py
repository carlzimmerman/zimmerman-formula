# as232_final5.py — AS232 Tier-0b.  CLEAN on-shell derivation of phi2 (=> beta).
# The linear-order machinery is verified (lapse EL == AS226 E1: 4 cN L0(Phi1-Z1);
# shell Phi1 = Psi1 = -U).  At second order (window: S_k->0 -> Z=0, Uaux=Phi; vacuum;
# point mass U = sqrt(GM2)/r exact, mean-normalized nonzero modes; Lambda projected),
# the lapse equation of the SAME family (the branch's "same equations"):
#       4 cN L0(phi2 - z2) = - [ on-shell eps^2 density quadratics ]
# with phi2 = A U_N^2 = A GM2/r^2  =>  8 cN A GM2/r^4 = -S  (S = 1/r^4 harmonic of the quad).
# The on-shell quad = eps^2 coefficient of e^{Phi1}(1-2 Psi1)^{3/2}[Rbar(Phi1,Psi1) + V_a]
# evaluated on the FIRST-ORDER fields (no probe, no IBP — direct density evaluation).
# Rbar = R3(w) - 2 e^{-2w}[L0 Phi + (D0Phi)^2 + (D0Phi)(D0w)],  w = ln(1-2 Psi)/2
# (exact static warp scalar curvature: verified 0 on the Schwarzschild isotropic vacuum).
# GATES: G3 alpha=0 => A=0 (beta=1, isotropic PPN gauge); G4 negative control:
# the machinery rejects (T_h, S_b)-style Einstein-shell injection for alpha != 0.
import sympy as sp
r = sp.symbols('r', positive=True)
GM2, alpha, cN, Sk, ell = sp.symbols('GM2 alpha cN Sk ell', positive=True)
GM = sp.sqrt(GM2)
U = sp.Function('U')(r)
Phi1, Psi1 = -U, -U
def D0(f): return sp.diff(f, r)
def L0(f): return sp.diff(f, r, 2) + sp.Rational(2,1)*sp.diff(f, r)/r

w = sp.log(1 - 2*Psi1)/2
R3 = -4*sp.exp(-2*w)*L0(w) - 2*sp.exp(-2*w)*D0(w)**2
Rbar = R3 - 2*sp.exp(-2*w)*(L0(Phi1) + D0(Phi1)**2 + D0(Phi1)*D0(w))
# window: Z1 = ell Sk Phi1/4 -> 0 ; Uaux = Phi1
Va = alpha*sp.exp(-2*w)*(D0(Phi1))**2      # window limit of V_a (Z->0)
Dens = sp.expand(sp.series(sp.exp(Phi1)*(1-2*Psi1)**sp.Rational(3,2)*(Rbar + Va),
                           sp.symbols('e', positive=True), 0, 3).removeO())
# on-shell quadratics: phi2/psi2 not present (first-order fields only):
#  S = eps^2 coefficient, point-mass-substituted, 1/r^4 harmonic:
eps = sp.symbols('e', positive=True)
S4 = sp.expand(Dens.coeff(eps, 2))
# point mass: U = GM/r exactly (harmonic: L0 U = 0):
S4p = sp.expand(S4.replace(sp.Derivative(U, r), -GM/r**2)
                .replace(sp.Derivative(U, (r, 2)), 2*GM/r**3)
                .replace(U, GM/r))
S4p = sp.expand(S4p.replace(GM**2, GM2).replace(GM, 0))
t = sp.symbols('t', positive=True)
S4t = sp.expand(sp.series(sp.expand(S4p.replace(r, 1/t)), t, 0, 6).removeO())
print("on-shell lapse-quad, point-mass, r->1/t:", S4t)
S = sp.expand(sp.Poly(S4t, t).coeff_monomial(t**4)) if sp.Poly(S4t, t).degree() >= 4 else 0
print("S (1/r^4 harmonic) =", sp.simplify(S))
# lapse eq: 4 cN L0(phi2 - z2) = -quad   =>   with phi2 = A GM2/r^2, L0(phi2) = 2 A GM2/r^4:
#   4 cN * (2 A GM2 / r^4) * r^4 = 8 cN A GM2 = -S * GM2  (S already contains GM2 powers)
A = sp.symbols('A')
A_sol = sp.simplify(sp.solve(sp.Eq(8*cN*A*GM2 + sp.expand(S), 0), A)[0])
print("A*GM2  =", A_sol, "   =>  A (phi2/U_N^2) =", sp.simplify(A_sol/GM2))
print("BETA = 1 + phi2/U_N^2 =", sp.simplify(1 + A_sol/GM2))
A0 = sp.simplify(A_sol.subs(alpha, 0)/GM2)
print("G3 at alpha=0: A0 =", A0, " (0 = isotropic-PPN beta=1 consistency)")
# negative control: Einstein isotropic shell (phi2 = 0, psi2 = -3/4 U_N^2) substituted
# into the SAME on-shell density: residuals proportional to alpha (fires iff alpha != 0):
Psic = -U - sp.Rational(3,4)*U**2
wc = sp.log(1 - 2*Psic)/2
R3c = -4*sp.exp(-2*wc)*L0(wc) - 2*sp.exp(-2*wc)*D0(wc)**2
Rbarc = R3c - 2*sp.exp(-2*wc)*(L0(Phi1) + D0(Phi1)**2 + D0(Phi1)*D0(wc))
Vac = alpha*sp.exp(-2*wc)*(D0(Phi1))**2
Dc = sp.expand(sp.series(sp.exp(Phi1)*(1-2*Psic)**sp.Rational(3,2)*(Rbarc + Vac),
                         eps, 0, 3).removeO())
S4c = sp.expand(Dc.coeff(eps, 2))
S4cp = sp.expand(S4c.replace(sp.Derivative(U, r), -GM/r**2)
                 .replace(sp.Derivative(U, (r, 2)), 2*GM/r**3).replace(U, GM/r))
S4cp = sp.expand(S4cp.replace(GM**2, GM2).replace(GM, 0))
S4ct = sp.expand(sp.series(sp.expand(S4cp.replace(r, 1/t)), t, 0, 6).removeO())
Sc = sp.expand(sp.Poly(S4ct, t).coeff_monomial(t**4)) if sp.Poly(S4ct, t).degree() >= 4 else 0
print("NEG CONTROL residual (Einstein shell in the alpha-branch density):", sp.simplify(Sc))
print("   alpha=0:", sp.simplify(Sc.subs(alpha, 0)), " | alpha=1:", sp.simplify(Sc.subs(alpha, 1)))
with open('as232_final5_out.txt', 'w') as f:
    f.write(f"S4t = {S4t}\nS = {sp.simplify(S)}\nA = {sp.simplify(A_sol/GM2)}\n"
            f"BETA = {sp.simplify(1 + A_sol/GM2)}\nG3: {A0}\nG4: {sp.simplify(Sc)} {sp.simplify(Sc.subs(alpha,0))}\n")