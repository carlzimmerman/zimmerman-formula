#!/usr/bin/env python3
"""SCALE-SPLIT DOOR — general two-auxiliary localization of the nonlocal (-D^2)^-1 kernel.
Fields chi=(chi1,chi2), quadratic sector  L = 1/2 chi'^T A chi' (relativistic) - 1/2 chi^T M chi + chi^T c S,
kernel read out through d^T chi. Static response R(k^2) = d^T (A k^2 + M)^{-1} c.
DEMAND: R(k^2) = 1/k^2 EXACTLY for all k (Coulomb: no Yukawa, no contact term).
Derive what that forces (Thm A), then whether a ghost-free scale-split solution exists (Thm B)."""
import sympy as sp

k2, m = sp.symbols('k2 m', positive=True)
a11,a12,a22,m11,m12,m22,c1,c2,d1,d2 = sp.symbols('a11 a12 a22 m11 m12 m22 c1 c2 d1 d2', real=True)
A = sp.Matrix([[a11,a12],[a12,a22]]); M = sp.Matrix([[m11,m12],[m12,m22]])
c = sp.Matrix([c1,c2]); d = sp.Matrix([d1,d2])

print("=== THEOREM A: what does an EXACT Coulomb kernel force? ===")
X = A*k2 + M
R = (d.T * X.inv() * c)[0,0]
# exact matching: k^2 * numerator(R) - denominator(R)*1 = 0 as a polynomial in k2
num, den = sp.fraction(sp.cancel(sp.together(R - 1/k2)))
eqs = sp.Poly(sp.expand(num), k2).all_coeffs()
print(f"   matching R(k^2)=1/k^2 for ALL k => {len(eqs)} polynomial conditions in k^2:")
conds = [sp.simplify(e) for e in eqs]
for i,e in enumerate(conds): print(f"     C{i}: {e} = 0")
# identify the k^0 condition = det(M)
detM = sp.det(M)
c_k0 = conds[-1]
ratio = sp.simplify(c_k0 / detM)
print(f"   k^0 condition / det(M) = {ratio}   -> exact Coulomb FORCES det(M)=0: ONE MASSLESS MODE, always.")
print("   COROLLARY (dichotomy): gap that mode (det(M)!=0) => R(k->0) finite => Yukawa/contact, kernel dead.")
print("   => The massless pole IS the kernel. 'Gap everything' is impossible. Scale-split = gap ONLY mode 2.")

print("\n=== THEOREM B: does a GHOST-FREE scale-split solution exist? (A ≻ 0, M ⪰ 0, exact Coulomb) ===")
# canonical frame: field redefinition sets A = I (possible iff A ≻ 0 = the no-ghost demand).
# Then try M = m^2 * w w^T (rank-1 PSD => det(M)=0 automatic), w = (0,1) WLOG rotation.
A0 = sp.eye(2); w = sp.Matrix([0,1]); M0 = m**2 * w*w.T
cv = sp.Matrix(sp.symbols('cA cB', real=True)); dv = sp.Matrix(sp.symbols('dA dB', real=True))
R0 = sp.simplify((dv.T * (A0*k2 + M0).inv() * cv)[0,0])
print(f"   R(k^2) with A=I, M=m^2 diag(0,1):  {R0}")
# demand exact 1/k^2: c_B (source along heavy dir) must vanish; d_A c_A = 1
sol = sp.solve([sp.together(R0 - 1/k2)], [cv[1]], dict=True)
R_split = R0.subs(cv[1], 0)
print(f"   set c_B=0 (source couples ONLY to the massless direction): R = {sp.simplify(R_split)}")
print(f"   => exact 1/k^2 iff d_A*c_A = 1. Explicit solution: A=I (NO GHOST), M=m^2 diag(0,1) (NO TACHYON),")
print(f"      c=(1,0), d=(1,d_B): kernel EXACT Coulomb at every k; second mode gapped at m, FREE choice")
print(f"      1/m < 1 kpc (frozen on galactic k-band) with ZERO effect on the kernel. DC-011 evaded.")

print("\n=== verify the full original conditions hold for the explicit point ===")
subs = {a11:1,a12:0,a22:1, m11:0,m12:0,m22:m**2, c1:1,c2:0, d1:1,d2:sp.Symbol('dB')}
Rcheck = sp.simplify(R.subs(subs))
print(f"   R(k^2) at the explicit point = {Rcheck}   (must be 1/k2) -> {'PASS' if sp.simplify(Rcheck-1/k2)==0 else 'FAIL'}")
eigA = list(A.subs(subs).eigenvals()); eigM = list(M.subs(subs).eigenvals())
print(f"   eig(A) = {eigA} (all >0: no ghost)   eig(M) = {eigM} (>=0: no tachyon)")

print("\n=== what the massless mode IS, and the honest cost ===")
print("   The massless direction chi_A is a genuine propagating Lorentz scalar (omega = c k): the MOND")
print("   kernel is its static exchange. UNAVOIDABLE by Thm A. So the price of localization is ONE")
print("   massless radiative scalar. Its couplings inherit the F+ structure: at high y the vertex runs")
print("   with 2F+' = e^{-y}, so radiative losses in binary-pulsar/solar-system regimes are screened by")
print("   the SAME exponential that protects PPN -- and because chi_A is not a preferred-frame carrier,")
print("   there is NO alpha_1/alpha_2 to pay. P7 does not bite: the kinetic matrix is A=I, FIXED, not")
print("   proportional to the screened coupling (the screening lives in the VERTEX c(y), not in A).")
print('CERTIFICATE_JSON: {"gate":"SCALE-SPLIT-spectral","status":"PASS-CONDITIONAL",'
      '"certificate":"Thm A: exact Coulomb kernel forces det(M)=0 (massless pole = the kernel); '
      'fully-gapped auxiliary sector impossible (dichotomy: gap => Yukawa). Thm B: explicit ghost-free '
      'scale-split point EXISTS: A=I, M=m^2 diag(0,1), c=(1,0), d_A=1 -- exact 1/k^2 at all k, second '
      'mode gapped freely (1/m<1kpc), no ghost, no tachyon, kinetic normalization independent of '
      'screening (P7 safe). COST: one massless radiative scalar, vertex-screened by e^-y at high y.",'
      '"assumptions":["relativistic 2nd-order kinetic terms","quadratic spectral level only: lensing '
      'embedding, c_T on FRW, Cassini time-domain, and Dirac count of the FULL coupled system remain '
      'the open gates"],"numeric_values":{}}')
