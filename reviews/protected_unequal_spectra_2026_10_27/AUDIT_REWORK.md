# Adversarial audit and rework of K796-K800

Audited revision: 89d81635b7eb01cd0703e9b3c0960b96e653a4c6.
Primary verdict: **incomplete, with the smallest missing implication being a
physical interacting action and its source-dependent protecting identity**.
The algebra below survives in restricted settings. The recent narrative gave
those calculations too much weight as progress toward a microscopic origin.
This is self-review by the originating assistant, not independent validation.
No new kappa derivation or candidate search is performed here.

## Dependency graph and obligations

Required chain:

    microscopic action + physical state + baryon coupling
      -> physical fluctuation operators on sourced backgrounds
      -> protected quantum response and healthy force law
      -> Newtonian and MOND matching plus absolute gravitating vacuum
      -> a parameter-independent amplitude relation.

Actual chain:

    assumed bare cubic-gradient EFT
      -> quadratic fluctuation determinant
      -> formal infrared correction
      -> arbitrarily assigned signed spectra cancelling selected moments.

The first chain has never been completed by the second. The unequal-spectrum
ansatz already assumes background dependence inherited from the desired cubic.
It cannot serve as an independent microscopic derivation of that cubic.

| Obligation | Verdict | Evidence and limit |
|---|---|---|
| K796 integral and angular coefficient | passed | Recomputed derivative, exact integral, expansion and quadrature; formal one-loop continuum EFT only |
| Extrapolate K796 to a physical lowest-gradient force | not addressed | Fluctuations grow in the same limit; no controlled resummation or sourced solution |
| K797 signed moments and Jensen lemma | passed | Exact finite algebra and strict convexity; no particle-action realization |
| K797 retained cubic as universal microscopic response | failed | It is a cutoff boundary contribution; continuum subtracted determinant is zero |
| K797 positive cutoff constant as fixed gravitating vacuum | not addressed | No gravitational matching or absolute normalization principle |
| K798 spectator relaxation | passed in stated boundary class | Cauchy-Schwarz bound with periodic fluctuations and fixed affine twist; no MOND cubic |
| K799 gapped determinant separation | conditional | Finite cutoff and summable third-derivative bounds; not all interacting/string limits |
| K800 modular identities imply MOND response cancellation | not addressed | Source constrains masses, not the required background-response coefficients |
| Complete stable vacuum and sourced MOND model | incomplete | No candidate supplies both, much less their exact amplitude relation |

## Decisive regulator test of the four-spectrum fixture

For one radial mode the exact expression already used was

    I(m,L) = (L^2+m^2)^(5/2)/5
             -m^2(L^2+m^2)^(3/2)/3 + 2m^5/15.

Subtract its displayed degree-zero, one and two terms in m^2:

    J(m,L)=I(m,L)-L^5/5-L^3 m^2/6+L m^4/8.

Directly taking the limit gives

    lim_(L->infinity) J(m,L)=2m^5/15.

In the four-node construction m_i^2=t_i s a, a=1+mu^2. Thus for finite many
modes, fixed s and angle, the subtracted determinant is proportional to

    s^(5/2) a^(5/2) sum_i w_i t_i^(5/2) = 0.

The angular interval is compact and the finite number of masses bounded at
fixed s, so the limit also commutes with the angular integral. This is an
exact property of the stipulated dispersions, not just a small-s statement.
At finite cutoff the reported positive cubic is

    C3_cut=4320 hbar v0 t0^3/(7pi^2 L),

and tends to zero. Its positivity was real in that prescription, but its
survival did not represent a regulator-independent quantum prediction.
Adding a finite cubic matching term can restore any desired coefficient;
that coefficient then requires physical matching and is not selected here.

This does NOT assume a physical EFT is valid to arbitrarily large momentum.
The continuum extension is a mathematical stress test of the claimed
universality. If L is instead a physical microscopic scale, the ultraviolet
completion must specify the regulator, matching and remaining coefficients.
No such completion was provided. The old report already called the term
cutoff-dependent; this audit makes the stronger consequence explicit and
retires the fixture as a proposed microscopic opening. Its limited value is
as an algebraic counterexample about moment constraints.

## What the test counts really establish

The existing baseline scripts rerun successfully: 18/18, 16/16, 15/15. These
are NOT 49 independent physical validations. Several are rearrangements of
the same equation, expected derivatives, or checks of definitions. For example,
the third script sets the gapless coefficient from whether the twist equals
zero; it does not derive the spectrum of an interacting compactified action.
The second computes a nullspace and checks the defining nullspace equations.
Those are useful implementation checks, but they cannot validate the missing
microscopic assumptions. Mutation failures show that these assertions notice
specific input changes, not that a theory of gravity has survived falsification.

The direct continuum-limit check used SymPy on J as displayed above and
returned 2*m**5/15; the four-node fractional moment returned zero; the finite
cubic coefficient limit returned zero. No new executable, fitted constants or
parameter scan was introduced. The analytic limit is the evidence; the symbolic
result is a corroboration. External string-source claims remain as scoped in
SOURCES.md; their full proofs were not independently re-proved in this audit.

## Reworked research status

Keep K796 as a conditional quantum-consistency diagnostic for the stated bare
EFT. Keep K798 and K799 as narrow exclusions with explicit assumptions. Keep
K797's moment/Jensen results as algebra, not a physical candidate. K800 is a
source-transfer check: it identifies an interesting established mechanism and
also records that its required application is absent. It is not a newly
constructed microscopic route or a reason to expect 32pi.

The model has a separate problem even before quantum corrections: the vacuum
constant is freely specifiable in the EFT. Cancelling response corrections does
not fix that constant. A productive construction must address its absolute
gravitational value at the action level rather than adding this obligation
only after a spectral cancellation succeeds.

For future work, require the following concrete input BEFORE another spectral
search: an explicit action, its field transformations, physical sourced state,
and the identity relating the vacuum term to the response operators. First test
whether a symmetry-preserving deformation changes the target amplitude ratio.
If it does, that action fails selection regardless of how elegant its spectrum
is. Only after that gate should we spend effort on background spectra and loops.
No source currently inspected supplies this input; inventing new weights,
renaming an existing mass sum rule, or collecting more routine symbolic checks
would repeat the same missing step.

No broad impossibility theorem is claimed. The research question remains open,
but the four-node fixture should not be pursued as a model without genuinely
new physical structure. Kappa=1/2 remains fitted, not derived.
