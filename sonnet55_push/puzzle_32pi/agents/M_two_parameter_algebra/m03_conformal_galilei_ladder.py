"""m03: the conformal-Galilei ladder cg_l(3) (l = 1/2 Schroedinger, l = 1 GCA / the MOND z=1, l = 3/2, 2 ...): where dilatation, Newton-Hooke and quantised integers live.

Vector fields on (t, x1,x2,x3):  H = d_t,  D = t d_t + l x.d,  C = t^2 d_t + 2 l t x.d,  P^(n)_i = t^n d_i (n = 0..2l),  J_ij rotations.
Dynamical exponent of D:  x ~ t^l, i.e. z = 1/l = 2/N with N = 2l  (N=1: z=2 Schroedinger; N=2: z=1 = the MOND scaling (t,r)->q(t,r); N=4: z=1/2 = the scaling that leaves an ACCELERATION invariant).

 A  closure and dimensions (12, 15, 18, 21); controls: non-integer 2l and a wrong C-coefficient break closure.
 B  the sl(2) = {H,D,C}: [D,H] = -H, [C,H] = -2D, [D,C] = C.  ad_D eigenvalues on the multiplet = n - l  (weights -l..l).
 C  Newton-Hooke inside: for l = 1/2 the elliptic H + w^2 C (oscillating NH) and hyperbolic H - w^2 C (expanding NH) with the (J,P,K) block close into the 10-dimensional NH algebras;
    spectrum of ad(H +- w^2 C) on the multiplet = (2 m) w  with m = -l..l  (times i for the elliptic one): the top frequency is N w -- an INTEGER multiple of the sl(2) unit w.
 D  the magnitude w is a unit: D-conjugation maps H + w^2 C to (scale) x (H + w'^2 C): all w are conjugate; the integer N is not.
 E  a pair of hyperbolic elements (the MOND dilatation D and the Lambda time-translation H - w^2 C) inside ONE sl(2): their relative rapidity is a free continuous modulus.
"""
import sympy as sp, numpy as np, itertools, sys
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)
t = sp.Symbol('t'); X = sp.symbols('x1 x2 x3'); coords = (t,) + X

def vf_bracket(A, B):
    return [sp.expand(sum(A[v] * sp.diff(B[m], coords[v]) - B[v] * sp.diff(A[m], coords[v]) for v in range(4))) for m in range(4)]

def build(l, cH=1, cC=None, nmax=None):
    l = sp.Rational(l)
    if cC is None: cC = 2 * l
    if nmax is None: nmax = int(2 * l)
    gens = {}
    gens['H'] = [sp.Integer(1), 0, 0, 0]
    gens['D'] = [t] + [l * x for x in X]
    gens['C'] = [t ** 2] + [cC * t * x for x in X]
    for n in range(nmax + 1):
        for i in range(3):
            gens['P%d_%d' % (n, i + 1)] = [0] + [t ** n if j == i else 0 for j in range(3)]
    for (i, j) in [(0, 1), (0, 2), (1, 2)]:
        gens['J%d%d' % (i + 1, j + 1)] = [0] + [(X[i] if k == j else 0) - (X[j] if k == i else 0) for k in range(3)]
    return gens

def decompose(field, gens):
    names = list(gens)
    cs = sp.symbols('c0:%d' % len(names))
    eqs = []
    for m in range(4):
        expr = sp.expand(field[m] - sum(cs[a] * gens[nm][m] for a, nm in enumerate(names)))
        if expr != 0: eqs += sp.Poly(expr, *coords).coeffs()
    if not eqs: return {nm: 0 for nm in names}
    sol = sp.solve(eqs, cs, dict=True)
    if not sol: return None
    return {nm: sol[0].get(cs[a], cs[a]) for a, nm in enumerate(names)}

def structure(gens):
    names = list(gens); f = {}
    closed = True
    for a in range(len(names)):
        for b in range(a + 1, len(names)):
            d = decompose(vf_bracket(gens[names[a]], gens[names[b]]), gens)
            if d is None: closed = False; continue
            f[(names[a], names[b])] = {k: v for k, v in d.items() if v != 0}
    return f, closed

ladder = {}
for l in (sp.Rational(1, 2), 1, sp.Rational(3, 2), 2):
    g = build(l); f, closed = structure(g)
    ladder[l] = (g, f, closed)
    dim = len(g)
    print("l = %s  N = %s  z = %s   dim = %d   closed under [,] : %s" % (l, 2 * l, 1 / l, dim, closed))
