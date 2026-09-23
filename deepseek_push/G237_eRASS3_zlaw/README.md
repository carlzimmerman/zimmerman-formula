# G237 — The z-extension of the cluster closed form (derived, sympy-verified)

**Sibling:** G236 (eRASS:3/eROSITA DR2) registered the virial-T ratio null; G237 **derives the
mechanism** behind it from the committed pieces and pushes the closed form to its z-law.
All checks sympy/float-verified; 5/5 PASS. Greps verified that no prior lane carries these
statements (the repo's a0(z) work is footing/21-cm; the cluster sector was z = 0).

## The derivation chain (every input committed, no numbers invented)

**L1 — the phantom equipartition radius is exact.** From the committed Gauss-map charge
(G154, 18/18) M_ph(<r>) = √(GM_b·a0)·r/G and the committed equipartition M_ph(<r_M>) = M_b
(Q003, Lean), the 2-line solve gives

  **r_M = √(G M_b / a0)**

(sympy exact; cross-checks g03b's r_break = √(GM_b/a0)·α at α = 1, the MW r_M ~ 9.8 kpc).
Constitutive consequence, never written down before: **r_M ∝ a0^{−1/2}**.

**L2 — the sector scale relation's z-law.** At fixed observed M500 (Δ500 self-similarity
fixes R500; E2 fixes c_dust), L1 gives

  **u(z) ≡ r_M(z)/R500 = u(0) · [a0(0)/a0(z)]^{1/2}**

Framework (a0(z)/a0(0) = 1 − 3e-5·z, S3-05): **u is z-invariant to 1e-5 below z = 3**
(0.1850 at every z). M-RISE (Ciocan 1.59e-10 m/s²·z): u shrinks 39% by z = 1.
Falsifier F3: |u(z)/u(0) − 1| > 10% at z ~ 0.5 voids L2.

**L3 — the constitution row is a function of u only; therefore the pie is z-invariant.**
Using the committed G179 u-form (s_b = 1/(1 + c·x/u), s_ph = s_b/u at x = 1) with (c/u)_0 =
4.6506 pinned by the 12-cluster data pie:

  s_b(z) = 1/[1 + 4.6506·(a0(z)/a0(0))^{1/2}]

Framework: **s_b/s_ph/s_d = 0.177/0.569/0.254 at every z < 3** (data pie: 0.246 s_d — 0.008
is the u-form vs median-pie slack, stated). M-RISE: s_b → 0.137 by z = 0.5, 0.116 by z = 1.
Falsifier F2: any eRASS:3 lensing-pie measurement at 0.2 < z < 0.6 with |s_b − 0.177| > 0.020
voids the z-invariance of the sector (E2).

**L5 — the virial-T ratio laws (G236 E1 with its mechanism now derived).**
Case A, fixed M_b (richness-matched — the sharp primary): via Q001 (σ² = √(GM_b a0)/2,
Lean), ALL structure factors cancel:

  **T_X(z₂)/T_X(z₁)|_{M_b} = [a0(z₂)/a0(z₁)]^{1/2}**    (exact)

  framework 0.0000 dex vs M-RISE **+0.0996 dex** at z 0.1 → 0.5 (vs (1+z)^{3/2}: +0.1014).

Case B, fixed observed M500 (the X-ray-native selection): the L2/L3 correction
**enhances**, not dilutes — growing a0 grows f = 1 + (c/u)(z) in the same direction:

  R_T^B = [a0(z₂)/a0(z₁)]^{1/2} · [(1 + k₀ r₂^{1/2})/(1 + k₀ r₁^{1/2})]^{2/3},  k₀ = 4.65 (pie-pinned;
  dust-law route 3.0 — the committed −0.18-dex band),  r_i = a0(z_i)/a0(0)

  M-RISE: **+0.156 dex** (k₀ = 4.65) — framework still 1.0000. Selection convention changes
  the rival's signal by 1.56×, never the framework's.

**L4 — consistency anchor.** r_M(derived at M500 = 8e14 with M_b = 0.177·M500) → R500 =
1303 kpc vs the Δ500 self-similar R500 = 1411 kpc: ratio 0.92, inside the committed
−0.18-dex closure-offset band (G192 states R500 lies outside the dust law's 50–600 kpc
window). The derivation chain coheres with the pie and the u-chain to 8%.

## Falsifiers (registered; verdicts PENDING the eRASS:3 cluster WG products + SDSS DR20 z)

F1 |Δlog₁₀ T_X(z)/T_X(0)||_{M_b} > 0.010 dex at ≥ 2σ in any z-bin [0.2, 1.0]; M-RISE sits at
+0.10 dex → ~9σ with 50-cluster bins (0.076/√50 floor).
F2 |s_b(z) − 0.177| > 0.020 at 0.2 < z < 0.6 (lensing + X-ray pie). M-RISE: 0.040 at z = 0.5.
F3 |u(z)/u(0) − 1| > 10% at z ~ 0.5 (r_M reconstruction).

## Honest status

- All inputs are committed G-numbers; the two "new laws" (u(z) ∝ a0^{−1/2}; pie z-invariance)
  are derived, sympy-verified, and printed with their rivals — but nothing here is measured
  yet: DR2 is catalogue-only, so every verdict is PENDING data.
- L1's r_M = √(GM_b/a0) was known only in the r_break garb (g03b); the equipartition → z-line
  of reasoning is this lane's addition.
- Next wave candidates: Lean certificates for L1/L2 (the algebra is one-line each), and the
  eRASS:3 + SDSS DR20 z cross-match once the WG cluster products land.

## Files

- `G237_eRASS3_zlaw.py` (lane: 5/5 PASS, rerunnable), `.out`, `G237_results.json`.