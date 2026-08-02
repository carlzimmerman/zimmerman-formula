# GAIA DR4 PRE-REGISTRATION FREEZE
## de Sitter-Unruh modified-inertia program — the two banked DR4 pipelines
**Frozen: 2026-07-16. Confrontation target: Gaia DR4 (~Dec 2026).**

---

### Purpose and freeze mechanism

Gaia DR4 will be confronted by exactly two pre-built pipelines in this directory.
Every analysis choice either pipeline makes — cuts, estimator, binning, error
model, statistic, decision bands — is frozen in this document BEFORE the data
exist. Nothing in the tables below may be changed after DR4 lands. The freeze is
enforced by SHA-256 hashes of the pipeline files (this directory is not a git
repository; the hashes are the mechanism). Any change after this date must be
recorded as a dated, clearly-labeled **POST-HOC AMENDMENT** appendix at the
bottom of this file — the original frozen choice is never edited, and any
post-hoc amendment must state what the frozen analysis returned first.

**Framework statement (own terms, not the standard-MOND lens):** modified
INERTIA with horizon-derived a0 = cH_Lambda/Z and the framework's own
dS-Unruh interpolation g_obs = sqrt(g_bar^2 + g_bar*a0), i.e.
nu(y) = sqrt(1 + 1/y). Both a0 footings are carried everywhere a0 enters
(working-rule 4): **canonical a0 = 9.36e-11 m/s^2** (rho_DE / cH_Lambda) and
**alt a0 = 1.13e-10 m/s^2** (rho_total / cH0).

**Honesty rules binding on the confrontation write-up:** no
"validates/proves/confirms" language — outcomes are stated as
consistent/disfavored-at-k-sigma/killed per the pre-declared bands below; the
gamma = 1.137 value is the modified-GRAVITY number and is never presented as
the framework-MI target (which is ~1.09, band 1.05–1.10); the s^TX margin is
~1.5x (the "~9.6x" figure is a superseded looser-bound corner and must not be
cited); s^TX outcomes are preferred-frame/Lorentz-violation verdicts,
MOND-family-shared, never MI-vs-MG verdicts.

### Freeze manifest (SHA-256)

| file | role | sha256 |
|---|---|---|
| `prep_2026/gaia_dr4_prep/wide_binary_pipeline.py` | FROZEN analysis pipeline, Door 4A | `669fecc4b42b0f0a23c263715d45c3a56cca112af70fccdc4ed95696d53bb4ff` |
| `prep_2026/gaia_dr4_prep/stx_dipole_template.py` | FROZEN analysis pipeline, Door 4B | `09cf51aef657292412ba0d647744b4470a0dcf58e6e192ba92475fe9930d506b` |
| `zimmerman-formula/real_research/reviews/wb_dr4_prereg_framework_curve.py` | banked theory-target script (read-only, frozen repo) | `6b8fad626067e076219f56309144b7d56c1050f129601b2d73f3286911ac3798` |
| `zimmerman-formula/real_research/reviews/stx_target.py` | banked s^TX prediction (read-only, frozen repo) | `1451b7810e48674f3d8759c484aee3bfd7b874836ca0e810de56d289bfab6987` |
| `zimmerman-formula/real_research/reviews/stx_inpop_recipe.py` | banked s^TX physics + kill ledger (read-only, frozen repo) | `8227bea52b9aa070769b767070cbd0146709c8cafab42432448d4cacd7b7aab1` |

Reproduction commands (both must exit 0):
`python3 wide_binary_pipeline.py --dry-run` and `python3 stx_dipole_template.py`.
Frozen RNG seed for both: **20261216**.

---

## SECTION 1 — Wide-binary gamma test (Door 4A)

### 1.1 Hypotheses and frozen theory targets

The observable is **gamma_v**, the deep-regime velocity-boost asymptote
(v_rms / v_rms,Newton). **Convention warning (frozen):** Chae-style
gravity-boost gamma = G_eff/G_N is the SQUARE of gamma_v. Published
force-boost numbers must be square-rooted before comparison
(e.g. Chae et al. 2026, arXiv:2601.21728: force gamma 1.600 (+0.171/−0.141)
= velocity gamma_v ≈ 1.26). All targets below are gamma_v.

