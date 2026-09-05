#!/usr/bin/env python3
r"""
fc_ob_engine_2026.py -- OPERATOR-BASIS engine for the fried-chicken exhaustion step.

Unitary gauge (clock T = t), spatially covariant building blocks
    N, a_i = D_i ln N, K_ij, R_ij, D_i, eps_ijk
on the FROZEN static MOND background of fc_kh_terminal/decisive_reduction.py:
    gamma_ij = delta_ij,  K_ij = 0,  a_i = gbar zhat,  gbar = a0*y0,
scalar perturbations  N = e^phi, N_i = d_i B, gamma_ij = e^{2 psi} delta_ij  (E = 0 residual gauge),
tensor perturbations  gamma_ij = delta_ij + h_ij (TT), N = 1, N_i = 0.

Every geometric object (K_ij, a_i, D_i a_j, R_ij, L_n K_ij, eps^{ijk}, electric Weyl E_ij) is built
EXACTLY and truncated at second order in the perturbation bookkeeping symbol `epsilon`.  Any
coefficient function c(a^2) is expanded about the background value:  c = c0 + c1*delta + c2*delta^2/2,
delta = a^2 - gbar^2 = O(epsilon).

Analysis tools (all can fail):
  hermitian_form   : period-averaged Fourier quadratic form  L2 = (1/2) v^dag H v
  dof_count        : degree in omega of det H  (2 -> one scalar DOF; 4 -> two, etc.)
  static_reduce    : omega = 0 sector; Schur-reduce to the lapse -> S_phi(kx,kz) and slip psi/phi
  dispersion       : integrate out (phi,B) (requires omega-free H_cc) -> A, V, UV speeds
  tensor_speeds    : TT quadratic action on the same background -> c_T^2 per polarization/direction

Conventions identical to decisive_reduction.py (K_ij = (gdot_ij - D_iN_j - D_jN_i)/(2N), K = grad.n,
L2 = N sqrt(gamma)[(1-beta)K_ijK^ij - (1+lambda)K^2 + R3 + a0^2 F(y)],  (W0,W1,W2) = (F,F',F'')(y0)).
"""
import sympy as sp

t, x, y, z = sp.symbols('t x y z', real=True)
X = (x, y, z)
eps = sp.Symbol('epsilon')
a0, y0 = sp.symbols('a0 y0', positive=True)
gbar = a0*y0
beta, lam = sp.symbols('beta lambda', positive=True)
W0, W1, W2 = sp.symbols('W0 W1 W2', real=True)
kx, kz, w = sp.symbols('k_x k_z omega', real=True)
I = sp.I
DELTA = lambda i, j: 1 if i == j else 0
LC = {(0,1,2):1,(1,2,0):1,(2,0,1):1,(0,2,1):-1,(2,1,0):-1,(1,0,2):-1}
def lc(i,j,k): return LC.get((i,j,k),0)

def tr2(e, order=2):
    e = sp.expand(e)
    return sum(e.coeff(eps, n)*eps**n for n in range(order+1))

def mul(*args):
    out = sp.Integer(1)
    for a in args:
        out = tr2(out*a)
    return out

def coeff_fn(name):
    """c(a^2) = c0 + c1*delta + c2*delta^2/2 about the background; returns (symbols, function-of-delta)."""
    c0, c1, c2 = sp.symbols(f'{name}0 {name}1 {name}2', real=True)
    return (c0, c1, c2), (lambda delta: c0 + c1*delta + c2*tr2(delta*delta)/2)

