#!/usr/bin/env python3
r"""
fc_fk_routeB_covariant.py  --  ROUTE-B (independent) finite-k AeST scalar dispersion
====================================================================================
INDEPENDENT of the route-A "assumed K_eff(k)" path.  Here we DERIVE the full scalar-
sector quadratic action of FC-FINAL ( AeST^*  +  a0^2 J_10 , a0 const ) directly from
the covariant Lagrangian by a from-scratch 2nd-order expansion on a perturbed FLRW
background (cosmic time t, comoving z, longitudinal/Newtonian gauge), including:

   L = sqrt(-g)[ R - (K_B/2)F^2 + 2(2-K_B) J^mu d_mu phi - (2-K_B) Y
                 - 4 Lambda + 2 K2 (Q-Q0)^2 ]            (MOND part a0^2 J_10 = O(eps^3), dropped)

Fields (scalar sector): metric potentials Phi (lapse), Psi (curvature); aether
longitudinal potential v (A_i = d_i v, A_0 fixed by the unit norm A^2=-1); scalar
chi = delta phi.  Background: a(t), H, phi0(t) with Qb=phidot0 the condensate (de
Sitter attractor => Qb = Q0 minimum, phiddot0=0).

STRATEGY of THIS file (stage 1): VALIDATION on the flat limit (a=1,H=0 => Minkowski).
We reduce the (chi, v, Phi, Psi) system to physical variables (integrate out the
non-dynamical Phi, Psi) and reproduce the PUBLISHED AeST result
      k_*^2 = (1+lam_s)/lam_s * mu^2,   mu^2 = 2 K2 Q0^2/(2-K_B)
and the ghost band K_eff<0 for k<k_*.  If we reproduce it FROM SCRATCH, the setup is
validated; stage 2 (FLRW) then reads off C_2 and the band character.

Honesty: every step is sympy-verified.  Gravity term R is computed by sympy Ricci
(no hand Poisson coefficient).  No asserted PASS.
"""
import sympy as sp

sp.init_printing()
P = print
def hdr(s): P("\n"+"="*94+"\n"+s+"\n"+"="*94)

# ---------------------------------------------------------------------------
# symbols
# ---------------------------------------------------------------------------
t, z, k = sp.symbols('t z k', real=True)
eps = sp.symbols('epsilon', positive=True)          # bookkeeping order parameter
KB, K2, Q0, Lam = sp.symbols('K_B K2 Q0 Lambda', positive=True)   # AeST params
a = sp.Function('a', positive=True)(t)              # scale factor
phi0 = sp.Function('phi0', real=True)(t)            # background scalar

# perturbation profiles (t-part) x cos(k z)   [scalar sector: all ~ cos(kz)]
# SPATIALLY-FLAT GAUGE: spatial metric unperturbed (Psi=E=0); keep lapse Phi and shift B.
# Phi,B are Lagrange multipliers (Hamiltonian + momentum constraints); v,chi are the 2 DOF.
Phi_t = sp.Function('Phi', real=True)(t)
Bsh_t = sp.Function('Bsh', real=True)(t)     # shift potential:  g_0i = a^2 d_i B
vv_t  = sp.Function('vv',  real=True)(t)
chi_t = sp.Function('chi', real=True)(t)
C = sp.cos(k*z)
Phi = eps*Phi_t*C
Bsh = eps*Bsh_t*C
vv  = eps*vv_t *C
chi = eps*chi_t*C

# ---------------------------------------------------------------------------
# metric (t,x,y,z), scalar perturbations depend on (t,z) only.  Spatially-flat gauge.
#   g_00 = -(1+2Phi),  g_0i = a^2 d_i B,  g_ij = a^2 delta_ij
# ---------------------------------------------------------------------------
g = sp.zeros(4,4)
g[0,0] = -(1+2*Phi)
g[0,3] = a**2*sp.diff(Bsh, z)
g[3,0] = a**2*sp.diff(Bsh, z)
g[1,1] = a**2
g[2,2] = a**2
g[3,3] = a**2
coords = [t, sp.Symbol('x'), sp.Symbol('y'), z]

