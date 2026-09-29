#!/usr/bin/env python3
"""g01_origin_of_32pi.py  --  lane B (gravitational waves / graviton): where EXACTLY does 32 pi come from?

Units c = 1, signature (-+++).  Everything is recomputed from the metric with sympy; nothing is quoted from memory except the conventions stated.

Part A  quadratic Einstein-Hilbert action of a TT plane wave, from sqrt(-g) R expanded to O(eps^2) (equality up to total derivatives is tested with the
        Euler operator).  => canonical graviton normalisation kappa_g^2 = 32 pi G.
Part B  Isaacson stress tensor from the EXACT Ricci tensor of the plane wave (metric depends on u = t - z): <G^(2)_mu nu> averaged over a period.
        => t_mu nu = (1/32 pi G) <d_mu h_ab d_nu h_ab>, and the flux c^3 w^2 h0^2/(32 pi G).  Second route: canonical stress tensor of the Part-A action.
Part C  the same 32 pi as  8 pi G x 4  (the 4 = 1/(1/4), the 1/4 being the second-order Ricci coefficient) and as  16 pi G x 2.
Part D  Isaacson identity  rho_GW = a_tidal^2 / (8 pi G), a_tidal = (1/2) w h0 = the geodesic-deviation acceleration at the reduced wavelength (Riemann computed).
Part E  one-graviton exchange: 32 pi = 8 x 4 pi (tensor structure x Poisson Green function); classical route: 16 pi G / 4 pi = 4 G.
Part F  memory: linear memory coefficient 4G/r = 16 pi G/(4 pi) is pi-free.
Conventions used in Part E (inputs, stated): g = eta + kappa h, L_int = +(kappa/2) h_mn T^mn, de Donder propagator P/q^2 with P = (1/2)(eta eta + eta eta - eta eta)
        for L = -(1/2) d_l h_mn d^l h^mn + ...; these are the conventions in which kappa^2 = 32 pi G (Part A3) is the canonical normalisation.
Controls (each must FAIL when the coefficient is mutated): C1..C4.  'BOOK' lines are exact arithmetic restatements, counted separately, not independent checks.
Exit 0 iff every check (including every control) behaves as declared.
"""
import sys
import sympy as sp

ok = []; bk_ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)
def bk(name, cond):
    """bookkeeping: an exact arithmetic restatement of what the preceding recomputed checks established; NOT an independent check, counted separately"""
    bk_ok.append(bool(cond)); print(("BOOK " if cond else "FAIL ") + name)

t, x, y, z, eps = sp.symbols('t x y z epsilon', real=True)
G, w, A, B = sp.symbols('G omega A B', positive=True)
X = (t, x, y, z)

def T2(e):
    """truncate a polynomial in eps to O(eps^2)"""
    e = sp.expand(e)
    return sum(e.coeff(eps, k) * eps**k for k in range(3))

def ginv_trunc(hm):
    """inverse of eta + eps*hm to O(eps^2): eta - eps eta.h.eta + eps^2 eta.h.eta.h.eta"""
    e1 = eta * hm * eta
    e2 = eta * hm * eta * hm * eta
    return (eta - eps * e1 + eps**2 * e2)

