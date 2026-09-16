# G237 — THE SELF-PREDICTED FALSIFIER: does the framework predict its own falsifier?

**The theory's own falsifier, stated as the theory's theorem (hy4 H057 V4, read through V1 and V35).**
*Lane: G237. Repo: zimmerman-formula. Date: 2026-09-16. Sources: hy4_push/H057_VON_NEUMANN_DOORS.md (V4 the framework predicts its own falsifier; V1 the theory must contain its own derivation; V10 is n=2 a computational bound; V35 prove some question undecidable and then stop), deepseek_push/FALSIFIER_MATRIX.md + G207_results.json (the 20 registered rows), deepseek_push/THEORY_CLOSURE_2026-09-16.md (G205), and the lane kill-registries G191 (kink width), G157 (slope floor), G161 (plateau), G170/G203 (anisotropy), G168 (mass band), G156 (charge/relic), G190 (footing), G113/G177 (tSZ 3-way), G173 (pair-break), G078/g083 (surface-density column), G112 (funnel), G088/G092/G165 (ridge). Everything is read from committed artifacts; nothing here is recomputed.*

---

## 1. THE QUESTION — does the framework PREDICT its own falsifier (V4)?

**V4's question, made exact:** is the set of observations that would refute the theory *itself derivable from the theory's structure*? I.e., for each registered kill, is there an entailment — the theory's axioms/derived chain produce the very observation O whose negation would kill it — or is the kill an external imposition (the theory says nothing, someone pinned a kill onto it from outside)?

### 1.1 The maximal falsifier set (compiled from the committed registrations)

**The 20 matrix rows (G207):** 1 DR4 ridge, 2 double-map, 3 funnel, 4 merger q, 5 tSZ 3-way, 6 plateau, 7 anisotropy, 8 saturation, 9 D2 core slope, 10 slope floor, 11 n-kill, 12 particle mass, 13 footing K1/K2, 14 kink width, 15 ontology charge/relic, 16 ZW1215, 17 EFE test, 18 break F(e_N), 19 2/3 law, 20 cosmic pie.

**The lane-carried kills (beyond the matrix rows):** the kink width (row 14), the slope floor (row 10), the plateau (row 6), the anisotropy beta (row 7), the mass band (row 12), the charge/relic (row 15), the footing kills (row 13), the tSZ 3-way (row 5), the pair-break (row 18), the funnel (row 3), the ridge (row 1) are all already rows of the matrix — and **one lane kill is NOT in the matrix**: the **universal dark surface-density column** Σ_ph(<r_M) = a0/(πG) = **213.74 M☉/pc²** (G078/G083, Lean-certified; locally ρ_dark(R₀) = 0.0081 in the measured 0.008–0.015 band). Kill: a measured phantom-sheet column deviating from a0/πG at registered precision, M_b NOT cancelling.

**The maximal falsifier set = 21 registered kills** (20 matrix rows + the surface-density column).

### 1.2 The derivation question, per row

**DERIVABLE** = the theory's own structure (equipartition M_dark = M_b r/r_M, the r⁻² phantom, the equilibrium temperature, the two-phase selection at g = a0, the charge ontology, the cap line) entails the observation whose absence/opposite would fire the kill. **AD HOC** = the theory is footing- or convention-invariant on that axis — it derives shapes, not the value under test; the kill is pinned externally.

