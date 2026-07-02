# RUN_NEXT_DOORS — RESULTS (2026-07-02)

**Doors executed from** `real_research/NEW_DOORS_FROM_LITERATURE_2026-07.md`. Three lanes, each independently adversarially verified (scripts re-run exit 0, all paper numbers value-matched against fetched arXiv source, no invented data, fresh-code recomputes where load-bearing). Framework tested on its **own** terms throughout: modified inertia, ν(y)=√(1+1/y) ⇔ g_obs=√(g_bar²+g_bar·a0), canonical a0 = c²√(Λ/32π) = cH_Λ/Z = **9.36e-11 m/s²**, with the ρ_total/cH0 → **1.13e-10** footing fork run alongside everywhere (rule 4). McGaugh's exponential ν appears only as the *opponent* in Lane B3. Kills at full weight; no manufactured wins, no manufactured deficits.

**Verdict key**: STRIKE (kill fired against framework) / RELIEF (kill fired for) / LEAN (arrow, below kill threshold) / NON-DIAGNOSTIC / DOOR-KILL (the door's own pre-registered collapse condition fired).

---

## LANE C1 — Powered η(β) test on CLASH-VLT (Maraboli+26 / Biviano+26 / Donahue+14)

### What was run
The banked MI-distinctive prediction (DOI 10.5281/zenodo.21104820): kinematic mass-ratio η slides **UP** with radial velocity anisotropy β (2.15 isotropic → ~2.8–3.0 at β~0.3–0.5 as banked; the self-consistent Milgrom-2022-functional kernel gives a shallower 2.15 → ~2.37 — both run), while MG/ΛCDM predict **FLAT**. Confronted, for the first time with per-cluster β *measurements*, against nine CLASH-VLT clusters with published MAMPOSSt anisotropy profiles. Full pipeline: own NFW + r500 solver + gas extrapolation, η per cluster on the framework's ν, injection-calibrated Monte Carlo for the slope statistic, permutation and mass-residualized cross-checks. Supersedes the earlier crude single-point CLASH-VLT look (which leaned flat-to-anti-MI, underpowered, banked honestly).

### Data + provenance
- Biviano+26 Table 2 (nine clusters: r200_kin, rs, symmetrized β intervals) and Table 1 (Umetsu+18 lensing masses) — parsed from fetched arXiv HTML, value-matched row by row.
- Donahue+14 Tables 8–9 (Chandra + XMM X-ray masses).
- Maraboli+26 stack anchors (r200 = 2.13±0.20 Mpc, M200 = 1.51±0.41e15, z=0.315, β-grid endpoints, 250-kpc β feature; A209+AS1063 = 40.1% of 5348 members — derived correctly from the member table).
- Nothing invented; all inputs trace to published tables.

### Numbers
- **η anchor reproduced**: kinematic mean η = **2.39** (canonical a0) / **2.19** (1.13e-10 fork); XMM cross-check 2.42; per-cluster A383 2.65, A209 2.76, M1115 1.78, R2248 2.33; geometric-mean M_kin/M_X = 1.17. **Lands on the banked eRASS1 η(R500)~2.33 with no kinematic-vs-X-ray anomaly** — independent confirmation of the 2.33 standing from a disjoint mass channel.
- **η–β slope**: R1 = +0.084±0.071 — **positive across all three mass-ratio observables**, i.e. the *opposite side* from the MI prediction (negative in mass space; MG/ΛCDM exactly zero).
- **Significance is error-treatment-dependent, honest range 1.2–2.4σ**: injection-calibrated MC z = +1.19/+1.31/+1.80; exact permutation on centrals 1.98σ one-sided vs null, ~2.3σ vs the attenuated MI kernel; naive OLS t = 2.42 (invalid with these x-errors — upper bound only).
- **Robustness kills the strike**: drop M1115 (the one kinematic-only fit, 2.4σ below its own lensing mass) → 1.6σ; control the mass–anisotropy confound (Spearman(β, lnM_kin) = +0.77–0.82; mass-residualized permutation slope) → **0.97σ**. β and mass effects are **not separable at N=9**; the unpublished MAMPOSSt β–mass posterior correlation is an unquantifiable residual systematic (cuts both ways — it would equally absorb a true MI signal).
- **Power calibration**: MI-truth could produce at most 0.61σ (banked kernel) / 0.12σ (computed kernel) of separation at N=9 with published β errors. **3σ requires ~216 / ~6030 clusters** (CHANCES-era) or σ_β≈0.1 per cluster.

### Verdict + kill status
**LEAN, anti-MI side; kill (calibrated anti-MI >2σ) NOT robustly met.** The flat-to-anti-MI lean from the crude first look **persists and hardens somewhat** — it now straddles the 2σ line (1.2–2.4σ) rather than sitting safely below — but collapses to ~1.0–1.6σ under the two mandatory robustness cuts. No strike declared, no relief granted. This is, by its own injection calibration, **not a powered test** at N=9.

**Theory-side flag (bank with DOI 21104820)**: the self-consistent kernel slide is ~3× shallower (2.15→2.37 over β 0→0.4) than the note's banked 2.15→2.8–3.0 and is construction-dependent; the **sign and the 2.15 floor are robust in every variant**. The DOI note should carry the magnitude caveat. Verdict holds under both kernel sizes.

**Script**: `eta_beta_powered_maraboli.py` (scratchpad, verified; commit).

---

## LANE B3 — MIGHTEE-HI resolved-M/L RAR ν-shape head-to-head (arXiv:2504.20857)

### What was run
First head-to-head **shape** test of the framework's own interpolation ν(y)=√(1+1/y) against McGaugh's exponential ν (a0 free for both) on the MIGHTEE-HI resolved RAR — 19 gas-rich galaxies, 80 points, per-galaxy SED-measured M/L (the dataset's distinctive feature: it *measures* Υ instead of fitting it). Then fixed-coefficient placement of 9.36e-11 (+ fork) on the same footing. Data recovered from the paper's vector-PDF figures (the machine-readable table is withheld: `%\input{gbar_gobs_table}` commented out in main.tex, "available on request"), pinned by three independent absolute anchors (tick-mark calibration residual 0.0000 dex; published red/blue fit curves reproduced at their published a0's to rms 0.0000 dex; residual-panel cross-check 0.0005 dex), then passed through a validation gate: the paper's fiducial a0 = 1.69±0.13e-10 and σ_int = 0.045 recovered at **0.03σ**. Verifier ran an independent refit with different machinery (slope-propagated x-errors, y-only likelihood) — concordant on all three load-bearing numbers.

### Data + provenance
- arXiv src.tar.gz (sha256 0a3174fc…), genuine e-print; every quoted paper number verified against main.tex line-by-line (fiducial fit l.646; M/L forks 1.08/1.47/1.32/2.06e-10 ll.718–750; δ=3.94±1.4; DPL β=0.46±0.04; rising a1=4.47±1.88e-10 at 2.4σ l.781; Υ_K=0.36 ≡ Υ_3.6=0.27 ll.741, 903; the "intrinsic to the data used" concession l.919).
- Extracted data: `mightee_rar_extracted.csv` + three M/L-fork CSVs (same 80 points re-derived — robustness variants, **not** independent confirmations; not multiplied).

### Numbers
- **Shape (the door's target)**: framework ν beats McGaugh ν with **Δχ² = −2.5 to −8.6 across all three M/L forks** (ln B ≈ +1.3…+4.3 BIC-approx), the preference concentrated in the transition region — consistent with the paper's own sharper-than-MLS δ = 3.94±1.4 and deep slope β = 0.46 ≈ ½ (the framework's exact deep exponent). Independent-machinery refit: Δ(−2lnL) = −3.2, same sign. 19-block bootstrap: framework wins **200/200**, median Δ = −3.2, 16–84% [−4.8, −1.7].
- **Correlation ceiling (verifier's added caveat)**: 80 points from 19 galaxies share distance/inclination/M/L errors; the paper treats them as independent, so the σ's are on the paper's own footing. Worst-case deflation (×√(80/19)): shape lean drops from ~1.6–2.9σ to **~1.3σ** — sign bootstrap-stable, but the shape claim is a **sign-robust lean, never to be quoted past ~3σ**.
- **Coefficient (adverse on the same footing)**: with the framework's ν, this dataset wants a0 = (1.94±0.13)e-10 — 9.36e-11 excluded at **6.9–7.4σ** (6.1σ under worst-case deflation; 4.1σ on the fixed-Υ fork); 1.13e-10 fork at 5.4–6.0σ. **Context that blocks a strike**: the dataset's normalization is high against *every* local anchor — Milgrom's 1.2e-10 out at 3.2–3.9σ, SPARC's own MLS 1.15±0.02e-10 at ~4σ — swings ×2 under their own documented systematics (1.08 → 2.06e-10), and the paper concedes the MIGHTEE-vs-SPARC discrepancy is "intrinsic to the data used."
- **The genuinely uncomfortable residue**: their resolved SEDs *measure* Υ_K ≈ 0.36 (≡ Υ_3.6 ≈ 0.27), breaking the a0–Υ degeneracy away from 9.36e-11 — the SPARC 0.108-dex anchor (`real_research/rar_framework_a0_mlfit.py`) needs Υ_3.6 ≈ 0.70. A real unfavorable datum on 19 gas-rich dwarfs. Not a kill; logged at full weight.
- **Cassini non-transfer**: the framework's power-law Newtonian tail means the paper's δ≳2–3 Cassini/WBT escape does **not** transfer; banked Cassini-Q2 standing (3–15σ inherited AeST tension) unchanged.
- **Front B side note**: their tentative 2.4σ *rising* a0(z) matches the cH·E(z) fork's sign; ΛCDM-degenerate as banked — no update.

### Verdict + kill status
**Kill (framework ν disfavored >2–3σ on shape) did NOT fire — the arrow points the other way.** First dataset where the framework's own interpolation **wins a shape head-to-head**: a sign-robust LEAN for (1.3–2.9σ depending on correlation treatment), not decisive. **Coefficient: adverse LEAN on a contested normalization** — the 6–7σ number is real on this dataset's own footing but the dataset excludes all anchors simultaneously and swings ×2 under its own systematics; the transferable adverse content is the measured-low-Υ residue, which is the direct target of the next computation (below).

**Scripts**: `mightee_b3/b3_mightee_nushape_test.py`, `mightee_b3/b3_mightee_forks_robustness.py`, `mightee_b3/verify_independent_refit.py` + 4 CSVs (scratchpad, all exit 0; commit all — the verifier's independent refit ships alongside per the self-verifying-repo rule).

---

## LANE A1 — Deffayet–Woodard nonlocal MOND: sign theorem + a0(z) discriminant

### What was run
Two confrontations against the DW nonlocal reconstruction (fetched arXiv source, `synthesis.tex`, quotes verified verbatim): **(1)** does DW evade or break the anti-MOND sign theorem (Scale Without Law, DOI 10.5281/zenodo.21016309: passive ghost-free bath ⇒ δm = 2∫ρ/ω² ≥ 0), and can it serve as the template for the unwritten MI completion? **(2)** what does DW's own Z[g] = (4c⁴/a0²)g^μν∂_μχ∂_νχ (χ = □⁻¹R_uu) predict for a0(z), composed with a static source at leading order: Z_tot = (2g_obs/a0)² − B(z)², where B(z) is their eq. (52) cosmological background (u-substitution re-derived, quadrature cross-checked by trapezoid; their z_c ≃ 0.0880 on Kim+ Planck-2015 recovered at 0.0878). DW's own a0 = cH0/√30 ≃ 1.2e-10 (ratio to framework 1.277); their own deep-MOND definition **0 < Z ≲ 1** (their l.622 — no strawman).

### Numbers + structural findings
- **Prong 1 (sign theorem / horn III)**: DW is **horn-II nonlocal modified gravity**, not modified inertia — matter rides unmodified geodesics (their v²/r = c²Ψ'), lensing enforced to Φ = −Ψ, u_μ = ∂_μφ[g] a metric functional inside the gravity action. The sign theorem has **no object to act on**: DW neither breaks nor evades it. Their MOND sign is a tuned two-coefficient choice (their own "constructed to enforce"); sympy-verified counterfactual: flip the sign and [c²rΨ']² = −a0GM < 0 — no real MOND branch, identical |Z| structure. **The door's pre-registered kill-condition (a) fired: DW collapses as a template for the MI completion. Horn III stays closed.**
- **Prong 2 (a0(z) floor)**: DW's MOND branch sits above g_floor = (a0/2)|B(z)|, vanishing only at **z_c ≈ 0.08–0.10**. Today, across cosmologies (0.3/0.7 | Planck-15 | Planck-18): B(0) = −1.440 | −1.238 | −1.102 (independently recomputed), so |Z_bg(0)| = 1.21–2.07 > 1 — **their entire own deep-MOND band is drowned at z=0**, robust in sign on all three cosmologies, marginal on Planck-18 (1.10×) vs comfortable on their own (1.44×). g_bar floor **3.6–6.2e-11**; **1.6–1.8 dex** of the in-hand SPARC deep RAR sits below the floor in a corner their f does not suppress (exp(−√|Z|/3) ≈ 0.62). Severe tension **pending their own deferred transition numerics** ("formidable numerical undertaking") — not a completed kill of DW.
- **Corrections applied per verification (both banked here)**: rising-fork comparison at z = 0.33 is **+19%** (not +14%; E(0.33) = 1.186); floor figures carried as the cosmology **band**, not the paper-cosmology endpoint.
- **Front B / MUSE**: DW's floor exceeds the fitted a0 everywhere at MUSE redshifts (1.3× at z=0.33, 3× at z=1) — DW hides behind the same ΛCDM-assembly degeneracy that already made MUSE non-diagnostic. **Front B loses nothing.**
- **New discriminant gained**: DW predicts a **MOND-quality cusp at z ≈ 0.09 ± 0.02** — *more* MOND at z≈0.09 than at z=0, deep band fully off outside 0.03 < z < 0.17. No other model on the table predicts this. The framework predicts **flat** (declining-√ρ_DE canonical footing) over this range. SPARC / WALLABY-DR2 / MIGHTEE data straddle z≈0.09 **today**.

### Verdict + kill status
**DOOR-KILL (pre-registered, against DW-as-template), plus a genuinely new in-hand discriminant.** The anti-MOND sign theorem's standing is *reinforced* (the one published nonlocal-MOND construction turns out not to touch it, and its MOND sign is put in by hand); the covariant-MI trichotomy closure holds. DW itself takes on an uncompleted-but-severe deep-RAR tension. No σ overclaims anywhere in this lane.

**Scripts**: `a1_dw_sign_theorem.py`, `a1_dw_a0z_discriminant.py` + `dw_paper/synthesis.tex` (scratchpad, exit 0; commit).

---

## COMBINED BOTTOM LINE

### Moved the ledger — FOR
- **B3 shape**: first head-to-head where ν=√(1+1/y) **beats** McGaugh's exponential on real data (Δχ² −2.5…−8.6, bootstrap 200/200, transition-region concentrated, deep slope β≈½ matched). Ceiling: sign-robust lean, ~1.3–2.9σ. The kill aimed at the framework's interpolation fired *in reverse*.
- **A1 structure**: horn-III closure and the anti-MOND sign theorem come out *stronger* — DW is not a counterexample, not a template, and its MOND sign is tuned. Plus a free gift: the z≈0.09 DW cusp vs the framework's flat a0(z), testable with data in hand.
- **C1 anchor**: kinematic η = 2.39/2.19 independently confirms the banked eRASS1 η(R500)~2.33 from a disjoint (dynamics, not X-ray) channel.

### Moved the ledger — AGAINST
- **B3 Υ residue**: SED-*measured* Υ_K≈0.36 (Υ_3.6≈0.27) on 19 gas-rich dwarfs breaks the a0–Υ degeneracy away from 9.36e-11 (the SPARC 0.108-dex anchor sits at Υ_3.6≈0.70). The 6–7σ coefficient exclusion itself is quarantined (dataset excludes ALL anchors incl. Milgrom at 3.2–3.9σ and SPARC's own MLS at ~4σ; ×2 systematic swing; paper's own concession) — the *transferable* adverse content is the Υ measurement, logged at full weight.
- **C1 lean**: the anti-MI η–β lean hardened from "flat-to-anti" to "straddling 2σ" (1.2–2.4σ) but is **not a strike** — 1.6σ without the lensing-discrepant M1115, ~1.0σ mass-controlled, inseparable from the mass trend at N=9, and injection calibration proves the test underpowered by an order of magnitude (~216–6000 clusters for 3σ). Status: adverse lean, banked, unresolved.

### Non-diagnostic
- MIGHTEE's 2.4σ rising a0(z): matches the cH·E(z) fork's sign, ΛCDM-degenerate — Front B standing unchanged.
- MUSE vs DW: DW joins the degeneracy pile; no model separates there.
- The B3 M/L forks: robustness variants of the same 80 points, correctly not stacked.

### Housekeeping (before/at commit)
- DOI 21104820 gains the kernel-magnitude caveat: self-consistent slide 2.15→~2.37 (not 2.8–3.0) over β 0→0.4, construction-dependent; **sign and 2.15 floor robust in all variants**.
- Copy the six lane scripts + 4 CSVs + `synthesis.tex` from the scratchpad into the repo (suggest `opus_48_extended_research/reviews/next_doors_2026_07/`) so the ledger stays self-verifying.

### The single next computation
**SED-prior joint a0–Υ refit of the SPARC RAR on the framework's own ν** — extend `real_research/rar_framework_a0_mlfit.py` to fit (a0, Υ_3.6) jointly with the MIGHTEE-measured Υ_3.6 ≈ 0.27–0.36 as a prior (and as a hard fix, both ways; both footing forks; reg-MOND comparator alongside). This is the one computation that determines whether B3's only transferable adverse datum — measured-low Υ — actually moves the in-hand 0.108-dex/Υ=0.70 anchor against 9.36e-11, or whether SPARC's (earlier-type, higher-mass) sample legitimately carries a higher Υ and the residue stays quarantined to gas-rich dwarfs. Pre-registered both-ways: if the SPARC anchor collapses under a realistic Υ prior, the coefficient miss is real and the working-rule anchor must be amended; if it holds, B3's residue is a population-Υ effect and the coefficient standing is unchanged. (Cheap parallel check, second priority: bin the in-hand SPARC+MIGHTEE RAR by z across 0.03–0.17 to confront DW's z≈0.09 cusp against the framework's flat prediction — a kill-DW-or-not test, no framework risk.)

---
*All lane numbers adversarially verified 2026-07-02 (scripts re-run exit 0; paper values matched against fetched sources; fresh-code recomputes on load-bearing pipelines; A1's two numeric corrections and B3's correlation caveat and C1's significance-range amendment are incorporated above at full weight).*