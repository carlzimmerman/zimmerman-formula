# CFG172 — Door 11C: a covariant timelike-flow completion of the flowing Λ-vacuum picture. FROZEN CRITERIA (phase 1)

Written 2026-09-29, before any script of this lane. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure. No physics script has been written or run: every number marked "hand" is arithmetic done by hand from record formulas and is itself to be checked in phase 2. Literature facts are **from memory, unverified** unless a record file is cited (and then they are as the record states them, not re-read from the source). κ = ½ is FITTED. Nothing here says the theory is closed, and nothing says any data favour the framework. A scoped no-go is a valid and likely answer.

Addendum 2 of the Door 11 file (the flowing medium has no rest mass and is not a particle; 2026-09-29) was received while this file was being written and is folded in as §9 (dated); §9 adds one admission check and two script/MUTATE items and changes no gate line.

Sources read for this file (all under the repo root): `campaign_fresh_gravity/closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md` (gates G1–G8, variants, rules, addendum 1), `TEN_DOORS_GATES_2026-09-29.md`, `TEN_DOORS_RESULT_2026-09-29.md`, `ACTIONS_AND_NOGOS.md`, `GATES.md` (rows 4.01, 4.02); `campaign_fresh_gravity/CFG44_fluid_target/README.md` and `Bcommon.py` (target, kernels, exponential sphere); `CFG43_fluid_tie/README.md` (a₀–Λ tie); `CFG48_gap1_switch/README.md` (gate-stiffness result, G4 pass lines); `CFG7_hierarchy_fg001.py` (the Q₂ computation of gate 4.01); `real_research/khronon_momentum_2026/` (KM1, KM3); `real_research/g03_audit_2026/L333…py`, `L350…py`; `real_research/chk_v0_2026/README.md`, `CV4…py`; `real_research/dark_energy_2026/DE12…py` and the DE12/DE13 entries of the index notes; `qwen_claude_field_theory/closure_2026/fc_kh_terminal/FC_KH_PAPER_vNEXT.md`; `opus_48_extended_research/reviews/` (Routes 2–4 aether verdicts, AETHER_IDENTIFICATION verdict).

## Forking paths and multiplicity (stated first)

- **The menu is not blind.** Door 11's variant list was written knowing the CFG44 target and the ten-door result (gates file, origin paragraph). The three sub-variants below were chosen after reading the record's exclusions (FC-KH, KM1, CV4, DE12/13); in particular 11C-a is the record's FC-KH/C-H/K aether class with the P2 kernel, and 11C-b/-c are the two ways I could find to let the flow's divergence θ matter. That is a design made with the answer's neighbourhood in view.
- **Hand estimates in §3 were written before any script**; they are kept whatever the scripts show.
- **Gates and pass lines are the orchestrator's** (Door 11 file). Where I had to add a definition (G1 reading, G3 quantities, G5's Q₂ recipe, G7's metric) it is declared in §2 and marked "declared here".

---

## 0. The record's exclusions, addressed first

Notation used below: a_μ = u^ν∇_ν u_μ is the flow's 4-acceleration, θ = ∇_μu^μ its expansion, K the extrinsic curvature trace of the flow's orthogonal slices (K = θ for a hypersurface-orthogonal unit flow), c₁…c₄ the Einstein-aether couplings, c₁₃ = c₁+c₃, c₁₄ = c₁+c₄. In spherical symmetry twist vanishes, so a unit-timelike-vector (aether) and a khronon (u_μ ∝ ∂_μφ) are the same object for every scored configuration here; the spin-1 mode of the general aether is not scored.

### 0.1 FC-KH (exponential khronometric MOND) — APPLIES to the acceleration channel (11C-a, and the a-channel inside 11C-b and 11C-c)

- **What the record found.** `qwen_claude_field_theory/closure_2026/fc_kh_terminal/FC_KH_PAPER_vNEXT.md` (+ `decisive_reduction.py`, `PASS_KILL.md`; index row N6 in `campaign_fresh_gravity/closure_map/ACTIONS_AND_NOGOS.md`): a hypersurface-orthogonal khronometric action S = ∫√−g [R − 2f(a)] (a = |D ln N|, matter minimally coupled, with the β,λ backbone) has, for the exponential kernel μ = 1−e^{−y}, a radial khronon gradient coefficient c²∥ ∝ f″ that is negative on 1 < y ≲ 38, with growth times 5e3–5e4 yr; the β,λ terms enter only the kinetic normalisation. A general statement follows: with q ≡ 1−μ, radial stability is (yq)′ ≥ 0; exact-GR at high a needs yq → 0; with yq ≥ 0 this forces q ≡ 0. Only a slow tail (μ = y/(1+y)) is radially stable, and it leaves an acceleration ≈ a₀ at every g ≫ a₀ (index: "constant ~a₀ tail, ~1e4× over the Solar-System bound"). Flanagan 2023 (arXiv:2302.14846, as cited by the record; not re-read) is the stated source of the stability condition.
- **Does it apply?** Yes, in structure. In spherical symmetry a static aether with an F(a²) term is exactly the FC-KH class, and the P2 kernel of the target is μ(y) = y/(1+y) (hand check: g μ = g_N with g = g_N[½+√(¼+a₀/g_N)] gives g² − g_N g − a₀g_N = 0, i.e. μ = g/(g+a₀)). For this μ, (yq)′ = 1/(1+y)² > 0 (hand): P2 is radially stable but carries the unremovable tail. So the record's pincer becomes, for 11C, a statement about the target kernel itself. **Hand consequence (to be verified in phase 2):** the G1 band (±10% on g) at y_N ≈ 1.5 already forces an anomalous acceleration ≥ ≈0.47 a₀ (max over y_N of 0.9·g_P2 − g_N, hand), and (yq)′ ≥ 0 keeps it ≥ 0.47 a₀ for all larger g, against a gate that needs the tail ≲ 1e-4 a₀ (a₀/R_Saturn = 6.6e-23 s⁻² against 5.2e-27 s⁻²: 1.3e4×, hand).
- **What is unclear / not covered.** (i) The record's identity that β,λ are "free" of the gradient numerator was shown for separate quadratic β,λ terms. In 11C-b a single function F(K) contains both a² and θ² inside one argument, so that identity is not established for it; phase 2 must derive the radial principal coefficient from 11C-b's own action. (ii) The record's escape routes for the tail are a nonlocal filter (a new length ξ — a constant beyond κ and Ω_c h²) or a region gate (0.5, 0.6 below). (iii) Whether the theorem survives a non-spherical or time-dependent configuration is not claimed.

### 0.2 KM1 (khronon momentum; a₀ tracks the CMB-frame speed unless c₂ ≫ 1e-4) — APPLIES to 11C-b and 11C-c; UNCLEAR for 11C-a

