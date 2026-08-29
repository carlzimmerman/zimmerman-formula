#!/usr/bin/env python3
r"""
ppn_khronon_routeB_num_2026.py -- GAUGE-SAFE Route B PPN readout.

The tau = 0 gauge FAILS on the candidate locus beta + lam = 0: there tau enters the action
only through w.grad(tau), so at w -> 0 the residual static xi^0 freedom is unfixed and the
5x5 response matrix degenerates (verified: det ~ w_z^2 at beta=lam=0, det == 0 in GR).

Fix: DO NOT gauge fix.  Solve the full 6x6 system (Phi, Psi, Z_x, Z_y, Z_z, tau) as an
underdetermined linear system.  The one-parameter null direction is the static xi^0 gauge
mode.  We then use only the pieces that are INVARIANT under it:
    h_00 = 2 Phi              (invariant: xi^0 static => delta h_00 = -2 d_0 xi_0 = 0)
    h_ij = 2 Psi delta_ij     (invariant)
    Z_x  with k along z       (delta Z_i = +d_i xi^0 has NO x-component when k_x = 0)
and we CHECK that those three are free of the null parameter.

Readout (Will TEGP 4.46), static source at rest, preferred frame moving at w:
    Phi/U = 1 - (1/2)(alpha_1 - alpha_3) w^2 + alpha_2 (k.w)^2/k^2
    Z_x   = (alpha_2 - alpha_1)/2 * w_x U            (k_x = 0)
    Psi/Phi|_{w=0} = gamma_PPN ;  Phi|_{w=0} = 4 pi G_N rho / k^2
"""
import sympy as sp
import pickle
import os
import itertools

here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, '_routeB_feq.pkl'), 'rb') as fh:
    D = pickle.load(fh)
FEQ = {k: sp.sympify(v) for k, v in D['FEQ'].items()}

k1, k2, k3 = sp.symbols('k1 k2 k3', real=True)
w1, w2, w3 = sp.symbols('w1 w2 w3', real=True)
G = sp.symbols('G', positive=True)
al, be, lm = sp.symbols('alpha beta lambda_', real=True)
Ph, Ps, Z1h, Z2h, Z3h, Th, Rh = sp.symbols('Phih Psih Z1h Z2h Z3h tauh rhoh')
kk, wx, wz = sp.symbols('kk wx wz', real=True)

FRAME = {k1: 0, k2: 0, k3: kk, w1: wx, w2: 0, w3: wz}
EQS = {key: sp.expand(e.subs(FRAME)) for key, e in FEQ.items()}
UNK = [Ph, Ps, Z1h, Z2h, Z3h, Th]
SYS = [EQS['Phi'], EQS['Psi'], EQS['Z0'], EQS['Z1'], EQS['Z2'], EQS['tau']]
M6, R6 = sp.linear_eq_to_matrix(SYS, UNK)

p_free = sp.Symbol('p_free')