def series2(expr):
    """truncate to O(eps^2) inclusive, via exact Taylor derivatives (avoids sp.series artifacts)."""
    expr = sp.sympify(expr)
    e0 = expr.subs(eps, 0)
    e1 = sp.diff(expr, eps).subs(eps, 0)
    e2 = sp.diff(expr, eps, 2).subs(eps, 0)/2
    return sp.expand(e0 + e1*eps + e2*eps**2)

ginv = g.inv()
ginv = ginv.applyfunc(series2)
detg = series2(g.det())
sqrtmg = series2(sp.sqrt(-detg))

# ---------------------------------------------------------------------------
# Christoffel, Ricci, Ricci scalar  (to O(eps^2))
# ---------------------------------------------------------------------------
def christoffel(g, ginv, coords):
    n=4; Gamma=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for nn in range(m,n):
                s=0
                for r in range(n):
                    s+= ginv[l,r]*(sp.diff(g[r,m],coords[nn])+sp.diff(g[r,nn],coords[m])-sp.diff(g[m,nn],coords[r]))
                s=series2(s*sp.Rational(1,2))
                Gamma[l][m][nn]=s; Gamma[l][nn][m]=s
    return Gamma

P("building Christoffel...")
Gamma = christoffel(g, ginv, coords)

def ricci_tensor(Gamma, coords):
    n=4; Ric=sp.zeros(n,n)
    for m in range(n):
        for nn in range(m,n):
            s=0
            for l in range(n):
                s+= sp.diff(Gamma[l][m][nn],coords[l]) - sp.diff(Gamma[l][m][l],coords[nn])
                for r in range(n):
                    s+= Gamma[l][l][r]*Gamma[r][m][nn]-Gamma[l][nn][r]*Gamma[r][m][l]
            s=series2(s); Ric[m,nn]=s; Ric[nn,m]=s
    return Ric

P("building Ricci...")
Ric = ricci_tensor(Gamma, coords)
Rscalar = 0
for m in range(4):
    for nn in range(4):
        Rscalar += ginv[m,nn]*Ric[m,nn]
Rscalar = series2(Rscalar)
P("Ricci scalar built.")

# ---------------------------------------------------------------------------
# aether:  A_i = d_i v  (only A_z = d_z v nonzero);  A_0 from unit norm A^2 = -1
# ---------------------------------------------------------------------------
A_low = sp.zeros(4,1)
A0sym = sp.Function('A0pert', real=True)(t)          # placeholder, solved below
# parametrize A_0 = -(1 + eps*u1 + eps^2*u2) with u1,u2 to be fixed by A^2=-1
u1 = sp.Function('u1', real=True)(t); u2 = sp.Function('u2', real=True)(t)
A_low[0] = -(1 + eps*u1*C + eps**2*u2)               # u2 kept z-indep piece (2nd order avg)
A_low[3] = sp.diff(vv, z)                             # A_z = d_z v  (= -eps vv_t k sin(kz))
# A^2 = g^{mn} A_m A_n
A2 = 0
for m in range(4):
    for nn in range(4):
        A2 += ginv[m,nn]*A_low[m]*A_low[nn]
A2 = series2(A2)
# solve order by order:  A2 = -1
e1 = series2(A2 + 1).coeff(eps,1)
e2 = series2(A2 + 1).coeff(eps,2)
sol_u1 = sp.solve(sp.Eq(e1,0), u1)[0]
u1v = sp.simplify(sol_u1)
# substitute u1 then solve 2nd order for u2 (average of cos^2 -> use identity later; here keep z)
A_low2 = A_low.subs(u1, u1v)
A2b = 0
for m in range(4):
    for nn in range(4):
        A2b += ginv[m,nn]*A_low2[m]*A_low2[nn]
A2b = series2(A2b)
e2b = series2(A2b+1).coeff(eps,2)
# e2b depends on z through cos^2/sin^2; replace to constant via averaging AFTER solving u2 pointwise:
sol_u2 = sp.solve(sp.Eq(e2b,0), u2)[0]
A_low2 = A_low2.subs(u2, sol_u2)
# raise index
A_up = sp.zeros(4,1)
for m in range(4):
    s=0
    for nn in range(4):
        s+= ginv[m,nn]*A_low2[nn]
    A_up[m]=series2(s)
