"""s02: (a) the Newtonian field action and the 1/(8 pi G) from the quadratic Einstein-Hilbert action; (b) the sign and LOCALISATION
of 'field energy density'; (c) Landau-Lifshitz and Einstein pseudotensors of the Schwarzschild field versus the quasi-local (Brown-York) budget.
c = 1, G explicit.

 A  metric ds^2 = -(1+2 e phi) dt^2 + (1 - 2 e psi) dx^2 (phi, psi functions of x,y,z).  (1/16 pi G) sqrt(-g) R expanded to O(e^2) EQUALS
    (1/8 pi G)[(grad psi)^2 - 2 grad phi . grad psi] up to a total divergence (Euler-Lagrange operators agree identically).  Adding the dust coupling
    -rho phi and varying gives psi = phi and  lap phi = 4 pi G rho  (Poisson).  Mutations (coefficient 1/(4 pi G), or the cross term dropped) fail.
 B  Static energy E = -L on the constraint surface: gradient part +g^2/(8 pi G), interaction rho phi, total on shell = (1/2) int rho phi = -(1/8 pi G) int g^2.
    Uniform ball: three different local densities have the SAME integral up to sign; only the total (and the BY exterior budget) is meaningful.
 C  Pseudotensors of the exact Schwarzschild field (isotropic and harmonic coordinates): Landau-Lifshitz t^00 = -7 g^2/(8 pi G); Einstein canonical (Gamma-Gamma)
    density; both compared with the covariant BY exterior budget (-1).
"""
import sympy as sp

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

G = sp.symbols('G', positive=True)
x, y, z, t, e = sp.symbols('x y z t e', real=True)
X = [t, x, y, z]
phi = sp.Function('phi')(x, y, z); psi = sp.Function('psi')(x, y, z)

def christoffel(g, ginv, X):
    n = len(X)
    return [[[sum(ginv[l, m]*(sp.diff(g[m, i], X[j]) + sp.diff(g[m, j], X[i]) - sp.diff(g[i, j], X[m])) for m in range(n))/2
              for j in range(n)] for i in range(n)] for l in range(n)]
def ricci_scalar(g, ginv, Gam, X):
    n = len(X)
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(n):
            Ric[i, j] = sum(sp.diff(Gam[l][i][j], X[l]) for l in range(n)) - sum(sp.diff(Gam[l][i][l], X[j]) for l in range(n)) \
                        + sum(Gam[l][l][m]*Gam[m][i][j] for l in range(n) for m in range(n)) - sum(Gam[l][j][m]*Gam[m][i][l] for l in range(n) for m in range(n))
    return sum(ginv[i, j]*Ric[i, j] for i in range(n) for j in range(n))

# ---------------------------------------------------------------- A
g = sp.diag(-(1 + 2*e*phi), (1 - 2*e*psi), (1 - 2*e*psi), (1 - 2*e*psi))
ginv = g.inv()
Gam = christoffel(g, ginv, X)
Rs = ricci_scalar(g, ginv, Gam, X)
sqrtg = sp.sqrt((1 + 2*e*phi)*(1 - 2*e*psi)**3)
dens = sqrtg*Rs
L1 = sp.simplify(sp.diff(dens, e).subs(e, 0))
L2 = sp.simplify(sp.diff(dens, e, 2).subs(e, 0)/2)
lap = lambda f: sp.diff(f, x, 2) + sp.diff(f, y, 2) + sp.diff(f, z, 2)
grad2 = lambda f, h: sp.diff(f, x)*sp.diff(h, x) + sp.diff(f, y)*sp.diff(h, y) + sp.diff(f, z)*sp.diff(h, z)
chk("A0 O(e^0) term of sqrt(-g) R vanishes (flat space)", sp.simplify(dens.subs(e, 0)) == 0)
def euler_lagrange(L, f):
    """EL operator for L(f, f_i, f_ij) in x,y,z"""
    out = sp.diff(L, f)
    for v in (x, y, z):
        out -= sp.diff(sp.diff(L, sp.diff(f, v)), v)
    for v in (x, y, z):
        for w in (x, y, z):
            if v == w:
                out += sp.diff(sp.diff(L, sp.diff(f, v, 2)), v, 2)
            elif (str(v) < str(w)):
                out += sp.diff(sp.diff(L, sp.diff(f, v, w)), v, w)
    return out
