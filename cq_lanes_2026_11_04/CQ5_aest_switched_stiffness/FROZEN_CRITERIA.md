# CQ5_aest_switched_stiffness: FROZEN CRITERIA, committed alone before any script or number

κ = ½ FITTED; not theory closed. Footings never pooled (canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s²). No particle, no cold sector (it stays retired). Nothing here says the data favour the framework. Owner's go for action-building lanes is on record for this lane (the 11-01 rule). This lane adopts nothing.

## Question
AeST (Skordis & Złośnik 2021, PRL 127, 161302) fails Cassini in AX1 (`rebuild_2026_10_22/AX1_action_for_law/AeST/`: Q2 2.44–5.15× Hees; Saturn 1.34e4 / 1.62e4× its bound; G2c F). v3s passes with the switched stiffness −(γ_L/2)[max(D·P, 0)]², L★ ≥ 21.7 / 22.9 pc. **Does grafting that switched stiffness onto AeST's scalar give one theory that passes the Solar System, leaves AeST's cosmological background unchanged, and keeps AeST's static galaxy limit?**

## Record check (done before freezing): PARTLY ON RECORD, not done as one lane
- C1 (`covariant_push_2026_10_22/C1_aest_embedding`): AeST's static limit is PAPER49's Lagrangian with K P_i = q_i^μ∂_μφ ≈ ∂_iχ + Q₀a_i, Φ = Ψ; AeST has γ_L ≡ 0; the missing term is −(γ_L/2K²)(q^{μν}∇_μ∇_νφ + θ𝒬)², K = 8πG̃/(2−K_B) = 4πG. **Unswitched.**
- C3 (`C3_scale_map`) V1 = AeST + that term at AeST's own (physical) curl stiffness: Cassini Q2 PASS at 24/50/90 pc, planets GM/L★², FRW linear term k⁴χ² ~1e-11. **Unswitched; no G2c, no health.**
- v4 = AeST + γ_L + capped F (THEORY_V3_DRAFT §1b): I1 ILL-POSED wherever the aether twists; C7 FRW runaway for the Cosh dust shape (a K choice, not the stiffness); M1 R2. **Unswitched.**
- AS3 Part 1: AeST-type moving-source PPN (two branches); AS3 Part 2: closed-form screened Q2 for a curl-free scalar with (D²χ)², at the floors and 90 pc.
- X3 D2: for C6's solution, D·P > 0 everywhere within 1 kpc of the Sun (margin ≥ 1.8e4).
- AX1 AeST criteria say "its stiffened, switched form is v3s". That is a static-limit identification; v3s is built on the khronon, not on AeST's twisting aether, so AeST's PPN, health and cosmology were never graded with the switched term.
- **New here:** the switched graft as one theory, graded on Q2, planets, γ − 1, G2c, FRW background, law, c_T and health together, with AX1's engine.

## The grafted action (fixed now)
S = S_AeST − ∫d⁴x √−g (γ_L / 2K²) [max(D·V, 0)]², with V^μ ≡ q^{μν}∇_νφ, q^{μν} = g^{μν} + A^μA^ν, D·V ≡ q^{μν}∇_μ∇_νφ + θ𝒬 (= D_μV^μ, the leaf divergence), θ = ∇_μA^μ, 𝒬 = A^μ∇_μφ, γ_L = K L★²/2.
- The term acts on **AeST's scalar φ**, through its aether-projected spatial gradient. **P = V/K** and **D = the derivative on the aether's orthogonal space**. Static weak field: K P = ∇χ + Q₀a, so D·P = (∇²χ + Q₀∇·a)/K (checked in S2).
- F is AX1's AeST law candidate (C1's capped 𝓕, μ = x/(1+x)). Curl stiffness is AeST's own K_B term. At AeST's physical scales this is the curl-free (χ∞) limit on Solar-System scales (C3 K5b, read).

