"""m04: Lie-algebra cohomology of the kinematical / Newton-Hooke / Galilean-conformal algebras (numerical, full Chevalley-Eilenberg complex).

  H^2(g,R)  = central extensions (what central charges exist);   H^2(g,g) = infinitesimal deformations (which parameters can be turned on).
Since D is IN the algebra it acts trivially on H^*(g,M): only D-INVARIANT (weight-0) central charges and deformations survive.  So H^2 of Galilei x| D_z answers
'which central charge / which deformation parameter is compatible with the dilatation of exponent z'.  m05 repeats the deformation count exactly (rational) in the
rotation-covariant ansatz and names the directions.

 A  controls of the cohomology code (so(3), Heisenberg, abelian; a Jacobi-violating mutation is rejected; exact rational cross-check).
 B  table of H^2(g,R) and H^2(g,g) (d = 3; and d = 2 for H^2(g,R)); the abelianisation classes (a pair of commuting generators outside [g,g]) are separated from the 'genuine' central charges.
 C  explicit cocycles on Galilei x| D_z: mass psi_M, exotic psi_theta (2+1), the 1/c^2 direction phi_c and the Lambda direction phi_L (both defined as first-order derivatives of one-parameter families of vector fields).
 D  what central charges can carry.
"""
import numpy as np, sympy as sp, sys, itertools
from m_cohom import *
from m_vf import *
ok = []
def chk(name, cond):
    ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

# ---------------- A controls ----------------
def so3():
    C = np.zeros((3, 3, 3))
    for i, j, k in itertools.permutations(range(3)): C[i, j, k] = np.linalg.det(np.eye(3)[[i, j, k]])
    return C
h3 = np.zeros((3, 3, 3)); h3[0, 1, 2] = 1; h3[1, 0, 2] = -1
r_so3 = (H2_trivial(so3())[0], H2_adjoint(so3())[0]); r_h3 = H2_trivial(h3)[0]
chk("A1 control so(3): H^2(g,R) = H^2(g,g) = 0 (semisimple rigidity)  -> %s" % (r_so3,), r_so3 == (0, 0))
chk("A2 control Heisenberg h3: H^2(g,R) = 2 (known)", r_h3 == 2)
so41 = so_pq(4, 1); so32 = so_pq(3, 2); so42 = so_pq(4, 2)
bad = so41.copy(); bad[0, 1, 2] += 0.3
raised = False
try: H2_trivial(bad)
except AssertionError: raised = True
chk("A3 MUTATION: a Jacobi-violating structure tensor is rejected by the d^2 = 0 assertion", raised)
sig41, sig32 = killing_sig(so41), killing_sig(so32)
chk("A4 Killing signatures label the two (b1,h1)-nonzero Lorentz classes: so(4,1) -> %s, so(3,2) -> %s" % (sig41, sig32), sig41 == (6, 4) and sig32 == (4, 6))
# exact rational cross-check of ranks for Galilei(3): sympy DomainMatrix over QQ on the d1,d2 of H^2(g,R)
from sympy.polys.matrices import DomainMatrix
from sympy import QQ
g_, co_ = fam(3); nm_, C_ = tensor_from_vf(g_, co_)
n_ = C_.shape[0]; P2 = pairs(n_); P3 = triples(n_); i2 = {p: i for i, p in enumerate(P2)}
d1 = sp.zeros(len(P2), n_)
for (a, b), r in i2.items():
    for e in range(n_): d1[r, e] = -sp.Rational(C_[a, b, e]).limit_denominator(1000)
d2 = sp.zeros(len(P3), len(P2))
for r, (a, b, c) in enumerate(P3):
    for (x, y, z_, sg) in ((a, b, c, -1), (a, c, b, +1), (b, c, a, -1)):
        for e in range(n_):
            co = sp.Rational(C_[x, y, e]).limit_denominator(1000)
            if co == 0 or e == z_: continue
            idx, sgn = (i2[(e, z_)], 1) if e < z_ else (i2[(z_, e)], -1)
            d2[r, idx] += sg * co * sgn
rk1 = DomainMatrix.from_Matrix(d1).convert_to(QQ).rank(); rk2 = DomainMatrix.from_Matrix(d2).convert_to(QQ).rank()
chk("A5 exact rational ranks reproduce the numerical H^2(g,R) of Galilei(3): %d - %d - %d = %d" % (len(P2), rk2, rk1, len(P2) - rk2 - rk1), len(P2) - rk2 - rk1 == H2_trivial(C_)[0] == 1)

