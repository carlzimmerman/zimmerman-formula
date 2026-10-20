# Roadmap to complete the cold-energy mechanisms

User-requested roadmap for Claude. Baseline evidence: `bcba9fc59` (CFG872).
Companion: `FORMATION_TO_CLAUDE_ONE_SHOT_2026-10-19.md` in this directory.
Status: OPEN research program; these are proposed tests, not completed results
or changes to any existing frozen criteria. Do not call a fitted mass, finite
simulation or pooled observational pass a completed physical mechanism.

## NEXT TEST: can the outer envelope accept the required E and J?

Run this cheap necessary-capacity check BEFORE another costly formation PDE.
Test Draco, Sextans, Fornax and Leo I with the same microscopic model. A finite
bound envelope can accept the core's energy/angular momentum; whole-galaxy
escape is optional. But all its mass inside the observed aperture counts.

Inputs must be independently fixed or bracketed with justified bounds:
- Finite initial cold inventory, initial density/velocity field, origin and
  frame; predicted initial vector J and energy from the chosen action.
- Desired core mass, aperture profile, permissible final core J, and survival
  history. Use matched stellar M/L, gravity law and aperture conventions.
- Receiver mass Mout, maximum cylindrical radius Rmax over the transfer phase,
  and kinetic-energy allowance Kavailable. Radius and energy cannot be taken
  arbitrarily large to force a pass. State assembly duration and tidal boundary.
- Include initial retained cold mass and any returning outer material. Track
  core, envelope and escaped mass disjointly; declare any label conversion.

For angular momentum transferred to material, the necessary capacity bound is

    |Jreq|^2 <= 2 Iout Kout <= 2 Mout Rmax^2 Kavailable.

Here Jreq is the required FINAL material receiver angular momentum after
accounting for its initial J, core J and declared external torque. Apply vector
conservation; cancellation of counter-rotating components must not be mistaken
for transport. If reporting Delta J to an already rotating receiver, include
its initial angular momentum and energy: the inequality bounds its final
J/K, not an arbitrary increment with initial energy omitted.

Obtain Kavailable from ONE conserved energy ledger:

    Ecore + Eout + Einteraction = Einitial + Wexternal,
    Jcore + Jout = Jinitial + integral(tau_external dt).

If a radiative channel is measured, add its E/J flux explicitly to the ledger.
Count binding release, self/interaction potential, internal excitation,
external work and escape cost once each. Kavailable must not be total rest
energy. Material escaping the boundary is not automatically unbound from the
host; measure its total orbital energy and possible return. Record the charge
flux separately. Fragment fusion/rest binding is not COM orbital cooling.

Mass-budget inputs from the prior capped-retained aperture model:

| Target | Remaining inventory, Msun | Needed fraction inside aperture | Fraction if binary shift transfers globally |
|---|---:|---:|---:|
| Draco | 2.77236e7 | .469303 | .427664 |
| Sextans | 2.53958e7 | .988540 | .645287 |
| Fornax | 9.90289e8 | .0130695 | .0117393 |
| Leo I | 1.88437e8 | .0345131 | .0344714 |

These are conditional model budgets, not measured cold masses. Total supply
53.64 Mstars assumes ratio5.364 and retention .1. Sextans still assumes stellar
M/L=2. Binary-transfer values are a separate sensitivity, NOT replacement
observations. Recompute for any changed baseline; do not mix with CFG870's
full exponential-law fit. Fornax/Leo I must not acquire extra uncounted inner
envelope mass. 1-f is an optimistic upper allowance for material outside the
required aperture, not an automatically permitted escape fraction: core
inefficiency, survival and other losses consume the same stock. An outer
receiver may stay bound while preserving aperture mass.

Report THREE outcomes for each dwarf and branch:
1. CAPACITY EXCLUDED only if even justified upper bounds on receiver capacity
   cannot meet E/J transfer and finite stock simultaneously.
