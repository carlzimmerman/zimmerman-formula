# G221 — THE MNRAS ABSTRACT + INTRODUCTION
**The paper's opening, drafted from the closure state: the claim, the law, the force-face, the particle, the observables, the puzzle, the one-boundary framing, and the plan of the paper.**

*Lane: G221. Repo: zimmerman-formula. Date: 2026-09-16.*
*Sources (all committed, nothing recomputed): THEORY_CLOSURE_2026-09-16.md (G205), MNRAS_RESULTS_SKELETON.md (G202), ONE_BOUNDARY_STATEMENT.md (G196), LAW_VERIFIED.md, FALSIFIER_MATRIX.md (G207), G209_results.json (the anisotropy profile), G206/G203 (the window mean), G168 (the mass), G184 (the outer slope), G088/G165 (the DR4 ridge). Companion artifact: G221_results.json.*

---

## PART 1 — THE ABSTRACT (~200 words)

**Title (recommended):** *The radial acceleration relation is the phase diagram of a single boundary: the dark sector's equilibrium at its virial temperature*

**Abstract (200 words):**

> The observed radial acceleration relation (RAR) between a galaxy's total and baryonic accelerations is reproduced with zero free parameters; we show the RAR is not a force law but the equation of state of a cold, shift-charged sector of one scalar field, equilibrated at the virial temperature its vacuum scale sets. The theory contains exactly one boundary — the baryonic a0-crossing, r_M = sqrt(G M_b/a0) — and one sector: inside r_M the missing mass is un-equilibrated free dust; outside, sub-a0, the phantom equilibrates and dominates. The law M_dark(<r) = M_b r/r_M holds across 12 decades of baryonic mass with slope b = 1.004 ± 0.011 (n = 542); cluster temperatures follow the same switch with structural exponent 2/3 (31 systems, rms 0.076 dex); the dust law's two parameters are now both derived within the measured error. No force is modified in any regime: PPN = GR identically and the Cassini null is architectural. The sector makes one mass prediction, m = 5.0–5.2 keV, and carries three new observables: a velocity-anisotropy profile rising from β ≃ 0.03 at the core to 0.56 at 5 R500; a cluster outer envelope falling as r**−2.40 ± 0.08, 7.7σ from NFW's −3; and a wide-binary ridge pre-registered for Gaia DR4 at 30.7σ.

**Count: 207 words** (whitespace-token count; verified at write time — see G221_results.json C1).

---

## PART 2 — THE INTRODUCTION (~400 words)

Galaxies rotate faster than their starlight explains, and the discrepancy is not arbitrary: the observed acceleration at every radius is one tight function of the baryonic acceleration alone, holding across thousands of galaxies and four decades of acceleration with scatter only at the measurement level. The standard resolution — a cold-dark-matter halo per system — reproduces the relation only by construction: one halo per galaxy at the price of thousands of parameters. Modified-dynamics theories attribute the excess to a changed force below a0 ≈ 10⁻¹⁰ m s⁻², but a0 floats and every force-law completion that could source the deep relation is dead on existing constraints (§5).

The cluster sector is the second face of the same puzzle. There the missing mass heats X-ray temperatures and holds the outer envelopes, and the division between equilibrated and streaming dark matter — the sector pie — had to be refitted at every mass. The same scale governs both faces: the RAR bends exactly where the baryonic field falls to a0, and the cluster environment sits at the a0 floor.

This paper reads both faces from one mechanism: the cold sector is the shift-symmetry charge of one scalar field whose vacuum value is dark energy. The field sets one equilibrium temperature — the virial temperature of maximum entropy at the vacuum scale — and wherever the baryonic field is deep (g < a0) the sector equilibrates to it; where it is strong, collisionless free dust carries the deficit. The theory has exactly one physical radius, the baryonic a0-crossing r_M = sqrt(G M_b/a0), and it is a phase switch: interior, the dust carries the missing mass; exterior, the phantom equilibrates and dominates. Every phase change in the dark sector — the Milky Way's rotation-curve break, the cluster density seam, the temperature pivot, the sector pie — is this one boundary, the environment projecting it through r_b = r_M sqrt(a0/g_ext). The RAR is the phase diagram of this one boundary.

The plan of the paper. Section 2 states the action and the machine-checked equilibrium identification. Section 3 describes the data. Section 4 presents the results section by section: the equipartition law across twelve decades (§4.1); the one boundary and its diagnostics (§4.2); the cluster sector in closed form (§4.3); the dark sector's two phases and the predicted carrier mass (§4.4); the force-face, PPN = GR with no fifth force (§4.5); and the open items with their falsifiers (§4.6). Section 5 sets the framework against the dead routes and the verdicts awaiting Gaia DR4, the z ≈ 2.5 Tully–Fisher zero point, the thermal-SZ 3-way, and XRISM.

**Count: 429 words** (whitespace-token count; verified at write time — see G221_results.json C2).

---

## PART 3 — THE HONEST FRAMING: what is new, what is dead, what was corrected

**What is new and owned.** The framework's claim is not a new force and not a new species per galaxy. It is a reading: the RAR is the equation of state of a sector whose equilibrium temperature is set by the vacuum scale — an equilibrium/EOS theory, with the deep law's coefficient fixed to one (the phantom rho = sqrt(G M_b a0)/(4 pi G r^2), Lean-certified), the equipartition M_ph(<r_M) = M_b exact to |ratio−1| = 2.2e-16, the universal surface density a0/(pi G) = 213.74 M_sun/pc^2, and a predicted carrier mass. The over-determination is the strength: ten independent diagnostics sit on the single boundary r_M.