> ### ⚠️ AMENDMENT 1 — 2026-07-27, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **The original table below had a scoring defect: it listed γ_v = 1.000 as the *Newtonian rival* only.
> On the framework's own committed action, 1.000 in the 2–30 kAU window is ALSO the framework's
> prediction.** As frozen, a Newtonian DR4 result would have been recorded as a kill of the framework
> when it may be a confirmation — and could not have been claimed afterwards without being post-hoc.
> This amendment fixes that, and it is entered *before* DR4 rather than after.
>
> **Why.** The framework carries a response gate `G(ω) = 1/(1 + iω/ω_c)` with
> ω_c ∈ [1.782, 2.211]×10⁻¹⁴ rad/s. A wide binary's *orbital* frequency at 10 kAU is
> Ω = 2.44×10⁻¹³ rad/s — **11× above the entire committed ω_c window** — so the gate is SHUT and the
> boost is suppressed by Re G ≈ 0.005–0.008.
> The question of whether the kernel senses the acceleration *magnitude* (constant on a circular orbit
> → gate open → 1.09 stands) or the orbital *frequency* (→ gate shut → 1.000) is now **SETTLED from the
> committed action**, not left open: `S_matter = −½∫√−g ρ_m [s uᵘ K(□_u/a₀²) u_μ]` with
> `□_u f = uᵃ∇_a(uᵇ∇_b f)`, and on a circular orbit **□_u u_μ = −Ω² u_μ identically** (sympy residual
> zero, `real_research/reviews/mi_dcac_branch_settled_2026.py`, 5/5). So K's argument is
> z = −(Ωc/a₀)² — a frequency. The acceleration magnitude, though genuinely constant, never enters the
> operator. **The gated (AC) branch is the framework's branch.**
>
> | amended hypothesis | γ_v target, 2–30 kAU | basis |
> |---|---|---|
> | Newtonian | 1.000 exactly | — |
> | **framework-MI, GATED (the framework's prediction)** | **1.0004–1.0006**, i.e. <0.04σ from Newton | `mi_wb_gate_fork_2026.py` (11/11), all four footing × ω_c-edge combinations |
> | framework-MI, ungated (superseded — retained for the record) | band 1.05–1.10, point 1.09 | the original row below |
>
> **So a Newtonian DR4 result in 2–30 kAU CONFIRMS the framework's gated branch and does NOT falsify
> it.** Conversely, a detection of γ_v ≈ 1.09 in that window would falsify the gated branch and revive
> the ungated one. Both outcomes are informative; neither is a free pass.
>
> **Where the framework IS falsifiable — the discriminating window moves outward.** The gate opens at
> r_gate = (GM/ω_c²)^(1/3), which exceeds the MOND radius r_M = √(GM/a₀) for every mass (ratio
> 4.54–7.76). Between them is a **dead zone**: sub-a₀ but gate-shut, hence Newtonian, running ~10 → ~50–60
> kAU for 1.5 M☉. Beyond r_gate the boost switches on as
> **γ_v − 1 ≃ ½[ν(y_ext) − 1](ω_c²/GM)s³** — exponent **exactly 3**, derived not fitted, amplitude fixed
> by ω_c, the measured pair mass and the Galactic field, with **zero free parameters**
> (`mi_wb_cubic_rise_2026.py`, 10/10). An n-pole gate would give s^(3n), so the measured log-slope
> returns the pole count as n = p/3 (`mi_wb_exponent_pipeline_2026.py`, 6/6). Every published
> contaminant channel rises as s^(1/2) instead. **FROZEN PREDICTION: p = 3.**
>
> **Pre-registered falsifiers of the gated branch**, any one of which kills it: (i) no excess beyond
> ~50 kAU in a contamination-controlled sample; (ii) an excess whose log-slope is inconsistent with 3;
> (iii) a knee that does not move as M^(1/3); (iv) an amplitude inconsistent with ω_c²/GM on both
> footings and both window edges; (v) γ_v ≈ 1.09 detected *inside* 30 kAU.
>
> **Power, and the honest limitation.** The shape test needs ~2000 clean pairs per separation bin for
> ~5σ separation of p = 3 from p = 0.5 (~400 gives only ~2.3σ). El-Badry, Rix & Heintz 2021 has, at
> d < 200 pc, only 436/270/155/60/24/3 clean pairs across the 30→236 kAU bins — **364 total beyond 50
> kAU**. So **this test cannot be run on DR3**; it requires DR4's astrometry and sample
> (`mi_wb_dr3_feasibility_2026.py`, 5/5). That is precisely why this amendment is entered now.
>
> **Unchanged by this amendment:** the a₀-degeneracy flag below still holds in full — DR4 γ_v constrains
> the ν+EFE+gate prescription, **not** the value a₀ = 9.36×10⁻¹¹, and no outcome may be reported as
> measuring a₀ or Z. a₀'s value, Z, s = −1 and ω_c remain POSTULATED. ω_c in particular is anchored by
> no independent argument and is the framework's most exposed quantity.
>
> **Still open, and newly sharpened:** on the frequency axis |K| = 1 exactly, so K contributes pure
> phase there and the entire magnitude suppression rests on the separate gate. Giving the gate the same
> frequency argument as K is now *consistent* rather than assumed — but the K/gate division of labour is
> underived. This amendment does not close that.

| hypothesis | frozen gamma_v target | source |
|---|---|---|
| Newtonian | 1.000 exactly | — |
| **framework-MI** (per-star MI-EFE prescription) | **band 1.05–1.10, point target 1.09** (dynamical asymptote 1.1015, observable-diluted edge 1.0508) — ⚠️ **SUPERSEDED for 2–30 kAU by Amendment 1: this is the UNGATED number** | banked `wb_dr4_prereg_framework_curve.py` (asserts 1.095 < asy < 1.105), rerun 2026-07-16, exit 0 |
| framework-as-MG (AQUAL-EFE point-field, framework nu) | 1.137 (computed 1.1389) | same banked script (asserts \|asy − 1.137\| < 0.005) |
| conventional-MOND benchmark | 1.33 (dynamic-range injection only; Milgrom a0 + literature-scale EFE asymptote — NOT a framework number) | pipeline injection ladder |

Frozen flags carried with the targets:
- **Prescription flag** (banked, verbatim honored): the per-star MI-EFE law is
  a prescription, not a completion — the band 1.05–1.10 is a
  prescription+observable bracket, not a theorem.
- **a0-degeneracy** (computed in the banked script): Milgrom-a0 MI asymptote
  1.134 ≈ framework-a0 MG 1.139. A 22% a0 shift moves gamma_v by 3.3%.
  **DR4 gamma_v constrains the nu+EFE prescription, NOT the value
  a0 = 9.36e-11.** No outcome below may be reported as measuring a0.
- **External field (frozen both ways):** primary g_ext,obs = 1.778e-10 m/s^2
  (= 1.9 a0_can, McMillan-2017-class solar neighborhood; the value the banked
  targets are computed at). Alt convention g_ext = Vc^2/R0 = 2.078e-10
  (Vc = 229 km/s, R0 = 8.178 kpc, per the repo Saad-Ting confrontation
  script). Higher g_ext → more EFE Newtonization → LOWER MI and MG asymptotes.
  Both g_ext values are frozen now; targets are quoted at the primary and the
  alt is reported alongside by mechanically rerunning the banked script — no
  new freedom at confrontation time.
- **Both a0 footings:** binning and y_extN run both ways always
  (canonical y_extN = 1.4647; alt y_extN = 1.1513). Gate-measured recovery
  spread between footings ≤ 0.005 in gamma — the footing is non-diagnostic
  here; canonical decides, alt is always reported.


> ### ⚠️ AMENDMENT 2 — 2026-07-30, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **(a) What changed.** Section 1.1 carries a frozen flag on its own MI target: *"the per-star MI-EFE
> law is a PRESCRIPTION, not a completion — the band 1.05–1.10 is a prescription+observable bracket,
> not a theorem."* As of 2026-07-30 that is no longer true. The EFE is **derived** from Theorem B
> (⟨□_u⟩_u = +|a|², exact on every timelike worldline): the closure's argument is the squared magnitude
> of the **total** four-acceleration, so the external field enters in **quadrature with a vector cross
> term** and no multiplying phase function θ(ω_ex/ω_in) is available. Published as Theorem 5 of
> *Structural Theorems for de Sitter–Unruh Modified Inertia*, DOI 10.5281/zenodo.21707845.
>
> **(b) THE FROZEN TARGET SURVIVES — no number is being moved.** Re-deriving γ_v from the derived law
> at the frozen g_ext values gives an orientation-averaged **γ_v = 1.0799**, which lies inside the
> frozen band (1.05–1.10) and sits **0.0101** from the frozen point target 1.09. The full nonlinear
> two-body solve agrees with the linear-response derivation to 0.0014 in γ_v. This amendment therefore
> **adds** information rather than shifting a target after the fact, which is the only honest form a
> pre-data amendment can take.
>
> **(c) One flag is discharged, one is NOT.** The *prescription flag* above is discharged: the law is
> now a theorem within the first-moment closure family. The **a0-degeneracy flag is untouched** and
> still binding — no DR4 outcome may be reported as measuring a₀ = 9.36e-11.
>
> **(d) NEW PHYSICS THE FROZEN PIPELINE AVERAGES AWAY: the EFE is ANISOTROPIC.** Because the cross term
> is a vector, the response to the internal field is a **tensor**, with eigenvalues
> γ²∥ = d(νg)/dg|_g_ext (separation along g_ext) and γ²⊥ = ν(g_ext) (perpendicular). At the frozen
> primary g_ext = 1.778e-10 and canonical a₀:
>
> | orientation | derived γ_v |
> |---|---|
> | separation ∥ g_ext (toward/away from Galactic centre) | **1.0112** |
> | separation ⊥ g_ext | **1.1115** |
> | isotropic average (what the frozen scalar fit measures) | **1.0799** |
>
> The spread is **0.1004 in γ_v = 3.6× the frozen σ_tot = 0.028**, and it exceeds σ_tot on *every*
> footing and g_ext convention (0.0888–0.1158, i.e. 3.2–4.1 σ_tot). The frozen §1.3 estimator fits a
> single scalar γ_v and averages this away.
>
> **(e) ADDED STATISTIC (pre-registered here, before data).** Alongside — never substituted for — the
> frozen scalar fit, run an **orientation-resolved** fit: bin pairs by the angle between the projected
> relative-separation vector and the Galactic-centre direction, and fit γ_v per bin using the otherwise
> unchanged frozen estimator, cuts, error model and strictness ladder.
>
> **(f) SIGN PRE-DECLARED, so the new statistic cannot be read post-hoc.** **Perpendicular pairs must
> show the LARGER boost.** A measured anisotropy of the opposite sense at ≥3σ falsifies the derived EFE
> **independently of the aggregate γ_v**, and must be reported as such. A null anisotropy at the
> frozen allowances is *not* a kill, because (h) below shows the observable spread is diluted.
>
> **(g) This does NOT rescue MI-vs-MG.** The derived average sits +0.0571 from the frozen MG target
> 1.137, still inside the pre-declared "MI-vs-MG is NOT decided in this zone" band. The §1.5 forecast
> that MI-vs-MG is **likely undecidable in DR4** stands unamended.

> ### ⚠️ AMENDMENT 3 — 2026-07-30, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **(a) WHAT CHANGED, AND IT IS A THEORY CHANGE, NOT A REINTERPRETATION.** The framework has adopted an
> **α ≥ 2** interpolation, replacing ν(y) = √(1+1/y) (α = 1). Reason, computed in
> `real_research/reviews/mi_disformal_tail_freedom_2026.py` and
> `real_research/reviews/mi_alpha2_migration_2026.py`: the α = 1 tail forces a constant sunward
> anomaly a₀/2 that is **1279× the Earth 2σ ephemeris bound** (Sereno & Jetzer 2006 Table 1 through
> their Eq. 9) and drives the disformal lensing construction's own B < 1 premise past **257×** across
> Mercury→Saturn — while buying **+0.0033 dex** on 175 SPARC galaxies (0.10 σ_int), which the data
> cannot resolve. **Crucially, a₀'s derivation does not depend on α = 1:** the α = 2 kernel
> K = √(z/(1+z)) satisfies every premise that derivation uses — Herglotz–Nevanlinna positivity,
> passivity sup K = 1, the unit sum rule ∫dμ/|t| = K(∞) − K(0) = 1, the horizon floor — and its spectral
> measure ρ(s) = (1/π)√(s/(1−s)) on 0 < s < 1 is *simpler* than the α = 1 measure (single region,
> compact support, finite mass 1/2, no additive constant), verified against the closed form to 1e-14
> over eight decades. So a₀ = cH_Λ/Z is unaffected. What is withdrawn is the word **exact**.
>
> **(b) THE FROZEN γ_v TARGETS MOVE. This is the amendment.** Re-deriving through Amendment 2's own
> quadrature-EFE construction (machinery reproduced against Amendment 2's α = 1 numbers to 0.0008)
> with the α = 2 kernel:
>
> | quantity | frozen (α = 1) | **amended (α = 2)** |
> |---|---|---|
> | framework-MI, orientation-averaged, primary g_ext / canonical a₀ | 1.0799 (point target 1.09, band 1.05–1.10) | **1.0246** |
> | framework-MI, full range over both footings × both g_ext | — | **1.0182 – 1.0350** |
> | framework-as-MG (scalar μ(a_ex/a₀)) | 1.137 | **1.0473 – 1.0885** |
> | γ_v ∥ g_ext (primary/canonical) | 1.0112 | **0.9669 — sub-Newtonian** |
> | γ_v ⊥ g_ext (primary/canonical) | 1.1115 | **1.0523** |
>
> The MI prediction now sits **below the frozen band's lower edge (1.05) on every footing/g_ext
> combination**, and moves by 0.0553 = **2.9σ** at the frozen DR4 error model (σ(γ_v) = 0.0191,
> N = 30,000). **The frozen band 1.05–1.10 and point target 1.09 are hereby superseded** by the range
> in the table. Everything else in §1.3 — the estimator, the frozen cuts, the error model, the
> strictness ladder, the NSS screen — is **unchanged**.
>
> **(c) THE PRE-DECLARED ANISOTROPY SIGN IS PRESERVED AND STRENGTHENED.** Amendment 2 (f) pre-declared
> that **perpendicular pairs must show the larger boost**. Under α = 2 that still holds, and more
> sharply: the parallel direction goes **sub-Newtonian** (γ_v ∥ = 0.962–0.972 on all four combinations)
> while perpendicular stays above 1. So Amendment 2's falsifier is not weakened — a measured anisotropy
> of the opposite sense at ≥3σ still kills the derived EFE independently of the aggregate γ_v.
>
> **(d) WHY THIS AMENDMENT IS LEGITIMATE AND ONE PROPOSED EARLIER THE SAME DAY WAS NOT.** Earlier on
> 2026-07-30 a Milgrom-2022 θ(0)-driven amendment was drafted and then **withdrawn**: it rested on a
> multiplying phase function θ(ω_ex/ω_in) that this framework provably cannot use (the kernel is exactly
> unimodular on the oscillatory branch, and Theorem B forces quadrature rather than Milgrom's linear
> a_in + θa_ex — as Amendment 2 (a) already stated). That was a change of *analysis* on an inapplicable
> basis, and amending a frozen target for it would have been illegitimate. **This** amendment is a change
> of *theory*, made by the owner, declared before data, with its cost computed and its losses stated. The
> distinction is the whole point of pre-registration and is recorded here deliberately.
>
> **(e) WHAT THIS AMENDMENT DOES NOT DO.** It does not touch the a₀-degeneracy flag, which remains
> binding: no DR4 outcome may be reported as measuring a₀ = 9.36e-11. It does not change §1.5's forecast
> that MI-vs-MG is likely undecidable in DR4 — under α = 2 the MI (1.0246) and as-MG (1.0631, primary/
> canonical) values separate by 0.0385 = 2.0σ, still inside the pre-declared undecidable zone. And it
> does not migrate the 267 other corpus scripts still computing on the α = 1 kernel; their numbers are
> α = 1 results until re-derived.

>
> **(h) Scope, stated so the added statistic is not oversold.** The eigenvalue calculation is
> equal-mass and deep-regime, and the observable angle is a **projection**. Unequal mass ratios and
> projection both **dilute** the anisotropy, so 0.1004 is an **upper bound** on what DR4 can see, not a
> forecast. The dilution factor is not computed here and must not be assumed to be unity at scoring.
>
> **(i) Prior art, credited.** An anisotropic effective gravity in an external field is a **known**
> feature of MOND-type EFE treatments (Milgrom; Banik & Zhao and others have discussed it for wide
> binaries). Novelty here is confined to (i) its **derivation** from this framework's action rather
> than prescription, and (ii) the specific frozen numbers above.
>
> **(j) Related tightening, recorded for completeness.** The off-circular closure ambiguity — directly
> relevant because wide binaries are eccentric — was narrowed from ~570% to **7.9%** on 2026-07-30
> (`real_research/reviews/mi_offcircular_closure_collapse_2026.py`, published in DOI
> 10.5281/zenodo.21702746). This removes a named liability on the WB prediction but changes no frozen
> target. The residual weighting freedom within the first-moment family remains open, and is now
> testable via dispersion-supported systems at ~1.2–1.9σ on archival data (Prop 7 of the same paper).
>
> **(k) Verification.** All numbers in this amendment are produced by
> `prep_2026/gaia_dr4_prep/amendment2_derived_efe.py` (exit 0, 6 internal checks, output committed
> alongside as `.out`). Nothing in Sections 1.1–1.6 above is edited; this block is additive.


> ### ⚠️ AMENDMENT 4 — 2026-07-31, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **This is an ARITHMETIC CORRECTION to Amendments 2 and 3, not a change of theory.** It was found by
> adversarial audit of this document, and it runs *against* the framework. Verified by
> `real_research/reviews/mi_prereg_gext_argument_audit_2026.py` (exit 0, 16 structural checks, output
> committed alongside as `.out`).
>
> **(a) WHAT THE FROZEN ANALYSIS RETURNED FIRST.** Amendment 2 (α = 1): γ_v ∥ = 1.0112, γ_v ⊥ = 1.1115,
> orientation-averaged 1.0799. Amendment 3 (α = 2): γ_v ∥ = 0.9669, γ_v ⊥ = 1.0523, orientation-averaged
> 1.0246, full range 1.0182–1.0350.
>
> **(b) THE DEFECT.** The framework's interpolation is defined with the **Newtonian** argument,
> a = ν(y)·g_bar with y = g_bar/a₀. Both amendments instead evaluate ν and d(νg)/dg at
> **g_ext,obs / a₀ = 1.8996** — the *observed* ratio. This is demonstrated, not asserted: feeding the
> observed ratio reproduces the frozen table to **3.3e-5** (Amendment 3) and **7.9e-4** (Amendment 2),
> while the closure-inverted Newtonian argument misses it by **1.1e-2** and **2.8e-2** — a 330×
> discrimination. §1.1 of this document *already publishes the correct quantity* (`y_extN`), and §3's
> gate shape uses it; the amendments bypassed it. **This is the same bug class STANDING §5.1 records
> from the Lyman-α forest chain**, where a response kernel evaluated at the Newtonian instead of the
> observed argument inflated every significance by 1.9–5.6×.
>
> **(c) A SECOND, INDEPENDENT DEFECT.** §1.1's `canonical y_extN = 1.4647; alt y_extN = 1.1513` are the
> **α = 1** closure inversions of g_ext,obs (confirmed to 4.3e-4 / 3.2e-4). Under the **α = 2** kernel in
> force since 2026-07-30 the inversions are **1.6809** and **1.3280**. Those published `y_extN` values
> are therefore **stale** with respect to Amendment 3's own kernel, independently of (b).
>
> **(d) THE CORRECTED TARGETS. These supersede the Amendment 3 table.**
>
> | quantity | Amendment 3 (as frozen) | **Amendment 4 (corrected)** |
> |---|---|---|
> | framework-MI, orientation-averaged, primary g_ext / canonical a₀ | 1.0246 | **1.0310** |
> | framework-MI, full range over both footings × both g_ext | 1.0182 – 1.0350 | **1.0218 – 1.0472** |
> | γ_v ∥ g_ext (primary/canonical) | 0.9669 | **0.9636 — still sub-Newtonian** |
> | γ_v ⊥ g_ext (primary/canonical) | 1.0523 | **1.0631** |
> | `y_extN` fed to ν (canonical / alt), α = 2 | 1.4647 / 1.1513 (α = 1 values) | **1.6809 / 1.3280** |
>
> **(e) BOTH OF AMENDMENT 3's CONCLUSIONS SURVIVE — computed, not hoped.** (i) The MI prediction still
> sits **below the frozen band's lower edge 1.05 on all 4/4** footing × g_ext combinations (corrected
> range 1.0218–1.0472). (ii) γ_v ∥ stays **sub-Newtonian on all 4/4** (0.9592–0.9688), so Amendment 2 (f)
> and Amendment 3 (c)'s pre-declared anisotropy sign is intact. The correction moves the
> orientation-averaged γ_v by 3.6e-3 to 2.9e-2 — **88× to 716×** the 4.1e-5 accuracy at which the frozen
> table reproduces, so the defect is real; but far too small to flip any pre-registered PASS/FAIL.
>
> **(f) THE ERROR RAN AGAINST THE FRAMEWORK, and that is recorded deliberately.** On every footing and
> both kernels the as-frozen numbers are **more Newtonian** than the corrected ones (|γ−1| = 0.0246 vs
> 0.0310 at α = 2 primary/canonical). The defect was making this framework's wide-binary prediction look
> *closer* to Newton — i.e. *less* detectable — than its own kernel implies. It manufactured a deficit,
> not a win.
>
> **(g) THE UPPER EDGE IS BREACHED, AND THE SURVIVING MARGIN IS THIN.** Independently reproduced by
> `real_research/reviews/mi_dragged_frame_consolidation_2026.py` (100 checks, 6 mutation controls all
> killed, exit 0), which identifies the convention rather than assuming it: mutating to the *consistent*
> convention returns 1.030988. Two consequences beyond (d)–(e):
> - The worst corner goes 1.0350 → **1.047199**, **breaching Amendment 3's own frozen upper edge by
>   0.0122 = 0.639 σ_fit.** That range endpoint is superseded by the (d) table.
> - Amendment 3's decisive conclusion ("MI below 1.05 on every combination") survives, but its **worst
>   margin is cut 5.36×: 0.786 σ_fit → 0.147 σ_fit.** It is now a *thin* pass, not a comfortable one, and
>   must be reported that way at scoring.
>
> **(h) TWO FURTHER DEFECTS, found in the same audit and NOT corrected here — reported so they are on the
> record before DR4.** (i) **Amendment 1's gated row is stale under α = 2**: it carries 1.0004–1.0006,
> where the α = 2 kernel implies **1.00012–1.00020**. (ii) **Amendments 2 and 3 use mismatched
> orientation-averaging conventions** — no single fixed convention reproduces both frozen averages, missing
> one of them by 6.4e-4 to 1.2e-3 (the frozen document itself declares 0.0008). (iii) Two sub-1e-3
> provenance wrinkles: §1.1's `y_extN = 1.4647` comes from rounding g_ext/a₀ to exactly 1.9, and its
> `alt y_extN = 1.1513` implies a₀_alt = 1.1298e-10 rather than the mandated 1.13e-10. None of (i)–(iii)
> moves a verdict; all three are owed a correction.
>
> **(i) SCOPE — what is NOT corrected here, so this block is not read as complete.** Only the
> framework-MI eigenvalues are recomputed. Amendment 3's **framework-as-MG row (1.0473–1.0885)** uses a
> scalar μ(a_ex/a₀) prescription that plausibly carries the *same* argument error and is **not corrected**;
> the **§2 s^TX Door-4B** numbers were not examined at all. Neither may be assumed sound because the MI
> row has been fixed. Both are owed a separate audit.
>
> **(j) A FALSIFIABILITY TRAP IS FLAGGED BUT NOT RESOLVED, and resolving it is the owner's call.** The
> **gate branch** (knee 43–72 kAU, slope p = 3) and the **frame branch** (knee 532–603 kAU, beyond any
> bound pair) between them cover **both outcomes** of the frozen >50 kAU shape test, and both predict
> Newton in 2–30 kAU at γ_v − 1 ≈ 1.0–1.5e-6 — 17 883× below the frozen lower edge 1.0182. **A test that
> cannot fail is not a test.** One branch must be committed to in the open before DR4 lands, or the shape
> test struck. This amendment does **not** make that choice.
>
> **(h) WHAT THIS AMENDMENT DOES NOT DO.** It does not touch the a₀-degeneracy flag: no DR4 outcome may
> be reported as measuring a₀ = 9.36e-11. It does not change the estimator, the frozen cuts, the error
> model, the strictness ladder, or the NSS screen. It does not change κ = 1/2, which remains **fitted,
> not derived**. And it does not alter the standing rule that a confirmation of a frozen prediction is
> scored as a **kill** where the pre-registration says so.

> ### 🚨 AMENDMENT 5 — 2026-08-02, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **§2's s^TX AMPLITUDE IS BUILT ON THE RETIRED α = 1 KERNEL AND COLLAPSES BY SIX ORDERS OF MAGNITUDE.
> A TEST THIS DOCUMENT DECLARED LIVE AND FALSIFIABLE IS NOT.** This is the amendment with the largest
> consequence of any filed so far, and it is filed against interest.
>
> **THE DEFECT.** §2 builds the boost dipole from `S → a₀/(2|g_orb|)`, the deep-Newtonian tail of the
> **α = 1** closure. Symbolically the two kernels differ in FORM, not in coefficient: α = 1 gives
> x − y → ½, a **constant** offset a₀/2, so A₁ = a₀/2g; α = 2 gives x − y → 1/(2y), a **decaying**
> offset, so A₂ = a₀²/2g². Hence
>
> $$A_2/A_1 \;=\; a_0/g \;=\; 1.45\times10^{-6}\ \text{ at Saturn.}$$
>
> The α ≥ 2 kernel has been in force since 2026-07-30 (Amendment 3), because the α = 1 tail implies a
> constant sunward anomaly a₀/2 at **1279× the Earth 2σ ephemeris bound**. So the kernel that §2's
> amplitude assumes is the one this document already retired.
>
> **THE NUMBERS.** |s^TX| falls **8.68e-10 → 1.258e-15** (canonical) and **1.048e-9 → 1.834e-15** (alt).
> The pre-registered margin goes from a live **1.50× / 1.24×** to **1.03e6× / 7.09e5×**. Reproducing the
> frozen 1.50×/1.24× exactly confirms the normalisation is this document's own, not the auditor's.
>
> **THE SIGN IS UNCHANGED.** The collapse factor a₀/g is positive, so the pre-declared **NEGATIVE** sign
> survives intact. Only the amplitude dies. No post-hoc sign freedom is created or claimed.
>
> **WHAT THIS COSTS, STATED PLAINLY.** Amendment 4 moved numbers without flipping any pre-registered
> outcome. **This one flips an outcome: a test declared LIVE and FALSIFIABLE becomes untestable.** The
> α ≥ 2 switch cured the 1278× ephemeris liability for 0.0033 dex on SPARC — and it also destroyed the
> s^TX front as a falsifier. **That cost was not priced when the switch was made.** Combined with the
> separate finding that a locally-dragged frame flips the s^TX sign, the s^TX front is **doubly
> compromised**, and the α = 2 one binds because α = 2 is in force.
>
> **SCORING CONSEQUENCE.** §2's DETECT / KILL / WRONG-SIGN-KILL bands are **VOID under α = 2**. No DR4
> s^TX result may be scored against them. The front reverts to NO-VERDICT by construction, not by data.
> The **direction** lock (Planck apex, component ratios 0.208:−0.971:−0.120) and the **negative sign**
> lock are unaffected and remain frozen.
>
> **WHAT IS NOT CHANGED.** Not the wide-binary sections. Not the estimator, cuts, error model, strictness
> ladder or NSS screen. Not the a₀-degeneracy flag: no DR4 outcome may be reported as measuring
> a₀ = 9.36e-11. Not κ = ½, which remains **fitted, not derived**.
>
> Source: `real_research/reviews/mi_stx_alpha2_collapse_2026.py` (10 checks, exit 0, both footings).
> Author-verified from scratch: every adversarial verifier and the critic died on a spend limit, so
> nothing here rests on an unrefuted subagent claim.

> ### 🚨 AMENDMENT 6 — 2026-08-02, ADDED IN THE OPEN BEFORE DR4. READ BEFORE SCORING.
>
> **AMENDMENT 1's BASIS IS WITHDRAWN, AND THE WIDE-BINARY BRANCH INVERTS. The registered γ_v target of
> 1.0004–1.0006 is not the framework's prediction; the UNGATED value is.** Filed against interest,
> because it removes a hedge this document created for the framework's benefit.
>
> **WHAT AMENDMENT 1 DID.** It cited `mi_dcac_branch_settled_2026.py` by name as having SETTLED the
> DC/AC branch "from the committed action", on the strength of "□_u u_μ = −Ω² u_μ identically (sympy
> residual zero)", and on that basis registered **γ_v = 1.0004–1.0006, <0.04σ from Newton**, declaring
> that "a Newtonian DR4 result in 2–30 kAU CONFIRMS the framework's gated branch and does NOT falsify it."
>
> **WHY THAT BASIS FAILS — three defects, increasing in seriousness.**
> **(i)** The eigenvector identity is **FALSE AS STATED.** It was verified on a two-component *spatial*
> vector; the time leg was never formed. On the actual 4-velocity □_u annihilates u⁰ (eigenvalue **0**)
> while the spatial legs give **−(γΩ)²**, so u_μ is **not** an eigenvector. A mutation control reproduces
> the false PASS by deleting the time leg, isolating the defect exactly.
> **(ii)** Pulling K out of the contraction as K(z)(u·u) = −K(z) requires a genuine eigenvector. The
> correct block value is **+γ²v²K(z)** — opposite SIGN and suppressed by (v/c)², a factor **6.75e11** at
> the wide-binary scale this was written to decide.
> **(iii) DECISIVELY, THE STRATEGY FAILS.** Selecting the branch by reading □_u off the action selects the
> reading in which the action's modification is **amplitude-free** — |K| → 1 at every real system, on both
> kernels and both footings, against a law requiring μ_fw(1) = 0.618. That is the reading in which the
> framework has **no rotation curves at all**. A wide-binary prediction cannot be settled by the reading
> that deletes the galaxy phenomenology.
>
> **AND IT INVERTS, without needing ω_c at all.** A one-pole low-pass **passes DC with unit gain**
> whatever ω_c is, and |a| is **exactly constant** on a circular orbit (the Jul 27 script verified that
> itself). So Amendment 1's Re G = 0.005–0.008 suppression **does not apply** on the branch the
> framework's phenomenology actually uses, and γ_v reverts to the **UNGATED** value.
>
> | amended hypothesis | γ_v target, 2–30 kAU |
> |---|---|
> | Newtonian | 1.000 exactly |
> | **framework-MI, UNGATED (the framework's prediction under α = 2)** | **≈ 1.02** |
> | framework-MI, ungated under the retired α = 1 | band 1.05–1.10, point 1.09 |
> | framework-MI, GATED (Amendment 1 — **basis withdrawn**) | 1.0004–1.0006 |
>
> **SCORING CONSEQUENCE, AND IT CUTS AGAINST THE FRAMEWORK.** Amendment 1 existed to stop a Newtonian DR4
> result being scored as a kill. **That hedge is withdrawn.** A Newtonian result in 2–30 kAU is once again
> evidence AGAINST the framework's wide-binary prediction, and γ_v ≈ 1.02 is a real risk taken in advance.
> **This must not be re-hedged after DR4 lands.**
>
> **ONE THING IT DOES NOT DO, stated so this is not read as more than it is.** Withdrawing the gate branch
> removes only **ONE** of this document's two routes to a Newtonian reading. The **locally-dragged FRAME**
> branch reaches γ_v − 1 ≈ 1.0–1.5 × 10⁻⁶ independently, with **no gate involved** (17 878× below the
> frozen undragged lower edge 0.0182). What remains of that branch is a single ajar door —
> **screening + differential drag**. So the falsifiability trap is **NARROWED from two branches to one,
> NOT resolved**, and committing to one branch in the open remains owed.
>
> **ALSO WITHDRAWN.** The **DEAD ZONE** prediction (r_gate/r_M = 4.54–7.76, the ~10→50–60 kAU window for
> 1.5 M☉) was AC-conditional and goes with the branch. And ω_c is not a forced ingredient of the
> framework: on the magnitude branch K's own argument already separates the Earth (|a|/a₀ ~ 10⁷) from a
> galactic orbit (~1), which is ordinary MOND logic needing no gate. Read with §1's "ω_c is a free
> parameter", the gate is **neither forced nor anchored**.
>
> **WHAT IS NOT CHANGED.** Not §2 (see Amendment 5). Not the estimator, frozen cuts, error model,
> strictness ladder or NSS screen. Not the 16-row cut table. Not the a₀-degeneracy flag. Not κ = ½,
> **fitted, not derived**. And no measurement moves: the SPARC RAR at 0.108 dex, the a₀-line and the flat
> curves are measurements against a LAW and are untouched.
>
> Sources: `real_research/reviews/mi_dcac_branch_verdict_withdrawn_2026.py` (29 checks, exit 0, both
> footings, mutation control isolating the defect), building on `mi_action_eom_vs_rar_2026.py` and
> `mi_dcac_split_settled_2026.py`. The superseded file carries a WITHDRAWN notice at its head.


### 1.2 Frozen DR4 cut list

The DR4 catalog fed to the pipeline (`--catalog`, columns
`sep_kAU, v_perp_kms, M1_msun, M2_msun, d_pc`) MUST be built with exactly
these cuts. This table is mirrored in the code (`FROZEN_DR4_CUTS`).

| # | cut | frozen value | a-priori ground |
|---|---|---|---|
| 1 | Galactic latitude | \|b\| > 15 deg | Banik et al. 2024 (MNRAS 527, 4573) §2.1 — crowding/extinction |
| 2 | magnitude | G < 17 both components | Banik+24 §2.1; astrometric error model validity; MS mass calibration |
| 3 | distance | d < 250 pc (parallax > 4 mas) | Banik+24 §2.1 |
| 4 | parallax S/N | ≥ 40 both components | distance error < 2.5% → vtilde error < 4%, subdominant to the 5% mass error; non-binding for most of the G<17, d<250 pc DR4 sample (guards tails only) |
| 5 | parallax consistency | \|d1 − d2\| < min(4 sigma, 8 pc) | Banik+24 §2.1 |
| 6 | projected separation | 2 < s < 30 kAU | Banik+24; the MOND radius r_M(1 Msun) ≈ 7 kAU sits inside the window (deep-regime leverage); > 30 kAU = chance-alignment + Galactic-tide regime |
| 7 | RUWE | < 1.4 both | Gaia DPAC single-star threshold (Lindegren 2018 TN; Lindegren+21); RUWE inflation traces unresolved companions (Belokurov+20, MNRAS 496, 1922) — a direct contamination screen |
| 8 | ipd_frac_multi_peak | ≤ 2 both | Banik+24 §2.4.3 — resolved blends |
| 9 | extinction | A_V < 0.5 | Banik+24 §2.4.1 |
| 10 | total mass | 0.464 < M_tot < 4.31 Msun | validity range of the Banik+24 eq.6 cubic M_G→M (M_G in [0.6, 11.1]); outside it the inversion is non-physical |
| 11 | RV consistency | reject \|dRV\| > max(3 sigma_dRV, 3 v_c(s_proj)) where both components carry DR4 RVs | Banik+24 §2.4.5 (his own screen; ~3.5% loss at DR3) — hierarchical triples induce km/s-scale dRV vs ≤ ~1.4 km/s orbital ceiling at s ≥ 2 kAU, M_tot ≤ 4.31 |
| 12 | **NSS screen (NEW, DR4-enabled)** | reject pairs where either component has ANY DR4 non-single-star solution (astrometric orbit, acceleration, or spectroscopic orbit) | DR4's 66-month epoch astrometry is the designed detector for exactly the undetected inner companions that inflate gamma — the direct cut on the contamination axis that DR3 lacked |
| 13 | resolved-triple search | no co-moving third Gaia source (parallax within 3 sigma, PM within 5 sigma of the pair) with G < 20 within projected 30 kAU of either component | Banik+24 faint-companion search analog (his m_G < 20 depth) |
| 14 | chance alignment | R_chance_align < 0.01 (El-Badry-style statistic recomputed on DR4) | El-Badry, Rix & Heintz 2021 (MNRAS 506, 2269): the > 99%-bound-probability subsample threshold (their own highest-confidence class); Chae 2023 (ApJ 952, 128) §2.1 uses the same value |
| 15 | vtilde error | sigma(vtilde) ≤ 0.1 max(1, vtilde/2) | Banik+24 eq.10 — bounds deep-bin noise inflation (D1-type diagnostic) |
| 16 | vtilde cap | **NONE at catalog level**; the estimator's symmetric cap vtilde < 6.0 applies identically to data and forward model | symmetry between data and model MC (Banik's catalog-level vtilde ≤ 5 is NOT adopted for DR4; it appears only in the DR3-era dry-run transcription, and an asymmetric catalog cap the model does not share would bias the medians) |

