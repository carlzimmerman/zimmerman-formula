# CFG941: self-gravity repair of CFG938's covariant parent

**Lane label: STRUCTURAL OBSTRUCTION.** The deep law forces the tether's quadratic coefficient to c₂ = 1. That coefficient both
makes the law the medium's static equilibrium and cancels the medium's linear self-gravity and its gravity on other tethered
medium (F1 and F2). No repair passes (a)–(e) together.
- The one repair that restores a¹ growth and keeps the law (a local turnaround gate) has a ghost.
- Every repair fails F2 and the class-A limit, so the T1x/T2x/NC1x shear passes **do not transfer** to CFG938's parent or to any
  repair tested here.

**Settings.**
- **Criteria:** `FROZEN_CRITERIA.md` (0b41bd0cf, committed alone first); `AMENDMENT_A1_pre_result.md` (7c395c866). Block 940–949.
- κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 never pooled. Cold energy; no particle species. Framework-native only.
- Not "theory closed". Nothing here says the data favour the framework.

## Diagnosis (DERIVATION §1)
- **No source double count.** ∇²Φ = K(ρ_b + ρ_c) in both S2 + ID and CFG938. S2's P·∇Φ *is* the medium's rest-mass coupling.
- **What cancels self-gravity.** The u term of D_full = u + R, i.e. the quadratic u²/2K of W_full (S2's critical quadratic
  −K|P|²/2). On a medium element: −∇Φ + D_full∇̂χ = −∇Φ_b + R(|∇χ|)∇̂χ, because χ is the medium's own potential.
  - Mode average: ⟨L⟩ = (K/4k²)[(B + C)² − c₂C²]. The self term and the C₁C₂ mutual term are both ∝ (1 − c₂).
- **Theorem D-T.** For a cold static medium whose phantom is its own mass, the law forces F(u) = D_full(u), so c₂ = 1. Any law
  with the deep limit g_N → g²/a₀ does the same, and only c₂ = 1 gives the BTFR. Hence **(a) ⟹ no linear self-gravity**:
  F1 is structural to S2+S3.
- **A correction to CFG938 S6.** CFG938's FRW χ̄(t) carries a timelike gradient χ̄̇/c² = −Kρ̄/(3H). Covariantly, u² = |∇δχ + (χ̄̇/c²)V|²
  (an O(c⁰) term). It lowers the medium's inertia by Ω_c/6 and adds a force (Kρ̄_c/3)qψ. The parent's exponent is **a^0.694**,
  not a^0.610. F1 stands.
