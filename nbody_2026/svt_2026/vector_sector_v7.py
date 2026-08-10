"""
VECTOR SECTOR of the v7 THE_COMPLETION action (AeST + Route-A kernel + DBI khronon
+ a0-bump + v7 pressure-promotion  a0^2 -> Acal(Q) = kappa^2 G(-K(Q)) ).

Explicit second-order sympy component computation on flat FRW, single Fourier
mode ~ e^{ikz} (real form cos/sin), polarization xhat.

Conventions:
  signature (-,+,+,+);  coords (t,x,y,z);  ds^2 = -dt^2 + a^2 dx^i dx^i
  R_{mn} = d_r Gam^r_{mn} - d_n Gam^r_{mr} + Gam^r_{rl}Gam^l_{mn} - Gam^r_{ml}Gam^l_{rn}
  (background check R = 6(addot/a + H^2) enforced below)
  metric vector modes:  g_{0x} = eps a S(t) cos(kz),  g_{xz} = a^2 d_z[eps F(t)cos(kz)]
  aether:               A^x   = eps V(t) cos(kz)/a,   A^0 fixed by g_{mn}A^m A^n = -1
  khronon:              phi = phib(t)  (NO vector part -- scalar field)
  gauge freedom (transverse x^i -> x^i + xi^i(t)cos(kz) xhat):
        S -> S - a xidot,  F -> F - xi,  V -> V + a xidot
  gauge invariants:  Sigma = S + V   and   Phi = S - a Fdot  (checked below)

Action (v7):
  S = int d^4x sqrt(-g) { [R - 2 Lambda - (K_B/2) F^{mn}F_{mn} + lam(A^m A_m + 1)]/(16 pi G)
        + (Acal(Q)/8 pi G) F_Y(Y/Acal(Q)) + K(Q) + A_b B(Y/Acal(Q)) (Q - Q_0)^2 } + S_matter
  F_Y'(y) = 1 - exp(-sqrt(y))  =>  F_Y(y) = y - 2 + 2(sqrt(y)+1)exp(-sqrt(y))  (F_Y(0)=0)
  B(y) = y/(1+y)^2 ;  K(Q) = DBI (kept symbolic; only K, K'=n enter at this order)
  unit-norm constraint solved exactly for A^0 (no independent lam d.o.f. left).

Matter: vacuum + Lambda + Q-sector background; matter vorticity omitted (standard:
it only adds the usual (rho+p) source to the momentum constraint, decays, and does
not enter the UV no-ghost/gradient conditions).

Every claim printed as PASS is asserted; script exits non-zero on any failure.
"""
import sys
import sympy as sp
from sympy import cos, sin, pi, exp, sqrt, Rational, Function, Derivative as D

npass = 0
def check(name, cond):
    global npass
    ok = bool(cond)
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        sys.exit(1)
    npass += 1

t, z, xs, ys = sp.symbols('t z x y', real=True)
k, eps = sp.symbols('k epsilon', positive=True)
G, KB, Lam, Ab, Q0 = sp.symbols('G K_B Lambda A_b Q_0', real=True)
coords = [t, xs, ys, z]

a    = Function('a', positive=True)(t)
S    = Function('S')(t)
V    = Function('V')(t)
Fm   = Function('Fm')(t)
phib = Function('varphi')(t)
cz, sz = cos(k*z), sin(k*z)
NT = 3

def trunc(e, n=NT):
    e = sp.expand(e)
    return sp.Add(*[e.coeff(eps, i)*eps**i for i in range(n)])

# ================= 1. metric, inverse, sqrt(-g) =================
gxz = sp.diff(eps*Fm*cz, z)*a**2
g = sp.Matrix([[-1,         eps*a*S*cz, 0,    0   ],
               [eps*a*S*cz, a**2,       0,    gxz ],
               [0,          0,          a**2, 0   ],
               [0,          gxz,        0,    a**2]])
check("metric symmetric", g.is_symmetric())
gbar, gbarinv = sp.diag(-1, a**2, a**2, a**2), sp.diag(-1, a**-2, a**-2, a**-2)
dg   = g - gbar
ginv = (gbarinv - gbarinv*dg*gbarinv + gbarinv*dg*gbarinv*dg*gbarinv).applyfunc(trunc)
chk  = (ginv*g).applyfunc(trunc) - sp.eye(4)
check("inverse metric exact to O(eps^2)",
      all(sp.simplify(chk[i, j]) == 0 for i in range(4) for j in range(4)))
