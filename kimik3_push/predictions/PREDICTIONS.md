# PREDICTIONS.md — the programme's testable-predictions ledger (kimi-k3 consolidation, 2026-09-13)

Numbered, falsifiable, number-carrying predictions the framework makes that Newton/GR/ΛCDM do **not**,
with values, kill conditions, the ΛCDM contrast, and the deciding instrument. Both a₀ footings are quoted
wherever a dimensionful number appears: **canonical** a₀ = ½c√(Gρ_DE) = 9.3619e-11 m/s²,
**alt** a₀ = ½c√(Gρ_crit) = 1.1279e-10 m/s². Ratios a₀(z)/a₀(0) are footing-independent.

Every value below is recomputed in `kimik3_push/scripts/K004_predictions.py`
(output captured at `kimik3_push/logs/K004_predictions.out`). Sources named per entry.
Pre-registration status is stated per entry — do not represent a NEW entry as registered.

---

## P1. Gaia DR4 wide-binary velocity boost (Arm A / Arm B)

| field | value |
|---|---|
| Observable | γ_v, the wide-binary velocity boost at 2–30 kAU |
| Predicted value | **Arm A (Amendment 10, frozen): γ_v = 1.1614–1.1814 canonical / 1.1917–1.2267 alt.** Arm B (Amendment 11, covariant candidate at Cassini-minimal ξ): ceilings **1.0450 / 1.0300**, falling toward 1.000. Newton = **1.0000 exactly** |
| L240 photocount reading (n = 2, recomputed) | γ_v(20 kAU) = **1.095–1.111** (mult/add EFE laws bracket; K004 reproduces 1.0953/1.1113, Y_e = 1.146), **below the Arm-A band**; the Milky Way external field removes ~83% of the isolated boost (1.575) |
| Kill condition | Amendment 11 decision rule, fixed in advance: **A falsified if γ̂ < 1.056; B falsified if γ̂ ≥ 1.129; undecided 1.084–1.101.** γ̂ > 1.23 = unscoreable (contamination guard). Separately: a confident DR4 detection **inside Arm A counts AGAINST the framework's photocount external-field effect** (L240), which predicts 1.095–1.111 |
| ΛCDM contrast | Newton/GR: γ_v = 1.000 at every separation, no boost, no band |
| Deciding instrument | **Gaia DR4, ~Dec 2026** (N ≈ 30k wide binaries, σ_sys = 0.02; frozen pipeline `prep_2026/gaia_dr4_prep/`, readiness 7/7). DR4 separates Arm A from Arm B at 4.2σ_tot but cannot confirm B over Newton beyond 1.6σ_tot |
| Status | **Pre-registered** — Amendment 10/11, append-only, hash-stamped |

## P2. a₀(z) redshift law — flat vs evolving

| field | value |
|---|---|
| Observable | a₀(z)/a₀(0) = √(ρ_DE(z)/ρ_DE(0)) — footing-independent |
| Predicted value | **w = −1: flat to <1% for z ≤ 5** (a₀(3)/a₀(0) = 0.99997; a₀(5)/a₀(0) = 0.99963). On DESI DR2 w₀wₐ (stage-17 lane): **1.036 at z = 0.35, 0.99 at z = 1, 0.87 at z = 2, 0.78 at z = 3** (K004's independent CPL evaluation at (w₀,wₐ) = (−0.827,−0.75) gives 1.032/0.963/0.818/0.700 — same trend, slightly deeper; the quoted ledger values stand as the corpus's stage-17 numbers). Within ±20% of today out to z = 3 for any constant w ∈ [−1.1, −0.9] |
| Decisive sub-test | **Deep-MOND BTFR zero-point at z ≈ 2.5: framework 0.00 dex (DEC −0.09) vs ΛCDM-native +0.33 dex; one clean point at ±0.13 dex decides at 20:1** |
| Kill condition | Any robust evolution of a₀, **either sign**, below z ≈ 5. A value at +0.3 dex at z ~ 2.5 kills FLAT; a robustly rising a₀ ∝ H(z) (~3× by z = 2) kills the F(Q)Θ constant-a₀ prediction (L90). Cannot track H(z) (×3 by z = 2) and cannot mimic ΛCDM's emergent scale (×1.8 by z = 2) |
| ΛCDM contrast | ΛCDM's effective acceleration scale is emergent and rises: ×1.8 (z=2), ×2.1 (z=2.5), ×2.6 (z=3). To mimic a flat a₀, ΛCDM needs halo dilution c/c_Nbody = (H/H₀)^(−2/3): **0.61 at z=2, 0.40 at z=3, 0.12 at z=5** (the "crispy gap", A-9) |
| Deciding instrument | Deep-MOND lensed rotator at z ≈ 2.3–2.9, screened with **JWST/NIRSpec** then **ALMA CO(3–2) Band 3**; existing archives exhausted (12 constraints, prior-dominated). DESI (w₀wₐ) and Rubin/LSST-DESC for the w(z) gate (A-3, frozen 2026-07-21) |
| Status | **Pre-registered** — DOI 10.5281/zenodo.22563139 (target gate, two-stage funnel, frozen statistic) |

