"""m01: Jacobi identities of the general rotation-covariant kinematical algebra (J,K,P,H), and what they force.

Question (lane M, task 1): in the algebras where BOTH Lambda-type and c-type deformations of Galilei appear, which relations among the
deformation parameters are FORCED by Jacobi, which are free, and can the MAGNITUDE of a ratio of two dimensionful structure constants be an
invariant of the algebra?  (If not, a0/H can never be 'fixed by closure': it can only be a convention or a property of a realisation.)

 A  the 16-parameter rotation-covariant ansatz; its Jacobi identities as polynomials (distinct ones counted).
 B  the parity+time-reversal slice: exact solution (c1 = a2 h1, d1 = -b1 h1); nothing else; free parameters = 3 (a2,b1,h1).
 C  the rescaling group K->aK, P->bP, H->gH acts on (a2,b1,h1) with weights that are LINEARLY INDEPENDENT (det = -4): no non-constant monomial
    (hence no nonconstant rational function) of the structure constants is invariant: only SIGNS and zero/non-zero survive -> the nine
    P,T-symmetric algebras; every ratio of two dimensionful structure constants is a unit convention.
 D  the nine sign classes, labelled by the Killing-form signature of the (J,K) block and checked to satisfy Jacobi; controls / mutations that must fail.
 E  dimensions of the structure constants (M,L,T) computed from generator dimensions: exactly three independent dimensionful scales
    (1/tau^2, 1/c^2, 1/R^2 = product) -- Jacobi ties the third to the other two (the 'forced relation'); an acceleration a0 = L T^-2 is
    NOT a monomial and only appears as a0 = nu * sqrt(b1/c1) with nu an unconstrained dimensionless number.
"""
import sympy as sp, numpy as np, itertools, sys
from m_tools import *
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ---------------- A: general ansatz -------------
names14 = 'a1 a2 a3 b1 b2 b3 c1 c2 c3 d1 d2 d3 h1 e2 e3 e4'.split()
S = sp.symbols(names14); par = dict(zip(names14, S))
f, n = rot_ansatz(par, with_D=False)
polys = jacobi_polys(f, n)
print("A: distinct Jacobi polynomials in the 16 structure constants:", len(polys))
chk("A1 the rotation-covariant ansatz on (J,K,P,H) has exactly 16 free structure constants (14 + the two J-components of [H,K],[H,P]) and 20 distinct Jacobi polynomials", len(names14) == 16 and len(polys) == 20)
# rotation part is consistent: with all 14 = 0 the algebra (semidirect so(3) x abelian) is Lie
f0, _ = rot_ansatz({}, with_D=False)
chk("A2 zero deformation (so(3) acting on abelian K,P,H) satisfies Jacobi", is_lie(f0, n))

# ---------------- B: P,T slice -------------
a2, b1, c1, d1, h1 = sp.symbols('a2 b1 c1 d1 h1')
parB = {'a2': a2, 'b1': b1, 'c1': c1, 'd1': d1, 'h1': h1}
fB, _ = rot_ansatz(parB, with_D=False)
pB = jacobi_polys(fB, n)
print("B: Jacobi polynomials on the P,T slice:", pB)
sol = sp.solve(pB, [c1, d1], dict=True)
print("   solution for (c1,d1):", sol)
chk("B1 P,T slice: Jacobi <=> c1 = a2*h1 and d1 = -b1*h1 (a2,b1,h1 free)", sol == [{c1: a2 * h1, d1: -b1 * h1}])
fBs, _ = rot_ansatz({'a2': a2, 'b1': b1, 'c1': a2 * h1, 'd1': -b1 * h1, 'h1': h1}, with_D=False)
chk("B2 the 3-parameter family satisfies ALL 20 general Jacobi polynomials symbolically", is_lie(fBs, n))
# mutations
chk("B3 MUTATION c1 -> 2 a2 h1 breaks Jacobi", not is_lie(rot_ansatz({'a2': 1, 'b1': 1, 'c1': 2, 'd1': -1, 'h1': 1}, False)[0], n))
chk("B4 MUTATION d1 -> +b1 h1 (sign) breaks Jacobi", not is_lie(rot_ansatz({'a2': 1, 'b1': 1, 'c1': 1, 'd1': +1, 'h1': 1}, False)[0], n))
chk("B5 MUTATION drop the [K,P]=H term but keep c1,d1 != 0 breaks Jacobi", not is_lie(rot_ansatz({'a2': 1, 'b1': 1, 'c1': 1, 'd1': -1, 'h1': 0}, False)[0], n))