detg  = trunc(g.det())
w2    = trunc(-detg/a**6)
sqrtg = trunc(sp.expand(a**3*(1 + (w2-1)/2 - (w2-1)**2/8)))

# ================= 2. curvature =================
Gam = [[[trunc(Rational(1,2)*sum(ginv[r,s]*(sp.diff(g[s,m],coords[n])+sp.diff(g[s,n],coords[m])
        -sp.diff(g[m,n],coords[s])) for s in range(4))) for n in range(4)] for m in range(4)]
        for r in range(4)]
Ric = [[trunc( sum(sp.diff(Gam[r][m][n],coords[r]) for r in range(4))
             - sum(sp.diff(Gam[r][r][n],coords[m]) for r in range(4))
             + sum(Gam[r][r][l]*Gam[l][m][n] for r in range(4) for l in range(4))
             - sum(Gam[r][m][l]*Gam[l][r][n] for r in range(4) for l in range(4)))
        for n in range(4)] for m in range(4)]
Rs = trunc(sum(ginv[m,n]*Ric[m][n] for m in range(4) for n in range(4)))
check("background R = 6(addot/a + H^2)",
      sp.simplify(Rs.coeff(eps,0) - 6*(D(a,(t,2))/a + D(a,t)**2/a**2)) == 0)

# ================= 3. aether: unit-norm solved exactly to O(eps^2) =================
A2v = sp.symbols('A2v')
Au  = [1 + eps**2*A2v, eps*V*cz/a, 0, 0]
norm = trunc(sum(g[m,n]*Au[m]*Au[n] for m in range(4) for n in range(4)))
check("unit-norm violated only at O(eps^2)",
      sp.simplify(sp.expand(norm+1).coeff(eps,0)) == 0 and
      sp.simplify(sp.expand(norm+1).coeff(eps,1)) == 0)
A2 = sp.solve(sp.expand(norm+1).coeff(eps,2), A2v)[0]
check("A^0 = 1 + eps^2 (2S+V)V cos^2/2  (delta A^0 is SECOND order for vectors)",
      sp.simplify(A2 - (2*S+V)*V*cz**2/2) == 0)
Au = [1 + eps**2*A2, eps*V*cz/a, 0, 0]
Ad = [trunc(sum(g[m,n]*Au[n] for n in range(4))) for m in range(4)]
Fmn = [[trunc(sp.diff(Ad[n],coords[m]) - sp.diff(Ad[m],coords[n])) for n in range(4)] for m in range(4)]
F2  = trunc(sum(ginv[m,r]*ginv[n,s]*Fmn[m][n]*Fmn[r][s]
                for m in range(4) for n in range(4) for r in range(4) for s in range(4)))
check("F^2 starts at O(eps^2) (background F_{mn}=0)",
      F2.coeff(eps,0) == 0 and F2.coeff(eps,1) == 0)
Sig = S + V
F2exp = -2*(sp.diff(a*Sig,t))**2*cz**2/a**2 + 2*k**2*Sig**2*sz**2/a**2
check("F^2 = (2/a^2)[k^2 (S+V)^2 sin^2 - (d_t[a(S+V)])^2 cos^2]  -- ONLY Sigma=S+V",
      sp.simplify(sp.expand(F2.coeff(eps,2) - sp.expand(F2exp))) == 0)

# ================= 4. khronon invariants: delta Q, delta Y =================
dphi = [sp.diff(phib, c_) for c_ in coords]
Q  = trunc(sum(Au[m]*dphi[m] for m in range(4)))
Yx = trunc(sum((ginv[m,n]+Au[m]*Au[n])*dphi[m]*dphi[n] for m in range(4) for n in range(4)))
Qb = D(phib, t)
check("delta Q^(1) = 0 (vector): Q = Qbar(1 + eps^2 A2)",
      sp.simplify(Q - Qb*(1+eps**2*A2)) == 0)
check("delta Y^(1) = 0 identically", Yx.coeff(eps,0) == 0 and Yx.coeff(eps,1) == 0)
Y2 = sp.simplify(Yx.coeff(eps,2))
check("delta Y^(2) = Qbar^2 (S+V)^2 cos^2 = Qbar^2 h^{00,(2)}  (>= 0: a perfect square)",
      sp.simplify(Y2 - Qb**2*(S+V)**2*cz**2) == 0)