def readout(a, b, l, label, symbolic_alpha=False):
    print("-" * 74)
    print("CASE", label, " (alpha,beta,lam) =", (a, b, l))
    sub = {al: a, be: b, lm: l, kk: 1, G: 1, Rh: 1}
    Mn = M6.subs(sub).applyfunc(sp.cancel)
    Rn = R6.subs(sub).applyfunc(sp.cancel)
    aug = Mn.row_join(Rn)
    rk, rka = Mn.rank(), aug.rank()
    print("   rank(M)=%d  rank([M|b])=%d  (6 unknowns)" % (rk, rka))
    if rk != rka:
        print("   *** INCONSISTENT SYSTEM ***")
        return None
    sol = sp.linsolve((Mn, Rn), UNK)
    sol = list(sol)[0]
    free = sorted(set().union(*[s.free_symbols for s in sol]) -
                  {wx, wz, al, sp.pi}, key=str)
    free = [f for f in free if str(f).startswith('tau') or str(f) in
            ('Phih', 'Psih', 'Z1h', 'Z2h', 'Z3h')]
    PhiS, PsiS, ZxS = [sp.cancel(sp.together(s)) for s in (sol[0], sol[1], sol[2])]
    for nm, ex in (('Phi', PhiS), ('Psi', PsiS), ('Z_x', ZxS)):
        bad = [f for f in ex.free_symbols if f in set(UNK)]
        if bad:
            print("   *** %s depends on gauge parameter %s -- NOT invariant ***" % (nm, bad))
            return None
    Phi0 = sp.simplify(sp.limit(sp.limit(PhiS, wx, 0), wz, 0))
    GN = sp.simplify(Phi0/(4*sp.pi))
    gam = sp.simplify(sp.limit(sp.limit(PsiS, wx, 0), wz, 0)/Phi0)
    print("   G_N/G     =", GN, "        [khronometric prediction 1/(1-alpha/2) =",
          sp.simplify(1/(1 - a/2)), "]")
    print("   gamma_PPN =", gam)
    U0 = 4*sp.pi*GN
    r = sp.cancel(PhiS/U0)
    A = sp.simplify(sp.limit(sp.diff(r, wx, 2).subs(wz, 0), wx, 0)/2)
    C = sp.simplify(sp.limit(sp.diff(r, wz, 2).subs(wx, 0), wz, 0)/2)
    a2 = sp.simplify(C - A)
    a1m3 = sp.simplify(-2*A)
    Azx = sp.simplify(sp.limit(sp.limit(sp.diff(ZxS/U0, wx), wz, 0), wx, 0))
    a1ma2 = sp.simplify(-2*Azx)
    a1 = sp.simplify(a2 + a1ma2)
    a3 = sp.simplify(a1 - a1m3)
    print("   alpha_1 =", sp.factor(a1))
    print("   alpha_2 =", sp.factor(a2))
    print("   alpha_3 =", sp.factor(a3))
    return {'GN': GN, 'gamma': gam, 'a1': a1, 'a2': a2, 'a3': a3}


print("#### VALIDATION 1: GR ####")
readout(0, 0, 0, "GR")

print()
print("#### VALIDATION 2: generic khronometric, exact rationals ####")
PTS = [(sp.Rational(1, 5), sp.Rational(1, 7), sp.Rational(1, 3)),
       (sp.Rational(1, 3), sp.Rational(1, 11), sp.Rational(1, 5)),
       (sp.Rational(2, 7), -sp.Rational(1, 5), sp.Rational(1, 4)),
       (sp.Rational(1, 9), sp.Rational(1, 4), -sp.Rational(1, 13))]
RES = {}
for p in PTS:
    RES[p] = readout(*p, label="generic")

print()
print("#### sign-convention identification vs published khronometric ####")
A_, B_, L_ = sp.symbols('A_ B_ L_')
a1_pub = 4*(A_ - 2*B_)/(B_ - 1)
a2_pub = a1_pub/2 + (A_ - 2*B_)*(A_ + B_ + 3*L_)/((B_ + L_)*(2 - A_))
for sb, sl in itertools.product([1, -1], [1, -1]):
    ok1 = ok2 = True
    for p in PTS:
        if RES.get(p) is None:
            continue
        a, b, l = p
        m = {A_: a, B_: sb*b, L_: sl*l}
        if sp.simplify(a1_pub.subs(m) - RES[p]['a1']) != 0:
            ok1 = False
        if sp.simplify(a2_pub.subs(m) - RES[p]['a2']) != 0:
            ok2 = False
    print("  (beta->%+dbeta, lam->%+dlam):  alpha_1 match=%s   alpha_2 match=%s"
          % (sb, sl, ok1, ok2))

print()
print("#### CANDIDATE LOCUS beta = lam = 0 ####")
for a in [sp.Rational(1, 5), sp.Rational(1, 100), sp.Rational(1, 10000)]:
    readout(a, 0, 0, "candidate beta=lam=0")

print()
print("#### neighbouring degenerate locus beta + lam = 0 with beta != 0 ####")
readout(sp.Rational(1, 5), sp.Rational(1, 7), -sp.Rational(1, 7), "beta+lam=0")