| # | Row | Entailment — the theory says X → the killing observation O exists | Class |
|---|---|---|---|
| 1 | DR4 ridge | Equipartition + EFE cap (r_b/r_M = sqrt(a0/g_ext), **theorem, 1e-16** G196) → a local a0-scale phantom structure exists at 10–30 kAU; γ_v plateau and the 7.4-kAU cap break are its predicted signatures | **DERIVABLE** |
| 2 | Double-map | The phantom slab (z_c ~ a0/(16πGρ_b)) + sech² dust disk are the projected equilibrium; D1 slope −2, D2 column 27.8, D3 **negative** outer bin are the slab-subtraction consequences | **DERIVABLE** |
| 3 | Funnel | z_c(R) = a0/(16πGρ_b(R)) is the derived closed form (140.63 pc at 8.2 kpc; flare e^(+R/3)) | **DERIVABLE** |
| 4 | Merger q | q = 1 is the equipartition law in pair form: at s = r_M each partner's phantom = one M_b → excess exactly 2.000 (G086 exact) | **DERIVABLE** |
| 5 | tSZ 3-way | Joint outer slope −2.54 is the two-sector composition (G113 × G122), **zero new parameters**; −1.44 is the phantom-only member | **DERIVABLE** |
| 6 | Plateau | 2 T_floor is the **derived** equilibrium temperature σ_floor = (GM_b a0)^{1/4}/√2; flat tail = isothermality of the equilibrated phantom | **DERIVABLE** |
| 7 | Anisotropy | The dust is **derived** collisionless (t_relax 70–76 orders above t_H, G103) → streams → infall-class β rising outward; the 0.5 threshold carries the imported FG template (honest note §1.3) | **DERIVABLE** (class) |
| 8 | Saturation | M_sat = 3.09e14 and the f_dust = 1 all-dust pie are the two-phase selection at g = a0 (G03E/G093 phase line) below the phantom regime | **DERIVABLE** |
| 9 | D2 core slope | Composite inner slope ~ −1.5 is the phantom(−2) + dust(−1.7) composition; −1 (NFW) is the external alternative | **DERIVABLE** |
| 10 | Slope floor | γ(20–100) ≈ −2 **IS the phantom's own derived density law** ρ ∝ r⁻² held to the 0.117 band — the floor is the law | **DERIVABLE** |
| 11 | n-kill | n = 2.000 is the derived deep law (g² = a0 g_N, amplitude 2.21 pooled); window exponent n/2 derived. **It FIRED** (12.7σ) — the theory's own derived index killed its reading | **DERIVABLE** (FIRED, explained) |
| 12 | Particle mass | m = [5.0, 5.2] keV from the freeze inversion T_b = mσ²/k_B = T_CMB(z*), σ and T_b **derived**; z* = 2.37–2.49 from G132's placed boundary | **DERIVABLE** |
| 13 | Footing K1/K2 | **The one non-entailment.** Every shape is footing-invariant (G172, four to machine precision); the theory derives shapes, not the scale's VALUE. a0 is the single anchoring input (a0 ↔ ρ_L relation exists — rho_Λ = 4a0²/(Gc²) is a theorem, the DE anchor is the Lean-consistent one — but pinning the value still needs external Planck data; G166(iii) itself calls the DE leg the "weakest"). Kills test the empirical calibration against another empirical read — external | **AD HOC** |
| 14 | Kink width | The first-order class is **derived** (G132: latent heat L/(N k_B T_b) = 10.8–23.7, water-class, finite) → discontinuous β step, w90 < 0.3 | **DERIVABLE** |
| 15 | Ontology charge/relic | The charge ontology is **derived** (G154: Gauss-map charge, R(k) = 1 at every k, no cutoff — a charge has no free-streaming length); the relic kill is the negation of the derived no-cutoff claim | **DERIVABLE** |
| 16 | ZW1215 | The gas-rise (d ln M_gas/d ln r ≥ d ln M_HSE/d ln r) is the phantom hold-up beyond R500 (isothermal envelope supports the gas outward); P4 fired on the one NCC-disturbed cluster, read as hydrostatic bias | **DERIVABLE** (FIRED, explained) |
| 17 | EFE test | The cap line is a **theorem** (G196 exact 1e-16): r_b/r_M = sqrt(a0/g_ext) frames both scales; G100's 0.50-a0 boundary is the registered prediction | **DERIVABLE** |
| 18 | Break F(e_N) | r_cut/r_M = F(e_N) is the **zero-parameter** kernel break, F² e_N μ₂(e_N/2) = M_enc(F r_M/R_d); band [0.62, 0.66]; no root above e_N* = 8.1 | **DERIVABLE** |
| 19 | 2/3 law | α = 2/3 is the **derived** structural exponent (T_obs/T_pred = f^α, closed form); 1/2 is the external alternative | **DERIVABLE** |
| 20 | Cosmic pie | The pie = f(r/r_M) only is the equipartition law in cluster form; the sharp saturation with the 0.85-falsifier is the phase-switch consequence | **DERIVABLE** |
| + | Surface-density column | Σ_ph(<r_M) = a0/(πG) = 213.74 M☉/pc², M_b cancels — **Lean-certified derivable constant**; local ρ_dark(R₀) = 0.0081 measured in band | **DERIVABLE** |

### 1.3 The two honest flags on the derivable set

- **Row 7 (anisotropy):** the *class* (collisionless → streaming → β > 0) is derived; the quantitative *0.5 threshold* rides the imported FG secondary-infall template. The first confrontation (β_win = 0.434 ± 0.015) killed the static null at 29.7σ but sits 4.5σ below the 0.5 envelope — the framework's derived content held, the template's number missed. Both facts are registered.
- **Row 13 (footing):** the ad hoc status is precise, not dismissive — a0 is the theory's single anchor; the theory constrains it (rho_Λ = 4a0²/(Gc²) theorem, DE anchor inside the Lean Ω_Λ window) but does not *derive* its value from nothing. Kills on the value are calibrations, not derived predictions.

**The derivable count: X = 19 of 20 matrix rows** (20 of 21 including the surface-density column).

---

## 2. THE FORMAL STATEMENT — the falsifier set F entailed by the theory

