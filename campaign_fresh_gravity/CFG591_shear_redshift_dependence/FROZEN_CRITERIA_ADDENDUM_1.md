# CFG591 FROZEN CRITERIA, ADDENDUM 1 (dated 2026-10-10): a declared variant with a0(z) tracking DESI DR2 w0wa dark energy

Added on the owner's instruction (relayed by the coordinator), committed alone, before any CFG591 result was looked at. At the time of this commit the only CFG591 numbers seen are the toy-launch header lines (Δ_ta(z), D(z), s_c* at four masses, per epoch, w = −1) and the MUTATE test of the projection code on z = 0 inputs (which reproduces CFG590 exactly by construction). No R(k, z > 0), A_eff or class has been seen. `FROZEN_CRITERIA.md` is NOT edited; its w = −1 PRIMARY and its verdict rule stand unchanged. This addendum adds one declared variant, reported side by side with the primary. It does not replace the primary verdict.

## A1. The variant ("DESI-tracking")

- **Dark energy:** flat w0waCDM with (w0, wa) = the weighted posterior mean of the DESI DR2 + CMB + DES-Y5 SN chain, read from `CFG549_dark_energy_evolution_prediction/cfg549_results.json` (`chains.desy5.w0wa_mean`; computed there from the on-disk chains as CFG511 reads them; 30% burn-in). ρ_DE(z)/ρ_DE(0) = f(z) = (1+z)^{3(1+w0+wa)} exp(−3 wa z/(1+z)). The other DR2 chains (CMB-only, Pantheon+, Union3) are NOT run; their a0(z) ratios are reported only.
- **The framework's a0(z):** a0(z) = a0(0) √f(z) (the record's tracking law a0 = κ c √(G ρ_DE); κ cancels in the ratio). a0(0) is each footing's value.
- **Background:** Ω_m, h, ω_b, n_s and σ8(z = 0) = 0.811 are kept at CFG556's values (declared: the variant isolates the dark-energy evolution; the chain's own Ω_m is reported, not used). Everything that depends on the background is recomputed with the w0wa H(z):
  - H(z), the age t(z) and t_obs;
  - the linear growth D(z) (growth ODE, D ∝ a early), hence σ(M, z), the Tinker08 mass function, the Tinker10 bias, the 2-halo normalisations;
  - the spherical-collapse shell ODE (r̈ = −Ω_m/(2 r²) − ½ Ω_DE f(a) (1 + 3 w(a)) r, with a(t) integrated alongside), hence Δ_ODE(z), δ_ta,lin, the EPS main-progenitor ODE and s_c*(M_ta, z);
  - Ω_m(z) for r200c;
  - Δ_ta(z) = 11.81 × Δ_ODE,DESI(z) / Δ_ODE,Λ(0) (the same anchor constant as the primary).
- **Kinetic toy:** rerun at all five epochs including z = 0 (90 cells: 5 z × 9 nodes × 2 footings), since a0(z), s_c* and r_ta all change. The method is otherwise unchanged (§1 of the criteria). These runs start after the primary toy run, ≤ 4 processes.
- **Same models** as the primary (PRIMARY, CFG557 TESTED, CFG556 cen / emg / r200scope), same k grid.
- **The ΛCDM-equivalent comparison model in the same background:** in R, the reference L-std / L-ta halo model uses the same w0wa background. In the projection, CAMB 1.6.6 with `set_dark_energy(w = w0, wa = wa, dark_energy_model = 'ppf')` provides the DMO HMcode-2020 P_NL, the linear P_L, the BAHAMAS feedback S_fb and the distances (σ8 = 0.811 at z = 0). `cfg590_shear.py` is exec'd with this ONE textual insertion after each `set_cosmology(...)` call. The "w0waCDM-DMO" comparison model (R ≡ 1) is judged by the same rule. The A_mod data (Amon & Efstathiou 2022, Preston+2023) were derived in ΛCDM. This is disclosed, not corrected.

## A2. Reporting

- R(k = 1, z) and s(z) for the primary and the DESI variant side by side, both footings.
- CFG590's frozen rule applied to the DESI variant (PRIMARY class, final class with mapping systematics, the VARIANT-SENSITIVE flag over the same mainline variants, the HIGH-Z-TAIL bracket, survivors' classes), side by side with the primary.
- The variant has no verdict authority of its own: the lane's verdict is the primary's. If the two classes differ, the README states it plainly as DE-SENSITIVE.

## A3. MUTATE teeth for the variant (cheap code-path checks; in `CFG591_MUTATE=1` runs)

- **MD1:** the DESI-path background with (w0, wa) = (−1, 0) reproduces the primary path at z = 0.5: D(z) ratio, age, Δ_ODE and the s_c* grid (both footings), each to ≤ 1e-6 relative. This bounds the ODE-vs-integral numerics.
- **MD2:** the DESI-path projection with (w0, wa) = (−1, 0) and R ≡ 1 reproduces CFG590's ΛCDM A_eff table to ≤ 1e-6.

## A4. Outputs (additional)

`cfg591_desi.py` (background patch helpers); toy results `cfg591_toy_DESI_results.json` / `.out`; halo `cfg591_halo_DESI_results.json` / `.out`; shear `cfg591_shear_DESI.out`, `cfg591_results_DESI.json`; MUTATE outputs `_DESI_MUTATE`. The README lists the halo model's ΛCDM-calibrated ingredients as inherited assumptions: the mass function, the bias and the concentration–mass relation (plus Moster13 stellar masses and the EPS progenitor form).
