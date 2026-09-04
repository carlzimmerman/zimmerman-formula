# Run record

Repository state at implementation start:

- commit: `edff7fddedb24f76af60a1133e49f1110ab38dce`;
- branch: `main`;
- worktree: dirty from unrelated pre-existing files;
- Python: 3.9.6;
- SymPy: 1.14.0;
- platform: macOS 26.5.2 arm64;
- randomness: none.

## TDD record

1. RED — missing derivation artifact

   ```bash
   PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_hpi_delta_full_spherical_2026.py
   ```

   Exit status: `1`. One test ran and failed because
   `hpi_delta_full_spherical_2026.py` did not exist.

2. Minimal GREEN — artifact existence

   The empty derivation module was created only after the first RED.

   Same command, exit status: `0`; one test passed.

3. RED — behavior contract

   The complete eleven-test behavior contract was installed before the
   implementation.

   Same command, exit status: `1`; setup failed with the expected missing
   `derive_full_spherical_audit` API.

4. First implementation run

   The initial symbolic implementation remained live in SymPy's generic limit
   expansion for more than four minutes. It was interrupted with exit status
   `130`; the traceback located the bottleneck at the Puiseux exponential limit.
   The exact constitutive Taylor jet was then taken before substitution, which
   computes the required finite coefficients without altering them.

5. GREEN — complete behavior contract

   ```text
   Ran 11 tests in 4.992s
   OK
   ```

   Exit status: `0`.

6. Executable certificate

   ```text
   [PASS] spherical geometry benchmarks
   [PASS] barred kinetic action expanded exactly
   [PASS] lambda equation varied
   [PASS] radial shift equation varied
   [PASS] source-free isolated auxiliary branch derived
   [PASS] exact N A R equations varied
   [PASS] raw and boundary-reduced actions agree
   [PASS] radial diffeomorphism identities
   [PASS] smooth center compatibility derived
   [PASS] Puiseux branch solves both center equations
   [PASS] curvature coefficients derived
   [PASS] curvature benchmarks
   [PASS] mutations are live
   ```

   Exit status: `0`; 13/13 certificate predicates passed. Cold runtime was
   approximately 70.4 seconds.

7. RED/GREEN — full-action metric-restriction regression

   A regression requiring the full barred-kinetic (N,A,R) Euler derivatives
   to vanish only after substitution of the derived auxiliary-flat branch was
   added first. The first run exited `1` with the expected missing-result
   `KeyError`; after implementation, the same command exited `0` with 11/11
   tests passing in 4.981 seconds.

## Derived certificate

```text
isolated branch: bar_Kij=0, beta=0, D2(lambda)=0
smooth requirement: rho_0+3 p_c = Lambda/(4 pi G)
c^2 = [4 pi G(rho_0+3 p_c)-Lambda]/(3 ell_0)
sqrt(r) R4 -> 5 c
r Kretschmann -> 43 c^2
status: DEAD_UNDER_ISOLATED_STATIC_CLASSICAL_REGULAR_CENTER_REQUIREMENTS
```

## Fresh final verification

After the implementation and report were finalized, the complete local audit was
rerun from the isolated directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest -v test_hpi_delta_full_spherical_2026.py
PYTHONDONTWRITEBYTECODE=1 python3 hpi_delta_full_spherical_2026.py
```

- unit tests: exit status `0`; 11/11 passed in 4.908 seconds (5.470-second
  command wall time);
- executable certificate: exit status `0`; 13/13 predicates passed
  (5.346-second command wall time).

The three nearest committed closure suites were then rerun without writing byte
code:

- `hpi_delta_covariant_lift_2026`: exit status `0`; 14/14 passed in 8.581
  seconds;
- `cde_hpi_delta_2026`: exit status `0`; 16/16 passed in 1.894 seconds;
- `exact_mond_regular_center_no_go_2026`: exit status `0`; 15/15 passed in
  4.897 seconds.

The computation manifest records the local-audit verification command, its
runtime, and SHA-256 digests of every non-manifest artifact.

After the full-action metric-restriction regression, that exact combined
manifest command was replayed at `2026-09-04T04:46:39Z`: exit status `0`,
11/11 unit tests and 13/13 executable predicates passed, with a measured
command wall time of 10.667 seconds.