P("aether A_mu solved to O(eps^2): u1 =", u1v)

# ---------------------------------------------------------------------------
# F_{mu nu} = d_mu A_nu - d_nu A_mu ;  F^2 = F_{mn}F^{mn}
# ---------------------------------------------------------------------------
F = sp.zeros(4,4)
for m in range(4):
    for nn in range(4):
        F[m,nn] = sp.diff(A_low2[nn], coords[m]) - sp.diff(A_low2[m], coords[nn])
F2 = 0
for m in range(4):
    for nn in range(4):
        for r in range(4):
            for s_ in range(4):
                F2 += ginv[m,r]*ginv[nn,s_]*F[m,nn]*F[r,s_]
F2 = series2(F2)

# ---------------------------------------------------------------------------
# J^mu = A^nu nabla_nu A^mu = A^nu( d_nu A^mu + Gamma^mu_{nu l} A^l )
# ---------------------------------------------------------------------------
J_up = sp.zeros(4,1)
for m in range(4):
    s=0
    for nn in range(4):
        cov = sp.diff(A_up[m], coords[nn])
        for l in range(4):
            cov += Gamma[m][nn][l]*A_up[l]
        s += A_up[nn]*cov
    J_up[m]=series2(s)

# phi, Q, Y
phi = phi0 + chi
dphi = sp.Matrix([sp.diff(phi, coords[i]) for i in range(4)])
Q = 0
for m in range(4):
    Q += A_up[m]*dphi[m]
Q = series2(Q)
# Y = (g^{mn}+A^m A^n) dphi_m dphi_n
Y = 0
for m in range(4):
    for nn in range(4):
        Y += (ginv[m,nn]+A_up[m]*A_up[nn])*dphi[m]*dphi[nn]
Y = series2(Y)
# J^mu d_mu phi
Jdphi = 0
for m in range(4):
    Jdphi += J_up[m]*dphi[m]
Jdphi = series2(Jdphi)

P("Q,Y,F2,J.dphi built. sample: Q =", sp.simplify(Q.coeff(eps,0)), " (background)")

# ---------------------------------------------------------------------------
# assemble Lagrangian density (drop MOND O(eps^3)); enforce background at min: Qb=Q0
# ---------------------------------------------------------------------------
Lpot = -4*Lam + 2*K2*(Q-Q0)**2                       # = -F(0,Q)
Ldens = sqrtmg*( Rscalar - (KB/2)*F2 + 2*(2-KB)*Jdphi - (2-KB)*Y + Lpot )
Ldens = series2(Ldens)

# set background scalar at condensate minimum on the attractor: phidot0 = Q0 (const), phiddot0=0
# implement by substituting Derivative(phi0,t)->Q0 and higher ->0 in the quadratic action
def bg_condensate(expr):
    expr = expr.subs(sp.Derivative(phi0,(t,2)), 0)
    expr = expr.subs(sp.Derivative(phi0,t), Q0)
    return expr

L2 = Ldens.coeff(eps,2)
L2 = bg_condensate(L2)

# ---------------------------------------------------------------------------
# spatial average over z : cos^2 ->1/2, sin^2 ->1/2, sin*cos ->0, leftover cos,sin ->0
# ---------------------------------------------------------------------------
def zaverage(expr):
    expr = sp.expand(expr)
    c = sp.cos(k*z); s = sp.sin(k*z)
    expr = expr.subs(c**2, sp.Rational(1,2)).subs(s**2, sp.Rational(1,2))
    expr = expr.subs(c*s, 0).subs(s*c, 0)
    expr = expr.subs(c, 0).subs(s, 0)   # kill leftover linear (tadpole) terms
    return sp.expand(expr)

P("z-averaging L2 ...")
L2avg = bg_condensate(zaverage(L2))
P("L2 (z-averaged) assembled.")

