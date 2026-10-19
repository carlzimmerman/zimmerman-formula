# CFG836: published hot-gas measurements vs the CFG746 sealed falsifier (literature, no compute)

**Label: NOT DIAGNOSTIC (NO RESULT, with the exact decider stated).** No 2022-2026 source measures the hot / total
circumgalactic gas mass inside 100 kpc of quiescent galaxies at log M* 10.5-11.0. Eight sources were read; none maps onto the
sealed test (criteria in `FROZEN_CRITERIA.md`, written before the numbers). The falsifier (M_hot < 0.0853 M*, i.e. 5.4e9 Msun) is
neither reached nor avoided. The one usable bound, an X-ray luminosity ceiling, sits above the sealed band for almost all
stated conversions.

Settings: kappa = 1/2 FITTED; footings never pooled; no particle species; not "theory closed". Everything below that comes from a web
look-up is **PROVISIONAL**: the page tool returns a summary, not the table. "A" = number also seen in abstract-level text,
"T" = number from a summarised table only. Hand arithmetic only (no code was run).

## 1. Per-source table (one trial each, none dropped after reading)

Sealed target: M_hot(<100 kpc)/M* in [0.171, 0.247]; falsifier line F = 0.0853.

| # | source (arXiv; journal) | what it measures | sample (log M*, quiescent?, isolated?) | aperture | number (status) | class |
|---|---|---|---|---|---|---|
| S1 | 2411.19945 (A&A 693, A197), eRASS:4 CGM stacks paper III | L_X,CGM(0.5-2 keV), beta-model fits; NO gas mass, NO kT/Z | CENQU bin 10.5-11.0, median 10.8, N = 16485 (T); quiescent centrals (group-finder), "about 70%" purity (garbled, T); not isolated-selected | within R500c | 1.1 +/- 0.4 e40 erg/s (A, T; matches the CFG580 record); fit r_c ~1-5 kpc, beta ~0.35-0.45 (T) | NOT DIAGNOSTIC (L_X-only, item 6); gives a CEILING, see 2 |
| S2 | 2601.16499 (ApJ, accepted), nearby L* with eRASS | M_hot from beta-model integral, 10-200 kpc | 474 L* galaxies (M_B = -20.5 +/- 1), median M* = 2.4e10 (log 10.38; split of 237+237, T), mostly main-sequence, no quiescent fraction given | 10-200 kpc | M_hot = 2e10, log 10.3 +0.2/-0.5 (A, T); low-SFR half log 10.5 +0.1/-0.5 (T); assumes kT = 0.23 keV, solar Z, isothermal, all emission = CGM | NOT DIAGNOSTIC (median M* below 10.5; mixed SFR; q unknown). Unscored information in 3 |
| S3 | 2508.09514 (ApJ 2025), tSZ in CGM II | Compton-y of ~0.7M quiescent (WISE x DESI) vs ACT DR4 | halo mass assigned from stellar mass via an SHMR (LCDM-calibrated); M200 10^12-10^14 | R200 | values only in figures (Fig. 7, 9); S/N of stacked y 4.9-18.5 (A) | NOT DIAGNOSTIC (no table; SHMR; aperture R200; halo-mass binning) |
| S4 | 2604.19745 (kSZ DESI DR2 x ACT DR6, part II) | kSZ tau profiles, BGS | threshold bins M* > 10, 10.5, 11, 11.25; mean halo log Mh = 13.26 / 13.34 / 13.51 / 13.68 [Msun/h] (T); no quiescent split | up to R_vir (CAP 1-14 arcmin) | gas fraction ~0.2-0.3 of cosmic near R_vir (text, approximate); no gas mass | NOT DIAGNOSTIC (group-scale halos; aperture >> 100 kpc; no split) |
| S5 | 2607.08721, ACT DR6 on Planck locally bright galaxies | cylinder Y within 3 arcmin | centrals, bins from 11.1; tabulated 11.2-11.8; bins below 11.1 "noise dominated, not shown" (T) | 3 arcmin (about 750 kpc at z = 0.25, source's own scaling) | Y(11.2-11.3) = 1.4 +/- 1.0 e-6 arcmin^2 (T) | NOT DIAGNOSTIC (mass above 11.2; aperture; noise 2-3 orders above the sealed Y) |
| S6 | 2609.08939, ACT DR6 + DESI DR1 tSZ tau | y_AP in 2.7 arcmin disk, BGS threshold bins | mean log M* 10.72 / 10.82 / 10.94 / 11.08 / 11.25 / 11.42 (T), mean log Mh 13.1-13.5; no quiescent split | 2.7 arcmin (about 0.7 Mpc, my z = 0.28 arithmetic) | M* > 10.5: y_AP = 0.04 +/- 0.02 (fiducial ILC), 0.02 +/- 0.02 (CIB-deproj.), 0.01 +/- 0.04 (dbeta-deproj.), all x1e-7 (T); lowest two bins negative with radio sources in | NOT DIAGNOSTIC (group halos; aperture; 1 sigma noise 16x the sealed mean y, see 2) |
| S7 | 2107.14281 (ApJ 2022), Planck SZ of 11 nearby L* spirals | M_hot(<250 kpc) | spirals only, 3-10 Mpc, no M* range | 250 kpc | 9.8 +/- 2.8 e10 Msun at assumed T = 3e6 K (A) | NOT DIAGNOSTIC (spirals; aperture 2.5x; T assumed). Bound vacuous (>> band) |
| S8 | 2609.18006, XMM + Planck SZ of NGC 4594 | single object, two-phase hidden-component analysis | massive isolated disk (M* "several times MW", no log M*), M200 ~ 1e13; quiescence not stated | 33 kpc - 330 kpc annuli, key bin about 50 kpc | kT ~ 0.75 keV, Z 0.3 fiducial; SZ exceeds single-phase X-ray prediction (a = 0.06-0.08); no gas mass tabulated | NOT DIAGNOSTIC (one object, mass above range, no M_hot). Qualitative: gas is ~6x hotter than the sealed 0.115 keV |

Not read, with the reason fixed before any number: the eRASS paper I/II (2401.17308/2401.17309; same stacks as S1, L_X only);
eFEDS stacks (2201.05169; L_X only); 2506.09123 and other simulation comparisons (rule 3); baryonification fits (2507.07991,
model-dependent); LRG kSZ/tSZ papers (log M* >= 11.3, group halos); pre-2022 ROSAT/Chandra samples (out of window; SLUGGS is the record:
CFG57/CFG528).

Deviations from the frozen reading list (disclosed): 2502.08850 (ACT x DESI LRG tSZ) was not read (LRG log M* >= 11, group halos; judged out of range from its
abstract-level description before any number); no Chandra/XMM early-type survey in the 2022-2026 window was found by two searches (the
Virgo early-type Chandra paper is 2021 and cluster-environment; SLUGGS is the record CFG57/CFG528); S6, S7, S8 were added from the searches.

**Same class as the KiDS excess (isolated, quiescent, log M* ~ 10.7, inner bins 52-98 kpc)?** NO source. Closest is S1 (quiescent, 10.8,
but centrals, not isolation-selected, L_X only). S2 is isolation-screened but star-forming-mixed and below 10.5. No source has an
isolated quiescent sample with a mass-linear probe.

## 2. The best single constraint: the S1 X-ray ceiling (hand arithmetic, from committed CFG580/CFG746 numbers)

L_X is a ceiling on M_hot, not a floor (uniform sphere = minimum luminosity, item 6): L(<100 kpc) <= L_X,CGM(<R500c) = 1.1e40 and
L ∝ M^2 at fixed kT, Z. CFG580's canonical rows (M = 5.1e10 Msun, uniform 100 kpc; kT 0.10 to 0.13 keV): Z = 0.1: 3.5e39-1.1e40;
Z = 0.3: 9.8e39-2.9e40; Z = 1: 3.2e40-9.5e40 erg/s. M_max = 5.1e10 x sqrt(1.1e40 / L_580), M* = 6.31e10.

| Z | kT 0.10: M_max, M_max/M* | kT 0.13: M_max, M_max/M* |
|---|---|---|
| 0.1 | 5.1e10 x 1.773 = 9.0e10, 1.43 | 5.1e10 x 1.000 = 5.1e10, 0.81 |
| 0.3 | 5.1e10 x 1.060 = 5.4e10, 0.86 | 5.1e10 x 0.616 = 3.1e10, 0.50 |
| 1.0 | 5.1e10 x 0.586 = 3.0e10, 0.47 | 5.1e10 x 0.340 = 1.7e10, 0.28 |

- Systematic span of the ceiling: factor 5.2 across (Z, kT) (9.0e10 vs 1.74e10). Statistical +/-36% in L is +/-17% in M (1 sigma:
  sqrt(0.7/1.1) = 0.80 at the low end). A centrally concentrated profile (CFG580: r_c = 10 kpc is 1.7x brighter than uniform)
  lowers the ceiling by 1/sqrt(1.7) = 0.77; for a power-law n ∝ r^-1.2 over 100 kpc I get a clumping factor 3.24/1.8 = 1.8, i.e. about
  the same, so the fitted cuspy profile does not change this much (my analytic estimate, not in the paper). Any non-CGM part of the stack
  (XRB residual, hot ISM, AGN) lowers the true CGM share and RAISES the ceiling.
- Lowest corner: Z = 1, kT = 0.13, -1 sigma L, concentrated: 1.74e10 x 0.80 x 0.77 = 1.07e10 = 0.169 M*. That is at the band minimum (0.171)
  and still 2x above F (0.0853 M* = 5.4e9). To reach F, the profile would have to be 6.8x brighter than uniform at the same mass: it is not.
- Conclusion of the ceiling: the sealed band is allowed everywhere; the stack L_X is only a one-sided upper bound. It cannot test the
  falsifier. CFG746's own "consistent, not a test" is confirmed. Note the sealed gas at Z = 1 (CFG746 JSON) emits 3.0e39-8.9e39 (canonical|0.95),
  i.e. 27-81% of the whole stack: at solar metallicity the sealed hot gas would have to be most of the X-ray signal.
- X-ray cannot test the floor either: at F (half the smallest sealed row) L ∝ M^2 is 1/4 of that row's L. CFG746 alt|0.85 row: Z = 0.3 gives
  4.4e38-1.3e39, so 1.1e38-3.2e38 at F; Z = 1 gives 1.4e39-4.2e39, so 3.6e38-1.1e39 at F. All far below the 4e39 statistical error (1 sigma) of the stack.

tSZ noise vs the sealed Y (S6, hand arithmetic): sealed Y D_A^2 = 1.83-2.56e-10 Mpc^2 (CFG746 JSON); take 2.0e-10. At z = 0.28,
D_A ~ 920 Mpc (from memory of the standard distance; PROVISIONAL): Y = 2.0e-10/920^2 = 2.4e-16 sr; the 2.7 arcmin disk (7.85e-4 rad) has
solid angle 1.94e-6 sr, mean y = 1.2e-10. S6's CIB-deprojected y_AP error for M* > 10.5 is 2e-9 (if y_AP is a mean Compton-y in the disk; the
definition was not read). So the 1-sigma noise of a ~1e6-galaxy stack is about 16x the sealed signal, and the signal there also includes group gas
at larger radii. S5: noise 1.0e-6 arcmin^2 x 0.0586 Mpc^2/arcmin^2 (z = 0.25, D_A ~ 830 Mpc) = 5.9e-8 Mpc^2 = about 260x the sealed Y D_A^2.

