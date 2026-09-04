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
Then the surviving field's response is inspected for omega-dependence and for continuity as X -> 0.  This decides
the scoped gate-7 and gate-9 diagnostics.  It does NOT determine alpha_1, alpha_2, or alpha_3: those require a full
boosted post-Newtonian metric solution and standard-PPN gauge matching, neither of which this reduction contains.
Checks can fail.  Mutation controls reproduce the repo's Lorentz-branch ghost, the fixed-background 4x4 result,
the inconsistent unscaled source, and a faster-switching source whose off-zero response loses finite path memory.
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


def derive_ppn_provenance_audit():
    """Return what this reduced calculation supplies and what PPN still needs."""

    provided_outputs = frozenset({
        "u_frame_auxiliary_dirac_chain",
        "static_scalar_response",
        "omega_independence",
    })
    required_outputs = frozenset({
        "boosted_g00_through_required_PN_order",
        "boosted_g0i_through_required_PN_order",
        "boosted_gij_through_required_PN_order",
        "all_constraint_and_multiplier_backreaction",
        "moving_matter_solution",
        "standard_PPN_gauge_map",
        "PPN_coefficient_matching",
    })
    missing_outputs = required_outputs - provided_outputs
    boosted_ppn_complete = len(missing_outputs) == 0
    status = "COMPUTED" if boosted_ppn_complete else "UNCOMPUTED"
    return {
        "provided_outputs": provided_outputs,
        "required_outputs": required_outputs,
        "missing_outputs": missing_outputs,
        "boosted_ppn_complete": boosted_ppn_complete,
        "boosted_ppn_status": status,
        "alpha_1": status,
        "alpha_2": status,
        "alpha_3": status,
    }


def derive_zero_field_response_limit(source_power=1):
    """Derive the X -> 0+ response for J=X**source_power*Jtilde.

    The exact X=0 equation must be evaluated before cancelling X.  Two source
    paths differing by X**source_power*Delta_Jtilde reach the same zero source.
    Their finite-X chi solutions diagnose whether that common endpoint selects
    a unique limiting response.
    """

    if not isinstance(source_power, int) or source_power < 1:
        raise ValueError("source_power must be a positive integer")

    X_response = sp.Symbol("X_response", positive=True)
    k_response = sp.Symbol("k_response", positive=True)
    chi_response = sp.Symbol("chi_response", real=True)
    Jtilde_response = sp.Symbol("Jtilde_response", real=True)
    delta_Jtilde = sp.Symbol("Delta_Jtilde", nonzero=True, real=True)

    source = X_response**source_power * Jtilde_response
    lambda_equation = sp.expand(
        -X_response * k_response**2 * chi_response - source
    )
    finite_X_solution = sp.solve(lambda_equation, chi_response)[0]
    finite_X_response = sp.simplify(
        sp.diff(finite_X_solution, Jtilde_response)
    )

    exact_zero_equation = sp.simplify(lambda_equation.subs(X_response, 0))
    exact_zero_chi_coefficient = sp.simplify(
        sp.diff(exact_zero_equation, chi_response)
    )
    chi_selected_at_exact_zero = exact_zero_chi_coefficient != 0

    source_path_gap = X_response**source_power * delta_Jtilde
    field_path_gap = sp.simplify(
        finite_X_solution.subs(
            Jtilde_response, Jtilde_response + delta_Jtilde
        )
        - finite_X_solution
    )
    source_path_gap_limit = sp.limit(source_path_gap, X_response, 0, dir="+")
    field_path_gap_limit = sp.limit(field_path_gap, X_response, 0, dir="+")
    finite_X_response_limit = sp.limit(
        finite_X_response, X_response, 0, dir="+"
    )
    path_dependent_zero_field_limit = bool(
        source_path_gap_limit == 0
        and field_path_gap_limit != 0
        and not chi_selected_at_exact_zero
    )

    return {
        "symbols": {
            "X": X_response,
            "k": k_response,
            "chi": chi_response,
            "Jtilde": Jtilde_response,
            "delta_Jtilde": delta_Jtilde,
        },
        "source_power": source_power,
        "source": source,
        "lambda_equation": lambda_equation,
        "finite_X_solution": finite_X_solution,
        "finite_X_response": finite_X_response,
        "finite_X_response_limit": finite_X_response_limit,
        "exact_zero_equation": exact_zero_equation,
        "exact_zero_chi_coefficient": exact_zero_chi_coefficient,
        "chi_selected_at_exact_zero": chi_selected_at_exact_zero,
        "source_path_gap": source_path_gap,
        "source_path_gap_limit": source_path_gap_limit,
        "field_path_gap": field_path_gap,
        "field_path_gap_limit": field_path_gap_limit,
        "path_dependent_zero_field_limit": path_dependent_zero_field_limit,
    }

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
ck("D6 with J = X J~ the constraint count is consistent on BOTH branches: for X != 0 it is the four second-class constraints of D2 (det C unchanged), for X = 0 every X-dependent constraint vanishes identically and the sector is pure gauge.  This establishes zero auxiliary degrees of freedom on each branch; it does NOT establish a continuous zero-field response",
   sp.simplify(cmatrix(cons_tilde).det() - X**4*k**8) == 0 and all(sp.simplify(c.subs(X, 0)) in (0, plam, pchi) for c in cons_tilde),
   "DOF(X!=0) = 0 second-class; DOF(X=0) = 0 first-class; response limit tested next")

