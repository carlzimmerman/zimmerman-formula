# Opt-in common Fourier modes for future X48 convergence studies

The historical `x48_zoom.py` and all running/checkpointed jobs are unchanged.
Reusing its seed with a different grid size does not reuse the same physical
low-frequency realization: both Gaussian draw arrays change shape. Its
unconstrained complex draws also do not impose the required Hermitian relation
on the k_z=0 rFFT plane. `irfftn` returns a real field but projects those
inconsistent boundary coefficients; a round trip need not recover the input.

`x48_common_modes.py` is an opt-in correction helper for a future, separately
named run. It keys each Gaussian coefficient to `(seed, nx, ny, nz)` and uses
the same key plus conjugation for the opposite mode. For a fixed physical box
and P(k), `dk/ng**3` agrees on shared interior modes at different resolutions.
The convention is E|dk/ng**3|^2 = P(k)/L^3. P(k) is in volume units and k in
inverse-length units. The mean mode is zero.

Even-grid Nyquist planes are deliberately zero because their self-aliasing
changes on refinement. The k_z=0 plane is Hermitian; odd grids have no Nyquist
planes. This is a new, disclosed realization convention, not a reproduction
of old seeds. An optional common physical `kmax` makes a band-limited field.
The separate `x48_zoom_common.py` launcher wires the helper into a copy of the
historical function in memory. It masks P(k) with the helper's shared support
before drawing dk and constructing every Hoffman–Ribak covariance. The power
normalization on retained modes is unchanged. It replaces the random-dk draw and
records the generator, cutoff and source/helper hashes in checkpoint metadata.
It requires a new work directory and rejects legacy/incompatible resumes.
Check the invocation without loading cosmology or starting a simulation:

```bash
python3 rebuild_2026_10_22/X48_native_cf_zoom/x48_zoom_common.py --common-kmax 4 --work NEW_COMMON_RUN --dry-run --mass 1e12 --seed 1 --ng 48
```

The numeric cutoff above is an invocation example, not an approved physical
convergence setting. It must retain at least two distinct nonzero |k| shells
for independent height and Laplacian constraints; otherwise their covariance
can be singular. Dry-run checks wiring and run identity, not that physical
condition or target solvability. A future authorized run removes `--dry-run`; common-mode
resumption uses the same command/identity with `--resume`. All other integration
arguments pass through to the historical launcher. The integration's actual
random-field prefix and its constraint-covariance/correction code are tested
with fixed synthetic constraints, without running the collapse calculation.
Direct helper usage is also available:

```python
from x48_common_modes import gaussian_rfft
dk = gaussian_rfft(ng, L, seed, lambda k: P_of_k(k), kmax=common_physical_cutoff)
d_r = np.fft.irfftn(dk, s=(ng, ng, ng))
```

**Remaining convergence obligation.** This helper fixes the unconstrained
Gaussian coefficients, not the whole experiment. X48 subsequently computes
grid-dependent Hoffman–Ribak covariance, target peak and curvature, and a
constraint correction. Adding high-frequency modes changes these quantities
and can change the corrected low modes. Before a paired convergence claim:

1. Declare a common physical box, spectrum, band limit, peak constraints,
   target normalization and particle-selection convention. Use a shared
   constrained master field restricted to each grid, or demonstrate that the
   chosen constraint discretizations preserve the required paired realization.
2. Verify matching *post-constraint* density and displacement modes and actual
   constraint residuals. Verify the newly added modes separately if the physical
   band limit is deliberately increased.
3. Vary particle/force resolution, softening, time step and profile estimator;
   compare paired halos in every claimed mass bin with declared tolerances.
   Seed variation alone is not a convergence study.

The bounded checks cover shared modes at ng=8/12/16, real-field round trips and
Parseval at ng=7/8/12, and 256 fixed seeds for approximate power and cross-mode
covariance at ng=8. These are implementation evidence, not a proof of continuum
convergence or physical halo formation. No simulation has been launched.

**Fix-forward review correction.** The first launcher version replaced dk but
left P(k) unmasked in the constraint covariance. That was inconsistent with
the random field and reintroduced excluded modes. The new support/covariance
regression failed on that version (maximum normalized excluded coefficient
0.06823) and now passes, using actual transformed HR code and an independent
full complex-grid covariance oracle. It checks a radial cutoff and a larger
cutoff that still excludes Nyquist planes, as well as constraint residuals.
`technical_fixes/run_CORRECTED_002` supersedes `001` for the launcher; the
earlier evidence is preserved. This does not establish matching of the
astrophysical post-constraint targets across different grid resolutions.