**Frozen strictness ladder** (each run alongside the primary, never substituted
for it): RUWE 1.4 → 1.2; R_chance 0.01 → 0.001; separation 2–30 → 3–20 kAU;
RV-screened subsample only; NSS screen OFF (as a contamination probe — the
off/on shift measures the contamination the screen removes).

### 1.3 Frozen estimator and statistic (exactly as coded)

- Observable per pair: vtilde = v_perp / sqrt(G M_tot / s_proj).
- Binning: median(vtilde) in 8 bins of log10(y_proj), y_proj = g_N(s_proj)/a0,
  frozen edges **[−1.5, −1.1, −0.8, −0.5, −0.2, 0.1, 0.5, 1.0, 2.2]**;
  bins with < 80 pairs dropped; symmetric outlier cap vtilde < 6.0;
  per-bin errors: 200-resample bootstrap of the median.
- Forward model: Newtonian Kepler population MC (3,000,000-pair master, sized
  so its finite-MC error is subdominant; that error is bootstrapped at a
  reference gamma and propagated — ignoring it produces a ±1–2% pseudo-bias,
  found and fixed at the gate), thermal f(e) = 2e primary, DR4 noise
  (§1.4), 5% Gaussian mass scatter, masses via the Banik+24 eq.6 cubic.
