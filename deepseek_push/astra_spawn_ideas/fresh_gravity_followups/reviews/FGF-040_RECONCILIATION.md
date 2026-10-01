# FGF040: separate force product fails; combined momentum coefficients exist

Accepted exact domain counterexample and conditional conservative identity.
Finite isothermal entropy of fixed-mass density n and finite-action H1 potential
do NOT imply n*phi_x is locally integrable. This is not a proof of nonlinear
ill-posedness or rejection of every weak formulation.

The author uses density exponent2/3 and potential-gradient exponent2/5,
giving force exponent16/15>1; the independently frozen root/reviewer use
3/4 and1/3, giving13/12>1. These are distinct exact examples, not a scan. Density has
finite mass/entropy, gradient square is integrable, potential is bounded with
zero perturbation wall traces, and all exact interaction/scale/kinetic energies
are finite. Fixed-mass normalization and wall corrections are explicit in the
proofs. The root additionally uses a positive mixture with the background and
an independently scaled gradient: both amplitudes can tend to zero, making
exact excess energy tend to zero while the force product stays nonintegrable.
The bounds use exact entropy convexity, A<=1 and complete first-variation
cancellation. This extension was separately audited. No density-gradient term
or static Gauss constraint is silently added to exclude these comparison states.

For smooth solutions, let j=nv, u=phi_t,g=phi_x,w=chi_t,kx=chi_x, C=4piG.
The inherited source is B_x=Cn+tau u_t and the scale equation is
sigma w_t-J chi_xx+U'-T=0. Direct algebra before any weak limit gives

P_t+F_x=0,
P=j-(tau u g+sigma w kx)/C,
F=j²/n+cs²n+[B g-W+tau u²/2+sigma w²/2+J kx²/2-U]/C.

Both field momentum signs, both kinetic stresses, the scale-gradient stress
and the minus U term were checked. The source/matter interaction is included
through the exact equations. Smooth equivalence to separate Euler momentum
requires the field equations and valid product differentiation.

On finite time slabs with n of uniformly finite mass, j²/n integrable,
u,g,w,kx square-integrable in spacetime and bounded chi, these P,F belong to
L1. At vacuum j²/n is defined as0 for j=n=0 and infinity if n=0,j!=0.
Cauchy controls j and field products; Q gives |B|<=|g|,
0<=B g-W<=g² and 0<=T<=a|g|/2. The mass, two field equations and combined
momentum equation can therefore be tested against compact-support smooth tests
without forming n*g. Merely finite energy at every time without an integrable
time bound is insufficient; the required spacetime hypotheses are explicit.
The author also proves a conditional component bound: uniform raw total-energy
upper bound, fixed mass/wall potential and bounded scale control the positive
kinetic, unweighted gradient, scale and entropy components. It uses the exact
Q lower bound W>=g²/4-a_max²/4 and absorbs the negative density-potential
interaction. This supplies norms if the energy bound is given, not an energy
conservation theorem. The independent author audit checks that extra estimate.

This supplies a candidate conservative weak SYSTEM, not a constructed solution,
proof of equivalence to an undefined separate force law, uniqueness, energy
inequality or passage to a weak limit. Weak convergence does not automatically
identify quadratic/constitutive products. FGF041 records a distinct bounded
concentration/approximation test for this remaining implication; not proved here.

At walls, the smooth integrated balance is d integral P/dt=F(left)-F(right).
Impermeability and fixed field values do not cancel the pressure/field traction.
For L1 coefficients, wall and initial traces need extra justification; no global
constant-momentum assertion is accepted. The result is not covariant physical
matter conservation or a physical metric construction.

Both a0 choices and separate constant-vacuum/frozen-H/evolving-H branches are
retained. Q diagnostic only; no RAR/M/filtered-MONO transfer, physical reservoir,
metric/photon/DOF, instrument-calibrated result or historical novelty. FGF031
calibration stop, primary AS228 repair ownership and FGF037 upper/Taylor failure
remain. Proof-only, zero mathematical computations/manifests. FGF039's earlier
equality correction remains part of ancestry; no discarded error is reinstated.

## Evidence pins

- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-040/fgf040_run_001/result.json` SHA256 `4ba102598510b35d6a1f61e445c7d4bd954166e999d4eda89dc23635765badc4`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-040/fgf040_run_001/DERIVATION.md` SHA256 `c9bf96698f5dc0675af01103e929bda4001e8f1b44f45e5960ae68a33ab0ca06`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-040/fgf040_run_001/REPORT.md` SHA256 `8e7a3face30f7eb15a8d55c05d0b75d65398c85c6c3c64fc87ddb432a4d5df04`.
- `deepseek_push/astra_spawn_ideas/fresh_gravity_followups/results/FGF-040/fgf040_run_001/input_sha256.json` SHA256 `d2d30cfe488246be5d14a1d75d27547e7ff67f3eb4f2dbccf89766d0a27ee843`.
- `campaign_fresh_gravity_astra/stage_27/weak_momentum/INDEPENDENT_AUDIT.md` SHA256 `547055610b0fb69706b3a486a881096ef94b11a4233111eb757dedb84e6d2ef6`.
- `campaign_fresh_gravity_astra/stage_27/weak_momentum/PROOF_COMPARISON.json` SHA256 `08c9982bae1c2d371afcf126da29fd7ef852c60b8a520dcd8f4ebfc75fa3372d`.
- `campaign_fresh_gravity_astra/stage_27/weak_momentum/PROOF_RECORD.json` SHA256 `202f5617944d5368b133432546e5046ea3921076f05f9cb815ab29f44c5ec29e`.
- `campaign_fresh_gravity_astra/stage_27/weak_momentum/ROOT_DERIVATION.md` SHA256 `9eb8d61177602f4cf4cc093bf43162ec997ced56693dc9e0ee709e601c5d534a`.
- `campaign_fresh_gravity_astra/stage_27/weak_momentum/audit_result.json` SHA256 `f7f77964dd6e706571ced830b7df8e646c789ba320aeecbcb3983a963cae280f`.
- `campaign_fresh_gravity_astra/stage_27/independent_audit/DERIVATION_FROZEN.json` SHA256 `60d9b5e6ef9e534965edd744ddfc6583fddc97139f984016f377a7f5416edd0e`.
- `campaign_fresh_gravity_astra/stage_27/independent_audit/FROZEN_DERIVATION.md` SHA256 `04372794ede2e8bcf04761549957dfe0a590b641222cb9abb68f659b4445bf2e`.
- `campaign_fresh_gravity_astra/stage_27/independent_audit/INDEPENDENT_AUDIT.md` SHA256 `4235649980cce7c257146499db6428054cde7a8a842fcfe3c6af69a09fddd2b8`.
- `campaign_fresh_gravity_astra/stage_27/independent_audit/audit_result.json` SHA256 `ac8f105018739c53a857633902d0ddaa19bef50e4bba78faa17d7f313cebd825`.

Reconciled 2026-09-30T21:42:36.315620+00:00.