# ---------------------------------------------------------------------------
# Convert to a polynomial in INDEPENDENT symbols {field, fielddot}; provide IBP so that
# only first time-derivatives remain (move all second derivatives onto partners).
# ---------------------------------------------------------------------------
FLD = [('Phi',Phi_t), ('Bsh',Bsh_t), ('vv',vv_t), ('chi',chi_t)]
sym  = {name: sp.Symbol(name, real=True)            for name,_ in FLD}
symd = {name: sp.Symbol(name+'_d', real=True)       for name,_ in FLD}
symdd= {name: sp.Symbol(name+'_dd', real=True)      for name,_ in FLD}

def ibp_second_derivs(expr):
    """Integrate by parts to remove 2nd time derivatives: f*g'' -> -f'*g' (drop total deriv)."""
    expr = sp.expand(expr)
    changed=True
    while changed:
        changed=False
        for nm,f in FLD:
            fdd = sp.Derivative(f,(t,2))
            if expr.has(fdd):
                # coefficient of fdd:  expr = A*fdd + rest ; replace A*fdd -> -dA/dt * fdot
                A = expr.coeff(fdd,1)
                rest = expr - A*fdd
                expr = sp.expand(rest - sp.diff(A,t)*sp.Derivative(f,t))
                changed=True
    return expr

def to_poly_syms(expr):
    """map functions and their 1st t-derivatives to independent symbols."""
    expr = sp.expand(expr)
    for nm,f in FLD:
        expr = expr.subs(sp.Derivative(f,t), symd[nm])
    for nm,f in FLD:
        expr = expr.subs(f, sym[nm])
    return sp.expand(expr)

# ---------------------------------------------------------------------------
# GENERAL reduction+dispersion (reused flat & FLRW).  Standard form:
#   L = 1/2 qd^T K qd + qd^T N q - 1/2 q^T Om q ,  split N=N_s+N_a ,
#   qd^T N_s q = 1/2 d/dt(q^T N_s q) - 1/2 q^T Ndot_s q  ->  Om_eff = Om + Ndot_s ; keep N_a.
# EOM (WKB, leading):  K qdd + (Kdot+2N_a) qd + (Ndot_a + Om_eff) q = 0
#   -> M(w) = -w^2 K - i w (Kdot + 2 N_a) + (Ndot_a + Om_eff)
# ---------------------------------------------------------------------------
def matrices_over(Lpoly, names):
    n=len(names)
    q =[sym[nm]  for nm in names]
    qd=[symd[nm] for nm in names]
    K=sp.zeros(n,n); N=sp.zeros(n,n); Om=sp.zeros(n,n)
    for i in range(n):
        for j in range(n):
            K[i,j]  = sp.diff(Lpoly, qd[i], qd[j])
            N[i,j]  = sp.diff(Lpoly, qd[i], q[j])
            Om[i,j] = -sp.diff(Lpoly, q[i], q[j])
    return K,N,Om,q,qd

def dt_coeff(M):
    """time-derivative of a coefficient matrix (explicit a(t) dependence only)."""
    return M.applyfunc(lambda e: sp.diff(e, t))

def build_Lstd(K,N,Om,q,qd):
    """reconstruct standardized polynomial Lagrangian with N->N_a and Om->Om+Ndot_s."""
    Ns=(N+N.T)/2; Na=(N-N.T)/2
    Om_eff = Om + dt_coeff(Ns)
    n=len(q)
    L = 0
    for i in range(n):
        for j in range(n):
            L += sp.Rational(1,2)*K[i,j]*qd[i]*qd[j]
            L += Na[i,j]*qd[i]*q[j]
            L += -sp.Rational(1,2)*Om_eff[i,j]*q[i]*q[j]
    return sp.expand(L), K, Na, Om_eff

def eom_matrix(L2_expr, order=('Phi','Bsh','vv','chi'), extra_subs=None):
    """Build the WKB linearized-EOM matrix M(w) over the given field ORDER, from the
    quadratic Lagrangian.  M(w) = -w^2 K - i w (Kdot + 2 N_a) + (Ndot_a + Om + Ndot_s),
    where the last group is Om_eff (symmetric-mixing total-derivative absorbed)."""
    L = ibp_second_derivs(L2_expr)
    L = to_poly_syms(L)
    if extra_subs: L = sp.expand(L.subs(extra_subs))
    K,N,Om,q,qd = matrices_over(L, order)
    Ns=(N+N.T)/2; Na=(N-N.T)/2
    Om_eff = Om + dt_coeff(Ns)
    Kdot = dt_coeff(K); Nadot = dt_coeff(Na)
    w=sp.symbols('omega')
    M = -w**2*K - sp.I*w*(Kdot + 2*Na) + (Nadot + Om_eff)
    return dict(M=M, K=K, Na=Na, Om_eff=Om_eff, w=w, order=list(order), L=L)

