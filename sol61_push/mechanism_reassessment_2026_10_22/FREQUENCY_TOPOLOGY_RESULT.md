# Frequency folds must be resolved before continuation

The stored orbital data show substantial nonmonotonic dependence of radial frequency on energy. A single inverse energy-versus-frequency map is therefore unsuitable for the planned spectral-density reconstruction. This changes the next implementation step: branch splitting and turning-point treatment must precede a continued-pole solve.

## Finite calculation

The audit reads the A10000 action samples directly: 4096 orbits at order64 and 16384 at order128. At each fixed sampled u=L², energy increases along the row, with E=-Q-u/2. The constant offset drops out of frequency derivatives. We test all adjacent frequency steps and compare PCHIP roots with direct sign brackets for harmonics1–32 at omega=.8228. This audit excludes exact energy endpoints and unsampled angular momenta.

| action order | rows with any reversal | rows with interior minimum more than 1e-5 below both sampled endpoints |
|---|---:|---:|
|64|15|15|
|128|32|30|

The two extra reversal rows at order128 are near the largest sampled angular momenta and have tiny fluctuations. They are not evidence for additional physical folds. The prominence threshold is a diagnostic separation, not a rigorous error bound. The substantial minima occur on rows0–14 and0–29 respectively. Their smallest prominences are about.00157 and.000868, respectively. The first grids are not nested in angular momentum; these counts do not establish a precise phase-space fraction.

All interior PCHIP root counts agree with adjacent sign brackets. At order64 the counts for harmonics1–7 are1,7,59,41,22,8,3; at order128 they are2,13,119,83,45,19,6. These are counts over angular-momentum rows, not integrated spectral weights or distinct global resonance families. No represented interior roots occur at harmonics8–32. Earlier endpoint-completed direct-orbit calculations remain the stronger source for actual absorption; this diagnostic does not replace them.

## Consequence for the spectral-density integral

Our preceding derivation uses the sum over all energy roots of n Omega(E,u)=s, weighted by 1/|Omega_E|. A substantial smooth minimum can create two roots, and at their meeting point that denominator vanishes. If locally

    Omega(E,u)=Omega_min(u)+a(u)(E-E_star(u))²/2+...,

with a>0 and nonzero Fourier numerator, then the fixed-u spectral density has a conditional inverse-square-root behavior in s-n Omega_min(u). This follows directly by solving the quadratic for the two energies and evaluating the Jacobian; it is not a newly established theorem about the full model.

For the substantial sampled minima, approximate frequencies span .123–.177 at order64 and .121–.176 at order128. Their fifth and sixth harmonic ranges straddle .8228. This flags those harmonics for turning-point treatment. It does **not** locate an exact fold at a sampled u, certify continuity between rows, or prove that the fully u-integrated spectral density is singular at .8228. Integration transverse to a moving fold can smooth the fixed-u singularity. Global endpoints and stationary values of the fold-frequency curve require separate analysis.

The previously dominant third-harmonic absorption is not invalidated by this finding. Nor does dominance alone justify discarding the other harmonics when continuing the whole matrix. A useful next calculation is to locate actual minima with direct orbit evaluation, track their frequencies versus u, and integrate in coordinates that remove the square-root endpoint before fitting an analytic spectral numerator.

## Evidence and limits

frequency_topology.py and frequency_topology_run preserve the initial raw-reversal diagnostic. frequency_topology_v2.py adds the prominence diagnostic without modifying that earlier evidence. Both runs completed; both manifests validate. The v2 run passes five finite checks: finite inputs, energy ordering, interpolation/bracket agreement, reversals on both grids, and substantial minima on both grids. Reproduction argv, versions, input hashes and outputs are recorded in frequency_topology_v2_run/manifest.json. The checks establish properties of the stored samples and their interpolation, conditional on numerical accuracy; they do not independently validate the original orbit integrations.

No new physical damping rate, analytically continued pole, formation mechanism, or novelty claim is established. The result identifies a concrete obstacle to a naive continuation and specifies how the next calculation must handle it.
