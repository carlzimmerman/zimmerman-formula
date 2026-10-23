# The canonical statement of the theory: v4 DRAFT (dated 2026-10-21; written 2026-10-20)

**Status: DRAFT for the owner's review.** This is a synthesis. It adds no computation, no constant and no prediction, and it
supersedes nothing until the owner adopts it. The frozen 2026-10-14 file, v2 (2026-10-16), v3 (2026-10-18, with all its appended
notes) and the 2026-10-16 corrections note are untouched. Their sealed predictions stand with their dates and hashes. CFG689
(native-ruler BAO) landed while this draft was written and is folded in (§3.8). NC2x (CFG654-A3), CFG928 and CFG929 landed on
2026-10-21 and are filled (§8); CFG924 remains PENDING. Dated 2026-10-21 edit: the DR4 kill line is restated to the registered
test's detectable size (§6; `OWNER_DECISION_2026-10-21_DR4_KILL_LINE.md`).

**How it was built.**
- Every number is copied from a committed LEDGER row, lane README or results JSON. Each carries its lane ID, and the LEDGER's
  commit hash where the LEDGER gives one ("crit." marks a criteria commit when no result hash is given).
- Where a newer committed lane disagrees with an older canonical, the newer lane wins. §0 lists each such change.
- κ = ½ FITTED. The footings 9.3603e-11 and 1.1312e-10 m s⁻² are never pooled. Not theory closed. Nothing here says the data
  favour the framework. "Cold energy" throughout; its mass is required; there is no particle species.
- Audit: `python3 theory_canonical_v4_audit.py` (output committed as `theory_canonical_v4_audit.out`). It checks every commit hash,
  every lane ID and every headline number in this file against the committed record.

## 0. What changed since v3 (the newer committed lane wins)

| # | older statement | what the newer committed lane says | lane |
|---|---|---|---|
| 1 | v2: the framework's two-halo term narrows the outer KiDS deficit "from +149 to +11" (CFG805) | CFG805 profiled a free bias. With no free amplitude, the catalogue two-halo term closes 57–59% of the all-radii shortfall (+100.10 → +40.72 canonical, +123.12 → +52.80 alt): PARTIAL, not robust. The baseline itself moved after a unit fix (+148.7 → +100.1). | CFG903, CFG902 |
| 2 | v2/v3: early-type (red-lens) lensing excess open | A literature IMF α–σ relation removes it on both footings (+0.127 → +0.048 dex canonical, +0.088 → +0.009 alt), CONDITIONAL on discs staying near Chabrier. It may be a stellar-population effect, not cold energy. The condition is untested, so the item stays open. | CFG926 |
| 3 | 10-14 file: "Use native initial conditions" not done | Done on both footings: NC1x (canonical) and NC2x (alt) HOLD against their own control. | CFG654-A2; CFG654-A3 |
| 4 | PAPER55 (2026-10-19) quotes the shear pass by its Δχ² | Quote it as a class. The size of the advantage is amplitude-driven, for the inherited runs and for NC1x. | CFG909, CFG654-A2 |
| 5 | v3 addenda (CFG871/877/878): clump mass M_cl = 81σ⁴/(4Ga0) | CONDITIONAL on a coupling the record does not write; not derived. The record's equations neither bind nor retain a dwarf clump. | CFG888, CFG889 |
| 6 | 10-14 S1: "κ = ½ (measured, not derived)" | κ = ½ is FITTED: an adopted round value inside the combined interval. | CFG835 |
| 7 | the a0(z) reading | A fossil-a0 reframing helps the dwarfs only under the rival a0 ∝ H(z). The framework's flat or DE-tracking a0 gives zero or the wrong sign: evidence about a0(z) that points away from the framework's law, not a rescue. The record also reads three different dark-energy quantities for a0 (ε in canonical S1, −p in stage 17, V in R16). | CFG926, CFG911 |
| 8 | v3: the pressure-supported excess family "open" | Still open, and narrower: no one-constant selector, density threshold, mobility law, history label or kinematic measure reproduces dwarfs, red lenses and cluster cores together. | CFG913 to CFG923 (§4) |
| 9 | the a0(z) prediction from the CPL-chain M-DEC curve; the decisive z ≈ 2.5 target "σ ≤ 0.13 dex" (which assumed an exactly flat a0) | Replaced by the framework's own BAO-ruler band (primary rows only; the θ* rows are not folded in because K9 failed as frozen). The decisive kinematic a0 point at z ≈ 2.5 now needs ≈ 0.100 dex. See §3.8. | CFG689 (6c064b83a) |

## 1. The law and its inputs

**The law.** On galaxy scales g_N = g²/(g + a0), with a0 = ½ c √(G ρ_DE). In the Solar System and the laboratory it is Newtonian,
through the stiffness term of the one-field action (10-14 file, S2; Cassini PASS, CFG770). Some lanes score with the record's
ν_mono kernel, as primary or as a declared variant (CFG571, CFG686, CFG922); each verdict states which.

**Inputs that are still inputs.**

| input | value used | status | lane |
|---|---|---|---|
| κ | ½ | **FITTED.** Combined interval 0.417 ± 0.095 (canonical), 0.345 ± 0.078 (alt); ½ sits 0.80σ / 1.63σ away. | CFG835 |
| a0 footings | 9.3603e-11 (canonical), 1.1312e-10 (alt) m s⁻² | Both reported, never pooled. Their ratio squared is Planck's Ω_Λ (0.68470) by construction, so the ratio is not a finding. | CFG835 |
| Ω_c/Ω_b | 5.364 | Measured input. Rebuilt without the Planck fit: 5.272 ± 0.218 from DESI DR2 BAO + BBN (5.364 RECOVERED), 6.122 ± 0.321 with SH0ES (TENSION), so **NOT PINNED**; the rebuild rests on constant ρ_DE. Closed-form symbol search: ORDINARY (numerology level). | CFG886, CFG855 |
| f_ret (catchment retention) | census, 0.10 at galaxy masses; N = 1/f_ret | Input. A framework derivation failed (NOT DERIVED). Provenance MIXED: the floor is not traceable and the ramp is hand-set. | CFG804, CFG806, CFG886 |
| L* (stiffness length) | ≥ 24.0 pc (95%, canonical; alt 24.7) to ≳ 1 kpc (grid edge) | Bounded, not derived. A soft upper edge 2.04 / 2.14 kpc (single lane). The dSphs want ≤ 22 pc: INCONSISTENT (CONDITIONAL), read as a missing-mass signal, not an L* bound. | CFG820, CFG832, CFG821 |
| α (cold-energy mobility) | galaxy side α ≳ 0.5 | Bounded, not derived. Keeping half a dwarf clump for 12 Gyr would need α ≲ 1e-2. | CFG882, CFG889 |
| Shared inputs of the native shear run | Planck ΛCDM-chain column, H0 from θ*, massless ν, f_ret census, M2 cooling inputs, survey nuisances | Still shared after NC1x. | CFG654-A2 |

