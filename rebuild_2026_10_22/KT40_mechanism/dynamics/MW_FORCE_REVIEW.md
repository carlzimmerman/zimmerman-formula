# Independent review of the outward MW vertical-force band

Verdict: **computationally verified in the recorded finite range**. This is
a read-only review of `force_probe.py`, its contract and completed manifest,
and all eight literal-source model outputs. No field solve was rerun by the
reviewer. Exact input hashes appear below and in MW_FORCE_REVIEW.json.

The run uses the same p=9/8, ell=3 kpc and fixed baryon cells 1368/1287,
at refinements 3,4,5,6. Every model reconstructs the literal density, solves
the Newtonian field and the full action response, and separates the linear
Poisson solutions from the A and B source terms. The coordinate conversion
is the standard spherical-to-cylindrical potential gradient,
partial_z Phi=cos(theta) partial_r Phi-sin(theta) grad_theta Phi.

All 2,384 stored profile samples satisfy total=Newton+A+B; the maximum
profile-normalized discrepancy is 2.262e-12. At R=12 kpc,z=.3 kpc, the
total potential derivative is negative on both footings at every refinement.
At refinement 6, in (km/s)²/kpc:

| Footing | Newton | A | B | Total partial_z Phi |
|---|---:|---:|---:|---:|
| Canonical | 350.131213 | 251.165653 | -1445.066811 | -843.769944 |
| Alternate | 347.380466 | 293.184099 | -1576.675991 | -936.111425 |

The physical acceleration is **minus** this derivative. Thus the negative
values mean acceleration away from the midplane at positive z. The B term
reverses the positive Newtonian and A contributions; this is not a sign
convention that would make Newtonian attraction outward.

Centered differences of the same total potential with steps .005,.01,.02
kpc independently check the derivative estimator. All are negative at the
specified outer-disk point, on all four refinements and both footings. At
refinement 6 their best relative agreements with the grid-gradient estimate
are 8.814e-6 canonical and 1.445e-4 alternate. Refinement 5-to-6 changes the
force magnitude by 0.3867% and 0.3890%. The accepted contract gates remain
5% for the best finest potential difference and 2% for refinement change.

At R=12 kpc the finest sampled negative bands span z=.24 to .51 kpc
(canonical, 28 samples) and .24 to .52 kpc (alternate, 29 samples). These
are sampled profile ranges, not certified continuous interval endpoints.

This confirms an outward-force region in the fixed numerical witnesses.
Combined with their prescribed decreasing gas profiles, it rules out the
named positive-compressibility barotropic hydrostatic completion there.
It does not prove every possible anisotropic, magnetic, nonstationary or
different-density completion impossible. A potential-difference check uses
the same solved potential, so it is an independent derivative estimate,
not an independent gravitational field solver or a continuum error proof.

The completed manifest validates with unchanged input/output hashes. The
read-only algebra, signs, finite-difference errors and refinement comparisons
were rechecked by mechanism_dynamics separately from the root implementer.

## Exact reviewed input hashes

| File | SHA-256 |
|---|---|
| rebuild_2026_10_22/KT40_mechanism/mw/force_probe.py | `d4631943d02dbbee93d592293dde088d4b619d478d75fe4285ac395944ad686b` |
| rebuild_2026_10_22/KT40_mechanism/mw/force_contract.json | `f2bdaa05fbdee71ea7d4f4d790d1f1a82fd346995fbc8e0c931f3192d4639ee9` |
| rebuild_2026_10_22/KT40_mechanism/mw/force_001/manifest.json | `ec43f79b1cb5c85c96511a643dcf70199a4c4afa4851171a70dd09ca290b9e2c` |
| rebuild_2026_10_22/KT40_mechanism/mw/force_001/results.json | `d42ad067d17c9987b37e0268dca037225a1ca3e94c6b51a6a23fc20e2369bcaf` |
| rebuild_2026_10_22/KT40_mechanism/mw/diagnose.py | `1cec0ea730ea933244a8099a050594c2beb95452a0627b446eede7dc925506e9` |
| rebuild_2026_10_22/KT40_mechanism/mw/hydro_002/results.json | `fc57d5823da0fa7dccfebcb7f1193910394c0bea1da0df42464b050c8f4d934d` |
