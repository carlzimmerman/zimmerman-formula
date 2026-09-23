# Independent reduced-state transport reproduced

Qwen ea49733caad248c6bf1eb8334413a525 contains a real reduced-state flight
simulation. Its scalar s,z updates, Thomson rejection sampler, azimuth and
exit-time correction match the stated model. It raises on path-cap exhaustion.
The original source is preserved byte-for-byte as qwen_candidate.py with origin
hashes. It does not manufacture samples from the target equation.

The local referee's objection that this is a different physical model from
3D transport is false: the scalar reduction is a coordinate reduction of the
same process. Substituting residence time for excess delay is a legitimate
observable-error control, though it does not by itself validate the kernel.
Other local reviews wrongly call different positive seeds nondeterminism and
misinterpret mean(Y)/SE as the residual z score. Those are not valid refutations.

Real limitations: per-path seed ranges in original main and positive modes
overlap in 9,900 of 10,000 paths (99%). They are not independent replications.
The source also clamps all negative square-root arguments, rather than throwing
on large geometry errors. Its next extension should enforce a small tolerance.
These limitations do not justify discarding the correct transport calculation.

## Reproduction and new samples

Both original main results reproduced to 1e-12. The corrected audit then uses
four disjoint ranges of 20,000 per-path seeds, also disjoint from the original
ranges, and two 40,000-photon samples from the separate preexisting 3D solver.
The first audit run accidentally overlapped one original range; `certified/`
preserves that superseded run. `certified_v2/` uses the corrected declared
ranges; its manifest validates against current source. No candidate code changed.

Fresh reduced-solver identity residuals are 0.144,-1.408,-0.866,-0.590 Monte
Carlo SE. Residence-time substitution fails by at least 51 SE. Unscattered
fractions agree with exp(-k) within 0.95 SE and final geometry checks pass.
Between the two implementations, D,D^2,Z,Z^2 means agree within 1.48 combined
SE at both k=1 and k=2. All 30 declared checks pass. These are approximate
sampling statements; final geometry checks do not instrument every internal
clamp. The test does not claim universal numerical validation or novelty.

Later 0585914d20cc4b51841a239b056451ef has a diagnostic counter bug: it counts
the final escape condition as “unscattered” for every photon. That does not mean
its scattering loop never runs. The 992fc4736a0a41ac8e45ea6daa928383 revision
fixes the counter but inverts the negative check, causing protocol rejection
despite reasonable main moments. Reuse the verified root, not its regressions.

The conditional uniform-model relation now has a separate analytic derivation
and two transport implementations supporting it at finite precision. Novelty
remains unverified; see ../boundary/SOURCES.md. No observational claim follows.
The next research question is whether the uniform-model consequence
Var(D)>=2(E[D])^2/5 survives bounded but strongly decreasing radial opacity.
That extension is a conjecture to test, not a theorem or a new discovery label.
