# CFG172 — Door 11C: a covariant timelike-flow completion of the flowing Λ-vacuum (phase 2: results)

Frozen criteria: `CFG172_FROZEN_CRITERIA.md` (commit 51716d8e4 with §9 Addendum 2; Erratum 1 appended in ac2d5a2be). Scripts, outputs and results JSONs are in this directory; nothing in the repository was edited (the scripts import CFG44's `Bcommon.py` read-only). κ = ½ is FITTED. Literature facts are from memory or as the record / data-chat note quotes them, none re-read. No new data.

**Nothing here says the theory is closed, that the timelike-flow reading is refuted outside the frozen class, or that any data favour the framework. A scoped no-go is not a closure.**

## 0. Flag first: did anything pass G1 as a derived mechanism (M2)?

**No.** 11C-a and 11C-c(full) pass the G1 *law* only because the flow function is set to the target's kernel by declaration (grade **P-declared**, M1, script A1). The kernel does not follow from rule T (the Λ-tie) or from any symmetry. Per the frozen rule this is a restatement of the kernel choice, not a pass as a mechanism; I nevertheless request an independent re-derivation of the field equations of §1 (cheap: `CFG172_A1_static_reductions.py` S1–S6 derive them with sympy) because a P-declared result is a G1-law pass. 11C-b fails G1; 11C-c's coupling produces no law by itself (θ-only test fails).

## 1. Gate table (each cell cites its script; PASS / FAIL / UNDEFINED / NOT ADDRESSED)

Scripts: A1 = `CFG172_A1_static_reductions.py`, A2 = `..._A2_stability_pincer.py`, A3 = `..._A3_ppn_frame.py`, A4 = `..._A4_growth.py`, A5 = `..._A5_reaction_energy.py`, A6 = `..._A6_b_operating_point.py`, A7 = `..._A7_c_response.py`, A8 = `..._A8_stress_energy.py`, V = `CFG172_verdict.py` (output `CFG172_verdict.out`). G8 is 11B-only (not addressed here).

| gate | 11C-a (acceleration channel, P2) | 11C-b (single F(K), θ in the argument) | 11C-c (matter–θ coupling; full = a-channel + coupling) |
|---|---|---|---|
| G1 law | **PASS** [A1: max dev 5e-14 over 7 masses × point/exp sphere × both footings; ν_mono 5e-6] (declared kernel) | **FAIL** [A6: passes only for offset t ≤ 1.2e-6 (4e-4 with a mirrored continuation); G6∧G7 need t ≥ 4.0e6, a gap of 3e12 (1e10)] | **PASS (full)**, inherited from the a-channel; **FAIL (θ-only)**: best deviation 0.97 for every K_c, point mass gets no force [A7] |
| G1 mechanism | **P-declared** (not M2) [A1] | FAIL [A6] | **FAIL**: no kernel from the coupling (local, linear in M_b) [A7] |
| G2, cold fluid ON | **FAIL** [A4: quasi-static \|G_eff/G−1\| up to 2e2; linear theory strongly coupled; CMB part UNDEFINED] | **FAIL where G1 passes** (t = 1.2e-6: 28); PASS only at the G6/G7 corner t = 4e6 where G1 fails [A4]; CMB part UNDEFINED | **FAIL** [A4, same a-channel] |
| G2, cold OFF (labelled 11C-x-nocold, never pooled) | **FAIL**: ρ_ae = 0 on FRW (leaf-averaged θ-term); baryon-only growth D(1)/D(1e-3) = 156 vs 710 (ratio 0.22) [A8] | **FAIL**: ρ_ae/ρ_req = 1e-3…1.6e-2 with the wrong sign; growth ratio 0.22 [A8] | **FAIL** [A8] |
| G3 | **FAIL**: reaction PASS by construction (minimal coupling); energy stored in the flow term to 0.4 r_ta is 14–240× the orbital energy (both r_ta conventions) [A5] | **FAIL** (energy) [A5] | **FAIL**: energy as a; contact-force reaction ≤ 0.10 g_law only for K_c ≤ 4.5e-6 (km/s)² kpc³/M☉ [A5, A7] |
| G4 strict / inert-window | **FAIL** (1: c₂) / PASS (0 counted: verdicts invariant over c₂ ∈ [5.3e-5, 6.3e-4]) [A3, A6] | **FAIL** (1: size of c₂) / PASS (0 counted: fails for every c₂) [A3, A6] | **FAIL** (2: c₂, β) / **FAIL** (1 counted: β; G1(full) goes 0.10 → 1.0 → 100 at 1×, 10×, 1000× the G3 ceiling) [A7, V] |
| G5 | **FAIL**: isolated Sun's own flow field at Saturn is 6.3e3× (canonical) / 7.6e3× (alt) the Q₂ bound; any kernel within the G1 band with (yq)′ ≥ 0 keeps a tail ≥ 0.282 a₀ (Q₂ ≥ 3.6e3×). Kinetic signs PASS; γ = 1 PASS; hyperbolicity / criterion B UNDEFINED [A2] | **FAIL**: same Sun tail; (y q_eff)′ < 0 above the branch point for any t > 0 [A2] | **FAIL**: c_s² = −K_cρ < 0 for every K_c > 0 (c₂ < 0 is a ghost); at the G3 ceiling Γ = k·47 km/s, unbounded in the UV; plus the a-channel tail [A7, A2] |
| G6, α₁ lines 3.4e-5 (frozen) / 3.5e-5 / 2.1e-5 (Liu+2020), α₂ ≤ 1.6e-9 | **PASS**; the three α₁ lines agree; α₂ binds nowhere (isolated systems at their own acceleration; quoted formulas) [A3] | **FAIL** at every c₂ that G7 allows: α₂ needs c₂ ≤ 3.5e-14 (1.6e-14 with θ = 3H₀); α₁ alone needs c₂ ≤ 2.8e-8 (1.7e-8 at 2.1e-5); the three α₁ lines give the same region; α₂ is the binding line [A3] | **PASS**; three α₁ lines agree [A3] |
| G7 | **UNDEFINED**: in the KM1 modelling (re-derived) PASS iff c₂ ≥ 2.7e-5 (c₁₄^eff = 0) … 5.3e-5 (c₁₄^eff = 1); the transfer to the nonlinear a²-channel is not derived [A3] | **FAIL** at every c₂ that G6 allows (needs c₂ ≥ 2.7e-5) [A3] | **UNDEFINED** as 11C-a [A3] |
| S1 stress-energy (Addendum 2) | REPORTED: T_uu = the Φ-equation source; p_r = −p_t = −ℓ′Φ′²/8πG (O(Φ/c²) relative); conserved (Newtonian-limit residual 0) [A8] | as a, plus a G-renormalisation ρ_ae ∝ H² on FRW | as a; the coupling adds −K_cρ²/2 pressure to the baryons |
| S2 inside the owner's picture | **PASS** (no rest-mass parameter; Q = 0 by the vanishing momentum constraint; ρ_eff ∝ √M at large r) [A8] | PASS [A8] | PASS with caveat (the coupling changes the baryons' mass) [A8] |
| D1 a₀(z) law (diagnostic) | flat by rule T | **∝ H(z)-like**: a_*(z)/a_*(0) = 1.79, 3.77, 8.29 at z = 1, 2.5, 5 (the rival law) [A6] | flat |
| D2 lensing vs dynamics (diagnostic) | Ψ = Φ exactly [A1 S1]; not otherwise scored | as a | as a |