chk("A1 closure: cg_l(3) closes for l = 1/2, 1, 3/2, 2 with dimensions 12, 15, 18, 21",
    all(ladder[l][2] for l in ladder) and [len(ladder[l][0]) for l in ladder] == [12, 15, 18, 21])
chk("A2 dimension of l = 1 equals dim so(4,2) = 15 (the Galilean conformal algebra is a contraction of the relativistic conformal algebra, same dimension)", len(ladder[1][0]) == 15)
# controls
g_bad = build(sp.Rational(1, 2), cC=sp.Rational(3, 2)); _, closed_bad = structure(g_bad)
chk("A3 MUTATION: C with the wrong coefficient (3/2 instead of 2l = 1 at l=1/2) does not close", not closed_bad)
g_frac = build(sp.Rational(1, 3), nmax=1); _, closed_frac = structure(g_frac)
chk("A4 MUTATION: non-integer 2l (l = 1/3 with a truncated multiplet n=0..1) does not close: finite-dimensional cg_l needs 2l = N integer", not closed_frac)

# B: sl(2) and ad_D weights
def get(f, a, b, names):
    if (a, b) in f: return f[(a, b)]
    if (b, a) in f: return {k: -v for k, v in f[(b, a)].items()}
    return {}
allB = True; okW = True
for l, (g, f, closed) in ladder.items():
    allB &= (get(f, 'D', 'H', g) == {'H': -1} and get(f, 'C', 'H', g) == {'D': -2} and get(f, 'D', 'C', g) == {'C': 1})
    for n in range(int(2 * l) + 1):
        d_ = get(f, 'D', 'P%d_1' % n, g)
        okW &= (d_.get('P%d_1' % n, 0) == n - l and all(k == 'P%d_1' % n for k in d_))
chk("B1 sl(2) relations [D,H] = -H, [C,H] = -2D, [D,C] = C hold at every level", allB)
chk("B2 ad_D eigenvalue on P^(n) is n - l at every level: the weights are -l..l in integer steps", okW)

# C: NH inside l = 1/2 ; spectrum of H +- w^2 C on the multiplet
w = sp.Symbol('w', positive=True)
def adspec(l, sign):
    g, f, _ = ladder[l]
    names = ['P%d_1' % n for n in range(int(2 * l) + 1)]
    M = sp.zeros(len(names), len(names))
    for j, nm in enumerate(names):
        for a_, fac in (('H', 1), ('C', sign * w ** 2)):
            for k, v in get(f, a_, nm, g).items():
                if k in names: M[names.index(k), j] += fac * v
    return M, sorted(M.eigenvals().keys(), key=lambda e: sp.re(sp.N(e.subs(w, 1))) + 1e-3 * sp.im(sp.N(e.subs(w, 1))))
res_spec = {}
for l in ladder:
    for sgn, lab in ((+1, 'elliptic H + w^2 C'), (-1, 'hyperbolic H - w^2 C')):
        M, ev = adspec(l, sgn)
        res_spec[(l, sgn)] = [sp.simplify(e) for e in ev]
        print("l = %s  %s :  eigenvalues of ad on the multiplet = %s" % (l, lab, res_spec[(l, sgn)]))
def expected(l, sgn):
    m = [sp.Rational(k, 1) - l for k in range(int(2 * l) + 1)]
    return sorted([sp.simplify(2 * mm * w * (sp.I if sgn > 0 else 1)) for mm in m], key=lambda e: sp.N(sp.re(e.subs(w, 1)) + 1e-3 * sp.im(e.subs(w, 1))))
chk("C1 spectrum of ad(H + w^2 C) [oscillating] on the multiplet is 2 m w i, m = -l..l ; of ad(H - w^2 C) [expanding] is 2 m w",
    all(sorted([sp.simplify(e) for e in res_spec[(l, s)]], key=lambda e: sp.N(sp.re(e.subs(w, 1)) + 1e-3 * sp.im(e.subs(w, 1)))) ==
        expected(l, s) for l in ladder for s in (+1, -1)))
chk("C2 the top frequency of the multiplet is N w = 2l w : an INTEGER multiple of the sl(2) unit w  (N = 1, 2, 3, 4)",
    all(sp.simplify(max([sp.Abs(e) for e in res_spec[(l, 1)]]) - 2 * l * w) == 0 for l in ladder))
