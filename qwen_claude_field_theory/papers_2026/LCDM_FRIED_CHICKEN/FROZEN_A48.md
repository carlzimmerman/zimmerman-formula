# FROZEN A48: "the law is produced by data systematics on ordinary LCDM halos"

Frozen before any A48 number. Script `scripts/recipe49.py`, output `scripts/recipe49.out`, checkpoint `scripts/recipe49.json`. COVERAGE_MAP.md classes (1) (M/L trend, gas systematics) and (6) (beam smearing, sample selection). Quarantined experiment: rival language, adopts nothing, never feeds anything outside this folder. Passing shows freedom, not evidence. kappa = 1/2 FITTED; not theory closed.

Known before freezing (from the record, no new number): A20(b)/A40 noiseless plain-LCDM mock (SHMR + Diemer19, (1 - f_b) NFW, no contraction, Upsilon 0.5/0.7) against the law: E1 0.1419, E2 0.2877, E3 0.1613, bins +0.161 at log g_b -12 falling to +0.004 at -9.0, fitted a 1.576e-10 (`recipe41.out` l.109-112). The mock lies ABOVE the law everywhere, most at low g_b (gas-dominated, outer points). SPARC observer fit (A20): scatter 0.1489 all, 0.0814 on errV/V <= 0.05, a0 8.03e-11. The law's own rms to observed on all 3373 points: 0.1951 (A6).

## What lib.load() and the SPARC table give (checked)

lib.load: 171 galaxies, 3373 points; per point R, V_obs, errV, V_gas, V_disk, V_bul (rotmod; V_gas includes He 1.33 as SPARC built it, V_disk and V_bul at Upsilon = 1); per galaxy L[3.6], R_disk, M_HI, Q. `SPARC_Lelli2016c.mrt` also gives T, D, e_D, f_D, Inc, e_Inc, Reff, SBeff, SBdisk (central disc SB), RHI (HI radius at 1 Msun/pc^2; 0 for 4 galaxies), Vflat (0 = no flat part), Q, and the HI/Halpha reference codes. There is NO beam column and no colour column. Rotmod has SBdisk/SBbul profiles but no HI surface-density profile.

## LCDM rows (the "ordinary LCDM halos")

N0: the A20(b)/A40 noiseless mock, reimplemented from `recipe41.py` (same functions: gbu, halo, m200_of, Diemer19 c(M, z), f_b = min(M_b/M200, 0.5)), 0 knobs tuned. N0c: the same with full Blumenthal contraction (secondary, printed only for each family's best setting). R11b is not used: its knobs were tuned on the law's curves, so it is not "ordinary". The systematic is applied to the truth or to the observation as each family says; the observer always uses nominal SPARC baryons unless reading beta.

Two readings for the baryon families (c) and (d):
- alpha (primary, the swoop): the TRUE baryons carry the systematic, the observer uses nominal SPARC baryons. Mock-observed curve g = g_b,true + g_DM(halo from true M*), graded against law(g_b,nominal, A0) with lib.grade.
- beta (secondary): the community adopts the systematic; mock g as in alpha, graded against law(g_b,true, A0).
And the law's own fit to the observed data with the systematic applied to SPARC baryons: refit a0 (lib.fit_a on (g_b', g_obs)), shift log10(a0/A0), rms to observed at the refit a0 and at A0 (baseline 0.1951), and the A20 observer fit (per-galaxy u, prior 0.1, one global a0) scatter on good points and a0 (baseline 0.0814, 8.03e-11).

## Gates (every family; frozen)

