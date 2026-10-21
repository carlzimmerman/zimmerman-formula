# Local delta through 177591c05: first ask whether the residual is physical mass

This appends to, and does not rewrite, `RESULT.md` and `source_hashes.json`.
The new assessment pin is `177591c05a384bc07c819e3fe0d5517aa8798cb4`, observed
local HEAD on resumption. It includes the merge `e17d4aee4`, CFG925/926/927,
AG4h, W4-01 and the revised canonical note `de7085997`. Older pins remain valid
for the older assessment; the canonical and LEDGER changes are new evidence
versions, not freshness errors to erase. `update_source_hashes.json` records
the delta and actual source bytes against both pins. No network, external data
fetch, numerical evolution, owner-job inspection or campaign edit was performed.

## Revised recommendation

The new empirical lead is **a physical-mass feasibility test of the five clean,
positive, shape-driven SPARC residuals**, using the correct axisymmetric force
kernel and independent bounds on radial stellar M/L. Before treating them as
retained cold mass, ask whether a nonnegative ordinary-mass distribution can
produce their entire residual curves. A positive fitted stellar-M/L pull alone
does not establish that.

This is sharper than “follow up the five”: AG4h already explicitly recommends
follow-up. Its code tests a single stellar M/L and a coherent log-acceleration
offset, not whether the remaining shape has a physical mass source. The latter
is the concrete operation absent from that code. This is a scoped record
comparison, not an assertion that no older session ever considered it.

The finite-host release/restoration susceptibility test remains the decisive
microscopic test once a candidate mass-bearing state is identified. It no longer
has a justified prerequisite that one state rule explain three established
excess populations: **red lenses are now a conditional stellar-population
control; dwarfs and cluster cores remain the unresolved robust targets.**

## What changed, including controls

**CFG925 is now executed.** Its primary law-Jeans correction is NO EFFECT:
canonical dwarf F0 `0.372 -> 0.369` dex; median `sigma_J/sigma_W = 1.0009`.
Radial-anisotropy corners remove at most `0.114` dex; their aperture/anisotropy
assumptions are explicit. Self-sourcing is WORSENS on both footings: the literal
fixed point is ill-posed, the primary reformulation has the `(ln 2)^2 a0` floor
and breaks rotators, and argument-only sourcing lowers predictions. Including
the coded EFE raises canonical F0 to `0.654` dex and makes satellites still
farther above the field sample. The EFE-free baseline was already the lenient
one. All main K checks pass under A1, but **MUTATE M2's EFE arm is toothless**
(`0.009/0.008` dex versus `0.02` required); the MUTATE run exits 3 and must not
be described as all controls passing. Host-mass MUTATE M3 does bite. Source:
`CFG925_small_reframings_A/README.md:5–21,43–61,65–109,120–146,149–165`, raw
`cfg925_results.json:{classes,K_all}`, and its MUTATE JSON/output.

**CFG926 conditionally removes the red-lens excess.** R5 adds `0.172` dex to red
stellar masses, on top of CFG667's `0.123`, while leaving discs at Chabrier.
The graded F1 becomes `0.127 -> 0.048` dex canonical and `0.088 -> 0.009` alt;
the cell split drops to about `0.9 sigma`. All nine declared primary corners
resolve. This changes the mandatory empirical target. However, the asymmetry
carries the result: the slope alone changes the split only `0.02` dex; applying
one relation to both lens classes leaves a roughly `2.1 sigma` split and gives
PARTIAL (MIXED). The colour-window statistic removes only 49% canonical; the
post-hoc SLUGGS ceiling removes 45%. Neither is the graded primary statistic.
Clusters get under 1% of the needed extra mass; dwarfs remain effectively
unchanged. Sources: `CFG926_small_reframings_B/README.md:100–146`, raw JSON
`R5` and `summary`.

R4 fossil `a0` gives zero under FLAT and mostly the wrong sign under the
framework's DE tracking. Only the rival `a0 proportional to H(z)` helps the
dwarf mean, while missing cluster amplitude/slope and pressing the age-slope
guard; the reported low-bracket alt RESOLVES corners do not rescue the
framework's own scale law. R6's round/flat ESD correction is NO EFFECT.
All CFG926 main K checks and its three amended MUTATE tests pass; A1 and the
post-hoc reported sensitivities remain disclosed. Sources:
`README.md:34–98,148–200`. The new canonical note says explicitly that red lenses
may be a stellar-population effect and that dwarf/cluster cores stay open:
`THEORY_CANONICAL_2026-10-18.md:144–148`.

**AG4h narrows AG4g's systematics interpretation.** The primary result is 11/13
shape-driven; zero are distance/inclination-plausible within the declared
coherent-error model, and the other two require implausible TRGB shifts. K1
passes; K2 recovers the planted 30% distance error in exactly 11/13, its frozen
threshold; the inner-half-M/L MUTATE yields 12/13 shape-driven and bites. The
distance-factor label was corrected without changing its numbers. There is no
independent kinematic inclination for these objects on disk, and a radial warp
or non-circular motion is not a single coherent offset. Consequently this is
not exclusion of every inclination/kinematic systematic, nor a cold-mass
detection. Sources: `argon_push/AG4h_pull_systematics/README.md:3–11,13–50`,
`FROZEN_CRITERIA.md:6–16,18–51`, and raw JSON `K1`, `K2`, `counts`, `TD`.

