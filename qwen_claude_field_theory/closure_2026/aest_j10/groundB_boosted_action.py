#!/usr/bin/env python3
"""
GROUND-B Part 2: BOOSTED AeST quadratic action around Minkowski.

Aether tilted by solar-system velocity w (along x) wrt the CMB/aether frame:
    A^mu_bg = (1, w, 0, 0)+O(w^2),  d_mu phi_bg = -Q0 A_bg,mu = (Q0,-Q0 w,0,0).
Metric source h_{mn}(x) external.  Signature (-,+,+,+).

Optimisation: every block (E_i, B_i, dQ, F) has a VANISHING or constant
background, hence is O(eps); quadratic products use eta-contraction and the
aether constraint only to O(eps).  We split
    L2(w) = L0 + w*L1 + O(w^2)
and check L0 == rest-frame GROUND-A, then exhibit the O(w) cross terms.
"""
import sympy as sp
KB,lam_s,Q0,K2,w = sp.symbols('K_B lambda_s Q0 K2 w', real=True)
eps = sp.symbols('eps', real=True)
X = sp.symbols('t x y z', real=True); t,x,y,zc=X
eta = sp.diag(-1,1,1,1)

a1=sp.Function('a1')(*X); a2=sp.Function('a2')(*X); a3=sp.Function('a3')(*X)
vf=sp.Function('vf')(*X)
hf=[[None]*4 for _ in range(4)]
for m in range(4):
    for n in range(m,4):
        f=sp.Function(f'h{m}{n}')(*X); hf[m][n]=f; hf[n][m]=f
h=sp.Matrix(4,4, lambda m,n: hf[m][n])
def d(f,mu): return sp.diff(f,X[mu])

# background aether (upper), boosted along x
Abar=[1,w,0,0]
# aether perturbation (upper): spatial a^i free; A^0 solved from constraint to O(eps)
aP=[None,a1,a2,a3]
# constraint g_{mn}A^mA^n=-1, A^mu=Abar+eps*aP(+eps*P1 in slot0), g=eta+eps*h
P1=sp.symbols('P1')
Aup_e=[1+eps*P1, w+eps*a1, eps*a2, eps*a3]
g=eta+eps*h
Cexpr=sp.expand(sp.series(sum(g[m,n]*Aup_e[m]*Aup_e[n] for m in range(4) for n in range(4))+1, eps,0,2).removeO())
P1sol=sp.solve(Cexpr.coeff(eps,1), P1)[0]
Aup=[1+eps*P1sol, w+eps*a1, eps*a2, eps*a3]
print("A^0 O(eps) coeff P1 =", sp.expand(P1sol))

# scalar gradient
dphibg=[Q0,-Q0*w,0,0]
dphi=[dphibg[mu]+d(eps*vf,mu) for mu in range(4)]
# lowered aether with full metric (needed for F and B_i to O(eps))
Alow=[sum(g[m,n]*Aup[n] for n in range(4)) for m in range(4)]

# F to O(eps); eta-raise
F=sp.Matrix(4,4, lambda nu,mu: d(Alow[mu],nu)-d(Alow[nu],mu))
Lmax=-(KB/2)*sum(eta[a_,a_]*eta[b_,b_]*F[a_,b_]**2 for a_ in range(4) for b_ in range(4))
Ei=[F[0,i] for i in range(4)]
Bi=[dphi[i]+Q0*Alow[i] for i in range(4)]
EdotB=sum(Ei[i]*Bi[i] for i in range(1,4))
B2=sum(Bi[i]**2 for i in range(1,4))
dQ=sum(Aup[m]*dphi[m] for m in range(4))-Q0
Lscal=2*(2-KB)*EdotB-(2-KB)*(1+lam_s)*B2+2*K2*dQ**2
Lag=Lmax+Lscal
print("assembling ...")
Lag2=sp.expand(sp.series(Lag,eps,0,3).removeO()).coeff(eps,2)
Lag2=sp.expand(sp.series(Lag2,w,0,2).removeO())
L0=sp.expand(Lag2.coeff(w,0)); L1=sp.expand(Lag2.coeff(w,1))
print("split done")

