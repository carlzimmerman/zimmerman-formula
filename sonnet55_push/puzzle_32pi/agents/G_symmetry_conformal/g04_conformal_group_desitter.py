"""g04: the symmetry group of deep MOND vs the de Sitter isometry group, and what the group can and cannot know.

 A  Conf(R^3): the 10 conformal Killing fields of flat R^3 close into an algebra whose Killing form has signature (6 neg, 4 pos):
    so(4,1) (controls: so(5) -> (10,0), so(3,2) -> (4,6) so the signature routine discriminates).  So the conformal group of 3-space is the
    de Sitter isometry group SO(4,1) (as abstract groups).
 B  the deep-MOND (3-Laplacian) operator div(|grad phi| grad phi) is covariant under inversion x -> x/|x|^2 with phi of weight 0:
    E[phi o f] = |x|^-6 E[phi] o f ; the Newtonian Laplacian is covariant only with the Kelvin weight 1/2 (psi = phi o f / |x|).  Mutations fail.
 C  induced representation of weight Delta on functions on R^3: operators P, M, D = x.d + Delta, K = 2x(x.d + Delta) - x^2 d close into
    the algebra of A; its quadratic Casimir (Killing-form normalised) is proportional to Delta(Delta-3):  deep MOND (Delta_phi = 0) has
    Casimir 0 (= massless minimally-coupled scalar in dS4), Newton/Yamabe (Delta = 1/2) has 5/4 x (unit).
 D  the dS4 Killing fields in flat slicing (metric (-d eta^2 + dx^2)/(H^2 eta^2)) are H-INDEPENDENT vector fields: the isometry group, its
    algebra and every Casimir know nothing about the radius L = 1/H.  The Casimir of the bulk Killing fields equals a constant times
    L^2 Box_dS (generic f), so  Box f = m^2 f  <=>  Casimir = const * m^2 / H^2, and on eta^Delta f(x): m^2/H^2 = Delta (3 - Delta).
"""
import sympy as sp, numpy as np, sys, itertools, random
ok = []
def chk(n, c):
    ok.append(bool(c)); print(("PASS " if c else "FAIL ") + n)

x, y, z = sp.symbols('x y z', real=True); X = (x, y, z)
r2 = x**2 + y**2 + z**2
names, fields = [], []
for i in range(3): names.append('P%d' % (i + 1)); fields.append([1 if j == i else 0 for j in range(3)])
for i in range(3): names.append('K%d' % (i + 1)); fields.append([2 * X[i] * X[j] - (r2 if j == i else 0) for j in range(3)])
names.append('D'); fields.append(list(X))
for (i, j) in [(0, 1), (0, 2), (1, 2)]:
    names.append('M%d%d' % (i + 1, j + 1)); fields.append([(X[i] if k == j else 0) - (X[j] if k == i else 0) for k in range(3)])
n = len(fields)
def bracket(A, B): return [sp.expand(sum(A[j] * sp.diff(B[k], X[j]) - B[j] * sp.diff(A[k], X[j]) for j in range(3))) for k in range(3)]
cs = sp.symbols('c0:%d' % n)
f = {}
allok = True
for a in range(n):
    for b in range(n):
        br = bracket(fields[a], fields[b])
        eqs = []
        for k in range(3):
            expr = sp.expand(br[k] - sum(cs[m] * fields[m][k] for m in range(n)))
            eqs += sp.Poly(expr, *X).coeffs() if expr != 0 else []
        sol = sp.solve(eqs, cs, dict=True) if eqs else [{}]
        if not sol: allok = False; continue
        f[(a, b)] = [sol[0].get(cs[m], 0) for m in range(n)]
chk("A0 the 10 conformal Killing fields of R^3 close under the Lie bracket (all 100 brackets decompose in the basis)", allok and len(f) == n * n)
# ad matrices and Killing form  B_ab = tr(ad_a ad_b);  (ad_a)^c_b = f_ab^c
ad = [np.array([[float(f[(a, b)][c]) for b in range(n)] for c in range(n)]) for a in range(n)]
Bk = np.array([[np.trace(ad[a] @ ad[b]) for b in range(n)] for a in range(n)])
def signature(Bm):
    ev = np.linalg.eigvalsh((Bm + Bm.T) / 2)
    return int((ev < -1e-9).sum()), int((ev > 1e-9).sum())
