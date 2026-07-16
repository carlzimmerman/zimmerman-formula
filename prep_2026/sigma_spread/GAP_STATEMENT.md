# GAP STATEMENT — Non-Adiabatic Relational Sigma-Spread (Cluster Members)

**Lane F verdict (2026-07-16): NO-GO for any confirmatory firing on 2026 data. This document is the
gap statement + pre-registerable estimator spec so the test is ready the day the data lands.**

Firewall: any touch of real data before the reopen conditions below are met is EXPLORATORY ONLY —
it can neither support nor kill the framework. This is not caution theater: the pre-derived power on
the in-hand carriers is 0.1–0.4 sigma median (best corner 0.36), so a "detection" or "null" at that
power is noise reified either way.

---

## 1. The observable (frozen)

MI (the de Sitter–Unruh modified-inertia framework, own interpolation nu(y)=sqrt(1+1/y),
mu_fw(x)=(sqrt(1+4x^2)−1)/(2x)) modifies each cluster member's inertia by its OWN trajectory
history: the EFE strength entering the inertia argument is a_ext·theta(omega_ex/omega_in)
(Milgrom 2022, arXiv:2208.07073v3, Eq 34), a FUNCTION of the member's infall phase. Members at the
SAME cluster-centric radius (matched momentary a_ext) but different orbit shapes therefore carry
DIFFERENT effective velocity-dispersion boosts. Any modified-gravity realization (one shared field)
responds only to the momentary a_ext — identical boost for all such members, for ANY a0.

- **MI prediction:** relational sigma-spread across infall phase at matched a_ext.
- **MG prediction: exactly zero.** No a0 retune manufactures a spread MG structurally lacks.
  MG-impossible signature; no field theory can fake it.
- **Sign (theta-robust):** theta decreasing ⇒ deep plungers are LESS boosted than near-circular
  members at the same radius. Always.
- **Magnitude (theta-form UNVERIFIED):** only theta(1)=1, decreasing, theta(0)~few are fixed.

## 2. Re-derived prediction (not taken on faith) — both footings

Re-derived from the committed sources
`zimmerman-formula/real_research/reviews/member_MI_nonadiabatic_plunge.py` (STEP 3b/4),
`member_MI_genuine_dynamics.py`, `member_MI_adversarial_check.py`,
`sigma_spread_survey_forecast.py`, by `./rederive_spread_and_power.py` (exit 0, output in
`rederive_spread_and_power.out`). Fiducial carrier: a_in=0.3·(9.36e-11), a_ext=2.0·(9.36e-11)
m/s² fixed physically; infall phases y=omega_ex/omega_in in {0.05, 0.5, 1.0, 1.5}; Milgrom's three
verified example theta forms.

| footing | a0 (m/s²) | sigma-spread band |
|---|---|---|
| canonical rho_DE / cH_Lambda / Z | 9.36e-11 | **6.2% – 11.8%** |
| alt rho_total / cH0 | 1.13e-10 | **7.5% – 14.1%** |

Both-footing envelope 6.2–14.1%, consistent with the banked 6–13% (the corpus band was quoted on
the canonical footing; the alt footing shifts it up ~20%, it does not flip anything — the footing
fork is NOT a wall for this observable, the MG null is zero on both). The 6–13% claim REPRODUCES.

## 3. The exact data gap (quantified)

Estimator power (variance-excess statistic, re-derived in `rederive_spread_and_power.py`):
z ≈ (s·p)² / (eps_eff²·sqrt(2/N)), with s = true spread, p ≈ 0.6 realistic infall-phase
classification purity, eps_eff = sqrt(eps_meas² + eps_FJ²) the per-carrier effective sigma scatter.

**In hand (2026): N = 23 carriers** (diffuse/LSB cluster members with resolved internal sigma,
matched-a_ext bins, caustic infall tags) at eps_meas ≈ 0.25, FJ intrinsic floor ≈ 0.15
⇒ **z ≈ 0.05–0.24** (0.1–0.4 across the Lane-F purity/eps corners; best corner 0.36). NO-GO.