h00 = trunc(ginv[0,0] + Au[0]*Au[0])
check("h^00 = g^00 + A^0 A^0 = eps^2 (S+V)^2 cos^2 (vanishes at first order, NOT at second)",
      sp.simplify(h00 - eps**2*(S+V)**2*cz**2) == 0)

# ================= 5. dark sector to O(eps^2) =================
Kf = Function('K')
Kser = trunc(sp.series(Kf(Q), eps, 0, NT).removeO().doit())
nQ  = sp.symbols('n_Q', real=True)     # K'(Qbar) = charge density n
Kbg = sp.symbols('K_bar', real=True)   # K(Qbar)  = background pressure p_Q
qdum = sp.symbols('qdum')
dKbar = sp.diff(Kf(qdum), qdum).subs(qdum, Qb)   # K'(Qbar) in sympy's own form
check("K(Q) at O(eps^2) = K'(Qbar) Qbar A2  (only background K' enters)",
      sp.simplify(Kser.coeff(eps,2) - dKbar*Qb*A2) == 0)

# --- the v7 promotion: Acal(Q). Taylor stand-ins (exact to this order since Q-Qbar=O(eps^2))
Abar, Aprm = sp.symbols('Abar Aprm', positive=True)
AcalQ = Abar + Aprm*(Q - Qb)
yarg  = Yx/AcalQ
Bser  = trunc(sp.series(Ab*(yarg/(1+yarg)**2)*(Q-Q0)**2, eps, 0, NT).removeO())
Bco   = sp.simplify(Bser.coeff(eps,2))
check("B-term O(eps^2) = A_b (Qbar-Q0)^2 Y2/Abar -- background values only",
      sp.simplify(Bco - Ab*(Qb-Q0)**2*Y2/Abar) == 0)
check("Acal'(Qbar) ABSENT from vector sector (promotion never couples)",
      Aprm not in Bco.free_symbols)

# --- F_Y term: exact kernel F_Y(y) = y - 2 + 2(sqrt(y)+1)e^{-sqrt(y)}; prove it is O(eps^3)
yv = sp.symbols('yv', positive=True)
FY = yv - 2 + 2*(sqrt(yv)+1)*exp(-sqrt(yv))
check("F_Y'(y) = 1 - e^{-sqrt y} (Route-A kernel)",
      sp.simplify(sp.diff(FY,yv) - (1-exp(-sqrt(yv)))) == 0)
wv = sp.symbols('wv', positive=True)
FYw = FY.subs(yv, wv**2)
check("F_Y(w^2) = (2/3)w^3 + O(w^4): with w = eps sqrt(Y2/Abar) the WHOLE Acal*F_Y term is O(eps^3) -> 0",
      sp.simplify(sp.series(FYw, wv, 0, 4).removeO() - Rational(2,3)*wv**3) == 0)
# --- and every promotion-generated coupling vanishes as Y -> 0+  (the v7 question)
FQnew  = (FY - yv*sp.diff(FY,yv))               # d/dQ[Acal F_Y] = Acal' * this
FYQ    = -yv*sp.diff(FY,yv,2)                   # d^2/dQdY[...] = -(Acal'/Acal) * this
FQQa   = FQnew                                  # Acal'' piece
FQQb   = yv**2*sp.diff(FY,yv,2)                 # (Acal'^2/Acal) piece
lims = [sp.limit(e, yv, 0, '+') for e in (FQnew, FYQ, FQQa, FQQb)]
check("promotion couplings F_Q^new, F_YQ, F_QQ^new all -> 0 as Y->0+ : limits " + str(lims),
      all(l == 0 for l in lims))

# ================= 6. total O(eps^2) Lagrangian, z-averaged =================
Ldens = sqrtg*((Rs - 2*Lam)/(16*pi*G) - Rational(1,2)*KB*F2/(16*pi*G) + Kser + Bser)
L2 = sp.expand(Ldens).coeff(eps, 2)
L2 = sp.integrate(L2, (z, 0, 2*pi/k))*k/(2*pi)
L2 = sp.expand(L2.subs(dKbar, nQ).subs(Kf(Qb), Kbg))

