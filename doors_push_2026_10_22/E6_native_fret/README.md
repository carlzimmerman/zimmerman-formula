# E6_native_fret — CRISP FINDING. Dynamics: STILL UNDECIDABLE (a scoped no-go). The satellites' own chemistry: the supply ceiling suffices without the census

**Verdict.**
1. **Main (dynamics, as asked): STILL UNDECIDABLE. Both footings.** The framework's own dynamics cannot fix a satellite's
   catchment.
   - The law acts only inside the turnaround ball (CFG557 D1, CFG654 primary, SCT R1). The law-on-outside reading is
     excluded by the LG zero-velocity radius (CFG548, Z +6).
   - The phantom it builds there is drawn from the same catchment; its source sums to zero on the catchment (CFG424, SCT R3).
   - So, by Gauss's law, every shell outside the ball turns around under plain GR dust + Λ with its true enclosed mass.
   - The catchment mass M_ta is therefore set by the **initial overdensity of the satellite's Lagrangian patch** and by **when
     its accretion stopped** (infall). M_b, a0, κ and L★ do not enter.
   - Baryon retention is set by cooling and feedback (CFG806), not by the law. The cold supply needs no baryon retention anyway:
     C = (Ω_c/Ω_m) M_ta.
   - The record fixes neither number per satellite. Per the brief, the lane names them and stops.
2. **What the framework's own tides demand (D2).** For a catchment to survive inside its Jacobi radius in the host's law field
   today, it must have turned around by z_req. z_req does not depend on the satellite's mass.
   - Median z_req = **11.3** canonical / **11.6** alt (range 3.7 to beyond 49).
   - Pictor II, at 11.9 kpc, needs a density above the z = 49 turnaround value.
3. **Is the required catchment unusual? (D3, EXTERNALLY CALIBRATED IC column.)** No. It is an ordinary fluctuation.
   - The catchment the data need is small: median M_ta,req = 6.0e5 M☉ (F1) and 1.2e6 M☉ (F2).
   - In the CFG654 native linear field (Planck A_s and n_s), a patch of that mass turning around by z_req is a
     **ν_req = 1.21σ** peak (F1 canonical; F2 1.27; alt 1.31 / 1.26). Class **IC-ORDINARY**.
   - The largest values are 3.7–3.9 (Carina II, Reticulum II).
   - So the initial field allows the catchment. It does not assign one to a given satellite.
4. **The satellites' own chemistry bounds the catchment from below, with no ΛCDM input (Part C). CHEM-SUPPLIES on both
   footings.** Every baryon that passed through a satellite's star-forming gas was in its catchment.
   - CFG920's homogeneous leaky box, with LVD [Fe/H], gives catchment baryons ≥ L_min × present baryons.
   - At the most conservative corner (log y −0.5, closed box plus strip), the median L_min is **38.3** canonical / 37.9 alt.
     That is above the census's 10 and above the median L_req of 8.3 / 8.0.
   - So **E3's census-free shortfall (q = 8.0, +0.90 dex) does not survive the satellites' own chemistry.**
   - Median q_chem is **0.21** (84%: 0.25) canonical and 0.19 (0.24) alt. With the phantom also paid from the catchment
     (F2), it is 0.27 / 0.27. At the nominal yield it is 0.08–0.10.
   - 6 of 36 tested systems exceed q = 1 at their central values: Columba I, Segue 1, Tucana IV, Ursa Major I, Ursa Major II
     and Willman 1. None exceeds it at 2σ.
5. **What E3 said still holds.** "Can supply" also needs a mechanism that packs the cold energy inside r12. That means
   compressing a turnaround sphere of about 0.8 kpc (at z_req) into tens of pc. The record has no such mechanism
   (CFG822/842/888/889/959).

κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold energy; no particle. Not "theory closed". Nothing here
says the data favour the framework.

## Commits and files
- Criteria: `FROZEN_CRITERIA.md`, c42925d9dc (committed alone first).
- A1 (pre-result for all D/C numbers): 5c0669a33d.
- A2 (post-result; reporting only plus one bug fix): appended in the result commit.
- Script `e6_native_fret.py` → `e6_native_fret.out`, `e6_native_fret_results.json`, `e6_per_system.csv`. `--mutate` →
  `*_MUTATE.*` (exit 1).
- One thread, nice 15, about 6 s, about 110 MB. Nothing was downloaded.

## Input ledger
| input | source | class | verdict sensitivity |
|---|---|---|---|
| σ, R_e, M* (Υ_V 2), binaries, distance | E3 per-system CSV (LVD + Arroyo-Polonio) | RAW + SURVEY-CALIBRATION (E3 ledger) | inherited from E3 |
| Law ν(y), L★ = 24 pc screening (F1) | A26/CFG820 via E3 | FRAMEWORK-NATIVE (a0 via κ = ½, FITTED) | F1 vs F2 bracket |
| Ω_c/Ω_b = 5.364 | Planck; CFG886 recovered, not pinned | ΛCDM-PROCESSED | q ∝ 1/5.364 (and Ω_m/Ω_c in M_ta,req) |
| Census f_ret 0.10 | CFG416 | ΛCDM-PROCESSED | used only to reproduce E3; **not used by D or C** |
| Background h 0.67403, Ω_cb 0.31285; native Δ_ta(z), D(z) | CFG654 native column (BBN ω_b, CMB ω_c, θ*) | FRAMEWORK-NATIVE background with CMB-fit parameters | D2 only, via ρ̄_m (z_req ∝ weakly) |
| Host baryons MW 6e10, M31 1e11; distance_host | CFG332 / external label; LVD | SURVEY-CALIBRATION / external | D2 only; T ∝ M_h^½ in the deep regime |
| Linear P(k) at z = 0 (A_s, n_s, CAMB transfer); extrapolation beyond k 110 h/Mpc | CFG654 ICs | **ΛCDM-PROCESSED IC column (externally calibrated)** | D3 only. Extrapolating with slope n_s − 4 changes the ν median by ≤ 0.01 |
| [Fe/H] | LVD `metallicity` | RAW (spectroscopic or photometric) | Part C; errors not propagated |
| Fe yield log y ∈ {−0.5, −0.2, +0.1}; ζ = 1; no pre-enrichment | CFG317/CFG920 bracket | SURVEY-CALIBRATION + MODEL ASSUMPTION | Part C: class holds over the whole yield bracket; ζ_break median 14 |

