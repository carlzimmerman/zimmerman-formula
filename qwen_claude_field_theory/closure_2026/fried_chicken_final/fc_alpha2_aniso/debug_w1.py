import sys, time
sys.path.insert(0, '.')
import sympy as sp
import fc_alpha2_methodB_opt3 as M
P = lambda *a: print(*a, flush=True)

kbv, k2v, q0v, jyv = 0.3, 10.0, 0.2, 1.0
sub = {M.KB: sp.nsimplify(kbv), M.K2: sp.nsimplify(k2v), M.Q0: sp.nsimplify(q0v),
       M.JY: sp.nsimplify(jyv), M.GT: 1, M.kx: 1, M.ky: 0, M.kz: 0}
L = sp.expand(sp.expand(M.L2dc.subs(M.GAUGE)).subs(sub))
eqf = {A: sp.expand(sp.diff(L, A)) for A in M.BRAS}

# static
VZ = {M.Bk[1]:0, M.Bk[2]:0, M.ak[1]:0, M.ak[2]:0, M.hk[(2,3)]:0}
su = [M.Psik, M.hk[(2,2)], M.hk[(3,3)], M.ak[0], M.chik]
sb = [M.Psib, M.hb[(2,2)], M.hb[(3,3)], M.ab[0], M.chib]
e0 = [sp.expand(eqf[A].coeff(M.wb,0).subs(VZ)) for A in sb]
s0s = M.lin_solve(e0, su)
P("static solved:", s0s is not None)
s0 = {**s0s, M.Bk[1]:sp.S(0), M.Bk[2]:sp.S(0), M.ak[1]:sp.S(0), M.ak[2]:sp.S(0), M.hk[(2,3)]:sp.S(0)}

# O(wb^1) system
d1 = {A: sp.Symbol(f'd1_{A}') for A in M.KETS}
d2 = {A: sp.Symbol(f'd2_{A}') for A in M.KETS}
subFull = {A: s0[A] + M.wb*d1[A] + M.wb**2*d2[A] for A in M.KETS}
eqW = {A: sp.expand(eqf[A].subs(subFull)) for A in M.BRAS}
eqs1 = [sp.expand(eqW[A].coeff(M.wb,1)) for A in M.BRAS]
unk1 = list(d1.values())
P("\n--- O(wb^1) equations (which bras are trivial 0 vs sourced) ---")
Uh = M.Uh; subU = {M.Rk: -Uh/(4*sp.pi)}
for A, e in zip(M.BRAS, eqs1):
    ee = sp.expand(e.subs(subU))
    P(f"  bra {A}: {'ZERO' if ee==0 else 'nonzero, len='+str(len(sp.Add.make_args(ee)))}")
Amat, bvec = sp.linear_eq_to_matrix(eqs1, unk1)
P("\nmatrix shape:", Amat.shape, " rank:", Amat.rank(), " of", len(unk1), "unknowns")
# augmented rank to detect inconsistency
Aug = Amat.row_join(bvec)
P("augmented rank:", Aug.rank())
# which unknowns actually appear
appearing = [u for u in unk1 if any(Amat[i, unk1.index(u)] != 0 for i in range(Amat.shape[0]))]
P("unknowns appearing in matrix:", [str(u) for u in appearing])
P("unknowns ABSENT (free):", [str(u) for u in unk1 if u not in appearing])
# nullspace
ns = Amat.nullspace()
P("nullspace dim:", len(ns))
for v in ns:
    nz = [(str(unk1[i]), v[i]) for i in range(len(unk1)) if v[i] != 0]
    P("   null vector nonzero comps:", nz)
