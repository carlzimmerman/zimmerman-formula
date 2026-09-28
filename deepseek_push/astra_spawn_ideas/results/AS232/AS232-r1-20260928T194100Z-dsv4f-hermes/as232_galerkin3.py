# as232_galerkin3.py — AS232 Tier-0b: beta via Galerkin (Ritz) projection, exact point-mass.
# Ansatz class (window: gate inactive, dust, heat S_k -> 0; vacuum; natural c=1):
#     Phi = eps*(-U) + eps^2*A*U^2 ,  Psi = eps*(-U) + eps^2*B*U^2 ,  U = sqrt(GM2)/r
# A = beta - 1 = phi2/U_N^2 ,  B = psi2/U_N^2.
# Action density (branch, per sqrt(-g)):  L = e^{Phi}(1-2 Psi)^{3/2}[R4 + V_a],
#   R4 = R3(w) - 2 e^{-2w}[L0 Phi + (D0 Phi)^2 + (D0 Phi)(D0 w)],  w = ln(1-2 Psi)/2,
#   Z2 = (ell S_k/4) Phi2 (window S_k->0),  Uaux = Phi - Z2,  V_a as FINAL_ACTION.
# Ritz conditions at leading order:  d/dA S4 = 0, d/dB S4 = 0, S4 = r^2 [eps^4 coeff of L],
# evaluated at the leading 1/r^2 harmonic (r -> 1/t, t^0-series coefficient).
# G3: alpha=0 => A=0 (beta=1), B=-3/4; G4: negative control fires iff alpha != 0.
import sympy as sp
r = sp.symbols('r', positive=True)
GM2, alpha, cN, Sk, ell = sp.symbols('GM2 alpha cN Sk ell', positive=True)
A, B = sp.symbols('A B')
eps = sp.symbols('eps', positive=True)
GM = sp.sqrt(GM2)
U = GM / r
Phi = eps * (-U) + eps ** 2 * A * U ** 2
Psi = eps * (-U) + eps ** 2 * B * U ** 2
Phi2 = A * U ** 2
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
                           eps, 0, 5).removeO())
S4 = sp.expand(Dens.coeff(eps, 4).subs(Sk, 0))       # window heat suppression
Sbar = sp.expand(S4 * r ** 2)

dA = sp.expand(sp.diff(Sbar, A))
dB = sp.expand(sp.diff(Sbar, B))
dA = sp.expand(dA.replace(GM ** 2, GM2)); dB = sp.expand(dB.replace(GM ** 2, GM2))

t = sp.symbols('t', positive=True)
def lead(f):
    f = sp.expand(f.subs(r, 1 / t))
    f = sp.expand(f.replace(GM, sp.sqrt(GM2)))
    s = sp.series(f, t, 0, 1).removeO()          # leading harmonic: order t^0
    s = sp.simplify(sp.simplify(s))
    return sp.expand(s)

dA_l, dB_l = lead(dA), lead(dB)
print("leading dA:", dA_l)
print("leading dB:", dB_l)

# polynomial in A, B (rational in alpha, cN, GM2):
dA_l = sp.expand(sp.together(dA_l)); dB_l = sp.expand(sp.together(dB_l))
print("Galerkin lapse-like  eq:", dA_l)
print("Galerkin shell-like eq:", dB_l)
sol = sp.solve([dA_l, dB_l], [A, B], dict=True)
print("solution:", sol)
if sol:
    As = sp.simplify(sol[0][A]); Bs = sp.simplify(sol[0][B])
    print("A = phi2/U_N^2 = beta-1 =", As)
    print("B = psi2/U_N^2 =", Bs)
    print("BETA =", sp.simplify(1 + As))
    print("residuals:", sp.simplify(sp.expand(dA_l.subs({A: As, B: Bs}))),
          sp.simplify(sp.expand(dB_l.subs({A: As, B: Bs}))))
    A0 = sp.simplify(As.subs(alpha, 0)); B0 = sp.simplify(Bs.subs(alpha, 0))
    print("G3 alpha=0: A0 =", A0, " B0 =", B0, " [expect 0 , -3/4]")
    cB = sp.simplify(sp.expand(dB_l.subs({A: 0, B: -sp.Rational(3, 4)})))
    cA = sp.simplify(sp.expand(dA_l.subs({A: 0, B: -sp.Rational(3, 4)})))
    print("G4 @ Einstein shell: dB =", cB, " dA =", cA)
    print("   at alpha=0:", sp.simplify(cB.subs(alpha, 0)), sp.simplify(cA.subs(alpha, 0)))
else:
    print("no solution; equations:", dA_l, dB_l)
with open('as232_galerkin_out.txt', 'w') as f:
    f.write(f"dA = {dA_l}\ndB = {dB_l}\nsol = {sol}\n"
            f"BETA = {sp.simplify(1+As) if sol else 'nan'}\n"
            f"G3 = {A0 if sol else '?'}, {B0 if sol else '?'}\n"
            f"G4 = {cB if sol else '?'}, {cA if sol else '?'}\n" if False else
            f"dA={dA_l}\ndB={dB_l}\nsol={sol}\n")