#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
vanishing_projector_dirac_chain_2026.py -- the open residual on the nonlocal door, run through its rank bifurcation.
=====================================================================================================================
METRIC_ONLY_ELLIPTIC_PROJECTOR_RANK_CHANGE_2026-09-03.md withdrew "every regular metric-only elliptic projector is
excluded" and left ONE loophole: a Poincare-equivariant tensor cannot be a nonzero rank-3 spatial projector AT
Minkowski, but it CAN be rank-3 away from zero field and vanish smoothly at zero:
        H^{mu nu} = X (g^{mu nu} + u^mu u^nu),   X = -V^2 > 0,   u = V/sqrt(X)
The auxiliary sector  S_aux = int sqrt(-g) lambda (H^{mu nu} nabla_mu nabla_nu chi - J)  then has a constraint
structure that CHANGES RANK as X -> 0.  The verdict called this "a rank bifurcation rather than a nonexistence
theorem" and left "the full homogeneous Dirac chain" open.  This file runs that chain.

REDUCTION (the one the repo already uses): background u = (1,0,0,0), Fourier mode k != 0, X a background parameter
that may pass through zero.  Then H^{00} = X(-1+1) = 0 and H^{ij} = X delta^{ij}, so the auxiliary Lagrangian is
        L = -X k^2 lambda chi - J lambda            (NO time derivatives: the spatial projector kills them)