2. CAPACITY ALLOWED if independently specified inputs satisfy both conservation
   capacity and aperture budgets. This is necessary feasibility, NOT formation.
3. INDETERMINATE if initial J, available energy, receiver radius/mass or external
   work lacks a defensible value/bound. Do not fit missing inputs to get a pass.

Deliver per-system E/J/mass ledgers with units, origins, input hashes, bound
assumptions and an executable small audit. Audit the most favorable admissible
receiver first: failure there can reject a branch cheaply. If it passes, move
to the actual transfer-rate test below. Do not change existing frozen gates.

## Gate 2: demonstrate actual transport and its rate

First check Claude's live work to avoid duplication. For the chosen original
action, measure isolated and matched collision/patch histories with the same
Hamiltonian, boundaries and discretization. Track core/envelope/escaped E, J,
charge and orbital COM energy separately from binding/internal energy.
Demonstrate convergence of the SMALL transfer signal, including radius/box
and resolution changes; global Hamiltonian drift alone does not certify it.
Use physical outgoing flux rather than treating a reflecting/periodic box as
escape. Keep independent runs below 1 GB while the shared 1024-cubed job lives.

Success requires enough net transfer within the independently specified
assembly time, no disallowed loss of core inventory, and no rebound/return
that restores the deficit. Too little transport closes that action/initial-
state branch. Capacity without rate leaves the mechanism open, not complete.

## Gate 3: derive production and the four-system selector

Derive the initial cold abundance, coherence/phase space, fragment spectrum
and patch shear/spin from native initial conditions; do not assume the needed
cold compact cloud. Preserve the original charged Phi/X versus ARGON real-
mediator distinction. ARGON11 established scoped fragmentation, not universal
cosmological production or successful-capture cross section.

Use the same physical parameters across all four systems. Predict differences
in assembly histories BEFORE fitting their central masses. Common late
Maxwellian capture and common early density/clock prescriptions failed recorded
selectivity tests. New initial spins/densities are predictions only if supplied
independently. Per-dwarf tuned core normalization is not a repair.

## Gate 4: derive the equilibrium/profile and test survival

Produce a finite-mass distribution/profile from transport, rather than an
infinite isothermal extension. Derive core size, velocity scale and truncation;
check stability and both algebraic branches where applicable. H-LINK's
c=4.5 sigma_x^2/a0 ansatz has an exact excess ceiling and fails Draco's recorded
central requirement; raising the clump mass cannot solve that branch.

Evolve the complete core+envelope through baryon/gas and tidal histories.
Count retained background and returning material, include stripping/heating,
and fit representative radial stellar kinematics with membership/binary
likelihoods. Need enough aperture mass in Draco/Sextans and no excess in
Fornax/Leo I simultaneously; finite stock and survival must hold together.

## Gate 5: close the broader cold-energy theory dependencies

Independently establish the action-to-occupied-response/source normalization,
source populations, a0 and coefficient origins; CE093 leaves these open.
A mathematical susceptibility identity is not occupied physical matter.
Verify stability, production and relevant cosmological/galaxy observables in
the same declared theory. Re-test the finite cored form against held-out data
when it changes; fitted Vx/core mean gates do not derive their origin.
Preserve existing failures and condition every imported result on its actual
hypotheses. No new photon portal or borrowed ultralight coherence by assertion.

## Completion rule and handoff deliverables

For each gate save: exact source revision, raw-input hashes, conservation/unit
checks, executable command, tested regime, result and remaining limitation.
Only claim a four-dwarf physical mechanism after production, independently
predicted selectivity, measured E/J transfer rate, finite mass/profile,
survival and radial kinematics agree with one common model. Complete broader
theory claims only after the additional source/normalization and cosmological
obligations are met. Otherwise report the successful sub-obligation precisely.

Existing small algebra/source audit:
`python3 sol61_push/formation_one_shot_2026_10_19/audit.py` (21 checks).
It does NOT run the next capacity test: required physical input ledgers are
still missing. Start there and report indeterminate inputs explicitly.
