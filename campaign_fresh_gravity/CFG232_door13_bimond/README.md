# CFG232 — Door 13: BIMOND (Milgrom's bimetric MOND) against the candidate-B target. Phase 2 result (scoped no-go on the frozen class)

Frozen criteria: `CFG232_FROZEN_CRITERIA.md` (committed as "CFG230 / CFG231 / CFG232: frozen criteria", before any script). Every statement below is a scoped result on that frozen class; nothing here says the theory is closed, and nothing here says any data favour the framework. κ = ½ is FITTED. Nothing was tuned or scanned to make a gate pass; grids are reported, not optimised. Literature facts are from memory, unverified (section 8).

## 0. Flag first

**Nothing passes G1 as a derived mechanism.** G1-law passes for 13a, 13b-i, 13b-ii and 13c only as **M1-inv**: the interaction function (or the scalar's kinetic function) is *solved for from the target by inversion* (hand formula H4, verified symbolically), so the pass restates the kernel; it is not a mechanism (grade M2 not reached). Read against CFG44's actual C(r) target it fails on the exponential sphere at M_b ≤ 1e11 (section 3, the frozen text's claim that ν(g_N)g_N is "equivalent to C(r) for P2" is wrong for extended profiles). No independent re-derivation is owed for a mechanism claim; the field-equation reduction of A1 is what an independent lane should re-derive first, because the P-declared G1-law pass rests on it.

**Binding gates.** The ghost (G5a) fails for 13a/13b-i/13b-ii, but that is a labelled *reproduction* of the earlier WF2/L70 closure (third derivation, fresh code). Among the legs this door scores anew the binding one is **G1-C** (every sub-variant fails it), then **G4** (13a, 13b), **G2** (no real FRW background without a continuation the frozen class does not contain), **G7** (reading-dependent, recorded UNDEFINED) and **G5b Q₂** (a property of the bare law). For 13c: G1-C and G5b Q₂.

## 1. What was run

| script | content | gates / controls |
|---|---|---|
| `CFG232_common.py` | constants, kernels (read-only `Bcommon.py`), the designed-M solver, run/exit machinery | — |
| `CFG232_A1_static_reduction.py` | EH calibration (C2), the five invariants' static values (C4), spherical Euler–Lagrange, H1–H6 symbolic, design by inversion, legality, round trip (C3), G1-law at 7 masses × 2 profiles × 2 footings × P2/ν_mono, D2, phantom vs CFG44 cold mass, C8, C10 | G1-law, G1-mech; C2, C3, C4(static), C8, C10; M1–M4 |
| `CFG232_A2_spectrum_flat_and_mond_background.py` (outputs `CFG232_A2_spectrum.*`) | fresh-code flat-space quadratic action of the relative sector, Stückelberg vector/scalar, TT dispersion, lapse-velocity tuning, exact static-MOND-background vector operator, 9×9 determinant | G5a, G5c; C4, C5, C9; M1, M3, M8 |
| `CFG232_A3_cold_coupling.py` | G1-C for (c-g), (c-ĝ), 13c couplings; twin sum rule; G3 reaction | G1-C, G3; C7; M5 |
| `CFG232_A4_cosmology.py` | FRW reduction of T4−T1 (own code), symmetric-branch obstruction, constraint-only background estimate (not converged), growth coupling, G7, vector operator on FRW | G2, G7, G5a-FRW; M6, M7 |
| `CFG232_A5_lambda_tie.py` | vacuum tie derived from the minisuperspace action, rule-T check, ledgers strict/inert-window | G4; M6, M7 |
| `CFG232_A6_solar_system.py` | Q₂ (Sun at Saturn; MW tide), γ − 1 at Saturn | G5b; C6 |
| `CFG232_A7_scalar_tensor_13c.py` | 13c law by inversion, k-essence legality, sound speed, lensing slip, G2 nonlinear estimate | 13c; M9 |
| `CFG232_A8_energy.py` | canonical energy of the interaction sector and the relative sector, both r_ta conventions | G3 energy |
| `CFG232_verdict.py`, `CFG232_run_all.py` | aggregation (no physics); driver | — |

Outputs: `CFG232_<script>.out/.json` (main) and `CFG232_<script>_MUTATE_<M>.out/.json`; `CFG232_verdict.json`. Note on reading the `.out` files: a "(result)" check line's [PASS]/[FAIL] refers to the claim printed on that line (for example "G1-C FAILS the 10% line" shows [PASS] when the failure is confirmed); the gate verdicts are the ">>> VERDICT" lines and the table below.

**Exact re-run command** (from the lane directory in the repo, or with `ZF_REPO=<repo root>` if run elsewhere; about 5 minutes; a failing reproduction control exits 1 and is kept, see section 6):

`python3 CFG232_run_all.py`

## 2. Gate table per sub-variant (each cell cites its script)

Letters as in the gates file: PASS / FAIL / UNDEFINED / NOT ADDRESSED; "P-decl" = pass with the function designed by inversion; "*" = passes by a stated definition only.

| gate | 13a (Milgrom BIMOND, Λ̂ = 0) | 13b-i (Λ̂ sets a₀, Λ̂ = Λ_g by hand) | 13b-ii (M₀ is the vacuum energy) | 13c (conformal AQUAL-type scalar; reproduction control of N1) |
|---|---|---|---|---|
| G1-law, target ν(g_N)g_N | **PASS P-decl (M1-inv)**, max dev 1.5e-6 [A1] | same [A1] | same [A1] | **PASS P-decl (M1-inv)**, 2.3e-6 [A7] |
| G1-law, CFG44 C(r) target | **FAIL** on the exponential sphere: up to 0.50 (P2), 0.54 (ν_mono) at M_b = 1e9; point mass P2 exact, ν_mono 0.14 [A1 B.3b] | same [A1] | same [A1] | same (law depends on g_N alone) [A1/A7] |
| G1-mechanism | M1-inv [A1] | M1-inv [A1] | M1-inv [A1] | M1-inv [A7] |
| G1-C, cold in g (c-g) | **FAIL** (g_tot/g_target = ν(g_target): 1.31 at x=1, 1.96 at x=3, 5.57 at x=30; crosses 1.10 at x = 0.483) [A3] | FAIL [A3] | FAIL [A3] | FAIL (conformal) 4.6–5.0; Einstein-frame kernel-blind 0.97–1.45 [A3] |
| G1-C, cold in ĝ (c-ĝ) | **FAIL** (force reduced; g_tot/g_C − 1 down to −5.8: sign reversal) [A3] | FAIL [A3] | FAIL [A3] | n/a |
| G2 | **UNDEFINED** (no B = 0 branch with matter in g only; on every solution Q < 0, outside the design); growth estimate under a declared mirror continuation FAIL (7.5% at z=0, > 5% for z ≲ 1) [A4]; CMB UNDEFINED | **UNDEFINED**; growth estimate FAIL (13% at z=0) [A4] | **UNDEFINED** [A4] | **FAIL** on the nonlinear quasi-static estimate (G_eff/G − 1 up to 2e2 at k = 30/Mpc); the linear χ theory is strongly coupled (UNDEFINED); CMB UNDEFINED [A7] |
| G3 reaction | PASS* (c-g, by the frozen definition); **FAIL** (c-ĝ: 5.4 g_law) [A3] | same [A3] | same [A3] | PASS* [A3] |
| G3 energy | **FAIL**: \|E_int\| = 19–254 × ½M_bV_f² (sign NEGATIVE); relative-sector excess 1.2–2.8 × [A8] | same [A8] | same [A8] | FAIL by the (2/3)ln(r_e/r_M) indicator (≥ 1.8; not a separate script) [A8 hand column] |
| G4 strict | **FAIL** (a₀ free; γ/β; u₁/u₀) [A5] | **FAIL** (γ/β, u₁/u₀ remain; a₀ tie written in; Λ̂ = Λ_g by hand) [A5] | **FAIL** (u₁/u₀; M₀ = κ fitted; γ = β forced; a new free function, the continuation to Q < 0) [A5] | **FAIL** (a₀; coupling normalisation) [A5] |
| G4 a₀–Λ tie | not tied [A5] | written in (rule T), a stated equivalent, not derived [A5] | native but INVERTED (a₀ primary); κ² = −16πβ/(σ_s M₀) derived, κ ↔ M₀ [A5] | not tied [A5] |
| G5a well-posedness | **FAIL**: fourth-order Stückelberg vector, coefficient ∝ the MOND coefficient (REPRODUCTION of WF2/L70) + same on the FRW background (NEW) [A2, A4] | same [A2, A4] | same [A2, A4] | PASS on the conditions checked (μ_χ > 0, F_X + 2XF_XX > 0, 0 < c_r² ≤ 1); c_r² = 1/(4y) = 3.6e-7 at Saturn for P2 (strongly coupled) [A7] |
| G5b Q₂ (bare law) | **FAIL** (Sun's own phantom at Saturn: 6.3e3–1.6e4 × the bound; MW tide at the Sun 3e-5 × the bound passes only under ownership, which is not supplied) [A6] | same [A6] | same [A6] | same [A6] |
| G5b γ | PASS (Ψ′/Φ′ − 1 = −4.8e-7 P2, −9.9e-7 ν_mono, canonical) [A6] | PASS [A6] | PASS [A6] | PASS (same order, analytic) |
| G5c c_T | **UNDEFINED** for the relative TT modes: their kinetic term −(1/2)(κ²−ω²)(1+4μu₀) vanishes exactly at the tuned (MOND) value; the sum graviton has c_T = 1 [A2] | same [A2] | same [A2] | PASS (analytic: EH + conformal scalar; not scripted) |
| G7 | **UNDEFINED** (R-static PASS: relative Q shift 4e-6 at 600 km/s; R-add FAIL: argument negative at z=0, boost cross term 2.8% at y=1, > 100% at y ≤ 0.03) [A4] | UNDEFINED (R-add: \|Q_bg\| = 17–200; cross term 0.5–1.6% at y=1) [A4] | UNDEFINED [A4] | PASS (analytic: X is a gradient invariant; not scripted) |

Frozen estimates against outcomes are in section 6.

## 3. What is new here (the results that were not in the record)

1. **The static reduction is exact and algebraic in g_N** (A1, symbolic). With the tuned invariant T4−T1: δΨ′·D(x) = g_N/β, D = 1 − 4x − 32x², x = σ_s m (1/β + 1/γ), δΦ′ = δΨ′(1+8x), Φ′ = [g_N + 4σ_s m δΨ′(3+8x)]/β. Hence Φ′ is a function of g_N alone: the same for every mass and every spherical profile (G1-law "same constants at every mass" holds by structure), and *incapable* of reproducing CFG44's profile-dependent C(r) on an extended profile (the exponential sphere at low mass fails by up to 0.50).
2. **MOND needs a tuned interaction** (H1, verified): the deep regime sits on the kinetic degeneracy D = 0, roots x = 1/8 (branch A, attractive, m₀ = βγ/[8(β+γ)] = 1/16 at β=γ) and x = −1/4 (branch B). Branch A has m decaying to 0 in the Newtonian end (legal: Q monotone, m non-increasing, D > 0, all kernels, γ/β ∈ {1/3,1,3}); branch B has m → 0.1875 at high acceleration (never decouples: not a legal Newtonian limit).
3. **The record's "representative" M ∝ Q^{3/2} (M′(0) = 0) does not by itself give MOND in this reduction** (C10, H6): Newtonian G/β at low gradient, the locked value G/(β+γ) = ½ at high gradient, a root-branch with constant force 8.5e-4 a₀ (λ = 10) independent of the source for the second root, and no real root at large source accelerations for λ ≥ 1. An untuned constant m gives a scale-free constant factor (17.05 for m = 0.06, −5.16 for m = 0.07). Only M′(0) = m₀ gives the r⁻¹ regime. So the earlier statement "MOND-alive" means "static coefficient a ≠ 0", not "the reduced equations give MOND".
4. **The ghost, fresh code** (A2): L_A1 = −(μ/2)(2u₀+u₁)(κ²−ω²)² A_x², exactly the record's structure and proportional to a = −2(2u₀+u₁); the pure-π row of the helicity-0 form vanishes on the tuned subspace; the lapse-velocity-free conditions give c₁ = −c₄, c₂ = c₃ = −c₅/2 (2-dim, the record's family). On the exact static-MOND background (pulled-back metric g′ = φ*g) T̄ = −4(p²+2q²) exactly, δT = 0, and the vector operator is *purely* four-derivative, −(κ²−ω²)², with no first-jet part; on FRW it is (κ²/a² − ω²)². The record's 2×2 matrix W is **not reproduced as a matrix** (its variables are not defined in the record file I read); the shared conclusion (a fourth-order vector ∝ M′ at every M′ ≠ 0, a dipole ghost for either sign) is reproduced.
5. **The relative TT kinetic term vanishes at the MOND-tuned value** (A2): L_TT = −(h²/2)(κ²−ω²)(1 + 4μu₀); the degeneracy value needed for MOND is μ = −1/(4u₀) (u₁ = 0), where it is zero. The record's c_T² = 1 is correct at non-degenerate μ. At the tuned value the whole 9×9 flat kinetic matrix is degenerate (det ∝ (2μ−1)(4μ+1)⁵ (κ²−ω²)⁷ vanishes): the linearised flat spectrum is not defined there (strong coupling), so the flat-space count is only defined off the tuned value (14 = 7 dof-equivalents with an Ostrogradsky vector counted twice).
6. **On FRW the interaction argument changes sign** (A4, own reduction): T4−T1 = 3(B + 2wq)² − 4p² − 8q², B = (2H·nn − Ĥ(nn²+rr²))/nn. The cosmological (timelike) part is +3B² (Q = −T/a₀² negative), the static part negative T (Q positive), and a moving source enters only through B → B + 2wq. There is **no symmetric (B = 0) FRW solution with matter in g only** (E_N − E_N̂ = dust term, symbolic), so every FRW background sits at Q < 0, where the static design of A1 says nothing: the background needs a continuation of M to negative argument (a new free function, not in the frozen ledger). With Ĥ = 0 the record's k_Q = 3 becomes 12 (|Q_bg| = 12H²/a₀² = 587 at z = 0), and with the sign opposed to the static one.
7. **G1-C, exactly:** with the cold component at CFG44's target profile and coupled to g, g_tot/g_target = ν(g_target/a₀) (1.0050, 1.0717, 1.31, 1.96, 5.57 at x = 0.1, 0.4, 1, 3, 30), checked numerically to 6e-6; the 10% line is crossed at x = 0.483. Coupled to ĝ, the force on the baryons is reduced and reverses sign. The twin sum rule of the record (F_TM = 1 − ν) is reproduced *at fixed interaction argument* (C7a, exact); with the full nonlinear response F_TM is 2 to more than 40 times smaller in magnitude (C7b), so the record's theorem is a fixed-Q statement.
8. **Energy:** the interaction sector's canonical energy is NEGATIVE (−19…−254 × ½M_bV_f²), growing ∝ r_e; the relative-sector excess energy (EH-relative + interaction, minus the decoupled Newtonian value) is 1.2–2.8 × ½M_bV_f², about 0.7 of the hand indicator (2/3)ln(r_e/r_M) (a control on the frozen hand estimate). A negative interaction energy is the ghost-like signature; it is reported, not counted as a pass.

## 4. Does a Λ-sourced second metric supply the a₀–Λ tie? (13b, A5 and A4)

**No, not as a derivation. What it does and does not give:**
- **13b-i (Λ̂ in ĝ sets a₀).** The bimetric structure does not force it: a₀ is an independent coupling and Λ̂ another. Writing a₀ = κc²√(Λ̂/8π) (rule T, a Henneaux–Teitelboim-type promotion of Λ̂ to an integration constant) and imposing Λ̂ = Λ_g by hand reproduces the canonical a₀ (9.355e-11 vs 9.3603e-11, 6e-4) and the CFG43 identity a₀²/8πG = (κ²/8π)ρ_Λc² by definition. It fixes c H_Λ̂/a₀ = √(8π/3)/κ = 5.789. It is a stated equivalent of the CFG43 tie, written in; κ stays fitted; G4 tie = PASS only in that sense. The gates it does not repair: ĝ is de Sitter while g has matter, so H ≠ Ĥ and B ≠ 0 (Q < 0) at every z; under the additive reading the local argument is negative at z=0 (|Q_bg| = 17.5–200 against a local Q ≤ 12 for y ≤ 1).
- **13b-ii (the interaction's constant part is the vacuum energy; Milgrom's route as the record quotes it).** Derived here from the minisuperspace action: the symmetric vacuum exists only for **γ = β**, and κ² = −16πβ/(σ_s M₀) (κ = ½ ⇔ σ_s M₀ = −64π = −201.06 at β = 1). This coincides with the record's quotation of eq. 87 (κ² = 16π/(−M̃₀)) in my normalisation; that coincidence is not evidence about Milgrom's own normalisation. The relation is *native* but **inverted** (a₀ primary, Λ derived), κ is traded for the value of a dimensionless function at zero argument (still fitted), and the vacuum branch it uses has no solution with matter in g only (item 6 above), so the identification "interaction constant = observed Λ" holds at most as a late-time attractor that was not shown.
- So: the bimetric structure allows a tie of either form but derives neither; κ = ½ remains a fitted number in both readings.

## 5. Earlier verdicts: inherited or newly scored (state per frozen §0.5 and §0.7; updated by outcome)

| earlier item | treatment in this lane | outcome |
|---|---|---|
| WF2 / L70 (vector ghost, tuned five-invariant class) | labelled REPRODUCTION (A2, fresh code) | reproduced in structure (item 4); W matrix not reproduced as a matrix; c_T reproduced only off the degenerate value (item 5) |
| DC-018 (HR potential, integer Galileons) | control C5 | reproduced (n = 3/2 needed) |
| Route 6 (F_TM = 1 − ν) | outcome control C7 | reproduced at fixed Q (C7a); full nonlinear response differs (C7b) |
| door-3 asymmetric FRW (a_eff rises, k_Q = 3) | re-derived (A4) | the FRW argument is +3B² (k_Q = 12 for Ĥ = 0), opposite sign to static; no symmetric branch |
| eq. 87 "O(1) unfixed" | derived in a definite normalisation (A5) | κ² = −16πβ/(σ_sM₀), γ = β forced |
| BIMOND_HOST preprint's "no vector, R2 absent" | not inherited | superseded (the relative-diffeomorphism Stückelberg vector is present); the preprint is not a survivor |
| CLOSURE_LEDGER's "BD ghost UNCHECKED" | not inherited for this class | superseded by WF2/L70 and A2 |
| sf10/sf10E/sf13c/sf15 withdrawn items | not inherited | discipline applied (calibration C2, both lapses, a script that raises is not a PASS) |
| newly scored: G1-law at CFG44's masses/geometry, G1-C, G2 (actual FRW reduction), G3 reaction and energy, G4/tie, G7, Q₂ and γ for the BIMOND law | scored anew | see the table |

## 6. Failed controls, wrong expectations, disclosures (kept, not repaired)

- **C6 as frozen fails.** The frozen text expected the CFG7 H1 recipe to give "4.0–5.7× the ceiling". It gives 3e-5–5e-5 × the bound (MW tide) and 6.3e3–1.6e4 × (Sun's own field at Saturn); the 4.0–5.7 has another origin (the door-11 lane found the same). `CFG232_A6` exits 1 by the frozen convention; the C6a reproduction of H1's own committed numbers passes.
- **C7 as frozen partly wrong**: the record's twin sum rule holds only at fixed interaction argument (C7a passes exactly; C7b, the full response, differs by factors 2 to more than 40).
- **The frozen claim "ν(g_N)g_N is equivalent to C(r) for P2" is wrong for extended profiles**: G1-law vs the C(r) target fails on the exponential sphere at low mass (table). The primary G1-law line (law target) follows the frozen §1.1.
- **C10 details**: my first tolerance (1e-3 at y = 1e-6) was too strict for λ = 100 (1.006); the untuned-constant-m statement in the frozen text ("(1+..) enhancement") had the wrong sign for m above m₀ (−5.16). H1's numerical tolerance (1e-6) was too tight for the y = 1e-8 grid floor (4e-6); set to 1e-4 and disclosed.
- **A2 M3 (γ → ∞) does not bite** in the ghost counting (expected by the frozen text to change it): the Stückelberg vector's fourth-order term is independent of b; the same MUTATE bites in A1 (G1-law). Declared control failure.
- **The frozen G5c estimate (P 0.70) was wrong**: the relative TT kinetic term vanishes at the MOND-tuned value.
- **The frozen G2 hand numbers used k_Q = 3 and a positive argument**: the derived FRW reduction is k_Q = 12 (Ĥ = 0) with the opposite sign.
- **Sign convention erratum**: the frozen §1.2 wrote the action interaction with a minus sign and the static Lagrangian with a plus sign; the two differ by σ_action = −σ_s. All H-formulas, designs and results use the static-Lagrangian sign σ_s (branch A = σ_s = +1); the action-level branch is the other sign of the same construction. Both signs were scored (branch B fails legality).
- **Background solver not converged**: the constraints-only FRW estimate (A4 Part 3) shows solver flags in 16 of 21 points (13a 7/7, 13b-i 7/7, 13b-ii 2/7); deviations of tens of percent and Ĥ ~ 60 are artefacts of the arbitrary initial ratio rr_i = â/a = 1 at z = 30 and of the amplification (a/â)^{3/2}; **no verdict uses them**. The growth estimate uses prescribed backgrounds (H = H_ΛCDM; ĝ static, or de Sitter with Ĥ = H_Λ and rr = 0.07), under a **declared** mirror continuation M(Q<0) := M(|Q|); it is not the theory.
- **Estimates were not blind** (the class was chosen after reading WF2/L70). Frozen estimate vs outcome: G1-law P-inv 0.85 → passed as predicted (but the C(r)-target reading fails, unforeseen); G1-C F 0.98 → FAIL; G2 (13a) F 0.25/P 0.25/U 0.50 → UNDEFINED + estimate FAIL; G3 energy F 0.5 → FAIL; G4 strict F → FAIL; G4 tie 13b-i P-rule 0.70 → as predicted, 13b-ii P-count 0.60 → as predicted (native, inverted); G5a F 0.90 → FAIL (reproduced, P(reproduce) 0.85 realised); G5b γ P 0.80 → PASS; G5b Q₂ F 0.90 → FAIL on the isolated-Sun reading; G5c P 0.70 → wrong (UNDEFINED); G7 U/F → UNDEFINED.

## 7. MUTATE outcomes (exit 1 = the control bites)

| MUTATE | where | outcome |
|---|---|---|
| M1 interaction off | A1, A2 | bites: G1-law deviation 0.90 (g = g_N); the Stückelberg vector operator vanishes (EH + EH healthy) |
| M2 swap baryons to ĝ (γ/β = 3) | A1 | bites: 0.79; at γ/β = 1 the swap is a symmetry and does NOT bite (1.5e-6), as required |
| M3 γ → 1e6 β | A1 (G1-law) bites 0.76; A2 (ghost counting) **does not bite** (declared) | |
| M4 flip σ_s | A1 | bites: 0.95 |
| M5 cold coupling swap (c-g) → (c-ĝ) | A3 | bites: at x = 3, +0.96 (overshoot) becomes −1.40 (reversal) |
| M6 Λ̂ = 4Λ_g (a₀ doubles vs observed) | A4 (|Q_bg| 200 → 17, change 0.92), A5 (G1-law 0.41) | bites |
| M7 M₀ → 0 (13b-ii) | A4 (matter-only H(0)/H_ΛCDM − 1 = −0.44), A5 (H² = 0) | bites |
| M8 detune off the tuned line | A2 | bites: lapse-velocity terms appear (−1/N⁴, …) and the pure-π row of the helicity-0 form is nonzero |
| M9 GR-quadratic 13c kinetic function | A7 | bites: G1-law deviation 0.97 while the phantom (and Q₂) vanish |

## 8. Literature claims (each from memory, unverified; for the data chat)

The frozen file's §0.6 list L1–L10 stands unchanged. Least sure: **(i) the exact scalar(s) Υ** of Milgrom's interaction (whether one scalar or several; the class scored here is the record's tuned five-invariant transcription, direction T4−T1, which may not be Milgrom's own); **(ii) the overall sign** of the interaction against the Einstein–Hilbert terms (see the erratum); **(iii) the factor in eq. 87** (my derivation gives κ² = −16πβ/(σ_sM₀) in my normalisation; the record quotes 16π/(−M̃₀) with O(1) unfixed). Also unverified: that Milgrom's function is M ~ Q^{3/2} at small argument (C10 shows this alone does not give MOND in my reduction, which either means my reduction of his action differs from his NR limit or that his NR limit involves a different regime; I cannot tell from memory), Milgrom 2009 = PRD 80, 123536 = arXiv:0912.0790 (bibliographic details Crossref-checked in the repo, content not), Chesler–Loeb 2017 (abstract only), Hassan–Rosen 2012, Bekenstein–Milgrom 1984, and the constraint numbers (Q₂ ≤ 5.2e-27 s⁻², γ − 1 = (2.1 ± 2.3)e-5, |c_T/c − 1| < 1e-15).

## 9. What was NOT tested

Non-spherical baryons and the full 3D nonlinear elliptic system (only Gauss-integrable spherical symmetry; no external-field solution beyond the CFG7 H1 recipe); other interaction scalars than the tuned five-invariant quadratic family, non-quadratic arguments, Milgrom's own scalars if they differ; the Hassan–Rosen potential as a sub-variant (control only); a lapse-free spatial-scalar HR-type interaction with a preferred foliation; the DBI khronon dark sector; twin matter as a new species (never added); a Boltzmann-code CMB (G2's CMB part UNDEFINED throughout); the full coupled FRW dynamics (evolution equations of a, â and the relative lapse were not solved; the constraint solver did not converge); nonlinear cosmology, clusters, mergers; the nonlinear matching solution of ĝ around a collapsed g region (which decides R-static vs R-add, the bimetric form of candidate B's Gap 1); lensing beyond D2 (Φ′/Ψ′ → 2 in the deep phantom, hand and numerics; the record's M_dyn/M_lens = 2 convention was not re-derived); the physical branch selection between multiple roots; time-dependent stability of 13c beyond the sound-speed conditions; G5c and G7 for 13c are analytic statements, not scripted; the energy of 13c is the hand indicator only; Gap 1 (bound-only ownership), CFG250/251/252 (not touched); quantum corrections and UV completion.

## 10. Files

`CFG232_common.py`, `CFG232_A1_static_reduction.py`, `CFG232_A2_spectrum_flat_and_mond_background.py`, `CFG232_A3_cold_coupling.py`, `CFG232_A4_cosmology.py`, `CFG232_A5_lambda_tie.py`, `CFG232_A6_solar_system.py`, `CFG232_A7_scalar_tensor_13c.py`, `CFG232_A8_energy.py`, `CFG232_verdict.py`, `CFG232_run_all.py`, the corresponding `.out`/`.json` files (main and `_MUTATE_<M>`), `CFG232_verdict.json`, `README.md`; `CFG232_FROZEN_CRITERIA.md` is the committed frozen file (unchanged).

## In-place re-run (orchestrator)

`python3 CFG232_run_all.py` was re-run in this directory with `ZF_REPO` set (`run_all.out`; about 2 minutes here): the main runs exit 0 except A6 (exit 1, the kept failed reproduction control C6); of the thirteen MUTATE run modes twelve exit 1 (bite) and A2 MUTATE=M3 exits 0 (does not bite, a declared control failure). Every `.out` and `_results.json` is identical to the author's apart from timing lines. The frozen criteria are `../CFG232_FROZEN_CRITERIA.md` (79974a5a, committed in b31f5e705). The published BIMOND preprint and the four withdrawn RETRACTIONS items on this door are not inherited as survivors.
