Written: `/Users/carlzimmerman/new_physics/zimmerman-formula/real_research/INHAND_CALCS_RESULTS_2026-07.md`

Full contents (commit-ready, verbatim):

# IN-HAND CALCULATIONS — RESULTS & VERDICTS (2026-07)

**Scope.** Six computation lanes run on in-hand data, each independently adversarially verified (re-run + independent re-implementation + source-provenance checks; every script exit 0). Framework judged on its OWN terms throughout: de Sitter–Unruh **modified inertia**, a0 = c²√(Λ/32π) = cH_Λ/Z = **9.36e-11 m/s²**, Z = √(32π/3), own interpolation ν(y) = √(1+1/y) ⇒ g_obs = √(g_bar² + g_bar·a0). McGaugh's ν used only as a named comparator. Footing fork a0 = 1.13e-10 (ρ_total/cH0) run alongside everywhere (rule 4). Both-ways discipline: every "fails" verified as hard as every "works"; nothing manufactured in either direction. Kills reported at full weight.

**Verification status.** All six lane results below are FINAL: each survived an adversarial verification pass with independent code paths. Three lanes took substantive corrections during verification (L1 likelihood Jacobian, L5 control-handling fork, L6 suppression-bound estimator); the corrected numbers are the headlines below, with the lane-original values kept as labeled forks.

---

## LANE L1 — Hierarchical SPARC arbiter (D, i nuisances; the coefficient question)

**What ran.** Full hierarchical maximum-likelihood fit of a0 on SPARC with per-galaxy distance and inclination marginalization (the missing nuisances that inflated the banked joint-refit Δχ²), on the framework's own ν; published-config anchor (McGaugh ν, Υ=0.5, D0/i0 fixed) independently reproduces a0 = 1.200e-10 vs McGaugh/Li's published 1.2e-10 — provenance and likelihood direction sound. **Substantive correction found in verification:** the lane's inclination-norm term omitted the data-transformation Jacobian (spurious −2N·ln t bonus pulling a0_hat low); the corrected Li-faithful data-space likelihood is the headline, the lane's form kept as a labeled fork. Corrected mock gate unbiased at −0.05%.

**Data.** 175 SPARC rotmod curves (`real_research/data/sparc_data/*_rotmod.dat`) + master table with per-galaxy D, e_D, i, e_i, L36 (`real_research/data/SPARC_Lelli2016c.mrt`); samples 175/171 full, 37 gas-dominated, 94 star-dominated (counts verified exact).

**Numbers** (framework ν unless noted; lane norm / corrected data-space):

| Config | a0_hat | Δχ²(9.36e-11) | Δχ²(1.13e-10 fork) |
|---|---|---|---|
| Full sample | 1.239e-10 / **1.372e-10** | 161 / **270** | 18.4 / **64** |
| Leave-out-top-2 | — | 88 / **168** | 1.0 / **16.8** |
| Bootstrap P(≤9.36e-11) / P(≤fork) | — | 0.000 / 0.000 | 0.122 / **0.016** (~2.1σ) |
| Gas-dominated (Υ-free) | 8.665e-11 / **9.816e-11** | 1.5 / **0.7** (boot P(≤fw)=0.39) | 22.3 / **5.9** |
| McGaugh-ν comparator, full | 9.966e-11 / 1.100e-10 | 10.4 / 48 (boot P=0.034) | — |

