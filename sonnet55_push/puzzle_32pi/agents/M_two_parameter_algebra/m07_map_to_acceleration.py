"""m07: what map from an algebraic number to an acceleration would be needed, and is any such map derived?

 A  Buckingham: the accelerations that can be built from the kinematical scales and central-charge scales; where hbar can and cannot enter.
 B  the puzzle number as an eigenvalue/weight/integer question: the DECLARED candidate origins of a '1/2' (all listed before any evaluation), classified by
    (i) forced by algebra or dimension?  (ii) hbar-free?  (iii) same value in every spatial dimension d?  (iv) is the map to kappa derived?
 C  the quantised 'reduced cosmological constant' of the conformal-Galilei ladder: which integer N would the puzzle need, under each normalisation convention?
 D  two dS embeddings in so(4,2): the relative modulus is free.
"""
import sympy as sp, numpy as np, mpmath as mp, sys, itertools
from m_vf import so_pq
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ---------------- A Buckingham ----------------
M_, L_, T_ = sp.symbols('M L T')
dims = {'c': (0, 1, -1), 'G': (-1, 3, -2), 'rho': (1, -3, 0), 'hbar': (1, 2, -1), 'a0': (0, 1, -2), 'H': (0, 0, -1), 'Lambda': (0, 0, -2), 'c3': (0, -1, 2)}
def nullspace_of(vars_):
    A = sp.Matrix([[dims[v][i] for v in vars_] for i in range(3)])
    return A.nullspace()
ns = nullspace_of(['c', 'G', 'rho', 'hbar'])
print("A: dimensionless group of (c, G, rho, hbar):", [dict(zip(['c', 'G', 'rho', 'hbar'], list(v))) for v in ns])
chk("A1 (c,G,rho,hbar) have exactly ONE dimensionless group, Pi = hbar G^2 rho / c^5", len(ns) == 1 and list(ns[0] / ns[0][3]) == [-5, 2, 1, 1])
# a0 in terms of (c,G,rho): unique real exponents
xs = sp.symbols('x_c x_G x_rho')
sol = sp.solve([sum(xs[k] * dims[v][i] for k, v in enumerate(['c', 'G', 'rho'])) - dims['a0'][i] for i in range(3)], xs, dict=True)
print("   a0 = c^x G^y rho^z :", sol)
chk("A2 without hbar the acceleration built from (c,G,rho) is UNIQUE: a0 = nu c sqrt(G rho) with nu a dimensionless number: the whole content of kappa is nu", sol == [{xs[0]: 1, xs[1]: sp.Rational(1, 2), xs[2]: sp.Rational(1, 2)}])
# numerical size of Pi with the observed vacuum density
c = mp.mpf(299792458); G = mp.mpf('6.6743e-11'); hbar = mp.mpf('1.054571817e-34')
H0 = mp.mpf('67.4e3') / mp.mpf('3.0856775814913673e22'); OL = mp.mpf('0.685')
rho_L = 3 * H0 ** 2 * OL / (8 * mp.pi * G)      # mass density of the vacuum energy
Pi = hbar * G ** 2 * rho_L / c ** 5
print("   rho_Lambda = %s kg/m^3 ; Pi = hbar G^2 rho_L / c^5 = %s" % (mp.nstr(rho_L, 4), mp.nstr(Pi, 4)))
a0_fw = c * H0 / mp.sqrt(32 * mp.pi / 3)
print("   framework scale c H / Z = %s m/s^2 (sanity)" % mp.nstr(a0_fw, 4))
chk("A3 Pi ~ 1e-122: any dependence a0 ~ Pi^n with n != 0 is 122n orders of magnitude away from an O(1) coefficient; a hbar-carrying number (spin 1/2 x hbar, zero-point hbar w/2) can therefore enter a0 only if hbar CANCELS in a ratio", 1e-125 < Pi < 1e-119)
chk("A4 sanity: c H0 / Z with Z = sqrt(32 pi/3) is 1.1e-10 m/s^2 (the framework a0)", 1.0e-10 < a0_fw < 1.3e-10)
# kinematical scales only: accelerations from (c, rate) and central charges (mass m, hbar)
ns2 = nullspace_of(['a0', 'c', 'H'])
chk("A5 from the kinematical scales alone (c, a rate H) the only acceleration is c H: a0 = nu c H, nu dimensionless (one relation among (a0,c,H))", len(ns2) == 1 and list(ns2[0] / ns2[0][0]) == [1, -1, -1])
ns3 = nullspace_of(['a0', 'c', 'hbar'])
chk("A6 from (c, hbar) alone NO acceleration exists (a mass is needed: Compton m c^3/hbar): a central charge m adds the scale m c^3/hbar, which is not a0 unless m is set by G and rho (G-dependent)", ns3 == [] or all(v[0] == 0 for v in ns3))
# Hubble mass
mH = c ** 3 / (G * H0)
print("   Hubble mass c^3/(G H) = %s kg ; Compton acceleration of a mass m_H*Z: m c^3/hbar = %s m/s^2 (vs a0 = %s)" % (mp.nstr(mH, 3), mp.nstr(mH * 5.7888 * c ** 3 / hbar, 3), mp.nstr(a0_fw, 3)))

