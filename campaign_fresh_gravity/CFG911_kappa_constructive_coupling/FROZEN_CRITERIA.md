# CFG911 FROZEN CRITERIA: κ constructive lane. HYPOTHESIS BUILDING: the minimal π-free couplings of a dynamical ρ_DE that could give κ = ½, and what else each predicts

Written before any script of this lane exists. Committed alone. Block CFG910–919 (orchestrator reservation of 2026-10-20 in
`campaign_fresh_gravity/LEDGER.md`: "CFG911 κ constructive: the minimal π-free c-coupling of a dynamical ρ_DE that would give
κ = ½ and its required second predictions (hypothesis building, not a derivation)"). Rules:
`campaign_fresh_gravity/CFG894_kappa_campaign_ledger/KAPPA_CAMPAIGN_RULES.md`.

**This lane is HYPOTHESIS BUILDING, not a derivation.** It writes down couplings, states what each needs and what else each
predicts. A candidate that "gives ½" here is a conjecture with stated tests. It is a derivation only if it passes every campaign
rule, including the look-elsewhere rule (§8 of the rules), which no single route can pass today without a second prediction.

Standing facts (rules §0). κ = ½ is FITTED: κ_Λ = 0.417 ± 0.095 (ρ_DE footing), κ_crit = 0.345 ± 0.078 (ρ_crit footing),
CFG493. The footings 9.3603e-11 and 1.1312e-10 m/s² are never pooled. Z ≡ κ. No de Sitter–Unruh argument is used or cited for
½. GF2's "κ derived" is the SIS ratio (AUDIT_GF2, a755b66ca). No knob scans: every candidate, variant and convention is listed
below before any computation. Identities are checked by construction. Cold energy is real gravitating mass; no particle species
is added (the dark-energy field φ below is the dark energy itself, not dark matter). Not "theory closed". LEDGER.md,
THEORY_CANONICAL*.md, CFG894's register and every other lane are NOT edited; the register line is returned to the orchestrator.

## 0. What was read before freezing, and the starting point

Read: KAPPA_CAMPAIGN_RULES.md, KAPPA_DOORS.md, CFG894 README; CFG891 README (census: no record equation gives exact ½; the five
π-free halves carry the target; horizon-type values are π-odd; Einstein's 8π is load-bearing); CFG893 (c-free dynamics are
S_λ-invariant, so κ needs c); CFG897 (stiffness-term FRW vacuum: sign, w and size fail); CFG898 (causality saturation: menu of
misses, H-type); CFG900 (Lorentz-invariant nodal medium: no law; κ² = 12π/(σλ³) one-parameter map); CFG905 (Festina Lente:
κ = √2 s𝒩 with 𝒩 free; π-even only for the G-normalised map = premise A); THEORY_CANONICAL_2026-10-14.md S1–S2 and the
2026-10-18 v3; sonnet55_push/puzzle_32pi/p63_a0_field_coupling/FROZEN_CRITERIA.md (pending, not run here);
fable_independent_2026/lean_2026/PUZZLE_32pi_premise_A_2026_10_05.lean (premise A = a G-coupled horizon balance
Gρ·4πr² = 4π with r = c²/2a₀); real_research/reviews/mi_pi_free_area_2026.py header (K433: the π-free horizon area);
register rows K022, K058, K079, K219, K433, K532, K594.

**The starting point (CFG891's sentence).** An exact κ = ½ needs a π-free coupling, through c, of a dynamical ρ_DE that does
not pass through Einstein's 8πG. Two observations shape the family below, both to be checked in sympy:

1. **In energy units the law has no explicit c:** a₀ = κ c √(G ρ_DE) = κ √(G ε_DE) with ε_DE = ρ_DE c². So "a c-coupling" means
   the a₀ sector reads the dark energy's **stress** (energy density, pressure, trace, flux), a relativistic quantity, not its
   mass density. This is how c enters without a horizon.
2. **"π-free outside 8πG" means G appears bare.** Every Gauss-law normalisation (Poisson 4πG, Einstein 8πG, the record's
   K = 4πG, forced by ∇·P = ρ − ρ̄ in CFG723) carries one π per power of G. Since κ² ∝ G¹, κ² is π-free only if (a) G enters
   bare (premise A, here hypothesis H_A), or (b) a geometric 1/π (a solid angle, an area) cancels it.

## 1. Hypotheses (named) and record equations used

- **Record (held):** the law a₀ = κ c√(Gρ_DE), κ FITTED (THEORY_CANONICAL_2026-10-14.md S1). The stiffened action (S2):
  L = −|∇Φ − K P|²/(2K) − ρ_bΦ − W_rem(u) − (γ/2)|∇P|², K = 4πG, u = K|P|, K W_rem′(u) = u²/(a₀ − u), whose closed form
  W_rem = −(a₀/K)[u + a₀ ln(1 − u/a₀)] − u²/(2K) is checked symbolically (K12). The field relation g = a₀u/(a₀ − u) gives the
  simple law g_N = g²/(g + a₀). The portals below change only a₀ → a₀[DE]; the local sector (and so Cassini, CFG770) is untouched.
- **H_P (portal):** a₀ is not a constant but a functional of the dark-energy stress tensor T^DE at the same spacetime point
  (so it reads ρ_DE locally in time: rule S8).
- **H_A (G-normalised portal; premise A as a hypothesis, declared):** the portal uses G, not 4πG or 8πG. Declared openly as
  the hypothesis under test; the question is whether, GIVEN H_A, ½ follows without inserting it.
- **H_φ (dynamical dark energy):** for N6, a canonical scalar φ with ε = ½φ̇²/c² + ½|∇φ|² + V(φ) and an Einstein-normalised
  decay scale φ_P² = c⁴/(8πG), slope λ ≡ φ_P V′/V = O(1).
- Candidate-specific hypotheses are listed with each candidate.

## 2. Inputs, with provenance

- Symbolic: G, c, ε_DE (or ρ_DE), d, the candidates' own coefficients. ħ is not used (I7); N3 checks the one ħ variant.
- **Second predictions only** (never upstream of any κ):
  - DESI DR2 w₀w_a (CPL) for DESI+CMB+{Pantheon+, Union3, DESY5}: parsed at run time from the tracked file
    `fable_independent_2026/L273_desi_a0z_band.py` (the `DESI = {...}` line; verified there against arXiv:2503.14738v2), with
    the w₀–w_a correlations −0.895 / −0.933 / −0.907 and per-combination Ω_m 0.3114 / 0.3275 / 0.3191 quoted in that file's
    docstring (L275 chains). Measured w₀/w_a enter only the second predictions, as the rules allow for converting a finished
    prediction.
  - CFG829's blue-lens amplitudes (canonical and alt footings) read from
    `campaign_fresh_gravity/CFG829_lensing_low_g_vs_dwarf_excess/cfg829_results.json`; lens redshifts bracketed at
    z_l ∈ {0.15, 0.25, 0.35} (the values CFG885 used).
  - The record's Jeanneau deep refit (prep_2026/jeanneau_refit/DATA.md §5): Δb = +0.140 ± 0.272 (honest) at median z = 1.06,
    canonical fork 0.000, a₀∝H fork −0.243. Used report-only, as an approximate mapping Δb ≈ −D log₁₀[a₀(z)/a₀(0)] with
    D = 0.243 / log₁₀E(1.06) (ΛCDM E, Ω_m = 0.3027 as in L273).
  - Report-only magnitudes (N6): H₀ = 67.4 km/s/Mpc, Ω_Λ = 0.685 (the law's unit c√(Gρ_DE) at κ = ½, fitted), Ω_b h² = 0.02221
    (CFG886, BBN D/H), solar, Earth and MW-like (6e10 M_⊙, as CFG893) masses, cluster 1e14 M_⊙.
- **Forbidden (rules §2), checked by grep (I1):** no footing a₀ value, no measured κ, no Z = 5.7888 and no 0.1727 appear in the
  script. The target "ρ_DE c² = 4a₀²/G" is never used as a premise; it appears only as the planted M4 control.

## 3. Footing

Declared **ρ_DE** (the portals read the dark energy's own stress). ρ_crit readings are printed separately (κ_crit = κ√Ω_Λ),
never pooled.

## 4. The candidate family (complete; nothing outside it may be promoted after the run)

For each: the coupling, why it is π-free, its admissible variants (the option space Ω), its free constants, and the second
predictions to compute. "Formal ½" means κ² = ¼ exactly for one admissible variant.

**N0. Premise A as the record states it, written as a coupling.** A second (MOND-sector) metric g̃ whose Einstein equation
couples ε_DE with G̃ instead of G, so its de Sitter radius R̃ obeys (8πG̃/3)ρ_DE R̃² = c²; premise A is G̃ = 3G/(8π)
(⟺ Gρ_DE R̃² = c², the Lean file's balance); a₀ is identified with a surface gravity of that horizon. Variants: surface gravity
c²/(2R̃) (the Schwarzschild form the Lean file uses: r = c²/2a₀) or c²/R̃ (the de Sitter horizon's actual surface gravity).
Free constant: G̃/G. Expected: TRADE in G̃/G; the ½ needs the Schwarzschild form at a non-Schwarzschild horizon (X7, k05 H1).
Second prediction: a horizon at R* = c/√(Gρ_DE) in the a₀ sector's metric; a₀ ∝ √ε_DE(z).

**N1. Premise A as an action term (the multiplier portal).** S ⊃ ∫ λ(x)[a₀(x)² − ξ G ε_DE(x)] with a₀ an auxiliary field read
by W_rem(u; a₀). π-free by H_A. κ² = ξ. Free constant: ξ (record precedent K532/AS070: "imposed not derived"). Second
predictions: a₀(z) = a₀(0)√(ε(z)/ε₀) (κ-free); the running law d ln a₀/d ln a = −(3/2)(1 + w) (sign of ȧ₀ = sign of −(1 + w));
universality (local terms in N6).

**N2. The stress-invariant portals.** The same with ε replaced by another scalar of T^DE, each π-free by H_A:
F_V = (ε − p)/2 (potential; record R16), F_p = −p (pressure; stage-17, K219), F_X = (ε + p)/2 (kinetic), F_T = ε − 3p (trace),
F_act = −(ε + 3p) (active mass). κ² = ξ F/ε at w = −1 = ξ × {1, 1, 0, 4, 2}. Free constant ξ (TRADE). Report-only menu at
ξ = 1: κ ∈ {1, 1, –, 2, √2}. Second predictions (κ-free): the a₀(z) shape a₀ ∝ √F(z) under the three DESI fits at
z ∈ {0.25, 0.5, 1.06, 1.42, 2.0, 2.5} (1.06 = Jeanneau median; 1.42 and 2.0 = the sealed ALMA redshifts; 2.5 = the PAPER7
rotator), with the DESI band (Gaussian, the L275 correlations), and the running d ln a₀/d ln a at z = 0.
- **Kinetic portal, extra:** F_X vanishes at w = −1 and is negative for w < −1. (i) Report the CPL crossing z_c where
  a₀ → 0 for each DESI fit. (ii) A canonical scalar cannot cross w = −1, so evaluate the representative non-crossing thawing
  variant 1 + w = (1 + w₀)a³ (leading-order thawing in the matter era; ε/ε₀ = exp[(1 + w₀)(1 − a³)]) and compare its
  predicted KiDS amplitude A = √(a₀(z_l)/a₀(0)) (deep regime) with CFG829 on both footings, and its Δb at z = 1.06 with the
  Jeanneau refit (report-only).

**N3. A G-free tie through c only.** a₀ = f(ε_DE or ρ_DE, c) with no G. Dimensional analysis (sympy null space): no
dimensionless group exists, so a new dimensional constant ℓ* or M* is needed (TRADE). Variants declared: (a) ℓ* = the dark
energy's own field scale 1/√V″ (brings G back through φ_P: Einstein-normalised → π-odd; G-normalised → H_A, slope free);
(b) the ħ variant ℓ_DE = (ħc/ε)^{1/4}, a₀ = n c²/ℓ_DE (ħ-bearing, wall 3; print its size against the law's unit);
(c) a horizon length c/H (G via Friedmann: H-type, π-odd, and it drifts with H(z): S8).

**N4. Canonical field-strength portal.** One G-normalised field whose vacuum energy is the dark energy, ε_DE = s F², and whose
vacuum field strength sets the saturation scale, a₀ = √G |F|. κ² = 1/s. Variants: s = ½ (canonical) or s = 1. Expected: MENU
{√2, 1}, both misses. The four-form instance is k04/p63 (pending; not re-run here, only checked for consistency: k04's
κ² = 2β²/(Z + 2bβ²) at Z = 1, β = 1, b = 0 gives 2).

**N5. Trace-share portal.** a₀² = G |T^μ_μ[DE]| / N_d with N_d a power of the spacetime dimension. For the vacuum |T| = dε.
Variants (the convention of where the d lands; rules X4): N_d ∈ {d², d, 1} → κ² ∈ {1/d, 1, d} = {¼, 1, 4} at d = 4. Formal ½
for N_d = d² only. Second predictions: κ² = 1/d in general d (S3), and the trace-portal a₀(z) shape (|T| = ε(1 − 3w)) under DESI.

**N6. The dynamical portal (H_φ).** N1/N2 with φ dynamical: a₀(φ)² = ξ G V(φ) and W_rem(u; a₀(φ)) in the action, so the
galaxy's own field sources φ with the "a₀-charge" density q ≡ −a₀ ∂W_rem/∂a₀|_u. κ² = ξ (TRADE). Second predictions computed:
(i) q in the deep and Newtonian limits (symbolic); (ii) the induced local variation δ ln a₀ = (G λ²/2c⁴) ∫ q/|x − x′| d³x′ for
the Sun at 1 AU, the MW at 8 kpc, a 1e14 M_⊙ cluster and the Earth (equivalence-principle scale); (iii) the cosmic back-reaction
⟨q⟩/(2V) on the dark energy's slope (order of magnitude). Compare with the record's environment slope −0.010 ± 0.015
(THEORY_CANONICAL_2026-10-14 S1), Cassini and MICROSCOPE (10⁻¹⁵) scales.

**N7. Areal-horizon portal (record K433; cross-check only).** a₀ = n c²/√A_Λ, A_Λ = 4π(c/H_Λ)², H_Λ² = 8πGρ_DE/3. π-free because
√A carries √(4π). κ² = 2n²/3; natural n = 1 → κ = √(2/3). ½ needs n = √6/4 (K433's √6/8 on a₀/2). General d:
κ² = 16π/((d − 1)(d − 2) Ω_{d−2}^{2/(d−2)}), π-free only for even d. Expected: MISS (record verdict stands).

**N8. Hemispherical-flux (effusion) portal.** The a₀ sector reads the dark energy as an isotropic bath of quanta with speed v,
specific intensity I = εv/(4π) per steradian and one-sided flux Φ₁ = εv/4 (the hemisphere factor ¼ is π-free in 3 space
dimensions). Variants: (a) a₀² = G Φ₁/c (H_A) → κ² = v/4c; (b) a₀² = K I/c (the record's own K = 4πG, no H_A) → κ² = v/c;
(b′) a₀² = K Φ₁/(2πc) (per hemisphere solid angle) → κ² = v/2c; (c) a₀² = K Φ₁/c → κ² = πv/c. At v = c: MENU {¼, 1, ½, π}
in κ²; formal ½ for (a). General d: the hemisphere fraction Γ(n/2)/(2√π Γ((n+1)/2)), n = d − 1 (π-free only for odd n).
Second prediction (all variants): such a bath has w = v²/(3c²) ∈ [0, 1/3] (1/3 at v = c), never negative; and the
Lorentz-invariant vacuum (T^{0i} = 0 in every frame) has Φ₁ = 0, so a₀ = 0. Compare w = 1/3 with the DESI w₀ values.

## 5. Per-candidate grading (frozen, mechanical)

- **SELECTS ½ WITH A SECOND PREDICTION:** κ² = ¼ exactly and determinate (every admissible variant gives ¼, or there is
  only one), π-free, ħ-free, no free constant, no X-class ingredient (rules §3 S7 / KAPPA_DOORS X1–X17) beyond the declared
  H_A, the rename test I4 shows a selection (output stays ½ when κ_law = 2/5), and its second prediction is computed and not
  excluded by existing record data. Even then: a conjecture, scored under §8 of the rules.
- **TRADE:** κ is swapped for a free constant (ξ, G̃/G, ℓ*, n).
- **IDENTITY:** the relation holds for every κ (the output follows κ_law in I4).
- **MENU / MISS:** a discrete set of values (MENU; a ½ inside a menu is spurious, rules §4) or a determinate value ≠ ½ (MISS
  if outside W_data = [0.227, 0.607] on ρ_DE).
- **EXCLUDED:** the construction's own second prediction is excluded by existing record or public data (thresholds in §6), or
  it sits inside an X-class (named).
- A candidate can carry two labels (e.g. MENU + EXCLUDED); the more severe one is its grade.

## 6. Data thresholds for EXCLUDED (frozen)

- Kinetic portal: EXCLUDED by data iff the thawing variant's predicted KiDS amplitude at z_l = 0.25 is more than 3σ below
  CFG829's blue-lens amplitude on BOTH footings. A CPL crossing at z_c is reported as "incompatible with the DESI CPL fits"
  (a conditional exclusion: it holds if the crossing is confirmed), not as a data exclusion.
- N8: EXCLUDED iff w = +1/3 lies more than 5σ above w₀ for all three DESI fits (any w ≥ 0 bath would also need the universe
  not to accelerate).
- N6: a local signature counts as testable only if it reaches 10⁻³ (environment slope precision 0.015, galaxy scale) or
  10⁻¹⁵ (MICROSCOPE, Earth scale); otherwise "silent".
- Portal shapes (N1, N2, N5's trace shape): "testable now" iff two portals differ by more than the record's honest band at
  some redshift where the record has a measurement (Jeanneau ±0.272 dex at z = 1.06); otherwise the separation is reported as a
  future target with the required precision.

## 7. Lane outcome classes (frozen)

- **CONSTRUCTIVE CANDIDATE:** at least one SELECTS ½ WITH A SECOND PREDICTION.
- **½ ONLY IN MENUS OR POSITS:** no determinate ½; ½ appears only as a menu member or through a posit. The second predictions
  of the TRADE couplings are reported as falsifiable targets.
- **NO ½ AT ALL.**

## 8. Identity checks (I1–I8) and controls (all reported in the .out)

- K1 (I1): grep the script for the §2 forbidden constants; fail on any hit.
- K2 (I2): every κ² printed symbolically with its free symbols.
- K3 (I3): G → λG, ε → μν²ε (ρ → μρ, c → νc): a₀ → ν√(λμ)a₀, κ invariant, for every candidate.
- K4 (I4): rename test at κ_law = 2/5 (TRADE outputs follow it; determinate outputs do not and fail the comparison).
- K5 (I5): N0 and N7 use Friedmann; check that their κ holds for every ρ (posit, not data selection).
- K6 (I6): ρ_crit values printed separately.
- K7 (I7): no ħ in any κ² except N3(b), which is reported as ħ-bearing.
- K8 (I8): π-weight of each κ² equals the class declared in §4 (0 for H_A, N7, N8(a)(b)(b′); 1 for N8(c)).
- K9: reproduce L273's density-portal a₀(2.5)/a₀(0) = 0.82 (DESY5) within 0.01.
- K10: CFG829 amplitudes read from JSON equal the README's 1.016 ± 0.086 / 0.928 ± 0.078 within 0.001.
- K11: N7 at κ = ½ gives a₀√A/c² = √6/4 exactly (K433's factor).
- K12: the closed form of W_rem satisfies K W_rem′ = u²/(a₀ − u) and gives g_N = g²/(g + a₀).
- K13: the hemisphere fraction equals ¼ at n = 3 (symbolic integral), 1/π at n = 2.
- K14: three planted classifier rows get their classes: a planted determinate ½ (SELECTS…), a planted ξ row (TRADE), a planted
  menu with ½ (MENU).

## 9. Mutation controls (`CFG911_MUTATE=1`; separate `_MUTATE` outputs; exit 1 when every control bites, 3 if one does not)

- **M1, Einstein coupling 8πG → 4πG** (Friedmann). Expected: N7's κ² moves 2/3 → 1/3, N0's natural values move; the G-bare
  portals (N1, N2, N4, N5, N8(a)) do not move (they never touch Einstein's coupling; that is their point).
- **M2, w = −1 → −0.9** in the κ normalisation. Expected: N2's ξ = 1 menu moves (F/ε = 0.95, 0.9, 0.05, 3.7, 1.7); N5's
  formal value moves (κ² = 3.7/16); N8 does not move (its bath is not the vacuum).
- **M3, d = 4 → 5.** Expected: N5 → κ² = 1/5; N7 and N8(a) become π-bearing (π^{−1/3} and 2/(3π)); N4 unchanged.
- **M4, planted insertion.** N1 with ξ = ¼ written in and labelled "derived": the rename test must class it as following the
  law (insertion/identity), not as a selection.

## 10. Hand expectations (disclosed; the script decides and any disagreement is recorded)

- N0 TRADE (G̃/G = 3/8π is premise A; ½ only with the Schwarzschild form; c²/R̃ gives κ = 1). N1 TRADE. N2 TRADE; at ξ = 1 no ½.
- CPL crossings of the kinetic portal: z_c ≈ 0.354 (Pantheon+), 0.440 (Union3), 0.405 (DESY5). Thawing variant at z_l = 0.25:
  A ≈ 0.85, about 2σ below CFG829 canonical and about 1σ below alt, so NOT excluded by data under §6 (graded TRADE with a
  strong second prediction: a₀ ∝ a^{3/2} into the past, about −0.47 dex at z = 1.06, Δb ≈ +0.44 against +0.140 ± 0.272).
- At z = 1.06 (DESY5) the portals differ: ε +0.000, V ≈ +0.05, −p ≈ +0.10, trace ≈ +0.07, active ≈ +0.16 dex. Spread
  ≤ 0.16 dex < 0.272, so not testable now.
- N3 TRADE; the ħ variant is ħ-bearing and ~10³¹ times the law's unit.
- N4 MENU {√2, 1}, misses. N5 MENU {½, 1, 2} (the ½ is spurious, X4). N7 MISS (√(2/3) = 0.816).
- N6: δ ln a₀ ~ 10⁻²³ λ² (Sun), ~10⁻¹³ λ² (MW), ~10⁻¹⁰ λ² (cluster); Earth ~10⁻²⁹; back-reaction ~10⁻⁸. Silent.
- N8 MENU {½, 1, 1/√2, √π} with w = +1/3 required: EXCLUDED at ≳ 10σ by the DESI w₀ values.
- Lane: **½ ONLY IN MENUS OR POSITS.** The cost of an exact ½ is H_A plus a "4" taken from d = 4 counting (N5, X4), from the
  hemisphere flux of a bath that cannot be dark energy (N8), or from the Schwarzschild form at a horizon that is not
  Schwarzschild (N0, X7).

## 11. Files and resources

`cfg911.py` (sympy + numpy, one process, seconds, < 1 GB, `nice -n 10`, `OMP_NUM_THREADS=1`), `cfg911.out`,
`cfg911_results.json`, `cfg911_MUTATE.out`, `cfg911_results_MUTATE.json`, `README.md`. The script reads only the three
tracked files named in §2. Nothing is downloaded. Commit only this lane's paths; no push.
