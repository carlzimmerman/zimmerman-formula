# What is the cold component?

**In candidate B it is actual unseen gravitating mass, with the cosmological
role of cold dark matter. Its physical identity is not yet uniquely derived.**
Calling it a field, a fluid or a mode does not remove its mass or energy
budget. The most concrete construction adds a complex scalar wave field;
its mass and abundance remain inputs. This folder exposes that unresolved
piece rather than hiding it behind the phrase “cold component.”

The [new clock-state calculation](../recombination_and_structure_growth/clock_scalar_clustering_2026_10_06/REPORT.md) tests a different proposed realization: its free vacuum scalar mode has small short-wavelength pressure but leading momentum transport, and is not exactly dust. The [homogeneous shift-charge route](../recombination_and_structure_growth/homogeneous_clock_current_2026_10_06/REPORT.md) requires boundary tuning and does not supply an independent early cold mass. These are scoped tests of the retained clock action, rather than a replacement of candidate B's explicit material cold source.

Assessment: 2026-10-05. Base `6e0f6469ff5419cbad5395c230199045c8c475bb`.
This is a targeted repository audit and self-review. Physical identity and
the original theory closure remain OPEN.

## Three different objects

| Object | Meaning in the records | Real independently specified dark mass? |
|---|---|---|
| MOND phantom density | Effective density inferred by rewriting the modified force as a Newtonian Poisson source | Not from that rewrite alone |
| Cold component, candidate B T4 | A gravitating component with approximately dust-like stress and an adopted cosmic abundance | Yes, by construction |
| Complex wave field, FL1 / CFG288 road W | Proposed dynamical realization of the cold mass using a massive scalar and its nonrelativistic envelope | Yes; new field content in that construction |

“Cold” means a small pressure/streaming response on the required scales,
not a measured temperature or a known material. A fluid stress description
does not establish the microscopic substance. An effective MOND density is
not automatically a material halo with conserved charge or wave energy.

## What candidate B assumes

