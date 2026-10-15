# Angular route checkpoint

VC4-ANGULAR-2026-10-15. Starting task base
`a553a4a663d393f29ec5da69c8cae68c164bb5b0`; live checkout advanced during
parallel work. Immutable actual inputs are pinned in `inputs/source_manifest.json`.
All writes of this route are inside this angular directory.

Result: a new analytic static theorem for every nonspherical harmonic sector
of the actual joined critical body. For l>=2, the complete density/common-shape
Hessian has the explicit coercivity bound in PROOF.md (16), including arbitrary
relative fluid profiles. For l=1 it is positive after removing translation;
material relabelings remain static nulls. The frozen radial proof supplies
l=0. Independent reconstruction now accepts the new phase, common-edge
gravity and all-harmonic shell derivatives as proved within the declared
model. This closes the static angular comparison-energy obligation. It
does not close dynamic interface health.

Proof: `PROOF.md`; elementary flux/kernel details: `DERIVATION_APPENDIX.md`;
adversarial self-review: `AUDIT_SELF.md`; completed independent review:
[EINSTEIN_AGENT_AUDIT.md](EINSTEIN_AGENT_AUDIT.md). Its primary verdict is
proved as written at the static hybrid configuration-energy scope. This is
a separate same-team reconstruction, not external peer review or formal
verification. The frozen proof
`0b9f3fdb54c22303084a43cf39354de15709995f20e2371fdd4691985e88583d`
and its code/run bytes remain unchanged; its opening awaiting-audit note
records the historical state when that immutable proof was written.

Evidence: 219 exact checks passed in `run_exact/results.json`; the version-2
manifest validates against current input/output hashes. Conservative exact
coercivity constants are greater than 0.019999935999666665 for the density
norm and 0.29999949548455734 per (l-1)(l+2) shape norm. Finite Legendre
checks cover l=0..16 and ratio checks l=2..64. The analytic proof covers all l.

Executed attempts and information gained:

- Initial l=2 electric-shape destabilization attempt: the shape term is
  negative in part, so bulk convexity alone fails as a proof method. The
  complete Gauss/phase term is nevertheless bounded by the exterior Maxwell
  square and is tiny compared with the actual counted capillary tension.
- Relative-species counterexample attempt: allowing independent arbitrary
  density profiles, including mixed shape/relative directions, is covered
  by the same positive pressure norm and small-G bound. This is not a
  finite-dimensional trial-family result.
- Wall gravity attempt: actual area-mass variation gives a negative shape
  term, but its size is suppressed by G/c^2 and Gsigma/c^4. Keeping its exact
  coefficients reveals the l=1 translation cancellation.
- Strict positivity in all displacement variables: refuted by exact
  weighted divergence-free tangent relabelings. The correct theorem is on
  physical density/shape variables, with an explicit translation quotient.

Next executable discriminator: the separate dynamical boundary characteristic
problem, including velocity/magnetic mixing and exterior Maxwell radiation.
The independent phase and shell-Hessian reconstruction has completed. No
unperformed numerical simulation or larger finite grid is needed to
strengthen this static estimate.
