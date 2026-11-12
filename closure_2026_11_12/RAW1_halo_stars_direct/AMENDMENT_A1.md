# RAW1 AMENDMENT A1 (2026-11-12, written before the re-run; FROZEN_CRITERIA.md is not edited)

## What happened

Run 1 (output kept as `raw1_run1_K6b_FAIL.out`) passed K2 to K5 and K6a, then FAILED check K6b and stopped
before any kinematic quantity was computed: 4.85 per cent of the 5,441 S1-S2 stars have dereddened g outside
[15.9, 20.1] (range 15.71 to 20.99). The frozen magnitude window (dereddened g in [16, 20], from memory of
the MWS BHB target class) is therefore wrong, as K6 was designed to detect.

## What was then looked at (magnitudes and target bits only; no velocity, no proper motion, no distance
distribution)

Observed g and r (from FLUX_G, FLUX_R), MAG_DERED_G, MWS_TARGET and SURVEY of the PRIMARY stars:
- 501 stars have MWS_TARGET = 0 (targeted by other programmes or SV); they include every star fainter than
  dereddened g = 20.1. Their magnitude selection is not known.
- MWS-targeted stars fall in classes whose observed r runs 16.03 to 19.22 (two classes, 4,192 stars) and one
  class (MWS_TARGET = 64 alone, 732 stars) whose observed r runs 19.05 to 20.21. So the MWS selection is a
  cut in observed r near 16 and 19 for the main classes, extended to r near 20 by a separate faint class
  whose completeness relative to the main classes is not known.

## Changes (each before any kinematic number)

A1.1 Alpha-fit sample and windows (replaces the window rule of section 4.2): only stars with SURVEY = main
     and MWS_TARGET != 0, and observed r (22.5 - 2.5 log10 FLUX_R) inside the window, enter the alpha fit.
     Nominal window: observed r in [16.2, 18.9], inside the main classes' edges (one documented selection,
     flat-in-magnitude assumed). Window edges along each line of sight: d_lim = DIST * 10^((r_lim - r_obs)/5)
     (extinction held fixed along the line of sight beyond the star's distance range; the catalogue's DIST
     agrees with 10^((g - M_g + 5)/5) for 100 per cent of stars, K6c). The nominal window reaches only about
     45 kpc for a typical BHB, so the single slope over 20 to 80 kpc is constrained mostly inside 45 kpc;
     this is stated as a limit.
A1.2 New fragility variant (added to section 7's list, which makes FRAGILE harder to avoid, not easier):
     the two-class window, observed r in [16.2, 19.9] with the same MWS-targeted main-survey stars, which
     assumes the faint class is as complete as the main classes.
A1.3 K6b replaced by K6b': fewer than 1 per cent of MWS-targeted main-survey stars with observed r < 19.0
     lie below 15.95, and fewer than 1 per cent of all MWS-targeted main-survey stars lie above r = 20.3.
     This check was set after the magnitudes were seen; it is a consistency check, not a blind one.
A1.4 Section 10's reported "faint limit 19.5" (dereddened g) becomes "faint limit r = 18.5" (observed r).
A1.5 The synthetic check K1 draws its alpha-fit distances inside the amended windows.

Nothing else changes: samples for the velocity fits (S1 to S6), bins, estimators, models, labels,
thresholds, checks K1 to K5, and mutations are as frozen.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