## P3. Positive dark-matter equation of state

| field | value |
|---|---|
| Observable | w_dm, the dark sector's equation of state |
| Predicted value | **0 < w_dm ≲ 1e-4** (strictly positive — criticality requires w > 0; acoustic scale bounds above). Tightened: see P4 |
| Kill condition | A measurement of w_dm consistent with exactly 0 at better than the band width, or any negative w_dm, kills the criticality mechanism (w = 0 puts the clock at proper time, removes the instability and the attractor — L201 V5: "the framework cannot sit at w = 0") |
| ΛCDM contrast | ΛCDM: w_dm = **0 exactly** |
| Deciding instrument | Testable in **existing data** — a dedicated reanalysis of the CMB acoustic scale + large-scale structure (CLASS refuses w > 0 by design, so the acoustic scale must be integrated directly; L201); not a future-mission prediction |
| Status | **New to the published record via this programme** (README rev 13–15, L192–L207 chain, DOI 10.5281/zenodo.22728789); not an externally registered prediction |

## P4. Tightened upper bound w ≤ 5.7e-7

| field | value |
|---|---|
| Observable | The dark sector's equation of state, upper edge |
| Predicted value | **w ≤ 5.66e-7** (L217), forced by holding a₀ flat against the matter coupling's symmetry breaking (a₀ would otherwise drift down 12.4% since z = 5 against the 1% the flat law allows). **177× tighter than the acoustic bound** 1e-4. Two-sided window (L218): **1.5e-8 ≲ w ≲ 5.7e-7** — the first time the programme bounds w from below (floor: criticality must have run by z = 30) |
| Kill condition | A measurement resolving w_dm above 5.7e-7 kills the flat-a₀ conservation argument; a measurement below 1.5e-8 kills criticality at the forest's own κ. (Caveat, flagged honestly: at 5.7e-7 the number is far out of experimental reach — recorded as a real cost) |
| ΛCDM contrast | ΛCDM: w_dm = 0, which sits **below the framework's floor** — the *sign* of w is the discriminator, not the magnitude |
| Deciding instrument | None currently named that reaches 1e-7; the acoustic band (1e-4) is reachable in existing data (P3), the tightened ceiling is a theory bound |
| Status | Programme-internal (L217/L218, README rev 18); the *published* band is 0 < w ≲ 1e-4 |

## P5. Power-law approach to Newton — Saturn anomalous acceleration

| field | value |
|---|---|
| Observable | Anomalous sunward acceleration at Saturn's orbit from the residual 1 − μ = (s/g)² of the parameter-free photocount curve μ = 1 − (1+Y)^(−2) |
| Predicted value | **5.84e-16 m/s² canonical / 8.53e-16 m/s² alt** (K004; corpus headline 5.8e-16, ~17× under the Cassini residual ~1e-14). Fractional departure 9.7e-12 / 1.4e-11 |
| Kill condition | Ranging that reaches below **8.5e-16 m/s²** at Saturn and finds nothing kills the n = 2 power-law curve. Conversely the framework's fitted Route-A (exponential) kernel predicts **exactly zero** there — so a *detection* at this level kills the fitted kernel. The two are distinguishable in principle by ranging; this curve is the one that sticks its neck out |
| ΛCDM contrast | GR: zero anomalous acceleration (beyond modelled gravitoelectric terms) |
| Deciding instrument | **Cassini-class ranging / next-generation ephemeris** (current Cassini residual ~1e-14 misses by 12–17× — safe but not comfortable) |
| Status | Derived in L233; **the both-footings band [5.84e-16, 8.53e-16] is NEW to this ledger (N1)** |

## P6. Universal galaxy-scale dark fraction (clock-frame kicks)

