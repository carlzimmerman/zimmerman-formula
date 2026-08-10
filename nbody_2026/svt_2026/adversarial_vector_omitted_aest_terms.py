"""
THE REFUTATION HUNT, PART 2: the FULL AeST action (arXiv:2007.00082 Eq. 5, as sourced in
real_research/bridge1_aest_equations.md) contains, besides the K_B Maxwell term,

    + 2(2-K_B) J^mu grad_mu phi   with  J^mu = A^alpha nabla_alpha A^mu
    -   (2-K_B) Y

inside the 1/(16 pi G) bracket.  vector_sector_v7.py OMITS BOTH.  Since this very
derivation proves delta Y^(2) = Qbar^2 (S+V)^2 cos^2 != 0, the -(2-K_B)Y term contributes
at O(eps^2) unless something cancels.  Here: compute BOTH omitted terms' exact O(eps^2)
vector-sector contribution and re-run the full EL reduction with them included.
"""
import sys
import sympy as sp
from sympy import cos, sin, pi, exp, sqrt, Rational, Function, Derivative as D

t, z = sp.symbols('t z', real=True)
xs, ys = sp.symbols('xx yy', real=True)
k, eps = sp.symbols('k epsilon', positive=True)
G, KB, Lam, Ab, Q0 = sp.symbols('G K_B Lambda A_b Q_0', real=True)
coords = [t, xs, ys, z]

a  = Function('a', positive=True)(t)
S  = Function('S')(t)
V  = Function('V')(t)
F  = Function('F')(t)
ph = Function('phi')(t)
c_, s_ = cos(k*z), sin(k*z)

nfail = 0
def check(name, cond):
    global nfail
    ok = bool(cond)
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        nfail += 1

def cut(e, n=3):
    e = sp.expand(e)
    return sp.Add(*[e.coeff(eps, i)*eps**i for i in range(n)])

# ---------------- geometry (same as the independent script) ----------------
gxz = sp.diff(eps*F*c_, z)*a**2
g = sp.Matrix([[-1,          eps*a*S*c_, 0,     0  ],
               [eps*a*S*c_,  a**2,       0,     gxz],
               [0,           0,          a**2,  0  ],
               [0,           gxz,        0,     a**2]])
ginv = g.inv().applyfunc(lambda e: cut(sp.series(sp.together(e), eps, 0, 3).removeO()))
detg = sp.factor(g.det())
sqrtg = cut(sp.series(sqrt(-detg), eps, 0, 3).removeO())
Gam = [[[cut(Rational(1, 2)*sum(ginv[r, w]*(sp.diff(g[w, m], coords[n]) + sp.diff(g[w, n], coords[m])
        - sp.diff(g[m, n], coords[w])) for w in range(4))) for n in range(4)] for m in range(4)]
        for r in range(4)]
Ric = [[cut(sum(sp.diff(Gam[r][m][n], coords[r]) for r in range(4))
          - sum(sp.diff(Gam[r][m][r], coords[n]) for r in range(4))
          + sum(Gam[r][r][l]*Gam[l][m][n] for r in range(4) for l in range(4))
          - sum(Gam[r][n][l]*Gam[l][m][r] for r in range(4) for l in range(4)))
        for n in range(4)] for m in range(4)]
Rsc = cut(sum(ginv[m, n]*Ric[m][n] for m in range(4) for n in range(4)))

# ---------------- aether ----------------
A0s = sp.symbols('A0s')
Ax = eps*V*c_/a
normeq = g[0, 0]*A0s**2 + 2*g[0, 1]*A0s*Ax + g[1, 1]*Ax**2 + 1
sel = [r for r in sp.solve(sp.expand(normeq), A0s) if sp.limit(r, eps, 0) == 1][0]
A0 = cut(sp.series(sel, eps, 0, 3).removeO())
Au = [A0, Ax, 0, 0]
Ad = [cut(sum(g[m, n]*Au[n] for n in range(4))) for m in range(4)]
Fmn = [[cut(sp.diff(Ad[n], coords[m]) - sp.diff(Ad[m], coords[n])) for n in range(4)] for m in range(4)]
F2 = cut(sum(ginv[m, r]*ginv[n, w]*Fmn[m][n]*Fmn[r][w]
             for m in range(4) for n in range(4) for r in range(4) for w in range(4)))
Qb = D(ph, t)
Q = cut(A0*Qb)
Y = cut((ginv[0, 0] + A0**2)*Qb**2)

# ---------------- THE OMITTED TERMS ----------------
# J^mu = A^alpha nabla_alpha A^mu = A^alpha ( d_alpha A^mu + Gamma^mu_{alpha beta} A^beta )
Jup = [cut(sum(Au[al]*(sp.diff(Au[m], coords[al])
               + sum(Gam[m][al][be]*Au[be] for be in range(4))) for al in range(4)))
       for m in range(4)]
Jphi = cut(Jup[0]*Qb)          # J^mu grad_mu phi ; phi = phi(t) only
check("J^mu grad_mu phi vanishes at O(eps^0) and O(eps^1)  (background J^mu = 0)",
      sp.expand(Jphi).coeff(eps, 0) == 0 and sp.expand(Jphi).coeff(eps, 1) == 0)
print("   [info] (J.grad phi)^(2) =", sp.simplify(sp.expand(Jphi).coeff(eps, 2)))
print("   [info] Y^(2)            =", sp.simplify(sp.expand(Y).coeff(eps, 2)))

