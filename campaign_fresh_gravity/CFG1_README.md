# CFG1: the evidence audit

Campaign "fresh gravity", first wave, 2026-09-27. One script, `CFG1_evidence_audit.py`, run from the repository root; its
`.out` and `_results.json` hold every number quoted below, and the `_MUTATE` files hold the control that must fail.
Nothing outside the `CFG1_*` files was edited. κ = ½ is fitted (Z = κ-form = 5.7888). Both a₀ footings are carried
(9.3603e-11 and 1.1312e-10 m/s²). Nothing here says the theory is closed.

## What this lane does

It builds the campaign's evidence ledger in three parts.
- **Part A**: every result in the charter's table and on the answer page's scorecard. For each one it records:
  - how it was measured (instrument, pipeline, citations);
  - the model assumptions built into the pipeline;
  - a quantified shift: how far a framework-consistent but defensible treatment could move it, with the same shift
    applied to ΛCDM;
  - a class.
- **Own results**: the framework's own empirical findings (rule 0), audited the same way.
- **Part B**: the record's own computational approximations, the verdicts they touched, and their status.

It ends with the verdicts that are not established and the requirements list.

### The class rule (declared before the recorded runs)

- **CONTESTED**: published analyses (or the record's own independent analyses) of the same observable disagree by more
  than their errors.
- **Otherwise**, the rule compares a stake with a budget:
  - **The stake.** For a recorded failure, it is the data shift that would rescue the framework's most favourable
    variant: either construction (M\* or the chain), either footing. For a pass, it is the shift that would break the
    least favourable variant. If a failure's best variant already passes, the stake is that variant's margin.
  - **The budget.** The documented data-side systematics, combined in quadrature. The aligned corner, where every
    systematic sits at its edge in the same direction, is printed beside it.
- **SOFT** if the budget reaches the stake; **MODEL-INDEPENDENT** otherwise.

**Fairness.** Every shift is applied to the data through one function, so the framework and ΛCDM see the same shifted
data. ΛCDM's pull at the shift the framework needs is printed. Where ΛCDM's number is a per-object halo fit, no pull is
printed: a fitted halo simply refits.

## Headline

- **Part A: 33 results.** 14 MODEL-INDEPENDENT, 11 SOFT, 8 CONTESTED.
- **Own results: 8.** 2 MODEL-INDEPENDENT, 4 SOFT, 2 CONTESTED.
- **Part B:** 18 equipment items; 12 past verdicts are not established.

Three findings change the picture the charter drew:
1. **Two of the three external-field failures are model-independent, not soft.** The LV-dwarf and Coma-UDG results
   survive every documented data systematic. Only the cluster-infall slope is soft, and only for the gentlest EFE form.
2. **The X-COP failure that empties the dark sector's window (FP16) is soft.** On the canonical footing, the
   PM-calibrated turned-around-web cell already sits on the gate (M_dyn/M_HSE = 1.1997). The least favourable cell needs
   a hydrostatic bias of 0.14, inside the published range.
3. **The CMB-lensing failure holds for the action as written but is open for the reading the chain has adopted.** The
   committed FP22 (bfe9a2fe5) excludes the all-matter reading in every cell. The chain has since adopted the baryons-only
   reading (08548fc85). There the linear base passes Planck and ACT and the halofit base fails ACT, so the verdict waits
   on the nonlinear phantom.

## Controls and MUTATE

All three controls re-execute committed code read-only (file writes refused, output paths neutralised) and reproduce
the committed numbers exactly.

| Check | What it reproduces | Result |
|---|---|---|
| K1 | FP18's pincer, from FP18's own `main()` in its own module namespace | T_nominal 101.967, T_profiled 7.4974, nuisances: deviation 0 |
| K2 | FP20's projector audit, from its own source through its V section | 88 projector rows, max deviation 0.0 pp (esd_of_M −58.56% at 35 kpc on the SIS) |
| K3 | XR26's CMB-lensing pipeline (CAMB, CLASS, FP13's yardstick, Limber, Planck MV bands) | amplitude 1.149178 / 2.134361, f\* 0.618 / 0.178, whole A(f) table: deviation 0 |
| K4 | the sources | 47 committed sources, all tracked and unmodified (sha256 in the JSON) |
| K5 | the commits | 68 cited commits, all exist |
| K6 | FP0's footings and Z | reproduced |
| F1 | fairness: both models scored on identical shifted data | pass (29 scorings) |
| F2 | every SOFT row has a quantified budget and ΛCDM's standing | pass |
| F3 | every row has a class, a measurement, assumptions and a citation | pass |

