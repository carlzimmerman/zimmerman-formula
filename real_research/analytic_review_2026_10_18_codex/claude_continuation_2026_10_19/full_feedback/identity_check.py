"""Symbolic identity checks for RESULT.md (checkpoint ZAR-2026-10-19-09-CL).

Pure algebra (sympy); no numerics, no data. Each printed value must be 0.

1. Free-species epicyclic frequency: with a_f = -G (M_b + M)/r^2 and
   L_c = r^3 (-a_f), omega_f^2 = L_c'/r^3 satisfies
   (omega_f^2)' = G (r^2 M'' - r M' - 3 M - 3 M_b)/r^4.      (Prop N(d))
2. Inner taper M = A r S((r - r0)/Delta): the sign condition above is
   r^2 S'/Delta + r^3 S''/Delta^2 < 3 r_M + 4 r S,  r_M = M_b/A.  (Prop N(d))
3. Tethered species on the law annulus (M_t = f A r, M_f = (1-f) A r,
   A = sqrt(a_0 M_b/G), c = G^2/a_0):
   omega_t^2 = [G M_b (1 - f^2) + 2 G (1 - f) A r]/r^3.           (Prop N(e))
4. Eigenmode energy per harmonic: with u = kO psi/(kO - nu),
   u^2 - u psi = psi^2 kO nu/(kO - nu)^2.                          (B3(c))
"""
import sympy as sp

r, G, Mb, A, r0, D, f, a0 = sp.symbols('r G M_b A r_0 Delta f a_0', positive=True)
M = sp.Function('M')(r)

# 1
Lc = r**3 * G * (Mb + M) / r**2
w2 = sp.diff(Lc, r) / r**3
target = G * (-3*Mb - 3*M - r*sp.diff(M, r) + r**2*sp.diff(M, r, 2)) / r**4
print('1 free (omega^2)\' identity:', sp.simplify(sp.diff(w2, r) - target))

# 2
S = sp.Function('S')
z = (r - r0) / D
Mt = A * r * S(z)
lhs = sp.simplify((-3*Mb - 3*Mt - r*sp.diff(Mt, r) + r**2*sp.diff(Mt, r, 2)) / A)
claim = -(3*Mb/A + 4*r*S(z)) + r**2*sp.diff(S(z), r) + r**3*sp.diff(S(z), r, 2)
print('2 inner-taper condition identity:', sp.simplify(lhs - claim))

# 3
c = G**2 / a0
Ar = sp.sqrt(a0 * Mb / G)
Mt_ = f * Ar * r
Mf_ = (1 - f) * Ar * r
at = -G * (Mb + Mf_) / r**2 + c * Mt_**2 / r**4
w2t = sp.simplify(sp.diff(r**3 * (-at), r) / r**3)
print('3 tethered omega^2 on law annulus:',
      sp.simplify(w2t - (G*Mb*(1 - f**2) + 2*G*(1 - f)*Ar*r) / r**3))

# 4
kO, nu, ps = sp.symbols('kO nu psi', real=True)
u = kO * ps / (kO - nu)
print('4 eigenmode energy per harmonic:',
      sp.simplify(u**2 - u*ps - ps**2*kO*nu/(kO - nu)**2))