# ---- reduction check: rebuild rest frame (w=0) ----
def restframe():
    Aups=[1+eps*(h[0,0]/2), eps*a1, eps*a2, eps*a3]
    gg=eta+eps*h
    Alw=[sum(gg[m,n]*Aups[n] for n in range(4)) for m in range(4)]
    dph=[Q0+d(eps*vf,0) if mu==0 else d(eps*vf,mu) for mu in range(4)]
    Fr=sp.Matrix(4,4, lambda nu,mu: d(Alw[mu],nu)-d(Alw[nu],mu))
    Lm=-(KB/2)*sum(eta[a_,a_]*eta[b_,b_]*Fr[a_,b_]**2 for a_ in range(4) for b_ in range(4))
    Eir=[Fr[0,i] for i in range(4)]; Bir=[dph[i]+Q0*Alw[i] for i in range(4)]
    Ls=2*(2-KB)*sum(Eir[i]*Bir[i] for i in range(1,4))-(2-KB)*(1+lam_s)*sum(Bir[i]**2 for i in range(1,4))
    dQr=sum(Aups[m]*dph[m] for m in range(4))-Q0
    return sp.expand(sp.series(Lm+Ls+2*K2*dQr**2,eps,0,3).removeO()).coeff(eps,2)
Lrest=sp.expand(restframe())
diff=sp.simplify(sp.expand(L0-Lrest))
print("="*66)
print("REDUCTION: (L2 at w=0) - (rest-frame GROUND-A) =", diff)
print("REDUCES TO GROUND-A ->", diff==0)

# ---- exhibit O(w) cross terms ----
print("="*66)
pert=[a1,a2,a3,vf]; src=[hf[m][n] for m in range(4) for n in range(m,4)]
def hasany(tm,fs): return any(tm.has(f) for f in fs)
terms=L1.as_ordered_terms()
cross=[tm for tm in terms if hasany(tm,pert) and hasany(tm,src)]
pp=[tm for tm in terms if hasany(tm,pert) and not hasany(tm,src)]
print(f"O(w): total {len(terms)} monomials; source*pert cross = {len(cross)}; pert*pert = {len(pp)}")
print("--- O(w) pert*pert (frame-drag mixing, factored) ---")
sp.pprint(sp.factor(sp.expand(sum(pp))) if pp else sp.Integer(0))
print("--- O(w) source*pert cross terms (all) ---")
for tm in cross: print("   ",tm)

# ---- verify the physically-grouped combined coefficients of key O(w) structures ----
print("="*66); print("GROUPED O(w) coefficients (combine the block contributions):")
def coeff_of(expr, factor):
    return sp.expand(sp.expand(expr).coeff(factor))
# 1) algebraic mass-mixing  a_i * h_{1i}  (i=x): expect -2(2-K_B)(1+lam_s)Q0^2
c_mass = coeff_of(L1, a1*hf[1][1])
print(" coeff[ w * a_x h_xx ] =", sp.factor(c_mass),
      "  expect -2(2-K_B)(1+lam_s)Q0^2 ->",
      sp.simplify(c_mass + 2*(2-KB)*(1+lam_s)*Q0**2)==0)
# 2) scalar delta-Q source coupling  h00 * d_x vf : expect 2 K2 Q0
c_dq = coeff_of(L1, hf[0][0]*sp.diff(vf,x))
print(" coeff[ w * h00 d_x vf ] =", sp.factor(c_dq),
      "  expect 2 K2 Q0 ->", sp.simplify(c_dq-2*K2*Q0)==0)
# 3) screening scalar-source  h_xx * d_x vf : combine
c_sc = coeff_of(L1, hf[1][1]*sp.diff(vf,x))
print(" coeff[ w * h_xx d_x vf ] =", sp.factor(c_sc),
      "  expect -2(2-K_B)(1+lam_s)Q0? ->",
      sp.simplify(c_sc + 2*(2-KB)*(1+lam_s)*Q0)==0)
# 4) electric-source  d_x a_x * d_x h00 : expect -K_B  (from 2(2-K_B)E.B boosted)
c_el = coeff_of(L1, sp.diff(a1,x)*sp.diff(hf[0][0],x))
print(" coeff[ w * d_x a_x d_x h00 ] =", sp.factor(c_el))