- Fit: 1-parameter profile chi2 for the deep asymptote gamma_inf over the
  frozen grid **0.90 to 1.50, step 0.0025**, with the EFE-saturated transition
  shape gamma(y) = 1 + (gamma_inf − 1) · y_extN/(y_extN + y),
  y_extN = framework-inverted external field (primary g_ext §1.1).
- Nuisance: one multiplicative kappa (eccentricity-calibration mismatch),
  **anchored** as a Gaussian prior on the high-acceleration bins
  (log10 y ≥ 0.5, boost ≈ 1 for every gamma on the grid) and profiled
  analytically over the deep bins. (A fully-free kappa is degenerate with
  gamma and biases it low by ~0.01–0.05 — found and fixed at the gate.)
  **Frozen kappa acceptance window: [0.95, 1.05].** kappa outside the window
  = eccentricity/anchor calibration mismatch → the verdict is downgraded to
  "systematic-limited" (§1.5), never re-tuned.
- 1-sigma from delta-chi2 ≤ 1; the quoted sigma(gamma) is
  **max(profile sigma, independent-realization rms)** (the pipeline's own
  conservative rule).
- Shape caveat (frozen): injection and recovery share the transition shape by
  construction — the gate certifies ASYMPTOTE RECOVERY, not shape
  discrimination. The confrontation must also overlay the banked exact
  framework curve (`wb_dr4_prereg_framework_curve.py`); shape
  mis-specification is a flagged systematic, not a tunable.