The dwarfs' empirical clump velocity σ ≈ 7.53 km/s (CFG877) is a description of the dwarfs, not an input of the law, and it is not
universal (CFG880).

**κ.**
- No record equation gives exact ½. Of 439 derivation or selection attempts, none derives κ = ½ (CFG894). The register later grew
  to 451 attempts with the same result (commit 1845c2149).
- Any derivation must bring in c: the c-free cold-energy system has no dimensionless group that fixes κ (CFG893).
- Every π-free ½ in the record carries the target (CFG891). ½ appears only in menus or posits (CFG911).
- All five CFG894 doors have run without producing κ (CFG897, CFG898, CFG900, CFG905, census CFG891).
- A new exact ½ needs a second independent prediction (P_LEE 0.20, CFG894).
- The fine-structure constant α stays an input (CFG895: 0 derivations; doors CFG896, CFG899, CFG901, CFG906, CFG907, CFG910).

## 2. The cold sector as it stands

| piece | as recorded | status | lane |
|---|---|---|---|
| Rest state | Tethered cold energy's unique static rest state is the law (AG4, Lean 12/12). | Derived under the record's assumptions. | v2 S2 |
| Kinetic / fluid form | Moments of the record's kinetic equation with its relaxation term: Israel–Stewart pressure tensor, τ_π = τ_ff/(2α), η = pτ/(2α), ζ = pτ/(3α), characteristics u and u ± √3 σ, Kn = √2/(4α), Re = 4α. | Derived (sympy 11/11). It sets TIMING, not the settled profile. It sees baryons only through ρ_b, so it cannot select on kinematics (CFG919). Its bath σ_J² is not a universal floor (CFG876). | CFG638 |
| Deficit gate | Drift and relaxation act only where d = ρ_ph − ρ_c > 0. | Not established: Part A NOT DIAGNOSTIC as frozen, VG-1 UNDETERMINED (CFG639). Drift-only retention (CFG882) does not survive orbit mixing: the clump is ERODED in all 8 cells, gated t_50 = 105–148 Myr/α (CFG889). | CFG639, CFG882, CFG889 |
| Supply (catchment) | Supply = 5.364 × catchment baryons = 5.364 N M_b,gal, N = 1/f_ret; collisionless infall fills onto the law. | A settled edge at the galaxy's own share is EXCLUDED (CFG801). Primary KiDS range: DERIVED SUPPLY SUFFICES with no free parameter (CFG804; still after the unit fix, CFG902). All radii: FALLS SHORT; catalogue two-halo term PARTIAL (CFG903). | CFG801, CFG803, CFG804, CFG902, CFG903 |
| Settling dynamics | Radial collisionless shells under the law. | Deficits fill in the inner halo (CFG747, CFG748). Surpluses are expelled but overshoot into a deficit (CFG776). "Two-sided attractor" is not shown for surpluses (corrections note, item C5). | CFG747, CFG748, CFG776 |
| Mobility | One α(local variables). | INFEASIBLE IN THE DECLARED CLASSES: a galaxy's dense inner region must stay mobile to finish settling (CFG913). A history label is CONTRADICTED (CFG915). Lock-and-release is UNDERDETERMINED (CFG916). | CFG913, CFG915, CFG916 |
| Untethering (S4 / H-EX) | The cold share of expelled baryons is free; retained baryons tether only their own share. | Working rule with recorded failures: FAIL on all 318 eRASS1 clusters (CFG815); SHORT for early types (CFG811); negligible for dSphs (CFG822). No quantified S4 gate is available to pass (corrections note, item C10). | CFG809, CFG811, CFG815, CFG822 |
| Dwarf extra mass | Empirical finite clump: σ = 7.53 km/s, M_cl = 5.3e6 M_⊙ (canonical). | A description, not a mechanism. The law's source is baryons only in every formulation, so the clump mass is NOT DERIVED (CFG888). NOT UNIVERSAL (CFG880). No single compact or extended component fits all dwarfs (CFG884, CFG890). | CFG877, CFG880, CFG884, CFG888, CFG890 |
| Stiffness | −(γ/2)\|∇P\|², γ = 2πG L*². | Screens only; it cannot make the dwarfs' extra speed (CFG858). Its covariant completion is cosmologically harmless at background level (CFG897). | CFG858, CFG897 |
| Selector (open) | ∂_t f_c + v·∇_x f_c − ∇Φ_g·∇_v f_c = C_sel[f_c, ρ_b, χ]. | OPEN. Named as the unresolved object in the cold-energy equations inventory (`sol61_push/cold_production_2026_10_11/MASTER_COLD_ENERGY_EQUATIONS.md`, Supplement E, commit 33ec30852). That inventory marks the carrier as MODEL, the vacuum-acceleration relation as TARGET, and the bridge term S_bridge as not specified. | MASTER (read only) |
| Formation roadmap | Gate 1 receiver capacity; gates 2–5 rate, production + selector, profile + survival, broader closure (`sol61_push/ROADMAP_COLD_ENERGY_MECHANISMS_2026-10-19.md`, commit 9147fb3b9). | Gate 1 run: the bound outer envelope is BROKEN for the four dwarfs; only an escaping receiver remains (CFG918). Gates 2–5 not run. | CFG918 |