**MUTATE** applies every systematic to the framework's comparison only, the special pleading charter rule 3 forbids. F1
must fail, and it does: 19 of 29 scorings are asymmetric, rc = 1. Everything else passes. The main run is 9/9, rc = 0,
81 s.

## Part A: the ledger

Classes are shown in capitals. "Stake" and "budget" follow the rule above; the full numbers are in the `.out`.

### Solar System and wide binaries

**A01. Cassini and the ephemeris quadrupole: MODEL-INDEPENDENT.**
- Measured: Cassini gives γ − 1 = (2.1 ± 2.3)e-5. The ephemerides give Q2 = (1.6 ± 1.8)e-27 s⁻², with a 2σ ceiling of
  5.2e-27.
- The framework: the strict law predicts 4.0–5.7× the ceiling. Rescuing it needs a shift of 1.6e-26 s⁻². The published
  analyses differ by about 2.4e-27.
- It passes only with the screening length ξ, which is a knob (FP17). GR predicts Q2 = 0.

**A02. Gaia DR3 wide binaries: CONTESTED.**
- Published boosts run from about 1.0 (Banik et al. 2024; Pittordis & Sutherland 2023) to about 1.4 (Chae 2023, 2024;
  Hernandez 2023). The analyses differ in their hidden-triple and error models.
- The chain predicts a ceiling of 1.0725 (canonical) / 1.0900 (alt) at ξ's floor (XR22). DR4 can kill it only from
  above.

### Galaxies

**A03a. The RAR's form and tightness: MODEL-INDEPENDENT.** The scatter is 0.108 dex on 175 SPARC galaxies. M\*'s carrier
moves it by at most 1.2e-4 dex (L391).

**A03b. The RAR's a₀ normalisation: SOFT.** McGaugh et al. 2016 find g† = 1.20 ± 0.02 ± 0.24 (sys). The ±0.24 M/L
systematic covers both footings. κ stays fitted.

**A04. The high-z RAR/BTFR and a₀(z): CONTESTED.**
- MUSE-DARK III measures a rise, a₁ = +1.59 ± 0.105. McGaugh et al. 2024 see no evolution. A ΛCDM simulation
  (Magneticum) produces an apparent ×2.3–3 rise.
- Flattening MUSE would need stellar masses 0.2–0.45 dex heavier, which its authors do not support.
- M\*'s flat-a₀ flagship at z = 2.5 is not established (XR17: +0.106 to +0.126 dex).

**A17a. The Milky Way's outer decline: CONTESTED.** The published DR3 curves disagree: the outer power-law index is −0.47
(Jiao et al.) and −0.56 (Ou et al.), against −0.19 to −0.40 in XR29's fits of the same tables.

**A17b. The Milky Way's stellar mass: MODEL-INDEPENDENT, but marginal.**
- The chain needs M\* = 7.3–8.2e10. McMillan's census gives 5.43 ± 0.57e10.
- The stake is 0.74e10; the spread between census methods is 0.65e10.
- Against Licquia & Newman alone (6.08 ± 1.14e10), the chain sits at 1.1–1.9σ.
- ΛCDM uses the census baryons and pays in halo concentration instead.

### Dwarfs, UDGs and the external field

**A05a. The cluster-infall BTFR slope: SOFT, for the gentlest form only.**
- Measured: +0.0033 ± 0.0304 (ALFALFA α.100 line widths, PSZ2 clusters, N = 314).
- M\*'s scalar-sum form sits at 2.23σ, so the stake is 0.007. The data-side budget is 0.021 (membership cut, deprojection,
  Υ×1.5).