### 1.4 Frozen error model

DR3 per-star sigma_pm, sigma_plx vs G interpolated from Lindegren et al. 2021
(A&A 649, A2) grid as tabulated in the code; DR4 scaling frozen at
**sigma_pm × (66/34)^−1.5 = 0.372** and **sigma_plx × (66/34)^−0.5 = 0.718**
(nominal mission scaling; flagged APPROX). Mass calibration error: 5% Gaussian
per pair (Banik+24 quote ~5.5%, §2.3.3). If DR4's published per-source errors
differ from this model, the pipeline uses the PUBLISHED DR4 errors and the
model-MC noise is regenerated from them — that is a mechanical substitution,
not a re-tune, and is recorded in the amendment appendix.

### 1.5 Pre-declared decision bands

Let gamma_hat, sigma_fit be the pipeline output on the frozen-cut DR4 catalog
(canonical footing decides; alt footing reported). Frozen total error:

- **sigma_sys = 0.02** (frozen allowance), covering: eccentricity-model
  mismatch ±0.015 (gate-measured flat-vs-thermal shift −0.015; the
  Hwang+22-preferred SUPERTHERMAL population lies beyond thermal on the same
  axis and is covered at the same magnitude with opposite sign — flagged),
  a0-footing spread ≤ 0.005, residual shape/g_ext dependence.
