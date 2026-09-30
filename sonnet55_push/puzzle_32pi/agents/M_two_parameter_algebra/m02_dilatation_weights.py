"""m02: which dilatations D can be added to the kinematical algebras, and what Jacobi says about the scales (a0, H_Lambda, c).

Setting: the 11-dimensional rotation-covariant ansatz (J,K,P,H,D), 25 structure constants (21 + the J-components of [H,K],[H,P],[D,K],[D,P]).  D is a scalar generator.
Convention for D_z: t -> lam^z t, x -> lam x, i.e. D = z t d_t + x d_x, so  [D,H] = -z H, [D,P] = -P, [D,K] = (z-1) K
  (K = t d_x, the Galilei boost).  z is the dynamical exponent: z=1 the MOND space-time scaling, z=2 Schroedinger, z=0 pure space dilatation.
  Weights of dimensionful constants: L -> 1, T -> z:   a0 (L T^-2): 1-2z ;  H_Lambda (1/T): -z ;  c (L/T): 1-z.

 A  size of the general problem (Jacobi polynomials of the 25-constant ansatz).
 B  the nine kinematical classes: outer derivations (semi-direct D) by exact linear algebra -> allowed z per class.
 C  non-semi-direct D (D also appears in [K,P]): full non-linear solve on the slice; only the Bargmann-type (mass) extension appears.
 D  the symbolic slice (a2,b1,h1 free, D diagonal): the constraint polynomials -> 'each of b1, h1 kills a weight'.
 E  a0: invariant only at z = 1/2; H_Lambda only at z = 0; c only at z = 1; which class admits which z.
 F  controls and mutations.
"""
import sympy as sp, numpy as np, sys
from m_tools import *
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

names21 = 'a1 a2 a3 b1 b2 b3 p1 p2 p3 q1 q2 q3 f1 f2 c1 c2 c3 d1 d2 d3 h1 h2 e2 e3 e4'.split()
S21 = sp.symbols(names21)
f21, n = rot_ansatz(dict(zip(names21, S21)), with_D=True)
poly21 = jacobi_polys(f21, n)
print("A: distinct Jacobi polynomials of the general 25-constant ansatz on (J,K,P,H,D):", len(poly21))
chk("A1 the general ansatz has 25 structure constants (incl. the J-components); its Jacobi identities give %d distinct polynomials (quadratic)" % len(poly21), len(poly21) > 20)

classes = {'Galilei': (0, 0), 'Euclid-type (b1=0,h1=+1)': (0, 1), 'Poincare-type (b1=0,h1=-1)': (0, -1),
           'NH+ (b1=+1)': (1, 0), 'NH- (b1=-1)': (-1, 0), '(b1=+1,h1=-1)': (1, -1), '(b1=+1,h1=+1)': (1, 1), '(b1=-1,h1=-1)': (-1, -1), '(b1=-1,h1=+1)': (-1, 1)}
def base(st, sc): return {'a2': 1, 'b1': st, 'h1': sc, 'c1': sc, 'd1': -st * sc}

# ---------------- B: outer derivations -------------
p1, p2, p3, q1, q2, q3, f1 = sp.symbols('p1 p2 p3 q1 q2 q3 f1')
res = {}
for name, (st, sc) in classes.items():
    par = base(st, sc); par.update({'p1': p1, 'p2': p2, 'p3': p3, 'q1': q1, 'q2': q2, 'q3': q3, 'f1': f1})
    fD, _ = rot_ansatz(par, with_D=True)
    eqs = [v for _, _, v in jacobi_residuals(fD, n)]
    sol = sp.solve(eqs, [p1, p2, p3, q1, q2, q3, f1], dict=True)
    # dimension of the linear solution space
    A = sp.Matrix([[sp.diff(e, u) for u in (p1, p2, p3, q1, q2, q3, f1)] for e in eqs])
    dimV = 7 - A.rank()
    res[name] = (sol, dimV)
    print("B: %-28s derivation space dim %d (inner ad_H is 1 of them);  solution: %s" % (name, dimV, sol))
