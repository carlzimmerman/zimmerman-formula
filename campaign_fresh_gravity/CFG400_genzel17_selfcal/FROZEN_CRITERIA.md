# CFG400 FROZEN CRITERIA: the first self-calibrated a0(z) test. Genzel+2017's six deep outer curves (z 0.85-2.38)

Committed alone, before any digitising. kappa = 1/2 FITTED. No dark-matter particle species: the cold MASS is still required and is
kept. No knob scans. Never "theory closed"; never "the data favour the framework". Owner (2026-10-06, chat "Nobel Prize and
neutrinos"): "yeah" to fetching Genzel+2017 (arXiv:1703.04310, PDF 1,379,733 bytes, sha256 9926059e...d5e4, in
_external_data/arxiv_pdf/; fetched with that approval) and checking the on-disk overlaps; "swing it bro".

**Question.** CFG385: discs that span the Newtonian and deep regimes calibrate their own baryon scale. Do Genzel+2017's six curves,
each with its OWN free calibration, prefer the DE-tracking a0(z) (the owner's law) or a0 proportional to H(z)?

## Data extraction (declared)
- Figure 1 (PDF page 3) is vector. For each galaxy, digitise the major-axis v_rot sin(i) points and the sigma points, with their
  error bars, by calibrating each panel's axes from its own tick-label positions. The digitiser is validated first (C1-C3).
  Points on both sides are folded by abs(offset) (receding and approaching averaged where both exist, each kept otherwise).
- Deprojection: v_rot = v sin(i)/sin(i) with Table 1 inclinations. Circular speed with Genzel's own asymmetric-drift term:
  v_c^2 = v_rot^2 + 3.36 sigma0^2 (R/R_1/2) (Table 1 sigma0 and R_1/2), as the paper uses. g_obs = v_c^2/R.
- Points with R < PSF FWHM/2 are dropped (beam). PSF: AO 0.2" / seeing 0.6" per the caption; the per-galaxy value is read from
  the paper's text if stated, else seeing 0.6" (conservative).
- Baryon SHAPE (the normalisation is per-galaxy free): exponential disc with R_1/2 (Table 1 n = 1 fit) plus a bulge of R = 1 kpc
  with Table 1 Mbulge/Mbaryon; g_bar(R) from the thin-disc (Freeman) + spherical-bulge forms.

## Model and statistic
- For law L in {DE: a0(z)/a0(0) from DESI CPL (w0, wa) = (-0.838, -0.62), sqrt(rho_DE); RIVAL: E(z) = H(z)/H0; FLAT: 1 (reported)},
  a0(0) fixed at the footing value (canonical 9.36e-11 and alt 1.13e-10, never pooled), kernel nu_mono (P2 reported).
- Per galaxy: g_pred(R) = f_j g_bar(R) nu(f_j g_bar/a0_L(z_j)), with f_j free (profiled). Data errors from the digitised error bars
  (velocity error propagated to g), with a 0.05 dex floor per point.
- chi2_L = Sum_j min over f_j of Sum_i (log g_obs - log g_pred)^2/err^2. Delta chi2 = chi2_RIVAL - chi2_DE.

## Verdict (declared)
- **SEPARATES** if abs(Delta chi2) >= 9 (3 sigma, 1 dof-equivalent) on BOTH footings, in the same direction. Name the direction.
- **LEANS** if 4 <= abs(Delta chi2) < 9 on both footings in the same direction.
- **NON-DIAGNOSTIC** otherwise.
- Forecast check (reported): sigma(log a0) from the CFG385 Fisher model at the digitised y and errors. If it is above 0.22 dex,
  a non-diagnostic outcome is expected and is said so.
- Pressure systematic (reported): rerun with the asymmetric-drift term halved and doubled.

## Controls
- C1 digitiser: the axis calibration reproduces at least 3 labelled tick values per panel to within 1% of the axis range.
- C2: the digitised v_rot sin(i) at R_1/2, corrected as above, reproduces Table 1 vc(R_1/2) within 20% for >= 5 of 6 galaxies.
- C3: the point counts per galaxy are >= 4 after the beam cut; otherwise the galaxy is dropped and reported.
- MUTATE: every digitised outer point (R > R_1/2) has its velocity multiplied by 1.3. The Delta chi2 must move by > 4 (rc 1).

The 5 on-disk KMOS3D x SINS overlaps are NOT in this lane (they need cube extraction; a later lane).
Local compute only after the approved fetch. No other downloads.
