# CFG441 FROZEN CRITERIA: old tidal dwarf galaxies selected by tidal origin

Frozen 2026-10-06, before any script, any literature table read in detail, or any result number of this lane exists.
Standing: kappa = 1/2 is FITTED. Both a0 footings (canonical 9.3603e-11, alt 1.1312e-10 m/s^2) are run everywhere.
No dark-matter particle is added; the framework's cold-fluid mass is still required wherever the law needs it.

## The fork
The settling working model (WORKING_MODEL_SETTLED_PHANTOM_2026-10-06.md) says a TDG has the law's target but no
cold-fluid catchment, so it is Newtonian. Young TDGs (CFG7 FG041) are Newtonian but have turned < 1 orbit. CFG391
found satellite-plane members carry the full law boost. Old TDGs, selected by tidal origin, decide: are they
Newtonian (settling) or boosted (law)?

## Prior knowledge disclosed (before freezing)
- The CFG7 young sample (Lelli+2015, 6 TDGs) and its numbers: Newton chi^2 1.09 for 6; law+EFE worse by +5.2..+12.0.
- NGC 1052-DF2/DF4 were scored by CFG7 FG001 (Newton 0.0 / 0.8 sigma; law+EFE 3.0 / 1.5 sigma).
- From general knowledge (not yet read in detail): Duc+2014 NGC 5557 old TDG candidates; Kaviraj+2012 photometric
  TDG candidates; Duc+2007 VCC 2062. I do not recall published kinematics for the NGC 5557 or Kaviraj objects.

## Sample rules (applied object by object, logged in candidates.csv with the reason for every inclusion/exclusion)
S0 Tidal origin (required): independent published evidence that the object formed from material stripped in a
   tidal interaction: location inside an identified tidal tail/shell/stream of a host or merger remnant, AND at least
   one of (a) gas/stellar metallicity well above the mass-metallicity relation (>= 0.3 dex or stated by authors as
   TDG-like), (b) kinematic continuity with the tidal debris, (c) an interaction model reproducing it. Objects proposed
   as TDGs only because of a satellite plane, or only from metallicity without a host debris feature, are excluded.
   Collision-debris objects (e.g. the NGC 1052 "bullet dwarf" trail, DF2/DF4) are NOT tidal by this rule: stratum C,
   reported, never in the verdict.
S1 Age (required): published evidence that the tidal formation epoch is >= 1 Gyr ago: dated interaction (merger/shell
   age from stellar populations or N-body model) or the TDG's own stellar-population age of the tidally formed stars.
   The adopted age t_form is the published central value; if only a range is given, its LOWER end.
S2 Kinematic quality (required): either
   (rot) a resolved rotation measurement (HI, H-alpha or stellar) with V_rot and its error, inclination i >= 30 deg
         (or an authors' inclination-independent V_circ), and an outer radius R_out; or
   (disp) a line-of-sight dispersion sigma with error from >= 5 discrete tracers or integrated-light spectroscopy,
         with fractional error <= 50%, and a half-light radius R_e.
   Plus a baryonic mass M_bar = M_star + M_gas (atomic incl. He factor as published, + molecular if measured) with an
   error (if no error is published: 0.15 dex on M_star, 10% on M_HI, adopted and disclosed).
S3 Equilibrium (required): t_form / t_orb >= 1, with t_orb = 2 pi R / V_c at the measured radius
   (rot: R = R_out, V_c = V_circ; disp: R = r_1/2 = (4/3) R_e, V_c = sqrt(3) sigma).
Tiers: A = passes S0-S3 (the verdict sample). B = passes S0 and S2 but fails S1 or S3 (reported only).
C = collision debris (reported only). The CFG7 young six are Tier B by construction and are the control set.

## Observable and statistic (as CFG7)
- rot: V_obs = V_circ at R_out (asymmetric-drift corrected as published); M_enc = M_bar (all baryons within R_out,
  unless the authors give enclosed mass).
- disp: V_obs = sqrt(3) sigma at r = (4/3) R_e (Wolf+2010 estimator); M_enc = M_bar / 2.
- Newton: V_N = sqrt(G M_enc / R).
- Law: nu_mono from campaign_fresh_gravity/CFG4_common.py, a_i per the CFG7 / Famaey-McGaugh eq. 60 1-D EFE form
  a_i = gNi nu((gNi+gNe)/a0) + gNe[nu((gNi+gNe)/a0) - nu(gNe/a0)], gNe = G M_host / D_p^2. M_host = published host
  dynamical/stellar mass if given, else 0.6 L_K (as CFG7); D_p = projected distance. Also the isolated law (gNe = 0).
  P2 reported as a secondary kernel.
- Prediction errors propagated from M_bar and R as CFG7. chi^2 = sum (V_obs - V_pred)^2 / (e_obs^2 + e_pred^2).
- Delta chi^2 = chi^2_law - chi^2_Newton, law = law+EFE at the nominal host mass (factor 1); isolated if no host.

## Verdicts (Tier A only; nu_mono; must hold on BOTH footings)
- SETTLING SUPPORTED (old TDGs Newtonian): Delta chi^2 > +9.
- LAW SUPPORTED (old TDGs boosted): Delta chi^2 < -9.
- NON-DISCRIMINATING: otherwise, or N_A < 3 (then no verdict is computed on Tier A; the lane reports which
  observations would supply the missing objects).
- Robustness (reported): the host-mass factor in {0.5, 2} least favourable to the verdict reached; a 10% equilibrium
  systematic on V_obs. A verdict that flips under either is labelled FRAGILE (verdict itself unchanged).

## Controls
- C1: reproduce CFG7's young-TDG Newton chi^2 = 1.09 (6 objects) within 0.01 from real_research/data/tidal_dwarfs/
  lelli2015_tdg.csv with this lane's code, and CFG7's nu_mono most-favourable-host chi^2_EFE (canonical 10.55, alt
  13.08) within 0.05.
- C2: the nu_mono import is the committed one (nu_mono(1) agrees with CFG4_common to 1e-12; deep limit
  nu*sqrt(y) -> 1 within 2% at y = 1e-4).
- MUTATE (MUTATE=1, outputs suffixed _MUTATE): V_obs replaced by V_N for every object in the analysis set. The analysis
  set is Tier A if N_A >= 3, else Tier A + Tier B + the CFG7 control six (pipeline test, N rule suspended). It must
  return SETTLING SUPPORTED on both footings; the script exits 1 when it does (expected failure).
- Main run exits 0 iff C1 and C2 pass.

Departures from these rules, if any, are disclosed in README.md; failed controls are kept as they fell.
