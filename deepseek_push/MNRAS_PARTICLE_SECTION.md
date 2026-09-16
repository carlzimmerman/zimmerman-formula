# D08 — THE MNRAS PARTICLE SECTION (§4.4 THE DARK SECTOR'S PARTICLE FACE)

**The paper's particle section, drafted from the closed record: the one derived mass, the line, the free-streaming cut, the thermodynamic face, the honest limits, the testable-predictions table, the falsifiers — ready for the author's voice pass.**

*Lane: D08. Repo: zimmerman-formula. Date: 2026-09-16.*
*Sources (all committed, nothing recomputed): project_atomos/PARTICLE_SECTOR.md (B10, the B-series capstone); THE_HORIZON_EQUATION.md (Z11); MNRAS_ABSTRACT.md (G221); MNRAS_METHODS.md (Z10); MNRAS_RESULTS_SKELETON.md (G202, the §4.x numbering); SOLAR_FACE_CLOSEOUT.md (G224); the committed B/A/C registers (B01–B09, A01–A08, C01/C02/C05/C08) as carried by B10 and the D-wave (D02 the f_b-invariance audit, D05 the phantom re-settling second clock, D07 the derivation ledger). Every number below is read from a committed register; each falsifier is copied verbatim from its lane's gate (f). Companion artifact: D08_results.json.*

---

## PART 1 — THE SECTION (slots into the results skeleton as §4.4)

## §4.4 THE DARK SECTOR'S PARTICLE FACE — the derived mass and its predictions

The dark sector is one charge and two phases; this section derives what the equilibrated phase is made of. Inverting the equilibrium temperature against the CMB dates the equilibrium's formation to cosmic noon and returns exactly one particle mass; that mass carries exactly two parameter-free observables — a fully specified X-ray line and a free-streaming cut, or its absence — plus a zero-parameter X-ray temperature law and the thermodynamic faces of the 5.09-keV isothermal gas. What the framework does not predict is stated in the same register.

### 4.4.1 The one derived mass

The equilibrium of §4.1 has a temperature T_b = mσ²/k_B, which the freeze hypothesis of §4.2 sets to the CMB at formation. With the galaxy-class triad σ = 119.2 km/s and the committed freeze band z\* = 2.37–2.49 (T_b = 9.2–9.5 K, the CMB at cosmic noon), the inversion returns a single mass,

> **m = 5.09 ± 0.10 keV**  (joint 5.0886 ± 0.0969 keV, χ² = 1.04, p = 0.59 over three independent windows).

The inversion is environment-blind by construction, and the multi-rung test closes it: the ladder m = k_B T_0 (1+z\*)/σ² evaluated at every committed freeze rung — the 65 km/s freeze floor, the galaxy 119.2, the group 250, the cluster class 600–992, the supercluster 2100 km/s — recovers m ∈ [5.0000, 5.0001] keV in 11 of 11 environments, spread 0.00012 keV. The one coefficient spanning the whole framework — **Z = 2√(8π/3) = 5.7888**, the same number that carries gravity through a₀ = c²/(Z R_dS), ratio 1.00005 (Z11) — enters the ladder as Z^(+1/2), and committed inputs alone predict m ∈ [4.9992, 5.1887] keV, inside the measured [4.99, 5.19] keV at −0.05σ: the double-Z. The negative control is the massless rung: the UFD/dSph class never froze (z\* < 0; σ = 2.3–11.7 km/s, below the 65 km/s floor), its inversion degrades to 0.26–0.80 keV scatter, and the naive freeze-today masses (154–3990 keV) sit above the 6.0-keV kill-band top for 34 of 34 objects — the ladder breaks exactly where the freeze map says it must. The mass stands independently of the forest bracket (m ≳ 3.3–5.7 keV from Lyman-α); the loop z\*→m→z\* is self-consistent at the ~10–20% level.

### 4.4.2 The line