# ======================================================================================
class Geometry:
    """Exact ADM geometry, truncated at O(eps^2), for a given (N, N_i, gamma_ij) ansatz.
    gamma_ij must be given with its inverse, sqrt, and Christoffels (conformally flat or TT)."""
    def __init__(self, N, Ninv, N_dn, gam, ginv, sqrtg, sqrtg_inv, Gam, lnN_grad, dt):
        d = lambda f, i: sp.diff(f, X[i])
        self.d = d; self.dt = dt
        self.N, self.Ninv, self.gam, self.ginv, self.sqrtg, self.sqrtg_inv = N, Ninv, gam, ginv, sqrtg, sqrtg_inv
        self.Gam = Gam
        self.measure = mul(N, sqrtg)
        # shift
        self.N_dn = N_dn
        self.N_up = [tr2(sum(ginv[i][k]*N_dn[k] for k in range(3))) for i in range(3)]
        DN = [[tr2(d(N_dn[j], i) - sum(Gam(k,i,j)*N_dn[k] for k in range(3))) for j in range(3)] for i in range(3)]
        # extrinsic curvature K_ij = (gdot_ij - D_i N_j - D_j N_i)/(2N)
        self.K_dn = [[mul(Ninv, (dt(gam[i][j]) - DN[i][j] - DN[j][i])/2) for j in range(3)] for i in range(3)]
        self.K_ud = [[tr2(sum(ginv[i][k]*self.K_dn[k][j] for k in range(3))) for j in range(3)] for i in range(3)]
        self.K_up = [[tr2(sum(self.K_ud[i][k]*ginv[k][j] for k in range(3))) for j in range(3)] for i in range(3)]
        self.K = tr2(sum(self.K_ud[i][i] for i in range(3)))
        self.KK = tr2(sum(self.K_ud[i][j]*self.K_ud[j][i] for i in range(3) for j in range(3)))
        # acceleration a_i = D_i ln N (exact), a^i, a^2
        self.a_dn = lnN_grad
        self.a_up = [tr2(sum(ginv[i][k]*self.a_dn[k] for k in range(3))) for i in range(3)]
        self.a2 = tr2(sum(self.a_dn[i]*self.a_up[i] for i in range(3)))
        # D_i a_j
        self.Da_dn = [[tr2(d(self.a_dn[j], i) - sum(Gam(k,i,j)*self.a_dn[k] for k in range(3))) for j in range(3)] for i in range(3)]
        self.Da_tr = tr2(sum(ginv[i][j]*self.Da_dn[i][j] for i in range(3) for j in range(3)))   # D_i a^i
        # D_i D_j N / N = D_i a_j + a_i a_j  (exact identity)
        self.DDN_dn = [[tr2(self.Da_dn[i][j] + self.a_dn[i]*self.a_dn[j]) for j in range(3)] for i in range(3)]
        # D_i K (scalar) and D_i K_jk
        self.DK = [d(self.K, i) for i in range(3)]
        self.DK_dn = [[[tr2(d(self.K_dn[j][k], i) - sum(Gam(l,i,j)*self.K_dn[l][k] + Gam(l,i,k)*self.K_dn[j][l] for l in range(3)))
                        for k in range(3)] for j in range(3)] for i in range(3)]
        # Levi-Civita eps^{ijk} = [ijk]/sqrt(gamma)
        self.eps_up = lambda i,j,k: lc(i,j,k)*sqrtg_inv
        # L_n K_ij = (1/N)(K_ij,t - N^k d_k K_ij - K_kj d_i N^k - K_ik d_j N^k)
        self.LnK_dn = [[mul(Ninv, dt(self.K_dn[i][j]) - sum(self.N_up[k]*d(self.K_dn[i][j],k)
                        + self.K_dn[k][j]*d(self.N_up[k],i) + self.K_dn[i][k]*d(self.N_up[k],j) for k in range(3)))
                        for j in range(3)] for i in range(3)]
        self.LnK = mul(Ninv, dt(self.K) - sum(self.N_up[k]*d(self.K,k) for k in range(3)))

    def set_ricci(self, R_dn):
        self.R_dn = R_dn
        self.R_ud = [[tr2(sum(self.ginv[i][k]*R_dn[k][j] for k in range(3))) for j in range(3)] for i in range(3)]
        self.R3 = tr2(sum(self.R_ud[i][i] for i in range(3)))
        # electric Weyl (clock frame), lower indices, trace-free:
        #   E_ij = R_ij + K K_ij - K_ik K^k_j - D_iD_jN/N - L_n K_ij   (TF part)
        Efull = [[tr2(R_dn[i][j] + self.K*self.K_dn[i][j] - sum(self.K_dn[i][k]*self.K_ud[k][j] for k in range(3))
                      - self.DDN_dn[i][j] - self.LnK_dn[i][j]) for j in range(3)] for i in range(3)]
        trE = tr2(sum(self.ginv[i][j]*Efull[i][j] for i in range(3) for j in range(3)))
        self.E_dn = [[tr2(Efull[i][j] - self.gam[i][j]*trE/3) for j in range(3)] for i in range(3)]
        self.E_ud = [[tr2(sum(self.ginv[i][k]*self.E_dn[k][j] for k in range(3))) for j in range(3)] for i in range(3)]
        # magnetic Weyl B_ij = eps_i^{kl} D_k K_lj  (symmetrised)
        Braw = [[tr2(sum(self.gam[i][m]*self.eps_up(m,k,l)*self.DK_dn[k][l][j] for m in range(3) for k in range(3) for l in range(3)))
                 for j in range(3)] for i in range(3)]
        self.B_dn = [[tr2((Braw[i][j]+Braw[j][i])/2) for j in range(3)] for i in range(3)]
        self.B_ud = [[tr2(sum(self.ginv[i][k]*self.B_dn[k][j] for k in range(3))) for j in range(3)] for i in range(3)]

    # ---------------- operator dictionary (densities BEFORE the measure) ----------------
    def operators(self):
        g = self
        K, KK, R3 = g.K, g.KK, g.R3
        Kaa = tr2(sum(g.K_dn[i][j]*g.a_up[i]*g.a_up[j] for i in range(3) for j in range(3)))
        Raa = tr2(sum(g.R_dn[i][j]*g.a_up[i]*g.a_up[j] for i in range(3) for j in range(3)))
        KijDa = tr2(sum(g.K_up[i][j]*g.Da_dn[i][j] for i in range(3) for j in range(3)))
        RijKij = tr2(sum(g.R_ud[i][j]*g.K_ud[j][i] for i in range(3) for j in range(3)))
        DKDK = tr2(sum(g.ginv[i][j]*g.DK[i]*g.DK[j] for i in range(3) for j in range(3)))
        Eaa = tr2(sum(g.E_dn[i][j]*g.a_up[i]*g.a_up[j] for i in range(3) for j in range(3)))
        EE = tr2(sum(g.E_ud[i][j]*g.E_ud[j][i] for i in range(3) for j in range(3)))
        BB = tr2(sum(g.B_ud[i][j]*g.B_ud[j][i] for i in range(3) for j in range(3)))
        EB = tr2(sum(g.E_ud[i][j]*g.B_ud[j][i] for i in range(3) for j in range(3)))
        # parity-odd
        po_aKK = tr2(sum(g.eps_up(i,j,k)*g.a_dn[i]*g.K_dn[j][l]*g.K_ud[l][k] for i in range(3) for j in range(3) for k in range(3) for l in range(3)))
        po_KDK = tr2(sum(g.eps_up(i,j,k)*g.K_dn[i][l]*sum(g.ginv[l][m]*g.DK_dn[j][m][k] for m in range(3)) for i in range(3) for j in range(3) for k in range(3) for l in range(3)))
        po_aDa = tr2(sum(g.eps_up(i,j,k)*g.a_dn[i]*g.Da_dn[j][k] for i in range(3) for j in range(3) for k in range(3)))
        po_aRK = tr2(sum(g.eps_up(i,j,k)*g.a_dn[i]*g.R_dn[j][l]*g.K_ud[l][k] for i in range(3) for j in range(3) for k in range(3) for l in range(3)))
        return dict(K=K, KK=KK, K2=tr2(K*K), R3=R3, a2=g.a2,
                    Kaa=Kaa, Raa=Raa, KDa=tr2(K*g.Da_tr), KijDa=KijDa, Da=g.Da_tr, Da2=tr2(g.Da_tr**2),
                    KKaa=tr2(K*Kaa), Kaa2=tr2(Kaa*Kaa), RK=tr2(R3*K), RijKij=RijKij, DKDK=DKDK,
                    LnK=g.LnK, Eaa=Eaa, EE=EE, BB=BB, EB=EB,
                    po_aKK=po_aKK, po_KDK=po_KDK, po_aDa=po_aDa, po_aRK=po_aRK)

