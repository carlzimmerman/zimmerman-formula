# C6P_cassini_high_precision: FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Owner 11-04:** "Yes, rerun C6", under the 11-04 lift ("we can open new lanes that break stuff that is frozen to test
them out"). This test adopts nothing. The 10-24 v3s verdict (`covariant_push_2026_10_22/V3S_FINAL_VERDICT_2026-10-24.md`)
stands unless the owner changes it. κ = ½ FITTED. Footings canonical a0 = 9.3603e-11 and alt 1.1312e-10 m/s², never
pooled. **Not blind:** C6's numbers, AX1's grades and the D7c/D7d/E2 records are all seen. Not theory closed. Nothing
here says the data favour the framework. No file under `covariant_push_2026_10_22/` is edited; C6's code is imported
read-only (no bytecode written).

## Question

AX1 (`rebuild_2026_10_22/AX1_action_for_law/v3s/`) labels v3s **UNDECIDED, reading PASS** on G1–G4 because it reads
G2a from C6 (`covariant_push_2026_10_22/C6_literal_cassini/`), whose frozen check **C2 failed**: the isolated (x_e = 0)
comparison r_F = 0 vs r_F = 1 of the Route F kernel gave 3.8e-11 against < 1e-12. Does a high-precision rerun clear C2,
and does v3s then get a clean PASS or FAIL on the Solar-System gate?

## What cancels (diagnosis, from reading C6 before this file; to be confirmed by check H3)

C6's general in-plane kernel `chi_gen` builds A = (κ²/2)[r_F(I − k̂k̂) + k̂k̂] + J − k̂k̂ with entries such as
A_xx = r_F κ²/2 + j_p + (κ²/2 − 1)(1 − c²), and returns k̂·A⁻¹·k̂ = num/det. At x_e = 0 (J = I) and small κ the O(1) parts
of A cancel against the −k̂k̂ term: det = O(κ²) is formed from O(1) products (for κ = 0.01, det ≈ 5e-5 from terms ≈ 1),
so ~4–5 digits of float64 are lost. D7d's `chi` (r_F = 1) has the same (κ²/2 + j_p) − 1 subtraction. The identity is
exact (C6's C1); only the float evaluation is off.

## Method (both required, and required to agree)

- **Method A, high precision of the literal formulas.** C6's `chi_gen` (any r_F) and D7d's `chi`, transcribed line for
  line into mpmath, evaluated at **30, 50 and 80 decimal digits** on exactly C6's C2 grids (the float64 nodes converted
  exactly to mpf). The Route F integral I2 = ∫₀^∞ κ² χ₂ dκ (χ₂ the P₂ projection, (5/2)∫χP₂dc) is done by nested
  mpmath quadrature of the literal r_F = 0 kernel on [0, 10⁷] plus C6's analytic tail −4c₂/κ_max (truncation O(κ_max⁻³)
  ≈ 1e-21 relative), at the same three precisions.
- **Method B, analytic rewrite that removes the cancellation.** With x = x_e, q = κ²/2, s² = 1 − c², b = x(1 + x):
  - r_F = 0: χ = (1 + x s²) / [x(1 + x + c²) + q(1 + x s²)]   (from m = (1 + x s²)/(1 + x)², 1 − m = x(1 + x + c²)/(1 + x)²);
  - r_F = 1: χ = (q + 1 + x + b s²) / [(q + x)(q + 1 + x) + b(q + x + c²)];
  every term non-negative, so no subtraction. The κ-integral is done in closed form: κ²χ − 2 = −2(1 − m)/((1 − m) + qm),
  so I2 = −(5π/√2) ∫₋₁¹ P₂(c) √(x(1 + x + c²)/(1 + x(1 − c²))) dc (the isotropic 2 integrates to zero against P₂; the
  rearranged integrand decays as κ⁻², so the swap is legal). Evaluated in float64 (C2 grids) and by mpmath at 30/50/80.
