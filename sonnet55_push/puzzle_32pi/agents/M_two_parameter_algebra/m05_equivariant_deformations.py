"""m05: exact (rational) deformation count of the rotation-covariant ansatz at chosen base algebras, with the surviving directions NAMED.

At a base algebra g0 in the 21-constant ansatz (J,K,P,H,D):  tangent space to the Jacobi variety = ker(dJac at g0);  orbit tangent = image of the infinitesimal
rescalings/mixings GL(K,P) x GL(H,D) of the basis (exact automorphisms of the ansatz form);  H^2_rot(g0,g0) = ker / orbit.  For so(3) semisimple this equals the full
H^2(g0,g0) (spectral sequence of a reductive subalgebra), and m04 computes the full one numerically: the two must agree (cross-check).

 A  base points: Galilei, NH+-, Poincare-type, Euclid-type, (b1,h1 != 0) dS/AdS-type; Galilei x| D_z for z = 0, 1/2, 1, 3/2, 2, 3; NH x| D_0; Poincare x| Weyl.
 B  the surviving directions, by name.
 C  what the z = 1 (MOND) and z = 1/2 (a0-invariant) algebras can and cannot be deformed into.
"""
import sympy as sp, numpy as np, sys
from m_tools import *
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

names21 = 'a1 a2 a3 b1 b2 b3 p1 p2 p3 q1 q2 q3 f1 f2 c1 c2 c3 d1 d2 d3 h1 h2 e2 e3 e4'.split()
S21 = sp.symbols(names21)
DONLY = ('p1', 'p2', 'p3', 'q1', 'q2', 'q3', 'f1', 'f2', 'h2')
SETUP = {}
for wd in (False, True):
    sym = [s_ for s_ in S21 if wd or str(s_) not in DONLY]
    fs_, n_ = rot_ansatz({str(s_): s_ for s_ in sym}, with_D=wd)
    polys_ = [v for _, _, v in jacobi_residuals(fs_, n_)]
    Jac_ = [[sp.diff(p, s_) for s_ in sym] for p in polys_]
    Ds_ = dense(fs_, n_)
    dT_ = {s_: [[[sp.diff(sp.sympify(Ds_[a][b][e]), s_) for e in range(n_)] for b in range(n_)] for a in range(n_)] for s_ in sym}
    SETUP[wd] = (sym, n_, Jac_, Ds_, dT_)
    print("A: with_D=%s : %d Jacobi residual entries, %d structure constants, n = %d" % (wd, len(polys_), len(sym), n_))

