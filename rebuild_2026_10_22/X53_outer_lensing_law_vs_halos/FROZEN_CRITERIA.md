# X53_outer_lensing_law_vs_halos: FROZEN CRITERIA (committed alone, before any script or number)

κ = ½ FITTED. Footings never pooled (canonical a₀ = 9.3603e-11, alt 1.1312e-10 m/s²). No dark-matter particle.
The route-E clumping w ≈ 0 component is "cold dark energy" (not matter, not a particle). ΛCDM is the external rival.
Not "theory closed". Nothing here may say the data favour the framework.

## Question

Do the KiDS-1000 isolated-lens ΔΣ profiles (Brouwer+21 Fig. 3, 4 stellar-mass bins, 15 radii 0.035–2.6 Mpc, released
60 × 60 covariance) separate:

- **(L) the galaxy law as fundamental**: v3s / AQUAL with μ = x/(1+x), isolated (y_e = 0; v3s screening is irrelevant at
  these radii per S2 L6), the phantom extending indefinitely (~1/r isothermal tail, no edge); from
- **(H) route E**: Newtonian gravity, baryons plus cold dark energy halos at the a₀/(2πG) Burkert floor (X38), M200
  from EM1's committed SPARC relation, truncated at R200, with X43's collapse core where it applies?

## 1. Data, units, isolation (no downloads; nothing new)

- B21 Fig. 3 data and covariance read exactly as CFG801/803/805/F2 read them (ESD_t / (1+K); cov / (1+K)²-column).
- Converted to the native background (h 0.679, Ω_m 0.3085) exactly as F2 `data_native(0.679)` (F2 L2–L4 frame).
- Isolation: B21's own isolated sample, as used by CFG801–805 and F2 Track A. No re-selection.
- Ranges (on B21 radius labels, as F2/CFG801): **primary R ≤ 0.31 Mpc** (one-halo dominated, 7 radii × 4 bins) and
  **all radii** (15 × 4).

## 2. Lens baryons (identical for both models; nothing fitted)

F2's inventory, executed read-only from `F2_outer_lensing/f2_outer_lensing.py` (sections 1 and 4 only):
record lens catalogue (`lr_lenses.npz`, LePhare + 0.15 dex, i.e. the record's Υ), per-lens source weights
(`cfg110_perlens.npz`), native h/Ω_m mass rescaling, cold gas by B21's relation, hot CGM 0.5 M★ inside 100 kpc
(r³ ramp), lens-weighted stack per bin.

## 3. Models

- **(L)** = F2's `stack_model` with CENTRAL and y_e = 0, i.e. F2 ladder row L4 (inventory + hot CGM, isolated AQUAL,
  linear M ∝ r tail beyond the grid). Zero fitted parameters.
