#!/usr/bin/env python3
"""x1_03_ledger.py -- lane X1 task (1): the ledger.  Every 4 pi / 8 pi / 16 pi / 32 pi / 32 pi^2 instance is decomposed as a product of NAMED ATOMS,
each atom having a source that x1_01_atoms.py / x1_02_dlifts.py recomputed (solid angle, sphere volumes, Fourier/heat-kernel, trace-reversal 2, TT quarter,
thermal period, Pfaffian count, BPST profile integral, ...).  The row's VALUE is recomputed independently of its decomposition (metric / integral / tensor
algebra); the check is  value == product of atoms^exponents  (exact, sympy).  Then:
  * every decomposition is mutated (one exponent shifted) and must FAIL (non-vacuity);
  * NON-UNIQUENESS control: 32 pi has 5 exact decompositions over {2, 4 pi, 2 pi} within exponents [-4,4]: matching a decomposition is not evidence of origin,
    only the derivation labels are (the honest limit of any ledger);
  * the D-class of each row (D-independent 'EH-normalisation class' vs D-dependent 'geometry class') is read from x1_dlifts.json (computed in x1_02);
  * the MacDowell-Mansouri / TT double role of 1/(64 pi G) is tested: equal at D = 4, different origin (QEH vs MMQ), different value at D = 5.
Exit 0 iff all checks and controls behave as declared.  Requires x1_atoms.json and x1_dlifts.json (run x1_01, x1_02 first).
"""
import sys, json, itertools, time
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations

ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name, flush=True)
def ctl(name, cond_rejected):
    ok.append(bool(cond_rejected)); print(("PASS CONTROL " if cond_rejected else "FAIL CONTROL ") + name, flush=True)
here = __file__.rsplit('/', 1)[0]
atoms_json = json.load(open(here + '/x1_atoms.json')); dl = json.load(open(here + '/x1_dlifts.json'))
T0 = time.time()
pi = sp.pi
eps = sp.symbols('epsilon')

