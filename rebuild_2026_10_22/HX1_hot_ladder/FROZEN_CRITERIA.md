# HX1_hot_ladder: frozen criteria

Committed alone, before any script or any ladder number. kappa = 1/2 FITTED. Footings canonical 9.3603e-11 and alt 1.1312e-10 are graded apart, never pooled. No LCDM input. A description: no action, no field equation, no particle, no fluid, no halo. **This isn't route E.** Route E added a cored halo whose surface density went as sigma^q (GR1, X40b). Here nothing is added; the law's own phantom acceleration is multiplied. The cold sector stays retired, and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. Not blind (see "Seen before freezing").

## Question
Is there one boost of the law's phantom, keyed on a hot system's measured velocity dispersion sigma, that lifts each dispersion-supported class by what it needs, ellipticals through groups to clusters, while rotation-supported discs stay at the law?

The boost: g = g_N + B(sigma) (law(g_N) - g_N), with law(x) = x/2 + sqrt(x^2/4 + a0 x), B = 1 for discs by class (a [LABEL]: discs are cold, rotation-supported).

## Stage 1, the plain ladder (no fit)
For each hot system, B_need is the multiplier its data ask for. Every estimator below is linear in g, so B_need = (D_obs - D_N) / (D_law - D_N), where D is the estimator's quantity (sigma^2 or g) under g_N, the law, and the data. Exact, no root-finding.

