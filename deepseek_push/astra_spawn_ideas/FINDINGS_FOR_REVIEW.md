# FINDINGS FOR REVIEW — astra_spawn_ideas (2026-09-28, 121 hash-verified / 2000)

Legit claims needing attention from a deeper agent. Every item below is Lean-certified
(zero sorry, axioms ⊆ {propext, Classical.choice, Quot.sound}) unless flagged; every
numeric is an ACTUAL residual from an executed run (see the cited run dirs). κ = 1/2 is an
ADOPTED input throughout. Both a0 footings (9.3619e-11 / 1.1279e-10 m/s²) carried separately.

## A. The κ status — now a theorem, not a gap
1. **Continuum theorem (AS138.C01, run AS138.C01-20260928T1950Z-dsv4f-hermes):** total-Ward
   conservation (matter + heat + U(1) + four-form vacuum + terminal BC, ten-premise assembly
   at pin b8c04d4e) reduces to 0 = 0 identically in the couplings: conservation CANNOT force
   κ. Witness family κ(r) over r ∈ {1,2,4,8,16,64}: {1.3894, 0.9911, 0.7039, 0.5000, 0.4989,
   0.3532, 0.1767}, all conserving identically; κ(8) = 0.498878447859 ≠ 1/2 is a full
   counterexample to forcing. → κ = 1/2 is a DATUM, and the framework's content is exactly
   one ratio. The "why κ" question is not a derivation gap but a selection-mechanism gap.
2. **The ratio is pinned and arithmetically exact (AS651, AS138.C01):**
   κ = 1/2 ⟺ Z/β² = 8 − 2b = 7.9639892129110, with b = j_sat/8π = 0.0180053935445 read off the
   pinned k04 flux coefficient (j_sat = 0.45252489667513); consistency |b − (8−r*)/2| ≤ 6e-61.