print("   O(e) term  L1 =", L1)
chk("A1 O(e^1) term is a pure total divergence: Euler-Lagrange operators of L1 vanish identically", sp.simplify(euler_lagrange(L1, phi)) == 0 and sp.simplify(euler_lagrange(L1, psi)) == 0)
target = (1/(8*sp.pi*G))*(grad2(psi, psi) - 2*grad2(phi, psi))      # candidate reduced Lagrangian
L2G = L2/(16*sp.pi*G)
ELphi_a = sp.simplify(euler_lagrange(L2G, phi)); ELphi_b = sp.simplify(euler_lagrange(target, phi))
ELpsi_a = sp.simplify(euler_lagrange(L2G, psi)); ELpsi_b = sp.simplify(euler_lagrange(target, psi))
chk("A2 (1/16 pi G)(sqrt(-g)R)_2 and (1/8 pi G)[(grad psi)^2 - 2 grad phi.grad psi] have identical Euler-Lagrange operators in phi", sp.simplify(ELphi_a - ELphi_b) == 0)
chk("A3 ... and in psi (hence they differ by a total divergence)", sp.simplify(ELpsi_a - ELpsi_b) == 0)
rho = sp.Function('rho')(x, y, z)
Ltot = target - rho*phi                                   # dust at rest: S_m = -int rho sqrt(-g_00) -> -rho phi
EL_phi = sp.simplify(euler_lagrange(Ltot, phi)); EL_psi = sp.simplify(euler_lagrange(Ltot, psi))
chk("A4 delta psi:  -(1/4 pi G) lap(psi - phi) = 0  (no anisotropic stress => psi = phi)", sp.simplify(EL_psi + (1/(4*sp.pi*G))*lap(psi - phi)) == 0)
chk("A5 delta phi:  (1/4 pi G) lap(psi) - rho = 0  => lap phi = 4 pi G rho (Poisson)", sp.simplify(EL_phi - ((1/(4*sp.pi*G))*lap(psi) - rho)) == 0)
# point mass check of the coefficient: phi = -G M/r solves lap phi = 4 pi G rho with M = int rho  (Gauss)
rr = sp.sqrt(x**2 + y**2 + z**2); Mm = sp.symbols('M', positive=True); rs_sym = sp.symbols('r_s', positive=True)
chk("A6 phi = -G M/r is harmonic away from the origin and its flux 4 pi r^2 (d phi/dr) = 4 pi G M (the Poisson constant)",
    sp.simplify(lap(-G*Mm/rr)) == 0 and sp.simplify(4*sp.pi*rs_sym**2*sp.diff(-G*Mm/rs_sym, rs_sym) - 4*sp.pi*G*Mm) == 0)
# mutations
target_bad = (1/(4*sp.pi*G))*(grad2(psi, psi) - 2*grad2(phi, psi))
chk("A7 mutation: coefficient 1/(4 pi G) instead of 1/(8 pi G) gives lap phi = 8 pi G rho (Newton's constant off by 2)",
    sp.simplify(sp.simplify(euler_lagrange(target_bad - rho*phi, phi)) - ((1/(2*sp.pi*G))*lap(psi) - rho)) == 0)
target_nocross = (1/(8*sp.pi*G))*(grad2(psi, psi))
chk("A8 mutation: dropping the cross term leaves phi unconstrained by the field (no gravitational potential dynamics)",
    sp.simplify(euler_lagrange(target_nocross - rho*phi, phi) + rho) == 0)

