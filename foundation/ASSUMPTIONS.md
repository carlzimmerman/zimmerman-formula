# Assumption register (charter §3), DRAFT entries A01–A59

Status: **DRAFT.** The charter (`PROGRAM.md`) is not approved ("not yet", owner 2026-10-10), and nothing here changes it. These entries fold in `campaign_fresh_gravity/CFG594_halo_assumption_audit/HALO_ASSUMPTIONS_AUDIT.md` (59 items, 2026-10-10). Documentation only: no result is re-derived and no number here is new. Quick-check numbers (QC) come from `cfg594_sensitivity_results.json`.

Settings that apply to everything below: κ = ½ is FITTED. The footings (9.3603e-11 / 1.1312e-10) are never pooled. The cold energy's mass is still required. This is not "theory closed".

**Rule (charter §3):** a verdict counts only if it survives the framework-native alternative, or if the dependence is stated on the board. **Owner rule 2026-10-10:** verdicts use RAW data against framework-native predictions only. ΛCDM and standard MOND are neither yardsticks.

**Key to the entries.** Each entry gives: what it is and where it enters; the direction it could bias a test; the framework-native replacement. "E" is the halo-model excess max(R − 1) over 0.05 ≤ k ≤ 1 (CFG556 base +0.715 canonical / +0.883 alt); "CUT" means the 10% cut on both footings.

Class counts: DATA-FORCED 10, FRAMEWORK-DERIVED 13 (2 posited), ΛCDM-INHERITED 17, STANDARD-MOND-INHERITED 7, CONVENTION 12.

Source keys: PM = `CFG527_law_respecting_engine/cfg527_pm.py`; HM = `CFG556_halo_model_matter_power/cfg556_halo_model.py`; LIB557 = `CFG557_settling_catchment_derived/cfg557_lib.py`.

## A. Data-forced (A01–A10): no replacement needed; the dependence is on the data

| ID | audit | ingredient | where it enters | bias direction / note |
|---|---|---|---|---|
| A01 | D01 | low-acceleration law shape (SPARC RAR) | PM:107-119; HM:53-55 | fitted to SPARC; ν_simple and ν_standard fail SPARC |
| A02 | D02 | a0 levels, two footings (κ = ½ FITTED) | PM:90; HM:47 | footing-conditional; never pooled |
| A03 | D03 | cosmic cold amount ω_c = 0.120 (Ω_c/Ω_b = 5.364) | PM:85; HM:27; `cfg515_lib.py:17` | CMB-measured at z ≈ 1100 (CFG511) |
| A04 | D04 | ω_b = 0.02237, cosmic f_b | PM:85-86; HM:28 | CMB/BBN |
| A05 | D05 | cold energy has c_s² ≈ 0 and clusters below the horizon | one cold species, PM:248-263 | DESI fσ8, Ly-α (CFG508 T1 c_s² ≤ 7e-7) |
| A06 | D06 | R6: round settled cold energy, not a phantom disc | HM frame_profile:111-180 | MW K_z 32/32 (CFG514/516). NOT obeyed by the PM (see A41) |
| A07 | D07 | R7: no external-field effect | HM, CFG557/559 | cluster satellites (CFG478), Gaia DR3 (CFG447). NOT obeyed by the PM (see A41). R7 is what keeps halos concentrated (see A45) |
| A08 | D08 | isothermal phantom tail out to ~Mpc | edge at 0.2–0.4 r_ta (CFG556) | KiDS lensing RAR = dynamical RAR |
| A09 | D09 | extra gravitating matter in clusters and lenses beyond the law of baryons | A4 and G9 | cluster lensing / Bullet |
| A10 | D10 | survey calibrations: ξ± data, covariance, n(z), m-bias, NLA IA | `cfg590_shear.py`, `cfg592_native.py` | measurement nuisances, not cosmology |

## B. Framework-derived (A11–A23): replacement is the derivation itself

