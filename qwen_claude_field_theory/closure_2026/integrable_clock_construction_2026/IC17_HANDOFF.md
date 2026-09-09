# Current constructive handoff: IC17 pole clock, real sources, transition scope

**Full relativistic theory OPEN; IC17 fails the tested relative-flow matter
stability gate.** This checkpoint constructs an early
radiation/cold-clock regime from a specified action, not a union of unrelated
passing gates. Carl's retained-clock idea and explicit pre-recombination
question motivated the direction. The pole pressure and calculations below
were introduced in this investigation; no literature-wide novelty is claimed.

## Explicit construction and its surviving early-history result

[IC17](IC17_POLE_CLOCK.md) keeps the exact original static exponential
primitive and replaces the compact momentum window with a one-sided switch.
Its global phase Hamiltonian is

    H17=H10[eta_up]-eta_up exp(-4w) f17(Xtilde),
    f17(X)=(5/64)(2X)^16+10^-5 (2X)^2/(1-2X).

The linked action specifies all fields, coefficients, active/inactive open
domains, boundary conditions and physical matter coupling. On its expanding
plateau, stationary momentum variation gives Einstein gravity plus the
explicitly counted clock. The pole dominates the previously negative early
clock kinetic term. With delta=1-2X -> 0+, the derived leading behaviour is

    rho_clock ~ q ~ 2epsilon/delta²,
    w_clock ~ delta/2,  c_clock² ~ delta/4,
    rho_clock proportional to Aphysical^-3,
    rho_rad proportional to Aphysical^-4.

The density amplitude is a conserved initial clock charge, not a prediction
from baryonic mass. A cold clock is an additional gravitating component;
its name does not remove the usual abundance and structure tests.

At epsilon=10^-5 the 241-point early logarithmic scan is healthy on the
tested plateau. An 81-point late scan stops before the zero-sound-speed
endpoint. The sourced radiation history spans eight **physical** e-folds
backward from S=.1, reaching S≈9.5540e-9 with radiation fraction≈82.04%.
Its charge and independent quadrature agree. This uses new energies and
field equations, not a prescribed expansion history or late-condensate
tuning. It is not an empirical CMB/recombination fit.

## Actual baryons, not massless-scalar substitutes

[The same-action baryon calculation](IC17_BARYON_BACKGROUND.md) varies
the conserved pressureless particle density through `Ldust=-b exp(w)`.
The clock and baryon charges give `b=k q`. The auxiliary equation is
re-solved with this source; none of IC14's eliminated vacuum jets is
silently reused. The chosen k=.2 is initial data, not a measured abundance.
The actual two-equation time-preservation system supplies physical H.

The [full irrotational dust principal calculation](IC17_DUST_PRINCIPAL.md)
then varies the physical dust multiplier action before eliminating it. This
gives exactly `Leff(X,Y)=P17(X,log(2Y)/2)`, with TWO coupled physical scalar
matter/clock modes. Both aligned modes have positive kinetic coefficients
and subluminal speeds at all 51 sampled backgrounds; the auxiliary
four-constraint block has computed rank four there.

The next gate fails. At S=.1,k=.2 with physical relative dust speed v=.1,
the actual characteristic roots include

    c=.09812744994361576 +/- .00466804840250795 i.

A 70-digit solve checks these against the direct determinant with normalized
residual below 6.3e-71. Positive time kinetic does not remove the complex
pair. The note constructs regular local ADM constraint data admitting the
point; it is not an assumed homogeneous FLRW state or a constructed global
solution. IC17 must therefore not be presented as uniformly healthy under
the requested matter-stability requirement. This failure does not falsify
the exponential kernel or the vacuum-density relation by themselves.

Independent review clarified the signed convention without changing the
computed polynomial: use perturbations `exp[i k(x+c t)]` and
`v=theta_x/theta_n`. Then physical phase velocity is -c and future-directed
dust velocity is -v. The reported complex roots and local constraint patch
are consistent in this convention; the absolute relative speed is .1.
Reflecting the spatial axis changes root signs, not their non-reality.