**Binding gate per sub-variant.** 11C-a: **G5** (the Q₂ tail, forced by the G1 band plus (yq)′ ≥ 0, a pincer), with G2 and G3-energy also failing. 11C-b: the **G1 × (G6, G7) pincer through the tie** (G1 needs t ≲ 1e-6, G6 and G7 need t ≳ 4e6), and G1 × G2. 11C-c: **G5** (c_s² < 0) and **G1 as a mechanism** (the coupling supplies no law).

## 2. MUTATE outcomes (13 runs, all exit 1 = the control bit)

| control | script | claim that had to fail | outcome |
|---|---|---|---|
| M1 flow scale 3a₀ | A1 | G1 law | bites (max dev 0.73) |
| M1 flow scale 3a₀ at t = 1.2e-7 | A6 | G1(b) baseline pass | bites (0.000 → 0.73) |
| M2 kernel → GR | A1 | G1 law | bites (0.97) |
| M2 kernel → GR | A2 | G5 Q₂ cell flips to PASS | bites (Q₂ = 0) |
| M2 kernel → GR | A4 | G2 recovers | bites (worst |G_eff/G−1| ≤ 5%) |
| M3 q → −q | A1 | G1 law | bites (0.98) |
| M3 q → −q | A2 | kinetic-sign cell | bites (fails) |
| M3 c₂ → −c₂ | A7 | c_s² < 0 cell | bites (c_s² > 0, but the sector becomes a ghost) |
| M4 β = 0 | A7 | δθ ≡ 0, no force | bites |
| M5 w = 3000 km/s | A3 | G7 (a, c) | bites (D/3 0.011 → 0.267) |
| M6 offset t → 0.01 t | A6 | G1(b) responds | **Newtonian continuation: DOES NOT BITE** (both saturate at 0.967; declared control failure); mirrored continuation bites (0.946 → 0.661) |
| M7 khronon charge Q ≠ 0 | A8 | S2(b) fails | bites, **tautologically** (a nonzero conserved charge is the definition of failing S2; weak control) |
| M8 cold restored in the no-cold run | A8 | growth ratio recovers | bites (0.22 → 1.000) |

