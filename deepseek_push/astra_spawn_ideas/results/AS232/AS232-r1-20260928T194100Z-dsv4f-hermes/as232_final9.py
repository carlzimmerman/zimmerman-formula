# as232_final9.py — AS232 Tier-0b FINAL: EXACT second-order Euler-Lagrange.
# Action density for the static warped ansatz, spherical measure r^2 dr:
#   S = ∫ Dens r^2 dr,  Dens = e^{Phi}(1-2 Psi)^{3/2} [ Rbar + Va ]
#   Rbar = R3(w) - 2 e^{-2w}[ L0 Phi + (D0 Phi)^2 + (D0 Phi)(D0 w) ],  w = ln(1-2 Psi)/2
#   R3(w) = -4 e^{-2w} L0(w) - 2 e^{-2w} (D0 w)^2
#   Va    = alpha e^{-2w}(D0 Phi - D0 Z)^2 + 4 e^{-2w} D0 Phi D0 Z - 2 e^{-2w}(D0 Z)^2
#           - 4 cN e^{-2w} D0 Z D0(Uaux);  Z = (ell Sk/4) Phi, Uaux = Phi - Z   [window]
# EXACT EL (second-order Lagrangian in 1 radial variable, measure r^2 dr):
#   E = ∂(r^2 Dens)/∂f - d/dr[∂(r^2 Dens)/∂f'] + d^2/dr^2[∂(r^2 Dens)/∂f'']
# No probes, no hand IBP.  ε² coefficient on the point-mass ansatz
#   Phi = -e U + e^2 A GM2/r^2,  Psi = -e U + e^2 B GM2/r^2,  U = sqrt(GM2)/r,
# window Sk -> 0; leading 1/r^4 harmonic (t^4 coefficient after r -> 1/t).
# GATES: G1 linear lapse == E1 (AS226); G1s shell; G3 alpha=0 => A=0,B=-3/4; G4 control.
import sympy as sp
r = sp.symbols('r', positive=True)
GM2, alpha, cN, Sk, ell = sp.symbols('GM2 alpha cN Sk ell', positive=True)
eps = sp.symbols('e', positive=True)
GM = sp.sqrt(GM2)
U = sp.Function('U')(r)
def D0(f): return sp.diff(f, r)
def L0(f): return sp.diff(f, r, 2) + sp.Rational(2,1)*sp.diff(f, r)/r

def build(PhiX, PsiX, ZX, UauxX):
    w = sp.log(1 - 2*PsiX)/2
    R3 = -4*sp.exp(-2*w)*L0(w) - 2*sp.exp(-2*w)*D0(w)**2
    Rbar = R3 - 2*sp.exp(-2*w)*(L0(PhiX) + D0(PhiX)**2 + D0(PhiX)*D0(w))
    iv = 1/(1 - 2*PsiX)
    Va = (alpha*iv*(D0(PhiX)-D0(ZX))**2 + 4*iv*D0(PhiX)*D0(ZX)
          - 2*iv*D0(ZX)**2 - 4*cN*iv*D0(ZX)*D0(UauxX))
    return sp.expand(sp.exp(PhiX)*(1-2*PsiX)**sp.Rational(3,2)*(Rbar + Va))

phi2 = sp.Function('phi2')(r); psi2 = sp.Function('psi2')(r)
Phi = -eps*U + eps**2*phi2
Psi = -eps*U + eps**2*psi2
Z  = (ell*Sk/4)*Phi
Uaux = Phi - Z
A, B = sp.symbols('A B')

