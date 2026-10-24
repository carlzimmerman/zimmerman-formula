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
