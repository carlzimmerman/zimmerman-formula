"""Vector sector of the v7 THE_COMPLETION action -- exploratory second-order expansion.

Conventions: signature (-,+,+,+); coords (t,x,y,z); single Fourier mode ~ cos(kz)/sin(kz),
polarization xhat.  Metric vector perturbations: g_{0x} = eps*a*S(t)*cos(kz),
g_{xz} = a^2 * d_z[eps*F(t)cos(kz)]  (i.e. g_ij vector part 2*d_(i F_j)).
Aether: A^x = eps*V(t)*cos(kz)/a ; A^0 fixed by unit-norm to O(eps^2).
Khronon: phi = phib(t) only (no vector part).
"""
import sympy as sp
from sympy import sqrt, cos, sin, pi, exp, Rational, Function, Derivative as D

t, z, xs, ys = sp.symbols('t z x y', real=True)
k, eps = sp.symbols('k epsilon', positive=True)
G, KB, Lam, Ab, Q0 = sp.symbols('G K_B Lambda A_b Q_0', real=True)
coords = [t, xs, ys, z]

a   = Function('a', positive=True)(t)
S   = Function('S')(t)
V   = Function('V')(t)
Fm  = Function('Fm')(t)     # metric vector potential F_x = eps*Fm*cos(kz)
phib= Function('varphi')(t)
cz, sz = cos(k*z), sin(k*z)

NTRUNC = 3   # keep up to eps^2

def trunc(e, n=NTRUNC):
    e = sp.expand(e)
    return sp.Add(*[e.coeff(eps, i)*eps**i for i in range(n)])

# ---------------- metric ----------------
gxz = sp.diff(eps*Fm*cz, z) * a**2          # a^2 * d_z F_x
g = sp.Matrix([[-1,        eps*a*S*cz, 0,     0   ],
               [eps*a*S*cz, a**2,      0,     gxz ],
               [0,          0,         a**2,  0   ],
               [0,          gxz,       0,     a**2]])
assert g.is_symmetric(), "metric must be symmetric"
gbar    = sp.diag(-1, a**2, a**2, a**2)
gbarinv = sp.diag(-1, a**-2, a**-2, a**-2)
dg   = g - gbar
ginv = gbarinv - gbarinv*dg*gbarinv + gbarinv*dg*gbarinv*dg*gbarinv
ginv = ginv.applyfunc(trunc)

chk = (ginv*g).applyfunc(trunc) - sp.eye(4)
assert all(sp.simplify(chk[i, j]) == 0 for i in range(4) for j in range(4)), "inverse check failed"
print("CHECK inverse metric to O(eps^2): OK")

detg  = trunc(g.det())
w2    = sp.simplify(trunc(-detg/a**6) )     # = 1 + eps^2 * (...)
sqrtg = sp.expand(a**3*(1 + (w2 - 1)/2 - (w2-1)**2/8))
sqrtg = trunc(sqrtg)
print("sqrt(-g)/a^3 - 1 =", sp.simplify(sqrtg/a**3 - 1))

# ---------------- Christoffels & Ricci ----------------
Gam = [[[trunc(Rational(1,2)*sum(ginv[r,s]*(sp.diff(g[s,m],coords[n]) + sp.diff(g[s,n],coords[m])
        - sp.diff(g[m,n],coords[s])) for s in range(4))) for n in range(4)] for m in range(4)]
        for r in range(4)]

Ric = [[trunc( sum(sp.diff(Gam[r][m][n], coords[r]) for r in range(4))
             - sum(sp.diff(Gam[r][r][n], coords[m]) for r in range(4))
             + sum(Gam[r][r][l]*Gam[l][m][n] for r in range(4) for l in range(4))
             - sum(Gam[r][m][l]*Gam[l][r][n] for r in range(4) for l in range(4)) )
        for n in range(4)] for m in range(4)]

Rs = trunc(sum(ginv[m,n]*Ric[m][n] for m in range(4) for n in range(4)))
R0 = Rs.coeff(eps, 0)
print("background R =", sp.simplify(R0), " (expect 6(addot/a + (adot/a)^2))")

# ---------------- aether ----------------
A2v = sp.symbols('A2v')                     # coefficient of eps^2 in A^0
Au  = [1 + eps**2*A2v, eps*V*cz/a, 0, 0]
norm = trunc(sum(g[m,n]*Au[m]*Au[n] for m in range(4) for n in range(4)))
sol  = sp.solve(sp.expand(norm + 1).coeff(eps, 2), A2v)
assert len(sol) == 1
A2 = sp.simplify(sol[0])
print("A^0 = 1 + eps^2 * A2,   A2 =", A2)
Au = [1 + eps**2*A2, eps*V*cz/a, 0, 0]

