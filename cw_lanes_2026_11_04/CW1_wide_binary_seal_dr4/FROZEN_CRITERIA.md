# CW1_wide_binary_seal_dr4: FROZEN CRITERIA

Written 2026-11-04. These criteria are committed alone, before any CW1 script or number. Lane proposed 11-04 as CW1 in a local planning brainstorm. κ = ½ FITTED, held fixed. Footings never pooled. No cold component, no particle. Not theory closed. Nothing here says the data favour the framework. **`prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md` and everything it hashes are never edited.** This lane seals a separate prediction beside it. Fetching DR4 later needs the owner's yes.

## Question
- What does each filter form still on record predict for Gaia DR4 wide binaries, once QUMOND's ν gets the Newtonian external field?
- What vacuum scale g* do the solar system and the DR3 inner shape allow, and does it contain c√(Gρ) from the native BAO ruler?

## Stage 0 (done before these criteria; not blind)
KT20 (`kt20.py`, `GE = (1.9e-10, 2.32e-10)` in `nu(np.sqrt(ge*ge + h*h)/a0)`) puts an **observed** field into QUMOND's ν. 1.9e-10 is BN11's observed g_e and 2.32e-10 is KT16's observed field. KT21 inherits 1.9e-10. **Both carry the CZ1 defect.** The CW3 sweep records the same rows.

## Fields (frozen)
- Observed Galactic field at the Sun: **primary 1.9e-10** (KT20, for continuity), beside 1.778e-10 (the DR4 primary) and 2.32e-10 (KT16/CZ2 Cassini).
- Each is converted to the Newtonian field by inverting the simple ν on each footing: g_N = g²/(g + a0), as CZ1/CZ2 do.
- a0: canonical 9.3603e-11, alt 1.1312e-10.
- g* = a0/κ = 2 a0 unless scanned (stage 2).
- ν(y) = ½ + √(¼ + 1/y), the KT/CZ simple ν.

## Forms (frozen)
- **N.** Newton.
- **PQ.** Plain QUMOND. Reference only: it fails Cassini (KT16) and the planets (AZ12) on record.
- **LOC3, primary.** KT26's local rule ξ_loc = |g|²/(|∇|g|| g*).
  - |g| = ν(|g_N|/a0)|g_N|, with g_N the full **vector** Newtonian field (binary + uniform Galactic field).
  - |∇|g|| is its full 3D gradient magnitude.
  - The binary's mass is Gaussian-smoothed row-wise with the width ξ_loc taken at the point evaluated (KT27/CZ2's gather form).
  - ξ is clipped at 1e4 r_M.
- **LOC1, beside.** The same rule with CZ2's spherical quadrature |g_N| = √(g_N,int² + g_Ne²) and the radial derivative only. This is exactly the form CZ2 graded.
- **E55 and HALF, beside.** Global ε = 0.55 (KT17) and 0.5 (KT25) r_M. These fixed-width forms are not survivors: HALF fails CZ3's planet gate, and E55 is the same class (not graded on planets).
- TID is not computed. It fails the Milky Way with the full tidal tensor (KT29–KT32).
- **Survivor on record.** Only LOC, on alt (CZ2–CZ4), and only at Milky Way prior-corner cells. LOC on canonical fails the Milky Way and SPARC. Labels say so.

## Method (frozen)
1. **3D solver.** Axisymmetric QUMOND for a point mass M in a uniform Newtonian field η = g_Ne/a0 along z, in units r_M = √(GM/a0), so it is mass-free.
   - F = (ν(|g_f|/a0) − 1) g_f − (ν_e − 1) g_Ne, where g_f = smoothed internal field + g_Ne.
   - The phantom field is the curl-free projection of F, done by Legendre multipoles: a_l, b_l from F_r, F_θ by Gauss–Legendre quadrature, and stable radial recursions with no derivatives of F.
   - The internal field is the unsmoothed Newtonian field plus the phantom field, minus the uniform l = 1 field at the origin (the self-acceleration, reported).
   - γ_r(x, μ) = −g_int,r/(GM/r²).
   - Grid: ln x from ln 1e-7 to ln 1e5, 200 points per decade; 96 Gauss–Legendre μ nodes; L_max 64.