- E1 rms to law <= 0.02 dex, E2 p95 per-galaxy <= 0.04, E3 worst 0.5-dex bin <= 0.02 (lib.grade, bins with >= 50 points).
- Holdout: knobs tuned on GS[::2] (minimum E1 there), unseen rms to law on GS[1::2] <= 0.025.
- Tie gates on the scale the systematic produces (the fitted a of the family's best mock-observed curves): G1 kappa_eff = a/(c sqrt(G rho_DE)) within 0.05 dex of 0.5; G3 a(z)/a(0) at z 1, 1.5, 2.33 (Diemer19 c(M, z), 200c of rho_crit(z), M200 held, the systematic held fixed in physical units, as A40) inside [0.76,1.03], [0.71,1.12], [0.33,1.21]; GT with the LCDM a(z) ratio in each A29 background (rho ratios hard-coded from recipe41/recipe31; approximation as frozen in A40); G4 rms of per-galaxy fitted a over log M200 11 to 12.5 <= 0.1 dex; G5 halo pull G M_DM/r^2 >= 0.1 a_T at 1 to 30 kpc in the median galaxy (the halo is operative; expected trivial PASS). G2 is 0 for every halo route in one cosmology (A26/A29 slopes); printed as "not native" and not recomputed.
- Verdict per family: "SYSTEMATIC MAKES THE LAW" only if E1, E2, E3 and holdout pass with every knob inside its frozen allowed range. A pass outside the range is reported as "needs a disallowed systematic". Tie gates graded separately; a shape pass with tie fails is "shape bought, no tie".

## (a) Beam smearing

SPARC has no beam column. Model, all choices fixed now: thin disc at the table inclination (clipped to [15, 89] deg), circular rotation V(R); Gaussian beam FWHM theta_b arcsec, sigma_b = theta_b x 4.8481e-3 x D[Mpc] / 2.3548 kpc. HI surface density (no profile in SPARC): Sigma(R) = 1 for R <= R_HI, exp(-(R - R_HI)/(0.2 R_HI)) beyond (provisional shape; R_HI from the table, or the last measured radius when RHI = 0). No central HI hole (holes would make smearing worse; stated). Observed velocity at radius R_k = first moment along the major axis, M1(x = R_k, y = 0) = int Sigma v_los K / int Sigma K, v_los = V(R) sin i x/R, R = sqrt(x^2 + (y/cos i)^2), divided by sin i. The Gaussian kernel is separable: column integrals over y on a grid, then a 1D convolution in x. V(R) at any R: baryons V_b linear in R from 0 to the first point, rotmod values between points (linear in R), V_b^2 proportional to 1/R beyond the last point; halo analytic (NFW mass). Residual smearing left in the published curve (many SPARC curves were corrected by their authors or use Halpha inner points): V_obs = V_true + f_bs (V_smeared - V_true).
Knobs (2, grid, fixed now): theta_b in {15, 22.5, 30} arcsec (provisional typical WSRT/VLA HI beams, from memory), f_bs in {0.25, 0.5, 1.0} (1.0 = uncorrected first moment, the upper bound). 9 cells, plus f_bs 0 (control = N0).
Graded: (i) smeared N0 against law(g_b) (the swoop: observed = smeared LCDM truth); (ii) smeared law against observed SPARC (the law's fit with smearing modelled: rms to observed, refit a0); (iii) diagnostic: smeared law against the law (size of the systematic) and smeared N0 against smeared law. Holdout: cell chosen on GS[::2]. Tie gates on the best cell (beam fixed in kpc at z, stated).
Expected: smearing lowers inner, high-g_b velocities only; N0's excess is at low g_b (outer points), where smearing is negligible. E1 moves by under 0.01, FAIL in every cell. The law's rms to observed moves by under 0.005.

## (b) Sample selection

b1, observable cuts on the real sample (fixed now): Q = 1; Q <= 2; Inc >= 30; Q <= 2 and Inc >= 30 (A28's subset); HI-rich M_HI/M* >= 1 (M* = 0.5 L); extended HI R_HI/R_d >= its median; Vflat > 0. For each subset: N0 E1, E2, E3 against the law on that subset (egates restricted), N0 fitted a; the law's refit a0 and rms to observed on that subset. The question: does the LCDM-law gap vanish in any SPARC-like selected region?
b2, halo-dependent selection at fixed SPARC baryons: K = 40 halo realisations per galaxy (A20 scatter: Upsilon 0.1 dex, SHMR 0.15 dex, c 0.11 dex, independent; seed 4900), selection applied per realisation:
- SF1 curve-class match: flatness F = max/min of V over the last 3 points - 1 <= 0.05 defines "flat"; a realisation is kept if its class equals the class of the observed SPARC curve under the same rule (conditioning on an observable, not on the law). Diagnostic: agreement of this rule with the table's Vflat > 0 on the real curves.
- SF2 disc stability (Efstathiou, Lake & Negroponte 1982, from memory): epsilon = V_max/sqrt(G M_*/R_d) >= 1.1 over the data radii; unstable (barred, disturbed, lower Q) realisations dropped.
- SF3 halo-strength weight: w = exp(beta z_h), z_h = standardised (within each galaxy's 40) log of the halo pull at 2.2 R_d; beta in {0, -0.5, -1, -2, -3, -5} (negative favours weak halos). Allowed range, fixed now: the selected population's weighted mean shift in log M200 at fixed true M* within [-0.3, 0] dex (HI-selected samples in lower-mass halos, ALFALFA clustering, FROM MEMORY, provisional) AND in log c within [-0.11, 0] dex (one c-scatter). beta beyond that is "not realistic".
- SF1 and SF2 and SF3 combined.
Graded per beta (with SF1, SF2 on and off): weighted intrinsic E1, E2, E3 against the law (each galaxy's realisation weights normalised to 1; galaxies with all weights 0 dropped and counted); weighted rms at own fitted a; with observation errors (A20: D, i, errV), 3 samples of one weighted-drawn realisation per galaxy, observer fit: B1 good-points scatter within 0.02 of SPARC's 0.0814, B2 a0 within 0.05 dex of A0. Holdout: beta (and SF switch) chosen on GS[::2] by weighted E1, unseen on GS[1::2]. Knobs: beta (1) and 2 switches; thresholds fixed from the literature/rule.
Expected: b1 subsets leave N0 E1 at 0.12-0.16 in every subset (the excess is in gas-rich outer points, present in all). b2: SF1 and SF2 barely move E1 (SF2 favours stronger halos, wrong way); beta -5 lowers E1 toward 0.08-0.10 and a toward +0.1 dex, but only with M200 shifts beyond -0.3 dex; no allowed setting passes E1. B1 passes or nearly passes (A40), B2 fails.

## (c) Mass-to-light as a systematic trend

Upsilon_disk = 0.5 x 10^d x (M*/1e10)^p x (SBdisk/100 Lsun pc^-2)^q; Upsilon_bul = 0.7 x 10^d x (M*/1e10)^p x 10^(A_imf clip(log M* - 10, 0, 1)); M* = 0.5 L (lib nominal) in the trend arguments; true M* = sum of components (disc L_disk = 2 pi SBdisk R_d^2 times Upsilon_disk, the rest of L times Upsilon_bul), used for the SHMR.
Allowed ranges (fixed now): d in [-0.097, +0.041] (Upsilon 0.40 to 0.55 at 3.6 um, Schombert, McGaugh & Lelli 2019, arXiv 1811.10579 abstract via ar5iv, PROVISIONAL); p in [-0.05, +0.10] (same paper's sec. 6.3 as summarised: about 0.45 for the bluest to 0.6 for the most massive spirals, a slope near +0.04 dex/dex; widened, PROVISIONAL); q in [-0.05, +0.05] (no published SB trend found; colour-SB correlation, FROM MEMORY); A_imf in [0, 0.25] dex on bulges (Salpeter-like IMF in massive spheroids, FROM MEMORY). 4 knobs.
Graded: corners of the box (16), then a bounded minimisation of reading-alpha E1 over the 4 knobs (L-BFGS-B, 4 starts) on all galaxies and on GS[::2] (holdout); knobs at bound disclosed; reading beta at the same knobs; the law's refit on data at the same knobs and at the knobs that most move a0. Diagnostic (not a gate): the same minimisation with each knob widened to [-0.5, +0.5] dex, to show what a trend would have to be.
Expected: N0's excess sits at low g_b, gas-dominated, where Upsilon does nothing; E1 stays >= 0.12 in the box and >= 0.08 widened; FAIL. The law's refit a0 moves by -0.05 to +0.03 dex across the box (d dominates), rms to observed by under 0.005.

## (d) Gas mass systematics

V_gas,true^2 = V_gas^2 x k_g x X/1.33 + V_mol^2, V_mol^2 = V_disk^2(Upsilon = 1) x M_mol/L_disk, M_mol = f_mol x M* x (M*/1e10)^s (molecular gas with helium, distributed like the stellar disc; L_disk as in (c); M* = 0.5 L). M_b updated for f_b; M* (SHMR) unchanged.
Allowed ranges (fixed now): X in [1.33, 1.40] (helium factor, as the lane brief); k_g in [0.9, 1.1] (HI flux calibration and distance-independent mass error about 10 %, FROM MEMORY); f_mol in [0, 0.15], s in [-0.5, 0] (molecular fraction about 0.1 weakly mass dependent, xCOLD GASS type, FROM MEMORY / search summary PROVISIONAL; s < 0 lets CO-dark gas grow in dwarfs). 4 knobs (X and k_g degenerate: effective 3).
Graded exactly as (c). Diagnostic widening: k_g in [0.3, 3], f_mol in [0, 1].
Expected: N0's excess is at low g_b; lowering gas (k_g 0.9) lowers the truth there by a few per cent of a dex, raising gas makes it worse. E1 >= 0.12, FAIL. The law's refit a0 moves under 0.03 dex.

## Combined

(c) + (d) together (8 knobs, all in their boxes), minimised on all and on GS[::2], then with the best (a) cell added, graded the same way. Tie gates on the combined best.

Parameters counted per family: (a) 2 grid knobs; (b) beta + 2 switches (selection thresholds fixed); (c) 4; (d) 4 (3 effective); combined 8 + 2. The 3 A20 scatter amplitudes (b2 only) are literature values, not tuned.

Expected overall: no family and no combination puts ordinary LCDM halos on the law inside the allowed ranges (E1 >= 0.08); the fitted a stays +0.15 to +0.23 dex high (G1 FAIL, kappa_eff about 0.7-0.85), G3 and GT fail as in A40, G4 fails, G5 trivially passes. The law's own fit to data moves by at most a few hundredths of a dex in a0 under any allowed systematic.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.

## RESULTS (written after the run; criteria above unchanged)

Run: `scripts/recipe49.out`, 329 s wall, peak RSS 356 MB, single thread. Line numbers refer to that file.

Bug disclosed. The first run produced NaN in some beam-smearing cells: the halo velocity was evaluated at R = 1e-6 kpc, where NFW mu(x) cancels to a tiny negative number and sqrt went NaN. Fixed by setting R >= 1e-3 kpc and clipping the halo mass at >= 0. The control was also changed from a 0.05" beam, which is below the grid spacing, to a 1" beam plus a grid-resolution check. The wrong run was killed during (a) and is kept as `scripts/recipe49_before_fix.out`. Its non-NaN numbers match the fixed run.

Controls (l.7-13, 16-18). N0 reproduces A40: E1 0.1419, E2 0.2877, E3 0.1613, a 1.576e-10. The SPARC observer fit reproduces A20: 0.1489 / 0.0814 / 8.03e-11. The law's rms to observed is 0.1951. Smearing grid, 1500 vs 4000 cells at 15": max |dV/V| 0.0002. 1" beam: median max |V_s/V - 1| 0.0077, but up to 0.37 in one galaxy, where the beam is below the grid; this does not affect 15-30" beams. The table's L_disk = 2 pi SBdisk Rd^2 exceeds L in 145 of 171 galaxies, so f_disk = 1 there (l.3): the bulge IMF term then does not enter M*, and V_mol uses L in place of L_disk.

(a) Beam smearing (l.20-53). Full first-moment smearing changes the law's own curve by > 10 % at 27-43 % of points. Forward-modelled into the law's fit to the data, it ruins that fit: at 30", f 1 the rms to observed is 0.389 at the refit a0 of +0.299 dex (l.42). At 15", f 0.25 it is 0.1957 at +0.043 dex (l.43). So the published curves are not left heavily smeared; only small f_bs is consistent with them. Smeared N0 against the law: E1 0.132-0.379 across the 9 cells. Best: 30", f 0.25, E1 0.1316, E2 0.2626, E3 0.1360 (l.35); holdout unseen 0.1197 (l.36). All FAIL. Smearing lowers the high-g_b end (bin -9.0 goes to -0.134) and leaves the +0.136 low-g_b excess (l.39). Tie gates (l.44-53): kappa_eff 0.700 (G1 FAIL); a(z)/a(0) 1.316, 1.666, 2.588 (G3 FAIL); GT FAIL in all 8 backgrounds; G4 0.140 FAIL; G5 PASS. Verdict: SYSTEMATIC DOES NOT MAKE THE LAW.

(b) Selection. b1 (l.57-65): in every SPARC-like subset N0 stays at E1 0.125-0.170 and its a at +0.18 to +0.24 dex. The extended-HI half is closest (E1 0.1245, E3 0.0892). The law's own refit a0 moves between subsets, from -0.039 (HI-rich) to +0.096 dex (Q = 1, rms 0.1632). b2 (l.66-112): SF1 (curve-class match; 0.848 agreement with the table's Vflat flag) and SF2 (ELN stability) each make E1 worse. SF2 selects heavier halos, as expected. A weight toward weak halos lowers E1 to at best 0.1292 (beta -2, NOT REALISTIC: log c shift -0.154). The best realistic setting is beta -1 (shift log M200 -0.059, log c -0.092): E1 0.1371, E2 0.2241, E3 0.0688, FAIL (l.73, 97). Stronger beta makes E1 worse again (l.99-101), so no selection strength reaches 0.02. Holdout unseen 0.1343 FAIL (l.98). Not expected: realistic beta -1 buys the SCALE. Observer B2 a0 is +0.049 dex (PASS, l.73), and the tie G1 on the weighted curves gives kappa_eff 0.518 (PASS, l.103). But B1 fails (0.1138 vs 0.0814), E1 to E3 fail, G3 is 1.33/1.69/2.63 (FAIL), GT fails in all 8 backgrounds, and G4 is 0.143 (FAIL). B1 passes only at NOT REALISTIC beta. Disclosed: SF2 cells and SF1+SF2 cells shift log M200 upward, outside the frozen range, and are labelled NOT REALISTIC by the frozen rule. Verdict: SCALE BOUGHT BY A REALISTIC SELECTION (G1, B2), SHAPE AND z NOT. The selection does not make the law.

(c) M/L trend (l.114-141). 16 box corners: E1 0.126-0.234. The bounded search gives E1 0.1222 (d at its lower bound -0.097, p -0.034, q -0.010, A_imf 0.150), E2 0.2766, E3 0.1478 (bin -12.0 is +0.148). Reading beta 0.1332; holdout unseen 0.1172; N0c 0.1704. All FAIL. Widened to ±0.5 dex: 0.1197 FAIL (l.130), so no trend of any size works. The trend does move the law's own fit: refit a0 from -0.139 to +0.157 dex across the corners and +0.100 at the best knobs, with rms to observed 0.2005-0.2133 against 0.1951 (l.126-128). Ties: kappa_eff 0.635, G3 FAIL, GT FAIL, G4 0.197 FAIL, G5 PASS. Verdict: DOES NOT MAKE THE LAW.

(d) Gas (l.142-169). Corners E1 0.1416-0.1554. Best: X 1.33, k_g 0.9, f_mol 0, all at bounds (less gas), E1 0.1416, same as N0. Holdout 0.1305; widened to k_g 0.35, E1 0.1408 (l.158). All FAIL. The law's refit a0 moves from -0.174 dex (corner with He 1.40, k_g 1.1, f_mol 0.15, s -0.5) to +0.012 (l.154-156). Ties: kappa_eff 0.833, G3 FAIL, GT FAIL, G4 0.131 FAIL. Verdict: DOES NOT MAKE THE LAW.

Combined (c)+(d), 8 knobs (l.170-186): E1 0.1192 with 6 knobs at bound; holdout unseen 0.1146; adding the 30" f 0.25 beam gives 0.1217. FAIL. kappa_eff 0.646, G3/GT/G4 FAIL.

Expected vs found: as frozen for (a), (c), (d) and the combined row. Not foreseen:
- In (a), smearing size: up to 0.38 dex at f 1.
- In (a), the law's fit to data degrades strongly when full smearing is modelled.
- In (b), realistic selection on halo strength buys G1 and B2.
- In (c), and in (d) at the dwarf-heavy molecular corner, the law's own a0 moves by 0.14-0.17 dex; I expected a few hundredths. The law's rms to observed worsens at those settings.
Everywhere the failure is the same: a +0.13 to +0.16 dex excess at log g_b -12, in gas-dominated outer points, which no listed systematic reaches.

Provisional or from memory:
- Beam sizes 15-30", the HI profile shape and f_bs.
- The ELN 1.1 threshold.
- The ALFALFA-based [-0.3, 0] dex M200 realism range.
- The Upsilon range and slope (SML19 abstract and summary via ar5iv; a first WebFetch to a wrong arXiv id returned an unrelated paper and was not used).
- The SB trend range, the IMF amplitude, and the HI calibration of 10 %.
- The f_mol 0-0.15 range (search summary only; no fitted scaling found).
No downloads.

Parameters: (a) 2 grid; (b) beta + 2 switches; (c) 4; (d) 4 (3 effective); combined 8 + 2.

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