Ad = [trunc(sum(g[m,n]*Au[n] for n in range(4))) for m in range(4)]   # A_mu
Fmn = [[trunc(sp.diff(Ad[n], coords[m]) - sp.diff(Ad[m], coords[n])) for n in range(4)] for m in range(4)]
F2  = trunc(sum(ginv[m,r]*ginv[n,s]*Fmn[m][n]*Fmn[r][s]
                for m in range(4) for n in range(4) for r in range(4) for s in range(4)))
print("F^2 (aether) O(eps^0,1):", sp.simplify(F2.coeff(eps,0)), sp.simplify(F2.coeff(eps,1)))
print("F^2 (aether) at O(eps^2):")
sp.pprint(sp.simplify(F2.coeff(eps,2)))

# ---------------- khronon invariants ----------------
dphi = [sp.diff(phib, c_) for c_ in coords]
Q  = trunc(sum(Au[m]*dphi[m] for m in range(4)))
Yx = trunc(sum((ginv[m,n] + Au[m]*Au[n])*dphi[m]*dphi[n] for m in range(4) for n in range(4)))
print("Q =", sp.simplify(Q))
print("Y order eps^0:", sp.simplify(Yx.coeff(eps,0)), " order eps^1:", sp.simplify(Yx.coeff(eps,1)))
Y2 = sp.simplify(Yx.coeff(eps,2))
print("Y = eps^2 * Y2,  Y2 =", sp.factor(Y2))

# ---------------- dark sector expansions ----------------
Kf   = Function('K')          # K(Q), DBI -- kept symbolic
Acal = Function('Acal')       # promoted a0^2(Q) = kappa^2 G(-K(Q)); kept symbolic
Kser = sp.series(Kf(Q), eps, 0, NTRUNC).removeO()
Kser = trunc(Kser)
print("K(Q) at O(eps^2):", sp.simplify(Kser.coeff(eps,2)))

Qb = D(phib, t)
Abar, Aprm = sp.symbols('Abar Aprm', positive=True)   # Acal(Qbar), Acal'(Qbar) stand-ins
# B-term:  A_b * B(Y/Acal(Q)) * (Q-Q0)^2 ,  B(y) = y/(1+y)^2
# Taylor-substitute Acal(Q) = Abar + Aprm*(Q - Qbar) + O((Q-Qbar)^2); Q-Qbar = O(eps^2)
AcalQ = Abar + Aprm*(Q - Qb)
yarg  = Yx/AcalQ
Bser  = sp.series(Ab * (yarg/(1+yarg)**2) * (Q - Q0)**2, eps, 0, NTRUNC).removeO()
Bser  = trunc(Bser)
print("B-term O(eps^0,1):", sp.simplify(Bser.coeff(eps,0)), sp.simplify(Bser.coeff(eps,1)))
Bco = sp.simplify(Bser.coeff(eps,2))
print("B-term at O(eps^2):", Bco)
assert Aprm not in Bco.free_symbols, "promotion derivative Acal' should NOT enter the vector sector"
print("CHECK: Acal'(Qbar) absent from the O(eps^2) B-term -- promotion enters via background Abar only")

# F_Y-term: (Acal/8 pi G) F_Y(Y/Acal); F_Y(y) = y - 2 + 2(sqrt(y)+1)exp(-sqrt(y))
wv = sp.symbols('w', positive=True)
FY = wv**2 - 2 + 2*(wv + 1)*exp(-wv)
assert sp.simplify(sp.diff(FY, wv)/(2*wv) - (1 - exp(-wv))) == 0   # F_Y'(y)=1-e^{-sqrt y}, y=w^2
FYser = sp.series(FY, wv, 0, 4).removeO()
print("F_Y(w^2) small-w series:", FYser, "  => with w = eps*sqrt(Y2/Abar): term is O(eps^3)")

# ---------------- total Lagrangian density, O(eps^2), z-averaged ----------------
Ldens = sqrtg*((Rs - 2*Lam)/(16*pi*G) - Rational(1,2)*KB*F2/(16*pi*G) + Kser + Bser)
L2 = sp.expand(Ldens).coeff(eps, 2)
L2z = sp.integrate(L2, (z, 0, 2*pi/k))*k/(2*pi)
L2z = sp.simplify(L2z)
print("\n================= z-averaged O(eps^2) Lagrangian =================")
sp.pprint(L2z)

import os
out = os.path.join(os.path.dirname(__file__), 'L2z.srepr')
with open(out, 'w') as f:
    f.write(sp.srepr(L2z))
print("saved", out)