| ID | audit | ingredient | lane | where |
|---|---|---|---|---|
| A11 | F01 | a0 = κc√(Gρ_DE); a0(z) tracks ρ_DE | PAPER42; CFG512 | PM:96-105 |
| A12 | F02 | R1 phantom = settled cold energy, gravitating (G9) | THEORY_v1 R1 | PM:448, :491; HM:111-180 |
| A13 | F03 | candidate-B switch λ₂ ≥ τ = (Δ_ta − 1)/3 = the turnaround ball for a spherical profile | CFG557 D1 | PM:374-378 |
| A14 | F04 | R2 supply edge r_e = r_M/ln(1 + f f_b/(1 − f_b)), exact for the RAR kernel | CFG423 / T10 | PM:313-319; HM:136 |
| A15 | F05 | R3 per-catchment mass conservation | CFG424 (MUTATE +15% clumping) | PM:448-491 |
| A16 | F06 | R5 draw from the shell between the edge and r_ta | CFG527 | PM:458 |
| A17 | F07 | R4 phantom sourced by retained baryons f_ret(x)(1 + δ) (the rule; the f_ret values are A29) | CFG518 | PM:410-416 |
| A18 | F08 | R8 shared supply for overlapping catchments | CFG522 | LG timing |
| A19 | F09 | gravitating-field statistic δ_grav = −k²φ/(1.5Ω_m) | CFG555 | `cfg555_compute.py:130-133` |
| A20 | F10 | free-fall ceiling on the settled supply (α-free), a derived UPPER bound | CFG557 | LIB557:156-200 (dynamics under it are A33) |
| A21 | F11 | cold-energy EoM class A (metriplectic), α FREE | CFG539/541/542 | not in the verdict engines |
| A22 | F12 *posited* | FIX-2 kinetic closure (isotropic Jeans OU): POSITED, not derived | CFG544/554 | CFG559 toy |
| A23 | F13 *posited* | A6 supply postulate: each system settles the cosmic share of its baryons. Six derivations failed | THEORY_v1 | HM:117; PM catchments |

A11 and A13 contain fitted or inherited numbers (κ; Δ_ta), listed under their own classes.

## C. ΛCDM-inherited (A24–A40)

**A24 (L01) Linear initial spectrum.** Eisenstein–Hu no-wiggle, n_s 0.965, σ8 = 0.811, Zel'dovich at z_i = 49, D(a) from GR + Λ. *Where:* PM:85-87, 121-139, 248-263; HM:27-43; LIB557:28-41; `cfg592_native.py:31-43`. *Bias:* enters framework and S0 identically, so ratio verdicts are insensitive at first order; absolute shear (CFG590/592) is directly sensitive. *Native:* ω_c, ω_b are CMB-measured (A03/A04) and B equals ΛCDM linearly (CFG324/354); what is not native is σ8 = 0.811 and h, from a ΛCDM CMB fit. Fit A_s, h, Ω_m inside the framework (switch off at z > z_i) to CMB + BAO and regenerate ICs. Not run. *QC:* σ8 0.76 MINOR (ΔE +0.023 / +0.006).

**A25 (L02) Background expansion.** Flat GR + Λ, w = −1, h = 0.6736, Ω_m = 0.315. *Where:* PM:85-94; HM:27-28; LIB557:65-77; CAMB in `cfg590_shear.py`, `cfg592_like.py:28-43`. *Bias:* small for growth ratios (a0 tracking vs flat: Δσ8 ≤ 0.0006, CFG508); larger for absolute ages (CFG557 ceiling). *Native:* PM with a DESI w0wa background and a0 tracking (only CFG591 addendum and CFG592 distances do this). Needs a PM rerun.

**A26 (L03) Turnaround density Δ_ta = 11.81.** Spherical top-hat shell ODE in the ΛCDM background. *Where:* PM:142-171, :310-311, :327, :341, :374-378; HM:50. *Bias:* a lower Δ_ta means a larger catchment, so more supply and more excess. *Native:* under B the law is off before turnaround, so this ODE IS the framework's own spherical collapse given A25. The residual native correction is a secondary-infall model with settled interior cold energy and the w0wa background. *QC:* × 0.8 / × 1.2 MODERATE (ΔE +0.106 / −0.085 canonical).