**Needed for 3 sigma** (from the same arithmetic, exit-0):

| tier | eps_meas | eps_FJ | N(3σ), s=0.13 | N(3σ), s=0.09 | N(3σ), s=0.06 |
|---|---|---|---|---|---|
| today (Keck/VLT slit, DESI-grade) | 0.25 | 0.15 | ~3,500 | ~15,000 | ~77,000 |
| ELT tier | 0.10 | 0.15 | ~510 | ~2,200 | ~11,000 |
| ELT tier + FJ floor demonstrated ≤0.10 | 0.10 | 0.10 | ~200 | ~850 | ~4,300 |

The gap is therefore **two multiplicative factors, not one**: (a) carrier count — 23 vs 10²–10³
needed; (b) per-carrier precision — the test only becomes affordable at a ≤10% carrier-sigma tier,
AND only if the intrinsic Faber–Jackson scatter of a homogeneous cluster-dwarf sample floors at
≤0.10–0.15 (otherwise no instrument tier rescues it). Carrier counts alone (even 4MOST-CHANCES's
>1000 members/cluster) do not close the gap at today's eps: most survey members are redshifts,
not resolved internal dispersions of LSB carriers.

## 4. Which named future release closes it, and when

- **DESI DR3 (~2028): does NOT close it.** DR3 multiplies redshifts and caustic/infall tagging
  quality (better p, better matched-a_ext bins, bigger target pool via the dwarf VAC successor),
  but DESI fiber spectra do not deliver ≤10% internal sigmas for LSB dwarfs (sigma ~ 10–30 km/s at
  R~3000–5000 on low-SB targets). DR3's role: **carrier-list and phase-tag upgrade only.**
- **4MOST-CHANCES (2028–2031): closes the COUNT axis, not the precision axis.** 150 clusters,
  ~300k spectra, >1000 members/cluster to 5·r200 — the matched-a_ext, phase-spanning carrier pool
  stops being the limit. Same resolution class as DESI for internal sigma, so eps_meas stays ~0.2+.
  Also the venue for the **FJ-floor measurement** (reopen condition 2) — a homogeneous
  cluster-dwarf sample large enough to measure whether intrinsic sigma scatter floors at ≤0.15.
- **WEAVE-WWFCS (2027–2029):** same role as CHANCES at z~0.05, 16–20 clusters; earliest source of
  the FJ-floor answer.
- **Euclid spectroscopy: does NOT contribute.** Slitless NISP (R~450, emission-line redshifts)
  cannot measure internal stellar dispersions of quiescent LSB dwarfs at all. Euclid's role is
  photometric carrier discovery (LSB structural parameters) only.
- **ELT-HARMONI (~2032): the release that actually closes it.** IFU sigma at ≤10% per LSB carrier.
  With CHANCES/WEAVE-built target lists of ~200–900 phase-tagged matched-a_ext carriers, 3-sigma
  becomes reachable in a plausible allocation (~10²–10³ carriers at eps_meas=0.10, table above).

**Earliest honest confirmatory window: ~2032–2034 (ELT tier on CHANCES/WEAVE-selected carriers),
provided the FJ floor comes in at ≤0.15 (measurable 2028–2031).** If the FJ floor comes in above
~0.2, the observable stays MG-impossible in principle but undetectable at any listed tier — that
result would itself be worth banking.

## 5. What is GO now (free, required either way)

1. **Pre-register the frozen estimator + cuts (Section 6)** — before any collaboration can peek.
2. **Build the ELT target list now:** cross-match the DESI DR1 647k-dwarf VAC LSB tail against
   HeCS-omnibus/gfinder clusters with public caustic infall tags. Output: per-cluster carrier
   lists with (R_proj, v_los, caustic phase tag, surface brightness, size) — the exposure-time
   inputs HARMONI proposals will need. (Building a list is not a firing; no sigma is touched.)