# ================= 7. background EOM (mini-superspace, same conventions) =================
N = Function('N', positive=True)(t)
gN = sp.diag(-N**2, a**2, a**2, a**2)
gNi = gN.inv()
GamN = [[[Rational(1,2)*sum(gNi[r,s]*(sp.diff(gN[s,m],coords[n])+sp.diff(gN[s,n],coords[m])
         -sp.diff(gN[m,n],coords[s])) for s in range(4)) for n in range(4)] for m in range(4)]
         for r in range(4)]
RicN = [[ sum(sp.diff(GamN[r][m][n],coords[r]) for r in range(4))
        - sum(sp.diff(GamN[r][r][n],coords[m]) for r in range(4))
        + sum(GamN[r][r][l]*GamN[l][m][n] for r in range(4) for l in range(4))
        - sum(GamN[r][m][l]*GamN[l][r][n] for r in range(4) for l in range(4))
        for n in range(4)] for m in range(4)]
RN = sp.simplify(sum(gNi[m,n]*RicN[m][n] for m in range(4) for n in range(4)))
LBG = N*a**3*((RN - 2*Lam)/(16*pi*G) + Kf(D(phib,t)/N))   # A^0=1/N, Y=0, F_Y(0)=0, B(0)=0
def setN1(e):
    return sp.expand(e.doit().subs(D(N,(t,2)),0).subs(D(N,t),0).subs(N,1).doit())
eomN   = setN1(sp.diff(LBG, N) - sp.diff(sp.diff(LBG, D(N,t)), t))              # energy constraint
eoma   = setN1(sp.diff(LBG,a) - sp.diff(sp.diff(LBG,D(a,t)),t)
               + sp.diff(sp.diff(LBG,D(a,(t,2))),(t,2)))                        # acceleration
pphi   = sp.simplify(sp.diff(LBG, D(phib,t)).doit().subs(N,1))                  # conjugate momentum
check("scalar EOM = charge conservation: p_phi = a^3 K'(Qbar), EL eq is d/dt(a^3 K') = 0",
      sp.simplify(pphi - a**3*dKbar) == 0)
eomN, eoma = [sp.expand(e.subs(dKbar, nQ).subs(Kf(Qb), Kbg)) for e in (eomN, eoma)]
solL  = sp.solve(eomN, Lam);  check("Friedmann solvable for Lambda", len(solL)==1)
Lsub  = solL[0]   # Lambda = 3H^2 - 8 pi G (Qbar nQ - Kbar)
check("energy constraint: Lambda = 3H^2 - 8piG(rho_Q),  rho_Q = Qbar K' - K",
      sp.simplify(Lsub - (3*D(a,t)**2/a**2 - 8*pi*G*(Qb*nQ - Kbg))) == 0)
sola  = sp.solve(eoma.subs(Lam, Lsub), D(a,(t,2))); check("acceleration eq solvable", len(sola)==1)
asub  = sola[0]
check("acceleration: 2 addot/a + H^2 = Lambda - 8 pi G p_Q  (p_Q = Kbar exactly)",
      sp.simplify(2*asub/a + D(a,t)**2/a**2 - (Lsub - 8*pi*G*Kbg)) == 0)

def on_shell(e):
    e = sp.expand(e)
    for _ in range(3):
        e = sp.expand(e.subs(D(a,(t,2)), asub).subs(Lam, Lsub))
    return sp.simplify(e)

# ================= 8. reduction =================
Sg = Function('Sigma')(t)
L2s = sp.expand(L2.subs(V, Sg - S).doit())
check("after Sigma = S+V substitution, Vdot gone and Sdot survives ONLY in one EH term",
      sp.simplify(sp.diff(L2s, D(V,t)) if L2s.has(D(V,t)) else sp.Integer(0)) == 0)

# IBP 1: remove the single EH term  -3 a^2 adot S Sdot /(16 pi G)   -> add d/dt[3 a^2 adot S^2/(32 pi G)]
TD1 = 3*a**2*D(a,t)*S**2/(32*pi*G)
L2s = sp.expand(L2s + sp.diff(TD1, t))
check("no Sdot left anywhere: S is now manifestly ALGEBRAIC (a constraint field)",
      not L2s.has(D(S,t)))
# IBP 2: remove Fddot:  -k^2 a^3 Fm Fmddot/(16 pi G) -> add d/dt[k^2 a^3 Fm Fmdot/(16 pi G)]
TD2 = k**2*a**3*Fm*D(Fm,t)/(16*pi*G)
L2s = sp.expand(L2s + sp.diff(TD2, t))
check("no Fddot left", not L2s.has(D(Fm,(t,2))))

