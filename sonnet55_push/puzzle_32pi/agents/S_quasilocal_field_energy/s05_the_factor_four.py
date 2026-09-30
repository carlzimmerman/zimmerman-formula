"""s05: item (4) of the lane: the chain  rho_Lambda / u_g(a0) = 32 pi = 8 pi x 4.  Is the '4' a quasi-local/derived number or the puzzle itself?

 A  d = 3 algebra: rho/u_g(a0) = 32 pi <=> xi = 1/4 ; u_g(a)/a = a/(8 pi G) = T_U sigma_BH ; rho = 32 pi a0 T_U sigma_BH ; the factorisations of 32 pi.
 B  Newtonian limit of Einstein gravity in D = d+1 dimensions from the quadratic EH action (d = 3, 4, 5, sympy): psi = phi/(d-2),
    Poisson  lap phi = 8 pi G (d-2)/(d-1) rho  and the field-energy normalisation u_g = g^2 (d-1)/(16 pi G (d-2))  (= g^2/(8 pi G) only at d = 3).
 C  Brown-York in d = 4 (covariant, 5-metric): s = (a + (d-2) sqrt(f)/R)/(8 pi G), horizon limit a/(8 pi G) = T sigma_BH with sigma_BH = 1/(4G) in every d.
    => the identity u_g(a)/a = T_U sigma_BH holds ONLY at d = 3: [u_g(a)/a]/[T_U sigma] = (d-1)/(2(d-2)).
 D  The two d-generalisations of the puzzle: (A) xi_d = 1/4 (the record's Z_d^2 = 64 pi/(d(d-1))): rho/u_g = 64 pi (d-2)/(d-1); (B) rho/u_g = 32 pi for all d: xi_d = (d-2)/(2(d-1)).
    Candidate origins of the '4' (Q1..Q5 of PREDECLARED_PRINCIPLES.md) as functions of d.
 E  (POST-HOC, not part of the declared menu, labelled as such) area budgets G rho A(R) = q: pi-class.
"""
import sympy as sp, itertools

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

G, a0, a, rho = sp.symbols('G a0 a rho', positive=True)
xi = sp.symbols('xi', positive=True)

# ------------------------------------------------------------------ A
ug = lambda g: g**2/(8*sp.pi*G)
TU = a/(2*sp.pi); sigma = 1/(4*G)
chk("A1 rho/u_g(a0) = 32 pi  <=>  G rho/a0^2 = 4  (xi = 1/4)", sp.simplify((rho/ug(a0)).subs(rho, a0**2/(xi*G)) - 8*sp.pi/xi) == 0 and sp.simplify((8*sp.pi/xi).subs(xi, sp.Rational(1, 4)) - 32*sp.pi) == 0)
chk("A2 u_g(a)/a = a/(8 pi G) = T_U sigma_BH (T_U = a/2pi, sigma = 1/4G)  [d = 3]", sp.simplify(ug(a)/a - TU*sigma) == 0 and sp.simplify(TU*sigma - a/(8*sp.pi*G)) == 0)
chk("A3 rho_Lambda = 32 pi a0 T_U(a0) sigma_BH at xi = 1/4", sp.simplify((32*sp.pi*a0*TU.subs(a, a0)*sigma) - 4*a0**2/G) == 0)
facts = [(sp.Integer(k), 32*sp.pi/k) for k in (1, 2, 4, 8, 16, 32)]
print("   factorisations 32 pi = k x (32 pi/k):", [(int(k), str(v)) for k, v in facts])
print("   the split 8 pi x 4 is one of six integer splits; 8 pi = 2 pi (Unruh) x 4 (BH quarter) = 16 pi (EH) x 1/2 (Newtonian trace-reversal, part B)")

# ------------------------------------------------------------------ B  D-dimensional Newtonian limit
def christoffel(g, ginv, X):
    n = len(X)
    return [[[sum(ginv[l, m]*(sp.diff(g[m, i], X[j]) + sp.diff(g[m, j], X[i]) - sp.diff(g[i, j], X[m])) for m in range(n))/2
              for j in range(n)] for i in range(n)] for l in range(n)]