## 3. The record's kills, re-checked against the owner's "compaction" reading (matter changes the expansion rate θ of the time-flow)

| record kill (path) | what the record found | does the compaction reading escape it? | why, from what the scripts showed |
|---|---|---|---|
| FC-KH khronometric instability (`qwen_claude_field_theory/closure_2026/fc_kh_terminal/FC_KH_PAPER_vNEXT.md`; index N6) | for S = R − 2f(a), radial khronon stability needs (yq)′ ≥ 0; exact GR at high a forces q ≡ 0; only a slow tail is stable and it leaves ≈ a₀ at high g (Cassini ≈ 1e4×) | **No** for the acceleration channel; **not helped** by θ in 11C-b | A2 re-derives the second variation (decoupling limit, own sympy): K_x = N(yq)′, K_⊥ = Nq (A2.1–2.2), reproduces the exponential kernel's (1−y)e^{−y} < 0 for y > 1 (C2), finds true P2 stable ((yq)′ = 1−2y/√(1+4y²) > 0) but keeping a tail a₀/2 at the Sun (Q₂ = 6.3e3× the bound, A2), and constructs the minimal-tail kernel inside the G1 band (tail 0.282 a₀ ⇒ Q₂ ≥ 3.6e3×). θ does not enter the acceleration channel (11C-a, -c). In 11C-b, putting θ in the same function makes (y q_eff)′ negative just above the branch point for any t > 0 (A2, declared continuation). The record's "β,λ cannot cure it" identity was **not** re-tested (θ-channel not in the decoupling limit). |
| KM1 / L333: a₀ tracks the CMB-frame speed unless c₂ ≫ 1e-4 (`real_research/khronon_momentum_2026/KM1…py`, `real_research/g03_audit_2026/L333…py`) | a moving phantom is carried only by the c₂ channel; the aether's acceleration input is distorted by D cos²θ, D = 2w²/(c²c₂) | **No** where θ is stiff enough to be pinned; the compaction reading needs a *soft* θ, KM1 needs a *stiff* one | A3 re-derived (not imported) the moving-source solve: φ = φ_static(1 + C v²μ²), C = 2(2+3c₂)/(c₂(2−c₁₄)) (matches the record's leading 4/(c₂(2−c₁₄)); the O(c₂) terms differ, kept); D/3 = 0.114 and 0.285 reproduced at 620 km/s; G7 needs c₂ ≥ 2.7e-5. In 11C-b the tie forces c₁₄ = 302 c₂ (440 c₂), so α₂ needs c₂ ≤ 3.5e-14 against G7's 2.7e-5: no point passes both (A3). For 11C-a/-c the transfer to the nonlinear a²-channel is not derived (UNDEFINED). |
| AeST v9 PPN kill (`qwen_claude_field_theory/closure_2026/V9_PPN_KILL_VERDICT.md`; index N7) | with the scalar's drag term the effective aether anisotropy at the deep-field background gives α₁ = −2(K_B+2), ≳ 4.4e4× the bound, evaluated linearised about the cosmological background | **Not decided** by these scripts | 11C has no scalar. A3 evaluates the aether coefficient at the test system's own acceleration (q(y) ~ 1e-8…1e-12): α₁ ≈ −3e-8 (1 AU), −2.9e-6 (Saturn), PASS on all three α₁ lines. **But** if the preferred-frame sector of the Solar System were governed by the galactic background (y ≈ 1.5, q ≈ 0.27), α₁ ≈ −1.1: a FAIL by 3e4 (A3, printed, not scored). The record's kill used the deep-field value; which background applies is exactly what the frozen "own acceleration" definition assumes and this lane did not resolve. This is a live unresolved item, not a pass. |
| Single-metric pincer (DC-013 / DC-019; index N1; `qwen_claude_field_theory/closure_2026/frame_free_slip_lock_2026/`) | one frame-free metric: slip locked to a ray; constraint-first version leaves α₃ = O(1) unless retarded | **Yes by hypothesis** (a preferred-frame flow), not tested for α₃ | A1 S1: the g_ij equation has no flow source, Ψ = Φ exactly (γ = 1); A8: the flow's stresses are O(Φ/c²) relative. α₃ and the retardation question were not computed. |
| V0 region-gate obstruction and CV4 (`real_research/chk_v0_2026/README.md`, `CV3…`, `CV4…`) | a gate as a varied term is obstructed; the khronon's K is pinned to 3H inside bound regions, so a K-only gate is blind | **Not shown to escape**; the compaction reading needs exactly what CV4 says does not happen | A6: G1 needs the local operating offset t ≲ 1.2e-6 while the cosmic value that G6, G7 allow is t ≈ 4e6, i.e. θ inside galaxies must be lower than the cosmic θ by a factor ≈ 2e6 in θ (t ∝ θ²). A7: an explicit matter–θ coupling makes θ respond locally to ρ (δθ ∝ ρ − ρ̄), but the response is local (no long-range force; θ-only best deviation 0.97) and unstable (c_s² < 0). CV4 itself was not re-run (θ = 3H used as input). The non-perturbative "maximal-leaf" branch was not constructed. |
| DE12 / DE13 gate stiffness (`real_research/dark_energy_2026/DE12…py`, `DE13…py`; index N14) | a smooth on/off gate has W″ of both signs, the instability lands on the field the gate reads (baryons for the MOND-sector reading) | **No** for local gates, consistent with the record | A2 (11C-b): the local F(K) transition has a band of wrong-sign radial kinetic coefficient; A7 (11C-c): the θ-coupling's second variation lands on the baryons as a negative pressure (c_s² = −K_cρ). No nonlocal gate is in the frozen class, so CFG48's stable nonlocal counter-case is untouched (it would add a length). DE12's numbers were not used. |

