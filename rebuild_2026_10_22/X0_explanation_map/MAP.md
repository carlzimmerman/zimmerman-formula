# X0: every explanation for v3's failures, against the record (2026-10-23)

The owner's request: "we need to explore all possible explanations and i dont think you have done a thorough enough job".
Six read-only audits, one per failure plus one for alternative frameworks, mapped every explanation class they could find
in the record and the literature. Each class is classed as (1) a data or analysis artefact, (2) physics inside v3 not yet
included, (3) a change to the action, or (4) another framework within the rules. Each row cites the lane or file that tested
it. Literature status comes from search snippets and abstracts and is PROVISIONAL.

κ = ½ FITTED. Footings 9.36e-11 / 1.13e-10 m/s², never pooled. No dark-matter particle. Not "theory closed". Nothing here
says the data favour the framework.

## Bottom line

- **The record is broad, but not complete.** About 25 classes are untested or only partly tested. Most are cheap: data and
  solvers are on disk, runs take minutes at under 1 GB, and none needs a new fitted knob.
- **Several record verdicts are stronger than what was computed** (§3). Some failures may be smaller than stated. None
  turns a failure into a pass by itself.
- **Three failures are generic to the whole MOND class, not to v3.** In each case no rule-compatible framework in the
  literature claims a clean pass:
  - **Cluster cores.** The only published cluster passes are contested (MOG), cover two clusters with inconsistent parameters
    (refracted gravity), or carry a particle (superfluid DM, νHDM).
  - **The CMB's third peak.** It forms at z ≈ 1100, where x ≈ 11–14, the Newtonian regime. a₀ is inert there, so no
    nonlinear MOND effect (L1 included) can reach it. Only an a⁻³ dust has ever fitted it.
  - **The Milky Way.** Joint radial-plus-vertical MOND fits fail in the literature (Lisanti+19; Wang+26 at >13σ). The
    steep outer decline is beyond the whole μ-law family: a point mass at 15–27 kpc gives a slope of −0.13 to −0.17 (audit
    hand estimate), and v3's −0.126 already sits at that bound.
- **Two structural leads are new to the record:**
  - **Switched stiffness −(γ_L/2)(D·P)₊².** It has zero new constants, and its statics are unchanged wherever screening is
    used. Where ρ_τ < 0 it falls back to Blanchet–Skordis's bounded branch. This targets the saddle ill-posedness directly.
  - **The hosted-dwarf failure may come partly from the sample and a premise.** E3's mass cut keeps only ultra-faints. U1's
    theorem T3 premise (held host ⇒ no dust) is contradicted by Crater II, the bright M31 dSphs, Coma's UDGs (CFG948) and the
    UMa members (U1 A2).

## 1. Failures and their untested classes (ranked: decisiveness × cheapness)

### A. Cluster cores: 1.68–1.85 / 1.54–1.70 × the law in 0.3–1 Mpc (F1, H2, S4)
1. **The outskirts anchor.** F1 extrapolates gas as β = 2/3 (ρ ∝ r⁻²) to 3 Mpc, which is 78 % of the gas budget. The record's
   own measured slope is r⁻³ (CFG814). With aperture-only gas, A_OUTER is 1.57 / 1.44 (F1 C3c G2). A_OUTER by gas tercile
   runs 0.57 → 0.96 → 1.38 (CFG687), and the catalogue EFE was never run on the stack.
   → Rerun F1 with the measured slope, per tercile, with and without the EFE. About 7 min, < 0.7 GB, no knob.
2. **One fixed-form component on that baseline.** Candidates: Milgrom's cluster baryonic dark matter (cold clouds), the
   published missing-to-gas form (FPS 2410.02612), or CFG949's debris profile. No constant is fitted here; external
   parameters are labelled as such.
3. **Shear systematics.** The cross-shear in MID is 2.0σ and the random-minus-random OUTER offset 2.2σ (neither propagated).
   F1's `esd()` has no reduced-shear (1 − κ) term.
4. CFG745's selector on F1 (it carries a fitted k); CFG962 (frozen at 0e2421c721, never run); L1's production halo profiles;
   triaxial AQUAL; CFG967's native two-halo term.

### B. Linear growth, CMB, BBN (F3, M1, Q6, Q7, C7, L1)
1. **Grade at the native cap.** S4's galaxy guard fails for μ_K ≥ 0.1 Mpc⁻¹ and passes at ≤ 0.03. Every growth number "at
   the cap" (14.8 h/Mpc ≈ 10 Mpc⁻¹) is graded at a value the record itself excludes. Restating the gap is minutes of
   bookkeeping; it is likely ~10⁴×.