- The subtract form (6.3σ) stays excluded.
- HI stripping lowers member line widths, which biases the measured slope toward an apparent deficit (the framework's
  sign). Correcting for it would move the slope away from the framework, so it adds nothing to the favourable budget.
- ΛCDM's pull at the needed shift is 0.12σ.

**A05b. LV dwarfs, statistic C: MODEL-INDEPENDENT.**
- Measured: +0.080 ± 0.047. The prediction is −0.10 (3.87–4.48σ).
- The stake is 0.087; the budget is 0.039 (the aligned corner 0.055).
- Dropping the ultra-faints (the binary-inflated systems) still leaves 3.15σ. Dropping the 10 nearest (tides) leaves
  3.88σ. Υ×1.5 moves it 0.33σ.
- ΛCDM (slope 0) sits at 1.71σ.

**A05c. Coma UDGs: MODEL-INDEPENDENT.**
- The excess is +0.92–1.01 dex over the EFE-suppressed prediction.
- The stake is 0.79 dex. XR6's own systematic budget is 0.22 dex in quadrature and 0.51 dex at the aligned corner.
- Even with no EFE at all, the UDGs sit +0.40 dex high.

**A05d. Crater II and the M31 dSphs: SOFT.** The literature's radius convention alone moves Crater II from 4.2σ to
0.06–2.5σ; Υ_V moves the M31 dSphs.

**A05e. DF2/DF4: CONTESTED.** The distance is disputed: about 13 Mpc against 22.1 ± 1.2 Mpc (TRGB).

**A05f. Chae's SPARC EFE signal: SOFT.** The environment geometry (catalogued vs group-collapsed) moves D2 by 1.6–1.9σ.

### Lensing and groups

**A06. SLACS strong lensing: CONTESTED.**
- The chain needs an IMF +0.118 ± 0.013 dex above the spectroscopic relation, whose own rms is 0.12 dex. ΛCDM's IMF sits
  +0.02 dex from it.
- But the published IMF methods disagree by more than that: SNELLS vs SLACS differ by 0.26 dex in the chain and 0.30 dex
  in ΛCDM.

**A07a. KiDS inside 0.3 Mpc: MODEL-INDEPENDENT.** FP20 moved the model's inner ΔΣ by up to 59% at 35 kpc without flipping
a deciding verdict. The data-side budget there is about 0.1 dex.

**A07b. KiDS at 0.3–2.6 Mpc: SOFT.**
- B21's own photo-z leakage makes the published signal about 30% high (−0.11 dex).
- For LV-like isolated spirals the profiled shift is −0.48 / −0.54 dex (FP18).
- FP21's isolated late types give A = 2.19 ± 1.46 of the mixed level (undecided; about 2100 lenses would decide).

**A07c. The KiDS–R0 pincer: SOFT.** Face value is T = 102.0 (9.8σ); profiled it is 7.50 (2.3σ). ΛCDM shares it: its
KiDS-fitted halos turn around at 1.85–1.94 Mpc.

**A08. The LG zero-velocity radius: MODEL-INDEPENDENT, but marginal.**
- The chain overshoots by +0.20 dex. With FP18's honest error that is 4.0σ, and 2.9σ once the method systematic is
  added. FP12 had quoted 13.6σ from errors that omit the velocity scatter.
- For M\*'s most favourable cell, the stake is 0.076 dex against a budget of 0.056. The aligned corner, 0.076, just
  reaches the stake.
- ΛCDM's KiDS-calibrated halo is off by 4.2σ at the needed shift.

### Clusters

**A09a. Mass beyond MOND in clusters: MODEL-INDEPENDENT.** η(R500) = 2.33 [1.55–2.80]. Every hydrostatic correction
raises it: 2.48 at b = 0.06, 2.91 at b = 0.2.