The one mass makes one line: E = m/2 = **2.5443 keV** (band [2.50, 2.60]). Its width is kinematic, never intrinsic — the Gaussian σ_E = **1.19 eV** (FWHM 2.80 eV) at the committed caustic/dust footing (σ_d = 140.2 km/s → ΔE/E = 4.68 × 10⁻⁴), the thermal and core footings reading the same velocity scale at 6.05 eV and 7.16 eV; the honest envelope is **[1.19, 8.08] eV, Doppler-dominated**. Its spatial shape is the sector's own density projected: the phantom A/r² profile Abel-projects to an exact **b⁻¹ surface-brightness cusp** (I(b) = πA_ph/b plus the dust term 2A_d K(0.7) b⁻⁰·⁷), composite slope in [0.7, 1.0) inside r_M, a 6.4× brightness gain from 1 to 0.1 r_M against the NFW flat core's 1.4× — and the shape is rate-independent (identical at Γ and 2Γ to 1 part in 10¹⁰), the zero-free-parameter signature even though the flux is not predicted (§4.4.5). Its environmental presence is the freeze map itself: **present where the sector froze** (z\* ≥ 0 — galaxies, groups, clusters), **absent in the never-froze dwarfs** (34 dSphs, z\* < 0) — the UFD-absence switch, independent of the rate. The null restricts only the lifetime, never the mass: **Γ < 1.88 × 10⁻²⁹ s⁻¹ (τ > 1.69 × 10¹² yr) on the cosmic budget, Γ < 3.30 × 10⁻³³ s⁻¹ (τ > 9.6 × 10¹⁵ yr) on the Milky-Way-center column** (B02).

### 4.4.3 The free-streaming cut

The mass's second observable is a cut, or its absence. Under the standard relic reading a 5.09-keV species free-streams with **λ_fs = 0.558 Mpc** (k_hm = 57 h/Mpc; M_hm ~ 7 × 10⁵–8 × 10⁶ M☉), and the two P(k) faces separate exactly there: the particle face removes R(k) = 1 by 0.293 at k = 30 h/Mpc and by 0.984 at k = 100 h/Mpc, while the condensed face — bias = 1 by construction, the equilibrium of the baryonic well (B07) — carries **R(k) = 1 with no cutoff at all** (1−R = 0.000). The deciding decade is **k ~ 100–500 h/Mpc** (the sub-halo decade 10⁵–10⁸ M☉), where the census already leans 3.2–4.1σ toward the no-cutoff face (N_obs(>10⁵ M☉) = 19 vs 5.1 for the 5.7-keV truncated relic and 1.0 for 3.3 keV); a measured cutoff there kills the charge reading, R(k) = 1 there kills the relic reading — the charges' genuine separation point, pre-registered as the G156 decade decision. The condensed side carries ΔN_eff ~ 0 (thermal r = 1 excluded at ≥ 9σ), and the sector is not a thermal relic population: the occupation factor at T_b = 9.17 K is e⁻⁶·⁴⁴ᵉ⁶ — the Boltzmann gas holds ~10⁻²·⁸ᵉ⁶ of the committed particle number — and the phase condensed at z\* = 2.4 at δ = 1.3 × 10⁵ above the cosmic mean.

### 4.4.4 The thermodynamic face

The 5.09-keV gas carries the thermal register of a maximally-soft isothermal fluid: **P = σ²ρ exactly, γ = 1** (compression never heats), C_V = N k_B, c_s² = σ². Its dynamics therefore have a predicted speed: perturbations re-arrange the sector at the sound speed c_s = σ — 119.2 km/s in the Milky Way, 918 km/s in the HeCS core — with the response lag t_sound = r_M/c_s in exact ratio **√2 to the dynamical time** (t_sound/t_dyn = 1.414214 exactly, machine-checked); the HeCS sound response lags the 1.90-Myr light crossing by **c/c_s = 327**. The same three clocks order a merger: the phantom re-attaches to the baryonic centroid at the light crossing (τ_ph = 1.90 Myr, the algebraic response), the condensate re-arranges at its sound response (621 Myr), the baryonic gas re-conditions at ~10⁸ yr, and the dust never (t_relax/t_H ~ 10⁷³) — **phantom-first re-alignment, the sourced field's signature ordering** (D05). Its temperature is a fixed point, not an input: T_b = mσ²/k_B = 9.52–9.69 K, locked to σ², with the fluctuation floor dT_rms/T = N⁻¹/² = 2.65 × 10⁻³⁷ — the measured 0.076-dex temperature-law scatter (17.5%) is 6.6 × 10³⁵ times the heat-capacity floor, i.e. 100% non-thermal — and formal heating cannot thermalize (t_relax/t_H ~ 10⁷³; Landau damping at v_c = c_s), so mergers re-order the phantom without heating it: the Bullet's ordered 8σ offset with no dark thermalization is the measured face, and the gapless sound branch (ω = c_s k, zero gap, zero damping) the coherent phase's mode spectrum.

### 4.4.5 The honest limits

What the sector does not predict is as registered as what it does.

