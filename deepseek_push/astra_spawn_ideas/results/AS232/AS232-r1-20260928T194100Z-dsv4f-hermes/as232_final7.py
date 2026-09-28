# as232_final7.py — AS232 Tier-0b FINAL 2x2 (last iteration; r-space-first pipeline).
# Verified linear gates: lapse EL == E1 (4 cN L0(Phi1-Z1)); shell Phi1=Psi1=-U.
# ELs (exact, measure-included; fixed measure e^Phi(1-2Psi)^{3/2}):
#   E_Phi = Dens - D0[M*(-4 e^-2w D0Phi - 2 e^-2w D0w + 2a inv(D0Phi-D0Z) + 4 inv D0Z)]
#           + L0[M*(-2 e^-2w)]                      (lapse slot; hand IBP)
#   E_Psi = probe in Psi2 with flat-leaf adjoints (r^2 dr): chi''F -> chi(F''+4F'/r+2F/r^2),
#           chi'F -> -chi(F'+2F/r); then chi->1      (spatial slot)
# Window Sk->0; vacuum point mass U = sqrt(GM2)/r (exact rational); ansatz
#   phi2 = A GM2/r^2, psi2 = B GM2/r^2  (A = phi2/U_N^2, B = psi2/U_N^2).
# Pipeline: substitute in r-space -> expand rational -> * r^4 -> r->1/t -> t^0 = 1/r^4 harmonic.
# Gates: G1 linear; G3 alpha=0 => A=0, B=-3/4 (Einstein isotropic); G4 control fires for a!=0.
import sympy as sp
r = sp.symbols('r', positive=True)
GM2, alpha, cN, Sk, ell = sp.symbols('GM2 alpha cN Sk ell', positive=True)
eps = sp.symbols('e', positive=True)
U = sp.Function('U')(r)
Phi1, Psi1 = -U, -U
varphi2, psi2 = sp.Function('varphi2')(r), sp.Function('psi2')(r)
Phi = eps*Phi1 + eps**2*varphi2
Psi = eps*Psi1 + eps**2*psi2
Z  = eps*(ell*Sk*Phi1/4) + eps**2*(ell*Sk*varphi2/4)
Uaux = eps*(Phi1 - ell*Sk*Phi1/4) + eps**2*(varphi2 - ell*Sk*varphi2/4)
def D0(f): return sp.diff(f, r)
def L0(f): return sp.diff(f, r, 2) + sp.Rational(2,1)*sp.diff(f, r)/r
w = sp.log(1 - 2*Psi)/2
R3 = -4*sp.exp(-2*w)*L0(w) - 2*sp.exp(-2*w)*D0(w)**2
Rbar = R3 - 2*sp.exp(-2*w)*(L0(Phi) + D0(Phi)**2 + D0(Phi)*D0(w))
inv = 1/(1 - 2*Psi)
Va = (alpha*inv*(D0(Phi)-D0(Z))**2 + 4*inv*D0(Phi)*D0(Z)
      - 2*inv*D0(Z)**2 - 4*cN*inv*D0(Z)*D0(Uaux))
M = sp.exp(Phi)*(1-2*Psi)**sp.Rational(3,2)
Dens = M*(Rbar + Va)

# ---- lapse EL ----
K1 = M*(-4*sp.exp(-2*w)*D0(Phi) - 2*sp.exp(-2*w)*D0(w)
        + 2*alpha*inv*(D0(Phi)-D0(Z)) + 4*inv*D0(Z))
K2 = M*(-2*sp.exp(-2*w))
E_Phi = sp.expand(sp.series(Dens, eps, 0, 3).removeO()) \
        - sp.expand(sp.series(sp.diff(K1, r), eps, 0, 3).removeO()) \
        + sp.expand(sp.series(L0(K2), eps, 0, 3).removeO())
E_Phi = sp.expand(sp.series(E_Phi, eps, 0, 3).removeO())

# ---- spatial EL (probe; flat-leaf adjoints w.r.t. r^2 dr) ----
chi = sp.Function('chi')(r); s = sp.symbols('s')
PsiP = eps*Psi1 + eps**2*(psi2 + s*chi)
wP = sp.log(1 - 2*PsiP)/2
R3P = -4*sp.exp(-2*wP)*L0(wP) - 2*sp.exp(-2*wP)*D0(wP)**2
RbarP = R3P - 2*sp.exp(-2*wP)*(L0(Phi) + D0(Phi)**2 + D0(Phi)*D0(wP))
invP = 1/(1 - 2*PsiP)
VaP = (alpha*invP*(D0(Phi)-D0(Z))**2 + 4*invP*D0(Phi)*D0(Z)
       - 2*invP*D0(Z)**2 - 4*cN*invP*D0(Z)*D0(Uaux))
MP = sp.exp(Phi)*(1-2*PsiP)**sp.Rational(3,2)
prob = sp.expand(sp.series(sp.diff(MP*(RbarP + VaP), s), s, 0, 2).removeO())
prob = sp.expand(sp.series(prob, eps, 0, 3).removeO())
E_Psi = sp.S.Zero
for term in sp.Add.make_args(sp.expand(prob)):
    if term.has(sp.Derivative(chi, (r, 2))):
        F = sp.simplify(term / sp.Derivative(chi, (r, 2)))
        E_Psi += chi * sp.expand(sp.diff(F, (r, 2)) + 4*sp.diff(F, r)/r + 2*F/r**2)
    elif term.has(sp.Derivative(chi, r)):
        F = sp.simplify(term / sp.Derivative(chi, r))
        E_Psi -= chi * sp.expand(sp.diff(F, r) + 2*F/r)
    elif term.has(chi):
        E_Psi += term