**A09b. X-COP against the chain's dark sector (FP16): SOFT.**
- The hydrostatic bias needed ranges from 0.000 (canonical, turned-around web, PM-calibrated) to 0.142 (alt, halo, raw).
  The published range is b ≈ 0.06–0.2 (X-COP's own 6%; weak-lensing calibrations; simulations).
- ΛCDM pays for the same shift: at b = 0.142, its X-COP gas fraction drops to 0.91 of its calibration.

**A09c. The Bullet Cluster's lensing–gas offset: MODEL-INDEPENDENT (8σ).**

**A09d. Harvey's 72 collisions: CONTESTED.** Harvey 2015 bounds σ/m < 0.47 cm²/g; Wittman et al. 2018 find about 2.
M\* is knife-edge (β = +0.096 against +0.10) and uncontrolled.

**A19. Cluster counts: CONTESTED.**
- eRASS1 gives S8 = 0.86 ± 0.01; SPT gives 0.795 ± 0.029.
- The fluid's conversion puts the counts at 0.64–0.81 of ΛCDM: it fits SPT and sits 5–9σ below eRASS1 (XR32, hub
  re-run pending).

### Cosmology

**A10. The CMB primary spectra: MODEL-INDEPENDENT.** The chain moves them by 7.8e-8, against CLASS's own precision of
1.9e-3.

**A11. The CMB lensing amplitude: MODEL-INDEPENDENT on the data side.**
- Planck gives 1.011 ± 0.028 and ACT 1.013 ± 0.023. The two differ by 0.002.
- The chain's verdict depends on its equipment (B01, B04), mapped onto XR26's own A(f):

| Variant | Linear base | Halofit base |
|---|---|---|
| XR26 headline (per-mode, all matter) | 1.149 (+4.9σ) | 2.134 (+40σ) |
| real-space, all matter | 1.036–1.099 | 1.250–1.737 |
| real-space, baryons only | 1.013–1.043 (passes) | 1.081–1.301 |

  FP22's committed Limber-weighted calculation reaches the same verdicts. Its cut factors are 0.52–1.35 (all matter) and
  0.13–0.26 (baryons only); my k-point mapping gives 0.42–0.78 and 0.21–0.47.

**A12a. BAO, P(k) shape and RSD: MODEL-INDEPENDENT.** The background is ΛCDM's (r_d moves by 8e-10). The fluid's
conversion leaves DESI's fσ8 3.5–7.3% low (−2.2σ; XR32, re-run pending).

**A12b. S8: CONTESTED.** KiDS-1000 gives 0.759, KiDS-Legacy 0.815 and Planck 0.832. The conversion gives an inferred
0.766 / 0.752 (XR32).

**A18. Small-scale cosmic shear (R(k) at k ~ 1): SOFT.** M\*'s capped alt value of 1.124 sits 0.076 from the 20% gate,
inside the roughly 10% baryonic-feedback budget. It is a halo-model estimate.

**A13. The Lyman-α forest: SOFT at 10–15%.**
- McDonald et al. 2005 constrain the forest-only linear amplitude to about ±14% after marginalising over the IGM.
- M\*'s switch: DE11b's worst is 0.0046. Correcting the kernel argument multiplies MOND by 2.0–3.2 at z = 2–3 (FP6's own
  kernel), giving an estimated 0.015 against 0.10.
- The fluid's conversion (XR12: 11.3% / 8.0%) sits inside the soft band.

**A14. JWST early galaxies: SOFT.** The required efficiency ε is 1.275 with published Salpeter masses, 0.778 with
Chabrier, and 0.273 after spectroscopic revision. The chain and ΛCDM are identical here (XR23).

**A15a. BBN (Y_P, D/H): MODEL-INDEPENDENT.**

**A15b. Lithium-7: SOFT.** The ×2.95 excess is shared by both models; stellar depletion is about 0.25 dex.

**A16. The GW speed: MODEL-INDEPENDENT.**

### Scorecard rows (ANSWER_AS_IT_STANDS §3), mapped

| Scorecard row | Ledger row | Note |
|---|---|---|
| flat-a₀ flagship | A04, O4 | |
| KiDS on M\* | A07a/b | not established: B02, P2 projector |
| cosmic shear | A18 | B07, B10 |
| forest (switch) | A13 | B05 |
| forest (fluid) | A13 | B06 |
| RAR RC100 | A03a, A04 | |
| S8 / X-COP (not run on M\*) | A12b, A09b | |
| Harvey | A09d | B14 |
| EFE clusters | A05a | |
| EFE dwarfs | A05b | |
| LG R0 | A08, A07c | |
| Coma UDGs | A05c | |

