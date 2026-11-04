# Independent general-power Solar derivation review

Verdict: the full general beta derivatives, fixed-g H-zero regularity,
contact powers and Gaussian STF limit in ../cassini/DERIVATION.md are
correct as written for each fixed tested p>1, including the adaptive9/8.
This is an independent read-only analytic review, not another numerical
Solar solver or a claim of regulator independence.

Recomputed h=s^p and beta=p lambda²s^(p-1): their first/second logarithmic
product derivatives match every displayed s'/s, s''/s and squared-s' term.
The inherited D'=beta'E+beta E' and D''=beta''E+2beta'E'+beta E'' retain
all terms. The positive finite-radius Solar Hessian norm supports ordinary
fractional derivatives there; the exact ell0 branch avoids0/0 without a floor.

At fixed g!=0, the energy's leading curvature correction has degree2p in
H and B degree2p-1. This verifies the stated C² energy and C¹ B result,
including the lack of generic C² B at p<=3/2 and the locally integrable
transverse singularity distance^(2p-3). It does not settle joint g/H zeros.

The small-core estimates follow independently from
z>=2^p lambda^(2p)g^(2p)/r^(2p) and
D_xx=O(lambda² z^(-3/2-1/p)). After angular cancellation, the A integrands
are r^(5p-1)g^(3-5p) and r^(7p-1)g^(3-7p); B is
|gp-gt|r^(3p)/g^(3p), with denominator lambda powers5p,7p,3p.
Gaussian rescaling gives powers15p-7,21p-7,9p-3. Each rescaled integrand
is O(v²) at zero and grows with the stated positive power at infinity.
Contacts have k^(1-3p)lambda^(-3p), hence sigma^(9p-3)lambda^(-3p).
The B outer tail r^(-6p-3), and A r^-7, are integrable. Together with the
inherited uniform mean-density lower bound and compact exterior convergence,
these close the fixed-p,eta>0,lambda>0 Gaussian STF limit. No uniformity
as lambda->0 or unrestricted source-regulator claim is introduced.

Reviewer: response_obstruction. Reviewed SHA256 pins:

* `rebuild_2026_10_22/KT39_power_curvature/cassini/DERIVATION.md`: `93a33ebbfad749c8b122a05691aea4e2935958a1a070c2fabadda4315a8677bc`
* `rebuild_2026_10_22/KT39_power_curvature/analytic/law.py`: `52a5f9bece8f46aa307f320fe2bb8418b04d581e7d53801518d8448ea2952390`
* `rebuild_2026_10_22/KT38_weak_field_curvature/cassini/DERIVATION.md`: `f88a03a66e95f64e0a06228b73da3514f7fb26d0c1a8ea7e27bc6a586d1e05b9`
* `rebuild_2026_10_22/KT37_generalized_action/cassini/REGULARIZATION_PROOF.md`: `e908b73a1b11c74bb31494f5413113a40a7607ffd3ec7b886ce75997a649f6d4`
