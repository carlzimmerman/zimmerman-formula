# Independent review of the Gaussian Solar STF limit

Verdict: the fixed-eta>0, fixed-lambda>0 Gaussian-regularization limit in
`../cassini/REGULARIZATION_PROOF.md` is proved as written, subject to its
explicit scope. This review checks the analytic bounds and limit argument;
it does not independently replay the Solar numerical quadrature.

The target is the complete smooth-Gaussian STF quadrupole, including its
origin contacts, converging to the exterior point-field integral with zero
origin contacts. The conclusion is about that observable and that regulator.
It neither defines the nonlinear action on a distributional Hessian nor
proves regulator independence or uniformity as lambda also tends to zero.

The following load-bearing steps were independently recomputed:

* With x varied at fixed h=lambda^2 H:H, C=R-1+xR' gives
  C_xx=3R''+xR''' and C_xxx=4R'''+xR''''; D=lambda^2 xR'
  gives D_xx=lambda^2(2R''+xR'''). The stated bounds follow from
  R^(j)=O(z^(-j-1/2)) and x<=z. The logarithmic corrections to R
  have faster decay for each of the required positive derivative orders.
* The Rodrigues coefficient is v^l/(2^l l!) with positive sign after
  l integrations by parts. Since 3mu-5mu^3=-2P3 and 1-3mu^2=-2P2,
  the stated b=-2(g C2+eta C3) and d=2D2 give the advertised orders.
* For f(s)=P(3/2,s^2/2)/s^2, all three small-s integrands against
  d(log s) are O(s^2). Their large-s powers are s^8,s^14,s^6.
  Rescaling r=sigma s therefore gives exactly delta^8/lambda^5,
  delta^14/lambda^7 and delta^6/lambda^3 for the two A terms and B term.
* Gaussian enclosed mean density decreases with radius. For sigma<=delta,
  g/r is at least P(3/2,1/2)/delta^3 throughout r<=delta. This supplies
  the uniform large-z threshold, including the small-r region where g
  itself vanishes. Bounding only g without its tangential Hessian would
  not supply that threshold.
* C_x=O(z^-3/2) gives the A contact O(eta^2/(lambda^3 k^2));
  D_xx=O(lambda^2 z^-5/2) gives the same B-contact order. Since
  k is proportional to sigma^-3, both vanish as sigma^6/lambda^3.
* On each exterior compact interval, the radial Gaussian fields and
  derivatives converge to the point field. For a large-r uniform tail,
  z>=eta^2/4, g<=r^-2, and |gp|+|gt|<=C r^-3 give respectively
  r^-7 and r^-9 bounds against d(log r), both integrable.

The uniform core bounds, vanishing contacts, and exterior dominated
convergence close the limit in the stated order. No additional unproved
exchange of sigma and lambda limits is needed. The old derivation's caution
about arbitrary regulators remains valid and is not contradicted by this
more specific Gaussian proof.

Review provenance: independent subagent response_obstruction, read-only
inspection of the two source notes and the unchanged action API. SHA256 pins
are listed below. The parent had separately reconstructed the Green
contractions and smooth-core contact formulas; this review checks the new
uniform limiting argument rather than claiming an unrelated third solver.

* `rebuild_2026_10_22/KT37_generalized_action/cassini/REGULARIZATION_PROOF.md`: `e908b73a1b11c74bb31494f5413113a40a7607ffd3ec7b886ce75997a649f6d4`
* `rebuild_2026_10_22/KT37_generalized_action/cassini/DERIVATION.md`: `921a0313a4a9e8dd20f37061ccd116bd0ad26358d1178b01b169bfe345d98904`
* `rebuild_2026_10_22/KT37_generalized_action/analytic/law.py`: `7a7f4710cacb6b33a88e170147c64eb6554ba44f6fda1fc81104bea5a222740f`
