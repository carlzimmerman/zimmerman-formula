# CFG262 — ADDENDUM 1 (written after the frozen criteria `FROZEN_CRITERIA.md` (1c1e4fe44) and BEFORE any CFG262 script exists or any level is computed)

Clarifications only; no pass line, threshold or decision rule is changed.

1. **Gas knobs (§4 (b)) are split so the wording "coefficient ×0.5 / ×2" is unambiguous:** knob **(b)** = {Σ_HI = 0, Σ_HI = 15 M⊙/pc², the HI term × 0.5, the HI term × 2} (CFG236's `Sig` and `gcoef`, routes (ii) and (iii)); knob **(b2)** = {the H₂ coefficient μ_mol × 0.5, × 2} (CFG236's `mu_scale`, route (ii) only). Both enter the recipe half-width by the rule of §4 (largest |Δ log₁₀ s\*| inside each knob, quadrature over knobs).
2. **The recipe half-width's knob list is therefore** (b), (b2), (d) the natural-log μ_mol reading (route (ii) only), (e) the kernel P2, and the historical-estimator alternative; the pressure term (a) and the drifts (c) are reported separately and are not in the half-width, as frozen.
3. **Row labels** are `z{1,2,3}-route{i,ii,iii}-{b,bD}`; the bootstrap seed of a row is crc32(label) mod 100000; the historical-estimator interval uses the same seed with the prefix `HIST|`.
4. **Reading D1** uses the dispersion σ_1 of the same run file at |rad_Re| = 1 (`load_dat`'s `s1`) and the inclination of the catalogue; a galaxy whose v_f(R_e) or σ_1 is not finite is dropped from every reading that needs it and counted per third (the dropped galaxies are the same in the b and bD sets only if both are finite; the third's count is reported per row).
5. **The rival's expected change for A5 and the flags** uses CFG223's `curves["H(z)"]` (Ω_m = 0.3153), not CFG236's E(z) at 0.315; the two differ by less than 0.002 in log₁₀ over this range.
6. **Stage A prints counts, the baryon-side distribution of y, and noiseless-world levers only.** It reads the run files only to count finite values (C6); no g_perp, D or level is formed from them.
