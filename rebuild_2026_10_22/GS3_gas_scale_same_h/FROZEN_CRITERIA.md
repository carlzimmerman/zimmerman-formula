# GS3_gas_scale_same_h: FROZEN CRITERIA (committed alone, before any number from this comparison)

**Question.** ZN3's cluster pass needs eRASS1's gas raised to X-COP's scale. SM1 says +0.111 dex, RF3's hydrostatic-free version +0.092, and G-OUT-M3 reaches Z 2 at +0.093. Neither compared the surveys at one distance scale: gas mass from X-ray surface brightness goes roughly as h^(−2.5). RF3 flagged this with a recalled h 0.6774, provisional. This lane measures each catalogue's own cosmology from its own numbers, and restates the offset at one h.

**Disclosed.** A positive correction would help ZN3, so this is a check I'd like to come out one way. So the h values come from the data files, not memory, and the same arithmetic is applied whichever way it goes. RF3's +0.092 and the recalled conversion suggest about +0.128. Five clusters; none in the lensing sample.

**Standing.** κ = ½ FITTED. Cold dark energy, never a particle. Not "theory closed". Nothing here says the data favour the framework. No downloads.

## Measurement
- **Catalogue h:** M500 = 500 ρ_c(z) (4π/3) R500³ holds by definition. From each catalogue's own M500, R500, z, solve for E²(z) h². Fit h with Ω_m free and fixed at 0.3, median and scatter, for eRASS1 and for X-COP's `hydro_mass` files. If the relation doesn't identify h to 0.005, the lane says UNDETERMINED and stops.
- **Offset at one h:** for the clusters in SM1's match, X-COP's gas converted to eRASS1's distance scale, M × (h_X/h_E)^2.5 with radius × (h_X/h_E), read at eRASS1's R500 (RF3's hydrostatic-free aperture). Median and SE. This is the offset the grader's `qd` step then carries to the native scale.

## Grade
ZN3's frozen rule with that offset, unchanged otherwise: 15 keys, both h, both f★. X-COP's own path isn't changed in the graded line.
- **ZN3 HOLDS AT ONE h:** 15 of 15 at both f★.
- **ZN3 FAILS AT ONE h:** otherwise, naming keys.
- **[OFFSET WITHIN 1 SE OF THE LINE]** appended if the offset is within one SE of the Z = 2 crossings on either side.

## Reported
1. The same grade at offset ± 1 SE, and where the upper edge is (the keys can fail OVER too).
2. X-COP's own path uses X-COP's h 0.7 masses against native-h baryon and halo terms: size of restating it on the native scale.

## Checks
K1 at +0.111 this path reproduces ZN3's numbers |d| ≤ 1e-9. K2 the h solve recovers a synthetic catalogue's h to 1e-4. MUTATE: offset + 0.1 must move G-OUT-M3 by more than 1.