**The dead routes, cited (in print).**
1. **The fifth-force closure (G155).** No shift-symmetric force-law completion can source the deep equation: every completion carries an unscreened O(1) fifth force with gamma = 1/2 (Cassini fails 2.2e4x); a 44-solve scan of the surviving modification classes never drops below 6.18x the Park 2025 ceiling, and the smooth-shell lemma closes the isotropic-screen class with proof. The Solar System is Newtonian by construction — the Cassini null is architectural, and PPN = GR identically (c_T = c, gamma = 1, alpha_1 = alpha_2 = 0).
2. **The k^4 closure (G030/G034).** Seven local quartic-operator classes (k^4 modifications of the stress/kinetic sector) are dead: no local higher-derivative modification sources the deep relation. The deep law is not an operator expansion — it is an equilibrium statement, which is why the equilibrium reading, not a modified action, is the survivor.
3. **The seesaw's demotion (G189).** The apparent identity between the RAR scale and the vacuum scale (a0 = Lambda^2/2 M_Pl) is by construction an identity, not an independent tracking law — the +0.07% Omega_Lambda closure is the inversion of a definition; the global n(a0) tracking relation is rejected at 8 sigma, and n = 2.000 survives only as the full-curve convention. a0_DE remains the unique cosmological reading of the identity; the paper cites this correction rather than the old claim.

**The claim, stated at confidence.** The law is measured, not assumed: b = 1.004 ± 0.011 at n = 542 over log M_b = 2.63–14.35 (0.4σ from unity), rms 0.180 dex; the temperature law's structural exponent 2/3 fits 31 systems at 0.076 dex with the virial 1/2 excluded at ~2.2σ; the cluster dust law is closed to its last parameter (q measured −0.414 ± 0.157, derived −1/3 at 0.52σ); the outer envelope slope −2.404 ± 0.078 stands 7.7σ from NFW's −3 on three independent instruments. The registered caveats stay in the text: the seam's sharpness is provisional (d_BIC = 16 to smooth steepening — "a resolved transition"), and the cap's firing mechanism is not derived (its environmental placement is).

**The observables on the table.** Measured here: the 12-decade line; the dSph floor (0.222 dex median over 34 dwarfs); the one boundary's ten diagnostics (break 0.623 r_M, seam 0.96 r_M, latent heat 10.8–23.7 k_B, A_jump 0.650/0.484); the cluster pie (17.7/56.9/24.6 at R500); the anisotropy profile beta 0.03 → 0.56 across 0.5–5 R500 (static null dead at 29.7σ); the cosmic closure Omega_dust = 0.2619 = 99.2% of Omega_dm with equilibrium + dust = 1.000. Armed and awaiting their instruments, each with a kill number in print (§4.6 and the falsifier matrix): Gaia DR4 on 2026-12-02 (the 30.7σ ridge, the 7.4-kAU break, the double-map, the funnel; scorer 9/9 on mocks), the z ≈ 2.5 BTFR zero point (20:1 per clean point), the tSZ 3-way (joint −2.54, 47.8σ pooled vs phantom-only), the XRISM plateau, the sub-1e6 collapsed-halo count (charge vs relic), and the kink-width contract. Three registered events have fired and all three carry registered explanations (the ZW1215 hydrostatic-bias case, the n = 2 deep reading absorbed by the two-scale reading, the EFE split refused as a detection); the ledger reports zero unexplained fires.

---

## PART 4 — VERDICTS

### V1 — The abstract is complete.
The 200-word abstract carries the claim (one scalar field, one boundary, one sector), the law (M_dark = M_b r/r_M; the 12-decade line b = 1.004 ± 0.011, n = 542; the temperature law's 2/3; the dust law with both parameters derived — the zero-parameter standing statement), the force-face (PPN = GR, no fifth force), the particle (m = 5.0–5.2 keV), and the three key new observables (the anisotropy profile beta 0.03 → 0.56; the DR4 ridge at 30.7σ; the outer slope −2.40 ± 0.08 at 7.7σ from NFW). 207 words. PASS.

### V2 — The introduction is complete.
The ~400-word introduction states the puzzle on both faces (the RAR's parameter-free tightness with no first-principles a0; the cluster sector's refit-per-mass), the one-boundary framing (r_M as the phase switch between strong-field free dust and deep-field phantom, projected by the environment, the RAR as the boundary's phase diagram), and the plan of the paper mapped to the results skeleton's sections (§2 action/equilibrium, §3 data, §4.1–4.6 the law/boundary/cluster sector/dark sector/force-face/open items, §5 discussion). 429 words. PASS.

### V3 — The honest statement is ready for the author's voice pass.
The opening is drafted from the closure state with the claim stated at confidence (the law's numbers with their significances; the caveats in the text, not hidden), the dead routes cited (the fifth-force closure G155, the k^4 closure G030/G034, the seesaw's demotion G189), and the observables listed in two columns — measured and armed — each with its instrument and kill number. What remains is the author's voice pass: the sentences carry the campaign's register of precision, and the voice pass should set tone and trim the parentheticals, not add or remove claims. PASS.

*Deliverable complete. Pass: 3/3 verdicts. G221_results.json written alongside.*