def ricci_scalar(g, ginv, Gam, X):
    n = len(X)
    Ric = sp.zeros(n, n)
    for i in range(n):
        for j in range(i, n):
            Ric[i, j] = sum(sp.diff(Gam[l][i][j], X[l]) for l in range(n)) - sum(sp.diff(Gam[l][i][l], X[j]) for l in range(n)) \
                        + sum(Gam[l][l][m]*Gam[m][i][j] for l in range(n) for m in range(n)) - sum(Gam[l][j][m]*Gam[m][i][l] for l in range(n) for m in range(n))
            Ric[j, i] = Ric[i, j]
    return sum(ginv[i, j]*Ric[i, j] for i in range(n) for j in range(n))

e = sp.symbols('e', real=True)
def newtonian_limit(d):
    xs = sp.symbols('x1:%d' % (d + 1), real=True)
    t = sp.symbols('t', real=True)
    X = [t] + list(xs)
    phi = sp.Function('phi')(*xs); psi = sp.Function('psi')(*xs)
    g = sp.diag(*([-(1 + 2*e*phi)] + [(1 - 2*e*psi)]*d))
    ginv = g.inv()
    Gam = christoffel(g, ginv, X)
    Rs = ricci_scalar(g, ginv, Gam, X)
    sqrtg = sp.sqrt((1 + 2*e*phi)*(1 - 2*e*psi)**d)
    dens = sqrtg*Rs
    L2 = sp.simplify(sp.diff(dens, e, 2).subs(e, 0)/2)
    L2G = L2/(16*sp.pi*G)
    def EL(L, f):
        out = sp.diff(L, f)
        for v in xs:
            out -= sp.diff(sp.diff(L, sp.diff(f, v)), v)
        for i_, v in enumerate(xs):
            for j_, w in enumerate(xs):
                if i_ == j_:
                    out += sp.diff(sp.diff(L, sp.diff(f, v, 2)), v, 2)
                elif i_ < j_:
                    out += sp.diff(sp.diff(L, sp.diff(f, v, w)), v, w)
        return out
    rhoF = sp.Function('rho')(*xs)
    Ltot = L2G - rhoF*phi
    ELphi = sp.simplify(EL(Ltot, phi)); ELpsi = sp.simplify(EL(Ltot, psi))
    lap = lambda f: sum(sp.diff(f, v, 2) for v in xs)
    return xs, phi, psi, rhoF, ELphi, ELpsi, lap, L2G