[CFG4's target table](../../campaign_fresh_gravity/CFG4_README.md) specifies:

- T4: Omega_c h²=0.1200, **FITTED as initial data**, behaving like CDM where
  the MOND law is off. This is the model's cosmological input, not an
  independently measured abundance in this audit.
- T5: identify the cold mass with the law's effective dark mass in bound
  regions, with **DECLARED** bookkeeping:

      M_dark = max(M_phantom, (Omega_c/Omega_b) M_b).

- Ownership, a density edge and permitted late transport specify where the
  mass resides and where the MOND response operates.

The max rule is meant to prevent adding the MOND apparent mass to an
already present cold halo and double-counting it. It is **not a derived
mass distribution or evolution equation**. Actual conserved fields and
compatible forces must implement it. The current effective model retains
the cosmological dark-matter mass requirement; it changes the proposed
realization and galaxy bookkeeping. Claiming it eliminates unseen
gravitating matter would contradict these recorded assumptions.

## The explicit wave-field proposal

[FL1's raw derivation](../../real_research/dark_fluid_2026/FL1_order_parameter.py)
explicitly says **“THIS IS NEW FIELD CONTENT.”** The tested C-H/K chassis
has the clock scalar and constrained auxiliaries, not an independent dust
degree of freedom. FL1 introduces a complex order parameter psi, related
to a relativistic scalar Phi. With hbar=c=1, its reduced equations are

    rho_d = m |psi|²,
    i partial_t psi = -laplacian(psi)/(2m) + m u psi,
    laplacian(u) = 4 pi G (rho_b + rho_d).

In that branch an auxiliary coupling pair makes the dark field feel the
Newtonian potential u rather than the baryons' MOND-enhanced potential.
This is branch-specific; it cannot be transferred automatically to candidate
B or another minimally coupled action. The assembled relativistic coupling,
source/force reciprocity and source dictionary remain audit obligations.

Wave superposition can represent intersecting streams. The tested finite
wave examples avoid the phase-only dust model's first-crossing failure;
they do not prove global regularity for arbitrary nonlinear halos or mergers.

If quantized, this scalar's excitations are bosons. A highly occupied state
can be treated classically. Thus “no dark-matter particle species” in these
notes is a choice to model a classical field, not a proof that it has no
particle interpretation. Large occupation also does not by itself establish
a thermodynamic superfluid phase. That label requires additional state physics.

## One field does not yet explain both dark sectors

[CFG288](../../campaign_fresh_gravity/CFG288_one_field_dark_sector/README.md)
tries V(Phi)=rho_Lambda+m²|Phi|². The constant term supplies vacuum stress;
the rapidly oscillating massive part can behave approximately like dust.
Those are different contributions to the same field's stress tensor.

The constant rho_Lambda drops out of the scalar equation. It therefore does
not fix the oscillation amplitude or cold amount. CFG288 reports needing an
initial amplitude around 0.015 reduced Planck masses at m=2e-20 eV, under
its onset/thermal-history assumptions. Mass and amplitude are inputs. A shared
field label is not a prediction of dark-matter abundance from dark energy.

Our [exact toy checks](identity_checks.py) illustrate the freedom in a canonical
harmonic degree of freedom in fixed geometry: changing its vacuum constant
leaves the scalar equation unchanged; doubling the amplitude quadruples
the oscillation energy. Its cycle-averaged local pressure is zero. This is a
counterfamily to selection by the constant potential term alone, not a full
expanding-universe or halo theorem.

## Other proposals and their limits

| Proposal | Physical content | Recorded status, not independently rerun here |
|---|---|---|
| CFG288 road S | Real P(X) scalar near a condensate point; conserved charge controls the dust amount | Charge is free; tested phase-only flow fails stream crossing/mergers |
| Clock's own dust | Preferred-foliation clock also carries cold matter | Tested identification conflicts with multistream flow and has prior growth/hold-scale problems; not FL1's separate field |
| CFG253 / CFG288 vacuum conversion | Early energy-conserving transfer creates a real cold reservoir | Tested late/recombination creation fails energy/CMB gates; sufficiently early conversion is conditional and does not predict the amount |
| CFG293 solitonic cores | Spatial structure of the wave-field realization | Tested core prescriptions did not give the required satellite correction |
| CFG344/345 cold accretion | Pre-existing cold matter grows into dwarf halos while gas accretion is suppressed | Conditional repair requiring small-scale power, formation/infall history and a consistent profile |

These are alternatives or restrictions, not all pieces of one proved substance.
Their quantitative bounds are construction-dependent. This audit does not
independently reproduce their CMB or satellite calculations.

## Closure obligations

1. Specify the field content, action, state, couplings and conserved quantity.
   Demonstrate whether it is new field content or a state of an existing field;
   FL1 currently uses the former.
2. Derive its production/selection, or openly retain a fitted abundance. A
   fitted abundance can be allowed phenomenologically, but is not a derivation
   of the amount from rho_Lambda.
3. Derive the physical identification with the MOND profile and max rule
   through assembly, baryon loss, transport and mergers, with energy conserved.
4. Check both gravitational source and response, including reaction. Do not
   borrow kernel invisibility from an action different from the retained model.
5. Use the same realization and parameters in cosmology, small-scale collapse,
   galaxies, clusters, satellites and lensing.

The next decisive target is the **same-action bridge from the explicit wave
field to T5's galaxy mass rule**, with conserved evolution and a source
dictionary. Without that bridge, the current construction is a proposed
cold-dark-matter field plus a separate phenomenological MOND law, not their
physical unification.

[Scope and hashes](scope.json) pin the inspected records. The
[current run](runs/identity_a/manifest.json) records nine exact toy-model
checks and raw stdout. No peer-session file is edited or physical identity
marked derived. This is the third continuation lane alongside
[main theory](../main_theory/README.md) and [32pi](../puzzle_32pi/README.md).