3. **Every four-form selection channel is CLOSED (each a full run):** metric variation (AS651:
   ε_vac = +(Z/2+bβ²)q² > 0 — AS068's sign obstruction repaired; B-ii/B-iv fail), flux EOM
   (AS652: the integration constant makes a0 ENVIRONMENTAL — switch-off g_* = 155.2/177.4 a0;
   k04's s₀=1000 "0.0000" row is a spurious fixed point — but does not fix the ratio),
   homogeneity (AS653: amplitude-independent iff n = 2m), gauge/DOF (AS658: exactly
   gauge-invariant, ZERO propagating bulk modes — count 4−3−1), volume (AS669: blind in both
   regimes). **Next door (registered): AS651.C02 boundary ensemble — see in flight below.**
4. **Do NOT re-derive κ from symmetries.** The continuum theorem is the reason.

## B. Derived observables (falsifier-ready, not yet data-tested)
5. **G_N is derived (AS226):** G_N = G_bare/c_N = G_bare/(1−α/2) from the reciprocal high-k
   limit; mode coefficient 4πG_N to 4.4e-16; GR limit α→0; consistent with FINAL_ACTION
   eq. (18) G_cosm/G_N = c_N. Open: α is a one-parameter family — needs an independent
   same-action observable to fix c_N ∈ (0,1) (children AS226.C01/C02 written).
6. **EFE tensor branch-discriminating (AS245):** C_L = (ν−1)+y·ν′ < C_T = ν−1 everywhere;
   deep limit C_L/C_T → 1/2 EXACT with 2C_L−C_T = c−1 taking distinct values per branch:
   Q −1, RAR/MONO −1/2, EXP −3/4, MU2 −5/8. One deep-EFE slope measurement identifies the
   law. Sphere factor exp(−ξ²/R²) exact. Open: near-field finite-curvature (θ-tilt) case.
7. **Lensing slip linear in the filter scale (AS228):** lapse ΔΦ = 4πG_Nρ_b + S·div[(ν−1)p];
   spatial Δψ = 4πG_N·ρ_slip; slip_max = 1.04e-5 at ℓ=0.04 (slip/Φ = 6.7e-2), ×10.08 per
   decade of ℓ. Ψ=Φ-before-varying FAILS at 8,749× the noise floor → anisotropy is real.
   Measurable: slip ∝ ℓ with a scaling law in the filter scale.
8. **Vacuum lensing is O(z⁴) (AS229):** F(t) = 1+(t+1/t−2)² gives F′(1)=F″(1)=F‴(1)=0,
   F⁗(1)=24; projected ΔT^ij = +4V₀⟨z³⟩_h z h^ij/N leading term; the OLD 1/t_c floor is
   FALSIFIED (F_old′(1) = −1 ⇒ linear susceptibility, amplitude 0.5000 vs 1/32 — NEG1 fired).
9. **β = 1 in the static window-vacuum (AS232):** the α-deformation sits in the spatial shell
   (ψ₂/U_N² = −(6+α)/8, exact Einstein −3/4 at α=0); gauge identity β = 1 + φ₂/U_N²
   Lean-certified. Static-sector PPN β matches GR — constraint, not freedom.
10. **α₂ extraction is OBSTRUCTED as pinned (AS234, rescued run):** order-v² E_A consistency
    residual R = −8ρ/D with D = 28 at the branch point ⇒ R = −2ρ/7 ≠ 0; the pinned
    rest-isotropic config cannot carry the conserved moving-source stress at v². Same-action
    α₂ needs a pin/tie relaxation — named, untried.
11. **Shapiro delay from the same action (AS247):** Δt = (1/c³)∫−(Φ+Ψ)dl; heat-filter factor
    1/Q−1 = 1.00% EXACTLY as analytic; deep-band conditional +2.94e8 s ADVANCE (canonical
    footing) — conditional on two open hypotheses (H1/H2), do not cite as prediction.

## C. Phantom equilibrium — pinned from every side (conditional deep sector)
12. ρ = A/r² is GLOBALLY non-normalizable for every γ (AS078): finite-domain profile fixed by
    equipartition M_ph(<r_M) = M_b; v_c² ≡ C only as r_in→0 (deviations 0.9938/0.9319/0.3871).
13. **The half factor is EXPLAINED (AS087):** zero surface pressure ⇒ σ² = (C/3)F, with
    pressure σ² = (C/2)F; ratio 3/2 exact for every shell (Lean); C/2 exact only at the
    r_in→0, R = r_M consistent truncation. Virial chain AS083/084: two-boundary identity exact,
    one-boundary misreading fails by exactly 4πr_in³P(r_in).
14. Entropy concavity of the imposed well is exact (AS079); the u⁻² ansatz is NOT stationary
    against the full MONO-deep kernel (residual 0.051 @ 10 r_M) — the kernel transfer is the
    licence gap, EVERYWHERE. ξ (filter scale) remains unpinned; see AS651.C01 in flight.

## D. Action spine (structural, derived not assumed)
15. Matter Ward: ∇·T^{μν} = 0 on shell; S_b contains NO a0/κ/G (AS137) — both footings
    identically. Heat diffeo Ward exact at jet level, endpoint multipliers load-bearing
    (AS138: omitting leaves N·M = −57/50 ≠ 0). U(1): div J_φ = +E, div J_χ = −E, div J_total = 0
    (AS147). Dirac–Bergmann: exactly 18 primary constraints = the static fields; metric-trace
    sector adds NONE; r-as-time contamination shifts 18→10 (AS151).
16. Terminal heat BC: L_b = −R_W, R_W = −div_N(fJ_p+ℓa) + ℓN⁻¹Δ_h(Nf) (AS133). Gate→lapse:
    δ_lnN S_gate = C_N∫N√h φ[G(Y_h) − ℓΔ_hW_b], no-G″ structural (AS145). CRITICAL STRUCTURE:
    the compensator's lapse source (AS132) is the SAME operator (Laplacian-of-W) as the gate's
    — two functionals may merge into ONE sink at the MONO closure cell. Do not treat them as
    independent.
17. Carrier Legendre without freezing t_c is exact; σ_H + σ_R = 0 identically (AS142).
    Lapse density rho_R = t K_d + W_exc/t + V₀F(t) exact (AS127). Reciprocal lapse density:
    ρ_R = −(N√h)⁻¹ δS_R/δln N (AS127).
18. Metric variation of the intrinsic Laplacian: δΔu = −k̂^ij∇_i∇_j u − (∇_i k̂^ij − ½h^jm
    ∂_mT)∂_j u (AS206); heat-semigroup first metric derivative bounded, mode kernel
    I(λ,μ) = (e^{−bλ}−e^{−bμ})/(λ−μ), M = 0.4603, two-leg AM–GM allocation r-uniform (AS208).
19. Wave-health: every characteristic cone hyperbolic, dτ-contracting, superluminal carrier
    1.4286c PASSES criterion B while a metric-cone veto wrongly rejects it (AS215). Ghosts
    fail hyperbolicity (discriminant −2.04e-2). Curved-leaf heat-force bound r_curved = 0.0645
    (≥15× margin) on S³ (AS204).

## E. Currently in flight (do not duplicate)
- AS651.C01 (MONO-kernel transfer of b: does 8−2b shift off 7.96399 on the operative kernel?)
- AS651.C02 (boundary-ensemble origin of q₀ — the only surviving κ-selection mechanism)
- AS500.C01 (gate-5 matter-only Ward atom: decoupling (a) or closed-form cross-source T (b))
- Seeds: AS235 (α₃), AS238/239 (GW dispersion/propagation), AS240 (GW transport, on disk),
  AS263 (projector commutator), AS285 (growth equation), AS252 (cosmological G, on disk),
  AS233 (preferred-frame, on disk), AS236 (cosmo vs local G, on disk)

## F. Interaction rules for reviewers
- Ratios: 8−2b = 7.9639892129110 is THE number. Any claim that κ follows from symmetries
  must refute the continuum theorem first (its witness family and Lean certs are in
  results/AS138/AS138.C01-20260928T1950Z-dsv4f-hermes/).
- The EFE deep-limit numbers are branch FINGERPRINTS: do not average across branches; the
  distinction IS the result.
- Every transfer claim (phantom ↔ MONO kernel, interior ↔ exterior, β window ↔ tensor
  sector) must name ξ and the filter; transfers without ξ are the campaign's single most
  repeated invalid move. Kill it on sight.
- Lean hard bar: zero sorry, axioms ⊆ {propext, Classical.choice, Quot.sound}. Certs compile
  host-only from fable_independent_2026/lean_2026. Chain registry:
  deepseek_push/astra_spawn_ideas/LEAN_CHAIN_REGISTRY.md (170 cert files / 1505 theorems).
- Nothing is deleted; superseded work is superseded by new commits, never by removal.