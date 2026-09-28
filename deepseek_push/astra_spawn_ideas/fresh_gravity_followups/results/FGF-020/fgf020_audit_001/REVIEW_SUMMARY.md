# FGF-020 proof-only worker result — not yet orchestrator accepted

Actual worker: Astra agent `/root/dynamics_precision`; not a DeepSeek run.
Outcome: **supports_scoped_claim**. DM1's integrated-moment counterexample
survives independent reconstruction. No new numerical experiment was run.

For a shell with density L>0 and fraction 0<epsilon<1, exact positive
feasibility on a nonatomic volume requires and permits

    epsilon <= V/[V+(L-mu)²],  epsilon L < mu.

The complement has mean m and variance v given in the raw audit. If v=0 it
is constant. If v>0, complementary densities m/2 and m+2v/m, with probabilities
4v/(m²+4v) and m²/(m²+4v), explicitly realize the moments with positive density.
This extends DM1's sufficient equal-volume construction; it does not correct
an asserted sufficiency claim that DM1 never made.

At variance-bound equality with L!=mu the constant complement is
m=(mu L-nu)/(L-mu). It is positive for L<mu or L>nu/mu. At L=nu/mu it vanishes
and is excluded by strict positivity. L=mu retains epsilon<1; zero global
variance instead forces density mu almost everywhere.

For every finite L the shell can be chosen thin enough to preserve both
moments, so two integrated numbers do not supply a finite universal density
bound. A physical lower feature width would add a bound; an instrument PSF
alone is not such a width. Piecewise spherical volumes are explicitly realized
in the independent derivation.

The exact-rational source checks are correctly separated from their floating
Q/R examples. Rational moment parameters do not imply rational bulk densities:
the latter may include square roots, whose display rounding is not used for
positivity. The eight force examples use both normalizations and distinct
vacuum/frozen-H branches, but are synthetic local force conversions.

Preserving an unweighted density-squared moment does not preserve real detector
counts at changed temperature. The missing response is the actual weighted
rho² Lambda_E(T,Z,composition) map with its detector/projection dependence.
At fixed thermal pressure, changing density changes ideal-gas temperature.
The audit supplies a purely illustrative positive emissivity-functional
counterexample to universal count preservation, without pretending it is a
cluster plasma model.

All five candidate snapshot hashes matched; the candidate manifest passed
provenance validation. This review inspected the source code and established
its moment/positivity logic algebraically. It did not rerun candidate numerical
outputs, evaluate a plasma/detector model or fit any real cluster. Source and
output hashes, exact proof coverage and absent computational bounds are
recorded in result.json.

Next: obtain an independently authenticated physical width/resolved response
and thermal emissivity map before testing whether the moment-compatible family
can satisfy additional observations. No current result manufactures a global
hydrostatic or detector-compatible cluster solution. Shared tasks, queue,
claims and candidate files were not edited.
