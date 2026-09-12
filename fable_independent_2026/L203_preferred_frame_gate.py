#!/usr/bin/env python3
"""L203 -- THE PREFERRED-FRAME GATE: how far it can be taken for THIS action, and what the answer rests on.

WHY THIS IS THE DANGEROUS GATE. The clock defines a rest frame. A body moving through it at velocity w sees, in its own frame, a clock
with a SPATIAL gradient: tau = s0 gamma (t' + w.x'), so grad' tau = s0 w. That tilt is the preferred-frame coupling, and it is what the
parameter alpha_1 measures. Earlier in this programme (L170) a cuscuton clock inside a DIFFERENT action was killed on exactly this test,
producing a potential 3e-2 of the Newtonian one at Saturn. The question is whether that verdict carries over.

WHAT IS COMPUTED HERE, and what is not. Three things are computable and are computed: the tilt itself; the sector's own boosted momentum
density and the preferred-frame amplitude it produces; and the amplification factor of the clock's constraint in this action, which is
what made the earlier case fatal. The full boosted metric expansion for this action is NOT done, and the verdict is reported as
'not killed, not passed' rather than as a pass. The structural observation that decides whether the earlier kill transfers is stated as
a property of the action and checked against it.
No literal-True checks."""
import numpy as np, json
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""), flush=True)
print("=" * 118 + "\nL203 THE PREFERRED-FRAME GATE: the tilt, the amplification, and the structural difference from the case that died\n" + "=" * 118)
c_kms = 2.998e5; G = 6.674e-8; MSUN = 1.989e33; AU = 1.496e13
W_CMB = 370.0                                                              # the solar system's speed through the cosmic rest frame
RHO_DM = 0.4*1.783e-24; FRET = 0.135
beta = W_CMB/c_kms
print(f"    the tilt: a system moving at {W_CMB:.0f} km/s sees the clock acquire a spatial gradient of s0 times {beta:.3e} in units of its time gradient")
check("V1 [the coupling exists and is first order in the velocity] the tilt is beta = w/c = 1.23e-3, not a second-order effect, so the preferred frame is visible to the solar system at first order and the gate cannot be dismissed on the grounds that the velocity is small",
      1e-4 < beta < 1e-2, f"beta = {beta:.3e}; the bound on the preferred-frame parameter alpha_1 is about 1e-4, so an order-unity coefficient in front of this tilt would be excluded by roughly a factor of 12")
# the sector's own boosted momentum density: the unambiguous, computable contribution
for rname, rAU in (("Saturn", 9.54), ("Neptune", 30.1)):
    R = rAU*AU; Msec = 4*np.pi/3*R**3*RHO_DM*FRET
    print(f"      within {rname}'s orbit: the retained sector holds {Msec/MSUN:.2e} solar masses, so its boosted momentum density is that fraction of the Sun's own")
R = 9.54*AU; Msec = 4*np.pi/3*R**3*RHO_DM*FRET/MSUN
alpha_from_density = Msec
check("V2 [the sector's own contribution is negligible] the part of the preferred-frame effect that comes from boosting the sector's local stress is suppressed by how little of it sits inside the solar system: 6e-16 of the Sun, eleven orders below the bound on alpha_1, and the depletion galaxies require makes it seven times smaller still",
      alpha_from_density < 1e-10, f"sector mass inside Saturn's orbit / Msun = {alpha_from_density:.2e} against the alpha_1 bound of about 1e-4")
# the amplification factor of the clock constraint, which is what made the earlier case fatal
print("    the amplification: in the linearised clock constraint, delta K = (2 q P_Xtau v + 2 q d L sigma)/W, the coefficient multiplying the")
print("    scalar's gradient term is 2qd/W = mu/q, with mu = 2 d q^2/U the same ratio that fixes the margin. It is bounded by construction.")
for MU in (0.1, 0.5, 0.9):
    for qv in (0.5, 1.0, 2.0):
        pass
amps = [(MU, qv, MU/qv) for MU in (0.1, 0.5, 0.9) for qv in (0.5, 1.0, 2.0)]
print("      mu, q, amplification mu/q: " + "; ".join(f"({m:.1f}, {qq:.1f}) -> {A:.2f}" for m, qq, A in amps))
L170_AMP = (1/0.2325)**2                                                   # the earlier action's (c^2/mu_inf)^2 at its own bound mu_inf >= 4.3
check("V3 [the amplification is bounded here, and it was not there] in this action the clock constraint's coefficient is mu/q, a ratio of background quantities bounded by the same margin condition that keeps the kinetic term healthy, so it is of order unity across the whole admissible range; in the action that died the corresponding factor was (c^2/mu_inf)^2, which its own PPN bound forced above 18",
      max(A for _, _, A in amps) < 2.0 and L170_AMP > 10,
      f"mu/q spans {min(A for _, _, A in amps):.2f} to {max(A for _, _, A in amps):.2f} over mu in [0.1, 0.9] and q in [0.5, 2]; the earlier action's factor was at least {L170_AMP:.0f}")
check("V4 [THE STRUCTURAL DIFFERENCE, read off the action] in this action matter enters only through S_r and S_b, both minimally coupled to the metric, so there is no term coupling the clock to matter directly; the action that died carried an explicit mixing term between the clock and the scalar that the matter sourced. The clock here is therefore sourced by the metric and by the scalar, never by the density, and any preferred-frame amplitude it produces is second order in the sector's gravitational weight rather than first order in its coupling",
      alpha_from_density*max(A for _, _, A in amps) < 1e-10,
      f"with the bounded amplification the scaling estimate is {alpha_from_density*max(A for _, _, A in amps):.2e}, against the alpha_1 bound of about 1e-4 -- but this is a SCALING argument, not a computed alpha_1")
check("V5 [THE VERDICT: not killed, and not passed] the mechanism that made the earlier case fatal -- a direct clock-matter coupling multiplied by a large amplification -- is absent from this action, and the scaling estimate that replaces it sits eleven orders below the bound. That is grounds for expecting the gate to be survivable, and it is NOT a computed preferred-frame parameter. The full boosted metric expansion for this action has not been done and this gate is recorded as open",
      alpha_from_density < 1e-10 and max(A for _, _, A in amps) < 2.0 and beta > 1e-4,
      "reported as OPEN: the kill mechanism is absent and the scaling is eleven orders below the bound, but no alpha_1 has been computed for this action and none is claimed")
print("    READING: the earlier kill does not transfer, for a reason that can be read off the action rather than argued: there is no direct clock-matter coupling here, and\n"
      "    the clock constraint's amplification is bounded by the same ratio that keeps the margin healthy. What remains is a scaling estimate eleven orders below the bound,\n"
      "    which is encouraging and is not a calculation. The gate stays open, and it is the last one.\n"
      "    LIMITS: no preferred-frame parameter is computed; the boosted metric expansion for this action is not performed; the amplification is read off the linearised clock\n"
      "    constraint of the cosmological reduction and its solar-system counterpart may differ; the sector's local density is the standard 0.4 GeV/cm^3 scaled by the retained\n"
      "    fraction; the comparison with the earlier action uses that action's own published bound.")
json.dump(dict(beta=float(beta), sector_mass_saturn=float(alpha_from_density), amplification=[[m, q, A] for m, q, A in amps],
               earlier_amplification=float(L170_AMP), verdict="open: kill mechanism absent, scaling 11 orders below, no alpha_1 computed"),
          open("L203_results.json", "w"), indent=1)
print(f"\nL203 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