dL_extra = sqrtg*(2*(2 - KB)*Jphi - (2 - KB)*Y)/(16*pi*G)
dL2 = sp.expand(dL_extra).coeff(eps, 2)
dL2 = sp.expand(sp.integrate(dL2, (z, 0, 2*pi/k))*k/(2*pi)).doit()
print("   [info] z-averaged O(eps^2) contribution of the omitted AeST terms:")
print("          dL2 =", sp.simplify(dL2))
check("omitted-terms contribution is NOT identically zero (if PASS, vector_sector_v7's action is "
      "missing O(eps^2) vector-sector terms of the full AeST action)", sp.simplify(dL2) != 0)

# ---------------- full quadratic Lagrangian WITH the omitted terms ----------------
Kf   = Function('K')
Acal = Function('Acal')
qq   = sp.symbols('qq')
Kp   = sp.diff(Kf(qq), qq).subs(qq, Qb)
Kpp  = sp.diff(Kf(qq), qq, 2).subs(qq, Qb)
Ap_  = sp.diff(Acal(qq), qq).subs(qq, Qb)
dQ   = cut(Q - Qb)
LK   = cut(Kf(Qb) + Kp*dQ + Kpp*dQ**2/2)
invA = cut((1 - Ap_*dQ/Acal(Qb))/Acal(Qb))
yy   = cut(Y*invA)
LB   = cut(Ab*(Q - Q0)**2*(yy - 2*yy**2))

Ldens = sqrtg*((Rsc - 2*Lam)/(16*pi*G) - KB*F2/(32*pi*G)) + sqrtg*(LK + LB) + dL_extra
L2 = sp.expand(Ldens).coeff(eps, 2)
L2 = sp.expand(sp.integrate(L2, (z, 0, 2*pi/k))*k/(2*pi)).doit()

# kinetic read-off with the J-term present
cVd2 = sp.simplify(L2.coeff(D(V, t), 2))
print("   [info] coeff(Vdot^2) with omitted terms =", cVd2)
check("kinetic coeff of Sigma-dot^2 STILL = K_B a^3/(32 pi G)? (does the J-term touch the kinetic term)",
      sp.simplify(cVd2 - KB*a**3/(32*pi*G)) == 0)

# ---------------- background on-shell rules ----------------
rhoQ  = Qb*Kp - Kf(Qb)
Lsub  = 3*D(a, t)**2/a**2 - 8*pi*G*rhoQ
asub  = a*(Lam - 8*pi*G*Kf(Qb))/2 - D(a, t)**2/(2*a)
phidd = -3*(D(a, t)/a)*Kp/Kpp

def OS(e):
    e = sp.expand(sp.sympify(e).doit())
    for _ in range(5):
        e = sp.expand(e.subs(D(ph, (t, 4)), sp.diff(phidd, t, 2).doit())
                       .subs(D(ph, (t, 3)), sp.diff(phidd, t).doit())
                       .subs(D(ph, (t, 2)), phidd)
                       .subs(D(a, (t, 4)), sp.diff(asub, t, 2).doit())
                       .subs(D(a, (t, 3)), sp.diff(asub, t).doit())
                       .subs(D(a, (t, 2)), asub)
                       .subs(Lam, Lsub).doit())
    return e

def EL(Lg, f):
    r = sp.diff(Lg, f)
    for n_ in range(1, 5):
        r += (-1)**n_ * sp.diff(sp.diff(Lg, D(f, (t, n_))), (t, n_))
    return sp.expand(r.doit())

# ---------------- EL reduction with the full action ----------------
Sg = Function('Sig')(t)
L2p = sp.expand(L2.subs(V, Sg - S).doit())

elS_os = sp.expand(OS(EL(L2p, S)))
check("EL_S still algebraic in S (constraint survives)",
      not (elS_os.has(D(S, t)) or elS_os.has(D(S, (t, 2)))))
cS_lin = sp.simplify(sp.diff(elS_os, S))
print("   [info] d(EL_S)/dS =", cS_lin)
solS = sp.solve(elS_os, S)
check("S-constraint unique", len(solS) == 1)
Ssol = sp.simplify(solS[0])
print("   [info] constraint solution S =", Ssol)
dev = sp.simplify(Ssol - a*D(F, t))
check("is the constraint STILL S = a Fdot (Phi = 0)?  deviation printed above if not", dev == 0)

Lred = sp.expand(OS(L2p.subs(S, Ssol).doit()))
elF_os = sp.simplify(OS(EL(Lred, F)))
print("   [info] EL_F(Lred) on-shell =", elF_os)
check("F still pure gauge with the omitted terms included", elF_os == 0)

# compare against the CLAIMED final action
W = Function('W')(t)
Ttarget = (KB/(32*pi*G))*(a*D(W, t)**2 - k**2*W**2/a) \
          + a*(Kp*Qb/4 + Ab*Qb**2*(Qb - Q0)**2/(2*Acal(Qb)))*W**2
elSig_os = sp.simplify(OS(EL(Lred, Sg).subs(Sg, W/a).doit()))
elW_target = sp.simplify(OS(EL(Ttarget, W)))
diff_el = sp.simplify(sp.expand(elSig_os - a*elW_target))
print("   [info] EL_Sigma(full) - a*EL_W(claimed) =", diff_el)
check("does the claimed final action SURVIVE the omitted AeST terms?", diff_el == 0)

if nfail:
    print("\n%d CHECK(S) FAILED (interpret via the printed [info] lines)" % nfail)
print("\nDONE")
