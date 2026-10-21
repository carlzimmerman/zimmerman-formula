# CFG944: can the turnaround-gated tether (CFG941 R3θ) be made ghost-free?

**Lane label: NO CURE.** Every cure is NOT CURABLE, and **Theorem G** passes its checks. No local Lagrangian L(θ, u) of the medium's
expansion θ and tether invariant u can satisfy all four of:
- (a) the static law on NGC 3198;
- (c-amp) linear growth at the actual linear amplitude;
- (d) ghost freedom at every k;
- (e) the slip line.

Three findings:
- The one construction that cures the ghost globally (C4) has to switch the tether on in the linear regime at z ≳ 84.
- Every candidate's settled sector is CFG938's P0, so (g) fails: class A is not the non-relativistic limit, and the T1x/T2x/NC1x shear
  passes do not transfer.
- F2 (CFG945) is unaffected.

**Settings.**
- **Criteria:** `FROZEN_CRITERIA.md` (2587be5c7, committed alone first). Block 940–949. No amendment.
- κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 never pooled. Cold energy; no particle species. Framework-native inputs only (CFG654's
  native table is used for the linear amplitude, with its caveats).
- Not "theory closed". Nothing here says the data favour the framework.

## The ghost (DERIVATION §1)
- **Exact form.** In label coordinates θ = J̇/J. Any medium term F(θ, u) has the rank-one second variation
  (F_θθ/2J₀)(δJ̇ − θ₀δJ)² (sympy). One Fourier mode's J₂ vanishes, so the longitudinal kinetic coefficient is exactly ρ₀ + F_θθk².
- **R3θ.** F_θθ = −s″W < 0 on the gate's convex half, so there is a ghost for k > k_g.
- **The degenerate surface.** At k_g the inertia vanishes and ω² ∝ 1/(k − k_g) → −∞: ω² is not bounded below independently of k.
- **Reproduction.** CFG941's nine k_g R values (0.23–2.19) are reproduced exactly.
- **Galaxy interiors.** Settled galaxies reach the convex half with |∇·v| ~ 1e-18 s⁻¹. On NGC 3198, k_g r = 5e-4 – 1.2e-2, so the
  ghost covers all galactic scales.

## Cures and outcomes

| cure (one new constant) | action change | a | b | c | c-amp | d | e | g | class |
|---|---|---|---|---|---|---|---|---|---|
| C1 | +(c_θ/2)θ², always on | PASS | PASS + cost G_cosmo/G = 1/(1 − 12πGc_θ/c²) | FAIL: needs c_θ ≤ 8.9e14 kg/m; ghost bound 1.6e24–1.5e25 (×2e9–2e10) | = c | FAIL (region u ≤ 1e-5 a₀ at the growth max) | PASS | FAIL | **NOT CURABLE** |
| C2 | gate on ρ_c / χ / a multiplier latch, incl. Y = Kρ_cT² | FAIL (ρ, Y: BTFR); χ changes the law | — | FAIL (ρ: on at z > 18) | — | FAIL (ρ, Y: gradient instability, ΔY needed ≥ 1e5 vs 1.2e3); latch: −λ̄F_θθ ghost, H linear in the multiplier | — | FAIL | **NOT CURABLE** |
| C3 | any s(θ): smooth, saturating, bounded s″ | PASS | PASS | PASS | = c | FAIL: concavity theorem; min max s″ = 2/θ_s² moves k_g ×5.1 at most | PASS | FAIL | **NOT CURABLE** |
| C4 | s(θ, u) = ŝ + h(u)(1 − ŝ) + transition-localized convex L₀(θ); constant u_c | PASS | PASS | PASS (literal) | FAIL: the 1σ linear field U reaches 15.6a₀ at z = 1100 (U ≥ a₀ for z ≥ 84); needs u_c ≥ 24–29a₀ | **PASS, global** (F_θθ ≥ 0 exactly; ω² ≥ −max(Kρ₀, θ₀²)) | PASS for u_c ≤ 0.22 / 0.16a₀ | FAIL | **NOT CURABLE** |

**Theorem G (DERIVATION §7).**
- Convexity in θ, the static law at θ = 0, and the tether being off on the linear locus together force a vacuum offset in every static
  region: B = L(0, 0) − T(0) ≥ W(u*).
- B ≥ 0.71 a₀²/K (canonical) and 0.62 (alt), against the slip-allowed 0.048 / 0.025: ×15 / ×25.
- For every gate profile ∫₀¹ x s″ = 1, so no profile escapes.

