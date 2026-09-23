# Scope of the normalization Lean certificate

`NormalizationConsequences.lean` is compiled using the repository's existing `fable_independent_2026/lean_2026` host. It imports Mathlib and declares no custom axioms or placeholders. All six theorem axiom lists are printed in the compiler output.

The theorem meanings are:

1. `coefficient_bound_from_area`: for `0<a<2`, `A>a`, `g0>0`, **assuming** `g0^2 A(A-a)/a <= I`, the measured-Newton-constant expression `8 pi(2-a)a0^2/I` is bounded by `8 pi(2-a)a/[A(A-a)] (a0/g0)^2`. The analytic integral lower bound is a named hypothesis, not a theorem formalized in this file.
2. `same_scale_excludes_half`: for positive `a0` and `I >= (4999999/2) a0^2`, the squared coefficient at `a=10^-7` is strictly below `1/4`. The proof uses exact inequalities, including `pi<4`, with no decimal calculation.
3. `proposed_area_coefficient`: the sharp area coefficient for `a=10^-7`, `A=1/2` is exactly `4999999/2`.
4. `primitive_shift_preserves_flux`: any known derivative is unchanged when a constant is added to its primitive (`HasDerivAt` statement for arbitrary real functions).
5. `two_normalizations`: in the declared AQUAL expression `8 pi/(n^2 F0)`, the distinct choices `n=2, F0=8pi` and `n=2, F0=2pi` give exactly `1/4` and `1`. Together with theorem 4, this certifies the mathematical primitive-constant ambiguity; the association of these formulas with the action is the analytic derivation in the reports.
6. `finite_profile_health_margin_positive`: for `a>0`, `a(1-3sqrt(3)/8)>0`. The analytic proof that the explicit profile's coefficient lies above this quantity remains in REPORT.md.

This certificate does **not** formalize the area integral, the smooth profile's integral, lapse variation, the profile-to-health-bound inequality, or the physical adequacy of the entire theory. Those limits are stated in the Lean file as well as the run contract.

The archival computation record is `lean_run/manifest.json`; the exact underlying compile argv, compiler version, stdout, stderr, and exit code are in `lean_run/compiler_result.json`. The runner pins hashes of the Lean source, wrapper, analytic report, and Lean host's toolchain/configuration/lock file. Existing Mathlib dependencies are supplied by that host. The compile imports its installed dependencies; it does not rebuild the complete Mathlib library from source.
