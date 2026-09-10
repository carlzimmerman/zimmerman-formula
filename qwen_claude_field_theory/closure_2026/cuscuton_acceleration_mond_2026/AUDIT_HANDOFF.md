# CAM handoff: verified obstructions, not full closure

2026-09-10. Read ACTION.md and REPORT.md before continuing this branch.
The current physical audit passes 21 derivation checks. Lean passes with
only the standard printed axioms. The closure-required command exits 1.
The old action-bridge gate now exits 1, exposing its three failed bridges.
Six new regression tests, seven historical algebra tests, and nine existing
closure regressions pass. Surrogate success is not a theory certificate.
All 11 reproduction commands and their exit statuses are in run_002/stdout.txt;
run_002/manifest.json pins source files and records runtime and log hashes.

## Changes that matter

1. Minimal physical matter fixes the source as -rho*Phi. The old plus-Q
   candidate has the wrong attractive-gravity equation. The static match
   selects eta=1, sigma=-1 in the family eta*M2*a²+sigma*M2*a0²Q.
2. The trace-free multiplier is a derivative of an existing constraint:
   it shifts ell by minus div Lambda and adds no independent bulk condition.
3. The coupled lapse/shift/metric scalar retains one canonical pair.
   Its quadratic Hamiltonian vanishes at zero field, but the computed
   cubic Hamiltonian has nonzero momentum interactions.
4. The repaired action's lapse symbol is proportional to
   exp(-y)[k_perp²+(1-y)k_parallel²]. It is nonelliptic for y>=1.
5. C=V=C0 exp(-3H*tau) carries positive dust energy, not stealth stress.
6. The repaired action is in the known Blanchet–Marsat khronometric class.
   Neither a new architecture nor kappa=1/2 has been derived.

## New concurrent commits inspected

- 671b93a1f, L111: recomputes the same three-coordinate auxiliary toy
  Hamiltonian with K=2,A=3,k=1, then adds assigned tensor=2/vector=0 counts.
  It omits the metric scalar zeta and shift B, whose canonical pair is
  retained by the physical ADM calculation. Its toy rank-six result is
  compatible with our calculations but cannot certify total DOF=2.
- 6d69ba194, L112: uses gamma_CAM=1 and infers preferred-frame suppression
  from a purported linear clock. It performs no moving-frame field solution.
  The acceleration a_mu=n^nu nabla_nu n_mu is not linear in the clock, and
  the corrected action contains F(a); a linear multiplier does not remove it.
- 1dd35945b, L113: the BETA-1 and PPN-1 assertions use literal True.
  Linear Newtonian Poisson superposition cannot determine a second-order
  PPN coefficient. Metrics with g00=-(1+2Phi+2 beta Phi²+...) have the same
  Newtonian-order source equation for arbitrary beta. The local exponential
  constitutive tail also does not bound a global external-field response.

These are source inspections, not new reruns of L111-L113. Their claimed
PPN/total-DOF conclusions do not fill the missing calculations in REPORT.md.
Preserve these distinctions if reproducing their numerical outputs.

## Next useful construction

An independent nonlinear constraint or different kinetic architecture must
remove or demonstrate healthy dynamics of the scalar pair, while the lapse
operator remains admissible across the MOND transition. Re-derive the same
physical source equation after each change. A multiplier proportional to
a derivative of B_i cannot supply the needed new constraint.

The scalar clock is allowed by the user's specification only if separately
counted and demonstrated healthy. Our cubic interaction and nonelliptic lapse
require analysis; neither an assumed infinite sound speed nor zero quadratic
Hamiltonian supplies that demonstration. Do not advertise a completed theory
or a general impossibility theorem from this bounded result.
