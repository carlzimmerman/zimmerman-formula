# Formation verdict and the strongest remaining physical route


Next authorized work: [mechanism roadmap](ROADMAP_COLD_ENERGY_MECHANISMS_2026-10-19.md).
FIRST gate: outer-envelope energy/angular-momentum capacity versus all four
finite dwarf mass budgets; capacity allowed is not formation demonstrated.

User requested one focused attempt and a pushed handoff, with little usage
remaining. Source snapshot: `bcba9fc59` (CFG872), following CFG870/871.
**Verdict: a physical formation mechanism satisfying all four dwarfs is NOT
established. The strongest remaining candidate in this record is early
non-spherical collapse with gravitational energy redistribution and mass
export. Its required receiver and selectivity can be stated precisely; its
rate and native initial conditions remain uncomputed. Do not report it as
successful, or report the full theory complete.**

## Physical process to test

A finite, initially inhomogeneous cold patch collapses. Its time-dependent,
non-spherical gravitational potential torques low-angular-momentum material
inward and transfers angular momentum to an extended envelope. During collapse,
some material gains orbital energy and remains at large radii or escapes;
the retained inner material becomes more tightly bound. A fluctuating
potential changes each parcel's orbital energy; spherical symmetry alone
cannot remove its angular momentum. Phase mixing can make the core appear
relaxed without destroying total energy or angular momentum.

This uses a material receiver rather than assuming photons or freely escaping
low-frequency mediator waves. A finite outer halo can be the receiver; escape
from the whole galaxy is not required to reduce the CORE's energy. But its
mass inside today's stellar aperture still contributes to the dynamics and
must be counted, particularly in Fornax and Leo I. Returning orbits must be
evolved; a temporary outward excursion is not permanent removal.