# ---------------- B tables ----------------
print("\nB: cohomology table (d = 3)   [H2(g,R) = all classes;  'genuine' = minus the C(a,2) classes supported on the abelianisation g/[g,g]]")
res = {}
def entry(label, C, adj=True):
    jd = jacobi_defect(C); h2r = H2_trivial(C)[0]; h2a = H2_adjoint(C)[0] if adj else None
    nab, a = abelianisation_classes(C)
    res[label] = dict(dim=C.shape[0], R=h2r, adj=h2a, nab=nab, a=a, genuine=h2r - nab)
    print("   %-36s dim %2d  Jac %.0e  H2(g,R)=%d (abelianisation a=%d -> %d, genuine %d)  H2(g,g)=%s" % (label, C.shape[0], jd, h2r, a, nab, h2r - nab, h2a))
def vf_entry(label, kind_args, d=3, adj=True, kind='fam'):
    g, co = (fam(d, **kind_args) if kind == 'fam' else cg(d, **kind_args)); names, C = tensor_from_vf(g, co); entry(label, C, adj); return names, C
vf_entry('Galilei', dict())
vf_entry('Newton-Hooke expanding (s=-1)', dict(s=-1))
vf_entry('Newton-Hooke oscillating (s=+1)', dict(s=+1))
vf_entry('Poincare (Lorentz boosts, eps=+1)', dict(eps=1))
vf_entry('Euclid-type (eps=-1)', dict(eps=-1))
entry('so(4,1) = dS4', so41); entry('so(3,2) = AdS4', so32)
zs = (sp.Rational(1, 2), 1, sp.Rational(3, 2), 2, 3)
for zz in zs: vf_entry('Galilei x| D_z, z = %s' % zz, dict(z=zz))
vf_entry('Galilei x| D_0 (space dil.)', dict(z=0))
vf_entry('Newton-Hooke(-) x| D_0 (space dil.)', dict(s=-1, z=0))
vf_entry('Newton-Hooke(+) x| D_0 (space dil.)', dict(s=+1, z=0))
vf_entry('Poincare x| Weyl D (z=1)', dict(eps=1, z=1))
vf_entry('Schroedinger = cg_{1/2}(3)', dict(l=sp.Rational(1, 2)), kind='cg')
vf_entry('GCA = cg_1(3)', dict(l=1), kind='cg')
entry('so(4,2)', so42)
vf_entry('cg_{3/2}(3)  (H2(g,R) only)', dict(l=sp.Rational(3, 2)), kind='cg', adj=False)
vf_entry('cg_2(3)  (H2(g,R) only)', dict(l=2), kind='cg', adj=False)
print("   (2+1 dimensional, H^2(g,R) only)")
res2 = {}
for label, kind, kw in (('Galilei(2)', 'fam', {}), ('NH oscillating(2)', 'fam', {'s': 1}), ('NH expanding(2)', 'fam', {'s': -1}),
                        ('Galilei x| D_1 (2)', 'fam', {'z': 1}), ('Galilei x| D_2 (2)', 'fam', {'z': 2}),
                        ('Schroedinger cg_{1/2}(2)', 'cg', {'l': sp.Rational(1, 2)}), ('GCA cg_1(2)', 'cg', {'l': 1}),
                        ('cg_{3/2}(2)', 'cg', {'l': sp.Rational(3, 2)}), ('cg_2(2)', 'cg', {'l': 2})):
    g, co = (fam(2, **kw) if kind == 'fam' else cg(2, **kw)); names, C = tensor_from_vf(g, co)
    h2 = H2_trivial(C)[0]; nab, a = abelianisation_classes(C); res2[label] = (h2, nab, h2 - nab)
    print("   %-36s dim %2d   H2(g,R) = %d   abelianisation classes %d   genuine %d" % (label, C.shape[0], h2, nab, h2 - nab))