P(""); P("="*116); P("4.  WHAT THE SURVIVING FIELD IS -- and this decides the door"); P("="*116)
info("On the X != 0 branch the on-shell chi is fixed by the secondary constraint with NO reference to time:")
chi_os = sp.simplify(chi_sol.subs(J, X*Jt))
info(f"    chi = {chi_os}")
info("Its response to the source is a pure 1/k^2 with NO omega anywhere.  That is the definition of an instantaneous,")
info("elliptic channel: the MOND potential at time t is determined by the source at the SAME t everywhere in space, in")
info("the u-frame.  The projector's field-dependence does not change this -- it only switches the channel off at X = 0.")
resp = sp.simplify(sp.diff(chi_os, Jt))
ck("D7 (GATE 7, for this candidate reduction) the physical MOND channel is omega-INDEPENDENT: d chi / d J~ = -1/k^2 with no frequency dependence, so it is instantaneous.  This fails the requested 'no unacceptable instantaneous physical channel' gate if chi is the MOND mediator; it does not determine a PPN parameter",
   sp.simplify(sp.diff(resp, w)) == 0 and sp.simplify(resp + 1/k**2) == 0, f"response = {resp}, d/d(omega) = 0")
ppn_audit = derive_ppn_provenance_audit()
info(f"boosted PPN status = {ppn_audit['boosted_ppn_status']}; alpha_1 = {ppn_audit['alpha_1']}, alpha_2 = {ppn_audit['alpha_2']}, alpha_3 = {ppn_audit['alpha_3']}")
info(f"missing PPN outputs = {sorted(ppn_audit['missing_outputs'])}")
ck("D8 (GATE 4 PROVENANCE) alpha_1, alpha_2, and alpha_3 are UNCOMPUTED: this u-frame auxiliary Dirac chain and its static 1/k^2 response contain none of the boosted metric components, moving-matter solution, constraint backreaction, standard-PPN gauge map, or coefficient matching required to derive them.  Instantaneous response alone is not alpha_3",
   not ppn_audit["boosted_ppn_complete"]
   and ppn_audit["missing_outputs"] == ppn_audit["required_outputs"]
   and len({ppn_audit[name] for name in ("alpha_1", "alpha_2", "alpha_3")}) == 1
   and ppn_audit["alpha_3"] == "UNCOMPUTED",
   "full boosted PPN solve remains unavoidable")