2. **The DBI door.** Q7 §5 found that λ_D ≈ 4e9–3.6e10 reaches R_B 0.95 and Δχ² +1.6 at the cap, but λ_D is set by the
   failure (a knob). Cheap closure checks: max |δQ| against λ_D^-1/2 ≈ 1.1e-5, and the Lyman-α forest gate on its P(k) at
   z ≈ 3. These can close the door; they cannot adopt it.
3. **Q-keyed and τ-keyed holds.** Theorems D-T and D-T′ (CFG941, CFG946) leave only these keys. Candidates: a two-scale
   K(Q), a comoving Jeans scale μ_K = μ_cap/a, and SZ21's Cosh / Exp / Higgs K inside the Khronon CLASS. Each is a
   postulated function, likely with a new scale near Φ/c² ≈ 1e-5.
4. **L1** (running). Hwang–Noh 2410.10205 vs 2503.20151 on 0PN growth (reading only). The "dark solid"
   (`qwen_claude_field_theory/closure_2026/condensate_pincer_2026/dark_solid_first_gates_2026.py`) is CDM-like at linear
   order and holds < 30 % M_b in galaxies; it has 2 new constants and was never developed.

### C. Saddles: ill-posed where ρ_τ < 0 (H4, I1, M1)
1. **Switched stiffness −(γ_L/2)(D·P)₊²** (above). Test: H4's B1/B2 slab with the piecewise operator, whose rate must
   converge under resolution doubling. Then check D·P ≥ 0 wherever C6 (Cassini) and D10 (globulars) rely on screening.
   Hazards: the Lagrangian is only C¹; the interface; D·P < 0 lobes near stars.
2. **Lifshitz regulator β(∇·n)²**, inside C5's window (~6e-19 < β ≲ 1e-9, an estimate). sympy, minutes.
3. **Strong coupling at saddles.** c_π → 0 where ρ_τ = 0. P3's strong-coupling PASS applies only where D·P > 0. This
   decides whether the kill lies inside the EFT.
4. **Alternative screens.** A33 with η = γ_L plus β, on ρ_τ < 0 backgrounds. A leaf-tidal (Hořava-type ∇_i a_j) key:
   M1's ghost argument used a Lorentz-invariant toy scored for v4. A BDEF 2011 / k-mouflage reproduction: the record holds
   conflicting notes, and k-mouflage was never tried as a Cassini screen.

### D. Hosted small systems: satellites, Coma UDGs (S1, U1, T1)
1. **The sample.** E3's cut M < a₀L★²/G (≈ 3.9e5 M☉ at 24 pc) removed every classical MW dSph and the bright M31 dSphs.
   42 of 45 systems have log M★ < 5.5, and 32 are MW ultra-faints. McGaugh & Milgrom 2013 and Crater II were never
   reproduced as controls. Central medians (audit, from `s1_per_system.csv`): MW +1.47, M31 +0.89, M31 with log M★ ≥ 5
   +0.47, Crater II +0.36.
   → Run S1's solver on all Local Group satellites, with MM13 and Crater II as controls. About 20 min.
2. **The T3 premise.** These are hosted but not Newtonian: Crater II, the bright M31 dSphs, Coma's UDGs (CFG948 excludes
   Newton at 5.45σ) and the UMa members (13–14σ per galaxy; U1 A2 leaves this at DEPENDS). The TDG/DF2 "native pass" is the
   same T3 prediction and must be booked together with these.
3. **Binaries at v3's sub-km/s predicted σ.** CFG892's forward model was graded against the bare law's σ, not v3's.
4. **Hammer+2019 first-infall tidal shocks.** Never tested. T1 A3 finds the residual tracking the host field at a slope of
   +0.78 ± 0.28.
5. **Membership jackknife** on the Walker+23 per-star table (on disk). **The dust coupling** (−∇Φ), which exists only as U1's
   mutation control.

### E. Milky Way disc: K_z +39–46 %, v_c(R₀) low, outer slope Z −4.4 (P4, S3, U1)
1. **Joint light-column baryon test.** P4's solver with a light local column plus a compact bar / inner disc, within
   published priors. Line: χ²_Kz ≤ 67.5 AND |v_c − 229.1| ≤ 2σ AND the priors. About 10 min. Expected to FAIL; if it does,
   K and V are AQUAL-structural.