## 4. Controls that failed, did not bite, or were weak (all kept)

- **C5 as frozen failed:** the frozen text said the strict-law Milky-Way tide is 4.0–5.7× the ceiling. CFG7 H1's recipe gives 1.56e-31…2.56e-31 s⁻², about 3e-5 of the bound (reproduced to 3 digits by C5b, A2). The 4.0–5.7 in `GATES.md` has another origin. A2 main exits 1 for this reason.
- **A5.1 failed (non-load-bearing):** my phantom-inclusive r_ta (fixed Δ = 11.81) differs from CFG4's by 2.45–4.37× against the referee's 1.7–3.6×; A5 main exits 1. The G3-energy verdict does not depend on it (14–240× in both conventions).
- **M6** (Newtonian continuation) did not bite; **M7** is tautological. **M4** was run for β = 0 only, not for the 11C-b half of the frozen wording (c₂ → ∞), and **M6** was implemented as a change of the ratio c₂/c₁₄ (the frozen wording, c₂ → 0.01c₂ with the ratio kept, leaves t unchanged).
- C3 (KM1 numbers): the D/3 numbers reproduce; the O(c₂) part of C differs from the record's (6c₂ against 4c₂ + c₁₄c₂): unexplained, immaterial at c₂ ≤ 1e-3.

