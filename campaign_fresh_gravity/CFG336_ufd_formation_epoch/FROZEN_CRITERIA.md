# CFG336 FROZEN CRITERIA: formation-epoch density of the native cold mass vs the ultra-faint shortfall

Written and committed before any score. κ = ½ is FITTED and fixed. Both footings (a₀ = 9.36e-11, 1.13e-10 m s⁻²). Kernel ν_mono (identical to the record's exponential kernel in the dwarf regime, AUDIT_UFD row 3). No DM particle; the cold component's mass is required. No downloads, no scans: z_f is fixed a priori per class below and never tuned.

## The candidate (derived, not fitted)

1. **Mass (record's own, CFG35 / CFG313):** the cold component collapses with the baryons at the cosmic ratio, M_c = M_b / f_b, f_b = 0.157126 (Planck 2018 ω_b = 0.02237, ω_c = 0.1200). M_b = the lane's own baryon inventory (CFG45 `sigma_read`: Υ_V L_V + 1.33 M_HI, plus CFG42's infall gas for the gas=True satellite rows exactly as CFG45 does).
2. **Density set by the collapse epoch:** the region collapses at z_f with mean interior density Δ_c ρ_m(z_f), Δ_c = 18π² (top-hat, Einstein–de Sitter; Ω_m(z) > 0.9 for z ≥ 2, declared approximation also used at the z_f = 0 control), ρ_m(z) = ρ_m0 (1+z)³, ρ_m0 = 2.7754e11 (ω_b+ω_c) M☉ Mpc⁻³ (h-free). Hence
   r_f(z_f) = [3 M_c / (4π · 18π² · ρ_m0 (1+z_f)³)]^{1/3}  ∝ M_c^{1/3} / (1+z_f).
3. **Profiles (declared; the record has no z-dependent collapse profile, so the record's own parameter-free shape is primary):**
   - **P1 (primary):** singular isothermal truncated at r_f — CFG313's V2 shape with its truncation radius replaced by the collapse-epoch radius: M_cold(<r) = M_c min(r/r_f, 1).
   - **P2 (variant, reported):** NFW with r_s = r_f / 4 (declared standard: concentration ≈ 4 at the collapse epoch, Zhao+2009), normalised to M_c at r_f.
   - **PB (profile-independent upper bound, reported and certified):** all of M_c inside the scored radius, M_cold(<r) = M_c.
4. **Bookkeeping (cited, followed exactly):**
   - **(S) B's committed rule** (CFG35; CFG313 FROZEN_CRITERIA line 7; CFG45 reading S): g = ν g_N + f_ex (1−f_b) G M_cold(<r)/r², f_ex = max(0, 1 − M_ph,edge / [(1−f_b) M_c]), edge = 0.40 r_ta_law. f_ex depends only on total masses, so (S) is z_f-independent by construction; it is scored anyway.
   - **(M) the radial max = CFG4 T5's identity bookkeeping** (dark = max(phantom, cosmic share)) written locally (CFG45 reading M): g = g_N + max((ν−1) g_N, (1−f_b) G M_cold(<r)/r²).
   - Diagnostic only (NOT B, reported): **(A)** additive, g = ν g_N + (1−f_b) G M_cold(<r)/r², no switch.
5. **Scored radius and estimator:** CFG45 `sigma_read` unchanged: r = (4/3) r_half, half the baryons inside, σ² = g r / 3; KM median with upper limits; the record's bootstrap (1000, seed 42) and Υ_V 1–4 floor.

## z_f inputs (declared before scoring)

- On-disk ages: the LVD `age` column is filled for 4 systems only (Carina IV 12.5, Phoenix III 11.8, Pegasus VII 10.0, NGC 55-dw1 6.5 Gyr); no SFH/quenching table is on disk (Weisz+14 absent, CFG317). Too few to use, so the **a-priori class split** is used:
  - M_V > −7.7 (ultra-faint; MW, M31): z_f = 8, range 6–10.
  - M_V ≤ −7.7 (classical MW and M31 satellites) and all LV field dwarfs: z_f = 3, range 2–4.
  - Outer globulars: no cold component; unaffected by construction (CFG333 R2 rows reproduced from its JSON).
- Error: the record's terms ⊕ f_zf = ½ |median(z_f lo) − median(z_f hi)| (class range). For readings that do not move, f_zf = 0.

## Populations and statistics (the record's own)

MW ultra-faints (CFG45 UF, KM median, 31 + 9 limits); MW classicals (CFG45 CL "cls", gas=True); M31 Collins+13 ("col") and M31 LVD ("m31"); LV field dwarfs (CFG58 d2 via CFG313's recipe). Pass = |z| < 2.

## Decision (per reading (S), (M); P1 decides, P2 reported)

- **SOLVES:** UFD |z| < 2 AND classicals, both M31 rows, LV field all |z| < 2, on BOTH footings.
- **PARTIAL:** UFD median offset ≤ ½ of the baseline (+0.325 → ≤ +0.162 canonical; +0.304 → ≤ +0.152 alt) without any other row failing, both footings.
- **NOT:** otherwise.
- **Declared expectation (hand pre-flight):** NOT. The whole native cold share (1−f_b) M_c = 5.36 M_b is expected to be below the law's own phantom inside (4/3) r_half for every ultra-faint, so (M) cannot switch on for any profile and (S) has f_ex = 0 (CFG313). The PB bound tests this per object.

## Controls

- **C1:** z_f = 0 for all reproduces CFG313's native rows (= law rows; UFD +0.325 / z 3.77 canonical, +0.304 / 3.55 alt) to 1e-6 dex.
- **C2:** the AUDIT_UFD baseline (audit_ufd_results.json) is reproduced to 1e-4 dex.
- **C3:** r_f obeys r_f ∝ M_c^{1/3}(1+z_f)^{-1} to 1e-12, and P1/P2 enclose M_c at r_f.
- **MUTATE (CFG336_MUTATE=1, separate `_MUTATE` outputs):** z_f permuted at random (seed 336) across all scored dwarfs (MW, M31, LV pooled). Check: the UFD offset under (A) must rise (degrade) vs the main run; under (M) it must not improve. If the main (M) reading is inert, its MUTATE row is identical and that is reported, not hidden.

## Screens (report only)
1. Does z_f-dependent density explain CFG335's 0.6 dex scatter / ΔM ∝ M_b^0.52? (analytic slope of P1 at fixed z_f, plus the needed multiplier k on M_c for UFDs to reach 2σ under (M)-PB and (M)-P1.)
2. Other framework-native untested ideas from the record: named with a one-line feasibility, not run.

## Lean
Certify with rational intervals (Mathlib, no sorry): per ultra-faint, (1−f_b) M_c < M_ph(<r) on both footings (from rounded-outward values in the results JSON), the lemma max(a, b) = a when b ≤ a, and the decisive |m| vs 2e inequality per population × footing × reading.
