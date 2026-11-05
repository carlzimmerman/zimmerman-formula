# Structural checkpoint, 2026-11-04

This is a read-only postmortem of KT33/34 and a paper reconnaissance, not a new
physical result. The source records below retain their numerical qualifications.

The normalized claim is that the original baryon family has no common MW and
Cassini epsilon window for equal fixed source/outer Gaussians, the simple nu
function, and sigma=epsilon sqrt(G M_b/a0). Verdict: computationally verified
only in the stated finite ranges, with the independently audited analytic MW
tail bound conditional on its recorded Newtonian baseline and finite mass.
Cassini's absence of a narrow unsampled lower-width island is not certified.

The general obstruction to source-only filtering is variational, not specifically
Gaussian: if B is the symmetric derivative of the phantom-potential map, the
source-only derivative is N+B S, whose adjoint is N+S* B. An energy composed
with a fixed linear source map instead gives N+S* B S. Except where B commutes
with S, the outer adjoint cannot simply be dropped. This does not establish
that all possible actions must use the same composed energy.

The observational obstruction is narrower. KT33 shows outer smoothing removes
needed radial support (one saved canonical cell changes 227.0 to 215.7 km/s),
while the original source smoothing was intended to round the phantom disc and
reduce vertical force. The Newtonian field remains unsmoothed. KT34 places
conservative production MW upper edges at .313549/.465284, versus numerical
Cassini onsets .515606/.592818. Positivity of a kernel does not by itself imply
pointwise monotonic radial force or chi-square with width; KT34 explicitly
enumerated width states instead of assuming that implication.

The MW tail lemma uses finite nonnegative inversion-symmetric sources, zero
external field, simple nu and the explicit Gaussian derivative norm. Its
bound |g_ph(x)|<=2 sqrt(G M a0)|x|/sigma^2 does not automatically extend with
constant 2 to every positive kernel or another nu. The mass rule ties Solar
and galaxy widths by a common epsilon but does not define a filter on an
unsplit host+satellite universe.

Solar EFE is a separate nonlocal Hessian constraint. A normalized symmetric
Gaussian preserves the uniform affine external potential, while the nonlinear
response to the Sun plus that field is anisotropic. KT33 corrected an omitted
origin surface in the old source-only integral: canonical old .480594 times
the ceiling is an archival flux integral, physical source-only is 3.69093,
and the reciprocal Hessian is 1.09159. Outer smoothing lowers the physical
quadrupole, but its required scale conflicts with MW radial support.

Prior routes that must not be advertised as untried:

- The old FRIED_CHICKEN_SPEC already includes inner S and outer S* with
  nu_mono. It supplies no transferred empirical grade for simple-nu KT33.
- CFG653 is a two-sided high-pass action, exactly blind to uniform gradients;
  it already failed its constant-length/host-satellite scale tests. Its
  zero-mode, asymptotic Keplerian, and finite-host leakage issues differ from
  KT34. It is not a clean new replacement for the low-pass model.
- KT26/27 local acceleration-gradient widths erased satellite self-response
  in near-uniform host fields, and used inconsistent variable-width operators.
- KT28's in-plane tidal success depended on dropping vertical tides. KT29/30
  full/trace-free midplane norms produced 33–53 kpc and lost radial support.
  KT31 varying gather added mass and had a failed premise in its check;
  KT32 varying scatter conserved mass but gave K0>=84.5–86 for vc-passing
  cells, versus an upper cut 70.8. None includes the full action variation of
  a density-dependent width.

Three genuinely different action ingredients remain possible on paper:

1. Change nu while retaining the KT33 composed energy. Define H'(g)=
   g[nu(g/a0)-1]. This evades only the simple-nu empirical obstruction; it
   does not solve source composition. A steeper high-field response could
   lower Solar EFE while sacrificing galaxy support. KT13 already tested
   eight *unfiltered* kernels (including power n=2,3,6); these were not a
   reciprocal-filter scan. First test is joint MW radial/vertical plus
   corrected Cassini with fixed baryons and one epsilon, not Solar-only tuning.
2. Introduce an actual variational filter state b with ell=L0 exp(b),
   S_b=exp[div(ell^2 grad)/2], and reduced energy
   E[rho,b]=U_N+U_ph[S_b rho]+a0^2/(4pi G) integral
   {L0^2 |grad b|^2/2+alpha(b^2/2+b^4/4)}.
   Impose b->0 at infinity and vary b, rather than prescribing it from observed
   velocities. On a stationary branch the envelope derivative in rho includes
   S_b* Phi_ph; b's stationarity accounts for its implicit variation. This is
   an illustrative exact static functional, not an established well-posed
   model. L0 and alpha are new inputs. First tests: existence/second variation,
   source relabelling, and a compact source in a smooth host. KT26–32 warn of
   a thin-disc Kz failure. A prescribed A[rho]=S[rho]rho instead needs DA*.
3. A local geometric QUMOND response changes the action density rather than
   smoothing the source. For u solving Delta u=4pi G rho, take the static
   action integral {-rho Phi-[2 grad Phi.grad u-a0^2 P(grad u,Hess u)]/(8pi G)}.
   Its physical equation is Delta Phi=(a0^2/2)[partial_i P_{u_i}
   -partial_i partial_j P_{u_ij}]. A concrete rotationally invariant geometry
   term can use C=P_perp Hess(u) P_perp-(P_perp/2)tr(P_perp Hess(u)),
   P_perp=(|g|^2 I-g g^T)/(a0^2+|g|^2), and add ell_g^2 C:C/a0^2 to the
   ordinary QUMOND density. C vanishes for an isolated spherical potential,
   so this changes nonspherical response without changing that exact branch.
   ell_g is a new scale and the sign/coefficient is a new choice. First tests
   are boundary variation and high-frequency response, then a flattened
   source and Solar external-field configuration. This is untested and may
   worsen derivative sensitivity. Existing generalized-QUMOND prior art is
   recorded in the repository audit; no novelty is claimed here.

Fixed baryons means the same physical density profiles, masses, thick shares,
distances, acceleration footings, external field and original observational
cuts, retaining all 1,375 in-prior cells per footing. A changed nu, state-field
potential, geometric term or width rule is a new law, not a baryon adjustment.

Load-bearing locators (SHA-256 inventory in SOURCE_PINS.json):

- KT33_reciprocal_filter/DISCRETE_ENERGY.md and README.md.
- KT33_reciprocal_filter/cassini/README.md.
- KT34_reciprocal_epsilon_scan/REVIEW.md and mw/README.md.
- reviews/repo_audit_2026_11_03/FILTER_RECIPROCITY.md, NEXT_STEP.md,
  gravity/REPORT.md and REPORT.md.
- KT26 through KT32 README.md files (individual qualifications preserved).
- campaign_fresh_gravity/CFG653_nonlocal_filter_length/README.md;
  sol61_push/nonlocal_response_2026_10_12/RESULT.txt.
- qwen_claude_field_theory/closure_2026/FRIED_CHICKEN_SPEC.md.

No original file or result was edited, no old calculation was rerun, and no
commit was made. This checkpoint is a structural self-review, not an independent
re-audit of every archived computation. No retired cold/particle sector is reopened.
