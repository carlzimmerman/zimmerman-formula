# CFG391 FROZEN CRITERIA: satellite-plane members vs non-members (MW VPOS, M31 GPoA)

Frozen 2026-10-06 before any CFG391 script exists and before any CFG391 offset number exists. The only
numbers known at freezing are (a) the published plane normals and membership lists read from the papers
(inputs, listed below with their location) and (b) the exploratory session-06 result
(ai_slop/crispy_fried_chicken_council_on_gravity/session06_calcs: Delta +0.034 +- 0.098, recalled normal).

Standing: kappa = 1/2 is FITTED, not derived. Both a0 footings are run: 9.3603e-11 and 1.1312e-10 m/s^2.
No dark-matter particle is added; the framework's cold-fluid mass is still required. A verdict here is about
one working model (settling), not about the framework vs LCDM.

## Hypothesis
H_TDG: the VPOS (MW) and the Great Plane of Andromeda (GPoA) formed from tidal debris, so their members
are tidal dwarfs. Under the settling working model (CFG7 tidal-dwarf section: no catchment, so no settled
cold fluid) tidal dwarfs should be near-Newtonian. Then members sit BELOW non-members in sigma relative to
the law, by up to 0.5 log10 nu (the full law boost).

## Inputs (published, read from the papers; see FETCH_LOG.md)
- VPOSnew normal (l, b) = (164.0, -6.9) deg: minor axis of the overall MW satellite system (Pawlowski 2015
  MNRAS 453, 1047), as quoted in Pawlowski & Kroupa 2020 (MNRAS 491, 3042; arXiv:1911.05081) Sect. 2.3,
  itemized list after Table 4. PRIMARY normal (it is fitted to the full satellite set incl. faint ones).
- VPOSclass normal (157.3, -12.7): PK20 same list and Sect. 2.3 text (Metz et al. 2007), 11 classicals.
- DoS normal (156.4, -2.2): Pawlowski, Pflamm-Altenburg & Kroupa 2012 (MNRAS 423, 1109; arXiv:1204.5176)
  Table 1 ("Directions of normal-vectors", row "DoS", 24 satellites, Kroupa et al. 2010).
- Mean orbital pole of the 7 most concentrated poles, Combined PMs: (179.5, -9.0), PK20 Table 4.
- PK20 published classical membership (Combined sample, Sect. 2.3.3): co-orbiting cluster of 7 = LMC, SMC,
  Draco, Ursa Minor, Carina, Fornax, Leo II; Sculptor counter-orbiting in the same plane (member);
  Sagittarius, Sextans, Leo I NOT associated. PK20 Table 3 gives each classical's pole (l_pole, b_pole, Delta_pole).
- GPoA membership: Ibata et al. 2013 (Nature 493, 62; arXiv:1301.0446) Supplementary Information Sect. 2
  (arXiv PDF p. 17): 15 planar satellites = 13 co-rotating (And I, III, IX, XI, XII, XIV, XVI, XVII, XXV,
  XXVI, Cas II, NGC 147, NGC 185) + And XIII, And XXVII (planar, not co-rotating). "May plausibly be
  associated": NGC 205, LGS 3, IC 1613 (outside the PAndAS homogeneous sample).
- The recalled exploratory normal (169.3, -2.8) is NOT in PPK12 or PK20; it is used only for control C2.

## Data and offset (same estimator as AUDIT_UFD, isolated law)
- MW: real_research/data/dsph/lvd_dwarf_mw.csv (LVD, Pace 2024). M31: real_research/data/dsph/lvd_dwarf_m31.csv;
  collins2013_m31_dsph.tsv used as an alternative sigma source (sensitivity S4).
