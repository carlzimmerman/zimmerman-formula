# YM-C1-C source and input provenance

Assigned checkpoint base: `b73311096299e2f1816be00036ccdb2922bc44d4`.
First observed shared-workspace HEAD: `a0dc7c516f7a5c33ae9db03a9af6340ffdc74d2c`.
The assigned source I15 was compared against the assigned base with `git diff`;
there were no differences. No chronology is inferred from the moving HEAD.

## Project inputs

1. `../CONTRACT.md`, SHA-256
   `563555c68bafae04e62b69fef58ffb5f8f8aac8db93afafc9d4e72a98052f114`.
2. `../../spectral_spine_closure_2026_09_22/i15/PROOF.md`, SHA-256
   `223d5d0f7ba6bd6fc7cfeffc8cfa18ac32c906e7172af2f4acd2708b5e149b72`.
   Used its exact Hamiltonian convention and §4 strong-coupling conclusion
   as supplied input. This route did not independently reproduce Yarotsky's
   proof or audit every part of I15.
3. Root's message supplied the candidate inverse-gap estimate quoted as (13).
   Its applicability is explicitly conditional. No root artifact was used as
   an authenticated theorem at the time this record was written.

## JW: official problem definition

- Authors/title: Arthur Jaffe and Edward Witten, *Quantum Yang–Mills Theory*.
- Primary locator: [official Clay PDF](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf).
- Version: unversioned 14-page official PDF served at that locator; checked
  2026-09-22. No changing arXiv version is involved.
- Authenticated and read: PDF title, authors, §3 on printed p.5 and §4 on p.6.
- Exact extraction: §4 requires the all-compact-simple-group target, a
  nontrivial theory on R^4, the cited axiom strength, positive finite
  Hamiltonian mass, curvature-based local observables, and the indicated
  ultraviolet behavior. §3 fixes the vacuum and positivity conventions.
- Source status: authoritative definition of the target, not a proof of it.
- Translation: source H is this route's physical K; source Omega is Omega;
  its mass m is the spectral bottom above the unique vacuum. Lattice x and
  a are not supplied by this source.
- Application: valid for specifying the target. It supplies none of CT,
  (8), (12), or a cutoff-to-continuum construction.
- Cache: read-only project cache lookup reported `cache_present:false`.
  No cache initialized, because the assigned write scope excludes the root
  cache and ignore rules. No PDF was retained; local source content hash is
  therefore unavailable. Browser extraction was available and inspected.
- Search scope: official Clay site and exact official PDF, English,
  target-definition verification only. No novelty search was performed.

## Conditional beta-function calculation

PROOF.md (14) is an explicit hypothesis with abstract beta_0,beta_1. Equation
(15) follows by reciprocal-series expansion and integration, reproduced
there. No source is asserted to prove (14) for the I15 Hamiltonian or every
magnetic normalization it covers. In particular, no pure-SU(N) coefficient
is inserted without an authenticated normalization dictionary.

A bounded search for primary beta-coefficient material found candidate PDG,
research-paper, and lattice-source locators. They were not used as proof
leaves: the accessible candidate snippets were not an exact source check,
and some full-text fetches failed. This affects no theorem C1--C4, which
does not assume perturbative coefficients. The RG agent independently also
kept its scaling argument in abstract parameters.

## Attribution and overlap

All transfer arguments are direct spectral-theorem consequences written out
in this route. They are not claimed new. Counterexamples are fully specified
operators; no numerical experiment supports a universal statement. The
Yang–Mills application remains conditional on the named construction and
uniform estimates.
