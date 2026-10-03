# CFG291: khronon dipole radiation in binary pulsars over the filtered C-H/K window

Criteria frozen first: `FROZEN_CRITERIA.md` (commit 9b2bc6fe0). Script: `cfg291_khronon_binary_pulsar.py`
(main: `.out`, `_results.json`, 12/13 checks pass, 0 load-bearing failures, rc 0; MUTATE: `_MUTATE.out`,
`_results_MUTATE.json`, rc 1 as required). Run from anywhere; about 6 s.

## Verdict: CONDITIONAL (recipe section 6), by the frozen rule

**Surviving window.** The whole primary window survives: alpha_c in [9.6e-14, 3.2e-9] and c_2 = lambda_K - 1 in
[7.29e-3, 0.0667], with beta = 0 (L340 P1; cosmologically allowed with L350's leaf-average lambda-term). All three
pulsars pass under every published sensitivity bracket, with both the computed and the universal wave-zone factor:
625/625 points under B0, B1 and B2.

**Size of the effect.**
- The largest predicted dipole deviation in Pb-dot is 4.9e-13 with the computed wave-zone factor (B2, J1738+0333 at
  the window's top-alpha / bottom-c_2 corner). With the universal bound it is 1.9e-8.
- The limits are +0.19 (J1738+0333), +0.41 (J0348+0432) and 1.3e-4 (J0737-3039). The closest approach to any limit
  is 1e-4 of it (B2, universal, double pulsar).
- In sensitivity terms, the neutron-star sensitivity would have to be at least 5e4 times the published B2 bracket
  (s_crit = 5.5e-4 to 9e-2, depending on the system) before any of the three pulsars noticed.

**Why CONDITIONAL and not PASS.** The frozen rule demands PASS also under B3. B3 is a counterfactual, not a published
bracket: the khronon charge is assumed to scale with lambda rather than with alpha_c. B3 fails at every W1 point. The
condition is therefore named: the neutron-star sensitivities at alpha_c != 0 must follow the published brackets.
- Barausse 2019 finds the sensitivities vanish exactly at alpha = beta = 0 for any lambda.
- Foster 2007 eq. 70 gives the weak-field law s = (alpha1 - 2 alpha2/3) Omega/m. At beta = 0 that is
  about (11/3) alpha_c |Omega/m|.
- Yagi et al. 2014 say realistic NS sensitivities can exceed the weak-field value by up to a factor 3.
- A strong-field NS sensitivity at alpha_c != 0 has not been computed, here or in any paper read.

Which systems drive the B3 failure:
- The double pulsar fails everywhere, but only under the deliberately conservative NS-NS rule |s1 - s2| = |s_NS|.
- J1738+0333 fails only for c_2 >= 0.055 (0.061 for the dipole alone).
- J0348+0432 passes B3 everywhere.

**Record window** (1 < lambda_K <= 1.10). Radiation passes at every alpha_c for these c_2 ranges:

| sensitivity bracket | wave-zone factor | passes for |
|---|---|---|
| B1 | computed | c_2 >= 4.6e-9 |
| B2 | computed | c_2 >= 1.3e-8 |
| B2 | universal | c_2 >= 3.7e-5 |

The PPN bound |alpha-hat2| < 1.6e-9 already requires c_2 >= 1.6e-9. L350's Planck-era plain-branch ceilings
(6.3e-4 to 2.9e-3) lie inside the surviving range. Only a sliver next to lambda_K = 1 is lost.

**PPN consistency** (the same window, exact khronometric formulas).
- alpha1 = -4 alpha_c ranges over -3.8e-13 to -1.28e-8. The bounds are 2.1e-5 (pulsar) and about 1e-4 (LLR).
- |alpha2| ranges over 4.8e-14 to 1.600e-9. The window's top edge is set by the pulsar bound |alpha-hat2| < 1.6e-9
  itself, so the top corner sits on that bound by construction.

## What was done

1. **Parameters, from committed files.**
   - alpha_c and c_2: L340 results JSON (P1).
   - The Planck-era ceilings: L350 G2.
   - The xi floors: recipe I5 and L340 S1.
   - nu_mono: recipe user-decision block. Reimplemented and matched to L340's committed A1 numbers (C9).
2. **Map onto the literature.** alpha = alpha_c, beta = 0, lambda = c_2. Checked: F1's khronon speed equals XC1's
   decoupling-limit c_2/alpha to O(alpha, lambda), and the wrong maps fail (C4). XC1's committed UV speeds
   (443.85 c, 7.9356e5 c) are reproduced (C3).
3. **Formulas.**
   - Adopted: Barausse 2019 eqs. 15-22 (flux, A1-A3, B, C, c0, Z); Yagi et al. 2014 PRL's Pb-dot form; Foster 2007
     eq. 70; the khronometric PPN parameters; Peters-Mathews.
   - Controls on them: Barausse's alpha, beta -> 0 limit is reproduced symbolically (C2). The GR Pb-dot of J1738+0333
     (-27.46 vs -27.7 fs/s) and of J0348+0432 (-0.2591 vs -0.258 ps/s) are reproduced inside their quoted intervals,
     within 1% (C1).
4. **The MOND sector and the heat filter.** Two results; the second contradicts the brief's expectation.
   - **Near zone: screened.** At the orbit y = 6e11 to 5e12. The filter exponent is -(xi/a)^2 ~ -1e12 at the orbit
     and -6e21 at a neutron star. The binary's time-varying part of the filtered source is (mu/m)(a/xi)^2 ~ 1e-13
     of the static part. The tensor-GW filter exponent is ~ -1e7. Even unfiltered, nu_mono - 1 at the orbit is 1e-12.
   - **Khronon wave zone: NOT screened.** The khronon is superluminal, so at orbital frequencies its wavelength is
     ~0.06 pc, with k* xi ~ 3. There the filter factor is only 1e-5. That is not small next to alpha_c, so the C-H
     clock inertia 2C/(1+C) raises the khronon's effective alpha by 60 to 1e7 at the radiated wavenumber.
   - **The wave-zone factor, derived here.** From the decoupling-limit quadratic action, by Sokhotski-Plemelj:
     R_l = (k*/k_UV)^(2l-1) * 2Bk*/F'(k*).
     - Check: a k^1 source reproduces the alpha- and lambda-exponents of Barausse's C, and a k^2 source those of A3 (C5).
     - Value: R_1 is 0.2 to 360 at the W1 corners, and up to 440 on extended xi and C_0 grids.
     - Bound: R_1 <= sqrt(1 + 2/alpha_c) ("universal"), for any environment and any xi.
     - Effect: even under the universal bound the dipole stays at least 1e4 below every limit.
5. **alpha_c -> 0 (C6).** Under B1 and B2 the khronon flux vanishes monotonically, as alpha_c^(5/2) (UV) and at most
   alpha_c^2 (universal). XC1's strong-coupling momentum drops below 1e3 x the LHC once alpha_c < 1e-16. This is the
   fourth place alpha_c > 0 is load-bearing (L340 H4, XC1, XC2, and now this lane). Under the counterfactual B3 with
   the universal factor the flux would not vanish; only strong coupling stops it.
6. **MUTATE (lambda_K = 2).** The window gate flags it: it lies outside L340's c_2 window, and in the plain -c_2 K^2
   branch |G_cos/G_N - 1| = 0.60 > 0.1. rc is 1. Disclosed: the radiation score alone passes lambda_K = 2 under
   B0-B2. Radiation is not what excludes it. In the leaf-average branch (L350 G5) the BBN ceiling has no physical
   origin, and lambda_K = 2 is flagged only as outside the committed window.

## Disclosures

- **C8 coding error, fixed after the first run.**
  - The first run's injection control included the strong-field-G factor [(1-s1)(1-s2)]^(2/3). The 0.99 s_crit point
    therefore failed on that factor (about (2/3)s), not on the dipole, and the run read OPEN.
  - Recoded to isolate the dipole, which is how s_crit is defined in the frozen criteria. The first-run output was not
    kept in the lane.
- **A failed reading row is kept.** "R_1 decreases with xi" is false: R_1 goes 0.56, 0.38, 0.18, then 1 at xi = 1 pc,
  where the filter finally screens k_UV.
  - The frozen primary takes the maximum over the committed floors, which is not the maximum over all xi >= floor.
  - A POST HOC row confirms R_1 never exceeds the universal bound on extended grids (xi up to 100 pc, C_0 from 1e-4
    to 10). The universal row already passes B1/B2 everywhere, so the verdict does not depend on this.
- **Not blind.** Rough estimates were made while reading the formulas, before the freeze (listed in FROZEN_CRITERIA
  sec. 0).
- **Literature values are PROVISIONAL.** They were read through a summarising fetch tool, with no PDF fetched. Read
  twice: Barausse's coefficients, the PPN formulas, Foster eq. 70, the J1738 GR value. Read once: Z, Yagi's PRL Pb-dot
  form, the double-pulsar masses (MPIfR compilation page, used only for v^2).
- **Double pulsar.** Only the abstract's "1.3 x 10^-4 (95% conf.)" was verifiable. The full-text tables were
  truncated, and one fetch returned another system's numbers, which were discarded.
- **J0348+0432.** The MPIfR page also lists revised masses (1.806 / 0.154 Msun); their source was not read. The lane
  uses Antoniadis et al. 2013's own consistent set.
- **Record inconsistencies noticed, not load-bearing here.**
  - L340 P1 uses |alpha1| < 1.1e-5, which matches no value in the DOOR11 bounds table (that table has 2.1e-5 and
    3.5e-5). alpha_c's ceiling is set by alpha2, so nothing changes.
  - Recipe I5 and XC1 call 0.031 / 0.045 pc "canonical / alt". L340's JSON shows these are the canonical quadrupole
    and monopole floors; the alt floors are 0.033 / 0.049. All of them are scored here.
- **The strong-field-G factor** is degenerate with GR-based mass inference. It matters only at |s| ~ 1e-3 (B3); under
  B1/B2 it is ~1e-9.

## What this lane cannot say

- It does not compute neutron-star sensitivities at alpha_c != 0; it brackets them.
- The wave zone is the decoupling-limit quadratic action on a homogeneous Galactic background. Metric mixing in the
  MOND regime and the binary's own filtered field enter only through the universal bound.
- It is leading post-Newtonian order, not a timing analysis.
- One gate on one chassis. It is not "the theory works". kappa = 1/2 remains FITTED, and the dark sector still
  requires the cold mass.
