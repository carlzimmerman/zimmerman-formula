# M2_cluster_compact — frozen criteria (written before any script or number; committed alone with the ledger)

Lane of the 2026-10-22 rebuild (`rebuild_2026_10_22/BRIEF.md`; doors `BRIEF.md` and `BRIEF_E_AUDIT.md` apply).
κ = ½ FITTED. Footings canonical a₀ = 9.3603e-11, alt 1.1312e-10 m/s², never pooled. No dark-matter particle.
Never "theory closed". Never "the data favour the framework".

## What the cluster cores need (record, verified by F1, H2, J1, K1)

Extra lensing mass ≈ 1.4–1.8 × the hot gas inside 0.3–1 Mpc and ≈ 0 beyond 1 Mpc (more concentrated than the gas).
Isolated galaxies need nothing extra (F2). Dwarf satellites need +0.89 dex (E3). The Solar System must be untouched (C6).

## Hypothesis (coordinator; frozen here)

K1's C2 component (DMPR tidal charge per baryon mass element, P = −2U; Φ_W = −Gℓ_Q ∫ρ_b/|x − x′|² d³x′; lensing 3/4 of
dynamics) came closest on F1's profile (χ² 7.0–16.0 vs 11.07) and passed isolated galaxies (≤ +13 %), but overshot dwarfs by
2.4–2.5 dex and the planets by 10²⁰–10²³. **Hypothesis:** the same component, screened by the theory's existing stiffness
length L★ through the record's isolated profile S(s), vanishes for the Sun and planets, is partly suppressed in dwarfs and
acts fully in cluster cores.

## The screened component (frozen)

- **S(s).** Re-solve CFG691's ODE −[q″ + 2q′/s − 2q/s²] + q|q| = 1/s² (vector Laplacian; t = ln s, s ∈ [1e-4, 1e4];
  CFG691's boundary conditions); S = s q. Below s = 1e-4 use the inner series q = ½ + A s + s²/16 (A from the solve:
  A = q′(s_min) − s_min/8; the s²/16 term follows from the ODE); above 1e4 use S = 1 − 1/s.
- **Per object:** ℓ_g = L★²/(2 r_M), r_M = √(G M_b/a₀), M_b = the object's total baryon mass (ledger L12). The object's
  own C2 dynamical acceleration is multiplied by S(r/ℓ_g) at 3D radius r: g_W,scr(r) = g_W(r) S(r/ℓ_g). Dynamical mass
  M_W,scr = g_W,scr r²/G; lensing density 0.75 dM_W,scr/dr / (4πr²). Dwarfs: s = r₁₂/ℓ_g with r₁₂ = (4/3) R_h (E3).
- **External objects' fields are not screened by the receiver** (a host's or the Galaxy's C2 field acts in full where the
  host itself is unscreened). Disclosed simplification (D7d/D10: the external-field response is not multiplicative).
- **One constant:** ℓ_Q, calibrated on F1 MID only (A_MID = 1, closed form, as K1), per footing, per h (0.672, 0.686),
  per L★. **L★ = 24, 50, 90 pc**, from D10/D7d/C6/D8, not fitted. No other knob.

**Disclosed before freezing (not blind).** Back-of-envelope estimates in my head:
- Clusters (M_b ~ 1e14 M☉) have ℓ_g ~ 1e-3 pc and galaxies (1e10.4–1e11.2 M☉) ℓ_g ~ 0.02–0.05 pc. So **O1 and R1 should
  equal K1's C2 numbers to ≲ 1e-6**: K1's C2 O1 FAILED (A_OUTER 0.75–0.80, Z −2.8 to −4.0; h 0.686 alt χ² 16.0) and its R1
  PASSED. **So WORKS is unreachable by construction**; the screening can move only R3, R5 and R6.
- Inside ℓ_g, S ≈ s/2, so the screened C2 term is GMℓ_Q/(ℓ_g r²): a pure 1/r² law, i.e. a change of the object's GM by
  the factor 1 + ℓ_Q/ℓ_g (≈ 160 for the Sun at L★ = 24 pc, ≈ 11 at 90 pc). Perihelion bounds cannot see a 1/r² term; they
  see the next term, GMℓ_Q A/(ℓ_g² r) with A ≈ −0.2 (CFG691 table). My estimate: ~10⁴–10⁵ × the Mars bound at 24 pc,
  ~10²–10³ at 90 pc.
