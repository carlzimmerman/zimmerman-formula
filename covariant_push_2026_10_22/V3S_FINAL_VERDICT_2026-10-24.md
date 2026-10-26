# v3s: final verdict (2026-10-24)

This document closes the v3s investigation. The theory is frozen as stated below. Every thread now has a final status: it
passes, it fails with a named mechanism, or it waits on dated data. No further lanes are opened on the v3s family unless a
new forced kernel appears; data due on fixed dates (§5) is scored against the sealed predictions as it arrives.

Freezing the investigation does not mean the theory passes; §3 says where it fails. κ = ½ FITTED. Footings 9.3603e-11 /
1.1312e-10 m/s², never pooled. No dark-matter particle. Nothing here says the data favour the framework. Full derivations,
equations and Lean names: `V3_FULL_PICTURE.md`. Every explanation the record has tried: `rebuild_2026_10_22/X0_explanation_map/MAP.md`.

## 1. The frozen theory

    S = (c³/16πG) ∫ √−g [ R − 2 J_x(Y) + 2 K(Q) ]  −  (γ_L/2) ∫ √−g [max(D_i P^i, 0)]²  +  S_m[g, matter]

    J_x = Λ − 2a₀²[y − ln(1 + y)],  y = √Y/a₀      (static limit: AQUAL, μ(x) = x/(1 + x))
    K(Q) = μ_K²(Q − 1)²,  μ_K < 0.1 Mpc⁻¹            (isolated-galaxy lensing bound, S4)
    γ_L = K L★²/2,  L★ ≥ 21.7 / 22.9 pc              (outer globulars, D10)
    a₀ = κ c √(G ρ_Λ) = c² √(Λ/32π),  κ = ½ FITTED

**Inputs:** κ (fitted), L★ (a lower bound only), the cold-dust abundance (an initial condition), and μ_K (bounded above
only). The β K² caustic completion (C1) is **not** part of the frozen theory; its status is in §4.

## 2. What passes (each result reproduced by the coordinator; Lean where named)

| test | result | evidence |
|---|---|---|
| The a₀-line and RAR form | forced: slope 1, intercept 0 | LEAN `EQB_A0LINE_uniqueness` |
| SPARC RAR | rms 0.054 / 0.054 dex, one Υ per galaxy, EFE solved for 109 (χ² line fails: conditional) | P4 |
| MeerKAT a₀ | +0.032 dex from SPARC's, same recipe | P4 |
| Isolated groups, isolated LG dwarfs | +0.010 / −0.010 dex; +0.06 / +0.02 ± 0.08 dex | P4, X1 |
| Tidal dwarfs, DF2/DF4 | Newtonian in their host, as predicted | U1 |
| Solar System (screened) | all 24 Cassini cells pass by 4.8e7–5.1e9 (the unscreened law fails) | C6, E2 |
| Gravitational waves, binary pulsars | c_T = c; ≤ 3.2e-14 of the double pulsar's precision | C8, P3 |
| Static black holes, neutron stars | shifts ≤ 2.9e-11 | P3 |
| Constraint algebra; saddle health | closes with 3 DOF; switched stiffness well-posed and statics unchanged (qualifiers in V3_FULL_PICTURE §4.7) | Codex review, X3, LEAN `switched_*` |

## 3. What fails, with the mechanism

**The one mechanism.** v3s has one cold field, and kinematics fix it to be the field that carries the law (α ≡ 1; X6,
LEAN `coupling_one_is_law`). It cannot be weightless in isolated galaxies, weigh in clusters and hosts, and grow like dust
from z ≈ 1100 all at once. A separate dust that does those things double-counts in galaxies: it is CDM under another name.

| failure | numbers | lanes | status |
|---|---|---|---|
| **Cluster cores** | 1.5–1.7 × the law in 0.3–1 Mpc; Z 4.5–5.5 all-source, 4.1–5.0 selection-corrected; no excess in the lightest third | F1, X2, X7, X11, X13 | FAIL (data robust; no μ_K fixes it, S4) |
| **Linear growth / CMB** | σ₈/σ₈,dust 0.003–0.005 at galaxy-allowed μ_K; nonlinear J_x does not restore it (ρ_NL ≈ −0.05, converged 128³–384³) | F3, X4, L1 | FAIL (512³ production pending, §5) |
| **No radiation era** | stiff a⁻⁶ partner; BBN needs μ_K ≥ 1.84e8 h/Mpc | Q6, Q7 | FAIL for the literal K |
| **Hosted dwarfs** | hosted ⇒ Newtonian (T3); six hosted sets disagree at ≥ 5σ (Antlia II 24σ, MW ultra-faints 12.6σ, …) | U1, X1 | FAIL |
| **Milky Way disc** | K_z(1.1 kpc) 92–97 vs 66.4 ± 2.2; outer slope excluded (Z −3.9 to −4.6) | P4, S3, X5 | FAIL (generic to the μ-law family) |
| **Caustics** | the single-stream khronon folds generically (analytic, X14; self-consistent axisymmetric, peer review cc727f275c); no completion without a new constant | X8, X10, X14 | STRUCTURAL GAP (§4) |

