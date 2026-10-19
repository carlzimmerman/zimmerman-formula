# Actual lattice proton points in the full Born kernel

**The data acquisition succeeded, and a new physical-QCD finite functional was calculated without a form-factor ansatz or numerical alpha.** It uses the individual-proton Sachs points of [Alexandrou et al., arXiv:1812.10311v2](https://arxiv.org/abs/1812.10311v2), Appendix B/Table VI, PDF page 26, including the source's light disconnected current contribution. It does not provide a continuum/full-current proton mass slope or the target vacuum ratio.

The public versioned source contains `table_ffs.tex`, with nineteen nonzero-Q² proton GE/GM pairs between **0.057 and 0.963 GeV²**. We authenticated the exact TeX against the PDF text and visually inspected the printed table. The Q²=0 magnetic entry is `NA`; that row is excluded, with no magnetic-moment fit or endpoint extrapolation. The source's dipole, z-expansion, Galster, radius and magnetic-moment fits are not used.

Using the full Born kernel, which combines both Compton amplitudes **and its elastic subtraction**, the declared nonuniform trapezoid in `z=sqrt(Q²)/(2m_ref)` gives

    I_tab = 0.002522992696893573,
          = 0.013772451332589844  [dispersive elastic]
           -0.011249458635696271 [Born subtraction].

The normalization is the dimensionless coefficient per `u=e²`: a first-order mass estimator would be `delta M/m = u I_tab`. Its coefficient per alpha is `4 pi I_tab = 0.031704861286486197`; no numerical alpha was chosen. The large subtraction illustrates why integrating the dispersive elastic term alone is insufficient.

The exact numerical object is a finite source-point functional, not a controlled approximation to the continuum integral. The table has no joint GE/GM covariance. At fixed printed Q² and source mass, the printed marginal errors imply a **linearized statistical covariance ceiling** of `0.000700009727622490` per u. This is a bound for the linearized fluctuation with arbitrary admissible correlations, not a confidence interval, the nonlinear estimator's standard deviation or total uncertainty. It excludes mass/scale covariance, source rounding, current normalization systematics, finite volume, lattice spacing, excited states, flavor omissions and quadrature bias.

The conditions on these data matter:

- The cB211.072.64 ensemble has Nf=2+1+1, `am_N=0.3813(19)`, `a=0.0801(4) fm`, and `m_pi L=3.62`. Its source scale is calibrated from the **measured average nucleon mass 0.9389 GeV**, used explicitly here. This is not an input-free QCD mass prediction or a variation along a newly calculated QCD+QED matching path.
- The proton columns include connected u,d and light u+d disconnected matrix elements. Strange/charm are dynamical sea flavors of the ensemble; strange/charm electromagnetic current insertions are not authenticated in these columns. The observable is restricted accordingly to the source's light-current elastic sector.
- The published points already involve ground-state/plateau fits and source current normalization. The disconnected local current uses `ZV=0.728(1)`; the source's connected current is conserved. These are imported source extraction choices. Our new functional performs no fit to Q² or to a target.
- Squaring the total light-current elastic vertex includes its coherent disconnected contributions. It does not isolate or complete the disconnected **two-current non-Born** sea response.

The [bounded run](run_001/manifest.json) completed and its current-input v2 manifest validates. It checks all nineteen source transcriptions and Born decompositions, eighteen segments against the nodal implementation, constant/linear quadrature invariants and analytic versus numerical sensitivities. See [derivation](DERIVATION.md), [inputs](INPUTS.json), [results](run_001/RESULTS.json), [source receipts](SOURCE_RECEIPTS.json), [contract](COMPUTATION_CONTRACT.json) and [reproduction command](REPRODUCE.md). Sixty-digit internal arithmetic provides reproducibility, not sixty-digit physical precision.

The actual change at the previous gap is therefore concrete: the elastic Born kernel now contains an evaluated finite functional of physical-point QCD data with included light disconnected vertices, rather than only a free-Dirac benchmark. Missing low/high photon regions, the all-flavor non-Born tensor and its sea covariances, finite QCD matching, and the independently required global curved-vacuum coefficient remain. Neither R(alpha) nor a preferred alpha follows from this partial result.