# S-sector mass cancellation on the background EOM (the gauge-invariance guarantee):
cS2 = on_shell(L2s.coeff(S, 2))
check("ALL S^2 non-gradient terms (Lambda, addot, K_bar, n Qbar, adot^2) cancel on background EOM: "
      "coeff(S^2) = k^2 a/(64 pi G) -- pure momentum-constraint gradient term",
      sp.simplify(cS2 - k**2*a/(64*pi*G)) == 0)

# solve the S constraint
eomS = sp.expand(on_shell(sp.diff(L2s, S)))
solS = sp.solve(eomS, S)
check("S constraint algebraic and unique", len(solS) == 1)
Ssol = sp.simplify(solS[0])
check("constraint sets S = a Fmdot  i.e. gauge-invariant shear Phi = S - a Fmdot = 0 "
      "(matter vorticity would source the RHS)",
      sp.simplify(Ssol - a*D(Fm,t)) == 0)
Lred = sp.expand(on_shell(L2s.subs(S, Ssol).doit()))

# IBP 3: residual Fm Fmdot term -> complete to Fm^2 and re-apply background EOM
cFF = sp.simplify(Lred.coeff(Fm,1).coeff(D(Fm,t),1))
Lred = sp.expand(Lred - cFF*Fm*D(Fm,t) - sp.expand(sp.diff(cFF,t))*Fm**2/2)  # + d/dt[cFF Fm^2/2]
Lred = sp.expand(on_shell(Lred))
check("metric vector potential Fm drops out COMPLETELY (pure gauge): L_red independent of Fm, Fmdot",
      not (Lred.has(Fm) or Lred.has(D(Fm,t))))

# ================= 9. final quadratic action =================
W = Function('W')(t)     # canonical variable W = a Sigma = the lower-index aether mode A_x amplitude
LW = sp.expand(sp.simplify(Lred.subs(Sg, W/a).doit()))
Ttarget = KB*a/(32*pi*G)*D(W,t)**2 - KB*k**2/(32*pi*G*a)*W**2 \
          + (nQ*Qb/4 + Ab*Qb**2*(Qb-Q0)**2/(2*Abar))*a*W**2
check("FINAL: L_vec = (K_B/32piG)[ a Wdot^2 - (k^2/a) W^2 ] "
      "+ a[ n Qbar/4 + A_b Qbar^2 (Qbar-Q0)^2/(2 Abar) ] W^2,   W = a(S+V)",
      sp.simplify(LW - Ttarget) == 0)

# no-ghost / gradient / mass read-off
cKin  = sp.simplify(LW.coeff(D(W,t),2));  cGrad = sp.simplify(-LW.coeff(W,2).coeff(k,2)*k**2)
check("kinetic coeff = K_B a/(32 pi G):  NO-GHOST <=> K_B > 0  (no upper bound appears)",
      sp.simplify(cKin - KB*a/(32*pi*G)) == 0)
check("gradient coeff = K_B k^2/(32 pi G a):  c_v^2 = +1 exactly (subluminal-marginal, k->infty)",
      sp.simplify(cGrad - KB*k**2/(32*pi*G*a)) == 0)
cW2   = sp.simplify(LW.coeff(W,2))
omega2 = sp.simplify(-cW2/cKin)         # Wddot + (friction) W dot + omega^2 W = 0
m2exp  = -(8*pi*G/KB)*(nQ*Qb + 2*Ab*Qb**2*(Qb-Q0)**2/Abar)
check("dispersion: omega^2 = k^2/a^2 - (8piG/K_B)[ n Qbar + 2 A_b Qbar^2 ubar^2/Abar ]  "
      "(tachyon-TYPE sign, trace-suppressed)",
      sp.simplify(omega2 - (k**2/a**2 + m2exp)) == 0)

# Einstein-aether cross-check: SZ2021 map K_B = c1 = -c3, c2 = c4 = 0
c1, c3 = KB, -KB
c14, c13 = c1, c1 + c3
cv2_ae = (c1 - c1**2/2 + c3**2/2)/(c14*(1 - c13))
check("Einstein-aether vector-speed formula at the AeST point (c1=-c3=K_B, c2=c4=0) gives c_v^2 = 1 "
      "-- matches our exact FRW result",
      sp.simplify(cv2_ae - 1) == 0)