Committed `real_research/rar_framework_a0_mlfit.py` re-run direct: 0.108 dex @ Υ=0.70 vs reg-MOND 0.122 — exact, unchanged (working-rule #2 satisfied).

**Verdict + kill status.** Three convention-robust conclusions:
1. **AGAINST (new, banked at full weight):** the full-SPARC hierarchical fit on the framework's own ν puts the optimum at **1.24–1.37e-10** and **excludes the canonical 9.36e-11 at >3σ-equivalent on every honest reading** (naive 161–270; bootstrap P<0.002; leave-out-top-2 keeps 88–168; SPS zero-point cannot rescue). This is a REAL full-sample coefficient tension on this model class. Standing caveats: Υ_bul locked at 1.4Υ_d while the top influencers (UGC06787, IC4202, NGC7814) are bulge-heavy — independent-Υ_bul is the one unrun knob; σ_int form is a lever; the ~1.8x gas/star split (corrected ~9.8e-11 vs ~1.5e-10) survives on either convention and either ν, so no single a0 resolves SPARC and the coefficient question stays entangled with population/M-L systematics. Never quote "~12.7σ" without the bootstrap ~3.3σ alongside (correlated points).
2. **FOR (supersedes a banked deficit):** the cleanest Υ-free evidence — the gas-dominated cut with full D,i marginalization — is **framework-COMPATIBLE-to-CENTERED on both conventions**: Δχ²(9.36e-11) ≤ 1.5, corrected optimum 9.82e-11 essentially AT the canonical value. The banked gas-dom "7.7e-11 low preference" is **retracted as a norm-term artifact and SUPERSEDED**. Gas-dom is also mildly anti-fork (Δχ² 5.9–22.3, convention spread).
3. **Fork status:** 1.13e-10 not excluded at the pre-registered >3σ honest bar, but under the corrected likelihood it is mildly disfavored (~2.1σ bootstrap; leave-out-top-2 Δχ² = 16.8). "Fork sits at the joint optimum" no longer holds unconditionally.

No pre-registered kill triggered; the full-sample exclusion banks as the strongest in-hand coefficient tension, with the Υ_bul knob explicitly open.

**Scripts (scratchpad, exit 0):** `lane_L1_hierarchical_sparc_arbiter.py` (commit WITH the norm-fork caveat), `VERIFY_L1_independent.py`, `VERIFY_L1_inclination_norm_fork.py`, `L1_rerun_verify.txt`.

---

## LANE L2 — Cluster gravitational redshift discriminator

**What ran.** Predicted stacked BCG–member gravitational redshift Δ for 2–4×10¹⁴ M☉ clusters under (1) GR+DM/dynamically-calibrated potentials, (2) the framework's canonical AeST/ghost-condensate (extra-matter) reading, (3) pure-MI photons-on-baryon-only-GR-metric, (4) MG-MOND-from-baryons on the framework's ν (both a0 footings); compared to the three stacked detections. Independently re-derived with analytic NFW/Hernquist potentials to <1%.

**Data.** Wojtak+2011 (Nature) −7.7±3.0 km/s; Sadeh+2015 −11 +7/−5; Rosselli+2023 (arXiv:2206.05313, 3058 SDSS clusters z<0.5) −11.4±3.3 — all provenance-confirmed.

**Numbers.** GR+DM prediction −8.1 to −12.4 km/s (matches data). Pure-MI baryon-only −1.6 to −2.2 km/s = 18–20% of signal (nearly mass-independent, 0.177→0.196 over 2x mass) → disfavored **2.9σ (Rosselli), 1.9σ (Wojtak; ~2.5–2.7σ after Kaiser transverse-Doppler correction), 1.3σ (Sadeh)**, same direction; no formal combination claimed (SDSS overlap; naive √Σσ²=3.7σ noted, refused). MG-MOND(framework ν) underpredicts ~2x, 1.6–1.8σ vs Rosselli; fork spread ≤9% between footings → a0-non-diagnostic. All modeling choices audited as conservative for the exclusion (f_b×NFW, BCG Hernquist spike, cosmic-f_b bracket).

**Verdict + kill status.** **NON-DIAGNOSTIC for the framework proper — consistency pass at zero discriminating cost, NOT a win** (the condensate amount is banked-FREE; do not upgrade to support). The signal **forces the extra-matter reading the framework's canonical stance already takes**: both historical MOND escapes (the "Wojtak killed TeVeS" folklore tested a log-diverging profile with too MUCH blueshift; the Bekenstein–Sanders isothermal rescue works only by calibrating to observed kinematics, implicitly conceding the ~2x residual — an inference from their construction, not their words) collapse into that reading. The no-extra-matter pure-MI corner takes a lensing-independent, photon-side ~3σ (best-single) squeeze — this excludes that *specific assumed photon sector*, not MI per se (MI has no written photon sector; it squeezes the unwritten completion), one next-gen stacking survey from a formal kill. No kill triggered.

**Scripts:** `l2_cluster_gravz_discriminator.py` (lane), `l2_VERIFY_independent.py` (analytic re-derivation) — commit both.

---

## LANE L3 — Cluster η(R500) non-thermal-pressure envelope

**What ran.** The banked eRASS1 η(R500) recomputed under the 2026 Lebeau+ (arXiv:2607.00610) non-thermal-pressure correction schemes, full generosity envelope (Popesso gas credit, cosmic-baryon credit, both a0 footings). Independent code path reproduced every headline cell to 6 digits; sign direction ("NT correction *increases* the mass") verified verbatim from the paper; FITS unit conversions verified from the header. One trivial correction: scheme B is "~+5% at R500" (paper's words), not +6% → η = 2.45 not 2.47.

**Data.** eRASS1 primary cluster catalog, N=9830, z_med=0.298 (`real_research/data/erass1cl_primary_v3.2.fits`); Lebeau+ 2026 correction factors (one Virgo replica in one constrained simulation, applied as uniform R500 multipliers — the honest precision limit of the source, labeled).

**Numbers.** η(R500) baseline (no NT) = **2.33**; scheme A (+20% at R500, verbatim-verified) → **2.80**; scheme B (~+5%, corrected) → **2.45**; XRISM-sightline-calibrated A (+10%) → **2.57**; cosmic-baryon credit → 1.69; maximal-generosity floor (fork + full credit + no NT) = **1.55**. Median g_bar/a0 ≈ 0.04 at R500 → deep regime → this front IS diagnostic of the a0 value (fork scales η by √(a0_c/a0_f) ≈ 0.91), and neither footing rescues. Headline stays 2.33 (not 2.80) because eRASS1 masses are WL-calibrated, so full-strength HSE-NT correction borders on double-counting — the lane correctly resisted manufacturing the worse number.

**Verdict + kill status.** **AGAINST, full weight, unchanged-to-worsened.** η(R500) = 2.33 [envelope 1.55–2.80] on the framework's own terms; the 2026 NT systematics move the deficit the WRONG way (thermal HSE *under*estimates dynamical mass). No cell approaches η = 1 even stacking every generosity simultaneously. **The cluster central deficit remains the framework's cleanest standing quantitative failure** — shared with MOND generally, not uniquely fatal; the MI-distinctive relational σ-spread discriminator is unaffected by this lane. Not a formal kill (shared-MOND wall, extra-matter reading absorbs it as with L2), but the deficit is now robust to the NT escape hatch.

**Script:** `eta_nt_budget_2026.py` (exit 0; apply the one-line scheme-B fix 1.06→1.05 before commit).

---

## LANE L4 — Khronon-Tensor Q2 lineage (Cassini quadrupole wall)

**What ran.** Tested whether the Blanchet–Skordis Khronon-Tensor theory (the newest MG-MOND lineage, "same PPN as GR") evades the Cassini Q2 quadrupole that AeST inherits. Derived KT's quasistatic stationary limit (verbatim BM-AQUAL in the total field + a μ²φ term negligible by ~15–17 orders at the Q2-sourcing radii — corrected from "≥19"), showed the framework's own ν is an admissible KT free function (its induced J(Y) reproduces JCAP Eq. 3.23 exactly, 2c²/3a0 coefficient verified in source), and computed the zero-shape-freedom point prediction via the DHF q(ẽ) machinery (calibration vs DHF's published q values passes at 0.0–0.8%; independent Newton-solver re-implementation agrees to 0.03%).

**Data/sources.** KT letter + JCAP paper (equation-level claims verified verbatim); Desmond–Hees–Famaey 2024 (arXiv:2401.04796, MNRAS 530.1781); Park+ 2026 (arXiv:2602.17884): Q2 = (1.6±1.8)e-27 s⁻², "3–15σ" band confirmed from abstract; Hees+ 2014; Gaia g_ext = 2.32±0.16e-10.

**Numbers.** Framework point prediction **Q2 = 2.33e-26 s⁻² → 12.1σ vs Park+ 2026, 6.8σ vs Hees+ 2014**; fork 1.13e-10 → 2.67e-26 → **13.9σ (worse)**. McGaugh-RAR-ν comparator 3.65e-26 (11.2σ vs Hees, inside DHF's own 10.9–14.3σ range; note Park's "~2.9e-26 required boost" is posterior-marginalized, not this point value). Exact-AQUAL correction bounded UPWARD by DHF footnote 6 → conservative. All in-KT escapes close on the sources' own equations: sharp-shutoff Eq. 4a (Q2 probes the IF at e_N≈2.03, exactly where the RAR pins it — DHF Fig. 1 caption verbatim), K(Q)/μ² (~15–17 orders margin; >20 at Saturn), stationarity (0.31%), α-stabilization (α₁=−8α confirmed), Λ-drift (8e4x margin). Both-ways: the framework's milder transition genuinely buys ~35% vs McGaugh's ν and the canonical footing is the favorable one — it still misses by more than an order of magnitude.

**Verdict + kill status.** **AGAINST any MG realization — the Cassini Q2 wall extends to the entire Blanchet–Skordis lineage, banked at full weight.** The "MG-realization escape" narrows to nothing within this lineage: the framework inheriting KT's Solar-System sector is a 12σ point exclusion with zero shape freedom. MI-evasion still requires the unwritten covariant MI completion (banked position, unchanged — and the covariant-MI trichotomy is banked CLOSED, so this wall now presses directly on the framework's only remaining realization route). Sign convention: DHF Eq. (10) carries a minus; magnitude convention declared, matching DHF's own tension-quoting practice. This is a kill of the KT/AeST-realization escape hatch, not of MI itself.

**Scripts:** `l4/kt_q2_lineage.py` (apply corrections 1–3, commit as `reviews/kt_khronon_q2_lineage.py`), `l4/verify_q_independent.py` (commit as `reviews/kt_khronon_q2_lineage_xcheck.py`).

---

## LANE L5 — Out-of-sample dwarf RAR (WALLABY / LITTLE THINGS)

**What ran.** Attempted the WALLABY out-of-sample RAR: **confirmed NOT DOABLE from the in-hand corpus** (all 203 entries carry ring kinematics only — no HI mass or photometry key exists, g_bar not constructible; a data-content block, not a framework failure; door open pending external W1/HI cross-match). The honestly-doable substitute: 18 genuinely out-of-SPARC LITTLE THINGS dwarfs (18/8 split audited against all 175 rotmod files including aliases — no misclassification), one deep-regime (y ≲ 0.3) outer-ring point each, a0 inverted via the framework's own ν (a0_impl = (g_obs²−g_bar²)/g_bar, the exact algebraic inversion), with an 8-galaxy SPARC-overlap calibration control.

**Data.** Corpus `corpus_v7.json`; LITTLE THINGS Oh+2015 tables (VizieR J/AJ/149/180; column mapping self-validated); SPARC rotmods for the control.

**Numbers.** Naive OOS fit: a0 ≈ 2.2e-10, apparently 4.4σ above canonical — **collapses under its own controls**: fitted per-galaxy scatter 0.67–0.87 dex; the identical estimator reads **+0.37±0.09 dex HIGH** on the 8 known-decomposition overlap galaxies (re-derived from raw inputs: median +0.373, rms 0.240, N=7; direction confirmed); DDO_101's distance controversy alone is −0.56 dex (matches analytic 1/D² to 3 decimals). Calibration-corrected: **a0(OOS) ≈ 0.9–1.2e-10 ± ~0.29 dex** — the span reflects one control's handling (DDO_50 dropped vs re-included: 9.4e-11 ↔ 1.2e-10); **both forks pass under both handlings at <0.5σ**. The formal both-fork >3σ kill was never met even naively (fork fails >3σ in the Oh-(R,V) source variant).

**Verdict + kill status.** **UNDERPOWERED-CONSISTENT — a null both ways; pre-registered kill NOT triggered; NON-DIAGNOSTIC.** With 18 points and ~0.9 dex MAD this test cannot discriminate anything in ~5e-11–4e-10 at 3σ. The corrected central value is a calibration artifact, not a measurement of the third decimal. Coherent with the L1 gas-dom window. State the DDO_50 fork explicitly wherever quoted.

**Scripts:** `L5_corpus_oos_rar_FINAL.py` (amend bottom-line text to state the 0.9–1.2e-10 DDO_50 fork before commit), `L5_wallaby_corpus_outofsample_rar.py`, `L5_control_overlap_calibration.py`, inputs `corpus_v7.json`, `lt_table1.dat`, `lt_table2.dat`, `lt_rotdmbar.dat`.

---

## LANE L6 — Deffayet–Woodard z≈0.09 cusp kill-test

**What ran.** Confronted DW-naive (the Deffayet–Woodard arXiv:2512.10513 nonlocal reconstruction with its MOND branch, Z>0, simply ABSENT below the cosmological floor g_floor(z) = (a0_DW/2)|B(z)|, nothing replacing its phenomenology) with in-hand SPARC deep-MOND data. B(z) integrand re-derived by hand from DW's own tex (u-substitution, 6√30 prefactor); sign confirmed twice — numerically and in DW's own prose (floor bites hardest at z→0, exactly where SPARC lives); z_c = 0.0878 vs their published 0.0880; a0_DW = cH0/√30 = 1.1956e-10 derived from their ρ₀. Independent re-implementation with separate load code reproduces census, σ, and MIGHTEE numbers.

**Data.** SPARC deep-MOND census (966 points, 954 below floor); DW tex source in hand; MIGHTEE extracted RAR (`opus_48_extended_research/reviews/next_doors_2026_07/mightee_rar_extracted.csv`, z ≲ 0.08) as the both-ways check.

**Numbers.** **98.8% of 966 deep points sit below DW's floor** yet trace DW's own on-branch MOND locus at −0.08 dex mean, 0.22 dex scatter. Off-branch offset **+0.594±0.022 dex → ~26.5σ** exclusion of the dead Newtonian branch (26.1–31.6σ across Υ/a0 forks; conservative per-galaxy counting; DW-most-charitable cosmology). Nonparametric backstop: 101/105 galaxies above the dead branch, binomial **p = 2.4e-25** — not a Gaussianity artifact. Maximal DW-style suppression allowed: **~16–28% depending on estimator** (mean-based s ≥ 0.84 vs robust median s ≥ 0.72 at 95%; 0% on the Υ=0.50 fork); s=0 is ≥13σ away on every variant. SPARC deep a0_eff flat in z at 1.7σ with an insignificant DECLINE toward z_c — opposite to DW's required rise. Framework's own flat prediction (a0=9.36e-11, own ν, footing forks <1% here) **passes as-is; zero framework risk in this lane**. Both-ways flag preserved: MIGHTEE's +0.28 dex deep offset (deep median 1.71e-10) is the one rise-like datum, but it is the banked B3 cross-survey Υ systematic, has no per-point z, and cannot undo a branch-existence violation at z<0.03. Phrasing caution: "entire deep band off-branch" holds strictly at z=0; on P18 the floor dips below a0_DW/2 for z ≳ 0.007 (immaterial — census is per-point at each galaxy's own z).

**Verdict + kill status.** **FOR the framework (rival eliminated in its published form): DW-naive excluded at ~26σ.** NOT a completed kill of DW: their unpublished M-transport memory sector ("formidable numerical undertaking," verbatim) could in principle replace the branch — but survival requires reproducing the on-branch MOND locus to 0.22 dex over 1.5+ dex of g_bar at every z in 0.0002–0.03 with the branch off and no free parameter. Upgrades banked A1 from "severe tension pending numerics" to a quantified 26σ / ≤16–28%-suppression bound.

**Scripts:** `l6_dw_cusp_kill.py` (lane, re-run byte-identical), `l6_verify_spotcheck.py` — commit both.

---

# COMBINED BOTTOM LINE

## What MOVED — against the framework
1. **L1 full-sample coefficient tension (NEW, the biggest mover).** On the framework's own ν with D,i properly marginalized, the full-SPARC optimum is 1.24–1.37e-10 and canonical 9.36e-11 is excluded >3σ-equivalent on every honest reading — and the verification CORRECTION (Jacobian) *strengthened* it (161→270). This supersedes "naive Δχ² inflated by missing D,i nuisances" as a hope: the nuisances are now in, and the tension survives them. Caveats that keep it short of a kill: Υ_bul locked (top influencers bulge-heavy), σ_int lever, and the convention-robust ~1.8x gas/star split meaning no single a0 fits SPARC on ANY ν — the tension is entangled with population-level M-L systematics by construction.
2. **L4 Q2 lineage closure.** The MG-realization escape is now shut across the entire Blanchet–Skordis family (AeST banked 3–15σ; KT now a 12.1σ zero-freedom point exclusion on the framework's own ν, fork worse at 13.9σ). Combined with the banked covariant-MI trichotomy closure, the framework has NO written realization that clears the Solar System: the unwritten MI completion now carries the whole load on this front.
3. **L3 η(R500) worsened directionally.** 2.33 [1.55–2.80]; the 2026 NT systematics close the last conventional escape hatch and move the deficit the wrong way; the front IS a0-diagnostic (deep regime) and neither footing rescues. Cleanest standing quantitative failure, shared-MOND.

## What MOVED — for the framework
1. **L1 gas-dominated cut RESOLVED IN THE FRAMEWORK'S FAVOR.** The cleanest Υ-free evidence, properly marginalized, is centered essentially AT 9.36e-11 (corrected optimum 9.82e-11, Δχ² ≤ 1.5 both conventions). The banked 7.7e-11 low-preference is retracted (norm-term artifact) and superseded. This is the single most convention-robust, M-L-free statement SPARC can make about the coefficient, and it lands on the canonical value.
2. **L6 rival eliminated.** DW-naive dead at 26σ; the framework's flat a0(z) passes the same census untouched. The nonlocal-reconstruction lane of competitors is now quantitatively behind the framework on in-hand data.
3. **L2 squeeze on the no-extra-matter corner confirms the canonical stance.** Cluster grav-z independently forces the extra-matter reading the framework's ghost-condensate position already takes — the framework paid this cost years ago; rivals that didn't now owe ~3σ.

## Non-diagnostic (do not let these drift into either column)
- **L2 grav-z framework-vs-ΛCDM:** consistency pass at zero discriminating cost (condensate amount banked-FREE).
- **L5 OOS dwarfs:** null both ways, kill not triggered, cannot discriminate 5e-11–4e-10.
- **RAR point-fit (working-rule #2):** unchanged — 0.108 vs 0.122 dex; the SPARC RAR *scatter* remains convention-compatible and non-diagnostic of the coefficient. L1's hierarchical result is a DIFFERENT statement (population-level optimum) and does not overwrite this.
- **Fork 1.13e-10 running tally:** mildly disfavored L1 (~2.1σ corrected, leave-out Δχ²=17), worse at L4 (13.9σ), lowers-but-nowhere-near-rescues L3 (floor 1.55), passes L5, <1% effect L6, ≤9% L2. Net: the fork is now mildly behind canonical on in-hand data; keep running both (rule 4), but "fork at the joint optimum" is retired.

## The single next computation
**Re-run the L1 hierarchical arbiter with Υ_bul freed from the 1.4Υ_d lock (independent per-galaxy or population Υ_bul prior), corrected data-space likelihood, both ν's, both footings.** It is the one explicitly unrun knob standing between the new full-sample >3σ coefficient exclusion and a banked hard result: the three top-influence galaxies (UGC06787, IC4202, NGC7814) are all bulge-heavy, so this single systematic could plausibly move the full-sample optimum toward the gas-dom value — or, if it doesn't, the exclusion hardens to referee-proof. Either outcome is decisive for the coefficient question; nothing else in-hand has that property. (Second in line, not concurrent: the WALLABY W1/HI cross-match to unblock the real out-of-sample RAR.)

## Scoreboard / memory updates required
1. **[project-coefficient-footing] + [Fable a0-footing audit]:** BANK the L1 full-sample hierarchical exclusion (optimum 1.24–1.37e-10, canonical >3σ-equiv excluded on this model class, Jacobian-corrected, Υ_bul knob open). SUPERSEDE the banked gas-dom 7.7e-11 low preference → gas-dom is framework-compatible-to-centered (9.8e-11, Δχ²≤1.5). RETIRE "fork 1.13e-10 sits at the joint optimum" → mildly disfavored (~2.1σ) on the corrected likelihood.
2. **[working rule #2] amendment:** the RAR-scatter statement stands verbatim, but append: the hierarchical D,i-marginalized full-sample fit (2026-07, L1) is a genuine >3σ coefficient tension NOT dissolved by the nuisances — quote it alongside, never instead of, the scatter result; gas-dom cut is centered on canonical.
3. **[project-cluster-standing]:** update η(R500) to 2.33 [envelope 1.55–2.80]; NT-motion escape CLOSED wrong-way (Lebeau+ 2026 verified); front is a0-diagnostic, neither footing rescues; relational σ-spread discriminator unaffected.
4. **[project-honest-lcdm-stress / Cassini]:** extend the Q2 inheritance from AeST to the ENTIRE Blanchet–Skordis lineage incl. Khronon-Tensor: 12.1σ (Park+26) zero-freedom point prediction on the framework's own ν, fork worse; all in-KT escapes closed on the sources' own equations; MI-evasion = the unwritten completion, now load-bearing alone.
5. **[project a0(z) / A1]:** upgrade DW standing to "DW-naive excluded ~26σ; ≤16–28% max suppression; only escape is the unwritten M-transport sector under a 0.22-dex straitjacket." MIGHTEE +0.28 dex stays flagged as B3 Υ systematic, not a rise detection.
6. **[grav-z, new]:** bank L2 as non-diagnostic-consistency for the framework + ~3σ (best-single, conservative) photon-side squeeze on the no-extra-matter pure-MI corner; TeVeS-folklore corrective noted.
7. **[L5]:** bank LITTLE THINGS OOS as underpowered-null (0.9–1.2e-10 ± 0.3 dex, both forks pass, DDO_50 handling fork stated); WALLABY RAR blocked on data content, door open.

## Kills ledger (full weight, this cycle)
- **Triggered:** DW-naive branch-existence (26σ, L6 — rival, not framework). KT/AeST MG-realization Solar-System escape (12σ, L4 — closes a framework realization route, not MI itself).
- **Not triggered:** L1 pre-registered fork kill (>3σ both forks) — canonical excluded full-sample but gas-dom compatible; L5 both-fork kill — never met; L2 pure-MI photon-corner — ~3σ best-single, one survey short; L3 — shared-MOND wall, no formal kill bar defined.
- **Nothing manufactured either way** — three lane corrections in verification went 2-against/1-for the original lane verdicts (L1 correction strengthened the exclusion AND rescued gas-dom; L5 correction widened the pass window; L6 correction widened the suppression bound), which is what an honest process looks like.

---

*All load-bearing numbers trace to exit-0 scripts listed per lane (scratchpad, commit-ready). Committed anchors re-verified this cycle: `real_research/rar_framework_a0_mlfit.py` (0.108/0.122 exact), eRASS1 FITS provenance, SPARC master-table provenance, and all external-source quotes fetched verbatim.*