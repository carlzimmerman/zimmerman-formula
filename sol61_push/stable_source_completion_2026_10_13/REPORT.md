# An explicit nonnegative scalar potential for the source and messenger

2026-10-13. This is a chosen tree-level model family. It closes the previously unspecified quadratic source–messenger coefficient for this family and proves nonnegativity of the displayed classical scalar potential. It does not derive that choice from observations, establish radiative stability, or construct a physical apparatus.

## The choice and its purpose

The prior extension added -A R|S|^2 and -mu R|Phi|^2. The source-medium calculation showed that the independent term -(lambda_RS/2)R^2|S|^2 affects production. Rather than leaving its value implicit, choose

    lambda_RS = A^2/(2M_S^2) + eta,     eta >= 0.

Then the messenger contribution to the potential becomes

    [M_S^2 + A R + (lambda_RS/2)R^2]|S|^2
      = (M_S + A R/(2M_S))^2 |S|^2 + (eta/2) R^2 |S|^2.

It is nonnegative for every real R. This relation is a sufficient design choice for classical stability, not a symmetry requirement or a uniquely necessary condition. Other stable potentials can allow different coefficients. The selected family is not claimed to remain in this form automatically under renormalization.

## Completion including the original carrier sector

Write y=|Phi|^2, z=|chi|^2, s=|S|^2, all nonnegative, and retain

    Q = |sqrt(Delta_chi) chi + g_chi Phi^2/sqrt(Delta_chi)|^2,
    Delta_chi > 0.

The original globally charged source chi is distinct from the new neutral resonance R. Its positive carrier potential was m^2 y+4m^2 z+Q+lambda_rep y^2. Adding the R and S sector gives the following exact rearrangement:

    V = m^2 y + 4m^2 z + Q
        + (M_R^2/2) (R + mu y/M_R^2)^2
        + [lambda_rep - mu^2/(2M_R^2)] y^2
        + (M_S + A R/(2M_S))^2 s
        + (eta/2) R^2 s + h y s + lambda_S s^2.

For m^2>0, M_R^2>0, M_S>0, lambda_S>=0, h>=0, eta>=0 and

    lambda_rep >= mu^2/(2M_R^2),

all displayed terms are nonnegative. Expanding the R square and its compensating quartic preserves the original lambda_rep y^2 coefficient and supplies mu R y; it does not silently increase the original carrier self-repulsion. Choose lambda_S>0 if a strictly positive messenger quartic is desired. This is a polynomial potential of degree at most four, compatible with the stated scalar charges.

For lambda_rep=1e-6, M_R approximately 2 MeV, and mu=47.4124532 eV, the remaining coefficient is 9.9971900741e-7. The square completion consumes 0.02810% of that illustrative repulsive quartic. No background field scan is needed to prove the stated nonnegativity: it is an algebraic statement for arbitrary field magnitudes and real R.

## Effect on the proposed source window

With A=2589.91624 eV and M_S=10 MeV, the minimal choice eta=0 gives

    lambda_RS = 3.3538330675e-8.

Use the preceding leading-density free-constituent formulas at n=5e24 m^-3. The quadratic and cubic *static*, fixed-number source curvatures cancel at eta=0. The timelike response at omega=M_R does not cancel exactly. Including the tadpole contribution to each carrier gives:

| eta | Source mass shift (eV) | Corrected pair excess D (eV) |
|---:|---:|---:|
| 0 | -1.62684e-19 | 7.91237e-11 |
| 1e-6 | 4.80056e-16 | 7.91241e-11 |
| 1e-4 | 4.80217e-14 | 7.91717e-11 |
| 1e-3 | 4.80219e-13 | 7.96039e-11 |

These examples keep the source above the carrier-pair threshold in that approximation. The model choice therefore allows a nonnegative tree potential and the previously identified cold-production window simultaneously. It does not fix actual production yields: the in-medium source line shape, composite neutral-atom response, finite cavity modes and reverse annihilation remain required. The photon spectrum is an assumed input, not a source technology demonstrated here.

## Formal verification and limits

The accompanying StableSource.lean proves two polynomial identities and nonnegativity of the general real-variable potential under explicit coefficient and magnitude assumptions. The map to physical notation is a=M_R^2/2, b=mu/M_R^2, c=M_S, d=A/(2M_S), Lean eta=physical eta/2, m2=m^2, x2=4m^2, l=lambda_rep, q=Q, and y,z,s as above. The theorem takes q>=0 as a hypothesis; the complex-field norm interpretation is supplied here, not implemented as a full quantum-field model in Lean.

The compiler record gives the exact command, source hash and outputs. The proofs do not contain sorry and depend only on the standard listed axioms. This certificate covers the displayed classical polynomial inequality. It does not certify vacuum loop corrections, quantum stability, naturalness of the tiny source–pair mass gap, experimentally allowed particle masses or coefficients, or the existence of the messenger reservoir.

The numerical runner separately checks four symbolic identities, positivity of the remaining quartic, and four open-threshold examples using 60-decimal arithmetic. Its manifest records source/output hashes and environment. These nine checks are not a universal physical validation.

## What this changes

There is now an explicit classically bounded candidate potential for the added production sector instead of an unassigned quadratic coupling. Its choice is transparent and conditional. A complete theoretical preparation route still needs a viable neutral medium, its dynamical response, production and capture in the same finite geometry, and controlled losses. The model also adds no enhanced gravity or propulsion law. The research goal remains open.

Reproduce numerical/symbolic evidence:

    python3 sol61_push/stable_source_completion_2026_10_13/check.py /tmp/stable_source_results.json

Compile StableSource.lean with lake env lean in the existing fable_independent_2026/lean_2026 environment. The preceding source-medium derivation and primary-source normalization are in ../source_medium_shift_2026_10_13/REPORT.md; the original carrier definition is in ../cold_production_2026_10_11/MASTER_COLD_ENERGY_EQUATIONS.md. This report gives a new hypothesis and its algebraic consequences, not an additional empirical result.