## Checks and gates
Engine: `common/ax1_engine.py`, a byte-identical copy of AX1's engine. It is never edited. The script execs it unchanged (class AeST, then v3s) and uses its constants, bounds, fields E0–E3 and functions.
- **KA0** the copy's SHA-256 equals AX1's engine.
- **KA1 (known answer)** the copy, run as AeST, reproduces AX1's committed `ax1_AeST.json`: every Q2_QUMOND, over_Hees_AQUAL_E2 and Saturn_over_bound, both footings, all candidates, max rel ≤ 1e-12. Labels must be identical. The copy's own K1–K4 must pass.
- **KA2** the copy, run as v3s, reproduces AX1's `ax1_v3s.json` hedgehog table and C6 margins (rel ≤ 1e-12). The lane's hedgehog function must match the engine's at 24/50/90 pc to 1e-12.
- **KA3** the closed-form screened Q2 (AS3 Part 2 form: Q2 = √2 GM/L★³ |∫₋₁¹ (½ − 3u²/2) √(S⊥(1−u²) + S∥u²) du|, S⊥ = x_e, S∥ = x_e(2 + x_e), x_e from the engine's E0–E3) must reproduce two record sets. (a) AS3 Part 2's 16 Q2 cells, rel ≤ 1e-6. (b) C3's V1 K6 Q2_V1 at 24/50/90 pc, 24 cells at D7c's a0, rel ≤ 1e-2 (an independent implementation; AS3's two implementations agreed to 0.18 %). (c) Doubling the quadrature must change it ≤ 1e-9.
- **S1/S4 (sympy, exact)** On flat FRW (any a(t), φ(t), comoving unit aether), and with a finite TT tensor mode h(t, z) added, V^μ ≡ 0 and D·V ≡ 0. Then the term and its first variation vanish, so the background equations and the tensor sector are unchanged.
- **S2 (sympy)** In the weak field (Ψ, Φ, χ, a ~ ε, time-dependent), D·V = ∇²χ + Q₀∇·a + O(ε²), with no Ψ or Φ at O(ε). So the graft adds nothing to the Φ, Ψ equations at O(ε), and Φ = Ψ (C1) is kept: γ − 1 = 0.
- **S3 (sympy)** The O(ε) part of D·V has no ∂_tχ or ∂_t²χ. So the graft adds no kinetic term for χ.
- **G2a** Q2 / Hees (9.0e-27 s⁻²) and Q2 / Park (5.2e-27) ≤ 1 at E0–E3. The grade is at L★ = the floor (21.7 canonical, 22.9 alt) and at 50 pc, per footing. Q2 = the switched graft's Q2. That equals V1's wherever D·V > 0. By X3 D2 the Solar-System region has D·V > 0 with margin ≥ 1.8e4. The graft's solution differs from C6's by an O(1) factor at most (V1/C6 ≈ 1.1–1.3), so the switch is on throughout [READ + ARGUED, stated as such].
- **G2b** (GM/L★² + GMμ_K²/2) / bound ≤ 1 for Earth 8.7e-15, Mars 1.4e-15 and Saturn 7.0e-15 m/s² (engine bounds), at μ_K = 0.1 and 1 Mpc⁻¹, at both graded L★.
- **G2γ** |γ − 1| ≤ 2.3e-5 (Cassini, Bertotti et al. 2003).
- **G2c** This carries AX1's AeST entry (record AS3) unless this lane shows the graft changes it. Branch (a), no sound speed: a moving source gives α1 = α2 = 0, but the law is lost for moving systems. If S3 holds, the graft gives χ no kinetic term and cannot change that. Branch (b), with a sound speed (c2*): AS3's exact static-branch α1 = −4(2 + K_B J)/(1 + J). The stiffness raises the scalar's static kernel, J → J + L★²k²/2 → ∞ at r ≪ L★, so α1 → −4K_B (AS3's J → ∞ value) [READING, not a solve]. G2c is F if neither branch passes both the PPN bounds and the law for moving systems, as AX1 graded it.
- **BG** PASS iff S1 and S4 hold exactly. Reported, not graded: the switched term's size on perturbations relative to the scalar's gradient term, (L★ k (1+z))²/2, at k = 0.01/0.1/0.3 Mpc⁻¹ and z = 0, 1100, 1e4, 1e5, with no cosmological model input; the k(1+z) where it reaches 1; and the fact that the background sits on the switch's kink. **The CMB itself is not recomputed.**
- **LAW** Where D·V < 0 the static equation is AeST's exactly. Elsewhere the stiffness changes the scalar kernel by the relative amount (L★/r)²/(2x). PASS if that is ≤ 0.02 dex for r ≥ 1 kpc and x ≥ 0.05, at both graded L★. Rows at 0.5 kpc are reported only. This is a reading, not a SPARC solve. AeST's own static form (AQUAL at ℓ_F → 0, per C1/AX1; curl-free two-field at physical ℓ_F, per C3) is whatever AeST gives; the graft does not choose it.
- **G4** c_T: unchanged from AeST's (c by construction [PROVISIONAL], as in AX1) iff S4 holds. Health: at AX1's level (record entries). Where D·V > 0 the graft is v4, and I1 is read for it: ill-posed wherever the aether twists. The twist is forced off symmetry (I1 K5). The switch removes the stiffness only where D·V < 0. So G4 is F unless the record shows otherwise.

## MUTATE twin and rerun
- `--mutate`: stiffness off (γ_L = 0). The graft is then AeST, graded from the engine copy's unscreened AeST numbers. It must reproduce AX1's AeST failure (G2a 2.44–5.15×, G2b 1.34e4 / 1.62e4×) to 1e-12 and must FAIL G2a and G2b (check M1). It exits 1 by design.
- Rerun: identical JSON (SHA-256 compared).

## Label (per footing, frozen)
- **GRAFT PASSES** if G2a, G2b, G2γ, BG and LAW pass and neither G2c nor G4 is F.
- **GRAFT FAILS: <every failed gate>** otherwise.
- **NOT EVALUABLE** if KA0–KA3 or S1–S4 fail.

**Expected by hand (not blind; every input is on record).** GRAFT FAILS: G2c, G4 on both footings, both inherited (AeST's preferred-frame sector; v4's twist ill-posedness). G2a passes at ~3.5e-8 of Hees at the floor, G2b passes (Mars ~0.21 of its bound at 21.7 pc), γ = 1. BG is unchanged exactly. LAW is kept outside L★.

Compute: one thread, `nice -n 10`, under 1 GB, seconds, no download.