- **Hover lemma.** In any static cold tethered equilibrium, medium at rest feels zero net force (CFG939's flat potential). A
  satellite's tethered medium therefore feels no host force while its stars feel g_host: **Δa/g_host = 1.02–1.11**.

## Repaired actions and outcomes (P0 = CFG938: S = ∫√−g[c⁴R/16πG − mc²n − W_full(u) − (3γ/4K²)τ² + λ(D²χ − Kmn)] + S_b)

| repair | action change | a | b | c | d | e | f | g | class |
|---|---|---|---|---|---|---|---|---|---|
| R1 | W_full → W_rem (dust gravity kept, tether only redistributes) | FAIL (1.64 / 1.88; floor a₀/2; = CFG938 M3) | PASS | PASS (n = 1) | PASS | FAIL (3.3e-5) | FAIL (1.000) | FAIL | **NOT REPAIRABLE** |
| R2 | −mc²n_f − mc²n_t; tether sector on n_t only; no conversion | FAIL jointly (f_t ≤ 0.060 ⇒ free mass ×15.6 enters the law's source: dev 74 / 82; supply 0.68 / 0.61) | PASS | FAIL (f_t = 1: 0.694) | PASS | PASS | FAIL | FAIL | **NOT REPAIRABLE** |
| R3n | s(ρ_c)·[W_full + stiffness] | FAIL (tether ends at 73 kpc; BTFR → 0) | PASS | FAIL (gate on for z > 18) | FAIL (c_eff² < 0) | PASS | FAIL | FAIL | **NOT REPAIRABLE** |
| R3θ | s(θ)·[W_full + stiffness], θ = ∇·u (CFG649's turnaround switch, made local) | PASS (2.2e-16) | PASS | PASS (n = 1, all k) | **FAIL (ghost, k_g R = 0.23–2.19)** | PASS | FAIL | FAIL | **PARTIAL** |
| R3ℓ | D²χ − χ/ℓ² = Kmn | FAIL (ℓ ≥ 63 Mpc; BTFR fails for every finite ℓ) | PASS | FAIL (ℓ ≤ 13 pc – 6.5 kpc) | PASS | PASS | FAIL | FAIL | **NOT REPAIRABLE** |
| P0 | (reference) | PASS | PASS | FAIL (0.610 / 0.694) | PASS | PASS (1.54e-5) | FAIL | FAIL | — |

**F2 detail** (6e10 M⊙ host at 50–250 kpc; CFG882 dwarfs H1–H3; both footings):
- the satellite's baryonic pull at its scale radius is 0.017–0.52 of Δa;
- the stars leave their medium in 9–106 Myr;
- the ambient medium re-settles 10²–10⁴·⁵ times more slowly than the satellite crosses itself;
- a static satellite phantom would be cut by 0.10–0.73 dex (an EFE).

**CFG925 R3 (no satellite EFE) is not respected** by any tethered sector. The tethered sector would leave satellites without a
settled medium (an estimate; assumptions in DERIVATION §6). The record reads satellites as above the EFE-free law.

**(g).** Class A's four defining features are:
- universal −∇Φ for all cold particles;
- turnaround-ball catchments built on the cosmic mean;
- a zero-sum source per catchment;
- an own-baryon phantom.

The catchment switch and the own-baryon phantom are non-local, and the source is zero-sum by prescription rather than derived
from an action. None of the four is produced by any local parent tested. The shear passes remain results of the class-A engine
only.

## Controls
- **K: all pass.** K1 2.2e-16 / 2.2e-16; K2 w = 0; K3 0.60954; K4 the Lagrangian route = K3, dust n = 1; K5 s_847 1.5398e-5;
  K6 R1 = CFG938 M3 (1.6445 / 1.8844).
- **MUTATE: all bite (exit 1 by design).**
  - M1: each repair removed gives 0.60954.
  - M2: double counting the phantom breaks the law (M2a 6.4 / 7.2; M2b 1.74 / 1.86).
  - M3: the χ̄ gradient moves n by 0.085.
  - M4: tether off gives Δa = 3.5e-16 g_host.

## Files and commands (one core, nice 10, < 0.25 GB, ~4 s each, nothing downloaded, no other lane touched)
- `CFG941_STAGE=K OMP_NUM_THREADS=1 nice -n 10 python3 cfg941.py` → `cfg941_K.out`, `cfg941_results_K.json` (exit 0).
- `CFG941_MUTATE=1 …` → `cfg941_MUTATE.out`, `cfg941_results_MUTATE.json` (exit 1 by design).
- `OMP_NUM_THREADS=1 nice -n 10 python3 cfg941.py` → `cfg941.out`, `cfg941_results.json` (exit 0; all checks pass).
- `DERIVATION.md` has the equations, every number, and the disclosures.

## Disclosures (full list in DERIVATION §6)
- **A1 (pre-result).** The numeric BTFR point moved from y = 1e-12 to 1e-14. The law's own correction is √y; at y = 1e-12 the
  exact law would have failed by 2.5e-13.
- **Code fixes before the first run.** brentq's rtol floor, K substitution, zero-density rows, a shadowed symbol, a sinh
  overflow, and literal test outcomes replaced by computed ones.
- **First MUTATE attempt.** It crashed on the satellite truncation bracket; M1–M3 had already printed. The fix touched only the
  F2 helper.
- **Final reruns.** K, MUTATE and main were rerun from one final script (sha256 cf4edd42…). The last edit was wording only:
  "> 4 decades" became the computed 4.0–6.7.
- **Implementation choices.**
  - Satellite medium truncated where u_s = u_h (or at its scale radius).
  - On-axis EFE.
  - R2's free mass in the phantom's shape.
  - R3θ example uses the total turnaround density.
  - Δ = 1, θ_s = H₀, Yukawa medium to 1 Mpc.
  - λ̄ = 0.
- **Open (not tested).** A ghost-free, probably latching, turnaround switch carried by a new field; or a medium held up by
  dispersion rather than a tether. The latter is a different theory.