- **What the record found.** `real_research/khronon_momentum_2026/KM1_khronon_carries_phantom.py` and (first, fuller) `real_research/g03_audit_2026/L333_c2_channel_carries_the_phantom.py`: in linearised khronometric gravity (c₁₃ = 0, λ = 1+c₂), a moving source's MOND "phantom" is carried by the khronon only through the c₂ (θ²) channel; at c₂ = 0 there is no solution (L330). The price: the aether's own acceleration a_i — the input the MOND sector reads — is distorted by D cos²θ with D = 2w²/(c²c₂) (w = the galaxy's speed through the flow frame); the isotropic part is D/3 (0.11 at c₂ = 2.5e-5, 0.29 at 1e-5 for w = 620 km/s; the record's numbers, reproduced by hand: 2(620/299792)² = 8.55e-6). So either a₀ tracks each galaxy's speed through the CMB frame at 10–30%, or c₂ ≫ 1e-4. Cost: K ~ 6–60 H₀ at r_M is needed to carry the phantom; the aether flow perturbation is 0.5–80 km/s; the nonlinear khronon energy is 8–55% for clusters (outside validity).
- **Does it apply?** The mechanism does: in every 11C variant the flow's acceleration or expansion is what carries the law, so a galaxy moving through the flow's rest frame tilts the foliation. It applies most directly to 11C-b and 11C-c (θ is an active field, c₂ sets its stiffness). For 11C-a the record's derivation used a MOND scalar sitting on top of the aether; in 11C-a the "phantom" is the aether's own a²-channel stress, and at c₂ = 0 the record's own control says there is no solution. So whether D = 2w²/(c²c₂) transfers with the same coefficient to a nonlinear F(a²) sector is **not established**; G7 in §2 re-derives it from each variant's action rather than importing it.
- **Sharp use.** At w = 600 km/s the record's formula gives D/3 ≤ 0.10 iff c₂ ≥ 2.7e-5 and D ≤ 0.10 iff c₂ ≥ 8.0e-5 (hand). This is the G7 line (§2) and it is what 11C-b's Λ-tie collides with (§1.3).

### 0.3 KM3 ("C-H/K 1PN = GR") — DOES NOT APPLY as an exclusion; it is a source of formulas and it is silent about 11C's tail

- **What the record found.** `real_research/khronon_momentum_2026/KM3_chk_one_pn.py`: for the filtered C-H/K construction, γ = β = 1 derived (from the static second-order khronometric equations), α₃ = ζᵢ = ξ = 0 by the action's structure, α₁ = −4α_c, α₂ = α_c(α_c − c₂)/(2c₂) at β = 0 (the fuller Yagi–Blas–Barausse–Yunes expression α₂ = c₁₄(c₁₄ − c₂ + 2c₁₄c₂)/(c₂(2−c₁₄)) is in the L333 script header, as the record quotes it), η_N = (11/3)α_c ≤ 1.2e-8 across L340's window, filtered MOND remainder only at (floor)×U.
- **Does it apply?** As an exclusion, no: it is a positive, scoped result. But its Solar-System safety rests on the **heat filter** (a length ξ; the "filtered remainder"), which none of 11C-a/b/c contains, so KM3 says nothing about 11C's unfiltered tail (§0.1). What it does supply is the formula set for G6: with c₂ ≫ c₁₄ one has α₂ ≈ −c₁₄/2, hence |α₂| ≤ 1.6e-9 gives c₁₄ ≲ 3.2e-9 (hand; matches the record's window α_c ≤ 3.2e-9), and α₁ = −4c₁₄ ≤ 3.4e-5 gives only c₁₄ ≲ 8.5e-6. Also: on the FRW background G_cos/G_N = (2−α_c)/(2+3c₂) (L350), and Planck-era published bounds cap c₂ at 6.3e-4 … 2.9e-3 when the θ² term is not leaf-averaged (L350, as cited from Frusciante & Benetti 2020; not re-read). The leaf-averaged version −c₂(K−⟨K⟩)² removes the cap (L350 G5; a construction, not a derivation).
- **Unclear.** Whether the KM3 static-block derivation of β = 1 holds when the a²-channel is a nonlinear F(a²) that is O(1) in the deep-MOND regime (it was derived for a linear α_c a²). The PPN quantities are evaluated in the Solar System where the local effective c₁₄ is q(y) ≈ 1/y ≲ 1e-6 (hand), but this is an assumption to be checked.

### 0.4 The V0 region-gate obstruction (and CV4: the flow's K is blind) — APPLIES CONDITIONALLY

- **What the record found.** `real_research/chk_v0_2026/README.md` (CV1–CV4) and the V0 entry of the index: V0 is an action for the C-H/K branch whose region gate f = W(U) is an unvaried mask in the data passes; varied as an action term it is obstructed. **CV4** (`CV4_khronon_K_profile.py`, K1–K3): varying the khronon τ in −c₂∫(K−⟨K⟩)² gives c₂D_i(N D^iK) = 0, so a static bound region has K harmonic on each leaf and equal to its Hubble-flow value, K = 3H(z), with |K/3H − 1| < 1e-2 (4.8e-3 in the XR8 summary) and only a dipole for moving sources. A gate on K alone (Ω_Λ(K) = 3Λc²/K²) is therefore **blind**. Its stated scope: linear khronon on a given metric, no matter–K coupling, no non-perturbative "maximal leaf" branch (K ~ 0 inside halos), which "has no source in the linear equation and is not constructed".
- **Does it apply?** CV4 applies directly to 11C-b: there the flow's divergence changes only through gravity, and CV4 says that change is ≲ 1e-4 of 3H. It does **not** apply to 11C-c, whose whole point is an explicit matter–θ coupling (a source for K that CV4 excluded by hypothesis); 11C-c has to be judged on its own (§1.3). The V0 obstruction proper (a region gate as a varied term) applies to any 11C variant that repairs G2 or G5 by adding a gate.
- **Unclear.** The numbers of DE12 (c_gate 1500–3700 km/s against gas 37–117 km/s) are for the MOND-sector reading with the phantom response amplification; they do not transfer to a gate on the flow's θ, so no number from V0 is used as evidence here.

### 0.5 DE12 / DE13 (gate stiffness) — the STRUCTURAL theorem applies to any local smooth gate in 11C; the numbers do not; CFG48 G6 is the counter-case