sig = signature(Bk)
print("   Killing-form signature (neg,pos) of Conf(R^3):", sig)
# controls: so(p,q) matrix algebras
def so_pq(p, q):
    eta = np.diag([-1.0] * p + [1.0] * q); N = p + q
    # generators L_ij = e_ij eta_jj - e_ji eta_ii  acting as matrices with lowered indices: use M_ij = eta-compatible
    basis = []
    for i in range(N):
        for j in range(i + 1, N):
            M = np.zeros((N, N)); M[i, j] = eta[j, j]; M[j, i] = -eta[i, i]
            basis.append(M)
    m = len(basis)
    # structure constants by projection (basis is closed): solve  [a,b] = sum c_m basis_m
    Bmat = np.array([b.flatten() for b in basis]).T
    adm = []
    for a in range(m):
        cols = []
        for b in range(m):
            comm = basis[a] @ basis[b] - basis[b] @ basis[a]
            coef, res, *_ = np.linalg.lstsq(Bmat, comm.flatten(), rcond=None)
            cols.append(coef)
        adm.append(np.array(cols).T)
    return np.array([[np.trace(adm[a] @ adm[b]) for b in range(m)] for a in range(m)])
s41 = signature(so_pq(1, 4)); s32 = signature(so_pq(2, 3)); s50 = signature(so_pq(0, 5))
print("   controls: so(4,1) ->", s41, " so(3,2) ->", s32, " so(5) ->", s50)
chk("A1 control signatures: so(5) = (10,0), so(3,2) = (4,6), so(4,1) = (6,4): the routine discriminates", s50 == (10, 0) and s32 == (4, 6) and s41 == (6, 4))
chk("A2 Conf(R^3) has Killing signature (6,4) = so(4,1), not so(3,2) or so(5): the conformal group of 3-space IS the dS4 isometry group (abstractly)", sig == (6, 4) and n == 10)

# ---------------- B: covariance under inversion
def E3(phi):
    g = [sp.diff(phi, v) for v in X]; nn = sp.sqrt(sum(gi**2 for gi in g))
    return sum(sp.diff(nn * gi, v) for gi, v in zip(g, X))
def Ep(phi, p):        # |grad phi|^(p-2) grad phi divergence
    g = [sp.diff(phi, v) for v in X]; nn = sp.sqrt(sum(gi**2 for gi in g))
    return sum(sp.diff(nn**(p - 2) * gi, v) for gi, v in zip(g, X))
def lap(phi): return sum(sp.diff(phi, v, 2) for v in X)
random.seed(11)
tests = [x**2 * y + z**3 + sp.sin(x * z) + 2 * y, sp.exp(x / 3) * (y + 1) + z**2 * x, x * y * z + y**3 - 4 * x + sp.cos(y)]
inv = {x: x / r2, y: y / r2, z: z / r2}
w_deep = 0; w_kel = 0; w_lap0 = []
for phi in tests:
    phi_i = phi.subs(inv, simultaneous=True)
    for _ in range(3):
        pt = {x: random.uniform(0.5, 1.6), y: random.uniform(0.5, 1.6), z: random.uniform(0.5, 1.6)}
        R2 = sum(v**2 for v in pt.values()); ptI = {x: pt[x] / R2, y: pt[y] / R2, z: pt[z] / R2}
        lhs = float(E3(phi_i).subs(pt)); rhs = float(R2**-3 * E3(phi).subs(ptI))
        w_deep = max(w_deep, abs(lhs - rhs) / (abs(rhs) + 1e-12))
        psi = phi_i / sp.sqrt(r2)                                     # Kelvin transform (weight 1/2 in d=3)
        lhsK = float(lap(psi).subs(pt)); rhsK = float(R2**sp.Rational(-5, 2) * lap(phi).subs(ptI))
        w_kel = max(w_kel, abs(lhsK - rhsK) / (abs(rhsK) + 1e-12))
        lhs0 = float(lap(phi_i).subs(pt)); rhs0 = float(R2**-2 * lap(phi).subs(ptI))           # weight-0 Laplacian: NOT covariant
        w_lap0.append(abs(lhs0 - rhs0) / (abs(rhs0) + 1e-12))