- **(H)** per lens (stacked with the same weights and the same delta_sigma projector, `f2_aqual.delta_sigma`):
  M(<r) = M_bar,Newt(<r) + M_halo(<r).
  - M_b for the halo relation = M★ + M_cold (SPARC-equivalent baryons: stars + gas; the hot CGM is in the lensing mass but
    not in the relation, since SPARC M_b has no hot CGM). Disclosed in the ledger.
  - log M200 = a + b (log M_b − 10), EM1 committed R1 relation, background A: a = 11.18, b = 0.90 (from
    `em1_emergent_results.json`; not refit). R200 from 200 ρ_crit,0 with background A's h (X38's definition).
  - Burkert at fixed core surface density: M_halo(<r) = π Σ_core r₀² B(r/r₀), B(x) = ln(1+x²) + 2 ln(1+x) − 2 arctan x,
    r₀ the compact root with M_halo(<R200) = M200 (X38 A1; saturation counted and reported).
  - Σ_core = max(a₀/(2πG), η Σ_coll(M200)) (X43 rule). Σ_coll(M) from X43's committed table
    (`x43_collapse_core_results.json`, 1e11–1e15, log-log interpolation; bg A).
  - **c_f treatment (coordinator note):** PRIMARY c_f = 4 (X43's external value, η = 14.83). REPORTED VARIANT: X48's ng 48
    native c_f(M) (`x48_analyze_results_ng48.json`: 7.17 / 6.97 / 5.62 at 1e12 / 1e13 / 1e14; interpolated in lg M,
    flat outside, as `x48_regrade.py`), η = (4/(3B(1))) c_f^(5/4). Every reported number says which c_f it uses. I report
    the lens-weight fraction above each crossover; if the bins are dominated by sub-crossover lenses I say so and show
    the variant's Δχ² shift.
  - **Truncation form:** sharp 3D truncation, ρ_halo = 0 for r > R200 (M_halo = M200 beyond R200; delta_sigma tail
    "const"). The projection then carries the full M200 as a point mass at R ≫ R200.
- **(L2H), (H2H)**: (L) or (H) plus CFG805's two-halo term, rebuilt by executing CFG805's own `esd2h` code read-only
  (T1x P_grav at z = 0.2562, ξ by its Fourier transform with its 0.05 Mpc/h smoothing, ξ = 0 inside each bin's
  CFG804 derived edge REX = 0.343 / 0.442 / 0.433 / 0.429 Mpc, projected, ΔΣ_2h). Only change: the T1x JSON path is
  given relative to the repository, not as an absolute path. Template converted to native units with the data's own
  factor f (as F2 post-hoc (c)).
  - **b_eff ≥ 0 per bin is the only fitted quantity** (CFG805 profiles it per bin). Here it is profiled per bin per model
    (4 each), by non-negative least squares on the covariance-whitened residual, in each range separately. Same freedom
    for both models. Masses are NOT profiled (CFG805 profiled M_b; this lane does not: zero-knob baryons).

## 4. Statistic

Δχ² = χ²(H-type) − χ²(L-type) with the full released covariance (native-scaled): positive = the law fits better.
Reported per range for (L) vs (H) and (L2H) vs (H2H), total (full covariance) and per bin (each bin's diagonal block).
Also χ², p and b_eff for every model.

## 5. Verdict classes (graded on (L2H) vs (H2H), all radii, primary c_f = 4)

Per footing:
- **OUTER LENSING DISCRIMINATES: LAW**: Δχ²_all(H2H − L2H) ≥ +9.
- **OUTER LENSING DISCRIMINATES: HALOS**: Δχ²_all ≤ −9.
- **NOT DIAGNOSTIC**: |Δχ²_all| < 9, OR the two-halo systematics dominate, defined as: the per-footing class changes
  under systematic variant S1 (two-halo exclusion radius set to each bin's lens-weighted median R200 of (H), for both
  models), OR under S2 (b_eff capped at 1, the isolated-sample ceiling, for both models). The class must hold under
  both S1 and S2.
- Lane: the same class on both footings → that class; otherwise **UNDECIDED**. If step 0 (stop rule) fails →
  **UNDECIDED** with no grading.

If LAW: the README may say only "this test prefers the fundamental-law reading over route E's halos", nothing broader.

## 6. Step 0 (stop rule)

Rerun the committed CFG801, CFG803 and CFG805 scripts unchanged in a scratch copy (outputs land in scratch, never in their
folders) and require:
- CFG801 primary Δχ² +197 (canonical) / +234 (alt) and all-radii +753 / +813 within 1 (committed JSON values);
- CFG803 primary dC = +0.1 and all radii +2.8 within 0.2 (canonical);
- CFG805: K1 b = 0 Δχ² +148.7 and with two-halo +11.1 within 0.2.
Plus: K_L, my (L) reproduces F2's committed L4 χ²_all (160.70 canonical / 127.60 alt) within 0.05.

## 7. Reported (not graded)

- Per bin: the smallest radius where |ΔΣ_L − ΔΣ_H| > 1σ (σ = sqrt of the covariance diagonal), with and without 2h.
- Whether the two-halo term can mimic either model: fraction of the expected Δχ² between (L) and (H) absorbed when
  b_eff·T2 is fitted to their difference; plus F2's committed isolation-leakage numbers as context (no new run).
- Future survey: the expected Δχ² between (L2H) and (H2H) if the data were exactly one of them (Fisher-like), and the
  lens-number factor needed for 5σ (Δχ² 25) if the present one is short.
- Variants: X48 native c_f(M); R200 at ρ_crit(z_eff) instead of z = 0; EM1 background B relation (a 11.2).

## 8. Checks and MUTATE

- K0: step 0 (above). K_L: F2 L4 reproduced. K_T: (H) at R = 2.6 Mpc for a lens whose R200 < 1 Mpc equals the
  baryon + M200 point-mass ΔΣ within 1 % (truncation). K_N: (L)'s ΔΣ at 2.6 Mpc exceeds the Newtonian-baryon-only ΔΣ by
  > 3× in every bin (phantom present). K_B: Burkert closed form vs quadrature 1e-6 (X38 K1). K_R: peak RSS < 1 GB.
- **MUTATE** (`X53_MUTATE=1`, separate `_MUTATE` outputs): truncation removed (Burkert continued to 100 R200) AND the law's
  μ set to Newtonian (ν ≡ 1). K_T and K_N must FAIL and the run must exit 1.

## 9. Resources

One thread, `nice -n 15`, PYTHONHASHSEED=0, < 1 GB. No downloads. `compute_queue/` untouched. Nothing outside this lane
is written.
