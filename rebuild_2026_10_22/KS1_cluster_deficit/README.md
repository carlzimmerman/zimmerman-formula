# KS1_cluster_deficit: k is not one number. It falls with radius in every method, HSC reads it 1.6 times higher than KiDS, mass dependence is not established, and a kernel test still has 0 bits after look-elsewhere

Criteria: `FROZEN_CRITERIA.md` (f8a0fb38e8), committed alone first. Scripts `ks1_basis.py`, `ks1.py`, `ks1_bits.py`; numbers `ks1.out`, `ks1_results.json`, `ks1_bits.out`, `ks1_bits.json`, `ks1_MUTATE.out`. **Not blind.** A measurement and a description: nothing here reinstates the cold sector, which stays retired. kappa = 1/2 FITTED. Footings never pooled. Not theory closed. Nothing here says the data favour the framework.

## Verdict, frozen labels, primary cell (h 0.672, f* 0.034)
| Question | canonical | alt |
|---|---|---|
| One number? | **NOT ONE NUMBER** (chi^2 473/14) | **NOT ONE NUMBER** (528/14) |
| Function of x? | **FUNCTION OF x**, s -0.52 +- 0.03 | **FUNCTION OF x**, s -0.56 +- 0.03 |
| Function of mass? | **FUNCTION OF MASS**, p -0.25 +- 0.08, 3.0 sigma, on the line | **MASS NOISE-LIMITED**, -0.26 +- 0.09, 2.8 sigma |
| Methods | **METHOD OFFSET**: HSC +0.21 +- 0.06 dex (3.8), HSE +0.13 +- 0.07 (1.8) | **METHOD OFFSET**: +0.22 +- 0.06 (3.7), +0.14 +- 0.08 (1.7) |
| f_b reading, x >= 1 | **DISAGREES**, sets differ | **DISAGREES**, sets differ |

**Read these labels with three cautions, all post-criteria.**
- **The mass label comes from HSC.** Without HSC, KiDS plus X-COP read p -0.07 +- 0.07 (alt -0.06 +- 0.07). HSC alone reads -0.29 +- 0.10, and GM1's mocks produce about that size from noise alone. I do not read this as a mass dependence.
- **The offset drops to 2.3 sigma** once HSC's own 0.035 dex mass budget is applied across its bins. In mass the gap is about 25 % (UX3). It is amplified in k because the law holds half the mass.
- **s's small error is X-COP's**, from a bootstrap of 7 clusters. KiDS alone gives -0.45 +- 0.21, which is 2.2 sigma. The fall with x is well supported, but 20 sigma overstates it. X-COP alone fits s with chi^2 6.6/2, so a single power law is only rough.

## k3(x) = (M_tot - M_law) / M_gas, 3D, canonical. Alt in `ks1.out`, lower by 0.3-0.5
| x | 0.2 | 0.35 | 0.6 | 1.0 | 1.7 |
|---|---|---|---|---|---|
| KiDS 326, forward | 8.31 +- 1.24 | 5.40 +- 0.77 | 5.07 +- 0.66 | 2.89 +- 0.57 | 1.94 +- 0.67 |
| KiDS lg Mg 12.37 | 25.2 +- 5.4 | 4.0 +- 3.7 | 6.7 +- 4.2 | -1.2 +- 2.5 | -4.2 +- 3.7 |
| KiDS lg Mg 13.06 | 10.9 +- 2.9 | 4.3 +- 1.8 | 6.1 +- 1.4 | 4.3 +- 1.3 | -0.3 +- 1.3 |
| KiDS lg Mg 13.50 | 7.2 +- 1.3 | 5.7 +- 0.9 | 4.8 +- 0.7 | 2.9 +- 0.7 | 3.3 +- 0.7 |
| KiDS, the 35 | 7.4 +- 3.5 | 6.8 +- 2.5 | 4.9 +- 2.0 | 2.3 +- 1.9 | 2.7 +- 2.2 |
| X-COP HSE, 7 | 7.72 +- 0.60 | 7.08 +- 0.54 (x 0.3) | 5.09 +- 0.49 | 2.63 +- 0.38 | 2.13 +- 1.37 (x 1.5, N 5) |
| X-COP, HSE - 0.12 dex | 5.08 | 4.59 | 3.00 | 1.00 | 0.38 |
| HSC 60, mock-corrected | | | 7.99 +- 0.52, NFW SHAPE | 5.23 +- 0.43 | 3.22 +- 0.40, NFW SHAPE |
| HSC gas bins 13.06, 13.35, 13.87 | | | | 6.96 +- 0.92, 6.16 +- 0.85, 4.08 +- 0.52 | |