- Offset = log10(sigma_obs / sigma_law), sigma_law^2 = g r / 3 at r = 4/3 r_half (circularised r_half_sph,
  else r_half), M_b = 2 L_V + 1.33 M_HI, half the mass inside r, g = g_N nu(g_N/a0), nu = 1/(1 - exp(-sqrt y)).
  Isolated law for both hosts (no external field; M31's field is noted as a caveat, as AUDIT_UFD does for MW).
- Objects with a sigma upper limit are excluded from the primary (as in session 06); sensitivity S3 includes
  them at the limit value.
- Populations: UFD (M_V > -7.7) and classical (M_V <= -7.7). LMC, SMC excluded (MW). M32 excluded (compact
  elliptical, central sigma; inside Ibata's 2.5 deg mask). Each host x population has its own median
  subtracted, then rows are pooled.
- MW selection as session 06: sigma, r_half and full phase space (ra, dec, distance, vlos, pmra, pmdec) present;
  UFDs also need a host distance.

## MW membership
- Orbital pole L = r x v in astropy Galactocentric defaults; 300 MC draws over quoted errors (seed 41,
  same fallbacks as session 06). Normal direction n = (cos b cos l, cos b sin l, sin b).
- D1 (PRIMARY): VPOSnew normal, member if >= 50% of draws have |L.n| > cos(theta_cut), theta_cut = 30 deg.
  Robustness: theta_cut = 20 and 40 deg. Co-orbiting-only (L.n > cos theta_cut) reported for each cut.
- D2: other published normals (VPOSclass, DoS, PK20 mean pole k=7) at 30 deg, either sense.
- D3: PK20 published classical list (classicals only; members Draco, UMi, Carina, Fornax, Leo II, Sculptor;
  non-members Sextans, Leo I, Sagittarius if present). No published per-object list for the UFDs exists in
  these papers, so D3 is classical-only and expected to be low-N.
- MW-primary verdict = D1 at 30 deg. It is called ROBUST only if D1 at 20, 30, 40 deg all give the same verdict.

## M31 membership
- G1 (PRIMARY): the 15 Ibata planar satellites are members; NGC 205, LGS 3, IC 1613 excluded from the
  primary (ambiguous); every other M31 LVD object with a measured sigma is a non-member.
- G2: the 13 co-rotating only are members (And XIII, XXVII dropped from both groups).
- G3: the 15 + the 3 "plausibly associated" are members.
- S3 (upper limits included at the limit), S4 (Collins 2013 sigma replacing LVD sigma where Collins has a
  non-zero sigV; sigV = 0 rows treated as upper limits and dropped).

## Statistic and verdict (per footing; MW, M31 and COMBINED separately)
- Delta = median(member offsets) - median(non-member offsets) after the population-median subtraction.
- sigma_Delta = std of Delta over 2000 bootstrap resamples of objects (seed 43; resamples with an empty group skipped).
- TDG-ORIGIN SUPPORTED if Delta < -0.2 dex AND Delta/sigma_Delta < -3.
- DISFAVOURED if Delta - 2 sigma_Delta > -0.2 (members cannot be 0.2 dex below non-members at 2 sigma).
- NON-DISCRIMINATING otherwise.
- COMBINED = MW D1 (30 deg) rows + M31 G1 rows pooled (each host x population median-subtracted).
- Reported alongside (not part of the verdict): the predicted Newtonian shift for the members,
  Delta_pred = -median(0.5 log10 nu) over members, and the retained-boost fraction f = 1 - Delta/Delta_pred.
  If |Delta_pred| < 0.2 the -0.2 threshold cannot be reached even if H_TDG were exactly true; that host is
  then flagged UNDERPOWERED in the README (the verdict text stands as computed).

## Controls (kept as they fall)
- C1 permutation null: 2000 random relabellings of membership (same group sizes, seed 47) per primary test;
  report the median permuted Delta (must be within 0.03 of 0) and the one-sided p = P(Delta_perm <= Delta_obs).
- C2 fidelity: the session-06 configuration (normal 169.3, -2.8; 30 deg; a0 9.36e-11) must reproduce
  Delta = +0.034 +- 0.098 (any sense) to within 0.005 in Delta and 0.01 in sigma.
- C3 pole check: for the classicals in the MW sample (LMC/SMC excluded), our median MC pole must lie within
  max(3 Delta_pole, 10 deg) of PK20 Table 3 (l_pole, b_pole) for at least 7 of the 9 (or all but 2 present).
- MUTATE (separate run, outputs suffixed _MUTATE): member offsets replaced by offset - 0.5 log10 nu (members
  made Newtonian) for the MW-primary, M31-primary and COMBINED tests. It must return TDG-ORIGIN SUPPORTED on
  all three at the canonical footing; the MUTATE run exits 1 when it does (the planted signal is seen), 0 otherwise
  (a failed control, kept and reported).

## Implication rule (written now)
- If MW and M31 primaries are both DISFAVOURED: members are not Newtonian-poor, so the fork reads: EITHER the
  planes are not tidal-dwarf planes, OR old tidal dwarfs are not Newtonian (the settling model's "no catchment"
  premise fails for them). This test cannot pick between those two branches.
- If either is SUPPORTED: a host-level hint for TDG planes + Newtonian TDGs (a mass deficit in plane members);
  needs the permutation p and MUTATE to stand.
- NON-DISCRIMINATING: no statement.