The physical precedent is gravitational cooling in other self-gravitating
scalar models: [Seidel and Suen, gr-qc/9309015](https://arxiv.org/abs/gr-qc/9309015)
and [gr-qc/9412062](https://arxiv.org/abs/gr-qc/9412062). Those studies establish
that a conservative field can form bound objects while ejecting field energy.
They do NOT demonstrate this process for ARGON's potential, the original
charged Phi/X model, MeV fragments in dwarf halos, or these four galaxies.
The two local actions must remain separate. Here the galaxy-scale carrier
could instead be escaping bound fragments or outer-halo orbital energy.

## Exact conservation test: identify the receiver

For a closed system retain core, outer material and their interaction energy:

    E_core + E_outer + E_interaction = E_initial,
    J_core + J_outer = J_initial + integral(external torque dt).

Charge and mass bookkeeping must include all outgoing material. Fusion's
rest binding and internal excitations are separate from center-of-mass kinetic
energy. Radiation of newly released binding alone does not prove capture.
For material accepting angular momentum, Cauchy-Schwarz gives the necessary
bound

    |Delta J|^2 <= 2 I_outer K_outer,
    I_outer <= M_outer R_outer^2,
    M_outer >= |Delta J|^2 / (2 R_outer^2 K_outer).

Use cylindrical radius and kinetic energy about one common origin. K_outer
must come from the actual Hamiltonian, including potential/interaction work,
not the whole rest energy. For escape, separately pay the escape cost. This
is a necessary receiver-capacity condition, not a torque rate or sufficiency
proof. A receiver still bound at large radius is allowed.

In dimensionless terms, if the angular momentum to transfer is
j M R_i v and the allowed receiver kinetic energy is alpha M v^2/2, then

    M_outer/M >= (j^2/alpha) (R_i/R_outer)^2.

At equal radii and alpha=1, j=.05/.1/.2 needs at least .0025/.01/.04 of the
patch mass in the receiver. These are sensitivity examples, NOT measured
spins, energy allowances or successful dwarf models. The original Sextans
remaining-stock target .98854 leaves only .01146 outside the target core;
the earlier conditional binary-transfer target .64529 would relax that to
.35471. That correction is not an established global dispersion measurement.
Apply the same population/selection likelihood before replacing the target.

## Why an unspecified scalar radiation channel is insufficient

A linear massive scalar in vacuum has omega^2=c^2 k^2+(m c^2/hbar)^2.
A bare slow source can emit propagating modes only above the mass threshold.
At m=1 MeV, the threshold is 1.52e21 /s. A 10 km/s motion on 100 pc has
omega~3.24e-15 /s: the ratio is 4.69e35. This excludes treating slow ordinary
orbital oscillations as freely radiating that massive scalar in linear vacuum.
It does NOT exclude near-mass carrier sidebands, nonlinear harmonics,
above-threshold bound-field dynamics, light collective modes in a medium,
or energy carried by escaping massive fragments. Each needs its own coupling,
kinematics and flux calculation. ARGON's real mediator is heavier still.

Also, a 1 MeV quantum at 10 km/s has de Broglie wavelength ~3.72e-8 m.
Galaxy-scale wave coherence cannot be borrowed from ultralight-field examples.
This observation is not an all-condensate or self-interaction no-go. Establish
the appropriate coherent field or kinetic description instead of switching
between them at the unresolved step.

## The selectivity problem remains the decisive missing prediction

This route can redistribute E and J without a new radiative portal. It has
not predicted WHY Draco/Sextans get compact mass while Fornax/Leo I do not.
Native patch shear, inertia, collapse timing, mergers and the baryonic/tidal
history must set those differences before fitting stellar dispersions. Picking
four initial spins or cloud densities to hit four answers reproduces the
missing normalization. Common late Maxwellian capture and common early dense
cloud prescriptions already failed their recorded selectivity tests.
Fragmentation alone is neither orbital cooling nor central mass delivery.

The prior early-cloud benchmarks required Draco/Sextans density contrasts
~2000/~39000 relative to Fornax under identical effective capture coefficient
and dynamical clock. These numbers describe that conditional model, not
measured densities or a requirement for every violent-collapse history.
The conditional binary shift materially relaxes Sextans but does not produce
the required assembly history. Low-spin initial patches remain hypotheses.

Latest Claude results reinforce that pooled fits are insufficient:
- CFG870 reports cored-SPARC and pooled dwarf mean gates pass, with Vx and
  core radius fitted. This is useful phenomenology, not formation evidence.
- CFG871 adds H-LINK, c=4.5 sigma_x^2/a0. Identifying c with r_M is an
  additional assumption; the quoted virial relation alone does not force it.
- CFG872 explicitly has no root for Draco on either footing. Its FLOOR-LIKE
  regression uses only the solvable selected subset and a chosen root; it
  does not establish a universal formation mass or reject every supply model.

For the declared H-LINK profile its exact maximum added stellar dispersion is

    q(x)=(2/3)x R^2/[R^2+(4.5x/a0)^2] <= a0 R/13.5,
    x=sigma_x^2 >=0.

Equality occurs at core radius R. Our separate capped-retained central-value
bridge needs Draco q=72.42 versus maximum55.12 (km/s)^2, or65.99 IF the binary
shift transfers globally. Making the clump heavier cannot fix that ansatz.
This uses a different baseline from source's exponential law and is not a
regrade or uncertainty-aware exclusion. Do not retrofit k=4.5 silently.

## One decisive next experiment, rather than another fitted core

Use the actual chosen action and independently specified finite initial
patches. First measure net orbital E/J transfer in matched isolated/pair or
small-patch evolutions with open-boundary flux accounting. Integrate the
same Hamiltonian used by the solver, and subtract isolated evolution to
separate binding/internal relaxation from orbital capture. Demonstrate
convergence of the small transferred orbital energy and angular momentum.
Keep the actual cold-mass inventory and every receiver particle/field cell.

Then embed the measured transport in independently generated patch histories
for all four dwarfs, retaining outer material and evolving tides/gas loss.
Require the same microscopic parameters, radial stellar-kinematic likelihood,
finite stock, core survival and receiver-capacity bound for all four. If net
transport is too weak, or the necessary receiver consumes the allowed stock,
this route fails on that branch. No live Claude experiment should be duplicated.
Do not spend a heavy PDE run before the receiver/energy budget is viable.

Audit: `sol61_push/formation_one_shot_2026_10_19/audit.py` and `receipt.json`.
Run `python3 sol61_push/formation_one_shot_2026_10_19/audit.py`: 21 bounded
stdlib algebra/source-pin checks. This is not a formation simulation, not a
v2 experiment manifest and not independent replay of the source likelihoods.
No frozen criteria, manuscripts, publications, shared CURRENT, live queue or
other agent's files changed. This handoff and its small audit are the requested
push. The theory and four-dwarf formation target remain OPEN.