# ---------------------------------------------------------------- B  energy localisations, uniform ball
R0, Mb, rs = sp.symbols('R_0 M_b r', positive=True)
g_in = G*Mb*rs/R0**3; g_out = G*Mb/rs**2
phi_in = G*Mb*(rs**2 - 3*R0**2)/(2*R0**3); phi_out = -G*Mb/rs
rho_b = 3*Mb/(4*sp.pi*R0**3)
grad_energy = sp.integrate(4*sp.pi*rs**2*g_in**2/(8*sp.pi*G), (rs, 0, R0)) + sp.integrate(4*sp.pi*rs**2*g_out**2/(8*sp.pi*G), (rs, R0, sp.oo))
half_rho_phi = sp.integrate(4*sp.pi*rs**2*rho_b*phi_in/2, (rs, 0, R0))
chk("B1 uniform ball: gradient-only energy +int g^2/(8 pi G) = +3 G M^2/(5 R0)", sp.simplify(grad_energy - 3*G*Mb**2/(5*R0)) == 0)
chk("B2 uniform ball: (1/2) int rho phi = -3 G M^2/(5 R0)", sp.simplify(half_rho_phi + 3*G*Mb**2/(5*R0)) == 0)
Etot = grad_energy + sp.integrate(4*sp.pi*rs**2*rho_b*phi_in, (rs, 0, R0))
chk("B3 total on shell E = (1/8 pi G) int g^2 + int rho phi = -3 G M^2/(5 R0) (interaction term is -2x the gradient term)", sp.simplify(Etot + 3*G*Mb**2/(5*R0)) == 0)
chk("B4 the gradient-only localisation and the (1/2) rho phi localisation integrate to equal and opposite values: the sign of 'field energy' depends on the localisation, only the total is meaningful", sp.simplify(grad_energy + half_rho_phi) == 0 and grad_energy != 0)

# ---------------------------------------------------------------- C  pseudotensors
mL = sp.symbols('m', positive=True)     # m = G M / 2 in isotropic coordinates (G = 1 units inside the pseudotensor algebra; G restored below)
xs = sp.symbols('x1 x2 x3', real=True); r3 = sp.sqrt(sum(v**2 for v in xs))
def d2_contract(Fmat):
    return sum(sp.diff(Fmat[i, j], xs[i], xs[j]) for i in range(3) for j in range(3))
Mg = sp.symbols('Mg', positive=True)   # geometric mass G M (with G = 1 in this block; energy densities are then expressed in units of 1/(8 pi))
# isotropic Schwarzschild: g00 = -A^2, gij = B^4 delta;  (-g) g^00 g^ij = -B^8 delta_ij
B = 1 + Mg/(2*r3)
F_iso = -B**8*sp.eye(3)
X_iso = sp.simplify(d2_contract(F_iso)/(16*sp.pi))
X_iso_series = sp.series(sp.simplify(X_iso.subs({xs[1]: 0, xs[2]: 0, xs[0]: sp.Symbol('rr', positive=True)})), Mg, 0, 3).removeO()
rr_ = sp.Symbol('rr', positive=True)
g2 = Mg**2/rr_**4                                       # g^2 with G = 1
chk("C1 Landau-Lifshitz, isotropic Schwarzschild: (-g)(T^00 + t^00) = (1/16 pi G) d_i d_j[(-g) g^00 g^ij]; vacuum O(M^2) coefficient = -7 g^2/(8 pi G)  (g^2 = M^2/r^4, G = 1)",
    sp.simplify(X_iso_series.coeff(Mg, 2)*rr_**4 + 7/(8*sp.pi)) == 0)