- **sigma_tot = sqrt(sigma_fit^2 + 0.02^2)**.

Verdict rule (frozen): z_H = (gamma_hat − gamma_H)/sigma_tot for each
hypothesis H in {1.00, 1.09 [band 1.05–1.10], 1.137, 1.33}.
"**Consistent with H**" requires |z_H| < 2; "**H disfavored**" requires
|z_H| > 3; "**supports H over H'**" requires BOTH |z_H| < 2 AND |z_H'| > 3.

Expected DR4 numbers (from the gate, N = 30,000 assumed; if DR4 yields a
different N after the frozen cuts, sigma_fit scales as sqrt(30000/N) —
mechanical, no freedom): sigma_fit ≈ 0.019, sigma_tot ≈ 0.028. Illustrative
band edges at sigma_tot = 0.028:

| gamma_hat lands in | pre-declared reading |
|---|---|
| ≤ 1.007 | supports Newtonian over framework-MI (MI disfavored > 3 sigma); a Newton-side verdict is contamination-ROBUST (contamination only pushes gamma UP) |
| 1.007 – 1.083 | no hypothesis separation at the frozen thresholds — report as undecided with the z-table |
| 1.083 – 1.145 | non-Newtonian at ≥ 3 sigma AND framework-MI-compatible; **MI-vs-MG is NOT decided in this zone** (1.137 lies inside it); requires the ladder-stability + kappa-window + contamination tests to pass, else "systematic-limited" |
| 1.145 – 1.20 | MG-side; MI disfavored per z; same ladder requirements |
| > 1.20 | **contamination-guard zone**: above every EFE-saturated target, approaching the no-EFE benchmark — pre-declared reading is "contamination-dominated or EFE-shape failure", NO hypothesis verdict permitted (this is where the DR3 dry run landed, §1.6) |