# ======================================================================================
def scalar_geometry():
    """Scalar sector on the frozen background: N=e^phi, N_i=d_i B, gamma=e^{2psi}delta, a_i = gbar zhat + d_i phi."""
    phi = sp.Function('phi')(t,x,z); B = sp.Function('B')(t,x,z); psi = sp.Function('psi')(t,x,z)
    P, Bs, S = eps*phi, eps*B, eps*psi
    d = lambda f,i: sp.diff(f, X[i]); dt = lambda f: sp.diff(f,t)
    N = 1 + P + P**2/2; Ninv = 1 - P + P**2/2
    e2 = 1 + 2*S + 2*S**2; em2 = 1 - 2*S + 2*S**2
    e3 = 1 + 3*S + sp.Rational(9,2)*S**2; em3 = 1 - 3*S + sp.Rational(9,2)*S**2
    gam = [[e2*DELTA(i,j) for j in range(3)] for i in range(3)]
    ginv = [[em2*DELTA(i,j) for j in range(3)] for i in range(3)]
    dS = [d(S,i) for i in range(3)]
    Gam = lambda k,i,j: (dS[j] if k==i else 0) + (dS[i] if k==j else 0) - (dS[k] if i==j else 0)
    N_dn = [d(Bs,i) for i in range(3)]
    lnN_grad = [d(P,0), d(P,1), gbar + d(P,2)]
    G = Geometry(N, Ninv, N_dn, gam, ginv, e3, em3, Gam, lnN_grad, dt)
    lapS = sum(d(d(S,k),k) for k in range(3)); gradS2 = sum(dS[k]**2 for k in range(3))
    R_dn = [[tr2(-d(dS[j],i) + dS[i]*dS[j] - DELTA(i,j)*(lapS + gradS2)) for j in range(3)] for i in range(3)]
    G.set_ricci(R_dn)
    G.fields = (phi, B, psi)
    # y = |a|/a0 expanded to 2nd order in delta = a^2 - gbar^2
    delta = tr2(G.a2 - gbar**2)
    dy = tr2(delta/(2*gbar*a0) - tr2(delta*delta)/(8*gbar**3*a0))
    G.delta = delta
    G.Fpot = tr2(W0 + W1*dy + W2*tr2(dy*dy)/2)     # F(y) about y0 (dimensionless; times a0^2)
    return G