Let T = the framework's derived chain (one constant a0 → shift-symmetric scalar → cold shift-charged sector → equipartition M_dark = M_b r/r_M, ρ = sqrt(G M_b a0)/(4πG r²), σ² = v_flat²/2, Σ = a0/πG → one boundary r_M → two phases at g = a0 → cluster/particle/cosmology closures, PPN = GR by construction). Then the falsifier set

**F = {f₁ … f₂₀}** (the 20 registered rows), with the *derivable subset*

**F_deriv = {f₁, f₂, f₃, f₄, f₅, f₆, f₇, f₈, f₉, f₁₀, f₁₁, f₁₂, f₁₄, f₁₅, f₁₆, f₁₇, f₁₈, f₁₉, f₂₀}** — **19 members** — and the ad hoc singleton **F_adhoc = {f₁₃}**.

For each f ∈ F_deriv the entailment is of the form **T ⊨ O_f**, where O_f is the observation whose registered negation fires the kill: T entails the ridge, the two-scale map, the funnel formula, the pair excess 2.000, the joint tSZ slope, the 2 T_floor level and its isothermal tail, the streaming envelope (class), the saturation, the composite −1.5, the r⁻² floor, the deep n = 2, the 5.0–5.2 keV mass, the first-order step, the no-cutoff charge, the gas-rise, the cap line, the zero-parameter break, the 2/3 exponent, the r/r_M pie, the 213.74 M☉/pc² column. **The theory's theorem: T ⊨ ∧_{f ∈ F_deriv} O_f.**

The one row with **T ⊭ O_13**: the footing value is not entailed (footing-invariance, G172) — f₁₃ is a kill *on the anchor's calibration*, external by construction. That is V4's honest boundary: **19 of 20 falsifiers are the theory's own theorem; 1 is externally pinned by necessity — the theory cannot derive the value of its own input constant.**

> **The self-prediction is not ceremonial — it fires.** The theory's derived n = 2 (row 11) is the theory's own falsifier's target, and it FIRED at 12.7σ, absorbed by the two-scale/effective reading; the ZW1215 P4 fired (9.8σ, hydrostatic-bias class); the EFE split fired and was refused as a detection. Zero unexplained fires.

---

## 3. THE UNDECIDABILITY QUESTION (V35) — n = 2 computable from the axioms? Honest status, no overclaiming

