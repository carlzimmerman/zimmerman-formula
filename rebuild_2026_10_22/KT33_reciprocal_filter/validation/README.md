# Independent periodic operator check

`run/manifest.json` records a completed, validated bounded run of four tests
and the four-grid force diagnostic in `run/results.json`. This is independent
of the axisymmetric Milky Way and Cassini quadrature implementations.

The tests check an exact Newtonian Fourier mode, the zero-width limit, the
prior audit's analytically integrated two-mode nonlinear response, and net
force for a nonspherical multi-mode density in a fixed external field. The
old map's force remains 0.0003442870684 in dimensionless units; the completed
map's magnitude is below 2.9e-14 on grids 16, 24, 32 and 48.

Terminology clarification: the test name and contract use “asymmetric” for
this benchmark. The density `2+cos(x)+0.4 cos(2x)+0.1 cos(y+z)` is itself
inversion-even. The fixed external field breaks the symmetry of the full
problem. The check is meaningful for this declared configuration; it does
not assert a test over all asymmetric sources or prove isolated-boundary
momentum conservation. Pinned executed code and contracts are preserved.

`independent_review/` contains additional independently authored probes of
the inherited finite-volume Jacobian and a Gaussian-times-solid-harmonic
convolution. Its `provenance.json` maps exact copies to their original
execution paths, commands and hashes. These probes have that narrower
provenance, not bounded-run v2 manifests.