E_Psi = sp.expand(sp.series(E_Psi, eps, 0, 3).removeO()).subs(chi, 1)

# ---- linear gates ----
UP, UPP = sp.Derivative(U, r), sp.Derivative(U, (r, 2))
E1o = sp.expand(4*cN*L0(Phi1 - ell*Sk*Phi1/4))
def linsubs(f):
    return sp.expand(f.coeff(eps, 1).subs(Sk, 0).replace(UPP, 0).replace(UP, 0).replace(U, 0))
g1 = sp.simplify(linsubs(E_Phi) - linsubs(E1o))
g1s = sp.simplify(linsubs(E_Psi))
print("G1 lapse linear:", g1, " | G1s shell linear:", g1s)
assert g1 == 0

# ---- r-space substitution (window first), expand rational ----
GM = sp.sqrt(GM2)
A, B = sp.symbols('A B')
def reduce_EL(f):
    f = sp.expand(f.subs(Sk, 0))
    submap = {sp.Derivative(varphi2, (r,2)): 6*A*GM2/r**4,
              sp.Derivative(psi2, (r,2)):   6*B*GM2/r**4,
              sp.Derivative(varphi2, r):    -2*A*GM2/r**3,
              sp.Derivative(psi2, r):       -2*B*GM2/r**3,
              sp.Derivative(varphi2, (r,3)): -24*A*GM2/r**5,
              sp.Derivative(psi2, (r,3)):    -24*B*GM2/r**5,
              varphi2: A*GM2/r**2,  psi2: B*GM2/r**2,
              UPP: 2*GM/r**3,  UP: -GM/r**2,  U: GM/r}
    f = sp.expand(f.subs(submap, simultaneous=True))
    f = sp.expand(f).replace(GM**2, GM2).replace(GM, 0)
    return sp.expand(f)
E2l = reduce_EL(sp.expand(E_Phi.coeff(eps, 2)))
E2s = reduce_EL(sp.expand(E_Psi.coeff(eps, 2)))
# ---- multiply r^4, then t^0 extraction ----
t = sp.symbols('t', positive=True)
def harm4(f):
    f = sp.expand(f * r**4)
    f = sp.expand(f.replace(r, 1/t))
    f = sp.expand(sp.series(f, t, 0, 1).removeO())
    return sp.simplify(f)
hl = harm4(E2l); hs = harm4(E2s)
print("lapse eq (1/r^4):", hl)
print("spatial eq (1/r^4):", hs)
# polynomial in A, B:
Pl = sp.expand(sp.together(hl)); Ps = sp.expand(sp.together(hs))
plA = sp.expand(sp.Poly(Pl, A, B).coeff_monomial(A)); plB = sp.expand(sp.Poly(Pl, A, B).coeff_monomial(B))
plC = sp.expand(Pl.subs({A: 0, B: 0}))
psA = sp.expand(sp.Poly(Ps, A, B).coeff_monomial(A)); psB = sp.expand(sp.Poly(Ps, A, B).coeff_monomial(B))
psC = sp.expand(Ps.subs({A: 0, B: 0}))
print("lapse:  A*%s + B*%s + %s = 0" % (sp.simplify(plA), sp.simplify(plB), sp.simplify(plC)))
print("spatial:A*%s + B*%s + %s = 0" % (sp.simplify(psA), sp.simplify(psB), sp.simplify(psC)))
sol = sp.solve([Pl, Ps], [A, B], dict=True)
print("solution:", sol)
if sol:
    As = sp.simplify(sol[0][A]); Bs = sp.simplify(sol[0][B])
    print("A = phi2/U_N^2 =", As, " B = psi2/U_N^2 =", Bs)
    print("BETA = 1 + phi2/U_N^2 =", sp.simplify(1 + As))
    print("residuals:", sp.simplify(sp.expand(Pl.subs({A: As, B: Bs}))),
          sp.simplify(sp.expand(Ps.subs({A: As, B: Bs}))))
    A0 = sp.simplify(As.subs(alpha, 0)); B0 = sp.simplify(Bs.subs(alpha, 0))
    print("G3 alpha=0: A0 =", A0, " B0 =", B0, " [expect 0, -3/4]")
    cB = sp.simplify(sp.expand(Ps.subs({A: 0, B: -sp.Rational(3,4)})))
    cA = sp.simplify(sp.expand(Pl.subs({A: 0, B: -sp.Rational(3,4)})))
    print("G4 neg control (A=0,B=-3/4): spatial", cB, " lapse", cA)
    print("   alpha=0:", sp.simplify(cB.subs(alpha, 0)), sp.simplify(cA.subs(alpha, 0)))
else:
    print("no solution; equations:", Pl, Ps)
with open('as232_final7_out.txt', 'w') as f:
    f.write(f"lapse_eq = {Pl}\nspatial_eq = {Ps}\nsol = {sol}\n"
            f"BETA = {sp.simplify(1+As) if sol else 'nan'}\n"
            f"G3 = {A0 if sol else '?'} {B0 if sol else '?'}\n"
            f"G4 = {cB if sol else '?'} {cA if sol else '?'}\n")