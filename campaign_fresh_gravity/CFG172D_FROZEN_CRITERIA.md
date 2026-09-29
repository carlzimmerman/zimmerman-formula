# CFG172D — Door 11C-d: V0 (C-H/K) with its region gate replaced by the time-flow's matter-sourced expansion θ. FROZEN CRITERIA (phase 1)

Written 2026-09-29, before any script of this lane. Nothing below may change after a result is seen; any later deviation goes in the README as a disclosed departure. No physics script has been written or run. Every number marked "hand" is arithmetic done by hand (checked once with a one-line calculator, not a script) from record formulas and is itself to be re-derived in phase 2. Numbers marked "record" are as the cited record file states them and were not re-derived. Literature facts are **from memory, unverified** unless a record file is cited. κ = ½ is FITTED. Nothing here says the theory is closed, and nothing says any data favour the framework. A scoped no-go is a valid and likely answer.

This is a fourth sub-variant of Door 11C, scored separately from 11C-a/-b/-c (`CFG172_FROZEN_CRITERIA.md`, committed 51716d8e4, with its Erratum 1) and never pooled with them. It shares that file's setup (rule T, the target, the G1–G7 scoring lines, the MUTATE conventions, the exclusions analysis) and cites it instead of repeating it. The Door 11 file's Erratum 1 applies: P2 is ν = √(1 + a₀/g_N); the simple kernel ½ + √(¼ + a₀/g_N) is a labelled sensitivity only.

Sources read for this file (under the repo root): `campaign_fresh_gravity/closure_map/DOOR11_FLOWING_VACUUM_GATES_2026-09-29.md` (variants, gates, addenda 1–2, erratum 1); `campaign_fresh_gravity/CFG172_FROZEN_CRITERIA.md`; `campaign_fresh_gravity/closure_map/ACTIONS_AND_NOGOS.md` (V0 row, N1, N5–N8, N12, N14, N15, N21; Gaps 1–2), `GATES.md` (rows 4.01–4.04); `real_research/chk_v0_2026/README.md` and the CV1 output and CV4 header; `real_research/dark_energy_2026/DE1`, `DE7`, `DE12`, `DE13` headers and the DE12 output; `real_research/g03_audit_2026/L359` header; `campaign_fresh_gravity/CFG44_fluid_target/Bcommon.py` and README. Not re-read in full: the CV2/CV3 scripts, L340, L350, L333, KM1/KM3, the XR36 output (their content enters only as the record states it in the files above).

## Forking paths and multiplicity (stated first)

- **The menu is not blind.** Door 11's variants were written knowing the CFG44 target and the ten-door result. 11C-d was requested by the owner's orchestrator after the record showed V0's region gate as the one open obstruction of the one surviving covariant action; the replacement variable (the flow's θ), the two ways of sourcing it (d1, d2) and the gate's calibration are my design, made with the obstruction's mechanism in view (§0.3). The hand argument in §3 (the "T-d1 theorem" and the "pincer formula") was written before any script and predicts failure; it is kept whatever the scripts show.
- **Gates and pass lines are the orchestrator's** (Door 11 file, CFG172 §2). Where I had to add a definition it is marked "declared here". In particular the **obstruction pass line (O1) is stricter than the negation of the record's own criterion**; the record's criterion and mine are both reported (§2.1).
- **A one-sided existence test, not a fit.** Wherever a coupling constant would be tuned (ζ in d2) the test asks whether ANY value satisfies all lines at once (interval intersection). No value is selected to make a gate pass, and no scan is used to pick a winner (standing rule: no knob scans).

---

## 0. What V0 / C-H/K is, and exactly what the obstruction was

### 0.1 The object (record)

- **Name and status.** "V0" is the cross-thread review's name for the C-H/K branch's one covariant action (`real_research/chk_v0_2026/README.md`; `ACTIONS_AND_NOGOS.md` V0 row). The 2026-09-26 owner decisions keep the branch: kernel ν_mono, causality criterion B, two branches never pooled. STANDING 09-28 calls it "the one surviving covariant action". Record status of the action itself: **INCOMPLETE — the varied region gate is OBSTRUCTED (DE12/DE13, XR15); the data passes use a prescribed mask.**
- **Covariant action (CV2, record):**
  I_V0 = c³/(16πG) ∫d⁴x √−g { R − 2Λ + 2h^{μν}(D_μU − a_μ)(D_νU − a_ν) + α_c a_μa^μ − c₂(K − ⟨K⟩_h)² + 2α² f q(h^{μν}D_μW_b D_νW_b/α²) + ∫₀^b dz L(∂_zW − Δ_hW) + λ₀(W₀ − Y) + 2Ψ[(Δ_h − m²(1 − f))Y − fΔ_h(U − V)] − 2σm²(1 − f)Y² + 2Λ_d[Δ_hV − (4πG/c⁴)(ε_d − ⟨ε_d⟩_h)] } + GHY + S_matter[g] + S_dark[g; dark state], with α = a₀/c², W_b the heat-filtered baryon field (filter S = e^{bΔ_h}, b = ξ²/2), and "the gate f a prescribed function of the leaf geometry (R⁽³⁾ + σ_ijσ^ij, K)". Every added field (Y, Ψ, V, Λ_d) is a leafwise auxiliary.
