# Total phantom tidal bound for a universal Gaussian length

This is a new corollary, separate from the hash-pinned incremental Solar proof
in `../universal_length/README.md`. It was proposed during independent review
and authorized for development on 2026-11-04. It bounds the total phantom
contribution, including a spatially varying Galactic background, under the
specified whole-space response law. It does not bound the ordinary Newtonian
tide or perform a Solar ephemeris fit.

For the fixed, normalized, isotropic Gaussian S_ell and simple nu, let

    u = grad N S_ell rho + u_external,
    A(u) = [nu(|u|/a0)-1]u,
    Phi_ph,out = S_ell Delta^{-1} div A(u).

The inverse Laplacian has the whole-space Green convention used in KT33/34.
No independent homogeneous quadratic anomalous potential is added. Assume u
is defined and finite almost everywhere. No source-mass bound, source symmetry,
uniformity of the external field, or positive lower bound on |u| is required.
One may define the Hessian by the absolutely convergent kernel integral below
even if an infrared subtraction is needed to define the potential itself.

For r=|u|/a0, the response magnitude is

    |A(u)|/a0 = f(r) = (sqrt(r^2+4r)-r)/2
                      = 2/[sqrt(1+4/r)+1] < 1  (r>0),
    A(0)=0.

Thus `||A||_infinity <= a0`, globally. This bound is particular to the retained
simple nu; it must not be transferred to an arbitrary interpolation function.

Write `F_ell(x)=erf(|x|/(sqrt(2)ell))/|x|`. With the Poisson normalization
`Delta^{-1}` having kernel `-1/(4pi|x|)`, integration by parts gives

    D^2 Phi_ph,out(x) = -(1/(4pi)) integral D^3 F_ell(x-y) A(u(y)) d^3y.

The sign does not affect the norm bound. For every pair of unit vectors v,w,
the KT34 Gaussian third-derivative estimate gives

    (1/(4pi)) integral |D^3 F_ell[v,w]| d^3y
        <= C0/ell,   C0=2 sqrt(2/pi) sqrt(33)/3 < 46/15.

The absolute integral is finite at both zero and infinity. Taking the scalar
bilinear pairing of the symmetric Hessian J with v,w therefore proves

    ||J||_op <= C0 a0/ell < (46/15) a0/ell.

There is no extra factor of sqrt(3): taking the supremum over unit v,w is
already the matrix operator norm. For any unit axis n, symmetry gives

    |n^T J n-tr(J)/3| <= (4/3)||J||_op.

Using the inherited `Q2=(3/2)` times this trace-free projection yields

    |Q2_ph,total(n)| < (92/15) a0/ell.

This is uniform in x and in the entire field u. It therefore also bounds the
phantom Galactic tide that is absent from an incremental Solar calculation.
At ell=3 kpc it is less than 0.0015 of the frozen Cassini ceiling on both
footings. At ell=2.5 or 3.5 kpc it remains less than 0.002 of that ceiling.
The much smaller bound on the Sun-induced change remains a distinct result.

The ordinary Newtonian Galactic tide belongs to the standard gravitational
background and is outside this phantom bound. A real comparison with tracking
data still needs the ordinary ephemeris/background conventions and other
observables. This corollary supports the inherited quadrupole amplitude cut;
it does not certify an ephemeris likelihood or all Solar System constraints.

## Exact arithmetic check

`total_phantom_bound.py` checks the safe constants and physical ceiling ratios
using rational arithmetic. To avoid an unverified decimal pi approximation,
it uses

    pi > 4 sum_(k=0)^63 (-1)^k/(2k+1) > 25/8.

The first inequality follows by integrating the finite geometric identity for
`1/(1+x^2)` on [0,1]; with last index 63, the discarded remainder is positive.
Consequently `sqrt(2/pi)<4/5`. Also `sqrt(33)<23/4`, giving `C0<46/15`.
The code encloses both intended decimal input constants and their binary
float representations conservatively before forming physical ratios. All
displayed decimals are supplementary; the assertions use exact fractions.

`contract_total_bound.json` predates the run. The result checks arithmetic,
not the analytic kernel proof; that derivation is independently reconstructed
in `UNIVERSAL_REVIEW.md` and recorded in KT34. The new corollary and its run do
not modify the incremental theorem or its existing evidence.