## The framework's own results (rule 0)

**O1. The SN-Ia host-mass step at the a₀ scale: MODEL-INDEPENDENT (the step); the a₀ attribution is untested.**
- The step is −0.050 ± 0.007 mag (6.9σ), from raw SALT2 fits of Pantheon+ (N = 1548). It sits where g_bar crosses a₀
  (log M\* 9.6–10.2 against the step at 10).
- The fixed-mass test finds no acceleration dependence beyond mass (partial +0.030 against −0.170), but it has only 18%
  power (23% alt) against the framework's own model.
- Cross-check with CFG0: CFG0 reads this as "not an acceleration effect", following the 07-20 null. The later power audit
  (87812ee4ec) says "underpowered, not null".

**O2. The environmental null: MODEL-INDEPENDENT.** The ρ_local fork (slope +½) is excluded at 13–34σ on 175 SPARC. The
number comes from EMPIRICAL_TESTS A14; there is no committed `.out`.

**O3. The measured κ: SOFT.**
- 0.465 ± 0.076 (BTFR) and 0.55 ± 0.17 (distance-free, dominated by the bulge M/L). κ = ½ sits 0.46σ and 0.29σ away.
- The two estimators share galaxies. ½ vs 1/(2π) is 2.2σ at forecast grade. κ stays fitted.

**O4. Flat a₀(z): CONTESTED.**
- The registered z ≈ 2.5 test cannot run: 0 of the 2 deep-MOND rotators it needs.
- The on-disk proxy (+0.636 ± 0.054 dex) is not the registered test.
- One object at 0.13 dex gives only 3.8:1 odds (PAPER14 v2). Three at 0.10 dex give 122:1.

**O5. The comet anisotropy (DOI 21966646): SOFT.**
- The spike quadrupole is −0.027 ± 0.039 against a predicted 0.12. It is selection-dominated (the Jupiter-family control
  shows +0.166 ± 0.012) and needs about 3200 spike comets.
- The ν₀ pair collapses once stage76's ν₀ bound applies.

**O6. The directional EFE: CONTESTED.** In the same commit, the n = 16 firing gives Â = +2.95 (p = 0.029) and the n = 25
WALLABY firing gives Â = −1.70 ± 2.12 (p = 0.59). The first did not reproduce.

**O7. The Milky Way's vertical force: SOFT.**
- Full AQUAL matches at +0.2σ, but needs about 30% more stellar mass. Route A's box clears at 1.50σ (p = 0.030).
- The kernel's floor of 78.5 exceeds Bovy & Rix's 68 ± 4.

**O8. The Lyman-α b-cutoff sign: SOFT.** The tension is 1.1–9.0σ statistically but 0.4–0.9σ on the calibration channel.
The sign is robust; the magnitude depends on convention.

## Part B: the record's equipment

