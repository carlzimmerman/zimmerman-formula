# FGF041: weak residuals permit an initially present concentration defect

Accepted exact approximate-state counterexample in the stated weak topologies.
This is not a constructed exact solution or a failure of the limiting background
to solve its equations. Independent author and root-only audits found no errors.
All original proof/result bytes are preserved; source and artifact hashes match.

Fix the inherited Q crossing on a fixed interval. A compact trajectory X=x0+vt,
v=1/sqrt(tau), remains strictly on one regular side, away from cusp and walls.
For fixed physical potential Phi, length L and nonconstant smooth compact F,
psi=Phi sqrt(epsilon) F((x-X)/(L epsilon)). Set h=psi_x, u=psi_t=-v h,
n=rho,j=0,chi=chi0,w=0. Then integral h²=A0=Phi² integral F'²/L>0,
integral |h|=O(sqrt(epsilon)), and psi tends uniformly to zero. Derivatives
converge weakly in L2. The support exactly preserves all field walls, mass and
scale cap. Tau v²=1 is the diagnostic potential speed, not a photon-speed claim.

Exact global Q estimates, valid even for the large signed packet gradient, are
|B-g|<=a/2, |W-g²/2|<=a|g|/2, |Bg-W-g²/2|<=a|g|,
and |T(|g+h|)-T(|g|)|<=a|h|/2. Let eB=B(g0+h)-B0-h. It is supported on
the packet and uniformly bounded, with L2 norm O(sqrt(epsilon)). Thus:

- Continuity and both field kinematic identities are exact.
- Actual dynamic source residual tau phi_tt-B_x+C rho=-partial_x eB tends
  to zero in L-infinity_t H^-1_x; its spatial Lip-dual norm is O(epsilon).
- Scale residual T0-Tnew and separate matter residual rho h tend to zero
  in L-infinity_t L1_x at O(sqrt(epsilon)); not asserted L2-small.
