# Claim audit: density-free transport closure

Primary verdict: **proved as written**, within the approximate stochastic
transport model specified in THEOREM.md. This is an author self-review.
Astrophysical applicability and global novelty remain unestablished.

The dependency chain is:

1. Straight flight plus the specified conservative scattering kernel defines
   the transport generator. The source is central and the boundary spherical.
2. F(r)=2 integral_0^r s kappa(s) ds makes the generator of
   F(r)+2 x dot u equal to the constant 2c.
3. Bounded opacity and radius justify the stopping limit. The boundary's
   angular term cancels exactly in the distant-observer delay.
4. For constant density, a separate photon-count compensator links mean
   scattering count to mean residence time.
5. The independently derived Maxwell Doppler variance links the spectrum to
   that count. Bounding the exit-angle mean by [0,1] eliminates density and
   optical depth and produces the lag interval.

Only step 5 uses the thermal frequency approximation. The radial delay identity
is a spatial theorem and does not use a fitted line shape.

| Obligation | Status | Evidence |
|---|---|---|
| Distinct inputs and prediction | Passed | R, T_e and spectral variance are inputs; timing is predicted |
| No independent mean-free-path assumption at final flight | Passed | Compensator includes the censored last flight |
| All scattering orders, not only diffusion | Passed | Generator proof; tests from tau=0.03 to 30 |
| Optional stopping | Passed | Uniform positive escape probability bounds all exit-time moments |
| Observer normalization | Passed under stated symmetry | Central isotropic source and spherical medium |
| Frequency variance | Passed in linear Doppler model | Earlier proof plus independently sampled 3D thermal velocities |
| Uniform-density scope | Essential; tested adversarially | q=99 gradient violates the purported uniform band by 12.64 MC standard errors |
| Central-source scope | Essential; tested adversarially | Uniform volume source differs from central lag formula by 63.83 MC standard errors |
| General radial profile identity | Passed | Both gradient models satisfy the exact weighted integral |
| Radius equals continuum photospheric radius | Not established | Explicitly excluded from the theorem's inputs |
| Observed JWST confirmation | Not established | No matched radius, temperature, full variance and lag dataset fitted |
| Global originality | Not established | Bounded source search cannot establish absence of prior art |

The simulated gradient kappa(r)=a(1+99 r^2), with total radial optical depth 10,
has measured mean delay 7.4135 R/c; the exact radial formula predicts
7.42647 R/c. Treating it as a uniform cloud with the same optical depth predicts
5 R/c and fails by 96.84 Monte Carlo standard errors. Its line variance also
violates the density-free uniform lag–width band. These are genuine model
counterexamples, not tests that repeat an implemented formula.

The 600,000 trajectories use the pre-existing continuous-flight transport.py
without adding the new identities to its propagation logic. The theoretical
predictions are evaluated only after the trajectories escape. Spectral shifts,
collision counts and path lengths are separately accumulated.

No Lean certificate is claimed. The proof is a written mathematical derivation;
SymPy checks only its polynomial generator example and algebraic reductions.
The Monte Carlo run is a finite corroboration and scope test, not its proof.

The numerical example is an application of the formula to specified inputs,
not an observation or statistical detection. Its full-Laplace FWHM conversion
must not be applied to a Gaussian/exponential mixture without using the full
second moment. Using total line variance as an upper limit preserves only the
upper lag bound, not the lower one.