# harmonic Schwarzschild:  g00 = -(r - M)/(r + M);  gij = c delta + d n n, c = (1 + M/r)^2, d = (r+M)/(r-M) M^2/r^2
cH = (1 + Mg/r3)**2; dH = ((r3 + Mg)/(r3 - Mg))*Mg**2/r3**2
nvec = [v/r3 for v in xs]
F_har = sp.Matrix(3, 3, lambda i, j: -cH*(cH + dH)*(1 if i == j else 0) + cH*dH*nvec[i]*nvec[j])
X_har = d2_contract(F_har)/(16*sp.pi)
X_har_val = sp.series(sp.simplify(X_har.subs({xs[1]: 0, xs[2]: 0, xs[0]: rr_})), Mg, 0, 3).removeO()
chk("C2 Landau-Lifshitz, harmonic Schwarzschild: also -7 g^2/(8 pi G) at O(M^2) (same value in two asymptotically-Cartesian coordinates)",
    sp.simplify(X_har_val.coeff(Mg, 2)*rr_**4 + 7/(8*sp.pi)) == 0)
# control: exact d_i d_j structure: linear order reproduces the source, X1 = lap(phi)/(4 pi) in vacuum vanishes away from the origin
chk("C3 control: the O(M) term is harmonic (vanishes for r > 0), the flat-space value is 0", sp.simplify(X_iso_series.coeff(Mg, 1)) == 0 and sp.simplify(X_iso_series.coeff(Mg, 0)) == 0)

# LL energy inside radius r = flux of V^i = d_j F^ij/(16 pi):  sign check (ADM mass +M) and the partition M_LL(r) = M + 7 M^2/(2 r)
Bq = 1 + Mg/(2*rr_)
flux_iso = sp.simplify(-(1/(16*sp.pi))*4*sp.pi*rr_**2*sp.diff(Bq**8, rr_))
chk("C5 LL flux through a sphere of radius r in isotropic coordinates = M (1 + M/2r)^7 -> M at infinity (positive ADM mass: sign convention of the pseudotensor is right)",
    sp.simplify(flux_iso - Mg*Bq**7) == 0 and sp.limit(flux_iso, rr_, sp.oo) == Mg)
ser_flux = sp.series(flux_iso, Mg, 0, 3).removeO()
chk("C6 LL partition: 'energy inside r' = M + 7 G M^2/(2 r) + ..., i.e. exterior field energy -7 G M^2/(2r), versus the BY value -G M^2/(2r) (s01 D3): same total M, different local partition",
    sp.simplify(ser_flux - (Mg + 7*Mg**2/(2*rr_))) == 0)
# Einstein canonical (Gamma-Gamma) Lagrangian density for the same weak field, second order
gE = sp.diag(-(1 + 2*e*phi), (1 - 2*e*phi), (1 - 2*e*phi), (1 - 2*e*phi))
gEi = gE.inv(); GamE = christoffel(gE, gEi, X)
sqg = sp.sqrt((1 + 2*e*phi)*(1 - 2*e*phi)**3)
GG = sqg*sum(gEi[m, n]*(sum(GamE[a][m][b]*GamE[b][n][a] for a in range(4) for b in range(4)) - sum(GamE[a][m][n]*GamE[b][a][b] for a in range(4) for b in range(4))) for m in range(4) for n in range(4))
GG2 = sp.simplify(sp.diff(GG, e, 2).subs(e, 0)/2)
kE = sp.simplify(GG2/((sp.diff(phi, x)**2 + sp.diff(phi, y)**2 + sp.diff(phi, z)**2)))
chk("C4 the Einstein Gamma-Gamma second-order density is a pure number times (grad phi)^2 (a definite local coefficient, not a total derivative)", kE.is_number and kE != 0)
print("   Einstein Gamma-Gamma second-order density / (grad phi)^2 =", kE, " -> t^0_0 coefficient in units of g^2/(8 pi G):", sp.simplify(kE/2))
print("   Einstein Gamma-Gamma Lagrangian density = the Newtonian static Lagrangian density (coefficient -1); its energy sign depends on the T^0_0 convention -- not used.")
print("   Localisation table (coefficient of g^2/(8 pi G)): gradient-only +1 ; Newtonian on-shell -1 ; BY exterior -1 (flat reference) ; Landau-Lifshitz -7 (isotropic and harmonic)")

print("\nTOTAL", sum(ok), "/", len(ok), "pass;", len(ok) - sum(ok), "fail")
