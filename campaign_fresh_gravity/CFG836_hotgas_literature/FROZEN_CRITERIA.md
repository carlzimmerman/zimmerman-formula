# CFG836 FROZEN CRITERIA (written before any hot-gas mass, Y, or profile number was read)

Lane HOTGAS, PARAMRED round 2. NO COMPUTE: no code was or will be run; arithmetic by hand, shown. Literature only.
kappa = 1/2 FITTED. Footings 9.36e-11 / 1.13e-10 never pooled. No particle species. Not "theory closed".
Raw data or framework-native only: no LCDM mass function, no simulation comparison enters any verdict.

## What was already seen before this file (disclosure)
- The sealed CFG746 table and the CFG580/581/582/745 record (repo files).
- From one search snippet: the eRASS:4 quiescent L_X(0.5-2 keV) at log M* 10.8 is ~1.1e40 erg/s (this is the number
  already in the CFG580 record, Zhang et al. 2025). No M_hot, no Y, no kSZ profile and no tSZ number was read.

## The target (copied from the sealed CFG746 JSON; hash 79140240f3...)
- M_hot(<100 kpc)/M* band B = [0.171, 0.247] (alt|0.85 ... canonical|0.95), at log M* 10.8 (M* = 6.31e10 Msun,
  so B = [1.077e10, 1.559e10] Msun).
- Sealed falsifier: measured M_hot(<100 kpc) for log M* 10.5-11.0 quiescent galaxies "below half of every row".
  Half of the smallest row: F = 0.5 x 1.0767e10 = 5.38e9 Msun = 0.0853 M*. (Smallest-row basis is the reading
  used throughout; the half of the LARGEST row, 7.8e9 Msun = 0.124 M*, is quoted as a stricter secondary line only.)
- Sealed kT = 0.114-0.120 keV; sealed Y D_A^2 = 1.826e-10 ... 2.563e-10 Mpc^2.
- Conversion constant, taken from the CFG746 JSON itself (ratio Y D_A^2 / (M_hot kT), identical for all four rows):
  K_Y = 1.426e-19 Mpc^2 per (Msun keV). Hand check from constants: sigma_T/(m_e c^2) = 6.652e-25/511 = 1.302e-27 cm^2/keV;
  Msun/(1.14 m_p) = 1.989e33/1.907e-24 = 1.043e57; product 1.358e30 cm^2 = 1.426e-19 Mpc^2. Agrees.
  M_hot = (Y D_A^2) / (K_Y kT).

## Source admissibility (decided now)
1. MASS RANGE. Mean/median log M* of the sample must lie in 10.5-11.0 (in range) or 11.0-11.2 (edge: scored, flagged).
   Above 11.2, or mass bin straddling > 0.5 dex beyond these limits: NOT DIAGNOSTIC for mass (the sealed band is
   per M* at 10.8 only; scaling M_hot ∝ M* outside is NOT assumed).
2. COMPARISON IS IN THE RATIO M_hot/M*, not absolute mass, with M* taken as the source's own stated sample mass.
3. QUIESCENT SELECTION. If the sample is a quiescent (or early-type) subsample: used as is. If it is a mixed sample
   with a stated quiescent fraction q and no split, the most favourable quiescent value is M_mix/q (star-forming
   galaxies carry f_hot ~ 0 in the selector, so the mixture dilutes). A mixed sample with q not stated: NOT DIAGNOSTIC.
   Central vs isolated: KiDS used ISOLATED (f30) lenses. A stack of CENTRALS includes group-hosted centrals with more
   gas, so a central-sample value is an UPPER-leaning estimate for isolated galaxies: a central-sample result below F
   is robust to this; a central-sample result above the band is NOT a clean confirmation (flag it).
4. APERTURE (monotonicity rule, fixed now).
   - Mass inside a sphere is non-decreasing with radius, and a cylinder (projected) integral of a non-negative
     quantity (pressure, density) is >= the sphere inside the same radius. Hence:
     * a measurement in an aperture LARGER than 100 kpc is an UPPER bound on M_hot(<100 kpc) (Y or mass): it can support
       TENSION/EXCLUDED, never CONSISTENT, unless the source's own fitted profile gives the fraction inside 100 kpc
       (then extrapolate with that profile only, with its stated error);
     * a measurement in an aperture SMALLER than 100 kpc is a LOWER bound: it can support CONSISTENT, never EXCLUDED,
       unless the source's own profile extends it.
   - Extrapolation with an assumed profile of my own choosing is not allowed. A beta-model or NFW-like shape taken from
     the source counts as the source's own profile.
   - Background-subtracted stacks that can go negative are used as measured (with sign); no clipping.