**C1 cosmology.** The minisuperspace action with lapse gives H² = (8πGρ/3)/(1 − 12πGc_θ/c²), i.e. Einstein-aether with
c₂ = −8πGc_θ/c², and G_N = G.
- At the ghost bound G_cosmo/G = 1.05 (T1), 1.34–1.48 (NGC 3198 interior) and 1.41–1.75 (edge fields).
- For u ≥ 0.978a₀ / 0.944a₀ there is no Friedmann branch.
- The record has no BBN bound on G_cosmo. None is needed, because growth already excludes C1.

**Best candidate written out (ghost-free, but fails (c-amp)):**
  S = ∫√−g [c⁴R/16πG − mc²n − s(θ, u)W_full(u) − (3γ/4K²)τ² + L₀(θ) + λ(D²χ − Kmn)] + S_b, with:
- s = ŝ(θ) + h(u)(1 − ŝ(θ)), ŝ = R3θ's gate (θ_s = H₀), h = S5(2u/u_c − 1);
- L₀″ = W_g·60x(1 − x)/θ_s² (x = θ/θ_s), L₀ = 0 for θ ≥ θ_s;
- W_g = max over u ≤ u_c of (1 − h)W;
- bag B₀ = 5W_g.

**(g)** (DERIVATION §8; engine code read, not run). Only g3 (linear dust) matches:
- the engine uses a universal −∇φ with an extra zero-sum source (src), against the gated theory's tether force;
- its phantom is computed from the retained baryon fraction, against the total tethered field;
- its switch is non-local catchment balls, against a pointwise θ ≤ 0;
- its source is filled by an instantaneous shell draw, against medium transport.

The shear passes do not transfer.

**F2.** The settled sector is P0 plus at most a constant, so the hover lemma stands (CFG945 decides).

**Side flag (estimate, not graded).** P0's always-on tether reads the medium's linear field, which reaches W_full's wall (u = a₀) at
z ≥ 84 / 101 on typical points. CFG941's P0 exponents assume u ≪ a₀. CFG938/941 are not edited.

## Controls
- **K: all pass.**
  - K1: NGC 3198 law 2.22e-16 on both footings.
  - K2: BTFR +1.0e-7 at y = 1e-14.
  - K3: n = 0.609545 / 0.694330 / 1; c₂,max = 2.3458e-3.
  - K4: CFG941's k_g grid reproduced exactly.
  - K5: s_847 = 1.5398e-5.
  - K6: the second-variation identity reproduces CFG941's kinetic term.
- **MUTATE: all seven teeth bite (exit 1 by design).**
  - M1/M1b: removing the cure brings the ghost back.
  - M2: c_θ below the bound leaves a ghost.
  - M3: half the bag leaves a ghost.
  - M4: no saturation leaves a ghost at u → a₀.
  - M5: U ≡ 0 opens C4's window, so (c-amp) is what closes it.
  - M6: without (a) the bound is 0.

## Files and commands (one core, nice 10, < 0.35 GB, ~1.5 s each, nothing downloaded, no other lane touched)
- `CFG944_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg944.py` → `cfg944_K.out`, `cfg944_results_K.json` (exit 0).
- `CFG944_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg944.py` → `cfg944_MUTATE.out`, `cfg944_results_MUTATE.json` (exit 1 by
  design).
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg944.py` → `cfg944.out`, `cfg944_results.json` (exit 0; all checks pass).
- `DERIVATION.md` has the equations, every number and the disclosures.

## Disclosures (full list in DERIVATION §11)
- **Text-only edits after the first full run.** Three output strings were changed:
  - G3's sign wording;
  - C1's class line, which now prints the computed u_flip instead of a hand "0.9a₀";
  - g2's description of class A's phantom input.

  No check, test, number or class changed. K, MUTATE and main were rerun from the final script (sha256 9978ec65…).
- **Missed hand expectations (kept).**
  - u_flip 0.94 → 0.978 / 0.944a₀;
  - C1 inertia range;
  - (e) cap 0.3 → 0.22 / 0.16a₀.
- **Implementation choices.**
  - The EdS-consistent ρ̄_c in C1, which favours C1.
  - U without the D5 boost and with the medium share, both of which lower U.
  - The G3 example state, C4's dispersion sample with s₀ only, T2 capped at 0.999a₀, and the Y-gate age 2/(3H₀).
- **Open (not tested).** A non-variational latch; a medium held up by dispersion rather than a tether (a different theory);
  ρ-dependent extensions of Theorem G.
