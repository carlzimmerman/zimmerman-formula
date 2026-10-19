# Finite MSbar matching of the complete Dirac benchmark

FSP-008 supplement, written after run_001, whose frozen inputs remain unchanged. This appendix addresses a different theory from QCD: one free massive unit-charge Dirac field at u=0. It closes the one-loop finite ultraviolet matching for that benchmark. It neither supplies nor approximates the QCD proton counterterms.

Take d=4-2 epsilon, with a dimensionally regulated photon, Feynman gauge, and canonical u=e². The one-loop self-energy numerator is

    gamma_mu (p-slash-k-slash+m) gamma^mu
       = (2-d)(p-slash-k-slash)+d m.

Combine the photon denominator with the internal fermion denominator using x on the photon denominator. After shifting k=l+(1-x)p and projecting on the on-shell spinor p-slash=m, the coefficient of the scalar loop integral is

    d+(2-d)x = 4-2x+epsilon(2x-2).

The scalar denominator has Delta=(1-x)²m² at p²=m². The MSbar-subtracted mass derivative, divided by m, is therefore

    M_u^D,MSbar/m = 1/(16 pi²) integral_0^1 dx
       [-(4-2x) log((1-x)²m²/mu²)+(2x-2)].                 (A1)

The last term is the evanescent numerator multiplying the ultraviolet pole. Omitting it would produce a finite constant 5 rather than 4. The exact elementary integrals are

    integral(4-2x) dx = 3,
    integral(2x-2) dx = -1,
    -2 integral(4-2x) log(1-x) dx = 5,

so

    M_u^D,MSbar/m = [4+3 log(mu²/m²)]/(16 pi²).            (A2)

This is a derivative at u=0 with the MSbar fermion mass m held fixed, not an on-shell mass held fixed. The pole location is understood perturbatively; the charged-state infraparticle issue does not introduce an infrared divergence in this first-order mass shift. No numerical alpha or fermion mass is needed. At mu=m the dimensionless slope is exactly 1/(4 pi²).

The complete doubly Pauli–Villars convolution of run_001 gave

    D(lambda)=[3 log(lambda²)+3/2-6 log 2]/(16 pi²)+o(1),
    lambda=Lambda/m.

Matching this regularization to the MSbar mass definition fixes, by the explicit calculation above,

    M_u^D,PV counterterm/m
       =[3 log(mu²/Lambda²)+5/2+6 log 2]/(16 pi²).          (A3)

Then `lim_(Lambda/m -> infinity) [D(lambda)+counterterm]` equals (A2). This finite term is not adjusted to a mass, alpha or cosmological datum. It is the regulator conversion calculated from (A1). At finite Lambda there are cutoff corrections; the table in the separate appendix run is a finite comparison, not a claim that the limit is reached at any listed cutoff.

The load-bearing uniform statements here are the exact integral (A1) and the asymptotic primitive/logarithmic-moment argument already given in DERIVATION.md. The new finite computation checks their algebra and translates the previously computed ten PV integrals without reinterpreting them as QCD. For QCD, all physical current contractions and its quark/gluon operator matching must still be calculated; an elementary Dirac counterterm cannot be used in their place.