## 3. What passes, and what is partial

### 3.1 Rotators
- Where SPARC discs and dwarfs overlap (g_bar ≥ 1e-12 m s⁻², N = 8) they agree: +0.05 ± 0.07 dex (CFG828).
- SPARC's 56 small rotating dwarfs sit on the law: observed +0.032 dex (CFG845).
- No rotating cell carries an excess (CFG919).
- Raw SPARC with the stiffness term: canonical rms 0.1023 at L* = 1 kpc, against the 0.110 line (CFG832).
- Caveat: 13 of 170 SPARC galaxies need a non-stellar-population Υ at ≥ 3σ (AG4g, EXCESS; commit 01ca997a1). For 11 of 13 the
  cause is shape, not distance or inclination (AG4h, SHAPE DOMINATES; commit 2ec907467). A follow-up list, not a detection.

### 3.2 Isolated late-type lensing
- KiDS-1000 isolated blue lenses at the dwarfs' own g_bar (10^−13.3 to 10^−11.9 m s⁻²): A = 1.016 ± 0.086 over the law. The
  dwarfs' ×2.75 is excluded at 20σ (CFG829).
- FRAGILE by its frozen robustness rule: A 0.90 to 1.31 across variants, so "on the law" means within ~0.1 dex. The ×2.75
  exclusion holds at ≥ 12σ in every variant (CFG840).
- Without the lens catalogue's ΛCDM distances: SHIFTED, SAME CLASS; exclusion 18.4–21.3σ (CFG885, 9e6fb31b8).
- Scope: lensing probes 30–300 kpc. It tests the law's g(g_bar), not extra mass inside small systems (v3 clarification).

### 3.3 Cosmic shear (raw KiDS-1000 and DES Y3 ξ±, framework-native scoring)

| run | footing / inputs | KiDS class | reading | lane |
|---|---|---|---|---|
| T1x | canonical / inherited | CONSISTENT | pass, conditional on inherited ICs | CFG650 |
| T2x | alt / inherited | CONSISTENT | pass, conditional on inherited ICs | CFG650 |
| NC1x | canonical / native | CONSISTENT | A2 reading HOLDS; lifts the inherited-IC condition on the canonical footing only | CFG654-A2 (crit. fce7b081a) |
| NC2x | alt / native | CONSISTENT | A3 reading HOLDS (KiDS Δχ² −9.39, robust −5.69 to −12.85); lifts the inherited-IC condition on the alt footing | CFG654-A3 (crit. d2f59b90f; result 8e1f1763c) |

- DES Y3 is NOT DIAGNOSTIC in every run (T-OWN fails) except NC2x, where it is diagnostic and CONSISTENT (Δχ² −2.15).
- **The size of the advantage is amplitude-driven** (CFG909, 6e7ac5154). Over projection Ω_m 0.2806 to 0.3308 the inherited
  canonical Δχ² runs −0.94 to −11.93; NC1x runs −3.11 to −15.80; with the framework's own covariance NC1x gives −2.94. The class
  is ROBUST; the size is not. The framework run's lead comes mainly from lower lensing amplitude, not a shape preference.
- **Absolute fit:** NC1x χ²_min 144.68 / 108 (data-χ² p 0.024) against its control 154.76 (p 0.008). Both are worse than the
  inherited-input runs (T1x 136.6). The framework beats its control by suppressing small-scale power (P_grav/P_S0 0.949 at
  k = 1 h/Mpc, z = 0); it is not a good absolute fit (CFG654-A2). NC2x: χ²_min 145.38 / 108 (data-χ² p 0.023) against the
  same control; also not a good absolute fit (CFG654-A3).

### 3.4 CMB lensing (CFG917, eeb09d2a8)
- Part A (checklist item 2): SAFE ×3 (ΔA −0.0018 NC1x, −0.0017 T1x, −0.0016 T2x).
- Part B (raw Planck PR4 lensing, L 8–400): Δχ² −0.276 (NC1x), −0.088 (T1x), −0.085 (T2x). As frozen: NOT DIAGNOSTIC. Under
  post-hoc addendum A1 (187f895aa): CONSISTENT ×3.
- LOW POWER at box scales: the KiDS-excluded earlier model P1 reaches only +1.88. The gate neither threatens nor supports the shear
  pass. NC2x, scored blind after A1: SAFE / CONSISTENT under A1 (Δχ² −0.265, low power) (CFG654-A3).

### 3.5 Sealed CMB-lensing forecast (CFG927, seal d3bb2e4c6)
- theory-v2 against its control: ACT-like BLIND to L 3000 (≤ 2.2); SO-like DISCRIMINATING only to L ≈ 2000 (rule-dependent);
  S4-like DISCRIMINATING from L ≈ 700 and ROBUST from L ≤ 1000 (29–35).
- The noiseless ceiling at L ≤ 400 is only 0.82–1.00, so CFG917's low power is the multipole range, not Planck's noise.
- Caveats: the z > 1 continuation carries 45–78% of the difference; the noise models are optimistic. A forecast is not a
  measurement.

### 3.6 Lensing equals dynamics (slip bound, CFG847)
- s = |Φ − Ψ|/v_c² ≤ 2.2e-8 (dwarf), 3e-7 (MW), 1.3e-6 (group), 1.9e-5 (cluster), both footings.
- Conditional on a well-posed parent, and mostly by construction (the cold dispersion term). A covariant parent is not shown.

### 3.7 Partial or failing (stated as plainly as the passes)
- **Outer KiDS lensing of isolated galaxies:** all radii FALLS SHORT (+100.1 canonical after the unit fix, CFG902); with the
  catalogue two-halo term +40.72, not robust under stricter isolation (CFG903).
- **Cluster outskirts:** the law matches 1.2–3 Mpc (A_OUTER 1.01 ± 0.09 / 0.93 ± 0.08), but ΔΣ_OUTER scales as M_gas^0.90 ± 0.21
  against the law's 0.47: T2 FOLLOWS NEWTON, against the law (CFG687).