2. **S3 Part A under CFG532's S2 error budget** (5 % systematics). Minutes. That budget flipped the old rule to
   CONSISTENT.
3. **Jeans forward model.** Koop+24 (2405.19028): truncated tracers can fake a decline, so mock the estimator on v3's own
   potential. This is the most decisive test for the slope.
4. Gaia DR4 (2 December 2026, sealed). Also: an n = 2 rerun, a north/south split, a moving LMC, and BR13's model dependence.

### Frameworks within the rules that the record has not robustly tested
Covariant refracted gravity (Sanna+ 2109.11217): absent from the record; one scalar for DM phenomenology and DE, with
a₀ ∼ √Λ. MOG/STVG: never computed; its CFG230 cells are memory labels. Dipolar DM in massive bigravity
(Blanchet–Heisenberg): only the Newtonian medium was tested. k-mouflage-screened RMOND. BIMOND's variable-G cosmology
(2512.09353). Each has a cheap first check: SPARC RAR + X-COP with one published parameter set, or Q₂ plus saddle
hyperbolicity for the screens.

## 2. Lanes launched from this map (stop-ruled; frozen criteria committed alone first; no new fitted knob)

| lane | question | from |
|---|---|---|
| X1_hosted_recount | v3 on all Local Group satellites with MM13 and Crater II controls; T3 premise bookkeeping | D1, D2 |
| X2_cluster_outskirts | F1 with measured outskirt gas, per tercile, ± EFE, reduced shear; then fixed-form published components | A1–A3 |
| X3_switched_stiffness | (D·P)₊² stiffness: well-posed at saddles? statics unchanged where screening is used? | C1 (C2, C3 secondary) |
| X4_growth_native_cap | growth restated at the native cap; DBI door closure checks (δQ, forest) | B1, B2 |
| X5_mw_joint_baryons | light-column baryon test; S3 under the S2 error budget | E1, E2 |
| X6_dust_coupling | the owner's design lane: dust couplings derived from the action family, graded on satellites, clusters, growth and galaxies | D5, A, B |

## 3. Record verdicts that are stronger than what was computed (to fix forward)

- **F1 / THEORY_V3_DRAFT §3 / board.** "Any added cold profile that fixes MID overshoots the outskirts." CFG949 (MID 1.011 /
  OUTER 1.047) and CFG727 (0.93 / 1.05) contradict it, and OUTER ≈ 1 rests on the β = 2/3 gas, the tercile mix and no EFE.
  Z ≈ +5–6 uses jackknife errors only.
- **S4 and H2 "no-go".** Static, spherical branch only. U1 leaves the cap OPEN.
- **Growth "at the cap".** Graded at a μ_K that S4 excludes (Δχ² +3,627 at the cap). "0.391" is the formal ODE value;
  Boltzmann gives 0.073. M1's "no analytic K escapes" is contradicted by Q7's λ_D,95, which is analytic at Q = 1. "v3's one
  open escape is nonlinear (L1)" is overstated: XD3 is exact, both rungs have KX < LIN, and the CMB is out of L1's reach.
- **Board tile "Leaf problem well-posed: FAIL".** Contradicts H4 §5: C8's elliptic leaf problem stays well-posed; the
  ill-posedness is in the khronon/dust evolution, which belongs on the Health tile. THEORY_V3_DRAFT L13/L17: "η > 0 is
  ill-posed" holds only at β = 0.
- **Board tile 26 "Dwarf satellites".** The sample is the sub-threshold, ultra-faint-dominated set. S1's +1.33 and U1's
  +2.00 rest on T3's premise. MM13 was never reproduced.
- **P4's "every baryon model fails".** Robust to screening, EFE and footing, not to the baryon model (no light-column model
  was run). S3's "ROBUST" means robust to v3's ingredients, not to rotation-curve systematics.
- **M1 R2a (galileons).** Neither cites nor reproduces BDEF 2011, which `real_research/CASSINI_QUADRUPOLE_CONSTRAINT.md`
  records as a Cassini escape. M1 R2b4 (Weyl ghost) used a Lorentz-invariant toy.
