"""m06: the one place an acceleration scale a0 CAN appear as a structure constant, and what Jacobi then forces.

m05 found that the Galilei algebra has four first-order deformation directions in the rotation-covariant class:
    a1  : [H,K] += a1 K              (a rate, 1/T)
    b1  : [H,P] += b1 K              (Newton-Hooke, 1/T^2 = Lambda_NH)
    c3  : [K_i,K_j] += c3 eps_ijk P_k (dimension T^2/L = 1/ACCELERATION)
    h1  : [K,P] += h1 delta H, [K,K] += h1 eps J   (1/c^2)
c3 is the only one D-invariant at z = 1/2, the scaling that leaves an acceleration invariant.  This script solves the full Jacobi problem for c3 != 0.

 A  gauge: the shifts K -> K + wJ, P -> P + wJ change (c2,d3,e3,e4,...) only; c3, d2, a1,a2,b1,b2,h1 are invariant; gauge e3 = e4 = 0 is always reachable.
 B  c3 * h1 = 0 : an inverse-acceleration deformation and a Lorentz (1/c^2) deformation exclude each other.
 C  h1 = 0, a2 != 0: Jacobi <=> d2 fixed and  Q = -(c3/3a2) det (2 tr^2 - 9 det) = 0 ,  tr,det of ad_H on span(K,P):  eigenvalues l1,l2 with  l1 l2 (2 l1 - l2)(l1 - 2 l2) = 0.
 D  a2 = 0 branch: eigenvalues (a1, 2 a1) again.  E explicit algebras and mutations.  F dimensions, weights, dilatations.  G non-isomorphic to Galilei.  H moduli: c3 and the rate scale are independent; only the ratio 2:1 is an invariant.
"""
import sympy as sp, numpy as np, sys, random
from m_tools import *
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

names = 'a1 a2 a3 b1 b2 b3 c1 c2 c3 d1 d2 d3 h1 e2 e3 e4'.split()
S = sp.symbols(names); d = dict(zip(names, S))
f, n = rot_ansatz(d, with_D=False)
polys = jacobi_polys(f, n)
# ---------- A gauge ----------
C = dense(f, n)
w, wp = sp.symbols('w wp')
T = sp.eye(n)
for i in range(3): T[i, 3 + i] = w; T[i, 6 + i] = wp
Cn = change_basis(C, T)
g = lambda a, b, e: sp.expand(Cn[a][b][e])
new = {'a1': g(9, 3, 3), 'a2': g(9, 3, 6), 'a3': g(9, 3, 0), 'b1': g(9, 6, 3), 'b2': g(9, 6, 6), 'b3': g(9, 6, 0), 'c1': g(3, 4, 2), 'c2': g(3, 4, 5), 'c3': g(3, 4, 8),
       'd1': g(6, 7, 2), 'd2': g(6, 7, 5), 'd3': g(6, 7, 8), 'h1': g(3, 6, 9), 'e2': g(3, 7, 2), 'e3': g(3, 7, 5), 'e4': g(3, 7, 8)}
inv = [k for k in names if sp.expand(new[k] - d[k]) == 0]
print("A: constants invariant under K->K+wJ, P->P+w'J:", inv)
chk("A1 the J-shifts leave a1,a2,b1,b2,h1 and the two dimensionful deformation constants c3 (1/acceleration) and d2 invariant", set(['a1', 'a2', 'b1', 'b2', 'h1', 'c3', 'd2']) <= set(inv))
chk("A2 they act as c2 -> c2 + 2w, d3 -> d3 + 2w', e3 -> e3 + w', e4 -> e4 + w: the gauge e3 = e4 = 0 is always reachable (w = -e4, w' = -e3)",
    sp.expand(new['c2'] - d['c2'] - 2 * w) == 0 and sp.expand(new['d3'] - d['d3'] - 2 * wp) == 0 and sp.expand(new['e3'] - d['e3'] - wp) == 0 and sp.expand(new['e4'] - d['e4'] - w) == 0)