def reduce_and_disperse(L2_expr, elim=('Phi','Bsh'), dyn=('vv','chi'), extra_subs=None, label=""):
    """Physical dispersion via Schur determinant identity:
       det M4 = det(Mcc) * det(Mred)  =>  physical dispersion = det(M4)/det(Mcc).
    Multipliers with an identically-zero row+col in M (decoupled) are dropped."""
    order = list(elim)+list(dyn)
    info = eom_matrix(L2_expr, order=order, extra_subs=extra_subs)
    M=info['M']; w=info['w']
    # drop decoupled fields (zero row and zero col)
    keep=[i for i in range(M.rows) if any(sp.simplify(M[i,j])!=0 for j in range(M.cols))
                                   or any(sp.simplify(M[j,i])!=0 for j in range(M.rows))]
    order2=[order[i] for i in keep]
    M=M[keep,keep]
    elim2=[nm for nm in elim if nm in order2]; dyn2=[nm for nm in dyn if nm in order2]
    cidx=[order2.index(nm) for nm in elim2]; didx=[order2.index(nm) for nm in dyn2]
    Mcc = M[cidx,cidx] if cidx else sp.eye(0)
    detM  = sp.expand(M.det())
    detMcc= sp.expand(Mcc.det()) if cidx else sp.Integer(1)
    disp  = sp.cancel(detM/detMcc) if detMcc!=0 else sp.expand(detM)
    disp  = sp.simplify(disp)
    return dict(M=M, K=info['K'], Na=info['Na'], Om=info['Om_eff'],
                detM=detM, detMcc=detMcc, disp=disp, w=w, order=order2,
                elim=elim2, dyn=dyn2, Mcc=Mcc)

# ---------------------------------------------------------------------------
# FLAT VALIDATION:  a->1, H->0 (Minkowski), Lambda->0.
# ---------------------------------------------------------------------------
hdr("STAGE 1  --  FLAT (Minkowski) VALIDATION:  reproduce k_*^2 = 2 mu^2 (lam_s=1)")
def flatten(expr):
    expr = expr.subs(sp.Derivative(a,(t,2)),0).subs(sp.Derivative(a,t),0).subs(a,1).subs(Lam,0)
    return sp.expand(expr)
L2flat = flatten(L2avg)
P("contains Phidot?", L2flat.has(sp.Derivative(Phi_t,t)), " Bshdot?", L2flat.has(sp.Derivative(Bsh_t,t)))

res = reduce_and_disperse(L2flat, label="flat")
w = res['w']
disp = sp.factor(res['disp'])
P("\nphysical dispersion  det(M4)/det(Mcc) = 0  ->")
P("   disp =", disp)

# solve for omega^2 (the dispersion should be even in w on flat: no frame mixing at H=0)
poly_w = sp.Poly(sp.expand(res['disp']), w)
P("\n   powers of omega present:", sorted(set(m[0] for m in poly_w.monoms())))
sol_w2 = sp.solve(sp.Eq(res['disp'],0), w**2)
P("   omega^2 roots:", [sp.simplify(r) for r in sol_w2])

# published anchors
mu2 = 2*K2*Q0**2/(2-KB)
P("\npublished anchors: mu^2 = 2 K2 Q0^2/(2-K_B) =", mu2)
P("   lam_s=1 => k_*^2 = (1+lam_s)/lam_s * mu^2 = 2 mu^2 =", sp.simplify(2*mu2))
for r in sol_w2:
    P("   root factored:", sp.factor(sp.simplify(r)))
P("\n[stage-1 done] identify ghost band (omega^2<0 or K_eff<0) and its boundary k_*.")