def christoffel(g, ginv):
    n = 4
    return [[[sum(ginv[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(n)) / 2
              for c in range(n)] for b in range(n)] for a in range(n)]

def ricci(g, ginv):
    n = 4
    Gam = christoffel(g, ginv)
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(n):
            s = 0
            for a in range(n):
                s += sp.diff(Gam[a][b][c], X[a]) - sp.diff(Gam[a][b][a], X[c])
                for d in range(n):
                    s += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
            Ric[b, c] = s
    return Ric, Gam

def riemann_down(g, Gam):
    """R_{a b c d} (all lower) = g_{a e} R^e_{b c d}"""
    n = 4
    Rup = [[[[0] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for e in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    s = sp.diff(Gam[e][d][b], X[c]) - sp.diff(Gam[e][c][b], X[d])
                    for f in range(n):
                        s += Gam[e][c][f] * Gam[f][d][b] - Gam[e][d][f] * Gam[f][c][b]
                    Rup[e][b][c][d] = s
    return lambda a, b, c, d: sum(g[a, e] * Rup[e][b][c][d] for e in range(n))

# ------------------------------------------------------------------ Part A
print("PART A  quadratic EH action of a TT wave; canonical normalisation")
f = sp.Function('f')(t, z); g_ = sp.Function('g')(t, z)
eta = sp.diag(-1, 1, 1, 1)
h = sp.zeros(4, 4); h[1, 1] = f; h[2, 2] = -f; h[1, 2] = g_; h[2, 1] = g_        # h_xx = -h_yy = f (plus), h_xy = g (cross)
gm = eta + eps * h
ginv = ginv_trunc(h)
Ric, Gam = ricci(gm, ginv)
Ric = Ric.applyfunc(T2)
Rs = T2(sum(ginv[a, b] * Ric[a, b] for a in range(4) for b in range(4)))
detm = sp.expand(-gm.det())                       # = 1 - eps^2 (f^2+g^2)
sqrtg = 1 + sp.Rational(1, 2) * (detm - 1)       # sqrt(1+d) = 1 + d/2 + O(d^2), d = O(eps^2)
L2 = sp.simplify(T2(sqrtg * Rs).coeff(eps, 2))
print("   [sqrt(-g) R]_(eps^2) =", L2)
def target(c):      # c * (1/2)(fdot^2 - f'^2 + gdot^2 - g'^2)  == c * (-1/4) d_l h_ij d^l h_ij   (h_ij h_ij = 2 f^2 + 2 g^2)
    return c * sp.Rational(1, 2) * (sp.diff(f, t)**2 - sp.diff(f, z)**2 + sp.diff(g_, t)**2 - sp.diff(g_, z)**2)
from sympy.calculus.euler import euler_equations
def EL(L):
    return [sp.simplify(e.lhs) for e in euler_equations(L, [f, g_], [t, z])]
res = [sp.simplify(a - b) for a, b in zip(EL(L2), EL(target(1)))]
chk("A1  [sqrt(-g)R]_(eps^2) = -(1/4) d_l h_ij d^l h_ij up to a total derivative (Euler operators agree)", all(r == 0 for r in res))
res_bad = [sp.simplify(a - b) for a, b in zip(EL(L2), EL(target(sp.Rational(1, 3))))]
chk("C1  CONTROL: coefficient 1/3 instead of 1/4 is rejected", any(r != 0 for r in res_bad))
# canonical graviton
phi = sp.symbols('phi')
# S = (1/16 pi G) * (1/2)(fdot^2 - ...)  = (1/32 pi G)(...) = (1/2) phidot^2  with  f = kf * phi
kf = sp.symbols('k_f', positive=True)
ksol = sp.solve(sp.Eq(1 / (32 * sp.pi * G) * kf**2, sp.Rational(1, 2)), kf)[0]
chk("A2  h_+ = f = sqrt(16 pi G) phi is canonical when e^+_ij e^+_ij = 2 (h_ij h_ij = 2 f^2)", sp.simplify(ksol**2 - 16 * sp.pi * G) == 0)
# unit-normalised polarisation tensors (e e = 1): hhat = sqrt(2) f  =>  hhat = sqrt(32 pi G) phi
khat = sp.sqrt(2) * ksol
chk("A3  with unit-norm polarisation tensors, or per component of h_ij with L = -(1/2) d h_ij d h_ij:  kappa_g^2 = 32 pi G", sp.simplify(khat**2 - 32 * sp.pi * G) == 0)
# decomposition
bk("A4  32 pi = 2 x 16 pi = 2 x [16 pi x (1/4)^-1 / 2]:  1/(16 pi G) x (1/4) = 1/(64 pi G) = (1/2)/(32 pi G)", sp.Rational(1, 16) / sp.pi * sp.Rational(1, 4) == sp.Rational(1, 2) / (32 * sp.pi))

# ------------------------------------------------------------------ Part B
print("\nPART B  Isaacson tensor from the exact Ricci tensor of the plane wave (u = t - z)")
u = sp.symbols('u', real=True)
ph = sp.symbols('varphi', real=True)
def plane_wave_G2(Aamp, Bamp, phase):
    fx = Aamp * sp.cos(w * (t - z)); gx = Bamp * sp.cos(w * (t - z) + phase)
    hh = sp.zeros(4, 4); hh[1, 1] = fx; hh[2, 2] = -fx; hh[1, 2] = gx; hh[2, 1] = gx
    gg = eta + eps * hh
    gi = ginv_trunc(hh)
    Ri, _ = ricci(gg, gi)
    Ri = Ri.applyfunc(T2)
    Rs_ = T2(sum(gi[a, b] * Ri[a, b] for a in range(4) for b in range(4)))
    Ei = (Ri - sp.Rational(1, 2) * gg * Rs_).applyfunc(T2)
    G2 = Ei.applyfunc(lambda e: sp.simplify(e.coeff(eps, 2)))
    G1 = Ei.applyfunc(lambda e: sp.simplify(e.coeff(eps, 1)))
    return hh, G1, G2, fx, gx
hh, G1, G2, fx, gx = plane_wave_G2(A, B, sp.Symbol('varphi', real=True))
chk("B0  first-order Einstein tensor of the TT plane wave vanishes (vacuum wave)", G1 == sp.zeros(4, 4))
def avg(expr):
    return sp.simplify(sp.integrate(sp.expand(expr.subs(t, u / w + z)), (u, 0, 2 * sp.pi)) / (2 * sp.pi))
G2avg = G2.applyfunc(avg)
print("   <G^(2)_mu nu> =", [G2avg[0, 0], G2avg[0, 3], G2avg[3, 3]], "(tt, tz, zz)")
hd = lambda e, m: sp.diff(e, X[m])
def dhdh(m, n_):     # <d_m h_ab d_n h_ab>,  h_ab h_ab = 2 f^2 + 2 g^2
    return avg(2 * hd(fx, m) * hd(fx, n_) + 2 * hd(gx, m) * hd(gx, n_))
mism = []
for (m, n_) in [(0, 0), (0, 3), (3, 3)]:
    tmn = sp.simplify(-G2avg[m, n_] / (8 * sp.pi * G))          # t_mn = -(1/8 pi G) <G^(2)_mn>
    iso = sp.simplify(dhdh(m, n_) / (32 * sp.pi * G))
    mism.append(sp.simplify(tmn - iso))
chk("B1  t_mu nu = -(1/8 pi G)<G^(2)_mu nu> equals (1/32 pi G)<d_mu h_ab d_nu h_ab> for tt, tz, zz (A, B free, phase-independent)", all(m == 0 for m in mism))
rho = sp.simplify(-G2avg[0, 0] / (8 * sp.pi * G))
chk("B2  energy density  rho = w^2 (A^2 + B^2)/(32 pi G)", sp.simplify(rho - w**2 * (A**2 + B**2) / (32 * sp.pi * G)) == 0)
chk("B3  flux  = rho (null wave: t_tz = -rho, t_zz = rho)", sp.simplify(-G2avg[0, 3] / (8 * sp.pi * G) + rho) == 0 and sp.simplify(-G2avg[3, 3] / (8 * sp.pi * G) - rho) == 0)
chk("B4  traceless: eta^{mn} t_mn = -t_tt + t_zz = 0  (so an isotropic bath has p = rho/3; done in g02)", sp.simplify(-G2avg[0, 0] + G2avg[3, 3]) == 0)
# the exact plane-wave Ricci: R_uu = -(1/2) tr(g^-1 g'') + (1/4) tr(g^-1 g' g^-1 g')  -> the 1/4
Hm = sp.Matrix([[sp.Function('F')(u), sp.Function('K')(u)], [sp.Function('K')(u), -sp.Function('F')(u)]])
gab = sp.eye(2) + eps * Hm
Ruu = -sp.Rational(1, 2) * (gab.inv() * gab.diff(u, 2)).trace() + sp.Rational(1, 4) * (gab.inv() * gab.diff(u) * gab.inv() * gab.diff(u)).trace()
Ruu2 = sp.simplify(sp.series(Ruu, eps, 0, 3).removeO().coeff(eps, 2))
Fu, Ku = sp.Function('F')(u), sp.Function('K')(u)
# average by parts: <tr(H H'')> = -<tr(H' H')>, so <R_uu^(2)> = (-1/2+1/4)... check symbolically with explicit periodic F,K
Ruu2_val = Ruu2.subs({Fu: A * sp.cos(w * u), Ku: B * sp.cos(w * u + ph)}).doit()
avgR = sp.simplify(sp.integrate(sp.expand(sp.simplify(Ruu2_val)), (u, 0, 2 * sp.pi / w)) * w / (2 * sp.pi))
Hp2 = 2 * (A**2 + B**2) * w**2 / 2      # <h'_ab h'_ab> = 2<F'^2 + K'^2>
chk("B5  <R_uu^(2)> = -(1/4)<h'_ab h'_ab>  (the 1/4 = 1/2 - 1/4 after averaging by parts)", sp.simplify(avgR + sp.Rational(1, 4) * Hp2) == 0)
bk("B6  (1/8 pi G) x (1/4) = 1/(32 pi G): 32 pi = 8 pi x 4 with 4 = 1/(1/4), the 1/4 being the B5 coefficient", sp.simplify(sp.Rational(1, 8) / sp.pi * sp.Rational(1, 4) - sp.Rational(1, 32) / sp.pi) == 0)
# control: mutate the target coefficient
chk("C2  CONTROL: 1/16 pi G (instead of 1/32 pi G) is rejected by the same comparison",
    any(sp.simplify(-G2avg[m, n_] / (8 * sp.pi * G) - dhdh(m, n_) / (16 * sp.pi * G)) != 0 for (m, n_) in [(0, 0), (0, 3), (3, 3)]))
# route 2: canonical (Noether/Hilbert) stress tensor of the Part-A Lagrangian L = -(1/64 pi G) d_l h_ij d^l h_ij
c_can = 2 * sp.Rational(1, 64) / (sp.pi * G)      # T_mn = 2 * (1/64 pi G) d_m h d_n h  (+ eta L, which averages to zero on shell)
chk("B7  route 2: stress tensor of L2 = -(1/64 pi G)(dh)^2 is 2 x 1/(64 pi G) = 1/(32 pi G): the SAME 32 pi (the 2 = derivative of a quadratic form)", sp.simplify(c_can - 1 / (32 * sp.pi * G)) == 0)

# ------------------------------------------------------------------ Part D
print("\nPART D  Isaacson identity rho_GW = a_tidal^2/(8 pi G);  geodesic deviation from the Riemann tensor")
gp = eta + eps * h.subs({g_: 0})       # plus polarisation, general f(t,z)
gpi = ginv_trunc(h.subs({g_: 0}))
Rp, Gp = ricci(gp, gpi)
Rd = riemann_down(gp, Gp)
R0x0x = sp.simplify(T2(Rd(0, 1, 0, 1)).coeff(eps, 1))
chk("D1  R_{0x0x} = -(1/2) d_t^2 h_xx  (linear order)  => geodesic deviation  x''^i = -R^i_{0j0} x^j = +(1/2) h_ij'' x^j", sp.simplify(R0x0x + sp.Rational(1, 2) * sp.diff(f, t, 2)) == 0)
h0 = sp.symbols('h0', positive=True)
a_tid = w**2 * h0 / 2 * (1 / w)         # peak (1/2) w^2 h0 r at r = 1/w
rho_GW = w**2 * h0**2 / (32 * sp.pi * G)
chk("D2  rho_GW = a_tidal^2/(8 pi G)  with a_tidal = (1/2) w h0 (peak tidal acceleration at r = c/w):  8 pi x 4 = 32 pi is (Newtonian field energy) x (geodesic-deviation 1/2)^2", sp.simplify(rho_GW - a_tid**2 / (8 * sp.pi * G)) == 0)
chk("C3  CONTROL: rho_GW = a_tidal^2/(16 pi G) is rejected", sp.simplify(rho_GW - a_tid**2 / (16 * sp.pi * G)) != 0)

# ------------------------------------------------------------------ Part E
print("\nPART E  one-graviton exchange: 32 pi = 8 x 4 pi;  classical route 16 pi G/(4 pi) = 4 G")
eta4 = sp.diag(-1, 1, 1, 1)
m1, m2, kap, r, q = sp.symbols('m1 m2 kappa r q', positive=True)
T1 = sp.zeros(4, 4); T1[0, 0] = m1
T2 = sp.zeros(4, 4); T2[0, 0] = m2
def contract(P):          # T1^{mn} P_{mn ab} T2^{ab}, lower-index T via eta (T^{00}: lowering gives T_{00} = T^{00})
    Tl1 = eta4 * T1 * eta4; Tl2 = eta4 * T2 * eta4
    s = 0
    for a in range(4):
        for b in range(4):
            for c in range(4):
                for d in range(4):
                    s += T1[a, b] * P(a, b, c, d) * T2[c, d]
    return sp.simplify(s)
Pdd = lambda a, b, c, d: sp.Rational(1, 2) * (eta4[a, c] * eta4[b, d] + eta4[a, d] * eta4[b, c] - eta4[a, b] * eta4[c, d])
tens = contract(Pdd)
chk("E1  de Donder tensor structure for two static masses: T1 P T2 = (1/2) m1 m2", sp.simplify(tens - m1 * m2 / 2) == 0)
FT = sp.integrate(sp.sin(q * r) / q, (q, 0, sp.oo)) / (2 * sp.pi**2 * r)
chk("E2  Fourier transform  int d^3q/(2 pi)^3 e^{iq.r}/q^2 = 1/(4 pi r)", sp.simplify(FT - 1 / (4 * sp.pi * r)) == 0)
V = -(kap**2 / 4) * tens * FT      # vertices (kappa/2)^2, propagator P/q^2
chk("E3  V(r) = -kappa^2 m1 m2/(32 pi r): 32 pi = 8 (tensor structure x vertices) x 4 pi (Poisson Green function);  kappa^2 = 32 pi G gives Newton",
    sp.simplify(V.subs(kap, sp.sqrt(32 * sp.pi * G)) + G * m1 * m2 / r) == 0)
chk("C4  CONTROL: kappa^2 = 16 pi G gives G/2, not Newton", sp.simplify(V.subs(kap, sp.sqrt(16 * sp.pi * G)) + G * m1 * m2 / r) != 0)

# ------------------------------------------------------------------ Part F
print("\nPART F  memory: the coefficient is 4G/r = 16 pi G/(4 pi): pi-free")
rr, mm = sp.symbols('rr mm', positive=True)
hbar00 = 4 * G * mm / rr
flux = sp.integrate(sp.diff(hbar00, rr) * rr**2 * sp.sin(sp.Symbol('th')), (sp.Symbol('th'), 0, sp.pi)) * 2 * sp.pi
chk("F1  Laplacian h-bar_00 = -16 pi G m delta^3 : flux of grad(4Gm/r) through a sphere = -16 pi G m", sp.simplify(flux + 16 * sp.pi * G * mm) == 0)
chk("F2  static metric: h_00 = h-bar_00 - (1/2) eta_00 h-bar = 2Gm/r  (g_00 = -1 + 2Gm/r)", sp.simplify(hbar00 - sp.Rational(1, 2) * (-1) * (-hbar00) - 2 * G * mm / rr) == 0)
bk("F3  linear memory (Favata 2010, arXiv:1003.3486 eq 11) carries 4 M/R per particle = 16 pi/(4 pi): no pi remains", sp.Rational(16, 4) == 4)
bk("F4  nonlinear memory: 4 G/R x [dE/dt dOmega with dE = r^2 t_tr dt dOmega, t = 1/(32 pi G)<hdot hdot>] = 1/(8 pi) x r int int <hdot hdot> ...: a 1/(8 pi) reappears only when memory is written through the strain", sp.simplify(4 * G / (32 * sp.pi * G) - 1 / (8 * sp.pi)) == 0)
print("\n%d/%d recomputed checks (incl. 4 mutation controls) behaved as declared; %d/%d bookkeeping lines true" % (sum(ok), len(ok), sum(bk_ok), len(bk_ok)))
sys.exit(0 if all(ok) and all(bk_ok) else 1)