- Q2 = −(2GM/5πL★³) I2 (C6/D7d's BN11/Hees sign), GM = 1.32712440018e20 m³/s², pc = 3.0857e16 m, R_Saturn = 9.58 AU.
- Fields: E1–E3 total g_e from D7b (as C6). E0 g_Ne = 6.913e-11 with g_e = g_Ne(1 + A_law(g_Ne/a0)) recomputed at each
  exact footing, A_law = (√(1 + 4/y) − 1)/2. x_e = g_e/a0.
- Single thread, < 1 GB, minutes, no download. Script `c6p_cassini_hp.py`; outputs `c6p_cassini_hp.{json,out}`,
  rerun `*_RERUN.*`, twin `*_MUTATE.*`.

## Gate lines (copied from AX1 common / AX1 v3s / C6, unchanged)

- **G2a Cassini Q2:** each of the 24 cells (L★ = 24, 50, 90 pc; E0–E3; per footing) inside the Hees+2014 2σ band
  [−3.0e-27, 9.0e-27] s⁻² (AX1: Q2 ≤ 9.0e-27) **and** the Park+2026 2σ band [−2.0e-27, 5.2e-27] (C6's R1 line).
- **G2b planets:** hedgehog GM/L★² (AX1 G2b) and C6's R2 Route F monopole, both < bound at Earth 8.7e-15, Mars 1.4e-15,
  Saturn 7.0e-15 m/s², at 24, 50, 90 pc.
- **G2c Cassini γ − 1 = (2.1 ± 2.3)e-5** (AX1 common G2c), 2σ band [−2.5e-5, 6.7e-5]. Structural entry carried from the
  record (X15 / A22: γ = 1, α1 = α2 = 0 at β = 0; one metric). Reported proxy, graded against the same band: an
  effective |γ − 1| ≤ 2(r_max/L★)², r_max = 11 AU, the hedgehog potential (GM/L★²)r over the Newtonian GM/r at the largest
  Sun distance on the Earth–Saturn line. It is a conservative order-of-magnitude bound, not a PPN derivation.
- C6's R3 (wide binary 1.5 M☉ at 20 kAU, γ_v − 1) is reported, not graded, as in C6.

## Checks (script prints `Hn PASS/FAIL value threshold`; exit 0 iff all pass)

- **H1 sympy:** Method B's two kernels equal C6's general kernel at r_F = 0 and r_F = 1; 1/m − 1 = x(1 + x + c²)/(1 + x s²);
  ∫₀^∞ −2(1 − m)/((1 − m) + κ²m/2) dκ = −π√(2(1 − m)/m). All residuals 0.
- **H2 = C2 rerun (C6's frozen tolerance < 1e-12, unchanged)**, the four C6 sub-items on C6's grids (r_F = 1 vs D7d chi;
  κ = 0 vs linear AQUAL; x_e = 0 r_F = 0 vs r_F = 1, relative, κ ≥ 0.01; r_F = 0 vs closed form): max < 1e-12 by
  Method A at **each** of 30, 50, 80 digits **and** by Method B in float64.
- **H3 diagnosis / C6 float reproduction where it cancels:** C6's float `chi_gen` recomputed here gives C6's recorded
  3.77e-11 (rel ≤ 1e-6), and its error against Method A at 80 digits is ≥ 1e-12 (the failure is reproduced and located).
- **H4 C6 float reproduction where nothing cancels:** C2's other three float sub-items equal C6's JSON (|Δ| ≤ 1e-15);
  C6's float `routeF_Q2` at C6's footings (9.36e-11 / 1.13e-10) equals C6's 24 R1 Q2 (rel ≤ 1e-12), and Method B at 50
  digits matches them (rel ≤ 1e-8; C6's own quadrature is ~4e-10); C6's float R2 planet ratios equal C6's JSON
  (rel ≤ 1e-12).
- **H5 known answer (AX1 K1, PAPER58/D7c):** plain QUMOND law Q2 (AX1's integral, reimplemented) at D7c's a0 reproduces
  D7c's `L` Q2, 8 cells, max rel ≤ 1e-2.
- **H6 A = B:** Method A and Method B I2 agree for all 8 exact-footing fields at every precision, rel ≤ 1e-14.
- **H7 precision ladder:** Method B I2 at 30, 50, 80 digits agree, max rel ≤ 1e-25; Method A, max rel ≤ 1e-14;
  the C2 sub-items fall with precision (each rung's max ≤ 10^−(digits − 10)).
- **H8 E0 field:** recomputed g_e(E0) at 9.36e-11 equals D7b's to rel ≤ 1e-12.
- **H9 AX1 V1:** hedgehog Mars at 24 pc = 0.173 of bound within 2e-2.
- **MUTATE twin (`--mutate`), ν ≡ 1:** A_law ≡ 0 in H5's QUMOND integral and J = I (x_e → 0 in the response) in both
  Route F methods. H5 and H4's Q2 reproduction must FAIL and every screened Q2 must be 0. Exit 1.
- **Byte-identical rerun:** the run is done twice; the two JSON files must have the same SHA-256.

## Labels (per footing; the lane verdict is the pair)

- **PASS:** every check passes, and every G2a cell, every G2b ratio and G2c sit inside their lines.
- **FAIL:** every check passes and any G2a cell, G2b ratio or G2c is outside: name it and the factor.
- **still UNDECIDED:** any check fails. Say which and why.

Carried from C6, not rerun here: C1, C3–C8 (Route N and linear validity) as C6 recorded them, including C6's note that its
C6 check passed on an unconverged Λ = 0.01 solve (weak). The 10-24 failures (clusters, growth/CMB, radiation era, hosted
dwarfs, MW disc) are outside this gate and stay open.
