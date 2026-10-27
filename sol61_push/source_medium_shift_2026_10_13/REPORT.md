# Source resonance in the messenger medium: a small computed shift and an unfixed coupling

2026-10-13. The specified cubic messenger interaction produces a small leading-density source shift. A separate symmetry-allowed quadratic source–messenger coupling is not fixed by the previous photon widths and can change the near-threshold window substantially. This package makes that missing parameter explicit; it does not choose its physical value or certify a complete medium.

## Conventions and scope

Use natural units, a real source R of mass M_R, a complex messenger S of mass M_S, and carrier Phi of mass m. Write

    L_int = -A R |S|^2 - (lambda_RS/2) R^2 |S|^2
            -mu R |Phi|^2 -h |Phi|^2 |S|^2.

The cubic A and mu magnitudes were assigned by the earlier illustrative widths. lambda_RS is dimensionless and independent: neither the stated global U(1) nor electromagnetic gauge symmetry forbids it. Previous truncated source calculations omitted it. Setting its renormalized value to zero at a specified scale would be an additional model choice, not a consequence of the photon coupling or decay rate. A full potential and matching prescription remain necessary.

Calculate only the leading-density, stationary free-messenger contribution. The neutral atoms previously proposed as a reservoir are composite. Using their count as a count of messenger cores is a constituent approximation, not a derivation of the bound atom's MeV-frequency response. Atomic excitation, absorption, binding corrections, collective response, velocity averaging and higher-density terms are not included. The result therefore does not yet resolve the full neutral-reservoir self-energy.

## Cubic dynamic response and independent static check

For an R quantum at rest, energy omega, and a stationary messenger p=(M_S,0), the two crossed propagators give the invariant forward amplitude

    Mcal_cubic = -A^2 [1/(omega^2+2M_S omega)
                      +1/(omega^2-2M_S omega)].

With the invariant-amplitude convention in which a positive quartic contact has Mcal_contact=-lambda_RS, the leading-density self-energy is

    Pi_R(omega,0) = -n Mcal/(2M_S)
                 = n lambda_RS/(2M_S)
                   - n A^2/[M_S(4M_S^2-omega^2)].

Here n is in natural eV^3 units. Evaluate the dynamic term at omega=M_R and convert to a leading mass shift by delta M_R=Pi_R/(2M_R). We work away from the messenger-pair threshold. No static thermodynamic compressibility has been substituted for the timelike propagators.

As a separate check, the energy of fixed, stationary messenger number in a constant R background is

    E_density(R) = n sqrt(M_S^2+A R+(lambda_RS/2)R^2).

Its second derivative at R=0 is

    n lambda_RS/(2M_S) - n A^2/(4M_S^3),

which agrees with the omega->0 limit. At M_R=2 MeV and M_S=10 MeV, the cubic dynamic shift is 1.010101 times its fixed-density static limit. This comparison checks the frequency dependence and normalization; it is not a license to replace all bath responses by static curvature.

The same fixed-density energy produces a source tadpole. With a purely quadratic R potential near the vacuum, to first order in n,

    R_0 = -A n/(2M_S M_R^2),
    delta U_Phi = mu R_0/(2m),
    D_corrected = delta - 2U_in + delta M_R - 2 delta U_Phi.

Additional R self-interactions can change this expansion and must be specified. For the table we take mu*A positive. Previous rates determine magnitudes only; reversing that product reverses the carrier tadpole contribution.

## Half-density benchmark

Use n=5e24 m^-3, m=1 MeV, M_S=10 MeV, M_R approximately 2 MeV, h=1, A=2589.91624 eV and mu=47.4124532 eV. The tiny vacuum excess delta=2e-9 eV is carried separately to avoid subtracting MeV-sized numbers. Using M_R=2m in large prefactors neglects relative corrections of order delta/(2m)=1e-15.

At lambda_RS=0:

- Cubic source mass shift: -1.6268431e-17 eV.
- Induced R background: -1.2437272e-12 eV.
- Carrier tadpole shift: -2.9484080e-17 eV per particle for positive mu*A.
- Corrected pair excess: 7.9123650e-11 eV, compared with 7.9123608e-11 eV before these corrections.

The specified cubic terms alone therefore leave the proposed half-density window essentially unchanged within this approximation. However,

    delta M_R(quadratic) = (4.80219098e-10 eV) lambda_RS.

| lambda_RS | Total leading source shift (eV) | Corrected pair excess (eV) | Pole open? |
|---:|---:|---:|---|
| -0.2 | -9.60438e-11 | -1.69202e-11 | No |
| 0 | -1.62684e-17 | 7.91237e-11 | Yes |
| 0.1 | 4.80219e-11 | 1.27146e-10 | Yes |
| 1 | 4.80219e-10 | 5.59343e-10 | Yes |

These are sensitivity examples, not fully stable or experimentally allowed parameter points. In this approximation the pole closes at lambda_RS approximately -0.164766 for the stated sign choice. The opposite mu*A sign changes the lambda_RS=0 excess to 7.9123532e-11 eV, still open.

An absolute coefficient 0.00416477 moves the source by one *original vacuum total linewidth*, 2e-12 eV, through the quadratic term alone. This is a sensitivity scale, not a hard exclusion bound: the beam center could be retuned if the shift were known, and the bandwidth in the preceding source calculation was wider than this linewidth. Retuning photons does not remove the shifted pair threshold or determine the coupling. Previous production numbers must be recalculated for nonzero lambda_RS; merely testing D>0 is not a rate calculation.

## Source verification

[Eletsky and Kapusta, nucl-th/9810052v1](https://arxiv.org/pdf/nucl-th/9810052), dated 15 October 1998, Eq. (1) gives the leading-medium self-energy in terms of the forward scattering amplitude; Eq. (4) specifies the propagator pole and Eq. (6) its nonrelativistic target limit. Translating their f_cm to Mcal=8pi sqrt(s) f_cm yields Pi=-integral n(k) Mcal/(2E_k), hence the stationary expression used here. The positive contact mass term also fixes the sign independently. Their paper concerns hadronic media and provides formalism, not evidence for these particles. The paper explicitly limits the approximation where sequential-scattering interference is important.

Search scope: leading-density self-energy/forward-scattering normalization and a contact-model cross-check. The primary arXiv paper above was inspected. A separate PoS contact-model paper appeared in search, but publisher/mirror fetches failed; it was not used to authenticate an equation. No novelty or experimental-support claim is made.

## Evidence and next obligation

Four symbolic identities check the crossed denominators, the static curvature, its dynamic limit, and the tadpole. Four 70-decimal calculations check the linear mass conversion against direct square roots; ordinary float64 subtraction would erase these tiny shifts. The run manifest validates. No new Lean proof of QFT or empirical certification is claimed.

This narrows the missing information: the original cubic source sector is compatible at this order, but a defensible complete model must fix lambda_RS and the other scalar couplings, then compute the response of the actual neutral reservoir. The goal remains open. The present work does not justify declaring the source immune to its medium or the full apparatus realizable.

Reproduce:

    python3 sol61_push/source_medium_shift_2026_10_13/check.py /tmp/source_medium_shift_results.json

Related assumptions: ../threshold_resonance_2026_10_13/REPORT.md, ../source_bath_compatibility_2026_10_13/REPORT.md and ../carrier_collision_width_2026_10_13/REPORT.md.
