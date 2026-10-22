# E5_parent_logic: do the "no covariant parent" no-gos hold for the screened theory?

**Verdict: SCOPED NO-GO.** The answer to the item is **(a), a theorem for stated classes, and it holds WITH the stiffness**,
not only for the L★ → 0 law. The stiffness (L★ = 24–90 pc) changes none of the no-gos: it moves NG1's saddle trough by
≤ 9e-4, cannot remove NG2's superluminality, and cannot cure the R3θ ghost. Outside the stated classes the question stays
**open** (list below). Two of the "no-gos" are really properties of the screened theory itself, not of a parent.

Settings: κ = ½ FITTED (κ = Z/4π is a postulate). Footings 9.3603e-11 / 1.1312e-10 m/s², never pooled. Cold energy, no particle
species. Not "theory closed". Nothing here says the data favour the framework over ΛCDM. "Established parent": none.

## Files and runs
- `FROZEN_CRITERIA.md` committed alone first (039c76d2f9); AMENDMENT A1 (post-result) committed alone (ab0f5d006c).
- `e5_parent_logic.py` (sympy + numpy/scipy; 5 s, 0.36 GB RSS, one thread). `OMP_NUM_THREADS=1 nice -n 10 python3 e5_parent_logic.py`
  writes `e5_parent_logic.out` / `_results.json`. **14/15 PASS, exit 1 by design:** frozen E1 FAILS (its pass line forgot the
  O(u·L★²k²) cross terms of a truncated double series); E1b (A1, post hoc) shows the residual is exactly those terms. First run kept
  as `*_firstrun.*`. AG6C's deep two-body solver is copied verbatim (lines 58–208); AG6C's files are untouched.
- `E5_MUTATE=1`: L★ × 1000 and the G2(b) sign flipped. S3, S4 and G2 FAIL as required (11/15, `*_MUTATE.*`).

## Results
1. **NG1 survives the stiffness (S1–S4).** Linearised about AG6C's AQUAL saddle solution, the stiffness acts as an extra
   source (L★²/2)∇²ρ_ph (E1b). The response is linear to 4e-4 and robust to the core cut to 5.5%.
   - It **reduces** the trough, but by |δρ/ρ| at R = 0.2d of 5.7e-5 / 8.1e-4 (MW–M31 pair, 24 / 90 pc, canonical; alt 6.3e-5 /
     8.9e-4) and ≤ 8.6e-6 for the cluster pair. The unsuppliable mid-plane column moves by ≤ 0.92% (90 pc).
   - The stiffness-dominated core around the null point has R ≤ 0.0013d (≈ 1 kpc of a 674 kpc negative band).
   - To cancel the trough at 0.2d needs L★ ≈ 3.0–3.2 kpc (MW–M31) or 31–32 kpc (clusters); to fill the column, ≈ 0.94–0.98 kpc /
     9.5–10 kpc (first order, outside its validity; reported only). That is ≥ 10× the 90 pc ceiling.
   - So PAPER49 v1.2's "no saddle dip" depths stand for the screened theory.
2. **D-T is γ-independent (T1).** ω² = γρ₀k² + (c₂ − 1)Kρ₀. The stiffness adds only a stabilising k² term; the law's deep limit
   still forces c₂ = 1 (F(u) = D_full(u) exactly). No linear self-gravity at scales ≫ ℓ⊥ = L★√(a₀/2u) (0.13–0.53 kpc at the saddle).