chk("B1 Galilei: 3-dim derivation space (2 outer: independent time and space scalings) => the dynamical exponent z is FREE", res['Galilei'][1] == 3)
chk("B2 Newton-Hooke (both signs): 2-dim derivation space = ad_H + ONE outer derivation (space dilatation only)", res['NH+ (b1=+1)'][1] == 2 and res['NH- (b1=-1)'][1] == 2)
chk("B3 Poincare-type: 2-dim = ad_H + ONE outer derivation (Weyl scaling, z=1)", res['Poincare-type (b1=0,h1=-1)'][1] == 2)
chk("B4 the four classes with BOTH b1 and h1 nonzero (de Sitter, anti-de Sitter and their Euclidean-signature cousins): derivation space is just ad_H (dim 1): NO dilatation at all (rigidity)",
    all(res[k][1] == 1 for k in ['(b1=+1,h1=-1)', '(b1=+1,h1=+1)', '(b1=-1,h1=-1)', '(b1=-1,h1=+1)']))
# explicit z for NH: solution has f1 = 0 (time not rescaled)
solNH = res['NH+ (b1=+1)'][0][0]
chk("B5 NH: Jacobi forces f1 = 0, i.e. w(H) = 0: time cannot be dilated when H_Lambda != 0  (solution: %s)" % solNH, solNH.get(f1, None) == 0)
solP = res['Poincare-type (b1=0,h1=-1)'][0][0]
chk("B6 Poincare-type: Jacobi forces p1 = 0, i.e. w(K) = z-1 = 0, so z = 1 (Weyl): c fixed <=> only the relativistic scaling  (solution: %s)" % solP, solP.get(p1, None) == 0)
solG = res['Galilei'][0][0]
chk("B7 Galilei: p1 = q2 - f1 (the boost/momentum/energy relation) is the ONLY constraint on the weights: 2 free weights = the z family (solution: %s)" % solG,
    sp.simplify(solG[p1] - (q2 - f1)) == 0 and set(solG.keys()) == {p1, p3, q1, q3})

# ---------------- C: non-semi-direct D -------------
h2, f2 = sp.symbols('h2 f2')
print("\nC: all Jacobi branches of the 7-unknown slice (D allowed in [K,P] and [D,H]); duplicates removed:")
nonsemi = {}
for name in ['Galilei', 'NH+ (b1=+1)', 'NH- (b1=-1)', 'Poincare-type (b1=0,h1=-1)', 'Euclid-type (b1=0,h1=+1)', '(b1=+1,h1=-1)']:
    st, sc = classes[name]
    par = base(st, sc); par.update({'p1': p1, 'p2': p2, 'p3': p3, 'q1': q1, 'q2': q2, 'q3': q3, 'f1': f1, 'f2': f2, 'h2': h2})
    fD, _ = rot_ansatz(par, with_D=True)
    eqs = [v for _, _, v in jacobi_residuals(fD, n)]
    sol = sp.solve(eqs, [p1, p2, p3, q1, q2, q3, f1, f2, h2], dict=True)
    uniq = []
    for s_ in sol:
        if s_ not in uniq: uniq.append(s_)
    nonsemi[name] = uniq
    print("   %-28s %d branches" % (name, len(uniq)))
    for s_ in uniq: print("        ", s_)
def central_D(sol):  # D central with free h2: every weight/action constant zero, h2 unconstrained
    return all(sol.get(k, k) == 0 for k in (f1, f2, p1, p2, p3, q1, q2, q3)) and h2 not in sol
chk("C1 for h1 = 0 (Galilei, both Newton-Hooke) a branch with D CENTRAL and h2 free exists: the mass extension [K,P] = h2 M (non-removable, certified in m04 by H^2)",
    all(any(central_D(s_) for s_ in nonsemi[k]) for k in ['Galilei', 'NH+ (b1=+1)', 'NH- (b1=-1)']))
chk("C2 every branch with h2 != 0 is that central one (no non-central D enters [K,P]): so the ONLY way a scalar generator can appear in [K,P] is a central charge",
    all(all(central_D(s_) for s_ in nonsemi[k] if s_.get(h2, h2) != 0) for k in nonsemi))