def gl_generators(with_D):
    gens = []
    # K,P mixing (acts on the three components alike): X e_src = e_dst
    for (src, dst) in [(3, 3), (3, 6), (6, 3), (6, 6)]:
        gens.append(('K/P:%s->%s' % ('KP'[(src - 3) // 3], 'KP'[(dst - 3) // 3]), [(src + i, dst + i) for i in range(3)]))
    # vector -> J shifts (K -> K + w J, P -> P + w J): equivariant basis changes that keep J as the rotation generators
    gens.append(('K->J', [(3 + i, 0 + i) for i in range(3)])); gens.append(('P->J', [(6 + i, 0 + i) for i in range(3)]))
    if with_D:
        for (src, dst, nm) in [(9, 9, 'H->H'), (9, 10, 'H->D'), (10, 9, 'D->H'), (10, 10, 'D->D')]: gens.append(('H/D:' + nm, [(src, dst)]))
    else:
        gens.append(('H:H->H', [(9, 9)]))
    return gens

def analyse(base, with_D=True, label=''):
    sym, n, Jac, Ds, dT = SETUP[with_D]
    nn = n
    sub = {s_: base.get(str(s_), 0) for s_ in sym}
    Jn = sp.Matrix([[sp.nsimplify(e.subs(sub)) for e in row] for row in Jac])
    kerv = Jn.nullspace()
    C0 = [[[sp.nsimplify(sp.sympify(Ds[a][b][e]).subs(sub)) for e in range(n)] for b in range(n)] for a in range(n)]
    cols = []
    for gname, pairs_ in gl_generators(with_D):
        Xmap = {}
        for (src, dst) in pairs_: Xmap[src] = dst
        dC = [[[0] * n for _ in range(n)] for _ in range(n)]
        for a in range(n):
            for b in range(n):
                for e in range(n):
                    v = 0
                    for src, dst in Xmap.items():
                        if e == dst: v += C0[a][b][src]
                    if a in Xmap: v -= C0[Xmap[a]][b][e]
                    if b in Xmap: v -= C0[a][Xmap[b]][e]
                    dC[a][b][e] = v
        Amat = []; rhs = []
        for a in range(n):
            for b in range(a + 1, n):
                for e in range(n):
                    Amat.append([dT[s_][a][b][e] for s_ in sym]); rhs.append(dC[a][b][e])
        sol = sp.linsolve((sp.Matrix(Amat), sp.Matrix(rhs)))
        if sol == sp.S.EmptySet: raise RuntimeError("orbit direction leaves the ansatz: " + gname)
        sol = list(sol)[0]
        sol = sp.Matrix([x.subs({sy: 0 for sy in x.free_symbols}) if x.free_symbols else x for x in sol])
        cols.append(sol)
    Orb = sp.Matrix.hstack(*cols)
    dim_ker = len(kerv); rk_orb = Orb.rank()
    inker = all(sp.simplify((Jn * Orb[:, k]).norm()) == 0 for k in range(Orb.shape[1]))
    Kmat = sp.Matrix.hstack(*kerv) if kerv else sp.zeros(len(sym), 0)
    cur = Orb; reps = []
    for k in range(Kmat.shape[1]):
        test = sp.Matrix.hstack(cur, Kmat[:, k])
        if test.rank() > cur.rank(): cur = test; reps.append(Kmat[:, k])
    fnames = [str(s_) for s_ in sym]
    named = [{fnames[i]: r[i] for i in range(len(sym)) if r[i] != 0} for r in reps]
    return dict(ker=dim_ker, orbit=rk_orb, H2=dim_ker - rk_orb, inker=inker, reps=named)

def base_d(st, sc): return {'a2': 1, 'b1': st, 'h1': sc, 'c1': sc, 'd1': -st * sc}
def with_z(par, z): d_ = dict(par); d_.update({'f1': -z, 'p1': z - 1, 'q2': -1}); return d_
R = {}
tests = [('Galilei', base_d(0, 0), False), ('Newton-Hooke expanding', base_d(1, 0), False), ('Newton-Hooke oscillating', base_d(-1, 0), False),
         ('Poincare-type (b1=0,h1=-1)', base_d(0, -1), False), ('Euclid-type (b1=0,h1=+1)', base_d(0, 1), False),
         ('(b1=+1,h1=-1)', base_d(1, -1), False), ('(b1=-1,h1=-1)', base_d(-1, -1), False)]
for zz in (0, sp.Rational(1, 2), 1, sp.Rational(3, 2), 2, 3):
    tests.append(('Galilei x| D_z, z = %s' % zz, with_z(base_d(0, 0), zz), True))
tests.append(('NH expanding x| D_0', with_z(base_d(1, 0), 0), True))
tests.append(('NH oscillating x| D_0', with_z(base_d(-1, 0), 0), True))
tests.append(('Poincare x| Weyl (z=1)', with_z(base_d(0, -1), 1), True))
print("\nB: exact rotation-covariant H^2(g0,g0) and the surviving directions (parameters that can be turned on)")
for lab, par, wd in tests:
    r = analyse(par, wd, lab); R[lab] = r
    print("   %-32s ker %2d  orbit %2d  ->  H2 = %d   directions: %s" % (lab, r['ker'], r['orbit'], r['H2'], r['reps']))
chk("B0 sanity: every orbit direction lies in the kernel of the linearised Jacobi map (the infinitesimal equivalences are exact automorphisms of the ansatz)", all(r['inker'] for r in R.values()))
# cross-check with the numerical full-complex values of m04
num = {'Galilei': 4, 'Newton-Hooke expanding': 2, 'Newton-Hooke oscillating': 2, 'Poincare-type (b1=0,h1=-1)': 1, 'Euclid-type (b1=0,h1=+1)': 1,
       '(b1=+1,h1=-1)': 0, '(b1=-1,h1=-1)': 0,
       'Galilei x| D_z, z = 0': 2, 'Galilei x| D_z, z = 1/2': 2, 'Galilei x| D_z, z = 1': 2, 'Galilei x| D_z, z = 3/2': 1, 'Galilei x| D_z, z = 2': 1, 'Galilei x| D_z, z = 3': 1,
       'NH expanding x| D_0': 0, 'NH oscillating x| D_0': 0, 'Poincare x| Weyl (z=1)': 0}
mism = {k: (R[k]['H2'], v) for k, v in num.items() if R[k]['H2'] != v}
chk("B1 CROSS-CHECK: the exact rotation-covariant H^2 equals the numerical full-complex H^2(g,g) of m04 for all 16 base algebras (reductive-subalgebra spectral-sequence with so(3)); mismatches: %s" % mism, not mism)

# named content
def has(lab, *keys): return any(all(k in d_ for k in keys) for d_ in R[lab]['reps'])
print("\nC: reading the directions")
chk("C1 Galilei: the four directions include the Lambda direction b1 (Newton-Hooke) and the c-direction h1 (with c1 = a2 h1)", any('b1' in d_ for d_ in R['Galilei']['reps']) and any('h1' in d_ or 'c1' in d_ for d_ in R['Galilei']['reps']))
z1 = R['Galilei x| D_z, z = 1']['reps']; zh = R['Galilei x| D_z, z = 1/2']['reps']
print("   z = 1   directions:", z1); print("   z = 1/2 directions:", zh)
chk("C2 Galilei x| D_1 (MOND kinematics): NO direction contains b1 (Lambda) or d1: the Lambda deformation is obstructed at first order for z = 1", not any(('b1' in d_) or ('d1' in d_) for d_ in z1))
chk("C3 Galilei x| D_1: a direction with h1 / c1 exists (deformation to the Weyl-Poincare algebra: c can be switched on, Lambda cannot)", any(('h1' in d_) or ('c1' in d_) for d_ in z1))
chk("C4 Galilei x| D_{1/2} (a0-invariant scaling): NO direction contains b1, h1, c1 or d1: neither Lambda nor 1/c^2 can be switched on", not any(any(k in d_ for k in ('b1', 'h1', 'c1', 'd1')) for d_ in zh))
chk("C5 z = 1/2: the two surviving directions are (i) a change of the D-action (p1,q2: moves along the z family) and (ii) c3: [K_i,K_j] = c3 eps_ijk P_k with c3 ~ 1/acceleration",
    len(zh) == 2 and any(set(d_) == {'p1', 'q2'} for d_ in zh) and any(set(d_) == {'c3'} for d_ in zh))
chk("C6 rigid points: (b1,h1 both nonzero) dS/AdS-type, NH x| D_0 and Poincare x| Weyl have H^2 = 0: no further parameter (in particular no a0) can be added at first order", all(R[k]['H2'] == 0 for k in ['(b1=+1,h1=-1)', '(b1=-1,h1=-1)', 'NH expanding x| D_0', 'NH oscillating x| D_0', 'Poincare x| Weyl (z=1)']))
chk("C7 at every z tested (0, 1/2, 1, 3/2, 2, 3) there is a direction that only changes the D-weights (f1,p1,q2): the dilatation exponent z is a genuine continuous modulus of Galilei x| D_z (the only D-invariant dimensionless one)",
    all(any(set(d_) <= {'f1', 'p1', 'q2'} for d_ in R['Galilei x| D_z, %s' % zz]['reps']) for zz in ('z = 0', 'z = 1/2', 'z = 1', 'z = 3/2', 'z = 2', 'z = 3')))
print("\n%d/%d checks pass" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