The same 35, x 1: HSC 5.58 +- 0.53, KiDS 2.27 +- 1.91, 1.67 sigma; KiDS on these 35 is too noisy to settle it. X-COP 4-of-7 splits move k3(0.7) over 3.74-4.79, sd 0.29, inside its 0.34 error, so they show sample variance and not a method difference. Between-catalogue HSE spread at x 1: L13 2.58 +- 0.15, L20 3.47 +- 0.09, M13 3.99 +- 0.27, V09 4.30, S09 5.37 +- 0.37, L15 5.66 +- 0.56. Part of that is mass and part is catalogue, and V09's rms of 0.16 shows its masses come from a scaling. Umetsu+20 x E16: 5.39 +- 1.85.

**The brief's three windows concern a different quantity.** k <= 7.2, >= 8.8, >= 12.9 are for the multiplier k_term in M_law (1 + k_term g_gas/a0), not k3.
- KiDS: 13.75 +- 1.26 (alt 13.90 +- 1.37), a 9 % statistical number. Constant across nodes 0.35-1 at 13.10, p 0.15.
- X-COP falls: 13.5, 12.9, 10.8, 7.75 at x 0.3, 0.5, 0.7, 1.
- HSC x 1: 20.3 +- 2.4, and by gas bin 40.8, 29.0, 12.3.
- So k_term is flatter in x than k3 on KiDS, not on X-COP, and it moves strongly with mass on HSC.

## The conflation, now split
1. **Radius.** A real fall, about x^-0.5.
2. **Method.** HSC over KiDS and HSE, as above.
3. **Gas zero point: found here, post-criteria, and larger than the k statistical error.** On the 5 X-COP clusters in eRASS1 (none in the 326), lg X-COP gas / eRASS1 gas is **+0.090 +- 0.014**, while HSE mass over catalogue mass is -0.016 +- 0.056. SM1 had +0.111 on 5, GS4 about 0 on more clusters and other catalogues, so this is unresolved. If that offset held everywhere, approximately, KiDS k3(1) goes 2.89 to 1.85 and HSC 5.48 raw to 3.94. It is a sensitivity row, not a claim.
4. **HSE bias.** LF1's -0.12 dex takes X-COP k3(1) from 2.63 to 1.00.

## Third mass: none on the 35
PSZ2 shares **1** of the 35 and 14 of the 326; L20 0; Groener+16 WL 0 of the 35, 3 of the 326; X-ray 5, CM 0. All THIN by the frozen rule, no vote. UX3's "no third mass" stands, now checked.

Reported only, non-voting: KiDS / NFW(MSZ) 0.92 +- 0.10 on 14; KiDS / NFW(Okabe) 0.72 +- 0.08 on the 35. MSZ / Okabe 0.67 +- 0.11 on 8. These lean towards HSC being the high one, on different clusters, and PSZ2 is hydrostatically calibrated. **No verdict on which survey is right.** Post-criteria, eRASS1 x PSZ2, N 358: k3(1) 6.25, 4.67, 3.49 in rising gas bins, no Eddington correction, selection untreated. eRASS1 gas x L20: 3.57 +- 0.12, N 57. HSC x pointed gas: 2 matched, no row.

## Best error and bits
| x, canonical (alt) | KiDS stat | HSE stat | HSC stat | Spread between methods | Total |
|---|---|---|---|---|---|
| 0.6 | 13 % | 10 % | 6 % (NFW SHAPE) | 5.07, 5.09, 7.99 | **25 % (27 %)** |
| 1.0 | 20 % | 15 % | 8 % | 2.89, 2.63, 5.23 | **38 % (42 %)** |