# ---------------- C: rescaling weights -------------
al, be, ga = sp.symbols('alpha beta gamma', positive=True)
# K'=al K, P'=be P, H'=ga H:  a2' = ga al/be a2 ; b1' = ga be/al b1 ; h1' = al be/ga h1
# verify by brute force on the tensor: transform basis and re-read the constants
def rescale(fpar):
    fr, _ = rot_ansatz(fpar, with_D=False)
    scale = [1, 1, 1, al, al, al, be, be, be, ga]
    out = {}
    for (a, b), v in fr.items():
        for e, c in v.items():
            out.setdefault((a, b), {})[e] = sp.simplify(c * scale[a] * scale[b] / scale[e])
    return out
fr = rescale({'a2': a2, 'b1': b1, 'h1': h1, 'c1': a2 * h1, 'd1': -b1 * h1})
newa2 = -fr[(3, 9)][6]; newb1 = -fr[(6, 9)][3]; newh1 = fr[(3, 6)][9]   # stored as [K,H],[P,H] with a<b
chk("C1 weights: a2'=ga*al/be*a2, b1'=ga*be/al*b1, h1'=al*be/ga*h1 (read off the rescaled tensor)",
    sp.simplify(newa2 - ga * al / be * a2) == 0 and sp.simplify(newb1 - ga * be / al * b1) == 0 and sp.simplify(newh1 - al * be / ga * h1) == 0)
W = sp.Matrix([[1, -1, 1], [-1, 1, 1], [1, 1, -1]])   # exponent rows of (al,be,ga) for (a2,b1,h1)
chk("C2 the three weight vectors are linearly independent (det W = -4): NO nonconstant monomial in (a2,b1,h1) is rescaling-invariant", W.det() == -4)
# invariant monomials a2^i b1^j h1^k : W^T (i,j,k) = 0 -> only zero
ns = W.T.nullspace()
chk("C3 integer relations among the weights: none (nullspace empty) -> the ring of rescaling-invariant monomials is the constants", len(ns) == 0)
# control: if a2 were NOT a free dimensionless constant (e.g. fixed a2 = 1 by convention) the residual group is 2-dim on (b1,h1): still no invariants
# with a2 pinned to 1 the residual rescalings obey be = ga*al; read the transformed constants off the substituted weights
b1p = sp.simplify((ga * be / al).subs(be, ga * al)); h1p = sp.simplify((al * be / ga).subs(be, ga * al))
chk("C4 control: pinning a2 = 1 (physical K=tP-mx convention) leaves a 2-parameter rescaling group (al,ga) acting as b1 -> ga^2 b1, h1 -> al^2 h1: still no invariant magnitude",
    sp.simplify(b1p - ga ** 2) == 0 and sp.simplify(h1p - al ** 2) == 0)
# consequence: b1/h1 -> (ga/al)^2 b1/h1 : any ratio of the two dimensionful constants is a convention
ratio = sp.simplify(newb1 / newh1 - (ga / al) ** 2 * b1 / h1)
chk("C5 ratio b1/h1 rescales as (ga/al)^2: its MAGNITUDE is a unit convention, only its sign is an invariant", ratio == 0)

# ---------------- D: nine sign classes -------------
def killing_sig(fpar):
    fr, nn = rot_ansatz(fpar, with_D=False)
    ad = [np.zeros((nn, nn)) for _ in range(nn)]
    for a in range(nn):
        for b in range(nn):
            for e, c in br(fr, a, b).items(): ad[a][e, b] = float(c)
    Bk = np.array([[np.trace(ad[a] @ ad[b]) for b in range(nn)] for a in range(nn)])
    lor = list(range(6))
    ev = np.linalg.eigvalsh(Bk[np.ix_(lor, lor)])
    return int((ev < -1e-9).sum()), int((ev > 1e-9).sum())
classes = {}
allj = True
for st in (-1, 0, 1):
    for sc in (-1, 0, 1):
        # a2 = 1 (convention), b1 = st, h1 = sc  -> c1 = sc, d1 = -st*sc
        p = {'a2': 1, 'b1': st, 'h1': sc, 'c1': sc, 'd1': -st * sc}
        lie = is_lie(rot_ansatz(p, False)[0], n)
        allj &= lie
        classes[(st, sc)] = killing_sig(p)
chk("D1 all nine sign classes (sign(b1), sign(h1)) in {-,0,+}^2 satisfy Jacobi", allj)
print("   Killing-form signature (neg,pos) of the (J,K) block per (sign b1, sign h1):", classes)
# Lorentz-type algebras have (3,3), Euclidean-type (6,0), degenerate (Galilei/Carroll like) contain zero eigenvalues
chk("D2 h1 = -1 and h1 = +1 give a Lorentz (3,3) and a Euclidean (6,0) rotation block respectively (which sign is which is convention-free)",
    {classes[(0, -1)], classes[(0, 1)]} == {(3, 3), (6, 0)})