Separation forecasts (frozen, statistical at N = 30k): Newton vs MI 1.09 at
3 sigma needs N ≳ 12,200 — expected DECIDABLE. MI 1.09 vs MG 1.137 at 3 sigma
needs N ≈ 45,000 statistically AND sigma_sys < 0.01 — pre-declared as
**likely UNDECIDABLE in DR4 at the frozen allowances**; no post-hoc shrinking
of sigma_sys may be used to claim it. MOND benchmark 1.33 separates from all
others at > 7 sigma.

Stability requirements for any non-Newtonian verdict (frozen): every
strictness-ladder variant (§1.2) must shift gamma_hat by < 1 sigma_fit; kappa
within [0.95, 1.05]; the NSS-off contamination probe must move gamma_hat
TOWARD the verdict value when the screen is turned ON. Any failure →
"systematic-limited, no verdict" — that outcome is reported, not repaired.

### 1.6 Contamination axis: mitigation plan and the DR3 dry run read honestly

**The axis:** undetected close companions (hierarchical triples) add orbital
velocity to v_perp and inflate gamma — contamination biases HIGH, mimicking a
boost, never a deficit. This is the known interpretation axis of the entire
wide-binary literature (Chae 2023 models hidden companions probabilistically;
Banik+24 rejects them by screens; their opposite conclusions — force-boost
detection vs Newtonian at 19 sigma — trace to exactly these choices).

**How the frozen cuts bound it:** four independent screens attack it — RUWE
< 1.4 (astrometric-wobble tracer, Belokurov+20), the DR4 NSS screen (direct
66-month orbit/acceleration detection — the qualitatively new DR4 handle),
the RV screen (km/s-scale dRV from inner companions vs ≤ 1.4 km/s orbital
ceiling), and the resolved-triple search to G < 20. The NSS-off ladder rung
measures removed contamination directly, and the asymmetric verdict rule
(§1.5) makes the Newton-side reading contamination-robust while holding any
boost-side reading to the stability tests.

**DR3 dry run (2026-07-16, El-Badry+21 eDR3 catalog, Banik-like cuts,
10,624 pairs): gamma = 1.205 ± 0.035 (canonical), 1.2025 ± 0.0337 (alt).**
Honest reading, frozen: this value lands in the pre-declared
contamination-guard zone (> 1.20) and is **consistent-with-contamination**:
the dry-run sample is LOOSER than Banik's 8,611 (three of his screens are not
implementable from the eDR3-era catalog: the chi2/nu cut beyond the RUWE
substitute, the faint-companion search, and the RV triple screen — each
removes triples, so their absence biases gamma HIGH by construction). The
repo's own banked audits quantify the degeneracy: a Newtonian population
needs f_triple ≈ 0.19–0.20 to absorb the deep-bin excess
(`wb_threshold_audit`), and the deep-bin medians sit ~2–3 sigma above the
calibrated Newtonian MC while the MOND upper bound overshoots them by 6–22
sigma (`wb_deprojection_mc`). **The dry run is a pipeline shakeout — machine
works, real data in, plausible-magnitude output — and is NOT evidence for any
hypothesis, including the framework's.** It is also not evidence against:
1.205 with no triple screens is exactly what either a Newtonian or an MI
population plus known contamination would produce. The DR4 run with cuts
11–13 active is what adjudicates.

### 1.7 Gate and dry-run record (rerun after the freeze edits, 2026-07-16)

`python3 wide_binary_pipeline.py --dry-run` → **exit 0, GATE VERDICT: PASS.**
Synthetic-injection gate (N = 30,000, DR4 noise, no hard-coded passes):
inject 1.00 → recover 0.9850 ± 0.0137 (canonical) / 0.9900 ± 0.0125 (alt);
inject 1.09 → 1.0950 ± 0.0137 / 1.0925 ± 0.0150;
inject 1.33 → 1.3450 ± 0.0212 / 1.3375 ± 0.0212 — all within
max(2 sigma, 0.02). Spread check (8 catalogs @ 1.09): mean 1.0881,
rms 0.0191. Eccentricity bracket: flat-e truth under thermal-e model shifts
gamma by −0.0150 (flagged systematic, §1.5). DR3 dry run: §1.6 numbers,
802 deep pairs (y < 0.3, canonical).