| field | value |
|---|---|
| Observable | Retained dark fraction f of galaxy-scale hosts under C003 clock-frame kicks |
| Predicted value | Retention saturates at the unkicked Poisson fraction **e^(−n) = e^(−2) = 0.135** (L191): the **SAME dark fraction at 10⁹ and 10¹¹ M☉ baryonic** — every host whose escape speed is below the kick speed sits on the floor, however hard the kick. (Best-fit: spiral 0.099, MW 0.099, group 0.097 — a prediction, no ledger anchor — cluster 0.594) |
| Kill condition | **SPARC demanding a dark-fraction trend steeper than 1.2× across 10⁹–10¹¹ M☉** baryonic kills the universality (the ledger's own shallow trend f ~ M^0.16 gives 1.33× spiral→MW; the mechanism gives 1.00×) |
| ΛCDM contrast | ΛCDM + abundance matching gives a strong, monotonic mass trend in the dark fraction across that range (mock: slope +0.23 vs framework +0.03; B-1) |
| Deciding instrument | **SPARC** (existing 175-galaxy sample, re-binned in baryonic mass); the mechanism is a CANDIDATE (C003), not derived — flagged |
| Status | Programme-internal (L189/L191, README rev 11); not pre-registered externally |

## P7. RAR scatter, BTFR zero-point, dwarf EFE

| field | value |
|---|---|
| RAR intrinsic scatter | **0.108 dex** at Υ = 0.70 on 175 SPARC galaxies (Route-A kernel; 0.127 on μ₁₀). FRIED CHICKEN row 1 wants ≤ 0.06 dex — ⚠️ **currently missed**, recorded as a standing shortfall, not a win |
| BTFR | v_c⁴ = G M_b a₀: **exponent DERIVED** (virialisation_2026), zero point 0.25·log₁₀(Ga₀) = −5.0511 canonical / −5.0308 alt — within 0.03 dex of the fitted-scale value; with a₀ fixed the normalisation stops being a calibration and becomes a falsifiable number (L233 V4) |
| Dwarf σ–R_gc external-field effect | **Standing cost, honestly flagged:** both EFE laws UNDERPREDICT classical dSph dispersions (median −0.13 dex at M/L_V = 2 isolated, worse with EFE), robust to a free M/L (σ ~ M^1/4 lifts both together) and to dropping Sagittarius. Part pre-existing MOND-wide dwarf problem, part genuine EFE over-suppression (L240 V6–V8) |
| Kill condition | RAR: a resolved interpolating shape with slope ≠ 2 kills the photocount curve. BTFR: a zero-point measurement outside [−0.03, +0.03] dex of the predicted footing values. Dwarfs: a clean dispersion measurement programme at known M/L decides whether the deficit is the EFE or the M/L |
| ΛCDM contrast | ΛCDM has no RAR with 0.108 dex intrinsic scatter as an input-free statement (AM+NFW mock: 0.45 dex); BTFR zero-point is a halo-property output, not a constant; no external-field effect exists in Newtonian dwarfs |
| Deciding instrument | SPARC (RAR, BTFR); **ELT/Keck-class** resolved stellar kinematics for dwarfs |
| Status | RAR/BTFR are retrodictions that hold (B-1/B-2); the dwarf EFE deficit is a standing liability |

---

## NEW predictions derived in this ledger (K004)

### N1. Saturn anomaly on both footings, as a band
**[5.84e-16, 8.53e-16] m/s²** (canonical/alt) for the n = 2 power-law curve. Kill: a ranging bound below 8.5e-16 m/s². Cassini (~1e-14) misses by 17×/12× — safe but thin. This is the first time the number is stated on both footings as a band with an explicit kill threshold.

### N2. Named-z, named-w a₀ value
On DESI DR2 (w₀, wₐ) = (−0.827, −0.75), at **z = 2.5**: **a₀(z)/a₀(0) = 0.7553**, i.e. a₀(2.5) = **7.07e-11 canonical / 8.52e-11 alt m/s²**, a BTFR velocity zero-point shift of **−0.031 dex**. A measured z ~ 2.5 zero-point at −0.03 dex would confirm the DESI-evolving branch and kill the frozen flat-law pre-registration at 0.00 dex — this is the specific number that pits the framework's own two branches against each other on a named dataset.

### N3. γ_v(20 kAU) on both footings, photocount EFE
**γ_v(20 kAU) = 1.0953 canonical / 1.1240 alt** (multiplicative law, n = 2). Kill: a DR4 value outside **[1.085, 1.134]** kills the photocount-EFE reading; a value inside Arm A (≥ 1.1614) kills it at high confidence. First both-footings statement of the L240 number.

---

## Honesty flags

- **Too close to distinguish:** P3/P4 — the w_dm band's *sign* is the discriminator and ΛCDM's exact 0 sits below the framework's floor, but no named instrument reaches w ~ 1e-6–1e-7; the acoustic band (1e-4) is reachable in existing data, the tightened ceiling is not. Flagged as a real cost.
- **Against-interest, on record:** a confident DR4 detection *inside* the registered Arm-A band counts **against** the framework's external-field effect (L240), not for it — the preregistration is frozen and the L240 number sits below it. Both statements stand; DR4 decides which falls.
- **Standing shortfalls carried, not hidden:** RAR 0.108 dex vs the 0.06 requirement (row 1); the dwarf EFE over-suppression; requirement 10 (amplitude law) OPEN — nothing here is published as a completed theory.
- **Pre-registered vs new:** P1 (Amendment 10/11) and P2 (DOI 10.5281/zenodo.22563139) are pre-registered; A-3 (Rubin w(z) gate) is frozen (2026-07-21); P3–P7 are programme-internal published-with-DOI (Zenodo) but not externally registered; N1–N3 are NEW to this ledger and must not be represented as registered.