# ---------------- B declared candidates ----------------
d_ = sp.symbols('d', positive=True)
cands = {}
# 1 inversion weight and 2 higher-dimensional Schwarzschild surface gravity times r_s
inv_w = (d_ - 2) / 2
r, rs = sp.symbols('r r_s', positive=True)
f_tan = 1 - (rs / r) ** (d_ - 2)
kappa_s = sp.simplify((sp.diff(f_tan, r) / 2).subs(r, rs) * rs)
cands['inversion weight (d-2)/2 of the Newton potential'] = dict(value_d3=inv_w.subs(d_, 3), hbar=False, d_indep=False, forced='harmonic Green function r^-(d-2)', formula=inv_w)
cands['Schwarzschild surface gravity x r_s in d+1 dims'] = dict(value_d3=kappa_s.subs(d_, 3), hbar=False, d_indep=False, forced='f = 1 + 2 phi/c^2 and the same exponent d-2', formula=kappa_s)
chk("B1 the two d-dependent candidates are the SAME function: higher-dimensional Schwarzschild kappa_s r_s = (d-2)/2 = inversion weight (both are the fall-off exponent of the Green function over 2): one origin, not two", sp.simplify(inv_w - kappa_s) == 0)
# 3 dilatation exponent of the a0-invariant scaling: from the weight equation a0 ~ L T^-2 -> 1-2z = 0
z = sp.symbols('z'); z_a0 = sp.solve(1 - 2 * z, z)[0]
cands['dilatation exponent z_a0 (a0 invariant)'] = dict(value_d3=z_a0, hbar=False, d_indep=True, forced='dimension of a0 = L/T^2 (and [K,K] = P/a0: w(P) = 2 w(K))', formula=z_a0)
# 4 spin-1/2 eigenvalue
Jz = sp.Matrix([[sp.Rational(1, 2), 0], [0, -sp.Rational(1, 2)]])
cands['spin-1/2 J_z eigenvalue (times hbar)'] = dict(value_d3=sp.Rational(1, 2), hbar=True, d_indep=False, forced='SU(2) fundamental', formula=sp.Rational(1, 2))
# 5 ad_H spectrum ratio 2:1 from m06
cands['ad_H eigenvalue ratio 1:2 with c3 != 0 (m06)'] = dict(value_d3=sp.Rational(1, 2), hbar=False, d_indep=True, forced='weight additivity of [K,K] = c3 P', formula=sp.Rational(1, 2))
# 6 oscillator zero point
cands['zero-point energy hbar w/2'] = dict(value_d3=sp.Rational(1, 2), hbar=True, d_indep=False, forced='[a,a^dag] = 1', formula=sp.Rational(1, 2))
# 7 conformal-Galilei N=4 <-> z = 2/N = 1/2
cands['z = 2/N at N = 4 (conformal Galilei level l = 2)'] = dict(value_d3=sp.Rational(2, 4), hbar=False, d_indep=True, forced='finite-dimensional cg_l requires 2l = N integer; a0-invariant scaling is N = 4', formula=sp.Rational(2, 4))
print("\nB: declared candidates (all evaluated to 1/2 at d = 3):")
for k, v in cands.items():
    print("   %-52s value %s | hbar-free %s | d-independent %s | forced by: %s" % (k, v['value_d3'], not v['hbar'], v['d_indep'], v['forced']))
    if isinstance(v['formula'], sp.Basic) and v['formula'].has(d_):
        print("        d = 2..6:", [sp.nsimplify(v['formula'].subs(d_, dd)) for dd in range(2, 7)])