def tensor_geometry(direction, pol):
    """TT sector: gamma = delta + eps h (TT), N = 1, N_i = 0, a_i = gbar zhat (frozen).
    direction: 'x' (k perp a) or 'z' (k along a).  pol: '+' or 'x'."""
    coord = x if direction == 'x' else z
    h = sp.Function('h')(t, coord)
    H = [[0]*3 for _ in range(3)]
    if direction == 'x':
        if pol == '+': H[1][1] = eps*h; H[2][2] = -eps*h
        else:          H[1][2] = H[2][1] = eps*h
    else:
        if pol == '+': H[0][0] = eps*h; H[1][1] = -eps*h
        else:          H[0][1] = H[1][0] = eps*h
    d = lambda f,i: sp.diff(f, X[i]); dt = lambda f: sp.diff(f,t)
    gam = [[DELTA(i,j) + H[i][j] for j in range(3)] for i in range(3)]
    # inverse to O(eps^2): delta - h + h.h
    hh = [[sum(H[i][k]*H[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    ginv = [[tr2(DELTA(i,j) - H[i][j] + hh[i][j]) for j in range(3)] for i in range(3)]
    trhh = sum(hh[i][i] for i in range(3))
    sqrtg = tr2(1 - trhh/4); sqrtg_inv = tr2(1 + trhh/4)
    # Christoffels Gamma^k_ij = (1/2) g^{kl}(d_i g_lj + d_j g_li - d_l g_ij)
    def Gam(k,i,j):
        return tr2(sum(ginv[k][l]*(d(gam[l][j],i) + d(gam[l][i],j) - d(gam[i][j],l)) for l in range(3))/2)
    Gc = [[[Gam(k,i,j) for j in range(3)] for i in range(3)] for k in range(3)]
    Gf = lambda k,i,j: Gc[k][i][j]
    N = sp.Integer(1); Ninv = sp.Integer(1)
    N_dn = [0,0,0]
    lnN_grad = [0, 0, gbar]
    G = Geometry(N, Ninv, N_dn, gam, ginv, sqrtg, sqrtg_inv, Gf, lnN_grad, dt)
    # Ricci: R_ij = d_k G^k_ij - d_j G^k_ik + G^k_kl G^l_ij - G^k_jl G^l_ik
    R_dn = [[tr2(sum(d(Gc[k][i][j],k) - d(Gc[k][i][k],j) for k in range(3))
                 + sum(Gc[k][k][l]*Gc[l][i][j] - Gc[k][j][l]*Gc[l][i][k] for k in range(3) for l in range(3)))
             for j in range(3)] for i in range(3)]
    G.set_ricci(R_dn)
    G.fields = (h,)
    G.delta = tr2(G.a2 - gbar**2)
    return G

# ======================================================================================
def to_fourier_avg(L2, fields, amps, conjs, kvec):
    """Period-averaged Fourier quadratic form.  fields -> (1/2)(v E + v* E*), E = exp(i(k.x - w t))."""
    kk = kvec
    E = sp.exp(I*(kk[0]*x + kk[1]*y + kk[2]*z - w*t))
    subs_field = {f: sp.Rational(1,2)*(a*E + ab/E) for f, a, ab in zip(fields, amps, conjs)}
    e = sp.expand(L2)
    xmap = {}
    for node in e.atoms(sp.Derivative):
        base = node.expr
        if base in subs_field:
            dd = subs_field[base]
            for v, n in node.variable_count:
                dd = sp.diff(dd, v, n)
            xmap[node] = dd
    for fld, rep in subs_field.items():
        xmap[fld] = rep
    Lf = sp.expand(e.xreplace(xmap))
    out = 0
    for term in Lf.as_ordered_terms():
        if term.has(x) or term.has(y) or term.has(z) or term.has(t):
            continue
        out += term
    return sp.expand(out)

def hermitian_form(L2, fields, kvec=(kx, 0, kz)):
    n = len(fields)
    amps = sp.symbols(' '.join(f'v{i}' for i in range(n))) if n > 1 else (sp.Symbol('v0'),)
    conjs = sp.symbols(' '.join(f'vb{i}' for i in range(n))) if n > 1 else (sp.Symbol('vb0'),)
    Lavg = to_fourier_avg(L2, fields, amps, conjs, kvec)
    H = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            H[i,j] = sp.simplify(sp.diff(Lavg, conjs[i], amps[j]))
    herm = sp.simplify(H - H.conjugate().T)
    assert herm == sp.zeros(n, n), f"non-Hermitian form: {herm}"
    return H

def dof_count(H):
    """Number of propagating scalar DOF = (degree in omega of det H)/2."""
    det = sp.expand(sp.cancel(H.det()))
    num, _ = sp.fraction(sp.together(det))
    deg = sp.Poly(sp.expand(num), w).degree()
    return sp.Rational(deg, 2), sp.factor(det)

def static_reduce(H, order=(0,1,2)):
    """omega=0 sector.  Index order: 0=phi (lapse), 1=B (shift), 2=psi.  Returns Schur complement to phi
    (the effective static lapse operator S_phi) and the slip ratio psi/phi for a lapse-only source."""
    H0 = H.subs(w, 0)
    Hcc = H0.extract([1,2],[1,2]); Hcp = H0.extract([1,2],[0]); Hpc = H0.extract([0],[1,2])
    S = sp.cancel(H0[0,0] - (Hpc*Hcc.inv()*Hcp)[0,0])
    # response to a lapse-only source: v = H0^{-1} (1,0,0)
    Hinv = H0.inv()
    slip = sp.cancel(Hinv[2,0]/Hinv[0,0])
    tilt = sp.cancel(Hinv[1,0]/Hinv[0,0])
    return S, slip, tilt

def dispersion(H):
    """Integrate out (phi,B) -> reduced propagator for psi.  Requires H_cc omega-free."""
    Hcc = H.extract([0,1],[0,1])
    if Hcc.has(w):
        return None
    Hcs = H.extract([0,1],[2]); Hsc = H.extract([2],[0,1]); Hss = H[2,2]
    Gred = sp.cancel(Hss - (Hsc*Hcc.inv()*Hcs)[0,0])
    num, den = sp.fraction(sp.together(Gred))
    num = sp.expand(num)
    degw = sp.Poly(num, w).degree()
    A = sp.cancel(num.coeff(w, 2)/den)
    lin = sp.cancel(num.coeff(w, 1)/den)
    V = sp.cancel(-num.coeff(w, 0)/den)
    cpar_UV = sp.cancel(sp.limit(V.subs(kx,0)/kz**2, kz, sp.oo)/sp.limit(A.subs(kx,0), kz, sp.oo))
    cperp_UV = sp.cancel(sp.limit(V.subs(kz,0)/kx**2, kx, sp.oo)/sp.limit(A.subs(kz,0), kx, sp.oo))
    return dict(A=A, lin=lin, V=V, cpar_UV=cpar_UV, cperp_UV=cperp_UV, degw=degw, Gred=Gred)

def tensor_speed(L2, h, direction):
    """Quadratic TT action -> (kinetic coeff of hdot^2, gradient coeff of (dh)^2, c_T^2)."""
    kvec = (kx,0,0) if direction == 'x' else (0,0,kz)
    k = kx if direction == 'x' else kz
    Hm = hermitian_form(L2, (h,), kvec)
    G = sp.expand(sp.cancel(Hm[0,0]))
    Pw = sp.Poly(G, w)
    if Pw.degree() > 2:
        return dict(kin=None, grad=None, cT2=None, higher_time=True, G=G)
    kin = sp.factor(G.coeff(w,2)); grad = sp.factor(-G.coeff(w,0))
    Pk = sp.Poly(sp.expand(-G.coeff(w,0)), k)
    cT2 = sp.factor(sp.cancel(Pk.coeff_monomial(k**2)/kin)) if kin != 0 else None
    return dict(kin=kin, grad=grad, cT2=cT2, higher_time=False, G=G, gradpoly=Pk)