Concurrent repository work reached Fable's L43 assembly (`94c41856e`) and
its significance corrections (`e8ae735f1`) during this run. Their commit
inventories were checked, but the full new assembly was not audited here.
Do not inherit its title as a completion claim; its commit description
itself retains cosmological/cluster failures and a fitted normalization.

## What was repaired, and what was not

- [IC16](IC16_RADIATION_HISTORY.md) proves the old compact switch limited
  radiation on its inherited vacuum domain, with an exact conditional 40%
  bound and a sharper located numerical ceiling about13%. Its new switch
  allows a long radiation history but exposes a small-S ghost. IC17 changes
  the pressure itself and removes that failure on the tested branch.
- [IC15](IC15_DUST_RESPONSE.md) independently constructs a rational
  auxiliary potential with regular roots on both separate pure-source axes.
  Large dust still destabilizes its clock. It is NOT inserted into IC17,
  and its matter passes must not be imported into IC17's constraint count.
- [The transition audit](IC17_TRANSITION_SCOPE.md) confirms Fable L35's
  fixed-auxiliary-coordinate identity and sign obstruction in its stated
  reduction. An explicit exact counterexample disproves its insufficiently
  qualified variable-coefficient extension. This is a kinematic path, not
  an IC17 constraint solution or a healthy transition construction.

Fable L26's sigma handle concerns older IC4–IC7 revisions. L33 concerns
another two-scalar action, not IC17. Its selected common-time argument does
not replace the uncomputed full coupled characteristic determinant. Neither
licenses deleting IC17's physical propagation requirements.

## Carl's vacuum-density question

[The calculation and source](VACUUM_DENSITY_RECOMBINATION.md) distinguish
constant vacuum density from the rapidly changing total density. Under a
constant Lambda and the stated Planck reference fit, rho_Lambda≈5.8e-27
kg/m³ at recombination and today. The proposed relation then gives constant
a0≈9.36e-11 m/s². These reference-fit values are not independently derived
or empirically confirmed by the IC17 action. The coefficient 1/2 remains
input; an evolving clock need not imply evolving vacuum density or a0.

## Next unavoidable construction and falsification

Freeze IC17 as a **failed uniform-matter baseline**, keeping its constructive
pressure result. Do not rerun the aligned scan as evidence of full viability.
The repair must alter the action's mixed clock–dust principal structure,
controlled here by P_Xw (equivalently the reduced P_XY), and remove the
explicit relative-flow counterexample. Changing only the radiation history
or a plotted sound speed cannot do that. Test the same counterexample first
on any proposed revision, then its other matter species and interaction scale.

Only a revision passing those tests warrants the full transition and embedded
galaxy calculation. The weak-field physical Phi and Psi, measured Newton
constant, PPN and galaxy/cluster force must be outputs of that same action.

Static zero jets preserve equations, not a matched galactic solution. The
global Dirac closure, healthy transition, small-sound-speed strong-coupling
scale, endpoint treatment, baryon/photon perturbations and empirical spectra
remain obligations. No completed theory, solved cluster discrepancy or
Kepler-grade empirical prediction is announced by this checkpoint.

Exact commands, input hashes, test statuses and owned file inventory are
recorded in [the run index](ic15_ic17_run_001/run_index.json). Strict theory
reports deliberately refuse a full-closure certificate; a passing regression
test is not a passing theory.

Final verification: **287 regression tests pass, exit 0**. All six new
scientific programs were run in strict mode and exited **2**, recording the
unmet full-closure request; the runner therefore records those six runs as
failed requests, not successful theories. All seven version-2 provenance
records validate against their 82 pinned inputs. The owned inventory contains
44 files, including source, tests, mathematical notes and evidence logs.

An independent reviewer additionally reproduced the raw energy derivative,
local ADM patch and characteristic determinant at 70 digits. The mathematical
notes received a scoped self-review; no unrelated manuscript was rewritten.
The only final notation clarification is the explicit signed Fourier
convention above. The scientifically decisive status is **IC17 fails uniform
matter hyperbolicity; the broader construction programme remains OPEN**.