R = lambda k: res[k]
chk("B1 3+1: Galilei and BOTH Newton-Hooke have exactly ONE genuine central extension (the mass)", all(R(k)['genuine'] == 1 for k in ['Galilei', 'Newton-Hooke expanding (s=-1)', 'Newton-Hooke oscillating (s=+1)']))
chk("B2 Poincare, Euclid-type, so(4,1), so(3,2): NO central extension at all", all(R(k)['R'] == 0 for k in ['Poincare (Lorentz boosts, eps=+1)', 'Euclid-type (eps=-1)', 'so(4,1) = dS4', 'so(3,2) = AdS4']))
chk("B3 so(4,1), so(3,2), so(4,2) are rigid: H^2(g,g) = 0 (semisimple rigidity)", R('so(4,1) = dS4')['adj'] == 0 and R('so(3,2) = AdS4')['adj'] == 0 and R('so(4,2)')['adj'] == 0)
chk("B4 3+1 Galilei x| D_z: a genuine central extension ONLY at z = 2 (the mass; weight z-2): none at z = 1/2, 1, 3/2, 3",
    [R('Galilei x| D_z, z = %s' % zz)['genuine'] for zz in zs] == [0, 0, 0, 1, 0])
chk("B5 GCA cg_1(3) (the MOND z=1 kinematics + accelerations): NO central extension in 3+1; Schroedinger cg_{1/2}: one (mass); cg_{3/2}: one; cg_2: none (half-integer l <-> mass, integer l <-> none in d=3)",
    R('GCA = cg_1(3)')['R'] == 0 and R('Schroedinger = cg_{1/2}(3)')['R'] == 1 and R('cg_{3/2}(3)  (H2(g,R) only)')['R'] == 1 and R('cg_2(3)  (H2(g,R) only)')['R'] == 0)
chk("B6 2+1 counts: Galilei has 2 genuine central charges (mass, exotic: types verified in C2 for Galilei x| D_z); cg_1(2), cg_2(2), cg_{1/2}(2), cg_{3/2}(2) have 1 each (types exotic/mass per the literature statement, not identified here)",
    res2['Galilei(2)'][2] == 2 and res2['GCA cg_1(2)'][2] == 1 and res2['Schroedinger cg_{1/2}(2)'][2] == 1 and res2['cg_{3/2}(2)'][2] == 1 and res2['cg_2(2)'][2] == 1)
chk("B7 the D_0-extended Newton-Hooke algebras have NO genuine central extension (their H^2(g,R) is the abelianisation pair (D_0, H)): the mass has weight -2 there",
    R('Newton-Hooke(-) x| D_0 (space dil.)')['genuine'] == 0 and R('Newton-Hooke(+) x| D_0 (space dil.)')['genuine'] == 0)

# Bargmann and Newton-Hooke-Bargmann (the mass-extended algebras): further central extensions?
def with_mass(names, C):
    n = C.shape[0]; C2 = np.zeros((n + 1, n + 1, n + 1)); C2[:n, :n, :n] = C
    for i in (1, 2, 3):
        a, b = names.index('K%d' % i), names.index('P%d' % i); C2[a, b, n] = 1.0; C2[b, a, n] = -1.0
    return names + ['M'], C2
print("\n   mass-extended algebras (d = 3):")
for label, kw in (('Bargmann', dict()), ('Newton-Hooke(-)-Bargmann', dict(s=-1)), ('Newton-Hooke(+)-Bargmann', dict(s=+1))):
    g, co = fam(3, **kw); names, C = tensor_from_vf(g, co); nm2, C2 = with_mass(names, C)
    h2 = H2_trivial(C2)[0]; nab, a = abelianisation_classes(C2)
    res[label] = dict(R=h2, genuine=h2 - nab, dim=C2.shape[0], jd=jacobi_defect(C2))
    print("   %-30s dim %d  Jac %.0e  H2(g,R) = %d  (abelianisation %d, genuine %d)" % (label, C2.shape[0], jacobi_defect(C2), h2, nab, h2 - nab))
chk("B8 the mass-extended (Bargmann-type) algebras in 3+1 admit NO further central extension (genuine H^2(g,R) = 0): the mass is the only central charge, and it is already in", all(res[k]['genuine'] == 0 and res[k]['jd'] < 1e-12 for k in ('Bargmann', 'Newton-Hooke(-)-Bargmann', 'Newton-Hooke(+)-Bargmann')))

