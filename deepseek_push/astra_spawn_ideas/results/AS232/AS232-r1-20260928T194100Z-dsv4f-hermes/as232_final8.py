# as232_final8.py — AS232 Tier-0b: BOTH ELs from the identical functional probe of
#   Dens = e^{Phi}(1-2 Psi)^{3/2} [Rbar + Va]
#   Rbar = R3(w) - 2 e^{-2w}[L0 Phi + (D0 Phi)^2 + (D0 Phi)(D0 w)],  w = ln(1-2 Psi)/2,
#   Va window limit: alpha e^{-2w} (D0 Phi - D0 Z)^2 + 4...-terms (Z -> 0 kept symbolic then
#   window: S_k -> 0).  Lapse probe: Phi -> Phi + s chi (chi genuine Function); Psi fixed.
#   Spatial probe: Psi -> Psi + s chi.  IBP flat-leaf adjoints (measure r^2 dr, interior;
#   boundary = AS143 declared business):  chi''F -> chi(F''+4F'/r+2F/r^2), chi'F -> -chi(F'+2F/r).
#   The ε² coefficients in the point-mass ansatz phi2=A GM2/r^2, psi2=B GM2/r^2 then solve.
#   Linear gates asserted: lapse == E1 (AS226: 4 cN L0(Phi1-Z1)); shell Psi1 = Phi1.
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
def Dens_of(PhiX, PsiX, ZX, UaX):
    w = sp.log(1 - 2*PsiX)/2
    R3 = -4*sp.exp(-2*w)*L0(w) - 2*sp.exp(-2*w)*D0(w)**2
    Rbar = R3 - 2*sp.exp(-2*w)*(L0(PhiX) + D0(PhiX)**2 + D0(PhiX)*D0(w))
    iv = 1/(1 - 2*PsiX)
    Va = (alpha*iv*(D0(PhiX)-D0(ZX))**2 + 4*iv*D0(PhiX)*D0(ZX)
          - 2*iv*D0(ZX)**2 - 4*cN*iv*D0(ZX)*D0(UaX))
    return sp.expand(sp.series(sp.exp(PhiX)*(1-2*PsiX)**sp.Rational(3,2)*(Rbar + Va),
                               eps, 0, 4).removeO())

def probe_EL(field_probe, other):
    chi = sp.Function('chi')(r); s = sp.symbols('s')
    prob = sp.expand(sp.series(sp.diff(field_probe(other, chi, s), s), s, 0, 2).removeO())
    prob = sp.expand(sp.series(prob, eps, 0, 3).removeO())
    E = sp.S.Zero
    for term in sp.Add.make_args(sp.expand(prob)):
        if term.has(sp.Derivative(chi, (r, 2))):
            F = sp.simplify(term / sp.Derivative(chi, (r, 2)))
            E += chi * sp.expand(sp.diff(F, (r, 2)) + 4*sp.diff(F, r)/r + 2*F/r**2)
        elif term.has(sp.Derivative(chi, r)):
            F = sp.simplify(term / sp.Derivative(chi, r))
            E -= chi * sp.expand(sp.diff(F, r) + 2*F/r)
        elif term.has(chi):
            E += term
    E = sp.expand(sp.series(E, eps, 0, 3).removeO())
    return sp.expand(E.subs(sp.Function('chi')(r), 1))

# ---- lapse EL: probe Phi2 ----
def lapse_probe(other, chi, s):
    PhiX = eps*Phi1 + eps**2*(varphi2 + s*chi)
    return Dens_of(PhiX, Psi, Z, Uaux)
E_Phi = probe_EL(lapse_probe, None)
# ---- spatial EL: probe Psi2 ----
def spatial_probe(other, chi, s):
    PsiX = eps*Psi1 + eps**2*(psi2 + s*chi)
    return Dens_of(Phi, PsiX, Z, Uaux)
E_Psi = probe_EL(spatial_probe, None)

