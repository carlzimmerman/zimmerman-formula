# GS4_pointed_gas_offset: ASSUMPTION LEDGER (committed with the criteria)

| input | value or source | class | role |
|---|---|---|---|
| eRASS1 Mgas500 | Bulbul+24 | RAW (X-ray, fit with a β-like form) | denominator |
| eRASS1 M500, R500 | WL-calibrated scaling in a ΛCDM count fit | ΛCDM-PROCESSED, labelled, no clean replacement | radius, mass axis |
| eRASS1 h 0.70, Ωm 0.30 | GS3, from its own M500, R500, z | RAW-DERIVED | one h. Geometry only, not a graded background |
| Pointed Mgas | papers listed in the criteria | RAW (X-ray imaging), each with its own centre, background and calibration; h and Ωm as each paper states | numerator |
| L20, L15, L13, S09 R500 | hydrostatic | HSE, labelled | radius conversion only |
| C08, M08 R500 | Y_X scaling (an external M–Y_X) | LITERATURE-INPUT | radius conversion only |
| E16 r500,MT | M–T calibrated on WL (XXL) | LITERATURE-INPUT, NFW-fit mass underneath | radius conversion only |
| M13 r500 WL | lensing, NFW fit | LITERATURE-INPUT, no HSE | radius conversion only |
| V09 Mgas from M_G and f_g(M) | its own relation inverted | LITERATURE-INPUT, not primary | reported row |
| Gas slope s 1.19 | X-COP's 12 profiles, 0.8–1.25 R500 | RAW, massive clusters, applied at all masses; L15's 2500–500 value is steeper at about 1.58, and over a wider range | radius conversion; s 1.0, 1.4 as sensitivity |
| X-COP profile | Ghirardini+19 files | RAW | XC row |
| Positions | tables; X-ray centres (A-S17, RXC names, XXL); NED for L15, L13, S09, V09 | LOOK-UP, name-resolved rows may be optical | matching only |
| Lensing terciles | X7's 326 clusters | RAW M500 column from eRASS1 | binning |
| ZN3's shapes, rule, grader, f★ | ZN3 | FRAMEWORK-NATIVE, κ fitted, as in its ledger | regrade |
| KiDS shear keys | X7 | RAW + survey calibration | regrade |

Planck 5.364 absent. No ΛCDM background used in any graded number; eRASS1's h, Ωm are used only to place the two surveys at one geometry. κ = ½ FITTED; not theory closed.