## 3. Unscored information (S2), why it does not decide

If S2 were scored anyway: own-profile extrapolation of the beta-model to 10-100 kpc. Integral I(X) = ∫ x^2 (1+x^2)^-p dx, p = 3 beta/2, by hand
(Simpson to x = 1, asymptotic beyond):
- full sample (beta 0.52, Rc 8.7 kpc, p 0.78): I(10 kpc) = 0.33, I(100) = 21.8, I(200) = 61.8; fraction M(10-100)/M(10-200) = 0.35;
- low-SFR half (beta 0.41, Rc 9.4 kpc, p 0.615): I = 0.30, 35.4, 124.6; fraction 0.28; the <10 kpc part is <1%.
M(10-100 kpc) = 0.35 x 2.0e10 = 7.0e9 (range 2.2e9-1.1e10, from log M_hot +0.2/-0.5); low-SFR 0.28 x 3.2e10 = 8.9e9 (2.8e9-1.1e10).
With the sample median M* = 2.4e10 the ratio would be 0.29 (0.09-0.46) full, about 0.37 low-SFR (low-SFR M* unknown): nominally in or above the band,
span straddling both F and the band: under the frozen rules this would be NOT DIAGNOSTIC anyway (m_lo about 0.09 is at F; star-forming mix; median 10.38 outside).
The assumptions (kT 0.23 keV, solar Z, isothermal, all emission CGM) are the paper's own; low Z would RAISE the mass. It is a weak hint
that a hot component of order 0.1-0.4 M* exists around main-sequence L* galaxies at 10-100 kpc; not a test of quiescent galaxies.

