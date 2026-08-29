import sys
sys.path.insert(0, '.')
import sympy as sp
import fc_alpha2_methodB_opt3 as M
P = lambda *a: print(*a, flush=True)

kbv, k2v, q0v, jyv = 0.3, 10.0, 0.2, 1.0
sub = {M.KB: sp.nsimplify(kbv), M.K2: sp.nsimplify(k2v), M.Q0: sp.nsimplify(q0v),
       M.JY: sp.nsimplify(jyv), M.GT: 1, M.kx: 1, M.ky: 0, M.kz: 0}
# UNGAUGED lagrangian (do NOT substitute GAUGE) -- so we can also vary the gauge fields
Lung = sp.expand(M.L2dc.subs(sub))
# all 14 bras and kets
ALLB = M.ALL_BRAS; ALLK = M.ALL_KETS
GAUGE_KETS = [M.Bk[0], M.hk[(1,1)], M.hk[(1,2)], M.hk[(1,3)]]
GAUGE_BRAS = [M.Bb[0], M.hb[(1,1)], M.hb[(1,2)], M.hb[(1,3)]]
GZERO = {k: 0 for k in GAUGE_KETS} | {b: 0 for b in GAUGE_BRAS}
eqf = {A: sp.expand(sp.diff(Lung, A).subs(GZERO)) for A in ALLB}  # 14 eqs, gauge fields set 0

# static solve (even sector) from the physical subset
VZ = {M.Bk[1]:0, M.Bk[2]:0, M.ak[1]:0, M.ak[2]:0, M.hk[(2,3)]:0}
su = [M.Psik, M.hk[(2,2)], M.hk[(3,3)], M.ak[0], M.chik]
sb = [M.Psib, M.hb[(2,2)], M.hb[(3,3)], M.ab[0], M.chib]
e0 = [sp.expand(eqf[A].coeff(M.wb,0).subs(VZ)) for A in sb]
s0s = M.lin_solve(e0, su)
P("static solved:", s0s is not None)
s0 = {**s0s, M.Bk[1]:sp.S(0), M.Bk[2]:sp.S(0), M.ak[1]:sp.S(0), M.ak[2]:sp.S(0), M.hk[(2,3)]:sp.S(0),
      **{k:sp.S(0) for k in GAUGE_KETS}}
# check the GAUGE-field static equations (constraints) are satisfied by static solution
P("\nstatic gauge-field (constraint) residuals:")
for A in GAUGE_BRAS:
    r = sp.expand(eqf[A].coeff(M.wb,0).subs(VZ).subs(s0s))
    P(f"  {A}: {sp.simplify(r)}")

# O(w^1): physical kets get d1; gauge kets stay 0
PHYS_KETS = M.KETS
d1 = {A: sp.Symbol(f'd1_{A}') for A in PHYS_KETS}
d2 = {A: sp.Symbol(f'd2_{A}') for A in PHYS_KETS}
subFull = {A: s0[A] + M.wb*d1[A] + M.wb**2*d2[A] for A in PHYS_KETS}
subFull.update({k: sp.S(0) for k in GAUGE_KETS})
# equations from ALL 14 bras at O(w^1):
eqs1_all = {A: sp.expand(sp.expand(eqf[A]).subs(subFull)).coeff(M.wb,1) for A in ALLB}
unk1 = list(d1.values())
# (a) physical-only 10 eqs:
phys_eqs = [eqs1_all[A] for A in M.BRAS]
Ap, bp = sp.linear_eq_to_matrix(phys_eqs, unk1)
P(f"\n[PHYS 10 eqs] matrix rank {Ap.rank()}  aug rank {Ap.row_join(bp).rank()}  (n={len(unk1)})")
# (b) all 14 eqs (physical + 4 gauge-constraints):
all_eqs = [eqs1_all[A] for A in ALLB]
Aa, ba = sp.linear_eq_to_matrix(all_eqs, unk1)
P(f"[ALL 14 eqs]  matrix rank {Aa.rank()}  aug rank {Aa.row_join(ba).rank()}  (n={len(unk1)})")
sol = list(sp.linsolve((Aa, ba), unk1))
P("14-eq system solves:", bool(sol))
if sol:
    Uh=M.Uh; subU={M.Rk:-Uh/(4*sp.pi)}
    d = dict(zip(unk1, sol[0]))
    b2 = sp.expand(d[d1[M.Bk[1]]].subs(subU)) if d1[M.Bk[1]] in d else None
    # alpha_1 from B2 (H02) coeff of w2*Uh
    B2val = sp.expand(d[d1[M.Bk[1]]].subs(subU))
    a1 = sp.cancel(2*B2val.coeff(M.w2*Uh))
    P("alpha_1 (from 14-eq solve) =", a1, "  target -4K_B =", sp.nsimplify(-4*kbv))
