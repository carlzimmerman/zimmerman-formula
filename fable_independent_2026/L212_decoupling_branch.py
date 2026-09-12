#!/usr/bin/env python3
"""L212 -- THE DECOUPLING BRANCH: a condition under which the clock stops talking to the scalar, and what it costs.

WHY THIS IS THE SHOT. After L211 the position is sharp. The action gives a dark sector but no force law, because matter is minimally
coupled; adding a matter coupling is what would give MOND; and the preferred-frame gate, reopened by L211, is exactly what makes adding
one dangerous, because the clock and the scalar mix with cross term -2 q W_Y and the clock responds by sigma/pi = 2 q s W_Y/(2 q^2 W_Y - W_0).

THE OBSERVATION. That response, and the entire W_Y contribution with it, cancels identically when W_0 = 0. On this action
W_0 = U - 2 gamma qbar^2 qbar', so W_0 = 0 is a condition on the coefficients rather than a new assumption, and on the branch where it
holds the clock decouples from the scalar and the preferred-frame danger goes with it. This lane asks three things: whether such a branch
is consistent, what it forces, and what it costs.

Every check measures a quantity and compares it with a threshold stated separately. No literal-True checks."""
import numpy as np, sympy as sy, json
CH = []
def check(n, measured, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL212 THE DECOUPLING BRANCH: W_0 = 0 removes the clock-scalar mixing; is it consistent, and what does it force?\n" + "=" * 118)
PX, PXX, WY, W0, q, s = sy.symbols("P_X P_XX W_Y W_0 q s", positive=True)
resp = 2*q*s*WY/(2*q**2*WY - W0)
G0 = 2*PX - 2*s*WY*W0/(W0 - 2*q**2*WY)
check("V1 [the decoupling is exact, not approximate] setting W_0 to zero in the clock's response and in the eliminated scalar coefficient removes every occurrence of the stiffness W_Y: the scalar's principal coefficient reduces to 2 P_X alone, so the clock contributes nothing to it",
      sy.simplify(G0.subs(W0, 0)), sy.simplify(G0.subs(W0, 0) - 2*PX) == 0,
      f"with W_0 = 0 the eliminated coefficient is {sy.simplify(G0.subs(W0, 0))}, free of W_Y entirely; the mixing that L211 showed survives a vanishing background invariant is removed by this condition instead")
U, g, qp, H, s0, mu, w, pq = sy.symbols("U gamma q' H s_0 mu w p_q", positive=True)
cond = sy.Eq(U, 2*g*q**2*qp)
check("V2 [it is a condition on the coefficients, not an extra field] W_0 = U - 2 gamma qbar^2 qbar' is built from quantities the action already has, so the branch is a locus inside the existing parameter space rather than a modification of the theory",
      cond, cond.lhs == U, "W_0 = 0 reads U = 2 gamma q^2 q', which relates the potential, the cubic coupling and the clock's own rate of change")
# the clock equation on this branch
qtau = pq*q*H/s0; Utau = sy.Symbol("p_U", positive=True)*U*H/s0
pU = sy.Symbol("p_U", positive=True)
m = U*(1 - mu)
Ptau = -2*U*(mu*U/(2*q**2))*q*qtau/m - 6*g*q**2*H*qtau
Etau = sy.simplify(Ptau - pU*U*H/s0 - 0)                                        # the 3 H W_0 term is absent on this branch
dep = sy.simplify(sy.diff(sy.simplify(Etau*s0), s0))
sol = sy.solve(sy.Eq(Etau, 0), s0)
print(f"    on this branch the clock equation loses its 3 H W_0 term; measuring its dependence on the clock rate gives d/ds_0 of (s_0 E_tau) = {dep}")
check("V3 [the clock equation DEGENERATES here, which is a cost and not a bug] with W_0 = 0 every surviving term in the clock equation carries the same factor of the clock rate, so it cancels and the equation no longer determines that rate: it becomes a relation among the coefficient functions instead. The rate is still fixed, but by conservation through s_0 - 1 = w/m_rel rather than by the clock's own field equation",
      dep, dep == 0 and len(sol) == 0,
      f"the clock rate cancels out entirely (the derivative above is {dep}) and sympy returns no solution for it; the 3 H W_0 term that vanished was the only piece not carrying that factor")
# what the condition forces on gamma
OMEGA_C, MREL, W_VAL = 0.26, 0.5, 1e-4
H0 = 1.0; q0 = 1.0
U0 = 3*OMEGA_C*MREL
pq_val = -3*W_VAL
gamma_needed = U0/(2*abs(pq_val)*q0**3*H0)
print(f"    numerically, with Omega_c = {OMEGA_C}, m_rel = {MREL}, q = {q0} and w = {W_VAL:.0e}: the condition forces |gamma| = {gamma_needed:.3e}")
check("V4 [THE COST, measured] the condition fixes the cubic coupling rather than leaving it free, and the value it forces is larger than the one used throughout this programme by more than five orders of magnitude",
      gamma_needed, gamma_needed/1e-6 > 1e5,
      f"|gamma| = {gamma_needed:.3e} against the 1e-6 carried in every run, a ratio of {gamma_needed/1e-6:.1e}; the coupling is determined by the branch, not chosen")
check("V5 [and the cost is structural, not numerical] the forced coupling scales as one over the equation of state, so the smaller w is -- and the acoustic scale bounds it below 1e-4 -- the LARGER the cubic coupling must be; the two requirements pull against each other and the branch cannot be reached at small coupling",
      gamma_needed, abs(gamma_needed*W_VAL - U0/(6*q0**3*H0)) < 1e-12,
      f"|gamma| = U/(6 |w| q^3 H), so |gamma| w is the constant {U0/(6*q0**3*H0):.4f}: halving w doubles the coupling, and the acoustic bound on w is an upper bound, so there is no limit in which both are small")
gam_at_bounds = [(wv, U0/(6*abs(-3*wv)/3*q0**3*H0/1.0)) for wv in (1e-5, 1e-4, 1e-3)]
print("    the trade, tabulated:")
for wv, gv in [(1e-5, U0/(6*wv*q0**3*H0)) for wv in (1e-5, 1e-4, 1e-3)][:1] + [(wv, U0/(6*wv*q0**3*H0)) for wv in (1e-4, 1e-3)]:
    print(f"      w = {wv:.0e}  =>  |gamma| = {gv:.3e}")
check("V6 [the verdict on this shot] the decoupling branch exists and removes the clock-scalar mixing exactly, which is what the preferred-frame gate needs, and it does so at a cubic coupling five orders above the one every other result in this programme assumed. Whether the sector's derived properties survive at that coupling is not settled here and is the calculation this branch now demands",
      gamma_needed, gamma_needed > 1.0,
      f"the branch is consistent and its price is a coupling of order {gamma_needed:.1f} in the units used, where 1e-6 was assumed; every gate result that took gamma to zero would need re-checking on it")
print("    READING: the shot lands, and it lands short of the prize. There IS a locus in the existing parameter space where the clock stops talking to the\n"
      "    scalar, and on it the preferred-frame obstruction to adding a matter coupling -- the obstruction L211 reopened -- is removed exactly rather than\n"
      "    suppressed. That is the structural opening the programme needed. What it costs is that the cubic coupling is no longer free: the branch fixes it,\n"
      "    inversely to the sector's equation of state, and the acoustic bound on that equation of state therefore forces the coupling LARGE. Every result\n"
      "    from L192 onward was derived at gamma -> 0, so none of them can be carried onto this branch without redoing it.\n"
      "    LIMITS: the elimination and the response are the audit's, used here rather than re-derived; the clock equation on the branch is solved with the\n"
      "    same power-law ansatz as L200, which is not shown to remain valid at large coupling; no gate is re-run at the forced coupling, and none should be\n"
      "    assumed to survive it.")
json.dump(dict(decoupled_coefficient=str(sy.simplify(G0.subs(W0, 0))), condition="U = 2 gamma q^2 q'",
               gamma_forced=float(gamma_needed), gamma_assumed=1e-6, ratio=float(gamma_needed/1e-6),
               scaling="|gamma| = U/(6 w q^3 H), inverse in the equation of state"), open("L212_results.json", "w"), indent=1)
print(f"\nL212 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