## 4. Both implications, no choice made

If the gas were found BELOW F (not found here):
- R1 (the sealed reading): the selector C = k M_hot fails as the C3 explanation (CFG746 falsifier).
- R2: it would also match CFG581 (hot gas cools). But CFG581 tested 0.8 / 0.55 M* only (t_cool 0.35-4.2 Gyr, t_cool/t_ff <= 4.0 / 5.9, unphysical
  because < 10). The sealed gas is 3.2-3.6x lighter (0.8/0.221 = 3.62 canonical; 0.55/0.171 = 3.22 alt), so at the same kT, Z and volume, n is
  lower by that factor and t_cool grows by it (t_cool ∝ 1/n): about 1.1-15 Gyr, t_cool/t_ff about 1.6-19 against the 10 line, t_ff = 0.71 Gyr
  (hand scaling of CFG581, NOT a CFG581 result, uniform sphere, same kT/Z). So CFG581 does not by itself say the sealed gas cannot persist; a measured
  absence would not be "just CFG581".
- These do not decide between "selector wrong" and "gas absent for another reason". The sealed falsifier is R1.
If the gas is found at or above the band: the selector survives its sealed test at that class; no mechanism is implied.

## 5. What one measurement would decide it (and what would not)

- A mass-linear probe on the right class: stacked kSZ (electron column, temperature-free) or localized-FRB dispersion measure on 10.5-11.0
  quiescent, isolation-selected galaxies at z <~ 0.1, aperture <= 100 kpc (about 1 arcmin at z = 0.1). It is an upper-bound probe of the hot phase
  (all phases count), so it can EXCLUDE, not confirm.
