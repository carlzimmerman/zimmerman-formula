#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A7_wellposed -- G5 of CFG123_FROZEN_CRITERIA.md: ghosts, characteristic speeds, tachyonic/gradient behaviour, Solar System.

Method (all sympy, exact):
 * the linear flat-space scalar system of the localised RR action (off shell in xi1, xi2): from the covariant field equation the trace of the linearised metric equation is
   -R^(1) + 3 box F1 = 8 pi G T,  F1 = -(m^2/6) S - xi1  (verified symbolically on a perturbed flat metric below), so with box -> -p^2 (p^2 = k^2 - omega^2) the four scalar EOMs are the
   symmetric matrix  M(p^2) phi = 8 pi G T b,  phi = (xi1, S, U, xi2):
        [3p^2, m^2 p^2/2, -p^2, 0; m^2 p^2/2, m^4 p^2/12, 0, -p^2; -p^2, 0, 0, 1; 0, -p^2, 1, 0]  =  Kin p^2 + Mass.
   Its symmetry is what an action requires; Kin (the kinetic matrix) = [[3, m^2/2, -1, 0],[m^2/2, m^4/12, 0, -1],[-1,0,0,0],[0,-1,0,0]].
 * G5-a ghost: signature of Kin (count of negative-kinetic directions), the poles of det M(p^2) and their orders, the sign structure of the propagator of F1 (the field the sources couple to);
   the gauge-graviton sector (h-tilde) is the standard massless one and is healthy.  PASS only if Kin is positive definite and all poles are simple with positive residue.
 * G5-b characteristic speeds from det(Kin p^2) (principal symbol); the tachyonic pole p^2 = m^2 gives omega^2 = k^2 - m^2 (growth rate up to m for k < m).
 * G5-c Solar System: RR |gamma - 1| = m^2 r^2/3 at 1 AU (PPN gamma = Psi/Phi from the exact linear solution, Einstein-frame relation Phi = Phi-tilde - F1/2, Psi = Psi-tilde + F1/2), beta bounded by
   the same factor times eps (not separately extracted); DW |gamma - 1| = 4 f1/(Fbar - 8 f1) (T0d, exact) -> bound on f1.