| # | Item | Status | Quantified | Verdicts touched |
|---|---|---|---|---|
| B01 | per-mode yardstick vs real-space operator | OPEN | b(real)/b(per-mode) = 0.50–0.91 (H_S), 0.28–0.51 (H_Y) | σ8 passes stand (conservative); forest proxies not established; XR26's lensing magnitude |
| B02 | Abel projection defect | P1 FIXED (7a8c25321); P2 PENDING | P1 SIS −58.6% at 35 kpc; P2 −3% SIS, up to +11.5% NFW, +187% / −123% carriers | FP20b (3924bb8c2): FP15/16/19 no flips; M\*'s KiDS (XR14, DE10, XR9) waits for XR35 |
| B03 | T_EH98 h-units error | PENDING (FP24 in flight) | committed/CLASS at fixed σ8: 0.43, 0.94, 1.29, 1.49 at k = 0.01/0.1/1/10 h/Mpc (reproduces XR23's flag) | FP13's high-z state and A6; XR26's lensing under-stated (1.149 → 1.172, FP22) |
| B04 | all-matter vs baryons-only reading | DECIDED (FP22 bfe9a2fe5; adopted 08548fc85) | the baryons-only reading cuts the matter boost to 0.04–0.06 but the lensing only to 0.17–0.46 | FP7's σ8 fail stands; CMB lensing open in (b); price: a dark–baryon WEP violation |
| B05 | (1+z) kernel argument in the forest PM codes | PENDING (XR34 running) | the MOND term is too weak by 2.0–2.3 (z = 2) and 2.7–3.2 (z = 3) | DE11/DE11b likely survive; L347/L358/L359/L362/DE2 borderline passes open |
| B06 | linear forest proxies vs flux runs | OPEN | the real-space rms field reaches the yield at z ≈ 1–2 | the chain's forest passes; XR12 |
| B07 | halo model / semi-analytic vs PM | OPEN | FP16 over-predicts PM retention by +0.07–0.40; turned-around share 0.12 vs 0.32 at z = 2 | shear pass, FP16 X-COP |
| B08 | frozen-coefficient / WKB stability | OPEN for O(H) rates | XR15 at 1.1–2.8 H; DE13's λ = 241 was an artefact (corrected) | XR15/XR11 magnitudes; DE12 and XR18 stand; XR18b: H_K1 well posed |
| B09 | the web's field omitted in the KiDS models | PENDING | +200 / +600 Δχ² (FP22 D2, upper side) | the chain's KiDS pass |
| B10 | shear gate: one-sided or two-sided | OPEN | two-sided passes only x_c0 ≤ 3.5 | neighbouring cells |
| B11 | B21 covariance reshape | FIXED | the plain reshape has eigenvalue −64 | pre-09-03 χ² |
| B12 | published R0 errors; FP12's fit form | FIXED in FP18 | bootstrap ±0.115, 4–6× the quoted error | FP12's significances |
| B13 | the boost against uniform randoms | FIXED | 0.91/1.15 → 1.00/1.28 | FP21 K6 |
| B14 | Harvey L389: no MUTATE | OPEN | β = 0.096 vs 0.10 | M\*'s Harvey pass |
| B15 | FP16 vs PM retention | OPEN | bias toward a stronger failure | FP16 |
| B16 | first-order leapfrog | FLAGGED | 1.8% at dlna = 0.02 | stage 3 |
| B17 | EFE and DR4 statistic conventions | OPEN (theory forms) | scalar vs subtract, 1–4σ | EFE sizes; DR4 kills only from above |
| B18 | bookkeeping of the own results | OPEN (record-keeping) | stale κ 0.529, "fired once", N ~ 1157, "20:1 from one object" | O-rows restate them |

## Past verdicts that are not established

1. **XR26's CMB-lensing FAIL.** It holds for the action as written. For the adopted baryons-only reading it is open until
   the nonlinear phantom is computed (B01, B03, B04).
2. **The chain's forest passes** (FP9/FP13/FP19). They are linear proxies (B06).
3. **M\*'s KiDS pass on M\*** (XR14), DE10's −37/−34 and XR9's cap. These use the P2 projector (B02); XR35 is in flight.
4. **The chain's KiDS passes.** The web's external field is omitted (B09), and the outer bins carry the leakage (A07b).
5. **M\*'s cosmic-shear pass.** It is a halo-model estimate, inside the feedback budget (B07, B10, A18).
6. **M\*'s Harvey pass.** It has no MUTATE run (B14).
7. **FP16's empty window from X-COP.** The data side is soft (A09b).
8. **The forest verdicts of L347, L358, L359, L362 and DE2.** Their deviations are under-stated by the kernel argument
   (B05).
9. **XR15/XR11 instabilities at O(H) rates.** Their magnitudes are not established (B08).
10. **FP12's R0 significances.** The offsets stand; the significances are overstated (B12).
11. **FP13's high-z state and its A6 systematic.** Both inherit the T_EH98 error (B03).
12. **M\*'s flagship.** It was already marked not established.

## Hypotheses, as they fell

| Hypothesis | Result | Detail |
|---|---|---|
| H1 (the three controls reproduce exactly) | held | |
| H2 (the listed rows are MODEL-INDEPENDENT) | held | |
| H3 (the pincer is soft; the chain's own R0 overshoot is ≥ 2σ) | held | pincer SOFT; overshoot 4.0σ with honest errors |
| H4 (at least two EFE samples are MODEL-INDEPENDENT) | held | dwarfs and UDGs; the cluster slope is SOFT |
| H5 (CMB lensing: baryons-only linear passes, all-matter halofit fails) | held | 1.013–1.043; 1.25–2.13 |
| H6 (X-COP needs a bias inside the published range but above 6%) | **fell** | the most favourable cell needs no bias at all |
| H7 (SLACS is CONTESTED) | held | |
| H8 (DE11b survives the kernel factor) | held | estimate 0.015 |
| H9 (F1 passes in the main run, fails in the MUTATE) | held | |
| H10 (the own results' classes) | held | |

## Disclosures

1. **Prototypes.** Three prototypes of the controls ran in scratch first. One XR26 prototype was stopped so that two jobs
   would not exceed the two-thread cap.
2. **The search agent.** A read-only search agent located the own-results' scripts. Every number from it was re-read at
   source before use.
3. **Development runs.** Three development runs wrote to scratch via `CFG1_OUTDIR`. The first exposed four issues, all
   fixed before the recorded runs; the hypotheses were not changed:
   - `classify` returned MODEL-INDEPENDENT for a zero stake;
   - rule 5 (a failure whose best variant already passes) was missing;
   - A11's budget used the Planck–ACT difference's uncertainty instead of the measured difference;
   - ΛCDM pulls were printed for per-object fits.
4. **Lanes that landed during the work.** FP22, FP20b, XR32, XR18b and XR28 were committed while this lane ran. Their
   committed numbers replaced the in-flight ones, and A19 was added from XR32 before the recorded runs.
5. **In-flight lanes.** XR34, XR35, FP24 and XR24 are cited as pending. The script re-checks their status at run time.
6. **CFG0's inventory.** `CFG0_own_findings_inventory.md` did not exist when this lane finished. The cross-check used
   CFG0's committed-style parameter-reduction output, which agrees on κ and on O1/O2.
7. **Published values not on disk** (Planck/ACT, S8, eRASS1/SPT, the hydrostatic-bias calibrations and others) are cited
   in their rows. None was downloaded.

## Requirements list

### MODEL-INDEPENDENT: reproduce as they stand

| Row | Fact |
|---|---|
| A01 | Newtonian where g ≫ a₀: Q2 ≤ 5.2e-27 s⁻² (2σ) and γ − 1 = (2.1 ± 2.3)e-5 |
| A03a | the RAR's form and tightness (about 0.1 dex on 175 SPARC), deterministic in the baryons |
| A05b | LV dwarfs: statistic C = +0.080 ± 0.047. No host-field suppression of dwarf dispersions at 50–300 kpc, robust to binaries, tides and Υ |
| A05c | Coma UDGs are dynamically hot. No visible EFE suppression at 0.2–2.3 Mpc (+0.92 to +1.01 dex over the suppressed prediction; +0.40 dex even over isolated MOND) |
| A07a | the KiDS isolated-lens ΔΣ inside 0.3 Mpc (Brouwer et al. 2021, four mass bins) |
| A08 | the LG zero-velocity radius R0 = 0.96 (0.91) ± 0.11 Mpc (honest error), plus a 0.05 dex method systematic |
| A09a | clusters need mass beyond MOND on the baryons: η(R500) = 2.33 [1.55–2.80], and hydrostatic corrections only raise it |
| A09c | collisionless lensing mass offset from the gas in mergers (Bullet, 8σ) |
| A10 | the CMB primary spectra: GR + CDM at z ≳ 10 with ω_c ≈ 0.120 and ω_b ≈ 0.0224 |
| A11 | the CMB lensing amplitude: 1.011 ± 0.028 (Planck 8–400) and 1.013 ± 0.023 (ACT DR6) |
| A12a | BAO and the P(k) shape: the ΛCDM background and linear growth to about 1% |
| A15a | standard BBN: Y_P ≈ 0.245–0.247 and D/H ≈ 2.45–2.59e-5 at ω_b = 0.0224 |
| A16 | c_T = c to 1e-15 |
| A17b | the MW's stellar mass, 5.0–6.1 (±0.6–1.1) × 1e10 M☉, together with the 8–19 kpc slope of −1.7 km/s/kpc (marginal) |

### SOFT: the allowed ranges

| Row | Fact |
|---|---|
| A03b | a₀ = 0.94–1.13 × 1e-10 lies inside g† = 1.20 ± 0.24 (sys); κ = ½ stays fitted |
| A05a | the cluster-infall BTFR slope: an EFE deficit no steeper than about −0.078. The gentlest QUMOND form (−0.065) fits; the subtract form (−0.188) does not |
| A05d | Crater II and the M31 dSphs: set by Υ_V and the radius convention |
| A05f | Chae's EFE: 1.0–2.9σ depending on the environment geometry |
| A07b | KiDS beyond 0.3 Mpc: −0.11 dex of leakage; up to about −0.5 dex for LV-like spirals; FP21 A = 2.19 ± 1.46 |
| A07c | the KiDS–R0 pincer: 2.3σ after systematics, shared by ΛCDM |
| A09b | X-COP totals with a hydrostatic bias of 0.06–0.2 (ΛCDM's gas fraction pays the same factor) |
| A13 | small-scale linear power at z = 2–3 within about 10–15% of ΛCDM |
| A14 | early massive galaxies need ε = 0.27–1.27, set by the IMF and spectroscopy |
| A15b | lithium-7: the ×3 excess is shared; depletion is about 0.25 dex |
| A18 | cosmic-shear power at k ~ 1 within the roughly 10% feedback budget |

### CONTESTED: state the prediction

| Row | What to state |
|---|---|
| A02 | wide binaries: γ̂ at the primary field and its ξ dependence (DR4, 2026-12-02) |
| A04 | the z ≈ 2.5 BTFR zero point (flat law 0.00 dex; ΛCDM-native +0.33 dex) |
| A05e | DF2/DF4 at both 13 and 20–22 Mpc |
| A06 | the IMF the construction needs |
| A09d | the fractional drag |
| A12b | S8 (the surveys span 0.76–0.82; Planck gives 0.83) |
| A17a | the MW's curve at 20–27 kpc |
| A19 | cluster counts (eRASS1 and SPT disagree) |

### The framework's own results: to keep

| Row | Class | Fact |
|---|---|---|
| O1 | MODEL-INDEPENDENT | the SN-Ia step, −0.050 ± 0.007 mag at log M\* ≈ 10. Tying it to a₀ needs a fixed-mass acceleration dependence; 80% power needs a 0.142 mag step |
| O2 | MODEL-INDEPENDENT | a₀ does not depend on the ambient density; its source is the cosmic ρ_Λ |
| O3 | SOFT | any construction that ties κ must land inside 0.465 ± 0.076 and 0.55 ± 0.17 |
| O4 | CONTESTED | a₀(z) flat to < 1% for z ≤ 5 on a true Λ; the decisive test needs 3 rotators at ±0.10 dex or 4 at ±0.20 dex at z ≈ 2.5 |
| O5 | SOFT | the comet anisotropy: no constraint yet (it needs original 1/a and about 3000 spike comets) |
| O6 | CONTESTED | the directional EFE: no constraint yet (consistent with zero); a 4–22% dipole needs about 1400–6000 galaxies |
| O7 | SOFT | Σ_dyn(\|z\| < 1.1 kpc) = 68–74 (±4–6) M☉/pc² at R0 with census-compatible baryons, together with v_c(R0) |
| O8 | SOFT | the b-cutoff sign: it must not grow beyond the calibration channel's 0.4–0.9σ |

## Files

- `CFG1_evidence_audit.py`: the script.
- `CFG1_evidence_audit.out` and `CFG1_evidence_audit_results.json`: the main run (rc 0).
- `CFG1_evidence_audit_MUTATE.out` and `CFG1_evidence_audit_results_MUTATE.json`: the MUTATE run (rc 1).
- `CFG1_README.md`: this file.

Run from the repository root, MUTATE first:

```
MUTATE=1 python3 campaign_fresh_gravity/CFG1_evidence_audit.py
python3 campaign_fresh_gravity/CFG1_evidence_audit.py
```
