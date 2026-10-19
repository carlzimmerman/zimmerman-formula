# Tail proof and precision diagnosis

The first bounded run reached the spectral comparison at mR=5, then failed
its declared 1e-65 roundoff allowance. Its discrepancy was approximately
1.86e-63, well inside the weaker 1e-50 identity tolerance at that point.
This was an implementation precision failure, not a counterexample to the
propagator formula. The original code, contract and failed run are preserved.

The separately contracted precision diagnostic compared every component at
70, 90 and 95 digits with 160-digit evaluations, for mR=5 and 30. It
located the excess error in extremely small high-order Hurwitz tails before
they are multiplied by large powers of a. Inspection of installed mpmath
1.3.0 `_hurwitz_em` shows a stopping test `mag(term)<-prec`, using absolute
rather than small-result-relative term size. Consequently even 95 nominal
digits need not give a usable 1e-65 allowance after that amplification. No
library defect beyond that precise accuracy limitation is asserted.

Version 2 replaces those special-function evaluations by explicit
Euler--Maclaurin arithmetic with a separate analytic remainder. Let Q=N+1.
For integer s>1 use

    zeta(s,Q)=Q^(1-s)/(s-1)+Q^(-s)/2
      +sum_(j=1)^P B_(2j)/(2j)! (s)_(2j-1) Q^(1-s-2j)+E_P.

The periodic Bernoulli integral and
sup |B_(2P)({x})| <= 2(2P)! zeta(2P)/(2pi)^(2P) give

    |E_P| <= |B_(2P)/(2P)! (s)_(2P-1)Q^(1-s-2P)|.

This is the magnitude of the last term included. Here P=50, N=256 and
s=2,...,82 even. Arithmetic is performed on the small tail's own scale.
No subtraction of nearly equal order-one functions is required.

The separate geometric expansion of the propagator uses

    1/(n^2+a^2)=sum_(k=0)^K (-a^2)^k/n^(2k+2)+remainder,
    |remainder| <= a^(2K+2)/n^(2K+4).

After the extra a^2 in the finite-part tadpole, the omitted spectral tail
is bounded by a^(2K+4) zeta(2K+4,N+1). The integral test gives an upper
bound Q^(1-s)/(s-1)+Q^(-s) without another Hurwitz evaluation. The script
adds this geometric bound to the sum of each explicit Euler--Maclaurin
error times its actual coefficient, then includes the separately declared
floating-roundoff allowance. This is not interval arithmetic; numerical
roundoff is checked by the two working precisions, while the displayed
truncation bounds are analytic. No physics or matching formula changed.