2. **1D form beside.** KT20's formula with the Newtonian η, directly comparable to KT20's table.
3. **Curves.** γ_r for M = 0.5, 1.0, 1.5 and 2.5 M☉ at s = 1, 2, 3, 5, 7, 10, 15, 20, 30 kAU: along the field (mean of μ = ±1), perpendicular (μ = 0), and the μ-average. Also the excess ratio (form − 1)/(PQ − 1).
4. **DR3 inner shape (KT21's Q).**
   - KT21's estimator, DR3 extract, seeds and K = 40 orbits per pair, copied verbatim.
   - A separate seeded node angle Ω.
   - The Galactic-centre direction for each pair from its (l, b), taken as the Sun–GC direction (offset at most 2° for d ≤ 250 pc).
   - μ = r̂·ê per orbit; ṽ_model = ṽ_N √γ_r(x₃, μ), KT21's local circular scaling.
   - z = (Q_obs − Q_pred)/√(σ_stat² + 0.020²).
5. **DR4 statistic.**
   - The frozen DR4 pipeline module is imported **read only**: bytecode writing off, SHA-256 recorded, no file in `prep_2026/` written.
   - Its master population is built (1e6 instead of its 3e6, for memory; stated) with its DR4 noise and its declared-shape model grid on each footing.
   - A synthetic catalogue (N = 30,000, 4 realisations) carries each form's μ-averaged boost γ_v(y_true) = √⟨γ_r⟩_μ.
   - Reported: the γ_inf the frozen fit returns (mean ± spread), and the bin-median ratio to Newton per pipeline bin.
6. **Stage 2, g* scan.** For LOC3 and LOC1, g*/a0 = 2^(k/4) for k = −4 … 12 (0.5 to 8) on each footing. At each g*:
   - Cassini q/ceiling: 3D solver, M = 1 M☉, η_N from 2.32e-10, KT16 ceiling 5.2e-27 s⁻². Q2 is 3 × the l = 2 potential coefficient at the origin.
   - Planets: CZ3's exact secular-rate code and AZ12 bounds, with the l = 0 phantom field from the 3D solver; pass if every Z ≤ 2.
   - DR3 Q: |z| ≤ 2.
   - **Allowed set:** the g* values that pass all three.
   - g*_vac = c√(Gρ) from CFG689 P3 at z = 0:
     - canonical: 2 × [9.00, 9.70]e-11, i.e. 68 % [1.80, 1.94]e-10, median 1.870e-10;
     - alt: ρ_total = ρ_DE + ω_m ρ_crit,100 with P3's ω_m.

## Checks (frozen; a failed check is reported and left failed)
- **K1.** η = 0, PQ: γ_r is independent of μ and equals ν(x⁻²) to 1e-6.
- **K2.** Deep EFE (x = 30, primary η): PQ γ_r(μ) is within 1 % of ν_e(1 + (K_e/2)(1 − μ²)), where K_e = dlnν/dlny at η.
- **K3.** Cassini with the CZ2 field: HALF q/ceiling reproduces CZ2's 1.179 / 2.97, and LOC1 reproduces 0.003948 / 0.02147, each within 2 %.
- **K4.** The 1D form with the observed 1.9e-10 reproduces KT20's `gamma_plain` / `gamma_filter` to 1e-10.
- **K5.** The Q code with the 1D form and 1.9e-10 reproduces KT21's committed Q_pred (Newton, plain, filter) and Q_obs to 1e-6.
- **K6.** The pipeline import: injecting its own declared shape at γ_inf = 1.00 and 1.1614 recovers each within max(2σ, 0.02).
- **K7.** Convergence: L_max 96 / N_μ 128 changes the seal's γ_r values by ≤ 0.003 and q by ≤ 2 %.
- **MUTATE twin** (ν ≡ 1, separate outputs). γ_r ≡ 1 for every form, every Q_pred equals Newton's, and q = 0. Exit 1 by design.

## Labels (frozen)
- **Separation from plain QUMOND, per form and footing:**
  - by Q: |Q_form − Q_PQ| / 0.020 (KT21's σ_sys, the floor DR4 can't beat);
  - by γ_inf: |γ_inf,form − γ_inf,PQ| / 0.028 (the pre-registration's σ_tot).
  - **SEPARABLE** if either is ≥ 3; **MARGINAL** if the larger is 2–3; **NOT SEPARABLE** if both are < 2.
  - The same three lines against Newton.
- **DR3:** CONSISTENT (|z| ≤ 2), TENSION (2–3), EXCLUDED (> 3), as in KT21.
- **g\*:**
  - MATCHES VACUUM SCALE: the allowed set is bounded on both sides within a factor of 4, and contains g*_vac's 68 % interval.
  - CONSISTENT, UNINFORMATIVE: it contains g*_vac but is one-sided or wider than a factor of 4.
  - EXCLUDES VACUUM SCALE: g*_vac is outside the allowed set.
  - NO ALLOWED g\*: the set is empty.
- **Stage 3:** `SEALED_PREDICTION.md` and its SHA-256 are committed only if K1–K7 pass, or a failed check is shown not to touch the sealed numbers and is stated in the seal. The seal lists, per form and footing:
  - the γ_r curves;
  - Q_pred;
  - the γ_inf the frozen pipeline would return;
  - the separation labels.

## Limits stated now
- The one-body point-mass treatment.
- The local circular scaling (no orbit integration).
- The Galactic tide is neglected.
- The μ-averaged boost is used in the pipeline injection, since the pipeline's population has no Galactic orientation.
- LOC3 extends a rule that was graded in 1D (LOC1), and the two may differ in the external-field regime. Both are sealed, with LOC3 as primary.