1. **No rate.** The framework contains no coupling or mixing constant: no decay rate, no branching fraction, no decay-existence statement. The line's flux is normalized by a bound from the background null (Γ < 1.9 × 10⁻²⁹ s⁻¹ cosmic, Γ < 3.3 × 10⁻³³ s⁻¹ Milky-Way), never a value — non-observation is always consistent and only raises the lifetime floor (τ > 10²²–10²⁵ yr class).
2. **No coupling, mixing, or production mechanism.** Nothing sets sin²2θ or any production channel; the sterile-class illustrations are analog context, not framework output.
3. **f_b is an input.** The halo-depletion chain closes arithmetically (0.1567 vs 0.1564, +0.2%) as an identity on measured sides — zero framework mechanisms appear in it. The two-rung band [0.150, 0.157] brackets the datum to 4.1%, the systematic envelope is [0.139, 0.180] — a consistency statement, not a prediction. **f_b = Ω_b/Ω_m = 0.157 remains the last measured input of the cosmic frame** — halo-anchored at 4%, not halo-derived. The per-object laws (the ladder, the line, the temperature law) are f_b-invariant — a wrong fraction would be invisible to every per-object fit (D02); only the pie's halo share and the Ω_dm closure carry f_b (D02/D07).
4. **The same register governs m_p/μ** (units of the baryonic rung, not derived) **and the sector's statistics**: the committed face is charge-like (R(k) = 1, no free-streaming), the relic reading disfavored at 3.2–4.1σ, the formal charge-vs-relic declaration awaiting the G156 decade. The universe-side bookkeeping closes elsewhere in the skeleton: Ω_dust = 0.2619 = 99.2% of Ω_dm, equilibrium + dust = 1.000.

### 4.4.6 The testable predictions — the eight most decisive