- **Wide binaries (2026 literature):** Cookson+26 CONSISTENT; Chae & Yoon 26's boost 1.15–1.20 is INCOMPATIBLE and kills the
  sealed construction if confirmed (CFG800); DR4 at the plan's N would most likely read such a boost UNDECIDED (CFG943).
- **a0(z):** see §0 item 7, §3.8 and obligation 10.

### 3.8 a0(z) from the framework's own BAO ruler (CFG689, results 6c064b83a)
Criteria 1c237145d, addenda 0db6da294 and bb21587be. Every number is from the committed `cfg689_summary.md`. This is the framework's
prediction for a0(z) from its own ruler. It is not a test of the framework against ΛCDM.
- **P1:** with the native r_d, BAO gives an absolute H(z): DEGENERACY BROKEN.
- **a0(z) band (primary rows only; replaces the CPL-chain M-DEC curve).** Primary = curvature free, DESI BAO + Pantheon+, native
  r_d, no CPL, no late-time CMB fit. Tracking √X = a0(z)/a0(0), median [68%]:

  | z | tracking √X | rival a0 ∝ H(z) | closest gap (dex) | 3σ tracking-vs-rival needs (dex) |
  |---|---|---|---|---|
  | 1.0 | 0.913 [0.762, 1.027] | 1.761 | +0.227 | 0.055 |
  | 1.2 | 0.925 [0.762, 1.048] | 1.987 | +0.272 | 0.072 |
  | 1.5 | 0.942 [0.706, 1.115] | 2.353 | +0.316 | 0.074 |
  | 2.33 | 0.909 [0.325, 1.212] | 3.490 | +0.453 | 0.084 |

  Beyond z 2.33 the band is extrapolated. No sample on the record reaches the 3σ errors (most CANNOT; one optimistic case LEANS).
- **θ* rows are NOT folded in.** The frozen K9 check failed (z* spread 1.24 > 1; D_M impact 9e-6, disclosed). Their tighter bands
  are reported only.
- **Dark-energy constancy (P2), flatness-sensitive.** Primary Δχ² 11.11/5, 1.97σ: CONSISTENT WITH CONSTANT. The flat mode gives
  2.10σ (HINT), so the reading is FLATNESS-SENSITIVE at the 2σ line. An "evolving" result would reject a constant Λ only; it never
  favours the framework.
- **Curvature (P0):** Ω_k +0.011 [−0.037, +0.059], FLAT CONSISTENT.
- **Decisive framework-vs-ΛCDM target (P6):** a kinematic a0 point at z ≈ 2.5 needs an error of 0.100 dex for 20:1 against ΛCDM's
  own DM14 law (primary; TARGET HARDER). z 2.5 lies beyond the last BAO node.
- **No-ΛCDM audit.** P4: INSIDE TESTED SPAN of DESI's fiducial. P5: framework vs Newtonian same-seed PM power, max|r| 0.0392,
  bound 0.00039: NEGLIGIBLE. B12 (no reconstruction) turns P1 to PARTLY BROKEN, and the post-hoc control B12c (DR1 post-recon)
  does the same, so it follows the DR1 isotropic data, not reconstruction.
- **What it rests on:** with SH0ES H0 and no CMB ω_c (B5c) the band collapses and P2 reads EVOLVING DE REQUIRED (3.45σ). The band
  rests on the CMB-anchored ω_c.
- **P3, report only (not a footing change):** native H0 67.70 [67.09, 68.31]; a0 at κ = ½ and z = 0 is 9.352e-11 against the
  footing 9.3603e-11. κ is fitted, so this is a consistency check, not a derivation.
- **Checks:** K1–K8 PASS; K9 FAIL as frozen (θ* only); K4 fails only in B9/B10 (no reading). MUTATE M1–M4 PASS.
- BAO cannot separate the framework from ΛCDM: both use the same background ingredients.

## 4. The open excess family

Every system with an excess is pressure-supported, and no rotator carries one. But pressure support alone does not set the amount
(CFG919, 8c46b7a2e). The family is OPEN and unexplained by the record.

### 4.1 Dwarfs
- With SFH-based stellar M/L, 25 of 28 independent dwarfs sit above the law, mean ln(σ_obs/σ_law) = +0.38, age-independent (CFG827).
- The excess lives below SPARC's floor: 21 dwarfs at g_bar < 1e-11.9 average +0.44 dex (CFG828).
- MW and M31 satellites carry the same excess: offset +0.055 ± 0.117 dex (CFG843).
- Isolated Local Group dwarfs carry part of it: E +0.194 ± 0.077 over the law, c −0.100 ± 0.091 below satellites, UNDECIDED (CFG874).
- It varies by dwarf: intrinsic scatter 0.380 in ln σ_x, NOT UNIVERSAL (CFG880, f055d83c4). That stands at central systematics
  (CFG887). Sextans alone needs ≥ 6.4e8 M_⊙ reaching ≥ 1.67 kpc (CFG884, fcc6529b8).
- Not an estimator artefact, and the record's EFE would RAISE the satellite excess by +0.48 dex mean: the quoted excess is a
  lower bound if the framework has an EFE (CFG925, 45e1c487a).
