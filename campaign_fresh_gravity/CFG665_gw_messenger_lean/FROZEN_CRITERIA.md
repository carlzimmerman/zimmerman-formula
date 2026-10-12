# CFG665 FROZEN CRITERIA: the GW messenger theorems (Lean 4, mathematics only)

Date: 2026-10-12. Written and committed ALONE, before any CFG665 Lean or number. Block CFG660–669 (CFG662/664 moot per
1812f594a; this lane takes 665). Nothing below may be edited after this commit; later changes go in dated README disclosures.

κ = ½ is FITTED. Footings (9.3603e-11 canonical, 1.1312e-10 alt) carried separately. The cold energy's mass is required. No
particle species. Not "theory closed". Lean certifies mathematics, not physics. No ΛCDM quantity enters: the only physical
inputs are a0, G, c, the Milky Way baryonic mass, radii, and the GW170817 arrival bound (1.7 s, an astrophysical measurement).

## 0. What has been seen (before any choice below)

- `prep_2026/gw170817_check/` (record): photons on g~ = g + B u u, gravitons on g ⇒ |c_γ − c_gw|/c = B/2, line integral with
  grad|B| = 4(ν−1) g_bar/c², void BC B→0; Δt ~ 3.5e7 s, EXCLUDED by 6–7 orders. ΛCDM audit 10-12: inputs are baryonic masses
  (host 1e11, MW 6e10 M☉), 40 Mpc, framework ν — no ΛCDM halo or cosmology. **Defect found:** that script uses the kernel
  ν = √(1+a0/g), not the record's ν_mono = ½ + √(¼ + a0/g) (user decision 09-26). CFG665 certifies a bound valid for BOTH.
- CFG663 (f5a9d1fe5): H-NL (response does not lens) EXCLUDED, SPARC over-predicted ×~1.8 (0.155 dex rms).
- Author's rough hand estimate before Lean (one MW crossing, ν_mono, M=6e10 M☉): Δt ≳ 4e6 s, i.e. ≳ 1e6 × the 1.7 s bound.

## 1. Theorems to certify (zero `sorry`, axioms ⊆ {propext, Classical.choice, Quot.sound})

- **T1 local delay.** For 0 ≤ B < 1: 1/√(1−B) − 1 ≥ B/2 (photon on g~ lags the graviton by at least B/2 per unit c·time).
- **T2 path delay.** If on a path segment of length L the integrand f ≥ 1/√(1−B) − 1 with B ≥ B_min ≥ 0 (integrable), then
  ∫ f ≥ B_min L / 2. Also: Δt ≥ 0 always, and two messengers on one metric (B ≡ 0) have Δt = 0 exactly.
- **T3 kernel floor (both kernels).** For 0 < g ≤ a0: (ν_mono(g) − 1) g ≥ √(a0 g)/φ (φ = golden ratio) and
  (ν_sqrt(g) − 1) g ≥ √(a0 g)/(1+√2); hence both ≥ √(a0 g)/(1+√2).
- **T4 accumulated tilt.** If B is differentiable on [r1, R] with B(R) ≥ 0 and B'(s) ≤ −K/s there (K > 0), then
  B(r) ≥ K ln(R/r) on [r1, R]. With a point-mass deep field, K = 4√(G M a0)/((1+√2) c²) (from T3, grad|B| = 4(ν−1)g/c²).
- **T5 no hiding direction.** ‖x − y‖ ≥ ‖x‖ − ‖y‖ in ℝ³: a straight sightline from any point at radius ≥ R2 to the Sun at radius
  ≤ r1 spends length ≥ R2 − r1 inside the shell r1 ≤ r ≤ R2 — independent of sky direction. (Curved paths: the radius is
  1-Lipschitz in arclength — cited, not certified.)
- **T6 numeric corollary (both footings).** MW inputs: M_enc ≥ 5e10 M☉ for r ≥ r1 (stated input, conservative vs 6e10),
  r1 = √(G M a0)/a0-deep radius rounded UP to 10 kpc, R = 300 kpc (void BC at R, the record's most favourable choice),
  shell used for the bound [10 kpc, R/e rounded down to 110 kpc] where ln(R/r) ≥ 1. Certify Δt_MW ≥ Δ_lo with Δ_lo / 1.7 s
  ≥ 10^5 (the threshold; report the certified number), per footing, by norm_num from T1–T5.
- **T7 CFG663 double count.** If lensing follows the law (g_lens = F) and the response does not lens, the required cold term is
  F − g_bar, and H-NL dynamics are 2F − g_bar. With F ≥ g_bar > 0: 1 ≤ (2F − g_bar)/F < 2, and → 2 as g_bar/F → 0 (deep).
  I.e. the non-lensing branch counts the law twice; CFG663's ×1.8 sits inside this window.

## 2. Classes

- **CERTIFIED** if all of T1–T7 compile with zero sorry and standard axioms, and T6's certified ratio ≥ 1e5 on both footings.
- **PARTIAL** if T1–T5, T7 compile but T6 falls below 1e5 on either footing (report the number; no rescue by changing inputs).
- **FAIL** if any of T1–T5, T7 cannot be proved as stated (record the obstruction; a false statement is a result).

## 3. MUTATE (`CFG665_gw_messenger_lean_MUTATE.lean`, must FAIL to compile at the intended theorems)

- M1: T1 with B/2 replaced by B (false near B→0: 1/√(1−B) − 1 ~ B/2 < B).
- M2: T3 floor for ν_sqrt with 1/(1+√2) replaced by 1/φ (false: ν_sqrt's floor is weaker).
- M3: T7 upper bound 2 replaced by 1.5 (false in the deep regime).

## 4. Scope statement (written now)

This certifies: any sector that bends light but not gravitational waves (or the reverse) by the framework's own deep-MOND tilt is
excluded by GW170817 from **every** sky direction through the Milky Way alone; a single shared metric gives exactly zero. It does
not certify that the framework is right, that cold energy exists, or anything about GW decay into a scalar (moot for real cold
mass; would need astra's action). Machine: Lean is light; `nice -n 10`; allowed while the 1024³ run is live.