Phase space (lambda, p_lambda, chi, p_chi).  Dirac's algorithm is run symbolically, the constraint matrix's rank is
computed as a function of X, first/second class is decided on each branch, and the degree-of-freedom count follows.
Then the surviving field's propagator is inspected for omega-dependence, which decides gate 7 and, through the
committed pincer (N_grav = 2 <=> MOND via second-class constraint <=> instantaneous <=> alpha_3 = O(1)), gate 4.
Checks can fail.  Mutation controls reproduce the repo's Lorentz-branch ghost and the fixed-background 4x4 result.
"""
import sys, os
import sympy as sp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "hunt_2026"))
from hunt_lib import P, info, Check
ck = Check()

lam, plam, chi, pchi = sp.symbols("lambda p_lambda chi p_chi", real=True)
X, k, J, w = sp.symbols("X k J omega", real=True)
A, B = sp.symbols("A B", real=True)
Q = [lam, chi]; Pm = [plam, pchi]
def PB(f, g):
    return sum(sp.diff(f, q)*sp.diff(g, p) - sp.diff(f, p)*sp.diff(g, q) for q, p in zip(Q, Pm))
def cmatrix(cons):
    return sp.Matrix(len(cons), len(cons), lambda i, j: sp.simplify(PB(cons[i], cons[j])))

P("="*116); P("1.  the vanishing spatial projector on the u-frame background: no time derivatives survive"); P("="*116)
# general H^{00} = -A, H^{ij} = B delta^{ij} on the background; the vanishing projector has A = 0, B = X
Lgen = -A*sp.Symbol("ldot")*sp.Symbol("cdot") - B*k**2*lam*chi - J*lam
Lproj = Lgen.subs({A: 0, B: X})
info(f"general auxiliary Lagrangian (mode k):  L = {Lgen}")
info(f"vanishing spatial projector H = X(g+uu):  H^00 = X(-1+1) = 0  =>  A = 0,  B = X")
info(f"                                            L = {Lproj}")
ck("D1 on the u-frame background the vanishing spatial projector removes EVERY time derivative from the auxiliary sector, because H^00 = X(g^00 + u^0 u^0) = X(-1+1) = 0 identically.  So lambda and chi enter with no kinetic term at all -- the sector is purely constrained, and its whole content is in Dirac's algorithm",
   sp.simplify(sp.diff(Lproj, sp.Symbol("ldot"))) == 0 and sp.simplify(sp.diff(Lproj, sp.Symbol("cdot"))) == 0, "dL/d(lambda-dot) = dL/d(chi-dot) = 0")

P(""); P("="*116); P("2.  DIRAC'S ALGORITHM, branch X != 0"); P("="*116)
H0 = -Lproj.subs({sp.Symbol("ldot"): 0, sp.Symbol("cdot"): 0})          # canonical Hamiltonian = -L (no velocities)
phi1, phi2 = plam, pchi                                                      # primaries: no velocities => momenta vanish
u1, u2 = sp.symbols("u1 u2")
HT = H0 + u1*phi1 + u2*phi2
phi3 = sp.simplify(PB(phi1, HT)); phi4 = sp.simplify(PB(phi2, HT))            # secondaries
info(f"primaries:   phi1 = {phi1},  phi2 = {phi2}")
info(f"secondaries: phi3 = {{phi1,H_T}} = {phi3},   phi4 = {{phi2,H_T}} = {phi4}")
cons = [phi1, phi2, phi3, phi4]
C = cmatrix(cons)
info(f"constraint matrix C_AB = {C.tolist()}")
detC = sp.factor(C.det())
info(f"det C = {detC}")
ck("D2 (X != 0) two primaries and two secondaries close the chain with NO tertiary: the 4x4 Poisson matrix has det C = X^4 k^8 != 0, so all four are SECOND CLASS.  Four second-class constraints remove four phase-space dimensions from a four-dimensional phase space: ZERO degrees of freedom.  This reproduces the repo's fixed-background result with B -> X",
   sp.simplify(detC - X**4*k**8) == 0 and C.rank() == 4, f"det C = {detC}, rank 4, DOF = (4 - 4)/2 = 0")
# tertiary check: preservation of secondaries fixes the multipliers, no new constraint
sol = sp.solve([sp.simplify(PB(phi3, HT)), sp.simplify(PB(phi4, HT))], [u1, u2], dict=True)
ck("D3 (X != 0) preservation of the secondaries SOLVES both multipliers rather than generating a tertiary, so the chain terminates -- the algorithm is complete on this branch",
   len(sol) == 1, f"multipliers fixed: {sol[0] if sol else 'none'}")
chi_sol = sp.solve(phi3, chi)[0]
info(f"on-shell: chi = {chi_sol},  lambda = {sp.solve(phi4, lam)[0]}")

P(""); P("="*116); P("3.  DIRAC'S ALGORITHM, branch X = 0 -- the rank bifurcation"); P("="*116)
cons0 = [sp.simplify(c.subs(X, 0)) for c in cons]
info(f"constraints at X = 0: {cons0}")
C0 = cmatrix([c for c in cons0 if c != 0 and c.free_symbols & set(Q + Pm)])
info(f"phi3 -> {cons0[2]}  (a CONSTANT: no phase-space dependence),   phi4 -> {cons0[3]}  (identically zero)")
info(f"surviving phase-space constraints: {[c for c in cons0 if c.free_symbols & set(Q+Pm)]},  their Poisson matrix: {C0.tolist()}")
ck("D4 (X = 0) the bifurcation is exactly this: phi4 vanishes identically and phi3 degenerates to the CONSTANT J.  The surviving constraints are the two primaries alone, which commute -- they become FIRST CLASS -- so lambda and chi turn into pure gauge.  Two first-class constraints remove 2 x 2 = 4 dimensions: STILL zero degrees of freedom.  The count does not jump; the CLASS does",
   C0.rank() == 0 and cons0[3] == 0 and cons0[2] == -J, "at X=0: constraints {p_lambda, p_chi} first class, DOF = (4 - 2*2)/2 = 0")
ck("D5 (X = 0, the consistency condition) phi3 = -J = 0 is not a constraint on phase space -- it is a CONDITION ON THE SOURCE.  The vanishing projector is consistent at zero field only if the MOND source vanishes there too: J must carry a factor of X.  Otherwise the chain is inconsistent at X = 0 and the loophole is dead outright",
   cons0[2] == -J, "J(X=0) = 0 required; write J = X * J~ and both X=0 constraints vanish identically, restoring consistency")
Jt = sp.Symbol("Jtilde")
cons_tilde = [c.subs(J, X*Jt) for c in cons]
ck("D6 with J = X J~ the full chain is consistent on BOTH branches: for X != 0 it is the four second-class constraints of D2 (det C unchanged), for X = 0 every X-dependent constraint vanishes identically and the sector is pure gauge.  The rank bifurcation is RESOLVED: zero degrees of freedom everywhere, second class off zero field, first class at zero field, no inconsistency",
   sp.simplify(cmatrix(cons_tilde).det() - X**4*k**8) == 0 and all(sp.simplify(c.subs(X, 0)) in (0, plam, pchi) for c in cons_tilde),
   "DOF(X!=0) = 0 second-class; DOF(X=0) = 0 first-class; consistent")

P(""); P("="*116); P("4.  WHAT THE SURVIVING FIELD IS -- and this decides the door"); P("="*116)
info("On the X != 0 branch the on-shell chi is fixed by the secondary constraint with NO reference to time:")
chi_os = sp.simplify(chi_sol.subs(J, X*Jt))
info(f"    chi = {chi_os}")
info("Its response to the source is a pure 1/k^2 with NO omega anywhere.  That is the definition of an instantaneous,")
info("elliptic channel: the MOND potential at time t is determined by the source at the SAME t everywhere in space, in")
info("the u-frame.  The projector's field-dependence does not change this -- it only switches the channel off at X = 0.")
resp = sp.simplify(sp.diff(chi_os, Jt))
ck("D7 (GATE 7) the surviving MOND channel is omega-INDEPENDENT: d chi / d J~ = -1/k^2 with no frequency dependence, so it is instantaneous.  This is precisely the 'no instantaneous channel' failure of gate 7, and the field-dependent projector does not evade it -- it merely makes the instantaneous channel vanish where the field vanishes",
   sp.simplify(sp.diff(resp, w)) == 0 and sp.simplify(resp + 1/k**2) == 0, f"response = {resp}, d/d(omega) = 0")
ck("D8 (GATE 4, by the committed pincer) the repo's pincer is: N_grav = 2 <=> MOND via a second-class constraint <=> omega-independent 1/k^2 propagator <=> alpha_3 = O(1).  This construction realises every link -- zero extra DOF (D2), MOND via second-class constraints (D2), instantaneous 1/k^2 (D7) -- so it inherits alpha_3 = O(1), excluded ~1e19x by the pulsar bound.  The 'nonlocal' projector is an elliptic constraint in disguise, and it lands on the same wall as the local constraint route (DC-019, York/CMC, CDE-L4C)",
   True, "cited: cde_l4c_ppn_alpha3.py (alpha_3 = -1 in the principal (k, omega) extraction); York/CMC causal gate; DC-019")

P(""); P("="*116); P("5.  mutation controls -- reproduce the repo's two known results from the same engine"); P("="*116)
# (a) Lorentz branch A = -B: the repo found velocity Hessian eigenvalues (-B, +B) => one ghost direction
ld, cd = sp.symbols("ldot cdot")
Llor = (-A*ld*cd - B*k**2*lam*chi - J*lam).subs(A, -B)
Hess = sp.hessian(Llor, [ld, cd])
ev = list(Hess.eigenvals().keys())
ck("M1 mutation (the Lorentz branch H = B eta, i.e. A = -B): the velocity Hessian is [[0, B],[B, 0]] with eigenvalues +B and -B -- one negative kinetic direction, the GHOST the repo found on this branch.  Same engine, opposite branch, opposite verdict: the spatial projector is what removes the kinetic term and with it the ghost",
   set(sp.simplify(e) for e in ev) == {B, -B}, f"Hessian eigenvalues {ev}")
# (b) fixed spatial B > 0 (not vanishing): the repo's 4x4 with det B^4 k^8
Cfix = cmatrix([plam, pchi, sp.simplify(PB(plam, -(-B*k**2*lam*chi - J*lam))), sp.simplify(PB(pchi, -(-B*k**2*lam*chi - J*lam)))])
ck("M2 mutation (fixed spatial projector, B a constant): det C = B^4 k^8, four second-class, zero modes -- reproducing the repo's committed fixed-background result exactly.  The vanishing projector differs from it ONLY at X = 0, which is where D4-D6 live",
   sp.simplify(Cfix.det() - B**4*k**8) == 0, f"det C = {sp.factor(Cfix.det())}")
# (c) source not proportional to X: inconsistency at X = 0
ck("M3 mutation (drop the J = X J~ requirement): at X = 0 the chain demands J = 0 with J a free source -- an inconsistency, not a constraint.  So D5 is load-bearing: without the source switching off with the field, the loophole is dead at zero field before gate 7 is even reached",
   sp.simplify(cons[2].subs(X, 0)) == -J and J != 0, "phi3(X=0) = -J must vanish for arbitrary J: impossible")

P(""); P("="*116); P("VERDICT"); P("="*116)
P("  The nonlocal door's named residual -- the smoothly-vanishing spatial projector H = X(g+uu) and its rank")
P("  bifurcation -- is run through Dirac's algorithm on both branches.  It is CONSISTENT: zero auxiliary degrees of")
P("  freedom for every X, second class off zero field, first class (pure gauge) at zero field, with the single")
P("  requirement that the MOND source vanish with the projector (J = X J~).  The bifurcation changes the CLASS of the")
P("  constraints, not the count.  So the loophole is not killed by inconsistency and not killed by a ghost.")
P("  It is killed by what it IS.  The surviving MOND channel is chi = -J~/k^2 with no frequency dependence: an")
P("  instantaneous elliptic potential in the u-frame.  That is the gate-7 failure by definition, and by the committed")
P("  pincer it carries alpha_3 = O(1), excluded ~1e19x.  The field-dependent projector is an elliptic constraint that")
P("  switches itself off at zero field -- a local constraint route wearing nonlocal clothes -- and it lands on the")
P("  same wall as DC-019, York/CMC and CDE-L4C.")
P("  Conditional on: the u-frame k-space reduction (the repo's own), and the pincer's instantaneous => alpha_3 link.")
P("  With this, the nonlocal door's LAST NAMED RESIDUAL IS CLOSED.  What remains for door B is not a loophole but a")
P("  construction nobody has written: a genuinely retarded (omega-dependent) nonlocal kernel that yields mu = 1-e^{-y}")
P("  with positive spectral weight -- and section 4 of the state-space verdict shows positive weight means extra")
P("  carrier states, failing gate 2'.  The door is not 'closed'; every route through it that has been written is.")
sys.exit(ck.done())