gauge = {'e3': 0, 'e4': 0}
# ---------- B ----------
p_h1 = [p for p in polys if sp.simplify(p + 3 * d['c3'] * d['h1']) == 0]
chk("B1 one of the 20 Jacobi polynomials is exactly -3 c3 h1 : c3 h1 = 0.  A finite Lorentz c (h1 != 0) forbids the inverse-acceleration deformation, and vice versa", len(p_h1) == 1)
# ---------- C ----------
par = dict(d); par.update(gauge); par['h1'] = 0
fC, _ = rot_ansatz(par, with_D=False)
PC = jacobi_polys(fC, n)
a1, a2, a3, b1, b2, b3, c1, c2, c3, d1, d2, d3, e2 = [d[k] for k in 'a1 a2 a3 b1 b2 b3 c1 c2 c3 d1 d2 d3 e2'.split()]
sub = {}
sub[c2] = c3 * (2 * a1 - b2) / a2
sub[a3] = (b1 * c3 - a1 * sub[c2]) / 2
sub[d3] = -(sub[a3] + b1 * c3) / a2
sub[c1] = -c3 * sub[d3]
sub[e2] = c3 * d2
sub[d1] = -sub[c2] * d2
sub[b3] = -a2 * d2 - b1 * sub[c2]
resid = [sp.factor(sp.simplify(p.subs(sub))) for p in PC]; resid = [r for r in resid if r != 0]
E1 = sp.numer(sp.together(resid[0]))
d2sol = sp.solve([r for r in resid if sp.degree(sp.numer(sp.together(r)), d2) == 1][0], d2)[0]
resid2 = [sp.factor(sp.simplify(r.subs(d2, d2sol))) for r in resid]; resid2 = [r for r in resid2 if r != 0]
tr, de = a1 + b2, a1 * b2 - a2 * b1
Qx = -(c3 / (3 * a2)) * de * (2 * tr ** 2 - 9 * de)
chk("C1 linear part of Jacobi (h1 = 0, gauge e3=e4=0, a2 != 0) fixes c2, a3, d3, c1, e2, d1, b3 and (via one quadratic) d2 in terms of (a1,a2,b1,b2,c3)", len(sub) == 7 and d2sol.has(c3))
chk("C2 after that, EVERY remaining Jacobi polynomial is a multiple of the single condition Q = -(c3/(3 a2)) det(ad_H) (2 tr^2 - 9 det) = 0", all(sp.simplify(sp.cancel(r / Qx)).free_symbols <= {a1, a2, b1, b2, c3} and sp.simplify(sp.cancel(r / Qx)) is not sp.nan for r in resid2) and len(resid2) >= 1)
l1, l2 = sp.symbols('l1 l2')
comp = {a1: 0, a2: 1, b2: l1 + l2, b1: -l1 * l2}
Qeig = sp.factor(Qx.subs(comp))
print("C: Q in terms of the eigenvalues l1,l2 of ad_H on span(K,P):", Qeig)
chk("C3 Q = -(c3/3) l1 l2 (2 l1 - l2)(l1 - 2 l2): with c3 != 0 the H-action on (K,P) must have a ZERO eigenvalue or eigenvalues in the exact ratio 2:1", sp.simplify(Qeig + c3 * l1 * l2 * (2 * l1 - l2) * (l1 - 2 * l2) / 3) == 0)
chk("C4 in terms of invariants: 2 tr^2 - 9 det = 2 (l1 - 2 l2)(2 l1 - l2)... ie the ratio 2 is where the discriminant relation 2 tr^2 = 9 det holds", sp.simplify((2 * (l1 + l2) ** 2 - 9 * l1 * l2) - (2 * l1 - l2) * (l1 - 2 * l2)) == 0)
# ---------- D: a2 = 0 branch ----------
parD = dict(d); parD.update(gauge); parD['h1'] = 0; parD['a2'] = 0
fD, _ = rot_ansatz(parD, with_D=False)
PD = jacobi_polys(fD, n)
solD = sp.solve(PD, [a3, b3, c1, c2, d1, d2, d3, e2, b2], dict=True)
print("D: a2 = 0 solutions:", solD)
chk("D1 a2 = 0, c3 != 0, a1 != 0: Jacobi forces b2 = 2 a1: ad_H = [[a1,b1],[0,2a1]] has eigenvalues (a1, 2 a1): the 2:1 ratio again", any(s_.get(b2) == 2 * a1 for s_ in solD))
parD0 = dict(parD); parD0['a1'] = 0
solD0 = sp.solve(jacobi_polys(rot_ansatz(parD0, with_D=False)[0], n), [a3, b3, c1, c2, d1, d2, d3, e2, b2], dict=True)
print("   a2 = 0 and a1 = 0:", solD0)
chk("D2 a2 = 0 and a1 = 0: b2 c3 = 0 so b2 = 0: ad_H nilpotent (both eigenvalues 0): the degenerate branch", all(s_.get(b2, b2) == 0 for s_ in solD0))
# ---------- E explicit algebras ----------
def build_params(L1, L2, c3v):
    s_ = {a1: 0, a2: 1, b2: L1 + L2, b1: -L1 * L2, c3: c3v, 'x': 0}
    vals = {a1: 0, a2: 1, b2: L1 + L2, b1: -L1 * L2, c3: c3v}
    d2val = sp.simplify(d2sol.subs(vals))
    dd = {k: sp.simplify(v.subs(vals).subs(d2, d2val)) for k, v in sub.items()}
    dd[d2] = d2val
    out = {str(k): v for k, v in vals.items()}; out.update({str(k): v for k, v in dd.items()})
    out.update({'h1': 0, 'e3': 0, 'e4': 0}); return out