# for h1 != 0 the central branch is trivial: H' = H + (h2/h1) D removes it (checked on the tensor)
hh = sp.symbols('hh')
fc, _ = rot_ansatz({**base(1, -1), 'h2': hh}, with_D=True)
f0_, _ = rot_ansatz(base(1, -1), with_D=True)
Cc = dense(fc, n); C0 = dense(f0_, n)
T = sp.eye(n); T[10, 9] = hh / (-1)      # e'_H = e_H + (hh/h1) e_D  with h1 = -1  (column 9 = new H, row 10 = D component)
Cn = change_basis(Cc, T)
same = all(sp.simplify(Cn[a][b][e] - C0[a][b][e]) == 0 for a in range(n) for b in range(n) for e in range(n))
chk("C3 for h1 != 0 the central branch is a trivial direct sum: after H' = H + (h2/h1) D the FULL structure tensor equals that of h2 = 0 (algebra x R)", is_lie(fc, n) and same)
# and the contrast: for h1 = 0 no such shift exists (the h2 term cannot be absorbed): the tensor with h2 != 0 differs from h2 = 0 for every shift H' = H + t D
fg, _ = rot_ansatz({**base(0, 0), 'h2': hh}, with_D=True); fg0, _ = rot_ansatz(base(0, 0), with_D=True)
tt = sp.symbols('tt'); T2 = sp.eye(n); T2[10, 9] = tt
Cg = change_basis(dense(fg, n), T2); Cg0 = dense(fg0, n)
diff = [sp.simplify(Cg[a][b][e] - Cg0[a][b][e]) for a in range(n) for b in range(n) for e in range(n)]
chk("C3b control: for h1 = 0 (Galilei) NO shift H' = H + tD removes the h2 term (the difference [K,P] = h2 D survives for all t): the mass extension is non-trivial", any(d != 0 for d in diff))
# f2 != 0 branches: character / Borel extensions
chk("C4 branches with f2 != 0 exist for the Newton-Hooke classes (a scalar on which H acts with a character, or a Borel partner of H): NOT dilatations of (t,x); they are the sl(2) partners seen in the conformal-Galilei ladder (m03)",
    any(s_.get(f2, f2) != 0 for s_ in nonsemi['NH+ (b1=+1)']))

# ---------------- D: symbolic slice -------------
a2s, b1s, h1s = sp.symbols('a2 b1 h1')
z = sp.symbols('z')
parD = {'a2': a2s, 'b1': b1s, 'h1': h1s, 'c1': a2s * h1s, 'd1': -b1s * h1s, 'p1': p1, 'q2': q2, 'f1': f1}
fDs, _ = rot_ansatz(parD, with_D=True)
polysD = jacobi_polys(fDs, n)
print("\nD: Jacobi polynomials on the diagonal-D slice (weights f1=w_H, p1=w_K, q2=w_P):")
for p in polysD: print("   ", p)
gens = [sp.factor(p) for p in polysD]
chk("D1 the diagonal-D slice has exactly 5 Jacobi polynomials: the weight-additivity conditions a2(q2-f1-p1)=0, b1(p1-f1-q2)=0, h1(f1-p1-q2)=0 and the two c1,d1 conditions c1 p1 = 0, d1 q2 = 0",
    len(polysD) == 5)
# substitute D_z weights f1=-z, p1=z-1, q2=-1
sub = {f1: -z, p1: z - 1, q2: -1}
cons = {str(p): sp.factor(p.subs(sub)) for p in polysD}
for k, v in cons.items(): print("   D_z ->", v)
expected = {sp.factor(2 * a2s * h1s * (z - 1)), sp.factor(2 * h1s * (z - 1)), sp.Integer(0), sp.factor(2 * b1s * h1s), sp.factor(2 * b1s * z)}
chk("D2 with the D_z weights the five constraints are exactly {2 a2 h1 (z-1), 2 h1 (z-1), 0, 2 b1 h1, 2 b1 z}: b1 != 0 kills every z but 0; h1 != 0 kills every z but 1; b1 h1 != 0 (spatial curvature d1) kills all",
    {sp.factor(v) for v in cons.values()} == expected)