- **Stale documents:** STANDING rev 10 (khronon dust "passes σ₈"); the memory line "cluster theory program COMPLETE" (06-26,
  before CFG727/949); the old MW vertical "PASS" (relative to the phantom disc, in EVIDENCE_DOSSIER 10-12, ASSESSMENT 10-09
  and KILL_SHEET G4); two DR4 MW seals (CFG553 old round rule; v3's is `SEALED_V3_MW_DR4.json`).
- **Frameworks resting on memory labels:** CFG230's MOG, TeVeS and Weyl cells. C7's AeST CMB result contradicts SZ21's
  published fit (normalisation g, unpublished initial conditions) and has no independent cross-check.
- **LEDGER.md has no rows for H4, I1, M1 or V1.**

## Sources (the six audits; full tables in the session record)
The audits read STANDING.md, campaign_fresh_gravity/LEDGER.md, THEORY_V3_DRAFT.md, the rebuild_2026_10_22, doors_push and
covariant_push READMEs, hunt_2026/, opus_48_extended_research/, CANDIDATE_LAWS_REGISTER.md,
campaign_fresh_gravity/closure_map/TEN_DOORS_RESULT_2026-09-29.md, data_assembly/DOORS_LITERATURE_STATUS_2026-09-29.md,
fable_independent_2026/RELATIVISTIC_MOND_GATE_MAP.md, and the owner's memory notes.
Literature (provisional): KL24 2405.08557; FPS 2410.02612; Kroupa+26 2602.06082; Milgrom 2008 (0712.4203); Hwang–Noh
2410.10205 and 2503.20151; KiDS-Legacy 2503.19441; Koop+24 2405.19028; Lisanti+19 1812.08169; Wang+26 2605.10857;
Coquery & Blanchard 2025; McGaugh & Milgrom 2013 (1308.5894); McGaugh 2016 (1610.06189); Hammer+2019 (1812.10714);
Freundlich+2022 (2109.04487); BDEF 2011 (1106.2538); Blas–Pujolàs–Sibiryakov 2011; Sanna+ 2109.11217;
Blanchet–Heisenberg 1505.05146; Durakovic & Skordis 2312.00889.

## 4. Lane results (2026-10-23; each lane reran by the coordinator and reproduced)

Lane directories are named in full. **X1 here means `X1_hosted_recount`.** Another session's `X1_seedfree_abundance`, started at
14:17 after this map named X1 at 14:11, is unrelated.

| lane | frozen verdict | key numbers (canonical / alt) | commits (criteria / results) |
|---|---|---|---|
| `X1_hosted_recount` | Controls: CONTROL FAIL, PUBLISHED APPROXIMATION (frozen class). Q1: CLASS-GRADED [W-SENSITIVE]. Q2: T3 PREMISE CONTRADICTED | v3 at the L★ floor, all 89 LG systems, no mass cut: MW ultra-faints +1.56 / +1.55 dex (FAIL); M31 others +1.14 / +1.10 (FAIL); bright M31 dSphs +0.60 / +0.58 ± 0.13 (FAIL, 4.6σ; +0.35 at the worst-case data choice); MW classical +0.36 / +0.32 ± 0.26 (UNRESOLVED; Fornax and Leo I fit, Draco/UMi/Sextans +0.9–1.1); isolated LG dwarfs +0.06 / +0.02 ± 0.08 (consistent). Exact MOND + EFE without screening is within 0.02–0.04 dex of v3: the failure is AQUAL's external field, not screening. Hosted sets ≥ 5σ above Newton: Antlia II 24.2σ, MW ultra-faints 12.6σ, UMa 12.6σ, bright M31 9.8σ, Crater II 8.7σ, Coma 5.4σ | cfd0ae45fb / c74c622229 |
| `X2_cluster_outskirts` | V1 OVERSHOOT WEAKENED BY the shear systematics; V2 A FIXED-FORM COMPONENT PASSES (CFG949 debris *replacing* the law at cluster scale); V3 core excess WEAKENED with all systematics, SURVIVES without them | The stacked A_OUTER ≈ 1 is a cancellation: OUTER by mass tercile 0.46–0.54 / 0.72–0.80 / 1.25–1.40. **The lightest tercile has no core excess** (MID 1.02–1.13). Core excess Z 5.4 / 6.1 / 4.7 / 5.3 → 2.7 / 2.6 / 2.3 / 2.2 with the cross-shear offset (+0.19–0.24, 1.7–2.1σ) propagated. The measured r⁻³ gas slope changes A by ≤ 0.01; the external field by ≤ 0.004; reduced shear moves A_MID by −0.03. Debris *added to* the law overshoots; FPS Eq. 17 fails | 40624db7e9 / 1d837f6945 |
| `X3_switched_stiffness` | (pending) | | |
| `X4_growth_native_cap` | (i) GROWTH FAILS AT THE NATIVE CAP; (ii) DBI DOOR CLOSED BY THE FOREST (marginal at one point) | At S4's galaxy-guard μ_K (0.03 / 0.1 Mpc⁻¹): Boltzmann R_B 0.0032 / 0.0052 (the cap gives 0.073), ODE upper bound 0.076 / 0.082. Gap to 0.95: ×300 / ×182; μ_K gap 2.4e3–5.7e4. The khronon is radiation-like until z ≈ 35–78. DBI λ_D,95: δQ consistency passes everywhere (0.05–0.35 of the line); forest FAIL at the cap and P1μ; P2μ passes L346's band but fails L319's strict line (0.972 / 0.896 vs 0.995) and the loose 0.9 line at z = 2 by 0.004 | 2060d39ced / c778d300e8 |
| `X5_mw_joint_baryons` | (i) FEASIBLE (wide priors only); (ii) SHAPE EXCLUDED ROBUST | 7 / 175 (canonical) and 4 / 175 (alt) prior-box cells pass χ²_Kz ≤ 67.5 with v_c(R₀) inside 2σ. All need R_d 1.93–2.27 kpc (≥ 2.8σ below Licquia & Newman) and Σ_b 40.3–43.7 (McKee −2σ to −1σ). Post-result diagnostics (no verdict weight): in every passing cell K_z(R₀) is still 76.7–80.9 vs 66.4 ± 2.2, the full rotation curve fails (χ² 96–194 vs 61.2), and the outer slope stays excluded. U1's v_c bound is specific to McMillan17. Outer slope under CFG532's S2 budget: Z −3.88 / −4.09, still EXCLUDED | 8e5b65bca5 / 04e5c6be40 |
| `X6_dust_coupling` | NO-GO FOR THE STATED CLASS | sympy theorems: in the khronon family the dust's coupling is fixed by kinematics (its acceleration relative to free fall is ∇Ξ, the field that carries the law; α ≡ 1); at Q = 1 it is exactly mimetic dust. Dust that has weight in hosts and self-gravity on linear scales must be a separate field, which sources the law like baryons and double counts. A separate mimetic dust passes growth for f_d ≥ 0.762 but fails isolated galaxies for every f_d > 0 (NGC 3198 off by 0.145 dex; SPARC Υ falls to 0.42 / 0.37): CDM under another name. AeST's sector fails clusters (H2) and health (H1) | fd303cac8b / fbcce8f612 |

### Corrections to sections 1 and 3 from the lanes (fix-forward)
- **§1.A.1:** the measured gas slope is not OUTER's weak point; it changes nothing under CFG814's prescription. The weak points are
  the tercile mix and where the steepening starts (X2).
- **§3, first bullet:** CFG949's passing debris *replaces* the law at cluster scale. Added to the law, the same debris overshoots
  ×1.6–2.0. F1's sentence holds for law-plus-component profiles shaped like the gas, but a compact central mass passes the
  profile χ² in 3 of 4 cells (X2). Quote the core-excess Z as 2.2–2.7 with systematics, beside the jackknife-only 5–6.
- **§1.B:** at the native cap the gap is 2.4e3–5.7e4 and v3's R_B is 0.003–0.005 (X4). The DBI door is closed by the forest, not
  by its own consistency.
- **§1.D:** the medians in §1.D came from S1's binary-corrected sample. X1 gives Crater II +0.50 / +0.46 without that correction.
  Published MOND's Crater II and M31 successes rest on the approximate EFE formula's full-mass normalisation; exact AQUAL + EFE is
  0.19 dex lower (X1 controls). §1.D.5: the −∇Φ coupling has no action at all (X6). U1's "what would have to change: the dust
  coupling (and J)" should read: the field content. J does not enter T3 (X6).
- **§1.E.1:** expected FAIL; the frozen result is FEASIBLE on wide priors, inside a corner that fails other Milky Way data (X5).
- **§1.C.4 (peer review):** the Codex arrival audit (reviews/codex_arrival_audit_2026_10_23/, c638cd7c12) finds a Hořava half mode
  in DSF-21's η > 0 branch and a second non-closure for β ≠ 0. This weakens the "A33 with η plus β" escape; it does not cover v3
  (β = η = 0).
- **L1:** the A5 ladder's 256³ rung gives ρ_NL −0.058 / −0.047 ("does not restore growth", indicative; 799a7af151). The L1 engine
  carries no gas expulsion; its KiDS score is KX against its own S0 (feedback-matched by construction; cf. CFG963).