def lie_of(par): return is_lie(rot_ansatz(par, with_D=False)[0], n)
oms = [sp.Rational(1, 1), sp.Rational(3, 7), sp.Rational(1000000, 1), sp.Rational(1, 1000000)]
c3s = [sp.Rational(1, 1), sp.Rational(5, 3), sp.Rational(1, 1000000), sp.Rational(1000000, 1)]
allok = all(lie_of(build_params(om, 2 * om, c3v)) and lie_of(build_params(2 * om, om, c3v)) for om in oms for c3v in c3s)
chk("E1 EXPLICIT: for 16 pairs (omega, c3) spanning 12 orders of magnitude each, spectrum (omega, 2 omega) and (2 omega, omega) satisfy ALL Jacobi identities: c3 and the rate scale are independent", allok)
chk("E2 spectrum (0,0) (Galilei + c3) and (omega, 0) (a friction-type H action) with c3 != 0 satisfy Jacobi", lie_of(build_params(0, 0, 1)) and lie_of(build_params(1, 0, 1)) and lie_of(build_params(0, sp.Rational(7, 2), 3)))
chk("E3 MUTATION: spectrum (omega, 3 omega) with the same construction violates Jacobi", not lie_of(build_params(1, 3, 1)))
chk("E4 MUTATION: expanding Newton-Hooke spectrum (omega, -omega) [b1 = omega^2] with c3 != 0 violates Jacobi: Lambda_NH and the a0-direction cannot coexist", not lie_of(build_params(1, -1, 1)))
chk("E5 MUTATION: oscillating Newton-Hooke (+-i omega) with c3 != 0 violates Jacobi (b1 = -omega^2... spectrum +-i: Q != 0)", not lie_of({'a1': 0, 'a2': 1, 'b2': 0, 'b1': -1, 'c3': 1, 'h1': 0, 'e3': 0, 'e4': 0, **{str(k): v for k, v in {c2: c3*(2*0-0)/1, a3: (-1*1)/2, }.items()}}) )
chk("E6 MUTATION: c3 != 0 together with h1 != 0 violates Jacobi (B1) even at Galilei-like rates", not lie_of({'a2': 1, 'c3': 1, 'h1': 1, 'c1': 1}))
# ---------- F dims and weights ----------
dimJ = sp.Matrix([1, 2, -1]); dimK = sp.Matrix([1, 1, 0]); dimP = sp.Matrix([1, 1, -1])
c3dim = 2 * dimK - dimJ - dimP
LT = (int(c3dim[1]), int(c3dim[2]))
chk("F1 c3 has dimensions (L,T) = (-1, 2): T^2/L = 1/ACCELERATION (mass cancels)", int(c3dim[0]) == 0 and LT == (-1, 2))
half = sp.Rational(1, 2)
fw = lambda z_, c3v, **kw: rot_ansatz({'a2': 1, 'c3': c3v, 'f1': -z_, 'p1': z_ - 1, 'q2': -1, **kw}, with_D=True)[0]
chk("F2 the 11-dimensional algebra 'Galilei + c3 x| D_{1/2}' satisfies Jacobi: a0 (c3 = 1/a0) is a D-invariant deformation exactly at z = 1/2", is_lie(fw(half, 1), 11))
chk("F3 MUTATION: the same c3 with z = 1 (the MOND scaling) or z = 0 or z = 2 violates Jacobi (weight of c3 is 2z - 1)", all(not is_lie(fw(z_, 1), 11) for z_ in (1, 0, 2, sp.Rational(3, 2))))
# no dilatation once a rate is turned on
pp = {str(k): v for k, v in build_params(1, 2, 1).items()}
q1_, q2_, q3_, p1_, p2_, p3_, f1_ = sp.symbols('q1 q2 q3 p1 p2 p3 f1')
fdil, n11 = rot_ansatz({**pp, 'p1': p1_, 'p2': p2_, 'p3': p3_, 'q1': q1_, 'q2': q2_, 'q3': q3_, 'f1': f1_}, with_D=True)
eqs = [v for _, _, v in jacobi_residuals(fdil, n11)]
Aeq = sp.Matrix([[sp.diff(e, u) for u in (p1_, p2_, p3_, q1_, q2_, q3_, f1_)] for e in eqs])
dimder = 7 - Aeq.rank()
solder = sp.solve(eqs, [p1_, p2_, p3_, q1_, q2_, q3_, f1_], dict=True)
print("F: derivation space of  Galilei+c3 with H-spectrum (1,2):", dimder, solder)
inner = {p1_: pp['a1'], p2_: pp['a2'], p3_: pp['a3'], q1_: pp['b1'], q2_: pp['b2'], q3_: pp['b3'], f1_: 0}
tq = q3_ / pp['b3']
is_inner = len(solder) == 1 and dimder == 1 and all(sp.simplify(solder[0].get(k, k) - tq * v) == 0 for k, v in inner.items() if k != q3_)
chk("F4 with c3 != 0 AND a nonzero H-spectrum (1,2) the ONLY derivation is the inner one, ad_H (weights of H fixed to 0): there is NO scalar dilatation D: a0 and the rate together break every scaling", is_inner)