---

## SECTION 2 — s^TX SME boost-dipole template (Door 4B, Front A)

### 2.1 Frozen prediction, direction convention, and current standing

- Prediction (banked, not re-derived): per-body
  s^{Tj} = (a0 / 2|g_orb|) gamma^2 beta_cmb n_hat_j; Saturn channel
  **|s^TX| = 8.68e-10 (canonical a0)**; a0 enters linearly →
  **alt footing 8.68e-10 × (1.13/0.936) = 1.048e-9**.
- **Frozen direction convention:** n_hat = the Planck 2018 CMB dipole apex,
  galactic (l, b) = (264.021°, 48.253°) = equatorial (J2000)
  RA 167.94°, Dec −6.94°. Locked equatorial component ratios
  **s^TY : s^TX : s^TZ = 0.208 : −0.971 : −0.120** (code-asserted against the
  IAU rotation to < 5e-3). The predicted **s^TX is NEGATIVE** (n_X < 0 with a
  positive per-body amplitude). Template sign frozen: alpha > 0 IS the
  framework sign; there is no post-hoc sign freedom.
- **Frozen reading fork:** primary = P (per-body, amplitude ∝ 1/g_orb — the
  ledger's own formula); U (universal single s^TX) always cross-fit. The
  noise-free P-signal-vs-U-template overlap in this channel is alpha_U =
  +0.0047 — the readings are nearly orthogonal; verdicts are quoted per
  reading, never mixed.
- **Current standing (frozen, correct margin):** tightest published bound =
  the COMBINED multi-planet fit s^TX = (−0.2 ± 1.3)e-9 (Hees et al. 2016,
  arXiv:1610.04682 Table 9; Kostelecky–Russell Data Tables v19 Table D50).
  The canonical prediction sits **0.67 sigma INSIDE the bar with the
  predicted negative sign** — margin **1.50x canonical / 1.24x alt**. LIVE:
  neither comfortably safe nor excluded, and the sign agreement is not a
  detection. **The "~9.6x margin" figure is superseded** (it was the
  Saturn-amplitude vs INPOP-only 8.3e-9 looser-bound corner; banked
  correction 2026-06-21) and must not be cited.
- **Interpretation guard (frozen):** any preferred-frame MG host
  (AeST/khronometric-class) induces a comparable s^TX. Every outcome below is
  a preferred-frame/Lorentz-violation verdict, MOND-family-SHARED — **never**
  an MI-vs-MG verdict.

### 2.2 Frozen statistic

GLS amplitude fit of the locked-direction template:
alpha_hat = ⟨T_perp, d⟩ / ⟨T_perp, T_perp⟩, sigma_a = sigma_NP/sqrt(⟨T_perp,T_perp⟩),
where T is the Earth–Saturn range perturbation from numerical integration
(DOP853, rtol 3e-12) of BOTH bodies carrying their per-body s (H15 eq. 3
boost term; Hees, Bailey et al., PRD 92, 064049 (2015)), and T_perp, d are
projected orthogonal to the frozen absorption basis: 6 Saturn ICs + 6 EMB ICs
+ GM_sun + range bias + linear drift (finite-difference partials; the banked
"conservative" level — a real INPOP/DE global refit absorbs more, so all
sensitivities quoted here are upper limits AT THIS ABSORPTION LEVEL, flagged).
Template linearity is gate-verified (two independent scalings, < 1%
required). Normalization: **alpha = 1 ⟺ |s^TX| = 8.68e-10 (canonical)**;
**alpha = 1.207 ⟺ |s^TX| = 1.048e-9 (alt footing)**.

### 2.3 Pre-declared decision bands (mirrored verbatim in the code output)

| outcome | frozen condition |
|---|---|
| DETECT (canonical) | alpha_hat ≥ 3 sigma_a AND \|alpha_hat − 1\| ≤ 2 sigma_a |
| DETECT (alt) | alpha_hat ≥ 3 sigma_a AND \|alpha_hat − 1.207\| ≤ 2 sigma_a |
| KILL (canonical) | \|alpha_hat\| < 2 sigma_a with sigma_a ≤ 0.50, i.e. sigma(s^TX) ≤ 4.34e-10; 3-sigma kill at sigma_a ≤ 0.33 (sigma(s^TX) ≤ 2.89e-10) |
| KILL (alt) | \|alpha_hat\| < 2 sigma_a with sigma_a ≤ 0.604 (sigma(s^TX) ≤ 5.24e-10) |
| WRONG-SIGN KILL | alpha_hat ≤ −3 sigma_a (direction- and sign-locked template) |
| NO VERDICT | any sigma_a too large to exclude either 0 or the prediction — the present standing |

A detection claim additionally requires the U-reading cross-fit to be
reported and the P/U discrimination stated; a canonical-vs-alt footing
discrimination requires the two DETECT windows to be disjoint at the achieved
sigma_a (they overlap for sigma_a > ~0.05 — pre-declared as unlikely to be
separable; the footings differ by 0.207 in alpha).

### 2.4 Honest sensitivity statement (frozen — no sensitivity claims beyond it)

This single Cassini–Saturn direct-range channel (623 normal points,
2004.0–2017.7, Di Ruscio et al. 2020, A&A 640, A7; sigma_NP = 6 m mid value,
3/15 m sensitivity rows, flagged approx) reaches sigma(s^TX) ≈ 1.5e-7 at the
conservative absorption level — **~2 orders short of the prediction**
(detection significance ~0.006 sigma; prediction-vs-bound separation ~0.003
sigma). It cannot alone detect 8.68e-10, nor separate it from a
bound-saturating 1.3e-9. This matches the banked recipe (Saturn sigma_A =
4.5e-8; the strong per-body channel is Mars, sigma_A = 3.44e-9; the published
1.3e-9 bound is the combined multi-planet secular fit). **The frozen
deliverable is the gated fixed-direction template machinery** — locked
direction, locked ratios, locked statistic, locked bands — ready to ingest
DR4-era ephemeris residual series (INPOP/DE refits absorbing Gaia DR4
asteroid/SSO astrometry) via `fit_amplitude()`. The decision, when it comes,
lives in the multi-planet combined fit evaluated against §2.3 exactly as
frozen.

### 2.5 Gate record (rerun after the freeze edits, 2026-07-16)

`python3 stx_dipole_template.py` → **exit 0, GATE VERDICT: PASS** (linearity
7.4e-5 rel. dev.; injection alpha = 1, null, and high-S/N alpha = 2000
recovered within tolerance at sigma_NP = 3/6/15 m over 500 noise
realizations each; empirical/analytic sigma ratios 1.057/0.985/1.002).
Template raw p2p 6.770e-2 m per unit alpha; after conservative absorption RMS
1.390e-3 m per unit alpha (94.3% absorbed). Locked ratios verified against
the Planck-apex rotation to 1.1e-3.

---

## Amendment protocol

Nothing above changes. Post-DR4, the only permitted additions are dated
**POST-HOC AMENDMENT** entries below this line, each stating (a) what the
frozen analysis returned first, (b) what is being added and why, (c) that the
addition is exploratory and carries no pre-registered evidential weight.

*(no amendments)*