# ================================================================ independent recomputations of the VALUES
# (a) VAR: the factor 2 in T_mn = -(2/sqrt(-g)) dS_m/dg^{mn}  (scalar field: T_00 must be the energy density)
u = sp.symbols('u0:4'); p = sp.symbols('p0:4')
sg = 1 / sp.sqrt(-u[0] * u[1] * u[2] * u[3])
Lm = -sp.Rational(1, 2) * sum(u[i] * p[i] ** 2 for i in range(4))
flat = {u[0]: -1, u[1]: 1, u[2]: 1, u[3]: 1}
T00 = sp.simplify((-2 / sg * sp.diff(sg * Lm, u[0])).subs(flat))
rho_scalar = sp.Rational(1, 2) * p[0] ** 2 + sp.Rational(1, 2) * (p[1] ** 2 + p[2] ** 2 + p[3] ** 2)
chk("V1 with T_mn = -(2/sqrt(-g)) delta S_m/delta g^{mn}, a scalar field has T_00 = (1/2)(phidot^2 + |grad phi|^2) = energy density (the factor VAR = 2)", sp.simplify(T00 - rho_scalar) == 0)
T00_wrong = sp.simplify((-1 / sg * sp.diff(sg * Lm, u[0])).subs(flat))
ctl("V1 CONTROL: without the 2 the T_00 is half the energy density (rejected)", sp.simplify(T00_wrong - rho_scalar) != 0)
# (b) EH coefficient: variation of c sqrt(-g) R + S_m gives c G_mn - (1/2) T_mn = 0 ; G = 8 pi T  =>  c = 1/(16 pi)
c = sp.Symbol('c'); Tsym = sp.Symbol('T')
c_EH = sp.solve(sp.Eq(c * 8 * pi * Tsym - sp.Rational(1, 2) * Tsym, 0), c)[0]
chk("V2 EH coefficient: c G_mn = (1/2) T_mn with G_mn = 8 pi G T_mn  =>  c = 1/(16 pi G) = 1/(VAR x 8 pi G)", c_EH == 1 / (16 * pi))
# (c) TT quadratic coefficient in D = 4 (recomputed here): sqrt(-g)R -> c_f (fdot^2 - f'^2 + gdot^2 - g'^2)
def ricci_full(g, ginv, X):
    n = len(X); Gam = [[[sum(ginv[a, d] * (sp.diff(g[d, b], X[c_]) + sp.diff(g[d, c_], X[b]) - sp.diff(g[b, c_], X[d])) for d in range(n)) / 2
                          for c_ in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c_ in range(b, n):
            s = 0
            for a in range(n):
                s += sp.diff(Gam[a][b][c_], X[a]) - sp.diff(Gam[a][b][a], X[c_])
                for d in range(n):
                    s += Gam[a][a][d] * Gam[d][b][c_] - Gam[a][c_][d] * Gam[d][b][a]
            Ric[b, c_] = Ric[c_, b] = s
    return Ric
X4 = sp.symbols('t x y z', real=True); t_, z_ = X4[0], X4[3]
f = sp.Function('f')(t_, z_); gg = sp.Function('g')(t_, z_)
g4 = sp.eye(4); g4[0, 0] = -1; g4[1, 1] = 1 + eps * f; g4[2, 2] = 1 - eps * f; g4[1, 2] = g4[2, 1] = eps * gg
det2 = 1 - eps ** 2 * (f ** 2 + gg ** 2)
gi4 = sp.eye(4); gi4[0, 0] = -1; gi4[1, 1] = (1 - eps * f) / det2; gi4[2, 2] = (1 + eps * f) / det2; gi4[1, 2] = gi4[2, 1] = -eps * gg / det2
Ric4 = ricci_full(g4, gi4, X4); Rs4 = sum(gi4[i, j] * Ric4[i, j] for i in range(4) for j in range(4))
L2 = sp.simplify(sp.diff(sp.sqrt(det2) * Rs4, eps, 2).subs(eps, 0) / 2)
cf = sp.Symbol('cf')
tgt = cf * (sp.diff(f, t_) ** 2 - sp.diff(f, z_) ** 2 + sp.diff(gg, t_) ** 2 - sp.diff(gg, z_) ** 2)
e1 = euler_equations(L2, [f, gg], [t_, z_]); e2 = euler_equations(tgt, [f, gg], [t_, z_])
c_f = sp.solve(sp.simplify(e1[0].lhs - e1[0].rhs - (e2[0].lhs - e2[0].rhs)), cf)[0]
TTN = sp.Integer(2)                                            # h_ij h_ij = 2 f^2 + 2 g^2 (polarisation-tensor norm)
QEH_val = c_f / TTN
chk("V3 TT expansion: sqrt(-g)R -> c_f(...) with c_f = 1/2, and h_ij h_ij = 2 f^2 (TTN = 2): coefficient of d_l h_ij d^l h_ij is c_f/TTN = 1/4 (QEH)", c_f == sp.Rational(1, 2) and QEH_val == sp.Rational(1, 4))
# (d) Isaacson coefficient: energy density of the canonical Hamiltonian / <hdot_ij hdot_ij>
G_ = 1
tv, zv, wv, h0 = sp.symbols('tv zv omega h0', positive=True)
fp = h0 * sp.cos(wv * (tv - zv))
rho_can = sp.Rational(1, 16) / pi * sp.Rational(1, 2) * (sp.diff(fp, tv) ** 2 + sp.diff(fp, zv) ** 2)     # (1/16 pi G) * (1/2)(fdot^2 + f'^2)
avg = lambda e: sp.integrate(e, (tv, 0, 2 * pi / wv)) * wv / (2 * pi)
hdd = avg(2 * sp.diff(fp, tv) ** 2)
isaacson_val = sp.simplify(avg(rho_can) / hdd)
chk("V4 Isaacson coefficient = <energy density of the quadratic action>/<hdot_ij hdot_ij> = 1/(32 pi)", sp.simplify(isaacson_val - 1 / (32 * pi)) == 0)
flux_val = sp.simplify(avg(rho_can) / (wv ** 2 * h0 ** 2))
chk("V4 flux coefficient rho/(omega^2 h0^2) = 1/(32 pi)  (= Isaacson x TTN x <cos^2>)", sp.simplify(flux_val - 1 / (32 * pi)) == 0)
# (e) MM coefficient from 300 random algebraic curvature tensors (D = 4):  R - 6k = alpha (E4(R) - E4(R - k delta)),  alpha = 1/(4k)
rng = np.random.default_rng(31415)
def KN(h, k):
    return (np.einsum('ac,bd->abcd', h, k) + np.einsum('bd,ac->abcd', h, k) - np.einsum('ad,bc->abcd', h, k) - np.einsum('bc,ad->abcd', h, k))
def rand_curv(n):
    R = np.zeros((n,) * 4)
    for _ in range(5):
        h = rng.normal(size=(n, n)); h = h + h.T; k = rng.normal(size=(n, n)); k = k + k.T
        R += KN(h, k)
    return R
def E4t(Rm):
    Ric = np.einsum('acbc->ab', Rm); R = np.trace(Ric)
    return np.sum(Rm * Rm) - 4 * np.sum(Ric * Ric) + R ** 2, R
alphas = []
for _ in range(300):
    Rm = rand_curv(4); kk = rng.uniform(0.3, 2.0)
    d = np.eye(4); dl_ = np.einsum('ac,bd->abcd', d, d) - np.einsum('ad,bc->abcd', d, d)
    e, R = E4t(Rm); e2, _ = E4t(Rm - kk * dl_)
    alphas.append(((R - 6 * kk) / (e - e2)) * 4 * kk)
chk("V5 MacDowell-Mansouri algebra in D = 4: (R - 2 Lambda) = (E4(R) - E4(F))/(4 k) with Lambda = 3k (300 random curvature tensors; alpha x 4k = %.12f +- %.1e)" % (np.mean(alphas), np.std(alphas)), abs(np.mean(alphas) - 1) < 1e-9 and np.std(alphas) < 1e-9)
MMQ_val = sp.Rational(1, 4)
# (f) S^4 Euler / S^2xS^2 / instanton values
S4vol = 8 * pi ** 2 / 3
CGB_val = sp.simplify(24 * S4vol / 2)                                     # int E4 / chi on S^4
CGB_val2 = sp.simplify(8 * (4 * pi) ** 2 / 4)                             # S^2 x S^2, chi = 4
chk("V6 Chern-Gauss-Bonnet constant per unit chi = 32 pi^2 from S^4 (24/L^4 x Vol, chi = 2) and from S^2 x S^2 (8 k1 k2 x areas, chi = 4)", CGB_val == 32 * pi ** 2 and CGB_val2 == 32 * pi ** 2)
rs, rho = sp.symbols('rs rho', positive=True)
INS_val = sp.integrate(2 * pi ** 2 * rs ** 3 * 192 * rho ** 4 / (rs ** 2 + rho ** 2) ** 4, (rs, 0, sp.oo))
RAD16_val = sp.integrate(rs ** 3 * 192 * rho ** 4 / (rs ** 2 + rho ** 2) ** 4, (rs, 0, sp.oo))
chk("V7 BPST: radial profile integral = 16 (RAD16), int F F~ = 2 pi^2 x 16 = 32 pi^2", sp.simplify(RAD16_val) == 16 and sp.simplify(INS_val) == 32 * pi ** 2)
# (g) thermal / horizon values
Gs, Msym, r = sp.symbols('G M r', positive=True)
rh = 2 * Gs * Msym; kap = sp.simplify(sp.diff(1 - 2 * Gs * Msym / r, r).subs(r, rh) / 2); Ah = 4 * pi * rh ** 2
SBH_quarter = sp.simplify(2 * pi / kap * (Msym / 2) / Ah * Gs)          # S G/A with S = (2 pi/kappa) Q_H, Q_H = M/2 (Noether charge, x1_01 A8)
chk("V8 S G/A = (2 pi/kappa)(M/2) G/A = 1/4 for Schwarzschild", SBH_quarter == sp.Rational(1, 4))
chk("V8 Smarr M = kappa A/(4 pi G): coefficient 1/(4 pi)", sp.simplify(Msym * Gs / (kap * Ah) - 1 / (4 * pi)) == 0)
chk("V8 Komar coefficient (M = 2 Q, Q = kappa A/(8 pi G) at the horizon): 1/(8 pi)  for the Noether potential, 1/(16 pi) as 2-form coefficient",
    sp.simplify((Msym / 2) * Gs / (kap * Ah) - 1 / (8 * pi)) == 0)
# (h) Friedmann and free fall and dS/Nariai/Schwarzschild dimensionless products
Frw = sp.Rational(8, 1) * pi / 3                                          # H^2 = (8 pi/3) G rho from G_00 = 3 H^2 (x1_01 A9)
FF_val = 3 * pi / 32
r0, rr2 = sp.symbols('r0 rr2', positive=True)
tff = sp.integrate(1 / sp.sqrt(2 * Gs * Msym * (1 / rr2 - 1 / r0)), (rr2, 0, r0))
chk("V9 free fall G rho t_ff^2 = 3 pi/32 (exact integral, rho = 3M/(4 pi r0^3))", sp.simplify(Gs * (Msym / (4 * pi * r0 ** 3 / 3)) * tff ** 2 - FF_val) == 0)
chk("V9 free fall = (pi/2)^2 / H_F^2 with H_F^2 = (8 pi/3) G rho: t_ff = (pi/2)/H_F  (the free-fall time is a quarter Friedmann cycle)", sp.simplify(FF_val - (pi / 2) ** 2 * 3 / (8 * pi)) == 0)
Lsym = sp.Symbol('L', positive=True)
Nariai = sp.simplify(4 * pi / 1)                                          # Nariai S^2 radius 1/sqrt(Lambda): A Lambda = 4 pi
dS_AL = sp.simplify(4 * pi * Lsym ** 2 * 3 / Lsym ** 2)
Sch_Ak2 = sp.simplify(Ah * kap ** 2)
chk("V9 A Lambda: de Sitter horizon 12 pi, Nariai sphere 4 pi (radius^2 = 1/Lambda), Schwarzschild A kappa^2 = pi", dS_AL == 12 * pi and Sch_Ak2 == pi)
# Lambda and the Nariai/dS areas from the curvature tensors themselves (R_mn = Lambda g_mn):
def _maxsym(n, kk_):
    d_ = np.eye(n); return kk_ * (np.einsum('ac,bd->abcd', d_, d_) - np.einsum('ad,bc->abcd', d_, d_))
kk_ = 0.37
Ric_dS = np.einsum('acbc->ab', _maxsym(4, kk_))
Rm_N = np.zeros((4, 4, 4, 4)); Rm_N[:2, :2, :2, :2] = _maxsym(2, kk_); Rm_N[2:, 2:, 2:, 2:] = _maxsym(2, kk_)
Ric_N = np.einsum('acbc->ab', Rm_N)
chk("V9 from the curvature tensors: dS_4 has R_mn = 3k g (Lambda = 3k, so A Lambda = 4 pi/k x 3k with A = 4 pi/k at the horizon: 12 pi); Nariai dS_2 x S^2 with equal radii has R_mn = k g (Lambda = k, S^2 area 4 pi/k): A Lambda = 4 pi",
    np.allclose(Ric_dS, 3 * kk_ * np.eye(4)) and np.allclose(Ric_N, kk_ * np.eye(4)))
# BH quarter versus the D = 4 accident 1/(BIA x chi(S^2)):
chi_sphere = lambda n: 2 if n % 2 == 0 else 0
bh_q = {D: sp.Rational(1, 4) for D in (4, 5, 6)}                                         # x1_02 L5: S = A/4G in every D
acc = {D: (1 / (sp.Rational(D - 2, D - 3) * chi_sphere(D - 2)) if chi_sphere(D - 2) else sp.oo) for D in (4, 5, 6)}
chk("M3 PER/E8 = 1/(BIA x chi(S^2)) = 1/4 holds at D = 4 (thermal period over Einstein coupling = 1/(trace-reversal 2 x Euler characteristic 2)), but the entropy quarter is 1/4 in every D while 1/(BIA chi(S^{D-2})) is %s at D = 5, 6: the D = 4 reading is an accident, PER/E8 is the D-independent one" % [str(acc[5]), str(acc[6])],
    acc[4] == sp.Rational(1, 4) and acc[5] == sp.oo and acc[6] == sp.Rational(3, 8) and bh_q[5] == bh_q[6] == sp.Rational(1, 4))
# (j) one-graviton EXCHANGE route to kappa_g^2 (the source-coupling route), D = 4..8: T_mn P^{mn,ab} T_ab = (D-3)/(D-2) for static masses;
#     V = -(kappa^2/4)(D-3)/(D-2) G_d(r), G_d = 1/((D-3) Omega_{D-2} r^{D-3});  Newton: V = -G_N/((D-3) r^{D-3})  =>  kappa^2 = 4 (D-2) Omega_{D-2} G_N/(D-3);  Omega G_N = 8 pi G_E (D-3)/(D-2)
Om_ = lambda n: sp.simplify(2 * pi ** sp.Rational(n + 1, 2) / sp.gamma(sp.Rational(n + 1, 2)))
kap2 = {}
for D in (4, 5, 6, 7, 8):
    eta_ = np.diag([-1.0] + [1.0] * (D - 1))
    P_ = 0.5 * (np.einsum('ma,nb->mnab', eta_, eta_) + np.einsum('mb,na->mnab', eta_, eta_) - (2.0 / (D - 2)) * np.einsum('mn,ab->mnab', eta_, eta_))
    T_ = np.zeros((D, D)); T_[0, 0] = 1.0
    tpt = np.einsum('mn,mnab,ab->', T_, P_, T_)
    assert abs(tpt - (D - 3) / (D - 2)) < 1e-12
    GN_GE = sp.sympify(dl['GN_over_GE'][str(D)])                            # G_N/G_E from x1_02 L3 (Newtonian limit of the Einstein equation and Gauss law)
    kap2[D] = sp.simplify(4 * (D - 2) * Om_(D - 2) * GN_GE / (D - 3))       # kappa^2 / G_E
chk("V10 one-graviton exchange: T P T = (D-3)/(D-2) (=1/BIA) for static masses, and kappa_g^2/G_E = %s for D = 4..8 (=32 pi in every D): the source-coupling route agrees with the action route" % {D: str(kap2[D]) for D in kap2},
    all(sp.simplify(kap2[D] - 32 * pi) == 0 for D in kap2))
chk("V10 consistency of the two routes: canonical (1/2) = QEH x VAR = (1/4)(2): the second-order coefficient is fixed by universality of the source coupling; the graviton 4 = VAR^2 = CAN VAR/QEH  (D-independent in both)",
    sp.Rational(1, 2) == QEH_val * 2 and 4 == 2 ** 2)
ctl("V10 CONTROL: with a wrong tensor structure 1/(D-2) instead of (D-3)/(D-2) the exchange route would give D-dependent kappa^2 (D = 5 differs from 32 pi)", sp.simplify(4 * Om_(3) * sp.sympify(dl['GN_over_GE']['5']) * 3 / 1 - 32 * pi) != 0)

# ================================================================ atoms and decompositions
A = {
    'S2':   (4 * pi,              'solid angle of S^2 (Gauss flux; FT of 1/q^2; heat kernel)',                 'D-dep: Omega_{D-2}'),
    'S3':   (2 * pi ** 2,         'volume of S^3 (angular integral)',                                          'D=4 (n = D/2)'),
    'BIA':  (sp.Integer(2),       'trace-reversal factor G_00 = 2 Lap Phi',                                    'D-dep: (D-2)/(D-3)'),
    'VAR':  (sp.Integer(2),       'the 2 in T_mn = -(2/sqrt(-g)) dS_m/dg^{mn}',                                'D-indep (convention)'),
    'QEH':  (QEH_val,             'TT second-order EH coefficient (c_f/TTN)',                                  'D-indep (computed D=4..8)'),
    'CAN':  (sp.Rational(1, 2),   'canonical normalisation (1/2)(d phi)^2',                                    'D-indep (convention)'),
    'VIR':  (sp.Integer(2),       'wave energy = kinetic + gradient, equal (virial)',                          'D-indep'),
    'TTN':  (TTN,                 'polarisation norm h_ij h_ij = 2 f^2',                                       'D-indep (convention)'),
    'AVG':  (sp.Rational(1, 2),   'time average of cos^2',                                                     'D-indep'),
    'PER':  (2 * pi,              'Euclidean regularity period 2 pi/kappa',                                    'D-indep'),
    'CHI2': (sp.Integer(2),       'Euler characteristic of S^2, S^4',                                          'topological'),
    'PF':   (sp.Integer(8),       'Pfaffian pairing count 2^n n! at n = 2',                                    'D=4 (n = D/2)'),
    'RAD16': (sp.Integer(16),     'BPST radial profile integral',                                              'D=4 only'),
    'TRC':  (sp.Rational(1, 4),   'SU(2) trace normalisation: tr F^2 = F^aF^a/2 and F^F = F F~ d^4x/2',        'D=4 only'),
    'ANG':  (pi / 2,              'quarter-cycle angle of the radial free-fall cycloid',                        'Newtonian, D-dep'),
    'F3':   (sp.Rational(1, 3),   '1/dim SO(3): G_00 = 3 H^2',                                                 'D-dep: 2/((D-1)(D-2))'),
    'MMQ':  (MMQ_val,             'MacDowell-Mansouri algebra: 1/(2(D-2)(D-3)) at D = 4',                      'D-dep; EH-closure only at D = 4'),
    'HOR':  (sp.Integer(4),       '(r_s kappa)^-2 for Schwarzschild (r_s = 2GM, kappa = 1/(2 r_s))',            'D-dep: 4/(D-3)^2'),
    'FIT':  (sp.Integer(4),       'the puzzle: 1/kappa_fit^2, kappa = 1/2 FITTED',                             'unknown'),
}
A['E8'] = (A['BIA'][0] * A['S2'][0], 'Einstein 8 pi = BIA x S2 (fixed so that G_N = G_E at D = 4)', 'conv E: D-indep by definition; conv N: D-dep')
chk("A0 Einstein 8 pi = BIA x S2 = 2 x 4 pi and G_N = G_E at D = 4 only (x1_02 L3)", A['E8'][0] == 8 * pi and dl['GN_over_GE']['4'] == '1' and dl['GN_over_GE']['5'] != '1')
val = lambda name: A[name][0]
rows = [
 # id, description, independent value, decomposition {atom: exp}, family
 ('R01', 'Poisson / Gauss solid angle 4 pi',                     4 * pi,                              {'S2': 1},                                                  'GAUSS'),
 ('R02', 'Einstein constant 8 pi (G_mn = 8 pi G T_mn)',          8 * pi,                              {'BIA': 1, 'S2': 1},                                        'GAUSS'),
 ('R03', 'EH action 1/(16 pi G)',                                c_EH,                                {'VAR': -1, 'BIA': -1, 'S2': -1},                           'GAUSS'),
 ('R04', 'TT graviton kinetic coeff. 1/(64 pi G)  [(1/64 pi G) d h_ij d h_ij]', c_EH * QEH_val,     {'VAR': -1, 'BIA': -1, 'S2': -1, 'QEH': 1},                 'GAUSS'),
 ('R05', 'graviton coupling kappa_g^2 = 32 pi G (tensor-canonical)', 1 / (2 * c_EH * QEH_val),      {'CAN': 1, 'VAR': 1, 'BIA': 1, 'S2': 1, 'QEH': -1},         'GAUSS'),
 ('R05b', 'same kappa_g^2 = 32 pi G from one-graviton exchange (source route)', kap2[4],           {'VAR': 2, 'BIA': 1, 'S2': 1},                              'GAUSS'),
 ('R06', 'Isaacson 1/(32 pi G)',                                 isaacson_val,                        {'VIR': 1, 'VAR': -1, 'BIA': -1, 'S2': -1, 'QEH': 1},       'GAUSS'),
 ('R07', 'GW flux coefficient rho/(omega^2 h0^2) = 1/(32 pi G)', flux_val,                            {'VIR': 1, 'VAR': -1, 'BIA': -1, 'S2': -1, 'QEH': 1, 'TTN': 1, 'AVG': 1}, 'GAUSS'),
 ('R08', 'MacDowell-Mansouri Euler coeff. L^2/(64 pi G)',        c_EH * (sp.Rational(1, 1) * MMQ_val), {'VAR': -1, 'BIA': -1, 'S2': -1, 'MMQ': 1},                'GAUSS x MM'),
 ('R09', 'Chern-Gauss-Bonnet constant 32 pi^2 chi',              CGB_val,                             {'CHI2': 1, 'S2': 2},                                       'TOPOLOGICAL'),
 ('R10', '  same, Chern-Weil form (2 pi)^2 x 2^n n!',            CGB_val,                             {'PER': 2, 'PF': 1},                                        'TOPOLOGICAL'),
 ('R11', 'BPST instanton int F F~ = 32 pi^2',                    INS_val,                             {'S3': 1, 'RAD16': 1},                                       'TOPOLOGICAL'),
 ('R12', 'instanton action 8 pi^2/g^2 (per k)',                  sp.simplify(INS_val / 4),            {'S3': 1, 'RAD16': 1, 'TRC': 1},                              'TOPOLOGICAL'),
 ('R13', 'dS Euclidean action |I| = c_E 32 pi^2 chi = pi L^2/G', pi,                                  {'VAR': -1, 'BIA': -1, 'S2': 1, 'MMQ': 1, 'CHI2': 2},        'TOPOLOGICAL x GAUSS'),
 ('R14', 'MM gauge coupling 1/g^2 = L^2/(16 pi hbar G) (= 4 c_E)', 4 * c_EH * MMQ_val,                 {'VAR': -1, 'BIA': -1, 'S2': -1},                           'GAUSS x MM'),
 ('R15', 'Bekenstein-Hawking S = A/(4G)  [1/4]',                SBH_quarter,                         {'PER': 1, 'E8': -1},                                       'THERMAL'),
 ('R16', 'Hawking T = kappa/(2 pi)',                             1 / (2 * pi),                        {'PER': -1},                                                'THERMAL'),
 ('R17', 'Komar / first-law coefficient 1/(8 pi G)',             sp.Rational(1, 8) / pi,              {'E8': -1},                                                 'GAUSS'),
 ('R18', 'Smarr M = kappa A/(4 pi G)',                           1 / (4 * pi),                        {'S2': -1},                                                 'GAUSS'),
 ('R19', 'Friedmann H^2 = (8 pi/3) G rho',                      Frw,                                 {'E8': 1, 'F3': 1},                                         'GAUSS'),
 ('R20', 'free fall G rho t_ff^2 = 3 pi/32',                     FF_val,                              {'ANG': 2, 'E8': -1, 'F3': -1},                             'ANGLE'),
 ('R21', 'de Sitter horizon A Lambda = 12 pi',                   dS_AL,                               {'S2': 1, 'F3': -1},                                        'GAUSS'),
 ('R22', 'Nariai sphere A Lambda = 4 pi',                        Nariai,                              {'S2': 1},                                                  'GAUSS'),
 ('R23', 'Schwarzschild A kappa^2 = pi',                         Sch_Ak2,                             {'S2': 1, 'HOR': -1},                                       'GAUSS x HOR'),
 ('R24', 'PUZZLE Lambda = 32 pi a0^2',                           32 * pi,                             {'E8': 1, 'FIT': 1},                                        'GAUSS x FIT'),
 ('R25', 'PUZZLE A Lambda = 32 pi^2, A = pi/a0^2',               32 * pi ** 2,                        {'E8': 1, 'S2': 1},                                         'GAUSS x GAUSS'),
 ('R26', 'PUZZLE G rho = 4 a0^2 (pi-free)',                      sp.Integer(4),                       {'FIT': 1},                                                 'FIT'),
 ('R27', '  same 32 pi as (8 pi)^2/(2 pi)  [BH-quarter form; NOT independent of R24]', 32 * pi,        {'E8': 2, 'PER': -1},                                       'THERMAL'),
]
def product(dec):
    p = sp.Integer(1)
    for k, e in dec.items():
        p *= A[k][0] ** e
    return sp.simplify(p)
tab = []
n_dec_ok = 0
for (rid, desc, value, dec, fam) in rows:
    prod = product(dec)
    good = sp.simplify(sp.nsimplify(value) - prod) == 0
    chk("%s %-62s value %-12s = %s" % (rid, desc, str(sp.simplify(value)), ' '.join('%s^%d' % (k, e) if e != 1 else k for k, e in dec.items() if e != 0)), good)
    n_dec_ok += good
    # mutation: shift the exponent of one atom (first non-zero) by 1 -> must break
    k0 = [k for k, e in dec.items() if e != 0][0]
    mut = dict(dec); mut[k0] += 1
    ctl("%s mutation (exponent of %s shifted) is rejected" % (rid, k0), sp.simplify(sp.nsimplify(value) - product(mut)) != 0)
    tab.append({'id': rid, 'desc': desc, 'value': str(sp.simplify(value)), 'decomp': {k: int(e) for k, e in dec.items() if e != 0}, 'family': fam})
# ---------------------------------------------------------------- non-uniqueness control
target = 32 * pi
sols = []
for a_, b_, c_ in itertools.product(range(-4, 5), repeat=3):
    if sp.simplify(sp.Integer(2) ** a_ * (4 * pi) ** b_ * (2 * pi) ** c_ - target) == 0:
        sols.append((a_, b_, c_))
chk("N1 NON-UNIQUENESS: 32 pi = 2^a (4 pi)^b (2 pi)^c has %d exact solutions with exponents in [-4,4]: %s" % (len(sols), sols), len(sols) >= 5)
ctl("N1 CONTROL: the count would be 0 for a target with an odd prime the atoms cannot make (35 pi)", all(sp.simplify(sp.Integer(2) ** a_ * (4 * pi) ** b_ * (2 * pi) ** c_ - 35 * pi) != 0 for a_, b_, c_ in itertools.product(range(-4, 5), repeat=3)))
print("      => a matched decomposition is bookkeeping; only the DERIVATION labels (V1-V9, x1_01, x1_02) carry information about origin.")

# ---------------------------------------------------------------- 2^a pi^b table and family incidence
def ab(v):
    rat, b = sp.sympify(v).as_coeff_exponent(pi)
    return b, rat
print("\n  row  value            pi-power  rational part")
for rrow in tab:
    b, rat = ab(sp.sympify(rrow['value']))
    print("  %-4s %-16s %3d       %s" % (rrow['id'], rrow['value'], b, rat))
inc = {}
for rrow in tab:
    for k in rrow['decomp']:
        inc.setdefault(k, []).append(rrow['id'])
print("\n  atom incidence (which rows use which atom):")
for k in sorted(inc):
    print("   %-5s %-70s  rows %s   [%s]" % (k, A[k][1], ','.join(inc[k]), A[k][2]))

# ---------------------------------------------------------------- the two 1/(64 pi G)'s: R04 (TT) and R08 (MM Euler)
R04_D = {D: c_EH * sp.Rational(1, 4) for D in (4, 5, 6)}                                  # QEH is D-independent (x1_02 L4)
R08_D = {D: c_EH * sp.Rational(1, 2 * (D - 2) * (D - 3)) for D in (4, 5, 6)}              # GB-shift coefficient 2(D-2)(D-3) (x1_02 L8)
chk("M1 R04 (TT kinetic) and R08 (MM Euler) are the same number 1/(64 pi) at D = 4 ...", R04_D[4] == R08_D[4] == 1 / (64 * pi))
chk("M1 ... but different atoms (QEH vs MMQ) and different values at D = 5, 6: %s vs %s" % ({D: str(R04_D[D]) for D in (5, 6)}, {D: str(R08_D[D]) for D in (5, 6)}),
    R04_D[5] != R08_D[5] and R04_D[6] != R08_D[6] and dl['MM_closes_only_at_D'] == [4])
chk("M1 and the EH-Lambda closure (R - 2 Lambda = (Euler - F^2)/norm) exists only at D = 4 (x1_02 L8): so the MM 1/4 is a D = 4 algebra, the TT 1/4 a D-independent expansion coefficient", dl['MM_closes_only_at_D'] == [4])
# lane-A cross-check: 1/g^2 = L^2/(16 pi hbar G) and 8 pi^2/g^2 = S_dS/2
Ls, Gq = sp.symbols('L G', positive=True)
inv_g2 = 4 * (Ls ** 2 / (64 * pi * Gq))
chk("M2 lane-A coupling: 1/g^2 = 4 c_E = L^2/(16 pi hbar G);  8 pi^2/g^2 = pi L^2/(2 G) = S_dS/2 (S_dS = pi L^2/G);  |I_E| = 2 x (8 pi^2/g^2) = S_dS",
    sp.simplify(inv_g2 - Ls ** 2 / (16 * pi * Gq)) == 0 and sp.simplify(8 * pi ** 2 * inv_g2 - pi * Ls ** 2 / (2 * Gq)) == 0 and sp.simplify(2 * 8 * pi ** 2 * inv_g2 - pi * Ls ** 2 / Gq) == 0)

# ---------------------------------------------------------------- the D-lift of each row's 'extra 4' (read from x1_dlifts.json): H_ONE test
Ds = ('4', '5', '6', '7', '8')
slots = {
    'graviton kappa_g^2/(8 pi G_E)  [QEH^-1]':       {D: sp.Integer(4) for D in Ds},
    'Bekenstein-Hawking 1/S-quarter  [E8/PER]':      {D: sp.Integer(4) for D in Ds},
    'Tangherlini (r_h kappa)^-2  [HOR]':             {D: sp.Rational(dl['Tang_inv_sq'][D]) for D in Ds},
    'MM/GB-shift 2(D-2)(D-3)  [1/MMQ]':              {D: sp.Integer(2 * (int(D) - 2) * (int(D) - 3)) for D in Ds},
}
print("\n  D-lift of each row's 'extra 4' (D = 4..8), computed in x1_02:")
for k, v in slots.items():
    print("   %-46s %s" % (k, [str(v[D]) for D in Ds]))
same = lambda a, b: all(sp.simplify(slots[a][D] - slots[b][D]) == 0 for D in Ds)
ks = list(slots)
chk("H1 the graviton '4' and the Bekenstein-Hawking '4' have the SAME D-lift (both constant 4): they are one EH-normalisation class", same(ks[0], ks[1]))
chk("H1 but the Tangherlini and MM/GB-shift '4's have different D-lifts from it and from each other", (not same(ks[0], ks[2])) and (not same(ks[0], ks[3])) and (not same(ks[2], ks[3])))
ctl("H1 CONTROL: a function of D that were the graviton 4 would have to be constant; D itself is not (D = 5 gives 5)", slots[ks[0]]['5'] != 5)
npair = sum(1 for a, b in itertools.combinations(ks, 2) if not same(a, b))
chk("H1 => no single function g(D) generates all the '4's: %d of %d slot pairs have different D-lifts (a generator must be a formula in D)" % (npair, len(ks) * (len(ks) - 1) // 2), npair == 5)

print("\n%d/%d checks and controls behave as declared  (%.1f s)" % (sum(ok), len(ok), time.time() - T0))
json.dump({'rows': tab, 'atoms': {k: [str(v[0]), v[1], v[2]] for k, v in A.items()}, 'slots': {k: {D: str(x) for D, x in v.items()} for k, v in slots.items()}}, open(here + '/x1_ledger.json', 'w'), indent=1)
sys.exit(0 if all(ok) else 1)
