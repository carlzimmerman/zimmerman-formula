# A shared threshold for production and the interior reservoir

2026-10-13. This calculation joins the earlier prescribed source and messenger mean potential. It finds a conditional density window in which products are born cold inside the cavity. It does not establish the new particles, their couplings, the assumed gamma source, actual trapping, or a manufacturing protocol.

## One energy reference for both stages

Let delta=M_R-2m=2e-9 eV be the vacuum pole excess and U the constant interior carrier energy shift. Keep the neutral R pole and the vacuum couplings fixed by assumption. Define U_wall as the wall potential measured from the vacuum exterior. At a center of mass at rest,

    D = delta - 2U,
    K_pole = D/2 = delta/2 - U,
    E_b = U_wall - U.

The pole can decay into carriers only if D>0. Products at the pole pass the classical kinetic-energy acceptance condition when K_pole<E_b. Substitution yields

    U < delta/2,                 (pole above pair threshold)
    delta/2 < U_wall.            (born-inside energy below wall)

The second condition is independent of U as long as the first holds. Raising the uniform interior potential makes both the kinetic energy of newly born particles and the relative barrier smaller by the same amount. Thus their margin is

    E_b - K_pole = U_wall - delta/2.

This cancellation concerns products born in the *static* medium. It does not describe switching the medium after creating particles while holding their kinetic energy fixed, as in the earlier storage-shift diagnostic. A dynamic switch transfers energy and needs a different calculation.

The old wall has U_wall=1.92087639236e-9 eV. With U=U_wall n_bath/(1e25 m^-3), pole production requires

    n_bath < 5.20595705156e24 m^-3.

The previously considered bath at 1e25 m^-3 is above this limit. Doubling the wall would restore its relative barrier but would not reopen the source pole. A lower-density interior provides a conditional alternative that keeps the original wall and pole open simultaneously.

## Fixed source and finite bandwidth

Retain the previous hypothetical equal vacuum partial widths w=1e-12 eV, m=1 MeV, prescribed 1 MW per photon beam, 1 mm^2 area and 2 mm overlap length. The Gaussian center-of-mass energy spread is 1e-10 eV RMS, centered on the fixed R pole. These beam properties are assumptions, not an available source specification.

For x=E_CM-M_R, the kinetic pair excess is x+D. In the isolated-pole approximation,

    r(x,D) = sqrt((x+D)/delta) for x+D>0,
    sigma(x,D)/sigma_peak = 4r / [4(x/w)^2 + (1+r)^2],
    sigma_peak = 2pi/(2m)^2.

The daughter width changes with threshold phase space; it is not reset to its vacuum value at each bath density. Cross sections are converted to m^2 before applying the previous photon luminosity. Two independent coordinates (piecewise x/w integration and a tangent substitution) check each of six finite-bandwidth integrals. The Gaussian integration is cut at 12 standard deviations; the omitted contribution is bounded by the peak production rate times the omitted Gaussian probability, below 1.2e-25 pairs/s.

| Interior density (m^-3) | Pole product kinetic energy (eV each) | Relative wall (eV) | Ideal production (pairs/s) |
|---:|---:|---:|---:|
| 0 | 1.0000e-9 | 1.9209e-9 | 395,287 |
| 1.0e24 | 8.0791e-10 | 1.7288e-9 | 374,378 |
| 2.5e24 | 5.1978e-10 | 1.4407e-9 | 331,560 |
| 5.0e24 | 3.9562e-11 | 9.6044e-10 | 131,451 |
| 5.2e24 | 1.1443e-12 | 9.2202e-10 | 25,643 |
| 6.0e24 | Pole closed | 7.6835e-10 | 0.03279, off-pole spectral tail |
| 1.0e25 | Pole closed | 0 | At most 1.511e-68 |

Kinetic energy in this table is the pole value, not the energy of every produced particle. Production rates integrate the full specified spectrum and do not assert capture of every product. At the highest density the threshold lies 18.42 Gaussian standard deviations above the beam center. No numerically truncated integral is called zero: instead, the all-spectrum upper bound follows from

    4r <= (1+r)^2 <= 4(x/w)^2+(1+r)^2,
    rate <= peak_rate * Prob(E_CM > 2m+2U).

The second displayed inequality uses x real; the numerator inequality is (r-1)^2>=0. The bound is about the stipulated line shape and Gaussian spectrum, not about an arbitrary source or all production mechanisms. Retuning photons above threshold can drive off-resonant production but does not move the fixed R pole.

## Interpretation and unresolved physics

Half the previous bath density is a concrete conditional candidate: products near the pole emerge about 25 times colder than in the vacuum interior, while the same wall retains the classical energy margin. This is a kinematic way to avoid requiring a long cooling stage *if* the assumed in-medium source description is valid. It is not a verified device design.

Holding R fixed remains an unverified approximation. Its messenger coupling, tadpoles, real self-energy, collision broadening, and the response of the carrier propagator must be calculated consistently. Mean-field energy shifts alone do not establish quasiparticle linewidths or a sharp production threshold. The very-near-threshold row also needs finite cavity modes and the real threshold self-energy; it must not be advertised as precise achievable cooling. Bath thermal kicks, spatial escape, reverse annihilation, tunnelling, charge balance, medium preparation, and density fluctuations remain unresolved. Thermal rates at the previous bath density cannot simply be copied into these lower-density configurations.

The next useful calculation is the in-medium carrier spectral response: whether scattering broadens the carriers beyond the extremely small excess energy assumed in the source. That tests the sharp-threshold premise of this density window before attempting a complete transport simulation.

## Verification

The numerical runner completed and its hash manifest validates. Six independent quadrature comparisons agree; the zero-density case reproduces the earlier 395,287 pairs/s benchmark. Numerical checks also cover spectral bounds and five confinement margins. The high-density case uses the analytic Gaussian upper bound, not an evaluated tiny production integral.

SourceBathBounds.lean compiles in the repository's existing Mathlib environment. Its four lemmas prove pole opening, margin cancellation, the equivalent energy-acceptance inequality, and the line-shape numerator bound for real parameters. The compiler lists only propext, Classical.choice and Quot.sound; there are no sorry axioms. These proofs certify algebra conditional on the definitions, not QFT, the numerical integrals, physical existence, or the full research goal. Command, source hash and output hashes are in lean_record.json.

Reproduction:

    python3 sol61_push/source_bath_compatibility_2026_10_13/check.py /tmp/source_bath_results.json

Use the existing fable_independent_2026/lean_2026 environment and lake env lean with the absolute SourceBathBounds.lean path for the algebra. Related assumptions are recorded in ../threshold_resonance_2026_10_13/REPORT.md, ../finite_temperature_kicks_2026_10_13/REPORT.md and ../resonance_storage_shift_2026_10_13/REPORT.md.
