# Evidence audit

Scope: own clock/radiation/supply derivations, numerical scripts and interpretation; self-review, not independent referee approval. No complete formation simulation or data fit was run this turn.

- Primary run completed: six local checks passed. Four selected quadrature repeats were insufficient to certify the whole grid.
- First full-grid refinement failed at JSON serialization of a NumPy bool. Its script, failed manifest and logs remain unchanged. refine_v2.py changes only bool serialization.
- Completed refinement_v2 exposed two failed integration gates: up to 12.8% relative power difference between 128 and256 Gauss-Laguerre nodes, and38.2% between64 and256 in retained weak cases. The sharp small-radius endpoint caused this; the failure is retained, not relabeled a pass.
- endpoint_check.py uses an independent log1p integration coordinate and Gauss-Legendre nodes. Across all125 radiating grid cases,256 versus512 nodes agree to1.53e-12 relative power. Integrating u to50 omits an exp(-50)-suppressed tail; the positive decreasing source integrand makes the cutoff harmless at reported precision. This is numerical convergence evidence, not a formal floating-point error proof.
- Endpoint output supersedes primary-grid radiation numbers. Weak-field tests were recomputed with the new quadrature and denser spatial sampling. The best weak case and conclusion are unchanged; some small-radius values shift.
- Independent segmented growth solves agree within6.39e-10 absolute normalized amplitude. The exact all-dust reference is1 to1.63e-11.
- Analytic checks: mass-conserving source has S=(epsilon/2)R partial_R Fourier[h^2]; radiation prefactor includes the inherited1/(4pi) field-energy normalization; fixed-size power scales as mass^4; virial frequency at fixed overdensity cancels mass. No additional2pi belongs in angular frequencies.
- Scope caveats: prescribed periodic source; Newtonian energy proxy; no nonlinear phase backreaction; static phase bound does not bound all driven amplitudes; no primordial spectrum, live baryons, accretion kernel, transport distribution, halo catalogue, lensing calculation or observational refit. A monochromatic radiation gap does not forbid high-frequency transient emission.
- Density profile caveat: Gaussian width is set to characteristic R200; it is not a self-consistent enclosed200critical Gaussian radius. Different size conventions change numbers and require a rerun.
- Interpretation gates: unique mass selection false; population closure false; joint observational preservation false. Absence of a successful mechanism in this bounded probe is not a general no-go theorem.
- Prose/equation self-review covered CONTRACT.md, DERIVATION.md, RESULT.md and this audit, checking units, threshold direction, source-harmonic meaning, mass moments and the separate growth/age backgrounds. No predecessor files were edited.