Three of these (clusters, the CMB's third peak, the Milky Way joint fit) are generic to every MOND-class theory: no
rule-compatible framework in the literature claims a clean pass (MAP §1).

## 4. The caustic completion (β K², C1): final status

| test | result | lane |
|---|---|---|
| Unique survivor of nine completion classes | yes; window β ∈ [2.0e-6 / 2.2e-6, 1.0e-5] at μ_K = 0.1 Mpc⁻¹ | X14 |
| Preferred-frame PPN | PASS: α₁ = α₂ = 0 at PPN order for every β; residuals ≤ 3.6e-10 | X15 |
| Binary pulsars | PASS on a condition: |s₁ − s₂| < 7e-7 (J0737), strong-field sensitivity uncomputed | X16 |
| Galaxy/cluster selector | NO (WRONG SIGN): inert in statics, wrong mass ordering in motion | X17 |
| Galaxy dynamics | works only for motion slower than c_A (160–770 km/s at the window top) | X15, X17 |
| Linear growth on forest scales | overshoots at k ≳ 1–3 h/Mpc for every β (linear) | X17 |
| Forest after saturation | **UNDECIDED** under the frozen rule: the linear khronon ODE breaks X14's flux cap at early times (last at z ≈ 200–500, even at β = 0), so it is outside its own validity. Ignoring the cap, the forest fails in 80/80 cells and no β puts both σ₈ and the forest inside the lines. Deciding it needs a nonlinear code started from a cap-consistent state | X18 (71e86472ea / c9832d656f; coordinator rerun identical apart from timing) |

C1 cures a health problem. It does not touch the mechanism in §3. Every test that could be graded passes or is conditional; the one test X18 could not grade (the forest) fails in every cell once the cap is ignored.

## 5. What can still change the verdict (dated, sealed in advance)

| data | date | sealed prediction |
|---|---|---|
| ALMA U4 / GS4 | 2026-11-06 / 11-28 | addendum F |
| Gaia DR4: wide binaries, MW | 2026-12-02 | `SEALED_V3_MW_DR4.json` (S3), C6 |
| L1 512³ production (only rung KiDS can score) | in the compute queue | the converged ladder says ρ_NL ≈ −0.05: it does not restore growth |

## 6. The verdict

- **As a galaxy-scale law, v3s is complete and passes:** the a₀-line, SPARC, isolated systems and Solar-System screening,
  with a well-posed covariant action.
- **As a theory of gravity and cosmology, v3s fails:** clusters, growth/CMB, the radiation era, hosted dwarfs and the Milky
  Way disc. Most of these follow from one mechanism (α ≡ 1, one field).
- **What a successor needs:** a gravitating cold sector that clusters like dust from z ≈ 1100, weighs in hosts and clusters,
  and adds nothing in isolated galaxies. That needs a selector between galaxy and cluster scales. Nothing in the record
  provides one: density-keyed pressure is excluded by the μ-pincer, and C1's acceleration-keyed sound speed is inert in
  statics (X17).

## 7. The missing piece: what the data allow (X19, 2026-10-24)

`rebuild_2026_10_22/X19_selector_rank_test` (8960ea2285 / 0fc9bade54 / a9ec701f5b; coordinator rerun identical apart from RSS) ranked every measured system class by eleven catalogue variables. The variables were baryon mass, velocity dispersion or temperature, density, internal acceleration x, host field e, potential depth, hot-gas fraction or kT, orbit count, environment density, and the hosted flag. The test was whether any single variable puts every class that needs extra cold mass on one side and every class that needs none on the other.

**Verdict: NO LOW-DIMENSIONAL SELECTOR, on both footings.** No single variable separates the classes, and no axis-aligned pair does.
- The variables that split light from heavy clusters (M_b ≈ 8e12 M☉, |Φ|/c² ≈ 1.7e-6) put the compact hosted dwarfs (MW ultra-faints, bright M31 dSphs) on the wrong side.
- The variables keyed to being hosted pull in Crater II, the tidal dwarfs, DF2/DF4 and the UMa members, which need no extra, and they miss the clusters and the cosmic background.
- The nearest miss is the pair (M_b, |Φ|), which fails on one class.
- Against the isolated law, Crater II, Antlia II and the Coma UDGs do not need extra. Their large "excess" exists only against the v3s EFE baseline.

**Reading.** The data ask for at least three separate ingredients:
- something that makes compact hosted dwarfs heavier, but not diffuse or tidal ones;
- a switch between about 4e12 and 1e13 M☉ of cluster baryons (the cluster mass trend itself is only marginal, X7);
- a cosmic dust.

No single new field or switch can supply all three. So the theory cannot be closed by adding one ingredient, and that rules out the whole one-selector family at once.

## 8. The three requirements, examined one by one (X20–X22, 2026-10-24; every coordinator rerun identical apart from timing)

| requirement | lane | finding |
|---|---|---|
| Extra mass in hosted dwarfs | `X20_hosted_dwarf_requirement` (8a6247efea / 9d459cb575); `X20_hosted_dwarf_disequilibrium` (87b6832e84 / bd736c128e; a peer lane; two lanes share the X20 id, so cite full folder names) | **A graded trend, not a switch.** Against the isolated law the extra rises toward low M★ and small r_half (ρ_S ≈ −0.60, 6–7σ, both footings), not toward compactness (Σ, x ≈ 2.7σ). No variable separates the systems one by one. The frozen verdict is UNDECIDED: the footings' top variables, M★ and r_half, are tied. The trend survives every measurement variable on disk, but an uncorrected binary or non-equilibrium floor in σ at 2–4 km/s would mimic it; multi-epoch σ for the ultra-faints decides. **The disequilibrium lane tests that caveat and rules it out on both footings.** Tides are small (median g_tid/g_iso 0.012, no correlation with the extra), and the τ ≤ 0.1 subset is still +0.48 / +0.45 dex, Z 5.8 / 5.4. Binaries would need σ × 0.41–0.81, but after X1's correction they leave room for only ≥ 0.82 (median 0.92). So the hosted-dwarf extra is real (τ uses the current distance, a lower bound on the pericentre stress). The large hosted excess of Crater II and Antlia II exists only against the EFE baseline |
| A cluster switch | X21_cluster_switch_anatomy (a48f6d5e08 / 3aa4f07b58) | **No real switch.** The tercile step comes from cutting on MGAS500; unbinned MGAS500 gives only ~1.9σ, and the best break is not significant once every break location is allowed for. The excess rises smoothly with KT (≈ 3σ; 1.7σ at fixed MGAS500), L500 and richness. It does not track the BCG, core concentration or stellar fraction. **Baryon budget INSUFFICIENT:** generous omitted baryons fall short ×4–7, and their trend with mass runs the wrong way |
| A cosmic dust | X22_cosmic_dust_window (a2b532e3c6 / 5c7114f508 / e1e3785cc5) | **No gravitational window.** The forest needs dust-like clustering down to λ_hm ≈ 0.42 Mpc/h (M_hm ≈ 5e9 M☉). The median SPARC galaxy collapses from 2× that radius and 10× that mass, so a forest-passing cold component falls into galaxies (median capture 0.76, against a tolerance of 0.20 / 0.03 of the fair share; the limit is set by the Υ window). A window opens only with non-gravitational exclusion: energy injected after z ≈ 2, raising c_s to ≈ 190–200 km/s (≈ 2V), universally or only in collapsed regions. That would keep it bound in every cluster tercile and empty the hosted dwarfs. The record has no action for either |

**Reading.** The decisive constraint is the cosmic dust. Growth and the forest need a cold component that clusters on the scales galaxies form from, and isolated galaxies leave no room for it unless new non-gravitational physics heats or expels it after z ≈ 2. The cluster excess is real, smooth and too large for known baryons. The dwarf requirement is a faintness trend that multi-epoch spectroscopy could shrink. The missing piece of the v3s family is therefore not a selector. It is a late-time, non-gravitational energy source in the cold sector, and nothing in the record or the literature provides an action for one.

**Late heating graded** (`X23_late_heating_graded`, 6ec6b89807 / 9c54fae62e, a peer lane; coordinator rerun identical apart from timing; a second folder, `X23_late_heated_cold`, also carries the X23 id). It uses X22's own hydrostatic profile at c_s 190 / 201 km/s. **LATE HEATING FAILS on both footings.** The frozen rule's literal reading is UNDECIDED, from a grading artefact on SPARC small rows, disclosed in A1.
- Hosted dwarfs get none of it: ≤ 8e-4 dex against +0.21 to +0.64 observed.
- Clusters over-capture: T2/T3 +1.0 / +1.2 against +0.27, and T1 is predicted EXTRA where none is measured.

**The hard wall is the hosted dwarfs.** Their extra is real: not tides, not binaries (`X20_hosted_dwarf_disequilibrium`). Yet every mechanism that keeps cold mass out of isolated galaxies removes it from these dwarfs too, which is a sign conflict. Isolated SPARC galaxies of every size need none; compact faint dwarfs inside hosts need +0.2 to +0.6 dex. Whatever supplies it must act on hosted faint systems and not on isolated ones, and X19 found no catalogue variable that orders that.

**The dwarf requirement, reframed** (`X24_dwarf_velocity_floor`, 7a79903c3f / 19d31a99d9, a peer lane, post hoc and disclosed; coordinator rerun identical apart from timing; `X24_vacuum_heated_cold` is a different lane).
- **Being hosted adds nothing.** At matched M★ (log 5.4–6.8), hosted minus field E is +0.04 / +0.02 (Z 0.27 / 0.16). Field dwarfs show the same rise toward low M★ (Spearman −0.73; Leo T +0.41, Phoenix +0.40). X19's field class read NONE only because its members are heavier.
- **A velocity floor fits most of it.** σ² = σ_iso² + c₀², with c₀ calibrated on the 13 field dwarfs only, gives c₀ = 4.6 [4.0, 5.1] / 4.1 [3.4, 4.7] km/s.
  - Out of sample on the hosted dwarfs, χ² falls 637 → 217 (canonical) and 559 → 195 (alt).
  - Bright M31, M31 others and MW classical are reproduced.
  - The MW ultra-faints are overshot (Z −3.9 / −3.0), and Crater II and Antlia II get worse.
  - SPARC moves by 0.002 dex.
- **So the dwarf rows are not a selector problem.** They are a single small-scale velocity constant of about 4–5 km/s, not yet derived. That removes the hosted-dwarf argument against late heating; clusters and growth are unchanged.

**Pericentre tides** (`X25_dwarf_pericentre_tides`, d4827bece5 / 5a754eb2e2; coordinator rerun identical apart from timing): **TIDES RULED OUT AT PERICENTRE** for the 31 MW ultra-faints, the only hosted dwarfs with orbits on disk. On both footings:
- Spearman(E, log τ_peri) is −0.17 / −0.16, and a heating proxy gives a null.
- The weak-stress subset (τ_peri ≤ 0.1) is still +0.60 / +0.55 dex, Z 4.8 / 4.4.
- The M★ trend survives at fixed τ_peri.
- The 30 M31 systems have no orbits on disk, so they keep only the current-distance bound.

The ultra-faint overshoot of the velocity floor is therefore not tidal either.

**One sound speed against every constraint** (`X23_late_heated_cold`, b8d81770bb / df896db507 / 8b21926ce6 / d5f2a449d1; coordinator rerun identical apart from timing): **WRONG AMPLITUDE**, and the one-c_s **INTERSECTION is EMPTY** on both footings.
- At c_s,need, clusters capture the whole fair share: A_MID 7.5–10.7 against the measured 1.0–2.2 (×11–15), and the cold mass self-gravity makes it worse.
- Scanning one c_s ≥ c_s,need: T1 ≈ none needs ≥ 475 / 503 km/s, T2 only 570 / 604, T3 and the KT slope only 760 / 805, and no single value fits all three KT terciles.
- An isothermal c_s produces a step in well depth, not X21's smooth rise with KT.
- Groups, the MW disc, the forest and σ₈ pass.
- **Reading.** Universal, single-temperature late heating is excluded by the clusters alone, independently of the dwarfs. Any late-heated cold sector would need a temperature that scales with the well it sits in, i.e. heating keyed to the system. `X24_vacuum_heated_cold` tests the density-keyed version.

**Vacuum heating** (`X24b_vacuum_heated_cold`, 1d0f8c6967 / 3492bcbeb4; coordinator rerun identical apart from timing): **NO ε WINDOW** on both footings, and the sign is wrong at both ε edges.
- The forest gives ε ≤ 2.41e-6. SPARC needs ε ≥ 7.65e-6 / 8.59e-6, or 360–740 × ε_up if SPARC's content assembled at its own z_c.
- The density inversion is real (sympy: entropy ∝ ρ^{-5/3}; non-barotropic attractor s = −(13/18)δ), but the divide falls at assembly z ≈ 1, not between galaxies and dwarfs.
- SPARC, groups, T1 and the MW disc come out with the wrong sign (SPARC +0.9 dex). Clusters over-capture ×3–4.
- The dwarf sign is mostly right, but the trend with M★ is reversed.
- The energy scale (~1e-6 of ρ_Λ) is invisible to DESI. No local action exists: CFG944 Theorem G blocks θ-keyed terms.

**The floor is not in the action** (`X25_floor_from_action`, 230c922864 / 63a4001236, a peer lane; coordinator rerun identical apart from timing; `X25_dwarf_pericentre_tides` is a different lane): **WRONG SIGN**. The v3s held medium's γ_L sound speed is not X24's floor.
- Raising L★ lowers the dwarf predictions: screening, not a floor.
- c_s at 24 pc is 0.6–0.95 km/s, far below the 4.1–4.6 km/s needed.
- The ultra-faints get the largest c_s, but they need the smallest.

**Parameter reduction.**
- c₀ stays a lead, not adopted.
- The dwarfs push L★ monotonically to its floor. Together with CFG821 (L★ ≤ 22 pc), that squeezes L★ from a lower bound to a narrow band near 21.7–22.9 pc. The joint frozen bound is not yet computed.
- **Update** (`X27_joint_lstar_band`, 4bf6612dc5 / 5977c2445f, a peer lane; coordinator rerun identical apart from timing): **no reduction.**
  - The literal v3s pins L★ only through a fit at χ²/N ≈ 52. Rescaling its errors widens the upper end to 26.6 / 27.1 pc.
  - Profiling a floor nuisance removes any upper bound up to 90 pc.
  - So the dwarf "upper bound" is the mass shortfall, not screening. L★ stays one-sided: ≥ 21.7 / 22.9 pc.

**Floor form** (`X28_dwarf_floor_form`, 32d4323f88 / dad0c9f1fe, a peer lane, post hoc and disclosed; coordinator rerun identical apart from timing). The core class is **VELOCITY FLOOR** on both footings; the frozen label reads UNDECIDED only because of a [SPARC-COST] tag on canonical.
- An acceleration floor η·a₀ loses out of sample: χ² 327 / 389 against 217 / 195 for a velocity floor.
- The field and hosted η values do not overlap.
- A free power law g_floor ∝ r^{−n} gives n = 0.78 / 0.80, which excludes both 0 and 1.
- **No reduction:** c₀ is not a₀-scaled and not in the action, so it stays a dimensionful lead.

**The cold-sector map** (`X26_cold_sector_map`, b10263968f / c9112e3126; coordinator rerun identical apart from timing, pass-mask npz byte-identical, MUTATE exit 1): **ALLOWED ONLY WITH A SEPARATE c₀**, on both footings.
- Family: c_s² = c_*²(σ/σ_*)^{2r}(ρ/ρ_*)^q h(z).
- **Dwarfs.** No point among the 18,513 grid points reproduces the dwarf floor. The virial bound (FP3) makes clusters plus dwarfs, against SPARC, linearly inseparable.
- **The surviving sheet.** With c₀ separate, a thin sheet survives (45 / 37 grid points, about 8e-4 of the grid): c_s in clusters ≈ 556–761 km/s ≈ 1.1–1.5 σ_KT, with weak dependence on σ. Reported MGAS500 bins leave 2 points.
- **Excluded families:**
  - virial heating (r = 1), which reverses the KT slope;
  - universal heating, which passes the KT terciles in a narrow 634–714 km/s window that X23's scan stepped over, but fails the MGAS500 terciles everywhere.
- Untested on the sheet: the cluster radial profile (X30), late S8 power (X29, a peer lane) and the Bullet Cluster (X32).

**The sheet's own cluster profile** (`X30_sheet_cluster_profile`, c6be83f91c / 0f19b6759b; coordinator rerun identical in every number). The input SHA of X26's JSON differs: the lane hashed X26's JSON while the coordinator's X26 rerun had rewritten its timing fields. **PROFILE EXCLUDES THE SHEET** on both footings: all 19 canonical / 16 alt X26 points fail, including the 2 MGAS500 survivors.
- **Mechanism.** Partial retention at c_s ≈ 1.1–1.5 σ is outskirts-heavy. The cold core is 2–5 × the gas core, with < 5 % of the retained cold mass inside 0.5 Mpc.
- **Binding band: OUTER.** Fixing MID raises OUTER by about the same factor: predicted 1.42–2.26 against measured 0.66–0.72, Z −5.4 to −11. It fails in every tercile and under X7's full calibrated errors.
- Within this model family (isothermal, spherical, bounded at turnaround), the last surviving cold-sector door is closed. A centrally concentrated profile is not derived in the record and was not tested.

**Feedback energy as the key** (`X31_feedback_energy_selector`, 1aa11f9bcb / 358e3859ed / 5695a61801; coordinator rerun identical apart from timing): **FEEDBACK FAILS** on both footings. F = e_fb/σ² spans five decades and is set mostly by 1/σ².
- The heavy clusters that need extra have the *lowest* F (≈ 1). The dwarfs that need extra have F ≈ 5e3–2e4. Crater II has the highest F (5e4) and needs less than the law.
- Neither direction separates the classes, and F does not order them (Spearman +0.10). Within the dwarfs, mass orders the extra (−0.65) and F does not.
- No feedback-to-cold-sector coupling is supported.

**System atlas** (`X33_system_atlas`, 53f8f4aaa7 / 72e47a6e41 / 4ce94a0437; coordinator rerun identical apart from timing).
- **Scope.** 676 objects in one per-object table, descriptive only.
- **Pooled vs within-class.** Pooled cross-class trends are class placement: a within-class shuffle keeps 15 pooled FDR survivors and zero within-class ones.
- **Within-class FDR survivors:**
  - LG dwarfs: the extra rises toward low M★ (ρ −0.65), small r_h (−0.64), low Σ (−0.43) and strong host field (+0.32).
  - Small SPARC galaxies sit below the law toward low Σ₀ and late type (+0.44, −0.30).
  - Large SPARC galaxies fall with the external field (−0.46).
  - SPARC data quality also correlates (−0.40), a confound.
- **Where the law is right.** Within ±0.05 dex mostly at high surface density and high x: 29 / 27 % of SPARC overall, ~30 % in the upper half of Σ, 5–9 % in the lower half.
- **The misfits.** They are diffuse systems at both ends: gas-rich LSB spirals below, faint compact dwarfs above.

**Bullet Cluster** (`X32_bullet_cold_sector`, 57ff3e7df4 / 975ccfbf49 / 547ae0b9b9; coordinator rerun identical apart from timing): **UNDECIDED** on both footings. The stop rule fired: check K4 failed because the main cluster's cold component keeps only 0.3–0.5 % at the low sheet c_s.
- **The law alone** puts both lensing peaks on the gas, 40–51 kpc from it; the observed peaks are on the galaxies, ~200 kpc away.
- **Collisionless at the sheet c_s:** EXCLUDED. The main nucleus is disrupted, and its peak falls back toward the gas.
- **Fluid:** TENSION, dependent on the placement rule.
- **A CDM-like tracer** with σ near the well's survives (f_ret 0.80–1.02) and lands on the galaxies (reported).
- **The deciding variable is c_s/σ_well, not fluid versus collisionless.** This agrees with X30: the extra cluster mass behaves like a component as hot as the well itself.

**a₀ tracking early dark energy** (`X35_a0_tracks_ede`, 02848d0330 / 0eb84a459a / 90f9391487; coordinator rerun identical apart from timing): **UNDECIDED** (frozen rule).
- **Magnitude is not the obstacle.** With literature EDE, a₀ at z ≈ 1100 is 1.7e3–7.6e3 × today and the plasma is deep in the law's regime. Today's a₀ is unchanged.
- **v3s has nothing for a huge a₀ to act on.** With no khronon charge, charge conservation gives ρ_τ ≡ 0 and Ξ ≡ 0, and the potential is GR for any a₀.
- With Blanchet–Skordis dust, a₀ drops out of the linear kernel.
- A static AQUAL reading gives a boost in phase with the plasma (G_eff/G 11–29). That makes the first-peak scales Jeans-unstable instead of supplying a steady well.
- **New caveat for CFG689.** EDE shifts the sound-horizon ruler by about 4 %, so CFG689's native a₀(z) band holds only for a ruler with no EDE.

**Recombination as a release boundary** (the owner's idea; `X34_recombination_release`, 6c5d581400 / ab4a3a8e1a). Coordinator rerun identical: the patched CLASS was rebuilt from the same patch (same patch SHA, new binary SHA), and every result line matches apart from elapsed time. **RRB REDUCES TO ORDINARY CDM.**
- **Timing.** In patched CLASS with an energy-conserving turn-on, the cold component must already be dust by z ≈ 5×10⁴. That is 45 × recombination and 15 × equality. Released at recombination, Δχ² ≈ +4.5×10⁵ and σ₈ ≈ 5 % of ΛCDM.
- **Relic speed.** Decoupling near z ≈ 1100 would give a forest-allowed floor matching the dwarf c₀. At the epochs the CMB allows, that window is empty on canonical and a sliver on alt, and it overshoots the ultra-faints.
- **Scale link.** Over 54 trials there is one chance-level match: the proton thermal speed at recombination, 4.95 km/s, against c₀. It has no a₀ and no action, so it is numerology.

**Naming (owner, 2026-10-25).** The cold component in this section is **cold dark energy**: a gravitating w ≈ 0 field component that clumps, paired with dark energy (w ≈ −1). It is not matter and not a particle. "Dust-like" describes only its clustering. ΛCDM remains the name of the external rival model. Committed lane text is not rewritten; where an earlier line in this section says "CDM-like" (e.g. X32's tracer), read "dust-like cold dark energy".
**Physics, stated plainly.** In every test run here, the cold dark energy that the data require behaves like the cold component of ΛCDM:
- cold and collisionless from z ≳ 5×10⁴;
- concentrated in cluster cores;
- carried with the galaxies through the Bullet collision;
- clustering down to forest scales.

No test here distinguishes it from that component. What the framework adds is the galaxy law, plus the open problem of why isolated galaxies show no extra today.

**Late power against KiDS** (`X29_late_power_shear`, peer lane; 35b3573518 / 1e06cc9946 / 365366ff9b): **SHEET CUT** on both footings, on raw KiDS-1000 ξ±.
- 23/45 canonical and 15/37 alt points survive.
- There is a clean edge at T²(k = 1 h/Mpc) ≈ 0.82, which means σ₈ loss ≤ ~1 % and cosmic c_s today ≤ 270–330 km/s.
- X29 is an independent S8-side cap. The whole sheet is already excluded by X30's OUTER band.
- **Coordinator rerun:** every number is identical. The committed main `.out` was generated before A1's K0 tolerance change in the committed script, so a rerun of that script grades K0 PASS on identical Δχ² values (−4.3e-5, −2.1e-5). The provenance gap is disclosed here; no result changes.

**Is the law fundamental or emergent?** (`X36_efe_discriminator`, d8651cafc3 / 667b97260b / 8d7df6a74d; coordinator rerun identical apart from timing; it reproduces EM1_emergent_dust_law exactly in a scratch copy): **NOT DIAGNOSTIC** on both footings.
- **Route E** (cold dark energy everywhere, law emergent) ties the law on SPARC at fixed Υ 0.5 (EM1).
- **X33's large-SPARC e_ext trend** (ρ −0.45) survives nine confound controls.
- **The law's own EFE predicts almost none of it** (≤ 0.005 dex at e ≈ 0.03–0.06). Route E reaches only a quarter of it.
- **With per-galaxy Υ the trend vanishes**, so it behaves like an environment-correlated normalisation, not an EFE shape.
- **Gaia DR4 cannot separate the two readings either.** The MW field barely varies over the binaries, and both predict Newtonian wide binaries (v3s is screened).

So no test in the record yet distinguishes "the law is fundamental" from "the law is how cold dark energy settles around baryons". In route E the a₀–Λ link is a coincidence.

**Orbit-keyed conversion** (`X37_orbit_conversion`, peer lane; criteria 204001f8ad; coordinator rerun identical apart from timing): **OC FAILS CLUSTERS** on both footings. Cold dark energy converting to dark energy as exp(−N_orb/N*), with N* set by SPARC alone, empties cluster cores first. It predicts OUTER 1.34–1.67 against 0.66–0.72 measured, and gives the MID slope with KT the wrong sign. General statement: any depletion rule keyed to orbits, density, temperature or time removes cold dark energy from cluster centres first, while the data want it concentrated there.

**Cold dark energy halos with surface density set by a₀** (`X38_a0_surface_density_halos`, peer lane; criteria 9cc80516df; coordinator rerun identical apart from timing). This is route E with Burkert-cored halos at ρ₀r₀ = a₀/(2πG) (107 / 129 M☉/pc²). It adds no new constant; the M200 relation is EM1's committed one. Frozen result: **SD PASSES SPARC ONLY**, on both footings.
- **SPARC passes** at a sensible Υ: rms 0.080 / 0.073, median Υ 0.77 / 0.60. EM1's NFW halos needed Υ 0.36.
- **The cluster OUTER band passes for the first time:** all-KT Z +0.14 / −0.06, and the terciles and slope pass too.
- **It fails the heaviest cores**, under-predicted: MID T3 Z +4.3 / +3.8; KT slope +3.1 / +3.0. The cores come out too large (0.27–0.44 Mpc).

This is the first model in the record that ties a₀ to the cold dark energy itself. Its constant-surface-density core gives a₀ a role in route E rather than leaving it a coincidence. Open: whether baryonic contraction by the BCG and hot gas shrinks the heavy cores (peer lane X39, gravity only, no new constant).

**Baryonic contraction** (`X39_baryonic_contraction`, peer lane; criteria b75acfc767; coordinator rerun identical apart from timing): **SD + AC FAILS** on both footings.
- Blumenthal and Gnedin contraction by the BCG and hot gas move the heavy cluster cores by only about +0.08 (MID T3 1.05 → 1.13 against 2.13).
- The same physics rebuilds the galaxy cusp and breaks SPARC (median Υ 0.77 → 0.39).
- X38 therefore stands without contraction. What remains is that cold dark energy cores must be about 2 × denser than a₀/(2πG) at cluster masses while staying at a₀/(2πG) in galaxies. That is a mass scaling of the core physics that baryons cannot supply.

**Fixed core radius** (`X40_fixed_core_radius`, peer lane; criteria b37983a0f7; coordinator rerun identical apart from timing): **FC FAILS** on both footings. A single core size calibrated on SPARC (r_c 9.7 kpc) fails SPARC (rms 0.119 at Υ 1.20) and overshoots clusters ×2–4. So the core's surface density, not its radius, is the right variable: a₀/(2πG) across galaxies, rising about ×2 in the heaviest clusters. That rise is the single remaining quantified gap; `X41_core_surface_density_scaling` tests framework-native rules for it.

**Framework-native rules for the cluster core density** (`X40b_core_surface_density_scaling`; it is not X41, because the criteria were committed before the rename; b09db13390 / ba368d2ba1; coordinator rerun identical apart from timing): **NO FRAMEWORK-NATIVE RULE CLOSES IT**, on both footings.
- **Rule A / A′ (the core set by max(a₀, g_b)) never switches on.** At cluster cores g_b is only 0.04–0.07 a₀ (gas 98–99.5 %). The cores would need 2–5 a₀, so the rule falls 30–100 × short, and every number equals X38's.
- **Rule B (a₀ at formation, DESI curve)** has the right sign, but its largest possible ratio is 1.34.
- **Reported only:** with galaxies pinned, the clusters need S ∝ M^0.25–0.30. The cluster cores then sit at 3–5 × a₀/(2πG), so the gap is 3–5 ×, not 2 ×.
- **New:** X38 also fails the groups line (σ under-predicted, +0.09–0.10 dex, Z +2.3–2.5), in the same direction as the clusters.

**Reading.** Cold dark energy halo cores sit at a₀/(2πG) in galaxies and rise with mass above galaxy scales (S ∝ M^~0.25–0.3). Nothing in the framework supplies that rise. It is the remaining quantified gap.

**Collapse floor** (`X41_collapse_floor_sigma`, peer lane; criteria 0ea05957ee; coordinator rerun identical apart from timing): **CF INACTIVE** on both footings; it reduces exactly to X38.
- The Lacey–Cole EPS collapse ρr on the record's CLASS P(k) scales as M^0.23 over 1e13–1e15 M☉, near the needed M^0.25–0.30.
- Its amplitude is only 0.22–0.26 × a₀/(2πG). Reaching the cluster cores would need a core-concentration factor of about 11–23.
- **Requirement now.** Cold dark energy cores sit at the a₀/(2πG) floor in galaxies, and at about 10–20 × the collapse ρr in groups and clusters. The origin of that concentration factor is missing.

**Collapse core floor** (`X43_collapse_core_floor`, peer lane; criteria 00bc1a7950; coordinator rerun identical apart from timing). **CC FAILS [c_f EXTERNAL]** on both footings, on only 2 of 17 keys. The rule is Σ_core = max(a₀/(2πG), η Σ_coll), with no fitted constant:
- Σ_coll is X41's Lacey–Cole EPS collapse ρr.
- η = (4/(3B(1))) c_f^{5/4} = 14.8 comes from Bertschinger r^{−9/4} infall with a core at r_f/c_f.
- c_f = 4 is an external value (Bullock/Zhao).

Results:
- **SPARC passes:** rms 0.078 / 0.073 at Υ 0.77 / 0.60.
- **14 of 15 cluster keys pass, including the heavy cores:** MID T3 Z +4.26 → +0.30; MGAS-all OUTER +2.36 → +0.49.
- **The two failures are slight under-predictions:** groups Z +2.05 (line 2.0) and MGAS T3 OUTER Z +2.41.
- **Reported only:** c_f = 5 (η 19.6) passes the groups.

**This is the closest complete picture in the record.** The cold dark energy core surface density is a₀/(2πG) in galaxies. Above galaxy scale it is the gravitational-collapse value, raised by a secondary-infall concentration factor. The one external input is c_f, which the peer is deriving from the infall solution (X44).

**Deriving c_f from scale-free infall** (`X44_self_similar_cf`, peer lane; criteria c8dd02f5aa; coordinator rerun identical apart from timing): **SS FAILS** on both footings.
- Self-similar infall timing gives c_f = 2^{8/9} = 1.85 (η 5.66), which fails four keys: groups, MID T3, MID slope and MGAS T3 OUTER.
- The data pin c_f ≈ 4–4.2: X43's groups line crosses at c_f ≈ 4.2, and X42's cluster-only calibration gives 3.3–4.6.
- That is the standard formation concentration. Scale-free infall cannot produce it; it needs the structure of the initial peaks.
- MGAS T3 OUTER should get a data-side check before more rules are built on it.

**Peak-curvature c_f** (`X45_peak_curvature_cf`, peer lane; criteria 1fd8e1238a; POST-HOC exploratory after two post-result amendments; coordinator rerun identical apart from timing): **PK FAILS** in every run on both footings. Spherical collapse of the BBKS peak profile on the record's P(k) gives a near-uniform core with no r₋₂, so c_f falls back to 1.85 and reproduces X44. Reading: c_f ≈ 4 comes from orbit mixing and relaxation, not from spherical peak collapse. The framework-native route is to measure formation-epoch concentrations in the record's own PM runs.

**The tether: a vacuum-set core floor** (the owner's question; `X47_vacuum_tethered_core_floor`, bafcb4754e / 9feeb722fc; coordinator rerun identical apart from timing). The hypothesis: cold dark energy stays bound only where its own pull exceeds g_T = 0.254 a₀ (2.4e-11 / 2.9e-11 m/s²).
- **As a local rule: FAILS** (growth and self-consistency).
  - The linear field's own pull is ≤ 0.02 g_T today, so a local key tethers the linear field and kills growth (the μ-pincer in acceleration form).
  - A latching key never forms a floor.
  - A cored halo's own pull is below g_T at the centre and in the envelope.
- **As a rule about bound objects: CONSISTENT but nonlocal**, with no action.
  - It must act after virialisation; collapse itself is below threshold.
  - Theorem D-T does not apply inside self-gravitating cores (premises P1 and P3 fail), but it returns wherever the tether is on.
- **Data.**
  - Per-galaxy free Σ fits centre on g_T (median +0.07 / −0.02 dex) with a ±0.32 dex spread: no sharp pile-up.
  - Context, PROVISIONAL: Gentile+2009 gives 1.3 / 1.1 g_T.
  - Prediction: Σ_floor(z) ∝ a₀(z) shifts only −0.06 dex by z = 2, too small for the record's z ≈ 2 samples.
- **Reading.** Whatever tethers cold dark energy must key on bound objects (halos), not on any local invariant. That is the remaining mechanism question.

**Core rise above galaxies** (`X42_core_rise_above_galaxies`, 4a13086d02 / 9caa641111 / 0d7d0d5686; coordinator rerun identical apart from timing): **BOTH FAIL**, on both footings.
- **H1 (self-similar floor, calibrated on clusters only).** Implied concentration 9–14 × the EPS Σ_coll (12.9 × at the median cluster mass), consistent with X43's η 14.8. α = 1/3 is allowed. It fails the groups out of sample (Z +2.41 / +2.27) and MGAS T3 OUTER.
- **H2 (baryon retention, f_b/0.0577, no fitted constant).** It improves SPARC (rms 0.0795 → 0.0705) and fails the groups by 0.03 on canonical only. It also fails MGAS T3 OUTER (+2.68).
- Every rule tried binds on the same two keys, the groups and MGAS T3 OUTER.

**Native c_f from zoom simulations** (`X48_native_cf_zoom`, a peer lane, owner-approved; criteria 1932858ae8): **UNRESOLVED**. This lane was not rerun by the coordinator, because it is ten multi-hour direct-summation runs.
- The method is collisionless zooms of constrained peaks, with cold dark energy plus Λ and no a₀ floor.
- At ng 38 the medians are c_f 10.6 / 5.9 / 11.0 at 1e12 / 1e13 / 1e14 M☉.
- The frozen resolution check fails: at 1e14 seed 1, ng 38 → 48 moves c_f from 12.68 to 2.59. So ng 38 is not converged and its regrade is not evidence.
- Reported only: the NFW-form fit gives 4.00 at ng 48, which matches the data-pinned 4–4.2. That is one run with no verdict weight.
- Resolving it needs ng ≥ 48 for every mass and seed. X43 stands with c_f = 4 as an external input.

**X48 at ng 48** (A1 2bfdeb83a9 / acb2bf5277 / 737193f3fa). The simulations were not rerun by the coordinator. The coordinator reran the regrade from the stored ng 48 analysis, and it is identical apart from timing.
- **Frozen class:** NATIVE c_f ABOVE WINDOW at ng 48; convergence beyond ng 48 is not tested.
- **Medians:** c_f 7.2 / 7.0 / 5.6 at 1e12 / 1e13 / 1e14 M☉. The per-seed scatter is ×4–6 and the ng 38 → 48 shifts run from −80 % to +48 %, so the medians are uncertain by about ×2.
- **X43 regraded with the native c_f(M)** passes SPARC (0.065), the groups (Z +1.53), every MID key with its slope, OUTER, and MGAS T3 OUTER (+1.80).
- **It fails one key:** the 326-cluster inner band, G-IN-Mall (predicted 4.81 against 2.28 ± 1.05, Z −2.41 / −2.06, over).
- **Reading.** This is the closest result in the record with no borrowed number. The only open item is the convergence of the native c_f.
