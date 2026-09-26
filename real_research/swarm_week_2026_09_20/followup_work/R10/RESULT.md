# R10 — Stop mixing inequivalent full force laws (result)

- Owner: Hermes (this lane); independent reviewer: none yet (self-review recorded)
- Execution state / claim state: completed / proved (exact symbolic inequivalence)
- Baseline: followup work order `3e857b5a6f8f05b48e29d0cbe42136998e9f9445`;
  inputs `reviews/kappa_unit_response_2026_09_20/README.md` (the rational
  auxiliary response mu_lambda = 1 - 1/(1+lambda y)^2) and
  `reviews/orbital_shape_law_2026_09_20/README.md` (its consequences), and
  `deepseek_push/lean/PD21_law_of_nature.lean` (the quadrature law
  g^2 = gN^2 + a0 gN).  `python3 model_equivalence.py` exit 0.
- Model/action ID: three distinct models, no ID mixing.

## Exact claim and scope

The rational auxiliary response, the PD21 quadrature law, and the L311 deep
law g^2 = a0 gN,tot are THREE DIFFERENT full force laws: they share the deep
asymptote g ~ sqrt(a0 gN) but differ at the transition and on the
Newtonian side.  With physical s, a0 and mass fixed there is no parameter or
field redefinition mapping any pair onto each other.

## First discriminator and result

**4/4 PASS.**  E1: at gN = a0 the solved fields are g/a0 = 1.4876 (aux),
1.4142 (quadrature), 1.0000 (deep-only) — a 5-49% spread at the transition.
E2: the exact symbolic residual mu_aux - mu_quad is nonzero (resid(a0) and
resid(2a0) both nonzero) — no reparametrization connects the two responses.
E3: on the Newtonian side at gN = 100 a0 the aux exceeds Newton by 1.65e-4 a0
while the quadrature exceeds it by 5.0e-4 a0 — different shapes in the
quasi-Newtonian regime that solar-system / wide-binary tests probe.  E4: the
L311 deep law with an added active source is deep-only: at total gN,tot =
0.1 a0 it gives g = 0.316 a0 vs the quadrature's 0.332 a0 (5% apart).

## Evidence

- `model_equivalence.py` → exit 0, 4/4 PASS + results JSON
  (g/a0 tables at the transition and deep corner).

## Independent check

E2 is exact symbolic (sympy residual evaluated at two points, not a fit);
E1's auxiliary root was solved with a bracketed root finder independent of the
quadrature's closed form.  The deep-corner agreement (all three -> sqrt(a0 gN))
is reproduced as the shared limit, which is what makes the transition
differences the discriminating content.

## Novelty and physical interpretation

The record's quarter-slope (orbital_shape_law), the unit-response claims
(kappa_unit_response) and the L311 active-mass law must not be quoted from
each other's derivations: each prediction attaches to the model it was derived
from.  This is the classification the followup work order's R10 requested;
nothing here changes the physics of any individual model, only the attribution
of their predictions.

## Decision and next action

proved.  Assign distinct model IDs (aux-response / quadrature / deep-active)
in any forward comparison; R18 must draw curves from each law separately.
R11 (new selector) and R12 (independent observable pair) may proceed with the
classification frozen.  Next cheap test: the R19 pair-mass-ratio control now
that PD20's amplitude is bounded to equal masses (R06).