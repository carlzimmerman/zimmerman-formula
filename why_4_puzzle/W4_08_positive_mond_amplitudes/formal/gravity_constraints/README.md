# Physical constraints and the normalization discriminator

**The original goal remains open.** Criteria-only commit 201229b5f
continues the clock/flux checkpoint f1565bc90. Reviewed evidence is
committed as 590d17d77; campaign entries K701-K706 record the separate
scopes. Regeneration passes 4/4 and adds no determinate prediction. [RESULT.md](RESULT.md)
derives the covariant actions, their retained modes and actual physical
force/density dictionaries. No healthy microscopic selector is found.

Pure BM at lambda=1 on its actual de Sitter vacuum retains a scalar with
positive kinetic energy and no quadratic restoring force. Both lapse
and shift equations, and the physical-wave-number redshift boundary,
are essential. This repairs an overbroad inference from a fixed-metric
tilt test. It does not certify nonlinear or quantum health. The explicit
f_delta deformation preserves the vacuum and all homogeneous quadratic
constraints while changing the MOND cubic: those constraints cannot
select the normalization.

For the rational prototype, a specified c1-only covariant bosonic
completion has a consistent local Bianchi-I background and an exact
frozen finite-k growing band. A conditional weak-gravity continuation
requires a regular harmonic/constraint reduction and a valid cutoff
window. A complete finite-coupling constraint matrix and microscopic
validity proof have not been supplied.

Universal conformal matter coupling gives G_UV=G_t+G_s and
xi_V0=f^3(125pi/128), with a free scalar fraction f. A density inferred
from Friedmann with G_UV differs from V0 by G_cos/G_UV. Using that
inferred-density footing, the target would require f>1/4 and local
unscreened gamma_UV<1/2. This is a downstream failure of this simple
matter completion, not a selection equation or an all-MOND exclusion.

[GravitySelection.lean](GravitySelection.lean) verifies fourteen exact
conditional statements: shift/lapse identities, redshift subtraction,
positive reduced kinetic coefficient, force/amplitude identities,
the inferred-target PPN inequality and normalized band-polynomial signs.
It does not prove the covariant expansion, physical mode identification,
PDE evolution, source dictionary, density interpretation, actual-pi
bounds, quantum health or microscopic selection. W4-08 has nine partial
modules; it has no end-to-end proof of the requested result.

The final module and the true rational controls pass. Three separate
mutations omit the redshift cancellation, assert unchanged amplitude
after doubling C3, or import scalar-only xi into the combined force.
Each fails solely at False. [check_evidence.py](check_evidence.py) binds
this additional contract to the unchanged raw runner, checks fourteen
standard-axiom prints, pins, resources, and all final input/log/object
hashes. [VERIFIED.json](VERIFIED.json) records its exact scope.

Development logs are preserved. dev01 had unused-order warnings and a
redundant ring tactic after field_simp had solved the goal. dev02 was
accepted by Lean but the unchanged runner rejected a wrapped axiom list.
final_gravity failed on an unsupported pretty-print option;
final_gravity02 was accepted by Lean but still hit that parser limitation.
The final source uses a shorter theorem name, preserving the statement
and proof; final_gravity03 passes Lean and the unmodified runner with
no warnings. No earlier rejected run is counted as final proof evidence.

Reproduce from the repository root, with fresh evidence-directory names:

```sh
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py gravity_constraints/GravitySelection.lean gravity_constraints/runs/local_gravity
python3 why_4_puzzle/W4_08_positive_mond_amplitudes/formal/verify.py gravity_constraints/controls/Normal.lean gravity_constraints/runs/local_normal
```

Boundary.lean, Normalization.lean and ScalarOnly.lean are deliberate false
controls; run separately and require exit1 with only an unsolved False
goal. One worker, 1024 MiB, 30s CPU and 45s wall apply to each invocation.
No scan, download, broad build, reserved-file edit or simulation
interruption was used. [SOURCES.md](SOURCES.md) distinguishes authenticated
external results from new calculations. [REVIEW.md](REVIEW.md) indexes
independent derivations and their limits.