chk("D3 h1 = 0 gives a degenerate (J,K) Killing block ((3,0)): Galilei / Newton-Hooke / Carroll-like",
    all(classes[(s, 0)] == (3, 0) for s in (-1, 0, 1)))
# expansion sign: NH_+ vs NH_-: eigenvalues of ad_H on span(K,P): +-sqrt(a2*b1): real for b1>0, imaginary for b1<0
def adH_eigs(b1v):
    fr, nn = rot_ansatz({'a2': 1, 'b1': b1v, 'h1': 0, 'c1': 0, 'd1': 0}, with_D=False)
    M = np.zeros((2, 2))   # ad_H on (K1,P1): H,K1 = a2 P1 ; H,P1 = b1 K1
    for j, src in enumerate((3, 6)):
        for e, c in br(fr, 9, src).items():
            if e in (3, 6): M[e // 3 - 1, j] = float(c)
    return np.linalg.eigvals(M)
ev_p, ev_m = adH_eigs(1), adH_eigs(-1)
chk("D4 sign(a2*b1) is the invariant: ad_H on span(K,P) has REAL eigenvalues +-sqrt(a2 b1) (expanding NH) for a2 b1>0 and IMAGINARY (oscillating NH) for a2 b1<0",
    np.allclose(ev_p.imag, 0) and np.allclose(ev_m.real, 0) and abs(abs(ev_p[0]) - 1) < 1e-12)

# ---------------- E: dimensions of the structure constants -------------
# generator dimension vectors (M,L,T): J=A action, K=ML, P=ML/T, H=ML^2/T^2; bracket = Poisson bracket -> [X,Y] has dim XY/A
dimJ = sp.Matrix([1, 2, -1]); dimK = sp.Matrix([1, 1, 0]); dimP = sp.Matrix([1, 1, -1]); dimH = sp.Matrix([1, 2, -2])
def cdim(x, y, z): return x + y - dimJ - z   # dim of the coefficient c in [X,Y]=c Z
table = {'a2 ([H,K]=a2 P)': cdim(dimH, dimK, dimP), 'a1 ([H,K]=a1 K)': cdim(dimH, dimK, dimK),
         'b1 ([H,P]=b1 K)': cdim(dimH, dimP, dimK), 'b2 ([H,P]=b2 P)': cdim(dimH, dimP, dimP),
         'c1 ([K,K]=c1 J)': cdim(dimK, dimK, dimJ), 'd1 ([P,P]=d1 J)': cdim(dimP, dimP, dimJ), 'h1 ([K,P]=h1 H)': cdim(dimK, dimP, dimH)}
LT = {k: (int(v[1]), int(v[2])) for k, v in table.items()}
print("E: (L-exponent, T-exponent) of each structure constant:", LT)
chk("E1 mass exponent cancels in every structure constant (they are pure L,T quantities)", all(int(v[0]) == 0 for v in table.values()))
chk("E2 b1 ~ T^-2 (time curvature 1/tau^2), c1 ~ h1 ~ T^2 L^-2 (1/c^2), d1 ~ L^-2 (spatial curvature 1/R^2)",
    LT['b1 ([H,P]=b1 K)'] == (0, -2) and LT['c1 ([K,K]=c1 J)'] == (-2, 2) and LT['h1 ([K,P]=h1 H)'] == (-2, 2) and LT['d1 ([P,P]=d1 J)'] == (-2, 0))
chk("E3 the FORCED relation d1 = -b1 h1 is dimensionally consistent (L^-2 = T^-2 * T^2 L^-2) : spatial curvature = (time curvature)/c^2 (Jacobi ties it)",
    LT['d1 ([P,P]=d1 J)'] == (LT['b1 ([H,P]=b1 K)'][0] + LT['h1 ([K,P]=h1 H)'][0], LT['b1 ([H,P]=b1 K)'][1] + LT['h1 ([K,P]=h1 H)'][1]))
# a0 = L T^-2: solve a0 = b1^x c1^y (real exponents)
x, y = sp.symbols('x y')
solx = sp.solve([-2 * y - 1, -2 * x + 2 * y + 2], [x, y], dict=True)
print("   a0 = L T^-2 as a real power of (b1, c1):", solx)
chk("E4 a0 (L T^-2) is NOT an integer monomial of the structure constants (needs half-integer powers): a0 = nu * sqrt(b1/c1) = nu * c * H with nu dimensionless",
    solx == [{x: sp.Rational(1, 2), y: sp.Rational(-1, 2)}])
print("   note: the only place a dimensionless number nu could live is a2 (and the other dimensionless constants); C1-C5 show a2 is a normalisation of P against K, i.e. a convention")
print("\n%d/%d checks pass" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