No halo concentration, mass function, r200/NFW or splashback calibration enters. No standard-MOND machinery: the host field is the
framework law, and no EFE is used.

## Part D numbers (from `e6_native_fret_results.json`)
| | canonical | alt |
|---|---|---|
| E3 per-system median q, census f_ret 0.10, F1 / F2 | 0.828 / 0.934 | 0.804 / 0.918 |
| same, f_ret = 1 (present baryons only), F1 / F2 | 8.28 / 9.34 | 8.04 / 9.18 |
| median M_ta,req (q = 1), F1 / F2 [M☉] | 5.97e5 / 1.19e6 | 5.34e5 / 1.23e6 |
| D2 median z_req (N) | 11.28 (44) | 11.61 (45) |
| D3 median ν_req, F1 / F2 | 1.21 / 1.27 | 1.31 / 1.26 |
| ν_req > 3, F1 | 2/38 | 3/37 |

## Part C numbers (median q_chem = L_req / L_min; tested 36/45 canonical, 37/46 alt)
| corner (log y, form) | −0.5 W2 | −0.5 W1 | −0.2 W2 | −0.2 W1 | +0.1 W2 | +0.1 W1 |
|---|---|---|---|---|---|---|
| canonical F1 | **0.211** | 0.151 | 0.105 | 0.076 | 0.053 | 0.038 |
| canonical F2 | 0.274 | 0.181 | 0.138 | 0.091 | 0.069 | 0.046 |
| alt F1 | **0.188** | 0.141 | 0.094 | 0.071 | 0.047 | 0.035 |
| alt F2 | 0.271 | 0.180 | 0.137 | 0.090 | 0.069 | 0.045 |

- **Not tested:** 9 systems have no LVD [Fe/H]: Carina III, And XI, XIII, XVII, XX, XXII, XXVI, XXVII and Cassiopeia II.
- **Metal-enhanced winds (A2, post-result, reported only).** A wind ζ times the ISM metallicity lowers the chemical floor.
  For the 24 supplied systems with a requirement, the floor reaches L_req only at a median ζ_break = 14.5 canonical / 14.3 alt.
  The minimum is 2.8 / 3.0, and only one system (canonical) breaks at ζ ≤ 3.

## Checks and mutation
| check | result |
|---|---|
| K1 | Spherical collapse: EdS Δ_ta 5.55165, δ_lin 1.06243. Native dust + Λ against the CFG654 table: max 0.19% |
| K2 | Catchment identity, a code check that is true by construction: Δt_ta = 0 for a shell 29× outside the edge |
| K3′ (A1) | E3's CSV: median L_req 8.28 / 8.04; q = L_req/10 to 4e-16 |
| K4 | CFG920 leaky box reproduced (Hercules, 6 corners, exact) |
| K5 | σ8 = 0.8271 |

- **MUTATE** (the law acts on shells outside the ball as an extra source): K2 FAILS, with Δt_ta/t_ta = 0.83 (exit 1). This
  reading would make the catchment depend on M_b and a0, but CFG548 excludes it.
- **K3 as frozen FAILED** (0.828 against 0.811). It compared E3's per-system median with E3's all-draw bootstrap headline,
  which are different statistics. It was replaced pre-result by K3′ (A1). The original line is still printed.

## Record errors / wording found
- `doors_push_2026_10_22/E3_dwarf_excess/README.md` Part B takes the extra-only F1 as primary. Under the record's
  mass-conserving rule (CFG424: the phantom is drawn from the same catchment), the tethered phantom inside r12 must also be
  paid from the supply. The consistent requirement is F2 (E3's "Newton" row): median q 0.93 at the census, 9.3 census-free.
  The class does not change.
- E3's "the supply suffices only through the ΛCDM-processed census" is superseded **conditionally**. The satellites'
  chemistry (ζ = 1, no pre-enrichment) gives a larger catchment than the census.
- `THEORY_CANONICAL_2026-10-16.md` S3 defines the catchment as "the baryons within its turnaround radius". For a satellite,
  that radius is fixed by initial conditions and infall, not by the framework law (D1). Any "native f_ret(M)" for satellites
  therefore needs the initial field plus orbits, not the law.

## What this does not show
- No satellite's actual catchment: z_inf needs orbits, and the IC peak assignment needs more than D3's single number.
- Part C is not dynamics. It assumes homogeneous mixing, ζ = 1 and no pre-enrichment (Pop III or external enrichment would
  lower L_min). [Fe/H] errors and the 0.1-dex MDF allowance are not propagated. UFD enrichment is often stochastic.
- D2 uses d_now. Pericentres raise z_req; earlier infall at larger distance lowers it.
- No binding mechanism: the catchment's cold energy is available, not shown to sit inside r12.
- **Most valuable next step:** an Fe-yield / [α/Fe] or MDF-shape constraint for the six chemically short UFDs, plus a test of
  pre-enrichment. That would turn Part C from conditional into decisive. The dynamics side needs per-satellite infall epochs
  from proper-motion orbits in the framework's host field.