chk("B2 all seven candidates equal 1/2 at d = 3 (declared before the classification)", all(sp.simplify(v['value_d3'] - sp.Rational(1, 2)) == 0 for v in cands.values()))
survive = [k for k, v in cands.items() if (not v['hbar']) and v['d_indep']]
print("   hbar-free AND d-independent:", survive)
chk("B3 only three candidates are hbar-free and d-independent: z_a0 = 1/2, the ad_H ratio 1:2, and z = 2/N at N = 4 - and these are ONE origin (a bilinear bracket [K,K] -> P gives w(P) = 2 w(K); N = 4 <-> z = 1/2 is the same scaling)", len(survive) == 3)
chk("B4 hbar-carrying candidates (spin 1/2, zero-point) are excluded from a0 by A3 unless hbar cancels; d-dependent ones (inversion, Schwarzschild) are not 1/2 at d = 4 (value 1): they do not survive the p05-type second-setting test", set(k for k, v in cands.items() if v['hbar']) == {'spin-1/2 J_z eigenvalue (times hbar)', 'zero-point energy hbar w/2'} and sp.simplify(inv_w.subs(d_, 4)) == 1)
# the map: a0 = kappa c sqrt(G rho): kappa is defined through c and rho, none of which is in the algebra
print("\n   The map needed for ANY of them: kappa := a0/(c sqrt(G rho_Lambda)) = candidate value.  The algebra contains: rates (H), 1/c^2 (h1) OR 1/a0 (c3) [never both: m06 B1], central charges m,theta.")
print("   It does NOT contain G or rho_Lambda; and kappa uses c AND a0 at once, which the class of kinematical algebras excludes (c3 h1 = 0).")
# the puzzle relation written in the algebra's own constants: a0 = 1/c3, c^2 = 1/h1, (G rho) ~ b1 (same dimension T^-2), a0^2 = kappa^2 c^2 (G rho)  ->  1/c3^2 = kappa^2 b1/h1
c3s, h1s, b1s, kap = sp.symbols('c3 h1 b1 kappa', nonzero=True)
system = [c3s * h1s, kap ** 2 * c3s ** 2 * b1s - h1s]          # Jacobi c3 h1 = 0 (m06 B1) and the puzzle relation in algebra variables
solsys = sp.solve(system, [c3s, h1s, b1s], dict=True)
print("   puzzle relation in the algebra's own constants: 1/c3^2 = kappa^2 b1/h1 ; with the Jacobi condition c3 h1 = 0 the solutions (all three nonzero) are:", solsys)
chk("B5 the relation a0^2 = kappa^2 c^2 (G rho) written with a0 = 1/c3, c^2 = 1/h1 and G rho -> b1 (the only structure constant of dimension T^-2) has NO solution with c3, h1, b1 all nonzero once Jacobi's c3 h1 = 0 is imposed: it cannot be a relation among the structure constants of any algebra in the class", solsys == [])
print("   also dimensionally: the rate^2 b1 has the dimensions of G rho (T^-2) but the algebra does not say WHICH density: identifying b1 with G rho_Lambda (or 8 pi G rho_Lambda = Lambda) is the Newton-Hooke 'Lambda' reading, an assumption")