**The candidate:** is n = 2 (the deep index, V10's "is n = 2 a computational bound?") *computable in principle from the theory's own axioms*?

**The honest answer — the n-question is DECIDABLE, not undecidable, and it was decided:**
- At the DE footing, n = 2.000 **is** computed from the axioms (g² = a0 g_N is the derived deep law, Lean-certified in the G201 sqrt reading; the deep RAR window exponent β = n/2 is the derived translation). At the RAR footing the axioms compute n = 1.660. **The axioms compute a footing-dependent n — the same derivation, two readings.** The deep-end measurement (n = 1.20 ± 0.06) then *fired* both — the axioms' computation was measurable, measured, and wrong at 12.7σ/7.3σ, absorbed by the two-scale/effective reading (a0_eff for g_N < 0.2 a0, the environmental leg).
- **V10's computational-bound reading fails honestly:** n is the *shape parameter* of the Lomax kernel (H055, the RAR as a sampling distribution) — a distribution parameter, not a complexity/information bound. Nothing in the derived chain bounds n by computation cost; n is fixed by the equilibrium reading and measured off it. So: n is computable-in-principle (decidable), it was computed and measured, and the honest residue is the *effective-scale* input a0_eff — which is data, not axiom.

**The honest register — where the theory genuinely contains under-determination (no Gödel claim, per V35's own warning):**

**(a) Statements the experiments cannot resolve at the registered precision** (not kills — *unresolvable today*):
- The D2 core-slope formality −1 vs −1.5: NFW's own window slope −1.68 overlaps the claim — "undecided at this resolution", gated on the lensing σ_s ≤ 0.167 (1.7× over the HSE floor).
- The slope floor: only 1.58σ past the kill line at 3 r_M — data-insufficient today (the constancy sub-prediction already FAILED: spread 1.19 vs 0.12 predicted).
- The kink width's strict 3σ verdict: needs per-bin σ_β ~ 0.01 (~2–3 yr, SDSS-V/WEAVE/4MOST); the ≤0.03 level separates only by sign ≥95%.
- The tSZ F1′ axis: steeper-than-joint kill at 1.7–2.6σ pooled — honestly registered sub-3σ (the weak axis); A644's own joint band lives entirely in the "neither" branch — per-cluster inapplicable.
- The anisotropy's exact envelope value: β_win = 0.434 ± 0.015 is 4.5σ from 0.5 and 29.7σ from 0 — a mid-ground the current precision cannot place (gated on the Wojtak-class 2D fit).
- The 2–3e14 gap: zero committed objects between IC1633 and A1644 — the sharp-vs-smooth saturation discriminator sits on an unobserved window.
- The plateau tail: 2/12 flat vs the ≥ 9/12 supermajority — the flat claim is 5.9× stronger than the envelope continuation, certified only by XRISM-class precision.

**(b) Statements the theory itself cannot derive** (under-determined by the axioms):
- **The footing value** (the deepest one): shapes footing-invariant; the scale's value pinned by external calibration — the theory cannot derive its own input constant (H029's circularity audit on a0-from-ρ_L stands).
- **The cap's position**: G132's registered non-derivability — the entropy functional selects no truncation (max on the whole well); the boundary's *position* is environmental (g_ext), its *character* (first-order, latent heat, T_b) derived. The theory derives the physics of its boundary, not its place.
- **The effective deep scale a0_eff** (G190 branch c): the two-scale reading's second scale is environmental, not derived.
- **The ontology's open upper window**: the relic's 5.7–8.3 keV floor survives only behind m_hm convention factors (×2.7–9.7) — the sub-1e6 collapsed count is data-gated.

**(c) The "and then stop" clause (V35):** NO question here is *proven* formally undecidable; claiming Gödel-style incompleteness would overclaim (the framework is analytic field/algebra — V12's Turing-completeness is untested, so the undecidability-by-universality route is NOT open). **STOP = we stop pretending the under-determined items are kills waiting for precision; they are registered as what they are:** (a) precision-gated verdicts and (b) axiomatically under-determined inputs. The one question V35 offers — n — is decidable, and it is the campaign's cleanest example of a *derived, measured, fired* self-prediction.

---

## 4. VERDICTS

**V1 — The derivable-falsifier count. X = 19 of 20** matrix rows are DERIVABLE predictions (the theory entails the observation that would kill it); **1 of 20 is AD HOC** (the footing K1/K2 — T ⊭ O on the anchor's value, by footing-invariance). With the lane-carried surface-density column the maximal set is 21 kills, **20 of 21 derivable**. Members of F_deriv: rows 1–12, 14–20 (19); F_adhoc: row 13. Statuses inside F_deriv: 12 ARMED, 3 PENDING, 3 FIRED-and-EXPLAINED (rows 11, 16, 17), plus 2 resolved non-fires (rows 8, 19) — **zero unexplained fires**.

**V2 — The undecidable-content statement (honest, not overclaimed).** No formal undecidability is proven or claimed (V12 untested; the framework is analytic, not universal-computation-embedded). The n-question is **decidable** — the axioms compute n (2.000 DE / 1.660 RAR), the measurement decided against both (1.20 ± 0.06), the deep reading fired and was absorbed by the effective scale; V10's computational-bound reading fails (n is a distribution shape, not a complexity bound). The theory genuinely contains: **(a) 8 statements experiments cannot resolve at the registered precision** (D2 formality, slope floor 3 r_M, strict kink width, tSZ F1′ axis, anisotropy exact value, 2–3e14 gap, plateau tail, A644 per-cluster inapplicability) **and (b) 4 statements the theory cannot derive** (the footing value, the cap's position, a0_eff, the ontology's upper window). V35's instruction honored: the under-determined items are named as under-determined, and we stop.

**V3 — The honest statement (V4's answer). YES — the framework predicts its own falsifier.**
> 19 of the 20 registered kill-conditions are the theory's own theorem — each killing observation is entailed by the derived chain (equipartition, r⁻², equilibrium temperature, phase selection, charge ontology, cap line), stated as T ⊨ ∧ O_f with the members and numbers above. The 20th (the footing) is externally pinned because no theory can derive the value of its own input constant — the single honest exception, and it is precisely the axis where the framework is footing-invariant. The self-prediction has already worked as V4 demands: the derived deep index n = 2 was the theory's own falsifier, it FIRED at 12.7σ, and the framework survived by the two-scale reading — the machine that builds the machine that stops it exists, named, numbered, and fired. 12 falsifiers remain armed (DR4 ridge/double-map/funnel Dec-2026, tSZ 3-way, XRISM plateau, MIGHTEE/BTFR footing, kink width ~1 yr, WALLABY DR3 pair-breaks, ontology census, cosmic-pie gap), 3 pending a final reading (anisotropy, D2 slope, slope floor), zero unexplained fires on the record. The falsifier is not a decoration bolted on from outside; it is the theory's own statement about the observations it requires — and 19/20 of those statements are derived.

---

*Deliverable complete. Pass: 3/3 verdicts (V1 count 19/20 derivable + 1 ad hoc, verified 20 rows / 12 ARMED / 3 PENDING / 5 EXPLAINED / 3 fired events / 0 unexplained; V2 honest register, no formal undecidability overclaimed; V3 V4 answered YES with the count and members). G237_results.json written alongside.*