- **What the record found.** `real_research/dark_energy_2026/DE12_mond_sector_gate_stiffness.py`, `DE13_gate_gradient_repair.py` (+ DE7 T1, CV3, FL2 V5; index N14): a smooth on/off gate flat at both ends has W″ of both signs, so half of every transition layer has the wrong-sign second variation; the instability lands on whatever field the gate reads (a multiplier or the metric → metric k⁴; constrained fields → baryons; K alone → nowhere, but blind). DE13: a gradient repair μ_f|∇f|² has its own background term and no μ stabilises; a μ_U|∇U|² repair costs 32 v_f² at r_F. Rule learned: any localised stiffness coefficient must be convex somewhere, and its own k⁰ term returns; take the exact second variation, never WKB only.
- **Counter-case.** `campaign_fresh_gravity/CFG48_gap1_switch/G6_nonlocal_gate_stiffness.py` (README, "the stability result"): a nonlocal enclosed-mass (Volterra) gate that reads baryon mass has no negative mode on 48/48 layer×width cases, against 4/48 for the local gate; the record's own pre-declared instability hypotheses failed and were kept.
- **Does it apply?** 11C-a contains no gate unless one is added; 11C-b has a "gate" only in the sense that F(K) changes character with K (a local function of the flow's invariants, so the local-gate structure applies and F″ and F′ + 2KF″ signs must be computed); 11C-c couples matter to θ locally, and its second variation lands on the baryons (§1.3; hand result: negative pressure). No nonlocal gate is in the frozen class (that would be a filter: a new length).

### 0.6 GW170817 (c_T = c to 1e-15) — DOES NOT APPLY as an exclusion; it is a structural constraint c₁₃ = 0 that costs nothing in the static scoring

- **What the record found.** `closure_map/GATES.md` row 4.02 ("NS (no action)" for candidate B); L351 (a switch variable killed by GW170817); C-H/K and FC-KH impose β ≲ 1e-15 (c_T² = 1/(1−β)); Route 3 and Route 4 aether verdicts (`opus_48_extended_research/reviews/ROUTE3…`, `ROUTE4…`, not re-read beyond their tables) state that c_T = c forces c₁₃ = 0 in the aether class (Foster–Jacobson: c_T² = 1/(1−c₁₃), from memory).
- **Does it apply?** With c₁₃ = 0 the shear drops out of K identically (K M² = (c₁+c₃)σ² + (c₁+3c₂+c₃)θ²/3 + (c₁−c₃)ω² − c₁₄a² → c₂θ² − c₁₄a² for ω = 0, hand), which is what 11C-a/b/c use. The constraint is therefore built in. Two side notes: (i) in 11C-c only massive baryons couple to θ, so the light cone equals the graviton cone (both from g) and photon/GW speeds agree; (ii) that coupling is a violation of the universality of free fall between baryons and photons/cold dark matter, which affects lensing versus dynamics (a diagnostic, D2 below), not G1–G7.

### 0.7 Other record items that bear on 11C and were not in the list (noted, not used as evidence)

Routes 2–4 (June 2026 aether/foliation lensing-slip verdicts: γ = 1 wall, static aether only renormalises G_N); N7 (v9 AeST PPN kill: α₁ = −2(K_B+2), FC-AeST α₂); N8 (khronon-dust aether identity); N15 (θ-gate mirror lemma: Brown–Schutz dust gate on the baryons' θ_b, every saturated gate has a ghost pole on 24/24 layers; a different variable from the aether's θ, so transfer is unclear). The lensing-slip items concern Φ versus Ψ; G1–G7 do not score lensing, so they enter only as diagnostic D2.

### 0.8 Summary of §0

| exclusion | verdict | scope |
|---|---|---|
| FC-KH | **applies** | 11C-a fully; a-channel of 11C-b, -c; whether it transfers to a single F(K) mixing a² and θ² is unclear |
| KM1 / L333 | **applies (mechanism)**; transfer of D = 2w²/(c²c₂) to a nonlinear a²-channel **unclear** | 11C-b, 11C-c directly; 11C-a unclear |
| KM3 | **does not apply as an exclusion**; supplies α₁, α₂, G_cos/G_N; silent on the unfiltered tail | all |
| V0 region gate + CV4 | **applies conditionally**: CV4 applies to 11C-b (K ≈ 3H inside bound regions); it does not apply to 11C-c (a source is added); V0 obstruction applies to any added gate | b, c; a if a gate is added |
| DE12/DE13 | **structure applies** to local F(K) transition and local θ coupling; numbers do not transfer; CFG48 G6 is a nonlocal counter-case | b, c |
| GW170817 | **does not apply** (c₁₃ = 0 built in) | all |

---

## 1. The exact model class to be scored

### 1.1 Shared conventions (all variants)

- Signature (−+++), c restored where shown. Weak static field: ds² = −(1+2Φ/c²)c²dt² + (1−2Ψ/c²)dx². Unit timelike flow u^μ (Lagrange multiplier λ(u²+1)); a_i = ∂_iΦ/c² for a flow at rest in the static frame; a stationary radial flow has u^r ≠ 0 with u_μ ∝ ∂_μφ, φ = t + χ(r) and δθ = ∇²χ (to leading order).
- **Aether kinetic function** (gEA notation, from memory): K^{ab}_{mn} = c₁g^{ab}g_{mn} + c₂δ^a_mδ^b_n + c₃δ^a_nδ^b_m, K ≡ M⁻²K^{ab}_{mn}∇_au^m∇_bu^n (c₄ absorbed into c₁₄). With **c₁₃ = 0** (GW170817) and ω = 0: **M²K = c₂θ² − c₁₄ a_μa^μ** (hand; matches the khronometric normalisation "K_ijK^ij − (1+c₂)K² + R³ + c₁₄a²").
- **Matter:** baryons only, S_m[g] minimally coupled, except 11C-c. Cold dark matter is not a source in G1 (the gates file: the flow replaces the law's phantom; the CDM double counting inside galaxies is declared not covered, §8).
- **Target for G1** (Door 11 file, CFG44 B1): g_tot = ν(g_N/a₀)g_N with P2 primary, ν_mono reported. Point mass, x = r/r_M, r_M = √(GM/a₀): g_tot = √(g_N²+a₀g_N), y_N = g_N/a₀ = 1/x²; exponential sphere ρ_b = ρ₀e^{−r/h}, h = 2 kpc, M_b(<r) = M[1−(1+s+s²/2)e^{−s}], s = r/h (`Bcommon.py`); for spherical symmetry g_N = GM_b(<r)/r² and the target is ν(g_N/a₀)g_N(r), equivalent to CFG44's C(r) = ρ_c r³g_tot = (a₀/4π)M_b(<r) for P2. Footings: a₀ = 9.3603e-11 (canonical) and 1.1312e-10 m/s²; G = 4.30091727e-6 kpc (km/s)²/M☉; c = 299792.458 km/s.

### 1.2 The Λ-tie rule (stated once, used by every variant)

- **Rule T.** The only dimensionful inputs to the flow sector are Λ (the action's own cosmological constant, ρ_Λ = Λc⁴/8πG) and G, c. a₀ ≡ κc√(Gρ_Λ) = κc²√(Λ/8π), so the *invariant* a_μa^μ has the scale a_*² ≡ (a₀/c²)² = κ²Λ/8π (units m⁻²), and the flow's expansion has the de Sitter scale θ_Λ² ≡ 3Λc² (the value of θ on the attractor). Every dimensionful scale in F, in the matter coupling and in the a₀ formula is one of these two; nothing else with units may enter.
- **Constants allowed:** κ = ½ (FITTED) and Ω_c h² = 0.1200 (FITTED, as in ΛCDM; enters only G2, and ρ_c/ρ_b = 0.1200/0.02237 as in CFG44). **Everything dimensionless that the flow sector still needs (c₂, β, shape of a function) is logged in a constants ledger (§1.3 per variant) and counted twice: strict (each is a G4 failure unless tied to κ or Λ in the same action) and "inert-window" (declared here: a coefficient is not counted if every gate verdict is unchanged when it is varied through its allowed window). Both counts are reported; the orchestrator's G4 is the strict one.**
- **How the tie is realised.** Λ is made a global integration constant (Henneaux–Teitelboim-type unimodular multiplier, XR20 T1 in the record: "TIED, not derived"); κ is written in, not derived (κ underivable: `ACTIONS_AND_NOGOS.md` N19). So the a₀–Λ tie is a **rule**, not a consequence, in all three variants. The same is true of the fitted κ = ½.
- **Function shapes are declared, not derived.** F_a (the a²-function) is set to the P2 kernel: with q ≡ 1−μ, μ = y/(1+y), y = |∇Φ|/a₀, the static Lagrangian term is (a₀²/8πG)·𝒬(y), 𝒬(y) = 2[y − ln(1+y)] (hand: with s = y², d𝒬/ds = q(y) = 1/(1+y), so μ = 1 − q; for y → 0, 𝒬 ≈ y² − (2/3)y³, whose y² part cancels the Newtonian term and leaves the cubic deep-MOND term). ν_mono is reported as a second declared shape. **Menu written knowing the target: shape = the target's kernel.**

### 1.3 The three sub-variants

For each: action, reduction, what solves for what, constants ledger.

**11C-a — acceleration channel: the aether carries the law through its 4-acceleration; θ is passive (the record's FC-KH / C-H/K aether class with the P2 kernel and Λ-tied scale).**

- Action: S_a = (1/16πG)∫√−g [R − 2Λ + 𝔉_a(a_μa^μ) − c₂(θ−⟨θ⟩)²] + λ(u²+1) + S_m[g], with 𝔉_a chosen so that its static reduction has q(y) = 1/(1+y) and scale a_*² of rule T; ⟨θ⟩ the leaf average (L350 G5).
- Static spherical reduction (hand; to be re-derived symbolically): per unit 1/8πG, L = |∇Ψ|² − 2∇Φ·∇Ψ + a₀²𝒬(|∇Φ|/a₀) − 8πGρΦ. The Ψ-equation gives Ψ = Φ (γ = 1); the Φ-equation gives ∇·[μ(|∇Φ|/a₀)∇Φ] = 4πGρ, i.e. in spherical symmetry the algebraic law μ g = g_N(r). Unknowns: Φ, Ψ (and the flow, which is at rest: a_i = ∂_iΦ/c² is then a kinematic identity, not a solution). **What solves for what:** the field equations (Einstein + flow/khronon equation) determine Φ, Ψ from ρ_b; the flow's spatial equation must be checked as an independent constraint (it is a consequence of the Bianchi identity only when the flow is on shell); its second variation gives the radial and tangential stability of the flow about the solution.
- **Reading of "flow acceleration" (declared here).** For a flow at rest the aether's 4-acceleration equals the static observers' acceleration by definition, so "flow acceleration = g_tot" would be vacuous. G1 is therefore scored on the acceleration of baryons, −∇Φ, from the solved field equations. The literal river reading (v∂_r v with v the flow speed relative to the static frame) is scored as a *diagnostic* (§2, G1-river) and is zero here: 11C-a has no flow in the river sense.
- Constants ledger: c₂ (stiffness of the θ-sector; window from G7 ≥ 2.7e-5 and, if not leaf-averaged, Planck ceiling 6.3e-4–2.9e-3 [record]); the shape of 𝔉_a (declared P2); c₁₃ = 0 (structural). Strict count: 1 (c₂). Inert-window: to be tested.

**11C-b — single-function generalized Einstein-aether: one F(K) carries both the acceleration and the flow's expansion; the flow's divergence changes only through gravity.** (Nearest published relative, from memory: Zlosnik–Ferreira–Starkman, PRD 75, 044017 (2007), astro-ph/0607411; Skordis–Zlosnik PRL 127, 161302 (2021) is the scalar-plus-vector successor, not scored here.)

- Action: S_b = (1/16πG)∫√−g [R − 2Λ + M²F(K)] + λ(u²+1) + S_m[g], K = (c₂θ² − c₁₄a_μa^μ)/M², F(K) = −K + (nonlinear part) with the nonlinear part's shape set by requiring q(y) = 1/(1+y) at fixed θ.
- **Λ-tie in this action (rule T made concrete):** M² ≡ 3c₂Λc² (K equals 1 on the de Sitter attractor, where θ = θ_Λ, a = 0), and the MOND transition sits where the a-term balances the θ-term: c₁₄a_*² = c₂θ² ⇒ a_* = √(c₂/c₁₄)·cθ. Requiring a_* = a₀ at θ_Λ gives **c₁₄/c₂ = 24π/κ² = 301.6 (hand)**; requiring it at the *actual* θ = 3H₀ gives **c₁₄/c₂ = 24π/(Ω_Λκ²) = 440 (hand, Ω_Λ = 0.6847)**. Since the actual flow in the cosmic web has θ = 3H(z), the transition acceleration a_*(z) = 3cH(z)√(c₂/c₁₄) tracks H(z): this variant, unless θ inside galaxies differs from 3H (CV4 says it does not, 1e-4), realises the *rival* law a₀ ∝ H(z), not the flat one (diagnostic D1; it is not a G-gate).
- Static spherical reduction: as 11C-a for the a-part, with the operating-point shift K_bg = 9c₂H²/(c²M²) in the argument of F: F is evaluated at K = K_bg − c₁₄a²/(c²M²)·(units), so the MOND branch of F is reached only where c₁₄a² ≳ c₂θ_bg². **What solves for what:** Φ, Ψ, and δθ (the flow potential χ from the flow's constraint Π ≡ ∂L/∂θ = const on the leaf; for c₂ ≠ 0 this is the CMC condition K = 3H(1+O(Φ/c²)); hand estimate δθ/(3H) ~ |Φ|/c² ~ 1e-6…1e-4 — CV4 says ≲ 1e-2 and typically 1e-4). Background: G_cos/G_N = (2−c₁₄)/(2+3c₂) at F′ = 1 (L350 formula).
- Constants ledger: c₂ and c₁₄ (ratio fixed by rule T: 301.6, overall size free), the shape of F (declared P2), c₁₃ = 0. Strict count: 1 (the overall size of c₂) plus the declared function. Inert-window: to be tested.

**11C-c — matter compacts the flow: an explicit matter–θ coupling, with θ slaved to the local density.** Two sub-cases: 11C-c(lin) linear coupling; 11C-c(sat) saturating coupling h(s) = s/(1+|s|) (declared; the generous version).

- Action: S_c = S_a + ∫√−g (−ρ_b c²)[ β h((θ−⟨θ⟩)/θ_Λ) ] (baryon dust whose effective mass depends on the flow's expansion; θ_Λ from rule T), with the same 𝔉_a and c₂ as 11C-a. β is a dimensionless coupling.
- **What solves for what (hand):** the flow's equation for static matter is ∇Π = 0 with Π = ∂L/∂θ; for the linear case (c₂/8πG)δθ + βρc²/θ_Λ = Π₀, so **δθ = −(8πGβc²/(c₂θ_Λ))(ρ − ρ̄)**: the compaction is locally slaved to the density (a *local algebraic* response, no gradient). The flow field v = ∇χ with ∇²χ = δθ is long-range (a Coulomb-like flow ∝ M_b(<r)/r²) but its θ vanishes outside the baryons. The force on baryons is a **contact force** −(βc²/θ_Λ)∇δθ ∝ ∇ρ.
- **Hand results (to be verified in phase 2):** (i) integrating out δθ gives an interaction energy density −(K_c/2)ρ² with K_c = 8πGβ²c⁴/(c₂θ_Λ²), i.e. pressure P = −K_cρ²/2 and **c_s² = −K_cρ < 0 for c₂ > 0** (a gradient instability; c₂ < 0 is a khronon ghost): a stability pincer independent of the size of β. (ii) The far field: outside the baryons ρ = ρ̄, so the θ-mediated force vanishes; the flow's momentum flux ∝ (∂v)² ∝ (M_b/r³)² ∝ r⁻⁶ cannot supply a 1/r phantom. (iii) Any force linear in M_b cannot reproduce a target whose scale r_M ∝ M^{1/2} (Door 1's binding failure, a √1000 spread over 10⁹–10¹²). (iv) A nonlinear saturating h changes the scale to a density scale (ρ ~ ρ_Λ), which gives radii ∝ M^{1/3} (Door 6/8's failure mode).
- Constants ledger: β (free, counts strictly), c₂, shape of h (declared), 𝔉_a shape (declared P2). Strict count: 2.

**Reference controls, not scored as variants:** (i) the K-only Λ-gate of the record (CV4; equals 11C-b's channel without a matter source); (ii) AeST-type vector-plus-scalar (Skordis–Zlosnik; record rows N7, N8); (iii) projectable Hořava with N = N(t): a_i ≡ 0 and there is no local Newtonian potential from N in the static limit (from memory: Mukohyama-type "dark matter as an integration constant" is the known feature of that class), so it fails the Newtonian end of G1 by construction; not scored, recorded so the menu is honest.

### 1.4 The pass structure of G1 (declared here)

G1 has two parts, reported separately per variant:
- **G1-law:** the solved g_tot(r) from the variant's field equations is within 10% of the target over x ∈ [0.1, 30], for M_b = 10⁹ … 10¹² M☉ (seven log-spaced masses), point mass and the h = 2 kpc exponential sphere, with the same constants at every mass, on both footings, P2 primary (ν_mono reported). Pass line: max over (x, M, profile) of |g/g_target − 1| ≤ 0.10.
- **G1-mechanism:** graded M0 (a profile or flow is prescribed: FAIL), M1 (**declared kernel**: an action contains a free function fixed to the target's kernel and the field equations then produce the law: reported "P-declared"; this is a restatement of the kernel choice, not a derivation of ν, and it is **not** a "pass as a mechanism" in the sense of the orchestrator's rule, but I request an independent re-derivation of the field equations because a P-declared pass is a G1-law pass), M2 (**derived kernel**: the kernel emerges from the action's structure with only the rule-T constants; only this is a pass as a mechanism).
- G1-river (diagnostic): v∂_r v for the solved stationary flow, and the identity g_flow = g_tot it would need.

---

## 2. Scoring of G1–G7 (pass lines from the Door 11 file) and tools

Common numerics: numpy/scipy for profiles and root-finds (no tuned constants; nothing is scanned to make a gate pass); sympy for every analytic step (field equations from the Lagrangian by Euler–Lagrange, principal symbols, second variations). Each script reproduces its controls (§4) before it scores.

| gate | pass line | how it is scored | tools |
|---|---|---|---|
| **G1 law** | max |g/g_target − 1| ≤ 0.10 over x ∈ [0.1, 30], M_b = 1e9–1e12 M☉ (7 masses), point mass and exponential sphere h = 2 kpc, same constants at every mass; both footings | solve each variant's static spherical field equations (11C-a, -b: μ g = g_N with the operating point; -c: with the contact force and δθ response); compare with P2 (and ν_mono) | sympy (Euler–Lagrange), numpy/scipy (brentq on the algebraic law, ODE for the exponential sphere) |
| **G1 mechanism** | M2 for a pass as mechanism; M1 = P-declared; M0 = FAIL | inspect which functions are declared and whether the kernel follows from rule T | sympy |
| **G2 growth** | linear growth within 5% of ΛCDM to k = 30 /Mpc (also reported per h/Mpc); CMB unchanged; state the perturbation equations or state UNDEFINED | sub-horizon quasi-static equations for each variant; effective G_eff(k, z, δ); ΛCDM reference (h = 0.6736, Ω_m = 0.3153, Ω_b h² = 0.02237, Ω_c h² = 0.1200, from memory unverified); table over k ∈ {0.1, 0.3, 1, 3, 10, 30}/Mpc and z ∈ {0, 0.5, 1, 2, 3, 10, 30, 1000}; pass iff |G_eff/G − 1| ≤ 5% everywhere (growth ODE solved for the ratio). **Declared:** around FRW the a-channel has μ(y→0) → 0, so the quadratic action for Φ vanishes (strong coupling) and "linear growth" is ill-defined; G2 for 11C-a/-b is then scored by the nonlinear quasi-static estimate ν(y_lin) with y_lin = (3/2)Ω_mH²δ/(k a₀) (hand: y_lin ≈ 2.5e-5δ at k = 30/Mpc and ≈ 8e-3δ at 0.1/Mpc, δ ≲ 1), and the CMB part is UNDEFINED (no Boltzmann treatment) | numpy/scipy (growth ODE), sympy (quasi-static reduction) |
| **G3 reaction and energy** | reaction ≤ 0.10 g_law for x ∈ [0.3, 30]; energy the flow sector stores inside r_e ≤ ½M_bV_f², V_f² = √(GM_ba₀), in both r_ta conventions (CFG48 G4: this lane's and CFG4's, whose r_ta differ by 1.7–3.6×); the origin of the "boost" energy stated | reaction = any force on baryons beyond −∇Φ from the flow's own field equations (zero by construction for 11C-a/-b; the contact force for 11C-c), divided by g_law; energy = canonical (Noether) energy of the flow sector integrated to r_e from the solved fields; conventions imported read-only from `CFG48_gap1_switch/G4_exchange_action.py` and `Gcommon.py`; if the definition is unclear it is stated and disclosed, not guessed | sympy (T^{00}), numpy (quadrature) |
| **G4 constants** | no constant beyond κ, Ω_c h²; scale tied by rule T | the ledgers of §1.3, strict and inert-window counts, and an explicit re-tie check (vary each ledger constant through its window and see which gate verdicts move) | numpy |
| **G5 stability, Q₂, Cassini** | no ghost, no gradient instability, hyperbolic, causal by **criterion B** (no signal backward in a global time function compatible with every characteristic cone; criterion A also reported); Q₂ ≤ 5.2e-27 s⁻² (2σ, gate 4.01); γ−1 ∈ (2.1 ± 2.3)e-5 (2σ) | (i) second variation about the static solution: kinetic signs, radial and tangential gradient coefficients, characteristic speeds (control: reproduce FC-KH's exponential result (yq)′ = (1−y)e^{−y} < 0 for y > 1 before scoring P2, where (yq)′ = 1/(1+y)²); for 11C-c the sign of c_s² = −K_cρ; (ii) **Q₂ computed as CFG7 H1 does** (tide = max(|dg_ph/dR|, g_ph/R)): (a) the flow's anomalous field of the Sun at Saturn's orbit (isolated, no EFE), (b) the Milky Way's flow-tide at the Sun (`CFG7_hierarchy_fg001.py` H1 gives 4.0–5.7× the ceiling for the strict P2/ν_mono law, gate 4.01 text); EFE not modelled; (iii) γ = 1 from the Ψ-equation (Ψ = Φ) | sympy (second variation, principal symbol), numpy |
| **G6 preferred frame** | |α₁| ≤ 3.4e-5, |α₂| ≤ 1.6e-9 (commonly quoted, Shao & Wex 2012; Shao et al. 2013; **from memory, unverified; the data chat verifies before scoring**) | α₁ = −4c₁₄^eff, α₂ = c₁₄(c₁₄ − c₂ + 2c₁₄c₂)/(c₂(2−c₁₄)) (Yagi et al. 2014 as the L333 header quotes it), with c₁₄^eff the F-dressed local value at the test system's own acceleration (q(y) for the P2 a-channel; Solar System y ~ 1e6–1e8, pulsar systems y ≫ 1) — declared here; reproduce the record's α₁, α₂ formulas as controls first | sympy, numpy |
| **G7 a₀ vs frame speed** | a₀ changes by ≤ 10% for w = 0–600 km/s w.r.t. the flow's rest frame | re-derive KM1's moving-source solution for each variant's linearised action (KM1 pipeline for the c₂/c₁₄ structure; the record's D/3 numbers as control), do not import D = 2w²/(c²c₂); isotropic part D/3 and tilt amplitude both ≤ 0.10 (declared: the isotropic part is the primary metric; the larger D reported) | sympy (KM1-style Fourier solve), numpy |

Diagnostics, reported and **not** gates: **D1** flat versus ∝ H(z) a₀ law (evaluate a_*(z) from each variant at z = 0, 1, 2.5, 5; the distinctive law is flat, the rival ∝ H(z)); **D2** lensing versus dynamics (Φ, Ψ, slip; not scored by G1–G7); **D3** G1-river (§1.4).

---

## 3. Hand ESTIMATES of the outcome (written before any script; kept whatever the scripts show)

Probabilities are my subjective estimates for the verdict each script will record. F = fail, P = pass, U = undefined, "P-decl" = pass with a declared kernel.

| gate | 11C-a | 11C-b | 11C-c(lin) / (sat) |
|---|---|---|---|
| G1 law | P 0.95 (algebraic; declared kernel) | F 0.8 (no point in the G6∧G7-allowed region passes; see below) | F 0.97 / F 0.93 |
| G1 mechanism | P-decl 0.93, M2 0.02 | P-decl 0.5, M2 0.02, else F | F 0.9 (no kernel emerges) |
| G2 | F 0.75, U 0.23, P 0.02 | F 0.35, P 0.30, U 0.35 | F 0.4, U 0.5 |
| G3 | reaction P 0.9; energy uncertain (F 0.4) | same as a | reaction F 0.6 (contact force ∼ law inside baryons); energy F 0.5 |
| G4 strict | F 0.9 (c₂) | F 0.9 | F 0.98 (β, c₂) |
| G4 inert-window | P 0.5 | F 0.7 | F 0.9 |
| G5 | **F 0.9** (tail ≥ ~0.47 a₀ ⇒ Q₂ ≳ 6e3× the bound, from (yq)′ ≥ 0 and G1's band) | F 0.75 (tail plus F-function stability) | F 0.85 (c_s² = −K_cρ) |
| G6 | P 0.6 | F 0.7 (the tie forces c₁₄/c₂ ~ 300 while α₂ needs c₁₄ ≲ 3e-9 ⇒ c₂ ≲ 1e-11 …) | P 0.6 |
| G7 | U 0.45 (P 0.3, F 0.25) | F 0.85 (c₂ ≲ 3e-8 vs c₂ ≥ 2.7e-5) | U 0.5 |

**Expected binding gate per variant.** 11C-a: G5 (isolated-Sun tail via the (yq)′ pincer), with G2. 11C-b: the G1 × G6/G7 pincer through the tie: G6 (α₂) needs c₁₄ ≲ 3.2e-9 and G7 needs c₂ ≳ 2.7e-5, i.e. c₂/c₁₄ ≳ 8.3e3 (hand), whereas the a₀-at-the-right-place tie needs c₂/c₁₄ = 1/301.6 (Λ-tie) or 1/440 (actual θ = 3H₀); at c₂/c₁₄ = 8.3e3 the MOND transition sits at a_* = a₀ √(8.3e3/2.27e-3) ≈ 1.9e3 a₀ (hand; 2.27e-3 = (a₀/3cH₀)² at H₀ = 67.4 km/s/Mpc, from memory), so the rotation-curve law is off by orders of magnitude at G1. The escape (θ inside galaxies smaller than 3H) is what CV4 says does not happen. 11C-c: G1 (locality, linearity) and G5 (negative pressure).

**Overall.** P(scoped no-go for all three variants) ≈ 0.90. P(any variant passes G1-law and G5 and G6 and G7 with only rule-T constants) ≈ 0.02. P(any variant passes G1 as a derived mechanism, M2) ≈ 0.01. If a variant surprises, the surprise is kept and independently re-derived (§7).

**Assumptions these estimates rest on (each unverified until phase 2):** KM1's D formula transfers to the 11C actions; the Yagi et al. α₂ expression is right as quoted; the FC-KH (yq)′ identity holds for F(K) mixing a² and θ²; my identification of the MOND transition at c₁₄a² = c₂θ²; the sign of c_s² in 11C-c.

---

## 4. Controls

**Reproduction controls (must pass in the main run; a failure is kept, disclosed, exit 1):**
- C1 CFG44 identities at the P2 point mass: M_c = M(√(1+x²)−1), g = √(g_N²+a₀g_N), and the extended-profile target from `Bcommon.py` (read-only import), to 1e-6.
- C2 FC-KH: for μ = 1−e^{−y}, (yq)′ = (1−y)e^{−y} < 0 for y > 1 and the ordering "static Hessian W″ > 0 but W″ > 1" (stable statically, unstable dynamically); for μ = y/(1+y), (yq)′ = 1/(1+y)² > 0.
- C3 KM1/L333 numbers: D/3 = 0.114 (c₂ = 2.5e-5) and 0.285 (c₂ = 1e-5) at w = 620 km/s; α₁ = −4c₁₄; the α₂ formula.
- C4 L350: G_cos/G_N = (2−c₁₄)/(2+3c₂).
- C5 Q₂ recipe: CFG7 H1 Milky-Way strict-law ratio 4.0–5.7 reproduced from the same baryon budget.
- C6 (positive control of the pass logic) a **prescribed flow** v(r) = √(2∫g dr) with g the target: G1-law passes, G1-mechanism must be graded M0.

**MUTATE controls (each flips a load-bearing cell; `MUTATE=<name>`; the control must make its named claim fail and the script exit 1; outputs are named by mode):**
- **M1 drop the Λ-tie:** scale a_* multiplied by 3 (a₀ → 3a₀ in the flow sector, target unchanged). G1-law must flip to F; in 11C-b the c₁₄/c₂ tie is broken at the same time and G6/G7 no longer bind (shows the tie is the coupling between them).
- **M2 replace the kernel by GR:** F → linear (μ ≡ 1, q ≡ 0). G1-law must flip to F (g = g_N deviates by √(1+x²) at large x); G5's Q₂ must flip to P (the tail vanishes): the pincer's two ends move in opposite directions.
- **M3 flip the sign of the coupling:** 11C-a/-b: q → −q (μ > 1); 11C-c: c₂ → −c₂ (the khronon sector becomes a ghost). G5 must flip (the stability cell) and, for q → −q, G1-law must fail.
- **M4 decouple the aether:** β = 0 in 11C-c (and c₂ → ∞ in 11C-b: no response of θ). δθ ≡ 0 and the contact force vanishes; G1-law must flip to F at every x (and the "compaction" diagnostic must read zero).
- **M5 raise the boost:** w = 3000 km/s (5×), G7 must flip to F for the variants that passed at 600 km/s.
- **M6 change the operating point:** 11C-b with c₂ → 0.01 c₂ (ratio tie kept): the transition moves to a_* → 0.1 a_* and G1 must respond in the direction predicted (shows the H-tracking is load-bearing).

- **M7 give the flow a charge (§9):** khronon form with a nonzero background Noether charge Q. The admission check S2 (no conserved particle number) must flip to F, and the FRW background must acquire the a⁻³ term.
- **M8 cold component switched on in the no-cold run (§9):** with Ω_c h² = 0.1200 restored, the G2 (no-cold) row must recover the ΛCDM growth, which shows the test discriminates.

---

## 5. Declared choices and where the menu was written knowing the target

1. F_a is the target's kernel (P2; ν_mono reported): the menu was written knowing the target. Any pass in G1-law is therefore a restatement unless the kernel is derived (M2).
2. c₁₃ = 0 (GW170817), leaf-averaged θ-term in 11C-a/c (so the Planck ceiling on c₂ is lifted; L350's construction), unaveraged in 11C-b (Planck ceiling 6.3e-4–2.9e-3 applies; record numbers).
3. Rule T (a_*² = κ²Λ/8π, θ_Λ² = 3Λc², M² = 3c₂Λc² in 11C-b) is my choice of realising the tie; another rule would give a different c₁₄/c₂ ratio. The 301.6 versus 440 distinction (θ_Λ versus actual 3H₀) is reported, not chosen between.
4. Inert-window rule for G4 (declared here; the strict count is reported alongside).
5. G1-river as a diagnostic, and "acceleration of baryons" as the operative G1 reading (the literal flow-acceleration reading is vacuous for a flow at rest).
6. The transfer of KM1's D to each 11C action is re-derived, not imported; the record's D/3 is used only as control C3.
7. Q₂ computed as CFG7 H1 (tide = max(|dg/dR|, g/R)), isolated Sun and MW tide, no EFE.
8. G2 for a-channel variants uses a nonlinear quasi-static estimate because the linear theory is strongly coupled (μ → 0).
9. Hand estimates (§3) and hand arithmetic (§0, §1.3) are unverified until phase 2.

---

## 6. Script plan

Names (in the lane directory `campaign_fresh_gravity/CFG172_door11C/`, to be created by the orchestrator at commit; in phase 2 scripts are written in the scratch dir first). Repo root found from `ZF_REPO` or by walking up from `__file__`; every printed path is `<repo>/…`; no absolute home path is ever printed or stored. Each script < 15 min; numpy/scipy/sympy only. Exit convention: **main run exits 0 if all reproduction controls and internal identities pass (gate verdicts F or P are results, not exit codes); a control failure exits 1 and is kept; `MUTATE=<name>` exits 1 when the control bites (the claim it targets fails as required) and writes `*_MUTATE_<name>.out/.json`; if a MUTATE run does not bite that is a declared control failure.**

| script | content | gates |
|---|---|---|
| `cfg172_common.py` | constants (both footings), P2 / ν_mono kernels, CFG44 target (read-only import of `Bcommon.py`), exponential sphere, rule-T scales, repo-root helper | — |
| `CFG172_A1_static_reductions.py` | sympy: weak-field Lagrangian, Euler–Lagrange for a, b, c; reductions of §1.3; controls C1, C4 | G1 law, G1 mech |
| `CFG172_A2_stability_pincer.py` | sympy: second variation and principal symbols, (yq)′ theorem for a and for the F(K) of b, c_s² of c; C2; tail and Q₂ (isolated Sun, MW tide; C5); γ | G5 |
| `CFG172_A3_ppn_frame.py` | α₁, α₂ (with the F-dressed effective c₁₄), G_cos/G_N; the (c₂, c₁₄) allowed-region map; KM1-style moving-source solve for each action; C3 | G6, G7 |
| `CFG172_A4_growth.py` | quasi-static G_eff(k, z, δ) tables for a, b, c; growth ODE; states UNDEFINED where it is | G2 |
| `CFG172_A5_reaction_energy.py` | contact force reaction, canonical energy of the flow sector in both r_ta conventions (CFG48 read-only), energy-source statement | G3 |
| `CFG172_A6_b_operating_point.py` | 11C-b: K_bg(z), a_*(z), the tie pincer (c₁₄/c₂ = 301.6 / 440 versus ≥ 8.3e3), D1 | G1(b), G4, D1 |
| `CFG172_A7_c_response.py` | 11C-c: δθ(ρ), flow v(r), contact force, linearity test across masses, saturating variant, far-field falloff, c_s² | G1(c), G5(c) |
| `CFG172_A8_stress_energy.py` | §9: the flow sector's stress-energy tensor per variant (sympy, from the action), conservation, rest-mass / particle-number / khronon-charge checks, the cold-component-off labelled run | S1, S2, G2(no-cold) |
| `CFG172_verdict.py` | reads the JSONs, prints the table G1–G7 per variant and the diagnostics; no physics | — |

Each numbered script has its own MUTATE modes from §4 (A1: M1, M2, M4; A2: M2, M3; A3: M5; A6: M1, M6; A7: M3, M4; A8: M7, M8).

---

## 7. What counts as a pass of G1 as a mechanism; what a scoped no-go looks like

- **Pass of G1 as a mechanism (M2):** the field equations of an action containing only the rule-T scales, κ and Ω_c h², with no declared function shape beyond what a stated symmetry fixes, produce g_tot within 10% of the target across the whole G1 grid, and the derivation of the kernel is written out (which term gives q(y) = 1/(1+y) or ν_mono). It must also not be a prescribed flow (C6 shows the harness recognises that). **In that case an independent re-derivation is required before anything is reported**, and the pass is stated with the gates that still fail. A P-declared result (M1) gets an independent re-derivation of the field equations, no mechanism claim.
- **A scoped no-go looks like:** "within the frozen class (S_a, S_b, S_c(lin/sat); static spherical weak field; c₁₃ = 0; P2 or ν_mono declared kernels; rule T), no parameter point satisfies G1-law together with G5 (11C-a), together with G6 and G7 (11C-b), or at all (11C-c)", with the exact hypotheses listed and the binding gate named. Nothing here would say the theory is closed, that the timelike-flow reading is refuted outside the class, or that any data favour the framework.

## 8. What is NOT covered

Non-spherical baryons (discs; the exponential sphere is 3D spherical); relativistic or strong-field regimes beyond the weak-field static limit; the aether's spin-1 (twist) mode and the general Einstein-aether with c₁₃ ≠ 0; nonlinear cosmology, clusters, mergers, time-dependent solutions and the flow's nonlinear regime (KM1: 8–55% for clusters); Boltzmann-code CMB (G2's CMB part is UNDEFINED); the external-field effect in the Solar System and in galaxies; CDM (Ω_c h² = 0.1200) coexisting with a flow-generated phantom inside galaxies (the "double counting" of the record, N13/L363; G1 is scored with baryons only as the source); lensing (only diagnostic D2); AeST-type vector-scalar models; nonlocal or heat-filtered variants (they add a length ξ, a constant beyond κ and Ω_c h²); projectable Hořava (recorded, not scored); quantum, UV completion, and any modified-inertia reading. Literature statements (Zlosnik–Ferreira–Starkman, Skordis–Zlosnik, Blanchet–Skordis, Foster–Jacobson, Yagi et al., Mukohyama, Shao–Wex, Flanagan) are from memory or as the record cites them, and none was re-read.

---

## 9. Addendum 2 (dated 2026-09-29; folded in before phase 1 closed): the flowing medium has no rest mass and is not a particle

The owner's clarification (Door 11 file, addendum 2): the medium has no mass and is not a particle; the extra gravity is an effect of the flow itself; "no mass" is read as no rest mass and no particle content (as for a field or the cosmological constant), not as no energy; each variant states its stress-energy; the cold component (Ω_c h² ≈ 0.12) is not supplied by a massless flow unless a variant passes G2 without it.

### 9.1 The flow sector's stress-energy tensor, per sub-variant

**Definition.** T^{flow}_{ab} ≡ −(2/√−g) δS_flow/δg^{ab}, so that the field equations read G_ab + Λg_ab = 8πG T^{(b)}_ab + T^{flow}_ab (with the flow action normalised as in §1.3). Signs and factors below are the structure I expect from the standard Einstein-aether stress tensor (Jacobson and collaborators; from memory) with c_i → c_iF′(K); **phase 2 derives every term with sympy from the action and checks (i) reduction to the standard aether at F = −K, (ii) ∇_aT^{ab}_{flow} = 0 on the flow's equation of motion.**

*Aether form (11C-a, 11C-b, and the flow sector of 11C-c).* Let 𝒥^a{}_m ≡ F′(K) K^{ab}{}_{mn}∇_bu^n (for 11C-a, F′ is replaced by the derivative of 𝔉_a with respect to a², and only the −c₁₄a² part of K^{ab}{}_{mn}∇u∇u survives at rest). Then

8πG T^{flow}_{ab} = ∇_m[ 𝒥_{(a}{}^m u_{b)} − 𝒥^m{}_{(a}u_{b)} − 𝒥_{(ab)}u^m ] + F′[ c₁((∇_mu_a)(∇^mu_b) − (∇_au_m)(∇_bu^m)) + c₄a_aa_b ] + λ̃ u_au_b − ½ g_{ab} M²F(K),

with the multiplier fixed on shell, λ̃ = u_n∇_m𝒥^{mn} − c₄F′a²; the multiplier term is therefore not an independent density. The flow equation is ∇_a𝒥^a{}_m − c₄F′a_a∇_mu^a = λ u_m (up to sign conventions).
- **Rest mass:** none. The action contains no term of the form m·(function of u) with a mass parameter; the only scales are a_* and θ_Λ from rule T (§1.2). **Particle number / conserved current:** none. A unit constrained vector field has no global symmetry, so no Noether charge; the multiplier λ is an enforcement of u² = −1, not a density.
- **Static weak-field content (hand, to be verified):** the time–time source in the Φ equation is the effective density ρ_eff = ∇·(q∇Φ)/(4πG) = (1/4πG r²) d[r²(g−g_N)]/dr in spherical symmetry (for the P2 point mass this is the CFG44 phantom density a₀/(4πG r√(1+x²)) > 0); the aether's own anisotropic and pressure stresses are O(Φ/c²) relative to ρ_effc² (so Ψ = Φ, γ = 1); the u-frame canonical density T_{ab}u^au^b is reported separately (it is not the same as ρ_eff, because the a²-channel also feeds the metric equations through Φ). **ρ_eff is a functional of ρ_b** (response, slaved to the baryons): with the baryons removed it is zero, so it carries no free "amount" of mass, unlike a cold species whose amount is initial data. It gravitates (an effect of the flow's stress) and is conserved jointly with the rest by diffeomorphism invariance; with baryons minimally coupled it is conserved on its own.
- **Equation of state:** not a perfect fluid, and not vacuum-like (w ≠ −1): in the static limit it behaves as a stress-free (dust-like) source of the Poisson equation with no particle content; in FRW the θ² channel gives H²(1+3c₂/2) = 8πGρ/3 + Λ/3 (L350), i.e. an effective ρ_ae ∝ H² slaved to the expansion, w = −1 − 2Ḣ/(3H²) (hand; w ≈ 0 in the matter era) — a renormalisation G_cos = G/(1+3c₂/2), not an independent conserved fluid.

*Khronon form (11C-b, 11C-c, alternative reading).* With u_a = −∂_aφ/√(−X), X = g^{ab}∂_aφ∂_bφ, T^{flow}_{ab} has the same structure with the multiplier replaced by the projection required by u's dependence on g^{ab} (the extra term proportional to u_au_b). The flow's equation of motion is now scalar: ∇_aJ^a = 0 with J^a = (−X)^{−1/2}(g^{ab}+u^au^b)𝔈_b, 𝔈_b the aether equation. **This is a conserved current (the Noether current of φ → φ + const), so the khronon form carries one conserved charge Q = ∫J⁰d³x, absent from the aether form.** In FRW a nonzero Q gives an a⁻³ term ("dark matter as an integration constant" in projectable Hořava/khronometric gravity; from memory, Mukohyama-type). **Frozen rule: Q ≡ 0 in every scored configuration (the leaf-constant Π₀ of 11C-c is fixed by ⟨δθ⟩ = 0, not a charge).** A configuration needing Q ≠ 0 would carry a conserved number and is reported as a labelled sub-case "11C-x (khronon charge ≠ 0)", outside the owner's picture, never pooled.

*Per sub-variant (explicit):*
- **11C-a:** T^{flow} from the a²-channel of 𝔉_a plus the −c₂(θ−⟨θ⟩)² term (which vanishes on the static configuration and on FRW with the leaf average). Effective source ρ_eff as above; no rest mass; no charge (aether form) or Q = 0 (khronon form).
- **11C-b:** T^{flow} from M²F(K) with the operating-point shift K_bg; on FRW an effective ρ_ae = −(3c₂/16πG)θ²-type term ∝ H² (G-renormalisation); static content as in 11C-a but evaluated at the shifted operating point; no rest mass; Q = 0.
- **11C-c:** T^{flow} as 11C-a. **The coupling adds an interaction, not a flow mass:** the baryons' effective mass is m(1 + βh), i.e. the flow modifies the *baryon* sector; integrating out δθ gives an energy density −(K_c/2)ρ_b² and pressure −K_cρ_b²/2 (hand, §1.3), which is the flow's effect on baryons, not a species. The flow itself has no rest mass and, in the aether form, no charge.

**Admission check S1 (stress-energy reported).** Each script prints, for every variant: T_uu, p_r, p_t, ρ_eff, the on-shell conservation residual (11C-c includes the coupling force), and the FRW ρ_ae(a), p_ae(a).
**Admission check S2 (owner's picture; not a G1–G7 gate).** A variant is "inside the owner's picture" iff: (a) the action has no rest-mass parameter (no term whose coefficient carries a mass), (b) the flow sector has no conserved particle number or charge (aether form: none by construction, checked by sympy; khronon form: Q = 0), and (c) its effective density is a functional of the baryons (no free amount). A variant failing S2 is still scored on G1–G7 but is labelled "outside the owner's picture" in the table.

### 9.2 The cold component

- **As in candidate B:** the cold dark component (Ω_c h² = 0.1200, FITTED, a conserved cold fluid, not a new particle species; the record's standing rule that the mass is still required) is present in every run of G2 (CMB and growth; the ΛCDM reference has it). The flow replaces only the law's phantom, as the Door 11 file states. G1 is scored with baryons only as the source (§1.1), and the co-existence of the cold fluid with a flow-generated phantom inside galaxies (candidate B's declared max rule; the double counting of N13) is **not** covered (§8).
- **Can a variant pass G2 without it? A labelled test, never pooled.** Run "**11C-x-nocold**" as a separate variant column: same action, same constants, Ω_c h² → 0 in the G2 evaluation, everything else (baryons, radiation, Λ, the flow) unchanged. Pass lines, frozen now: (i) background: the flow's effective density ρ_ae(a) from its own FRW equations must equal the density the cold fluid supplies, ρ_req(a) = 0.1200/h² · ρ_crit,0 · a⁻³, to within 5% for a ∈ [1e-3, 1]; (ii) perturbations: the flow's effective sound speed c_s² ≤ 1e-6 c² over 10 ≲ z ≲ 1100 (declared here; the record's GDM constraint on the cold component is far tighter), and linear growth within 5% of ΛCDM to k = 30 /Mpc; (iii) the CMB part stays UNDEFINED unless (i) and (ii) pass, in which case a Boltzmann-level treatment is requested as a further step, not done here. The cold-on and cold-off columns are reported side by side and **never combined into one verdict**.
- **Hand estimate for the no-cold run (written before any script):** a massless flow with no charge can supply at most a renormalisation of G (c₂ ≲ 6e-4–3e-3 from the Planck-era bounds the record cites, L350), i.e. an effective density fraction of order 1e-3 of the matter density, against the ≈ 0.84 of the matter that is cold; so (i) fails by about three orders of magnitude for all three sub-variants: **P(11C-x-nocold fails G2) ≈ 0.97**. The only route to a pass would be a nonzero khronon charge Q (an a⁻³ dust from an integration constant), which S2 rules out for the owner's picture; it would be reported as 11C-x with the outside-the-picture label.
- **What would be tested if it surprised:** an independent re-derivation of the flow's FRW equations and of its perturbation sound speed, exactly as for a G1 pass (§7).

### 9.3 Additions to the estimate table (written before any script)

| item | 11C-a | 11C-b | 11C-c |
|---|---|---|---|
| S2 (inside the owner's picture) | P 0.9 in aether form; P 0.85 in khronon form with Q = 0 | P 0.9 / 0.85 | P 0.8 (the baryon coupling changes the baryons' mass by the flow, not a flow mass; reads as a fifth-force coupling) |
| G2 with the cold fluid | as §3 | as §3 | as §3 |
| G2 with no cold fluid (11C-x-nocold) | F 0.97 | F 0.97 | F 0.97 |

---

Hash of this file is reported by the writer after the last edit; a later change would void it.