## 6. Pre-registered estimator specification (frozen 2026-07-16)

**E1. Carrier definition.** Diffuse/LSB cluster members (the low-omega_in population that reaches
omega_ex/omega_in ~ O(1)): mu_0,r fainter than 24 mag/arcsec², R_e ≥ 1 kpc, spectroscopic member of
a cluster with a published caustic profile, resolved internal sigma with quoted error ≤ the tier's
eps_meas.

**E2. Matched-a_ext binning.** Bin carriers by cluster-centric a_ext(R) computed from the cluster's
caustic mass profile (NOT from R_proj alone; deproject statistically). Bins of width ≤0.3 dex in
a_ext. The test lives strictly WITHIN bins.

**E3. Infall-phase tag.** Two-class tag per carrier from projected phase space (R_proj/r200,
(v_los−v_cl)/sigma_cl) against the caustic pattern: "settled/near-circular" (y→0 proxy) vs
"infalling/plunging" (y~O(1) proxy). Classification purity p estimated per cluster from the same
mock suite used for the DS cut calibration; p enters the likelihood, never a post-hoc excuse.

**E4. Statistic.** Within each a_ext bin: (i) SIGN statistic — mean sigma residual (from the bin's
carrier FJ relation) of plungers minus settled, prediction NEGATIVE (plungers less boosted),
theta-robust; (ii) SPREAD statistic — excess variance of FJ residuals over eps_eff², prediction
(s·p)² with s in the Section-2 band, MG prediction exactly 0 for both. Combine bins by inverse
variance. Report both footings.

**E5. MANDATORY substructure cut (the 28% fake-rate cut).** Apply a Dressler–Shectman test per
cluster; excise carriers in DS-significant substructure (local-deviation delta above the 99th
percentile of shuffled mocks) before E4. Pre-derived result (Lane F): WITHOUT this cut, a 3-sigma
"detection" arises 28% of the time under true MG, because infalling substructure carries correlated
sigma offsets that masquerade as phase-dependent spread. No DS cut ⇒ no valid firing. Period.

**E6. Confound separator (CDM/tidal heating).** Tidal heating grows TOWARD pericenter and persists
after passage (hysteresis); the MI excess grows OUTWARD into the low-g zone and vanishes at
virialization (no hysteresis). Pre-registered discriminant: fit the radial trend of the spread; MI
requires it increasing with R within 0.5–2 r200 and consistent with zero in the virialized core.

**E7. Decision rule (pre-registered).** Confirmatory firing permitted only when the pre-derived
power at the in-hand (N, eps_meas, eps_FJ, p) reaches ≥3 sigma at s=0.09 (band midpoint). Kill
condition: sign statistic significantly POSITIVE (plungers more boosted) at ≥3 sigma — that
falsifies the theta-decreasing structure on its own terms. Support condition: negative sign AND
spread in the 6.2–14.1% envelope AND E6 radial trend. A zero spread at ≥3 sigma power kills the
non-adiabatic relational channel (not the framework; the ellipsoid-anisotropy SIGN observable is
independent).

## 7. Reopen conditions (verbatim from Lane F, now with the arithmetic attached)

1. A ≤10% carrier-sigma instrument tier exists (ELT-HARMONI, ~2032), **or**
2. a homogeneous cluster-dwarf sample demonstrates an FJ floor at or below 0.15
   (WEAVE-WWFCS / 4MOST-CHANCES, 2028–2031).

Until then: target-list building and estimator pre-registration only. Anything else touching real
sigma data is exploratory, firewalled, and cannot support or kill.

---
*Verification: every number above is produced by `./rederive_spread_and_power.py` (exit 0; output
committed alongside as `rederive_spread_and_power.out`). Sources re-derived, not cited on faith:
`real_research/reviews/member_MI_nonadiabatic_plunge.py`, `member_MI_genuine_dynamics.py`,
`member_MI_adversarial_check.py`, `sigma_spread_survey_forecast.py` (zimmerman-formula, read-only).*