## 5. Wrong expectations (kept; frozen values not repaired)

- **Kernel (Erratum 1).** The frozen §0/§1.2 hand algebra used the simple kernel (q = 1/(1+y), 𝒬 = 2[y−ln(1+y)], tail ≥ 0.47 a₀, tail/Q₂ ≈ 1.3e4×). For CFG44's P2 (ν = √(1+a₀/g_N)), with the aether's argument being the acceleration g (not y_N): μ(y_g) = (√(1+4y²)−1)/(2y) (equivalent to the erratum's μ = √(y_N/(1+y_N)) as a function of y_N), q = 1−μ, 𝒬 = y² − y√(4y²+1)/2 + y − asinh(2y)/4, (yq)′ = 1−2y/√(1+4y²). **Changed hand numbers:** minimal tail 0.47 a₀ → **0.282 a₀** (simple 0.4675 and ν_mono 0.424 reproduced/reported as sensitivities); the Sun's own P2 tail is a₀/2, giving Q₂ = **6.3e3×** (frozen: ≈ 1.3e4×; the 1.3e4 is what the simple kernel and ν_mono give: 1.26e4, 1.30e4); sign of (yq)′ unchanged (positive). The simple and P2 kernels differ by up to 15.5% in ν, so declaring one and scoring against the other would fail G1.
- **§3 estimate G1(11C-c) "F 0.97":** wrong as an estimate of the full model: S_c contains the a-channel, so G1 passes by inheritance; the frozen θ mechanism fails (θ-only diagnostic added).
- **§1.3 (ii) "flow momentum flux ∝ r⁻⁶":** wrong: with c₁₃ = 0 the flow's stress is local in δθ, exactly zero outside the baryons at quadratic order (A7 C7.6).
- **§9.1 "T_uu differs from ρ_eff":** wrong: T_uu equals the Φ-equation source (A8.1).
- **G6(b) "c₂ ≲ 1e-11"** was loose: the α₂ line gives 3.5e-14 (1.6e-14); the α₁-only ceiling is 2.8e-8.
- **G3 energy** (frozen "uncertain, F 0.4"): a clear FAIL (14–240×).
- **G3 reaction (11C-c)** (frozen "F 0.6"): PASS for small enough K_c; the coupling is unneeded and fails G5 at any K_c > 0.
- **11C-b "at the rule-T tie the transition sits at a₀":** the balance c₁₄a² = c₂θ² is a branch point of F, not a shift: G1 already fails at t = 1 (A6). The frozen estimate of a_* ≈ 1.9e3 a₀ at the G6/G7 corner is confirmed (√t = 2.0e3).
- **G7 (11C-a) "P(U) 0.45":** consistent (UNDEFINED).

## 6. Departures from the frozen criteria (disclosed)

1. True P2 is the primary kernel (Erratum 1); the simple kernel is a labelled sensitivity, never pooled.
2. 11C-c: a **θ-only** diagnostic was added (a-channel removed) because the full model inherits 11C-a's law; G1(full) and G1(θ-only) are reported separately.
3. G5: only the **kinetic signs in the decoupling limit** (metric fixed, no θ-channel) were derived; the gradient/characteristic sector (the decoupling limit gives ω_x² = N² da/dx, kernel-independent, not trusted), hyperbolicity and criterion B are UNDEFINED. Q₂ and the pincer are computed as frozen.
4. G6: α₁ = −4c₁₄ and the α₂ expression are the **quoted** formulas (not re-derived); only G_N = G/(1−c₁₄/2), G_cos/G_N = (2−c₁₄)/(2+3c₂) and the moving-source C were re-derived. The α₂ ≤ 1.6e-9 line is applied to the pulsar row only (a strong-field limit, per the data-chat note); at Saturn α₂ = 3.6e-7 would exceed it if it were applied to planetary systems.
5. 11C-b model: F depends on u = y² − t; the branch below u = 0 is a declared continuation (Newtonian; a mirrored one as sensitivity); the numbers differ (t ≤ 1.2e-6 versus 4e-4), the conclusion does not (gap 1e10–3e12).
6. G2: crude BBKS reference (σ₈ = 0.811) and a nonlinear quasi-static estimate; the CMB part is UNDEFINED; the no-cold growth test ignores Compton drag and baryon pressure (which would make it worse).
7. G3 energy: E_a = |(1/8πG)∫a₀²𝒬 d³x| (the flow's Lagrangian term) is my declared definition; the phantom-inclusive r_ta uses Δ = 11.81 (approximation of CFG4's).
8. `run_all.sh` and `cfg172_common.py` (repo-root helper) were added to the frozen script list; A5's script order in `run_all.sh` puts A6/A7 before it because it reads their JSONs.

## 7. Hypotheses NOT tested

Non-spherical baryons; the aether's twist mode and c₁₃ ≠ 0 (GW170817 is built in and was not tested by a script; the shear drop-out at c₁₃ = 0 is asserted, not run); nonlinear cosmology, clusters, mergers, time-dependent solutions and KM1's nonlinear khronon regime; the external-field effect and the ambient-background reading of PPN (printed, not scored, §3); α₃ and retardation (single-metric pincer); the record's "β,λ-free" identity in the θ-channel; the maximal-leaf branch of CV4; lensing beyond Ψ = Φ (D2); CDM co-existing with a flow-generated phantom inside galaxies (double counting, N13); any Boltzmann-level CMB or perturbation solver; Compton drag in the no-cold run; CFG48's nonlocal gates; the projectable Hořava class; AeST (vector + scalar), whose CMB/GW-speed/ghost checks the data-chat note reports at the abstract level only (not treated here as verified).

## 8. Inputs from the peers, checked against the scripts

- **CFG176's statement** (time-direction flow reproduces ΛCDM's H(z) up to a rescaling of cosmological G by 1/(1 + (c₁ + 3c₂ + c₃)/2)): **consistent**: A3 C4 derives H²(1+3c₂/2) = 8πGρ/3 + Λ/3 from the minisuperspace at c₁₃ = 0, i.e. G_cos = G/(1+3c₂/2). The claim that in GR a cosmological constant cannot flow (effects ∝ 1+w) was not checked. No script contradicts either input.
- **Data-chat note:** its remark that the dark-matter regime of generalized Einstein-aether fails CMB+LSS is consistent with A4 (the a-channel over-grows, G2 FAIL); Addendum 2's no-cold result (A8) agrees with it that the flow cannot supply the cold mass.