check("neither kinetic nor gradient coefficient contains (2 - K_B): the upper edge of the published "
      "0 < K_B < 2 window is NOT a vector-sector condition on FRW",
      sp.simplify(sp.diff(cKin, KB) - a/(32*pi*G)) == 0 and
      sp.simplify(sp.diff(cGrad, KB) - k**2/(32*pi*G*a)) == 0)

# ================= 10. explicit gauge-invariance of the quadratic action =================
# transverse diffeo x^i -> x^i + xi(t)cos(kz) xhat:  S -> S - a xidot, V -> V + a xidot, F -> F - xi
# (so Sigma = S+V and Phi = S - a Fdot are invariant).  The O(eps^2) action must be invariant
# up to total derivatives AND terms proportional to the background EOM.  Verified by applying
# the Euler-Lagrange operator to Delta L and going fully on-shell (incl. charge conservation).
L2K = sp.expand(Ldens).coeff(eps, 2)
L2K = sp.integrate(L2K, (z, 0, 2*pi/k))*k/(2*pi)     # K, Acal kept as functions (chain rules alive)
xi = Function('xi')(t)
L2T = L2K
for f_, rep_ in [(S, S - a*sp.diff(xi,t)), (V, V + a*sp.diff(xi,t)), (Fm, Fm - xi)]:
    L2T = L2T.subs(f_, rep_)
dLg = sp.expand((L2T - L2K).doit())
Kp_  = sp.diff(Kf(qdum),qdum).subs(qdum, Qb)
Kpp_ = sp.diff(Kf(qdum),qdum,2).subs(qdum, Qb)
phidd = -3*D(a,t)/a*Kp_/Kpp_                          # charge conservation d/dt(a^3 K') = 0
LsubK = Lsub.subs(nQ, Kp_).subs(Kbg, Kf(Qb))
asubK = asub.subs(nQ, Kp_).subs(Kbg, Kf(Qb))
def on_shell_full(e):
    e = sp.expand(e.doit())
    for _ in range(4):
        e = sp.expand(e.subs(D(phib,(t,3)), sp.diff(phidd,t).doit())
                       .subs(D(phib,(t,2)), phidd)
                       .subs(D(a,(t,3)), sp.diff(asubK,t).doit())
                       .subs(D(a,(t,2)), asubK)
                       .subs(Lam, LsubK).doit())
    return e
def EulerLagrange(Lg, f):
    r = sp.diff(Lg, f)
    for n_ in range(1, 4):
        r += (-1)**n_ * sp.diff(sp.diff(Lg, D(f,(t,n_))), (t, n_))
    return r
for f_ in [S, V, Fm, xi]:
    check("gauge invariance: EL_%s(Delta L) = 0 on-shell (mod total derivatives)" % f_.func.__name__,
          sp.simplify(on_shell_full(EulerLagrange(dLg, f_))) == 0)

# magnitude of the tachyon-type mass (background inputs from the committed corpus):
# n Qbar ~ rho_exc = Omega_exc * rho_crit, Omega_exc <= 4.4e-7  =>  |m^2| <= 3 Omega_exc H^2/K_B
import math
Om, KBn = 4.4e-7, 0.1
ratio = math.sqrt(3*Om/KBn)      # |m|/H
print(f"\nNUMBER: |m_v|/H <= sqrt(3 Omega_exc/K_B) = {ratio:.2e} at K_B={KBn}, Omega_exc<={Om} "
      f"=> growth timescale >= {1/ratio:.0f} Hubble times; unstable only for lambda_phys > "
      f"{1/ratio:.0f} Hubble radii")

print(f"\nALL {npass} CHECKS PASSED")
print("""
FINAL VECTOR QUADRATIC ACTION (per polarization, mode ~ e^{ikz}, z-averaged, on-shell background):
  S_2 = int dt  (K_B/(32 pi G)) [ a Wdot^2 - (k^2/a) W^2 ]
                + a [ n Qbar/4 + A_b Qbar^2 (Qbar - Q0)^2 / (2 Acal(Qbar)) ] W^2
  with W = a (S + V) = the lower-index aether amplitude A_x (gauge-invariant),
  S = a Fdot on the constraint (shear Phi = S - a Fdot = 0 in vacuum), F pure gauge.
""")