# ---------------- C required N ----------------
print("\nC: integer N required by the puzzle for a reduced constant X/omega^2 = N, with omega = xi * a0 (c = 1); Lambda = 32 pi a0^2:")
conv = {'X = Lambda': 32 * sp.pi, 'X = Lambda/3 = H^2': 32 * sp.pi / 3, 'X = 4 pi G rho = Lambda/2': 16 * sp.pi, 'X = 8 pi G rho/3 = H^2': 32 * sp.pi / 3, 'X = G rho = Lambda/(8 pi)': sp.Integer(4)}
xis = {'omega = a0': 1, 'omega = a0/2': sp.Rational(1, 2), 'omega = 2 a0': 2}
for cn, val in conv.items():
    row = {xn: sp.nsimplify(val / xi ** 2) for xn, xi in xis.items()}
    print("   %-28s N = %s   %s" % (cn, val, {k: sp.N(v, 6) for k, v in row.items()}))
chk("C1 for every convention that contains Einstein's 8 pi (Lambda, H^2, 4 pi G rho) the required N is a nonzero rational multiple of pi (transcendental): NOT an integer, for every algebraic xi", all((val / xi ** 2).has(sp.pi) for cn, val in conv.items() if cn != 'X = G rho = Lambda/(8 pi)' for xi in xis.values()))
chk("C2 only the pi-free normalisation X = G rho_Lambda gives an integer, N = 4 (at omega = a0, z = 2/N = 1/2): this is the SAME statement as G rho_Lambda = 4 a0^2, not evidence for it", conv['X = G rho = Lambda/(8 pi)'] == 4)
print("   Caveats stated plainly: (i) the normalisation of the 'reduced cosmological constant' in the source (arXiv:1104.1502, abstract and Sections 1, 5 opened) was not verified; the table lists what each convention would need.")
print("   (ii) in the Galilean algebra omega = a0 is dimensionally impossible (a0 is L/T^2, omega is 1/T): it needs a velocity, i.e. c, which is not in the algebra (c3 h1 = 0).")
chk("C3 dimensional check of (ii): a0/omega has dimensions L/T (a velocity), so 'omega = xi a0' in the c=1 statement silently inserts c", (sp.Matrix(dims['a0']) - sp.Matrix(dims['H'])).T.tolist()[0] == [0, 1, -1])
# scale of the near-integer coincidence: 32 pi is within 0.53 % of 100 + 1/2? decoy
print("   near-integer remark: 32 pi = %s; every real number in [50,150] is within 0.5 of an integer, so 'N = 100 or 101 nearly works' has no content" % sp.N(32 * sp.pi, 6))

# ---------------- D two dS embeddings in so(4,2) ----------------
n42 = 6; eta = np.diag([-1.0, -1.0, 1.0, 1.0, 1.0, 1.0])            # R^{2,4}: the conformal group of Minkowski space is SO(2,4)
basis = []
for i in range(n42):
    for j in range(i + 1, n42):
        M = np.zeros((n42, n42)); M[i, j] = eta[j, j]; M[j, i] = -eta[i, i]; basis.append(M)
def stab_dim(vs):
    A = np.array([np.concatenate([b @ v for v in vs]) for b in basis]).T
    return len(basis) - np.linalg.matrix_rank(A, tol=1e-10)
def sub_basis(vs):
    A = np.array([np.concatenate([b @ v for v in vs]) for b in basis]).T
    u, sv, vt = np.linalg.svd(A); rank = int((sv > 1e-10).sum())
    ns_ = vt[rank:].T                                                # coefficients of the stabiliser in the generator basis
    return [sum(ns_[i, k] * basis[i] for i in range(len(basis))) for k in range(ns_.shape[1])]