**A27 (L04) Cold energy = collisionless CDM outside bound systems.** One PM species carries all of Ω_m; the settled part is bookkeeping. *Where:* PM:248-263, :435; THEORY_v1 A5. *Bias:* sign-setting through the supply amount (A28), but the bookkeeping is not the driver (CFG539's moving species gives the same excess: 0.347 vs 0.336 canonical). *Native:* a two-species PM whose cold species obeys the framework's own settling dynamics, with the settled amount measured. CFG539 tried; class A has α free and fails. Open.

**A28 (L05) Supply amount = (1 − f_b)M_ta, the whole turnaround ball.** *Where:* HM:117; `cfg515_lib.py:9-10`; PM:383, :391. *Bias:* the largest. Turnaround ball E +0.715 / +0.883; r200m ball −0.000 / −0.081 (CFG556); α-free ceiling +0.382 / +0.458 (CFG557). *Native:* (i) measure the cold mass that actually enters each host's edge in the PM (done in CFG595: supply 1.5–3.6× larger than assumed, excess persists at about half size); (ii) the A27 two-species run. *QC:* × 0.5 / × 0.75 DRIVER / MODERATE; × 0.5 does not reach CUT.

**A29 (L06) Census f_ret(M_ta).** Numerator observed baryons; denominator uses a ΛCDM halo mass. 0.10 below 10^12.5, 0.55 at 10^13.5, capped 0.90. *Where:* PM:302-308; HM:87-92; `cfg515_lib.py:20-40`. *Bias:* large and sign-relevant; for a galaxy the supply is 54 M_b (the ΛCDM abundance-matched halo). *Native:* each system's catchment mass from its own data (Hubble-flow zero-velocity surface, as CFG548 for the LG; weak-lensing profile beyond r_e), then f_ret = observed baryons / (f_b × that mass). Lane CFG600. *QC:* × 0.5 canonical E = +0.063 (CUT), alt +0.188; × 2: +0.165 / +0.163. DRIVER.

**A30 (L07) Moster13 / Behroozi SHMR.** *Where:* HM:93-96 (star/gas split only); KiDS harness `CFG529…/cfg529_tables.py:47, 61` (sets lens M_ta). *Bias:* halo model none (|ΔE| ≤ 0.001); KiDS sets the per-lens supply, same direction as A29. *Native:* as A29. KiDS-side sensitivity: lane CFG601.

**A31 (L08) NFW + Duffy08 c(M).** The ΛCDM reference profile in R = P_F/P_L; the shape defining r_ta, M_ta; the shell outside r_e. *Where:* HM:76-84, 159-180; CFG557/559; `cfg591_lib.py:79-99`; `cfg593_lib.py:81`. *Bias:* mostly yardstick; a lower ΛCDM concentration gives larger R. *Native:* drop the halo-model reference; compare the framework's own P(k) or ξ± with raw data (CFG592 native); take r_ta and shell shape from PM infall profiles. *QC:* c × 0.7 / × 1.3 DRIVER / MODERATE (ΔE +0.281 / −0.153 canonical). The size of the "excess" is not robust to this choice; neither direction removes it.

**A32 (L09) Tinker08 mass function + Tinker10 bias.** *Where:* HM:57-73. *Bias:* small. *Native:* the PM's own n(M_ta) from turnaround balls. *QC:* Press–Schechter MINOR (+0.036 / +0.008).

**A33 (L10) EPS main-progenitor histories + ΛCDM shell trajectories.** Neistein+06, q = 2.2, recalled, PROVISIONAL. *Where:* LIB557:8-9, 78-100, 140-152. *Bias:* sets the settled fraction, roughly half the excess (CFG557 0.50–0.80; CFG559; CFG590/591). *Native:* accretion histories of the PM's own turnaround balls across snapshots. No QC (needs halo matching).

**A34 (L11) S0 (ΛCDM DM-only PM) as the YARDSTICK.** The CFG361 cut |P/P_S0 − 1| ≤ 0.10 (k ≤ 1) and σ8 within 5%. *Where:* `CFG530…/cfg530_analysis.py:197`; cfg424/518/527 analyses; CFG556 growth; CFG557/559. *Bias:* two-sided. Every GROWTH OK / TENSION label rests on it. Against raw shear ΛCDM-DMO is itself above the data (A = 1 vs 0.86). *Native:* S0 stays as the same-pipeline comparison only; the verdict is framework vs raw ξ± or fσ8 (CFG592 native: 27 of 29 runs NOT DIAGNOSTIC at k ≤ k_Nyq/4; the two L100 N512 runs give Δχ² +24 / +30 KiDS, +4 / +6 DES). A decisive version needs a higher-resolution or zoom PM reaching k ≈ 5–10 h/Mpc.

**A35 (L12) HMcode-2020 DMO P_NL × BAHAMAS feedback S_fb.** *Where:* `cfg590_shear.py:61-62`; `cfg592_like.py:42, 59-67`; `cfg592_de.py:50`; `cfg591_shear.py:33`. *Bias:* multiplies the framework's R onto a ΛCDM non-linear spectrum with ΛCDM-calibrated feedback. CFG590 is CONTEXT ONLY. *Native:* CFG592 native, plus a framework baryon/feedback model (none exists).

**A36 (L13) A_mod form P = P_L + A(P_NL − P_L).** *Where:* CFG590. *Bias:* amplifies R − 1, since A − 1 ≈ (R − 1)P_NL/(P_NL − P_L). *Native:* direct ξ± likelihood (CFG592 native).

**A37 (L14) KiDS lensing harness.** DK14 transition, halofit × ζ two-halo, stripping. *Where:* `CFG529…/cfg529_score.py:3, 470-471`. *Bias:* unknown sign; the 2-halo term is NOT CROSS-CHECKED BY PM. *Native:* the PM's own galaxy–matter cross-spectrum for the 2-halo term, or restrict to 1-halo radii.

**A38 (L15) Epoch evolution of ΛCDM fits.** Duffy (1+z)^−1.01, Tinker and Moster z-evolution. *Where:* `cfg591_lib.py:4-5, 66-99`. *Bias:* as A31/A32 per epoch. *Native:* PM snapshots at z = 1 and 0.5.

**A39 (L16) Planck-like CAMB distances and growth in the shear projection.** *Where:* `cfg592_like.py:28-43`; `cfg592_native.py:52-71`. *Bias:* small (DESI variant moves KiDS Δχ² +23.9 → +18.1). *Native:* framework background (A25).

**A40 (L17) r_ta and "cold infall from r_ta" in the kinetic toy.** From the NFW-extended halo. *Where:* `CFG559…/cfg559_toy.py:55-61`. *Bias:* as A31 and A26. *Native:* PM infall profiles.

## D. Standard-MOND-inherited (A41–A47)

**A41 (M01) QUMOND phantom on the global peculiar baryon field.** ρ_ph = −∇·[(ν − 1)g_b]/4πG; non-round, and |g_b| contains neighbours' fields (an implicit EFE). *Where:* PM:421-434; named open in `CFG541…/EQUATIONS.md:91, 227`. *Bias:* the EFE part lowers ν, so the excess is understated; the negative-phantom lobes clipped at PM:448 bias it up; they partly cancel. *Native:* round per-region phantom from the enclosed retained baryons of each B region (EQUATIONS E7). *Check on disk:* core mass ratio R = M_grav(PM)/M_law(round) is 0.94–0.98 (256³) and 1.04–1.14 (N512), so the departure from R6/R7 is bounded to about 15% in halo mass; not the driver.

**A42 (M02) Kernel reads the local |g_b| alone, in comoving peculiar fields.** *Where:* PM:424. *Bias:* unknown; limited by the switch. *Native:* as A41.

**A43 (M03) Kernel low-y form is an empirical fit (McGaugh+16 RAR) extrapolated to groups, clusters and Mpc edges.** ν_mono's monotone high-y tail is the framework's own. *Where:* PM:107-119; HM:53-55. *Bias:* moderate. *Native:* data-forced for discs (A01); for groups and clusters the group baryonic Faber–Jackson (Tian+26) and lensing-RAR data decide. *QC:* ν_simple MINOR (+0.002); ν_standard MODERATE (−0.138 / −0.136); both SPARC-disfavoured.

**A44 (M04) Deep-MOND asymptotics as derivation shortcuts.** Edge r_e ≈ r_M(1 − f_b)/(f f_b); V_f = (G M_b a0)^¼ in the kinetic toy; σ⁴ = G M_b a0/4 (CFG539 class B); T = V_f²/2 (CFG550). *Where:* edge in every lane; CFG544/550/554/559. *Bias:* small (point mass vs extended baryons). *Native:* numerical supply exhaustion on the real enclosed baryon profile (the point-mass closed form is exact for the RAR kernel, QC M0). No σ⁴ = (4/81)G M a0 shortcut appears in the audited lanes.

**A45 (M05) The EFE question.** Framework: none (A07). Standard MOND: yes. *Where:* HM and CFG557/559 have none; the PM has a partial EFE through A41. *Bias:* **decisive in the halo model.** With a standard-MOND EFE the phantom saturates at (ν(y_ext) − 1)M_b, far below the 54 M_b galaxy supply; the edge never forms and the halo is not concentrated. *Native:* not a replacement. R7 is data-chosen, so the framework's halo excess depends on it rejecting EFE. Keep R7 under test (Gaia DR4 wide binaries, PAPER35; cluster satellites). *QC:* y_ext 0.01 MODERATE (−0.105 / −0.103); y_ext 0.03 DRIVER and CUT (E −0.002 / −0.002).

**A46 (M06) r_M, the "MOND radius".** Where a0 enters the supply edge (PM:313-319). As A44.

**A47 (M07) "Standard MOND predicts X" yardsticks.** None is used as a verdict yardstick in the audited lanes (grep of the READMEs). The only "phantom = extra gravity" construction is the MUTATE no-compensation control, used as a tooth.

## E. Convention / numerical (A48–A59)

| ID | audit | item | where | note |
|---|---|---|---|---|
| A48 | C01 | box L (200, 100, 50, 25), mesh 256/512, NSEED, seed 359 | PM:92 | CFG530: P(k) converges at fixed box; core R does not (canonical) |
| A49 | C02 | resolved-host cut RMIN = 1.56 Mpc/h | PM:80, :344 | PM hosts are groups and clusters only; the f_ret ≈ 0.10 galaxy regime is untested in the PM |
| A50 | C03 | switch width ε = 0.077; peak threshold 3(τ − ε) | PM:93, :327, :378 | CFG427: ε insensitive |
| A51 | C04 | MIX-A gas pressure filter | PM:81, :398-409 | replaced by NOFILT in CFG527/530 |
| A52 | C05 | cover recomputed every 10 force calls | PM:380-384 | — |
| A53 | C06 | 150 KDK steps | PM:265-271 | — |
| A54 | C07 | CIC / mesh softening; P(k) cut k ≤ 1 | PM:541 | — |
| A55 | C08 | halo-model grids (mass 1e8–1e16, NR 1600, k 1e-3–10) | HM:57, 106-109, 194 | control C4 1e-3 |
| A56 | C09 | cap e/q when q > 1 | PM:461-466 | never acted |
| A57 | C10 | sharp vs softened edges (s25 / s55) | HM:140-176 | declared variants |
| A58 | C11 | declared baryon shapes: Hernquist stars, β-model gas | HM:97-106 | emergent-edge variant very sensitive to outer gas (CFG556) |
| A59 | C12 | CFG592 native support cut k ≤ k_Nyq/4 | `cfg592_native.py:250-304` | makes most runs NOT DIAGNOSTIC |

## F. Ranking from the audit (what to replace first)

1. A27 + A28 (catchment supply sized by ΛCDM-like clustering): measure the settled amount (CFG595 did the first half).
2. A29 + A30 (census f_ret and SHMR masses): catchment mass from each system's own data (lane CFG600; sensitivity CFG601).
3. A34 + A35 + A36 (S0 yardstick, HMcode/BAHAMAS, A_mod): CFG592 native at a resolution that keeps most ξ± points.
4. A31 (NFW/Duffy reference): retire the halo model from verdicts (done by the owner rule).
5. A41 + A45 (QUMOND phantom, EFE): round per-region phantom in the PM; R7 against DR4.

## G. What this register does NOT say

- It does not say the excess is an artefact. The most native PM evidence (CFG555 gravitating field at 512³; CFG530 core R about 1) shows the framework's halos are more concentrated than ΛCDM's at the same initial field.
- It does not say the data favour the framework.
- The supply (A23) and the switch remain inputs.