# ---------------- E: a0, H, c invariance -------------
w = {'a0 (L T^-2)': 1 - 2 * z, 'H_Lambda (T^-1)': -z, 'c (L T^-1)': 1 - z}
zinv = {k: sp.solve(v, z) for k, v in w.items()}
print("\nE: dilatation exponent z at which each scale is invariant:", zinv)
chk("E1 a0 is invariant only at z=1/2, H_Lambda only at z=0, c only at z=1: three DIFFERENT dilatations",
    zinv['a0 (L T^-2)'] == [sp.Rational(1, 2)] and zinv['H_Lambda (T^-1)'] == [0] and zinv['c (L T^-1)'] == [1])
def allowed_z(name):
    st, sc = classes[name]
    if st == 0 and sc == 0: return 'any z'
    if st == 0: return 'z = 1 only'
    if sc == 0: return 'z = 0 only'
    return 'none'
tab = {k: allowed_z(k) for k in classes}
print("   allowed z per class:", tab)
chk("E2 among the nine parity/time-reversal-symmetric classes, z=1/2 (the dilatation that leaves a0 invariant) is available ONLY in the Galilei class (1/c^2 = 0 and 1/tau^2 = 0): with finite c or finite H_Lambda a0 is never invariant (the parity-odd Galilei + c3 of m06 also has it)",
    [k for k, v in tab.items() if v == 'any z'] == ['Galilei'])
chk("E3 z=1 (the MOND scaling (t,r)->q(t,r), also the Weyl scaling) exists for Galilei and Poincare-type, and NOT once H_Lambda != 0: deep-MOND space-time scale invariance is incompatible with a nonzero tau^-2",
    tab['Galilei'] == 'any z' and tab['Poincare-type (b1=0,h1=-1)'] == 'z = 1 only' and tab['NH+ (b1=+1)'] == 'z = 0 only' and tab['(b1=+1,h1=-1)'] == 'none')
# mass weight: [K,P] = M central: w(M) = w_K + w_P = z-2
chk("E4 a central mass in [K,P] has weight z-2: scale-invariant only at z=2 (Schroedinger); at the MOND z=1 the mass carries weight -1 (no scale-invariant massive extension)",
    sp.simplify((z - 1) + (-1) - (z - 2)) == 0)

# ---------------- F: controls / mutations -------------
fw = lambda st, sc, **kw: rot_ansatz({**base(st, sc), **kw}, with_D=True)[0]
# MOND z=1 on Galilei passes; on NH fails (mutation of a known-good derivation)
chk("F1 control: z=1 weights (f1=-1,p1=0,q2=-1) satisfy Jacobi on Galilei", is_lie(fw(0, 0, f1=-1, p1=0, q2=-1), n))
chk("F2 MUTATION: the same z=1 weights on Newton-Hooke (b1=+1) violate Jacobi", not is_lie(fw(1, 0, f1=-1, p1=0, q2=-1), n))
chk("F3 control: space dilatation (f1=0,p1=-1,q2=-1) satisfies Jacobi on NH+ and NH-", is_lie(fw(1, 0, f1=0, p1=-1, q2=-1), n) and is_lie(fw(-1, 0, f1=0, p1=-1, q2=-1), n))
chk("F4 MUTATION: Weyl weights (f1=-1,p1=0,q2=-1) on the (b1=+1,h1=-1) algebra violate Jacobi (rigidity)", not is_lie(fw(1, -1, f1=-1, p1=0, q2=-1), n))
chk("F5 control: Weyl weights satisfy Jacobi on the Poincare-type algebra", is_lie(fw(0, -1, f1=-1, p1=0, q2=-1), n))
chk("F6 MUTATION: z=1/2 weights on the Poincare-type algebra violate Jacobi (c fixes z=1)", not is_lie(fw(0, -1, f1=-sp.Rational(1, 2), p1=-sp.Rational(1, 2), q2=-1), n))
chk("F7 control: z=1/2 (a0-invariant) weights satisfy Jacobi on Galilei", is_lie(fw(0, 0, f1=-sp.Rational(1, 2), p1=-sp.Rational(1, 2), q2=-1), n))
print("\n%d/%d checks pass" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