- Arithmetic for the sealed gas (M = 1.4e10 Msun): N_e = 1.4e10 x 1.989e33 g / (1.14 x 1.6726e-24 g) = 1.46e67; area pi (3.0857e23 cm)^2 = 2.99e47 cm^2;
  mean column 4.9e19 cm^-2 (about 16 pc/cm^3); tau = 6.652e-25 x 4.9e19 = 3.2e-5; kSZ rms ΔT = 2.725 K x 3.2e-5 x 1e-3 (v = 300 km/s) = 0.09 muK per galaxy.
  With a per-galaxy aperture noise of 4-15 muK and velocity-reconstruction efficiency 0.6 the per-galaxy S/N is 0.004-0.014, so a 3 sigma stack needs
  roughly 5e4-7e5 galaxies of that class (order of magnitude only, ignores 2-halo and line-of-sight terms, PROVISIONAL). F-level gas halves the
  amplitude and quadruples the sample need.
- tSZ cannot do it with current maps (16x-260x above the signal), and L_X is a ceiling. A temperature- and metallicity-resolved density profile from
  X-ray spectra would only tighten the ceiling by a factor of up to ~5 (the Z, kT span); it cannot reach F.

## 6. Objections to this result

1. My criteria make a literature-only test almost bound to come out NOT DIAGNOSTIC: the sealed test is at 100 kpc, where the surface brightness
   and the SZ signal are the faintest. The class of results that would count did not appear in the window, so the result is a statement about the
   data, not about the selector.
2. The look-ups are summariser output. Figures I could not read (S3, Fig. 9 "Y vs M*", the quiescent bins) could carry a relevant point; the
   S2 and S1 numbers could differ in the tables.
3. The mass range cut (S2 median 10.38) excludes the only source with a gas mass at ~100 kpc; scored loosely it reads as support. Both statements
   are in the table; the frozen rule decides the label.

Suggested ledger row (orchestrator to enter): `CFG836 | (round-2 lane HOTGAS; criteria FROZEN_CRITERIA.md first) literature test of the CFG746 falsifier: NOT DIAGNOSTIC - 8 sources 2022-2026, none measures M_hot(<100 kpc) for quiescent log M* 10.5-11.0; eRASS:4 L_X ceiling leaves the sealed band allowed (M_max/M* 0.28-1.4 for Z 1-0.1), tSZ noise 16x-260x the sealed Y; kSZ stack of ~5e4-7e5 isolated quiescent z<~0.1 galaxies would decide (exclusion-only). All look-ups PROVISIONAL.`