results = {}
for d in (3, 4, 5):
    xs, phi, psi, rhoF, ELphi, ELpsi, lap, L2G = newtonian_limit(d)
    c_psi = sp.symbols('c_psi');
    # ansatz: EL_psi = A1 lap(psi) + A2 lap(phi) ; EL_phi = B1 lap(psi) - rho   (verify by matching coefficients)
    A1, A2, B1 = sp.symbols('A1 A2 B1')
    e1 = sp.expand(ELpsi - (A1*lap(psi) + A2*lap(phi)))
    e2 = sp.expand(ELphi - (B1*lap(psi) - rhoF))
    # collect coefficient of each second derivative
    sol1 = sp.solve([e1.coeff(sp.diff(psi, xs[0], 2)), e1.coeff(sp.diff(phi, xs[0], 2))], [A1, A2], dict=True)
    sol2 = sp.solve([e2.coeff(sp.diff(psi, xs[0], 2))], [B1], dict=True)
    A1v, A2v, B1v = sol1[0][A1], sol1[0][A2], sol2[0][B1]
    chk("B%d.1 D = %d: EL operators have the form (A1 lap psi + A2 lap phi, B1 lap psi - rho) exactly" % (d, d + 1), sp.simplify(e1.subs({A1: A1v, A2: A2v})) == 0 and sp.simplify(e2.subs(B1, B1v)) == 0)
    # psi = -A2/A1 phi
    ratio = sp.simplify(-A2v/A1v)
    chk("B%d.2 psi = phi/(d-2) from the psi-equation (d = %d: ratio %s)" % (d, d, ratio), sp.simplify(ratio - sp.Rational(1, d - 2)) == 0)
    # Poisson: B1 lap(psi) = rho, psi = phi/(d-2)  =>  lap phi = (d-2) rho / B1
    poisson_coeff = sp.simplify((d - 2)/B1v)
    chk("B%d.3 Poisson: lap phi = 8 pi G (d-2)/(d-1) rho = %s rho" % (d, poisson_coeff), sp.simplify(poisson_coeff - 8*sp.pi*G*sp.Rational(d - 2, d - 1)) == 0)
    # field Lagrangian on the constraint surface: L2G(psi = phi/(d-2)) = -k_d (grad phi)^2 with k_d = 1/(2 Omega G_N) = (d-1)/(16 pi G (d-2))
    gr2 = sum(sp.diff(phi, v)**2 for v in xs)
    Lred = sp.simplify(L2G.subs(psi, phi/(d - 2)).doit())
    # remove total derivatives by comparing Euler-Lagrange operators with those of -k (grad phi)^2 :  EL[-k (grad phi)^2] = 2 k lap(phi)
    def EL_phi_only(Lp):
        out = sp.diff(Lp, phi)
        for v in xs:
            out -= sp.diff(sp.diff(Lp, sp.diff(phi, v)), v)
        for i_, v in enumerate(xs):
            for j_, w in enumerate(xs):
                if i_ == j_:
                    out += sp.diff(sp.diff(Lp, sp.diff(phi, v, 2)), v, 2)
                elif i_ < j_:
                    out += sp.diff(sp.diff(Lp, sp.diff(phi, v, w)), v, w)
        return out
    ELred = sp.simplify(EL_phi_only(Lred))
    k_d = sp.Rational(d - 1, d - 2)/(16*sp.pi*G)
    chk("B%d.4 reduced field action = -k_d (grad phi)^2 with k_d = (d-1)/(16 pi G (d-2)) = 1/(2 Omega_{d-1} G_N) (EL operators agree)" % d, sp.simplify(ELred - 2*k_d*lap(phi)) == 0)
    results[d] = k_d
chk("B6 field-energy normalisation: 1/(2 Omega_{d-1} G_N) = (d-1)/(16 pi G (d-2)); equals 1/(8 pi G) ONLY at d = 3 (values %s)" % {d: str(results[d]) for d in results},
    sp.simplify(results[3] - 1/(8*sp.pi*G)) == 0 and sp.simplify(results[4] - 1/(8*sp.pi*G)) != 0 and sp.simplify(results[5] - 1/(8*sp.pi*G)) != 0)

# ------------------------------------------------------------------ C  Brown-York in d = 4 (D = 5), covariant
t, r = sp.symbols('t r', positive=True)
th1, th2, th3 = sp.symbols('th1 th2 th3', positive=True)
Nf = sp.Function('N')(r); ff = sp.Function('f')(r)
X5 = [t, r, th1, th2, th3]
g5 = sp.diag(-Nf**2, 1/ff, r**2, r**2*sp.sin(th1)**2, r**2*sp.sin(th1)**2*sp.sin(th2)**2)
g5i = g5.inv()
Gam5 = christoffel(g5, g5i, X5)
n_dn = [0, 1/sp.sqrt(ff), 0, 0, 0]
def nabla_n(a_, b_):
    return sp.diff(n_dn[b_], X5[a_]) - sum(Gam5[l][a_][b_]*n_dn[l] for l in range(5))