3. **NG2 = a positivity violation, and the stiffness cannot fix it (N1, N2).** v_X² − 1 = −2XL_XX/(L_X + 2XL_XX), and the law's
   dual has L_XX = −1/(Ka₀²s(1+s)²) < 0 for every field, so v² = 1 + g/a₀ (exact). This is the sign Adams et al. 2006
   (hep-th/0602178) tie to "no local Lorentz-invariant UV completion" (external theorem; the law's L is non-analytic at X = 0).
   The screened theory's curl stiffness γ|∇×P|² is absent from AG6C's C1 (S0.3) and needs dark-sector gradients. Carried there it
   gives ω²/k² = N(1/ε∥ + γk²) (positive Hamiltonian: unbounded speed) or a kinetic coefficient ε∥(1 − γε∥k²) (local Lagrangian:
   ghost for k² > 1/γε∥). Both → 1 + g/a₀ as k → 0 and both raise v² with k.
4. **The R3θ ghost is not removable by the stiffness or by a parameter-free gate (G1–G5).**
   - Any term without ξ̇, the stiffness included, leaves the kinetic coefficient at ρ₀ + F_θθk² (G1).
   - Covariantly, CFG938's tidal stiffness adds nothing in the Hessian reading (h h∇∇χ), and F_θθ = −γχ̇²/K² < 0 in the iterated
     reading D_i(h∂χ) (G2): the wrong sign. In that reading the ungated parent has its own ghost band on FRW at
     k L★ > √(12/Ω_c) = 3.8 (EdS medium share) to 6.7 (Ω_c = 0.264).
   - Theorem G extends to L(θ, u, τ): the bag bound becomes W(u*) + S(τ*), so the ×15 / ×25 slip excess only grows (G3, by construction).
   - Gating the stiffness too lowers k_g by √(W/(W + S)) (G4). The one parameter-free saturation scale, u_c = a₀, lies outside C4's
     window on both footings: slip needs ≤ 0.46 / 0.34 a₀, amplitude needs ≥ 29.3 / 24.3 a₀ (G5).

## Hypothesis audit (does each no-go apply to the screened theory?)
| no-go | hypotheses | vs the screened theory (with stiffness) | applies? |
|---|---|---|---|
| NG1 (AG6C S0.4) | ρ_c = ρ̄ + ∇·P; ρ_c ≥ 0; exact static law at the saddle; isolated pair, no external field | first two are PAPER49's own kinematics and claim; the stiffness changes the trough ≤ 9e-4 (S3); external field NOT TESTED (AG7: it fills the null point) | **yes**, for the isolated pair. It is a property of the theory (no exact positive realisation near saddles), not of a parent |
| NG2 (AG6C) + D9 V2 | U(1) dark field, P = D/K, Gauss law enforced; Lorentz-invariant L(X, Y); principal symbol on a uniform background; **no dark-sector gradient terms**; criterion A (v ≤ c) | the curl stiffness breaks "no gradients", but N2 shows it only makes v larger or adds a ghost; inside the EFT band (k ≪ 1/L★) v² = 1 + g/a₀ | **yes** (Lorentz-invariant class) |
| D9 Λ_LV (foliated U(1)) | as NG2, but preferred frame; **criterion A** | with a global time function v > c is not by itself acausal; the record accepts instantaneous χ (CFG938, owner's criterion B) | **only under criterion A**; open under B |
| D-T (CFG941) | cold static medium; always-on tether F(u); phantom = own mass; law with deep limit; **local equilibrium F(u) = g** | PAPER49's tether is always on and its medium is the phantom; stiffness makes equilibrium non-local but only below ℓ⊥ ≤ 0.5 kpc (T1) | **yes**, at scales ≫ L★. A property of the theory (no self-gravity), fatal only against growth data |
| WT-02 | CFG938's χ/λ constraint with the −3Hχ̇ term; frozen-coefficient WKB; metric unperturbed | PAPER49 has no χ; the intrinsic-leaf repair (MU3) and D9b's M\* are well posed | **no** (one parent's defect) |
| D9b double count | A33's clock ξ = 1 and minimal medium coupling m_c = 1; γ → 0 statics | literal A33 only | **no** (for M\*); M\* is unique |
| D9b M\* ⇒ D-T + NG1 | linear multiplier; L49 static branch | T1 and S3 show both survive the stiffness | **yes** |
| CFG944 Theorem G | local L(θ, u), convex in θ; static law; tether off on linear locus; slip line | extends to L(θ, u, τ) (G3); stiffness cannot enter the kinetic matrix (G1, G2) | **yes** |

Hidden assumptions checked: minimal coupling (D9b: the literal A33 coupling is what double-counts); U(1) structure (only NG2/Λ_LV
need it); static ansatz (NG1, D-T statics; G1/G2 are dynamical); standard-MOND phantom-as-gravity (not used: the γ = 0 branch is
the action's own AQUAL, E2/D9b L2; QUMOND nowhere); ΛCDM background (used only for Ω_c in G2's k_g L★ and, via CFG654's CAMB
table, in G5's amplitude bound; neither carries a verdict).

## Input ledger
| input | class | source | verdict sensitivity |
|---|---|---|---|
| pair masses 8e10 / 2e13 M☉ | SURVEY-CALIBRATION (SPS / illustrative) | AG6C | δρ/ρ ∝ λ ∝ M^-½: ×10 lighter raises 90 pc to 2.8e-3; survives |
| separations 0.77 / 5 Mpc | RAW (illustrative) | AG6C | λ ∝ 1/d; survives |
| a₀ footings | FRAMEWORK-NATIVE (κ fitted) | brief | both reported |
| L★ 24 / 90 pc / 1 kpc | FRAMEWORK-NATIVE from RAW kinematics | CFG820, D8, D9 | the verdict line |
| AQUAL saddle solver (deep limit) | FRAMEWORK-NATIVE (action's γ = 0 branch) | AG6C, E2 | full-μ within 4% (AG6C) |
| Ω_c = 0.264 | ΛCDM-PROCESSED (Planck) | D9b | G2 number only (∝ Ω_c^-½); sign verdict independent |
| C4 amplitude bound 29.3 / 24.3 a₀ | ΛCDM-PROCESSED (CFG654 CAMB table) | CFG944 | G5 holds on the native slip bound alone |
| C4 slip bound 0.46 / 0.34 a₀ | FRAMEWORK-NATIVE | CFG944 / CFG847 | — |
| Adams et al. positivity | external theorem (labelled) | hep-th/0602178 | N1's reading only |

## What this does not show
- **Not a parent.** Open classes: foliated U(1) under criterion B; non-local parents beyond CFG947; non-variational latches;
  media held up by dispersion; multi-field latches; parents that do not enforce the identity (A33 stays a healthy EFT).
- The saddle solve is first order in the stiffness about the deep-MOND solution, isolated pair, no external field. At 1 kpc the
  column response is O(1), so linear theory fails there.
- No UV value for L★, κ or u.

## Record issues
- `campaign_fresh_gravity/CFG938_medium_continuum_eft/DERIVATION.md:133` defines τ_μν = D_μD_νχ − ⅓h D²χ, but line 107 defines
  only the trace (h^{μν}∇_μ∇_νχ). Read iteratively, the stiffness carries −γχ̇²θ²/2K² and a ghost band at kL★ > 3.8–6.7 on FRW.
  CFG941/944 treat the stiffness as potential only, which is right only in the Hessian reading.
- `doors_push_2026_10_22/D9_uv_parent/MAP.md` row 2 (foliated U(1), SCOPED NO-GO) rests on v ≤ c (criterion A). It does not say
  so; under the owner's criterion B (AG6C §2) it is open.
- MAP row 1 (C1) is not the screened theory off spherical symmetry: C1 carries only the divergence stiffness (AG6C S0.3).
