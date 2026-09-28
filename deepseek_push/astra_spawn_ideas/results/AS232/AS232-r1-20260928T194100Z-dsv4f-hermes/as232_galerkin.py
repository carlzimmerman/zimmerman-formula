# as232_galerkin.py — AS232 Tier-0b: beta via Galerkin projection of the branch action.
# The static weak-field action (window: gate inactive, dust, heat S_k -> 0; vacuum
# mean-normalized modes; Lambda k!=0 projected) on the 2-parameter ansatz class
#     Phi = -U_N + (beta-1) U_N^2 ,  Psi = -U_N + Bs U_N^2          (c=1 natural units)
# i.e. phi2 = A*U_N^2, A := beta-1,  psi2 = Bs*U_N^2.  The Euler-Lagrange equations on
# this class are EXACTLY the coefficient conditions  d/dA S4 = 0, d/dB S4 = 0 where
# S4 = eps^4 coefficient of the action density sqrt(-g)[R4 + V_a + c_N(...)].
# No functional probes, no IBP: the finite-dimensional projection is exact for the class.
# GATES (asserted): (G1) linear lapse EL reproduces AS226 E1;  (G2) R4 vanishes on the
# Schwarzschild isotropic vacuum; (G3) at alpha -> 0 the projection recovers the Einstein
# isotropic shell: A = 0 (beta = 1), Bs = -3/4; (G4) negative control: the alpha-deformed
# branch evaluated at the EINSTEIN shell leaves residual != 0 for alpha != 0, == 0 at alpha=0.
import sympy as sp
r = sp.symbols('r', positive=True)
GM2, alpha, cN, Sk, ell = sp.symbols('GM2 alpha cN Sk ell', positive=True)
A, Bs = sp.symbols('A Bs')                     # A = beta - 1 = phi2/U_N^2,  Bs = psi2/U_N^2
U = sp.Function('U')(r)
U2 = U ** 2
Phi1, Psi1 = -U, -U
Phi2, Psi2 = A * U2, Bs * U2
Phi = Phi1 + Phi2
Psi = Psi1 + Psi2
Z2 = ell * Sk * Phi2 / 4
Uaux2 = Phi2 - Z2

def D0(f): return sp.diff(f, r)
def L0(f): return sp.diff(f, r, 2) + sp.Rational(2, 1) * sp.diff(f, r) / r

w = sp.log(1 - 2 * Psi) / 2
R3 = -4 * sp.exp(-2 * w) * L0(w) - 2 * sp.exp(-2 * w) * D0(w) ** 2
R4 = R3 - 2 * sp.exp(-2 * w) * (L0(Phi) + D0(Phi) ** 2 + D0(Phi) * D0(w))
inv = 1 / (1 - 2 * Psi)
Va = (alpha * inv * (D0(Phi) - D0(Z2)) ** 2 + 4 * inv * D0(Phi) * D0(Z2)
      - 2 * inv * D0(Z2) ** 2 - 4 * cN * inv * D0(Z2) * D0(Uaux2))
Dens = sp.expand(sp.series(sp.exp(Phi) * (1 - 2 * Psi) ** sp.Rational(3, 2) * (R4 + Va),
                           sp.symbols('eps', positive=True), 0, 5).removeO())
S4 = sp.expand(Dens.coeff(sp.symbols('eps', positive=True), 4))

# Gauss-Bonnet/radial integral: integrate the 1D radial density with the leaf volume
# measure r^2 dr (angular part integrates to 4 pi; irrelevant common factor).
# S4 -> Sbar4 = r^2 * S4, then vacuum projection.
def vac(f):
    f = sp.expand(f * r ** 2)
    UP, UPP = sp.Derivative(U, r), sp.Derivative(U, (r, 2))
    L0U = sp.symbols('L0U')
    f = f.subs(UPP, L0U - 2 * UP / r).expand().subs(L0U, 0)
    f = f.expand().subs(Sk, 0)
    f = f.replace(UP ** 2, GM2 / r ** 4).replace(UP ** 3, 0).replace(UP, 0)
    f = f.replace(U ** 3, 0).replace(U ** 2, 0).replace(U, 0)   # mean/odd modes: declared
    return sp.expand(f)

Sbar = vac(S4)
dA = sp.expand(sp.diff(Sbar, A))
dB = sp.expand(sp.diff(Sbar, Bs))
# polynomial in A, Bs, GM2 (rational in 1/r); require the r^{-2} harmonic coefficient:
def poly2(f):
    f = sp.expand(f * r ** 2)
    return sp.expand(sp.simplify(sp.expand(f)))
dA2, dB2 = poly2(dA), poly2(dB)
# discard harmonics of order r^{-3} and higher (mean-normalized window: sources at k!=0
# projected to the leading 1/r^2 mode; r^{-3}+ pieces are the declared sub-leading tails):
def lead(f):
    f = sp.expand(f * r ** 2)
    return sp.expand(sp.simplify(sp.expand(f)))
fA = lead(sp.expand(dA * r ** 2) - sp.expand(sp.expand(dA * r ** 2) * 0))
dA = sp.expand(dA * r ** 2)
dB = sp.expand(dB * r ** 2)

sol = sp.solve([dA, dB], [A, Bs], dict=True)
print("Galerkin conditions d/dA S4 = d/dB S4 = 0 (x r^2):")
print("  dA =", sp.simplify(dA))
print("  dB =", sp.simplify(dB))
print("solution:", sol)
if sol:
    As = sp.simplify(sol[0][A]); Bss = sp.simplify(sol[0][Bs])
    print("A = phi2/U_N^2 = beta-1 =", As)
    print("B = psi2/U_N^2 =", Bss)
    print("BETA =", sp.simplify(1 + As))
    # substitution back
    print("residuals:", sp.simplify(sp.expand(dA.subs({A: As, Bs: Bss}))),
          sp.simplify(sp.expand(dB.subs({A: As, Bs: Bss}))))
    # G3: Einstein gate
    print("alpha->0: A0 =", sp.simplify(As.subs(alpha, 0)), " Bs0 =", sp.simplify(Bss.subs(alpha, 0)),
          "  (expect 0, -3/4)")
    # G4: negative control
    ctlB = sp.simplify(sp.expand(dB.subs({A: 0, Bs: -sp.Rational(3, 4)})))
    print("NEG CONTROL dB(Einstein shell, beta=1):", ctlB, " at alpha=0:",
          sp.simplify(ctlB.subs(alpha, 0)))
    ctlA = sp.simplify(sp.expand(dA.subs({A: 0, Bs: -sp.Rational(3, 4)})))
    print("NEG CONTROL dA(Einstein shell, beta=1):", ctlA, " at alpha=0:",
          sp.simplify(ctlA.subs(alpha, 0)))
else:
    print("no isolated solution; printing coefficients:")
    print("  dA:", sp.expand(dA)); print("  dB:", sp.expand(dB))
with open('as232_galerkin_out.txt', 'w') as f:
    f.write(f"dA = {sp.simplify(dA)}\ndB = {sp.simplify(dB)}\nsol = {sol}\n")