# ---- linear gates ----
UP, UPP = sp.Derivative(U, r), sp.Derivative(U, (r, 2))
E1o = sp.expand(4*cN*L0(Phi1 - ell*Sk*Phi1/4))
def linsubs(f):
    return sp.expand(f.coeff(eps, 1).subs(Sk, 0).replace(UPP, 0).replace(UP, 0).replace(U, 0))
g1 = sp.simplify(linsubs(E_Phi) - linsubs(E1o))
g1s = sp.simplify(linsubs(E_Psi))
print("G1 lapse linear  :", g1, " (0 = E1 AS226 match)")
print("G1s shell linear :", g1s, " (0 = shell identity)")
assert g1 == 0 and g1s == 0

# ---- eps^2 system, point mass ----
GM = sp.sqrt(GM2)
A, B = sp.symbols('A B')
def red(f):
    f = sp.expand(f.subs(Sk, 0))
    submap = {sp.Derivative(varphi2, (r,2)): 6*A*GM2/r**4,
              sp.Derivative(psi2, (r,2)):   6*B*GM2/r**4,
              sp.Derivative(varphi2, r):    -2*A*GM2/r**3,
              sp.Derivative(psi2, r):       -2*B*GM2/r**3,
              varphi2: A*GM2/r**2,  psi2: B*GM2/r**2,
              UPP: 2*GM/r**3,  UP: -GM/r**2,  U: GM/r}
    f = sp.expand(f.subs(submap, simultaneous=True))
    f = sp.expand(f).replace(GM**2, GM2).replace(GM, 0)
    return sp.expand(f)
E2l = red(sp.expand(E_Phi.coeff(eps, 2)))
E2s = red(sp.expand(E_Psi.coeff(eps, 2)))
t = sp.symbols('t', positive=True)
def harm4(f):
    f = sp.expand(f * r**4)
    f = sp.expand(f.replace(r, 1/t))
    f = sp.expand(sp.series(f, t, 0, 5).removeO())
    p = sp.Poly(f, t)
    return sp.simplify(p.coeff_monomial(t**4)) if p.degree() >= 4 else sp.S.Zero
hl = harm4(E2l); hs = harm4(E2s)
print("lapse eq   (1/r^4):", hl)
print("spatial eq (1/r^4):", hs)
Pl = sp.expand(sp.together(hl)); Ps = sp.expand(sp.together(hs))
sol = sp.solve([Pl, Ps], [A, B], dict=True)
print("solution:", sol)
if sol:
    As, Bs = sp.simplify(sol[0][A]), sp.simplify(sol[0][B])
    print("A = phi2/U_N^2 =", As, "  B = psi2/U_N^2 =", Bs)
    print("BETA = 1 + phi2/U_N^2 =", sp.simplify(1 + As))
    print("residuals:", sp.simplify(sp.expand(Pl.subs({A: As, B: Bs}))),
          sp.simplify(sp.expand(Ps.subs({A: As, B: Bs}))))
    A0, B0 = sp.simplify(As.subs(alpha, 0)), sp.simplify(Bs.subs(alpha, 0))
    print("G3 alpha=0: A0 =", A0, " B0 =", B0, " [expect 0, -3/4]")
    cA = sp.simplify(sp.expand(Pl.subs({A: 0, B: -sp.Rational(3,4)})))
    cB = sp.simplify(sp.expand(Ps.subs({A: 0, B: -sp.Rational(3,4)})))
    print("G4 neg control (A=0,B=-3/4): lapse", cA, " spatial", cB)
    print("   alpha=0:", sp.simplify(cA.subs(alpha, 0)), sp.simplify(cB.subs(alpha, 0)))
else:
    print("no solution; eqs:", Pl, " | ", Ps)
with open('as232_final8_out.txt', 'w') as f:
    f.write(f"Pl = {Pl}\nPs = {Ps}\nsol = {sol}\nBETA = {sp.simplify(1+As) if sol else 'nan'}\n"
            f"G3 = {A0 if sol else '?'} {B0 if sol else '?'}\n"
            f"G4 = {cA if sol else '?'} {cB if sol else '?'}\n")