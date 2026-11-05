# Cassini for the weak-field curvature variant

All ten explicitly tested physical lengths pass the inherited Cassini
quadrupole cut on both frozen acceleration footings. The calculation uses
the new law z=x+s^2 and its complete variation, including the Hessian term
and the radial derivatives of its new prefactor. No KT37 numerical score
or Gaussian-filter bound is transferred.

| Length (kpc) | Canonical abs(Q2)/ceiling | Alternate abs(Q2)/ceiling |
|---:|---:|---:|
| 0.3 | 0.000164323935 | 0.000205507710 |
| 1 | 0.0000492971891 | 0.0000616523250 |
| 1.5 | 0.0000328647934 | 0.0000411015509 |
| 1.75 | 0.0000281698230 | 0.0000352299009 |
| 2 | 0.0000246485952 | 0.0000308261634 |
| 2.25 | 0.0000219098625 | 0.0000274010343 |
| 2.5 | 0.0000197188763 | 0.0000246609309 |
| 3 | 0.0000164323969 | 0.0000205507758 |
| 5 | 0.00000985943821 | 0.0000123304656 |
| 10 | 0.00000492971912 | 0.00000616523280 |

The ceiling is the unchanged 5.2e-27 s^-2. Every signed Q2 is negative.
For example, at 2 kpc Q2 is -1.28172695e-31 s^-2 canonical and
-1.60296050e-31 s^-2 alternate. These are finite constant-external-field
quadrupole results, not a theorem for all intermediate lengths or a full
Solar ephemeris analysis.

## Exact implementation

This lane implements the specified new phenomenological function in the
known generalized-action framework:

```
x=|g|^2, s=lambda^2 H:H, z=x+s^2, P=xQ(z)/z,
A=(R-1+xR')g,
B=2lambda^2 s xR' H,  R=Q/z,
S_ph=div A-double_div B.
```

Quantities here use Solar rM and a0 units; lambda=ell_physical/rM. Q is the
unchanged primitive of the simple response, with Q(0)=0. No Gaussian field
filter is present. This particular z is not claimed to be literally
Milgrom's equation 16 or a fundamentally derived function.

DERIVATION.md records the complete product derivatives of
beta=2lambda^2s, both origin contacts, the angular Green contractions, and
the differential-density calculation. The full B term dominates the Solar
quadrupole and is retained. At canonical 3 kpc, for example, q_B is of order
7.25e-7 while q_A is of order 1e-15. Dropping B would produce an incorrect
prediction despite the resulting value also being small.

The point-source computation is the Gaussian-source shrink limit. A literal
distributional Newtonian Hessian is never squared. For fixed positive
external field and lambda, the two contacts vanish as
O(eta^2 sigma^15/lambda^6); the uniform small-core B integral is
O(eta^2 delta^15/lambda^6), with still higher powers for A. Together with
integrable exterior bounds, this establishes the specified Gaussian limit.

The analytic owner independently checked the new derivatives, contact
coefficients, and limit argument in
`../analytic/SOLAR_DERIVATION_REVIEW.md`, with source hashes. No assertion
of independence from every possible regulator is made.

## Checks and provenance

The original five-point `run_001/` completed in 11.28 seconds. All
predeclared checks passed, including:

- 24 direct comparisons against the shared tensor API, with maximum
  relative discrepancy 2.18e-16.
- Same-node ell=0 reproduction of inherited QUMOND and its finite-source
  origin correction; exact zero anomaly for Q=z and exact zero STF for
  zero external field.
- 8,000x160 versus 16,000x320 radial/angular nodes, with an expanded radial
  domain; largest relative change 1.19e-9 among the initial ten physical
  rows.
- Independent analytic differentiation of the full A/B angular moments
  to form the differential density; largest relative Green/density
  discrepancy 2.67e-8 among those rows.
- Gaussian source widths .5,.1,.01,.001,5e-7 rM at .3 kpc. Every width
  agrees with the point result within 3.23e-11 relative. Halving and
  quartering the broad-core inner cutoff changes q by at most 2.70e-16.

The origin prescription uses rmin=max(1e-10,.001sigma) with both analytic
contacts, retaining the resolved-core procedure established in KT37. It
does not repeat KT37's known tiny-r/sigma cancellation. Scaled derivatives
zR', z^2R'', and z^3R''' avoid overflow when z approaches 1e143; they are
algebraically identical to the full derivatives, with no high-field floor.

After the parent explicitly expanded the MW probes, `focus_001/` computed
the five additional lengths 1.5,1.75,2,2.25,2.5 kpc in 5.29 seconds. The
implementation was unchanged. Each new point received fresh base/fine and
Green/density checks; the tensor API comparison was repeated. The original
Newtonian, QUMOND, and regularization controls are explicitly inherited from
the unchanged, hash-pinned successful run, rather than falsely described as
newly rerun in the focused calculation.

Both manifests completed and validate against their current input hashes.
Their contracts preceded execution and retain the exact commands, software
versions, bounded wall/CPU/log resources, one numerical thread, and output
hashes. No randomness is used. Every KT37 artifact remains unchanged.

## Limits

The external field is the unchanged prescribed constant, with zero external
Newtonian Hessian. Real Galactic gradients and the full tracking-data model
are separate questions. Numerical convergence is empirical, not certified
interval quadrature. These Solar passes establish neither Milky Way nor
dwarf success, dynamical health, nor viability of every law in the generalized
action framework. Final mathematical self-proofreading covered this new
text and the displayed formulas only.