- Combined momentum residual is directly calculated, not obtained by multiplying
  the weak source residual by an unbounded gradient. With S=Bg-W and
  DeltaRS=S(g0+h)-S(g0)-[(g0+h)²-g0²]/2, it is
  (g0' h+partial_x DeltaRS)/C. Its spatial Lip-dual norm tends to zero.
- Full energy balance residual tends to zero against compact spacetime C1
  tests by cancellation of a transported square and L1-small remainders.

Write E*=A0/C. Full combined momentum P and stress Pi from FGF040, exact
energy density H (including n phi and all field/matter terms), and the actual
energy flux Qe have measure limits

P -> (E*/v) delta_X,
Pi -> Pi0 dx+E* delta_X,
H -> H0 dx+E* delta_X,
Qe -> v E* delta_X.

For each limit the lower-order remainder tends to zero in L1. The singular
parts obey the transport balances. Evaluating these nonlinear quantities at
the weak limiting fields gives only the background and misses all four defects.
The background remains an exact solution. The failed implication is solely that
bounded energy plus THESE weak residuals and weak initial derivatives identify
nonlinear fluxes. No strong-residual, exact-solution or uniqueness theorem is
refuted. No deep-MOND expansion is used in the concentrated high-gradient core;
the background and dynamic Q source retain their signed MOND relation.

Initial energy already has the same nonzero E* defect. Exact source cancellation
gives integrated relative energy between E*/2 and E*, tending uniformly to E*.
No energy is created from zero-energy initial data. Author's amplitude Phi epsilon
control gives energy <=epsilon E* and strong derivative convergence. Reviewer's
Phi epsilon^(3/4) control also works; root covers any additional amplitude tending
to zero. These are analytic controls, not a numerical exponent sweep.

For fixed density/scale, strong L2 potential derivatives identify the displayed
momentum and energy fluxes in L1 by product estimates and Q Lipschitz bounds.
Convergence in measure plus uniform integrability of derivative squares suffices;
a bound on their integrals alone does not. These hypotheses are not derived
from the residual equations. Root's separately audited general sufficient gate
also assumes strong L2 scale derivatives, uniform bounded scale convergence,
strong L2 sqrt(n) and j/sqrt(n), and vacuum compatibility of the latter limit.
Without that compatibility a kinetic defect may survive on limiting vacuum.
Energy density additionally needs internal-energy L1 convergence and bounded
uniform potential convergence. General matter energy advection needs extra
velocity/enthalpy control and is not included. No boundary trace theorem follows.

Both a0=9.3619e-11 and1.1279e-10 m/s² and separate vacuum/frozen-H/evolving-H
branches remain distinct. This is fixed-reference Q diagnostic evidence only;
no RAR/M/filtered-MONO transfer, physical scale reservoir, metric/photon/DOF,
calibrated observation or historical novelty. FGF031 calibration stop and AS228
primary ownership remain; FGF037 failed upper-control route and FGF039 equality
correction remain part of ancestry. Proof-only, zero mathematical computations
or bounded manifests. Physical objective remains open.

Next changed premise: FGF042 asks whether vanishing FULL relative total energy
forces strong unweighted derivative convergence by retaining exact Q convexity,
and what follows conditional on an already-supplied energy inequality. It does
not assume this next implication is proved or that an approximation exists.

## Evidence pins

- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-041/fgf041_run_001/result.json` SHA256 `07785d7a09b507a224722edaaf389aeec09d65cb5ce0882d26683d78ad3287d2`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-041/fgf041_run_001/DERIVATION.md` SHA256 `54e8390a0fb61573041e28aade6a68d3bb67e17adfe82b049eb5a63b5f0fd7a5`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-041/fgf041_run_001/REPORT.md` SHA256 `6920375c82d2a47aa9ad5666ab47d8017d05aa69c539bc14a56df8e3d0af987f`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-041/fgf041_run_001/input_sha256.json` SHA256 `c8002865be590b08daaddd73346480f3ba6a7ef3f5cb0d66071e3811a2fae947`.
- `campaign_fresh_gravity_astra/stage_28/packet_defect/INDEPENDENT_AUDIT.md` SHA256 `281cada84eb7c8c068894ae688e09d14f9b6a1871d26e1969b923520cbb33afb`.
- `campaign_fresh_gravity_astra/stage_28/packet_defect/PROOF_COMPARISON.json` SHA256 `037a451b96b5e3604de25bcd3cd541fa5cdcc4878153075cb9aad046fe75e79e`.
- `campaign_fresh_gravity_astra/stage_28/packet_defect/PROOF_RECORD.json` SHA256 `83e8aed4aa5e70177365bfc3a28dcfaf739e5a1fe0c0f6c8597c5b98cfce8ff6`.
- `campaign_fresh_gravity_astra/stage_28/packet_defect/ROOT_DERIVATION.md` SHA256 `57549a5543c71a35307ed3ccef9036fe8a0cb6d015bfed8e0a20bb294a80ca3b`.
- `campaign_fresh_gravity_astra/stage_28/packet_defect/audit_result.json` SHA256 `2dc7c3cb274c434750d231dd9c0163d5487c36ff4ba6ef7b94971cac0d6004b7`.
- `campaign_fresh_gravity_astra/stage_28/independent_audit/DERIVATION_FROZEN.json` SHA256 `e54850ca6aa977fe0176a6aae2075eb98ae5c89a7e43b476134b5994057eb47f`.
- `campaign_fresh_gravity_astra/stage_28/independent_audit/FROZEN_DERIVATION.md` SHA256 `a436daa8e9950c7385e1d312b91d0dd14f897ff8241b7b8ff73583bdc6d3d605`.
- `campaign_fresh_gravity_astra/stage_28/independent_audit/INDEPENDENT_AUDIT.md` SHA256 `58231681db9fd8b4244cc48718f7bc2f703c4f18f8cc101e31196c3757d2e4ca`.
- `campaign_fresh_gravity_astra/stage_28/independent_audit/audit_result.json` SHA256 `919d50cab0d51b008c66c3e7ec260b030e4150d74b7c5dabb4f017e6a549724e`.

Reconciled 2026-09-30T22:44:52.016788+00:00.
