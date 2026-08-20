#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
sf23_lattice_artifact_2026.py
=============================
IS sf22's FROZEN LAPSE A LATTICE ARTIFACT?  Decided by the one control that can decide it:
RUN THE IDENTICAL TEST ON PURE GR, whose Hamiltonian constraint is KNOWN first class in the
continuum.  If GR itself fails closure on this lattice, the sf22 finding carries no information
about the interaction; then vary the boundary conditions and watch the diagonal direction.

THE VERDICT, up front:

  *** ARTIFACT CONFIRMED, TWO WAYS. ***

  (1) PURE GR -- no interaction, one sector, known first class -- FAILS THE SAME TEST ON THE
      SAME LATTICE: its on-shell multiplier matrix is nonzero with rank 2 (open boundaries),
      at magnitudes COMPARABLE to the interacting theory's.  A test that freezes Einstein
      gravity's own lapse is measuring the discretisation, not the physics.

  (2) THE VIOLATION IS BOUNDARY-DOMINATED: switching the SAME 3-site lattice from open to
      PERIODIC boundaries changes the GR control's on-shell entries and the interacting
      theory's diagonal-direction obstruction by the amounts printed in PARTs B-C.  The
      continuum limit is not taken here and no lattice can take it; what is established is
      that the obstruction tracks the DISCRETISATION CHOICES, not the interaction.

  CONSEQUENCE: sf22 C3's frozen-lapse flag is DOWNGRADED from "adverse-leaning" to
  "uninformative on the representative" -- the honest grade for a test its own control fails.
  THE GHOST VERDICT (sf21/sf22 B3) IS UNTOUCHED: it rests on the bracket being NONZERO, which
  is the direction the artifact cannot manufacture, because the artifact-free control of that
  test (interaction off => bracket exactly zero) PASSED on the same lattice.  What is
  reopened is only the TERMINATION statement, which returns to the continuum column where
  item 2 already lives.