**Graded rungs**, each with its key sigma (km/s):
1. **MaNGA ellipticals** (Tian+2026, J/A+A/710/L39, 1218), split into four sigma quartiles, four rungs. Estimator: RQ3's B1 integral (crg1_groups: Hernquist, a = Re/1.8153, isotropic virial sigma), D = sigma^2. Key: the catalogue's sigma.
2. **ATLAS ellipticals** (same catalogue, 26), one rung, same estimator.
3. **Galaxy groups** (same catalogue, 63, RQ3's B1 sample), one rung, same estimator.
4. **SLUGGS** (19, RQ3's A26a path, h50: gamma 3 tracer, Jeans, outer bins outside max(Re, 2 kpc)), D = mean of sigma_los^2 over the outer bins. Key: mean measured outer GC sigma.
5. **Lovisari groups** (20, RQ3's B2 path, h7 stellar masses), D = g at R500; a second rung at R2500. Key: sigma^2 = kT / (0.6 m_p), kT from the table.
6. **X-COP** (12, RQ3's B23 path, x = 0.1, 0.2, 0.3, 0.5, 0.7 R500), D = g = G M_HSE / r^2. Key: sigma^2 = kT/(0.6 m_p) with TX1's emission-weighted kT inside R500 (`tx1_lib.tload()["Tew"]`, data in TX1's external directory, read only).

**Reported only, not graded**: Local Group, Fornax and Virgo dwarfs (same catalogue). They sit in external fields that the B1 integral doesn't carry, so their B_need is the law's EFE question, not this one.

**Rung value and error, set now from real errors.** A rung's value y = log10 of the median B_need over its objects (X-COP: over its 60 points). Its error s is the half-width of the 16-84 % interval of y over:
- 2000 bootstrap draws of the rung's objects, combined in quadrature with
- the rung's systematic, which is the harness's own: B1-type rungs (1-3), Mb +-0.10 dex (B1's 0.10 x slope rule); SLUGGS, A26a's stat error (std/sqrt n) propagated; Lovisari, B2's tot (stat, star-mass factor SBR both ways, 20 % HSE); X-COP, B23's 0.121 dex on M_HSE.

A rung whose median B_need <= 0 (data below Newton) is SUB-NEWTONIAN: y is undefined, and the rung counts as a fail of L-ORDER.

**Ladder tests, per footing.** The tolerance line is RQ3's: |Z| <= 2, p >= 0.05.
- **L-ORDER.** Sort the graded rungs by median key sigma. Fit a weighted non-decreasing (isotonic) curve with floor 0 (B >= 1, a boost), f = max(0, iso(y)). chi^2 = sum((y - f)/s)^2. p by parametric bootstrap: 2000 draws y* ~ N(f, s), refit, same chi^2. **ORDERED** if p >= 0.05.
- **L-NEED.** X-COP's y > 0 at Z = y/s > 2.
- **L-FLAT.** A scalar B per system must give the same B_need at every radius of that system. X-COP: slope of log B_need on log x over the 60 points, error from bootstrap over clusters; FLAT if |Z| <= 2. Lovisari: y(R2500) - y(R500), error from the two rungs' s in quadrature; FLAT if |Z| <= 2.
- **L-KEY** (reported label, MaNGA only, objects with B_need > 0). Joint least squares of log B_need on log sigma and log gbar(Re) (the catalogue's loggbarRe), errors by bootstrap. "SIGMA CARRIES IT" if sigma's coefficient |Z| > 2 and gbar's <= 2; "GBAR CARRIES IT" if the reverse; "BOTH" or "NEITHER" otherwise.

**Stage 1 class, per footing.**
- **LADDER**: ORDERED and NEED and FLAT on both X-COP and Lovisari.
- **LADDER, NOT FLAT**: ORDERED and NEED, FLAT fails. A scalar B(sigma) can't fit inside systems, so B25, B2's bins and the keys are predicted to fail.
- **NO LADDER**: not ORDERED, or NEED fails.

## Stage 2, only if stage 1 reads LADDER or LADDER, NOT FLAT on a footing
Form B(sigma) = max(1, (sigma/sigma_h)^p), with (sigma_h, p) fitted by weighted least squares to that footing's graded rungs' y. Two arms and a control:
- **P**: the multiplier on the whole phantom, as above, on every hot sample (et, group, xgroup, cluster, keys, merger).
- **S**: the extra (B - 1)(law - g_N) rides only with the stars, scaled by g_s/g_b. Its own B_need and fit (equal to P on gas-poor ellipticals).
- **CL, control**: P's form with the measured sigma swapped for the law's own sigma_law = (G M_b a0)^(1/4), refitted. If CL does as well as P, measured sigma adds nothing that baryonic mass doesn't.

Graded through RQ3's acceptance.py, unedited, keys and the Bullet included. The rows the boost can touch are A26a, A26b, B1, B2, B19, B20, B23-B25, B28 and the keys B4-B18. **HOT ROWS PASS** only if every one passes. Everything else is the law's own row and reads as the law's. How each call finds its system's sigma (sample tag plus a lookup), and the Bullet's sigma and its source, are frozen in an amendment before any stage-2 number. If stage 1 reads NO LADDER on both footings, stage 2 doesn't run, and that is the lane's result.

## Checks (all before any graded number is read)
- **K1, reproduction at B = 1.** The stage-1 machinery at the law reproduces RQ3's law rows: B1 mean (-0.0100 / +0.0103) to 1e-4, B23 (+0.4675 / +0.4345) to 1e-4, B2 values (0.161, 0.349 / 0.123, 0.312) to 1e-3, A26a (+0.0767 / +0.0620) to 1e-4.
- **K2, linearity.** For 5 objects in each estimator, D computed with g = g_N + 2 (law - g_N) equals D_N + 2 (D_law - D_N) to 1e-9 relative.
- **K3, power.** A planted ladder, sigma_obs (or M_HSE) built from B = max(1, (sigma/300)^0.8) on the real rungs' inputs with noise at the real errors, must read ORDERED (p >= 0.05) and NEED. A planted break (groups at B = 1, ellipticals at B = 2 below the groups' sigma, clusters at their real B) must read NOT ORDERED. If either check misses, stage 1 is NOT DIAGNOSTIC.
- **K4.** A rerun is byte-identical.
- **MUTATE.** Every graded rung's B_need replaced by 1/B_need. NEED must fail, and the exit code comes from the result: exit 1 if caught.

## Expectations on record (priors, before any number)
| | prior |
|---|---|
| L-ORDER ORDERED, canonical | 35 %. The record has SLUGGS short of the law (A26a +0.077 dex in sigma, B ~ 2) while the B1 groups sit at it (B ~ 1), likely at higher sigma |
| L-NEED | 97 % |
| L-FLAT, X-COP | 30 % |
| L-FLAT, Lovisari | 25 %. B2 reads +0.161 at R500 and +0.349 at R2500 |
| MaNGA rungs ill-conditioned (B_need errors above a factor 2, IMF inside Re) | 60 % |
| Stage 1 class NO LADDER on both footings | 55 % |
| If stage 2 runs: P fails the Bullet (sign stays on the gas) | 95 % |
| If stage 2 runs: HOT ROWS PASS for any arm | 5 % |

## Seen before freezing
The law's aggregate RQ3 rows on these classes (A26a, A26b, B1, B2, B23-B25, B28), which were already in the record. GR1's and X40b's route-E reads of the groups and SLUGGS. The catalogue's class counts and columns. TX1's verdict and its T loader. No per-rung B_need, no rung sigma, and no ladder number.

## Limits
Static and spherical. Isotropic for rungs 1-3, gamma 3 tracer for SLUGGS, hydrostatic for 5-6 (X-COP DISPUTED). Inside Re, ellipticals are Newtonian-dominated and the stellar IMF moves D_N, so B_need there carries the IMF. Lovisari star masses come from h7's relation. sigma from kT takes beta_spec = 1. Dwarfs are reported only. Red KiDS lenses have no sigma per lens and aren't graded (as GR1 found).
