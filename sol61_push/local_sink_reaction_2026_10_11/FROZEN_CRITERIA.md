# Local vacuum sink reaction — freeze alone before computation

Prior known results: CFG131/CFG195 already derive the vacuum gradient force;
CFG542 derives the settling power and a canonical partner singular at phi_dot=0;
CFG630 is computing the homogeneous energy ledger. Do not reproduce those
lanes or label their mathematics novel. Test the additional implication that
small deposited rest-energy fraction need not mean small local force.

Exact model for this diagnostic: Minkowski metric (-,+,+,+), x0=ct. A receiving
sector is PURE vacuum T_v^{mu nu}=-V eta^{mu nu}; matter exchanges the opposite
four-force. Let V=V0+eta rho0 v^2 F(t) exp(-r^2/(2L^2)), matter mass density
rho_c=rho0 exp(-r^2/(2L^2)), F=1-exp(-t/tau). All constants positive.
These are specified smooth TEST FIELDS, not a self-consistent halo evolution,
derived coupling, or candidate-B profile. eta is an illustrative deposited
energy fraction, not adopted as a parameter of the theory.

Derive Q=dV/dt, the required matter force density +grad V, and the acceleration
ratio to g_ref=v^2 r/L^2 (a reference acceleration, not claimed to be the gas's
self-gravity). The sign and c factors must follow directly from tensor
divergence. Check all four components, mixed-derivative integrability, zero-
deposit and spatially uniform controls. MUTATE a sink that keeps Q but deletes
the spatial exchange must violate conservation; MUTATE the reaction sign must
also fail. Check deltaV/(rho_c c^2)=eta F(v/c)^2 but |a_react|/g_ref=eta F.

Numerical illustration only: eta=1, F=1-exp(-1), v=200 and1000 km/s. Report
rest-energy fraction and force ratio; never compare with data or treat eta=1
as the framework's prediction. No observational or universal action exclusion.
The identity is independent of kernel/a0; it applies conditionally on either
footing, without pooling footing-dependent results. Kappa remains fitted.

For a homogeneous interacting vacuum, define w_eff by recasting dot V=Q as
dot V+3H(1+w_eff)V=0. Check w_eff=-1-Q/(3HV) while intrinsic p/V=-1. This is
an effective bookkeeping parameter, not proof of a canonical phantom field.

Use Sympy exact algebra and standard-library arithmetic; one process/thread,
CPU10s/wall20s, <150MB expected. Pin code/criteria/contract/results. Preserve
failure. Produce a handoff distinguishing the already-known gradient identity
from the local-reaction consequence and what a full action still must derive.