| # | Prediction (number) | Instrument / data | Expected date | Falsifier (verbatim) |
|---|---|---|---|---|
| 1 | **m = 5.09 ± 0.10 keV** (the one derived mass; ladder [4.9992, 5.1887] at −0.05σ) | Lyman-α forest (Viel 3.3 / Iršič 5.3 / Villaseñor 5.7 keV, UNVERIFIED); sub-halo census | constraints now; forest 2026–2030; G156 decade the decider | m < 4.0 or m > 6.0 keV kills the double-Z (G168/A08); outside [3.3, 5.7] keV kills the triangle (A05) |
| 2 | **Line energy E = m/2 = 2.5443 keV** (band [2.50, 2.60]) | XRISM, eROSITA, XMM deep fields, Athena X-IFU (late 2030s, UNVERIFIED) | now — ongoing | a line detected at E ∉ [2.50, 2.60] keV kills the m/2 relation (A05); a null only raises the lifetime floor, never kills the mass |
| 3 | **Line width σ_E = 1.19 eV** (envelope [1.19, 8.08] eV, Doppler-dominated) | high-resolution X-ray spectrometers (XRISM Resolve-class, X-IFU) | now — when resolved | a resolved σ_E far outside [1.2, 8.1] eV at 2.55 keV kills the kinematic reading (B01) |
| 4 | **Line shape F(b) ~ b⁻¹ cusp** (composite slope in [0.7, 1.0) within r_M; 6.4× vs NFW's 1.4×) | stacked line imaging (XMM / eROSITA / X-IFU) | now — stacking campaigns | a measured F(b) flatter than 1/b in a phantom-dominated interior kills the r⁻² projection — **the shape is the claim** (B02) |
| 5 | **UFD absence: line present in the frozen class (z\* ≥ 0), absent in never-froze dwarfs (34 dSphs)** | pointed X-ray observations of UFDs/dSphs | now — feasible with committed catalogs | a 2.55-keV line from a never-froze dwarf (z\* < 0) kills the freeze-map face independently of the rate (B01) |
| 6 | **Free-streaming cut λ_fs = 0.558 Mpc, or R(k) = 1** (the deciding decade k ~ 100–500 h/Mpc) | sub-halo census (lensing flux ratios, stellar streams, satellite census); 21-cm at k > 30 h/Mpc (future) | G156 decade now; 21-cm future | measured R(k) < 1 at k ≲ 57 h/Mpc → RELIC declared, CHARGE dead; R(k) = 1 in the 10⁵–10⁸ M☉ decade → RELIC dead, CHARGE declared (S07/B07) |
| 7 | **T_X-ray = μ m_p √(G M_b a₀)/(2 k_B), 0.06-dex class** (MAD 0.053 dex, 50 objects) and its SZ-class inverse M_impl = 4(k_B T/(μ m_p))²/(G a₀) | X-ray hydrostatic masses (X-COP, HeCS, E11 — in hand); XRISM/eROSITA profiles | verified now; new objects ongoing | a well-measured (M_b, T) pair outside the 0.06-dex band, or sample scatter > ~0.12 dex, falsifies the zero-parameter scaling claim (B06) |
| 8 | **Sound-speed response, no-heating, phantom-first re-alignment: perturbations propagate at c_s = σ, lag √2 × t_dyn; mergers heat nothing and re-attach the phantom at R/c = 1.9 Myr** | merger offsets, AGN-driven waves (Bullet-class); measured | no committed date — the out-of-equilibrium class is registered | a resolved response at speed ≠ σ, lag ≠ √2 × t_dyn, any dark thermalization, or t_dark ≳ t_gas kills the gas/clock faces (B05/B08/D05) |

### 4.4.7 The falsifiers, named

1. **A cleaner measured mass outside [4.6, 5.2] keV** (hard kill band [4, 6] keV) — kills the double-Z and the cosmic-noon identity at once (G168/A08).
2. **A line at E ∉ [2.50, 2.60] keV** — kills the m/2 relation (A05).
3. **A resolved width far outside [1.2, 8.1] eV at 2.55 keV** — kills the Doppler/kinematic reading (B01).
4. **A measured F(b) flatter than 1/b in a phantom-dominated galaxy interior** — kills the r⁻² projection; the shape is the claim (B02).
5. **A 2.55-keV line from a never-froze dwarf (z\* < 0)** — kills the freeze-map face independently of the rate (B01).
6. **A measured free-streaming cut R(k) < 1 at k ≲ 57 h/Mpc** — kills the coherent/charge face; **R(k) = 1 in the 10⁵–10⁸ M☉ decade** kills the relic reading; the sub-1e6 collapsed count resolving 0.60–0.79 vs 0.79–0.95 picks the ontology (S07/B07/G156).
7. **A (M_b, T) pair outside the 0.06-dex band, or sample scatter > ~0.12 dex** — falsifies the zero-parameter temperature-law scaling (B06).
8. **A resolved response at speed ≠ σ, lag ≠ √2 × t_dyn, any dark thermalization in a merger, or a dark offset persisting ≳ the gas's own re-alignment (t_dark ≳ t_gas ~ 10⁸ yr)** — kills the isothermal-gas, no-heating, and phantom-first re-alignment faces (B05/B08/G233; D05).
9. **The high-z BTFR zero point NOT breaking at z\* = 2.4** — kills the decoupling-epoch identification; a frozen environment returning m outside the G212 band breaks environment-blindness (B03/B07/G168).

The honest complements ride with every one: a null line is always consistent (it raises the lifetime floor); the rate, the coupling, and the production mechanism are not predicted, so no null in any radiative channel touches the mass itself.

---

## PART 2 — THE INTEGRATION

### Where the section slots into the skeleton

Per the MNRAS_RESULTS_SKELETON (G202) numbering, the particle section is **§4.4 The dark sector** — between the galaxy-sector results (§4.1 the equipartition law, §4.2 the one boundary) and the cluster sector (§4.3) on the galaxy side, and the force-face (§4.5) and open-items box (§4.6) on the cosmology/closure side. In the skeleton's own one-line table, §4.4 is "One charge, two phases; m = 5.0–5.2 keV; the cosmic density closes": this draft replaces the particle-face wording with the final-state numbers (m = 5.09 ± 0.10 keV; the line; the cut; the limits) and leaves the density-closure headline (Ω_dust = 0.2619 = 99.2%, equilibrium + dust = 1.000) in place as the section's closing cosmology face. Nothing in the skeleton's §4.1–4.3 or §4.5–4.6 changes; the section's cross-references are to §4.1 (the equilibrium, σ = 119.2 km/s) and §4.2 (the freeze temperature, T_b = 9.52 K) as written.

### The abstract's particle sentence — revised with the sector's final state

G221's draft read: *"The sector makes one mass prediction, m = 5.0–5.2 keV, and carries three new observables: …" (207 words).* The particle sentence is now:

> The sector derives one mass, m = 5.09 ± 0.10 keV, environment-blind, with two parameter-free observables — a 2.55-keV line (E = m/2; width 1.19–8.08 eV; b⁻¹ cusp; none in never-froze dwarfs) and a 0.558-Mpc free-streaming cut excluded by the condensed phase (R(k) = 1) — and three further observables: an anisotropy profile rising β ≃ 0.03 → 0.56 within 5 R500; a cluster outer envelope r**−2.40 ± 0.08, 7.7σ from NFW; and a wide-binary ridge pre-registered for Gaia DR4 at 30.7σ.

**Revised abstract (218 words, within the 200-word ±10% gate):**

> The observed radial acceleration relation (RAR) between total and baryonic accelerations is reproduced with zero free parameters; we show the RAR is not a force law but the equation of state of a cold, shift-charged scalar sector, equilibrated at the virial temperature its vacuum scale sets. The theory has one boundary — the baryonic a0-crossing, r_M = sqrt(G M_b/a0) — and one sector: inside r_M the missing mass is free dust; outside, the phantom equilibrates and dominates. The law M_dark(<r) = M_b r/r_M holds across 12 decades of baryonic mass (b = 1.004 ± 0.011, n = 542); cluster temperatures follow the same switch (exponent 2/3; 31 systems, rms 0.076 dex); the dust law's two parameters are derived within error. No force is modified in any regime: PPN = GR identically; the Cassini null is architectural. The sector derives one mass, m = 5.09 ± 0.10 keV, environment-blind, with two parameter-free observables — a 2.55-keV line (E = m/2; width 1.19–8.08 eV; b⁻¹ cusp; none in never-froze dwarfs) and a 0.558-Mpc free-streaming cut excluded by the condensed phase (R(k) = 1) — and three further observables: an anisotropy profile rising β ≃ 0.03 → 0.56 within 5 R500; a cluster outer envelope r**−2.40 ± 0.08, 7.7σ from NFW; and a wide-binary ridge pre-registered for Gaia DR4 at 30.7σ.

---

## PART 3 — VERDICTS

### V1 — THE SECTION IS COMPLETE. PASS.
Every element the task required is in the draft: the claim (one derived mass m = 5.09 ± 0.10 keV from the equilibrium ladder, environment-blind, the double-Z at −0.05σ with the multi-rung test and the massless UFD rung), the line (E = m/2 = 2.5443 keV, width [1.19, 8.08] eV, the exact b⁻¹ cusp, the UFD-absence switch, the lifetime bound), the free-streaming cut (λ_fs = 0.558 Mpc, the two P(k) faces, the deciding decade k ~ 100–500), the thermodynamic face (isothermal EOS γ = 1, the √2 sound lag, the phantom-first merger clocks, the thermal fixed point), the honest limits (no rate, no coupling, f_b an input with the f_b-invariance of the per-object laws), the testable-predictions table (B10's 17 condensed to the paper's 8 most decisive, each with instrument, date, verbatim falsifier), and the falsifiers (9 named kill conditions with their numbers). Measured section length: 1,668 words of prose (2,175 with the table; target ~1,500 — the voice pass trims the remaining parentheticals without removing a number; see D08_results.json C1). Every number read from a committed register.

### V2 — THE INTEGRATION MAP IS COMPLETE. PASS.
The section slots into the G202 skeleton as **§4.4**, between §4.3 (cluster sector) and §4.5 (force-face), adjacent to the galaxy-sector sections (§4.1–4.2) on one side and the cosmology/closure faces on the other, per the skeleton's own numbering (§4.4 = "The dark sector"); the density-closure headline stays as the section's closing cosmology face. The abstract's particle sentence is revised to the sector's final state (m = 5.09 ± 0.10 keV; the 2.55-keV line; the 0.558-Mpc cut; R(k) = 1), and the revised abstract measures 218 words, inside the 200 ± 10% gate of G221's C1 (108–109% of the original 207-word draft's content window, trimmed from the 244-word first pass). No committed number in §4.1–4.3 or §4.5–4.6 changes.

### V3 — THE HONEST STATEMENT. PASS.
**The paper's particle section is drafted from the closed record** — the mass (5.09 ± 0.10 keV, one coefficient Z = 2√(8π/3) spanning gravity and the particle ladder, environment-blind across every frozen rung, with the never-froze UFD class as the registered breakdown point), the line (2.5443 keV, Doppler width 1.19–8.08 eV, the rate-independent b⁻¹ cusp, present-frozen/absent-never-froze), the cut (λ_fs = 0.558 Mpc as the face that would kill the charge reading; R(k) = 1 as the face the census already leans 3.2–4.1σ toward; the deciding decade k ~ 100–500), the thermodynamic face (isothermal, √2 sound lag, phantom-first merger clocks, thermal fixed point), and the limits stated with their numbers (no rate — a bound, never a value; no coupling or production; f_b = 0.157 the last measured input, halo-anchored at 4%). Nine falsifiers are armed with their kill numbers and the honest complements ride with them (a null line is always consistent; no null in any radiative channel touches the mass). What remains is the author's voice pass: the sentences carry the campaign's register of precision, and the voice pass should set tone and trim the parentheticals — not add or remove claims.

*Deliverable complete. Pass: 3/3 verdicts. D08_results.json written alongside. Commit + push authorized.*