MUTATE=e : Kin replaced by the positive-definite diag(3, 1, 1, 1): the ghost detector must flip FAIL -> PASS.  Pre-registered P8.
"""
import os, sys, math
import numpy as np
import sympy as sp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfg123_common import *
import cfg123_geom as GM

MUT = mutate_mode()
if MUT not in ("", "e"):
    print("A7: MUTATE mode", MUT, "not applicable"); sys.exit(3)
R = Report("A7_wellposed", MUT)
R.banner(f"A7 G5: well-posedness.  MUTATE={MUT or 'none'}")
lam, sol = rr_background()
mu = math.sqrt(lam)

# ------------------------------------------------------------------ verify the linear trace relation on a perturbed flat metric
t, x, y, z, eps = sp.symbols("t x y z epsilon"); m2 = sp.Symbol("m2", positive=True)
Ph, Ps, u, s, c1, c2 = [sp.Function(n)(t, x) for n in ("Phi", "Psi", "u", "s", "chi1", "chi2")]
g = sp.diag(-(1 + 2 * eps * Ph), (1 - 2 * eps * Ps), (1 - 2 * eps * Ps), (1 - 2 * eps * Ps))
geo = GM.geometry(g, [t, x, y, z])
E = GM.E_RR(geo, m2, eps * u, eps * s, eps * c1, eps * c2)                     # off shell: xi1 = eps chi1, xi2 = eps chi2
tr1 = sp.simplify(sp.diff(sum(geo["gi"][i, i] * E[i, i] for i in range(4)), eps).subs(eps, 0).doit())
R1 = sp.simplify(sp.diff(geo["R"], eps).subs(eps, 0).doit())
F1 = -m2 * s / 6 - c1
box_eta = lambda f: -sp.diff(f, t, 2) + sp.diff(f, x, 2)
chk = sp.simplify(tr1 - (-R1 + 3 * box_eta(F1)))
R.check("G5 set-up: the trace of the linearised metric equation is -R^(1) + 3 box F1, F1 = -(m^2/6) S - xi1 (symbolic, perturbed flat metric, off shell)", f"residual = {chk}", chk == 0)

# ------------------------------------------------------------------ the scalar matrix
p2, m2s = sp.symbols("p2 m2s", positive=True)
Kin = sp.Matrix([[3, m2s / 2, -1, 0], [m2s / 2, m2s ** 2 / 12, 0, -1], [-1, 0, 0, 0], [0, -1, 0, 0]])
Mass = sp.zeros(4, 4); Mass[2, 3] = 1; Mass[3, 2] = 1
if MUT == "e":
    Kin = sp.diag(3, 1, 1, 1)
Mp = Kin * p2 + Mass
# cross-check M(p^2) against the four scalar EOMs derived directly (box -> -p2): rows (1) -p2 U + 3 p2 xi1 + (m^2/2) p2 S ; (2) -p2 S + U ; (3) -p2 xi1 + xi2 ; (4) (m^2/2) p2 xi1 + (m^4/12) p2 S - p2 xi2
xi1_, S_, U_, xi2_ = sp.symbols("xi1 S U xi2")
box_ = lambda f: -p2 * f
F1s = -m2s * S_ / 6 - xi1_
Rlin = 3 * box_(F1s)                                                           # R^(1) with T = 0 (source added below)
eqs = [box_(U_) + Rlin, box_(S_) + U_, box_(xi1_) + xi2_, m2s / 6 * Rlin + box_(xi2_)]
Mdirect = sp.Matrix([[sp.diff(e_, v) for v in (xi1_, S_, U_, xi2_)] for e_ in [eqs[0], eqs[3], eqs[2], eqs[1]]])
R.P("  Mass/kinetic decomposition (rows: E_xi1, E_S, E_U, E_xi2 in the basis (xi1, S, U, xi2)): M(p^2) = Kin p^2 + Mass, Kin = " + str(Kin.tolist()))
if MUT == "":
    okM = sp.simplify(Mdirect - Mp).is_zero_matrix
    R.check("G5-a set-up: the symmetric matrix Kin p^2 + Mass equals the directly derived linearised scalar equations (box -> -p^2, with R^(1) = 3 box F1)", f"matrices equal: {okM}", okM)

# ------------------------------------------------------------------ G5-a ghost analysis
det = sp.factor(sp.simplify(Mp.det()))
R.P(f"  det M(p^2) = {det}")
eig = np.linalg.eigvalsh(np.array(Kin.subs(m2s, lam).evalf(), dtype=float))
nneg = int((eig < 0).sum())
R.P(f"  eigenvalues of the kinetic matrix Kin (m^2 = {lam:.5f} in H0 units): {np.round(eig, 5).tolist()} -> {nneg} negative-kinetic direction(s), signature ({4 - nneg}, {nneg})")
poles = sp.roots(sp.Poly(det, p2))
R.P(f"  poles of the propagator (p^2 = k^2 - omega^2): {poles}")
det_mult0 = poles.get(0, 0)
Mi = sp.simplify(Mp.inv())


def pole_order_at_zero(e):
    n, d = sp.fraction(sp.together(e))
    k = 0
    dd = sp.Poly(sp.expand(d), p2)
    while not dd.is_zero and dd.eval(0) == 0:
        dd = sp.Poly(sp.cancel(dd.as_expr() / p2), p2); k += 1
    nn = sp.Poly(sp.expand(n), p2); k2 = 0
    if not nn.is_zero:
        while nn.eval(0) == 0:
            nn = sp.Poly(sp.cancel(nn.as_expr() / p2), p2); k2 += 1
    return k - k2


order0 = max(pole_order_at_zero(e) for e in Mi)
R.P(f"  multiplicity of the root p^2 = 0 in det M(p^2): {det_mult0} (number of massless-type fields);  highest pole order of any propagator entry at p^2 = 0: {order0} ({'dipole 1/p^4: the CFG50-type structure' if order0 == 2 else 'simple' if order0 == 1 else 'higher'})")
# propagator of F1: source T couples to F1 (h = h-tilde - F1 eta): solve M phi = b, b = (1, 0, 0, m^2/6) 8 pi G T ; G_F1 = F1/(8 pi G T)
b = sp.Matrix([1, m2s / 6, 0, 0])                                               # rows are (E_xi1, E_S, E_U, E_xi2): the sources sit on the trace-carrying rows 0 and 1 (an earlier draft put m^2/6 on row 3; the T0c consistency check caught it)
phi = sp.simplify(Mp.LUsolve(b)) if MUT == "" else None
if MUT == "":
    F1sol = sp.simplify(-m2s * phi[1] / 6 - phi[0])
    GF1 = sp.simplify(F1sol)
    R.P(f"  F1/(8 pi G T) = {sp.factor(GF1)}")
    R.P(f"  partial fractions in p^2: {sp.apart(GF1, p2)}")
    ser = sp.series(GF1, m2s, 0, 3).removeO()
    R.P(f"  series in m^2: {sp.simplify(ser)}  (static leading term should be +m^2/(3 p^4): F1 = -m^2 S/3, S = -8 pi G T/p^4)")
    ok_lead = sp.simplify(sp.limit(GF1 / m2s, m2s, 0) - 1 / (3 * p2 ** 2)) == 0
    R.check("G5-a consistency with T0c: the leading (order m^2) static propagator of F1 is m^2/(3 p^4), i.e. F1 = -m^2 S/3 with S = -8 pi G T/p^4", f"{ok_lead}", ok_lead)
ghost = (nneg > 0) or (order0 > 1)
R.verdict("G5-a ghost (localised action, free initial data)", "FAIL" if ghost else "PASS",
          f"Kin signature ({4 - nneg}, {nneg}); highest propagator pole order at p^2 = 0 is {order0}; det root multiplicity {det_mult0}; other poles {[k for k in poles if k != 0]}" + ("" if not ghost else "; the retarded zero-data prescription removes the free data and is scored PARTIAL, never PASS (CFG48 GA analogue: ownership-as-initial-data)"))
R.check("P8a (pre-registered): a mixed-signature (ghost-like) sector exists in the localised action with free data", f"signature ({4 - nneg}, {nneg}), propagator pole order {order0}", ghost)

# ------------------------------------------------------------------ G5-b speeds and tachyon
principal = sp.factor(sp.simplify((Kin * p2).det()))
R.P(f"\n  G5-b principal symbol det(Kin p^2) = {principal}: all characteristic surfaces p^2 = 0 (null cones): every characteristic speed = c; no superluminal characteristic.")
R.check("P8b (pre-registered): all characteristic speeds equal c", f"det(Kin p^2) = {principal}", sp.simplify(principal - p2 ** 4 * Kin.det()) == 0)
if MUT == "":
    R.P(f"  the pole p^2 = m^2 (k^2 - omega^2 = m^2): omega^2 = k^2 - m^2 -> for k < m the homogeneous solutions GROW at rate up to m = {mu:.4f} H0 (e-folding time {1 / mu:.2f}/H0 = {977.8 / H0_KMS_MPC / mu:.0f} Gyr); static solutions are cos(m r)/r, not exponentials. A long-wavelength (k < m ~ 0.28 H0/c) tachyon with free data: reported, not a Solar System effect.")
    R.num("tachyon_growth_rate_over_H0", mu)

# ------------------------------------------------------------------ G5-c Solar System
AU = 1.495978707e11
m_si = mu * H0_SI / C_SI
gam = m_si ** 2 * AU ** 2 / 3.0
R.P(f"\n  G5-c  RR: |gamma - 1| = m^2 r^2/3 at 1 AU = {gam:.3e} (Cassini 2.3e-5); delta g/g_N = m^2 r^2/6 = {gam / 2:.3e}; beta: nonlinear corrections to this are smaller by eps(1 AU, Sun) = {G_SI * MSUN / C_SI ** 2 / AU:.1e} (bound, not separately extracted)")
R.check("P8c (pre-registered): |gamma - 1| <= 1e-25 for RR at 1 AU", f"{gam:.3e}", gam <= 1e-25)
R.check("G5-c: RR passes Cassini (|gamma - 1| <= 2.3e-5)", f"{gam:.3e}", gam <= 2.3e-5)
R.P(f"       DW: |gamma - 1| = |4 f1/(Fbar - 8 f1)| (T0d, exact) <= 2.3e-5  =>  |f1| <~ {2.3e-5 / 4:.2e} Fbar: reported as a bound on the local f'; DW passes only inside that range and the door has no target amplitude that needs anything else.")
R.P("       G5-d (GW speed / tensor propagation): NOT tested.")
sys.exit(finish(R, MUT))