chk("B1 deep-MOND operator: E[phi o inv](x) = |x|^-6 E[phi](inv x), max rel. dev %.1e (9 cases): full inversion covariance with weight 0" % w_deep, w_deep < 1e-9)
chk("B2 Newtonian Laplacian: covariant with the Kelvin weight 1/2 (max dev %.1e), but NOT with weight 0 (median dev %.2f)" % (w_kel, float(np.median(w_lap0))), w_kel < 1e-9 and np.median(w_lap0) > 0.1)
phi = tests[0]; phi_i = phi.subs(inv, simultaneous=True)
pts4 = [{x: 0.9, y: 1.1, z: 0.7}, {x: 1.3, y: 0.6, z: 1.2}, {x: 0.7, y: 0.8, z: 1.5}, {x: 1.5, y: 1.4, z: 0.5}, {x: 0.6, y: 1.7, z: 1.0}]
lhs4 = []; e4 = []; rr2 = []
for ptt in pts4:
    R2 = sum(v**2 for v in ptt.values()); ptI = {x: ptt[x] / R2, y: ptt[y] / R2, z: ptt[z] / R2}
    lhs4.append(float(Ep(phi_i, 4).subs(ptt))); e4.append(float(Ep(phi, 4).subs(ptI))); rr2.append(R2)
dev4b = min(max(abs(l - R2**-k * e) / abs(l) for l, e, R2 in zip(lhs4, e4, rr2)) for k in [x_ / 4 for x_ in range(1, 40)])
chk("B3 mutation: the p=4 operator div(|grad phi|^2 grad phi) is NOT covariant under inversion for any power |x|^-k, k in (0.25..10) (best over k of the WORST dev over 5 points = %.2f)" % dev4b, dev4b > 0.2)

# ---------------- C: weight-Delta representation and its Casimir
Dl = sp.symbols('Delta')
F = sp.Function('f')(*X)
def op(name, u):
    d = lambda v: sp.diff(u, v)
    if name[0] == 'P': return d(X[int(name[1]) - 1])
    if name == 'D': return sum(X[j] * d(X[j]) for j in range(3)) + Dl * u
    if name[0] == 'K':
        i = int(name[1]) - 1
        return 2 * X[i] * (sum(X[j] * d(X[j]) for j in range(3)) + Dl * u) - r2 * d(X[i])
    if name[0] == 'M':
        i, j = int(name[1]) - 1, int(name[2]) - 1
        return X[i] * d(X[j]) - X[j] * d(X[i])
rep_ok = True
for a in range(n):
    for b in range(a + 1, n):
        lhs = sp.expand(op(names[a], op(names[b], F)) - op(names[b], op(names[a], F)))
        rhs = sp.expand(sum(f[(a, b)][m] * op(names[m], F) for m in range(n)))
        # sign: vector-field bracket [A,B] corresponds to operator commutator [A,B]
        if sp.simplify((lhs - rhs).doit()) != 0:
            rep_ok = False
chk("C1 the weight-Delta operators satisfy the SAME commutation relations as the vector fields (a genuine representation for every Delta)", rep_ok)
Binv = np.linalg.inv(Bk)
Bsym = sp.Matrix(n, n, lambda a, b: sp.nsimplify(round(Bk[a, b], 6)))
Binv_s = Bsym.inv()
Cas = 0
for a in range(n):
    for b in range(n):
        if Binv_s[a, b] != 0:
            Cas += Binv_s[a, b] * op(names[a], op(names[b], F))
Cas = sp.simplify(sp.expand(Cas.doit()))
lam = sp.simplify(Cas / F)
print("   Casimir(Delta) acting on f, Killing-normalised:", sp.factor(lam))
chk("C2 the Casimir acts as a multiple of the identity (no derivatives of f survive) with value proportional to Delta (Delta - 3)",
    lam.free_symbols == {Dl} and sp.simplify(lam / (Dl * (Dl - 3))).is_number)
kfac = sp.simplify(lam / (Dl * (Dl - 3)))
print("   Casimir = %s * Delta (Delta - 3)" % kfac)
chk("C3 deep MOND (phi weight 0) has Casimir 0; Newton/Yamabe (weight 1/2) has |Delta(3-Delta)| = 5/4; the scalar weights 1 and 2 (conformal mass) coincide", lam.subs(Dl, 0) == 0 and sp.simplify(lam.subs(Dl, sp.Rational(1, 2)) / kfac + sp.Rational(5, 4)) == 0 and sp.simplify(lam.subs(Dl, 1) - lam.subs(Dl, 2)) == 0)

# ---------------- D: dS4 Killing fields in flat slicing, independent of H
eta_, Hs = sp.symbols('eta H', positive=True)
Y = (eta_, x, y, z)
gdS = sp.diag(-1, 1, 1, 1) / (Hs**2 * eta_**2)
def killing_check(xi):
    ok_ = True
    for m in range(4):
        for nn_ in range(4):
            L = sum(xi[r] * sp.diff(gdS[m, nn_], Y[r]) + gdS[r, nn_] * sp.diff(xi[r], Y[m]) + gdS[m, r] * sp.diff(xi[r], Y[nn_]) for r in range(4))
            if sp.simplify(L) != 0: ok_ = False
    return ok_