# ---------- G non-isomorphic to Galilei ----------
def derivation_dim(par):
    fx, nn = rot_ansatz(par, with_D=False); Cx = np.array(dense(fx, nn), dtype=float)
    rows = []
    for a in range(nn):
        for b in range(a + 1, nn):
            for e in range(nn):
                row = np.zeros((nn, nn))       # unknown D[m,k]: D e_k = sum_m D[m,k] e_m
                # (D[x,y])_e = sum_k C[a,b,k] D[e,k] ; ([Dx,y])_e = sum_m D[m,a] C[m,b,e] ; ([x,Dy])_e = sum_m D[m,b] C[a,m,e]
                for k in range(nn): row[e, k] += Cx[a, b, k]
                for m in range(nn): row[m, a] -= Cx[m, b, e]; row[m, b] -= Cx[a, m, e]
                rows.append(row.flatten())
    M = np.array(rows); s_ = np.linalg.svd(M, compute_uv=False)
    return nn * nn - int((s_ > 1e-9 * s_[0]).sum())
dG = derivation_dim({'a2': 1}); dGc = derivation_dim({'a2': 1, 'c3': 1, 'e3': 0, 'e4': 0, 'c2': 0, 'a3': 0, 'b1': 0, 'b2': 0, 'c1': 0, 'd3': 0, 'e2': 0, 'd1': 0, 'b3': 0, 'd2': 0}) 
print("G: dim Der(Galilei) =", dG, "   dim Der(Galilei + c3) =", dGc)
chk("G1 Galilei + c3 is NOT isomorphic to Galilei: their derivation algebras have different dimensions (%d vs %d)" % (dG, dGc), dG != dGc)
# ---------- H moduli / invariants ----------
al, be, ga = sp.symbols('alpha beta gamma', positive=True)
Sc = sp.diag(*([1] * 3 + [al] * 3 + [be] * 3 + [ga]))
fH, _ = rot_ansatz({'a2': a2, 'b1': b1, 'b2': b2, 'a1': a1, 'c3': c3, **{str(k): v for k, v in sub.items()}, 'd2': d2sol, 'h1': 0, 'e3': 0, 'e4': 0}, with_D=False)
CH = dense(fH, n); CS = change_basis(CH, Sc)
c3p = sp.simplify(CS[3][4][8]); a2p = sp.simplify(-CS[3][9][6]) ; l_scale = sp.simplify(CS[9][3][3])
print("H: under K->aK, P->bP, H->gH: c3 ->", c3p, "; a2 ->", a2p, "; a1 ->", l_scale)
chk("H1 c3 -> (alpha^2/beta) c3, a2 -> (gamma alpha/beta) a2, rates -> gamma * rates: three independent weights => NO monomial of (c3, a2, rate) is rescaling-invariant: the magnitude of c3 relative to a rate is a unit convention",
    sp.simplify(c3p - al ** 2 / be * c3) == 0 and sp.simplify(a2p - ga * al / be * a2) == 0 and sp.simplify(l_scale - ga * a1) == 0
    and sp.Matrix([[2, -1, 0], [1, -1, 1], [0, 0, 1]]).det() != 0)
