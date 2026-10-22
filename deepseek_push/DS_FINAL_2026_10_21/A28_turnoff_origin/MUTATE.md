# A28 — mutation control

Two mutations, both invoked from the same script: `python3 a28_checks.py --mutate=<name>`.
A mutation is expected to fail checks and exit 1; the unmutated run exits 0 with 16/16.
Mutated runs write `a28_results_mutated.json` so they cannot clobber the canonical `a28_results.json`.
Captured outputs: `mutate.out` (M1), `mutate_sat.out` (M2).

## M1 — `--mutate=kernel`: replace the Langmuir kernel by the quadrature

    ν_L(y) = (1+√(1+4/y))/2      →      ν_Q(y) = √(1+1/y)
    h_L(y) = ½(√(y²+4y) − y)     →      h_Q(y) = √(y²+y) − y

This is the single most consequential physical substitution available: the whole lane is predicated on
the canonical law being `ν_L` (A25 §7, A12 K10). If the checks cannot see the kernel change, they
prove nothing. They can.

    K2 FAIL y_t=128.755867 |y_t-66.2999|<5e-4  [canonical Langmuir root at Lambda c^4/a0^2=100.4058]
    K3 FAIL rel_exact=9.71e-01, rel_asym=9.71e-01 rel<1e-10 and rel<1e-3  [quadrature vs exact rational vs asymptotic]
    K4 FAIL y_asym=66.6947, rel=4.82e-01, min dF/dy=0.5635 rel<1e-3 and dF/dy>0  [inversion of A4 eq. 13; monotone => root unique]
    K5 FAIL y_t(32pi)=128.915371 |y_t-66.3803|<5e-4  [32*pi = 3Z^2 at kappa=1/2; 0.121% above the observed-Lambda root]
    K6 FAIL y_t_alt=88.569046, ratio=1.45373 vs (a0a/a0)^2=1.45749 |y_t_alt-46.0148|<2e-3  [required exponent p=dln y/dln Z=0.99783]
    K12 FAIL kappa(y_t)=0.500311 vs sqrt(8pi/N)=0.500311; kappa(32pi)=0.500000; dln y/dln kappa=-0.99783 agree<1e-6, kappa(32pi)=0.5, monotone, elasticity=-1.9469  [F(y_t)=8*pi/kappa^2 => y_t and kappa are the same unknown]
    K14 FAIL half=133.4348 dbl=32.9132 nolog=64.4846 noC=65.7021 L+1%=130.0358 32pi=128.9154 73.19=94.0539 factor-2 shifts y_t by ~2x  [sensitivity dln y/dln N=0.9735]
    K15 FAIL 2Z^2=66.93723 (-48.012%), alt=45.92641 (-48.146%), kappa_impl=0.695651, strain=11.5704 |err|<1% both footings  [a two-parameter power law, not a principle; strain 11.57 at the turn-off]

    MUTATION CONFIRMED (kernel): 8/16 checks broken.

**8/16 broken, exit 1.** The root moves to 128.755867 — exactly A4's stored quadrature value, so the
mutation is the physical one and not a numerical accident. K3's exact-rational form is Langmuir-specific
and fails at 97 %, which is why K3 compares two independent representations rather than two settings of
the same one. K12's elasticity flips from −1.946912 to −0.99783, i.e. `y_t ∝ Z¹` for the quadrature —
the *same* power-counting statement as §7's class theorem. K7/K8/K9/K10/K11/K13/K16 stay green: those
checks test the candidate principles, whose numbers do not depend on the kernel, and their staying green
shows the mutation is targeted rather than a crash.

## M2 — `--mutate=sat`: move the saturation strain reference by one factor of `Z`

    A = cH_Λ   →   A = (cH_Λ)²/a0        (i.e. y_t: √2 Z = 8.181518  →  √2 Z² = 47.331769)

This is the "insert one factor of `Z`" temptation described in report §3: the free constitutive
normalization of the strain. It is the strongest *near-miss* variant in the lane (28.61 % low instead of
87.66 %), so it is the one a reader is most likely to think should pass.

    K7 FAIL y_sat=47.331769, err=-28.61%, resid=1.40075 y_sat=8.1815+-1e-3 and |err|>50%  [implied kappa=0.59525 (A1 P1: 4.09331)]
    K16 FAIL RAR(y=10): target=0.97776, sat=0.95727; a_sat/a0=8.18152; kappa_P1=4.09331 supp_sat<0.5 and supp_target>0.95  [saturation also fixes a0=7.6579e-10 and kappa_P1=4.0933]

    MUTATION CONFIRMED (sat): 2/16 checks broken.

**2/16 broken, exit 1.** K7 pins the saturation number to A1's `√2 Z` and K16 pins the RAR cost that
follows from it; both are the numerical content of "the saturation principle gives 8.18, not 66.3".
Everything else stays green, including K8 (which lists this very variant as one of the four free
normalizations — a family member failing its own row would be a contradiction). Note that the mutated
value 47.331769 is still 28.61 % from 66.30, so even the *most favourable* normalization of the
saturation principle fails by more than the 1 % band the lane is testing.

## Why these two

M1 attacks the kernel (the lane's premise); M2 attacks the constitutive normalization (the lane's most
likely escape route). Together they bracket the two ways a reader could discount the result — "you used
the wrong ν" and "you normalized the strain wrong" — and both are visible to the checks. A third
mutation, changing `a0` to the alt footing inside the closure, would not be a mutation: it is the
legitimate second data point of §8 and is exercised by K6/K13.