def killing_rank(mats):
    m = len(mats); Am = np.array([x.flatten() for x in mats]).T
    ad = []
    for X in mats:
        cols = []
        for Y in mats:
            com = X @ Y - Y @ X; cols.append(np.linalg.lstsq(Am, com.flatten(), rcond=None)[0])
        ad.append(np.array(cols).T)
    Kf = np.array([[np.trace(ad[a] @ ad[b]) for b in range(m)] for a in range(m)])
    return int(np.linalg.matrix_rank(Kf, tol=1e-9))
def nrm(a): return float(a @ eta @ a)
e = np.eye(n42)
v1 = e[0]                                                           # unit TIMELIKE vector (norm -1): stabiliser = so(1,4) = dS4
assert abs(nrm(v1) + 1) < 1e-12
rows = {}
for th in (0.0298, 0.1727, 0.5, 1.0, 2.5):                          # compact relative angle: rotation in the (e0,e1) time-time plane
    v2 = np.cos(th) * e[0] + np.sin(th) * e[1]; rows['rot %.4f' % th] = (stab_dim([v1]), stab_dim([v2]), stab_dim([v1, v2]), -float(v1 @ eta @ v2))
for ch in (0.3, 1.0, 2.0):                                          # hyperbolic relative angle: boost with a spacelike direction
    v2 = np.cosh(ch) * e[0] + np.sinh(ch) * e[2]; rows['boost %.1f' % ch] = (stab_dim([v1]), stab_dim([v2]), stab_dim([v1, v2]), -float(v1 @ eta @ v2))
print("\nD: dS4 = stab of a unit timelike vector in R^{2,4}.  (dim stab v1, dim stab v2, dim of the intersection, |(v1.v2)|):")
for k, v in rows.items(): print("   %-10s" % k, v)
killing_generic = {k: None for k in rows}
kr_gen = killing_rank(sub_basis([v1, np.cos(0.5) * e[0] + np.sin(0.5) * e[1]])); kr_gen2 = killing_rank(sub_basis([v1, np.cosh(1.0) * e[0] + np.sinh(1.0) * e[2]]))
chk("D1 the stabiliser of a unit timelike vector in R^{2,4} is 10-dimensional (de Sitter algebra so(1,4)); two such, at ANY generic relative angle (compact or hyperbolic, 8 values incl. |v1.v2| = 0.9996 and 0.985), meet in a 6-dimensional SEMISIMPLE subalgebra (Killing rank %d, %d): the relative modulus is a continuous parameter that no incidence/dimension count selects" % (kr_gen, kr_gen2),
    all(v[0] == 10 and v[1] == 10 and v[2] == 6 for v in rows.values()) and kr_gen == 6 and kr_gen2 == 6)
n_null = e[0] + e[2]
v2_deg = v1 + (e[1] + e[3])                                         # v1 + null vector orthogonal to v1: unit norm, |v1.v2| = 1, Gram determinant 0
assert abs(nrm(v2_deg) + 1) < 1e-12 and abs(float(v1 @ eta @ (e[1] + e[3]))) < 1e-12 and abs(nrm(e[1] + e[3])) < 1e-12
kr_deg = killing_rank(sub_basis([v1, v2_deg])); dim_deg = stab_dim([v1, v2_deg])
print("   degenerate pair (v2 = v1 + null, orthogonal): dim of intersection = %d, Killing rank = %d" % (dim_deg, kr_deg))
chk("D2 CONTROL: a degenerate pair (Gram determinant 0) also has dimension 6 but a DEGENERATE Killing form (rank %d != 6: it is iso(3), not semisimple): the invariant used does detect special positions; they sit at the boundary |v1.v2| = 1, not at generic values" % kr_deg, kr_deg != 6 and dim_deg == 6)
print("\n%d/%d checks pass" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