zero_limit = derive_zero_field_response_limit(source_power=1)
info(f"finite-X equation after J=X J~: {zero_limit['lambda_equation']} = 0")
info(f"exact X=0 equation before cancellation: {zero_limit['exact_zero_equation']} = 0  (chi arbitrary)")
info(f"X->0+ response: {zero_limit['finite_X_response_limit']}")
info(f"two paths with source gap -> {zero_limit['source_path_gap_limit']} retain field gap -> {zero_limit['field_path_gap_limit']}")
ck("D9 (GATE 9) the zero-field limit is not controlled by this ansatz: at exact X=0 the lambda equation is 0=0 and selects no chi, while for every X>0 cancelling X gives chi=-J~/k^2.  Distinct J~ paths all approach the same (X,J)=(0,0) but retain distinct finite chi limits, so the solution map is path-dependent/nonunique",
   zero_limit["exact_zero_equation"] == 0
   and zero_limit["exact_zero_chi_coefficient"] == 0
   and not zero_limit["chi_selected_at_exact_zero"]
   and zero_limit["source_path_gap_limit"] == 0
   and zero_limit["field_path_gap_limit"] != 0
   and zero_limit["path_dependent_zero_field_limit"],
   f"Delta source -> {zero_limit['source_path_gap_limit']}; Delta chi -> {zero_limit['field_path_gap_limit']}")

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
   sp.simplify(cons[2].subs(X, 0)) == -J and sp.diff(cons[2].subs(X, 0), J) == -1, "phi3(X=0) = -J must vanish for arbitrary J: impossible")
# (d) faster source switch-off removes the finite path memory
faster_source = derive_zero_field_response_limit(source_power=2)
ck("M4 mutation (replace J=X J~ by J=X^2 J~): the X>0 solution becomes chi=-X J~/k^2, so both its response and the difference between two J~ paths tend to zero.  This negative control would FAIL the D9 finite-path-memory predicate and proves that D9 is sensitive to the load-bearing linear source scaling",
   zero_limit["path_dependent_zero_field_limit"]
   and not faster_source["path_dependent_zero_field_limit"]
   and faster_source["finite_X_response_limit"] == 0
   and faster_source["field_path_gap_limit"] == 0,
   f"linear scaling Delta chi -> {zero_limit['field_path_gap_limit']}; quadratic scaling Delta chi -> {faster_source['field_path_gap_limit']}")

P(""); P("="*116); P("VERDICT"); P("="*116)
P("  The specified smoothly-vanishing spatial projector H = X(g+uu) is run through the reduced u-frame Dirac")
P("  algorithm on both branches.  It is algebraically CONSISTENT: zero auxiliary degrees of")
P("  freedom for every X, second class off zero field, first class (pure gauge) at zero field, with the single")
P("  requirement that the MOND source vanish with the projector (J = X J~).  The bifurcation changes the CLASS of the")
P("  constraints, not the count.  That count does not cure the response singularity at the rank-changing point.")
P("  For X>0 the physical MOND response is chi = -J~/k^2 with no frequency dependence, so this specified mechanism")
P("  fails the strict no-instantaneous-channel gate 7.  At exact X=0 its equation vanishes, while different J~ paths")
P("  approaching the same zero source retain different finite chi limits; this specified mechanism also fails the")
P("  controlled-zero-field gate 9 unless a further action-derived prescription removes that path dependence.")
P("  alpha_1 = UNCOMPUTED; alpha_2 = UNCOMPUTED; alpha_3 = UNCOMPUTED.  A full boosted metric/matter solution and")
P("  standard-PPN gauge matching are still required.  Instantaneous response alone supplies no PPN coefficient.")
P("  Scope: candidate-specific u-frame, k!=0 auxiliary reduction.  This is not a theorem closing every metric-only")
P("  projector and not a full covariant-action Dirac/PPN calculation.  The broader nonlocal door remains OPEN.")

if __name__ == "__main__":
    sys.exit(ck.done())