tang = [0, 2, 3, 4]
K5 = sp.Matrix(4, 4, lambda i, j: sp.simplify(nabla_n(tang[i], tang[j])))
gam5 = sp.diag(-Nf**2, r**2, r**2*sp.sin(th1)**2, r**2*sp.sin(th1)**2*sp.sin(th2)**2)
gam5i = gam5.inv()
Ktr5 = sp.simplify(sum(gam5i[i, j]*K5[i, j] for i in range(4) for j in range(4)))
dd = 4
a_acc = sp.sqrt(ff)*sp.diff(Nf, r)/Nf
eps5 = sp.simplify((-(K5[0, 0] - Ktr5*gam5[0, 0])/(8*sp.pi*G))/Nf**2)
s5 = sp.simplify(gam5i[1, 1]*(-(K5[1, 1] - Ktr5*gam5[1, 1]))/(8*sp.pi*G))
chk("C1 d = 4: eps = -(d-1) sqrt(f)/(8 pi G r)  (k = (d-1) sqrt(f)/r for S^{d-1})", sp.simplify(eps5 + (dd - 1)*sp.sqrt(ff)/(8*sp.pi*G*r)) == 0)
chk("C2 d = 4: s = (a + (d-2) sqrt(f)/r)/(8 pi G)", sp.simplify(s5 - (a_acc + (dd - 2)*sp.sqrt(ff)/r)/(8*sp.pi*G)) == 0)
# horizon limit: near a horizon a -> kappa/N diverges, so s -> a/(8 pi G) = T_loc sigma_BH, sigma = 1/(4G) in any D
rh, delta = sp.symbols('r_h delta', positive=True)
fT = 1 - (rh/r)**(dd - 2)                         # Tangherlini
kappa = sp.diff(fT, r).subs(r, rh)/2
Rs_ = rh*(1 + delta)
sq = sp.sqrt(fT.subs(r, Rs_)); a_ = sp.diff(sp.sqrt(fT), r).subs(r, Rs_)
s_T = (a_ + (dd - 2)*sq/Rs_)/(8*sp.pi*G)
T_loc = kappa/(2*sp.pi*sq)
chk("C3 Tangherlini d = 4: s / (T_loc / 4G) -> 1 at the horizon (membrane pressure = T x entropy density, sigma_BH = 1/4G in every D)", sp.limit(sp.simplify(s_T/(T_loc/(4*G))), delta, 0) == 1)
ratio_d = lambda dv: sp.Rational(dv - 1, 2*(dv - 2))
chk("C4 [u_g(a)/a]/[T_U sigma_BH] = (d-1)/(2(d-2)): equals 1 only at d = 3 (3/4 at d = 4, 2/3 at d = 5)",
    ratio_d(3) == 1 and ratio_d(4) == sp.Rational(3, 4) and ratio_d(5) == sp.Rational(2, 3) and all(sp.simplify((sp.Rational(dv - 1, dv - 2)/(16*sp.pi*G)*a**2/a)/(a/(2*sp.pi)/(4*G)) - ratio_d(dv)) == 0 for dv in (3, 4, 5)))
# vacuum solution check (D = 5): Tangherlini f = 1 - (r_h/r)^2 with N = sqrt(f) is Ricci flat
fT5 = 1 - (rh/r)**2
gT = sp.diag(-fT5, 1/fT5, r**2, r**2*sp.sin(th1)**2, r**2*sp.sin(th1)**2*sp.sin(th2)**2)
gTi = gT.inv(); GamT = christoffel(gT, gTi, X5)
RicT = sp.zeros(5, 5)
for i in range(5):
    for j in range(5):
        RicT[i, j] = sp.simplify(sum(sp.diff(GamT[l][i][j], X5[l]) for l in range(5)) - sum(sp.diff(GamT[l][i][l], X5[j]) for l in range(5))
                                 + sum(GamT[l][l][m]*GamT[m][i][j] for l in range(5) for m in range(5)) - sum(GamT[l][j][m]*GamT[m][i][l] for l in range(5) for m in range(5)))
chk("C5a D = 5 Tangherlini f = 1 - (r_h/r)^2 is a vacuum solution (Ricci flat, from the metric)", RicT == sp.zeros(5, 5))
# E_BY(horizon) = 2 M_ADM in d = 3..6: E_ref(R) = (d-1) Omega R^{d-2} (1 - sqrt f)/(8 pi G) (from C1's eps), M from f = 1 - 16 pi G M/((d-1) Omega r^{d-2})
Om = sp.symbols('Omega', positive=True)
allok = True
for dv in (3, 4, 5, 6):
    Mh = sp.symbols('M_h', positive=True)
    rh_sol = sp.solve(sp.Eq(1 - 16*sp.pi*G*Mh/((dv - 1)*Om*rh**(dv - 2)), 0), rh**(dv - 2))
    E_hor = (dv - 1)*Om*rh**(dv - 2)*(1 - 0)/(8*sp.pi*G)
    allok = allok and sp.simplify(E_hor.subs(rh**(dv - 2), rh_sol[0]) - 2*Mh) == 0