## 9. Files and re-run

`cfg172_common.py`, `CFG172_A1_static_reductions.py`, `..._A2_stability_pincer.py`, `..._A3_ppn_frame.py`, `..._A4_growth.py`, `..._A5_reaction_energy.py`, `..._A6_b_operating_point.py`, `..._A7_c_response.py`, `..._A8_stress_energy.py`, `CFG172_verdict.py`, `run_all.sh`, the matching `*.out` and `*_results.json` (main and `*_MUTATE_<M>_…`), `CFG172_verdict.out`, this README, and the frozen file.

Re-run (about 35 s; needs numpy, scipy, sympy; from this directory): `ZF_REPO=<repo root> bash run_all.sh`. Main runs exit 0 unless a reproduction control failed (A2 and A5 exit 1 for the two failed controls of §4, kept); MUTATE runs exit 1 when the control bites. No absolute home path is printed or stored (the repository appears as `<repo>`).

**Once more: a scoped no-go on the frozen class (S_a, S_b, S_c(lin/sat); static spherical weak field; c₁₃ = 0; declared P2 kernel; rule T) is not a closure of the time-flow reading, and κ = ½ stays fitted.**

## In-place re-run (orchestrator)

`bash run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`): main runs exit 0 except A2 and A5 (exit 1, the two failed reproduction controls C5 and A5.1, kept); all 13 MUTATE runs exit 1; the verdict script exits 0. Every `.out` and `_results.json` is identical to the agent's apart from timing. The frozen criteria are `../CFG172_FROZEN_CRITERIA.md` (51716d8e4, with Erratum 1 appended in ac2d5a2be); the fourth sub-variant (11C-d, V0 / C-H/K with the region gate replaced by the time-flow's matter-sourced expansion) is NOT part of this lane's results and gets its own frozen file. An independent re-derivation of the field equations A1 S1-S6 is requested (the G1 law passes only through the declared P2 kernel).