- Binaries do not make it (except possibly Carina's small one): Draco/UMi/Sextans reach 3.41/3.48/3.27 km/s at Q95 against a
  need of 7.81/7.40/4.88 (CFG892, d182623b4).
- No ≤ 2-parameter global description works; mass-like forms are preferred (CFG890, 9497ed064).

### 4.2 Red (spheroidal) lenses
- At the dwarfs' g_bar, with +0.123 dex on red stellar masses, the red–blue split is 4.0σ (A_red 1.45 vs blue 1.02) (CFG850).
- Not neighbours: the catalogue two-halo term explains f_env = 0.064 / 0.067 of the split (CFG912, a173537d9).
- **Possibly IMF:** a literature IMF α–σ relation removes the excess on both footings (split z 2.53 → 0.92), CONDITIONAL on discs
  staying near Chabrier; the same relation on discs is PARTIAL (CFG926 R5, a15a87fb7).
- H-EX does not produce it: +0.013 predicted vs +0.280 (CFG811).

### 4.3 Cluster cores
- 318 eRASS1 clusters: A_MID = 1.91 ± 0.12 / 1.75 ± 0.11, cold energy ×1.8 inside ~1 Mpc (CFG687).
- **CFG922 stands (e10ff47a2): EXCESS STANDS**, both footings and both kernels. Removing it needs extra concentrated baryons of
  2.24 / 1.84 × the gas inside 0.5 Mpc; with every testable component at its upper end MID is still Z +5.2 / +4.3.
- The middle-mass tercile is short ×1.64 (Z +4.6) on the H-EX rule (CFG815). Lock-and-release leaves MID failing as the law
  itself, 1.91 / 1.75 (CFG916).

### 4.4 What was tested against the family, 2026-10-18 to 2026-10-20

| lane | idea | class (as in the LEDGER) | hash |
|---|---|---|---|
| CFG838 | present-day tides vs the dwarf excess | NO TIDAL SIGNAL | — |
| CFG839 | pericentric tides in the framework's MW field | NO SIGNAL | — |
| CFG840 | robustness of CFG829 | FRAGILE (exclusion of ×2.75 holds) | — |
| CFG841 | SPARC shape test, simple vs quadratic | NOT DIAGNOSTIC | — |
| CFG842 | satellites capturing host cold energy (Liouville) | MARGINAL as frozen (rule flaw); capture cannot supply | — |
| CFG843 | MW vs M31 satellites | SAME | — |
| CFG844 | free cold core collapsed at assembly (H-PRIM) | SUPPORTS (weak), then excluded by CFG845 | — |
| CFG845 | H-PRIM vs SPARC small rotating dwarfs | H-PRIM EXCLUDED | — |
| CFG846 | excess vs gas-poorness | NO PATTERN (within SPARC) | — |
| CFG847 | gravitational slip | LENSING = DYNAMICS AT TEST PRECISION (conditional) | — |
| CFG848 | maximum-entropy tethered/free partition | No concentrated free core (WRONG SIGN / ILL-POSED) | crit. cf0aad80f |
| CFG849 | structure vs colour at low g | BOTH / DEGENERATE | — |
| CFG850 | red split vs stellar-mass bias | SPLIT SURVIVES | — |
| CFG851 | one excess law for spheroids | DSPHS ABOVE | — |
| CFG852 | gas loss via metallicity deficit | NO SIGNAL | — |
| CFG853 | fragment dynamical-friction transport | EXCLUDED | crit. cbe934afe |
| CFG854 | symbolic regression for the extra mass | LINEAR SUFFICES; power control FAILED, no formula validated | — |
| CFG855 | closed forms for 5.364 | ORDINARY | — |
| CFG856 | universal extra circular speed | SPARC-COMPATIBLE ONLY | — |
| CFG857 | size dependence of the extra speed | NO SIZE DEPENDENCE | — |
| CFG858 | stiffness producing the extra speed | STIFFNESS ONLY SCREENS | — |
| CFG859 | extra speed vs ultra-faints | OVER-PREDICTS UFDs | — |
| CFG860 | gas lost by stripping; lab bound | NOT GAS; NO LAB CHANNEL | crit. 219d4d5dc |
| CFG861 | unresolved binaries in classical dSphs | PARTIAL | crit. 4bcf7ce28 |
| CFG870 | cored extra component, joint test | JOINT FIT HOLDS (empirical, 2 numbers) | — |
| CFG871 | core set by σ through the law | LAW-LINKED CORE CONSISTENT (conditional, CFG888) | — |
| CFG872 | clump mass vs stellar mass | FLOOR-LIKE (canonical) | — |
| CFG873 | satellite vs small-system property | UNDECIDED (GAS-SENSITIVE) | crit. 30dd0b297 |
| CFG874 | all 11 isolated LG dwarfs pooled | UNDECIDED | crit. ac12da6c0 |
| CFG875 | host-distance slope | UNDECIDED | crit. bdc023e85 |
| CFG876 | universal cold-energy temperature floor | BROKEN | crit. 21fab6d76 |
| CFG877 | finite clump, no new parameter | PARTIAL (canonical); conditional (CFG888) | crit. 37fd77c59 |
| CFG878 | fragment mass from the record's bath | RECORD BATH EXCLUDED | crit. f39ef2490 |
| CFG880 | one clump σ for all dwarfs | NOT UNIVERSAL | f055d83c4 |
| CFG881 | clump mass SPARC can hide | PARTIAL | 84b6202ce |
| CFG882 | clump retention, drift only | RETENTION REQUIRES THE GATE (superseded by CFG889) | f370e5577 |
| CFG883 | clumps in globulars | MIXED | 89495cac8 |
| CFG884 | Sextans' two populations | CLUMP SHORT, EXTENDED MARGINAL | fcc6529b8 |
| CFG885 | lensing lanes without ΛCDM distances | SHIFTED, SAME CLASS | 9e6fb31b8 |
| CFG886 | 5.364 and f_ret without Planck | 5.364 RECOVERED / NOT PINNED; f_ret MIXED | 5614bd0a5 |
| CFG887 | σ systematics behind CFG880 | CFG880 STANDS | — |
| CFG888 | clump self-gravity from the action | LAW SOURCE = BARYONS ONLY; NOT DERIVED | 753cf3d98 |
| CFG889 | deficit gate with orbit mixing | INCONCLUSIVE as frozen; CLUMP ERODED | 52812d58b |
| CFG890 | best ≤ 2-parameter description | NONE WORKS; MASS-LIKE PREFERRED | 9497ed064 |
| CFG892 | forward-modelled undetected binaries | PARTIAL (reached: Carina) | d182623b4 |
| CFG902 | catchment supply rerun, declared units | NO CLASS CHANGES | 176331be7 |
| CFG903 | catalogue two-halo term, no free amplitude | PARTIAL | ec10af603 |
| CFG909 | ΛCDM inputs in the shear scoring | ROBUST (class); size amplitude-driven | 6e7ac5154 |
| CFG912 | red/blue split vs two-halo term | NOT ENVIRONMENT | a173537d9 |
| CFG913 | one mobility law for mergers, galaxies, clumps | INFEASIBLE IN THE DECLARED CLASSES | f5b527d5e |
| CFG914 | one density threshold for the excesses | NO COMMON ORDERING | 7c0324ad4 |
| CFG915 | history-label mobility (H-POP) | CONTRADICTED | 9e1915dcb |
| CFG916 | lock-and-release (H-LR) | LR-x CONTRADICTED; LR-c UNDERDETERMINED | bca1e0573 |
| CFG917 | CMB-lensing gate | SAFE ×3; NOT DIAGNOSTIC as frozen; CONSISTENT ×3 under post-hoc A1 | eeb09d2a8 |
| CFG918 | outer-envelope E/J receiver capacity | BOUND ENVELOPE EXCLUDED (Sextans; Draco and Sextans in G1); escape permitted | bb9b20525 |
| CFG919 | pressure support as the selector | SELECTOR CONTRADICTED (FRAGILE) | 8c46b7a2e |
| CFG920 | ×4.3 formation baryon loss vs chemistry | UNDERDETERMINED | b2d0bff6a |
| CFG921 | five one-constant selectors | NONE SURVIVES | f4c87a342 |
| CFG922 | cluster-core excess vs baryon census | EXCESS STANDS | e10ff47a2 |
| CFG923 | late binding vs the framework's clock | canonical CONTRADICTED; OVERALL UNDERDETERMINED | ec6316d0f |
| CFG924 | aperture-mass recheck of an earlier lane's condensed masses (owner-started) | the earlier hot-group lensing verdict moves: BOTH EXCLUDED → NOT DIAGNOSTIC (FRAGILE: gas extent) | 8e7374552 |
| CFG925 | reframings A: Jeans estimator, self-sourcing, EFE | NO EFFECT; WORSENS; WORSENS | 45e1c487a |
| CFG926 | reframings B: fossil a0, IMF α–σ, ESD estimator | R4 NO EFFECT / WORSENS (rival PARTIAL); R5 RESOLVES the red-lens excess (conditional); R6 NO EFFECT | a15a87fb7 |
| CFG927 | sealed high-L CMB-lensing forecast | SEALED FORECAST | 4f7b35baf |
| CFG928 | re-grade of CFG921's posits with IMF-corrected red lenses, clusters as a separate class | P2 velocity-space capture SURVIVES the galaxy-scale facts on both footings (post-hoc-motivated, IMF-conditional, fragile) but FAILS clusters; P1, P3, P5 FAIL; P4 UNDERDETERMINED | 82a69be8f |
| CFG929 | small reframings for the cluster-core excess | none resolves it (four reframings: no effect, bracket-dependent, or breaks something) | 1f1b87ce8 |

## 5. What any completion must still supply

1. **A selector for pressure-supported systems that costs ≤ 1 constant.** It must give the dwarfs their varying excess, the
   cluster cores ×1.8 rising with g_bar, and the red lenses (unless obligation 3 removes them), while leaving rotators and blue
   lenses on the law. The record's kinetic equation cannot do it (CFG919). *Decisive test:* CFG921's constraint intersection on
   both footings (all five tested posits FAIL), plus CFG880's per-dwarf scatter and CFG884's Sextans.
2. **Binding and retention of the dwarf extra mass inside the record's equations.** *Decisive test:* a kinetic run in CFG889's
   setup that keeps half a clump for 12 Gyr at the galaxy side's α ≳ 0.5; then the roadmap's gates 2–4 (rate, production and
   selectivity, profile and survival) on Draco, Sextans, Fornax and Leo I with one model.
3. **The red-lens IMF condition.** *Decisive test:* the IMF relation that removes the red-lens excess must leave blue (disc)
   lenses on the law (now PARTIAL, CFG926), backed by an independent IMF measurement for the two lens populations.
4. **The cluster-core excess and the cluster outer slope.** Extra concentrated mass of about twice the core hot gas (CFG922), the
   outer ΔΣ ∝ M_gas^0.90 (CFG687) and the middle-mass tercile (CFG815). *Decisive test:* the 318-cluster eRASS1 stack on both
   footings. CFG929 (1f1b87ce8): none of four small reframings resolves it; the excess is real mass the law does not supply.
5. **A derivation of κ = ½.** It must bring in c (CFG893) and carry no π (CFG891). *Decisive test:* a second, independent
   prediction from the same derivation, confirmed (CFG894's look-elsewhere rule).
6. **Derivations of 5.364 and f_ret.** *Decisive test:* a framework-native f_ret(M) that reproduces the census and closes the
   all-radii KiDS shortfall (CFG902, CFG903); a 5.364 that does not rest on a constant-ρ_DE background (CFG886).
7. **The alt-footing native shear (NC2x): MET (2026-10-21).** CFG654-A3 HOLDS (KiDS Δχ² −9.39, CONSISTENT); blind CMB lensing
   CONSISTENT under A1. The native shear pass now holds on both footings, with the same caveats (absolute fit, amplitude-driven
   size, the engine's missing physical parent).
8. **The remaining inherited inputs** (Planck ΛCDM-chain column, H0 from θ*, massless ν, M2 cooling inputs; CFG654-A2).
   CFG689 now gives a native-ruler background and H0 (67.70), but its band rests on the CMB-anchored ω_c (B5c). *Decisive test:*
   none frozen yet for the Planck column, ν mass or cooling inputs inside the shear runs.
9. **The relativistic parent.** Lensing from one covariant action. The bridge term is unspecified (MASTER), the slip bound is
   conditional on a well-posed parent (CFG847), and no candidate passes the one-action contract (CFG678: B1, B3/A2, C3, D2
   unpassed). *Decisive tests:* CFG678's gates; observationally, S4-class high-L CMB lensing (CFG927).
10. **Which dark-energy quantity a0 reads, and a0(z).** Three readings are in use (CFG911). *Decisive tests:* the ALMA gas at
    z 1.4–2 (CFG571) and a kinematic a0 point at z ≈ 2.5 with an error of about 0.100 dex (CFG689 P6).
11. **L*.** Derive it, and resolve the dSph conflict (CFG821, conditional). *Decisive test:* Gaia DR4 under CFG800's rule.
12. **A quantified untethering (S4) gate.** None is available to pass (corrections note, item C10); H-EX fails on all 318
    clusters (CFG815). *Decisive test:* a new S4 gate frozen before its data. Whether to freeze one is the owner's decision.

## 6. Dated external tests and sealed predictions

| date | data | what is sealed or frozen | kills or decides | lane / seal |
|---|---|---|---|---|
| 2026-11-06 | ALMA U4_27928 (z 1.42) | required gas per model and a0 branch, both footings | conditional on CO V_c at 8.3 kpc; < 200 km/s tests nothing | CFG571 (259f7825c) |
| 2026-11-28 | ALMA GS4_24110 (z 2.0, [CI](2-1) + dust) | framework needs log M_gas ~9.1–10.7; both rivals FLOOR in every branch | single-disc demonstration, no exclusion; routes never averaged | CFG571 (259f7825c); scoring plan CFG809 (966d50a87); horizon branch CFG778 |
| 2026-12 (12-02 in the 10-14 file) | Gaia DR4 wide binaries | Newtonian; any boost obeys γ_v − 1 = ½ (s/L*)², envelope 8.9e-4 at 50 kAU at L* 5.754 pc (≥ 17× smaller at L* ≥ 24 pc, CFG820) | KILLED iff R − 1 ≥ max(0.01, 3σ_R), σ_R from the pairs in R; else UNDECIDED (CONSISTENT unreachable, σ_R ≥ 0.02). At the plan's N (~2,100 pairs in R, σ_R 0.075) a kill needs R ≳ 1.22: a full MOND-size boost is caught ~half the time, a 1.15 boost almost never; reliable at ~7,000 pairs (MOCK, CFG943; owner decision 2026-10-21) | CFG740 (crit. c4f88c6ee), CFG800 |
| no date set | JWST GO 12088 (J0946 perturber) | Q = M_lens/M_b ≤ 1.08/1.09 inside 0.3 kpc | EXCLUDED if Q_obs > 3 Q_max | CFG672 (sealed 52f4363bf) |
| data released (used by CFG674) | JWST GO 8281 (B1938 A) | stars F277W 26.4–29.6/29.8 AB | EXCLUDED if the 2σ limit is fainter than 30.8/31.0; own photometry NOT DIAGNOSTIC (can confirm, never exclude) | CFG673 (crit. a0b9c9bf7), CFG674 |
| no date set | a kinematic a0 point at z ≈ 2.5 | the native band of §3.8 | needs an error of 0.100 dex for 20:1 against ΛCDM's own DM14 law; no public sample yet | CFG689 (6c064b83a) |
| future surveys | high-L CMB lensing | theory-v2 vs control: S4-like DISCRIMINATING from L ≈ 700, ROBUST from L ≤ 1000; ACT-like BLIND | a forecast, not a measurement | CFG927 (seal d3bb2e4c6) |
| any | Cavendish repeat, deep-space probe, old tidal dwarf | unchanged from the 10-14 file §2 | as sealed there | CFG772, CFG774, CFG441 |

## 7. Do-not-cite and standing wording rules
- **κ = ½ FITTED.** Never "derived". CFG908 lists 200 lines in 142 tracked files that still say κ is derived, and CFG904 lists the
  files that present 0.4607 as coefficient-free. Corrections to public files are the owner's call.
- **Not theory closed.** Never write "theory closed" for any state of this record.
- **Never say "the data favour the framework".** CONSISTENT is not a preference. A class that only requires "no worse than the
  control" cannot favour anything.
- **Quote the shear result as a class** (CONSISTENT, inherited and native, canonical; inherited, alt), never as −7.7 or −10 (CFG909).
- **Footings never pooled.** The footing ratio 1/√Ω_Λ is an identity, not a finding (CFG835 withdraws it).
- **Raw data and framework-native verdicts only.** No HMcode, BAHAMAS, ΛCDM mass function or "within X% of ΛCDM" in a verdict.
- **CFG917's gate PASS needs post-hoc A1.** Quote "NOT DIAGNOSTIC as frozen, CONSISTENT under A1, low power".
- **CFG927 is a forecast.** Never cite it as a measurement.
- **CFG926 R5 is conditional.** Never say the red-lens excess is solved. **CFG926 R4** is evidence about a0(z), never a rescue.
- **CFG871/877/878 clump formulas are conditional** on an unwritten coupling (CFG888). **CFG882's retention** is superseded (CFG889).
- **CFG829's "on the law"** means within ~0.1 dex (CFG840). **"Satellite property"** is withdrawn (CFG873).
- **CFG844's SUPPORTS** is excluded by CFG845. **CFG851's g† ≈ a0** is a distance-dependent coincidence flag (CFG885).
- **CFG674's point estimate** is never cited. **CFG833's footing "structural finding"** is withdrawn (CFG835).
- **BAO cannot separate the framework from ΛCDM** (CFG689). An "evolving dark energy" reading rejects a constant Λ only. CFG689's
  a0(z) band is a prediction, not a test; its θ* rows are not citable as folded results (K9 failed as frozen).
- **No dark matter particle.** "Cold energy"; its mass is required.

## 8. Placeholders: PENDING (fill when committed)
Do not use any number for these until the lane's README result and LEDGER row are committed. None is invented here.

- **P1. NC2x, CFG654-A3: FILLED (2026-10-21; result 8e1f1763c).** KiDS CONSISTENT, Δχ² −9.39 against NCS0 (robust −5.69 to
  −12.85); A3 reading HOLDS; χ²_min 145.38 / 108 (data-χ² p 0.023) vs 154.76 (p 0.008); DES −2.15 CONSISTENT (diagnostic); CFG917 blind CMB
  lensing SAFE / CONSISTENT under A1 (Δχ² −0.265, low power). CFG909's NC2x re-score (reported sensitivity, no verdict weight)
  goes in CFG909's README when it lands.
- **P2. CFG928: FILLED (82a69be8f).** Re-grade of CFG921's five posits with the IMF-corrected red-lens fact (CFG926 R5) and
  clusters as a separate class: P2 velocity-space capture survives the galaxy-scale facts on both footings, but it is
  post-hoc-motivated, conditional on old spheroids being bottom-heavy and discs not, and fragile; clusters still need a second
  ingredient. P1, P3, P5 FAIL; P4 UNDERDETERMINED. Best of 20 tried, not evidence for P2.
- **P3. CFG929: FILLED (1f1b87ce8).** Four small reframings of the cluster-core excess with zero new constants: none resolves it.
- **P4. CFG689 BAO fold-in: FILLED (no longer pending).** It landed in 6c064b83a (LEDGER row, README, `cfg689_summary.md`) and is
  folded in as §3.8, following its handoff (07259c4c6) and the dated note in v3 (f39b66063). Primary rows only. The θ* rows are
  held back because K9 failed as frozen; the handoff's rule is to report a failed check as a failure, so §3.8 does.
- **P5. CFG924: FILLED (8e7374552).** The data re-check of the earlier hot-group lensing test (eFEDS groups) with CFG922 A1's total-flux census moves its verdict: both models go from EXCLUDED to NOT DIAGNOSTIC (FRAGILE: gas extent), on both footings.

## Sources (read only)
- `THEORY_CANONICAL_2026-10-18.md` (v3 and all its notes), `THEORY_CANONICAL_2026-10-16.md` (v2, b7b3ba9a7),
  `THEORY_CANONICAL_2026-10-14_CORRECTIONS_2026-10-16.md`, `THEORY_CANONICAL_2026-10-14.md`.
- `LEDGER.md` rows CFG820 to CFG927, CFG654-A2 and CFG689; the 920–929 reservation row for CFG928/CFG929.
- CFG689: README and `cfg689_summary.md` (6c064b83a); its fold-in note at the bottom of v3 (f39b66063).
- READMEs of CFG650, CFG909, CFG913 to CFG927, and the RESULT section of the README behind CFG654-A2.
- `sol61_push/ROADMAP_COLD_ENERGY_MECHANISMS_2026-10-19.md` (9147fb3b9) and the committed
  `sol61_push/cold_production_2026_10_11/MASTER_COLD_ENERGY_EQUATIONS.md` (33ec30852). Another agent's files: cited, not edited.
- `qwen_claude_field_theory/papers_2026/PAPER55_low_acceleration_map_2026.tex` (1bf444040).
- `argon_push/AG4g_galaxy_pull_census/README.md`, `argon_push/AG4h_pull_systematics/README.md`.

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.

---
**Correction, 2026-10-23 (CFG961 f7b966292, independent check of what_is_time WT-02 9b3d77382; corrects the 2026-10-20 CFG938 note, whose text is left as written).**
- **Well-posedness holds only on static media.** That case stands: the dispersion relation, slip ≤ 1.54e-5, and the law to 2.2e-16.
- **On FRW the parent is Hadamard ILL-POSED.** S1d's constraint operator turns (χ, λ) into a forward/backward heat pair, and λ becomes χ's conjugate momentum. Growing modes have Re σ = c²k²/(3|H|), for both signs of H, at z = 0 and 10, with gravity off and in full GR.
  - The mode is PHYSICAL, not a multiplier artefact: λ's gradient drives the medium (1.05×), the Bardeen potential responds, and in GR the λ equation follows from the Hamiltonian and trace-ij equations.
  - The intrinsic-Laplacian repair needs an explicit mean-density subtraction (under test in WT-08).
- **c_T is not structurally c (A5 withdrawn as structural).** δ(c_T²/c²) = (3/2) L*² [u_⊥² + (u_∥ + ∂₀χ)²]/c⁴. The FRW clock term ∂₀χ̄ = c Ω_c H/2 dominates GW170817's path average, which gives c_T/c − 1 = 3.9e-19 (L* = 24 pc) to 6.8e-16 (1 kpc).
  - This passes, but caps L* ≲ 1.0 kpc (0.76 kpc at the measured distance).
  - If the medium exists early, the tensor kinetic coefficient turns negative before 1 + z ≈ 2.7e5 to 1.1e7 (sol61 audit a67f9ed9c).
- **The hidden cosmic clock is confirmed:** 1.1e-3 a₀ at 370 km/s. Not visible in SPARC, wide binaries or the Solar System; undecided against the KiDS tail ends.
- PAPER57 (10.5281/zenodo.23532885) states "linear well-posedness". A v1.1 correction is drafted in CFG961_wt02_verification/CORRECTION_PAPER57_v1.1_DRAFT.md and awaits the owner's go.

---
**Dated note, 2026-10-23 (CFG963 e96c21a87): the native shear pass is carried by gas expulsion.**
- **M3 does it.** The KiDS lead of theory-v2 over NCS0 (NC1x −10.08, NC2x −9.39) comes from the census gas expulsion M3, which the Poisson control does not apply. Plain gravity + the same M3 scores −11.87 vs NCS0.
- **Against that feedback-matched control** the engine scores +1.78 / +2.47, within noise, and the capped cold-sector rules alone (M1+M2) score +2.66.
- **Correct reading of the shear tile:** the capped cold sector does not overproduce structure (unlike the uncapped settling engine's +68.7), and gas expulsion lowers power. KiDS cannot tell the framework's cold sector from plain gravity + feedback. It is not a preference for the law.
- The engine-parent problem is therefore not load-bearing for the shear result.
- **Rule for every future engine score (v3, L1 khronon included):** report vs NCS0 first, then vs a control with the same baryon physics.