chk("C5 E_BY(horizon) = 2 M_ADM in every dimension d = 3..6 (Tangherlini normalisation): the 'BY/mass = 2' factor is d-independent", allok)

# ------------------------------------------------------------------ D  the two d-generalisations; candidate origins of the '4'
dsym = sp.symbols('d', positive=True)
ug_d = lambda dv: sp.Rational(dv - 1, dv - 2)/(16*sp.pi*G)             # coefficient of g^2
def ratioA(dv):   # xi_d = 1/4 for all d (record's Z_d^2 = 64 pi/(d(d-1)) with H^2 = 16 pi G rho/(d(d-1)))
    return sp.simplify((4*a0**2/G)/(ug_d(dv)*a0**2))
def ratioB_xi(dv):  # rho/u_g = 32 pi for all d  => xi_d
    rho_ = 32*sp.pi*ug_d(dv)*a0**2
    return sp.simplify(a0**2/(G*rho_))
print("\n   d : rho/u_g(a0) under (A) xi = 1/4   |   xi_d under (B) rho/u_g = 32 pi   |   H^2 = 16 pi G rho/(d(d-1)) => Z_d^2 (A) = 64 pi/(d(d-1))")
for dv in (3, 4, 5, 6):
    Zd2 = sp.simplify((16*sp.pi/(dv*(dv - 1)))/sp.Rational(1, 4))
    print("   %d : %-14s | %-10s | %s" % (dv, ratioA(dv), ratioB_xi(dv), Zd2))
chk("D1 (A): rho/u_g(a0) = 64 pi (d-2)/(d-1), equals 32 pi at d = 3 only; the '8 pi x 4' split has 8 pi = 16 pi (d-2)/(d-1) x ... : the chain is 16 pi x [(d-2)/(d-1)] x [1/xi]",
    all(sp.simplify(ratioA(dv) - 64*sp.pi*sp.Rational(dv - 2, dv - 1)) == 0 for dv in (3, 4, 5, 6)) and sp.simplify(ratioA(3) - 32*sp.pi) == 0)
chk("D2 (B): keeping rho/u_g = 32 pi in every d gives xi_d = (d-2)/(2(d-1)) (1/4 at d = 3, 1/3 at d = 4)",
    all(sp.simplify(ratioB_xi(dv) - sp.Rational(dv - 2, 2*(dv - 1))) == 0 for dv in (3, 4, 5, 6)))
chk("D3 the record's Z_d^2 = 64 pi/(d(d-1)) is (A): it needs xi_d = 1/4 in all d, which makes the Poisson normalisation (d-2)/(d-1), not the '4', carry the d-dependence",
    all(sp.simplify((16*sp.pi/(dv*(dv - 1)))/sp.Rational(1, 4) - 64*sp.pi/(dv*(dv - 1))) == 0 for dv in (3, 4, 5, 6)))
# Friedmann constraint in d spatial dimensions (computed): G_00 = d(d-1)/2 H^2 for ds^2 = -dt^2 + a(t)^2 dx^2 (flat slicing); so 8 pi G rho = d(d-1)H^2/2
tt = sp.symbols('tt', real=True)
def friedmann_coeff(dv):
    xs_ = sp.symbols('y1:%d' % (dv + 1), real=True)
    Xf = [tt] + list(xs_)
    aa = sp.Function('a')(tt)
    gf = sp.diag(*([-1] + [aa**2]*dv)); gfi = gf.inv(); Gf = christoffel(gf, gfi, Xf)
    n_ = len(Xf)
    Ric = sp.zeros(n_, n_)
    for i in range(n_):
        for j in range(n_):
            Ric[i, j] = sum(sp.diff(Gf[l][i][j], Xf[l]) for l in range(n_)) - sum(sp.diff(Gf[l][i][l], Xf[j]) for l in range(n_)) \
                        + sum(Gf[l][l][m]*Gf[m][i][j] for l in range(n_) for m in range(n_)) - sum(Gf[l][j][m]*Gf[m][i][l] for l in range(n_) for m in range(n_))
    Rsc_ = sum(gfi[i, j]*Ric[i, j] for i in range(n_) for j in range(n_))
    G00 = sp.simplify(Ric[0, 0] - Rsc_*gf[0, 0]/2)
    Hh = sp.diff(aa, tt)/aa
    return sp.simplify(G00/Hh**2)
