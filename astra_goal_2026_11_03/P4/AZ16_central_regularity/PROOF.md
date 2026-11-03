# AZ16 — FAIL smooth-core claim; weak branch NO VERDICT

κ = ½ FITTED; not theory closed

Claim card: for positive lambda,G and central psi0>0, test existence of a spherical, centrally nonincreasing, C² stationary solution of the SAME AZ14 energy with a regular origin. Domain is a neighborhood of the origin with positive density; no outer boundary assumption is needed for this local obstruction. Dependencies are direct constrained variation, radial divergence and positivity of Newtonian enclosed mass. Numerical checks test operator normalization and local asymptotics, not the existence theorem.

The conserved mass is integral psi^4; F=256lambda integral |grad psi|^4. Varying F+W-mu integral psi^4 and dividing the Euler equation by four gives

-256lambda div(|grad psi|² grad psi)+(Phi-mu)psi³=0,
Delta Phi=4piG psi^4.

The factor four from varying mass and the factor four from varying the gradient fourth power must both be retained. For spherical psi, define flux Q=r² psi'^3. Then

Q'=r²(Phi-mu)psi³/(256lambda),
Phi'=G M(<r)/r².

A regular C² radial scalar has psi'=O(r) and bounded psi''. Consequently div(psi'^3)=3psi'^2 psi''+2psi'^3/r=O(r²), tending to zero. Evaluating the equilibrium equation at the origin forces mu=Phi0. Positive central density gives Phi(r)>Phi0 for sufficiently small r>0. The exact flux equation then gives Q'>0, with Q(0)=0, hence psi'>0. This contradicts central nonincrease. Even a flatter C² center cannot avoid the flux sign argument. This proves FAIL for the stated smooth-core claim on both footing labels; a0 does not enter.

The obstruction is NOT a no-go for finite-density weak cores. Let Delta=mu-Phi0>0. The same flux equation gives

Q=-Delta psi0³ r³/(768lambda)+higher order,
psi'=-psi0[Delta/(768lambda)]^(1/3) r^(1/3)+higher order,
psi=psi0-(3/4)psi0[Delta/(768lambda)]^(1/3) r^(4/3)+higher order.

This is C¹ with divergent second derivative. Its gradient energy density is integrable at the origin, and its cubic-gradient flux has finite divergence. A nonsingular density and potential do not imply C² density. The expansion is locally compatible with Poisson, whose central potential correction is (2piG/3)psi0^4 r². It does not prove a global isolated equilibrium or stable evolution. In particular, AZ15's smooth-solution energy bound is not being silently promoted to a weak-solution existence result.

For the separately disclosed regularization

F_reg=lambda integral rho[(|grad ln rho|²+q0²)²-q0^4],

expansion gives the original quartic plus 2lambda q0² |grad rho|²/rho. Around homogeneous rho0, its linear chemical potential is -4lambda q0² Delta(delta rho)/rho0. Combining Euler and continuity gives omega²=4lambda q0² k^4 before gravity. Every positive q0 thus removes the exact zero-linear-pressure structural gate. It is NOT automatically incompatible with measured cosmology: a physical lambda,q0 and causal completion are absent. Both would count as FITTED if chosen; no value is adopted here.

All seven controls pass. The independently integrated local slope ratios are .99999832863 and .99996396585 at r=1e-4 and1e-3. Their asymptotic tolerance margin is +.00096396585; start/tolerance-refinement margin is +.0000099999989133. Omitting the radial divergence term makes the manufactured operator wrong by 2/3. The regularized synthetic linear coefficient is 4.000000025 against exact4. These are identity margins, not observational errors.

Self-audit checked the origin limit under C² hypotheses, the sign of Poisson's radial field, the mass-constraint factor, the weak-core exponent and coefficient, and the distinction between smooth nonexistence and weak admissibility. No external theorem was invoked. This is self-review only. Full requirement and RQ3 rows remain NOT EVALUABLE and earn zero credit.