- Dwarfs: S(r₁₂/ℓ_g) ≳ 0.05–0.9 for typical systems, against an overshoot of ~10^3.4: an overshoot of ≳ 1 dex should remain.

## Graded lines (each on both footings; a line passes at an L★ only if it passes at the h 0.672 AND the h 0.686 calibration)

- **CAL:** ℓ_Q > 0 and finite.
- **O1, F1 OUTER and profile (K1's line):** |A_OUTER − 1| ≤ 2σ_OUTER AND profile χ² of the bins 3–7 residual stack
  (30-patch jackknife covariance, Hartlap) ≤ 11.07. INNER reported. Compactness reported: M_lens,W/M_gas (median cluster) at
  0.5 / 1 / 2 / 3 Mpc.
- **R1, isolated galaxies (F2's four masses, K1's A3 point-source formula):** ratio ∫ΔΣ_W d ln R / ∫ΔΣ_law d ln R over O1
  (0.4–1.1 Mpc) and O2 (1.1–2.6 Mpc), with ΔΣ_W = (9/16) M_b ℓ_Q S(R/ℓ_g)/R³ (S at the projected radius bounds the screened
  value from below; max |1 − S| over the bands printed). PASS iff ≤ 0.14 in both bands for all four masses.
- **R3, dwarf satellites (E3 CSV, central values, K1 A1 baseline):** baseline r_i = log10(M_dyn,i/M_pred,i),
  M_pred = B_scr(L★) M★/2 with E3's own `B_scr` at the same L★. With the component:
  r_i′ = r_i − log10(1 + M_W,i/M_pred,i), M_W = own screened C2 mass inside r₁₂ (Plummer with half-mass radius r₁₂,
  ℓ_Q M★ F_X/b × S(r₁₂/ℓ_g), b = r₁₂/1.305, F_X as K1) + host C2 term (K1's form, unscreened). PASS iff |median r′| ≤ 0.26 dex.
- **R5, Solar System:**
  - **R5a planets (graded):** the perihelion-equivalent anomaly δg_eq(r) = (1/2r) d(r² δg)/dr (for a near-circular orbit the
    apsidal advance of δg ∝ rⁿ is (n + 2)/2 times that of a constant δg; the C6 bounds are constant-δg bounds from perihelion
    σ's, BOUNDS.md §1.2). For the Sun's own screened term δg_eq = GM☉ℓ_Q q′(s)/(r ℓ_g²). Add the Galaxy's unscreened C2
    effective density at the Sun (from the MW Hernquist C2 field): δg = (4π/3)Gρ_eff r, δg_eq = (3/2)|δg|. PASS iff
    |δg_eq|/bound < 1 at Earth, Mars and Saturn.
  - **R5b Cassini Q₂ (graded, order of magnitude):** the Galaxy's C2 tidal quadrupole at the Sun, Q₂ = |Φ_W″ − Φ_W′/R| at
    R₀ (BN11-type traceless coefficient; convention factor ≤ 2 disclosed). PASS iff Q₂ < 9.0e-27 s⁻² (Hees 2σ); Park 5.2e-27
    reported.
  - Reported, not graded: K1's raw reading |δg|/bound; the GM change G_eff/G − 1 = 2(ℓ_Q/ℓ_g)q(s) for the Sun, the Earth
    (3.0035e-6 M☉) and a 1.5 M☉ binary; the L★ at which Mars's δg_eq would reach its bound (inversion δg_eq ∝ L★⁻⁴, one
    number, not a scan); Cassini γ − 1 is not affected at leading order (static Newtonian-gauge term; stated, not computed).
- **R6, wide binaries (1.5 M☉ total, separations 5 and 20 kAU):** γ_v = √(g/g_N) with g/g_N = [1 + 2c q(s)]/[1 + 2c q(s_cal)],
  c = ℓ_Q/ℓ_g, s_cal at 1 AU (masses calibrated dynamically at short separations), plus the Galaxy's C2 tide at the largest
  tidal eigenvalue × r over g_N. PASS iff |γ_v − 1| ≤ 0.25 at both separations. Reported: the reading against masses not
  calibrated dynamically, γ_v = √(1 + 2c q(s)).
- **R7, cosmology (reported only; growth belongs to F3/CFG960):**
  - background: the homogeneous mode of (−∇²)^{1/2}ρ_b is zero (k = 0), so ρ̄_eff = 0: no ΔN_eff, no H(z) change. C2 is not
    linked to the FRW Weyl dark radiation (K1). State plainly whether it is BBN-safe.
  - perturbations (linear modes are unscreened: their masses give ℓ_g ≪ 1/k): G_eff/G − 1 = (π/2)(k/a)ℓ_Q × ρ_b δ_b/(ρ_m δ_m)
    (dynamics; lensing 3/4). Report it at k = 0.01, 0.1, 1 h/Mpc at z = 0 and z = 1100, and the growth ratio D_W/D_GR at
    z = 0 from z = 99 (dust + baryons, both feel the potential, baryon pressure ignored, E-886 background, ℓ_Q = the
    canonical h 0.672 L★ = 24 pc value). Interpretation frozen: D_W/D_GR − 1 > 0.1 at k = 0.1 h/Mpc means "growth-breaking on
    linear scales unless the component is absent on FRW".

## Verdict rule

- **WORKS:** at some L★ ∈ {24, 50, 90} pc, CAL, O1, R1, R3, R5a, R5b and R6 all pass on both footings.
- **PARTIAL:** not WORKS, and at some L★ on both footings either (i) O1 passes and at least one of R3, R5a, R6 passes, or
  (ii) O1 fails but R1, R3, R5a, R5b and R6 all pass (the screening removes every small-scale failure while the cluster
  shape stays K1's near-miss).
- **FAILS:** otherwise. Report which lines fail, at which L★, and by how much.
Reported with every verdict: what the component physically is (a postulated term, counted in the ledger) and R7.

## Checks (script `m2_cluster_compact.py`; one line each; exit 0 iff all pass)

- **M1 profile:** solve_bvp converged with max relative ODE residual ≤ 1e-6; S reproduces CFG691's table (s = 0.01, 0.1,
  0.3, 1, 3, 10, 100, 1000) to ≤ 1e-3 absolute; |q(1e-3) − ½| ≤ 1e-3; the inner series matches the solve at s = 1e-2 to
  ≤ 1e-5.
- **M2 F1 reproduction:** cache sha256 961ea4fc…e720; the law reproduces F1's PRIMARY A_MID and A_OUTER (2 h × 2 footings)
  to ≤ 1e-6 relative; my linear projector agrees with F1's on the law to ≤ 0.5 % (K1 K6).
- **M3 K1 reproduction (S ≡ 1):** my unscreened C2 reproduces K1's committed C2 values: ℓ_Q (4 cells) and A_OUTER to ≤ 1e-6
  relative, profile χ² to ≤ 1e-4 relative, R3 median to ≤ 1e-6 dex, R5 Mars raw ratio to ≤ 1e-6 relative.
- **M4 E3 baseline:** E3's `B_scr` at L★ = 24 pc from the CSV columns equals the CSV `B_scr_L24` to ≤ 1e-6 relative for every
  system; the baseline medians equal K1's K9 central values (0.94566 / 0.90929) to ≤ 1e-4 dex.
- **M5 screened point mass:** (i) at s = 1e-4, g_W,scr r²/(GMℓ_Q/ℓ_g) = 2q → 1 within 1e-3; (ii) δg_eq from a finite
  difference of r²δg equals GMℓ_Q q′(s)/(r ℓ_g²) to ≤ 1e-3 at s = 1e-3 and 1e-1.
- **M6 tidal numerics:** for a Plummer sphere (b = 5 kpc) on the grid, Φ_W″ − Φ_W′/R at R = 100 b equals −8GMℓ/R⁴ to ≤ 1e-2.
- **M7 growth solver:** with ℓ_Q = 0 on an Ω_m = 1 background, D(a)/a is constant to ≤ 1e-4 from z = 99 to 0.
- **`--mutate`:** the scalar Laplacian in the profile ODE (−2q/s² term dropped, CFG691's M2): M1 must FAIL; outputs in
  `*_MUTATE.*`.

Runs: `OMP_NUM_THREADS=1 nice -n 15`, < 1 GB RSS, single thread, minutes, no downloads, no network. F1's measurement cache
is passed as argv[1] (a read-only copy in session scratch); nothing of another lane is written.