With METHOD OFFSET the frozen rule forbids combining: inverse-variance would give 5-7 %, chi^2 about 20-22 on 2, so that number is **NOT A MEASUREMENT OF k.** Total error rises from BK1's 16-25 % on this split, because BK1's windows held only part of the method gap. HSE bracket and gas zero point are on top.

| Window, canonical | Ceiling, bits | After log2 15 | BK1 engine: bits, hits / control |
|---|---|---|---|
| Total x 0.6, x 1 | 2.04, 1.22 (alt 1.92, 0.94) | 0, 0 | 0, 1.08; 0, 1.06 |
| HSE x 0.6, x 1 | 3.57, 2.94 | 0, 0 | 0, 1.00; 0, 1.12 |
| HSC x 1 | 3.79 | 0 | 0, 0.99 |
| k_term KiDS | 3.63 (3.53) | 0 | 0, 1.09 |
| Best, HSC x 0.6, stat only, NFW SHAPE | 4.14 (4.10) | 0.23 | 0, 0.94 |

3-node shape, KiDS stat: correlations 0.14-0.28, effective count 2.7, bound 7.7 bits (alt 7.3) before look-elsewhere, for a formula with no free amplitude. It is still under BK1's 10, and only counts if KiDS's scale is right. Sqrt(N) alone would need about 127,000 KiDS-depth clusters for 1 % at x 1, with no floor. **A forced-kernel test on k has no power on disk.** A shape test against a whole k(x) is the only reading that gets near, and it needs the method offset settled first.

## The f_b reading, a description
Y = M_tot / M_b; 1/f_b 6.27 native, 6.35 BK1's. Neither f_b is a direct measurement; they differ by 1 %, far under the power here. Y doesn't depend on footing.

| Set | x | Y | Z | Frozen label |
|---|---|---|---|---|
| X-COP HSE, 7 | 0.7, 1, 1.2, 1.5 | 7.53, 6.38 +- 0.44, 6.42 +- 0.72, 6.83 +- 1.42 | +3.5, +0.24, +0.21, +0.39 | **CONSISTENT** at 1, 1.2 |
| KiDS forward | 1.18, 1.67 | 7.92 +- 0.46, 8.47 +- 0.60 | +3.54, +3.65 | **DISAGREES** |
| HSC | 1 | 10.05 +- 0.55 | +6.9 (+3.9 with its sys, by hand) | **DISAGREES** |

Overall **DISAGREES**, and the sets differ.
- **X-COP tracks it from x 1 outward:** k_F = (1 + f*)/f_b - law/gas reads 2.37, 1.96, 1.37 against measured 2.63, 2.25, 2.13. Not at x 0.7: 2.79 against 4.33. **But this test has LOW POWER on X-COP:** P(|Z| >= 3) is 0.01-0.11 against a Y 20 % high, constant k, or continued power law. X-COP cannot tell these apart. It also depends on HSE as measured: HSE - 0.12 dex gives Y(1) 4.84, well below 1/f_b.
- **KiDS and HSC can reject a rival** (P 0.72-1.00 on constant k or power law, 0.18-0.38 on 20 % high), and they read above 1/f_b, not at it. KiDS beyond x 1.5 carries unsubtracted two-halo; its gas beyond R500 is X-COP's tail. Projected A_F is less severe: 1.17 +- 0.12 and 1.35 +- 0.10.
- **X-COP and KiDS differ by lg 0.094 in Y, about the gas offset above.** With the +0.090 row KiDS reads Y 6.22, 6.44, 6.89 at x 1, 1.18, 1.67. That would remove the KiDS disagreement but rests on 5 clusters against GS4. HSC would still sit at about 8.4.

## Checks, every failure
K1 PASS, trivially by construction. K2 PASS: 5.38, 4.22, 2.27 against GM1's 5.92, 4.38, 2.39. **K3a FAILS:** injection recovered -2.6 to -4.1 %, frozen 2 %. Diagnosed post-result: with the same reduced-shear factor, -0.8 to -1.6 %, so most of it is that factor; nodes 0.2 and 3.5 are edges. Stays failed; size under each node's error. K3b PASS. **K4 FAILS:** 0.054 against 0.05, on LM1's row printed to 0.1. K5 PASS, 0.724 against 0.746. K6 PASS, 5.48. K7 PASS, `ks1.out` and JSON byte-identical on rerun; `ks1_bits` wasn't rerun. K8 PASS, 1.31 GB in the bits run, the only one measured. **MUTATE a0 x 1.5:** K2, K4, K6 fail, exit 1, as required.