5. TEMPERATURE (for Y -> M). M_hot = Y D_A^2 / (K_Y kT). Lowest kT allowed in the conversion (most favourable to the
   selector, gives the largest M for a given Y): 0.10 keV (CFG580's grid floor; below it the gas is not a single hot
   phase). Highest kT (most unfavourable): the larger of (i) the source's own measured/assumed gas temperature and
   (ii) twice the sealed kT, 0.24 keV. No LCDM halo-mass-derived temperature is used by me; if the source supplies
   one it is recorded as a source assumption and enters only the unfavourable end.
6. X-RAY LUMINOSITY. L_X ∝ n^2 so M inferred from L_X depends on kT, Z, clumping and profile; a uniform sphere is the
   minimum-luminosity geometry, therefore an L_X measurement gives a CEILING on M_hot for a given (kT, Z), never a
   floor, and the stack L_X can contain XRBs, the stellar/ISM hot gas, AGN. Hence L_X alone is classed NOT DIAGNOSTIC
   for EXCLUDED (CFG580 already shows 5.1e10 Msun can hide below the 1.9e40 bound) and NOT DIAGNOSTIC for CONSISTENT
   (CFG746: L_X "consistent, not a test"), unless the source ALSO supplies a gas mass or a temperature-resolved density
   profile. A resolved X-ray surface-brightness profile with a deprojected density counts as a mass measurement.
7. SOURCE TYPE. kSZ-derived profiles measure the electron column (mass-weighted, temperature-free): the cleanest map to
   M_hot. tSZ measures M x T. Both need the host galaxy sample to match item 1-3.

## Classes (applied to the span [m_lo, m_hi] of M_hot(<100 kpc)/M* = source value with statistical 1 sigma, combined with
   every conversion range in items 3-6, plus nominal m_nom)
- EXCLUDED: m_hi < F/M* = 0.0853 (below half the sealed minimum even with the most favourable stated conversion).
- NOT DIAGNOSTIC: (a) mass, quiescent selection or aperture cannot be mapped under items 1-4; or (b) the span straddles
  both sides: m_lo < 0.0853 AND m_hi >= 0.171; or (c) L_X-only (item 6).
- TENSION: m_hi >= 0.0853 but m_hi < 0.171 (the best-case end still lies below the band, but above the falsifier).
- CONSISTENT: m_lo >= 0.0853 AND m_hi >= 0.171. Sub-label "nominal in band" if m_nom >= 0.171, else "favourable end
  only".
Statistical 1 sigma is added linearly at the favourable and unfavourable ends. A detection with S/N < 2 in the
relevant aperture is scored by its 2 sigma upper limit on the favourable side only (so it can give EXCLUDED only if
the 2 sigma ceiling after the most favourable conversion is < 0.0853).

## Interpretation clause (fixed now, both implications reported, no choice made between them)
If a source places M_hot(<100 kpc) below the falsifier:
 (R1) CFG746's declared falsifier fires: the selector C = k M_hot fails as the C3 (early-type shortfall) explanation.
 (R2) The measurement is also what CFG581 expects (gas this massive cools in 0.35-4.2 Gyr) and so does NOT by itself
      say anything about the cold energy; it removes only the hot-gas route to the early-type shortfall (CFG580-582 then
      leave it a limit of the law). R1 and R2 are not alternatives: the sealed falsifier is R1; R2 explains why the gas
      might be absent. If the gas IS absent, nothing here says which of "selector wrong" or "gas cooled/ejected, selector
      tracks a different state variable" is correct; the selector as sealed ties retention to MEASURED hot gas now.
If a source finds M_hot at or above the band: selector survives its sealed test at that class; this is not a mechanism.

## Does any source measure the SAME class as the KiDS early-type excess?
KiDS class (CFG531 README): isolated (f30) quiescent lenses, log M* weighted 10.72 (95th percentile 10.95), inner
bins 52-98 kpc. Each source gets a row: SAME-CLASS YES / PARTIAL / NO (isolated? quiescent? 10.5-11.0?).

## Trial count
One trial per source whose numbers I read. No source is dropped after reading its numbers; sources I decide not to read
are listed with the reason before they are read. Planned reading list (fixed before reading): the eROSITA CGM series
(Zhang et al.), ACT x DESI/WISE tSZ papers (Liu et al. 2502.08850; 2508.09514), kSZ x DESI papers (incl. 2604.19745), the
Planck/ROSAT isolated-galaxy hot-halo papers (Bregman et al.), a Chandra/XMM early-type survey, plus whatever the searches
turn up in 2022-2026 with log M* ~ 10.5-11.2. Cap ~ 8 sources.
