"""
ADVERSARIAL INDEPENDENT re-derivation of the v7 vector sector.
Deliberately different code path from vector_sector_v7.py:
  - inverse metric: exact sympy Matrix.inv() (adjugate), then eps-series  (NOT a Neumann series)
  - sqrt(-g): sympy series of sqrt(-det g)                                 (NOT a hand Taylor)
  - A^0: exact quadratic-formula solve of the unit-norm equation           (NOT a linear solve of the eps^2 coeff)
  - K(Q), Acal(Q): generic sympy Functions with chain rule alive           (NOT Taylor stand-in symbols)
  - reduction: pure Euler-Lagrange elimination, NO integration by parts anywhere
    (EL of the raw quadratic Lagrangian is IBP-insensitive => hunts incomplete-IBP errors)
Exit nonzero on any failure.
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

# ---------------- metric (same physical ansatz; independent handling) ----------------
gxz = sp.diff(eps*F*c_, z)*a**2
g = sp.Matrix([[-1,          eps*a*S*c_, 0,     0  ],
               [eps*a*S*c_,  a**2,       0,     gxz],
               [0,           0,          a**2,  0  ],
               [0,           gxz,        0,     a**2]])
ginv_exact = g.inv()          # exact adjugate/det inverse
ginv = ginv_exact.applyfunc(lambda e: cut(sp.series(sp.together(e), eps, 0, 3).removeO()))
idchk = (ginv*g).applyfunc(cut) - sp.eye(4)
check("independent inverse metric correct to O(eps^2)",
      all(sp.simplify(idchk[i, j]) == 0 for i in range(4) for j in range(4)))
detg = sp.factor(g.det())
sqrtg = cut(sp.series(sqrt(-detg), eps, 0, 3).removeO())

# ---------------- curvature (own loop; standard convention) ----------------
Gam = [[[cut(Rational(1, 2)*sum(ginv[r, w]*(sp.diff(g[w, m], coords[n]) + sp.diff(g[w, n], coords[m])
        - sp.diff(g[m, n], coords[w])) for w in range(4))) for n in range(4)] for m in range(4)]
        for r in range(4)]
Ric = [[cut(sum(sp.diff(Gam[r][m][n], coords[r]) for r in range(4))
          - sum(sp.diff(Gam[r][m][r], coords[n]) for r in range(4))
          + sum(Gam[r][r][l]*Gam[l][m][n] for r in range(4) for l in range(4))
          - sum(Gam[r][n][l]*Gam[l][m][r] for r in range(4) for l in range(4)))
        for n in range(4)] for m in range(4)]
Rsc = cut(sum(ginv[m, n]*Ric[m][n] for m in range(4) for n in range(4)))
check("background Ricci scalar = 6(addot/a + adot^2/a^2)  [sign convention anchored]",
      sp.simplify(Rsc.coeff(eps, 0) - 6*(D(a, (t, 2))/a + D(a, t)**2/a**2)) == 0)

# ---------------- aether: A^0 from the EXACT quadratic unit-norm equation ----------------
A0s = sp.symbols('A0s')
Ax = eps*V*c_/a
normeq = g[0, 0]*A0s**2 + 2*g[0, 1]*A0s*Ax + g[1, 1]*Ax**2 + 1   # A^z = A^y = 0
roots = sp.solve(sp.expand(normeq), A0s)
sel = [r for r in roots if sp.limit(r, eps, 0) == 1]
check("unit-norm quadratic has exactly one root -> 1 as eps -> 0", len(sel) == 1)
A0 = cut(sp.series(sel[0], eps, 0, 3).removeO())
check("A^0 = 1 + eps^2 (2S+V) V cos^2 / 2   (delta A^0 purely second order)",
      sp.simplify(A0 - (1 + eps**2*(2*S + V)*V*c_**2/2)) == 0)
Au = [A0, Ax, 0, 0]

# lower-index aether amplitude
Ad = [cut(sum(g[m, n]*Au[n] for n in range(4))) for m in range(4)]
check("A_x = eps a (S+V) cos  (the lower-index amplitude is the gauge-invariant Sigma channel)",
      sp.simplify(Ad[1] - eps*a*(S + V)*c_) == 0)

# ---------------- Q and Y ----------------
Qb = D(ph, t)
Q = cut(A0*Qb)                                   # A^i d_i phi = 0 (khronon scalar)
check("delta Q^(1) = 0;  delta Q^(2) = Qbar (2S+V)V cos^2/2",
      Q.coeff(eps, 1) == 0 and
      sp.simplify(Q.coeff(eps, 2) - Qb*(2*S + V)*V*c_**2/2) == 0)
Y = cut((ginv[0, 0] + A0**2)*Qb**2)
Y2 = sp.simplify(Y.coeff(eps, 2))
check("delta Y^(1) = 0 identically", Y.coeff(eps, 0) == 0 and Y.coeff(eps, 1) == 0)
check("delta Y^(2) = Qbar^2 (S+V)^2 cos^2   (perfect square, >= 0)",
      sp.simplify(Y2 - Qb**2*(S + V)**2*c_**2) == 0)
h00 = cut(ginv[0, 0] + A0**2)
check("h^00 = g^00 + A^0A^0 = eps^2 (S+V)^2 cos^2  (NOT zero at 2nd order: row-19 correction confirmed)",
      sp.simplify(h00 - eps**2*(S + V)**2*c_**2) == 0)

# ---------------- Maxwell term of the aether ----------------
Fmn = [[cut(sp.diff(Ad[n], coords[m]) - sp.diff(Ad[m], coords[n])) for n in range(4)] for m in range(4)]
F2 = cut(sum(ginv[m, r]*ginv[n, w]*Fmn[m][n]*Fmn[r][w]
             for m in range(4) for n in range(4) for r in range(4) for w in range(4)))
Sig_expr = S + V
check("F^2: O(eps^0)=O(eps^1)=0 and O(eps^2) = (2/a^2)[k^2 Sig^2 sin^2 - (d_t[a Sig])^2 cos^2]",
      F2.coeff(eps, 0) == 0 and F2.coeff(eps, 1) == 0 and
      sp.simplify(F2.coeff(eps, 2) - (2*k**2*Sig_expr**2*s_**2/a**2
                                      - 2*(sp.diff(a*Sig_expr, t))**2*c_**2/a**2)) == 0)

# ---------------- dark sector with GENERIC functions ----------------
# Q - Qbar and Y are EXACT polynomials in eps of lowest order eps^2 (proved above), so a
# 2-term Taylor composition is EXACT to O(eps^2).  No sympy nseries needed.
Kf   = Function('K')
Acal = Function('Acal')
qq   = sp.symbols('qq')
Kp   = sp.diff(Kf(qq), qq).subs(qq, Qb)
Kpp  = sp.diff(Kf(qq), qq, 2).subs(qq, Qb)
Ap_  = sp.diff(Acal(qq), qq).subs(qq, Qb)
dQ   = cut(Q - Qb)                       # = eps^2 * Qbar (2S+V)V cos^2/2 exactly
check("dQ is purely O(eps^2)", dQ.coeff(eps, 0) == 0 and dQ.coeff(eps, 1) == 0)
LK   = cut(Kf(Qb) + Kp*dQ + Kpp*dQ**2/2)          # exact to O(eps^2)
# 1/Acal(Q) = (1/Acal(Qbar)) (1 - (Acal'/Acal) dQ) + O(eps^4)
invA = cut((1 - Ap_*dQ/Acal(Qb))/Acal(Qb))
yy   = cut(Y*invA)                                # y = Y/Acal(Q), O(eps^2)
# B(y) = y/(1+y)^2 = y - 2y^2 + ... => at O(eps^2) only the linear piece survives
LB   = cut(Ab*(Q - Q0)**2*(yy - 2*yy**2))
Aprime_atoms = lambda e: [d for d in e.atoms(sp.Derivative) if d.expr.func == Acal]
check("B-term: O(eps^2) = A_b (Qbar-Q0)^2 Y2 / Acal(Qbar)  and  Acal' NEVER appears",
      sp.simplify(LB.coeff(eps, 2) - Ab*(Qb - Q0)**2*Y2/Acal(Qb)) == 0
      and len(Aprime_atoms(sp.expand(LB.coeff(eps, 2)))) == 0)

# MOND term: exact Route-A closed form, Y = eps^2 * (positive), lowest eps-power must be 3
yv = sp.symbols('yv', positive=True)
FYfun = yv - 2 + 2*(sqrt(yv) + 1)*exp(-sqrt(yv))
check("kernel: d/dy F_Y = 1 - e^{-sqrt y}", sp.simplify(sp.diff(FYfun, yv) - (1 - exp(-sqrt(yv)))) == 0)
Y2pos, Abarpos = sp.symbols('Y2pos Abarpos', positive=True)
mond = (Abarpos/(8*pi*G))*FYfun.subs(yv, eps**2*Y2pos/Abarpos)
mser = sp.series(mond, eps, 0, 4).removeO()
check("MOND term = (Abar/8piG) F_Y(eps^2 Y2/Abar) starts at eps^3  (2/3 y^{3/2}) => ZERO in the quadratic action",
      sp.expand(mser).coeff(eps, 0) == 0 and sp.expand(mser).coeff(eps, 1) == 0
      and sp.expand(mser).coeff(eps, 2) == 0
      and sp.simplify(sp.expand(mser).coeff(eps, 3) - Rational(2, 3)*Y2pos*sqrt(Y2pos/Abarpos)/(8*pi*G)) == 0)
# promotion couplings at Y -> 0+
lims = [sp.limit(e, yv, 0, '+') for e in
        (FYfun - yv*sp.diff(FYfun, yv), -yv*sp.diff(FYfun, yv, 2), yv**2*sp.diff(FYfun, yv, 2))]
check("promotion couplings (F - yF'), -yF'', y^2 F'' all -> 0 as y -> 0+ : " + str(lims),
      all(l == 0 for l in lims))

# ---------------- total quadratic Lagrangian, z-averaged ----------------
Ldens = sqrtg*((Rsc - 2*Lam)/(16*pi*G) - KB*F2/(32*pi*G)) + sqrtg*(LK + LB)
L2 = sp.expand(Ldens).coeff(eps, 2)
L2 = sp.expand(sp.integrate(L2, (z, 0, 2*pi/k))*k/(2*pi)).doit()

# no-ghost read-off BEFORE any elimination: Sigma-kinetic = V-dot-squared coefficient
cVdot2 = sp.simplify(L2.coeff(D(V, t), 2))
check("raw kinetic coeff of Vdot^2 (= Sigma-dot^2) = K_B a^3/(32 pi G)  => no-ghost iff K_B > 0",
      sp.simplify(cVdot2 - KB*a**3/(32*pi*G)) == 0)
check("no Sdot^2 and no Sdot*Vdot beyond the K_B block: coeff(Sdot^2) = K_B a^3/(32piG), coeff(Sdot Vdot) = 2x",
      sp.simplify(L2.coeff(D(S, t), 2) - KB*a**3/(32*pi*G)) == 0 and
      sp.simplify(L2.coeff(D(S, t), 1).coeff(D(V, t), 1) - KB*a**3/(16*pi*G)) == 0)

# ---------------- background on-shell rules (standard Friedmann + charge conservation) ----------------
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

# ---------------- EL-based reduction in (S, Sigma, F): NO integration by parts ----------------
Sg = Function('Sig')(t)
L2p = sp.expand(L2.subs(V, Sg - S).doit())

elS = EL(L2p, S)
elS_os = sp.simplify(OS(elS))
check("EL_S is ALGEBRAIC in S on-shell (no Sdot, no Sddot survive the EL operator)",
      not (elS_os.has(D(S, t)) or elS_os.has(D(S, (t, 2)))))
cS = sp.simplify(sp.diff(elS_os, S))
print("   [info] EL_S linear coefficient in S =", cS)
check("EL_S linear coefficient = +/- k^2 a/(32 pi G)  (constraint nondegenerate; consistent with "
      "|coeff(S^2)| = k^2 a/(64 pi G))", sp.simplify(cS**2 - (k**2*a/(32*pi*G))**2) == 0)
solS = sp.solve(sp.expand(elS_os), S)
check("S-constraint unique", len(solS) == 1)
Ssol = sp.simplify(solS[0])
check("constraint: S = a Fdot  exactly  (=> gauge-invariant shear Phi = S - a Fdot = 0 in vacuum; "
      "NO Sigma source on the RHS)", sp.simplify(Ssol - a*D(F, t)) == 0)

# back-substitute the auxiliary field (legit: S enters quadratically, EL_S linear)
Lred = sp.expand(OS(L2p.subs(S, Ssol).doit()))

# F must now be pure gauge: its EL must vanish identically for ARBITRARY Sigma(t), F(t)
elF_os = sp.simplify(OS(EL(Lred, F)))
check("EL_F(L_red) = 0 identically on-shell: F is PURE GAUGE after the constraint", elF_os == 0)

# and Sigma's EL must reproduce the claimed reduced dynamics
W = Function('W')(t)
Ttarget = (KB/(32*pi*G))*(a*D(W, t)**2 - k**2*W**2/a) \
          + a*(Kp*Qb/4 + Ab*Qb**2*(Qb - Q0)**2/(2*Acal(Qb)))*W**2
elSig_os = sp.simplify(OS(EL(Lred, Sg).subs(Sg, W/a).doit()))
elW_target = sp.simplify(OS(EL(Ttarget, W)))
# EL_Sigma at Sigma = W/a equals a * EL_W of L(W) when L(Sigma) = L(W=a Sigma):  chain rule dSigma = dW/a
check("EL_Sigma(L_red)|_{Sigma=W/a} = a * EL_W(T_target): the reduced dynamics IS the claimed final action "
      "(kinetic K_B a/32piG, gradient K_B k^2/32piG a, mass a[nQbar/4 + Ab Qbar^2 ubar^2/(2 Acal(Qbar))])",
      sp.simplify(sp.expand(elSig_os - a*elW_target)) == 0)

# dispersion from the claimed action, derived independently
alpha = KB*a/(32*pi*G)
mu    = Kp*Qb/4 + Ab*Qb**2*(Qb - Q0)**2/(2*Acal(Qb))
# L = alpha Wdot^2 - (KB k^2/(32 pi G a)) W^2 + a mu W^2  ->  Wddot + H Wdot + omega^2 W = 0
om2 = sp.simplify((KB*k**2/(32*pi*G*a) - a*mu)/alpha)
check("omega^2 = k^2/a^2 - (8 pi G/K_B)[K'(Qbar) Qbar + 2 A_b Qbar^2 (Qbar-Q0)^2/Acal(Qbar)]  "
      "(tachyon-type when n Qbar > 0)",
      sp.simplify(om2 - (k**2/a**2 - (8*pi*G/KB)*(Kp*Qb + 2*Ab*Qb**2*(Qb - Q0)**2/Acal(Qb)))) == 0)
check("c_v^2 = 1 exactly: gradient/kinetic ratio = k^2/a^2 with NO K_B left and NO (2-K_B) anywhere",
      sp.simplify((KB*k**2/(32*pi*G*a))/alpha - k**2/a**2) == 0 and not (om2.coeff(k, 2)).has(KB))

# ---------------- gauge invariance, independent route ----------------
# apply S -> S - a xidot, V -> V + a xidot, F -> F - xi to the RAW L2 and demand EL wrt xi vanish on-shell
xi = Function('xi')(t)
L2g = L2
for f_, rep_ in [(S, S - a*sp.diff(xi, t)), (V, V + a*sp.diff(xi, t)), (F, F - xi)]:
    L2g = L2g.subs(f_, rep_)
dL = sp.expand((L2g - L2).doit())
check("gauge invariance: EL_xi(Delta L) = 0 on-shell  (Sigma and Phi invariant by construction)",
      sp.simplify(OS(EL(dL, xi))) == 0)

# ---------------- Einstein-aether cross-check ----------------
c1, c3 = KB, -KB
c14, c13 = c1, c1 + c3
check("ae-theory c_v^2 formula at AeST point (c1=-c3=K_B, c2=c4=0) = 1",
      sp.simplify((c1 - c1**2/2 + c3**2/2)/(c14*(1 - c13)) - 1) == 0)

# ---------------- numbers ----------------
import math
Om, KBn = 4.4e-7, 0.1
print("NUMBER |m_v|/H = sqrt(3*%.1e/%.1f) = %.2e ; 1/ratio = %.0f Hubble times" %
      (Om, KBn, math.sqrt(3*Om/KBn), 1/math.sqrt(3*Om/KBn)))

if nfail:
    print("\n%d CHECK(S) FAILED" % nfail); sys.exit(1)
print("\nALL INDEPENDENT CHECKS PASSED")