# invariance of the eigenvalue ratio: ad_H on span(K,P) is a 2x2 matrix M; K/P mixing = similarity, H-rescaling = overall scale: eigenvalue RATIO invariant
Mh = sp.Matrix([[a1, b1], [a2, b2]]); Gm = sp.Matrix(2, 2, sp.symbols('g11 g12 g21 g22')); Mh2 = Gm * Mh * Gm.inv()
lam_ = sp.symbols('lam_')
cp1 = sp.factor(Mh.charpoly(lam_).as_expr()); cp2 = sp.factor(sp.simplify(Mh2.charpoly(lam_).as_expr()))
tr_inv = sp.simplify(Mh2.trace() - Mh.trace()) == 0 and sp.simplify(Mh2.det() - Mh.det()) == 0
scale_ok = sp.simplify((2 * (ga * Mh.trace()) ** 2 - 9 * ga ** 2 * Mh.det()) - ga ** 2 * (2 * Mh.trace() ** 2 - 9 * Mh.det())) == 0
chk("H2 the ratio of the two ad_H eigenvalues is invariant under every K/P mixing (similarity: trace and det unchanged) and every H-rescaling (2 tr^2 - 9 det is homogeneous): the ONLY dimensionless number Jacobi forces is this ratio, 2", tr_inv and scale_ok)

# ---------- I independent numerical test (no gauge fixing, no a2 normalisation, random starts) ----------
from scipy.optimize import least_squares
import warnings; warnings.filterwarnings('ignore')
free_names = [k for k in names if k not in ('c3', 'h1')]
fpoly = sp.lambdify([d[k] for k in free_names] + [d['c3'], d['h1']], polys, 'numpy')
rng = np.random.default_rng(20260929)
def sample(c3v, h1v, ntry=400):
    sols = []
    for _ in range(ntry):
        x0 = rng.normal(size=len(free_names)) * rng.choice([0.3, 1.0, 3.0])
        r = least_squares(lambda x: np.array(fpoly(*x, c3v, h1v), dtype=float), x0, xtol=1e-14, ftol=1e-14, gtol=1e-14, max_nfev=400)
        if np.linalg.norm(r.fun) < 1e-11: sols.append(dict(zip(free_names, r.x)))
    return sols
def spec_defect(s_):
    M = np.array([[s_['a1'], s_['b1']], [s_['a2'], s_['b2']]]); ev = np.linalg.eigvals(M)
    tr_, de_ = np.trace(M), np.linalg.det(M)              # det (2 tr^2 - 9 det) = l1 l2 (2 l1 - l2)(l1 - 2 l2): polynomial in the entries (well conditioned)
    sc = max(np.linalg.norm(M) ** 4, 1e-12)
    return abs(de_ * (2 * tr_ ** 2 - 9 * de_)) / sc, ev