chk("D0 Friedmann in d spatial dims (from the metric, d = 3, 4, 5): G_00 = d(d-1)/2 H^2, hence H^2 = 16 pi G rho/(d(d-1)) and Z_d^2 = H^2/a0^2 = 64 pi/(d(d-1)) at xi = 1/4",
    all(sp.simplify(friedmann_coeff(dv) - sp.Rational(dv*(dv - 1), 2)) == 0 for dv in (3, 4, 5)))
# candidate origins of the 4, as functions of d
Omega = lambda n: 2*sp.pi**sp.Rational(n + 1, 2)/sp.gamma(sp.Rational(n + 1, 2))      # area of unit S^n
Vball = lambda n: sp.pi**sp.Rational(n, 2)/sp.gamma(sp.Rational(n, 2) + 1)
cand = {
 'Q1 trace count d+1': lambda dv: sp.Integer(dv + 1),
 'Q2 (1/(kappa r_s))^2 = (2/(d-2))^2': lambda dv: sp.Rational(2, dv - 2)**2,
 'Q3 area/disc Omega_{d-1}/V_{d-1}': lambda dv: sp.simplify(Omega(dv - 1)/Vball(dv - 1)),
 'Q4 BH quarter 1/(1/4)': lambda dv: sp.Integer(4),
 'Q5 (E_BY(horizon)/M_ADM)^2': lambda dv: sp.Integer(4),
 'Q6 [1/xi under (B)] = 2(d-1)/(d-2)': lambda dv: sp.Rational(2*(dv - 1), dv - 2),
}
print("\n   candidate '4' vs d:")
vals = {}
for name, fn in cand.items():
    vals[name] = [sp.nsimplify(fn(dv)) for dv in (3, 4, 5, 6)]
    print("   %-40s d=3..6: %s" % (name, [sp.N(v, 5) for v in vals[name]]))
chk("D4 all six candidates equal 4 at d = 3 (six structures agree at one point, four of them d-dependent: uninformative), but differ at d = 4 in at least three distinct values",
    all(v[0] == 4 for v in vals.values()) and len(set(sp.N(v[1], 8) for v in vals.values())) >= 3)
# no candidate is derived: the puzzle's '4' is 1/xi; check the one structural identity (B): 1/xi_d = 2(d-1)/(d-2) is the quasi-local (Newtonian trace-reversal) function
chk("D5 under reading (B) the '4' IS the trace-reversal ratio 2(d-1)/(d-2) (a derived function of d equal to 4 at d = 3); under reading (A) it is the constant 1/xi = 4 and carries no derived content",
    all(sp.simplify(1/ratioB_xi(dv) - 2*sp.Rational(dv - 1, dv - 2)) == 0 for dv in (3, 4, 5, 6)) and sp.simplify(1/ratioB_xi(3) - 4) == 0)

# ------------------------------------------------------------------ E  post-hoc area budgets (NOT part of the declared menu; recorded for the pi-class statement)
q = sp.symbols('q', positive=True)
A_R = lambda R_: 4*sp.pi*R_**2
Lsq = sp.symbols('L', positive=True)
rho_L = 3/(8*sp.pi*G*Lsq**2)
chk("E1 (post hoc) G rho A_dS = 3/2 EXACTLY (pi-free): the Friedmann pi cancels the area's pi", sp.simplify(G*rho_L*A_R(Lsq) - sp.Rational(3, 2)) == 0)
chk("E2 (post hoc) for the a0-horizon (r = 1/(2 a0)): G rho A = pi/xi; a rational area budget G rho A = q gives xi = pi/q (pi-class Q x pi); xi = 1/4 needs q = 4 pi, the Gauss-Bonnet constant (restatement V3)",
    sp.simplify((G*(a0**2/(xi*G))*A_R(1/(2*a0))) - sp.pi/xi) == 0 and sp.simplify(sp.pi/(4*sp.pi) - sp.Rational(1, 4)) == 0)

print("\nTOTAL", sum(ok), "/", len(ok), "pass;", len(ok) - sum(ok), "fail")
