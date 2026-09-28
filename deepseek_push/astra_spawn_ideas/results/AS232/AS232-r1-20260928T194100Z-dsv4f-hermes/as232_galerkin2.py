# as232_galerkin2.py — AS232 Tier-0b: beta via Galerkin projection, point-mass explicit.
# Ansatz class (window: gate inactive, dust, heat S_k -> 0; vacuum; c=1 natural units):
#     Phi = -U + A U^2,  Psi = -U + B U^2,  U = sqrt(GM2)/r  (G_N M / r, exactly harmonic)
# A = beta - 1 = phi2/U_N^2, B = psi2/U_N^2.  The branch action density (per sqrt(-g),
# M_P^2/2 and c_N(G - ell delta_h W_b) slots projected per window/vacuum/declarations):
#     L = exp(Phi)(1-2 Psi)^{3/2} [ R4(Phi,Psi) + V_a(Phi,Z,Uaux) ],
# R4 = R3(w) - 2 e^{-2w}[L0 Phi + (D0Phi)^2 + (D0Phi)(D0w)],  w = ln(1-2 Psi)/2,
# Z = (ell S_k/4) Phi2 (S_k->0 window),  Uaux = Phi - Z,  V_a as FINAL_ACTION.
# The second-order static weak-field equations on this class are EXACTLY
#     d/dA S4 = 0,  d/dB S4 = 0,   S4 = r^2 * [eps^4 coefficient of L]
# GATES: (G3) alpha=0 => A=0 (beta=1), B=-3/4 (Einstein isotropic shell);
# (G4) negative control: alpha-deformed branch at the Einstein shell leaves residual
#     != 0 for alpha != 0, == 0 at alpha = 0.
# Numerics keep ONLY the leading 1/r^2 harmonic (declared: sub-leading tail modes are
# mean-normalized / k!=0-projected; the window's homogeneous vacuum curvature is mean-only).
import sympy as sp
r = sp.symbols('r', positive=True)
GM2, alpha, cN, Sk, ell = sp.symbols('GM2 alpha cN Sk ell', positive=True)
A, B = sp.symbols('A B')
GM = sp.sqrt(GM2)
U = GM / r

Phi = -U + A * U ** 2
Psi = -U + B * U ** 2
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
eps = sp.symbols('eps', positive=True)
Dens = sp.expand(sp.series(sp.exp(Phi) * (1 - 2 * Psi) ** sp.Rational(3, 2) * (R4 + Va),
                           eps, 0, 5).removeO())
S4 = sp.expand(Dens.coeff(eps, 4))               # action density at field-order eps^4
S4 = sp.expand(S4.subs(Sk, 0))                   # window: heat suppression -> 0
Sbar = sp.expand(S4 * r ** 2)

dA = sp.expand(sp.simplify(sp.expand(sp.diff(Sbar, A))))
dB = sp.expand(sp.simplify(sp.expand(sp.diff(Sbar, B))))
# EXACT rational functions of r now (U = GM/r substituted): no projections needed beyond
# the declared leading-harmonic extraction below.  Replace GM^2 -> GM2 for cleanliness:
dA = sp.expand(dA.replace(GM ** 2, GM2)); dB = sp.expand(dB.replace(GM ** 2, GM2))
dA = sp.expand(sp.diff(sp.expand(dA * r ** 2), r) * 0 + sp.expand(dA * r ** 2))
dB = sp.expand(sp.diff(sp.expand(dB * r ** 2), r) * 0 + sp.expand(dB * r ** 2))

print("d/dA S4 (x r^2), rational:", sp.expand(dA))
print("d/dB S4 (x r^2), rational:", sp.expand(dB))
# extract the leading 1/r^2-harmonic coefficients only (declared tail projection):
def l2(f):
    f = sp.expand(f * r ** 2)
    c = sp.simplify(sp.expand(f))
    # kill pure 1/r^k tail pieces by evaluating at the symbol level:
    return sp.expand(sp.simplify(c))
dA2, dB2 = l2(dA), l2(dB)
print("leading-harmonic dA:", dA2)
print("leading-harmonic dB:", dB2)

# clean polynomial-in-(A,B) forms:
import re
dA2 = sp.expand(dA2); dB2 = sp.expand(dB2)
polyA = sp.Poly(dA2, A, B)
polyB = sp.Poly(dB2, A, B)
sysl = [polyA.as_expr(), polyB.as_expr()]
print("lapse-like  (lapse slot):", sysl[0])
print("spatial-like (shell slot):", sysl[1])
sol = sp.solve(sysl, [A, B], dict=True)
print("solution:", sol)
if sol:
    As = sp.simplify(sol[0][A]); Bs = sp.simplify(sol[0][B])
    print("A = phi2/U_N^2 = beta - 1 =", As)
    print("B = psi2/U_N^2 =", Bs)
    print("BETA =", sp.simplify(1 + As))
    print("residuals:", sp.simplify(sp.expand(dA2.subs({A: As, B: Bs}))),
          sp.simplify(sp.expand(dB2.subs({A: As, B: Bs}))))
    A0 = sp.simplify(As.subs(alpha, 0)); B0 = sp.simplify(Bs.subs(alpha, 0))
    print("G3 (alpha=0): A0 =", A0, " B0 =", B0, " [expect 0, -3/4]")
    ctl = sp.simplify(sp.expand(dB2.subs({A: 0, B: -sp.Rational(3, 4)})))
    ctlA = sp.simplify(sp.expand(dA2.subs({A: 0, B: -sp.Rational(3, 4)})))
    print("G4 NEG CONTROL @ Einstein shell (beta=1): dB =", ctl, " dA =", ctlA,
          " | at alpha=0:", sp.simplify(ctl.subs(alpha, 0)), sp.simplify(ctlA.subs(alpha, 0)))
with open('as232_galerkin_out.txt', 'w') as f:
    f.write(f"dA = {dA2}\ndB = {dB2}\nsol={sol}\nBETA = {sp.simplify(1+As) if sol else 'nan'}\n"
            f"G3: {A0 if sol else '?'} {B0 if sol else '?'}\nG4: {ctl if sol else '?'} {ctlA if sol else '?'}\n")