def exact_EL(Dens, f, order):
    # f = applied function symbol (phi2(r) or psi2(r)); U(r) is fixed background.
    f1, f2 = sp.diff(f, r), sp.diff(f, (r, 2))
    Fsym = f.func
    L = sp.expand(r**2 * Dens)
    E = sp.diff(L, f) - sp.diff(sp.diff(L, f1), r) + sp.diff(sp.diff(L, f2), (r, 2))
    E = sp.expand(sp.series(E, eps, 0, 4).removeO())
    E = sp.expand(E.coeff(eps, order))
    E = sp.expand(E.subs(Sk, 0))
    submap = {sp.Derivative(Fsym(r), (r,4)): 120*(A if Fsym is sp.Function('phi2') else B)*GM2/r**6,
              sp.Derivative(Fsym(r), (r,3)): -24*(A if Fsym is sp.Function('phi2') else B)*GM2/r**5,
              sp.Derivative(Fsym(r), (r,2)): 6*(A if Fsym is sp.Function('phi2') else B)*GM2/r**4,
              sp.Derivative(Fsym(r), r):     -2*(A if Fsym is sp.Function('phi2') else B)*GM2/r**3,
              Fsym(r): (A if Fsym is sp.Function('phi2') else B)*GM2/r**2,
              sp.Derivative(U, (r,2)): 2*GM/r**3,
              sp.Derivative(U, r):     -GM/r**2,
              U: GM/r}
    E = sp.expand(E.subs(submap, simultaneous=True))
    E = sp.expand(E).replace(GM**2, GM2).replace(GM, 0)
    return sp.expand(E)

Dens = build(Phi, Psi, Z, Uaux)
E_Phi = exact_EL(Dens, phi2, 1)   # linear (gate)
E2_Phi = exact_EL(Dens, phi2, 2)
E2_Psi = exact_EL(Dens, psi2, 2)

# linear gates
E1o = sp.expand(4*cN*L0(-U - (ell*Sk/4)*(-U)))
UP, UPP = sp.Derivative(U, r), sp.Derivative(U, (r, 2))
def linsubs(f):
    return sp.expand(f.replace(UPP, 0).replace(UP, 0).replace(U, 0))
g1 = sp.simplify(sp.expand(linsubs(E_Phi) - E1o.replace(UPP,0).replace(UP,0).replace(U,0).replace(Sk,0)))
print("G1 lapse linear (EL - E1, vac/window):", g1)
assert g1 == 0

def harm4(f):
    t = sp.symbols('t', positive=True)
    f = sp.expand(f * r**4)
    f = sp.expand(f.replace(r, 1/t))
    f = sp.expand(sp.series(f, t, 0, 5).removeO())
    p = sp.Poly(f, t)
    return sp.simplify(p.coeff_monomial(t**4)) if p.degree() >= 4 else sp.S.Zero

hl = harm4(E2_Phi); hs = harm4(E2_Psi)
Pl = sp.expand(sp.together(hl)); Ps = sp.expand(sp.together(hs))
print("lapse eq   (1/r^4):", Pl)
print("spatial eq (1/r^4):", Ps)
sol = sp.solve([Pl, Ps], [A, B], dict=True)
print("solution:", sol)
if sol:
    As, Bs = sp.simplify(sol[0][A]), sp.simplify(sol[0][B])
    print("A = phi2/U_N^2 =", As, "  B = psi2/U_N^2 =", Bs)
    print("BETA = 1 + phi2/U_N^2 =", sp.simplify(1 + As))
    print("residuals:", sp.simplify(Pl.subs({A: As, B: Bs})), sp.simplify(Ps.subs({A: As, B: Bs})))
    A0, B0 = sp.simplify(As.subs(alpha, 0)), sp.simplify(Bs.subs(alpha, 0))
    print("G3 alpha=0: A0 =", A0, " B0 =", B0, " [expect 0, -3/4]")
    cA = sp.simplify(Pl.subs({A: 0, B: -sp.Rational(3,4)}))
    cB = sp.simplify(Ps.subs({A: 0, B: -sp.Rational(3,4)}))
    print("G4 neg control (A=0, B=-3/4): lapse", cA, " spatial", cB,
          " | alpha=0:", sp.simplify(cA.subs(alpha,0)), sp.simplify(cB.subs(alpha,0)))
with open('as232_final9_out.txt', 'w') as f:
    f.write(f"Pl = {Pl}\nPs = {Ps}\nsol = {sol}\nBETA = {sp.simplify(1+As) if sol else 'nan'}\n"
            f"G3 = {A0 if sol else '?'} {B0 if sol else '?'}\n"
            f"G4 = {cA if sol else '?'} {cB if sol else '?'}\n")