- **Non-relativistic limit (CV1, record; units of potential, S = 1 in what follows):**
  L = −(ρ_b + ρ_d)Φ − [2∇Φ·∇u − |∇u|²]/(8πG) + a₀² f q(|∇Sw|²/a₀²)/(8πG) + Ψ[(∇² − M²)w − f∇²(u − v)]/(8πG) + λ[∇²v − 4πG(ρ_d − ⟨ρ_d⟩)]/(8πG) − σM²w²/(8πG), with M² = m²(1 − f), q′(Z) = ν_mono(√Z) − 1.
  Field equations (CV1 A1, sympy residual 0): the kernel reads w, (∇² − M²)w = 4πG f(ρ_b − ⟨ρ_b⟩); baryons feel Φ = u + fP (P = Ψ/2); the dark component feels u only (L353's reciprocity pair). On a gate-on plateau (f = 1 with every derivative 0, M = 0): ∇²u = 4πGρ_b, ∇²Φ = 4πGρ_b + ∇·[(ν_mono − 1)∇u] (CV1 A2). Inside a spherical plateau the baryon force is ν_mono(g_N/a₀)g_N to 1×10⁻⁴; beyond the transition it is exactly Newtonian (CV1 A5).
- **Constants and declared numbers of V0 (record; all inherited by 11C-d, counted in §1.5):** κ = ½ (FITTED) and Ω_c h² (FITTED); c₂ in L340's window (7.3×10⁻³ … 0.067) and α_c ≤ 3.2×10⁻⁹ (KM3 window); the filter length ξ (N18: irreducible); σ = 1 (CV1: "the record's σ is inconsistent and must be declared per result"); the web screening length 1/m (100–500 kpc quoted in CV1 A5); the vacuum gate's (p, x_c0, w) = (1, 2.5, ≤ 0.25 declared; DE12 also runs w = 1); the MS5 cap v_cap = 325 km/s (declared); the kernel shape ν_mono (declared, from L340).
- **What the region gate does.** f = W(t), t = (s − 1)/(2w) + ½, W(t) = g(t)/(g(t) + g(1 − t)), g = e^{−1/t} (t > 0) else 0, s = u/x_c0 (DE7). The gate variable is the vacuum gate of L359/DE1: u = x̃ [Ω_Λ(K)/Ω_Λ,0]^p ≥ x_c0, x̃ = 9R⁽³⁾/(4K²), Ω_Λ(K) = 3Λc²/K² (units of the record), i.e. x_c,eff(z) = x_c0E(z)^(2p). By the Hamiltonian constraint x̃ = 4πGρ_dyn/H²: **the gate is a local dynamical-density switch.** Its jobs in the record: MOND on in bound regions, off in the cosmic web (growth: without a switch σ₈ is 18–27% off, L341; forest, KiDS external-field and cosmic-shear passes use it; the flagship's edge law is DE1's). On the cosmic background the gate is 0 (x̃ = 0 on flat FRW), so FRW = GR's Friedmann equation (CV2 B3) and the homogeneous zero is off-plateau (CV1 A6, Lean-certified for the curvature variable only; "each other gate variable must show its own homogeneous background is off-plateau" — this applies to u_θ below).

### 0.2 The obstruction, exactly (record; the numbers I will re-run against)

- **T1 (Lean DE7; record).** Any C² gate flat at both ends (f = 0 and f = 1 plateaus) has f″ of both signs on its transition. Wherever a gate multiplies a nonzero coefficient B (here B = a₀²q/(8πG), the region kernel's own Lagrangian density), one half of every transition layer has a wrong-sign second variation. The instability lands on whatever field the gate reads: the metric (k⁴ term; DE7 U1: E_* > 0 on part of every transition, repaired only at the cost of slip), a multiplier (CV3 G3: a zero of the constraint symbol on every transition, an eigenvalue crossing at some epoch for reading B, G3b), constrained fields (the baryons: DE12), or K alone (nowhere — but blind, CV4).
- **CV3 reading A+** (V0's best reading, C[∇²(u − v) + ∇·((ν − 1)∇Sw)], baryons plus their phantom built from constrained fields): leak-free, slip-free, all constraints invertible (determinant a²b² for every gate shape), cap held. **Its second variation lands on the baryons**: δ²E = ½(c_s²/ρ_b − S)(δρ_b)², S = B[W″t_U²U_ρ² + W′t_UU_ρρ], t_U = 1/(2w), U_ρ carrying the phantom's own response A = ν + yν′cos²θ (≈ 56 radial, 112 transverse at a 10¹¹ M☉ edge, y ≈ 8×10⁻⁵).
- **DE12 (record):** c_gate = √(ρ_bS) = 1500–3700 km/s at z = 0.25 against gas at 37 / 117 km/s (T = 10⁵ / 10⁶ K), growth Γ(k = 1/kpc)/H ≥ 2.0×10⁴ at z = 0.25 (minimum over the 12 galaxy cells: c_gate 1526 km/s, Γ/H 2.0×10⁴), 2.7×10³–8.2×10³ at z = 2.5, on every galaxy edge; the unstable gas mass is 0.25–1.4 of M_b per layer; even the broad w = 1 gate gives 300–620 km/s at z = 0.25. Pre-declared hypothesis G1 of DE12 ("the varied gate makes transition-layer gas unstable") **passed** (as a hypothesis of failure). Control A = 1 (reading A, baryons alone, no phantom amplification): c_gate = 18.4 km/s (z = 0.25) and 93.4 km/s (z = 2.5) at 10¹¹ M☉ — i.e. scaled by the A² of the phantom's response; CV3's own A = 1 table gives σ_v²/c_g² = 0.001–0.012 for 10 km/s gas (unstable) and 0.16–4.8 at 200 km/s.
- **DE13 (record):** a gradient stiffness repair μ|∇U|² or μ|∇f|² has its own background term K0 > 0 that destabilises the layer; no μ stabilises (E2 of DE13); the μ_U repair costs 32 v_f² at r_F; XR15: no single smoothing length (needs ≥ 500 kpc, the flagship holds to 100 kpc). **No repair is allowed in 11C-d** (a gradient repair is a new constant/length).
- **CV4 (record):** for a K-only gate f(Ω_Λ(K)) (no slip, no k⁴ term), the khronon equation on a static region is c₂D_i(N D^iK) = 0, so K = 3H(z) inside bound regions: |K/3H − 1| = 2×10⁻⁴ (10¹¹ M☉, 600 km/s, z = 0.25), 6.5×10⁻⁴ (z = 2.5), 1.9×10⁻³ and 4.8×10⁻³ (10¹⁴ M☉ cluster, 1000 km/s, z = 0.25 / 2.5); only a dipole for moving sources. **A K-only gate is blind.** Stated scope of CV4: linear khronon on a given metric, **no matter–K coupling**, and the non-perturbative "maximal leaf" branch (K ≈ 0 in halos) "has no source in the linear equation and is not constructed".
- **The dilemma the record leaves (this file's framing, hand):** a gate that reads curvature or the MOND sector is selective but unstable (DE7, DE12); a gate that reads K alone is stable but blind (CV4). 11C-d asks whether the owner's "matter compacts the time-flow" (a matter source in the θ equation, which CV4 excluded by hypothesis) can make K selective while a stiff θ sector (c₂) absorbs the gate's negative stiffness.

### 0.3 What "removed" would have to mean (declared here, before any script)

The obstruction is removed only if ONE run, with ONE set of constants, satisfies all of: (O1) the gate's second variation is stable on every transition layer, the stability being computed on the fields the gate now reads, including the baryons through any coupling; (O2) the gate is a genuine region gate (on in bound regions, off in the web) — not merely stable because it does nothing (CV4's blindness); (O3) V0's structural identities survive (plateau reductions, homogeneous background off-plateau, constraint symbols regular). **"Moved" = O1 passes but O2 fails, or O2 passes and the negative stiffness reappears on the baryons or on a new mode. "Still present" = anything else.** The three verdicts are reported per arm and never pooled across arms.

---

## 1. The exact replacement

### 1.1 Field content and the gate variable

V0 keeps every field of §0.1 (metric, khronon τ with unit normal u_μ = −∂_μτ/√(−X), the leafwise auxiliaries, the L353 pair, the dark slot exactly as V0/candidate B: a conserved cold component, Ω_c h² fitted, feeling u only). No field is added. The khronon's expansion θ ≡ ∇_μu^μ (= K of the record for a hypersurface-orthogonal flow) becomes the gate's argument. In spherical symmetry twist vanishes and khronon = unit timelike vector = the "time-direction flow" of Addendum 1.

**Gate variable (declared here).**
  D(θ) ≡ (⟨θ⟩/θ)² − 1 = Ω_Λ(θ)/Ω_Λ(⟨θ⟩) − 1,  u_θ ≡ D(θ)·[Ω_Λ(⟨θ⟩)/Ω_Λ,0]^p = D(θ)·E(z)^(−2p),  Ω_Λ(θ) = 3Λ/θ² (θ in inverse length; CV4's K-only variable),
  s = u_θ/x_c0,  t = (s − 1)/(2w) + ½,  f = W(t), with V0's declared (p, x_c0, w) = (1, 2.5, 0.25), w = 1 reported alongside (DE12's broad gate), and p = 2, x_c0 = 2 (the L364/DE1 cell) as a labelled sensitivity.
  Reading: u_θ is CV4's K-only gate variable, offset so that it vanishes on the background (⟨θ⟩ = 3H/c is the leaf average of CV2, so u_θ = 0 and f = 0 there for every w ≤ 1: t = ½ − 1/(2w) ≤ 0), and with V0's own z-scaling x_c,eff = x_c0E^(2p). It **replaces** x̃ = 9R⁽³⁾/(4K²) (the curvature/density measure, whose derivative f_R carried DE7's slip and k⁴ term) by the expansion deficit of the flow. Hand: the gate is ON (t = ½) where θ/⟨θ⟩ = [1 + x_c0E^(2p)]^(−1/2) = 0.535 (z = 0), 0.485 (0.25), 0.333 (1), 0.166 (2.5), 0.099 (4); i.e. a 46–90% depletion of the local expansion. This calibration is my choice (it keeps V0's x_c,eff(z)); a z-independent variant (u_θ = D) is a labelled sensitivity.

### 1.2 The action of 11C-d

  I_11C-d = I_V0 with f → f(θ) = W(t(θ)) everywhere f appears (three places: the region kernel, the Ψ constraint's M² and f∇²(U − V), and the σ term), plus, in the arm d2 only, the matter–θ source term below.
  f is no longer prescribed: it is a function of the flow's θ, so **varying τ (the khronon) now brings a gate term** — the piece CV4 did not have and the piece the record found obstructed when varied.

**Arm d1 — gate-sourced compaction (no new term; zero new constants).** Matter reaches θ only through the varied action: the gate multiplies the region kernel's energy density 𝓑, which is baryon-sourced (through w). This is "matter-sourced expansion" with the minimum modification of V0.

**Arm d2 — explicit compaction (one added term).**
  ΔI_d2 = c³/(16πG) ∫d⁴x √−g { −(16πG/c⁴)(ε_b − ⟨ε_b⟩_h) ζ h(ϑ) },  ϑ ≡ (θ − ⟨θ⟩)/θ_Λ,  θ_Λ ≡ √(3Λ),
  ε_b = the baryons' energy density (S_matter coupling: baryon dust with an effective inertial mass depending on ϑ; the coupling is to baryons only, minimal to g otherwise). d2(lin): h(ϑ) = ϑ. d2(sat): h(ϑ) = ϑ/(1 + |ϑ|) (CFG172 11C-c's declared shape). ζ is one dimensionless number (counts as a G4 failure unless tied). The leaf-mean subtraction removes the homogeneous part into ⟨θ⟩ (a background renormalisation) exactly as CV2 does for K. This is CFG172's 11C-c coupling attached to the gate instead of carrying the law: the law stays V0's region kernel, θ only decides where it is on.

**Reference arm d0 (control, not scored as a variant): CV4's gravity-only K.** Reproduces the record's blindness (§4 C2) with the gate now in the action, so d1's difference from d0 isolates the new gate-sourced term.

### 1.3 The θ equation (the new field equation), hand form to be derived symbolically in phase 2

Varying τ: δθ = ∇_μδu^μ, δu^μ = −h^{μν}∇_νδτ/√(−X). With Π ≡ ∂𝓛/∂θ (the flow's conjugate to θ, per (c⁴/16πG) units):
  Π = −2c₂(θ − ⟨θ⟩) + 𝓑 f′(t)·dt/dθ [− (16πG/c⁴)ζ(ε_b − ⟨ε_b⟩)h′(ϑ)/θ_Λ in d2],
  𝓑 ≡ ∂(brace)/∂f = 2α²q + 2Ψ[m²Y − Δ_h(U − V)] + 2σm²Y²  (V0's own coefficient of f; CV3's B),
and the khronon equation on a static leaf is ∇_ν[h^{μν}∇_μΠ/√(−X)] = 0, **so Π is a leaf constant Π₀** (regular at infinity; Π₀ fixed by the leaf average ⟨θ − ⟨θ⟩⟩ = 0). Hand statement of the hypotheses under which this is the whole equation: (H-i) the MOND sector has no O(π) source on the static background (CV4 K1, quoting XC3 C1) — **this must be re-derived for V0 with f = f(θ)**, because f now multiplies leafwise operators (Δ_h, m²) that depend on the foliation; (H-ii) α_c enters only through time derivatives (quasi-static, α_c/c₂ ≤ 4×10⁻⁷; record). If phase 2's derived θ equation differs from the above, the derived equation governs and the difference is disclosed; the hypotheses of §3's theorem are then re-checked and, if void, it is reported void.

### 1.4 The static weak-field spherical system that would be solved (what solves for what)

Given ρ_b(r) (point mass, and CFG44's exponential sphere ρ_b = ρ₀e^{−r/h}, h = 2 kpc, M_b(<r) = M[1 − (1 + s + s²/2)e^{−s}], s = r/h, `Bcommon.py`) in a flat leaf of mean baryon density ⟨ρ_b⟩(z) with H(z):
- **Solved by CV1's equations (with f = f(r) from θ(r)):** ∇²u = 4πGρ_b (+ dark, which feels u only); the Ψ, w, v, λ constraints as in §0.1; Φ = u + fP; the baryon acceleration g_bar = −∇Φ. The kernel is ν_mono (V0's declared kernel; P2 is the Door 11 primary and is run as the target of comparison and, separately, as a labelled "V0 with the P2 q-function" sensitivity; never pooled).
- **Solved by the θ equation:** θ(r) from Π = Π₀ (an algebraic, local relation on each leaf point given 𝓑(r) and ε_b(r); Π₀ from ⟨δθ⟩ = 0 or δθ → 0 at the box edge), iterated to a fixed point with the CV1 system (θ → f → CV1 → 𝓑 → θ). Multiple roots of Π(θ) at fixed r (an S-curve) are recorded as branch points and counted (§2.1 O1(b)); a solution branch is not chosen by hand — the continuation from the background is reported and the alternative branches are listed.
- **Nothing is prescribed but the shape of W, the kernel, and rule T's scales.** In particular the flow's "acceleration" (the khronon's own a_i) is a kinematic identity for a flow at rest (CFG172 §1.3 reading, declared there); G1 is scored on the baryons' acceleration −∇Φ from the solved equations, and the literal river reading is diagnostic D3 (zero here, as for 11C-a).
- Filter S = 1 in the static solves (ξ ≪ r_M; V0's CV1 used S = 1 for its field equations); the filter's length enters only in G5(ii) through the record's KM3 filtered remainder, as inherited.

### 1.5 Constants ledger (strict; the orchestrator's G4)

| item | status | count |
|---|---|---|
| κ = ½; Ω_c h² | FITTED (allowed) | — |
| rule T: a₀ = κc√(Gρ_Λ), θ_Λ = √(3Λ) | rule, not derived (CFG172 §1.2) | — |
| c₂ (window 7.3×10⁻³–0.067, record), α_c (≤ 3.2×10⁻⁹) | inherited from V0 | 2 (inherited) |
| ξ (filter), σ = 1, 1/m, v_cap | inherited from V0 (declared) | 4 (inherited) |
| gate (p, x_c0, w), W's shape, u_θ's offset definition | inherited numbers; u_θ's form is a declared choice | 3 + 1 shape |
| ν_mono shape | declared (V0) | 1 shape |
| ζ and h's shape (d2 only) | new | 1 + 1 shape |
| d1 | new constants: **0** | |
| d2 | new constants: **1 (ζ)** | |

So G4 (strict) **fails by inheritance for every arm**: V0 was never a two-constant action (record: ACTIONS_AND_NOGOS notes V0's "declared" gate/cap numbers). The G4 line that 11C-d can add to the record is the **new-constant count** (d1: 0, d2: 1) and whether the replacement removes any inherited constant (it removes x̃'s curvature normalisation and the "reads a multiplier" choice of DE7/CV3; it removes none of the numbers above). The inert-window count of CFG172 (§1.2) is also reported.

### 1.6 Stress-energy of the flow sector (Addendum 2)

- **No rest mass, no particle number.** The action has no term with a mass coefficient and no conserved current of the aether form (unit vector with multiplier, CFG172 §9.1). In the khronon form the Noether charge of τ → τ + const is Q; **frozen rule (CFG172 §9.1): Q ≡ 0**, the leaf constant Π₀ being fixed by the leaf average, not a charge. A configuration needing Q ≠ 0 is reported as "11C-x (khronon charge ≠ 0)", outside the owner's picture, never pooled.
- **The gate's stress-energy.** T^{flow}_{ab} ≡ −(2/√−g)δS_flow/δg^{ab}, S_flow = the θ sector + c₂ term + α_c a² term + the gate-dependent terms. New with 11C-d: the gate now makes the region kernel's energy (2α²q f(θ)) a function of the flow's θ, so an energy density ~ (c⁴/8πG)α²q f is stored in the MOND sector wherever f ≠ 0. It is a functional of the baryons (through w), not a species, and vanishes when the baryons are removed. In d2 the added term is an interaction energy of baryons with the flow (a coupling of matter to θ), not a flow mass; integrating out δθ gives an interaction energy −ζ²ε_b²/(6c₂ε_Λ) (hand; ε_Λ = Λc⁴/8πG), i.e. a pressure P = −ζ²ε_b²/(6c₂ε_Λ) applied to the baryons (§3.2).
- **Admission checks S1 (stress-energy reported), S2 (owner's picture)** exactly as CFG172 §9.1: (a) no rest-mass parameter, (b) no conserved particle number or charge (Q = 0), (c) effective density a functional of the baryons. d1 expected inside; d2 labelled "matter–flow coupling (fifth-force class)": reported, not disqualified.
- **The cold dark component** stays as in V0 / candidate B (conserved cold fluid, Ω_c h² = 0.1200, feeling u only). The flow supplies no cold mass (CFG172 §9.2's hand estimate applies unchanged: at most a G-renormalisation ~ 10⁻³). No "no-cold" arm is run for 11C-d; the CFG172 A8 run covers the flow-sector fraction, and 11C-d cites it. The double counting of the cold fluid against the region kernel's phantom (N13/L363, candidate B's max rule) is not covered (§8).

---

## 2. The tests

### 2.1 The obstruction test, re-run under the replacement (primary; exact lines)

Common grid (declared, follows DE12/DE13 so the controls can reproduce the record): isolated point-mass baryons M_b = 10¹⁰, 10¹¹, 10¹² M☉ (10¹⁴ M☉ with the κ cap reported, as DE12 G6); z = 0.25, 1, 2.5, 4; both footings (a₀ = 9.3603×10⁻¹¹ canonical / 1.1312×10⁻¹⁰ alt); gate widths w = 0.25 and 1; c₂ = 7.3×10⁻³ and 0.067 (L340's window ends); gas c_s = 37 and 117 km/s (10⁵, 10⁶ K), plus 10 km/s (CV3's cold-gas line). Gas density ρ_b = f_b(ρ_NFW + ρ̄_m) as in DE12 (its construction is re-implemented and checked to DE12's committed values in C3).

**O1 — stability (the record's criterion, on the exact second variation, never WKB only — DE13's rule).**
- (a) **Record's criterion, ported:** with the exact second variation of the reduced static energy about the solved profile (θ eliminated at fixed Π₀ and fixed leaf average; baryon perturbation δρ_b; both θ-sector and gas terms), define c_eff² = ρ_bS_eff, where S_eff is the total coefficient of (δρ_b)² beyond the gas pressure (DE12's definition; in d2 it includes the −ζ²/(3c₂ε_Λ) contact term and the gate's f″, in d1 the gate's f″ and the c₂ term). The record's line: the obstruction bites iff c_eff > c_s (T = 10⁶ K) somewhere on every z = 0.25 galaxy transition with Γ(k = 1/kpc)/H > 10³.
- (b) **Single-valuedness of the θ map:** Π(θ) at fixed r monotone on the transition (dΠ/dθ < 0 everywhere, i.e. 2c₂ > 𝓑f_θθ (+ d2 term)); an S-curve (three roots) is a first-order jump layer, which needs a gradient term (a new length) and counts as O1 FAILED.
- (c) **Stricter line, declared here:** O1 **PASSES** iff on all cells of the grid c_eff ≤ 37 km/s, (b) holds, and no negative mode fits in a half-layer window (DE13's method: negative LDL^T pivots of the discretised radial form with weights r²dr, Dirichlet windows of half the layer width, five windows). O1 is **PARTIAL** if c_eff ≤ 117 km/s but > 37 km/s somewhere. O1 **FAILS** otherwise. The cold-gas line (10 km/s) is reported as a separate row with no verdict weight.
- (d) **Where the negative stiffness lands** is reported per arm as a table: on the θ sector (absorbed if 2c₂ > 𝓑f_θθ), on the baryons (through the coupling), on a multiplier (constraint symbol zero: CV3's determinant test, using the global-operator eigenvalue count of G3b on 500 and 1000 points), on the metric (k⁴ coefficient: zero by construction since f_R = 0; reported).

**O2 — region selectivity (the record's CV4 criterion, inverted).** For isolated systems (M_b = 10⁹–10¹², z = 0.25, 1; both footings), from the solved θ(r): **PASS** iff f(r = 3r_M) ≥ 0.99 (r_M = √(GM_b/a₀)) AND f ≤ 0.01 at every point of the cosmic web (density contrast δ_b ≤ 5, including the mean), for all cells. Report |θ/⟨θ⟩ − 1| at r_M, 3r_M, r_½, the half-gate radius r_½ and the plateau's outer radius; the record's blind value is 2×10⁻⁴–5×10⁻³.

**O3 — V0's structural identities under f = f(θ).** (a) Plateau reductions: on f = 1 (all derivatives zero) the equations are CV1's, hence L361's at σ = 1, with zero symbolic residual (CV3 G5 / CV1 A3 ported); (b) homogeneous background: for w ∈ {0.25, 1} and every z ≥ 0 (also the future to E = 0.83) W(t(u_θ,bg)) = 0 exactly and all its derivatives (Lean-style argument: the same smooth-transition function; a sympy/mpmath check of t ≤ 0 with margin); (c) constraint determinants of the (Φ,u), (Ψ,w), (λ,v) blocks remain gate-independent when the θ row is added (reduced Hessian on the constraint surface, not only the diagonal entry); (d) the θ equation without the gate source reproduces CV4's c₂D_i(ND^iK) = 0 and the numbers of §0.2 to 20% (control C2).

**Verdict grammar for the obstruction (per arm; never pooled across arms; per gate width and per c₂ end, reported as cells):**
REMOVED iff O1 PASS ∧ O2 PASS ∧ O3 PASS in the same cell with the same constants; MOVED iff exactly the "moved" cases of §0.3; STILL PRESENT otherwise. A "REMOVED" cell for d2 exists only if the ζ interval defined below is non-empty.

**The ζ-interval test (d2; existence, not a fit).** For every cell, compute analytically and numerically ζ_min(cell) = the smallest ζ for which O2 holds on that cell (the gate reaches f = 1 at 3r_M) and ζ_max(cell) = the largest ζ for which O1(c) holds. The cell passes iff ζ_min ≤ ζ_max and the intersection over all cells of the grid (masses × z × footings) is non-empty for one (w, c₂). Reported: the intervals themselves and their ratio ζ_min/ζ_max (hand expectation ≥ 30, §3.2). If empty, G1–G7 for d2 are scored at ζ_min of the reference cell (10¹¹ M☉, z = 0.25, canonical), labelled "closest to passing".

### 2.2 G1–G7 (pass lines as CFG172 §2; adapted where the replacement changes what is scored)

| gate | line | how scored for 11C-d |
|---|---|---|
| **G1 law** | max |g/g_target − 1| ≤ 0.10, x = r/r_M ∈ [0.1, 30], M_b = 10⁹–10¹² (7 masses, log-spaced), point mass + h = 2 kpc exponential sphere, same constants at every mass, both footings; **P2 primary** (Door 11 erratum), ν_mono reported | solve the §1.4 system; g = −∇Φ with f = f(θ(r)). Declared here: **three reported lines.** (i) G1-strict: the whole grid with the gate as solved (outside the plateau g = g_N, deviation √(1 + x²) − 1 ≥ 10% for x ≥ 0.46 in P2 terms, so a gate edge inside the grid fails). (ii) G1-edge: the grid truncated at x_ta (the turnaround radius in both r_ta conventions of CFG48 G4, imported read-only); the position of r_½ against the record's edge closed form (DE1: r_e = v_f/(√x_c0 H₀E^(1+p))) reported. (iii) G1 against the ν_mono target (V0's own kernel). Note (declared): V0's kernel is ν_mono, not P2; the P2 mismatch is a kernel choice already in the record (CFG44: the phantom's charge function departs from P2's by R(x = 1) = 1.46, and up to 2.5 on extended profiles, under ν_mono), so a G1 failure against P2 from the kernel alone is expected and is not a failure of the θ replacement; both are reported |
| G1 mechanism | M0 prescribed = FAIL; M1 declared kernel = "P-declared"; M2 derived kernel = pass as mechanism (CFG172 §1.4) | the kernel is declared (V0's ν_mono in q) ⇒ at best M1. The θ replacement adds no kernel derivation; it may add "the gate is derived from the flow's own equation" (call it G1-gate: M0 if the gate edge is set by hand, M1 if from Π = Π₀ with a declared W and threshold, M2 never, because W and (p, x_c0, w) are declared) |
| G2 growth | linear growth within 5% of ΛCDM to k = 30/Mpc; CMB unchanged; equations stated or UNDEFINED | (i) homogeneous background off-plateau (O3b); (ii) in the web f = 0 exactly ⇒ V0's forest/growth passes carry over only if the web's θ stays below the gate (it does in d1 by construction); (iii) **d2's contact interaction acts in the web too** (the baryons' c_s² = −ζ²ε_b/(3c₂ε_Λ)·c² < 0 at every density): Γ(k)/H at the mean baryon density for k = 0.1, 1, 10, 30/Mpc and z = 0, 1, 3, 10; pass iff the baryon-perturbation growth deviates ≤ 5% (the baryons are 16% of the matter, the cold component is untouched; declared). CMB: UNDEFINED unless (iii) is stable |
| G3 reaction and energy | reaction ≤ 0.10 g_law for x ∈ [0.3, 30]; energy the θ-sector + gate store inside r_e ≤ ½M_bV_f², V_f² = √(GM_ba₀), both r_ta conventions (CFG48 G4, read-only); origin of the energy stated | reaction = every force on baryons other than −∇Φ_law: the gate's own first variation (DE12 G4: |Φ_gate|/v_f² 0.03–0.48 at the edge, record; ported to the θ-mediated form) and, in d2, the contact force −(ζc²/θ_Λ)∇ϑ h′; energy = canonical energy of the θ sector + gate + coupling |
| G4 constants | no constant beyond κ, Ω_c h² | ledger §1.5: strict FAIL by inheritance for both arms; new constants d1 = 0, d2 = 1; the ζ interval (§2.1) is the d2 tie test |
| G5 stability, Q₂, Cassini | no ghost, no gradient instability, hyperbolic, causal by criterion B (A also reported); Q₂ ≤ 5.2×10⁻²⁷ s⁻²; γ − 1 in (2.1 ± 2.3)×10⁻⁵ | (i) = O1 (the exact second variation about the static solution; ghosts: the sign of c₂ and of the θ-sector kinetic terms; characteristic cones of the khronon θ sector for criterion B); (ii) Q₂ by CFG7 H1's recipe (tide = max(|dg/dR|, g/R)) for V0's filtered law (KM3 filtered remainder, inherited; η_N = (11/3)α_c ≤ 1.2×10⁻⁸, record) and, as a labelled second row, for the unfiltered law; what the θ replacement changes: whether the gate is ON at the Sun (in d2 the local ε_b/ε_Λ ~ 10³–10⁴ makes ϑ enormous: h saturates or ϑ crosses zero, and f = 1 identically — report the sign and size of ϑ at the Sun, and that D(θ) has a pole at θ = 0 where f ≡ 1 in a neighbourhood so the gate stays C^∞); (iii) γ = 1 from the Ψ equation (Ψ = Φ) as in CV2 B1 |
| G6 preferred frame | |α₁| ≤ 3.4×10⁻⁵, also 3.5×10⁻⁵ and 2.1×10⁻⁵ (Liu et al. 2020, tighter), |α₂| ≤ 1.6×10⁻⁹ (as quoted in the task and the Door 11 file, from memory, unverified; the data chat verifies before scoring) | KM3's formulas for V0's static block (α₁ = −4α_c, α₂ = α_c(α_c − c₂)/(2c₂), record) reproduced as control C3; then re-derived with the added d2 coupling (a scalar matter–θ coupling adds a term ∝ ζ² to the effective coupling of a moving source; its size is **not** estimated here) |
| G7 a₀ vs frame speed | a₀ changes ≤ 10% for w = 0–600 km/s | V0 carries c₂ ≥ 7.3×10⁻³ ≫ 1e-4, so KM1's D = 2w²/(c²c₂) is 1.1×10⁻³ at 600 km/s (hand: 2(600/299792)² = 8.0×10⁻⁶, divided by 7.3×10⁻³); KM1's condition c₂ ≥ 2.7×10⁻⁵ (isotropic part ≤ 10%) and c₂ ≥ 8.0×10⁻⁵ (D itself) are satisfied. New for 11C-d: the moving-source dipole in θ (CV4 K2: δK = ωG₁ψ_N) shifts the gate's edge by a fraction δ ≈ (dipole/θ deficit); scored as the relative edge shift at 600 km/s (declared: pass ≤ 10%). The a₀ value itself is not in the gate |

Diagnostics (reported, not gates): D1 flat versus H(z)-tracking a₀: V0's a₀ is a constant (rule T ties it to Λ, not to θ), so D1 is FLAT; but the gate's edge x_c,eff(z) evolves (DE1: flagship survives only below M_*(z), which falls as E⁻⁸ for p = 1) — reported as in DE1 for the θ-gate; D2 lensing = dynamics (Ψ = Φ, slip ≤ 3.7×10⁻⁸ / 2.9×10⁻⁷ record for the MOND-sector gate; here f_R = 0 so gate slip is expected 0, to be checked); D3 G1-river = 0.

---

## 3. Hand ESTIMATES (written before any script; kept whatever the scripts show)

### 3.1 d1 — gate-sourced compaction

**T-d1 (structural statement, hand; a hypothesis to be tested).** From §1.3, on any plateau (f′ = 0, C^∞-flat) Π = −2c₂(θ − ⟨θ⟩) = Π₀, so θ takes the same value on the bound plateau and on the web plateau; both are that leaf constant. The gate variable u_θ is therefore the same on both plateaus, but a region gate needs f = 1 on one and f = 0 on the other. Hence **d1 cannot be a region gate**, for any smooth W and any 𝓑 ≥ 0: the only place θ deviates from the constant is where f′ ≠ 0 (the transition layer itself), and it returns to the same constant on the other side. This holds under (H-i) and (H-ii) of §1.3. It is stronger than CV4 (which was perturbative: K ≈ 3H to 10⁻²–10⁻⁴): it says the varied gate reproduces CV4's blindness structurally, not by size. Numerically (hand): the layer bump δθ/⟨θ⟩ ≈ 2α²q f′ t_θ/(2c₂) ≈ 3×10⁻⁶ at z = 0.25 (M_b = 10¹¹, edge y ≈ 9×10⁻⁵, q ≈ (4/3)y^(3/2) ≈ 1×10⁻⁶) and ≈ 2×10⁻³ at z = 4 (M_b = 10¹⁰, y ≈ 0.018, q ≈ 3×10⁻³), against the 0.5–0.9 depletion the gate needs.
**The θ sector's own stiffness absorbs the gate's second variation** (hand): the single-valuedness condition 2c₂ > 𝓑f_θθ reduces (𝓑 ≈ 2α²q, W″max = 9.84, W′max = 2 [hand: W(t) = g(t)/(g(t) + g(1 − t))]) to c₂ ≳ 0.9q (z = 0.25) and 0.9–1.9q depending on z; with q ≲ 3×10⁻³ (10¹⁰, z = 4) and ≲ 0.06 (10¹², z = 4, hand deep-MOND estimate) this holds at c₂ = 7.3×10⁻³ except at the highest z and mass (there short by ≈ 8× at c₂ = 7.3×10⁻³ and passing by ≈ 1.2× at 0.067) — a small and uncertain window. Reading: **d1 is stable (mostly) because it is blind**: a "moved" outcome at best.

### 3.2 d2 — explicit compaction (the pincer, hand)

Integrating out δθ at fixed Π₀: δϑ = −ζ(ε_b − ⟨ε_b⟩)/(3c₂ε_Λ) (lin), interaction energy E_int = −ζ²ε_b²/(6c₂ε_Λ), pressure P = E_int, **c_s²/c² = −ζ²ε_b/(3c₂ε_Λ)** (imaginary sound speed: an attractive contact interaction, independent of the sign of ζ and of the gate). Requiring the gate to turn on where ε_b is (the depletion of §1.1): |δϑ| = Δ ≡ (1 − θ/⟨θ⟩)·⟨θ⟩/θ_Λ, with ⟨θ⟩/θ_Λ = E/√Ω_Λ (hand table for the ON point, t = ½: z = 0: Δ = 0.56; 0.25: 0.71; 1: 1.44; 2.5: 3.8; 4: 6.9). Eliminating ζ:
  **−c_s²/c² = 3c₂Δ²(ε_Λ/ε_b)** — independent of ζ and of the coupling's normalisation (a pincer between "the gate can reach the plateau" and "the baryon fluid is stable").
Hand numbers (z = 0.25; ε_b/ε_Λ from 0.14, the cosmic mean baryon density, to 14, a baryon overdensity of ~100; c₂ = 7.3×10⁻³ up to 0.067): |c_s|/c = 0.028–0.28, i.e. **≥ 8×10³ km/s at c₂ = 7.3×10⁻³**, against gas at 37–117 km/s (a factor ≥ 70). To bring |c_s| under 117 km/s requires c₂ ≲ 1.4×10⁻⁶ (at ε_b/ε_Λ = 14), 5×10³ below L340's floor (and 20 below KM1's 2.7×10⁻⁵ G7 line). ζ itself (hand, from ζ = 3c₂Δε_Λ/ε_b at c₂ = 7.3×10⁻³, Δ = 0.71): about 1×10⁻³ at ε_b/ε_Λ = 14 to 0.1 at 0.14, and then −c_s²/c² = ζΔ.
Also: d2 makes the compaction a local algebraic response to ρ_b, so the gate reads baryon density (a density gate in disguise): O2 can pass, but the second variation then lands on the baryons exactly like CV3's reading A / A = 1 control (c_gate 18–93 km/s at z = 0.25 / 2.5, unstable for gas colder than that) **plus** the negative contact term above. Reading: **d2 is selective and unstable**; the negative stiffness moves from the gate-reading fields to the baryons through the coupling. d2(sat) reduces the effective coupling as |ϑ| grows (h′ = (1 + |ϑ|)⁻²) and needs a larger ζ for the same depletion, so its pincer is expected to be worse by a factor of order (1 + Δ)² at the plateau (hand, not derived).

### 3.3 Probability table (subjective; F = fail, P = pass, PT = partial, U = undefined)

| item | d1 | d2(lin) | d2(sat) |
|---|---|---|---|
| O3b homogeneous background off-plateau (w = 0.25) | P 0.97 | P 0.95 | P 0.95 |
| O3b, w = 1 | P 0.9 (t_bg ≤ 0 for every z ≥ 0) | P 0.85 | P 0.85 |
| O3 plateau reductions / constraint symbols | P 0.85 | P 0.8 | P 0.8 |
| O2 region-selective | **F 0.93** (T-d1) | P 0.85 | P 0.75 |
| O1 stable (line (c)) | P 0.55 (stable because blind) | **F 0.93** | **F 0.93** |
| ζ-interval non-empty | n.a. | **F 0.95** (ratio ≥ 30) | F 0.97 |
| **Obstruction verdict** | MOVED (blind) 0.85; STILL PRESENT 0.10; REMOVED 0.02 | STILL PRESENT 0.92; REMOVED 0.03 | STILL PRESENT 0.94; REMOVED 0.02 |
| G1-strict | F 0.98 (gate never on; g = g_N beyond r_M) | F 0.7 (edge inside the grid at many masses) | F 0.8 |
| G1-edge vs ν_mono | F 0.9 (gate off) | P 0.5 | P 0.4 |
| G1 vs P2 (kernel mismatch inherited) | F 0.8 | F 0.8 | F 0.8 |
| G2 (web instability of the contact term) | P 0.8 (gate off in web) | **F 0.9** | F 0.85 |
| G3 reaction | P 0.8 | F 0.7 (contact force) | F 0.6 |
| G4 strict / new-constant count | F (inherited) / 0 new | F / 1 new | F / 2 new (ζ, shape) |
| G5 | U (depends on O1) 0.5; P 0.4 | F 0.9 | F 0.9 |
| G6 | P 0.8 (V0's window) | U 0.5, F 0.3 | U 0.5, F 0.3 |
| G7 | P 0.75 | P 0.6, U 0.3 | P 0.6, U 0.3 |

**Overall.** P(the θ replacement removes V0's obstruction — REMOVED verdict in any arm) ≈ 0.04. P(scoped no-go for all arms) ≈ 0.9. The record's dilemma (selective ⇒ unstable, stable ⇒ blind) is expected to survive in the form "d1 blind, d2 unstable". Assumptions these estimates rest on (each unverified until phase 2): H-i and H-ii (the θ equation of §1.3 is the whole equation); the deep-MOND estimate q ≈ (4/3)y^(3/2) at the edges; the density scale ε_b/ε_Λ ~ 0.14–14 at the gate edge; DE12's edge construction; that a contact interaction of this sign is an instability of the baryon fluid at scales above the gas Jeans length (as in the record's CFG172 11C-c hand result).

---

## 4. Controls

**Reproduction controls (main run; a failure is kept, disclosed, exit 1):**
- C1 CFG44 identities for P2 (point mass M_c = M(√(1+x²) − 1); target and ν_mono via read-only import of `Bcommon.py`) to 1e-6.
- C2 CV4 reproduced: the θ equation without the gate source (and without d2) gives K ≈ 3H with |K/3H − 1| within 20% of the record's 2×10⁻⁴ / 6.5×10⁻⁴ / 1.9×10⁻³ / 4.8×10⁻³ (K3 cells), the harmonic statement c₂∇²δK = 0 symbolic, and the d1 arm with 𝓑 → 0 collapses onto it.
- C3 KM3 formulas (α₁ = −4α_c, α₂ = α_c(α_c − c₂)/(2c₂)) and KM1's D/3 numbers (0.114 at c₂ = 2.5×10⁻⁵, 0.285 at 10⁻⁵, w = 620 km/s; record; hand check of the prefactor: 2(620/299792)² = 8.55×10⁻⁶) as controls for G6/G7.
- C4 DE12 reproduced: this lane's re-implementation of the transition and c_gate machinery, run with V0's ORIGINAL gate (reading A+, density/phantom-sourced, w = 0.25), reproduces DE12's committed numbers (min c_gate 1526 km/s and min Γ/H 2.0×10⁴ over the z = 0.25 galaxy cells; G3's A = 1 values 18.4 and 93.4 km/s) to 2%. This is the pre-declared positive control of the obstruction itself.
- C5 CV1 plateau identities (A2, A3, A5 numbers: force to 1×10⁻⁴ in the plateau; σ = 1 layer numbers 1.4 and 0.8 g_N at 1/m = 100 and 500 kpc) to the record's tolerance.
- C6 the DE1 edge closed form r_e = v_f/(√x_c0H₀E^(1+p)) against the V0 gate at z = 0.25 (record: L352 Z6 z = 0 edges 1.11/0.99/1.73/1.55/2.34/2.10 Mpc reproduced to 1%).
- C7 T1: any C² flat-flat gate has f″ of both signs (numeric check on W: W″max = 9.84 at t = 0.218, min −9.84 at t = 0.782, hand).

**MUTATE controls (`MUTATE=<name>`; each flips a load-bearing cell; the control must make its named claim fail and the script exit 1; outputs named by mode):**
- **M1 restore the original gate.** Replace u_θ by V0's u (reading A+, density and phantom). O1 must return to STILL PRESENT at DE12's values (c_gate ≥ 1500 km/s, Γ/H ≥ 2×10³ at z = 0.25), O2 passes (a prescribed-like selective gate): the record's dilemma reproduced in this lane's own numerics. Flips the O1 cell of d1/d2 from the replacement's value to the record's value.
- **M2 drop the θ coupling.** ζ = 0 in d2 (≡ d1). O2 must FAIL in every cell (blind), and the ζ-interval test must return "empty by construction". Flips O2.
- **M3 flip the sign of the coupling.** ζ → −ζ (θ increased where matter is): the gate can never turn on, O2 must FAIL and G1-edge must fail at every mass; O1's c_s² is unchanged (∝ ζ²), which is the point: the pincer is not about the sign.
- **M4 c₂ → 0.01c₂ (ζ re-solved for the same gate depletion).** d2's |c_s| must drop by 10 (∝ √c₂) but stay above 117 km/s in at least one cell of the grid (expected: 8×10² km/s); if it does not the pincer's c₂ dependence is not load-bearing and that is declared. Also flips G7 (KM1's D rises to 0.11: F) — a real cost.
- **M5 prescribed gate (do not vary f).** Remove the f′ terms from the τ equation (the record's data-pass mode): O1 must PASS trivially (no stiffness at all) and O2 PASS (the mask is given): shows the obstruction is a property of varying the gate, and that the test discriminates.
- **M6 background not off-plateau.** Drop the leaf-mean offset from D (u_θ = (H₀/H)^{2p}, i.e. Ω_Λ(θ)/Ω_Λ,0 alone): O3b must FAIL for w = 1 (t_bg > 0 at z = 0: hand, s = 0.4 ⇒ t = 0.2) and the CV2 B3 identity (FRW = GR) must fail.
- **M7 flip the sign of c₂ (a ghost θ sector).** O1 must FAIL in every cell with the ghost flag set (kinetic sign), and G5 flips.
- **M8 give the flow a charge (§1.6).** Q ≠ 0 in the khronon form: S2(b) must flip to F and an a⁻³ term must appear in the FRW background.

A MUTATE run that does not bite is a declared control failure, kept.

---

## 5. Declared choices; and whether the θ replacement escapes each record kill (hypotheses to be tested)

**Declared choices.** (1) The gate variable u_θ (§1.1): the expansion deficit relative to the leaf mean with V0's z-scaling; V0's (p, x_c0, w) unchanged; the z-independent variant is a labelled sensitivity. (2) d2's coupling form ζ(ε_b − ⟨ε_b⟩)h(ϑ) with h lin / sat; ζ is not tuned (interval test). (3) Kernel ν_mono (V0's declared kernel) with P2 as the Door 11 target; the P2-in-q variant is a sensitivity. (4) S = 1 in static solves; ξ inherited. (5) σ = 1 (the record's construction); the σ = 0 hard-edge variant is not run (edge-sensitive observables are not scored here) and this is a declared restriction. (6) c₂ at the two ends of L340's window; the leaf-averaged θ term (L350's G5 construction), so the Planck ceiling on c₂ (0.6–2.9×10⁻³, record) is not imposed; reported. (7) G1 is scored on the baryons' acceleration from the solved fields (the river reading is vacuous for a flow at rest, CFG172 §1.3). (8) O1's "removed" line (c_eff ≤ 37 km/s) is stricter than the negation of DE12's line; both are reported. (9) Isolated point-mass baryons for the gate transitions (DE12's construction), exponential sphere for G1. (10) Hand arithmetic (§0, §3) is unverified until phase 2.

**Does the θ replacement escape each prior kill? (hypothesis, to be tested; not a claim).**

| prior kill (record) | does the replacement escape it? |
|---|---|
| **FC-KH** (yq)′ ≥ 0 theorem, exponential khronometric MOND unstable (N6) | Not touched: V0's MOND sector lives on its own field w (its own AQUAL-type q), the record's FP7 R7m/C-H/K escape ("(yq)′ obstruction absent"), and 11C-d does not add an a²-channel function of the khronon. Expected: not applicable, exactly as for V0. Phase 2 checks the khronon's radial principal coefficient with the gate term present (the gate adds a function of θ, not of a) |
| **KM1 / L333** (a₀ tracks CMB-frame speed unless c₂ ≫ 1e-4) | V0's window c₂ ≥ 7.3×10⁻³ ≫ 10⁻⁴ satisfies it (D = 1.1×10⁻³ hand). New risk: the θ dipole for a moving source (CV4 K2) shifts the gate edge; scored in G7. Expected to escape for the a₀ value; the edge-shift size is unknown (hand: small because δK/3H ≲ 5×10⁻³) |
| **AeST v9 PPN kill** (N7: α₁ = −2(K_B + 2), FC-AeST α₂) | A different action (vector + scalar); V0's PPN is KM3's (α₁ = −4α_c, α₂ = α_c(α_c − c₂)/(2c₂), α_c ≤ 3.2×10⁻⁹). Not applicable to d1; for d2 the coupling's contribution to α₂ is unknown (G6 = U) |
| **Single-metric slip-lock / elliptic pincer** (N1) and **foliation theorem** (N5) | V0 is a preferred-frame action that "accepts the foliation" (N1/N5 escape column); the replacement keeps one metric and the khronon. The gate reads θ, so f_R = 0 and gate slip should vanish (DE12 slip ≤ 3.7×10⁻⁸ already tiny). Expected to escape (by inheritance) |
| **V0 obstruction (DE12/DE13, XR15, CV3 G4)** | The hypothesis under test. Expected NOT to escape: d1 by T-d1 (blind), d2 by the pincer −c_s²/c² = 3c₂Δ²ε_Λ/ε_b |
| **DE7 T1 / any smooth gate** | Structural: T1 is about the gate's shape and is not removed by changing the variable it reads; it only moves where the negative stiffness lands (θ, baryons, multiplier, metric). This is the record's own lesson (N14) and is the reason for O1(d) |
| **CV4 blind K-only gate** | Attacked directly: d1 adds the gate source (T-d1 says no help), d2 adds the matter source CV4 excluded by hypothesis (pincer says no help at c₂ in the window) |
| **N15 θ-gate mirror lemma** (Brown–Schutz dust θ_b gate: ghost pole 1/k_g = 132–1756 kpc, Γ = 0.7–4.7 H on 24/24 layers for saturated gates; unsaturated costs SPARC; filtered needs R ≥ 0.26–7.7 Mpc) | A different variable (the baryons' dust θ_b, not the flow's θ) but the same class of statement (the gate term is largest where MOND is on). Expected to transfer in spirit to d2 (the gate then reads baryon density); untested here |
| **FL2 V3's safe convex gate** | Unavailable: a gate that must be on at one plateau and off at the other cannot be convex (T1) |
| **N21 edge / N12 web external field** | Inherited unchanged (a density-like edge; the kernel's web blindness via M² is V0's). Not scored here |
| **N19/κ, N18 ξ** | κ = ½ FITTED, ξ irreducible: inherited |
| **GW170817** | c₁₃ = 0 built in (CFG172 §0.6); the gate does not touch the tensor sector. Not applicable |

---

## 6. Script plan

Lane directory `campaign_fresh_gravity/CFG172D_door11C_d/` (created by the orchestrator at commit; in phase 2 the scripts are written in the scratch dir first). Names `CFG172D_*`. Repo root from `ZF_REPO` or by walking up from `__file__`; every printed path is `<repo>/…`; no absolute home path is ever printed or stored. Each run < 15 min; numpy/scipy/sympy/mpmath only. **Exit convention:** the main run exits 0 if every reproduction control and internal identity passes (gate verdicts P/F/PT/U are results, not exit codes); a control failure exits 1 and is kept; `MUTATE=<name>` exits 1 when the control bites (the claim it targets fails as required) and writes `*_MUTATE_<name>.out/.json`; a MUTATE run that does not bite is a declared control failure.

| script | content | lines scored |
|---|---|---|
| `CFG172D_common.py` | constants (both footings; G = 4.30091727e-6 kpc (km/s)²/M☉; c = 299792.458 km/s), read-only import of `Bcommon.py` (P2, ν_mono, exponential sphere), W and its derivatives, u_θ, cosmology (h = 0.6736, Ω_m = 0.3153, Ω_b h² = 0.02237, Ω_c h² = 0.1200; from memory, unverified), the repo-root helper, DE12's gas and NFW construction (re-implemented) | — |
| `CFG172D_A1_theta_equation.py` | sympy: the τ-variation of V0 with f = f(θ) from the covariant brace (H-i, H-ii checked); Π = Π₀; T-d1 as a symbolic statement; the d2 reduction, the pincer formula, the interaction energy; CV4 control C2; plateau reductions and O3(a,b,c); C7 | O3, T-d1, §1.3 |
| `CFG172D_A2_static_solve.py` | radial fixed-point solve of the §1.4 system for d0, d1, d2(lin), d2(sat), point mass and exponential sphere, 7 masses, both footings, z = 0, 0.25, 1; branch listing for Π(θ); G1 (three lines); O2; D3; C1, C5, C6 | G1, O2 |
| `CFG172D_A3_obstruction.py` | the exact second variation and c_eff, single-valuedness of Π, the half-layer negative-mode count (DE13's LDL^T method), the global-operator eigenvalue count (G3b), the O1 table, the per-arm landing table, the ζ-interval test (ζ_min, ζ_max, their ratio), C4, M1/M5 | O1, ζ-interval |
| `CFG172D_A4_gates_G2_G5_G6_G7.py` | G2 (background off-plateau, web contact instability Γ(k)/H), G5 (Q₂ by CFG7 H1, ϑ at the Sun, characteristics for criterion B), G6 (KM3 re-derivation with and without the d2 coupling), G7 (KM1-style moving-source solve for the gate-edge shift), C3 | G2, G5, G6, G7 |
| `CFG172D_A5_reaction_energy_stress.py` | G3 (gate force and contact force, canonical energy in both r_ta conventions, CFG48 read-only), stress-energy S1/S2, Q = 0 check, M8 | G3, S1, S2 |
| `CFG172D_verdict.py` | reads the JSONs and prints the O1/O2/O3 table, the arm verdicts (REMOVED / MOVED / STILL PRESENT), G1–G7 per arm, the ζ intervals, the diagnostics; no physics | — |

MUTATE modes by script: A1: M6, M7; A2: M2, M3; A3: M1, M4, M5; A4: M4 (G7 side); A5: M8.

---

## 7. What counts as passing G1 as a mechanism; what a scoped no-go looks like

- **A pass of G1 as a mechanism** (CFG172 §7 adapted): V0's law inside the plateau (ν_mono, P-declared; M1) with the gate region determined by the flow's own θ equation (G1-gate M1 or better), on the whole G1 grid (G1-strict ≤ 10%, or G1-edge with the edge at or beyond x_ta), for all masses and both profiles with the same constants — **and** the obstruction verdict REMOVED (O1, O2, O3 in the same cell). That is a pass of "the replacement removes the obstruction" and it is NOT a derivation of the kernel (M2 never: W, (p, x_c0, w) and ν_mono are declared). **An independent re-derivation is required before anything is reported** (the θ equation from V0's action; the O1 second variation; the O2 solve), and the pass is stated with every gate that still fails. A "MOVED" or "STILL PRESENT" verdict is not a pass.
- **A scoped no-go looks like:** "within the frozen class (V0's action with f = W(t(u_θ)), arms d1, d2(lin), d2(sat); static spherical weak field; c₁₃ = 0; ν_mono in q (P2 as target); rule T; c₂ in L340's window), no parameter point makes the gate region-selective (O2) and stable (O1) at once: d1 fails O2 by T-d1 (θ takes one value on both plateaus, or bump ≲ 2×10⁻³ against 0.5), d2 fails O1 through c_s²/c² = −3c₂Δ²ε_Λ/ε_b (≥ 8×10³ km/s at the window's floor), and the ζ intervals do not intersect; the hypotheses are H-i, H-ii, the cited record values, and the grid." Nothing here would say the theory is closed, that the timelike-flow reading is refuted outside the class, that a nonlocal gate (CFG48 G6's counter-case: 48/48 layer×width cases with no negative mode; a new length) could not work, or that any data favour the framework.

## 8. What is NOT covered

Non-spherical baryons (discs; the exponential sphere is 3D spherical); the σ = 0 hard-edge layer and edge-sensitive lensing (KiDS, Harvey: the record's unscored σ = 1 layer stays unscored); nonlocal or filtered gates (a new length ξ_gate; CFG48 G6's nonlocal enclosed-mass Volterra gate is the record's positive counter-case and is not in the frozen class); a dynamical gate field χ with its own stiffness (CV6, never run in the record; not run here); a gradient repair (DE13: not allowed, adds a length); the non-perturbative "maximal leaf" branch of CV4 beyond what d2's algebraic θ reaches (d2's solution for large |ϑ| is a nonlinear response, not a maximal-leaf construction; near θ = 0 the variable D has a pole where f ≡ 1); the khronon's spin-1 (twist) mode and c₁₃ ≠ 0 aethers; time-dependent, merger, cluster (κ-cap layer reported as in DE12 G6 only), and nonlinear-cosmology regimes; Boltzmann-code CMB (UNDEFINED); the external-field effect; the CDM–phantom double counting inside galaxies (candidate B's max rule; N13/L363); relativistic strong-field regimes beyond the weak-field static limit; lensing except diagnostic D2; a matter coupling to θ other than d2's (coupling to the baryon trace, to dust θ_b (N15), to the dark component); a "no-cold" run (cited to CFG172 A8); quantum and UV questions. Literature statements (Skordis–Zlosnik, Zlosnik–Ferreira–Starkman, Blanchet–Skordis, Yagi et al., Shao–Wex, Liu et al. 2020, Mukohyama) are from memory or as the record cites them, and none was re-read.

---

Hash of this file is reported by the writer after the last edit; a later change would void it.