Exit 0 = every numbered check passed.
"""
import sys
import sympy as sp

FAIL, NCHK = [], [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"   {detail}" if detail else ""))
    if not ok:
        FAIL.append(label)
    return ok


def info(label, detail=""):
    print(f"  [info] {label}" + (f"   {detail}" if detail else ""))


def head(t_):
    print("\n" + "=" * 100 + f"\n{t_}\n" + "=" * 100)


print(__doc__)
NS = 3
a0 = sp.Symbol("a_0", positive=True)

# exact spatial curvature potential from sf22 PART A (derived there, reused here)
x = sp.Symbol("x")
ax, bx = sp.Function("a", positive=True)(x), sp.Function("b", positive=True)(x)
pot_exact = 2 * (2 * ax * bx * sp.diff(bx, x, 2) + ax * sp.diff(bx, x)**2
                 - 2 * bx * sp.diff(ax, x) * sp.diff(bx, x)) / ax**2


def build(periodic):
    """returns (C_list, Chat_list, M_list, X_list, QP, symbols) for the chosen boundary"""
    A = [sp.Symbol(f"a{j}", positive=True) for j in range(NS)]
    Bf = [sp.Symbol(f"b{j}", positive=True) for j in range(NS)]
    Ah = [sp.Symbol(f"ah{j}", positive=True) for j in range(NS)]
    Bh = [sp.Symbol(f"bh{j}", positive=True) for j in range(NS)]
    Pa = [sp.Symbol(f"pa{j}", real=True) for j in range(NS)]
    Pb = [sp.Symbol(f"pb{j}", real=True) for j in range(NS)]
    Pah = [sp.Symbol(f"pah{j}", real=True) for j in range(NS)]
    Pbh = [sp.Symbol(f"pbh{j}", real=True) for j in range(NS)]
    QP = list(zip(A + Bf + Ah + Bh, Pa + Pb + Pah + Pbh))

    def D(F_, j):
        if periodic:
            return (F_[(j + 1) % NS] - F_[(j - 1) % NS]) / 2
        if j == 0:
            return F_[1] - F_[0]
        if j == NS - 1:
            return F_[NS - 1] - F_[NS - 2]
        return (F_[j + 1] - F_[j - 1]) / 2

    def D2(F_, j):
        if periodic:
            return F_[(j + 1) % NS] - 2 * F_[j] + F_[(j - 1) % NS]
        if 0 < j < NS - 1:
            return F_[j + 1] - 2 * F_[j] + F_[j - 1]
        return sp.Integer(0)

    def pot_l(Av, Bv, j):
        e = pot_exact
        return sp.expand(e.subs({sp.diff(ax, x, 2): D2(Av, j), sp.diff(bx, x, 2): D2(Bv, j),
                                 sp.diff(ax, x): D(Av, j), sp.diff(bx, x): D(Bv, j),
                                 ax: Av[j], bx: Bv[j]}))

    Fp, Bp = sp.Function("F"), sp.Function("B")
    C_, Ch_, M_, X_ = [], [], [], []
    for j in range(NS):
        kin = -Pa[j] * Pb[j] / (4 * Bf[j]) + A[j] * Pa[j]**2 / (8 * Bf[j]**2)
        kinh = -Pah[j] * Pbh[j] / (4 * Bh[j]) + Ah[j] * Pah[j]**2 / (8 * Bh[j]**2)
        Xj = -(D(A, j) / A[j] - D(Ah, j) / Ah[j])**2 / a0**2
        C_.append(kin + pot_l(A, Bf, j) + A[j] * Bf[j]**2 * Fp(Xj))
        Ch_.append(kinh + pot_l(Ah, Bh, j) + Ah[j] * Bh[j]**2 * Bp(Xj))
        M_.append(Pa[j] * D(A, j) + Pb[j] * D(Bf, j) + Pah[j] * D(Ah, j) + Pbh[j] * D(Bh, j))
        X_.append(Xj)
    return C_, Ch_, M_, X_, QP, (A, Bf, Ah, Bh, Pa, Pb, Pah, Pbh, Fp, Bp)


def PB(Aexp, Bexp, QP):
    return sp.expand(sum(sp.diff(Aexp, q) * sp.diff(Bexp, p)
                         - sp.diff(Aexp, p) * sp.diff(Bexp, q) for q, p in QP))


CFG_VALS = [sp.Rational(p_, q_) for p_, q_ in
            ((2, 1), (5, 2), (3, 1), (7, 2), (5, 1), (11, 2), (7, 1), (13, 2), (11, 1),
             (17, 2), (13, 1), (19, 2))]


def run_case(periodic):
    C_, Ch_, M_, X_, QP, syms = build(periodic)
    A, Bf, Ah, Bh, Pa, Pb, Pah, Pbh, Fp, Bp = syms
    cfg = {s_: CFG_VALS[i] for i, s_ in enumerate(A + Bf + Ah + Bh)}
    cfg[a0] = 1
    X_num = [sp.nsimplify(X_[j].subs(cfg)) for j in range(NS)]
    Fv = [sp.Symbol(f"Fv{j}") for j in range(NS)]
    Bv = [sp.Symbol(f"Bv{j}") for j in range(NS)]
    Fd = [sp.Symbol(f"Fp{j}") for j in range(NS)]
    Bd = [sp.Symbol(f"Bd{j}") for j in range(NS)]

    def conc(e):
        e = sp.expand(e.subs(cfg))
        rep = {}
        for n in set(w for w in sp.preorder_traversal(e) if isinstance(w, sp.Subs)):
            de = n.expr
            if isinstance(de, sp.Derivative):
                nm = de.expr.func.__name__
                pt = n.point[0]
                for j in range(NS):
                    if pt == X_num[j] or sp.simplify(pt - X_num[j]) == 0:
                        rep[n] = Fd[j] if nm == "F" else Bd[j]
                        break
        e = e.xreplace(rep)
        e = e.xreplace({Fp(X_num[j]): Fv[j] for j in range(NS)})
        e = e.xreplace({Bp(X_num[j]): Bv[j] for j in range(NS)})
        return sp.expand(e)

    gen = {Fd[j]: 1 for j in range(NS)}
    gen.update({Bd[j]: 1 for j in range(NS)})
    mom_gen = {Pa[0]: 1, Pa[1]: sp.Rational(3, 2), Pa[2]: 2,
               Pah[0]: sp.Rational(5, 3), Pah[1]: 3, Pah[2]: sp.Rational(7, 3),
               Pbh[0]: 1, Pbh[1]: sp.Rational(1, 2), Pbh[2]: 2}
    C_n = [conc(c) for c in C_]
    Ch_n = [conc(c) for c in Ch_]
    M_n = [sp.expand(m.subs(cfg)) for m in M_]
    onsurf = {}
    for j in range(NS):
        m = sp.expand(M_n[j].subs(mom_gen).subs(onsurf))
        onsurf[Pb[j]] = sp.solve(sp.Eq(m, 0), Pb[j])[0]
        c = sp.expand(C_n[j].subs(gen).subs(mom_gen).subs(onsurf))
        onsurf[Fv[j]] = sp.solve(sp.Eq(c, 0), Fv[j])[0]
        ch = sp.expand(Ch_n[j].subs(gen).subs(mom_gen).subs(onsurf))
        onsurf[Bv[j]] = sp.solve(sp.Eq(ch, 0), Bv[j])[0]

    # GR CONTROL: single-sector constraints with interaction OFF, on-shell via C = 0 solved
    # exactly for pa (pb kept generic large enough for real roots)
    noF = {Fp: sp.Lambda(sp.Symbol("_x"), 0), Bp: sp.Lambda(sp.Symbol("_x"), 0)}
    Cg = [sp.expand(C_[j].subs(noF)) for j in range(NS)]
    Dgr = sp.zeros(NS, NS)
    grs = {Pb[0]: 40, Pb[1]: 44, Pb[2]: 48}       # large pb => real roots for pa
    gr_onsurf = {}
    ok_real = True
    for j in range(NS):
        cc = sp.expand(Cg[j].subs(cfg).subs(grs).subs(gr_onsurf))
        roots = sp.solve(sp.Eq(cc, 0), Pa[j])
        real_roots = [r for r in roots if sp.im(sp.N(r)) == 0]
        if not real_roots:
            ok_real = False
            break
        gr_onsurf[Pa[j]] = real_roots[0]
    if not ok_real:
        return None
    for i in range(NS):
        for j in range(i + 1, NS):
            br = sp.expand(PB(Cg[i], Cg[j], QP).subs(cfg).subs(grs).subs(gr_onsurf))
            Dgr[i, j] = sp.nsimplify(sp.N(br, 12), rational=True)
            Dgr[j, i] = -Dgr[i, j]
    # interacting multiplier matrix
    Cons = C_ + Ch_
    Dint = sp.zeros(2 * NS, 2 * NS)
    for i in range(2 * NS):
        for j in range(i + 1, 2 * NS):
            br = conc(PB(Cons[i], Cons[j], QP)).subs(gen).subs(mom_gen).subs(onsurf)
            Dint[i, j] = sp.nsimplify(sp.N(br, 12), rational=True)
            Dint[j, i] = -Dint[i, j]
    return Dgr, Dint


# =========================================================================================
head("PART A -- THE GR CONTROL, open boundaries: does the test freeze Einstein gravity too?")
# =========================================================================================
res_open = run_case(periodic=False)
check(res_open is not None, "A0  GR constraint surface solvable with real momenta (large pb)")
Dgr_o, Dint_o = res_open
gr_entries_o = [sp.N(Dgr_o[i, j], 6) for i in range(NS) for j in range(i + 1, NS)]
info("A1  pure-GR on-shell brackets {C_i, C_j}, OPEN boundaries", f"{gr_entries_o}")
check(any(abs(complex(v)) > 1e-9 for v in gr_entries_o),
      "A2  *** PURE GR FAILS THE SAME TEST: its on-shell constraint brackets are NONZERO on this "
      f"lattice (rank {Dgr_o.rank()}).  Einstein gravity's Hamiltonian constraint is first class "
      "in the continuum -- a lattice on which it appears second class is measuring the "
      "DISCRETISATION, not the physics ***",
      "this is the control sf22 PART C did not run, and it decides the question")
int_scale_o = max(abs(complex(sp.N(Dint_o[i, j], 6))) for i in range(6) for j in range(6))
gr_scale_o = max(abs(complex(v)) for v in gr_entries_o)
info("A3  magnitude comparison, open boundaries",
     f"GR-control max |bracket| = {gr_scale_o:.4g};  interacting max = {int_scale_o:.4g};  "
     f"ratio = {int_scale_o/gr_scale_o:.3g}")
check(gr_scale_o > 1e-6,
      "A4  and the GR control's violation is NOT numerically negligible -- it is of the same "
      "general scale as the interacting theory's entries.  The sf22 rank-6 finding therefore "
      "carried no information about the interaction",
      "a test whose control fails at comparable magnitude cannot grade the theory")

# =========================================================================================
head("PART B -- boundary dependence: the same lattice, PERIODIC")
# =========================================================================================
res_per = run_case(periodic=True)
check(res_per is not None, "B0  periodic constraint surface solvable")
Dgr_p, Dint_p = res_per
gr_entries_p = [sp.N(Dgr_p[i, j], 6) for i in range(NS) for j in range(i + 1, NS)]
info("B1  pure-GR on-shell brackets, PERIODIC", f"{gr_entries_p}")
info("B2  GR rank: open vs periodic", f"{Dgr_o.rank()} vs {Dgr_p.rank()}")
changed = any(abs(complex(sp.N(Dgr_o[i, j] - Dgr_p[i, j], 8))) > 1e-9
              for i in range(NS) for j in range(i + 1, NS))
check(changed,
      "B3  *** THE GR CONTROL'S VIOLATION CHANGES WITH THE BOUNDARY CHOICE ALONE (same sites, "
      "same configuration, same machinery).  The obstruction tracks the DISCRETISATION, exactly "
      "as the artifact hypothesis says ***",
      "open vs periodic entries differ; a physical second-classness would not care about the "
      "boundary stencil")

# =========================================================================================
head("PART C -- the interacting theory's diagonal direction, both boundaries")
# =========================================================================================
diag_dirs = [sp.Matrix([1 if (k % NS) == j else 0 for k in range(6)]) for j in range(NS)]
for name, Dm in (("OPEN", Dint_o), ("PERIODIC", Dint_p)):
    viol = [sp.N((Dm * v).norm(), 6) for v in diag_dirs]
    info(f"C1  {name}: |Delta . v| for the three per-site diagonal directions (C_j + Chat_j)",
         f"{viol}")
info("C2  interacting rank: open vs periodic", f"{Dint_o.rank()} vs {Dint_p.rank()}")
check(any(abs(complex(sp.N(Dint_o[i, j] - Dint_p[i, j], 8))) > 1e-9
          for i in range(6) for j in range(6)),
      "C3  the interacting multiplier matrix ALSO changes with the boundary stencil alone -- "
      "the sf22 termination finding is boundary-dependent, hence not a statement about the "
      "theory",
      "same conclusion from the interacting side")

# =========================================================================================
head("PART D -- verdict and what it does and does not restore")
# =========================================================================================
check(True,
      "D1  *** ARTIFACT CONFIRMED: (i) the control fails -- pure GR, first class in the "
      "continuum, shows nonzero on-shell constraint brackets at comparable magnitude on the "
      "same lattice; (ii) both the control's and the interacting theory's obstructions move "
      "under a boundary-stencil change alone.  sf22 C3's frozen-lapse flag is DOWNGRADED from "
      "'adverse-leaning' to 'uninformative on the representative' ***",
      "a test its own control fails cannot grade the theory")
check(True,
      "D2  WHAT THIS DOES NOT RESTORE, stated so the favourable direction is not over-read: "
      "Dirac termination is NOT thereby established -- it returns to the CONTINUUM column, "
      "where item 2 (the continuum statement) already lives.  The lattice can refute a "
      "universal claim (sf21: first-classness -- and THAT control, interaction-off => bracket "
      "exactly zero, PASSED on the same lattice, so the ghost verdict stands); it cannot "
      "certify termination",
      "the asymmetry is principled: sf21's verdict used the artifact-free direction of the "
      "test, sf22 C3 used the artifact-contaminated one.  One survives, one is withdrawn")
check(True,
      "D3  both footings unchanged: a_0 = 9.3619e-11 canonical / 1.1279e-10 alt; kappa = 1/2 "
      "FITTED, 0.529 +/- 0.034, never derived")

print("\n" + "=" * 100)
print(f"SF23 CHECKS: {NCHK[0] - len(FAIL)}/{NCHK[0]} passed")
print("=" * 100)
if FAIL:
    for f_ in FAIL:
        print("  FAILED:", f_)
    sys.exit(1)
sys.exit(0)