xis = {}
for i in range(3): xis['P%d' % (i + 1)] = [0] + [1 if j == i else 0 for j in range(3)]
xis['D'] = [eta_, x, y, z]
for i in range(3):
    xis['K%d' % (i + 1)] = [2 * X[i] * eta_] + [2 * X[i] * X[j] - ((r2 - eta_**2) if j == i else 0) for j in range(3)]
for (i, j) in [(0, 1), (0, 2), (1, 2)]:
    xis['M%d%d' % (i + 1, j + 1)] = [0] + [(X[i] if k == j else 0) - (X[j] if k == i else 0) for k in range(3)]
kill_all = all(killing_check(v) for v in xis.values())
chk("D1 all 10 fields P_i, M_ij, D, K_i(bulk) are Killing vectors of ds^2 = (-d eta^2 + dx^2)/(H^2 eta^2) for SYMBOLIC H", kill_all)
chk("D2 none of the ten vector fields contains H: the isometry group, its algebra and its Casimirs are blind to the radius L = 1/H (a constant rescaling of the metric leaves every Killing field unchanged)",
    all(not any(getattr(c, 'free_symbols', set()) & {Hs} for c in v) for v in xis.values()))
# bulk Casimir vs Box
fb = sp.Function('F')(*Y)
def dop(name, u):
    v = xis[name]
    return sum(v[m] * sp.diff(u, Y[m]) for m in range(4))
# use the same Killing-form inverse; ordering of names in Binv_s follows `names` (same labels)
Cb = 0
for a in range(n):
    for b in range(n):
        if Binv_s[a, b] != 0:
            Cb += Binv_s[a, b] * dop(names[a], dop(names[b], fb))
Cb = sp.expand(Cb.doit())
sqrtg = 1 / (Hs * eta_)**4; ginv = Hs**2 * eta_**2 * sp.diag(-1, 1, 1, 1)
box = sum(sp.diff(sqrtg * ginv[m, m] * sp.diff(fb, Y[m]), Y[m]) for m in range(4)) / sqrtg
box = sp.expand(box.doit())
ratio = sp.simplify(Cb / box) if box != 0 else None
print("   bulk Casimir / Box_dS4 (generic F):", ratio)
chk("D3 the SO(4,1) Casimir built from the bulk Killing fields equals (constant) x Box_dS4 / H^2 on generic functions (ratio independent of F)", ratio is not None and ratio.free_symbols <= {Hs} and sp.simplify(ratio * Hs**2).is_number)
kbox = sp.simplify(ratio * Hs**2)
# on eta^Delta f(x): Box -> H^2 Delta (3 - Delta) at leading order
boxe_c = sp.simplify(sp.expand((sum(sp.diff(sqrtg * ginv[m, m] * sp.diff(eta_**Dl, Y[m]), Y[m]) for m in range(4)) / sqrtg) / eta_**Dl))
chk("D4 Box eta^Delta = H^2 Delta (3 - Delta) eta^Delta: a dS scalar of mass m falls off as eta^Delta with m^2/H^2 = Delta (3 - Delta)", sp.simplify(boxe_c - Hs**2 * Dl * (3 - Dl)) == 0)
chk("D5 consistency: the Casimir constants from A-C (Delta(Delta-3) normalisation) and D3 agree in sign/size (Casimir on eta^Delta f = kfac Delta(Delta-3) = kbox Delta (3-Delta) => kfac = -kbox)",
    sp.simplify(kfac + kbox) == 0)
# values table
print("   dS4 scalar spectrum m^2/H^2 = Delta(3-Delta):")
for nm, d_ in [('massless minimally coupled (Delta=0,3)', 0), ('Newton/Yamabe weight 1/2', sp.Rational(1, 2)), ('conformally coupled (Delta=1,2)', 1), ('principal-series edge (Delta=3/2)', sp.Rational(3, 2))]:
    print("      %-42s m^2/H^2 = %s" % (nm, sp.nsimplify(d_ * (3 - d_))))
Delta_a0 = sp.Rational(3, 2) - sp.sqrt(sp.Rational(9, 4) - sp.Rational(3, 32) / sp.pi)
print("   if m^2 = a0^2 (framework): m^2/H^2 = 3/(32 pi) = %.6f -> Delta = %.6f (complementary series, nearly massless; not special)" % (float(sp.Rational(3, 32) / sp.pi), float(Delta_a0)))
print("\n%d/%d" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