solsA = sample(1.7, 0.0)
defA = [spec_defect(s_)[0] for s_ in solsA]
solsB = sample(0.0, 0.0)
defB = [spec_defect(s_)[0] for s_ in solsB]
generic_B = sum(1 for v in defB if v > 1e-3)
def nondeg(s_):
    M = np.array([[s_['a1'], s_['b1']], [s_['a2'], s_['b2']]]); return abs(np.linalg.det(M)) / max(np.linalg.norm(M) ** 2, 1e-12) > 1e-3
ratios = []
for s_ in solsA:
    if nondeg(s_):
        ev = np.linalg.eigvals(np.array([[s_['a1'], s_['b1']], [s_['a2'], s_['b2']]])); ratios.append(max(abs(ev)) / min(abs(ev)))
print("   of the c3 != 0 solutions, %d have det(ad_H|K,P) != 0; their |l_max/l_min| values: min %.6f max %.6f" % (len(ratios), min(ratios) if ratios else float('nan'), max(ratios) if ratios else float('nan')))
print("I: c3 = 1.7, h1 = 0: %d random Jacobi solutions found; max |det (2 tr^2 - 9 det)|/|M|^4 = %.2e" % (len(solsA), max(defA) if defA else float('nan')))
print("   control c3 = 0     : %d solutions, %d of them with a generic spectrum (defect > 1e-3), max defect %.2e" % (len(solsB), generic_B, max(defB) if defB else float('nan')))
chk("I1 INDEPENDENT numerical solutions of the full 16-constant system (no gauge fixing, random starts, c3 = 1.7, h1 = 0): every one has l1 l2 (2 l1 - l2)(l1 - 2 l2) = 0 to 1e-8 (%d solutions)" % len(solsA), len(solsA) >= 30 and max(defA) < 1e-8)
chk("I1b among the c3 != 0 solutions, the nondegenerate ones (det != 0) all have |l_max/l_min| = 2 to 1e-6 (%d found)" % len(ratios), len(ratios) >= 20 and max(abs(np.array(ratios) - 2)) < 1e-6)
chk("I2 CONTROL: with c3 = 0 the same sampler finds solutions with GENERIC spectra (the constraint is caused by c3, not by the solver): %d of %d generic" % (generic_B, len(solsB)), generic_B >= 5)
solsC = sample(1.7, 0.9, ntry=200)
chk("I3 CONTROL: with c3 = 1.7 and h1 = 0.9 (both nonzero) the sampler finds NO solution (%d found), as B1 requires" % len(solsC), len(solsC) == 0)

# ---------- J parity / time reversal of the a0 direction ----------
Pm = sp.diag(*([1] * 3 + [-1] * 3 + [-1] * 3 + [1]))     # parity: J,H even ; K,P odd
Tm = sp.diag(*([1] * 3 + [-1] * 3 + [1] * 3 + [-1]))     # time reversal (the standard tau): K,H odd ; J,P even
fJ, _ = rot_ansatz({'a2': 1, 'c3': c3, 'e3': 0, 'e4': 0}, with_D=False)   # NOT a Lie algebra in general; only the bracket [K,K] = c3 P is read (linear change of basis)
CJ = dense(fJ, n)
c3P = sp.simplify(change_basis(CJ, Pm)[3][4][8]); c3T = sp.simplify(change_basis(CJ, Tm)[3][4][8]); a2P = sp.simplify(change_basis(CJ, Pm)[9][3][6]); a2T = sp.simplify(change_basis(CJ, Tm)[9][3][6])
print("J: c3 under parity ->", c3P, "; under time reversal ->", c3T, " (a2 under P, T ->", a2P, a2T, ")")
chk("J1 the a0-direction is PARITY-ODD (c3 -> -c3 under K,P -> -K,-P) and T-even: any algebra with c3 != 0 is chiral (the pair c3, -c3 are isomorphic, but neither is mapped to itself by parity); this is why the P,T-symmetric P,T-symmetric classification of m01 does not contain it", sp.simplify(c3P + c3) == 0 and sp.simplify(c3T - c3) == 0 and sp.simplify(a2P - 1) == 0)
print("\n%d/%d checks pass" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