# NH inside l=1/2:  (J, P^(0), P^(1), H + s w^2 C) closes and has [H_s, P0] , [H_s, P1]
g12, f12, _ = ladder[sp.Rational(1, 2)]
for sgn in (1, -1):
    # e = H + sgn w^2 C acting on P0, P1 (component 1)
    def ade(nm):
        d = {}
        for a_, fac in (('H', 1), ('C', sgn * w ** 2)):
            for k, v in get(f12, a_, nm, g12).items(): d[k] = d.get(k, 0) + fac * v
        return {k: sp.simplify(v) for k, v in d.items() if sp.simplify(v) != 0}
    d0, d1 = ade('P0_1'), ade('P1_1')
    print("l = 1/2, e = H %s w^2 C:   [e,P0] = %s ;  [e,P1] = %s" % ('+' if sgn > 0 else '-', d0, d1))
    # in the (K = P1, P = P0) NH convention [H,K] = a2 P, [H,P] = b1 K : a2 = coeff of P0 in [e,P1], b1 = coeff of P1 in [e,P0]
    a2c = d1.get('P0_1', 0); b1c = d0.get('P1_1', 0)
    chk("C3%s NH (a2 = %s, b1 = %s): b1 = %s w^2 with a2 = 1 : %s Newton-Hooke of frequency w" % ('a' if sgn > 0 else 'b', a2c, b1c, '-' if sgn > 0 else '+', 'oscillating' if sgn > 0 else 'expanding'),
        sp.simplify(a2c) == 1 and sp.simplify(b1c + sgn * w ** 2) == 0)
# D: D-conjugation rescales w
Dm = [[0] * 12 for _ in range(12)]
g12names = list(g12)
chk("D1 [D, H + w^2 C] = -H + w^2 C : e^{s ad D}(H + w^2 C) = e^{-s} (H + w^2 e^{2s} C): every w is conjugate to every other up to an overall scale of the generator",
    get(f12, 'D', 'H', g12) == {'H': -1} and get(f12, 'D', 'C', g12) == {'C': 1})
s_, w0 = sp.symbols('s w0', positive=True)
# exact conjugation from the structure constants: ad_D restricted to span(H, C), matrix exponential
adD = sp.zeros(2, 2)
for j_, nm in enumerate(('H', 'C')):
    dd = get(f12, 'D', nm, g12)
    for i_, mm in enumerate(('H', 'C')): adD[i_, j_] = dd.get(mm, 0)
conj = sp.simplify((s_ * adD).exp() * sp.Matrix([1, w0 ** 2]))     # e^{s ad D} (H + w0^2 C) as (coefficient of H, coefficient of C)
wp = sp.simplify(w0 * sp.exp(s_))
print("D: e^{s ad D}(H + w0^2 C) has components", list(conj))
chk("D2 computed from the structure constants: e^{s ad D}(H + w^2 C) = e^{-s} (H + wp^2 C) with wp = w e^{s}: the whole family of frequencies is ONE D-orbit (up to an overall factor e^{-s} on the generator), so the magnitude w is a unit; the spectrum of the conjugated element is unchanged (conjugation) while N is not touched",
    sp.simplify(conj[0] - sp.exp(-s_)) == 0 and sp.simplify(conj[1] - sp.exp(-s_) * wp ** 2) == 0)

# E: pair of hyperbolic elements in one sl(2): free rapidity
th = sp.Symbol('theta', real=True)
Xm = sp.Matrix([[1, 0], [0, -1]]); Ym_base = Xm
g = sp.Matrix([[sp.cosh(th), sp.sinh(th)], [sp.sinh(th), sp.cosh(th)]])   # boost in SL(2,R), det 1
Y = sp.simplify(g * Xm * g.inv())
trXY = sp.simplify((Xm * Y).trace())
print("E: tr(X Y) for two hyperbolic unit elements related by a rapidity theta:", trXY)
chk("E1 tr(XY) = 2 cosh(2 theta): the relative position of two hyperbolic (dilatation-type) elements of sl(2,R) is a continuous invariant in [2, inf): not fixed by the algebra",
    sp.simplify(trXY - 2 * sp.cosh(2 * th)) == 0)
chk("E2 control: theta = 0 gives tr(XY) = 2 = tr(X^2) (same element); mutation: tr(XY) can never be < 2 for hyperbolic pairs of equal norm (it is 2 cosh)",
    sp.simplify(trXY.subs(th, 0)) == 2 and all(float(trXY.subs(th, v)) >= 2 for v in (0.1, 0.5, 1.0, 3.0)))
print("\n%d/%d checks pass" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