# ---------------- C explicit cocycles ----------------
def d2_apply(C, psi_vec):
    n = C.shape[0]; P2_ = pairs(n); P3_ = triples(n); i2_ = {p: i for i, p in enumerate(P2_)}
    out = np.zeros(len(P3_))
    for r, (a, b, c) in enumerate(P3_):
        for (x, y, z_, sg) in ((a, b, c, -1), (a, c, b, +1), (b, c, a, -1)):
            for e in range(n):
                co_ = C[x, y, e]
                if co_ == 0 or e == z_: continue
                idx, sgn = (i2_[(e, z_)], 1) if e < z_ else (i2_[(z_, e)], -1)
                out[r] += sg * co_ * sgn * psi_vec[idx]
    return out
def pair_cochain(names, C, entries):
    n = len(names); P2_ = pairs(n); i2_ = {p: i for i, p in enumerate(P2_)}; psi = np.zeros(len(P2_))
    for (x, y, val) in entries:
        a, b = names.index(x), names.index(y)
        if a < b: psi[i2_[(a, b)]] += val
        else: psi[i2_[(b, a)]] -= val
    return psi
def nontrivial(C, psi):
    n = C.shape[0]; P2_ = pairs(n); i2_ = {p: i for i, p in enumerate(P2_)}
    d1_ = np.zeros((len(P2_), n))
    for (a, b), r in i2_.items(): d1_[r, :] = -C[a, b, :]
    return rank_gap(np.column_stack([d1_, psi]))[0] > rank_gap(d1_)[0]
print("\nC: explicit central cocycles on Galilei x| D_z")
resid = {}; nontriv = {}
zs2 = (0, sp.Rational(1, 2), 1, sp.Rational(3, 2), 2, 3)
for zz in zs2:
    g, co = fam(3, z=zz); names, C = tensor_from_vf(g, co)
    psi = pair_cochain(names, C, [('K%d' % i, 'P%d' % i, 1.0) for i in (1, 2, 3)])
    resid[zz] = np.linalg.norm(d2_apply(C, psi)); nontriv[zz] = nontrivial(C, psi)
    print("   d=3  z = %-4s  mass psi_M(K_i,P_j)=delta_ij : |d psi| = %.3g" % (zz, resid[zz]))
chk("C1 the mass cocycle is closed exactly at z = 2 (checked z = 0, 1/2, 1, 3/2, 2, 3) and is non-trivial there", [z_ for z_, v in resid.items() if v < 1e-9] == [2] and nontriv[2])
res_th = {}
for zz in (0, sp.Rational(1, 2), 1, sp.Rational(3, 2), 2):
    g, co = fam(2, z=zz); names, C = tensor_from_vf(g, co)
    psi_th = pair_cochain(names, C, [('K1', 'K2', 1.0)]); psi_m = pair_cochain(names, C, [('K1', 'P1', 1.0), ('K2', 'P2', 1.0)])
    res_th[zz] = (np.linalg.norm(d2_apply(C, psi_th)), np.linalg.norm(d2_apply(C, psi_m)), nontrivial(C, psi_th))
    print("   d=2  z = %-4s  exotic psi_theta(K1,K2) : |d psi| = %.3g ; mass : |d psi| = %.3g" % (zz, res_th[zz][0], res_th[zz][1]))
chk("C2 in 2+1: exotic charge [K1,K2] is closed and non-trivial exactly at z = 1 (weight 2(z-1) = 0), mass exactly at z = 2 (weight z-2 = 0)",
    [z_ for z_, v in res_th.items() if v[0] < 1e-9] == [1] and [z_ for z_, v in res_th.items() if v[1] < 1e-9] == [2] and res_th[1][2])
# deformation directions as derivatives of one-parameter families (exactly linear in the parameter)
def fam_tensor(d, z=None, **kw):
    g, co = fam(d, z=z, **kw); return tensor_from_vf(g, co)
def adj_apply(C, phi):
    n = C.shape[0]; P2_ = pairs(n); P3_ = triples(n); i2_ = {p: i for i, p in enumerate(P2_)}
    def ph(x, y):
        if x == y: return np.zeros(n)
        return phi[i2_[(x, y)]] if x < y else -phi[i2_[(y, x)]]
    tot = 0.0
    for (a, b, c) in P3_:
        v = np.zeros(n)
        for (x, y, z_, sg) in ((a, b, c, +1), (b, a, c, -1), (c, a, b, +1)): v += sg * np.einsum('e,em->m', ph(y, z_), C[x])
        for (x, y, z_, sg) in ((a, b, c, -1), (a, c, b, +1), (b, c, a, -1)):
            for k in range(n):
                if C[x, y, k] != 0: v += sg * C[x, y, k] * ph(k, z_)
        tot += float(v @ v)
    return np.sqrt(tot)
