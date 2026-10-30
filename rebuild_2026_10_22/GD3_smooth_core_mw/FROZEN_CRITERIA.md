# GD3_smooth_core_mw — FROZEN CRITERIA (committed alone, before any script or graded number)

κ = ½ FITTED. Footings canonical / alt are computed and graded separately, never pooled. Cold dark energy, not matter. No
dark-matter particle. Nothing here says the data favour the framework or ΛCDM. Not "theory closed". One thread, nice 15,
peak RSS < 1 GB (X48 A4 runs are live).

## Question (owner, 2026-10-29)

GD2 found the flagship (route E + OS1 Burkert core law) passes the Milky Way only with short discs (R_d 1.93–2.27 kpc,
outside Licquia & Newman). The cap is structural: a Burkert core pulls at most 0.2545 · 2πGρ₀r₀. The smooth core
ρ₀/(1+x²)^(3/2) (X70_smooth_core_shape) pulls at most 0.3487 · 2πGρ₀r₀. **With the smooth shape and q re-calibrated on
SPARC for that shape, does the flagship pass the Milky Way inside the published priors?**

**Disclosure (look-elsewhere).** Before freezing, a chat check (not committed, not graded) ran GD1's McMillan baryons with
the smooth shape at OS1's *Burkert* q_f, V_last 229: V_c(R₀) 218.6 / 221.7, K_z(R₀) 72.1 / 72.9, χ²_Ou 124 / 147. That
row was seen. The graded rows here use the re-calibrated q and X5's box, which were not seen.

## Stage S: SPARC calibration of q for the smooth shape (OS1 rule, shape swapped, nothing else)

- OS1's machinery (SC1 → X38 → X30, read-only, exec'd in a namespace exactly as OS1 does). The ONLY change: the halo mass
  function B(x) in both the SC1 and X38 namespaces becomes the smooth core's,
  M(<r) = π Σ r₀² B_S(r/r₀), with B_S(x) = 4 [arcsinh x − x/√(1+x²)] and Σ = ρ₀r₀.
  X38's A1 compact root is kept (solve_r0 uses the swapped B).
- Σ_i = Σ_a₀ (σ_i/σ_ref)^q, σ_i = V_last/√2, σ_ref 70.50 km/s, Σ_a₀ 106.879 / 129.165 M☉ pc⁻².
- q_fS = argmin of the SPARC rms (EM1 background A) on 0.00–1.20 in steps of 0.02, refined in steps of 0.002 within
  ±0.02 of the coarse minimum (OS1's grid).
- **Gate:** EM1's line at q_fS (rms ≤ 0.110 and 0.50 ≤ median Υ ≤ 0.80). If it fails on a footing, that footing's
  class is **SPARC LINE FAILS**; its Milky Way rows are still computed and printed, labelled reported only.
- Background B at q_fS is reported only. OS1's cluster cells and dwarfs are NOT graded here.

## Stage M: Milky Way on X5's box (GD2 rules, shape swapped, q = q_fS)

- Everything as in GD2's frozen criteria (78f30f7368): X5's 175-cell family and grid, X5's Licquia & Newman tags, P4's
  Newtonian solver and observables, EM1's M200 relation (background A primary, B reported), X38's A1 compact root.
- Halo: smooth core with Σ = Σ_a₀ (V_last/√2/σ_ref)^q_fS; g_h(r) = G π Σ r₀² B_S(r/r₀) / r².
- PRIMARY V_last = 172.98 km/s (Ou+24's last point); VARIANT V_last = 229.05 km/s, its own graded row, never pooled.
- Lines L1 (V_c(R₀)), L2a (χ²_Kz ≤ 67.459), L2b (|K_z(R₀) − 66.4| ≤ 4.4), L3 (χ²_Ou ≤ 59.893), distance D: exactly
  GD2's.

## Class per footing (PRIMARY, background A), first match wins

0. **SPARC LINE FAILS** (stage S gate).
1. **FEASIBLE IN PRIORS:** at least one cell passes L1, L2a, L2b and L3 with tag_Rd_IN and tag_Mstar_IN both true.
2. **FEASIBLE (WIDE PRIORS ONLY):** all four lines pass in some cell, but none with both tags true.
3. **V+K ONLY:** L1, L2a and L2b pass together in some cell, but no cell passes L3.
4. **INFEASIBLE:** no cell passes L1, L2a and L2b together.

Lane verdict: the two footings' classes, printed separately. If they agree, the verdict is that class; otherwise
UNDECIDED (footings disagree). The VARIANT row is reported beside PRIMARY under the same rules, never replacing it.

**Reported only (not graded):** the McMillan 2017 cell (GD1's baryons) at q_fS, both V_last; the box at OS1's Burkert
q_f (0.892 / 0.748) with the smooth shape; the best in-prior cell's D.

## Checks (all must pass in the normal run)

- **K0:** with the Burkert B, stage S reproduces OS1's q_f (0.892 / 0.748) and SPARC A rms (from
  `os1_out_of_sample_results.json`) to 1e-9.
- **K1:** B_S against quadrature of 4∫₀ˣ t²(1+t²)^(−3/2) dt at x ∈ {0.3, 1, 3, 10}, |rel| < 1e-10; B_S(1) = 0.69707.
- **K2:** with the Burkert B and OS1's q_f, stage M reproduces GD2's class and best-cell D on all four graded keys
  (canonical / alt × PRIMARY / VARIANT, background A), D to 1e-9.
- **K3:** the halo raises both v_c and K_z(R₀) in every cell.
- **K4:** peak RSS < 1 GB.
- **MUTATE (`--mutate`):** stage M with q = 0 (smooth shape at Σ_a₀). Check K5 "VARIANT Σ factor > 1" must FAIL (exit 1).
  Outputs go to `*_MUTATE` files.

## Not done here

No refit of the M200 relation or of any baryon parameter. No grid refinement after results. No cluster or dwarf grade
(the smooth shape's cluster grade is X70/X73's). No AQUAL. No EFE (route E has none).