## Departures, errors, limits
- Departures: "k = 0 beyond 1.7" run as a taper to 0 at 3.5, not a step. Power computed from a normal with the measured sigma, not by mock. KiDS k3 uses LM1's V with C*, the term has none. One negative KiDS value dropped from the fit by the frozen rule. HSC mock uses k 3.3 in every subset.
- Rows not used: C08, M08 have no M500 in GS4's file. **E16's M500 reads M/Mg 3.35**, a gas fraction of 0.30 against Umetsu's M/Mg 11 on the same survey; I suspect the column and did not chase it. It belongs to GS4; flagged, not edited.
- Bugs caught during the build, before any label was read: X-COP bootstrap indexed wrongly (errors were the rms, not rms/sqrt N); L20's mass first read from GS4's matched file, which is the catalogue mass, ratio exactly 1.000 gave it away; M500 axis first in wrong units.
- x means different things: KiDS catalogue R500, HSC its stack's lensing R500, X-COP its own hydrostatic R500. Gas and M500 aren't separated (GM1). Sets assumed independent; shared gas and overlapping sky aren't modelled. Other cells are in `ks1.out`; h 0.686 keeps the shape of every row.

## Expectation against result
One number fails 90 %: yes. Mass NOISE-LIMITED 65 %: alt yes, canonical on the line. HSC above KiDS at 2-3 sigma 70 %: 3.8 stat, 2.3 with sys. Third mass doesn't settle 70 %: yes, far thinner than I thought. Total over 10 % 75 %: yes. Ceiling under 5 80 %: yes. f_b consistent near x 1, underpowered beyond 60 %: only on X-COP. I did not foresee the gas zero point being the largest term.

## Files that would shrink the error, for owner approval. Nothing downloaded
Ranked by what they'd do. Sizes from HEAD requests 2026-11-02, PROVISIONAL.
| File | Source | Bytes | Gain |
|---|---|---|---|
| `DESY3_metacal_v03-004.h5` | desdr-server.ncsa.illinois.edu/despublic/y3a2_files/y3kp_cats/ | 312,037,859,376 | Grandis+24: 2201 eRASS1 clusters at S/N 92 (65 after cuts), against KiDS 19 (Kleinebreil+25). Roughly 3.5-5 times smaller stat, about 5 % at x 1, and a third shear on any shared clusters. Overlap with the 35 not counted |
| `DESY3_indexcat.h5` | same | 27,246,838,040 | Needed with the above |
| `DESY3_sompz_v0.50.h5` | same | 36,792,670,792 | Needed with the above. Set total about 376 GB; a gold or mask file may also be needed, name not verified. Too big for this machine's current load |

**Better value if they exist, not verified:** the shear profiles and covariances for the eRASS1 clusters from Grandis+24 (DES), Kleinebreil+25 (KiDS) and Grandis+24b (HSC, 96 clusters). These would be small and would replace HSC's NFW SHAPE with a measured profile, but I couldn't find a repository, so no filename or size. Asking the authors is probably the cheapest step. A one-table literature lensing set (CoMaLit LC2, J/MNRAS/450/3633; Herbonnet+20, J/MNRAS/497/4684, from memory) is small, but the VizieR mirror returned 502, so no size and no overlap count.

**Note:** none of these touches HSE bias or the gas zero point. For the gas, more pointed XMM or Chandra gas on eRASS1 clusters beyond the 5 is what's wanted; I name no file. Without that, more shear shrinks statistical error but not the total.

Sources, PROVISIONAL: [Grandis+24](https://arxiv.org/pdf/2402.08455), [Okabe+25](https://arxiv.org/pdf/2503.09952), [A&A Okabe+25](https://www.aanda.org/articles/aa/full_html/2025/08/aa53708-25/aa53708-25.html). S/N figures come from a search summary, not read in the papers themselves.

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework.