The Q=1 positive subset is reported post hoc, not independently graded:

| galaxy | Delta chi2 from fixed-SPS-plus-coherent-offset versus free M/L | distance information in this lane |
|---|---:|---|
| NGC0024 | 6.91 | SPARC TRGB; no matching CF4 datum |
| NGC5985 | 57.22 | Hubble flow; no independent rotation-free datum |
| UGC00128 | 56.27 | Hubble flow; no independent rotation-free datum |
| UGC00731 | 101.19 | Hubble flow; no independent rotation-free datum |
| UGC08286 | 15.86 | SPARC TRGB; CF4/SPARC = 0.910 |

UGC08286 offers the strongest existing distance cross-check among this subset;
UGC00731 supplies the largest shape contrast but needs an independent distance.
The four CF4 entries are catalog cross-checks, not four guaranteed independent
new distance measurements. AG4h already identifies this follow-up subset.

**Other landed lanes do not close the state problem.** CFG927 is a sealed,
illustrative-survey forecast, not a CMB measurement: ACT-like is blind for
theory-v2 to L=3000; S4-survey-like to L around 2000 is the safer forecast after
continuation/noise sensitivities. Its high-L signal substantially uses the
unmeasured z>1 continuation; SO-like is rule-dependent. This “S4” denotes a CMB
survey class, not the untethering statement. W4-01's seven declared gravity
families select no kappa; its 13/13 checks and MUTATE pass, but recalled starting
equations are explicitly provisional. Neither supplies a microscopic response
selector. Sources: CFG927 `README.md:1–15,81–113,115–150`; W4-01
`README.md:1–11,15–45,83–85`. The current LEDGER reserves CFG928 for regrading
with IMF-corrected red lenses and separate clusters, and CFG929 for cluster-core
reframings (`LEDGER.md:663`); reservations are not results.

## The new empirical operation, with its exact limits

At the declared fixed SPS baryonic model define the vector

`d_i = V_obs(R_i)^2 - V_law[rho_b](R_i)^2`.

Use the complete declared forward model for the baryonic baseline, its coherent
nuisances and covariance. A later canonical test must also check its actual
non-spherical field operator, rather than silently treating the pointwise RAR
as the exact disc solution. In the class-A hypothesis of an additional ordinary
gravitating remnant, the new mass produces a Newtonian radial force.

A **spherical-only control** would require

`M_x(<r) = r d(r)/G = r^2 [g_obs(r)-g_law(r)]/G >= 0`,

`rho_x(r) = [1/(4 pi G r^2)] d[r^2(g_obs-g_law)]/dr >= 0`.

This is not a disc inversion. An axisymmetric positive ring can pull radially
outward inside the ring, and rotation data alone do not determine the vertical
force or a unique three-dimensional density. Therefore rejecting the spherical
control cannot reject every positive-mass explanation.

The useful generalization is forward feasibility: build the Newtonian radial
force matrix `A_ij` of declared nonnegative axisymmetric ring/finite-thickness
and halo basis densities, including external material consistently, and test

`d = A m + noise`, with `m_j >= 0`,

over the measured uncertainty region. Check geometry/support resolution rather
than fixing an arbitrary smoothing length to the answer. Where a basis class is
infeasible, preserve a separating witness or minimum negative-mass requirement;
state its geometry and finite-grid scope. The stellar alternative must recompute
the law after changing `Upsilon(R)` within independent resolved stellar bounds;
it is not generally the same linear Newtonian addition to an unchanged law.
If stellar M/L is unconstrained and extra mass is allowed to trace the stellar
disc, the alternatives can be exactly degenerate. That is a diagnostic outcome,
not permission to choose the cold component by preference.

Why this discriminates: AG4h's `ag4h.py:37–65` only varies a scalar M/L and one
coherent offset. It never asks whether its required profile belongs to the
positive-mass force set. Its M/L-gradient MUTATE demonstrates that shape alone
can arise without an extra component. An arbitrary positive-mass fit would
establish feasibility only, not formation, retention, a new force, or a
parameter-free prediction. A robust failure would instead reject that declared
retained-mass interpretation before adding microscopic latches.

Prior-record check: CFG484 `README.md:70` already tests positive QUMOND phantom
density for ideal isolated exponential discs and negative EFE belts. That is
not the proposed positivity/geometry test of the five measured residual curves.
The inspected AG4h result/code and targeted recent-record search do not execute
this operation. No exhaustive novelty claim is made.

## Outcome and resumption

The original physical closure remains open. The improved empirical priority is
to determine whether the clean rotation-curve residuals require an admissible
extra mass profile once stellar gradients and geometry are accounted for.
This uses a concrete new lead, rather than forcing the old three-population
selector after R5 has weakened its premise.

If a physically admissible remnant survives that test, the bound/released/
restored same-operator susceptibility receipt remains necessary to identify it
with the requested canonical collective state. If radial stellar M/L removes
the shape discrepancy, use those galaxies as baryonic controls and retain the
independent dwarf/cluster closure question. If both explanations remain feasible,
record that degeneracy and the missing stellar/vertical-force observable.

No feasibility solver or new galaxy-data analysis was run in this update. The
delivered result is a pinned reconciliation and a specific falsifiable next
operation, not an empirical verdict on the five residual density profiles.