respd = {}
for zz in (0, sp.Rational(1, 2), 1, 2):
    names, C0 = fam_tensor(3, z=zz); n = len(names)
    # first-order directions: derivative of the family; the 10-dim block changes, the D rows/columns are unchanged
    nm10, C0_10 = fam_tensor(3); nmE, CE = fam_tensor(3, eps=1); nmS, CS = fam_tensor(3, s=1)
    assert nm10 == nmE == nmS == names[:10]
    phiC = np.zeros((n, n, n)); phiL = np.zeros((n, n, n))
    phiC[:10, :10, :10] = CE - C0_10; phiL[:10, :10, :10] = CS - C0_10
    def to_pair(T):
        P2_ = pairs(n); return np.array([T[a, b, :] for (a, b) in P2_])
    respd[zz] = (adj_apply(C0, to_pair(phiL)), adj_apply(C0, to_pair(phiC)))
    print("   z = %-4s  |d phi_Lambda| = %.3g    |d phi_c| = %.3g" % (zz, *respd[zz]))
chk("C3 first-order deformation towards Newton-Hooke / Lambda (derivative of the family H_s = H + s C) is a cocycle ONLY for z = 0", [z_ for z_, v in respd.items() if v[0] < 1e-9] == [0])
chk("C4 first-order deformation towards finite c (derivative of K_eps = t d_i + eps x_i d_t) is a cocycle ONLY for z = 1 (Weyl scaling)", [z_ for z_, v in respd.items() if v[1] < 1e-9] == [1])
chk("C5 at z = 1/2 (the dilatation that leaves a0 invariant) NEITHER direction is a cocycle: 1/c^2 and 1/tau^2 are both obstructed at first order", respd[sp.Rational(1, 2)][0] > 1e-6 and respd[sp.Rational(1, 2)][1] > 1e-6)
chk("C6 the two directions are never simultaneously closed for any z tested: no dilatation tolerates c and H_Lambda together", not any(v[0] < 1e-9 and v[1] < 1e-9 for v in respd.values()))

# ---------------- D summary of what the central charges are ----------------
print("\nD: central charges found and what they carry")
print("   3+1 Galilei / NH / Schroedinger / cg_{3/2}: the MASS m ([K_i,P_j] = m delta_ij).  2+1: mass and the exotic charge theta ([K_1,K_2] = theta).  No other classes.")
print("   In [K,P] = m delta the bracket has dimensions M (from K ~ ML, P ~ ML/T, A = ML^2/T):  m is a MASS; theta ~ M L^2/T x (1/...)  (an action per mass^2 scale); neither is a rate or an acceleration.")
g2, co2 = fam(2); nm2, C2 = tensor_from_vf(g2, co2); n2 = len(nm2)
psi_m2 = pair_cochain(nm2, C2, [('K1', 'P1', 1.0), ('K2', 'P2', 1.0)]); psi_t2 = pair_cochain(nm2, C2, [('K1', 'K2', 1.0)]); psi_jh = pair_cochain(nm2, C2, [('J12', 'H', 1.0)])
P2_ = pairs(n2); i2_ = {p: i for i, p in enumerate(P2_)}
d1_ = np.zeros((len(P2_), n2))
for (a, b), r in i2_.items(): d1_[r, :] = -C2[a, b, :]
rk_all = rank_gap(np.column_stack([d1_, psi_m2, psi_t2, psi_jh]))[0] - rank_gap(d1_)[0]
closed3 = all(np.linalg.norm(d2_apply(C2, p)) < 1e-9 for p in (psi_m2, psi_t2, psi_jh))
chk("D1 the whole H^2(g,R) of Galilei(2+1) (dimension 3, table B) is spanned by three EXPLICIT classes: mass psi(K,P), exotic psi(K1,K2), and psi(J,H) (the abelianisation pair); all closed, independent modulo coboundaries. None is a rate or an acceleration.",
    closed3 and rk_all == 3 and res2['Galilei(2)'][0] == 3)
print("\n%d/%d checks pass" % (sum(ok), len(ok)))
sys.exit(0 if all(ok) else 1)
